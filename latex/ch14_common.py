r"""
ch14_common.py -- shared helpers of the Chapter 14 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_14/ch14_numbers.json (generate_all_charts.py) and
sem14_results.json (seminar12.py); the clickable citations of Chapter 14 (DOIs checked against Crossref, arXiv and the
official pages, 6 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_14')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_14'
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
    with open(os.path.join(QL, 'ch14_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem14_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
AX = 'https://arxiv.org/abs/'
R = {
    'AbG': ('10.1257/000282803321455188', 'Abadie and Gardeazabal (2003)', 'Abadie și Gardeazabal (2003)',
            r'Abadie, A., \& Gardeazabal, J. (2003). The economic costs of conflict: A case study of the Basque Country. \textit{American Economic Review}, 93(1), 113--132.'),
    'ADHa': ('10.1198/jasa.2009.ap08746', 'Abadie, Diamond and Hainmueller (2010)', 'Abadie, Diamond și Hainmueller (2010)',
             r'Abadie, A., Diamond, A., \& Hainmueller, J. (2010). Synthetic control methods for comparative case studies: Estimating the effect of California’s tobacco control program. \textit{Journal of the American Statistical Association}, 105(490), 493--505.'),
    'ADHs': ('10.18637/jss.v042.i13', 'Abadie, Diamond and Hainmueller (2011)', 'Abadie, Diamond și Hainmueller (2011)',
             r'Abadie, A., Diamond, A., \& Hainmueller, J. (2011). Synth: An R package for synthetic control methods in comparative case studies. \textit{Journal of Statistical Software}, 42(13), 1--17.'),
    'ADHb': ('10.1111/ajps.12116', 'Abadie, Diamond and Hainmueller (2015)', 'Abadie, Diamond și Hainmueller (2015)',
             r'Abadie, A., Diamond, A., \& Hainmueller, J. (2015). Comparative politics and the synthetic control method. \textit{American Journal of Political Science}, 59(2), 495--510.'),
    'Aba': ('10.1257/jel.20191450', 'Abadie (2021)', 'Abadie (2021)',
            r'Abadie, A. (2021). Using synthetic controls: Feasibility, data requirements, and methodological aspects. \textit{Journal of Economic Literature}, 59(2), 391--425.'),
    'AJK': ('10.1080/07350015.2016.1204919', 'Angrist, Jordà and Kuersteiner (2018)', 'Angrist, Jordà și Kuersteiner (2018)',
            r'Angrist, J. D., Jordà, Ò., \& Kuersteiner, G. M. (2018). Semiparametric estimates of monetary policy effects: String theory revisited. \textit{Journal of Business \& Economic Statistics}, 36(3), 371--387.'),
    'SDID': ('10.1257/aer.20190159', 'Arkhangelsky et al.\\ (2021)', 'Arkhangelsky et al.\\ (2021)',
             r'Arkhangelsky, D., Athey, S., Hirshberg, D. A., Imbens, G. W., \& Wager, S. (2021). Synthetic difference-in-differences. \textit{American Economic Review}, 111(12), 4088--4118.'),
    'AI': ('10.1257/jep.31.2.3', 'Athey and Imbens (2017)', 'Athey și Imbens (2017)',
           r'Athey, S., \& Imbens, G. W. (2017). The state of applied econometrics: Causality and policy evaluation. \textit{Journal of Economic Perspectives}, 31(2), 3--32.'),
    'BBG': ('10.1016/j.qref.2025.102006', 'Babalos, Bouri and Gupta (2025)', 'Babalos, Bouri și Gupta (2025)',
            r'Babalos, V., Bouri, E., \& Gupta, R. (2025). Does the introduction of US spot Bitcoin ETFs affect spot returns and volatility of major cryptocurrencies? \textit{The Quarterly Review of Economics and Finance}, 102, 102006.'),
    'Bai': ('10.3982/ECTA6135', 'Bai (2009)', 'Bai (2009)',
            r'Bai, J. (2009). Panel data models with interactive fixed effects. \textit{Econometrica}, 77(4), 1229--1279.'),
    'BBS': ('10.1103/PhysRevLett.103.238701', 'Barnett, Barrett and Seth (2009)', 'Barnett, Barrett și Seth (2009)',
            r'Barnett, L., Barrett, A. B., \& Seth, A. K. (2009). Granger causality and transfer entropy are equivalent for Gaussian variables. \textit{Physical Review Letters}, 103(23), 238701.'),
    'BaC': ('10.1073/pnas.1700369114', 'Baskerville and Cobey (2017)', 'Baskerville și Cobey (2017)',
            r'Baskerville, E. B., \& Cobey, S. (2017). Does influenza drive absolute humidity? \textit{Proceedings of the National Academy of Sciences}, 114(12), E2270--E2271.'),
    'ASCM': ('10.1080/01621459.2021.1929245', 'Ben-Michael, Feller and Rothstein (2021)', 'Ben-Michael, Feller și Rothstein (2021)',
             r'Ben-Michael, E., Feller, A., \& Rothstein, J. (2021). The augmented synthetic control method. \textit{Journal of the American Statistical Association}, 116(536), 1789--1803.'),
    'BMKW': ('10.1007/s10797-019-09566-5', 'Benedek et al.\\ (2020)', 'Benedek et al.\\ (2020)',
             r'Benedek, D., De Mooij, R. A., Keen, M., \& Wingender, P. (2020). Varieties of VAT pass through. \textit{International Tax and Public Finance}, 27(4), 890--930.'),
    'BoS': ('10.1080/01621459.2018.1527225', 'Bojinov and Shephard (2019)', 'Bojinov și Shephard (2019)',
            r'Bojinov, I., \& Shephard, N. (2019). Time series experiments and causal estimands: Exact randomization tests and trading. \textit{Journal of the American Statistical Association}, 114(528), 1665--1682.'),
    'BMSS': ('10.1093/ej/uez020', 'Born et al.\\ (2019)', 'Born et al.\\ (2019)',
             r'Born, B., Müller, G. J., Schularick, M., \& Sedláček, P. (2019). The costs of economic nationalism: Evidence from the Brexit experiment. \textit{The Economic Journal}, 129(623), 2722--2744.'),
    'BrC': ('10.1016/j.jeconom.2005.02.004', 'Breitung and Candelon (2006)', 'Breitung și Candelon (2006)',
            r'Breitung, J., \& Candelon, B. (2006). Testing for short- and long-run causality: A frequency-domain approach. \textit{Journal of Econometrics}, 132(2), 363--378.'),
    'CI': ('10.1214/14-AOAS788', 'Brodersen et al.\\ (2015)', 'Brodersen et al.\\ (2015)',
           r'Brodersen, K. H., Gallusser, F., Koehler, J., Remy, N., \& Scott, S. L. (2015). Inferring causal impact using Bayesian structural time-series models. \textit{The Annals of Applied Statistics}, 9(1), 247--274.'),
    'CSA': ('10.1016/j.jeconom.2020.12.001', 'Callaway and Sant’Anna (2021)', 'Callaway și Sant’Anna (2021)',
            r'Callaway, B., \& Sant’Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. \textit{Journal of Econometrics}, 225(2), 200--230.'),
    'dCDH': ('10.1257/aer.20181169', 'de Chaisemartin and D’Haultfœuille (2020)', 'de Chaisemartin și D’Haultfœuille (2020)',
             r'de Chaisemartin, C., \& D’Haultfœuille, X. (2020). Two-way fixed effects estimators with heterogeneous treatment effects. \textit{American Economic Review}, 110(9), 2964--2996.'),
    'DML': ('10.1111/ectj.12097', 'Chernozhukov et al.\\ (2018)', 'Chernozhukov et al.\\ (2018)',
            r'Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W., \& Robins, J. (2018). Double/debiased machine learning for treatment and structural parameters. \textit{The Econometrics Journal}, 21(1), C1--C68.'),
    'CWZ': ('10.1080/01621459.2021.1920957', 'Chernozhukov, Wüthrich and Zhu (2021)', 'Chernozhukov, Wüthrich și Zhu (2021)',
            r'Chernozhukov, V., Wüthrich, K., \& Zhu, Y. (2021). An exact and robust conformal inference method for counterfactual and synthetic controls. \textit{Journal of the American Statistical Association}, 116(536), 1849--1864.'),
    'DI': ('10.3386/w22791', 'Doudchenko and Imbens (2016)', 'Doudchenko și Imbens (2016)',
           r'Doudchenko, N., \& Imbens, G. W. (2016). Balancing, regression, difference-in-differences and synthetic control methods: A synthesis. NBER Working Paper 22791.'),
    'DK': ('10.1093/acprof:oso/9780199641178.001.0001', 'Durbin and Koopman (2012)', 'Durbin și Koopman (2012)',
           r'Durbin, J., \& Koopman, S. J. (2012). \textit{Time Series Analysis by State Space Methods} (2nd ed.). Oxford University Press.'),
    'EuroCT': ('https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_ct/default/table', 'Eurostat (2026b)', 'Eurostat (2026b)',
               r'Eurostat (2026b). HICP at constant tax rates, monthly data (prc\_hicp\_ct). European Commission, Luxembourg.'),
    'EuroM': ('https://ec.europa.eu/eurostat/web/hicp/methodology', 'Eurostat (2026c)', 'Eurostat (2026c)',
              r'Eurostat (2026c). Harmonised Index of Consumer Prices (HICP): Methodology. European Commission, Luxembourg.'),
    'FP': ('10.3982/QE1596', 'Ferman and Pinto (2021)', 'Ferman și Pinto (2021)',
           r'Ferman, B., \& Pinto, C. (2021). Synthetic controls with imperfect pretreatment fit. \textit{Quantitative Economics}, 12(4), 1197--1221.'),
    'FiP': ('10.1515/jci-2016-0026', 'Firpo and Possebom (2018)', 'Firpo și Possebom (2018)',
            r'Firpo, S., \& Possebom, V. (2018). Synthetic control method: Inference, sensitivity analysis and confidence sets. \textit{Journal of Causal Inference}, 6(2), 20160026.'),
    'Gew': ('10.1080/01621459.1982.10477803', 'Geweke (1982)', 'Geweke (1982)',
            r'Geweke, J. (1982). Measurement of linear dependence and feedback between multiple time series. \textit{Journal of the American Statistical Association}, 77(378), 304--313.'),
    'GB': ('10.1016/j.jeconom.2021.03.014', 'Goodman-Bacon (2021)', 'Goodman-Bacon (2021)',
           r'Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment timing. \textit{Journal of Econometrics}, 225(2), 254--277.'),
    'Gra': ('10.2307/1912791', 'Granger (1969)', 'Granger (1969)',
            r'Granger, C. W. J. (1969). Investigating causal relations by econometric models and cross-spectral methods. \textit{Econometrica}, 37(3), 424--438.'),
    'Ham': ('10.1515/9780691218632', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'Har': ('10.1017/CBO9781107049994', 'Harvey (1989)', 'Harvey (1989)',
            r'Harvey, A. C. (1989). \textit{Forecasting, Structural Time Series Models and the Kalman Filter}. Cambridge University Press.'),
    'HCW': ('10.1002/jae.1230', 'Hsiao, Ching and Wan (2012)', 'Hsiao, Ching și Wan (2012)',
            r'Hsiao, C., Ching, H. S., \& Wan, S. K. (2012). A panel data approach for program evaluation: Measuring the benefits of political and economic integration of Hong Kong with mainland China. \textit{Journal of Applied Econometrics}, 27(5), 705--740.'),
    'IR': ('10.1017/CBO9781139025751', 'Imbens and Rubin (2015)', 'Imbens și Rubin (2015)',
           r'Imbens, G. W., \& Rubin, D. B. (2015). \textit{Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction}. Cambridge University Press.'),
    'Jor': ('10.1257/0002828053828518', 'Jordà (2005)', 'Jordà (2005)',
            r'Jordà, Ò. (2005). Estimation and inference of impulse responses by local projections. \textit{American Economic Review}, 95(1), 161--182.'),
    'KL': ('10.1017/9781108164818', 'Kilian and Lütkepohl (2017)', 'Kilian și Lütkepohl (2017)',
           r'Kilian, L., \& Lütkepohl, H. (2017). \textit{Structural Vector Autoregressive Analysis}. Cambridge University Press.'),
    'LCG': ('10.1093/ije/dyw098', 'Lopez Bernal, Cummins and Gasparrini (2017)', 'Lopez Bernal, Cummins și Gasparrini (2017)',
            r'Lopez Bernal, J., Cummins, S., \& Gasparrini, A. (2017). Interrupted time series regression for the evaluation of public health interventions: A tutorial. \textit{International Journal of Epidemiology}, 46(1), 348--355.'),
    'Mac': ('https://www.jstor.org/stable/2729691', 'MacKinlay (1997)', 'MacKinlay (1997)',
            r'MacKinlay, A. C. (1997). Event studies in economics and finance. \textit{Journal of Economic Literature}, 35(1), 13--39.'),
    'Mon': ('10.1016/j.future.2016.12.009', 'Mønster et al.\\ (2017)', 'Mønster et al.\\ (2017)',
            r'Mønster, D., Fusaroli, R., Tylén, K., Roepstorff, A., \& Sherson, J. F. (2017). Causal inference from noisy time-series data: Testing the convergent cross-mapping algorithm in the presence of noise and external influence. \textit{Future Generation Computer Systems}, 73, 52--62.'),
    'NW': ('10.2307/1913610', 'Newey and West (1987)', 'Newey și West (1987)',
           r'Newey, W. K., \& West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. \textit{Econometrica}, 55(3), 703--708.'),
    'Pea': ('10.1017/CBO9780511803161', 'Pearl (2009)', 'Pearl (2009)',
            r'Pearl, J. (2009). \textit{Causality: Models, Reasoning, and Inference} (2nd ed.). Cambridge University Press.'),
    'PMW': ('10.3982/ECTA17813', 'Plagborg-Møller and Wolf (2021)', 'Plagborg-Møller și Wolf (2021)',
            r'Plagborg-Møller, M., \& Wolf, C. K. (2021). Local projections and VARs estimate the same impulse responses. \textit{Econometrica}, 89(2), 955--980.'),
    'RS': (AX + '1903.01637', 'Rambachan and Shephard (2021)', 'Rambachan și Shephard (2021)',
           r'Rambachan, A., \& Shephard, N. (2021). When do common time series estimands have nonparametric causal meaning? Working paper, arXiv:1903.01637.'),
    'RSBP': ('10.1016/j.jeconom.2023.03.008', 'Roth et al.\\ (2023)', 'Roth et al.\\ (2023)',
             r'Roth, J., Sant’Anna, P. H. C., Bilinski, A., \& Poe, J. (2023). What’s trending in difference-in-differences? A synthesis of the recent econometrics literature. \textit{Journal of Econometrics}, 235(2), 2218--2244.'),
    'Rub': ('10.1037/h0037350', 'Rubin (1974)', 'Rubin (1974)',
            r'Rubin, D. B. (1974). Estimating causal effects of treatments in randomized and nonrandomized studies. \textit{Journal of Educational Psychology}, 66(5), 688--701.'),
    'PCMCI': ('10.1126/sciadv.aau4996', 'Runge et al.\\ (2019a)', 'Runge et al.\\ (2019a)',
              r'Runge, J., Nowack, P., Kretschmer, M., Flaxman, S., \& Sejdinovic, D. (2019a). Detecting and quantifying causal associations in large nonlinear time series datasets. \textit{Science Advances}, 5(11), eaau4996.'),
    'RunE': ('10.1038/s41467-019-10105-3', 'Runge et al.\\ (2019b)', 'Runge et al.\\ (2019b)',
             r'Runge, J., Bathiany, S., Bollt, E., Camps-Valls, G., Coumou, D., Deyle, E., Glymour, C., Kretschmer, M., Mahecha, M. D., Muñoz-Marí, J., et al.\ (2019b). Inferring causation from time series in Earth system sciences. \textit{Nature Communications}, 10, 2553.'),
    'Sch': ('10.1103/PhysRevLett.85.461', 'Schreiber (2000)', 'Schreiber (2000)',
            r'Schreiber, T. (2000). Measuring information transfer. \textit{Physical Review Letters}, 85(2), 461--464.'),
    'SV': ('10.1504/IJMMNO.2014.059942', 'Scott and Varian (2014)', 'Scott și Varian (2014)',
           r'Scott, S. L., \& Varian, H. R. (2014). Predicting the present with Bayesian structural time series. \textit{International Journal of Mathematical Modelling and Numerical Optimisation}, 5(1/2), 4--23.'),
    'SEC': ('https://www.sec.gov/files/rules/sro/nysearca/2024/34-99306.pdf', 'SEC (2024)', 'SEC (2024)',
            r'U.S. Securities and Exchange Commission (2024). Order granting accelerated approval of proposed rule changes to list and trade bitcoin-based commodity-based trust shares and trust units. Release No. 34-99306, 10 January 2024.'),
    'Sims': ('https://www.jstor.org/stable/1806097', 'Sims (1972)', 'Sims (1972)',
             r'Sims, C. A. (1972). Money, income, and causality. \textit{American Economic Review}, 62(4), 540--552.'),
    'SGS': ('10.7551/mitpress/1754.001.0001', 'Spirtes, Glymour and Scheines (2000)', 'Spirtes, Glymour și Scheines (2000)',
            r'Spirtes, P., Glymour, C., \& Scheines, R. (2000). \textit{Causation, Prediction, and Search} (2nd ed.). MIT Press.'),
    'SW': ('10.1111/ecoj.12593', 'Stock and Watson (2018)', 'Stock și Watson (2018)',
           r'Stock, J. H., \& Watson, M. W. (2018). Identification and estimation of dynamic causal effects in macroeconomics using external instruments. \textit{The Economic Journal}, 128(610), 917--948.'),
    'Sug': ('10.1126/science.1227079', 'Sugihara et al.\\ (2012)', 'Sugihara et al.\\ (2012)',
            r'Sugihara, G., May, R., Ye, H., Hsieh, C.-h., Deyle, E., Fogarty, M., \& Munch, S. (2012). Detecting causality in complex ecosystems. \textit{Science}, 338(6106), 496--500.'),
    'SA': ('10.1016/j.jeconom.2020.09.006', 'Sun and Abraham (2021)', 'Sun și Abraham (2021)',
           r'Sun, L., \& Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. \textit{Journal of Econometrics}, 225(2), 175--199.'),
    'TY': ('10.1016/0304-4076(94)01616-8', 'Toda and Yamamoto (1995)', 'Toda și Yamamoto (1995)',
           r'Toda, H. Y., \& Yamamoto, T. (1995). Statistical inference in vector autoregressions with possibly integrated processes. \textit{Journal of Econometrics}, 66(1--2), 225--250.'),
    'Xu': ('10.1017/pan.2016.2', 'Xu (2017)', 'Xu (2017)',
           r'Xu, Y. (2017). Generalized synthetic control method: Causal inference with interactive fixed effects models. \textit{Political Analysis}, 25(1), 57--76.'),
    'YDGS': ('10.1038/srep14750', 'Ye et al.\\ (2015)', 'Ye et al.\\ (2015)',
             r'Ye, H., Deyle, E. R., Gilarranz, L. J., \& Sugihara, G. (2015). Distinguishing time-delayed causal interactions using convergent cross mapping. \textit{Scientific Reports}, 5, 14750.'),
}

R.update({
    'KPSb': ('10.1186/s41937-017-0004-9', 'Klößner et al.\\ (2018)', 'Klößner et al.\\ (2018)',
             r'Klößner, S., Kaul, A., Pfeifer, G., \& Schieler, M. (2018). Comparative politics and the synthetic control method revisited: A note on Abadie et al.\ (2015). \textit{Swiss Journal of Economics and Statistics}, 154, 11.'),
    'FrP': ('10.1103/PhysRevLett.99.204101', 'Frenzel and Pompe (2007)', 'Frenzel și Pompe (2007)',
            r'Frenzel, S., \& Pompe, B. (2007). Partial mutual information for coupling analysis of multivariate time series. \textit{Physical Review Letters}, 99(20), 204101.'),
    'KSG': ('10.1103/PhysRevE.69.066138', 'Kraskov, Stögbauer and Grassberger (2004)', 'Kraskov, Stögbauer și Grassberger (2004)',
            r'Kraskov, A., Stögbauer, H., \& Grassberger, P. (2004). Estimating mutual information. \textit{Physical Review E}, 69(6), 066138.'),
    'KKPS': ('10.1080/07350015.2021.1930012', 'Kaul et al.\\ (2022)', 'Kaul et al.\\ (2022)',
             r'Kaul, A., Klößner, S., Pfeifer, G., \& Schieler, M. (2022). Standard synthetic control methods: The case of using all preintervention outcomes together with covariates. \textit{Journal of Business \& Economic Statistics}, 40(3), 1362--1376.'),
    'And': ('10.1111/1468-0262.00466', 'Andrews (2003)', 'Andrews (2003)',
            r'Andrews, D. W. K. (2003). End-of-sample instability tests. \textit{Econometrica}, 71(6), 1661--1694.'),
    'Tak': ('10.1007/BFb0091924', 'Takens (1981)', 'Takens (1981)',
            r'Takens, F. (1981). Detecting strange attractors in turbulence. In D. Rand \& L.-S. Young (Eds.), \textit{Dynamical Systems and Turbulence, Warwick 1980}, Lecture Notes in Mathematics 898, 366--381. Springer.'),
    'ADHd': ('10.7910/DVN/24714', 'Abadie, Diamond and Hainmueller (2014)', 'Abadie, Diamond și Hainmueller (2014)',
             r'Abadie, A., Diamond, A., \& Hainmueller, J. (2014). Replication data for: Comparative politics and the synthetic control method. Harvard Dataverse, version 2.1 (CC0); erratum and updated archive, version 3 (2026).'),
    'OECD': ('https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN1@DF_QNA/1.1', 'OECD (2026)', 'OECD (2026)',
             r'OECD (2026). Quarterly National Accounts: GDP, chain-linked volumes, PPP, seasonally adjusted (DSD\_NAMAIN1@DF\_QNA). OECD Data Explorer, SDMX API.'),
    'EuroH': ('https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_minr/default/table', 'Eurostat (2026a)', 'Eurostat (2026a)',
              r'Eurostat (2026a). Harmonised index of consumer prices (HICP), ECOICOP ver. 2, indices and rates of change, monthly data (prc\_hicp\_minr).'),
})


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
