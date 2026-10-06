"""
lm_core.py -- the numpy engine of Chapter 10 (ATS): long memory and rough volatility
=====================================================================================
Everything is written with numpy/scipy, so the code can be read line by line and copied into the Colab notebooks:
  * fractional processes  fractional differencing weights, ARFIMA autocovariances, fractional Gaussian noise,
                          exact simulation by circulant embedding (Davies and Harte 1987), the hybrid scheme of
                          Bennedsen, Lunde and Pakkanen (2017) for Riemann-Liouville fractional processes;
  * semiparametric d      periodogram, GPH (Geweke and Porter-Hudak 1983), local Whittle (Robinson 1995),
                          exact local Whittle with unknown mean (Shimotsu and Phillips 2005; Shimotsu 2010),
                          local Whittle with additive noise (Hurvich, Moulines and Soulier 2005), Qu (2011) test;
  * fractional cointegration  FCVAR with k = 0 lags by profile likelihood (Johansen and Nielsen 2012), narrow-band
                          least squares (Robinson 1994);
  * volatility            FIGARCH, HYGARCH and GARCH(1,1) with Student t innovations (ARCH(infinity) weights by FFT);
  * rough volatility      variogram scaling of log volatility (Gatheral, Jaisson and Rosenbaum 2018), the same with a
                          measurement-error intercept, the RFSV forecasting kernel; HAR and ARFIMA forecasts of log RV;
  * evaluation            QLIKE, Newey-West long-run variance, Diebold-Mariano statistic.
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import numpy as np
from scipy import integrate, optimize, signal, special, stats


# =============================================================================
# 1. FRACTIONAL PROCESSES
# =============================================================================
def frac_weights(d, n):
    """Coefficients pi_k of (1 - L)^d, k = 0..n-1: pi_0 = 1, pi_k = pi_{k-1}(k - 1 - d)/k."""
    w = np.empty(n)
    w[0] = 1.0
    k = np.arange(1, n)
    w[1:] = np.cumprod((k - 1 - d) / k)
    return w


def frac_diff(x, d):
    """Type II fractional difference (1 - L)^d x_t with x_t = 0 for t <= 0, by FFT convolution; works on columns."""
    x = np.asarray(x, float)
    n = x.shape[0]
    w = frac_weights(d, n)
    nfft = 1 << (2 * n - 1).bit_length()
    W = np.fft.rfft(w, nfft)
    if x.ndim == 1:
        return np.fft.irfft(np.fft.rfft(x, nfft) * W, nfft)[:n]
    return np.fft.irfft(np.fft.rfft(x, nfft, axis=0) * W[:, None], nfft, axis=0)[:n]


def arfima_acov(d, n, sigma2=1.0):
    """Autocovariances gamma(0..n-1) of ARFIMA(0, d, 0), |d| < 1/2 (Hosking 1981)."""
    g = np.empty(n)
    g[0] = sigma2 * special.gamma(1 - 2 * d) / special.gamma(1 - d) ** 2
    k = np.arange(1, n)
    g[1:] = g[0] * np.cumprod((k - 1 + d) / (k - d))
    return g


def arfima_acf(d, n):
    return arfima_acov(d, n) / arfima_acov(d, 1)[0]


def fgn_acov(H, n):
    """Autocovariances of fractional Gaussian noise with unit variance: (|k+1|^2H - 2|k|^2H + |k-1|^2H)/2."""
    k = np.arange(n, dtype=float)
    return 0.5 * (np.abs(k + 1) ** (2 * H) - 2 * k ** (2 * H) + np.abs(k - 1) ** (2 * H))


def circulant_sim(acov, rng, n_paths=1):
    """Exact simulation of a stationary Gaussian series with autocovariances acov[0..n-1] by circulant embedding
    (Davies and Harte 1987; Dietrich and Newsam 1997). Returns an (n_paths, n) array."""
    acov = np.asarray(acov, float)
    n = len(acov)
    c = np.concatenate([acov, acov[-2:0:-1]])
    lam = np.fft.fft(c).real
    if lam.min() < -1e-8 * lam.max():
        raise ValueError('circulant embedding is not non-negative definite')
    lam = np.clip(lam, 0, None)
    M = len(c)
    k = (n_paths + 1) // 2
    Z = rng.standard_normal((k, M)) + 1j * rng.standard_normal((k, M))
    Y = np.fft.fft(np.sqrt(lam / M) * Z, axis=1)
    out = np.vstack([Y.real[:, :n], Y.imag[:, :n]])
    return out[:n_paths]


def circulant_eigs(acov):
    c = np.concatenate([acov, acov[-2:0:-1]])
    return np.fft.fft(c).real


def sim_arfima(n, d, rng, phi=0.0, theta=0.0, burn=500, n_paths=1):
    """ARFIMA(1, d, 1) paths: exact ARFIMA(0, d, 0) by circulant embedding, then the ARMA filter (burn-in dropped).
    For d >= 1/2 the series is the partial sum of an ARFIMA(0, d - 1, 0)."""
    if d >= 0.5:
        x = sim_arfima(n, d - 1, rng, phi, theta, burn, n_paths)
        return np.cumsum(x, axis=1)
    x = circulant_sim(arfima_acov(d, n + burn), rng, n_paths)
    if phi or theta:
        x = signal.lfilter([1.0, theta], [1.0, -phi], x, axis=1)
    return x[:, burn:]


def fbm(n, H, rng, n_paths=1, T=1.0):
    """Fractional Brownian motion on a grid of n steps over [0, T] (cumulated exact fGn); B_0 = 0 included."""
    g = circulant_sim(fgn_acov(H, n), rng, n_paths) * (T / n) ** H
    return np.hstack([np.zeros((n_paths, 1)), np.cumsum(g, axis=1)])


def hybrid_rl(n, H, rng, n_paths=1, T=1.0, kappa=1):
    """Riemann-Liouville process X(t) = int_0^t (t - s)^(H - 1/2) dW(s) on n steps over [0, T].
    kappa = 1: the hybrid scheme of Bennedsen, Lunde and Pakkanen (2017) (exact Wiener integral on the first cell,
    optimal evaluation points b_k on the others); kappa = 0: the plain forward Riemann sum (kernel at k/n)."""
    a = H - 0.5
    dt = T / n
    k = np.arange(1, n + 1, dtype=float)
    if kappa == 1:
        cov = np.array([[dt, dt ** (a + 1) / (a + 1)], [dt ** (a + 1) / (a + 1), dt ** (2 * a + 1) / (2 * a + 1)]])
        L = np.linalg.cholesky(cov)
        Z = rng.standard_normal((n_paths, n, 2)) @ L.T
        dW, first = Z[..., 0], Z[..., 1]
        b = ((k ** (a + 1) - (k - 1) ** (a + 1)) / (a + 1)) ** (1 / a)
        g = (b * dt) ** a
        g[0] = 0.0                                  # the first cell is the exact integral
    else:
        dW = rng.standard_normal((n_paths, n)) * np.sqrt(dt)
        first = 0.0
        g = (k * dt) ** a
    nfft = 1 << (2 * n - 1).bit_length()
    conv = np.fft.irfft(np.fft.rfft(dW, nfft, axis=1) * np.fft.rfft(g, nfft)[None, :], nfft, axis=1)[:, :n]
    X = conv + first
    return np.hstack([np.zeros((n_paths, 1)), X])


# =============================================================================
# 2. SEMIPARAMETRIC ESTIMATION OF d
# =============================================================================
def periodogram(x, m=None, demean=True):
    """Periodogram I(lambda_j) = |sum_t x_t e^{-i lambda_j t}|^2 / (2 pi n) at lambda_j = 2 pi j / n, j = 1..m."""
    x = np.asarray(x, float)
    n = len(x)
    X = np.fft.fft(x - x.mean() if demean else x)
    m = m or n // 2
    j = np.arange(1, m + 1)
    return 2 * np.pi * j / n, np.abs(X[1:m + 1]) ** 2 / (2 * np.pi * n)


def bandwidth(n, a):
    return int(np.floor(n ** a))


def gph(x, m):
    """Log-periodogram (GPH) estimator: OLS of log I on -log(4 sin^2(lambda/2)); returns (d, asymptotic SE pi/sqrt(24m),
    OLS SE)."""
    lam, I = periodogram(x, m)
    X = -np.log(4 * np.sin(lam / 2) ** 2)
    Y = np.log(I)
    Xc = X - X.mean()
    d = Xc @ (Y - Y.mean()) / (Xc @ Xc)
    u = Y - Y.mean() - d * Xc
    return float(d), float(np.pi / np.sqrt(24 * m)), float(np.sqrt(u @ u / (m - 2) / (Xc @ Xc)))


def lw_objective(d, lam, I):
    return np.log(np.mean(lam ** (2 * d) * I)) - 2 * d * np.mean(np.log(lam))


def local_whittle(x, m, lo=-0.49, hi=1.49):
    """Local Whittle (Gaussian semiparametric) estimator of Robinson (1995); SE 1/(2 sqrt(m))."""
    lam, I = periodogram(x, m)
    grid = np.linspace(lo, hi, 41)
    g0 = grid[np.argmin([lw_objective(d, lam, I) for d in grid])]
    r = optimize.minimize_scalar(lw_objective, bounds=(max(lo, g0 - 0.06), min(hi, g0 + 0.06)), args=(lam, I),
                                 method='bounded', options=dict(xatol=1e-6))
    return float(r.x), float(1 / (2 * np.sqrt(m)))


def shimotsu_weight(d):
    """Weight on the sample mean in the unknown-mean ELW of Shimotsu (2010): 1 for d <= 1/2, 0 for d >= 3/4."""
    if d <= 0.5:
        return 1.0
    if d >= 0.75:
        return 0.0
    return 0.5 * (1 + np.cos(4 * np.pi * d))


def elw_objective(d, x, m, mean=True):
    n = len(x)
    if mean:
        w = shimotsu_weight(d)
        x = x - (w * x.mean() + (1 - w) * x[0])
    v = frac_diff(x, d)
    V = np.fft.fft(v)
    j = np.arange(1, m + 1)
    lam = 2 * np.pi * j / n
    I = np.abs(V[1:m + 1]) ** 2 / (2 * np.pi * n)
    return np.log(np.mean(I)) - 2 * d * np.mean(np.log(lam))


def elw(x, m, lo=-0.49, hi=2.0, mean=True):
    """Exact local Whittle estimator (Shimotsu and Phillips 2005) with the unknown-mean correction of Shimotsu (2010);
    consistent and N(d, 1/(4m)) for any d in the search range."""
    x = np.asarray(x, float)
    grid = np.linspace(lo, hi, 51)
    g0 = grid[np.argmin([elw_objective(d, x, m, mean) for d in grid])]
    r = optimize.minimize_scalar(elw_objective, bounds=(max(lo, g0 - 0.06), min(hi, g0 + 0.06)), args=(x, m, mean),
                                 method='bounded', options=dict(xatol=1e-6))
    return float(r.x), float(1 / (2 * np.sqrt(m)))


def lwn(x, m):
    """Local Whittle with additive noise (Hurvich, Moulines and Soulier 2005): f(lambda) = G(lambda^-2d + theta),
    theta >= 0 the noise-to-signal ratio; returns (d, theta)."""
    lam, I = periodogram(x, m)

    def obj(p):
        d, th = p
        g = lam ** (-2 * d) + th
        return np.log(np.mean(I / g)) + np.mean(np.log(g))
    best = None
    for d0 in (0.1, 0.3, 0.5):
        for t0 in (0.0, 1.0, 10.0):
            r = optimize.minimize(obj, [d0, t0], bounds=[(-0.49, 0.99), (0.0, 1e4)], method='L-BFGS-B')
            if best is None or r.fun < best.fun:
                best = r
    return float(best.x[0]), float(best.x[1])


def lbias_constant(phi):
    """Leading bias constant of GPH / local Whittle for ARFIMA(1, d, 0): bias ~ C (m/n)^2 with
    C = -(2 pi^2/9) f*''(0)/f*(0) = (2 pi^2/9) 2 phi/(1 - phi)^2."""
    return 2 * np.pi ** 2 / 9 * 2 * phi / (1 - phi) ** 2


def mse_opt_m(n, C):
    """MSE-optimal bandwidth of local Whittle: bias^2 + 1/(4m) with bias C (m/n)^2 -> m* = (n^4/(16 C^2))^(1/5)."""
    return (n ** 4 / (16 * C ** 2)) ** 0.2


# =============================================================================
# 3. SHORT OR LONG MEMORY: THE QU (2011) TEST
# =============================================================================
def qu_stat(x, m, eps=0.02):
    """Qu (2011) statistic W = sup_{r in [eps, 1]} |sum_{j <= mr} nu_j (lambda_j^{2d} I_j / G - 1)| / sqrt(sum nu_j^2),
    with d and G the local Whittle estimates on the same m frequencies."""
    lam, I = periodogram(x, m)
    d, _ = local_whittle(x, m)
    G = np.mean(lam ** (2 * d) * I)
    nu = np.log(lam) - np.mean(np.log(lam))
    S = np.cumsum(nu * (lam ** (2 * d) * I / G - 1))
    r0 = max(int(np.floor(eps * m)), 1)
    return float(np.max(np.abs(S[r0 - 1:])) / np.sqrt(nu @ nu)), d


def qu_critical(eps=0.02, n=16384, a=0.7, reps=2000, seed=11):
    """Critical values of the Qu statistic simulated under Gaussian white noise (its null limit does not depend on d)."""
    rng = np.random.default_rng(seed)
    m = bandwidth(n, a)
    W = np.array([qu_stat(rng.standard_normal(n), m, eps)[0] for _ in range(reps)])
    return {str(q): float(np.quantile(W, q)) for q in (0.90, 0.95, 0.99)}


def random_level_shift(n, rng, p=0.005, s_shift=1.0, s_noise=1.0, phi=0.0):
    """Short memory plus random level shifts (Lu and Perron 2010): y = mu_t + u_t, mu_t jumps with probability p."""
    jumps = (rng.random(n) < p) * rng.normal(0, s_shift, n)
    u = signal.lfilter([1.0], [1.0, -phi], rng.normal(0, s_noise, n))
    return np.cumsum(jumps) + u


# =============================================================================
# 4. FRACTIONAL COINTEGRATION
# =============================================================================
def fcvar_loglik(X, d, b, r):
    """Concentrated log-likelihood of the FCVAR with k = 0 lags (Johansen and Nielsen 2012),
    Delta^d X_t = alpha beta' L_b Delta^(d-b) X_t + eps_t, L_b = 1 - Delta^b, X demeaned; rank r."""
    Z0 = frac_diff(X, d)
    Z1 = frac_diff(X, d - b) - Z0
    T = X.shape[0]
    S00, S11, S01 = Z0.T @ Z0 / T, Z1.T @ Z1 / T, Z0.T @ Z1 / T
    ll = -T / 2 * np.log(np.linalg.det(S00))
    if r == 0:
        return ll, None
    A = np.linalg.solve(S11, S01.T @ np.linalg.solve(S00, S01))
    ev, V = np.linalg.eig(A)
    o = np.argsort(-ev.real)
    ev, V = ev.real[o], V.real[:, o]
    ll -= T / 2 * np.sum(np.log(1 - ev[:r]))
    beta = V[:, :r]
    beta = beta / beta[0]
    alpha = S01 @ beta @ np.linalg.inv(beta.T @ S11 @ beta)
    return ll, dict(ev=ev, beta=beta, alpha=alpha)


