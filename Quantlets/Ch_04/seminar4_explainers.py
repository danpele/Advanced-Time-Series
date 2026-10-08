"""
seminar4_explainers.py -- explanatory (primer) charts of Seminar 4 (ATS): cointegration, VECM, ARDL and panels
==============================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 4, which
takes place BEFORE Lecture 4. All charts use SIMULATED data only (fixed seeds): they illustrate the concepts
(cointegration and the stationary spread, error correction, the common trend of the Granger representation,
the non-standard null distribution of the trace statistic, its small-sample size and the Reinsel-Ahn factor,
ARDL dynamic multipliers, the bounds of the PSS test, the partial sums of a NARDL, the over-rejection of IPS
under a common factor and the CIPS remedy). They contain no exercise answers and no market data.

Output: charts/ch4_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each figure
sized for its box on the slides (ats_style.fit_for_slide), so that its text is at least 6.4 pt there.

Run:  python3 Quantlets/Ch_04/seminar4_explainers.py

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
import ats_style as st   # noqa: E402

st.apply()
st.SLIDE_MIN_PT = 6.4          # this script only: smallest chart text on the slide
st.SLIDE_BASE_PT = 6.8
MainBlue, IDAred, Forest, Amber, Navy = st.MainBlue, st.IDAred, st.Forest, st.Amber, st.DarkText
BandBlue = '#C5D2E8'

TW, TH = 409.72 / 72, 214.79 / 72          # \textwidth, \textheight of the decks (inches)
HALF = (0.50 * TW, 0.78 * TH)              # chart in the left column (0.50\textwidth), height 0.78\textheight
FULL = (0.96 * TW, 0.50 * TH)              # chart across the slide, height 0.50\textheight


def save(fig, name, box):
    """Size for the slide box, check the house rules, save PDF + PNG in charts/."""
    st.fit_for_slide(fig, name, box=box)
    st.check_no_grey(fig)
    os.makedirs(st.CHART_DIR, exist_ok=True)
    fig.savefig(os.path.join(st.CHART_DIR, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(st.CHART_DIR, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print(f'   saved {name}')


def simulate_vecm(T, alpha, beta, seed, burn=50):
    """Bivariate VECM without lags: dy_t = alpha beta' y_{t-1} + eps_t, eps_t ~ N(0, I)."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(alpha, float), np.asarray(beta, float)
    y = np.zeros((T + burn, 2))
    e = rng.standard_normal((T + burn, 2))
    for t in range(1, T + burn):
        y[t] = y[t - 1] + a * (b @ y[t - 1]) + e[t]
    return y[burn:] - y[burn], e[burn:]


# =============================================================================
# (1) cointegration: two I(1) series with a stationary spread, against two independent random walks
# =============================================================================
def fig_cointegration(T=300, seed=4):
    y, _ = simulate_vecm(T, (-0.25, 0.10), (1, -1), seed)
    rng = np.random.default_rng(seed + 10)
    w = np.cumsum(rng.standard_normal((T, 2)), axis=0)
    t = np.arange(T)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axes[0]
    ax.plot(t, y[:, 0], color=MainBlue, lw=1.1, label='$y_{1t}$')
    ax.plot(t, y[:, 1], color=IDAred, lw=1.1, label='$y_{2t}$')
    ax.set_title('Cointegrated pair: both I(1)', loc='left')
    ax.set_xlabel('Time $t$')
    ax = axes[1]
    ax.plot(t, w[:, 0] - w[:, 1], color=Amber, lw=1.0, label='$w_{1t} - w_{2t}$: independent random walks')
    ax.plot(t, y[:, 0] - y[:, 1], color=Forest, lw=1.2, label=r"$\beta'y_t = y_{1t} - y_{2t}$: cointegrated")
    ax.axhline(0, color=Navy, lw=0.6, ls=':')
    ax.set_title('The spread: I(0) only under cointegration', loc='left')
    ax.set_xlabel('Time $t$')
    st.fig_legend_bottom(fig, ncol=2)
    save(fig, 'ch4_sem_primer_cointegration', FULL)
    return dict(sd_spread=float(np.std(y[:, 0] - y[:, 1])), sd_rw=float(np.std(w[:, 0] - w[:, 1])))


