"""
generate_all_charts.py -- charts and numbers of Chapter 7 (ATS): regime-switching models
=========================================================================================
Course data (ats_data.py), chart style (ats_style.py), the numpy engine ms_core.py. Every number on the slides comes
from here.
  * Hamilton (1989)          -- the switching-mean AR(4) on Hamilton's own data set (real GNP 1951Q2-1984Q4, distributed
                                with statsmodels), by numerical ML in numpy and with statsmodels MarkovAutoregression;
                                the same specification on today's real GDP (FRED GDPC1) against the NBER dates (USRECQ);
                                pseudo-real-time filtered probabilities 1990-2026 (Chauvet and Piger 2008);
  * EM (Hamilton 1990)       -- paths of the log-likelihood from many starting values, local and degenerate maxima;
  * number of regimes        -- information criteria and a parametric bootstrap of the likelihood-ratio statistic
                                (nuisance parameters unidentified under the null: Hansen 1992, Garcia 1998);
  * TVTP                     -- Filardo (1994): US industrial production with transition probabilities driven by the
                                leading indicator (data distributed with statsmodels), numpy and statsmodels;
  * MS-VAR                   -- MSIAH(2)-VAR(1) for US GDP growth and the change of unemployment, regime-dependent
                                impulse responses (Krolzig 1997; Ehrmann, Ellison and Valla 2003);
  * MS-GARCH                 -- S&P 500 daily returns: GARCH(1,1) against the Markov-switching GARCH of Haas, Mittnik and
                                Paolella (2004) and of Gray (1996);
  * bull and bear markets    -- weekly S&P 500 and BET returns, two regimes in mean and variance; Ang and Bekaert (2002)
                                regime-dependent allocation;
  * Bayesian estimation      -- Gibbs sampling with forward filtering-backward sampling (Chib 1996) on Romanian GDP
                                growth, with and without the random permutation sampler (label switching);
  * long memory              -- Diebold and Inoue (2001): rare regime switches look like long memory (GPH estimates);
  * Romanian inflation       -- HICP (Eurostat), three regimes since 1997, against a change-point model (Chib 1998);
  * EUR/RON                  -- weekly changes, volatility regimes around the 2005 float and the 2025 depreciation;
  * forecasting              -- recursive one-step density forecasts of US GDP growth, AR(1) against MSIH(2)-AR(1);
  * AI mini-case             -- how robust is a recession dating across defensible specifications.
Output: charts/ats_ch7_*.pdf/.png, Quantlets/Ch_07/ch7_numbers.json
Run:  python3 Quantlets/Ch_07/generate_all_charts.py [name ...]
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
from ats_data import load_close, read_ecb, read_eurostat, read_fred, read_reference_rate   # noqa: E402
import ats_style as st                                                                   # noqa: E402
from ms_core import (acf, best_em, concordance, em_msr, em_msvar, ergodic, gibbs_ms, gph, hamilton_filter,  # noqa: E402
                     info_criteria, kim_smoother, lag_design, linear_ar, mixture_logscore, mixture_pit,
                     msgarch_fit, msm_filter, msm_fit, msr_logf, order_regimes, qps, regime_irf, simulate_chain,
                     var_design)

warnings.filterwarnings('ignore')
SEED = 2026
RO_HICP = ('prc_hicp_minr', 'M.I25.TOTAL.RO')           # Romanian HICP, index 2025 = 100 (Eurostat)
RO_GDP = ('namq_10_gdp', 'Q.CLV10_MEUR.SCA.B1GQ.RO')    # Romanian real GDP, seasonally and calendar adjusted
US = dict(start='1947-04-01', est_end='2019-10-01', ham_start='1952-04-01', end='2026-04-01')
MARKET = dict(start='2000-01-01', end='2026-09-18')
EVENTS_EURRON = [('2005-07-01', 'RON redenomination'), ('2008-10-01', 'October 2008'), ('2025-05-01', 'May 2025')]
_FILES = {}


# =============================================================================
# DATA
# =============================================================================
def cached(key, fn):
    if key not in _FILES:
        _FILES[key] = fn()
    return _FILES[key]


def save(name, save_it=True):
    if save_it:
        st.check_no_grey(plt.gcf())
        st.save_fig(name)
    else:
        plt.show()


def hamilton_gnp():
    """Hamilton's (1989) data: 100 x change of log real GNP, 1951Q2-1984Q4 (as distributed with statsmodels)."""
    from statsmodels.tsa.regime_switching.tests.test_markov_autoregression import rgnp
    return pd.Series(np.asarray(rgnp, float), index=pd.period_range('1951Q2', periods=len(rgnp), freq='Q').to_timestamp(),
                     name='rgnp')


def filardo_data():
    """Filardo's (1994) data: monthly growth of US industrial production (dlip) and of the composite leading indicator
    (dmdlleading), 1948-1991 (as distributed with statsmodels)."""
    import statsmodels
    p = os.path.join(os.path.dirname(statsmodels.__file__), 'tsa', 'regime_switching', 'tests', 'results', 'mar_filardo.csv')
    d = pd.read_csv(p)[['dlip', 'dmdlleading']]
    d.index = pd.date_range('1948-01-01', periods=len(d), freq='MS')
    return d


def us_gdp():
    """US real GDP growth (100 x change of log GDPC1, % per quarter) and the NBER recession quarters (USRECQ)."""
    def get():
        g = read_fred('GDPC1')
        y = (100 * np.log(g).diff()).dropna().rename('gdp')
        rec = read_fred('USRECQ').reindex(y.index).fillna(0).astype(int)
        return y, rec
    return cached('us_gdp', get)


def us_unemp_q():
    return cached('us_u', lambda: read_fred('UNRATE').resample('QS').mean())


def ro_gdp():
    g = cached('ro_gdp', lambda: read_eurostat(*RO_GDP))
    return (100 * np.log(g).diff()).dropna().rename('ro_gdp')


def ro_inflation():
    """Romanian annual HICP inflation, 100 x log(P_t / P_{t-12}), monthly from January 1997."""
    p = cached('ro_hicp', lambda: read_eurostat(*RO_HICP))
    return (100 * np.log(p).diff(12)).dropna().rename('ro_infl')


def weekly_returns(name, start=MARKET['start'], end=MARKET['end']):
    """Weekly log returns (%), Friday closes (last trading day of each week)."""
    p = load_close(name, start, end).resample('W-FRI').last().dropna()
    return (100 * np.log(p).diff()).dropna().rename(name)


def eurron_daily():
    """EUR/RON: ECB euro reference rate for the leu before July 2005 (old lei rescaled to RON), official BNR reference
    rate from 1 July 2005 (redenomination)."""
    def get():
        ecb = read_ecb('EXR', 'D.RON.EUR.SP00.A').loc[:'2005-06-30']
        bnr = read_reference_rate('EUR', start='2005-07-01')
        return pd.concat([ecb, bnr]).sort_index().rename('eurron')
    return cached('eurron', get)


def shade(ax, ind, color=st.Amber, alpha=0.2):
    """Shade the periods where the 0/1 indicator equals 1 (date index)."""
    ind = ind.astype(int)
    on = False
    idx = ind.index
    for i, v in enumerate(ind.values):
        if v and not on:
            s, on = idx[i], True
        if on and (not v or i == len(ind) - 1):
            ax.axvspan(s, idx[i], color=color, alpha=alpha, lw=0, label='_shade')
            on = False


def patch(color, alpha=0.2):
    from matplotlib.patches import Patch
    return Patch(color=color, alpha=alpha)


# =============================================================================
# 1. HAMILTON (1989): REPLICATION AND TODAY'S DATA
# =============================================================================
def fit_hamilton(y, nrand=8, seed=SEED):
    """Hamilton's switching-mean AR(4) by numerical ML (numpy), regimes ordered so that regime 0 is the low mean."""
    r = msm_fit(np.asarray(y, float), 4, nrand=nrand, seed=seed)
    if r['mu'][0] > r['mu'][1]:
        th = r['theta'].copy()
        th[[0, 1]] = th[[1, 0]]
        th[-2:] = th[-2:][::-1]
        r = msm_fit(np.asarray(y, float), 4, starts=[th], nrand=0)
    return r


