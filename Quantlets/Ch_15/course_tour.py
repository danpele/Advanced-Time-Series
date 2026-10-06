"""
course_tour.py -- the course in one notebook (ATS, Chapter 15): one short computation per chapter on real data
=============================================================================================================
Each function reproduces in a few lines the central tool of one chapter, on the course data (EODHD daily data in
data/market, the BNR reference rate, FRED), and returns a small dictionary of results:
  tour_dependence   (Ch. 0)  mean of squared S&P 500 returns: i.i.d. against Newey-West standard error; Omega / gamma_0
  tour_forecast     (Ch. 1)  EUR/RON monthly: random walk against AR(1), rolling window, DM-HLN and Clark-West
  tour_breaks       (Ch. 2)  sup-Wald test for a break in the variance of US GDP growth (15% trimming)
  tour_svar         (Ch. 3)  recursive VAR for US industrial production, inflation and the federal funds rate
  tour_state_space  (Ch. 6)  local level model for US CPI inflation (statsmodels UnobservedComponents)
  tour_regimes      (Ch. 7)  two-regime Markov-switching mean for US GDP growth
  tour_var_backtest (Ch. 9)  historical-simulation VaR 1% for the S&P 500 and the Kupiec test
  tour_long_memory  (Ch. 10) local Whittle d of absolute S&P 500 returns for several bandwidths
  tour_spectrum     (Ch. 11) smoothed periodogram of US industrial production growth: share of business-cycle variance
  tour_conformal    (Ch. 13) split conformal and ACI intervals for daily S&P 500 returns
  tour_granger      (Ch. 14) Granger tests between the S&P 500 and the BET with HAC covariance
  tour_bubbles      (Ch. 16) SADF for the weekly Nasdaq 100, 1990-2004
numpy, pandas, scipy, statsmodels.
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import math

import numpy as np
import pandas as pd
from scipy import optimize, stats

from ats_data import load_close, log_returns, read_fred
from review_core import dm_test, lrv, nw_lags


def tour_dependence():
    r = log_returns('sp500', start='2000-01-01')
    x = (r ** 2).values
    T = len(x)
    g0 = x.var()
    om = lrv(x, int(1.3 * math.sqrt(T)))
    se_iid, se_nw = math.sqrt(g0 / T), math.sqrt(om / T)
    return dict(T=T, mean=float(x.mean()), ratio=float(om / g0), se_iid=se_iid, se_nw=se_nw)


def tour_forecast(window=60, first='2016-01'):
    s = load_close('eurron')
    y = np.log(s.resample('ME').last()).diff().dropna() * 100
    if s.index[-1] < y.index[-1] - pd.Timedelta(days=3):
        y = y.iloc[:-1]
    t0 = int(np.argmax(y.index >= pd.Timestamp(first)))
    e_rw, e_ar, f_ar = [], [], []
    for t in range(t0, len(y)):
        tr = y.iloc[t - window:t].values
        b = np.linalg.lstsq(np.column_stack([np.ones(window - 1), tr[:-1]]), tr[1:], rcond=None)[0]
        f = b[0] + b[1] * tr[-1]
        e_rw.append(y.iloc[t])
        e_ar.append(y.iloc[t] - f)
        f_ar.append(f)
    e_rw, e_ar, f_ar = map(np.array, (e_rw, e_ar, f_ar))
    cw = e_rw ** 2 - (e_ar ** 2 - f_ar ** 2)
    P = len(cw)
    return dict(P=P, ratio=float(np.sqrt(np.mean(e_ar ** 2) / np.mean(e_rw ** 2))), dm=dm_test(e_ar, e_rw),
                cw=float(cw.mean() / math.sqrt(lrv(cw, nw_lags(P)) / P)))


def sup_wald_mean(x, trim=0.15):
    """sup-Wald statistic for one break in the mean of x (HAC variance under the null) and its date index."""
    x = np.asarray(x, float)
    T = len(x)
    om = lrv(x)
    best, kb = 0.0, None
    for k in range(int(trim * T), int((1 - trim) * T)):
        d = x[:k].mean() - x[k:].mean()
        w = d ** 2 / (om * (1 / k + 1 / (T - k)))
        if w > best:
            best, kb = w, k
    return best, kb


def tour_breaks():
    g = 400 * np.log(read_fred('GDPC1')).diff().dropna().loc['1953':'2019']
    u = np.abs(g - g.mean())
    W, k = sup_wald_mean(u.values)
    return dict(T=len(u), supW=float(W), date=str(u.index[k].date()),
                sd_before=float(g.iloc[:k].std()), sd_after=float(g.iloc[k:].std()))


def tour_svar(p=12):
    from statsmodels.tsa.api import VAR
    f = read_fred(['INDPRO', 'CPIAUCSL', 'FEDFUNDS']).dropna().loc['1965':'2007']
    d = pd.DataFrame({'ip': 100 * np.log(f['INDPRO']).diff(), 'pi': 100 * np.log(f['CPIAUCSL']).diff(),
                      'ff': f['FEDFUNDS']}).dropna()
    res = VAR(d).fit(p)
    irf = res.irf(48).orth_irfs                       # Cholesky, ordering ip, pi, ff
    ip_cum = np.cumsum(irf[:, 0, 2])                  # level response of IP to a funds-rate shock
    return dict(T=int(res.nobs), shock_sd=float(irf[0, 2, 2]), ip_min=float(ip_cum.min()), ip_argmin=int(ip_cum.argmin()),
                pi_max_12=float(np.cumsum(irf[:, 1, 2])[:12].max()))


def tour_state_space():
    from statsmodels.tsa.statespace.structural import UnobservedComponents
    c = read_fred('CPIAUCSL').loc['1990':]
    pi = (1200 * np.log(c).diff()).dropna()
    m = UnobservedComponents(pi.values, level='llevel').fit(disp=False)
    lvl = m.smoothed_state[0]
    return dict(T=len(pi), s2_irr=float(m.params[0]), s2_level=float(m.params[1]), q=float(m.params[1] / m.params[0]),
                level_last=float(lvl[-1]), last=str(pi.index[-1].date()))


def tour_regimes():
    from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
    g = 400 * np.log(read_fred('GDPC1')).diff().dropna().loc['1953':'2019']
    m = MarkovRegression(g.values, k_regimes=2, trend='c', switching_variance=False).fit(search_reps=20)
    mu = m.params[2:4]
    lo = int(np.argmin(mu))
    P = m.regime_transition
    p_ll = float(P[lo, lo, 0])
    prob = m.smoothed_marginal_probabilities[:, lo]
    return dict(mu_low=float(mu[lo]), mu_high=float(mu[1 - lo]), p_low=p_ll, dur_low=1 / (1 - p_ll),
                share_low=float(np.mean(prob > 0.5)))


def tour_var_backtest(window=500, alpha=0.01, start='2010-01-01'):
    r = log_returns('sp500', start='2005-01-01')
    q = r.rolling(window).quantile(alpha).shift(1)
    d = pd.DataFrame({'r': r, 'q': q}).dropna().loc[start:]
    hits = (d['r'] < d['q']).astype(int)
    T, x = len(hits), int(hits.sum())
    ph = x / T
    LR = -2 * ((T - x) * math.log(1 - alpha) + x * math.log(alpha) - (T - x) * math.log(1 - ph) - x * math.log(ph))
    return dict(T=T, hits=x, rate=ph, LR=LR, p=float(stats.chi2.sf(LR, 1)))


def local_whittle(x, m):
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    lam = 2 * np.pi * np.arange(1, m + 1) / n
    I = np.abs(np.fft.fft(x)[1:m + 1]) ** 2 / (2 * np.pi * n)

    def R(d):
        return math.log(np.mean(lam ** (2 * d) * I)) - 2 * d * np.mean(np.log(lam))
    return float(optimize.minimize_scalar(R, bounds=(-0.49, 0.99), method='bounded').x)


def tour_long_memory():
    a = np.abs(log_returns('sp500', start='2000-01-01').values)
    n = len(a)
    return {f'm=n^{e}': local_whittle(a, int(n ** e)) for e in (0.5, 0.6, 0.7, 0.8)}


def tour_spectrum():
    ip = 100 * np.log(read_fred('INDPRO').loc['1960':'2019']).diff().dropna()
    x = ip.values - ip.values.mean()
    n = len(x)
    I = np.abs(np.fft.rfft(x)) ** 2 / n
    fr = np.fft.rfftfreq(n)                           # cycles per month
    k = np.ones(9) / 9
    Is = np.convolve(I, k, mode='same')
    per = np.divide(1.0, fr, out=np.full_like(fr, np.inf), where=fr > 0) / 12   # period in years
    bc = (per >= 1.5) & (per <= 8)
    return dict(n=n, share_bc=float(Is[bc].sum() / Is[1:].sum()), peak_years=float(per[1:][np.argmax(Is[1:])]))


def tour_conformal(alpha=0.1, n_cal=500, gamma=0.005):
    r = log_returns('sp500', start='2010-01-01').values
    s = np.abs(r)
    T = len(r)
    q_static = np.quantile(s[:n_cal], math.ceil((n_cal + 1) * (1 - alpha)) / n_cal)
    miss_static = np.abs(r[n_cal:]) > q_static
    a_t, miss = alpha, []
    for t in range(n_cal, T):
        cal = s[t - n_cal:t]
        lev = min(max(1 - a_t, 0.0), 1.0)
        q = np.quantile(cal, lev) if lev < 1 else np.inf
        err = float(abs(r[t]) > q)
        miss.append(err)
        a_t += gamma * (alpha - err)
    miss = np.array(miss)
    return dict(cov_static=float(1 - miss_static.mean()), cov_aci=float(1 - miss.mean()),
                cov_static_2020=float(1 - miss_static[-1000:].mean()), n=T - n_cal)


def tour_granger(p=2):
    d = pd.concat([log_returns('sp500', start='2015-01-01'), log_returns('bet', start='2015-01-01')], axis=1).dropna()
    out = {}
    for y, x in (('bet', 'sp500'), ('sp500', 'bet')):
        Y = d[y].values[p:]
        X = [np.ones(len(Y))] + [d[y].values[p - j:-j] for j in range(1, p + 1)] + [d[x].values[p - j:-j] for j in range(1, p + 1)]
        X = np.column_stack(X)
        XtXi = np.linalg.inv(X.T @ X)
        b = XtXi @ X.T @ Y
        e = Y - X @ b
        u = X * e[:, None]
        L = nw_lags(len(Y))
        S = u.T @ u
        for j in range(1, L + 1):
            G = u[j:].T @ u[:-j]
            S += (1 - j / (L + 1)) * (G + G.T)
        V = XtXi @ S @ XtXi
        idx = list(range(1 + p, 1 + 2 * p))
        W = float(b[idx] @ np.linalg.solve(V[np.ix_(idx, idx)], b[idx]))
        out[f'{x}->{y}'] = dict(W=W, p=float(stats.chi2.sf(W, p)))
    return out


def adf_stat(y):
    dy = np.diff(y)
    X = np.column_stack([np.ones(len(dy)), y[:-1]])
    b, res, *_ = np.linalg.lstsq(X, dy, rcond=None)
    e = dy - X @ b
    s2 = e @ e / (len(dy) - 2)
    return b[1] / math.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])


def sadf(y, w0):
    return max(adf_stat(y[:k]) for k in range(w0, len(y) + 1))


def tour_bubbles(reps=199, seed=2026):
    p = load_close('ndx', start='1990-01-01', end='2004-12-31').resample('W-FRI').last().dropna()
    y = np.log(p.values)
    T = len(y)
    r0 = 0.01 + 1.8 / math.sqrt(T)
    w0 = int(r0 * T)
    sadf_path = [adf_stat(y[:k]) for k in range(w0, T + 1)]
    k = int(np.argmax(sadf_path))
    rng = np.random.default_rng(seed)
    null = [sadf(np.cumsum(rng.standard_normal(T)), w0) for _ in range(reps)]   # random walk without drift
    return dict(T=T, w0=w0, sadf=float(max(sadf_path)), date=str(p.index[w0 - 1 + k].date()),
                cv95_mc=float(np.quantile(null, 0.95)), reps=reps)
