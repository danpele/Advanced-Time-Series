"""
risk_core.py -- the numerical engine of Chapter 9 (ATS): VaR, ES, scoring functions, dynamic quantile and ES models,
backtests and forecast comparison, written out in numpy/scipy (numba only accelerates the recursions)
====================================================================================================================
Conventions: returns y_t in %; alpha is the tail level (VaR 1%: alpha = 0.01); v_t and e_t are the alpha-quantile and
the alpha-tail mean of the return distribution (both negative), so VaR_t = -v_t and ES_t = -e_t.
  * losses        pinball (quantile score), FZ0 (Patton, Ziegel and Chen 2019, eq. 6), elementary quantile scores
                  (Ehm et al. 2016) for Murphy diagrams;
  * benchmarks    rolling-window historical simulation; ARMA-GARCH with Normal, skew-t (Hansen 1994) or empirical
                  (EDF) innovations; GJR-GARCH-t;
  * CAViaR        the four specifications of Engle and Manganelli (2004), their estimation procedure, the asymptotic
                  asymptotic covariance and the out-of-sample DQ test;
  * FZ models     GAS-2F, GAS-1F, GARCH-FZ and Hybrid of Patton, Ziegel and Chen (2019), estimated by FZ0
                  minimisation with the smoothing schedule of their Appendix C; joint linear (VaR, ES) regression;
  * backtests     Kupiec, Christoffersen, duration (Christoffersen and Pelletier 2004), DQ, the generalised-residual
                  regressions of PZC (eq. 41), McNeil-Frey;
  * comparison    Diebold-Mariano with HAC variance, the model confidence set (Hansen, Lunde and Nason 2011);
  * other         extremal index (Ferro and Segers 2003), adaptive conformal inference (Gibbs and Candes 2021).
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import numpy as np
from scipy import optimize, stats, special, integrate

try:
    from numba import njit
except ImportError:                     # plain Python if numba is missing (slower, same results)
    def njit(*args, **kw):
        if args and callable(args[0]):
            return args[0]
        return lambda f: f


# =============================================================================
# LOSSES AND SCORES
# =============================================================================
def pinball(y, q, a):
    """Quantile (pinball, tick) loss (1{y <= q} - a)(q - y), strictly consistent for the a-quantile."""
    y, q = np.asarray(y, float), np.asarray(q, float)
    return ((y <= q).astype(float) - a) * (q - y)


def fz0(y, v, e, a):
    """FZ0 loss of Patton, Ziegel and Chen (2019, eq. 6): the zero-homogeneous member of the Fissler-Ziegel class;
    needs e < 0 (and e <= v)."""
    y, v, e = np.asarray(y, float), np.asarray(v, float), np.asarray(e, float)
    return -((y <= v) * (v - y)) / (a * e) + v / e + np.log(-e) - 1.0


def fz_general(y, v, e, a, G1, G2, calG2):
    """The Fissler-Ziegel (2016) class as written in PZC (eq. 4): G1 weakly increasing, calG2' = G2 > 0 increasing."""
    ind = (y <= v).astype(float)
    return (ind - a) * (G1(v) - G1(y)) + G2(e) * (v - e + ind * (y - v) / a) - calG2(e)


