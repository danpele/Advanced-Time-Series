"""
seminar5_explainers.py -- explanatory (primer) charts of Seminar 5 (ATS): Bayesian VARs, factor models, nowcasting
==================================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 5, which
takes place BEFORE Lecture 5. All charts use SIMULATED data only (fixed seeds): conjugate Normal updating and
empirical Bayes, a Gibbs sampler, MCMC diagnostics (trace plots, R-hat, autocorrelation and ESS), the Minnesota
prior standard deviations, shrinkage paths and the marginal likelihood of the tightness, principal components and
the Bai-Ng criterion, mixed-frequency weights, the ragged edge of a nowcasting panel and a news decomposition.
They contain no exercise answers and no market data.

Output: charts/ch5_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each figure
sized for its box on the slides (ats_style.fit_for_slide), so that its text is at least 6.4 pt there.

Run:  python3 Quantlets/Ch_05/seminar5_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
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
# (1) conjugate Normal updating and empirical Bayes
# =============================================================================
def fig_conjugate(m0=0.5, s0=0.3, bhat=0.9, s=0.15):
    v1 = 1 / (1 / s0 ** 2 + 1 / s ** 2)
    m1 = v1 * (m0 / s0 ** 2 + bhat / s ** 2)
    x = np.linspace(-0.4, 1.6, 600)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axes[0]
    ax.plot(x, stats.norm.pdf(x, m0, s0), color=Amber, lw=1.5, label=rf'prior $N({m0}, {s0}^2)$')
    ax.plot(x, stats.norm.pdf(x, bhat, s), color=MainBlue, lw=1.5, ls='--',
            label=rf'likelihood: $\hat\beta = {bhat}$, $s = {s}$')
    ax.plot(x, stats.norm.pdf(x, m1, np.sqrt(v1)), color=IDAred, lw=1.8,
            label=rf'posterior $N({m1:.2f}, {np.sqrt(v1):.3f}^2)$')
    ax.set_xlabel(r'$\beta$')
    ax.set_ylabel('Density')
    ax.set_title(f'Prior weight {v1 / s0 ** 2:.2f}', loc='left')
    ax = axes[1]
    tau2 = np.linspace(0.01, 3, 400)
    ll = stats.norm.logpdf(bhat, 0, np.sqrt(tau2 + s ** 2))
    t_hat = max(0, bhat ** 2 - s ** 2)
    ax.plot(tau2, ll, color=Forest, lw=1.6, label=r'$\ln p(\hat\beta\mid\tau^2)$, $\hat\beta \sim N(0, \tau^2 + s^2)$')
    ax.axvline(t_hat, color=IDAred, lw=1.0, ls='--', label=rf'maximum $\hat\tau^2 = \hat\beta^2 - s^2$ = {t_hat:.2f}')
    ax.set_xlabel(r'Prior variance $\tau^2$')
    ax.set_ylabel('Log marginal likelihood')
    ax.set_title('Empirical Bayes', loc='left')
    ax.set_ylim(ll.max() - 1.6, ll.max() + 0.2)
    st.fig_legend_bottom(fig, ncol=2)
    save(fig, 'ch5_sem_primer_conjugate', FULL)
    return dict(m1=float(m1), sd1=float(np.sqrt(v1)), w0=float(v1 / s0 ** 2), tau2=float(t_hat))


# =============================================================================
# (2) a Gibbs sampler on a correlated bivariate Normal
# =============================================================================
def fig_gibbs(rho=0.9, M=400, seed=5):
    rng = np.random.default_rng(seed)
    th = np.empty((M + 1, 2))
    th[0] = (-2.5, 2.5)
    path = [th[0].copy()]
    sd = np.sqrt(1 - rho ** 2)
    for m in range(1, M + 1):
        a = rho * th[m - 1, 1] + sd * rng.standard_normal()
        path.append((a, th[m - 1, 1]))
        b = rho * a + sd * rng.standard_normal()
        th[m] = (a, b)
        path.append((a, b))
    path = np.array(path)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), gridspec_kw=dict(width_ratios=[1, 1.6]))
    ax = axes[0]
    g = np.linspace(-3.2, 3.2, 200)
    X, Y = np.meshgrid(g, g)
    Z = np.exp(-(X ** 2 - 2 * rho * X * Y + Y ** 2) / (2 * (1 - rho ** 2)))
    ax.contour(X, Y, Z, levels=[0.05, 0.3, 0.7], colors=[BandBlue, MainBlue, Navy], linewidths=0.8)
    ax.plot(path[:40, 0], path[:40, 1], color=IDAred, lw=0.9, marker='o', ms=2.2, label='first 20 Gibbs sweeps')
    ax.plot(*th[0], 's', color=Forest, ms=5, label='start')
    ax.set_xlabel(r'$\theta_1$')
    ax.set_ylabel(r'$\theta_2$')
    ax.set_title(f'Target: correlation {rho}', loc='left')
    ax = axes[1]
    ax.plot(np.arange(M + 1), th[:, 0], color=MainBlue, lw=0.8, label=r'draws of $\theta_1$')
    ax.axhline(0, color=Navy, lw=0.6, ls=':')
    ax.set_xlabel('Iteration $m$')
    ax.set_ylabel(r'$\theta_1^{(m)}$')
    ax.set_title('Trace plot', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch5_sem_primer_gibbs', FULL)
    return dict(acf1=float(np.corrcoef(th[1:-1, 0], th[2:, 0])[0, 1]))


# =============================================================================
# (3) MCMC diagnostics: four chains (one stuck) and the autocorrelation of an AR(1) chain
# =============================================================================
def _ar1_chain(n, rho, mu, rng, sd=0.1):
    x = np.empty(n)
    x[0] = mu
    e = rng.standard_normal(n) * sd * np.sqrt(1 - rho ** 2)
    for t in range(1, n):
        x[t] = mu + rho * (x[t - 1] - mu) + e[t]
    return x


def _rhat(ch):
    n = ch.shape[1]
    W = ch.var(axis=1, ddof=1).mean()
    B = n * ch.mean(axis=1).var(ddof=1)
    return float(np.sqrt(((n - 1) / n * W + B / n) / W))


def fig_mcmc_diag(n=500, rho=0.8, seed=8, K=25):
    rng = np.random.default_rng(seed)
    mus = (0.20, 0.20, 0.20, 0.42)
    ch = np.array([_ar1_chain(n, rho, m, rng) for m in mus])
    r_all, r3 = _rhat(ch), _rhat(ch[:3])
    long = _ar1_chain(20000, rho, 0, rng)
    xc = long - long.mean()
    acf = np.array([np.sum(xc[k:] * xc[:-k]) / np.sum(xc ** 2) for k in range(1, K + 1)])
    ess = 20000 * (1 - rho) / (1 + rho)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axes[0]
    cols = [MainBlue, Forest, Amber, IDAred]
    for c, x in enumerate(ch):
        ax.plot(x, color=cols[c], lw=0.6, label=f'chain {c + 1}' if c < 3 else 'chain 4: stuck elsewhere')
    ax.set_xlabel('Iteration')
    ax.set_ylabel(r'$\theta^{(m)}$')
    ax.set_title(rf'$\widehat R$ = {r_all:.2f}; without chain 4: {r3:.2f}', loc='left')
    ax = axes[1]
    k = np.arange(1, K + 1)
    ax.vlines(k, 0, acf, color=MainBlue, lw=2.0, label=r'sample $\hat\rho_k$ of the draws')
    ax.plot(k, rho ** k, color=IDAred, lw=1.2, ls='--', label=rf'AR(1): $\rho^k$, $\rho$ = {rho}')
    ax.set_xlabel('Lag $k$')
    ax.set_ylabel('Autocorrelation')
    ax.set_title(f'ESS {ess:,.0f} of 20,000 draws', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch5_sem_primer_mcmc_diag', FULL)
    return dict(rhat=r_all, rhat3=r3, ess=float(ess))


# =============================================================================
# (4) the Minnesota prior standard deviations by lag
# =============================================================================
def fig_minnesota(lams=(0.1, 0.2, 0.5), sig_i=1.0, sig_j=2.0, L=6):
    l = np.arange(1, L + 1)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    cols = {0.1: MainBlue, 0.2: IDAred, 0.5: Forest}
    for lam in lams:
        ax.plot(l, lam / l, 'o-', color=cols[lam], lw=1.3, ms=4, label=rf'own lags, $\lambda$ = {lam}')
        ax.plot(l, lam * sig_i / (l * sig_j), 's--', color=cols[lam], lw=1.0, ms=3.5,
                label=rf'other variable, $\lambda$ = {lam}')
    ax.set_xlabel('Lag $l$')
    ax.set_ylabel('Prior standard deviation')
    ax.set_title(rf'$\sigma_i = {sig_i:.0f}$, $\sigma_j = {sig_j:.0f}$: decay like $1/l$', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch5_sem_primer_minnesota', HALF)


# =============================================================================
# (5) shrinkage path and the marginal likelihood of the tightness (univariate AR(4), random-walk prior)
# =============================================================================
def fig_shrinkage(T=60, p=4, seed=17):
    rng = np.random.default_rng(seed)
    y = np.zeros(T + p + 100)
    for t in range(2, len(y)):
        y[t] = 0.75 * y[t - 1] + 0.15 * y[t - 2] + rng.standard_normal()
    y = y[100:]
    Y = y[p:]
    X = np.column_stack([y[p - l:-l] for l in range(1, p + 1)])
    sig2 = 1.0
    b0 = np.r_[1.0, np.zeros(p - 1)]
    lams = np.exp(np.linspace(np.log(0.01), np.log(10), 200))
    paths, lml = [], []
    for lam in lams:
        O = np.diag((lam / np.arange(1, p + 1)) ** 2)
        P = np.linalg.inv(X.T @ X / sig2 + np.linalg.inv(O))
        paths.append(P @ (X.T @ Y / sig2 + np.linalg.solve(O, b0)))
        S = sig2 * np.eye(len(Y)) + X @ O @ X.T
        lml.append(stats.multivariate_normal.logpdf(Y, X @ b0, S))
    paths, lml = np.array(paths), np.array(lml)
    ols = np.linalg.lstsq(X, Y, rcond=None)[0]
    lam_hat = lams[np.argmax(lml)]
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axes[0]
    cols = [MainBlue, IDAred, Forest, Amber]
    for j in range(p):
        ax.plot(lams, paths[:, j], color=cols[j], lw=1.4, label=f'lag {j + 1}')
        ax.plot(lams[-1] * 1.15, ols[j], '<', color=cols[j], ms=5)
    ax.axvline(lam_hat, color=Navy, lw=0.8, ls=':')
    ax.set_xscale('log')
    ax.set_xlabel(r'Tightness $\lambda$ (log scale)')
    ax.set_ylabel('Posterior mean')
    ax.set_title('Random walk to OLS (triangles)', loc='left')
    ax = axes[1]
    ax.plot(lams, lml, color=Forest, lw=1.6)
    ax.axvline(lam_hat, color=Navy, lw=0.8, ls=':', label=rf'mode $\hat\lambda$ = {lam_hat:.2f}')
    ax.set_xscale('log')
    ax.set_xlabel(r'Tightness $\lambda$ (log scale)')
    ax.set_ylabel(r'$\ln p(y\mid\lambda)$')
    ax.set_title('Marginal likelihood', loc='left')
    ax.set_ylim(lml.max() - 12, lml.max() + 1.5)
    st.fig_legend_bottom(fig, ncol=5)
    save(fig, 'ch5_sem_primer_shrinkage', FULL)
    return dict(lam_hat=float(lam_hat), ols=ols.round(3).tolist())


# =============================================================================
# (6) principal components and the Bai-Ng criterion
# =============================================================================
def fig_factors(N=60, T=150, r=2, seed=23, kmax=8):
    rng = np.random.default_rng(seed)
    F = rng.standard_normal((T, r))
    Lam = rng.standard_normal((N, r)) * np.array([1.0, 0.7])
    Xr = F @ Lam.T + rng.standard_normal((T, N)) * 1.0
    X = (Xr - Xr.mean(0)) / Xr.std(0)
    ev = np.sort(np.linalg.eigvalsh(X.T @ X / T))[::-1]
    share = ev / ev.sum()
    V = np.r_[1.0, 1 - np.cumsum(share)][:kmax + 1]
    k = np.arange(kmax + 1)
    pen = (N + T) / (N * T) * np.log(min(N, T))
    ic = np.log(V) + k * pen
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axes[0]
    ax.bar(np.arange(1, 13), 100 * share[:12], color=[IDAred] * r + [MainBlue] * (12 - r), width=0.6)
    ax.set_xlabel('Component')
    ax.set_ylabel('Share of variance (%)')
    ax.set_title(f'Scree plot ({r} true factors)', loc='left')
    ax.set_xticks(range(1, 13))
    ax = axes[1]
    ax.plot(k, np.log(V), 'o-', color=MainBlue, lw=1.3, ms=4, label=r'$\ln V(k)$: always falls')
    ax.plot(k, ic, 's-', color=IDAred, lw=1.3, ms=4, label=r'$IC_{p2}(k)$ = $\ln V(k)$ + penalty')
    kh = int(np.argmin(ic))
    ax.plot(kh, ic[kh], 'o', color=Forest, ms=9, mfc='none', mew=1.5, label=f'minimum: $k$ = {kh}')
    ax.set_xlabel('Number of factors $k$')
    ax.set_title(f'Penalty per factor {pen:.3f}', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch5_sem_primer_factors', FULL)
    return dict(share=share[:4].round(3).tolist(), k=kh)


# =============================================================================
# (7) mixed frequencies: Mariano-Murasawa weights and exponential Almon shapes
# =============================================================================
def almon(theta, K):
    j = np.arange(K)                          # j = 0: the latest month (as in generate_all_charts.almon)
    w = np.exp(theta[0] * j + theta[1] * j ** 2)
    return w / w.sum()


def fig_mixed_freq(K=12):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axes[0]
    w = np.array([1, 2, 3, 2, 1]) / 3
    ax.bar(np.arange(5), w, color=MainBlue, width=0.55)
    for j, v in enumerate(w):
        ax.text(j, v + 0.03, f'{int(round(3 * v))}/3', ha='center', color=Navy)
    ax.set_xticks(range(5))
    ax.set_xticklabels([r'$y_t$', r'$y_{t-1}$', r'$y_{t-2}$', r'$y_{t-3}$', r'$y_{t-4}$'])
    ax.set_ylim(0, 1.2)
    ax.set_ylabel('Weight in $y_t^Q$')
    ax.set_title('Mariano–Murasawa weights', loc='left')
    ax = axes[1]
    j = np.arange(K)
    for th, c in (((0.0, 0.0), Navy), ((-0.3, 0.0), IDAred), ((0.4, -0.06), Forest)):
        ax.plot(j, almon(th, K), 'o-', color=c, lw=1.3, ms=3.5, label=rf'$\theta$ = ({th[0]}, {th[1]})')
    ax.set_xlabel('Months back $j$')
    ax.set_ylabel('$w_j(\\theta)$')
    ax.set_title(f'Exponential Almon, $K$ = {K}', loc='left')
    ax.set_xticks([0, 3, 6, 9, 11])
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch5_sem_primer_mixed_freq', FULL)


# =============================================================================
# (8) the ragged edge of a nowcasting panel
# =============================================================================
def fig_ragged_edge():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    series = [('GDP (quarterly)', 'Q'), ('industrial production', 2), ('retail sales', 2), ('unemployment', 1),
              ('economic sentiment', 0), ('consumer confidence', 0)]
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    now = 4                                   # end of May: index of the last month of the information set
    for r, (nm, lag) in enumerate(series):
        yy = len(series) - 1 - r
        for m in range(len(months)):
            ok = m <= 2 if lag == 'Q' else m <= now - lag     # Q1 GDP is published two months after March
            ax.add_patch(plt.Rectangle((m, yy + 0.1), 0.92, 0.8, color=MainBlue if ok else BandBlue, lw=0))
        ax.text(-0.15, yy + 0.5, nm, ha='right', va='center')
    ax.axvline(now + 0.96, color=IDAred, lw=1.4, ls='--')
    ax.text(now + 0.9, len(series) + 0.15, 'nowcast date', color=IDAred, ha='right')
    ax.set_xlim(0, len(months))
    ax.set_ylim(0, len(series) + 0.8)
    ax.set_xticks(np.arange(len(months)) + 0.46)
    ax.set_xticklabels(months)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_title('Data available at the end of May', loc='left')
    st.legend_outside_bottom(ax, ncol=2, handles=[Patch(color=MainBlue), Patch(color=BandBlue)],
                             labels=['published', 'not yet published'])
    save(fig, 'ch5_sem_primer_ragged_edge', HALF)


# =============================================================================
# (9) news decomposition of a nowcast revision (illustrative numbers)
# =============================================================================
def fig_news():
    old = 1.20
    rel = [('industrial production', 2.0, 1.1, 0.10), ('retail sales', 1.0, 1.4, 0.06),
           ('sentiment', 98.0, 101.0, 0.02), ('unemployment', 5.4, 5.8, -0.20)]
    imp = [w * (x - e) for _, e, x, w in rel]
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    level = old
    xs = np.arange(len(rel) + 2)
    ax.bar(0, old, color=Navy, width=0.6, label='nowcast')
    for i, ((nm, e, x, w), d) in enumerate(zip(rel, imp), start=1):
        ax.bar(i, d, bottom=level, color=Forest if d > 0 else IDAred, width=0.6)
        ax.text(i, level + d + (0.02 if d >= 0 else -0.02), f'{d:+.2f}', ha='center',
                va='bottom' if d >= 0 else 'top', color=Navy)
        level += d
    ax.bar(len(rel) + 1, level, color=Navy, width=0.6)
    ax.text(0, old + 0.02, f'{old:.2f}', ha='center', va='bottom', color=Navy)
    ax.text(len(rel) + 1, level + 0.02, f'{level:.2f}', ha='center', va='bottom', color=Navy)
    ax.set_xticks(xs)
    ax.set_xticklabels(['old', 'IP', 'retail', 'sentiment', 'unemployment', 'new'], rotation=30, ha='right')
    ax.set_ylabel('GDP growth nowcast (%)')
    ax.set_ylim(0, 1.6)
    st.legend_outside_bottom(ax, ncol=3, handles=[Patch(color=Navy), Patch(color=Forest), Patch(color=IDAred)],
                             labels=['nowcast', 'positive news', 'negative news'])
    save(fig, 'ch5_sem_primer_news', HALF)
    return dict(impacts=[round(v, 3) for v in imp], new=level)


def run_all():
    res = {}
    res['conjugate'] = fig_conjugate()
    res['gibbs'] = fig_gibbs()
    res['mcmc'] = fig_mcmc_diag()
    fig_minnesota()
    res['shrinkage'] = fig_shrinkage()
    res['factors'] = fig_factors()
    fig_mixed_freq()
    fig_ragged_edge()
    res['news'] = fig_news()
    return res


if __name__ == '__main__':
    import pprint
    pprint.pprint(run_all())
