"""
seminar8_explainers.py -- Explanatory (primer) charts for Seminar 8 (ATS): advanced volatility modelling
========================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 8, which takes
place BEFORE Lecture 8. All charts use SIMULATED data only (fixed seeds): they illustrate the concepts (a GARCH(1,1)
path, the QML standard errors with fat-tailed shocks, GARCH-MIDAS components, the noise bias of realised variance,
kernel weights, a jump inside a day and the jump statistic, the HAR lag structure, the attenuation of the OLS slope,
the QLIKE and MSE losses, a DCC correlation path) and contain no exercise answers.

Output: charts/ch8_sem_primer_*.pdf and .png (course style: transparent, legend below the plot, no grey), each sized
for its box on the seminar slides (text at least 6.4 pt there).

Run:  python3 Quantlets/Ch_08/seminar8_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
from math import lgamma
import sys

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


def garch_sim(T, om, a, b, rng, shocks=None):
    z = rng.standard_normal(T) if shocks is None else shocks
    s2 = np.empty(T)
    e = np.empty(T)
    s2[0] = om / (1 - a - b)
    for t in range(T):
        if t > 0:
            s2[t] = om + a * e[t - 1] ** 2 + b * s2[t - 1]
        e[t] = np.sqrt(s2[t]) * z[t]
    return e, s2


def unit_t(nu, size, rng):
    return rng.standard_t(nu, size) * np.sqrt((nu - 2) / nu)


# =============================================================================
# (i) GARCH(1,1): returns and conditional volatility
# =============================================================================
def garch_path():
    rng = np.random.default_rng(8)
    e, s2 = garch_sim(1500, 0.05, 0.08, 0.90, rng)
    t = np.arange(1, len(e) + 1)
    fig, ax = plt.subplots(figsize=FULL_FIG)
    ax.plot(t, e, color=st.LightBlue, lw=0.6, label='$\\varepsilon_t$ (simulated return, %)')
    ax.plot(t, 2 * np.sqrt(s2), color=st.IDAred, lw=1.2, label='$\\pm 2\\sigma_t$')
    ax.plot(t, -2 * np.sqrt(s2), color=st.IDAred, lw=1.2)
    ax.axhline(2 * np.sqrt(0.05 / 0.02), color=st.Forest, ls='--', lw=1.1,
               label='$\\pm 2\\sqrt{\\omega/(1-\\alpha-\\beta)}$ (long-run level)')
    ax.axhline(-2 * np.sqrt(0.05 / 0.02), color=st.Forest, ls='--', lw=1.1)
    ax.set_xlabel('day $t$')
    ax.set_xlim(0, len(e) + 1)
    st.fig_legend_bottom(fig, ncol=3)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_garch_path', FULL_BOX)


# =============================================================================
# (ii) QML with fat tails: the sampling distribution of the variance estimator
# =============================================================================
def qml_tails(R=4000, T=500):
    rng = np.random.default_rng(12)
    s2_n = (rng.standard_normal((R, T)) ** 2).mean(1)
    s2_t = (unit_t(5, (R, T), rng) ** 2).mean(1)
    x = np.linspace(0.6, 1.5, 400)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.hist(s2_t, bins=50, range=(0.6, 1.6), density=True, color=BandBlue, edgecolor=st.MainBlue, lw=0.4,
            label='$\\hat\\sigma^2$ with Student-$t_5$ shocks (simulated)')
    ax.plot(x, stats.norm.pdf(x, 1, np.sqrt(2 / T)), color=st.IDAred, lw=1.6,
            label='Hessian-only approximation $N(1, 2/T)$')
    ax.plot(x, stats.norm.pdf(x, 1, np.sqrt(8 / T)), color=st.MainBlue, lw=1.6, ls='--',
            label='sandwich: $N(1, (\\kappa_\\eta - 1)/T)$, $\\kappa_\\eta = 9$')
    ax.set_xlim(0.6, 1.6)
    ax.set_xlabel('$\\hat\\sigma^2$ (true value 1, $T = 500$)')
    ax.set_ylabel('density')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_qml_tails', HALF_BOX)
    return s2_n.std(), s2_t.std()


# =============================================================================
# (iii) GARCH-MIDAS: monthly long-run level times a daily GARCH factor
# =============================================================================
def midas():
    rng = np.random.default_rng(21)
    months, days = 60, 21
    X = np.zeros(months + 12)
    for m in range(1, len(X)):
        X[m] = 0.8 * X[m - 1] + rng.normal(0, 0.5)
    K, w = 12, 3.0
    k = np.arange(1, K + 1)
    phi = (1 - k / (K + 1)) ** (w - 1)
    phi /= phi.sum()
    tau = np.exp(0.0 + 0.6 * np.array([phi @ X[m + 12 - k] for m in range(months)]))
    T = months * days
    tau_d = np.repeat(tau, days)
    a, b = 0.07, 0.90
    g = np.ones(T)
    e = np.zeros(T)
    z = rng.standard_normal(T)
    for t in range(T):
        if t > 0:
            g[t] = (1 - a - b) + a * e[t - 1] ** 2 / tau_d[t - 1] + b * g[t - 1]
        e[t] = np.sqrt(tau_d[t] * g[t]) * z[t]
    t = np.arange(1, T + 1)
    fig, ax = plt.subplots(figsize=FULL_FIG)
    ax.plot(t, np.sqrt(tau_d * g), color=st.MainBlue, lw=0.8, label='total volatility $\\sqrt{\\tau_t g_{i,t}}$')
    ax.plot(t, np.sqrt(tau_d), color=st.IDAred, lw=2.0, label='long-run component $\\sqrt{\\tau_t}$ (constant within a month)')
    ax.set_xlabel('trading day (60 months of 21 days)')
    ax.set_ylabel('volatility')
    ax.set_xlim(0, T + 1)
    st.fig_legend_bottom(fig, ncol=2)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_midas', FULL_BOX)


# =============================================================================
# (iv) the noise bias and variance of RV: expected RV and MSE against the sampling interval
# =============================================================================
def signature():
    IV = IQ = 1.0
    om2 = 2e-5
    secs = np.geomspace(1, 1800, 300)
    n = 23400 / secs
    bias = 2 * n * om2
    mse = 2 * IQ / n + bias ** 2
    ns = (IQ / (4 * om2 ** 2)) ** (1 / 3)
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(secs, IV + bias, color=st.MainBlue, lw=1.8, label='$\\mathrm{E}\\,\\mathrm{RV} = \\mathrm{IV} + 2n\\omega^2$')
    ax.plot(secs, mse, color=st.IDAred, lw=1.6, label='MSE $= 2\\,\\mathrm{IQ}/n + (2n\\omega^2)^2$')
    ax.axhline(IV, color=st.Forest, ls='--', lw=1.1, label='IV = 1')
    ax.axvline(23400 / ns, color=st.Amber, ls=':', lw=1.6, label=f'optimum: one return every {23400 / ns:.0f} s')
    ax.set_xscale('log')
    ax.set_xlabel('sampling interval (seconds, log scale)')
    ax.set_ylim(0, 2.0)
    ax.set_title('$\\omega^2 = 2\\times10^{-5}$, IV = IQ = 1, 6.5-hour day')
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_signature', HALF_BOX)


# =============================================================================
# (v) kernel weight functions
# =============================================================================
def kernels():
    x = np.linspace(0, 1, 400)
    parzen = np.where(x <= 0.5, 1 - 6 * x ** 2 + 6 * x ** 3, 2 * (1 - x) ** 3)
    bartlett = 1 - x
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(x, parzen, color=st.MainBlue, lw=2.0, label='Parzen $k(x)$')
    ax.plot(x, bartlett, color=st.IDAred, lw=1.4, ls='--', label='Bartlett $k(x) = 1 - x$ (Newey--West)')
    ax.set_xlabel('$x = h/(H+1)$')
    ax.set_ylabel('weight $k(x)$')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_kernels', HALF_BOX)


# =============================================================================
# (vi) a jump inside a day; RV against BV and the jump statistic under the null
# =============================================================================
def jumps(days=3000, n=78):
    rng = np.random.default_rng(30)
    mu1 = np.sqrt(2 / np.pi)                                        # E|Z|
    mu43 = 2 ** (2 / 3) * np.exp(lgamma(7 / 6)) / np.sqrt(np.pi)    # E|Z|^{4/3}
    theta = np.pi ** 2 / 4 + np.pi - 5
    r = rng.standard_normal((days, n)) / np.sqrt(n)
    a = np.abs(r)
    rv = (r ** 2).sum(1)
    bv = mu1 ** -2 * n / (n - 1) * (a[:, 1:] * a[:, :-1]).sum(1)
    tq = n * mu43 ** -3 * n / (n - 2) * (a[:, 2:] * a[:, 1:-1] * a[:, :-2]) ** (4 / 3)
    tq = tq.sum(1)
    z = ((rv - bv) / rv) / np.sqrt(theta / n * np.maximum(1, tq / bv ** 2))
    # one day with a jump
    day = rng.standard_normal(n) / np.sqrt(n)
    day[50] += 0.8
    p = np.r_[0, np.cumsum(day)]
    ad = np.abs(day)
    rv1 = (day ** 2).sum()
    bv1 = mu1 ** -2 * n / (n - 1) * (ad[1:] * ad[:-1]).sum()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=FULL_FIG)
    a1.plot(np.arange(n + 1) * 5 / 60, p, color=st.MainBlue, lw=1.3, label='log price (%), one jump of 0.8')
    a1.set_xlabel('hour of the trading day')
    a1.set_title(f'RV = {rv1:.2f}, BV = {bv1:.2f}')
    x = np.linspace(-4, 5, 300)
    a2.hist(z, bins=60, density=True, color=BandBlue, edgecolor=st.MainBlue, lw=0.4,
            label=f'$z$ on {days} simulated days without jumps')
    a2.plot(x, stats.norm.pdf(x), color=st.IDAred, lw=1.6, label='$N(0, 1)$')
    a2.axvline(stats.norm.ppf(0.999), color=st.Forest, ls='--', lw=1.3, label='$z_{0.999} = 3.09$')
    a2.set_xlabel('jump statistic $z$ ($n = 78$)')
    st.fig_legend_bottom(fig, ncol=4)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_jumps', FULL_BOX)


# =============================================================================
# (vii) HAR: the implied AR(22) coefficients and the slow decay of the ACF
# =============================================================================
def har():
    bd, bw, bm = 0.40, 0.35, 0.15
    j = np.arange(1, 23)
    phi = bm / 22 + np.where(j <= 5, bw / 5, 0) + np.where(j == 1, bd, 0)
    rng = np.random.default_rng(4)
    T = 20000
    rv = np.ones(T + 22)
    for t in range(22, T + 22):
        rv[t] = 0.1 + phi @ rv[t - j] + 0.3 * rng.standard_normal()
    x = rv[22:] - rv[22:].mean()
    acf = np.array([x[k:] @ x[:len(x) - k] for k in range(1, 61)]) / (x @ x)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=FULL_FIG)
    a1.bar(j, phi, color=st.MainBlue, width=0.7, label='$\\phi_j$ on $\\mathrm{RV}_{t+1-j}$')
    a1.set_xlabel('lag $j$ (days)')
    a1.set_title('$\\beta_d = 0.40$, $\\beta_w = 0.35$, $\\beta_m = 0.15$')
    a2.plot(np.arange(1, 61), acf, color=st.IDAred, lw=1.6, label='ACF of simulated HAR')
    a2.plot(np.arange(1, 61), acf[0] ** np.arange(1, 61), color=st.Forest, ls='--', lw=1.3,
            label='AR(1) with the same lag-1 autocorrelation')
    a2.set_xlabel('lag $k$ (days)')
    a2.set_ylim(0, 1)
    st.fig_legend_bottom(fig, ncol=3)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_har', FULL_BOX)


# =============================================================================
# (viii) errors in variables: the OLS slope is attenuated
# =============================================================================
def attenuation():
    rng = np.random.default_rng(9)
    T, phi = 1500, 0.9
    iv = np.empty(T)
    iv[0] = 0
    for t in range(1, T):
        iv[t] = phi * iv[t - 1] + rng.normal(0, np.sqrt(1 - phi ** 2))
    rv = iv + rng.normal(0, 1.0, T)
    b_iv = np.polyfit(iv[:-1], iv[1:], 1)[0]
    b_rv = np.polyfit(rv[:-1], rv[1:], 1)[0]
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.scatter(rv[:-1], rv[1:], s=4, color=st.LightBlue, label='$(\\mathrm{RV}_t, \\mathrm{RV}_{t+1})$, simulated')
    xx = np.array([-4, 4])
    ax.plot(xx, phi * xx, color=st.Forest, lw=1.8, label=f'true slope $\\phi = {phi}$')
    ax.plot(xx, b_rv * xx, color=st.IDAred, lw=1.8, ls='--',
            label=f'OLS slope on RV: {b_rv:.2f} $\\approx \\phi\\lambda$, $\\lambda = 0.5$')
    ax.set_xlabel('$\\mathrm{RV}_t$')
    ax.set_ylabel('$\\mathrm{RV}_{t+1}$')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_attenuation', HALF_BOX)
    return b_iv, b_rv


# =============================================================================
# (ix) QLIKE and MSE as functions of the forecast
# =============================================================================
def losses():
    h = np.linspace(0.2, 3, 400)
    s = 1.0
    fig, ax = plt.subplots(figsize=HALF_FIG)
    ax.plot(h, s / h - np.log(s / h) - 1, color=st.MainBlue, lw=2.0, label='QLIKE $= \\hat\\sigma^2/h - \\ln(\\hat\\sigma^2/h) - 1$')
    ax.plot(h, (s - h) ** 2, color=st.IDAred, lw=1.6, ls='--', label='MSE $= (\\hat\\sigma^2 - h)^2$')
    ax.axvline(1, color=st.Forest, ls=':', lw=1.3, label='$h = \\hat\\sigma^2 = 1$')
    ax.set_xlabel('forecast $h$')
    ax.set_ylabel('loss')
    ax.set_ylim(0, 2)
    st.legend_outside_bottom(ax, ncol=1, y=-0.25)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_losses', HALF_BOX)


# =============================================================================
# (x) DCC: a simulated conditional correlation path
# =============================================================================
def dcc():
    rng = np.random.default_rng(14)
    T, a, b, rho_bar = 1500, 0.05, 0.93, 0.4
    S = np.array([[1, rho_bar], [rho_bar, 1]])
    Q = S.copy()
    rho = np.empty(T)
    z = np.zeros(2)
    for t in range(T):
        if t > 0:
            Q = (1 - a - b) * S + a * np.outer(z, z) + b * Q
        d = np.sqrt(np.diag(Q))
        R = Q / np.outer(d, d)
        rho[t] = R[0, 1]
        z = np.linalg.cholesky(R) @ rng.standard_normal(2)
    fig, ax = plt.subplots(figsize=FULL_FIG)
    ax.plot(np.arange(1, T + 1), rho, color=st.MainBlue, lw=1.0, label='$\\rho_{12,t}$ (simulated DCC)')
    ax.axhline(rho_bar, color=st.IDAred, ls='--', lw=1.2, label='target: $S_{12} = 0.4$')
    ax.set_xlabel('day $t$')
    ax.set_ylabel('correlation')
    ax.set_xlim(0, T + 1)
    ax.set_title('$a = 0.05$, $b = 0.93$')
    st.fig_legend_bottom(fig, ncol=2)
    fig.tight_layout()
    save(fig, 'ch8_sem_primer_dcc', FULL_BOX)


if __name__ == '__main__':
    os.makedirs(st.CHART_DIR, exist_ok=True)
    garch_path()
    print('   QML s.d. (Normal, t5):', qml_tails())
    midas()
    signature()
    kernels()
    jumps()
    har()
    print('   attenuation slopes (IV, RV):', attenuation())
    losses()
    dcc()
