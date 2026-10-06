"""
fm_core.py -- the engine of Chapter 13 (ATS): foundation models and conformal prediction
=========================================================================================
numpy, scipy, statsmodels and PyTorch on CPU (small open checkpoints, fixed seeds). Every function is self-contained, so
the Quantlet notebooks can copy it with inspect.getsource.
  * scoring             pinball loss, quantile CRPS, weighted quantile loss, interval score, QLIKE, MASE;
  * inference           HAC variance, Diebold-Mariano with the HLN correction, the Model Confidence Set, Holm and
                        Benjamini-Hochberg corrections, Kupiec and Christoffersen backtests (as in Chapters 1 and 9);
  * baselines           seasonal naive, AR(p) by OLS with Gaussian quantiles, damped-trend ETS, HAR, GARCH(1,1);
  * deep baselines      DLinear and a small N-BEATS (the architectures of Chapter 12), trained globally;
  * foundation models   one interface for Chronos-Bolt, Chronos-2, TimesFM 2.5 and TiRex (skipped if not installed);
                        the Chronos tokeniser (mean scaling and uniform bins);
  * conformal           split conformal, CQR, and online thresholds from a stream of scores: static, rolling,
                        weighted (Barber et al. 2023), ACI (Gibbs and Candes 2021), quantile tracking and conformal PID
                        (Angelopoulos, Candes and Tibshirani 2023); EnbPI (Xu and Xie 2021).
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import math

import numpy as np
from scipy import optimize, stats

try:                                            # PyTorch is preinstalled in Colab; without it the deep parts are skipped
    import torch
    from torch import nn
    TORCH = True
except ImportError:                             # pragma: no cover
    import types
    torch = None
    nn = types.SimpleNamespace(Module=object)
    TORCH = False


# =============================================================================
# SCORING RULES
# =============================================================================
def pinball(y, q, tau):
    """Pinball (quantile) loss of the tau-quantile forecast q."""
    u = np.asarray(y, float) - np.asarray(q, float)
    return np.maximum(tau * u, (tau - 1) * u)


def crps_q(y, Q, taus):
    """CRPS approximated by twice the average pinball loss over the quantile levels taus; Q has the levels in its last
    axis, y broadcasts against Q[..., 0]."""
    y = np.asarray(y, float)[..., None]
    taus = np.asarray(taus, float)
    return 2 * pinball(y, Q, taus).mean(axis=-1)


def wql(y, Q, taus):
    """Weighted quantile loss of Chronos (Ansari et al. 2024): summed pinball losses scaled by the summed |y|."""
    return float(crps_q(y, Q, taus).sum() / np.abs(np.asarray(y, float)).sum())


def interval_score(y, lo, hi, alpha):
    """Interval score of a central (1 - alpha) interval (Winkler 1972; Gneiting and Raftery 2007): width plus 2/alpha
    times the distance by which y falls outside."""
    y, lo, hi = (np.asarray(v, float) for v in (y, lo, hi))
    return (hi - lo) + 2 / alpha * (lo - y) * (y < lo) + 2 / alpha * (y - hi) * (y > hi)


def qlike(rv, f):
    """QLIKE loss of a variance forecast f for the realised variance rv (Patton 2011)."""
    x = np.asarray(rv, float) / np.asarray(f, float)
    return x - np.log(x) - 1


def mase_scale(insample, m):
    """Scale of MASE (Hyndman and Koehler 2006): in-sample MAE of the seasonal naive forecast with period m."""
    x = np.asarray(insample, float)
    x = x[~np.isnan(x)]
    return float(np.mean(np.abs(x[m:] - x[:-m])))


def gmean(x):
    """Geometric mean (the aggregate of relative scores across series; Fleming and Wallace 1986)."""
    x = np.asarray(x, float)
    return float(np.exp(np.mean(np.log(x))))


# =============================================================================
# INFERENCE ON FORECASTS (as in Chapters 1 and 9)
# =============================================================================
def hac_var(x, lags, kernel='bartlett'):
    """Long-run variance: Bartlett (Newey-West) or rectangular kernel."""
    x = np.asarray(x, float) - np.mean(x)
    T = len(x)
    v = x @ x / T
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1) if kernel == 'bartlett' else 1.0
        v += 2 * w * (x[k:] @ x[:-k]) / T
    return v


def dm_test(d, h=1):
    """Diebold-Mariano test of E[d] = 0 for the loss differential d, HAC variance with h - 1 lags (rectangular;
    Bartlett if negative) and the Harvey-Leybourne-Newbold correction with t(T - 1). Two-sided p-value."""
    d = np.asarray(d, float)
    d = d[~np.isnan(d)]
    T = len(d)
    v = hac_var(d, h - 1, 'rect')
    if v <= 0:
        v = hac_var(d, max(h - 1, 1), 'bartlett')
    dm = d.mean() / np.sqrt(v / T)
    hln = np.sqrt((T + 1 - 2 * h + h * (h - 1) / T) / T) * dm
    return {'T': T, 'dbar': float(d.mean()), 'hln': float(hln), 'p': float(2 * stats.t.sf(abs(hln), T - 1))}


def mcs(losses, alpha=0.10, B=2000, block=7, seed=2026):
    """Model Confidence Set (Hansen, Lunde and Nason 2011), T_max statistic, moving-block bootstrap.
    losses: T x m DataFrame; returns the MCS p-value of every model and the set at level alpha."""
    L = np.asarray(losses, float)
    L = L[~np.isnan(L).any(axis=1)]
    T, m = L.shape
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / block))
    idx = np.concatenate([np.arange(s, s + block) for s in rng.integers(0, T - block + 1, size=(B, nb)).ravel()])
    idx = idx.reshape(B, nb * block)[:, :T]
    Lb = L[idx].mean(axis=1)
    alive, pvals, p_run = list(range(m)), {}, 0.0
    while len(alive) > 1:
        Lm = L[:, alive].mean(axis=0)
        dbar = Lm - Lm.mean()
        db = Lb[:, alive] - Lb[:, alive].mean(axis=1, keepdims=True)
        se = np.sqrt(((db - dbar) ** 2).mean(axis=0))
        t = dbar / se
        p = float((((db - dbar) / se).max(axis=1) > t.max()).mean())
        p_run = max(p_run, p)
        worst = alive[int(np.argmax(t))]
        pvals[worst] = p_run
        alive.remove(worst)
    pvals[alive[0]] = 1.0
    cols = list(losses.columns) if hasattr(losses, 'columns') else list(range(m))
    out = {cols[i]: pvals[i] for i in range(m)}
    return {'p': out, 'set': [c for c in cols if out[c] >= alpha]}


def holm(p):
    """Holm (1979) step-down adjusted p-values (family-wise error rate)."""
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)
    adj = np.empty(m)
    run = 0.0
    for k, i in enumerate(o):
        run = max(run, (m - k) * p[i])
        adj[i] = min(1.0, run)
    return adj


def bh(p):
    """Benjamini-Hochberg (1995) adjusted p-values (false discovery rate)."""
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)[::-1]
    adj = np.empty(m)
    run = 1.0
    for k, i in enumerate(o):
        run = min(run, p[i] * m / (m - k))
        adj[i] = run
    return adj


def kupiec(hits, a):
    """Unconditional coverage LR test (Kupiec 1995), chi2(1): (LR, p-value)."""
    h = np.asarray(hits, float)
    n, x = len(h), h.sum()
    pi = x / n
    ll0 = x * np.log(a) + (n - x) * np.log(1 - a)
    ll1 = (x * np.log(pi) if x > 0 else 0) + ((n - x) * np.log(1 - pi) if x < n else 0)
    lr = -2 * (ll0 - ll1)
    return float(lr), float(stats.chi2.sf(lr, 1))


def christoffersen(hits, a):
    """Independence and conditional coverage LR tests (Christoffersen 1998): chi2(1) and chi2(2)."""
    h = np.asarray(hits, int)
    h0, h1 = h[:-1], h[1:]
    n00, n01 = np.sum((h0 == 0) & (h1 == 0)), np.sum((h0 == 0) & (h1 == 1))
    n10, n11 = np.sum((h0 == 1) & (h1 == 0)), np.sum((h0 == 1) & (h1 == 1))
    p01 = n01 / max(n00 + n01, 1)
    p11 = n11 / max(n10 + n11, 1)
    p = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    xl = lambda k, q: k * np.log(q) if k > 0 else 0.0   # noqa: E731
    l0 = xl(n00 + n10, 1 - p) + xl(n01 + n11, p)
    l1 = xl(n00, 1 - p01) + xl(n01, p01) + xl(n10, 1 - p11) + xl(n11, p11)
    lr_ind = -2 * (l0 - l1)
    lr_cc = kupiec(h[1:], a)[0] + lr_ind
    return {'p_ind': float(stats.chi2.sf(lr_ind, 1)), 'p_cc': float(stats.chi2.sf(lr_cc, 2))}


# =============================================================================
# STATISTICAL BASELINES
# =============================================================================
def seasonal_naive(ctx, H, m):
    """Seasonal naive point forecast: repeat the last season of length m over H steps."""
    ctx = np.asarray(ctx, float)
    return np.array([ctx[len(ctx) - m + (h % m)] for h in range(H)])


def ar_fit(y, p):
    """OLS fit of an AR(p) with intercept: coefficients (c, phi_1..phi_p), residual variance, AIC."""
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y) - p)] + [y[p - j:len(y) - j] for j in range(1, p + 1)])
    Y = y[p:]
    b = np.linalg.lstsq(X, Y, rcond=None)[0]
    e = Y - X @ b
    s2 = e @ e / len(Y)
    return b, s2, len(Y) * np.log(s2) + 2 * (p + 1)


def ar_forecast(y, H, taus, pmax=12, p=None):
    """Iterated AR(p) forecasts (p by AIC on a common sample if not given) with Gaussian quantiles from the
    psi-weight forecast variance; returns (mean (H,), quantiles (H, k), p)."""
    y = np.asarray(y, float)
    if p is None:
        best = None
        for q in range(1, pmax + 1):
            aic = ar_fit(y[pmax - q:], q)[2]
            if best is None or aic < best[0]:
                best = (aic, q)
        p = best[1]
    b, s2, _ = ar_fit(y, p)
    c, phi = b[0], b[1:]
    hist = list(y[-p:])
    mean = []
    for _ in range(H):
        f = c + sum(phi[j] * hist[-1 - j] for j in range(p))
        mean.append(f)
        hist.append(f)
    psi = [1.0]
    for h in range(1, H):
        psi.append(sum(phi[j] * psi[h - 1 - j] for j in range(min(p, h))))
    sd = np.sqrt(s2 * np.cumsum(np.square(psi)))
    mean = np.array(mean)
    return mean, mean[:, None] + sd[:, None] * stats.norm.ppf(np.asarray(taus))[None, :], p


def ets_forecast(y, H, taus, seasonal_periods=None, reps=400, seed=0):
    """Damped additive-trend ETS (statsmodels ETSModel, maximum likelihood) with simulated predictive quantiles;
    additive seasonality if seasonal_periods is given. Returns (mean (H,), quantiles (H, k))."""
    from statsmodels.tsa.exponential_smoothing.ets import ETSModel
    import warnings
    y = np.asarray(y, float)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        mod = ETSModel(y, error='add', trend='add', damped_trend=True,
                       seasonal='add' if seasonal_periods else None, seasonal_periods=seasonal_periods)
        res = mod.fit(disp=False, maxiter=200)
        sims = res.simulate(H, repetitions=reps, anchor='end', random_state=seed)
    sims = np.asarray(sims).reshape(H, -1)
    return np.asarray(res.forecast(H)), np.quantile(sims, taus, axis=1).T


def har_design(x):
    """HAR regressors (Corsi 2009) of a daily series x (log realised variance): x_t, mean of the last 5 and 22 days."""
    x = np.asarray(x, float)
    d = x[21:]
    w = np.array([x[t - 4:t + 1].mean() for t in range(21, len(x))])
    m = np.array([x[t - 21:t + 1].mean() for t in range(21, len(x))])
    return np.column_stack([np.ones(len(d)), d, w, m])


def har_forecast(x, h=1):
    """HAR forecast of x at t + h (direct regression of x_{t+h} on the HAR regressors), with the residual s.d."""
    x = np.asarray(x, float)
    X = har_design(x)
    Y = x[21 + h:]
    b = np.linalg.lstsq(X[:-h], Y, rcond=None)[0]
    e = Y - X[:-h] @ b
    return float(X[-1] @ b), float(e.std(ddof=4))


def garch11_fit(r, dist='t'):
    """QML fit of a GARCH(1,1) with constant mean zero (returns in %): Student-t (dist='t') or Normal innovations.
    Returns (omega, alpha, beta, nu) with nu = inf for the Normal."""
    r = np.asarray(r, float)
    v0 = r.var()

    def nll(p):
        om, a, b = np.exp(p[0]), 1 / (1 + np.exp(-p[1])), 1 / (1 + np.exp(-p[2]))
        if a + b >= 0.9999:
            return 1e10
        nu = 2.05 + np.exp(p[3]) if dist == 't' else np.inf
        h = np.empty(len(r))
        h[0] = v0
        for t in range(1, len(r)):
            h[t] = om + a * r[t - 1] ** 2 + b * h[t - 1]
        if dist == 't':
            ll = (math.lgamma((nu + 1) / 2) - math.lgamma(nu / 2) - 0.5 * np.log(np.pi * (nu - 2) * h)
                  - (nu + 1) / 2 * np.log1p(r ** 2 / ((nu - 2) * h)))
            return -ll.sum()
        return 0.5 * np.sum(np.log(2 * np.pi * h) + r ** 2 / h)
    x0 = [np.log(0.05 * v0), np.log(0.08 / 0.92), np.log(0.9 / 0.1)] + ([np.log(6.0)] if dist == 't' else [])
    res = optimize.minimize(nll, x0, method='Nelder-Mead',
                            options={'maxiter': 3000, 'xatol': 1e-6, 'fatol': 1e-6})
    p = res.x
    nu = 2.05 + np.exp(p[3]) if dist == 't' else np.inf
    return float(np.exp(p[0])), float(1 / (1 + np.exp(-p[1]))), float(1 / (1 + np.exp(-p[2]))), float(nu)


def garch11_filter(r, par):
    """Conditional variances h_1..h_{T+1} of a GARCH(1,1) for returns r (the last one is the one-step forecast)."""
    om, a, b, _ = par
    r = np.asarray(r, float)
    h = np.empty(len(r) + 1)
    h[0] = r.var()
    for t in range(1, len(r) + 1):
        h[t] = om + a * r[t - 1] ** 2 + b * h[t - 1]
    return h


# =============================================================================
# DEEP BASELINES (architectures of Chapter 12), trained globally on windows
# =============================================================================
def set_seed(seed):
    np.random.seed(seed)
    if TORCH:
        torch.manual_seed(seed)


class DLinear(nn.Module):
    """DLinear (Zeng et al. 2023): moving-average trend plus remainder, one linear map from L inputs to H outputs each."""

    def __init__(self, L, H, k=25):
        super().__init__()
        self.k = k
        self.lin_t = nn.Linear(L, H)
        self.lin_s = nn.Linear(L, H)

    def forward(self, x):
        pad = (self.k - 1) // 2
        xp = torch.cat([x[:, :1].repeat(1, pad), x, x[:, -1:].repeat(1, self.k - 1 - pad)], dim=1)
        trend = xp.unfold(1, self.k, 1).mean(-1)
        return self.lin_t(trend) + self.lin_s(x - trend)


class NBeats(nn.Module):
    """A small generic N-BEATS (Oreshkin et al. 2020): stacked fully connected blocks with backcast and forecast."""

    def __init__(self, L, H, width=128, blocks=3, layers=3):
        super().__init__()
        self.blocks = nn.ModuleList()
        for _ in range(blocks):
            mods, d = [], L
            for _ in range(layers):
                mods += [nn.Linear(d, width), nn.ReLU()]
                d = width
            self.blocks.append(nn.ModuleDict({'fc': nn.Sequential(*mods), 'b': nn.Linear(width, L), 'f': nn.Linear(width, H)}))

    def forward(self, x):
        res, out = x, 0
        for bl in self.blocks:
            h = bl['fc'](res)
            res = res - bl['b'](h)
            out = out + bl['f'](h)
        return out


def fit_global(model, X, Y, epochs=40, lr=1e-3, batch=256, seed=0):
    """Train a global network on windows (X: n x L, Y: n x H, already scaled) with Adam and the MAE loss;
    the last 10% of the windows (in time) is the validation set for early stopping."""
    set_seed(seed)
    X, Y = torch.tensor(X, dtype=torch.float32), torch.tensor(Y, dtype=torch.float32)
    nv = max(1, int(0.1 * len(X)))
    Xt, Yt, Xv, Yv = X[:-nv], Y[:-nv], X[-nv:], Y[-nv:]
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    best, state, wait = np.inf, None, 0
    g = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(len(Xt), generator=g)
        for i in range(0, len(Xt), batch):
            j = perm[i:i + batch]
            opt.zero_grad()
            loss = (model(Xt[j]) - Yt[j]).abs().mean()
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            v = float((model(Xv) - Yv).abs().mean())
        if v < best - 1e-6:
            best, state, wait = v, {k: t.clone() for k, t in model.state_dict().items()}, 0
        else:
            wait += 1
            if wait >= 5:
                break
    model.load_state_dict(state)
    model.eval()
    return model


def predict_global(model, X):
    with torch.no_grad():
        return model(torch.tensor(np.asarray(X), dtype=torch.float32)).numpy()


# =============================================================================
# FOUNDATION MODELS: one interface, CPU, graceful skip
# =============================================================================
FM_SPECS = {   # display name: (library, Hugging Face checkpoint, quantile levels the model was trained on)
    'Chronos-Bolt tiny': ('chronos', 'amazon/chronos-bolt-tiny', 'deciles'),
    'Chronos-Bolt mini': ('chronos', 'amazon/chronos-bolt-mini', 'deciles'),
    'Chronos-Bolt small': ('chronos', 'amazon/chronos-bolt-small', 'deciles'),
    'Chronos-Bolt base': ('chronos', 'amazon/chronos-bolt-base', 'deciles'),
    'Chronos-2': ('chronos', 'amazon/chronos-2', 'wide'),
    'TimesFM 2.5': ('timesfm', 'google/timesfm-2.5-200m-pytorch', 'deciles'),
    'TiRex': ('tirex', 'NX-AI/TiRex', 'deciles'),
}
DECILES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
WIDE = [0.01, 0.05] + DECILES + [0.95, 0.99]
_FM = {}


def fm_load(name):
    """Load a foundation model once (CPU); None if its library or checkpoint is not available."""
    if name in _FM:
        return _FM[name]
    lib, ckpt, _ = FM_SPECS[name]
    model = None
    try:
        if TORCH:
            torch.set_num_threads(1)
        if lib == 'chronos':
            from chronos import BaseChronosPipeline
            model = BaseChronosPipeline.from_pretrained(ckpt, device_map='cpu', torch_dtype=torch.float32)
        elif lib == 'timesfm':
            import timesfm
            model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(ckpt)
            model.compile(timesfm.ForecastConfig(max_context=2048, max_horizon=128, normalize_inputs=True,
                                                 use_continuous_quantile_head=True, fix_quantile_crossing=True))
        elif lib == 'tirex':
            from tirex import load_model
            model = load_model(ckpt, device='cpu')
    except Exception as e:                       # library missing, no network, incompatible version: skip
        print(f'{name}: not available ({type(e).__name__}); skipped')
        model = None
    _FM[name] = model
    return model


def fm_levels(name):
    """Quantile levels a model can return: 0.1-0.9 (deciles) or 0.01-0.99 (Chronos-2)."""
    return WIDE if FM_SPECS[name][2] == 'wide' else DECILES


def fm_params(name):
    """Number of parameters of a loaded model (millions)."""
    m = fm_load(name)
    if m is None:
        return np.nan
    net = getattr(m, 'model', m)
    if hasattr(net, 'parameters'):
        return sum(p.numel() for p in net.parameters()) / 1e6
    return np.nan


def _interp_levels(Q, have, want):
    """Quantiles at the levels `want` by linear interpolation of the quantile function between the levels `have`
    (NaN outside the range the model was trained on)."""
    have = np.asarray(have, float)
    out = np.full(Q.shape[:-1] + (len(want),), np.nan)
    for k, t in enumerate(want):
        if t < have[0] - 1e-9 or t > have[-1] + 1e-9:
            continue
        j = int(np.clip(np.searchsorted(have, t) - 1, 0, len(have) - 2))
        w = (t - have[j]) / (have[j + 1] - have[j])
        out[..., k] = (1 - w) * Q[..., j] + w * Q[..., j + 1]
    return out


def fm_forecast(name, contexts, H, taus, batch=64, covariates=None, cross_learning=False):
    """Zero-shot quantile forecasts of a foundation model.
    contexts: list of 1-d arrays (histories, possibly of different lengths); H: horizon; taus: quantile levels.
    covariates (Chronos-2 only): list of dicts {'past': {name: array}, 'future': {name: array}} aligned with contexts.
    Returns an array (n, H, len(taus)), or None if the model is not available."""
    m = fm_load(name)
    if m is None:
        return None
    lib = FM_SPECS[name][0]
    have = fm_levels(name)
    out = []
    for i in range(0, len(contexts), batch):
        ctx = [np.asarray(c, np.float32) for c in contexts[i:i + batch]]
        with torch.no_grad():
            if lib == 'chronos' and name == 'Chronos-2':
                if covariates is not None:
                    inp = [{'target': c, 'past_covariates': {k: np.asarray(v, np.float32) for k, v in cv['past'].items()},
                            'future_covariates': {k: np.asarray(v, np.float32) for k, v in cv['future'].items()}}
                           for c, cv in zip(ctx, covariates[i:i + batch])]
                else:
                    inp = [torch.tensor(c) for c in ctx]
                q, _ = m.predict_quantiles(inp, prediction_length=H, quantile_levels=have, cross_learning=cross_learning)
                q = np.stack([np.asarray(x)[0] for x in q])                 # (n, H, k): first (only) target variate
            elif lib == 'chronos':
                q, _ = m.predict_quantiles([torch.tensor(c) for c in ctx], prediction_length=H, quantile_levels=have)
                q = np.asarray(q)
            elif lib == 'timesfm':
                _, qf = m.forecast(horizon=H, inputs=ctx)
                q = np.asarray(qf)[:, :, 1:]                                 # column 0 is the mean
            else:
                q = m.forecast(context=[torch.tensor(c) for c in ctx], prediction_length=H, output_type='numpy')[0]
                q = np.asarray(q)
        out.append(np.sort(q, axis=-1))
    return _interp_levels(np.concatenate(out), have, list(taus))


def chronos_tokenise(x, n_bins=4093, low=-15.0, high=15.0):
    """The Chronos tokeniser (Ansari et al. 2024): mean scaling s = mean|x| over the context, then uniform bins on
    [low, high]; returns (token ids 0..n_bins-1, the dequantised values s * centre, the scale s)."""
    x = np.asarray(x, float)
    s = np.mean(np.abs(x))
    s = s if s > 0 else 1.0
    centres = np.linspace(low, high, n_bins)
    edges = (centres[1:] + centres[:-1]) / 2
    ids = np.searchsorted(edges, x / s, side='right')
    return ids, s * centres[ids], s


# =============================================================================
# CONFORMAL PREDICTION
# =============================================================================
def conformal_quantile(scores, alpha, weights=None):
    """The conformal threshold: the (1 - alpha) quantile of the scores with an extra point mass at +infinity
    (weight 1 for split conformal; weights w_i and w_{n+1} = 1 for the weighted version of Barber et al. 2023).
    Unweighted: the ceil((n + 1)(1 - alpha))-th smallest score, +inf if that rank exceeds n."""
    s = np.asarray(scores, float)
    n = len(s)
    if weights is None:
        k = int(np.ceil((n + 1) * (1 - alpha)))
        return np.inf if k > n else float(np.sort(s)[k - 1])
    w = np.asarray(weights, float)
    p = np.append(w, 1.0) / (w.sum() + 1.0)
    o = np.argsort(s)
    c = np.cumsum(p[:-1][o])
    k = np.searchsorted(c, 1 - alpha - 1e-12)
    return np.inf if k >= n else float(s[o][k])


def split_conformal(y_cal, f_cal, f_test, alpha):
    """Split conformal interval with absolute residual scores: f_test +/- the conformal quantile of |y - f| on the
    calibration set (Papadopoulos et al. 2002; Lei et al. 2018)."""
    q = conformal_quantile(np.abs(np.asarray(y_cal) - np.asarray(f_cal)), alpha)
    return np.asarray(f_test) - q, np.asarray(f_test) + q


def cqr(y_cal, lo_cal, hi_cal, lo_test, hi_test, alpha):
    """Conformalized quantile regression (Romano, Patterson and Candes 2019): score max(lo - y, y - hi) on the
    calibration set; the interval [lo - q, hi + q]."""
    s = np.maximum(np.asarray(lo_cal) - y_cal, y_cal - np.asarray(hi_cal))
    q = conformal_quantile(s, alpha)
    return np.asarray(lo_test) - q, np.asarray(hi_test) + q


def online_threshold(scores, alpha, method='static', n_cal=250, window=None, rho=0.99, gamma=0.005, eta=None,
                     KI=None, Csat=None, scorecaster=None, start=None):
    """Online conformal thresholds q_t, each computed from the scores s_1..s_{t-1} only; the set at time t is
    {y : s_t(y) <= q_t}, so the miss indicator is err_t = 1{s_t > q_t}.
    method: 'static'   split conformal on the first n_cal scores, never updated;
            'rolling'  conformal quantile of the last `window` scores (all past scores if window is None);
            'weighted' weights rho^(t - i) on past scores (non-exchangeable conformal, Barber et al. 2023);
            'aci'      adaptive conformal inference (Gibbs and Candes 2021): level alpha_t,
                       alpha_{t+1} = alpha_t + gamma (alpha - err_t), threshold = quantile of the last `window` scores;
            'qt'       quantile tracking (Angelopoulos, Candes and Tibshirani 2023): q_{t+1} = q_t + eta (err_t - alpha);
            'pid'      quantile tracking + integrator r_t(sum(err - alpha)) = KI tan(x log t / (t Csat)) + a scorecaster
                       (a function past_scores -> forecast of the next score), the conformal PID controller.
    Returns (q, alpha_t) arrays of the same length as scores (NaN before `start`)."""
    s = np.asarray(scores, float)
    T = len(s)
    start = n_cal if start is None else start
    q = np.full(T, np.nan)
    at = np.full(T, np.nan)
    a_t = alpha
    if method in ('qt', 'pid'):
        B = np.nanmax(np.abs(s[:start]))
        eta = 0.01 * B if eta is None else eta
        q_t = conformal_quantile(s[:start], alpha)
        KI = B if KI is None else KI
        Csat = 1.0 if Csat is None else Csat
        integ = 0.0
    for t in range(start, T):
        past = s[:t]
        if method == 'static':
            q[t] = conformal_quantile(s[:n_cal], alpha)
        elif method == 'rolling':
            q[t] = conformal_quantile(past if window is None else past[-window:], alpha)
        elif method == 'weighted':
            w = rho ** np.arange(t, 0, -1)
            q[t] = conformal_quantile(past, alpha, weights=w)
        elif method == 'aci':
            at[t] = a_t
            if a_t <= 0:
                q[t] = np.inf
            elif a_t >= 1:
                q[t] = -np.inf
            else:
                q[t] = conformal_quantile(past if window is None else past[-window:], a_t)
            err = float(s[t] > q[t])
            a_t = a_t + gamma * (alpha - err)
        else:
            base = q_t
            if method == 'pid':
                x = integ * np.log(max(t - start + 1, 2)) / ((t - start + 1) * Csat)
                r = KI * np.tan(x) if abs(x) < np.pi / 2 else np.sign(x) * np.inf
                sc = scorecaster(past) if scorecaster is not None else 0.0
                base = q_t + r + sc
            q[t] = base
            err = float(s[t] > q[t])
            q_t = q_t + eta * (err - alpha)
            integ += err - alpha
    return q, at


def ar_scorecaster(p=1, window=500):
    """A scorecaster for conformal PID: the AR(p) forecast of the next score minus the mean score (so that it adds
    the predictable part only), fitted on the last `window` scores."""
    def f(past):
        x = np.asarray(past[-window:], float)
        if len(x) < 5 * (p + 1):
            return 0.0
        b = ar_fit(x, p)[0]
        return float(b[0] + sum(b[1 + j] * x[-1 - j] for j in range(p)) - x.mean())
    return f


def enbpi(X, y, n_train, alpha, B=25, block=24, s=1, seed=0, lam=1.0):
    """EnbPI (Xu and Xie 2021) with ridge regressions on block-bootstrap samples of the first n_train points:
    leave-one-out residuals of the training points form the initial window; at each later t the interval is the
    ensemble mean +/- the (1 - alpha) quantile of the last n_train absolute residuals; the window is updated with
    the new residual every s steps. Returns (centre, half-width) for t >= n_train."""
    rng = np.random.default_rng(seed)
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, d = X.shape
    mu, sd = X[:n_train].mean(0), X[:n_train].std(0) + 1e-12
    Z = np.column_stack([np.ones(n), (X - mu) / sd])
    nb = int(np.ceil(n_train / block))
    preds = np.empty((B, n))
    inbag = np.zeros((B, n_train), bool)
    for b in range(B):
        starts = rng.integers(0, n_train - block + 1, nb)
        idx = np.concatenate([np.arange(a, a + block) for a in starts])[:n_train]
        inbag[b, np.unique(idx)] = True
        Zb, yb = Z[idx], y[idx]
        beta = np.linalg.solve(Zb.T @ Zb + lam * np.eye(d + 1), Zb.T @ yb)
        preds[b] = Z @ beta
    loo = np.array([preds[~inbag[:, i], i].mean() if (~inbag[:, i]).any() else preds[:, i].mean() for i in range(n_train)])
    resid = list(np.abs(y[:n_train] - loo))
    centre = preds[:, n_train:].mean(axis=0)
    half = np.empty(n - n_train)
    new = []
    for k, t in enumerate(range(n_train, n)):
        half[k] = np.quantile(resid[-n_train:], 1 - alpha)
        new.append(abs(y[t] - centre[k]))
        if len(new) == s:
            resid += new
            new = []
    return centre, half
