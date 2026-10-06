"""
build_quantlets.py -- Quantlet folders of Chapter 6 (ATS): state space models and Bayesian filtering
=====================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_06/generate_all_charts.py && python3 Quantlets/Ch_06/seminar6.py
      python3 Quantlets/Ch_06/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 6
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
DATA = ('FRED (GDPDEF, GDPC1, INDPRO, PAYEMS, W875RX1, CMRMTSPL); Eurostat (prc_hicp_minr, namq_10_gdp); daily S&P 500 '
        'and BET closes from EODHD (data/market of the ATS repository); BNR EUR/RON reference rate')
NODATA = 'Simulated data and FRED GDPDEF'
CONSTS = ['import time', 'from scipy import linalg', f'SEED = {g.SEED!r}', 'LOG2PI = np.log(2 * np.pi)',
          f'KSC_P = np.array({g.KSC_P.tolist()!r})', f'KSC_M = np.array({g.KSC_M.tolist()!r})',
          f'KSC_V = np.array({g.KSC_V.tolist()!r})', f'SV = {g.SV!r}', f'MNZ = {g.MNZ!r}', f'UCSV = {g.UCSV!r}',
          f'TVP = {g.TVP!r}', f'DFM_SERIES = {g.DFM_SERIES!r}', '_sv_cache = {}']
KF = [g.save, g.ssm, g._zrow, g.kalman_filter, g.kalman_smoother, g.big_kappa, g.local_level, g.num_hessian,
      g.fit_local_level, g.us_inflation, g.hicp_index, g.hicp_yoy, g.ro_quarterly_inflation, g.gdp_log, g.returns]
SIMS = [g.simulate_ssm, g.sim_smoother_dk, g.ffbs, g.precision_rw, g.ineff]
SVF = [g.ar1_precision, g.draw_h_ksc, g.draw_s_ksc, g.sv_gibbs, g.garch11, g.systematic_resample, g.pf_sv]
UC = [g.ar2_from_pacf, g.uc_model, g.uc_statsmodels, g.fit_uc, g.bn_arma, g.hamilton_filter, g.trend_cycle,
      g.smooth_trend_model, g.fit_smooth_trend, g.ro_gdp_covid_missing]

QUANTLETS = [
    dict(name='ATS_ch6_kalman_mle',
         desc='A transparent numpy Kalman filter and state smoother for the linear Gaussian state space model with exact '
              'diffuse initialisation (Koopman 1997; Durbin and Koopman 2012), checked against statsmodels; the diffuse '
              'log-likelihood against big-kappa initialisation (US GDP-deflator inflation, Romanian real GDP); exact '
              'diffuse ML of the local level model; the pile-up of the signal-to-noise ratio at zero by simulation.',
         keywords='state space, Kalman filter, smoother, exact diffuse initialisation, maximum likelihood, pile-up, local level',
         consts=CONSTS, funcs=KF + [g.llt_model, g.fit_llt, g.fig_diffuse, g.ll_profile, g.fig_pileup, g.fig_local_level],
         run='print(fig_local_level())\nprint(fig_diffuse()["exact"])\nprint(fig_pileup(reps=2000))',
         charts=['ats_ch6_local_level', 'ats_ch6_diffuse', 'ats_ch6_pileup']),
    dict(name='ATS_ch6_simulation_smoother',
         desc='Three samplers of the state posterior of a local level model (US inflation): Carter-Kohn forward filtering '
              'backward sampling, the Durbin-Koopman (2002) mean-correction simulation smoother and the precision sampler '
              '(Chan and Jeliazkov 2009); a Gibbs sampler for the two variances with inverse-gamma priors.',
         keywords='simulation smoother, FFBS, Carter-Kohn, Durbin-Koopman, precision sampler, Gibbs sampling, Bayesian',
         consts=CONSTS, funcs=KF + SIMS + [g.fig_simsmoother, g.gibbs_local_level, g.fig_gibbs_ll],
         run='print(fig_simsmoother(draws=500))\nprint(fig_gibbs_ll(draws=1500, burn=300))',
         charts=['ats_ch6_simsmoother', 'ats_ch6_gibbs_ll']),
    dict(name='ATS_ch6_stochastic_volatility',
         desc='Stochastic volatility of daily S&P 500 and BET returns, 2016-2026: the Kim, Shephard and Chib (1998) '
              'seven-component mixture against the log chi-square(1) law; the KSC Gibbs sampler with the precision sampler '
              'for the log-volatility path; GARCH(1,1) by ML; the bootstrap particle filter likelihood; particle marginal '
              'Metropolis-Hastings (Andrieu, Doucet and Holenstein 2010) against the Gibbs posterior.',
         keywords='stochastic volatility, KSC mixture, Gibbs sampler, particle filter, PMMH, GARCH, S&P 500, BET',
         consts=CONSTS, funcs=KF + SIMS + SVF + [g.fig_ksc, g.fig_sv, g.fig_pf, g.pmmh_sv, g.fig_pmmh],
         run='print(fig_ksc())\nprint(fig_sv(draws=4000, burn=500)["sp500"])\nprint(fig_pf(reps=20))\n'
             'print(fig_pmmh(n_iter=1000, N=600, draws=4000))',
         charts=['ats_ch6_ksc', 'ats_ch6_sv', 'ats_ch6_pf', 'ats_ch6_pmmh']),
    dict(name='ATS_ch6_nonlinear_filters',
         desc='Nonlinear filtering: the unscented transform (Julier and Uhlmann 2004) against first-order linearisation '
              '(EKF) for the volatility exp(h/2); bootstrap and auxiliary (Pitt and Shephard 1999) particle filters against '
              'the exact Kalman likelihood of a local level model for US inflation.',
         keywords='extended Kalman filter, unscented Kalman filter, particle filter, auxiliary particle filter, likelihood',
         consts=CONSTS, funcs=KF + [g.systematic_resample, g.unscented, g.fig_ukf, g.pf_local_level, g.fig_pf_check],
         data=NODATA, run='print(fig_ukf())\nprint(fig_pf_check(reps=50))', charts=['ats_ch6_ukf', 'ats_ch6_pf_check']),
    dict(name='ATS_ch6_tvp_inflation',
         desc='Time-varying-parameter regression of Romanian on euro-area quarterly HICP inflation since 2005Q4 (Eurostat): '
              'random-walk intercept and slope, constant seasonal coefficients as exact diffuse states, numpy against '
              'statsmodels; LR test of a constant slope with a parametric bootstrap p-value; rolling OLS for comparison.',
         keywords='time-varying parameters, TVP regression, inflation, Romania, euro area, boundary test, bootstrap',
         consts=CONSTS, funcs=KF + [g.simulate_ssm, g.quarterly_inflation, g.seasonal_dummies, g.tvp_data, g.tvp_model,
                                    g.fit_tvp, g.tvp_statsmodels, g.fig_tvp],
         run='print(fig_tvp(B=99))', charts=['ats_ch6_tvp']),
    dict(name='ATS_ch6_dfm_ragged_edge',
         desc='A one-factor dynamic factor model of the four US coincident indicators (FRED: INDPRO, PAYEMS, W875RX1, '
              'CMRMTSPL), monthly growth since 1990: two-step estimator of Doz, Giannone and Reichlin (2011) and the Kalman '
              'smoother with the univariate treatment of the observation vector at the ragged edge.',
         keywords='dynamic factor model, state space, ragged edge, missing data, Kalman smoother, nowcasting',
         consts=CONSTS, funcs=[g.save, g.dfm_data, g.dfm_two_step, g.fig_dfm], run='print(fig_dfm())', charts=['ats_ch6_dfm']),
    dict(name='ATS_ch6_trend_cycle',
         desc='Trend-cycle decompositions: replication of Morley, Nelson and Zivot (2003) on US real GDP 1947Q1-1998Q2 '
              '(UC0 against UC-UR, the Beveridge-Nelson cycle of an ARIMA(2,1,2), the Hamilton 2018 cycle); the Romanian '
              'output gap since 2000 with random-walk and smooth trends, filtered against smoothed gaps.',
         keywords='Beveridge-Nelson, unobserved components, output gap, Morley-Nelson-Zivot, Hamilton filter, Romania',
         consts=CONSTS, funcs=KF + UC + [g.fig_mnz, g.fig_ro_gap], run='print(fig_mnz())\nprint(fig_ro_gap())',
         charts=['ats_ch6_mnz', 'ats_ch6_ro_gap']),
    dict(name='ATS_ch6_ucsv_inflation',
         desc='Trend inflation with stochastic volatility (UC-SV, Stock and Watson 2007): US GDP-deflator inflation since '
              '1953 and Romanian HICP inflation since 2001 (with quarterly seasonal dummies); Gibbs sampler with the '
              'precision sampler and the KSC mixture; the BNR target band.',
         keywords='trend inflation, UC-SV, stochastic volatility, Gibbs sampler, Romania, inflation targeting',
         consts=CONSTS, funcs=KF + [g.precision_rw, g.draw_s_ksc, g.ucsv_gibbs, g.fig_ucsv_us, g.fig_ucsv_ro],
         run='print(fig_ucsv_us(draws=4000, burn=1000))\nprint(fig_ucsv_ro(draws=4000, burn=1000))',
         charts=['ats_ch6_ucsv_us', 'ats_ch6_ucsv_ro']),
    dict(name='ATS_ch6_ai_robustness',
         desc='AI mini-case: how much does the US UC-SV trend in 2021-2026 depend on gamma, the fixed variance of the '
              'log-volatility shocks (0.05, 0.1, 0.2, 0.4)?',
         keywords='robustness, UC-SV, trend inflation, tuning parameter, AI for science',
         consts=CONSTS, funcs=KF + [g.precision_rw, g.draw_s_ksc, g.ucsv_gibbs, g.fig_ai_case],
         run='print(fig_ai_case(draws=3000, burn=1000))', charts=['ats_ch6_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar6 as s
    SEMC = [f'A1Y, A1E, A1H = np.array({s.A1Y.tolist()!r}), {s.A1E!r}, {s.A1H!r}', f'A4 = {s.A4!r}', f'A5 = {s.A5!r}',
            f'A7H, A7Y, A7U = np.array({s.A7H.tolist()!r}), {s.A7Y!r}, {s.A7U!r}',
            f'A8X, A8Y, A8E, A8H = np.array({s.A8X.tolist()!r}), {s.A8Y!r}, {s.A8E!r}, {s.A8H!r}', f'A9 = {s.A9!r}',
            f'A10Q = {s.A10Q!r}', '_cache = {}']
    QUANTLETS.append(dict(
        name='ATS_ch6_seminar',
        desc='Seminar 6 of Advanced Time Series Analysis and Forecasting: the exact diffuse Kalman filter by hand, one '
             'backward-sampling step, moments of the SV model, one bootstrap particle-filter step, the Beveridge-Nelson '
             'cycle; Romanian trend growth by a local linear trend; TVP regressions for Hungary and Poland; stochastic '
             'volatility of EUR/RON by Gibbs and by the particle filter; the real-time Romanian output gap; Romanian trend '
             'inflation and the BNR target; an AI answer to audit.',
        keywords='seminar, state space, Kalman filter, stochastic volatility, particle filter, output gap, Romania',
        consts=CONSTS + SEMC, data=DATA,
        funcs=KF + SIMS + SVF + UC + [g.llt_model, g.fit_llt, g.quarterly_inflation, g.seasonal_dummies, g.tvp_data,
                                      g.tvp_model, g.fit_tvp, g.ucsv_gibbs,
                                      s.a1_diffuse, s.a2_concentrated, s.a3_ffbs, s.a4_ig, s.a5_sv_moments, s.a6_qml,
                                      s.a7_pf_step, s.a8_apf, s.a9_bn, s.a10_ima, s.b1_llt, s.b2_tvp, s.b3_sv_eurron,
                                      s.b4_pf, s.b5_realtime, s.c1_anchor, s.c2_check],
        run="print(a1_diffuse())\nprint(a3_ffbs())\nprint(a5_sv_moments())\nprint(a7_pf_step())\nprint(a9_bn())\n"
            "print(b1_llt())\nprint(b3_sv_eurron(draws=4000, burn=1000))",
        charts=['ch6_sem_b1', 'ch6_sem_b3']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 6, 'State space models and Bayesian filtering', HERE, data=DATA, submitted=SUBMITTED)
