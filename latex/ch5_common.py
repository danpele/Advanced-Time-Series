r"""
ch5_common.py -- shared helpers of the Chapter 5 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_05/ch5_numbers.json (generate_all_charts.py) and
sem5_results.json (seminar5.py); the clickable citations of Chapter 5 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_05')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_05'
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
    with open(os.path.join(QL, 'ch5_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem5_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'ADS': ('10.1198/jbes.2009.07205', 'Aruoba, Diebold and Scotti (2009)', 'Aruoba, Diebold și Scotti (2009)',
            r'Aruoba, S. B., Diebold, F. X., \& Scotti, C. (2009). Real-time measurement of business conditions. \textit{Journal of Business \& Economic Statistics}, 27(4), 417--427.'),
    'AGK': ('10.1080/07350015.2013.767199', 'Andreou, Ghysels and Kourtellos (2013)', 'Andreou, Ghysels și Kourtellos (2013)',
            r'Andreou, E., Ghysels, E., \& Kourtellos, A. (2013). Should macroeconomic forecasters use daily financial data and how? \textit{Journal of Business \& Economic Statistics}, 31(2), 240--251.'),
    'BBE': ('10.1162/0033553053327452', 'Bernanke, Boivin and Eliasz (2005)', 'Bernanke, Boivin și Eliasz (2005)',
            r'Bernanke, B. S., Boivin, J., \& Eliasz, P. (2005). Measuring the effects of monetary policy: A factor-augmented vector autoregressive (FAVAR) approach. \textit{The Quarterly Journal of Economics}, 120(1), 387--422.'),
    'BGMR': ('10.1016/B978-0-444-53683-9.00004-9', 'Bańbura, Giannone, Modugno and Reichlin (2013)', 'Bańbura, Giannone, Modugno și Reichlin (2013)',
             r'Bańbura, M., Giannone, D., Modugno, M., \& Reichlin, L. (2013). Now-casting and the real-time data flow. In G. Elliott \& A. Timmermann (Eds.), \textit{Handbook of Economic Forecasting} (Vol.\ 2A, pp.\ 195--237). Elsevier.'),
    'BGP': ('10.1016/S0169-2070(03)00067-0', 'Baffigi, Golinelli and Parigi (2004)', 'Baffigi, Golinelli și Parigi (2004)',
            r'Baffigi, A., Golinelli, R., \& Parigi, G. (2004). Bridge models to forecast the euro area GDP. \textit{International Journal of Forecasting}, 20(3), 447--460.'),
    'BGR': ('10.1002/jae.1137', 'Bańbura, Giannone and Reichlin (2010)', 'Bańbura, Giannone și Reichlin (2010)',
            r'Bańbura, M., Giannone, D., \& Reichlin, L. (2010). Large Bayesian vector auto regressions. \textit{Journal of Applied Econometrics}, 25(1), 71--92.'),
    'BM': ('10.1002/jae.2306', 'Bańbura and Modugno (2014)', 'Bańbura și Modugno (2014)',
           r'Bańbura, M., \& Modugno, M. (2014). Maximum likelihood estimation of factor models on datasets with arbitrary pattern of missing data. \textit{Journal of Applied Econometrics}, 29(1), 133--160.'),
    'BN': ('10.1111/1468-0262.00273', 'Bai and Ng (2002)', 'Bai și Ng (2002)',
           r'Bai, J., \& Ng, S. (2002). Determining the number of factors in approximate factor models. \textit{Econometrica}, 70(1), 191--221.'),
    'Bai': ('10.1111/1468-0262.00392', 'Bai (2003)', 'Bai (2003)',
            r'Bai, J. (2003). Inferential theory for factor models of large dimensions. \textit{Econometrica}, 71(1), 135--171.'),
    'BDA': ('10.1201/b16018', 'Gelman et al.\\ (2013)', 'Gelman et al.\\ (2013)',
            r'Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., \& Rubin, D. B. (2013). \textit{Bayesian Data Analysis} (3rd ed.). Chapman and Hall/CRC.'),
    'CCMa': ('10.1080/07350015.2015.1040116', 'Carriero, Clark and Marcellino (2016)', 'Carriero, Clark și Marcellino (2016)',
             r'Carriero, A., Clark, T. E., \& Marcellino, M. (2016). Common drifting volatility in large Bayesian VARs. \textit{Journal of Business \& Economic Statistics}, 34(3), 375--390.'),
    'CCMb': ('10.1016/j.jeconom.2019.04.024', 'Carriero, Clark and Marcellino (2019)', 'Carriero, Clark și Marcellino (2019)',
             r'Carriero, A., Clark, T. E., \& Marcellino, M. (2019). Large Bayesian vector autoregressions with stochastic volatility and non-conjugate priors. \textit{Journal of Econometrics}, 212(1), 137--154.'),
    'CG': ('10.1198/073500108000000015', 'Clements and Galvão (2008)', 'Clements și Galvão (2008)',
           r'Clements, M. P., \& Galvão, A. B. (2008). Macroeconomic forecasting with mixed-frequency data: Forecasting output growth in the United States. \textit{Journal of Business \& Economic Statistics}, 26(4), 546--554.'),
    'Chan': ('10.1007/978-3-030-31150-6_4', 'Chan (2020)', 'Chan (2020)',
             r'Chan, J. C. C. (2020). Large Bayesian vector autoregressions. In P. Fuleky (Ed.), \textit{Macroeconomic Forecasting in the Era of Big Data} (pp.\ 95--125). Springer.'),
    'Clark': ('10.1198/jbes.2010.09248', 'Clark (2011)', 'Clark (2011)',
              r'Clark, T. E. (2011). Real-time density forecasts from Bayesian vector autoregressions with stochastic volatility. \textit{Journal of Business \& Economic Statistics}, 29(3), 327--341.'),
    'CR': ('10.2307/1912275', 'Chamberlain and Rothschild (1983)', 'Chamberlain și Rothschild (1983)',
           r'Chamberlain, G., \& Rothschild, M. (1983). Arbitrage, factor structure, and mean-variance analysis on large asset markets. \textit{Econometrica}, 51(5), 1281--1304.'),
    'CS': ('10.1016/S0304-4076(01)00072-0', 'Croushore and Stark (2001)', 'Croushore și Stark (2001)',
           r'Croushore, D., \& Stark, T. (2001). A real-time data set for macroeconomists. \textit{Journal of Econometrics}, 105(1), 111--130.'),
    'DGRa': ('10.1016/j.jeconom.2008.08.011', 'De Mol, Giannone and Reichlin (2008)', 'De Mol, Giannone și Reichlin (2008)',
             r'De Mol, C., Giannone, D., \& Reichlin, L. (2008). Forecasting using a large number of predictors: Is Bayesian shrinkage a valid alternative to principal components? \textit{Journal of Econometrics}, 146(2), 318--328.'),
    'DGRb': ('10.1016/j.jeconom.2011.02.012', 'Doz, Giannone and Reichlin (2011)', 'Doz, Giannone și Reichlin (2011)',
             r'Doz, C., Giannone, D., \& Reichlin, L. (2011). A two-step estimator for large approximate dynamic factor models based on Kalman filtering. \textit{Journal of Econometrics}, 164(1), 188--205.'),
    'DGRc': ('10.1162/REST_a_00225', 'Doz, Giannone and Reichlin (2012)', 'Doz, Giannone și Reichlin (2012)',
             r'Doz, C., Giannone, D., \& Reichlin, L. (2012). A quasi-maximum likelihood approach for large, approximate dynamic factor models. \textit{The Review of Economics and Statistics}, 94(4), 1014--1024.'),
    'DK': ('10.1093/acprof:oso/9780199641178.001.0001', 'Durbin and Koopman (2012)', 'Durbin și Koopman (2012)',
           r'Durbin, J., \& Koopman, S. J. (2012). \textit{Time Series Analysis by State Space Methods} (2nd ed.). Oxford University Press.'),
    'DLS': ('10.1080/07474938408800053', 'Doan, Litterman and Sims (1984)', 'Doan, Litterman și Sims (1984)',
            r'Doan, T., Litterman, R., \& Sims, C. (1984). Forecasting and conditional projection using realistic prior distributions. \textit{Econometric Reviews}, 3(1), 1--100.'),
    'FHLR': ('10.1162/003465300559037', 'Forni, Hallin, Lippi and Reichlin (2000)', 'Forni, Hallin, Lippi și Reichlin (2000)',
             r'Forni, M., Hallin, M., Lippi, M., \& Reichlin, L. (2000). The generalized dynamic-factor model: Identification and estimation. \textit{The Review of Economics and Statistics}, 82(4), 540--554.'),
    'FMS': ('10.1111/rssa.12043', 'Foroni, Marcellino and Schumacher (2015)', 'Foroni, Marcellino și Schumacher (2015)',
            r'Foroni, C., Marcellino, M., \& Schumacher, C. (2015). Unrestricted mixed data sampling (MIDAS): MIDAS regressions with unrestricted lag polynomials. \textit{Journal of the Royal Statistical Society: Series A}, 178(1), 57--82.'),
    'GG': ('10.1109/TPAMI.1984.4767596', 'Geman and Geman (1984)', 'Geman și Geman (1984)',
           r'Geman, S., \& Geman, D. (1984). Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images. \textit{IEEE Transactions on Pattern Analysis and Machine Intelligence}, PAMI-6(6), 721--741.'),
    'Gh': ('10.1016/j.jeconom.2016.04.008', 'Ghysels (2016)', 'Ghysels (2016)',
           r'Ghysels, E. (2016). Macroeconomics and the reality of mixed frequency data. \textit{Journal of Econometrics}, 193(2), 294--314.'),
    'GLP': ('10.1162/REST_a_00483', 'Giannone, Lenza and Primiceri (2015)', 'Giannone, Lenza și Primiceri (2015)',
            r'Giannone, D., Lenza, M., \& Primiceri, G. E. (2015). Prior selection for vector autoregressions. \textit{The Review of Economics and Statistics}, 97(2), 436--451.'),
    'GLPb': ('10.3982/ECTA17842', 'Giannone, Lenza and Primiceri (2021)', 'Giannone, Lenza și Primiceri (2021)',
             r'Giannone, D., Lenza, M., \& Primiceri, G. E. (2021). Economic predictions with big data: The illusion of sparsity. \textit{Econometrica}, 89(5), 2409--2437.'),
    'GR': ('10.1214/ss/1177011136', 'Gelman and Rubin (1992)', 'Gelman și Rubin (1992)',
           r'Gelman, A., \& Rubin, D. B. (1992). Inference from iterative simulation using multiple sequences. \textit{Statistical Science}, 7(4), 457--472.'),
    'GRS': ('10.1016/j.jmoneco.2008.05.010', 'Giannone, Reichlin and Small (2008)', 'Giannone, Reichlin și Small (2008)',
            r'Giannone, D., Reichlin, L., \& Small, D. (2008). Nowcasting: The real-time informational content of macroeconomic data. \textit{Journal of Monetary Economics}, 55(4), 665--676.'),
    'GS': ('10.1080/01621459.1990.10476213', 'Gelfand and Smith (1990)', 'Gelfand și Smith (1990)',
           r'Gelfand, A. E., \& Smith, A. F. M. (1990). Sampling-based approaches to calculating marginal densities. \textit{Journal of the American Statistical Association}, 85(410), 398--409.'),
    'GSV': ('10.1016/j.jeconom.2005.01.004', 'Ghysels, Santa-Clara and Valkanov (2006)', 'Ghysels, Santa-Clara și Valkanov (2006)',
            r'Ghysels, E., Santa-Clara, P., \& Valkanov, R. (2006). Predicting volatility: Getting the most out of return data sampled at different frequencies. \textit{Journal of Econometrics}, 131(1--2), 59--95.'),
    'GSVb': ('10.1080/07474930600972467', 'Ghysels, Sinko and Valkanov (2007)', 'Ghysels, Sinko și Valkanov (2007)',
             r'Ghysels, E., Sinko, A., \& Valkanov, R. (2007). MIDAS regressions: Further results and new directions. \textit{Econometric Reviews}, 26(1), 53--90.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'Karl': ('10.1016/B978-0-444-62731-5.00015-4', 'Karlsson (2013)', 'Karlsson (2013)',
             r'Karlsson, S. (2013). Forecasting with Bayesian vector autoregression. In G. Elliott \& A. Timmermann (Eds.), \textit{Handbook of Economic Forecasting} (Vol.\ 2B, pp.\ 791--897). Elsevier.'),
    'KK': ('10.1002/(SICI)1099-1255(199703)12:2<99::AID-JAE429>3.0.CO;2-A', 'Kadiyala and Karlsson (1997)', 'Kadiyala și Karlsson (1997)',
           r'Kadiyala, K. R., \& Karlsson, S. (1997). Numerical methods for estimation and inference in Bayesian VAR-models. \textit{Journal of Applied Econometrics}, 12(2), 99--132.'),
    'KL': ('10.1017/9781108164818', 'Kilian and Lütkepohl (2017)', 'Kilian și Lütkepohl (2017)',
           r'Kilian, L., \& Lütkepohl, H. (2017). \textit{Structural Vector Autoregressive Analysis}. Cambridge University Press.'),
    'KoKo': ('10.1561/0800000013', 'Koop and Korobilis (2010)', 'Koop și Korobilis (2010)',
             r'Koop, G., \& Korobilis, D. (2010). Bayesian multivariate time series methods for empirical macroeconomics. \textit{Foundations and Trends in Econometrics}, 3(4), 267--358.'),
    'Koop': ('10.1002/jae.1270', 'Koop (2013)', 'Koop (2013)',
             r'Koop, G. (2013). Forecasting with medium and large Bayesian VARs. \textit{Journal of Applied Econometrics}, 28(2), 177--203.'),
    'KR': ('10.1080/01621459.1995.10476572', 'Kass and Raftery (1995)', 'Kass și Raftery (1995)',
           r'Kass, R. E., \& Raftery, A. E. (1995). Bayes factors. \textit{Journal of the American Statistical Association}, 90(430), 773--795.'),
    'Lit': ('10.1080/07350015.1986.10509491', 'Litterman (1986)', 'Litterman (1986)',
            r'Litterman, R. B. (1986). Forecasting with Bayesian vector autoregressions: Five years of experience. \textit{Journal of Business \& Economic Statistics}, 4(1), 25--38.'),
    'LP': ('10.1002/jae.2895', 'Lenza and Primiceri (2022)', 'Lenza și Primiceri (2022)',
           r'Lenza, M., \& Primiceri, G. E. (2022). How to estimate a vector autoregression after March 2020. \textit{Journal of Applied Econometrics}, 37(4), 688--699.'),
    'MM': ('10.1002/jae.695', 'Mariano and Murasawa (2003)', 'Mariano și Murasawa (2003)',
           r'Mariano, R. S., \& Murasawa, Y. (2003). A new coincident index of business cycles based on monthly and quarterly series. \textit{Journal of Applied Econometrics}, 18(4), 427--443.'),
    'MN': ('10.1080/07350015.2015.1086655', 'McCracken and Ng (2016)', 'McCracken și Ng (2016)',
           r'McCracken, M. W., \& Ng, S. (2016). FRED-MD: A monthly database for macroeconomic research. \textit{Journal of Business \& Economic Statistics}, 34(4), 574--589.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'Prim': ('10.1111/j.1467-937X.2005.00353.x', 'Primiceri (2005)', 'Primiceri (2005)',
             r'Primiceri, G. E. (2005). Time varying structural vector autoregressions and monetary policy. \textit{The Review of Economic Studies}, 72(3), 821--852.'),
    'Sims': ('https://www.nber.org/books-and-chapters/business-cycles-indicators-and-forecasting/nine-variable-probabilistic-macroeconomic-forecasting-model',
             'Sims (1993)', 'Sims (1993)',
             r'Sims, C. A. (1993). A nine-variable probabilistic macroeconomic forecasting model. In J. H. Stock \& M. W. Watson (Eds.), \textit{Business Cycles, Indicators and Forecasting} (pp.\ 179--212). University of Chicago Press.'),
    'SS': ('10.1080/07350015.2014.954707', 'Schorfheide and Song (2015)', 'Schorfheide și Song (2015)',
           r'Schorfheide, F., \& Song, D. (2015). Real-time forecasting with a mixed-frequency VAR. \textit{Journal of Business \& Economic Statistics}, 33(3), 366--380.'),
    'SWa': ('10.1198/016214502388618960', 'Stock and Watson (2002a)', 'Stock și Watson (2002a)',
            r'Stock, J. H., \& Watson, M. W. (2002a). Forecasting using principal components from a large number of predictors. \textit{Journal of the American Statistical Association}, 97(460), 1167--1179.'),
    'SWb': ('10.1198/073500102317351921', 'Stock and Watson (2002b)', 'Stock și Watson (2002b)',
            r'Stock, J. H., \& Watson, M. W. (2002b). Macroeconomic forecasting using diffusion indexes. \textit{Journal of Business \& Economic Statistics}, 20(2), 147--162.'),
    'SWc': ('10.1016/bs.hesmac.2016.04.002', 'Stock and Watson (2016)', 'Stock și Watson (2016)',
            r'Stock, J. H., \& Watson, M. W. (2016). Dynamic factor models, factor-augmented vector autoregressions, and structural vector autoregressions in macroeconomics. In J. B. Taylor \& H. Uhlig (Eds.), \textit{Handbook of Macroeconomics} (Vol.\ 2A, pp.\ 415--525). Elsevier.'),
    'SWd': ('10.1086/654119', 'Stock and Watson (1989)', 'Stock și Watson (1989)',
            r'Stock, J. H., \& Watson, M. W. (1989). New indexes of coincident and leading economic indicators. \textit{NBER Macroeconomics Annual}, 4, 351--394.'),
    'SZ': ('10.2307/2527347', 'Sims and Zha (1998)', 'Sims și Zha (1998)',
           r'Sims, C. A., \& Zha, T. (1998). Bayesian methods for dynamic multivariate models. \textit{International Economic Review}, 39(4), 949--968.'),
    'VGS': ('10.1214/20-BA1221', 'Vehtari et al.\\ (2021)', 'Vehtari et al.\\ (2021)',
            r'Vehtari, A., Gelman, A., Simpson, D., Carpenter, B., \& Bürkner, P.-C. (2021). Rank-normalization, folding, and localization: An improved $\widehat{R}$ for assessing convergence of MCMC. \textit{Bayesian Analysis}, 16(2), 667--718.'),
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
