"""
causal_core.py -- the engine of Chapter 14 (ATS): causal inference for time series
==================================================================================
numpy, scipy and statsmodels only. Every function is self-contained so that the Quantlet notebooks can copy it with
inspect.getsource.
  * dependence        HAC (Newey-West) long-run variance and OLS with HAC standard errors (Chapter 0);
  * Granger           Wald tests of Granger non-causality (pairwise and conditional, HAC or classical); Gaussian
                      transfer entropy; a k-nearest-neighbour (Frenzel-Pompe / KSG) conditional mutual information
                      with a block-permutation test;
  * discovery         PCMCI with partial correlations (Runge et al. 2019): the PC1 condition selection and the MCI
                      test; convergent cross mapping (Sugihara et al. 2012) with simplex projection;
  * synthetic control the weights of Abadie, Diamond and Hainmueller (2010) for a given V, the nested choice of V
                      (Synth), the cross-validated V of Abadie, Diamond and Hainmueller (2015); demeaned synthetic
                      control; ridge-augmented synthetic control (Ben-Michael, Feller and Rothstein 2021); synthetic
                      difference in differences (Arkhangelsky et al. 2021); in-space and in-time placebos;
  * staggered DiD     two-way fixed effects and the group-time ATT of Callaway and Sant'Anna (2021);
  * BSTS              a CausalImpact-type analysis (Brodersen et al. 2015) on a statsmodels unobserved-components model:
                      local level + regression on controls, fitted on the pre-period, counterfactual paths simulated
                      with parameter uncertainty;
  * DML               the partially linear model with blocked cross-fitting (Chernozhukov et al. 2018).
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import numpy as np
import pandas as pd
from scipy import optimize, stats
from scipy.special import digamma
from scipy.spatial import cKDTree


# =============================================================================
# DEPENDENCE: HAC (as in Chapter 0)
# =============================================================================
def nw_lags(T):
    """Newey-West (1994) rule of thumb: floor(4 (T/100)^(2/9)) lags."""
    return int(np.floor(4 * (T / 100) ** (2 / 9)))


def ols_hac(y, X, lags=None, hac=True):
    """OLS of y on X (X includes the constant); coefficient covariance: Newey-West with Bartlett weights (hac=True)
    or classical. Returns beta, covariance, residuals."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    T, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    if not hac:
        return b, XtXi * (e @ e) / (T - k), e
    L = nw_lags(T) if lags is None else lags
    u = X * e[:, None]
    S = u.T @ u
    for j in range(1, L + 1):
        G = u[j:].T @ u[:-j]
        S += (1 - j / (L + 1)) * (G + G.T)
    return b, XtXi @ S @ XtXi * T / (T - k), e


def wald(b, V, idx):
    """Wald statistic of b[idx] = 0 and its chi-square p-value (q restrictions); also the F form W/q."""
    bi = b[idx]
    W = float(bi @ np.linalg.solve(V[np.ix_(idx, idx)], bi))
    q = len(idx)
    return {'W': W, 'F': W / q, 'p': float(stats.chi2.sf(W, q)), 'q': q}


# =============================================================================
# GRANGER CAUSALITY AND TRANSFER ENTROPY
# =============================================================================
def lag_design(cols, p):
    """Rows t = p..T-1 of [1, lags 1..p of every column]; cols: list of 1-d arrays of equal length."""
    T = len(cols[0])
    blocks = [np.ones((T - p, 1))]
    for c in cols:
        c = np.asarray(c, float)
        blocks.append(np.column_stack([c[p - j:T - j] for j in range(1, p + 1)]))
    return np.hstack(blocks)


def granger(y, x, z=None, p=2, hac=True, lags=None):
    """Test of Granger non-causality from x to y (conditional on z if given): regression of y_t on p lags of y, x
    (and z); Wald test that the p lags of x are zero, with HAC (default) or classical covariance."""
    cols = [y, x] + ([] if z is None else [np.asarray(c, float) for c in (z if isinstance(z, (list, tuple)) else [z])])
    X = lag_design(cols, p)
    yy = np.asarray(y, float)[p:]
    b, V, e = ols_hac(yy, X, lags, hac)
    idx = list(range(1 + p, 1 + 2 * p))
    out = wald(b, V, idx)
    # restricted regression (without x): the Gaussian transfer entropy is half the log of the variance ratio
    Xr = np.delete(X, idx, axis=1)
    er = yy - Xr @ np.linalg.lstsq(Xr, yy, rcond=None)[0]
    out['te'] = 0.5 * np.log((er @ er) / (e @ e))
    out['T'] = len(yy)
    return out


