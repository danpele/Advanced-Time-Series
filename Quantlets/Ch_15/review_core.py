"""
review_core.py -- the engine of Chapter 15 (ATS): tools that every project uses
===============================================================================
Long-run variance (Newey-West, Bartlett weights), the Diebold-Mariano test with the Harvey-Leybourne-Newbold
correction, and three Monte Carlo designs for the project chapter:
  * snooping   the family-wise false-positive rate of a specification search over K candidate predictors of a series
               with no predictability, with and without a correction (Bonferroni, max-t over the K statistics);
  * leakage    out-of-sample R^2 of a forecasting regression whose predictors were selected on the whole sample
               (look-ahead) against selection on the training sample only;
  * power      the power of the DM test for a given out-of-sample length, effect size and serial dependence of the
               loss differential (the pre-registration question: how long must the evaluation sample be?).
numpy and scipy only.
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import numpy as np
from scipy import stats
from scipy.signal import lfilter


def nw_lags(T):
    """Newey-West (1994) rule of thumb: floor(4 (T/100)^(2/9)) lags."""
    return int(np.floor(4 * (T / 100) ** (2 / 9)))


def lrv(x, lags=None):
    """Long-run variance of x (Bartlett kernel, Newey-West): gamma_0 + 2 sum_j (1 - j/(L+1)) gamma_j."""
    x = np.asarray(x, float) - np.mean(x)
    T = len(x)
    L = nw_lags(T) if lags is None else lags
    v = x @ x / T
    for j in range(1, L + 1):
        v += 2 * (1 - j / (L + 1)) * (x[j:] @ x[:-j]) / T
    return v


def dm_test(e1, e2, h=1, loss='se'):
    """Diebold-Mariano test of equal accuracy, d_t = L(e1) - L(e2); HAC variance with h-1 lags (at least the NW
    rule), Harvey-Leybourne-Newbold small-sample correction, Student t(P-1) p-value (two-sided)."""
    e1, e2 = np.asarray(e1, float), np.asarray(e2, float)
    d = e1 ** 2 - e2 ** 2 if loss == 'se' else np.abs(e1) - np.abs(e2)
    P = len(d)
    L = max(h - 1, nw_lags(P))
    dm = d.mean() / np.sqrt(lrv(d, L) / P)
    hln = dm * np.sqrt((P + 1 - 2 * h + h * (h - 1) / P) / P)
    return {'dbar': float(d.mean()), 'dm': float(dm), 'hln': float(hln), 'p': float(2 * stats.t.sf(abs(hln), P - 1)),
            'P': P}


def ar1(T, rho, rng, burn=100):
    """Gaussian AR(1) with unit innovation variance (a T-vector)."""
    e = rng.standard_normal(T + burn)
    e[0] /= np.sqrt(1 - rho ** 2)
    return lfilter([1.0], [1.0, -rho], e)[burn:]


def hac_t(y, x):
    """t-statistic of the slope of y on (1, x) with a Newey-West covariance."""
    X = np.column_stack([np.ones(len(x)), x])
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    u = X * e[:, None]
    T = len(y)
    L = nw_lags(T)
    S = u.T @ u
    for j in range(1, L + 1):
        G = u[j:].T @ u[:-j]
        S += (1 - j / (L + 1)) * (G + G.T)
    V = XtXi @ S @ XtXi
    return b[1] / np.sqrt(V[1, 1])


def snooping_rates(K, T=250, rho_x=0.9, common=0.5, reps=1000, seed=0, alpha=0.05):
    """Specification search: y_t = u_t (no predictability, AR(1) with rho 0.3); K candidate predictors x_{k,t-1},
    persistent (AR(1) with rho_x) and correlated through a common factor (share `common` of the variance).
    For each data set: HAC t-statistic of each predictor; report the share of data sets in which
      naive   at least one |t| > 1.96 (the best predictor is reported as if it were the only one tried);
      bonf    at least one p < alpha/K;
      maxt    max |t| above the 95% quantile of max |t| under the null (simulated from the same design: the
              Reality Check / step-down logic with the dependence across predictors kept)."""
    rng = np.random.default_rng(seed)
    tmax = np.empty(reps)
    pmin = np.empty(reps)
    for r in range(reps):
        y = ar1(T + 1, 0.3, rng)[1:]
        f = ar1(T + 1, rho_x, rng)
        ts = np.empty(K)
        for k in range(K):
            x = np.sqrt(common) * f + np.sqrt(1 - common) * ar1(T + 1, rho_x, rng)
            ts[k] = hac_t(y, x[:-1])
        tmax[r] = np.max(np.abs(ts))
        pmin[r] = 2 * stats.norm.sf(tmax[r])
    half = reps // 2                      # critical value from one half, rejection rate on the other half
    crit = np.quantile(tmax[:half], 1 - alpha)
    return {'K': K, 'naive': float(np.mean(pmin < alpha)), 'bonf': float(np.mean(pmin < alpha / K)),
            'maxt': float(np.mean(tmax[half:] > crit)), 'crit_maxt': float(crit)}


def leakage_r2(T=240, n_test=60, P=100, k=5, reps=500, seed=0):
    """Predictor selection with look-ahead: y and P candidate predictors are independent white noise (no
    predictability). The k predictors with the largest |correlation| with y are selected
      leaky   on the whole sample (training and test periods), or
      honest  on the training sample only;
    OLS on the training sample, forecasts on the last n_test periods, out-of-sample R^2 against the training mean."""
    rng = np.random.default_rng(seed)
    out = {'leaky': [], 'honest': []}
    n_tr = T - n_test
    for _ in range(reps):
        y = rng.standard_normal(T)
        X = rng.standard_normal((T, P))
        for lab, rows in (('leaky', slice(0, T)), ('honest', slice(0, n_tr))):
            yc = y[rows] - y[rows].mean()
            Xc = X[rows] - X[rows].mean(0)
            c = np.abs(Xc.T @ yc) / (np.sqrt((Xc ** 2).sum(0)) * np.sqrt(yc @ yc))
            sel = np.argsort(-c)[:k]
            Z = np.column_stack([np.ones(n_tr), X[:n_tr, sel]])
            b = np.linalg.lstsq(Z, y[:n_tr], rcond=None)[0]
            Zt = np.column_stack([np.ones(n_test), X[n_tr:, sel]])
            f = Zt @ b
            bench = y[:n_tr].mean()
            out[lab].append(1 - np.sum((y[n_tr:] - f) ** 2) / np.sum((y[n_tr:] - bench) ** 2))
    return {k_: np.array(v) for k_, v in out.items()}


def dm_power(P, delta, rho=0.3, reps=2000, seed=0, alpha=0.05):
    """Power of the DM-HLN test (two-sided, level alpha) when the loss differential is d_t = delta + u_t, u_t a
    Gaussian AR(1) with coefficient rho and unit variance: delta is the mean gain in standard deviations of d."""
    rng = np.random.default_rng(seed)
    rej = 0
    for _ in range(reps):
        d = delta + ar1(P, rho, rng)
        L = nw_lags(P)
        s = d.mean() / np.sqrt(lrv(d, L) / P)
        s *= np.sqrt((P - 1) / P)
        rej += 2 * stats.t.sf(abs(s), P - 1) < alpha
    return rej / reps


def dm_power_approx(P, delta, rho=0.3, alpha=0.05):
    """Large-sample power: the statistic is approximately N(delta sqrt(P / Omega), 1), Omega = (1+rho)/(1-rho) the
    long-run variance of d (unit variance AR(1))."""
    om = (1 + rho) / (1 - rho)
    m = delta * np.sqrt(P / om)
    z = stats.norm.ppf(1 - alpha / 2)
    return float(stats.norm.sf(z - m) + stats.norm.cdf(-z - m))


def p_required(delta, rho=0.3, power=0.8, alpha=0.05):
    """Out-of-sample length for a given power (large-sample formula): P = Omega ((z_{1-a/2} + z_power) / delta)^2."""
    om = (1 + rho) / (1 - rho)
    return float(om * ((stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)) / delta) ** 2)