def murphy_quantile(y, x, a, thetas):
    """Average elementary quantile scores S_theta(x, y) = (1{y < x} - a)(1{theta < x} - 1{theta < y}) (Ehm et al.
    2016): one curve per forecast; a forecast dominates if its curve is below for every theta."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    ind = (y < x).astype(float) - a
    return np.array([np.mean(ind * ((th < x).astype(float) - (th < y).astype(float))) for th in thetas])


# =============================================================================
# DISTRIBUTIONS
# =============================================================================
def skewt_consts(nu, lam):
    c = special.gamma((nu + 1) / 2) / (np.sqrt(np.pi * (nu - 2)) * special.gamma(nu / 2))
    a = 4 * lam * c * (nu - 2) / (nu - 1)
    b = np.sqrt(1 + 3 * lam ** 2 - a ** 2)
    return a, b, c


def skewt_logpdf(z, nu, lam):
    """Hansen (1994) skewed t, zero mean and unit variance."""
    a, b, c = skewt_consts(nu, lam)
    s = np.where(z < -a / b, 1 - lam, 1 + lam)
    return np.log(b) + np.log(c) - (nu + 1) / 2 * np.log1p(((b * z + a) / s) ** 2 / (nu - 2))


def skewt_ppf(u, nu, lam):
    a, b, _ = skewt_consts(nu, lam)
    u = np.asarray(u, float)
    k = np.sqrt((nu - 2) / nu)
    lo = (1 - lam) * k * stats.t.ppf(np.clip(u / (1 - lam), 1e-15, 1 - 1e-15), nu)
    hi = (1 + lam) * k * stats.t.ppf(np.clip(0.5 + (u - (1 - lam) / 2) / (1 + lam), 1e-15, 1 - 1e-15), nu)
    return (np.where(u < (1 - lam) / 2, lo, hi) - a) / b


def skewt_var_es(a_lvl, nu, lam):
    """(alpha-quantile, alpha-tail mean) of the standardised skewed t."""
    q = float(skewt_ppf(a_lvl, nu, lam))
    m = integrate.quad(lambda z: z * np.exp(skewt_logpdf(z, nu, lam)), -np.inf, q, limit=200)[0] / a_lvl
    return q, m


def skewt_fit(z):
    """Maximum likelihood for (nu, lambda) of the skewed t on standardised residuals."""
    f = lambda p: -np.sum(skewt_logpdf(z, 2.05 + np.exp(p[0]), np.tanh(p[1])))
    r = optimize.minimize(f, [np.log(6.0), -0.1], method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-8})
    return 2.05 + np.exp(r.x[0]), float(np.tanh(r.x[1]))


def t_std_var_es(a_lvl, nu):
    """(alpha-quantile, alpha-tail mean) of the Student t scaled to unit variance."""
    s = np.sqrt((nu - 2) / nu)
    q = stats.t.ppf(a_lvl, nu)
    es = -stats.t.pdf(q, nu) * (nu + q ** 2) / ((nu - 1) * a_lvl)
    return s * q, s * es


def normal_var_es(a_lvl):
    z = stats.norm.ppf(a_lvl)
    return z, -stats.norm.pdf(z) / a_lvl


# =============================================================================
# ROLLING WINDOW (HISTORICAL SIMULATION)
# =============================================================================
def rolling_hs(y, w, a):
    """Rolling-window VaR and ES: for day t the sample a-quantile and the mean of the returns at or below it among
    y[t-w], ..., y[t-1]. Returns arrays of length len(y) (NaN for t < w)."""
    y = np.asarray(y, float)
    T = len(y)
    v, e = np.full(T, np.nan), np.full(T, np.nan)
    win = np.lib.stride_tricks.sliding_window_view(y[:-1], w)        # window ending at t-1, for t = w..T-1
    q = np.quantile(win, a, axis=1)
    m = np.where(win <= q[:, None], win, 0.0).sum(axis=1) / np.maximum((win <= q[:, None]).sum(axis=1), 1)
    v[w:], e[w:] = q, m
    return v, e


# =============================================================================
# GARCH FAMILY
# =============================================================================
@njit(cache=True, error_model="numpy")
def garch_path(eps, omega, alpha, gamma, beta, h0):
    """GJR-GARCH(1,1) variance h_t = omega + (alpha + gamma 1{eps<0}) eps_{t-1}^2 + beta h_{t-1}; length T + 1
    (the last element is the forecast for T + 1)."""
    T = eps.shape[0]
    h = np.empty(T + 1)
    h[0] = h0
    for t in range(1, T + 1):
        e = eps[t - 1]
        g = gamma if e < 0 else 0.0
        h[t] = omega + (alpha + g) * e * e + beta * h[t - 1]
    return h


def garch_negll(p, eps, dist='normal', gjr=False):
    omega, alpha = p[0], p[1]
    gamma, beta = (p[2], p[3]) if gjr else (0.0, p[2])
    if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta + gamma / 2 >= 0.9999 or (gjr and alpha + gamma < 0):
        return 1e10
    h = garch_path(eps, omega, alpha, gamma, beta, np.var(eps))[:-1]
    if dist == 'normal':
        return 0.5 * np.sum(np.log(2 * np.pi * h) + eps ** 2 / h)
    nu = p[-1]
    if nu <= 2.05 or nu > 200:
        return 1e10
    z = eps / np.sqrt(h)
    ll = (special.gammaln((nu + 1) / 2) - special.gammaln(nu / 2) - 0.5 * np.log(np.pi * (nu - 2))
          - 0.5 * np.log(h) - (nu + 1) / 2 * np.log1p(z ** 2 / (nu - 2)))
    return -np.sum(ll)


def garch_fit(eps, dist='normal', gjr=False):
    """(Q)ML for GARCH(1,1) or GJR-GARCH(1,1) with Normal or Student-t innovations; returns the parameter vector
    (omega, alpha, [gamma,] beta, [nu])."""
    eps = np.asarray(eps, float)
    v = np.var(eps)
    best = None
    for b0 in (0.85, 0.93):
        p0 = [v * (1 - b0 - 0.06), 0.06] + ([0.04] if gjr else []) + [b0] + ([7.0] if dist == 't' else [])
        if gjr:
            p0[1] = 0.02
        r = optimize.minimize(garch_negll, p0, args=(eps, dist, gjr), method='Nelder-Mead',
                              options={'maxiter': 6000, 'xatol': 1e-8, 'fatol': 1e-8})
        r = optimize.minimize(garch_negll, r.x, args=(eps, dist, gjr), method='Nelder-Mead',
                              options={'maxiter': 6000, 'xatol': 1e-9, 'fatol': 1e-10})
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def garch_sigma(eps, p, gjr=False, h0=None):
    """Conditional standard deviation path (length T + 1) for given parameters."""
    omega, alpha = p[0], p[1]
    gamma, beta = (p[2], p[3]) if gjr else (0.0, p[2])
    return np.sqrt(garch_path(np.asarray(eps, float), omega, alpha, gamma, beta, np.var(eps) if h0 is None else h0))


# =============================================================================
# ARMA MEAN (BIC), AS IN PZC SECTION 5
# =============================================================================
def arma_bic(y_in, pmax=5, qmax=5):
    """ARMA(p, q) with a constant chosen by BIC over 0 <= p <= pmax, 0 <= q <= qmax (Gaussian ML, statsmodels)."""
    import warnings
    from statsmodels.tsa.arima.model import ARIMA
    best = (np.inf, (0, 0), None)
    for p in range(pmax + 1):
        for q in range(qmax + 1):
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                try:
                    r = ARIMA(y_in, order=(p, 0, q), trend='c').fit()
                except Exception:
                    continue
            if r.bic < best[0]:
                best = (r.bic, (p, q), r)
    return best[1], best[2]


def arma_onestep(res, y_full):
    """One-step-ahead conditional means for the whole series with the in-sample parameters kept fixed."""
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        r = res.apply(np.asarray(y_full, float))
    return np.asarray(r.fittedvalues, float)


# =============================================================================
# CAViaR (ENGLE AND MANGANELLI 2004)
# =============================================================================
CAVIAR_K = {'SAV': 3, 'AS': 4, 'IG': 3, 'ADAPT': 1}


@njit(cache=True, error_model="numpy")
def caviar_path(spec, b, y, theta, f1, G):
    """CAViaR recursions written for VaR_t = -q_t(theta) > 0 (spec 0 SAV, 1 AS, 2 IG, 3 adaptive). Length T + 1."""
    T = y.shape[0]
    f = np.empty(T + 1)
    f[0] = f1
    for t in range(1, T + 1):
        x = y[t - 1]
        if spec == 0:
            f[t] = b[0] + b[1] * f[t - 1] + b[2] * abs(x)
        elif spec == 1:
            f[t] = b[0] + b[1] * f[t - 1] + b[2] * max(x, 0.0) + b[3] * max(-x, 0.0)
        elif spec == 2:
            s = b[0] + b[1] * f[t - 1] * f[t - 1] + b[2] * x * x
            f[t] = np.sqrt(s) if s > 0 else 1e6
        else:                                                   # adaptive, in the quantile q = -VaR
            q = -f[t - 1]
            arg = G * (x - q)
            hit = 1.0 / (1.0 + np.exp(arg)) if arg < 700 else 0.0
            f[t] = -(q + b[0] * (hit - theta))
    return f


SPEC_ID = {'SAV': 0, 'AS': 1, 'IG': 2, 'ADAPT': 3}


def caviar_var(spec, b, y, theta, f1, G=10.0):
    return caviar_path(SPEC_ID[spec], np.asarray(b, float), np.asarray(y, float), theta, f1, G)


def caviar_rq(b, spec, y, theta, f1, G=10.0):
    """Regression-quantile objective of EM (2004): the average pinball loss of q_t = -VaR_t."""
    f = caviar_var(spec, b, y, theta, f1, G)[:-1]
    if not np.all(np.isfinite(f)) or np.any(np.abs(f) > 1e5):
        return 1e10
    return float(np.mean(pinball(y, -f, theta)))


def caviar_fit(spec, y, theta, n_rand=10_000, n_best=10, seed=2026, G=10.0, max_loops=10):
    """EM (2004), empirical section: f_1 = minus the empirical theta-quantile of the first 300 observations; 10^4 uniform
    random parameter vectors, the 10 with the lowest RQ refined by alternating simplex and quasi-Newton steps until
    the objective stops improving; the best of the 10 is kept."""
    y = np.asarray(y, float)
    f1 = -np.quantile(y[:300], theta)
    rng = np.random.default_rng(seed)
    k = CAVIAR_K[spec]
    cand = rng.uniform(0, 1, size=(n_rand, k))
    obj = np.array([caviar_rq(c, spec, y, theta, f1, G) for c in cand])
    starts = cand[np.argsort(obj)[:n_best]]
    best = (np.inf, None)
    for s in starts:
        x, fx = s, caviar_rq(s, spec, y, theta, f1, G)
        for _ in range(max_loops):
            r1 = optimize.minimize(caviar_rq, x, args=(spec, y, theta, f1, G), method='Nelder-Mead',
                                   options={'maxiter': 4000, 'xatol': 1e-8, 'fatol': 1e-12})
            r2 = optimize.minimize(caviar_rq, r1.x, args=(spec, y, theta, f1, G), method='BFGS',
                                   options={'maxiter': 500})
            xn, fn = (r2.x, r2.fun) if r2.fun < r1.fun else (r1.x, r1.fun)
            if fx - fn < 1e-10:
                x, fx = (xn, fn) if fn < fx else (x, fx)
                break
            x, fx = xn, fn
        if fx < best[0]:
            best = (fx, x)
    return {'b': best[1], 'rq': best[0], 'f1': f1, 'spec': spec, 'theta': theta}


def num_grad_path(fun, b, eps=1e-6):
    """Jacobian of a path function b -> f (length T) by central differences: T x k."""
    b = np.asarray(b, float)
    cols = []
    for j in range(len(b)):
        d = np.zeros_like(b)
        d[j] = eps * max(1.0, abs(b[j]))
        cols.append((fun(b + d) - fun(b - d)) / (2 * d[j]))
    return np.column_stack(cols)


def qr_bandwidth(T, theta, resid):
    """Hall-Sheather bandwidth on the probability scale, mapped to the residual scale with a robust spread
    (Koenker 2005): c = s (z_{theta+h} - z_{theta-h}), s = MAD of the residuals / 0.6745."""
    z = stats.norm.ppf(theta)
    h = T ** (-1 / 3) * stats.norm.ppf(0.975) ** (2 / 3) * (1.5 * stats.norm.pdf(z) ** 2 / (2 * z ** 2 + 1)) ** (1 / 3)
    h = min(h, theta * 0.99)
    s = np.median(np.abs(resid - np.median(resid))) / 0.6745
    return s * (stats.norm.ppf(theta + h) - stats.norm.ppf(theta - h))


def caviar_se(fit, y, G=10.0):
    """EM (2004), asymptotic covariance: Var(b) = theta(1 - theta) D^{-1} A D^{-1} / T, A = T^{-1} sum grad grad',
    D = (2 T c)^{-1} sum 1{|y_t - q_t| < c} grad grad' (uniform kernel)."""
    y = np.asarray(y, float)
    spec, theta, f1 = fit['spec'], fit['theta'], fit['f1']
    fun = lambda b: -caviar_var(spec, b, y, theta, f1, G)[:-1]          # the quantile q_t
    q = fun(fit['b'])
    g = num_grad_path(fun, fit['b'])
    T = len(y)
    res = y - q
    c = qr_bandwidth(T, theta, res)
    A = g.T @ g / T
    k = (np.abs(res) < c).astype(float)
    Dm = (g * k[:, None]).T @ g / (2 * T * c)
    Di = np.linalg.pinv(Dm)
    V = theta * (1 - theta) * Di @ A @ Di / T
    return np.sqrt(np.diag(V)), {'c': c, 'D': Dm, 'grad': g, 'q': q}


