"""
build_quantlets.py -- Quantlet folders of Chapter 3 (ATS): structural VAR and local projections
================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  python3 Quantlets/Ch_03/generate_all_charts.py && python3 Quantlets/Ch_03/seminar3.py
      python3 Quantlets/Ch_03/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 3
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
DATA = ('Replication files of Ramey (2016, Handbook of Macroeconomics) and Ramey and Zubairy (2018, JPE), public on the '
        "author's website; EIA international energy statistics (bulk file) and Monthly Energy Review; FRED (IGREA, CPIAUCSL, "
        'GNPC96, LNS14000025); Eurostat (sts_inpr_m, prc_hicp_minr, irt_st_m); BNR reference rate; ECB Data Portal (yield '
        'curve); euro-area monetary policy shocks of Jarocinski and Karadi (2020), update by the authors (public CSV)')
NODATA = 'Simulated data'
CONSTS = ['import io', 'import zipfile', 'import urllib.error', f'SEED = {g.SEED!r}', f'RAMEY_MON = {g.RAMEY_MON!r}',
          f'RAMEY_RZ = {g.RAMEY_RZ!r}', f'EIA_INTL = {g.EIA_INTL!r}', f'EIA_PROD = {g.EIA_PROD!r}', f'EIA_MER9 = {g.EIA_MER9!r}',
          f'EA_Y1 = {g.EA_Y1!r}', f'JK_ECB = {g.JK_ECB!r}', f'RO_IP = {g.RO_IP!r}', f'EA_IP = {g.EA_IP!r}',
          f'RO_HICP = {g.RO_HICP!r}', f'EA_HICP = {g.EA_HICP!r}', f'RO_R3M = {g.RO_R3M!r}', f'EA_R3M = {g.EA_R3M!r}',
          f'RO_START = {g.RO_START!r}', f'CEE = {g.CEE!r}', f'KIL = {g.KIL!r}', f'BQ = {g.BQ!r}', f'UHL = {g.UHL!r}',
          f'GK = {g.GK!r}', f'LPGK = {g.LPGK!r}', f'RZ = {g.RZ!r}', f'RO = {g.RO!r}', f'NBOOT = {g.NBOOT!r}',
          f'RO_VARS = {g.RO_VARS!r}', 'PSI = np.array(' + repr(g.PSI.tolist()) + ')',
          'KIL_SIGN = np.diag(' + repr(g.KIL_SIGN.diagonal().tolist()) + ')', '_FILES = {}']
CORE = [AD.read_ecb, g.get_bytes, g.zip_member, g.save, g.lagmat, g.var_ols, g.companion, g.max_root, g.ma_coefs, g.irf,
        g.fevd, g.simulate_var, g.bootstrap_var, g.shrink_bias, g.kilian_bias, g.bands, g.chol, g.band_plot, g.patch,
        g.nw_se, g.lp, g.tsls, g.lp_iv, g.lags_of]
KILF = [g.oil_data, g.kilian_ident, g.kilian_model]
ROF = [g.ro_monthly, g.month_dummies, g.ro_model, g.lag_ic, g.jk_ecb_shocks, g.ro_lp_frame, g.ro_lp]

QUANTLETS = [
    dict(name='ATS_ch3_recursive_var',
         desc='The recursive monetary VAR of Christiano, Eichenbaum and Evans (1999) in the specification of Ramey (2016, '
              'Figure 1): VAR(12) in log IP, unemployment, log CPI, log commodity prices, federal funds rate, log nonborrowed '
              'and total reserves and log M1, 1965:1-1995:6, Cholesky with the funds rate fifth; responses with 90% '
              'residual-bootstrap bands and the variance decomposition of IP.',
         keywords='structural VAR, Cholesky, recursive identification, monetary policy shock, price puzzle, bootstrap, FEVD',
         consts=CONSTS, funcs=CORE + [g.ramey_monthly, g.cee_model, g.fig_cee], run='print(fig_cee())',
         charts=['ats_ch3_cee_irf']),
    dict(name='ATS_ch3_oil_shocks',
         desc='Kilian (2009): oil supply, aggregate demand and oil-specific demand shocks in a recursive VAR(24) of world '
              'crude oil production (EIA), global real activity (FRED IGREA) and the real refiner acquisition cost of '
              'imported crude (EIA, deflated by CPI); responses with recursive-design wild-bootstrap bands, the extended '
              'sample to 2026, the historical decomposition of the real price of oil and the Kilian (1998) bias correction.',
         keywords='oil price, supply shock, demand shock, Kilian, recursive VAR, wild bootstrap, historical decomposition, bias correction',
         consts=CONSTS, funcs=CORE + KILF + [g.fig_kilian, g.fig_kilian_hd, g.kilian_bias_demo],
         run='print(fig_kilian())\nprint(fig_kilian_hd())\nprint(kilian_bias_demo(B=200))',
         charts=['ats_ch3_kilian_irf', 'ats_ch3_kilian_hd']),
    dict(name='ATS_ch3_long_run',
         desc='Blanchard and Quah (1989): supply and demand shocks identified by a long-run restriction in a VAR(8) of US real '
              'GNP growth and the unemployment rate of men aged 20 and over, 1950:2-1987:4, with separate means of output '
              'growth before and after 1973:4 and a linear trend in unemployment; responses with bootstrap bands and the '
              'variance decomposition of the output level.',
         keywords='long-run restriction, Blanchard-Quah, supply shock, demand shock, structural VAR, GNP, unemployment',
         consts=CONSTS, funcs=CORE + [g.bq_data, g.bq_impact, g.bq_model, g.bq_ident, g.fig_bq], run='print(fig_bq())',
         charts=['ats_ch3_bq']),
    dict(name='ATS_ch3_sign_restrictions',
         desc='Sign restrictions and set identification: the set of rotations satisfying demand and supply signs in a '
              'two-variable example; Uhlig (2005): six-variable monthly VAR(12) without constant, 1965:1-2003:12, '
              'restrictions on prices, commodity prices, nonborrowed reserves and the funds rate for months 0-5, Normal-'
              'inverse-Wishart draws with Haar rotations (Rubio-Ramirez, Waggoner and Zha 2010) and the identified set at '
              'the OLS estimate.',
         keywords='sign restrictions, set identification, Haar measure, Uhlig, monetary policy, Bayesian VAR, identified set',
         consts=CONSTS, funcs=CORE + [g.haar, g.niw_draw, g.ramey_monthly, g.fig_rotation, g.uhlig_data, g.uhlig_check,
                                      g.uhlig_draws, g.uhlig_set, g.fig_uhlig],
         run='print(fig_rotation())\nprint(fig_uhlig(ndraw=500))', charts=['ats_ch3_rotation', 'ats_ch3_uhlig']),
    dict(name='ATS_ch3_proxy_svar',
         desc='Gertler and Karadi (2015): a proxy SVAR with high-frequency FF4 surprises as external instrument for a '
              'monetary policy shock in a VAR(12) of the 1-year Treasury yield, log IP, log CPI and the excess bond premium, '
              '1979:7-2012:6 (instrument 1991:1-2012:6); first-stage F and moving-block bootstrap bands (Jentsch and '
              'Lunsford 2019).',
         keywords='proxy SVAR, external instrument, high-frequency identification, Gertler-Karadi, FF4, moving-block bootstrap',
         consts=CONSTS, funcs=CORE + [g.ramey_monthly, g.first_stage, g.proxy_impact, g.proxy_irf, g.proxy_mbb, g.gk_model,
                                      g.fig_gk], run='print(fig_gk())', charts=['ats_ch3_gk']),
    dict(name='ATS_ch3_lp_vs_var',
         desc='Local projections against VARs: a simulation of the bias-variance trade-off (Li, Plagborg-Moller and Wolf '
              '2024) with a misspecified VAR(2), a VAR(12) and LP(2); LP-IV with the Gertler-Karadi instrument (Ramey 2016, '
              'Figure 3B specification) against the proxy SVAR.',
         keywords='local projections, LP-IV, VAR, bias-variance trade-off, Newey-West, simulation, monetary policy',
         consts=CONSTS, funcs=CORE + [g.ramey_monthly, g.first_stage, g.proxy_impact, g.proxy_irf, g.gk_model, g.lp_iv_se,
                                      g.fig_lp_gk, g.sim_dgp, g.true_irf, g.lp_sim_estimates, g.fig_lp_sim],
         run='print(fig_lp_gk())\nprint(fig_lp_sim(reps=200))', charts=['ats_ch3_lp_gk', 'ats_ch3_lp_sim']),
    dict(name='ATS_ch3_state_dependent_lp',
         desc='Ramey and Zubairy (2018): cumulative government spending multipliers by LP-IV with the military news shock, '
              'US quarterly data 1889-2015, linear and state-dependent (slack: unemployment at least 6.5% in t-1), 4 lags of '
              'news, output and spending, Newey-West standard errors.',
         keywords='state-dependent local projections, fiscal multiplier, Ramey-Zubairy, military news, LP-IV, slack',
         consts=CONSTS, funcs=CORE + [g.rz_quarterly, g.tsls_multi, g.rz_frame, g.rz_multipliers, g.fig_rz],
         run='print(fig_rz())', charts=['ats_ch3_rz']),
    dict(name='ATS_ch3_romania',
         desc='Romania and euro-area spillovers: monthly data 2005-2026 (Eurostat IP, HICP, 3-month rates; BNR EUR/RON); a '
              'recursive VAR(2) with the euro-area block first, responses to ROBOR and Euribor shocks with bootstrap bands '
              'and the variance decomposition; lag-augmented local projections on the euro-area monetary policy shocks of '
              'Jarocinski and Karadi (2020); robustness of the 12-month HICP response across lags, samples and estimators.',
         keywords='Romania, ROBOR, euro area, spillovers, structural VAR, local projections, Jarocinski-Karadi, weak instrument',
         consts=CONSTS, funcs=CORE + ROF + [g.fig_ro_data, g.fig_ro_var, g.fig_ro_lp, g.fig_ai_case],
         run='print(fig_ro_data())\nprint(fig_ro_var())\nprint(fig_ro_lp())\nprint(fig_ai_case())',
         charts=['ats_ch3_ro_data', 'ats_ch3_ro_var', 'ats_ch3_ro_lp', 'ats_ch3_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar3 as s
    QUANTLETS.append(dict(
        name='ATS_ch3_seminar',
        desc='Seminar 3 of Advanced Time Series Analysis and Forecasting: Cholesky, a known elasticity, a long-run '
             'restriction, the sign-restricted set, an external instrument, LP in an AR(1), FEVD and identification '
             'through heteroskedasticity by hand; Kilian (2009) on oil; orderings of a Romanian VAR; the Gertler-Karadi '
             'proxy SVAR; Romer-Romer shocks by LP and VAR; Blanchard-Quah robustness; euro-area spillovers with an '
             'Anderson-Rubin set; an AI answer to audit.',
        keywords='seminar, structural VAR, identification, sign restrictions, proxy SVAR, local projections, Romania',
        consts=CONSTS + ['SIG = np.array(' + repr(s.SIG.tolist()) + ')', 'A1M = np.array(' + repr(s.A1M.tolist()) + ')',
                         f'A21 = {s.A21!r}', 'A3A = np.array(' + repr(s.A3A.tolist()) + ')',
                         'A3S = np.array(' + repr(s.A3S.tolist()) + ')', 'A4S = np.array(' + repr(s.A4S.tolist()) + ')',
                         'A5C = np.array(' + repr(s.A5C.tolist()) + ')', f'A6 = {s.A6!r}',
                         'A8B = np.array(' + repr(s.A8B.tolist()) + ')', 'A8D1 = np.diag(' + repr(s.A8D1.diagonal().tolist()) + ')',
                         'A8D2 = np.diag(' + repr(s.A8D2.diagonal().tolist()) + ')'],
        funcs=CORE + KILF + ROF + [g.ramey_monthly, g.bq_data, g.bq_impact, g.bq_ident, g.first_stage, g.proxy_impact,
                                   g.proxy_irf, g.proxy_mbb, g.gk_model,
                                   s.a1_cholesky, s.a2_known_elasticity, s.a3_long_run, s.a4_sign_set, s.a5_proxy,
                                   s.a6_lp_ar1, s.a7_fevd, s.a8_hetero, s.b1_kilian, s.b2_ro_ordering, s.b3_gk, s.b4_romer,
                                   s.b5_bq_robust, s.c1_spillover_ar, s.c2_check],
        run="print(a1_cholesky())\nprint(a3_long_run())\nprint(a5_proxy())\nprint(a7_fevd())\nprint(b1_kilian())\nprint(b3_gk())",
        charts=['ch3_sem_b1', 'ch3_sem_b3']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 3, 'Structural VAR and local projections', HERE, data=DATA, submitted=SUBMITTED)
