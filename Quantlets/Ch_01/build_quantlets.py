"""
build_quantlets.py -- Quantlet folders of Chapter 1 (ATS): forecast evaluation, scoring rules and combination
=============================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_01/generate_all_charts.py && python3 Quantlets/Ch_01/seminar1.py
      python3 Quantlets/Ch_01/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 1
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('S&P 500 daily closes from EODHD (data/market of the ATS repository); EUR/RON BNR reference rate; Romanian HICP '
        'inflation and 3-month money-market rates (Eurostat prc_hicp_minr, irt_st_m); US CPI and unemployment (FRED '
        'CPIAUCSL, UNRATE); individual forecasts of the Survey of Professional Forecasters and the Real-Time Data Set for '
        'Macroeconomists (Federal Reserve Bank of Philadelphia, public files); Romanian hourly electricity load '
        '(Energy-Charts, Fraunhofer ISE, ENTSO-E transparency data)')
NODATA = 'Simulated data'
INSTALL = ("# The arch package (Hansen's SPA test) is not preinstalled in Google Colab: pip install arch\n"
           "import importlib.util, subprocess, sys\n"
           "if importlib.util.find_spec('arch') is None:\n"
           "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'arch'])")
CONSTS = ['import io', 'import urllib.error', 'from scipy import special', 'import statsmodels.api as sm',
          f'SEED = {g.SEED!r}', f'HICP_RO = {g.HICP_RO!r}', f'RATE_RO = {g.RATE_RO!r}', f'RATE_EA = {g.RATE_EA!r}',
          f'SPF_URL = {g.SPF_URL!r}', f'RTDSM_URL = {g.RTDSM_URL!r}', f'LOAD_API = {g.LOAD_API!r}',
          f'LOAD_YEARS = {g.LOAD_YEARS!r}', f'LOAD_END = {g.LOAD_END!r}', f'DGT_SPLIT = {g.DGT_SPLIT!r}',
          f'INFL_H, INFL_WIN, INFL_P = {g.INFL_H!r}, {g.INFL_WIN!r}, {g.INFL_P!r}', f'INFL_EVAL = {g.INFL_EVAL!r}',
          f'BNR_TARGET = {g.BNR_TARGET!r}', f'AO_WIN, AO_LAGS, AO_EVAL = {g.AO_WIN!r}, {g.AO_LAGS!r}, {g.AO_EVAL!r}',
          f'FX_START, FX_EVAL = {g.FX_START!r}, {g.FX_EVAL!r}',
          f'LOAD_WIN, LOAD_RES, LOAD_EVAL = {g.LOAD_WIN!r}, {g.LOAD_RES!r}, {g.LOAD_EVAL!r}',
          'TAUS = np.arange(1, 100) / 100', f'SPF_VAR, SPF_H = {g.SPF_VAR!r}, {g.SPF_H!r}', f'SPF_EVAL = {g.SPF_EVAL!r}',
          f'SPF_WIN, SPF_MIN = {g.SPF_WIN!r}, {g.SPF_MIN!r}',
          f'MCS_ALPHA, BOOT_B, BLOCK = {g.MCS_ALPHA!r}, {g.BOOT_B!r}, {g.BLOCK!r}', '_FILES = {}']
CORE = [g.get_bytes, g.save, g.pinball, g.interval_score, g.crps_normal, g.crps_t, g.hac_var, g.dm_test, g.gw_test,
        g.cw_test, g.mz_test, g.encompassing_test, g.berkowitz_test, g.mcs]
DATAF = [g.spf_sheet, g.us_cpi_quarterly, g.ro_load_hourly, g.realtime_gdp]
GARCH = [g.garch_filter, g.logdens, g.garch_fit, g.dgt_forecasts]
SPF = [g.spf_panel, g.combine_spf]

QUANTLETS = [
    dict(name='ATS_ch1_loss_functions',
         desc='Loss functions and optimal point forecasts: the expected squared, absolute and pinball (tau = 0.9) loss of a '
              'log-normal variable as functions of the point forecast, minimised by the mean, the median and the '
              '0.9-quantile (Gneiting 2011).',
         keywords='loss function, consistency, elicitability, mean, median, quantile, pinball loss, Bregman loss',
         consts=CONSTS, funcs=CORE + [g.fig_loss_minimizers], run='print(fig_loss_minimizers())',
         charts=['ats_ch1_loss_minimizers'], data=NODATA),
    dict(name='ATS_ch1_calibration_scores',
         desc='Calibration and proper scoring rules: PIT histograms of ideal, too sharp, too wide and biased Normal forecasts '
              'with their CRPS and log scores; expected log score, CRPS and the improper linear score as functions of the '
              'forecast spread (Gneiting, Balabdaoui and Raftery 2007; Gneiting and Raftery 2007).',
         keywords='calibration, sharpness, PIT, proper scoring rule, logarithmic score, CRPS, linear score',
         consts=CONSTS, funcs=CORE + [g.fig_pit_shapes, g.fig_proper_scores],
         run='print(fig_pit_shapes())\nprint(fig_proper_scores())', charts=['ats_ch1_pit_shapes', 'ats_ch1_proper_scores'],
         data=NODATA),
    dict(name='ATS_ch1_density_forecasts',
         desc='The density forecast evaluation of Diebold, Gunther and Tay (1998) re-run on the S&P 500: i.i.d. Normal, '
              'MA(1)-GARCH(1,1)-Normal and MA(1)-GARCH(1,1)-t estimated on 2000-2012 with fixed parameters, one-day density '
              'forecasts for 2013-2026; PIT histograms and correlograms, Berkowitz test, log score and CRPS with DM tests '
              '(Amisano and Giacomini 2007), optimal linear pools (Geweke and Amisano 2011).',
         keywords='density forecast, PIT, Berkowitz test, GARCH-t, log score, CRPS, optimal prediction pool, S&P 500',
         consts=CONSTS, funcs=CORE + GARCH + [g.fig_dgt, g.fig_pool], run='print(fig_dgt())\nprint(fig_pool())',
         charts=['ats_ch1_dgt', 'ats_ch1_pool']),
    dict(name='ATS_ch1_dm_tests',
         desc='Diebold-Mariano tests with HAC variance and the Harvey-Leybourne-Newbold correction: Monte Carlo size for '
              'small samples; Romanian HICP inflation 12 months ahead (AR(3), no change, BNR target, average) with DM, HLN '
              'and Giacomini-White; Atkeson and Ohanian (2001) on US CPI inflation: the naive forecast against the '
              'Phillips curve of Stock and Watson (1999), with GW and encompassing tests.',
         keywords='Diebold-Mariano, HAC, Harvey-Leybourne-Newbold, Giacomini-White, encompassing, inflation, Romania, Phillips curve',
         consts=CONSTS, funcs=CORE + [g.us_cpi_quarterly, g.ro_inflation_forecasts, g.fig_ro_inflation, g.fig_dm_size,
                                      g.ao_forecasts, g.fig_ao],
         run='print(fig_ro_inflation())\nprint(fig_dm_size(reps=1000))\nprint(fig_ao())',
         charts=['ats_ch1_ro_inflation', 'ats_ch1_dm_size', 'ats_ch1_ao']),
    dict(name='ATS_ch1_nested_spa',
         desc='Meese and Rogoff (1983) on monthly EUR/RON (BNR reference rate): recursive forecasts of drift, AR(1-4), the '
              'uncovered-interest-parity regression on the Romania minus euro-area 3-month rate differential (Eurostat), '
              'UIP imposed, momentum and their average against the random walk; Clark-West tests for nested models and '
              "Hansen's SPA test (arch package).",
         keywords='Clark-West, nested models, random walk, Meese-Rogoff, uncovered interest parity, SPA, reality check, EUR/RON',
         consts=CONSTS, funcs=CORE + [g.eurron_data, g.eurron_forecasts, g.fig_eurron], run='print(fig_eurron())',
         charts=['ats_ch1_eurron']),
    dict(name='ATS_ch1_load_mcs',
         desc='Day-ahead probabilistic forecasts of Romanian hourly electricity load (Energy-Charts, ENTSO-E data): naive, '
              'weekly naive, four-week mean, the expert ARX model of Ziel and Weron (2018) and a combination; quantiles at '
              'the 99 percentiles scored by the pinball loss of GEFCom2014, coverage, and the Model Confidence Set of '
              'Hansen, Lunde and Nason (2011).',
         keywords='electricity load, probabilistic forecasting, pinball loss, quantile forecast, expert ARX, Model Confidence Set, Romania',
         consts=CONSTS, funcs=CORE + [g.ro_load_hourly, g.load_forecasts, g.fig_load], run='print(fig_load())',
         charts=['ats_ch1_load_week', 'ats_ch1_load_mcs']),
    dict(name='ATS_ch1_combination',
         desc='The forecast combination puzzle by simulation (Smith and Wallis 2009): the MSE of Bates-Granger weights '
              'estimated from n past errors relative to equal weights, for similar and dissimilar forecasts.',
         keywords='forecast combination, combination puzzle, Bates-Granger, equal weights, estimation error, simulation',
         consts=CONSTS, funcs=CORE + [g.fig_puzzle], run='print(fig_puzzle(reps=2000))', charts=['ats_ch1_puzzle'],
         data=NODATA),
    dict(name='ATS_ch1_spf_combination',
         desc='Combination schemes on the individual CPI forecasts of the US Survey of Professional Forecasters (four '
              'quarters ahead, surveys 1990-2025): mean, median, trimmed mean, inverse-MSE performance weights, shrinkage '
              'and the previous best forecaster, as compared by Genre et al. (2013); DM-HLN, Mincer-Zarnowitz and a '
              'sub-period robustness check of the shrinkage factor.',
         keywords='forecast combination, Survey of Professional Forecasters, equal weights, median, shrinkage, Mincer-Zarnowitz',
         consts=CONSTS, funcs=CORE + DATAF + SPF + [g.fig_spf, g.fig_ai_case], run='print(fig_spf())\nprint(fig_ai_case())',
         charts=['ats_ch1_spf', 'ats_ch1_spf_schemes', 'ats_ch1_ai_case']),
    dict(name='ATS_ch1_real_time',
         desc='Real-time data: first release against the latest vintage of US real GDP growth (Philadelphia Fed RTDSM), the '
              'size of revisions, and the SPF current-quarter nowcast evaluated against each vintage.',
         keywords='real-time data, data vintages, revisions, RTDSM, ALFRED, GDP, nowcast, Survey of Professional Forecasters',
         consts=CONSTS, funcs=CORE + DATAF + [g.fig_realtime], run='print(fig_realtime())', charts=['ats_ch1_realtime']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar1 as s
    QUANTLETS.append(dict(
        name='ATS_ch1_seminar',
        desc='Seminar 1 of Advanced Time Series Analysis and Forecasting: optimal forecasts under several losses, log score '
             'and CRPS, DM, HLN and Clark-West by hand, Bates-Granger weights and their estimation cost; Romanian GDP '
             'growth forecasts with DM-HLN; combining SPF unemployment forecasts; EUR/RON density forecasts; SPF GDP '
             'forecasts against data vintages; Romanian electricity load quantiles at the evening peak; Romanian '
             'inflation forecasts by horizon with a Holm correction.',
        keywords='seminar, forecast evaluation, Diebold-Mariano, Clark-West, CRPS, PIT, forecast combination, real-time data, Romania',
        consts=CONSTS + [f'GDP_RO = {s.GDP_RO!r}', f'GDP_EVAL = {s.GDP_EVAL!r}', f'FX_DAILY = {s.FX_DAILY!r}',
                         f'SPF_U, SPF_UH = {s.SPF_U!r}, {s.SPF_UH!r}', f'PEAK_HOUR = {s.PEAK_HOUR!r}', f'HORIZONS = {s.HORIZONS!r}'],
        funcs=CORE + DATAF + GARCH[:3] + SPF + [g.ro_inflation_forecasts, g.load_forecasts,
                                                s.a1_optimal_forecasts, s.a2_linex, s.a3_scores, s.a4_linear_and_interval,
                                                s.a5_dm_by_hand, s.a6_cw_by_hand, s.a7_bates_granger, s.a8_puzzle,
                                                s.b1_ro_gdp, s.spf_unemp_panel, s.b2_spf_unemployment, s.b3_eurron_density,
                                                s.b4_spf_vintages, s.b5_load_peak, s.c1_inflation_by_horizon, s.c2_check],
        run="print(a1_optimal_forecasts())\nprint(a3_scores())\nprint(a5_dm_by_hand())\nprint(a7_bates_granger())\n"
            "print(b1_ro_gdp())\nprint(b3_eurron_density())",
        charts=['ch1_sem_b1', 'ch1_sem_b3']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 1, 'Forecast evaluation, scoring rules and combination', HERE, data=DATA, submitted=SUBMITTED,
              install=INSTALL)