# =============================================================================
# (2) error correction: one disequilibrium, no further shocks
# =============================================================================
def fig_adjustment(alpha=(-0.25, 0.10), H=12):
    a = np.array(alpha)
    y = np.zeros((H + 1, 2))
    y[0] = (1.0, 0.0)                        # y1 one unit above its equilibrium with y2
    for t in range(1, H + 1):
        y[t] = y[t - 1] + a * (y[t - 1, 0] - y[t - 1, 1])
    a_perp = np.array([a[1], -a[0]])         # alpha' alpha_perp = 0
    lim = (a_perp @ y[0]) / a_perp.sum()      # common level = C y_0, beta_perp = (1, 1)'
    rho = 1 + a[0] - a[1]
    hl = np.log(0.5) / np.log(rho)
    h = np.arange(H + 1)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.plot(h, y[:, 0], 'o-', color=MainBlue, ms=3.5, lw=1.2, label=rf'$y_{{1t}}$, $\alpha_1 = {a[0]}$')
    ax.plot(h, y[:, 1], 's-', color=IDAred, ms=3.5, lw=1.2, label=rf'$y_{{2t}}$, $\alpha_2 = {a[1]}$')
    ax.plot(h, y[:, 0] - y[:, 1], color=Forest, lw=1.2, ls='--', label=r"spread $\beta'y_t$")
    ax.axhline(lim, color=Amber, lw=1.0, ls=':', label=f'common level {lim:.2f}')
    ax.axvline(hl, color=Navy, lw=0.7, ls=':')
    ax.annotate(f'half-life {hl:.1f}', (hl, 0.62), xytext=(6, 0), textcoords='offset points', color=Navy)
    ax.set_xlabel('Periods after the disequilibrium')
    ax.set_ylabel('Level')
    ax.set_ylim(-0.08, 1.08)
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch4_sem_primer_adjustment', HALF)
    return dict(common=float(lim), rho=float(rho), half_life=float(hl))


# =============================================================================
# (3) Granger representation: the common trend and the transitory parts
# =============================================================================
def fig_common_trend(T=200, seed=7, alpha=(-0.25, 0.10)):
    y, e = simulate_vecm(T, alpha, (1, -1), seed)
    a = np.array(alpha)
    a_perp = np.array([a[1], -a[0]])         # alpha' alpha_perp = 0
    b_perp = np.array([1.0, 1.0])
    C = np.outer(b_perp, a_perp) / (a_perp @ b_perp)
    tau = np.cumsum(e @ C.T, axis=0)
    tau = tau - tau[0] + C @ y[0]
    t = np.arange(T)
    fig, axes = plt.subplots(2, 1, figsize=(4.4, 3.9), sharex=True, gridspec_kw=dict(height_ratios=[1.6, 1]))
    ax = axes[0]
    ax.plot(t, y[:, 0], color=MainBlue, lw=0.9, label='$y_{1t}$')
    ax.plot(t, y[:, 1], color=IDAred, lw=0.9, label='$y_{2t}$')
    ax.plot(t, tau[:, 0], color=Navy, lw=1.5, label=r'common trend $C\sum_{s\leq t}\varepsilon_s$')
    ax.set_title('Levels and the common trend', loc='left')
    ax = axes[1]
    ax.plot(t, y[:, 0] - tau[:, 0], color=MainBlue, lw=0.8)
    ax.plot(t, y[:, 1] - tau[:, 1], color=IDAred, lw=0.8)
    ax.axhline(0, color=Navy, lw=0.6, ls=':')
    ax.set_title('Transitory parts: stationary', loc='left')
    ax.set_xlabel('Time $t$')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch4_sem_primer_common_trend', HALF)
    return dict(C=C.round(4).tolist())


# =============================================================================
# Johansen trace statistic (case 1: no deterministic terms), with k-1 lagged differences
# =============================================================================
def trace_stats(y, k=1):
    """Trace statistics LR_tr(r), r = 0..n-1, of a VAR(k) in levels without deterministic terms."""
    dy = np.diff(y, axis=0)
    T0 = dy.shape[0]
    R0 = dy[k - 1:]
    R1 = y[k - 1:-1]
    if k > 1:
        Z = np.hstack([dy[k - 1 - j:T0 - j] for j in range(1, k)])
        coef0 = np.linalg.lstsq(Z, R0, rcond=None)[0]
        coef1 = np.linalg.lstsq(Z, R1, rcond=None)[0]
        R0 = R0 - Z @ coef0
        R1 = R1 - Z @ coef1
    T = R0.shape[0]
    S00, S01, S11 = R0.T @ R0 / T, R0.T @ R1 / T, R1.T @ R1 / T
    M = np.linalg.solve(S11, S01.T) @ np.linalg.solve(S00, S01)
    lam = np.sort(np.clip(np.real(np.linalg.eigvals(M)), 0, 1 - 1e-12))[::-1]
    return np.array([-T * np.sum(np.log(1 - lam[r:])) for r in range(len(lam))]), T


