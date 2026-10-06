"""
generate_all_charts.py -- charts and numbers of Chapter 13 (ATS): foundation models and conformal prediction
============================================================================================================
Course data (ats_data.py), chart style (ats_style.py), the engine fm_core.py (numpy, scipy, statsmodels, PyTorch on CPU;
open checkpoints Chronos-Bolt, Chronos-2, TimesFM 2.5 and TiRex, skipped if not installed). Every number on the slides
comes from here.
  * pretraining           the Chronos tokeniser on the BET index; accuracy against model size on our benchmarks;
  * zero-shot forecasts   Romanian hourly load (Energy-Charts, ENTSO-E data) day-ahead against the weekly naive, the
                          expert ARX of Ziel and Weron (2018), DLinear and N-BEATS; Chronos-2 with in-context calendar and
                          temperature covariates (Open-Meteo); EU HICP inflation (27 countries, Eurostat) against the random
                          walk, AR and damped ETS, multiple testing across countries; realised variance of Bitcoin
                          (Binance) and of the S&P 500 (Oxford-Man) against HAR; windows before and after the release of
                          the models (contamination check);
  * conformal prediction  the coverage of split conformal given the calibration set; CQR on the synthetic design of
                          Romano, Patterson and Candes (2019); the failure of a static calibration on returns; ACI on the
                          GARCH volatility design of Gibbs and Candes (2021); the step size gamma; weighted conformal under
                          changepoints (Barber et al. 2023); quantile tracking, conformal PID and EnbPI on Romanian load;
                          conditional coverage diagnostics;
  * calibrating models    conformal calibration of foundation-model intervals; VaR 1% and 5% of the BET and S&P 500 from
                          Chronos-2 and from conformalised deciles, against GARCH-t;
  * AI mini-case          how much a cherry-picked benchmark subset can change the verdict.
Output: charts/ats_ch13_*.pdf/.png, Quantlets/Ch_13/ch13_numbers.json
Run:  OMP_NUM_THREADS=1 ATS_CACHE=<folder> ATS_FM_CACHE=<folder> python3 Quantlets/Ch_13/generate_all_charts.py [name ...]
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import io
import json
import os
import sys
import urllib.request
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_style as st                                                                                 # noqa: E402
from ats_data import log_returns, load_close, read_omi                                                 # noqa: E402
from fm_core import (DECILES, DLinear, NBeats, TORCH, ar_forecast, ar_scorecaster, bh, christoffersen,  # noqa: E402
                     chronos_tokenise, conformal_quantile, cqr, crps_q, dm_test, enbpi, ets_forecast, fit_global,
                     fm_forecast, fm_load, fm_params, garch11_filter, garch11_fit, gmean, har_forecast,
                     holm, kupiec, mcs, online_threshold, pinball, predict_global, qlike,
                     set_seed, split_conformal)

warnings.filterwarnings('ignore')
st.apply()
SEED = 2026
REAL_RAW = 'https://raw.githubusercontent.com/danpele/Advanced-Time-Series/main/data/realized/'
REAL_DIR = next((p for p in [os.path.join(HERE, '..', '..', 'data', 'realized')]
                 + [os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..')]
                 if os.path.isdir(p)), '')
LOAD_API = 'https://api.energy-charts.info/public_power?country=ro&start={a}&end={b}'   # Romanian load, ENTSO-E data
METEO_API = ('https://archive-api.open-meteo.com/v1/archive?latitude=44.43&longitude=26.10&start_date={a}&end_date={b}'
             '&hourly=temperature_2m&timezone=Europe%2FBucharest')                     # Bucharest, ERA5-based archive
LOAD_YEARS = (2022, 2023, 2024, 2025, 2026)
LOAD_END = '2026-09-30'
LOAD_EVAL = '2025-01-01'                     # first forecast day of the day-ahead comparison (as in Chapter 1)
LOAD_WIN, LOAD_RES = 364, 182                # expert ARX window and residual window (days), as in Chapter 1
LOAD_CTX = 2048                              # hours of context for the foundation models (Chronos-Bolt maximum)
EU27 = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU',
        'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']
HICP = ('prc_hicp_minr', 'M.RCH_A.TOTAL.')   # HICP, annual rate of change, % (Eurostat)
INFL = dict(start='2000-01-01', first='2012-01-01', H=12)
RELEASE = {'Chronos-Bolt': '2024-11-25', 'TiRex': '2025-05-26', 'TimesFM 2.5': '2025-09-02', 'Chronos-2': '2025-10-30'}
PRE_END, POST_START = '2024-11-24', '2025-11-01'   # before the first and after the last release (Hugging Face dates)
RV_FIRST = {'btc': '2021-01-01', 'spx': '2010-01-04'}   # first forecast day of the realised-variance comparison
RET_FIRST = '2016-01-04'                     # first VaR forecast day (as in Chapter 9)
GS_START = '2003-01-01'                      # first day of the GARCH volatility scores (ACI design)
FMS = ['Chronos-Bolt small', 'Chronos-2', 'TimesFM 2.5', 'TiRex']
FM_COL = {'Chronos-Bolt small': st.Orange, 'Chronos-2': st.IDAred, 'TimesFM 2.5': st.Purple, 'TiRex': st.Teal,
          'Chronos-Bolt tiny': st.Amber, 'Chronos-Bolt mini': st.Amber, 'Chronos-Bolt base': st.Amber}
_MEM = {}


def save(name, save_it=True):
    st.check_no_grey(plt.gcf())
    if save_it:
        st.save_fig(name)
    else:
        plt.show()
        plt.close()


# =============================================================================
# 0. DATA
# =============================================================================
def get_bytes(url):
    """Download a public file once per session (no key); optional local cache folder in ATS_CACHE."""
    import hashlib
    import time
    if url in _MEM:
        return _MEM[url]
    cache = os.environ.get('ATS_CACHE')
    path = os.path.join(cache, hashlib.md5(url.encode()).hexdigest()) if cache else None
    if path and os.path.exists(path):
        _MEM[url] = open(path, 'rb').read()
        return _MEM[url]
    for attempt in range(6):                    # the Energy-Charts API limits the request rate
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ATS course)'})
            _MEM[url] = urllib.request.urlopen(req, timeout=180).read()
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            time.sleep(15 * (attempt + 1))
    if path:
        os.makedirs(cache, exist_ok=True)
        open(path, 'wb').write(_MEM[url])
    return _MEM[url]


def fm_cached(key, name, contexts, H, taus, **kw):
    """fm_forecast with an optional disk cache (folder in ATS_FM_CACHE): the forecasts of one experiment and model."""
    cache = os.environ.get('ATS_FM_CACHE')
    path = os.path.join(cache, f'{key}__{name.replace(" ", "_")}.npy') if cache else None
    if path and os.path.exists(path):
        return np.load(path)
    Q = fm_forecast(name, contexts, H, taus, **kw)
    if Q is not None and path:
        os.makedirs(cache, exist_ok=True)
        np.save(path, Q)
    return Q


def read_realized(fname, **kw):
    """A file of data/realized: local copy of the course data, otherwise the ATS repository on GitHub."""
    p = os.path.join(REAL_DIR, fname) if REAL_DIR else ''
    return pd.read_csv(p if p and os.path.exists(p) else REAL_RAW + fname, **kw)


def ro_load_hourly():
    """Romanian hourly electricity load (GW), local time, 2022 to LOAD_END (Energy-Charts, ENTSO-E transparency data):
    15-minute values averaged within each hour; a days x 24 table (DST days: 23 or 25 hours become 24)."""
    if 'load' in _MEM:
        return _MEM['load']
    parts = []
    for y in LOAD_YEARS:
        b = min(f'{y}-12-31', LOAD_END)
        d = json.loads(get_bytes(LOAD_API.format(a=f'{y}-01-01', b=b)))
        load = [x for x in d['production_types'] if x['name'] == 'Load'][0]['data']
        parts.append(pd.Series(load, index=pd.to_datetime(d['unix_seconds'], unit='s', utc=True), dtype=float))
    s = pd.concat(parts).sort_index()
    s = s[~s.index.duplicated()].tz_convert('Europe/Bucharest')
    df = pd.DataFrame({'y': s.values, 'day': s.index.tz_localize(None).normalize(), 'hour': s.index.hour})
    tab = df.groupby(['day', 'hour'])['y'].mean().unstack('hour')
    tab = tab.interpolate(axis=1, limit_direction='both').interpolate(axis=0, limit_direction='both')
    _MEM['load'] = tab.loc[:LOAD_END] / 1000.0
    return _MEM['load']


def bucharest_temperature():
    """Hourly 2 m temperature in Bucharest (Open-Meteo historical archive, ERA5-based), local time, days x 24."""
    if 'temp' in _MEM:
        return _MEM['temp']
    d = json.loads(get_bytes(METEO_API.format(a=f'{LOAD_YEARS[0]}-01-01', b=LOAD_END)))
    t = pd.Series(d['hourly']['temperature_2m'], index=pd.to_datetime(d['hourly']['time']), dtype=float)
    df = pd.DataFrame({'y': t.values, 'day': t.index.normalize(), 'hour': t.index.hour})
    tab = df.groupby(['day', 'hour'])['y'].mean().unstack('hour').interpolate(axis=0, limit_direction='both')
    _MEM['temp'] = tab
    return tab


def orthodox_easter(y):
    """Orthodox Easter (Gregorian date): Meeus' Julian algorithm plus 13 days (valid 1900-2099)."""
    a, b, c = y % 4, y % 7, y % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    mo, da = divmod(d + e + 114, 31)
    return pd.Timestamp(y, mo, da + 1) + pd.Timedelta(days=13)


def ro_holidays(years):
    """Romanian public holidays: fixed dates, Orthodox Good Friday, Easter and Pentecost (Sunday and Monday)."""
    out = []
    for y in years:
        fixed = ['01-01', '01-02', '01-24', '05-01', '06-01', '08-15', '11-30', '12-01', '12-25', '12-26']
        fixed += ['01-06', '01-07'] if y >= 2024 else []
        out += [pd.Timestamp(f'{y}-{m}') for m in fixed]
        e = orthodox_easter(y)
        out += [e + pd.Timedelta(days=k) for k in (-2, 0, 1, 49, 50)]
    return pd.DatetimeIndex(sorted(set(out)))


