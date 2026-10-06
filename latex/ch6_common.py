r"""
ch6_common.py -- shared helpers of the Chapter 6 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_06/ch6_numbers.json (generate_all_charts.py) and
sem6_results.json (seminar6.py); the clickable citations of Chapter 6 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401
from ch3_common import T, V2, finalize, month, quarter, pv, minus_fix   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_06')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_06'


def load():
    with open(os.path.join(QL, 'ch6_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem6_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'AG': ('10.1086/511283', 'Aguiar and Gopinath (2007)', 'Aguiar și Gopinath (2007)',
           r'Aguiar, M., \& Gopinath, G. (2007). Emerging market business cycles: The cycle is the trend. \textit{Journal of Political Economy}, 115(1), 69--102.'),
    'ADH': ('10.1111/j.1467-9868.2009.00736.x', 'Andrieu, Doucet and Holenstein (2010)', 'Andrieu, Doucet și Holenstein (2010)',
            r'Andrieu, C., Doucet, A., \& Holenstein, R. (2010). Particle Markov chain Monte Carlo methods. \textit{Journal of the Royal Statistical Society: Series B}, 72(3), 269--342.'),
    'AR': ('10.1214/07-AOS574', 'Andrieu and Roberts (2009)', 'Andrieu și Roberts (2009)',
           r'Andrieu, C., \& Roberts, G. O. (2009). The pseudo-marginal approach for efficient Monte Carlo computations. \textit{The Annals of Statistics}, 37(2), 697--725.'),
    'AK': ('10.1214/aos/1176349739', 'Ansley and Kohn (1985)', 'Ansley și Kohn (1985)',
           r'Ansley, C. F., \& Kohn, R. (1985). Estimation, filtering, and smoothing in state space models with incompletely specified initial conditions. \textit{The Annals of Statistics}, 13(4), 1286--1316.'),
    'BM': ('10.1002/jae.2306', 'Bańbura and Modugno (2014)', 'Bańbura și Modugno (2014)',
           r'Bańbura, M., \& Modugno, M. (2014). Maximum likelihood estimation of factor models on datasets with arbitrary pattern of missing data. \textit{Journal of Applied Econometrics}, 29(1), 133--160.'),
    'BN': ('10.1016/0304-3932(81)90040-4', 'Beveridge and Nelson (1981)', 'Beveridge și Nelson (1981)',
           r"Beveridge, S., \& Nelson, C. R. (1981). A new approach to decomposition of economic time series into permanent and transitory components with particular attention to measurement of the `business cycle'. \textit{Journal of Monetary Economics}, 7(2), 151--174."),
    'Bol': ('10.1016/0304-4076(86)90063-1', 'Bollerslev (1986)', 'Bollerslev (1986)',
            r'Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. \textit{Journal of Econometrics}, 31(3), 307--327.'),
    'Bro': ('10.1214/14-AOAS788', 'Brodersen et al.\\ (2015)', 'Brodersen et al.\\ (2015)',
            r'Brodersen, K. H., Gallusser, F., Koehler, J., Remy, N., \& Scott, S. L. (2015). Inferring causal impact using Bayesian structural time-series models. \textit{The Annals of Applied Statistics}, 9(1), 247--274.'),
    'CK': ('10.1093/biomet/81.3.541', 'Carter and Kohn (1994)', 'Carter și Kohn (1994)',
           r'Carter, C. K., \& Kohn, R. (1994). On Gibbs sampling for state space models. \textit{Biometrika}, 81(3), 541--553.'),
    'CJ': ('10.1504/IJMMNO.2009.030090', 'Chan and Jeliazkov (2009)', 'Chan și Jeliazkov (2009)',
           r'Chan, J. C. C., \& Jeliazkov, I. (2009). Efficient simulation and integrated likelihood estimation in state space models. \textit{International Journal of Mathematical Modelling and Numerical Optimisation}, 1(1/2), 101--120.'),
    'CP': ('10.1007/978-3-030-47845-2', 'Chopin and Papaspiliopoulos (2020)', 'Chopin și Papaspiliopoulos (2020)',
           r'Chopin, N., \& Papaspiliopoulos, O. (2020). \textit{An Introduction to Sequential Monte Carlo}. Springer.'),
    'Cla': ('10.2307/1884282', 'Clark (1987)', 'Clark (1987)',
            r'Clark, P. K. (1987). The cyclical component of U.S. economic activity. \textit{The Quarterly Journal of Economics}, 102(4), 797--814.'),
    'CSa': ('10.1086/654451', 'Cogley and Sargent (2001)', 'Cogley și Sargent (2001)',
            r'Cogley, T., \& Sargent, T. J. (2001). Evolving post-World War II U.S. inflation dynamics. \textit{NBER Macroeconomics Annual}, 16, 331--373.'),
    'CSb': ('10.1016/j.red.2004.10.009', 'Cogley and Sargent (2005)', 'Cogley și Sargent (2005)',
            r'Cogley, T., \& Sargent, T. J. (2005). Drifts and volatilities: Monetary policies and outcomes in the post WWII US. \textit{Review of Economic Dynamics}, 8(2), 262--302.'),
    'dJa': ('10.1214/aos/1176348139', 'de Jong (1991)', 'de Jong (1991)',
            r'de Jong, P. (1991). The diffuse Kalman filter. \textit{The Annals of Statistics}, 19(2), 1073--1083.'),
    'dJS': ('10.1093/biomet/82.2.339', 'de Jong and Shephard (1995)', 'de Jong și Shephard (1995)',
            r'de Jong, P., \& Shephard, N. (1995). The simulation smoother for time series models. \textit{Biometrika}, 82(2), 339--350.'),
    'DM': ('10.1007/978-1-4684-9393-1', 'Del Moral (2004)', 'Del Moral (2004)',
           r'Del Moral, P. (2004). \textit{Feynman--Kac Formulae: Genealogical and Interacting Particle Systems with Applications}. Springer.'),
    'DNP': ('10.1093/restud/rdv024', 'Del Negro and Primiceri (2015)', 'Del Negro și Primiceri (2015)',
            r'Del Negro, M., \& Primiceri, G. E. (2015). Time varying structural vector autoregressions and monetary policy: A corrigendum. \textit{The Review of Economic Studies}, 82(4), 1342--1345.'),
    'DPDK': ('10.1093/biomet/asu075', 'Doucet, Pitt, Deligiannidis and Kohn (2015)', 'Doucet, Pitt, Deligiannidis și Kohn (2015)',
             r'Doucet, A., Pitt, M. K., Deligiannidis, G., \& Kohn, R. (2015). Efficient implementation of Markov chain Monte Carlo when using an unbiased likelihood estimator. \textit{Biometrika}, 102(2), 295--313.'),
    'DGR': ('10.1016/j.jeconom.2011.02.012', 'Doz, Giannone and Reichlin (2011)', 'Doz, Giannone și Reichlin (2011)',
            r'Doz, C., Giannone, D., \& Reichlin, L. (2011). A two-step estimator for large approximate dynamic factor models based on Kalman filtering. \textit{Journal of Econometrics}, 164(1), 188--205.'),
    'DKa': ('10.1093/biomet/89.3.603', 'Durbin and Koopman (2002)', 'Durbin și Koopman (2002)',
            r'Durbin, J., \& Koopman, S. J. (2002). A simple and efficient simulation smoother for state space time series analysis. \textit{Biometrika}, 89(3), 603--616.'),
    'DK': ('10.1093/acprof:oso/9780199641178.001.0001', 'Durbin and Koopman (2012)', 'Durbin și Koopman (2012)',
           r'Durbin, J., \& Koopman, S. J. (2012). \textit{Time Series Analysis by State Space Methods} (2nd ed.). Oxford University Press.'),
    'FS': ('10.1111/j.1467-9892.1994.tb00184.x', 'Frühwirth-Schnatter (1994)', 'Frühwirth-Schnatter (1994)',
           r'Frühwirth-Schnatter, S. (1994). Data augmentation and dynamic linear models. \textit{Journal of Time Series Analysis}, 15(2), 183--202.'),
    'FSW': ('10.1016/j.jeconom.2009.07.003', 'Frühwirth-Schnatter and Wagner (2010)', 'Frühwirth-Schnatter și Wagner (2010)',
            r'Frühwirth-Schnatter, S., \& Wagner, H. (2010). Stochastic model specification search for Gaussian and partial non-Gaussian state space models. \textit{Journal of Econometrics}, 154(1), 85--100.'),
    'GRS': ('10.1016/j.jmoneco.2008.05.010', 'Giannone, Reichlin and Small (2008)', 'Giannone, Reichlin și Small (2008)',
            r'Giannone, D., Reichlin, L., \& Small, D. (2008). Nowcasting: The real-time informational content of macroeconomic data. \textit{Journal of Monetary Economics}, 55(4), 665--676.'),
    'GSS': ('10.1049/ip-f-2.1993.0015', 'Gordon, Salmond and Smith (1993)', 'Gordon, Salmond și Smith (1993)',
            r'Gordon, N. J., Salmond, D. J., \& Smith, A. F. M. (1993). Novel approach to nonlinear/non-Gaussian Bayesian state estimation. \textit{IEE Proceedings F (Radar and Signal Processing)}, 140(2), 107--113.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'HamB': ('10.1162/rest_a_00706', 'Hamilton (2018)', 'Hamilton (2018)',
             r'Hamilton, J. D. (2018). Why you should never use the Hodrick--Prescott filter. \textit{The Review of Economics and Statistics}, 100(5), 831--843.'),
    'Har': ('10.1017/CBO9781107049994', 'Harvey (1990)', 'Harvey (1990)',
            r'Harvey, A. C. (1990). \textit{Forecasting, Structural Time Series Models and the Kalman Filter}. Cambridge University Press.'),
    'HJ': ('10.1002/jae.3950080302', 'Harvey and Jaeger (1993)', 'Harvey și Jaeger (1993)',
           r'Harvey, A. C., \& Jaeger, A. (1993). Detrending, stylized facts and the business cycle. \textit{Journal of Applied Econometrics}, 8(3), 231--247.'),
    'HRS': ('10.2307/2297980', 'Harvey, Ruiz and Shephard (1994)', 'Harvey, Ruiz și Shephard (1994)',
            r'Harvey, A., Ruiz, E., \& Shephard, N. (1994). Multivariate stochastic variance models. \textit{The Review of Economic Studies}, 61(2), 247--264.'),
    'JPR': ('10.1080/07350015.1994.10524553', 'Jacquier, Polson and Rossi (1994)', 'Jacquier, Polson și Rossi (1994)',
            r'Jacquier, E., Polson, N. G., \& Rossi, P. E. (1994). Bayesian analysis of stochastic volatility models. \textit{Journal of Business \& Economic Statistics}, 12(4), 371--389.'),
    'JU': ('10.1109/JPROC.2003.823141', 'Julier and Uhlmann (2004)', 'Julier și Uhlmann (2004)',
           r'Julier, S. J., \& Uhlmann, J. K. (2004). Unscented filtering and nonlinear estimation. \textit{Proceedings of the IEEE}, 92(3), 401--422.'),
    'JK': ('10.1111/ectj.12029', 'Jungbacker and Koopman (2015)', 'Jungbacker și Koopman (2015)',
           r'Jungbacker, B., \& Koopman, S. J. (2015). Likelihood-based dynamic factor analysis for measurement and forecasting. \textit{The Econometrics Journal}, 18(2), C1--C21.'),
    'Kal': ('10.1115/1.3662552', 'Kalman (1960)', 'Kalman (1960)',
            r'Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. \textit{Journal of Basic Engineering}, 82(1), 35--45.'),
    'KMW': ('10.1162/REST_a_00691', 'Kamber, Morley and Wong (2018)', 'Kamber, Morley și Wong (2018)',
            r'Kamber, G., Morley, J., \& Wong, B. (2018). Intuitive and reliable estimates of the output gap from a Beveridge--Nelson filter. \textit{The Review of Economics and Statistics}, 100(3), 550--566.'),
    'KN': ('10.7551/mitpress/6444.001.0001', 'Kim and Nelson (1999)', 'Kim și Nelson (1999)',
           r'Kim, C.-J., \& Nelson, C. R. (1999). \textit{State-Space Models with Regime Switching: Classical and Gibbs-Sampling Approaches with Applications}. MIT Press.'),
    'KSC': ('10.1111/1467-937X.00050', 'Kim, Shephard and Chib (1998)', 'Kim, Shephard și Chib (1998)',
            r'Kim, S., Shephard, N., \& Chib, S. (1998). Stochastic volatility: Likelihood inference and comparison with ARCH models. \textit{The Review of Economic Studies}, 65(3), 361--393.'),
    'Kit': ('10.1080/10618600.1996.10474692', 'Kitagawa (1996)', 'Kitagawa (1996)',
            r'Kitagawa, G. (1996). Monte Carlo filter and smoother for non-Gaussian nonlinear state space models. \textit{Journal of Computational and Graphical Statistics}, 5(1), 1--25.'),
    'Koo': ('10.1080/01621459.1997.10473685', 'Koopman (1997)', 'Koopman (1997)',
            r'Koopman, S. J. (1997). Exact initial Kalman filtering and smoothing for nonstationary time series models. \textit{Journal of the American Statistical Association}, 92(440), 1630--1638.'),
    'KD': ('10.1111/1467-9892.00186', 'Koopman and Durbin (2000)', 'Koopman și Durbin (2000)',
           r'Koopman, S. J., \& Durbin, J. (2000). Fast filtering and smoothing for multivariate state space models. \textit{Journal of Time Series Analysis}, 21(3), 281--296.'),
    'MM': ('10.1002/jae.695', 'Mariano and Murasawa (2003)', 'Mariano și Murasawa (2003)',
           r'Mariano, R. S., \& Murasawa, Y. (2003). A new coincident index of business cycles based on monthly and quarterly series. \textit{Journal of Applied Econometrics}, 18(4), 427--443.'),
    'MNZ': ('10.1162/003465303765299765', 'Morley, Nelson and Zivot (2003)', 'Morley, Nelson și Zivot (2003)',
            r'Morley, J. C., Nelson, C. R., \& Zivot, E. (2003). Why are the Beveridge--Nelson and unobserved-components decompositions of GDP so different? \textit{The Review of Economics and Statistics}, 85(2), 235--243.'),
    'OCSN': ('10.1016/j.jeconom.2006.07.008', 'Omori, Chib, Shephard and Nakajima (2007)', 'Omori, Chib, Shephard și Nakajima (2007)',
             r'Omori, Y., Chib, S., Shephard, N., \& Nakajima, J. (2007). Stochastic volatility with leverage: Fast and efficient likelihood inference. \textit{Journal of Econometrics}, 140(2), 425--449.'),
    'OvN': ('10.1162/003465302760556422', 'Orphanides and van Norden (2002)', 'Orphanides și van Norden (2002)',
            r'Orphanides, A., \& van Norden, S. (2002). The unreliability of output-gap estimates in real time. \textit{The Review of Economics and Statistics}, 84(4), 569--583.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'PS': ('10.1080/01621459.1999.10474153', 'Pitt and Shephard (1999)', 'Pitt și Shephard (1999)',
           r'Pitt, M. K., \& Shephard, N. (1999). Filtering via simulation: Auxiliary particle filters. \textit{Journal of the American Statistical Association}, 94(446), 590--599.'),
    'PSGK': ('10.1016/j.jeconom.2012.06.004', 'Pitt, Silva, Giordani and Kohn (2012)', 'Pitt, Silva, Giordani și Kohn (2012)',
             r'Pitt, M. K., Silva, R. d. S., Giordani, P., \& Kohn, R. (2012). On some properties of Markov chain Monte Carlo simulation methods based on the particle filter. \textit{Journal of Econometrics}, 171(2), 134--151.'),
    'Pri': ('10.1111/j.1467-937X.2005.00353.x', 'Primiceri (2005)', 'Primiceri (2005)',
            r'Primiceri, G. E. (2005). Time varying structural vector autoregressions and monetary policy. \textit{The Review of Economic Studies}, 72(3), 821--852.'),
    'SV': ('10.1504/IJMMNO.2014.059942', 'Scott and Varian (2014)', 'Scott și Varian (2014)',
           r'Scott, S. L., \& Varian, H. R. (2014). Predicting the present with Bayesian structural time series. \textit{International Journal of Mathematical Modelling and Numerical Optimisation}, 5(1/2), 4--23.'),
    'SH': ('10.1111/j.1467-9892.1990.tb00062.x', 'Shephard and Harvey (1990)', 'Shephard și Harvey (1990)',
           r'Shephard, N., \& Harvey, A. C. (1990). On the probability of estimating a deterministic component in the local level model. \textit{Journal of Time Series Analysis}, 11(4), 339--347.'),
    'SS': ('10.1111/j.1467-9892.1982.tb00349.x', 'Shumway and Stoffer (1982)', 'Shumway și Stoffer (1982)',
           r'Shumway, R. H., \& Stoffer, D. S. (1982). An approach to time series smoothing and forecasting using the EM algorithm. \textit{Journal of Time Series Analysis}, 3(4), 253--264.'),
    'SWa': ('10.1080/01621459.1998.10474116', 'Stock and Watson (1998)', 'Stock și Watson (1998)',
            r'Stock, J. H., \& Watson, M. W. (1998). Median unbiased estimation of coefficient variance in a time-varying parameter model. \textit{Journal of the American Statistical Association}, 93(441), 349--358.'),
    'SWb': ('10.1111/j.1538-4616.2007.00014.x', 'Stock and Watson (2007)', 'Stock și Watson (2007)',
            r'Stock, J. H., \& Watson, M. W. (2007). Why has U.S. inflation become harder to forecast? \textit{Journal of Money, Credit and Banking}, 39(s1), 3--33.'),
    'Tay': ('10.1111/j.1467-9965.1994.tb00057.x', 'Taylor (1994)', 'Taylor (1994)',
            r'Taylor, S. J. (1994). Modeling stochastic volatility: A review and comparative study. \textit{Mathematical Finance}, 4(2), 183--204.'),
    'Wat': ('10.1016/0304-3932(86)90054-1', 'Watson (1986)', 'Watson (1986)',
            r'Watson, M. W. (1986). Univariate detrending methods with stochastic trends. \textit{Journal of Monetary Economics}, 18(1), 49--75.'),
}


def _url(x):
    return x if x.startswith('http') else D_ + x


def _safe(u):
    return u.replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#').replace(';', '\\%3B')


REFS = ''.join(ref(k, _safe(_url(v[0])), v[1], v[2]) for k, v in R.items())


def bib(keys=None):
    """Bibliography entries (alphabetical) with a clickable DOI or URL."""
    out = []
    key = lambda kv: re.sub(r'[^a-z0-9]', '', kv[1][3].lower().replace('ń', 'n').replace('ü', 'u'))   # noqa: E731
    for k, v in sorted(R.items(), key=key):
        if keys is not None and k not in keys:
            continue
        u = _safe(_url(v[0]))
        shown = ('doi:' + v[0]) if not v[0].startswith('http') else v[0].split('/')[2].replace('www.', '')
        shown = shown.replace('_', '\\_').replace('<', '\\textless{}').replace('>', '\\textgreater{}').replace('#', '\\#')
        out.append(v[3] + f' \\href{{{u}}}{{{shown}}}')
    return out
