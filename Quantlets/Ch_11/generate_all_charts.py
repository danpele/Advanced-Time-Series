"""
generate_all_charts.py -- charts and numbers of Chapter 11 (ATS): spectral and wavelet analysis
===============================================================================================
Course data (ats_data.py), chart style (ats_style.py), the numpy engine spectral_core.py. Every number on the slides
comes from here.
  * spectral representation  band decomposition of an AR(2) path and the variance shares given by its spectrum;
  * estimation theory        lag windows and spectral windows; bias, variance and MSE of the Parzen estimator against
                             the bandwidth (Monte Carlo and asymptotic formulas); leakage and the multitaper estimator
                             (Thomson 1982) on the AR(4) of Percival and Walden (1993); DPSS tapers; coverage of the
                             chi-square bands; Romanian and euro-area industrial production; the harmonic F test as a
                             check of residual seasonality;
  * two series               coherence, phase and gain of Romanian and euro-area industrial production; dynamic
                             correlation (Croux, Forni and Reichlin 2001) of GDP growth in Romania, Poland, Hungary,
                             Czechia with the euro area; Geweke (1982) measures and the Breitung-Candelon (2006) test;
  * filters                  gains of the ideal band-pass, Baxter-King, Christiano-Fitzgerald, HP and Hamilton filters;
                             the spurious cycle of the HP filter on a random walk (Cogley and Nason 1995); cycles of
                             Romanian GDP; end-point revisions; synchronisation with the euro area;
  * nonstationary spectra    a time-varying AR(2) and its short-time multitaper spectrogram;
  * wavelets                 MODWT filters, multiresolution analysis, wavelet variance and correlation by scale of the
                             BET, DAX and S&P 500; Morlet wavelet power of the BET; wavelet coherence (Monte Carlo
                             significance) of BET-DAX, BET-S&P 500, Brent-S&P 500 and of inflation in Romania and
                             Poland with the euro area; the areawise check of the AI mini-case.
Output: charts/ats_ch11_*.pdf/.png, Quantlets/Ch_11/ch11_numbers.json
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_11/generate_all_charts.py [name ...]
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
from ats_data import load_close, read_eurostat, read_fred                                    # noqa: E402
import ats_style as st                                                                      # noqa: E402
from spectral_core import (_transfer, acov, andrews_bandwidth, ar1_coef, arma_spectrum, band_dyncorr, bk_filter,  # noqa: E402
                           bk_weights, breitung_candelon, coi_mask, cross_spectrum, cwt, daniell, dpss,
                           filter_gain, geweke, hamilton_filter, hamilton_gain, harmonic_ftest, hp_filter,
                           hp_gain, hp_one_sided, ideal_gain, kernel, KERNEL_CONST, lag_window, modwt, mra,
                           multitaper, periodogram, red_noise_signif, simulate_arma, var_order, wavelet_coherence,
                           wavelet_corr, wavelet_filters, wavelet_variance, welch, wtc_montecarlo, concordance)

warnings.filterwarnings('ignore')
SEED = 2026
END = '2026-09-18'
PW_AR4 = (2.7607, -3.8106, 2.6535, -0.9238)       # Percival and Walden (1993, eq. 46a): a spectrum with 60 dB range
AR2 = (1.3, -0.7)                                 # a business-cycle-like AR(2): peak near 9.5 periods
AR2_SHARP = (1.6, -0.9)                           # a sharper peak for the bias-variance experiment
BC_Q = (6, 32)                                    # business-cycle band in quarters (Burns-Mitchell, Baxter-King)
BC_M = (18, 96)                                   # the same band in months
CEE = ['RO', 'PL', 'HU', 'CZ']
GEO_LAB = {'RO': 'Romania', 'PL': 'Poland', 'HU': 'Hungary', 'CZ': 'Czechia', 'EA20': 'euro area', 'EA': 'euro area'}
GEO_COL = {'RO': st.IDAred, 'PL': st.Purple, 'HU': st.Forest, 'CZ': st.Orange, 'EA20': st.MainBlue, 'EA': st.MainBlue}
_MEM = {}


# =============================================================================
# DATA AND HELPERS
# =============================================================================
def save(name, save_it=True):
    if save_it:
        st.check_no_grey(plt.gcf())
        st.save_fig(name)
    else:
        plt.show()


def online(fn, *a, tries=4, **k):
    """Online sources (Eurostat, FRED) with a few retries."""
    key = (fn.__name__,) + a + tuple(sorted(k.items()))
    if key in _MEM:
        return _MEM[key]
    for i in range(tries):
        try:
            _MEM[key] = fn(*a, **k)
            return _MEM[key]
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def gdp(geo, end='2026-06-30'):
    """100 x log real GDP (chain-linked volumes 2010, seasonally and calendar adjusted), Eurostat namq_10_gdp."""
    s = online(read_eurostat, 'namq_10_gdp', f'Q.CLV10_MEUR.SCA.B1GQ.{geo}')
    return (100 * np.log(s.loc['1995-01-01':end])).rename(geo)


def ip(geo, adj='SCA'):
    """100 x log industrial production (B-D: mining, manufacturing, energy), 2021 = 100, Eurostat sts_inpr_m."""
    s = online(read_eurostat, 'sts_inpr_m', f'M.PRD.B-D.{adj}.I21.{geo}')
    return (100 * np.log(s.loc['2000-01-01':])).rename(geo)


def hicp(geo, start='2001-01-01'):
    """HICP annual rate of change (%), all items, Eurostat prc_hicp_minr."""
    s = online(read_eurostat, 'prc_hicp_minr', f'M.RCH_A.TOTAL.{geo}')
    return s.loc[start:].rename(geo)


def weekly_returns(name, start='2000-01-01', end=END):
    """Weekly log returns in % from Friday closes (the last close of each week)."""
    p = load_close(name, start=start, end=end).resample('W-FRI').last().dropna()
    return (100 * np.log(p).diff().dropna()).rename(name)


def brent_weekly(start='2000-01-01', end=END):
    p = online(read_fred, 'DCOILBRENTEU').loc[start:end].dropna()
    p = p[p > 0].resample('W-FRI').last().dropna()
    return (100 * np.log(p).diff().dropna()).rename('brent')


def daily_common(names, start='2000-01-01', end=END):
    """Daily log returns in % on the days on which all markets traded (prices aligned first)."""
    p = pd.concat([load_close(n, start=start, end=end) for n in names], axis=1, join='inner').dropna()
    return 100 * np.log(p).diff().dropna()


def per_axis(ax, lo, hi, ticks, label='period'):
    """Logarithmic period axis (long cycles on the left)."""
    ax.set_xscale('log')
    ax.set_xlim(hi, lo)
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    ax.minorticks_off()
    ax.set_xlabel(label)


def shade_band(ax, lo, hi, label='business-cycle band'):
    ax.axvspan(lo, hi, color=st.Amber, alpha=0.15, lw=0, label=label)


# =============================================================================
# 1. SPECTRAL REPRESENTATION: VARIANCE BY FREQUENCY BAND
# =============================================================================
def fig_bands(save_it=True, n=240):
    """An AR(2) path split by FFT into long (> 32), business-cycle (6-32) and short (< 6) components; the variance
    shares 2 int_band f / gamma(0) of the spectrum against the shares in the sample."""
    rng = np.random.default_rng(SEED)
    x = simulate_arma(n, ar=AR2, rng=rng)
    X = np.fft.rfft(x - x.mean())
    per = np.r_[np.inf, n / np.arange(1, len(X))]
    bands = {'long (> 32)': per > 32, 'business cycle (6-32)': (per >= 6) & (per <= 32), 'short (< 6)': per < 6}
    comp = {k: np.fft.irfft(X * m, n) for k, m in bands.items()}
    om = np.linspace(1e-6, np.pi, 200001)
    f = arma_spectrum(om, ar=AR2)
    g0 = 2 * np.trapezoid(f, om)
    th = {'long (> 32)': (0, 2 * np.pi / 32), 'business cycle (6-32)': (2 * np.pi / 32, 2 * np.pi / 6),
          'short (< 6)': (2 * np.pi / 6, np.pi)}
    share_th = {k: float(2 * np.trapezoid(f[(om >= a) & (om <= b)], om[(om >= a) & (om <= b)]) / g0) for k, (a, b) in th.items()}
    share_s = {k: float(np.var(v) / np.var(x)) for k, v in comp.items()}
    fig, axs = plt.subplots(2, 2, figsize=(12, 4.8), sharex=True)
    axs = axs.ravel()
    axs[0].plot(x, color=st.MainBlue, lw=1.1)
    axs[0].set_title('AR(2) path')
    for ax, (k, v), c in zip(axs[1:], comp.items(), [st.Forest, st.IDAred, st.Purple]):
        ax.plot(v, color=c, lw=1.1)
        ax.set_title(f'{k}: {100 * share_s[k]:.0f}% of the sample variance, {100 * share_th[k]:.0f}% in theory')
        ax.set_ylim(axs[0].get_ylim())
    for ax in axs[2:]:
        ax.set_xlabel('t (quarters)')
    plt.tight_layout()
    save('ats_ch11_bands', save_it)
    peak = float(2 * np.pi / om[np.argmax(f)])
    return dict(theory=share_th, sample=share_s, peak=peak, n=n, g0=float(g0))


# =============================================================================
# 2. ESTIMATION THEORY
# =============================================================================
def fig_kernels(save_it=True, M=10):
    """Lag windows k(u) and the corresponding spectral windows W_M(w) = (2 pi)^-1 sum_{|h| < M'} k(h/M) exp(-i w h)."""
    u = np.linspace(0, 1.3, 400)
    om = np.linspace(-np.pi / 2, np.pi / 2, 801)
    names = {'bartlett': 'Bartlett', 'parzen': 'Parzen', 'tukey': 'Tukey-Hanning', 'qs': 'quadratic spectral'}
    cols = [st.MainBlue, st.IDAred, st.Forest, st.Purple]
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.0))
    out = {}
    for (k, lab), c in zip(names.items(), cols):
        axs[0].plot(u, kernel(u, k), color=c, lw=1.8, label=lab)
        h = np.arange(1, 400)
        w = (1 + 2 * (kernel(h / M, k)[:, None] * np.cos(np.outer(h, om))).sum(axis=0)) / (2 * np.pi)
        axs[1].plot(om, w, color=c, lw=1.6)
        out[k] = dict(q=KERNEL_CONST[k][0], kq=KERNEL_CONST[k][1], k2=KERNEL_CONST[k][2],
                      w0=float(w[np.argmin(np.abs(om))]), wmin=float(w.min()))
    axs[0].set_xlabel('u = h / M')
    axs[0].set_ylabel('lag window k(u)')
    axs[1].set_xlabel('frequency (radians)')
    axs[1].set_ylabel(f'spectral window, M = {M}')
    axs[1].axhline(0, color=st.DarkText, lw=0.6)
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch11_kernels', save_it)
    return out


