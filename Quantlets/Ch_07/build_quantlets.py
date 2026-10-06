"""
build_quantlets.py -- Quantlet folders of Chapter 7 (ATS): regime-switching models
==================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_07/generate_all_charts.py && python3 Quantlets/Ch_07/seminar7.py
      python3 Quantlets/Ch_07/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 7
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_data as AD                           # noqa: E402
import generate_all_charts as g                 # noqa: E402
import ms_core as m                             # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('Hamilton (1989) real GNP data and Filardo (1994) industrial production data, both distributed with statsmodels; '
        'FRED: GDPC1, UNRATE, USRECQ, USREC; Eurostat: Romanian real GDP (namq_10_gdp) and HICP (prc_hicp_minr); '
        'EODHD daily closes of the S&P 500 and the BET (data/market); EUR/RON: ECB reference rate to June 2005, BNR '
        'reference rate from July 2005')
CONSTS = ['import math', f'SEED = {g.SEED!r}', f'RO_HICP = {g.RO_HICP!r}', f'RO_GDP = {g.RO_GDP!r}', f'US = {g.US!r}',
          f'MARKET = {g.MARKET!r}', f'EVENTS_EURRON = {g.EVENTS_EURRON!r}', '_FILES = {}']
CORE = [m.ergodic, m.durations, m.simulate_chain, m.hamilton_filter, m.kim_smoother, m.ffbs, m.lag_design, m.msr_logf,
        m._wls_shared, m.em_msr, m.order_regimes, m.best_em, m.info_criteria, m.linear_ar, m.msr_pack, m.msr_unpack,
        m.msr_ml, m.num_hessian, m.num_jacobian, m.expanded_states, m.msm_logf, m.expand_P, m.msm_unpack,
        m.expanded_init, m.msm_filter, m.msm_negll, m.msm_fit, m.var_design, m.msvar_logf, m.em_msvar, m.regime_irf,
        m.msgarch_unpack, m.msgarch_filter, m.msgarch_fit, m.gibbs_ms, m.msr_forecast, m.mixture_logscore,
        m.mixture_pit, m.qps, m.concordance, m.gph, m.acf]
DATAF = [AD.read_ecb, g.cached, g.save, g.hamilton_gnp, g.filardo_data, g.us_gdp, g.us_unemp_q, g.ro_gdp, g.ro_inflation,
         g.weekly_returns, g.eurron_daily, g.shade, g.patch]
BASE = DATAF + CORE

QUANTLETS = [
    dict(name='ATS_ch7_hamilton',
         desc='Hamilton (1989): the switching-mean AR(4) of US real GNP on Hamilton\'s data (1951Q2-1984Q4), estimated by '
              'numerical maximum likelihood on the expanded state with a numpy Hamilton filter and Kim smoother and with '
              'statsmodels MarkovAutoregression; the same model on today\'s real GDP (FRED GDPC1) against the NBER dates '
              '(QPS, concordance); pseudo-real-time filtered probabilities 1990-2026; robustness of the recession dating '
              'across specifications and samples; durations and mixing of a two-regime chain.',
         keywords='Markov switching, Hamilton filter, Kim smoother, business cycle, NBER, recession dating, QPS, real time',
         consts=CONSTS, funcs=BASE + [g.fit_hamilton, g.fig_chain, g.fig_hamilton, g.fig_hamilton_probs, g.fig_realtime,
                                      g.dating_variant, g.fig_ai_case],
         run='print(fig_chain())\nprint(fig_hamilton()["paper"])\nprint(fig_realtime(step=8))\nprint(fig_ai_case()["n_both"])',
         charts=['ats_ch7_chain', 'ats_ch7_hamilton89', 'ats_ch7_realtime', 'ats_ch7_ai_case']),
    dict(name='ATS_ch7_estimation',
         desc='Estimation and testing of Markov-switching regressions: the EM algorithm of Hamilton (1990) from many starting '
              'values (local and degenerate maxima) on Hamilton\'s GNP data; information criteria and a parametric '
              'bootstrap of the likelihood-ratio statistic for one against two regimes on US GDP growth 1947-2019.',
         keywords='EM algorithm, maximum likelihood, local maxima, likelihood ratio test, nuisance parameters, bootstrap, Markov switching',
         consts=CONSTS, funcs=BASE + [g.fig_em, g.lr_bootstrap, g.regime_ic, g.fig_lrtest],
         run='print(fig_em())\nprint(fig_lrtest(B=49))', charts=['ats_ch7_em', 'ats_ch7_lrtest']),
    dict(name='ATS_ch7_tvtp',
         desc='Time-varying transition probabilities (Diebold, Lee and Weinbach 1994; Filardo 1994): switching-mean AR(4) of '
              'US industrial production growth with logistic transition probabilities driven by the leading indicator, '
              'numpy maximum likelihood and statsmodels, LR test against constant transitions.',
         keywords='time-varying transition probabilities, TVTP, leading indicator, business cycle, Markov switching, Filardo',
         consts=CONSTS, funcs=BASE + [g.fit_hamilton, g.fig_tvtp], run='print(fig_tvtp())', charts=['ats_ch7_tvtp']),
    dict(name='ATS_ch7_msvar',
         desc='Markov-switching VAR (MSIAH(2)-VAR(1), Krolzig 1997) for US GDP growth and the change of the unemployment rate, '
              '1960-2019, estimated by EM; regime-dependent impulse responses (Ehrmann, Ellison and Valla 2003).',
         keywords='Markov-switching VAR, MS-VAR, EM algorithm, regime-dependent impulse responses, Okun law',
         consts=CONSTS, funcs=BASE + [g.us_var_data, g.fig_msvar], run='print(fig_msvar())', charts=['ats_ch7_msvar']),
    dict(name='ATS_ch7_msgarch',
         desc='Markov-switching GARCH for S&P 500 daily returns 2000-2026: GARCH(1,1) against the MS-GARCH of Haas, Mittnik '
              'and Paolella (2004), without path dependence, and of Gray (1996), with collapsing; numerical maximum likelihood.',
         keywords='MS-GARCH, GARCH, path dependence, volatility regimes, Haas Mittnik Paolella, Gray, S&P 500',
         consts=CONSTS, funcs=BASE + [g.fig_msgarch], run="print(fig_msgarch(start='2015-01-01'))", charts=['ats_ch7_msgarch']),
    dict(name='ATS_ch7_bullbear',
         desc='Bull and bear regimes of weekly S&P 500 and BET returns 2000-2026: two regimes in mean and variance by EM and '
              'numerical ML, comparison with statsmodels MarkovRegression, regime-dependent mean-variance weights '
              '(Ang and Bekaert 2002).',
         keywords='bull and bear markets, Markov switching, volatility regimes, asset allocation, S&P 500, BET',
         consts=CONSTS, funcs=BASE + [g.fit_bullbear, g.fig_bullbear], run='print(fig_bullbear())', charts=['ats_ch7_bullbear']),
    dict(name='ATS_ch7_bayes',
         desc='Bayesian estimation of a two-regime model of Romanian quarterly GDP growth: Gibbs sampling with data '
              'augmentation and forward filtering-backward sampling (Albert and Chib 1993; Chib 1996), random permutation '
              'sampler and label switching (Fruhwirth-Schnatter 2001), comparison with EM.',
         keywords='Gibbs sampling, data augmentation, FFBS, label switching, Bayesian Markov switching, Romania, GDP',
         consts=CONSTS, funcs=BASE + [g.fig_gibbs], run='print(fig_gibbs(n_iter=3000, burn=500))', charts=['ats_ch7_gibbs']),
    dict(name='ATS_ch7_longmem',
         desc='Regime switching and long memory (Diebold and Inoue 2001): GPH estimates of d for a switching-mean process with '
              'rare switches against fixed transition probabilities, by simulation.',
         keywords='long memory, regime switching, GPH estimator, spurious long memory, simulation',
         consts=CONSTS, funcs=BASE + [g.sim_ms, g.fig_longmem], run='print(fig_longmem(reps=100))', charts=['ats_ch7_longmem']),
    dict(name='ATS_ch7_ro_inflation',
         desc='Romanian annual HICP inflation since 1997 (Eurostat): MSIH(3)-AR(1) estimated by EM against change-point '
              'models with 3, 4 and 5 regimes (Chib 1998), information criteria and regime dates.',
         keywords='inflation regimes, Romania, HICP, Markov switching, change-point model, structural breaks',
         consts=CONSTS, funcs=BASE + [g.fig_ro_infl], run='print(fig_ro_infl())', charts=['ats_ch7_ro_infl']),
    dict(name='ATS_ch7_eurron',
         desc='EUR/RON weekly log changes 1999-2026 (ECB reference rate to June 2005, BNR reference rate afterwards): three '
              'regimes in mean and variance, the 2005 redenomination and float, 2008 and May 2025.',
         keywords='exchange-rate regimes, EUR/RON, volatility regimes, Markov switching, BNR',
         consts=CONSTS, funcs=BASE + [g.fig_eurron], run='print(fig_eurron())', charts=['ats_ch7_eurron']),
    dict(name='ATS_ch7_forecast',
         desc='Forecasting with regime models: recursive one-step density forecasts of US GDP growth 1990-2019 from an AR(1) '
              'and an MSIH(2)-AR(1), RMSE, log score, Diebold-Mariano test on the log-score difference, PIT histograms.',
         keywords='density forecast, log score, PIT, Diebold-Mariano, Markov switching, GDP',
         consts=CONSTS, funcs=BASE + [g.fig_forecast], run='print(fig_forecast(refit=8))', charts=['ats_ch7_forecast']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar7 as s
    SEMC = [f'A1 = {s.A1!r}', f'A3 = {s.A3!r}', f'A4 = {s.A4!r}', f'A5 = {s.A5!r}', f'A6 = {s.A6!r}', f'A7 = {s.A7!r}',
            f'A8 = {s.A8!r}']
    SEMF = [g.fit_hamilton, g.lr_bootstrap, g.regime_ic, g.fit_bullbear]
    QUANTLETS.append(dict(
        name='ATS_ch7_seminar',
        desc='Seminar 7 of Advanced Time Series Analysis and Forecasting: the Hamilton filter and the Kim smoother by hand, '
             'one EM step, regime forecasts, information criteria and bootstrap p-values, identification, MS-GARCH variances, '
             'Gibbs conditionals; numpy against statsmodels on US GDP, Hamilton (1989), the number of regimes in Romanian '
             'GDP growth, Romanian inflation regimes, bull and bear regimes of the S&P 500 and the BET, MS-GARCH for the '
             'BET; EUR/RON in 2025; an AI answer to audit.',
        keywords='seminar, Markov switching, Hamilton filter, EM algorithm, bootstrap, MS-GARCH, Romania, BET, EUR/RON',
        consts=CONSTS + SEMC,
        funcs=BASE + SEMF + [s.a1_filter, s.a2_smoother, s.a3_em, s.a4_forecast, s.a5_ic, s.a6_states, s.a7_garch, s.a8_gibbs,
                             s.b1_numpy_vs_sm, s.b2_hamilton, s.b3_ro_regimes, s.b4_ro_infl, s.b5_bullbear, s.b6_bet_garch,
                             s.c1_eurron_2025, s.c2_check],
        run="print(a1_filter())\nprint(a3_em())\nprint(a5_ic())\nprint(a7_garch())\nprint(b1_numpy_vs_sm())\nprint(b3_ro_regimes(B=49))\nprint(b5_bullbear())",
        charts=['ch7_sem_b1', 'ch7_sem_b3', 'ch7_sem_b5']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 7, 'Regime-switching models', HERE, data=DATA, submitted=SUBMITTED)