def dq_test(y, q, theta, lags=4, extra=None):
    """Out-of-sample DQ test (EM 2004): Hit_t = 1{y_t < q_t} - theta regressed on a constant, `lags`
    lagged hits and the quantile forecast; DQ = Hit'X(X'X)^{-1}X'Hit / (theta(1 - theta)) ~ chi2(lags + 2)."""
    y, q = np.asarray(y, float), np.asarray(q, float)
    hit = (y < q).astype(float) - theta
    X = [np.ones(len(hit) - lags)] + [hit[lags - j:len(hit) - j] for j in range(1, lags + 1)] + [q[lags:]]
    if extra is not None:
        X.append(np.asarray(extra, float)[lags:])
    X = np.column_stack(X)
    H = hit[lags:]
    b = np.linalg.lstsq(X, H, rcond=None)[0]
    stat = float(b @ X.T @ X @ b / (theta * (1 - theta)))
    return stat, float(stats.chi2.sf(stat, X.shape[1]))


# =============================================================================
# SEMIPARAMETRIC (VaR, ES) MODELS: PATTON, ZIEGEL AND CHEN (2019)
# =============================================================================
@njit(cache=True, error_model="numpy")
def _ind(y, v, tau):
    if tau <= 0:
        return 1.0 if y <= v else 0.0
    x = tau * (y - v)
    if x > 700:
        return 0.0
    return 1.0 / (1.0 + np.exp(x))


