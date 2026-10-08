"""
seminar12_explainers.py -- Explanatory (primer) charts for Seminar 12 (ATS): machine learning and deep learning
==============================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 12, which takes
place BEFORE Lecture 12. All charts use SIMULATED data only (fixed seeds) and parameters that differ from those of
the exercises: validation schemes, the autocorrelation of an overlapping target, shrinkage rules of penalised
regression, the variance of bagging, trees, forests and boosting, the pinball loss and interval coverage,
vanishing gradients in RNN and LSTM, attention weights, the receptive field of a dilated convolution and the DLinear
decomposition. No exercise answers.

Output: charts/ch12_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each sized for
its box on the slides (ats_style.fit_for_slide), and Quantlets/Ch_12/seminar12_explainers.json (the few numbers the
primer slides quote about these simulations).

Run:  python3 Quantlets/Ch_12/seminar12_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import ats_style as st                                  # noqa: E402

st.apply()
MainBlue, IDAred, Forest, Amber, Navy, Purple = st.MainBlue, st.IDAred, st.Forest, st.Amber, st.DarkText, st.Purple
BandBlue = '#C5D2E8'
CHART_DIR = st.CHART_DIR
TW, TH = 409.72 / 72, 214.79 / 72                       # \textwidth, \textheight of the decks (inches)
TWO = (0.50 * TW, 0.80 * TH)                            # chart in the left column of a two-column primer frame
FULL = (0.96 * TW, 0.62 * TH)                           # full-width chart above two or three bullets
OUT = {}


def save(fig, name, box):
    st.fit_for_slide(fig, name, box=box)
    st.check_no_grey(fig)
    os.makedirs(CHART_DIR, exist_ok=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print(f'   saved {name}')


# =============================================================================
# 1. validation schemes for one fold
# =============================================================================
def fig_cv(n=60, K=5, fold=2, h=3, seed=1):
    rng = np.random.default_rng(seed)
    col = {0: MainBlue, 1: IDAred, 2: Amber, 3: BandBlue}           # train, test, purged, unused
    perm = rng.permutation(n)
    rand = np.zeros(n, int)
    rand[perm[fold * n // K:(fold + 1) * n // K]] = 1
    blk = np.zeros(n, int)
    lo, hi = fold * n // K, (fold + 1) * n // K
    blk[lo:hi] = 1
    pur = blk.copy()
    pur[max(lo - h, 0):lo] = 2
    pur[hi:hi + h] = 2
    oos = np.zeros(n, int)
    oos[int(0.8 * n):] = 1
    rows = [('random K-fold', rand), ('blocked K-fold', blk), (f'blocked, purge $h = {h}$', pur), ('OOS (last block)', oos)]
    fig, ax = plt.subplots(figsize=(10, 2.6))
    for i, (lab, r) in enumerate(rows):
        for t in range(n):
            ax.add_patch(plt.Rectangle((t, -i - 0.4), 0.92, 0.8, color=col[r[t]], lw=0))
    ax.set_xlim(-0.5, n + 0.5)
    ax.set_ylim(-len(rows) + 0.4, 0.6)
    ax.set_yticks([-i for i in range(len(rows))])
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_xlabel('row of the lag matrix (time order)')
    ax.set_title(f'One of the $K = {K}$ folds, $n = {n}$ rows', loc='left')
    for s in ('left',):
        ax.spines[s].set_visible(False)
    handles = [Patch(color=MainBlue, label='training'), Patch(color=IDAred, label='test'),
               Patch(color=Amber, label='purged (dropped)')]
    st.fig_legend_bottom(fig, handles=handles, labels=[h_.get_label() for h_ in handles], ncol=3)
    save(fig, 'ch12_sem_primer_cv', FULL)


# =============================================================================
# 2. the autocorrelation of an overlapping target
# =============================================================================
def fig_overlap(h=10, n=5000, seed=2):
    rng = np.random.default_rng(seed)
    y = rng.standard_normal(n + h)
    z = np.convolve(y, np.ones(h) / h, mode='valid')[1:n + 1]
    zc = z - z.mean()
    K = 20
    acf = np.array([zc[k:] @ zc[:-k] for k in range(1, K + 1)]) / (zc @ zc)
    k = np.arange(1, K + 1)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.bar(k, acf, color=MainBlue, width=0.6, label=r'sample ACF of $z_t$')
    ax.plot(k, np.clip((h - k) / h, 0, None), color=IDAred, lw=1.6, marker='o', ms=3, label=r'$(h - k)/h$')
    ax.axhline(0, color=Navy, lw=0.6)
    ax.set_xlabel('lag $k$')
    ax.set_ylabel('autocorrelation')
    ax.set_title(f'$y_t$ white noise, $z_t$ = mean of the next $h = {h}$', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch12_sem_primer_overlap', TWO)


# =============================================================================
# 3. shrinkage rules under an orthonormal design
# =============================================================================
def fig_shrink(lam=1.0):
    z = np.linspace(-3, 3, 601)
    soft = np.sign(z) * np.maximum(np.abs(z) - lam, 0)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.plot(z, z, color=Navy, lw=1.0, ls=':', label='OLS $z_j$')
    ax.plot(z, soft, color=IDAred, lw=1.8, label='lasso')
    ax.plot(z, z / (1 + lam), color=MainBlue, lw=1.6, label='ridge')
    with np.errstate(divide='ignore', invalid='ignore'):
        ada = np.sign(z) * np.maximum(np.abs(z) - lam / np.abs(z), 0)
    ax.plot(z, ada, color=Forest, lw=1.6, ls='--', label=r'adaptive lasso, $\gamma = 1$')
    en = np.sign(z) * np.maximum(np.abs(z) - lam * 0.5, 0) / (1 + lam * 0.5)
    ax.plot(z, en, color=Amber, lw=1.6, ls='-.', label=r'elastic net, $\alpha = 0.5$')
    ax.set_xlabel('OLS coefficient $z_j$')
    ax.set_ylabel(r'penalised $\hat\beta_j$')
    ax.set_title(f'Shrinkage rules, $\\lambda = {lam:g}$', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch12_sem_primer_shrink', TWO)


# =============================================================================
# 4. the variance of an average of correlated predictors
# =============================================================================
def fig_bagging():
    B = np.arange(1, 201)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    for rho, c in ((0.1, Forest), (0.5, MainBlue), (0.8, IDAred)):
        ax.plot(B, rho + (1 - rho) / B, color=c, lw=1.6, label=f'$\\rho = {rho}$')
        ax.axhline(rho, color=c, lw=0.8, ls=':')
    ax.set_xscale('log')
    ax.set_xlabel('number of trees $B$ (log scale)')
    ax.set_ylabel(r'variance of the average ($\sigma^2 = 1$)')
    ax.set_title(r'Floor $\rho\sigma^2$ (dotted)', loc='left')
    st.legend_outside_bottom(ax, ncol=3)
    save(fig, 'ch12_sem_primer_bagging', TWO)


# =============================================================================
# 5. a tree, a forest and boosting
# =============================================================================
def fig_trees(n=200, seed=6):
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    rng = np.random.default_rng(seed)
    x = np.sort(rng.uniform(0, 6, n))
    y = np.sin(x) + 0.35 * rng.standard_normal(n)
    g = np.linspace(0, 6, 600)[:, None]
    tree = DecisionTreeRegressor(max_depth=3).fit(x[:, None], y)
    rf = RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=0).fit(x[:, None], y)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    for a in ax:
        a.plot(x, y, '.', color=BandBlue, ms=3.5, label='_')
        a.plot(g[:, 0], np.sin(g[:, 0]), color=Navy, lw=1.0, ls=':', label=r'true $\sin x$')
    ax[0].plot(g[:, 0], tree.predict(g), color=IDAred, lw=1.6, label='one tree, depth 3')
    ax[0].plot(g[:, 0], rf.predict(g), color=MainBlue, lw=1.6, label='random forest, 200 trees')
    ax[0].set_xlabel('$x$')
    ax[0].set_title('Piecewise constant fits', loc='left')
    F = np.zeros(n)
    Fg = np.zeros(len(g))
    nu = 0.1
    keep = {1: Amber, 10: Forest, 100: Purple}
    for m in range(1, 101):
        stump = DecisionTreeRegressor(max_depth=1).fit(x[:, None], y - F)
        F += nu * stump.predict(x[:, None])
        Fg += nu * stump.predict(g)
        if m in keep:
            ax[1].plot(g[:, 0], Fg, color=keep[m], lw=1.6, label=f'boosting, $M = {m}$')
    ax[1].set_xlabel('$x$')
    ax[1].set_title(r'Boosting with stumps, $\nu = 0.1$', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch12_sem_primer_trees', FULL)


# =============================================================================
# 6. pinball loss and an 80% interval
# =============================================================================
def fig_pinball(seed=4, n=60):
    u = np.linspace(-2, 2, 401)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    for tau, c in ((0.1, MainBlue), (0.5, Forest), (0.9, IDAred)):
        ax[0].plot(u, np.maximum(tau * u, (tau - 1) * u), color=c, lw=1.6, label=f'$\\tau = {tau}$')
    ax[0].set_xlabel('$u$ = actual $-$ quantile forecast')
    ax[0].set_ylabel(r'$\rho_\tau(u)$')
    ax[0].set_title('Pinball loss', loc='left')
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    m = 10 + 2 * np.sin(2 * np.pi * t / 30)
    y = m + rng.standard_t(4, n)
    q10, q90 = m - 1.9, m + 1.9
    out = (y < q10) | (y > q90)
    ax[1].fill_between(t, q10, q90, color=BandBlue, alpha=0.9, lw=0, label='80% interval $[q_{0.1}, q_{0.9}]$')
    ax[1].plot(t[~out], y[~out], 'o', color=MainBlue, ms=3, label='actual inside')
    ax[1].plot(t[out], y[out], 'o', color=IDAred, ms=3.5, label='actual outside')
    ax[1].set_xlabel('day')
    ax[1].set_title(f'Coverage {100 * (1 - out.mean()):.0f}%, mean width {np.mean(q90 - q10):.1f}', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch12_sem_primer_pinball', FULL)
    OUT['cov'] = float(1 - out.mean())


# =============================================================================
# 7. vanishing gradients: RNN bound and LSTM cell path
# =============================================================================
def fig_gradients():
    k = np.arange(0, 101)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    for w, c in ((0.5, Amber), (0.95, MainBlue)):
        ax.semilogy(k, w ** k, color=c, lw=1.6, label=f'RNN, $|w|^k$, $w = {w}$')
    for b, c in ((-1, IDAred), (2, Forest), (5, Purple)):
        f = 1 / (1 + np.exp(-b))
        ax.semilogy(k, f ** k, color=c, lw=1.6, ls='--', label=f'LSTM, $f^k$, $b_f = {b}$')
    ax.set_ylim(1e-12, 2)
    ax.set_xlabel('steps back $k$')
    ax.set_ylabel('gradient factor (log scale)')
    ax.set_title('Gradient factor $k$ steps back', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch12_sem_primer_gradients', TWO)


# =============================================================================
# 8. attention weights on a seasonal series
# =============================================================================
def fig_attention(n=72, seed=9, scale=3.0):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    x = 5 + 2 * np.sin(2 * np.pi * t / 24) + 0.4 * rng.standard_normal(n)
    E = np.column_stack([np.sin(2 * np.pi * t / 24), np.cos(2 * np.pi * t / 24)]) * scale   # keys: hour of day
    q = np.array([np.sin(2 * np.pi * n / 24), np.cos(2 * np.pi * n / 24)]) * scale            # query: the next hour
    s = E @ q / np.sqrt(2)
    w = np.exp(s - s.max())
    w /= w.sum()
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    ax[0].plot(t, x, color=MainBlue, lw=1.3, label='input $x_1, \\dots, x_{72}$ (hourly)')
    ax[0].axvline(n, color=IDAred, ls='--', lw=1.0, label='forecast origin')
    ax[0].set_xlabel('hour $t$')
    ax[0].set_title('Seasonal input window', loc='left')
    ax[1].bar(t, w, color=IDAred, width=0.8, label='softmax weight of token $t$')
    ax[1].set_xlabel('hour $t$')
    ax[1].set_title('Attention of the next hour on the past', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch12_sem_primer_attention', FULL)
    top = np.argsort(w)[-3:]
    OUT['att'] = dict(top=sorted(int(i) for i in top), share=float(w[top].sum()))


# =============================================================================
# 9. receptive field of a dilated causal convolution
# =============================================================================
def fig_tcn(T=16):
    dil = [1, 2, 4]
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    L = len(dil) + 1
    active = {L - 1: {T - 1}}
    for lev in range(L - 1, 0, -1):                     # trace the inputs of the last output back, kernel 2
        d = dil[lev - 1]
        active[lev - 1] = {t - j * d for t in active[lev] for j in (0, 1) if t - j * d >= 0}
    for lev in range(L):
        for t in range(T):
            on = t in active.get(lev, set())
            ax.plot(t, lev, 'o', color=IDAred if on else BandBlue, ms=6 if on else 4.5, zorder=3)
    for lev in range(L - 1, 0, -1):
        d = dil[lev - 1]
        for t in active[lev]:
            for j in (0, 1):
                if t - j * d >= 0:
                    ax.plot([t, t - j * d], [lev, lev - 1], color=MainBlue, lw=1.0, zorder=2)
    ax.set_yticks(range(L))
    ax.set_yticklabels(['input', 'dilation 1', 'dilation 2', 'dilation 4'])
    ax.set_xticks(range(0, T, 3))
    ax.set_xlabel('time $t$')
    ax.set_title(f'Kernel $k = 2$: the last output sees {len(active[0])} inputs', loc='left')
    ax.spines['left'].set_visible(False)
    save(fig, 'ch12_sem_primer_tcn', TWO)
    OUT['tcn'] = len(active[0])


# =============================================================================
# 10. DLinear decomposition
# =============================================================================
def fig_dlinear(n=200, seed=12, w=25):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    x = 0.02 * t + 1.5 * np.sin(2 * np.pi * t / 12) + 0.6 * rng.standard_normal(n) + 0.002 * (t - 100) ** 2 / 10
    pad = np.r_[np.repeat(x[0], w // 2), x, np.repeat(x[-1], w // 2)]
    trend = np.convolve(pad, np.ones(w) / w, mode='valid')
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    ax[0].plot(t, x, color=MainBlue, lw=1.0, label='input window $x$')
    ax[0].plot(t, trend, color=IDAred, lw=1.8, label=f'trend $Ax$ (moving average, length {w})')
    ax[0].set_xlabel('$t$')
    ax[0].set_title('Trend by a moving average', loc='left')
    ax[1].plot(t, x - trend, color=Forest, lw=1.0, label='remainder $x - Ax$')
    ax[1].axhline(0, color=Navy, lw=0.6)
    ax[1].set_xlabel('$t$')
    ax[1].set_title('Remainder (seasonal and noise)', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch12_sem_primer_dlinear', FULL)


if __name__ == '__main__':
    fig_cv()
    fig_overlap()
    fig_shrink()
    fig_bagging()
    fig_trees()
    fig_pinball()
    fig_gradients()
    fig_attention()
    fig_tcn()
    fig_dlinear()
    with open(os.path.join(HERE, 'seminar12_explainers.json'), 'w') as fh:
        json.dump(OUT, fh, indent=1)
    print(json.dumps(OUT, indent=1))
