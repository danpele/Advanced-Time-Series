"""
seminar3_explainers.py -- Explanatory (primer) charts for Seminar 3 (ATS): structural VARs and local projections
================================================================================================================
Teaching charts for the slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 3, which takes
place BEFORE Lecture 3. All charts use SIMULATED data or a textbook VAR with chosen coefficients (fixed seeds):
they illustrate the concepts (impulse responses, the variance decomposition, long-run restrictions, the set
identified by sign restrictions, weak instruments and the Anderson--Rubin set, local projections against a VAR,
bootstrap bands) and contain no exercise answers.

Output: charts/ch3_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each
sized for its box on the slides (text at least 6.4 pt there).

Run:  python3 Quantlets/Ch_03/seminar3_explainers.py
      (run it again after the seminar decks are regenerated, so that every chart gets its slide box)

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
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'Quantlets', 'common'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import ats_style as st                      # noqa: E402
from chart_boxes import boxes as deck_boxes  # noqa: E402

st.SLIDE_MIN_PT = 6.4
st.SLIDE_BASE_PT = 6.8
CHART_DIR = os.path.join(REPO, 'charts')
SEED = 2026
B, R, G, A, P, N = st.MainBlue, st.IDAred, st.Forest, st.Amber, st.Purple, st.DarkText
_BOX = None

# a bivariate VAR(1) used in several charts (coefficients chosen for illustration)
A1 = np.array([[0.5, 0.1], [0.4, 0.6]])
SIG = np.array([[1.0, 0.5], [0.5, 1.5]])


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


def irf(A, B0, H):
    """Structural impulse responses Theta_h = Phi_h B0 of a VAR(1), h = 0..H (array H+1 x n x n)."""
    out, Ph = [], np.eye(len(A))
    for _ in range(H + 1):
        out.append(Ph @ B0)
        Ph = A @ Ph
    return np.array(out)


# =============================================================================
# 1. Cholesky impulse responses of a bivariate VAR(1)
# =============================================================================
def chart_irf():
    P = np.linalg.cholesky(SIG)
    th = irf(A1, P, 12)
    h = np.arange(13)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
    for i in range(2):
        ax[i].plot(h, th[:, i, 0], color=B, marker='o', ms=3, lw=1.5, label=r'to shock 1, $\theta_{i1,h}$')
        ax[i].plot(h, th[:, i, 1], color=R, marker='s', ms=3, lw=1.5, label=r'to shock 2, $\theta_{i2,h}$')
        ax[i].axhline(0, color=N, lw=0.6, ls='--')
        ax[i].set_xlabel('horizon $h$')
        ax[i].set_title(f'Response of $y_{{{i + 1}}}$')
    ax[0].set_ylabel('response')
    fig.tight_layout()
    st.fig_legend_bottom(fig, ncol=2)
    save(fig, 'ch3_sem_primer_irf')


# =============================================================================
# 2. Forecast error variance decomposition of y2
# =============================================================================
def chart_fevd():
    P = np.linalg.cholesky(SIG)
    th = irf(A1, P, 20)
    H = np.arange(1, 21)
    num = np.cumsum(th[:, 1, :] ** 2, axis=0)[:20]           # sum over s < h
    share = num / num.sum(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    ax.stackplot(H, 100 * share[:, 0], 100 * share[:, 1], colors=[B, A], alpha=0.75,
                 labels=['shock 1', 'shock 2'])
    ax.set_xlim(1, 20)
    ax.set_ylim(0, 100)
    ax.set_xlabel('forecast horizon $h$')
    ax.set_ylabel('share of the variance (%)')
    ax.set_title('FEVD of $y_2$, Cholesky ordering $(y_1, y_2)$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch3_sem_primer_fevd')


# =============================================================================
# 3. Long-run restrictions: a permanent and a transitory shock
# =============================================================================
def chart_longrun():
    A = np.array([[0.3, -0.2], [0.1, 0.7]])                   # VAR(1) for (output growth, unemployment)
    S = np.array([[1.0, -0.3], [-0.3, 0.5]])
    A1i = np.linalg.inv(np.eye(2) - A)
    Th1 = np.linalg.cholesky(A1i @ S @ A1i.T)                 # long-run impact, lower triangular
    B0 = (np.eye(2) - A) @ Th1
    th = irf(A, B0, 24)
    level = np.cumsum(th[:, 0, :], axis=0)                    # output level = cumulated growth
    h = np.arange(25)
    sgn = np.sign(level[-1, 0])
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.plot(h, sgn * level[:, 0], color=B, lw=1.8, marker='o', ms=3, label='output level, supply shock (permanent)')
    s2 = np.sign(level[:3, 1].sum()) or 1
    ax.plot(h, s2 * level[:, 1], color=R, lw=1.8, marker='s', ms=3, label='output level, demand shock (transitory)')
    ax.axhline(0, color=N, lw=0.6, ls='--')
    ax.set_xlabel('horizon $h$')
    ax.set_ylabel('cumulated response')
    ax.set_title(r'Long-run restriction: the demand shock has no effect on the level as $h \to \infty$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch3_sem_primer_longrun')


# =============================================================================
# 4. Sign restrictions: impact responses along the rotation angle
# =============================================================================
def chart_signs():
    S = np.array([[1.0, -0.4], [-0.4, 1.0]])                  # (price, quantity)
    P = np.linalg.cholesky(S)
    th = np.linspace(0, 2 * np.pi, 721)
    b11 = P[0, 0] * np.cos(th) - 0 * np.sin(th)
    b21 = P[1, 0] * np.cos(th) + P[1, 1] * np.sin(th)
    ok = (b11 > 0) & (b21 > 0)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.plot(th, b11, color=B, lw=1.6, label=r'impact on the price, $b_{11}(\theta)$')
    ax.plot(th, b21, color=R, lw=1.6, label=r'impact on the quantity, $b_{21}(\theta)$')
    ax.fill_between(th, -1.2, 1.2, where=ok, color=G, alpha=0.3, lw=0, label='both positive: admissible')
    ax.axhline(0, color=N, lw=0.6, ls='--')
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
    ax.set_xticklabels(['0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
    ax.set_xlabel(r'rotation angle $\theta$')
    ax.set_ylabel('impact of the first shock')
    ax.set_title(r'First column of $B_0 = PR(\theta)$, an illustrative $\Sigma_u$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=3)
    save(fig, 'ch3_sem_primer_signs')


# =============================================================================
# 5. Weak instruments: the sampling distribution of the IV estimator
# =============================================================================
def iv_sample(rng, T, pi, beta=1.0, rho=0.8):
    z = rng.standard_normal(T)
    e = rng.standard_normal((T, 2))
    v = e[:, 0]
    u = rho * v + np.sqrt(1 - rho ** 2) * e[:, 1]             # endogeneity: corr(u, v) = rho
    x = pi * z + v
    y = beta * x + u
    return y, x, z


def chart_weakiv():
    rng = np.random.default_rng(SEED)
    T, reps = 100, 4000
    res = {}
    for lab, pi in (('strong', 0.7), ('weak', 0.12)):
        b, F = np.empty(reps), np.empty(reps)
        for r in range(reps):
            y, x, z = iv_sample(rng, T, pi)
            b[r] = (z @ y) / (z @ x)
            g = (z @ x) / (z @ z)
            e = x - g * z
            F[r] = g ** 2 / (e @ e / (T - 1) / (z @ z))
        res[lab] = (b, np.median(F))
    grid = np.linspace(-2, 4, 121)
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    for lab, c in (('strong', B), ('weak', R)):
        b, Fm = res[lab]
        ax.hist(np.clip(b, -2, 4), bins=grid, density=True, histtype='step', color=c, lw=1.6,
                label=rf'{lab} instrument, median first-stage $F = {Fm:.0f}$')
    ax.axvline(1, color=G, lw=1.2, ls='--', label=r'true $\beta = 1$')
    ax.axvline(1 + 0.8 / (1 + 0.12 ** 2), color=A, lw=1.2, ls='-.', label='probability limit of OLS (weak case)')
    ax.set_xlabel(r'IV estimate $\hat\beta$ (clipped to $[-2, 4]$)')
    ax.set_ylabel('density')
    ax.set_title(r'4000 samples, $T = 100$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch3_sem_primer_weakiv')


# =============================================================================
# 6. Anderson--Rubin statistic: a bounded and an unbounded set
# =============================================================================
def ar_stat(y, x, z, betas):
    T = len(y)
    out = []
    for b in betas:
        r = y - b * x
        g = (z @ r) / (z @ z)
        e = r - g * z
        s2 = np.sum(e ** 2 * z ** 2) / (z @ z) ** 2               # heteroskedasticity-robust variance of g
        out.append(g ** 2 / s2)
    return np.array(out)


def chart_arset():
    rng = np.random.default_rng(SEED + 1)
    T = 150
    betas = np.linspace(-6, 8, 701)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    for lab, pi, c in (('strong instrument', 0.6, B), ('weak instrument', 0.06, R)):
        y, x, z = iv_sample(rng, T, pi)
        ax.plot(betas, ar_stat(y, x, z, betas), color=c, lw=1.6, label=lab)
    cv = stats.chi2.ppf(0.90, 1)
    ax.axhline(cv, color=G, lw=1.2, ls='--', label=rf'90% critical value $\chi^2_{{0.90}}(1) = {cv:.2f}$')
    ax.set_ylim(0, 20)
    ax.set_xlabel(r'hypothesised effect $\beta_0$')
    ax.set_ylabel(r'$\mathrm{AR}(\beta_0)$')
    ax.set_title(r'Anderson--Rubin set $= \{\beta_0: \mathrm{AR}(\beta_0) \leq$ critical value$\}$'.replace('--', '–'))
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=3)
    save(fig, 'ch3_sem_primer_arset')


# =============================================================================
# 7. Local projections against the VAR on one simulated AR(2) sample
# =============================================================================
def nw_se(X, e, L):
    """Newey--West standard errors of OLS coefficients with L lags."""
    T = len(e)
    XXi = np.linalg.inv(X.T @ X)
    g = X * e[:, None]
    S = g.T @ g
    for j in range(1, L + 1):
        w = 1 - j / (L + 1)
        G = g[j:].T @ g[:-j]
        S += w * (G + G.T)
    return np.sqrt(np.diag(XXi @ S @ XXi))


def chart_lp():
    rng = np.random.default_rng(SEED + 2)
    a1, a2, T, H = 1.2, -0.4, 240, 16
    eps = rng.standard_normal(T + 100)
    y = np.zeros(T + 100)
    for t in range(2, T + 100):
        y[t] = a1 * y[t - 1] + a2 * y[t - 2] + eps[t]
    y, eps = y[100:], eps[100:]
    true = [1.0, a1]
    for h in range(2, H + 1):
        true.append(a1 * true[-1] + a2 * true[-2])
    # LP of y_{t+h} on the observed shock eps_t, with two lags of y as controls
    b, se = [], []
    for h in range(H + 1):
        Y = y[2 + h:]
        X = np.c_[np.ones(T - 2 - h), eps[2:T - h], y[1:T - 1 - h], y[0:T - 2 - h]]
        coef = np.linalg.lstsq(X, Y, rcond=None)[0]
        e = Y - X @ coef
        b.append(coef[1])
        se.append(nw_se(X, e, h + 1)[1])
    b, se = np.array(b), np.array(se)
    # VAR (AR(2)) responses
    X = np.c_[np.ones(T - 2), y[1:T - 1], y[0:T - 2]]
    c = np.linalg.lstsq(X, y[2:], rcond=None)[0]
    var = [1.0, c[1]]
    for h in range(2, H + 1):
        var.append(c[1] * var[-1] + c[2] * var[-2])
    hh = np.arange(H + 1)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.fill_between(hh, b - 1.96 * se, b + 1.96 * se, color=st.LightBlue, alpha=0.35, lw=0, label='LP 95% band (Newey--West)'.replace('--', '–'))
    ax.plot(hh, b, color=B, marker='o', ms=3, lw=1.4, label=r'LP $\hat\beta_h$')
    ax.plot(hh, var, color=R, lw=1.6, ls='--', label='AR(2) iterated response')
    ax.plot(hh, true, color=G, lw=1.2, ls=':', label='true response')
    ax.axhline(0, color=N, lw=0.6)
    ax.set_xlabel('horizon $h$')
    ax.set_ylabel('response to a unit shock')
    ax.set_title(r'One sample, $T = 240$, $y_t = 1.2y_{t-1} - 0.4y_{t-2} + \varepsilon_t$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch3_sem_primer_lp')


# =============================================================================
# 8. Residual bootstrap bands for an impulse response (recursive design)
# =============================================================================
def chart_bands():
    rng = np.random.default_rng(SEED + 3)
    a1, a2, T, H, Bn = 1.2, -0.4, 120, 16, 999
    e0 = rng.standard_normal(T + 100)
    y = np.zeros(T + 100)
    for t in range(2, T + 100):
        y[t] = a1 * y[t - 1] + a2 * y[t - 2] + e0[t]
    y = y[100:]

    def fit(y):
        X = np.c_[np.ones(len(y) - 2), y[1:-1], y[:-2]]
        c = np.linalg.lstsq(X, y[2:], rcond=None)[0]
        return c, y[2:] - X @ c

    def resp(c):
        r = [1.0, c[1]]
        for _ in range(2, H + 1):
            r.append(c[1] * r[-1] + c[2] * r[-2])
        return np.array(r)
    c, u = fit(y)
    point = resp(c)
    boot = np.empty((Bn, H + 1))
    for b in range(Bn):
        us = rng.choice(u - u.mean(), size=T)
        ys = np.zeros(T)
        ys[:2] = y[:2]
        for t in range(2, T):
            ys[t] = c[0] + c[1] * ys[t - 1] + c[2] * ys[t - 2] + us[t]
        boot[b] = resp(fit(ys)[0])
    hh = np.arange(H + 1)
    q = np.quantile(boot, [0.05, 0.16, 0.84, 0.95], axis=0)
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    ax.fill_between(hh, q[0], q[3], color=st.LightBlue, alpha=0.35, lw=0, label='90% percentile band')
    ax.fill_between(hh, q[1], q[2], color=B, alpha=0.35, lw=0, label='68% percentile band')
    ax.plot(hh, point, color=B, lw=1.8, label='estimated response')
    ax.axhline(0, color=N, lw=0.6)
    ax.set_xlabel('horizon $h$')
    ax.set_ylabel('response')
    ax.set_title(f'AR(2), $T = {T}$, {Bn} bootstrap samples')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch3_sem_primer_bands')


def main():
    st.apply()
    chart_irf()
    chart_fevd()
    chart_longrun()
    chart_signs()
    chart_weakiv()
    chart_arset()
    chart_lp()
    chart_bands()


if __name__ == '__main__':
    main()
