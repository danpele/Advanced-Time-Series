"""
seminar7_explainers.py -- Explanatory (primer) charts for Seminar 7 (ATS): regime-switching models
==================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 7, which takes
place BEFORE Lecture 7. All charts use SIMULATED data only (fixed seeds): they illustrate the concepts (a two-regime
switching model, regime durations, regime forecasts, filtered and smoothed probabilities, the mixture predictive
density, the non-standard distribution of the LR statistic, MS-GARCH variances, the Beta posterior of a transition
probability, spurious long memory from rare switches) and contain no exercise answers.

Output: charts/ch7_sem_primer_*.pdf and .png (course style: transparent, legend below the plot, no grey), each sized
for its box on the seminar slides (text at least 6.4 pt there).

Run:  python3 Quantlets/Ch_07/seminar7_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_style as st                                                       # noqa: E402
from ms_core import acf, em_msr, ergodic, gph, hamilton_filter, kim_smoother, msr_logf, simulate_chain  # noqa: E402

st.apply()
st.SLIDE_MIN_PT = 6.4            # primer charts: every text at least 6.4 pt on the slide
st.SLIDE_BASE_PT = 6.8

TW, TH = 409.72 / 72, 214.79 / 72                      # \textwidth, \textheight of the decks (inches)
HALF_BOX = (0.52 * TW, 0.80 * TH)                     # chart in the left column (0.52\textwidth), height 0.80\textheight
FULL_BOX = (0.96 * TW, 0.58 * TH)                     # chart across the slide, height 0.58\textheight
HALF_FIG = (4.6, 4.3)
FULL_FIG = (10.0, 3.2)
BandBlue = '#C5D2E8'


def save(fig, name, box):
    st.check_no_grey(fig)
    st.fit_for_slide(fig, name, box=box)
    for ext, kw in (('pdf', {}), ('png', {'dpi': 180})):
        fig.savefig(os.path.join(st.CHART_DIR, f'{name}.{ext}'), bbox_inches='tight', transparent=True, **kw)
    plt.close(fig)
    print(f'   saved {name}')


def shade(ax, s, t, regime=1, color=BandBlue, label=None):
    """Shade the periods with s == regime."""
    on = np.r_[0, (s == regime).astype(int), 0]
    starts, ends = np.where(np.diff(on) == 1)[0], np.where(np.diff(on) == -1)[0]
    for k, (a, b) in enumerate(zip(starts, ends)):
        ax.axvspan(t[a] - 0.5, t[b - 1] + 0.5, color=color, lw=0, alpha=0.8, label=label if k == 0 else None)


# =============================================================================
# (i) a two-regime switching model (MSIH(2)): data and regimes
# =============================================================================
def ms_path():
    rng = np.random.default_rng(7)
    P = np.array([[0.95, 0.05], [0.15, 0.85]])
    mu, sd = np.array([0.8, -0.6]), np.array([0.6, 1.4])
    T = 300
    s = simulate_chain(P, T, rng, s0=0)
    y = mu[s] + sd[s] * rng.standard_normal(T)
    t = np.arange(1, T + 1)
    fig, ax = plt.subplots(figsize=FULL_FIG)
    shade(ax, s, t, 1, label='regime 2 (low mean, high variance)')
    ax.plot(t, y, color=st.MainBlue, lw=1.0, label='$y_t$')
    for j, c in ((0, st.Forest), (1, st.IDAred)):
        ax.axhline(mu[j], color=c, ls='--', lw=1.1, label=f'$\\mu_{j + 1} = {mu[j]:g}$')
    ax.set_xlabel('t')
    ax.set_xlim(0, T + 1)
    st.fig_legend_bottom(fig, ncol=4)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_ms_path', FULL_BOX)


# =============================================================================
# (ii) durations of a regime: geometric distribution
# =============================================================================
def durations():
    d = np.arange(1, 31)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    for p, c, off in ((0.9, st.MainBlue, -0.2), (0.75, st.IDAred, 0.2)):
        pr = (1 - p) * p ** (d - 1)
        ax.bar(d + off, pr, width=0.4, color=c, label=f'$p_{{ii}} = {p:g}$: mean $1/(1-p_{{ii}}) = {1 / (1 - p):.0f}$')
        ax.axvline(1 / (1 - p), color=c, ls='--', lw=1.1)
    ax.set_xlabel('duration $D$ of a visit (periods)')
    ax.set_ylabel('$\\Pr(D = d)$')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_durations', HALF_BOX)


# =============================================================================
# (iii) regime forecasts converge to the ergodic probability
# =============================================================================
def forecast():
    P = np.array([[0.95, 0.05], [0.20, 0.80]])
    pi1 = ergodic(P)[0]
    lam = P[0, 0] + P[1, 1] - 1
    h = np.arange(0, 31)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(h, pi1 + lam ** h * (1 - pi1), 'o-', ms=3, color=st.MainBlue, label='start in regime 1: $S_t = 1$')
    ax.plot(h, pi1 - lam ** h * pi1, 's-', ms=3, color=st.IDAred, label='start in regime 2: $S_t = 2$')
    ax.axhline(pi1, color=st.Forest, ls='--', lw=1.2, label=f'ergodic $\\pi_1 = {pi1:.2f}$')
    ax.set_xlabel('horizon $h$')
    ax.set_ylabel('$\\Pr(S_{t+h} = 1 \\mid S_t)$')
    ax.set_ylim(-0.03, 1.03)
    ax.set_title(f'$p_{{11}} = 0.95$, $p_{{22}} = 0.80$, $\\lambda = {lam:.2f}$')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_forecast', HALF_BOX)


# =============================================================================
# (iv) filtered against smoothed probabilities
# =============================================================================
def filter_smooth():
    rng = np.random.default_rng(11)
    P = np.array([[0.95, 0.05], [0.10, 0.90]])
    mu, sd = np.array([1.0, -1.0]), np.array([1.0, 1.0])
    T = 200
    s = simulate_chain(P, T, rng, s0=0)
    y = mu[s] + sd[s] * rng.standard_normal(T)
    X = np.ones((T, 1))
    logf = msr_logf(y, X, mu[:, None], sd ** 2)
    f = hamilton_filter(logf, P)
    sm, _ = kim_smoother(f['filt'], f['pred'], P)
    t = np.arange(1, T + 1)
    fig, ax = plt.subplots(figsize=FULL_FIG)
    shade(ax, s, t, 1, label='true regime 2 (simulated)')
    ax.plot(t, f['filt'][:, 1], color=st.Amber, lw=1.2, label='filtered $\\Pr(S_t = 2 \\mid Y_t)$')
    ax.plot(t, sm[:, 1], color=st.MainBlue, lw=1.6, label='smoothed $\\Pr(S_t = 2 \\mid Y_T)$')
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlim(0, T + 1)
    ax.set_xlabel('t')
    ax.set_ylabel('probability')
    st.fig_legend_bottom(fig, ncol=3)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_filter_smooth', FULL_BOX)


# =============================================================================
# (v) the predictive density is a mixture
# =============================================================================
def mixture():
    x = np.linspace(-6, 5, 600)
    w, m, s = np.array([0.7, 0.3]), np.array([0.8, -1.0]), np.array([0.7, 1.6])
    fig, ax = plt.subplots(figsize=HALF_FIG)
    for j, c in ((0, st.Forest), (1, st.IDAred)):
        ax.plot(x, w[j] * stats.norm.pdf(x, m[j], s[j]), color=c, ls='--', lw=1.3,
                label=f'$\\hat\\xi_{{{j + 1}}}\\,N({m[j]:g}, {s[j]:g}^2)$, $\\hat\\xi_{{{j + 1}}} = {w[j]:g}$')
    mix = sum(w[j] * stats.norm.pdf(x, m[j], s[j]) for j in range(2))
    ax.plot(x, mix, color=st.MainBlue, lw=2.0, label='mixture: the sum of the two')
    ax.set_xlabel('$y_{T+1}$')
    ax.set_ylabel('density')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_mixture', HALF_BOX)


# =============================================================================
# (vi) the LR statistic of K = 1 against K = 2 is not chi-square
# =============================================================================
def lr_null(B=200, T=200):
    rng = np.random.default_rng(2026)
    X = np.ones((T, 1))
    lr = []
    for b in range(B):
        y = rng.standard_normal(T)
        ll1 = float(-0.5 * T * (np.log(2 * np.pi * np.var(y)) + 1))
        best = -np.inf
        for k in range(4):
            try:
                r = em_msr(y, X, 2, rng=np.random.default_rng(1000 * b + k), maxit=400, tol=1e-6)
                best = max(best, r['loglik'])
            except Exception:                      # noqa: BLE001
                pass
        lr.append(max(0.0, 2 * (best - ll1)))
    lr = np.array(lr)
    x = np.linspace(0.01, max(16, np.quantile(lr, 0.995)), 400)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.hist(lr, bins=25, density=True, color=BandBlue, edgecolor=st.MainBlue, lw=0.5,
            label=f'LR simulated under $K = 1$ ({B} samples, $T = {T}$)')
    ax.plot(x, stats.chi2.pdf(x, 3), color=st.IDAred, lw=1.6, label='$\\chi^2_3$ density (wrong reference)')
    q = np.quantile(lr, 0.95)
    ax.axvline(q, color=st.MainBlue, ls='--', lw=1.3, label=f'95% quantile of the simulated LR: {q:.1f}')
    ax.axvline(stats.chi2.ppf(0.95, 3), color=st.IDAred, ls=':', lw=1.5,
               label=f'95% quantile of $\\chi^2_3$: {stats.chi2.ppf(0.95, 3):.1f}')
    ax.set_xlabel('LR')
    ax.set_ylabel('density')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_lr_null', HALF_BOX)
    return q


# =============================================================================
# (vii) MS-GARCH (Haas, Mittnik and Paolella): two GARCH variances in parallel
# =============================================================================
def msgarch():
    rng = np.random.default_rng(5)
    P = np.array([[0.99, 0.01], [0.03, 0.97]])
    om, a, b = np.array([0.02, 0.20]), np.array([0.04, 0.10]), np.array([0.92, 0.85])
    T = 500
    s = simulate_chain(P, T, rng, s0=0)
    h = np.zeros((T, 2))
    h[0] = om / (1 - a - b)
    e = np.zeros(T)
    for t in range(T):
        if t > 0:
            h[t] = om + a * e[t - 1] ** 2 + b * h[t - 1]
        e[t] = np.sqrt(h[t, s[t]]) * rng.standard_normal()
    tt = np.arange(1, T + 1)
    fig, ax = plt.subplots(figsize=FULL_FIG)
    shade(ax, s, tt, 1, label='regime 2 active (simulated)')
    ax.plot(tt, h[:, 0], color=st.Forest, lw=1.1, label='$h_{1,t}$ (calm GARCH)')
    ax.plot(tt, h[:, 1], color=st.IDAred, lw=1.1, label='$h_{2,t}$ (turbulent GARCH)')
    ax.plot(tt, h[np.arange(T), s], color=st.MainBlue, lw=1.8, label='$h_{S_t,t}$: the variance of $\\varepsilon_t$')
    ax.set_xlabel('t')
    ax.set_ylabel('conditional variance')
    ax.set_xlim(0, T + 1)
    st.fig_legend_bottom(fig, ncol=4)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_msgarch', FULL_BOX)


# =============================================================================
# (viii) Bayesian updating of a transition probability: Beta prior and posterior
# =============================================================================
def beta_post():
    a0, b0, n11, n12 = 2, 2, 27, 3
    x = np.linspace(0.001, 0.999, 600)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(x, stats.beta.pdf(x, a0, b0), color=st.Amber, lw=1.6, ls='--', label=f'prior Beta({a0}, {b0})')
    ax.plot(x, stats.beta.pdf(x, a0 + n11, b0 + n12), color=st.MainBlue, lw=2.0,
            label=f'posterior Beta({a0} + {n11}, {b0} + {n12}) after $n_{{11}} = {n11}$, $n_{{12}} = {n12}$')
    ax.axvline((a0 + n11) / (a0 + b0 + n11 + n12), color=st.MainBlue, ls=':', lw=1.3,
               label=f'posterior mean {(a0 + n11) / (a0 + b0 + n11 + n12):.3f}')
    ax.set_xlabel('$p_{11}$')
    ax.set_ylabel('density')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_beta', HALF_BOX)


# =============================================================================
# (ix) rare regime switches look like long memory (Diebold and Inoue 2001)
# =============================================================================
def long_memory():
    rng = np.random.default_rng(3)
    T = 3000
    P = np.array([[0.998, 0.002], [0.002, 0.998]])
    s = simulate_chain(P, T, rng, s0=0)
    y_ms = np.array([-0.5, 0.5])[s] + rng.standard_normal(T)
    y_iid = rng.standard_normal(T)
    lags = np.arange(1, 101)
    a_ms, a_iid = acf(y_ms, 100), acf(y_iid, 100)
    a_ms = np.asarray(a_ms)[-100:]
    a_iid = np.asarray(a_iid)[-100:]
    d_ms, d_iid = gph(y_ms), gph(y_iid)
    d_ms = d_ms['d'] if isinstance(d_ms, dict) else d_ms
    d_iid = d_iid['d'] if isinstance(d_iid, dict) else d_iid
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(lags, a_ms, color=st.IDAred, lw=1.4, label=f'rare switches ($p_{{ii}} = 0.998$): GPH $\\hat d = {d_ms:.2f}$')
    ax.plot(lags, a_iid, color=st.MainBlue, lw=1.0, label=f'i.i.d. noise: GPH $\\hat d = {d_iid:.2f}$')
    band = 1.96 / np.sqrt(T)
    ax.axhline(band, color=st.Forest, ls='--', lw=1.0, label='$\\pm 1.96/\\sqrt{T}$')
    ax.axhline(-band, color=st.Forest, ls='--', lw=1.0)
    ax.set_xlabel('lag $k$')
    ax.set_ylabel('autocorrelation $\\hat\\rho_k$')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch7_sem_primer_long_memory', HALF_BOX)


if __name__ == '__main__':
    os.makedirs(st.CHART_DIR, exist_ok=True)
    ms_path()
    durations()
    forecast()
    filter_smooth()
    mixture()
    msgarch()
    beta_post()
    long_memory()
    lr_null()
