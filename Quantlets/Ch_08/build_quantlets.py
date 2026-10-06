"""
build_quantlets.py -- Quantlet folders of Chapter 8 (ATS): advanced volatility modelling
========================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_08/generate_all_charts.py && OMP_NUM_THREADS=1 python3 Quantlets/Ch_08/seminar8.py
      python3 Quantlets/Ch_08/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 8
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
DATA = ("Oxford-Man Institute's realized library v0.3 (Heber, Lunde, Shephard and Sheppard 2009; archived copy of 28 "
        "February 2022, downloaded from the Internet Archive by read_omi, not redistributed), six indices; daily realised measures of Bitcoin and Ether "
        "computed from Binance public one-minute and one-second prices (data.binance.vision); daily S&P 500, DAX, BET, "
        "Bitcoin and 25 US stocks and ETFs from EODHD (data/market); BNR EUR/RON reference rate; FRED (INDPRO, WPSFD49207); "
        "Eurostat (sts_inpr_m)")
SIMDATA = 'Simulated data (two-factor stochastic volatility with jumps and microstructure noise)'
CONSTS = ['import time', 'from scipy import special', 'from scipy.signal import lfilter', f'SEED = {g.SEED!r}',
          f'REAL_RAW = {g.REAL_RAW!r}',
          "REAL_DIR = next((os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..')\n"
          "                 if os.path.isdir(os.path.join(d, 'data', 'realized'))), '')",
          f'OMI_NAMES = {g.OMI_NAMES!r}', 'MU1 = np.sqrt(2 / np.pi)', 'HT_C = np.pi ** 2 / 4 + np.pi - 5',
          f'SIM = {g.SIM!r}', f'HAR_WIN = {g.HAR_WIN!r}', f'GMV_ASSETS = {g.GMV_ASSETS!r}']
DATAF = [g.save, g.read_realized, g.omi, g.binance_daily, g.returns]
GARCH = [g.garch_var, g.t_logpdf_std, g.garch_lt, g.num_scores, g.num_hessian, g.sandwich, g.fit_garch]
MIDAS = [g.beta_weights, g.midas_data, g.gm_components, g.gm_lt, g.fit_garch_midas]
RM = [g.simulate_intraday, g.rv_k, g.rv_subsampled, g.tsrv, g.parzen, g.realised_kernel, g.rk_bandwidth]
JUMP = [g.bipower, g.tripower, g.ht_stat, g.jump_days]
HAR = [g.har_X, g.newey_west, g.ols, g.qlike, g.har_forecasts, g.dm_test]
RG = [g.rgarch_paths, g.rgarch_lt, g.fit_rgarch, g.heavy_var, g.fit_heavy]
MG = [g.n_params, g.dcc_loglik, g.cdcc_target, g.fit_dcc, g.simulate_cdcc, g.lw_linear, g.nl_shrink,
      g.garch_univariate_std, g.gmv, g.corr_shrunk]

QUANTLETS = [
    dict(name='ATS_ch8_qmle',
         desc='Gaussian quasi-maximum likelihood for GARCH(1,1): Hessian-based, outer-product and Bollerslev-Wooldridge '
              '(1992) sandwich standard errors; a Monte Carlo of the coverage of 95% intervals under Gaussian and '
              'Student-t(5) innovations; robust against naive standard errors for the S&P 500, DAX, BET, EUR/RON and '
              'Bitcoin, 2010-2026.',
         keywords='GARCH, quasi-maximum likelihood, QMLE, sandwich, Bollerslev-Wooldridge, robust standard errors, kurtosis',
         consts=CONSTS, funcs=DATAF + GARCH + [g.simulate_garch, g.fig_qmle_sim, g.fig_qmle_markets],
         run="print(fig_qmle_sim(reps=100))\nprint({k: v['ratio'] for k, v in fig_qmle_markets().items()})",
         charts=['ats_ch8_qmle_sim', 'ats_ch8_qmle_markets']),
    dict(name='ATS_ch8_components',
         desc='Long-run and short-run volatility of the S&P 500 since 1990: the Engle-Lee (1999) component GARCH; '
              'GARCH-MIDAS (Engle, Ghysels and Sohn 2013) with monthly realised variance, US industrial production growth '
              'and PPI inflation (FRED) as long-run drivers, restricted beta weights, 36 monthly lags; variance ratios and '
              'BIC against GARCH(1,1) on the same days.',
         keywords='component GARCH, GARCH-MIDAS, mixed frequency, long-run volatility, macroeconomic fundamentals, variance ratio',
         consts=CONSTS, funcs=DATAF + GARCH + [g.cgarch_var, g.fit_cgarch, g.fig_cgarch] + MIDAS + [g.macro_us, g.fig_garch_midas],
         run="print(fig_cgarch())\nr = fig_garch_midas()\nprint({k: r[k] for k in ('ip', 'ppi', 'rv', 'bic', 'bic_garch')})",
         charts=['ats_ch8_cgarch', 'ats_ch8_garch_midas']),
    dict(name='ATS_ch8_realised_measures',
         desc='Realised measures: a calibrated two-factor stochastic volatility model with jumps and microstructure noise '
              'on a one-second grid; coverage of the feasible CLT of realised variance (raw and log); RV at several '
              'frequencies, subsampled RV, two-scales RV and the Parzen realised kernel against the true quadratic '
              'variation; the signature plot and the Epps effect of Bitcoin and Ether (Binance one-second prices, August '
              '2026); realised kernel volatility of the S&P 500, DAX and Nikkei (Oxford-Man library) and of Bitcoin.',
         keywords='realised variance, realized volatility, microstructure noise, signature plot, realised kernel, two scales, Epps effect',
         consts=CONSTS, funcs=DATAF + RM + [g.fig_rv_clt, g.fig_kernels, g.fig_signature, g.fig_omi_overview],
         run="print(fig_rv_clt(days=150))\nprint(fig_kernels(days=100))\nprint(fig_signature())\nprint(fig_omi_overview())",
         charts=['ats_ch8_rv_clt', 'ats_ch8_kernels', 'ats_ch8_signature', 'ats_ch8_rk_overview']),
    dict(name='ATS_ch8_jumps',
         desc='Bipower variation, tripower quarticity and the ratio jump test of Huang and Tauchen (2005): size and power by '
              'simulation with 5-minute and 1-minute returns; jump days of Bitcoin and Ether from 5-minute returns, '
              '2018-2026, against the number of false rejections expected under the null.',
         keywords='jumps, bipower variation, tripower quarticity, Huang-Tauchen test, Bitcoin, Ether, multiple testing',
         consts=CONSTS, funcs=DATAF + RM + JUMP + [g.fig_jump_sim, g.fig_jumps_crypto], data=DATA,
         run="print(fig_jump_sim(days=500))\nprint(fig_jumps_crypto())", charts=['ats_ch8_jump_power', 'ats_ch8_jumps_crypto']),
    dict(name='ATS_ch8_har',
         desc='HAR-RV (Corsi 2009) for the S&P 500 (Oxford-Man 5-minute RV, 2000-2022) with Newey-West standard errors '
              'and the implied lag weights against an unrestricted AR(22); out-of-sample HAR, HAR-CJ and log-HAR for six '
              'indices; HARQ (Bollerslev, Patton and Quaedvlieg 2016) for Bitcoin and Ether with the insanity filter, '
              'QLIKE and Diebold-Mariano tests.',
         keywords='HAR, HAR-RV, HARQ, realised quarticity, measurement error, volatility forecasting, QLIKE, Diebold-Mariano',
         consts=CONSTS, funcs=DATAF + HAR + [g.fig_har_insample, g.fig_har_oos, g.fig_harq],
         run="print(fig_har_insample())\nprint(fig_har_oos())\nprint(fig_harq())",
         charts=['ats_ch8_har_weights', 'ats_ch8_har_oos', 'ats_ch8_harq']),
    dict(name='ATS_ch8_realized_garch',
         desc='Realized GARCH (Hansen, Huang and Shek 2012), log-linear form with the leverage function, and the HEAVY '
              'variance equation (Shephard and Sheppard 2010) for S&P 500 open-to-close returns with the Parzen realised '
              'kernel (Oxford-Man, 2000-2022); comparison with GARCH(1,1) and GJR on the partial likelihood of returns.',
         keywords='Realized GARCH, HEAVY, realised kernel, measurement equation, leverage, partial likelihood',
         consts=CONSTS, funcs=DATAF + GARCH + RG + [g.fig_rgarch], run='print(fig_rgarch())', charts=['ats_ch8_rgarch']),
    dict(name='ATS_ch8_robust_loss',
         desc='Robust loss functions for volatility forecasts (Patton 2011): expected MSE, QLIKE, MAE and MSE-log losses of '
              'the true variance and of a biased forecast against proxies of increasing precision; an out-of-sample '
              'comparison of GARCH, GJR, GARCH-t, Realized GARCH, HEAVY, HAR and log-HAR for the S&P 500, 2016-2022, '
              'against the realised kernel, with Diebold-Mariano tests.',
         keywords='robust loss, QLIKE, MSE, volatility proxy, forecast evaluation, Diebold-Mariano, Realized GARCH, HAR',
         consts=CONSTS, funcs=DATAF + GARCH + HAR + RG + [g.loss, g.fig_patton, g.fig_vol_oos],
         run="print(fig_patton(T=50000))\nprint(fig_vol_oos()['res'])", charts=['ats_ch8_patton', 'ats_ch8_vol_oos']),
    dict(name='ATS_ch8_mgarch',
         desc='Multivariate GARCH: parameter counts of VEC, BEKK and DCC; DCC against cDCC (Aielli 2013) by simulation; '
              'global minimum-variance portfolios of 25 US stocks and ETFs with sample, Ledoit-Wolf linear, analytical '
              'nonlinear shrinkage (Ledoit and Wolf 2020), DCC and DCC-NL (Engle, Ledoit and Wolf 2019) covariance '
              'matrices; realised (5-minute) and DCC correlations of Bitcoin and Ether.',
         keywords='multivariate GARCH, BEKK, DCC, cDCC, DCC-NL, nonlinear shrinkage, minimum variance, realised correlation',
         consts=CONSTS, funcs=DATAF + GARCH + MG + [g.fig_dcc_sim, g.fig_gmv, g.fig_corr_crypto],
         run="print(n_params(25))\nprint(fig_dcc_sim(reps=10))\nprint(fig_gmv(hold=63))\nprint(fig_corr_crypto())",
         charts=['ats_ch8_dcc_sim', 'ats_ch8_gmv', 'ats_ch8_corr_crypto']),
    dict(name='ATS_ch8_ai_robustness',
         desc='AI mini-case: how robust is the HARQ gain over HAR for Bitcoin and Ether across 12 analysis choices '
              '(estimation window, treatment of implausible forecasts, realised measure)?',
         keywords='robustness, HARQ, HAR, forecast comparison, specification grid, AI for science',
         consts=CONSTS, funcs=DATAF + HAR + [g.fig_ai_case], run="r = fig_ai_case()\nprint({k: r[k] for k in r if k != 'rows'})",
         charts=['ats_ch8_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar8 as s
    SEMC = [f'A2J, A2I, A2T = np.array({s.A2J.tolist()!r}), np.array({s.A2I.tolist()!r}), {s.A2T!r}', f'A3 = {s.A3!r}',
            f'A4 = {s.A4!r}', f'A5R = np.array({s.A5R.tolist()!r})', f'A6 = {s.A6!r}', f'A7 = {s.A7!r}', f'A8 = {s.A8!r}',
            f'A9 = {s.A9!r}', f'A10 = {s.A10!r}', f'ETF_DATE = {s.ETF_DATE!r}', 'from math import gamma as gamma_fn']
    QUANTLETS.append(dict(
        name='ATS_ch8_seminar',
        desc='Seminar 8 of Advanced Time Series Analysis and Forecasting: the QML variance and its robust standard error; '
             'the noise bias of realised variance and the optimal sampling frequency; RV, BV and the jump test on a toy '
             'day; HAR as a restricted AR(22); robust and non-robust losses; jumps in Ether; HAR for the DAX; HARQ for '
             'Ether; QML for EUR/RON; GARCH-MIDAS for the BET with Romanian industrial production; Bitcoin before and '
             'after the US spot ETFs; an AI answer to audit.',
        keywords='seminar, GARCH, QML, realised variance, jumps, HAR, HARQ, GARCH-MIDAS, Romania, Bitcoin',
        consts=CONSTS + SEMC, data=DATA,
        funcs=DATAF + GARCH + MIDAS + JUMP + HAR + [g.parzen,
                                                    s.a1_const_var, s.a2_sandwich, s.a3_noise, s.a4_tsrv, s.a5_toy_day,
                                                    s.a6_power, s.a7_har_ar22, s.a8_attenuation, s.a9_patton, s.a10_dcc,
                                                    s.b1_eth_jumps, s.b2_har_dax, s.b3_harq_eth, s.b4_eurron, s.ro_ip,
                                                    s.b5_midas_bet, s.c1_btc_etf, s.c2_check],
        run="print(a1_const_var())\nprint(a3_noise())\nprint(a5_toy_day())\nprint(a7_har_ar22())\nprint(a9_patton())\n"
            "print(b1_eth_jumps())\nprint(b2_har_dax())\nprint(b4_eurron())",
        charts=['ch8_sem_b1', 'ch8_sem_b2', 'ch8_sem_b4']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 8, 'Advanced volatility modelling: realised measures, HAR and multivariate GARCH', HERE, data=DATA,
              submitted=SUBMITTED)