def fig_bias_variance(save_it=True, n=512, reps=400, Ms=(6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256)):
    """Parzen lag-window estimator at the peak of an AR(2) spectrum: Monte Carlo bias^2, variance and MSE against M,
    and the asymptotic approximations bias = -(k_2 / M^2) f^(2)(w), variance = (M / n) f(w)^2 int k^2."""
    rng = np.random.default_rng(SEED)
    om = np.linspace(1e-4, np.pi, 20001)
    f = arma_spectrum(om, ar=AR2_SHARP)
    wp = float(om[np.argmax(f)])
    fp = float(arma_spectrum([wp], ar=AR2_SHARP)[0])
    # f^(2)(w) = (2 pi)^-1 sum_h h^2 gamma(h) e^{-i w h}: gamma from the inverse transform of the spectrum
    H = 400
    g = np.array([2 * np.trapezoid(f * np.cos(h * om), om) for h in range(H)])
    f2 = float((0 * g[0] + 2 * np.sum(np.arange(1, H) ** 2 * g[1:] * np.cos(wp * np.arange(1, H)))) / (2 * np.pi))
    est = np.zeros((reps, len(Ms)))
    for r in range(reps):
        x = simulate_arma(n, ar=AR2_SHARP, rng=rng)
        for i, M in enumerate(Ms):
            est[r, i] = lag_window(x, M, 'parzen', omega=[wp])[1][0]
    bias2 = (est.mean(axis=0) - fp) ** 2
    var = est.var(axis=0)
    mse = bias2 + var
    q, kq, k2 = KERNEL_CONST['parzen']
    Mg = np.linspace(Ms[0], Ms[-1], 300)
    b_as = (kq * f2 / Mg ** 2) ** 2
    v_as = Mg / n * fp ** 2 * k2
    M_th = float((4 * kq ** 2 * f2 ** 2 * n / (fp ** 2 * k2)) ** 0.2)
    fig, ax = plt.subplots(figsize=(10.5, 4.3))
    ax.plot(Ms, bias2 / fp ** 2, 'o-', color=st.IDAred, lw=1.6, label='squared bias (Monte Carlo)')
    ax.plot(Ms, var / fp ** 2, 's-', color=st.MainBlue, lw=1.6, label='variance (Monte Carlo)')
    ax.plot(Ms, mse / fp ** 2, 'D-', color=st.Forest, lw=2, label='MSE (Monte Carlo)')
    ax.plot(Mg, b_as / fp ** 2, '--', color=st.IDAred, lw=1.1, label='asymptotic squared bias')
    ax.plot(Mg, v_as / fp ** 2, '--', color=st.MainBlue, lw=1.1, label='asymptotic variance')
    ax.axvline(M_th, color=st.Amber, ls=':', lw=1.6, label=f'asymptotic optimum M* = {M_th:.0f}')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xticks(Ms)
    ax.set_xticklabels([str(m) for m in Ms])
    ax.minorticks_off()
    ax.set_ylim(1e-3, 5)
    ax.set_xlabel('truncation lag M (Parzen window), n = 512')
    ax.set_ylabel('relative to f(peak)$^2$')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch11_bias_variance', save_it)
    i = int(np.argmin(mse))
    return dict(M_mc=int(Ms[i]), M_th=M_th, peak_period=2 * np.pi / wp, rmse_opt=float(np.sqrt(mse[i]) / fp),
                rmse_12=float(np.sqrt(mse[Ms.index(12)]) / fp), rmse_96=float(np.sqrt(mse[Ms.index(96)]) / fp),
                bias_12=float(np.sqrt(bias2[Ms.index(12)]) / fp), sd_96=float(np.sqrt(var[Ms.index(96)]) / fp), reps=reps, n=n)


def fig_leakage(save_it=True, n=1024, reps=200):
    """The AR(4) of Percival and Walden: true spectrum, raw periodogram, Hann-tapered periodogram and multitaper
    (NW = 4, K = 7) for one path; Monte Carlo mean bias in dB at high frequencies (0.3-0.5 cycles)."""
    rng = np.random.default_rng(SEED)
    w = 2 * np.pi * np.arange(1, n // 2 + 1) / n
    hi0 = w / (2 * np.pi) >= 0.3
    trh = arma_spectrum(w[hi0], ar=PW_AR4)
    paths = [simulate_arma(n, ar=PW_AR4, rng=rng) for _ in range(21)]       # show the path with the median leakage
    lk = [np.mean(10 * np.log10(periodogram(p)[1][hi0] / trh)) for p in paths]
    x = paths[int(np.argsort(lk)[10])]
    w, I = periodogram(x)
    _, Ih = periodogram(x, np.hanning(n))
    mt = multitaper(x, 4)
    mta = multitaper(x, 4, adaptive=True)
    tr = arma_spectrum(w, ar=PW_AR4)
    nu = w / (2 * np.pi)
    db = lambda v: 10 * np.log10(v)
    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.plot(nu, db(I), color=st.Amber, lw=0.6, label='periodogram')
    ax.plot(nu, db(Ih), color=st.Teal, lw=0.6, label='Hann-tapered periodogram')
    ax.plot(nu, db(mt['f']), color=st.MainBlue, lw=1.0, label='multitaper, NW = 4, K = 7')
    ax.plot(nu, db(mta['f']), color=st.Forest, lw=1.3, label='multitaper with adaptive weights')
    ax.plot(nu, db(tr), color=st.IDAred, lw=2, label='true spectrum')
    ax.set_xlabel('frequency (cycles per observation)')
    ax.set_ylabel('dB')
    ax.set_xlim(0, 0.5)
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch11_leakage', save_it)
    hi = nu >= 0.3
    B = {'raw': [], 'hann': [], 'mt': [], 'mta': []}
    for _ in range(reps):
        y = simulate_arma(n, ar=PW_AR4, rng=rng)
        B['raw'].append(np.mean(db(periodogram(y)[1][hi] / tr[hi])))
        B['hann'].append(np.mean(db(periodogram(y, np.hanning(n))[1][hi] / tr[hi])))
        B['mt'].append(np.mean(db(multitaper(y, 4)['f'][hi] / tr[hi])))
        B['mta'].append(np.mean(db(multitaper(y, 4, adaptive=True)['f'][hi] / tr[hi])))
    return dict(range_db=float(db(tr.max() / tr.min())), bias_raw=float(np.mean(B['raw'])),
                bias_hann=float(np.mean(B['hann'])), bias_mt=float(np.mean(B['mt'])), bias_mta=float(np.mean(B['mta'])), reps=reps, n=n)


def fig_dpss(save_it=True, n=512, NW=4, K=10):
    """The first four Slepian tapers and the concentration ratios lambda_k: about 2NW - 1 tapers are well concentrated."""
    v, lam = dpss(n, NW, K)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.0), gridspec_kw=dict(width_ratios=[1.6, 1]))
    for k, c in zip(range(4), [st.MainBlue, st.IDAred, st.Forest, st.Purple]):
        axs[0].plot(v[k], color=c, lw=1.5, label=f'taper k = {k}')
    axs[0].set_xlabel('t')
    axs[0].set_ylabel('$v_t^{(k)}$')
    axs[1].bar(np.arange(K), 1 - lam, color=[st.MainBlue if k < 2 * NW - 1 else st.IDAred for k in range(K)])
    axs[1].set_yscale('log')
    axs[1].set_xlabel('taper k')
    axs[1].set_ylabel('leakage 1 - $\\lambda_k$')
    axs[1].set_xticks(range(K))
    st.legend_outside_bottom(axs[0], ncol=4, y=-0.2)
    plt.tight_layout()
    save('ats_ch11_dpss', save_it)
    return dict(lam=lam.tolist(), n=n, NW=NW)


