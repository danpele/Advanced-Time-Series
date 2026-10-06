r"""
ch9_common.py -- shared helpers of the Chapter 9 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_09/ch9_numbers.json (generate_all_charts.py) and
sem9_results.json (seminar9.py); the clickable citations of Chapter 7 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_09')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_09'
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
    with open(os.path.join(QL, 'ch9_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem9_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'AT': ('10.1016/S0378-4266(02)00283-2', 'Acerbi and Tasche (2002)', 'Acerbi și Tasche (2002)',
           r'Acerbi, C., \& Tasche, D. (2002). On the coherence of expected shortfall. \textit{Journal of Banking \& Finance}, 26(7), 1487--1503.'),
    'AS': ('https://www.msci.com/documents/10199/22aa9922-f874-4060-b77a-0f0e267a489b', 'Acerbi and Székely (2014)', 'Acerbi și Székely (2014)',
           r'Acerbi, C., \& Székely, B. (2014). Backtesting expected shortfall. \textit{Risk}, December 2014 (MSCI working paper).'),
    'ADEH': ('10.1111/1467-9965.00068', 'Artzner et al.\\ (1999)', 'Artzner et al.\\ (1999)',
             r'Artzner, P., Delbaen, F., Eber, J.-M., \& Heath, D. (1999). Coherent measures of risk. \textit{Mathematical Finance}, 9(3), 203--228.'),
    'BCBS': ('https://www.bis.org/publ/bcbs22.htm', 'Basel Committee (1996)', 'Comitetul de la Basel (1996)',
             r'Basel Committee on Banking Supervision (1996). \textit{Supervisory framework for the use of ``backtesting'' in conjunction with the internal models approach to market risk capital requirements}. Bank for International Settlements.'),
    'MAR': ('https://www.bis.org/basel_framework/chapter/MAR/33.htm', 'Basel Committee (MAR33)', 'Comitetul de la Basel (MAR33)',
            r'Basel Committee on Banking Supervision (2019). \textit{MAR33: Internal models approach, capital requirements calculation}. Basel Framework, Bank for International Settlements.'),
    'BD': ('10.1093/jjfinec/nbaa013', 'Bayer and Dimitriadis (2022)', 'Bayer și Dimitriadis (2022)',
           r'Bayer, S., \& Dimitriadis, T. (2022). Regression-based expected shortfall backtesting. \textit{Journal of Financial Econometrics}, 20(3), 437--471.'),
    'Boll': ('10.1016/0304-4076(86)90063-1', 'Bollerslev (1986)', 'Bollerslev (1986)',
             r'Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. \textit{Journal of Econometrics}, 31(3), 307--327.'),
    'BDKM': ('10.1016/j.jbankfin.2014.03.019', 'Boucher et al.\\ (2014)', 'Boucher et al.\\ (2014)',
             r'Boucher, C. M., Daníelsson, J., Kouontchou, P. S., \& Maillet, B. B. (2014). Risk models-at-risk. \textit{Journal of Banking \& Finance}, 44, 72--92.'),
    'Chr': ('10.2307/2527341', 'Christoffersen (1998)', 'Christoffersen (1998)',
            r'Christoffersen, P. F. (1998). Evaluating interval forecasts. \textit{International Economic Review}, 39(4), 841--862.'),
    'CG': ('10.21314/JOR.2005.112', 'Christoffersen and Gonçalves (2005)', 'Christoffersen și Gonçalves (2005)',
           r'Christoffersen, P., \& Gonçalves, S. (2005). Estimation risk in financial risk management. \textit{The Journal of Risk}, 7(3), 1--28.'),
    'CP': ('10.1093/jjfinec/nbh004', 'Christoffersen and Pelletier (2004)', 'Christoffersen și Pelletier (2004)',
           r'Christoffersen, P., \& Pelletier, D. (2004). Backtesting value-at-risk: A duration-based approach. \textit{Journal of Financial Econometrics}, 2(1), 84--108.'),
    'CKL': ('10.1002/jae.1279', 'Creal, Koopman and Lucas (2013)', 'Creal, Koopman și Lucas (2013)',
            r'Creal, D., Koopman, S. J., \& Lucas, A. (2013). Generalized autoregressive score models with applications. \textit{Journal of Applied Econometrics}, 28(5), 777--795.'),
    'DJVZ': ('10.1016/j.jfs.2016.02.002', 'Danielsson et al.\\ (2016)', 'Danielsson et al.\\ (2016)',
             r'Danielsson, J., James, K. R., Valenzuela, M., \& Zer, I. (2016). Model risk of risk models. \textit{Journal of Financial Stability}, 23, 79--91.'),
    'DZ': ('10.1016/j.jbankfin.2005.10.002', 'Daníelsson and Zigrand (2006)', 'Daníelsson și Zigrand (2006)',
           r'Daníelsson, J., \& Zigrand, J.-P. (2006). On time-scaling of risk and the square-root-of-time rule. \textit{Journal of Banking \& Finance}, 30(10), 2701--2713.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'DB': ('10.1214/19-EJS1560', 'Dimitriadis and Bayer (2019)', 'Dimitriadis și Bayer (2019)',
           r'Dimitriadis, T., \& Bayer, S. (2019). A joint quantile and expected shortfall regression framework. \textit{Electronic Journal of Statistics}, 13(1), 1823--1871.'),
    'DE': ('10.1287/mnsc.2015.2342', 'Du and Escanciano (2017)', 'Du și Escanciano (2017)',
           r'Du, Z., \& Escanciano, J. C. (2017). Backtesting expected shortfall: Accounting for tail risk. \textit{Management Science}, 63(4), 940--958.'),
    'EGJK': ('10.1111/rssb.12154', 'Ehm et al.\\ (2016)', 'Ehm et al.\\ (2016)',
             r'Ehm, W., Gneiting, T., Jordan, A., \& Krüger, F. (2016). Of quantiles and expectiles: Consistent scoring functions, Choquet representations and forecast rankings. \textit{Journal of the Royal Statistical Society: Series B}, 78(3), 505--562.'),
    'EKM': ('10.1007/978-3-642-33483-2', 'Embrechts, Klüppelberg and Mikosch (1997)', 'Embrechts, Klüppelberg și Mikosch (1997)',
            r'Embrechts, P., Klüppelberg, C., \& Mikosch, T. (1997). \textit{Modelling Extremal Events for Insurance and Finance}. Springer.'),
    'EM': ('10.1198/073500104000000370', 'Engle and Manganelli (2004)', 'Engle și Manganelli (2004)',
           r'Engle, R. F., \& Manganelli, S. (2004). CAViaR: Conditional autoregressive value at risk by regression quantiles. \textit{Journal of Business \& Economic Statistics}, 22(4), 367--381.'),
    'EO': ('10.1198/jbes.2009.07063', 'Escanciano and Olmo (2010)', 'Escanciano și Olmo (2010)',
           r'Escanciano, J. C., \& Olmo, J. (2010). Backtesting parametric value-at-risk with estimation risk. \textit{Journal of Business \& Economic Statistics}, 28(1), 36--51.'),
    'FS': ('10.1111/1467-9868.00401', 'Ferro and Segers (2003)', 'Ferro și Segers (2003)',
           r'Ferro, C. A. T., \& Segers, J. (2003). Inference for clusters of extreme values. \textit{Journal of the Royal Statistical Society: Series B}, 65(2), 545--556.'),
    'FZ': ('10.1214/16-AOS1439', 'Fissler and Ziegel (2016)', 'Fissler și Ziegel (2016)',
           r"Fissler, T., \& Ziegel, J. F. (2016). Higher order elicitability and Osband's principle. \textit{The Annals of Statistics}, 44(4), 1680--1707."),
    'FZG': ('https://arxiv.org/abs/1507.00244', 'Fissler, Ziegel and Gneiting (2016)', 'Fissler, Ziegel și Gneiting (2016)',
            r'Fissler, T., Ziegel, J. F., \& Gneiting, T. (2016). Expected shortfall is jointly elicitable with value at risk: Implications for backtesting. \textit{Risk}, January 2016, 58--61; arXiv:1507.00244.'),
    'GLLS': ('10.1198/jbes.2010.07318', 'Gaglianone et al.\\ (2011)', 'Gaglianone et al.\\ (2011)',
             r'Gaglianone, W. P., Lima, L. R., Linton, O., \& Smith, D. R. (2011). Evaluating value-at-risk models via quantile regression. \textit{Journal of Business \& Economic Statistics}, 29(1), 150--160.'),
    'GS': ('10.1017/S0266466608080559', 'Gao and Song (2008)', 'Gao și Song (2008)',
           r'Gao, F., \& Song, F. (2008). Estimation risk in GARCH VaR and ES estimates. \textit{Econometric Theory}, 24(5), 1404--1424.'),
    'GC': ('https://arxiv.org/abs/2106.00170', 'Gibbs and Candès (2021)', 'Gibbs și Candès (2021)',
           r'Gibbs, I., \& Candès, E. (2021). Adaptive conformal inference under distribution shift. \textit{Advances in Neural Information Processing Systems}, 34; arXiv:2106.00170.'),
    'GW': ('10.1111/j.1468-0262.2006.00718.x', 'Giacomini and White (2006)', 'Giacomini și White (2006)',
           r'Giacomini, R., \& White, H. (2006). Tests of conditional predictive ability. \textit{Econometrica}, 74(6), 1545--1578.'),
    'GJR': ('10.1111/j.1540-6261.1993.tb05128.x', 'Glosten, Jagannathan and Runkle (1993)', 'Glosten, Jagannathan și Runkle (1993)',
            r'Glosten, L. R., Jagannathan, R., \& Runkle, D. E. (1993). On the relation between the expected value and the volatility of the nominal excess return on stocks. \textit{The Journal of Finance}, 48(5), 1779--1801.'),
    'Gn': ('10.1198/jasa.2011.r10138', 'Gneiting (2011)', 'Gneiting (2011)',
           r'Gneiting, T. (2011). Making and evaluating point forecasts. \textit{Journal of the American Statistical Association}, 106(494), 746--762.'),
    'GR': ('10.1198/016214506000001437', 'Gneiting and Raftery (2007)', 'Gneiting și Raftery (2007)',
           r'Gneiting, T., \& Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. \textit{Journal of the American Statistical Association}, 102(477), 359--378.'),
    'Han': ('10.2307/2527081', 'Hansen (1994)', 'Hansen (1994)',
            r'Hansen, B. E. (1994). Autoregressive conditional density estimation. \textit{International Economic Review}, 35(3), 705--730.'),
    'HLN': ('10.3982/ECTA5771', 'Hansen, Lunde and Nason (2011)', 'Hansen, Lunde și Nason (2011)',
            r'Hansen, P. R., Lunde, A., \& Nason, J. M. (2011). The model confidence set. \textit{Econometrica}, 79(2), 453--497.'),
    'HE': ('10.1214/13-AOAS709', 'Holzmann and Eulert (2014)', 'Holzmann și Eulert (2014)',
           r'Holzmann, H., \& Eulert, M. (2014). The role of the information set for forecasting -- with applications to risk management. \textit{The Annals of Applied Statistics}, 8(1), 595--621.'),
    'KR': ('10.1016/j.jedc.2016.05.002', 'Kellner and Rösch (2016)', 'Kellner și Rösch (2016)',
           r'Kellner, R., \& Rösch, D. (2016). Quantifying market risk with value-at-risk or expected shortfall? Consequences for capital requirements and model risk. \textit{Journal of Economic Dynamics and Control}, 68, 45--63.'),
    'KB': ('10.2307/1913643', 'Koenker and Bassett (1978)', 'Koenker și Bassett (1978)',
           r'Koenker, R., \& Bassett, G. (1978). Regression quantiles. \textit{Econometrica}, 46(1), 33--50.'),
    'Koe': ('10.1017/CBO9780511754098', 'Koenker (2005)', 'Koenker (2005)',
            r'Koenker, R. (2005). \textit{Quantile Regression}. Cambridge University Press.'),
    'KX': ('10.1198/016214506000000672', 'Koenker and Xiao (2006)', 'Koenker și Xiao (2006)',
           r'Koenker, R., \& Xiao, Z. (2006). Quantile autoregression. \textit{Journal of the American Statistical Association}, 101(475), 980--990.'),
    'KLM': ('10.1016/j.jbankfin.2018.01.002', 'Kratz, Lok and McNeil (2018)', 'Kratz, Lok și McNeil (2018)',
            r'Kratz, M., Lok, Y. H., \& McNeil, A. J. (2018). Multinomial VaR backtests: A simple implicit approach to backtesting expected shortfall. \textit{Journal of Banking \& Finance}, 88, 393--407.'),
    'Kup': ('10.3905/jod.1995.407942', 'Kupiec (1995)', 'Kupiec (1995)',
            r'Kupiec, P. H. (1995). Techniques for verifying the accuracy of risk measurement models. \textit{The Journal of Derivatives}, 3(2), 73--84.'),
    'MF': ('10.1016/S0927-5398(00)00012-8', 'McNeil and Frey (2000)', 'McNeil și Frey (2000)',
           r'McNeil, A. J., \& Frey, R. (2000). Estimation of tail-related risk measures for heteroscedastic financial time series: An extreme value approach. \textit{Journal of Empirical Finance}, 7(3--4), 271--300.'),
    'NZ': ('10.1214/17-AOAS1041', 'Nolde and Ziegel (2017)', 'Nolde și Ziegel (2017)',
           r'Nolde, N., \& Ziegel, J. F. (2017). Elicitability and backtesting: Perspectives for banking regulation. \textit{The Annals of Applied Statistics}, 11(4), 1833--1874.'),
    'PZC': ('10.1016/j.jeconom.2018.10.008', 'Patton, Ziegel and Chen (2019)', 'Patton, Ziegel și Chen (2019)',
            r'Patton, A. J., Ziegel, J. F., \& Chen, R. (2019). Dynamic semiparametric models for expected shortfall (and value-at-risk). \textit{Journal of Econometrics}, 211(2), 388--413.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'TayA': ('10.1093/jjfinec/nbn001', 'Taylor (2008)', 'Taylor (2008)',
             r'Taylor, J. W. (2008). Estimating value at risk and expected shortfall using expectiles. \textit{Journal of Financial Econometrics}, 6(2), 231--252.'),
    'TayB': ('10.1080/07350015.2017.1281815', 'Taylor (2019)', 'Taylor (2019)',
             r'Taylor, J. W. (2019). Forecasting value at risk and expected shortfall using a semiparametric approach based on the asymmetric Laplace distribution. \textit{Journal of Business \& Economic Statistics}, 37(1), 121--133.'),
    'Web': ('10.1111/j.1467-9965.2006.00277.x', 'Weber (2006)', 'Weber (2006)',
            r'Weber, S. (2006). Distribution-invariant risk measures, information, and dynamic consistency. \textit{Mathematical Finance}, 16(2), 419--441.'),
    'Zie': ('10.1111/mafi.12080', 'Ziegel (2016)', 'Ziegel (2016)',
            r'Ziegel, J. F. (2016). Coherence and elicitability. \textit{Mathematical Finance}, 26(4), 901--918.'),
    'CO': ('https://github.com/danpele/Conformal_Oracle', 'Pele et al.\\ (Conformal\\_Oracle)', 'Pele et al.\\ (Conformal\\_Oracle)',
           r'Pele, D. T., Bolovăneanu, V., Ginavar, A., Lessmann, S., \& Härdle, W. K. Conformal recalibration of extreme tail quantiles under temporal dependence. Working paper and replication package (further reading).'),
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