def fcvar_fit(X, dgrid, bstep=0.02):
    """Profile likelihood over (d, b) for ranks 0, 1 and p; trace statistics; estimates at the rank-1 maximum."""
    X = np.asarray(X, float) - np.asarray(X, float).mean(0)
    p = X.shape[1]
    best = {0: (-np.inf, None), 1: (-np.inf, None), p: (-np.inf, None)}
    surf = []
    for d in dgrid:
        l0 = fcvar_loglik(X, d, 0.5 * d, 0)[0]
        if l0 > best[0][0]:
            best[0] = (l0, (d, None))
        for b in np.arange(bstep, d + 1e-9, bstep):
            for r in (1, p):
                ll, _ = fcvar_loglik(X, d, b, r)
                if ll > best[r][0]:
                    best[r] = (ll, (d, b))
                if r == 1:
                    surf.append((d, b, ll))
    d1, b1 = best[1][1]
    _, est = fcvar_loglik(X, d1, b1, 1)
    out = dict(d=d1, b=b1, beta=est['beta'][:, 0].tolist(), alpha=est['alpha'][:, 0].tolist(),
               ll0=best[0][0], ll1=best[1][0], llp=best[p][0], d0=best[0][1][0], dp=best[p][1][0], bp=best[p][1][1],
               surf=np.array(surf))
    out['trace0'] = 2 * (out['llp'] - out['ll0'])
    out['trace1'] = 2 * (out['llp'] - out['ll1'])
    out['p0'] = float(stats.chi2.sf(out['trace0'], p ** 2))
    out['p1'] = float(stats.chi2.sf(out['trace1'], (p - 1) ** 2))
    return out