def fig_mt_mc(save_it=True, n=512, reps=400):
    """Monte Carlo on the sharp AR(2) (peak near 11 periods): mean bias (dB) of five estimators across frequencies and
    the coverage of the nominal 95% chi-square bands of the periodogram (2 df), Daniell (2L df), multitaper (2K df)
    and adaptive multitaper (its equivalent degrees of freedom)."""
    rng = np.random.default_rng(SEED + 1)
    w = 2 * np.pi * np.arange(1, n // 2 + 1) / n
    tr = arma_spectrum(w, ar=AR2_SHARP)
    m, M, nseg, NW = 3, 32, 64, 4
    acc = {k: [] for k in ('periodogram', 'Daniell, L = 7', 'Parzen, M = 32', 'Welch, segments of 64', 'multitaper, K = 7')}
    cov = {k: [] for k in ('periodogram', 'Daniell, L = 7', 'multitaper, K = 7', 'adaptive multitaper')}
    for _ in range(reps):
        x = simulate_arma(n, ar=AR2_SHARP, rng=rng)
        I = periodogram(x)[1]
        Dn = daniell(x, m)[1]
        Pz = lag_window(x, M, 'parzen', omega=w)[1]
        ww, We = welch(x, nseg)
        We = np.interp(w, ww, We)
        mt = multitaper(x, NW)
        mta = multitaper(x, NW, adaptive=True)
        for k, v in zip(acc, (I, Dn, Pz, We, mt['f'])):
            acc[k].append(10 * np.log10(np.maximum(v, 1e-12) / tr))
        for k, v, d in (('periodogram', I, 2), ('Daniell, L = 7', Dn, 2 * (2 * m + 1))):
            cov[k].append((d * v / stats.chi2.ppf(0.975, d) <= tr) & (tr <= d * v / stats.chi2.ppf(0.025, d)))
        cov['multitaper, K = 7'].append((mt['lo'] <= tr) & (tr <= mt['hi']))
        cov['adaptive multitaper'].append((mta['lo'] <= tr) & (tr <= mta['hi']))
    nu = w / (2 * np.pi)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.2))
    cols = [st.Amber, st.Teal, st.Purple, st.Forest, st.MainBlue]
    for (k, v), c in zip(acc.items(), cols):
        axs[0].plot(nu, np.mean(v, axis=0), color=c, lw=1.2, label=k)
    axs[0].axhline(0, color=st.DarkText, lw=0.6)
    axs[0].set_xlabel('frequency (cycles per observation)')
    axs[0].set_ylabel('mean of 10 log$_{10}$(estimate / true) (dB)')
    for k, c in zip(cov, [st.Amber, st.Teal, st.MainBlue, st.IDAred]):
        axs[1].plot(nu, np.mean(cov[k], axis=0), color=c, lw=1.2, label=k if k == 'adaptive multitaper' else '_' + k)
    axs[1].axhline(0.95, color=st.DarkText, ls='--', lw=0.9)
    axs[1].set_xlabel('frequency (cycles per observation)')
    axs[1].set_ylabel('coverage of the nominal 95% band')
    axs[1].set_ylim(0, 1.02)
    st.fig_legend_bottom(fig, ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.12, 1, 1))
    save('ats_ch11_mt_mc', save_it)
    peak = np.abs(nu - 1 / 11.1) < 0.01
    out = {k: dict(bias_all=float(np.mean(v)), bias_peak=float(np.mean(np.array(v)[:, peak])),
                   sd=float(np.mean(np.std(v, axis=0)))) for k, v in acc.items()}
    for k, v in cov.items():
        out.setdefault(k, {}).update(cov_all=float(np.mean(v)), cov_peak=float(np.mean(np.array(v)[:, peak])))
    out['reps'] = reps
    out['n'] = n
    return out


def ip_growth(geo, adj='SCA'):
    return ip(geo, adj).diff().dropna()


def fig_ip_spectrum(save_it=True, NW=4):
    """Multitaper spectra (95% bands) of monthly industrial production growth, Romania and the euro area."""
    out = {}
    fig, ax = plt.subplots(figsize=(11, 4.3))
    for geo in ('RO', 'EA20'):
        y = ip_growth(geo)
        mt = multitaper(y.values, NW)
        per = 2 * np.pi / mt['w']
        ax.plot(per, mt['f'], color=GEO_COL[geo], lw=1.6, label=f'{GEO_LAB[geo]} (multitaper, K = {mt["K"]})')
        ax.fill_between(per, mt['lo'], mt['hi'], color=GEO_COL[geo], alpha=0.15, lw=0, label=f'_95% band {geo}')
        bc = (per >= BC_M[0]) & (per <= BC_M[1])
        out[geo] = dict(n=len(y), start=str(y.index[0].date()), end=str(y.index[-1].date()), sd=float(y.std()),
                        share_bc=float(mt['f'][bc].sum() / mt['f'].sum()), share_short=float(mt['f'][per < 6].sum() / mt['f'].sum()),
                        dof=float(mt['dof'][0]))
    shade_band(ax, *BC_M, label='business-cycle band (18-96 months)')
    ax.set_yscale('log')
    per_axis(ax, 2, 160, [2, 3, 4, 6, 12, 24, 48, 96, 160], 'period (months)')
    ax.set_ylabel('spectral density')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch11_ip_spectrum', save_it)
    return out


def fig_ftest(save_it=True, NW=4, nfft=1200):
    """Thomson's harmonic F test on Romanian industrial production growth, unadjusted and seasonally adjusted:
    p-values by frequency (cycles per year) with the six seasonal harmonics k/12 marked."""
    out = {}
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.0), sharey=True)
    for ax, adj, lab in zip(axs, ('NSA', 'SCA'), ('unadjusted', 'seasonally and calendar adjusted')):
        y = ip_growth('RO', adj)
        r = harmonic_ftest(y.values, NW, nfft=nfft)
        cpy = 12 * r['w'] / (2 * np.pi)
        lp = -np.log10(r['p'])
        ax.plot(cpy, lp, color=st.MainBlue if adj == 'SCA' else st.IDAred, lw=0.8, label=f'{lab}')
        ax.axhline(-np.log10(0.01), color=st.Amber, ls='--', lw=1.2, label='1% level')
        for k in range(1, 7):
            ax.axvline(k, color=st.Forest, ls=':', lw=0.9, label='seasonal harmonics k/12' if k == 1 else '_h')
        hits = []
        for k in range(1, 7):
            i = int(np.argmin(np.abs(cpy - k)))
            hits.append(float(r['p'][i]))
        out[adj] = dict(p=hits, n_sig=int(sum(p < 0.01 for p in hits)), n=len(y), K=r['K'],
                        n_other=int(((r['p'] < 0.01) & (np.min(np.abs(cpy[:, None] - np.arange(1, 7)[None, :]), axis=1) > 0.1)).sum()),
                        n_freq=int(len(cpy)),
                        p_td=float(r['p'][(np.abs(cpy - 4.176) < 0.05)].min()))   # trading-day frequency 0.348 cycles per month
        ax.set_xlabel('frequency (cycles per year)')
        ax.set_xlim(0, 6)
        ax.set_title(lab)
    axs[0].set_ylabel('$-\\log_{10}$ p-value')
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch11_ftest', save_it)
    return out


