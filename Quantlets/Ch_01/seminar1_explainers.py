"""
seminar1_explainers.py -- Explanatory (primer) charts for Seminar 1 (ATS): forecast evaluation
================================================================================================
Teaching charts for the slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 1, which takes
place BEFORE Lecture 1. All charts use SIMULATED data or textbook distributions only (fixed seeds): they
illustrate the concepts (loss functions, optimal point forecasts, PIT histograms, CRPS, the interval score,
the loss differential of the Diebold--Mariano test, Mincer--Zarnowitz regressions, forecast combination) and
contain no exercise answers.

Output: charts/ch1_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each
sized for its box on the slides (text at least 6.4 pt there).

Run:  python3 Quantlets/Ch_01/seminar1_explainers.py
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


# =============================================================================
# 1. Loss functions of the forecast error e = y - x
# =============================================================================
def chart_losses():
    e = np.linspace(-3, 3, 400)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    ax[0].plot(e, e ** 2, color=B, lw=1.6, label='squared $e^2$')
    ax[0].plot(e, np.abs(e), color=R, lw=1.6, label='absolute $|e|$')
    ax[0].set_ylim(0, 4)
    ax[0].set_title('Symmetric losses')
    tau, a = 0.9, 0.5
    ax[1].plot(e, (tau - (e < 0)) * e, color=G, lw=1.6, label=r'pinball, $\tau = 0.9$')
    ax[1].plot(e, np.exp(a * e) - a * e - 1, color=A, lw=1.6, label=r'LinEx, $a = 0.5$, $b = 1$')
    ax[1].set_ylim(0, 2.8)
    ax[1].set_title('Asymmetric losses')
    for x in ax:
        x.axvline(0, color=N, lw=0.6, ls='--')
        x.set_xlabel('forecast error $e = y - x$')
        x.set_ylabel('loss')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=2)
    st.legend_outside_bottom(ax[1], ncol=1)
    save(fig, 'ch1_sem_primer_losses')


# =============================================================================
# 2. Optimal point forecasts of a skewed variable: mean, median, quantile
# =============================================================================
def chart_optimal():
    d = stats.gamma(2)
    y = np.linspace(0, 9, 400)
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    ax.plot(y, d.pdf(y), color=B, lw=1.6, label='_d')
    ax.fill_between(y, 0, d.pdf(y), where=y <= d.ppf(0.9), color=st.LightBlue, alpha=0.35, lw=0, label='_f')
    for v, c, ls, lab in ((d.mean(), R, '-', f'mean {d.mean():.2f}: squared loss'),
                          (d.median(), G, '--', f'median {d.median():.2f}: absolute loss'),
                          (d.ppf(0.9), A, '-.', f'0.9-quantile {d.ppf(0.9):.2f}: pinball, ' + r'$\tau = 0.9$')):
        ax.axvline(v, color=c, lw=1.5, ls=ls, label=lab)
    ax.text(1.0, 0.03, '90%', color=B, fontsize=11)
    ax.set_xlabel('$y$')
    ax.set_ylabel('density $f(y)$')
    ax.set_title('Gamma(2, 1): three optimal forecasts')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch1_sem_primer_optimal')


# =============================================================================
# 3. PIT histograms: calibrated, too narrow, too wide, biased
# =============================================================================
def chart_pit():
    rng = np.random.default_rng(SEED)
    y = rng.standard_normal(2000)
    cases = [('calibrated: $N(0, 1)$', stats.norm.cdf(y), B),
             ('too narrow: $N(0, 0.6^2)$', stats.norm.cdf(y / 0.6), R),
             ('too wide: $N(0, 1.6^2)$', stats.norm.cdf(y / 1.6), G),
             ('biased: $N(0.5, 1)$', stats.norm.cdf(y - 0.5), A)]
    fig, axs = plt.subplots(2, 2, figsize=(5.4, 4.4), sharex=True, sharey=True)
    for ax, (t, u, c) in zip(axs.ravel(), cases):
        ax.hist(u, bins=10, range=(0, 1), density=True, color=c, alpha=0.75, edgecolor='white', lw=0.5)
        ax.axhline(1, color=N, lw=0.8, ls='--')
        ax.set_title(t)
        ax.set_ylim(0, 2.6)
    for ax in axs[1]:
        ax.set_xlabel('PIT $u_t = F_t(y_t)$')
    for ax in axs[:, 0]:
        ax.set_ylabel('density')
    fig.tight_layout()
    save(fig, 'ch1_sem_primer_pit')


# =============================================================================
# 4. CRPS: the area between the forecast CDF and the step at the outcome; scores as functions of y
# =============================================================================
def crps_normal(y, mu, s):
    z = (y - mu) / s
    return s * (z * (2 * stats.norm.cdf(z) - 1) + 2 * stats.norm.pdf(z) - 1 / np.sqrt(np.pi))


def chart_crps():
    z = np.linspace(-4, 4, 600)
    y0 = 1.2
    F = stats.norm.cdf(z)
    step = (z >= y0).astype(float)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.7))
    ax[0].plot(z, F, color=B, lw=1.6, label='forecast CDF $F(z)$, $N(0, 1)$')
    ax[0].plot(z, step, color=R, lw=1.6, label=r'outcome: $\mathbf{1}\{y \leq z\}$, $y = 1.2$')
    ax[0].fill_between(z, F, step, color=A, alpha=0.4, lw=0, label='squared gap integrated: CRPS')
    ax[0].set_xlabel('$z$')
    ax[0].set_ylabel('probability')
    ax[0].set_title(f'CRPS $= {crps_normal(y0, 0, 1):.3f}$')
    y = np.linspace(-4, 4, 400)
    for s, c, ls in ((1.0, B, '-'), (0.5, R, '--')):
        ax[1].plot(y, -stats.norm.logpdf(y, scale=s), color=c, lw=1.5, ls=ls, label=rf'log score, $\sigma = {s:g}$')
        ax[1].plot(y, crps_normal(y, 0, s), color=c, lw=1.0, ls=':', label=rf'CRPS, $\sigma = {s:g}$')
    ax[1].set_ylim(0, 6)
    ax[1].set_xlabel('outcome $y$')
    ax[1].set_ylabel('score (lower is better)')
    ax[1].set_title(r'Two forecasts $N(0, \sigma^2)$')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=1)
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch1_sem_primer_crps')


# =============================================================================
# 5. The interval score of a central 90% interval
# =============================================================================
def chart_interval():
    l, u, alpha = -1.645, 1.645, 0.10
    y = np.linspace(-3.5, 3.5, 500)
    IS = (u - l) + 2 / alpha * (l - y) * (y < l) + 2 / alpha * (y - u) * (y > u)
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    ax.axvspan(l, u, color=st.LightBlue, alpha=0.35, lw=0, label='90% interval $[l, u]$')
    ax.plot(y, IS, color=B, lw=1.8, label='interval score')
    ax.axhline(u - l, color=G, lw=1.0, ls='--', label=f'width $u - l = {u - l:.2f}$')
    ax.annotate(r'slope $2/\alpha = 20$', xy=(2.6, (u - l) + 20 * (2.6 - u)), xytext=(0.2, 25),
                color=R, fontsize=11, arrowprops=dict(arrowstyle='->', color=R, lw=0.8))
    ax.set_xlabel('outcome $y$')
    ax.set_ylabel('score (lower is better)')
    ax.set_title(r'$\alpha = 0.10$, interval $[-1.645, 1.645]$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch1_sem_primer_interval')


# =============================================================================
# 6. The loss differential of h-step forecasts: an MA(h - 1)
# =============================================================================
def chart_dm():
    rng = np.random.default_rng(SEED + 1)
    P, h = 120, 3
    e = rng.standard_normal(P + h)
    d = 0.15 + (e[2:] + e[1:-1] + e[:-2])[:P] / np.sqrt(3)       # MA(2): overlapping three-step targets
    K = 10
    dc = d - d.mean()
    acf = np.array([np.dot(dc[k:], dc[:P - k]) / np.dot(dc, dc) for k in range(1, K + 1)])
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
    ax[0].plot(np.arange(1, P + 1), d, color=B, lw=0.9, label='$d_t$')
    ax[0].axhline(d.mean(), color=R, lw=1.4, label=rf'$\bar d = {d.mean():.2f}$')
    ax[0].axhline(0, color=N, lw=0.6, ls='--', label='_z')
    ax[0].set_xlabel('forecast $t$')
    ax[0].set_ylabel('$d_t = L(e_{1t}) - L(e_{2t})$')
    ax[0].set_title(r'Loss differential, $h = 3$, $P = 120$')
    ax[1].bar(np.arange(1, K + 1), acf, color=A, width=0.6, label='sample ACF of $d_t$')
    ax[1].axhspan(-1.96 / np.sqrt(P), 1.96 / np.sqrt(P), color=st.LightBlue, alpha=0.35, lw=0, label=r'$\pm 1.96/\sqrt{P}$')
    ax[1].axhline(0, color=N, lw=0.6)
    ax[1].set_xlabel('lag $k$')
    ax[1].set_ylabel('autocorrelation')
    ax[1].set_title('Lags 1 and 2 correlated, the rest not')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=2)
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch1_sem_primer_dm')


# =============================================================================
# 7. Mincer--Zarnowitz: an efficient forecast and a timid one
# =============================================================================
def chart_mz():
    rng = np.random.default_rng(SEED + 2)
    n = 150
    m = rng.normal(0, 1.2, n)                     # predictable part
    y = 2 + m + rng.normal(0, 1, n)
    f_eff = 2 + m
    f_tim = 2 + 0.5 * m
    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    for f, c, mk, lab in ((f_eff, B, 'o', 'efficient'), (f_tim, R, '^', 'timid (shrunk to the mean)')):
        b1, b0 = np.polyfit(f, y, 1)
        ax.scatter(f, y, s=8, color=c, alpha=0.5, marker=mk, label='_s')
        xx = np.linspace(f.min(), f.max(), 10)
        ax.plot(xx, b0 + b1 * xx, color=c, lw=1.6, label=rf'{lab}: $\hat a = {b0:.2f}$, $\hat b = {b1:.2f}$')
    xx = np.linspace(-1.5, 5.5, 10)
    ax.plot(xx, xx, color=N, lw=0.9, ls='--', label='45-degree line: $a = 0$, $b = 1$')
    ax.set_xlabel(r'forecast $\hat y_{t+h|t}$')
    ax.set_ylabel('outcome $y_{t+h}$')
    ax.set_title('Mincer–Zarnowitz regressions')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch1_sem_primer_mz')


# =============================================================================
# 8. Forecast combination: the MSE as a function of the weight
# =============================================================================
def chart_combination():
    s1, s2, rho = 1.0, 1.3, 0.5
    s12 = rho * s1 * s2
    D = s1 ** 2 + s2 ** 2 - 2 * s12
    w = np.linspace(-0.2, 1.2, 400)
    mse = w ** 2 * s1 ** 2 + (1 - w) ** 2 * s2 ** 2 + 2 * w * (1 - w) * s12
    ws = (s2 ** 2 - s12) / D
    m_opt = (s1 ** 2 * s2 ** 2 - s12 ** 2) / D
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    ax.plot(w, mse, color=B, lw=1.8, label=r'$\mathrm{MSE}(w)$')
    ax.plot([ws], [m_opt], 'o', color=R, ms=6, label=rf'optimal $w^* = {ws:.2f}$')
    ax.plot([0.5], [0.25 * (s1 ** 2 + s2 ** 2 + 2 * s12)], 's', color=G, ms=6, label='equal weights $w = 1/2$')
    ax.plot([1, 0], [s1 ** 2, s2 ** 2], 'D', color=A, ms=5, label='one forecast alone ($w = 1$ or $0$)')
    ax.set_xlabel('weight $w$ on forecast 1')
    ax.set_ylabel('MSE of the combination')
    ax.set_title(rf'$\sigma_1 = {s1:g}$, $\sigma_2 = {s2:g}$, $\rho = {rho:g}$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch1_sem_primer_combination')


def main():
    st.apply()
    chart_losses()
    chart_optimal()
    chart_pit()
    chart_crps()
    chart_interval()
    chart_dm()
    chart_mz()
    chart_combination()


if __name__ == '__main__':
    main()