def sim_common_driver(T, a=0.9, lag_x=1, lag_y=3, s=1.0, seed=0):
    """A common driver w_t (AR(1)) moves x with delay lag_x and y with delay lag_y; x has no effect on y.
    x_t = w_{t-lag_x} + e_t, y_t = w_{t-lag_y} + u_t."""
    rng = np.random.default_rng(seed)
    n = T + 50 + lag_y
    w = np.zeros(n)
    eps = rng.standard_normal(n)
    for t in range(1, n):
        w[t] = a * w[t - 1] + eps[t]
    x = np.r_[np.zeros(lag_x), w[:-lag_x]] + s * rng.standard_normal(n)
    y = np.r_[np.zeros(lag_y), w[:-lag_y]] + s * rng.standard_normal(n)
    k = 50 + lag_y
    return x[k:], y[k:], w[k:]


def knn_cmi(x, y, z=None, k=5):
    """Conditional mutual information I(X; Y | Z) by the k-nearest-neighbour estimator of Frenzel and Pompe (2007)
    (the Kraskov-Stoegbauer-Grassberger idea), maximum norm, rank-transformed margins. Without z: KSG mutual
    information (algorithm 1). In nats."""
    def col(a):
        a = np.asarray(a, float)
        return a[:, None] if a.ndim == 1 else a

    def rank(a):
        return np.column_stack([stats.rankdata(a[:, j]) / len(a) for j in range(a.shape[1])])
    x, y = rank(col(x)), rank(col(y))
    n = len(x)
    if z is None:
        xy = np.hstack([x, y])
        d = cKDTree(xy).query(xy, k + 1, p=np.inf)[0][:, -1] - 1e-12
        nx = np.array([len(v) - 1 for v in cKDTree(x).query_ball_point(x, d, p=np.inf)])
        ny = np.array([len(v) - 1 for v in cKDTree(y).query_ball_point(y, d, p=np.inf)])
        return float(digamma(k) + digamma(n) - np.mean(digamma(nx + 1) + digamma(ny + 1)))
    z = rank(col(z))
    xyz = np.hstack([x, y, z])
    d = cKDTree(xyz).query(xyz, k + 1, p=np.inf)[0][:, -1] - 1e-12
    xz, yz = np.hstack([x, z]), np.hstack([y, z])
    nxz = np.array([len(v) - 1 for v in cKDTree(xz).query_ball_point(xz, d, p=np.inf)])
    nyz = np.array([len(v) - 1 for v in cKDTree(yz).query_ball_point(yz, d, p=np.inf)])
    nz = np.array([len(v) - 1 for v in cKDTree(z).query_ball_point(z, d, p=np.inf)])
    return float(digamma(k) - np.mean(digamma(nxz + 1) + digamma(nyz + 1) - digamma(nz + 1)))