# =============================================================================
# 3. TWO SERIES
# =============================================================================
def fig_coherence(save_it=True, NW=6):
    """Romania and the euro area, monthly industrial production growth: squared coherence with its 5% null threshold,
    phase (positive: the euro area leads) with two-standard-error bands where coherence is significant, gain."""
    d = pd.concat([ip_growth('EA20'), ip_growth('RO')], axis=1, join='inner').dropna()
    cs = cross_spectrum(d['EA20'].values, d['RO'].values, NW)
    per = 2 * np.pi / cs['w']
    sig = cs['coh'] > cs['thr']
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.0))
    axs[0].plot(per, cs['coh'], color=st.MainBlue, lw=1.6, label='squared coherence')
    axs[0].axhline(cs['thr'], color=st.IDAred, ls='--', lw=1.1, label='5% threshold under no coherence')
    axs[0].set_ylabel('squared coherence')
    ph = np.where(sig, cs['phase'], np.nan)
    axs[1].plot(per, ph, color=st.Forest, lw=1.6, label='phase (where coherence is significant)')
    axs[1].fill_between(per, ph - 2 * cs['se_phase'], ph + 2 * cs['se_phase'], color=st.Forest, alpha=0.2, lw=0,
                        label='$\\pm$ 2 standard errors')
    axs[1].axhline(0, color=st.DarkText, lw=0.6)
    axs[1].set_ylabel('phase (radians)')
    axs[2].plot(per, cs['gain'], color=st.Purple, lw=1.6, label='gain of Romania on the euro area')
    axs[2].set_ylabel('gain')
    for ax in axs:
        shade_band(ax, *BC_M, label='_bc')
        per_axis(ax, 2, 160, [2, 6, 12, 24, 48, 96], 'period (months)')
    st.fig_legend_bottom(fig, ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch11_coherence', save_it)
    bc = (per >= BC_M[0]) & (per <= BC_M[1])
    sh = per < 12
    lead = cs['phase'][bc & sig] / cs['w'][bc & sig]
    return dict(n=len(d), start=str(d.index[0].date()), end=str(d.index[-1].date()), K=cs['K'], thr=cs['thr'],
                coh_bc=float(cs['coh'][bc].mean()), coh_short=float(cs['coh'][sh].mean()),
                share_sig_bc=float(sig[bc].mean()), share_sig_short=float(sig[sh].mean()),
                lead_med=float(np.median(lead)) if len(lead) else float('nan'),
                gain_bc=float(cs['gain'][bc].mean()), gain_short=float(cs['gain'][sh].mean()),
                corr=float(np.corrcoef(d['EA20'], d['RO'])[0, 1]))


def gdp_growth(geo, end='2026-06-30'):
    return gdp(geo, end).diff().dropna()


def fig_dyncorr(save_it=True, NW=3):
    """Dynamic correlation (Croux, Forni and Reichlin 2001) of quarterly GDP growth with the euro area: curves for the
    pre-COVID sample 1995Q2-2019Q4 and band averages (2-6 and 6-32 quarters) for the pre-COVID and the full sample."""
    out = {}
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw=dict(width_ratios=[1.35, 1]))
    for geo in CEE:
        o = {}
        for lab, end in (('pre', '2019-12-31'), ('full', '2026-06-30')):
            d = pd.concat([gdp_growth('EA20', end), gdp_growth(geo, end)], axis=1, join='inner').dropna()
            cs = cross_spectrum(d['EA20'].values, d[geo].values, NW)
            o[lab] = dict(bc=band_dyncorr(cs, 2 * np.pi / 32, 2 * np.pi / 6), short=band_dyncorr(cs, 2 * np.pi / 6, np.pi),
                          corr=float(np.corrcoef(d['EA20'], d[geo])[0, 1]), n=len(d))
            if lab == 'pre':
                per = 2 * np.pi / cs['w']
                axs[0].plot(per, cs['dyncorr'], color=GEO_COL[geo], lw=1.6, label=GEO_LAB[geo])
        out[geo] = o
    shade_band(axs[0], *BC_Q, label='business-cycle band (6-32 quarters)')
    axs[0].axhline(0, color=st.DarkText, lw=0.6)
    per_axis(axs[0], 2, 50, [2, 4, 6, 8, 16, 32, 50], 'period (quarters)')
    axs[0].set_ylabel('dynamic correlation with the euro area')
    xs = np.arange(len(CEE))
    for j, (lab, c, hatch) in enumerate((('pre', st.MainBlue, ''), ('full', st.IDAred, ''))):
        axs[1].bar(xs + (j - 0.5) * 0.38, [out[g][lab]['bc'] for g in CEE], 0.36, color=c,
                   label='6-32 quarters, ' + ('1995-2019' if lab == 'pre' else '1995-2026'))
        axs[1].plot(xs + (j - 0.5) * 0.38, [out[g][lab]['short'] for g in CEE], 'D', color=st.Amber, ms=7,
                    label='2-6 quarters' if j == 0 else '_s')
    axs[1].set_xticks(xs)
    axs[1].set_xticklabels([GEO_LAB[g] for g in CEE])
    axs[1].axhline(0, color=st.DarkText, lw=0.6)
    axs[1].set_ylabel('band dynamic correlation')
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch11_dyncorr', save_it)
    return out


def fig_causality(save_it=True, pmax=12, pmin=3):
    """Euro area and Romania, monthly industrial production growth: Geweke (1982) measures in both directions and the
    Breitung-Candelon (2006) F statistic across frequencies, VAR order by AIC (at least 3, so that the frequency
    restrictions are not equivalent to the full Granger test)."""
    d = pd.concat([ip_growth('EA20'), ip_growth('RO')], axis=1, join='inner').dropna()
    Y = d[['RO', 'EA20']].values                       # series 0 = Romania, series 1 = euro area
    p, _ = var_order(Y, pmax, 'aic')
    p = max(p, pmin)
    om = np.linspace(2 * np.pi / 240, np.pi, 600)
    g = geweke(Y, p, om)
    bc1 = breitung_candelon(Y, p, om, cause=1, target=0)   # EA -> RO
    bc2 = breitung_candelon(Y, p, om, cause=0, target=1)   # RO -> EA
    per = 2 * np.pi / om
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.1))
    axs[0].plot(per, g['1->0'], color=st.MainBlue, lw=1.8, label='euro area $\\to$ Romania')
    axs[0].plot(per, g['0->1'], color=st.IDAred, lw=1.8, label='Romania $\\to$ euro area')
    axs[0].set_ylabel('Geweke measure $M(\\omega)$')
    axs[1].plot(per, bc1['F'], color=st.MainBlue, lw=1.8)
    axs[1].plot(per, bc2['F'], color=st.IDAred, lw=1.8)
    axs[1].axhline(bc1['crit'], color=st.Amber, ls='--', lw=1.2, label='5% critical value F(2, T - 2p - 1)')
    axs[1].set_ylabel('Breitung-Candelon F statistic')
    for ax in axs:
        shade_band(ax, *BC_M, label='_bc')
        per_axis(ax, 2, 240, [2, 4, 6, 12, 24, 48, 96, 240], 'period (months)')
    st.fig_legend_bottom(fig, ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.1, 1, 1))
    save('ats_ch11_causality', save_it)
    rej = per[bc1['p'] < 0.05]
    rej2 = per[bc2['p'] < 0.05]
    bc = (per >= BC_M[0]) & (per <= BC_M[1])
    return dict(p=int(p), n=len(d), F_ea_ro=g['F1->0'], F_ro_ea=g['F0->1'],
                int_ea_ro=float(np.trapezoid(g['1->0'], om) / np.pi), M_bc=float(g['1->0'][bc].mean()),
                M_short=float(g['1->0'][per < 6].mean()), M0=float(g['1->0'][0]),
                rej_min=float(rej.min()) if len(rej) else None, rej_max=float(rej.max()) if len(rej) else None,
                share_rej=float((bc1['p'] < 0.05).mean()), share_rej2=float((bc2['p'] < 0.05).mean()),
                share_rej_bc=float((bc1['p'][bc] < 0.05).mean()), crit=bc1['crit'],
                Fmax=float(bc1['F'].max()), per_Fmax=float(per[np.argmax(bc1['F'])]))