def fig_hamilton(save_it=True):
    """Left: Hamilton's data, smoothed probability of the low-growth regime against the NBER recessions.
    Right: the same specification estimated on today's GDP (1952Q2-2019Q4), probabilities through 2026."""
    import statsmodels.api as sm
    y0 = hamilton_gnp()
    r0 = fit_hamilton(y0)
    smr = sm.tsa.MarkovAutoregression(y0.values, k_regimes=2, order=4, switching_ar=False).fit(search_reps=20, disp=False)
    pr = np.asarray(smr.params)
    sm_low = int(np.argmin(pr[2:4]))
    sm_smooth = np.asarray(smr.smoothed_marginal_probabilities)[:, sm_low]
    y, rec = us_gdp()
    ye = y.loc[US['ham_start']:US['est_end']]
    r1 = fit_hamilton(ye)
    yall = y.loc[US['ham_start']:US['end']]
    f, Pe, tup = msm_filter(r1['theta'], yall.values, 2, 4)
    sm_all, _ = kim_smoother(f['filt'], f['pred'], Pe)
    low_all = sm_all[:, tup[:, 0] == 0].sum(1)
    filt_all = f['filt'][:, tup[:, 0] == 0].sum(1)
    idx0 = y0.index[4:]
    idx1 = yall.index[4:]
    rec0 = rec.reindex(idx0).fillna(0)
    rec1 = rec.reindex(idx1)
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9), gridspec_kw=dict(width_ratios=[1, 1.5]))
    for ax, idx, p, rr, title in ((axs[0], idx0, r0['smooth'][:, 0], rec0, "Hamilton's data, 1952-1984"),
                                  (axs[1], idx1, low_all, rec1, 'Real GDP today, estimated 1953-2019')):
        shade(ax, rr)
        ax.plot(idx, p, color=st.MainBlue, lw=1.4, label='smoothed probability of the low-growth regime')
        ax.set_ylim(-0.02, 1.02)
        ax.set_title(title)
    axs[0].plot(idx0, sm_smooth, ':', color=st.IDAred, lw=1.6, label='statsmodels MarkovAutoregression')
    h, l = axs[0].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h + [patch(st.Amber)], l + ['NBER recessions'], ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch7_hamilton89', save_it)
    est = (rec1.loc[:US['est_end']].values == 1)
    p_est = low_all[:len(est)]
    starts = []
    rc = rec1.values
    for i in range(1, len(rc)):
        if rc[i] == 1 and rc[i - 1] == 0:
            first = next((j for j in range(i - 2, min(i + 8, len(rc))) if low_all[j] > 0.5), None)
            starts.append(dict(nber=str(idx1[i].to_period('Q')), model=str(idx1[first].to_period('Q')) if first is not None else 'none'))
    return dict(
        paper=dict(mu=r0['mu'].tolist(), phi=r0['phi'].tolist(), sigma=float(np.sqrt(r0['sig2'])),
                   p00=float(r0['P'][0, 0]), p11=float(r0['P'][1, 1]), loglik=r0['loglik'], se=r0['se_theta'].tolist(),
                   dur=[1 / (1 - r0['P'][0, 0]), 1 / (1 - r0['P'][1, 1])], T=int(len(y0) - 4)),
        sm=dict(loglik=float(smr.llf), mu=pr[2:4].tolist(), sigma=float(np.sqrt(pr[4])), phi=pr[5:9].tolist(),
                p00=float(pr[0]), p11=float(1 - pr[1]), maxdiff=float(np.max(np.abs(sm_smooth - r0['smooth'][:, 0])))),
        qps_paper=qps(r0['smooth'][:, 0], rec0.values), conc_paper=concordance(r0['smooth'][:, 0] > 0.5, rec0.values),
        today=dict(mu=r1['mu'].tolist(), phi=r1['phi'].tolist(), sigma=float(np.sqrt(r1['sig2'])), p00=float(r1['P'][0, 0]),
                   p11=float(r1['P'][1, 1]), loglik=r1['loglik'], dur=[1 / (1 - r1['P'][0, 0]), 1 / (1 - r1['P'][1, 1])],
                   T=int(len(ye) - 4), qps=qps(p_est, est), conc=concordance(p_est > 0.5, est),
                   nrec=int(est.sum()), p2020=float(low_all[list(idx1).index(pd.Timestamp('2020-04-01'))]),
                   p2008=float(low_all[list(idx1).index(pd.Timestamp('2008-10-01'))]),
                   p2001=float(low_all[list(idx1).index(pd.Timestamp('2001-07-01'))].max()),
                   p2001max=float(low_all[[list(idx1).index(pd.Timestamp(d)) for d in ('2001-01-01', '2001-04-01', '2001-07-01', '2001-10-01')]].max()),
                   last=float(low_all[-1]), lastq=str(idx1[-1].to_period('Q')), filt_last=float(filt_all[-1])),
        starts=starts)