def transfer_entropy(x, y, lag=1, k=5, B=99, block=20, seed=0):
    """Transfer entropy from x to y with history length 1: TE = I(y_t; x_{t-lag} | y_{t-1}) by the kNN estimator;
    p-value from B block permutations of the source (blocks keep its autocorrelation)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = max(lag, 1)
    yt, ylag, xl = y[m:], y[m - 1:-1], x[m - lag:len(x) - lag]
    te = knn_cmi(yt, xl, ylag, k)
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(len(xl) / block))
    null = []
    for _ in range(B):
        starts = rng.integers(0, len(xl) - block, nb)
        xs = np.concatenate([xl[s:s + block] for s in starts])[:len(xl)]
        null.append(knn_cmi(yt, xs, ylag, k))
    null = np.array(null)
    return {'te': te, 'p': float((1 + (null >= te).sum()) / (B + 1)), 'null95': float(np.quantile(null, 0.95))}


def sim_nonlinear_coupling(T, c=0.6, seed=0):
    """x drives y through a symmetric nonlinearity (y_t = 0.4 y_{t-1} + c (x_{t-1}^2 - 1) + u_t): the linear
    Granger regression sees no effect, the transfer entropy does. x is Gaussian AR(1)."""
    rng = np.random.default_rng(seed)
    n = T + 100
    x, y = np.zeros(n), np.zeros(n)
    for t in range(1, n):
        x[t] = 0.5 * x[t - 1] + np.sqrt(0.75) * rng.standard_normal()
        y[t] = 0.4 * y[t - 1] + c * (x[t - 1] ** 2 - 1) + rng.standard_normal()
    return x[100:], y[100:]


# =============================================================================
# CAUSAL DISCOVERY: PCMCI (partial correlation) AND CONVERGENT CROSS MAPPING
# =============================================================================
def parcorr(data, i, tau, j, cond, T0):
    """Partial correlation of X^i_{t-tau} and X^j_t given the lagged variables in cond = [(k, s), ...] (value of
    X^k_{t-s}); rows t = T0..T-1. Returns (r, p-value) with T - T0 - |cond| - 2 degrees of freedom."""
    T = data.shape[0]
    rows = np.arange(T0, T)
    a, b = data[rows - tau, i], data[rows, j]
    if cond:
        Z = np.column_stack([np.ones(len(rows))] + [data[rows - s, k] for k, s in cond])
        a = a - Z @ np.linalg.lstsq(Z, a, rcond=None)[0]
        b = b - Z @ np.linalg.lstsq(Z, b, rcond=None)[0]
    r = float(np.corrcoef(a, b)[0, 1])
    df = len(rows) - len(cond) - 2
    t = r * np.sqrt(df / max(1e-12, 1 - r ** 2))
    return r, float(2 * stats.t.sf(abs(t), df))


def pcmci(data, tau_max=3, pc_alpha=0.2, alpha=0.01, max_conds=None):
    """PCMCI with partial correlations (Runge et al. 2019, Science Advances), lagged links only.
    Step 1 (PC1): for each X^j, start from all (i, tau), tau = 1..tau_max; at stage p remove every candidate that is
    independent of X^j_t (level pc_alpha) given the p strongest other candidates; stop when no stage-p test is
    possible. Step 2 (MCI): test X^i_{t-tau} -> X^j_t given the parents of X^j_t and the (shifted) parents of
    X^i_{t-tau}. Returns MCI values, p-values (N x N x tau_max+1, index [i, j, tau]) and the PC1 parents."""
    data = np.asarray(data, float)
    data = (data - data.mean(0)) / data.std(0)
    T, N = data.shape
    T0 = 2 * tau_max
    parents = {}
    for j in range(N):
        cand = [(i, tau) for i in range(N) for tau in range(1, tau_max + 1)]
        stat = {c: abs(parcorr(data, c[0], c[1], j, [], T0)[0]) for c in cand}
        cand = [c for c in cand if parcorr(data, c[0], c[1], j, [], T0)[1] <= pc_alpha]
        cand.sort(key=lambda c: -stat[c])
        p = 1
        while len(cand) > p and (max_conds is None or p <= max_conds):
            keep = []
            for c in cand:
                others = [o for o in cand if o != c][:p]
                r, pv = parcorr(data, c[0], c[1], j, others, T0)
                if pv <= pc_alpha:
                    keep.append(c)
                    stat[c] = min(stat[c], abs(r))
            cand = sorted(keep, key=lambda c: -stat[c])
            p += 1
        parents[j] = cand
    val = np.zeros((N, N, tau_max + 1))
    pval = np.ones((N, N, tau_max + 1))
    for j in range(N):
        for i in range(N):
            for tau in range(1, tau_max + 1):
                cond = [c for c in parents[j] if c != (i, tau)]
                cond += [(k, s + tau) for k, s in parents[i] if s + tau <= 2 * tau_max and (k, s + tau) not in cond
                         and (k, s + tau) != (i, tau)]
                val[i, j, tau], pval[i, j, tau] = parcorr(data, i, tau, j, cond, T0)
    return {'val': val, 'pval': pval, 'parents': parents, 'links': (pval <= alpha)}


def full_granger_links(data, tau_max=3, alpha=0.01):
    """Benchmark: lagged links from one VAR(tau_max) regression per target (full conditioning), coefficient t-tests."""
    data = np.asarray(data, float)
    data = (data - data.mean(0)) / data.std(0)
    T, N = data.shape
    X = lag_design([data[:, k] for k in range(N)], tau_max)
    pval = np.ones((N, N, tau_max + 1))
    for j in range(N):
        b, V, _ = ols_hac(data[tau_max:, j], X, hac=False)
        se = np.sqrt(np.diag(V))
        for i in range(N):
            for tau in range(1, tau_max + 1):
                c = 1 + i * tau_max + (tau - 1)
                pval[i, j, tau] = 2 * stats.t.sf(abs(b[c] / se[c]), len(X) - X.shape[1])
    return {'pval': pval, 'links': pval <= alpha}


def corr_links(data, tau_max=3, alpha=0.01):
    """Benchmark: lagged links from pairwise (unconditional) lagged correlations."""
    data = np.asarray(data, float)
    data = (data - data.mean(0)) / data.std(0)
    T, N = data.shape
    pval = np.ones((N, N, tau_max + 1))
    for i in range(N):
        for j in range(N):
            for tau in range(1, tau_max + 1):
                pval[i, j, tau] = parcorr(data, i, tau, j, [], 2 * tau_max)[1]
    return {'pval': pval, 'links': pval <= alpha}


def sim_pcmci_system(T, seed=0, a=0.95, c=0.4, n_extra=0, tau_max=3):
    """A known 6-variable lagged system with strong autocorrelation and a common driver (variable 0):
    0 -> 1 (lag 1), 0 -> 2 (lag 2), 1 -> 3 (lag 1), 2 -> 3 (lag 1), 3 -> 4 (lag 2), 5 independent (AR);
    n_extra further independent AR(1) variables (coefficient a) make the problem high-dimensional.
    Returns data (T x (6 + n_extra)) and the true link array [i, j, tau], tau = 0..tau_max."""
    rng = np.random.default_rng(seed)
    n = T + 200
    N = 6 + n_extra
    X = np.zeros((n, N))
    for t in range(2, n):
        e = rng.standard_normal(6)
        X[t, 0] = a * X[t - 1, 0] + e[0]
        X[t, 1] = 0.7 * X[t - 1, 1] + c * X[t - 1, 0] + e[1]
        X[t, 2] = 0.7 * X[t - 1, 2] + c * X[t - 2, 0] + e[2]
        X[t, 3] = 0.6 * X[t - 1, 3] + c * X[t - 1, 1] - c * X[t - 1, 2] + e[3]
        X[t, 4] = 0.8 * X[t - 1, 4] + c * X[t - 2, 3] + e[4]
        X[t, 5] = a * X[t - 1, 5] + e[5]
        if n_extra:
            X[t, 6:] = a * X[t - 1, 6:] + rng.standard_normal(n_extra)
    true = np.zeros((N, N, tau_max + 1), bool)
    for k in range(6, N):
        true[k, k, 1] = True
    for (i, j, tau) in [(0, 0, 1), (0, 1, 1), (0, 2, 2), (1, 1, 1), (1, 3, 1), (2, 2, 1), (2, 3, 1), (3, 3, 1),
                        (3, 4, 2), (4, 4, 1), (5, 5, 1)]:
        true[i, j, tau] = True
    return X[200:], true


def link_rates(links, true):
    """True positive rate (share of true cross links found) and false positive rate (share of absent cross links
    reported); auto-links (i = j) excluded."""
    N = true.shape[0]
    off = ~np.eye(N, dtype=bool)[:, :, None] & np.ones(true.shape, bool)
    off[:, :, 0] = False
    tp = (links & true & off).sum() / max(1, (true & off).sum())
    fp = (links & ~true & off).sum() / max(1, (~true & off).sum())
    return float(tp), float(fp)


def sim_logistic_pair(T, bxy=0.0, byx=0.32, rx=3.8, ry=3.5, seed=0, forcing=None):
    """Coupled logistic maps of Sugihara et al. (2012, Fig. 1): x_{t+1} = x_t (rx - rx x_t - bxy y_t),
    y_{t+1} = y_t (ry - ry y_t - byx x_t). byx > 0: x drives y. forcing=(F, period): both maps receive the same
    periodic forcing, the case in which CCM can report spurious bidirectional causality."""
    rng = np.random.default_rng(seed)
    x, y = np.empty(T + 200), np.empty(T + 200)
    x[0], y[0] = rng.uniform(0.2, 0.4), rng.uniform(0.2, 0.4)
    for t in range(T + 199):
        fx = fy = 0.0
        if forcing is not None:
            F, per = forcing
            fx = fy = F * np.sin(2 * np.pi * t / per)
        x[t + 1] = x[t] * (rx * (1 + fx) - rx * (1 + fx) * x[t] - bxy * y[t])
        y[t + 1] = y[t] * (ry * (1 + fy) - ry * (1 + fy) * y[t] - byx * x[t])
        x[t + 1], y[t + 1] = np.clip(x[t + 1], 1e-6, 1 - 1e-6), np.clip(y[t + 1], 1e-6, 1 - 1e-6)
    return x[200:], y[200:]


def embed_delay(x, E, tau=1):
    """Delay embedding: rows (x_t, x_{t-tau}, ..., x_{t-(E-1)tau}), t = (E-1)tau..T-1."""
    x = np.asarray(x, float)
    s = (E - 1) * tau
    return np.column_stack([x[s - k * tau:len(x) - k * tau] for k in range(E)])


def cross_map(lib_from, target, E=2, tau=1, L=None, rng=None):
    """Cross-map skill: reconstruct `target` from the shadow manifold of `lib_from` with simplex projection
    (E + 1 nearest neighbours, exponential weights), using a random library of L points; returns the correlation
    between the estimates and the true target. Sugihara et al. (2012): if X drives Y, the manifold of Y
    contains the information on X, so cross-mapping Y -> X has skill that grows with L."""
    M = embed_delay(lib_from, E, tau)
    tgt = np.asarray(target, float)[(E - 1) * tau:]
    n = len(M)
    rng = rng or np.random.default_rng(0)
    idx = np.arange(n) if L is None or L >= n else rng.choice(n, L, replace=False)
    tree = cKDTree(M[idx])
    d, nn = tree.query(M, E + 2)
    est = np.empty(n)
    for t in range(n):
        dd, ii = d[t], idx[nn[t]]
        keep = ii != t
        dd, ii = dd[keep][:E + 1], ii[keep][:E + 1]
        w = np.exp(-dd / max(dd[0], 1e-12))
        est[t] = w @ tgt[ii] / w.sum()
    return float(np.corrcoef(est, tgt)[0, 1])


def ccm_curve(x, y, libs, E=2, reps=20, seed=0):
    """Cross-map skill against library size, both directions, averaged over random libraries.
    'xmap_y_from_x': skill of estimating y from the manifold of x (evidence that y drives x)."""
    rng = np.random.default_rng(seed)
    out = {'L': list(libs), 'y_drives_x': [], 'x_drives_y': []}
    for L in libs:
        out['y_drives_x'].append(float(np.mean([cross_map(x, y, E, 1, L, rng) for _ in range(reps)])))
        out['x_drives_y'].append(float(np.mean([cross_map(y, x, E, 1, L, rng) for _ in range(reps)])))
    return out


# =============================================================================
# SYNTHETIC CONTROL
# =============================================================================
def sc_weights(X1, X0, v=None):
    """Synthetic control weights: argmin (X1 - X0 w)' V (X1 - X0 w), w >= 0, sum w = 1 (V = diag(v)).
    X1: k-vector, X0: k x J. Solved by SLSQP from equal weights."""
    X1, X0 = np.asarray(X1, float), np.asarray(X0, float)
    scale = max(np.abs(X0).max(), 1e-12)            # the weights do not depend on a common rescaling
    X1, X0 = X1 / scale, X0 / scale
    k, J = X0.shape
    v = np.ones(k) if v is None else np.asarray(v, float)
    H = X0.T @ (v[:, None] * X0)
    g = X0.T @ (v * X1)
    f = lambda w: 0.5 * w @ H @ w - g @ w
    jac = lambda w: H @ w - g
    r = optimize.minimize(f, np.ones(J) / J, jac=jac, bounds=[(0, 1)] * J,
                          constraints=({'type': 'eq', 'fun': lambda w: w.sum() - 1, 'jac': lambda w: np.ones(J)},),
                          method='SLSQP', options={'ftol': 1e-14, 'maxiter': 1000})
    w = np.clip(r.x, 0, None)
    return w / w.sum()


def synth_v(X1, X0, Z1, Z0, starts=4, seed=0):
    """Nested optimisation of Synth (Abadie, Diamond and Hainmueller 2011): predictors scaled by their standard
    deviation across units; V = diag(v), v on the simplex (softmax parametrisation); v minimises the pre-period
    MSPE of the outcomes Z (Z1: T0-vector, Z0: T0 x J). Returns v, w and the loss."""
    X = np.column_stack([X1, X0])
    sd = X.std(axis=1, ddof=1)
    sd[sd == 0] = 1
    X1s, X0s = X1 / sd, X0 / sd[:, None]
    k = len(X1)

    def loss(theta):
        v = np.exp(theta - theta.max())
        v /= v.sum()
        w = sc_weights(X1s, X0s, v)
        return float(np.mean((Z1 - Z0 @ w) ** 2))
    rng = np.random.default_rng(seed)
    best = None
    inits = [np.zeros(k)] + [rng.normal(0, 1.5, k) for _ in range(starts - 1)]
    # the regression-based starting point of Synth: v proportional to the squared OLS coefficients of Z on X
    for th in inits:
        r = optimize.minimize(loss, th, method='Nelder-Mead', options={'maxiter': 3000, 'xatol': 1e-6, 'fatol': 1e-10})
        if best is None or r.fun < best.fun:
            best = r
    v = np.exp(best.x - best.x.max())
    v /= v.sum()
    return v, sc_weights(X1s, X0s, v), float(best.fun), sd


def sc_demeaned(Y1pre, Y0pre):
    """Synthetic control with an intercept (Doudchenko and Imbens 2016; Ferman and Pinto 2021): weights fitted on
    pre-period outcomes after removing each unit's pre-period mean; intercept = difference of the means."""
    w = sc_weights(Y1pre - Y1pre.mean(), Y0pre - Y0pre.mean(0))
    return w, float(Y1pre.mean() - Y0pre.mean(0) @ w)


