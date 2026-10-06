"""
ms_core.py -- transparent numpy engine of Chapter 7 (ATS): Markov-switching models
==================================================================================
Everything is written out in numpy/scipy so that each step of the slides can be followed line by line:
  * hamilton_filter   -- predicted and filtered regime probabilities and the log-likelihood (Hamilton 1989, 1994 ch. 22),
                         in a scaled form (log-sum-exp) that never underflows; constant or time-varying transitions;
  * kim_smoother      -- smoothed probabilities and joint smoothed transition probabilities (Kim 1994);
  * em_msr            -- EM algorithm (Hamilton 1990) for a Markov-switching regression with switching and non-switching
                         coefficients and regime-specific or common variance (MSI, MSIH, MSIAH in Krolzig's notation);
  * msm_ar            -- Hamilton's (1989) switching-mean autoregression on the expanded state (S_t, ..., S_{t-p}),
                         estimated by numerical maximum likelihood, with constant or time-varying transitions (TVTP);
  * em_msvar          -- EM for a Markov-switching VAR with regime-dependent intercept, coefficients and covariance
                         (MSIAH-VAR, Krolzig 1997) and regime-dependent impulse responses (Ehrmann, Ellison, Valla 2003);
  * ms_garch          -- Markov-switching GARCH: Haas, Mittnik and Paolella (2004) and Gray (1996), by numerical ML;
  * gibbs_ms          -- Bayesian estimation by Gibbs sampling with data augmentation (Albert and Chib 1993) and
                         forward filtering-backward sampling of the regimes (Chib 1996), with the random permutation
                         sampler of Fruhwirth-Schnatter (2001) for label switching;
  * forecasts, scores and helpers (ergodic probabilities, durations, simulation, GPH estimator, QPS, concordance).
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import numpy as np
from scipy import optimize, stats


# =============================================================================
# MARKOV CHAIN
# =============================================================================
def ergodic(P):
    """Ergodic (stationary) probabilities of a transition matrix P[i, j] = Pr(S_t = j | S_{t-1} = i):
    the left eigenvector of P for the eigenvalue 1, i.e. the solution of pi' P = pi', sum(pi) = 1."""
    M = P.shape[0]
    A = np.vstack([P.T - np.eye(M), np.ones(M)])
    b = np.r_[np.zeros(M), 1.0]
    return np.linalg.lstsq(A, b, rcond=None)[0]


def durations(P):
    """Expected duration of each regime, 1 / (1 - p_ii)."""
    return 1.0 / (1.0 - np.diag(P))


def simulate_chain(P, T, rng, s0=None):
    M = P.shape[0]
    s = np.empty(T, dtype=int)
    s[0] = rng.choice(M, p=ergodic(P)) if s0 is None else s0
    u = rng.random(T)
    cum = np.cumsum(P, axis=1)
    for t in range(1, T):
        s[t] = min(int(np.searchsorted(cum[s[t - 1]], u[t])), M - 1)
    return s


# =============================================================================
# HAMILTON FILTER AND KIM SMOOTHER
# =============================================================================
def hamilton_filter(logf, P, xi1=None):
    """Hamilton filter.
    logf : T x M array, log f(y_t | S_t = j, Y_{t-1}) for each regime j;
    P    : M x M transition matrix (rows sum to 1) or T x M x M array, P[t] the transition from t-1 to t;
    xi1  : Pr(S_1 = j | Y_0), the ergodic probabilities by default.
    Returns pred (xi_{t|t-1}), filt (xi_{t|t}), the log-likelihood and its contributions log f(y_t | Y_{t-1})."""
    T, M = logf.shape
    tv = P.ndim == 3
    pred = np.empty((T, M))
    filt = np.empty((T, M))
    llt = np.empty(T)
    xi = ergodic(P[0] if tv else P) if xi1 is None else np.asarray(xi1, float)
    for t in range(T):
        if t > 0:
            xi = filt[t - 1] @ (P[t] if tv else P)          # prediction: xi_{t|t-1} = P' xi_{t-1|t-1}
        pred[t] = xi
        m = logf[t].max()
        w = xi * np.exp(logf[t] - m)                         # xi_{t|t-1} * f_j(y_t), scaled by exp(-m)
        s = w.sum()
        llt[t] = m + np.log(s)                               # log f(y_t | Y_{t-1}) = log sum_j xi_j f_j
        filt[t] = w / s                                      # Bayes update
    return dict(pred=pred, filt=filt, loglik=float(llt.sum()), llt=llt)


def kim_smoother(filt, pred, P):
    """Kim (1994) smoother: smoothed probabilities xi_{t|T} and joint smoothed probabilities
    Pr(S_{t-1} = i, S_t = j | Y_T) (stored in joint[t], t >= 1), from
    Pr(S_t = i, S_{t+1} = j | Y_T) = xi_{t|t}(i) p_ij xi_{t+1|T}(j) / xi_{t+1|t}(j)."""
    T, M = filt.shape
    tv = P.ndim == 3
    sm = np.empty((T, M))
    joint = np.zeros((T, M, M))
    sm[-1] = filt[-1]
    for t in range(T - 2, -1, -1):
        Pn = P[t + 1] if tv else P
        ratio = np.divide(sm[t + 1], pred[t + 1], out=np.zeros(M), where=pred[t + 1] > 0)
        J = filt[t][:, None] * Pn * ratio[None, :]
        sm[t] = J.sum(axis=1)
        joint[t + 1] = J
    return sm, joint


def ffbs(filt, P, rng):
    """Forward filtering, backward sampling (Chib 1996): one draw of the whole regime path S_1..S_T from
    p(S | Y, theta) = p(S_T | Y) prod_t p(S_t | S_{t+1}, Y_t), with p(S_t = i | S_{t+1} = j, Y_t) prop. to xi_{t|t}(i) p_ij."""
    T, M = filt.shape
    tv = P.ndim == 3
    s = np.empty(T, dtype=int)
    u = rng.random(T)
    s[-1] = min(int(np.searchsorted(np.cumsum(filt[-1]), u[-1])), M - 1)
    for t in range(T - 2, -1, -1):
        Pn = P[t + 1] if tv else P
        w = filt[t] * Pn[:, s[t + 1]]
        s[t] = min(int(np.searchsorted(np.cumsum(w / w.sum()), u[t])), M - 1)
    return s


# =============================================================================
# MARKOV-SWITCHING REGRESSION (MSI, MSIH, MSIAH) BY EM
# =============================================================================
def lag_design(y, p, const=True):
    """Response y_t and regressors (1, y_{t-1}, ..., y_{t-p}) for t = p, ..., T-1."""
    y = np.asarray(y, float)
    X = [y[p - k:len(y) - k] for k in range(1, p + 1)]
    if const:
        X = [np.ones(len(y) - p)] + X
    return y[p:], (np.column_stack(X) if X else np.empty((len(y) - p, 0)))


def msr_logf(y, X, beta, sig2):
    """log N(y_t; x_t' beta_j, sigma2_j) for each regime: beta is K x k, sig2 has K entries."""
    mu = X @ beta.T                                                  # T x K
    return -0.5 * (np.log(2 * np.pi * sig2)[None, :] + (y[:, None] - mu) ** 2 / sig2[None, :])


def _wls_shared(y, X, W, sig2, switch):
    """M-step for coefficients when some are switching (switch[k] True) and others common to all regimes:
    weighted least squares on the stacked design, weights W[t, j] / sigma2_j."""
    T, k = X.shape
    K = W.shape[1]
    sw = np.where(switch)[0]
    ns = np.where(~np.asarray(switch))[0]
    npar = len(ns) + K * len(sw)
    A = np.zeros((npar, npar))
    b = np.zeros(npar)
    for j in range(K):
        D = np.zeros((T, npar))
        D[:, :len(ns)] = X[:, ns]
        D[:, len(ns) + j * len(sw):len(ns) + (j + 1) * len(sw)] = X[:, sw]
        w = W[:, j] / sig2[j]
        A += D.T @ (D * w[:, None])
        b += D.T @ (w * y)
    th = np.linalg.solve(A, b)
    beta = np.zeros((K, k))
    for j in range(K):
        beta[j, ns] = th[:len(ns)]
        beta[j, sw] = th[len(ns) + j * len(sw):len(ns) + (j + 1) * len(sw)]
    return beta


def em_msr(y, X, K, switch=None, switch_var=True, P0=None, beta0=None, sig20=None, maxit=1000, tol=1e-8,
           P_mask=None, rng=None, var_floor=1e-6, xi1_fixed=None):
    """EM algorithm of Hamilton (1990) for y_t = x_t' beta_{S_t} + e_t, e_t ~ N(0, sigma2_{S_t}).
    switch     : boolean mask of the switching coefficients (default: all switch);
    switch_var : regime-specific variances (True) or a common variance;
    P_mask     : optional 0/1 mask of allowed transitions (e.g. an upper-triangular change-point model, Chib 1998);
    xi1_fixed  : a fixed distribution of S_1 (e.g. (1, 0, ..., 0) for a change-point model), otherwise estimated.
    E-step: Hamilton filter + Kim smoother. M-step: p_ij = sum_t Pr(S_{t-1}=i, S_t=j|Y_T) / sum_t Pr(S_{t-1}=i|Y_T);
    weighted least squares for beta_j with weights xi_{t|T}(j); sigma2_j = weighted mean of squared residuals.
    The distribution of S_1 is a free parameter, estimated by xi_{1|T} (Hamilton 1990): then each EM step cannot lower
    the likelihood. The final likelihood is reported both with this estimate and with the ergodic distribution."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    T, k = X.shape
    switch = np.ones(k, bool) if switch is None else np.asarray(switch, bool)
    rng = rng or np.random.default_rng(0)
    if beta0 is None:
        b_ols = np.linalg.lstsq(X, y, rcond=None)[0]
        s_ols = np.std(y - X @ b_ols)
        beta = np.tile(b_ols, (K, 1))
        if switch_var and rng.random() < 0.5:        # a start that separates the regimes by their variances
            sig2 = s_ols ** 2 * np.geomspace(0.2, 2.5, K) * rng.uniform(0.7, 1.3, K)
            if switch.any():
                beta[:, np.where(switch)[0][0]] += 0.1 * s_ols * rng.normal(size=K)
        else:                                         # a start that separates the regimes by their means
            if switch.any():
                beta[:, np.where(switch)[0][0]] += np.linspace(-1, 1, K) * s_ols * (0.5 + rng.random(K))
            sig2 = np.full(K, s_ols ** 2) * (np.linspace(0.5, 1.5, K) if switch_var else 1.0)
    else:
        beta, sig2 = np.array(beta0, float), np.array(sig20, float)
    if P0 is None:
        d = rng.uniform(0.6, 0.97, K) if K > 1 else np.ones(1)
        P = np.where(np.eye(K, dtype=bool), d[:, None], ((1 - d) / max(K - 1, 1))[:, None])
    else:
        P = np.array(P0, float)
    if P_mask is not None:
        P = P * P_mask
        P = P / P.sum(1, keepdims=True)
    path = []
    xi1 = ergodic(P) if xi1_fixed is None else np.asarray(xi1_fixed, float)
    for it in range(maxit):
        f = hamilton_filter(msr_logf(y, X, beta, sig2), P, xi1)
        path.append(f['loglik'])
        sm, joint = kim_smoother(f['filt'], f['pred'], P)
        if xi1_fixed is None:
            xi1 = np.clip(sm[0], 1e-10, None) / np.clip(sm[0], 1e-10, None).sum()   # M-step: Pr(S_1 = j)
        # M-step: transition probabilities
        num = joint[1:].sum(axis=0)
        den = sm[:-1].sum(axis=0)
        P = num / den[:, None]
        if P_mask is not None:
            P = P * P_mask
        P = np.clip(P, 1e-12, None)
        P = P / P.sum(1, keepdims=True)
        # M-step: coefficients and variances
        if switch.all():
            beta = np.vstack([np.linalg.solve(X.T @ (X * sm[:, j:j + 1]), X.T @ (sm[:, j] * y)) for j in range(K)])
        else:
            beta = _wls_shared(y, X, sm, sig2, switch)
        res2 = (y[:, None] - X @ beta.T) ** 2
        if switch_var:
            sig2 = np.maximum((sm * res2).sum(0) / sm.sum(0), var_floor)
        else:
            sig2 = np.full(K, max((sm * res2).sum() / T, var_floor))
        if it > 2 and abs(path[-1] - path[-2]) < tol * (1 + abs(path[-1])):
            break
    f_free = hamilton_filter(msr_logf(y, X, beta, sig2), P, xi1)
    f = f_free if xi1_fixed is not None else hamilton_filter(msr_logf(y, X, beta, sig2), P)
    sm, joint = kim_smoother(f['filt'], f['pred'], P)
    npar = K * (K - 1) + int(switch.sum()) * K + int((~switch).sum()) + (K if switch_var else 1)
    if P_mask is not None:
        npar -= int((P_mask == 0).sum())
    return dict(beta=beta, sig2=sig2, P=P, loglik=f['loglik'], loglik_free=f_free['loglik'], filt=f['filt'],
                pred=f['pred'], smooth=sm, path=np.array(path + [f_free['loglik']]), iters=it + 1, npar=npar, T=T, K=K,
                switch=switch, switch_var=switch_var)


def order_regimes(r, key='mean', col=0):
    """Relabel the regimes of an em_msr result in increasing order of the intercept (key='mean') or of the variance
    (key='var'): one identification restriction against label switching."""
    o = np.argsort(r['beta'][:, col] if key == 'mean' else r['sig2'])
    out = dict(r)
    out['beta'], out['sig2'] = r['beta'][o], r['sig2'][o]
    out['order'] = o
    out['P'] = r['P'][np.ix_(o, o)]
    for k in ('filt', 'pred', 'smooth'):
        out[k] = r[k][:, o]
    return out


def best_em(y, X, K, starts=10, seed=0, order='mean', polish=False, **kw):
    """EM from several random starting values; the best log-likelihood wins (EM finds local maxima);
    polish=True finishes with numerical ML from the best EM solution (msr_ml)."""
    rng = np.random.default_rng(seed)
    best, lls = None, []
    for s in range(starts):
        try:
            r = em_msr(y, X, K, rng=rng, **kw)
        except np.linalg.LinAlgError:
            continue
        lls.append(r['loglik'])
        if best is None or r['loglik'] > best['loglik']:
            best = r
    best = order_regimes(best, order) if order else best
    if polish:
        best = msr_ml(y, X, best)
    best['start_ll'] = np.array(lls)
    return best


def info_criteria(loglik, npar, T):
    return dict(AIC=-2 * loglik + 2 * npar, BIC=-2 * loglik + npar * np.log(T), HQ=-2 * loglik + 2 * npar * np.log(np.log(T)))


def linear_ar(y, X):
    """Gaussian linear regression (K = 1): ML estimates and log-likelihood."""
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    s2 = e @ e / len(y)
    return dict(beta=b, sig2=s2, loglik=float(-0.5 * len(y) * (np.log(2 * np.pi * s2) + 1)), npar=X.shape[1] + 1)


# =============================================================================
# NUMERICAL ML AND STANDARD ERRORS FOR THE MS REGRESSION
# =============================================================================
def msr_pack(r):
    """Unconstrained parameters of an MS regression: common coefficients, switching coefficients by regime,
    log variances, and for each row i of P the logs of p_ij / p_ii (j != i)."""
    K, sw = r['K'], r['switch']
    th = list(r['beta'][0, ~sw]) + list(r['beta'][:, sw].ravel())
    th += list(np.log(r['sig2'] if r['switch_var'] else r['sig2'][:1]))
    P = r['P']
    for i in range(K):
        th += [np.log(P[i, j] / P[i, i]) for j in range(K) if j != i]
    return np.array(th)


def msr_unpack(th, K, k, sw, switch_var):
    ns, nsw = int((~sw).sum()), int(sw.sum())
    beta = np.zeros((K, k))
    beta[:, ~sw] = th[:ns]
    beta[:, sw] = th[ns:ns + K * nsw].reshape(K, nsw)
    pos = ns + K * nsw
    nv = K if switch_var else 1
    sig2 = np.exp(th[pos:pos + nv]) * np.ones(K)
    pos += nv
    P = np.zeros((K, K))
    for i in range(K):
        a = np.zeros(K)
        a[[j for j in range(K) if j != i]] = th[pos:pos + K - 1]
        pos += K - 1
        P[i] = np.exp(a - a.max()) / np.exp(a - a.max()).sum()
    return beta, sig2, P


def msr_ml(y, X, r):
    """Numerical ML with the ergodic initial distribution (BFGS on unconstrained parameters), started from an EM
    solution r; standard errors of the natural parameters (coefficients, variances, p_ii) by the delta method
    from the numerical Hessian of the log-likelihood."""
    K, k, sw, sv = r['K'], X.shape[1], r['switch'], r['switch_var']

    def nll(th):
        beta, sig2, P = msr_unpack(th, K, k, sw, sv)
        return -hamilton_filter(msr_logf(y, X, beta, sig2), P)['loglik']
    o = optimize.minimize(nll, msr_pack(r), method='BFGS', options=dict(gtol=1e-7, maxiter=5000))

    def nat(th):
        beta, sig2, P = msr_unpack(th, K, k, sw, sv)
        return np.r_[beta[0, ~sw], beta[:, sw].ravel(), sig2 if sv else sig2[:1], np.diag(P)]
    try:
        V = np.linalg.inv(num_hessian(nll, o.x))
        J = num_jacobian(nat, o.x)
        se = np.sqrt(np.clip(np.diag(J @ V @ J.T), 0, None))
    except np.linalg.LinAlgError:
        se = np.full(len(nat(o.x)), np.nan)
    beta, sig2, P = msr_unpack(o.x, K, k, sw, sv)
    f = hamilton_filter(msr_logf(y, X, beta, sig2), P)
    sm, _ = kim_smoother(f['filt'], f['pred'], P)
    out = dict(r)
    out.update(beta=beta, sig2=sig2, P=P, loglik=f['loglik'], filt=f['filt'], pred=f['pred'], smooth=sm, se=se,
               theta=nat(o.x), nfev=o.nfev)
    return out


def num_hessian(f, x, h=1e-4):
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ei, ej = np.zeros(n), np.zeros(n)
            ei[i], ej[j] = h, h
            H[i, j] = H[j, i] = (f(x + ei + ej) - f(x + ei - ej) - f(x - ei + ej) + f(x - ei - ej)) / (4 * h * h)
    return H


def num_jacobian(f, x, h=1e-6):
    f0 = np.asarray(f(x))
    J = np.zeros((len(f0), len(x)))
    for i in range(len(x)):
        e = np.zeros(len(x))
        e[i] = h
        J[:, i] = (np.asarray(f(x + e)) - np.asarray(f(x - e))) / (2 * h)
    return J


# =============================================================================
# HAMILTON (1989): SWITCHING MEAN AR(p) ON THE EXPANDED STATE, CONSTANT OR TIME-VARYING TRANSITIONS
# =============================================================================
def expanded_states(K, p):
    """All tuples (S_t, S_{t-1}, ..., S_{t-p}) and the transition map between them."""
    import itertools
    tup = np.array(list(itertools.product(range(K), repeat=p + 1)))       # column 0 = S_t
    M = len(tup)
    index = {tuple(r): i for i, r in enumerate(tup)}
    frm, to = [], []
    for i, r in enumerate(tup):
        for j0 in range(K):
            frm.append(i)
            to.append(index[(j0,) + tuple(r[:p])])
    return tup, np.array(frm), np.array(to)


def msm_logf(y, p, mu, phi, sig2, tup):
    """log f(y_t | S_t..S_{t-p}, Y_{t-1}) for y_t - mu_{S_t} = sum_k phi_k (y_{t-k} - mu_{S_{t-k}}) + e_t."""
    T = len(y) - p
    mus = mu[tup]                                   # M x (p+1)
    e = y[p:, None] - mus[None, :, 0]
    for k in range(1, p + 1):
        e = e - phi[k - 1] * (y[p - k:len(y) - k, None] - mus[None, :, k])
    return -0.5 * (np.log(2 * np.pi * sig2) + e ** 2 / sig2)


def expand_P(P2, K, p, tup, frm, to):
    """Transition matrix of the expanded state from the K x K regime matrix (constant or T x K x K)."""
    M = len(tup)
    if P2.ndim == 2:
        Pe = np.zeros((M, M))
        Pe[frm, to] = P2[tup[frm, 0], tup[to, 0]]
        return Pe
    Pe = np.zeros((P2.shape[0], M, M))
    Pe[:, frm, to] = P2[:, tup[frm, 0], tup[to, 0]]
    return Pe


def msm_unpack(th, K, p, Z=None):
    """theta = (mu_1..mu_K, phi_1..phi_p, log sigma2, transition parameters). Two regimes: constant (logit p11,
    logit p22) or TVTP: Pr(S_t = i | S_{t-1} = i) = logistic(z_{t-1}' gamma_i) (Diebold, Lee, Weinbach 1994)."""
    mu = th[:K]
    phi = th[K:K + p]
    sig2 = np.exp(th[K + p])
    g = th[K + p + 1:]
    if Z is None:
        q = 1 / (1 + np.exp(-g))
        P2 = np.array([[q[0], 1 - q[0]], [1 - q[1], q[1]]])
    else:
        nz = Z.shape[1]
        q1 = 1 / (1 + np.exp(-(Z @ g[:nz])))
        q2 = 1 / (1 + np.exp(-(Z @ g[nz:])))
        P2 = np.zeros((len(Z), 2, 2))
        P2[:, 0, 0], P2[:, 0, 1], P2[:, 1, 0], P2[:, 1, 1] = q1, 1 - q1, 1 - q2, q2
    return mu, phi, sig2, P2


def expanded_init(P2, K, p, tup):
    """Distribution of the first expanded state (S_p, ..., S_0): S_0 from the ergodic distribution of the first
    transition matrix, then p steps of the chain (with time-varying matrices, those of periods 1..p)."""
    pi = ergodic(P2[0] if P2.ndim == 3 else P2)
    J = {(s,): pi[s] for s in range(K)}
    for r in range(1, p + 1):
        Pr = P2[r] if P2.ndim == 3 else P2
        J = {(j,) + key: v * Pr[key[0], j] for key, v in J.items() for j in range(K)}
    return np.array([J[tuple(t)] for t in tup])


def msm_filter(th, y, K, p, Z=None, tup=None, frm=None, to=None):
    """Hamilton filter of the switching-mean AR(p). Z (optional): T x m transition covariates for the FULL sample y,
    row t holding the variables that drive Pr(S_t | S_{t-1}) (e.g. z_{t-1})."""
    if tup is None:
        tup, frm, to = expanded_states(K, p)
    mu, phi, sig2, P2 = msm_unpack(th, K, p, Z)
    Pe = expand_P(P2[p:] if Z is not None else P2, K, p, tup, frm, to)
    logf = msm_logf(y, p, mu, phi, sig2, tup)
    f = hamilton_filter(logf, Pe, expanded_init(P2, K, p, tup))
    return f, Pe, tup


def msm_negll(th, y, K, p, Z, tup, frm, to):
    try:
        return -msm_filter(th, y, K, p, Z, tup, frm, to)[0]['loglik']
    except (FloatingPointError, np.linalg.LinAlgError, ValueError):
        return 1e10


def msm_fit(y, p, K=2, Z=None, starts=None, seed=0, nrand=10):
    """Numerical ML of Hamilton's switching-mean AR(p) (BFGS from several starting values).
    Z: T x m matrix of transition covariates for the full sample y (row t holds z_{t-1}), or None."""
    y = np.asarray(y, float)
    tup, frm, to = expanded_states(K, p)
    rng = np.random.default_rng(seed)
    nz = 1 if Z is None else Z.shape[1]
    s = np.std(y)
    base = []
    for _ in range(nrand):
        mu0 = np.sort(np.mean(y) + s * rng.normal(0, 1, K))
        g0 = (rng.uniform(1, 3, 2) if Z is None else np.r_[rng.uniform(1, 3), np.zeros(nz - 1), rng.uniform(1, 3), np.zeros(nz - 1)])
        base.append(np.r_[mu0, rng.normal(0, 0.1, p), np.log(s ** 2 * rng.uniform(0.3, 1)), g0])
    best = None
    for th0 in (starts or []) + base:
        o = optimize.minimize(msm_negll, np.asarray(th0, float), args=(y, K, p, Z, tup, frm, to), method='BFGS',
                              options=dict(gtol=1e-6, maxiter=3000))
        if best is None or o.fun < best.fun:
            best = o
    f, Pe, _ = msm_filter(best.x, y, K, p, Z, tup, frm, to)
    sm, _ = kim_smoother(f['filt'], f['pred'], Pe)
    mu, phi, sig2, P2 = msm_unpack(best.x, K, p, Z)
    # regime probabilities of S_t: sum over the tuples with S_t = j
    agg = lambda a: np.column_stack([a[:, tup[:, 0] == j].sum(1) for j in range(K)])
    H = num_hessian(lambda t: msm_negll(t, y, K, p, Z, tup, frm, to), best.x)
    try:
        se_th = np.sqrt(np.diag(np.linalg.inv(H)))
    except np.linalg.LinAlgError:
        se_th = np.full(len(best.x), np.nan)
    return dict(theta=best.x, se_theta=se_th, mu=mu, phi=phi, sig2=sig2, P=P2, loglik=-best.fun,
                filt=agg(f['filt']), smooth=agg(sm), pred=agg(f['pred']), npar=len(best.x), T=len(y) - p)


# =============================================================================
# MARKOV-SWITCHING VAR (MSIAH) BY EM AND REGIME-DEPENDENT IMPULSE RESPONSES
# =============================================================================
def var_design(Y, p):
    Y = np.asarray(Y, float)
    X = np.column_stack([np.ones(len(Y) - p)] + [Y[p - k:len(Y) - k] for k in range(1, p + 1)])
    return Y[p:], X


def msvar_logf(Y, X, B, S):
    T, n = Y.shape
    K = len(B)
    out = np.empty((T, K))
    for j in range(K):
        E = Y - X @ B[j]
        L = np.linalg.cholesky(S[j])
        Z = np.linalg.solve(L, E.T)
        out[:, j] = -0.5 * (n * np.log(2 * np.pi) + 2 * np.log(np.diag(L)).sum() + (Z ** 2).sum(0))
    return out


def em_msvar(Y, p, K=2, maxit=2000, tol=1e-9, seed=0, starts=10):
    """EM for the MSIAH(K)-VAR(p): regime-dependent intercepts, lag matrices and covariances (Krolzig 1997, ch. 6);
    the M-step is a weighted multivariate least-squares regression in each regime."""
    Yt, X = var_design(Y, p)
    T, n = Yt.shape
    rng = np.random.default_rng(seed)
    best = None
    B_ols = np.linalg.lstsq(X, Yt, rcond=None)[0]
    S_ols = np.cov((Yt - X @ B_ols).T)
    for s in range(starts):
        W = rng.dirichlet(np.ones(K) * 0.5, size=T)
        W = np.array([np.convolve(W[:, j], np.ones(5) / 5, 'same') for j in range(K)]).T + 1e-3
        W /= W.sum(1, keepdims=True)
        P = np.full((K, K), 0.05 / max(K - 1, 1)) + np.eye(K) * (0.95 - 0.05 / max(K - 1, 1))
        B = [np.linalg.solve(X.T @ (X * W[:, [j]]), X.T @ (Yt * W[:, [j]])) for j in range(K)]
        S = [S_ols.copy() for _ in range(K)]
        path = []
        try:
            for it in range(maxit):
                f = hamilton_filter(msvar_logf(Yt, X, B, S), P)
                path.append(f['loglik'])
                sm, joint = kim_smoother(f['filt'], f['pred'], P)
                P = joint[1:].sum(0) / sm[:-1].sum(0)[:, None]
                P = np.clip(P, 1e-12, None)
                P /= P.sum(1, keepdims=True)
                for j in range(K):
                    w = sm[:, [j]]
                    B[j] = np.linalg.solve(X.T @ (X * w), X.T @ (Yt * w))
                    E = Yt - X @ B[j]
                    S[j] = (E * w).T @ E / w.sum() + 1e-8 * np.eye(n)
                if it > 2 and abs(path[-1] - path[-2]) < tol * (1 + abs(path[-1])):
                    break
        except np.linalg.LinAlgError:
            continue
        f = hamilton_filter(msvar_logf(Yt, X, B, S), P)
        if best is None or f['loglik'] > best['loglik']:
            sm, _ = kim_smoother(f['filt'], f['pred'], P)
            best = dict(B=[b.copy() for b in B], S=[x.copy() for x in S], P=P.copy(), loglik=f['loglik'], smooth=sm,
                        filt=f['filt'], iters=it + 1, T=T, n=n, p=p, K=K, npar=K * (n * (1 + n * p) + n * (n + 1) // 2) + K * (K - 1))
    return best


def regime_irf(B, S, n, p, H, shock=0):
    """Regime-dependent impulse responses (Ehrmann, Ellison and Valla 2003): the responses of the VAR of one regime
    to a one-standard-deviation orthogonalised (Cholesky) shock, assuming the regime stays in place for H periods."""
    A = [B[1 + n * (k - 1):1 + n * k].T for k in range(1, p + 1)]
    L = np.linalg.cholesky(S)
    Psi = [np.eye(n)]
    for h in range(1, H + 1):
        Psi.append(sum(A[k - 1] @ Psi[h - k] for k in range(1, min(h, p) + 1)))
    return np.array([Ps @ L[:, shock] for Ps in Psi])          # (H + 1) x n


# =============================================================================
# MARKOV-SWITCHING GARCH: HAAS-MITTNIK-PAOLELLA (2004) AND GRAY (1996)
# =============================================================================
def msgarch_unpack(th, K):
    mu = th[0]
    om = np.exp(th[1:1 + K])
    a = np.exp(th[1 + K:1 + 2 * K])
    b = np.exp(th[1 + 2 * K:1 + 3 * K])
    if K == 1:
        return mu, om, a, b, np.ones((1, 1))
    q = 1 / (1 + np.exp(-th[1 + 3 * K:1 + 3 * K + 2]))
    return mu, om, a, b, np.array([[q[0], 1 - q[0]], [1 - q[1], q[1]]])


def msgarch_filter(th, r, K=2, kind='hmp'):
    """Log-likelihood and filtered quantities of a K-regime GARCH(1,1) with Normal innovations and a common mean.
    kind='hmp': Haas, Mittnik and Paolella (2004), h_{j,t} = w_j + a_j e_{t-1}^2 + b_j h_{j,t-1} for every regime in
                parallel, so h_{j,t} does not depend on the regime path (no path dependence);
    kind='gray': Gray (1996), h_{j,t} = w_j + a_j e_{t-1}^2 + b_j h_{t-1}, with h_{t-1} the variance of the mixture
                 given Y_{t-2} (the regime history collapsed into one number).
    The recursion runs on plain Python floats (math module), which is fast for a scalar loop."""
    import math
    mu, om, a, b, P = msgarch_unpack(th, K)
    e = (np.asarray(r, float) - mu).tolist()
    om, a, b, Pl = om.tolist(), a.tolist(), b.tolist(), P.tolist()
    T = len(e)
    v0 = float(np.var(r))
    h = [v0] * K
    xi = list(ergodic(P)) if K > 1 else [1.0]
    ll = 0.0
    filt, pred, hpred = [], [], []
    hmix_prev = v0
    c = 0.5 * math.log(2 * math.pi)
    for t in range(T):
        if t > 0:
            e2 = e[t - 1] * e[t - 1]
            if kind == 'hmp':
                h = [om[j] + a[j] * e2 + b[j] * h[j] for j in range(K)]
            else:
                h = [om[j] + a[j] * e2 + b[j] * hmix_prev for j in range(K)]
            xi = [sum(xi[i] * Pl[i][j] for i in range(K)) for j in range(K)]
        hmix_prev = sum(xi[j] * h[j] for j in range(K))
        et2 = e[t] * e[t]
        dens = [xi[j] * math.exp(-c - 0.5 * math.log(h[j]) - 0.5 * et2 / h[j]) for j in range(K)]
        s = sum(dens)
        if not s > 0:
            return -1e10, None
        ll += math.log(s)
        pred.append(xi)
        hpred.append(h)
        xi = [d / s for d in dens]
        filt.append(xi)
    pred, hpred = np.array(pred), np.array(hpred)
    return ll, dict(filt=np.array(filt), pred=pred, h=hpred, hmix=(pred * hpred).sum(1))


def msgarch_fit(r, K=2, kind='hmp', starts=None):
    """Numerical ML (BFGS on log-parameters) of the (MS-)GARCH(1,1); K = 1 gives the ordinary GARCH(1,1)."""
    v = np.var(r)

    def nll(th):
        mu, om, a, b, P = msgarch_unpack(th, K)
        if np.any(a + b >= 0.9999):
            return 1e10
        ll, _ = msgarch_filter(th, r, K, kind)
        return -ll
    if starts is None:
        if K == 1:
            starts = [np.r_[np.mean(r), np.log(0.05 * v), np.log(0.08), np.log(0.9)]]
        else:                                   # starting values around the single-regime GARCH(1,1)
            g = msgarch_fit(r, 1)
            w, al, be = g['omega'][0], g['alpha'][0], g['beta'][0]
            starts = [np.r_[g['mu'], np.log([0.5 * w, 2.0 * w]), np.log([0.7 * al, 1.3 * al]), np.log([be, 0.97 * be]), 3.5, 2.5],
                      np.r_[g['mu'], np.log([0.3 * w, 3.0 * w]), np.log([0.5 * al, 1.5 * al]), np.log([min(be * 1.02, 0.97 - 0.5 * al), 0.9 * be]), 4.0, 3.0],
                      np.r_[g['mu'], np.log([0.02 * v, 0.2 * v]), np.log([0.05, 0.12]), np.log([0.92, 0.8]), 3.5, 2.5],
                      np.r_[g['mu'], np.log([0.01 * v, 0.05 * v]), np.log([0.03, 0.08]), np.log([0.95, 0.9]), 4.0, 3.0]]
    best = None
    for s0 in starts:
        o = optimize.minimize(nll, s0, method='BFGS', options=dict(gtol=1e-4, maxiter=400))
        if best is None or o.fun < best.fun:
            best = o
    mu, om, a, b, P = msgarch_unpack(best.x, K)
    ll, out = msgarch_filter(best.x, r, K, kind)
    return dict(theta=best.x, mu=mu, omega=om, alpha=a, beta=b, P=P, loglik=ll, npar=len(best.x), **out)


# =============================================================================
# BAYESIAN ESTIMATION: GIBBS SAMPLING WITH DATA AUGMENTATION
# =============================================================================
def gibbs_ms(y, K=2, n_iter=6000, burn=1000, seed=0, permute=False, prior=None, constrain='mean'):
    """Gibbs sampler for y_t = mu_{S_t} + sigma_{S_t} e_t (Albert and Chib 1993; Chib 1996):
      1. S | mu, sigma2, P, y  by forward filtering-backward sampling (the whole path in one block);
      2. P | S   rows ~ Dirichlet(a_ij + n_ij), n_ij = number of transitions i -> j;
      3. mu_j | sigma2_j, S, y ~ Normal (conjugate), sigma2_j | mu_j, S, y ~ inverse gamma;
      4. permute=True: random permutation of the labels at each sweep (Fruhwirth-Schnatter 2001), which visits all
         K! symmetric modes; the labels are then identified afterwards by the constraint mu_1 < ... < mu_K.
    Returns the draws (after burn-in) and the posterior mean of the regime probabilities."""
    rng = np.random.default_rng(seed)
    y = np.asarray(y, float)
    T = len(y)
    pr = dict(m0=np.mean(y), v0=100 * np.var(y), a0=2.0, d0=np.var(y), a_stay=8.0, a_move=2.0)
    pr.update(prior or {})
    q = np.quantile(y, np.linspace(0.2, 0.8, K))
    mu, sig2 = q.copy(), np.full(K, np.var(y))
    P = np.full((K, K), 0.1 / max(K - 1, 1)) + np.eye(K) * (0.9 - 0.1 / max(K - 1, 1))
    A = np.full((K, K), pr['a_move']) + np.eye(K) * (pr['a_stay'] - pr['a_move'])
    draws = dict(mu=[], sig2=[], P=[])
    prob = np.zeros((T, K))
    kept = 0
    for it in range(n_iter):
        logf = -0.5 * (np.log(2 * np.pi * sig2)[None, :] + (y[:, None] - mu[None, :]) ** 2 / sig2[None, :])
        f = hamilton_filter(logf, P)
        s = ffbs(f['filt'], P, rng)
        n = np.zeros((K, K))
        np.add.at(n, (s[:-1], s[1:]), 1)
        P = np.vstack([rng.dirichlet(A[i] + n[i]) for i in range(K)])
        for j in range(K):
            yj = y[s == j]
            vj = 1 / (1 / pr['v0'] + len(yj) / sig2[j])
            mu[j] = rng.normal(vj * (pr['m0'] / pr['v0'] + yj.sum() / sig2[j]), np.sqrt(vj))
            sig2[j] = 1 / rng.gamma(pr['a0'] + len(yj) / 2, 1 / (pr['d0'] + ((yj - mu[j]) ** 2).sum() / 2))
        if permute:
            o = rng.permutation(K)
            mu, sig2, P, s = mu[o], sig2[o], P[np.ix_(o, o)], np.argsort(o)[s]
        if it >= burn:
            draws['mu'].append(mu.copy())
            draws['sig2'].append(sig2.copy())
            draws['P'].append(P.copy())
            onehot = np.zeros((T, K))
            onehot[np.arange(T), s] = 1
            if constrain == 'mean':
                o = np.argsort(mu)
                onehot = onehot[:, o]
            prob += onehot
            kept += 1
    out = {k: np.array(v) for k, v in draws.items()}
    out['prob'] = prob / kept
    if constrain == 'mean':
        o = np.argsort(out['mu'], axis=1)
        idx = np.arange(len(o))[:, None]
        out['mu_id'] = out['mu'][idx, o]
        out['sig2_id'] = out['sig2'][idx, o]
        out['P_id'] = np.array([Pd[np.ix_(oo, oo)] for Pd, oo in zip(out['P'], o)])
    return out


# =============================================================================
# FORECASTS, SCORES, SIMULATION, LONG MEMORY
# =============================================================================
def msr_forecast(r, X_next, h=1):
    """h-step regime probabilities xi_{T+h|T} = (P')^h xi_{T|T} and the one-step mixture density moments
    for the next observation, given its regressors X_next (1 x k)."""
    xi = r['filt'][-1] @ np.linalg.matrix_power(r['P'], h)
    m = X_next @ r['beta'].T
    mean = float(xi @ m.ravel())
    var = float(xi @ (r['sig2'] + (m.ravel() - mean) ** 2))
    return xi, mean, var


def mixture_logscore(y, xi, means, sig2):
    return float(np.log(np.sum(xi * stats.norm.pdf(y, means, np.sqrt(sig2)))))


def mixture_pit(y, xi, means, sig2):
    return float(np.sum(xi * stats.norm.cdf(y, means, np.sqrt(sig2))))


def qps(prob, event):
    """Quadratic probability score (Brier 1950; Diebold and Rudebusch 1989): 2/T sum (p_t - d_t)^2, between 0 and 2."""
    prob, event = np.asarray(prob, float), np.asarray(event, float)
    return float(2 * np.mean((prob - event) ** 2))


def concordance(a, b):
    """Concordance index of Harding and Pagan (2002): share of periods in which two 0/1 phase indicators agree."""
    a, b = np.asarray(a, int), np.asarray(b, int)
    return float(np.mean(a * b + (1 - a) * (1 - b)))


def gph(x, power=0.5):
    """Geweke and Porter-Hudak log-periodogram estimate of the memory parameter d, m = T^power frequencies."""
    x = np.asarray(x, float) - np.mean(x)
    T = len(x)
    m = int(T ** power)
    lam = 2 * np.pi * np.arange(1, m + 1) / T
    I = np.abs(np.fft.fft(x)[1:m + 1]) ** 2 / (2 * np.pi * T)
    Xr = -np.log(4 * np.sin(lam / 2) ** 2)
    Xr = Xr - Xr.mean()
    return float(Xr @ np.log(I) / (Xr @ Xr))


def acf(x, L):
    x = np.asarray(x, float) - np.mean(x)
    d = x @ x
    return np.array([x[k:] @ x[:len(x) - k] / d for k in range(L + 1)])
