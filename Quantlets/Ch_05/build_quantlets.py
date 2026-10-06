"""
build_quantlets.py -- Quantlet folders of Chapter 5 (ATS): Bayesian VAR, factor models and nowcasting
=======================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_05/generate_all_charts.py && python3 Quantlets/Ch_05/seminar5.py
      python3 Quantlets/Ch_05/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 5
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
DATA = ('FRED (St. Louis Fed): 117 FRED-MD series distributed by FRED, read one by one as public CSV files, with the '
        'FRED-MD transformation codes of McCracken and Ng (2016); USREC, CUMFNS, UNRATE, INDPRO. Eurostat: Romanian '
        'industrial production, retail trade, construction, unemployment, business and consumer survey balances, '
        'euro-area industrial production, quarterly real GDP; BNR reference rate (seminar)')
CONSTS = ['import hashlib', 'from scipy import linalg, special', f'SEED = {g.SEED!r}', f'FRED_MD_URL = {g.FRED_MD_URL!r}',
          f'END_M = {g.END_M!r}', f'FRED_SPEC = {g.FRED_SPEC!r}', f'SPREADS = {g.SPREADS!r}', f'TCODE = {g.TCODE!r}',
          f'GROUP = {g.GROUP!r}', f'GROUPS = {g.GROUPS!r}', f'SMALL = {g.SMALL!r}', f'MEDIUM = {g.MEDIUM!r}',
          f'FAST_GROUPS = {g.FAST_GROUPS!r}', f'BGR = {g.BGR!r}', f'GLP = {g.GLP!r}', f'SW = {g.SW!r}', f'BBE = {g.BBE!r}',
          f'RO_SPEC = {g.RO_SPEC!r}', f'RO_GDP = {g.RO_GDP!r}', f'RO = {g.RO!r}', 'MM = np.array([1, 2, 3, 2, 1]) / 3.0',
          f'BRIDGE = {g.BRIDGE!r}', f'MIDAS_X = {g.MIDAS_X!r}', f'FAVAR_SHOW = {g.FAVAR_SHOW!r}', '_FILES = {}']
DATAF = [g.cached, g.save, g.fred_md_raw, g.fred_md_official, g.transform, g.remove_outliers, g.fred_md_panel,
         g.bvar_levels, g.large_names, g.ro_raw, g.ro_panel]
CORE = [g.lagmat, g.ar_var, g.minnesota, g.soc_dummies, g.dio_dummies, g.niw_post, g.niw_logml, g.gamma_pars,
        g.bvar_setup, g.glp_logpost, g.glp_optimize, g.bvar_fit, g.companion_roots, g.var_forecast, g.niw_draw,
        g.irf_shock, g.recursive_impact, g.band_plot, g.plain_log_axis, g.patch, g.recessions]
FACT = [g.em_pca, g.bai_ng]
BGRF = [g.bgr_systems, g.bgr_scale, g.bgr_post, g.insample_msfe, g.bgr_lambda, g.bgr_forecasts, g.rel_msfe, g.bgr_ordering]
DIF = [g.di_target, g.bic_ols, g.di_forecasts, g.di_rel]
FAVF = [g.favar_data, g.favar_estimate, g.ols_var, g.favar_irf_obs, g.favar_run]
NOWF = [g.mshift, g.ro_vintage, g.dfm_fit, g.dfm_matrices, g.kalman_dfm, g.dfm_nowcast, g.dfm_em_nowcast, g.ar_nowcast,
        g.fill_ar, g.quarter_agg, g.bridge_nowcast, g.almon, g.midas_design, g.midas_fit, g.midas_nowcast,
        g.nowcast_eval, g.nowcast_rmse, g.news_decomposition]

QUANTLETS = [
    dict(name='ATS_ch5_bvar',
         desc='The curse of dimensionality: one-step forecasts from a stationary VAR(1) with common dynamics, T = 120, '
              'estimated as a VAR(4) by OLS, as a Minnesota BVAR with the tightness chosen by the marginal likelihood '
              '(natural conjugate Normal-inverse-Wishart prior) and as a univariate AR(4), for 2 to 24 variables.',
         keywords='Bayesian VAR, Minnesota prior, curse of dimensionality, shrinkage, marginal likelihood, simulation',
         consts=CONSTS, funcs=CORE + [g.sim_var, g.fig_curse], run='print(fig_curse(reps=50))', charts=['ats_ch5_curse']),
    dict(name='ATS_ch5_bayes',
         desc='Bayesian inference refresher: precision-weighted updating of the AR(1) coefficient of the US unemployment '
              'rate under a N(1, 0.2^2) prior for 24 and 240 months; a one-at-a-time Gibbs sampler for a regression of '
              'IP growth on capacity utilisation with raw and centred regressor, four chains, traces, autocorrelation, '
              'effective sample size, R-hat and the Geweke statistic.',
         keywords='Bayesian inference, conjugate prior, Gibbs sampling, MCMC diagnostics, effective sample size, R-hat, Geweke',
         consts=CONSTS, funcs=[g.fig_conjugate, g.gibbs_regression, g.acf, g.ess, g.rhat, g.geweke, g.gibbs_data, g.fig_gibbs],
         run='print(fig_conjugate())\nprint(fig_gibbs())', charts=['ats_ch5_conjugate', 'ats_ch5_gibbs']),
    dict(name='ATS_ch5_large_bvar',
         desc='Large Bayesian VARs: Banbura, Giannone and Reichlin (2010) on a FRED-MD-format panel (SMALL, MEDIUM, LARGE '
              'systems, p = 13, rolling 10-year windows, lambda by the in-sample fit rule, sum-of-coefficients prior), '
              'Giannone, Lenza and Primiceri (2015) hyperparameters by the marginal likelihood, the fit/out-of-sample '
              'trade-off, responses to a 100 bp funds-rate shock with posterior bands, a common-volatility proxy.',
         keywords='large Bayesian VAR, Minnesota prior, Normal-inverse-Wishart, dummy observations, marginal likelihood, FRED-MD, monetary policy',
         consts=CONSTS, funcs=DATAF + CORE + BGRF + [g.fig_lambda, g.fig_tradeoff, g.fig_bgr, g.fig_bvar_irf, g.fig_common_vol],
         run='print(fig_lambda())\nprint(fig_tradeoff(step=12))\nprint(fig_bgr(step=12)["lam_fit"])\nprint(fig_bvar_irf(ndraw=200)["LARGE"])\nprint(fig_common_vol())',
         charts=['ats_ch5_lambda', 'ats_ch5_tradeoff', 'ats_ch5_bgr', 'ats_ch5_bvar_irf', 'ats_ch5_common_vol']),
    dict(name='ATS_ch5_factors',
         desc='Approximate factor models on a FRED-MD-format panel 1960-2026: principal components with EM imputation, '
              'McCracken-Ng outlier rule, Bai-Ng (2002) criteria, marginal R2 by group, diffusion-index forecasts of IP, '
              'employment and CPI inflation (Stock and Watson 2002, JBES) against an AR benchmark.',
         keywords='factor model, principal components, FRED-MD, Bai-Ng, diffusion index, forecasting, EM algorithm',
         consts=CONSTS, funcs=DATAF + CORE + FACT + DIF + [g.fig_factors, g.fig_mr2, g.fig_di],
         run='print(fig_factors())\nprint(fig_mr2())\nprint(fig_di(step=12)["eval1"])',
         charts=['ats_ch5_factors', 'ats_ch5_mr2', 'ats_ch5_di']),
    dict(name='ATS_ch5_favar',
         desc='FAVAR of Bernanke, Boivin and Eliasz (2005): three factors and the federal funds rate, two-step estimation '
              'with slow-moving factors, VAR(13), 1960:1-2001:8 and 1960:1-2007:12, responses of nine series to a 25 bp '
              'shock with residual-bootstrap bands.',
         keywords='FAVAR, factor-augmented VAR, monetary policy, price puzzle, principal components, bootstrap',
         consts=CONSTS, funcs=DATAF + CORE + FAVF + [g.fig_favar], run='print(fig_favar(B=100)["INDPRO"])',
         charts=['ats_ch5_favar']),
    dict(name='ATS_ch5_nowcast',
         desc='Nowcasting Romanian GDP growth from 11 monthly Eurostat indicators: bridge equations, ADL-MIDAS with '
              'exponential Almon weights, a two-factor dynamic factor model with the Mariano-Murasawa aggregation '
              '(two-step and EM with statsmodels DynamicFactorMQ), pseudo-real-time evaluation 2013-2026 with stylised '
              'release lags, the 2026Q3 nowcast and its news decomposition, robustness of the ranking.',
         keywords='nowcasting, mixed frequency, MIDAS, bridge equation, dynamic factor model, Kalman filter, news, Romania, GDP',
         consts=CONSTS, funcs=DATAF + CORE + FACT + NOWF + [g.fig_ro_data, g.fig_midas, g.fig_nowcast, g.fig_news, g.fig_ai_case],
         run='print(fig_ro_data())\nprint(fig_midas())\nprint(fig_nowcast(em=False)["rmse"])\nprint(fig_news(em=True)["by"])\nprint(fig_ai_case()["n_better"])',
         charts=['ats_ch5_ro_data', 'ats_ch5_midas', 'ats_ch5_nowcast', 'ats_ch5_news', 'ats_ch5_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar5 as s
    SEMC = [f'A1 = {s.A1!r}', f'A2 = {s.A2!r}', f'A3 = {s.A3!r}', f'A4 = {s.A4!r}', f'A5 = {s.A5!r}', f'A6 = {s.A6!r}',
            f'A7 = {s.A7!r}', f'A8 = {s.A8!r}', f'RO_BVAR = {s.RO_BVAR!r}']
    QUANTLETS.append(dict(
        name='ATS_ch5_seminar',
        desc='Seminar 5 of Advanced Time Series Analysis and Forecasting: conjugate updating and empirical Bayes, '
             'Minnesota prior variances, Gibbs diagnostics, dummy observations, principal components, Bai-Ng, the '
             'Mariano-Murasawa weights, news; hyperparameters by marginal likelihood, a Romanian BVAR, factors on three '
             'samples, FAVAR and the number of factors, nowcasts of Romanian GDP and the news of September 2026; an AI '
             'answer to audit.',
        keywords='seminar, Bayesian VAR, Minnesota prior, factor model, FAVAR, nowcasting, MIDAS, news, Romania',
        consts=CONSTS + SEMC,
        funcs=DATAF + CORE + FACT + BGRF + FAVF + NOWF + [s.a1_conjugate, s.a2_minnesota, s.a3_mcmc, s.a4_dummies,
                                                         s.a5_pca, s.a6_bai_ng, s.a7_mm, s.a8_news, s.b1_glp,
                                                         s.ro_bvar_data, s.b2_ro_bvar, s.b3_factor_samples, s.b4_favar_k,
                                                         s.b5_nowcast_q2, s.b6_news, s.c1_surveys, s.c2_check],
        run="print(a1_conjugate())\nprint(a3_mcmc())\nprint(a5_pca())\nprint(a7_mm())\nprint(b1_glp())\nprint(b3_factor_samples())\nprint(b5_nowcast_q2())",
        charts=['ch5_sem_b1', 'ch5_sem_b3', 'ch5_sem_b5']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 5, 'Bayesian VAR, factor models and nowcasting', HERE, data=DATA, submitted=SUBMITTED)