def ascm_ridge(Y1pre, Y0pre, Y0post, w, lam):
    """Ridge-augmented synthetic control (Ben-Michael, Feller and Rothstein 2021, eq. 7): the synthetic control
    plus a ridge correction for the remaining pre-period imbalance,
    Y0hat_t = sum_j w_j Y_jt + (Y1pre - Y0pre w)' eta_t, eta_t = ridge coefficients of Y_jt on Y_j,pre across donors
    (centred). Y0pre: T0 x J, Y0post: T1 x J. Returns the counterfactual path and the augmented weights."""
    Xc = Y0pre.T - Y0pre.T.mean(0)                         # J x T0, donors as observations
    G = Xc @ Xc.T
    J = Xc.shape[0]
    # augmented weights: w_aug = w + Xc (Xc'Xc + lam I)^-1 (Y1pre - Y0pre w)
    imb = Y1pre - Y0pre @ w
    w_aug = w + Xc @ np.linalg.solve(Xc.T @ Xc + lam * np.eye(Xc.shape[1]), imb)
    return Y0post @ w_aug, w_aug, G.trace() / J


def ascm_lambda(Y1pre, Y0pre, grid, holdout=6):
    """Choice of the ridge penalty by holding out the last pre-periods: fit on the first T0 - holdout periods,
    predict the held-out ones, keep the penalty with the smallest MSE."""
    best, mse = None, []
    a, b = Y0pre[:-holdout], Y0pre[-holdout:]
    for lam in grid:
        w = sc_weights(Y1pre[:-holdout], a)
        f, _, _ = ascm_ridge(Y1pre[:-holdout], a, b, w, lam)
        m = float(np.mean((Y1pre[-holdout:] - f) ** 2))
        mse.append(m)
        if best is None or m < best[1]:
            best = (lam, m)
    return best[0], mse


