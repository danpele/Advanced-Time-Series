"""
build_quantlets.py -- Quantlet folders of Chapter 13 (ATS): foundation models and conformal prediction
======================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
The notebooks run shorter evaluation windows than the slides (the constants are set in the first code cell), so that
the foundation models finish in minutes on a Colab CPU.
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_13/generate_all_charts.py && python3 Quantlets/Ch_13/seminar13.py
      python3 Quantlets/Ch_13/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 13
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import fm_core as c                             # noqa: E402
import generate_all_charts as g                 # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Tuesday, 6 October 2026'
DATA = ('Romanian hourly electricity load (Energy-Charts, ENTSO-E transparency data) and Bucharest temperature (Open-Meteo '
        'historical archive), HICP annual inflation of the 27 EU countries (Eurostat), realised variance of Bitcoin '
        '(Binance 5-minute returns) and of the S&P 500 (Oxford-Man realized library v0.3, Heber, Lunde, Shephard and Sheppard 2009; archived copy downloaded '
        'from the Internet Archive by read_omi), EODHD daily closes of the BET, DAX, '
        'WIG20, S&P 500 and NVIDIA (data/market of the ATS repository); all read without a key')
INSTALL = ('# open foundation models on a CPU (Colab: installed here if missing; a model that does not install is skipped)\n'
           '%pip install -q chronos-forecasting timesfm tirex-ts')
EXTRA_IMPORTS = 'import io\nimport math\nimport hashlib\nimport time\nimport inspect\nimport types'
TORCH_IMPORT = ('try:\n    import torch\n    from torch import nn\n    TORCH = True\nexcept ImportError:\n    torch = None\n'
                '    nn = types.SimpleNamespace(Module=object)\n    TORCH = False')
CONSTS = [EXTRA_IMPORTS, TORCH_IMPORT, f'SEED = {g.SEED!r}', f'REAL_RAW = {g.REAL_RAW!r}',
          "REAL_DIR = next((os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..') if os.path.isdir(os.path.join(d, 'data', 'realized'))), '')",
          f'LOAD_API = {g.LOAD_API!r}', f'METEO_API = {g.METEO_API!r}', f'LOAD_YEARS = {g.LOAD_YEARS!r}',
          f'LOAD_END = {g.LOAD_END!r}', f'LOAD_WIN, LOAD_RES = {g.LOAD_WIN!r}, {g.LOAD_RES!r}', f'LOAD_CTX = {g.LOAD_CTX!r}',
          f'EU27 = {g.EU27!r}', f'HICP = {g.HICP!r}', f'RELEASE = {g.RELEASE!r}',
          f'PRE_END, POST_START = {g.PRE_END!r}, {g.POST_START!r}', f'FMS = {g.FMS!r}',
          "FM_COL = {'Chronos-Bolt small': st.Orange, 'Chronos-2': st.IDAred, 'TimesFM 2.5': st.Purple, 'TiRex': st.Teal, "
          "'Chronos-Bolt tiny': st.Amber, 'Chronos-Bolt mini': st.Amber, 'Chronos-Bolt base': st.Amber}",
          '_MEM = {}', f'FM_SPECS = {c.FM_SPECS!r}', f'DECILES = {c.DECILES!r}', f'WIDE = {c.WIDE!r}', '_FM = {}',
          '# shorter windows than the slides (the slides: LOAD_EVAL 2025-01-01, INFL first 2012-01-01, RV_FIRST 2021/2010, RET_FIRST 2016-01-04)',
          "LOAD_EVAL = '2026-03-01'", "INFL = dict(start='2000-01-01', first='2022-01-01', H=12)",
          "RV_FIRST = {'btc': '2024-06-03', 'spx': '2020-01-02'}", "RET_FIRST = '2023-01-02'", "GS_START = '2003-01-01'"]
CORE = [c.pinball, c.crps_q, c.wql, c.interval_score, c.qlike, c.gmean, c.hac_var, c.dm_test, c.mcs, c.holm, c.bh,
        c.kupiec, c.christoffersen, c.seasonal_naive, c.ar_fit, c.ar_forecast, c.ets_forecast, c.har_design,
        c.har_forecast, c.garch11_fit, c.garch11_filter, c.set_seed, c.DLinear, c.NBeats, c.fit_global,
        c.predict_global, c.fm_load, c.fm_levels, c.fm_params, c._interp_levels, c.fm_forecast, c.chronos_tokenise,
        c.conformal_quantile, c.split_conformal, c.cqr, c.online_threshold, c.ar_scorecaster, c.enbpi]
DATAF = [g.save, g.get_bytes, g.fm_cached, g.read_realized, g.ro_load_hourly, g.bucharest_temperature,
         g.orthodox_easter, g.ro_holidays, g.eu_hicp, g.btc_rv, g.spx_rv]
BASE = DATAF + CORE

QUANTLETS = [
    dict(name='ATS_ch13_pretraining',
         desc='Pretraining of time series foundation models: the Chronos tokeniser (mean scaling and 4093 uniform bins on '
              '[-15, 15]) on the BET index and the clipping of a series that leaves the range; accuracy against the number '
              'of parameters for the Chronos-Bolt family (tiny, mini, small, base), Chronos-2, TimesFM 2.5 and TiRex on '
              'Romanian load, EU inflation and Bitcoin realised variance.',
         keywords='foundation models, tokenisation, mean scaling, quantisation, scaling laws, Chronos, TimesFM, TiRex',
         consts=CONSTS, funcs=BASE + [g.fig_tokens, g.load_baselines, g.load_deep, g.load_fm, g.load_all, g.infl_forecasts,
                                      g.rv_forecasts, g.rv_forecasts_extra, g.fig_scaling],
         run='print(fig_tokens())\nprint(fig_scaling())', charts=['ats_ch13_tokens', 'ats_ch13_scaling']),
    dict(name='ATS_ch13_zero_shot',
         desc='Zero-shot forecasts of open foundation models on a CPU: Chronos-2 on four data sets; Romanian day-ahead load '
              'with Chronos-Bolt, Chronos-2, TimesFM 2.5 and TiRex against the weekly naive, the expert ARX of Ziel and '
              'Weron (2018), DLinear and N-BEATS (MAE, CRPS, coverage, DM tests, Model Confidence Set); Chronos-2 with '
              'in-context calendar and temperature covariates.',
         keywords='zero-shot forecasting, Chronos-2, covariates, electricity load, Romania, expert ARX, Model Confidence Set',
         consts=CONSTS, funcs=BASE + [g.fig_zeroshot, g.load_baselines, g.load_deep, g.load_fm, g.load_all, g.fig_load,
                                      g.fig_covariates],
         run='print(fig_zeroshot())\nprint(fig_load())\nprint(fig_covariates())',
         charts=['ats_ch13_zeroshot', 'ats_ch13_load', 'ats_ch13_covariates']),
    dict(name='ATS_ch13_benchmark',
         desc='Benchmark methodology: EU HICP inflation (27 countries, rolling origins, h = 1-12) with the random walk, '
              'AR(p), damped ETS, DLinear, N-BEATS and four foundation models (geometric means of relative MAE, bootstrap '
              'over countries, CRPS); Romanian forecasts from three origins; 27 DM tests with Holm and Benjamini-Hochberg; '
              'realised variance of Bitcoin and the S&P 500 against HAR; windows before and after the model releases; how '
              'much a random benchmark subset changes the verdict.',
         keywords='benchmark, contamination, multiple testing, Holm, Benjamini-Hochberg, inflation, realised variance, HAR',
         consts=CONSTS, funcs=BASE + [g.infl_forecasts, g.fig_inflation, g.fig_ro_inflation, g.fig_multiple,
                                      g.rv_forecasts, g.fig_rv, g.load_baselines, g.load_deep, g.load_fm, g.load_all,
                                      g.fig_contamination, g.fig_ai_case],
         run=('print(fig_inflation())\nprint(fig_ro_inflation())\nprint(fig_multiple())\nprint(fig_rv())\n'
              'print(fig_contamination())\nprint(fig_ai_case(reps=500))'),
         charts=['ats_ch13_inflation', 'ats_ch13_ro_inflation', 'ats_ch13_multiple', 'ats_ch13_rv',
                 'ats_ch13_contamination', 'ats_ch13_ai_case']),
    dict(name='ATS_ch13_conformal_basics',
         desc='Split conformal prediction: the Beta law of coverage given the calibration set (n = 50, 500); conformalized '
              'quantile regression on the synthetic design of Romano, Patterson and Candes (2019, Figure 1) against split '
              'conformal with a mean model.',
         keywords='conformal prediction, split conformal, exchangeability, coverage, CQR, quantile regression',
         consts=CONSTS, funcs=BASE + [g.fig_split_coverage, g.cqr_data, g.fig_cqr],
         run='print(fig_split_coverage(reps=2000))\nprint(fig_cqr())', charts=['ats_ch13_split_coverage', 'ats_ch13_cqr']),
    dict(name='ATS_ch13_conformal_time',
         desc='Conformal prediction for dependent data: weighted conformal under changepoints (Barber et al. 2023); the '
              'volatility design of Gibbs and Candes (2021) with ACI on the S&P 500, BET and NVIDIA; the step size gamma; '
              'conditional coverage by volatility regime; quantile tracking, conformal PID (Angelopoulos, Candes and '
              'Tibshirani 2023) and EnbPI (Xu and Xie 2021) on Romanian day-ahead load.',
         keywords='adaptive conformal inference, conformal PID, quantile tracking, EnbPI, weighted conformal, GARCH, coverage',
         consts=CONSTS, funcs=BASE + [g.fig_weighted, g.garch_scores, g.local_cov, g.fig_aci, g.fig_aci_gamma,
                                      g.fig_condcov, g.load_baselines, g.load_deep, g.load_fm, g.load_all,
                                      g.load_scores, g.fig_pid],
         run=('print(fig_weighted(reps=50))\nprint(fig_aci())\nprint(fig_aci_gamma())\nprint(fig_condcov())\n'
              'print(fig_pid(n_cal=30))'),
         charts=['ats_ch13_weighted', 'ats_ch13_aci', 'ats_ch13_aci_gamma', 'ats_ch13_condcov', 'ats_ch13_pid']),
    dict(name='ATS_ch13_calibration',
         desc='Calibrating foundation-model intervals: raw 10-90% bands of Chronos-Bolt, Chronos-2, TimesFM 2.5 and TiRex '
              'and online CQR (ACI) at 80% and 95% on Romanian load, Bitcoin log RV, EU inflation and BET returns; VaR 1% '
              'and 5% of the BET and the S&P 500 from Chronos-2 and from conformalised deciles against GARCH-t, with '
              'Kupiec and Christoffersen backtests.',
         keywords='calibration, conformal prediction, foundation models, VaR, backtesting, Kupiec, Christoffersen',
         consts=CONSTS, funcs=BASE + [g.load_baselines, g.load_deep, g.load_fm, g.load_all, g.rv_forecasts,
                                      g.infl_forecasts, g.returns_fm, g.garch_var, g.fig_fm_calib, g.fig_fm_var],
         run='print(fig_fm_calib(w=60, w_infl=24))\nprint(fig_fm_var(w=250))', charts=['ats_ch13_fm_calib', 'ats_ch13_fm_var']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar13 as s
    SEMC = [f'A1 = {s.A1!r}', f'A2 = {s.A2!r}', f'A3 = {s.A3!r}', f'A4 = {s.A4!r}', f'A5 = {s.A5!r}', f'A6 = {s.A6!r}',
            f'A7 = {s.A7!r}', f'A8 = {s.A8!r}', f'B1 = {s.B1!r}', f'B5 = {s.B5!r}', f'B6 = {s.B6!r}', f'B7 = {s.B7!r}',
            f'B8 = {s.B8!r}']
    SEMF = [g.load_baselines, g.garch_scores, g.local_cov]
    QUANTLETS.append(dict(
        name='ATS_ch13_seminar',
        desc='Seminar 13 of Advanced Time Series Analysis and Forecasting: split conformal by hand and the Beta law of '
             'coverage, ACI and quantile tracking by hand, CQR and weighted conformal quantiles, the Chronos tokeniser and '
             'its range; Romanian load after the model releases, Chronos-2 with calendar covariates, static, rolling and '
             'adaptive conformal intervals for BET returns, the ACI volatility design on the DAX, online CQR of Chronos-Bolt '
             'forecasts of Bitcoin RV, EnbPI on the load peak, CEE inflation with Holm and Benjamini-Hochberg, VaR of the '
             'WIG20; a pre-registered inflation forecast; an AI answer to audit.',
        keywords='seminar, foundation models, conformal prediction, ACI, CQR, EnbPI, multiple testing, VaR',
        consts=CONSTS + SEMC,
        funcs=BASE + SEMF + [s.a1_split, s.a2_beta, s.a3_aci, s.a4_qt, s.a5_cqr, s.a6_weighted, s.a7_tokens, s.a8_range,
                             s.b1_load_zero_shot, s.b2_load_covariates, s.b3_bet_conformal, s.b4_dax_aci, s.b5_btc_cqr,
                             s.b6_load_enbpi, s.b7_cee_inflation, s.b8_wig_var, s.c1_preregistered, s.c2_check],
        run="print(a1_split())\nprint(a3_aci())\nprint(a5_cqr())\nprint(a7_tokens())\nprint(b1_load_zero_shot())\nprint(b3_bet_conformal())\nprint(b5_btc_cqr())\nprint(b7_cee_inflation())",
        charts=['ch13_sem_b1', 'ch13_sem_b3', 'ch13_sem_b5', 'ch13_sem_b7']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 13, 'Foundation models and conformal prediction', HERE, data=DATA, submitted=SUBMITTED,
              install=INSTALL)