def nbls(y, x, m):
    """Narrow-band least squares (Robinson 1994): beta = Re sum_{j<=m} I_xy / sum_{j<=m} I_xx."""
    n = len(y)
    Y, Xf = np.fft.fft(y - y.mean()), np.fft.fft(x - x.mean())
    j = np.arange(1, m + 1)
    return float(np.real(np.sum(Xf[j] * np.conj(Y[j]))) / np.sum(np.abs(Xf[j]) ** 2))


# =============================================================================
# 5. LONG MEMORY IN VOLATILITY: FIGARCH, HYGARCH, GARCH
# =============================================================================
def arch_inf_weights(kind, par, K):
    """ARCH(infinity) weights lambda_1..lambda_K of sigma^2_t = omega/(1 - beta) + sum_k lambda_k eps^2_{t-k}.
    FIGARCH(1,d,1) (Baillie, Bollerslev and Mikkelsen 1996): 1 - (1 - beta L)^-1 (1 - phi L)(1 - L)^d;
    HYGARCH (Davidson 2004): the same with (1 - L)^d replaced by 1 + a((1 - L)^d - 1); GARCH(1,1): a L/(1 - beta L)."""
    if kind == 'garch':
        a, beta = par
        return a * beta ** np.arange(K)
    if kind == 'figarch':
        d, phi, beta = par
        amp = 1.0
    else:
        d, phi, beta, amp = par
    w = amp * frac_weights(d, K + 1)
    w[0] += 1 - amp
    bb = np.convolve([1.0, -phi], w)[:K + 1]
    c = signal.lfilter([1.0], [1.0, -beta], bb)
    lam = -c
    lam[0] += 1
    return lam[1:]


