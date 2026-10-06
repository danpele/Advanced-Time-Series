"""
build_quantlets.py -- Quantlet folders of Chapter 15 (ATS): review and project defence
======================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_15/generate_all_charts.py && python3 Quantlets/Ch_15/seminar15.py
      python3 Quantlets/Ch_15/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 15
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import review_core as rc                        # noqa: E402
import course_tour as ct                        # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Tuesday, 6 October 2026'
DATA = ('Daily market data from EODHD (data/market of the ATS repository) and the BNR reference rate; FRED (real GDP, '
        'industrial production, CPI, federal funds rate, Treasury yields); simulated data')
INSTALL = "# numpy, scipy and statsmodels are preinstalled in Colab\n# !pip install statsmodels"
CONSTS = ['import math\nfrom scipy.signal import lfilter', f'SEED = {g.SEED!r}', f'KS = {g.KS!r}',
          f'PS = {g.PS!r}', f'DELTAS = {g.DELTAS!r}']
CORE = [rc.nw_lags, rc.lrv, rc.dm_test, rc.ar1, rc.hac_t, rc.snooping_rates, rc.leakage_r2, rc.dm_power,
        rc.dm_power_approx, rc.p_required]
TOUR = [ct.tour_dependence, ct.tour_forecast, ct.sup_wald_mean, ct.tour_breaks, ct.tour_svar, ct.tour_state_space,
        ct.tour_regimes, ct.tour_var_backtest, ct.local_whittle, ct.tour_long_memory, ct.tour_spectrum,
        ct.tour_conformal, ct.tour_granger, ct.adf_stat, ct.sadf, ct.tour_bubbles]

QUANTLETS = [
    dict(name='ATS_ch15_pitfalls',
         desc='Two failure modes of empirical time series projects, by Monte Carlo: a specification search over K persistent '
              'candidate predictors of a series with no predictability (naive, Bonferroni and max-t family-wise '
              'false-positive rates with HAC t-tests), and predictor selection with look-ahead (out-of-sample R2 after '
              'selection on the whole sample against the training sample).',
         keywords='data snooping, p-hacking, Reality Check, multiple testing, leakage, look-ahead bias, out-of-sample R2',
         consts=CONSTS, funcs=CORE + [g.save, g.fig_snooping, g.fig_leakage],
         run="print(fig_snooping(reps=300))\nprint(fig_leakage(reps=500))",
         charts=['ats_ch15_snooping', 'ats_ch15_leakage']),
    dict(name='ATS_ch15_power',
         desc='Power of the Diebold-Mariano test (Harvey-Leybourne-Newbold version, Newey-West variance) by out-of-sample '
              'length, mean gain and serial dependence of the loss differential, with the large-sample approximation and '
              'the evaluation length needed for 80% power: the power calculation of a pre-registered forecast comparison.',
         keywords='Diebold-Mariano test, power, pre-registration, sample size, long-run variance, forecast evaluation',
         consts=CONSTS, funcs=CORE + [g.save, g.fig_power], run="print(fig_power(reps=500))", charts=['ats_ch15_power']),
    dict(name='ATS_ch15_course_tour',
         desc='The course in one notebook: one short computation per chapter on real data. HAC for squared S&P 500 returns; '
              'random walk against AR(1) for EUR/RON with DM-HLN and Clark-West; a variance break in US GDP growth; a '
              'recursive monetary VAR; a local level for US inflation; a Markov-switching mean for US GDP growth; a '
              'historical-simulation VaR 1% backtest; local Whittle memory of absolute returns; the business-cycle share '
              'of the spectrum of industrial production; split conformal and ACI intervals; Granger tests between the '
              'S&P 500 and the BET; SADF for the Nasdaq 100.',
         keywords='course review, HAC, forecast evaluation, structural break, SVAR, Kalman filter, Markov switching, VaR, '
                  'long memory, spectrum, conformal prediction, Granger causality, bubbles',
         consts=CONSTS, funcs=CORE + TOUR,
         run='\n'.join(f'print({f.__name__}())' for f in TOUR if f.__name__.startswith('tour_')), charts=[]),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar15 as s
    SEMC = [f'{k} = {getattr(s, k)!r}' for k in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'B1', 'B2', 'B4')]
    QUANTLETS.append(dict(
        name='ATS_ch15_seminar',
        desc='Seminar 15 of Advanced Time Series Analysis and Forecasting, a project clinic and defence rehearsal: short '
             'problems across the course (long-run variance, a Diebold-Mariano test by hand, Cholesky responses, the '
             'half-life of an equilibrium error, a Kalman step, a Markov chain, the Kupiec test, GARCH persistence, the '
             'split-conformal quantile, placebo p-values and Holm); mock defences on replication outputs (Meese-Rogoff for '
             'EUR/RON, the term spread, a leakage audit, a rule search on the BET with a max-t bootstrap); a power '
             'calculation for the pre-registration; an AI answer to audit.',
        keywords='seminar, project defence, replication, Diebold-Mariano, Clark-West, HAC, leakage, data snooping, power',
        consts=CONSTS + SEMC,
        funcs=CORE + [s.save, s.a1_lrv_mean, s.a2_dm_by_hand, s.a3_cholesky, s.a4_vecm_halflife, s.a5_kalman, s.a6_markov,
                      s.a7_kupiec, s.a8_garch, s.a9_conformal, s.a10_placebo_holm, s.eurron_monthly, s.b1_meese_rogoff,
                      s.term_spread, s.ols_se, s.b2_term_spread, s.b3_leakage, s.stationary_bootstrap_index,
                      s.b4_ma_search, s.c1_power, s.c2_check],
        run="print(a1_lrv_mean())\nprint(a3_cholesky())\nprint(a5_kalman())\nprint(a7_kupiec())\nprint(a9_conformal())\n"
            "print(b1_meese_rogoff())\nprint(b3_leakage())",
        charts=['ch15_sem_b1']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 15, 'Review and project defence', HERE, data=DATA, submitted=SUBMITTED, install=INSTALL)