@njit(cache=True, error_model="numpy")
def fz_paths(model, p, y, a, tau, init):
    """(v_t, e_t) paths of length T + 1 for model 0 GAS-2F (eq. 9-16), 1 GAS-1F (eq. 17-20), 2 GARCH-FZ (eq. 25-26,
    omega = 1), 3 Hybrid (eq. 27, omega = 0). tau > 0 replaces the indicator by the logistic function of PZC eq. 64."""
    T = y.shape[0]
    v = np.empty(T + 1)
    e = np.empty(T + 1)
    if model == 0:
        wv, we, bv, be, avv, ave, aev, aee = p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7]
        v[0], e[0] = init[0], init[1]
        for t in range(T):
            I = _ind(y[t], v[t], tau)
            lv = -v[t] * (I - a)
            le = I * y[t] / a - e[t]
            v[t + 1] = wv + bv * v[t] + avv * lv + ave * le
            e[t + 1] = we + be * e[t] + aev * lv + aee * le
    elif model == 1:
        beta, gamma, aa, bb = p[0], p[1], p[2], p[3]
        k = init[0]
        for t in range(T + 1):
            ek = np.exp(k)
            v[t], e[t] = aa * ek, bb * ek
            if t < T:
                I = _ind(y[t], v[t], tau)
                k = beta * k + gamma * (-1.0 / e[t]) * (I * y[t] / a - e[t])
    elif model == 2:
        beta, gamma, aa, bb = p[0], p[1], p[2], p[3]
        k2 = init[0]
        for t in range(T + 1):
            s = np.sqrt(k2)
            v[t], e[t] = aa * s, bb * s
            if t < T:
                k2 = 1.0 + beta * k2 + gamma * y[t] * y[t]
    else:
        beta, gamma, delta, aa, bb = p[0], p[1], p[2], p[3], p[4]
        k = init[0]
        for t in range(T + 1):
            ek = np.exp(k)
            v[t], e[t] = aa * ek, bb * ek
            if t < T:
                I = _ind(y[t], v[t], tau)
                ay = abs(y[t])
                k = beta * k + gamma * (-1.0 / e[t]) * (I * y[t] / a - e[t]) + delta * np.log(ay if ay > 1e-4 else 1e-4)
    return v, e