def fig_realtime(save_it=True, step=4, first='1990-01-01'):
    """Pseudo-real-time filtered probabilities (Chauvet and Piger 2008, without data vintages): Hamilton's model is
    re-estimated every `step` quarters on the data available then; each quarter's filtered probability uses only data
    up to that quarter."""
    y, rec = us_gdp()
    y = y.loc[US['ham_start']:US['end']]
    dates = y.loc[first:].index
    th = None
    out = []
    for i, d in enumerate(dates):
        if i % step == 0:
            yi = y.loc[:d]
            r = msm_fit(yi.values, 4, starts=[th] if th is not None else None, nrand=0 if th is not None else 8, seed=SEED)
            if r['mu'][0] > r['mu'][1]:
                r = fit_hamilton(yi, nrand=8)
            th = r['theta']
        f, Pe, tup = msm_filter(th, y.loc[:d].values, 2, 4)
        out.append(f['filt'][-1, tup[:, 0] == 0].sum())
    p = pd.Series(out, index=dates)
    full = fig_hamilton_probs()
    fig, ax = plt.subplots(figsize=(11, 3.6))
    shade(ax, rec.reindex(dates))
    ax.plot(dates, p.values, color=st.IDAred, lw=1.5, label='pseudo-real-time filtered probability')
    ax.plot(full.loc[first:].index, full.loc[first:].values, color=st.MainBlue, lw=1.2, ls='--',
            label='smoothed probability, full sample')
    ax.set_ylim(-0.02, 1.02)
    ax.set_ylabel('Pr(low-growth regime)')
    h, l = ax.get_legend_handles_labels()
    ax.legend(h + [patch(st.Amber)], l + ['NBER recessions'], loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
    save('ats_ch7_realtime', save_it)
    r_ = rec.reindex(dates).values
    signals = {}
    for lab, a, b in (('1990', '1990-07-01', '1991-10-01'), ('2001', '2001-01-01', '2002-01-01'),
                      ('2008', '2008-01-01', '2009-10-01'), ('2020', '2020-01-01', '2020-10-01')):
        w = p.loc[a:b]
        hit = w[w > 0.5]
        signals[lab] = dict(first=str(hit.index[0].to_period('Q')) if len(hit) else 'none', maxp=float(w.max()))
    pre = dates < pd.Timestamp('2020-01-01')
    return dict(qps=qps(p.values[pre], r_[pre]), qps_smooth=qps(full.reindex(dates).values[pre], r_[pre]),
                signals=signals, false=int(((p.values > 0.5) & (r_ == 0)).sum()), n=int(len(p)))


def fig_hamilton_probs():
    """Smoothed low-growth probability of Hamilton's model on today's GDP (estimated 1952Q2-2019Q4)."""
    def get():
        y, _ = us_gdp()
        r1 = fit_hamilton(y.loc[US['ham_start']:US['est_end']])
        yall = y.loc[US['ham_start']:US['end']]
        f, Pe, tup = msm_filter(r1['theta'], yall.values, 2, 4)
        sm_all, _ = kim_smoother(f['filt'], f['pred'], Pe)
        return pd.Series(sm_all[:, tup[:, 0] == 0].sum(1), index=yall.index[4:])
    return cached('ham_probs', get)


# =============================================================================
# 2. EM: LOCAL AND DEGENERATE MAXIMA
# =============================================================================
def fig_em(save_it=True, starts=30):
    """EM (Hamilton 1990) for an MSIH(2)-AR(1) on Hamilton's data from many random starting values: the path of the
    log-likelihood, and the solutions it converges to."""
    import statsmodels.api as sm
    y0 = hamilton_gnp()
    ys, X = lag_design(y0.values, 1)
    rng = np.random.default_rng(SEED)
    runs = [em_msr(ys, X, 2, switch=[True, False], rng=rng, maxit=3000, tol=1e-10) for _ in range(starts)]
    fins = np.array([r['loglik'] for r in runs])
    groups = np.unique(np.round(fins, 2))
    smr = sm.tsa.MarkovRegression(ys, k_regimes=2, exog=X[:, 1:], switching_exog=False, switching_variance=True).fit(
        search_reps=20, disp=False)
    fig, ax = plt.subplots(figsize=(10.5, 3.8))
    cols = [st.MainBlue, st.IDAred, st.Forest, st.Purple, st.Orange, st.Teal]
    for r in runs:
        g = int(np.argmin(np.abs(groups - round(r['loglik'], 2))))
        ax.plot(np.arange(1, len(r['path']) + 1), r['path'], color=cols[g % len(cols)], lw=0.9, alpha=0.8)
    for g, v in enumerate(groups):
        ax.plot([], [], color=cols[g % len(cols)], lw=2, label=f'converges to {v:.2f} ({int((np.round(fins, 2) == v).sum())} starts)')
    ax.set_xscale('log')
    lo = np.percentile([r['path'][0] for r in runs], 10)
    ax.set_ylim(lo, groups.max() + 1.5)
    ax.set_xlabel('EM iteration')
    ax.set_ylabel('log-likelihood')
    st.legend_outside_bottom(ax, ncol=2, y=-0.2)
    save('ats_ch7_em', save_it)
    best = runs[int(np.argmax(fins))]
    bo = order_regimes(best, 'var')
    deg = dict(sig2=bo['sig2'].tolist(), P=np.diag(bo['P']).tolist(), beta=bo['beta'][:, 0].tolist(),
               share=float(bo['smooth'][:, 0].mean()), n_hi=int((bo['smooth'][:, 0] > 0.5).sum()))
    good = [r for r in runs if abs(r['loglik'] - groups[groups < groups.max() - 0.5].max()) < 0.01] if (groups < groups.max() - 0.5).any() else []
    return dict(groups=groups.tolist(), counts=[int((np.round(fins, 2) == v).sum()) for v in groups],
                iters_med=float(np.median([r['iters'] for r in runs])), iters_max=int(max(r['iters'] for r in runs)),
                sm_llf=float(smr.llf), degenerate=deg, n=starts,
                second=dict(P=np.diag(good[0]['P']).tolist(), sig2=good[0]['sig2'].tolist(), beta=good[0]['beta'][:, 0].tolist()) if good else None)


# =============================================================================
# 3. THE NUMBER OF REGIMES: INFORMATION CRITERIA AND A PARAMETRIC BOOTSTRAP OF THE LR STATISTIC
# =============================================================================
def lr_bootstrap(y, p=1, B=199, starts=4, seed=SEED, maxit=400):
    """H0: Gaussian AR(p) (one regime); H1: MSIH(2)-AR(p). The LR statistic has no chi-square limit (the transition
    probabilities are not identified under H0 and the score is degenerate), so its null distribution is simulated:
    data from the estimated AR(p), both models re-estimated on every simulated sample."""
    y = np.asarray(y, float)
    ys, X = lag_design(y, p)
    r0 = linear_ar(ys, X)
    r1 = best_em(ys, X, 2, starts=10, switch=[True] + [False] * p, seed=seed)
    LR = 2 * (r1['loglik'] - r0['loglik'])
    rng = np.random.default_rng(seed)
    c, phi = r0['beta'][0], r0['beta'][1:]
    s = np.sqrt(r0['sig2'])
    sims = []
    for b in range(B):
        n = len(y) + 100
        z = np.zeros(n)
        e = rng.normal(0, s, n)
        z[:p] = np.mean(y)
        for t in range(p, n):
            z[t] = c + phi @ z[t - p:t][::-1] + e[t]
        z = z[100:]
        zs, Z = lag_design(z, p)
        l0 = linear_ar(zs, Z)['loglik']
        l1 = best_em(zs, Z, 2, starts=starts, switch=[True] + [False] * p, seed=seed + b + 1, order=None, maxit=maxit)['loglik']
        sims.append(max(0.0, 2 * (l1 - l0)))
    sims = np.array(sims)
    return dict(LR=float(LR), sims=sims, p=float((1 + (sims >= LR).sum()) / (B + 1)), q95=float(np.quantile(sims, 0.95)),
                r0=r0, r1=r1)


def regime_ic(y, p=1, Ks=(1, 2, 3), starts=15):
    y = np.asarray(y, float)
    ys, X = lag_design(y, p)
    out = {}
    for K in Ks:
        if K == 1:
            r = linear_ar(ys, X)
        else:
            r = best_em(ys, X, K, starts=starts, switch=[True] + [False] * p, seed=SEED)
        out[K] = dict(loglik=float(r['loglik']), npar=int(r['npar']), **info_criteria(r['loglik'], r['npar'], len(ys)))
    return out


def fig_lrtest(save_it=True, B=199):
    """US GDP growth 1947Q2-2019Q4: AR(1) against MSIH(2)-AR(1); the bootstrap distribution of the LR statistic
    compared with chi-square distributions with 2 and 4 degrees of freedom."""
    y, _ = us_gdp()
    y = y.loc[US['start']:US['est_end']]
    bt = lr_bootstrap(y.values, 1, B=B)
    ic = regime_ic(y.values)
    fig, ax = plt.subplots(figsize=(10.5, 3.8))
    ax.hist(bt['sims'], bins=30, density=True, color=st.MainBlue, alpha=0.55, label=f'bootstrap LR under H0 (B = {B})')
    xs = np.linspace(0.01, max(bt['sims'].max(), 16), 300)
    ax.plot(xs, stats.chi2.pdf(xs, 2), color=st.IDAred, lw=1.6, label='chi-square, 2 df')
    ax.plot(xs, stats.chi2.pdf(xs, 4), color=st.Forest, lw=1.6, ls='--', label='chi-square, 4 df')
    ax.axvline(bt['q95'], color=st.Purple, lw=1.2, ls=':', label='bootstrap 95% quantile')
    ax.set_xlabel('LR statistic')
    ax.set_xlim(0, max(bt['sims'].max(), 16) * 1.05)
    st.legend_outside_bottom(ax, ncol=4, y=-0.2)
    save('ats_ch7_lrtest', save_it)
    r1 = bt['r1']
    return dict(LR=bt['LR'], p=bt['p'], q95=bt['q95'], c2=float(stats.chi2.ppf(0.95, 2)), c4=float(stats.chi2.ppf(0.95, 4)),
                B=B, mean_sim=float(bt['sims'].mean()), share_zero=float((bt['sims'] < 1e-6).mean()),
                ic={str(k): v for k, v in ic.items()}, sig=np.sqrt(r1['sig2']).tolist(), P=np.diag(r1['P']).tolist(),
                mu=(r1['beta'][:, 0] / (1 - r1['beta'][0, 1])).tolist(), T=int(len(y) - 1))


# =============================================================================
# 4. TIME-VARYING TRANSITION PROBABILITIES: FILARDO (1994)
# =============================================================================
def fig_tvtp(save_it=True):
    """Filardo (1994): switching-mean AR(4) for US industrial production growth, Pr(S_t = i | S_{t-1} = i) logistic in
    the lagged growth of the leading indicator; numpy ML against statsmodels; constant transitions for comparison."""
    import statsmodels.api as sm
    d = filardo_data()
    y = d['dlip'].iloc[2:]
    z = d['dmdlleading'].iloc[1:-1]
    Z = np.column_stack([np.ones(len(z)), z.values])
    r = msm_fit(y.values, 4, Z=Z, nrand=10, seed=SEED)
    if r['mu'][0] > r['mu'][1]:
        th = r['theta'].copy()
        th[[0, 1]] = th[[1, 0]]
        th[-4:] = np.r_[th[-2:], th[-4:-2]]
        r = msm_fit(y.values, 4, Z=Z, starts=[th], nrand=0)
    rc = fit_hamilton(y)
    th = r['theta']
    start = np.r_[th[7], -th[9], th[8], -th[10], th[0:2], np.exp(th[6]), th[2:6]]     # statsmodels ordering
    smm = sm.tsa.MarkovAutoregression(y.values, k_regimes=2, order=4, switching_ar=False, exog_tvtp=sm.add_constant(z.values))
    smr = smm.fit(start_params=start, disp=False)
    sm_search = smm.fit(search_reps=20, disp=False)
    idx = y.index[4:]
    stay_exp = r['P'][4:, 1, 1]
    stay_rec = r['P'][4:, 0, 0]
    fig, axs = plt.subplots(2, 1, figsize=(11, 4.8), sharex=True)
    usrec = cached('usrec_m', lambda: read_fred('USREC'))
    shade(axs[0], usrec.reindex(idx).fillna(0))
    axs[0].plot(idx, r['smooth'][:, 0], color=st.MainBlue, lw=1.2, label='smoothed Pr(low-growth regime), TVTP')
    axs[0].set_ylim(-0.02, 1.02)
    axs[1].plot(idx, stay_exp, color=st.Forest, lw=1.0, label='Pr(stay in expansion), driven by the leading indicator')
    axs[1].plot(idx, stay_rec, color=st.Purple, lw=1.0, label='Pr(stay in recession)')
    axs[1].set_ylim(-0.02, 1.02)
    h, l = [], []
    for ax in axs:
        hh, ll = ax.get_legend_handles_labels()
        h += hh
        l += ll
    st.fig_legend_bottom(fig, h + [patch(st.Amber)], l + ['NBER recessions'], ncol=2, y=0.04)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch7_tvtp', save_it)
    rr = usrec.reindex(idx).fillna(0).values
    LR = 2 * (r['loglik'] - rc['loglik'])
    g = r['theta'][-4:]
    return dict(loglik=r['loglik'], loglik_const=rc['loglik'], LR=float(LR), pLR=float(stats.chi2.sf(LR, 2)),
                sm_llf=float(smr.llf), sm_search=float(sm_search.llf), mu=r['mu'].tolist(), sigma=float(np.sqrt(r['sig2'])), gamma=g.tolist(),
                se_gamma=r['se_theta'][-4:].tolist(), T=int(len(idx)), start=str(idx[0])[:7], end=str(idx[-1])[:7],
                stay_exp_min=float(stay_exp.min()), stay_exp_med=float(np.median(stay_exp)),
                p_const=[float(rc['P'][0, 0]), float(rc['P'][1, 1])], mu_const=rc['mu'].tolist(),
                share_rec=float((r['smooth'][:, 0] > 0.5).mean()), qps=qps(r['smooth'][:, 0], rr),
                conc=concordance(r['smooth'][:, 0] > 0.5, rr))


# =============================================================================
# 5. MARKOV-SWITCHING VAR AND REGIME-DEPENDENT IMPULSE RESPONSES
# =============================================================================
def us_var_data(start='1960-01-01', end=US['est_end']):
    y, rec = us_gdp()
    u = us_unemp_q()
    D = pd.concat([y, u.diff().rename('du')], axis=1).loc[start:end].dropna()
    return D, rec.reindex(D.index)


def fig_msvar(save_it=True, H=12):
    """MSIAH(2)-VAR(1) for US GDP growth and the change of the unemployment rate (quarterly, 1960-2019); regime-dependent
    responses of the unemployment rate (cumulated) to a one-standard-deviation output shock (Cholesky, output first)."""
    D, rec = us_var_data()
    r = em_msvar(D.values, 1, K=2, seed=SEED, starts=12)
    hi = int(np.argmax([s[0, 0] for s in r['S']]))      # volatile regime: larger variance of the output shock
    lo = 1 - hi
    Yt, X = var_design(D.values, 1)
    Bl = np.linalg.lstsq(X, Yt, rcond=None)[0]
    Sl = np.cov((Yt - X @ Bl).T, bias=True)
    irf = {k: regime_irf(r['B'][j], r['S'][j], 2, 1, H) for k, j in (('lo', lo), ('hi', hi))}
    irf['lin'] = regime_irf(Bl, Sl, 2, 1, H)
    irf = {k: v / v[0, 0] for k, v in irf.items()}          # scaled to a 1 pp output shock on impact
    idx = D.index[1:]
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9), gridspec_kw=dict(width_ratios=[1.4, 1]))
    shade(axs[0], rec.iloc[1:])
    axs[0].plot(idx, r['smooth'][:, hi], color=st.MainBlue, lw=1.2, label='smoothed Pr(volatile regime)')
    axs[0].set_ylim(-0.02, 1.02)
    hs = np.arange(H + 1)
    for k, c, lab in (('lo', st.Forest, 'calm regime'), ('hi', st.IDAred, 'volatile regime'), ('lin', st.MainBlue, 'linear VAR(1)')):
        axs[1].plot(hs, np.cumsum(irf[k][:, 1]), color=c, lw=1.8, ls='--' if k == 'lin' else '-', label=f'unemployment response, {lab}')
    axs[1].axhline(0, color=st.DarkText, lw=0.6)
    axs[1].set_xlabel('quarters after the output shock')
    axs[1].set_title('Unemployment rate (pp) after a 1 pp output shock')
    h0, l0 = axs[0].get_legend_handles_labels()
    h1, l1 = axs[1].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h0 + [patch(st.Amber)] + h1, l0 + ['NBER recessions'] + l1, ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.12, 1, 1))
    save('ats_ch7_msvar', save_it)
    mean_g = [float(b[0, 0] / (1 - b[1, 0])) for b in r['B']]
    return dict(loglik=r['loglik'], npar=r['npar'], T=r['T'], P=[float(r['P'][lo, lo]), float(r['P'][hi, hi])],
                dur=[float(1 / (1 - r['P'][lo, lo])), float(1 / (1 - r['P'][hi, hi]))],
                sd_y=[float(np.sqrt(r['S'][lo][0, 0])), float(np.sqrt(r['S'][hi][0, 0]))],
                sd_u=[float(np.sqrt(r['S'][lo][1, 1])), float(np.sqrt(r['S'][hi][1, 1]))],
                corr=[float(r['S'][j][0, 1] / np.sqrt(r['S'][j][0, 0] * r['S'][j][1, 1])) for j in (lo, hi)],
                a11=[float(r['B'][lo][1, 0]), float(r['B'][hi][1, 0])],
                u_h4=[float(np.cumsum(irf[k][:, 1])[4]) for k in ('lo', 'hi', 'lin')],
                u_h12=[float(np.cumsum(irf[k][:, 1])[H]) for k in ('lo', 'hi', 'lin')],
                shock=[float(irf[k][0, 0]) for k in ('lo', 'hi', 'lin')],
                share_lo=float(r['smooth'][:, hi].mean()), qps=qps(r['smooth'][:, hi], rec.iloc[1:].values),
                rec_in_vol=float(r['smooth'][rec.iloc[1:].values == 1, hi].mean()),
                vol_pre84=float(r['smooth'][idx < pd.Timestamp('1984-01-01'), hi].mean()),
                vol_post84=float(r['smooth'][idx >= pd.Timestamp('1984-01-01'), hi].mean()),
                mean_g=[float(r['B'][j][0, 0] / (1 - r['B'][j][1, 0])) for j in (lo, hi)],
                ll_lin=float(-0.5 * len(Yt) * (np.log(np.linalg.det(Sl)) + 2 * np.log(2 * np.pi) + 2)), iters=r['iters'])