def eu_hicp():
    """Annual HICP inflation (%), monthly, of the 27 EU countries (Eurostat prc_hicp_minr, all items), common sample."""
    if 'hicp' in _MEM:
        return _MEM['hicp']
    url = ('https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/' + HICP[0] + '/' + HICP[1] + '+'.join(EU27)
           + '?format=SDMX-CSV&startPeriod=1999-01')
    t = pd.read_csv(io.BytesIO(get_bytes(url)))
    t['date'] = pd.to_datetime(t['TIME_PERIOD'] + '-01')
    P = t.pivot_table(index='date', columns='geo', values='OBS_VALUE')[EU27].loc[INFL['start']:]
    _MEM['hicp'] = P.dropna()
    return _MEM['hicp']


def btc_rv():
    """Daily realised variance of Bitcoin from 5-minute Binance returns (data/realized), in %^2; log RV."""
    d = read_realized('binance_daily_realized.csv', parse_dates=['date']).set_index('date')
    rv = d['btc_rv5'].astype(float)
    return rv[rv > 0].dropna()


def spx_rv():
    """Oxford-Man realized library v0.3 (Heber, Lunde, Shephard and Sheppard 2009): daily 5-minute realised variance
    of the S&P 500, in %^2."""
    d = read_omi()
    s = d[d['symbol'] == '.SPX'].set_index('date').sort_index()['rv5'] * 1e4
    return s[s > 0].dropna()


