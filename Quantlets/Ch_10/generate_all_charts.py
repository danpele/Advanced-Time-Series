"""
generate_all_charts.py -- charts and numbers of Chapter 10 (ATS): long memory and rough volatility
====================================================================================================
Course data (ats_data.py), chart style (ats_style.py), realised measures (Oxford-Man realized library v0.3 for six
equity indices, 2000 - February 2022, via ats_data.read_omi; our Binance one-minute measures for Bitcoin, 2018-2026, in data/realized),
the numpy engine lm_core.py. Every number on the slides comes from here.
  * definitions           ARFIMA autocorrelations and spectra against AR(1); aggregation of AR(1) with random
                          coefficients (Granger 1980); twenty-two years of S&P 500 log realised variance;
  * estimation            Monte Carlo of GPH, local Whittle and exact local Whittle (stationary and non-stationary d);
                          the bias of local Whittle and the MSE-optimal bandwidth for ARFIMA(1, d, 0);
  * short or long memory  Qu (2011) critical values, size and power against random level shifts, d across bandwidths
                          (Perron and Qu 2010); US and Romanian inflation before and after the disinflation;
  * co-memory             FCVAR (Johansen and Nielsen 2012) of S&P 500 log realised variance and log VIX^2;
  * volatility models     GARCH, FIGARCH and HYGARCH for the S&P 500, BET and Bitcoin; long memory of |r|, log r^2
                          and log RV across assets, with the noise-robust local Whittle of Hurvich, Moulines and
                          Soulier (2005); HAR as an approximation of long memory (Corsi 2009);
  * rough volatility      fractional Brownian paths, the hybrid scheme, the Gatheral-Jaisson-Rosenbaum (2018) scaling on
                          six indices and Bitcoin, the measurement-error critique by simulation, roughness and
                          persistence (Bennedsen, Lunde and Pakkanen 2022), the RFSV kernel;
  * forecasting           rolling out-of-sample comparison of HAR, ARFIMA and RFSV forecasts of realised variance
                          at 1, 5 and 22 days (QLIKE, MSE of logs, Diebold-Mariano);
  * AI mini-case          how robust is ``H of order 0.1'' across assets, measures, estimators and subsamples.
Output: charts/ats_ch10_*.pdf/.png, Quantlets/Ch_10/ch10_numbers.json
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_10/generate_all_charts.py [name ...]
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import functools
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import special, stats
from scipy.signal import lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
from ats_data import load_close, load_ohlc, log_returns, read_eurostat, read_fred, read_omi          # noqa: E402
import ats_style as st                                                                               # noqa: E402
from lm_core import (arch_inf_weights, arfima_acf, bandwidth, circulant_eigs, circulant_sim, dm_stat, elw, fbm, fcvar_fit,  # noqa: E402
                     fgn_acov, frac_diff, frac_weights, gjr_scaling, gph, h_with_noise, har_ar_weights, har_design,
                     hybrid_rl, lbias_constant, local_whittle, ltm_fit, lwn, mse_opt_m, nbls, periodogram, qlike,
                     qu_critical, qu_stat, random_level_shift, rfsv_c, rfsv_kernel, sim_arfima, variogram)

warnings.filterwarnings('ignore')
SEED = 2026
REAL_RAW = 'https://raw.githubusercontent.com/danpele/Advanced-Time-Series/main/data/realized/'
REAL_DIR = next((p for p in [os.path.join(HERE, '..', '..', 'data', 'realized')]
                 + [os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..')]
                 if os.path.isdir(p)), '')
OMI_NAMES = {'.SPX': 'S&P 500', '.GDAXI': 'DAX', '.FTSE': 'FTSE 100', '.N225': 'Nikkei 225',
             '.STOXX50E': 'Euro Stoxx 50', '.FCHI': 'CAC 40'}
LAGS = tuple(range(1, 51))                  # lags (days) of the variogram regressions
QS = (0.5, 1.0, 1.5, 2.0, 3.0)              # moments q of the scaling analysis
A_BW = 0.65                                 # default bandwidth m = n^0.65
FC = dict(window=1000, refit=20, horizons=(1, 5, 22))   # rolling out-of-sample design
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
def read_realized(fname, **kw):
    """A file of data/realized: local copy of the course data, otherwise the ATS repository on GitHub."""
    p = os.path.join(REAL_DIR, fname) if REAL_DIR else ''
    return pd.read_csv(p if p and os.path.exists(p) else REAL_RAW + fname, **kw)


def omi(symbol='.SPX', col='rv5'):
    """Oxford-Man realized library v0.3 (Heber, Lunde, Shephard and Sheppard 2009): one index and one measure,
    daily, in %^2 (5-minute realised variance by default); non-positive days dropped."""
    if 'omi' not in _MEM:
        _MEM['omi'] = read_omi()
    d = _MEM['omi']
    s = d[d['symbol'] == symbol].set_index('date').sort_index()[col] * 1e4
    return s[s > 0].dropna().rename(OMI_NAMES[symbol])


def binance(col='rv5', coin='btc'):
    """Our daily realised measures of Bitcoin from Binance one-minute prices (UTC days, %^2)."""
    if 'bin' not in _MEM:
        _MEM['bin'] = read_realized('binance_daily_realized.csv', parse_dates=['date'], index_col='date')
    s = _MEM['bin'][f'{coin}_{col}']
    return s[s > 0].dropna().rename('Bitcoin')


def rv_series(name, col=None):
    """Daily realised variance (%^2) of a named asset: OMI indices (rv5) or Bitcoin (Binance, rv5)."""
    if name == 'btc':
        return binance(col or 'rv5')
    return omi(name, col or 'rv5')


def parkinson(name, start='2000-01-01'):
    """Parkinson (1980) range-based daily variance (ln H - ln L)^2 / (4 ln 2), in %^2; zero-range days dropped."""
    t = load_ohlc(name, start=start)
    v = 1e4 * (np.log(t['high']) - np.log(t['low'])) ** 2 / (4 * np.log(2))
    return v[v > 0]


def returns(name, start='2000-01-01'):
    """Daily log returns in % (EUR/RON: BNR reference rate; Bitcoin: 7 days a week)."""
    return log_returns(name, start=start).dropna()


def sample_acf(x, K):
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    a = np.fft.irfft(f * np.conj(f))[:K + 1]
    return a / a[0]


def inflation(country):
    """Monthly inflation, % annualised: US CPI (FRED CPIAUCSL, seasonally adjusted), 1960 onwards; Romania: HICP
    (Eurostat prc_hicp_minr, index 2025 = 100, not adjusted), 1997 onwards, monthly means removed (seasonal dummies)."""
    if country == 'us':
        p = read_fred('CPIAUCSL').loc['1959-12-01':]
        return (1200 * np.log(p).diff()).dropna().rename('US')
    p = read_eurostat('prc_hicp_minr', 'M.I25.TOTAL.RO').loc['1996-12-01':]
    x = (1200 * np.log(p).diff()).dropna()
    sea = x.groupby(x.index.month).transform('mean') - x.mean()
    return (x - sea).rename('Romania')


# =============================================================================
# 1. LONG MEMORY: DEFINITIONS
# =============================================================================
def fig_overview(save_it=True, K=500):
    """S&P 500 and Bitcoin log realised variance; the sample ACF of S&P 500 log RV against an AR(1) with the same
    first autocorrelation and a hyperbolic fit c k^(2d - 1) on lags 10-500."""
    s = np.log(rv_series('.SPX'))
    b = np.log(rv_series('btc'))
    acf = sample_acf(s.values, K)
    k = np.arange(1, K + 1)
    sl, ic = np.polyfit(np.log(k[4:200]), np.log(acf[5:201]), 1)          # lags 5-200
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw=dict(width_ratios=[1.35, 1]))
    axs[0].plot(s.index, s.values, color=st.MainBlue, lw=0.5, label='S&P 500 (Oxford-Man, 5-min RV)')
    axs[0].plot(b.index, b.values, color=st.Amber, lw=0.5, label='Bitcoin (Binance, 5-min RV)')
    axs[0].set_ylabel('log realised variance (%$^2$)')
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.14)
    axs[1].loglog(k, acf[1:], 'o', ms=2.5, color=st.MainBlue, label='sample ACF, S&P 500 log RV')
    axs[1].loglog(k, acf[1] ** k, color=st.IDAred, lw=1.6, label='AR(1) with the same lag-1 ACF')
    axs[1].loglog(k, np.exp(ic) * k ** sl, '--', color=st.Forest, lw=1.6, label=f'hyperbolic fit on lags 5-200, slope {sl:.2f}')
    axs[1].set_ylim(1e-3, 1.2)
    axs[1].set_xlabel('lag k (days)')
    axs[1].set_ylabel('autocorrelation')
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_overview', save_it)
    return dict(n=len(s), start=str(s.index[0].date()), end=str(s.index[-1].date()), nb=len(b),
                bstart=str(b.index[0].date()), bend=str(b.index[-1].date()), acf1=float(acf[1]), acf22=float(acf[22]),
                acf250=float(acf[250]), acf500=float(acf[500]), ar250=float(acf[1] ** 250), slope=float(sl),
                d_acf=float((sl + 1) / 2))


def fig_acf_spec(save_it=True, K=200):
    """ARFIMA(0, d, 0) against AR(1): autocorrelations (log-log) and spectral densities near frequency zero."""
    k = np.arange(1, K + 1)
    lam = np.logspace(-3, np.log10(np.pi), 300)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    out = {}
    for d, c in ((0.2, st.Teal), (0.4, st.MainBlue)):
        r = arfima_acf(d, K + 1)
        phi = r[1]
        axs[0].loglog(k, r[1:], color=c, lw=1.8, label=f'ARFIMA(0, {d}, 0)')
        axs[0].loglog(k, phi ** k, '--', color=c, lw=1.4, label=f'AR(1), $\\phi$ = {phi:.2f}')
        f = (2 * np.sin(lam / 2)) ** (-2 * d) / (2 * np.pi)
        fa = 1 / (2 * np.pi * np.abs(1 - phi * np.exp(-1j * lam)) ** 2) * (1 - phi ** 2) * special.gamma(1 - 2 * d) / special.gamma(1 - d) ** 2
        axs[1].loglog(lam, f, color=c, lw=1.8, label='_spec')
        axs[1].loglog(lam, fa, '--', color=c, lw=1.4, label='_spec_ar')
        out[str(d)] = dict(r1=float(r[1]), r10=float(r[10]), r100=float(r[100]), ar100=float(phi ** 100),
                           sum100=float(r[1:101].sum()), sum200=float(r[1:201].sum()),
                           ratio=float(r[100] / r[10]))
    axs[0].set_ylim(1e-6, 1.2)
    axs[0].set_xlabel('lag k')
    axs[0].set_ylabel('autocorrelation')
    axs[1].set_xlabel('frequency $\\lambda$')
    axs[1].set_ylabel('spectral density $f(\\lambda)$')
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch10_acf_spec', save_it)
    return out


def aggregate_ar1(N, n, rng, p=1.0, q=1.4):
    """Sum of N independent stationary AR(1) series with phi^2 ~ Beta(p, q) (Granger 1980), scaled by sqrt(N)."""
    phi = np.sqrt(rng.beta(p, q, N))
    x = rng.standard_normal(N) / np.sqrt(1 - phi ** 2)
    out = np.empty(n)
    for t in range(n):
        x = phi * x + rng.standard_normal(N)
        out[t] = x.sum()
    return out / np.sqrt(N)


def fig_aggregation(save_it=True, n=4000, q=1.4, reps=20):
    """Granger (1980): aggregating AR(1) with phi^2 ~ Beta(1, q) gives long memory with d = 1 - q/2."""
    rng = np.random.default_rng(SEED)
    d0 = 1 - q / 2
    m = bandwidth(n, A_BW)
    Ns = [1, 10, 100, 1000, 3000]
    est = {N: [local_whittle(aggregate_ar1(N, n, rng, q=q), m)[0] for _ in range(reps)] for N in Ns}
    x = aggregate_ar1(3000, n, rng, q=q)
    lam, I = periodogram(x, n // 2)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    axs[0].loglog(lam, I, '.', ms=1.5, color=st.MainBlue, label='periodogram of the aggregate (N = 3000)')
    G = np.mean(lam[:m] ** (2 * d0) * I[:m])
    axs[0].loglog(lam, G * lam ** (-2 * d0), color=st.IDAred, lw=1.8, label=f'slope $-2d$, d = 1 - q/2 = {d0:.1f}')
    axs[0].set_xlabel('frequency $\\lambda_j$')
    axs[0].set_ylabel('$I(\\lambda_j)$')
    st.legend_outside_bottom(axs[0], ncol=1, y=-0.18)
    med = [np.median(est[N]) for N in Ns]
    lo = [np.quantile(est[N], 0.1) for N in Ns]
    hi = [np.quantile(est[N], 0.9) for N in Ns]
    axs[1].fill_between(Ns, lo, hi, color=st.Teal, alpha=0.25, lw=0, label='10%-90% across replications')
    axs[1].semilogx(Ns, med, 'o-', color=st.MainBlue, label='median local Whittle $\\hat d$')
    axs[1].axhline(d0, color=st.IDAred, ls='--', lw=1.2, label=f'Granger limit d = {d0:.1f}')
    axs[1].set_xlabel('number of aggregated AR(1) series N')
    axs[1].set_ylabel('$\\hat d$')
    st.legend_outside_bottom(axs[1], ncol=2, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_aggregation', save_it)
    return dict(d0=d0, q=q, n=n, m=m, reps=reps, med={str(N): float(v) for N, v in zip(Ns, med)},
                lo={str(N): float(v) for N, v in zip(Ns, lo)}, hi={str(N): float(v) for N, v in zip(Ns, hi)})


# =============================================================================
# 2. SEMIPARAMETRIC ESTIMATION
# =============================================================================
def fig_mc_estimators(save_it=True, n=2000, reps=400):
    """Finite-sample distributions of GPH, local Whittle and exact local Whittle (m = n^0.65) for d = 0.3 and for the
    non-stationary d = 1.2, against their asymptotic Normal laws; coverage of the nominal 95% intervals."""
    rng = np.random.default_rng(SEED)
    m = bandwidth(n, A_BW)
    out = dict(n=n, m=m, reps=reps, se_gph=float(np.pi / np.sqrt(24 * m)), se_lw=float(1 / (2 * np.sqrt(m))))
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    for ax, d in zip(axs, (0.3, 1.2)):
        X = sim_arfima(n, d, rng, n_paths=reps)
        E = {'GPH': [], 'LW': [], 'ELW': []}
        for x in X:
            E['GPH'].append(gph(x, m)[0])
            E['LW'].append(local_whittle(x, m)[0])
            E['ELW'].append(elw(x, m)[0])
        res = {}
        bins = np.linspace(d - 0.35, d + 0.35, 50)
        for k, c in (('GPH', st.Amber), ('LW', st.MainBlue), ('ELW', st.IDAred)):
            e = np.array(E[k])
            se = out['se_gph'] if k == 'GPH' else out['se_lw']
            res[k] = dict(mean=float(e.mean()), sd=float(e.std()), cover=float(np.mean(np.abs(e - d) <= 1.96 * se)))
            ax.hist(np.clip(e, bins[0], bins[-1]), bins=bins, density=True, histtype='step', lw=1.8, color=c,
                    label={'GPH': 'GPH', 'LW': 'local Whittle', 'ELW': 'exact local Whittle'}[k])
        g = np.linspace(bins[0], bins[-1], 300)
        ax.plot(g, stats.norm.pdf(g, d, out['se_lw']), ':', color=st.Forest, lw=1.6, label='N(d, 1/(4m))')
        ax.axvline(d, color=st.DarkText, lw=0.8)
        ax.set_title(f'true d = {d}' + (' (non-stationary)' if d > 0.5 else ''))
        ax.set_xlabel('$\\hat d$')
        out[str(d)] = res
    axs[0].set_ylabel('density')
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch10_mc_estimators', save_it)
    return out


def fig_bandwidth(save_it=True, n=2000, phi=0.6, d=0.3, reps=300):
    """Local Whittle for ARFIMA(1, 0.3, 0) with phi = 0.6: Monte Carlo bias and RMSE across bandwidths m = n^a,
    against the leading bias C (m/n)^2 and the asymptotic RMSE; the MSE-optimal bandwidth."""
    rng = np.random.default_rng(SEED + 1)
    a_grid = np.round(np.arange(0.40, 0.801, 0.05), 2)
    X = sim_arfima(n, d, rng, phi=phi, n_paths=reps)
    C = lbias_constant(phi)
    bias, rmse, ms = [], [], []
    for a in a_grid:
        m = bandwidth(n, a)
        e = np.array([local_whittle(x, m)[0] for x in X]) - d
        bias.append(e.mean())
        rmse.append(np.sqrt(np.mean(e ** 2)))
        ms.append(m)
    ms = np.array(ms)
    th_b = C * (ms / n) ** 2
    th_r = np.sqrt(th_b ** 2 + 1 / (4 * ms))
    mopt = mse_opt_m(n, C)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    axs[0].plot(ms, bias, 'o-', color=st.MainBlue, label='Monte Carlo bias')
    axs[0].plot(ms, th_b, '--', color=st.IDAred, label='leading term C (m/n)$^2$')
    axs[0].set_xscale('log')
    axs[0].set_xlabel('bandwidth m (log scale)')
    axs[0].set_ylabel('bias of $\\hat d$')
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.18)
    axs[1].plot(ms, rmse, 'o-', color=st.MainBlue, label='Monte Carlo RMSE')
    axs[1].plot(ms, th_r, '--', color=st.IDAred, label='asymptotic RMSE')
    axs[1].axvline(mopt, color=st.Forest, lw=1.2, ls=':', label=f'MSE-optimal m* = {mopt:.0f}')
    axs[1].set_xscale('log')
    axs[1].set_xlabel('bandwidth m (log scale)')
    axs[1].set_ylabel('RMSE of $\\hat d$')
    st.legend_outside_bottom(axs[1], ncol=3, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_bandwidth', save_it)
    i = int(np.argmin(rmse))
    return dict(n=n, phi=phi, d=d, reps=reps, C=float(C), mopt=float(mopt), aopt=float(np.log(mopt) / np.log(n)),
                a=a_grid.tolist(), m=ms.tolist(), bias=[float(x) for x in bias], rmse=[float(x) for x in rmse],
                th_bias=th_b.tolist(), best_m=int(ms[i]), best_a=float(a_grid[i]))


# =============================================================================
# 3. SHORT OR LONG MEMORY
# =============================================================================
def qu_designs(n, rng):
    """Data-generating processes of the size and power study (each one path)."""
    return {'ARFIMA(0, 0.3, 0)': lambda: sim_arfima(n, 0.3, rng)[0],
            'ARFIMA(1, 0.3, 0), phi = 0.5': lambda: sim_arfima(n, 0.3, rng, phi=0.5)[0],
            'AR(1) + level shifts': lambda: random_level_shift(n, rng, p=0.004, s_shift=1.0, s_noise=1.0, phi=0.3),
            'one break in mean': lambda: rng.standard_normal(n) + 0.6 * (np.arange(n) >= n // 2)}


def fig_qu(save_it=True, n=2000, reps=300, a=0.7):
    """Qu (2011): simulated critical values; rejection rates at 5% under two long-memory nulls and two short-memory
    alternatives with level shifts; local Whittle d across bandwidths (Perron and Qu 2010), with S&P 500 log RV."""
    crit = {str(e): qu_critical(eps=e) for e in (0.02, 0.05)}
    c5 = crit['0.02']['0.95']
    rng = np.random.default_rng(SEED + 2)
    a_grid = np.round(np.arange(0.40, 0.851, 0.05), 2)
    rej, dbar, curves = {}, {}, {}
    m = bandwidth(n, a)
    for name, gen in qu_designs(n, rng).items():
        W, D, C = [], [], []
        for _ in range(reps):
            x = gen()
            w, d = qu_stat(x, m, 0.02)
            W.append(w)
            D.append(d)
            if len(C) < 100:
                C.append([local_whittle(x, bandwidth(n, aa))[0] for aa in a_grid])
        rej[name] = float(np.mean(np.array(W) > c5))
        dbar[name] = float(np.mean(D))
        curves[name] = np.mean(C, axis=0)
    y = np.log(rv_series('.SPX').values)
    spx = [local_whittle(y, bandwidth(len(y), aa))[0] for aa in a_grid]
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw=dict(width_ratios=[1.2, 1]))
    cols = [st.MainBlue, st.Teal, st.IDAred, st.Orange]
    for (name, cv), c in zip(curves.items(), cols):
        axs[0].plot(a_grid, cv, 'o-', ms=3, color=c, label=name)
    axs[0].plot(a_grid, spx, 's-', ms=3, color=st.Forest, lw=2, label='S&P 500 log RV')
    axs[0].set_xlabel('bandwidth exponent a (m = n$^a$)')
    axs[0].set_ylabel('local Whittle $\\hat d$')
    st.legend_outside_bottom(axs[0], ncol=3, y=-0.18)
    names = list(rej)
    axs[1].barh(range(len(names)), [100 * rej[k] for k in names], color=cols)
    axs[1].axvline(5, color=st.DarkText, ls='--', lw=1)
    axs[1].set_yticks(range(len(names)))
    axs[1].set_yticklabels(names)
    axs[1].invert_yaxis()
    axs[1].set_xlabel('rejection rate of the Qu test at 5% (%)')
    plt.tight_layout()
    save('ats_ch10_qu', save_it)
    W_spx = qu_stat(y, bandwidth(len(y), a), 0.02)[0]
    return dict(crit=crit, n=n, reps=reps, m=m, a=a, rej=rej, dbar=dbar, a_grid=a_grid.tolist(),
                curves={k: v.tolist() for k, v in curves.items()}, spx=spx, W_spx=W_spx,
                spx_drop=float(spx[0] - spx[-1]))


def fig_inflation(save_it=True, a=0.65):
    """US and Romanian monthly inflation: exact local Whittle d across bandwidths for the full sample and after the
    disinflation (US from 1985, Romania from 2005); Qu statistics (m = n^0.7, eps = 0.05)."""
    crit = qu_critical(eps=0.05)
    out = dict(crit=crit)
    a_grid = np.round(np.arange(0.45, 0.801, 0.05), 2)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    for ax, c, cut in zip(axs, ('us', 'ro'), ('1985-01-01', '2005-01-01')):
        x = inflation(c)
        res = {}
        for lab, s, col in (('full', x, st.MainBlue), ('post', x.loc[cut:], st.IDAred)):
            v = s.values
            n = len(v)
            dd = [elw(v, bandwidth(n, aa))[0] for aa in a_grid]
            se = [1 / (2 * np.sqrt(bandwidth(n, aa))) for aa in a_grid]
            lab_t = f'{s.index[0].year}-{s.index[-1].year}'
            ax.fill_between(a_grid, np.array(dd) - 1.96 * np.array(se), np.array(dd) + 1.96 * np.array(se),
                            color=col, alpha=0.15, lw=0)
            ax.plot(a_grid, dd, 'o-', ms=3, color=col, label=f'{lab_t} (n = {n})')
            W = qu_stat(v - v.mean(), bandwidth(n, 0.7), 0.05)[0]
            res[lab] = dict(n=n, start=str(s.index[0].date()), end=str(s.index[-1].date()),
                            d=float(elw(v, bandwidth(n, a))[0]), se=float(1 / (2 * np.sqrt(bandwidth(n, a)))),
                            lw=float(local_whittle(v, bandwidth(n, a))[0]), W=float(W), mean=float(v.mean()),
                            curve=[float(z) for z in dd])
        ax.axhline(0.5, color=st.DarkText, ls=':', lw=1)
        ax.set_title({'us': 'United States, CPI', 'ro': 'Romania, HICP'}[c])
        ax.set_xlabel('bandwidth exponent a (m = n$^a$)')
        ax.set_ylabel('exact local Whittle $\\hat d$')
        st.legend_outside_bottom(ax, ncol=2, y=-0.18)
        out[c] = res
    plt.tight_layout()
    save('ats_ch10_inflation', save_it)
    out['a_grid'] = a_grid.tolist()
    return out


# =============================================================================
# 4. FRACTIONAL COINTEGRATION
# =============================================================================
def rv_vix():
    """S&P 500 log realised variance (OMI, 5-min) and log VIX^2/252 (daily %^2), common days."""
    rv = rv_series('.SPX')
    vix = load_close('vix', start='2000-01-01')
    df = pd.concat([np.log(rv), np.log(vix ** 2 / 252)], axis=1, keys=['rv', 'iv']).dropna()
    return df


def fig_fcvar(save_it=True):
    """FCVAR with k = 0 (Johansen and Nielsen 2012) of (log RV, log VIX^2): profile likelihood over (d, b), rank tests,
    the cointegrating vector; local Whittle d of each series and of the spread; narrow-band least squares."""
    df = rv_vix()
    X = df[['rv', 'iv']].values
    f = fcvar_fit(X, np.round(np.arange(0.30, 1.001, 0.02), 2))
    n = len(df)
    m = bandwidth(n, A_BW)
    beta2 = -f['beta'][1]
    spread = df['rv'].values - beta2 * df['iv'].values
    out = dict(n=n, start=str(df.index[0].date()), end=str(df.index[-1].date()), m=m,
               d_rv=local_whittle(df['rv'].values, m)[0], d_iv=local_whittle(df['iv'].values, m)[0],
               d_spread=local_whittle(spread, m)[0], se=1 / (2 * np.sqrt(m)),
               nbls=nbls(df['rv'].values, df['iv'].values, bandwidth(n, 0.6)),
               **{k: v for k, v in f.items() if k != 'surf'})
    out['beta2'] = beta2
    S = f['surf']
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw=dict(width_ratios=[1.35, 1]))
    axs[0].plot(df.index, df['rv'], color=st.MainBlue, lw=0.5, label='log RV, S&P 500')
    axs[0].plot(df.index, df['iv'], color=st.IDAred, lw=0.7, label='log VIX$^2$/252')
    axs[0].set_ylabel('log daily variance (%$^2$)')
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.14)
    sel = S[:, 2] > S[:, 2].max() - 60
    sc = axs[1].scatter(S[sel, 0], S[sel, 1], c=S[sel, 2] - S[:, 2].max(), s=14, cmap='viridis')
    axs[1].plot([f['d']], [f['b']], '*', ms=16, color=st.IDAred, label=f'maximum: d = {f["d"]:.2f}, b = {f["b"]:.2f}')
    plt.colorbar(sc, ax=axs[1], label='profile log-likelihood (minus maximum)')
    axs[1].set_xlabel('d')
    axs[1].set_ylabel('b')
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_fcvar', save_it)
    return out


# =============================================================================
# 5. LONG MEMORY IN VOLATILITY
# =============================================================================
VOL_ASSETS = {'sp500': '2000-01-01', 'bet': '2000-01-01', 'btc': '2015-01-01'}


def fig_figarch(save_it=True, K=1000):
    """GARCH(1,1), FIGARCH(1,d,1) and HYGARCH with Student t innovations for the S&P 500, BET and Bitcoin; the ARCH
    weights of the S&P 500 models."""
    out = {}
    for nm, s0 in VOL_ASSETS.items():
        r = returns(nm, start=s0).values
        out[nm] = {k: ltm_fit(r, k, K) for k in ('garch', 'figarch', 'hygarch')}
        out[nm]['n'] = len(r)
        for k in ('garch', 'figarch', 'hygarch'):
            p = out[nm][k]['par']
            lam = (arch_inf_weights('garch', (p[1], p[2]), K) if k == 'garch' else
                   arch_inf_weights(k, tuple(p[1:4]) if k == 'figarch' else tuple(p[1:5]), K))
            out[nm][k]['w22'] = float(lam[22:].sum() / lam.sum())
            out[nm][k]['w250'] = float(lam[250:].sum() / lam.sum())
            out[nm][k]['sum'] = float(lam.sum())
            if nm == 'sp500':
                out[nm][k]['lam'] = lam
        out[nm]['lr_fig_garch'] = 2 * (out[nm]['figarch']['ll'] - out[nm]['garch']['ll'])
        out[nm]['lr_hy_fig'] = 2 * (out[nm]['hygarch']['ll'] - out[nm]['figarch']['ll'])
    k = np.arange(1, K + 1)
    fig, ax = plt.subplots(figsize=(10, 4.0))
    for m_, c, lab in (('garch', st.IDAred, 'GARCH(1,1)'), ('figarch', st.MainBlue, 'FIGARCH(1,d,1)'),
                       ('hygarch', st.Forest, 'HYGARCH')):
        lam = out['sp500'][m_].pop('lam')
        ax.loglog(k, np.clip(lam, 1e-12, None), color=c, lw=1.8, ls='--' if m_ == 'hygarch' else '-', label=lab)
    ax.set_ylim(1e-8, 0.3)
    ax.set_xlabel('lag k (days)')
    ax.set_ylabel('ARCH($\\infty$) weight $\\lambda_k$')
    st.legend_outside_bottom(ax, ncol=3, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_figarch', save_it)
    return out


def logsq(r):
    """log(r^2 + c) with c = 1% of the sample variance (guards against zero returns)."""
    r = np.asarray(r, float)
    return np.log(r ** 2 + 0.01 * r.var())


ASSETS_D = {'sp500': ('S&P 500', '2000-01-01', '.SPX'), 'dax': ('DAX', '2000-01-01', '.GDAXI'),
            'bet': ('BET', '2000-01-01', None), 'eurron': ('EUR/RON', '2005-07-01', None),
            'btc': ('Bitcoin', '2014-09-17', 'btc')}


def fig_assets_d(save_it=True, a=A_BW):
    """Long memory of volatility proxies: local Whittle d of |r| and log r^2, the noise-robust estimator of Hurvich,
    Moulines and Soulier (2005) on log r^2, and local Whittle on log RV where realised measures exist; Qu test on |r|."""
    crit = qu_critical(eps=0.02)
    out = dict(crit=crit, a=a)
    rows = []
    for nm, (lab, s0, rvk) in ASSETS_D.items():
        r = returns(nm, start=s0).values
        n = len(r)
        m = bandwidth(n, a)
        res = dict(n=n, m=m, abs=local_whittle(np.abs(r), m)[0], lsq=local_whittle(logsq(r), m)[0],
                   lwn=lwn(logsq(r), bandwidth(n, 0.8))[0], qu=qu_stat(np.abs(r), bandwidth(n, 0.7), 0.02)[0],
                   zeros=float(np.mean(r == 0)))
        if rvk:
            y = np.log(rv_series(rvk).values)
            res['rv'] = local_whittle(y, bandwidth(len(y), a))[0]
            res['n_rv'] = len(y)
            res['qu_rv'] = qu_stat(y, bandwidth(len(y), 0.7), 0.02)[0]
        out[nm] = res
        rows.append((lab, res))
    fig, ax = plt.subplots(figsize=(12, 4.0))
    w = 0.2
    x = np.arange(len(rows))
    for i, (key, c, lab) in enumerate((('abs', st.MainBlue, 'LW, |r|'), ('lsq', st.Amber, 'LW, log r$^2$'),
                                       ('lwn', st.Forest, 'LW with noise, log r$^2$'), ('rv', st.IDAred, 'LW, log RV'))):
        vals = [res.get(key, np.nan) for _, res in rows]
        ax.bar(x + (i - 1.5) * w, vals, w, color=c, label=lab)
    ax.axhline(0.5, color=st.DarkText, ls=':', lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([lab for lab, _ in rows])
    ax.set_ylabel('$\\hat d$')
    st.legend_outside_bottom(ax, ncol=4, y=-0.14)
    plt.tight_layout()
    save('ats_ch10_assets_d', save_it)
    return out


def har_fit_full(y, h=1):
    """OLS of y_{t+h} on the HAR regressors (full sample)."""
    t, X = har_design(y)
    keep = t + h < len(y)
    b = np.linalg.lstsq(X[keep], y[t[keep] + h], rcond=None)[0]
    u = y[t[keep] + h] - X[keep] @ b
    return b, float(u.var())


def fig_har_approx(save_it=True, K=500, n_sim=200_000):
    """HAR as an approximation of long memory (Corsi 2009): implied AR weights against ARFIMA pi-weights; the ACF
    implied by the fitted HAR against the sample ACF of S&P 500 log RV."""
    y = np.log(rv_series('.SPX').values)
    b, s2 = har_fit_full(y, 1)
    w = har_ar_weights(b[1:])
    m = bandwidth(len(y), A_BW)
    d = local_whittle(y, m)[0]
    pi = -frac_weights(d, 101)[1:]
    rng = np.random.default_rng(SEED + 3)
    e = rng.standard_normal(n_sim + 2000) * np.sqrt(s2)
    from scipy import signal as sg
    sim = sg.lfilter([1.0], np.concatenate([[1.0], -w]), e)[2000:]
    acf_h = sample_acf(sim, K)
    acf_s = sample_acf(y, K)
    k = np.arange(1, K + 1)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    kk = np.arange(1, 101)
    axs[0].loglog(kk[:22], w, 'o-', ms=3, color=st.IDAred, label='HAR, implied AR weights')
    axs[0].loglog(kk, pi, color=st.MainBlue, lw=1.8, label=f'ARFIMA, $-\\pi_k$ with d = {d:.2f}')
    axs[0].set_xlabel('lag k (days)')
    axs[0].set_ylabel('weight on $y_{t+1-k}$')
    st.legend_outside_bottom(axs[0], ncol=1, y=-0.18)
    axs[1].loglog(k, acf_s[1:], 'o', ms=2.5, color=st.MainBlue, label='sample ACF, S&P 500 log RV')
    axs[1].loglog(k, np.clip(acf_h[1:], 1e-4, None), color=st.IDAred, lw=1.8, label='ACF implied by the fitted HAR')
    axs[1].set_ylim(1e-2, 1.1)
    axs[1].set_xlabel('lag k (days)')
    axs[1].set_ylabel('autocorrelation')
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_har_approx', save_it)
    gap = np.where(acf_h[1:] < 0.5 * acf_s[1:])[0]
    return dict(b=b.tolist(), d=d, persistence=float(w.sum()), acf_s=dict(k22=float(acf_s[22]), k100=float(acf_s[100]), k250=float(acf_s[250]), k500=float(acf_s[500])),
                acf_h=dict(k22=float(acf_h[22]), k100=float(acf_h[100]), k250=float(acf_h[250]), k500=float(acf_h[500])),
                half_lag=int(gap[0] + 1) if len(gap) else None, pi=dict(k1=float(pi[0]), k5=float(pi[4]), k22=float(pi[21]), k100=float(pi[99])))


# =============================================================================
# 6. ROUGH VOLATILITY
# =============================================================================
def fig_fbm_paths(save_it=True, n=1000):
    """Fractional Brownian motion with H = 0.1, 0.3, 0.5, 0.7 (circulant embedding)."""
    fig, axs = plt.subplots(4, 1, figsize=(12, 5.2), sharex=True)
    out = {}
    for ax, H, c in zip(axs, (0.1, 0.3, 0.5, 0.7), (st.IDAred, st.Orange, st.MainBlue, st.Forest)):
        B = fbm(n, H, np.random.default_rng(SEED), 1)[0]
        ax.plot(np.linspace(0, 1, n + 1), B, color=c, lw=0.8, label=f'H = {H}')
        ax.set_yticks([])
        ax.legend(loc='upper left', frameon=False)
        out[str(H)] = dict(rho1=float(fgn_acov(H, 2)[1]), eig_min=float(circulant_eigs(fgn_acov(H, 2 ** 10)).min()))
    axs[-1].set_xlabel('t')
    plt.tight_layout()
    save('ats_ch10_fbm_paths', save_it)
    return out


def fig_hybrid(save_it=True, n=250, paths=4000):
    """Variance of X(1) for the Riemann-Liouville process: forward Riemann sum against the hybrid scheme of
    Bennedsen, Lunde and Pakkanen (2017), relative to the exact value 1/(2H)."""
    Hs = np.array([0.05, 0.1, 0.2, 0.3, 0.4])
    out = dict(n=n, paths=paths, H=Hs.tolist(), riemann=[], hybrid=[])
    for H in Hs:
        rng = np.random.default_rng(SEED)
        ex = 1 / (2 * H)
        out['riemann'].append(float(hybrid_rl(n, H, rng, paths, kappa=0)[:, -1].var() / ex))
        out['hybrid'].append(float(hybrid_rl(n, H, rng, paths, kappa=1)[:, -1].var() / ex))
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(Hs, out['riemann'], 'o-', color=st.IDAred, label='forward Riemann sum')
    ax.plot(Hs, out['hybrid'], 's-', color=st.MainBlue, label='hybrid scheme ($\\kappa$ = 1)')
    ax.axhline(1, color=st.DarkText, ls=':', lw=1)
    ax.set_xlabel('Hurst exponent H')
    ax.set_ylabel('simulated / exact Var X(1)')
    st.legend_outside_bottom(ax, ncol=2, y=-0.2)
    plt.tight_layout()
    save('ats_ch10_hybrid', save_it)
    return out


def fig_gjr(save_it=True):
    """Gatheral, Jaisson and Rosenbaum (2018) on S&P 500 5-minute RV: log m(q, Delta) against log Delta, and zeta_q
    against q; H by subsample."""
    s = rv_series('.SPX')
    x = 0.5 * np.log(s.values)
    g = gjr_scaling(x, LAGS, QS)
    lg = np.log(np.array(LAGS, float))
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw=dict(width_ratios=[1.3, 1]))
    cols = [st.Teal, st.MainBlue, st.Forest, st.IDAred, st.Purple]
    for q, c in zip(QS, cols):
        y = np.log(variogram(x, LAGS, q))
        axs[0].plot(lg, y, 'o', ms=2.5, color=c, label=f'q = {q}')
        bq, aq = np.polyfit(lg, y, 1)
        axs[0].plot(lg, aq + bq * lg, color=c, lw=1)
    axs[0].set_xlabel('log $\\Delta$ (days)')
    axs[0].set_ylabel('log m(q, $\\Delta$)')
    st.legend_outside_bottom(axs[0], ncol=5, y=-0.18)
    axs[1].plot(QS, g['zeta'], 'o', ms=7, color=st.MainBlue, label='$\\zeta_q$ (slopes)')
    qq = np.linspace(0, 3.2, 50)
    axs[1].plot(qq, g['H'] * qq, color=st.IDAred, lw=1.6, label=f'$\\zeta_q$ = qH, H = {g["H"]:.3f}')
    axs[1].set_xlabel('q')
    axs[1].set_ylabel('$\\zeta_q$')
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_gjr', save_it)
    sub = {}
    for lab, a, b in (('2000-2010', '2000-01-01', '2010-12-31'), ('2011-2022', '2011-01-01', '2022-12-31')):
        xx = 0.5 * np.log(s.loc[a:b].values)
        sub[lab] = gjr_scaling(xx, LAGS, QS)['H']
    lin = np.polyfit(QS, g['zeta'], 1)
    return dict(n=len(s), **g, sub=sub, c=float(rfsv_c(g['H'])), lin_icpt=float(lin[1]))


def fig_gjr_assets(save_it=True):
    """H of six OMI indices and Bitcoin: moment regression (GJR), with a measurement-error intercept, and from the
    Parkinson range of daily OHLC prices (EODHD) over the same days."""
    rows = {}
    pk = {'.SPX': 'sp500', '.GDAXI': 'dax', '.STOXX50E': 'stoxx50', '.N225': 'nikkei', 'btc': 'btc'}
    for k in list(OMI_NAMES) + ['btc']:
        s = rv_series(k)
        x = 0.5 * np.log(s.values)
        g = gjr_scaling(x, LAGS, QS)
        hn = h_with_noise(x, LAGS)
        r = dict(n=len(s), H=g['H'], nu=g['nu'], Hn=hn['H'], share=hn['share'], d=local_whittle(2 * x, bandwidth(len(x), A_BW))[0])
        if k in pk:
            p = parkinson(pk[k], start=str(s.index[0].date()))
            p = p.loc[:s.index[-1]]
            xp = 0.5 * np.log(p.values)
            r['Hp'] = gjr_scaling(xp, LAGS, QS)['H']
            r['Hpn'] = h_with_noise(xp, LAGS)['H']
            r['sharep'] = h_with_noise(xp, LAGS)['share']
        rows[k] = r
    labs = [OMI_NAMES.get(k, 'Bitcoin') for k in rows]
    x_ = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(12, 4.0))
    w = 0.2
    for i, (key, c, lab) in enumerate((('H', st.MainBlue, 'RV, moment regression'), ('Hn', st.Teal, 'RV, with error intercept'),
                                       ('Hp', st.IDAred, 'Parkinson range'), ('Hpn', st.Orange, 'Parkinson, with error intercept'))):
        ax.bar(x_ + (i - 1.5) * w, [rows[k].get(key, np.nan) for k in rows], w, color=c, label=lab)
    ax.axhline(0.5, color=st.DarkText, ls=':', lw=1)
    ax.set_xticks(x_)
    ax.set_xticklabels(labs)
    ax.set_ylabel('estimated H')
    st.legend_outside_bottom(ax, ncol=4, y=-0.14)
    plt.tight_layout()
    save('ats_ch10_gjr_assets', save_it)
    return rows


def sim_sv_rv(H, n_days, rng, M=78, kappa=0.01, eta=0.15, mean_logv=0.0):
    """Log volatility as a fractional OU on an intraday grid (M steps a day, mean reversion kappa per day, daily
    increment s.d. eta), intraday returns sigma dW: daily integrated variance IV and realised variance RV."""
    N = n_days * M
    dt = 1.0 / M
    g = circulant_sim(fgn_acov(H, N), rng, 1)[0] * eta * dt ** H
    x = lfilter([1.0], [1.0, -(1 - kappa * dt)], g)          # x_i = (1 - kappa dt) x_{i-1} + g_i
    sig2 = np.exp(2 * (x + mean_logv))
    r2 = sig2 * dt * rng.standard_normal(N) ** 2
    IV = (sig2 * dt).reshape(n_days, M).sum(1)
    RV = r2.reshape(n_days, M).sum(1)
    return IV, RV


def fig_noise_sim(save_it=True, n_days=2500, reps=8):
    """Measurement error and roughness: H estimated from log IV (true), from log RV (78 intraday returns), and from log
    RV with the error intercept, when the true log volatility has H = 0.1, 0.3 or 0.5."""
    rng = np.random.default_rng(SEED + 4)
    Hs = (0.1, 0.3, 0.5)
    res = {str(H): dict(iv=[], rv=[], rvn=[]) for H in Hs}
    for H in Hs:
        for _ in range(reps):
            IV, RV = sim_sv_rv(H, n_days, rng)
            res[str(H)]['iv'].append(gjr_scaling(0.5 * np.log(IV), LAGS, QS)['H'])
            res[str(H)]['rv'].append(gjr_scaling(0.5 * np.log(RV), LAGS, QS)['H'])
            res[str(H)]['rvn'].append(h_with_noise(0.5 * np.log(RV), LAGS)['H'])
    out = {H: {k: dict(mean=float(np.mean(v)), sd=float(np.std(v))) for k, v in r.items()} for H, r in res.items()}
    fig, ax = plt.subplots(figsize=(10, 3.9))
    x = np.arange(len(Hs))
    w = 0.25
    for i, (k, c, lab) in enumerate((('iv', st.Forest, 'from log IV (no error)'), ('rv', st.IDAred, 'from log RV, moment regression'),
                                     ('rvn', st.MainBlue, 'from log RV, with error intercept'))):
        ax.bar(x + (i - 1) * w, [out[str(H)][k]['mean'] for H in Hs], w, yerr=[out[str(H)][k]['sd'] for H in Hs],
               color=c, capsize=3, label=lab)
    ax.plot(x, Hs, '_', ms=40, mew=2, color=st.DarkText, label='true H')
    ax.set_xticks(x)
    ax.set_xticklabels([f'true H = {H}' for H in Hs])
    ax.set_ylabel('estimated H')
    st.legend_outside_bottom(ax, ncol=4, y=-0.14)
    plt.tight_layout()
    save('ats_ch10_noise_sim', save_it)
    out['design'] = dict(n_days=n_days, reps=reps, M=78)
    return out


def fig_decouple(save_it=True, K=1000):
    """Roughness and persistence (Bennedsen, Lunde and Pakkanen 2022): the variogram of S&P 500 log volatility over
    lags 1-1000 (short-lag slope 2H, flattening at long lags) and its ACF (hyperbolic decay)."""
    x = 0.5 * np.log(rv_series('.SPX').values)
    lags = np.unique(np.round(np.logspace(0, np.log10(K), 40)).astype(int))
    m2 = variogram(x, lags, 2.0)
    acf = sample_acf(x, K)
    lg = np.log(lags)
    s_short = np.polyfit(lg[lags <= 10], np.log(m2[lags <= 10]), 1)
    s_long = np.polyfit(lg[(lags >= 100)], np.log(m2[(lags >= 100)]), 1)
    k = np.arange(1, K + 1)
    a_long = np.polyfit(np.log(k[9:250]), np.log(acf[10:251]), 1)              # lags 10-250
    n = len(x)
    d_lw = local_whittle(x, bandwidth(n, 0.5))[0]
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    axs[0].loglog(lags, m2, 'o', ms=3, color=st.MainBlue, label='m(2, $\\Delta$), S&P 500 log volatility')
    axs[0].loglog(lags[lags <= 30], np.exp(s_short[1]) * lags[lags <= 30] ** s_short[0], color=st.IDAred, lw=1.8,
                  label=f'short lags: slope 2H = {s_short[0]:.2f}')
    axs[0].loglog(lags[lags >= 50], np.exp(s_long[1]) * lags[lags >= 50] ** s_long[0], '--', color=st.Forest, lw=1.8,
                  label=f'long lags: slope {s_long[0]:.2f}')
    axs[0].axhline(2 * x.var(), color=st.Amber, ls=':', lw=1.4, label='2 Var(log $\\sigma$)')
    axs[0].set_xlabel('lag $\\Delta$ (days)')
    axs[0].set_ylabel('m(2, $\\Delta$)')
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.18)
    axs[1].loglog(k, np.clip(acf[1:], 1e-3, None), '.', ms=2.5, color=st.MainBlue, label='sample ACF')
    axs[1].loglog(k[9:250], np.exp(a_long[1]) * k[9:250] ** a_long[0], '--', color=st.Forest, lw=1.8,
                  label=f'k$^{{2d-1}}$ fit on lags 10-250: d = {(a_long[0] + 1) / 2:.2f}')
    axs[1].set_xlabel('lag k (days)')
    axs[1].set_ylabel('autocorrelation')
    axs[1].set_ylim(1e-2, 1.1)
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_decouple', save_it)
    return dict(H_short=float(s_short[0] / 2), slope_long=float(s_long[0]), d_acf=float((a_long[0] + 1) / 2),
                d_long=float(s_long[0] / 2 + 0.5), acf1000=float(acf[K]),
                d_lw=float(d_lw), m_lw=bandwidth(n, 0.5), var2=float(2 * x.var()), m2_1000=float(m2[-1]))


@functools.lru_cache(maxsize=None)
def rfsv_kernel_c(H3, h, K=500):
    """rfsv_kernel with H rounded to three decimals (cached for the rolling evaluation)."""
    return rfsv_kernel(H3 / 1000, h, K)


def fig_rfsv_kernel(save_it=True, K=100):
    """Weights of the RFSV predictor (H of the S&P 500) for horizons 1 and 22 days, against the HAR weights."""
    x = 0.5 * np.log(rv_series('.SPX').values)
    H = gjr_scaling(x, LAGS, QS)['H']
    b, _ = har_fit_full(2 * x, 1)
    wh = har_ar_weights(b[1:])
    wh = wh / wh.sum()
    k = np.arange(1, K + 1)
    out = dict(H=H)
    fig, ax = plt.subplots(figsize=(11, 4.0))
    for h, c in ((1, st.MainBlue), (22, st.Teal)):
        w = rfsv_kernel_c(int(round(1000 * H)), h, 500)
        ax.loglog(k, w[:K], color=c, lw=1.8, label=f'RFSV kernel, h = {h}, H = {H:.2f}')
        out[str(h)] = dict(w1=float(w[0]), w5=float(w[:5].sum()), w22=float(w[:22].sum()), w100=float(w[:100].sum()))
    ax.loglog(np.arange(1, 23), wh, 'o-', ms=3, color=st.IDAred, label='HAR weights (normalised), h = 1')
    out['har'] = dict(w1=float(wh[0]), w5=float(wh[:5].sum()))
    ax.set_xlabel('lag k (days)')
    ax.set_ylabel('weight on log RV$_{t+1-k}$')
    st.legend_outside_bottom(ax, ncol=3, y=-0.18)
    plt.tight_layout()
    save('ats_ch10_rfsv_kernel', save_it)
    return out


# =============================================================================
# 7. FORECASTING REALISED VARIANCE: HAR, ARFIMA, RFSV
# =============================================================================
def forecast_rv(rv, window=1000, refit=20, horizons=(1, 5, 22), d_a=A_BW):
    """Rolling out-of-sample forecasts of RV_{t+h} (a single day h ahead) from three models of y = log RV:
    HAR (direct regression for each h), ARFIMA(0, d, 0) (local Whittle d, AR(infinity) iterated), RFSV (Gatheral,
    Jaisson and Rosenbaum 2018: H and nu from the window's variogram, kernel predictor, lognormal correction).
    Level forecasts: HAR and ARFIMA exp(mean + variance/2); RFSV exp(mean + 2 c nu^2 h^(2H)).
    Returns a DataFrame with the target and the forecasts of each model and horizon."""
    y = np.log(np.asarray(rv, float))
    n = len(y)
    H_max = max(horizons)
    rows = []
    par = {}
    for t in range(window - 1, n - H_max):
        if (t - window + 1) % refit == 0:
            Y = y[t - window + 1:t + 1]
            mu = Y.mean()
            tt, X = har_design(Y)
            har = {}
            for h in horizons:
                keep = tt + h < len(Y)
                b = np.linalg.lstsq(X[keep], Y[tt[keep] + h], rcond=None)[0]
                har[h] = (b, float(np.var(Y[tt[keep] + h] - X[keep] @ b)))
            d = local_whittle(Y, bandwidth(window, d_a))[0]
            d = min(d, 0.49)
            pw = frac_weights(d, window + H_max + 1)
            e = frac_diff(Y - mu, d)[50:]
            s2e = float(e.var())
            psi = np.array([1.0] + list(np.cumprod((np.arange(1, H_max) - 1 + d) / np.arange(1, H_max))))
            g = gjr_scaling(0.5 * Y, LAGS, QS)
            H = min(max(g['H'], 0.01), 0.49)
            ker = {h: rfsv_kernel_c(int(round(1000 * H)), h, 500) for h in horizons}
            par = dict(har=har, mu=mu, pw=pw, s2e=s2e, psi=psi, H=H, nu=g['nu'], ker=ker, d=d)
        Y = y[t - window + 1:t + 1]
        row = dict(t=t)
        # HAR
        s = np.cumsum(np.concatenate([[0.0], Y]))
        xr = np.array([1.0, Y[-1], (s[-1] - s[-6]) / 5, (s[-1] - s[-23]) / 22])
        # ARFIMA: iterate the AR(infinity) recursion
        hist = list(Y - par['mu'])
        fc = []
        for k in range(H_max):
            hh = np.array(hist[::-1])
            nxt = -par['pw'][1:len(hh) + 1] @ hh
            fc.append(nxt)
            hist.append(nxt)
        for h in horizons:
            b, v = par['har'][h]
            mh = xr @ b
            row[f'har_l{h}'] = mh
            row[f'har_{h}'] = np.exp(mh + v / 2)
            ma = par['mu'] + fc[h - 1]
            va = par['s2e'] * np.sum(par['psi'][:h] ** 2)
            row[f'arf_l{h}'] = ma
            row[f'arf_{h}'] = np.exp(ma + va / 2)
            w = par['ker'][h]
            mr = w @ Y[::-1][:len(w)]
            row[f'rfsv_l{h}'] = mr
            row[f'rfsv_{h}'] = np.exp(mr + 2 * rfsv_c(par['H']) * par['nu'] ** 2 * h ** (2 * par['H']))
            row[f'y{h}'] = y[t + h]
        row['H'] = par['H']
        row['d'] = par['d']
        rows.append(row)
    return pd.DataFrame(rows)


FC_ASSETS = {'.SPX': 'S&P 500', '.GDAXI': 'DAX', 'btc': 'Bitcoin'}


def evaluate_forecasts(df, horizons=(1, 5, 22)):
    """Average QLIKE (levels) and MSE (logs) of the three models; DM statistics of ARFIMA and RFSV against HAR."""
    out = {}
    for h in horizons:
        rv = np.exp(df[f'y{h}'].values)
        r = {}
        for mdl in ('har', 'arf', 'rfsv'):
            r[mdl] = dict(qlike=float(qlike(rv, df[f'{mdl}_{h}'].values).mean()),
                          mse=float(np.mean((df[f'y{h}'] - df[f'{mdl}_l{h}']) ** 2)))
        for mdl in ('arf', 'rfsv'):
            r[mdl]['dm_q'] = dm_stat(qlike(rv, df[f'{mdl}_{h}'].values), qlike(rv, df[f'har_{h}'].values), h)
            r[mdl]['dm_m'] = dm_stat((df[f'y{h}'] - df[f'{mdl}_l{h}']) ** 2, (df[f'y{h}'] - df[f'har_l{h}']) ** 2, h)
            r[mdl]['rel_q'] = r[mdl]['qlike'] / r['har']['qlike']
            r[mdl]['rel_m'] = r[mdl]['mse'] / r['har']['mse']
        out[str(h)] = r
    return out


def run_forecasts():
    if 'fc' not in _MEM:
        res = {}
        for k in FC_ASSETS:
            s = rv_series(k)
            df = forecast_rv(s.values, **FC)
            df['date'] = s.index[df['t'].values]
            res[k] = df
        _MEM['fc'] = res
    return _MEM['fc']


def fig_forecast(save_it=True):
    """Relative QLIKE (model / HAR) of ARFIMA and RFSV forecasts of RV at 1, 5 and 22 days; DM significance."""
    res = run_forecasts()
    out = {}
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.9), sharey=True)
    for ax, (k, lab) in zip(axs, FC_ASSETS.items()):
        df = res[k]
        ev = evaluate_forecasts(df, FC['horizons'])
        out[k] = dict(eval=ev, T=len(df), start=str(df['date'].iloc[0].date()), end=str(df['date'].iloc[-1].date()),
                      H_med=float(df['H'].median()), H_min=float(df['H'].min()), H_max=float(df['H'].max()),
                      d_med=float(df['d'].median()))
        x = np.arange(len(FC['horizons']))
        for i, (mdl, c, ml) in enumerate((('arf', st.Forest, 'ARFIMA'), ('rfsv', st.IDAred, 'RFSV'))):
            vals = [ev[str(h)][mdl]['rel_q'] for h in FC['horizons']]
            bars = ax.bar(x + (i - 0.5) * 0.36, vals, 0.36, color=c, label=ml)
            for j, h in enumerate(FC['horizons']):
                p = ev[str(h)][mdl]['dm_q'][1]
                if p < 0.05:
                    ax.text(x[j] + (i - 0.5) * 0.36, vals[j] + 0.004, '*', ha='center', color=st.DarkText, fontsize=13)
        ax.axhline(1, color=st.DarkText, ls=':', lw=1)
        ax.set_xticks(x)
        ax.set_xticklabels([f'h = {h}' for h in FC['horizons']])
        ax.set_title(lab)
        lo = min(ev[str(h)][m]['rel_q'] for h in FC['horizons'] for m in ('arf', 'rfsv'))
        hi = max(ev[str(h)][m]['rel_q'] for h in FC['horizons'] for m in ('arf', 'rfsv'))
        ax.set_ylim(min(0.85, lo - 0.03), max(1.1, hi + 0.04))
    axs[0].set_ylabel('QLIKE relative to HAR')
    st.fig_legend_bottom(fig, ncol=2, y=0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch10_forecast', save_it)
    return out


# =============================================================================
# 8. AI MINI-CASE
# =============================================================================
AI_MEASURES = {'omi': ['rv5', 'rv10', 'bv', 'medrv', 'rk_parzen'], 'btc': ['rv1', 'rv5', 'rv15', 'bv5', 'rk1']}


def fig_ai_case(save_it=True):
    """``Volatility is rough'': H for 7 assets x 5 realised measures x 2 estimators x 2 halves of the sample;
    local Whittle d of log RV in the same cells."""
    rows = []
    for k in list(OMI_NAMES) + ['btc']:
        for col in AI_MEASURES['btc' if k == 'btc' else 'omi']:
            s = rv_series(k, col)
            half = len(s) // 2
            for part, ss in (('first half', s.iloc[:half]), ('second half', s.iloc[half:])):
                x = 0.5 * np.log(ss.values)
                rows.append(dict(asset=OMI_NAMES.get(k, 'Bitcoin'), measure=col, part=part, est='moments',
                                 H=gjr_scaling(x, LAGS, QS)['H'], d=local_whittle(2 * x, bandwidth(len(x), A_BW))[0]))
                rows.append(dict(asset=OMI_NAMES.get(k, 'Bitcoin'), measure=col, part=part, est='intercept',
                                 H=h_with_noise(x, LAGS)['H'], d=np.nan))
    t = pd.DataFrame(rows)
    assets = list(dict.fromkeys(t['asset']))
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw=dict(width_ratios=[1.6, 1]))
    rng = np.random.default_rng(SEED)
    for est, c, lab in (('moments', st.MainBlue, 'moment regression'), ('intercept', st.IDAred, 'with error intercept')):
        tt = t[t['est'] == est]
        xs = np.array([assets.index(a) for a in tt['asset']]) + (0.15 if est == 'intercept' else -0.15) + rng.uniform(-0.08, 0.08, len(tt))
        axs[0].plot(xs, tt['H'], 'o', ms=3.5, color=c, alpha=0.8, label=lab)
    axs[0].axhline(0.5, color=st.DarkText, ls=':', lw=1)
    axs[0].set_xticks(range(len(assets)))
    axs[0].set_xticklabels(assets, rotation=20)
    axs[0].set_ylabel('estimated H')
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.3)
    dd = t[t['est'] == 'moments']
    axs[1].scatter(dd['H'], dd['d'], s=14, color=st.Forest, label='cells (moment H, local Whittle d)')
    axs[1].set_xlabel('H (roughness)')
    axs[1].set_ylabel('d (persistence)')
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.3)
    plt.tight_layout()
    save('ats_ch10_ai_case', save_it)
    H = t['H'].values
    return dict(n=int(len(t)), n_cells=int(len(t) // 2), H_min=float(H.min()), H_max=float(H.max()), H_med=float(np.median(H)),
                share02=float(np.mean(H < 0.2)), share03=float(np.mean(H < 0.3)),
                H_med_mom=float(t[t['est'] == 'moments']['H'].median()), H_med_int=float(t[t['est'] == 'intercept']['H'].median()),
                d_min=float(dd['d'].min()), d_max=float(dd['d'].max()), d_med=float(dd['d'].median()),
                corr=float(np.corrcoef(dd['H'], dd['d'])[0, 1]))


if __name__ == '__main__':
    st.apply()
    N = {}
    only = sys.argv[1:]
    path = os.path.join(HERE, 'ch10_numbers.json')
    if os.path.exists(path):
        N = json.load(open(path))
    for name, f in [('overview', fig_overview), ('acf_spec', fig_acf_spec), ('aggregation', fig_aggregation),
                    ('mc', fig_mc_estimators), ('bandwidth', fig_bandwidth), ('qu', fig_qu), ('inflation', fig_inflation),
                    ('fcvar', fig_fcvar), ('figarch', fig_figarch), ('assets_d', fig_assets_d), ('har', fig_har_approx),
                    ('fbm', fig_fbm_paths), ('hybrid', fig_hybrid), ('gjr', fig_gjr), ('gjr_assets', fig_gjr_assets),
                    ('noise', fig_noise_sim), ('decouple', fig_decouple), ('kernel', fig_rfsv_kernel),
                    ('forecast', fig_forecast), ('ai', fig_ai_case)]:
        if only and name not in only:
            continue
        print(name, flush=True)
        N[name] = f()
        with open(path, 'w') as fh:
            json.dump(N, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else (list(o) if isinstance(o, tuple) else float(o)))
    print('written ch10_numbers.json')
