"""
seminar9_explainers.py -- Explanatory (primer) charts for Seminar 9 (ATS): VaR, ES and backtesting
==================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 9, which takes
place BEFORE Lecture 9. All charts use SIMULATED data or closed forms only (fixed seeds): VaR and ES on a density,
the pinball loss and its expectation, the expected FZ0 loss around the true pair, CAViaR news-impact curves, VaR hits
over time, the Kupiec acceptance region, Weibull hazards of durations, the square-root-of-time ratio under GARCH and
adaptive conformal inference. They contain no exercise answers.

Output: charts/ch9_sem_primer_*.pdf and .png (course style: transparent, legend below the plot, no grey), each sized
for its box on the seminar slides (text at least 6.4 pt there).

Run:  python3 Quantlets/Ch_09/seminar9_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys
from math import gamma

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import ats_style as st                                                       # noqa: E402

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


def unit_t_pdf(x, nu):
    s = np.sqrt((nu - 2) / nu)
    return stats.t.pdf(x / s, nu) / s


# =============================================================================
# (i) VaR and ES on a density
# =============================================================================
def var_es():
    a = 0.025
    x = np.linspace(-5, 4, 800)
    v = stats.norm.ppf(a)
    e = -stats.norm.pdf(v) / a
    nu = 4
    s = np.sqrt((nu - 2) / nu)
    vt = stats.t.ppf(a, nu) * s
    et = -s * stats.t.pdf(stats.t.ppf(a, nu), nu) * (nu + stats.t.ppf(a, nu) ** 2) / ((nu - 1) * a)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(x, stats.norm.pdf(x), color=st.MainBlue, lw=1.8, label='$N(0, 1)$')
    ax.plot(x, unit_t_pdf(x, nu), color=st.IDAred, lw=1.4, ls='--', label='Student-$t_4$, variance 1')
    xx = x[x <= v]
    ax.fill_between(xx, 0, stats.norm.pdf(xx), color=BandBlue, label='tail of $N(0,1)$: probability 2.5%')
    ax.axvline(v, color=st.MainBlue, lw=1.2, ls=':', label=f'$N$: $v = {v:.2f}$, $e = {e:.2f}$')
    ax.axvline(e, color=st.MainBlue, lw=1.2, ls='-.')
    ax.axvline(vt, color=st.IDAred, lw=1.2, ls=':', label=f'$t_4$: $v = {vt:.2f}$, $e = {et:.2f}$')
    ax.axvline(et, color=st.IDAred, lw=1.2, ls='-.')
    ax.set_xlabel('daily return $y$ (standardised)')
    ax.set_ylabel('density')
    ax.set_xlim(-5, 4)
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_var_es', HALF_BOX)
    return v, e, vt, et


# =============================================================================
# (ii) the pinball loss and its expectation
# =============================================================================
def pinball():
    a = 0.05
    u = np.linspace(-3, 3, 400)                       # u = y - x
    xs = np.linspace(-3.5, 0.5, 400)
    rng = np.random.default_rng(1)
    y = rng.standard_normal(200000)
    ql = [np.mean(((y <= x) - a) * (x - y)) for x in xs]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=FULL_FIG)
    a1.plot(u, np.where(u < 0, (1 - a) * (-u), a * u), color=st.MainBlue, lw=1.8, label='$\\rho_{0.05}$ against $y - x$')
    a1.set_xlabel('$y - x$ (negative: a hit)')
    a1.set_ylabel('loss')
    a1.set_title('slopes $1 - \\alpha = 0.95$ and $\\alpha = 0.05$')
    a2.plot(xs, ql, color=st.IDAred, lw=1.8, label='$\\mathrm{E}\\,\\rho_{0.05}(Y, x)$, $Y \\sim N(0, 1)$')
    a2.axvline(stats.norm.ppf(a), color=st.Forest, ls='--', lw=1.2, label=f'minimum at $q_{{0.05}} = {stats.norm.ppf(a):.3f}$')
    a2.set_xlabel('forecast $x$')
    st.fig_legend_bottom(fig, ncol=3)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_pinball', FULL_BOX)


# =============================================================================
# (iii) the expected FZ0 loss is minimised by the true (VaR, ES)
# =============================================================================
def fz0():
    a = 0.025
    v0 = stats.norm.ppf(a)
    e0 = -stats.norm.pdf(v0) / a

    def EL(v, e):                                     # closed form for Y ~ N(0, 1)
        Fv = stats.norm.cdf(v)
        part = v * Fv + stats.norm.pdf(v)            # E[(v - Y) 1{Y <= v}]
        return -part / (a * e) + v / e + np.log(-e) - 1

    vs = np.linspace(-3.0, -1.2, 300)
    es = np.linspace(-3.6, -1.7, 300)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=FULL_FIG)
    a1.plot(vs, [EL(v, e0) for v in vs], color=st.MainBlue, lw=1.8, label='expected FZ0 loss')
    a1.axvline(v0, color=st.Forest, ls='--', lw=1.2, label='true value')
    a1.set_xlabel(f'$v$ (with $e = {e0:.3f}$ fixed)')
    a1.set_ylabel('$\\mathrm{E}\\,L(Y, v, e)$')
    a2.plot(es, [EL(v0, e) for e in es], color=st.MainBlue, lw=1.8)
    a2.axvline(e0, color=st.Forest, ls='--', lw=1.2)
    a2.set_xlabel(f'$e$ (with $v = {v0:.3f}$ fixed)')
    st.fig_legend_bottom(fig, ncol=2)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_fz0', FULL_BOX)


# =============================================================================
# (iv) CAViaR: news-impact curves
# =============================================================================
def caviar():
    y = np.linspace(-5, 5, 400)
    var_prev = 2.0
    sav = 0.20 + 0.80 * var_prev + 0.40 * np.abs(y)
    asym = 0.15 + 0.85 * var_prev + 0.05 * np.maximum(y, 0) + 0.50 * np.maximum(-y, 0)
    ig = np.sqrt(0.10 + 0.85 * var_prev ** 2 + 0.20 * y ** 2)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(y, sav, color=st.MainBlue, lw=1.8, label='SAV: $0.20 + 0.80\\,\\mathrm{VaR}_{t-1} + 0.40\\,|y_{t-1}|$')
    ax.plot(y, asym, color=st.IDAred, lw=1.8, ls='--', label='AS: $0.15 + 0.85\\,\\mathrm{VaR}_{t-1} + 0.05\\,y^+ + 0.50\\,y^-$')
    ax.plot(y, ig, color=st.Forest, lw=1.6, ls='-.', label='IG: $(0.10 + 0.85\\,\\mathrm{VaR}_{t-1}^2 + 0.20\\,y^2)^{1/2}$')
    ax.set_xlabel('yesterday\'s return $y_{t-1}$ (%), with $\\mathrm{VaR}_{t-1} = 2$')
    ax.set_ylabel('$\\mathrm{VaR}_t$ (%)')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_caviar', HALF_BOX)


# =============================================================================
# (v) VaR hits: a correct dynamic VaR against a constant VaR
# =============================================================================
def hits():
    rng = np.random.default_rng(6)
    T, om, al, be = 1500, 0.02, 0.08, 0.90
    s2 = np.empty(T)
    y = np.empty(T)
    s2[0] = om / (1 - al - be)
    for t in range(T):
        if t > 0:
            s2[t] = om + al * y[t - 1] ** 2 + be * s2[t - 1]
        y[t] = np.sqrt(s2[t]) * rng.standard_normal()
    z = stats.norm.ppf(0.01)
    q_dyn = z * np.sqrt(s2)
    q_con = np.full(T, np.quantile(y, 0.01))
    t = np.arange(1, T + 1)
    h_dyn, h_con = y < q_dyn, y < q_con
    fig, ax = plt.subplots(figsize=FULL_FIG)
    ax.plot(t, y, color=st.LightBlue, lw=0.6, label='$y_t$ (simulated GARCH, %)')
    ax.plot(t, q_dyn, color=st.MainBlue, lw=1.1, label=f'GARCH quantile $q_t$: {h_dyn.sum()} hits')
    ax.plot(t, q_con, color=st.IDAred, lw=1.1, ls='--', label=f'constant quantile: {h_con.sum()} hits')
    ax.scatter(t[h_con], y[h_con], s=14, color=st.IDAred, zorder=3, label='hits of the constant quantile')
    ax.set_xlabel('day $t$ (VaR 1%: 15 hits expected in 1 500 days)')
    ax.set_xlim(0, T + 1)
    st.fig_legend_bottom(fig, ncol=2)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_hits', FULL_BOX)
    return h_dyn.sum(), h_con.sum()


# =============================================================================
# (vi) the Kupiec LR statistic against the number of hits
# =============================================================================
def kupiec():
    T, a = 500, 0.01
    N = np.arange(0, 16)
    pi = np.clip(N / T, 1e-12, 1)
    l0 = (T - N) * np.log(1 - a) + N * np.log(a)
    l1 = (T - N) * np.log(1 - pi) + np.where(N > 0, N * np.log(pi), 0)
    lr = -2 * (l0 - l1)
    c = stats.chi2.ppf(0.95, 1)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ok = lr <= c
    ax.bar(N[ok], lr[ok], color=st.Forest, width=0.7, label='not rejected at 5%')
    ax.bar(N[~ok], lr[~ok], color=st.IDAred, width=0.7, label='rejected at 5%')
    ax.axhline(c, color=st.MainBlue, ls='--', lw=1.3, label=f'$\\chi^2_1$ critical value {c:.2f}')
    ax.set_xlabel(f'number of hits $N$ in $T = {T}$ days (expected {T * a:.0f})')
    ax.set_ylabel('$LR_{uc}$')
    ax.set_xticks(np.arange(0, 16, 3))
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_kupiec', HALF_BOX)
    return N[ok].min(), N[ok].max()


# =============================================================================
# (vii) duration hazards: exponential against Weibull
# =============================================================================
def hazards():
    a = 0.01
    d = np.linspace(1, 300, 400)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    for b, c, ls in ((1.0, st.MainBlue, '-'), (0.7, st.IDAred, '--'), (1.4, st.Forest, '-.')):
        lam = gamma(1 + 1 / b) * a                      # mean duration = 1/a for every b
        hz = b * lam ** b * d ** (b - 1)
        txt = {1.0: 'no memory', 0.7: 'clustering', 1.4: 'too regular'}[b]
        ax.plot(d, hz, color=c, ls=ls, lw=1.8, label=f'$b = {b:g}$: {txt}')
    ax.set_xlabel('days since the last hit $d$')
    ax.set_ylabel('hazard $\\lambda(d)$')
    ax.set_title('Weibull hazards, mean gap $1/\\alpha = 100$ days')
    ax.set_ylim(0, 0.04)
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_hazards', HALF_BOX)


# =============================================================================
# (viii) the square-root-of-time rule under GARCH
# =============================================================================
def sqrt_time():
    om, al, be = 0.05, 0.10, 0.85
    sbar = om / (1 - al - be)
    h = np.arange(1, 61)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    for s1, c, lab in ((4 * sbar, st.IDAred, 'start at $4\\bar\\sigma^2$ (crisis)'), (sbar, st.Forest, 'start at $\\bar\\sigma^2$'),
                       (0.4 * sbar, st.MainBlue, 'start at $0.4\\bar\\sigma^2$ (calm)')):
        cum = np.array([sum(sbar + (al + be) ** k * (s1 - sbar) for k in range(H)) for H in h])
        ax.plot(h, np.sqrt(cum / (h * s1)), color=c, lw=1.8, label=lab)
    ax.axhline(1, color=st.Amber, ls='--', lw=1.2, label='$\\sqrt{h}$ rule')
    ax.set_xlabel('horizon $h$ (days)')
    ax.set_ylabel('$h$-day volatility / ($\\sqrt{h}\\,\\sigma_{t+1}$)')
    ax.set_title('$\\omega = 0.05$, $\\alpha = 0.10$, $\\beta = 0.85$')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_sqrt_time', HALF_BOX)


# =============================================================================
# (ix) adaptive conformal inference
# =============================================================================
def aci():
    rng = np.random.default_rng(11)
    T, a, g = 2000, 0.01, 0.001
    s = np.where(np.arange(T) < 1000, 1.15, 0.8)       # volatility falls in the middle; the model keeps sigma = 1
    y = s * rng.standard_normal(T)
    at = np.empty(T + 1)
    at[0] = a
    err = np.zeros(T)
    for t in range(T):
        q = stats.norm.ppf(np.clip(at[t], 1e-6, 1 - 1e-6)) if at[t] > 0 else -np.inf
        err[t] = float(y[t] < q)
        at[t + 1] = at[t] + g * (a - err[t])
    run_fixed = np.cumsum(y < stats.norm.ppf(a)) / np.arange(1, T + 1)
    run_aci = np.cumsum(err) / np.arange(1, T + 1)
    t = np.arange(1, T + 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=FULL_FIG)
    a1.plot(t, at[1:], color=st.MainBlue, lw=1.2, label='$\\alpha_t$ (ACI, $\\gamma = 0.001$)')
    a1.axhline(a, color=st.Forest, ls='--', lw=1.1, label='target $\\alpha = 0.01$')
    a1.axvline(1000, color=st.Amber, ls=':', lw=1.3, label="volatility falls from 1.15 to 0.8")
    a1.set_xlabel('day $t$')
    a2.plot(t, run_fixed, color=st.IDAred, lw=1.4, label='running hit rate, model quantile')
    a2.plot(t, run_aci, color=st.MainBlue, lw=1.4, label='running hit rate, ACI')
    a2.axhline(a, color=st.Forest, ls='--', lw=1.1)
    a2.axvline(1000, color=st.Amber, ls=':', lw=1.3)
    a2.set_xlabel('day $t$')
    a2.set_ylim(0, 0.05)
    st.fig_legend_bottom(fig, ncol=3)
    fig.tight_layout()
    save(fig, 'ch9_sem_primer_aci', FULL_BOX)


if __name__ == '__main__':
    os.makedirs(st.CHART_DIR, exist_ok=True)
    print('   (v, e) Normal and t4:', var_es())
    pinball()
    fz0()
    caviar()
    print('   hits (GARCH, constant):', hits())
    print('   Kupiec acceptance region:', kupiec())
    hazards()
    sqrt_time()
    aci()
