"""
generate_all_charts.py -- charts and numbers of Chapter 0 (ATS): refresher and inference for dependent data
===========================================================================================================
Course data (ats_data.py), chart style (ats_style.py). Every number on the slides comes from here.
  * dependence in our data -- Romanian HICP inflation and real GDP growth (Eurostat), EUR/RON (BNR reference rate),
                              S&P 500 and BET daily log returns and squared returns (EODHD), US macro series (FRED);
  * long-run variance       -- the variance inflation of the sample mean under AR(1) dependence; the size of the
                              naive t-test; the kernels of Newey and West (1987) and Andrews (1991);
  * HAC estimation          -- Bartlett, Parzen and quadratic spectral kernels; the Newey-West rule of thumb, the
                              Andrews (1991) AR(1) plug-in bandwidth, the Lazarus-Lewis-Stock-Watson (2018) rules
                              (Newey-West with fixed-b critical values, equal-weighted cosine), fixed-b critical
                              values (Kiefer and Vogelsang 2005) by simulation;
  * Monte Carlo of size     -- rejection rates of the t-test for a mean under AR(1) dependence, for each estimator;
  * block bootstrap         -- moving-block (Kunsch 1989), circular and stationary (Politis and Romano 1994)
                              bootstrap, with the automatic block length of Politis and White (2004), corrected by
                              Patton, Politis and White (2009);
  * predictive regression   -- US real GDP growth over the next four quarters on the term spread (Estrella and
                              Hardouvelis 1991): overlapping observations and HAC standard errors;
  * data snooping           -- the family-wise error of the best of K tests; the Reality Check of White (2000) for
                              moving-average rules on the BET index;
  * AI mini-case            -- the mean of Romanian HICP inflation since 2013 against the 2.5% target.
Output: charts/ats_ch0_*.pdf/.png, Quantlets/Ch_00/ch0_numbers.json
Run:  python3 Quantlets/Ch_00/generate_all_charts.py
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
from ats_data import load_close, log_returns, read_eurostat, read_fred   # noqa: E402
import ats_style as st                                                   # noqa: E402

warnings.filterwarnings('ignore')
SEED = 2026
GDP_RO = ('namq_10_gdp', 'Q.CLV10_MEUR.SCA.B1GQ.RO')   # Romanian real GDP, chain-linked 2010 volumes, SCA (Eurostat)
HICP_RO = ('prc_hicp_minr', 'M.RCH_A.TOTAL.RO')        # Romanian HICP, annual rate of change, % (Eurostat)
START_MACRO = '2000-01-01'                             # Romanian macro sample start
START_INFL = '2006-01-01'                              # HICP inflation sample start (after the 2005 adoption of inflation targeting)
TARGET_START = '2013-01-01'                            # BNR flat multi-annual target 2.5% +/- 1 pp since 2013
TARGET = 2.5
H_TS = 4                                               # horizon (quarters) of the term-spread regression
FIXED_B_GRID = (0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
MA_LENGTHS = tuple(range(5, 255, 5))                   # 50 moving-average rules for the Reality Check
SB_MEAN_BLOCK = 10                                     # mean block length 1/q of the stationary bootstrap in the Reality Check
NUM = {}


# =============================================================================
# DATA
# =============================================================================
def ro_gdp_growth(start=START_MACRO):
    """Quarter-on-quarter growth of Romanian real GDP, in % (100 x log difference)."""
    y = read_eurostat(*GDP_RO)
    return (100 * np.log(y).diff()).dropna().loc[start:].rename('RO GDP growth')


def ro_inflation(start=START_INFL):
    """Romanian HICP inflation, annual rate of change in % (monthly observations)."""
    return read_eurostat(*HICP_RO).loc[start:].rename('RO HICP inflation')


def daily_series():
    """Daily log returns in % of the S&P 500, the BET and EUR/RON (BNR reference rate); squared S&P 500 returns."""
    sp = log_returns('sp500')
    return {'S&P 500 returns': sp, 'S&P 500 squared returns': (sp ** 2).rename('sq'),
            'BET returns': log_returns('bet'), 'EUR/RON returns': log_returns('eurron')}


def term_spread_data(h=H_TS):
    """US quarterly data: annualised real GDP growth over the next h quarters and the 10-year minus 3-month spread."""
    f = read_fred(['GS10', 'TB3MS'])
    spread = (f['GS10'] - f['TB3MS']).resample('QS').mean()
    gdp = read_fred('GDPC1')
    growth = (400 / h) * np.log(gdp.shift(-h) / gdp)
    d = pd.concat([growth.rename('growth'), spread.rename('spread')], axis=1).dropna()
    return d.loc['1962-01-01':]


def save(name, save_it=True):
    """Save the current figure in charts/ (or show it in a notebook)."""
    if save_it:
        st.check_no_grey(plt.gcf())
        st.save_fig(name)
    else:
        plt.show()
        plt.close()


# =============================================================================
# LONG-RUN VARIANCE AND HAC ESTIMATION
# =============================================================================
def acov_all(x):
    """Sample autocovariances gamma_0, ..., gamma_{T-1} (divisor T, demeaned), by FFT."""
    x = np.asarray(x, float)
    x = x - x.mean(axis=-1, keepdims=True)
    T = x.shape[-1]
    f = np.fft.rfft(x, 2 * T, axis=-1)
    return np.fft.irfft(f * np.conj(f), axis=-1)[..., :T] / T


def kernel(x, kind='bartlett'):
    """Kernel weights k(x): Bartlett (Newey-West), Parzen, quadratic spectral (QS), truncated."""
    x = np.abs(np.asarray(x, float))
    if kind == 'bartlett':
        return np.where(x <= 1, 1 - x, 0.0)
    if kind == 'parzen':
        return np.where(x <= 0.5, 1 - 6 * x ** 2 + 6 * x ** 3, np.where(x <= 1, 2 * (1 - x) ** 3, 0.0))
    if kind == 'qs':
        z = 6 * np.pi * np.where(x == 0, 1.0, x) / 5
        w = 25 / (12 * np.pi ** 2 * np.where(x == 0, 1.0, x) ** 2) * (np.sin(z) / z - np.cos(z))
        return np.where(x == 0, 1.0, w)
    if kind == 'truncated':
        return np.where(x <= 1, 1.0, 0.0)
    raise ValueError(kind)


def lrv(u, S, kind='bartlett'):
    """Kernel estimator of the long-run variance: gamma_0 + 2 sum_j k(j/S) gamma_j (works on rows of a matrix)."""
    g = acov_all(u)
    T = g.shape[-1]
    j = np.arange(1, T)
    return g[..., 0] + 2 * (g[..., 1:] * kernel(j / S, kind)).sum(axis=-1)


def nw_rule(T):
    """Newey-West (1994) rule of thumb: L = floor(4 (T/100)^(2/9)) lags, i.e. Bartlett bandwidth S = L + 1."""
    return int(np.floor(4 * (T / 100) ** (2 / 9))) + 1


def ar1_coef(u):
    """OLS AR(1) coefficient of the demeaned series (rows of a matrix)."""
    u = np.asarray(u, float)
    u = u - u.mean(axis=-1, keepdims=True)
    return (u[..., 1:] * u[..., :-1]).sum(axis=-1) / (u[..., :-1] ** 2).sum(axis=-1)


def andrews_bw(u, kind='bartlett'):
    """Andrews (1991) AR(1) plug-in bandwidth: 1.1447 (a1 T)^(1/3) Bartlett; 2.6614 / 1.3221 (a2 T)^(1/5) Parzen / QS."""
    u = np.asarray(u, float)
    T = u.shape[-1]
    r = ar1_coef(u)
    if kind == 'bartlett':
        a1 = 4 * r ** 2 / ((1 - r) ** 2 * (1 + r) ** 2)
        S = 1.1447 * (a1 * T) ** (1 / 3)
    else:
        a2 = 4 * r ** 2 / (1 - r) ** 4
        S = (2.6614 if kind == 'parzen' else 1.3221) * (a2 * T) ** (1 / 5)
    return np.clip(S, 1.0, T)


def llsw_bw(T):
    """Lazarus, Lewis, Stock and Watson (2018): Newey-West bandwidth S = 1.3 sqrt(T), used with fixed-b critical values."""
    return 1.3 * np.sqrt(T)


def ewc_nu(T):
    """Lazarus, Lewis, Stock and Watson (2018): number of cosine terms (degrees of freedom) of the EWC estimator, 0.4 T^(2/3)."""
    return max(1, int(round(0.4 * T ** (2 / 3))))


def ewc_lrv(u, nu):
    """Equal-weighted cosine (EWC) estimator: the average of nu squared cosine projections of the demeaned series."""
    u = np.asarray(u, float)
    u = u - u.mean(axis=-1, keepdims=True)
    T = u.shape[-1]
    t = np.arange(1, T + 1)
    C = np.sqrt(2 / T) * np.cos(np.pi * np.outer(np.arange(1, nu + 1), t - 0.5) / T)   # nu x T
    lam = u @ C.T
    return (lam ** 2).mean(axis=-1)


def fixed_b_table(grid=FIXED_B_GRID, kind='bartlett', n=500, reps=20000, alpha=0.05, seed=SEED):
    """Fixed-b critical values (Kiefer and Vogelsang 2005) of the two-sided t-test for a mean, by simulation:
    the (1 - alpha) quantile of |t| when S = b T, i.i.d. N(0, 1) data of length n (approximates the limit)."""
    rng = np.random.default_rng(seed)
    j = np.arange(1, n)
    W = np.array([kernel(j / (b * n), kind) for b in grid])        # len(grid) x (n - 1)
    tabs = []
    for _ in range(reps // 5000):                                  # in chunks of 5000 replications
        x = rng.standard_normal((5000, n))
        g = acov_all(x)
        v = g[:, :1] + 2 * g[:, 1:] @ W.T                          # 5000 x len(grid)
        tabs.append(np.abs(np.sqrt(n) * x.mean(axis=1))[:, None] / np.sqrt(np.maximum(v, 1e-12)))
    t = np.vstack(tabs)
    return {b: float(np.quantile(t[:, i], 1 - alpha)) for i, b in enumerate(grid)}


def fixed_b_cv(b, table):
    """Fixed-b critical value at b, by linear interpolation in the simulated table (1.96 at b = 0)."""
    bs = np.array([0.0] + sorted(table))
    cv = np.array([stats.norm.ppf(0.975)] + [table[k] for k in sorted(table)])
    return float(np.interp(b, bs, cv))


def mean_inference(x, cvtab, mu0=0.0):
    """Standard errors of a sample mean and t-statistics for H0: mu = mu0, by method."""
    x = np.asarray(x, float)
    T = len(x)
    m = x.mean()
    g0 = acov_all(x)[0]
    S_nw, S_and, S_qs, S_ll, nu = nw_rule(T), float(andrews_bw(x)), float(andrews_bw(x, 'qs')), llsw_bw(T), ewc_nu(T)
    out = {'T': T, 'mean': m, 'rho1': float(ar1_coef(x)), 'S_nw': S_nw, 'S_and': S_and, 'S_qs': S_qs, 'S_ll': S_ll, 'nu': nu}
    v = {'naive': g0, 'nw': lrv(x, S_nw), 'andrews': lrv(x, S_and), 'qs': lrv(x, S_qs, 'qs'), 'llsw': lrv(x, S_ll),
         'ewc': ewc_lrv(x, nu)}
    cv = {'naive': 1.96, 'nw': 1.96, 'andrews': 1.96, 'qs': 1.96, 'llsw': fixed_b_cv(S_ll / T, cvtab),
          'ewc': float(stats.t.ppf(0.975, nu))}
    for k in v:
        se = float(np.sqrt(max(v[k], 1e-300) / T))
        out[f'se_{k}'] = se
        out[f't_{k}'] = (m - mu0) / se
        out[f'cv_{k}'] = cv[k]
        out[f'lo_{k}'], out[f'hi_{k}'] = m - cv[k] * se, m + cv[k] * se
    return out


# =============================================================================
# BLOCK BOOTSTRAP
# =============================================================================
def politis_white(x):
    """Automatic block length of Politis and White (2004) with the correction of Patton, Politis and White (2009):
    returns (b_SB, b_CB), the optimal mean block lengths of the stationary and of the circular block bootstrap."""
    x = np.asarray(x, float)
    n = len(x)
    g = acov_all(x)
    rho = g / g[0]
    kn = max(5, int(np.ceil(np.sqrt(np.log10(n)))))
    mmax = int(np.ceil(np.sqrt(n))) + kn
    bmax = int(np.ceil(min(3 * np.sqrt(n), n / 3)))
    c = 2 * np.sqrt(np.log10(n) / n)
    mhat = None
    for m in range(1, mmax + 1):
        if np.all(np.abs(rho[m:m + kn]) < c):
            mhat = m
            break
    if mhat is None:
        mhat = mmax
    M = min(2 * mhat, mmax)
    k = np.arange(-M, M + 1)
    lam = np.where(np.abs(k / M) <= 0.5, 1.0, np.where(np.abs(k / M) <= 1, 2 * (1 - np.abs(k / M)), 0.0))
    gk = g[np.abs(k)]
    G = np.sum(lam * np.abs(k) * gk)
    g0 = np.sum(lam * gk)
    b_sb = (2 * G ** 2 / (2 * g0 ** 2)) ** (1 / 3) * n ** (1 / 3)
    b_cb = (2 * G ** 2 / (4 / 3 * g0 ** 2)) ** (1 / 3) * n ** (1 / 3)
    return float(min(b_sb, bmax)), float(min(b_cb, bmax))


def mbb_means(x, l, B, rng, circular=False):
    """Bootstrap means of the moving-block (Kunsch 1989) or circular (Politis and Romano 1992) block bootstrap:
    k = ceil(T / l) blocks of length l drawn with replacement; the first T values are kept."""
    x = np.asarray(x, float)
    T = len(x)
    l = int(max(1, round(l)))
    k = int(np.ceil(T / l))
    xx = np.concatenate([x, x[:l - 1]]) if circular else x
    nblocks = T if circular else T - l + 1
    starts = rng.integers(0, nblocks, size=(B, k))
    idx = (starts[:, :, None] + np.arange(l)[None, None, :]).reshape(B, -1)[:, :T]
    return xx[idx].mean(axis=1)


def sb_means(x, b, B, rng):
    """Bootstrap means of the stationary bootstrap (Politis and Romano 1994): blocks with geometric lengths of
    mean b, starting at uniform positions, wrapped around the end of the sample."""
    x = np.asarray(x, float)
    T = len(x)
    p = 1 / b
    out = np.empty(B)
    for i in range(B):
        idx = np.empty(T, dtype=int)
        idx[0] = rng.integers(T)
        new = rng.random(T) < p
        jumps = rng.integers(0, T, size=T)
        for t in range(1, T):
            idx[t] = jumps[t] if new[t] else (idx[t - 1] + 1) % T
        out[i] = x[idx].mean()
    return out


def sb_indices(T, b, B, rng):
    """Index matrix (B x T) of the stationary bootstrap, vectorised over replications."""
    p = 1 / b
    idx = np.empty((B, T), dtype=int)
    idx[:, 0] = rng.integers(0, T, size=B)
    new = rng.random((B, T)) < p
    jumps = rng.integers(0, T, size=(B, T))
    for t in range(1, T):
        idx[:, t] = np.where(new[:, t], jumps[:, t], (idx[:, t - 1] + 1) % T)
    return idx


def iid_means(x, B, rng):
    """Bootstrap means of the i.i.d. (Efron) bootstrap."""
    x = np.asarray(x, float)
    return x[rng.integers(0, len(x), size=(B, len(x)))].mean(axis=1)


# =============================================================================
# 1. DEPENDENCE IN OUR DATA
# =============================================================================
def fig_data_dashboard(save_it=True):
    """Four series of the chapter: Romanian HICP inflation and GDP growth, EUR/RON and S&P 500 daily returns."""
    infl, gdp, d = ro_inflation(), ro_gdp_growth(), daily_series()
    fig, ax = plt.subplots(2, 2, figsize=(12, 6.2))
    ax[0, 0].plot(infl.index, infl, color=st.IDAred, label='Romania: HICP inflation, annual rate (%)')
    ax[0, 0].axhline(TARGET, color=st.Forest, ls='--', lw=1, label='2.5% (BNR target since 2013)')
    ax[0, 1].bar(gdp.index, gdp, width=70, color=st.MainBlue, label='Romania: real GDP growth, q/q (%)')
    e = d['EUR/RON returns']
    ax[1, 0].plot(e.index, e, color=st.Forest, lw=0.5, label='EUR/RON (BNR) daily log change (%)')
    s = d['S&P 500 returns']
    ax[1, 1].plot(s.index, s, color=st.Purple, lw=0.5, label='S&P 500 daily log return (%)')
    for a in ax.flat:
        a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), frameon=False, fontsize=10.5)
    plt.tight_layout()
    save('ats_ch0_data_dashboard', save_it)
    out = {'infl_first': str(infl.index[0].date()), 'infl_last': str(infl.index[-1].date()), 'infl_n': len(infl),
           'infl_max': float(infl.max()), 'infl_max_d': str(infl.idxmax().date()), 'infl_min': float(infl.min()),
           'infl_min_d': str(infl.idxmin().date()), 'infl_last_v': float(infl.iloc[-1]),
           'gdp_first': str(gdp.index[0].date()), 'gdp_last': str(gdp.index[-1].date()), 'gdp_n': len(gdp),
           'gdp_min': float(gdp.min()), 'gdp_min_d': str(gdp.idxmin().date()),
           'eur_first': str(e.index[0].date()), 'eur_n': len(e), 'sp_n': len(s), 'sp_first': str(s.index[0].date()),
           'bet_n': len(d['BET returns']), 'last_daily': str(s.index[-1].date())}
    NUM['dash'] = out
    return out


def fig_acf_panel(save_it=True, K=24):
    """Sample ACF of six series of the chapter, with the +/- 1.96/sqrt(T) band of the i.i.d. hypothesis."""
    d = daily_series()
    ser = {'S&P 500 returns': d['S&P 500 returns'], 'S&P 500 squared returns': d['S&P 500 squared returns'],
           'EUR/RON returns': d['EUR/RON returns'], 'BET returns': d['BET returns'],
           'RO GDP growth (q/q)': ro_gdp_growth(), 'RO HICP inflation (annual rate)': ro_inflation()}
    cols = [st.MainBlue, st.IDAred, st.Forest, st.Amber, st.Purple, st.Orange]
    fig, ax = plt.subplots(2, 3, figsize=(12.5, 5.8))
    out = {}
    for a, (name, x), c in zip(ax.flat, ser.items(), cols):
        g = acov_all(x.values)
        r = g[1:K + 1] / g[0]
        band = 1.96 / np.sqrt(len(x))
        a.bar(np.arange(1, K + 1), r, color=c, width=0.6, label=name)
        a.axhspan(-band, band, color=st.MainBlue, alpha=0.12, lw=0)
        a.axhline(0, color=st.DarkText, lw=0.6)
        a.set_ylim(min(-0.25, r.min() - 0.05), 1.0)
        a.set_xlabel('lag')
        a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), frameon=False, fontsize=10.5)
        T = len(x)
        out[name] = {'T': T, 'r1': float(r[0]), 'r5': float(r[4]), 'r12': float(r[11]), 'band': float(band),
                     'n_out': int((np.abs(r) > band).sum()), 'ratio_bartlett': float(lrv(x.values, nw_rule(T)) / g[0]),
                     'ratio_andrews': float(lrv(x.values, andrews_bw(x.values)) / g[0])}
    plt.tight_layout()
    save('ats_ch0_acf_panel', save_it)
    NUM['acf'] = out
    return out


# =============================================================================
# 2. LONG-RUN VARIANCE AND THE NAIVE t-TEST
# =============================================================================
def fig_lrv_ar1(save_it=True, T=200, reps=20000):
    """Variance inflation of the sample mean under AR(1): T Var(mean) / gamma_0 against phi, theory and simulation;
    asymptotic size of the naive 5% t-test."""
    rng = np.random.default_rng(SEED)
    phis = np.array([-0.5, -0.25, 0.0, 0.25, 0.5, 0.7, 0.8, 0.9])
    sim = []
    for p in phis:
        e = rng.standard_normal((reps, T + 200))
        x = np.zeros_like(e)
        for t in range(1, e.shape[1]):
            x[:, t] = p * x[:, t - 1] + e[:, t]
        x = x[:, 200:]
        sim.append(T * x.mean(axis=1).var() / (1 / (1 - p ** 2)))
    grid = np.linspace(-0.6, 0.95, 200)
    theo = (1 + grid) / (1 - grid)
    size = 2 * (1 - stats.norm.cdf(1.96 / np.sqrt(theo)))
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    ax[0].plot(grid, theo, color=st.MainBlue, label=r'theory: $(1+\phi)/(1-\phi)$')
    ax[0].plot(phis, sim, 'o', color=st.IDAred, label=f'simulation, T = {T}')
    ax[0].set_yscale('log')
    ax[0].set_xlabel(r'AR(1) coefficient $\phi$')
    ax[0].set_ylabel(r'$T\,\mathrm{Var}(\bar{x}) / \gamma_0$')
    ax[1].plot(grid, size, color=st.Forest, label='asymptotic size of the naive 5% t-test')
    ax[1].axhline(0.05, color=st.Amber, ls='--', lw=1, label='nominal 5%')
    ax[1].set_xlabel(r'AR(1) coefficient $\phi$')
    ax[1].set_ylabel('rejection probability under H0')
    for a in ax:
        st.legend_outside_bottom(a, ncol=1, y=-0.2)
    plt.tight_layout()
    save('ats_ch0_lrv_ar1', save_it)
    f = lambda p: (1 + p) / (1 - p)
    sz = lambda p: 2 * (1 - stats.norm.cdf(1.96 / np.sqrt(f(p))))
    out = {'T': T, 'reps': reps, 'sim': dict(zip([str(p) for p in phis], [float(s) for s in sim])),
           'f05': f(0.5), 'f09': f(0.9), 'fm05': f(-0.5), 'size03': sz(0.3), 'size05': sz(0.5), 'size09': sz(0.9),
           'sizem05': sz(-0.5), 'sim05': float(sim[list(phis).index(0.5)]), 'sim09': float(sim[list(phis).index(0.9)])}
    NUM['lrv'] = out
    return out


def fig_kernels(save_it=True):
    """The kernels k(x) of Newey-West (Bartlett), Parzen and quadratic spectral, with the truncated kernel."""
    x = np.linspace(0, 2.2, 400)
    fig, ax = plt.subplots(figsize=(9.5, 4))
    for kind, c, lab in (('truncated', st.Amber, 'truncated (Hansen-Hodrick)'), ('bartlett', st.MainBlue, 'Bartlett (Newey-West)'),
                         ('parzen', st.Forest, 'Parzen'), ('qs', st.IDAred, 'quadratic spectral (Andrews)')):
        ax.plot(x, kernel(x, kind), color=c, label=lab, lw=1.8)
    ax.axhline(0, color=st.DarkText, lw=0.6)
    ax.set_xlabel(r'$x = j / S$ (lag over bandwidth)')
    ax.set_ylabel(r'weight $k(x)$')
    st.legend_outside_bottom(ax, ncol=4, y=-0.2)
    save('ats_ch0_kernels', save_it)
    out = {'qs_min': float(kernel(np.linspace(0, 5, 5001), 'qs').min())}
    NUM['kern'] = out
    return out


def truncated_negative_example():
    """A sample whose truncated-kernel long-run variance is negative while the Bartlett estimate is positive."""
    x = np.array([1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 2.0, -2.0])
    g = acov_all(x)
    return {'g0': float(g[0]), 'g1': float(g[1]), 'g2': float(g[2]), 'trunc_S2': float(g[0] + 2 * g[1] + 2 * g[2]),
            'trunc_S1': float(g[0] + 2 * g[1]), 'bart_S2': float(lrv(x, 2.0)), 'bart_S3': float(lrv(x, 3.0))}


# =============================================================================
# 3. HAC IN PRACTICE: BANDWIDTH, FIXED-b
# =============================================================================
def fig_hac_bandwidth(save_it=True):
    """HAC standard error of the mean relative to the naive one, as a function of the Bartlett bandwidth."""
    d = daily_series()
    ser = {'S&P 500 returns': d['S&P 500 returns'], 'S&P 500 squared returns': d['S&P 500 squared returns'],
           'EUR/RON returns': d['EUR/RON returns'], 'RO HICP inflation': ro_inflation(),
           'RO GDP growth': ro_gdp_growth()}
    cols = [st.MainBlue, st.IDAred, st.Forest, st.Orange, st.Purple]
    Ss = np.unique(np.round(np.geomspace(1, 400, 60)))
    fig, ax = plt.subplots(figsize=(10.5, 4.4))
    out = {}
    for (name, x), c in zip(ser.items(), cols):
        x = x.values
        T = len(x)
        g0 = acov_all(x)[0]
        Sv = Ss[Ss <= T / 2]
        ratio = np.sqrt([lrv(x, S) / g0 for S in Sv])
        ax.plot(Sv, ratio, color=c, label=f'{name} (T = {T})')
        Sa = float(andrews_bw(x))
        ax.plot([Sa], [np.sqrt(lrv(x, Sa) / g0)], 'o', color=c, ms=6, label='_a')
        out[name] = {'T': T, 'S_and': Sa, 'r_and': float(np.sqrt(lrv(x, Sa) / g0)), 'S_nw': nw_rule(T),
                     'r_nw': float(np.sqrt(lrv(x, nw_rule(T)) / g0)), 'r_max': float(ratio.max()),
                     'S_max': float(Sv[np.argmax(ratio)])}
    ax.axhline(1, color=st.DarkText, lw=0.7, ls=':')
    ax.set_xscale('log')
    ax.set_xlabel('Bartlett bandwidth S (log scale); dots: Andrews (1991) AR(1) plug-in')
    ax.set_ylabel('HAC s.e. / naive s.e.')
    st.legend_outside_bottom(ax, ncol=3, y=-0.22)
    save('ats_ch0_hac_bandwidth', save_it)
    NUM['bw'] = out
    return out


def fig_fixed_b(save_it=True, cvtab=None, cvqs=None):
    """Fixed-b critical values (two-sided 5%) of the Bartlett and QS t-tests against b = S/T (Kiefer and Vogelsang 2005)."""
    cvtab = cvtab or fixed_b_table()
    cvqs = cvqs or fixed_b_table(kind='qs')
    bs = sorted(cvtab)
    fig, ax = plt.subplots(figsize=(9.5, 4))
    ax.plot([0] + bs, [1.96] + [cvtab[b] for b in bs], 'o-', color=st.MainBlue, label='Bartlett kernel')
    ax.plot([0] + bs, [1.96] + [cvqs[b] for b in bs], 's-', color=st.IDAred, label='quadratic spectral kernel')
    ax.axhline(1.96, color=st.Forest, ls='--', lw=1, label='standard normal critical value 1.96')
    ax.set_xlabel('b = S / T')
    ax.set_ylabel('5% two-sided critical value')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch0_fixed_b', save_it)
    out = {'bart': {str(b): v for b, v in cvtab.items()}, 'qs': {str(b): v for b, v in cvqs.items()}}
    NUM['fixedb'] = out
    return cvtab, cvqs


# =============================================================================
# 4. MONTE CARLO OF SIZE
# =============================================================================
def mc_size(phi, T, cvtab, reps=5000, B=399, breps=1000, seed=SEED):
    """Rejection rates at 5% of H0: mu = 0 for an AR(1) with N(0, 1) innovations, by method."""
    rng = np.random.default_rng(seed + int(1000 * phi) + T)
    e = rng.standard_normal((reps, T + 200))
    x = np.zeros_like(e)
    for t in range(1, e.shape[1]):
        x[:, t] = phi * x[:, t - 1] + e[:, t]
    x = x[:, 200:]
    m = x.mean(axis=1)
    g = acov_all(x)
    j = np.arange(1, T)
    t_of = lambda v: np.abs(np.sqrt(T) * m / np.sqrt(np.maximum(v, 1e-12)))
    S_nw = nw_rule(T)
    S_and = andrews_bw(x)
    S_qs = andrews_bw(x, 'qs')
    S_ll = llsw_bw(T)
    nu = ewc_nu(T)
    v_nw = g[:, 0] + 2 * (g[:, 1:] * kernel(j / S_nw)).sum(axis=1)
    v_and = g[:, 0] + 2 * (g[:, 1:] * kernel(j[None, :] / S_and[:, None])).sum(axis=1)
    v_qs = g[:, 0] + 2 * (g[:, 1:] * kernel(j[None, :] / S_qs[:, None], 'qs')).sum(axis=1)
    v_ll = g[:, 0] + 2 * (g[:, 1:] * kernel(j / S_ll)).sum(axis=1)
    out = {'naive': float((t_of(g[:, 0]) > 1.96).mean()), 'nw': float((t_of(v_nw) > 1.96).mean()),
           'andrews': float((t_of(v_and) > 1.96).mean()), 'qs': float((t_of(v_qs) > 1.96).mean()),
           'llsw': float((t_of(v_ll) > fixed_b_cv(S_ll / T, cvtab)).mean()),
           'ewc': float((t_of(ewc_lrv(x, nu)) > stats.t.ppf(0.975, nu)).mean())}
    rej = []
    for i in range(breps):
        b_sb, b_cb = politis_white(x[i])
        bm = mbb_means(x[i], b_cb, B, rng, circular=True)
        rej.append(abs(m[i]) > np.quantile(np.abs(bm - bm.mean()), 0.95))
    out['cbb'] = float(np.mean(rej))
    return out


def fig_mc_size(save_it=True, cvtab=None, reps=5000, breps=1000):
    """Monte Carlo size of the 5% t-test for a mean under AR(1) dependence, T = 100 and T = 400."""
    cvtab = cvtab or fixed_b_table()
    phis = (0.0, 0.3, 0.5, 0.7, 0.9)
    res = {T: {p: mc_size(p, T, cvtab, reps=reps, breps=breps) for p in phis} for T in (100, 400)}
    lab = {'naive': 'naive (i.i.d.)', 'nw': 'NW, rule of thumb', 'andrews': 'NW, Andrews bandwidth',
           'qs': 'QS, Andrews bandwidth', 'llsw': 'NW, S = 1.3 sqrt(T), fixed-b', 'ewc': 'EWC, t critical values',
           'cbb': 'circular block bootstrap'}
    cols = dict(zip(lab, [st.IDAred, st.Orange, st.Amber, st.Purple, st.MainBlue, st.Forest, st.Teal]))
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.4), sharey=True)
    for a, T in zip(ax, (100, 400)):
        for k in lab:
            a.plot(phis, [res[T][p][k] for p in phis], 'o-', color=cols[k], label=lab[k], ms=4)
        a.axhline(0.05, color=st.DarkText, ls=':', lw=1)
        a.set_title(f'T = {T}')
        a.set_xlabel(r'AR(1) coefficient $\phi$')
    ax[0].set_ylabel('rejection rate under H0 (nominal 5%)')
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch0_mc_size', save_it)
    out = {str(T): {str(p): res[T][p] for p in phis} for T in res}
    NUM['mc'] = {'res': out, 'reps': reps, 'breps': breps}
    return out


# =============================================================================
# 5. BLOCK BOOTSTRAP ON REAL DATA
# =============================================================================
def fig_bootstrap(save_it=True, B=1999):
    """Bootstrap distributions of the mean of S&P 500 squared returns: i.i.d., moving-block, stationary."""
    rng = np.random.default_rng(SEED)
    x = daily_series()['S&P 500 squared returns'].values
    T = len(x)
    b_sb, b_cb = politis_white(x)
    m_iid = iid_means(x, B, rng)
    m_mbb = mbb_means(x, b_cb, B, rng)
    m_cbb = mbb_means(x, b_cb, B, rng, circular=True)
    idx = sb_indices(T, b_sb, B, rng)
    m_sb = x[idx].mean(axis=1)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    bins = np.linspace(min(m_iid.min(), m_sb.min()), max(m_iid.max(), m_sb.max()), 70)
    ax.hist(m_iid, bins=bins, color=st.Amber, alpha=0.6, density=True, label='i.i.d. bootstrap (Efron)')
    ax.hist(m_mbb, bins=bins, histtype='step', color=st.MainBlue, lw=1.8, density=True,
            label=f'moving-block bootstrap, l = {int(round(b_cb))}')
    ax.hist(m_sb, bins=bins, histtype='step', color=st.IDAred, lw=1.8, density=True,
            label=f'stationary bootstrap, mean block {b_sb:.0f}')
    ax.axvline(x.mean(), color=st.Forest, ls='--', lw=1.2, label='sample mean')
    ax.set_xlabel('bootstrap mean of squared daily returns (%²)')
    st.legend_outside_bottom(ax, ncol=2, y=-0.2)
    save('ats_ch0_bootstrap', save_it)
    g0 = acov_all(x)[0]
    out = {'T': T, 'mean': float(x.mean()), 'b_sb': b_sb, 'b_cb': b_cb, 'se_naive': float(np.sqrt(g0 / T)),
           'se_iid': float(m_iid.std()), 'se_mbb': float(m_mbb.std()), 'se_cbb': float(m_cbb.std()),
           'se_sb': float(m_sb.std()), 'se_and': float(np.sqrt(lrv(x, andrews_bw(x)) / T)),
           'se_qs': float(np.sqrt(lrv(x, andrews_bw(x, 'qs'), 'qs') / T)),
           'mbb_bias': float(m_mbb.mean() - x.mean()), 'cbb_bias': float(m_cbb.mean() - x.mean())}
    NUM['boot'] = out
    return out


def fig_block_length(save_it=True, B=999):
    """Bootstrap standard error of the mean against the block length (circular block bootstrap), three series."""
    rng = np.random.default_rng(SEED + 1)
    d = daily_series()
    ser = {'S&P 500 squared returns': d['S&P 500 squared returns'], 'RO HICP inflation': ro_inflation(),
           'RO GDP growth': ro_gdp_growth()}
    cols = [st.IDAred, st.Orange, st.Purple]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    out = {}
    for (name, x), c in zip(ser.items(), cols):
        x = x.values
        T = len(x)
        se0 = np.sqrt(acov_all(x)[0] / T)
        ls = np.unique(np.round(np.geomspace(1, T / 4, 25))).astype(int)
        r = [mbb_means(x, l, B, rng, circular=True).std() / se0 for l in ls]
        ax.plot(ls, r, 'o-', ms=3, color=c, label=f'{name} (T = {T})')
        b_sb, b_cb = politis_white(x)
        out[name] = {'T': T, 'b_sb': b_sb, 'b_cb': b_cb,
                     'r_pw': float(mbb_means(x, b_cb, B, rng, circular=True).std() / se0)}
    ax.axhline(1, color=st.DarkText, ls=':', lw=0.8)
    ax.set_xscale('log')
    ax.set_xlabel('block length l (log scale)')
    ax.set_ylabel('bootstrap s.e. / naive s.e.')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch0_block_length', save_it)
    NUM['blk'] = out
    return out


def real_data_table(cvtab=None, B=1999):
    """Mean, standard errors and confidence intervals by method for six series of the chapter."""
    cvtab = cvtab or fixed_b_table()
    rng = np.random.default_rng(SEED + 2)
    d = daily_series()
    ser = {'sp': d['S&P 500 returns'], 'sq': d['S&P 500 squared returns'], 'bet': d['BET returns'],
           'eur': d['EUR/RON returns'], 'gdp': ro_gdp_growth(), 'infl': ro_inflation()}
    out = {}
    for k, x in ser.items():
        x = x.values
        r = mean_inference(x, cvtab)
        b_sb, b_cb = politis_white(x)
        idx = sb_indices(len(x), b_sb, B, rng)
        r['se_sb'] = float(x[idx].mean(axis=1).std())
        r['b_sb'] = b_sb
        r['ratio_and'] = r['se_andrews'] / r['se_naive']
        r['ratio_sb'] = r['se_sb'] / r['se_naive']
        out[k] = r
    NUM['tab'] = out
    return out


# =============================================================================
# 6. OVERLAPPING OBSERVATIONS: THE TERM SPREAD AND FUTURE GROWTH
# =============================================================================
def ols_hac(y, X, S=None, kind='bartlett'):
    """OLS with the sandwich covariance (X'X)^-1 T Omega (X'X)^-1; Omega the kernel long-run variance of x_t u_t."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    T = len(y)
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    h = X * u[:, None]
    if S is None:
        Om = h.T @ h / T
    else:
        Om = h.T @ h / T
        for j in range(1, T):
            w = kernel(j / S, kind)
            if w == 0 and kind != 'qs':
                break
            G = h[j:].T @ h[:-j] / T
            Om += w * (G + G.T)
    V = T * XtX_inv @ Om @ XtX_inv
    return beta, np.sqrt(np.diag(V)), u