FZ_MODELS = {'FZ-2F': 0, 'FZ-1F': 1, 'GCH-FZ': 2, 'Hybrid': 3}
FZ_NPAR = {0: 8, 1: 4, 2: 4, 3: 5}


def fz_init(model, p, y_in, a):
    """Starting state: GAS-2F the in-sample sample VaR and ES; GAS-1F kappa = 0; GARCH-FZ the unconditional
    kappa^2 = (1 + gamma s^2)/(1 - beta); Hybrid kappa = delta E log|y| / (1 - beta)."""
    y_in = np.asarray(y_in, float)
    if model == 0:
        q = np.quantile(y_in, a)
        return np.array([q, y_in[y_in <= q].mean()])
    if model == 1:
        return np.array([0.0])
    if model == 2:
        return np.array([(1 + p[1] * np.mean(y_in ** 2)) / max(1 - p[0], 1e-3)])
    return np.array([p[2] * np.mean(np.log(np.maximum(np.abs(y_in), 1e-4))) / max(1 - p[0], 1e-3)])


def fz_valid(model, p):
    if model == 0:
        return abs(p[2]) < 1 and abs(p[3]) < 1
    if model in (1, 3):
        return 0 <= p[0] < 1 and p[-1] < p[-2] < 0
    return 0 <= p[0] < 1 and p[1] >= 0 and p[3] < p[2] < 0


def fz_objective(p, model, y, a, tau, init_y):
    """Average (smoothed if tau > 0) FZ0 loss of a semiparametric model on y; large value if inadmissible."""
    if not fz_valid(model, p):
        return 1e6
    v, e = fz_paths(model, np.asarray(p, float), y, a, tau, fz_init(model, p, init_y, a))
    v, e = v[:-1], e[:-1]
    if not (np.all(np.isfinite(e)) and np.all(e < 0) and np.all(e <= v + 1e-12)):
        return 1e6
    if tau > 0:
        I = 1.0 / (1.0 + np.exp(np.clip(tau * (y - v), -700, 700)))
    else:
        I = (y <= v).astype(float)
    L = -I * (v - y) / (a * e) + v / e + np.log(-e) - 1.0
    m = float(np.mean(L))
    return m if np.isfinite(m) else 1e6


