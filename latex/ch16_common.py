r"""
ch16_common.py -- shared helpers of the Chapter 16 generator (lecture, self-study), ATS
=====================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_16/ch16_numbers.json (generate_all_charts.py); the clickable
citations of Chapter 16 (DOIs checked against Crossref, other links with HTTP 200 and the title on the page;
6 October 2026). Corbet, Lucey and Yarovaya (2018) on Bitcoin bubbles is retracted and is not cited.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_16')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_16'
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


def minus_fix(V):
    """Negative numbers: a real minus sign in text and in math mode."""
    for k, v in list(V.items()):
        if isinstance(v, str) and v.startswith('⁅-'):
            V[k] = '⁅\\ensuremath{-}' + v[2:]


def load():
    with open(os.path.join(QL, 'ch16_numbers.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    # ---------------------------------------------------------------- rational bubbles
    'BW': ('10.3386/w0945', 'Blanchard and Watson (1982)', 'Blanchard și Watson (1982)',
           r'Blanchard, O. J., \& Watson, M. W. (1982). Bubbles, rational expectations and financial markets. NBER Working Paper 945.'),
    'DGa': ('10.2307/2233912', 'Diba and Grossman (1988a)', 'Diba și Grossman (1988a)',
            r'Diba, B. T., \& Grossman, H. I. (1988a). The theory of rational bubbles in stock prices. \textit{The Economic Journal}, 98(392), 746--754.'),
    'DGb': ('https://ideas.repec.org/a/aea/aecrev/v78y1988i3p520-30.html', 'Diba and Grossman (1988b)', 'Diba și Grossman (1988b)',
            r'Diba, B. T., \& Grossman, H. I. (1988b). Explosive rational bubbles in stock prices? \textit{American Economic Review}, 78(3), 520--530.'),
    'Ev': ('https://ideas.repec.org/a/aea/aecrev/v81y1991i4p922-30.html', 'Evans (1991)', 'Evans (1991)',
           r'Evans, G. W. (1991). Pitfalls in testing for explosive bubbles in asset prices. \textit{American Economic Review}, 81(4), 922--930.'),
    'CS': ('10.1086/261502', 'Campbell and Shiller (1987)', 'Campbell și Shiller (1987)',
           r'Campbell, J. Y., \& Shiller, R. J. (1987). Cointegration and tests of present value models. \textit{Journal of Political Economy}, 95(5), 1062--1088.'),
    'Tir': ('10.2307/1913232', 'Tirole (1985)', 'Tirole (1985)',
            r'Tirole, J. (1985). Asset bubbles and overlapping generations. \textit{Econometrica}, 53(6), 1499--1528.'),
    'SW': ('10.2307/2171812', 'Santos and Woodford (1997)', 'Santos și Woodford (1997)',
           r'Santos, M. S., \& Woodford, M. (1997). Rational asset pricing bubbles. \textit{Econometrica}, 65(1), 19--57.'),
    'Gur': ('10.1111/j.1467-6419.2007.00530.x', 'Gürkaynak (2008)', 'Gürkaynak (2008)',
            r'Gürkaynak, R. S. (2008). Econometric tests of asset price bubbles: Taking stock. \textit{Journal of Economic Surveys}, 22(1), 166--186.'),
    'GSY': ('10.1016/j.jfineco.2018.09.002', 'Greenwood, Shleifer and You (2019)', 'Greenwood, Shleifer și You (2019)',
            r'Greenwood, R., Shleifer, A., \& You, Y. (2019). Bubbles for Fama. \textit{Journal of Financial Economics}, 131(1), 20--43.'),
    'Shi': ('10.1515/9781400865536', 'Shiller (2015)', 'Shiller (2015)',
            r'Shiller, R. J. (2015). \textit{Irrational Exuberance} (3rd ed.). Princeton University Press.'),
    'KA': ('10.1057/9780230628045', 'Kindleberger and Aliber (2005)', 'Kindleberger și Aliber (2005)',
           r'Kindleberger, C. P., \& Aliber, R. Z. (2005). \textit{Manias, Panics and Crashes: A History of Financial Crises} (5th ed.). Palgrave Macmillan.'),
    # ---------------------------------------------------------------- explosive asymptotics and tests
    'Whi': ('10.1214/aoms/1177706450', 'White (1958)', 'White (1958)',
            r'White, J. S. (1958). The limiting distribution of the serial correlation coefficient in the explosive case. \textit{The Annals of Mathematical Statistics}, 29(4), 1188--1197.'),
    'And': ('10.1214/aoms/1177706198', 'Anderson (1959)', 'Anderson (1959)',
            r'Anderson, T. W. (1959). On asymptotic distributions of estimates of parameters of stochastic difference equations. \textit{The Annals of Mathematical Statistics}, 30(3), 676--687.'),
    'PM': ('10.1016/j.jeconom.2005.08.002', 'Phillips and Magdalinos (2007)', 'Phillips și Magdalinos (2007)',
           r'Phillips, P. C. B., \& Magdalinos, T. (2007). Limit theory for moderate deviations from a unit root. \textit{Journal of Econometrics}, 136(1), 115--130.'),
    'DF': ('10.1080/01621459.1979.10482531', 'Dickey and Fuller (1979)', 'Dickey și Fuller (1979)',
           r'Dickey, D. A., \& Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. \textit{Journal of the American Statistical Association}, 74(366), 427--431.'),
    'PWY': ('10.1111/j.1468-2354.2010.00625.x', 'Phillips, Wu and Yu (2011)', 'Phillips, Wu și Yu (2011)',
            r'Phillips, P. C. B., Wu, Y., \& Yu, J. (2011). Explosive behavior in the 1990s Nasdaq: When did exuberance escalate asset values? \textit{International Economic Review}, 52(1), 201--226.'),
    'PSYa': ('10.1111/iere.12132', 'Phillips, Shi and Yu (2015a)', 'Phillips, Shi și Yu (2015a)',
             r'Phillips, P. C. B., Shi, S., \& Yu, J. (2015a). Testing for multiple bubbles: Historical episodes of exuberance and collapse in the S\&P 500. \textit{International Economic Review}, 56(4), 1043--1078.'),
    'PSYb': ('10.1111/iere.12131', 'Phillips, Shi and Yu (2015b)', 'Phillips, Shi și Yu (2015b)',
             r'Phillips, P. C. B., Shi, S., \& Yu, J. (2015b). Testing for multiple bubbles: Limit theory of real-time detectors. \textit{International Economic Review}, 56(4), 1079--1134.'),
    'PSYs': ('10.1111/obes.12026', 'Phillips, Shi and Yu (2014)', 'Phillips, Shi și Yu (2014)',
             r'Phillips, P. C. B., Shi, S., \& Yu, J. (2014). Specification sensitivity in right-tailed unit root testing for explosive behaviour. \textit{Oxford Bulletin of Economics and Statistics}, 76(3), 315--333.'),
    'PS': ('10.1016/bs.host.2018.12.002', 'Phillips and Shi (2020)', 'Phillips și Shi (2020)',
           r'Phillips, P. C. B., \& Shi, S. (2020). Real time monitoring of asset markets: Bubbles and crises. In \textit{Handbook of Statistics}, Vol.\ 42, 61--80. Elsevier.'),
    'PSi': ('10.1017/S0266466617000202', 'Phillips and Shi (2018)', 'Phillips și Shi (2018)',
            r'Phillips, P. C. B., \& Shi, S. (2018). Financial bubble implosion and reverse regression. \textit{Econometric Theory}, 34(4), 705--753.'),
    'PY': ('10.3982/QE82', 'Phillips and Yu (2011)', 'Phillips și Yu (2011)',
           r'Phillips, P. C. B., \& Yu, J. (2011). Dating the timeline of financial bubbles during the subprime crisis. \textit{Quantitative Economics}, 2(3), 455--491.'),
    'HB': ('10.1093/jjfinec/nbr009', 'Homm and Breitung (2012)', 'Homm și Breitung (2012)',
           r'Homm, U., \& Breitung, J. (2012). Testing for speculative bubbles in stock markets: A comparison of alternative methods. \textit{Journal of Financial Econometrics}, 10(1), 198--231.'),
    'CSW': ('10.2307/2171955', 'Chu, Stinchcombe and White (1996)', 'Chu, Stinchcombe și White (1996)',
            r'Chu, C.-S. J., Stinchcombe, M., \& White, H. (1996). Monitoring structural change. \textit{Econometrica}, 64(5), 1045--1065.'),
    'HLST': ('10.1016/j.jempfin.2015.09.002', 'Harvey et al.\\ (2016)', 'Harvey et al.\\ (2016)',
             r'Harvey, D. I., Leybourne, S. J., Sollis, R., \& Taylor, A. M. R. (2016). Tests for explosive financial bubbles in the presence of non-stationary volatility. \textit{Journal of Empirical Finance}, 38, 548--574.'),
    'HLS': ('10.1016/j.jempfin.2016.11.001', 'Harvey, Leybourne and Sollis (2017)', 'Harvey, Leybourne și Sollis (2017)',
            r'Harvey, D. I., Leybourne, S. J., \& Sollis, R. (2017). Improving the accuracy of asset price bubble start and end date estimators. \textit{Journal of Empirical Finance}, 40, 121--138.'),
    'HLZ': ('10.1017/S0266466619000057', 'Harvey, Leybourne and Zu (2020)', 'Harvey, Leybourne și Zu (2020)',
            r'Harvey, D. I., Leybourne, S. J., \& Zu, Y. (2020). Sign-based unit root tests for explosive financial bubbles in the presence of deterministically time-varying volatility. \textit{Econometric Theory}, 36(1), 122--169.'),
    'AHLT': ('10.1080/07474938.2017.1307490', 'Astill et al.\\ (2017)', 'Astill et al.\\ (2017)',
             r'Astill, S., Harvey, D. I., Leybourne, S. J., \& Taylor, A. M. R. (2017). Tests for an end-of-sample bubble in financial time series. \textit{Econometric Reviews}, 36(6--9), 651--666.'),
    'AHLST': ('10.1111/jtsa.12409', 'Astill et al.\\ (2018)', 'Astill et al.\\ (2018)',
              r'Astill, S., Harvey, D. I., Leybourne, S. J., Sollis, R., \& Taylor, A. M. R. (2018). Real-time monitoring for explosive financial bubbles. \textit{Journal of Time Series Analysis}, 39(6), 863--891.'),
    'VPM': ('10.18637/jss.v103.i10', 'Vasilopoulos, Pavlidis and Martínez-García (2022)', 'Vasilopoulos, Pavlidis și Martínez-García (2022)',
            r'Vasilopoulos, K., Pavlidis, E., \& Martínez-García, E. (2022). exuber: Recursive right-tailed unit root testing with R. \textit{Journal of Statistical Software}, 103(10).'),
    'Pav': ('10.1007/s11146-015-9531-2', 'Pavlidis et al.\\ (2016)', 'Pavlidis et al.\\ (2016)',
            r'Pavlidis, E., Yusupova, A., Paya, I., Peel, D., Martínez-García, E., Mack, A., \& Grossman, V. (2016). Episodes of exuberance in housing markets: In search of the smoking gun. \textit{The Journal of Real Estate Finance and Economics}, 53(4), 419--449.'),
    'KLR': ('10.2307/3867328', 'Kaminsky, Lizondo and Reinhart (1998)', 'Kaminsky, Lizondo și Reinhart (1998)',
            r'Kaminsky, G., Lizondo, S., \& Reinhart, C. M. (1998). Leading indicators of currency crises. \textit{IMF Staff Papers}, 45(1), 1--48.'),
    # ---------------------------------------------------------------- LPPLS
    'JLS': ('10.1142/S0219024900000115', 'Johansen, Ledoit and Sornette (2000)', 'Johansen, Ledoit și Sornette (2000)',
            r'Johansen, A., Ledoit, O., \& Sornette, D. (2000). Crashes as critical points. \textit{International Journal of Theoretical and Applied Finance}, 3(2), 219--255.'),
    'FS': ('10.1016/j.physa.2013.04.012', 'Filimonov and Sornette (2013)', 'Filimonov și Sornette (2013)',
           r'Filimonov, V., \& Sornette, D. (2013). A stable and robust calibration scheme of the log-periodic power law model. \textit{Physica A}, 392(17), 3698--3707.'),
    'FDS': ('10.1080/14697688.2016.1276298', 'Filimonov, Demos and Sornette (2017)', 'Filimonov, Demos și Sornette (2017)',
            r'Filimonov, V., Demos, G., \& Sornette, D. (2017). Modified profile likelihood inference and interval forecast of the burst of financial bubbles. \textit{Quantitative Finance}, 17(8), 1167--1186.'),
    'DS': ('10.1080/14697688.2016.1231417', 'Demos and Sornette (2017)', 'Demos și Sornette (2017)',
           r'Demos, G., \& Sornette, D. (2017). Birth or burst of financial bubbles: Which one is easier to diagnose? \textit{Quantitative Finance}, 17(5), 657--675.'),
    'Sha': ('10.21314/JOIS.2015.063', 'Sornette et al.\\ (2015)', 'Sornette et al.\\ (2015)',
            r'Sornette, D., Demos, G., Zhang, Q., Cauwels, P., \& Zhang, Q. (2015). Real-time prediction and post-mortem analysis of the Shanghai 2015 stock market bubble and crash. \textit{Journal of Investment Strategies}, 4(4), 77--95.'),
    'SZ': ('10.1016/j.physa.2020.124892', 'Shu and Zhu (2020)', 'Shu și Zhu (2020)',
           r'Shu, M., \& Zhu, W. (2020). Detection of Chinese stock market bubbles with LPPLS confidence indicator. \textit{Physica A}, 557, 124892.'),
    'SWYZ': ('10.1016/j.physa.2013.05.011', 'Sornette et al.\\ (2013)', 'Sornette et al.\\ (2013)',
             r'Sornette, D., Woodard, R., Yan, W., \& Zhou, W.-X. (2013). Clarifications to questions and criticisms on the Johansen--Ledoit--Sornette financial bubble model. \textit{Physica A}, 392(19), 4417--4428.'),
    'ZS': ('10.1142/S0129183103005212', 'Zhou and Sornette (2003)', 'Zhou și Sornette (2003)',
           r'Zhou, W.-X., \& Sornette, D. (2003). Nonparametric analyses of log-periodic precursors to financial crashes. \textit{International Journal of Modern Physics C}, 14(8), 1107--1125.'),
    'Lom': ('10.1007/BF00648343', 'Lomb (1976)', 'Lomb (1976)',
            r'Lomb, N. R. (1976). Least-squares frequency analysis of unequally spaced data. \textit{Astrophysics and Space Science}, 39(2), 447--462.'),
    'Fei': ('10.1088/1469-7688/1/3/306', 'Feigenbaum (2001)', 'Feigenbaum (2001)',
            r'Feigenbaum, J. A. (2001). A statistical analysis of log-periodic precursors to financial crashes. \textit{Quantitative Finance}, 1(3), 346--360.'),
    'BJ': ('10.1016/j.irfa.2013.05.005', 'Brée and Joseph (2013)', 'Brée și Joseph (2013)',
           r'Brée, D. S., \& Joseph, N. L. (2013). Testing for financial crashes using the log periodic power law model. \textit{International Review of Financial Analysis}, 30, 287--297.'),
    'GF': ('10.1080/1351847X.2011.601657', 'Geraskin and Fantazzini (2013)', 'Geraskin și Fantazzini (2013)',
           r'Geraskin, P., \& Fantazzini, D. (2013). Everything you always wanted to know about log-periodic power laws for bubble modeling but were afraid to ask. \textit{The European Journal of Finance}, 19(5), 366--391.'),
    'GDS': ('10.1098/rsos.180643', 'Gerlach, Demos and Sornette (2019)', 'Gerlach, Demos și Sornette (2019)',
            r'Gerlach, J.-C., Demos, G., \& Sornette, D. (2019). Dissection of Bitcoin\textquoteright s multiscale bubble history from January 2012 to February 2018. \textit{Royal Society Open Science}, 6(7), 180643.'),
    'Ham': ('10.1515/9780691218632', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    # ---------------------------------------------------------------- further reading (instructor)
    'PMM': ('10.1016/j.sbspro.2012.09.1030', 'Pele and Mazurencu-Marinescu (2012)', 'Pele și Mazurencu-Marinescu (2012)',
            r'Pele, D. T., \& Mazurencu-Marinescu, M. (2012). Modelling stock market crashes: The case of Bucharest Stock Exchange. \textit{Procedia -- Social and Behavioral Sciences}, 58, 533--542 (further reading).'),
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
        shown = 'doi:' + v[0] if not v[0].startswith('http') else v[0].split('/')[2].replace('www.', '')
        shown = shown.replace('_', '\\_')
        out.append(v[3] + f' \\href{{{u}}}{{{shown}}}')
    return out