def fig_term_spread(save_it=True, cvtab=None, h=H_TS):
    """Annualised US real GDP growth over the next four quarters on the 10-year minus 3-month Treasury spread:
    OLS, White, Newey-West (h lags), Andrews and fixed-b standard errors; residual autocorrelation."""
    cvtab = cvtab or fixed_b_table()
    d = term_spread_data(h)
    y, X = d['growth'].values, np.column_stack([np.ones(len(d)), d['spread'].values])
    T = len(y)
    b, se_ols, u = ols_hac(y, X)
    s2 = u @ u / (T - 2)
    se_classic = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    _, se_nw, _ = ols_hac(y, X, S=h)            # Bartlett with h - 1 = 3 lags: S = h
    _, se_hh, _ = ols_hac(y, X, S=h - 1 + 1e-9, kind='truncated')   # Hansen-Hodrick: truncated kernel, h - 1 lags
    Sa = float(andrews_bw(u * (X[:, 1] - X[:, 1].mean())))
    _, se_and, _ = ols_hac(y, X, S=Sa)
    S_ll = llsw_bw(T)
    _, se_ll, _ = ols_hac(y, X, S=S_ll)
    g = acov_all(u)
    rho = g[1:13] / g[0]
    sub = {}
    for lab, (a, z) in {'early': ('1962-01-01', '1988-12-31'), 'late': ('1989-01-01', '2030-01-01')}.items():
        dd = d.loc[a:z]
        bb, ss, _ = ols_hac(dd['growth'].values, np.column_stack([np.ones(len(dd)), dd['spread'].values]), S=h)
        sub[lab] = {'b': float(bb[1]), 'se': float(ss[1]), 't': float(bb[1] / ss[1]), 'n': len(dd)}
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.3), gridspec_kw={'width_ratios': [1.6, 1]})
    ax[0].plot(d.index, d['growth'], color=st.MainBlue, label='US real GDP growth over the next 4 quarters (% p.a.)')
    ax[0].plot(d.index, d['spread'], color=st.IDAred, label='10-year minus 3-month Treasury spread (pp)')
    ax[0].axhline(0, color=st.DarkText, lw=0.6)
    st.legend_outside_bottom(ax[0], ncol=1, y=-0.15)
    ax[1].bar(np.arange(1, 13), rho, color=st.Forest, width=0.6, label='ACF of the OLS residuals')
    ax[1].axhspan(-1.96 / np.sqrt(T), 1.96 / np.sqrt(T), color=st.MainBlue, alpha=0.12, lw=0)
    ax[1].axvline(h - 0.5, color=st.Amber, ls='--', lw=1, label=f'overlap: lags 1 to {h - 1}')
    ax[1].set_xlabel('lag (quarters)')
    st.legend_outside_bottom(ax[1], ncol=1, y=-0.2)
    plt.tight_layout()
    save('ats_ch0_term_spread', save_it)
    out = {'T': T, 'first': str(d.index[0].date()), 'last': str(d.index[-1].date()), 'b0': float(b[0]), 'b1': float(b[1]),
           'se_classic': float(se_classic[1]), 'se_white': float(se_ols[1]), 'se_nw': float(se_nw[1]),
           'se_hh': float(se_hh[1]), 'se_and': float(se_and[1]), 'S_and': Sa, 'se_ll': float(se_ll[1]), 'S_ll': S_ll,
           'cv_ll': fixed_b_cv(S_ll / T, cvtab), 'rho1': float(rho[0]), 'rho3': float(rho[2]), 'rho4': float(rho[3]),
           'rho8': float(rho[7]), 'r2': float(1 - u @ u / ((y - y.mean()) @ (y - y.mean()))), 'sub': sub}
    out['t_classic'] = out['b1'] / out['se_classic']
    out['t_nw'] = out['b1'] / out['se_nw']
    out['t_and'] = out['b1'] / out['se_and']
    out['t_ll'] = out['b1'] / out['se_ll']
    NUM['ts'] = out
    return out


