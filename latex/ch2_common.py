r"""
ch2_common.py -- shared helpers of the Chapter 2 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_02/ch2_numbers.json (generate_all_charts.py) and
sem2_results.json (seminar2.py); the clickable citations of Chapter 2 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401
from ch1_common import T, V2, finalize, month, date, quarter, pv, minus_fix, ref, MONTHS_EN, MONTHS_RO   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_02')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_02'


def ym(s):
    """'2003-12' -> December 2003 / decembrie 2003."""
    return month(s + '-01' if len(s) == 7 else s)


def qq(s):
    """'1984Q1' -> 1984Q1 / T1 1984."""
    return quarter(s)


def load():
    with open(os.path.join(QL, 'ch2_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem2_results.json')) as f:
        return json.load(f)


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'And': ('10.2307/2951764', 'Andrews (1993)', 'Andrews (1993)',
            r'Andrews, D. W. K. (1993). Tests for parameter instability and structural change with unknown change point. \textit{Econometrica}, 61(4), 821--856.'),
    'AP': ('10.2307/2951753', 'Andrews and Ploberger (1994)', 'Andrews și Ploberger (1994)',
           r'Andrews, D. W. K., \& Ploberger, W. (1994). Optimal tests when a nuisance parameter is present only under the alternative. \textit{Econometrica}, 62(6), 1383--1414.'),
    'Bai': ('10.1162/003465397557132', 'Bai (1997)', 'Bai (1997)',
            r'Bai, J. (1997). Estimation of a change point in multiple regression models. \textit{The Review of Economics and Statistics}, 79(4), 551--563.'),
    'BPa': ('10.2307/2998540', 'Bai and Perron (1998)', 'Bai și Perron (1998)',
            r'Bai, J., \& Perron, P. (1998). Estimating and testing linear models with multiple structural changes. \textit{Econometrica}, 66(1), 47--78.'),
    'BPb': ('10.1002/jae.659', 'Bai and Perron (2003)', 'Bai și Perron (2003)',
            r'Bai, J., \& Perron, P. (2003). Computation and analysis of multiple structural change models. \textit{Journal of Applied Econometrics}, 18(1), 1--22.'),
    'BF': ('10.2307/2527284', 'Balke and Fomby (1997)', 'Balke și Fomby (1997)',
           r'Balke, N. S., \& Fomby, T. B. (1997). Threshold cointegration. \textit{International Economic Review}, 38(3), 627--645.'),
    'BDSL': ('10.1080/07474939608800353', 'Brock et al.\\ (1996)', 'Brock et al.\\ (1996)',
             r'Brock, W. A., Dechert, W. D., Scheinkman, J. A., \& LeBaron, B. (1996). A test for independence based on the correlation dimension. \textit{Econometric Reviews}, 15(3), 197--235.'),
    'BDE': ('10.1111/j.2517-6161.1975.tb01532.x', 'Brown, Durbin and Evans (1975)', 'Brown, Durbin și Evans (1975)',
            r'Brown, R. L., Durbin, J., \& Evans, J. M. (1975). Techniques for testing the constancy of regression relationships over time. \textit{Journal of the Royal Statistical Society, Series B}, 37(2), 149--192.'),
    'Car': ('10.1016/S0304-4076(02)00112-4', 'Carrasco (2002)', 'Carrasco (2002)',
            r'Carrasco, M. (2002). Misspecified structural change, threshold, and Markov-switching models. \textit{Journal of Econometrics}, 109(2), 239--273.'),
    'Cas': ('10.2307/2223329', 'Cassel (1918)', 'Cassel (1918)',
            r'Cassel, G. (1918). Abnormal deviations in international exchanges. \textit{The Economic Journal}, 28(112), 413--415.'),
    'CP': ('10.1093/acrefore/9780190625979.013.179', 'Casini and Perron (2019)', 'Casini și Perron (2019)',
           r'Casini, A., \& Perron, P. (2019). Structural breaks in time series. In \textit{Oxford Research Encyclopedia of Economics and Finance}. Oxford University Press.'),
    'Chan': ('10.1214/aos/1176349040', 'Chan (1993)', 'Chan (1993)',
             r'Chan, K. S. (1993). Consistency and limiting distribution of the least squares estimator of a threshold autoregressive model. \textit{The Annals of Statistics}, 21(1), 520--533.'),
    'Chow': ('10.2307/1910133', 'Chow (1960)', 'Chow (1960)',
             r'Chow, G. C. (1960). Tests of equality between sets of coefficients in two linear regressions. \textit{Econometrica}, 28(3), 591--605.'),
    'CHK': ('10.1093/biomet/82.3.603', 'Chu, Hornik and Kuan (1995)', 'Chu, Hornik și Kuan (1995)',
            r'Chu, C.-S. J., Hornik, K., \& Kuan, C.-M. (1995). MOSUM tests for parameter constancy. \textit{Biometrika}, 82(3), 603--617.'),
    'CSW': ('10.2307/2171955', 'Chu, Stinchcombe and White (1996)', 'Chu, Stinchcombe și White (1996)',
            r'Chu, C.-S. J., Stinchcombe, M., \& White, H. (1996). Monitoring structural change. \textit{Econometrica}, 64(5), 1045--1065.'),
    'CFS': ('10.1016/j.ijforecast.2003.10.004', 'Clements, Franses and Swanson (2004)', 'Clements, Franses și Swanson (2004)',
            r'Clements, M. P., Franses, P. H., \& Swanson, N. R. (2004). Forecasting economic and financial time-series with non-linear models. \textit{International Journal of Forecasting}, 20(2), 169--183.'),
    'CHa': ('10.1017/CBO9780511599286', 'Clements and Hendry (1998)', 'Clements și Hendry (1998)',
            r'Clements, M. P., \& Hendry, D. F. (1998). \textit{Forecasting Economic Time Series}. Cambridge University Press.'),
    'CHb': ('10.1016/S1574-0706(05)01012-8', 'Clements and Hendry (2006)', 'Clements și Hendry (2006)',
            r'Clements, M. P., \& Hendry, D. F. (2006). Forecasting with breaks. In G. Elliott, C. W. J. Granger, \& A. Timmermann (Eds.), \textit{Handbook of Economic Forecasting} (Vol.\ 1, pp.\ 605--657). Elsevier.'),
    'Dav': ('10.1093/biomet/74.1.33', 'Davies (1987)', 'Davies (1987)',
            r'Davies, R. B. (1987). Hypothesis testing when a nuisance parameter is present only under the alternative. \textit{Biometrika}, 74(1), 33--43.'),
    'DI': ('10.1016/S0304-4076(01)00073-2', 'Diebold and Inoue (2001)', 'Diebold și Inoue (2001)',
           r'Diebold, F. X., \& Inoue, A. (2001). Long memory and regime switching. \textit{Journal of Econometrics}, 105(1), 131--159.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'ET': ('10.1016/0304-4076(95)01751-8', 'Eitrheim and Teräsvirta (1996)', 'Eitrheim și Teräsvirta (1996)',
           r'Eitrheim, Ø., \& Teräsvirta, T. (1996). Testing the adequacy of smooth transition autoregressive models. \textit{Journal of Econometrics}, 74(1), 59--75.'),
    'ES': ('10.1198/073500101316970395', 'Enders and Siklos (2001)', 'Enders și Siklos (2001)',
           r'Enders, W., \& Siklos, P. L. (2001). Cointegration and threshold adjustment. \textit{Journal of Business \& Economic Statistics}, 19(2), 166--176.'),
    'Fry': ('10.1214/14-AOS1245', 'Fryzlewicz (2014)', 'Fryzlewicz (2014)',
            r'Fryzlewicz, P. (2014). Wild binary segmentation for multiple change-point detection. \textit{The Annals of Statistics}, 42(6), 2243--2281.'),
    'GP': ('10.2307/2109851', 'Garcia and Perron (1996)', 'Garcia și Perron (1996)',
           r'Garcia, R., \& Perron, P. (1996). An analysis of the real interest rate under regime shifts. \textit{The Review of Economics and Statistics}, 78(1), 111--125.'),
    'GRa': ('10.1111/j.1467-937X.2009.00545.x', 'Giacomini and Rossi (2009)', 'Giacomini și Rossi (2009)',
            r'Giacomini, R., \& Rossi, B. (2009). Detecting and predicting forecast breakdowns. \textit{The Review of Economic Studies}, 76(2), 669--705.'),
    'GRb': ('10.1002/jae.1177', 'Giacomini and Rossi (2010)', 'Giacomini și Rossi (2010)',
            r'Giacomini, R., \& Rossi, B. (2010). Forecast comparisons in unstable environments. \textit{Journal of Applied Econometrics}, 25(4), 595--620.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'Ha': ('10.2307/2171789', 'Hansen (1996)', 'Hansen (1996)',
           r'Hansen, B. E. (1996). Inference when a nuisance parameter is not identified under the null hypothesis. \textit{Econometrica}, 64(2), 413--430.'),
    'Hb': ('10.2202/1558-3708.1024', 'Hansen (1997)', 'Hansen (1997)',
           r'Hansen, B. E. (1997). Inference in TAR models. \textit{Studies in Nonlinear Dynamics \& Econometrics}, 2(1).'),
    'Hc': ('10.1111/1468-0262.00124', 'Hansen (2000)', 'Hansen (2000)',
           r'Hansen, B. E. (2000). Sample splitting and threshold estimation. \textit{Econometrica}, 68(3), 575--603.'),
    'Hd': ('10.1257/jep.15.4.117', 'Hansen (2001)', 'Hansen (2001)',
           r'Hansen, B. E. (2001). The new econometrics of structural change: Dating breaks in U.S. labor productivity. \textit{Journal of Economic Perspectives}, 15(4), 117--128.'),
    'He': ('10.4310/SII.2011.v4.n2.a4', 'Hansen (2011)', 'Hansen (2011)',
           r'Hansen, B. E. (2011). Threshold autoregression in economics. \textit{Statistics and Its Interface}, 4(2), 123--127.'),
    'HS': ('10.1016/S0304-4076(02)00097-0', 'Hansen and Seo (2002)', 'Hansen și Seo (2002)',
           r'Hansen, B. E., \& Seo, B. (2002). Testing for two-regime threshold cointegration in vector error-correction models. \textit{Journal of Econometrics}, 110(2), 293--318.'),
    'HLN': ('10.1016/S0169-2070(96)00719-4', 'Harvey, Leybourne and Newbold (1997)', 'Harvey, Leybourne și Newbold (1997)',
            r'Harvey, D., Leybourne, S., \& Newbold, P. (1997). Testing the equality of prediction mean squared errors. \textit{International Journal of Forecasting}, 13(2), 281--291.'),
    'Holm': ('https://www.jstor.org/stable/4615733', 'Holm (1979)', 'Holm (1979)',
             r'Holm, S. (1979). A simple sequentially rejective multiple test procedure. \textit{Scandinavian Journal of Statistics}, 6(2), 65--70.'),
    'HP': ('10.1007/978-3-031-13584-2', 'Huang and Petukhina (2022)', 'Huang și Petukhina (2022)',
           r'Huang, C., \& Petukhina, A. (2022). \textit{Applied Time Series Analysis and Forecasting with Python}. Springer.'),
    'IT': ('10.1080/01621459.1994.10476824', 'Inclán and Tiao (1994)', 'Inclán și Tiao (1994)',
           r'Inclán, C., \& Tiao, G. C. (1994). Use of cumulative sums of squares for retrospective detection of changes of variance. \textit{Journal of the American Statistical Association}, 89(427), 913--923.'),
    'IJR': ('10.1016/j.jeconom.2016.03.006', 'Inoue, Jin and Rossi (2017)', 'Inoue, Jin și Rossi (2017)',
            r'Inoue, A., Jin, L., \& Rossi, B. (2017). Rolling window selection for out-of-sample forecasting with time-varying parameters. \textit{Journal of Econometrics}, 196(1), 55--67.'),
    'KSS': ('10.1016/S0304-4076(02)00202-6', 'Kapetanios, Shin and Snell (2003)', 'Kapetanios, Shin și Snell (2003)',
            r'Kapetanios, G., Shin, Y., \& Snell, A. (2003). Testing for a unit root in the nonlinear STAR framework. \textit{Journal of Econometrics}, 112(2), 359--379.'),
    'KL': ('10.1017/9781108164818', 'Kilian and Lütkepohl (2017)', 'Kilian și Lütkepohl (2017)',
           r'Kilian, L., \& Lütkepohl, H. (2017). \textit{Structural Vector Autoregressive Analysis}. Cambridge University Press.'),
    'KFE': ('10.1080/01621459.2012.737745', 'Killick, Fearnhead and Eckley (2012)', 'Killick, Fearnhead și Eckley (2012)',
            r'Killick, R., Fearnhead, P., \& Eckley, I. A. (2012). Optimal detection of changepoints with a linear computational cost. \textit{Journal of the American Statistical Association}, 107(500), 1590--1598.'),
    'KPe': ('10.1016/j.jeconom.2008.08.019', 'Kim and Perron (2009)', 'Kim și Perron (2009)',
            r'Kim, D., \& Perron, P. (2009). Unit root tests allowing for a break in the trend function at an unknown time under both the null and alternative hypotheses. \textit{Journal of Econometrics}, 148(1), 1--13.'),
    'KPo': ('10.1080/07350015.1999.10524819', 'Koop and Potter (1999)', 'Koop și Potter (1999)',
            r'Koop, G., \& Potter, S. M. (1999). Dynamic asymmetries in U.S. unemployment. \textit{Journal of Business \& Economic Statistics}, 17(3), 298--312.'),
    'LS': ('10.1162/003465303772815961', 'Lee and Strazicich (2003)', 'Lee și Strazicich (2003)',
           r'Lee, J., \& Strazicich, M. C. (2003). Minimum Lagrange multiplier unit root test with two structural breaks. \textit{The Review of Economics and Statistics}, 85(4), 1082--1089.'),
    'LWZ': ('https://www3.stat.sinica.edu.tw/statistica/j7n2/j7n213/j7n213.htm', 'Liu, Wu and Zidek (1997)', 'Liu, Wu și Zidek (1997)',
            r'Liu, J., Wu, S., \& Zidek, J. V. (1997). On segmented multivariate regression. \textit{Statistica Sinica}, 7(2), 497--525.'),
    'LP': ('10.1162/003465397556791', 'Lumsdaine and Papell (1997)', 'Lumsdaine și Papell (1997)',
           r'Lumsdaine, R. L., \& Papell, D. H. (1997). Multiple trend breaks and the unit-root hypothesis. \textit{The Review of Economics and Statistics}, 79(2), 212--218.'),
    'LST': ('10.1093/biomet/75.3.491', 'Luukkonen, Saikkonen and Teräsvirta (1988)', 'Luukkonen, Saikkonen și Teräsvirta (1988)',
            r'Luukkonen, R., Saikkonen, P., \& Teräsvirta, T. (1988). Testing linearity against smooth transition autoregressive models. \textit{Biometrika}, 75(3), 491--499.'),
    'MPQ': ('10.1257/aer.90.5.1464', 'McConnell and Perez-Quiros (2000)', 'McConnell și Perez-Quiros (2000)',
            r"McConnell, M. M., \& Perez-Quiros, G. (2000). Output fluctuations in the United States: What has changed since the early 1980's? \textit{American Economic Review}, 90(5), 1464--1476."),
    'MNP': ('10.1086/262096', 'Michael, Nobay and Peel (1997)', 'Michael, Nobay și Peel (1997)',
            r'Michael, P., Nobay, A. R., \& Peel, D. A. (1997). Transactions costs and nonlinear adjustment in real exchange rates: An empirical investigation. \textit{Journal of Political Economy}, 105(4), 862--879.'),
    'MZTT': ('10.1080/01621459.1998.10473696', 'Montgomery et al.\\ (1998)', 'Montgomery et al.\\ (1998)',
             r'Montgomery, A. L., Zarnowitz, V., Tsay, R. S., \& Tiao, G. C. (1998). Forecasting the U.S. unemployment rate. \textit{Journal of the American Statistical Association}, 93(442), 478--493.'),
    'Nef': ('10.1086/261226', 'Neftçi (1984)', 'Neftçi (1984)',
            r'Neftçi, S. N. (1984). Are economic time series asymmetric over the business cycle? \textit{Journal of Political Economy}, 92(2), 307--328.'),
    'OP': ('10.1016/j.jeconom.2018.01.003', 'Oka and Perron (2018)', 'Oka și Perron (2018)',
           r'Oka, T., \& Perron, P. (2018). Testing for common breaks in a multiple equations system. \textit{Journal of Econometrics}, 204(1), 66--85.'),
    'Per': ('10.2307/1913712', 'Perron (1989)', 'Perron (1989)',
            r'Perron, P. (1989). The great crash, the oil price shock, and the unit root hypothesis. \textit{Econometrica}, 57(6), 1361--1401.'),
    'PP': ('10.1198/jbes.2010.09018', 'Pesaran and Pick (2011)', 'Pesaran și Pick (2011)',
           r'Pesaran, M. H., \& Pick, A. (2011). Forecast combination across estimation windows. \textit{Journal of Business \& Economic Statistics}, 29(2), 307--318.'),
    'PT': ('10.1016/j.jeconom.2006.03.010', 'Pesaran and Timmermann (2007)', 'Pesaran și Timmermann (2007)',
           r'Pesaran, M. H., \& Timmermann, A. (2007). Selection of estimation window in the presence of breaks. \textit{Journal of Econometrics}, 137(1), 134--161.'),
    'Petro': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
              r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., et al.\ (2022). Forecasting: theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'PK': ('10.2307/2951597', 'Ploberger and Krämer (1992)', 'Ploberger și Krämer (1992)',
           r'Ploberger, W., \& Krämer, W. (1992). The CUSUM test with OLS residuals. \textit{Econometrica}, 60(2), 271--285.'),
    'Qua': ('10.1080/01621459.1960.10482067', 'Quandt (1960)', 'Quandt (1960)',
            r'Quandt, R. E. (1960). Tests of the hypothesis that a linear regression system obeys two separate regimes. \textit{Journal of the American Statistical Association}, 55(290), 324--330.'),
    'RS': ('10.1214/aoms/1177696787', 'Robbins and Siegmund (1970)', 'Robbins și Siegmund (1970)',
           r'Robbins, H., \& Siegmund, D. (1970). Boundary crossing probabilities for the Wiener process and sample sums. \textit{The Annals of Mathematical Statistics}, 41(5), 1410--1429.'),
    'Ros': ('10.1016/B978-0-444-62731-5.00021-X', 'Rossi (2013)', 'Rossi (2013)',
            r'Rossi, B. (2013). Advances in forecasting under instability. In G. Elliott \& A. Timmermann (Eds.), \textit{Handbook of Economic Forecasting} (Vol.\ 2B, pp.\ 1203--1324). Elsevier.'),
    'SAC': ('https://econpapers.repec.org/RePEc:ubi:deawps:5', 'Sansó, Aragó and Carrion (2004)', 'Sansó, Aragó și Carrion (2004)',
            r'Sansó, A., Aragó, V., \& Carrion, J. L. (2004). Testing for changes in the unconditional variance of financial time series. \textit{Revista de Economía Financiera}, 4, 32--52.'),
    'SW': ('10.1080/07350015.1996.10524626', 'Stock and Watson (1996)', 'Stock și Watson (1996)',
           r'Stock, J. H., \& Watson, M. W. (1996). Evidence on structural instability in macroeconomic time series relations. \textit{Journal of Business \& Economic Statistics}, 14(1), 11--30.'),
    'TPS': ('10.1111/1468-2354.00144', 'Taylor, Peel and Sarno (2001)', 'Taylor, Peel și Sarno (2001)',
            r'Taylor, M. P., Peel, D. A., \& Sarno, L. (2001). Nonlinear mean-reversion in real exchange rates: Toward a solution to the purchasing power parity puzzles. \textit{International Economic Review}, 42(4), 1015--1042.'),
    'Ter': ('10.1080/01621459.1994.10476462', 'Teräsvirta (1994)', 'Teräsvirta (1994)',
            r'Teräsvirta, T. (1994). Specification, estimation, and evaluation of smooth transition autoregressive models. \textit{Journal of the American Statistical Association}, 89(425), 208--218.'),
    'TDM': ('10.1016/j.ijforecast.2005.04.010', 'Teräsvirta, van Dijk and Medeiros (2005)', 'Teräsvirta, van Dijk și Medeiros (2005)',
            r'Teräsvirta, T., van Dijk, D., \& Medeiros, M. C. (2005). Linear models, smooth transition autoregressions, and neural networks for forecasting macroeconomic time series: A re-examination. \textit{International Journal of Forecasting}, 21(4), 755--774.'),
    'TL': ('10.1111/j.2517-6161.1980.tb01126.x', 'Tong and Lim (1980)', 'Tong și Lim (1980)',
           r'Tong, H., \& Lim, K. S. (1980). Threshold autoregression, limit cycles and cyclical data. \textit{Journal of the Royal Statistical Society, Series B}, 42(3), 245--268.'),
    'TOV': ('10.1016/j.sigpro.2019.107299', 'Truong, Oudre and Vayatis (2020)', 'Truong, Oudre și Vayatis (2020)',
            r'Truong, C., Oudre, L., \& Vayatis, N. (2020). Selective review of offline change point detection methods. \textit{Signal Processing}, 167, 107299.'),
    'Tsa': ('10.1093/biomet/73.2.461', 'Tsay (1986)', 'Tsay (1986)',
            r'Tsay, R. S. (1986). Nonlinearity tests for time series. \textit{Biometrika}, 73(2), 461--466.'),
    'Tsb': ('10.1080/01621459.1989.10478760', 'Tsay (1989)', 'Tsay (1989)',
            r'Tsay, R. S. (1989). Testing and modeling threshold autoregressive processes. \textit{Journal of the American Statistical Association}, 84(405), 231--240.'),
    'VDTF': ('10.1081/ETC-120008723', 'van Dijk, Teräsvirta and Franses (2002)', 'van Dijk, Teräsvirta și Franses (2002)',
             r'van Dijk, D., Teräsvirta, T., \& Franses, P. H. (2002). Smooth transition autoregressive models: A survey of recent developments. \textit{Econometric Reviews}, 21(1), 1--47.'),
    'ZEIL': ('10.18637/jss.v007.i02', 'Zeileis et al.\\ (2002)', 'Zeileis et al.\\ (2002)',
             r'Zeileis, A., Leisch, F., Hornik, K., \& Kleiber, C. (2002). strucchange: An R package for testing for structural change in linear regression models. \textit{Journal of Statistical Software}, 7(2), 1--38.'),
    'ZA': ('10.1080/07350015.1992.10509904', 'Zivot and Andrews (1992)', 'Zivot și Andrews (1992)',
           r'Zivot, E., \& Andrews, D. W. K. (1992). Further evidence on the great crash, the oil-price shock, and the unit-root hypothesis. \textit{Journal of Business \& Economic Statistics}, 10(3), 251--270.'),
}


def _url(x):
    return x if x.startswith('http') else D_ + x


REFS = ''.join(ref(k, _url(v[0]).replace('#', '\\#'), v[1], v[2]) for k, v in R.items())


def bib(keys=None):
    """Bibliography entries (alphabetical) with a clickable DOI or URL."""
    out = []
    def key(kv):
        e = kv[1][3].lower().replace('van dijk', 'dijk')
        i = e.index('(')
        return (re.sub(r'[^a-z]', '', e[:i]), e[i:i + 6])
    for k, v in sorted(R.items(), key=key):
        if keys is not None and k not in keys:
            continue
        u = _url(v[0])
        shown = ('doi:' + v[0]) if not v[0].startswith('http') else u.split('/')[2]
        shown = shown.replace('_', '\\_')
        out.append(v[3] + f' \\href{{{u}}}{{{shown}}}')
    return out
