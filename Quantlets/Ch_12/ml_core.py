"""
ml_core.py -- the engine of Chapter 12 (ATS): machine learning and deep learning for time series
================================================================================================
numpy, scikit-learn and PyTorch (CPU, small models, fixed seeds). Every function is self-contained so that the
Quantlet notebooks can copy it with inspect.getsource.
  * evaluation           HAC variance, Diebold-Mariano with the HLN correction and the Model Confidence Set (the
                         same code as Chapter 1), QLIKE, pinball loss, sMAPE, MASE;
  * dependent data       lag embedding, OLS with closed-form leave-one-out, the cross-validation schemes of
                         Bergmeir, Hyndman and Koo (2018): 5-fold, LOOCV, non-dependent CV, out-of-sample;
  * high dimension       lasso, adaptive lasso and elastic net with a blocked-CV choice of the penalty;
  * trees                quantile regression forests (Meinshausen 2006) on top of a scikit-learn random forest;
  * deep learning        MLP, RNN/LSTM/GRU, TCN, Linear/NLinear/DLinear, a patch Transformer, N-BEATS, N-HiTS and a
                         DeepAR-type Gaussian LSTM, with one training loop (Adam, early stopping on the last block);
  * interpretation       exact interventional Shapley values for groups of features.
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import itertools
import math

import numpy as np
from scipy import stats

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
# EVALUATION (as in Chapter 1)
# =============================================================================
def hac_var(x, lags, kernel='bartlett', center=True):
    """Long-run variance of a series: Bartlett (Newey-West) or rectangular (truncated) kernel."""
    x = np.asarray(x, float)
    x = x - x.mean() if center else x
    T = len(x)
    v = x @ x / T
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1) if kernel == 'bartlett' else 1.0
        v += 2 * w * (x[k:] @ x[:-k]) / T
    return v


def dm_test(d, h=1, kernel='rect', lags=None):
    """Diebold-Mariano test of E[d] = 0 for the loss differential d (model 1 minus model 2), HAC variance with h - 1
    lags (rectangular; Bartlett if negative) and the Harvey-Leybourne-Newbold correction with t(T - 1)."""
    d = np.asarray(d, float)
    d = d[~np.isnan(d)]
    T = len(d)
    L = h - 1 if lags is None else lags
    v = hac_var(d, L, kernel)
    if v <= 0:
        v = hac_var(d, L, 'bartlett')
    dm = d.mean() / np.sqrt(v / T)
    hln = np.sqrt((T + 1 - 2 * h + h * (h - 1) / T) / T) * dm
    return {'T': T, 'dbar': float(d.mean()), 'dm': float(dm), 'hln': float(hln),
            'p_hln': float(2 * stats.t.sf(abs(hln), T - 1))}


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


def qlike(rv, f):
    """QLIKE loss of a variance forecast f for the realised variance rv (Patton 2011)."""
    x = np.asarray(rv, float) / np.asarray(f, float)
    return x - np.log(x) - 1


def pinball(y, q, tau):
    """Pinball (quantile) loss of the tau-quantile forecast q."""
    u = np.asarray(y, float) - np.asarray(q, float)
    return np.maximum(tau * u, (tau - 1) * u)


def smape(y, f):
    """Symmetric MAPE of the M4 competition, in % (Makridakis, Spiliotis and Assimakopoulos 2020)."""
    y, f = np.asarray(y, float), np.asarray(f, float)
    return 200 * np.mean(np.abs(y - f) / (np.abs(y) + np.abs(f)))


def mase(y, f, insample, m):
    """Mean absolute scaled error (Hyndman and Koehler 2006): scale = in-sample MAE of the seasonal naive forecast."""
    x = np.asarray(insample, float)
    return np.mean(np.abs(np.asarray(y, float) - np.asarray(f, float))) / np.mean(np.abs(x[m:] - x[:-m]))


# =============================================================================
# DEPENDENT DATA: EMBEDDING AND CROSS-VALIDATION
# =============================================================================
def embed(y, p):
    """Rows t = p, ..., n - 1: X[t] = (y_{t-1}, ..., y_{t-p}), target y_t."""
    y = np.asarray(y, float)
    n = len(y)
    X = np.column_stack([y[p - k:n - k] for k in range(1, p + 1)])
    return X, y[p:]


def ols(Xtr, ytr, Xte):
    """OLS with an intercept: predictions for Xte."""
    A = np.column_stack([np.ones(len(Xtr)), Xtr])
    b = np.linalg.lstsq(A, ytr, rcond=None)[0]
    return np.column_stack([np.ones(len(Xte)), Xte]) @ b


def loocv_ols(X, y):
    """Leave-one-out residuals of OLS with an intercept in closed form, e_i / (1 - h_ii)."""
    A = np.column_stack([np.ones(len(X)), X])
    Q, _ = np.linalg.qr(A)
    h = (Q ** 2).sum(axis=1)
    e = y - Q @ (Q.T @ y)
    return e / (1 - h)


def ar_sim(phi, n, burn=100, rng=None, theta=None, sigma=1.0):
    """Gaussian ARMA path: phi (AR coefficients, any lags), theta (MA coefficients)."""
    rng = rng or np.random.default_rng()
    phi = np.asarray(phi, float)
    theta = np.asarray(theta if theta is not None else [], float)
    e = rng.normal(0, sigma, n + burn)
    x = np.zeros(n + burn)
    p, q = len(phi), len(theta)
    for t in range(n + burn):
        v = e[t]
        for k in range(1, q + 1):
            if t - k >= 0:
                v += theta[k - 1] * e[t - k]
        for k in range(1, p + 1):
            if t - k >= 0:
                v += phi[k - 1] * x[t - k]
        x[t] = v
    return x[burn:]


def random_stationary_ar(p, rng):
    """AR(p) coefficients drawn uniformly on [-1, 1]^p and kept if the process is stationary (rejection sampling)."""
    while True:
        phi = rng.uniform(-1, 1, p)
        if np.all(np.abs(np.roots(np.r_[1.0, -phi])) < 1):
            return phi


def bhk_trial(y, pmax=5, k=5, in_frac=0.7, rng=None):
    """One Monte Carlo trial of Bergmeir, Hyndman and Koo (2018, Section 4): in-set 70%, out-set 30%; AR(1)..AR(pmax)
    by OLS; RMSE estimated by 5-fold CV, LOOCV, non-dependent CV (training rows within pmax lags of a test row
    removed) and OOS (last 20% of the in-set); the 'true' RMSE: model fitted on the whole in-set, one-step forecasts
    of the out-set. Returns a dict model -> procedure -> RMSE."""
    rng = rng or np.random.default_rng()
    y = np.asarray(y, float)
    n = len(y)
    T = int(round(in_frac * n))
    X, z = embed(y, pmax)                           # rows t = pmax..n-1
    tt = np.arange(pmax, n)
    inn = tt < T
    Xi, zi, ti = X[inn], z[inn], tt[inn]
    Xo, zo = X[~inn], z[~inn]
    m = len(zi)
    folds = rng.permutation(np.arange(m) % k)
    n_oos = int(round(0.2 * m))
    out = {}
    for p in range(1, pmax + 1):
        A = Xi[:, :p]
        e5, en = np.empty(m), np.empty(m)
        for f in range(k):
            te = folds == f
            e5[te] = zi[te] - ols(A[~te], zi[~te], A[te])
            far = np.ones(m, bool)
            for t0 in ti[te]:
                far &= np.abs(ti - t0) >= pmax
            en[te] = zi[te] - ols(A[far], zi[far], A[te])
        eo = zi[-n_oos:] - ols(A[:-n_oos], zi[:-n_oos], A[-n_oos:])
        etrue = zo - ols(A, zi, Xo[:, :p])
        r = lambda e: float(np.sqrt(np.mean(e ** 2)))
        out[f'AR({p})'] = {'5-fold CV': r(e5), 'LOOCV': r(loocv_ols(A, zi)), 'nonDepCV': r(en), 'OOS': r(eo),
                           'true': r(etrue)}
    return out


def purged_folds(n, k, gap):
    """Blocked k-fold for rows 0..n-1 with a purge: training rows within `gap` of the test block are removed."""
    edges = np.linspace(0, n, k + 1).astype(int)
    for a, b in zip(edges[:-1], edges[1:]):
        te = np.arange(a, b)
        tr = np.r_[np.arange(0, max(a - gap, 0)), np.arange(min(b + gap, n), n)]
        yield tr, te


# =============================================================================
# HIGH-DIMENSIONAL LINEAR MODELS
# =============================================================================
def standardise(Xtr, Xte):
    mu, sd = Xtr.mean(axis=0), Xtr.std(axis=0)
    sd = np.where(sd > 0, sd, 1.0)
    return (Xtr - mu) / sd, (Xte - mu) / sd


def penalised_fit(X, y, kind='lasso', keep=(), alphas=None, k=5, gap=12, l1_ratio=0.5, gamma=1.0):
    """Lasso, adaptive lasso (Zou 2006; weights |ridge coefficient|^gamma) or elastic net (Zou and Hastie 2005) on
    standardised features; the columns in `keep` are not penalised (partialled out by OLS, Frisch-Waugh-Lovell).
    The penalty is chosen by blocked k-fold CV with a purge of `gap` rows (h-step targets).
    Returns (intercept, coefficients on the original scale, chosen alpha, selected mask of the penalised columns)."""
    from sklearn.linear_model import ElasticNet, Lasso, Ridge
    X = np.asarray(X, float)
    keep = list(keep)
    pen = [j for j in range(X.shape[1]) if j not in keep]
    K = np.column_stack([np.ones(len(y))] + [X[:, j] for j in keep])
    proj = lambda v: v - K @ np.linalg.lstsq(K, v, rcond=None)[0]
    Xp, yp = proj(X[:, pen]), proj(y)
    sd = Xp.std(axis=0)
    sd = np.where(sd > 0, sd, 1.0)
    Z = Xp / sd
    w = np.ones(len(pen))
    if kind == 'adaptive':
        w = np.abs(Ridge(alpha=1.0).fit(Z, yp).coef_) ** gamma + 1e-8
    Zw = Z * w
    if alphas is None:
        alphas = np.geomspace(1.0, 1e-3, 20) * np.max(np.abs(Zw.T @ yp)) / len(y)

    def model(a):
        if kind == 'enet':
            return ElasticNet(alpha=a, l1_ratio=l1_ratio, max_iter=20000, fit_intercept=False)
        return Lasso(alpha=a, max_iter=20000, fit_intercept=False)
    cv = np.zeros(len(alphas))
    for tr, te in purged_folds(len(y), k, gap):
        for i, a in enumerate(alphas):
            cv[i] += np.sum((yp[te] - model(a).fit(Zw[tr], yp[tr]).predict(Zw[te])) ** 2)
    a = alphas[int(np.argmin(cv))]
    bp = model(a).fit(Zw, yp).coef_ * w / sd
    beta = np.zeros(X.shape[1])
    beta[pen] = bp
    bk = np.linalg.lstsq(K, y - X[:, pen] @ bp, rcond=None)[0]
    beta[keep] = bk[1:]
    return float(bk[0]), beta, float(a), np.abs(bp) > 0


# =============================================================================
# QUANTILE REGRESSION FOREST
# =============================================================================
class QRF:
    """Quantile regression forest (Meinshausen 2006): a random forest whose leaves keep all training targets;
    the conditional distribution at x is the weighted empirical distribution with weights
    w_i(x) = (1/B) sum_b 1{x_i in leaf_b(x)} / |leaf_b(x)|."""

    def __init__(self, n_estimators=100, min_samples_leaf=10, max_features=0.5, seed=0):
        from sklearn.ensemble import RandomForestRegressor
        self.rf = RandomForestRegressor(n_estimators=n_estimators, min_samples_leaf=min_samples_leaf,
                                        max_features=max_features, random_state=seed, n_jobs=1)

    def fit(self, X, y):
        self.rf.fit(X, y)
        self.y = np.asarray(y, float)
        self.order = np.argsort(self.y)
        self.leaves = self.rf.apply(X)              # n x B
        return self

    def weights(self, X):
        Lte = self.rf.apply(X)
        n, B = self.leaves.shape
        W = np.zeros((len(X), n))
        for b in range(B):
            lt = self.leaves[:, b]
            cnt = np.bincount(lt)
            same = Lte[:, b][:, None] == lt[None, :]
            W += same / cnt[lt][None, :]
        return W / B

    def predict(self, X):
        return self.rf.predict(X)

    def quantiles(self, X, taus):
        W = self.weights(X)[:, self.order]
        C = np.cumsum(W, axis=1)
        ys = self.y[self.order]
        return np.column_stack([ys[np.minimum((C < t).sum(axis=1), len(ys) - 1)] for t in taus])


# =============================================================================
# DEEP LEARNING (PyTorch, CPU)
# =============================================================================
def set_seed(seed):
    np.random.seed(seed)
    if TORCH:
        torch.manual_seed(seed)


class MLPNet(nn.Module):
    """Multilayer perceptron: L inputs -> hidden (ReLU) -> H outputs."""

    def __init__(self, L, H, hidden=32, layers=2):
        super().__init__()
        mods, d = [], L
        for _ in range(layers):
            mods += [nn.Linear(d, hidden), nn.ReLU()]
            d = hidden
        self.net = nn.Sequential(*mods, nn.Linear(d, H))

    def forward(self, x):
        return self.net(x)


class RNNNet(nn.Module):
    """Recurrent network (kind = 'rnn', 'lstm' or 'gru') on the input window; the last hidden state is mapped to H outputs."""

    def __init__(self, H, hidden=16, kind='lstm', layers=1):
        super().__init__()
        cell = {'rnn': nn.RNN, 'lstm': nn.LSTM, 'gru': nn.GRU}[kind]
        self.rnn = cell(1, hidden, num_layers=layers, batch_first=True)
        self.out = nn.Linear(hidden, H)

    def forward(self, x):
        o, _ = self.rnn(x.unsqueeze(-1))
        return self.out(o[:, -1])


class TCNNet(nn.Module):
    """Temporal convolutional network (Bai, Kolter and Koltun 2018): residual blocks of two dilated causal
    convolutions (kernel k, dilations 1, 2, 4, ...); receptive field 1 + 2 (k - 1)(2^levels - 1)."""

    def __init__(self, H, channels=16, k=3, levels=4):
        super().__init__()
        self.k = k
        self.convs = nn.ModuleList()
        self.skips = nn.ModuleList()
        c_in = 1
        for i in range(levels):
            d = 2 ** i
            self.convs.append(nn.ModuleList([nn.Conv1d(c_in, channels, k, dilation=d), nn.Conv1d(channels, channels, k, dilation=d)]))
            self.skips.append(nn.Conv1d(c_in, channels, 1) if c_in != channels else nn.Identity())
            c_in = channels
        self.out = nn.Linear(channels, H)

    def forward(self, x):
        z = x.unsqueeze(1)
        for (c1, c2), sk in zip(self.convs, self.skips):
            d = c1.dilation[0]
            pad = (self.k - 1) * d
            u = torch.relu(c1(nn.functional.pad(z, (pad, 0))))
            u = torch.relu(c2(nn.functional.pad(u, (pad, 0))))
            z = torch.relu(u + sk(z))
        return self.out(z[:, :, -1])


class LinearNet(nn.Module):
    """The linear baselines of Zeng et al. (2023): 'linear' (one layer on the window), 'nlinear' (the last value is
    subtracted and added back), 'dlinear' (moving-average trend + remainder, one linear layer each)."""

    def __init__(self, L, H, kind='dlinear', kernel=25):
        super().__init__()
        self.kind, self.kernel = kind, kernel
        self.lin = nn.Linear(L, H)
        if kind == 'dlinear':
            self.lin_t = nn.Linear(L, H)

    def forward(self, x):
        if self.kind == 'nlinear':
            last = x[:, -1:]
            return self.lin(x - last) + last
        if self.kind == 'dlinear':
            p = (self.kernel - 1) // 2
            xp = torch.cat([x[:, :1].repeat(1, p), x, x[:, -1:].repeat(1, self.kernel - 1 - p)], dim=1)
            trend = xp.unfold(1, self.kernel, 1).mean(-1)
            return self.lin(x - trend) + self.lin_t(trend)
        return self.lin(x)


class PatchTransformer(nn.Module):
    """A small patch Transformer in the spirit of PatchTST (Nie et al. 2023): instance normalisation, non-overlapping
    patches as tokens, learnable positional embedding, encoder layers with multi-head self-attention, a flatten head.
    The attention weights of the last forward pass are kept in self.attn (batch x tokens x tokens, head average)."""

    def __init__(self, L, H, patch=24, d=32, heads=4, layers=1, ff=64):
        super().__init__()
        self.patch, self.n_tok = patch, L // patch
        self.embed = nn.Linear(patch, d)
        self.pos = nn.Parameter(0.02 * torch.randn(1, self.n_tok, d))
        self.att = nn.ModuleList([nn.MultiheadAttention(d, heads, batch_first=True) for _ in range(layers)])
        self.ff = nn.ModuleList([nn.Sequential(nn.Linear(d, ff), nn.GELU(), nn.Linear(ff, d)) for _ in range(layers)])
        self.n1 = nn.ModuleList([nn.LayerNorm(d) for _ in range(layers)])
        self.n2 = nn.ModuleList([nn.LayerNorm(d) for _ in range(layers)])
        self.head = nn.Linear(self.n_tok * d, H)
        self.attn = None

    def forward(self, x):
        x = x[:, -self.n_tok * self.patch:]
        mu, sd = x.mean(1, keepdim=True), x.std(1, keepdim=True) + 1e-5
        z = ((x - mu) / sd).reshape(len(x), self.n_tok, self.patch)
        z = self.embed(z) + self.pos
        for att, ff, n1, n2 in zip(self.att, self.ff, self.n1, self.n2):
            a, w = att(z, z, z, need_weights=True, average_attn_weights=True)
            self.attn = w.detach()
            z = n1(z + a)
            z = n2(z + ff(z))
        return self.head(z.flatten(1)) * sd + mu


class NBeatsBlock(nn.Module):
    """One N-BEATS block (Oreshkin et al. 2020): a fully connected stack, then linear backcast and forecast.
    pool > 1 and n_coef < H give the N-HiTS block (Challu et al. 2023): max-pooled input and a forecast of n_coef
    coefficients interpolated linearly to H points."""

    def __init__(self, L, H, width=128, layers=3, pool=1, n_coef=None):
        super().__init__()
        self.L, self.H, self.pool = L, H, pool
        self.n_coef = n_coef or H
        mods, d = [], L // pool
        for _ in range(layers):
            mods += [nn.Linear(d, width), nn.ReLU()]
            d = width
        self.fc = nn.Sequential(*mods)
        self.back = nn.Linear(width, L)
        self.fore = nn.Linear(width, self.n_coef)

    def forward(self, x):
        u = x if self.pool == 1 else nn.functional.max_pool1d(x.unsqueeze(1), self.pool, self.pool).squeeze(1)
        h = self.fc(u)
        f = self.fore(h)
        if self.n_coef != self.H:
            f = nn.functional.interpolate(f.unsqueeze(1), size=self.H, mode='linear', align_corners=True).squeeze(1)
        return self.back(h), f


class NBeatsNet(nn.Module):
    """Doubly residual stacking: x_{l+1} = x_l - backcast_l, forecast = sum_l forecast_l. Generic N-BEATS:
    pools = (1, 1, ...); N-HiTS: pools = (8, 4, 1) with n_coefs = (H // 12, H // 4, H)."""

    def __init__(self, L, H, width=128, layers=3, pools=(1, 1, 1), n_coefs=None):
        super().__init__()
        n_coefs = n_coefs or [None] * len(pools)
        self.blocks = nn.ModuleList([NBeatsBlock(L, H, width, layers, p, c) for p, c in zip(pools, n_coefs)])

    def forward(self, x):
        scale = x.abs().mean(1, keepdim=True) + 1e-5     # each window divided by its mean absolute level
        r, f = x / scale, 0.0
        for b in self.blocks:
            bc, fc = b(r)
            r = r - bc
            f = f + fc
        return f * scale


def fit_torch(model, X, Y, epochs=60, lr=1e-3, batch=128, val_frac=0.2, patience=8, seed=0, loss='mse',
              weight_decay=0.0, max_steps=None):
    """Adam on mini-batches; the last val_frac of the (chronological) sample is the validation block for early
    stopping; the weights with the lowest validation loss are kept. loss: 'mse', 'mae' or a callable."""
    set_seed(seed)
    X = torch.as_tensor(np.asarray(X, np.float32))
    Y = torch.as_tensor(np.asarray(Y, np.float32))
    n = len(X)
    nv = int(round(val_frac * n))
    Xt, Yt, Xv, Yv = X[:n - nv], Y[:n - nv], X[n - nv:], Y[n - nv:]
    lf = {'mse': nn.functional.mse_loss, 'mae': nn.functional.l1_loss}.get(loss, loss)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    g = torch.Generator().manual_seed(seed)
    best, best_state, wait, steps = np.inf, None, 0, 0
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(len(Xt), generator=g)
        for i in range(0, len(Xt), batch):
            j = perm[i:i + batch]
            opt.zero_grad()
            ls = lf(model(Xt[j]), Yt[j])
            ls.backward()
            opt.step()
            steps += 1
            if max_steps and steps >= max_steps:
                break
        model.eval()
        with torch.no_grad():
            v = float(lf(model(Xv), Yv)) if nv else float(ls)
        if v < best - 1e-7:
            best, wait = v, 0
            best_state = {k: t.clone() for k, t in model.state_dict().items()}
        else:
            wait += 1
            if wait >= patience:
                break
        if max_steps and steps >= max_steps:
            break
    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    return model


def predict_torch(model, X, batch=4096):
    X = torch.as_tensor(np.asarray(X, np.float32))
    with torch.no_grad():
        return np.concatenate([model(X[i:i + batch]).numpy() for i in range(0, len(X), batch)])


def grad_through_time(kind, T=100, hidden=32, batch=64, seed=0, forget_bias=None):
    """Mean |d h_T / d x_t| (t = 1..T, summed over the units of h_T) for a freshly initialised RNN, LSTM or GRU
    (PyTorch default initialisation), Gaussian inputs: how far back the gradient reaches before any training.
    forget_bias: for the LSTM, the bias of the forget gate (0 at the default initialisation)."""
    set_seed(seed)
    cell = {'rnn': nn.RNN, 'lstm': nn.LSTM, 'gru': nn.GRU}[kind](1, hidden, batch_first=True)
    if kind == 'lstm' and forget_bias is not None:
        with torch.no_grad():
            cell.bias_ih_l0[hidden:2 * hidden] = forget_bias
            cell.bias_hh_l0[hidden:2 * hidden] = 0.0
    x = torch.randn(batch, T, 1, requires_grad=True)
    o, _ = cell(x)
    o[:, -1].sum().backward()
    return x.grad.abs().squeeze(-1).mean(0).numpy()


DEEPAR_LAGS = (1, 24, 168)


class DeepARNet(nn.Module):
    """A DeepAR-type model (Salinas et al. 2020): an LSTM over (scaled lagged targets at lags 1, 24, 168; sin and cos of
    the hour of the day) whose state gives the mean and the standard deviation of a Gaussian for the next scaled value."""

    def __init__(self, hidden=40, layers=2, n_in=len(DEEPAR_LAGS) + 2):
        super().__init__()
        self.lstm = nn.LSTM(n_in, hidden, num_layers=layers, batch_first=True)
        self.mu = nn.Linear(hidden, 1)
        self.sd = nn.Linear(hidden, 1)

    def forward(self, feat, state=None):
        o, state = self.lstm(feat, state)
        return self.mu(o).squeeze(-1), nn.functional.softplus(self.sd(o)).squeeze(-1) + 1e-3, state


def deepar_features(Z, P, j0, j1, lags=DEEPAR_LAGS, period=24):
    """Inputs for the targets at columns j0..j1-1 of the scaled segments Z (batch x length): the lagged values and the
    hour of the day of the target (positions P, same shape as Z)."""
    cols = np.arange(j0, j1)
    lagged = [Z[:, cols - l] for l in lags]
    a = 2 * np.pi * (P[:, cols] % period) / period
    return np.stack(lagged + [np.sin(a), np.cos(a)], -1).astype(np.float32)


def deepar_train(series, C, H, steps=1500, batch=64, lr=1e-3, seed=0, hidden=40, layers=2, lags=DEEPAR_LAGS, checkpoints=()):
    """Train on random segments of length max(lags) + C + H, with the Gaussian log-likelihood of the last C + H values
    given their lagged values (teacher forcing); each segment is divided by 1 + the mean of its context, as in DeepAR.
    checkpoints: steps at which a copy of the weights is kept (returned in net.checkpoints)."""
    set_seed(seed)
    rng = np.random.default_rng(seed)
    net = DeepARNet(hidden, layers, len(lags) + 2)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    M = max(lags)
    S = M + C + H
    ok = [i for i, s in enumerate(series) if len(s) > S]
    saved = {}
    for step in range(1, steps + 1):
        Z, P = [], []
        for i in rng.choice(ok, batch):
            a = rng.integers(0, len(series[i]) - S + 1)
            Z.append(series[i][a:a + S])
            P.append(np.arange(a, a + S))
        Z, P = np.array(Z, np.float32), np.array(P)
        Z = Z / (1 + Z[:, M:M + C].mean(1, keepdims=True))
        mu, sd, _ = net(torch.as_tensor(deepar_features(Z, P, M, S, lags)))
        y = torch.as_tensor(Z[:, M:S])
        nll = (torch.log(sd) + 0.5 * ((y - mu) / sd) ** 2).mean()
        opt.zero_grad()
        nll.backward()
        opt.step()
        if step in checkpoints:
            saved[step] = {k: v.clone() for k, v in net.state_dict().items()}
    net.eval()
    net.checkpoints = saved
    return net


def deepar_sample(net, histories, starts, C, H, n_samples=100, seed=0, lags=DEEPAR_LAGS):
    """Ancestral sampling of H steps after each history (array n x (max(lags) + C), the last values of a series whose
    first value has position `starts`): the LSTM runs over the context with the observed values, then each sampled
    value is fed back. Returns samples n x n_samples x H on the original scale."""
    set_seed(seed)
    Hst = np.asarray(histories, np.float32)
    n, M = len(Hst), max(lags)
    sc = 1 + Hst[:, M:M + C].mean(1, keepdims=True)
    Z = np.zeros((n * n_samples, M + C + H), np.float32)
    Z[:, :M + C] = np.repeat(Hst / sc, n_samples, 0)
    P = np.repeat(np.asarray(starts)[:, None] + np.arange(M + C + H)[None, :], n_samples, 0)
    with torch.no_grad():
        _, _, state = net(torch.as_tensor(deepar_features(Z, P, M, M + C, lags)))
        for k in range(H):
            j = M + C + k
            mu, sd, state = net(torch.as_tensor(deepar_features(Z, P, j, j + 1, lags)), state)
            Z[:, j] = (mu[:, 0] + sd[:, 0] * torch.randn(len(Z))).numpy()
    return Z[:, M + C:].reshape(n, n_samples, H) * sc[:, :, None]


# =============================================================================
# INTERPRETATION
# =============================================================================
def shapley_groups(predict, X, background, groups):
    """Exact interventional Shapley values of feature groups: v(S) = mean over the background rows of the prediction
    with the features of S taken from x and the others from the background row; phi_g = sum over S without g of
    |S|!(G - |S| - 1)!/G! [v(S + g) - v(S)]. Returns phi (n x G) and the base value v(empty)."""
    X, Bg = np.asarray(X, float), np.asarray(background, float)
    G = len(groups)
    n, nb = len(X), len(Bg)
    v = {}
    for r in range(G + 1):
        for S in itertools.combinations(range(G), r):
            Z = np.repeat(Bg[None], n, 0)
            for g in S:
                Z[:, :, groups[g]] = X[:, None, groups[g]]
            v[S] = predict(Z.reshape(n * nb, -1)).reshape(n, nb).mean(1)
    phi = np.zeros((n, G))
    for g in range(G):
        rest = [j for j in range(G) if j != g]
        for r in range(G):
            for S in itertools.combinations(rest, r):
                w = math.factorial(r) * math.factorial(G - r - 1) / math.factorial(G)
                phi[:, g] += w * (v[tuple(sorted(S + (g,)))] - v[S])
    return phi, float(v[()].mean())
