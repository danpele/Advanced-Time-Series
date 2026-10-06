r"""
ch11_common.py -- shared helpers of the Chapter 11 generators (lecture and seminar), ATS
========================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_11/ch11_numbers.json (generate_all_charts.py) and
sem11_results.json (seminar11.py); the clickable citations of Chapter 11 (DOIs checked against Crossref, 5 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_11')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_11'
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
    with open(os.path.join(QL, 'ch11_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem11_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    'ACS': ('10.1111/joes.12012', 'Aguiar-Conraria and Soares (2014)', 'Aguiar-Conraria și Soares (2014)',
            r'Aguiar-Conraria, L., \& Soares, M. J. (2014). The continuous wavelet transform: Moving beyond uni- and bivariate analysis. \textit{Journal of Economic Surveys}, 28(2), 344--375.'),
    'AAS': ('10.1016/j.physa.2008.01.063', 'Aguiar-Conraria, Azevedo and Soares (2008)', 'Aguiar-Conraria, Azevedo și Soares (2008)',
            r'Aguiar-Conraria, L., Azevedo, N., \& Soares, M. J. (2008). Using wavelets to decompose the time--frequency effects of monetary policy. \textit{Physica A}, 387(12), 2863--2878.'),
    'And': ('10.2307/2938229', 'Andrews (1991)', 'Andrews (1991)',
            r'Andrews, D. W. K. (1991). Heteroskedasticity and autocorrelation consistent covariance matrix estimation. \textit{Econometrica}, 59(3), 817--858.'),
    'BK': ('10.1162/003465399558454', 'Baxter and King (1999)', 'Baxter și King (1999)',
           r'Baxter, M., \& King, R. G. (1999). Measuring business cycles: Approximate band-pass filters for economic time series. \textit{Review of Economics and Statistics}, 81(4), 575--593.'),
    'BC': ('10.1016/j.jeconom.2005.02.004', 'Breitung and Candelon (2006)', 'Breitung și Candelon (2006)',
           r'Breitung, J., \& Candelon, B. (2006). Testing for short- and long-run causality: A frequency-domain approach. \textit{Journal of Econometrics}, 132(2), 363--378.'),
    'BD': ('10.1007/978-1-4419-0320-4', 'Brockwell and Davis (1991)', 'Brockwell și Davis (1991)',
           r'Brockwell, P. J., \& Davis, R. A. (1991). \textit{Time Series: Theory and Methods} (2nd ed.). Springer.'),
    'CF': ('10.1111/1468-2354.t01-1-00076', 'Christiano and Fitzgerald (2003)', 'Christiano și Fitzgerald (2003)',
           r'Christiano, L. J., \& Fitzgerald, T. J. (2003). The band pass filter. \textit{International Economic Review}, 44(2), 435--465.'),
    'CN': ('10.1016/0165-1889(93)00781-X', 'Cogley and Nason (1995)', 'Cogley și Nason (1995)',
           r'Cogley, T., \& Nason, J. M. (1995). Effects of the Hodrick--Prescott filter on trend and difference stationary time series: Implications for business cycle research. \textit{Journal of Economic Dynamics and Control}, 19(1--2), 253--278.'),
    'CFR': ('10.1162/00346530151143770', 'Croux, Forni and Reichlin (2001)', 'Croux, Forni și Reichlin (2001)',
            r'Croux, C., Forni, M., \& Reichlin, L. (2001). A measure of comovement for economic variables: Theory and empirics. \textit{Review of Economics and Statistics}, 83(2), 232--241.'),
    'Cro': ('10.1111/j.1467-6419.2006.00502.x', 'Crowley (2007)', 'Crowley (2007)',
            r'Crowley, P. M. (2007). A guide to wavelets for economists. \textit{Journal of Economic Surveys}, 21(2), 207--267.'),
    'Dah': ('10.1214/aos/1034276620', 'Dahlhaus (1997)', 'Dahlhaus (1997)',
            r'Dahlhaus, R. (1997). Fitting time series models to nonstationary processes. \textit{The Annals of Statistics}, 25(1), 1--37.'),
    'Dau': ('10.1002/cpa.3160410705', 'Daubechies (1988)', 'Daubechies (1988)',
            r'Daubechies, I. (1988). Orthonormal bases of compactly supported wavelets. \textit{Communications on Pure and Applied Mathematics}, 41(7), 909--996.'),
    'FK': ('10.1016/j.jce.2006.06.007', 'Fidrmuc and Korhonen (2006)', 'Fidrmuc și Korhonen (2006)',
           r'Fidrmuc, J., \& Korhonen, I. (2006). Meta-analysis of the business cycle correlation between the euro area and the CEECs. \textit{Journal of Comparative Economics}, 34(3), 518--537.'),
    'FR': ('10.1111/0022-1082.00494', 'Forbes and Rigobon (2002)', 'Forbes și Rigobon (2002)',
           r'Forbes, K. J., \& Rigobon, R. (2002). No contagion, only interdependence: Measuring stock market comovements. \textit{The Journal of Finance}, 57(5), 2223--2261.'),
    'GSW': ('10.1016/j.jimonfin.2004.10.003', 'Gençay, Selçuk and Whitcher (2005)', 'Gençay, Selçuk și Whitcher (2005)',
            r'Gençay, R., Selçuk, F., \& Whitcher, B. (2005). Multiscale systematic risk. \textit{Journal of International Money and Finance}, 24(1), 55--70.'),
    'GSWb': ('10.1016/B978-012279670-8.50010-0', 'Gençay, Selçuk and Whitcher (2002)', 'Gençay, Selçuk și Whitcher (2002)',
             r'Gençay, R., Selçuk, F., \& Whitcher, B. (2002). Wavelets for variance--covariance estimation. In \textit{An Introduction to Wavelets and Other Filtering Methods in Finance and Economics}. Academic Press.'),
    'Gew': ('10.1080/01621459.1982.10477803', 'Geweke (1982)', 'Geweke (1982)',
            r'Geweke, J. (1982). Measurement of linear dependence and feedback between multiple time series. \textit{Journal of the American Statistical Association}, 77(378), 304--313.'),
    'Gra': ('10.2307/1909859', 'Granger (1966)', 'Granger (1966)',
            r'Granger, C. W. J. (1966). The typical spectral shape of an economic variable. \textit{Econometrica}, 34(1), 150--161.'),
    'GMJ': ('10.5194/npg-11-561-2004', 'Grinsted, Moore and Jevrejeva (2004)', 'Grinsted, Moore și Jevrejeva (2004)',
            r'Grinsted, A., Moore, J. C., \& Jevrejeva, S. (2004). Application of the cross wavelet transform and wavelet coherence to geophysical time series. \textit{Nonlinear Processes in Geophysics}, 11(5/6), 561--566.'),
    'GM': ('10.1137/0515056', 'Grossmann and Morlet (1984)', 'Grossmann și Morlet (1984)',
           r'Grossmann, A., \& Morlet, J. (1984). Decomposition of Hardy functions into square integrable wavelets of constant shape. \textit{SIAM Journal on Mathematical Analysis}, 15(4), 723--736.'),
    'Ham': ('10.1162/rest_a_00706', 'Hamilton (2018)', 'Hamilton (2018)',
            r'Hamilton, J. D. (2018). Why you should never use the Hodrick--Prescott filter. \textit{The Review of Economics and Statistics}, 100(5), 831--843.'),
    'HPa': ('10.1016/S0304-3932(01)00108-8', 'Harding and Pagan (2002)', 'Harding și Pagan (2002)',
            r'Harding, D., \& Pagan, A. (2002). Dissecting the cycle: A methodological investigation. \textit{Journal of Monetary Economics}, 49(2), 365--381.'),
    'HP': ('10.2307/2953682', 'Hodrick and Prescott (1997)', 'Hodrick și Prescott (1997)',
           r'Hodrick, R. J., \& Prescott, E. C. (1997). Postwar U.S. business cycles: An empirical investigation. \textit{Journal of Money, Credit and Banking}, 29(1), 1--16.'),
    'Hur': ('10.1080/01621459.1985.10478207', 'Hurvich (1985)', 'Hurvich (1985)',
            r'Hurvich, C. M. (1985). Data-driven choice of a spectrum estimate: Extending the applicability of cross-validation methods. \textit{Journal of the American Statistical Association}, 80(392), 933--940.'),
    'KP': ('10.1111/j.1468-2354.2009.00568.x', 'Kilian and Park (2009)', 'Kilian și Park (2009)',
           r'Kilian, L., \& Park, C. (2009). The impact of oil price shocks on the U.S. stock market. \textit{International Economic Review}, 50(4), 1267--1287.'),
    'LLW': ('10.1175/2007JTECHO511.1', 'Liu, Liang and Weisberg (2007)', 'Liu, Liang și Weisberg (2007)',
            r'Liu, Y., San Liang, X., \& Weisberg, R. H. (2007). Rectification of the bias in the wavelet power spectrum. \textit{Journal of Atmospheric and Oceanic Technology}, 24(12), 2093--2102.'),
    'Mal': ('10.1109/34.192463', 'Mallat (1989)', 'Mallat (1989)',
            r'Mallat, S. G. (1989). A theory for multiresolution signal decomposition: The wavelet representation. \textit{IEEE Transactions on Pattern Analysis and Machine Intelligence}, 11(7), 674--693.'),
    'MK': ('10.5194/npg-11-505-2004', 'Maraun and Kurths (2004)', 'Maraun și Kurths (2004)',
           r'Maraun, D., \& Kurths, J. (2004). Cross wavelet analysis: Significance testing and pitfalls. \textit{Nonlinear Processes in Geophysics}, 11(4), 505--514.'),
    'Par': ('10.1080/00401706.1961.10489939', 'Parzen (1961)', 'Parzen (1961)',
            r'Parzen, E. (1961). Mathematical considerations in the estimation of spectra. \textit{Technometrics}, 3(2), 167--190.'),
    'Per': ('10.1093/biomet/82.3.619', 'Percival (1995)', 'Percival (1995)',
            r'Percival, D. B. (1995). On estimation of the wavelet variance. \textit{Biometrika}, 82(3), 619--631.'),
    'PWa': ('10.1017/CBO9780511622762', 'Percival and Walden (1993)', 'Percival și Walden (1993)',
            r'Percival, D. B., \& Walden, A. T. (1993). \textit{Spectral Analysis for Physical Applications: Multitaper and Conventional Univariate Techniques}. Cambridge University Press.'),
    'PWb': ('10.1017/CBO9780511841040', 'Percival and Walden (2000)', 'Percival și Walden (2000)',
            r'Percival, D. B., \& Walden, A. T. (2000). \textit{Wavelet Methods for Time Series Analysis}. Cambridge University Press.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'PS': ('10.1111/iere.12495', 'Phillips and Shi (2021)', 'Phillips și Shi (2021)',
           r'Phillips, P. C. B., \& Shi, Z. (2021). Boosting: Why you can use the HP filter. \textit{International Economic Review}, 62(2), 521--570.'),
    'Pri': ('10.1111/j.2517-6161.1965.tb01488.x', 'Priestley (1965)', 'Priestley (1965)',
            r'Priestley, M. B. (1965). Evolutionary spectra and non-stationary processes. \textit{Journal of the Royal Statistical Society: Series B}, 27(2), 204--229.'),
    'QW': ('10.1080/07350015.2020.1784747', 'Quast and Wolters (2022)', 'Quast și Wolters (2022)',
           r'Quast, J., \& Wolters, M. H. (2022). Reliable real-time output gap estimates based on a modified Hamilton filter. \textit{Journal of Business \& Economic Statistics}, 40(1), 152--168.'),
    'RU': ('10.1162/003465302317411604', 'Ravn and Uhlig (2002)', 'Ravn și Uhlig (2002)',
           r'Ravn, M. O., \& Uhlig, H. (2002). On adjusting the Hodrick--Prescott filter for the frequency of observations. \textit{Review of Economics and Statistics}, 84(2), 371--376.'),
    'RS': ('10.1109/78.365298', 'Riedel and Sidorenko (1995)', 'Riedel și Sidorenko (1995)',
           r'Riedel, K. S., \& Sidorenko, A. (1995). Minimum bias multiple taper spectral estimation. \textit{IEEE Transactions on Signal Processing}, 43(1), 188--195.'),
    'RN': ('10.1016/j.jempfin.2009.02.002', 'Rua and Nunes (2009)', 'Rua și Nunes (2009)',
           r'Rua, A., \& Nunes, L. C. (2009). International comovement of stock market returns: A wavelet analysis. \textit{Journal of Empirical Finance}, 16(4), 632--639.'),
    'Sch': ('10.5194/npg-23-45-2016', 'Schulte (2016)', 'Schulte (2016)',
            r'Schulte, J. A. (2016). Cumulative areawise testing in wavelet analysis and its application to geophysical time series. \textit{Nonlinear Processes in Geophysics}, 23(1), 45--57.'),
    'SS': ('10.1007/978-3-319-52452-8', 'Shumway and Stoffer (2017)', 'Shumway și Stoffer (2017)',
           r'Shumway, R. H., \& Stoffer, D. S. (2017). \textit{Time Series Analysis and Its Applications: With R Examples} (4th ed.). Springer.'),
    'Tho': ('10.1109/PROC.1982.12433', 'Thomson (1982)', 'Thomson (1982)',
            r'Thomson, D. J. (1982). Spectrum estimation and harmonic analysis. \textit{Proceedings of the IEEE}, 70(9), 1055--1096.'),
    'TC': ('10.1175/1520-0477(1998)079<0061:APGTWA>2.0.CO;2', 'Torrence and Compo (1998)', 'Torrence și Compo (1998)',
           r'Torrence, C., \& Compo, G. P. (1998). A practical guide to wavelet analysis. \textit{Bulletin of the American Meteorological Society}, 79(1), 61--78.'),
    'TW': ('10.1175/1520-0442(1999)012<2679:ICITEM>2.0.CO;2', 'Torrence and Webster (1999)', 'Torrence și Webster (1999)',
           r'Torrence, C., \& Webster, P. J. (1999). Interdecadal changes in the ENSO--monsoon system. \textit{Journal of Climate}, 12(8), 2679--2690.'),
    'VB': ('10.1016/j.eneco.2011.10.007', 'Vacha and Barunik (2012)', 'Vacha și Barunik (2012)',
           r'Vacha, L., \& Barunik, J. (2012). Co-movement of energy commodities revisited: Evidence from wavelet coherence analysis. \textit{Energy Economics}, 34(1), 241--247.'),
    'VG': ('10.1016/0167-2789(89)90077-8', 'Vautard and Ghil (1989)', 'Vautard și Ghil (1989)',
           r'Vautard, R., \& Ghil, M. (1989). Singular spectrum analysis in nonlinear dynamics, with applications to paleoclimatic time series. \textit{Physica D}, 35(3), 395--424.'),
    'Wel': ('10.1109/TAU.1967.1161901', 'Welch (1967)', 'Welch (1967)',
            r'Welch, P. D. (1967). The use of fast Fourier transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms. \textit{IEEE Transactions on Audio and Electroacoustics}, 15(2), 70--73.'),
    'WGP': ('10.1029/2000JD900110', 'Whitcher, Guttorp and Percival (2000)', 'Whitcher, Guttorp și Percival (2000)',
            r'Whitcher, B., Guttorp, P., \& Percival, D. B. (2000). Wavelet analysis of covariance with application to atmospheric time series. \textit{Journal of Geophysical Research: Atmospheres}, 105(D11), 14941--14962.'),
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
