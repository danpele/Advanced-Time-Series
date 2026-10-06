"""
build_quantlets.py -- Quantlet folders of Chapter 9 (ATS): VaR, ES and backtesting
==================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_09/generate_all_charts.py && python3 Quantlets/Ch_09/seminar9.py
      python3 Quantlets/Ch_09/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 9
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import risk_core as r                           # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('EODHD daily closes of the S&P 500, DAX, BET, Bitcoin and VIX (data/market of the ATS repository); EUR/RON: '
        'official BNR reference rate')
NUMBA = '''import pickle
from scipy import special, integrate
try:                                    # numba accelerates the recursions; without it the code runs in plain Python
    from numba import njit as _njit

    def njit(*args, **kw):
        kw.pop('cache', None)           # no on-disk cache for functions defined in a notebook
        return _njit(*args, **kw)
except ImportError:
    def njit(*args, **kw):
        if args and callable(args[0]):
            return args[0]
        return lambda f: f'''
CONSTS = [NUMBA, f'SEED = {g.SEED!r}', f'END = {g.END!r}', f'ASSETS = {g.ASSETS!r}', f'LAB = {g.LAB!r}',
          f'MODELS = {g.MODELS!r}', f'FZ_NAMES = {g.FZ_NAMES!r}', f'STRESS = {g.STRESS!r}', f'PZC_TABLE = {g.PZC_TABLE!r}',
          f'PZC_GOF = {g.PZC_GOF!r}', f'EM_DESIGN = {g.EM_DESIGN!r}', "CACHE = ''", '_MEM = {}',
          f'CAVIAR_K = {r.CAVIAR_K!r}', f'SPEC_ID = {r.SPEC_ID!r}', f'FZ_MODELS = {r.FZ_MODELS!r}', f'FZ_NPAR = {r.FZ_NPAR!r}']
CORE = [r.pinball, r.fz0, r.murphy_quantile, r.skewt_consts, r.skewt_logpdf, r.skewt_ppf, r.skewt_var_es, r.skewt_fit,
        r.t_std_var_es, r.normal_var_es, r.rolling_hs, r.garch_path, r.garch_negll, r.garch_fit, r.garch_sigma,
        r.arma_bic, r.arma_onestep, r.caviar_path, r.caviar_var, r.caviar_rq, r.caviar_fit, r.num_grad_path,
        r.qr_bandwidth, r.caviar_se, r.dq_test, r._ind, r.fz_paths, r.fz_init, r.fz_valid, r.fz_objective,
        r.fz_candidates, r.fz_fit, r.fz_forecast, r.es_regression, r.kupiec, r.christoffersen, r.durations,
        r.cp_duration_test, r.ols_wald, r.pzc_gof, r.mcneil_frey, r.nw_lrv, r.dm_test, r.mcs, r.extremal_index,
        r.aci_levels]
DATAF = [g.save, g.returns, g.cached, g.shade_stress, g.pzc_models, g.run_asset, g.oos_losses]
BASE = DATAF + CORE

QUANTLETS = [
    dict(name='ATS_ch9_scoring',
         desc='Scoring functions for VaR and ES: expected pinball and FZ0 losses of a Student t(5) with their minimisers, '
              'the level sets of the quantile and of ES under mixing (why ES alone is not elicitable), and a Murphy diagram '
              '(Ehm et al. 2016) of three VaR 2.5% forecasts of the S&P 500, 2000-2016.',
         keywords='elicitability, consistent scoring function, pinball loss, FZ0 loss, Fissler-Ziegel, Murphy diagram, expected shortfall',
         consts=CONSTS, funcs=BASE + [g.fig_fz0_contour, g._cdf_pe, g.mix_var_es, g.fig_level_sets, g.fig_murphy],
         run='print(fig_fz0_contour())\nprint(fig_level_sets())\nprint(fig_murphy())',
         charts=['ats_ch9_fz0_contour', 'ats_ch9_level_sets', 'ats_ch9_murphy']),
    dict(name='ATS_ch9_caviar',
         desc='CAViaR (Engle and Manganelli 2004): SAV, asymmetric slope, indirect GARCH and adaptive specifications for the '
              'S&P 500 VaR 1% with the design of the paper (2,892 in-sample and 500 out-of-sample days, ending 18 September '
              '2026); random-search plus simplex/quasi-Newton estimation, asymptotic standard errors, out-of-sample DQ test, '
              'news impact curves.',
         keywords='CAViaR, quantile regression, value at risk, DQ test, news impact curve, S&P 500',
         consts=CONSTS, funcs=BASE + [g.em_sample, g.caviar_table, g.fig_caviar, g.fig_nic],
         run='print(fig_caviar())\nprint(fig_nic())', charts=['ats_ch9_caviar', 'ats_ch9_nic']),
    dict(name='ATS_ch9_pzc',
         desc='Replication of Patton, Ziegel and Chen (2019), Section 5, on our data: ten models for VaR and ES (rolling '
              'windows, ARMA-GARCH with Normal, skewed-t and empirical innovations, GAS-2F, GAS-1F, GARCH-FZ, Hybrid by FZ0 '
              'minimisation), S&P 500 estimated on 1990-1999 and evaluated on 2000-2016 (Tables 8, 9, S5); the GAS-1F '
              'forecasts 2000-2026.',
         keywords='expected shortfall, value at risk, FZ0 loss, GAS model, semiparametric, Diebold-Mariano, replication',
         consts=CONSTS, funcs=BASE + [g.pzc_replication, g.fig_pzc_paths, g.fig_pzc_table, g.fig_dm, g.fig_overview],
         run="print(fig_pzc_table())\nprint(fig_pzc_paths())\nprint(fig_dm())\nprint(fig_overview())",
         charts=['ats_ch9_pzc_table', 'ats_ch9_pzc_paths', 'ats_ch9_dm', 'ats_ch9_overview']),
    dict(name='ATS_ch9_esreg',
         desc='Joint linear regression of the 2.5% quantile and expected shortfall of daily S&P 500 returns on the VIX of the '
              'previous close, 2000-2026 (Dimitriadis and Bayer 2019), by FZ0 minimisation, with moving-block bootstrap '
              'standard errors.',
         keywords='expected shortfall regression, quantile regression, VIX, FZ0 loss, block bootstrap',
         consts=CONSTS, funcs=BASE + [g.fig_esreg], run='print(fig_esreg(B=50))', charts=['ats_ch9_esreg']),
    dict(name='ATS_ch9_backtests',
         desc='Backtests of VaR and ES 2.5% for ten models and five assets (S&P 500, DAX, BET, EUR/RON, Bitcoin), parameters '
              'fixed on the first ten years: Kupiec, Christoffersen, duration-based (Christoffersen and Pelletier 2004), DQ, '
              'PZC goodness-of-fit regressions, McNeil-Frey; size of the Kupiec and DQ tests under estimation risk by Monte Carlo.',
         keywords='backtesting, conditional calibration, duration test, DQ test, estimation risk, expected shortfall',
         consts=CONSTS, funcs=BASE + [g.backtest_table, g.fig_backtests, g.fig_durations, g.sim_garch, g.fig_estrisk_mc],
         run='print(fig_backtests()["pass_both"])\nprint(fig_durations())\nprint(fig_estrisk_mc(reps=100))',
         charts=['ats_ch9_backtests', 'ats_ch9_durations', 'ats_ch9_estrisk_mc']),
    dict(name='ATS_ch9_comparison',
         desc='Comparison of ten VaR/ES models by FZ0 loss in the stress periods 2008, 2020, 2022 and 2025 and over the whole '
              'out-of-sample period, 90% model confidence sets (Hansen, Lunde and Nason 2011), and the robustness of the '
              'winner across assets, levels and periods.',
         keywords='model confidence set, FZ0 loss, stress periods, forecast comparison, expected shortfall',
         consts=CONSTS, funcs=BASE + [g.comparison, g.fig_stress, g.fig_mcs, g.fig_ai_case],
         run='print(fig_stress()["best"])\nprint(fig_mcs())\nprint(fig_ai_case()["wins"])',
         charts=['ats_ch9_stress', 'ats_ch9_mcs', 'ats_ch9_ai_case']),
    dict(name='ATS_ch9_horizon',
         desc='10-day VaR 1% of the S&P 500 by filtered historical simulation from a GJR-GARCH(1,1) against the '
              'square-root-of-time rule, 2001-2026, and a non-overlapping backtest.',
         keywords='square-root-of-time rule, multi-period VaR, filtered historical simulation, GJR-GARCH, overlapping observations',
         consts=CONSTS, funcs=BASE + [g.fhs_hday, g.fig_sqrt], run='print(fig_sqrt())', charts=['ats_ch9_sqrt']),
    dict(name='ATS_ch9_modelrisk',
         desc='Model risk: risk ratio of six standard VaR 1% models (HS, Normal, EWMA, GARCH-N, GARCH-t, FHS) for the S&P 500 '
              'and the BET (Danielsson et al. 2016); estimation risk: parametric bootstrap intervals of GARCH-t ES 2.5% '
              'forecasts.',
         keywords='model risk, risk ratio, estimation risk, bootstrap, expected shortfall, GARCH',
         consts=CONSTS, funcs=BASE + [g.six_models, g.fig_riskratio, g.fig_es_ci],
         run='print(fig_riskratio()["sp500"]["med"])\nprint(fig_es_ci(B=40)["rel_med"])', charts=['ats_ch9_riskratio', 'ats_ch9_es_ci']),
    dict(name='ATS_ch9_extremes',
         desc='Extremal index (Ferro and Segers 2003 intervals estimator) of daily losses above their 95% quantile, raw and '
              'GARCH-filtered, for the S&P 500, DAX, BET, EUR/RON and Bitcoin.',
         keywords='extremal index, clusters of extremes, extreme value theory, GARCH filtering, McNeil-Frey',
         consts=CONSTS, funcs=BASE + [g.fig_extremal], run='print(fig_extremal())', charts=['ats_ch9_extremal']),
    dict(name='ATS_ch9_conformal',
         desc='Adaptive conformal inference (Gibbs and Candes 2021) on top of a Normal GARCH VaR 1% for Bitcoin and the BET, '
              '2016-2026: rolling hit rates, Kupiec and conditional coverage tests.',
         keywords='adaptive conformal inference, value at risk, calibration, GARCH, Bitcoin, BET',
         consts=CONSTS, funcs=BASE + [g.conformal_base, g.fig_conformal], run='print(fig_conformal())', charts=['ats_ch9_conformal']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar9 as s
    SEMC = [f'A1 = {s.A1!r}', f'A3 = {s.A3!r}', f'A4 = {s.A4!r}', f'A5 = {s.A5!r}', f'A6 = {s.A6!r}', f'A7 = {s.A7!r}',
            f'A8 = {s.A8!r}']
    SEMF = [g.em_sample, g.caviar_table, g.pzc_replication, g.comparison, g.fhs_hday, g.conformal_base, g._cdf_pe, g.mix_var_es]
    QUANTLETS.append(dict(
        name='ATS_ch9_seminar',
        desc='Seminar 9 of Advanced Time Series Analysis and Forecasting: pinball consistency, ES under mixing, FZ0 by hand, '
             'durations, the square-root-of-time rule under GARCH, CAViaR recursions, ES backtests and comparative zones; '
             'CAViaR for the S&P 500 and the BET, the Patton-Ziegel-Chen replication, the DAX to 2026, model confidence sets '
             'for Bitcoin and EUR/RON in stress periods, 10-day VaR of the DAX; adaptive conformal correction of the BET '
             'VaR; an AI answer to audit.',
        keywords='seminar, VaR, expected shortfall, CAViaR, FZ0 loss, backtesting, model confidence set, conformal',
        consts=CONSTS + SEMC,
        funcs=BASE + SEMF + [s.a1_pinball, s.a2_mixture, s.a3_fz0, s.a4_durations, s.a5_sqrt, s.a6_caviar, s.a7_es_tests,
                             s.a8_zones, s.b1_caviar_sp500, s.b2_caviar_bet, s.b3_pzc, s.b4_dax, s.b5_mcs, s.b6_dax_10day,
                             s.c1_conformal, s.c2_check],
        run="print(a1_pinball())\nprint(a3_fz0())\nprint(a5_sqrt())\nprint(a7_es_tests())\nprint(b1_caviar_sp500())\nprint(b3_pzc())\nprint(b5_mcs())",
        charts=['ch9_sem_b1', 'ch9_sem_b3', 'ch9_sem_b5']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 9, 'VaR, ES and backtesting: elicitability, scoring and model risk', HERE, data=DATA, submitted=SUBMITTED)