# =============================================================================
# 4. FILTERS
# =============================================================================
def cf_central_weights(n=126, low=6, high=32):
    """Weights of the Christiano-Fitzgerald random-walk filter at the middle of a sample of n quarters, obtained by
    filtering unit vectors (the filter is linear but asymmetric and time-varying)."""
    from statsmodels.tsa.filters.cf_filter import cffilter
    E = np.eye(n)
    Wm = np.column_stack([cffilter(E[:, j], low, high, drift=False)[0] for j in range(n)])
    return Wm[n // 2], Wm


def fig_gains(save_it=True):
    """Gains (level to cycle) of the ideal band-pass filter, Baxter-King (6, 32, K = 12), Christiano-Fitzgerald (middle
    of a 126-quarter sample), HP (lambda = 1600) and Hamilton (h = 8, p = 4: random-walk weights and the weights
    estimated on Romanian GDP)."""
    om = np.linspace(2 * np.pi / 120, np.pi, 3000)
    per = 2 * np.pi / om
    a = bk_weights(6, 32, 12)
    wcf, _ = cf_central_weights()
    n = len(wcf)
    lags = n // 2 - np.arange(n)          # y_t weight index j -> lag (t_mid - j)
    _, b = hamilton_filter(gdp('RO').values, 8, 4)
    curves = {'ideal band-pass (6-32)': ideal_gain(om), 'Baxter-King (K = 12)': filter_gain(a, om),
              'Christiano-Fitzgerald (mid-sample)': np.abs(np.exp(-1j * np.outer(om, lags)) @ wcf),
              'HP cycle, $\\lambda$ = 1600': hp_gain(om, 1600), 'Hamilton, random-walk weights': hamilton_gain(om, [1, 0, 0, 0]),
              'Hamilton, estimated on Romanian GDP': hamilton_gain(om, b[1:])}
    cols = [st.Amber, st.MainBlue, st.Teal, st.IDAred, st.Forest, st.Purple]
    sty = ['-', '-', '-', '-', '--', '-']
    fig, ax = plt.subplots(figsize=(11, 4.4))
    for (k, v), c, s in zip(curves.items(), cols, sty):
        ax.plot(per, v, color=c, ls=s, lw=1.7 if k.startswith('ideal') is False else 1.2, label=k)
    per_axis(ax, 2, 120, [2, 4, 6, 8, 12, 16, 32, 64, 120], 'period (quarters)')
    ax.set_ylabel('gain')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch11_gains', save_it)
    at = lambda v, P: float(np.interp(P, per[::-1], v[::-1]))
    hg = curves['Hamilton, random-walk weights']
    he = curves['Hamilton, estimated on Romanian GDP']
    return dict(hp32=at(curves['HP cycle, $\\lambda$ = 1600'], 32), hp40=at(curves['HP cycle, $\\lambda$ = 1600'], 40),
                hp60=at(curves['HP cycle, $\\lambda$ = 1600'], 60), hp6=at(curves['HP cycle, $\\lambda$ = 1600'], 6),
                bk_peak=float(filter_gain(a, om).max()), bk_40=at(curves['Baxter-King (K = 12)'], 40),
                bk_4=at(curves['Baxter-King (K = 12)'], 4), ham16=at(hg, 16), ham8=at(hg, 8), ham_e16=at(he, 16),
                ham_e8=at(he, 8), ham_b=b.tolist(), bk_a0=float(a[12]), bk_sum=float(a.sum()))


def fig_cogley_nason(save_it=True, n=200, reps=500):
    """The HP cycle of a random walk: theoretical spectrum H(w)^2 / (2 (1 - cos w)) (Cogley and Nason 1995) and the
    Monte Carlo average periodogram of HP-filtered random walks (n = 200 quarters)."""
    rng = np.random.default_rng(SEED)
    om = np.linspace(2 * np.pi / 200, np.pi, 4000)
    th = hp_gain(om) ** 2 / (2 * (1 - np.cos(om))) / (2 * np.pi)
    P = []
    for _ in range(reps):
        c, _ = hp_filter(np.cumsum(rng.standard_normal(n)))
        P.append(periodogram(c)[1])
    w = 2 * np.pi * np.arange(1, n // 2 + 1) / n
    Pm = np.mean(P, axis=0)
    u = np.sqrt(3 / (4 * 1600))
    p_th = 2 * np.pi / np.arccos(1 - u)
    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    ax.plot(2 * np.pi / om, th, color=st.IDAred, lw=2, label='theory: HP cycle of a random walk')
    ax.plot(2 * np.pi / w, Pm, 'o', color=st.MainBlue, ms=4, label=f'Monte Carlo mean periodogram ({reps} paths of {n} quarters)')
    ax.axvline(p_th, color=st.Amber, ls='--', lw=1.4, label=f'peak at {p_th:.1f} quarters')
    shade_band(ax, *BC_Q, label='business-cycle band (6-32 quarters)')
    per_axis(ax, 2, 200, [2, 4, 8, 16, 32, 64, 128, 200], 'period (quarters)')
    ax.set_ylabel('spectral density')
    st.legend_outside_bottom(ax, ncol=2, y=-0.2)
    save('ats_ch11_cogley_nason', save_it)
    i = np.argmax(Pm)
    return dict(p_th=float(p_th), p_mc=float(2 * np.pi / w[i]), n=n, reps=reps, u=float(u))


def ro_cycles():
    from statsmodels.tsa.filters.cf_filter import cffilter
    y = gdp('RO')
    c = pd.DataFrame(index=y.index)
    c['HP'] = hp_filter(y.values, 1600)[0]
    c['Baxter-King'] = bk_filter(y.values, 6, 32, 12)
    c['Christiano-Fitzgerald'] = cffilter(y.values, 6, 32, drift=True)[0]
    c['Hamilton'] = hamilton_filter(y.values, 8, 4)[0]
    return y, c


def fig_ro_cycles(save_it=True):
    """Romanian real GDP, 1995Q1-2026Q2: cycles (in % of trend) of HP, Baxter-King, Christiano-Fitzgerald and Hamilton."""
    y, c = ro_cycles()
    fig, ax = plt.subplots(figsize=(11.5, 4.3))
    for k, col in zip(c.columns, [st.IDAred, st.MainBlue, st.Teal, st.Forest]):
        ax.plot(c.index, c[k], color=col, lw=1.6, label=k)
    ax.axhline(0, color=st.DarkText, lw=0.6)
    ax.set_ylabel('% deviation from trend')
    st.legend_outside_bottom(ax, ncol=4, y=-0.14)
    save('ats_ch11_ro_cycles', save_it)
    cc = c.dropna()
    q = lambda d: f'{d.year}Q{(d.month - 1) // 3 + 1}'
    return dict(sd={k: float(c[k].std()) for k in c}, corr={f'{a}|{b}': float(cc[a].corr(cc[b])) for a in c for b in c if a < b},
                last={k: float(c[k].dropna().iloc[-1]) for k in c}, last_q={k: q(c[k].dropna().index[-1]) for k in c},
                min09={k: float(c[k].loc['2008-01-01':'2011-12-31'].min()) for k in c},
                minq09={k: q(c[k].loc['2008-01-01':'2011-12-31'].idxmin()) for k in c},
                max08={k: float(c[k].loc['2006-01-01':'2009-12-31'].max()) for k in c},
                start=q(y.index[0]), end=q(y.index[-1]), n=len(y))


def fig_endpoint(save_it=True, start=40):
    """Real-time (one-sided) and final (two-sided) HP cycles of Romanian GDP, and the real-time Hamilton cycle (the
    regression re-estimated on the data available at each date) against its final version."""
    y = gdp('RO')
    Yv = y.values
    hp_final = hp_filter(Yv, 1600)[0]
    hp_rt = hp_one_sided(Yv, 1600, start)
    ham_final = hamilton_filter(Yv, 8, 4)[0]
    ham_rt = np.full(len(Yv), np.nan)
    for t in range(start, len(Yv) + 1):
        ham_rt[t - 1] = hamilton_filter(Yv[:t], 8, 4)[0][-1]
    df = pd.DataFrame(dict(hp_final=hp_final, hp_rt=hp_rt, ham_final=ham_final, ham_rt=ham_rt), index=y.index)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0), sharey=True)
    axs[0].plot(df.index, df['hp_final'], color=st.IDAred, lw=1.8, label='final (two-sided)')
    axs[0].plot(df.index, df['hp_rt'], color=st.MainBlue, lw=1.4, ls='--', label='real time (one-sided)')
    axs[0].set_title('HP filter, $\\lambda$ = 1600')
    axs[1].plot(df.index, df['ham_final'], color=st.IDAred, lw=1.8)
    axs[1].plot(df.index, df['ham_rt'], color=st.MainBlue, lw=1.4, ls='--')
    axs[1].set_title('Hamilton filter, h = 8, p = 4')
    for ax in axs:
        ax.axhline(0, color=st.DarkText, lw=0.6)
    axs[0].set_ylabel('% deviation from trend')
    st.fig_legend_bottom(fig, ncol=2, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch11_endpoint', save_it)
    d = df.dropna()
    r = lambda a, b: float(np.sqrt(np.mean((d[a] - d[b]) ** 2)))
    return dict(rms_hp=r('hp_final', 'hp_rt'), rms_ham=r('ham_final', 'ham_rt'),
                corr_hp=float(d['hp_final'].corr(d['hp_rt'])), corr_ham=float(d['ham_final'].corr(d['ham_rt'])),
                sign_hp=float((np.sign(d['hp_final']) != np.sign(d['hp_rt'])).mean()),
                sign_ham=float((np.sign(d['ham_final']) != np.sign(d['ham_rt'])).mean()),
                sd_hp=float(d['hp_final'].std()), sd_ham=float(d['ham_final'].std()), n=len(d),
                start=f'{d.index[0].year}Q{(d.index[0].month - 1) // 3 + 1}')


def fig_sync(save_it=True, win=20):
    """Baxter-King cycles of Romania and the euro area and their rolling 20-quarter correlation; Harding-Pagan
    concordance of the phases."""
    c = pd.DataFrame({g: bk_filter(gdp(g).values, 6, 32, 12) for g in ('RO', 'EA20')}, index=gdp('RO').index).dropna()
    roll = c['RO'].rolling(win).corr(c['EA20'])
    fig, axs = plt.subplots(2, 1, figsize=(11.5, 5.4), sharex=True, gridspec_kw=dict(height_ratios=[1.4, 1]))
    axs[0].plot(c.index, c['RO'], color=st.IDAred, lw=1.7, label='Romania, Baxter-King cycle')
    axs[0].plot(c.index, c['EA20'], color=st.MainBlue, lw=1.7, label='euro area, Baxter-King cycle')
    axs[0].axhline(0, color=st.DarkText, lw=0.6)
    axs[0].set_ylabel('% of trend')
    axs[1].plot(roll.index, roll, color=st.Forest, lw=1.8, label=f'rolling {win}-quarter correlation')
    axs[1].axhline(0, color=st.DarkText, lw=0.6)
    axs[1].set_ylim(-1, 1)
    axs[1].set_ylabel('correlation')
    st.fig_legend_bottom(fig, ncol=3, y=0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch11_sync', save_it)
    sub = lambda a, b: float(c.loc[a:b, 'RO'].corr(c.loc[a:b, 'EA20']))
    C, C0 = concordance(c['RO'], c['EA20'])
    return dict(corr=float(c['RO'].corr(c['EA20'])), c_pre=sub('1995-01-01', '2007-12-31'), c_gfc=sub('2008-01-01', '2012-12-31'),
                c_post=sub('2013-01-01', '2019-12-31'), c_cov=sub('2020-01-01', '2026-12-31'), conc=C, conc0=C0,
                roll_min=float(roll.min()), roll_min_q=f'{roll.idxmin().year}Q{(roll.idxmin().month - 1) // 3 + 1}',
                start=f'{c.index[0].year}Q{(c.index[0].month - 1) // 3 + 1}', end=f'{c.index[-1].year}Q{(c.index[-1].month - 1) // 3 + 1}',
                sd_ro=float(c['RO'].std()), sd_ea=float(c['EA20'].std()))


# =============================================================================
# 5. NONSTATIONARY SPECTRA
# =============================================================================
def tvar2(n=2048, r=0.95, p0=20, p1=5, seed=SEED):
    """x_t = 2 r cos(theta_t) x_{t-1} - r^2 x_{t-2} + e_t with the peak period moving from p0 to p1 (log-linearly)."""
    rng = np.random.default_rng(seed)
    per = p0 * (p1 / p0) ** (np.arange(n) / (n - 1))
    th = 2 * np.pi / per
    x = np.zeros(n + 200)
    e = rng.standard_normal(n + 200)
    a1 = np.r_[np.full(200, 2 * r * np.cos(th[0])), 2 * r * np.cos(th)]
    for t in range(2, n + 200):
        x[t] = a1[t] * x[t - 1] - r ** 2 * x[t - 2] + e[t]
    return x[200:], a1[200:], per


def fig_spectrogram(save_it=True, n=2048, win=256, step=16, NW=3):
    """Time-varying AR(2): the true local spectrum f(u, w) and the short-time multitaper estimate (windows of 256)."""
    x, a1, per = tvar2(n)
    r = 0.95
    nu = np.linspace(0.005, 0.5, 200)
    true = np.array([arma_spectrum(2 * np.pi * nu, ar=(a, -r ** 2)) for a in a1[::step]]).T
    cent, est = [], []
    for s in range(0, n - win + 1, step):
        mt = multitaper(x[s:s + win], NW)
        est.append(np.interp(nu, mt['w'] / (2 * np.pi), mt['f']))
        cent.append(s + win // 2)
    est = np.array(est).T
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.1), sharey=True, layout='constrained')
    vmin, vmax = np.log10(true).min(), np.log10(true).max()
    axs[0].imshow(np.log10(true), aspect='auto', origin='lower', extent=(0, n, nu[0], nu[-1]), cmap='viridis', vmin=vmin, vmax=vmax)
    im = axs[1].imshow(np.log10(est), aspect='auto', origin='lower', extent=(cent[0], cent[-1], nu[0], nu[-1]), cmap='viridis', vmin=vmin, vmax=vmax)
    axs[0].plot(np.arange(n), 1 / per, color=st.IDAred, lw=1.2, ls='--', label='frequency of the AR(2) peak')
    axs[1].plot(np.arange(n), 1 / per, color=st.IDAred, lw=1.2, ls='--')
    axs[0].set_title('true local spectrum')
    axs[1].set_title(f'short-time multitaper, window {win}, NW = {NW}')
    axs[0].set_ylabel('frequency (cycles per observation)')
    for ax in axs:
        ax.set_xlabel('t')
        ax.set_ylim(0, 0.3)
    cb = fig.colorbar(im, ax=axs, shrink=0.85, pad=0.01)
    cb.set_label('$\\log_{10}$ spectral density')
    st.fig_legend_bottom(fig, ncol=1, y=0.0)
    save('ats_ch11_spectrogram', save_it)
    return dict(n=n, win=win, NW=NW, res=2 * NW / win, p0=float(per[0]), p1=float(per[-1]))


# =============================================================================
# 6. WAVELETS: MODWT, MRA, VARIANCE AND CORRELATION BY SCALE
# =============================================================================
def fig_wavelets(save_it=True, J=5, n=1024):
    """Squared gains of the MODWT LA(8) level-j wavelet filters (octave bands [1/2^{j+1}, 1/2^j]) and the Morlet
    wavelet (w0 = 6) in time."""
    g, h = wavelet_filters('sym4')
    G = _transfer(g / np.sqrt(2), n)
    H = _transfer(h / np.sqrt(2), n)
    k = np.arange(n)
    f = k / n
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw=dict(width_ratios=[1.4, 1]))
    Gp = np.ones(n, complex)
    cols = [st.MainBlue, st.IDAred, st.Forest, st.Purple, st.Orange]
    for j in range(1, J + 1):
        idx = (k * 2 ** (j - 1)) % n
        Hj = H[idx] * Gp
        Gp = Gp * G[idx]
        m = f <= 0.5
        axs[0].plot(f[m], np.abs(Hj[m]) ** 2, color=cols[j - 1], lw=1.6, label=f'level {j}: periods {2 ** j}-{2 ** (j + 1)}')
    axs[0].set_xscale('log')
    axs[0].set_xlim(1 / 128, 0.5)
    axs[0].set_xlabel('frequency (cycles per observation)')
    axs[0].set_ylabel('squared gain')
    t = np.linspace(-4, 4, 800)
    psi = np.pi ** -0.25 * np.exp(1j * 6 * t) * np.exp(-t ** 2 / 2)
    axs[1].plot(t, psi.real, color=st.Teal, lw=1.6, label='Morlet, real part')
    axs[1].plot(t, psi.imag, color=st.Amber, lw=1.4, ls='--', label='Morlet, imaginary part')
    axs[1].plot(t, np.abs(psi), color=st.DarkText, lw=1.2, label='modulus')
    axs[1].set_xlabel('time (in units of the scale s)')
    st.fig_legend_bottom(fig, ncol=4, y=0.0)
    plt.tight_layout(rect=(0, 0.12, 1, 1))
    save('ats_ch11_wavelets', save_it)
    return dict(L=len(g), sumg=float(g.sum()), sumh=float(h.sum()))