# =============================================================================
# 7. DATA SNOOPING
# =============================================================================
def fig_snooping(save_it=True, reps=20000):
    """Probability that the best of K tests rejects at 5% when every null is true: independent tests and
    equicorrelated test statistics (correlation 0.5 and 0.9)."""
    rng = np.random.default_rng(SEED)
    Ks = np.array([1, 2, 5, 10, 20, 50, 100, 200, 500])
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    ax.plot(Ks, 1 - 0.95 ** Ks, 'o-', color=st.IDAred, label='independent tests: 1 - 0.95^K')
    out = {'indep': {str(k): float(1 - 0.95 ** k) for k in Ks}}
    for rho, c in ((0.5, st.MainBlue), (0.9, st.Forest)):
        z0 = rng.standard_normal((reps, 1))
        fw = []
        for K in Ks:
            z = np.sqrt(rho) * z0 + np.sqrt(1 - rho) * rng.standard_normal((reps, K))
            fw.append(float((np.abs(z).max(axis=1) > 1.96).mean()))
        ax.plot(Ks, fw, 's-', color=c, label=f'equicorrelated statistics, correlation {rho}')
        out[str(rho)] = dict(zip([str(k) for k in Ks], fw))
    ax.axhline(0.05, color=st.DarkText, ls=':', lw=1)
    ax.set_xscale('log')
    ax.set_xlabel('number of tests K (log scale)')
    ax.set_ylabel('P(at least one rejection | all nulls true)')
    st.legend_outside_bottom(ax, ncol=2, y=-0.2)
    save('ats_ch0_snooping', save_it)
    out['bonf20'] = 0.05 / 20
    NUM['snoop'] = out
    return out


