r"""
ch0_common.py -- shared helpers of the Chapter 0 generators (lecture and seminar), ATS
=====================================================================================
Numbers from Quantlets/Ch_00/ch0_numbers.json (generate_all_charts.py) and sem0_results.json (seminar0.py);
the clickable citations of Chapter 0 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_00')
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']
MONTHS_RO = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie',
             'octombrie', 'noiembrie', 'decembrie']


def T(en, ro=None):
    """Bilingual text ⟦EN||RO⟧."""
    return f'⟦{en}||{ro if ro is not None else en}⟧'


def month(s):
    y, m = int(s[:4]), int(s[5:7]) - 1
    return T(f'{MONTHS_EN[m]} {y}', f'{MONTHS_RO[m]} {y}')


def quarter(s):
    return f'{s[:4]}Q{(int(s[5:7]) - 1) // 3 + 1}'


def day(s):
    y, m, d = int(s[:4]), int(s[5:7]) - 1, int(s[8:10])
    return T(f'{d} {MONTHS_EN[m]} {y}', f'{d} {MONTHS_RO[m]} {y}')


def load():
    with open(os.path.join(QL, 'ch0_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem0_results.json')) as f:
        return json.load(f)


def finalize(V):
    """Negative numbers: a real minus sign in text and in math mode."""
    for k, v in list(V.items()):
        if isinstance(v, str) and v.startswith('⁅-'):
            V[k] = '⁅\\ensuremath{-}' + v[2:]
    return V


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
REFS = ''.join([
    ref('Hamilton', D_ + '10.2307/j.ctv14jx6sm', 'Hamilton (1994)'),
    ref('KL', D_ + '10.1017/9781108164818', 'Kilian and Lütkepohl (2017)', 'Kilian și Lütkepohl (2017)'),
    ref('DK', D_ + '10.1093/acprof:oso/9780199641178.001.0001', 'Durbin and Koopman (2012)', 'Durbin și Koopman (2012)'),
    ref('Petropoulos', D_ + '10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)'),
    ref('HP', D_ + '10.1007/978-3-031-13584-2', 'Huang and Petukhina (2022)', 'Huang și Petukhina (2022)'),
    ref('FPP', 'https://otexts.com/fpp3/', 'Hyndman and Athanasopoulos (2021)', 'Hyndman și Athanasopoulos (2021)'),
    ref('Lutkepohl', D_ + '10.1007/978-3-540-27752-1', 'Lütkepohl (2005)'),
    ref('SS', D_ + '10.1007/978-3-319-52452-8', 'Shumway and Stoffer (2017)', 'Shumway și Stoffer (2017)'),
    ref('Baltagi', D_ + '10.1007/978-3-030-53953-5', 'Baltagi (2021)'),
    ref('AB', D_ + '10.1561/2200000101', 'Angelopoulos and Bates (2023)', 'Angelopoulos și Bates (2023)'),
    ref('NW', D_ + '10.2307/1913610', 'Newey and West (1987)', 'Newey și West (1987)'),
    ref('NWb', D_ + '10.2307/2297912', 'Newey and West (1994)', 'Newey și West (1994)'),
    ref('Andrews', D_ + '10.2307/2938229', 'Andrews (1991)'),
    ref('AM', D_ + '10.2307/2951574', 'Andrews and Monahan (1992)', 'Andrews și Monahan (1992)'),
    ref('Kunsch', D_ + '10.1214/aos/1176347265', 'Künsch (1989)'),
    ref('Lahiri', D_ + '10.1007/978-1-4757-3803-2', 'Lahiri (2003)'),
    ref('PR', D_ + '10.1080/01621459.1994.10476870', 'Politis and Romano (1994)', 'Politis și Romano (1994)'),
    ref('PW', D_ + '10.1081/ETC-120028836', 'Politis and White (2004)', 'Politis și White (2004)'),
    ref('PPW', D_ + '10.1080/07474930802459016', 'Patton, Politis and White (2009)', 'Patton, Politis și White (2009)'),
    ref('KV', D_ + '10.1017/S0266466605050565', 'Kiefer and Vogelsang (2005)', 'Kiefer și Vogelsang (2005)'),
    ref('KVB', D_ + '10.1111/1468-0262.00128', 'Kiefer, Vogelsang and Bunzel (2000)', 'Kiefer, Vogelsang și Bunzel (2000)'),
    ref('KVb', D_ + '10.1111/1468-0262.00366', 'Kiefer and Vogelsang (2002)', 'Kiefer și Vogelsang (2002)'),
    ref('LLSW', D_ + '10.1080/07350015.2018.1506926', 'Lazarus et al.\\ (2018)'),
    ref('LLS', D_ + '10.3982/ECTA15404', 'Lazarus, Lewis and Stock (2021)', 'Lazarus, Lewis și Stock (2021)'),
    ref('Muller', D_ + '10.1080/07350015.2014.931238', 'Müller (2014)'),
    ref('SPJ', D_ + '10.1111/j.0012-9682.2008.00822.x', 'Sun, Phillips and Jin (2008)', 'Sun, Phillips și Jin (2008)'),
    ref('White', D_ + '10.1111/1468-0262.00152', 'White (2000)'),
    ref('Hansen', D_ + '10.1198/073500105000000063', 'Hansen (2005)'),
    ref('RW', D_ + '10.1111/j.1468-0262.2005.00615.x', 'Romano and Wolf (2005)', 'Romano și Wolf (2005)'),
    ref('STW', D_ + '10.1111/0022-1082.00163', 'Sullivan, Timmermann and White (1999)', 'Sullivan, Timmermann și White (1999)'),
    ref('LM', D_ + '10.1093/rfs/3.3.431', 'Lo and MacKinlay (1990)', 'Lo și MacKinlay (1990)'),
    ref('HLZ', D_ + '10.1093/rfs/hhv059', 'Harvey, Liu and Zhu (2016)', 'Harvey, Liu și Zhu (2016)'),
    ref('BH', D_ + '10.1111/j.2517-6161.1995.tb02031.x', 'Benjamini and Hochberg (1995)', 'Benjamini și Hochberg (1995)'),
    ref('Rosenblatt', D_ + '10.1073/pnas.42.1.43', 'Rosenblatt (1956)'),
    ref('Ibragimov', D_ + '10.1137/1107036', 'Ibragimov (1962)'),
    ref('Brown', D_ + '10.1214/aoms/1177693494', 'Brown (1971)'),
    ref('Billingsley', D_ + '10.1090/S0002-9939-1961-0126871-X', 'Billingsley (1961)'),
    ref('PS', D_ + '10.1214/aos/1176348666', 'Phillips and Solo (1992)', 'Phillips și Solo (1992)'),
    ref('Bradley', D_ + '10.1214/154957805100000104', 'Bradley (2005)'),
    ref('CC', D_ + '10.1017/S0266466602181023', 'Carrasco and Chen (2002)', 'Carrasco și Chen (2002)'),
    ref('Mokkadem', D_ + '10.1016/0304-4149(88)90045-2', 'Mokkadem (1988)'),
    ref('Birkhoff', D_ + '10.1073/pnas.17.2.656', 'Birkhoff (1931)'),
    ref('WhiteH', D_ + '10.2307/1912934', 'White (1980)'),
    ref('Efron', D_ + '10.1214/aos/1176344552', 'Efron (1979)'),
    ref('Singh', D_ + '10.1214/aos/1176345636', 'Singh (1981)'),
    ref('Wu', D_ + '10.1214/aos/1176350142', 'Wu (1986)'),
    ref('Liu', D_ + '10.1214/aos/1176351062', 'Liu (1988)'),
    ref('Mammen', D_ + '10.1214/aos/1176349025', 'Mammen (1993)'),
    ref('Shao', D_ + '10.1198/jasa.2009.tm08744', 'Shao (2010)'),
    ref('Buhlmann', D_ + '10.2307/3318584', 'Bühlmann (1997)'),
    ref('GK', D_ + '10.1016/j.jeconom.2003.10.030', 'Gonçalves and Kilian (2004)', 'Gonçalves și Kilian (2004)'),
    ref('GN', D_ + '10.1016/0304-4076(74)90034-7', 'Granger and Newbold (1974)', 'Granger și Newbold (1974)'),
    ref('Phillips', D_ + '10.1016/0304-4076(86)90001-1', 'Phillips (1986)'),
    ref('HH', D_ + '10.1086/260910', 'Hansen and Hodrick (1980)', 'Hansen și Hodrick (1980)'),
    ref('EH', D_ + '10.1111/j.1540-6261.1991.tb02674.x', 'Estrella and Hardouvelis (1991)', 'Estrella și Hardouvelis (1991)'),
    ref('Vilhuber', D_ + '10.1162/99608f92.4f6b9e67', 'Vilhuber (2020)'),
    ref('CM', D_ + '10.1257/jel.20171350', 'Christensen and Miguel (2018)', 'Christensen și Miguel (2018)'),
    ref('CS', D_ + '10.1016/S0304-4076(01)00072-0', 'Croushore and Stark (2001)', 'Croushore și Stark (2001)'),
])


def _b(authors, year, title, venue, doi, book=False):
    t = f'\\emph{{{title}}}' if book else title
    v = venue if book else f'\\emph{{{venue}}}'
    return f'{authors} ({year}). \\href{{https://doi.org/{doi}}}{{{t}}}. {v}.'.replace('\\emph{}', '')


BIB = [
    _b('Andrews, D.W.K.', 1991, 'Heteroskedasticity and autocorrelation consistent covariance matrix estimation', 'Econometrica}, 59(3), 817--858\\emph{', '10.2307/2938229'),
    _b('Andrews, D.W.K., Monahan, J.C.', 1992, 'An improved heteroskedasticity and autocorrelation consistent covariance matrix estimator', 'Econometrica}, 60(4), 953--966\\emph{', '10.2307/2951574'),
    r"Angelopoulos, A.N., Bates, S. (2023). \href{https://doi.org/10.1561/2200000101}{Conformal prediction: a gentle introduction}. \emph{Foundations and Trends in Machine Learning}, 16(4), 494--591.",
    r"Baltagi, B.H. (2021). \href{https://doi.org/10.1007/978-3-030-53953-5}{\emph{Econometric Analysis of Panel Data}} (6th ed.). Springer.",
    _b('Benjamini, Y., Hochberg, Y.', 1995, 'Controlling the false discovery rate: a practical and powerful approach to multiple testing', 'Journal of the Royal Statistical Society B}, 57(1), 289--300\\emph{', '10.1111/j.2517-6161.1995.tb02031.x'),
    _b('Billingsley, P.', 1961, 'The Lindeberg--Lévy theorem for martingales', 'Proceedings of the American Mathematical Society}, 12(5), 788--792\\emph{', '10.1090/S0002-9939-1961-0126871-X'),
    _b('Birkhoff, G.D.', 1931, 'Proof of the ergodic theorem', 'Proceedings of the National Academy of Sciences}, 17(12), 656--660\\emph{', '10.1073/pnas.17.2.656'),
    _b('Bradley, R.C.', 2005, 'Basic properties of strong mixing conditions. A survey and some open questions', 'Probability Surveys}, 2, 107--144\\emph{', '10.1214/154957805100000104'),
    _b('Brown, B.M.', 1971, 'Martingale central limit theorems', 'The Annals of Mathematical Statistics}, 42(1), 59--66\\emph{', '10.1214/aoms/1177693494'),
    _b('Bühlmann, P.', 1997, 'Sieve bootstrap for time series', 'Bernoulli}, 3(2), 123--148\\emph{', '10.2307/3318584'),
    _b('Carrasco, M., Chen, X.', 2002, 'Mixing and moment properties of various GARCH and stochastic volatility models', 'Econometric Theory}, 18(1), 17--39\\emph{', '10.1017/S0266466602181023'),
    _b('Christensen, G., Miguel, E.', 2018, 'Transparency, reproducibility, and the credibility of economics research', 'Journal of Economic Literature}, 56(3), 920--980\\emph{', '10.1257/jel.20171350'),
    _b('Croushore, D., Stark, T.', 2001, 'A real-time data set for macroeconomists', 'Journal of Econometrics}, 105(1), 111--130\\emph{', '10.1016/S0304-4076(01)00072-0'),
    r"Durbin, J., Koopman, S.J. (2012). \href{https://doi.org/10.1093/acprof:oso/9780199641178.001.0001}{\emph{Time Series Analysis by State Space Methods}} (2nd ed.). Oxford University Press.",
    _b('Efron, B.', 1979, 'Bootstrap methods: another look at the jackknife', 'The Annals of Statistics}, 7(1), 1--26\\emph{', '10.1214/aos/1176344552'),
    _b('Estrella, A., Hardouvelis, G.A.', 1991, 'The term structure as a predictor of real economic activity', 'The Journal of Finance}, 46(2), 555--576\\emph{', '10.1111/j.1540-6261.1991.tb02674.x'),
    _b('Gonçalves, S., Kilian, L.', 2004, 'Bootstrapping autoregressions with conditional heteroskedasticity of unknown form', 'Journal of Econometrics}, 123(1), 89--120\\emph{', '10.1016/j.jeconom.2003.10.030'),
    _b('Granger, C.W.J., Newbold, P.', 1974, 'Spurious regressions in econometrics', 'Journal of Econometrics}, 2(2), 111--120\\emph{', '10.1016/0304-4076(74)90034-7'),
    r"Hamilton, J.D. (1994). \href{https://doi.org/10.2307/j.ctv14jx6sm}{\emph{Time Series Analysis}}. Princeton University Press.",
    _b('Hansen, L.P., Hodrick, R.J.', 1980, 'Forward exchange rates as optimal predictors of future spot rates: an econometric analysis', 'Journal of Political Economy}, 88(5), 829--853\\emph{', '10.1086/260910'),
    _b('Hansen, P.R.', 2005, 'A test for superior predictive ability', 'Journal of Business \\& Economic Statistics}, 23(4), 365--380\\emph{', '10.1198/073500105000000063'),
    _b('Harvey, C.R., Liu, Y., Zhu, H.', 2016, '\\ldots and the cross-section of expected returns', 'The Review of Financial Studies}, 29(1), 5--68\\emph{', '10.1093/rfs/hhv059'),
    r"Huang, C., Petukhina, A. (2022). \href{https://doi.org/10.1007/978-3-031-13584-2}{\emph{Applied Time Series Analysis and Forecasting with Python}}. Springer.",
    r"Hyndman, R.J., Athanasopoulos, G. (2021). \href{https://otexts.com/fpp3/}{\emph{Forecasting: Principles and Practice}} (3rd ed.). OTexts.",
    _b('Ibragimov, I.A.', 1962, 'Some limit theorems for stationary processes', 'Theory of Probability and Its Applications}, 7(4), 349--382\\emph{', '10.1137/1107036'),
    _b('Kiefer, N.M., Vogelsang, T.J.', 2002, 'Heteroskedasticity-autocorrelation robust standard errors using the Bartlett kernel without truncation', 'Econometrica}, 70(5), 2093--2095\\emph{', '10.1111/1468-0262.00366'),
    _b('Kiefer, N.M., Vogelsang, T.J.', 2005, 'A new asymptotic theory for heteroskedasticity-autocorrelation robust tests', 'Econometric Theory}, 21(6), 1130--1164\\emph{', '10.1017/S0266466605050565'),
    _b('Kiefer, N.M., Vogelsang, T.J., Bunzel, H.', 2000, 'Simple robust testing of regression hypotheses', 'Econometrica}, 68(3), 695--714\\emph{', '10.1111/1468-0262.00128'),
    r"Kilian, L., Lütkepohl, H. (2017). \href{https://doi.org/10.1017/9781108164818}{\emph{Structural Vector Autoregressive Analysis}}. Cambridge University Press.",
    _b('Künsch, H.R.', 1989, 'The jackknife and the bootstrap for general stationary observations', 'The Annals of Statistics}, 17(3), 1217--1241\\emph{', '10.1214/aos/1176347265'),
    r"Lahiri, S.N. (2003). \href{https://doi.org/10.1007/978-1-4757-3803-2}{\emph{Resampling Methods for Dependent Data}}. Springer.",
    _b('Lazarus, E., Lewis, D.J., Stock, J.H.', 2021, 'The size-power tradeoff in HAR inference', 'Econometrica}, 89(5), 2497--2516\\emph{', '10.3982/ECTA15404'),
    _b('Lazarus, E., Lewis, D.J., Stock, J.H., Watson, M.W.', 2018, 'HAR inference: recommendations for practice', 'Journal of Business \\& Economic Statistics}, 36(4), 541--559\\emph{', '10.1080/07350015.2018.1506926'),
    _b('Liu, R.Y.', 1988, 'Bootstrap procedures under some non-i.i.d.\\ models', 'The Annals of Statistics}, 16(4), 1696--1708\\emph{', '10.1214/aos/1176351062'),
    _b('Lo, A.W., MacKinlay, A.C.', 1990, 'Data-snooping biases in tests of financial asset pricing models', 'The Review of Financial Studies}, 3(3), 431--467\\emph{', '10.1093/rfs/3.3.431'),
    r"Lütkepohl, H. (2005). \href{https://doi.org/10.1007/978-3-540-27752-1}{\emph{New Introduction to Multiple Time Series Analysis}}. Springer.",
    _b('Mammen, E.', 1993, 'Bootstrap and wild bootstrap for high dimensional linear models', 'The Annals of Statistics}, 21(1), 255--285\\emph{', '10.1214/aos/1176349025'),
    _b('Mokkadem, A.', 1988, 'Mixing properties of ARMA processes', 'Stochastic Processes and their Applications}, 29(2), 309--315\\emph{', '10.1016/0304-4149(88)90045-2'),
    _b('Müller, U.K.', 2014, 'HAC corrections for strongly autocorrelated time series', 'Journal of Business \\& Economic Statistics}, 32(3), 311--322\\emph{', '10.1080/07350015.2014.931238'),
    _b('Newey, W.K., West, K.D.', 1987, 'A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix', 'Econometrica}, 55(3), 703--708\\emph{', '10.2307/1913610'),
    _b('Newey, W.K., West, K.D.', 1994, 'Automatic lag selection in covariance matrix estimation', 'The Review of Economic Studies}, 61(4), 631--653\\emph{', '10.2307/2297912'),
    _b('Patton, A., Politis, D.N., White, H.', 2009, 'Correction to ``Automatic block-length selection for the dependent bootstrap\'\'', 'Econometric Reviews}, 28(4), 372--375\\emph{', '10.1080/07474930802459016'),
    r"Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M.Z., et al.\ (2022). \href{https://doi.org/10.1016/j.ijforecast.2021.11.001}{Forecasting: theory and practice}. \emph{International Journal of Forecasting}, 38(3), 705--871.",
    _b('Phillips, P.C.B.', 1986, 'Understanding spurious regressions in econometrics', 'Journal of Econometrics}, 33(3), 311--340\\emph{', '10.1016/0304-4076(86)90001-1'),
    _b('Phillips, P.C.B., Solo, V.', 1992, 'Asymptotics for linear processes', 'The Annals of Statistics}, 20(2), 971--1001\\emph{', '10.1214/aos/1176348666'),
    _b('Politis, D.N., Romano, J.P.', 1994, 'The stationary bootstrap', 'Journal of the American Statistical Association}, 89(428), 1303--1313\\emph{', '10.1080/01621459.1994.10476870'),
    _b('Politis, D.N., White, H.', 2004, 'Automatic block-length selection for the dependent bootstrap', 'Econometric Reviews}, 23(1), 53--70\\emph{', '10.1081/ETC-120028836'),
    _b('Romano, J.P., Wolf, M.', 2005, 'Stepwise multiple testing as formalized data snooping', 'Econometrica}, 73(4), 1237--1282\\emph{', '10.1111/j.1468-0262.2005.00615.x'),
    _b('Rosenblatt, M.', 1956, 'A central limit theorem and a strong mixing condition', 'Proceedings of the National Academy of Sciences}, 42(1), 43--47\\emph{', '10.1073/pnas.42.1.43'),
    _b('Shao, X.', 2010, 'The dependent wild bootstrap', 'Journal of the American Statistical Association}, 105(489), 218--235\\emph{', '10.1198/jasa.2009.tm08744'),
    r"Shumway, R.H., Stoffer, D.S. (2017). \href{https://doi.org/10.1007/978-3-319-52452-8}{\emph{Time Series Analysis and Its Applications}} (4th ed.). Springer.",
    _b('Singh, K.', 1981, "On the asymptotic accuracy of Efron's bootstrap", 'The Annals of Statistics}, 9(6), 1187--1195\\emph{', '10.1214/aos/1176345636'),
    _b('Sullivan, R., Timmermann, A., White, H.', 1999, 'Data-snooping, technical trading rule performance, and the bootstrap', 'The Journal of Finance}, 54(5), 1647--1691\\emph{', '10.1111/0022-1082.00163'),
    _b('Sun, Y., Phillips, P.C.B., Jin, S.', 2008, 'Optimal bandwidth selection in heteroskedasticity--autocorrelation robust testing', 'Econometrica}, 76(1), 175--194\\emph{', '10.1111/j.0012-9682.2008.00822.x'),
    _b('Vilhuber, L.', 2020, 'Reproducibility and replicability in economics', 'Harvard Data Science Review}, 2(4)\\emph{', '10.1162/99608f92.4f6b9e67'),
    _b('White, H.', 1980, 'A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity', 'Econometrica}, 48(4), 817--838\\emph{', '10.2307/1912934'),
    _b('White, H.', 2000, 'A reality check for data snooping', 'Econometrica}, 68(5), 1097--1126\\emph{', '10.1111/1468-0262.00152'),
    _b('Wu, C.F.J.', 1986, 'Jackknife, bootstrap and other resampling methods in regression analysis', 'The Annals of Statistics}, 14(4), 1261--1295\\emph{', '10.1214/aos/1176350142'),
]