# =============================================================================
# 1. PRETRAINING: TOKENISATION AND SCALE
# =============================================================================
def fig_tokens(save_it=True, n=512):
    """The Chronos tokeniser on the last n daily closes of the BET: mean scaling, 4093 uniform bins on [-15, 15];
    a coarse 64-bin version to make the quantisation visible; the clipping of a series that leaves the range."""
    p = load_close('bet').iloc[-n:]
    ids, deq, s = chronos_tokenise(p.values)
    ids64, deq64, _ = chronos_tokenise(p.values, n_bins=64)
    width = 30 / (4093 - 1) * s
    rng = np.random.default_rng(SEED)
    ctx = 1 + 0.05 * rng.standard_normal(400)                                   # a context near 1, then the future
    fut = np.linspace(1, 25, 112)                                                # rises to 25 times that level
    _, _, sj = chronos_tokenise(ctx)
    centres = np.linspace(-15, 15, 4093)
    dj = sj * centres[np.clip(np.searchsorted((centres[1:] + centres[:-1]) / 2, fut / sj), 0, 4092)]
    jump = np.r_[ctx, fut]
    dj = np.r_[chronos_tokenise(ctx)[1], dj]
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 3.8))
    axs[0].plot(p.index, p.values, color=st.MainBlue, lw=1.3, label='BET close')
    axs[0].step(p.index, deq64, color=st.IDAred, lw=1.0, where='mid', label='64 bins (illustration)')
    axs[0].set_ylabel('index points')
    import matplotlib.dates as mdates
    axs[0].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    axs[1].plot(np.arange(len(jump)), jump / sj, color=st.MainBlue, lw=1.3, label='scaled series x / s (s from the context)')
    axs[1].plot(np.arange(len(jump)), dj / sj, color=st.IDAred, lw=1.2, ls='--', label='dequantised tokens')
    axs[1].axvline(400, color=st.Amber, ls=':', lw=1.2, label='end of context')
    axs[1].axhline(15, color=st.Forest, ls=':', lw=1.2, label='upper limit 15')
    axs[1].set_ylabel('scaled value')
    axs[1].set_xlabel('time step')
    st.fig_legend_bottom(fig, ncol=5, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch13_tokens', save_it)
    return dict(n=n, scale=float(s), width=float(width), maxerr=float(np.max(np.abs(deq - p.values))),
                maxerr64=float(np.max(np.abs(deq64 - p.values))), first=str(p.index[0].date()), last=str(p.index[-1].date()),
                jump_scaled=float(jump[-1] / sj), jump_err=float(abs(dj[-1] - jump[-1]) / jump[-1]),
                clip_share=float(np.mean(fut / sj > 15)))


# =============================================================================
# 2. ROMANIAN LOAD: DAY-AHEAD ZERO-SHOT FORECASTS
# =============================================================================
def load_baselines(win=LOAD_WIN, res_win=LOAD_RES, first=None):
    """Day-ahead forecasts for day d1 with data up to day d1 - 1: the weekly naive and the expert ARX of Ziel and
    Weron (2018) for each hour (as in Chapter 1); quantiles = point forecast plus empirical quantiles of the last
    res_win errors at the same hour. Returns days, actuals, points and decile quantiles from `first`."""
    first = first or LOAD_EVAL
    Y = ro_load_hourly()
    days, A = Y.index, Y.values
    nD = len(days)
    dow = np.array([d.dayofweek for d in days])
    start = int(np.searchsorted(days, pd.Timestamp(first)))
    P = {k: np.full((nD, 24), np.nan) for k in ('weekly naive', 'expert ARX')}
    for d1 in range(7, nD):
        P['weekly naive'][d1] = A[d1 - 7]
    mins, maxs, last = A.min(axis=1), A.max(axis=1), A[:, 23]
    for d1 in range(start - res_win - 1, nD):
        rows = np.arange(d1 - win, d1)
        for h in range(24):
            X = np.column_stack([np.ones(len(rows)), A[rows - 1, h], A[rows - 2, h], A[rows - 7, h], mins[rows - 1],
                                 maxs[rows - 1], last[rows - 1], dow[rows] == 0, dow[rows] == 5, dow[rows] == 6])
            b = np.linalg.lstsq(X, A[rows, h], rcond=None)[0]
            x = np.r_[1.0, A[d1 - 1, h], A[d1 - 2, h], A[d1 - 7, h], mins[d1 - 1], maxs[d1 - 1], last[d1 - 1],
                      dow[d1] == 0, dow[d1] == 5, dow[d1] == 6]
            P['expert ARX'][d1, h] = x @ b
    Q = {}
    for k in P:
        E = A - P[k]
        Q[k] = np.full((nD, 24, 9), np.nan)
        for d1 in range(start, nD):
            Q[k][d1] = P[k][d1][:, None] + np.nanquantile(E[d1 - res_win:d1], DECILES, axis=0).T
    return days[start:], A[start:], {k: v[start:] for k, v in P.items()}, {k: v[start:] for k, v in Q.items()}


def load_deep(first=None, L=336, refit_months=3, seed=SEED):
    """DLinear and N-BEATS (Chapter 12 architectures) trained on all hourly windows before each refit date (every
    refit_months months), inputs and targets divided by the mean of the input window; day-ahead point forecasts."""
    if not TORCH:
        return {}
    first = first or LOAD_EVAL
    Y = ro_load_hourly()
    days = Y.index
    y = Y.values.ravel()
    start = int(np.searchsorted(days, pd.Timestamp(first)))
    out = {k: np.full((len(days) - start, 24), np.nan) for k in ('DLinear', 'N-BEATS')}
    refits = pd.date_range(first, days[-1], freq=f'{refit_months}MS')
    for i, r in enumerate(refits):
        d0 = int(np.searchsorted(days, r))
        d1 = int(np.searchsorted(days, refits[i + 1])) if i + 1 < len(refits) else len(days)
        ends = np.arange(L, d0 * 24 - 24 + 1, 6)                                    # window ends (hours), stride 6
        X = np.stack([y[e - L:e] for e in ends])
        Yt = np.stack([y[e:e + 24] for e in ends])
        sc = X.mean(axis=1, keepdims=True)
        Xo = np.stack([y[d * 24 - L:d * 24] for d in range(d0, d1)])
        so = Xo.mean(axis=1, keepdims=True)
        for k, net in (('DLinear', DLinear(L, 24)), ('N-BEATS', NBeats(L, 24))):
            set_seed(seed)
            m = fit_global(net, X / sc, Yt / sc, epochs=30, seed=seed)
            out[k][d0 - start:d1 - start] = predict_global(m, Xo / so) * so
    return out


def load_fm(first=None, ctx=LOAD_CTX, names=FMS):
    """Zero-shot day-ahead decile forecasts of the foundation models: context = the last ctx hours up to the end of
    day d1 - 1."""
    first = first or LOAD_EVAL
    Y = ro_load_hourly()
    days = Y.index
    y = Y.values.ravel()
    start = int(np.searchsorted(days, pd.Timestamp(first)))
    C = [y[d * 24 - ctx:d * 24] for d in range(start, len(days))]
    out = {}
    for nm in names:
        Q = fm_cached(f'load_{first}_{ctx}', nm, C, 24, DECILES)
        if Q is not None:
            out[nm] = Q
    return out


def load_all():
    if 'load_all' in _MEM:
        return _MEM['load_all']
    days, A, P, Q = load_baselines()
    deep = load_deep()
    F = load_fm()
    for k, v in F.items():
        P[k] = v[:, :, 4]
        Q[k] = v
    P.update(deep)
    _MEM['load_all'] = (days, A, P, Q)
    return _MEM['load_all']


def fig_load(save_it=True):
    """Romanian day-ahead load, 2025-01-01 to LOAD_END: MAE and CRPS (deciles) by model, coverage of the 80% interval,
    DM tests against the expert ARX and the Model Confidence Set on daily MAE."""
    days, A, P, Q = load_all()
    names = [k for k in ['weekly naive', 'expert ARX', 'DLinear', 'N-BEATS'] + FMS if k in P]
    mae = {k: float(np.nanmean(np.abs(A - P[k]))) for k in names}
    daily = pd.DataFrame({k: np.abs(A - P[k]).mean(axis=1) for k in names}, index=days)
    crps = {k: float(np.nanmean(crps_q(A, Q[k], DECILES))) for k in names if k in Q}
    cov80 = {k: float(np.nanmean((A >= Q[k][:, :, 0]) & (A <= Q[k][:, :, 8]))) for k in names if k in Q}
    dm = {k: dm_test(daily[k] - daily['expert ARX'], 1) for k in names if k != 'expert ARX'}
    M = mcs(daily, alpha=0.10, block=7)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    order = sorted(names, key=lambda k: mae[k])
    base_col = {'weekly naive': st.Amber, 'expert ARX': st.Forest, 'DLinear': st.MainBlue, 'N-BEATS': st.Crimson}
    cols = [FM_COL.get(k, base_col.get(k, st.MainBlue)) for k in order]
    axs[0].barh(range(len(order)), [mae[k] for k in order], color=cols)
    for i, k in enumerate(order):
        axs[0].text(mae[k], i, ('  MCS' if k in M['set'] else ''), va='center', fontsize=10, color=st.DarkText)
    axs[0].set_yticks(range(len(order)))
    axs[0].set_yticklabels(order)
    axs[0].invert_yaxis()
    axs[0].set_xlabel('MAE (GW), day-ahead, 24 hours')
    wk = slice(len(days) - 7, len(days))
    t = np.arange(7 * 24)
    axs[1].plot(t, A[wk].ravel(), color=st.DarkText, lw=1.4, label='load')
    axs[1].plot(t, P['expert ARX'][wk].ravel(), color=st.Forest, lw=1.1, label='expert ARX')
    if 'Chronos-2' in Q:
        axs[1].plot(t, P['Chronos-2'][wk].ravel(), color=st.IDAred, lw=1.1, label='Chronos-2 median')
        axs[1].fill_between(t, Q['Chronos-2'][wk][:, :, 0].ravel(), Q['Chronos-2'][wk][:, :, 8].ravel(), color=st.IDAred,
                            alpha=0.18, label='Chronos-2 80%')
    axs[1].set_xticks(np.arange(0, 7 * 24 + 1, 24))
    axs[1].set_xticklabels([d.strftime('%d %b') for d in days[wk]] + [''], fontsize=9)
    axs[1].set_ylabel('GW')
    st.legend_outside_bottom(axs[1], ncol=2, y=-0.16)
    plt.tight_layout()
    save('ats_ch13_load', save_it)
    return dict(first=str(days[0].date()), last=str(days[-1].date()), n_days=int(len(days)), mae=mae, crps=crps,
                cov80=cov80, dm={k: dict(t=v['hln'], p=v['p']) for k, v in dm.items()}, mcs=M['set'], mcs_p=M['p'])


def fig_covariates(save_it=True, first=None, ctx=LOAD_CTX):
    """Chronos-2 in-context covariates: univariate, + calendar (weekend and holiday flags of the context and of the
    forecast day), + calendar and Bucharest temperature (realised values for the forecast day: an oracle upper bound).
    MAE on holidays and on other days."""
    first = first or LOAD_EVAL
    Y = ro_load_hourly()
    days = Y.index
    y = Y.values.ravel()
    T = bucharest_temperature().reindex(days).interpolate(limit_direction='both').values.ravel()
    hol = set(ro_holidays(range(days[0].year, days[-1].year + 1)))
    dflag = np.array([(d in hol) for d in days], float)
    wflag = np.array([d.dayofweek >= 5 for d in days], float)
    hflag, wh = np.repeat(dflag, 24), np.repeat(wflag, 24)
    start = int(np.searchsorted(days, pd.Timestamp(first)))
    D = range(start, len(days))
    C = [y[d * 24 - ctx:d * 24] for d in D]
    cal = [{'past': {'holiday': hflag[d * 24 - ctx:d * 24], 'weekend': wh[d * 24 - ctx:d * 24]},
            'future': {'holiday': hflag[d * 24:d * 24 + 24], 'weekend': wh[d * 24:d * 24 + 24]}} for d in D]
    tmp = [{'past': dict(c['past'], temp=T[d * 24 - ctx:d * 24]), 'future': dict(c['future'], temp=T[d * 24:d * 24 + 24])}
           for c, d in zip(cal, D)]
    A = Y.values[start:]
    res = {}
    for lab, cv in (('univariate', None), ('+ calendar', cal), ('+ calendar + temperature', tmp)):
        key = 'cov_' + lab.replace(' ', '').replace('+', 'p')
        Q = fm_cached(f'{key}_{first}_{ctx}', 'Chronos-2', C, 24, DECILES, covariates=cv)
        if Q is None:
            return {}
        res[lab] = Q
    isH = dflag[start:].astype(bool)
    mae = {k: dict(all=float(np.mean(np.abs(A - Q[:, :, 4]))), hol=float(np.mean(np.abs(A[isH] - Q[isH][:, :, 4]))),
                   other=float(np.mean(np.abs(A[~isH] - Q[~isH][:, :, 4]))),
                   crps=float(np.mean(crps_q(A, Q, DECILES)))) for k, Q in res.items()}
    daily = pd.DataFrame({k: np.abs(A - Q[:, :, 4]).mean(axis=1) for k, Q in res.items()})
    dm_cal = dm_test(daily['+ calendar'] - daily['univariate'], 1)
    dm_tmp = dm_test(daily['+ calendar + temperature'] - daily['+ calendar'], 1)
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    labs = list(res)
    x = np.arange(3)
    for j, (grp, nm) in enumerate((('all', 'all days'), ('other', 'working days and weekends'), ('hol', 'public holidays'))):
        ax.bar(x + (j - 1) * 0.26, [mae[k][grp] for k in labs], width=0.26, color=[st.MainBlue, st.Forest, st.IDAred][j], label=nm)
    ax.set_xticks(x)
    ax.set_xticklabels(['Chronos-2 ' + k for k in labs])
    ax.set_ylabel('MAE (GW)')
    st.legend_outside_bottom(ax, ncol=3, y=-0.16)
    plt.tight_layout()
    save('ats_ch13_covariates', save_it)
    return dict(mae=mae, n_hol=int(isH.sum()), dm_cal=dict(t=dm_cal['hln'], p=dm_cal['p']),
                dm_tmp=dict(t=dm_tmp['hln'], p=dm_tmp['p']))


# =============================================================================
# 3. EU INFLATION PANEL
# =============================================================================
def infl_forecasts(first=None, H=None):
    """Rolling-origin forecasts of annual HICP inflation, h = 1..H, for the 27 EU countries: random walk, AR(p) by
    AIC (p <= 12), damped ETS, a global DLinear and N-BEATS (refit each January on all countries, look-back 36 months),
    and the foundation models (context: all observations since 2000; Chronos-2 also with cross-learning across the
    27 countries of the same origin). Returns origins, actual paths (n_orig x 27 x H) and forecasts {model: (point,
    deciles)}."""
    if 'infl' in _MEM:
        return _MEM['infl']
    first, H = first or INFL['first'], H or INFL['H']
    P = eu_hicp()
    dates = P.index
    Y = P.values
    o0 = int(np.searchsorted(dates, pd.Timestamp(first)))
    origins = list(range(o0, len(dates)))                       # origin = last observed month
    nO, nC = len(origins), len(EU27)
    act = np.full((nO, nC, H), np.nan)
    for i, o in enumerate(origins):
        for h in range(1, H + 1):
            if o + h < len(dates):
                act[i, :, h - 1] = Y[o + h]
    F = {}
    pt = np.repeat(Y[origins][:, :, None], H, axis=2)
    F['random walk'] = (pt, None)
    for nm, fn in (('AR(p)', lambda y: ar_forecast(y, H, DECILES)[:2]), ('ETS', lambda y: ets_forecast(y, H, DECILES))):
        cache = os.environ.get('ATS_FM_CACHE')
        path = os.path.join(cache, f'infl_{first}_{nm[:2]}.npy') if cache else None
        if path and os.path.exists(path):
            Z = np.load(path)
        else:
            Z = np.full((nO, nC, H, 10), np.nan)
            for i, o in enumerate(origins):
                for c in range(nC):
                    m, q = fn(Y[:o + 1, c])
                    Z[i, c, :, 0], Z[i, c, :, 1:] = m, q
            if path:
                np.save(path, Z)
        F[nm] = (Z[..., 0], Z[..., 1:])
    if TORCH:
        Lb = 36
        for nm, mk in (('DLinear', lambda: DLinear(Lb, H, k=13)), ('N-BEATS', lambda: NBeats(Lb, H, width=64))):
            Z = np.full((nO, nC, H), np.nan)
            for yr in sorted(set(dates[origins].year)):
                idx = [i for i, o in enumerate(origins) if dates[o].year == yr]
                o_first = origins[idx[0]]
                X, T_ = [], []
                for c in range(nC):
                    for e in range(Lb, o_first - H + 1):
                        X.append(Y[e - Lb:e, c])
                        T_.append(Y[e:e + H, c])
                X, T_ = np.array(X), np.array(T_)
                mu, sd = X.mean(axis=1, keepdims=True), X.std(axis=1, keepdims=True) + 0.5
                net = fit_global(mk(), (X - mu) / sd, (T_ - mu) / sd, epochs=60, seed=SEED)
                for i in idx:
                    o = origins[i]
                    Xo = Y[o + 1 - Lb:o + 1].T
                    m_, s_ = Xo.mean(axis=1, keepdims=True), Xo.std(axis=1, keepdims=True) + 0.5
                    Z[i] = predict_global(net, (Xo - m_) / s_) * s_ + m_
            F[nm] = (Z, None)
    ctxs = [Y[:o + 1, c] for o in origins for c in range(nC)]
    for nm in FMS:
        Q = fm_cached(f'infl_{first}_{H}', nm, ctxs, H, DECILES)
        if Q is not None:
            Q = Q.reshape(nO, nC, H, 9)
            F[nm] = (Q[..., 4], Q)
    if fm_load('Chronos-2') is not None:
        Q = fm_cached(f'infl_{first}_{H}_cross', 'Chronos-2', ctxs, H, DECILES, batch=nC, cross_learning=True)
        Q = Q.reshape(nO, nC, H, 9)
        F['Chronos-2 cross-learning'] = (Q[..., 4], Q)
    _MEM['infl'] = (dates, origins, act, F)
    return _MEM['infl']


def fig_inflation(save_it=True):
    """MAE relative to the random walk by horizon (geometric mean over countries of the country-level ratios), with
    95% bootstrap intervals over countries at h = 12; CRPS of the probabilistic models relative to AR(p)."""
    dates, origins, act, F = infl_forecasts()
    H = act.shape[2]
    rw = F['random walk'][0]
    names = [k for k in ['AR(p)', 'ETS', 'DLinear', 'N-BEATS'] + FMS + ['Chronos-2 cross-learning'] if k in F]
    rel = {}
    for k in names:
        e, e0 = np.abs(act - F[k][0]), np.abs(act - rw)
        r = np.nanmean(e, axis=0) / np.nanmean(e0, axis=0)                     # countries x H
        rel[k] = [gmean(r[:, h]) for h in range(H)]
    rng = np.random.default_rng(SEED)
    ci = {}
    for k in names:
        e, e0 = np.abs(act[:, :, -1] - F[k][0][:, :, -1]), np.abs(act[:, :, -1] - rw[:, :, -1])
        r = np.nanmean(e, axis=0) / np.nanmean(e0, axis=0)
        b = [gmean(r[rng.integers(0, len(r), len(r))]) for _ in range(2000)]
        ci[k] = (float(np.quantile(b, 0.025)), float(np.quantile(b, 0.975)))
    crps_rel = {}
    for k in names:
        if F[k][1] is None:
            continue
        c = np.nanmean(crps_q(act, F[k][1], DECILES), axis=(0, 2)) / np.nanmean(crps_q(act, F['AR(p)'][1], DECILES), axis=(0, 2))
        crps_rel[k] = gmean(c)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    hh = np.arange(1, H + 1)
    for k in names:
        c = FM_COL.get(k, {'AR(p)': st.Forest, 'ETS': st.Amber, 'DLinear': st.MainBlue, 'N-BEATS': st.Crimson,
                           'Chronos-2 cross-learning': st.DarkText}.get(k, st.MainBlue))
        ls = '--' if k == 'Chronos-2 cross-learning' else '-'
        axs[0].plot(hh, rel[k], color=c, lw=1.5, ls=ls, marker='o', ms=3, label=k)
    axs[0].axhline(1, color=st.DarkText, ls=':', lw=1)
    axs[0].set_xlabel('horizon (months)')
    axs[0].set_ylabel('MAE relative to the random walk')
    order = sorted(names, key=lambda k: rel[k][-1])
    for i, k in enumerate(order):
        c = FM_COL.get(k, {'AR(p)': st.Forest, 'ETS': st.Amber, 'DLinear': st.MainBlue, 'N-BEATS': st.Crimson,
                           'Chronos-2 cross-learning': st.DarkText}.get(k, st.MainBlue))
        axs[1].plot(ci[k], [i, i], color=c, lw=2.2)
        axs[1].plot(rel[k][-1], i, 'o', color=c)
    axs[1].set_yticks(range(len(order)))
    axs[1].set_yticklabels(order)
    axs[1].invert_yaxis()
    axs[1].axvline(1, color=st.DarkText, ls=':', lw=1)
    axs[1].set_xlabel('h = 12: relative MAE, 95% bootstrap over countries')
    st.fig_legend_bottom(fig, ncol=5, y=0.0)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch13_inflation', save_it)
    return dict(rel={k: dict(h1=v[0], h6=v[5], h12=v[-1]) for k, v in rel.items()}, ci=ci, crps_rel=crps_rel,
                first=str(dates[origins[0]].date()), last=str(dates[origins[-1] - H].date()), n_orig=len(origins),
                end=str(dates[-1].date()))


def fig_ro_inflation(save_it=True):
    """Romanian HICP inflation: Chronos-2 and AR(p) 12-month forecasts with 80% bands from three origins (before the
    2022 surge, at its peak, and the latest origin with a full year of outcomes)."""
    dates, origins, act, F = infl_forecasts()
    P = eu_hicp()['RO']
    c = EU27.index('RO')
    oo = [pd.Timestamp('2021-06-01'), pd.Timestamp('2022-11-01'), dates[origins[-1]] - pd.DateOffset(months=12)]
    fig, ax = plt.subplots(figsize=(11, 4.0))
    ax.plot(P.loc['2019':].index, P.loc['2019':].values, color=st.DarkText, lw=1.6, label='Romania, HICP annual inflation')
    out, used = {}, []
    for j, o in enumerate(oo):
        i = int(np.clip(np.searchsorted(dates[origins], o), 0, len(origins) - 1))
        od = dates[origins[i]]
        used.append(str(od.date()))
        fx = pd.date_range(od + pd.DateOffset(months=1), periods=12, freq='MS')
        for k, col in (('Chronos-2', st.IDAred), ('AR(p)', st.Forest)):
            if k not in F:
                continue
            q = F[k][1][i, c]
            ax.plot(fx, q[:, 4], color=col, lw=1.4, label=f'{k} median, 80%' if j == 0 else None)
            ax.fill_between(fx, q[:, 0], q[:, 8], color=col, alpha=0.15)
            out[f'{k}|{j}'] = dict(med12=float(q[-1, 4]), lo12=float(q[-1, 0]), hi12=float(q[-1, 8]),
                                   act12=float(act[i, c, -1]))
    ax.set_ylabel('% year on year')
    st.legend_outside_bottom(ax, ncol=3, y=-0.12)
    plt.tight_layout()
    save('ats_ch13_ro_inflation', save_it)
    return dict(origins=used, fc=out, peak=float(P.loc['2021':'2024'].max()),
                peak_date=str(P.loc['2021':'2024'].idxmax().date()), last=float(P.iloc[-1]), last_date=str(P.index[-1].date()))


def fig_multiple(save_it=True, model='Chronos-2', h=12):
    """Country-level DM tests (HLN, HAC with h - 1 lags) of the h-step absolute errors of a foundation model against
    AR(p): the distribution of the 27 p-values and the number of rejections at 5% without correction, with Holm and
    with Benjamini-Hochberg."""
    dates, origins, act, F = infl_forecasts()
    p, t = [], []
    for c in range(len(EU27)):
        d = np.abs(act[:, c, h - 1] - F[model][0][:, c, h - 1]) - np.abs(act[:, c, h - 1] - F['AR(p)'][0][:, c, h - 1])
        r = dm_test(d[~np.isnan(d)], h)
        p.append(r['p'])
        t.append(r['hln'])
    p, t = np.array(p), np.array(t)
    ph, pb = holm(p), bh(p)
    fig, ax = plt.subplots(figsize=(11, 3.8))
    o = np.argsort(t)
    cols = [st.MainBlue if t[i] < 0 else st.IDAred for i in o]
    ax.bar(range(len(o)), t[o], color=cols)
    ax.set_xticks(range(len(o)))
    ax.set_xticklabels([EU27[i] for i in o], fontsize=9)
    crit = 1.96
    ax.axhline(-crit, color=st.Forest, ls='--', lw=1, label='|t| = 1.96 (5%, no correction)')
    ax.axhline(crit, color=st.Forest, ls='--', lw=1)
    from scipy import stats as _s
    hc = _s.norm.ppf(1 - 0.025 / len(EU27))
    ax.axhline(-hc, color=st.Purple, ls=':', lw=1.2, label=f'|t| = {hc:.2f} (Bonferroni, 27 tests)')
    ax.axhline(hc, color=st.Purple, ls=':', lw=1.2)
    ax.set_ylabel(f'DM-HLN statistic, {model} minus AR(p)')
    st.legend_outside_bottom(ax, ncol=2, y=-0.14)
    plt.tight_layout()
    save('ats_ch13_multiple', save_it)
    return dict(model=model, h=h, n=len(p), rej=int((p < 0.05).sum()), rej_fm=int(((p < 0.05) & (t < 0)).sum()),
                rej_ar=int(((p < 0.05) & (t > 0)).sum()), rej_holm=int((ph < 0.05).sum()), rej_bh=int((pb < 0.05).sum()),
                neg=int((t < 0).sum()), ro_t=float(t[EU27.index('RO')]), ro_p=float(p[EU27.index('RO')]), hc=float(hc))


# =============================================================================
# 4. REALISED VARIANCE: HAR AGAINST FOUNDATION MODELS
# =============================================================================
def rv_forecasts(series='btc', first=None, ctx=1024, win=1000):
    """One-day-ahead forecasts of log realised variance: HAR on a rolling window of `win` days and the foundation
    models (context: the last ctx days of log RV). Variance forecasts: exp(median + s^2/2), s from the 10-90% spread
    (HAR: the residual s.d.). Returns dates, rv, {model: (log median, variance forecast, deciles of log RV)}."""
    key = f'rv_{series}'
    if key in _MEM:
        return _MEM[key]
    rv = btc_rv() if series == 'btc' else spx_rv()
    first = first or RV_FIRST[series]
    x = np.log(rv.values)
    dates = rv.index
    o0 = int(np.searchsorted(dates, pd.Timestamp(first)))
    idx = np.arange(o0, len(x))
    out = {}
    med, var = np.empty(len(idx)), np.empty(len(idx))
    for j, t in enumerate(idx):
        f, s = har_forecast(x[t - win:t], 1)
        med[j], var[j] = f, np.exp(f + s ** 2 / 2)
    out['HAR'] = (med, var, None)
    C = [x[t - ctx:t] for t in idx]
    for nm in FMS:
        Q = fm_cached(f'{key}_{first}_{ctx}', nm, C, 1, DECILES)
        if Q is None:
            continue
        q = Q[:, 0, :]
        s = (q[:, 8] - q[:, 0]) / (2 * 1.2816)
        out[nm] = (q[:, 4], np.exp(q[:, 4] + s ** 2 / 2), q)
    _MEM[key] = (dates[idx], rv.values[idx], x[idx], out)
    return _MEM[key]


def fig_rv(save_it=True):
    """Bitcoin (Binance, 2021-2026) and S&P 500 (Oxford-Man, 2010-2022): MSE of log RV and QLIKE relative to HAR,
    MCS on QLIKE; for Bitcoin, the ratio before the first release and after the last release of the models."""
    res = {}
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    for ax, ser, lab in ((axs[0], 'btc', 'Bitcoin'), (axs[1], 'spx', 'S&P 500')):
        dates, rv, x, F = rv_forecasts(ser)
        names = list(F)
        mse = {k: float(np.mean((x - F[k][0]) ** 2)) for k in names}
        ql = {k: float(np.mean(qlike(rv, F[k][1]))) for k in names}
        L = pd.DataFrame({k: qlike(rv, F[k][1]) for k in names}, index=dates)
        M = mcs(L, alpha=0.10, block=10)
        dm = {k: dm_test(L[k] - L['HAR'], 1) for k in names if k != 'HAR'}
        win = {}
        if ser == 'btc':
            for w, (a, b) in (('pre', (dates[0], PRE_END)), ('post', (POST_START, dates[-1]))):
                m = (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b))
                win[w] = {k: float(np.mean(qlike(rv[m], F[k][1][m])) / np.mean(qlike(rv[m], F['HAR'][1][m]))) for k in names}
                win[w + '_n'] = int(m.sum())
        res[ser] = dict(mse=mse, qlike=ql, mcs=M['set'], dm={k: dict(t=v['hln'], p=v['p']) for k, v in dm.items()},
                        first=str(dates[0].date()), last=str(dates[-1].date()), n=int(len(dates)), win=win)
        ks = [k for k in names if k != 'HAR']
        r1 = [mse[k] / mse['HAR'] for k in ks]
        r2 = [ql[k] / ql['HAR'] for k in ks]
        y = np.arange(len(ks))
        ax.barh(y - 0.2, r1, height=0.38, color=st.MainBlue, label='MSE of log RV / HAR')
        ax.barh(y + 0.2, r2, height=0.38, color=st.IDAred, label='QLIKE / HAR')
        ax.set_yticks(y)
        ax.set_yticklabels(ks)
        ax.axvline(1, color=st.DarkText, ls=':', lw=1)
        ax.set_title(f'{lab}, {dates[0].year}-{dates[-1].year}, one day ahead')
    st.fig_legend_bottom(fig, ncol=2, y=0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch13_rv', save_it)
    return res


def fig_contamination(save_it=True):
    """Relative accuracy of each foundation model in an earlier window and after the last release (from 1 November
    2025): Romanian load (MAE / expert ARX; earlier window January-October 2025, before the release of Chronos-2 and
    TimesFM 2.5) and Bitcoin RV (QLIKE / HAR; earlier window 2021 to 24 November 2024, before every release)."""
    days, A, P, Q = load_all()
    m1 = (days >= pd.Timestamp('2025-01-01')) & (days <= pd.Timestamp('2025-10-31'))
    m2 = days >= pd.Timestamp(POST_START)
    ld = {}
    for k in FMS:
        if k in P:
            ld[k] = [float(np.mean(np.abs(A[m] - P[k][m])) / np.mean(np.abs(A[m] - P['expert ARX'][m]))) for m in (m1, m2)]
    dates, rv, x, F = rv_forecasts('btc')
    b1 = dates <= pd.Timestamp(PRE_END)
    b2 = dates >= pd.Timestamp(POST_START)
    bt = {}
    for k in FMS:
        if k in F:
            bt[k] = [float(np.mean(qlike(rv[m], F[k][1][m])) / np.mean(qlike(rv[m], F['HAR'][1][m]))) for m in (b1, b2)]
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 3.9))
    for ax, R, ttl, labs in ((axs[0], ld, 'Romanian load: MAE / expert ARX', ('Jan-Oct 2025', 'Nov 2025-Sep 2026')),
                              (axs[1], bt, 'Bitcoin RV: QLIKE / HAR', ('2021 to 24 Nov 2024', 'Nov 2025-Sep 2026'))):
        ks = list(R)
        y = np.arange(len(ks))
        ax.barh(y - 0.2, [R[k][0] for k in ks], height=0.38, color=st.Amber, label='earlier window: ' + labs[0])
        ax.barh(y + 0.2, [R[k][1] for k in ks], height=0.38, color=st.MainBlue, label='after all releases: ' + labs[1])
        ax.set_yticks(y)
        ax.set_yticklabels(ks)
        ax.axvline(1, color=st.DarkText, ls=':', lw=1)
        ax.set_title(ttl)
        st.legend_outside_bottom(ax, ncol=1, y=-0.14)
    plt.tight_layout()
    save('ats_ch13_contamination', save_it)
    return dict(load=ld, btc=bt, n_load=[int(m1.sum()), int(m2.sum())], n_btc=[int(b1.sum()), int(b2.sum())])


