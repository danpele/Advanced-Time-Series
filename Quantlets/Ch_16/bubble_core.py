"""
bubble_core.py -- the engine of Chapter 16 (ATS): explosive roots, bubble tests, monitoring, LPPLS, evaluation
==============================================================================================================
numpy, scipy and statsmodels only; every routine is written out so that the Quantlets and the notebooks are
self-contained (the code is copied into them with inspect.getsource).
  * right-tailed ADF on all windows (OLS by cumulative sums, vectorised over start points and replications):
    adf_window, psy (ADF, SADF, GSADF, BSADF), bsadf_paths, psy_cv (Monte Carlo under a random walk with a weak
    drift), wild_cv (wild bootstrap, Rademacher signs), episodes (date-stamping with a minimum duration);
  * simulated bubbles: Blanchard-Watson, Evans (1991) periodically collapsing bubbles with a present-value
    fundamental, the bubble-and-collapse process used for date-stamping experiments, explosive AR(1) samples;
  * monitoring: the boundary-crossing constant of Chu, Stinchcombe and White (1996) and a CUSUM monitor of returns;
  * LPPLS: the Filimonov-Sornette calibration, the filter of Shu and Zhu (2020), the confidence indicator, the
    profile likelihood of the critical time;
  * evaluation: future drawdowns, ROC curves and AUC, a moving-block bootstrap.
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import numpy as np
import pandas as pd
from scipy import optimize, stats


# =============================================================================
# 1. RIGHT-TAILED ADF ON WINDOWS: ADF, SADF, GSADF, BSADF
#    regression Delta y_t = a + delta y_{t-1} + e_t on a window, no lagged differences; H1: delta > 0
# =============================================================================
def _cums(y):
    """Cumulative sums for the regression Delta y_t = a + delta y_{t-1} (rows t = 1..n); y is (n+1,) or (R, n+1)."""
    y = np.atleast_2d(np.asarray(y, float))
    x, z = y[:, :-1], np.diff(y, axis=1)
    pad = lambda a: np.concatenate([np.zeros((a.shape[0], 1)), np.cumsum(a, axis=1)], axis=1)   # noqa: E731
    return pad(x), pad(x * x), pad(z), pad(z * z), pad(x * z)


def _adf_end(C, e, s):
    """t-statistic of delta on the windows [s, e] (s: vector of first rows, e: last row), for every replication."""
    Sx, Sxx, Sz, Szz, Sxz = (c[:, e + 1][:, None] - c[:, s] for c in C)
    n = (e + 1 - s).astype(float)
    den = n * Sxx - Sx ** 2
    b = (n * Sxz - Sx * Sz) / den
    a = (Sz - b * Sx) / n
    ssr = np.maximum(Szz - a * Sz - b * Sxz, 1e-300)
    return b / np.sqrt(ssr / (n - 2) * n / den)


def adf_window(y):
    """Right-tailed ADF on one window: intercept a, slope delta, its standard error and the t-statistic."""
    y = np.asarray(y, float)
    x, z = y[:-1], np.diff(y)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, z, rcond=None)
    e = z - X @ beta
    s2 = e @ e / (len(z) - 2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    return dict(a=float(beta[0]), delta=float(beta[1]), se=float(se), t=float(beta[1] / se), n=len(z))


def min_window(T, r0=None):
    """Smallest window of Phillips, Shi and Yu (2015): r0 = 0.01 + 1.8 / sqrt(T); w0 = floor(r0 T)."""
    r0 = 0.01 + 1.8 / np.sqrt(T) if r0 is None else r0
    return int(np.floor(r0 * T)), float(r0)


def _lag_design(y, k):
    """Rows t = k+1..n of the ADF regression with k lagged differences: z_t = Delta y_t,
    x_t = (1, y_{t-1}, Delta y_{t-1}, ..., Delta y_{t-k}); y is (R, n+1)."""
    dy = np.diff(y, axis=1)
    n = dy.shape[1]
    cols = [np.ones_like(dy[:, k:]), y[:, k:n]] + [dy[:, k - j:n - j] for j in range(1, k + 1)]
    return np.stack(cols, axis=2), dy[:, k:]


def _bsadf_lags(Y, w0, k, chunk=16):
    """BSADF and forward sequences with k lagged differences (cumulated cross-products, batched solves); entries
    before row k + w0 are NaN; the output has n columns like the k = 0 version."""
    R, n = Y.shape[0], Y.shape[1] - 1
    bs, fw = np.full((R, n), np.nan), np.full((R, n), np.nan)
    for i in range(0, R, chunk):
        X, z = _lag_design(Y[i:i + chunk], k)
        m, p = X.shape[1], X.shape[2]
        pad = lambda a: np.concatenate([np.zeros((a.shape[0], 1) + a.shape[2:]), np.cumsum(a, axis=1)], axis=1)   # noqa: E731
        CXX = pad(np.einsum('rti,rtj->rtij', X, X))
        CXz = pad(X * z[:, :, None])
        Czz = pad(z * z)
        for e in range(w0 - 1, m):
            s_ = np.arange(0, e - w0 + 2)
            XX = CXX[:, e + 1][:, None] - CXX[:, s_]
            Xz = CXz[:, e + 1][:, None] - CXz[:, s_]
            zz = Czz[:, e + 1][:, None] - Czz[:, s_]
            inv = np.linalg.inv(XX)
            b = np.einsum('rsij,rsj->rsi', inv, Xz)
            ssr = np.maximum(zz - np.einsum('rsi,rsi->rs', b, Xz), 1e-300)
            nn = (e + 1 - s_)[None, :]
            t = b[..., 1] / np.sqrt(ssr / (nn - p) * inv[..., 1, 1])
            bs[i:i + chunk, e + k] = t.max(axis=1)
            fw[i:i + chunk, e + k] = t[:, 0]
    return bs, fw


def psy(y, r0=None, w0=None, k=0):
    """ADF (whole sample), SADF (sup of forward-expanding ADF), GSADF (sup over start and end points), the BSADF
    sequence (sup over start points for each end point) and the start point that attains it (k = 0); k > 0 adds k
    lagged differences to every window regression."""
    y = np.asarray(y, float)
    n = len(y) - 1
    if w0 is None:
        w0, r0 = min_window(n, r0)
    if k:
        bs, fw = _bsadf_lags(y[None, :], w0, k)
        return dict(adf=float(fw[0, -1]), sadf=float(np.nanmax(fw)), gsadf=float(np.nanmax(bs)), bsadf=bs[0], fwd=fw[0],
                    w0=int(w0), r0=r0, n=n, k=k)
    C = _cums(y)
    bsadf, fwd, arg = np.full(n, np.nan), np.full(n, np.nan), np.full(n, -1)
    for e in range(w0 - 1, n):
        stat = _adf_end(C, e, np.arange(0, e - w0 + 2))[0]
        bsadf[e], fwd[e], arg[e] = stat.max(), stat[0], int(np.argmax(stat))
    return dict(adf=float(fwd[-1]), sadf=float(np.nanmax(fwd)), gsadf=float(np.nanmax(bsadf)), bsadf=bsadf, fwd=fwd,
                start=arg, w0=int(w0), r0=r0, n=n, k=0)


def bsadf_paths(Y, w0, chunk=64, k=0):
    """BSADF and forward (SADF) sequences for several paths (rows of Y), vectorised over start points and paths."""
    Y = np.atleast_2d(np.asarray(Y, float))
    if k:
        return _bsadf_lags(Y, w0, k)
    R, n = Y.shape[0], Y.shape[1] - 1
    bs, fw = np.full((R, n), np.nan), np.full((R, n), np.nan)
    for i in range(0, R, chunk):
        C = _cums(Y[i:i + chunk])
        for e in range(w0 - 1, n):
            stat = _adf_end(C, e, np.arange(0, e - w0 + 2))
            bs[i:i + chunk, e] = stat.max(axis=1)
            fw[i:i + chunk, e] = stat[:, 0]
    return bs, fw


def bic_lag(y, kmax):
    """Lag order of the null model Delta y_t = mu + sum_j phi_j Delta y_{t-j} + e_t chosen by BIC (common sample)."""
    dy = np.diff(np.asarray(y, float))
    z = dy[kmax:]
    best = (np.inf, 0)
    for k in range(kmax + 1):
        X = np.column_stack([np.ones_like(z)] + [dy[kmax - j:len(dy) - j] for j in range(1, k + 1)])
        e = z - X @ np.linalg.lstsq(X, z, rcond=None)[0]
        bic = len(z) * np.log(e @ e / len(z)) + (k + 1) * np.log(len(z))
        best = min(best, (bic, k))
    return best[1]


def null_paths(T, R, rng, sig=None):
    """Random walk with a weak drift, y_t = T^(-1) + y_{t-1} + sig_t e_t (PSY 2015); sig: optional volatility path."""
    e = rng.standard_normal((R, T)) * (1.0 if sig is None else np.asarray(sig)[None, :])
    return np.concatenate([np.zeros((R, 1)), np.cumsum(1.0 / T + e, axis=1)], axis=1)


def psy_cv(T, w0, R=2000, seed=2026, probs=(0.90, 0.95, 0.99)):
    """Monte Carlo critical values under the null: quantiles of ADF, SADF and GSADF, the pointwise 95% quantile of
    BSADF at each end point, and the null draws."""
    rng = np.random.default_rng(seed)
    bs, fw = bsadf_paths(null_paths(T, R, rng), w0)
    q = lambda a: {f'{int(round(100 * p))}': float(np.quantile(a, p)) for p in probs}   # noqa: E731
    return dict(adf=q(fw[:, -1]), sadf=q(np.nanmax(fw, axis=1)), gsadf=q(np.nanmax(bs, axis=1)),
                bsadf95=np.nanquantile(bs, 0.95, axis=0), draws=dict(gsadf=np.nanmax(bs, axis=1), sadf=np.nanmax(fw, axis=1),
                                                                    adf=fw[:, -1]), bs=bs)


def wild_cv(y, w0, B=499, seed=2026, tau=None, k=0):
    """Wild bootstrap of Phillips and Shi (2020): residuals of the null model Delta y_t = mu + sum_j phi_j Delta y_{t-j}
    + e_t times Rademacher signs, Delta y*_t = sum_j phi_j Delta y*_{t-j} + w_t e_t, cumulated into paths with a unit
    root and the volatility pattern of the data. Returns the pointwise 95% BSADF sequence, the 95% quantile of the
    sample maximum (GSADF: family-wise over the whole sample) and, when tau is given, for every end point the 95%
    quantile of the maximum of BSADF over the last tau end points (family-wise over a moving window)."""
    rng = np.random.default_rng(seed)
    dy = np.diff(np.asarray(y, float))
    if k:
        X = np.column_stack([np.ones(len(dy) - k)] + [dy[k - j:len(dy) - j] for j in range(1, k + 1)])
        phi = np.linalg.lstsq(X, dy[k:], rcond=None)[0]
        e = dy[k:] - X @ phi
        W = rng.choice([-1.0, 1.0], size=(B, len(e)))
        D = np.zeros((B, len(dy)))
        D[:, :k] = dy[:k] - dy.mean()
        for t in range(k, len(dy)):
            D[:, t] = sum(phi[j] * D[:, t - j] for j in range(1, k + 1)) + W[:, t - k] * e[t - k]
    else:
        e = dy - dy.mean()
        D = rng.choice([-1.0, 1.0], size=(B, len(e))) * e
    Y = np.concatenate([np.zeros((B, 1)), np.cumsum(D, axis=1)], axis=1)
    bs, fw = bsadf_paths(Y, w0, k=k)
    out = dict(bsadf95=np.nanquantile(bs, 0.95, axis=0), gsadf95=float(np.quantile(np.nanmax(bs, axis=1), 0.95)),
               sadf95=float(np.quantile(np.nanmax(fw, axis=1), 0.95)), draws=np.nanmax(bs, axis=1))
    if tau:
        roll = pd.DataFrame(bs.T).rolling(tau, min_periods=1).max().values.T
        out['fwer95'] = np.nanquantile(roll, 0.95, axis=0)
    return out


def episodes(stat, cv, index, min_len):
    """Date-stamping: runs of at least min_len consecutive end points with stat > cv (cv scalar or sequence).
    Returns (start, end, length); the start is dated at the first exceedance, the end at the last one."""
    stat = np.asarray(stat, float)
    cv = np.broadcast_to(np.asarray(cv, float), stat.shape)
    above = (stat > cv) & ~np.isnan(stat) & ~np.isnan(cv)
    out, i, n = [], 0, len(above)
    while i < n:
        if above[i]:
            j = i
            while j + 1 < n and above[j + 1]:
                j += 1
            if j - i + 1 >= min_len:
                out.append((index[i], index[j], int(j - i + 1)))
            i = j + 1
        else:
            i += 1
    return out


def weekly(s):
    """Weekly log price: last close of each week (Friday)."""
    return np.log(s.resample('W-FRI').last().dropna())


# =============================================================================
# 2. SIMULATED BUBBLES AND EXPLOSIVE AUTOREGRESSIONS
# =============================================================================
def blanchard_watson(T=400, r=0.02, pi=0.98, b0=1.0, sd=0.3, seed=13):
    """Blanchard-Watson bubble: with probability pi it survives and grows by (1 + r)/pi, otherwise it bursts to
    noise; E_t[b_{t+1}] = (1 + r) b_t."""
    rng = np.random.default_rng(seed)
    b = np.empty(T)
    b[0] = b0
    for t in range(1, T):
        eps = sd * rng.standard_normal()
        b[t] = (1 + r) / pi * b[t - 1] + eps if rng.random() < pi else eps
    return b


def evans_price(T=400, r=0.05, alpha=1.0, delta=0.5, pi=0.85, tau=0.05, mu=0.0373, sd=0.3967, d0=1.3, scale=20.0,
                seed=11):
    """Price = present-value fundamental + scale * Evans (1991) bubble. Dividends: random walk with drift mu, so the
    fundamental is P^f_t = mu (1 + r) / r^2 + D_t / r. The bubble grows at 1 + r while B <= alpha; above alpha it
    survives with probability pi (growing faster) or collapses to delta; u_t lognormal with mean 1."""
    rng = np.random.default_rng(seed)
    D = d0 + np.cumsum(mu + sd * rng.standard_normal(T))
    pf = mu * (1 + r) / r ** 2 + D / r
    u = np.exp(rng.normal(-0.5 * tau ** 2, tau, T))
    B = np.empty(T)
    B[0] = delta
    for t in range(1, T):
        if B[t - 1] <= alpha:
            B[t] = (1 + r) * B[t - 1] * u[t]
        else:
            theta = rng.random() < pi
            B[t] = (delta + (1 + r) / pi * (B[t - 1] - delta / (1 + r)) * theta) * u[t]
    return pf, scale * B


def bubble_collapse(T, te, tf, rho, y0=100.0, sd=1.0, rng=None):
    """Random walk up to te, explosive y_t = rho y_{t-1} + e_t on (te, tf], collapse at tf + 1 back to the level of
    te, random walk afterwards (the bubble-and-collapse process used for date-stamping experiments)."""
    rng = rng or np.random.default_rng()
    e = sd * rng.standard_normal(T + 1)
    y = np.empty(T + 1)
    y[0] = y0
    for t in range(1, T + 1):
        if t <= te:
            y[t] = y[t - 1] + e[t]
        elif t <= tf:
            y[t] = rho * y[t - 1] + e[t]
        elif t == tf + 1:
            y[t] = y[te] + e[t]
        else:
            y[t] = y[t - 1] + e[t]
    return y


def ar1_explosive(n, rho, R, rng, dist='normal'):
    """R samples y_1..y_n of y_t = rho y_{t-1} + u_t, y_0 = 0; u_t standard normal or centred exponential."""
    u = rng.standard_normal((R, n)) if dist == 'normal' else rng.exponential(1.0, (R, n)) - 1.0
    y = np.zeros((R, n + 1))
    for t in range(1, n + 1):
        y[:, t] = rho * y[:, t - 1] + u[:, t - 1]
    return y


def ols_rho(y):
    """OLS of y_t on y_{t-1} without intercept, row by row."""
    x, z = y[:, :-1], y[:, 1:]
    return (x * z).sum(axis=1) / (x * x).sum(axis=1)


# =============================================================================
# 3. MONITORING: CUSUM WITH THE CHU-STINCHCOMBE-WHITE BOUNDARY
# =============================================================================
def csw_constant(alpha=0.05):
    """One-sided boundary-crossing constant: P{W(s) >= sqrt((s + 1)(a^2 + ln(s + 1))) for some s >= 0}
    = 1 - Phi(a) + a phi(a) (Robbins-Siegmund); solve for a at level alpha."""
    f = lambda a: 1 - stats.norm.cdf(a) + a * stats.norm.pdf(a) - alpha   # noqa: E731
    return float(optimize.brentq(f, 0.5, 6.0))


def cusum_monitor(r, n, alpha=0.05):
    """CUSUM monitoring of the mean of returns r after a training sample of n observations:
    S_t = sum_{j=n+1}^t (r_j - mean_n) / (sigma_n sqrt(n)) with the Chu-Stinchcombe-White boundary
    b_t = sqrt(((t - n)/n)(t/n)(a^2 + ln(t/(t - n)))), which S crosses under the null with probability alpha
    (one-sided, over an infinite horizon). Returns S, b and the first crossing (index in r, or None)."""
    r = np.asarray(r, float)
    mu, sig = r[:n].mean(), r[:n].std(ddof=1)
    S = np.cumsum(r[n:] - mu) / (sig * np.sqrt(n))
    t = np.arange(n + 1, len(r) + 1)
    a = csw_constant(alpha)
    b = np.sqrt((t - n) / n * t / n * (a ** 2 + np.log(t / (t - n))))
    hit = np.nonzero(S > b)[0]
    return S, b, (int(n + hit[0]) if len(hit) else None)


# =============================================================================
# 4. LPPLS: ln p(t) = A + B f + C1 f cos(w ln(tc - t)) + C2 f sin(w ln(tc - t)),  f = (tc - t)^m
#    calibration of Filimonov and Sornette (2013); search space and filter of Shu and Zhu (2020), eq. (11)-(12)
# =============================================================================
LPPLS_SEARCH = dict(m=(0.0, 1.0), w=(1.0, 50.0), tc_frac=(0.0, 1 / 3), damping_min=1.0)
LPPLS_FILTER = dict(m=(0.01, 0.99), w=(2.0, 25.0), tc_frac=(0.0, 1 / 5), osc_min=2.5, rel_err_max=0.15,
                    lomb_alpha=0.10, ar1_alpha=0.10)
WINDOWS = list(range(750, 45, -25))          # window lengths: 750, 725, ..., 50 observations (29 windows)


def yrs(idx):
    """Dates as decimal years (the time unit of the LPPLS fits)."""
    idx = pd.DatetimeIndex(idx)
    return np.asarray(idx.year + (idx.dayofyear - 1) / 365.25, float)


def todate(x):
    """Decimal year -> date."""
    y = int(np.floor(x))
    return pd.Timestamp(y, 1, 1) + pd.Timedelta(days=float((x - y) * 365.25))


def lppl_design(t, tc, m, w):
    dt = np.maximum(tc - np.asarray(t, float), 1e-9)
    f = dt ** m
    lg = np.log(dt)
    return np.column_stack([np.ones_like(dt), f, f * np.cos(w * lg), f * np.sin(w * lg)])


def lppl_linear(t, y, tc, m, w):
    """Linear step: for given (tc, m, omega), A, B, C1, C2 by OLS and the sum of squared residuals."""
    X = lppl_design(t, tc, m, w)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    return beta, float(res @ res)


def _damping(m, w, beta):
    C = np.hypot(beta[..., 2], beta[..., 3])
    return m * np.abs(beta[..., 1]) / (w * np.maximum(C, 1e-300))


def _grid(t, y, tcs, ms, ws):
    """SSR of the linear step on a grid of (tc, m, omega), vectorised."""
    TC, M, W = (a.ravel() for a in np.meshgrid(tcs, ms, ws, indexing='ij'))
    dt = np.maximum(TC[:, None] - t[None, :], 1e-9)
    f = dt ** M[:, None]
    lg = np.log(dt)
    X = np.stack([np.ones_like(f), f, f * np.cos(W[:, None] * lg), f * np.sin(W[:, None] * lg)], axis=2)
    XtX = np.einsum('gni,gnj->gij', X, X) + 1e-10 * np.eye(4)
    Xty = np.einsum('gni,n->gi', X, y)
    beta = np.linalg.solve(XtX, Xty[..., None])[..., 0]
    ssr = y @ y - np.einsum('gi,gi->g', beta, Xty)
    return TC, M, W, beta, ssr


def lppl_fit(t, y, search=LPPLS_SEARCH, grid=(8, 8, 16), tc_fixed=None):
    """Nonlinear step: minimum SSR over (tc, m, omega) in the search space (damping >= 1): a grid, then Nelder-Mead
    from the best grid point. With tc_fixed, only (m, omega) are free (profile of the critical time)."""
    t, y = np.asarray(t, float), np.asarray(y, float)
    t1, t2 = t[0], t[-1]
    D = t2 - t1
    lo = np.array([t2 + search['tc_frac'][0] * D + 1e-6, search['m'][0] + 1e-3, search['w'][0]])
    hi = np.array([t2 + search['tc_frac'][1] * D, search['m'][1] - 1e-3, search['w'][1]])
    if tc_fixed is not None:
        lo[0] = hi[0] = tc_fixed
    tcs = np.array([tc_fixed]) if tc_fixed is not None else np.linspace(lo[0], hi[0], grid[0])
    TC, M, W, beta, ssr = _grid(t, y, tcs, np.linspace(lo[1], hi[1], grid[1]), np.linspace(lo[2], hi[2], grid[2]))
    ok = _damping(M, W, beta) >= search['damping_min']
    if not ok.any():
        return None
    k = int(np.argmin(np.where(ok, ssr, np.inf)))
    x0 = np.array([TC[k], M[k], W[k]])
    free = slice(1, 3) if tc_fixed is not None else slice(0, 3)

    def obj(p):
        q = x0.copy()
        q[free] = p
        q = np.clip(q, lo, hi)
        b, sr = lppl_linear(t, y, *q)
        return sr if _damping(q[1], q[2], b) >= search['damping_min'] else sr + 1e6
    r = optimize.minimize(obj, x0[free], method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-10, maxiter=400))
    if r.fun < 1e6:
        x0[free] = r.x
        x0 = np.clip(x0, lo, hi)
    tc, m, w = x0
    (A, B, C1, C2), s = lppl_linear(t, y, tc, m, w)
    C = np.hypot(C1, C2)
    yhat = lppl_design(t, tc, m, w) @ np.array([A, B, C1, C2])
    return dict(tc=float(tc), m=float(m), w=float(w), A=float(A), B=float(B), C1=float(C1), C2=float(C2), C=float(C),
                ssr=float(s), damping=float(m * abs(B) / (w * C)) if C > 0 else np.inf,
                osc=float(w / np.pi * np.log((tc - t1) / (tc - t2))) if tc > t2 else 0.0,
                rel_err=float(np.max(np.abs(np.exp(yhat) - np.exp(y)) / np.exp(y))), t1=float(t1), t2=float(t2),
                n=len(t), _t=t, _y=y, _yhat=yhat)


def lomb_pvalue(fit, wmin=2.0, wmax=25.0, nw=200):
    """Lomb test of the detrended residual (tc - t)^(-m) (ln p - A - B (tc - t)^m) against ln(tc - t)."""
    from scipy.signal import lombscargle
    t, y = fit['_t'], fit['_y']
    dt = np.maximum(fit['tc'] - t, 1e-9)
    r = dt ** (-fit['m']) * (y - fit['A'] - fit['B'] * dt ** fit['m'])
    x = np.log(dt)
    r = r - r.mean()
    ws = np.linspace(wmin, wmax, nw)
    p = lombscargle(x, r, ws) / r.var()
    return float(1 - (1 - np.exp(-p.max())) ** min(nw, len(r)))


def ar1_pass(fit, alpha):
    """The residual ln p_hat - ln p is stationary: the Dickey-Fuller and Phillips-Perron tests both reject a unit
    root at level alpha (as in TSA, Chapter 13)."""
    from statsmodels.tsa.stattools import adfuller
    from arch.unitroot import PhillipsPerron
    e = fit['_yhat'] - fit['_y']
    return bool(adfuller(e, maxlag=0, autolag=None, regression='c')[1] < alpha and PhillipsPerron(e, trend='c').pvalue < alpha)


def lppl_conditions(fit, flt=LPPLS_FILTER, search=LPPLS_SEARCH):
    """Filter of Shu and Zhu (2020), eq. (12), for a positive bubble (B < 0); the Lomb test only when the parameter
    conditions and the relative error pass, the residual unit-root test only when Lomb passes."""
    if fit is None:
        return None
    D = fit['t2'] - fit['t1']
    c = dict(B=fit['B'] < 0, m=flt['m'][0] <= fit['m'] <= flt['m'][1], w=flt['w'][0] <= fit['w'] <= flt['w'][1],
             tc=fit['t2'] + flt['tc_frac'][0] * D <= fit['tc'] <= fit['t2'] + flt['tc_frac'][1] * D,
             osc=fit['osc'] >= flt['osc_min'], damping=fit['damping'] >= search['damping_min'],
             rel_err=fit['rel_err'] <= flt['rel_err_max'])
    if all(c.values()):
        c['lomb'] = lomb_pvalue(fit) <= flt['lomb_alpha']
        c['ar1'] = ar1_pass(fit, flt['ar1_alpha']) if c['lomb'] else False
    else:
        c['lomb'] = c['ar1'] = None
    return c


def qualified(c):
    return c is not None and all(v is True for v in c.values())


def ci_point(args):
    """LPPLS confidence indicator at one end point: the share of windows whose fit passes the whole filter, and the
    median critical time of the qualified fits."""
    t, y, i2, windows = args
    full, tcs = [], []
    for L in windows:
        i1 = i2 - L
        if i1 < 0:
            continue
        f = lppl_fit(t[i1:i2 + 1], y[i1:i2 + 1])
        q = qualified(lppl_conditions(f))
        full.append(q)
        if q:
            tcs.append(f['tc'])
    return (float(np.mean(full)) if full else np.nan, float(np.median(tcs)) if tcs else np.nan)


def confidence_series(s, start, end=None, step=5, windows=WINDOWS, procs=1):
    """LPPLS confidence indicator (positive bubbles) at the end points t2 in [start, end], every `step` observations;
    procs > 1 uses a process pool."""
    t, y = yrs(s.index), np.log(s.values)
    i0 = s.index.searchsorted(pd.Timestamp(start))
    i1 = len(s) if end is None else s.index.searchsorted(pd.Timestamp(end), 'right')
    jobs = [(t, y, int(i), windows) for i in range(i0, i1, step)]
    if procs == 1:
        res = [ci_point(j) for j in jobs]
    else:
        from multiprocessing import get_context
        with get_context('fork').Pool(procs) as pool:
            res = pool.map(ci_point, jobs, chunksize=4)
    return pd.DataFrame(res, index=s.index[[j[2] for j in jobs]], columns=['ci', 'tc_median'])


def tc_profile(t, y, tcs):
    """Profile log-likelihood of the critical time (Gaussian errors): for each tc, (m, omega) and the linear
    parameters are concentrated out; l(tc) = -(n/2) ln(SSR(tc)/n)."""
    out = []
    for tc in tcs:
        f = lppl_fit(t, y, search=dict(LPPLS_SEARCH, tc_frac=(0.0, 10.0)), tc_fixed=tc)
        out.append(-0.5 * len(t) * np.log(f['ssr'] / len(t)) if f is not None else np.nan)
    return np.array(out)


# =============================================================================
# 5. EVALUATION OF EARLY-WARNING SIGNALS
# =============================================================================
def future_fall(s, horizon=182):
    """For each date t: min_{t < u <= t + horizon days} p_u / p_t - 1 (NaN when the horizon is not observed)."""
    p, d = s.values, s.index
    out = np.full(len(s), np.nan)
    j = 0
    for i in range(len(s)):
        lim = d[i] + pd.Timedelta(days=horizon)
        if lim > d[-1]:
            break
        j = max(j, i + 1)
        while j < len(s) and d[j] <= lim:
            j += 1
        out[i] = p[i + 1:j].min() / p[i] - 1 if j > i + 1 else np.nan
    return pd.Series(out, index=d)


def auc(score, event):
    """Area under the ROC curve: P(score of an event date > score of a non-event date), ties counted 1/2."""
    score, event = np.asarray(score, float), np.asarray(event, bool)
    r = stats.rankdata(score)
    n1, n0 = event.sum(), (~event).sum()
    return float((r[event].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)) if n1 and n0 else np.nan


def roc(score, event):
    """ROC curve: false-alarm rate and hit rate for every threshold."""
    score, event = np.asarray(score, float), np.asarray(event, bool)
    o = np.argsort(-score, kind='mergesort')
    e = event[o]
    tp, fp = np.cumsum(e), np.cumsum(~e)
    return np.r_[0, fp / max(fp[-1], 1)], np.r_[0, tp / max(tp[-1], 1)]


def block_bootstrap_auc(score, event, block=26, B=999, seed=2026):
    """Moving-block bootstrap of the AUC (blocks of consecutive evaluation dates keep the overlap of the horizons)."""
    rng = np.random.default_rng(seed)
    score, event = np.asarray(score, float), np.asarray(event, bool)
    n = len(score)
    k = int(np.ceil(n / block))
    out = []
    for _ in range(B):
        idx = (rng.integers(0, n - block + 1, k)[:, None] + np.arange(block)[None, :]).ravel()[:n]
        out.append(auc(score[idx], event[idx]))
    return np.array(out)


def alarm_table(alarm, event):
    """Hit rate, false-alarm rate, precision and base rate of a 0/1 alarm against a 0/1 event."""
    a, e = np.asarray(alarm, bool), np.asarray(event, bool)
    return dict(hit=float((a & e).sum() / max(e.sum(), 1)), false_alarm=float((a & ~e).sum() / max((~e).sum(), 1)),
                precision=float((a & e).sum() / max(a.sum(), 1)) if a.sum() else np.nan, base=float(e.mean()),
                n_alarm=int(a.sum()), n=int(len(a)))
