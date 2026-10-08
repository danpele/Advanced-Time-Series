"""
seminar13_explainers.py -- Explanatory (primer) charts for Seminar 13 (ATS): foundation models and conformal prediction
======================================================================================================================
Teaching charts for the slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 13, which takes place
BEFORE Lecture 13. All charts use SIMULATED data only (fixed seeds): they illustrate the concepts (mean scaling and
the range of the Chronos tokeniser, the pinball loss, Holm and Benjamini-Hochberg, split conformal and its Beta law,
exchangeability, CQR and weighted conformal, ACI under volatility clustering, the Kupiec and Christoffersen tests,
a one-sided conformal shift of a VaR quantile) and contain no exercise answers.

Output: charts/ch13_sem_primer_*.pdf/.png (EN) and charts/ch13_sem_primer_*_ro.pdf/.png (RO), transparent
background, legend outside at the bottom, each chart sized for its box on the slides (text >= 6.3 pt there);
the numbers quoted on the slides go to Quantlets/Ch_13/sem13_primer.json.

Run:  python3 Quantlets/Ch_13/seminar13_explainers.py

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


def num(x, d=2):
    s = f'{x:.{d}f}'
    return s if LANG == 'en' else s.replace('.', '{,}')          # used inside math mode


def save(fig, name, box=HALF):
    """Fit the figure to its box on the slides and save PDF + PNG (EN name, or name_ro)."""
    nm = name + ('' if LANG == 'en' else '_ro')
    out = CHART_DIR
    st.check_no_grey(fig)
    st.fit_for_slide(fig, nm, box=box)
    os.makedirs(out, exist_ok=True)
    fig.savefig(os.path.join(out, nm + '.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(out, nm + '.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print('   saved', nm)


def legend(fig, ax=None, ncol=2):
    if ax is not None:
        st.legend_outside_bottom(ax, ncol=ncol)
    else:
        st.fig_legend_bottom(fig, ncol=ncol)


# =============================================================================
# (1) Chronos tokeniser: the range limit and arcsinh scaling
# =============================================================================
def tokens():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    x = np.linspace(0, 40, 400)
    a1.plot(x, np.minimum(x, 15), color=st.MainBlue, lw=2, label=L('uniform bins on [-15, 15]', 'intervale uniforme pe [-15, 15]'))
    a1.plot(x, np.arcsinh(x), color=st.IDAred, lw=2, label=r'$\mathrm{arcsinh}(x)$')
    a1.plot(x[x > 1], np.log(2 * x[x > 1]), color=st.Forest, ls='--', lw=1.4, label=r'$\ln(2x)$')
    a1.set_xlabel(L(r'scaled value $x = y/s$', r'valoarea scalată $x = y/s$'))
    a1.set_ylabel(L('represented value', 'valoarea reprezentată'))
    legend(fig, a1, ncol=3)
    rng = np.random.default_rng(13)
    T_ = 120
    y = np.where(rng.random(T_) < 0.15, rng.gamma(2.0, 1.0, T_), 0.0)
    y[95] = 14.0                                        # a rare large order (intermittent demand)
    s = np.mean(np.abs(y))
    a2.vlines(np.arange(T_), 0, y, color=st.MainBlue, lw=1.4, label=L('series $y_t$', 'seria $y_t$'))
    a2.axhline(15 * s, color=st.IDAred, ls='--', lw=1.4, label=L(r'limit $15s$', r'limita $15s$'))
    a2.axhline(s, color=st.Amber, ls=':', lw=1.4, label=L(r'scale $s$', r'scala $s$'))
    a2.set_xlabel(L('time $t$', 'timpul $t$'))
    a2.set_ylabel('$y_t$')
    legend(fig, a2, ncol=3)
    OUT['tok'] = dict(s=float(s), lim=float(15 * s), peak=float(y[95]), ratio=float(y[95] / s))
    save(fig, 'ch13_sem_primer_tokens', FULL)


# =============================================================================
# (2) the pinball loss and its minimiser
# =============================================================================
def pinball():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    u = np.linspace(-3, 3, 301)
    for tau, c in ((0.1, st.MainBlue), (0.5, st.Forest), (0.9, st.IDAred)):
        a1.plot(u, u * (tau - (u < 0)), color=c, lw=2, label=rf'$\tau = {num(tau, 1)}$')
    a1.set_xlabel(L(r'error $u = y - \hat q_\tau$', r'eroarea $u = y - \hat q_\tau$'))
    a1.set_ylabel(r'$\rho_\tau(u)$')
    legend(fig, a1, ncol=3)
    q = np.linspace(-2.5, 3.5, 301)
    tau = 0.9
    z = stats.norm()
    # E rho_tau(Y - q) for Y ~ N(0, 1): (tau - 1)(q - ... ) closed form via E(Y - q)^+ = phi(q) - q(1 - Phi(q))
    ep = z.pdf(q) - q * (1 - z.cdf(q))
    el = ep - (0 - q)                                   # E(Y - q)^- = E(Y - q)^+ - E(Y - q)
    loss = tau * ep + (1 - tau) * el
    qs = z.ppf(tau)
    a2.plot(q, loss, color=st.IDAred, lw=2, label=L(r'expected loss, $Y \sim N(0, 1)$, $\tau = 0.9$',
                                                      r'pierderea așteptată, $Y \sim N(0, 1)$, $\tau = 0{,}9$'))
    a2.axvline(qs, color=st.MainBlue, ls='--', lw=1.4, label=L(r'true quantile $q_{0.9} = 1.28$', r'cuantila adevărată $q_{0{,}9} = 1{,}28$'))
    a2.set_xlabel(L(r'quantile forecast $\hat q$', r'prognoza cuantilei $\hat q$'))
    a2.set_ylabel(r'$E\,\rho_{0.9}(Y - \hat q)$' if LANG == 'en' else r'$E\,\rho_{0{,}9}(Y - \hat q)$')
    legend(fig, a2, ncol=1)
    OUT['pin'] = dict(q90=float(qs), minloss=float(loss.min()))
    save(fig, 'ch13_sem_primer_pinball', FULL)


# =============================================================================
# (3) Holm and Benjamini-Hochberg on sorted p-values
# =============================================================================
def holm_bh():
    rng = np.random.default_rng(7)
    S, a = 20, 0.05
    z = np.r_[rng.normal(3.0, 1, 6), rng.normal(0, 1, S - 6)]
    p = np.sort(2 * (1 - stats.norm.cdf(np.abs(z))))
    k = np.arange(1, S + 1)
    holm_line, bh_line = a / (S - k + 1), k * a / S
    ok = p <= holm_line
    n_holm = int(np.argmin(ok)) if not ok.all() else S
    below = np.where(p <= bh_line)[0]
    n_bh = int(below.max() + 1) if len(below) else 0
    fig, ax = plt.subplots(figsize=(5.0, 4.4))
    ax.plot(k, p, 'o', color=st.MainBlue, ms=5, label=L(r'sorted p-values $p_{(k)}$', r'p-value-uri ordonate $p_{(k)}$'))
    ax.plot(k, np.full(S, a), color=st.Amber, ls=':', lw=1.6, label=L(r'no correction, $\alpha$', r'fără corecție, $\alpha$'))
    ax.plot(k, np.full(S, a / S), color=st.Navy if hasattr(st, 'Navy') else st.DarkText, ls='-.', lw=1.4,
            label=L(r'Bonferroni, $\alpha/S$', r'Bonferroni, $\alpha/S$'))
    ax.plot(k, holm_line, color=st.IDAred, lw=1.8, label=r'Holm, $\alpha/(S - k + 1)$')
    ax.plot(k, bh_line, color=st.Forest, lw=1.8, label=r'BH, $k\alpha/S$')
    ax.set_yscale('log')
    ax.set_ylim(1e-6, 1.5)
    ax.set_xlabel(L(r'rank $k$', r'rangul $k$'))
    ax.set_ylabel('p-value')
    ax.set_xticks([1, 5, 10, 15, 20])
    legend(fig, ax, ncol=2)
    OUT['mt'] = dict(S=S, raw=int((p <= a).sum()), bonf=int((p <= a / S).sum()), holm=n_holm, bh=n_bh)
    save(fig, 'ch13_sem_primer_holm_bh')


# =============================================================================
# (4) split conformal: the order statistic and the Beta law of the coverage
# =============================================================================
def split_beta():
    rng = np.random.default_rng(11)
    n, a = 19, 0.1
    S = np.sort(np.abs(rng.normal(0, 1, n)))
    k = int(np.ceil((n + 1) * (1 - a)))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(np.arange(1, n + 1), S, 'o', color=st.MainBlue, ms=5, label=L(r'sorted scores $S_{(i)}$', r'scoruri ordonate $S_{(i)}$'))
    a1.plot([k], [S[k - 1]], 'o', color=st.IDAred, ms=9, mfc='none', mew=2,
            label=L(rf'$\hat q = S_{{({k})}}$, $k = \lceil 20 \cdot 0.9 \rceil$', rf'$\hat q = S_{{({k})}}$, $k = \lceil 20 \cdot 0{{,}}9 \rceil$'))
    a1.axhline(S[k - 1], color=st.IDAred, ls='--', lw=1.2)
    a1.set_xlabel(L(r'rank $i$', r'rangul $i$'))
    a1.set_ylabel(L('score', 'scorul'))
    a1.set_xticks([1, 5, 10, 15, 19])
    legend(fig, a1, ncol=2)
    c = np.linspace(0.70, 1.0, 600)
    sds = {}
    for nn, col in ((9, st.Amber), (49, st.Forest), (499, st.MainBlue)):
        kk = int(np.ceil((nn + 1) * (1 - a)))
        b = stats.beta(kk, nn + 1 - kk)
        a2.plot(c, b.pdf(c), color=col, lw=2, label=rf'$n = {nn}$')
        sds[nn] = float(b.std())
    a2.axvline(0.9, color=st.IDAred, ls='--', lw=1.2, label=L('mean 0.90', 'media 0,90'))
    a2.set_xlabel(L('coverage given the calibration set', 'acoperirea condiționat de setul de calibrare'))
    a2.set_ylabel(L('density', 'densitatea'))
    legend(fig, a2, ncol=4)
    OUT['split'] = dict(k=k, q=float(S[k - 1]), sd9=sds[9], sd49=sds[49], sd499=sds[499])
    save(fig, 'ch13_sem_primer_split_beta', FULL)


# =============================================================================
# (5) exchangeability: an AR(1) path and a random reordering of the same values
# =============================================================================
def exchange():
    rng = np.random.default_rng(5)
    T_, phi = 300, 0.95
    x = np.zeros(T_)
    e = rng.normal(0, 1, T_)
    for t in range(1, T_):
        x[t] = phi * x[t - 1] + e[t]
    xp = rng.permutation(x)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    a1.plot(x, color=st.MainBlue, lw=1.2, label=L(r'AR(1), $\phi = 0.95$', r'AR(1), $\phi = 0{,}95$'))
    a2.plot(xp, color=st.IDAred, lw=1.0, label=L('the same values, randomly reordered', 'aceleași valori, reordonate aleator'))
    for ax in (a1, a2):
        ax.set_xlabel(L('time $t$', 'timpul $t$'))
        ax.set_ylabel('$x_t$')
        legend(fig, ax, ncol=1)
    r1 = np.corrcoef(x[1:], x[:-1])[0, 1]
    r2 = np.corrcoef(xp[1:], xp[:-1])[0, 1]
    OUT['exch'] = dict(r1=float(r1), r2=float(r2))
    save(fig, 'ch13_sem_primer_exchange', FULL)


# =============================================================================
# (6) CQR on heteroskedastic data; weighted conformal with a point mass at +infinity
# =============================================================================
def cqr_weighted():
    rng = np.random.default_rng(3)
    n, a = 400, 0.2
    x = rng.uniform(0, 1, 2 * n)
    sig = 0.2 + 1.2 * x
    y = 2 * np.sin(2 * np.pi * x) + sig * rng.normal(0, 1, 2 * n)
    zq = stats.norm.ppf(0.9)
    lo = 2 * np.sin(2 * np.pi * x) - 0.6 * zq * sig          # too narrow quantile forecasts (60% of the true width)
    hi = 2 * np.sin(2 * np.pi * x) + 0.6 * zq * sig
    cal, te = slice(0, n), slice(n, 2 * n)
    s = np.maximum(lo[cal] - y[cal], y[cal] - hi[cal])
    k = int(np.ceil((n + 1) * (1 - a)))
    qh = np.sort(s)[k - 1]
    raw = np.mean((y[te] >= lo[te]) & (y[te] <= hi[te]))
    adj = np.mean((y[te] >= lo[te] - qh) & (y[te] <= hi[te] + qh))
    o = np.argsort(x[te])
    xs, ys = x[te][o], y[te][o]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(xs, ys, '.', color=st.MainBlue, ms=3, label=L('test points', 'puncte de test'))
    a1.plot(xs, lo[te][o], color=st.Amber, lw=1.6, label=L('raw 10%, 90% quantiles', 'cuantile brute 10%, 90%'))
    a1.plot(xs, hi[te][o], color=st.Amber, lw=1.6)
    a1.plot(xs, lo[te][o] - qh, color=st.IDAred, lw=1.6, ls='--', label=L(r'CQR band, $\pm\hat q$', r'banda CQR, $\pm\hat q$'))
    a1.plot(xs, hi[te][o] + qh, color=st.IDAred, lw=1.6, ls='--')
    a1.set_xlabel('$x$')
    a1.set_ylabel('$y$')
    legend(fig, a1, ncol=3)
    # weighted conformal: ten scores in time order, weights 0.85^(age), test point at +inf with weight 1
    sc = np.array([1.8, 0.6, 2.4, 1.1, 0.9, 3.0, 1.5, 0.4, 2.1, 1.3])
    m = len(sc)
    w = 0.85 ** np.arange(m, 0, -1)
    tw = np.r_[w, 1.0] / (w.sum() + 1.0)
    order = np.argsort(sc)
    cum = np.cumsum(tw[:m][order])
    aw = 0.3
    j = int(np.searchsorted(cum, 1 - aw - 1e-12))
    qw = sc[order][j] if j < m else np.inf
    a2.step(np.r_[0, sc[order]], np.r_[0, cum], where='post', color=st.MainBlue, lw=2,
            label=L(r'cumulative weight', r'ponderea cumulată'))
    a2.axhline(1 - aw, color=st.IDAred, ls='--', lw=1.4, label=L(r'$1 - \alpha = 0.7$', r'$1 - \alpha = 0{,}7$'))
    a2.axhline(cum[-1], color=st.Amber, ls=':', lw=1.6, label=r'$1 - \tilde w_{n+1}$')
    if np.isfinite(qw):
        a2.axvline(qw, color=st.Forest, lw=1.4, label=L(r'weighted $\hat q$', r'$\hat q$ ponderat'))
    a2.set_xlabel(L('score', 'scorul'))
    a2.set_ylabel(L('cumulative weight', 'ponderea cumulată'))
    a2.set_ylim(0, 1.0)
    legend(fig, a2, ncol=4)
    OUT['cqr'] = dict(n=n, qh=float(qh), raw=float(raw), adj=float(adj), pinf=float(tw[-1]), top=float(cum[-1]),
                      qw=float(qw), neff=float(w.sum() ** 2 / (w ** 2).sum()))
    save(fig, 'ch13_sem_primer_cqr_weighted', FULL)


# =============================================================================
# (7) ACI under volatility clustering
# =============================================================================
def aci():
    rng = np.random.default_rng(21)
    T_, a, g, w0 = 3000, 0.1, 0.005, 500
    om, al, be = 0.02, 0.08, 0.90
    r = np.zeros(T_)
    s2 = np.full(T_, om / (1 - al - be))
    z = rng.standard_t(6, T_) / np.sqrt(1.5)
    for t in range(1, T_):
        s2[t] = om + al * r[t - 1] ** 2 + be * s2[t - 1]
        r[t] = np.sqrt(s2[t]) * z[t]
    S = np.abs(r)
    cal = S[:w0]
    ks = int(np.ceil((w0 + 1) * (1 - a)))
    q_static = np.sort(cal)[ks - 1]
    at = a
    q_aci = np.full(T_, np.nan)
    err_s, err_a = np.zeros(T_), np.zeros(T_)
    for t in range(w0, T_):
        past = S[t - w0:t]
        lev = 1 - at
        if lev >= 1:
            q = np.inf
        elif lev <= 0:
            q = -np.inf
        else:
            kk = int(np.ceil((w0 + 1) * lev))
            q = np.inf if kk > w0 else np.sort(past)[kk - 1]
        q_aci[t] = q
        err_a[t] = float(S[t] > q)
        err_s[t] = float(S[t] > q_static)
        at = at + g * (a - err_a[t])
    tt = np.arange(w0, T_)
    W = 250
    loc = lambda e: np.convolve(1 - e[w0:], np.ones(W) / W, mode='valid')   # noqa: E731
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(tt, S[w0:], color=st.MainBlue, lw=0.6, label=L(r'score $|r_t|$', r'scorul $|r_t|$'))
    a1.axhline(q_static, color=st.Amber, lw=1.8, label=L('static threshold', 'pragul static'))
    a1.plot(tt, q_aci[w0:], color=st.IDAred, lw=1.2, label=L(r'ACI threshold $q_t$', r'pragul ACI $q_t$'))
    a1.set_xlabel(L('day $t$', 'ziua $t$'))
    a1.set_ylabel(L('score', 'scorul'))
    a1.set_ylim(0, 1.15 * np.quantile(S[w0:], 0.999))
    legend(fig, a1, ncol=3)
    a2.plot(tt[W - 1:], loc(err_s), color=st.Amber, lw=1.6, label=L('static', 'static'))
    a2.plot(tt[W - 1:], loc(err_a), color=st.IDAred, lw=1.6, label='ACI')
    a2.axhline(1 - a, color=st.Forest, ls='--', lw=1.2, label=L('target 0.90', 'ținta 0,90'))
    a2.set_xlabel(L('day $t$', 'ziua $t$'))
    a2.set_ylabel(L(f'coverage, last {W} days', f'acoperirea, ultimele {W} de zile'))
    legend(fig, a2, ncol=3)
    OUT['aci'] = dict(cov_s=float(1 - err_s[w0:].mean()), cov_a=float(1 - err_a[w0:].mean()),
                      lmin_s=float(loc(err_s).min()), lmax_s=float(loc(err_s).max()),
                      lmin_a=float(loc(err_a).min()), lmax_a=float(loc(err_a).max()), T=T_ - w0)
    save(fig, 'ch13_sem_primer_aci', FULL)


# =============================================================================
# (8) Kupiec and Christoffersen: independent and clustered misses
# =============================================================================
def lr_tests(e, a):
    T_, x = len(e), e.sum()
    ph = x / T_
    luc = -2 * (x * np.log(a) + (T_ - x) * np.log(1 - a) - x * np.log(ph) - (T_ - x) * np.log(1 - ph))
    e0, e1 = e[:-1], e[1:]
    n00 = np.sum((e0 == 0) & (e1 == 0)); n01 = np.sum((e0 == 0) & (e1 == 1))
    n10 = np.sum((e0 == 1) & (e1 == 0)); n11 = np.sum((e0 == 1) & (e1 == 1))
    p01, p11 = n01 / (n00 + n01), n11 / max(n10 + n11, 1)
    p1 = (n01 + n11) / (n00 + n01 + n10 + n11)

    def ll(p, a_, b_):
        return (a_ * np.log(1 - p) if a_ else 0) + (b_ * np.log(p) if b_ else 0)
    lind = -2 * (ll(p1, n00 + n10, n01 + n11) - ll(p01, n00, n01) - ll(p11, n10, n11))
    return dict(x=int(x), luc=float(luc), puc=float(1 - stats.chi2.cdf(luc, 1)), p01=float(p01), p11=float(p11),
                lind=float(lind), pcc=float(1 - stats.chi2.cdf(luc + lind, 2)))


def misses():
    T_, a, p11 = 500, 0.05, 0.30
    p01 = a * (1 - p11) / (1 - a)                       # clustered: same long-run rate, P(miss | miss) = 0.30
    for seed in range(8, 400):                          # first seed with a typical pair of sequences
        rng = np.random.default_rng(seed)
        e1 = (rng.random(T_) < a).astype(float)
        e2 = np.zeros(T_)
        for t in range(1, T_):
            e2[t] = float(rng.random() < (p11 if e2[t - 1] else p01))
        r1, r2 = lr_tests(e1, a), lr_tests(e2, a)
        if min(r1['puc'], r1['pcc'], r2['puc']) > 0.3 and r2['pcc'] < 0.01:
            break
    fig, ax = plt.subplots(figsize=(5.0, 3.6))
    t1, t2 = np.where(e1 == 1)[0], np.where(e2 == 1)[0]
    ax.vlines(t1, 1.1, 1.9, color=st.MainBlue, lw=1.4, label=L('independent misses', 'ratări independente'))
    ax.vlines(t2, 0.1, 0.9, color=st.IDAred, lw=1.4, label=L(r'clustered misses, $\pi_{11} = 0.30$', r'ratări grupate, $\pi_{11} = 0{,}30$'))
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels([L('clustered', 'grupate'), L('independent', 'independente')])
    ax.set_xlabel(L('day $t$', 'ziua $t$'))
    ax.set_ylim(0, 2)
    legend(fig, ax, ncol=1)
    OUT['miss'] = dict(T=T_, ind=lr_tests(e1, a), clu=lr_tests(e2, a))
    save(fig, 'ch13_sem_primer_misses')


# =============================================================================
# (9) VaR: a too-narrow model quantile and its one-sided conformal shift
# =============================================================================
def var_shift():
    a = 0.01
    true = stats.t(4, scale=1.0 * np.sqrt(2 / 4))        # unit variance Student-t(4) returns, in %
    model = stats.norm(0, 0.8)                          # a model that underestimates the volatility
    qt, qm = true.ppf(a), model.ppf(a)
    c = qm - qt
    x = np.linspace(-5, 5, 800)
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.plot(x, true.pdf(x), color=st.MainBlue, lw=2, label=L('true density (Student-$t$)', 'densitatea adevărată (Student-$t$)'))
    ax.plot(x, model.pdf(x), color=st.Amber, lw=1.8, ls='--', label=L('model density (Normal)', 'densitatea modelului (Normală)'))
    xx = x[x <= qt]
    ax.fill_between(xx, 0, true.pdf(xx), color=st.IDAred, alpha=0.45, label=L(r'true 1% tail', r'coada stîngă de 1%'))
    ax.axvline(qm, color=st.Amber, lw=1.6, label=L(r'model quantile $\hat q_t$', r'cuantila modelului $\hat q_t$'))
    ax.axvline(qt, color=st.IDAred, lw=1.6, label=L(r'shifted quantile $\hat q_t - c_t$', r'cuantila deplasată $\hat q_t - c_t$'))
    ax.annotate('', xy=(qt, 0.12), xytext=(qm, 0.12), arrowprops=dict(arrowstyle='->', color=st.DarkText, lw=1.2))
    ax.text((qt + qm) / 2, 0.14, '$c_t$', ha='center', color=st.DarkText)
    ax.set_xlim(-5, 3)
    ax.set_xlabel(L('daily return (%)', 'randamentul zilnic (%)'))
    ax.set_ylabel(L('density', 'densitatea'))
    legend(fig, ax, ncol=2)
    OUT['var'] = dict(qm=float(qm), qt=float(qt), c=float(c), hit=float(true.cdf(qm)))
    save(fig, 'ch13_sem_primer_var_shift')


if __name__ == '__main__':
    for LANG in ('en', 'ro'):
        tokens(); pinball(); holm_bh(); split_beta(); exchange(); cqr_weighted(); aci(); misses(); var_shift()
    with open(os.path.join(HERE, 'sem13_primer.json'), 'w') as fh:
        json.dump(OUT, fh, indent=1)
    print('numbers -> sem13_primer.json')