def fig_scaling(save_it=True):
    """Accuracy against the number of parameters: the Chronos-Bolt family (tiny, mini, small, base), Chronos-2,
    TimesFM 2.5 and TiRex on three tasks: Romanian load (MAE / expert ARX, 2025-2026), EU inflation (MAE / random walk,
    h = 12) and Bitcoin RV (MSE of log RV / HAR)."""
    names = ['Chronos-Bolt tiny', 'Chronos-Bolt mini', 'Chronos-Bolt small', 'Chronos-Bolt base', 'Chronos-2',
             'TimesFM 2.5', 'TiRex']
    names = [k for k in names if fm_load(k) is not None]
    par = {k: fm_params(k) for k in names}
    days, A, P, Q = load_all()
    extra = load_fm(names=[k for k in names if k not in P])
    PP = dict(P, **{k: v[:, :, 4] for k, v in extra.items()})
    base = np.mean(np.abs(A - P['expert ARX']))
    r_load = {k: float(np.mean(np.abs(A - PP[k])) / base) for k in names}
    dates, origins, act, F = infl_forecasts()
    Y = eu_hicp().values
    ctxs = [Y[:o + 1, c] for o in origins for c in range(len(EU27))]
    rw = np.abs(act[:, :, -1] - F['random walk'][0][:, :, -1])
    r_inf = {}
    for k in names:
        f = F[k][0] if k in F else fm_cached(f'infl_{INFL["first"]}_{INFL["H"]}', k, ctxs, act.shape[2], DECILES).reshape(
            len(origins), len(EU27), act.shape[2], 9)[..., 4]
        r = np.nanmean(np.abs(act[:, :, -1] - f[:, :, -1]), axis=0) / np.nanmean(rw, axis=0)
        r_inf[k] = gmean(r)
    d2, rv, x, FR = rv_forecasts('btc')
    rv_all = rv_forecasts_extra('btc', [k for k in names if k not in FR])
    har = np.mean((x - FR['HAR'][0]) ** 2)
    r_rv = {k: float(np.mean((x - (FR[k][0] if k in FR else rv_all[k])) ** 2) / har) for k in names}
    fig, ax = plt.subplots(figsize=(10, 4.0))
    for R, mk, lab, col in ((r_load, 'o', 'Romanian load', st.MainBlue), (r_inf, 's', 'EU inflation, h = 12', st.Forest),
                            (r_rv, '^', 'Bitcoin log RV', st.IDAred)):
        bolt = [k for k in names if k.startswith('Chronos-Bolt')]
        ax.plot([par[k] for k in bolt], [R[k] for k in bolt], color=col, lw=1.2, marker=mk, label=lab + ' (Chronos-Bolt family)')
        oth = [k for k in names if not k.startswith('Chronos-Bolt')]
        ax.scatter([par[k] for k in oth], [R[k] for k in oth], color=col, marker=mk, s=60, facecolors='none', linewidths=1.5)
        for k in oth:
            ax.annotate(k, (par[k], R[k]), textcoords='offset points', xytext=(4, 3), fontsize=8.5, color=col)
    ax.set_xscale('log')
    ax.axhline(1, color=st.DarkText, ls=':', lw=1)
    ax.set_xlabel('parameters (millions, log scale)')
    ax.set_ylabel('loss relative to the baseline')
    st.legend_outside_bottom(ax, ncol=3, y=-0.16)
    plt.tight_layout()
    save('ats_ch13_scaling', save_it)
    return dict(params=par, load=r_load, infl=r_inf, rv=r_rv)


