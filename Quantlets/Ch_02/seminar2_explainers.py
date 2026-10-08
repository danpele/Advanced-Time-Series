"""
seminar2_explainers.py -- Explanatory (primer) charts for Seminar 2 (ATS): structural breaks and nonlinear models
=================================================================================================================
Teaching charts for the slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 2, which takes
place BEFORE Lecture 2. All charts use SIMULATED data only (fixed seeds): they illustrate the concepts (a mean
shift and the F distribution, the Wald process and the sup-Wald test, Bai--Perron partitions with BIC and LWZ,
the distribution of the break-date estimator, monitoring boundaries, the Inclán--Tiao statistic, the estimation
window trade-off, a SETAR skeleton, smooth transition functions) and contain no exercise answers.

Output: charts/ch2_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each
sized for its box on the slides (text at least 6.4 pt there).

Run:  python3 Quantlets/Ch_02/seminar2_explainers.py
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


def wald_process(y, lo=0.15, hi=0.85, sigma2=None):
    """Wald statistics of a mean shift at every candidate fraction (pooled residual variance unless given)."""
    T = len(y)
    ks = np.arange(int(np.floor(lo * T)), int(np.ceil(hi * T)) + 1)
    out = []
    for k in ks:
        m1, m2 = y[:k].mean(), y[k:].mean()
        s2 = sigma2 if sigma2 is not None else (np.sum((y[:k] - m1) ** 2) + np.sum((y[k:] - m2) ** 2)) / (T - 2)
        out.append(k * (T - k) / T * (m1 - m2) ** 2 / s2)
    return ks / T, np.array(out)


def sup_wald_cv(lo=0.15, hi=0.85, n=400, reps=6000, alpha=0.05, seed=SEED):
    """5% critical value of sup B(pi)^2 / [pi (1 - pi)] over [lo, hi] (Andrews 1993), by simulation."""
    rng = np.random.default_rng(seed)
    W = np.cumsum(rng.standard_normal((reps, n)), axis=1) / np.sqrt(n)
    r = np.arange(1, n + 1) / n
    Bb = W - r * W[:, -1:]
    sel = (r >= lo) & (r <= hi)
    stat = (Bb[:, sel] ** 2 / (r[sel] * (1 - r[sel]))).max(axis=1)
    return float(np.quantile(stat, 1 - alpha))


# =============================================================================
# 1. A mean shift at a known date and the F distribution of the Chow test
# =============================================================================
def chart_break():
    rng = np.random.default_rng(SEED)
    T, T1 = 120, 72
    y = np.r_[rng.normal(1.0, 1, T1), rng.normal(2.2, 1, T - T1)]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    t = np.arange(1, T + 1)
    ax[0].plot(t, y, color=B, lw=0.9, label='$y_t$')
    ax[0].hlines(y.mean(), 1, T, color=A, lw=1.4, ls='--', label='pooled mean')
    ax[0].hlines([y[:T1].mean(), y[T1:].mean()], [1, T1 + 1], [T1, T], color=R, lw=1.8, label='sub-sample means')
    ax[0].axvline(T1 + 0.5, color=N, lw=0.7, ls=':')
    ax[0].set_xlabel('$t$')
    ax[0].set_title(r'A mean shift after $T_1 = 72$')
    k, df2 = 2, 116
    x = np.linspace(0, 8, 400)
    cv = stats.f.ppf(0.95, k, df2)
    ax[1].plot(x, stats.f.pdf(x, k, df2), color=B, lw=1.6, label=r'density of $F(2, 116)$')
    ax[1].fill_between(x, 0, stats.f.pdf(x, k, df2), where=x >= cv, color=R, alpha=0.4, lw=0, label=f'5% rejection region, $F > {cv:.2f}$')
    ax[1].set_xlabel('value of the $F$ statistic')
    ax[1].set_ylabel('density')
    ax[1].set_title('Reference distribution of the Chow test')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=3)
    st.legend_outside_bottom(ax[1], ncol=1)
    save(fig, 'ch2_sem_primer_break')


# =============================================================================
# 2. The Wald process and the sup-Wald critical value
# =============================================================================
def chart_supwald():
    rng = np.random.default_rng(SEED + 1)
    T = 150
    y0 = rng.standard_normal(T)
    y1 = rng.standard_normal(T) + 0.6 * (np.arange(T) >= 90)
    try:                                          # the critical value used on the slides (Chapter 2 tables)
        import json
        with open(os.path.join(HERE, 'ch2_numbers.json')) as fh:
            cv = float(json.load(fh)['chow']['cv']['sup']['1'][1])
    except (OSError, KeyError, ValueError):
        cv = sup_wald_cv()
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    for y, c, lab in ((y0, B, 'no break'), (y1, R, r'break at $\pi = 0.6$')):
        p, w = wald_process(y)
        ax.plot(p, w, color=c, lw=1.5, label=lab)
    ax.axhline(3.84, color=G, lw=1.0, ls='--', label=r'3.84: $\chi^2_{0.95}(1)$, known date')
    ax.axhline(cv, color=A, lw=1.2, ls='-.', label=f'{cv:.2f}: 5% value of the supremum')
    ax.set_xlabel(r'candidate break fraction $\pi$')
    ax.set_ylabel(r'$W_T(\pi)$')
    ax.set_title(r'Wald process, trimming $[0.15, 0.85]$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch2_sem_primer_supwald')


# =============================================================================
# 3. Bai--Perron: the best partition by dynamic programming, BIC and LWZ
# =============================================================================
def best_partitions(y, M, h):
    """Global minimisers of the SSR of mean-shift models with 0..M breaks (dynamic programming)."""
    T = len(y)
    cs, cs2 = np.r_[0, np.cumsum(y)], np.r_[0, np.cumsum(y ** 2)]

    def ssr(i, j):                         # observations i..j-1 (0-based, half-open)
        n = j - i
        return cs2[j] - cs2[i] - (cs[j] - cs[i]) ** 2 / n
    INF = np.inf
    best = {0: {j: (ssr(0, j), []) for j in range(h, T + 1)}}
    for m in range(1, M + 1):
        best[m] = {}
        for j in range((m + 1) * h, T + 1):
            cand = [(best[m - 1][k][0] + ssr(k, j), best[m - 1][k][1] + [k])
                    for k in range(m * h, j - h + 1) if k in best[m - 1]]
            best[m][j] = min(cand, key=lambda z: z[0]) if cand else (INF, [])
    return [best[m][T] for m in range(M + 1)]


def chart_bp():
    rng = np.random.default_rng(SEED + 2)
    T = 150
    mu = np.r_[np.full(50, 0.0), np.full(55, 1.5), np.full(45, 0.6)]
    y = mu + rng.standard_normal(T)
    M, h = 5, 15
    parts = best_partitions(y, M, h)
    ssr = np.array([p[0] for p in parts])
    m = np.arange(M + 1)
    pstar = 2 * m + 1
    bic = np.log(ssr / T) + pstar * np.log(T) / T
    lwz = np.log(ssr / (T - pstar)) + pstar * 0.299 * np.log(T) ** 2.1 / T
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    t = np.arange(1, T + 1)
    ax[0].plot(t, y, color=B, lw=0.8, label='$y_t$')
    br = parts[2][1]
    edges = [0] + br + [T]
    for i in range(3):
        a, b = edges[i], edges[i + 1]
        ax[0].hlines(y[a:b].mean(), a + 1, b, color=R, lw=1.8, label='fitted means, $m = 2$' if i == 0 else '_f')
    ax[0].plot(t, mu, color=G, lw=1.0, ls='--', label='true means')
    ax[0].set_xlabel('$t$')
    ax[0].set_title('Best two-break partition')
    ax[1].plot(m, bic, color=B, marker='o', ms=4, lw=1.4, label='BIC$(m)$')
    ax[1].plot(m, lwz, color=A, marker='s', ms=4, lw=1.4, label='LWZ$(m)$')
    ax[1].set_xlabel('number of breaks $m$')
    ax[1].set_ylabel('criterion')
    ax[1].set_title('Choose the $m$ with the smallest value')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=3)
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch2_sem_primer_bp')


# =============================================================================
# 4. The limit distribution of the break-date estimator (Bai 1997)
# =============================================================================
def chart_bai():
    rng = np.random.default_rng(SEED + 3)
    reps, L, ds = 4000, 120.0, 0.05
    n = int(L / ds)
    s = np.arange(1, n + 1) * ds
    out = np.empty(reps)
    for r in range(reps):
        wr = np.cumsum(rng.standard_normal(n)) * np.sqrt(ds) - s / 2
        wl = np.cumsum(rng.standard_normal(n)) * np.sqrt(ds) - s / 2
        ir, il = wr.argmax(), wl.argmax()
        out[r] = s[ir] if wr[ir] > max(wl[il], 0) else (-s[il] if wl[il] > 0 else 0.0)
    q = np.quantile(out, [0.025, 0.975])
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    ax.hist(out, bins=np.arange(-40, 40.5, 1.0), density=True, color=st.LightBlue, edgecolor='white', lw=0.3,
            label=r'simulated $\arg\max_s[W(s) - |s|/2]$')
    for v in q:
        ax.axvline(v, color=R, lw=1.4, ls='--')
    ax.plot([], [], color=R, ls='--', label=f'2.5% and 97.5% quantiles: {q[0]:.1f}, {q[1]:.1f}')
    ax.set_xlim(-40, 40)
    ax.set_xlabel(r'$(\delta^2/\sigma^2)(\hat T_1 - T_1)$')
    ax.set_ylabel('density')
    ax.set_title('Error of the estimated break date')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch2_sem_primer_bai')


# =============================================================================
# 5. Monitoring: CUSUM of recursive residuals and the boundary
# =============================================================================
def chart_monitoring():
    rng = np.random.default_rng(SEED + 6)
    m, n_end, brk, a2 = 60, 220, 120, 7.78
    y = rng.standard_normal(n_end) + 1.0 * (np.arange(n_end) >= brk)
    w = np.empty(n_end)
    for t in range(1, n_end):                     # recursive residuals of a constant mean
        w[t] = (y[t] - y[:t].mean()) / np.sqrt(1 + 1 / t)
    sig = y[:m].std(ddof=1)
    n = np.arange(m + 1, n_end + 1)
    Q = np.cumsum(w[m:n_end]) / sig
    bound = np.sqrt(n * (a2 + np.log(n / m)))
    hit = np.argmax(np.abs(Q) > bound)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.plot(n, Q, color=B, lw=1.4, label=r'CUSUM $\sum_{t=m+1}^{n} w_t/\hat\sigma$')
    ax.plot(n, bound, color=R, lw=1.2, ls='--', label=r'boundary $\pm\sqrt{n[a^2 + \ln(n/m)]}$, $a^2 = 7.78$')
    ax.plot(n, -bound, color=R, lw=1.2, ls='--', label='_b')
    ax.axvline(brk, color=G, lw=1.0, ls=':', label=f'true break at $t = {brk}$')
    if np.abs(Q[hit]) > bound[hit]:
        ax.plot(n[hit], Q[hit], 'o', color=A, ms=7, label=f'alarm at $n = {n[hit]}$')
    ax.set_xlabel(f'observation $n$ (monitoring starts after $m = {m}$)')
    ax.set_ylabel('cumulated residuals')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch2_sem_primer_monitoring')


# =============================================================================
# 6. A variance break and the Inclán--Tiao statistic
# =============================================================================
def chart_icss():
    rng = np.random.default_rng(SEED + 5)
    T, k0 = 1000, 600
    a = np.r_[rng.normal(0, 1.0, k0), rng.normal(0, 1.8, T - k0)]
    a = a - a.mean()
    C = np.cumsum(a ** 2)
    k = np.arange(1, T + 1)
    Dk = C / C[-1] - k / T
    bound = 1.358 / np.sqrt(T / 2)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
    ax[0].plot(k, a, color=B, lw=0.5, label='$a_t$')
    ax[0].axvline(k0, color=R, lw=1.0, ls='--', label='true break')
    ax[0].set_xlabel('$t$')
    ax[0].set_title('Standard deviation 1, then 1.8')
    ax[1].plot(k, Dk, color=B, lw=1.4, label='$D_k = C_k/C_T - k/T$')
    ax[1].axhline(bound, color=R, lw=1.0, ls='--', label=r'$\pm 1.358/\sqrt{T/2}$')
    ax[1].axhline(-bound, color=R, lw=1.0, ls='--', label='_b')
    ax[1].plot(k[np.argmax(np.abs(Dk))], Dk[np.argmax(np.abs(Dk))], 'o', color=A, ms=6, label=r'$\arg\max_k|D_k|$')
    ax[1].set_xlabel('$k$')
    ax[1].set_title('Centred cumulative sum of squares')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=2)
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch2_sem_primer_icss')


# =============================================================================
# 7. The estimation window after a mean shift: bias against variance
# =============================================================================
def chart_window():
    n2, d, s2 = 30, 0.2, 1.0
    w = np.arange(n2, 301)
    bias2 = ((w - n2) * d / w) ** 2
    var = s2 / w
    tot = var + bias2
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    ax.plot(w, var, color=G, lw=1.4, ls='--', label=r'variance of the mean $\sigma^2/w$')
    ax.plot(w, bias2, color=A, lw=1.4, ls='-.', label=r'squared bias $[(w - n_2)\delta/w]^2$')
    ax.plot(w, tot, color=B, lw=1.8, label=r'MSFE $- \sigma^2$')
    ax.plot(w[tot.argmin()], tot.min(), 'o', color=R, ms=6, label=f'best window, $w = {w[tot.argmin()]}$')
    ax.set_xlabel('window length $w$')
    ax.set_ylabel('contribution to the MSFE')
    ax.set_title(r'$n_2 = 30$, $\delta = 0.2\sigma$, $\sigma = 1$')
    fig.tight_layout()
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch2_sem_primer_window')


# =============================================================================
# 8. A SETAR(2; 1, 1) with two stable equilibria: path and skeleton
# =============================================================================
def chart_setar():
    rng = np.random.default_rng(SEED + 6)
    c1, p1, c2, p2 = -0.5, 0.5, 0.3, 0.6
    T = 300
    y = np.zeros(T)
    for t in range(1, T):
        y[t] = (c1 + p1 * y[t - 1] if y[t - 1] <= 0 else c2 + p2 * y[t - 1]) + 0.45 * rng.standard_normal()
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.7))
    t = np.arange(T)
    ax[0].plot(t, y, color=N, lw=0.6, label='_l')
    ax[0].scatter(t[y <= 0], y[y <= 0], s=5, color=B, label=r'regime 1: $y_t \leq 0$')
    ax[0].scatter(t[y > 0], y[y > 0], s=5, color=R, label=r'regime 2: $y_t > 0$')
    ax[0].axhline(0, color=G, lw=1.0, ls='--', label=r'threshold $\gamma = 0$')
    ax[0].set_xlabel('$t$')
    ax[0].set_title('Simulated SETAR path')
    x = np.linspace(-2.5, 2.5, 400)
    ax[1].plot(x, np.where(x <= 0, c1 + p1 * x, c2 + p2 * x), color=B, lw=1.8, label=r'skeleton $y_t = g(y_{t-1})$')
    ax[1].plot(x, x, color=N, lw=0.8, ls='--', label='45-degree line')
    for e in (c1 / (1 - p1), c2 / (1 - p2)):
        ax[1].plot(e, e, 'o', color=A, ms=6, label='equilibria' if e < 0 else '_e')
    ax[1].set_xlabel('$y_{t-1}$')
    ax[1].set_ylabel('$y_t$')
    ax[1].set_title(r'$-0.5 + 0.5y$ if $y \leq 0$; $0.3 + 0.6y$ if $y > 0$')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=2)
    st.legend_outside_bottom(ax[1], ncol=2)
    save(fig, 'ch2_sem_primer_setar')


# =============================================================================
# 9. Smooth transition functions: logistic and exponential
# =============================================================================
def chart_star():
    s = np.linspace(-3, 3, 500)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    for g, c, ls in ((1, B, '-'), (4, R, '--'), (50, G, '-.')):
        ax[0].plot(s, 1 / (1 + np.exp(-g * s)), color=c, lw=1.5, ls=ls, label=rf'$\gamma = {g}$')
        ax[1].plot(s, 1 - np.exp(-g * s ** 2), color=c, lw=1.5, ls=ls, label=rf'$\gamma = {g}$')
    ax[0].set_title(r'Logistic (LSTAR), $c = 0$')
    ax[1].set_title(r'Exponential (ESTAR), $c = 0$')
    for x in ax:
        x.set_xlabel('transition variable $s_t$')
        x.set_ylabel(r'weight $G(s_t; \gamma, c)$')
    fig.tight_layout()
    st.legend_outside_bottom(ax[0], ncol=3)
    st.legend_outside_bottom(ax[1], ncol=3)
    save(fig, 'ch2_sem_primer_star')


def main():
    st.apply()
    chart_break()
    chart_supwald()
    chart_bp()
    chart_bai()
    chart_monitoring()
    chart_icss()
    chart_window()
    chart_setar()
    chart_star()


if __name__ == '__main__':
    main()
