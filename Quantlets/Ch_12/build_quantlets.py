"""
build_quantlets.py -- Quantlet folders of Chapter 12 (ATS): machine learning and deep learning for time series
=============================================================================================================
Metainfo.txt + self-contained Colab notebook + charts for each Quantlet (Quantlets/common/ats_quantlets.py).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_12/generate_all_charts.py && python3 Quantlets/Ch_12/seminar12.py
      python3 Quantlets/Ch_12/build_quantlets.py
      python3 notebooks/add_colab_banner.py && python3 notebooks/split_seminar_notebooks.py 12
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import generate_all_charts as g                 # noqa: E402
import ml_core as c                             # noqa: E402
from ats_quantlets import build_all             # noqa: E402

SUBMITTED = 'Tuesday, 6 October 2026'
DATA = ('Romanian hourly electricity load from Energy-Charts (ENTSO-E transparency data, public API, 2023-2026); Eurostat '
        'HICP annual rates of the 27 EU countries (prc_hicp_minr); Oxford-Man Institute realized library v0.3 (Heber, Lunde, '
        'Shephard and Sheppard 2009), six equity indices, 2000-2022 (archived copy, downloaded from the Internet Archive by '
        'read_omi, not redistributed), and Bitcoin and Ether realised measures from Binance '
        'one-minute prices (data/realized of the ATS repository); the M4 hourly series and evaluation file (M4-methods '
        'repository, Makridakis, Spiliotis and Assimakopoulos 2020)')
INSTALL = "# PyTorch, scikit-learn and openpyxl are preinstalled in Colab\n# !pip install torch scikit-learn openpyxl"
CONSTS = ['import io\nimport sys\nimport math\nimport itertools\nimport urllib.error',
          "try:                                            # PyTorch is preinstalled in Colab\n"
          "    import torch\n    from torch import nn\n    TORCH = True\n"
          "except ImportError:\n    import types\n    torch = None\n    nn = types.SimpleNamespace(Module=object)\n    TORCH = False",
          f'SEED = {g.SEED!r}', f'REAL_RAW = {g.REAL_RAW!r}',
          "REAL_DIR = next((os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..')\n"
          "                 if os.path.isdir(os.path.join(d, 'data', 'realized'))), '')",
          f'OMI_NAMES = {g.OMI_NAMES!r}', f'LOAD_API = {g.LOAD_API!r}', f'LOAD_YEARS = {g.LOAD_YEARS!r}',
          f'LOAD_END = {g.LOAD_END!r}', f'LOAD_EVAL = {g.LOAD_EVAL!r}', f'EU27 = {g.EU27!r}', f'HICP = {g.HICP!r}',
          f'INFL = {g.INFL!r}', f'M4_RAW = {g.M4_RAW!r}', f'M4H = {g.M4H!r}', f'ZENG = {g.ZENG!r}', f'RV = {g.RV!r}',
          'TAUS9 = np.arange(1, 10) / 10', f'MONO = {g.MONO!r}', f'DEEPAR_LAGS = {c.DEEPAR_LAGS!r}', '_MEM = {}']
CORE = [c.hac_var, c.dm_test, c.mcs, c.qlike, c.pinball, c.smape, c.mase, c.embed, c.ols, c.loocv_ols, c.ar_sim,
        c.random_stationary_ar, c.bhk_trial, c.purged_folds, c.standardise, c.penalised_fit, c.QRF, c.set_seed, c.MLPNet,
        c.RNNNet, c.TCNNet, c.LinearNet, c.PatchTransformer, c.NBeatsBlock, c.NBeatsNet, c.fit_torch, c.predict_torch,
        c.grad_through_time, c.DeepARNet, c.deepar_features, c.deepar_train, c.deepar_sample, c.shapley_groups]
DATAF = [g.save, g.get_bytes, g.read_realized, g.omi, g.ro_load_hourly, g.orthodox_easter, g.ro_holidays, g.eu_hicp,
         g.m4_hourly]
BASE = DATAF + CORE

QUANTLETS = [
    dict(name='ATS_ch12_validation',
         desc='Learning from dependent data: the four data sets of the chapter; the Monte Carlo design of Bergmeir, Hyndman '
              'and Koo (2018, Section 4) comparing 5-fold CV, LOOCV, non-dependent CV and out-of-sample evaluation for AR(3), '
              'MA(1) and a seasonal AR fitted to US accidental deaths; leakage through overlapping targets and a time index '
              'with a random forest under random, blocked and purged folds.',
         keywords='cross-validation, time series, leakage, blocked cross-validation, purged cross-validation, autoregression',
         consts=CONSTS, funcs=BASE + [g.fig_overview, g.usaccdeaths_sar, g.cv_experiment, g.fig_cv_bhk, g.leakage_experiment, g.fig_leakage],
         run="print(fig_overview())\nr = fig_cv_bhk(reps=200)\nprint({k: v['AR(3)'] for k, v in r.items() if k in ('AR(3)', 'MA(1)', 'SAR')})\n"
             "print(fig_leakage(reps=10))",
         charts=['ats_ch12_overview', 'ats_ch12_cv_bhk', 'ats_ch12_leakage']),
    dict(name='ATS_ch12_global_models',
         desc='Global and local models (Montero-Manso and Hyndman 2021) for the annual HICP inflation of the 27 EU countries '
              'across memory lengths at 1 and 12 months; ridge, lasso, adaptive lasso, elastic net and post-lasso OLS on the '
              'EU panel for Romanian inflation 12 months ahead, with selection frequencies and Diebold-Mariano tests.',
         keywords='global models, local models, lasso, adaptive lasso, elastic net, inflation, Eurostat HICP, Romania',
         consts=CONSTS, funcs=BASE + [g.lagmat, g.global_local, g.fig_global_local, g.ols_coef, g.ro_highdim, g.fig_ro_lasso],
         run="print(fig_global_local())\nprint(fig_ro_lasso())", charts=['ats_ch12_global_local', 'ats_ch12_ro_lasso']),
    dict(name='ATS_ch12_trees',
         desc='Tree ensembles for Romanian day-ahead electricity load (Energy-Charts, ENTSO-E data): the expert ARX of Ziel '
              'and Weron (2018) against a random forest with quantile regression forest bands (Meinshausen 2006), histogram '
              'gradient boosting with and without monotone constraints and quantile boosting; MAE, pinball loss, coverage, '
              'Diebold-Mariano tests and the Model Confidence Set; partial dependence under the monotone constraint.',
         keywords='random forest, quantile regression forest, gradient boosting, LightGBM, monotone constraints, electricity load, Romania',
         consts=CONSTS, funcs=BASE + [g.load_features, g.load_tree_forecasts, g.fig_load_trees, g.fig_monotone],
         run="print(fig_load_trees(n_trees=50, refit='QS'))\nprint(fig_monotone())",
         charts=['ats_ch12_load_trees', 'ats_ch12_monotone']),
    dict(name='ATS_ch12_recurrent',
         desc='Recurrent and convolutional networks: gradients through time at initialisation for a tanh RNN, a GRU and an '
              'LSTM with forget-gate bias 0, 1 and 3; S&P 500 realised variance forecasts at 1, 5 and 22 days from HAR, an '
              'MLP, an LSTM, a TCN and boosting on 22 lags (expanding window), QLIKE, Diebold-Mariano and MCS.',
         keywords='recurrent neural network, LSTM, GRU, vanishing gradients, temporal convolutional network, HAR, realised variance',
         consts=CONSTS, funcs=BASE + [g.fig_vanishing, g.rv_windows, g.har_feats, g.rv_forecasts, g.evaluate_rv, g.fig_rv_deep],
         run="print(fig_vanishing())\nprint(fig_rv_deep(horizons=(1, 22), epochs=30)['eval'])",
         charts=['ats_ch12_vanishing', 'ats_ch12_rv_deep']),
    dict(name='ATS_ch12_transformers',
         desc='The protocol of Zeng et al. (2023) on Romanian hourly load: look-back 336 hours, horizons 96 and 336, chronological '
              '7:1:2 split, MSE and MAE on the z-scored series; repeat, seasonal naive, Linear, NLinear, DLinear, a patch '
              'Transformer in the spirit of PatchTST and the same Transformer with one token per hour.',
         keywords='Transformer, attention, DLinear, NLinear, PatchTST, long-horizon forecasting, electricity load',
         consts=CONSTS, funcs=BASE + [g.zeng_data, g.zeng_windows, g.zeng_experiment, g.fig_zeng],
         run="print(fig_zeng(seeds=(0,), epochs=10)['res'])", charts=['ats_ch12_zeng']),
    dict(name='ATS_ch12_global_deep',
         desc='Global deep models on the M4 hourly subset (414 series, horizon 48): Naive, seasonal naive and Naive 2 (which '
              'reproduce the official M4 evaluation), global DLinear, N-BEATS and N-HiTS (sMAPE, MASE, OWA, compared with the '
              'official results of the M4 entries); a DeepAR-type Gaussian LSTM with ancestral sampling, weighted quantile '
              'loss and coverage at several training budgets.',
         keywords='N-BEATS, N-HiTS, DeepAR, global models, M4 competition, probabilistic forecasting, quantile loss',
         consts=CONSTS, funcs=BASE + [g.naive2, g.m4_windows, g.scaled_mae, g.m4_global, g.m4_official, g.m4_scores, g.fig_m4, g.fig_deepar],
         run="print(fig_m4(seeds=(0,))['scores'])\nprint(fig_deepar(steps=1000, checkpoints=(500,)))",
         charts=['ats_ch12_m4', 'ats_ch12_deepar']),
    dict(name='ATS_ch12_interpretation',
         desc='Interpretation and honest benchmarks: exact Shapley values of three lag groups for boosting on S&P 500 log '
              'realised variance against the HAR coefficients; attention received by the input patches of the patch '
              'Transformer against occlusion importance; seed dispersion of an MLP against HAR and a simulation of data '
              'snooping (the best of K equally good models).',
         keywords='Shapley values, SHAP, attention, interpretability, data snooping, random seeds, benchmark',
         consts=CONSTS, funcs=BASE + [g.rv_windows, g.har_feats, g.rv_forecasts, g.fig_shap, g.zeng_data, g.zeng_windows,
                                      g.zeng_experiment, g.fig_zeng, g.torch_no_grad, g.torch_tensor, g.fig_attention,
                                      g.seeds_snooping, g.snooping_sim, g.fig_snooping],
         run="print(fig_shap())\nprint(fig_attention())\nprint(fig_snooping(n_seeds=5, epochs=30))",
         charts=['ats_ch12_shap', 'ats_ch12_attention', 'ats_ch12_snooping']),
    dict(name='ATS_ch12_ai_case',
         desc='AI mini-case: do learners beat HAR across markets? Six Oxford-Man indices, horizons 1, 5 and 22 days, an MLP and '
              'boosting against HAR with the same expanding design; QLIKE ratios and Diebold-Mariano tests in every cell.',
         keywords='pre-registration, realised volatility, HAR, machine learning, deep learning, Diebold-Mariano, robustness',
         consts=CONSTS, funcs=BASE + [g.rv_windows, g.har_feats, g.rv_forecasts, g.evaluate_rv, g.fig_ai_case],
         run="print(fig_ai_case(epochs=30))", charts=['ats_ch12_ai_case']),
]

try:                                   # seminar code (instructor files, see .gitignore)
    import seminar12 as s
    SEMC = [f'{k} = {getattr(s, k)!r}' for k in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'PEAK')]
    SEMF = [g.lagmat, g.global_local, g.ols_coef, g.ro_highdim, g.load_features, g.rv_windows, g.har_feats, g.rv_forecasts,
            g.evaluate_rv, g.naive2, g.m4_windows, g.m4_global, g.m4_scores]
    QUANTLETS.append(dict(
        name='ATS_ch12_seminar',
        desc='Seminar 12 of Advanced Time Series Analysis and Forecasting: lasso, ridge, adaptive lasso and elastic net under an '
             'orthonormal design, the variance of bagging, boosting as gradient descent, gradients through an RNN and an '
             'LSTM, attention by hand, DLinear as one linear map; cross-validation of HAR on FTSE 100 realised variance, a '
             'random forest with a time index, local and global AR models of EU inflation, the panel lasso for Romania, '
             'quantile forests and monotone boosting for the Romanian evening-peak load, LSTM against HAR, DLinear and '
             'N-BEATS on M4 hourly series; learners against HAR for Bitcoin and Ether; an AI answer to audit.',
        keywords='seminar, cross-validation, lasso, quantile regression forest, LSTM, HAR, N-BEATS, DLinear',
        consts=CONSTS + SEMC,
        funcs=BASE + SEMF + [s.soft, s.a1_lasso_ridge, s.a2_adaptive_enet, s.a3_bagging, s.a4_boosting, s.a5_rnn, s.a6_lstm,
                             s.a7_attention, s.a8_dlinear, s.cv_estimates, s.rv_targets, s.b1_cv_har, s.b2_cv_rf, s.b3_global,
                             s.b4_lasso, s.peak_data, s.peak_arx, s.b5_qrf_peak, s.b6_monotone_peak, s.b7_lstm_ftse,
                             s.b8_m4_subset, s.c1_crypto, s.c2_check],
        run="print(a1_lasso_ridge())\nprint(a3_bagging())\nprint(a5_rnn())\nprint(a7_attention())\nprint(b1_cv_har())\n"
            "print(b3_global())\nprint(b5_qrf_peak())\nprint(b7_lstm_ftse(seeds=(0,)))",
        charts=['ch12_sem_b1', 'ch12_sem_b3', 'ch12_sem_b5', 'ch12_sem_b7']))
except ImportError:
    pass

if __name__ == '__main__':
    build_all(QUANTLETS, 12, 'Machine learning and deep learning for time series', HERE, data=DATA, submitted=SUBMITTED,
              install=INSTALL)