def ma_rule_returns(price, lengths=MA_LENGTHS):
    """Excess daily log returns (%) of the moving-average rules over buy-and-hold: the rule is in the index on day t
    if the close of day t-1 is above its n-day moving average, otherwise out of the market (zero return), so
    f_t = (s_{t-1} - 1) r_t; no transaction costs."""
    r = 100 * np.log(price).diff()
    out = {}
    for n in lengths:
        sig = (price > price.rolling(n).mean()).astype(float).shift(1)
        out[n] = (sig - 1) * r
    df = pd.DataFrame(out).iloc[max(lengths) + 1:].dropna()
    return df


def reality_check(f, B=999, mean_block=SB_MEAN_BLOCK, seed=SEED):
    """White (2000) Reality Check: V = max_k sqrt(n) mean(f_k); bootstrap V* = max_k sqrt(n) (mean(f*_k) - mean(f_k))
    with the stationary bootstrap; p-value = share of V* above V. Also the naive p-value of the best rule alone."""
    rng = np.random.default_rng(seed)
    F = np.asarray(f, float)
    n = F.shape[0]
    fbar = F.mean(axis=0)
    V = np.sqrt(n) * fbar.max()
    idx = sb_indices(n, mean_block, B, rng)
    Vs = np.empty(B)
    for i in range(B):
        Vs[i] = np.sqrt(n) * (F[idx[i]].mean(axis=0) - fbar).max()
    kbest = int(np.argmax(fbar))
    x = F[:, kbest]
    se = np.sqrt(lrv(x, nw_rule(n)) / n)
    return {'V': float(V), 'p_rc': float((Vs > V).mean()), 'best': kbest, 'best_mean': float(fbar[kbest]),
            't_best': float(fbar[kbest] / se), 'p_naive': float(1 - stats.norm.cdf(fbar[kbest] / se)), 'n': n,
            'K': F.shape[1], 'n_sig': int((fbar / np.sqrt(lrv(F.T, nw_rule(n)) / n) > 1.645).sum()), 'Vs': Vs}


