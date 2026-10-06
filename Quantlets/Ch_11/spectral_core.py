"""
spectral_core.py -- the numpy engine of Chapter 11 (ATS): spectral and wavelet analysis
=======================================================================================
Everything is written in numpy/scipy so that each formula on the slides can be read in the code:
  * spectra       periodogram, lag-window (Bartlett, Parzen, quadratic-spectral) and Daniell estimators, Andrews
                  plug-in bandwidths, multitaper (Thomson 1982) with adaptive weights, chi-square bands and the
                  harmonic F test, theoretical ARMA spectra;
  * two series    multitaper cross-spectrum, squared coherence with its null threshold, phase and gain, dynamic
                  correlation (Croux, Forni and Reichlin 2001);
  * causality     VAR(p) by OLS, the Geweke (1982) frequency-domain causality measure, the Breitung-Candelon (2006)
                  test of no causality at a frequency;
  * filters       Hodrick-Prescott, Baxter-King, Hamilton (2018) regression filter and their gains;
  * wavelets      MODWT and multiresolution analysis (Percival and Walden 2000) with any orthonormal filter of
                  PyWavelets, wavelet variance, correlation and beta by scale with confidence intervals;
                  continuous Morlet transform (Torrence and Compo 1998), cone of influence, red-noise significance,
                  cross-wavelet transform, smoothed wavelet coherence and phase (Grinsted et al. 2004) with Monte
                  Carlo significance.
Conventions: f(w) = (2 pi)^-1 sum_h gamma(h) exp(-i w h) on [-pi, pi]; white noise has f = sigma^2 / (2 pi).
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import numpy as np
from scipy import linalg, signal, sparse, stats
from scipy.sparse.linalg import spsolve


# =============================================================================
# UNIVARIATE SPECTRA
# =============================================================================
def fourier_freqs(n):
    """Positive Fourier frequencies w_j = 2 pi j / n, j = 1, ..., floor(n/2)."""
    return 2 * np.pi * np.arange(1, n // 2 + 1) / n


def periodogram(x, taper=None):
    """I(w_j) = |sum_t x_t exp(-i w_j t)|^2 / (2 pi n) at the positive Fourier frequencies (mean removed).
    With a taper h_t the data are multiplied by h_t / sqrt(mean h_t^2), so that E I is still about f."""
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    if taper is not None:
        h = np.asarray(taper, float)
        x = x * h / np.sqrt(np.mean(h ** 2))
    X = np.fft.rfft(x)
    return fourier_freqs(n), (np.abs(X) ** 2 / (2 * np.pi * n))[1:n // 2 + 1]


def acov(x, maxlag):
    """Sample autocovariances gamma(0..maxlag) with divisor n."""
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    g = np.fft.irfft(np.abs(f) ** 2)[:maxlag + 1] / n
    return g


def kernel(u, name):
    """Lag windows k(u): Bartlett, Parzen, quadratic spectral (QS), Tukey-Hanning."""
    u = np.abs(np.asarray(u, float))
    if name == 'bartlett':
        return np.where(u <= 1, 1 - u, 0.0)
    if name == 'parzen':
        return np.where(u <= 0.5, 1 - 6 * u ** 2 + 6 * u ** 3, np.where(u <= 1, 2 * (1 - u) ** 3, 0.0))
    if name == 'tukey':
        return np.where(u <= 1, 0.5 * (1 + np.cos(np.pi * u)), 0.0)
    if name == 'qs':
        z = 6 * np.pi * u / 5
        with np.errstate(invalid='ignore', divide='ignore'):
            k = 25 / (12 * np.pi ** 2 * u ** 2) * (np.sin(z) / z - np.cos(z))
        return np.where(u == 0, 1.0, k)
    raise KeyError(name)


# characteristic exponent q, k_q = lim (1 - k(u)) / |u|^q, and int k^2 (Andrews 1991, Table 1 and eq. 5.2)
KERNEL_CONST = {'bartlett': (1, 1.0, 2 / 3), 'parzen': (2, 6.0, 0.539285), 'qs': (2, 1.421223, 1.0),
                'tukey': (2, np.pi ** 2 / 4, 0.75)}


def lag_window(x, M, name='parzen', omega=None):
    """f_hat(w) = (2 pi)^-1 sum_{|h| < n} k(h/M) gamma_hat(h) exp(-i w h) on a grid (default: Fourier freqs)."""
    n = len(x)
    omega = fourier_freqs(n) if omega is None else np.asarray(omega, float)
    H = n - 1 if name == 'qs' else int(min(np.ceil(M), n - 1))
    g = acov(x, H)
    h = np.arange(1, H + 1)
    w = kernel(h / M, name)
    return omega, (g[0] + 2 * (w * g[1:]) @ np.cos(np.outer(h, omega))) / (2 * np.pi)


def andrews_bandwidth(x, name='bartlett'):
    """Andrews (1991) AR(1) plug-in bandwidth for the spectrum at frequency zero (the HAC bandwidth of Chapter 0)."""
    x = np.asarray(x, float) - np.mean(x)
    rho = float(np.dot(x[1:], x[:-1]) / np.dot(x[:-1], x[:-1]))
    n = len(x)
    if name == 'bartlett':
        a1 = 4 * rho ** 2 / ((1 - rho) ** 2 * (1 + rho) ** 2)
        return 1.1447 * (a1 * n) ** (1 / 3)
    a2 = 4 * rho ** 2 / (1 - rho) ** 4
    return {'parzen': 2.6614, 'qs': 1.3221, 'tukey': 1.7462}[name] * (a2 * n) ** (1 / 5)


def daniell(x, m, taper=None):
    """Daniell estimator: average of 2m+1 neighbouring periodogram ordinates (reflected at the ends)."""
    w, I = periodogram(x, taper)
    Ip = np.concatenate([I[m:0:-1], I, I[-2:-m - 2:-1]])
    return w, np.convolve(Ip, np.ones(2 * m + 1) / (2 * m + 1), mode='valid')


def welch(x, nseg, overlap=0.5):
    """Welch (1967): average of Hann-tapered periodograms of overlapping segments of length nseg."""
    x = np.asarray(x, float) - np.mean(x)
    step = int(nseg * (1 - overlap))
    h = signal.windows.hann(nseg, sym=False)
    P = [periodogram(x[s:s + nseg], h)[1] for s in range(0, len(x) - nseg + 1, step)]
    return fourier_freqs(nseg), np.mean(P, axis=0)


_DPSS = {}


def dpss(n, NW, K):
    """Slepian (DPSS) tapers, unit energy, with their concentration ratios lambda_k (cached)."""
    if (n, NW, K) not in _DPSS:
        _DPSS[(n, NW, K)] = signal.windows.dpss(n, NW, K, return_ratios=True)
    return _DPSS[(n, NW, K)]


def eigenspectra(x, NW=4, K=None, nfft=None):
    """Tapered DFTs Y_k(w) = sum_t v_t^(k) x_t exp(-i w t) (k = 0..K-1) and the eigenspectra |Y_k|^2 / (2 pi)."""
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    K = K or int(2 * NW - 1)
    v, lam = dpss(n, NW, K)
    nfft = nfft or n
    Y = np.fft.rfft(v * x, nfft, axis=1)[:, 1:nfft // 2 + 1]
    w = 2 * np.pi * np.arange(1, nfft // 2 + 1) / nfft
    return w, Y, np.abs(Y) ** 2 / (2 * np.pi), v, lam


def multitaper(x, NW=4, K=None, adaptive=False, nfft=None, level=0.95):
    """Thomson (1982) multitaper estimate: the average of K eigenspectra (or Thomson's adaptive weights),
    with the chi-square band 2 nu f_hat / f ~ chi2(2 nu), nu = K (or the adaptive equivalent degrees of freedom)."""
    w, Y, S, v, lam = eigenspectra(x, NW, K, nfft)
    K = S.shape[0]
    if not adaptive:
        f = S.mean(axis=0)
        dof = np.full_like(f, 2 * K)
    else:
        s2 = np.var(x) / (2 * np.pi)                     # broadband level of white noise with the same variance
        f = S[:2].mean(axis=0)
        for _ in range(100):
            d = np.sqrt(lam)[:, None] * f / (lam[:, None] * f + (1 - lam)[:, None] * s2)
            fn = (d ** 2 * S).sum(axis=0) / (d ** 2).sum(axis=0)
            if np.max(np.abs(fn - f) / f) < 1e-6:
                f = fn
                break
            f = fn
        dof = 2 * (d ** 2).sum(axis=0) ** 2 / (d ** 4).sum(axis=0)
    a = (1 - level) / 2
    lo, hi = dof * f / stats.chi2.ppf(1 - a, dof), dof * f / stats.chi2.ppf(a, dof)
    return dict(w=w, f=f, lo=lo, hi=hi, dof=dof, K=K, NW=NW)


def harmonic_ftest(x, NW=4, K=None, nfft=None):
    """Thomson's harmonic F test of a line component (a deterministic sinusoid) at each frequency: F(2, 2K-2)."""
    w, Y, S, v, lam = eigenspectra(x, NW, K, nfft)
    K = Y.shape[0]
    U0 = v.sum(axis=1)                                   # zero-frequency transform of each taper (0 for odd k)
    mu = (U0[:, None] * Y).sum(axis=0) / (U0 ** 2).sum()
    num = (K - 1) * np.abs(mu) ** 2 * (U0 ** 2).sum()
    den = (np.abs(Y - mu[None, :] * U0[:, None]) ** 2).sum(axis=0)
    F = num / den
    return dict(w=w, F=F, p=stats.f.sf(F, 2, 2 * K - 2), K=K)


def arma_spectrum(omega, ar=(), ma=(), sigma2=1.0):
    """f(w) = sigma^2 |theta(e^{-iw})|^2 / (2 pi |phi(e^{-iw})|^2) for x_t = sum ar_j x_{t-j} + e_t + sum ma_j e_{t-j}."""
    z = np.exp(-1j * np.asarray(omega, float))
    phi = 1 - sum(a * z ** (j + 1) for j, a in enumerate(ar))
    th = 1 + sum(b * z ** (j + 1) for j, b in enumerate(ma))
    return sigma2 * np.abs(th) ** 2 / (2 * np.pi * np.abs(phi) ** 2)


def simulate_arma(n, ar=(), ma=(), burn=1000, rng=None, sigma=1.0):
    rng = np.random.default_rng(rng)
    e = sigma * rng.standard_normal(n + burn)
    return signal.lfilter(np.r_[1, ma], np.r_[1, -np.asarray(ar, float)], e)[burn:]


# =============================================================================
# TWO SERIES: CROSS-SPECTRUM, COHERENCE, PHASE, GAIN, DYNAMIC CORRELATION
# =============================================================================
def cross_spectrum(x, y, NW=4, K=None, nfft=None, level=0.95):
    """Multitaper cross-spectrum f_xy(w) = mean_k Y_k^x conj(Y_k^y) / (2 pi), with gamma_xy(h) = Cov(x_{t+h}, y_t).
    If y_t = x_{t-d} (x leads y by d periods), f_xy = exp(i w d) f_x: a positive phase means x leads.
    Squared coherence, its null threshold 1 - (1 - level)^{1/(K-1)}, phase with its approximate standard error,
    gain of y on x, co-spectrum and the dynamic correlation of Croux, Forni and Reichlin (2001)."""
    w, Yx, Sx, v, lam = eigenspectra(x, NW, K, nfft)
    _, Yy, Sy, _, _ = eigenspectra(y, NW, K, nfft)
    K = Yx.shape[0]
    fxy = (Yx * np.conj(Yy)).mean(axis=0) / (2 * np.pi)
    fx, fy = Sx.mean(axis=0), Sy.mean(axis=0)
    coh = np.abs(fxy) ** 2 / (fx * fy)
    phase = np.angle(fxy)
    se_phase = np.sqrt((1 / np.maximum(coh, 1e-12) - 1) / (2 * K))
    return dict(w=w, fxy=fxy, fx=fx, fy=fy, coh=coh, phase=phase, se_phase=se_phase,
                gain=np.abs(fxy) / fx, co=fxy.real, quad=-fxy.imag, dyncorr=fxy.real / np.sqrt(fx * fy),
                thr=1 - (1 - level) ** (1 / (K - 1)), K=K)


def band_dyncorr(cs, lo, hi):
    """Dynamic correlation over a band of frequencies [lo, hi] (Croux, Forni and Reichlin 2001, eq. 3)."""
    m = (cs['w'] >= lo) & (cs['w'] <= hi)
    return float(cs['co'][m].sum() / np.sqrt(cs['fx'][m].sum() * cs['fy'][m].sum()))


# =============================================================================
# FREQUENCY-DOMAIN CAUSALITY
# =============================================================================
def var_ols(Y, p):
    """VAR(p) with constant by OLS: Y (T x k). Returns A (p x k x k), c, Sigma (ML divisor), residuals."""
    Y = np.asarray(Y, float)
    T, k = Y.shape
    X = np.hstack([np.ones((T - p, 1))] + [Y[p - j:T - j] for j in range(1, p + 1)])
    B = np.linalg.lstsq(X, Y[p:], rcond=None)[0]
    U = Y[p:] - X @ B
    A = np.stack([B[1 + (j - 1) * k:1 + j * k].T for j in range(1, p + 1)])
    return dict(A=A, c=B[0], Sigma=U.T @ U / (T - p), U=U, X=X, B=B, p=p, T=T - p)


def var_order(Y, pmax=8, crit='bic'):
    """Lag order by BIC (or AIC) on a common sample."""
    Y = np.asarray(Y, float)
    best, out = None, {}
    for p in range(1, pmax + 1):
        r = var_ols(Y[pmax - p:], p)
        T, k = r['T'], Y.shape[1]
        ld = np.log(np.linalg.det(r['Sigma']))
        ic = ld + (np.log(T) if crit == 'bic' else 2) * p * k * k / T
        out[p] = ic
        if best is None or ic < out[best]:
            best = p
    return best, out


def geweke(Y, p, omega):
    """Geweke (1982) measures of causality from series 2 to series 1 and from 1 to 2 at each frequency, for a
    bivariate VAR(p): M_{2->1}(w) = ln( f_11(w) / (|H~_11(w)|^2 Sigma~_11 / 2 pi) ) after the normalisation that
    makes the innovation of series 1 uncorrelated with the transformed innovation of series 2."""
    r = var_ols(Y, p)
    A, S = r['A'], r['Sigma']
    out = {}
    for (i, j) in ((0, 1), (1, 0)):
        P = np.eye(2)
        P[j, i] = -S[i, j] / S[i, i]                    # orthogonalise the innovation of the target series i
        St = P @ S @ P.T
        M = []
        for om in omega:
            Az = np.eye(2) - sum(A[l] * np.exp(-1j * om * (l + 1)) for l in range(p))
            H = np.linalg.inv(Az) @ np.linalg.inv(P)
            f = (H @ St @ H.conj().T).real / (2 * np.pi)
            M.append(np.log(f[i, i] / (np.abs(H[i, i]) ** 2 * St[i, i] / (2 * np.pi))))
        out[f'{j}->{i}'] = np.array(M)
    # total (time-domain) Geweke measure from 2 to 1 and from 1 to 2: log ratio of restricted and full variances
    for (i, j) in ((0, 1), (1, 0)):
        Xr = np.hstack([np.ones((r['T'], 1))] + [Y[p - l:len(Y) - l, [i]] for l in range(1, p + 1)])
        ur = Y[p:, i] - Xr @ np.linalg.lstsq(Xr, Y[p:, i], rcond=None)[0]
        out[f'F{j}->{i}'] = float(np.log((ur @ ur / r['T']) / S[i, i]))
    out['Sigma'] = S
    return out


def breitung_candelon(Y, p, omega, cause=1, target=0):
    """Breitung and Candelon (2006): H0 'no causality from `cause` to `target` at frequency w' is the pair of linear
    restrictions sum_j psi_j cos(j w) = 0 and sum_j psi_j sin(j w) = 0 on the lag coefficients psi_j of the cause in
    the equation of the target; F statistic with (2, T - 2p - 1) degrees of freedom (one restriction at w = 0, pi)."""
    Y = np.asarray(Y, float)
    T = len(Y) - p
    X = np.hstack([np.ones((T, 1))] + [Y[p - j:len(Y) - j, [target]] for j in range(1, p + 1)]
                  + [Y[p - j:len(Y) - j, [cause]] for j in range(1, p + 1)])
    yv = Y[p:, target]
    b = np.linalg.lstsq(X, yv, rcond=None)[0]
    e = yv - X @ b
    k = X.shape[1]
    s2 = e @ e / (T - k)
    XtXi = np.linalg.inv(X.T @ X)
    j = np.arange(1, p + 1)
    Fs, ps = [], []
    for om in omega:
        R = np.zeros((2, k))
        R[0, 1 + p:] = np.cos(j * om)
        R[1, 1 + p:] = np.sin(j * om)
        if abs(np.sin(om)) < 1e-10:
            R = R[:1]
        Rb = R @ b
        F = float(Rb @ np.linalg.solve(R @ XtXi @ R.T * s2, Rb) / R.shape[0])
        Fs.append(F)
        ps.append(float(stats.f.sf(F, R.shape[0], T - k)))
    return dict(F=np.array(Fs), p=np.array(ps), crit=float(stats.f.ppf(0.95, 2, T - k)), T=T, df=T - k)


# =============================================================================
# FILTERS
# =============================================================================
def hp_filter(y, lam=1600):
    """Hodrick-Prescott: tau = argmin sum (y - tau)^2 + lam sum (Delta^2 tau)^2 = (I + lam D'D)^{-1} y."""
    y = np.asarray(y, float)
    n = len(y)
    D = sparse.diags([np.ones(n - 2), -2 * np.ones(n - 2), np.ones(n - 2)], [0, 1, 2], shape=(n - 2, n))
    tau = spsolve(sparse.eye(n, format='csc') + lam * (D.T @ D).tocsc(), y)
    return y - tau, tau


def hp_one_sided(y, lam=1600, start=20):
    """Real-time HP cycle: at each t the last value of the HP cycle computed on y_1..y_t (NaN before `start`)."""
    y = np.asarray(y, float)
    out = np.full(len(y), np.nan)
    for t in range(start, len(y) + 1):
        out[t - 1] = hp_filter(y[:t], lam)[0][-1]
    return out


def hp_gain(omega, lam=1600):
    """Gain of the HP cycle filter (from the level to the cycle): 4 lam (1 - cos w)^2 / (1 + 4 lam (1 - cos w)^2)."""
    u = 4 * lam * (1 - np.cos(omega)) ** 2
    return u / (1 + u)


def bk_weights(low=6, high=32, K=12):
    """Baxter-King (1999) symmetric band-pass weights a_{-K..K} for periods between `low` and `high`, constrained to
    sum to zero (so that the filter removes a unit root and a linear trend)."""
    w1, w2 = 2 * np.pi / high, 2 * np.pi / low
    j = np.arange(1, K + 1)
    b = np.r_[(w2 - w1) / np.pi, (np.sin(j * w2) - np.sin(j * w1)) / (np.pi * j)]
    theta = -(b[0] + 2 * b[1:].sum()) / (2 * K + 1)
    a = b + theta
    return np.r_[a[:0:-1], a]


def bk_filter(y, low=6, high=32, K=12):
    """Baxter-King cycle (K observations lost at each end, NaN there)."""
    y = np.asarray(y, float)
    a = bk_weights(low, high, K)
    c = np.full(len(y), np.nan)
    c[K:len(y) - K] = np.convolve(y, a, mode='valid')
    return c


def filter_gain(weights, omega, lags=None):
    """|sum_j a_j exp(-i w j)| for weights a_j at lags j (default: symmetric, centred)."""
    a = np.asarray(weights, float)
    lags = np.arange(len(a)) - (len(a) - 1) // 2 if lags is None else np.asarray(lags)
    return np.abs(np.exp(-1j * np.outer(omega, lags)) @ a)


def ideal_gain(omega, low=6, high=32):
    return ((omega >= 2 * np.pi / high) & (omega <= 2 * np.pi / low)).astype(float)


def hamilton_filter(y, h=8, p=4):
    """Hamilton (2018) regression filter: v_{t+h} = y_{t+h} - b0 - b1 y_t - ... - bp y_{t-p+1} (OLS residual).
    Returns the cycle aligned at t+h (NaN for the first h+p-1 observations) and the coefficients."""
    y = np.asarray(y, float)
    n = len(y)
    X = np.column_stack([np.ones(n - h - p + 1)] + [y[p - 1 - j:n - h - j] for j in range(p)])
    yy = y[h + p - 1:]
    b = np.linalg.lstsq(X, yy, rcond=None)[0]
    c = np.full(n, np.nan)
    c[h + p - 1:] = yy - X @ b
    return c, b


def hamilton_gain(omega, b, h=8):
    """Gain from the level to the Hamilton cycle: |1 - sum_j b_j exp(-i w (h + j - 1))|; b without the constant."""
    j = np.arange(1, len(b) + 1)
    return np.abs(1 - np.exp(-1j * np.outer(omega, h + j - 1)) @ np.asarray(b, float))


def concordance(cx, cy):
    """Harding and Pagan (2002) concordance of the phases S_t = 1{cycle > 0} and its value under independence."""
    sx, sy = (np.asarray(cx) > 0).astype(float), (np.asarray(cy) > 0).astype(float)
    C = float(np.mean(sx * sy + (1 - sx) * (1 - sy)))
    px, py = sx.mean(), sy.mean()
    return C, float(px * py + (1 - px) * (1 - py))


# =============================================================================
# MODWT AND MULTIRESOLUTION ANALYSIS
# =============================================================================
def wavelet_filters(name='sym4'):
    """Orthonormal scaling filter g (sum g = sqrt 2) of PyWavelets and the wavelet filter h_l = (-1)^l g_{L-1-l}.
    'sym4' is the least-asymmetric filter of length 8, LA(8) in Percival and Walden (2000); 'haar' and 'db4' as well."""
    import pywt
    g = np.asarray(pywt.Wavelet(name).rec_lo, float)
    L = len(g)
    h = np.array([(-1) ** l * g[L - 1 - l] for l in range(L)])
    return g, h


def _transfer(f, n):
    """DFT of a filter placed at lags 0..L-1 of a length-n circular array."""
    z = np.zeros(n)
    z[:len(f)] = f
    return np.fft.fft(z)


def modwt(x, J, name='sym4'):
    """MODWT (Percival and Walden 2000, ch. 5) by FFT: W_j = IFFT(H_j X), V_J = IFFT(G_J X), with
    H_j(f) = H~(2^{j-1} f) prod_{l<j-1} G~(2^l f), H~ = H / sqrt 2, G~ = G / sqrt 2 (circular filtering).
    Returns W (J x n), V_J (n) and the number of boundary coefficients L_j - 1 at the start of each level."""
    x = np.asarray(x, float)
    n = len(x)
    g, h = wavelet_filters(name)
    L = len(g)
    X = np.fft.fft(x)
    k = np.arange(n)
    W, Gprod = [], np.ones(n, complex)
    G = _transfer(g / np.sqrt(2), n)
    H = _transfer(h / np.sqrt(2), n)
    for j in range(1, J + 1):
        idx = (k * 2 ** (j - 1)) % n
        Hj = H[idx] * Gprod
        W.append(np.fft.ifft(Hj * X).real)
        Gprod = Gprod * G[idx]
    VJ = np.fft.ifft(Gprod * X).real
    nb = [min((2 ** j - 1) * (L - 1), n) for j in range(1, J + 1)]
    return dict(W=np.array(W), V=VJ, nb=nb, J=J, name=name, n=n, L=L)


def mra(x, J, name='sym4'):
    """Multiresolution analysis: details D_1..D_J and smooth S_J with x = sum_j D_j + S_J (exactly), each D_j the
    inverse MODWT of level j alone: D_j = IFFT(conj(H_j) DFT(W_j))."""
    x = np.asarray(x, float)
    n = len(x)
    g, h = wavelet_filters(name)
    X = np.fft.fft(x)
    k = np.arange(n)
    G = _transfer(g / np.sqrt(2), n)
    H = _transfer(h / np.sqrt(2), n)
    D, Gprod = [], np.ones(n, complex)
    for j in range(1, J + 1):
        idx = (k * 2 ** (j - 1)) % n
        Hj = H[idx] * Gprod
        D.append(np.fft.ifft(np.abs(Hj) ** 2 * X).real)
        Gprod = Gprod * G[idx]
    S = np.fft.ifft(np.abs(Gprod) ** 2 * X).real
    return np.array(D), S


def wavelet_variance(x, J, name='sym4', level=0.95):
    """Unbiased MODWT wavelet variance by level (boundary coefficients dropped) with the chi-square interval of
    Percival and Walden (2000, eq. 314c): eta = max(M_j / 2^j, 1) equivalent degrees of freedom."""
    m = modwt(x, J, name)
    out = []
    for j in range(J):
        w = m['W'][j][m['nb'][j]:]
        Mj = len(w)
        v = float(np.mean(w ** 2))
        eta = max(Mj / 2 ** (j + 1), 1)
        a = (1 - level) / 2
        out.append(dict(level=j + 1, var=v, lo=eta * v / stats.chi2.ppf(1 - a, eta), hi=eta * v / stats.chi2.ppf(a, eta),
                        M=Mj, eta=eta))
    return out


def wavelet_corr(x, y, J, name='sym4', level=0.95):
    """Wavelet correlation and wavelet beta (of y on x) by level (Whitcher, Guttorp and Percival 2000; Gencay,
    Selcuk and Whitcher 2005), with the Fisher-z interval tanh(atanh(r) +- z / sqrt(M_j / 2^j - 3))."""
    mx, my = modwt(x, J, name), modwt(y, J, name)
    z = stats.norm.ppf(0.5 + level / 2)
    out = []
    for j in range(J):
        a, b = mx['W'][j][mx['nb'][j]:], my['W'][j][my['nb'][j]:]
        r = float(np.sum(a * b) / np.sqrt(np.sum(a ** 2) * np.sum(b ** 2)))
        ne = max(len(a) / 2 ** (j + 1) - 3, 1)
        out.append(dict(level=j + 1, r=r, lo=float(np.tanh(np.arctanh(r) - z / np.sqrt(ne))),
                        hi=float(np.tanh(np.arctanh(r) + z / np.sqrt(ne))), beta=float(np.sum(a * b) / np.sum(a ** 2)),
                        M=len(a)))
    return out


# =============================================================================
# CONTINUOUS WAVELET TRANSFORM, CROSS-WAVELET AND WAVELET COHERENCE (numpy, after Torrence-Compo and Grinsted)
# =============================================================================
W0 = 6.0                                                    # Morlet central frequency
FOURIER_FACTOR = 4 * np.pi / (W0 + np.sqrt(2 + W0 ** 2))  # Fourier period = FOURIER_FACTOR * scale (about 1.033)


def morlet_scales(n, dt=1.0, dj=1 / 12, s0=None, pmax=None):
    """Scales s_j = s0 2^{j dj}, j = 0..J, s0 = 2 dt; up to the period pmax (default: n dt / 3)."""
    s0 = s0 or 2 * dt
    pmax = pmax or n * dt / 3
    J = int(np.floor(np.log2(pmax / FOURIER_FACTOR / s0) / dj))
    return s0 * 2 ** (dj * np.arange(J + 1))


def cwt(x, dt=1.0, dj=1 / 12, s0=None, pmax=None, scales=None):
    """Morlet CWT by FFT (Torrence and Compo 1998, eq. 4): W_n(s) = sum_k x^_k psi^*(s w_k) exp(i w_k n dt),
    psi^(s w) = sqrt(2 pi s / dt) pi^{-1/4} H(w) exp(-(s w - w0)^2 / 2). The series is standardised and
    zero-padded to the next power of two. Returns W (scales x n), scales, periods and the cone of influence."""
    x = np.asarray(x, float)
    n = len(x)
    x = (x - x.mean()) / x.std()
    npad = int(2 ** np.ceil(np.log2(n)) * 2)
    xp = np.r_[x, np.zeros(npad - n)]
    k = 2 * np.pi * np.fft.fftfreq(npad, dt)
    scales = morlet_scales(n, dt, dj, s0, pmax) if scales is None else np.asarray(scales)
    X = np.fft.fft(xp)
    ps = np.sqrt(2 * np.pi * scales[:, None] / dt) * np.pi ** -0.25 * np.exp(-(scales[:, None] * k - W0) ** 2 / 2) * (k > 0)
    W = np.fft.ifft(X[None, :] * ps, axis=1)[:, :n]
    t = np.arange(n)
    coi = FOURIER_FACTOR / np.sqrt(2) * dt * np.minimum(t + 0.5, n - t - 0.5)   # e-folding time sqrt(2) s
    return dict(W=W, scales=scales, period=FOURIER_FACTOR * scales, coi=coi, dt=dt, dj=dj, n=n)


def ar1_coef(x):
    x = np.asarray(x, float) - np.mean(x)
    return float(np.dot(x[1:], x[:-1]) / np.dot(x, x))


def red_noise_signif(x, c, level=0.95):
    """Torrence-Compo (eq. 16-18) significance of the normalised power |W|^2 / sigma^2 against an AR(1) red noise
    with the lag-1 autocorrelation of x: P_k chi2(2) / 2 at the Fourier frequency of each scale."""
    a = ar1_coef(x)
    freq = c['dt'] / c['period']
    Pk = (1 - a ** 2) / (1 + a ** 2 - 2 * a * np.cos(2 * np.pi * freq))
    return Pk * stats.chi2.ppf(level, 2) / 2


def _smooth(Wd, c):
    """Smoothing operator of Torrence and Webster (1999) / Grinsted et al. (2004) for the Morlet wavelet:
    a Gaussian in time with standard deviation equal to the scale, then a boxcar of width 0.6 in log2-scale."""
    n = Wd.shape[1]
    npad = int(2 ** np.ceil(np.log2(n)) * 2)
    k = 2 * np.pi * np.fft.fftfreq(npad)
    F = np.exp(-0.5 * (c['scales'][:, None] / c['dt']) ** 2 * k[None, :] ** 2)
    S = np.fft.ifft(F * np.fft.fft(Wd, npad, axis=1), axis=1)[:, :n]
    width = 0.6 / c['dj']                                # number of scale steps covered by the boxcar
    m = int(np.floor(width))
    wts = np.ones(2 * (m // 2) + 1)
    if width - m > 0 and m % 2 == 1:
        wts = np.r_[0.5 * (width - m), np.ones(m), 0.5 * (width - m)]
    wts = wts / wts.sum()
    from scipy.ndimage import convolve1d
    return convolve1d(S.real, wts, axis=0, mode='nearest') + 1j * convolve1d(S.imag, wts, axis=0, mode='nearest')


def wavelet_coherence(x, y, dt=1.0, dj=1 / 12, pmax=None):
    """Cross-wavelet W_xy = W_x conj(W_y), smoothed squared coherence R^2 = |S(W_xy/s)|^2 / (S(|W_x|^2/s) S(|W_y|^2/s))
    and the phase angle of S(W_xy/s): 0 in phase, pi anti-phase, positive when x leads y."""
    cx = cwt(x, dt, dj, pmax=pmax)
    cy = cwt(y, dt, dj, scales=cx['scales'])
    s = cx['scales'][:, None]
    Wxy = cx['W'] * np.conj(cy['W'])
    Sxy = _smooth(Wxy / s, cx)
    Sx = _smooth(np.abs(cx['W']) ** 2 / s, cx).real
    Sy = _smooth(np.abs(cy['W']) ** 2 / s, cx).real
    R2 = np.abs(Sxy) ** 2 / (Sx * Sy)
    return dict(R2=np.clip(R2, 0, 1), phase=np.angle(Sxy), Wxy=Wxy, cwt=cx, period=cx['period'], coi=cx['coi'],
                scales=cx['scales'])


def coi_mask(c):
    """True where the time-period point lies outside the cone of influence (reliable)."""
    return c['period'][:, None] <= c['coi'][None, :]


def wtc_montecarlo(x, y, dt=1.0, dj=1 / 12, pmax=None, reps=500, level=0.95, seed=2026, reps_check=200):
    """Monte Carlo significance of the wavelet coherence (Grinsted et al. 2004): pairs of independent AR(1)
    series with the lag-1 autocorrelations of x and y; the `level` quantile of R^2 at each scale (pooled over time
    inside the cone of influence). A second, independent set of `reps_check` pairs gives the null distribution of
    the share of the reliable area that is pointwise significant (the areawise check of the mini-case)."""
    rng = np.random.default_rng(seed)
    n = len(x)
    ax, ay = ar1_coef(x), ar1_coef(y)
    base = wavelet_coherence(x, y, dt, dj, pmax)
    mask = coi_mask(base['cwt'])

    def draw():
        ex, ey = rng.standard_normal(n + 200), rng.standard_normal(n + 200)
        sx = signal.lfilter([1], [1, -ax], ex)[200:]
        sy = signal.lfilter([1], [1, -ay], ey)[200:]
        return wavelet_coherence(sx, sy, dt, dj, pmax)['R2']
    R = np.array([draw() for _ in range(reps)])
    thr = np.array([np.quantile(R[:, i][:, mask[i]] if mask[i].any() else R[:, i], level) for i in range(R.shape[1])])
    share_null = np.array([(draw() > thr[:, None])[mask].mean() for _ in range(reps_check)])
    return dict(thr=thr, share_null=share_null, ax=ax, ay=ay, reps=reps, reps_check=reps_check,
                share_obs=float((base['R2'] > thr[:, None])[mask].mean()), base=base, mask=mask)


def ssa(x, Lw, r):
    """Singular spectrum analysis: embed with window Lw, SVD of the trajectory (Hankel) matrix, reconstruct the
    components of the first r eigentriples by diagonal averaging. Returns components (r x n) and eigenvalue shares."""
    x = np.asarray(x, float)
    n = len(x)
    Kc = n - Lw + 1
    Xm = np.column_stack([x[i:i + Lw] for i in range(Kc)])
    U, s, Vt = np.linalg.svd(Xm, full_matrices=False)
    comps = []
    for i in range(r):
        Xi = s[i] * np.outer(U[:, i], Vt[i])
        comps.append(np.array([np.mean(Xi[::-1].diagonal(d)) for d in range(-(Lw - 1), Kc)]))
    return np.array(comps), s ** 2 / np.sum(s ** 2)