def sdid(Y, n_treated_last, T0):
    """Synthetic difference in differences (Arkhangelsky et al. 2021, Algorithm 1) for one treated unit (the last
    row of Y, units x periods) treated after period T0. Unit weights: penalised SC with intercept, zeta^2 =
    (N_tr T_post)^(1/2) sigma^2, sigma = sd of first differences of the control outcomes before treatment; time
    weights: SC of the post-period mean on the pre-periods with intercept (tiny ridge). Returns the average effect,
    the per-period effects, omega and lambda."""
    Y = np.asarray(Y, float)
    N, T = Y.shape
    Nco = N - n_treated_last
    Yco, Ytr = Y[:Nco], Y[Nco:].mean(0)
    T1 = T - T0
    sig = np.std(np.diff(Yco[:, :T0], axis=1), ddof=1)
    zeta = (n_treated_last * T1) ** 0.25 * sig

    def simplex_ls(A, b, pen):
        k = A.shape[1]
        # intercept handled by demeaning across the rows of A and b
        sc_ = max(np.abs(A).max(), 1e-12)
        Ac, bc = (A - A.mean(0)) / sc_, (b - b.mean()) / sc_
        pen = pen / sc_ ** 2
        H = Ac.T @ Ac + pen * np.eye(k)
        g = Ac.T @ bc
        r = optimize.minimize(lambda x: 0.5 * x @ H @ x - g @ x, np.ones(k) / k, jac=lambda x: H @ x - g,
                              bounds=[(0, 1)] * k, method='SLSQP',
                              constraints=({'type': 'eq', 'fun': lambda x: x.sum() - 1},),
                              options={'ftol': 1e-14, 'maxiter': 1000})
        x = np.clip(r.x, 0, None)
        return x / x.sum()
    omega = simplex_ls(Yco[:, :T0].T, Ytr[:T0], zeta ** 2 * T0)
    lam = simplex_ls(Yco[:, :T0], Yco[:, T0:].mean(1), 1e-6 * sig ** 2 * Nco)
    base_tr = Ytr[:T0] @ lam
    base_co = Yco[:, :T0] @ lam
    per = (Ytr[T0:] - base_tr) - omega @ (Yco[:, T0:] - base_co[:, None])
    return {'tau': float(per.mean()), 'per': per, 'omega': omega, 'lambda': lam, 'zeta': float(zeta)}