# =============================================================================
# 6. MARKOV-SWITCHING GARCH
# =============================================================================
def fig_msgarch(save_it=True, start=MARKET['start']):
    """S&P 500 daily log returns: GARCH(1,1), MS-GARCH(1,1) of Haas, Mittnik and Paolella (2004) and of Gray (1996)."""
    r = load_close('sp500', start, MARKET['end'])
    ret = (100 * np.log(r).diff()).dropna()
    x = ret.values
    g1 = msgarch_fit(x, K=1)
    hmp = msgarch_fit(x, K=2, kind='hmp')
    gray = msgarch_fit(x, K=2, kind='gray')
    hi = int(np.argmax(hmp['omega'] / (1 - hmp['alpha'] - hmp['beta'])))
    ann = np.sqrt(252)
    fig, axs = plt.subplots(2, 1, figsize=(11, 5.0), sharex=True, gridspec_kw=dict(height_ratios=[1.4, 1]))
    axs[0].plot(ret.index, ann * np.sqrt(g1['h'][:, 0]), color=st.MainBlue, lw=0.8, label='GARCH(1,1)')
    axs[0].plot(ret.index, ann * np.sqrt(hmp['hmix']), color=st.IDAred, lw=0.8, label='MS-GARCH (Haas, Mittnik, Paolella)')
    axs[0].set_ylabel('volatility, % p.a.')
    axs[1].plot(ret.index, hmp['filt'][:, hi], color=st.Purple, lw=0.6, label='filtered Pr(high-volatility regime)')
    axs[1].set_ylim(-0.02, 1.02)
    st.fig_legend_bottom(fig, ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch7_msgarch', save_it)
    T = len(x)
    out = {}
    for k, m in (('garch', g1), ('hmp', hmp), ('gray', gray)):
        out[k] = dict(loglik=float(m['loglik']), npar=int(m['npar']), bic=float(-2 * m['loglik'] + m['npar'] * np.log(T)),
                      omega=m['omega'].tolist(), alpha=m['alpha'].tolist(), beta=m['beta'].tolist(),
                      pers=(m['alpha'] + m['beta']).tolist(), P=np.diag(m['P']).tolist())
    lo = 1 - hi
    out.update(hi=hi, lo=lo, T=T, start=str(ret.index[0].date()), end=str(ret.index[-1].date()),
               uncond=[float(ann * np.sqrt(hmp['h'][hmp['filt'][:, j] > 0.5, j]).mean()) for j in (lo, hi)],
               share_hi=float((hmp['filt'][:, hi] > 0.5).mean()),
               dur=[float(1 / (1 - hmp['P'][lo, lo])), float(1 / (1 - hmp['P'][hi, hi]))])
    return out


# =============================================================================
# 7. BULL AND BEAR MARKETS: WEEKLY S&P 500 AND BET; REGIME-DEPENDENT ALLOCATION
# =============================================================================
def fit_bullbear(name):
    r = weekly_returns(name)
    ys, X = r.values, np.ones((len(r), 1))
    e = best_em(ys, X, 2, starts=15, seed=SEED, order='var', polish=True)
    return r, e


def fig_bullbear(save_it=True, gamma=5.0):
    """Two regimes in mean and variance for weekly S&P 500 and BET log returns; regime 1 = calm, regime 2 = turbulent.
    Ang and Bekaert (2002), briefly: mean-variance weight of equity against cash, w = mu / (gamma sigma^2), by regime."""
    import statsmodels.api as sm
    fig, axs = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True)
    out = {}
    probs = {}
    for ax, name, lab in ((axs[0], 'sp500', 'S&P 500'), (axs[1], 'bet', 'BET')):
        r, e = fit_bullbear(name)
        lvl = np.exp(np.cumsum(r.values) / 100)
        shade(ax, pd.Series(e['smooth'][:, 1] > 0.5, index=r.index), color=st.IDAred, alpha=0.15)
        ax.plot(r.index, 100 * lvl, color=st.MainBlue if name == 'sp500' else st.Forest, lw=1.0, label=f'{lab} (first week = 100)')
        ax.set_yscale('log')
        smr = sm.tsa.MarkovRegression(r.values, k_regimes=2, switching_variance=True).fit(search_reps=20, disp=False)
        mu, s = e['beta'][:, 0], np.sqrt(e['sig2'])
        w = 100 * mu / (gamma * s ** 2)                     # returns in %: weight as a fraction of wealth
        xi = e['filt'] @ e['P']
        m_t = xi @ mu
        v_t = xi @ (s ** 2 + mu ** 2) - m_t ** 2
        probs[name] = pd.Series(e['smooth'][:, 1], index=r.index)
        out[name] = dict(mu=mu.tolist(), sd=s.tolist(), ann_mu=(52 * mu).tolist(), ann_sd=(np.sqrt(52) * s).tolist(),
                         P=np.diag(e['P']).tolist(), dur=(1 / (1 - np.diag(e['P']))).tolist(), loglik=float(e['loglik']),
                         sm_llf=float(smr.llf), se=e['se'].tolist(), share_turb=float((e['smooth'][:, 1] > 0.5).mean()),
                         w=w.tolist(), w_const=float(100 * np.mean(r.values) / (gamma * np.var(r.values))),
                         w_t_min=float((100 * m_t / (gamma * v_t)).min()), w_t_max=float((100 * m_t / (gamma * v_t)).max()),
                         T=int(len(r)), last=float(e['filt'][-1, 1]))
    h0, l0 = axs[0].get_legend_handles_labels()
    h1, l1 = axs[1].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h0 + h1 + [patch(st.IDAred, 0.15)], l0 + l1 + ['turbulent regime (smoothed probability > 0.5)'], ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch7_bullbear', save_it)
    j = pd.concat(probs, axis=1).dropna()
    out['corr_turb'] = float(j.corr().iloc[0, 1])
    out['both_turb'] = float(((j > 0.5).all(axis=1)).mean())
    out['gamma'] = gamma
    return out