def arch_inf_sigma2(e2, const, lam, init=None):
    """sigma^2_t = const + sum_k lambda_k e2_{t-k}, pre-sample e2 set to their mean, by FFT convolution."""
    K, n = len(lam), len(e2)
    pre = np.full(K, e2.mean() if init is None else init)
    z = np.concatenate([pre, e2])
    s = signal.fftconvolve(z, np.concatenate([[0.0], lam]))[K:K + n]
    return const + s


def _t_loglik(e, s2, nu):
    z2 = e ** 2 / s2
    c = special.gammaln((nu + 1) / 2) - special.gammaln(nu / 2) - 0.5 * np.log(np.pi * (nu - 2))
    return c - 0.5 * np.log(s2) - (nu + 1) / 2 * np.log1p(z2 / (nu - 2))


def ltm_negll(theta, e, kind, K):
    if kind == 'garch':
        om, a, beta, nu = theta
        if a < 0 or beta < 0 or a + beta >= 0.9999:
            return 1e10
        lam = arch_inf_weights('garch', (a, beta), K)
        const = om / (1 - beta)
    elif kind == 'figarch':
        om, d, phi, beta, nu = theta
        if not (0 < d < 1 and 0 <= phi < 1 and 0 <= beta < 1 and beta - d <= phi):
            return 1e10
        lam = arch_inf_weights('figarch', (d, phi, beta), K)
        const = om / (1 - beta)
    else:
        om, d, phi, beta, amp, nu = theta
        if not (0 < d < 1 and 0 <= phi < 1 and 0 <= beta < 1 and 0 <= amp < 3):
            return 1e10
        lam = arch_inf_weights('hygarch', (d, phi, beta, amp), K)
        const = om / (1 - beta)
    if om <= 0 or nu <= 2.05 or lam.min() < -1e-8:
        return 1e10
    s2 = arch_inf_sigma2(e ** 2, const, lam)
    if s2.min() <= 0:
        return 1e10
    return -np.sum(_t_loglik(e, s2, nu))