def fz_candidates(model, y, a, n, rng):
    """Random dynamic parameters; (a, b) or (w) matched to the in-sample VaR and ES so every candidate is sensible."""
    q = np.quantile(y, a)
    m = y[y <= q].mean()
    out = []
    for _ in range(n):
        if model == 0:
            bv, be = rng.uniform(0.85, 0.995, 2)
            p = np.array([q * (1 - bv), m * (1 - be), bv, be, *rng.uniform(-0.02, 0.02, 2), *rng.uniform(-0.02, 0.02, 2)])
        elif model == 1:
            p = np.array([rng.uniform(0.8, 0.999), rng.uniform(-0.05, 0.02), q, m])
        elif model == 2:
            beta, gamma = rng.uniform(0.7, 0.98), rng.uniform(0.005, 0.2)
            k2 = (1 + gamma * np.mean(y ** 2)) / (1 - beta)
            p = np.array([beta, gamma, q / np.sqrt(k2), m / np.sqrt(k2)])
        else:
            beta, gamma, delta = rng.uniform(0.8, 0.995), rng.uniform(-0.05, 0.02), rng.uniform(0.0, 0.05)
            kbar = delta * np.mean(np.log(np.maximum(np.abs(y), 1e-4))) / (1 - beta)
            p = np.array([beta, gamma, delta, q / np.exp(kbar), m / np.exp(kbar)])
        out.append(p)
    return out


def fz_fit(name, y, a, n_rand=400, n_best=4, seed=2026):
    """FZ0 minimisation with the schedule of PZC Appendix C: smoothed loss with tau = 5 (quasi-Newton), then tau = 20,
    then the exact loss with the simplex; from the best random starting values."""
    model = FZ_MODELS[name]
    y = np.asarray(y, float)
    rng = np.random.default_rng(seed)
    cands = fz_candidates(model, y, a, n_rand, rng)
    obj = np.array([fz_objective(c, model, y, a, 0.0, y) for c in cands])
    best = (np.inf, None)
    for i in np.argsort(obj)[:n_best]:
        x = cands[i]
        for tau in (5.0, 20.0):
            r = optimize.minimize(fz_objective, x, args=(model, y, a, tau, y), method='BFGS', options={'maxiter': 400})
            if r.fun < 1e5:
                x = r.x
        for _ in range(3):
            r = optimize.minimize(fz_objective, x, args=(model, y, a, 0.0, y), method='Nelder-Mead',
                                  options={'maxiter': 6000, 'xatol': 1e-8, 'fatol': 1e-10})
            x = r.x
        if r.fun < best[0]:
            best = (r.fun, x)
    return {'name': name, 'model': model, 'p': best[1], 'loss': best[0], 'a': a}


def fz_forecast(fit, y_full, n_in):
    """(v, e) for the whole series with the parameters fixed at their in-sample values (PZC design); element t is the
    forecast of y_t made at t - 1."""
    y = np.asarray(y_full, float)
    model, p, a = fit['model'], np.asarray(fit['p'], float), fit['a']
    v, e = fz_paths(model, p, y, a, 0.0, fz_init(model, p, y[:n_in], a))
    return v[:-1], e[:-1]


def es_regression(y, X, a, n_starts=6, seed=2026):
    """Joint linear (VaR, ES) regression q_t = x_t'b, e_t = x_t'g (Dimitriadis and Bayer 2019) by FZ0 minimisation;
    starting values from a quantile regression and a regression of the tail returns."""
    import statsmodels.api as sm
    y, X = np.asarray(y, float), np.asarray(X, float)
    k = X.shape[1]
    b0 = sm.QuantReg(y, X).fit(q=a).params
    qv = X @ b0
    sel = y <= qv
    g0 = np.linalg.lstsq(X[sel], y[sel], rcond=None)[0]

    def obj(p):
        v, e = X @ p[:k], X @ p[k:]
        if np.any(e >= 0) or np.any(e > v):
            return 1e6
        return float(np.mean(fz0(y, v, e, a)))
    rng = np.random.default_rng(seed)
    best = None
    for s in range(n_starts):
        x0 = np.concatenate([b0, g0]) * (1 + (0.1 * rng.standard_normal(2 * k) if s else 0))
        r = optimize.minimize(obj, x0, method='Nelder-Mead', options={'maxiter': 20000, 'xatol': 1e-9, 'fatol': 1e-12})
        if best is None or r.fun < best.fun:
            best = r
    return best.x[:k], best.x[k:], best.fun, b0


