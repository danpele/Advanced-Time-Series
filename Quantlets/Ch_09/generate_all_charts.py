"""
generate_all_charts.py -- charts and numbers of Chapter 9 (ATS): VaR, ES and backtesting
=========================================================================================
Course data (ats_data.py), chart style (ats_style.py), the numpy engine risk_core.py. Every number on the slides comes
from here.
  * scoring functions      expected pinball and FZ0 loss for a Student t, the level sets of VaR and ES under mixing
                           (why ES alone is not elicitable), Murphy diagrams (Ehm et al. 2016);
  * CAViaR                 Engle and Manganelli (2004): the four specifications, their estimation procedure, asymptotic
                           standard errors and the out-of-sample DQ test, with the design of their empirical section
                           (2,892 in-sample and 500 out-of-sample days) on the S&P 500 ending 18 September 2026;
  * Patton-Ziegel-Chen     the ten models of PZC (2019, Section 5): rolling windows (125, 250, 500 days), ARMA-GARCH with
                           Normal, skew-t and empirical innovations, GAS-2F, GAS-1F, GARCH-FZ and Hybrid estimated by FZ0
                           minimisation on January 1990 - December 1999, out-of-sample 2000-2016 (their Tables 8 and S5),
                           then the same design for the S&P 500, DAX, BET, EUR/RON and Bitcoin to September 2026;
  * backtests              PZC goodness-of-fit regressions, Kupiec, Christoffersen, duration (Christoffersen and
                           Pelletier 2004), McNeil-Frey; size of backtests under estimation risk (Monte Carlo);
  * comparison             Diebold-Mariano matrix, model confidence set under FZ0 loss, stress periods 2008, 2020,
                           2022 and 2025;
  * joint regression       VaR and ES 2.5% of S&P 500 returns on the lagged VIX (Dimitriadis and Bayer 2019);
  * horizon                10-day VaR 1% by filtered historical simulation against the square-root-of-time rule;
  * model risk             risk ratio across six standard models (Danielsson et al. 2016); bootstrap intervals of an ES
                           forecast (estimation risk);
  * extremes, conformal    extremal index of raw and filtered losses; adaptive conformal calibration of VaR 1%;
  * AI mini-case           how robust is ``the best ES model'' across assets, levels and periods.
Output: charts/ats_ch9_*.pdf/.png, Quantlets/Ch_09/ch9_numbers.json
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_09/generate_all_charts.py [name ...]
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import pickle
import sys
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
from ats_data import load_close, log_returns                                        # noqa: E402
import ats_style as st                                                             # noqa: E402
from risk_core import (aci_levels, arma_bic, arma_onestep, caviar_fit, caviar_se, caviar_var, christoffersen,  # noqa: E402
                       cp_duration_test, dm_test, dq_test, es_regression, extremal_index, fz0, fz_fit,
                       fz_forecast, garch_fit, garch_negll, garch_sigma, kupiec, mcneil_frey, mcs, murphy_quantile, normal_var_es,
                       pinball, pzc_gof, rolling_hs, skewt_fit, skewt_var_es, t_std_var_es)

warnings.filterwarnings('ignore')
SEED = 2026
END = '2026-09-18'
# asset -> (first day, first out-of-sample day): ten in-sample years as in PZC (five for Bitcoin, whose data start in 2014)
ASSETS = {'sp500': ('1990-01-01', '2000-01-01'), 'dax': ('1990-01-01', '2000-01-01'), 'bet': ('2000-01-01', '2010-01-01'),
          'eurron': ('2005-07-01', '2015-07-01'), 'btc': ('2014-09-17', '2020-01-01')}
LAB = {'sp500': 'S&P 500', 'dax': 'DAX', 'bet': 'BET', 'eurron': 'EUR/RON', 'btc': 'Bitcoin'}
MODELS = ['RW-125', 'RW-250', 'RW-500', 'GCH-N', 'GCH-Skt', 'GCH-EDF', 'FZ-2F', 'FZ-1F', 'GCH-FZ', 'Hybrid']
FZ_NAMES = ['FZ-2F', 'FZ-1F', 'GCH-FZ', 'Hybrid']
STRESS = {'2008': ('2008-09-01', '2009-03-31'), '2020': ('2020-02-19', '2020-06-30'),
          '2022': ('2022-01-03', '2022-12-30'), '2025': ('2025-03-03', '2025-06-30')}
# PZC (2019), S&P 500 column of Table 8 (alpha = 0.05) and Table S5 (alpha = 0.025): out-of-sample average FZ0 loss
PZC_TABLE = {0.05: dict(zip(MODELS, [0.914, 0.959, 1.023, 0.876, 0.866, 0.862, 0.856, 0.853, 0.862, 0.869])),
             0.025: dict(zip(MODELS, [1.119, 1.164, 1.245, 1.089, 1.043, 1.028, 1.041, 1.032, 1.020, 1.034]))}
PZC_GOF = {0.05: dict(zip(MODELS, [(0.021, 0.029), (0.001, 0.043), (0.001, 0.012), (0.031, 0.001), (0.003, 0.003),
                                   (0.003, 0.014), (0.000, 0.061), (0.242, 0.313), (0.005, 0.018), (0.001, 0.010)]))}
EM_DESIGN = dict(n_in=2892, n_out=500)                    # Engle and Manganelli (2004), empirical section
CACHE = os.environ.get('ATS_CH9_CACHE', '')
_MEM = {}


# =============================================================================
# DATA AND HELPERS
# =============================================================================
def save(name, save_it=True):
    if save_it:
        st.check_no_grey(plt.gcf())
        st.save_fig(name)
    else:
        plt.show()


def returns(name, start=None, end=END):
    """Daily log returns in % (EUR/RON: BNR reference rate; Bitcoin: 7 days a week)."""
    s = ASSETS[name][0] if start is None else start
    return log_returns(name, start=s, end=end).dropna()


def cached(key, fn):
    """Results of the expensive steps, kept in memory (and in a pickle if ATS_CH9_CACHE is set)."""
    if key in _MEM:
        return _MEM[key]
    if CACHE:
        p = os.path.join(CACHE, f'ch9_{key}.pkl')
        if os.path.exists(p):
            _MEM[key] = pickle.load(open(p, 'rb'))
            return _MEM[key]
    _MEM[key] = fn()
    if CACHE:
        os.makedirs(CACHE, exist_ok=True)
        pickle.dump(_MEM[key], open(os.path.join(CACHE, f'ch9_{key}.pkl'), 'wb'))
    return _MEM[key]


def shade_stress(ax, idx, alpha=0.18):
    for k, (a, b) in STRESS.items():
        if pd.Timestamp(a) >= idx[0] and pd.Timestamp(b) <= idx[-1]:
            ax.axvspan(pd.Timestamp(a), pd.Timestamp(b), color=st.Amber, alpha=alpha, lw=0, label='_stress')


# =============================================================================
# THE PZC DESIGN: TEN MODELS, FIXED IN-SAMPLE PARAMETERS
# =============================================================================
def pzc_models(y, n_in, a, fits=None):
    """The ten models of PZC (2019, Section 5) for (VaR, ES) at level a: forecasts for every day (NaN where a rolling
    window is not full), all parameters estimated once on the first n_in days and kept fixed."""
    Y = np.asarray(y, float)
    out = {}
    for w in (125, 250, 500):
        out[f'RW-{w}'] = rolling_hs(Y, w, a)
    if fits is None:
        order, res = arma_bic(Y[:n_in])
        mu = arma_onestep(res, Y)
        eps = Y - mu
        pg = garch_fit(eps[:n_in])
        sig = garch_sigma(eps, pg, h0=np.var(eps[:n_in]))[:-1]
        z = eps[:n_in] / sig[:n_in]
        nu, lam = skewt_fit(z)
        fits = dict(order=order, arma=np.asarray(res.params).tolist(), mu=mu, sig=sig, garch=pg.tolist(), z=z, nu=nu, lam=lam, fz={})
    mu, sig, z = fits['mu'], fits['sig'], fits['z']
    zn = normal_var_es(a)
    zs = skewt_var_es(a, fits['nu'], fits['lam'])
    q = np.quantile(z, a)
    ze = (q, z[z <= q].mean())
    for k, (zq, zm) in (('GCH-N', zn), ('GCH-Skt', zs), ('GCH-EDF', ze)):
        out[k] = (mu + sig * zq, mu + sig * zm)
    for nm in FZ_NAMES:
        key = (nm, a)
        if key not in fits['fz']:
            fits['fz'][key] = fz_fit(nm, Y[:n_in], a)
        out[nm] = fz_forecast(fits['fz'][key], Y, n_in)
    return out, fits


def run_asset(name, alphas=(0.025, 0.05)):
    """Forecasts of the ten models for one asset at the given levels (shared ARMA-GARCH fit)."""
    def go():
        y = returns(name)
        n_in = int((y.index < ASSETS[name][1]).sum())
        res, fits = {}, None
        for a in alphas:
            res[a], fits = pzc_models(y.values, n_in, a, fits)
        return dict(y=y, n_in=n_in, fc=res, fits={k: v for k, v in fits.items() if k not in ('mu', 'sig', 'z')},
                    sig=fits['sig'], mu=fits['mu'])
    return cached(f'asset_{name}', go)


def oos_losses(r, a, start=None, end=None):
    """T x 10 matrix of FZ0 losses over the out-of-sample days (optionally a sub-period)."""
    y = r['y']
    idx = y.index[r['n_in']:]
    sel = np.ones(len(idx), bool)
    if start:
        sel &= idx >= pd.Timestamp(start)
    if end:
        sel &= idx <= pd.Timestamp(end)
    Y = y.values[r['n_in']:][sel]
    L = np.column_stack([fz0(Y, r['fc'][a][m][0][r['n_in']:][sel], r['fc'][a][m][1][r['n_in']:][sel], a) for m in MODELS])
    return L, idx[sel]


# =============================================================================
# 1. SCORING FUNCTIONS: THEORY CHARTS
# =============================================================================
def fig_fz0_contour(save_it=True, nu=5, a=0.025, n=400_000):
    """Expected pinball loss (left) and expected FZ0 loss (right) for a Student t(5) scaled to unit variance; the
    minimisers are the true VaR and ES; the iso-loss contours are convex (Fissler 2017)."""
    rng = np.random.default_rng(SEED)
    y = rng.standard_t(nu, n) * np.sqrt((nu - 2) / nu)
    v0, e0 = t_std_var_es(a, nu)
    vs = np.linspace(v0 - 1.5, v0 + 1.2, 121)
    pb = np.array([pinball(y, v, a).mean() for v in vs])
    V, E = np.meshgrid(np.linspace(-4.2, -1.2, 61), np.linspace(-6.5, -2.0, 61))
    Z = np.full(V.shape, np.nan)
    ys = np.sort(y)
    cs = np.concatenate([[0], np.cumsum(ys)])
    for i in range(V.shape[0]):
        for j in range(V.shape[1]):
            v, e = V[i, j], E[i, j]
            if e < v:
                k = np.searchsorted(ys, v, side='right')
                tail = (k * v - cs[k]) / n                       # E[1{y<=v}(v - y)]
                Z[i, j] = -tail / (a * e) + v / e + np.log(-e) - 1
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.1))
    axs[0].plot(vs, pb, color=st.MainBlue, lw=2, label='expected pinball loss')
    axs[0].axvline(v0, color=st.IDAred, ls='--', lw=1.2, label=f'true quantile = {v0:.2f}')
    axs[0].set_xlabel('quantile forecast v')
    axs[0].set_ylabel('expected loss')
    lv = np.nanmin(Z) + np.array([0.002, 0.01, 0.03, 0.06, 0.1, 0.2, 0.35])
    cs_ = axs[1].contour(V, E, Z, levels=lv, colors=[st.MainBlue], linewidths=1.1)
    axs[1].clabel(cs_, fmt='%.2f', fontsize=8)
    axs[1].plot([-4.2, -1.2], [-4.2, -1.2], ls=':', color=st.Purple, lw=1.2, label='e = v (boundary)')
    axs[1].scatter([v0], [e0], marker='*', s=160, color=st.IDAred, zorder=3, label=f'true (quantile, tail mean) = ({v0:.2f}, {e0:.2f})')
    i, j = np.unravel_index(np.nanargmin(Z), Z.shape)
    axs[1].set_xlabel('VaR forecast v (return quantile)')
    axs[1].set_ylabel('ES forecast e (tail mean)')
    st.legend_outside_bottom(axs[0], ncol=1, y=-0.2)
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.2)
    plt.tight_layout()
    save('ats_ch9_fz0_contour', save_it)
    return dict(nu=nu, a=a, v0=float(v0), e0=float(e0), vmin=float(vs[pb.argmin()]), zmin_v=float(V[i, j]), zmin_e=float(E[i, j]),
                zmin=float(np.nanmin(Z)))


def _cdf_pe(kind, s, nu, x):
    """cdf and partial expectation E[Y 1{Y <= x}] of a Normal(0, s^2) or a t(nu) scaled by s (closed forms)."""
    u = x / s
    if kind == 'n':
        return stats.norm.cdf(u), -s * stats.norm.pdf(u)
    return stats.t.cdf(u, nu), -s * stats.t.pdf(u, nu) * (nu + u ** 2) / (nu - 1)


def mix_var_es(lam, c0, c1, a):
    """Quantile and tail mean of the mixture lam F0 + (1 - lam) F1, each component given as (kind, scale, nu)."""
    from scipy.optimize import brentq
    F = lambda x: lam * _cdf_pe(*c0, x)[0] + (1 - lam) * _cdf_pe(*c1, x)[0] - a
    q = brentq(F, -50, 0)
    es = (lam * _cdf_pe(*c0, q)[1] + (1 - lam) * _cdf_pe(*c1, q)[1]) / a
    return q, es


def fig_level_sets(save_it=True, a=0.025):
    """Level sets under mixing: two distributions with the same alpha-quantile keep it under every mixture (convex level
    set: VaR is elicitable); two distributions with the same ES do not keep the ES (ES alone is not elicitable)."""
    zq = stats.norm.ppf(a)
    s_t = zq / stats.t.ppf(a, 3)
    es_n = -stats.norm.pdf(zq) / a
    q3 = stats.t.ppf(a, 3)
    es_t3 = -stats.t.pdf(q3, 3) * (3 + q3 ** 2) / (2 * a)
    s_t1 = es_n / es_t3
    N0, T0, T1 = ('n', 1.0, None), ('t', s_t, 3), ('t', s_t1, 3)
    lams = np.linspace(0, 1, 41)
    vq = np.array([mix_var_es(l, N0, T0, a)[0] for l in lams])
    ve = np.array([mix_var_es(l, N0, T1, a)[1] for l in lams])
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 3.8))
    axs[0].plot(lams, vq, color=st.MainBlue, lw=2, label='2.5% quantile of the mixture')
    axs[0].axhline(zq, color=st.IDAred, ls='--', lw=1.2, label='common quantile of the two components')
    axs[0].set_ylim(zq - 0.5, zq + 0.5)
    axs[0].set_xlabel('mixture weight on N(0, 1)')
    axs[0].set_title('Same quantile: Normal and rescaled t(3)')
    axs[1].plot(lams, ve, color=st.MainBlue, lw=2, label='2.5% tail mean (ES) of the mixture')
    axs[1].axhline(es_n, color=st.IDAred, ls='--', lw=1.2, label='common ES of the two components')
    axs[1].set_xlabel('mixture weight on N(0, 1)')
    axs[1].set_title('Same ES: Normal and rescaled t(3)')
    for ax in axs:
        st.legend_outside_bottom(ax, ncol=1, y=-0.22)
    plt.tight_layout()
    save('ats_ch9_level_sets', save_it)
    k = int(np.argmax(np.abs(ve - es_n)))
    return dict(zq=float(zq), es_n=float(es_n), es_mid=float(ve[20]), es_dev=float(ve[k] - es_n), lam_dev=float(lams[k]),
                vq_dev=float(np.max(np.abs(vq - zq))), s_t=float(s_t), s_t1=float(s_t1))


def fig_murphy(save_it=True, a=0.025):
    """Murphy diagram (Ehm et al. 2016) of three VaR 2.5% forecasts of the S&P 500, out of sample 2000-2016."""
    r = run_asset('sp500')
    y = r['y']
    sel = (y.index >= '2000-01-01') & (y.index <= '2016-12-31')
    Y = y.values[sel]
    th = np.linspace(-6, -0.5, 111)
    curves = {m: murphy_quantile(Y, r['fc'][a][m][0][sel], a, th) for m in ('RW-250', 'GCH-EDF', 'FZ-1F')}
    fig, ax = plt.subplots(figsize=(10, 3.9))
    for m, c in zip(curves, (st.Amber, st.MainBlue, st.IDAred)):
        ax.plot(th, curves[m], color=c, lw=1.8, label=m)
    ax.set_xlabel('threshold theta (return, %)')
    ax.set_ylabel('mean elementary score')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch9_murphy', save_it)
    d = curves['FZ-1F'] - curves['GCH-EDF']
    d2 = curves['GCH-EDF'] - curves['RW-250']
    return dict(fz_better=float((d <= 1e-12).mean()), edf_vs_rw=float((d2 <= 1e-12).mean()),
                theta_cross=[float(t) for t in th[1:][np.diff(np.sign(d)) != 0]][:4],
                pin=dict((m, float(pinball(Y, r['fc'][a][m][0][sel], a).mean())) for m in curves))


# =============================================================================
# 2. CAViaR: ENGLE AND MANGANELLI (2004)
# =============================================================================
def em_sample():
    """The last 3,392 S&P 500 returns to 18 September 2026: 2,892 in-sample and 500 out-of-sample days (EM, empirical section)."""
    y = returns('sp500')
    n = EM_DESIGN['n_in'] + EM_DESIGN['n_out']
    return y.iloc[-n:]


def caviar_table(theta):
    def go():
        y = em_sample()
        Y = y.values
        n_in = EM_DESIGN['n_in']
        out = {}
        for spec in ('SAV', 'AS', 'IG', 'ADAPT'):
            f = caviar_fit(spec, Y[:n_in], theta)
            se, _ = caviar_se(f, Y[:n_in])
            var = caviar_var(spec, f['b'], Y, theta, f['f1'])[:-1]
            q = -var
            dq_os = dq_test(Y[n_in:], q[n_in:], theta)
            out[spec] = dict(b=f['b'].tolist(), se=se.tolist(), rq=f['rq'], f1=f['f1'],
                             hit_in=float((Y[:n_in] < q[:n_in]).mean()), hit_out=float((Y[n_in:] < q[n_in:]).mean()),
                             dq_out=dq_os, q=q, pin_out=float(pinball(Y[n_in:], q[n_in:], theta).mean()))
        return dict(y=y, res=out)
    return cached(f'caviar_{theta}', go)


def fig_caviar(save_it=True, theta=0.01):
    """VaR 1% of the S&P 500 from the four CAViaR specifications, the last 500 days out of sample."""
    t = caviar_table(theta)
    y, res = t['y'], t['res']
    n_in = EM_DESIGN['n_in']
    idx = y.index
    fig, ax = plt.subplots(figsize=(11, 4.0))
    sel = slice(n_in - 250, None)
    ax.bar(idx[sel], y.values[sel], color=st.MainBlue, width=1.0, alpha=0.55, label='daily return (%)')
    for spec, c in zip(('SAV', 'AS', 'IG', 'ADAPT'), (st.Forest, st.IDAred, st.Purple, st.Orange)):
        ax.plot(idx[sel], res[spec]['q'][sel], color=c, lw=1.3, label=f'{spec}: quantile q(1%)')
    ax.axvline(idx[n_in], color=st.DarkText, ls='--', lw=1)
    ax.text(idx[n_in], ax.get_ylim()[1] * 0.9, '  out of sample', color=st.DarkText, fontsize=10)
    ax.set_ylabel('%')
    st.legend_outside_bottom(ax, ncol=5, y=-0.12)
    save('ats_ch9_caviar', save_it)
    out = {k: {kk: vv for kk, vv in v.items() if kk != 'q'} for k, v in res.items()}
    out['dates'] = [str(idx[0].date()), str(idx[n_in - 1].date()), str(idx[n_in].date()), str(idx[-1].date())]
    return out


def fig_nic(save_it=True, theta=0.01):
    """News impact curves of the four CAViaR models: VaR_t as a function of y_{t-1}, VaR_{t-1} at its in-sample median."""
    t = caviar_table(theta)
    res = t['res']
    xs = np.linspace(-6, 6, 241)
    fig, ax = plt.subplots(figsize=(10, 3.9))
    med = {}
    for spec, c in zip(('SAV', 'AS', 'IG', 'ADAPT'), (st.Forest, st.IDAred, st.Purple, st.Orange)):
        m = float(np.median(-res[spec]['q'][:EM_DESIGN['n_in']]))
        med[spec] = m
        b = np.asarray(res[spec]['b'])
        nic = [caviar_var(spec, b, np.array([x]), theta, m)[1] for x in xs]
        ax.plot(xs, nic, color=c, lw=1.8, label=spec)
    ax.set_xlabel('return yesterday (%)')
    ax.set_ylabel('VaR 1% today (%)')
    st.legend_outside_bottom(ax, ncol=4, y=-0.2)
    save('ats_ch9_nic', save_it)
    b = np.asarray(res['AS']['b'])
    return dict(median=med, as_ratio=float(b[3] / b[2]) if b[2] > 0 else None)


# =============================================================================
# 3. PZC REPLICATION AND EXTENSION
# =============================================================================
def pzc_replication():
    """S&P 500, in-sample 1990-1999, out of sample 2000-2016: average FZ0 loss, goodness-of-fit p-values and the
    Diebold-Mariano matrix at alpha = 0.05 and 0.025, next to PZC Tables 7, 8, 9 and S5."""
    r = run_asset('sp500')
    out = dict(n_in=r['n_in'], order=list(r['fits']['order']), arma=r['fits']['arma'], garch=r['fits']['garch'],
               nu=r['fits']['nu'], lam=r['fits']['lam'])
    for a in (0.05, 0.025):
        L, idx = oos_losses(r, a, '2000-01-01', '2016-12-31')
        y = r['y']
        sel = (y.index >= '2000-01-01') & (y.index <= '2016-12-31')
        gof = {m: pzc_gof(y.values[sel], r['fc'][a][m][0][sel], r['fc'][a][m][1][sel], a) for m in MODELS}
        dm = np.array([[dm_test(L[:, i], L[:, j])[0] if i != j else np.nan for j in range(10)] for i in range(10)])
        out[str(a)] = dict(T=int(len(idx)), loss=dict(zip(MODELS, L.mean(0).tolist())), paper=PZC_TABLE[a],
                           gof={m: (g['p_var'], g['p_es']) for m, g in gof.items()}, dm=dm.tolist(),
                           fz={m: np.asarray(r['fits']['fz'][(m, a)]['p']).tolist() for m in FZ_NAMES},
                           fz_in={m: float(r['fits']['fz'][(m, a)]['loss']) for m in FZ_NAMES})
    return out


def fig_pzc_paths(save_it=True, a=0.05):
    """PZC Figures 4-5 on our data: VaR and ES 5% of the S&P 500 from RW-125, GARCH-EDF and GAS-1F, 2015-2016."""
    r = run_asset('sp500')
    y = r['y']
    sel = (y.index >= '2015-01-01') & (y.index <= '2016-12-31')
    idx = y.index[sel]
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9), sharey=True)
    for ax, k, ttl in ((axs[0], 0, 'VaR 5% (return quantile)'), (axs[1], 1, 'ES 5% (tail mean)')):
        ax.bar(idx, y.values[sel], color=st.MainBlue, alpha=0.35, width=1.0, label='daily return (%)')
        for m, c in zip(('RW-125', 'GCH-EDF', 'FZ-1F'), (st.Amber, st.Forest, st.IDAred)):
            ax.plot(idx, r['fc'][a][m][k][sel], color=c, lw=1.5, label=m)
        ax.set_title(ttl)
        ax.tick_params(axis='x', rotation=30)
    h, l = axs[0].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h, l, ncol=4, y=0.02)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch9_pzc_paths', save_it)
    days_flat = float(np.mean(np.abs(np.diff(r['fc'][a]['FZ-1F'][0][sel])) < 1e-3 * np.abs(r['fc'][a]['FZ-1F'][0][sel][1:])))
    return dict(min_es=float(np.nanmin(r['fc'][a]['FZ-1F'][1][(y.index >= '2008-01-01') & (y.index <= '2009-12-31')])))


def fig_pzc_table(save_it=True):
    """Our out-of-sample average FZ0 losses against PZC Table 8 (alpha = 0.05) and Table S5 (alpha = 0.025)."""
    rep = cached('pzc_rep', pzc_replication)
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9))
    x = np.arange(10)
    for ax, a in zip(axs, (0.05, 0.025)):
        ours = [rep[str(a)]['loss'][m] for m in MODELS]
        pap = [PZC_TABLE[a][m] for m in MODELS]
        ax.bar(x, ours, color=st.MainBlue, width=0.6, label='our data (EODHD), same design')
        ax.scatter(x, pap, color=st.IDAred, marker='D', s=36, zorder=3, label='Patton, Ziegel and Chen (2019)')
        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, rotation=45, ha='right')
        ax.set_ylim(min(ours + pap) - 0.08, max(ours + pap) + 0.04)
        ax.set_title(f'alpha = {a}: average FZ0 loss, 2000-2016')
    h, l = axs[0].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h, l, ncol=2, y=0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch9_pzc_table', save_it)
    dev = {str(a): max(abs(rep[str(a)]['loss'][m] - PZC_TABLE[a][m]) for m in MODELS) for a in (0.05, 0.025)}
    return dict(maxdev=dev)


def fig_dm(save_it=True, a=0.05):
    """Diebold-Mariano t statistics (row minus column, FZ0 loss), S&P 500 2000-2016, as PZC Table 9."""
    rep = cached('pzc_rep', pzc_replication)
    D = np.array(rep[str(a)]['dm'], float)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('dm', [st.Forest, '#FFFFFF', st.IDAred])
    fig, ax = plt.subplots(figsize=(12, 4.6))
    im = ax.imshow(np.clip(D, -6, 6), cmap=cmap, vmin=-6, vmax=6, aspect='auto')
    for i in range(10):
        for j in range(10):
            if i != j:
                ax.text(j, i, f'{D[i, j]:.1f}', ha='center', va='center', fontsize=8, color=st.DarkText)
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.set_xticklabels(MODELS, rotation=30, ha='right')
    ax.set_yticklabels(MODELS)
    cb = plt.colorbar(im, ax=ax, fraction=0.03)
    cb.set_label('DM t statistic: row minus column')
    save('ats_ch9_dm', save_it)
    j = MODELS.index('FZ-1F')
    return dict(fz1f_col=dict(zip(MODELS, D[:, j].tolist())))


def fig_esreg(save_it=True, a=0.025, B=200, block=20):
    """Joint linear regression of the S&P 500 VaR and ES 2.5% on the lagged VIX, 2000-2026, by FZ0 minimisation;
    moving-block bootstrap standard errors."""
    def go():
        y = returns('sp500', start='2000-01-01')
        vx = load_close('vix', start='1999-12-01')
        x = vx.reindex(vx.index.union(y.index)).ffill().shift(1).reindex(y.index).values
        ok = np.isfinite(x)
        Y, X = y.values[ok], np.column_stack([np.ones(ok.sum()), x[ok]])
        b, g, loss, b_qr = es_regression(Y, X, a)
        rng = np.random.default_rng(SEED)
        T = len(Y)
        bs = []
        for _ in range(B):
            st_ = rng.integers(0, T - block + 1, int(np.ceil(T / block)))
            idx = (st_[:, None] + np.arange(block)).ravel()[:T]
            bb, gg, _, _ = es_regression(Y[idx], X[idx], a, n_starts=1)
            bs.append(np.concatenate([bb, gg]))
        bs = np.array(bs)
        return dict(Y=Y, X=X, b=b, g=g, loss=loss, b_qr=b_qr, se=bs.std(axis=0, ddof=1))
    r = cached('esreg', go)
    Y, X, b, g = r['Y'], r['X'], r['b'], r['g']
    fig, ax = plt.subplots(figsize=(10, 4.0))
    ax.scatter(X[:, 1], Y, s=3, color=st.MainBlue, alpha=0.35, label='daily return against VIX yesterday')
    xs = np.linspace(X[:, 1].min(), X[:, 1].max(), 50)
    ax.plot(xs, b[0] + b[1] * xs, color=st.Orange, lw=2, label='fitted VaR 2.5% (quantile)')
    ax.plot(xs, g[0] + g[1] * xs, color=st.IDAred, lw=2, label='fitted ES 2.5% (tail mean)')
    ax.set_xlabel('VIX at the previous close')
    ax.set_ylabel('S&P 500 return (%)')
    ax.set_ylim(-13, 12)
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch9_esreg', save_it)
    v, e = X @ b, X @ g
    return dict(b=b.tolist(), g=g.tolist(), se=r['se'].tolist(), b_qr=np.asarray(r['b_qr']).tolist(), T=int(len(Y)),
                hit=float((Y <= v).mean()), ratio=float(g[1] / b[1]), gof=pzc_gof(Y, v, e, a))


# =============================================================================
# 4. BACKTESTS
# =============================================================================
def backtest_table(a=0.025):
    """For every asset and model (out of sample to 2026): hit rate, Kupiec, Christoffersen CC, duration, DQ and the PZC
    VaR and ES regressions; McNeil-Frey for the GARCH models."""
    def go():
        out = {}
        for nm in ASSETS:
            r = run_asset(nm)
            n = r['n_in']
            Y = r['y'].values[n:]
            out[nm] = {}
            for m in MODELS:
                v, e = r['fc'][a][m][0][n:], r['fc'][a][m][1][n:]
                h = (Y <= v).astype(int)
                g = pzc_gof(Y, v, e, a)
                row = dict(hit=float(h.mean()), kupiec=kupiec(h, a)[1], cc=christoffersen(h, a)['p_cc'],
                           dur=cp_duration_test(h)[1], weib=cp_duration_test(h)[2], dq=dq_test(Y, v, a)[1],
                           gof_v=g['p_var'], gof_e=g['p_es'], loss=float(fz0(Y, v, e, a).mean()))
                if m.startswith('GCH-') and m != 'GCH-FZ':
                    row['mf'] = mcneil_frey(Y, v, e, r['sig'][n:])[1]
                out[nm][m] = row
        return out
    return cached(f'bt_{a}', go)


def fig_backtests(save_it=True, a=0.025):
    """p-values of the PZC VaR and ES goodness-of-fit regressions, ten models, five assets, out of sample to 2026."""
    bt = backtest_table(a)
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap([st.IDAred, st.Amber, st.Forest])
    norm = BoundaryNorm([0, 0.05, 0.10, 1.0], 3)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.6))
    for ax, key, ttl in ((axs[0], 'gof_v', 'VaR 2.5%: hit regression'), (axs[1], 'gof_e', 'ES 2.5%: tail regression')):
        M = np.array([[bt[nm][m][key] for nm in ASSETS] for m in MODELS])
        ax.imshow(M, cmap=cmap, norm=norm, aspect='auto')
        for i in range(10):
            for j in range(5):
                ax.text(j, i, f'{M[i, j]:.2f}', ha='center', va='center', fontsize=8.5, color='white' if M[i, j] < 0.05 else st.DarkText)
        ax.set_xticks(range(5))
        ax.set_xticklabels([LAB[k] for k in ASSETS], rotation=30)
        ax.set_yticks(range(10))
        ax.set_yticklabels(MODELS)
        ax.set_title(ttl)
    from matplotlib.patches import Patch
    st.fig_legend_bottom(fig, [Patch(color=st.IDAred), Patch(color=st.Amber), Patch(color=st.Forest)],
                         ['p < 0.05', '0.05 <= p < 0.10', 'p >= 0.10'], ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    save('ats_ch9_backtests', save_it)
    passv = {nm: [m for m in MODELS if bt[nm][m]['gof_v'] >= 0.1 and bt[nm][m]['gof_e'] >= 0.1] for nm in ASSETS}
    return dict(table=bt, pass_both=passv, n_pass=int(sum(len(v) for v in passv.values())))


def fig_durations(save_it=True, a=0.025):
    """Durations between VaR 2.5% hits of the S&P 500 out of sample (2000-2026): empirical survival against the
    geometric survival implied by a correct model, RW-250 against GAS-1F."""
    r = run_asset('sp500')
    n = r['n_in']
    Y = r['y'].values[n:]
    fig, ax = plt.subplots(figsize=(10, 3.9))
    out = {}
    for m, c in (('RW-250', st.Amber), ('GCH-EDF', st.Forest), ('FZ-1F', st.IDAred)):
        h = (Y <= r['fc'][a][m][0][n:]).astype(int)
        d = np.diff(np.flatnonzero(h))
        ds = np.sort(d)
        ax.step(ds, 1 - np.arange(1, len(ds) + 1) / len(ds), where='post', color=c, lw=1.6, label=f'{m}: {len(d)} durations')
        lr, p, b = cp_duration_test(h)
        out[m] = dict(n=int(len(d)), share1=float((d == 1).mean()), share5=float((d <= 5).mean()), b=b, p=p, med=float(np.median(d)))
    xs = np.arange(1, 400)
    ax.plot(xs, (1 - a) ** xs, color=st.MainBlue, ls='--', lw=1.4, label='geometric, hit probability 2.5%')
    ax.set_yscale('log')
    ax.set_xlim(0, 400)
    ax.set_ylim(1e-2, 1.05)
    ax.set_xlabel('days between consecutive hits')
    ax.set_ylabel('share of durations longer than d')
    st.legend_outside_bottom(ax, ncol=4, y=-0.2)
    save('ats_ch9_durations', save_it)
    out['geo5'] = float(1 - (1 - a) ** 5)
    return out


def sim_garch(T, omega, alpha, beta, rng, burn=500):
    z = rng.standard_normal(T + burn)
    y = np.empty(T + burn)
    h = omega / (1 - alpha - beta)
    for t in range(T + burn):
        y[t] = np.sqrt(h) * z[t]
        h = omega + alpha * y[t] ** 2 + beta * h
    return y[burn:]


def fig_estrisk_mc(save_it=True, reps=500, a=0.01, Rs=(250, 1000), Ps=(250, 1000, 2500)):
    """Size of the Kupiec and DQ tests at 5% for VaR 1% when the GARCH(1,1) parameters are estimated on R days (fixed
    scheme) and the test uses P out-of-sample days; Normal GARCH data, correct model (Escanciano and Olmo 2010)."""
    def go():
        rng = np.random.default_rng(SEED)
        om, al, be = 0.02, 0.08, 0.90
        z = stats.norm.ppf(a)
        res = {}
        for R in Rs:
            for P in Ps:
                rk = rd = rk0 = rd0 = 0
                hits = []
                for _ in range(reps):
                    y = sim_garch(R + P, om, al, be, rng)
                    p = garch_fit(y[:R])
                    s = garch_sigma(y, p, h0=np.var(y[:R]))[:-1]
                    s0 = garch_sigma(y, np.array([om, al, be]), h0=om / (1 - al - be))[:-1]
                    q, q0 = z * s[R:], z * s0[R:]
                    Yo = y[R:]
                    h, h0 = (Yo <= q).astype(int), (Yo <= q0).astype(int)
                    hits.append(h.mean())
                    rk += kupiec(h, a)[1] < 0.05
                    rk0 += kupiec(h0, a)[1] < 0.05
                    rd += dq_test(Yo, q, a)[1] < 0.05
                    rd0 += dq_test(Yo, q0, a)[1] < 0.05
                res[(R, P)] = dict(kup=rk / reps, kup0=rk0 / reps, dq=rd / reps, dq0=rd0 / reps, hit_sd=float(np.std(hits)),
                                   hit_mean=float(np.mean(hits)))
        return res
    res = cached('estrisk_mc', go)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 3.9), sharey=True)
    x = np.arange(len(Ps))
    for ax, key, ttl in ((axs[0], 'kup', 'Kupiec test, VaR 1%'), (axs[1], 'dq', 'DQ test, VaR 1%')):
        ax.plot(x, [res[(Rs[0], P)][key + '0'] for P in Ps], 'o-', color=st.Forest, lw=1.6, label='true parameters')
        for R, c in zip(Rs, (st.IDAred, st.MainBlue)):
            ax.plot(x, [res[(R, P)][key] for P in Ps], 's-', color=c, lw=1.6, label=f'parameters estimated on R = {R} days')
        ax.axhline(0.05, color=st.DarkText, ls=':', lw=1)
        ax.set_xticks(x)
        ax.set_xticklabels([f'P = {P}' for P in Ps])
        ax.set_title(ttl)
        ax.set_ylabel('rejection rate at 5%')
    h, l = axs[0].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h, l, ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch9_estrisk_mc', save_it)
    return {f'{R}_{P}': v for (R, P), v in res.items()} | dict(reps=reps)


# =============================================================================
# 5. COMPARISON: STRESS PERIODS AND THE MCS
# =============================================================================
def comparison(a=0.025):
    def go():
        out = {}
        for nm in ASSETS:
            r = run_asset(nm)
            L, idx = oos_losses(r, a)
            res = dict(T=int(len(idx)), start=str(idx[0].date()), loss=dict(zip(MODELS, L.mean(0).tolist())),
                       mcs=mcs(L, MODELS, B=1000, block=10)['p'])
            per = {}
            for k, (s, e) in STRESS.items():
                Lp, ip = oos_losses(r, a, s, e)
                if len(ip) < 40 or ip[0] > pd.Timestamp(s) + pd.Timedelta(days=10):
                    continue
                per[k] = dict(T=int(len(ip)), loss=dict(zip(MODELS, Lp.mean(0).tolist())), mcs=mcs(Lp, MODELS, B=1000, block=5)['p'],
                              hits=int(sum((r['y'].loc[s:e].values <= r['fc'][a]['FZ-1F'][0][(r['y'].index >= s) & (r['y'].index <= e)]))))
            res['periods'] = per
            out[nm] = res
        return out
    return cached(f'cmp_{a}', go)


def fig_stress(save_it=True, a=0.025):
    """Average FZ0 loss of each model in the stress periods, minus that of the best model in the period, per asset."""
    cp = comparison(a)
    fig, axs = plt.subplots(1, 5, figsize=(14, 4.2), sharey=True)
    cols = {'2008': st.MainBlue, '2020': st.IDAred, '2022': st.Forest, '2025': st.Purple, 'full': st.Amber}
    for ax, nm in zip(axs, ASSETS):
        per = dict(cp[nm]['periods'])
        per['full'] = dict(loss=cp[nm]['loss'])
        ks = [k for k in ('2008', '2020', '2022', '2025', 'full') if k in per]
        w = 0.8 / len(ks)
        for i, k in enumerate(ks):
            lo = np.array([per[k]['loss'][m] for m in MODELS])
            ax.barh(np.arange(10) + (i - len(ks) / 2 + 0.5) * w, lo - lo.min(), height=w, color=cols[k],
                    label=('whole out-of-sample period' if k == 'full' else k))
        ax.set_yticks(range(10))
        ax.set_yticklabels(MODELS)
        ax.invert_yaxis()
        ax.set_xscale('symlog', linthresh=0.05)
        ax.set_xticks([0, 0.1, 1])
        ax.set_xticklabels(['0', '0.1', '1'])
        ax.set_title(LAB[nm])
        ax.set_xlabel('FZ0 loss minus best')
    handles = [plt.Rectangle((0, 0), 1, 1, color=cols[k]) for k in ('2008', '2020', '2022', '2025', 'full')]
    st.fig_legend_bottom(fig, handles, ['2008-2009', '2020', '2022', '2025', 'whole out-of-sample period'], ncol=5, y=0.0)
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    save('ats_ch9_stress', save_it)
    best = {nm: {k: min(v['loss'], key=v['loss'].get) for k, v in cp[nm]['periods'].items()} | {'full': min(cp[nm]['loss'], key=cp[nm]['loss'].get)}
            for nm in ASSETS}
    return dict(best=best, cmp=cp)


def fig_mcs(save_it=True, a=0.025):
    """90% model confidence sets (FZ0 loss): MCS p-values over the whole out-of-sample period and over 2020 and 2022."""
    cp = comparison(a)
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap([st.IDAred, st.Forest])
    norm = BoundaryNorm([0, 0.10, 1.0], 2)
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.4), sharey=True)
    sizes = {}
    for ax, k, ttl in ((axs[0], 'full', 'whole out-of-sample period'), (axs[1], '2020', '2020'), (axs[2], '2022', '2022')):
        M = np.array([[(cp[nm]['mcs'] if k == 'full' else cp[nm]['periods'][k]['mcs'])[m] for nm in ASSETS] for m in MODELS])
        ax.imshow(M, cmap=cmap, norm=norm, aspect='auto')
        for i in range(10):
            for j in range(5):
                ax.text(j, i, f'{M[i, j]:.2f}', ha='center', va='center', fontsize=8.5, color='white')
        ax.set_xticks(range(5))
        ax.set_xticklabels([LAB[n_] for n_ in ASSETS], rotation=30)
        ax.set_yticks(range(10))
        ax.set_yticklabels(MODELS)
        ax.set_title(ttl)
        sizes[k] = {nm: int((M[:, j] >= 0.10).sum()) for j, nm in enumerate(ASSETS)}
    from matplotlib.patches import Patch
    st.fig_legend_bottom(fig, [Patch(color=st.Forest), Patch(color=st.IDAred)], ['in the 90% MCS (p >= 0.10)', 'eliminated'], ncol=2, y=0.0)
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    save('ats_ch9_mcs', save_it)
    return dict(sizes=sizes)


def fig_overview(save_it=True, a=0.025):
    """S&P 500 returns 2000-2026 with the GAS-1F VaR and ES 2.5% forecasts (parameters fixed on 1990-1999)."""
    r = run_asset('sp500')
    y = r['y']
    sel = y.index >= '2000-01-01'
    idx = y.index[sel]
    fig, ax = plt.subplots(figsize=(12, 4.0))
    ax.plot(idx, y.values[sel], color=st.MainBlue, alpha=0.6, lw=0.5, label='daily return (%)')
    ax.plot(idx, r['fc'][a]['FZ-1F'][0][sel], color=st.Orange, lw=1.0, label='GAS-1F: VaR 2.5% (as a return quantile)')
    ax.plot(idx, r['fc'][a]['FZ-1F'][1][sel], color=st.IDAred, lw=1.0, label='GAS-1F: ES 2.5% (as a tail mean)')
    shade_stress(ax, idx)
    ax.set_ylim(-15, 12)
    ax.set_ylabel('%')
    h, l = ax.get_legend_handles_labels()
    from matplotlib.patches import Patch
    st.legend_outside_bottom(ax, ncol=4, y=-0.12, handles=h + [Patch(color=st.Amber, alpha=0.3)], labels=l + ['stress periods'])
    save('ats_ch9_overview', save_it)
    e = r['fc'][a]['FZ-1F'][1][sel]
    return dict(es_min=float(np.min(e)), es_min_day=str(idx[np.argmin(e)].date()), es_med=float(np.median(e)))


# =============================================================================
# 6. HORIZON: 10-DAY VaR AND THE SQUARE-ROOT-OF-TIME RULE
# =============================================================================
def fhs_hday(name='sp500', h=10, a=0.01, start='2001-01-01', win=2000, refit=250, npath=2000):
    """10-day VaR 1% by filtered historical simulation from a GJR-GARCH(1,1) (Gaussian QMLE, rolling 2000-day window,
    re-estimated every 250 days): bootstrapped standardised residuals pushed through the variance recursion."""
    def go():
        y = returns(name)
        Y = y.values - 0.0
        first = int((y.index < start).sum())
        rng = np.random.default_rng(SEED)
        v1, vh, sig = [], [], []
        p = None
        for t in range(first, len(Y)):
            if p is None or (t - first) % refit == 0:
                seg = Y[t - win:t]
                mu = seg.mean()
                p = garch_fit(seg - mu, gjr=True)
                s = garch_sigma(seg - mu, p, gjr=True)
                zres = (seg - mu) / s[:-1]
                hist = Y[:t] - mu
            # one-step variance from the filtered path up to t-1
            st_ = garch_sigma(Y[t - win:t] - mu, p, gjr=True)[-1]
            hnext = st_ ** 2
            zz = rng.choice(zres, size=(npath, h))
            hh = np.full(npath, hnext)
            cum = np.zeros(npath)
            for k in range(h):
                eps = np.sqrt(hh) * zz[:, k]
                cum += mu + eps
                hh = p[0] + (p[1] + p[2] * (eps < 0)) * eps ** 2 + p[3] * hh
            v1.append(-(mu + st_ * np.quantile(zres, a)))
            vh.append(-np.quantile(cum, a))
            sig.append(st_)
        idx = y.index[first:]
        return pd.DataFrame({'var1': v1, 'varh': vh, 'sig': sig}, index=idx), y
    return cached(f'fhs_{name}_{h}', go)


def fig_sqrt(save_it=True, h=10, a=0.01, npath=2000):
    """Ratio of the 10-day VaR 1% by FHS to sqrt(10) x the 1-day VaR 1%, S&P 500, 2001-2026; non-overlapping backtest."""
    df, y = fhs_hday('sp500', h, a, npath=npath)
    ratio = df['varh'] / (np.sqrt(h) * df['var1'])
    Y = y.values
    pos = np.searchsorted(y.index, df.index)
    fwd = np.array([Y[p:p + h].sum() if p + h <= len(Y) else np.nan for p in pos])
    ok = np.isfinite(fwd)
    nonov = np.arange(0, ok.sum(), h)
    f = fwd[ok][nonov]
    vh = df['varh'].values[ok][nonov]
    vs = np.sqrt(h) * df['var1'].values[ok][nonov]
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9), gridspec_kw=dict(width_ratios=[1.6, 1]))
    axs[0].plot(df.index, ratio, color=st.MainBlue, lw=0.8, label='10-day VaR 1% (FHS) / (sqrt(10) x 1-day VaR 1%)')
    axs[0].axhline(1, color=st.IDAred, ls='--', lw=1.2, label='square-root-of-time rule')
    shade_stress(axs[0], df.index)
    axs[0].set_ylabel('ratio')
    vol = df['sig'] * np.sqrt(252)
    axs[1].scatter(vol, ratio, s=3, color=st.MainBlue, alpha=0.4, label='one day')
    axs[1].axhline(1, color=st.IDAred, ls='--', lw=1.2)
    axs[1].set_xscale('log')
    axs[1].set_xlabel('forecast volatility today (% per year, log scale)')
    axs[1].set_ylabel('ratio')
    st.legend_outside_bottom(axs[0], ncol=2, y=-0.15)
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.22)
    plt.tight_layout()
    save('ats_ch9_sqrt', save_it)
    lo = vol < vol.quantile(0.2)
    hi = vol > vol.quantile(0.8)
    return dict(r_lo=float(ratio[lo].median()), r_hi=float(ratio[hi].median()), r_med=float(ratio.median()),
                r_min=float(ratio.min()), r_max=float(ratio.max()), n=int(len(f)),
                hit_fhs=float((f < -vh).mean()), hit_sqrt=float((f < -vs).mean()),
                kup_fhs=kupiec((f < -vh).astype(int), a)[1], kup_sqrt=kupiec((f < -vs).astype(int), a)[1],
                n_fhs=int((f < -vh).sum()), n_sqrt=int((f < -vs).sum()))


# =============================================================================
# 7. MODEL RISK AND ESTIMATION RISK
# =============================================================================
def six_models(name, a=0.01, start='2002-01-01', win=1000, refit=125):
    """VaR 1% from six standard model families, rolling 1000-day windows: historical simulation, Normal with the window
    volatility, EWMA (lambda = 0.94), GARCH-N, GARCH-t, filtered HS (GARCH-EDF)."""
    def go():
        y = returns(name)
        Y = y.values
        first = max(int((y.index < start).sum()), win + 1)
        out = {k: [] for k in ('HS', 'MA-N', 'EWMA', 'GARCH-N', 'GARCH-t', 'FHS')}
        zN = stats.norm.ppf(a)
        ew = np.var(Y[first - win:first])
        for t in range(first - win, first):
            ew = 0.94 * ew + 0.06 * Y[t] ** 2
        for t in range(first, len(Y)):
            seg = Y[t - win:t]
            if (t - first) % refit == 0:
                mu = seg.mean()
                pn = garch_fit(seg - mu)
                pt = garch_fit(seg - mu, dist='t')
                sn = garch_sigma(seg - mu, pn)
                zres = (seg - mu) / sn[:-1]
                qf = np.quantile(zres, a)
                tq = t_std_var_es(a, pt[-1])[0]
            sn_t = garch_sigma(seg - mu, pn)[-1]
            st_t = garch_sigma(seg - mu, pt[:3])[-1]
            out['HS'].append(-np.quantile(seg, a))
            out['MA-N'].append(-(seg.mean() + seg.std() * zN))
            out['EWMA'].append(-np.sqrt(ew) * zN)
            out['GARCH-N'].append(-(mu + sn_t * zN))
            out['GARCH-t'].append(-(mu + st_t * tq))
            out['FHS'].append(-(mu + sn_t * qf))
            ew = 0.94 * ew + 0.06 * Y[t] ** 2
        return pd.DataFrame(out, index=y.index[first:]), y
    return cached(f'six_{name}', go)


def fig_riskratio(save_it=True):
    """Risk ratio max/min of the six VaR 1% forecasts (Danielsson et al. 2016), S&P 500 and BET, 2002-2026."""
    fig, ax = plt.subplots(figsize=(12, 3.9))
    out = {}
    for nm, c in (('sp500', st.MainBlue), ('bet', st.IDAred)):
        df, y = six_models(nm)
        rr = df.max(axis=1) / df.min(axis=1)
        ax.plot(rr.index, rr.rolling(21).median(), color=c, lw=1.2, label=f'{LAB[nm]}: risk ratio (21-day median)')
        hits = {k: float((y.reindex(df.index).values < -df[k].values).mean()) for k in df}
        out[nm] = dict(med=float(rr.median()), q90=float(rr.quantile(0.9)), mx=float(rr.max()), mx_day=str(rr.idxmax().date()),
                       s2008=float(rr.loc['2008-09-01':'2009-03-31'].median()), s2020=float(rr.loc['2020-02-19':'2020-06-30'].median()),
                       calm=float(rr.loc['2017-01-01':'2017-12-31'].median()), hits=hits,
                       argmax=df.idxmax(axis=1).value_counts(normalize=True).to_dict(), argmin=df.idxmin(axis=1).value_counts(normalize=True).to_dict())
    shade_stress(ax, rr.index)
    ax.axhline(1, color=st.DarkText, ls=':', lw=1)
    ax.set_ylabel('max / min VaR 1%')
    st.legend_outside_bottom(ax, ncol=2, y=-0.15)
    save('ats_ch9_riskratio', save_it)
    return out


def fig_es_ci(save_it=True, a=0.025, B=150, win=2000):
    """Estimation risk: GARCH-t ES 2.5% forecasts of the S&P 500 at half-year ends 2019-2026 with 90% parametric
    bootstrap intervals (re-estimation on simulated paths, the forecast conditional on the observed history)."""
    def go():
        y = returns('sp500')
        Y = y.values
        dates = pd.date_range('2019-06-30', '2026-06-30', freq='6ME')
        rng = np.random.default_rng(SEED)
        rows = []
        for d in dates:
            t = int((y.index <= d).sum())
            seg = Y[t - win:t]
            mu = seg.mean()
            p = garch_fit(seg - mu, dist='t')
            s = garch_sigma(seg - mu, p[:3])
            zq, ze = t_std_var_es(a, p[-1])
            es = -(mu + s[-1] * ze)
            bs = []
            for _ in range(B):
                nu = p[-1]
                zz = rng.standard_t(nu, win) * np.sqrt((nu - 2) / nu)
                hsim, ysim = p[0] / (1 - p[1] - p[2]), np.empty(win)
                for k in range(win):
                    ysim[k] = np.sqrt(hsim) * zz[k]
                    hsim = p[0] + p[1] * ysim[k] ** 2 + p[2] * hsim
                r_ = optimize.minimize(garch_negll, p, args=(ysim, 't', False), method='Nelder-Mead', options={'maxiter': 3000})
                pb = r_.x
                sb = garch_sigma(seg - mu, pb[:3])[-1]
                bs.append(-(mu + sb * t_std_var_es(a, max(pb[-1], 2.1))[1]))
            bs = np.array(bs)
            rows.append(dict(date=str(d.date()), es=float(es), lo=float(np.quantile(bs, 0.05)), hi=float(np.quantile(bs, 0.95)),
                             nu=float(p[-1])))
        return rows
    rows = cached('es_ci', go)
    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    fig, ax = plt.subplots(figsize=(11, 3.9))
    ax.errorbar(df['date'], df['es'], yerr=[df['es'] - df['lo'], df['hi'] - df['es']], fmt='o', color=st.MainBlue,
                ecolor=st.IDAred, capsize=4, lw=1.4, label='GARCH-t ES 2.5% forecast with 90% bootstrap interval')
    ax.set_ylabel('ES 2.5% (%, loss)')
    st.legend_outside_bottom(ax, ncol=1, y=-0.15)
    save('ats_ch9_es_ci', save_it)
    rel = (df['hi'] - df['lo']) / df['es']
    return dict(rows=rows, rel_med=float(rel.median()), rel_max=float(rel.max()), rel_min=float(rel.min()),
                rel_max_day=str(df['date'][rel.idxmax()].date()))


# =============================================================================
# 8. EXTREMES FOR DEPENDENT DATA; CONFORMAL CALIBRATION
# =============================================================================
def fig_extremal(save_it=True, q=0.95):
    """Extremal index (Ferro-Segers intervals estimator) of daily losses above their 95% quantile, raw and filtered by
    the in-sample ARMA-GARCH (standardised residuals), whole sample."""
    out = {}
    for nm in ASSETS:
        r = run_asset(nm)
        L = -r['y'].values
        z = -(r['y'].values - r['mu']) / r['sig']
        out[nm] = dict(raw=extremal_index(L, np.quantile(L, q)), filt=extremal_index(z, np.quantile(z, q)))
    fig, ax = plt.subplots(figsize=(10, 3.8))
    x = np.arange(5)
    ax.bar(x - 0.18, [out[k]['raw'] for k in ASSETS], width=0.36, color=st.IDAred, label='raw losses')
    ax.bar(x + 0.18, [out[k]['filt'] for k in ASSETS], width=0.36, color=st.MainBlue, label='GARCH-filtered losses')
    ax.axhline(1, color=st.DarkText, ls=':', lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([LAB[k] for k in ASSETS])
    ax.set_ylabel('extremal index theta')
    st.legend_outside_bottom(ax, ncol=2, y=-0.15)
    save('ats_ch9_extremal', save_it)
    return out


def conformal_base(nm, a=0.01, gamma=0.005, start='2016-01-01', win=1000, refit=250):
    """GARCH-N VaR 1% (rolling 1000-day window, re-estimated every 250 days) from 2016 and its adaptive conformal
    correction (Gibbs and Candes 2021) with step gamma."""
    def go():
        y = returns(nm)
        Y = y.values
        first = int((y.index < start).sum())
        mus, sig = np.empty(len(Y) - first), np.empty(len(Y) - first)
        for t in range(first, len(Y)):
            seg = Y[t - win:t]
            if (t - first) % refit == 0:
                mu = seg.mean()
                p = garch_fit(seg - mu)
            mus[t - first] = mu
            sig[t - first] = garch_sigma(seg - mu, p)[-1]
        Yo = Y[first:]
        base = (Yo < mus + sig * stats.norm.ppf(a)).astype(float)
        f = lambda t, at: float(Yo[t] < mus[t] + sig[t] * stats.norm.ppf(min(max(at, 1e-5), 0.5)))
        at, err = aci_levels(f, a, gamma, len(Yo))
        return pd.DataFrame({'y': Yo, 'mu': mus, 'sig': sig, 'base': base, 'aci': err, 'at': at[:-1]}, index=y.index[first:])
    return cached(f'confb_{nm}', go)


def fig_conformal(save_it=True, a=0.01):
    """Rolling 250-day hit rates of the GARCH-N VaR 1% and of its ACI correction (gamma = 0.005), Bitcoin and BET."""
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9), sharey=True)
    out = {}
    for ax, nm in zip(axs, ('btc', 'bet')):
        df = conformal_base(nm)
        ax.plot(df.index, df['base'].rolling(250).mean() * 100, color=st.IDAred, lw=1.3, label='GARCH-N VaR 1%')
        ax.plot(df.index, df['aci'].rolling(250).mean() * 100, color=st.MainBlue, lw=1.3, label='with adaptive conformal correction')
        ax.axhline(100 * a, color=st.DarkText, ls=':', lw=1)
        ax.set_title(LAB[nm])
        ax.set_ylabel('hit rate over the last 250 days (%)')
        out[nm] = dict(base=float(df['base'].mean()), aci=float(df['aci'].mean()), at_min=float(df['at'].min()),
                       at_end=float(df['at'].iloc[-1]), kup_base=kupiec(df['base'].astype(int).values, a)[1],
                       kup_aci=kupiec(df['aci'].astype(int).values, a)[1],
                       cc_base=christoffersen(df['base'].astype(int).values, a)['p_cc'],
                       cc_aci=christoffersen(df['aci'].astype(int).values, a)['p_cc'], T=int(len(df)),
                       rmax_base=float(df['base'].rolling(250).mean().max()), rmax_aci=float(df['aci'].rolling(250).mean().max()))
    h, l = axs[0].get_legend_handles_labels()
    st.fig_legend_bottom(fig, h, l, ncol=2, y=0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch9_conformal', save_it)
    return out


# =============================================================================
# 9. AI MINI-CASE
# =============================================================================
def fig_ai_case(save_it=True):
    """Is there a ``best'' ES model? Winner (lowest average FZ0 loss) and 90% MCS size for each asset, level
    (2.5%, 5%) and period (whole out-of-sample period; before 2020; from 2020)."""
    rows = []
    for nm in ASSETS:
        r = run_asset(nm)
        for a in (0.025, 0.05):
            for per, (s, e) in (('whole', (None, None)), ('before 2020', (None, '2019-12-31')), ('from 2020', ('2020-01-01', None))):
                L, idx = oos_losses(r, a, s, e)
                if len(idx) < 500:
                    continue
                m = L.mean(0)
                ms = mcs(L, MODELS, B=500, block=10)
                rows.append(dict(asset=nm, a=a, per=per, win=MODELS[int(np.argmin(m))], size=len(ms['set']),
                                 fz1f_in=('FZ-1F' in ms['set'])))
    t = pd.DataFrame(rows)
    wins = t['win'].value_counts()
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.9), gridspec_kw=dict(width_ratios=[1.2, 1]))
    axs[0].bar(range(len(MODELS)), [wins.get(m, 0) for m in MODELS], color=st.MainBlue)
    axs[0].set_xticks(range(len(MODELS)))
    axs[0].set_xticklabels(MODELS, rotation=45, ha='right')
    axs[0].set_ylabel('cells won (lowest FZ0 loss)')
    axs[0].set_title(f'{len(t)} cells: asset x level x period')
    axs[1].hist(t['size'], bins=np.arange(0.5, 11.5, 1), color=st.Forest, rwidth=0.8, label='size of the 90% MCS')
    axs[1].set_xlabel('number of models in the 90% MCS')
    axs[1].set_ylabel('cells')
    st.legend_outside_bottom(axs[1], ncol=1, y=-0.22)
    plt.tight_layout()
    save('ats_ch9_ai_case', save_it)
    return dict(n=int(len(t)), wins=wins.to_dict(), size_med=float(t['size'].median()), size_min=int(t['size'].min()),
                size_max=int(t['size'].max()), fz1f_in=int(t['fz1f_in'].sum()), n_win_models=int((wins > 0).sum()),
                rows=rows)


if __name__ == '__main__':
    st.apply()
    N = {}
    only = sys.argv[1:]
    path = os.path.join(HERE, 'ch9_numbers.json')
    if os.path.exists(path):
        N = json.load(open(path))
    for name, f in [('contour', fig_fz0_contour), ('levelsets', fig_level_sets), ('overview', fig_overview),
                    ('caviar', fig_caviar), ('nic', fig_nic), ('pzcrep', lambda: cached('pzc_rep', pzc_replication)),
                    ('pzctable', fig_pzc_table), ('pzcpaths', fig_pzc_paths), ('dm', fig_dm), ('murphy', fig_murphy),
                    ('esreg', fig_esreg), ('backtests', fig_backtests), ('durations', fig_durations),
                    ('estrisk', fig_estrisk_mc), ('stress', fig_stress), ('mcs', fig_mcs), ('sqrt', fig_sqrt),
                    ('riskratio', fig_riskratio), ('esci', fig_es_ci), ('extremal', fig_extremal),
                    ('conformal', fig_conformal), ('ai', fig_ai_case)]:
        if only and name not in only:
            continue
        print(name, flush=True)
        N[name] = f()
        with open(path, 'w') as fh:
            json.dump(N, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else (list(o) if isinstance(o, tuple) else float(o)))
    print('written ch9_numbers.json')