def rv_forecasts_extra(series, names, ctx=1024):
    """Log-RV medians of additional models (the scaling chart), same design as rv_forecasts."""
    dates, rv, x, F = rv_forecasts(series)
    full = np.log(btc_rv().values if series == 'btc' else spx_rv().values)
    first = RV_FIRST[series]
    alld = (btc_rv() if series == 'btc' else spx_rv()).index
    o0 = int(np.searchsorted(alld, pd.Timestamp(first)))
    C = [full[t - ctx:t] for t in range(o0, len(full))]
    out = {}
    for nm in names:
        Q = fm_cached(f'rv_{series}_{first}_{ctx}', nm, C, 1, DECILES)
        if Q is not None:
            out[nm] = Q[:, 0, 4]
    return out


def fig_zeroshot(save_it=True):
    """Four zero-shot Chronos-2 forecasts from the last origin of each data set: Romanian load (48 hours), Romanian
    inflation (12 months), Bitcoin log RV (22 days), daily BET returns (22 days; 1-99% band)."""
    if fm_load('Chronos-2') is None:
        return {}
    fig, axs = plt.subplots(2, 2, figsize=(11.5, 6.2))
    y = ro_load_hourly().values.ravel()
    sets = [(axs[0, 0], 'Romanian load (GW), hourly', y[-24 * 7:], y[-2048:], 48),
            (axs[0, 1], 'Romanian HICP inflation (%), monthly', eu_hicp()['RO'].values[-48:], eu_hicp()['RO'].values, 12),
            (axs[1, 0], 'Bitcoin log realised variance, daily', np.log(btc_rv().values[-120:]), np.log(btc_rv().values[-1024:]), 22),
            (axs[1, 1], 'BET daily log return (%)', log_returns('bet').values[-120:], log_returns('bet').values[-1024:], 22)]
    out = {}
    for ax, ttl, show, ctx, H in sets:
        Q = fm_forecast('Chronos-2', [ctx], H, [0.01, 0.1, 0.5, 0.9, 0.99])[0]
        n = len(show)
        ax.plot(np.arange(n), show, color=st.DarkText, lw=1.2, label='observed (context)')
        t = np.arange(n, n + H)
        ax.fill_between(t, Q[:, 0], Q[:, 4], color=st.IDAred, alpha=0.12, label='1-99%')
        ax.fill_between(t, Q[:, 1], Q[:, 3], color=st.IDAred, alpha=0.25, label='10-90%')
        ax.plot(t, Q[:, 2], color=st.IDAred, lw=1.4, label='median')
        ax.set_title(ttl, fontsize=11.5)
        out[ttl] = dict(q01=float(Q[0, 0]), q50=float(Q[0, 2]), q99=float(Q[0, 4]))
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.05, 1, 1))
    save('ats_ch13_zeroshot', save_it)
    return out