def fig_reality_check(save_it=True, B=999):
    """Reality Check of White (2000) for 50 moving-average rules on the BET index, two subsamples."""
    p = load_close('bet')
    out = {}
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.2))
    for a, (lab, (s, e)) in zip(ax, {'2000-2012': ('2000-01-01', '2012-12-31'),
                                     '2013-2026': ('2013-01-01', '2026-12-31')}.items()):
        f = ma_rule_returns(p.loc[s:e])
        rc = reality_check(f.values, B=B)
        rc['first'], rc['last'] = str(f.index[0].date()), str(f.index[-1].date())
        rc['best_n'] = int(f.columns[rc['best']])
        a.hist(rc.pop('Vs'), bins=40, color=st.MainBlue, alpha=0.7, label='bootstrap distribution of V* (H0)')
        a.axvline(rc['V'], color=st.IDAred, lw=2, label=f"observed V = {rc['V']:.2f}; Reality Check p = {rc['p_rc']:.2f}")
        a.set_title(f'BET, {lab}: best rule MA({rc["best_n"]})')
        a.set_xlabel(r'$\max_k \sqrt{n}\,\bar f_k$')
        st.legend_outside_bottom(a, ncol=1, y=-0.2)
        out[lab] = rc
    plt.tight_layout()
    save('ats_ch0_reality_check', save_it)
    NUM['rc'] = out
    return out


