"""
build_quantlets.py -- Quantlet folders of Chapter 11 (ATS): spectral and wavelet analysis
=========================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_11/generate_all_charts.py && python3 Quantlets/Ch_11/seminar11.py
      python3 Quantlets/Ch_11/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 11
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import spectral_core as c                       # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('Eurostat (real GDP namq_10_gdp, industrial production sts_inpr_m, HICP prc_hicp_minr) and FRED (Brent crude oil '
        'DCOILBRENTEU), read online without a key; EODHD daily closes of the BET, DAX and S&P 500 (data/market of the ATS '
        'repository)')
INSTALL = '# PyWavelets gives the wavelet filters (Colab: installed here if missing)\n%pip install -q PyWavelets'
EXTRA_IMPORTS = ('import time\nfrom scipy import signal, sparse, linalg\nfrom scipy.sparse.linalg import spsolve\n'
                 'from scipy.ndimage import convolve1d')
CONSTS = [EXTRA_IMPORTS, f'SEED = {g.SEED!r}', f'END = {g.END!r}', f'PW_AR4 = {g.PW_AR4!r}', f'AR2 = {g.AR2!r}',
          f'AR2_SHARP = {g.AR2_SHARP!r}', f'BC_Q = {g.BC_Q!r}', f'BC_M = {g.BC_M!r}', f'CEE = {g.CEE!r}',
          f'GEO_LAB = {g.GEO_LAB!r}',
          "GEO_COL = {'RO': st.IDAred, 'PL': st.Purple, 'HU': st.Forest, 'CZ': st.Orange, 'EA20': st.MainBlue, 'EA': st.MainBlue}",
          '_MEM = {}', f'W0 = {c.W0!r}', 'FOURIER_FACTOR = 4 * np.pi / (W0 + np.sqrt(2 + W0 ** 2))',
          'KERNEL_CONST = ' + repr({k: tuple(float(x) for x in v) for k, v in c.KERNEL_CONST.items()}), '_DPSS = {}']
CORE = [c.fourier_freqs, c.periodogram, c.acov, c.kernel, c.lag_window, c.andrews_bandwidth, c.daniell, c.welch, c.dpss,
        c.eigenspectra, c.multitaper, c.harmonic_ftest, c.arma_spectrum, c.simulate_arma, c.cross_spectrum, c.band_dyncorr,
        c.var_ols, c.var_order, c.geweke, c.breitung_candelon, c.hp_filter, c.hp_one_sided, c.hp_gain, c.bk_weights,
        c.bk_filter, c.filter_gain, c.ideal_gain, c.hamilton_filter, c.hamilton_gain, c.concordance, c.wavelet_filters,
        c._transfer, c.modwt, c.mra, c.wavelet_variance, c.wavelet_corr, c.morlet_scales, c.cwt, c.ar1_coef,
        c.red_noise_signif, c._smooth, c.wavelet_coherence, c.coi_mask, c.wtc_montecarlo, c.ssa]
DATAF = [g.save, g.online, g.gdp, g.ip, g.hicp, g.weekly_returns, g.brent_weekly, g.daily_common, g.per_axis, g.shade_band,
         g.ip_growth, g.gdp_growth, g.bet_daily, g.year_axis, g.plot_tf]
BASE = DATAF + CORE

QUANTLETS = [
    dict(name='ATS_ch11_spectral_estimation',
         desc='Spectral estimation theory: variance shares of an AR(2) by frequency band (Cramer representation); lag and '
              'spectral windows (Bartlett, Parzen, Tukey-Hanning, quadratic spectral); Monte Carlo bias, variance and MSE of '
              'the Parzen estimator against the bandwidth with the asymptotic formulas; Slepian tapers; leakage on the AR(4) '
              'of Percival and Walden (1993) and the multitaper estimator of Thomson (1982) with adaptive weights; a Monte '
              'Carlo comparison of five estimators and the coverage of their chi-square bands.',
         keywords='spectral density, periodogram, lag window, bandwidth, multitaper, DPSS, leakage, Monte Carlo',
         consts=CONSTS, funcs=BASE + [g.fig_bands, g.fig_kernels, g.fig_bias_variance, g.fig_dpss, g.fig_leakage, g.fig_mt_mc],
         run=("print(fig_bands())\nprint(fig_kernels())\nprint(fig_bias_variance(reps=100))\nprint(fig_dpss())\n"
              "print(fig_leakage(reps=50))\nprint(fig_mt_mc(reps=100))"),
         charts=['ats_ch11_bands', 'ats_ch11_kernels', 'ats_ch11_bias_variance', 'ats_ch11_dpss', 'ats_ch11_leakage', 'ats_ch11_mt_mc']),
    dict(name='ATS_ch11_ip_spectrum',
         desc='Multitaper spectra (NW = 4, 95% chi-square bands) of monthly industrial production growth in Romania and the '
              'euro area, 2000-2026 (Eurostat), and Thomson\'s harmonic F test for seasonal and trading-day lines in the '
              'unadjusted and the seasonally adjusted Romanian series.',
         keywords='multitaper, industrial production, harmonic F test, residual seasonality, trading-day effects, Romania',
         consts=CONSTS, funcs=BASE + [g.fig_ip_spectrum, g.fig_ftest], run='print(fig_ip_spectrum())\nprint(fig_ftest())',
         charts=['ats_ch11_ip_spectrum', 'ats_ch11_ftest']),
    dict(name='ATS_ch11_cross_spectrum',
         desc='Multitaper coherence, phase and gain of monthly industrial production growth in Romania and the euro area; '
              'dynamic correlation (Croux, Forni and Reichlin 2001) of quarterly GDP growth of Romania, Poland, Hungary and '
              'Czechia with the euro area, 1995-2019 and 1995-2026.',
         keywords='cross-spectrum, coherence, phase, gain, dynamic correlation, business-cycle synchronisation, CEE',
         consts=CONSTS, funcs=BASE + [g.fig_coherence, g.fig_dyncorr], run='print(fig_coherence())\nprint(fig_dyncorr())',
         charts=['ats_ch11_coherence', 'ats_ch11_dyncorr']),
    dict(name='ATS_ch11_causality',
         desc='Granger causality by frequency between euro-area and Romanian industrial production growth: Geweke (1982) '
              'measures from a VAR and the Breitung-Candelon (2006) test across frequencies.',
         keywords='Granger causality, frequency domain, Geweke measure, Breitung-Candelon test, VAR',
         consts=CONSTS, funcs=BASE + [g.fig_causality], run='print(fig_causality())', charts=['ats_ch11_causality']),
    dict(name='ATS_ch11_filters',
         desc='Trend-cycle filters judged by their gain (ideal band-pass, Baxter-King, Christiano-Fitzgerald, HP, Hamilton '
              '2018); the spurious cycle of the HP filter on a random walk (Cogley and Nason 1995); cycles of Romanian real '
              'GDP 1995-2026; real-time against final cycles; synchronisation of Romania and the euro area (rolling '
              'correlation, Harding-Pagan concordance).',
         keywords='HP filter, Baxter-King, Christiano-Fitzgerald, Hamilton filter, business cycle, end-point problem, Romania',
         consts=CONSTS, funcs=BASE + [g.cf_central_weights, g.fig_gains, g.fig_cogley_nason, g.ro_cycles, g.fig_ro_cycles,
                                      g.fig_endpoint, g.fig_sync],
         run=("print(fig_gains())\nprint(fig_cogley_nason(reps=200))\nprint(fig_ro_cycles())\nprint(fig_endpoint())\n"
              "print(fig_sync())"),
         charts=['ats_ch11_gains', 'ats_ch11_cogley_nason', 'ats_ch11_ro_cycles', 'ats_ch11_endpoint', 'ats_ch11_sync']),
    dict(name='ATS_ch11_evolutionary',
         desc='A time-varying AR(2) whose peak period moves from 20 to 5: the true local spectrum and the short-time '
              'multitaper spectrogram (locally stationary processes, Dahlhaus 1997).',
         keywords='evolutionary spectrum, local stationarity, spectrogram, time-varying AR',
         consts=CONSTS, funcs=BASE + [g.tvar2, g.fig_spectrogram], run='print(fig_spectrogram())', charts=['ats_ch11_spectrogram']),
    dict(name='ATS_ch11_wavelets',
         desc='MODWT (LA(8)) squared gains and the Morlet wavelet; multiresolution analysis of daily BET returns; wavelet '
              'variance by scale of the BET, DAX and S&P 500 with 95% intervals; wavelet correlation and beta by scale '
              '(Whitcher, Guttorp and Percival 2000; Gencay, Selcuk and Whitcher 2005), 2000-2026.',
         keywords='MODWT, multiresolution analysis, wavelet variance, wavelet correlation, wavelet beta, BET, DAX',
         consts=CONSTS, funcs=BASE + [g.fig_wavelets, g.fig_mra, g.fig_wvar, g.fig_wcorr],
         run='print(fig_wavelets())\nprint(fig_mra())\nprint(fig_wvar())\nprint(fig_wcorr()["bet_dax"])',
         charts=['ats_ch11_wavelets', 'ats_ch11_mra', 'ats_ch11_wvar', 'ats_ch11_wcorr']),
    dict(name='ATS_ch11_wavelet_coherence',
         desc='Morlet wavelet power of weekly BET returns with the red-noise test (Torrence and Compo 1998); wavelet '
              'coherence and phase with Monte Carlo significance (Grinsted et al. 2004) for BET-DAX, BET-S&P 500, '
              'Brent-S&P 500 and annual HICP inflation of Romania and Poland against the euro area; the areawise check of '
              'how many significant islands independent AR(1) pairs produce.',
         keywords='continuous wavelet transform, wavelet coherence, Monte Carlo, cone of influence, co-movement, oil, inflation',
         consts=CONSTS, funcs=BASE + [g.fig_cwt_bet, g.wtc_pair, g.fig_wtc_bet_dax, g.fig_wtc_bet_spx, g.fig_wtc_oil,
                                      g.fig_wtc_infl, g.fig_ai_case],
         run=("print(fig_cwt_bet())\nprint(fig_wtc_bet_dax(reps=200))\nprint(fig_wtc_bet_spx(reps=200))\n"
              "print(fig_wtc_oil(reps=200))\nprint(fig_wtc_infl(reps=200))\nprint(fig_ai_case())"),
         charts=['ats_ch11_cwt_bet', 'ats_ch11_wtc_bet_dax', 'ats_ch11_wtc_bet_spx', 'ats_ch11_wtc_oil',
                 'ats_ch11_wtc_infl_ro', 'ats_ch11_wtc_infl_pl', 'ats_ch11_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar11 as s
    SEMC = [f'A2 = {s.A2!r}', f'A3 = {s.A3!r}', f'A4 = {s.A4!r}', f'A5 = {s.A5!r}', f'A6 = {s.A6!r}', f'A7 = {s.A7!r}',
            f'A8 = {s.A8!r}']
    SEMF = [s.hp_rw_peak, s.us_ip_growth, s.us_cycles]
    QUANTLETS.append(dict(
        name='ATS_ch11_seminar',
        desc='Seminar 11 of Advanced Time Series Analysis and Forecasting: the HP cycle of a random walk (Cogley and Nason '
             '1995) at three frequencies, confidence bands of lag-window and multitaper estimates, the cross-spectrum of a '
             'delayed copy, a Geweke measure, a Haar MODWT and the Morlet cone of influence; the spectrum of US industrial '
             'production, residual seasonality in German industrial production, coherence of US industrial production and '
             'unemployment, the Breitung-Candelon (2006) yield-spread application, filters for US GDP, real-time euro-area '
             'cycles, wavelet coherence of Bitcoin and the S&P 500, wavelet correlation of CEE indices with the DAX; CEE '
             'business-cycle synchronisation; an AI answer to audit.',
         keywords='seminar, spectral analysis, multitaper, coherence, frequency-domain causality, HP filter, wavelets',
        consts=CONSTS + SEMC,
        funcs=BASE + SEMF + [s.a1_cogley_nason, s.a2_frequencies, s.a3_lagwindow, s.a4_multitaper, s.a5_cross, s.a6_geweke,
                             s.a7_haar, s.a8_morlet, s.b1_us_ip, s.b2_de_seasonality, s.b3_okun, s.b4_breitung_candelon,
                             s.b5_us_filters, s.b6_ea_realtime, s.b7_btc_spx, s.b8_cee_wcorr, s.c1_cee_sync, s.c2_check],
        run="print(a1_cogley_nason())\nprint(a3_lagwindow())\nprint(a5_cross())\nprint(a7_haar())\nprint(b1_us_ip())\nprint(b3_okun())\nprint(b5_us_filters())\nprint(b7_btc_spx(reps=200))",
        charts=['ch11_sem_b1', 'ch11_sem_b3', 'ch11_sem_b5', 'ch11_sem_b7']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 11, 'Spectral and wavelet analysis', HERE, data=DATA, submitted=SUBMITTED, install=INSTALL)
