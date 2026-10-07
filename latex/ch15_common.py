r"""
ch15_common.py -- shared helpers of the Chapter 15 generators (lecture and seminar), ATS
======================================================================================
Bilingual text T(en, ro); numbers of the new material from Quantlets/Ch_15/ch15_numbers.json (generate_all_charts.py)
and sem15_results.json (seminar15.py); the numbers quoted in the chapter recaps are read from the numbers files of
Chapters 0-14 and 16 (Quantlets/Ch_NN/chN_numbers.json) and rounded exactly as in the chapter decks, so the review
and the chapters show the same values. Published values that the chapters compare with (cited from the papers) are
in PUBLISHED. Citations: DOIs checked against Crossref, arXiv identifiers against the arXiv API (6 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_15')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_15'
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


def minus_fix(V):
    """Negative numbers: a real minus sign in text and in math mode."""
    for k, v in list(V.items()):
        if isinstance(v, str) and v.startswith('⁅-'):
            V[k] = '⁅\\ensuremath{-}' + v[2:]


def load():
    with open(os.path.join(QL, 'ch15_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem15_results.json')) as f:
        return json.load(f)


def chapter_json(k):
    """The numbers file of Chapter k (None if the chapter has not written one)."""
    p = os.path.join(ROOT, 'Quantlets', f'Ch_{k:02d}', f'ch{k}_numbers.json')
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


# =============================================================================
# PUBLISHED VALUES QUOTED IN THE CHAPTERS (cited from the papers, as on the chapter slides)
# =============================================================================
PUBLISHED = {
    'hansen_gamma': 0.302,        # Hansen (1997), TAR threshold for US unemployment (Chapter 2)
    'tps_p': 0.002,               # Taylor, Peel and Sarno (2001), p-value of the ESTAR t-ratio (Chapter 2)
    'bgr_small': 1.14, 'bgr_medium': 0.54, 'bgr_large': 0.46,   # Banbura et al. (2010), Table 1, employment, h = 1
    'pzc_loss': 0.853,            # Patton, Ziegel and Chen (2019), GAS-1F FZ0 loss at 5% (Chapter 9)
    'pzc_gof_var': 0.242, 'pzc_gof_es': 0.313,   # their goodness-of-fit p-values for GAS-1F
    'brexit_gap': 2.4,            # Born et al. (2019), output loss of the UK by 2018Q4, % (Chapter 14)
}


def facts(V):
    """Put the recap numbers of every chapter into V (keys cN.*), with the rounding of the chapter decks."""
    P = V.put

    def pv(key, x, d=3):
        V.raw(key, '$<$' + n(10 ** (-d), d) if x < 10 ** (-d) else n(x, d))

    for k, v in PUBLISHED.items():
        P('pub.' + k, v, 1 if k == 'brexit_gap' else (2 if k.startswith('bgr') else 3))
    # ---------------------------------------------------------------- Chapter 0
    N = chapter_json(0)
    mc = N['mc']['res']
    P('c0.naive1', 100 * mc['100']['0.9']['naive'], 1)
    P('c0.naive4', 100 * mc['400']['0.9']['naive'], 1)
    P('c0.ewc', 100 * mc['100']['0.9']['ewc'], 1)
    P('c0.llsw', 100 * mc['100']['0.9']['llsw'], 1)
    ts = N['ts']
    P('c0.b1', ts['b1'], 2)
    P('c0.tcl', ts['t_classic'], 2)
    P('c0.tll', ts['t_ll'], 2)
    P('c0.cvll', ts['cv_ll'], 2)
    P('c0.early', ts['sub']['early']['b'], 2)
    P('c0.late', ts['sub']['late']['b'], 2)
    P('c0.tearly', ts['sub']['early']['t'], 1)
    P('c0.tlate', ts['sub']['late']['t'], 1)
    rc = N['rc']
    P('c0.rct', rc['2000-2012']['t_best'], 2)
    P('c0.rcpn', rc['2000-2012']['p_naive'], 3)
    P('c0.rcp', rc['2000-2012']['p_rc'], 2)
    P('c0.rcp2', rc['2013-2026']['p_rc'], 2)
    P('c0.snoop20', 100 * N['snoop']['indep']['20'], 0)
    # ---------------------------------------------------------------- Chapter 1
    N = chapter_json(1)
    P('c1.ar', N['fx']['AR(1)']['rel_rmse'], 3)
    P('c1.drift', N['fx']['drift']['rel_rmse'], 3)
    pv('c1.cwp', N['fx']['drift']['cw']['p'])
    P('c1.ao', N['ao']['ratio'], 2)
    pv('c1.aop', N['ao']['dm']['p_hln'])
    P('c1.med', N['spf']['rel']['median'], 3)
    P('c1.prev', N['spf']['rel']['previous best'], 3)
    pv('c1.prevp', N['spf']['dm_previous best']['p_hln'])
    P('c1.dm', 100 * N['dmsize']['8_16']['dm'], 1)
    P('c1.hln', 100 * N['dmsize']['8_16']['hln'], 1)
    # ---------------------------------------------------------------- Chapter 2
    N = chapter_json(2)
    P('c2.chow0', 100 * N['chow']['chosen'][0], 0)
    P('c2.chow1', 100 * N['chow']['chosen'][-1], 0)
    P('c2.supcv', N['chow']['cv']['sup']['1'][1], 2)
    P('c2.mpq', N['mpq']['paper']['var']['sup'], 1)
    V.raw('c2.mpqd', N['mpq']['paper']['date_var'])
    P('c2.mpqx', N['mpq']['ext']['var']['sup'], 1)
    P('c2.mpqr', N['mpq']['paper']['ratio_var'], 1)
    P('c2.mpqrx', N['mpq']['ext']['ratio_var'], 1)
    P('c2.gam', N['tar']['gamma'], 3)
    P('c2.tpsp', N['estar']['p_mc'], 3)
    V.raw('c2.bpm', str(N['bp']['m_seq']))
    # ---------------------------------------------------------------- Chapter 3
    N = chapter_json(3)
    P('c3.ip', N['cee']['ip_min'], 2)
    V.raw('c3.ipm', str(N['cee']['ip_argmin']))
    P('c3.pmax', N['cee']['p_max'], 3)
    P('c3.gkF', N['gk']['F'], 1)
    P('c3.ebp', N['gk']['ebp0'], 2)
    P('c3.k1', 100 * N['kilian']['fevd_p60'][0], 0)
    P('c3.k2', 100 * N['kilian']['fevd_p60'][1], 0)
    P('c3.k3', 100 * N['kilian']['fevd_p60'][2], 0)
    P('c3.vb', abs(N['lpsim']['VAR(2)_bias_8']), 2)
    P('c3.lb', abs(N['lpsim']['LP(2)_bias_8']), 2)
    # ---------------------------------------------------------------- Chapter 4
    N = chapter_json(4)
    P('c4.kplr', N['kpsw']['lr'], 1)
    pv('c4.kpp', N['kpsw']['plr'])
    P('c4.thl', N['pt']['theta_l'], 2)
    pv('c4.bo4', N['pt']['boot4'][0])
    P('c4.sa', 100 * N['size']['iid']['50'][0], 1)
    P('c4.sw', 100 * N['size']['iid']['50'][2], 1)
    P('c4.pmg', N['panel']['pmg']['theta'][0], 2)
    pv('c4.pH', N['panel']['pH'])
    # ---------------------------------------------------------------- Chapter 5
    N = chapter_json(5)
    P('c5.s', N['bgr']['eval1']['OLS SMALL|USPRIV|1'], 2)
    P('c5.m', N['bgr']['eval1']['BGR MEDIUM|USPRIV|1'], 2)
    P('c5.l', N['bgr']['eval1']['BGR LARGE|USPRIV|1'], 2)
    P('c5.x', N['bgr']['eval2']['BGR MEDIUM|USPRIV|12'], 2)
    P('c5.di1', N['di']['eval1']['INDPRO|12|DI'], 2)
    P('c5.di2', N['di']['pre2020']['INDPRO|12|DI'], 2)
    P('c5.dmt', N['nowcast']['dm_t'], 2)
    P('c5.dmp', N['nowcast']['dm_p'], 2)
    # ---------------------------------------------------------------- Chapter 6
    N = chapter_json(6)
    P('c6.rho', N['mnz']['ur']['par'][5], 3)
    P('c6.corr', N['mnz']['corr_ur_bn'], 3)
    P('c6.sd0', N['mnz']['sd_c0'], 2)
    P('c6.sd1', N['mnz']['sd_c1'], 2)
    P('c6.pu', 100 * N['pileup']['0.0']['zero'], 0)
    P('c6.dll', N['pf']['ll_sv'] - N['pf']['ll_garch'], 1)
    # ---------------------------------------------------------------- Chapter 7
    N = chapter_json(7)
    P('c7.ll', N['hamilton']['paper']['loglik'], 2)
    P('c7.qps', N['hamilton']['qps_paper'], 3)
    P('c7.p01', N['hamilton']['today']['p2001max'], 2)
    P('c7.p08', N['hamilton']['today']['p2008'], 2)
    P('c7.LR', N['lrtest']['LR'], 1)
    P('c7.q95', N['lrtest']['q95'], 2)
    P('c7.c2', N['lrtest']['c2'], 2)
    # ---------------------------------------------------------------- Chapter 8
    N = chapter_json(8)
    P('c8.qb', N['haroos']['btc']['harq']['qlike'], 3)
    P('c8.qe', N['haroos']['eth']['harq']['qlike'], 3)
    P('c8.gs', N['gmv']['sd']['sample'], 2)
    P('c8.gnl', N['gmv']['sd']['NL shrinkage'], 2)
    P('c8.gd', N['gmv']['sd']['DCC'], 2)
    P('c8.gdnl', N['gmv']['sd']['DCC-NL'], 2)
    ip, rv = N['midas']['ip'], N['midas']['rv']
    P('c8.ipt', ip['theta'][3] / ip['se'][3], 2)
    P('c8.ipvr', 100 * ip['vr'], 1)
    P('c8.rvt', rv['theta'][3] / rv['se'][3], 2)
    P('c8.rvvr', 100 * rv['vr'], 1)
    P('c8.hc', 100 * N['qmle_sim']['t5']['h'][1], 1)
    P('c8.bw', 100 * N['qmle_sim']['t5']['bw'][1], 1)
    # ---------------------------------------------------------------- Chapter 9
    N = chapter_json(9)
    P('c9.loss', N['pzcrep']['0.05']['loss']['FZ-1F'], 3)
    pv('c9.gv', N['pzcrep']['0.05']['gof']['FZ-1F'][0])
    pv('c9.ge', N['pzcrep']['0.05']['gof']['FZ-1F'][1])
    pv('c9.ig', N['caviar']['IG']['dq_out'][1])
    pv('c9.sav', N['caviar']['SAV']['dq_out'][1])
    P('c9.gn', 100 * N['riskratio']['sp500']['hits']['GARCH-N'], 1)
    # ---------------------------------------------------------------- Chapter 10
    N = chapter_json(10)
    P('c10.H', N['gjr']['H'], 3)
    P('c10.H1', N['gjr']['sub']['2000-2010'], 3)
    P('c10.H2', N['gjr']['sub']['2011-2022'], 3)
    P('c10.W', N['qu']['W_spx'], 2)
    P('c10.rq', N['forecast']['.SPX']['eval']['5']['rfsv']['rel_q'], 3)
    P('c10.rqp', N['forecast']['.SPX']['eval']['5']['rfsv']['dm_q'][1], 2)
    # ---------------------------------------------------------------- Chapter 11
    N = chapter_json(11)
    P('c11.cn', N['cn']['p_th'], 1)
    P('c11.cny', N['cn']['p_th'] / 4, 1)
    P('c11.cnmc', N['cn']['p_mc'], 1)
    P('c11.hpc', N['endpoint']['corr_hp'], 2)
    P('c11.hps', 100 * N['endpoint']['sign_hp'], 0)
    P('c11.wo', 100 * N['wtc_dax']['share_obs'], 0)
    P('c11.wq', 100 * N['wtc_dax']['null_q95'], 1)
    # ---------------------------------------------------------------- Chapter 12
    N = chapter_json(12)
    c = N['cv']['AR(3)']['AR(3)']
    P('c12.cv', c['5-fold CV']['mapae'], 3)
    P('c12.oos', c['OOS']['mapae'], 3)
    P('c12.lk', N['leakage']['random 5-fold']['med'], 2)
    z = N['zeng']['res']['96']
    P('c12.pt', z['Transformer, point tokens']['mse'], 3)
    P('c12.dl', z['DLinear']['mse'], 3)
    P('c12.patch', z['Transformer']['mse'], 3)
    P('c12.owa', N['m4']['scores']['N-BEATS']['owa'], 3)
    # ---------------------------------------------------------------- Chapter 13
    N = chapter_json(13)
    P('c13.st', N['aci']['sp500']['static']['cov'], 3)
    P('c13.aci', N['aci']['sp500']['aci']['cov'], 3)
    P('c13.raw', N['cqr']['raw']['cov'], 3)
    P('c13.cqr', N['cqr']['cqr']['cov'], 3)
    P('c13.c2', N['load']['mae']['Chronos-2'], 3)
    P('c13.arx', N['load']['mae']['expert ARX'], 3)
    V.raw('c13.neg', str(N['multiple']['neg']))
    V.raw('c13.holm', str(N['multiple']['rej_holm']))
    # ---------------------------------------------------------------- Chapter 14 (built in parallel: guarded)
    N = chapter_json(14)
    ok14 = False
    try:
        P('c14.ge', abs(N['germany']['avg_post']), 0)
        P('c14.gerel', 100 * abs(N['germany']['rel_post']), 1)
        P('c14.gp', N['germany_placebo']['p'], 3)
        P('c14.bx', abs(N['brexit']['gap2018']), 1)
        V.raw('c14.rk', str(N['brexit']['rank_uk']))
        V.raw('c14.nu', str(N['brexit']['n_units']))
        three = [N['ro_sc']['est'][k]['avg'] for k in ('demeaned SC', 'augmented SC', 'SDID')]
        P('c14.lo', min(three), 1)
        P('c14.hi', max(three), 1)
        P('c14.sc', N['ro_sc']['est']['SC']['avg'], 2)
        P('c14.rp', N['ro_placebo']['p'], 3)
        ok14 = True
    except (TypeError, KeyError):
        pass
    # ---------------------------------------------------------------- Chapter 16
    N = chapter_json(16)
    e = N['episodes']
    for k in ('sp500', 'ndx', 'ssec'):
        P(f'c16.{k}.g', e[k]['gsadf'], 2)
        P(f'c16.{k}.mc', e[k]['cv_mc'], 2)
        P(f'c16.{k}.w', e[k]['cv_wild'], 2)
    P('c16.hg', N['housing']['us_ratio']['gsadf'], 2)
    P('c16.hcv', N['housing']['us_ratio']['cv'], 2)
    P('c16.szmc', 100 * N['size']['rates']['up']['rej_mc'], 1)
    P('c16.szw', 100 * N['size']['rates']['up']['rej_wild'], 1)
    P('c16.ep', 100 * N['size']['rates']['iid']['ep_mc'], 1)
    minus_fix(V)
    return ok14


# =============================================================================
# CITATIONS
# =============================================================================
def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
AX = 'https://arxiv.org/abs/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    # ------------------------------------------------ landmark papers replicated in the chapters
    'NW': ('10.2307/1913610', 'Newey and West (1987)', 'Newey și West (1987)',
           r'Newey, W. K., \& West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. \textit{Econometrica}, 55(3), 703--708.'),
    'EH': ('10.1111/j.1540-6261.1991.tb02674.x', 'Estrella and Hardouvelis (1991)', 'Estrella și Hardouvelis (1991)',
           r'Estrella, A., \& Hardouvelis, G. A. (1991). The term structure as a predictor of real economic activity. \textit{The Journal of Finance}, 46(2), 555--576.'),
    'White': ('10.1111/1468-0262.00152', 'White (2000)', 'White (2000)',
              r'White, H. (2000). A reality check for data snooping. \textit{Econometrica}, 68(5), 1097--1126.'),
    'MR': ('10.1016/0022-1996(83)90017-X', 'Meese and Rogoff (1983)', 'Meese și Rogoff (1983)',
           r'Meese, R. A., \& Rogoff, K. (1983). Empirical exchange rate models of the seventies: Do they fit out of sample? \textit{Journal of International Economics}, 14(1--2), 3--24.'),
    'GKMT': ('10.1016/j.ijforecast.2012.06.004', 'Genre et al.\\ (2013)', 'Genre et al.\\ (2013)',
             r'Genre, V., Kenny, G., Meyler, A., \& Timmermann, A. (2013). Combining expert forecasts: Can anything beat the simple average? \textit{International Journal of Forecasting}, 29(1), 108--121.'),
    'AO': ('10.21034/qr.2511', 'Atkeson and Ohanian (2001)', 'Atkeson și Ohanian (2001)',
           r'Atkeson, A., \& Ohanian, L. E. (2001). Are Phillips curves useful for forecasting inflation? \textit{Federal Reserve Bank of Minneapolis Quarterly Review}, 25(1), 2--11.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'HLN': ('10.1016/S0169-2070(96)00719-4', 'Harvey, Leybourne and Newbold (1997)', 'Harvey, Leybourne și Newbold (1997)',
            r'Harvey, D., Leybourne, S., \& Newbold, P. (1997). Testing the equality of prediction mean squared errors. \textit{International Journal of Forecasting}, 13(2), 281--291.'),
    'CW': ('10.1016/j.jeconom.2006.05.023', 'Clark and West (2007)', 'Clark și West (2007)',
           r'Clark, T. E., \& West, K. D. (2007). Approximately normal tests for equal predictive accuracy in nested models. \textit{Journal of Econometrics}, 138(1), 291--311.'),
    'MPQ': ('10.1257/aer.90.5.1464', 'McConnell and Perez-Quiros (2000)', 'McConnell și Perez-Quiros (2000)',
            r"McConnell, M. M., \& Perez-Quiros, G. (2000). Output fluctuations in the United States: What has changed since the early 1980's? \textit{American Economic Review}, 90(5), 1464--1476."),
    'BP': ('10.1002/jae.659', 'Bai and Perron (2003)', 'Bai și Perron (2003)',
           r'Bai, J., \& Perron, P. (2003). Computation and analysis of multiple structural change models. \textit{Journal of Applied Econometrics}, 18(1), 1--22.'),
    'HanB': ('10.2202/1558-3708.1024', 'Hansen (1997)', 'Hansen (1997)',
             r'Hansen, B. E. (1997). Inference in TAR models. \textit{Studies in Nonlinear Dynamics \& Econometrics}, 2(1), 1--14.'),
    'TPS': ('10.1111/1468-2354.00144', 'Taylor, Peel and Sarno (2001)', 'Taylor, Peel și Sarno (2001)',
            r'Taylor, M. P., Peel, D. A., \& Sarno, L. (2001). Nonlinear mean-reversion in real exchange rates: Toward a solution to the purchasing power parity puzzles. \textit{International Economic Review}, 42(4), 1015--1042.'),
    'CEE': ('10.1016/S1574-0048(99)01005-8', 'Christiano, Eichenbaum and Evans (1999)', 'Christiano, Eichenbaum și Evans (1999)',
            r'Christiano, L. J., Eichenbaum, M., \& Evans, C. L. (1999). Monetary policy shocks: What have we learned and to what end? In J. B. Taylor \& M. Woodford (Eds.), \textit{Handbook of Macroeconomics}, Vol.\ 1A, 65--148. Elsevier.'),
    'GK': ('10.1257/mac.20130329', 'Gertler and Karadi (2015)', 'Gertler și Karadi (2015)',
           r'Gertler, M., \& Karadi, P. (2015). Monetary policy surprises, credit costs, and economic activity. \textit{American Economic Journal: Macroeconomics}, 7(1), 44--76.'),
    'Kil': ('10.1257/aer.99.3.1053', 'Kilian (2009)', 'Kilian (2009)',
            r'Kilian, L. (2009). Not all oil price shocks are alike: Disentangling demand and supply shocks in the crude oil market. \textit{American Economic Review}, 99(3), 1053--1069.'),
    'KPSW': ('https://www.jstor.org/stable/2006644', 'King, Plosser, Stock and Watson (1991)', 'King, Plosser, Stock și Watson (1991)',
             r'King, R. G., Plosser, C. I., Stock, J. H., \& Watson, M. W. (1991). Stochastic trends and economic fluctuations. \textit{American Economic Review}, 81(4), 819--840.'),
    'PSS': ('10.1080/01621459.1999.10474156', 'Pesaran, Shin and Smith (1999)', 'Pesaran, Shin și Smith (1999)',
            r'Pesaran, M. H., Shin, Y., \& Smith, R. P. (1999). Pooled mean group estimation of dynamic heterogeneous panels. \textit{Journal of the American Statistical Association}, 94(446), 621--634.'),
    'BGR': ('10.1002/jae.1137', 'Bańbura, Giannone and Reichlin (2010)', 'Bańbura, Giannone și Reichlin (2010)',
            r'Bańbura, M., Giannone, D., \& Reichlin, L. (2010). Large Bayesian vector auto regressions. \textit{Journal of Applied Econometrics}, 25(1), 71--92.'),
    'SW': ('10.1198/073500102317351921', 'Stock and Watson (2002)', 'Stock și Watson (2002)',
           r'Stock, J. H., \& Watson, M. W. (2002). Macroeconomic forecasting using diffusion indexes. \textit{Journal of Business \& Economic Statistics}, 20(2), 147--162.'),
    'MNZ': ('10.1162/003465303765299765', 'Morley, Nelson and Zivot (2003)', 'Morley, Nelson și Zivot (2003)',
            r'Morley, J. C., Nelson, C. R., \& Zivot, E. (2003). Why are the Beveridge--Nelson and unobserved-components decompositions of GDP so different? \textit{Review of Economics and Statistics}, 85(2), 235--243.'),
    'Ham': ('10.2307/1912559', 'Hamilton (1989)', 'Hamilton (1989)',
            r'Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. \textit{Econometrica}, 57(2), 357--384.'),
    'EGS': ('10.1162/REST_a_00300', 'Engle, Ghysels and Sohn (2013)', 'Engle, Ghysels și Sohn (2013)',
            r'Engle, R. F., Ghysels, E., \& Sohn, B. (2013). Stock market volatility and macroeconomic fundamentals. \textit{Review of Economics and Statistics}, 95(3), 776--797.'),
    'BPQ': ('10.1016/j.jeconom.2015.10.007', 'Bollerslev, Patton and Quaedvlieg (2016)', 'Bollerslev, Patton și Quaedvlieg (2016)',
            r'Bollerslev, T., Patton, A. J., \& Quaedvlieg, R. (2016). Exploiting the errors: A simple approach for improved volatility forecasting. \textit{Journal of Econometrics}, 192(1), 1--18.'),
    'ELW': ('10.1080/07350015.2017.1345683', 'Engle, Ledoit and Wolf (2019)', 'Engle, Ledoit și Wolf (2019)',
            r'Engle, R. F., Ledoit, O., \& Wolf, M. (2019). Large dynamic covariance matrices. \textit{Journal of Business \& Economic Statistics}, 37(2), 363--375.'),
    'PZC': ('10.1016/j.jeconom.2018.10.008', 'Patton, Ziegel and Chen (2019)', 'Patton, Ziegel și Chen (2019)',
            r'Patton, A. J., Ziegel, J. F., \& Chen, R. (2019). Dynamic semiparametric models for expected shortfall (and Value-at-Risk). \textit{Journal of Econometrics}, 211(2), 388--413.'),
    'EM': ('10.1198/073500104000000370', 'Engle and Manganelli (2004)', 'Engle și Manganelli (2004)',
           r'Engle, R. F., \& Manganelli, S. (2004). CAViaR: Conditional autoregressive value at risk by regression quantiles. \textit{Journal of Business \& Economic Statistics}, 22(4), 367--381.'),
    'GJR': ('10.1080/14697688.2017.1393551', 'Gatheral, Jaisson and Rosenbaum (2018)', 'Gatheral, Jaisson și Rosenbaum (2018)',
            r'Gatheral, J., Jaisson, T., \& Rosenbaum, M. (2018). Volatility is rough. \textit{Quantitative Finance}, 18(6), 933--949.'),
    'Qu': ('10.1198/jbes.2010.09153', 'Qu (2011)', 'Qu (2011)',
           r'Qu, Z. (2011). A test against spurious long memory. \textit{Journal of Business \& Economic Statistics}, 29(3), 423--438.'),
    'CN': ('10.1016/0165-1889(93)00781-X', 'Cogley and Nason (1995)', 'Cogley și Nason (1995)',
           r'Cogley, T., \& Nason, J. M. (1995). Effects of the Hodrick--Prescott filter on trend and difference stationary time series: Implications for business cycle research. \textit{Journal of Economic Dynamics and Control}, 19(1--2), 253--278.'),
    'HamB': ('10.1162/rest_a_00706', 'Hamilton (2018)', 'Hamilton (2018)',
             r'Hamilton, J. D. (2018). Why you should never use the Hodrick--Prescott filter. \textit{Review of Economics and Statistics}, 100(5), 831--843.'),
    'BHK': ('10.1016/j.csda.2017.11.003', 'Bergmeir, Hyndman and Koo (2018)', 'Bergmeir, Hyndman și Koo (2018)',
            r'Bergmeir, C., Hyndman, R. J., \& Koo, B. (2018). A note on the validity of cross-validation for evaluating autoregressive time series prediction. \textit{Computational Statistics \& Data Analysis}, 120, 70--83.'),
    'Zeng': ('10.1609/aaai.v37i9.26317', 'Zeng et al.\\ (2023)', 'Zeng et al.\\ (2023)',
             r'Zeng, A., Chen, M., Zhang, L., \& Xu, Q. (2023). Are Transformers effective for time series forecasting? \textit{Proceedings of the AAAI Conference on Artificial Intelligence}, 37(9), 11121--11128.'),
    'Nie': (AX + '2211.14730', 'Nie et al.\\ (2023)', 'Nie et al.\\ (2023)',
            r'Nie, Y., Nguyen, N. H., Sinthong, P., \& Kalagnanam, J. (2023). A time series is worth 64 words: Long-term forecasting with Transformers. \textit{International Conference on Learning Representations}; \textit{arXiv:2211.14730}.'),
    'GC': (AX + '2106.00170', 'Gibbs and Candès (2021)', 'Gibbs și Candès (2021)',
           r'Gibbs, I., \& Candès, E. (2021). Adaptive conformal inference under distribution shift. \textit{Advances in Neural Information Processing Systems 34}; \textit{arXiv:2106.00170}.'),
    'RPC': (AX + '1905.03222', 'Romano, Patterson and Candès (2019)', 'Romano, Patterson și Candès (2019)',
            r'Romano, Y., Patterson, E., \& Candès, E. (2019). Conformalized quantile regression. \textit{Advances in Neural Information Processing Systems 32}; \textit{arXiv:1905.03222}.'),
    'ADH': ('10.1111/ajps.12116', 'Abadie, Diamond and Hainmueller (2015)', 'Abadie, Diamond și Hainmueller (2015)',
            r'Abadie, A., Diamond, A., \& Hainmueller, J. (2015). Comparative politics and the synthetic control method. \textit{American Journal of Political Science}, 59(2), 495--510.'),
    'BMSS': ('10.1093/ej/uez020', 'Born et al.\\ (2019)', 'Born et al.\\ (2019)',
             r'Born, B., Müller, G. J., Schularick, M., \& Sedláček, P. (2019). The costs of economic nationalism: Evidence from the Brexit experiment. \textit{The Economic Journal}, 129(623), 2722--2744.'),
    'PWY': ('10.1111/j.1468-2354.2010.00625.x', 'Phillips, Wu and Yu (2011)', 'Phillips, Wu și Yu (2011)',
            r'Phillips, P. C. B., Wu, Y., \& Yu, J. (2011). Explosive behavior in the 1990s Nasdaq: When did exuberance escalate asset values? \textit{International Economic Review}, 52(1), 201--226.'),
    'PSY': ('10.1111/iere.12132', 'Phillips, Shi and Yu (2015)', 'Phillips, Shi și Yu (2015)',
            r'Phillips, P. C. B., Shi, S., \& Yu, J. (2015). Testing for multiple bubbles: Historical episodes of exuberance and collapse in the S\&P 500. \textit{International Economic Review}, 56(4), 1043--1078.'),
    'PY': ('10.3982/QE82', 'Phillips and Yu (2011)', 'Phillips și Yu (2011)',
           r'Phillips, P. C. B., \& Yu, J. (2011). Dating the timeline of financial bubbles during the subprime crisis. \textit{Quantitative Economics}, 2(3), 455--491.'),
    'HLST': ('10.1016/j.jempfin.2015.09.002', 'Harvey et al.\\ (2016)', 'Harvey et al.\\ (2016)',
             r'Harvey, D. I., Leybourne, S. J., Sollis, R., \& Taylor, A. M. R. (2016). Tests for explosive financial bubbles in the presence of non-stationary volatility. \textit{Journal of Empirical Finance}, 38, 548--574.'),
    # ------------------------------------------------ inference, testing and research practice
    'Holm': ('https://www.jstor.org/stable/4615733', 'Holm (1979)', 'Holm (1979)',
             r'Holm, S. (1979). A simple sequentially rejective multiple test procedure. \textit{Scandinavian Journal of Statistics}, 6(2), 65--70.'),
    'Hansen': ('10.1198/073500105000000063', 'Hansen (2005)', 'Hansen (2005)',
               r'Hansen, P. R. (2005). A test for superior predictive ability. \textit{Journal of Business \& Economic Statistics}, 23(4), 365--380.'),
    'HLNa': ('10.3982/ECTA5771', 'Hansen, Lunde and Nason (2011)', 'Hansen, Lunde și Nason (2011)',
             r'Hansen, P. R., Lunde, A., \& Nason, J. M. (2011). The model confidence set. \textit{Econometrica}, 79(2), 453--497.'),
    'RW': ('10.1111/j.1468-0262.2005.00615.x', 'Romano and Wolf (2005)', 'Romano și Wolf (2005)',
           r'Romano, J. P., \& Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. \textit{Econometrica}, 73(4), 1237--1282.'),
    'KV': ('10.1017/S0266466605050565', 'Kiefer and Vogelsang (2005)', 'Kiefer și Vogelsang (2005)',
           r'Kiefer, N. M., \& Vogelsang, T. J. (2005). A new asymptotic theory for heteroskedasticity-autocorrelation robust tests. \textit{Econometric Theory}, 21(6), 1130--1164.'),
    'LLSW': ('10.1080/07350015.2018.1506926', 'Lazarus et al.\\ (2018)', 'Lazarus et al.\\ (2018)',
             r'Lazarus, E., Lewis, D. J., Stock, J. H., \& Watson, M. W. (2018). HAR inference: Recommendations for practice. \textit{Journal of Business \& Economic Statistics}, 36(4), 541--559.'),
    'IK': ('10.1081/ETC-200040785', 'Inoue and Kilian (2005)', 'Inoue și Kilian (2005)',
           r'Inoue, A., \& Kilian, L. (2005). In-sample or out-of-sample tests of predictability: Which one should we use? \textit{Econometric Reviews}, 23(4), 371--402.'),
    'Diebold': ('10.1080/07350015.2014.983236', 'Diebold (2015)', 'Diebold (2015)',
                r'Diebold, F. X. (2015). Comparing predictive accuracy, twenty years later: A personal perspective on the use and abuse of Diebold--Mariano tests. \textit{Journal of Business \& Economic Statistics}, 33(1), 1--9.'),
    'Stam': ('10.1016/S0304-405X(99)00041-0', 'Stambaugh (1999)', 'Stambaugh (1999)',
             r'Stambaugh, R. F. (1999). Predictive regressions. \textit{Journal of Financial Economics}, 54(3), 375--421.'),
    'WG': ('10.1093/rfs/hhm014', 'Welch and Goyal (2008)', 'Welch și Goyal (2008)',
           r'Welch, I., \& Goyal, A. (2008). A comprehensive look at the empirical performance of equity premium prediction. \textit{Review of Financial Studies}, 21(4), 1455--1508.'),
    'SNS': ('10.1177/0956797611417632', 'Simmons, Nelson and Simonsohn (2011)', 'Simmons, Nelson și Simonsohn (2011)',
            r'Simmons, J. P., Nelson, L. D., \& Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. \textit{Psychological Science}, 22(11), 1359--1366.'),
    'GL': ('10.1511/2014.111.460', 'Gelman and Loken (2014)', 'Gelman și Loken (2014)',
           r'Gelman, A., \& Loken, E. (2014). The statistical crisis in science. \textit{American Scientist}, 102(6), 460--465.'),
    'HLZ': ('10.1093/rfs/hhv059', 'Harvey, Liu and Zhu (2016)', 'Harvey, Liu și Zhu (2016)',
            r'Harvey, C. R., Liu, Y., \& Zhu, H. (2016). \ldots\ and the cross-section of expected returns. \textit{Review of Financial Studies}, 29(1), 5--68.'),
    'Ioa': ('10.1371/journal.pmed.0020124', 'Ioannidis (2005)', 'Ioannidis (2005)',
            r'Ioannidis, J. P. A. (2005). Why most published research findings are false. \textit{PLoS Medicine}, 2(8), e124.'),
    'BLSZ': ('10.1257/app.20150044', 'Brodeur et al.\\ (2016)', 'Brodeur et al.\\ (2016)',
             r'Brodeur, A., Lé, M., Sangnier, M., \& Zylberberg, Y. (2016). Star wars: The empirics strike back. \textit{American Economic Journal: Applied Economics}, 8(1), 1--32.'),
    'Nos': ('10.1073/pnas.1708274114', 'Nosek et al.\\ (2018)', 'Nosek et al.\\ (2018)',
            r'Nosek, B. A., Ebersole, C. R., DeHaven, A. C., \& Mellor, D. T. (2018). The preregistration revolution. \textit{Proceedings of the National Academy of Sciences}, 115(11), 2600--2606.'),
    'Kau': ('10.1145/2382577.2382579', 'Kaufman et al.\\ (2012)', 'Kaufman et al.\\ (2012)',
            r'Kaufman, S., Rosset, S., Perlich, C., \& Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. \textit{ACM Transactions on Knowledge Discovery from Data}, 6(4), 15.'),
    'Cle': ('10.1111/joes.12139', 'Clemens (2017)', 'Clemens (2017)',
            r'Clemens, M. A. (2017). The meaning of failed replications: A review and proposal. \textit{Journal of Economic Surveys}, 31(1), 326--342.'),
    'CM': ('10.1257/jel.20171350', 'Christensen and Miguel (2018)', 'Christensen și Miguel (2018)',
           r'Christensen, G., \& Miguel, E. (2018). Transparency, reproducibility, and the credibility of economics research. \textit{Journal of Economic Literature}, 56(3), 920--980.'),
    'Vil': ('10.1162/99608f92.4f6b9e67', 'Vilhuber (2020)', 'Vilhuber (2020)',
            r'Vilhuber, L. (2020). Reproducibility and replicability in economics. \textit{Harvard Data Science Review}, 2(4).'),
    'CL': ('10.1561/104.00000053', 'Chang and Li (2022)', 'Chang și Li (2022)',
           r"Chang, A. C., \& Li, P. (2022). Is economics research replicable? Sixty published papers from thirteen journals say ``often not''. \textit{Critical Finance Review}, 11(1), 185--206."),
    'HAP': ('10.1093/cje/bet075', 'Herndon, Ash and Pollin (2014)', 'Herndon, Ash și Pollin (2014)',
            r'Herndon, T., Ash, M., \& Pollin, R. (2014). Does high public debt consistently stifle economic growth? A critique of Reinhart and Rogoff. \textit{Cambridge Journal of Economics}, 38(2), 257--279.'),
    'HXZ': ('10.1093/rfs/hhy131', 'Hou, Xue and Zhang (2020)', 'Hou, Xue și Zhang (2020)',
            r'Hou, K., Xue, C., \& Zhang, L. (2020). Replicating anomalies. \textit{Review of Financial Studies}, 33(5), 2019--2133.'),
    'Men': ('10.1111/jofi.13337', 'Menkveld et al.\\ (2024)', 'Menkveld et al.\\ (2024)',
            r'Menkveld, A. J., Dreber, A., Holzmeister, F., Huber, J., Johannesson, M., Kirchler, M., et al.\ (2024). Nonstandard errors. \textit{The Journal of Finance}, 79(3), 2339--2390.'),
    'Sil': ('10.1177/2515245917747646', 'Silberzahn et al.\\ (2018)', 'Silberzahn et al.\\ (2018)',
            r'Silberzahn, R., Uhlmann, E. L., Martin, D. P., Anselmi, P., Aust, F., Awtrey, E., et al.\ (2018). Many analysts, one data set: Making transparent how variations in analytic choices affect results. \textit{Advances in Methods and Practices in Psychological Science}, 1(3), 337--356.'),
    'SSN': ('10.1038/s41562-020-0912-z', 'Simonsohn, Simmons and Nelson (2020)', 'Simonsohn, Simmons și Nelson (2020)',
            r'Simonsohn, U., Simmons, J. P., \& Nelson, L. D. (2020). Specification curve analysis. \textit{Nature Human Behaviour}, 4(11), 1208--1214.'),
    'Ste': ('10.1177/1745691616658637', 'Steegen et al.\\ (2016)', 'Steegen et al.\\ (2016)',
            r'Steegen, S., Tuerlinckx, F., Gelman, A., \& Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. \textit{Perspectives on Psychological Science}, 11(5), 702--712.'),
    'Peng': ('10.1126/science.1213847', 'Peng (2011)', 'Peng (2011)',
             r'Peng, R. D. (2011). Reproducible research in computational science. \textit{Science}, 334(6060), 1226--1227.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., Barrow, D. K., Ben Taieb, S., et al.\ (2022). Forecasting: theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    # ------------------------------------------------ AI in research
    'MC': ('10.1038/s41586-024-07146-0', 'Messeri and Crockett (2024)', 'Messeri și Crockett (2024)',
           r'Messeri, L., \& Crockett, M. J. (2024). Artificial intelligence and illusions of understanding in scientific research. \textit{Nature}, 627(8002), 49--58.'),
    'WW': ('10.1038/s41598-023-41032-5', 'Walters and Wilder (2023)', 'Walters și Wilder (2023)',
           r'Walters, W. H., \& Wilder, E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. \textit{Scientific Reports}, 13, 14045.'),
    'Kor': ('10.1257/jel.20231736', 'Korinek (2023)', 'Korinek (2023)',
            r'Korinek, A. (2023). Generative AI for economic research: Use cases and implications for economists. \textit{Journal of Economic Literature}, 61(4), 1281--1317.'),
    'Wang': ('10.1038/s41586-023-06221-2', 'Wang et al.\\ (2023)', 'Wang et al.\\ (2023)',
             r'Wang, H., Fu, T., Du, Y., Gao, W., Huang, K., Liu, Z., et al.\ (2023). Scientific discovery in the age of artificial intelligence. \textit{Nature}, 620(7972), 47--60.'),
    'Lu': (AX + '2408.06292', 'Lu et al.\\ (2024)', 'Lu et al.\\ (2024)',
           r'Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., \& Ha, D. (2024). The AI Scientist: Towards fully automated open-ended scientific discovery. \textit{arXiv:2408.06292}.'),
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
