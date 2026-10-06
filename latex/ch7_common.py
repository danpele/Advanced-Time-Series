r"""
ch7_common.py -- shared helpers of the Chapter 7 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_07/ch7_numbers.json (generate_all_charts.py) and
sem7_results.json (seminar7.py); the clickable citations of Chapter 7 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_07')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_07'
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
    with open(os.path.join(QL, 'ch7_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem7_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'AB': ('10.1093/rfs/15.4.1137', 'Ang and Bekaert (2002)', 'Ang și Bekaert (2002)',
           r'Ang, A., \& Bekaert, G. (2002). International asset allocation with regime shifts. \textit{The Review of Financial Studies}, 15(4), 1137--1187.'),
    'AC': ('10.1080/07350015.1993.10509929', 'Albert and Chib (1993)', 'Albert și Chib (1993)',
           r'Albert, J. H., \& Chib, S. (1993). Bayes inference via Gibbs sampling of autoregressive time series subject to Markov mean and variance shifts. \textit{Journal of Business \& Economic Statistics}, 11(1), 1--15.'),
    'AT': ('10.1146/annurev-financial-110311-101808', 'Ang and Timmermann (2012)', 'Ang și Timmermann (2012)',
           r'Ang, A., \& Timmermann, A. (2012). Regime changes and financial markets. \textit{Annual Review of Financial Economics}, 4, 313--337.'),
    'BPR': ('10.1111/j.1368-423X.2009.00307.x', 'Bauwens, Preminger and Rombouts (2010)', 'Bauwens, Preminger și Rombouts (2010)',
            r'Bauwens, L., Preminger, A., \& Rombouts, J. V. K. (2010). Theory and inference for a Markov switching GARCH model. \textit{The Econometrics Journal}, 13(2), 218--244.'),
    'BPSW': ('10.1214/aoms/1177697196', 'Baum et al.\\ (1970)', 'Baum et al.\\ (1970)',
             r'Baum, L. E., Petrie, T., Soules, G., \& Weiss, N. (1970). A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains. \textit{The Annals of Mathematical Statistics}, 41(1), 164--171.'),
    'Boll': ('10.1016/0304-4076(86)90063-1', 'Bollerslev (1986)', 'Bollerslev (1986)',
             r'Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. \textit{Journal of Econometrics}, 31(3), 307--327.'),
    'CHP': ('10.3982/ECTA8609', 'Carrasco, Hu and Ploberger (2014)', 'Carrasco, Hu și Ploberger (2014)',
            r'Carrasco, M., Hu, L., \& Ploberger, W. (2014). Optimal test for Markov switching parameters. \textit{Econometrica}, 82(2), 765--784.'),
    'CHR': ('10.1080/01621459.2000.10474285', 'Celeux, Hurn and Robert (2000)', 'Celeux, Hurn și Robert (2000)',
            r'Celeux, G., Hurn, M., \& Robert, C. P. (2000). Computational and inferential difficulties with mixture posterior distributions. \textit{Journal of the American Statistical Association}, 95(451), 957--970.'),
    'ChibA': ('10.1080/01621459.1995.10476635', 'Chib (1995)', 'Chib (1995)',
              r'Chib, S. (1995). Marginal likelihood from the Gibbs output. \textit{Journal of the American Statistical Association}, 90(432), 1313--1321.'),
    'ChibB': ('10.1016/0304-4076(95)01770-4', 'Chib (1996)', 'Chib (1996)',
              r'Chib, S. (1996). Calculating posterior distributions and modal estimates in Markov mixture models. \textit{Journal of Econometrics}, 75(1), 79--97.'),
    'ChibC': ('10.1016/S0304-4076(97)00115-2', 'Chib (1998)', 'Chib (1998)',
              r'Chib, S. (1998). Estimation and comparison of multiple change-point models. \textit{Journal of Econometrics}, 86(2), 221--241.'),
    'CK': ('10.1093/biomet/81.3.541', 'Carter and Kohn (1994)', 'Carter și Kohn (1994)',
           r'Carter, C. K., \& Kohn, R. (1994). On Gibbs sampling for state space models. \textit{Biometrika}, 81(3), 541--553.'),
    'CKr': ('10.1111/1368-423X.11004', 'Clements and Krolzig (1998)', 'Clements și Krolzig (1998)',
            r'Clements, M. P., \& Krolzig, H.-M. (1998). A comparison of the forecast performance of Markov-switching and threshold autoregressive models of US GNP. \textit{The Econometrics Journal}, 1(1), C47--C75.'),
    'CP': ('10.1198/073500107000000296', 'Chauvet and Piger (2008)', 'Chauvet și Piger (2008)',
           r'Chauvet, M., \& Piger, J. (2008). A comparison of the real-time performance of business cycle dating methods. \textit{Journal of Business \& Economic Statistics}, 26(1), 42--49.'),
    'CW': ('10.1111/j.1468-0262.2007.00809.x', 'Cho and White (2007)', 'Cho și White (2007)',
           r'Cho, J. S., \& White, H. (2007). Testing for regime switching. \textit{Econometrica}, 75(6), 1671--1720.'),
    'Dav': ('10.1093/biomet/74.1.33', 'Davies (1987)', 'Davies (1987)',
            r'Davies, R. B. (1987). Hypothesis testing when a nuisance parameter is present only under the alternative. \textit{Biometrika}, 74(1), 33--43.'),
    'DI': ('10.1016/S0304-4076(01)00073-2', 'Diebold and Inoue (2001)', 'Diebold și Inoue (2001)',
           r'Diebold, F. X., \& Inoue, A. (2001). Long memory and regime switching. \textit{Journal of Econometrics}, 105(1), 131--159.'),
    'DLR': ('10.1111/j.2517-6161.1977.tb01600.x', 'Dempster, Laird and Rubin (1977)', 'Dempster, Laird și Rubin (1977)',
            r'Dempster, A. P., Laird, N. M., \& Rubin, D. B. (1977). Maximum likelihood from incomplete data via the EM algorithm. \textit{Journal of the Royal Statistical Society: Series B}, 39(1), 1--22.'),
    'DLW': ('10.1093/oso/9780198773917.003.0010', 'Diebold, Lee and Weinbach (1994)', 'Diebold, Lee și Weinbach (1994)',
            r'Diebold, F. X., Lee, J.-H., \& Weinbach, G. C. (1994). Regime switching with time-varying transition probabilities. In C. P. Hargreaves (Ed.), \textit{Nonstationary Time Series Analysis and Cointegration} (pp.\ 283--302). Oxford University Press.'),
    'DR': ('10.1086/296467', 'Diebold and Rudebusch (1989)', 'Diebold și Rudebusch (1989)',
           r'Diebold, F. X., \& Rudebusch, G. D. (1989). Scoring the leading indicators. \textit{The Journal of Business}, 62(3), 369--391.'),
    'EEV': ('10.1016/S0165-1765(02)00256-2', 'Ehrmann, Ellison and Valla (2003)', 'Ehrmann, Ellison și Valla (2003)',
            r'Ehrmann, M., Ellison, M., \& Valla, N. (2003). Regime-dependent impulse response functions in a Markov-switching vector autoregression model. \textit{Economics Letters}, 78(3), 295--299.'),
    'Fil': ('10.1080/07350015.1994.10524545', 'Filardo (1994)', 'Filardo (1994)',
            r'Filardo, A. J. (1994). Business-cycle phases and their transitional dynamics. \textit{Journal of Business \& Economic Statistics}, 12(3), 299--308.'),
    'FSa': ('10.1198/016214501750333063', 'Frühwirth-Schnatter (2001)', 'Frühwirth-Schnatter (2001)',
            r'Frühwirth-Schnatter, S. (2001). Markov chain Monte Carlo estimation of classical and dynamic switching and mixture models. \textit{Journal of the American Statistical Association}, 96(453), 194--209.'),
    'FSb': ('10.1007/978-0-387-35768-3', 'Frühwirth-Schnatter (2006)', 'Frühwirth-Schnatter (2006)',
            r'Frühwirth-Schnatter, S. (2006). \textit{Finite Mixture and Markov Switching Models}. Springer.'),
    'Gar': ('10.2307/2527399', 'Garcia (1998)', 'Garcia (1998)',
            r'Garcia, R. (1998). Asymptotic null distribution of the likelihood ratio test in Markov switching models. \textit{International Economic Review}, 39(3), 763--788.'),
    'GP': ('10.2307/2109851', 'Garcia and Perron (1996)', 'Garcia și Perron (1996)',
           r'Garcia, R., \& Perron, P. (1996). An analysis of the real interest rate under regime shifts. \textit{The Review of Economics and Statistics}, 78(1), 111--125.'),
    'GQ': ('10.1016/0304-4076(73)90002-X', 'Goldfeld and Quandt (1973)', 'Goldfeld și Quandt (1973)',
           r'Goldfeld, S. M., \& Quandt, R. E. (1973). A Markov model for switching regressions. \textit{Journal of Econometrics}, 1(1), 3--15.'),
    'Gray': ('10.1016/0304-405X(96)00875-6', 'Gray (1996)', 'Gray (1996)',
             r'Gray, S. F. (1996). Modeling the conditional distribution of interest rates as a regime-switching process. \textit{Journal of Financial Economics}, 42(1), 27--62.'),
    'HamA': ('10.2307/1912559', 'Hamilton (1989)', 'Hamilton (1989)',
             r'Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. \textit{Econometrica}, 57(2), 357--384.'),
    'HamB': ('10.1016/0304-4076(90)90093-9', 'Hamilton (1990)', 'Hamilton (1990)',
             r'Hamilton, J. D. (1990). Analysis of time series subject to changes in regime. \textit{Journal of Econometrics}, 45(1--2), 39--70.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'HamC': ('10.1016/bs.hesmac.2016.03.004', 'Hamilton (2016)', 'Hamilton (2016)',
             r'Hamilton, J. D. (2016). Macroeconomic regimes and regime shifts. In J. B. Taylor \& H. Uhlig (Eds.), \textit{Handbook of Macroeconomics} (Vol.\ 2A, pp.\ 163--201). Elsevier.'),
    'Han': ('10.1002/jae.3950070506', 'Hansen (1992)', 'Hansen (1992)',
            r'Hansen, B. E. (1992). The likelihood ratio test under nonstandard conditions: Testing the Markov switching model of GNP. \textit{Journal of Applied Econometrics}, 7(S1), S61--S82.'),
    'Hath': ('10.1214/aos/1176349557', 'Hathaway (1985)', 'Hathaway (1985)',
             r'Hathaway, R. J. (1985). A constrained formulation of maximum-likelihood estimation for normal mixture distributions. \textit{The Annals of Statistics}, 13(2), 795--800.'),
    'HMP': ('10.1093/jjfinec/nbh020', 'Haas, Mittnik and Paolella (2004)', 'Haas, Mittnik și Paolella (2004)',
            r'Haas, M., Mittnik, S., \& Paolella, M. S. (2004). A new approach to Markov-switching GARCH models. \textit{Journal of Financial Econometrics}, 2(4), 493--530.'),
    'HP': ('10.1016/S0304-3932(01)00108-8', 'Harding and Pagan (2002)', 'Harding și Pagan (2002)',
           r'Harding, D., \& Pagan, A. (2002). Dissecting the cycle: A methodological investigation. \textit{Journal of Monetary Economics}, 49(2), 365--381.'),
    'HS': ('10.1016/0304-4076(94)90067-1', 'Hamilton and Susmel (1994)', 'Hamilton și Susmel (1994)',
           r'Hamilton, J. D., \& Susmel, R. (1994). Autoregressive conditional heteroskedasticity and changes in regime. \textit{Journal of Econometrics}, 64(1--2), 307--333.'),
    'Kim': ('10.1016/0304-4076(94)90036-1', 'Kim (1994)', 'Kim (1994)',
            r'Kim, C.-J. (1994). Dynamic linear models with Markov-switching. \textit{Journal of Econometrics}, 60(1--2), 1--22.'),
    'KN': ('10.7551/mitpress/6444.001.0001', 'Kim and Nelson (1999)', 'Kim și Nelson (1999)',
           r'Kim, C.-J., \& Nelson, C. R. (1999). \textit{State-Space Models with Regime Switching: Classical and Gibbs-Sampling Approaches with Applications}. MIT Press.'),
    'Kla': ('10.1007/s001810100100', 'Klaassen (2002)', 'Klaassen (2002)',
            r'Klaassen, F. (2002). Improving GARCH volatility forecasts with regime-switching GARCH. \textit{Empirical Economics}, 27(2), 363--394.'),
    'Kro': ('10.1007/978-3-642-51684-9', 'Krolzig (1997)', 'Krolzig (1997)',
            r'Krolzig, H.-M. (1997). \textit{Markov-Switching Vector Autoregressions: Modelling, Statistical Inference, and Application to Business Cycle Analysis}. Springer.'),
    'LL': ('10.1080/07350015.1990.10509794', 'Lamoureux and Lastrapes (1990)', 'Lamoureux și Lastrapes (1990)',
           r'Lamoureux, C. G., \& Lastrapes, W. D. (1990). Persistence in variance, structural change, and the GARCH model. \textit{Journal of Business \& Economic Statistics}, 8(2), 225--234.'),
    'MM': ('10.1080/07350015.2000.10524851', 'Maheu and McCurdy (2000)', 'Maheu și McCurdy (2000)',
           r'Maheu, J. M., \& McCurdy, T. H. (2000). Identifying bull and bear markets in stock returns. \textit{Journal of Business \& Economic Statistics}, 18(1), 100--112.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'Rab': ('10.1109/5.18626', 'Rabiner (1989)', 'Rabiner (1989)',
            r'Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. \textit{Proceedings of the IEEE}, 77(2), 257--286.'),
    'Ste': ('10.1111/1467-9868.00265', 'Stephens (2000)', 'Stephens (2000)',
            r'Stephens, M. (2000). Dealing with label switching in mixture models. \textit{Journal of the Royal Statistical Society: Series B}, 62(4), 795--809.'),
    'SZ': ('10.1257/000282806776157678', 'Sims and Zha (2006)', 'Sims și Zha (2006)',
           r'Sims, C. A., \& Zha, T. (2006). Were there regime switches in U.S. monetary policy? \textit{American Economic Review}, 96(1), 54--81.'),
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
