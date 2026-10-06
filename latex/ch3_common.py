r"""
ch3_common.py -- shared helpers of the Chapter 3 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_03/ch3_numbers.json (generate_all_charts.py) and
sem3_results.json (seminar3.py); the clickable citations of Chapter 3 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_03')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_03'
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
    with open(os.path.join(QL, 'ch3_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem3_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'ARW': ('10.3982/ECTA14468', 'Arias, Rubio-Ramírez and Waggoner (2018)', 'Arias, Rubio-Ramírez și Waggoner (2018)',
            r'Arias, J. E., Rubio-Ramírez, J. F., \& Waggoner, D. F. (2018). Inference based on structural vector autoregressions identified with sign and zero restrictions: Theory and applications. \textit{Econometrica}, 86(2), 685--720.'),
    'ADRR': ('10.1257/aer.20161852', 'Antolín-Díaz and Rubio-Ramírez (2018)', 'Antolín-Díaz și Rubio-Ramírez (2018)',
             r'Antolín-Díaz, J., \& Rubio-Ramírez, J. F. (2018). Narrative sign restrictions for SVARs. \textit{American Economic Review}, 108(10), 2802--2829.'),
    'BS': ('10.1086/723574', 'Bauer and Swanson (2023)', 'Bauer și Swanson (2023)',
           r'Bauer, M. D., \& Swanson, E. T. (2023). A reassessment of monetary policy surprises and high-frequency identification. \textit{NBER Macroeconomics Annual}, 37, 87--155.'),
    'BHa': ('10.3982/ECTA12356', 'Baumeister and Hamilton (2015)', 'Baumeister și Hamilton (2015)',
            r'Baumeister, C., \& Hamilton, J. D. (2015). Sign restrictions, structural vector autoregressions, and useful prior information. \textit{Econometrica}, 83(5), 1963--1999.'),
    'BHb': ('10.1257/aer.20151569', 'Baumeister and Hamilton (2019)', 'Baumeister și Hamilton (2019)',
            r'Baumeister, C., \& Hamilton, J. D. (2019). Structural interpretation of vector autoregressions with incomplete identification: Revisiting the role of oil supply and demand shocks. \textit{American Economic Review}, 109(5), 1873--1910.'),
    'BP': ('10.1162/003355302320935043', 'Blanchard and Perotti (2002)', 'Blanchard și Perotti (2002)',
           r'Blanchard, O., \& Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. \textit{The Quarterly Journal of Economics}, 117(4), 1329--1368.'),
    'BQ': ('https://www.jstor.org/stable/1827924', 'Blanchard and Quah (1989)', 'Blanchard și Quah (1989)',
           r'Blanchard, O. J., \& Quah, D. (1989). The dynamic effects of aggregate demand and supply disturbances. \textit{American Economic Review}, 79(4), 655--673.'),
    'CEE': ('10.1016/S1574-0048(99)01005-8', 'Christiano, Eichenbaum and Evans (1999)', 'Christiano, Eichenbaum și Evans (1999)',
            r'Christiano, L. J., Eichenbaum, M., \& Evans, C. L. (1999). Monetary policy shocks: What have we learned and to what end? In J. B. Taylor \& M. Woodford (Eds.), \textit{Handbook of Macroeconomics} (Vol.\ 1A, pp.\ 65--148). Elsevier.'),
    'FL': ('10.1080/07350015.1997.10524712', 'Faust and Leeper (1997)', 'Faust și Leeper (1997)',
           r'Faust, J., \& Leeper, E. M. (1997). When do long-run identifying restrictions give reliable results? \textit{Journal of Business \& Economic Statistics}, 15(3), 345--353.'),
    'FP': ('10.1257/jel.49.4.938', 'Fry and Pagan (2011)', 'Fry și Pagan (2011)',
           r'Fry, R., \& Pagan, A. (2011). Sign restrictions in structural vector autoregressions: A critical review. \textit{Journal of Economic Literature}, 49(4), 938--960.'),
    'Gali': ('10.1257/aer.89.1.249', 'Galí (1999)', 'Galí (1999)',
             r'Galí, J. (1999). Technology, employment, and the business cycle: Do technology shocks explain aggregate fluctuations? \textit{American Economic Review}, 89(1), 249--271.'),
    'GK': ('10.1257/mac.20130329', 'Gertler and Karadi (2015)', 'Gertler și Karadi (2015)',
           r'Gertler, M., \& Karadi, P. (2015). Monetary policy surprises, credit costs, and economic activity. \textit{American Economic Journal: Macroeconomics}, 7(1), 44--76.'),
    'GKi': ('10.3982/ecta16773', 'Giacomini and Kitagawa (2021)', 'Giacomini și Kitagawa (2021)',
            r'Giacomini, R., \& Kitagawa, T. (2021). Robust Bayesian inference for set-identified models. \textit{Econometrica}, 89(4), 1519--1556.'),
    'GoK': ('10.1016/j.jeconom.2003.10.030', 'Gonçalves and Kilian (2004)', 'Gonçalves și Kilian (2004)',
            r'Gonçalves, S., \& Kilian, L. (2004). Bootstrapping autoregressions with conditional heteroskedasticity of unknown form. \textit{Journal of Econometrics}, 123(1), 89--120.'),
    'GSS': ('https://www.ijcb.org/journal/ijcb05q2a2.htm', 'Gürkaynak, Sack and Swanson (2005)', 'Gürkaynak, Sack și Swanson (2005)',
            r'Gürkaynak, R. S., Sack, B., \& Swanson, E. T. (2005). Do actions speak louder than words? The response of asset prices to monetary policy actions and statements. \textit{International Journal of Central Banking}, 1(1), 55--93.'),
    'Ham': ('10.2307/j.ctv14jx6sm', 'Hamilton (1994)', 'Hamilton (1994)',
            r'Hamilton, J. D. (1994). \textit{Time Series Analysis}. Princeton University Press.'),
    'JK': ('10.1257/mac.20180090', 'Jarociński and Karadi (2020)', 'Jarociński și Karadi (2020)',
           r'Jarociński, M., \& Karadi, P. (2020). Deconstructing monetary policy surprises: The role of information shocks. \textit{American Economic Journal: Macroeconomics}, 12(2), 1--43.'),
    'JL': ('10.1257/aer.20162011', 'Jentsch and Lunsford (2019)', 'Jentsch și Lunsford (2019)',
           r'Jentsch, C., \& Lunsford, K. G. (2019). The dynamic effects of personal and corporate income tax changes in the United States: Comment. \textit{American Economic Review}, 109(7), 2655--2678.'),
    'Jorda': ('10.1257/0002828053828518', 'Jordà (2005)', 'Jordà (2005)',
              r'Jordà, Ò. (2005). Estimation and inference of impulse responses by local projections. \textit{American Economic Review}, 95(1), 161--182.'),
    'KilA': ('10.1162/003465398557465', 'Kilian (1998)', 'Kilian (1998)',
              r'Kilian, L. (1998). Small-sample confidence intervals for impulse response functions. \textit{The Review of Economics and Statistics}, 80(2), 218--230.'),
    'KilB': ('10.1257/aer.99.3.1053', 'Kilian (2009)', 'Kilian (2009)',
              r'Kilian, L. (2009). Not all oil price shocks are alike: Disentangling demand and supply shocks in the crude oil market. \textit{American Economic Review}, 99(3), 1053--1069.'),
    'KilC': ('10.1016/j.econlet.2019.03.001', 'Kilian (2019)', 'Kilian (2019)',
              r'Kilian, L. (2019). Measuring global real economic activity: Do recent critiques hold up to scrutiny? \textit{Economics Letters}, 178, 106--110.'),
    'KL': ('10.1017/9781108164818', 'Kilian and Lütkepohl (2017)', 'Kilian și Lütkepohl (2017)',
           r'Kilian, L., \& Lütkepohl, H. (2017). \textit{Structural Vector Autoregressive Analysis}. Cambridge University Press.'),
    'Kut': ('10.1016/S0304-3932(01)00055-1', 'Kuttner (2001)', 'Kuttner (2001)',
            r'Kuttner, K. N. (2001). Monetary policy surprises and interest rates: Evidence from the Fed funds futures market. \textit{Journal of Monetary Economics}, 47(3), 523--544.'),
    'LL': ('10.1111/j.1538-4616.2008.00151.x', 'Lanne and Lütkepohl (2008)', 'Lanne și Lütkepohl (2008)',
           r'Lanne, M., \& Lütkepohl, H. (2008). Identifying monetary policy shocks via changes in volatility. \textit{Journal of Money, Credit and Banking}, 40(6), 1131--1149.'),
    'LPW': ('10.1016/j.jeconom.2024.105722', 'Li, Plagborg-Møller and Wolf (2024)', 'Li, Plagborg-Møller și Wolf (2024)',
            r'Li, D., Plagborg-Møller, M., \& Wolf, C. K. (2024). Local projections vs.\ VARs: Lessons from thousands of DGPs. \textit{Journal of Econometrics}, 244(2), 105722.'),
    'Lut': ('10.1007/978-3-540-27752-1', 'Lütkepohl (2005)', 'Lütkepohl (2005)',
            r'Lütkepohl, H. (2005). \textit{New Introduction to Multiple Time Series Analysis}. Springer.'),
    'MR': ('10.1257/aer.103.4.1212', 'Mertens and Ravn (2013)', 'Mertens și Ravn (2013)',
           r'Mertens, K., \& Ravn, M. O. (2013). The dynamic effects of personal and corporate income tax changes in the United States. \textit{American Economic Review}, 103(4), 1212--1247.'),
    'MOPa': ('10.1002/jae.2656', 'Montiel Olea and Plagborg-Møller (2019)', 'Montiel Olea și Plagborg-Møller (2019)',
             r'Montiel Olea, J. L., \& Plagborg-Møller, M. (2019). Simultaneous confidence bands: Theory, implementation, and an application to SVARs. \textit{Journal of Applied Econometrics}, 34(1), 1--17.'),
    'MOPb': ('10.3982/ECTA18756', 'Montiel Olea and Plagborg-Møller (2021)', 'Montiel Olea și Plagborg-Møller (2021)',
             r'Montiel Olea, J. L., \& Plagborg-Møller, M. (2021). Local projection inference is simpler and more robust than you think. \textit{Econometrica}, 89(4), 1789--1823.'),
    'MSW': ('10.1016/j.jeconom.2020.05.014', 'Montiel Olea, Stock and Watson (2021)', 'Montiel Olea, Stock și Watson (2021)',
            r'Montiel Olea, J. L., Stock, J. H., \& Watson, M. W. (2021). Inference in structural vector autoregressions identified with an external instrument. \textit{Journal of Econometrics}, 225(1), 74--87.'),
    'NS': ('10.1093/qje/qjy004', 'Nakamura and Steinsson (2018)', 'Nakamura și Steinsson (2018)',
           r'Nakamura, E., \& Steinsson, J. (2018). High-frequency identification of monetary non-neutrality: The information effect. \textit{The Quarterly Journal of Economics}, 133(3), 1283--1330.'),
    'PW': ('10.3982/ECTA17813', 'Plagborg-Møller and Wolf (2021)', 'Plagborg-Møller și Wolf (2021)',
           r'Plagborg-Møller, M., \& Wolf, C. K. (2021). Local projections and VARs estimate the same impulse responses. \textit{Econometrica}, 89(2), 955--980.'),
    'Ram': ('10.1016/bs.hesmac.2016.03.003', 'Ramey (2016)', 'Ramey (2016)',
            r'Ramey, V. A. (2016). Macroeconomic shocks and their propagation. In J. B. Taylor \& H. Uhlig (Eds.), \textit{Handbook of Macroeconomics} (Vol.\ 2A, pp.\ 71--162). Elsevier.'),
    'RZ': ('10.1086/696277', 'Ramey and Zubairy (2018)', 'Ramey și Zubairy (2018)',
           r'Ramey, V. A., \& Zubairy, S. (2018). Government spending multipliers in good times and in bad: Evidence from US historical data. \textit{Journal of Political Economy}, 126(2), 850--901.'),
    'Rig': ('10.1162/003465303772815727', 'Rigobon (2003)', 'Rigobon (2003)',
            r'Rigobon, R. (2003). Identification through heteroskedasticity. \textit{The Review of Economics and Statistics}, 85(4), 777--792.'),
    'RR': ('10.1257/0002828042002651', 'Romer and Romer (2004)', 'Romer și Romer (2004)',
           r'Romer, C. D., \& Romer, D. H. (2004). A new measure of monetary shocks: Derivation and implications. \textit{American Economic Review}, 94(4), 1055--1084.'),
    'RWZ': ('10.1111/j.1467-937X.2009.00578.x', 'Rubio-Ramírez, Waggoner and Zha (2010)', 'Rubio-Ramírez, Waggoner și Zha (2010)',
            r'Rubio-Ramírez, J. F., Waggoner, D. F., \& Zha, T. (2010). Structural vector autoregressions: Theory of identification and algorithms for inference. \textit{The Review of Economic Studies}, 77(2), 665--696.'),
    'Sims': ('10.2307/1912017', 'Sims (1980)', 'Sims (1980)',
             r'Sims, C. A. (1980). Macroeconomics and reality. \textit{Econometrica}, 48(1), 1--48.'),
    'SWa': ('10.1257/jep.15.4.101', 'Stock and Watson (2001)', 'Stock și Watson (2001)',
            r'Stock, J. H., \& Watson, M. W. (2001). Vector autoregressions. \textit{Journal of Economic Perspectives}, 15(4), 101--115.'),
    'SWb': ('10.1353/eca.2012.0005', 'Stock and Watson (2012)', 'Stock și Watson (2012)',
            r'Stock, J. H., \& Watson, M. W. (2012). Disentangling the channels of the 2007--09 recession. \textit{Brookings Papers on Economic Activity}, 2012(1), 81--135.'),
    'SWc': ('10.1111/ecoj.12593', 'Stock and Watson (2018)', 'Stock și Watson (2018)',
            r'Stock, J. H., \& Watson, M. W. (2018). Identification and estimation of dynamic causal effects in macroeconomics using external instruments. \textit{The Economic Journal}, 128(610), 917--948.'),
    'Uhl': ('10.1016/j.jmoneco.2004.05.007', 'Uhlig (2005)', 'Uhlig (2005)',
            r'Uhlig, H. (2005). What are the effects of monetary policy on output? Results from an agnostic identification procedure. \textit{Journal of Monetary Economics}, 52(2), 381--419.'),
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
        shown = ('doi:' + v[0]) if not v[0].startswith('http') else v[0].split('/')[2].replace('www.', '')
        safe_u = u.replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#')
        shown = shown.replace('_', '\\_').replace('<', '\\textless{}').replace('>', '\\textgreater{}').replace('#', '\\#')
        out.append(v[3] + f' \\href{{{safe_u}}}{{{shown}}}')
    return out