def fig_trace_null(T=400, reps=3000, seed=11):
    rng = np.random.default_rng(seed)
    out = {}
    for n in (1, 2):
        s = np.empty(reps)
        for i in range(reps):
            y = np.cumsum(rng.standard_normal((T + 1, n)), axis=0)
            s[i] = trace_stats(y)[0][0]
        out[n] = s
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    cols = {1: MainBlue, 2: IDAred}
    df = {1: 1, 2: 4}
    x = np.linspace(0, 30, 600)
    q = {}
    for n in (1, 2):
        kde = stats.gaussian_kde(out[n])
        q[n] = float(np.quantile(out[n], 0.95))
        ax.plot(x, kde(x), color=cols[n], lw=1.5, label=f'$n - r$ = {n}: simulated trace')
        ax.plot(x, stats.chi2.pdf(x, df[n]), color=cols[n], lw=1.0, ls='--',
                label=rf'$\chi^2({df[n]})$, same number of restrictions')
        ax.axvline(q[n], color=cols[n], lw=0.8, ls=':')
        ax.annotate(f'95%: {q[n]:.1f}', (q[n], 0.30 - 0.08 * n), xytext=(4, 0), textcoords='offset points',
                    color=cols[n])
    ax.set_ylim(0, 0.5)
    ax.set_xlim(0, 30)
    ax.set_xlabel(r'$LR_{tr}$ under $H(r)$ (case 1, $T$ = 400)')
    ax.set_ylabel('Density')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch4_sem_primer_trace_null', HALF)
    return dict(q1=q[1], q2=q[2], chi1=float(stats.chi2.ppf(0.95, 1)), chi4=float(stats.chi2.ppf(0.95, 4)))


# =============================================================================
# (4) small samples: trace statistic with n = 3, VAR(4), T = 50, and the Reinsel-Ahn factor
# =============================================================================
def fig_small_sample(n=3, k=4, T_small=50, reps=3000, seed=12, T_big=500):
    rng = np.random.default_rng(seed)
    small, big = np.empty(reps), np.empty(reps)
    for i in range(reps):
        y = np.cumsum(rng.standard_normal((T_small + k, n)), axis=0)
        s, Teff = trace_stats(y, k)
        small[i] = s[0]
        y = np.cumsum(rng.standard_normal((T_big + 1, n)), axis=0)
        big[i] = trace_stats(y, 1)[0][0]
    factor = (Teff - n * k) / Teff
    cv = float(np.quantile(big, 0.95))
    rej_raw = float(np.mean(small > cv))
    rej_ra = float(np.mean(factor * small > cv))
    x = np.linspace(0, 80, 800)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.plot(x, stats.gaussian_kde(big)(x), color=Navy, lw=1.5, label='asymptotic (large $T$)')
    ax.plot(x, stats.gaussian_kde(small)(x), color=IDAred, lw=1.5,
            label=f'$T$ = {Teff}, VAR({k}): rejects {100 * rej_raw:.0f}%')
    ax.plot(x, stats.gaussian_kde(factor * small)(x), color=Forest, lw=1.5,
            label=f'Reinsel–Ahn, factor {factor:.2f}: rejects {100 * rej_ra:.0f}%')
    ax.axvline(cv, color=Navy, lw=0.8, ls=':')
    ax.annotate(f'95% quantile {cv:.1f}', (cv, 0.045), xytext=(4, 0), textcoords='offset points', color=Navy)
    ax.set_xlim(0, 80)
    ax.set_xlabel(r'$LR_{tr}(0)$ for $n$ = 3 random walks')
    ax.set_ylabel('Density')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch4_sem_primer_small_sample', HALF)
    return dict(cv=cv, rej_raw=rej_raw, rej_ra=rej_ra, factor=float(factor), Teff=int(Teff))