def sdid_placebo_se(Y, T0, reps=None):
    """Placebo standard error of SDID (Arkhangelsky et al. 2021, Algorithm 4) with one treated unit: each control
    in turn plays the treated unit among the other controls; se = sd of the placebo average effects."""
    Yco = np.asarray(Y, float)[:-1]
    taus = []
    for j in range(len(Yco)):
        Yp = np.vstack([np.delete(Yco, j, axis=0), Yco[j]])
        taus.append(sdid(Yp, 1, T0)['tau'])
    return float(np.std(taus, ddof=1)), np.array(taus)


def placebo_ratios(Y, T0, method='sc', **kw):
    """In-space placebo test (Abadie, Diamond and Hainmueller 2010): each unit in turn is treated as the treated
    one with all the others as donors; ratio of post- to pre-period RMSPE. Y: units x periods, the treated unit in
    the last row. Returns gaps (units x periods), ratios and the permutation p-value of the treated unit."""
    Y = np.asarray(Y, float)
    N, T = Y.shape
    gaps, ratios = np.zeros((N, T)), np.zeros(N)
    for i in range(N):
        y1, Y0 = Y[i], np.delete(Y, i, axis=0).T
        if method == 'sc':
            w = sc_weights(y1[:T0], Y0[:T0])
            fit = Y0 @ w
        else:
            w, c = sc_demeaned(y1[:T0], Y0[:T0])
            fit = Y0 @ w + c
        gaps[i] = y1 - fit
        ratios[i] = np.sqrt(np.mean(gaps[i, T0:] ** 2)) / np.sqrt(np.mean(gaps[i, :T0] ** 2))
    p = float((ratios >= ratios[-1]).sum() / N)
    return gaps, ratios, p