def bet_daily():
    return (100 * np.log(load_close('bet', start='2000-01-01', end=END)).diff().dropna()).rename('bet')


def fig_mra(save_it=True, J=6):
    """MODWT multiresolution analysis (LA(8), J = 6) of the daily BET returns: details D1, D2, D4, D6 and smooth S6;
    energy share of each level (wavelet variance decomposition) against white noise."""
    y = bet_daily()
    D, S = mra(y.values, J)
    m = modwt(y.values, J)
    E = (y.values - y.values.mean()) ** 2
    share = [(m['W'][j] ** 2).sum() / ((m['W'] ** 2).sum() + (m['V'] ** 2).sum()) for j in range(J)]
    fig, axs = plt.subplots(3, 2, figsize=(12, 5.6), sharex=True)
    axs = axs.T.ravel()
    axs[0].plot(y.index, y.values, color=st.MainBlue, lw=0.5, label='BET daily returns (%)')
    for ax, (lab, v), c in zip(axs[1:], [('D1 (2-4 days)', D[0]), ('D2 (4-8 days)', D[1]), ('D4 (16-32 days)', D[3]),
                                         ('D6 (64-128 days)', D[5]), ('S6 (> 128 days)', S)],
                               [st.IDAred, st.Orange, st.Forest, st.Purple, st.Teal]):
        ax.plot(y.index, v, color=c, lw=0.6 if 'D1' in lab or 'D2' in lab else 1.0, label=lab)
    from matplotlib.ticker import MaxNLocator
    for ax in axs:
        ax.set_title(ax.get_lines()[0].get_label(), loc='left', pad=2)
        ax.yaxis.set_major_locator(MaxNLocator(3))
    plt.tight_layout()
    save('ats_ch11_mra', save_it)
    return dict(n=len(y), share=[float(s) for s in share], err=float(np.abs(D.sum(0) + S - y.values).max()),
                start=str(y.index[0].date()), end=str(y.index[-1].date()))