# =============================================================================
# BACKTESTS
# =============================================================================
def kupiec(hits, a):
    """Unconditional coverage LR test (Kupiec 1995), chi2(1)."""
    h = np.asarray(hits, float)
    n, x = len(h), h.sum()
    pi = x / n
    ll0 = x * np.log(a) + (n - x) * np.log(1 - a)
    ll1 = (x * np.log(pi) if x > 0 else 0) + ((n - x) * np.log(1 - pi) if x < n else 0)
    lr = -2 * (ll0 - ll1)
    return lr, float(stats.chi2.sf(lr, 1))


def christoffersen(hits, a):
    """Independence and conditional coverage LR tests (Christoffersen 1998): chi2(1) and chi2(2)."""
    h = np.asarray(hits, int)
    h0, h1 = h[:-1], h[1:]
    n00, n01 = np.sum((h0 == 0) & (h1 == 0)), np.sum((h0 == 0) & (h1 == 1))
    n10, n11 = np.sum((h0 == 1) & (h1 == 0)), np.sum((h0 == 1) & (h1 == 1))
    p01 = n01 / max(n00 + n01, 1)
    p11 = n11 / max(n10 + n11, 1)
    p = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    xl = lambda k, q: k * np.log(q) if k > 0 else 0.0
    l0 = xl(n00 + n10, 1 - p) + xl(n01 + n11, p)
    l1 = xl(n00, 1 - p01) + xl(n01, p01) + xl(n10, 1 - p11) + xl(n11, p11)
    lr_ind = -2 * (l0 - l1)
    lr_uc = kupiec(h[1:], a)[0]
    lr_cc = lr_uc + lr_ind
    return {'ind': lr_ind, 'p_ind': float(stats.chi2.sf(lr_ind, 1)), 'cc': lr_cc, 'p_cc': float(stats.chi2.sf(lr_cc, 2))}


def durations(hits):
    """Durations between hits with the censoring flags of Christoffersen and Pelletier (2004): the first spell is
    left-censored if the sample does not start with a hit, the last right-censored if it does not end with one."""
    h = np.asarray(hits, int)
    idx = np.flatnonzero(h)
    if len(idx) == 0:
        return np.array([len(h)]), np.array([1]), np.array([1])
    d = np.diff(np.concatenate([[-1], idx]))
    cl = np.zeros(len(d), int)
    cr = np.zeros(len(d), int)
    if h[0] == 0:
        cl[0] = 1
    if h[-1] == 0:
        d = np.append(d, len(h) - 1 - idx[-1])
        cl = np.append(cl, 0)
        cr = np.append(cr, 1)
    return d.astype(float), cl, cr


def cp_duration_test(hits):
    """Duration-based test of Christoffersen and Pelletier (2004): Weibull hazard lambda(d) = a^b b d^(b-1) against the
    memoryless exponential (b = 1); censored first and last spells; LR ~ chi2(1)."""
    d, cl, cr = durations(hits)

    def ll(p):
        aa, bb = np.exp(p[0]), np.exp(p[1])
        logf = bb * np.log(aa) + np.log(bb) + (bb - 1) * np.log(d) - (aa * d) ** bb
        logS = -(aa * d) ** bb
        c = (cl + cr) > 0
        return -np.sum(np.where(c, logS, logf))
    r1 = optimize.minimize(ll, [np.log(1 / d.mean()), 0.0], method='Nelder-Mead', options={'xatol': 1e-9, 'fatol': 1e-10})
    r0 = optimize.minimize_scalar(lambda la: ll([la, 0.0]), bounds=(-15, 5), method='bounded')
    lr = 2 * (r0.fun - r1.fun)
    lr = max(lr, 0.0)
    return lr, float(stats.chi2.sf(lr, 1)), float(np.exp(r1.x[1]))


def ols_wald(yv, X, hc=True):
    """Wald test that all coefficients are zero in an OLS regression; HC0 covariance (White) by default."""
    b = np.linalg.lstsq(X, yv, rcond=None)[0]
    u = yv - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    S = (X * (u ** 2)[:, None]).T @ X if hc else (u @ u / (len(u) - X.shape[1])) * (X.T @ X)
    V = XtXi @ S @ XtXi
    w = float(b @ np.linalg.solve(V, b))
    return w, float(stats.chi2.sf(w, X.shape[1])), b


def pzc_gof(y, v, e, a):
    """Goodness-of-fit regressions of PZC (eq. 40-41): standardised generalised residuals
    lam_v = 1{y <= v} - a and lam_e = 1{y <= v} y / (a e) - 1 on (1, own lag, v_t) or (1, own lag, e_t); Wald tests."""
    y, v, e = map(lambda z: np.asarray(z, float), (y, v, e))
    I = (y <= v).astype(float)
    lv = I - a
    le = I * y / (a * e) - 1
    Xv = np.column_stack([np.ones(len(y) - 1), lv[:-1], v[1:]])
    Xe = np.column_stack([np.ones(len(y) - 1), le[:-1], e[1:]])
    wv, pv, _ = ols_wald(lv[1:], Xv)
    we, pe, _ = ols_wald(le[1:], Xe)
    return {'W_var': wv, 'p_var': pv, 'W_es': we, 'p_es': pe}