# =============================================================================
# STAGGERED ADOPTION: TWFE AND CALLAWAY-SANT'ANNA
# =============================================================================
def sim_staggered(n_per=60, T=20, cohorts=(6, 11, 16), seed=0, slope=0.25):
    """Panel with staggered adoption: cohorts treated from the given periods, a never-treated group; the effect
    grows with exposure (slope per period; a dict {cohort: slope} makes it heterogeneous across cohorts), unit and
    time fixed effects, i.i.d. noise. Returns a long DataFrame."""
    rng = np.random.default_rng(seed)
    rows = []
    groups = list(cohorts) + [0]
    for g in groups:
        for i in range(n_per):
            a = rng.normal()
            for t in range(1, T + 1):
                e = max(0, t - g + 1) if g else 0
                sl = slope.get(g, 0.0) if isinstance(slope, dict) else slope
                y = a + 0.1 * t + sl * e + rng.normal(scale=0.5)
                rows.append((f'{g}_{i}', g, t, y, int(g > 0 and t >= g)))
    return pd.DataFrame(rows, columns=['id', 'g', 't', 'y', 'd'])


def twfe_event(df, K=8):
    """Two-way fixed effects event-study regression with relative-time dummies -K..K (reference -1, endpoints
    binned), never-treated units included; within transformation by two-way demeaning (balanced panel)."""
    d = df.copy()
    d['rel'] = np.where(d['g'] > 0, d['t'] - d['g'], -999)
    ks = [k for k in range(-K, K + 1) if k != -1]
    for k in ks:
        if k == -K:
            d[f'e{k}'] = ((d['rel'] <= k) & (d['rel'] > -999)).astype(float)
        elif k == K:
            d[f'e{k}'] = (d['rel'] >= k).astype(float)
        else:
            d[f'e{k}'] = (d['rel'] == k).astype(float)
    cols = ['y'] + [f'e{k}' for k in ks]
    W = d[cols] - d.groupby('id')[cols].transform('mean') - d.groupby('t')[cols].transform('mean') + d[cols].mean()
    b = np.linalg.lstsq(W[cols[1:]].values, W['y'].values, rcond=None)[0]
    static = np.linalg.lstsq((d['d'] - d.groupby('id')['d'].transform('mean') - d.groupby('t')['d'].transform('mean')
                              + d['d'].mean()).values[:, None], W['y'].values, rcond=None)[0][0]
    return dict(zip(ks, b)), float(static)


def cs_att(df, K=8):
    """Callaway and Sant'Anna (2021) group-time effects with never-treated controls (no covariates):
    ATT(g, t) = [E(Y_t - Y_{g-1} | G = g) - E(Y_t - Y_{g-1} | never treated)]; event-study aggregation with
    cohort-size weights; and the overall average of the post-treatment ATT(g, t)."""
    P = df.pivot_table(index='id', columns='t', values='y')
    g = df.groupby('id')['g'].first()
    never = P[g == 0]
    att = {}
    for gg in sorted(set(g) - {0}):
        grp = P[g == gg]
        for t in P.columns:
            base = gg - 1 if t >= gg else t - 1
            if base < P.columns.min():
                continue
            att[(gg, t)] = ((grp[t] - grp[base]).mean() - (never[t] - never[base]).mean(), len(grp))
    ev = {}
    for k in range(-K, K + 1):
        cells = [(v, n) for (gg, t), (v, n) in att.items() if t - gg == k]
        if cells:
            ev[k] = sum(v * n for v, n in cells) / sum(n for _, n in cells)
    post = [(v, n) for (gg, t), (v, n) in att.items() if t >= gg]
    return ev, float(sum(v * n for v, n in post) / sum(n for _, n in post))


