"""
build_quantlets.py -- Quantlet folders of Chapter 10 (ATS): long memory and rough volatility
============================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_10/generate_all_charts.py && python3 Quantlets/Ch_10/seminar10.py
      python3 Quantlets/Ch_10/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 10
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import lm_core as c                             # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('Oxford-Man Institute realized library v0.3 (Heber, Lunde, Shephard and Sheppard 2009), six equity indices, '
        '2000-2022 (archived copy of 28 February 2022, downloaded from the Internet Archive by read_omi, not redistributed), '
        'and Bitcoin realised measures from Binance one-minute prices, 2018-2026 (data/realized of the ATS repository); EODHD daily data of the S&P 500, DAX, BET, Bitcoin and VIX (data/market); EUR/RON: official BNR '
        'reference rate; FRED CPIAUCSL; Eurostat prc_hicp_minr')
CONSTS = ['import functools\nfrom scipy import integrate, signal, special\nfrom scipy.signal import lfilter',
          f'SEED = {g.SEED!r}', f'REAL_RAW = {g.REAL_RAW!r}',
          "REAL_DIR = next((os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..')\n"
          "                 if os.path.isdir(os.path.join(d, 'data', 'realized'))), '')",
          f'OMI_NAMES = {g.OMI_NAMES!r}', f'LAGS = {g.LAGS!r}', f'QS = {g.QS!r}', f'A_BW = {g.A_BW!r}', f'FC = {g.FC!r}',
          f'VOL_ASSETS = {g.VOL_ASSETS!r}', f'ASSETS_D = {g.ASSETS_D!r}', f'FC_ASSETS = {g.FC_ASSETS!r}',
          f'AI_MEASURES = {g.AI_MEASURES!r}', '_MEM = {}']
CORE = [c.frac_weights, c.frac_diff, c.arfima_acov, c.arfima_acf, c.fgn_acov, c.circulant_sim, c.circulant_eigs,
        c.sim_arfima, c.fbm, c.hybrid_rl, c.periodogram, c.bandwidth, c.gph, c.lw_objective, c.local_whittle,
        c.shimotsu_weight, c.elw_objective, c.elw, c.lwn, c.lbias_constant, c.mse_opt_m, c.qu_stat, c.qu_critical,
        c.random_level_shift, c.fcvar_loglik, c.fcvar_fit, c.nbls, c.arch_inf_weights, c.arch_inf_sigma2, c._t_loglik,
        c.ltm_negll, c.ltm_fit, c.variogram, c.gjr_scaling, c.h_with_noise, c.rfsv_kernel, c.rfsv_c, c.har_design,
        c.har_ar_weights, c.nw_lrv, c.dm_stat, c.qlike]
DATAF = [g.save, g.read_realized, g.omi, g.binance, g.rv_series, g.parkinson, g.returns, g.sample_acf, g.inflation]
BASE = DATAF + CORE

QUANTLETS = [
    dict(name='ATS_ch10_memory',
         desc='Long memory: twenty-two years of S&P 500 log realised variance (Oxford-Man) and Bitcoin log RV with the '
              'hyperbolic decay of the ACF; ARFIMA autocorrelations and spectra against AR(1); aggregation of AR(1) series '
              'with Beta-distributed coefficients (Granger 1980).',
         keywords='long memory, ARFIMA, autocorrelation, spectral density, aggregation, realised variance',
         consts=CONSTS, funcs=BASE + [g.fig_overview, g.fig_acf_spec, g.aggregate_ar1, g.fig_aggregation],
         run='print(fig_overview())\nprint(fig_acf_spec())\nprint(fig_aggregation(reps=5))',
         charts=['ats_ch10_overview', 'ats_ch10_acf_spec', 'ats_ch10_aggregation']),
    dict(name='ATS_ch10_estimation',
         desc='Semiparametric estimation of d: Monte Carlo of GPH, local Whittle and exact local Whittle (Shimotsu and '
              'Phillips 2005) for d = 0.3 and d = 1.2; bias and RMSE of local Whittle across bandwidths for ARFIMA(1, 0.3, 0) '
              'against the leading bias term and the MSE-optimal bandwidth.',
         keywords='GPH, local Whittle, exact local Whittle, bandwidth, bias, Monte Carlo, fractional integration',
         consts=CONSTS, funcs=BASE + [g.fig_mc_estimators, g.fig_bandwidth],
         run='print(fig_mc_estimators(reps=100))\nprint(fig_bandwidth(reps=100))',
         charts=['ats_ch10_mc_estimators', 'ats_ch10_bandwidth']),
    dict(name='ATS_ch10_qu_test',
         desc='The Qu (2011) test against spurious long memory: simulated critical values, size and power against random '
              'level shifts and a break in mean, local Whittle d across bandwidths (Perron and Qu 2010); US and Romanian '
              'inflation persistence before and after the disinflation (exact local Whittle with unknown mean).',
         keywords='spurious long memory, level shifts, Qu test, inflation persistence, exact local Whittle',
         consts=CONSTS, funcs=BASE + [g.qu_designs, g.fig_qu, g.fig_inflation],
         run='print(fig_qu(reps=100))\nprint(fig_inflation())', charts=['ats_ch10_qu', 'ats_ch10_inflation']),
    dict(name='ATS_ch10_fcvar',
         desc='Fractionally cointegrated VAR (Johansen and Nielsen 2012) with k = 0 of S&P 500 log realised variance and log '
              'VIX^2, profile likelihood over (d, b), trace tests, the cointegrating vector, narrow-band least squares.',
         keywords='fractional cointegration, FCVAR, realised variance, implied volatility, VIX, narrow-band least squares',
         consts=CONSTS, funcs=BASE + [g.rv_vix, g.fig_fcvar], run='print(fig_fcvar())', charts=['ats_ch10_fcvar']),
    dict(name='ATS_ch10_figarch',
         desc='Long memory in volatility: GARCH(1,1), FIGARCH(1,d,1) and HYGARCH with Student t innovations for the S&P 500, '
              'BET and Bitcoin; local Whittle d of |r|, log r^2 and log RV with the noise-robust estimator of Hurvich, '
              'Moulines and Soulier (2005) and the Qu test; HAR as an approximation of long memory (Corsi 2009).',
         keywords='FIGARCH, HYGARCH, long-memory stochastic volatility, local Whittle with noise, HAR, BET, EUR/RON',
         consts=CONSTS, funcs=BASE + [g.fig_figarch, g.logsq, g.fig_assets_d, g.har_fit_full, g.fig_har_approx],
         run='print(fig_figarch())\nprint(fig_assets_d())\nprint(fig_har_approx())',
         charts=['ats_ch10_figarch', 'ats_ch10_assets_d', 'ats_ch10_har_approx']),
    dict(name='ATS_ch10_simulation',
         desc='Simulating fractional processes: fractional Brownian motion by circulant embedding (Davies and Harte 1987) for '
              'H = 0.1, 0.3, 0.5, 0.7; the Riemann-Liouville process by the forward Riemann sum and by the hybrid scheme of '
              'Bennedsen, Lunde and Pakkanen (2017).',
         keywords='fractional Brownian motion, circulant embedding, Davies-Harte, hybrid scheme, Riemann-Liouville, rough volatility',
         consts=CONSTS, funcs=BASE + [g.fig_fbm_paths, g.fig_hybrid], run='print(fig_fbm_paths())\nprint(fig_hybrid())',
         charts=['ats_ch10_fbm_paths', 'ats_ch10_hybrid']),
    dict(name='ATS_ch10_rough',
         desc='Rough volatility: the scaling of S&P 500 log volatility (Gatheral, Jaisson and Rosenbaum 2018) on Oxford-Man '
              '5-minute RV; H for six indices and Bitcoin, with a measurement-error intercept and from Parkinson ranges; a '
              'simulation of measurement error; roughness and persistence (Bennedsen, Lunde and Pakkanen 2022); robustness '
              'of H across assets, measures, estimators and subsamples.',
         keywords='rough volatility, Hurst exponent, fractional Brownian motion, realised variance, measurement error, Oxford-Man',
         consts=CONSTS, funcs=BASE + [g.fig_gjr, g.fig_gjr_assets, g.sim_sv_rv, g.fig_noise_sim, g.fig_decouple, g.fig_ai_case],
         run='print(fig_gjr())\nprint(fig_gjr_assets())\nprint(fig_noise_sim(reps=3))\nprint(fig_decouple())\nprint(fig_ai_case())',
         charts=['ats_ch10_gjr', 'ats_ch10_gjr_assets', 'ats_ch10_noise_sim', 'ats_ch10_decouple', 'ats_ch10_ai_case']),
    dict(name='ATS_ch10_forecast',
         desc='Forecasting realised variance: the RFSV kernel (Gatheral, Jaisson and Rosenbaum 2018) against HAR weights; '
              'rolling out-of-sample forecasts of RV at 1, 5 and 22 days from HAR, ARFIMA and RFSV for the S&P 500, DAX and '
              'Bitcoin, QLIKE and Diebold-Mariano tests.',
         keywords='rough volatility forecasting, RFSV, HAR, ARFIMA, QLIKE, Diebold-Mariano, realised variance',
         consts=CONSTS, funcs=BASE + [g.rfsv_kernel_c, g.fig_rfsv_kernel, g.forecast_rv, g.evaluate_forecasts,
                                      g.run_forecasts, g.fig_forecast],
         run='print(fig_rfsv_kernel())\nprint(fig_forecast())', charts=['ats_ch10_rfsv_kernel', 'ats_ch10_forecast']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar10 as s
    SEMC = [f'A{i} = {getattr(s, f"A{i}")!r}' for i in range(1, 9)]
    SEMF = [g.har_fit_full, g.rfsv_kernel_c, g.forecast_rv, g.evaluate_forecasts]
    QUANTLETS.append(dict(
        name='ATS_ch10_seminar',
        desc='Seminar 10 of Advanced Time Series Analysis and Forecasting: ARFIMA autocorrelations and the variance of the '
             'mean, fractional differencing weights, standard errors and bias of GPH and local Whittle, fractional Gaussian '
             'noise, the RFSV kernel, circulant embedding by hand, Markov switching that mimics long memory; memory of '
             'FTSE 100 log RV, the BET and EUR/RON, roughness of the Euro Stoxx 50 and Bitcoin, forecasting FTSE 100 and '
             'CAC 40 realised variance; FCVAR of DAX and CAC 40 volatility; an AI answer to audit.',
        keywords='seminar, long memory, local Whittle, Qu test, rough volatility, RFSV, HAR, FCVAR',
        consts=CONSTS + SEMC,
        funcs=BASE + SEMF + [s.a1_arfima, s.a2_weights, s.a3_se, s.a4_bias, s.a5_fgn, s.a6_kernel, s.a7_circulant,
                             s.a8_switching, s.memory_table, s.b1_ftse, s.b2_bet_eurron, s.b3_stoxx, s.b4_btc_freq,
                             s.forecast_case, s.b5_ftse_forecast, s.b6_cac_forecast, s.c1_fcvar, s.c2_check],
        run="print(a1_arfima())\nprint(a3_se())\nprint(a5_fgn())\nprint(a7_circulant())\nprint(b1_ftse())\nprint(b3_stoxx())\nprint(b5_ftse_forecast())",
        charts=['ch10_sem_b1', 'ch10_sem_b3', 'ch10_sem_b5']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 10, 'Long memory and rough volatility', HERE, data=DATA, submitted=SUBMITTED)