# =============================================================================
# 8. BAYESIAN ESTIMATION: GIBBS SAMPLING, LABEL SWITCHING (ROMANIAN GDP GROWTH)
# =============================================================================
def fig_gibbs(save_it=True, n_iter=6000, burn=1000):
    """Romanian quarterly GDP growth: two regimes in mean and variance. Gibbs sampler with FFBS (Chib 1996), once with
    the random permutation sampler (label switching made visible), once identified by mu_1 < mu_2; EM for comparison."""
    y = ro_gdp()
    g_perm = gibbs_ms(y.values, 2, n_iter=n_iter, burn=burn, seed=SEED, permute=True)
    g_id = gibbs_ms(y.values, 2, n_iter=n_iter, burn=burn, seed=SEED + 1, permute=False)
    e = best_em(y.values, np.ones((len(y), 1)), 2, starts=15, seed=SEED, order='mean')
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9), gridspec_kw=dict(width_ratios=[1, 1.4]))
    axs[0].hist(g_perm['mu'][:, 0], bins=60, density=True, color=st.Purple, alpha=0.45, label='mu of label 1, permutation sampler')
    axs[0].hist(g_perm['mu_id'][:, 0], bins=60, density=True, histtype='step', color=st.IDAred, lw=1.6, label='mu_1 after imposing mu_1 < mu_2')
    axs[0].hist(g_perm['mu_id'][:, 1], bins=60, density=True, histtype='step', color=st.Forest, lw=1.6, label='mu_2 after imposing mu_1 < mu_2')
    axs[0].set_xlabel('regime mean, % per quarter')
    axs[1].plot(y.index, g_id['prob'][:, 0], color=st.MainBlue, lw=1.3, label='posterior Pr(low-mean regime), Gibbs')
    axs[1].plot(y.index, e['smooth'][:, 0], color=st.Orange, lw=1.1, ls='--', label='smoothed probability, EM')
    axs[1].set_ylim(-0.02, 1.02)
    st.fig_legend_bottom(fig, ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.12, 1, 1))
    save('ats_ch7_gibbs', save_it)
    mu = g_id['mu_id']
    sd = np.sqrt(g_id['sig2_id'])
    P = g_id['P_id']
    q = lambda a: [float(np.mean(a)), float(np.quantile(a, 0.05)), float(np.quantile(a, 0.95))]
    lab_sw = float(np.mean(g_perm['mu'][:, 0] > g_perm['mu'][:, 1]))
    acf1 = float(acf(mu[:, 0], 1)[1])
    return dict(T=int(len(y)), start=str(y.index[0].to_period('Q')), end=str(y.index[-1].to_period('Q')),
                mu1=q(mu[:, 0]), mu2=q(mu[:, 1]), sd1=q(sd[:, 0]), sd2=q(sd[:, 1]), p11=q(P[:, 0, 0]), p22=q(P[:, 1, 1]),
                em_mu=e['beta'][:, 0].tolist(), em_sd=np.sqrt(e['sig2']).tolist(), em_P=np.diag(e['P']).tolist(),
                share_swapped=lab_sw, acf1=acf1, n_kept=int(n_iter - burn),
                lo_quarters=[str(i.to_period('Q')) for i in y.index[g_id['prob'][:, 0] > 0.5]][:60],
                n_lo=int((g_id['prob'][:, 0] > 0.5).sum()), corr_em=float(np.corrcoef(g_id['prob'][:, 0], e['smooth'][:, 0])[0, 1]))


