"""
seminar15_explainers.py -- Explanatory (primer) charts for Seminar 15 (ATS): review and project defence
=====================================================================================================
Teaching charts for the slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 15, which takes place
BEFORE Lecture 15. All charts use SIMULATED data or closed-form formulas (fixed seeds): the long-run variance of an
AR(1) and the Bartlett weights, the power of a DM test, Cholesky impulse responses of a VAR(1), the half-life of an
equilibrium error, the Kalman filter of a local level, a two-state Markov chain, the decay of a GARCH volatility
shock, the binomial law of VaR exceedances with the Basel zones, and the maximum of many t-statistics.
No exercise answers.

Output: charts/ch15_sem_primer_*.pdf/.png (EN) and charts/ch15_sem_primer_*_ro.pdf/.png (RO), transparent
background, legend outside at the bottom, each chart sized for its box on the slides (text >= 6.3 pt there);
the numbers quoted on the slides go to Quantlets/Ch_15/sem15_primer.json.

Run:  python3 Quantlets/Ch_15/seminar15_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
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
st.SLIDE_MIN_PT = 6.5            # every chart text at least 6.3 pt on the slide
st.SLIDE_BASE_PT = 6.9
CHART_DIR = os.path.join(HERE, '..', '..', 'charts')
OUT = {}

TW, TH = 409.72 / 72, 214.79 / 72          # \textwidth, \textheight of the decks (inches)
HALF = (round(0.50 * TW, 3), round(0.80 * TH, 3))     # chart column of a two-column primer frame
FULL = (round(TW, 3), round(0.50 * TH, 3))            # full-width chart above the bullets
LANG = 'en'


def L(en, ro):
    return en if LANG == 'en' else ro


def dec(x):
    """A number for a math label: decimal comma in RO."""
    s = f'{x:g}'
    return s if LANG == 'en' else s.replace('.', '{,}')


def save(fig, name, box=HALF):
    nm = name + ('' if LANG == 'en' else '_ro')
    st.check_no_grey(fig)
    st.fit_for_slide(fig, nm, box=box)
    os.makedirs(CHART_DIR, exist_ok=True)
    fig.savefig(os.path.join(CHART_DIR, nm + '.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(CHART_DIR, nm + '.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print('   saved', nm)


def leg(ax, ncol=2):
    st.legend_outside_bottom(ax, ncol=ncol)


# =============================================================================
# (1) the long-run variance of an AR(1) and the Bartlett weights
# =============================================================================
def lrv():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    phi = np.linspace(-0.5, 0.9, 300)
    a1.plot(phi, np.sqrt((1 + phi) / (1 - phi)), color=st.MainBlue, lw=2, label=L(r'AR(1): $\sqrt{(1 + \phi)/(1 - \phi)}$', r'AR(1): $\sqrt{(1 + \phi)/(1 - \phi)}$'))
    a1.axhline(1, color=st.Amber, ls='--', lw=1.2, label=L('i.i.d. value 1', 'valoarea i.i.d. 1'))
    a1.set_xlabel(r'$\phi$')
    a1.set_ylabel(r'$\sqrt{\Omega/\gamma_0}$')
    leg(a1, 2)
    j = np.arange(0, 13)
    for Lg, c in ((2, st.IDAred), (5, st.Forest), (10, st.MainBlue)):
        w = np.where(j <= Lg, 1 - j / (Lg + 1), 0)
        a2.plot(j, w, color=c, lw=2, marker='o', ms=3.5, label=rf'$L = {Lg}$')
    a2.set_xlabel(L(r'lag $j$', r'lagul $j$'))
    a2.set_xticks(range(0, 13, 2))
    a2.set_ylabel(L(r'weight $1 - j/(L + 1)$', r'ponderea $1 - j/(L + 1)$'))
    leg(a2, 3)
    OUT['lrv'] = dict(f03=float(np.sqrt(1.3 / 0.7)), f09=float(np.sqrt(1.9 / 0.1)), L250=int(np.floor(4 * (250 / 100) ** (2 / 9))),
                      L1000=int(np.floor(4 * (1000 / 100) ** (2 / 9))))
    save(fig, 'ch15_sem_primer_lrv', FULL)


# =============================================================================
# (2) the power of a two-sided 5% DM test
# =============================================================================
def dm_power():
    z = stats.norm()
    d = np.linspace(0, 0.5, 300)
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    out = {}
    for P_, c in ((60, st.IDAred), (128, st.Forest), (250, st.MainBlue)):
        pw = z.cdf(d * np.sqrt(P_) - 1.96) + z.cdf(-d * np.sqrt(P_) - 1.96)
        ax.plot(d, pw, color=c, lw=2, label=rf'$P = {P_}$')
        out[str(P_)] = float(z.cdf(0.2 * np.sqrt(P_) - 1.96) + z.cdf(-0.2 * np.sqrt(P_) - 1.96))
    ax.axhline(0.8, color=st.Amber, ls='--', lw=1.2, label=L('power 0.80', 'puterea 0,80'))
    ax.axhline(0.05, color=st.DarkText, ls=':', lw=1.0, label=L('level 0.05', 'nivelul 0,05'))
    ax.set_xlabel(L(r'mean gain $\delta$ (in s.d. of $d_t$)', r'cîștigul mediu $\delta$ (în abateri standard ale lui $d_t$)'))
    ax.set_ylabel(L('power', 'puterea'))
    leg(ax, 3)
    OUT['pow'] = out
    save(fig, 'ch15_sem_primer_dm_power')


# =============================================================================
# (3) Cholesky impulse responses of a VAR(1)
# =============================================================================
def irf():
    A = np.array([[0.7, 0.1], [0.3, 0.5]])
    S = np.array([[1.0, 0.6], [0.6, 2.0]])
    B0 = np.linalg.cholesky(S)
    H = 12
    Th = [np.linalg.matrix_power(A, h) @ B0 for h in range(H + 1)]
    h = np.arange(H + 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for k, ax, ttl in ((0, a1, L(r'shock $\varepsilon_1$', r'șocul $\varepsilon_1$')), (1, a2, L(r'shock $\varepsilon_2$', r'șocul $\varepsilon_2$'))):
        ax.plot(h, [T_[0, k] for T_ in Th], color=st.MainBlue, lw=2, marker='o', ms=3, label=L(r'response of $y_1$', r'răspunsul lui $y_1$'))
        ax.plot(h, [T_[1, k] for T_ in Th], color=st.IDAred, lw=2, marker='o', ms=3, label=L(r'response of $y_2$', r'răspunsul lui $y_2$'))
        ax.axhline(0, color=st.DarkText, lw=0.6)
        ax.set_title(ttl)
        ax.set_xlabel(L(r'horizon $h$', r'orizontul $h$'))
        ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
        leg(ax, 2)
    OUT['irf'] = dict(b11=float(B0[0, 0]), b21=float(B0[1, 0]), b22=float(B0[1, 1]), r12_0=float(B0[0, 1]))
    save(fig, 'ch15_sem_primer_irf', FULL)


# =============================================================================
# (4) the half-life of an equilibrium error
# =============================================================================
def halflife():
    h = np.arange(0, 31)
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    out = {}
    for c_, col in ((0.5, st.IDAred), (0.8, st.Forest), (0.95, st.MainBlue)):
        hl = np.log(0.5) / np.log(c_)
        ax.plot(h, c_ ** h, color=col, lw=2, label=rf'$c = {dec(c_)}$, ' + L('half-life', 'timp de înjumătățire') + f' {hl:.1f}'.replace('.', '.' if LANG == 'en' else ','))
        out[str(c_)] = float(hl)
    ax.axhline(0.5, color=st.Amber, ls='--', lw=1.2)
    ax.set_xlabel(L(r'periods after a unit deviation, $h$', r'perioade după o abatere unitară, $h$'))
    ax.set_ylabel(r'$E(z_{t+h}\mid z_t = 1) = c^h$')
    leg(ax, 1)
    OUT['hl'] = out
    save(fig, 'ch15_sem_primer_halflife')


# =============================================================================
# (5) the Kalman filter of a local level and the convergence of the gain
# =============================================================================
def kalman():
    rng = np.random.default_rng(15)
    T_, se2, sh2 = 120, 1.0, 0.1
    mu = np.cumsum(rng.normal(0, np.sqrt(sh2), T_))
    y = mu + rng.normal(0, np.sqrt(se2), T_)
    a, P = 0.0, 10.0
    filt = np.zeros(T_)
    for t in range(T_):
        F = P + se2
        K = P / F
        a, P = a + K * (y[t] - a), P * (1 - K)
        filt[t] = a
        P = P + sh2
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(y, '.', color=st.MainBlue, ms=3.5, label='$y_t$')
    a1.plot(mu, color=st.Forest, lw=1.6, label=L(r'level $\mu_t$', r'nivelul $\mu_t$'))
    a1.plot(filt, color=st.IDAred, lw=1.8, label=L(r'filtered $a_{t|t}$', r'filtrat $a_{t|t}$'))
    a1.set_xlabel(L('time $t$', 'timpul $t$'))
    leg(a1, 3)
    out = {}
    for q, col in ((0.01, st.MainBlue), (0.1, st.Forest), (1.0, st.IDAred)):
        P, Ks = 10.0, []
        for t in range(25):
            K = P / (P + 1.0)
            Ks.append(K)
            P = P * (1 - K) + q
        Pb = (q + np.sqrt(q * q + 4 * q)) / 2
        a2.plot(np.arange(1, 26), Ks, color=col, lw=2, label=rf'$q = {dec(q)}$')
        a2.axhline(Pb / (Pb + 1), color=col, ls=':', lw=1.2)
        out[str(q)] = float(Pb / (Pb + 1))
    a2.set_xlabel(L('step $t$', 'pasul $t$'))
    a2.set_ylabel(L(r'gain $K_t$', r'cîștigul $K_t$'))
    leg(a2, 3)
    OUT['kf'] = out
    save(fig, 'ch15_sem_primer_kalman', FULL)


# =============================================================================
# (6) a two-state Markov chain
# =============================================================================
def markov():
    rng = np.random.default_rng(6)
    p11, p22, T_ = 0.97, 0.90, 300
    s = np.zeros(T_, int)
    for t in range(1, T_):
        stay = p11 if s[t - 1] == 0 else p22
        s[t] = s[t - 1] if rng.random() < stay else 1 - s[t - 1]
    y = np.where(s == 0, rng.normal(0.5, 0.6, T_), rng.normal(-1.0, 1.6, T_))
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.plot(y, color=st.MainBlue, lw=1.0, label='$y_t$')
    lo, hi = y.min() - 0.3, y.max() + 0.3
    ax.fill_between(np.arange(T_), lo, hi, where=s == 1, color=st.IDAred, alpha=0.30, step='mid', label=L('regime 2', 'regimul 2'))
    ax.set_ylim(lo, hi)
    ax.set_xlabel(L('period $t$', 'perioada $t$'))
    leg(ax, 2)
    OUT['mk'] = dict(p11=p11, p22=p22, d1=1 / (1 - p11), d2=1 / (1 - p22), pi1=(1 - p22) / (2 - p11 - p22),
                     share1=float(np.mean(s == 0)), lam=p11 + p22 - 1)
    save(fig, 'ch15_sem_primer_markov')


# =============================================================================
# (7) the decay of a volatility shock in a GARCH(1,1)
# =============================================================================
def garch_hl():
    h = np.arange(0, 121)
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    out = {}
    for p_, col in ((0.90, st.IDAred), (0.95, st.Forest), (0.99, st.MainBlue)):
        hl = np.log(0.5) / np.log(p_)
        ax.plot(h, p_ ** h, color=col, lw=2, label=rf'$\alpha + \beta = {dec(p_)}$')
        out[str(p_)] = float(hl)
    ax.axhline(0.5, color=st.Amber, ls='--', lw=1.2, label=L('half of the shock', 'jumătate din șoc'))
    ax.set_xlabel(L(r'days after the shock, $h$', r'zile după șoc, $h$'))
    ax.set_ylabel(r'$(\alpha + \beta)^h$')
    leg(ax, 2)
    OUT['gh'] = out
    save(fig, 'ch15_sem_primer_garch_hl')


# =============================================================================
# (8) the binomial law of VaR 1% exceedances in 250 days and the Basel zones
# =============================================================================
def kupiec_binom():
    T_, a = 250, 0.01
    x = np.arange(0, 13)
    pmf = stats.binom.pmf(x, T_, a)
    col = [st.Forest if k <= 4 else st.Amber if k <= 9 else st.IDAred for k in x]
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.bar(x, pmf, color=col, width=0.7)
    from matplotlib.patches import Patch
    hs = [Patch(color=st.Forest, label=L('green: 0--4', 'verde: 0--4').replace('--', '–')),
          Patch(color=st.Amber, label=L('yellow: 5--9', 'galben: 5--9').replace('--', '–')),
          Patch(color=st.IDAred, label=L('red: 10 or more', 'roșu: 10 sau mai multe'))]
    ax.legend(handles=hs, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=False)
    ax.set_xlabel(L(r'number of exceedances $x$ in $T = 250$ days', r'numărul de depășiri $x$ în $T = 250$ de zile'))
    ax.set_ylabel(r'$\Pr(X = x)$')
    ax.set_xticks(x)
    OUT['bin'] = dict(green=float(stats.binom.cdf(4, T_, a)), yellow=float(stats.binom.cdf(9, T_, a) - stats.binom.cdf(4, T_, a)),
                      red=float(stats.binom.sf(9, T_, a)), ge5=float(stats.binom.sf(4, T_, a)))
    save(fig, 'ch15_sem_primer_binom')


# =============================================================================
# (9) the maximum of many t-statistics
# =============================================================================
def maxt():
    rng = np.random.default_rng(20)
    m, R_ = 20, 20000
    out = {}
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    g = np.linspace(-3, 5, 400)
    ax.plot(g, stats.norm.pdf(g), color=st.DarkText, lw=1.6, ls='--', label=L(r'one $t$, $N(0, 1)$', r'un singur $t$, $N(0, 1)$'))
    for r_, col in ((0.0, st.IDAred), (0.5, st.MainBlue)):
        C = np.full((m, m), r_) + (1 - r_) * np.eye(m)
        Z = rng.multivariate_normal(np.zeros(m), C, R_)
        mx = Z.max(axis=1)
        ax.hist(mx, bins=60, density=True, histtype='step', lw=2, color=col,
                label=L(rf'max of 20, correlation {r_:g}', rf'maximul a 20, corelația {dec(r_)}'.replace('{,}', ',')))
        out[str(r_)] = float(np.quantile(mx, 0.95))
    ax.axvline(1.645, color=st.Amber, lw=1.2, label=L('1.645 (one test, 5%)', '1,645 (un test, 5%)'))
    ax.set_xlabel(L('statistic under $H_0$', 'statistica sub $H_0$'))
    ax.set_ylabel(L('density', 'densitatea'))
    leg(ax, 2)
    out['naive'] = float(1 - (0.95) ** m)
    OUT['maxt'] = out
    save(fig, 'ch15_sem_primer_maxt')


if __name__ == '__main__':
    for LANG in ('en', 'ro'):
        lrv(); dm_power(); irf(); halflife(); kalman(); markov(); garch_hl(); kupiec_binom(); maxt()
    with open(os.path.join(HERE, 'sem15_primer.json'), 'w') as fh:
        json.dump(OUT, fh, indent=1)
    print('numbers -> sem15_primer.json')