# =============================================================================
# (5) ARDL dynamic multipliers
# =============================================================================
def fig_ardl_multipliers(phi=0.6, b0=0.25, b1=0.15, H=12):
    theta = (b0 + b1) / (1 - phi)
    m = np.empty(H + 1)
    m[0] = b0
    for h in range(1, H + 1):
        m[h] = phi * m[h - 1] + b0 + b1
    hl = np.log(0.5) / np.log(phi)
    h = np.arange(H + 1)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.bar(h, m, color=MainBlue, width=0.6, label='cumulative multiplier $m_h$')
    ax.axhline(theta, color=IDAred, lw=1.3, ls='--', label=rf'long run $\theta$ = {theta:.2f}')
    ax.set_xlabel('Periods $h$ after a permanent unit rise of $x$')
    ax.set_ylabel('Effect on $y$')
    ax.set_ylim(0, 1.15 * theta)
    ax.set_title(rf'$y_t = {phi}y_{{t-1}} + {b0}x_t + {b1}x_{{t-1}} + u_t$; half-life {hl:.1f}', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch4_sem_primer_ardl_multipliers', HALF)
    return dict(theta=float(theta), m=m.round(3).tolist(), half_life=float(hl))


# =============================================================================
# (6) the bounds test: null distribution of F when x is I(0) or I(1) (case III, k = 1)
# =============================================================================
def _bounds_F(y, x):
    dy, dx = np.diff(y), np.diff(x)
    Y = dy
    X = np.column_stack([np.ones_like(Y), y[:-1], x[:-1], dx])
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    e = Y - X @ b
    s2 = e @ e / (len(Y) - X.shape[1])
    V = s2 * np.linalg.inv(X.T @ X)
    R = np.zeros((2, 4)); R[0, 1] = R[1, 2] = 1
    rb = R @ b
    return float(rb @ np.linalg.solve(R @ V @ R.T, rb) / 2)


def fig_bounds(T=500, reps=4000, seed=13):
    rng = np.random.default_rng(seed)
    F0, F1 = np.empty(reps), np.empty(reps)
    for i in range(reps):
        y = np.cumsum(rng.standard_normal(T + 1))
        x0 = rng.standard_normal(T + 1)
        x1 = np.cumsum(rng.standard_normal(T + 1))
        F0[i] = _bounds_F(y, x0)
        F1[i] = _bounds_F(y, x1)
    lo, hi = float(np.quantile(F0, 0.95)), float(np.quantile(F1, 0.95))
    x = np.linspace(0, 12, 600)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.plot(x, stats.gaussian_kde(F0)(x), color=MainBlue, lw=1.5, label='null density, $x$ I(0)')
    ax.plot(x, stats.gaussian_kde(F1)(x), color=IDAred, lw=1.5, label='null density, $x$ I(1)')
    top = 0.75
    ax.axvspan(0, lo, color=Forest, alpha=0.12, lw=0)
    ax.axvspan(lo, hi, color=Amber, alpha=0.22, lw=0)
    ax.axvspan(hi, 12, color=IDAred, alpha=0.10, lw=0)
    ax.axvline(lo, color=MainBlue, lw=0.9, ls='--')
    ax.axvline(hi, color=IDAred, lw=0.9, ls='--')
    ax.text(lo / 2, top * 0.93, 'no level\nrelation', ha='center', va='top', color=Forest)
    ax.text((lo + hi) / 2, top * 0.93, 'incon-\nclusive', ha='center', va='top', color=Navy)
    ax.text((hi + 12) / 2, top * 0.93, 'level\nrelation', ha='center', va='top', color=IDAred)
    ax.annotate(f'lower bound {lo:.2f}', (lo, 0.40), xytext=(-8, 0), textcoords='offset points', ha='right',
                color=MainBlue)
    ax.annotate(f'upper bound {hi:.2f}', (hi, 0.30), xytext=(5, 0), textcoords='offset points', color=IDAred)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, top)
    ax.set_xlabel(rf'Bounds $F$ (case III, $k$ = 1, $T$ = {T})')
    ax.set_ylabel('Density')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch4_sem_primer_bounds', HALF)
    return dict(lower=lo, upper=hi)