# =============================================================================
# 9. REGIME SWITCHING AND LONG MEMORY (DIEBOLD AND INOUE 2001)
# =============================================================================
def sim_ms(T, p, rng, mu=(0.0, 1.0), sigma=1.0):
    P = np.array([[p, 1 - p], [1 - p, p]])
    s = simulate_chain(P, T, rng)
    return np.asarray(mu)[s] + sigma * rng.normal(size=T), s


def fig_longmem(save_it=True, Ts=(250, 1000, 4000, 16000), reps=200, c=5.0):
    """Mean GPH estimate of d for y_t = mu_{S_t} + e_t: (a) p_ii = 1 - c / T, so the expected number of switches stays
    at c whatever T (Diebold and Inoue 2001); (b) fixed p_ii = 0.95 (short memory). Left: one path with T = 4000."""
    rng = np.random.default_rng(SEED)
    res = {'rare': [], 'fixed': []}
    for T in Ts:
        for k, p in (('rare', 1 - c / T), ('fixed', 0.95)):
            d = [gph(sim_ms(T, p, rng)[0]) for _ in range(reps)]
            res[k].append((float(np.mean(d)), float(np.std(d) / np.sqrt(reps))))
    y, s = sim_ms(4000, 1 - c / 4000, np.random.default_rng(SEED + 7))
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.8), gridspec_kw=dict(width_ratios=[1.3, 1]))
    axs[0].plot(y, color=st.MainBlue, lw=0.4, label='simulated series, T = 4000, p = 1 - 5/T')
    axs[0].plot(np.array([0.0, 1.0])[s], color=st.IDAred, lw=1.6, label='regime mean')
    for k, cc, lab in (('rare', st.IDAred, 'p = 1 - 5/T (rare switches)'), ('fixed', st.MainBlue, 'p = 0.95 (fixed)')):
        m = np.array([v[0] for v in res[k]])
        se = np.array([v[1] for v in res[k]])
        axs[1].errorbar(Ts, m, yerr=2 * se, color=cc, marker='o', lw=1.6, capsize=3, label=f'mean GPH estimate of d, {lab}')
    axs[1].set_xscale('log')
    axs[1].axhline(0, color=st.DarkText, lw=0.6)
    axs[1].set_xlabel('sample size T')
    st.fig_legend_bottom(fig, ncol=2, y=0.02)
    plt.tight_layout(rect=(0, 0.13, 1, 1))
    save('ats_ch7_longmem', save_it)
    a = acf(y, 200)
    return dict(rare=res['rare'], fixed=res['fixed'], Ts=list(Ts), c=c, reps=reps, acf50=float(a[50]), acf200=float(a[200]),
                switches=int((np.diff(s) != 0).sum()))


