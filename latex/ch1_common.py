r"""
ch1_common.py -- shared helpers of the Chapter 1 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_01/ch1_numbers.json (generate_all_charts.py) and
sem1_results.json (seminar1.py); the clickable citations of Chapter 1 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_01')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_01'
MONTHS_RO = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie',
             'octombrie', 'noiembrie', 'decembrie']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']


def T(en, ro):
    """Bilingual text."""
    return f'⟦{en}||{ro}⟧'


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


def date(s):
    y, m, d = s[:10].split('-')
    m = int(m) - 1
    return V2(f'{int(d)} {MONTHS_EN[m]} {y}', f'{int(d)} {MONTHS_RO[m]} {y}')


def quarter(s):
    """'2026-04-01' or '2026Q2' -> 2026Q2 / T2 2026."""
    if 'Q' in s:
        y, q = int(s[:4]), int(s[-1])
    else:
        y, q = int(s[:4]), (int(s[5:7]) - 1) // 3 + 1
    return V2(f'{y}Q{q}', f'T{q} {y}')


def pv(p, d=3):
    """A p-value in text mode: 3 decimals, or '< 0.001' (marked for the RO decimal comma)."""
    return '$<$\\,⁅0.001⁆' if p < 0.001 else '⁅' + f'{p:.{d}f}' + '⁆'


def minus_fix(V):
    """Negative numbers: a real minus sign in text and in math mode."""
    for k, v in list(V.items()):
        if isinstance(v, str) and v.startswith('⁅-'):
            V[k] = '⁅\\ensuremath{-}' + v[2:]


def load():
    with open(os.path.join(QL, 'ch1_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem1_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'AG': ('10.1198/073500106000000332', 'Amisano and Giacomini (2007)', 'Amisano și Giacomini (2007)',
           r'Amisano, G., \& Giacomini, R. (2007). Comparing density forecasts via weighted likelihood ratio tests. \textit{Journal of Business \& Economic Statistics}, 25(2), 177--190.'),
    'AO': ('10.21034/qr.2511', 'Atkeson and Ohanian (2001)', 'Atkeson și Ohanian (2001)',
           r'Atkeson, A., \& Ohanian, L. E. (2001). Are Phillips curves useful for forecasting inflation? \textit{Federal Reserve Bank of Minneapolis Quarterly Review}, 25(1), 2--11.'),
    'BGW': ('10.1109/TIT.2005.850145', 'Banerjee et al.\\ (2005)', 'Banerjee et al.\\ (2005)',
            r'Banerjee, A., Guo, X., \& Wang, H. (2005). On the optimality of conditional expectation as a Bregman predictor. \textit{IEEE Transactions on Information Theory}, 51(7), 2664--2669.'),
    'BG': ('10.1057/jors.1969.103', 'Bates and Granger (1969)', 'Bates și Granger (1969)',
           r'Bates, J. M., \& Granger, C. W. J. (1969). The combination of forecasts. \textit{Operational Research Quarterly}, 20(4), 451--468.'),
    'Berk': ('10.1198/07350010152596718', 'Berkowitz (2001)', 'Berkowitz (2001)',
             r'Berkowitz, J. (2001). Testing density forecasts, with applications to risk management. \textit{Journal of Business \& Economic Statistics}, 19(4), 465--474.'),
    'Boll': ('10.2307/1925546', 'Bollerslev (1987)', 'Bollerslev (1987)',
             r'Bollerslev, T. (1987). A conditionally heteroskedastic time series model for speculative prices and rates of return. \textit{The Review of Economics and Statistics}, 69(3), 542--547.'),
    'Brier': ('10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2', 'Brier (1950)', 'Brier (1950)',
              r'Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. \textit{Monthly Weather Review}, 78(1), 1--3.'),
    'CT': ('10.1198/jbes.2009.07211', 'Capistrán and Timmermann (2009)', 'Capistrán și Timmermann (2009)',
           r'Capistrán, C., \& Timmermann, A. (2009). Forecast combination with entry and exit of experts. \textit{Journal of Business \& Economic Statistics}, 27(4), 428--440.'),
    'ChH': ('10.2307/2297611', 'Chong and Hendry (1986)', 'Chong și Hendry (1986)',
            r'Chong, Y. Y., \& Hendry, D. F. (1986). Econometric evaluation of linear macro-economic models. \textit{The Review of Economic Studies}, 53(4), 671--690.'),
    'Chr': ('10.2307/2527341', 'Christoffersen (1998)', 'Christoffersen (1998)',
            r'Christoffersen, P. F. (1998). Evaluating interval forecasts. \textit{International Economic Review}, 39(4), 841--862.'),
    'CD': ('10.1017/S0266466600006277', 'Christoffersen and Diebold (1997)', 'Christoffersen și Diebold (1997)',
           r'Christoffersen, P. F., \& Diebold, F. X. (1997). Optimal prediction under asymmetric loss. \textit{Econometric Theory}, 13(6), 808--817.'),
    'CMVW': ('10.1016/j.ijforecast.2015.12.005', 'Claeskens et al.\\ (2016)', 'Claeskens et al.\\ (2016)',
             r'Claeskens, G., Magnus, J. R., Vasnev, A. L., \& Wang, W. (2016). The forecast combination puzzle: A simple theoretical explanation. \textit{International Journal of Forecasting}, 32(3), 754--762.'),
    'CM': ('10.1016/S0304-4076(01)00071-9', 'Clark and McCracken (2001)', 'Clark și McCracken (2001)',
           r'Clark, T. E., \& McCracken, M. W. (2001). Tests of equal forecast accuracy and encompassing for nested models. \textit{Journal of Econometrics}, 105(1), 85--110.'),
    'CW': ('10.1016/j.jeconom.2006.05.023', 'Clark and West (2007)', 'Clark și West (2007)',
           r'Clark, T. E., \& West, K. D. (2007). Approximately normal tests for equal predictive accuracy in nested models. \textit{Journal of Econometrics}, 138(1), 291--311.'),
    'Cr': ('10.1257/jel.49.1.72', 'Croushore (2011)', 'Croushore (2011)',
           r'Croushore, D. (2011). Frontiers of real-time data analysis. \textit{Journal of Economic Literature}, 49(1), 72--100.'),
    'CS': ('10.1016/S0304-4076(01)00072-0', 'Croushore and Stark (2001)', 'Croushore și Stark (2001)',
           r'Croushore, D., \& Stark, T. (2001). A real-time data set for macroeconomists. \textit{Journal of Econometrics}, 105(1), 111--130.'),
    'Dawid': ('10.2307/2981683', 'Dawid (1984)', 'Dawid (1984)',
              r'Dawid, A. P. (1984). Statistical theory: The prequential approach. \textit{Journal of the Royal Statistical Society, Series A}, 147(2), 278--292.'),
    'Die': ('10.1080/07350015.2014.983236', 'Diebold (2015)', 'Diebold (2015)',
            r'Diebold, F. X. (2015). Comparing predictive accuracy, twenty years later: A personal perspective on the use and abuse of Diebold--Mariano tests. \textit{Journal of Business \& Economic Statistics}, 33(1), 1.'),
    'DGT': ('10.2307/2527342', 'Diebold, Gunther and Tay (1998)', 'Diebold, Gunther și Tay (1998)',
            r'Diebold, F. X., Gunther, T. A., \& Tay, A. S. (1998). Evaluating density forecasts with applications to financial risk management. \textit{International Economic Review}, 39(4), 863--883.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'DP': ('10.1016/0169-2070(90)90028-A', 'Diebold and Pauly (1990)', 'Diebold și Pauly (1990)',
           r'Diebold, F. X., \& Pauly, P. (1990). The use of prior information in forecast combination. \textit{International Journal of Forecasting}, 6(4), 503--508.'),
    'EGJK': ('10.1111/rssb.12154', 'Ehm et al.\\ (2016)', 'Ehm et al.\\ (2016)',
             r'Ehm, W., Gneiting, T., Jordan, A., \& Krüger, F. (2016). Of quantiles and expectiles: Consistent scoring functions, Choquet representations and forecast rankings. \textit{Journal of the Royal Statistical Society, Series B}, 78(3), 505--562.'),
    'ET': ('10.1257/jel.46.1.3', 'Elliott and Timmermann (2008)', 'Elliott și Timmermann (2008)',
           r'Elliott, G., \& Timmermann, A. (2008). Economic forecasting. \textit{Journal of Economic Literature}, 46(1), 3--56.'),
    'Fama': ('10.1016/0304-3932(84)90046-1', 'Fama (1984)', 'Fama (1984)',
             r'Fama, E. F. (1984). Forward and spot exchange rates. \textit{Journal of Monetary Economics}, 14(3), 319--338.'),
    'FZ': ('10.1214/16-AOS1439', 'Fissler and Ziegel (2016)', 'Fissler și Ziegel (2016)',
           "Fissler, T., \\& Ziegel, J. F. (2016). Higher order elicitability and Osband's principle." + r' \textit{The Annals of Statistics}, 44(4), 1680--1707.'),
    'GKMT': ('10.1016/j.ijforecast.2012.06.004', 'Genre et al.\\ (2013)', 'Genre et al.\\ (2013)',
             r'Genre, V., Kenny, G., Meyler, A., \& Timmermann, A. (2013). Combining expert forecasts: Can anything beat the simple average? \textit{International Journal of Forecasting}, 29(1), 108--121.'),
    'GA': ('10.1016/j.jeconom.2011.02.017', 'Geweke and Amisano (2011)', 'Geweke și Amisano (2011)',
           r'Geweke, J., \& Amisano, G. (2011). Optimal prediction pools. \textit{Journal of Econometrics}, 164(1), 130--141.'),
    'GRaz': ('10.1002/jae.1177', 'Giacomini and Rossi (2010)', 'Giacomini și Rossi (2010)',
             r'Giacomini, R., \& Rossi, B. (2010). Forecast comparisons in unstable environments. \textit{Journal of Applied Econometrics}, 25(4), 595--620.'),
    'GW': ('10.1111/j.1468-0262.2006.00718.x', 'Giacomini and White (2006)', 'Giacomini și White (2006)',
           r'Giacomini, R., \& White, H. (2006). Tests of conditional predictive ability. \textit{Econometrica}, 74(6), 1545--1578.'),
    'Gnaa': ('10.1198/jasa.2011.r10138', 'Gneiting (2011)', 'Gneiting (2011)',
             r'Gneiting, T. (2011). Making and evaluating point forecasts. \textit{Journal of the American Statistical Association}, 106(494), 746--762.'),
    'GBR': ('10.1111/j.1467-9868.2007.00587.x', 'Gneiting, Balabdaoui and Raftery (2007)', 'Gneiting, Balabdaoui și Raftery (2007)',
            r'Gneiting, T., Balabdaoui, F., \& Raftery, A. E. (2007). Probabilistic forecasts, calibration and sharpness. \textit{Journal of the Royal Statistical Society, Series B}, 69(2), 243--268.'),
    'GK': ('10.1146/annurev-statistics-062713-085831', 'Gneiting and Katzfuss (2014)', 'Gneiting și Katzfuss (2014)',
           r'Gneiting, T., \& Katzfuss, M. (2014). Probabilistic forecasting. \textit{Annual Review of Statistics and Its Application}, 1, 125--151.'),
    'GRa': ('10.1198/016214506000001437', 'Gneiting and Raftery (2007)', 'Gneiting și Raftery (2007)',
            r'Gneiting, T., \& Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. \textit{Journal of the American Statistical Association}, 102(477), 359--378.'),
    'GRjaa': ('10.1198/jbes.2010.08110', 'Gneiting and Ranjan (2011)', 'Gneiting și Ranjan (2011)',
              r'Gneiting, T., \& Ranjan, R. (2011). Comparing density forecasts using threshold- and quantile-weighted scoring rules. \textit{Journal of Business \& Economic Statistics}, 29(3), 411--422.'),
    'GRjac': ('10.1214/13-EJS823', 'Gneiting and Ranjan (2013)', 'Gneiting și Ranjan (2013)',
              r'Gneiting, T., \& Ranjan, R. (2013). Combining predictive distributions. \textit{Electronic Journal of Statistics}, 7, 1747--1782.'),
    'Good': ('10.1111/j.2517-6161.1952.tb00104.x', 'Good (1952)', 'Good (1952)',
             r'Good, I. J. (1952). Rational decisions. \textit{Journal of the Royal Statistical Society, Series B}, 14(1), 107--114.'),
    'GRm': ('10.1002/for.3980030207', 'Granger and Ramanathan (1984)', 'Granger și Ramanathan (1984)',
            r'Granger, C. W. J., \& Ramanathan, R. (1984). Improved methods of combining forecasts. \textit{Journal of Forecasting}, 3(2), 197--204.'),
    'HM': ('10.1016/j.ijforecast.2006.08.001', 'Hall and Mitchell (2007)', 'Hall și Mitchell (2007)',
           r'Hall, S. G., \& Mitchell, J. (2007). Combining density forecasts. \textit{International Journal of Forecasting}, 23(1), 1--13.'),
    'Hamill': ('10.1175/1520-0493(2001)129<0550:IORHFV>2.0.CO;2', 'Hamill (2001)', 'Hamill (2001)',
               r'Hamill, T. M. (2001). Interpretation of rank histograms for verifying ensemble forecasts. \textit{Monthly Weather Review}, 129(3), 550--560.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'Han': ('10.1198/073500105000000063', 'Hansen (2005)', 'Hansen (2005)',
            r'Hansen, P. R. (2005). A test for superior predictive ability. \textit{Journal of Business \& Economic Statistics}, 23(4), 365--380.'),
    'HLNaa': ('10.3982/ECTA5771', 'Hansen, Lunde and Nason (2011)', 'Hansen, Lunde și Nason (2011)',
              r'Hansen, P. R., Lunde, A., \& Nason, J. M. (2011). The model confidence set. \textit{Econometrica}, 79(2), 453--497.'),
    'HLNig': ('10.1016/S0169-2070(96)00719-4', 'Harvey, Leybourne and Newbold (1997)', 'Harvey, Leybourne și Newbold (1997)',
              r'Harvey, D., Leybourne, S., \& Newbold, P. (1997). Testing the equality of prediction mean squared errors. \textit{International Journal of Forecasting}, 13(2), 281--291.'),
    'HLNih': ('10.1080/07350015.1998.10524759', 'Harvey, Leybourne and Newbold (1998)', 'Harvey, Leybourne și Newbold (1998)',
              r'Harvey, D. I., Leybourne, S. J., \& Newbold, P. (1998). Tests for forecast encompassing. \textit{Journal of Business \& Economic Statistics}, 16(2), 254--259.'),
    'HF': ('10.1016/j.ijforecast.2015.11.011', 'Hong and Fan (2016)', 'Hong și Fan (2016)',
           r'Hong, T., \& Fan, S. (2016). Probabilistic electric load forecasting: A tutorial review. \textit{International Journal of Forecasting}, 32(3), 914--938.'),
    'GEF': ('10.1016/j.ijforecast.2016.02.001', 'Hong et al.\\ (2016)', 'Hong et al.\\ (2016)',
            r'Hong, T., Pinson, P., Fan, S., Zareipour, H., Troccoli, A., \& Hyndman, R. J. (2016). Probabilistic energy forecasting: Global Energy Forecasting Competition 2014 and beyond. \textit{International Journal of Forecasting}, 32(3), 896--913.'),
    'HP': ('10.1007/978-3-031-13584-2', 'Huang and Petukhina (2022)', 'Huang și Petukhina (2022)',
           r'Huang, C., \& Petukhina, A. (2022). \textit{Applied Time Series Analysis and Forecasting with Python}. Springer.'),
    'HK': ('10.1016/j.ijforecast.2006.03.001', 'Hyndman and Koehler (2006)', 'Hyndman și Koehler (2006)',
           r'Hyndman, R. J., \& Koehler, A. B. (2006). Another look at measures of forecast accuracy. \textit{International Journal of Forecasting}, 22(4), 679--688.'),
    'KL': ('10.1017/9781108164818', 'Kilian and Lütkepohl (2017)', 'Kilian și Lütkepohl (2017)',
           r'Kilian, L., \& Lütkepohl, H. (2017). \textit{Structural Vector Autoregressive Analysis}. Cambridge University Press.'),
    'Md': ('10.1016/j.ijforecast.2019.04.014', 'Makridakis et al.\\ (2020)', 'Makridakis et al.\\ (2020)',
           r'Makridakis, S., Spiliotis, E., \& Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. \textit{International Journal of Forecasting}, 36(1), 54--74.'),
    'Me': ('10.1016/j.ijforecast.2021.11.013', 'Makridakis et al.\\ (2022)', 'Makridakis et al.\\ (2022)',
           r'Makridakis, S., Spiliotis, E., \& Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. \textit{International Journal of Forecasting}, 38(4), 1346--1364.'),
    'MW': ('10.1287/mnsc.22.10.1087', 'Matheson and Winkler (1976)', 'Matheson și Winkler (1976)',
           r'Matheson, J. E., \& Winkler, R. L. (1976). Scoring rules for continuous probability distributions. \textit{Management Science}, 22(10), 1087--1096.'),
    'MR': ('10.1016/0022-1996(83)90017-X', 'Meese and Rogoff (1983)', 'Meese și Rogoff (1983)',
           r'Meese, R. A., \& Rogoff, K. (1983). Empirical exchange rate models of the seventies. \textit{Journal of International Economics}, 14(1--2), 3--24.'),
    'MZ': ('https://www.nber.org/books-and-chapters/economic-forecasts-and-expectations-analysis-forecasting-behavior-and-performance/evaluation-economic-forecasts',
           'Mincer and Zarnowitz (1969)', 'Mincer și Zarnowitz (1969)',
           r'Mincer, J., \& Zarnowitz, V. (1969). The evaluation of economic forecasts. In J. Mincer (Ed.), \textit{Economic Forecasts and Expectations} (pp.\ 3--46). NBER.'),
    'NW': ('10.2307/1913610', 'Newey and West (1987)', 'Newey și West (1987)',
           r'Newey, W. K., \& West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. \textit{Econometrica}, 55(3), 703--708.'),
    'Pataa': ('10.1016/j.jeconom.2010.03.034', 'Patton (2011)', 'Patton (2011)',
              r'Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. \textit{Journal of Econometrics}, 160(1), 246--256.'),
    'Patbz': ('10.1080/07350015.2019.1585256', 'Patton (2020)', 'Patton (2020)',
              r'Patton, A. J. (2020). Comparing possibly misspecified forecasts. \textit{Journal of Business \& Economic Statistics}, 38(4), 796--809.'),
    'Petro': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
              r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., et al.\ (2022). Forecasting: theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'RWze': ('10.1111/j.1468-0262.2005.00615.x', 'Romano and Wolf (2005)', 'Romano și Wolf (2005)',
             r'Romano, J. P., \& Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. \textit{Econometrica}, 73(4), 1237--1282.'),
    'RS': ('10.1016/j.jeconom.2018.07.008', 'Rossi and Sekhposyan (2019)', 'Rossi și Sekhposyan (2019)',
           r'Rossi, B., \& Sekhposyan, T. (2019). Alternative tests for correct specification of conditional predictive densities. \textit{Journal of Econometrics}, 208(2), 638--657.'),
    'Sav': ('10.1080/01621459.1971.10482346', 'Savage (1971)', 'Savage (1971)',
            r'Savage, L. J. (1971). Elicitation of personal probabilities and expectations. \textit{Journal of the American Statistical Association}, 66(336), 783--801.'),
    'SH': ('10.1175/MWR-D-14-00269.1', 'Scheuerer and Hamill (2015)', 'Scheuerer și Hamill (2015)',
           r'Scheuerer, M., \& Hamill, T. M. (2015). Variogram-based proper scoring rules for probabilistic forecasts of multivariate quantities. \textit{Monthly Weather Review}, 143(4), 1321--1334.'),
    'SWal': ('10.1111/j.1468-0084.2008.00541.x', 'Smith and Wallis (2009)', 'Smith și Wallis (2009)',
             r'Smith, J., \& Wallis, K. F. (2009). A simple explanation of the forecast combination puzzle. \textit{Oxford Bulletin of Economics and Statistics}, 71(3), 331--355.'),
    'SC': ('10.1016/S0164-0704(02)00062-9', 'Stark and Croushore (2002)', 'Stark și Croushore (2002)',
           r'Stark, T., \& Croushore, D. (2002). Forecasting with a real-time data set for macroeconomists. \textit{Journal of Macroeconomics}, 24(4), 507--531.'),
    'SWii': ('10.1016/S0304-3932(99)00027-6', 'Stock and Watson (1999)', 'Stock și Watson (1999)',
             r'Stock, J. H., \& Watson, M. W. (1999). Forecasting inflation. \textit{Journal of Monetary Economics}, 44(2), 293--335.'),
    'SWzd': ('10.1002/for.928', 'Stock and Watson (2004)', 'Stock și Watson (2004)',
             r'Stock, J. H., \& Watson, M. W. (2004). Combination forecasts of output growth in a seven-country data set. \textit{Journal of Forecasting}, 23(6), 405--430.'),
    'Tim': ('10.1016/S1574-0706(05)01004-9', 'Timmermann (2006)', 'Timmermann (2006)',
            r'Timmermann, A. (2006). Forecast combinations. In G. Elliott, C. W. J. Granger, \& A. Timmermann (Eds.), \textit{Handbook of Economic Forecasting} (Vol.\ 1, pp.\ 135--196). Elsevier.'),
    'WHLK': ('10.1016/j.ijforecast.2022.11.005', 'Wang et al.\\ (2023)', 'Wang et al.\\ (2023)',
             r'Wang, X., Hyndman, R. J., Li, F., \& Kang, Y. (2023). Forecast combinations: An over 50-year review. \textit{International Journal of Forecasting}, 39(4), 1518--1547.'),
    'Weber': ('10.1111/j.1467-9965.2006.00277.x', 'Weber (2006)', 'Weber (2006)',
              r'Weber, S. (2006). Distribution-invariant risk measures, information, and dynamic consistency. \textit{Mathematical Finance}, 16(2), 419--441.'),
    'GWel': ('10.1093/rfs/hhm014', 'Welch and Goyal (2008)', 'Welch și Goyal (2008)',
             r'Welch, I., \& Goyal, A. (2008). A comprehensive look at the empirical performance of equity premium prediction. \textit{The Review of Financial Studies}, 21(4), 1455--1508.'),
    'West': ('10.2307/2171956', 'West (1996)', 'West (1996)',
             r'West, K. D. (1996). Asymptotic inference about predictive ability. \textit{Econometrica}, 64(5), 1067--1084.'),
    'White': ('10.1111/1468-0262.00152', 'White (2000)', 'White (2000)',
              r'White, H. (2000). A reality check for data snooping. \textit{Econometrica}, 68(5), 1097--1126.'),
    'ZW': ('10.1016/j.eneco.2017.12.016', 'Ziel and Weron (2018)', 'Ziel și Weron (2018)',
           r'Ziel, F., \& Weron, R. (2018). Day-ahead electricity price forecasting with high-dimensional structures: Univariate vs.\ multivariate modeling frameworks. \textit{Energy Economics}, 70, 396--420.'),
}


def _url(x):
    return x if x.startswith('http') else D_ + x


REFS = ''.join(ref(k, _url(v[0]).replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#'), v[1], v[2]) for k, v in R.items())


def bib(keys=None):
    """Bibliography entries (alphabetical, as ordered in R) with a clickable DOI or URL."""
    out = []
    for k, v in sorted(R.items(), key=lambda kv: re.sub(r'[^a-z]', '', kv[1][3].lower())):
        if keys is not None and k not in keys:
            continue
        u = _url(v[0])
        shown = ('doi:' + v[0]) if not v[0].startswith('http') else 'nber.org'
        safe_u = u.replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#')
        shown = shown.replace('_', '\\_').replace('<', '\\textless{}').replace('>', '\\textgreater{}').replace('#', '\\#')
        out.append(v[3] + f' \\href{{{safe_u}}}{{{shown}}}')
    return out