def mcneil_frey(y, v, e, sigma, B=2000, seed=2026):
    """McNeil and Frey (2000): exceedance residuals r_t = (y_t - e_t)/sigma_t on the days y_t <= v_t; H0 mean zero
    against mean < 0 (ES underestimated in magnitude); bootstrap p-value of the centred residuals."""
    y, v, e, sigma = map(lambda z: np.asarray(z, float), (y, v, e, sigma))
    r = ((y - e) / sigma)[y <= v]
    if len(r) < 3:
        return np.nan, np.nan, len(r)
    t0 = r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))
    rng = np.random.default_rng(seed)
    rc = r - r.mean()
    bs = rng.choice(rc, size=(B, len(rc)), replace=True)
    tb = bs.mean(axis=1) / (bs.std(axis=1, ddof=1) / np.sqrt(len(rc)))
    return float(t0), float((tb <= t0).mean()), len(r)


# =============================================================================
# FORECAST COMPARISON
# =============================================================================
def nw_lrv(d, lags=None):
    d = np.asarray(d, float) - np.mean(d)
    T = len(d)
    L = int(np.floor(4 * (T / 100) ** (2 / 9))) if lags is None else lags
    s = d @ d / T
    for j in range(1, L + 1):
        s += 2 * (1 - j / (L + 1)) * (d[j:] @ d[:-j]) / T
    return s


def dm_test(l1, l2, lags=None):
    """Diebold-Mariano t statistic of mean(l1 - l2) with a Newey-West long-run variance (Bartlett kernel,
    4(T/100)^(2/9) lags); positive: model 1 has the larger loss."""
    d = np.asarray(l1, float) - np.asarray(l2, float)
    t = d.mean() / np.sqrt(nw_lrv(d, lags) / len(d))
    return float(t), float(2 * stats.norm.sf(abs(t)))


def mcs(L, names, alpha=0.10, B=1000, block=10, seed=2026):
    """Model confidence set (Hansen, Lunde and Nason 2011), T_max statistic, moving-block bootstrap; returns the MCS
    p-value of every model and the set at level alpha."""
    L = np.asarray(L, float)
    T, m = L.shape
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / block))
    starts = rng.integers(0, T - block + 1, size=(B, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(B, -1)[:, :T]
    Lb = np.stack([L[i].mean(axis=0) for i in idx])
    alive = list(range(m))
    pv, run = {}, 0.0
    while len(alive) > 1:
        Lm = L[:, alive].mean(axis=0)
        dbar = Lm - Lm.mean()
        db = Lb[:, alive] - Lb[:, alive].mean(axis=1, keepdims=True)
        se = np.sqrt(((db - dbar) ** 2).mean(axis=0))
        t = dbar / se
        tb = ((db - dbar) / se).max(axis=1)
        run = max(run, float((tb > t.max()).mean()))
        worst = alive[int(np.argmax(t))]
        pv[worst] = run
        alive.remove(worst)
    pv[alive[0]] = 1.0
    out = {names[i]: pv[i] for i in range(m)}
    return {'p': out, 'set': [n for n in names if out[n] >= alpha]}


# =============================================================================
# EXTREMES AND CONFORMAL CALIBRATION
# =============================================================================
def extremal_index(x, u):
    """Intervals estimator of the extremal index (Ferro and Segers 2003) for exceedances of x over u."""
    idx = np.flatnonzero(np.asarray(x) > u)
    if len(idx) < 3:
        return np.nan
    Ti = np.diff(idx).astype(float)
    N = len(idx)
    if Ti.max() <= 2:
        th = 2 * Ti.sum() ** 2 / ((N - 1) * (Ti ** 2).sum())
    else:
        th = 2 * (Ti - 1).sum() ** 2 / ((N - 1) * ((Ti - 1) * (Ti - 2)).sum())
    return float(min(1.0, th))


def aci_levels(hits_fn, a, gamma, T):
    """Adaptive conformal inference (Gibbs and Candes 2021): a_{t+1} = a_t + gamma (a - err_t); hits_fn(t, a_t)
    returns err_t = 1 if day t's return falls below the quantile forecast at level a_t."""
    at = np.empty(T + 1)
    at[0] = a
    err = np.empty(T)
    for t in range(T):
        err[t] = hits_fn(t, at[t])
        at[t + 1] = at[t] + gamma * (a - err[t])
    return at, err
