r"""
ch12_common.py -- shared helpers of the Chapter 12 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_12/ch12_numbers.json (generate_all_charts.py) and
sem12_results.json (seminar12.py); the clickable citations of Chapter 12 (DOIs checked against Crossref, arXiv and the
proceedings pages, 6 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_12')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_12'
MONTHS_RO = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie',
             'octombrie', 'noiembrie', 'decembrie']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']


def T(en, ro):
    """Bilingual text; in raw strings a prime may be written as \\' and becomes '."""
    return f'⟦{en}||{ro}⟧'.replace("\\'", "'")


def V2(en, ro):
    """A bilingual value that can sit inside ⟦..||..⟧ text: resolved in the written files by finalize()."""
    return f'⟪{en}¦{ro}⟫'


def finalize(paths):
    """Resolve the ⟪en¦ro⟫ values in the written decks (EN file first, RO file second)."""
    for p, k in zip(paths, (1, 2)):
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'⟪(.*?)¦(.*?)⟫', lambda m: m.group(k), s)
        open(p, 'w', encoding='utf-8').write(s)


def month(s):
    y, m = int(s[:4]), int(s[5:7]) - 1
    return V2(f'{MONTHS_EN[m]} {y}', f'{MONTHS_RO[m]} {y}')


def day(s):
    """'2025-05-09' -> 9 May 2025 / 9 mai 2025."""
    y, m, d = int(s[:4]), int(s[5:7]) - 1, int(s[8:10])
    return V2(f'{d} {MONTHS_EN[m]} {y}', f'{d} {MONTHS_RO[m]} {y}')


def quarter(s):
    """'2026-06-01' (third month) or '2026Q2' -> 2026Q2 / T2 2026."""
    if 'Q' in s:
        y, q = int(s[:4]), int(s[-1])
    else:
        y, q = int(s[:4]), (int(s[5:7]) - 1) // 3 + 1
    return V2(f'{y}Q{q}', f'T{q} {y}')


def minus_fix(V):
    """Negative numbers: a real minus sign in text and in math mode."""
    for k, v in list(V.items()):
        if isinstance(v, str) and v.startswith('⁅-'):
            V[k] = '⁅\\ensuremath{-}' + v[2:]


def load():
    with open(os.path.join(QL, 'ch12_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem12_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
AX = 'https://arxiv.org/abs/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'BaiK': (AX + '1803.01271', 'Bai, Kolter and Koltun (2018)', 'Bai, Kolter și Koltun (2018)',
             r'Bai, S., Kolter, J. Z., \& Koltun, V. (2018). An empirical evaluation of generic convolutional and recurrent networks for sequence modeling. arXiv:1803.01271.'),
    'BCH': ('10.1093/restud/rdt044', 'Belloni, Chernozhukov and Hansen (2014)', 'Belloni, Chernozhukov și Hansen (2014)',
            r'Belloni, A., Chernozhukov, V., \& Hansen, C. (2014). Inference on treatment effects after selection among high-dimensional controls. \textit{The Review of Economic Studies}, 81(2), 608--650.'),
    'BSF': ('10.1109/72.279181', 'Bengio, Simard and Frasconi (1994)', 'Bengio, Simard și Frasconi (1994)',
            r'Bengio, Y., Simard, P., \& Frasconi, P. (1994). Learning long-term dependencies with gradient descent is difficult. \textit{IEEE Transactions on Neural Networks}, 5(2), 157--166.'),
    'Ben': ('10.1145/3533382', 'Benidis et al.\\ (2022)', 'Benidis et al.\\ (2022)',
            r'Benidis, K., Rangapuram, S. S., Flunkert, V., Wang, Y., et al.\ (2022). Deep learning for time series forecasting: Tutorial and literature survey. \textit{ACM Computing Surveys}, 55(6), 1--36.'),
    'BB': ('10.1016/j.ins.2011.12.028', 'Bergmeir and Benítez (2012)', 'Bergmeir și Benítez (2012)',
           r'Bergmeir, C., \& Benítez, J. M. (2012). On the use of cross-validation for time series predictor evaluation. \textit{Information Sciences}, 191, 192--213.'),
    'BHK': ('10.1016/j.csda.2017.11.003', 'Bergmeir, Hyndman and Koo (2018)', 'Bergmeir, Hyndman și Koo (2018)',
            r'Bergmeir, C., Hyndman, R. J., \& Koo, B. (2018). A note on the validity of cross-validation for evaluating autoregressive time series prediction. \textit{Computational Statistics \& Data Analysis}, 120, 70--83.'),
    'Berk': ('10.1214/12-AOS1077', 'Berk et al.\\ (2013)', 'Berk et al.\\ (2013)',
             r'Berk, R., Brown, L., Buja, A., Zhang, K., \& Zhao, L. (2013). Valid post-selection inference. \textit{The Annals of Statistics}, 41(2), 802--837.'),
    'BM': ('10.1214/15-AOS1315', 'Basu and Michailidis (2015)', 'Basu și Michailidis (2015)',
           r'Basu, S., \& Michailidis, G. (2015). Regularized estimation in sparse high-dimensional time series models. \textit{The Annals of Statistics}, 43(4), 1535--1567.'),
    'BreA': ('10.1007/BF00058655', 'Breiman (1996)', 'Breiman (1996)',
             r'Breiman, L. (1996). Bagging predictors. \textit{Machine Learning}, 24(2), 123--140.'),
    'BreB': ('10.1023/A:1010933404324', 'Breiman (2001)', 'Breiman (2001)',
             r'Breiman, L. (2001). Random forests. \textit{Machine Learning}, 45(1), 5--32.'),
    'Buc': ('10.1093/jjfinec/nbaa008', 'Bucci (2020)', 'Bucci (2020)',
            r'Bucci, A. (2020). Realized volatility forecasting with neural networks. \textit{Journal of Financial Econometrics}, 18(3), 502--531.'),
    'BCN': ('10.1093/biomet/81.2.351', 'Burman, Chow and Nolan (1994)', 'Burman, Chow și Nolan (1994)',
            r'Burman, P., Chow, E., \& Nolan, D. (1994). A cross-validatory method for dependent data. \textit{Biometrika}, 81(2), 351--358.'),
    'NHiTS': ('10.1609/aaai.v37i6.25854', 'Challu et al.\\ (2023)', 'Challu et al.\\ (2023)',
              r'Challu, C., Olivares, K. G., Oreshkin, B. N., Garza Ramirez, F., Mergenthaler Canseco, M., \& Dubrawski, A. (2023). NHITS: Neural hierarchical interpolation for time series forecasting. \textit{Proceedings of the AAAI Conference on Artificial Intelligence}, 37(6), 6989--6997.'),
    'CG': ('10.1145/2939672.2939785', 'Chen and Guestrin (2016)', 'Chen și Guestrin (2016)',
           r'Chen, T., \& Guestrin, C. (2016). XGBoost: A scalable tree boosting system. \textit{Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining}, 785--794.'),
    'Cho': ('10.3115/v1/D14-1179', 'Cho et al.\\ (2014)', 'Cho et al.\\ (2014)',
            r'Cho, K., van Merriënboer, B., Gulcehre, C., Bahdanau, D., Bougares, F., Schwenk, H., \& Bengio, Y. (2014). Learning phrase representations using RNN encoder--decoder for statistical machine translation. \textit{Proceedings of EMNLP 2014}, 1724--1734.'),
    'CSV': ('10.1093/jjfinec/nbac020', 'Christensen, Siggaard and Veliyev (2023)', 'Christensen, Siggaard și Veliyev (2023)',
            r'Christensen, K., Siggaard, M., \& Veliyev, B. (2023). A machine learning approach to volatility forecasting. \textit{Journal of Financial Econometrics}, 21(5), 1680--1727.'),
    'Cor': ('10.1093/jjfinec/nbp001', 'Corsi (2009)', 'Corsi (2009)',
            r'Corsi, F. (2009). A simple approximate long-memory model of realized volatility. \textit{Journal of Financial Econometrics}, 7(2), 174--196.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'Fri': ('10.1214/aos/1013203451', 'Friedman (2001)', 'Friedman (2001)',
            r'Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. \textit{The Annals of Statistics}, 29(5), 1189--1232.'),
    'GSC': ('10.1162/089976600300015015', 'Gers, Schmidhuber and Cummins (2000)', 'Gers, Schmidhuber și Cummins (2000)',
            r'Gers, F. A., Schmidhuber, J., \& Cummins, F. (2000). Learning to forget: Continual prediction with LSTM. \textit{Neural Computation}, 12(10), 2451--2471.'),
    'GR': ('10.1198/016214506000001437', 'Gneiting and Raftery (2007)', 'Gneiting și Raftery (2007)',
           r'Gneiting, T., \& Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. \textit{Journal of the American Statistical Association}, 102(477), 359--378.'),
    'GCLSS': ('10.1002/jae.2910', 'Goulet Coulombe et al.\\ (2022)', 'Goulet Coulombe et al.\\ (2022)',
              r'Goulet Coulombe, P., Leroux, M., Stevanovic, D., \& Surprenant, S. (2022). How is machine learning useful for macroeconomic forecasting? \textit{Journal of Applied Econometrics}, 37(5), 920--964.'),
    'GKX': ('10.1093/rfs/hhaa009', 'Gu, Kelly and Xiu (2020)', 'Gu, Kelly și Xiu (2020)',
            r'Gu, S., Kelly, B., \& Xiu, D. (2020). Empirical asset pricing via machine learning. \textit{The Review of Financial Studies}, 33(5), 2223--2273.'),
    'Han': ('10.1198/073500105000000063', 'Hansen (2005)', 'Hansen (2005)',
            r'Hansen, P. R. (2005). A test for superior predictive ability. \textit{Journal of Business \& Economic Statistics}, 23(4), 365--380.'),
    'HLN': ('10.3982/ECTA5771', 'Hansen, Lunde and Nason (2011)', 'Hansen, Lunde și Nason (2011)',
            r'Hansen, P. R., Lunde, A., \& Nason, J. M. (2011). The model confidence set. \textit{Econometrica}, 79(2), 453--497.'),
    'OMI': ('https://web.archive.org/web/20220301022212/https://realized.oxford-man.ox.ac.uk/', 'Heber et al.\\ (2009)', 'Heber et al.\\ (2009)',
            r'Heber, G., Lunde, A., Shephard, N., \& Sheppard, K. K. (2009). Oxford-Man Institute\'s realized library, version 0.3. Oxford-Man Institute, University of Oxford.'),
    'HAB': ('10.1007/s10618-022-00894-5', 'Hewamalage, Ackermann and Bergmeir (2023)', 'Hewamalage, Ackermann și Bergmeir (2023)',
            r'Hewamalage, H., Ackermann, K., \& Bergmeir, C. (2023). Forecast evaluation for data scientists: Common pitfalls and best practices. \textit{Data Mining and Knowledge Discovery}, 37(2), 788--832.'),
    'HBB': ('10.1016/j.ijforecast.2020.06.008', 'Hewamalage, Bergmeir and Bandara (2021)', 'Hewamalage, Bergmeir și Bandara (2021)',
            r'Hewamalage, H., Bergmeir, C., \& Bandara, K. (2021). Recurrent neural networks for time series forecasting: Current status and future directions. \textit{International Journal of Forecasting}, 37(1), 388--427.'),
    'HS': ('10.1162/neco.1997.9.8.1735', 'Hochreiter and Schmidhuber (1997)', 'Hochreiter și Schmidhuber (1997)',
           r'Hochreiter, S., \& Schmidhuber, J. (1997). Long short-term memory. \textit{Neural Computation}, 9(8), 1735--1780.'),
    'HK': ('10.1016/j.ijforecast.2006.03.001', 'Hyndman and Koehler (2006)', 'Hyndman și Koehler (2006)',
           r'Hyndman, R. J., \& Koehler, A. B. (2006). Another look at measures of forecast accuracy. \textit{International Journal of Forecasting}, 22(4), 679--688.'),
    'JW': ('10.18653/v1/N19-1357', 'Jain and Wallace (2019)', 'Jain și Wallace (2019)',
           r'Jain, S., \& Wallace, B. C. (2019). Attention is not explanation. \textit{Proceedings of NAACL-HLT 2019}, 3543--3556.'),
    'JZS': ('https://proceedings.mlr.press/v37/jozefowicz15.html', 'Jozefowicz, Zaremba and Sutskever (2015)', 'Jozefowicz, Zaremba și Sutskever (2015)',
            r'Jozefowicz, R., Zaremba, W., \& Sutskever, I. (2015). An empirical exploration of recurrent network architectures. \textit{Proceedings of the 32nd International Conference on Machine Learning}, PMLR 37, 2342--2350.'),
    'KeA': ('https://proceedings.neurips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html', 'Ke et al.\\ (2017)', 'Ke et al.\\ (2017)',
            r'Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., \& Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. \textit{Advances in Neural Information Processing Systems}, 30.'),
    'KB': (AX + '1412.6980', 'Kingma and Ba (2015)', 'Kingma și Ba (2015)',
           r'Kingma, D. P., \& Ba, J. (2015). Adam: A method for stochastic optimization. \textit{International Conference on Learning Representations}. arXiv:1412.6980.'),
    'LMDW': ('10.1016/j.apenergy.2021.116983', 'Lago et al.\\ (2021)', 'Lago et al.\\ (2021)',
             r'Lago, J., Marcjasz, G., De Schutter, B., \& Weron, R. (2021). Forecasting day-ahead electricity prices: A review of state-of-the-art algorithms, best practices and an open-access benchmark. \textit{Applied Energy}, 293, 116983.'),
    'LSST': ('10.1214/15-AOS1371', 'Lee et al.\\ (2016)', 'Lee et al.\\ (2016)',
             r'Lee, J. D., Sun, D. L., Sun, Y., \& Taylor, J. E. (2016). Exact post-selection inference, with application to the lasso. \textit{The Annals of Statistics}, 44(3), 907--927.'),
    'TFT': ('10.1016/j.ijforecast.2021.03.012', 'Lim et al.\\ (2021)', 'Lim et al.\\ (2021)',
            r'Lim, B., Arık, S. Ö., Loeff, N., \& Pfister, T. (2021). Temporal fusion transformers for interpretable multi-horizon time series forecasting. \textit{International Journal of Forecasting}, 37(4), 1748--1764.'),
    'LL': ('https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html', 'Lundberg and Lee (2017)', 'Lundberg și Lee (2017)',
           r'Lundberg, S. M., \& Lee, S.-I. (2017). A unified approach to interpreting model predictions. \textit{Advances in Neural Information Processing Systems}, 30.'),
    'MSAa': ('10.1371/journal.pone.0194889', 'Makridakis, Spiliotis and Assimakopoulos (2018)', 'Makridakis, Spiliotis și Assimakopoulos (2018)',
             r'Makridakis, S., Spiliotis, E., \& Assimakopoulos, V. (2018). Statistical and machine learning forecasting methods: Concerns and ways forward. \textit{PLOS ONE}, 13(3), e0194889.'),
    'MfourA': ('10.1016/j.ijforecast.2019.04.014', 'Makridakis, Spiliotis and Assimakopoulos (2020)', 'Makridakis, Spiliotis și Assimakopoulos (2020)',
               r'Makridakis, S., Spiliotis, E., \& Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. \textit{International Journal of Forecasting}, 36(1), 54--74.'),
    'MfiveA': ('10.1016/j.ijforecast.2021.11.013', 'Makridakis, Spiliotis and Assimakopoulos (2022)', 'Makridakis, Spiliotis și Assimakopoulos (2022)',
               r'Makridakis, S., Spiliotis, E., \& Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. \textit{International Journal of Forecasting}, 38(4), 1346--1364.'),
    'MM': ('10.1016/j.jeconom.2015.10.011', 'Medeiros and Mendes (2016)', 'Medeiros și Mendes (2016)',
           r'Medeiros, M. C., \& Mendes, E. F. (2016). $\ell_1$-regularization of high-dimensional time-series models with non-Gaussian and heteroskedastic errors. \textit{Journal of Econometrics}, 191(1), 255--271.'),
    'MVVZ': ('10.1080/07350015.2019.1637745', 'Medeiros et al.\\ (2021)', 'Medeiros et al.\\ (2021)',
             r'Medeiros, M. C., Vasconcelos, G. F. R., Veiga, Á., \& Zilberman, E. (2021). Forecasting inflation in a data-rich environment: The benefits of machine learning methods. \textit{Journal of Business \& Economic Statistics}, 39(1), 98--119.'),
    'Mei': ('https://jmlr.org/papers/v7/meinshausen06a.html', 'Meinshausen (2006)', 'Meinshausen (2006)',
            r'Meinshausen, N. (2006). Quantile regression forests. \textit{Journal of Machine Learning Research}, 7, 983--999.'),
    'MR': ('https://jmlr.org/papers/v11/mohri10a.html', 'Mohri and Rostamizadeh (2010)', 'Mohri și Rostamizadeh (2010)',
           r'Mohri, M., \& Rostamizadeh, A. (2010). Stability bounds for stationary $\varphi$-mixing and $\beta$-mixing processes. \textit{Journal of Machine Learning Research}, 11, 789--814.'),
    'MMH': ('10.1016/j.ijforecast.2021.03.004', 'Montero-Manso and Hyndman (2021)', 'Montero-Manso și Hyndman (2021)',
            r'Montero-Manso, P., \& Hyndman, R. J. (2021). Principles and algorithms for forecasting groups of time series: Locality and globality. \textit{International Journal of Forecasting}, 37(4), 1632--1653.'),
    'Nie': (AX + '2211.14730', 'Nie et al.\\ (2023)', 'Nie et al.\\ (2023)',
            r'Nie, Y., Nguyen, N. H., Sinthong, P., \& Kalagnanam, J. (2023). A time series is worth 64 words: Long-term forecasting with Transformers. \textit{International Conference on Learning Representations}. arXiv:2211.14730.'),
    'Ore': (AX + '1905.10437', 'Oreshkin et al.\\ (2020)', 'Oreshkin et al.\\ (2020)',
            r'Oreshkin, B. N., Carpov, D., Chapados, N., \& Bengio, Y. (2020). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. \textit{International Conference on Learning Representations}. arXiv:1905.10437.'),
    'PMB': ('https://proceedings.mlr.press/v28/pascanu13.html', 'Pascanu, Mikolov and Bengio (2013)', 'Pascanu, Mikolov și Bengio (2013)',
            r'Pascanu, R., Mikolov, T., \& Bengio, Y. (2013). On the difficulty of training recurrent neural networks. \textit{Proceedings of the 30th International Conference on Machine Learning}, PMLR 28(3), 1310--1318.'),
    'Pat': ('10.1016/j.jeconom.2010.03.034', 'Patton (2011)', 'Patton (2011)',
            r'Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. \textit{Journal of Econometrics}, 160(1), 246--256.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'Rac': ('10.1016/S0304-4076(00)00030-0', 'Racine (2000)', 'Racine (2000)',
            r'Racine, J. (2000). Consistent cross-validatory model-selection for dependent data: hv-block cross-validation. \textit{Journal of Econometrics}, 99(1), 39--61.'),
    'RHW': ('10.1038/323533a0', 'Rumelhart, Hinton and Williams (1986)', 'Rumelhart, Hinton și Williams (1986)',
            r'Rumelhart, D. E., Hinton, G. E., \& Williams, R. J. (1986). Learning representations by back-propagating errors. \textit{Nature}, 323(6088), 533--536.'),
    'DeepAR': ('10.1016/j.ijforecast.2019.07.001', 'Salinas et al.\\ (2020)', 'Salinas et al.\\ (2020)',
               r'Salinas, D., Flunkert, V., Gasthaus, J., \& Januschowski, T. (2020). DeepAR: Probabilistic forecasting with autoregressive recurrent networks. \textit{International Journal of Forecasting}, 36(3), 1181--1191.'),
    'SBV': ('10.1214/15-AOS1321', 'Scornet, Biau and Vert (2015)', 'Scornet, Biau și Vert (2015)',
            r'Scornet, E., Biau, G., \& Vert, J.-P. (2015). Consistency of random forests. \textit{The Annals of Statistics}, 43(4), 1716--1741.'),
    'Sha': ('10.1515/9781400881970-018', 'Shapley (1953)', 'Shapley (1953)',
            r'Shapley, L. S. (1953). A value for $n$-person games. In H. W. Kuhn \& A. W. Tucker (Eds.), \textit{Contributions to the Theory of Games II}, 307--318. Princeton University Press.'),
    'Smyl': ('10.1016/j.ijforecast.2019.03.017', 'Smyl (2020)', 'Smyl (2020)',
             r'Smyl, S. (2020). A hybrid method of exponential smoothing and recurrent neural networks for time series forecasting. \textit{International Journal of Forecasting}, 36(1), 75--85.'),
    'SVL': (AX + '1409.3215', 'Sutskever, Vinyals and Le (2014)', 'Sutskever, Vinyals și Le (2014)',
            r'Sutskever, I., Vinyals, O., \& Le, Q. V. (2014). Sequence to sequence learning with neural networks. \textit{Advances in Neural Information Processing Systems}, 27. arXiv:1409.3215.'),
    'Tib': ('10.1111/j.2517-6161.1996.tb02080.x', 'Tibshirani (1996)', 'Tibshirani (1996)',
            r'Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. \textit{Journal of the Royal Statistical Society: Series B}, 58(1), 267--288.'),
    'WaveNet': (AX + '1609.03499', 'van den Oord et al.\\ (2016)', 'van den Oord et al.\\ (2016)',
                r'van den Oord, A., Dieleman, S., Zen, H., Simonyan, K., Vinyals, O., Graves, A., Kalchbrenner, N., Senior, A., \& Kavukcuoglu, K. (2016). WaveNet: A generative model for raw audio. arXiv:1609.03499.'),
    'Vas': ('https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html', 'Vaswani et al.\\ (2017)', 'Vaswani et al.\\ (2017)',
            r'Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., \& Polosukhin, I. (2017). Attention is all you need. \textit{Advances in Neural Information Processing Systems}, 30.'),
    'WA': ('10.1080/01621459.2017.1319839', 'Wager and Athey (2018)', 'Wager și Athey (2018)',
           r'Wager, S., \& Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using random forests. \textit{Journal of the American Statistical Association}, 113(523), 1228--1242.'),
    'Whi': ('10.1111/1468-0262.00152', 'White (2000)', 'White (2000)',
            r'White, H. (2000). A reality check for data snooping. \textit{Econometrica}, 68(5), 1097--1126.'),
    'WP': ('10.18653/v1/D19-1002', 'Wiegreffe and Pinter (2019)', 'Wiegreffe și Pinter (2019)',
           r'Wiegreffe, S., \& Pinter, Y. (2019). Attention is not not explanation. \textit{Proceedings of EMNLP-IJCNLP 2019}, 11--20.'),
    'Auto': ('https://proceedings.neurips.cc/paper/2021/hash/bcc0d400288793e8bdcd7c19a8ac0c2b-Abstract.html', 'Wu et al.\\ (2021)', 'Wu et al.\\ (2021)',
             r'Wu, H., Xu, J., Wang, J., \& Long, M. (2021). Autoformer: Decomposition transformers with auto-correlation for long-term series forecasting. \textit{Advances in Neural Information Processing Systems}, 34.'),
    'Yu': ('10.1214/aop/1176988849', 'Yu (1994)', 'Yu (1994)',
           r'Yu, B. (1994). Rates of convergence for empirical processes of stationary mixing sequences. \textit{The Annals of Probability}, 22(1), 94--116.'),
    'Zeng': ('10.1609/aaai.v37i9.26317', 'Zeng et al.\\ (2023)', 'Zeng et al.\\ (2023)',
             r'Zeng, A., Chen, M., Zhang, L., \& Xu, Q. (2023). Are transformers effective for time series forecasting? \textit{Proceedings of the AAAI Conference on Artificial Intelligence}, 37(9), 11121--11128.'),
    'ZY': ('https://jmlr.org/papers/v7/zhao06a.html', 'Zhao and Yu (2006)', 'Zhao și Yu (2006)',
           r'Zhao, P., \& Yu, B. (2006). On model selection consistency of lasso. \textit{Journal of Machine Learning Research}, 7, 2541--2563.'),
    'Inf': ('10.1609/aaai.v35i12.17325', 'Zhou et al.\\ (2021)', 'Zhou et al.\\ (2021)',
            r'Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H., \& Zhang, W. (2021). Informer: Beyond efficient transformer for long sequence time-series forecasting. \textit{Proceedings of the AAAI Conference on Artificial Intelligence}, 35(12), 11106--11115.'),
    'ZW': ('10.1016/j.eneco.2017.12.016', 'Ziel and Weron (2018)', 'Ziel și Weron (2018)',
           r'Ziel, F., \& Weron, R. (2018). Day-ahead electricity price forecasting with high-dimensional structures: Univariate vs. multivariate modeling frameworks. \textit{Energy Economics}, 70, 396--420.'),
    'Zou': ('10.1198/016214506000000735', 'Zou (2006)', 'Zou (2006)',
            r'Zou, H. (2006). The adaptive lasso and its oracle properties. \textit{Journal of the American Statistical Association}, 101(476), 1418--1429.'),
    'ZH': ('10.1111/j.1467-9868.2005.00503.x', 'Zou and Hastie (2005)', 'Zou și Hastie (2005)',
           r'Zou, H., \& Hastie, T. (2005). Regularization and variable selection via the elastic net. \textit{Journal of the Royal Statistical Society: Series B}, 67(2), 301--320.'),
}


def _url(x):
    return x if x.startswith('http') else D_ + x


def _safe(u):
    return u.replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#')


REFS = ''.join(ref(k, _safe(_url(v[0])), v[1], v[2]) for k, v in R.items())


def bib(keys=None):
    """Bibliography entries (alphabetical) with a clickable DOI or URL."""
    out = []
    for k, v in sorted(R.items(), key=lambda kv: re.sub(r'[^a-z]', '', kv[1][3].lower())):
        if keys is not None and k not in keys:
            continue
        u = _safe(_url(v[0]))
        shown = ('doi:' + v[0]) if not v[0].startswith('http') else v[0].split('/')[2].replace('www.', '')
        shown = shown.replace('_', '\\_').replace('<', '\\textless{}').replace('>', '\\textgreater{}').replace('#', '\\#')
        out.append(v[3] + f' \\href{{{u}}}{{{shown}}}')
    return out
