"""
seminar14_explainers.py -- Explanatory (primer) charts for Seminar 14 (ATS): causal inference for time series
=============================================================================================================
Teaching charts for the slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 14, which takes place
BEFORE Lecture 14. All charts use SIMULATED data only (fixed seeds): a common driver that creates Granger causality,
the size of classical and HAC Wald tests under volatility clustering, a synthetic control and its placebos, a treated
unit outside the convex hull of the donors, an interrupted time series, the variance of a sum of AR(1) errors, a
local level counterfactual, an event study and the bias of a non-orthogonal estimator. No exercise answers.

Output: charts/ch14_sem_primer_*.pdf/.png (EN) and charts/ch14_sem_primer_*_ro.pdf/.png (RO), transparent
background, legend outside at the bottom, each chart sized for its box on the slides (text >= 6.3 pt there);
the numbers quoted on the slides go to Quantlets/Ch_14/sem14_primer.json.

Run:  python3 Quantlets/Ch_14/seminar14_explainers.py

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
from scipy.optimize import minimize

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


def ols(X, y):
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return b, y - X @ b


# =============================================================================
# (1) a common driver creates Granger causality from x to y
# =============================================================================
def common_driver():
    rng = np.random.default_rng(14)
    T_ = 400
    w = np.zeros(T_)
    for t in range(1, T_):
        w[t] = 0.5 * w[t - 1] + rng.normal()
    x = np.r_[0, w[:-1]] + rng.normal(0, 1, T_)          # x_t = w_{t-1} + e_t
    y = np.r_[0, 0, w[:-2]] + rng.normal(0, 1, T_)       # y_t = w_{t-2} + u_t
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(np.arange(50), w[200:250], color=st.Forest, lw=2.2, label=L(r'driver $w_t$', r'factorul comun $w_t$'))
    a1.plot(np.arange(50), x[200:250], color=st.MainBlue, lw=1.2, marker='o', ms=2.5, label='$x_t$')
    a1.plot(np.arange(50), y[200:250], color=st.IDAred, lw=1.2, marker='o', ms=2.5, label='$y_t$')
    a1.set_xlabel(L('time $t$', 'timpul $t$'))
    leg(a1, 3)
    ks = np.arange(-4, 5)
    cc = [np.corrcoef(y[5:-5], np.roll(x, k)[5:-5])[0, 1] for k in ks]
    a2.bar(ks, cc, color=[st.IDAred if k == 1 else st.MainBlue for k in ks], width=0.6,
           label=L(r'corr$(y_t, x_{t-k})$', r'corr$(y_t, x_{t-k})$'))
    a2.axhline(1.96 / np.sqrt(T_), color=st.Amber, ls='--', lw=1.2, label=L(r'$\pm 1.96/\sqrt{T}$', r'$\pm 1{,}96/\sqrt{T}$'))
    a2.axhline(-1.96 / np.sqrt(T_), color=st.Amber, ls='--', lw=1.2)
    a2.set_xlabel(L(r'lag $k$', r'lagul $k$'))
    a2.set_xticks(ks)
    leg(a2, 2)
    # Granger F-test y on 2 own lags with and without 2 lags of x
    Y = y[3:]
    Xr = np.column_stack([np.ones(T_ - 3), y[2:-1], y[1:-2]])
    Xf = np.column_stack([Xr, x[2:-1], x[1:-2]])
    _, er = ols(Xr, Y)
    _, ef = ols(Xf, Y)
    W = (len(Y) - Xf.shape[1]) * (er @ er - ef @ ef) / (ef @ ef)
    OUT['gc'] = dict(T=T_, cc1=float(cc[list(ks).index(1)]), W=float(W), p=float(stats.chi2.sf(W, 2)),
                     F=float(np.log((er @ er) / (ef @ ef))))
    save(fig, 'ch14_sem_primer_common_driver', FULL)


# =============================================================================
# (2) the size of classical and HAC Wald tests under volatility clustering
# =============================================================================
def garch(rng, T_, om=0.05, a=0.10, b=0.88):
    """Conditional standard deviations sigma_t of a simulated GARCH(1,1) with Student-t(6) shocks."""
    r, sd = np.zeros(T_ + 200), np.zeros(T_ + 200)
    z = rng.standard_t(6, T_ + 200) / np.sqrt(1.5)
    s2 = om / (1 - a - b)
    for t in range(1, T_ + 200):
        s2 = om + a * r[t - 1] ** 2 + b * s2
        sd[t] = np.sqrt(s2)
        r[t] = sd[t] * z[t]
    return sd[200:]


def wald_stats(y, x, p=2, L_=5):
    T_ = len(y)
    Y = y[p:]
    X = np.column_stack([np.ones(T_ - p)] + [y[p - j:T_ - j] for j in range(1, p + 1)] + [x[p - j:T_ - j] for j in range(1, p + 1)])
    b, e = ols(X, Y)
    XtXi = np.linalg.inv(X.T @ X)
    Vc = XtXi * (e @ e) / (len(Y) - X.shape[1])
    u = X * e[:, None]
    S = u.T @ u
    for j in range(1, L_ + 1):
        G = u[j:].T @ u[:-j]
        S += (1 - j / (L_ + 1)) * (G + G.T)
    Vh = XtXi @ S @ XtXi
    R = slice(1 + p, 1 + 2 * p)
    bb = b[R]
    return float(bb @ np.linalg.solve(Vc[R, R], bb)), float(bb @ np.linalg.solve(Vh[R, R], bb))


_CACHE = {}


def wald_hac():
    if 'wald' not in _CACHE:
        _CACHE['wald'] = _wald_sim()
    Wc, Wh, R_, T_ = _CACHE['wald']
    _wald_plot(Wc, Wh, R_, T_)


def _wald_sim():
    rng = np.random.default_rng(41)
    R_, T_ = 600, 1000
    Wc, Wh = [], []
    for _ in range(R_):
        s = garch(rng, T_)                               # a common volatility: y and x calm and turbulent together
        y = s * rng.normal(0, 1, T_) / np.std(s)
        x = s * rng.normal(0, 1, T_) / np.std(s)         # no lag of x enters the mean of y (H0 true)
        c, h = wald_stats(y, x)
        Wc.append(c); Wh.append(h)
    return np.array(Wc), np.array(Wh), R_, T_


def _wald_plot(Wc, Wh, R_, T_):
    crit = stats.chi2.ppf(0.95, 2)
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    bins = np.linspace(0, 20, 41)
    ax.hist(np.minimum(Wc, 19.9), bins=bins, density=True, color=st.IDAred, alpha=0.45, label=L('classical Wald', 'Wald clasic'))
    ax.hist(np.minimum(Wh, 19.9), bins=bins, density=True, histtype='step', color=st.MainBlue, lw=2, label='Wald HAC')
    g = np.linspace(0.05, 20, 300)
    ax.plot(g, stats.chi2.pdf(g, 2), color=st.Forest, lw=2, label=r'$\chi^2_2$')
    ax.axvline(crit, color=st.Amber, ls='--', lw=1.4, label=L(r'5% critical value', r'valoarea critică 5%'))
    ax.set_xlabel(L(r'statistic under $H_0$', r'statistica sub $H_0$'))
    ax.set_ylabel(L('density', 'densitatea'))
    leg(ax, 2)
    OUT['wald'] = dict(R=R_, T=T_, size_c=float(np.mean(Wc > crit)), size_h=float(np.mean(Wh > crit)), crit=float(crit))
    save(fig, 'ch14_sem_primer_wald_hac')


# =============================================================================
# (3) synthetic control: fit, gap and in-space placebos
# =============================================================================
def simplex_fit(y1, Y0):
    J = Y0.shape[1]
    f = lambda w: np.sum((y1 - Y0 @ w) ** 2)          # noqa: E731
    cons = ({'type': 'eq', 'fun': lambda w: w.sum() - 1},)
    r = minimize(f, np.full(J, 1 / J), bounds=[(0, 1)] * J, constraints=cons, method='SLSQP')
    return r.x


def sc_panel(rng, J=12, T_=40, T0=28, eff=2.0):
    F = np.cumsum(rng.normal(0.3, 1, (T_, 2)), axis=0)
    lam = rng.uniform(0, 1, (J + 1, 2))
    lam[0] = lam[1:4].mean(axis=0)                      # treated unit inside the hull of three donors
    Y = F @ lam.T + rng.normal(0, 0.5, (T_, J + 1))
    Y[T0:, 0] += eff * np.linspace(0.3, 1, T_ - T0)
    return Y, T0


def sc():
    rng = np.random.default_rng(3)
    Y, T0 = sc_panel(rng)
    T_, J1 = Y.shape
    ratios, gaps = [], []
    for j in range(J1):
        d = [k for k in range(J1) if k != j]
        w = simplex_fit(Y[:T0, j], Y[:T0, d])
        g = Y[:, j] - Y[:, d] @ w
        gaps.append(g)
        ratios.append(np.sqrt(np.mean(g[T0:] ** 2)) / np.sqrt(np.mean(g[:T0] ** 2)))
        if j == 0:
            synth = Y[:, d] @ w
            w0 = w
    ratios = np.array(ratios)
    pval = np.mean(ratios >= ratios[0])
    t = np.arange(T_)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(t, Y[:, 0], color=st.IDAred, lw=2, label=L('treated unit', 'unitatea tratată'))
    a1.plot(t, synth, color=st.MainBlue, lw=2, ls='--', label=L('synthetic control', 'controlul sintetic'))
    a1.axvline(T0 - 0.5, color=st.Amber, lw=1.2, label=L(r'treatment, $T_0$', r'tratamentul, $T_0$'))
    a1.set_xlabel(L('period $t$', 'perioada $t$'))
    a1.set_ylabel('$Y_{1t}$')
    leg(a1, 3)
    for j in range(1, J1):
        a2.plot(t, gaps[j], color=st.LightBlue, lw=0.9, label=L('placebo gaps (donors)', 'diferențe placebo (donatori)') if j == 1 else '_')
    a2.plot(t, gaps[0], color=st.IDAred, lw=2, label=L(r'gap of the treated unit $\hat\tau_{1t}$', r'diferența unității tratate $\hat\tau_{1t}$'))
    a2.axvline(T0 - 0.5, color=st.Amber, lw=1.2)
    a2.axhline(0, color=st.DarkText, lw=0.6)
    a2.set_xlabel(L('period $t$', 'perioada $t$'))
    leg(a2, 2)
    OUT['sc'] = dict(J=J1 - 1, T0=T0, T=T_, w_top=float(np.sort(w0)[-1]), n_pos=int(np.sum(w0 > 0.02)),
                     r1=float(ratios[0]), rank=int(np.sum(ratios >= ratios[0])), p=float(pval),
                     pre=float(np.sqrt(np.mean(gaps[0][:T0] ** 2))))
    save(fig, 'ch14_sem_primer_sc', FULL)


# =============================================================================
# (4) a treated unit outside the convex hull of the donors; demeaning restores the fit
# =============================================================================
def hull():
    rng = np.random.default_rng(9)
    T_, T0 = 30, 20
    t = np.arange(T_)
    base = 2 + 0.15 * t + 0.6 * np.sin(t / 3)
    donors = np.column_stack([base + c + rng.normal(0, 0.15, T_) for c in (-1.0, -0.4, 0.3, 0.8)])
    y1 = base + 3.0 + rng.normal(0, 0.15, T_)
    w = simplex_fit(y1[:T0], donors[:T0])
    m1, m0 = y1[:T0].mean(), donors[:T0].mean(axis=0)
    wd = simplex_fit(y1[:T0] - m1, donors[:T0] - m0)
    synth = donors @ w
    synth_d = (donors - m0) @ wd + m1
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for k in range(4):
        a1.plot(t, donors[:, k], color=st.LightBlue, lw=1.0, label=L('donors', 'donatori') if k == 0 else '_')
        a2.plot(t, donors[:, k], color=st.LightBlue, lw=1.0, label='_')
    for ax, s_, lab in ((a1, synth, L('SC on levels', 'SC pe niveluri')), (a2, synth_d, L('demeaned SC + intercept', 'SC demediat + interceptul'))):
        ax.plot(t, y1, color=st.IDAred, lw=2, label=L('treated unit', 'unitatea tratată'))
        ax.plot(t, s_, color=st.MainBlue, lw=2, ls='--', label=lab)
        ax.axvline(T0 - 0.5, color=st.Amber, lw=1.2)
        ax.set_xlabel(L('period $t$', 'perioada $t$'))
        leg(ax, 3)
    OUT['hull'] = dict(rmspe=float(np.sqrt(np.mean((y1[:T0] - synth[:T0]) ** 2))),
                       rmspe_d=float(np.sqrt(np.mean((y1[:T0] - synth_d[:T0]) ** 2))))
    save(fig, 'ch14_sem_primer_hull', FULL)


# =============================================================================
# (5) interrupted time series with AR(1) errors
# =============================================================================
def its():
    rng = np.random.default_rng(12)
    T_, T0, rho = 96, 72, 0.6
    t = np.arange(T_)
    season = 0.4 * np.sin(2 * np.pi * t / 12)
    u = np.zeros(T_)
    for k in range(1, T_):
        u[k] = rho * u[k - 1] + rng.normal(0, 0.3)
    y = 1 + 0.01 * t + season + u
    y[T0:] += 0.5
    X = np.column_stack([np.ones(T_), t] + [(t % 12 == m).astype(float) for m in range(1, 12)])
    b, e = ols(X[:T0], y[:T0])
    f = X @ b
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(t, y, color=st.MainBlue, lw=1.4, label='$y_t$')
    a1.plot(t[:T0], f[:T0], color=st.Forest, lw=1.4, ls='--', label=L(r'fit $\hat f(t)$', r'ajustarea $\hat f(t)$'))
    a1.plot(t[T0:], f[T0:], color=st.IDAred, lw=1.8, ls='--', label=L('counterfactual (extrapolated)', 'contrafactualul (extrapolat)'))
    a1.axvline(T0 - 0.5, color=st.Amber, lw=1.2)
    a1.set_xlabel(L('month $t$', 'luna $t$'))
    leg(a1, 3)
    tau = y[T0:] - f[T0:]
    a2.bar(t[T0:], tau, color=st.MainBlue, width=0.7, label=L(r'estimated effect $\hat\tau_t$', r'efectul estimat $\hat\tau_t$'))
    a2.axhline(0.5, color=st.IDAred, lw=2, ls='--', label=L('true effect 0.5', 'efectul adevărat 0,5'))
    a2.axhline(0, color=st.DarkText, lw=0.6)
    a2.set_xlabel(L('month $t$', 'luna $t$'))
    leg(a2, 2)
    OUT['its'] = dict(T0=T0, n=T_ - T0, cum=float(tau.sum()), true=float(0.5 * (T_ - T0)), rho=rho)
    save(fig, 'ch14_sem_primer_its', FULL)


# =============================================================================
# (6) variance of a sum of AR(1) errors relative to the i.i.d. formula
# =============================================================================
def ar1_sum():
    n = np.arange(1, 61)
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    out = {}
    for rho, c in ((0.3, st.Forest), (0.6, st.MainBlue), (0.9, st.IDAred)):
        k = np.arange(1, 60)
        ratio = np.array([1 + 2 * np.sum((1 - k[:m - 1] / m) * rho ** k[:m - 1]) for m in n])
        ax.plot(n, ratio, color=c, lw=2, label=rf'$\rho = {rho}$'.replace('.', '.' if LANG == 'en' else '{,}'))
        ax.axhline((1 + rho) / (1 - rho), color=c, ls=':', lw=1.2)
        out[str(rho)] = dict(lim=(1 + rho) / (1 - rho), at12=float(ratio[11]))
    ax.set_xlabel(L(r'number of summed errors $n$', r'numărul de erori însumate $n$'))
    ax.set_ylabel(r'$\mathrm{Var}(\sum u_t)\,/\,(n\gamma_0)$')
    leg(ax, 3)
    OUT['ar1'] = out
    save(fig, 'ch14_sem_primer_ar1_sum')


# =============================================================================
# (7) local level counterfactual: the band widens with the horizon
# =============================================================================
def local_level():
    rng = np.random.default_rng(7)
    T0, H = 80, 30
    se2, sh2 = 0.25, 0.02
    mu = np.cumsum(rng.normal(0, np.sqrt(sh2), T0 + H)) + 5
    y = mu + rng.normal(0, np.sqrt(se2), T0 + H)
    y[T0:] += 0.8
    a, P = y[0], 1.0
    for t in range(T0):                                  # Kalman filter of the local level
        F = P + se2
        K = P / F
        a, P = a + K * (y[t] - a), P * (1 - K)
        P = P + sh2
    P_T = P - sh2                                        # filtered variance at T0
    h = np.arange(1, H + 1)
    var = P_T + h * sh2 + se2
    t = np.arange(T0 + H)
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.plot(t, y, color=st.MainBlue, lw=1.2, label='$y_t$')
    ax.plot(t[T0:], np.full(H, a), color=st.IDAred, lw=2, ls='--', label=L('counterfactual mean', 'media contrafactualului'))
    ax.fill_between(t[T0:], a - 1.96 * np.sqrt(var), a + 1.96 * np.sqrt(var), color=st.IDAred, alpha=0.30, label=L('95% band', 'banda de 95%'))
    ax.axvline(T0 - 0.5, color=st.Amber, lw=1.2, label=L(r'intervention $T_0$', r'intervenția $T_0$'))
    ax.set_xlabel(L('period $t$', 'perioada $t$'))
    leg(ax, 2)
    OUT['ll'] = dict(se2=se2, sh2=sh2, P=float(P_T), v1=float(var[0]), vH=float(var[-1]), H=H)
    save(fig, 'ch14_sem_primer_local_level')


# =============================================================================
# (8) event study: abnormal and cumulative abnormal returns
# =============================================================================
def event():
    est, win = 250, 10
    for seed in range(5, 300):                          # first seed with no visible drift before the event
        rng = np.random.default_rng(seed)
        rm = rng.normal(0.03, 1.0, est + 2 * win + 1)
        r = 0.01 + 1.2 * rm + rng.normal(0, 0.4, len(rm))
        ev = est + win
        r[ev] += -4.0
        r[ev + 1] += -1.0
        b, _ = ols(np.column_stack([np.ones(est), rm[:est]]), r[:est])
        k = np.arange(-win, win + 1)
        AR = r[est:] - b[0] - b[1] * rm[est:]
        CAR = np.cumsum(AR)
        if np.max(np.abs(CAR[:win])) < 0.6 and abs(CAR[-1] - CAR[win + 1]) < 0.6:
            break
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.bar(k, AR, color=st.MainBlue, width=0.7, label=L(r'abnormal return $AR_t$', r'randamentul anormal $AR_t$'))
    ax.plot(k, CAR, color=st.IDAred, lw=2, marker='o', ms=3, label=L(r'$CAR$ from day $-10$', r'$CAR$ din ziua $-10$'))
    ax.axvline(0, color=st.Amber, lw=1.2, ls='--', label=L('event day', 'ziua evenimentului'))
    ax.axhline(0, color=st.DarkText, lw=0.6)
    ax.set_xlabel(L('day relative to the event', 'ziua față de eveniment'))
    ax.set_ylabel('%')
    leg(ax, 2)
    OUT['ev'] = dict(a=float(b[0]), b=float(b[1]), ar0=float(AR[win]), car=float(CAR[-1]))
    save(fig, 'ch14_sem_primer_event')


# =============================================================================
# (9) DML: a regularised plug-in estimator is biased, the orthogonal one is not
# =============================================================================
def ridge(X, y, lam):
    Xc = np.column_stack([np.ones(len(y)), X])
    I_ = np.eye(Xc.shape[1]); I_[0, 0] = 0
    return np.linalg.solve(Xc.T @ Xc + lam * I_, Xc.T @ y)


def feats(X):
    return np.column_stack([X, X ** 2, np.sin(2 * X)])


def dml():
    if 'dml' not in _CACHE:
        _CACHE['dml'] = _dml_sim()
    naive, orth, R_, n_, p_, theta = _CACHE['dml']
    _dml_plot(naive, orth, R_, n_, p_, theta)


def _dml_sim():
    rng = np.random.default_rng(10)
    R_, n_, p_, theta = 400, 500, 10, 0.5
    beta = 1.0 / np.arange(1, p_ + 1)
    naive, orth = [], []
    for _ in range(R_):
        X = rng.normal(0, 1, (n_, p_))
        m = X @ beta
        d = m + rng.normal(0, 1, n_)
        g = np.sin(2 * X @ beta) + 2 * X @ beta
        y = theta * d + g + rng.normal(0, 1, n_)
        Fx = feats(X)
        lam = 20.0                                      # ridge penalty: g and m are learned with a regularisation bias
        # plug-in: ridge of y on (d, features) with the penalty on the features only
        Z = np.column_stack([np.ones(n_), d, Fx])
        I_ = np.eye(Z.shape[1]); I_[:2, :2] = 0
        naive.append(np.linalg.solve(Z.T @ Z + lam * I_, Z.T @ y)[1])
        # DML with two folds (cross-fitting), ridge learners for l(X) = E[y|X] and m(X) = E[d|X]
        idx = rng.permutation(n_)
        num = den = 0.0
        for a_, b_ in ((idx[:n_ // 2], idx[n_ // 2:]), (idx[n_ // 2:], idx[:n_ // 2])):
            bl, bm = ridge(Fx[a_], y[a_], lam), ridge(Fx[a_], d[a_], lam)
            Fb = np.column_stack([np.ones(len(b_)), Fx[b_]])
            ry, rd = y[b_] - Fb @ bl, d[b_] - Fb @ bm
            num += rd @ ry
            den += rd @ rd
        orth.append(num / den)
    return np.array(naive), np.array(orth), R_, n_, p_, theta


def _dml_plot(naive, orth, R_, n_, p_, theta):
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    bins = np.linspace(min(naive.min(), orth.min()) - 0.02, max(naive.max(), orth.max()) + 0.02, 40)
    ax.hist(naive, bins=bins, color=st.IDAred, alpha=0.45, density=True, label=L('regularised plug-in', 'plug-in regularizat'))
    ax.hist(orth, bins=bins, histtype='step', color=st.MainBlue, lw=2, density=True, label=L('DML (orthogonal, cross-fitted)', 'DML (ortogonal, cross-fitting)'))
    ax.axvline(theta, color=st.Forest, lw=2, ls='--', label=L(r'true $\theta = 0.5$', r'$\theta$ adevărat $= 0{,}5$'))
    ax.set_xlabel(L(r'estimate $\hat\theta$', r'estimația $\hat\theta$'))
    ax.set_ylabel(L('density', 'densitatea'))
    leg(ax, 2)
    OUT['dml'] = dict(R=R_, n=n_, p=p_, bias_n=float(naive.mean() - theta), bias_o=float(orth.mean() - theta),
                      sd_n=float(naive.std()), sd_o=float(orth.std()))
    save(fig, 'ch14_sem_primer_dml')


if __name__ == '__main__':
    for LANG in ('en', 'ro'):
        common_driver(); wald_hac(); sc(); hull(); its(); ar1_sum(); local_level(); event(); dml()
    with open(os.path.join(HERE, 'sem14_primer.json'), 'w') as fh:
        json.dump(OUT, fh, indent=1)
    print('numbers -> sem14_primer.json')
