"""
build_quantlets.py -- Quantlet folders of Chapter 14 (ATS): causal inference for time series
=============================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_14/generate_all_charts.py && python3 Quantlets/Ch_14/seminar14.py
      python3 Quantlets/Ch_14/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 14
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import causal_core as c                         # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Tuesday, 6 October 2026'
DATA = ('Daily market data from EODHD (data/market of the ATS repository) and the BNR reference rate; Eurostat HICP '
        '(prc_hicp_minr) and HICP at constant tax rates (prc_hicp_ct) of the 27 EU countries; the replication data of '
        'Abadie, Diamond and Hainmueller (2015), Harvard Dataverse doi:10.7910/DVN/24714 (version 2.1, CC0); OECD '
        'Quarterly National Accounts (real GDP, PPP, public SDMX API)')
INSTALL = "# numpy, scipy, statsmodels and scikit-learn are preinstalled in Colab\n# !pip install statsmodels scikit-learn"
CONSTS = ['import io\nimport sys\nimport urllib.error\nfrom scipy.special import digamma\nfrom scipy.spatial import cKDTree',
          f'SEED = {g.SEED!r}', f'EUROSTAT = {g.EUROSTAT!r}', f'EU27 = {g.EU27!r}', f'EURO_AREA = {g.EURO_AREA!r}',
          f'RO_SC = {g.RO_SC!r}', f'GERMANY_URL = {g.GERMANY_URL!r}', f'OECD_QNA = {g.OECD_QNA!r}', f'BMSS = {g.BMSS!r}',
          f'EVENTS = {g.EVENTS!r}', f'BTC = {g.BTC!r}', f'STAG_SLOPES = {g.STAG_SLOPES!r}',
          f'PCMCI_NAMES = {g.PCMCI_NAMES!r}', f'PCMCI_LABELS = {g.PCMCI_LABELS!r}', f'ADH_SPEC = {g.ADH_SPEC!r}',
          '_MEM = {}']
CORE = [c.nw_lags, c.ols_hac, c.wald, c.lag_design, c.granger, c.sim_common_driver, c.knn_cmi, c.transfer_entropy,
        c.sim_nonlinear_coupling, c.parcorr, c.pcmci, c.full_granger_links, c.corr_links, c.sim_pcmci_system,
        c.link_rates, c.sim_logistic_pair, c.embed_delay, c.cross_map, c.ccm_curve, c.sc_weights, c.synth_v,
        c.sc_demeaned, c.ascm_ridge, c.ascm_lambda, c.sdid, c.sdid_placebo_se, c.placebo_ratios, c.sim_staggered,
        c.twfe_event, c.cs_att, c.causal_impact, c.dml_plr, c.sim_dml]
DATAF = [g.datefmt, g.save, g.get_bytes, g.eurostat_panel, g.hicp_annual, g.hicp_index, g.germany, g.oecd_gdp,
         g.weekly_logrv, g.daily_returns]
BASE = DATAF + CORE

QUANTLETS = [
    dict(name='ATS_ch14_granger',
         desc='Granger causality and transfer entropy: a Monte Carlo with a common driver (pairwise against conditional '
              'tests); lead and lag between the S&P 500, the DAX and the BET (daily returns, Wald tests with HAC '
              'covariance, cross-correlations); a nonlinear coupling detected by the k-nearest-neighbour transfer entropy '
              'with block permutations and missed by the linear Granger test.',
         keywords='Granger causality, transfer entropy, HAC, conditional mutual information, common driver, BET, S&P 500',
         consts=CONSTS, funcs=BASE + [g.fig_granger_sim, g.fig_granger_markets, g.fig_te],
         run="print(fig_granger_sim(reps=200))\nprint(fig_granger_markets())\nprint(fig_te(B=99))",
         charts=['ats_ch14_granger_sim', 'ats_ch14_granger_markets', 'ats_ch14_te']),
    dict(name='ATS_ch14_discovery',
         desc='Causal discovery: PCMCI with partial correlations (Runge et al. 2019) against pairwise lagged correlations and '
              'the full VAR on a known lagged system in low and high dimension; PCMCI on weekly log realised variances of '
              'five equity indices and EUR/RON; convergent cross mapping (Sugihara et al. 2012) for coupled logistic maps '
              'and for uncoupled maps with a common periodic forcing.',
         keywords='PCMCI, causal discovery, time series graph, convergent cross mapping, volatility spillovers, Takens',
         consts=CONSTS, funcs=BASE + [g.fig_pcmci_sim, g.fig_pcmci_vol, g.fig_ccm],
         run="print(fig_pcmci_sim(reps=20))\nprint(fig_pcmci_vol())\nprint(fig_ccm(reps=10))",
         charts=['ats_ch14_pcmci_sim', 'ats_ch14_pcmci_vol', 'ats_ch14_ccm']),
    dict(name='ATS_ch14_its_event',
         desc='Interrupted time series for Romanian monthly HICP inflation around the end of the electricity price cap '
              '(July 2025) and the VAT increase (August 2025), with i.i.d. and HAC standard errors of the cumulative effect; '
              'an event study of the BET against the Euro Stoxx 50 around four Romanian political and fiscal events of '
              '2024-2025.',
         keywords='interrupted time series, event study, HAC, cumulative abnormal return, Romania, VAT, inflation',
         consts=CONSTS, funcs=BASE + [g.its_design, g.fig_its, g.fig_event], run="print(fig_its())\nprint(fig_event())",
         charts=['ats_ch14_its', 'ats_ch14_event']),
    dict(name='ATS_ch14_germany',
         desc='Replication of Abadie, Diamond and Hainmueller (2015): the economic cost of German reunification with their '
              'public data; V chosen by cross-validation (training predictors 1971-1980, validation 1981-1990), weights by '
              'quadratic programming (Table 1), the gap (Figures 2-3), in-space placebos, the 1975 in-time placebo and '
              'leave-one-out (Figures 4-6).',
         keywords='synthetic control, German reunification, placebo test, replication, Synth, cross-validation',
         consts=CONSTS, funcs=BASE + [g.adh_matrices, g.adh_fit, g.fig_germany, g.fig_germany_placebo],
         run="print(fig_germany())\nprint(fig_germany_placebo())",
         charts=['ats_ch14_germany', 'ats_ch14_germany_placebo']),
    dict(name='ATS_ch14_brexit',
         desc='The Brexit doppelganger of Born, Mueller, Schularick and Sedlacek (2019) on today\'s OECD quarterly real GDP: '
              '23 donors, 1995Q1-2016Q2, outcome-only synthetic control, time placebos 2010Q1-2016Q1 and country placebos.',
         keywords='synthetic control, Brexit, doppelganger, data revisions, placebo test, OECD',
         consts=CONSTS, funcs=BASE + [g.bmss_fit, g.fig_brexit], run="print(fig_brexit())", charts=['ats_ch14_brexit']),
    dict(name='ATS_ch14_romania',
         desc='The effect of the end of the electricity price cap and of the 2025 VAT increase on Romanian inflation: the four '
              'case studies of the chapter; synthetic control, demeaned SC, ridge-augmented SC and synthetic difference in '
              'differences on the annual HICP inflation of 26 EU donors; in-space placebos; the tax component from the HICP '
              'at constant tax rates.',
         keywords='synthetic control, augmented synthetic control, synthetic difference in differences, VAT, inflation, Romania, Eurostat',
         consts=CONSTS, funcs=BASE + [g.fig_overview, g.ro_panel, g.ro_estimates, g.fig_ro_sc, g.fig_ro_placebo, g.fig_ro_tax],
         run="print(fig_overview())\nprint(fig_ro_sc())\nprint(fig_ro_placebo())\nprint(fig_ro_tax())",
         charts=['ats_ch14_overview', 'ats_ch14_ro_sc', 'ats_ch14_ro_placebo', 'ats_ch14_ro_tax']),
    dict(name='ATS_ch14_did_dml',
         desc='Staggered adoption: two-way fixed effects against the group-time estimator of Callaway and Sant\'Anna (2021) on '
              'a simulated panel with effects that grow with exposure; double/debiased machine learning with blocked '
              'cross-fitting on simulated dependent data.',
         keywords='difference in differences, staggered adoption, TWFE, Callaway Sant\'Anna, double machine learning, cross-fitting',
         consts=CONSTS, funcs=BASE + [g.fig_staggered, g.fig_dml], run="print(fig_staggered())\nprint(fig_dml(reps=20))",
         charts=['ats_ch14_staggered', 'ats_ch14_dml']),
    dict(name='ATS_ch14_causalimpact',
         desc='A CausalImpact-type analysis (Brodersen et al. 2015) on a statsmodels unobserved-components model of the US spot '
              'Bitcoin ETF approval (10 January 2024): weekly Bitcoin log realised variance with equity, gold and FX '
              'controls; pointwise and cumulative effects; Ether as a control; anticipation; placebo approval dates.',
         keywords='CausalImpact, Bayesian structural time series, state space, Bitcoin ETF, placebo, volatility',
         consts=CONSTS, funcs=BASE + [g.btc_data, g.fig_btc, g.fig_btc_placebo],
         run="print(fig_btc(draws=300))\nprint(fig_btc_placebo(draws=200))", charts=['ats_ch14_btc', 'ats_ch14_btc_placebo']),
    dict(name='ATS_ch14_ai_case',
         desc='AI mini-case: a specification curve for the Romanian estimate: four estimators, three donor pools and four '
              'pre-periods.',
         keywords='specification curve, robustness, synthetic control, pre-registration, Romania',
         consts=CONSTS, funcs=BASE + [g.ro_panel, g.ro_estimates, g.fig_ai_case], run="print(fig_ai_case())",
         charts=['ats_ch14_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar14 as s
    SEMC = [f'{k} = {getattr(s, k)!r}' for k in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'CEE_CONTROLS')]
    SEMF = [g.adh_matrices, g.adh_fit, g.bmss_fit, g.its_design, g.ro_panel]
    QUANTLETS.append(dict(
        name='ATS_ch14_seminar',
        desc='Seminar 14 of Advanced Time Series Analysis and Forecasting: Granger causality from a common driver, synthetic '
             'control weights by hand, placebo p-values, cumulative effects with AR(1) errors, the forbidden comparison of '
             'staggered DiD, local level intervals, orthogonal scores; Granger tests on stock and crypto markets, an '
             'outcome-only synthetic control for West Germany, robustness of the Romanian synthetic control, CausalImpact '
             'for Romanian inflation, placebo dates for the Bitcoin ETF, an interrupted time series with a placebo date, '
             'PCMCI settings; the Brexit doppelganger on revised data; an AI answer to audit.',
        keywords='seminar, Granger causality, synthetic control, placebo, CausalImpact, interrupted time series, PCMCI',
        consts=CONSTS + SEMC,
        funcs=BASE + SEMF + [s.a1_common_driver, s.a2_persistent_driver, s.a3_sc_by_hand, s.a4_placebo, s.a5_ar1_sum,
                             s.a6_forbidden, s.a7_local_level, s.a8_orthogonality, s.b1_granger_markets, s.b2_crypto,
                             s.b3_germany_outcome_only, s.b4_romania_robust, s.b5_impact_romania, s.b6_btc_placebo,
                             s.b7_its_placebo, s.b8_pcmci_sensitivity, s.c1_brexit, s.c2_check],
        run="print(a1_common_driver())\nprint(a3_sc_by_hand())\nprint(a5_ar1_sum())\nprint(a7_local_level())\n"
            "print(b1_granger_markets())\nprint(b3_germany_outcome_only())\nprint(b5_impact_romania())\nprint(b7_its_placebo())",
        charts=['ch14_sem_b3', 'ch14_sem_b4', 'ch14_sem_b5', 'ch14_sem_b6', 'ch14_sem_b7']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 14, 'Causal inference for time series', HERE, data=DATA, submitted=SUBMITTED, install=INSTALL)
