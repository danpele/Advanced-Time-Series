"""
generate_all_charts.py -- charts and numbers of Chapter 12 (ATS): machine learning and deep learning for time series
=====================================================================================================================
Course data (ats_data.py), chart style (ats_style.py), the engine ml_core.py (numpy, scikit-learn, PyTorch on CPU with
small models and fixed seeds). Every number on the slides comes from here.
  * learning from dependent data   the Monte Carlo design of Bergmeir, Hyndman and Koo (2018, Section 4): 5-fold CV,
                                   LOOCV, non-dependent CV and OOS for AR(3), MA(1) and seasonal AR data; leakage
                                   with overlapping h-step targets and a random forest (random, blocked, purged folds);
  * high dimension, globality      EU inflation (Eurostat HICP, 27 countries): local against global AR models across
                                   memory lengths (Montero-Manso and Hyndman 2021); lasso, adaptive lasso, elastic
                                   net and ridge on the EU panel for Romanian inflation 12 months ahead;
  * tree ensembles                 Romanian day-ahead load (Energy-Charts, ENTSO-E data): the expert ARX of Chapter 1,
                                   a random forest with quantile regression forest bands, histogram gradient boosting
                                   with and without monotone constraints, quantile boosting; MCS;
  * recurrent networks             gradients through time of RNN, LSTM and GRU at initialisation;
  * deep models against HAR        S&P 500 realised variance (Oxford-Man library): HAR, MLP, LSTM, TCN, boosting;
                                   seeds and data snooping; exact Shapley values of lag groups;
  * Transformers and linear models the protocol of Zeng et al. (2023) on Romanian hourly load: repeat, seasonal naive,
                                   Linear, NLinear, DLinear and a patch Transformer; attention against occlusion;
  * N-BEATS, N-HiTS, DeepAR        the M4 hourly subset (414 series, horizon 48): naive benchmarks, global N-BEATS,
                                   N-HiTS and DLinear (sMAPE, MASE, OWA); DeepAR-type probabilistic forecasts;
  * AI mini-case                   do deep models beat HAR? six indices, three horizons, pre-registered design.
Output: charts/ats_ch12_*.pdf/.png, Quantlets/Ch_12/ch12_numbers.json
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_12/generate_all_charts.py [name ...]
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
from ats_data import read_omi                                                                        # noqa: E402
import ats_style as st                                                                               # noqa: E402
from ml_core import (TORCH, QRF, DeepARNet, LinearNet, MLPNet, NBeatsNet, PatchTransformer, RNNNet,   # noqa: E402,F401
                     TCNNet, ar_sim, bhk_trial, deepar_sample, deepar_train, dm_test, embed, fit_torch,
                     grad_through_time, mase, mcs, ols, penalised_fit, pinball, predict_torch, purged_folds, qlike,
                     random_stationary_ar, set_seed, shapley_groups, smape)

warnings.filterwarnings('ignore')
SEED = 2026
REAL_RAW = 'https://raw.githubusercontent.com/danpele/Advanced-Time-Series/main/data/realized/'
REAL_DIR = next((p for p in [os.path.join(HERE, '..', '..', 'data', 'realized')]
                 + [os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..')]
                 if os.path.isdir(p)), '')
OMI_NAMES = {'.SPX': 'S&P 500', '.GDAXI': 'DAX', '.FTSE': 'FTSE 100', '.N225': 'Nikkei 225',
             '.STOXX50E': 'Euro Stoxx 50', '.FCHI': 'CAC 40'}
LOAD_API = 'https://api.energy-charts.info/public_power?country=ro&start={a}&end={b}'   # Romanian load, ENTSO-E data
LOAD_YEARS = (2023, 2024, 2025, 2026)
LOAD_END = '2026-09-30'
LOAD_EVAL = '2025-01-01'                       # first forecast day of the day-ahead comparison
EU27 = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU',
        'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']
HICP = ('prc_hicp_minr', 'M.RCH_A.TOTAL.')     # HICP, annual rate of change, % (Eurostat)
INFL = dict(start='2000-01-01', first='2015-01-01', win=120, lags=(1, 2, 3, 6, 12, 18, 24, 36), x_lags=3)
M4_RAW = 'https://raw.githubusercontent.com/Mcompetitions/M4-methods/master/Dataset/'
M4H = dict(H=48, m=24, L=336)                   # M4 hourly: horizon, seasonal period, look-back of the global models
ZENG = dict(L=336, horizons=(96, 336), split=(0.7, 0.1, 0.2))   # Zeng et al. (2023): look-back, horizons, 7:1:2 split
RV = dict(lags=22, first=2500, refit=500, horizons=(1, 5, 22))  # deep models against HAR (expanding window)
TAUS9 = np.arange(1, 10) / 10
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


def read_realized(fname, **kw):
    """A file of data/realized: local copy of the course data, otherwise the ATS repository on GitHub."""
    p = os.path.join(REAL_DIR, fname) if REAL_DIR else ''
    return pd.read_csv(p if p and os.path.exists(p) else REAL_RAW + fname, **kw)


def omi(symbol='.SPX', col='rv5'):
    """Oxford-Man realized library v0.3 (Heber, Lunde, Shephard and Sheppard 2009): daily 5-minute realised variance
    of one index, in %^2; non-positive days dropped."""
    if 'omi' not in _MEM:
        _MEM['omi'] = read_omi()
    d = _MEM['omi']
    s = d[d['symbol'] == symbol].set_index('date').sort_index()[col] * 1e4
    return s[s > 0].dropna().rename(OMI_NAMES[symbol])


def ro_load_hourly():
    """Romanian hourly electricity load (GW), local time, 2023 to LOAD_END (Energy-Charts, ENTSO-E transparency data):
    15-minute values averaged within each hour; a days x 24 table (DST days: 23 or 25 hours become 24)."""
    import json as _json
    if 'load' in _MEM:
        return _MEM['load']
    parts = []
    for y in LOAD_YEARS:
        b = min(f'{y}-12-31', LOAD_END)
        d = _json.loads(get_bytes(LOAD_API.format(a=f'{y}-01-01', b=b)))
        load = [x for x in d['production_types'] if x['name'] == 'Load'][0]['data']
        parts.append(pd.Series(load, index=pd.to_datetime(d['unix_seconds'], unit='s', utc=True), dtype=float))
    s = pd.concat(parts).sort_index()
    s = s[~s.index.duplicated()].tz_convert('Europe/Bucharest')
    df = pd.DataFrame({'y': s.values, 'day': s.index.tz_localize(None).normalize(), 'hour': s.index.hour})
    tab = df.groupby(['day', 'hour'])['y'].mean().unstack('hour')
    tab = tab.interpolate(axis=1, limit_direction='both').interpolate(axis=0, limit_direction='both')
    _MEM['load'] = tab.loc[:LOAD_END] / 1000.0
    return _MEM['load']


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


def m4_hourly():
    """The hourly subset of the M4 competition (414 series): training parts (list of arrays) and test parts (414 x 48)."""
    if 'm4' in _MEM:
        return _MEM['m4']
    tr = pd.read_csv(io.BytesIO(get_bytes(M4_RAW + 'Train/Hourly-train.csv')), index_col=0)
    te = pd.read_csv(io.BytesIO(get_bytes(M4_RAW + 'Test/Hourly-test.csv')), index_col=0)
    train = [r.dropna().values.astype(float) for _, r in tr.iterrows()]
    _MEM['m4'] = (train, te.values.astype(float), list(tr.index))
    return _MEM['m4']


# =============================================================================
# 1. OVERVIEW OF THE DATA
# =============================================================================
def fig_overview(save_it=True):
    """Four data sets of the chapter: Romanian load, EU inflation, S&P 500 realised variance, M4 hourly series."""
    Y = ro_load_hourly()
    P = eu_hicp()
    rv = omi('.SPX')
    train, test, ids = m4_hourly()
    fig, axs = plt.subplots(2, 2, figsize=(11, 6.2))
    daily = Y.mean(axis=1)
    axs[0, 0].plot(daily.index, daily.values, color=st.MainBlue, lw=0.8, label='Romanian load, daily mean (GW)')
    axs[0, 0].set_ylabel('GW')
    import matplotlib.dates as mdates
    axs[0, 0].xaxis.set_major_locator(mdates.YearLocator())
    axs[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    for c in EU27:
        if c != 'RO':
            axs[0, 1].plot(P.index, P[c], color=st.Teal, lw=0.4, alpha=0.5, label='_')
    axs[0, 1].plot(P.index, P['RO'], color=st.IDAred, lw=1.4, label='Romania')
    axs[0, 1].plot([], [], color=st.Teal, lw=1, label='other EU countries')
    axs[0, 1].set_ylabel('HICP inflation, % y/y')
    axs[1, 0].semilogy(rv.index, rv.values, color=st.Forest, lw=0.5, label='S&P 500 realised variance (%$^2$)')
    for i, c in zip((0, 100, 300), (st.Purple, st.Orange, st.Amber)):
        s = train[i][-24 * 14:]
        axs[1, 1].plot(np.arange(len(s)), s / s.mean(), color=c, lw=0.9, label=f'M4 {ids[i]}')
    axs[1, 1].set_xlabel('hour (last two weeks of the training part)')
    axs[1, 1].set_ylabel('level / mean')
    for a in axs.ravel()[:3]:
        st.legend_outside_bottom(a, ncol=2, y=-0.14)
    st.legend_outside_bottom(axs[1, 1], ncol=3, y=-0.28)
    plt.tight_layout()
    save('ats_ch12_overview', save_it)
    return dict(load_days=int(len(Y)), load_start=str(Y.index[0].date()), load_end=str(Y.index[-1].date()),
                hicp_start=str(P.index[0].date()), hicp_end=str(P.index[-1].date()), hicp_n=int(len(P)),
                rv_n=int(len(rv)), rv_start=str(rv.index[0].date()), rv_end=str(rv.index[-1].date()),
                m4_n=len(train), m4_min=int(min(map(len, train))), m4_max=int(max(map(len, train))),
                load_mean=float(Y.values.mean()), load_min=float(Y.values.min()), load_max=float(Y.values.max()))


# =============================================================================
# 2. LEARNING FROM DEPENDENT DATA
# =============================================================================
def usaccdeaths_sar():
    """Seasonal AR(1)(1)_12 fitted to the monthly US accidental deaths 1973-1978 (Brockwell and Davis 1991), the
    counterexample DGP of Bergmeir, Hyndman and Koo (2018): returns (phi, Phi, sigma) on the standardised series."""
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    u = pd.read_csv(io.BytesIO(get_bytes('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/USAccDeaths.csv')))
    x = u.iloc[:, -1].values.astype(float)
    z = (x - x.mean()) / x.std()
    r = SARIMAX(z, order=(1, 0, 0), seasonal_order=(1, 0, 0, 12), trend='c').fit(disp=False)
    return float(r.params[1]), float(r.params[2]), float(np.sqrt(r.params[3]))


def cv_experiment(reps=1000, n=200, seed=SEED):
    """Bergmeir, Hyndman and Koo (2018, Section 4): 1000 series of length 200 per DGP (stationary AR(3) with random
    coefficients, invertible MA(1) with random coefficient, the seasonal AR fitted to USAccDeaths); MAPAE and MPAE of
    the RMSE estimates of each procedure against the out-set RMSE."""
    rng = np.random.default_rng(seed)
    phi1, Phi, sg = usaccdeaths_sar()
    sar = np.zeros(13)
    sar[0], sar[11], sar[12] = phi1, Phi, -phi1 * Phi
    out = {}
    for dgp in ('AR(3)', 'MA(1)', 'SAR'):
        recs = []
        for r in range(reps):
            if dgp == 'AR(3)':
                y = ar_sim(random_stationary_ar(3, rng), n, rng=rng)
            elif dgp == 'MA(1)':
                y = ar_sim([], n, rng=rng, theta=[rng.uniform(-1, 1)])
            else:
                y = ar_sim(sar, n, burn=200, rng=rng, sigma=sg)
            recs.append(bhk_trial(y, rng=rng))
        res = {}
        for mdl in recs[0]:
            res[mdl] = {}
            for pr in ('5-fold CV', 'LOOCV', 'nonDepCV', 'OOS'):
                e = np.array([rr[mdl][pr] - rr[mdl]['true'] for rr in recs])
                res[mdl][pr] = dict(mapae=float(np.mean(np.abs(e))), mpae=float(np.mean(e)))
        out[dgp] = res
    out['sar_par'] = [phi1, Phi, sg]
    out['reps'] = reps
    return out


def fig_cv_bhk(save_it=True, reps=1000):
    r = cv_experiment(reps)
    fig, axs = plt.subplots(2, 3, figsize=(11.5, 6.0), sharex=True)
    cols = {'5-fold CV': st.MainBlue, 'LOOCV': st.Teal, 'nonDepCV': st.Amber, 'OOS': st.IDAred}
    p = np.arange(1, 6)
    for j, dgp in enumerate(('AR(3)', 'MA(1)', 'SAR')):
        for pr, c in cols.items():
            axs[0, j].plot(p, [r[dgp][f'AR({k})'][pr]['mapae'] for k in p], 'o-', color=c, label=pr, ms=4)
            axs[1, j].plot(p, [r[dgp][f'AR({k})'][pr]['mpae'] for k in p], 'o-', color=c, label=pr, ms=4)
        axs[1, j].axhline(0, color=st.DarkText, lw=0.6, ls=':')
        axs[0, j].set_title({'AR(3)': 'DGP: AR(3)', 'MA(1)': 'DGP: MA(1)', 'SAR': 'DGP: seasonal AR (counterexample)'}[dgp])
        axs[1, j].set_xlabel('fitted model AR(p)')
    for a in axs[0]:
        a.set_yscale('log')
    axs[0, 0].set_ylabel('MAPAE (precision, log)')
    axs[1, 0].set_ylabel('MPAE (bias)')
    plt.tight_layout()
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.subplots_adjust(bottom=0.16)
    save('ats_ch12_cv_bhk', save_it)
    return r


def leakage_experiment(reps=60, n=1000, h=20, phi=0.9, k=5, seed=SEED):
    """Overlapping targets: y_t AR(1); target = mean of y_{t+1..t+h}; features = y_t..y_{t-4} and the time index (a
    typical 'date' feature); random forest.
    Estimated RMSE from random 5-fold, blocked 5-fold, blocked 5-fold with a purge of h rows, the last 20%, against
    the RMSE on 1000 new observations from the same process."""
    from sklearn.ensemble import RandomForestRegressor
    rng = np.random.default_rng(seed)
    rows = []
    for r in range(reps):
        y = ar_sim([phi], 2 * n + 2 * h + 10, rng=rng)
        c = np.concatenate([[0.0], np.cumsum(y)])
        t = np.arange(4, len(y) - h)
        X = np.column_stack([y[t - k] for k in range(5)] + [t])          # y_t, ..., y_{t-4} and a time index
        z = (c[t + h + 1] - c[t + 1]) / h                               # mean of y_{t+1}, ..., y_{t+h}
        Xi, zi, Xo, zo = X[:n], z[:n], X[n + h:], z[n + h:]
        rf = lambda: RandomForestRegressor(n_estimators=50, min_samples_leaf=1, max_features=1.0, random_state=r, n_jobs=1)
        est = {}
        e = np.empty(n)
        f = np.random.default_rng(r).permutation(np.arange(n) % k)
        for j in range(k):
            m = rf().fit(Xi[f != j], zi[f != j])
            e[f == j] = zi[f == j] - m.predict(Xi[f == j])
        est['random 5-fold'] = np.sqrt(np.mean(e ** 2))
        for name, gap in (('blocked 5-fold', 0), ('purged 5-fold', h)):
            e = np.empty(n)
            for tr, te in purged_folds(n, k, gap):
                m = rf().fit(Xi[tr], zi[tr])
                e[te] = zi[te] - m.predict(Xi[te])
            est[name] = np.sqrt(np.mean(e ** 2))
        no = int(0.2 * n)
        m = rf().fit(Xi[:n - no - h], zi[:n - no - h])
        est['last 20%'] = np.sqrt(np.mean((zi[n - no:] - m.predict(Xi[n - no:])) ** 2))
        m = rf().fit(Xi, zi)
        true = np.sqrt(np.mean((zo - m.predict(Xo)) ** 2))
        rows.append({kk: v / true for kk, v in est.items()})
    return pd.DataFrame(rows)


def fig_leakage(save_it=True, reps=60):
    d = leakage_experiment(reps)
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    cols = [st.IDAred, st.MainBlue, st.Forest, st.Amber]
    b = ax.boxplot([d[c] for c in d.columns], vert=False, patch_artist=True, widths=0.55)
    from matplotlib.colors import to_rgba
    for patch, c in zip(b['boxes'], cols):
        patch.set_facecolor(to_rgba(c, 0.55))      # translucent fill, opaque coloured edge (no grey outline)
        patch.set_edgecolor(c)
    for part in ('whiskers', 'caps', 'medians'):
        for ln in b[part]:
            ln.set_color(st.DarkText)
    ax.set_yticks(range(1, len(d.columns) + 1))
    ax.set_yticklabels(d.columns)
    ax.axvline(1, color=st.DarkText, ls=':', lw=1)
    ax.set_xlabel('estimated RMSE / RMSE on new data (1 = unbiased)')
    for c, lab in zip(cols, d.columns):
        ax.plot([], [], color=c, lw=6, alpha=0.55, label=lab)
    st.legend_outside_bottom(ax, ncol=4, y=-0.25)
    plt.tight_layout()
    save('ats_ch12_leakage', save_it)
    return {c: dict(med=float(d[c].median()), q1=float(d[c].quantile(0.25)), q3=float(d[c].quantile(0.75))) for c in d.columns} | {'reps': reps}


# =============================================================================
# 3. GLOBAL AND LOCAL MODELS, HIGH-DIMENSIONAL REGRESSION: EU INFLATION
# =============================================================================
def lagmat(x, p):
    """Columns x_t, x_{t-1}, ..., x_{t-p+1} (NaN at the start)."""
    return np.column_stack([np.r_[np.full(k, np.nan), x[:len(x) - k]] for k in range(p)])


def global_local(h=12, lags=INFL['lags'], win=INFL['win'], first=INFL['first']):
    """Direct h-step forecasts of annual HICP inflation of the 27 EU countries from rolling windows of `win` months:
    local AR(p) (one OLS per country) against global AR(p) (one pooled OLS, the same coefficients for all
    countries; Montero-Manso and Hyndman 2021). Returns squared errors: dict p -> (local, global), each origins x 27."""
    P = eu_hicp()
    Y = P.values
    T, N = Y.shape
    dates = P.index
    o0 = int(np.searchsorted(dates, pd.Timestamp(first)))
    out = {}
    for p in lags:
        L = [lagmat(Y[:, i], p) for i in range(N)]
        el, eg = [], []
        for t in range(o0, T - h):
            rows = np.arange(max(t - win + 1, p - 1), t - h + 1)       # targets y_{s+h} known at t
            Xg, yg = [], []
            fl, fg = np.empty(N), np.empty(N)
            for i in range(N):
                X, y = L[i][rows], Y[rows + h, i]
                fl[i] = ols(X, y, L[i][t:t + 1])[0]
                Xg.append(X)
                yg.append(y)
            Xg, yg = np.vstack(Xg), np.concatenate(yg)
            for i in range(N):
                fg[i] = ols(Xg, yg, L[i][t:t + 1])[0]
            el.append((Y[t + h] - fl) ** 2)
            eg.append((Y[t + h] - fg) ** 2)
        out[p] = (np.array(el), np.array(eg))
    return out, list(P.columns)


def fig_global_local(save_it=True, lags=INFL['lags']):
    res = {}
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.0))
    for ax, h in zip(axs, (1, 12)):
        r, cn = global_local(h, lags)
        ro = cn.index('RO')
        loc = [np.sqrt(r[p][0].mean()) for p in lags]
        glo = [np.sqrt(r[p][1].mean()) for p in lags]
        lro = [np.sqrt(r[p][0][:, ro].mean()) for p in lags]
        gro = [np.sqrt(r[p][1][:, ro].mean()) for p in lags]
        ax.plot(lags, loc, 'o-', color=st.IDAred, label='local AR(p), 27 countries')
        ax.plot(lags, glo, 'o-', color=st.MainBlue, label='global AR(p), 27 countries')
        ax.plot(lags, lro, 's--', color=st.Orange, label='local AR(p), Romania')
        ax.plot(lags, gro, 's--', color=st.Teal, label='global AR(p), Romania')
        ax.set_xlabel('memory p (months)')
        ax.set_ylabel('RMSE, percentage points')
        ax.set_title(f'h = {h} month' + ('s' if h > 1 else '') + ' ahead')
        best_l, best_g = int(lags[int(np.argmin(loc))]), int(lags[int(np.argmin(glo))])
        dg = r[best_g][1][:, ro] - r[best_l][0][:, ro]
        dm = dm_test(dg, h)
        dall = (r[best_g][1] - r[best_l][0]).mean(axis=1)
        res[str(h)] = dict(local=loc, glob=glo, local_ro=lro, glob_ro=gro, best_l=best_l, best_g=best_g,
                           dm_ro=dm['hln'], p_ro=dm['p_hln'], dm_all=dm_test(dall, h)['hln'], p_all=dm_test(dall, h)['p_hln'],
                           T=int(r[lags[0]][0].shape[0]))
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch12_global_local', save_it)
    res['lags'] = list(lags)
    return res


def ro_highdim(h=12, win=INFL['win'], first=INFL['first'], p=INFL['x_lags'], refit=3):
    """Romanian inflation h months ahead from the EU panel on rolling windows of `win` months, re-estimated every
    `refit` months: AR(3) (local benchmark); ridge, lasso, adaptive lasso and elastic net on the 3 own lags (not
    penalised) plus 3 lags of the 26 other countries (78 penalised features; penalty by blocked CV with a purge of h
    months); post-lasso OLS; the global AR(12) of the panel."""
    from sklearn.linear_model import Ridge
    P = eu_hicp()
    Y = P.values
    T, N = Y.shape
    cn = list(P.columns)
    ro = cn.index('RO')
    others = [i for i in range(N) if i != ro]
    Z = np.column_stack([lagmat(Y[:, ro], p)] + [lagmat(Y[:, i], p) for i in others])   # own lags first
    own = list(range(p))
    L12 = [lagmat(Y[:, i], 12) for i in range(N)]
    dates = P.index
    o0 = int(np.searchsorted(dates, pd.Timestamp(first)))
    names = ['AR(3)', 'ridge', 'lasso', 'adaptive lasso', 'elastic net', 'post-lasso OLS', 'global AR(12)']
    F = {k: [] for k in names}
    sel, yv, od = [], [], []
    par = {}
    for t in range(o0, T - h):
        rows = np.arange(max(t - win + 1, 11), t - h + 1)
        X, y, x0 = Z[rows], Y[rows + h, ro], Z[t:t + 1]
        if (t - o0) % refit == 0:
            par = {'AR(3)': ols_coef(X[:, own], y)}
            K = np.column_stack([np.ones(len(y)), X[:, own]])
            Xo = X[:, p:]
            mu, sd = Xo.mean(0), Xo.std(0) + 1e-12
            r = Ridge(alpha=float(len(y))).fit(np.column_stack([X[:, own] * 1e3, (Xo - mu) / sd]), y)   # own lags nearly unpenalised
            par['ridge'] = (r, mu, sd)
            for kind, nm in (('lasso', 'lasso'), ('adaptive', 'adaptive lasso'), ('enet', 'elastic net')):
                a, b, _, s = penalised_fit(X, y, kind, keep=own, gap=h)
                par[nm] = (a, b)
                if kind == 'lasso':
                    par['sel'] = s
                    cols = own + [p + j for j in np.where(s)[0]]
                    par['post-lasso OLS'] = (cols, ols_coef(X[:, cols], y))
            Xg = np.vstack([L12[i][rows] for i in range(N)])
            yg = np.concatenate([Y[rows + h, i] for i in range(N)])
            par['global AR(12)'] = ols_coef(Xg, yg)
        F['AR(3)'].append(np.r_[1.0, x0[0, own]] @ par['AR(3)'])
        r, mu, sd = par['ridge']
        F['ridge'].append(r.predict(np.column_stack([x0[:, own] * 1e3, (x0[:, p:] - mu) / sd]))[0])
        for nm in ('lasso', 'adaptive lasso', 'elastic net'):
            a, b = par[nm]
            F[nm].append(a + x0[0] @ b)
        cols, b = par['post-lasso OLS']
        F['post-lasso OLS'].append(np.r_[1.0, x0[0, cols]] @ b)
        F['global AR(12)'].append(np.r_[1.0, L12[ro][t]] @ par['global AR(12)'])
        sel.append(par['sel'])
        yv.append(Y[t + h, ro])
        od.append(dates[t + h])
    return {k: np.array(v) for k, v in F.items()}, np.array(yv), np.array(sel), od, [cn[i] for i in others]


def ols_coef(X, y):
    """OLS coefficients with an intercept (first)."""
    A = np.column_stack([np.ones(len(X)), X])
    return np.linalg.lstsq(A, y, rcond=None)[0]


def fig_ro_lasso(save_it=True, h=12, refit=3):
    F, y, S, od, cn = ro_highdim(h, refit=refit)
    p = INFL['x_lags']
    N = len(cn)                                                          # the 26 other countries
    blocks = S.reshape(len(S), N, p).any(axis=2)                        # a country is selected if any of its lags is
    years = pd.DatetimeIndex(od).year
    yrs = sorted(set(years))
    freq = np.array([blocks[years == yy].mean(axis=0) for yy in yrs]).T
    e = {k: (y - f) ** 2 for k, f in F.items()}
    rmse = {k: float(np.sqrt(v.mean())) for k, v in e.items()}
    dm = {k: dm_test(e[k] - e['AR(3)'], h) for k in F if k != 'AR(3)'}
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw={'width_ratios': [1.25, 1]})
    im = axs[0].imshow(freq, aspect='auto', cmap='Blues', vmin=0, vmax=1)
    axs[0].set_yticks(range(N))
    axs[0].set_yticklabels(cn, fontsize=7)
    axs[0].set_xticks(range(len(yrs)))
    axs[0].set_xticklabels([str(v)[2:] for v in yrs], fontsize=9)
    axs[0].set_xlabel('year of the target (20..)')
    plt.colorbar(im, ax=axs[0], fraction=0.04, pad=0.02, label='share of origins with the country selected')
    ks = [k for k in F if k != 'AR(3)']
    rel = [rmse[k] / rmse['AR(3)'] for k in ks]
    cols = [st.MainBlue if dm[k]['p_hln'] < 0.05 and r < 1 else st.IDAred if dm[k]['p_hln'] < 0.05 else st.Amber for k, r in zip(ks, rel)]
    axs[1].barh(range(len(ks)), rel, color=cols)
    axs[1].set_yticks(range(len(ks)))
    axs[1].set_yticklabels(ks)
    axs[1].axvline(1, color=st.DarkText, ls=':', lw=1)
    axs[1].set_xlabel('RMSE relative to AR(3), Romania, h = 12')
    from matplotlib.patches import Patch
    hd = [Patch(color=st.MainBlue, label='better, DM p < 0.05'), Patch(color=st.Amber, label='not significant'),
          Patch(color=st.IDAred, label='worse, DM p < 0.05')]
    axs[1].legend(handles=hd, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)
    plt.tight_layout()
    save('ats_ch12_ro_lasso', save_it)
    tot = blocks.mean(axis=0)
    top = np.argsort(-tot)[:5]
    return dict(rmse=rmse, dm={k: dict(t=v['hln'], p=v['p_hln']) for k, v in dm.items()}, T=int(len(y)),
                n_sel_med=float(np.median(S.sum(axis=1))), n_sel_min=int(S.sum(axis=1).min()), n_sel_max=int(S.sum(axis=1).max()),
                top=[cn[i] for i in top], top_share=[float(tot[i]) for i in top], never=int((tot == 0).sum()),
                n_feat=int(S.shape[1]), first=str(od[0].date()), last=str(od[-1].date()))


# =============================================================================
# 4. TREE ENSEMBLES: ROMANIAN DAY-AHEAD LOAD
# =============================================================================
def load_features(Y):
    """Rows (day d+1, hour h) of the day-ahead problem with data up to day d: load at the same hour on days d, d - 1
    and d - 6, the minimum, maximum and last hour of day d, the hour, the day of the week, a holiday dummy, the
    annual cycle. Returns X, y, day index, hour, feature names."""
    A = Y.values
    days = Y.index
    nD = len(days)
    hol = set(ro_holidays(range(days[0].year, days[-1].year + 1)))
    d1 = np.repeat(np.arange(7, nD), 24)
    hh = np.tile(np.arange(24), nD - 7)
    doy = np.array([days[i].dayofyear for i in d1])
    dow = np.array([days[i].dayofweek for i in d1])
    X = np.column_stack([A[d1 - 1, hh], A[d1 - 2, hh], A[d1 - 7, hh], A[d1 - 1].min(1), A[d1 - 1].max(1), A[d1 - 1, 23],
                         hh, dow, [days[i] in hol for i in d1], [days[i - 1] in hol for i in d1],
                         np.sin(2 * np.pi * doy / 365.25), np.cos(2 * np.pi * doy / 365.25)]).astype(float)
    names = ['load d', 'load d-1', 'load d-6', 'min d', 'max d', 'last hour d', 'hour', 'weekday', 'holiday',
             'holiday d', 'sin year', 'cos year']
    return X, A[d1, hh], d1, hh, names


MONO = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]       # boosting: increasing in the three load lags


def load_tree_forecasts(first=LOAD_EVAL, refit='MS', n_trees=100):
    """Day-ahead forecasts of the 24 hourly loads from `first` to LOAD_END, re-estimated at the start of each month on
    all earlier data: the expert ARX of Chapter 1 (Ziel and Weron 2018; one regression per hour, 364-day window,
    empirical quantiles of the last 182 days of errors), a random forest with QRF quantiles, boosting (HGB) with and
    without monotone constraints and HGB quantile regressions (deciles). Returns a long DataFrame."""
    from sklearn.ensemble import HistGradientBoostingRegressor as HGB
    Y = ro_load_hourly()
    X, y, d1, hh, names = load_features(Y)
    days = Y.index
    A = Y.values
    dates = days[d1]
    starts = pd.date_range(first, LOAD_END, freq=refit)
    out = []
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else pd.Timestamp(LOAD_END) + pd.Timedelta(days=1)
        tr = dates < s
        te = (dates >= s) & (dates < e)
        res = dict(day=dates[te], hour=hh[te], y=y[te])
        hgb = lambda **kw: HGB(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40,
                               random_state=SEED, categorical_features=[6, 7], **kw)
        res['HGB'] = hgb().fit(X[tr], y[tr]).predict(X[te])
        res['HGB monotone'] = hgb(monotonic_cst=MONO).fit(X[tr], y[tr]).predict(X[te])
        for tau in TAUS9:
            res[f'HGBq{tau:.1f}'] = hgb(loss='quantile', quantile=tau).fit(X[tr], y[tr]).predict(X[te])
        q = QRF(n_estimators=n_trees, min_samples_leaf=10, max_features=0.5, seed=SEED).fit(X[tr], y[tr])
        res['RF'] = q.predict(X[te])
        Q = q.quantiles(X[te], TAUS9)
        for j, tau in enumerate(TAUS9):
            res[f'QRFq{tau:.1f}'] = Q[:, j]
        out.append(pd.DataFrame(res))
    D = pd.concat(out, ignore_index=True)
    # expert ARX (Chapter 1): rolling 364-day window, one regression per hour, refitted every day
    dow = np.array([d.dayofweek for d in days])
    mins, maxs, last = A.min(axis=1), A.max(axis=1), A[:, 23]
    s0 = int(np.searchsorted(days, pd.Timestamp(first)))
    P = np.full(A.shape, np.nan)
    for dd in range(s0 - 182, len(days)):
        rows = np.arange(dd - 364, dd)
        for h in range(24):
            Xa = np.column_stack([np.ones(len(rows)), A[rows - 1, h], A[rows - 2, h], A[rows - 7, h], mins[rows - 1],
                                  maxs[rows - 1], last[rows - 1], dow[rows] == 0, dow[rows] == 5, dow[rows] == 6])
            b = np.linalg.lstsq(Xa, A[rows, h], rcond=None)[0]
            P[dd, h] = np.r_[1.0, A[dd - 1, h], A[dd - 2, h], A[dd - 7, h], mins[dd - 1], maxs[dd - 1], last[dd - 1],
                             dow[dd] == 0, dow[dd] == 5, dow[dd] == 6] @ b
    E = A - P
    di = np.searchsorted(days, D['day'].values)
    D['ARX'] = P[di, D['hour'].values]
    D['ARX + HGB'] = 0.5 * (D['ARX'] + D['HGB monotone'])                  # equal-weight combination (Chapter 1)
    QA = np.array([[P[dd, h] + np.nanquantile(E[dd - 182:dd, h], TAUS9) for h in range(24)] for dd in range(s0, len(days))])
    for j, tau in enumerate(TAUS9):
        D[f'ARXq{tau:.1f}'] = QA[di - s0, D['hour'].values, j]
    return D


def fig_load_trees(save_it=True, n_trees=100, refit='MS'):
    D = load_tree_forecasts(refit=refit, n_trees=n_trees)
    D = D.sort_values(['day', 'hour']).reset_index(drop=True)
    pts = ['ARX', 'RF', 'HGB', 'HGB monotone', 'ARX + HGB']
    mae = {k: float(np.mean(np.abs(D['y'] - D[k]))) for k in pts}
    daily = pd.DataFrame({k: np.abs(D['y'] - D[k]).groupby(D['day']).mean() for k in pts})
    M = mcs(daily)
    dmv = {k: dm_test(daily[k] - daily['ARX'], 1) for k in pts if k != 'ARX'}
    pin, cov = {}, {}
    for k in ('ARX', 'QRF', 'HGB'):
        L = np.mean([pinball(D['y'], D[f'{k}q{t:.1f}'], t) for t in TAUS9], axis=0)
        pin[k] = float(L.mean())
        cov[k] = float(np.mean((D['y'] >= D[f'{k}q0.1']) & (D['y'] <= D[f'{k}q0.9'])))
        D[f'pin_{k}'] = L
    dpin = pd.DataFrame({k: D[f'pin_{k}'].groupby(D['day']).mean() for k in ('ARX', 'QRF', 'HGB')})
    Mq = mcs(dpin)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0), gridspec_kw={'width_ratios': [1.6, 1]})
    wk = D[(D['day'] >= '2026-01-12') & (D['day'] < '2026-01-19')]
    x = np.arange(len(wk))
    axs[0].fill_between(x, wk['QRFq0.1'], wk['QRFq0.9'], color=st.Teal, alpha=0.3, label='QRF 10%-90%')
    axs[0].plot(x, wk['y'], color=st.DarkText, lw=1.3, label='load')
    axs[0].plot(x, wk['ARX'], color=st.IDAred, lw=1, ls='--', label='expert ARX')
    axs[0].plot(x, wk['HGB monotone'], color=st.MainBlue, lw=1, label='HGB monotone')
    axs[0].set_xticks(np.arange(0, len(wk), 24))
    axs[0].set_xticklabels([d.strftime('%a %d %b') for d in wk['day'].iloc[::24]], fontsize=8)
    axs[0].set_ylabel('GW')
    st.legend_outside_bottom(axs[0], ncol=4, y=-0.18)
    ks = pts
    axs[1].bar(range(len(ks)), [1000 * mae[k] for k in ks], color=[st.IDAred, st.Forest, st.Amber, st.MainBlue, st.Purple])
    for i, k in enumerate(ks):
        axs[1].text(i, 1000 * mae[k], 'MCS' if k in M['set'] else '', ha='center', va='bottom', fontsize=9, color=st.DarkText)
    axs[1].set_xticks(range(len(ks)))
    axs[1].set_xticklabels(ks, rotation=15, fontsize=9)
    axs[1].set_ylabel('MAE, MW')
    plt.tight_layout()
    save('ats_ch12_load_trees', save_it)
    return dict(mae=mae, mcs=M['p'], dm={k: dict(t=v['hln'], p=v['p_hln']) for k, v in dmv.items()}, pin=pin, cov=cov,
                mcs_q=Mq['p'], days=int(D['day'].nunique()), first=str(D['day'].min().date()), last=str(D['day'].max().date()))


def fig_monotone(save_it=True):
    """Partial dependence of boosted trees on the load of day d at the same hour, with and without the monotone
    constraint, trained on all data before LOAD_EVAL."""
    from sklearn.ensemble import HistGradientBoostingRegressor as HGB
    Y = ro_load_hourly()
    X, y, d1, hh, names = load_features(Y)
    tr = Y.index[d1] < pd.Timestamp(LOAD_EVAL)
    grid = np.linspace(np.quantile(X[tr, 0], 0.01), np.quantile(X[tr, 0], 0.99), 60)
    ref = X[tr][::25]
    out = {}
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    for lab, kw, c in (('unconstrained', {}, st.IDAred), ('monotone increasing', {'monotonic_cst': MONO}, st.MainBlue)):
        m = HGB(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40, random_state=SEED,
                categorical_features=[6, 7], **kw).fit(X[tr], y[tr])
        pd_ = []
        for g in grid:
            Z = ref.copy()
            Z[:, 0] = g
            pd_.append(m.predict(Z).mean())
        pd_ = np.array(pd_)
        ax.plot(grid, pd_, color=c, label=lab)
        dif = np.diff(pd_)
        out[lab] = dict(n_down=int((dif < -1e-6).sum()), worst=float(dif.min()), range=float(pd_[-1] - pd_[0]))
    ax.set_xlabel('load of day d at the same hour (GW)')
    ax.set_ylabel('partial dependence (GW)')
    st.legend_outside_bottom(ax, ncol=2, y=-0.22)
    plt.tight_layout()
    save('ats_ch12_monotone', save_it)
    return out


# =============================================================================
# 5. RECURRENT NETWORKS: GRADIENTS THROUGH TIME
# =============================================================================
def fig_vanishing(save_it=True, T=100, seeds=5):
    """Gradients through time at initialisation: tanh RNN, GRU, LSTM with the default forget-gate bias 0, and LSTM
    with forget-gate bias 1 and 3 (Gers, Schmidhuber and Cummins 2000; Jozefowicz, Zaremba and Sutskever 2015)."""
    spec = {'rnn': ('rnn', None), 'gru': ('gru', None), 'lstm': ('lstm', None), 'lstm_b1': ('lstm', 1.0), 'lstm_b3': ('lstm', 3.0)}
    G = {k: np.mean([grad_through_time(c, T, seed=s, forget_bias=b) for s in range(seeds)], axis=0) for k, (c, b) in spec.items()}
    fig, ax = plt.subplots(figsize=(9, 3.9))
    lag = T - np.arange(1, T + 1)
    for k, c, lab in (('rnn', st.IDAred, 'tanh RNN'), ('gru', st.Forest, 'GRU'), ('lstm', st.MainBlue, 'LSTM, forget bias 0'),
                      ('lstm_b1', st.Purple, 'LSTM, forget bias 1'), ('lstm_b3', st.Amber, 'LSTM, forget bias 3')):
        ax.semilogy(lag, G[k], color=c, label=lab)
    ax.set_xlabel('lag T - t')
    ax.set_ylabel(r'mean $|\partial h_T / \partial x_t|$')
    st.legend_outside_bottom(ax, ncol=3, y=-0.22)
    plt.tight_layout()
    save('ats_ch12_vanishing', save_it)
    out = {}
    for k, g in G.items():
        r = g[::-1]                                                     # r[j]: lag j
        out[k] = dict(g1=float(r[1]), g10=float(r[10]), g50=float(r[50]), ratio50=float(r[50] / r[1]),
                      rate=float(-np.polyfit(np.arange(1, 41), np.log(r[1:41]), 1)[0]))
    out['T'], out['seeds'] = T, seeds
    return out


# =============================================================================
# 6. DEEP MODELS AGAINST HAR: S&P 500 REALISED VARIANCE
# =============================================================================
def rv_windows(y, L):
    """Rows t = L-1..n-1: X[t] = (y_{t-L+1}, ..., y_t) (oldest first)."""
    return np.lib.stride_tricks.sliding_window_view(y, L)


def har_feats(W):
    """HAR regressors from windows of 22 values (oldest first): daily, weekly and monthly means."""
    return np.column_stack([W[:, -1], W[:, -5:].mean(1), W.mean(1)])


def rv_forecasts(rv, models=('HAR', 'MLP', 'LSTM', 'TCN', 'HGB'), horizons=RV['horizons'], first=RV['first'],
                 refit=RV['refit'], seeds=(0,), epochs=60):
    """Expanding-window forecasts of RV_{t+h} (one day, h ahead) from y = log RV: HAR (OLS on the daily, weekly,
    monthly means), an MLP and an LSTM and a TCN on the last 22 values (standardised with the training mean and
    standard deviation; average of the seeds), boosting on the 22 lags. Level forecast exp(m + s^2/2), s^2 the
    training residual variance. Re-estimation every `refit` days from day `first`."""
    from sklearn.ensemble import HistGradientBoostingRegressor as HGB
    y = np.log(np.asarray(rv, float))
    L = RV['lags']
    W = rv_windows(y, L)
    tw = np.arange(L - 1, len(y))                                       # time of the last value of each window
    out = {}
    for h in horizons:
        ok = tw + h < len(y)
        Wh, th = W[ok], tw[ok]
        target = y[th + h]
        rec = {k: np.full(len(th), np.nan) for k in models}
        for o in range(first, len(y) - h, refit):
            tr = th + h <= o                                            # targets known at the origin o
            te = (th >= o) & (th < o + refit)
            if not te.any():
                continue
            mu, sd = Wh[tr].mean(), Wh[tr].std()
            Xtr, Xte, ytr = (Wh[tr] - mu) / sd, (Wh[te] - mu) / sd, (target[tr] - mu) / sd
            for k in models:
                if k == 'HAR':
                    A = har_feats(Wh[tr])
                    b = np.linalg.lstsq(np.column_stack([np.ones(len(A)), A]), target[tr], rcond=None)[0]
                    fi = np.column_stack([np.ones(len(A)), A]) @ b
                    f = np.column_stack([np.ones(te.sum()), har_feats(Wh[te])]) @ b
                    s2 = np.var(target[tr] - fi)
                elif k == 'HGB':
                    m = HGB(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=50, random_state=SEED)
                    m.fit(Xtr, ytr)
                    f = mu + sd * m.predict(Xte)
                    s2 = np.var(sd * (ytr - m.predict(Xtr)))
                elif TORCH:
                    fs, ss = [], []
                    for s in seeds:
                        net = {'MLP': lambda: MLPNet(L, 1, 32, 2), 'LSTM': lambda: RNNNet(1, 16, 'lstm'),
                               'TCN': lambda: TCNNet(1, 16, 3, 3)}[k]()
                        net = fit_torch(net, Xtr, ytr[:, None], epochs=epochs, lr=2e-3, batch=128, seed=s)
                        fs.append(mu + sd * predict_torch(net, Xte)[:, 0])
                        ss.append(np.var(sd * (ytr - predict_torch(net, Xtr)[:, 0])))
                    f, s2 = np.mean(fs, 0), np.mean(ss)
                else:
                    continue
                rec[k][te] = np.exp(f + s2 / 2)
        keep = ~np.isnan(rec[models[0]])
        out[h] = pd.DataFrame({'t': th[keep], 'rv': np.exp(target[keep]), **{k: v[keep] for k, v in rec.items()}})
    return out


def evaluate_rv(F, base='HAR'):
    """QLIKE of each model, ratio to the base, DM (HLN) statistics against the base and the MCS p-values."""
    out = {}
    for h, d in F.items():
        ms = [c for c in d.columns if c not in ('t', 'rv')]
        Lq = pd.DataFrame({k: qlike(d['rv'], d[k]) for k in ms})
        e = {'T': int(len(d)), 'qlike': {k: float(Lq[k].mean()) for k in ms}}
        e['rel'] = {k: e['qlike'][k] / e['qlike'][base] for k in ms}
        e['dm'] = {k: dm_test(Lq[k] - Lq[base], h) for k in ms if k != base}
        e['mcs'] = mcs(Lq, block=max(h, 5))['p']
        out[str(h)] = e
    return out


def fig_rv_deep(save_it=True, horizons=RV['horizons'], epochs=60):
    rv = omi('.SPX')
    F = rv_forecasts(rv, horizons=horizons, epochs=epochs)
    E = evaluate_rv(F)
    ms = ['MLP', 'LSTM', 'TCN', 'HGB']
    fig, ax = plt.subplots(figsize=(9.5, 3.9))
    w = 0.2
    cols = [st.Forest, st.MainBlue, st.Purple, st.Amber]
    for j, (k, c) in enumerate(zip(ms, cols)):
        vals = [E[str(h)]['rel'][k] for h in horizons]
        ax.bar(np.arange(len(horizons)) + (j - 1.5) * w, vals, w, color=c, label=k)
        for i, h in enumerate(horizons):
            p = E[str(h)]['dm'][k]['p_hln']
            if p < 0.05:
                ax.text(i + (j - 1.5) * w, vals[i], '*', ha='center', va='bottom', color=st.DarkText)
    ax.axhline(1, color=st.DarkText, ls=':', lw=1)
    ax.set_xticks(range(len(horizons)))
    ax.set_xticklabels([f'h = {h}' for h in horizons])
    ax.set_ylabel('QLIKE relative to HAR')
    lo = min(min(E[str(h)]['rel'][k] for k in ms) for h in horizons)
    hi = max(max(E[str(h)]['rel'][k] for k in ms) for h in horizons)
    ax.set_ylim(min(0.9, lo - 0.03), max(1.1, hi + 0.04))
    st.legend_outside_bottom(ax, ncol=4, y=-0.18)
    plt.tight_layout()
    save('ats_ch12_rv_deep', save_it)
    d = F[horizons[0]]
    ev = {}
    for h, e in E.items():
        ev[h] = dict(T=e['T'], qlike=e['qlike'], rel=e['rel'], mcs=e['mcs'],
                     dm={m: dict(t=v['hln'], p=v['p_hln']) for m, v in e['dm'].items()})
    return dict(eval=ev, n=int(len(rv)), start=str(rv.index[0].date()), end=str(rv.index[-1].date()),
                oos_start=str(rv.index[int(d['t'].iloc[0])].date()), oos_T=int(len(d)))


def seeds_snooping(rv=None, n_seeds=10, h=1, epochs=60):
    """MLP forecasts of S&P 500 RV with n_seeds random seeds: QLIKE ratio to HAR of each seed, of the seed ensemble,
    and of the seed that is best on the test period (data snooping)."""
    rv = omi('.SPX') if rv is None else rv
    Fh = rv_forecasts(rv, models=('HAR',), horizons=(h,))[h]
    ql_har = qlike(Fh['rv'], Fh['HAR'])
    rel, logs = [], []
    for s in range(n_seeds):
        F = rv_forecasts(rv, models=('MLP',), horizons=(h,), seeds=(s,), epochs=epochs)[h]
        rel.append(float(qlike(F['rv'], F['MLP']).mean() / ql_har.mean()))
        logs.append(np.log(F['MLP'].values))
    ens = np.exp(np.mean(logs, 0))
    rel_ens = float(qlike(Fh['rv'], ens).mean() / ql_har.mean())
    return dict(rel=rel, ens=rel_ens, best=float(min(rel)), worst=float(max(rel)), med=float(np.median(rel)), n=n_seeds)


def snooping_sim(K=(1, 2, 5, 10, 20, 50, 100), T=2500, reps=2000, rho=0.5, seed=SEED):
    """K forecasting models with the same expected loss; loss differentials against a benchmark are N(0, 1) per day
    with pairwise correlation rho across models. Expected 'gain' of the model that looks best on a test period of
    T days, in standard deviations of the daily differential, and the share of DM tests rejecting at 5% for it."""
    rng = np.random.default_rng(seed)
    out = {}
    for k in K:
        common = rng.normal(size=(reps, 1))
        own = rng.normal(size=(reps, k))
        mbar = (np.sqrt(rho) * common + np.sqrt(1 - rho) * own) / np.sqrt(T)   # mean differential over T days
        best = mbar.max(axis=1)
        out[k] = dict(gain=float(np.mean(best)), reject=float(np.mean(best * np.sqrt(T) > 1.96)))
    return out


def fig_snooping(save_it=True, n_seeds=10, epochs=60):
    s = seeds_snooping(n_seeds=n_seeds, epochs=epochs)
    sim = snooping_sim()
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.9))
    axs[0].scatter(np.arange(1, len(s['rel']) + 1), s['rel'], color=st.Forest, s=30, label='single seed')
    axs[0].axhline(s['ens'], color=st.MainBlue, lw=1.4, label='ensemble of the seeds')
    axs[0].axhline(1, color=st.DarkText, ls=':', lw=1)
    axs[0].set_xlabel('random seed')
    axs[0].set_ylabel('QLIKE relative to HAR, h = 1')
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.22)
    K = list(sim)
    axs[1].plot(K, [sim[k]['reject'] for k in K], 'o-', color=st.IDAred, label='DM declares the best of K better (one-sided, 2.5%)')
    axs[1].axhline(0.025, color=st.DarkText, ls=':', lw=1)
    axs[1].set_xscale('log')
    axs[1].set_xlabel('number of equally good models tried, K')
    axs[1].set_ylabel('share of rejections')
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.22)
    plt.tight_layout()
    save('ats_ch12_snooping', save_it)
    return dict(seeds=s, sim={str(k): v for k, v in sim.items()})


def fig_shap(save_it=True, n_eval=300, n_bg=100):
    """Exact Shapley values of three lag groups (last day, days 2-5, days 6-22) for boosting on the 22 lags of S&P 500
    log RV (h = 1), trained before the first forecast origin; evaluated on the forecast period."""
    from sklearn.ensemble import HistGradientBoostingRegressor as HGB
    y = np.log(omi('.SPX').values)
    W = rv_windows(y, RV['lags'])
    tw = np.arange(RV['lags'] - 1, len(y))
    ok = tw + 1 < len(y)
    W, tw = W[ok], tw[ok]
    tr = tw + 1 <= RV['first']
    m = HGB(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=50, random_state=SEED).fit(W[tr], y[tw[tr] + 1])
    rng = np.random.default_rng(SEED)
    te = np.where(~tr)[0]
    ev = rng.choice(te, n_eval, replace=False)
    bg = rng.choice(np.where(tr)[0], n_bg, replace=False)
    groups = [[21], [17, 18, 19, 20], list(range(17))]
    phi, base = shapley_groups(m.predict, W[ev], W[bg], groups)
    feat = np.column_stack([W[ev][:, g].mean(1) for g in groups])
    fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.6), sharey=True)
    names = ['last day', 'days 2-5', 'days 6-22']
    for j, (ax, c) in enumerate(zip(axs, (st.MainBlue, st.Forest, st.Amber))):
        ax.scatter(feat[:, j], phi[:, j], s=9, color=c, label=f'Shapley value, {names[j]}')
        ax.axhline(0, color=st.DarkText, lw=0.6, ls=':')
        ax.set_xlabel(f'mean log RV, {names[j]}')
        st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    axs[0].set_ylabel('contribution to log RV forecast')
    plt.tight_layout()
    save('ats_ch12_shap', save_it)
    imp = np.abs(phi).mean(0)
    # HAR coefficients estimated on the same training sample
    A = har_feats(W[tr])
    b = np.linalg.lstsq(np.column_stack([np.ones(len(A)), A]), y[tw[tr] + 1], rcond=None)[0]
    pred = m.predict(W[ev])
    return dict(share=[float(v / imp.sum()) for v in imp], base=float(base), additivity=float(np.max(np.abs(phi.sum(1) + base - pred))),
                har=[float(v) for v in b[1:]], slopes=[float(np.polyfit(feat[:, j], phi[:, j], 1)[0]) for j in range(3)],
                n_eval=n_eval, n_bg=n_bg)


# =============================================================================
# 7. TRANSFORMERS AGAINST LINEAR MODELS: THE PROTOCOL OF ZENG ET AL. (2023)
# =============================================================================
def zeng_data():
    """Romanian hourly load as one series, z-scored with the training mean and standard deviation; 7:1:2 split."""
    Y = ro_load_hourly()
    s = Y.values.ravel()
    n = len(s)
    a, b = int(ZENG['split'][0] * n), int((ZENG['split'][0] + ZENG['split'][1]) * n)
    mu, sd = s[:a].mean(), s[:a].std()
    return (s - mu) / sd, a, b, Y.index[0]


def zeng_windows(z, lo, hi, L, H, stride=1):
    """Windows whose targets lie in [lo, hi): inputs z[t-L:t], targets z[t:t+H]."""
    t = np.arange(max(lo, L), hi - H + 1, stride)
    idx = t[:, None] + np.arange(-L, 0)[None, :]
    jdx = t[:, None] + np.arange(H)[None, :]
    return z[idx], z[jdx]


def zeng_experiment(horizons=ZENG['horizons'], seeds=(0, 1, 2), epochs=20, stride=2):
    """Long-horizon forecasts on the test block: repeat the last value, seasonal naive (last week), Linear, NLinear,
    DLinear (kernel 25), the patch Transformer (patches of 24 hours) and the same Transformer with one token per hour
    (one seed, at most 8 epochs: the cost grows with the square of the number of tokens); MSE and MAE on the z-scored
    series; the networks are trained with Adam (MSE), early stopping on the validation block, seeds averaged."""
    z, a, b, _ = zeng_data()
    L = ZENG['L']
    res, keep = {}, {}
    for H in horizons:
        Xtr, Ytr = zeng_windows(z, 0, a, L, H, stride)
        Xva, Yva = zeng_windows(z, a, b, L, H, 1)
        Xte, Yte = zeng_windows(z, b, len(z), L, H, 1)
        X = np.vstack([Xtr, Xva])
        Yall = np.vstack([Ytr, Yva])
        vf = len(Xva) / len(X)
        P = {'repeat': np.repeat(Xte[:, -1:], H, 1),
             'seasonal naive': np.column_stack([Xte[:, -168 + (k % 168)] for k in range(H)])}
        for name, mk in (('Linear', lambda: LinearNet(L, H, 'linear')), ('NLinear', lambda: LinearNet(L, H, 'nlinear')),
                         ('DLinear', lambda: LinearNet(L, H, 'dlinear')), ('Transformer', lambda: PatchTransformer(L, H, 24)),
                         ('Transformer, point tokens', lambda: PatchTransformer(L, H, 1, 16, 2))):
            if not TORCH:
                continue
            fs = []
            point = 'point' in name
            for s in (seeds[:1] if point else seeds):
                net = fit_torch(mk(), X, Yall, epochs=min(epochs, 8) if point else epochs, lr=5e-3 if 'Linear' in name else 1e-3,
                                batch=128, val_frac=vf, patience=3, seed=s)
                fs.append(predict_torch(net, Xte))
                if name == 'Transformer' and H == horizons[0] and s == seeds[0]:
                    keep['net'] = net
            P[name] = np.mean(fs, 0)
        res[H] = {k: dict(mse=float(np.mean((Yte - v) ** 2)), mae=float(np.mean(np.abs(Yte - v)))) for k, v in P.items()}
        if H == horizons[0]:
            keep['Xte'], keep['Yte'], keep['P'] = Xte, Yte, P
    return res, keep


def fig_zeng(save_it=True, epochs=20, seeds=(0, 1, 2), horizons=ZENG['horizons']):
    res, keep = zeng_experiment(horizons=horizons, seeds=seeds, epochs=epochs)
    Hs = list(res)
    ms = [k for k in res[Hs[0]] if k != 'repeat']                      # 'repeat' is far off the scale (see the numbers)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0), gridspec_kw={'width_ratios': [1, 1.3]})
    cols = [st.Orange, st.Teal, st.Forest, st.MainBlue, st.IDAred, st.Purple]
    w = 0.8 / len(ms)
    for j, (k, c) in enumerate(zip(ms, cols)):
        axs[0].bar(np.arange(len(Hs)) + (j - (len(ms) - 1) / 2) * w, [res[H][k]['mse'] for H in Hs], w, color=c, label=k)
    axs[0].set_xticks(range(len(Hs)))
    axs[0].set_xticklabels([f'H = {H}' for H in Hs])
    axs[0].set_ylabel('MSE (z-scored load)')
    axs[0].set_ylim(0.15, None)
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.16)
    i = 1000
    x0, y0 = keep['Xte'][i], keep['Yte'][i]
    H = len(y0)
    axs[1].plot(np.arange(-168, 0), x0[-168:], color=st.DarkText, lw=1, label='input (last week shown)')
    axs[1].plot(np.arange(H), y0, color=st.DarkText, lw=1.6, ls='--', label='actual')
    for k, c in (('DLinear', st.MainBlue), ('Transformer', st.IDAred), ('seasonal naive', st.Orange)):
        if k in keep['P']:
            axs[1].plot(np.arange(H), keep['P'][k][i], color=c, lw=1.1, label=k)
    axs[1].set_xlabel('hours relative to the forecast origin')
    st.legend_outside_bottom(axs[1], ncol=3, y=-0.16)
    plt.tight_layout()
    save('ats_ch12_zeng', save_it)
    _MEM['zeng_keep'] = keep
    z, a, b, d0 = zeng_data()
    return dict(res={str(H): v for H, v in res.items()}, n=int(len(z)), a=int(a), b=int(b), L=ZENG['L'],
                start=str(d0.date()), test_start=str((d0 + pd.Timedelta(hours=b)).date()))


def fig_attention(save_it=True, n=1000):
    """Attention received by each input patch (average over heads, queries and test windows) against occlusion
    importance (increase of the MSE when the patch is replaced by the window mean), for the Transformer at H = 96."""
    from scipy.stats import spearmanr
    keep = _MEM.get('zeng_keep')
    if keep is None or 'net' not in keep:
        fig_zeng(save_it=False, seeds=(0,))
        keep = _MEM['zeng_keep']
    net, X, Y = keep['net'], keep['Xte'][:n], keep['Yte'][:n]
    base = np.mean((predict_torch(net, X) - Y) ** 2)
    with torch_no_grad():
        net(torch_tensor(X))
    A = net.attn.numpy().mean(axis=(0, 1))                              # attention received by each key patch
    T = net.n_tok
    occ = []
    for j in range(T):
        Z = X.copy()
        sl = slice(X.shape[1] - (T - j) * net.patch, X.shape[1] - (T - j - 1) * net.patch)
        Z[:, sl] = Z.mean(1, keepdims=True)
        occ.append(np.mean((predict_torch(net, Z) - Y) ** 2) - base)
    occ = np.array(occ)
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    x = np.arange(T) - T
    ax.bar(x - 0.2, A / A.sum(), 0.4, color=st.MainBlue, label='share of attention received')
    ax.bar(x + 0.2, np.maximum(occ, 0) / np.maximum(occ, 0).sum(), 0.4, color=st.IDAred, label='share of occlusion importance')
    ax.set_xlabel('input patch (days before the forecast origin)')
    ax.set_ylabel('share')
    st.legend_outside_bottom(ax, ncol=2, y=-0.22)
    plt.tight_layout()
    save('ats_ch12_attention', save_it)
    rho = spearmanr(A, occ)[0]
    return dict(rho=float(rho), top_att=int(T - np.argmax(A)), top_occ=int(T - np.argmax(occ)),
                share_last_att=float(A[-1] / A.sum()), share_last_occ=float(max(occ[-1], 0) / np.maximum(occ, 0).sum()),
                n_tok=int(T))


def torch_no_grad():
    import torch
    return torch.no_grad()


def torch_tensor(X):
    import torch
    return torch.as_tensor(np.asarray(X, np.float32))


# =============================================================================
# 8. N-BEATS, N-HiTS AND DeepAR ON THE M4 HOURLY SUBSET
# =============================================================================
def naive2(x, H, m):
    """Naive 2 of M4: seasonal adjustment by classical multiplicative decomposition if the lag-m autocorrelation is
    significant at 90% (|r_m| > 1.645 sqrt((1 + 2 sum_{k<m} r_k^2)/n)), then the naive forecast, then reseasonalise."""
    x = np.asarray(x, float)
    n = len(x)
    xc = x - x.mean()
    r = np.array([xc[k:] @ xc[:n - k] for k in range(m + 1)]) / (xc @ xc)
    seasonal = abs(r[m]) > 1.645 * np.sqrt((1 + 2 * np.sum(r[1:m] ** 2)) / n)
    if not seasonal:
        return np.repeat(x[-1], H)
    ma = pd.Series(x).rolling(m, center=True).mean().rolling(2, center=True).mean().shift(-1).values
    ratio = x / ma
    si = np.array([np.nanmean(ratio[k::m]) for k in range(m)])
    si = si / si.mean()
    s_all = si[np.arange(n) % m]
    adj = x / s_all
    return adj[-1] * si[np.arange(n, n + H) % m]


def m4_windows(train, L, H, per_series=60, seed=0):
    """Training windows of the global models: per_series random windows (input L, output H) from each series."""
    rng = np.random.default_rng(seed)
    X, Y = [], []
    for s in train:
        if len(s) < L + H:
            continue
        for a in rng.integers(0, len(s) - L - H + 1, per_series):
            X.append(s[a:a + L])
            Y.append(s[a + L:a + L + H])
    return np.array(X), np.array(Y)


def scaled_mae(pred, target):
    """MAE on the scale of each window's input level (the loss of the global models)."""
    return (pred - target).abs().mean()


