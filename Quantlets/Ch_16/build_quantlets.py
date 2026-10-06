"""
build_quantlets.py -- Quantlet folders of Chapter 16 (ATS): explosive roots and bubbles (self-study)
====================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
The notebooks use smaller Monte Carlo and bootstrap sizes than the slides (set in each run cell) and one process,
so that they finish on a Colab CPU; the LPPLS indicator series are read from the cached CSV files of the chapter.
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_16/generate_all_charts.py
      python3 Quantlets/Ch_16/build_quantlets.py
      python3 notebooks/add_colab_banner.py
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_data as AD                           # noqa: E402
import bubble_core as c                         # noqa: E402
import generate_all_charts as g                 # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Tuesday, 6 October 2026'
DATA = ('EODHD daily closes of the S&P 500, Nasdaq 100, Shanghai Composite, BET and Bitcoin and of all price series of '
        'data/market (ATS repository); FRED: S&P CoreLogic Case-Shiller US national index, CPI rent of primary residence, '
        'CPI; Eurostat: Romanian house price index and HICP (actual rentals, all items); all read without a key')
INSTALL = '# the residual unit-root test of the LPPLS filter uses arch (Phillips-Perron)\n%pip install -q arch'
CONSTS = ['import io', "# the cached indicator series: this folder, the chapter folder of a local copy, or GitHub (read_cached)",
          "HERE = next((p for p in ('.', '../../Quantlets/Ch_16', '../Quantlets/Ch_16', 'Quantlets/Ch_16') if os.path.exists(os.path.join(p, 'ch16_ci_ssec.csv'))), '.')", 'PROCS = 1', f'SEED = {g.SEED!r}', f"END = {g.END!r}", f'SAMPLES = {g.SAMPLES!r}',
          f'PEAKS = {g.PEAKS!r}',
          "COLORS = {'sp500': st.MainBlue, 'ndx': st.Teal, 'ssec': st.Orange, 'btc': st.Amber, 'bet': st.Crimson}",
          f'SHADE = {g.SHADE!r}', f'CRASH, HORIZON = {g.CRASH!r}, {g.HORIZON!r}', f'RO_END = {g.RO_END!r}',
          f'TAU = {g.TAU!r}', '_MEM = {}', f'CSV_RAW = {g.CSV_RAW!r}', f'EVAL = {g.EVAL!r}', f'EXCLUDE = {g.EXCLUDE!r}',
          f'LPPLS_SEARCH = {c.LPPLS_SEARCH!r}', f'LPPLS_FILTER = {c.LPPLS_FILTER!r}', f'WINDOWS = {c.WINDOWS!r}']
CORE = [c._cums, c._adf_end, c.adf_window, c.min_window, c._lag_design, c._bsadf_lags, c.psy, c.bsadf_paths, c.bic_lag,
        c.null_paths, c.psy_cv, c.wild_cv, c.episodes, c.weekly, c.blanchard_watson, c.evans_price, c.bubble_collapse,
        c.ar1_explosive, c.ols_rho, c.csw_constant, c.cusum_monitor, c.yrs, c.todate, c.lppl_design, c.lppl_linear,
        c._damping, c._grid, c.lppl_fit, c.lomb_pvalue, c.ar1_pass, c.lppl_conditions, c.qualified, c.ci_point,
        c.confidence_series, c.tc_profile, c.future_fall, c.auc, c.roc, c.block_bootstrap_auc, c.alarm_table,
        AD.manifest, g.read_cached, g.save, g.d2s, g.prices, g.min_len, g._pool]

QUANTLETS = [
    dict(name='ATS_ch16_rational_bubbles',
         desc='Rational bubbles: a Blanchard-Watson bubble that can burst (and turn negative, the case excluded by Diba and '
              'Grossman), an Evans (1991) periodically collapsing bubble added to the present-value fundamental of '
              'random-walk dividends; whole-sample ADF against SADF, GSADF and BSADF date-stamping with Monte Carlo '
              'critical values.',
         keywords='rational bubble, Blanchard-Watson, Evans, periodically collapsing bubble, present value, SADF, GSADF, BSADF',
         consts=CONSTS, funcs=CORE + [g.fig_rational], run='print(fig_rational(save_it=False, R=500))',
         charts=['ats_ch16_rational']),
    dict(name='ATS_ch16_explosive_asymptotics',
         desc='Explosive autoregressions: the normalised OLS error rho^n (rho_hat - rho)/(rho^2 - 1) for a mildly explosive '
              'root (Phillips and Magdalinos 2007) and a fixed explosive root (White 1958, Anderson 1959) with Gaussian and '
              'centred exponential errors, against the standard Cauchy law; Kolmogorov-Smirnov distances and the coverage '
              'of the 95% Cauchy confidence interval.',
         keywords='explosive autoregression, Cauchy limit, mildly explosive, invariance principle, confidence interval',
         consts=CONSTS, funcs=CORE + [g.fig_asymptotics], run='print(fig_asymptotics(save_it=False, R=5000))',
         charts=['ats_ch16_asymptotics']),
    dict(name='ATS_ch16_recursive_tests',
         desc='Null distributions of the whole-sample right-tailed ADF, SADF (Phillips, Wu and Yu 2011) and GSADF (Phillips, '
              'Shi and Yu 2015) under a random walk with a weak drift, and their 95% critical values for T = 100, 200, 400 '
              'and 800 with the minimum window r0 = 0.01 + 1.8/sqrt(T).',
         keywords='right-tailed unit root test, SADF, GSADF, BSADF, critical values, Monte Carlo',
         consts=CONSTS, funcs=CORE + [g.fig_null], run='print(fig_null(save_it=False, Ts=(100, 200, 400), R=500))',
         charts=['ats_ch16_null']),
    dict(name='ATS_ch16_size_wild_bootstrap',
         desc='Size of GSADF and of BSADF date-stamping under the null with constant volatility, a rise or fall of volatility '
              'and GARCH(1,1) shocks: Monte Carlo against wild-bootstrap (Phillips and Shi 2020) critical values, pointwise '
              'against family-wise thresholds; share of paths with at least one false dated episode.',
         keywords='wild bootstrap, non-stationary volatility, size, family-wise error rate, date-stamping',
         consts=CONSTS, funcs=CORE + [g.vol_path, g._size_job, g.fig_size],
         run='print(fig_size(save_it=False, N=96, B=99, Rmc=1000))', charts=['ats_ch16_size']),
    dict(name='ATS_ch16_date_stamping',
         desc='Accuracy of BSADF date-stamping in a bubble-and-collapse process (random walk, explosive phase with rho = '
              '1.005, 1.01, 1.02, collapse, random walk): detection rate, delay of the dated start and of the confirmation, '
              'false episodes before the bubble.',
         keywords='date-stamping, origination, detection delay, bubble-and-collapse process, BSADF',
         consts=CONSTS, funcs=CORE + [g._dating_job, g.fig_dating], run='print(fig_dating(save_it=False, N=200, R=500))',
         charts=['ats_ch16_dating']),
    dict(name='ATS_ch16_monitoring',
         desc='Real-time monitoring of weekly returns of the Nasdaq 100 and Bitcoin with a CUSUM and the boundary of Chu, '
              'Stinchcombe and White (1996), as discussed by Homm and Breitung (2012), against the first confirmed BSADF '
              'alarm; simulated size of the monitor under i.i.d. and GARCH returns.',
         keywords='monitoring, CUSUM, boundary crossing, real time, Homm-Breitung, Nasdaq 100, Bitcoin',
         consts=CONSTS, funcs=CORE + [g.fig_monitor], run='print(fig_monitor(save_it=False, R=300, Nsize=500))',
         charts=['ats_ch16_monitor']),
    dict(name='ATS_ch16_housing',
         desc='Explosive prices against explosive fundamentals: BSADF with BIC-selected lags and wild-bootstrap critical '
              'values for the log price-to-rent ratio, the log real rent and the log real house price of the United States '
              '(FRED, monthly) and Romania (Eurostat, quarterly).',
         keywords='housing bubble, price-to-rent ratio, fundamentals, GSADF, wild bootstrap, Romania, Case-Shiller',
         consts=CONSTS, funcs=CORE + [g.ro_housing, g.us_housing, g._dating, g.fig_housing],
         run='print(fig_housing(save_it=False, B=199))', charts=['ats_ch16_housing']),
    dict(name='ATS_ch16_episodes',
         desc='PSY date-stamping of five episodes on weekly log prices: S&P 500 and Nasdaq 100 (dot-com), Shanghai Composite '
              '(2015), Bitcoin (2017, 2021) and BET (2007), with Monte Carlo and wild-bootstrap critical values, pointwise '
              'and family-wise over 52 weeks; first confirmed alarms, leads and the falls after the peaks.',
         keywords='PSY, GSADF, BSADF, dot-com, Shanghai 2015, Bitcoin, BET, wild bootstrap, early warning',
         consts=CONSTS, funcs=CORE + [g._episode_job, g.run_episodes, g.fig_episodes],
         run='print(fig_episodes(save_it=False, R=300, B=199))', charts=['ats_ch16_episodes']),
    dict(name='ATS_ch16_lppls_inference',
         desc='LPPLS for the Shanghai 2015 bubble: the confidence indicator (filter of Shu and Zhu 2020, 29 windows) and the '
              'profile likelihood of the critical time for the window ending on 29 May 2015, with its 95% likelihood-ratio '
              'interval.',
         keywords='LPPLS, confidence indicator, critical time, profile likelihood, Shanghai, Filimonov-Sornette',
         consts=CONSTS, funcs=CORE + [g.fig_lppls], run='print(fig_lppls(save_it=False))', charts=['ats_ch16_lppls'],
         extra=['ch16_ci_ssec.csv']),
    dict(name='ATS_ch16_early_warning',
         desc='Early-warning evaluation for falls of 20% within 182 days of the S&P 500 (1993-2026) and Bitcoin (2014-2026): '
              'ROC curves and AUC with moving-block bootstrap intervals of the LPPLS confidence indicator, of BSADF minus its '
              'pointwise critical value and of the trailing one-year return; hit rates, false-alarm rates and precision.',
         keywords='early warning, ROC, AUC, base rate, false alarms, block bootstrap, LPPLS, BSADF',
         consts=CONSTS, funcs=CORE + [g.cached_ci, g.eval_frame, g.fig_evaluation],
         run='print(fig_evaluation(save_it=False, B=199, R=200))', charts=['ats_ch16_evaluation'],
         extra=['ch16_ci_sp500.csv', 'ch16_ci_btc.csv']),
    dict(name='ATS_ch16_ai_screen',
         desc='A GSADF screen of the monthly log prices of all series of the course data: p-values from the wild bootstrap '
              'and from the homoskedastic Monte Carlo null, rejections at 5%, after Holm and after Benjamini-Hochberg.',
         keywords='GSADF, multiple testing, Holm, Benjamini-Hochberg, wild bootstrap, screening, AI',
         consts=CONSTS, funcs=CORE + [g._screen_job, g.fig_ai_case], run='print(fig_ai_case(save_it=False, B=99))',
         charts=['ats_ch16_ai_case']),
]

if __name__ == '__main__':
    build_all(QUANTLETS, 16, 'Explosive roots and bubbles', HERE, data=DATA, submitted=SUBMITTED, install=INSTALL)