def ltm_fit(r, kind='figarch', K=1000):
    """Student t QML of GARCH(1,1), FIGARCH(1,d,1) or HYGARCH on demeaned returns (in %), ARCH(infinity) truncated at K."""
    e = np.asarray(r, float) - np.mean(r)
    v = e.var()
    starts = {'garch': [[0.02 * v, 0.08, 0.90, 6.0], [0.05 * v, 0.12, 0.85, 5.0]],
              'figarch': [[0.02 * v, 0.40, 0.20, 0.50, 6.0], [0.05 * v, 0.30, 0.10, 0.30, 5.0], [0.03 * v, 0.55, 0.30, 0.70, 6.0]],
              'hygarch': [[0.02 * v, 0.40, 0.20, 0.50, 0.95, 6.0], [0.03 * v, 0.55, 0.30, 0.70, 0.80, 5.0]]}[kind]
    best = None
    for s0 in starts:
        r_ = optimize.minimize(ltm_negll, s0, args=(e, kind, K), method='Nelder-Mead',
                               options=dict(maxiter=4000, maxfev=6000, xatol=1e-6, fatol=1e-6))
        if best is None or r_.fun < best.fun:
            best = r_
    k = len(best.x)
    return dict(par=best.x.tolist(), ll=float(-best.fun), bic=float(2 * best.fun + k * np.log(len(e))), k=k)