def fig_wvar(save_it=True, J=8):
    """Wavelet variance by level of daily returns (BET, DAX, S&P 500) with 95% intervals; the dashed lines show
    white noise with the same level-1 variance (variance halving at each level)."""
    out = {}
    fig, ax = plt.subplots(figsize=(10.5, 4.3))
    for nm, lab in (('bet', 'BET'), ('dax', 'DAX'), ('sp500', 'S&P 500')):
        y = 100 * np.log(load_close(nm, start='2000-01-01', end=END)).diff().dropna()
        wv = wavelet_variance(y.values, J)
        lev = np.array([d['level'] for d in wv])
        v = np.array([d['var'] for d in wv])
        lo = np.array([d['lo'] for d in wv])
        hi = np.array([d['hi'] for d in wv])
        c = st.COL[nm]
        ax.plot(lev, v, 'o-', color=c, lw=1.6, label=lab)
        ax.fill_between(lev, lo, hi, color=c, alpha=0.15, lw=0)
        ax.plot(lev, v[0] / 2 ** (lev - 1), ls='--', color=c, lw=0.9, label=f'_wn {lab}')
        out[nm] = dict(var=v.tolist(), ratio=(v * 2 ** (lev - 1) / v[0]).tolist(), lo=lo.tolist(), hi=hi.tolist(), n=len(y))
    ax.set_yscale('log')
    ax.set_xticks(range(1, J + 1))
    ax.set_xticklabels([f'{j}\n{2 ** j}-{2 ** (j + 1)}' for j in range(1, J + 1)])
    ax.set_xlabel('level j (periods in trading days)')
    ax.set_ylabel('wavelet variance')
    ax.plot([], [], ls='--', color=st.DarkText, lw=0.9, label='white noise with the same level-1 variance')
    st.legend_outside_bottom(ax, ncol=4, y=-0.3)
    save('ats_ch11_wvar', save_it)
    return out


def fig_wcorr(save_it=True, J=8):
    """Wavelet correlation by level of daily returns on common trading days: BET-DAX, BET-S&P 500, DAX-S&P 500
    (left) and BET-DAX in 2000-2012 and 2013-2026 (right), 95% Fisher-z intervals; BET beta on the DAX by level."""
    R = daily_common(['bet', 'dax', 'sp500'])
    out = {}
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.2), sharey=True)
    lev = np.arange(1, J + 1)
    for (a, b, lab, c) in (('bet', 'dax', 'BET-DAX', st.IDAred), ('bet', 'sp500', 'BET-S&P 500', st.MainBlue),
                           ('dax', 'sp500', 'DAX-S&P 500', st.Teal)):
        wc = wavelet_corr(R[b].values, R[a].values, J)
        r = np.array([d['r'] for d in wc])
        axs[0].plot(lev, r, 'o-', color=c, lw=1.6, label=lab)
        axs[0].fill_between(lev, [d['lo'] for d in wc], [d['hi'] for d in wc], color=c, alpha=0.15, lw=0)
        out[f'{a}_{b}'] = dict(r=r.tolist(), lo=[d['lo'] for d in wc], hi=[d['hi'] for d in wc], beta=[d['beta'] for d in wc],
                               corr=float(R[a].corr(R[b])))
    for (s, e, lab, c) in (('2000-01-01', '2012-12-31', 'BET-DAX, 2000-2012', st.Amber), ('2013-01-01', END, 'BET-DAX, 2013-2026', st.Forest)):
        Rs = R.loc[s:e]
        wc = wavelet_corr(Rs['dax'].values, Rs['bet'].values, J)
        r = np.array([d['r'] for d in wc])
        axs[1].plot(lev, r, 'o-', color=c, lw=1.6, label=lab)
        axs[1].fill_between(lev, [d['lo'] for d in wc], [d['hi'] for d in wc], color=c, alpha=0.15, lw=0)
        out['bet_dax_' + s[:4]] = dict(r=r.tolist(), lo=[d['lo'] for d in wc], hi=[d['hi'] for d in wc], n=len(Rs))
    for ax in axs:
        ax.set_xticks(lev)
        ax.set_xticklabels([f'{j}\n{2 ** j}-{2 ** (j + 1)}' for j in lev])
        ax.set_xlabel('level j (periods in trading days)')
        ax.set_ylim(0, 1)
    axs[0].set_ylabel('wavelet correlation')
    st.fig_legend_bottom(fig, ncol=5, y=0.0)
    plt.tight_layout(rect=(0, 0.08, 1, 1))
    save('ats_ch11_wcorr', save_it)
    out['n'] = len(R)
    return out


# =============================================================================
# 7. CONTINUOUS WAVELETS AND WAVELET COHERENCE
# =============================================================================
def year_axis(n, idx):
    """Positions and labels of every fifth year on an index of dates."""
    yrs = sorted({d.year for d in idx if d.year % 5 == 0})
    pos = [int(np.argmax(idx >= pd.Timestamp(f'{y}-01-01'))) for y in yrs]
    return pos, [str(y) for y in yrs]