# =============================================================================
# (7) NARDL: partial sums of increases and decreases
# =============================================================================
def fig_nardl(T=120, seed=21):
    rng = np.random.default_rng(seed)
    dx = 0.4 * rng.standard_normal(T) + 0.03
    x = np.r_[0.0, np.cumsum(dx)]
    xp = np.r_[0.0, np.cumsum(np.maximum(dx, 0))]
    xm = np.r_[0.0, np.cumsum(np.minimum(dx, 0))]
    t = np.arange(T + 1)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.plot(t, xp, color=IDAred, lw=1.4, label=r'$x_t^+$: cumulated increases')
    ax.plot(t, xm, color=MainBlue, lw=1.4, label=r'$x_t^-$: cumulated decreases')
    ax.plot(t, x, color=Navy, lw=1.1, label=r'$x_t - x_0 = x_t^+ + x_t^-$')
    ax.axhline(0, color=Navy, lw=0.6, ls=':')
    ax.set_xlabel('Time $t$ (months)')
    ax.set_ylabel('Cumulated change')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch4_sem_primer_nardl', HALF)
    return dict(xp=float(xp[-1]), xm=float(xm[-1]), x=float(x[-1]))


# =============================================================================
# (8) panel unit roots under a common factor: IPS against CIPS
# =============================================================================
def _adf_t(dy, X):
    b, *_ = np.linalg.lstsq(X, dy, rcond=None)
    e = dy - X @ b
    s2 = e @ e / (len(dy) - X.shape[1])
    V = s2 * np.linalg.inv(X.T @ X)
    return b[1] / np.sqrt(V[1, 1])


def _tbars(Y):
    """IPS t-bar (ADF without lags, constant) and CIPS (CADF with the cross-section averages) of a T x N panel."""
    T, N = Y.shape
    dY = np.diff(Y, axis=0)
    ybar = Y.mean(1)
    dybar = np.diff(ybar)
    ti, ci = np.empty(N), np.empty(N)
    one = np.ones(T - 1)
    for i in range(N):
        ti[i] = _adf_t(dY[:, i], np.column_stack([one, Y[:-1, i]]))
        ci[i] = _adf_t(dY[:, i], np.column_stack([one, Y[:-1, i], ybar[:-1], dybar]))
    return ti.mean(), ci.mean()


def fig_panel_ips(N=20, T=30, reps=1500, seed=31):
    rng = np.random.default_rng(seed)
    res = {k: np.empty((reps, 2)) for k in ('indep', 'factor')}
    for r in range(reps):
        e = rng.standard_normal((T, N))
        res['indep'][r] = _tbars(np.cumsum(e, axis=0))
        f = rng.standard_normal(T)
        lam = rng.uniform(0.5, 1.5, N)
        res['factor'][r] = _tbars(np.cumsum(e + np.outer(f, lam), axis=0))
    out = {}
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
    for j, (ax, name) in enumerate(zip(axes, ('IPS $\\bar t$', 'CIPS'))):
        cv = np.quantile(res['indep'][:, j], 0.05)
        rej = float(np.mean(res['factor'][:, j] < cv))
        out[name] = dict(cv=float(cv), rej_factor=rej)
        lo = min(res['indep'][:, j].min(), res['factor'][:, j].min())
        hi = max(res['indep'][:, j].max(), res['factor'][:, j].max())
        x = np.linspace(lo, hi, 500)
        ax.plot(x, stats.gaussian_kde(res['indep'][:, j])(x), color=MainBlue, lw=1.5,
                label='independent random walks')
        ax.plot(x, stats.gaussian_kde(res['factor'][:, j])(x), color=IDAred, lw=1.5,
                label='random walks with a common factor')
        ax.axvline(cv, color=Navy, lw=0.9, ls='--', label='5% critical value (independent units)')
        ax.set_title(f'{name}: rejects {100 * rej:.0f}% under the factor', loc='left')
        ax.set_xlabel('Statistic under $H_0$ (all units have a unit root)')
    axes[0].set_ylabel('Density')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch4_sem_primer_panel_ips', FULL)
    return out


def run_all():
    res = {}
    res['cointegration'] = fig_cointegration()
    res['adjustment'] = fig_adjustment()
    res['common_trend'] = fig_common_trend()
    res['trace_null'] = fig_trace_null()
    res['small_sample'] = fig_small_sample()
    res['ardl'] = fig_ardl_multipliers()
    res['bounds'] = fig_bounds()
    res['nardl'] = fig_nardl()
    res['panel'] = fig_panel_ips()
    return res


if __name__ == '__main__':
    import pprint
    pprint.pprint(run_all())