# =============================================================================
# 10. ROMANIAN INFLATION REGIMES SINCE 1997 AND A CHANGE-POINT MODEL
# =============================================================================
def fig_ro_infl(save_it=True, starts=25):
    """Romanian annual HICP inflation: MSIH(3)-AR(1) (switching intercept and variance, common AR coefficient), against
    change-point models with 3 and 4 regimes (Chib 1998: P upper bidiagonal, no return)."""
    y = ro_inflation()
    ys, X = lag_design(y.values, 1)
    idx = y.index[1:]
    ms3 = best_em(ys, X, 3, starts=starts, switch=[True, False], seed=SEED, order=None)
    lev = ms3['beta'][:, 0] / (1 - ms3['beta'][0, 1])
    o = np.argsort(-lev)
    ms3 = dict(ms3, beta=ms3['beta'][o], sig2=ms3['sig2'][o], P=ms3['P'][np.ix_(o, o)], smooth=ms3['smooth'][:, o], filt=ms3['filt'][:, o])
    lev = ms3['beta'][:, 0] / (1 - ms3['beta'][0, 1])
    cps = {}
    for K in (3, 4, 5):
        mask = np.eye(K) + np.eye(K, k=1)
        best = None
        rng = np.random.default_rng(SEED)
        for s in range(starts):
            # starting values: K segments of equal length
            cut = np.sort(rng.choice(np.arange(12, len(ys) - 12), K - 1, replace=False))
            seg = np.searchsorted(cut, np.arange(len(ys)), side='right')
            W = np.eye(K)[seg]
            beta0 = np.vstack([np.linalg.lstsq(X * np.sqrt(W[:, [j]]), ys * np.sqrt(W[:, j]), rcond=None)[0] for j in range(K)])
            beta0[:, 1] = beta0[:, 1].mean()
            sig0 = np.array([max(np.var(ys[seg == j]) * 0.1, 0.05) for j in range(K)])
            r = em_msr(ys, X, K, switch=[True, False], P0=0.5 * mask + 0.5 * np.eye(K) * 0 + np.diag([0.0] * K),
                       beta0=beta0, sig20=sig0, P_mask=mask, xi1_fixed=np.eye(K)[0], maxit=2000)
            seg_r = r['smooth'].argmax(1)
            lens = np.bincount(seg_r, minlength=K)
            if lens.min() < 6:                       # every segment at least six months
                continue
            if best is None or r['loglik'] > best['loglik']:
                best = r
        cps[K] = best
    fig, axs = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True, gridspec_kw=dict(height_ratios=[1.3, 1]))
    cols = [st.IDAred, st.Amber, st.Forest]
    reg = ms3['smooth'].argmax(1)
    for j in range(3):
        shade(axs[0], pd.Series(reg == j, index=idx), color=cols[j], alpha=0.18)
    axs[0].plot(y.index, y.values, color=st.MainBlue, lw=1.3, label='annual HICP inflation, %')
    axs[0].set_yscale('symlog', linthresh=10)
    axs[0].set_yticks([0, 2, 5, 10, 20, 50, 100])
    axs[0].set_yticklabels(['0', '2', '5', '10', '20', '50', '100'])
    cp = cps[4]
    seg = cp['smooth'].argmax(1)
    brk = [idx[i] for i in range(1, len(seg)) if seg[i] != seg[i - 1]]
    for b in brk:
        axs[0].axvline(b, color=st.Purple, lw=1.2, ls='--')
    axs[0].plot([], [], color=st.Purple, lw=1.2, ls='--', label='change points, 4-regime change-point model')
    labs = ['high-inflation regime', 'moderate-inflation regime', 'low-inflation regime']
    axs[1].stackplot(idx, ms3['smooth'].T, colors=cols, alpha=0.6, labels=[f'smoothed Pr({l})' for l in labs])
    axs[1].set_ylim(0, 1)
    st.fig_legend_bottom(fig, ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch7_ro_infl', save_it)
    T = len(ys)
    ic = {'MS3': info_criteria(ms3['loglik'], ms3['npar'], T)}
    for K, r in cps.items():
        ic[f'CP{K}'] = info_criteria(r['loglik'], r['npar'], T)
    # regime episodes of the MS model (most likely regime, runs of at least 3 months)
    eps = []
    cur = reg[0]
    st_ = idx[0]
    for i in range(1, len(reg)):
        if reg[i] != cur:
            eps.append(dict(regime=int(cur), start=str(st_)[:7], end=str(idx[i - 1])[:7]))
            cur, st_ = reg[i], idx[i]
    eps.append(dict(regime=int(cur), start=str(st_)[:7], end=str(idx[-1])[:7]))
    return dict(T=T, start=str(idx[0])[:7], end=str(idx[-1])[:7], last=float(y.iloc[-1]), max=float(y.max()),
                maxdate=str(y.idxmax())[:7], level=lev.tolist(), sd=np.sqrt(ms3['sig2']).tolist(), phi=float(ms3['beta'][0, 1]),
                P=np.diag(ms3['P']).tolist(), dur=(1 / (1 - np.diag(ms3['P']))).tolist(), loglik=float(ms3['loglik']),
                ll_cp={str(K): float(r['loglik']) for K, r in cps.items()}, ic={k: {kk: float(vv) for kk, vv in v.items()} for k, v in ic.items()},
                breaks4=[str(b)[:7] for b in brk], episodes=eps, P_full=ms3['P'].tolist(),
                last_probs=ms3['filt'][-1].tolist(), lastdate=str(idx[-1])[:7])


# =============================================================================
# 11. EUR/RON: VOLATILITY REGIMES
# =============================================================================
def fig_eurron(save_it=True, starts=20):
    """Weekly log changes of EUR/RON (%): three regimes in mean and variance (MSIH(3)-AR(0)), ordered by volatility."""
    d = eurron_daily()
    w = d.resample('W-FRI').last().dropna()
    r = (100 * np.log(w).diff()).dropna().loc[:MARKET['end']]
    e = best_em(r.values, np.ones((len(r), 1)), 3, starts=starts, seed=SEED, order='var')
    fig, axs = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True, gridspec_kw=dict(height_ratios=[1.2, 1]))
    axs[0].plot(w.index, w.values, color=st.Forest, lw=1.1, label='EUR/RON (ECB to June 2005, BNR from July 2005)')
    for dte, lab in EVENTS_EURRON:
        for ax in axs:
            ax.axvline(pd.Timestamp(dte), color=st.Purple, lw=0.9, ls='--')
    axs[0].plot([], [], color=st.Purple, lw=0.9, ls='--', label='July 2005, October 2008, May 2025')
    cols = [st.MainBlue, st.Amber, st.IDAred]
    labs = ['calm', 'intermediate', 'turbulent']
    axs[1].stackplot(r.index, e['smooth'].T, colors=cols, alpha=0.6, labels=[f'smoothed Pr({l} regime)' for l in labs])
    axs[1].set_ylim(0, 1)
    st.fig_legend_bottom(fig, ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch7_eurron', save_it)
    sm_ = pd.DataFrame(e['smooth'], index=r.index)
    share = lambda a, b: (sm_.loc[a:b].values.argmax(1)).tolist()
    pre = np.array(share('1999-01-01', '2005-06-30'))
    post = np.array(share('2005-07-01', '2026-12-31'))
    biggest = r.loc['2025-01-01':].abs().idxmax()
    return dict(T=int(len(r)), start=str(r.index[0].date()), end=str(r.index[-1].date()), sd=np.sqrt(e['sig2']).tolist(),
                mu=e['beta'][:, 0].tolist(), P=np.diag(e['P']).tolist(), dur=(1 / (1 - np.diag(e['P']))).tolist(),
                share_turb_pre=float((pre == 2).mean()), share_turb_post=float((post == 2).mean()),
                share_calm_pre=float((pre == 0).mean()), share_calm_post=float((post == 0).mean()),
                p_turb_2008=float(sm_.loc['2008-10-01':'2009-03-31', 2].max()),
                p_turb_2025=float(sm_.loc['2025-04-15':'2025-06-30', 2].max()), big2025=str(biggest.date()),
                big2025_val=float(r.loc[biggest]), lvl_2025_04=float(w.loc['2025-04-01':'2025-04-30'].mean()),
                lvl_last=float(w.iloc[-1]), last_probs=e['filt'][-1].tolist(), loglik=float(e['loglik']))


# =============================================================================
# 12. FORECASTING WITH REGIME MODELS: US GDP, ONE STEP AHEAD
# =============================================================================
def fig_forecast(save_it=True, first='1990-01-01', last='2019-10-01', refit=4):
    """Recursive one-step forecasts of US GDP growth, 1990Q1-2019Q4: Gaussian AR(1) against MSIH(2)-AR(1) (mixture
    density); RMSE, log score, PIT; Diebold-Mariano test on the log-score difference (Newey-West variance, 4 lags)."""
    y, rec = us_gdp()
    y = y.loc[US['start']:last]
    dates = y.loc[first:].index
    rows = []
    e = None
    for i, d in enumerate(dates):
        hist = y.loc[:d - pd.offsets.QuarterBegin(1)]
        ys, X = lag_design(hist.values, 1)
        lin = linear_ar(ys, X)
        if e is None or i % refit == 0:
            starts = [dict(P0=e['P'], beta0=e['beta'], sig20=e['sig2'])] if e is not None else []
            cand = [em_msr(ys, X, 2, switch=[True, False], maxit=500, **s0) for s0 in starts]
            cand.append(best_em(ys, X, 2, starts=3, switch=[True, False], seed=SEED + i, order=None, maxit=500))
            e = max(cand, key=lambda r: r['loglik'])
        f = hamilton_filter(msr_logf(ys, X, e['beta'], e['sig2']), e['P'])
        xi = f['filt'][-1] @ e['P']
        xn = np.array([1.0, hist.values[-1]])
        m = e['beta'] @ xn
        yt = float(y.loc[d])
        mean_ms = float(xi @ m)
        mu_l = float(lin['beta'] @ xn)
        rows.append(dict(date=d, y=yt, ar=mu_l, ms=mean_ms, ls_ar=float(stats.norm.logpdf(yt, mu_l, np.sqrt(lin['sig2']))),
                         ls_ms=mixture_logscore(yt, xi, m, e['sig2']), pit_ar=float(stats.norm.cdf(yt, mu_l, np.sqrt(lin['sig2']))),
                         pit_ms=mixture_pit(yt, xi, m, e['sig2']), p_lowvar=float(xi[np.argmax(e['sig2'])]),
                         p_lowmean=float(xi[np.argmin(e['beta'][:, 0] / (1 - e['beta'][0, 1]))])))
    D = pd.DataFrame(rows).set_index('date')
    dls = D['ls_ms'] - D['ls_ar']
    n = len(dls)
    u = dls - dls.mean()
    lr = u @ u / n + 2 * sum((1 - k / 5) * (u[k:].values @ u[:-k].values) / n for k in range(1, 5))
    dm = float(dls.mean() / np.sqrt(lr / n))
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.8), gridspec_kw=dict(width_ratios=[1.4, 1]))
    shade(axs[0], rec.reindex(D.index))
    axs[0].plot(D.index, dls.cumsum(), color=st.MainBlue, lw=1.6, label='cumulative log score, MSIH(2)-AR(1) minus AR(1)')
    axs[0].axhline(0, color=st.DarkText, lw=0.6)
    bins = np.linspace(0, 1, 11)
    axs[1].hist([D['pit_ar'], D['pit_ms']], bins=bins, color=[st.Forest, st.IDAred], alpha=0.7, label=['PIT, AR(1)', 'PIT, MSIH(2)-AR(1)'])
    axs[1].axhline(n / 10, color=st.DarkText, lw=0.8, ls='--')
    axs[1].set_xlabel('PIT value')
    h0, l0 = axs[0].get_legend_handles_labels()
    h1, l1 = axs[1].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h0 + [patch(st.Amber)] + h1, l0 + ['NBER recessions'] + l1, ncol=2, y=0.02)
    plt.tight_layout(rect=(0, 0.12, 1, 1))
    save('ats_ch7_forecast', save_it)
    rr = rec.reindex(D.index).values
    pre08 = D.index < pd.Timestamp('2008-01-01')
    return dict(n=int(n), rmse_ar=float(np.sqrt(((D['y'] - D['ar']) ** 2).mean())), rmse_ms=float(np.sqrt(((D['y'] - D['ms']) ** 2).mean())),
                ls_ar=float(D['ls_ar'].mean()), ls_ms=float(D['ls_ms'].mean()), dm=dm, p_dm=float(2 * stats.norm.sf(abs(dm))),
                qps_lowmean=qps(D['p_lowmean'].values, rr), qps_const=qps(np.full(n, rr.mean()), rr),
                cum_pre08=float(dls[pre08].sum()), cum_post08=float(dls[~pre08].sum()),
                ks_ar=float(stats.kstest(D['pit_ar'], 'uniform').pvalue), ks_ms=float(stats.kstest(D['pit_ms'], 'uniform').pvalue))