# =============================================================================
# 5. CONFORMAL PREDICTION: EXCHANGEABLE DATA
# =============================================================================
def fig_split_coverage(save_it=True, reps=4000, alpha=0.1, seed=SEED):
    """Coverage of split conformal conditional on the calibration set: with n calibration scores the coverage of the
    next point is F(q_hat), distributed Beta(k, n + 1 - k), k = ceil((n + 1)(1 - alpha)) (continuous scores).
    Simulation: |N(0, 1)| scores; n = 50 and 500."""
    from scipy import stats as _s
    rng = np.random.default_rng(seed)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    out = {}
    for n, col in ((50, st.IDAred), (500, st.MainBlue)):
        cov = []
        for _ in range(reps):
            sc = np.abs(rng.standard_normal(n))
            q = conformal_quantile(sc, alpha)
            cov.append(2 * _s.norm.cdf(q) - 1)
        cov = np.array(cov)
        k = int(np.ceil((n + 1) * (1 - alpha)))
        ax.hist(cov, bins=60, density=True, color=col, alpha=0.35, label=f'simulated, n = {n}')
        g = np.linspace(0.7, 1, 400)
        ax.plot(g, _s.beta.pdf(g, k, n + 1 - k), color=col, lw=1.6, label=f'Beta({k}, {n + 1 - k})')
        out[n] = dict(mean=float(cov.mean()), sd=float(cov.std()), theory_mean=k / (n + 1),
                      theory_sd=float(_s.beta.std(k, n + 1 - k)), p_below=float((cov < 1 - alpha).mean()),
                      p_below88=float((cov < 0.88).mean()), q05=float(np.quantile(cov, 0.05)), k=k)
    ax.axvline(1 - alpha, color=st.Forest, ls='--', lw=1.2, label='target 0.90')
    ax.set_xlabel('coverage of the next point, given the calibration set')
    st.legend_outside_bottom(ax, ncol=5, y=-0.16)
    plt.tight_layout()
    save('ats_ch13_split_coverage', save_it)
    return dict(n50=out[50], n500=out[500], reps=reps)


def cqr_data(n, rng):
    """The synthetic design of Romano, Patterson and Candes (2019, Figure 1):
    Y = Pois(sin^2(X) + 0.1) + 0.03 X e1 + 25 1{U < 0.01} e2, X ~ U[0, 5], e1, e2 ~ N(0, 1)."""
    X = rng.uniform(0, 5, n)
    Y = (rng.poisson(np.sin(X) ** 2 + 0.1) + 0.03 * X * rng.standard_normal(n)
         + 25 * (rng.uniform(size=n) < 0.01) * rng.standard_normal(n))
    return X, Y