# =============================================================================
# 6. ROUGH VOLATILITY
# =============================================================================
def variogram(x, lags, q=2.0):
    """m(q, Delta) = mean |x_{t+Delta} - x_t|^q for each lag Delta."""
    x = np.asarray(x, float)
    return np.array([np.mean(np.abs(x[L:] - x[:-L]) ** q) for L in lags])


def gjr_scaling(logsig, lags=tuple(range(1, 51)), qs=(0.5, 1.0, 1.5, 2.0, 3.0)):
    """Gatheral, Jaisson and Rosenbaum (2018): log m(q, Delta) = zeta_q log Delta + c_q; zeta_q = q H;
    H by least squares of zeta_q on q through the origin; nu from m(2, Delta) = nu^2 Delta^(2H)."""
    L = np.log(np.asarray(lags, float))
    zeta, icpt = [], []
    for q in qs:
        b, a = np.polyfit(L, np.log(variogram(logsig, lags, q)), 1)
        zeta.append(b)
        icpt.append(a)
    zeta, qs_ = np.array(zeta), np.array(qs)
    H = float(qs_ @ zeta / (qs_ @ qs_))
    i2 = list(qs).index(2.0)
    return dict(zeta=zeta.tolist(), H=H, H2=float(zeta[i2] / 2), nu=float(np.exp(icpt[i2] / 2)), qs=list(qs))


