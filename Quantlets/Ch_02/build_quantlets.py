"""
build_quantlets.py -- Quantlet folders of Chapter 2 (ATS): structural breaks and nonlinear models
================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_02/generate_all_charts.py && python3 Quantlets/Ch_02/seminar2.py
      python3 Quantlets/Ch_02/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 2
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('US ex-post real interest rate of Bai and Perron (2003), JAE data archive; FRED: TB3MS, CPIAUCNS, CPIAUCSL, GDPC1, '
        'DEXUSUK, GBRCPIALLMINMEI, BLS unemployment and labour force of men aged 20 and over (LNS13000025, LNS11000025, '
        'LNU03000025, LNU01000025); UK CPI (ONS D7BT); Eurostat: Romanian HICP (prc_hicp_minr) and real GDP (namq_10_gdp); '
        'EUR/RON BNR reference rate; Canadian lynx (R data set via statsmodels)')
NODATA = 'Simulated data'
_N = json.load(open(os.path.join(HERE, 'ch2_numbers.json')))
CONSTS = ['import io', 'import zipfile', 'import urllib.error', 'import statsmodels.api as sm', 'HERE = "."',
          f'SEED = {g.SEED!r}', f'TRIM = {g.TRIM!r}', f'HICP_RO = {g.HICP_RO!r}', f'GDP_RO = {g.GDP_RO!r}', f'BP_URL = {g.BP_URL!r}',
          f'MPQ_SAMPLE = {g.MPQ_SAMPLE!r}', f'HANSEN_SAMPLE = {g.HANSEN_SAMPLE!r}', f'VDTF_SAMPLE = {g.VDTF_SAMPLE!r}',
          f'TPS_SAMPLE = {g.TPS_SAMPLE!r}', f'UK_CPI_ONS = {g.UK_CPI_ONS!r}', f'MON_HIST = {g.MON_HIST!r}',
          f'LYNX_SPEC = {g.LYNX_SPEC!r}', f'LWZ_C0, LWZ_D0 = {g.LWZ_C0!r}, {g.LWZ_D0!r}', f'A2_5 = {g.A2_5!r}',
          '_FILES = {}', '_NULL = {}',
          '# Bai-Perron critical values (simulated once with bp_critical(T=1000, reps=1000); see generate_all_charts.py)',
          f"_BPCV = {{'cv': {json.dumps(_N['bpcv'])}}}"]
DATAF = [g.get_bytes, g.save, g.bp_real_rate, g.us_real_rate, g.ro_hicp, g.us_gdp_growth, g.unemp_men, g.uk_cpi, g.real_usd_gbp,
         g.ro_reer, g.lynx, g.qlabel, g.mlabel]
REG = [g.ols, g.lags, g.lrv_qs, g.nw_lrv, g.recursive_residuals, g.dm_hln]
BREAK = [g.break_wald_seq, g.bb_null, g.null_dist, g.andrews_tests]
BP = [g.segment_ssr, g.dp_breaks, g.segments, g.bp_fstat, g.bp_seq_stat, g.bp_critical, g.bai_ci_quantiles, g.bp_analysis,
      g.bp_fit, g.bp_cv, g.ci_dates, g.plot_bp]
MON = [g.csw_size, g.csw_boundary, g.monitor_mc]
VAR = [g.icss_stat, g.icss]
UR = [g.adf_break_t, g.min_t_two_breaks, g.min_t_one_break]
WIN = [g.window_mc, g.ro_window_forecasts]
TAR = [g.threshold_grid, g.tar_ssr, g.tar_wald_robust, g.hansen_test, g.tar_estimate, g.lynx_setar, g.unemp_tar_data]
STAR = [g.logistic, g.lm3_test, g.vdtf_data, g.star_fit, g.star_predict, g.estar_resid, g.estar_fit, g.estar_girf,
        g.estar_girf_history, g.df_power_estar, g.kss_stat, g.kss_null]
NLT = [g.keenan_test, g.tsay_test, g.bds_test, g.nl_battery]
NLF = [g.tar_paths, g.ar_paths]
CORE = DATAF + REG + BREAK + BP
ALL = CORE + MON + VAR + UR + WIN + TAR + STAR + NLT + NLF

QUANTLETS = [
    dict(name='ATS_ch2_chow_snooping',
         desc='The Chow test at a known date and at the date that maximises it: Monte Carlo size of the 5% test on white noise for '
              'T = 50 to 800; the simulated asymptotic null distributions of the sup-, exp- and ave-Wald statistics (Andrews 1993; '
              'Andrews and Ploberger 1994) from Brownian bridges, with their critical values.',
         keywords='Chow test, structural break, unknown break date, sup-Wald, Andrews test, Davies problem, Brownian bridge',
         consts=CONSTS, funcs=CORE + [g.fig_chow_snooping], run='print(fig_chow_snooping(reps=1000))',
         charts=['ats_ch2_chow_snooping'], data=NODATA),
    dict(name='ATS_ch2_great_moderation',
         desc='The Great Moderation test of McConnell and Perez-Quiros (2000) on US real GDP growth (FRED GDPC1): AR(1) for the mean, '
              'sup-, exp- and ave-Wald tests for a break in the mean of sqrt(pi/2)|e_t|, in their sample 1953Q2-1999Q2, to 2019 and '
              'to 2026.',
         keywords='Great Moderation, variance break, sup-Wald, Andrews-Ploberger, GDP growth, structural change',
         consts=CONSTS, funcs=CORE + [g.mpq_test, g.fig_great_moderation], run='print(fig_great_moderation())',
         charts=['ats_ch2_great_moderation']),
    dict(name='ATS_ch2_bai_perron',
         desc='Multiple structural breaks (Bai and Perron 1998, 2003): dynamic programming, sup F(k), UDmax, sequential tests, BIC and '
              'LWZ, confidence intervals for the break dates (Bai 1997); replication of the US ex-post real interest rate example '
              '(JAE data archive), the series rebuilt from FRED to 2026, and mean shifts in Romanian HICP inflation (Eurostat).',
         keywords='Bai-Perron, multiple breaks, dynamic programming, sequential test, BIC, LWZ, real interest rate, inflation, Romania',
         consts=CONSTS, funcs=CORE + [g.fig_bai_perron, g.fig_ro_inflation_breaks],
         run='print(fig_bai_perron())\nprint(fig_ro_inflation_breaks())',
         charts=['ats_ch2_bai_perron', 'ats_ch2_ro_inflation_breaks']),
    dict(name='ATS_ch2_monitoring',
         desc='Real-time monitoring with the CUSUM boundary of Chu, Stinchcombe and White (1996): false-alarm rates of repeated '
              'one-shot tests and of the boundary by simulation; monitoring the mean of Romanian monthly HICP inflation from a '
              '2015-2019 historical sample.',
         keywords='monitoring, CUSUM, recursive residuals, boundary crossing, false alarm, inflation, Romania',
         consts=CONSTS, funcs=CORE + MON + [g.fig_monitoring], run='print(fig_monitoring(reps=500))',
         charts=['ats_ch2_monitoring']),
    dict(name='ATS_ch2_variance_breaks',
         desc='Breaks in the unconditional variance of daily EUR/RON returns (BNR reference rate): the ICSS algorithm with the '
              'Inclan-Tiao statistic and with the kappa-2 statistic of Sanso, Arago and Carrion (2004), robust to fat tails and '
              'conditional heteroskedasticity.',
         keywords='variance break, ICSS, Inclan-Tiao, kappa-2, cumulative sum of squares, EUR/RON, volatility regimes',
         consts=CONSTS, funcs=CORE + VAR + [g.fig_variance_breaks], run='print(fig_variance_breaks())',
         charts=['ats_ch2_variance_breaks']),
    dict(name='ATS_ch2_unit_root_breaks',
         desc='Unit roots and breaks on the log of Romanian real GDP (Eurostat): ADF, Zivot-Andrews and a two-break minimum-t test '
              '(Lumsdaine-Papell model) with sieve-bootstrap null distributions.',
         keywords='unit root, structural break, Zivot-Andrews, Lumsdaine-Papell, sieve bootstrap, GDP, Romania',
         consts=CONSTS, funcs=CORE + UR + [g.fig_unit_root_breaks], run='print(fig_unit_root_breaks(B=49))',
         charts=['ats_ch2_unit_root_breaks']),
    dict(name='ATS_ch2_forecast_windows',
         desc='Forecasting under breaks: the relative MSFE of expanding, rolling, post-break and window-averaged forecasts after a '
              'mean shift (Pesaran and Timmermann 2007; Pesaran and Pick 2011) by simulation; one-month-ahead AR(2) forecasts of '
              'Romanian inflation with DM-HLN tests.',
         keywords='forecasting under breaks, estimation window, rolling window, AveW, forecast combination across windows, inflation',
         consts=CONSTS, funcs=CORE + WIN + [g.fig_forecast_windows], run='print(fig_forecast_windows(reps=1000))',
         charts=['ats_ch2_forecast_windows']),
    dict(name='ATS_ch2_lynx',
         desc='The SETAR(2; 7, 2) model of Tong and Lim (1980) for the log10 Canadian lynx trappings 1821-1934: threshold by least '
              'squares, the coefficients at the published threshold 3.116, and the limit cycle of the skeleton.',
         keywords='SETAR, threshold autoregression, Tong-Lim, lynx, limit cycle, skeleton, nonlinear dynamics',
         consts=CONSTS, funcs=CORE + TAR + [g.fig_lynx], run='print(fig_lynx())', charts=['ats_ch2_lynx']),
    dict(name='ATS_ch2_unemp_tar',
         desc='The threshold autoregression of Hansen (1997) for the US unemployment rate of men aged 20 and over (BLS via FRED), '
              '1959.1-1996.7: heteroskedasticity-robust sup-Wald tests with the fixed-regressor bootstrap (Hansen 1996) for '
              'q = y(t-1) - y(t-d), d = 2..12, the threshold and its LR confidence interval (Hansen 2000), and 1959-2019.',
         keywords='TAR, threshold, Hansen bootstrap, sup-Wald, LR confidence interval, unemployment, asymmetry',
         consts=CONSTS, funcs=CORE + TAR + [g.fig_unemp_tar], run='print(fig_unemp_tar(B=100))',
         charts=['ats_ch2_unemp_tar']),
    dict(name='ATS_ch2_unemp_lstar',
         desc='The LSTAR model of van Dijk, Terasvirta and Franses (2002, Section 7) for the unadjusted US unemployment rate of men '
              'aged 20 and over: LM linearity tests for s = y(t-d) - y(t-d-12), the Terasvirta (1994) sequence, nonlinear least '
              'squares, one-step forecasts for 1990-1999 against the linear model.',
         keywords='LSTAR, smooth transition, LM linearity test, Terasvirta, unemployment, nonlinear least squares, forecasting',
         consts=CONSTS, funcs=CORE + STAR + [g.fig_unemp_lstar], run='print(fig_unemp_lstar())',
         charts=['ats_ch2_unemp_lstar']),
    dict(name='ATS_ch2_ppp_estar',
         desc='Nonlinear mean reversion of the real dollar-sterling exchange rate (Taylor, Peel and Sarno 2001): ESTAR by nonlinear '
              'least squares on 1973M01-1996M12 and on the extended sample, Monte Carlo p-value under a random walk, half-lives '
              'from generalised impulse responses by shock size, the power of the Dickey-Fuller test, the KSS test.',
         keywords='ESTAR, purchasing power parity, real exchange rate, half-life, generalised impulse response, KSS test',
         consts=CONSTS, funcs=CORE + STAR + [g.fig_ppp_estar], run='print(fig_ppp_estar(reps=400))',
         charts=['ats_ch2_ppp_estar']),
    dict(name='ATS_ch2_nonlinearity_tests',
         desc='A battery of nonlinearity tests (BDS, Keenan, Tsay, Terasvirta LM3, Hansen sup-Wald) on five series: lynx, US '
              'unemployment changes, Romanian GDP growth, the real dollar-sterling rate and daily EUR/RON returns.',
         keywords='nonlinearity test, BDS, Keenan, Tsay, LM test, sup-Wald, threshold',
         consts=CONSTS, funcs=CORE + TAR + STAR + NLT + [g.fig_nonlinearity_tests], run='print(fig_nonlinearity_tests(B=100))',
         charts=['ats_ch2_nonlinearity_tests']),
    dict(name='ATS_ch2_nonlinear_forecasts',
         desc='Forecasting with a threshold model: TAR of Hansen (1997) and a linear AR(12), fixed 1959-1996 parameters, simulated '
              '1- and 12-month forecasts of the US unemployment rate of men 20+, 1996-2019, overall and in the rising regime; '
              '12-month forecast densities at one origin.',
         keywords='nonlinear forecasting, TAR, simulation, forecast density, Diebold-Mariano, unemployment',
         consts=CONSTS, funcs=CORE + TAR + NLF + [g.fig_nonlinear_forecasts], run='print(fig_nonlinear_forecasts(n_paths=200))',
         charts=['ats_ch2_nonlinear_forecasts']),
    dict(name='ATS_ch2_ai_discovery',
         desc='AI for scientific discovery, mini-case: is the ESTAR evidence for the real dollar-sterling rate (KSS test) robust to '
              'Bai-Perron mean regimes? Null distributions by simulating random walks through the same break search.',
         keywords='nonlinearity, structural breaks, KSS test, Bai-Perron, real exchange rate, simulation',
         consts=CONSTS, funcs=CORE + STAR + [g.fig_ai_case], run='print(fig_ai_case(reps=200))', charts=['ats_ch2_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar2 as s
    QUANTLETS.append(dict(
        name='ATS_ch2_seminar',
        desc='Seminar 2 of Advanced Time Series Analysis and Forecasting: the Chow test and the Wald process by hand, dynamic '
             'programming on a toy series, BIC and LWZ, a SETAR skeleton and the threshold LR critical value, ESTAR half-lives, the '
             'CUSUM monitoring boundary and the kappa-2 correction, the optimal window after a break; the Great Moderation test '
             'on Romanian GDP growth, Bai-Perron on the Romanian 3-month rate, a SETAR for the sunspots, an ESTAR for the Romanian '
             'real effective exchange rate, variance breaks in BET returns; window choice for Romanian inflation forecasts.',
        keywords='seminar, structural breaks, Bai-Perron, Chow test, SETAR, ESTAR, ICSS, monitoring, Romania',
        consts=CONSTS + [f'RATE_RO = {s.RATE_RO!r}', f'RATE_START = {s.RATE_START!r}', f'C1_H, C1_FIRST = {s.C1_H!r}, {s.C1_FIRST!r}'],
        funcs=ALL + [s.a1_chow, s.a2_wald_mean, s.a3_dp, s.a5_setar, s.a6_estar, s.a7_monitoring, s.a8_window,
                     s.b1_ro_moderation, s.b2_ro_rate, s.b3_sunspots, s.b4_ro_reer, s.b5_bet_variance, s.c1_windows],
        run="print(a1_chow())\nprint(a3_dp())\nprint(a5_setar())\nprint(a7_monitoring())\nprint(b1_ro_moderation())\n"
            "print(b3_sunspots(B=100))",
        charts=['ch2_sem_b1', 'ch2_sem_b3']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 2, 'Structural breaks and nonlinear models', HERE, data=DATA, submitted=SUBMITTED)
