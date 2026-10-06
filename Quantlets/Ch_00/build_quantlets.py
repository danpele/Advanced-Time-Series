"""
build_quantlets.py -- Quantlet folders of Chapter 0 (ATS): refresher and inference for dependent data
=====================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_00/generate_all_charts.py && python3 Quantlets/Ch_00/seminar0.py
      python3 Quantlets/Ch_00/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 0
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import seminar0 as s                            # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('Romanian real GDP and HICP inflation (Eurostat namq_10_gdp, prc_hicp_minr); EUR/RON reference rate (BNR); '
        'S&P 500 and BET daily closes from EODHD (data/market of the ATS repository); US real GDP and Treasury yields '
        '(FRED GDPC1, GS10, TB3MS)')
SIM = 'Simulated data (seed 2026)'
CONSTS = ['from scipy import stats',
          f'SEED = {g.SEED!r}', f'GDP_RO = {g.GDP_RO!r}', f'HICP_RO = {g.HICP_RO!r}', f'START_MACRO = {g.START_MACRO!r}',
          f'START_INFL = {g.START_INFL!r}', f'TARGET_START = {g.TARGET_START!r}', f'TARGET = {g.TARGET!r}',
          f'H_TS = {g.H_TS!r}', f'FIXED_B_GRID = {g.FIXED_B_GRID!r}', f'MA_LENGTHS = {g.MA_LENGTHS!r}',
          f'SB_MEAN_BLOCK = {g.SB_MEAN_BLOCK!r}', 'NUM = {}']
CORE = [g.ro_gdp_growth, g.ro_inflation, g.daily_series, g.term_spread_data, g.save, g.acov_all, g.kernel, g.lrv,
        g.nw_rule, g.ar1_coef, g.andrews_bw, g.llsw_bw, g.ewc_nu, g.ewc_lrv, g.fixed_b_table, g.fixed_b_cv,
        g.mean_inference, g.politis_white, g.mbb_means, g.sb_means, g.sb_indices, g.iid_means, g.ols_hac,
        g.ma_rule_returns, g.reality_check, g.mc_size]
SEM_CONSTS = CONSTS + [f'A2_DATA = {s.A2_DATA!r}', f'A3_DATA = {s.A3_DATA!r}', f'A5_DATA = {s.A5_DATA!r}',
                       f'A8_PVALUES = {s.A8_PVALUES!r}', f'GARCH = {s.GARCH!r}', 'R = {}']
SEM = [s.part_a, s.b1_sp500, s.b2_gdp, s.simulate_ar1, s.size_table, s.b3_size, s.simulate_garch, s.b4_garch,
       s.b5_spurious, s.b6_eurron, s.momentum_rule_returns, s.c1_snooping]

QUANTLETS = [
    dict(name='ATS_ch0_dependence_data',
         desc='The series of Chapter 0 and their dependence: Romanian HICP inflation (annual rate) and real GDP growth '
              '(Eurostat), EUR/RON daily changes (BNR reference rate), S&P 500 daily log returns; sample ACF of six series '
              'with the i.i.d. band and the ratio of the long-run variance to the variance (Newey-West rule of thumb and '
              'Andrews 1991 bandwidth).',
         keywords='autocorrelation, ACF, long-run variance, HICP, GDP, EUR/RON, S&P 500, squared returns, volatility clustering',
         consts=CONSTS, funcs=CORE + [g.fig_data_dashboard, g.fig_acf_panel],
         run='print(fig_data_dashboard())\nprint(fig_acf_panel())', charts=['ats_ch0_data_dashboard', 'ats_ch0_acf_panel']),
    dict(name='ATS_ch0_long_run_variance',
         desc='The long-run variance of a sample mean under AR(1) dependence: theory (1+phi)/(1-phi) against simulation, '
              'and the asymptotic size of the naive 5% t-test; the kernels of Newey and West (1987), Parzen and Andrews '
              '(1991, quadratic spectral) against the truncated kernel; a sample where the truncated estimate is negative.',
         keywords='long-run variance, AR(1), size distortion, Bartlett kernel, Parzen kernel, quadratic spectral kernel, truncated kernel',
         consts=CONSTS, funcs=CORE + [g.fig_lrv_ar1, g.fig_kernels, g.truncated_negative_example],
         run='print(fig_lrv_ar1())\nprint(fig_kernels())\nprint(truncated_negative_example())',
         charts=['ats_ch0_lrv_ar1', 'ats_ch0_kernels'], data=SIM),
    dict(name='ATS_ch0_hac',
         desc='HAC standard errors of a mean as a function of the Bartlett bandwidth for five series, with the Andrews '
              '(1991) AR(1) plug-in bandwidth; fixed-b critical values (Kiefer and Vogelsang 2005) of the Bartlett and '
              'quadratic spectral t-tests by simulation.',
         keywords='HAC, Newey-West, Andrews bandwidth, fixed-b, Kiefer-Vogelsang, critical values, bandwidth choice',
         consts=CONSTS, funcs=CORE + [g.fig_hac_bandwidth, g.fig_fixed_b],
         run='print(fig_hac_bandwidth())\nprint(fig_fixed_b())', charts=['ats_ch0_hac_bandwidth', 'ats_ch0_fixed_b']),
    dict(name='ATS_ch0_size_monte_carlo',
         desc='Monte Carlo of the size of seven 5% tests for a mean under AR(1) dependence (T = 100, 400; phi from 0 to '
              '0.9): naive, Newey-West rule of thumb, Newey-West and QS with Andrews bandwidths, Newey-West with '
              'S = 1.3 sqrt(T) and fixed-b critical values and EWC (Lazarus, Lewis, Stock and Watson 2018), circular '
              'block bootstrap with the Politis-White block length.',
         keywords='Monte Carlo, size distortion, HAR inference, fixed-b, EWC, block bootstrap, AR(1)',
         consts=CONSTS, funcs=CORE + [g.fig_mc_size],
         run='cvtab = fixed_b_table()\nprint(fig_mc_size(cvtab=cvtab))', charts=['ats_ch0_mc_size'], data=SIM),
    dict(name='ATS_ch0_block_bootstrap',
         desc='Block bootstraps of a mean: i.i.d. (Efron), moving-block (Kunsch 1989), circular and stationary (Politis '
              'and Romano 1994) bootstrap of the mean of squared S&P 500 returns, with the automatic block length of '
              'Politis and White (2004, corrected 2009); bootstrap standard error against the block length; standard '
              'errors of the means of six series by method.',
         keywords='block bootstrap, moving-block bootstrap, circular bootstrap, stationary bootstrap, block length, Politis-White',
         consts=CONSTS, funcs=CORE + [g.fig_bootstrap, g.fig_block_length, g.real_data_table],
         run='print(fig_bootstrap())\nprint(fig_block_length())\nprint(pd.DataFrame(real_data_table()).T.round(4))',
         charts=['ats_ch0_bootstrap', 'ats_ch0_block_length']),
    dict(name='ATS_ch0_term_spread',
         desc='Overlapping observations: annualised US real GDP growth over the next four quarters on the 10-year minus '
              '3-month Treasury spread (design of Estrella and Hardouvelis 1991), with classical, White, Hansen-Hodrick, '
              'Newey-West, Andrews and fixed-b standard errors, residual autocorrelation and two subsamples.',
         keywords='term spread, overlapping observations, Hansen-Hodrick, Newey-West, predictive regression, FRED',
         consts=CONSTS, funcs=CORE + [g.fig_term_spread], run='print(fig_term_spread())', charts=['ats_ch0_term_spread'],
         data='US real GDP, 10-year and 3-month Treasury yields (FRED GDPC1, GS10, TB3MS)'),
    dict(name='ATS_ch0_data_snooping',
         desc='Data snooping: the family-wise error of the best of K tests (independent and equicorrelated statistics); '
              'the Reality Check of White (2000) with the stationary bootstrap for 50 moving-average rules on the BET '
              'index against buy-and-hold, 2001-2012 and 2014-2026.',
         keywords='data snooping, multiple testing, family-wise error, Bonferroni, Reality Check, stationary bootstrap, BET, technical rules',
         consts=CONSTS, funcs=CORE + [g.fig_snooping, g.fig_reality_check],
         run='print(fig_snooping())\nprint(fig_reality_check())', charts=['ats_ch0_snooping', 'ats_ch0_reality_check']),
    dict(name='ATS_ch0_ai_discovery',
         desc='AI-for-discovery mini-case: has Romanian HICP inflation averaged the 2.5% BNR target since 2013? Confidence '
              'intervals for the mean by six methods and the size of each test in a Monte Carlo calibrated to the AR(1) '
              'fitted to the series.',
         keywords='inflation target, near unit root, HAR inference, Monte Carlo, size, Romania, HICP',
         consts=CONSTS, funcs=CORE + [g.fig_ai_minicase], run='print(fig_ai_minicase())', charts=['ats_ch0_ai_minicase']),
    dict(name='ATS_ch0_seminar',
         desc='Seminar 0: long-run variances, Newey-West by hand, a negative truncated estimate, moving-block and circular '
              'bootstrap by hand, family-wise error and Holm; S&P 500 mean return with HAC standard errors; Romanian GDP '
              'growth; Monte Carlo of size under AR(1) and GARCH(1,1); replication of Granger and Newbold (1974); block '
              'bootstrap of EUR/RON; Reality Check for BET trading rules.',
         keywords='seminar, HAC, Newey-West, block bootstrap, Monte Carlo, size, spurious regression, Granger-Newbold, data snooping',
         consts=SEM_CONSTS, funcs=CORE + SEM,
         run=('part_a()\nprint({k: R[k] for k in ("A1", "A2", "A3", "A5", "A7", "A8")})\ncvtab = fixed_b_table()\n'
              'print(b1_sp500(cvtab=cvtab))\nprint(b2_gdp(cvtab=cvtab))\nprint(b3_size(cvtab=cvtab))\n'
              'print(b4_garch(cvtab=cvtab))\nprint(b5_spurious(cvtab=cvtab))\nprint(b6_eurron())\nprint(c1_snooping())'),
         charts=['ch0_sem_b1_tstats', 'ch0_sem_b2_gdp', 'ch0_sem_b3_size', 'ch0_sem_b4_garch', 'ch0_sem_b5_spurious',
                 'ch0_sem_b6_eurron']),
]

if __name__ == '__main__':
    build_all(QUANTLETS, chapter=0, chapter_title='Refresher and inference for dependent data', ql_dir=HERE,
              data=DATA, submitted=SUBMITTED)