# =============================================================================
# 13. AI MINI-CASE: HOW ROBUST IS A RECESSION DATING?
# =============================================================================
def dating_variant(y, model, start):
    """Smoothed probability of the low-mean regime for one specification (estimated from `start` to 2019Q4)."""
    ye = y.loc[start:US['est_end']]
    if model == 'MSM-AR(4)':
        r = fit_hamilton(ye, nrand=6)
        return pd.Series(r['smooth'][:, 0], index=ye.index[4:])
    p = 1 if model.endswith('AR(1)') else 0
    ys, X = lag_design(ye.values, p)
    sv = model.startswith('MSIH')
    e = best_em(ys, X, 2, starts=10, switch=[True] + [False] * p, switch_var=sv, seed=SEED, order=None)
    lev = e['beta'][:, 0] / (1 - (e['beta'][0, 1] if p else 0))
    lo = int(np.argmin(lev))
    return pd.Series(e['smooth'][:, lo], index=ye.index[p:])


def fig_ai_case(save_it=True, window=('1985-01-01', US['est_end'])):
    y, rec = us_gdp()
    models = ['MSM-AR(4)', 'MSI-AR(0)', 'MSIH-AR(0)', 'MSIH-AR(1)']
    starts = ['1947-04-01', '1952-04-01', '1984-01-01']
    rows = []
    for m in models:
        for s in starts:
            p = dating_variant(y, m, s).loc[window[0]:window[1]]
            rr = rec.reindex(p.index).values
            false = float((p.values[rr == 0] > 0.5).mean())           # share of non-recession quarters signalled
            rows.append(dict(model=m, start=s[:4], qps=qps(p.values, rr), conc=concordance(p.values > 0.5, rr),
                             d2001=bool(p.loc['2001-01-01':'2001-10-01'].max() > 0.5 and false < 0.2),
                             d2008=bool(p.loc['2008-01-01':'2009-04-01'].max() > 0.5 and false < 0.2),
                             false=false, share=float((p > 0.5).mean())))
    t = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(11, 3.8))
    mk = {'1947': 'o', '1952': 's', '1984': '^'}
    cl = {True: st.Forest, False: st.IDAred}
    for i, m in enumerate(models):
        for _, r in t[t['model'] == m].iterrows():
            ax.scatter(i + {'1947': -0.15, '1952': 0, '1984': 0.15}[r['start']], r['qps'], marker=mk[r['start']], s=60,
                       color=cl[r['d2008'] and r['d2001']], zorder=3)
    for s, m_ in mk.items():
        ax.scatter([], [], marker=m_, color=st.MainBlue, label=f'sample from {s}')
    ax.scatter([], [], marker='o', color=st.Forest, label='dates 2001 and 2008, few false alarms')
    ax.scatter([], [], marker='o', color=st.IDAred, label='misses 2001 or 2008, or false alarms')
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models)
    ax.set_ylabel('QPS against NBER, 1985-2019')
    st.legend_outside_bottom(ax, ncol=3, y=-0.15)
    save('ats_ch7_ai_case', save_it)
    return dict(rows=rows, qmin=float(t['qps'].min()), qmax=float(t['qps'].max()), n=int(len(t)),
                n_both=int((t['d2001'] & t['d2008']).sum()), n_false=int((t['false'] >= 0.2).sum()), n2008=int(t['d2008'].sum()), n2001=int(t['d2001'].sum()),
                qconst=qps(np.full(len(rec.loc[window[0]:window[1]]), rec.loc[window[0]:window[1]].mean()), rec.loc[window[0]:window[1]].values))


# =============================================================================
# 14. THEORY CHART: DURATIONS AND THE h-STEP REGIME FORECAST
# =============================================================================
def fig_chain(save_it=True, p11=0.9, p22=0.75):
    """Two-regime chain: geometric duration distributions and the convergence of Pr(S_{t+h} = 1 | S_t) to the ergodic
    probability at the rate lambda^h, lambda = p11 + p22 - 1."""
    P = np.array([[p11, 1 - p11], [1 - p22, p22]])
    pi = ergodic(P)
    d = np.arange(1, 21)
    hs = np.arange(0, 21)
    fig, axs = plt.subplots(1, 2, figsize=(12, 3.6))
    axs[0].bar(d - 0.2, p11 ** (d - 1) * (1 - p11), width=0.4, color=st.MainBlue, label=f'regime 1, p11 = {p11}')
    axs[0].bar(d + 0.2, p22 ** (d - 1) * (1 - p22), width=0.4, color=st.IDAred, label=f'regime 2, p22 = {p22}')
    axs[0].set_xlabel('duration d (periods)')
    axs[0].set_title('Pr(D = d)')
    for s0, c, lab in ((0, st.MainBlue, 'starting in regime 1'), (1, st.IDAred, 'starting in regime 2')):
        pr = [np.linalg.matrix_power(P, h)[s0, 0] for h in hs]
        axs[1].plot(hs, pr, 'o-', color=c, ms=3, lw=1.4, label=f'Pr(S(t+h) = 1), {lab}')
    axs[1].axhline(pi[0], color=st.Forest, lw=1.2, ls='--', label='ergodic probability of regime 1')
    axs[1].set_xlabel('horizon h')
    st.fig_legend_bottom(fig, ncol=3, y=0.02)
    plt.tight_layout(rect=(0, 0.14, 1, 1))
    save('ats_ch7_chain', save_it)
    return dict(pi1=float(pi[0]), lam=p11 + p22 - 1, d1=1 / (1 - p11), d2=1 / (1 - p22))


if __name__ == '__main__':
    st.apply()
    N = {}
    only = sys.argv[1:]
    path = os.path.join(HERE, 'ch7_numbers.json')
    if os.path.exists(path):
        N = json.load(open(path))
    for name, f in [('chain', fig_chain), ('hamilton', fig_hamilton), ('realtime', fig_realtime), ('em', fig_em),
                    ('lrtest', fig_lrtest), ('tvtp', fig_tvtp), ('msvar', fig_msvar), ('msgarch', fig_msgarch),
                    ('bullbear', fig_bullbear), ('gibbs', fig_gibbs), ('longmem', fig_longmem), ('roinfl', fig_ro_infl),
                    ('eurron', fig_eurron), ('forecast', fig_forecast), ('ai', fig_ai_case)]:
        if only and name not in only:
            continue
        print(name, flush=True)
        N[name] = f()
        with open(path, 'w') as fh:
            json.dump(N, fh, indent=1, default=float)
    print('written ch7_numbers.json')
