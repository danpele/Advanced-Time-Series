"""
seminar6_explainers.py -- explanatory (primer) charts of Seminar 6 (ATS): state space models and Bayesian filtering
====================================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 6, which
takes place BEFORE Lecture 6. All charts use SIMULATED data only (fixed seeds): the local level model with its
filtered and smoothed level, the Kalman gain converging to its steady state, the large-kappa initialisation against
the exact diffuse likelihood, state draws by forward filtering and backward sampling, the pile-up of ML variance
estimates at zero, a stochastic volatility path and the autocorrelation of squared returns, the log chi-square
distribution of the linearised SV model, one step of a bootstrap particle filter, the Beveridge-Nelson trend and
cycle, and real-time (filtered) against final (smoothed) output gaps. No exercise answers and no market data.

Output: charts/ch6_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each figure
sized for its box on the slides (ats_style.fit_for_slide), so that its text is at least 6.4 pt there.

Run:  python3 Quantlets/Ch_06/seminar6_explainers.py

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
Purple = st.Purple
BandBlue = '#C5D2E8'

TW, TH = 409.72 / 72, 214.79 / 72          # \textwidth, \textheight of the decks (inches)
HALF = (0.50 * TW, 0.78 * TH)              # chart in the left column (0.50\textwidth), height 0.78\textheight
FULL = (0.96 * TW, 0.60 * TH)              # chart across the slide, height 0.60\textheight


def save(fig, name, box):
    """Size for the slide box, check the house rules, save PDF + PNG in charts/."""
    st.fit_for_slide(fig, name, box=box)
    st.check_no_grey(fig)
    os.makedirs(st.CHART_DIR, exist_ok=True)
    fig.savefig(os.path.join(st.CHART_DIR, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(st.CHART_DIR, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print(f'   saved {name}')


# =============================================================================
# a small Kalman filter and smoother (univariate observation)
# =============================================================================
def kfs(y, Z, Tm, RQR, H, a1, P1):
    """Kalman filter (predicted a_t, P_t; filtered a_t|t, P_t|t) and Rauch-Tung-Striebel smoother."""
    n, m = len(y), len(a1)
    a, P = a1.astype(float).copy(), P1.astype(float).copy()
    ap, Pp, af, Pf = np.zeros((n, m)), np.zeros((n, m, m)), np.zeros((n, m)), np.zeros((n, m, m))
    v, F = np.zeros(n), np.zeros(n)
    for t in range(n):
        ap[t], Pp[t] = a, P
        if np.isfinite(y[t]):
            F[t] = Z @ P @ Z + H
            v[t] = y[t] - Z @ a
            Kf = P @ Z / F[t]
            a_f, P_f = a + Kf * v[t], P - np.outer(Kf, Z @ P)
        else:
            F[t], v[t] = np.nan, np.nan
            a_f, P_f = a, P
        af[t], Pf[t] = a_f, P_f
        a, P = Tm @ a_f, Tm @ P_f @ Tm.T + RQR
    sm, Vs = af.copy(), Pf.copy()
    for t in range(n - 2, -1, -1):
        Pn = Tm @ Pf[t] @ Tm.T + RQR
        G = Pf[t] @ Tm.T @ np.linalg.pinv(Pn)
        sm[t] = af[t] + G @ (sm[t + 1] - Tm @ af[t])
        Vs[t] = Pf[t] + G @ (Vs[t + 1] - Pn) @ G.T
    return dict(ap=ap, Pp=Pp, af=af, Pf=Pf, sm=sm, Vs=Vs, v=v, F=F)


def local_level(n, s2e, s2h, seed, mu0=0.0):
    rng = np.random.default_rng(seed)
    mu = mu0 + np.cumsum(np.r_[0.0, np.sqrt(s2h) * rng.standard_normal(n - 1)])
    return mu + np.sqrt(s2e) * rng.standard_normal(n), mu


# =============================================================================
# (1) local level: data, filtered and smoothed level
# =============================================================================
def fig_local_level(n=100, s2e=1.0, s2h=0.1, seed=3):
    y, mu = local_level(n, s2e, s2h, seed, mu0=5)
    r = kfs(y, np.array([1.0]), np.eye(1), np.eye(1) * s2h, s2e, np.zeros(1), np.eye(1) * 1e7)
    t = np.arange(1, n + 1)
    sd = np.sqrt(r['Vs'][:, 0, 0])
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.fill_between(t, r['sm'][:, 0] - 1.645 * sd, r['sm'][:, 0] + 1.645 * sd, color=BandBlue, alpha=0.8, lw=0,
                    label='90% band of the smoothed level')
    ax.plot(t, y, 'o', color=Amber, ms=2.2, label='observations $y_t$')
    ax.plot(t, mu, color=Navy, lw=1.0, ls=':', label=r'true level $\mu_t$')
    ax.plot(t, r['af'][:, 0], color=IDAred, lw=1.1, label=r'filtered $a_{t|t}$')
    ax.plot(t, r['sm'][:, 0], color=MainBlue, lw=1.5, label=r'smoothed $\hat\alpha_t$')
    ax.set_xlabel('Time $t$')
    ax.set_title(rf'Local level, $q = {s2h / s2e:g}$', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch6_sem_primer_local_level', HALF)


# =============================================================================
# (2) the Kalman gain converges to its steady state
# =============================================================================
def fig_gain(n=15, qs=(0.1, 1.0, 3.0)):
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    cols = {0.1: MainBlue, 1.0: IDAred, 3.0: Forest}
    out = {}
    for q in qs:
        P = 1 + q                                  # after the diffuse step: P_2 = sigma_eps^2 + sigma_eta^2
        k = []
        for _ in range(n):
            kk = P / (P + 1)
            k.append(kk)
            P = P * (1 - kk) + q
        Pbar = (q + np.sqrt(q ** 2 + 4 * q)) / 2
        out[q] = Pbar / (Pbar + 1)
        ax.plot(np.arange(2, n + 2), k, 'o-', color=cols[q], ms=3.5, lw=1.2, label=rf'$q$ = {q}')
        ax.axhline(out[q], color=cols[q], lw=0.8, ls=':')
    ax.set_xlabel('Time $t$')
    ax.set_ylabel(r'Gain $k_t = P_t/F_t$')
    ax.set_ylim(0, 1)
    ax.set_title('Steady state (dotted) after a few steps', loc='left')
    st.legend_outside_bottom(ax, ncol=3)
    save(fig, 'ch6_sem_primer_gain', HALF)
    return out


# =============================================================================
# (3) a large-kappa start against the exact diffuse likelihood
# =============================================================================
def _ll_local_level(y, s2e, s2h, a1, P1):
    a, P, ll = a1, P1, []
    for yt in y:
        F = P + s2e
        v = yt - a
        ll.append(-0.5 * (np.log(2 * np.pi) + np.log(F) + v ** 2 / F))
        k = P / F
        a, P = a + k * v, P * (1 - k) + s2h
    return np.array(ll)


def fig_diffuse(n=80, s2e=1.0, s2h=0.5, seed=9):
    y, _ = local_level(n, s2e, s2h, seed, mu0=3)
    lld = _ll_local_level(y[1:], s2e, s2h, y[0], s2e + s2h).sum()      # exact diffuse: drop the first term
    lk = np.arange(0, 11)
    llk = np.array([_ll_local_level(y, s2e, s2h, 0.0, 10.0 ** k).sum() for k in lk])
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.plot(lk, llk, 'o-', color=IDAred, ms=4, lw=1.2, label=r'$\ln L$ with $P_1 = \kappa$, all $n$ terms')
    ax.plot(lk, llk + 0.5 * np.log(10.0 ** lk), 's--', color=Forest, ms=3.5, lw=1.0,
            label=r'the same $+\frac{1}{2}\ln\kappa$')
    ax.axhline(lld - 0.5 * np.log(2 * np.pi), color=MainBlue, lw=1.2,
               label=r'exact diffuse $\ln L_d - \frac{1}{2}\ln 2\pi$')
    ax.set_xlabel(r'$\log_{10}\kappa$')
    ax.set_ylabel('Log-likelihood')
    ax.set_title(r'$\ln L$ falls like $-\frac{1}{2}\ln\kappa$', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch6_sem_primer_diffuse', HALF)
    return dict(lld=float(lld), ll10=float(llk[-1]))


# =============================================================================
# (4) forward filtering, backward sampling: draws of the state path
# =============================================================================
def fig_ffbs(n=60, s2e=1.0, s2h=0.2, draws=15, seed=12):
    y, mu = local_level(n, s2e, s2h, seed, mu0=2)
    r = kfs(y, np.array([1.0]), np.eye(1), np.eye(1) * s2h, s2e, np.zeros(1), np.eye(1) * 1e7)
    rng = np.random.default_rng(seed + 1)
    af, Pf = r['af'][:, 0], r['Pf'][:, 0, 0]
    paths = np.empty((draws, n))
    for d in range(draws):
        a = af[-1] + np.sqrt(Pf[-1]) * rng.standard_normal()
        paths[d, -1] = a
        for t in range(n - 2, -1, -1):
            G = Pf[t] / (Pf[t] + s2h)
            m, S = af[t] + G * (a - af[t]), Pf[t] * (1 - G)
            a = m + np.sqrt(S) * rng.standard_normal()
            paths[d, t] = a
    t = np.arange(1, n + 1)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    for d in range(draws):
        ax.plot(t, paths[d], color=BandBlue, lw=0.9, label='FFBS draws of the path' if d == 0 else '_')
    ax.plot(t, y, 'o', color=Amber, ms=2.2, label='observations $y_t$')
    ax.plot(t, r['sm'][:, 0], color=MainBlue, lw=1.6, label=r'smoothed mean $\hat\alpha_t$')
    ax.plot(t, paths.mean(0), color=IDAred, lw=1.0, ls='--', label='mean of the draws')
    ax.set_xlabel('Time $t$')
    ax.set_title(f'{draws} draws of $\\alpha_{{1:n}}\\mid y$', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch6_sem_primer_ffbs', HALF)


# =============================================================================
# (5) pile-up: ML estimates of the signal-to-noise ratio at zero
# =============================================================================
def fig_pileup(n=100, q_true=0.005, reps=500, seed=21):
    rng = np.random.default_rng(seed)
    grid = np.r_[0.0, np.exp(np.linspace(np.log(1e-4), np.log(1.0), 160))]
    qhat = np.empty(reps)
    for r in range(reps):
        mu = np.cumsum(np.r_[0.0, np.sqrt(q_true) * rng.standard_normal(n - 1)])
        y = mu + rng.standard_normal(n)
        a = np.full(grid.shape, y[0])
        P = 1 + grid
        sv, slf = np.zeros(grid.shape), np.zeros(grid.shape)
        for t in range(1, n):
            F = P + 1
            v = y[t] - a
            sv += v ** 2 / F
            slf += np.log(F)
            k = P / F
            a, P = a + k * v, P * (1 - k) + grid
        s2 = sv / (n - 1)
        llc = -(n - 1) / 2 * (np.log(2 * np.pi) + 1 + np.log(s2)) - 0.5 * slf
        qhat[r] = grid[np.argmax(llc)]
    share0 = float(np.mean(qhat == 0))
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    bins = np.linspace(0, 0.08, 41)
    ax.hist(qhat[qhat > 0], bins=bins, color=MainBlue, label=r'$\hat q > 0$')
    ax.bar(0, np.sum(qhat == 0), width=0.0016, color=IDAred, label=rf'$\hat q = 0$ exactly: {100 * share0:.0f}%')
    ax.axvline(q_true, color=Forest, lw=1.4, ls='--', label=rf'true $q$ = {q_true}')
    ax.set_xlabel(r'ML estimate $\hat q = \hat\sigma^2_\eta/\hat\sigma^2_\varepsilon$')
    ax.set_ylabel('Number of samples')
    ax.set_title(f'{reps} local-level samples, $n$ = {n}', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch6_sem_primer_pileup', HALF)
    return dict(share0=share0, median=float(np.median(qhat)))


# =============================================================================
# (6) stochastic volatility: a path and the autocorrelation of squared returns
# =============================================================================
def fig_sv(n=2000, phi=0.95, s_eta=0.25, mu=0.0, seed=5, K=40):
    rng = np.random.default_rng(seed)
    s2h = s_eta ** 2 / (1 - phi ** 2)
    h = np.empty(n)
    h[0] = mu + np.sqrt(s2h) * rng.standard_normal()
    for t in range(1, n):
        h[t] = mu + phi * (h[t - 1] - mu) + s_eta * rng.standard_normal()
    y = np.exp(h / 2) * rng.standard_normal(n)
    y2 = y ** 2 - np.mean(y ** 2)
    acf = np.array([np.sum(y2[k:] * y2[:-k]) / np.sum(y2 ** 2) for k in range(1, K + 1)])
    k = np.arange(1, K + 1)
    theo = (np.exp(s2h * phi ** k) - 1) / (3 * np.exp(s2h) - 1)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axes[0]
    t = np.arange(500)
    ax.fill_between(t, -2 * np.exp(h[:500] / 2), 2 * np.exp(h[:500] / 2), color=BandBlue, alpha=0.8, lw=0,
                    label=r'$\pm 2\exp(h_t/2)$')
    ax.plot(t, y[:500], color=MainBlue, lw=0.6, label='$y_t$')
    ax.set_xlabel('Time $t$')
    ax.set_title(rf'SV path: $\phi = {phi}$, $\sigma_\eta = {s_eta}$', loc='left')
    ax = axes[1]
    ax.vlines(k, 0, acf, color=MainBlue, lw=1.8, label=r'sample ACF of $y_t^2$')
    ax.plot(k, theo, color=IDAred, lw=1.3, ls='--', label='theoretical $\\Corr(y_t^2, y_{t-k}^2)$'.replace('\\Corr', '\\mathrm{Corr}'))
    ax.axhline(0, color=Navy, lw=0.6)
    ax.set_xlabel('Lag $k$')
    ax.set_title(f'ACF of squares; kurtosis {3 * np.exp(s2h):.1f}', loc='left')
    st.fig_legend_bottom(fig, ncol=4)
    save(fig, 'ch6_sem_primer_sv', FULL)
    return dict(s2h=float(s2h), kurt=float(3 * np.exp(s2h)), r1=float(theo[0]))


# =============================================================================
# (7) the distribution of ln eps^2 against the Normal with the same mean and variance
# =============================================================================
def fig_logchi2():
    x = np.linspace(-12, 4, 800)
    # density of z = ln e^2, e ~ N(0,1): f(z) = exp(z/2 - exp(z)/2) / sqrt(2 pi)
    f = np.exp(x / 2 - np.exp(x) / 2) / np.sqrt(2 * np.pi)
    m, v = -1.2704, np.pi ** 2 / 2
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.plot(x, f, color=MainBlue, lw=1.6, label=r'density of $\ln\epsilon_t^2$, $\epsilon_t \sim N(0, 1)$')
    ax.plot(x, stats.norm.pdf(x, m, np.sqrt(v)), color=IDAred, lw=1.2, ls='--',
            label=r'Normal, mean $-1.27$, variance $\pi^2/2$')
    ax.axvline(m, color=Navy, lw=0.7, ls=':')
    ax.set_xlabel(r'$\xi_t = \ln\epsilon_t^2$')
    ax.set_ylabel('Density')
    ax.set_title('Long left tail: skewed, not Normal', loc='left')
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch6_sem_primer_logchi2', HALF)


# =============================================================================
# (8) one step of the bootstrap particle filter
# =============================================================================
def fig_particles(N=20, y=2.0, U=0.37, seed=4):
    rng = np.random.default_rng(seed)
    h = np.sort(rng.normal(0.0, 0.9, N))
    w = stats.norm.pdf(y, 0, np.exp(h / 2))
    W = w / w.sum()
    ess = 1 / np.sum(W ** 2)
    u = (U + np.arange(N)) / N
    idx = np.searchsorted(np.cumsum(W), u)
    counts = np.bincount(idx, minlength=N)
    fig, axes = plt.subplots(2, 1, figsize=(4.4, 3.9), sharex=True)
    ax = axes[0]
    ax.vlines(h, 0, W, color=MainBlue, lw=1.8, label=r'normalised weight $W^{(i)}$')
    ax.axhline(1 / N, color=Amber, lw=0.9, ls='--', label=f'equal weight 1/{N}')
    ax.set_title(f'Weights given $y_t$ = {y}; ESS = {ess:.1f} of {N}', loc='left')
    ax = axes[1]
    ax.vlines(h, 0, counts, color=IDAred, lw=1.8, label='copies after systematic resampling')
    ax.set_xlabel(r'Particle $h_t^{(i)}$ (log-variance)')
    ax.set_title(f'{int(np.sum(counts > 0))} distinct particles survive', loc='left')
    st.fig_legend_bottom(fig, ncol=1)
    save(fig, 'ch6_sem_primer_particles', HALF)
    return dict(ess=float(ess), survivors=int(np.sum(counts > 0)))


# =============================================================================
# (9) Beveridge-Nelson trend and cycle of an ARIMA(1,1,0)
# =============================================================================
def fig_bn(n=120, phi=0.5, mu=0.5, seed=8):
    rng = np.random.default_rng(seed)
    g = np.empty(n)
    g[0] = mu
    for t in range(1, n):
        g[t] = mu + phi * (g[t - 1] - mu) + rng.standard_normal()
    y = 100 + np.cumsum(g)
    c = -phi / (1 - phi) * (g - mu)
    tau = y - c
    t = np.arange(n)
    fig, axes = plt.subplots(2, 1, figsize=(4.4, 3.9), sharex=True, gridspec_kw=dict(height_ratios=[1.5, 1]))
    ax = axes[0]
    ax.plot(t, y, color=MainBlue, lw=1.0, label='$y_t$')
    ax.plot(t, tau, color=IDAred, lw=1.0, label=r'BN trend $\tau_t$')
    ax.set_title(rf'Growth AR(1), $\phi = {phi}$', loc='left')
    ax = axes[1]
    ax.plot(t, c, color=Forest, lw=1.0, label=r'BN cycle $c_t = y_t - \tau_t$')
    ax.axhline(0, color=Navy, lw=0.6, ls=':')
    ax.set_xlabel('Time $t$ (quarters)')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch6_sem_primer_bn', HALF)
    return dict(corr=float(np.corrcoef(c[1:], g[1:])[0, 1]))


# =============================================================================
# (10) real-time (filtered) against final (smoothed) gap: smooth trend + AR(2) cycle
# =============================================================================
def fig_realtime_gap(n=120, s_zeta=0.08, phi=(1.4, -0.5), s_c=0.5, seed=31):
    rng = np.random.default_rng(seed)
    slope = 0.6 + np.cumsum(s_zeta * rng.standard_normal(n))
    tau = 100 + np.cumsum(slope)
    c = np.zeros(n)
    for t in range(2, n):
        c[t] = phi[0] * c[t - 1] + phi[1] * c[t - 2] + s_c * rng.standard_normal()
    y = tau + c
    # state (tau_t, nu_t, c_t, c_{t-1}); tau_{t+1} = tau_t + nu_t, nu_{t+1} = nu_t + zeta_t
    Tm = np.array([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, phi[0], phi[1]], [0, 0, 1, 0]], float)
    RQR = np.diag([0.0, s_zeta ** 2, s_c ** 2, 0.0])
    Z = np.array([1.0, 0.0, 1.0, 0.0])
    P1 = np.diag([1e7, 1e7, s_c ** 2 * 5, s_c ** 2 * 5])
    r = kfs(y, Z, Tm, RQR, 1e-8, np.array([y[0], 0.0, 0.0, 0.0]), P1)
    filt, smo = r['af'][:, 2], r['sm'][:, 2]
    k0 = 12
    rev = filt[k0:] - smo[k0:]
    ns = float(np.std(rev) / np.std(smo[k0:]))
    corr = float(np.corrcoef(filt[k0:], smo[k0:])[0, 1])
    opp = float(np.mean(np.sign(filt[k0:]) != np.sign(smo[k0:])))
    t = np.arange(n)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.plot(t[k0:], c[k0:], color=Navy, lw=0.8, ls=':', label='true cycle')
    ax.plot(t[k0:], filt[k0:], color=IDAred, lw=1.3, label=r'real time: filtered $c_{t|t}$')
    ax.plot(t[k0:], smo[k0:], color=MainBlue, lw=1.5, label=r'final: smoothed $\hat c_t$')
    ax.axhline(0, color=Navy, lw=0.6)
    ax.set_xlabel('Time $t$ (quarters)')
    ax.set_ylabel('Gap (%)')
    ax.set_title(f'Correlation {corr:.2f}; noise-to-signal {ns:.2f}; opposite signs {100 * opp:.0f}%', loc='left')
    st.legend_outside_bottom(ax, ncol=3)
    save(fig, 'ch6_sem_primer_realtime_gap', FULL)
    return dict(corr=corr, ns=ns, opp=opp)


def run_all():
    res = {}
    fig_local_level()
    res['gain'] = fig_gain()
    res['diffuse'] = fig_diffuse()
    fig_ffbs()
    res['pileup'] = fig_pileup()
    res['sv'] = fig_sv()
    fig_logchi2()
    res['particles'] = fig_particles()
    res['bn'] = fig_bn()
    res['gap'] = fig_realtime_gap()
    return res


if __name__ == '__main__':
    import pprint
    pprint.pprint(run_all())