def m4_global(train, H, L, kind, seeds=(0, 1, 2), epochs=30, per_series=60):
    """Global N-BEATS (generic, three blocks), N-HiTS (pools 8, 4, 1) or DLinear trained on windows of all series,
    each window divided by the mean absolute level of its input; ensemble = median of the seeds."""
    X, Y = m4_windows(train, L, H, per_series)
    sc = np.abs(X).mean(1, keepdims=True)
    Xs, Ys = X / sc, Y / sc
    ctx = np.array([s[-L:] for s in train])
    csc = np.abs(ctx).mean(1, keepdims=True)
    fs = []
    for s in seeds:
        net = {'N-BEATS': lambda: NBeatsNet(L, H, 256, 3, (1, 1, 1)),
               'N-HiTS': lambda: NBeatsNet(L, H, 256, 3, (8, 4, 1), (max(H // 12, 2), H // 4, H)),
               'DLinear': lambda: LinearNet(L, H, 'dlinear')}[kind]()
        perm = np.random.default_rng(s).permutation(len(Xs))
        net = fit_torch(net, Xs[perm], Ys[perm], epochs=epochs, lr=1e-3, batch=512, val_frac=0.1, patience=4, seed=s, loss='mae')
        fs.append(predict_torch(net, ctx / csc) * csc)
    return np.median(fs, 0)


def m4_official(methods=('Naive', 'sNaive', 'Naive2', 'Theta', 'MLP', 'RNN', '118', '245')):
    """Hourly sMAPE, MASE and OWA of the M4 evaluation file ('Evaluation and Ranks.xlsx', M4-methods repository):
    the benchmarks, the ML benchmarks MLP and RNN, Smyl (118, the winner) and Montero-Manso et al. (245)."""
    d = pd.read_excel(io.BytesIO(get_bytes('https://raw.githubusercontent.com/Mcompetitions/M4-methods/master/Evaluation%20and%20Ranks.xlsx')),
                      sheet_name='Point Forecasts-Frequency', header=None).iloc[2:, [0, 6, 13, 20]]
    d.columns = ['method', 'smape', 'mase', 'owa']
    d['method'] = d['method'].astype(str)
    d = d[d['method'].isin(methods)].set_index('method').astype(float)
    return {k: dict(smape=float(r.smape), mase=float(r.mase), owa=float(r.owa)) for k, r in d.iterrows()}


def m4_scores(train, test, F, m):
    """sMAPE and MASE per series and the OWA of each method against Naive 2 (M4 definitions)."""
    out = {}
    for k, f in F.items():
        out[k] = dict(smape=float(np.mean([smape(test[i], f[i]) for i in range(len(train))])),
                      mase=float(np.mean([mase(test[i], f[i], train[i], m) for i in range(len(train))])))
    for k in out:
        out[k]['owa'] = 0.5 * (out[k]['smape'] / out['Naive 2']['smape'] + out[k]['mase'] / out['Naive 2']['mase'])
    return out


def fig_m4(save_it=True, seeds=(0, 1, 2), epochs=30):
    train, test, ids = m4_hourly()
    H, m, L = M4H['H'], M4H['m'], M4H['L']
    F = {'Naive': np.array([np.repeat(s[-1], H) for s in train]),
         'seasonal naive': np.array([np.tile(s[-m:], H // m) for s in train]),
         'Naive 2': np.array([naive2(s, H, m) for s in train])}
    if TORCH:
        for k in ('DLinear', 'N-BEATS', 'N-HiTS'):
            F[k] = m4_global(train, H, L, k, seeds=seeds, epochs=epochs)
    S = m4_scores(train, test, F, m)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0), gridspec_kw={'width_ratios': [1, 1.3]})
    ks = list(F)
    cols = [st.Amber, st.Orange, st.Purple, st.Teal, st.MainBlue, st.Forest]
    axs[0].barh(range(len(ks)), [S[k]['owa'] for k in ks], color=cols[:len(ks)])
    axs[0].set_yticks(range(len(ks)))
    axs[0].set_yticklabels(ks)
    axs[0].axvline(1, color=st.DarkText, ls=':', lw=1)
    axs[0].set_xlabel('OWA (Naive 2 = 1)')
    i = 7
    axs[1].plot(np.arange(-168, 0), train[i][-168:], color=st.DarkText, lw=1, label=f'{ids[i]}, training part')
    axs[1].plot(np.arange(H), test[i], color=st.DarkText, lw=1.6, ls='--', label='actual')
    for k, c in (('seasonal naive', st.Orange), ('N-BEATS', st.MainBlue), ('N-HiTS', st.Forest)):
        if k in F:
            axs[1].plot(np.arange(H), F[k][i], color=c, lw=1.1, label=k)
    axs[1].set_xlabel('hours relative to the forecast origin')
    st.legend_outside_bottom(axs[1], ncol=3, y=-0.16)
    plt.tight_layout()
    save('ats_ch12_m4', save_it)
    _MEM['m4F'] = F
    try:
        off = m4_official()
    except Exception:                                   # the official file is optional (openpyxl, network)
        off = {}
    return dict(scores=S, official=off, n=len(train), H=H, L=L, seeds=len(seeds))


def fig_deepar(save_it=True, steps=4000, n_samples=100, checkpoints=(500, 1000, 2000)):
    """DeepAR-type Gaussian LSTM, global over the 414 M4 hourly series (lags 1, 24, 168; context 168, horizon 48);
    weighted quantile loss (deciles), 80% coverage, sMAPE of the median, also at earlier training checkpoints;
    benchmark: seasonal naive with quantiles from its one-season-ahead training errors (spread growing with the
    number of seasons ahead)."""
    train, test, ids = m4_hourly()
    H, m = M4H['H'], M4H['m']
    C, M = 168, 168
    hist = np.array([s[-(M + C):] for s in train])
    starts = np.array([len(s) - M - C for s in train])
    sn = np.array([np.tile(s[-m:], H // m) for s in train])
    Qsn = []
    for i, s in enumerate(train):
        e = s[m:] - s[:-m]
        Qsn.append(sn[i][None, :] + np.quantile(e, TAUS9)[:, None] * np.sqrt(1 + np.arange(H) // m)[None, :])

    def score(Q):
        wql = np.sum([2 * pinball(test, Q[:, j], t).sum() for j, t in enumerate(TAUS9)]) / np.abs(test).sum() / len(TAUS9)
        return dict(wql=float(wql), cov80=float(np.mean((test >= Q[:, 0]) & (test <= Q[:, -1]))),
                    smape=float(np.mean([smape(test[i], Q[i, 4]) for i in range(len(test))])))
    out = {'seasonal naive': score(np.array(Qsn))}
    Qd = None
    if TORCH:
        net = deepar_train(train, C, H, steps=steps, checkpoints=checkpoints)
        final = {k: v.clone() for k, v in net.state_dict().items()}
        out['budget'] = {}
        for c in list(checkpoints) + [steps]:
            net.load_state_dict(net.checkpoints[c] if c != steps else final)
            Q = np.quantile(deepar_sample(net, hist, starts, C, H, n_samples), TAUS9, axis=1).transpose(1, 0, 2)
            out['budget'][str(c)] = score(Q)
        out['DeepAR'] = out['budget'][str(steps)]
        Qd = Q
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    i = 7
    ax.plot(np.arange(-168, 0), train[i][-168:], color=st.DarkText, lw=1, label=f'{ids[i]}, training part')
    ax.plot(np.arange(H), test[i], color=st.DarkText, lw=1.6, ls='--', label='actual')
    if Qd is not None:
        ax.fill_between(np.arange(H), Qd[i][0], Qd[i][-1], color=st.MainBlue, alpha=0.25, label='DeepAR 10%-90%')
        ax.plot(np.arange(H), Qd[i][4], color=st.MainBlue, lw=1.2, label='DeepAR median')
    ax.plot(np.arange(H), sn[i], color=st.Orange, lw=1, label='seasonal naive')
    ax.set_xlabel('hours relative to the forecast origin')
    st.legend_outside_bottom(ax, ncol=3, y=-0.22)
    plt.tight_layout()
    save('ats_ch12_deepar', save_it)
    out['steps'], out['C'], out['samples'] = steps, C, n_samples
    return out


# =============================================================================
# 9. AI MINI-CASE: DO DEEP MODELS BEAT HAR ACROSS MARKETS?
# =============================================================================
def fig_ai_case(save_it=True, models=('MLP', 'HGB'), epochs=40, symbols=tuple(OMI_NAMES)):
    """Pre-registered grid: six indices x horizons 1, 5, 22 x two learners (MLP, boosting) against HAR, the same
    expanding design; QLIKE ratio and HLN-DM p-value of each cell."""
    rows = []
    for sym in symbols:
        name = OMI_NAMES[sym]
        F = rv_forecasts(omi(sym), models=('HAR',) + tuple(models), epochs=epochs)
        E = evaluate_rv(F)
        for h in RV['horizons']:
            for k in models:
                rows.append(dict(asset=name, h=h, model=k, rel=E[str(h)]['rel'][k], p=E[str(h)]['dm'][k]['p_hln'],
                                 t=E[str(h)]['dm'][k]['hln']))
    t = pd.DataFrame(rows)
    fig, axs = plt.subplots(1, len(models), figsize=(11.5, 3.9), sharey=True)
    for ax, k in zip(np.atleast_1d(axs), models):
        names = [OMI_NAMES[x] for x in symbols]
        M = t[t['model'] == k].pivot(index='asset', columns='h', values='rel').loc[names]
        Pv = t[t['model'] == k].pivot(index='asset', columns='h', values='p').loc[names]
        im = ax.imshow(M.values, cmap='RdBu_r', vmin=0.85, vmax=1.15, aspect='auto')
        for a in range(M.shape[0]):
            for b in range(M.shape[1]):
                ax.text(b, a, f'{M.values[a, b]:.2f}' + ('*' if Pv.values[a, b] < 0.05 else ''), ha='center', va='center',
                        fontsize=9, color='white' if abs(M.values[a, b] - 1) > 0.09 else st.DarkText)
        ax.set_xticks(range(M.shape[1]))
        ax.set_xticklabels([f'h = {h}' for h in M.columns])
        ax.set_yticks(range(M.shape[0]))
        ax.set_yticklabels(M.index)
        ax.set_title(f'{k} / HAR (QLIKE)')
    plt.colorbar(im, ax=axs, fraction=0.03, pad=0.02)
    save('ats_ch12_ai_case', save_it)
    return dict(n=int(len(t)), better=int((t['rel'] < 1).sum()), sig_better=int(((t['rel'] < 1) & (t['p'] < 0.05)).sum()),
                sig_worse=int(((t['rel'] > 1) & (t['p'] < 0.05)).sum()), rel_min=float(t['rel'].min()),
                rel_max=float(t['rel'].max()), rel_med=float(t['rel'].median()),
                by_model={k: float(t[t['model'] == k]['rel'].median()) for k in models},
                by_h={str(h): float(t[t['h'] == h]['rel'].median()) for h in RV['horizons']})


if __name__ == '__main__':
    st.apply()
    N = {}
    only = sys.argv[1:]
    path = os.path.join(HERE, 'ch12_numbers.json')
    if os.path.exists(path):
        N = json.load(open(path))
    for name, f in [('overview', fig_overview), ('cv', fig_cv_bhk), ('leakage', fig_leakage), ('global', fig_global_local),
                    ('lasso', fig_ro_lasso), ('load', fig_load_trees), ('monotone', fig_monotone), ('vanishing', fig_vanishing),
                    ('rv', fig_rv_deep), ('snooping', fig_snooping), ('shap', fig_shap), ('zeng', fig_zeng),
                    ('attention', fig_attention), ('m4', fig_m4), ('deepar', fig_deepar), ('ai', fig_ai_case)]:
        if only and name not in only:
            continue
        print(name, flush=True)
        N[name] = f()
        with open(path, 'w') as fh:
            json.dump(N, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else (list(o) if isinstance(o, tuple) else float(o)))
    print('written ch12_numbers.json')