def fig_cqr(save_it=True, n=2000, n_test=5000, alpha=0.1, seed=SEED):
    """Split conformal with a conditional-mean model against CQR with quantile models (gradient boosting with the
    pinball loss), 1000 training and 1000 calibration points; coverage and width overall and by X."""
    from sklearn.ensemble import GradientBoostingRegressor as GBR
    rng = np.random.default_rng(seed)
    X, Y = cqr_data(n, rng)
    Xt, Yt = cqr_data(n_test, rng)
    tr, ca = slice(0, n // 2), slice(n // 2, n)
    kw = dict(n_estimators=150, max_depth=2, learning_rate=0.05, min_samples_leaf=50, random_state=seed)
    mean = GBR(loss='squared_error', **kw).fit(X[tr, None], Y[tr])
    lo = GBR(loss='quantile', alpha=alpha / 2, **kw).fit(X[tr, None], Y[tr])
    hi = GBR(loss='quantile', alpha=1 - alpha / 2, **kw).fit(X[tr, None], Y[tr])
    g = np.linspace(0, 5, 400)
    s_lo, s_hi = split_conformal(Y[ca], mean.predict(X[ca, None]), mean.predict(Xt[:, None]), alpha)
    c_lo, c_hi = cqr(Y[ca], lo.predict(X[ca, None]), hi.predict(X[ca, None]), lo.predict(Xt[:, None]), hi.predict(Xt[:, None]), alpha)
    r_lo, r_hi = lo.predict(Xt[:, None]), hi.predict(Xt[:, None])
    gs = split_conformal(Y[ca], mean.predict(X[ca, None]), mean.predict(g[:, None]), alpha)
    gc = cqr(Y[ca], lo.predict(X[ca, None]), hi.predict(X[ca, None]), lo.predict(g[:, None]), hi.predict(g[:, None]), alpha)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    for ax, (a, b), ttl, col in ((axs[0], gs, 'split conformal (mean model)', st.MainBlue), (axs[1], gc, 'CQR (quantile models)', st.IDAred)):
        ax.scatter(Xt[:1500], Yt[:1500], s=4, color=st.Amber, alpha=0.5, label='test points')
        ax.fill_between(g, a, b, color=col, alpha=0.25, label='90% interval')
        ax.set_ylim(-3, 8)
        ax.set_title(ttl)
        ax.set_xlabel('X')
    st.fig_legend_bottom(fig, ncol=2, y=0.0)
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    save('ats_ch13_cqr', save_it)
    bins = np.digitize(Xt, [1, 2, 3, 4])
    cs = lambda a, b: [float(np.mean((Yt[bins == j] >= a[bins == j]) & (Yt[bins == j] <= b[bins == j]))) for j in range(5)]  # noqa: E731
    return dict(split=dict(cov=float(np.mean((Yt >= s_lo) & (Yt <= s_hi))), width=float(np.mean(s_hi - s_lo)), bins=cs(s_lo, s_hi)),
                cqr=dict(cov=float(np.mean((Yt >= c_lo) & (Yt <= c_hi))), width=float(np.mean(c_hi - c_lo)), bins=cs(c_lo, c_hi)),
                raw=dict(cov=float(np.mean((Yt >= r_lo) & (Yt <= r_hi))), width=float(np.mean(r_hi - r_lo))))


# =============================================================================
# 6. CONFORMAL FOR DEPENDENT DATA: VOLATILITY, ACI, PID, EnbPI, WEIGHTS
# =============================================================================
def garch_scores(name, start=None, fit_win=1250, refit=20):
    """The design of Gibbs and Candes (2021) for stock volatility: V_t = r_t^2, sigma_t^2 from a GARCH(1,1) fitted on
    the previous fit_win days (re-estimated every `refit` days, filtered daily), score S_t = |V_t - sigma_t^2| /
    sigma_t^2. Returns dates, scores, sigma2, returns (from `start`)."""
    key = f'gs_{name}'
    if key in _MEM:
        return _MEM[key]
    start = start or GS_START
    r = log_returns(name)
    i0 = max(int(np.searchsorted(r.index, pd.Timestamp(start))), fit_win)
    rr = r.values
    sig2 = np.full(len(rr), np.nan)
    par = None
    for t in range(i0, len(rr)):
        if par is None or (t - i0) % refit == 0:
            par = garch11_fit(rr[t - fit_win:t], dist='normal')
        sig2[t] = garch11_filter(rr[t - fit_win:t], par)[-1]
    sl = slice(i0, len(rr))
    S = np.abs(rr[sl] ** 2 - sig2[sl]) / sig2[sl]
    _MEM[key] = (r.index[sl], S, sig2[sl], rr[sl])
    return _MEM[key]


def local_cov(miss, w=500):
    """Rolling coverage over the last w points (the local coverage frequency of Gibbs and Candes 2021)."""
    return 1 - pd.Series(miss).rolling(w).mean().values


def fig_aci(save_it=True, alpha=0.1, gamma=0.005, n_cal=1250):
    """S&P 500, BET and NVIDIA: local coverage (two-year window) of 90% volatility intervals: static split conformal
    (calibrated once on the first 1250 scores), rolling split conformal with a fixed level and ACI (gamma = 0.005)."""
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    out = {}
    for ax, nm, lab in zip(axs, ('sp500', 'bet', 'nvda'), ('S&P 500', 'BET', 'NVIDIA')):
        dates, S, s2, r = garch_scores(nm)
        res = {}
        for meth, col, lb in (('static', st.Amber, 'static split'), ('rolling', st.MainBlue, 'rolling, fixed level'),
                              ('aci', st.IDAred, 'ACI')):
            q, at = online_threshold(S, alpha, method=meth, n_cal=n_cal, window=n_cal, gamma=gamma)
            miss = (S > q)[n_cal:].astype(float)
            lc = local_cov(miss)
            ax.plot(dates[n_cal:], lc, color=col, lw=1.2, label=lb)
            hits = miss
            res[meth] = dict(cov=float(1 - miss.mean()), lc_min=float(np.nanmin(lc)), lc_max=float(np.nanmax(lc)),
                             kup=kupiec(hits, alpha)[1], cc=christoffersen(hits, alpha)['p_cc'],
                             inf=float(np.mean(np.isinf(q[n_cal:]))))
        ax.axhline(1 - alpha, color=st.Forest, ls='--', lw=1)
        ax.set_title(lab)
        out[nm] = dict(res, n=int(len(S) - n_cal), first=str(dates[n_cal].date()), last=str(dates[-1].date()))
    axs[0].set_ylabel('local coverage (500 days)')
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch13_aci', save_it)
    return out


def fig_aci_gamma(save_it=True, alpha=0.1, n_cal=1250):
    """ACI on the S&P 500 scores: the level alpha_t for gamma = 0.001, 0.005, 0.05; long-run miss rate, its bound
    (max(alpha_1, 1 - alpha_1) + gamma) / (gamma T), interval instability (s.d. of the threshold changes) and the
    share of infinite intervals."""
    dates, S, s2, r = garch_scores('sp500')
    fig, ax = plt.subplots(figsize=(11, 3.8))
    out = {}
    for g, col in ((0.001, st.MainBlue), (0.005, st.IDAred), (0.05, st.Forest)):
        q, at = online_threshold(S, alpha, method='aci', n_cal=n_cal, window=n_cal, gamma=g)
        miss = (S > q)[n_cal:]
        T = len(miss)
        ax.plot(dates[n_cal:], at[n_cal:], color=col, lw=1.0, label=f'gamma = {g}')
        qq = q[n_cal:][np.isfinite(q[n_cal:])]
        out[str(g)] = dict(miss=float(miss.mean()), bound=float((max(alpha, 1 - alpha) + g) / (g * T)),
                           inf=float(np.mean(np.isinf(q[n_cal:]))), amin=float(np.nanmin(at[n_cal:])),
                           amax=float(np.nanmax(at[n_cal:])), jitter=float(np.std(np.diff(qq))), T=T)
    ax.axhline(alpha, color=st.DarkText, ls=':', lw=1)
    ax.set_ylabel('ACI level alpha_t')
    st.legend_outside_bottom(ax, ncol=3, y=-0.14)
    plt.tight_layout()
    save('ats_ch13_aci_gamma', save_it)
    return out


def fig_condcov(save_it=True, alpha=0.1, n_cal=1250):
    """Conditional coverage on the S&P 500: coverage of the static, rolling and ACI intervals by tercile of the GARCH
    variance forecast and in the days after a miss (the dependence the Christoffersen test detects)."""
    dates, S, s2, r = garch_scores('sp500')
    terc = pd.qcut(s2[n_cal:], 3, labels=False)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    out = {}
    labs = ['low variance', 'middle', 'high variance', 'day after a miss']
    for j, (meth, col, lb) in enumerate((('static', st.Amber, 'static split'), ('rolling', st.MainBlue, 'rolling'),
                                         ('aci', st.IDAred, 'ACI'))):
        q, _ = online_threshold(S, alpha, method=meth, n_cal=n_cal, window=n_cal, gamma=0.005)
        cov = (S <= q)[n_cal:]
        v = [float(cov[terc == k].mean()) for k in range(3)] + [float(cov[1:][~cov[:-1]].mean())]
        ax.bar(np.arange(4) + (j - 1) * 0.26, v, width=0.26, color=col, label=lb)
        out[meth] = v
    ax.axhline(1 - alpha, color=st.Forest, ls='--', lw=1.2, label='target 0.90')
    ax.set_xticks(range(4))
    ax.set_xticklabels(labs)
    ax.set_ylim(0.85, 0.94)
    ax.set_ylabel('coverage')
    st.legend_outside_bottom(ax, ncol=4, y=-0.14)
    plt.tight_layout()
    save('ats_ch13_condcov', save_it)
    return out


def fig_weighted(save_it=True, n=2000, burn=200, rho=0.99, alpha=0.1, reps=200, seed=SEED):
    """Weighted (non-exchangeable) conformal prediction against standard conformal under changepoints, in the style
    of the simulations of Barber et al. (2023): Y = X'beta_t + N(0, 1), X ~ N(0, I_4), beta changes at t = 500 and
    1500; least squares refitted on all past data; prequential absolute residuals as scores; weights rho^(t - i).
    Coverage of each time point averaged over `reps` replications."""
    rng = np.random.default_rng(seed)
    b1, b2, b3 = np.array([2, 1, 0, 0.]), np.array([0, -2, -1, 0.]), np.array([0, 0, 2, 1.])
    covs = {'standard': np.zeros(n), 'weighted': np.zeros(n)}
    width = {'standard': np.zeros(n), 'weighted': np.zeros(n)}
    for _ in range(reps):
        X = rng.standard_normal((n, 4))
        B = np.where(np.arange(n)[:, None] < 500, b1, np.where(np.arange(n)[:, None] < 1500, b2, b3))
        Y = (X * B).sum(1) + rng.standard_normal(n)
        S = np.full(n, np.nan)
        XtX, Xty = np.eye(4) * 1e-6, np.zeros(4)
        for t in range(n):
            if t >= 10:
                S[t] = abs(Y[t] - X[t] @ np.linalg.solve(XtX, Xty))
            XtX += np.outer(X[t], X[t])
            Xty += X[t] * Y[t]
        for meth in covs:
            q, _ = online_threshold(S[10:], alpha, method='rolling' if meth == 'standard' else 'weighted', rho=rho,
                                    start=burn - 10)
            q = np.r_[np.full(10, np.nan), q]
            covs[meth] += (S <= q) / reps
            width[meth] += np.where(np.isfinite(q), 2 * q, np.nan) / reps
    fig, ax = plt.subplots(figsize=(11, 3.8))
    t = np.arange(n)
    for meth, col in (('standard', st.MainBlue), ('weighted', st.IDAred)):
        ax.plot(t[burn:], pd.Series(covs[meth][burn:]).rolling(20).mean(), color=col, lw=1.3,
                label=f'{meth} conformal' + (f' (rho = {rho})' if meth == 'weighted' else ''))
    ax.axhline(1 - alpha, color=st.Forest, ls='--', lw=1)
    for c in (500, 1500):
        ax.axvline(c, color=st.Amber, ls=':', lw=1.2)
    ax.set_xlabel('time')
    ax.set_ylabel(f'coverage (mean of {reps} runs)')
    st.legend_outside_bottom(ax, ncol=2, y=-0.16)
    plt.tight_layout()
    save('ats_ch13_weighted', save_it)
    after = slice(1500, 1600)
    return {m: dict(cov=float(np.mean(covs[m][burn:])), after=float(np.mean(covs[m][after])),
                    w=float(np.nanmean(width[m][burn:])), min=float(pd.Series(covs[m][burn:]).rolling(20).mean().min()))
            for m in covs}


def load_scores(base='expert ARX'):
    """Hour-by-hour streams of absolute day-ahead errors of a base forecaster (days x 24) on Romanian load."""
    days, A, P, Q = load_all()
    return days, A, P[base], np.abs(A - P[base])


def fig_pid(save_it=True, alpha=0.1, n_cal=91, base='Chronos-Bolt small'):
    """90% day-ahead intervals for Romanian load around a base point forecast, one online threshold per hour of the
    day: static split (first n_cal days), rolling split (last n_cal days), ACI, quantile tracking, conformal PID
    (quantile tracking + integrator + AR(1) scorecaster) and EnbPI on the expert ARX regressors."""
    days, A, P, S = load_scores(base)
    nD = len(days)
    meths = [('static', 'static split'), ('rolling', 'rolling split'), ('aci', 'ACI'), ('qt', 'quantile tracking'),
             ('pid', 'conformal PID')]
    miss = {m: np.full((nD, 24), np.nan) for m, _ in meths}
    wid = {m: np.full((nD, 24), np.nan) for m, _ in meths}
    for h in range(24):
        s = S[:, h]
        for m, _ in meths:
            q, _ = online_threshold(s, alpha, method=m, n_cal=n_cal, window=n_cal, gamma=0.005,
                                    scorecaster=ar_scorecaster(1, 365) if m == 'pid' else None)
            miss[m][n_cal:, h] = (s > q)[n_cal:]
            wid[m][n_cal:, h] = 2 * q[n_cal:]
    # EnbPI on the expert ARX regressors, one stream per hour
    Y = ro_load_hourly()
    dd, AA = Y.index, Y.values
    dow = np.array([d.dayofweek for d in dd])
    st0 = int(np.searchsorted(dd, days[0])) - 365
    em, ew = np.full((nD, 24), np.nan), np.full((nD, 24), np.nan)
    mins, maxs, last = AA.min(1), AA.max(1), AA[:, 23]
    for h in range(24):
        rows = np.arange(st0, len(dd))
        X = np.column_stack([AA[rows - 1, h], AA[rows - 2, h], AA[rows - 7, h], mins[rows - 1], maxs[rows - 1],
                             last[rows - 1], dow[rows] == 0, dow[rows] == 5, dow[rows] == 6]).astype(float)
        c, hw = enbpi(X, AA[rows, h], 365, alpha, B=20, block=7, seed=SEED)
        em[:, h] = np.abs(AA[rows[365:], h] - c) > hw
        ew[:, h] = 2 * hw
    miss['enbpi'], wid['enbpi'] = em, ew
    meths.append(('enbpi', 'EnbPI (ridge ensemble)'))
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    out = {}
    cols = {'static': st.Amber, 'rolling': st.MainBlue, 'aci': st.IDAred, 'qt': st.Purple, 'pid': st.Forest, 'enbpi': st.Teal}
    for m, lb in meths:
        mm = np.nanmean(miss[m], axis=1)
        lc = 1 - pd.Series(mm).rolling(30).mean()
        axs[0].plot(days, lc, color=cols[m], lw=1.1, label=lb)
        out[m] = dict(cov=float(1 - np.nanmean(miss[m][n_cal:])), width=float(np.nanmean(wid[m][n_cal:])),
                      lc_min=float(np.nanmin(lc[n_cal:])))
        axs[1].scatter(out[m]['width'], out[m]['cov'], color=cols[m], s=70)
    axs[0].axhline(1 - alpha, color=st.DarkText, ls=':', lw=1)
    axs[0].set_ylabel('coverage, 30-day rolling')
    import matplotlib.dates as mdates
    axs[0].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    axs[0].tick_params(axis='x', labelsize=9.5)
    axs[1].axhline(1 - alpha, color=st.DarkText, ls=':', lw=1)
    axs[1].set_xlabel('mean width (GW)')
    axs[1].set_ylabel('coverage')
    st.fig_legend_bottom(fig, ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch13_pid', save_it)
    out['base'] = base
    out['first'] = str(days[n_cal].date())
    return out


# =============================================================================
# 7. CALIBRATING FOUNDATION-MODEL INTERVALS
# =============================================================================
def fig_fm_calib(save_it=True, w=250, gamma=0.005, w_infl=60):
    """Coverage of the raw 80% intervals (10% and 90% quantiles) of the foundation models and after online CQR:
    80% and 95% intervals from the score max(q10 - y, y - q90) with an ACI threshold on the last w scores (w_infl for
    the monthly inflation streams). Tasks:
    Romanian load (hour by hour), Bitcoin log RV, EU inflation (h = 1, country by country), BET returns."""
    tasks = {}
    days, A, P, Q = load_all()
    tasks['load'] = {k: [(A[:, h], Q[k][:, h, 0], Q[k][:, h, 8]) for h in range(24)] for k in FMS if k in Q}
    d, rv, x, F = rv_forecasts('btc')
    tasks['btc'] = {k: [(x, F[k][2][:, 0], F[k][2][:, 8])] for k in FMS if k in F}
    dates, origins, act, FI = infl_forecasts()
    tasks['infl'] = {k: [(act[:, c, 0], FI[k][1][:, c, 0, 0], FI[k][1][:, c, 0, 8]) for c in range(len(EU27))]
                     for k in FMS if k in FI}
    rd, rr, RQ = returns_fm('bet')
    tasks['bet'] = {k: [(rr, RQ[k][:, 2], RQ[k][:, -3])] for k in FMS if k in RQ}
    out = {}
    W = {'load': w, 'btc': w, 'infl': w_infl, 'bet': w}           # inflation: 27 short monthly streams
    for tk, M in tasks.items():
        out[tk] = {}
        w = W[tk]
        for k, streams in M.items():
            raw, c80, c95, wd80, wraw = [], [], [], [], []
            for y, lo, hi in streams:
                ok = ~np.isnan(y)
                y, lo, hi = y[ok], lo[ok], hi[ok]
                s = np.maximum(lo - y, y - hi)
                raw.append((s <= 0)[w:])
                for a, lst in ((0.2, c80), (0.05, c95)):
                    q, _ = online_threshold(s, a, method='aci', n_cal=w, window=w, gamma=gamma)
                    lst.append((s <= q)[w:])
                    if a == 0.2:
                        qq = np.where(np.isfinite(q[w:]), q[w:], np.nan)
                        wd80.append(np.nanmean(hi[w:] - lo[w:] + 2 * qq))
                        wraw.append(np.mean(hi[w:] - lo[w:]))
            out[tk][k] = dict(raw=float(np.mean(np.concatenate(raw))), c80=float(np.mean(np.concatenate(c80))),
                              c95=float(np.mean(np.concatenate(c95))), wratio=float(np.mean(wd80) / np.mean(wraw)))
    fig, axs = plt.subplots(1, 4, figsize=(12.5, 3.9), sharey=True)
    ttl = {'load': 'Romanian load', 'btc': 'Bitcoin log RV', 'infl': 'EU inflation, h = 1', 'bet': 'BET returns'}
    for ax, tk in zip(axs, out):
        ks = list(out[tk])
        x0 = np.arange(len(ks))
        for j, (f, col, lb) in enumerate((('raw', st.Amber, 'raw 10-90% interval'), ('c80', st.MainBlue, 'conformal 80%'),
                                          ('c95', st.IDAred, 'conformal 95%'))):
            ax.bar(x0 + (j - 1) * 0.27, [out[tk][k][f] for k in ks], width=0.27, color=col, label=lb)
        ax.axhline(0.8, color=st.MainBlue, ls=':', lw=1)
        ax.axhline(0.95, color=st.IDAred, ls=':', lw=1)
        ax.set_xticks(x0)
        ax.set_xticklabels([k.replace('Chronos-Bolt small', 'Bolt-S').replace('TimesFM 2.5', 'TimesFM') for k in ks],
                           rotation=30, fontsize=9.5)
        ax.set_title(ttl[tk], fontsize=11.5)
        ax.set_ylim(0.4, 1.0)
    axs[0].set_ylabel('coverage')
    st.fig_legend_bottom(fig, ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch13_fm_calib', save_it)
    return out


def returns_fm(name, first=None, ctx=1024):
    """Daily log returns (%) and one-day-ahead quantile forecasts of the foundation models at the levels
    0.01, 0.05, 0.1, 0.5, 0.9, 0.95, 0.99 (NaN where a model was not trained on that level)."""
    key = f'ret_{name}'
    if key in _MEM:
        return _MEM[key]
    first = first or RET_FIRST
    r = log_returns(name)
    i0 = int(np.searchsorted(r.index, pd.Timestamp(first)))
    C = [r.values[t - ctx:t] for t in range(i0, len(r))]
    taus = [0.01, 0.05, 0.1, 0.5, 0.9, 0.95, 0.99]
    out = {}
    for nm in FMS:
        Q = fm_cached(f'{key}_{first}_{ctx}', nm, C, 1, taus)
        if Q is not None:
            out[nm] = Q[:, 0, :]
    _MEM[key] = (r.index[i0:], r.values[i0:], out)
    return _MEM[key]


def garch_var(name, first=None, win=1000, refit=250, levels=(0.01, 0.05)):
    """VaR from a GARCH(1,1)-t on a rolling window of `win` days re-estimated every `refit` days (Chapter 9):
    the alpha-quantile of the one-day-ahead predictive distribution (VaR_alpha = -q_alpha)."""
    from scipy import stats as _s
    first = first or RET_FIRST
    r = log_returns(name)
    i0 = int(np.searchsorted(r.index, pd.Timestamp(first)))
    rr = r.values
    Qv = np.full((len(rr) - i0, len(levels)), np.nan)
    par = None
    for j, t in enumerate(range(i0, len(rr))):
        if par is None or j % refit == 0:
            par = garch11_fit(rr[t - win:t], dist='t')
        h = garch11_filter(rr[t - win:t], par)[-1]
        nu = par[3]
        Qv[j] = np.sqrt(h * (nu - 2) / nu) * _s.t.ppf(levels, nu)
    return Qv


def fig_fm_var(save_it=True, w=500, gamma=0.005):
    """VaR 1% and 5% of the BET and the S&P 500, 2016-2026: GARCH-t; Chronos-2 raw quantiles; Chronos-2 + ACI; the
    deciles of Chronos-Bolt, TimesFM and TiRex extended to 1% and 5% by an online one-sided conformal shift of the
    10% quantile (score q10 - y, ACI threshold on the last w scores). Hit rates, Kupiec and Christoffersen p-values,
    the pinball loss and the DM test against GARCH-t."""
    out = {}
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    for ax, nm, lab in ((axs[0], 'bet', 'BET'), (axs[1], 'sp500', 'S&P 500')):
        dates, rr, RQ = returns_fm(nm)
        G = garch_var(nm)
        res = {}
        for a, ka in ((0.01, 0), (0.05, 1)):
            V = {'GARCH-t': G[:, ka]}
            if 'Chronos-2' in RQ:
                V['Chronos-2 raw'] = RQ['Chronos-2'][:, ka]
                s = RQ['Chronos-2'][:, ka] - rr
                q, _ = online_threshold(s, a, method='aci', n_cal=w, window=w, gamma=gamma)
                V['Chronos-2 + ACI'] = RQ['Chronos-2'][:, ka] - np.where(np.isfinite(q), q, np.nan)
            for k in ('Chronos-Bolt small', 'TimesFM 2.5', 'TiRex'):
                if k in RQ:
                    s = RQ[k][:, 2] - rr
                    q, _ = online_threshold(s, a, method='aci', n_cal=w, window=w, gamma=gamma)
                    V[k + ' + conformal'] = RQ[k][:, 2] - np.where(np.isfinite(q), q, np.nan)
            ok = np.all([~np.isnan(v) for v in V.values()], axis=0)
            ok[:w] = False
            rs = {}
            base = pinball(rr[ok], V['GARCH-t'][ok], a)
            for k, v in V.items():
                hit = (rr[ok] < v[ok]).astype(float)
                pl = pinball(rr[ok], v[ok], a)
                rs[k] = dict(hit=float(hit.mean()), kup=kupiec(hit, a)[1], cc=christoffersen(hit, a)['p_cc'],
                             loss=float(pl.mean()), dm=dm_test(pl - base, 1)['hln'], dmp=dm_test(pl - base, 1)['p'])
            res[str(a)] = rs
            res['n'] = int(ok.sum())
            res['first'] = str(dates[ok][0].date())
            if a == 0.01:
                ks = list(rs)
                y = np.arange(len(ks))
                ax.barh(y, [100 * rs[k]['hit'] for k in ks], color=[st.Forest if rs[k]['kup'] >= 0.05 else st.IDAred for k in ks])
                ax.set_yticks(y)
                ax.set_yticklabels(ks)
                ax.axvline(1, color=st.DarkText, ls=':', lw=1)
                ax.set_xlabel('VaR 1%: exceedances (% of days)')
                ax.set_title(lab)
        out[nm] = res
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=st.Forest, label='Kupiec p >= 0.05'), Patch(color=st.IDAred, label='Kupiec p < 0.05')],
               loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False)
    plt.tight_layout(rect=(0, 0.05, 1, 1))
    save('ats_ch13_fm_var', save_it)
    return out