# =============================================================================
# 8. AI MINI-CASE: MEAN INFLATION AGAINST THE TARGET
# =============================================================================
def fig_ai_minicase(save_it=True, cvtab=None, reps=5000):
    """Mean Romanian HICP inflation since 2013 against 2.5%: confidence intervals by method, and the size of each
    test in a Monte Carlo calibrated to the AR(1) fitted to the series."""
    cvtab = cvtab or fixed_b_table()
    x = ro_inflation(TARGET_START).values
    T = len(x)
    r = mean_inference(x, cvtab, mu0=TARGET)
    phi = float(ar1_coef(x))
    mc = mc_size(phi, T, cvtab, reps=reps, breps=500)
    lab = {'naive': 'naive', 'nw': 'NW rule of thumb', 'andrews': 'NW Andrews', 'qs': 'QS Andrews',
           'llsw': 'NW fixed-b (LLSW)', 'ewc': 'EWC (LLSW)'}
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.3), gridspec_kw={'width_ratios': [1.3, 1]})
    for i, k in enumerate(lab):
        ax[0].plot([r[f'lo_{k}'], r[f'hi_{k}']], [i, i], color=st.MainBlue, lw=3, solid_capstyle='butt',
                   label='95% interval for the mean' if i == 0 else '_')
    ax[0].plot([r['mean']] * len(lab), range(len(lab)), 'o', color=st.IDAred, label=f"sample mean {r['mean']:.2f}%")
    ax[0].axvline(TARGET, color=st.Forest, ls='--', label='target 2.5%')
    ax[0].set_yticks(range(len(lab)))
    ax[0].set_yticklabels(list(lab.values()))
    ax[0].set_xlabel('mean annual HICP inflation, %')
    st.legend_outside_bottom(ax[0], ncol=2, y=-0.2)
    keys = list(lab) + ['cbb']
    ax[1].barh(range(len(keys)), [mc[k] for k in keys], color=st.Amber, label=f'size in AR(1) Monte Carlo, phi = {phi:.2f}, T = {T}')
    ax[1].axvline(0.05, color=st.DarkText, ls=':', lw=1)
    ax[1].set_yticks(range(len(keys)))
    ax[1].set_yticklabels(list(lab.values()) + ['circular block bootstrap'])
    ax[1].set_xlabel('rejection rate under H0 (nominal 5%)')
    st.legend_outside_bottom(ax[1], ncol=1, y=-0.2)
    plt.tight_layout()
    save('ats_ch0_ai_minicase', save_it)
    out = dict(r, phi=phi, mc=mc, first=TARGET_START, last=str(ro_inflation().index[-1].date()))
    NUM['ai'] = out
    return out


def main():
    st.apply()
    fig_data_dashboard()
    fig_acf_panel()
    fig_lrv_ar1()
    fig_kernels()
    NUM['neg'] = truncated_negative_example()
    cvtab, cvqs = fig_fixed_b()
    fig_hac_bandwidth()
    fig_mc_size(cvtab=cvtab)
    fig_bootstrap()
    fig_block_length()
    real_data_table(cvtab=cvtab)
    fig_term_spread(cvtab=cvtab)
    fig_snooping()
    fig_reality_check()
    fig_ai_minicase(cvtab=cvtab)
    with open(os.path.join(HERE, 'ch0_numbers.json'), 'w') as f:
        json.dump(NUM, f, indent=1, default=float)
    print('numbers written to', os.path.join(HERE, 'ch0_numbers.json'))


if __name__ == '__main__':
    main()