def plot_tf(ax, Z, c, idx, levels, cmap='viridis', sig=None, sig_level=1.0, phase=None, arrows_where=None):
    """Time-period plot with log2 period axis, the cone of influence hatched and optional significance contours
    and phase arrows (right: in phase; left: anti-phase; up: the first series leads)."""
    n = Z.shape[1]
    t = np.arange(n)
    lp = np.log2(c['period'])
    cf = ax.contourf(t, lp, Z, levels=levels, cmap=cmap, extend='both')
    if sig is not None:
        ax.contour(t, lp, sig, levels=[sig_level], colors=[st.DarkText], linewidths=1.0)
    coi = np.log2(np.maximum(c['coi'], c['period'][0]))
    ax.fill_between(t, coi, lp[-1], facecolor='white', alpha=0.45, hatch='xx', edgecolor=st.DarkText, lw=0)
    if phase is not None:
        step_t = max(n // 45, 1)
        step_s = max(len(lp) // 14, 1)
        T, S = np.meshgrid(t[::step_t], np.arange(len(lp))[::step_s])
        ph = phase[::step_s, ::step_t]
        m = arrows_where[::step_s, ::step_t] if arrows_where is not None else np.ones_like(ph, bool)
        ax.quiver(T[m], lp[S[m]], np.cos(ph[m]), np.sin(ph[m]), color=st.DarkText, scale=38, width=0.0025,
                  headwidth=4, headlength=4)
    ax.set_ylim(lp[-1], lp[0])
    ticks = [p for p in (2, 4, 8, 16, 32, 64, 128, 256) if lp[0] <= np.log2(p) <= lp[-1]]
    ax.set_yticks(np.log2(ticks))
    ax.set_yticklabels([str(p) for p in ticks])
    pos, lab = year_axis(n, idx)
    ax.set_xticks(pos)
    ax.set_xticklabels(lab)
    return cf


def fig_cwt_bet(save_it=True):
    """Morlet wavelet power of weekly BET returns (standardised), 2000-2026, with the 5% red-noise contour, the cone
    of influence, and the global wavelet spectrum."""
    y = weekly_returns('bet')
    c = cwt(y.values, dj=1 / 12, pmax=256)
    P = np.abs(c['W']) ** 2
    sig = red_noise_signif(y.values, c)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw=dict(width_ratios=[4, 1]), sharey=True)
    cf = plot_tf(axs[0], np.log2(P), c, y.index, np.linspace(-4, 5, 19), sig=P / sig[:, None])
    axs[0].set_ylabel('period (weeks)')
    gws = P.mean(axis=1)
    a = ar1_coef(y.values)
    Pk = sig * 2 / stats.chi2.ppf(0.95, 2)                               # red-noise spectrum at each scale
    dof = 2 * np.sqrt(1 + (len(y) / (2.32 * c['scales'])) ** 2)          # Torrence-Compo eq. 23, Morlet gamma = 2.32
    lp = np.log2(c['period'])
    axs[1].plot(gws, lp, color=st.MainBlue, lw=1.8, label='global wavelet spectrum')
    axs[1].plot(Pk * stats.chi2.ppf(0.95, dof) / dof, lp, color=st.IDAred, ls='--', lw=1.2, label='5% red noise')
    axs[1].set_xlabel('power')
    cb = fig.colorbar(cf, ax=axs[0], pad=0.01)
    cb.set_label('$\\log_2$ power')
    st.fig_legend_bottom(fig, ncol=2, y=0.0)
    save('ats_ch11_cwt_bet', save_it)
    mask = coi_mask(c)
    Pm = np.where(mask, P, -np.inf)
    i, j = np.unravel_index(np.argmax(Pm), P.shape)
    big = (P / sig[:, None] > 1) & mask
    return dict(ar1=float(a), max_date=str(y.index[j].date()), max_per=float(c['period'][i]), n=len(y),
                share_sig=float(big.mean() / mask.mean()), share_sig_short=float(big[c['period'] < 16].mean()),
                gws_peak=float(c['period'][np.argmax(gws)]))


def wtc_pair(x, y, idx, name, title, reps=500, pmax=256, dj=1 / 12, lab_unit='weeks', bands=None, save_it=True):
    r = wtc_montecarlo(x, y, dj=dj, pmax=pmax, reps=reps, seed=SEED)
    b = r['base']
    sig = b['R2'] / r['thr'][:, None]
    fig, ax = plt.subplots(figsize=(12, 4.4))
    cf = plot_tf(ax, b['R2'], b['cwt'], idx, np.linspace(0, 1, 11), cmap='YlOrRd', sig=sig, phase=b['phase'],
                 arrows_where=(sig > 1) & r['mask'])
    ax.set_ylabel(f'period ({lab_unit})')
    ax.set_title(title)
    cb = fig.colorbar(cf, ax=ax, pad=0.01)
    cb.set_label('squared wavelet coherence')
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    hd = [Line2D([], [], color=st.DarkText, lw=1), Patch(facecolor='white', hatch='xx', edgecolor=st.DarkText),
          Line2D([], [], color=st.DarkText, marker='$\\rightarrow$', ls='', ms=14)]
    ax.legend(hd, [f'5% significance (Monte Carlo, {reps} AR(1) pairs)', 'cone of influence',
                   'phase: right in phase, up: first series leads'], loc='upper center', bbox_to_anchor=(0.5, -0.13),
              ncol=3, frameon=False)
    save(name, save_it)
    per = b['period']
    out = dict(share_obs=r['share_obs'], null_mean=float(r['share_null'].mean()), null_q95=float(np.quantile(r['share_null'], 0.95)),
               null_max=float(r['share_null'].max()), ax=r['ax'], ay=r['ay'], n=len(x), reps=reps,
               null_any=float((r['share_null'] > 0).mean()), reps_check=r['reps_check'])
    sigm = (sig > 1) & r['mask']
    out['phase_sig'] = float(np.angle(np.mean(np.exp(1j * b['phase'][sigm])))) if sigm.any() else float('nan')
    for k, (p0, p1, d0, d1) in (bands or {}).items():
        rows = (per >= p0) & (per <= p1)
        cols = (idx >= pd.Timestamp(d0)) & (idx <= pd.Timestamp(d1))
        sub = b['R2'][np.ix_(rows, cols)]
        out[k] = float(sub.mean())
        out[k + '_ph'] = float(np.angle(np.mean(np.exp(1j * b['phase'][np.ix_(rows, cols)]))))
    return out, r


def fig_wtc_bet_dax(save_it=True, reps=500):
    d = pd.concat([weekly_returns('bet'), weekly_returns('dax')], axis=1, join='inner').dropna()
    out, r = wtc_pair(d['bet'].values, d['dax'].values, d.index, 'ats_ch11_wtc_bet_dax', 'BET and DAX, weekly returns',
                      reps=reps, bands={'gfc': (8, 64, '2008-01-01', '2009-12-31'), 'calm': (8, 64, '2014-01-01', '2019-12-31'),
                                        'early': (8, 64, '2000-01-01', '2006-12-31'), 'covid': (8, 64, '2020-01-01', '2021-06-30'),
                                        'short_all': (2, 8, '2000-01-01', '2026-12-31')}, save_it=save_it)
    _MEM['wtc_bet_dax'] = r
    out['start'] = str(d.index[0].date())
    out['end'] = str(d.index[-1].date())
    return out


def fig_wtc_bet_spx(save_it=True, reps=500):
    d = pd.concat([weekly_returns('bet'), weekly_returns('sp500')], axis=1, join='inner').dropna()
    out, _ = wtc_pair(d['bet'].values, d['sp500'].values, d.index, 'ats_ch11_wtc_bet_spx', 'BET and S&P 500, weekly returns',
                      reps=reps, bands={'gfc': (8, 64, '2008-01-01', '2009-12-31'), 'calm': (8, 64, '2014-01-01', '2019-12-31'),
                                        'early': (8, 64, '2000-01-01', '2006-12-31'), 'covid': (8, 64, '2020-01-01', '2021-06-30'),
                                        'short_all': (2, 8, '2000-01-01', '2026-12-31')}, save_it=save_it)
    return out


def fig_wtc_oil(save_it=True, reps=500):
    d = pd.concat([brent_weekly(), weekly_returns('sp500')], axis=1, join='inner').dropna()
    out, _ = wtc_pair(d['brent'].values, d['sp500'].values, d.index, 'ats_ch11_wtc_oil', 'Brent crude oil and S&P 500, weekly returns',
                      reps=reps, bands={'early': (16, 128, '2000-01-01', '2007-06-30'), 'gfc': (16, 128, '2008-06-01', '2010-12-31'),
                                        'covid': (8, 64, '2020-01-01', '2021-12-31'), 'war': (8, 64, '2022-01-01', '2023-12-31'),
                                        'calm': (16, 128, '2012-01-01', '2019-12-31')}, save_it=save_it)
    out['start'] = str(d.index[0].date())
    out['end'] = str(d.index[-1].date())
    return out


def fig_wtc_infl(save_it=True, reps=500):
    """Wavelet coherence of annual HICP inflation, Romania and Poland with the euro area, monthly 2001-2026."""
    out = {}
    ea = hicp('EA')
    for geo in ('RO', 'PL'):
        d = pd.concat([hicp(geo), ea], axis=1, join='inner').dropna()
        o, _ = wtc_pair(d[geo].values, d['EA'].values, d.index, f'ats_ch11_wtc_infl_{geo.lower()}',
                        f'Annual HICP inflation: {GEO_LAB[geo]} and the euro area', reps=reps, pmax=128, lab_unit='months',
                        bands={'post': (24, 64, '2015-01-01', '2026-12-31'), 'pre': (24, 64, '2002-01-01', '2012-12-31'),
                               'surge': (12, 48, '2021-01-01', '2024-12-31')}, save_it=save_it)
        o['start'] = str(d.index[0].date())
        o['end'] = str(d.index[-1].date())
        o['corr'] = float(d[geo].corr(d['EA']))
        out[geo] = o
    return out


def fig_ai_case(save_it=True):
    """Areawise check: the share of the reliable time-period area of the BET-DAX coherence that is pointwise
    significant at 5%, against its distribution over the Monte Carlo pairs of independent AR(1) series."""
    r = _MEM.get('wtc_bet_dax')
    if r is None:
        d = pd.concat([weekly_returns('bet'), weekly_returns('dax')], axis=1, join='inner').dropna()
        r = wtc_montecarlo(d['bet'].values, d['dax'].values, dj=1 / 12, pmax=256, reps=500, seed=SEED)
    sn = r['share_null']
    fig, ax = plt.subplots(figsize=(10.5, 4.0))
    ax.hist(100 * sn, bins=30, color=st.MainBlue, alpha=0.8, label=f'independent AR(1) pairs ({len(sn)} new replications)')
    ax.axvline(100 * np.quantile(sn, 0.95), color=st.Amber, ls='--', lw=1.6, label='95th percentile under the null')
    ax.axvline(100 * r['share_obs'], color=st.IDAred, lw=2.2, label='BET-DAX')
    ax.set_xlabel('% of the reliable area that is pointwise significant at 5%')
    ax.set_ylabel('replications')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch11_ai_case', save_it)
    return dict(obs=float(r['share_obs']), mean=float(sn.mean()), q95=float(np.quantile(sn, 0.95)), max=float(sn.max()),
                any=float((sn > 0).mean()), over10=float((sn > 0.10).mean()), reps=int(len(sn)))


if __name__ == '__main__':
    st.apply()
    N = {}
    only = sys.argv[1:]
    path = os.path.join(HERE, 'ch11_numbers.json')
    if os.path.exists(path):
        N = json.load(open(path))
    for name, f in [('bands', fig_bands), ('kernels', fig_kernels), ('biasvar', fig_bias_variance), ('leakage', fig_leakage),
                    ('dpss', fig_dpss), ('mtmc', fig_mt_mc), ('ipspec', fig_ip_spectrum), ('ftest', fig_ftest),
                    ('coh', fig_coherence), ('dyncorr', fig_dyncorr), ('caus', fig_causality), ('gains', fig_gains),
                    ('cn', fig_cogley_nason), ('cycles', fig_ro_cycles), ('endpoint', fig_endpoint), ('sync', fig_sync),
                    ('spectrogram', fig_spectrogram), ('wavelets', fig_wavelets), ('mra', fig_mra), ('wvar', fig_wvar),
                    ('wcorr', fig_wcorr), ('cwt', fig_cwt_bet), ('wtc_dax', fig_wtc_bet_dax), ('wtc_spx', fig_wtc_bet_spx),
                    ('wtc_oil', fig_wtc_oil), ('wtc_infl', fig_wtc_infl), ('ai', fig_ai_case)]:
        if only and name not in only:
            continue
        print(name, flush=True)
        t0 = time.time()
        N[name] = f()
        print(f'   {time.time() - t0:.1f}s', flush=True)
        with open(path, 'w') as fh:
            json.dump(N, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else (list(o) if isinstance(o, tuple) else float(o)))
    print('written ch11_numbers.json')
