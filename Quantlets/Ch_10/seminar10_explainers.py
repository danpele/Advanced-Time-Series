"""
seminar10_explainers.py -- Explanatory (primer) charts for Seminar 10 (ATS): long memory and rough volatility
=============================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 10, which takes
place BEFORE Lecture 10. All charts use SIMULATED data only (fixed seeds) and parameters that differ from those of
the exercises: they illustrate the concepts (hyperbolic and exponential decay, fractional weights, the variance of
the mean, the log-periodogram, the bias-variance trade-off of the bandwidth, level shifts that mimic long memory,
the Qu partial sums, fractional Brownian motion, moment scaling, the RFSV kernel, the QLIKE loss) and contain no
exercise answers.

Output: charts/ch10_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each sized for
its box on the slides (ats_style.fit_for_slide), and Quantlets/Ch_10/seminar10_explainers.json (the few numbers the
primer slides quote about these simulations).

Run:  python3 Quantlets/Ch_10/seminar10_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_style as st                                  # noqa: E402
from lm_core import (arfima_acf, circulant_sim, fgn_acov, fbm, frac_weights, gph, lbias_constant, local_whittle,   # noqa: E402
                     mse_opt_m, periodogram, rfsv_kernel, sim_arfima, variogram)

st.apply()
MainBlue, IDAred, Forest, Amber, Navy, BandBlue = st.MainBlue, st.IDAred, st.Forest, st.Amber, st.DarkText, '#C5D2E8'
CHART_DIR = st.CHART_DIR
TW, TH = 409.72 / 72, 214.79 / 72                       # \textwidth, \textheight of the decks (inches)
TWO = (0.50 * TW, 0.80 * TH)                            # chart in the left column of a two-column primer frame
FULL = (0.96 * TW, 0.62 * TH)                           # full-width chart above three or four bullets
OUT = {}


def save(fig, name, box):
    st.fit_for_slide(fig, name, box=box)
    st.check_no_grey(fig)
    os.makedirs(CHART_DIR, exist_ok=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print(f'   saved {name}')


def legend_below(fig, ncol=3):
    st.fig_legend_bottom(fig, ncol=ncol)


# =============================================================================
# 1. long memory against short memory: a path and the ACF (log-log)
# =============================================================================
def fig_acf(d=0.4, n=1000, seed=7):
    rng = np.random.default_rng(seed)
    phi = d / (1 - d)                                  # AR(1) with the same lag-1 autocorrelation
    x = sim_arfima(n, d, rng)[0]
    e = rng.standard_normal(n + 500)
    y = np.zeros_like(e)
    for t in range(1, len(e)):
        y[t] = phi * y[t - 1] + e[t]
    y = y[500:] * np.sqrt(1 - phi ** 2)
    x = (x - x.mean()) / x.std()
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    ax[0].plot(y + 4, color=Amber, lw=0.7, label=f'AR(1), $\\phi = {phi:.2f}$')
    ax[0].plot(x - 4, color=MainBlue, lw=0.7, label=f'ARFIMA$(0, {d}, 0)$')
    ax[0].set_yticks([])
    ax[0].set_xlabel('$t$')
    ax[0].set_title('Simulated paths (same variance, shifted)', loc='left')
    k = np.arange(1, 501)
    rho_f = arfima_acf(d, 501)[1:]
    ax[1].loglog(k, rho_f, color=MainBlue, lw=1.6)
    ax[1].loglog(k, phi ** k, color=Amber, lw=1.6)
    from scipy.special import gamma
    ax[1].loglog(k, gamma(1 - d) / gamma(d) * k ** (2 * d - 1), color=IDAred, ls='--', lw=1.1,
                 label=r'$\frac{\Gamma(1-d)}{\Gamma(d)}k^{2d-1}$')
    ax[1].set_ylim(1e-4, 1.2)
    ax[1].set_xlabel('lag $k$ (log scale)')
    ax[1].set_ylabel(r'$\rho(k)$ (log scale)')
    ax[1].set_title('Autocorrelations', loc='left')
    legend_below(fig, ncol=3)
    save(fig, 'ch10_sem_primer_acf', FULL)
    OUT['acf'] = dict(d=d, phi=phi, rho100_f=float(rho_f[99]), rho100_ar=float(phi ** 100))


# =============================================================================
# 2. fractional differencing weights
# =============================================================================
def fig_weights():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    k = np.arange(0, 11)
    for d, c in ((0.15, Forest), (0.3, MainBlue), (0.45, IDAred)):
        w = frac_weights(d, 2001)
        ax[0].plot(k, w[:11], 'o-', color=c, ms=3.5, lw=1.1, label=f'$d = {d}$')
        kk = np.arange(1, 2001)
        ax[1].loglog(kk, np.abs(w[1:]), color=c, lw=1.4)
    ax[0].axhline(0, color=Navy, lw=0.6)
    ax[0].set_xlabel('$k$')
    ax[0].set_ylabel(r'$\pi_k$')
    ax[0].set_title(r'Weights $\pi_0, \dots, \pi_{10}$ of $(1 - L)^d$', loc='left')
    ax[1].set_xlabel('$k$ (log scale)')
    ax[1].set_ylabel(r'$|\pi_k|$ (log scale)')
    ax[1].set_title(r'Slow decay: $|\pi_k| \sim k^{-d-1}/|\Gamma(-d)|$', loc='left')
    legend_below(fig, ncol=3)
    save(fig, 'ch10_sem_primer_weights', FULL)


# =============================================================================
# 3. the standard deviation of the mean
# =============================================================================
def sd_ratio(d, n):
    g = arfima_acf(d, n)
    k = np.arange(1, n)
    var = (1 + 2 * np.sum((1 - k / n) * g[1:])) / n
    return np.sqrt(var * n)


def fig_mean():
    ns = np.unique(np.round(np.logspace(1, 4, 25)).astype(int))
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    for d, c in ((0.0, Navy), (0.1, Forest), (0.25, MainBlue), (0.4, IDAred)):
        r = [sd_ratio(d, n) if d > 0 else 1.0 for n in ns]
        ax.loglog(ns, r, color=c, lw=1.6, label=f'$d = {d}$')
    ax.set_xlabel('sample size $n$ (log scale)')
    ax.set_ylabel(r'$\mathrm{SD}(\bar X_n)\,/\sqrt{\gamma(0)/n}$')
    ax.set_title('True SD of the mean over the i.i.d. formula', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch10_sem_primer_mean', TWO)
    OUT['mean'] = {str(d): float(sd_ratio(d, 1000)) for d in (0.1, 0.25, 0.4)}


# =============================================================================
# 4. log-periodogram and the GPH regression
# =============================================================================
def fig_periodogram(d=0.35, n=4096, seed=21):
    rng = np.random.default_rng(seed)
    x = sim_arfima(n, d, rng)[0]
    lam, I = periodogram(x)
    m = int(np.floor(n ** 0.65))
    dg = gph(x, m)[0]
    dl = local_whittle(x, m)[0]
    f = (2 * np.sin(lam / 2)) ** (-2 * d) / (2 * np.pi)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.loglog(lam[m:], I[m:], '.', color=BandBlue, ms=2.0, label='_')
    ax.loglog(lam[:m], I[:m], '.', color=MainBlue, ms=2.4, label=f'$I(\\lambda_j)$, $j \\leq m = {m}$')
    ax.loglog(lam, f, color=IDAred, lw=1.4, label=r'true $f(\lambda)$')
    Xr = -np.log(4 * np.sin(lam[:m] / 2) ** 2)
    a = np.mean(np.log(I[:m])) - dg * np.mean(Xr)
    ax.loglog(lam[:m], np.exp(a + dg * Xr), color=Amber, lw=1.8, label='GPH fit (slope $-2\\hat d$)')
    ax.axvline(lam[m - 1], color=Forest, ls='--', lw=1.0)
    ax.set_xlabel(r'frequency $\lambda$ (log scale)')
    ax.set_ylabel('periodogram (log scale)')
    ax.set_title(f'ARFIMA$(0, {d}, 0)$, $n = {n}$', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch10_sem_primer_periodogram', TWO)
    OUT['per'] = dict(d=d, n=n, m=m, gph=dg, lw=dl)


# =============================================================================
# 5. bias, standard deviation and RMSE of local Whittle against the bandwidth
# =============================================================================
def fig_bandwidth(phi=0.3, n=2000):
    C = lbias_constant(phi)
    m = np.arange(10, n // 2)
    bias = C * (m / n) ** 2
    sd = 1 / (2 * np.sqrt(m))
    rmse = np.sqrt(bias ** 2 + sd ** 2)
    ms = mse_opt_m(n, C)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.plot(m, bias, color=IDAred, lw=1.6, label=r'bias $C(m/n)^2$')
    ax.plot(m, sd, color=MainBlue, lw=1.6, label=r'SD $1/(2\sqrt{m})$')
    ax.plot(m, rmse, color=Navy, lw=1.8, ls='--', label=r'RMSE')
    ax.axvline(ms, color=Forest, lw=1.1, ls=':', label=f'$m^* = {ms:.0f}$')
    ax.set_ylim(0, 0.2)
    ax.set_xlabel('bandwidth $m$')
    ax.set_title(f'ARFIMA$(1, d, 0)$, $\\phi = {phi}$, $n = {n}$', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch10_sem_primer_bandwidth', TWO)
    OUT['bw'] = dict(phi=phi, n=n, C=C, mopt=ms, a=np.log(ms) / np.log(n))


# =============================================================================
# 6. rare level shifts mimic long memory
# =============================================================================
def fig_shifts(q=0.99, mu=0.8, n=4000, seed=5):
    rng = np.random.default_rng(seed)
    s = np.empty(n)
    s[0] = 1
    u = rng.random(n)
    for t in range(1, n):
        s[t] = s[t - 1] if u[t] < q else -s[t - 1]
    x = mu * s + rng.standard_normal(n)
    m = int(np.floor(n ** 0.65))
    dl = local_whittle(x, m)[0]
    xc = x - x.mean()
    K = 300
    acf = np.array([xc[k:] @ xc[:-k] for k in range(1, K + 1)]) / (xc @ xc)
    k = np.arange(1, K + 1)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    ax[0].plot(x, color=MainBlue, lw=0.5, label='$X_t = \\mu S_t + \\varepsilon_t$')
    ax[0].plot(mu * s, color=IDAred, lw=1.4, label=r'level $\mu S_t$')
    ax[0].set_xlabel('$t$')
    ax[0].set_title(f'Markov switching: stay probability $q = {q}$', loc='left')
    ax[1].plot(k, acf, color=MainBlue, lw=1.3, label='sample ACF')
    ax[1].plot(k, mu ** 2 / (mu ** 2 + 1) * (2 * q - 1) ** k, color=Amber, lw=1.6, ls='--',
               label=r'$\frac{\mu^2}{\mu^2+1}(2q-1)^k$')
    ax[1].axhline(0, color=Navy, lw=0.6)
    ax[1].set_xlabel('lag $k$')
    ax[1].set_title(f'Slow decay; local Whittle $\\hat d = {dl:.2f}$', loc='left')
    legend_below(fig, ncol=2)
    save(fig, 'ch10_sem_primer_shifts', FULL)
    OUT['shift'] = dict(q=q, mu=mu, n=n, d=dl)


# =============================================================================
# 7. the Qu partial-sum process
# =============================================================================
def qu_path(x, m):
    lam, I = periodogram(x, m)
    d, _ = local_whittle(x, m)
    G = np.mean(lam ** (2 * d) * I)
    nu = np.log(lam) - np.mean(np.log(lam))
    S = np.cumsum(nu * (lam ** (2 * d) * I / G - 1)) / np.sqrt(nu @ nu)
    return np.arange(1, m + 1) / m, np.abs(S), d


def fig_qu(n=4000, seed=9):
    rng = np.random.default_rng(seed)
    m = int(np.floor(n ** 0.7))
    x1 = sim_arfima(n, 0.35, rng)[0]
    s = np.empty(n)
    s[0] = 1
    u = rng.random(n)
    for t in range(1, n):
        s[t] = s[t - 1] if u[t] < 0.997 else -s[t - 1]
    x2 = 0.8 * s + rng.standard_normal(n)
    crit = json.load(open(os.path.join(HERE, 'sem10_results.json')))['B1']['crit']['0.95']
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    r, S1, d1 = qu_path(x1, m)
    r, S2, d2 = qu_path(x2, m)
    ax.plot(r, S1, color=MainBlue, lw=1.4, label=f'ARFIMA, $\\hat d = {d1:.2f}$')
    ax.plot(r, S2, color=IDAred, lw=1.4, label=f'level shifts, $\\hat d = {d2:.2f}$')
    ax.axhline(crit, color=Forest, ls='--', lw=1.1, label=f'5% critical value {crit:.2f}')
    ax.axvspan(0, 0.02, color=Amber, alpha=0.3, lw=0, label=r'trimmed $r < \varepsilon$')
    ax.set_xlabel('share $r$ of the $m$ lowest frequencies')
    ax.set_ylabel('standardised partial sum')
    ax.set_title(f'$n = {n}$, $m = n^{{0.7}} = {m}$', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch10_sem_primer_qu', TWO)
    OUT['qu'] = dict(W1=float(S1[int(0.02 * m):].max()), W2=float(S2[int(0.02 * m):].max()), d1=d1, d2=d2, crit=crit)


# =============================================================================
# 8. fractional Brownian motion and the autocorrelations of its increments
# =============================================================================
def fig_fbm(n=1000, seed=3):
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    for i, (H, c) in enumerate(((0.1, IDAred), (0.5, MainBlue), (0.8, Forest))):
        B = fbm(n, H, np.random.default_rng(seed), T=1.0)[0]
        ax[0].plot(np.linspace(0, 1, n + 1), B - 1.4 * i, color=c, lw=0.8, label=f'$H = {H}$')
        k = np.arange(0, 11)
        ax[1].plot(k[1:] + (i - 1) * 0.22, fgn_acov(H, 11)[1:], 'o', color=c, ms=4)
        ax[1].vlines(k[1:] + (i - 1) * 0.22, 0, fgn_acov(H, 11)[1:], color=c, lw=1.4)
    ax[0].set_xlabel('$t$')
    ax[0].set_yticks([])
    ax[0].set_title(r'Paths of $W^H_t$ (shifted vertically)', loc='left')
    ax[1].axhline(0, color=Navy, lw=0.6)
    ax[1].set_xlabel('lag $k$')
    ax[1].set_ylabel(r'$\rho(k)$ of the increments')
    ax[1].set_title('Fractional Gaussian noise', loc='left')
    legend_below(fig, ncol=3)
    save(fig, 'ch10_sem_primer_fbm', FULL)


# =============================================================================
# 9. moment scaling of a rough log volatility
# =============================================================================
def fig_scaling(H=0.12, nu=0.3, n=4000, seed=17):
    rng = np.random.default_rng(seed)
    x = nu * np.cumsum(circulant_sim(fgn_acov(H, n), rng)[0])     # log sigma_t: nu W^H on a daily grid
    lags = np.arange(1, 51)
    qs = (0.5, 1.0, 2.0, 3.0)
    cols = (Forest, MainBlue, IDAred, Amber)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    zeta = []
    for q, c in zip(qs, cols):
        mq = variogram(x, lags, q)
        b, a = np.polyfit(np.log(lags), np.log(mq), 1)
        zeta.append(b)
        ax[0].loglog(lags, mq, 'o', color=c, ms=2.5, label=f'$q = {q:g}$')
        ax[0].loglog(lags, np.exp(a) * lags ** b, color=c, lw=1.1)
    zeta = np.array(zeta)
    Hhat = float(np.array(qs) @ zeta / (np.array(qs) @ np.array(qs)))
    ax[0].set_xlabel(r'lag $\Delta$ in days (log scale)')
    ax[0].set_ylabel(r'$m(q, \Delta)$ (log scale)')
    ax[0].set_title(r'Moments of $|\log\sigma_{t+\Delta} - \log\sigma_t|^q$', loc='left')
    qq = np.linspace(0, 3.2, 10)
    ax[1].plot(qs, zeta, 'o', color=MainBlue, ms=5, label=r'slopes $\zeta_q$')
    ax[1].plot(qq, Hhat * qq, color=IDAred, lw=1.3, label=f'$\\zeta_q = \\hat H q$, $\\hat H = {Hhat:.3f}$')
    ax[1].set_xlabel('moment order $q$')
    ax[1].set_ylabel(r'$\zeta_q$')
    ax[1].set_title(f'Simulated rough log volatility, $H = {H}$', loc='left')
    legend_below(fig, ncol=3)
    save(fig, 'ch10_sem_primer_scaling', FULL)
    OUT['scal'] = dict(H=H, Hhat=Hhat, zeta=zeta.tolist())


# =============================================================================
# 10. RFSV kernel against HAR weights
# =============================================================================
def fig_kernel(K=100):
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    k = np.arange(1, K + 1)
    for H, c in ((0.05, IDAred), (0.3, MainBlue)):
        w = rfsv_kernel(H, 1, K=250)[:K]
        ax.semilogx(k, w, color=c, lw=1.6, label=f'RFSV, $H = {H}$, $h = 1$')
    bd, bw, bm = 0.4, 0.35, 0.25                      # illustrative HAR coefficients that sum to one
    har = np.zeros(K)
    har[0] += bd
    har[:5] += bw / 5
    har[:22] += bm / 22
    ax.step(k, har, where='post', color=Forest, lw=1.4, label=r'HAR, $(\beta_d, \beta_w, \beta_m) = (0.4, 0.35, 0.25)$')
    ax.set_xlabel('days back $k + 1$ (log scale)')
    ax.set_ylabel('weight on $\\log\\sigma^2_{t-k}$')
    ax.set_title('Weights on past log variance', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch10_sem_primer_kernel', TWO)


# =============================================================================
# 11. QLIKE against the squared error
# =============================================================================
def fig_qlike():
    F = np.linspace(0.25, 3, 400)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.plot(F, 1 / F - np.log(1 / F) - 1, color=MainBlue, lw=1.8, label=r'QLIKE $= RV/F - \log(RV/F) - 1$')
    ax.plot(F, (F - 1) ** 2, color=Amber, lw=1.6, ls='--', label=r'squared error $(RV - F)^2$')
    ax.axvline(1, color=Navy, lw=0.6, ls=':')
    ax.set_ylim(0, 1.6)
    ax.set_xlabel('forecast $F$ (realised $RV = 1$)')
    ax.set_ylabel('loss')
    ax.set_title('Under-prediction costs more in QLIKE', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch10_sem_primer_qlike', TWO)


if __name__ == '__main__':
    fig_acf()
    fig_weights()
    fig_mean()
    fig_periodogram()
    fig_bandwidth()
    fig_shifts()
    fig_qu()
    fig_fbm()
    fig_scaling()
    fig_kernel()
    fig_qlike()
    with open(os.path.join(HERE, 'seminar10_explainers.json'), 'w') as fh:
        json.dump(OUT, fh, indent=1)
    print(json.dumps(OUT, indent=1))