# =============================================================================
# BSTS / CAUSALIMPACT ON AN UNOBSERVED-COMPONENTS MODEL
# =============================================================================
def causal_impact(y, X, pre_end, level='llevel', draws=1000, seed=0, alpha=0.05):
    """CausalImpact-type analysis (Brodersen et al. 2015) with a state space model fitted by maximum likelihood on
    the pre-period (statsmodels UnobservedComponents): y_t = mu_t + x_t'beta + e_t, mu_t a local level (random walk).
    Counterfactual post-period paths are simulated from the model given the observed controls, with parameter
    uncertainty (parameters drawn from their asymptotic normal distribution) and state uncertainty (simulation
    from the filtered state at the end of the pre-period). y, X: pandas objects on the same index.
    Returns pointwise and cumulative effects with (1 - alpha) intervals and the posterior tail probability."""
    import statsmodels.api as sm
    y = pd.Series(y, dtype=float)
    X = pd.DataFrame(X).astype(float)
    pre = y.index <= pd.Timestamp(pre_end)
    mod = sm.tsa.UnobservedComponents(y[pre], level=level, exog=X[pre] if X.shape[1] else None)
    res = mod.fit(disp=False, maxiter=2000)
    rng = np.random.default_rng(seed)
    npost = int((~pre).sum())
    Xpost = X[~pre].values if X.shape[1] else None
    cov = res.cov_params().values
    paths = np.empty((draws, npost))
    names = list(res.params.index)
    for d in range(draws):
        th = res.params.values.copy()
        try:
            th = rng.multivariate_normal(res.params.values, cov)
        except Exception:
            pass
        for k, nm in enumerate(names):                       # variances must stay positive
            if nm.startswith('sigma2'):
                th[k] = abs(th[k])
        rd = mod.smooth(th)
        sim = rd.simulate(npost, anchor='end', exog=Xpost, random_state=rng)
        paths[d] = np.asarray(sim).ravel()
    ypost = y[~pre].values
    point = ypost - paths.mean(0)
    lo, hi = np.quantile(ypost - paths, [alpha / 2, 1 - alpha / 2], axis=0)
    cum = np.cumsum(ypost - paths, axis=1)
    out = {'pred': paths.mean(0), 'pred_lo': np.quantile(paths, alpha / 2, axis=0),
           'pred_hi': np.quantile(paths, 1 - alpha / 2, axis=0), 'effect': point, 'lo': lo, 'hi': hi,
           'cum': cum.mean(0), 'cum_lo': np.quantile(cum, alpha / 2, axis=0), 'cum_hi': np.quantile(cum, 1 - alpha / 2, axis=0),
           'avg': float((ypost - paths).mean()), 'avg_lo': float(np.quantile((ypost - paths).mean(1), alpha / 2)),
           'avg_hi': float(np.quantile((ypost - paths).mean(1), 1 - alpha / 2)),
           'p': float(min((paths.mean(1) >= ypost.mean()).mean(), (paths.mean(1) <= ypost.mean()).mean())),
           'params': res.params.to_dict(), 'fitted_pre': (y[pre] - res.resid).values, 'index_post': y.index[~pre]}
    return out


# =============================================================================
# DOUBLE / DEBIASED MACHINE LEARNING WITH BLOCKED CROSS-FITTING
# =============================================================================
def dml_plr(y, d, X, learner, K=5, gap=0):
    """Partially linear model y = theta d + g(X) + u, d = m(X) + v (Chernozhukov et al. 2018): cross-fitted
    residuals from K contiguous blocks (training excludes `gap` observations on each side of the held-out block);
    theta = sum(v_hat y_hat) / sum(v_hat d_hat); HAC standard error of the orthogonal score."""
    y, d, X = np.asarray(y, float), np.asarray(d, float), np.asarray(X, float)
    n = len(y)
    ry, rd = np.empty(n), np.empty(n)
    edges = np.linspace(0, n, K + 1).astype(int)
    for k in range(K):
        a, b = edges[k], edges[k + 1]
        tr = np.r_[0:max(0, a - gap), min(n, b + gap):n]
        my = learner().fit(X[tr], y[tr])
        md = learner().fit(X[tr], d[tr])
        ry[a:b] = y[a:b] - my.predict(X[a:b])
        rd[a:b] = d[a:b] - md.predict(X[a:b])
    theta = float(rd @ ry / (rd @ rd))
    psi = (ry - theta * rd) * rd
    L = nw_lags(n)
    v = psi @ psi / n
    for j in range(1, L + 1):
        v += 2 * (1 - j / (L + 1)) * (psi[j:] @ psi[:-j]) / n
    se = float(np.sqrt(v / n) / np.mean(rd ** 2))
    return {'theta': theta, 'se': se}


def sim_dml(T, theta=0.5, seed=0):
    """A dependent-data design for DML: X_t is a VAR(1) of 10 variables; the treatment d_t and the outcome y_t
    depend on X_t through nonlinear functions; AR(1) errors."""
    rng = np.random.default_rng(seed)
    p = 10
    X = np.zeros((T + 100, p))
    for t in range(1, T + 100):
        X[t] = 0.7 * X[t - 1] + rng.standard_normal(p)
    X = X[100:]
    v, u = np.zeros(T), np.zeros(T)
    for t in range(1, T):
        v[t] = 0.5 * v[t - 1] + rng.standard_normal()
        u[t] = 0.5 * u[t - 1] + rng.standard_normal()
    m = np.tanh(X[:, 0]) + 0.5 * X[:, 1] ** 2 / 2
    g = np.sin(X[:, 0]) + 0.5 * X[:, 1] ** 2 + 0.5 * np.abs(X[:, 2])
    d = m + v
    y = theta * d + g + u
    return y, d, X
