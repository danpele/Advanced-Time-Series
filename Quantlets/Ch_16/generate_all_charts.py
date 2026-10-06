"""
generate_all_charts.py -- charts and numbers of Chapter 16 (ATS): explosive roots and bubbles (self-study)
=========================================================================================================
Course data (ats_data.py), chart style (ats_style.py), the engine bubble_core.py. Every number on the slides comes
from here.
  * rational      a Blanchard-Watson bubble; an Evans (1991) periodically collapsing bubble on a present-value
                  fundamental: full-sample ADF against SADF, GSADF and BSADF;
  * asymptotics   explosive AR(1): the Cauchy limit of White (1958) and Anderson (1959) with Gaussian and non-Gaussian
                  errors, the invariance of the mildly explosive limit of Phillips and Magdalinos (2007), coverage of
                  the Cauchy confidence interval;
  * null          null distributions of ADF, SADF and GSADF and their critical values as the sample grows;
  * size          GSADF and date-stamping under changing volatility: Monte Carlo against wild-bootstrap critical
                  values, pointwise against family-wise thresholds (false dated episodes);
  * dating        accuracy of BSADF date-stamping in a bubble-and-collapse process: detection rate, delays;
  * monitor       CUSUM monitoring with the Chu-Stinchcombe-White boundary (Homm and Breitung 2012) against BSADF;
  * housing       US price-to-rent (S&P CoreLogic Case-Shiller, CPI rent: FRED) and Romanian price-to-rent (Eurostat
                  HPI and HICP actual rentals): explosive ratio, non-explosive fundamental;
  * episodes      S&P 500 and Nasdaq 100 (dot-com), Shanghai 2015, Bitcoin 2017 and 2021, BET 2007: PSY dating with
                  Monte Carlo and wild-bootstrap critical values, first alarms, lead times;
  * lppls         Shanghai 2015: LPPLS confidence indicator and the profile likelihood of the critical time;
  * evaluation    early-warning value of the LPPLS confidence indicator, BSADF and momentum for 20% drawdowns of the
                  S&P 500 and Bitcoin: ROC curves, AUC with block-bootstrap intervals, hit and false-alarm rates;
  * ai_case       a GSADF screen of the course data (monthly): how many "bubbles" survive multiple testing.
Output: charts/ats_ch16_*.pdf/.png, Quantlets/Ch_16/ch16_numbers.json, ch16_ci_*.csv (cached indicator series)
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_16/generate_all_charts.py [name ...]
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_style as st                                                                                  # noqa: E402
from ats_data import read_market, read_fred, read_eurostat, manifest                                                   # noqa: E402
from bubble_core import (WINDOWS, adf_window, bic_lag, alarm_table, ar1_explosive, auc, blanchard_watson,       # noqa: E402
                         block_bootstrap_auc, bsadf_paths, bubble_collapse, confidence_series, csw_constant,
                         cusum_monitor, episodes, evans_price, future_fall, lppl_conditions, lppl_fit, min_window,
                         null_paths, ols_rho, psy, psy_cv, qualified, roc, tc_profile, todate, weekly, wild_cv, yrs)

warnings.filterwarnings('ignore')
st.apply()
SEED = 2026
PROCS = int(os.environ.get('ATS_PROCS', max(1, (os.cpu_count() or 2) - 2)))
END = '2026-09-18'
# weekly samples of the PSY dating: symbol, crypto (7 days a week), first and last day, label
SAMPLES = {'sp500': ('GSPC.INDX', False, '1990-01-01', '2004-12-31', 'S&P 500, 1990-2004'),
           'ndx': ('NDX.INDX', False, '1990-01-01', '2004-12-31', 'Nasdaq 100, 1990-2004'),
           'ssec': ('SSEC.INDX', False, '2010-01-01', '2018-12-31', 'Shanghai Composite, 2010-2018'),
           'btc': ('BTC-USD.CC', True, '2014-09-17', '2023-12-31', 'Bitcoin, 2014-2023'),
           'bet': ('BET', False, '2000-01-01', '2012-12-31', 'BET, 2000-2012')}
PEAKS = {'sp500': [('1999-06-01', '2000-12-31')], 'ndx': [('1999-06-01', '2000-12-31')],
         'ssec': [('2015-01-01', '2015-12-31')], 'btc': [('2017-06-01', '2018-03-31'), ('2021-01-01', '2021-06-30')],
         'bet': [('2007-01-01', '2007-12-31')]}
COLORS = {'sp500': st.MainBlue, 'ndx': st.Teal, 'ssec': st.Orange, 'btc': st.Amber, 'bet': st.Crimson}
SHADE = '#DCE6F2'                 # light blue band of a dated episode
CRASH, HORIZON = 0.20, 182        # an event: a fall of at least 20% within 182 calendar days
RO_END = '2026-03-31'             # the HICP rent index of Romania rises by 33% in April 2026 (one month): sample ends before
TAU = 52                          # family-wise window: one year of weekly end points
_MEM = {}
CSV_RAW = 'https://raw.githubusercontent.com/danpele/Advanced-Time-Series/main/Quantlets/Ch_16/'


def read_cached(name):
    """A cached indicator series of the chapter: local copy (Quantlets/Ch_16) or the ATS repository on GitHub."""
    for p in (os.path.join(HERE, name), CSV_RAW + name):
        try:
            return pd.read_csv(p, index_col=0, parse_dates=True)
        except Exception:
            pass
    return None


def save(name, save_it=True):
    st.check_no_grey(plt.gcf())
    if save_it:
        st.save_fig(name)
    else:
        plt.show()
        plt.close()


def d2s(d):
    return pd.Timestamp(d).strftime('%Y-%m-%d')


def prices(symbol, crypto=False, field='close'):
    """Daily close with the course conventions (weekdays only and no holiday-filled closes, except crypto)."""
    t = read_market(symbol)
    s = pd.to_numeric(t[field] if field in t.columns else t['close'], errors='coerce').dropna()
    s = s[s > 0].loc[:END]
    if not crypto:
        s = s[s.index.dayofweek < 5]
        s = s[s.diff() != 0]
    return s.rename(symbol)


def min_len(T):
    """Minimum duration of a dated episode: ceil(ln T) end points."""
    return int(np.ceil(np.log(T)))


def _pool(func, jobs):
    if PROCS == 1 or len(jobs) == 1:
        return [func(j) for j in jobs]
    from multiprocessing import get_context
    with get_context('fork').Pool(min(PROCS, len(jobs))) as pool:
        return pool.map(func, jobs, chunksize=1)


# =============================================================================
# 1. RATIONAL BUBBLES
# =============================================================================
def fig_rational(save_it=True, R=2000):
    """Blanchard-Watson bubble; Evans bubble on a present-value fundamental with BSADF against its 95% critical value."""
    T = 400
    rng = np.random.default_rng(SEED)
    fund = 20 + np.cumsum(0.3 * rng.standard_normal(T))
    b = blanchard_watson(T)
    pf, B = evans_price(T)
    p = pf + B
    o = psy(p)
    cv = psy_cv(o['n'], o['w0'], R=R, seed=SEED)
    L = min_len(o['n'])
    ep = episodes(o['bsadf'], cv['bsadf95'], np.arange(1, o['n'] + 1), L)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    axes[0].plot(fund + b, color=st.IDAred, label='Blanchard-Watson: fundamental + bubble')
    axes[0].plot(fund, color=st.MainBlue, label='fundamental value')
    axes[0].set_title('Blanchard-Watson bubble')
    axes[1].plot(p, color=st.IDAred, label='Evans: fundamental + bubble')
    axes[1].plot(pf, color=st.MainBlue, label='_fundamental')
    axes[1].set_title('Evans (1991) bubble')
    axes[2].plot(np.arange(1, o['n'] + 1), o['bsadf'], color=st.MainBlue, label='BSADF of the Evans price')
    axes[2].plot(np.arange(1, o['n'] + 1), cv['bsadf95'], color=st.IDAred, ls='--', label='95% critical value')
    for a_, b_, _ in ep:
        for ax in axes[1:]:
            ax.axvspan(a_, b_, color=st.Orange, alpha=0.18, lw=0)
    axes[2].set_title('Date-stamping the Evans bubble')
    for ax in axes:
        ax.set_xlabel('period')
    axes[0].set_ylabel('price')
    st.fig_legend_bottom(fig, ncol=5, y=0.02)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch16_rational', save_it)
    bursts = int(np.sum((B[1:] < 0.6 * 20) & (B[:-1] > 1.0 * 20)))
    return dict(T=o['n'], w0=o['w0'], r0=o['r0'], adf=o['adf'], sadf=o['sadf'], gsadf=o['gsadf'],
                cv={k: cv[k] for k in ('adf', 'sadf', 'gsadf')}, n_ep=len(ep), episodes=[(int(a), int(b_), int(n)) for a, b_, n in ep],
                L=L, collapses=bursts, bw_dur=1 / (1 - 0.98), R=R)


# =============================================================================
# 2. EXPLOSIVE AUTOREGRESSIONS: CAUCHY LIMITS
# =============================================================================
def fig_asymptotics(save_it=True, R=20000, n=200, n_fixed=30, n_big=2000):
    """Normalised OLS error rho^n/(rho^2 - 1) (rho_hat - rho) for a mildly explosive root rho = 1 + 1/n^0.7 (n = 200)
    and a fixed explosive root rho = 2 (n = 30), Gaussian and centred exponential errors, against the standard Cauchy
    law; coverage of the 95% Cauchy interval rho_hat +- (rho_hat^2 - 1)/rho_hat^n tan(0.475 pi); the mildly explosive
    case again with n = 2000."""
    rng = np.random.default_rng(SEED)
    cases = {'mild': (1 + 1 / n ** 0.7, n), 'fixed': (2.0, n_fixed), 'mild_big': (1 + 1 / n_big ** 0.7, n_big)}
    q975 = np.tan(np.pi * 0.475)
    out, Z = {}, {}
    for k, (rho, nn) in cases.items():
        for dist in ('normal', 'exp'):
            y = ar1_explosive(nn, rho, R if nn <= 200 else R // 4, rng, dist)
            rh = ols_rho(y)
            z = rho ** nn / (rho ** 2 - 1) * (rh - rho)
            half = (rh ** 2 - 1) / rh ** nn * q975
            Z[(k, dist)] = z
            ks = stats.kstest(z, 'cauchy')
            out[f'{k}_{dist}'] = dict(rho=rho, n=nn, ks=float(ks.statistic), ks_p=float(ks.pvalue),
                                      cover=float(np.mean(np.abs(rh - rho) <= half)),
                                      q90=float(np.quantile(np.abs(z), 0.9)))
    out['q90_cauchy'] = float(np.tan(np.pi * 0.45))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
    x = np.linspace(-6, 6, 400)
    bins = np.linspace(-6, 6, 61)
    for ax, k, title in ((axes[0], 'mild', f'mildly explosive: rho = 1 + 1/n^0.7 = {cases["mild"][0]:.4f}, n = {n}'),
                         (axes[1], 'fixed', f'fixed explosive: rho = 2, n = {n_fixed}')):
        ax.hist(np.clip(Z[(k, 'normal')], -6, 6), bins=bins, density=True, histtype='step', color=st.MainBlue, lw=1.6,
                label='Gaussian errors' if k == 'mild' else '_')
        ax.hist(np.clip(Z[(k, 'exp')], -6, 6), bins=bins, density=True, histtype='step', color=st.Orange, lw=1.6,
                label='centred exponential errors' if k == 'mild' else '_')
        ax.plot(x, stats.cauchy.pdf(x), color=st.IDAred, ls='--', label='standard Cauchy' if k == 'mild' else '_')
        ax.set_title(title)
        ax.set_xlabel('rho^n / (rho^2 - 1) (rho_hat - rho)')
    axes[0].set_ylabel('density')
    st.fig_legend_bottom(fig, ncol=3, y=0.02)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch16_asymptotics', save_it)
    out.update(R=R, k=float(n ** 0.7))
    return out


def fig_null(save_it=True, Ts=(100, 200, 400, 800), R=2000):
    """Null distributions of ADF, SADF and GSADF (T = 400) and the 95% critical values against T."""
    res = {}
    draws = None
    for T in Ts:
        w0, r0 = min_window(T)
        cv = psy_cv(T, w0, R=R if T <= 400 else R // 2, seed=SEED + T)
        res[str(T)] = dict(w0=w0, r0=r0, adf=cv['adf'], sadf=cv['sadf'], gsadf=cv['gsadf'],
                           bsadf_end=float(cv['bsadf95'][-1]), windows=int((T - w0 + 1) * (T - w0 + 2) / 2))
        if T == 400:
            draws = cv['draws']
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    bins = np.linspace(-4.5, 4.5, 70)
    for k, c, lab in (('adf', st.MainBlue, 'ADF (whole sample)'), ('sadf', st.Forest, 'SADF'), ('gsadf', st.IDAred, 'GSADF')):
        axes[0].hist(draws[k], bins=bins, density=True, histtype='step', lw=1.6, color=c, label=lab)
        axes[0].axvline(res['400'][k]['95'], color=c, ls='--', lw=0.9, label='_')
    axes[0].axvline(stats.norm.ppf(0.95), color=st.DarkText, ls=':', lw=0.9, label='1.645 (normal 95% quantile)')
    axes[0].set_title('Null distributions, T = 400 (dashed: 95% quantiles)')
    axes[0].set_xlabel('statistic')
    axes[0].set_ylabel('density')
    for k, c, lab in (('adf', st.MainBlue, '_'), ('sadf', st.Forest, '_'), ('gsadf', st.IDAred, '_')):
        axes[1].plot(Ts, [res[str(T)][k]['95'] for T in Ts], 'o-', color=c, label=lab)
    axes[1].plot(Ts, [res[str(T)]['bsadf_end'] for T in Ts], 's--', color=st.Purple, label='BSADF at the last date (pointwise)')
    axes[1].set_xscale('log')
    axes[1].set_xticks(Ts)
    axes[1].set_xticklabels([str(T) for T in Ts])
    axes[1].xaxis.set_minor_formatter(plt.NullFormatter())
    axes[1].set_xlabel('sample size T (minimum window r0 = 0.01 + 1.8/sqrt(T))')
    axes[1].set_ylabel('95% critical value')
    axes[1].set_title('Critical values against T')
    st.fig_legend_bottom(fig, ncol=5, y=0.02)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch16_null', save_it)
    return res


# =============================================================================
# 3. SIZE UNDER CHANGING VOLATILITY; POINTWISE AND FAMILY-WISE DATING
# =============================================================================
def vol_path(kind, T):
    """Volatility path of the null model: constant, a rise or a fall at T/2 (GARCH paths are drawn in _size_job)."""
    if kind == 'up':
        return np.r_[np.ones(T // 2), 3 * np.ones(T - T // 2)]
    if kind == 'down':
        return np.r_[np.ones(T // 2), np.ones(T - T // 2) / 3]
    return np.ones(T)


def _size_job(args):
    kind, T, w0, seeds, B, mc = args
    out = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        if kind == 'garch':
            om, a, b = 0.02, 0.10, 0.88
            h, e = np.empty(T), rng.standard_normal(T)
            h[0] = om / (1 - a - b)
            for t in range(1, T):
                h[t] = om + a * h[t - 1] * e[t - 1] ** 2 + b * h[t - 1]
            y = np.r_[0, np.cumsum(1.0 / T + np.sqrt(h) * e)]
        else:
            y = null_paths(T, 1, rng, vol_path(kind, T))[0]
        o = psy(y, w0=w0)
        wb = wild_cv(y, w0, B=B, seed=sd + 1)
        L = min_len(T)
        idx = np.arange(1, T + 1)
        out.append(dict(rej_mc=o['gsadf'] > mc['gsadf95'], rej_wild=o['gsadf'] > wb['gsadf95'],
                        ep_mc=len(episodes(o['bsadf'], mc['bsadf95'], idx, L)) > 0,
                        ep_wild=len(episodes(o['bsadf'], wb['bsadf95'], idx, L)) > 0,
                        ep_fw=len(episodes(o['bsadf'], wb['gsadf95'], idx, L)) > 0))
    return kind, out


def fig_size(save_it=True, T=200, N=400, B=199, Rmc=4000):
    """Rejection rates under the null for four volatility patterns: GSADF with Monte Carlo and wild-bootstrap critical
    values; share of paths with at least one dated episode (pointwise Monte Carlo, pointwise wild, family-wise wild)."""
    w0, r0 = min_window(T)
    cv = psy_cv(T, w0, R=Rmc, seed=SEED)
    mc = dict(gsadf95=cv['gsadf']['95'], bsadf95=cv['bsadf95'])
    kinds = ['iid', 'up', 'down', 'garch']
    jobs = []
    for i, k in enumerate(kinds):
        seeds = [SEED * 10 + 100000 * i + j for j in range(N)]
        jobs += [(k, T, w0, seeds[j::8], B, mc) for j in range(8)]
    res = {k: [] for k in kinds}
    for k, o in _pool(_size_job, jobs):
        res[k] += o
    rates = {k: {m: float(np.mean([r[m] for r in v])) for m in ('rej_mc', 'rej_wild', 'ep_mc', 'ep_wild', 'ep_fw')}
             for k, v in res.items()}
    fig, ax = plt.subplots(figsize=(12, 4.4))
    labs = {'iid': 'constant volatility', 'up': 'volatility x3 at T/2', 'down': 'volatility x1/3 at T/2',
            'garch': 'GARCH(1,1), a = 0.10, b = 0.88'}
    meas = [('rej_mc', 'GSADF, Monte Carlo critical value', st.MainBlue), ('rej_wild', 'GSADF, wild bootstrap', st.Forest),
            ('ep_mc', 'any dated episode: pointwise Monte Carlo', st.IDAred),
            ('ep_wild', 'any dated episode: pointwise wild', st.Orange),
            ('ep_fw', 'any dated episode: family-wise wild', st.Purple)]
    x = np.arange(len(kinds))
    for j, (m, lab, c) in enumerate(meas):
        ax.bar(x + (j - 2) * 0.16, [100 * rates[k][m] for k in kinds], width=0.15, color=c, label=lab)
    ax.axhline(5, color=st.DarkText, ls='--', lw=0.9, label='nominal 5%')
    ax.set_xticks(x)
    ax.set_xticklabels([labs[k] for k in kinds])
    ax.set_ylabel('rejection rate under the null (%)')
    st.legend_outside_bottom(ax, ncol=3, y=-0.12)
    save('ats_ch16_size', save_it)
    return dict(T=T, N=N, B=B, w0=w0, L=min_len(T), Rmc=Rmc, rates=rates)


# =============================================================================
# 4. DATE-STAMPING ACCURACY
# =============================================================================
def _dating_job(args):
    rho, T, te, tf, w0, cvb, seeds = args
    L = min_len(T)
    out = []
    for sd in seeds:
        y = bubble_collapse(T, te, tf, rho, y0=100.0, sd=1.0, rng=np.random.default_rng(sd))
        o = psy(y, w0=w0)
        ep = episodes(o['bsadf'], cvb, np.arange(1, T + 1), L)
        hit = [e for e in ep if e[1] >= te + 1 and e[0] <= tf + L]
        false_before = any(e[0] < te + 1 - 0 and e[1] < te + 1 for e in ep)
        if hit:
            e = hit[0]
            out.append(dict(det=True, start=e[0] - (te + 1), end=e[1] - tf, conf=e[0] + L - 1 - (te + 1), fb=false_before))
        else:
            out.append(dict(det=False, start=np.nan, end=np.nan, conf=np.nan, fb=false_before))
    return rho, out


def fig_dating(save_it=True, T=400, N=1000, rhos=(1.005, 1.01, 1.02), R=2000):
    """Bubble-and-collapse paths: random walk from y_0 = 100, explosive on (0.5T, 0.65T], collapse, random walk.
    BSADF dating with the pointwise 95% Monte Carlo critical values and a minimum duration of ceil(ln T)."""
    w0, r0 = min_window(T)
    cvb = psy_cv(T, w0, R=R, seed=SEED)['bsadf95']
    te, tf = int(0.5 * T), int(0.65 * T)
    jobs = []
    for rho in rhos:
        seeds = [SEED + 7919 * j + int(1e5 * rho) for j in range(N)]
        jobs += [(rho, T, te, tf, w0, cvb, seeds[j::8]) for j in range(8)]
    res = {r: [] for r in rhos}
    for r, o in _pool(_dating_job, jobs):
        res[r] += o
    out = {}
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    ex = bubble_collapse(T, te, tf, rhos[1], rng=np.random.default_rng(SEED))
    axes[0].plot(np.arange(T + 1), ex, color=st.MainBlue, label=f'one path, rho = {rhos[1]}')
    axes[0].axvspan(te, tf, color=st.Orange, alpha=0.18, lw=0, label='true explosive phase')
    axes[0].set_xlabel('period')
    axes[0].set_ylabel('y_t')
    axes[0].set_title('Bubble-and-collapse process, T = 400')
    bins = np.arange(-10, 61, 2)
    for rho, c in zip(rhos, (st.Forest, st.IDAred, st.Purple)):
        d = pd.DataFrame(res[rho])
        st_ = d['start'].dropna()
        axes[1].hist(st_, bins=bins, histtype='step', lw=1.6, color=c, density=True, label=f'rho = {rho}')
        out[str(rho)] = dict(det=float(d['det'].mean()), med_start=float(st_.median()) if len(st_) else np.nan,
                             q25=float(st_.quantile(0.25)) if len(st_) else np.nan,
                             q75=float(st_.quantile(0.75)) if len(st_) else np.nan,
                             med_conf=float(d['conf'].dropna().median()) if len(st_) else np.nan,
                             med_end=float(d['end'].dropna().median()) if len(st_) else np.nan,
                             false_before=float(d['fb'].mean()), growth=float(rho ** (tf - te)))
    axes[1].axvline(0, color=st.DarkText, ls=':', lw=0.9, label='_')
    axes[1].set_xlabel('estimated start minus true start (periods)')
    axes[1].set_ylabel('density')
    axes[1].set_title('Origination delay of the dated episode')
    st.fig_legend_bottom(fig, ncol=5, y=0.02)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch16_dating', save_it)
    out.update(T=T, N=N, te=te, tf=tf, dur=tf - te, w0=w0, L=min_len(T))
    return out


# =============================================================================
# 5. REAL-TIME MONITORING
# =============================================================================
def fig_monitor(save_it=True, R=1000, Nsize=2000):
    """CUSUM monitoring of weekly returns with the Chu-Stinchcombe-White boundary (training: 1990-1994 for the Nasdaq
    100, 2014-09 to 2016-06 for Bitcoin) against the first real-time BSADF alarm; size of the monitor under i.i.d.
    and GARCH returns."""
    out = {}
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    for ax, key, tr_end in ((axes[0], 'ndx', '1994-12-31'), (axes[1], 'btc', '2016-06-30')):
        sym, crypto, a, b, lab = SAMPLES[key]
        y = weekly(prices(sym, crypto)).loc[a:b]
        r = np.diff(y.values)
        idx = y.index[1:]
        n = int((idx <= pd.Timestamp(tr_end)).sum())
        S, bd, hit = cusum_monitor(r, n)
        o = psy(y.values)
        cvb = psy_cv(o['n'], o['w0'], R=R, seed=SEED)['bsadf95']
        L = min_len(o['n'])
        ep = [e for e in episodes(o['bsadf'], cvb, idx, L) if e[0] > pd.Timestamp(tr_end)]
        conf = idx[list(idx).index(ep[0][0]) + L - 1] if ep else None
        ax.plot(idx[n:], S, color=st.MainBlue, label='CUSUM of returns (scaled)')
        ax.plot(idx[n:], bd, color=st.IDAred, ls='--', label='5% boundary')
        if hit is not None:
            ax.axvline(idx[hit], color=st.Forest, lw=1.2, label='first CUSUM alarm')
        if conf is not None:
            ax.axvline(conf, color=st.Purple, lw=1.2, ls='-.', label='first confirmed BSADF alarm')
        ax.set_title(lab.split(',')[0] + ', weekly; monitoring after ' + tr_end[:7])
        ax.tick_params(axis='x', labelrotation=30)
        out[key] = dict(train_end=tr_end, n=n, cusum_alarm=d2s(idx[hit]) if hit is not None else None,
                        bsadf_start=d2s(ep[0][0]) if ep else None, bsadf_conf=d2s(conf) if conf is not None else None,
                        peak=d2s(np.exp(y).idxmax()))
    handles, labels = [], []
    for ax in axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l not in labels:
                handles.append(h)
                labels.append(l)
    st.fig_legend_bottom(fig, handles, labels, ncol=4, y=0.02)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch16_monitor', save_it)
    # size of the monitor: training n = 100, monitoring up to 5n
    rng = np.random.default_rng(SEED)
    n0, H = 100, 500
    hits = {'iid': 0, 'garch': 0}
    for _ in range(Nsize):
        e = rng.standard_normal(H)
        hits['iid'] += cusum_monitor(e, n0)[2] is not None
        om, a, b = 0.02, 0.10, 0.88
        h, z = np.empty(H), rng.standard_normal(H)
        h[0] = om / (1 - a - b)
        for t in range(1, H):
            h[t] = om + a * h[t - 1] * z[t - 1] ** 2 + b * h[t - 1]
        hits['garch'] += cusum_monitor(np.sqrt(h) * z, n0)[2] is not None
    out['size'] = {k: v / Nsize for k, v in hits.items()}
    out['a'] = csw_constant(0.05)
    out['Nsize'] = Nsize
    return out


# =============================================================================
# 6. FUNDAMENTALS AGAINST PRICES: HOUSING
# =============================================================================
def ro_housing():
    """Romanian house price index (Eurostat prc_hpi_q, 2015 = 100) over the quarterly mean of the HICP actual rentals
    index (prc_hicp_minr, CP041) and over the HICP all-items index."""
    hpi = read_eurostat('prc_hpi_q', 'Q.TOTAL.I15_Q.RO')
    rent = read_eurostat('prc_hicp_minr', 'M.I15.CP041.RO')
    cpi = read_eurostat('prc_hicp_minr', 'M.I15.TOTAL.RO')
    q = lambda s: s.groupby(s.index.to_period('Q')).mean()   # noqa: E731
    rq, cq = q(rent), q(cpi)
    hpi.index = hpi.index.to_period('Q')
    df = pd.concat([hpi.rename('hpi'), rq.rename('rent'), cq.rename('cpi')], axis=1).dropna()
    df.index = df.index.to_timestamp()
    return df.loc[:RO_END]


def us_housing():
    """S&P CoreLogic Case-Shiller US national index (SA), CPI rent of primary residence (SA) and CPI (FRED)."""
    df = read_fred(['CSUSHPISA', 'CUSR0000SEHA', 'CPIAUCSL']).dropna()
    df.columns = ['hpi', 'rent', 'cpi']
    return df


def _dating(y, B=499, tau=None, seed=SEED, kmax=0):
    """PSY with k lagged differences (k by BIC up to kmax) and wild-bootstrap critical values under the AR(k) null."""
    k = bic_lag(y, kmax) if kmax else 0
    o = psy(y, k=k)
    wb = wild_cv(y, o['w0'], B=B, seed=seed, tau=tau, k=k)
    return o, wb


def fig_housing(save_it=True, B=999):
    """BSADF of the log price-to-rent ratio and of the log real rent, US (monthly) and Romania (quarterly), with
    pointwise wild-bootstrap critical values."""
    us, ro = us_housing(), ro_housing()
    series = {'us_ratio': np.log(us['hpi'] / us['rent']), 'us_rent': np.log(us['rent'] / us['cpi']),
              'us_price': np.log(us['hpi'] / us['cpi']),
              'ro_ratio': np.log(ro['hpi'] / ro['rent']), 'ro_rent': np.log(ro['rent'] / ro['cpi']),
              'ro_price': np.log(ro['hpi'] / ro['cpi'])}
    out, dat = {}, {}
    for k, s in series.items():
        o, wb = _dating(s.values, B=B, kmax=6 if k.startswith('us') else 4)
        L = min_len(o['n'])
        ep = episodes(o['bsadf'], wb['bsadf95'], s.index[1:], L)
        dat[k] = (s, o, wb, ep)
        out[k] = dict(T=o['n'], w0=o['w0'], k=o['k'], gsadf=o['gsadf'], cv=wb['gsadf95'], L=L, first=d2s(s.index[0]),
                      last=d2s(s.index[-1]), episodes=[(d2s(a), d2s(b), n) for a, b, n in ep],
                      peak=d2s(s.idxmax()), max=float(np.exp(s.max() - s.iloc[0])))
    fig, axes = plt.subplots(2, 2, figsize=(13, 6.4), gridspec_kw=dict(height_ratios=[1, 1]))
    for j, (cty, title) in enumerate((('us', 'United States, monthly'), ('ro', 'Romania, quarterly'))):
        s, o, wb, ep = dat[f'{cty}_ratio']
        s2 = dat[f'{cty}_rent'][0]
        axes[0, j].plot(s.index, 100 * np.exp(s - s.iloc[0]), color=st.MainBlue, label='price-to-rent ratio (start = 100)')
        axes[0, j].plot(s2.index, 100 * np.exp(s2 - s2.iloc[0]), color=st.Forest, label='real rent (start = 100)')
        axes[0, j].set_title(title)
        axes[1, j].plot(s.index[1:], o['bsadf'], color=st.MainBlue, label='BSADF, price-to-rent')
        axes[1, j].plot(s.index[1:], wb['bsadf95'], color=st.IDAred, ls='--', label='95% wild-bootstrap critical value')
        o2, wb2 = dat[f'{cty}_rent'][1], dat[f'{cty}_rent'][2]
        axes[1, j].plot(s2.index[1:], o2['bsadf'], color=st.Forest, lw=1.0, label='BSADF, real rent')
        for a, b, _ in ep:
            for ax in axes[:, j]:
                ax.axvspan(a, b, color=SHADE, lw=0, zorder=0)
    axes[1, 0].set_ylabel('BSADF')
    h, l = [], []
    for ax in axes.ravel():
        for hh, ll in zip(*ax.get_legend_handles_labels()):
            if ll not in l:
                h.append(hh)
                l.append(ll)
    h.append(plt.Rectangle((0, 0), 1, 1, color=SHADE))
    l.append('explosive episode of the price-to-rent ratio')
    st.fig_legend_bottom(fig, h, l, ncol=3, y=0.02)
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    save('ats_ch16_housing', save_it)
    out['B'] = B
    return out


# =============================================================================
# 7. EPISODES: S&P 500, NASDAQ 100, SHANGHAI, BITCOIN, BET
# =============================================================================
def _episode_job(key, R=1000, B=499):
    sym, crypto, a, b, lab = SAMPLES[key]
    p = prices(sym, crypto)
    y = weekly(p).loc[a:b]
    o = psy(y.values)
    mc = psy_cv(o['n'], o['w0'], R=R, seed=SEED)
    wb = wild_cv(y.values, o['w0'], B=B, seed=SEED, tau=TAU)
    return key, y, o, mc, wb


def run_episodes(R=1000, B=499):
    """PSY statistics, Monte Carlo and wild-bootstrap critical values of the five weekly samples (one process each)."""
    if 'episodes' not in _MEM:
        if PROCS == 1:
            res = [_episode_job(k, R, B) for k in SAMPLES]
        else:
            from multiprocessing import get_context
            with get_context('fork').Pool(len(SAMPLES)) as pool:
                res = pool.starmap(_episode_job, [(k, R, B) for k in SAMPLES])
        _MEM['episodes'] = {k: v for k, *v in res}
    return _MEM['episodes']


def fig_episodes(save_it=True, R=1000, B=499):
    """Weekly log prices: BSADF against the pointwise Monte Carlo and wild-bootstrap 95% critical values; episodes dated
    with the wild bootstrap; for each peak the first alarm, the confirmation date and the fall in the next year."""
    E = run_episodes(R, B)
    out = {}
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 6.6))
    for ax, key in zip(axes.ravel(), SAMPLES):
        y, o, mc, wb = E[key]
        idx = y.index[1:]
        L = min_len(o['n'])
        ep_mc = episodes(o['bsadf'], mc['bsadf95'], idx, L)
        ep_w = episodes(o['bsadf'], wb['bsadf95'], idx, L)
        ep_fw = episodes(o['bsadf'], wb['fwer95'], idx, L)
        ax.plot(idx, o['bsadf'], color=COLORS[key], lw=1.1, label='_BSADF')
        ax.plot(idx, mc['bsadf95'], color=st.IDAred, ls='--', lw=0.9, label='pointwise 95%, Monte Carlo')
        ax.plot(idx, wb['bsadf95'], color=st.Forest, ls='--', lw=0.9, label='pointwise 95%, wild bootstrap')
        ax.plot(idx, wb['fwer95'], color=st.Purple, ls=':', lw=1.0, label='family-wise 95% over 52 weeks, wild')
        for a, b, _ in ep_w:
            ax.axvspan(a, b, color=SHADE, lw=0, zorder=0)
        px = np.exp(y)
        peaks = []
        for pa, pb in PEAKS[key]:
            pk = px.loc[pa:pb].idxmax()
            ax.axvline(pk, color=st.DarkText, ls=':', lw=0.8)
            after = px.loc[pk:pk + pd.Timedelta(days=365)]
            win = (pk - pd.Timedelta(weeks=104), pk)

            def first_conf(eps):
                c = [idx[list(idx).index(e[0]) + L - 1] for e in eps]
                c = [x for x in c if win[0] <= x <= win[1]]
                return c[0] if c else None

            def active(eps):
                return any(e[0] <= pk + pd.Timedelta(weeks=4) and e[1] >= pk - pd.Timedelta(weeks=4) for e in eps)
            cw, cf = first_conf(ep_w), first_conf(ep_fw)
            peaks.append(dict(peak=d2s(pk), conf=d2s(cw) if cw is not None else None,
                              lead=int((pk - cw).days // 7) if cw is not None else None, active=active(ep_w),
                              fw_conf=d2s(cf) if cf is not None else None,
                              fw_lead=int((pk - cf).days // 7) if cf is not None else None, fw_active=active(ep_fw),
                              fall=float(after.min() / px[pk] - 1)))
        ax.set_title(SAMPLES[key][4])
        ax.tick_params(axis='x', labelrotation=30)
        out[key] = dict(T=o['n'], w0=o['w0'], L=L, gsadf=o['gsadf'], sadf=o['sadf'], adf=o['adf'],
                        cv_mc=mc['gsadf']['95'], cv_wild=wb['gsadf95'], fwer_end=float(wb['fwer95'][-1]),
                        n_mc=len(ep_mc), n_wild=len(ep_w), n_fw=len(ep_fw), weeks_mc=int(sum(e[2] for e in ep_mc)),
                        weeks_wild=int(sum(e[2] for e in ep_w)), peaks=peaks,
                        ep_wild=[(d2s(a), d2s(b), n) for a, b, n in ep_w], ep_fw=[(d2s(a), d2s(b), n) for a, b, n in ep_fw])
    ax = axes.ravel()[-1]
    ax.axis('off')
    h = [plt.Line2D([], [], color=st.MainBlue, lw=1.1), plt.Line2D([], [], color=st.IDAred, ls='--'),
         plt.Line2D([], [], color=st.Forest, ls='--'), plt.Line2D([], [], color=st.Purple, ls=':'),
         plt.Rectangle((0, 0), 1, 1, color=SHADE), plt.Line2D([], [], color=st.DarkText, ls=':')]
    ax.legend(h, ['BSADF (colour of the series)', 'pointwise 95%, Monte Carlo', 'pointwise 95%, wild bootstrap',
                  'family-wise 95% over 52 weeks, wild', 'episode dated with the wild bootstrap', 'price peak'],
              loc='center', frameon=False)
    fig.tight_layout()
    save('ats_ch16_episodes', save_it)
    out['R'], out['B'] = R, B
    return out


# =============================================================================
# 8. LPPLS: SHANGHAI 2015
# =============================================================================
def fig_lppls(save_it=True):
    """Shanghai Composite: LPPLS confidence indicator from June 2014 to September 2015; profile likelihood of the
    critical time for the window from the March 2014 low to 29 May 2015."""
    s = prices('SSEC.INDX')
    path = os.path.join(HERE, 'ch16_ci_ssec.csv')
    ci = read_cached('ch16_ci_ssec.csv')
    if ci is None:
        ci = confidence_series(s.loc[:'2015-09-30'], '2014-06-01', step=5, procs=PROCS)
        ci.to_csv(path, float_format='%.4f')
    low = s.loc['2014-03-01':'2014-07-31'].idxmin()
    peak = s.loc['2015-01-01':'2015-12-31'].idxmax()
    t2 = pd.Timestamp('2015-05-29')
    x = s.loc[low:t2]
    t, y = yrs(x.index), np.log(x.values)
    f = lppl_fit(t, y)
    c = lppl_conditions(f)
    tcs = np.linspace(t[-1] + 2 / 365.25, t[-1] + 0.5, 90)
    prof = tc_profile(t, y, tcs)
    lr = 2 * (np.nanmax(prof) - prof)
    inside = tcs[lr <= stats.chi2.ppf(0.95, 1)]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    z = s.loc['2014-01-01':'2015-12-31']
    axes[0].plot(z.index, z.values, color=st.Purple, label='Shanghai Composite')
    axes[0].set_yscale('log')
    axes[0].yaxis.set_major_formatter(plt.ScalarFormatter())
    axes[0].yaxis.set_minor_formatter(plt.NullFormatter())
    axes[0].set_yticks([2000, 3000, 4000, 5000])
    ax2 = axes[0].twinx()
    ax2.fill_between(ci.index, 0, ci['ci'], color=st.IDAred, alpha=0.35, lw=0, label='LPPLS confidence indicator')
    ax2.set_ylim(0, 1)
    ax2.set_ylabel('confidence indicator')
    ax2.spines['right'].set_visible(True)
    axes[0].axvline(peak, color=st.DarkText, ls=':', lw=0.9, label='peak')
    axes[0].set_title('Price and confidence indicator')
    axes[0].tick_params(axis='x', labelrotation=30)
    days = (tcs - t[-1]) * 365.25
    axes[1].plot(days, lr, color=st.MainBlue, label='profile likelihood-ratio statistic of tc')
    axes[1].axhline(stats.chi2.ppf(0.95, 1), color=st.IDAred, ls='--', label='chi-square(1) 95% quantile')
    axes[1].axvline((yrs([peak])[0] - t[-1]) * 365.25, color=st.DarkText, ls=':', label='actual peak')
    axes[1].set_xlabel('days after 29 May 2015')
    axes[1].set_ylabel('2 [l(tc_hat) - l(tc)]')
    axes[1].set_ylim(0, 25)
    axes[1].set_xlim(0, 70)
    axes[1].set_title('Critical time: profile likelihood')
    h1, l1 = axes[0].get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    h3, l3 = axes[1].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h1 + h2 + h3, l1 + l2 + l3, ncol=3, y=0.02)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch16_lppls', save_it)
    cmax = ci['ci'].loc[:peak]
    return dict(low=d2s(low), peak=d2s(peak), t2=d2s(t2), n=len(x), tc=d2s(todate(f['tc'])), m=f['m'], w=f['w'],
                B=f['B'], osc=f['osc'], damping=f['damping'], qualified=qualified(c),
                cond={k: v for k, v in c.items()}, tc_prof=d2s(todate(tcs[int(np.nanargmax(prof))])),
                lo=d2s(todate(inside.min())) if len(inside) else None, hi=d2s(todate(inside.max())) if len(inside) else None,
                width=float((inside.max() - inside.min()) * 365.25) if len(inside) else None,
                ci_max=float(cmax.max()), ci_max_date=d2s(cmax.idxmax()),
                first_ci=d2s(ci.index[(ci['ci'] > 0).values][0]) if (ci['ci'] > 0).any() else None,
                n_points=len(ci), windows=len(WINDOWS))


# =============================================================================
# 9. EVALUATION OF EARLY WARNINGS
# =============================================================================
EVAL = {'sp500': ('GSPC.INDX', False, '1990-01-01', '1993-01-01'), 'btc': ('BTC-USD.CC', True, '2011-01-01', '2014-01-01')}


def cached_ci(key, recompute=False):
    sym, crypto, a, b = EVAL[key]
    s = prices(sym, crypto).loc[a:]
    path = os.path.join(HERE, f'ch16_ci_{key}.csv')
    ci = None if recompute else read_cached(f'ch16_ci_{key}.csv')
    if ci is not None:
        return s, ci
    ci = confidence_series(s, b, step=5, procs=PROCS)
    ci.to_csv(path, float_format='%.4f')
    return s, ci


def eval_frame(key, R=500):
    """Evaluation dates (the end points of the indicator), scores and the event 'fall of 20% within 182 days'."""
    s, ci = cached_ci(key)
    y = weekly(s)
    o = psy(y.values)
    cvb = psy_cv(o['n'], o['w0'], R=R, seed=SEED)['bsadf95']
    bs = pd.Series(o['bsadf'] - cvb, index=y.index[1:])
    mom = np.log(s).diff(252 if not EVAL[key][1] else 365)
    ff = future_fall(s, HORIZON)
    d = pd.DataFrame({'ci': ci['ci'], 'bsadf': bs.reindex(ci.index, method='ffill'),
                      'mom': mom.reindex(ci.index), 'fall': ff.reindex(ci.index)}).dropna()
    d['event'] = d['fall'] <= -CRASH
    return d, o['w0']


def fig_evaluation(save_it=True, B=999, R=500):
    """ROC curves of three early-warning scores (LPPLS confidence indicator, BSADF minus its pointwise 95% critical
    value, trailing one-year log return) for a 20% fall within 182 days; AUC with moving-block bootstrap intervals."""
    out = {}
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    for ax, key, title in ((axes[0], 'sp500', 'S&P 500, 1993-2026'), (axes[1], 'btc', 'Bitcoin, 2014-2026')):
        d, w0 = eval_frame(key, R=R)
        res = {}
        for sc, lab, c in (('ci', 'LPPLS confidence indicator', st.IDAred), ('bsadf', 'BSADF minus 95% critical value', st.MainBlue),
                           ('mom', 'trailing one-year return', st.Forest)):
            fa, hr = roc(d[sc], d['event'])
            a = auc(d[sc], d['event'])
            bb = block_bootstrap_auc(d[sc].values, d['event'].values, block=26, B=B)
            res[sc] = dict(auc=a, lo=float(np.nanquantile(bb, 0.05)), hi=float(np.nanquantile(bb, 0.95)))
            ax.plot(fa, hr, color=c, label=lab if key == 'sp500' else '_')
        ax.plot([0, 1], [0, 1], color=st.DarkText, ls=':', lw=0.8, label='no skill' if key == 'sp500' else '_')
        ax.set_xlabel('false-alarm rate')
        ax.set_ylabel('hit rate')
        ax.set_title(title)
        res['ci_any'] = alarm_table(d['ci'] > 0, d['event'])
        res['ci_02'] = alarm_table(d['ci'] >= 0.2, d['event'])
        res['bsadf_alarm'] = alarm_table(d['bsadf'] > 0, d['event'])
        res['mom_q90'] = alarm_table(d['mom'] >= d['mom'].quantile(0.9), d['event'])
        res.update(n=len(d), first=d2s(d.index[0]), last=d2s(d.index[-1]), base=float(d['event'].mean()),
                   n_event=int(d['event'].sum()), w0=w0, share_ci_pos=float((d['ci'] > 0).mean()))
        out[key] = res
    st.fig_legend_bottom(fig, ncol=4, y=0.02)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch16_evaluation', save_it)
    out['B'] = B
    return out


# =============================================================================
# 10. AI MINI-CASE: A GSADF SCREEN OF THE COURSE DATA
# =============================================================================
EXCLUDE = ('.GBOND', 'VIX', 'USDT', 'USDC', 'DAI', 'EURRON.FOREX', 'BTBETRETF', 'IBIT', 'ETHA')


def _screen_job(args):
    sym, crypto, B = args
    try:
        s = prices(sym, crypto, 'adjusted_close' if sym.endswith(('.US', '.RO', '.XETRA', '.PA', '.MC', '.LSE', '.AS')) else 'close')
    except Exception:
        return None
    y = np.log(s.resample('ME').last().dropna()).loc[:'2026-08-31']
    y = y.loc['1990-01-01':]
    if len(y) < 121:
        return None
    o = psy(y.values)
    wb = wild_cv(y.values, o['w0'], B=B, seed=SEED)
    rng = np.random.default_rng(SEED)
    bs, _ = bsadf_paths(null_paths(o['n'], B, rng), o['w0'])
    mcd = np.nanmax(bs, axis=1)
    p_w = (1 + np.sum(wb['draws'] >= o['gsadf'])) / (B + 1)
    p_mc = (1 + np.sum(mcd >= o['gsadf'])) / (B + 1)
    return dict(sym=sym, T=o['n'], gsadf=o['gsadf'], p_wild=float(p_w), p_mc=float(p_mc))


def fig_ai_case(save_it=True, B=1999):
    """GSADF on the monthly log price of every series of the course data with at least 10 years (from 1990), p-values
    from the wild bootstrap and from the homoskedastic Monte Carlo null; rejections at 5%, Holm and Benjamini-Hochberg."""
    m = manifest()
    syms = [r for r in m['symbol'] if not any(x in r for x in EXCLUDE)]
    jobs = [(sym, sym.endswith('.CC'), B) for sym in syms]
    res = [r for r in _pool(_screen_job, jobs) if r is not None]
    d = pd.DataFrame(res).sort_values('p_wild').reset_index(drop=True)
    K = len(d)
    holm = int(np.sum(np.cumprod(d['p_wild'].values <= 0.05 / (K - np.arange(K)))))
    pw = np.sort(d['p_wild'].values)
    bhk = np.nonzero(pw <= 0.05 * np.arange(1, K + 1) / K)[0]
    bh = int(bhk[-1] + 1) if len(bhk) else 0
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.plot(np.arange(1, K + 1), pw, 'o', ms=4, color=st.MainBlue, label='wild-bootstrap p-values, sorted')
    ax.plot(np.arange(1, K + 1), np.sort(d['p_mc'].values), 's', ms=3, color=st.Orange, label='Monte Carlo p-values, sorted')
    ax.plot(np.arange(1, K + 1), 0.05 * np.arange(1, K + 1) / K, color=st.IDAred, ls='--', label='Benjamini-Hochberg line, q = 5%')
    ax.axhline(0.05, color=st.Forest, ls=':', label='5% per test')
    ax.set_yscale('log')
    ax.set_xlabel('rank')
    ax.set_ylabel('p-value of GSADF')
    ax.set_title(f'GSADF screen of {K} monthly price series')
    st.legend_outside_bottom(ax, ncol=4, y=-0.2)
    save('ats_ch16_ai_case', save_it)
    return dict(K=K, B=B, rej_mc=int((d['p_mc'] <= 0.05).sum()), rej_wild=int((d['p_wild'] <= 0.05).sum()), holm=holm,
                bh=bh, expected=0.05 * K, min_p=1 / (B + 1), table=d.to_dict(orient='records'))


FIGS = ['rational', 'asymptotics', 'null', 'size', 'dating', 'monitor', 'housing', 'episodes', 'lppls', 'evaluation',
        'ai_case']


def main(names=None):
    """Run the figures and merge their numbers into ch16_numbers.json (re-read before each write)."""
    path = os.path.join(HERE, 'ch16_numbers.json')
    for nm in names or FIGS:
        print('==', nm, flush=True)
        res = globals()['fig_' + nm]()
        N = json.load(open(path)) if os.path.exists(path) else {}
        N[nm] = res
        with open(path, 'w') as f:
            json.dump(N, f, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))


if __name__ == '__main__':
    main(sys.argv[1:] or None)