def h_with_noise(logsig, lags=tuple(range(1, 51))):
    """m(2, Delta) = nu^2 Delta^(2H) + 2 s^2: the variogram of a rough log volatility observed with i.i.d.
    measurement error of variance s^2 (nonlinear least squares on the log scale)."""
    m2 = variogram(logsig, lags, 2.0)
    lg = np.asarray(lags, float)

    def res(p):
        lnu2, H, ls2 = p
        return np.log(np.exp(lnu2) * lg ** (2 * H) + 2 * np.exp(ls2)) - np.log(m2)
    best = None
    for H0 in (0.05, 0.15, 0.3, 0.5):
        for f in (0.1, 0.5):
            p0 = [np.log(m2[0] * (1 - f)), H0, np.log(m2[0] * f / 2)]
            r = optimize.least_squares(res, p0, bounds=([-20, 0.005, -30], [5, 0.99, 5]))
            if best is None or r.cost < best.cost:
                best = r
    lnu2, H, ls2 = best.x
    return dict(H=float(H), nu=float(np.exp(lnu2 / 2)), s2=float(np.exp(ls2)), share=float(2 * np.exp(ls2) / m2[0]))


def rfsv_kernel(H, h, K=500):
    """Weights w_k, k = 0..K-1, of the RFSV predictor of Gatheral, Jaisson and Rosenbaum (2018):
    E[log sigma^2_{t+h} | F_t] = cos(H pi)/pi h^(H+1/2) int log sigma^2_s / ((t - s + h)(t - s)^(H+1/2)) ds,
    with log sigma^2 constant over each day (day t - k covers t - s in [k, k + 1)); normalised to sum to one."""
    a = H + 0.5
    w = np.array([integrate.quad(lambda u: 1.0 / ((u + h) * u ** a), k, k + 1, limit=200)[0] for k in range(K)])
    return w / w.sum()


def rfsv_c(H):
    """c = Gamma(3/2 - H) / (Gamma(H + 1/2) Gamma(2 - 2H)) of the RFSV variance forecast exp(E log sigma^2 + 2 c nu^2 h^2H)."""
    return special.gamma(1.5 - H) / (special.gamma(H + 0.5) * special.gamma(2 - 2 * H))


def har_design(y):
    """HAR regressors of a daily series y (log RV): 1, y_t, mean of y_{t-4..t}, mean of y_{t-21..t}."""
    s = np.asarray(y, float)
    c = np.concatenate([[0.0], np.cumsum(s)])
    n = len(s)
    t = np.arange(21, n)
    w = (c[t + 1] - c[t - 4]) / 5
    mo = (c[t + 1] - c[t - 21]) / 22
    return t, np.column_stack([np.ones(len(t)), s[t], w, mo])


def har_ar_weights(b):
    """AR(22) coefficients implied by HAR coefficients (b_d, b_w, b_m) (Corsi 2009)."""
    bd, bw, bm = b
    w = np.zeros(22)
    w[0] += bd
    w[:5] += bw / 5
    w[:22] += bm / 22
    return w


def nw_lrv(x, L):
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    v = x @ x / n
    for k in range(1, L + 1):
        v += 2 * (1 - k / (L + 1)) * (x[k:] @ x[:-k]) / n
    return v


def dm_stat(l1, l2, h=1):
    """Diebold-Mariano t statistic of mean(l1 - l2) with a Newey-West variance (lag max(h - 1, 0) + a rule-of-thumb),
    and its two-sided Normal p-value."""
    dlt = np.asarray(l1) - np.asarray(l2)
    n = len(dlt)
    L = max(h - 1, int(np.floor(4 * (n / 100) ** (2 / 9))))
    t = dlt.mean() / np.sqrt(nw_lrv(dlt, L) / n)
    return float(t), float(2 * stats.norm.sf(abs(t)))


def qlike(rv, f):
    x = np.asarray(rv) / np.asarray(f)
    return x - np.log(x) - 1
