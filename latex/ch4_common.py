r"""
ch4_common.py -- shared helpers of the Chapter 4 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_04/ch4_numbers.json (generate_all_charts.py) and
sem4_results.json (seminar4.py); the clickable citations of Chapter 4 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401
from ch3_common import T, V2, finalize, month, pv, minus_fix   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_04')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_04'


def load():
    with open(os.path.join(QL, 'ch4_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem4_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'AL': ('10.1177/1536867X1601600314', 'Abrigo and Love (2016)', 'Abrigo și Love (2016)',
           r'Abrigo, M. R. M., \& Love, I. (2016). Estimation of panel vector autoregression in Stata. \textit{The Stata Journal}, 16(3), 778--804.'),
    'Bac': ('10.1016/0140-9883(91)90022-R', 'Bacon (1991)', 'Bacon (1991)',
            r'Bacon, R. W. (1991). Rockets and feathers: The asymmetric speed of adjustment of UK retail gasoline prices to cost changes. \textit{Energy Economics}, 13(3), 211--218.'),
    'BrP': ('10.1007/978-3-540-75892-1_9', 'Breitung and Pesaran (2008)', 'Breitung și Pesaran (2008)',
            r'Breitung, J., \& Pesaran, M. H. (2008). Unit roots and cointegration in panels. In L. Mátyás \& P. Sevestre (Eds.), \textit{The Econometrics of Panel Data} (pp.\ 279--322). Springer.'),
    'CRTa': ('10.1017/S0266466609990776', 'Cavaliere, Rahbek and Taylor (2010)', 'Cavaliere, Rahbek și Taylor (2010)',
             r'Cavaliere, G., Rahbek, A., \& Taylor, A. M. R. (2010). Cointegration rank testing under conditional heteroskedasticity. \textit{Econometric Theory}, 26(6), 1719--1760.'),
    'CRT': ('10.3982/ECTA9099', 'Cavaliere, Rahbek and Taylor (2012)', 'Cavaliere, Rahbek și Taylor (2012)',
            r'Cavaliere, G., Rahbek, A., \& Taylor, A. M. R. (2012). Bootstrap determination of the co-integration rank in vector autoregressive models. \textit{Econometrica}, 80(4), 1721--1740.'),
    'CP': ('10.1016/j.jeconom.2015.03.007', 'Chudik and Pesaran (2015)', 'Chudik și Pesaran (2015)',
           r'Chudik, A., \& Pesaran, M. H. (2015). Common correlated effects estimation of heterogeneous dynamic panel data models with weakly exogenous regressors. \textit{Journal of Econometrics}, 188(2), 393--420.'),
    'dB': ('10.1111/j.1465-6485.2005.00121.x', 'de Bondt (2005)', 'de Bondt (2005)',
           r'de Bondt, G. J. (2005). Interest rate pass-through: Empirical results for the euro area. \textit{German Economic Review}, 6(1), 37--78.'),
    'ECR': ('10.1016/j.jpolmod.2007.01.005', 'Égert, Crespo-Cuaresma and Reininger (2007)', 'Égert, Crespo-Cuaresma și Reininger (2007)',
            r'Égert, B., Crespo-Cuaresma, J., \& Reininger, T. (2007). Interest rate pass-through in Central and Eastern Europe: Reborn from ashes merely to pass away? \textit{Journal of Policy Modeling}, 29(2), 209--225.'),
    'EG': ('10.2307/1913236', 'Engle and Granger (1987)', 'Engle și Granger (1987)',
           r'Engle, R. F., \& Granger, C. W. J. (1987). Co-integration and error correction: Representation, estimation, and testing. \textit{Econometrica}, 55(2), 251--276.'),
    'GN': ('10.1016/S0165-1889(99)00062-7', 'Gonzalo and Ng (2001)', 'Gonzalo și Ng (2001)',
           r'Gonzalo, J., \& Ng, S. (2001). A systematic framework for analyzing the dynamic effects of permanent and transitory shocks. \textit{Journal of Economic Dynamics and Control}, 25(10), 1527--1546.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'HNR': ('10.2307/1913103', 'Holtz-Eakin, Newey and Rosen (1988)', 'Holtz-Eakin, Newey și Rosen (1988)',
            r'Holtz-Eakin, D., Newey, W., \& Rosen, H. S. (1988). Estimating vector autoregressions with panel data. \textit{Econometrica}, 56(6), 1371--1395.'),
    'IPS': ('10.1016/S0304-4076(03)00092-7', 'Im, Pesaran and Shin (2003)', 'Im, Pesaran și Shin (2003)',
            r'Im, K. S., Pesaran, M. H., \& Shin, Y. (2003). Testing for unit roots in heterogeneous panels. \textit{Journal of Econometrics}, 115(1), 53--74.'),
    'JohA': ('10.1016/0165-1889(88)90041-3', 'Johansen (1988)', 'Johansen (1988)',
              r'Johansen, S. (1988). Statistical analysis of cointegration vectors. \textit{Journal of Economic Dynamics and Control}, 12(2--3), 231--254.'),
    'JohB': ('10.2307/2938278', 'Johansen (1991)', 'Johansen (1991)',
              r'Johansen, S. (1991). Estimation and hypothesis testing of cointegration vectors in Gaussian vector autoregressive models. \textit{Econometrica}, 59(6), 1551--1580.'),
    'JohC': ('10.1111/j.1468-0084.1992.tb00008.x', 'Johansen (1992)', 'Johansen (1992)',
              r'Johansen, S. (1992). Determination of cointegration rank in the presence of a linear trend. \textit{Oxford Bulletin of Economics and Statistics}, 54(3), 383--397.'),
    'JohD': ('10.1093/0198774508.001.0001', 'Johansen (1995a)', 'Johansen (1995a)',
              r'Johansen, S. (1995a). \textit{Likelihood-Based Inference in Cointegrated Vector Autoregressive Models}. Oxford University Press.'),
    'JohE': ('10.1016/0304-4076(94)01664-L', 'Johansen (1995b)', 'Johansen (1995b)',
               r'Johansen, S. (1995b). Identifying restrictions of linear equations with applications to simultaneous equations and cointegration. \textit{Journal of Econometrics}, 69(1), 111--132.'),
    'JohF': ('10.1017/S0266466600009026', 'Johansen (1995c)', 'Johansen (1995c)',
               r'Johansen, S. (1995c). A statistical analysis of cointegration for I(2) variables. \textit{Econometric Theory}, 11(1), 25--59.'),
    'JohG': ('10.1111/1468-0262.00358', 'Johansen (2002)', 'Johansen (2002)',
              r'Johansen, S. (2002). A small sample correction for the test of cointegrating rank in the vector autoregressive model. \textit{Econometrica}, 70(5), 1929--1961.'),
    'JJ': ('10.1111/j.1468-0084.1990.mp52002003.x', 'Johansen and Juselius (1990)', 'Johansen și Juselius (1990)',
           r'Johansen, S., \& Juselius, K. (1990). Maximum likelihood estimation and inference on cointegration, with applications to the demand for money. \textit{Oxford Bulletin of Economics and Statistics}, 52(2), 169--210.'),
    'JMN': ('10.1111/1368-423X.00047', 'Johansen, Mosconi and Nielsen (2000)', 'Johansen, Mosconi și Nielsen (2000)',
            r'Johansen, S., Mosconi, R., \& Nielsen, B. (2000). Cointegration analysis in the presence of structural breaks in the deterministic trend. \textit{The Econometrics Journal}, 3(2), 216--249.'),
    'Jus': ('10.1093/oso/9780199285662.001.0001', 'Juselius (2006)', 'Juselius (2006)',
            r'Juselius, K. (2006). \textit{The Cointegrated VAR Model: Methodology and Applications}. Oxford University Press.'),
    'Kao': ('10.1016/S0304-4076(98)00023-2', 'Kao (1999)', 'Kao (1999)',
            r'Kao, C. (1999). Spurious regression and residual-based tests for cointegration in panel data. \textit{Journal of Econometrics}, 90(1), 1--44.'),
    'KPY': ('10.1016/j.jeconom.2010.10.001', 'Kapetanios, Pesaran and Yamagata (2011)', 'Kapetanios, Pesaran și Yamagata (2011)',
            r'Kapetanios, G., Pesaran, M. H., \& Yamagata, T. (2011). Panels with non-stationary multifactor error structures. \textit{Journal of Econometrics}, 160(2), 326--348.'),
    'KL': ('10.1017/9781108164818', 'Kilian and Lütkepohl (2017)', 'Kilian și Lütkepohl (2017)',
           r'Kilian, L., \& Lütkepohl, H. (2017). \textit{Structural Vector Autoregressive Analysis}. Cambridge University Press.'),
    'KPSW': ('https://www.jstor.org/stable/2006644', 'King, Plosser, Stock and Watson (1991)', 'King, Plosser, Stock și Watson (1991)',
             r'King, R. G., Plosser, C. I., Stock, J. H., \& Watson, M. W. (1991). Stochastic trends and economic fluctuations. \textit{American Economic Review}, 81(4), 819--840.'),
    'KS': ('10.1111/obes.12377', 'Kripfganz and Schneider (2020)', 'Kripfganz și Schneider (2020)',
           r'Kripfganz, S., \& Schneider, D. C. (2020). Response surface regressions for critical value bounds and approximate p-values in equilibrium correction models. \textit{Oxford Bulletin of Economics and Statistics}, 82(6), 1456--1481.'),
    'LLC': ('10.1016/S0304-4076(01)00098-7', 'Levin, Lin and Chu (2002)', 'Levin, Lin și Chu (2002)',
            r'Levin, A., Lin, C.-F., \& Chu, C.-S. J. (2002). Unit root tests in panel data: Asymptotic and finite-sample properties. \textit{Journal of Econometrics}, 108(1), 1--24.'),
    'Lut': ('10.1007/978-3-540-27752-1', 'Lütkepohl (2005)', 'Lütkepohl (2005)',
            r'Lütkepohl, H. (2005). \textit{New Introduction to Multiple Time Series Analysis}. Springer.'),
    'MHM': ('10.1002/(SICI)1099-1255(199909/10)14:5<563::AID-JAE530>3.0.CO;2-R', 'MacKinnon, Haug and Michelis (1999)', 'MacKinnon, Haug și Michelis (1999)',
            r'MacKinnon, J. G., Haug, A. A., \& Michelis, L. (1999). Numerical distribution functions of likelihood ratio tests for cointegration. \textit{Journal of Applied Econometrics}, 14(5), 563--577.'),
    'Nar': ('10.1080/00036840500278103', 'Narayan (2005)', 'Narayan (2005)',
            r'Narayan, P. K. (2005). The saving and investment nexus for China: Evidence from cointegration tests. \textit{Applied Economics}, 37(17), 1979--1990.'),
    'Nic': ('10.2307/1911408', 'Nickell (1981)', 'Nickell (1981)',
            r'Nickell, S. (1981). Biases in dynamic models with fixed effects. \textit{Econometrica}, 49(6), 1417--1426.'),
    'OL': ('10.1111/j.1468-0084.1992.tb00013.x', 'Osterwald-Lenum (1992)', 'Osterwald-Lenum (1992)',
           r'Osterwald-Lenum, M. (1992). A note with quantiles of the asymptotic distribution of the maximum likelihood cointegration rank test statistics. \textit{Oxford Bulletin of Economics and Statistics}, 54(3), 461--472.'),
    'Pan': ('10.1017/S0266466600012421', 'Pantula (1989)', 'Pantula (1989)',
            r'Pantula, S. G. (1989). Testing for unit roots in time series data. \textit{Econometric Theory}, 5(2), 256--271.'),
    'PedA': ('10.1111/1468-0084.0610s1653', 'Pedroni (1999)', 'Pedroni (1999)',
              r'Pedroni, P. (1999). Critical values for cointegration tests in heterogeneous panels with multiple regressors. \textit{Oxford Bulletin of Economics and Statistics}, 61(S1), 653--670.'),
    'PedB': ('10.1162/003465301753237803', 'Pedroni (2001)', 'Pedroni (2001)',
              r'Pedroni, P. (2001). Purchasing power parity tests in cointegrated panels. \textit{The Review of Economics and Statistics}, 83(4), 727--731.'),
    'PedC': ('10.1017/S0266466604203073', 'Pedroni (2004)', 'Pedroni (2004)',
              r'Pedroni, P. (2004). Panel cointegration: Asymptotic and finite sample properties of pooled time series tests with an application to the PPP hypothesis. \textit{Econometric Theory}, 20(3), 597--625.'),
    'PesA': ('10.1111/j.1468-0262.2006.00692.x', 'Pesaran (2006)', 'Pesaran (2006)',
              r'Pesaran, M. H. (2006). Estimation and inference in large heterogeneous panels with a multifactor error structure. \textit{Econometrica}, 74(4), 967--1012.'),
    'PesB': ('10.1002/jae.951', 'Pesaran (2007)', 'Pesaran (2007)',
              r'Pesaran, M. H. (2007). A simple panel unit root test in the presence of cross-section dependence. \textit{Journal of Applied Econometrics}, 22(2), 265--312.'),
    'PesC': ('10.1080/07474938.2014.956623', 'Pesaran (2015a)', 'Pesaran (2015a)',
               r'Pesaran, M. H. (2015a). Testing weak cross-sectional dependence in large panels. \textit{Econometric Reviews}, 34(6--10), 1089--1117.'),
    'PesD': ('10.1093/acprof:oso/9780198736912.001.0001', 'Pesaran (2015b)', 'Pesaran (2015b)',
              r'Pesaran, M. H. (2015b). \textit{Time Series and Panel Data Econometrics}. Oxford University Press.'),
    'PesE': ('10.1007/s00181-020-01875-7', 'Pesaran (2021)', 'Pesaran (2021)',
              r'Pesaran, M. H. (2021). General diagnostic tests for cross-sectional dependence in panels. \textit{Empirical Economics}, 60(1), 13--50.'),
    'PSa': ('10.1017/CCOL0521633230.011', 'Pesaran and Shin (1998)', 'Pesaran și Shin (1998)',
             r'Pesaran, M. H., \& Shin, Y. (1998). An autoregressive distributed-lag modelling approach to cointegration analysis. In S. Strøm (Ed.), \textit{Econometrics and Economic Theory in the 20th Century: The Ragnar Frisch Centennial Symposium} (pp.\ 371--413). Cambridge University Press.'),
    'PSSa': ('10.1080/01621459.1999.10474156', 'Pesaran, Shin and Smith (1999)', 'Pesaran, Shin și Smith (1999)',
              r'Pesaran, M. H., Shin, Y., \& Smith, R. P. (1999). Pooled mean group estimation of dynamic heterogeneous panels. \textit{Journal of the American Statistical Association}, 94(446), 621--634.'),
    'PSSb': ('10.1002/jae.616', 'Pesaran, Shin and Smith (2001)', 'Pesaran, Shin și Smith (2001)',
              r'Pesaran, M. H., Shin, Y., \& Smith, R. J. (2001). Bounds testing approaches to the analysis of level relationships. \textit{Journal of Applied Econometrics}, 16(3), 289--326.'),
    'PSm': ('10.1016/0304-4076(94)01644-F', 'Pesaran and Smith (1995)', 'Pesaran și Smith (1995)',
            r'Pesaran, M. H., \& Smith, R. (1995). Estimating long-run relationships from dynamic heterogeneous panels. \textit{Journal of Econometrics}, 68(1), 79--113.'),
    'PH': ('10.2307/2297545', 'Phillips and Hansen (1990)', 'Phillips și Hansen (1990)',
           r'Phillips, P. C. B., \& Hansen, B. E. (1990). Statistical inference in instrumental variables regression with I(1) processes. \textit{The Review of Economic Studies}, 57(1), 99--125.'),
    'PM': ('10.1111/1468-0262.00070', 'Phillips and Moon (1999)', 'Phillips și Moon (1999)',
           r'Phillips, P. C. B., \& Moon, H. R. (1999). Linear regression limit theory for nonstationary panel data. \textit{Econometrica}, 67(5), 1057--1111.'),
    'RA': ('10.1111/j.1467-9892.1992.tb00113.x', 'Reinsel and Ahn (1992)', 'Reinsel și Ahn (1992)',
           r'Reinsel, G. C., \& Ahn, S. K. (1992). Vector autoregressive models with unit roots and reduced rank structure: Estimation, likelihood ratio test, and forecasting. \textit{Journal of Time Series Analysis}, 13(4), 353--375.'),
    'Sai': ('10.1017/S0266466600004217', 'Saikkonen (1991)', 'Saikkonen (1991)',
            r'Saikkonen, P. (1991). Asymptotically efficient estimation of cointegration regressions. \textit{Econometric Theory}, 7(1), 1--21.'),
    'SYG': ('10.1007/978-1-4899-8008-3_9', 'Shin, Yu and Greenwood-Nimmo (2014)', 'Shin, Yu și Greenwood-Nimmo (2014)',
            r'Shin, Y., Yu, B., \& Greenwood-Nimmo, M. (2014). Modelling asymmetric cointegration and dynamic multipliers in a nonlinear ARDL framework. In R. C. Sickles \& W. C. Horrace (Eds.), \textit{Festschrift in Honor of Peter Schmidt} (pp.\ 281--314). Springer.'),
    'SWa': ('10.2307/2951763', 'Stock and Watson (1993)', 'Stock și Watson (1993)',
             r'Stock, J. H., \& Watson, M. W. (1993). A simple estimator of cointegrating vectors in higher order integrated systems. \textit{Econometrica}, 61(4), 783--820.'),
    'Swe': ('10.1111/j.1468-0262.2006.00723.x', 'Swensen (2006)', 'Swensen (2006)',
            r'Swensen, A. R. (2006). Bootstrap algorithms for testing and determining the cointegration rank in VAR models. \textit{Econometrica}, 74(6), 1699--1714.'),
    'TY': ('10.1016/0304-4076(94)01616-8', 'Toda and Yamamoto (1995)', 'Toda și Yamamoto (1995)',
           r'Toda, H. Y., \& Yamamoto, T. (1995). Statistical inference in vector autoregressions with possibly integrated processes. \textit{Journal of Econometrics}, 66(1--2), 225--250.'),
    'Wes': ('10.1111/j.1468-0084.2007.00477.x', 'Westerlund (2007)', 'Westerlund (2007)',
            r'Westerlund, J. (2007). Testing for error correction in panel data. \textit{Oxford Bulletin of Economics and Statistics}, 69(6), 709--748.'),
}


def _url(x):
    return x if x.startswith('http') else D_ + x


def _safe(u):
    return u.replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#').replace(';', '\\%3B')


REFS = ''.join(ref(k, _safe(_url(v[0])), v[1], v[2]) for k, v in R.items())


def bib(keys=None):
    """Bibliography entries (alphabetical) with a clickable DOI or URL."""
    out = []
    for k, v in sorted(R.items(), key=lambda kv: re.sub(r'[^a-z0-9]', '', kv[1][3].lower().replace('é', 'e'))):
        if keys is not None and k not in keys:
            continue
        u = _safe(_url(v[0]))
        shown = ('doi:' + v[0]) if not v[0].startswith('http') else v[0].split('/')[2].replace('www.', '')
        shown = shown.replace('_', '\\_').replace('<', '\\textless{}').replace('>', '\\textgreater{}').replace('#', '\\#')
        out.append(v[3] + f' \\href{{{u}}}{{{shown}}}')
    return out
