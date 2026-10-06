"""
build_quantlets.py -- Quantlet folders of Chapter 4 (ATS): cointegration revisited, VECM, ARDL and panel data
==============================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_04/generate_all_charts.py && python3 Quantlets/Ch_04/seminar4.py
      python3 Quantlets/Ch_04/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 4
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import ats_data as AD                           # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Monday, 5 October 2026'
DATA = ('IMF International Financial Statistics, interest rates (MFS_IR, public SDMX API; Romanian and Hungarian lending '
        'and deposit rates reported by the central banks); Eurostat (irt_st_m, prc_hicp_minr, prc_hicp_aind, nama_10_gdp, '
        'nasa_10_nf_tr, nama_10_pe); FRED (PCND, PCESV, FPI, GDP, GDPDEF, B230RC0Q173SBEA, POILBREUSDM); BNR reference '
        'rate')
NODATA = 'Simulated data'
CONSTS = ['import io', 'import urllib.error', 'from scipy import optimize', f'SEED = {g.SEED!r}', f'IMF_IR = {g.IMF_IR!r}',
          f'IMF_LEND = {g.IMF_LEND!r}', f'IMF_DEP = {g.IMF_DEP!r}', f'R3M = {g.R3M!r}', f'PT = {g.PT!r}',
          f'KPSW = {g.KPSW!r}', f'EU27 = {g.EU27!r}', f'PANEL = {g.PANEL!r}', f'NSIM = {g.NSIM!r}', f'CASES = {g.CASES!r}',
          f'PSS_CASES = {g.PSS_CASES!r}', '_FILES = {}', '_TAB = {}', "HERE = '.'"]
CORE = [g.get_bytes, g.save, g.patch, g.vecm_design, g.resid, g.johansen, g.vecm_fit, g.logdet, g.lr_beta,
        g.partial_moments, g.restricted_ml, g.weak_exog_lr, g.var_from_vecm, g.ma_coefs, g.perp, g.granger_C,
        g.lag_select, g.sim_trace_null, g.trace_tables, g.crit_table, g.pvalue, g.ols, g.ardl_ecm, g.ardl_select,
        g.bounds_sim, g.bounds_quantiles, g.reinsel_ahn, g.vecm_simulate, g.boot_trace]
PTF = [g.read_imf_rates, g.passthrough_data, g.passthrough_tests]
KPF = [g.kpsw_data, g.permanent_shock, g.common_trend_irf, g.kpsw_model, g.vecm_bootstrap]
PNF = [g.eu_panel, g.hicp_panel, g.wide, g.cd_test, g.adf_t, g.ips_tbar, g.cips, g.llc_t, g.panel_null,
       g.pedroni_group_adf, g.westerlund_gt, g.coint_null, g.ecm_unit, g.mean_group, g.pmg, g.dfe, g.ccemg, g.dols_mg,
       g.hausman]

QUANTLETS = [
    dict(name='ATS_ch4_johansen_asymptotics',
         desc='The Johansen trace statistic in the five deterministic cases: null distributions simulated from random walks '
              '(10,000 replications, T = 400) and their 90/95/99% quantiles for n - r = 1..4; the small-sample size of the '
              'trace test of H(1) in a three-variable VECM with persistent short-run dynamics: asymptotic critical value, '
              'Reinsel-Ahn (1992) correction and the wild bootstrap of Cavaliere, Rahbek and Taylor (2012), with i.i.d. and '
              'GARCH errors.',
         keywords='cointegration, Johansen, trace test, deterministic terms, Reinsel-Ahn, bootstrap, wild bootstrap, size',
         consts=CONSTS, funcs=CORE + [g.mc_dgp, g.mc_size, g.fig_trace_dists, g.fig_size_mc], data=NODATA,
         run='print(fig_trace_dists(reps=4000)["table"])\nprint(fig_size_mc(reps=100, B=99))',
         charts=['ats_ch4_trace_dists', 'ats_ch4_size_mc']),
    dict(name='ATS_ch4_passthrough_vecm',
         desc='Interest-rate pass-through in Romania: lending and deposit rates in lei (IMF IFS, BNR data) and ROBOR 3M '
              '(Eurostat), monthly 2005:8-2026:3; Johansen rank tests in case 2 with Reinsel-Ahn and wild-bootstrap '
              'p-values; a just-identified rank-2 VECM; LR tests of complete pass-through (restrictions on beta) and of weak '
              'exogeneity of ROBOR (restrictions on alpha); the two equilibrium errors.',
         keywords='VECM, Johansen, interest-rate pass-through, ROBOR, Romania, weak exogeneity, restricted cointegration',
         consts=CONSTS, funcs=CORE + PTF + [g.fig_rates], run='print(fig_rates())',
         charts=['ats_ch4_rates', 'ats_ch4_pt_ect']),
    dict(name='ATS_ch4_common_trends',
         desc='King, Plosser, Stock and Watson (1991): log real per capita consumption of nondurables and services, fixed '
              'investment and GDP (FRED), US quarterly 1949:1-1988:4; rank tests, the LR test of the great ratios in cases 3 '
              'and 4, the permanent (balanced-growth) shock of the common-trends VECM, its impulse responses and variance '
              'shares with residual-bootstrap bands; extended samples to 2019 and 2025.',
         keywords='common trends, structural VECM, permanent shock, balanced growth, great ratios, King-Plosser-Stock-Watson',
         consts=CONSTS, funcs=CORE + KPF + [g.fig_kpsw], run='print(fig_kpsw(B=100))', charts=['ats_ch4_kpsw']),
    dict(name='ATS_ch4_i2_check',
         desc='Is the Romanian price level I(2)? Monthly HICP (Eurostat), 1997-2026: log level, monthly inflation and ADF '
              'tests of inflation over the full sample and since the start of inflation targeting (August 2005).',
         keywords='I(2), unit root, inflation, HICP, Romania, ADF',
         consts=CONSTS, funcs=[g.save, g.ols, g.adf_t, g.fig_i2], run='print(fig_i2())', charts=['ats_ch4_i2']),
    dict(name='ATS_ch4_ardl_bounds',
         desc='ARDL and the bounds test of Pesaran, Shin and Smith (2001): asymptotic critical-value bounds simulated for '
              'cases II and III and k = 1..3, small-sample bounds for T = 30..250 (as in Narayan 2005); the conditional ECM of '
              'the Romanian lending and deposit rates on ROBOR, the long-run pass-through with delta-method standard errors '
              'and the cumulative dynamic multipliers.',
         keywords='ARDL, bounds test, conditional ECM, critical values, small samples, interest-rate pass-through, multipliers',
         consts=CONSTS, funcs=CORE + PTF + [g.ardl_multipliers, g.fig_bounds], run='print(fig_bounds(reps=3000))',
         charts=['ats_ch4_bounds']),
    dict(name='ATS_ch4_panel',
         desc='EU-27 annual panel (Eurostat), 2001-2022: real per capita household consumption, disposable income and '
              'inflation; Pesaran CD test; LLC, IPS and CIPS panel unit-root tests with simulated null distributions; Pedroni '
              'group ADF and Westerlund Gt panel cointegration tests; mean group, pooled mean group (Pesaran, Shin and Smith '
              '1999), dynamic fixed effects, group-mean DOLS and CCEMG long-run estimates; Hausman test.',
         keywords='panel unit root, CIPS, cross-section dependence, panel cointegration, pooled mean group, CCE, EU',
         consts=CONSTS, funcs=CORE + PNF + [g.fig_panel], run='print(fig_panel(reps=300))', charts=['ats_ch4_panel']),
    dict(name='ATS_ch4_ai_robustness',
         desc='AI mini-case: how robust is the verdict of complete pass-through of ROBOR to the Romanian lending rate? The '
              'long-run coefficient of the rank-2 VECM and the p-value of the restriction across lag lengths 2-6, '
              'deterministic cases 2 and 3 and samples ending in 2019 and 2026.',
         keywords='robustness, specification search, VECM, pass-through, AI for science, pre-registration',
         consts=CONSTS, funcs=CORE + PTF + [g.fig_ai_case], run='print(fig_ai_case())', charts=['ats_ch4_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar4 as s
    SEMC = [f'A1L = np.array({s.A1L.tolist()!r})', f'A2LR = {s.A2LR!r}', f'A3A = np.array({s.A3A.tolist()!r})',
            f'A3B = np.array({s.A3B.tolist()!r})', f'A4A = np.array({s.A4A.tolist()!r})',
            f'A4O = np.array({s.A4O.tolist()!r})', f'A6F = {s.A6F!r}', f'A7R = np.array({s.A7R.tolist()!r})', f'A8 = {s.A8!r}']
    QUANTLETS.append(dict(
        name='ATS_ch4_seminar',
        desc='Seminar 4 of Advanced Time Series Analysis and Forecasting: the trace test from eigenvalues, degrees of '
             'freedom, the Granger representation, a permanent shock, ARDL algebra, a bounds decision, the CD statistic and '
             'the Hausman test by hand; rank tests and restrictions for the Hungarian interest-rate pass-through; the bounds '
             'test for Romanian fuel prices and the oil price; the KPSW common trend on longer samples; EU-27 inflation by '
             'IPS and CIPS; an asymmetric (NARDL) fuel-price model; an AI answer to audit.',
        keywords='seminar, cointegration, VECM, ARDL, bounds test, panel unit root, NARDL, Hungary, Romania',
        consts=CONSTS + SEMC, data=DATA,
        funcs=CORE + PTF + KPF + PNF + [s.a1_trace, s.a2_df, s.a3_granger, s.a4_permanent, s.a5_ardl, s.a6_bounds,
                                         s.a7_cd, s.a8_hausman, s.hu_data, s.b1_hu_rank, s.b2_hu_restrict, s.fuel_data,
                                         s.b3_fuel, s.b4_kpsw_ext, s.b5_inflation_panel, s.c1_nardl, s.c2_check],
        run="print(a1_trace())\nprint(a3_granger())\nprint(a5_ardl())\nprint(a7_cd())\nprint(b1_hu_rank(B=199))\nprint(b3_fuel())",
        charts=['ch4_sem_b1', 'ch4_sem_b3']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 4, 'Cointegration revisited: VECM, ARDL and panel data', HERE, data=DATA, submitted=SUBMITTED)
