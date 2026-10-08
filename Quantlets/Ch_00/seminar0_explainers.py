"""
seminar0_explainers.py -- Explanatory (primer) charts for Seminar 0 (ATS): inference for dependent data
=========================================================================================================
Teaching charts for the slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 0, which takes
place BEFORE Lecture 0. All charts use SIMULATED data only (fixed seeds): they illustrate the concepts
(autocorrelation, the long-run variance, the size of the naive test, kernel estimators, fixed-b and Student-t
critical values, block bootstraps, Monte Carlo error, GARCH, spurious regression, multiple testing) and
contain no exercise answers.

Output: charts/ch0_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each
sized for its box on the slides (text at least 6.4 pt there).

Run:  python3 Quantlets/Ch_00/seminar0_explainers.py
      (run it again after the seminar decks are regenerated, so that every chart gets its slide box)

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'Quantlets', 'common'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import ats_style as st                      # noqa: E402
from chart_boxes import boxes as deck_boxes  # noqa: E402

st.SLIDE_MIN_PT = 6.4                        # smallest chart text on the slide (pt)
st.SLIDE_BASE_PT = 6.8                       # usual tick-label size on the slide (pt)
CHART_DIR = os.path.join(REPO, 'charts')
SEED = 2026
B, R, G, A, P, N = st.MainBlue, st.IDAred, st.Forest, st.Amber, st.Purple, st.DarkText
_BOX = None


def save(fig, name):
    """Size the figure for its box on the slides (read from the decks), then save PDF and PNG."""
    global _BOX
    if _BOX is None:
        _BOX = deck_boxes()
    st.check_no_grey(fig)
    box = _BOX.get(name)
    if box:
        st.fit_for_slide(fig, name, box)
    else:
        print(f'   {name}: not on the slides yet (run again after building the decks)')
    os.makedirs(CHART_DIR, exist_ok=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print(f'   saved {name}')


def acov(x, kmax):
    x = np.asarray(x, float) - np.mean(x)
    T = len(x)
    return np.array([np.dot(x[k:], x[:T - k]) / T for k in range(kmax + 1)])


def ar1(phi, T, rng, burn=200, eps=None):
    e = rng.standard_normal(T + burn) if eps is None else eps
    x = np.zeros(T + burn)
    for t in range(1, T + burn):
        x[t] = phi * x[t - 1] + e[t]
    return x[burn:]


def kern(x, kind):
    x = np.abs(np.asarray(x, float))
    if kind == 'bartlett':
        return np.where(x <= 1, 1 - x, 0.0)
    if kind == 'truncated':
        return np.where(x <= 1, 1.0, 0.0)
    z = 6 * np.pi * np.where(x == 0, 1.0, x) / 5            # quadratic spectral
    w = 25 / (12 * np.pi ** 2 * np.where(x == 0, 1.0, x) ** 2) * (np.sin(z) / z - np.cos(z))
    return np.where(x == 0, 1.0, w)


# =============================================================================
# 1. AR(1): paths and autocorrelation functions
# =============================================================================
def chart_ar1():
    rng = np.random.default_rng(SEED)
    T = 200
    e = rng.standard_normal(T + 200)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(ar1(0.0, T, rng, eps=e), color=B, lw=0.9, label=r'$\phi = 0$ (white noise)')
    ax[0].plot(ar1(0.8, T, rng, eps=e), color=R, lw=0.9, label=r'$\phi = 0.8$')
    ax[0].axhline(0, color=N, lw=0.6, ls='--')
    ax[0].set_xlabel('$t$')
    ax[0].set_ylabel('$x_t$')
    ax[0].set_title('Two AR(1) paths, same shocks')
    j = np.arange(0, 13)
    for phi, c, m in ((0.8, R, 'o'), (0.5, G, 's'), (-0.6, A, '^')):
        ax[1].plot(j, phi ** j, color=c, marker=m, ms=3.5, lw=1.0, label=rf'$\rho_j = ({phi:g})^j$')
    ax[1].axhline(0, color=N, lw=0.6, ls='--')
    ax[1].set_xlabel('lag $j$')
    ax[1].set_ylabel(r'$\rho_j$')
    ax[1].set_title('Autocorrelation function of AR(1)')
    fig.tight_layout()
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch0_sem_primer_ar1')


# =============================================================================
# 2. Long-run variance ratio and the asymptotic size of the naive test
# =============================================================================
def chart_lrv_ratio():
    phi = np.linspace(-0.9, 0.9, 361)
    ratio = (1 + phi) / (1 - phi)
    size = 2 * (1 - stats.norm.cdf(1.96 / np.sqrt(ratio)))
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].semilogy(phi, ratio, color=B, lw=1.6)
    ax[0].axhline(1, color=R, lw=0.9, ls='--')
    ax[0].text(-0.88, 1.15, r'i.i.d.: $\Omega = \gamma_0$', color=R, fontsize=11, va='bottom')
    ax[0].set_xlabel(r'AR(1) coefficient $\phi$')
    ax[0].set_ylabel(r'$\Omega/\gamma_0$ (log scale)')
    ax[0].set_title(r'$\Omega/\gamma_0 = (1+\phi)/(1-\phi)$')
    ax[1].plot(phi, 100 * size, color=B, lw=1.6)
    ax[1].axhline(5, color=R, lw=0.9, ls='--')
    ax[1].text(-0.88, 6, 'nominal 5%', color=R, fontsize=11, va='bottom')
    ax[1].set_xlabel(r'AR(1) coefficient $\phi$')
    ax[1].set_ylabel('size (%)')
    ax[1].set_title(r'naive test: $2[1-\Phi(1.96\sqrt{\gamma_0/\Omega})]$')
    fig.tight_layout()
    save(fig, 'ch0_sem_primer_lrv_ratio')


# =============================================================================
# 3. The naive t-statistic under AR(1): wider than N(0, 1)
# =============================================================================
def chart_naive_t():
    rng = np.random.default_rng(SEED + 1)
    phi, T, reps = 0.5, 200, 4000
    tt = np.empty(reps)
    for r in range(reps):
        x = ar1(phi, T, rng)
        tt[r] = np.sqrt(T) * x.mean() / x.std()
    grid = np.linspace(-7, 7, 400)
    ratio = (1 + phi) / (1 - phi)
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.hist(tt, bins=60, density=True, color=st.LightBlue, edgecolor='white', lw=0.3,
            label=r'naive $t$, simulated AR(1), $\phi = 0.5$')
    ax.plot(grid, stats.norm.pdf(grid), color=G, lw=1.5, label=r'$N(0, 1)$: what the test assumes')
    ax.plot(grid, stats.norm.pdf(grid, scale=np.sqrt(ratio)), color=R, lw=1.5,
            label=r'$N(0, \Omega/\gamma_0) = N(0, 3)$')
    for s in (-1.96, 1.96):
        ax.axvline(s, color=N, lw=0.8, ls='--')
    ax.text(1.96, 0.36, ' $\\pm 1.96$', color=N, va='top', fontsize=10)
    ax.set_xlabel('value of the $t$-statistic under a true $H_0$')
    ax.set_ylabel('density')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch0_sem_primer_naive_t')


# =============================================================================
# 4. Kernel weights and the estimate of Omega as the number of lags grows
# =============================================================================
def chart_kernels():
    rng = np.random.default_rng(SEED + 2)
    S = 5
    j = np.arange(0, 11)
    jj = np.linspace(0, 10, 400)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(jj, kern(jj / S, 'truncated'), color=A, lw=1.4, label='truncated')
    ax[0].plot(jj, kern(jj / S, 'bartlett'), color=B, lw=1.6, label='Bartlett')
    ax[0].plot(jj, kern(jj / S, 'qs'), color=G, lw=1.2, ls='--', label='QS')
    ax[0].plot(j[1:S], kern(j[1:S] / S, 'bartlett'), 'o', color=B, ms=4, label='_w')
    ax[0].axhline(0, color=N, lw=0.6)
    ax[0].set_xlabel('lag $j$')
    ax[0].set_ylabel('weight $k(j/S)$')
    ax[0].set_title(r'Weights, $S = 5$')
    st.legend_outside_bottom(ax[0], ncol=3)
    phi, T = 0.5, 200
    x = ar1(phi, T, rng)
    g = acov(x, 40)
    Ls = np.arange(0, 41)
    om_b = [g[0] + 2 * np.sum((1 - np.arange(1, L + 1) / (L + 1)) * g[1:L + 1]) for L in Ls]
    om_t = [g[0] + 2 * np.sum(g[1:L + 1]) for L in Ls]
    ax[1].plot(Ls, om_t, color=A, lw=1.4, label='truncated')
    ax[1].plot(Ls, om_b, color=B, lw=1.6, label='Bartlett')
    ax[1].axhline(1 / (1 - phi) ** 2, color=R, lw=1.0, ls='--', label=r'true $\Omega = 4$')
    ax[1].set_ylim(0, 5)
    ax[1].set_xlabel('number of lags $L$')
    ax[1].set_ylabel(r'$\hat\Omega$')
    ax[1].set_title(r'$\hat\Omega$, one AR(1) sample, $\phi = 0.5$')
    fig.tight_layout()
    st.legend_outside_bottom(ax[1], ncol=3)
    save(fig, 'ch0_sem_primer_kernels')


# =============================================================================
# 5. Fixed-b critical values (Bartlett) and Student-t critical values (EWC)
# =============================================================================
def chart_fixed_b():
    rng = np.random.default_rng(SEED + 3)
    n, reps = 200, 10000
    bs = np.array([0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    jl = np.arange(1, n)
    W = np.array([kern(jl / (b * n), 'bartlett') for b in bs])
    x = rng.standard_normal((reps, n))
    xc = x - x.mean(axis=1, keepdims=True)
    f = np.fft.rfft(xc, 2 * n, axis=1)
    g = np.fft.irfft(f * np.conj(f), axis=1)[:, :n] / n
    v = g[:, :1] + 2 * g[:, 1:] @ W.T
    t = np.abs(np.sqrt(n) * x.mean(axis=1))[:, None] / np.sqrt(np.maximum(v, 1e-12))
    cv = np.quantile(t, 0.95, axis=0)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(np.r_[0, bs], np.r_[1.96, cv], color=B, marker='o', ms=3.5, lw=1.5, label='fixed-$b$')
    ax[0].axhline(1.96, color=R, lw=0.9, ls='--', label='1.96 (Normal)')
    ax[0].set_xlabel('$b = S/T$')
    ax[0].set_ylabel('critical value')
    ax[0].set_title('Bartlett kernel, two-sided 5%')
    nu = np.arange(2, 61)
    ax[1].plot(nu, stats.t.ppf(0.975, nu), color=G, marker='o', ms=2.5, lw=1.3, label=r'$t_\nu$, 97.5% quantile')
    ax[1].axhline(1.96, color=R, lw=0.9, ls='--', label='1.96 (Normal)')
    ax[1].set_ylim(1.8, 4.5)
    ax[1].set_xlabel(r'degrees of freedom $\nu$')
    ax[1].set_ylabel('critical value')
    ax[1].set_title('EWC: Student-$t_\\nu$, two-sided 5%')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=2)
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch0_sem_primer_fixed_b')


# =============================================================================
# 6. Block bootstraps: which observations enter one resample
# =============================================================================
def chart_blocks():
    T, l = 12, 3
    cols = [B, R, G, A]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    rows = [('data', [(list(range(1, T + 1)), None)]),
            ('MBB', [([4, 5, 6], 0), ([9, 10, 11], 1), ([1, 2, 3], 2), ([6, 7, 8], 3)]),
            ('CBB', [([7, 8, 9], 0), ([11, 12, 1], 1), ([2, 3, 4], 2), ([5, 6, 7], 3)]),
            ('stationary', [([3, 4], 0), ([10, 11, 12, 1, 2], 1), ([6], 2), ([8, 9, 10, 11], 3)])]
    for r, (lab, blocks) in enumerate(rows):
        y = -r
        ax.text(-0.4, y + 0.4, lab, ha='right', va='center', fontsize=12, color=N)
        pos = 0
        for idx, c in blocks:
            for k, i in enumerate(idx):
                fc = 'none' if c is None else cols[c]
                ax.add_patch(Rectangle((pos, y), 0.92, 0.8, facecolor=fc, alpha=0.35 if c is not None else 1,
                                       edgecolor=N if c is None else cols[c], lw=0.8))
                ax.text(pos + 0.46, y + 0.4, f'$x_{{{i}}}$', ha='center', va='center', fontsize=11, color=N)
                pos += 1
            if c is not None and pos < T:
                ax.plot([pos - 0.04, pos - 0.04], [y - 0.05, y + 0.85], color=N, lw=1.2)
    ax.text(T + 0.2, -1 + 0.4, 'blocks of length $l = 3$', va='center', fontsize=11, color=B)
    ax.text(T + 0.2, -2 + 0.4, 'blocks wrap: $x_{12}, x_1$', va='center', fontsize=11, color=R)
    ax.text(T + 0.2, -3 + 0.4, r'lengths $\sim$ Geometric($p$)', va='center', fontsize=11, color=G)
    ax.set_xlim(-2.6, T + 4.6)
    ax.set_ylim(-3.3, 1.0)
    ax.axis('off')
    save(fig, 'ch0_sem_primer_blocks')


# =============================================================================
# 7. Monte Carlo: the running rejection rate and its Monte Carlo error
# =============================================================================
def chart_mc():
    rng = np.random.default_rng(SEED + 4)
    Rmax = 4000
    rej_ok = rng.random(Rmax) < 0.05
    rej_bad = rng.random(Rmax) < 0.17
    r = np.arange(1, Rmax + 1)
    fig, ax = plt.subplots(figsize=(9, 3.3))
    for rej, p, c, lab in ((rej_ok, 0.05, B, 'valid test (true size 5%)'), (rej_bad, 0.17, R, 'oversized test (true size 17%)')):
        run = np.cumsum(rej) / r
        se = np.sqrt(p * (1 - p) / r)
        ax.fill_between(r, 100 * (p - 1.96 * se), 100 * (p + 1.96 * se), color=c, alpha=0.3, lw=0, label='_b')
        ax.plot(r, 100 * run, color=c, lw=1.2, label=lab)
    ax.axhline(5, color=N, lw=0.7, ls='--', label='nominal 5%')
    ax.set_xscale('log')
    ax.set_xlim(20, Rmax)
    ax.set_ylim(0, 30)
    ax.set_xlabel('number of Monte Carlo replications $R$ (log scale)')
    ax.set_ylabel('rejections (%)')
    ax.set_title(r'Running rejection rate $\hat p_R$ and the band $p \pm 1.96\sqrt{p(1-p)/R}$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=3)
    save(fig, 'ch0_sem_primer_mc')


# =============================================================================
# 8. GARCH(1,1): volatility clustering, ACF of returns and of squared returns
# =============================================================================
def chart_garch():
    rng = np.random.default_rng(SEED + 5)
    om, al, be, T = 0.05, 0.08, 0.90, 3000
    z = rng.standard_normal(T + 500)
    r = np.zeros(T + 500)
    s2 = np.full(T + 500, om / (1 - al - be))
    for t in range(1, T + 500):
        s2[t] = om + al * r[t - 1] ** 2 + be * s2[t - 1]
        r[t] = np.sqrt(s2[t]) * z[t]
    r, s2 = r[500:], s2[500:]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    show = slice(0, 1000)
    ax[0].plot(r[show], color=B, lw=0.5, label='$r_t$')
    ax[0].plot(2 * np.sqrt(s2[show]), color=R, lw=1.0, label=r'$\pm 2\sigma_t$')
    ax[0].plot(-2 * np.sqrt(s2[show]), color=R, lw=1.0, label='_m')
    ax[0].set_xlabel('$t$')
    ax[0].set_ylabel('$r_t$')
    ax[0].set_title(r'$\omega = 0.05$, $\alpha = 0.08$, $\beta = 0.90$')
    st.legend_outside_bottom(ax[0], ncol=2)
    K = 30
    k = np.arange(1, K + 1)
    a1 = acov(r, K)
    a2 = acov(r ** 2, K)
    rho1 = al * (1 - al * be - be ** 2) / (1 - 2 * al * be - be ** 2)
    ax[1].bar(k - 0.2, a1[1:] / a1[0], width=0.4, color=B, label='ACF of $r_t$')
    ax[1].bar(k + 0.2, a2[1:] / a2[0], width=0.4, color=A, label='ACF of $r_t^2$')
    ax[1].plot(k, rho1 * (al + be) ** (k - 1), color=R, lw=1.4, label=r'theory: $\rho_1(\alpha+\beta)^{k-1}$')
    ax[1].axhline(0, color=N, lw=0.6)
    ax[1].set_xlabel('lag $k$')
    ax[1].set_ylabel('autocorrelation')
    ax[1].set_title('ACF of returns and of squares')
    fig.tight_layout()
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch0_sem_primer_garch')


# =============================================================================
# 9. Spurious regression: two independent random walks
# =============================================================================
def chart_spurious():
    rng = np.random.default_rng(SEED + 11)
    T = 200
    y = np.cumsum(rng.standard_normal(T))
    x = np.cumsum(rng.standard_normal(T))
    X = np.c_[np.ones(T), x]
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    s2 = e @ e / (T - 2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(y, color=B, lw=1.0, label='$y_t$')
    ax[0].plot(x, color=R, lw=1.0, label='$x_t$')
    ax[0].set_xlabel('$t$')
    ax[0].set_title('Two independent random walks')
    ax[1].scatter(x, y, s=6, color=B, alpha=0.6, label='_s')
    xx = np.linspace(x.min(), x.max(), 10)
    ax[1].plot(xx, b[0] + b[1] * xx, color=R, lw=1.5, label=rf'OLS line, slope $t = {b[1] / se:.1f}$')
    ax[1].set_xlabel('$x_t$')
    ax[1].set_ylabel('$y_t$')
    ax[1].set_title('Regression of $y_t$ on $x_t$')
    fig.tight_layout()
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch0_sem_primer_spurious')


# =============================================================================
# 10. Multiple testing: FWER and the Holm thresholds
# =============================================================================
def chart_fwer():
    K = np.arange(1, 101)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(K, 100 * (1 - 0.95 ** K), color=R, lw=1.6, label=r'$\alpha = 5\%$')
    ax[0].plot(K, 100 * (1 - 0.99 ** K), color=A, lw=1.6, label=r'$\alpha = 1\%$')
    ax[0].plot(K, 100 * (1 - (1 - 0.05 / K) ** K), color=B, lw=1.6, label=r'Bonferroni, 5%')
    ax[0].set_xlabel('number of true hypotheses $K$')
    st.legend_outside_bottom(ax[0], ncol=3)
    ax[0].set_ylabel('FWER (%)')
    ax[0].set_title(r'FWER $= 1 - (1-\alpha)^K$')
    p = np.array([0.001, 0.005, 0.007, 0.009, 0.03, 0.06, 0.15, 0.4])
    Kh = len(p)
    i = np.arange(1, Kh + 1)
    thr = 0.05 / (Kh - i + 1)
    ax[1].step(i, thr, where='mid', color=B, lw=1.5, label='Holm')
    ax[1].axhline(0.05 / Kh, color=A, lw=1.2, ls='--', label='Bonferroni')
    ok = np.cumprod(p <= thr).astype(bool)
    ax[1].plot(i[ok], p[ok], 'o', color=G, ms=5, label='rejected')
    ax[1].plot(i[~ok], p[~ok], 'o', color=R, ms=5, mfc='none', label='not rejected')
    ax[1].set_yscale('log')
    ax[1].set_xlabel('rank $i$ of the sorted p-value')
    ax[1].set_ylabel('p-value (log scale)')
    ax[1].set_title(r'$K = 8$ illustrative p-values')
    fig.tight_layout()
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch0_sem_primer_fwer')


def main():
    st.apply()
    chart_ar1()
    chart_lrv_ratio()
    chart_naive_t()
    chart_kernels()
    chart_fixed_b()
    chart_blocks()
    chart_mc()
    chart_garch()
    chart_spurious()
    chart_fwer()


if __name__ == '__main__':
    main()
