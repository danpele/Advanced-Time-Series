r"""
ch10_common.py -- shared helpers of the Chapter 10 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_10/ch10_numbers.json (generate_all_charts.py) and
sem10_results.json (seminar9.py); the clickable citations of Chapter 10 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_10')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_10'
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
    with open(os.path.join(QL, 'ch10_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem10_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
OMI_URL = 'https://web.archive.org/web/20220301022212/https://realized.oxford-man.ox.ac.uk/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'ABDL': ('10.1111/1468-0262.00418', 'Andersen et al.\\ (2003)', 'Andersen et al.\\ (2003)',
             r'Andersen, T. G., Bollerslev, T., Diebold, F. X., \& Labys, P. (2003). Modeling and forecasting realized volatility. \textit{Econometrica}, 71(2), 579--625.'),
    'AnSu': ('10.1111/j.1468-0262.2004.00501.x', 'Andrews and Sun (2004)', 'Andrews și Sun (2004)',
             r'Andrews, D. W. K., \& Sun, Y. (2004). Adaptive local polynomial Whittle estimation of long-range dependence. \textit{Econometrica}, 72(2), 569--614.'),
    'BBM': ('10.1016/S0304-4076(95)01749-6', 'Baillie, Bollerslev and Mikkelsen (1996)', 'Baillie, Bollerslev și Mikkelsen (1996)',
            r'Baillie, R. T., Bollerslev, T., \& Mikkelsen, H. O. (1996). Fractionally integrated generalized autoregressive conditional heteroskedasticity. \textit{Journal of Econometrics}, 74(1), 3--30.'),
    'BCT': ('10.1002/(SICI)1099-1255(199601)11:1<23::AID-JAE374>3.0.CO;2-M', 'Baillie, Chung and Tieslau (1996)', 'Baillie, Chung și Tieslau (1996)',
            r'Baillie, R. T., Chung, C.-F., \& Tieslau, M. A. (1996). Analysing inflation by the fractionally integrated ARFIMA--GARCH model. \textit{Journal of Applied Econometrics}, 11(1), 23--40.'),
    'BP': ('10.1093/jjfinec/nbl003', 'Bandi and Perron (2006)', 'Bandi și Perron (2006)',
           r'Bandi, F. M., \& Perron, B. (2006). Long memory and the relation between implied and realized volatility. \textit{Journal of Financial Econometrics}, 4(4), 636--670.'),
    'BFG': ('10.1080/14697688.2015.1099717', 'Bayer, Friz and Gatheral (2016)', 'Bayer, Friz și Gatheral (2016)',
            r'Bayer, C., Friz, P., \& Gatheral, J. (2016). Pricing under rough volatility. \textit{Quantitative Finance}, 16(6), 887--904.'),
    'BLPa': ('10.1007/s00780-017-0335-5', 'Bennedsen, Lunde and Pakkanen (2017)', 'Bennedsen, Lunde și Pakkanen (2017)',
             r'Bennedsen, M., Lunde, A., \& Pakkanen, M. S. (2017). Hybrid scheme for Brownian semistationary processes. \textit{Finance and Stochastics}, 21(4), 931--965.'),
    'BLPb': ('10.1093/jjfinec/nbaa049', 'Bennedsen, Lunde and Pakkanen (2022)', 'Bennedsen, Lunde și Pakkanen (2022)',
             r'Bennedsen, M., Lunde, A., \& Pakkanen, M. S. (2022). Decoupling the short- and long-term behavior of stochastic volatility. \textit{Journal of Financial Econometrics}, 20(5), 961--1006.'),
    'BFGK': ('10.1007/978-3-642-35512-7', 'Beran et al.\\ (2013)', 'Beran et al.\\ (2013)',
             r'Beran, J., Feng, Y., Ghosh, S., \& Kulik, R. (2013). \textit{Long-Memory Processes: Probabilistic Properties and Statistical Methods}. Springer.'),
    'BCPV': ('10.1016/j.jeconom.2022.06.009', 'Bolko et al.\\ (2023)', 'Bolko et al.\\ (2023)',
             r'Bolko, A. E., Christensen, K., Pakkanen, M. S., \& Veliyev, B. (2023). A GMM approach to estimate the roughness of stochastic volatility. \textit{Journal of Econometrics}, 235(2), 745--778.'),
    'BCL': ('10.1016/S0304-4076(97)00072-9', 'Breidt, Crato and de Lima (1998)', 'Breidt, Crato și de Lima (1998)',
            r'Breidt, F. J., Crato, N., \& de Lima, P. (1998). The detection and estimation of long memory in stochastic volatility. \textit{Journal of Econometrics}, 83(1--2), 325--348.'),
    'CN': ('10.1016/j.jeconom.2005.03.018', 'Christensen and Nielsen (2006)', 'Christensen și Nielsen (2006)',
           r'Christensen, B. J., \& Nielsen, M. Ø. (2006). Asymptotic normality of narrow-band least squares in the stationary fractional cointegration model and volatility forecasting. \textit{Journal of Econometrics}, 133(1), 343--371.'),
    'CR': ('10.1111/1467-9965.00057', 'Comte and Renault (1998)', 'Comte și Renault (1998)',
           r'Comte, F., \& Renault, E. (1998). Long memory in continuous-time stochastic volatility models. \textit{Mathematical Finance}, 8(4), 291--323.'),
    'CD': ('10.1007/s13571-024-00322-2', 'Cont and Das (2024)', 'Cont și Das (2024)',
           r'Cont, R., \& Das, P. (2024). Rough volatility: Fact or artefact? \textit{Sankhya B}, 86(1), 191--223.'),
    'Cor': ('10.1093/jjfinec/nbp001', 'Corsi (2009)', 'Corsi (2009)',
            r'Corsi, F. (2009). A simple approximate long-memory model of realized volatility. \textit{Journal of Financial Econometrics}, 7(2), 174--196.'),
    'Dav': ('10.1198/073500103288619359', 'Davidson (2004)', 'Davidson (2004)',
            r'Davidson, J. (2004). Moment and memory properties of linear conditional heteroscedasticity models, and a new model. \textit{Journal of Business \& Economic Statistics}, 22(1), 16--29.'),
    'DH': ('10.1093/biomet/74.1.95', 'Davies and Harte (1987)', 'Davies și Harte (1987)',
           r'Davies, R. B., \& Harte, D. S. (1987). Tests for Hurst effect. \textit{Biometrika}, 74(1), 95--101.'),
    'DI': ('10.1016/S0304-4076(01)00073-2', 'Diebold and Inoue (2001)', 'Diebold și Inoue (2001)',
           r'Diebold, F. X., \& Inoue, A. (2001). Long memory and regime switching. \textit{Journal of Econometrics}, 105(1), 131--159.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'DN': ('10.1137/S1064827592240555', 'Dietrich and Newsam (1997)', 'Dietrich și Newsam (1997)',
           r'Dietrich, C. R., \& Newsam, G. N. (1997). Fast and exact simulation of stationary Gaussian processes through circulant embedding of the covariance matrix. \textit{SIAM Journal on Scientific Computing}, 18(4), 1088--1107.'),
    'ER': ('10.1111/mafi.12173', 'El Euch and Rosenbaum (2019)', 'El Euch și Rosenbaum (2019)',
           r'El Euch, O., \& Rosenbaum, M. (2019). The characteristic function of rough Heston models. \textit{Mathematical Finance}, 29(1), 3--38.'),
    'FT': ('10.1214/aos/1176349936', 'Fox and Taqqu (1986)', 'Fox și Taqqu (1986)',
           r'Fox, R., \& Taqqu, M. S. (1986). Large-sample properties of parameter estimates for strongly dependent stationary Gaussian time series. \textit{The Annals of Statistics}, 14(2), 517--532.'),
    'FTW': ('10.1111/mafi.12354', 'Fukasawa, Takabatake and Westphal (2022)', 'Fukasawa, Takabatake și Westphal (2022)',
            r'Fukasawa, M., Takabatake, T., \& Westphal, R. (2022). Consistent estimation for fractional stochastic volatility model under high-frequency asymptotics. \textit{Mathematical Finance}, 32(4), 1086--1132.'),
    'GJR': ('10.1080/14697688.2017.1393551', 'Gatheral, Jaisson and Rosenbaum (2018)', 'Gatheral, Jaisson și Rosenbaum (2018)',
            r'Gatheral, J., Jaisson, T., \& Rosenbaum, M. (2018). Volatility is rough. \textit{Quantitative Finance}, 18(6), 933--949.'),
    'GPH': ('10.1111/j.1467-9892.1983.tb00371.x', 'Geweke and Porter-Hudak (1983)', 'Geweke și Porter-Hudak (1983)',
            r'Geweke, J., \& Porter-Hudak, S. (1983). The estimation and application of long memory time series models. \textit{Journal of Time Series Analysis}, 4(4), 221--238.'),
    'GS': ('10.1137/S0036144501394387', 'Gneiting and Schlather (2004)', 'Gneiting și Schlather (2004)',
           r'Gneiting, T., \& Schlather, M. (2004). Stochastic models that separate fractal dimension and the Hurst effect. \textit{SIAM Review}, 46(2), 269--282.'),
    'Gra': ('10.1016/0304-4076(80)90092-5', 'Granger (1980)', 'Granger (1980)',
            r'Granger, C. W. J. (1980). Long memory relationships and the aggregation of dynamic models. \textit{Journal of Econometrics}, 14(2), 227--238.'),
    'GH': ('10.1016/j.jempfin.2003.03.001', 'Granger and Hyung (2004)', 'Granger și Hyung (2004)',
           r'Granger, C. W. J., \& Hyung, N. (2004). Occasional structural breaks and long memory with an application to the S\&P 500 absolute stock returns. \textit{Journal of Empirical Finance}, 11(3), 399--421.'),
    'GJ': ('10.1111/j.1467-9892.1980.tb00297.x', 'Granger and Joyeux (1980)', 'Granger și Joyeux (1980)',
           r'Granger, C. W. J., \& Joyeux, R. (1980). An introduction to long-memory time series models and fractional differencing. \textit{Journal of Time Series Analysis}, 1(1), 15--29.'),
    'HW': ('10.1080/07350015.1995.10524577', 'Hassler and Wolters (1995)', 'Hassler și Wolters (1995)',
           r'Hassler, U., \& Wolters, J. (1995). Long memory in inflation rates: International evidence. \textit{Journal of Business \& Economic Statistics}, 13(1), 37--45.'),
    'OMI': (OMI_URL, 'Heber et al.\\ (2009)', 'Heber et al.\\ (2009)',
            r'Heber, G., Lunde, A., Shephard, N., \& Sheppard, K. K. (2009). Oxford-Man Institute\'s realized library, version 0.3. Oxford-Man Institute, University of Oxford.'),
    'HR': ('10.1007/978-1-4612-2412-9_16', 'Henry and Robinson (1996)', 'Henry și Robinson (1996)',
           r'Henry, M., \& Robinson, P. M. (1996). Bandwidth choice in Gaussian semiparametric estimation of long range dependence. In \textit{Athens Conference on Applied Probability and Time Series Analysis}, Lecture Notes in Statistics 115, 220--232. Springer.'),
    'Hos': ('10.1093/biomet/68.1.165', 'Hosking (1981)', 'Hosking (1981)',
            r'Hosking, J. R. M. (1981). Fractional differencing. \textit{Biometrika}, 68(1), 165--176.'),
    'Hur': ('10.1061/TACEAT.0006518', 'Hurst (1951)', 'Hurst (1951)',
            r'Hurst, H. E. (1951). Long-term storage capacity of reservoirs. \textit{Transactions of the American Society of Civil Engineers}, 116(1), 770--799.'),
    'HDB': ('10.1111/1467-9892.00075', 'Hurvich, Deo and Brodsky (1998)', 'Hurvich, Deo și Brodsky (1998)',
            r'Hurvich, C. M., Deo, R., \& Brodsky, J. (1998). The mean squared error of Geweke and Porter-Hudak\'s estimator of the memory parameter of a long-memory time series. \textit{Journal of Time Series Analysis}, 19(1), 19--46.'),
    'HMS': ('10.1111/j.1468-0262.2005.00616.x', 'Hurvich, Moulines and Soulier (2005)', 'Hurvich, Moulines și Soulier (2005)',
            r'Hurvich, C. M., Moulines, E., \& Soulier, P. (2005). Estimating long memory in volatility. \textit{Econometrica}, 73(4), 1283--1328.'),
    'JN': ('10.3982/ECTA9299', 'Johansen and Nielsen (2012)', 'Johansen și Nielsen (2012)',
           r'Johansen, S., \& Nielsen, M. Ø. (2012). Likelihood inference for a fractionally cointegrated vector autoregressive model. \textit{Econometrica}, 80(6), 2667--2732.'),
    'LMPR': ('10.1080/24725854.2018.1444297', 'Livieri et al.\\ (2018)', 'Livieri et al.\\ (2018)',
             r'Livieri, G., Mouti, S., Pallavicini, A., \& Rosenbaum, M. (2018). Rough volatility: Evidence from option prices. \textit{IISE Transactions}, 50(9), 767--776.'),
    'LP': ('10.1016/j.jempfin.2009.10.001', 'Lu and Perron (2010)', 'Lu și Perron (2010)',
           r'Lu, Y. K., \& Perron, P. (2010). Modeling and forecasting stock return volatility using a random level shift model. \textit{Journal of Empirical Finance}, 17(1), 138--156.'),
    'MN': ('10.1002/jae.2295', 'MacKinnon and Nielsen (2014)', 'MacKinnon și Nielsen (2014)',
           r'MacKinnon, J. G., \& Nielsen, M. Ø. (2014). Numerical distribution functions of fractional unit root and cointegration tests. \textit{Journal of Applied Econometrics}, 29(1), 161--171.'),
    'MVN': ('10.1137/1010093', 'Mandelbrot and Van Ness (1968)', 'Mandelbrot și Van Ness (1968)',
            r'Mandelbrot, B. B., \& Van Ness, J. W. (1968). Fractional Brownian motions, fractional noises and applications. \textit{SIAM Review}, 10(4), 422--437.'),
    'NS': ('10.1016/j.jeconom.2006.10.008', 'Nielsen and Shimotsu (2007)', 'Nielsen și Shimotsu (2007)',
           r'Nielsen, M. Ø., \& Shimotsu, K. (2007). Determining the cointegrating rank in nonstationary fractional systems by the exact local Whittle approach. \textit{Journal of Econometrics}, 141(2), 574--596.'),
    'Par': ('10.1086/296071', 'Parkinson (1980)', 'Parkinson (1980)',
            r'Parkinson, M. (1980). The extreme value method for estimating the variance of the rate of return. \textit{The Journal of Business}, 53(1), 61--65.'),
    'Pat': ('10.1016/j.jeconom.2010.03.034', 'Patton (2011)', 'Patton (2011)',
            r'Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. \textit{Journal of Econometrics}, 160(1), 246--256.'),
    'PQ': ('10.1198/jbes.2009.06171', 'Perron and Qu (2010)', 'Perron și Qu (2010)',
           r'Perron, P., \& Qu, Z. (2010). Long-memory and level shifts in the volatility of stock market return indices. \textit{Journal of Business \& Economic Statistics}, 28(2), 275--290.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'PS': ('10.1214/009053604000000139', 'Phillips and Shimotsu (2004)', 'Phillips și Shimotsu (2004)',
           r'Phillips, P. C. B., \& Shimotsu, K. (2004). Local Whittle estimation in nonstationary and unit root cases. \textit{The Annals of Statistics}, 32(2), 656--692.'),
    'Qu': ('10.1198/jbes.2010.09153', 'Qu (2011)', 'Qu (2011)',
           r'Qu, Z. (2011). A test against spurious long memory. \textit{Journal of Business \& Economic Statistics}, 29(3), 423--438.'),
    'RobA': ('10.1214/aos/1176325382', 'Robinson (1994)', 'Robinson (1994)',
             r'Robinson, P. M. (1994). Semiparametric analysis of long-memory time series. \textit{The Annals of Statistics}, 22(1), 515--539.'),
    'RobB': ('10.1214/aos/1176324636', 'Robinson (1995a)', 'Robinson (1995a)',
             r'Robinson, P. M. (1995a). Log-periodogram regression of time series with long range dependence. \textit{The Annals of Statistics}, 23(3), 1048--1072.'),
    'RobC': ('10.1214/aos/1176324317', 'Robinson (1995b)', 'Robinson (1995b)',
             r'Robinson, P. M. (1995b). Gaussian semiparametric estimation of long range dependence. \textit{The Annals of Statistics}, 23(5), 1630--1661.'),
    'SP': ('10.1214/009053605000000309', 'Shimotsu and Phillips (2005)', 'Shimotsu și Phillips (2005)',
           r'Shimotsu, K., \& Phillips, P. C. B. (2005). Exact local Whittle estimation of fractional integration. \textit{The Annals of Statistics}, 33(4), 1890--1933.'),
    'Shi': ('10.1017/S0266466609100075', 'Shimotsu (2010)', 'Shimotsu (2010)',
            r'Shimotsu, K. (2010). Exact local Whittle estimation of fractional integration with unknown mean and time trend. \textit{Econometric Theory}, 26(2), 501--540.'),
    'Vel': ('10.1111/1467-9892.00127', 'Velasco (1999)', 'Velasco (1999)',
            r'Velasco, C. (1999). Gaussian semiparametric estimation of non-stationary time series. \textit{Journal of Time Series Analysis}, 20(1), 87--127.'),
    'WXY': ('10.1016/j.jeconom.2021.08.001', 'Wang, Xiao and Yu (2023)', 'Wang, Xiao și Yu (2023)',
            r'Wang, X., Xiao, W., \& Yu, J. (2023). Modeling and forecasting realized volatility with the fractional Ornstein--Uhlenbeck process. \textit{Journal of Econometrics}, 232(2), 389--415.'),
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
