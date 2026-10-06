r"""
ch8_common.py -- shared helpers of the Chapter 8 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_08/ch8_numbers.json (generate_all_charts.py) and
sem8_results.json (seminar8.py); the clickable citations of Chapter 8 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401
from ch3_common import T, V2, finalize, month, quarter, pv, minus_fix   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_08')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_08'
OMI_URL = 'https://web.archive.org/web/20211204000000*/realized.oxford-man.ox.ac.uk'
BIN_URL = 'https://data.binance.vision'


def load():
    with open(os.path.join(QL, 'ch8_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem8_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'Aie': ('10.1080/07350015.2013.771027', 'Aielli (2013)', 'Aielli (2013)',
            r'Aielli, G. P. (2013). Dynamic conditional correlation: On properties and estimation. \textit{Journal of Business \& Economic Statistics}, 31(3), 282--299.'),
    'ABDL': ('10.1111/1468-0262.00418', 'Andersen, Bollerslev, Diebold and Labys (2003)', 'Andersen, Bollerslev, Diebold și Labys (2003)',
             r'Andersen, T. G., Bollerslev, T., Diebold, F. X., \& Labys, P. (2003). Modeling and forecasting realized volatility. \textit{Econometrica}, 71(2), 579--625.'),
    'ABD': ('10.1162/rest.89.4.701', 'Andersen, Bollerslev and Diebold (2007)', 'Andersen, Bollerslev și Diebold (2007)',
            r'Andersen, T. G., Bollerslev, T., \& Diebold, F. X. (2007). Roughing it up: Including jump components in the measurement, modeling, and forecasting of return volatility. \textit{The Review of Economics and Statistics}, 89(4), 701--720.'),
    'ADS': ('10.1016/j.jeconom.2012.01.011', 'Andersen, Dobrev and Schaumburg (2012)', 'Andersen, Dobrev și Schaumburg (2012)',
            r'Andersen, T. G., Dobrev, D., \& Schaumburg, E. (2012). Jump-robust volatility estimation using nearest neighbor truncation. \textit{Journal of Econometrics}, 169(1), 75--93.'),
    'AB': ('10.2307/2527343', 'Andersen and Bollerslev (1998)', 'Andersen și Bollerslev (1998)',
           r'Andersen, T. G., \& Bollerslev, T. (1998). Answering the skeptics: Yes, standard volatility models do provide accurate forecasts. \textit{International Economic Review}, 39(4), 885--905.'),
    'BR': ('10.1111/j.1467-937X.2008.00474.x', 'Bandi and Russell (2008)', 'Bandi și Russell (2008)',
           r'Bandi, F. M., \& Russell, J. R. (2008). Microstructure noise, realized variance, and optimal sampling. \textit{The Review of Economic Studies}, 75(2), 339--369.'),
    'BNSa': ('10.1111/1467-9868.00336', 'Barndorff-Nielsen and Shephard (2002)', 'Barndorff-Nielsen și Shephard (2002)',
             r'Barndorff-Nielsen, O. E., \& Shephard, N. (2002). Econometric analysis of realized volatility and its use in estimating stochastic volatility models. \textit{Journal of the Royal Statistical Society: Series B}, 64(2), 253--280.'),
    'BNSb': ('10.1093/jjfinec/nbh001', 'Barndorff-Nielsen and Shephard (2004)', 'Barndorff-Nielsen și Shephard (2004)',
             r'Barndorff-Nielsen, O. E., \& Shephard, N. (2004). Power and bipower variation with stochastic volatility and jumps. \textit{Journal of Financial Econometrics}, 2(1), 1--37.'),
    'BNSc': ('10.1093/jjfinec/nbi022', 'Barndorff-Nielsen and Shephard (2006)', 'Barndorff-Nielsen și Shephard (2006)',
             r'Barndorff-Nielsen, O. E., \& Shephard, N. (2006). Econometrics of testing for jumps in financial economics using bipower variation. \textit{Journal of Financial Econometrics}, 4(1), 1--30.'),
    'BNHLSa': ('10.3982/ECTA6495', 'Barndorff-Nielsen, Hansen, Lunde and Shephard (2008)', 'Barndorff-Nielsen, Hansen, Lunde și Shephard (2008)',
               r'Barndorff-Nielsen, O. E., Hansen, P. R., Lunde, A., \& Shephard, N. (2008). Designing realized kernels to measure the ex post variation of equity prices in the presence of noise. \textit{Econometrica}, 76(6), 1481--1536.'),
    'BNHLSb': ('10.1111/j.1368-423X.2008.00275.x', 'Barndorff-Nielsen et al.\\ (2009)', 'Barndorff-Nielsen et al.\\ (2009)',
               r'Barndorff-Nielsen, O. E., Hansen, P. R., Lunde, A., \& Shephard, N. (2009). Realized kernels in practice: Trades and quotes. \textit{The Econometrics Journal}, 12(3), C1--C32.'),
    'BNHLSc': ('10.1016/j.jeconom.2010.07.009', 'Barndorff-Nielsen et al.\\ (2011)', 'Barndorff-Nielsen et al.\\ (2011)',
               r'Barndorff-Nielsen, O. E., Hansen, P. R., Lunde, A., \& Shephard, N. (2011). Multivariate realised kernels: Consistent positive semi-definite estimators of the covariation of equity prices with noise and non-synchronous trading. \textit{Journal of Econometrics}, 162(2), 149--169.'),
    'BHK': ('10.3150/bj/1068128975', 'Berkes, Horváth and Kokoszka (2003)', 'Berkes, Horváth și Kokoszka (2003)',
            r'Berkes, I., Horváth, L., \& Kokoszka, P. (2003). GARCH processes: Structure and estimation. \textit{Bernoulli}, 9(2), 201--227.'),
    'Bol': ('10.1016/0304-4076(86)90063-1', 'Bollerslev (1986)', 'Bollerslev (1986)',
            r'Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. \textit{Journal of Econometrics}, 31(3), 307--327.'),
    'BolC': ('10.2307/2109358', 'Bollerslev (1990)', 'Bollerslev (1990)',
             r'Bollerslev, T. (1990). Modelling the coherence in short-run nominal exchange rates: A multivariate generalized ARCH model. \textit{The Review of Economics and Statistics}, 72(3), 498--505.'),
    'BW': ('10.1080/07474939208800229', 'Bollerslev and Wooldridge (1992)', 'Bollerslev și Wooldridge (1992)',
           r'Bollerslev, T., \& Wooldridge, J. M. (1992). Quasi-maximum likelihood estimation and inference in dynamic models with time-varying covariances. \textit{Econometric Reviews}, 11(2), 143--172.'),
    'BPQ': ('10.1016/j.jeconom.2015.10.007', 'Bollerslev, Patton and Quaedvlieg (2016)', 'Bollerslev, Patton și Quaedvlieg (2016)',
            r'Bollerslev, T., Patton, A. J., \& Quaedvlieg, R. (2016). Exploiting the errors: A simple approach for improved volatility forecasting. \textit{Journal of Econometrics}, 192(1), 1--18.'),
    'CV': ('10.1002/jae.1152', 'Chiriac and Voev (2011)', 'Chiriac și Voev (2011)',
           r'Chiriac, R., \& Voev, V. (2011). Modelling and forecasting multivariate realized volatility. \textit{Journal of Applied Econometrics}, 26(6), 922--947.'),
    'CL': ('10.1016/S0047-259X(02)00009-X', 'Comte and Lieberman (2003)', 'Comte și Lieberman (2003)',
           r'Comte, F., \& Lieberman, O. (2003). Asymptotic theory for multivariate GARCH processes. \textit{Journal of Multivariate Analysis}, 84(1), 61--84.'),
    'CK': ('10.1002/jae.2742', 'Conrad and Kleen (2020)', 'Conrad și Kleen (2020)',
           r'Conrad, C., \& Kleen, O. (2020). Two are better than one: Volatility forecasting using multiplicative component GARCH-MIDAS models. \textit{Journal of Applied Econometrics}, 35(1), 19--45.'),
    'Cor': ('10.1093/jjfinec/nbp001', 'Corsi (2009)', 'Corsi (2009)',
            r'Corsi, F. (2009). A simple approximate long-memory model of realized volatility. \textit{Journal of Financial Econometrics}, 7(2), 174--196.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'Eng': ('10.2307/1912773', 'Engle (1982)', 'Engle (1982)',
            r'Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. \textit{Econometrica}, 50(4), 987--1007.'),
    'EngD': ('10.1198/073500102288618487', 'Engle (2002)', 'Engle (2002)',
             r'Engle, R. (2002). Dynamic conditional correlation: A simple class of multivariate generalized autoregressive conditional heteroskedasticity models. \textit{Journal of Business \& Economic Statistics}, 20(3), 339--350.'),
    'EGS': ('10.1162/REST_a_00300', 'Engle, Ghysels and Sohn (2013)', 'Engle, Ghysels și Sohn (2013)',
            r'Engle, R. F., Ghysels, E., \& Sohn, B. (2013). Stock market volatility and macroeconomic fundamentals. \textit{The Review of Economics and Statistics}, 95(3), 776--797.'),
    'EK': ('10.1017/S0266466600009063', 'Engle and Kroner (1995)', 'Engle și Kroner (1995)',
           r'Engle, R. F., \& Kroner, K. F. (1995). Multivariate simultaneous generalized ARCH. \textit{Econometric Theory}, 11(1), 122--150.'),
    'EL': ('10.1093/oso/9780198296836.003.0020', 'Engle and Lee (1999)', 'Engle și Lee (1999)',
           r'Engle, R. F., \& Lee, G. G. J. (1999). A long-run and short-run component model of stock return volatility. In R. F. Engle \& H. White (Eds.), \textit{Cointegration, Causality, and Forecasting: A Festschrift in Honour of Clive W. J. Granger} (pp.\ 475--497). Oxford University Press.'),
    'ELW': ('10.1080/07350015.2017.1345683', 'Engle, Ledoit and Wolf (2019)', 'Engle, Ledoit și Wolf (2019)',
            r'Engle, R. F., Ledoit, O., \& Wolf, M. (2019). Large dynamic covariance matrices. \textit{Journal of Business \& Economic Statistics}, 37(2), 363--375.'),
    'ES': ('10.3386/w8554', 'Engle and Sheppard (2001)', 'Engle și Sheppard (2001)',
           r'Engle, R. F., \& Sheppard, K. (2001). Theoretical and empirical properties of dynamic conditional correlation multivariate GARCH. \textit{NBER Working Paper} 8554.'),
    'Epp': ('10.1080/01621459.1979.10482508', 'Epps (1979)', 'Epps (1979)',
            r'Epps, T. W. (1979). Comovements in stock prices in the very short run. \textit{Journal of the American Statistical Association}, 74(366), 291--298.'),
    'FZa': ('10.3150/bj/1093265632', 'Francq and Zakoïan (2004)', 'Francq și Zakoïan (2004)',
            r'Francq, C., \& Zakoïan, J.-M. (2004). Maximum likelihood estimation of pure GARCH and ARMA-GARCH processes. \textit{Bernoulli}, 10(4), 605--637.'),
    'FZ': ('10.1002/9781119313472', 'Francq and Zakoïan (2019)', 'Francq și Zakoïan (2019)',
           r'Francq, C., \& Zakoïan, J.-M. (2019). \textit{GARCH Models: Structure, Statistical Inference and Financial Applications} (2nd ed.). Wiley.'),
    'GSV': ('10.1016/j.jeconom.2005.01.004', 'Ghysels, Santa-Clara and Valkanov (2006)', 'Ghysels, Santa-Clara și Valkanov (2006)',
            r'Ghysels, E., Santa-Clara, P., \& Valkanov, R. (2006). Predicting volatility: Getting the most out of return data sampled at different frequencies. \textit{Journal of Econometrics}, 131(1--2), 59--95.'),
    'GJR': ('10.1111/j.1540-6261.1993.tb05128.x', 'Glosten, Jagannathan and Runkle (1993)', 'Glosten, Jagannathan și Runkle (1993)',
            r'Glosten, L. R., Jagannathan, R., \& Runkle, D. E. (1993). On the relation between the expected value and the volatility of the nominal excess return on stocks. \textit{The Journal of Finance}, 48(5), 1779--1801.'),
    'HP': ('10.1016/j.jmva.2009.03.011', 'Hafner and Preminger (2009)', 'Hafner și Preminger (2009)',
           r'Hafner, C. M., \& Preminger, A. (2009). On asymptotic theory for multivariate GARCH models. \textit{Journal of Multivariate Analysis}, 100(9), 2044--2054.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'HH': ('10.1080/07350015.2015.1038543', 'Hansen and Huang (2016)', 'Hansen și Huang (2016)',
           r'Hansen, P. R., \& Huang, Z. (2016). Exponential GARCH modeling with realized measures of volatility. \textit{Journal of Business \& Economic Statistics}, 34(2), 269--287.'),
    'HHS': ('10.1002/jae.1234', 'Hansen, Huang and Shek (2012)', 'Hansen, Huang și Shek (2012)',
            r'Hansen, P. R., Huang, Z., \& Shek, H. H. (2012). Realized GARCH: A joint model for returns and realized measures of volatility. \textit{Journal of Applied Econometrics}, 27(6), 877--906.'),
    'HLa': ('10.1002/jae.800', 'Hansen and Lunde (2005)', 'Hansen și Lunde (2005)',
            r'Hansen, P. R., \& Lunde, A. (2005). A forecast comparison of volatility models: Does anything beat a GARCH(1,1)? \textit{Journal of Applied Econometrics}, 20(7), 873--889.'),
    'HLb': ('10.1016/j.jeconom.2005.01.005', 'Hansen and Lunde (2006a)', 'Hansen și Lunde (2006a)',
            r'Hansen, P. R., \& Lunde, A. (2006a). Consistent ranking of volatility models. \textit{Journal of Econometrics}, 131(1--2), 97--121.'),
    'HLc': ('10.1198/073500106000000071', 'Hansen and Lunde (2006b)', 'Hansen și Lunde (2006b)',
            r'Hansen, P. R., \& Lunde, A. (2006b). Realized variance and market microstructure noise. \textit{Journal of Business \& Economic Statistics}, 24(2), 127--161.'),
    'HLN': ('10.3982/ECTA5771', 'Hansen, Lunde and Nason (2011)', 'Hansen, Lunde și Nason (2011)',
            r'Hansen, P. R., Lunde, A., \& Nason, J. M. (2011). The model confidence set. \textit{Econometrica}, 79(2), 453--497.'),
    'OMI': ('https://web.archive.org/web/2021/https://realized.oxford-man.ox.ac.uk/terms-and-conditions', 'Heber, Lunde, Shephard and Sheppard (2009)', 'Heber, Lunde, Shephard și Sheppard (2009)',
            r"Heber, G., Lunde, A., Shephard, N., \& Sheppard, K. (2009). \textit{Oxford-Man Institute's realized library}, version 0.3. Oxford-Man Institute, University of Oxford (discontinued in 2022; copy of 28 February 2022 preserved by the Internet Archive)."),
    'HT': ('10.1093/jjfinec/nbi025', 'Huang and Tauchen (2005)', 'Huang și Tauchen (2005)',
           r'Huang, X., \& Tauchen, G. (2005). The relative contribution of jumps to total price variance. \textit{Journal of Financial Econometrics}, 3(4), 456--499.'),
    'JLMPV': ('10.1016/j.spa.2008.11.004', 'Jacod et al.\\ (2009)', 'Jacod et al.\\ (2009)',
              r'Jacod, J., Li, Y., Mykland, P. A., Podolskij, M., \& Vetter, M. (2009). Microstructure noise in the continuous case: The pre-averaging approach. \textit{Stochastic Processes and their Applications}, 119(7), 2249--2276.'),
    'JR': ('10.1017/S0266466604206065', 'Jensen and Rahbek (2004)', 'Jensen și Rahbek (2004)',
           r'Jensen, S. T., \& Rahbek, A. (2004). Asymptotic inference for nonstationary GARCH. \textit{Econometric Theory}, 20(6), 1203--1226.'),
    'LRV': ('10.1002/jae.1248', 'Laurent, Rombouts and Violante (2012)', 'Laurent, Rombouts și Violante (2012)',
            r'Laurent, S., Rombouts, J. V. K., \& Violante, F. (2012). On the forecasting accuracy of multivariate GARCH models. \textit{Journal of Applied Econometrics}, 27(6), 934--955.'),
    'LWa': ('10.1016/S0047-259X(03)00096-4', 'Ledoit and Wolf (2004)', 'Ledoit și Wolf (2004)',
            r'Ledoit, O., \& Wolf, M. (2004). A well-conditioned estimator for large-dimensional covariance matrices. \textit{Journal of Multivariate Analysis}, 88(2), 365--411.'),
    'LWb': ('10.1214/19-AOS1921', 'Ledoit and Wolf (2020)', 'Ledoit și Wolf (2020)',
            r'Ledoit, O., \& Wolf, M. (2020). Analytical nonlinear shrinkage of large-dimensional covariance matrices. \textit{The Annals of Statistics}, 48(5), 3043--3065.'),
    'LH': ('10.1017/S0266466600008215', 'Lee and Hansen (1994)', 'Lee și Hansen (1994)',
           r'Lee, S.-W., \& Hansen, B. E. (1994). Asymptotic theory for the GARCH(1,1) quasi-maximum likelihood estimator. \textit{Econometric Theory}, 10(1), 29--52.'),
    'LM': ('10.1093/rfs/hhm056', 'Lee and Mykland (2008)', 'Lee și Mykland (2008)',
           r'Lee, S. S., \& Mykland, P. A. (2008). Jumps in financial markets: A new nonparametric test and jump dynamics. \textit{The Review of Financial Studies}, 21(6), 2535--2563.'),
    'LMc': ('10.1017/S0266466603192092', 'Ling and McAleer (2003)', 'Ling și McAleer (2003)',
            r'Ling, S., \& McAleer, M. (2003). Asymptotic theory for a vector ARMA-GARCH model. \textit{Econometric Theory}, 19(2), 280--310.'),
    'Lum': ('10.2307/2171862', 'Lumsdaine (1996)', 'Lumsdaine (1996)',
            r'Lumsdaine, R. L. (1996). Consistency and asymptotic normality of the quasi-maximum likelihood estimator in IGARCH(1,1) and covariance stationary GARCH(1,1) models. \textit{Econometrica}, 64(3), 575--596.'),
    'NW': ('10.2307/1913610', 'Newey and West (1987)', 'Newey și West (1987)',
           r'Newey, W. K., \& West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. \textit{Econometrica}, 55(3), 703--708.'),
    'PSSE': ('10.1080/07350015.2020.1713795', 'Pakel, Shephard, Sheppard and Engle (2021)', 'Pakel, Shephard, Sheppard și Engle (2021)',
             r'Pakel, C., Shephard, N., Sheppard, K., \& Engle, R. F. (2021). Fitting vast dimensional time-varying covariance models. \textit{Journal of Business \& Economic Statistics}, 39(3), 652--668.'),
    'Pat': ('10.1016/j.jeconom.2010.03.034', 'Patton (2011)', 'Patton (2011)',
            r'Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. \textit{Journal of Econometrics}, 160(1), 246--256.'),
    'PS': ('10.1162/REST_a_00503', 'Patton and Sheppard (2015)', 'Patton și Sheppard (2015)',
           r'Patton, A. J., \& Sheppard, K. (2015). Good volatility, bad volatility: Signed jumps and the persistence of volatility. \textit{The Review of Economics and Statistics}, 97(3), 683--697.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'SS': ('10.1002/jae.1158', 'Shephard and Sheppard (2010)', 'Shephard și Sheppard (2010)',
           r'Shephard, N., \& Sheppard, K. (2010). Realising the future: Forecasting with high-frequency-based volatility (HEAVY) models. \textit{Journal of Applied Econometrics}, 25(2), 197--231.'),
    'ZMA': ('10.1198/016214505000000169', 'Zhang, Mykland and Aït-Sahalia (2005)', 'Zhang, Mykland și Aït-Sahalia (2005)',
            r'Zhang, L., Mykland, P. A., \& Aït-Sahalia, Y. (2005). A tale of two time scales: Determining integrated volatility with noisy high-frequency data. \textit{Journal of the American Statistical Association}, 100(472), 1394--1411.'),
}


def _url(x):
    return x if x.startswith('http') else D_ + x


def _safe(u):
    return u.replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#').replace(';', '\\%3B').replace('%', '\\%').replace('\\\\%', '\\%')


REFS = ''.join(ref(k, _safe(_url(v[0])), v[1], v[2]) for k, v in R.items())


def bib(keys=None):
    """Bibliography entries (alphabetical) with a clickable DOI or URL."""
    out = []
    key = lambda kv: re.sub(r'[^a-z0-9]', '', kv[1][3].lower().replace('ï', 'i').replace('á', 'a'))   # noqa: E731
    for k, v in sorted(R.items(), key=key):
        if keys is not None and k not in keys:
            continue
        u = _safe(_url(v[0]))
        shown = ('doi:' + v[0]) if not v[0].startswith('http') else v[0].split('/')[2].replace('www.', '')
        shown = shown.replace('_', '\\_').replace('<', '\\textless{}').replace('>', '\\textgreater{}').replace('#', '\\#')
        out.append(v[3] + f' \\href{{{u}}}{{{shown}}}')
    return out