# =============================================================================
# 8. AI MINI-CASE: CHERRY-PICKED BENCHMARKS
# =============================================================================
def fig_ai_case(save_it=True, model='Chronos-2', k=5, years=3, reps=2000, h=12):
    """How often does a random 'benchmark' (k countries, one window of `years` years of origins) make a foundation
    model look significantly better, or significantly worse, than AR(p)? Pooled DM-HLN on the h-step absolute errors
    of the subset; the full-panel verdict for comparison."""
    dates, origins, act, F = infl_forecasts()
    od = dates[origins]
    D = np.abs(act[:, :, h - 1] - F[model][0][:, :, h - 1]) - np.abs(act[:, :, h - 1] - F['AR(p)'][0][:, :, h - 1])
    valid = ~np.isnan(D).any(axis=1)
    rng = np.random.default_rng(SEED)
    yrs = sorted(set(od[valid].year))
    stats_ = []
    for _ in range(reps):
        cs = rng.choice(len(EU27), k, replace=False)
        y0 = rng.choice(yrs[:len(yrs) - years + 1])
        m = valid & (od.year >= y0) & (od.year < y0 + years)
        d = D[m][:, cs].mean(axis=1)
        r = dm_test(d, h)
        stats_.append((r['hln'], r['p']))
    t = np.array([s[0] for s in stats_])
    p = np.array([s[1] for s in stats_])
    full = dm_test(D[valid].mean(axis=1), h)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    tc = np.clip(t, -8, 8)
    ax.hist(tc, bins=64, range=(-8, 8), color=st.MainBlue, alpha=0.7,
            label=f'{reps} random benchmarks ({k} countries, {years} years; clipped at |t| = 8)')
    ax.axvline(full['hln'], color=st.IDAred, lw=2, label='full panel, all origins')
    ax.axvline(-1.96, color=st.Forest, ls='--', lw=1, label='|t| = 1.96')
    ax.axvline(1.96, color=st.Forest, ls='--', lw=1)
    ax.set_xlabel(f'DM-HLN statistic, {model} minus AR(p), h = {h} (negative: {model} better)')
    st.legend_outside_bottom(ax, ncol=3, y=-0.16)
    plt.tight_layout()
    save('ats_ch13_ai_case', save_it)
    return dict(win=float(((p < 0.05) & (t < 0)).mean()), lose=float(((p < 0.05) & (t > 0)).mean()),
                full_t=full['hln'], full_p=full['p'], reps=reps, k=k, years=years)


# =============================================================================
# RUN
# =============================================================================
FIGS = ['tokens', 'zeroshot', 'load', 'covariates', 'inflation', 'ro_inflation', 'multiple', 'rv', 'contamination',
        'scaling', 'split_coverage', 'cqr', 'aci', 'aci_gamma', 'condcov', 'weighted', 'pid', 'fm_calib', 'fm_var', 'ai_case']


def main(names=None):
    """Run the figures and merge their numbers into ch13_numbers.json (re-read before each write)."""
    path = os.path.join(HERE, 'ch13_numbers.json')
    for nm in names or FIGS:
        print('==', nm)
        res = globals()['fig_' + nm]()
        N = json.load(open(path)) if os.path.exists(path) else {}
        N[nm] = res
        with open(path, 'w') as f:
            json.dump(N, f, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))


if __name__ == '__main__':
    main(sys.argv[1:] or None)
