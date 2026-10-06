r"""
build_chapter2.py -- Capitolul 2 (Rupturi structurale și modele neliniare), EN + RO
==================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_02/ch2_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice și a cifrelor publicate în lucrări, citate ca atare).
TSA, Capitolul 3 a predat Perron (1989) și Zivot--Andrews; aici construim pe ele.
Ieșire:
  EN/Courses/chapter2_structural_breaks_nonlinear_models.tex
  RO/Cursuri/capitol2_rupturi_structurale_modele_neliniare.tex
Rulare:
  python3 Quantlets/Ch_02/generate_all_charts.py
  python3 latex/build_chapter2.py && python3 latex/ats_build.py compile 2
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch2_common import REFS, QLURL, T, bib, finalize, load, minus_fix, pv, ym, qq, date   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(2, 'lecture', refs=REFS)
C = 'https://commons.wikimedia.org/wiki/File:'
P = V.put


def ql(folder):
    return f'\\quantlet{{{folder.replace("_", chr(92) + "_")}}}{{\\qlurl{{{folder}}}}}'


def chart(title, fig, folder, bullets, h='0.58\\textheight', size='footnotesize'):
    body = (f'\\begin{{center}}\n\\includegraphics[width=0.97\\textwidth,height={h},keepaspectratio]{{{fig}.pdf}}\n'
            f'\\end{{center}}\n\\vspace{{-0.25cm}}\n' + items(*bullets) + '\n' + ql(folder))
    D.frame(title, body, size)


def interp(title, bullets, size='small'):
    D.frame(T(f'Interpreting {title[0]}', f'Interpretarea {title[1]}'), items(*bullets), size)


FOTO = T('Photo', 'Foto')
PD = T('public domain', 'domeniu public')
PH = {
    'chow': ('ch2_chow.jpg', C + 'Gregory_Chi-chong_Chow.jpg', T('Portrait', 'Portret') + ': ' + T('unknown author (1950s--1960s)', 'autor necunoscut (anii 1950--1960)') + '; ' + PD + '; Wikimedia Commons'),
    'tong': ('ch2_tong.jpg', C + 'Howell-Tong.jpg', FOTO + ': Mr and Mrs Howell Tong / IMS; CC BY 3.0; Wikimedia Commons'),
    'lynx': ('ch2_lynx_2010.jpg', C + 'Canada_lynx_by_Michael_Zahra_(cropped).jpg', FOTO + ': Michael Zahra (2010); CC BY-SA 3.0; Wikimedia Commons'),
    'gas': ('ch2_gasline_1979.jpg', C + 'Line_at_a_gas_station,_June_15,_1979.jpg', FOTO + ': Warren K. Leffler (1979), Library of Congress; ' + PD + '; Wikimedia Commons'),
    'volcker': ('ch2_volcker_reagan_1981.jpg', C + 'President_Ronald_Reagan_Paul_Volcker_Meeting_to_Discuss_Monetary_Policy_with_Paul_Volker_in_Oval_Office_-_DPLA_-_e04117f4897610a724c267cdf855ce73.jpg',
                FOTO + ': White House Photographic Office (1981); ' + PD + '; Wikimedia Commons'),
    'cassel': ('ch2_cassel.jpg', C + 'Gustav_Cassel.jpg', T('Portrait', 'Portret') + ': ' + T('unknown author', 'autor necunoscut') + '; ' + PD + '; Wikimedia Commons'),
    'bretton': ('ch2_bretton_woods_1944.jpg', C + 'Morgenthau_Bretton_Woods_opening_1944.jpg', FOTO + ': US National Archives (1944); ' + PD + '; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


# =============================================================================
# CIFRE
# =============================================================================
CH = N['chow']
P('ch.cv1', CH['cv']['sup']['1'][1], 2)
P('ch.cv2', CH['cv']['sup']['2'][1], 2)
P('ch.cv1a', CH['cv']['sup']['1'][0], 2)
P('ch.cv1b', CH['cv']['sup']['1'][2], 2)
P('ch.exp1', CH['cv']['exp']['1'][1], 2)
P('ch.ave1', CH['cv']['ave']['1'][1], 2)
P('ch.size50', 100 * CH['chosen'][0], 0)
P('ch.size800', 100 * CH['chosen'][-1], 0)
P('ch.fix', 100 * CH['fixed'][1], 1)
V.int('ch.reps', CH['reps'])
M = N['mpq']
for tag, m in (('p', M['paper']), ('e', M['ext']), ('x', M['ex2019'])):
    P(f'mpq.{tag}.sup', m['var']['sup'], 1)
    V.raw(f'mpq.{tag}.psup', pv(m['var']['p_sup']))
    P(f'mpq.{tag}.exp', m['var']['exp'], 1)
    P(f'mpq.{tag}.ave', m['var']['ave'], 1)
    V.raw(f'mpq.{tag}.date', qq(m['date_var']))
    P(f'mpq.{tag}.ratio', m['ratio_var'], 1)
    P(f'mpq.{tag}.s1', m['s_pre'], 2)
    P(f'mpq.{tag}.s2', m['s_post'], 2)
    P(f'mpq.{tag}.msup', m['mean']['sup'], 1)
    V.raw(f'mpq.{tag}.pmsup', pv(m['mean']['p_sup']))
    V.raw(f'mpq.{tag}.n', str(m['n']))
P('mpq.p.phi', M['paper']['phi'], 2)
P('mpq.min', M['min'], 1)
V.raw('mpq.mind', qq(M['min_date']))
BP = N['bp']
V.raw('bp.n', str(BP['n']))
V.raw('bp.h', str(BP['h']))
for k in ('1', '2', '3', '4', '5'):
    P(f'bp.F{k}', BP['supF'][k], 1)
P('bp.ud', BP['UDmax'], 1)
P('bp.s1', BP['seq']['1'], 1)
P('bp.s2', BP['seq']['2'], 1)
P('bp.s3', BP['seq']['3'], 2)
for k in ('0', '1', '2', '3'):
    P(f'bp.bic{k}', BP['BIC'][k], 3)
    P(f'bp.lwz{k}', BP['LWZ'][k], 3)
    P(f'bp.ssr{k}', BP['ssr'][k], 0)
V.raw('bp.mseq', str(BP['m_seq']))
V.raw('bp.mbic', str(BP['m_bic']))
V.raw('bp.mlwz', str(BP['m_lwz']))
V.raw('bp.d3', ', '.join(qq(x) for x in BP['dates']['3']))
V.raw('bp.d2', ', '.join(qq(x) for x in BP['dates']['2']))
for i, x in enumerate(BP['mu']):
    P(f'bp.mu{i}', x, 2)
for i, (a, b) in enumerate(BP['ci']):
    V.raw(f'bp.ci{i}', f'[{qq(a)}; {qq(b)}]'.replace(';', '⟪,¦;⟫'))
E = BP['ext']
P('bpx.corr', E['corr'], 2)
V.raw('bpx.last', qq(E['last']))
V.raw('bpx.m', str(E['m_seq']))
V.raw('bpx.dates', ', '.join(qq(x) for x in E['dates']))
for i, x in enumerate(E['mu']):
    P(f'bpx.mu{i}', x, 2)
V.raw('bpx.ci2', f'[{qq(E["ci"][2][0])}; {qq(E["ci"][2][1])}]'.replace(';', '⟪,¦;⟫'))
CV = N['bpcv']['0.05']
for i in range(3):
    P(f'cv.F{i + 1}', CV['supF'][i], 2)
P('cv.ud', CV['UDmax'], 2)
P('cv.s1', CV['seq'][0], 2)
P('cv.s2', CV['seq'][1], 2)
RI = N['roinf']
V.raw('ri.n', str(RI['n']))
V.raw('ri.first', ym(RI['first']))
V.raw('ri.last', ym(RI['last']))
P('ri.F1', RI['supF']['1'], 1)
P('ri.s1', RI['seq']['1'], 2)
V.raw('ri.mseq', str(RI['m_seq']))
V.raw('ri.mbic', str(RI['m_bic']))
V.raw('ri.dates', ', '.join(ym(x) for x in RI['dates']))
for i, x in enumerate(RI['mu']):
    P(f'ri.mu{i}', x, 1)
V.raw('ri.ci1', f'[{ym(RI["ci"][1][0])}; {ym(RI["ci"][1][1])}]'.replace(';', '⟪,¦;⟫'))
MO = N['mon']
P('mo.size', 100 * MO['size_formula'], 1)
P('mo.size2', 100 * MO['size_625'], 1)
P('mo.n1', 100 * MO['mc']['naive'][1], 0)
P('mo.n9', 100 * MO['mc']['naive'][-1], 0)
P('mo.c9', 100 * MO['mc']['csw'][-1], 1)
V.int('mo.reps', MO['mc']['reps'])
V.raw('mo.first', ym(MO['first']))
V.raw('mo.naive', ym(MO['first_naive']))
V.raw('mo.lr', ym(MO['first_lr']))
P('mo.mean', MO['mean_hist'], 2)
P('mo.s', MO['s'], 2)
VA = N['var']
V.int('va.n', VA['n'])
P('va.it', VA['IT'], 1)
P('va.k2', VA['k2'], 2)
V.raw('va.nit', str(VA['n_it']))
V.raw('va.nk2', str(VA['n_k2']))
V.raw('va.dates', ', '.join(date(x) for x in VA['dates_k2']))
P('va.kurt', VA['kurt'], 1)
P('va.sdmax', max(VA['sd']), 2)
P('va.sdmin', min(VA['sd']), 2)
UR = N['ur']
P('ur.adf', UR['adf'], 2)
V.raw('ur.adfp', pv(UR['adf_p']))
P('ur.za', UR['za'], 2)
P('ur.zacv', UR['za_cv5'], 2)
V.raw('ur.zad', qq(UR['za_date']))
P('ur.two', UR['two_t'], 2)
V.raw('ur.twod', ' și '.join(qq(x) for x in UR['two_dates']).replace(' și ', '⟪ and ¦ și ⟫'))
V.raw('ur.ptwo', pv(UR['p_two']))
V.raw('ur.pone', pv(UR['p_one']))
P('ur.cvone', UR['cv_one_boot'], 2)
P('ur.cvtwo', UR['cv_two_boot'], 2)
V.raw('ur.B', str(UR['B']))
V.raw('ur.first', qq(UR['first']))
V.raw('ur.last', qq(UR['last']))
WI = N['win']
mc = WI['mc']
i2 = mc['deltas'].index(2.0)
i1 = mc['deltas'].index(1.0)
for k, tag in (('expanding', 'exp'), ('rolling', 'roll'), ('post (estimated date)', 'est'), ('average across windows', 'ave')):
    P(f'wi.{tag}1', mc['rel'][k][i1], 2)
    P(f'wi.{tag}2', mc['rel'][k][i2], 2)
P('wi.exp0', mc['rel']['expanding'][0], 2)
V.int('wi.reps', mc['reps'])
for k, tag in (('expanding', 'exp'), ('rolling 60', 'r60'), ('rolling 120', 'r120'), ('AveW', 'ave')):
    P(f'wr.{tag}', WI['rmse'][k], 3)
    P(f'wr.{tag}s', WI['rmse_sub'][k], 3)
for k, tag in (('rolling 60', 'r60'), ('rolling 120', 'r120'), ('AveW', 'ave')):
    P(f'wd.{tag}', WI['dm'][k]['hln'], 2)
    V.raw(f'wd.{tag}p', pv(WI['dm'][k]['p']))
V.raw('wr.n', str(WI['n']))
LY = N['lynx']
P('ly.g', LY['gamma'], 3)
for i, v in enumerate(LY['b1_tl'][:3]):
    P(f'ly.a{i}', v, 3)
for i, v in enumerate(LY['b2_tl']):
    P(f'ly.b{i}', v, 3)
P('ly.ssr', LY['ssr'], 3)
P('ly.ssrtl', LY['ssr_tl'], 3)
P('ly.per', LY['period'], 0)
P('ly.v1', LY['resvar_setar'], 4)
P('ly.v2', LY['resvar_ar11'], 4)
V.raw('ly.n1', str(LY['n1']))
V.raw('ly.n2', str(LY['n2']))
TA = N['tar']
P('ta.g', TA['gamma'], 3)
P('ta.ci0', TA['ci'][0], 3)
P('ta.ci1', TA['ci'][1], 3)
V.raw('ta.n', str(TA['n']))
V.raw('ta.n1', str(TA['n1']))
V.raw('ta.n2', str(TA['n2']))
V.raw('ta.p', pv(TA['p12']))
P('ta.W', TA['supW12'], 1)
P('ta.sse', TA['sse'], 2)
P('ta.lin', TA['lin_sse'], 2)
V.raw('ta.dhat', str(TA['dhat']))
P('ta.gd', TA['dhat_fit']['gamma'], 2)
P('ta.sse3', [r for r in TA['rows'] if r['d'] == TA['dhat']][0]['sse'], 2)
P('ta.xg', TA['ext']['gamma'], 3)
P('ta.xci0', TA['ext']['ci'][0], 3)
P('ta.xci1', TA['ext']['ci'][1], 3)
V.raw('ta.xp', pv(TA['ext']['p']))
P('ta.b11', TA['b1'][1], 2)
P('ta.b21', TA['b2'][1], 2)
P('ta.b10', TA['b1'][0], 3)
P('ta.b20', TA['b2'][0], 3)
P('ta.b12', TA['b1'][2], 2)
P('ta.b22', TA['b2'][2], 2)
nsig = sum(1 for r in TA['rows'] if r['p'] < 0.05)
V.raw('ta.nsig', str(nsig))
LS = N['lstar']
P('ls.g', LS['gamma'], 1)
P('ls.c', LS['c'], 2)
P('ls.ratio', LS['ratio_sd'], 2)
P('ls.aicl', LS['aic_lin'], 3)
P('ls.aics', LS['aic_star'], 3)
P('ls.bicl', LS['bic_lin'], 3)
P('ls.bics', LS['bic_star'], 3)
for d in ('1', '2', '3'):
    V.raw(f'ls.p{d}', pv(LS['tests'][d]['p']))
V.raw('ls.p24', pv(LS['tests']['2']['p4']))
V.raw('ls.p23', pv(LS['tests']['2']['p3']))
V.raw('ls.p22', pv(LS['tests']['2']['p2']))
P('ls.rs', LS['rmse_star'], 3)
P('ls.rl', LS['rmse_lin'], 3)
P('ls.dm', LS['dm']['hln'], 2)
V.raw('ls.dmp', pv(LS['dm']['p']))
P('ls.share', 100 * LS['share_G'], 0)
ES = N['estar']
P('es.th', ES['paper']['theta2'], 3)
P('es.thse', ES['paper']['se'][0], 3)
P('es.mu', ES['paper']['mu'], 3)
P('es.s', ES['paper']['s'], 3)
P('es.thx', ES['ext']['theta2'], 3)
P('es.mux', ES['ext']['mu'], 3)
V.raw('es.last', ym(ES['last']))
P('es.df', ES['df_p'], 2)
V.raw('es.dfp', pv(ES['df_pp']))
P('es.dfx', ES['df_e'], 2)
V.raw('es.dfxp', pv(ES['df_ep']))
V.raw('es.pmc', pv(ES['p_mc']))
P('es.t', ES['t_theta'], 2)
for k in ('0.01', '0.05', '0.10', '0.20', '0.40'):
    V.raw(f'es.h{k[2:]}', str(ES['hlh_p'][k]))
    V.raw(f'es.e{k[2:]}', str(ES['hl_p'][k]))
P('es.hlar', ES['hl_ar'], 0)
P('es.pow', 100 * ES['power'], 0)
P('es.kss', ES['kss_p'], 2)
P('es.kssx', ES['kss_e'], 2)
V.raw('es.ksp', pv(ES['kss_pp']))
V.raw('es.ksxp', pv(ES['kss_pe']))
P('es.kscv', ES['kss_cv_e'], 2)
NL = N['nlt']
names = list(NL)
for i, k in enumerate(names):
    for t in ('bds_p', 'keenan_p', 'tsay_p', 'lm3_p', 'supW_p'):
        V.raw(f'nl.{i}.{t}', pv(NL[k][t]))
NF = N['nlf']
for h in ('1', '12'):
    P(f'nf.{h}.t', NF[h]['rmse_tar'], 3)
    P(f'nf.{h}.a', NF[h]['rmse_ar'], 3)
    P(f'nf.{h}.t2', NF[h]['rmse_tar_reg2'], 3)
    P(f'nf.{h}.a2', NF[h]['rmse_ar_reg2'], 3)
    P(f'nf.{h}.dm', NF[h]['dm']['hln'], 2)
    V.raw(f'nf.{h}.p', pv(NF[h]['dm']['p']))
V.raw('nf.n', str(NF['1']['n']))
V.raw('nf.n2', str(NF['1']['n_reg2']))
V.raw('nf.origin', ym(NF['origin']))
P('nf.actual', NF['actual'], 1)
P('nf.tm', NF['tar_mean'], 1)
P('nf.am', NF['ar_mean'], 1)
P('nf.tq0', NF['tar_q'][0], 1)
P('nf.tq1', NF['tar_q'][1], 1)
P('nf.aq0', NF['ar_q'][0], 1)
P('nf.aq1', NF['ar_q'][1], 1)
AI = N['ai']
P('ai.kr', AI['k_raw'], 2)
P('ai.ks', AI['k_seg'], 2)
V.raw('ai.pr', pv(AI['p_raw']))
V.raw('ai.ps', pv(AI['p_seg']))
P('ai.cvr', AI['cv_raw'], 2)
P('ai.cvs', AI['cv_seg'], 2)
V.raw('ai.dates', ', '.join(ym(x) for x in AI['dates']))
V.raw('ai.reps', str(AI['reps']))
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T('\\textbf{Question}: when do the parameters of a time-series model change, and when is the dynamics itself state dependent?',
       '\\textbf{Întrebarea}: cînd se schimbă parametrii unui model de serii de timp și cînd depinde dinamica însăși de starea sistemului?'),
     [T('a \\textbf{break} is a change in the parameters at some dates; a \\textbf{nonlinear} model lets the parameters depend on the past of the series',
        'o \\textbf{ruptură} este o schimbare a parametrilor la anumite date; un model \\textbf{neliniar} lasă parametrii să depindă de trecutul seriei'),
      T('both produce the same symptoms: unstable forecasts, spurious persistence, rejected linearity',
        'ambele produc aceleași simptome: prognoze instabile, persistență aparentă, liniaritate respinsă')]),
    (T('\\textbf{Route} of the chapter', '\\textbf{Traseul} capitolului'),
     [T('breaks: Chow, sup-Wald (Andrews), Bai--Perron, monitoring (CUSUM, CSW), variance breaks (ICSS), unit roots with breaks', 'rupturi: Chow, sup-Wald (Andrews), Bai--Perron, monitorizare (CUSUM, CSW), rupturi în varianță (ICSS), rădăcini unitare cu rupturi'),
      T('forecasting under breaks: the choice of the estimation window', 'prognoza în prezența rupturilor: alegerea ferestrei de estimare'),
      T('nonlinear models: TAR/SETAR, STAR (LSTAR, ESTAR), nonlinearity tests, nonlinear forecasts', 'modele neliniare: TAR/SETAR, STAR (LSTAR, ESTAR), teste de neliniaritate, prognoze neliniare')]),
    T('We build on TSA, Chapter 3 (Perron 1989, Zivot--Andrews) and on Chapters 0 and 1 (HAC, bootstrap, DM tests); Seminar 2 comes before this lecture',
      'Pornim de la TSA, Capitolul 3 (Perron 1989, Zivot--Andrews) și de la Capitolele 0 și 1 (HAC, bootstrap, teste DM); Seminarul 2 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Derive the Chow test and explain why searching over the break date changes its null distribution (the Davies problem)',
      'Deduceți testul Chow și explicați de ce căutarea datei rupturii îi schimbă distribuția sub ipoteza nulă (problema Davies)'),
    T('Test for one or several breaks with unknown dates (sup-, exp-, ave-Wald, Bai--Perron), select their number and build confidence intervals for the dates',
      'Testați una sau mai multe rupturi cu date necunoscute (sup-, exp-, ave-Wald, Bai--Perron), alegeți numărul lor și construiți intervale de încredere pentru date'),
    T('Monitor a model in real time with a controlled false-alarm rate, and detect breaks in variance',
      'Monitorizați un model în timp real cu o rată controlată a alarmelor false și detectați rupturile în varianță'),
    T('Choose the estimation window when the data contain breaks, and evaluate the choice out of sample',
      'Alegeți fereastra de estimare cînd datele conțin rupturi și evaluați alegerea în afara eșantionului'),
    T('Specify, test, estimate and forecast threshold and smooth-transition models, with valid inference when the threshold is not identified under the null',
      'Specificați, testați, estimați și folosiți pentru prognoză modele cu prag și cu tranziție netedă, cu inferență validă cînd pragul nu este identificat sub ipoteza nulă')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T('Surveys: \\refCP, \\refHd, \\refRos, \\refVDTF, \\refHe', 'Sinteze: \\refCP, \\refHd, \\refRos, \\refVDTF, \\refHe'),
     [T('textbooks: \\refHam, Ch.~22 (regime changes); \\refKL; the forecasting survey \\refPetro\\ (open access); bridge: \\refHP', 'manuale: \\refHam, cap.~22 (schimbări de regim); \\refKL; sinteza despre prognoză \\refPetro\\ (acces liber); legătura cu licența: \\refHP')]),
    (T('Python Quantlets of this chapter: \\href{' + QLURL + '}{Quantlets/Ch\\_02}', 'Quantlet-urile Python ale capitolului: \\href{' + QLURL + '}{Quantlets/Ch\\_02}'),
     [T('Bai--Perron dynamic programming, sup-Wald, ICSS, CSW monitoring, Hansen\'s bootstrap and LR interval, LSTAR and ESTAR by nonlinear least squares, all written out in \\texttt{numpy}/\\texttt{scipy}',
        'programarea dinamică Bai--Perron, sup-Wald, ICSS, monitorizarea CSW, bootstrap-ul și intervalul LR ale lui Hansen, LSTAR și ESTAR prin cele mai mici pătrate neliniare, toate scrise explicit în \\texttt{numpy}/\\texttt{scipy}'),
      T('R users: the \\texttt{strucchange} package \\refZEIL\\ implements the same break tests', 'pentru R: pachetul \\texttt{strucchange} \\refZEIL\\ conține aceleași teste de ruptură')]),
    T('Lecture notebook: \\href{\\colaburl{notebooks/EN/chapter2_lecture_notebook.ipynb}}{open in Google Colab}',
      'Notebook-ul cursului: \\href{\\colaburl{notebooks/EN/chapter2_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

TB = '>{\\raggedright\\arraybackslash}'
D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{4.6cm}' + TB + 'p{4.6cm}' + TB + 'p{2.4cm}',
    T('\\textbf{Series}', '\\textbf{Seria}') + ' & ' + T('\\textbf{Source}', '\\textbf{Sursa}') + ' & ' + T('\\textbf{Use}', '\\textbf{Utilizare}'),
    [T('US ex-post real interest rate, 1961--1986', 'Rata reală ex post a dobînzii, SUA, 1961--1986') + ' & ' + T('JAE data archive (Bai--Perron); rebuilt from FRED (TB3MS, CPIAUCNS)', 'arhiva de date JAE (Bai--Perron); reconstruită din FRED (TB3MS, CPIAUCNS)') + ' & Bai--Perron',
     T('US real GDP growth, quarterly', 'Creșterea PIB real, SUA, trimestrial') + ' & FRED (GDPC1) & ' + T('variance break', 'ruptură în varianță'),
     T('HICP inflation, Romania (y/y and m/m)', 'Inflația IAPC, România (anuală și lunară)') + ' & Eurostat (prc\\_hicp\\_minr) & ' + T('breaks, monitoring', 'rupturi, monitorizare'),
     T('EUR/RON, daily', 'EUR/RON, zilnic') + ' & ' + T('BNR reference rate', 'cursul de referință BNR') + ' & ICSS',
     T('Real GDP, Romania, quarterly', 'PIB real, România, trimestrial') + ' & Eurostat (namq\\_10\\_gdp) & ' + T('unit roots', 'rădăcini unitare'),
     T('Unemployment rate, US men aged 20+', 'Rata șomajului, bărbați de 20 de ani și peste, SUA') + ' & ' + T('BLS via FRED (LNS13000025 / LNS11000025; not adjusted: LNU03000025 / LNU01000025)', 'BLS prin FRED (LNS13000025 / LNS11000025; neajustat: LNU03000025 / LNU01000025)') + ' & TAR, LSTAR',
     T('Real dollar-sterling rate', 'Cursul real dolar--liră sterlină') + ' & ' + T('FRED (DEXUSUK, CPIAUCNS), OECD and ONS UK CPI', 'FRED (DEXUSUK, CPIAUCNS), IPC britanic OECD și ONS') + ' & ESTAR',
     T('Canadian lynx trappings, 1821--1934', 'Linxi capturați în Canada, 1821--1934') + ' & ' + T('R data set read by statsmodels', 'set de date R citit prin statsmodels') + ' & SETAR'],
    size='scriptsize') + items(
    T('All sources are public and need no account or key; monthly data up to August--September 2026',
      'Toate sursele sînt publice și nu cer cont sau cheie; datele lunare merg pînă în august--septembrie 2026'),
    T('HICP: harmonised index of consumer prices; BLS: US Bureau of Labor Statistics; ONS: UK Office for National Statistics; JAE: Journal of Applied Econometrics',
      'IAPC (HICP): indicele armonizat al prețurilor de consum; BLS: Biroul de statistică a muncii din SUA; ONS: Oficiul britanic de statistică; JAE: Journal of Applied Econometrics')), 'footnotesize')

D.frame(T('Two founders', 'Doi fondatori'), cols(
    ph('chow', 'Gregory C. Chow', h='0.36\\textheight'),
    ph('tong', 'Howell Tong', h='0.36\\textheight'), '0.48', '0.48') + items(
    T('1960: \\refChow\\ tests whether two regressions share their coefficients; the same year \\refQua\\ maximises the likelihood ratio over the switch date',
      '1960: \\refChow\\ testează dacă două regresii au aceiași coeficienți; în același an \\refQua\\ maximizează raportul de verosimilitate după data schimbării'),
    T('1980: \\refTL\\ propose threshold autoregression: a linear model in each regime, nonlinear as a whole, able to produce limit cycles',
      '1980: \\refTL\\ propun autoregresia cu prag: un model liniar în fiecare regim, neliniar în ansamblu, capabil să producă cicluri limită')), 'footnotesize')

# =============================================================================
# 1. INSTABILITATE ȘI DATĂ CUNOSCUTĂ
# =============================================================================
D.section('Parameter instability and a known break date', 'Instabilitatea parametrilor și o dată cunoscută a rupturii')

D.frame(T('Setting and notation', 'Cadrul și notațiile'), items(
    (T('Linear model $y_t = x_t\'\\beta_t + u_t$, $t = 1, \\dots, T$; stability means $H_0$: $\\beta_t = \\beta$ for all $t$', 'Modelul liniar $y_t = x_t\'\\beta_t + u_t$, $t = 1, \\dots, T$; stabilitatea înseamnă $H_0$: $\\beta_t = \\beta$ pentru orice $t$'),
     [T('one break at $T_1 = [\\pi T]$: $\\beta_t = \\beta_1$ for $t \\le T_1$ and $\\beta_t = \\beta_2$ after; $\\pi \\in (0, 1)$ is the \\textbf{break fraction}', 'o ruptură la $T_1 = [\\pi T]$: $\\beta_t = \\beta_1$ pentru $t \\le T_1$ și $\\beta_t = \\beta_2$ după; $\\pi \\in (0, 1)$ este \\textbf{fracția rupturii}'),
      T('$m$ breaks $T_1 < \\dots < T_m$ split the sample into $m + 1$ regimes', '$m$ rupturi $T_1 < \\dots < T_m$ împart eșantionul în $m + 1$ regimuri')]),
    (T('Kinds of change', 'Tipuri de schimbare'),
     [T('\\textbf{pure} change (all coefficients) or \\textbf{partial} change ($y_t = x_t\'\\beta + z_t\'\\delta_j + u_t$: only $\\delta$ moves)', 'schimbare \\textbf{totală} (toți coeficienții) sau \\textbf{parțială} ($y_t = x_t\'\\beta + z_t\'\\delta_j + u_t$: doar $\\delta$ se schimbă)'),
      T('in the mean, in the dynamics, in the variance; abrupt or gradual (random-walk coefficients, \\refSW)', 'în medie, în dinamică, în varianță; bruscă sau graduală (coeficienți de tip mers aleator, \\refSW)')]),
    T('In TSA, Chapter 3 a break was a nuisance for unit-root tests; here the break is the object of inference', 'În TSA, Capitolul 3 ruptura era un obstacol pentru testele de rădăcină unitară; aici ruptura este obiectul inferenței')), 'small')

D.frame(T('The Chow test', 'Testul Chow'), items(
    (T('Known date $T_1$, $k$ regressors, i.i.d.\\ Normal errors; SSR of the pooled fit $S_0$, of the two sub-samples $S_1$, $S_2$ \\refChow', 'Dată cunoscută $T_1$, $k$ regresori, erori i.i.d.\\ Normale; SSR al regresiei comune $S_0$, al celor două subeșantioane $S_1$, $S_2$ \\refChow'),
     [T('$F = \\dfrac{(S_0 - S_1 - S_2)/k}{(S_1 + S_2)/(T - 2k)} \\sim F(k, T - 2k)$ under $H_0$', '$F = \\dfrac{(S_0 - S_1 - S_2)/k}{(S_1 + S_2)/(T - 2k)} \\sim F(k, T - 2k)$ sub $H_0$'),
      T('equivalent to the $F$ test of $\\delta = 0$ in $y_t = x_t\'\\beta + (x_t \\mathbf 1\\{t > T_1\\})\'\\delta + u_t$', 'echivalent cu testul $F$ pentru $\\delta = 0$ în $y_t = x_t\'\\beta + (x_t \\mathbf 1\\{t > T_1\\})\'\\delta + u_t$')]),
    (T('Robust version: the Wald statistic $W_T(T_1) = \\hat\\delta\'\\hat V_\\delta^{-1}\\hat\\delta$ with a heteroskedasticity- or HAC-robust $\\hat V_\\delta$ (Chapter 0), asymptotically $\\chi^2(k)$', 'Varianta robustă: statistica Wald $W_T(T_1) = \\hat\\delta\'\\hat V_\\delta^{-1}\\hat\\delta$ cu $\\hat V_\\delta$ robustă la heteroscedasticitate sau HAC (Capitolul 0), asimptotic $\\chi^2(k)$'),
     [T('the classical $F$ also assumes equal variances in the two regimes', '$F$ clasic presupune și varianțe egale în cele două regimuri')]),
    (T('\\textbf{Predictive} Chow test when $T - T_1 < k$: $F = \\dfrac{(S_0 - S_1)/(T - T_1)}{S_1/(T_1 - k)}$', 'Testul Chow \\textbf{predictiv} cînd $T - T_1 < k$: $F = \\dfrac{(S_0 - S_1)/(T - T_1)}{S_1/(T_1 - k)}$'),
     [T('it asks whether the model estimated up to $T_1$ forecasts the last observations; the ancestor of forecast-breakdown tests (Section 7)', 'întreabă dacă modelul estimat pînă la $T_1$ prognozează ultimele observații; precursorul testelor de eșec al prognozelor (secțiunea 7)')])), 'small')

D.frame(T('The date chosen by looking at the data', 'Data aleasă privind datele'), items(
    (T('In practice $T_1$ is rarely known: the researcher sees a jump in the plot and tests there', 'În practică $T_1$ este rar cunoscut: cercetătorul vede un salt în grafic și testează acolo'),
     [T('the test then uses the date that \\emph{maximises} the statistic: a data-snooping problem (Chapter 0)', 'testul folosește atunci data care \\emph{maximizează} statistica: o problemă de data snooping (Capitolul 0)')]),
    (T('Under $H_0$ the break date is \\textbf{not identified}: the parameter $\\pi$ appears only under the alternative \\refDav', 'Sub $H_0$ data rupturii \\textbf{nu este identificată}: parametrul $\\pi$ apare doar sub ipoteza alternativă \\refDav'),
     [T('standard asymptotics fail; the null distribution of $\\sup_\\pi W_T(\\pi)$ is that of the supremum of a stochastic process', 'asimptotica standard nu se aplică; distribuția sub $H_0$ a lui $\\sup_\\pi W_T(\\pi)$ este cea a supremumului unui proces stochastic')]),
    T('The same problem returns for the threshold of a TAR model (Section 8) and for the transition parameter of a STAR model (Section 9)', 'Aceeași problemă revine pentru pragul unui model TAR (secțiunea 8) și pentru parametrul de tranziție al unui model STAR (secțiunea 9)')), 'small')

chart(T('A Chow test at the data-chosen date', 'Un test Chow la data aleasă din date'), 'ats_ch2_chow_snooping', 'ATS_ch2_chow_snooping', [
    T('Left: white noise, mean-shift Chow test at 5\\%, @{ch.reps} replications per $T$; right: simulated null density of $\\sup_\\pi W_T(\\pi)$, $\\pi \\in [0.15, 0.85]$, against $\\chi^2(1)$',
      'Stînga: zgomot alb, testul Chow pentru o schimbare de medie la 5\\%, @{ch.reps} de replicări pentru fiecare $T$; dreapta: densitatea simulată sub $H_0$ a lui $\\sup_\\pi W_T(\\pi)$, $\\pi \\in [0{,}15; 0{,}85]$, față de $\\chi^2(1)$')], h='0.52\\textheight')

interp(('the size distortion', 'distorsiunii de mărime'), [
    (T('At a fixed date the test keeps its size (@{ch.fix}\\% for $T = 100$); at the maximising date it rejects a true null in @{ch.size50}\\% to @{ch.size800}\\% of samples', 'La o dată fixată dinainte testul își păstrează mărimea (@{ch.fix}\\% pentru $T = 100$); la data care maximizează statistica respinge o ipoteză nulă adevărată în @{ch.size50}\\% pînă la @{ch.size800}\\% din eșantioane'),
     [T('the distortion grows slowly with $T$: more candidate dates, a larger maximum', 'distorsiunea crește lent cu $T$: mai multe date candidate, un maxim mai mare')]),
    T('The 5\\% critical value of the supremum is @{ch.cv1}, against 3.84 for $\\chi^2(1)$; with two coefficients @{ch.cv2}', 'Valoarea critică de 5\\% a supremumului este @{ch.cv1}, față de 3,84 pentru $\\chi^2(1)$; cu doi coeficienți @{ch.cv2}'),
    T('Lesson: the date search is part of the test; the critical values must account for it', 'Lecția: căutarea datei face parte din test; valorile critice trebuie să țină cont de ea')])

D.recap(('Instability and known dates', 'instabilitatea și datele cunoscute'), [
    T('A break is a change of $\\beta_t$; pure or partial, in mean, dynamics or variance', 'O ruptură este o schimbare a lui $\\beta_t$; totală sau parțială, în medie, în dinamică sau în varianță'),
    T('Chow: an $F$ test valid only for a date fixed before seeing the data', 'Chow: un test $F$ valid doar pentru o dată fixată înainte de a vedea datele'),
    T('Choosing the date from the data multiplies the size several times', 'Alegerea datei din date multiplică de cîteva ori mărimea testului'),
    T('The break date is a nuisance parameter not identified under $H_0$', 'Data rupturii este un parametru neidentificat sub $H_0$')])

# =============================================================================
# 2. DATĂ NECUNOSCUTĂ
# =============================================================================
D.section('One break at an unknown date', 'O ruptură la o dată necunoscută')

D.frame(T('The sup-Wald test of Andrews (1993)', 'Testul sup-Wald al lui Andrews (1993)'), items(
    (T('Compute $W_T(\\pi)$ for every $\\pi \\in \\Pi = [\\pi_0, 1 - \\pi_0]$ and take $\\sup_{\\pi \\in \\Pi} W_T(\\pi)$ \\refAnd; \\refQua\\ used the LR version', 'Calculăm $W_T(\\pi)$ pentru orice $\\pi \\in \\Pi = [\\pi_0, 1 - \\pi_0]$ și luăm $\\sup_{\\pi \\in \\Pi} W_T(\\pi)$ \\refAnd; \\refQua\\ a folosit varianta LR'),
     [T('LM, Wald and LR versions share the same limit; $\\pi_0 = 0.15$ is the usual \\textbf{trimming}', 'variantele LM, Wald și LR au aceeași limită; $\\pi_0 = 0{,}15$ este \\textbf{trunchierea} obișnuită')]),
    (T('\\textbf{Theorem} \\refAnd: under $H_0$ and regularity conditions (stationary, mixing regressors)', '\\textbf{Teoremă} \\refAnd: sub $H_0$ și în condiții de regularitate (regresori staționari, cu dependență slabă)'),
     [T('$W_T(\\cdot) \\Rightarrow Q_p(\\pi) = \\dfrac{\\|B_p(\\pi) - \\pi B_p(1)\\|^2}{\\pi(1 - \\pi)}$, $B_p$ a $p$-dimensional Brownian motion', '$W_T(\\cdot) \\Rightarrow Q_p(\\pi) = \\dfrac{\\|B_p(\\pi) - \\pi B_p(1)\\|^2}{\\pi(1 - \\pi)}$, $B_p$ o mișcare browniană $p$-dimensională'),
      T('$\\sup W_T \\to_d \\sup_{\\pi \\in \\Pi} Q_p(\\pi)$: a squared, standardised Brownian bridge (derivation in the Appendix)', '$\\sup W_T \\to_d \\sup_{\\pi \\in \\Pi} Q_p(\\pi)$: o punte browniană la pătrat, standardizată (deducerea în Anexă)')]),
    (T('Why trimming: at fixed $\\pi$, $Q_p(\\pi) \\sim \\chi^2(p)$, but $\\sup_{\\pi \\in (0,1)} Q_p(\\pi) = \\infty$ almost surely (law of the iterated logarithm)', 'De ce trunchiere: la $\\pi$ fixat, $Q_p(\\pi) \\sim \\chi^2(p)$, dar $\\sup_{\\pi \\in (0,1)} Q_p(\\pi) = \\infty$ aproape sigur (legea logaritmului iterat)'),
     [T('critical values depend on $p$ and $\\pi_0$; here simulated: $p = 1$: @{ch.cv1a} (10\\%), @{ch.cv1} (5\\%), @{ch.cv1b} (1\\%)', 'valorile critice depind de $p$ și $\\pi_0$; aici simulate: $p = 1$: @{ch.cv1a} (10\\%), @{ch.cv1} (5\\%), @{ch.cv1b} (1\\%)')])), 'small')

D.frame(T('Optimal tests: Andrews and Ploberger (1994)', 'Teste optime: Andrews și Ploberger (1994)'), items(
    (T('The supremum is not the only functional; averaging is optimal against alternatives close to $H_0$ \\refAP', 'Supremumul nu este singura funcțională; medierea este optimă împotriva alternativelor apropiate de $H_0$ \\refAP'),
     [T('$\\mathrm{expW} = \\ln\\Big(\\dfrac{1}{|\\Pi|}\\displaystyle\\int_\\Pi \\exp\\big(\\tfrac12 W_T(\\pi)\\big)d\\pi\\Big)$: weighted average power, for medium and large breaks', '$\\mathrm{expW} = \\ln\\Big(\\dfrac{1}{|\\Pi|}\\displaystyle\\int_\\Pi \\exp\\big(\\tfrac12 W_T(\\pi)\\big)d\\pi\\Big)$: putere medie ponderată, pentru rupturi medii și mari'),
      T('$\\mathrm{aveW} = \\dfrac{1}{|\\Pi|}\\displaystyle\\int_\\Pi W_T(\\pi)\\,d\\pi$: optimal for very small breaks, close to the Nyblom test of random-walk coefficients', '$\\mathrm{aveW} = \\dfrac{1}{|\\Pi|}\\displaystyle\\int_\\Pi W_T(\\pi)\\,d\\pi$: optim pentru rupturi foarte mici, apropiat de testul Nyblom pentru coeficienți de tip mers aleator')]),
    T('5\\% values for $p = 1$, $\\pi_0 = 0.15$ (simulated): sup @{ch.cv1}, exp @{ch.exp1}, ave @{ch.ave1}', 'Valori de 5\\% pentru $p = 1$, $\\pi_0 = 0{,}15$ (simulate): sup @{ch.cv1}, exp @{ch.exp1}, ave @{ch.ave1}'),
    (T('The sup-Wald test has power against \\emph{any} kind of instability, not only a single break', 'Testul sup-Wald are putere împotriva \\emph{oricărui} tip de instabilitate, nu doar a unei singure rupturi'),
     [T('a rejection says ``unstable\'\', not ``one break at $\\hat\\pi$\'\'; the number of breaks is the subject of Section 3', 'o respingere spune „instabil”, nu „o ruptură la $\\hat\\pi$”; numărul rupturilor este subiectul secțiunii 3')])), 'small')

D.frame(T('Estimating the break date', 'Estimarea datei rupturii'), items(
    (T('Least squares: $\\hat T_1 = \\arg\\min_{T_1} [S_1(T_1) + S_2(T_1)]$, equivalently $\\arg\\max$ of the Wald statistic under homoskedasticity', 'Cele mai mici pătrate: $\\hat T_1 = \\arg\\min_{T_1} [S_1(T_1) + S_2(T_1)]$, echivalent cu $\\arg\\max$ al statisticii Wald sub homoscedasticitate'),
     [T('for a fixed break size, $\\hat T_1 - T_1 = O_p(1)$: the \\textbf{date} is estimated with an error that does not grow with $T$, the fraction at rate $T$ \\refBai', 'pentru o ruptură de mărime fixă, $\\hat T_1 - T_1 = O_p(1)$: \\textbf{data} se estimează cu o eroare care nu crește cu $T$, fracția cu rata $T$ \\refBai'),
      T('the regime coefficients are $\\sqrt T$-consistent and asymptotically Normal as if the date were known', 'coeficienții regimurilor sînt $\\sqrt T$-consistenți și asimptotic Normali ca și cum data ar fi cunoscută')]),
    (T('Confidence interval for the date: with a shrinking break $\\Delta_T \\to 0$, $\\Delta_T^2\\sigma^{-2}(\\hat T_1 - T_1) \\to_d \\arg\\max_s Z(s)$, $Z(s) = W(s) - |s|/2$ (two-sided Brownian motion) \\refBai', 'Interval de încredere pentru dată: cu o ruptură care scade, $\\Delta_T \\to 0$, $\\Delta_T^2\\sigma^{-2}(\\hat T_1 - T_1) \\to_d \\arg\\max_s Z(s)$, $Z(s) = W(s) - |s|/2$ (mișcare browniană bilaterală) \\refBai'),
     [T('large breaks, small noise: a short interval; the interval is asymmetric when variances differ across regimes', 'rupturi mari, zgomot mic: interval scurt; intervalul este asimetric cînd varianțele diferă între regimuri')])), 'small')

D.frame(T('Case study: McConnell and Perez-Quiros (2000)', 'Studiu de caz: McConnell și Perez-Quiros (2000)'), two(
    ph('gas', T('Gasoline queue, Maryland, 15 June 1979', 'Coadă la benzină, Maryland, 15 iunie 1979'), h='0.36\\textheight'),
    items((T('The paper: US real GDP growth, 1953Q2--1999Q2; AR(1) for the conditional mean; then a break in the mean of $\\sqrt{\\pi/2}\\,|\\hat e_t|$, an unbiased estimate of the standard deviation under Normality \\refMPQ', 'Lucrarea: creșterea PIB real în SUA, T2 1953--T2 1999; AR(1) pentru media condiționată; apoi o ruptură în media lui $\\sqrt{\\pi/2}\\,|\\hat e_t|$, o estimare nedeplasată a abaterii standard sub distribuția Normală \\refMPQ'),
           [T('tests: sup-, exp-, ave-Wald \\refAnd, \\refAP; their result: a variance break in 1984Q1, the ``Great Moderation\'\'', 'teste: sup-, exp-, ave-Wald \\refAnd, \\refAP; rezultatul lor: o ruptură în varianță în T1 1984, „Marea Moderație” (Great Moderation)')]),
          (T('Our replication: the same two steps on FRED GDPC1 (today\'s vintage), robust Wald statistics, simulated $p$-values; then the sample extended to 2026', 'Replicarea noastră: aceiași doi pași pe FRED GDPC1 (versiunea de azi), statistici Wald robuste, valori $p$ simulate; apoi eșantionul extins pînă în 2026'), []),
          T('Question: does the variance break survive revised data and the COVID-19 quarters?', 'Întrebarea: supraviețuiește ruptura în varianță datelor revizuite și trimestrelor COVID-19?')), '0.36', '0.62'), 'footnotesize')

chart(T('The Great Moderation in US output growth', 'Marea Moderație în creșterea PIB din SUA'), 'ats_ch2_great_moderation', 'ATS_ch2_great_moderation', [
    T('Top: growth with $\\pm 2$ residual standard deviations before and after the estimated break; bottom: the Wald sequence for a break in $\\E\\sqrt{\\pi/2}|e_t|$ (HAC), two samples',
      'Sus: creșterea cu $\\pm 2$ abateri standard reziduale înainte și după ruptura estimată; jos: șirul statisticilor Wald pentru o ruptură în $\\E\\sqrt{\\pi/2}|e_t|$ (HAC), două eșantioane')], h='0.64\\textheight')

interp(('the variance break', 'rupturii în varianță'), [
    (T('MPQ sample ($T = @{mpq.p.n}$): sup-Wald @{mpq.p.sup} ($p$ @{mpq.p.psup}), exp @{mpq.p.exp}, ave @{mpq.p.ave}; date @{mpq.p.date}, as in the paper', 'Eșantionul MPQ ($T = @{mpq.p.n}$): sup-Wald @{mpq.p.sup} ($p$ @{mpq.p.psup}), exp @{mpq.p.exp}, ave @{mpq.p.ave}; data @{mpq.p.date}, ca în lucrare'),
     [T('residual s.d. @{mpq.p.s1} before, @{mpq.p.s2} after: the variance falls by a factor of @{mpq.p.ratio}; no break in the mean equation (sup @{mpq.p.msup}, $p$ @{mpq.p.pmsup})', 'abaterea standard reziduală @{mpq.p.s1} înainte, @{mpq.p.s2} după: varianța scade de @{mpq.p.ratio} ori; nicio ruptură în ecuația mediei (sup @{mpq.p.msup}, $p$ @{mpq.p.pmsup})')]),
    T('To 2019: the break moves by one quarter (@{mpq.x.date}), variance ratio @{mpq.x.ratio}; the Great Moderation survived the 2008--2009 recession', 'Pînă în 2019: ruptura se mută cu un trimestru (@{mpq.x.date}), raportul varianțelor @{mpq.x.ratio}; Marea Moderație a supraviețuit recesiunii din 2008--2009'),
    (T('To 2026: sup-Wald falls to @{mpq.e.sup} ($p$ @{mpq.e.psup}) and the ratio to @{mpq.e.ratio}: two outliers (@{mpq.mind}: @{mpq.min}\\%) dominate the post-break variance', 'Pînă în 2026: sup-Wald scade la @{mpq.e.sup} ($p$ @{mpq.e.psup}) și raportul la @{mpq.e.ratio}: două valori extreme (@{mpq.mind}: @{mpq.min}\\%) domină varianța de după ruptură'),
     [T('a second break, or outliers? A one-break test cannot say; robust scale estimators or a second break are needed', 'o a doua ruptură sau valori extreme? Un test cu o singură ruptură nu poate decide; sînt necesari estimatori robuști ai scalei sau o a doua ruptură')])])

D.recap(('One break at an unknown date', 'o ruptură la o dată necunoscută'), [
    T('sup-Wald: the supremum of a squared Brownian bridge; trim, and use its own critical values', 'sup-Wald: supremumul unei punți browniene la pătrat; trunchiați și folosiți valorile critice proprii'),
    T('exp- and ave-Wald are optimal for moderate and small breaks', 'exp- și ave-Wald sînt optime pentru rupturi moderate și mici'),
    T('The date is estimated precisely, the CI comes from $\\arg\\max_s\\{W(s) - |s|/2\\}$', 'Data se estimează precis, intervalul de încredere vine din $\\arg\\max_s\\{W(s) - |s|/2\\}$'),
    T('Variance breaks: test the mean of $|\\hat e_t|$; outliers can mask or mimic them', 'Rupturile în varianță: testați media lui $|\\hat e_t|$; valorile extreme le pot ascunde sau imita')])

# =============================================================================
# 3. RUPTURI MULTIPLE
# =============================================================================
D.section('Multiple breaks: Bai and Perron', 'Rupturi multiple: Bai și Perron')

D.frame(T('The multiple-break model', 'Modelul cu rupturi multiple'), items(
    (T('$y_t = x_t\'\\beta + z_t\'\\delta_j + u_t$, $t = T_{j-1} + 1, \\dots, T_j$, $j = 1, \\dots, m + 1$, with $T_0 = 0$, $T_{m+1} = T$ \\refBPa', '$y_t = x_t\'\\beta + z_t\'\\delta_j + u_t$, $t = T_{j-1} + 1, \\dots, T_j$, $j = 1, \\dots, m + 1$, cu $T_0 = 0$, $T_{m+1} = T$ \\refBPa'),
     [T('pure change: no $x_t$; mean-shift model: $z_t = 1$', 'schimbare totală: fără $x_t$; modelul cu schimbări de medie: $z_t = 1$'),
      T('minimum segment length $h = [\\varepsilon T]$, usually $\\varepsilon = 0.15$; errors may be autocorrelated and heteroskedastic across regimes', 'lungimea minimă a unui segment $h = [\\varepsilon T]$, de obicei $\\varepsilon = 0{,}15$; erorile pot fi autocorelate și heteroscedastice între regimuri')]),
    (T('Estimator: the \\textbf{global} minimiser of the SSR over all admissible partitions $(T_1, \\dots, T_m)$', 'Estimatorul: minimul \\textbf{global} al SSR peste toate partițiile admisibile $(T_1, \\dots, T_m)$'),
     [T('break fractions consistent at rate $T$, as for one break; the dates are estimated jointly, not one at a time', 'fracțiile rupturilor sînt consistente cu rata $T$, ca pentru o ruptură; datele se estimează împreună, nu una cîte una')]),
    T('Brute force needs $O(T^m)$ regressions; dynamic programming needs $O(T^2)$ \\refBPb', 'Forța brută cere $O(T^m)$ regresii; programarea dinamică cere $O(T^2)$ \\refBPb')), 'small')

D.frame(T('Dynamic programming', 'Programarea dinamică'), items(
    (T('Step 1: compute $\\mathrm{SSR}(i, j)$ of one regression on every segment $[i, j]$ with $j - i + 1 \\ge h$ (recursive residuals: $O(T^2)$ operations)', 'Pasul 1: calculăm $\\mathrm{SSR}(i, j)$ al unei regresii pe fiecare segment $[i, j]$ cu $j - i + 1 \\ge h$ (reziduuri recursive: $O(T^2)$ operații)'), []),
    (T('Step 2: Bellman recursion for the best $r$-break partition of the first $n$ observations', 'Pasul 2: recursia Bellman pentru cea mai bună partiție cu $r$ rupturi a primelor $n$ observații'),
     [T('$\\mathrm{SSR}(\\{T_{r,n}\\}) = \\min_{rh \\le j \\le n - h}\\big[\\mathrm{SSR}(\\{T_{r-1,j}\\}) + \\mathrm{SSR}(j + 1, n)\\big]$', '$\\mathrm{SSR}(\\{T_{r,n}\\}) = \\min_{rh \\le j \\le n - h}\\big[\\mathrm{SSR}(\\{T_{r-1,j}\\}) + \\mathrm{SSR}(j + 1, n)\\big]$'),
      T('the optimal $m$-break partition contains optimal partitions of its prefixes (Bellman\'s principle)', 'partiția optimă cu $m$ rupturi conține partiții optime ale prefixelor ei (principiul lui Bellman)')]),
    (T('One pass gives the optimal partitions for every $m \\le M$: the input of all tests and criteria', 'O singură trecere dă partițiile optime pentru orice $m \\le M$: datele de intrare ale tuturor testelor și criteriilor'),
     [T('partial change ($\\beta$ common) needs an iteration between $\\beta$ and the partition \\refBPb; Seminar 2, A3 runs the recursion by hand', 'schimbarea parțială ($\\beta$ comun) cere o iterație între $\\beta$ și partiție \\refBPb; Seminarul 2, A3 parcurge recursia de mînă')])), 'small')

D.frame(T('Testing and selecting the number of breaks', 'Testarea și alegerea numărului de rupturi'), items(
    (T('$\\sup F_T(k)$: no break against exactly $k$ breaks, at the SSR-optimal partition, with robust variance \\refBPa', '$\\sup F_T(k)$: nicio ruptură față de exact $k$ rupturi, la partiția optimă după SSR, cu varianță robustă \\refBPa'),
     [T('\\textbf{UDmax} $= \\max_{k \\le M}\\sup F_T(k)$; \\textbf{WDmax} weights each $k$ by the ratio of critical values: no break against an unknown number', '\\textbf{UDmax} $= \\max_{k \\le M}\\sup F_T(k)$; \\textbf{WDmax} ponderează fiecare $k$ prin raportul valorilor critice: nicio ruptură față de un număr necunoscut')]),
    (T('\\textbf{Sequential} $\\sup F_T(\\ell + 1 \\mid \\ell)$: for each of the $\\ell + 1$ segments, the largest single-break statistic; add a break while it rejects', 'Testul \\textbf{secvențial} $\\sup F_T(\\ell + 1 \\mid \\ell)$: pentru fiecare dintre cele $\\ell + 1$ segmente, cea mai mare statistică pentru o ruptură; adăugăm o ruptură cît timp respinge'),
     [T('recommended strategy \\refBPb: UDmax or WDmax first, then the sequential tests', 'strategia recomandată \\refBPb: întîi UDmax sau WDmax, apoi testele secvențiale')]),
    (T('Information criteria: $\\mathrm{BIC}(m) = \\ln(\\mathrm{SSR}_m/T) + p^*\\ln T/T$; \\textbf{LWZ}: $\\ln\\frac{\\mathrm{SSR}_m}{T - p^*} + p^*\\frac{0.299}{T}(\\ln T)^{2.1}$ \\refLWZ', 'Criterii informaționale: $\\mathrm{BIC}(m) = \\ln(\\mathrm{SSR}_m/T) + p^*\\ln T/T$; \\textbf{LWZ}: $\\ln\\frac{\\mathrm{SSR}_m}{T - p^*} + p^*\\frac{0{,}299}{T}(\\ln T)^{2{,}1}$ \\refLWZ'),
     [T('$p^*$ counts coefficients and break dates; BIC picks too many breaks under serial correlation, LWZ too few with small breaks', '$p^*$ numără coeficienții și datele rupturilor; BIC alege prea multe rupturi cu autocorelație, LWZ prea puține cu rupturi mici')])), 'small')

D.frame(T('Case study: Bai and Perron (2003), the US real interest rate', 'Studiu de caz: Bai și Perron (2003), rata reală a dobînzii în SUA'), two(
    ph('volcker', T('Paul Volcker (left) and Ronald Reagan, December 1981', 'Paul Volcker (stînga) și Ronald Reagan, decembrie 1981'), h='0.33\\textheight'),
    items((T('The paper, Section 6.1: the ex-post real rate of \\refGP, quarterly 1961Q1--1986Q3 ($T = @{bp.n}$), mean-shift model, $\\varepsilon = 0.15$ ($h = @{bp.h}$), $M = 5$, HAC variances that differ across segments \\refBPb', 'Lucrarea, secțiunea 6.1: rata reală ex post din \\refGP, trimestrial T1 1961--T3 1986 ($T = @{bp.n}$), model cu schimbări de medie, $\\varepsilon = 0{,}15$ ($h = @{bp.h}$), $M = 5$, varianțe HAC diferite între segmente \\refBPb'),
           [T('our replication uses their data file (JAE data archive) and the same settings', 'replicarea noastră folosește fișierul lor de date (arhiva de date JAE) și aceleași setări')]),
          (T('Extension: the series rebuilt from FRED (T-bill rate at the end of the quarter minus next-quarter CPI inflation), correlation @{bpx.corr} with the original, 1961Q1--@{bpx.last}', 'Extensie: seria reconstruită din FRED (dobînda la titlurile de stat la sfîrșitul trimestrului minus inflația IPC din trimestrul următor), corelație @{bpx.corr} cu originalul, T1 1961--@{bpx.last}'), []),
          T('Question: how many regimes, and do they match the history of monetary policy?', 'Întrebarea: cîte regimuri și corespund ele istoriei politicii monetare?')), '0.36', '0.62'), 'footnotesize')

chart(T('Mean shifts in the US real interest rate', 'Schimbări de medie în rata reală a dobînzii din SUA'), 'ats_ch2_bai_perron', 'ATS_ch2_bai_perron', [
    T('Red: segment means of the BIC/LWZ partition; shaded: 95\\% intervals for the dates \\refBai, heterogeneous long-run variances. Top: original data; bottom: rebuilt to 2026',
      'Roșu: mediile segmentelor partiției alese de BIC/LWZ; umbrit: intervale de 95\\% pentru date \\refBai, varianțe de termen lung diferite. Sus: datele originale; jos: reconstruite pînă în 2026')], h='0.64\\textheight')

D.frame(T('Interpreting the Bai--Perron results', 'Interpretarea rezultatelor Bai--Perron'), table(
    'lcccccc', T('\\textbf{$m$}', '\\textbf{$m$}') + ' & 0 & 1 & 2 & 3 & 4 & 5',
    ['SSR & @{bp.ssr0} & @{bp.ssr1} & @{bp.ssr2} & @{bp.ssr3} & -- & --',
     '$\\sup F_T(m)$ & -- & @{bp.F1} & @{bp.F2} & @{bp.F3} & @{bp.F4} & @{bp.F5}',
     T('5\\% value', 'valoarea de 5\\%') + ' & -- & @{cv.F1} & @{cv.F2} & @{cv.F3} & -- & --',
     'BIC & @{bp.bic0} & @{bp.bic1} & @{bp.bic2} & @{bp.bic3} & -- & --',
     'LWZ & @{bp.lwz0} & @{bp.lwz1} & @{bp.lwz2} & @{bp.lwz3} & -- & --'], size='scriptsize') + items(
    (T('UDmax @{bp.ud} (5\\%: @{cv.ud}); sequential: $F(2|1) = @{bp.s1}$, $F(3|2) = @{bp.s2}$, $F(4|3) = @{bp.s3}$ (5\\%: @{cv.s1}, @{cv.s2}): @{bp.mseq} breaks, @{bp.d3}', 'UDmax @{bp.ud} (5\\%: @{cv.ud}); secvențial: $F(2|1) = @{bp.s1}$, $F(3|2) = @{bp.s2}$, $F(4|3) = @{bp.s3}$ (5\\%: @{cv.s1}, @{cv.s2}): @{bp.mseq} rupturi, @{bp.d3}'),
     [T('BIC and LWZ choose @{bp.mbic} breaks: @{bp.d2}; the dates are the ones reported by \\refBPb', 'BIC și LWZ aleg @{bp.mbic} rupturi: @{bp.d2}; datele sînt cele raportate de \\refBPb')]),
    T('Means @{bp.mu0}\\%, @{bp.mu1}\\%, @{bp.mu2}\\%: negative real rates in the 1970s, then the 1979--1981 disinflation; 95\\% intervals @{bp.ci0}, @{bp.ci1}', 'Mediile @{bp.mu0}\\%, @{bp.mu1}\\%, @{bp.mu2}\\%: rate reale negative în anii 1970, apoi dezinflația din 1979--1981; intervale de 95\\% @{bp.ci0}, @{bp.ci1}'),
    T('Extended sample: @{bpx.m} breaks (@{bpx.dates}); the last regime has a mean of @{bpx.mu3}\\%: the low-rate era after 2001, interval @{bpx.ci2}', 'Eșantionul extins: @{bpx.m} rupturi (@{bpx.dates}); ultimul regim are media @{bpx.mu3}\\%: era dobînzilor mici de după 2001, intervalul @{bpx.ci2}')), 'footnotesize')

chart(T('Mean shifts in Romanian inflation', 'Schimbări de medie în inflația din România'), 'ats_ch2_ro_inflation_breaks', 'ATS_ch2_ro_inflation_breaks', [
    T('HICP inflation, y/y, @{ri.first}--@{ri.last} ($T = @{ri.n}$), Bai--Perron mean shifts, $\\varepsilon = 0.15$, $M = 5$; red: the partition chosen by BIC and LWZ',
      'Inflația IAPC, anuală, @{ri.first}--@{ri.last} ($T = @{ri.n}$), schimbări de medie Bai--Perron, $\\varepsilon = 0{,}15$, $M = 5$; roșu: partiția aleasă de BIC și LWZ')], h='0.48\\textheight')

interp(('the Romanian inflation regimes', 'regimurilor inflației din România'), [
    (T('BIC and LWZ: @{ri.mbic} breaks (@{ri.dates}); means @{ri.mu0}\\%, @{ri.mu1}\\%, @{ri.mu2}\\%, @{ri.mu3}\\%', 'BIC și LWZ: @{ri.mbic} rupturi (@{ri.dates}); mediile @{ri.mu0}\\%, @{ri.mu1}\\%, @{ri.mu2}\\%, @{ri.mu3}\\%'),
     [T('disinflation, inflation targeting (adopted in August 2005), the low-inflation decade, the 2021--2023 surge', 'dezinflația, țintirea inflației (adoptată în august 2005), deceniul inflației scăzute, valul inflaționist din 2021--2023')]),
    (T('The robust sequential procedure stops at @{ri.mseq} break: $\\sup F(1) = @{ri.F1}$, but $F(2|1) = @{ri.s1}$', 'Procedura secvențială robustă se oprește la @{ri.mseq} ruptură: $\\sup F(1) = @{ri.F1}$, dar $F(2|1) = @{ri.s1}$'),
     [T('inflation is very persistent within regimes: the HAC variance absorbs the shifts, and the test loses power', 'inflația este foarte persistentă în interiorul regimurilor: varianța HAC absoarbe schimbările, iar testul își pierde puterea'),
      T('for the same reason the 95\\% intervals for the dates span years (second date: @{ri.ci1}); they are not drawn', 'din același motiv, intervalele de 95\\% pentru date acoperă ani întregi (a doua dată: @{ri.ci1}); nu sînt desenate')]),
    T('Better model: partial change in the intercept of an AR model, so that the errors are close to white noise (project idea)', 'Un model mai bun: schimbare parțială în termenul liber al unui model AR, astfel încît erorile să fie aproape de zgomot alb (idee de proiect)')])

D.frame(T('Change-point detection in statistics and machine learning', 'Detectarea punctelor de schimbare în statistică și machine learning'), items(
    (T('Penalised segmentation: minimise $\\sum_j \\mathrm{cost}(\\text{segment } j) + \\beta\\,m$ over partitions', 'Segmentare penalizată: minimizăm $\\sum_j \\mathrm{cost}(\\text{segmentul } j) + \\beta\\,m$ după partiții'),
     [T('PELT prunes the Bellman recursion to $O(T)$ under mild conditions \\refKFE; binary segmentation and wild binary segmentation \\refFry\\ scale to long series', 'PELT reduce recursia Bellman la $O(T)$ în condiții slabe \\refKFE; segmentarea binară și segmentarea binară aleatoare (wild binary segmentation) \\refFry\\ funcționează pe serii lungi'),
      T('the Python package \\texttt{ruptures} implements them \\refTOV; the BIC of Bai--Perron is a particular penalty', 'pachetul Python \\texttt{ruptures} le conține \\refTOV; BIC-ul din Bai--Perron este o penalizare particulară')]),
    (T('What econometrics adds: inference on the number of breaks and confidence intervals for dates under serial correlation', 'Ce adaugă econometria: inferența pentru numărul rupturilor și intervale de încredere pentru date cu autocorelație'),
     [T('common breaks in systems of equations \\refOP; survey \\refCP', 'rupturi comune în sisteme de ecuații \\refOP; sinteză \\refCP')]),
    T('Engineering practice tunes the penalty on labelled data; econometrics fixes the size of a test: both are valid if the choice is pre-registered', 'Practica inginerească ajustează penalizarea pe date etichetate; econometria fixează mărimea unui test: ambele sînt valide dacă alegerea este preînregistrată')), 'small')

D.recap(('Multiple breaks', 'rupturi multiple'), [
    T('Global least squares over all partitions, by dynamic programming in $O(T^2)$', 'Cele mai mici pătrate globale peste toate partițiile, prin programare dinamică în $O(T^2)$'),
    T('UDmax/WDmax, then sequential $F(\\ell + 1|\\ell)$; BIC and LWZ as a cross-check', 'UDmax/WDmax, apoi $F(\\ell + 1|\\ell)$ secvențial; BIC și LWZ ca verificare'),
    T('US real rate: breaks in 1972Q3 and 1980Q3 replicated; a further regime after 2001', 'Rata reală din SUA: rupturile din T3 1972 și T3 1980 replicate; încă un regim după 2001'),
    T('Persistent errors: robust tests lose power and date intervals become wide', 'Erori persistente: testele robuste își pierd puterea, iar intervalele pentru date devin largi')])

# =============================================================================
# 4. MONITORIZARE
# =============================================================================
D.section('Fluctuation tests and real-time monitoring', 'Teste de fluctuație și monitorizare în timp real')

D.frame(T('CUSUM and MOSUM tests', 'Testele CUSUM și MOSUM'), items(
    (T('Recursive residuals $w_t = (y_t - x_t\'\\hat\\beta_{t-1})/\\sqrt{1 + x_t\'(X_{t-1}\'X_{t-1})^{-1}x_t}$ are i.i.d.\\ $N(0, \\sigma^2)$ under $H_0$ with Normal errors \\refBDE', 'Reziduurile recursive $w_t = (y_t - x_t\'\\hat\\beta_{t-1})/\\sqrt{1 + x_t\'(X_{t-1}\'X_{t-1})^{-1}x_t}$ sînt i.i.d.\\ $N(0, \\sigma^2)$ sub $H_0$ cu erori Normale \\refBDE'),
     [T('CUSUM $W_r = \\hat\\sigma^{-1}\\sum_{t = k+1}^{r} w_t$ behaves like a Brownian motion; 5\\% boundary $\\pm 0.948[\\sqrt{T - k} + 2(r - k)/\\sqrt{T - k}]$', 'CUSUM $W_r = \\hat\\sigma^{-1}\\sum_{t = k+1}^{r} w_t$ se comportă ca o mișcare browniană; frontiera de 5\\% $\\pm 0{,}948[\\sqrt{T - k} + 2(r - k)/\\sqrt{T - k}]$'),
      T('detects changes in the intercept and a systematic drift of forecast errors; weak against changes that average out', 'detectează schimbări în termenul liber și o derivă sistematică a erorilor de prognoză; slab împotriva schimbărilor care se compensează')]),
    (T('OLS-CUSUM uses ordinary residuals: a Brownian bridge limit \\refPK; MOSUM sums over a moving window of fixed width \\refCHK', 'OLS-CUSUM folosește reziduurile obișnuite: limita este o punte browniană \\refPK; MOSUM însumează pe o fereastră mobilă de lățime fixă \\refCHK'),
     [T('MOSUM reacts faster to a break in the middle of the sample and to temporary changes', 'MOSUM reacționează mai repede la o ruptură în mijlocul eșantionului și la schimbări temporare')]),
    T('These are \\textbf{retrospective} tests: the whole sample is available when the test is run', 'Acestea sînt teste \\textbf{retrospective}: întregul eșantion este disponibil cînd se aplică testul')), 'small')

D.frame(T('Monitoring: why repeated tests fail', 'Monitorizarea: de ce eșuează testele repetate'), items(
    (T('A central bank estimates a model on $m$ historical observations and asks, at every new release, ``has it broken down?\'\'', 'O bancă centrală estimează un model pe $m$ observații istorice și întreabă, la fiecare nouă publicare, „s-a stricat?”'),
     [T('a 5\\% test repeated at $n = m + 1, m + 2, \\dots$ rejects a true $H_0$ eventually with probability 1: the law of the iterated logarithm', 'un test de 5\\% repetat la $n = m + 1, m + 2, \\dots$ respinge pînă la urmă o ipoteză nulă adevărată cu probabilitatea 1: legea logaritmului iterat')]),
    (T('\\refCSW: monitor $Q_n = \\hat\\sigma^{-1}\\sum_{t = m+1}^{n} w_t$ and stop the first time $|Q_n| > \\sqrt{n\\,[a^2 + \\ln(n/m)]}$', '\\refCSW: monitorizăm $Q_n = \\hat\\sigma^{-1}\\sum_{t = m+1}^{n} w_t$ și ne oprim prima dată cînd $|Q_n| > \\sqrt{n\\,[a^2 + \\ln(n/m)]}$'),
     [T('the boundary comes from \\refRS: $P\\{\\exists u \\ge 1: |W(u) - W(1)| \\ge \\sqrt{u(a^2 + \\ln u)}\\} = 2[1 - \\Phi(a) + a\\varphi(a)]$', 'frontiera vine din \\refRS: $P\\{\\exists u \\ge 1: |W(u) - W(1)| \\ge \\sqrt{u(a^2 + \\ln u)}\\} = 2[1 - \\Phi(a) + a\\varphi(a)]$'),
      T('$a^2 = 7.78$: size @{mo.size}\\% over an \\emph{infinite} horizon; $a^2 = 6.25$: @{mo.size2}\\%', '$a^2 = 7{,}78$: mărimea @{mo.size}\\% pe un orizont \\emph{infinit}; $a^2 = 6{,}25$: @{mo.size2}\\%')]),
    T('Forecast-based monitoring: forecast breakdowns \\refGRa\\ and the fluctuation test of relative accuracy \\refGRb\\ (Chapter 1)', 'Monitorizarea pe baza prognozelor: eșecul prognozelor \\refGRa\\ și testul de fluctuație al acurateței relative \\refGRb\\ (Capitolul 1)')), 'small')

chart(T('False alarms and real-time monitoring of Romanian inflation', 'Alarme false și monitorizarea în timp real a inflației din România'), 'ats_ch2_monitoring', 'ATS_ch2_monitoring', [
    T('Left: white noise, $m = 100$, @{mo.reps} replications; right: mean of monthly HICP inflation (m/m), historical sample 2015--2019, monitoring from January 2020',
      'Stînga: zgomot alb, $m = 100$, @{mo.reps} de replicări; dreapta: media inflației IAPC lunare, eșantion istoric 2015--2019, monitorizare din ianuarie 2020')], h='0.5\\textheight')

interp(('the monitoring results', 'rezultatelor monitorizării'), [
    (T('Repeated 5\\% tests raise a false alarm in @{mo.n1}\\% of samples by $n = 2m$ and in @{mo.n9}\\% by $n = 10m$; the CSW boundary in @{mo.c9}\\%', 'Testele de 5\\% repetate dau o alarmă falsă în @{mo.n1}\\% din eșantioane pînă la $n = 2m$ și în @{mo.n9}\\% pînă la $n = 10m$; frontiera CSW în @{mo.c9}\\%'),
     [T('the CSW size is reached only as $n \\to \\infty$: over a finite horizon the boundary is conservative', 'mărimea CSW se atinge doar cînd $n \\to \\infty$: pe un orizont finit frontiera este conservatoare')]),
    (T('Romania: historical mean @{mo.mean}\\% per month, $\\hat\\sigma = @{mo.s}$; the CUSUM crosses the boundary in @{mo.first}', 'România: media istorică @{mo.mean}\\% pe lună, $\\hat\\sigma = @{mo.s}$; CUSUM trece de frontieră în @{mo.first}'),
     [T('the repeated naive test would have signalled in @{mo.naive}; with a long-run $\\hat\\sigma$ (HAC) the signal comes only in @{mo.lr}', 'testul naiv repetat ar fi semnalat în @{mo.naive}; cu $\\hat\\sigma$ de termen lung (HAC) semnalul vine abia în @{mo.lr}')]),
    T('The price of a controlled false-alarm rate is delay: nearly two years after inflation started to rise in 2021', 'Prețul unei rate controlate a alarmelor false este întîrzierea: aproape doi ani după ce inflația a început să crească, în 2021')])

D.recap(('Monitoring', 'monitorizarea'), [
    T('CUSUM and MOSUM of recursive residuals: retrospective fluctuation tests', 'CUSUM și MOSUM ale reziduurilor recursive: teste de fluctuație retrospective'),
    T('Repeating a one-shot test as data arrive guarantees a false alarm', 'Repetarea unui test unic pe măsură ce sosesc datele garantează o alarmă falsă'),
    T('CSW boundary $\\sqrt{n[a^2 + \\ln(n/m)]}$ controls the size over an infinite horizon', 'Frontiera CSW $\\sqrt{n[a^2 + \\ln(n/m)]}$ controlează mărimea pe un orizont infinit'),
    T('Romanian inflation: detection in late 2022, a long but honest delay', 'Inflația din România: detectare la sfîrșitul lui 2022, o întîrziere lungă, dar onestă')])

# =============================================================================
# 5. RUPTURI ÎN VARIANȚĂ
# =============================================================================
D.section('Breaks in variance', 'Rupturi în varianță')

D.frame(T('The ICSS algorithm and its correction', 'Algoritmul ICSS și corecția lui'), items(
    (T('\\refIT: $C_k = \\sum_{t \\le k} a_t^2$, $D_k = C_k/C_T - k/T$; $\\mathrm{IT} = \\sqrt{T/2}\\max_k|D_k| \\Rightarrow \\sup|B^0(r)|$, 5\\% value 1.358', '\\refIT: $C_k = \\sum_{t \\le k} a_t^2$, $D_k = C_k/C_T - k/T$; $\\mathrm{IT} = \\sqrt{T/2}\\max_k|D_k| \\Rightarrow \\sup|B^0(r)|$, valoarea de 5\\% 1,358'),
     [T('ICSS: apply the test iteratively to sub-segments (binary segmentation), then re-check each break between its neighbours', 'ICSS: aplicăm testul iterativ pe subsegmente (segmentare binară), apoi reverificăm fiecare ruptură între vecinele ei')]),
    (T('The factor $\\sqrt{T/2}$ assumes $\\Var(a_t^2) = 2\\sigma^4$: i.i.d.\\ Normal data', 'Factorul $\\sqrt{T/2}$ presupune $\\Var(a_t^2) = 2\\sigma^4$: date i.i.d.\\ Normale'),
     [T('with kurtosis $\\kappa$ the statistic is inflated by $\\sqrt{(\\kappa - 1)/2}$; with GARCH, $a_t^2$ is also autocorrelated', 'cu coeficientul de boltire $\\kappa$, statistica este mărită de $\\sqrt{(\\kappa - 1)/2}$ ori; cu GARCH, $a_t^2$ este și autocorelat')]),
    (T('$\\kappa_2$ of \\refSAC: $\\max_k|C_k - (k/T)C_T|/\\sqrt{T\\hat\\omega_4}$, $\\hat\\omega_4$ the long-run variance of $a_t^2 - \\hat\\sigma^2$ (Bartlett)', '$\\kappa_2$ din \\refSAC: $\\max_k|C_k - (k/T)C_T|/\\sqrt{T\\hat\\omega_4}$, $\\hat\\omega_4$ varianța de termen lung a lui $a_t^2 - \\hat\\sigma^2$ (Bartlett)'),
     [T('same limit, valid under fat tails and conditional heteroskedasticity', 'aceeași limită, validă cu cozi groase și heteroscedasticitate condiționată')])), 'small')

chart(T('Variance regimes of EUR/RON', 'Regimuri de varianță pentru EUR/RON'), 'ats_ch2_variance_breaks', 'ATS_ch2_variance_breaks', [
    T('Daily log returns of the BNR reference rate, @{va.n} days; red ticks: ICSS with the Inclán--Tiao statistic; green ticks and shaded bands: ICSS with $\\kappa_2$',
      'Randamente logaritmice zilnice ale cursului de referință BNR, @{va.n} de zile; marcaje roșii: ICSS cu statistica Inclán--Tiao; marcaje verzi și benzi umbrite: ICSS cu $\\kappa_2$')], h='0.5\\textheight')

interp(('the EUR/RON variance breaks', 'rupturilor în varianța EUR/RON'), [
    (T('Excess kurtosis @{va.kurt}: the Inclán--Tiao statistic is @{va.it} and ICSS finds @{va.nit} breaks; $\\kappa_2 = @{va.k2}$ and @{va.nk2} breaks', 'Excesul de boltire @{va.kurt}: statistica Inclán--Tiao este @{va.it}, iar numărul rupturilor găsite de ICSS este @{va.nit}; $\\kappa_2 = @{va.k2}$, cu @{va.nk2} rupturi'),
     [T('most Inclán--Tiao ``breaks\'\' are volatility clusters, not changes of the unconditional variance', 'majoritatea „rupturilor” Inclán--Tiao sînt volatility clustering, nu schimbări ale varianței necondiționate')]),
    (T('$\\kappa_2$ dates: @{va.dates}', 'Datele $\\kappa_2$: @{va.dates}'),
     [T('the global financial crisis, the end of its turbulence, the calmer managed float after 2018; daily s.d.\\ between @{va.sdmin}\\% and @{va.sdmax}\\%', 'criza financiară globală, sfîrșitul turbulențelor ei, flotarea controlată mai calmă de după 2018; abaterea standard zilnică între @{va.sdmin}\\% și @{va.sdmax}\\%')]),
    T('For risk models (MFM, Chapter 5): a GARCH fitted across a variance break overstates persistence ($\\alpha + \\beta \\to 1$) \\refDI', 'Pentru modelele de risc (MFM, Capitolul 5): un GARCH estimat peste o ruptură în varianță supraestimează persistența ($\\alpha + \\beta \\to 1$) \\refDI')])

# =============================================================================
# 6. RĂDĂCINI UNITARE ȘI RUPTURI
# =============================================================================
D.section('Unit roots with breaks, revisited', 'Rădăcini unitare și rupturi, din nou')

D.frame(T('Beyond Zivot--Andrews', 'Dincolo de Zivot--Andrews'), items(
    (T('TSA, Chapter 3: a level shift mimics a unit root \\refPer; \\refZA\\ choose the date by minimising the ADF $t$ statistic', 'TSA, Capitolul 3: o schimbare de nivel imită o rădăcină unitară \\refPer; \\refZA\\ aleg data minimizînd statistica $t$ ADF'),
     [T('their null is a unit root \\emph{without} a break: a break under the null makes the test reject too often', 'ipoteza lor nulă este o rădăcină unitară \\emph{fără} ruptură: o ruptură sub ipoteza nulă face testul să respingă prea des')]),
    (T('Two breaks: \\refLP\\ minimise the $t$ statistic over two dates; \\refLS\\ propose an LM test whose null allows breaks', 'Două rupturi: \\refLP\\ minimizează statistica $t$ după două date; \\refLS\\ propun un test LM a cărui ipoteză nulă admite rupturi'),
     [T('\\refKPe: pre-test the break, then use a test valid under both hypotheses', '\\refKPe: testăm întîi ruptura, apoi folosim un test valid sub ambele ipoteze')]),
    T('Critical values depend on the model, the trimming and the number of breaks; a sieve bootstrap under the null avoids the tables', 'Valorile critice depind de model, de trunchiere și de numărul rupturilor; un bootstrap sieve sub ipoteza nulă evită tabelele')), 'small')

chart(T('Romanian GDP: unit root or broken trend?', 'PIB-ul României: rădăcină unitară sau trend cu rupturi?'), 'ats_ch2_unit_root_breaks', 'ATS_ch2_unit_root_breaks', [
    T('Log real GDP (SCA), @{ur.first}--@{ur.last}; one and two breaks in level and trend; null distributions from a sieve bootstrap (AR on $\\Delta y_t$, @{ur.B} replications)',
      'Logaritmul PIB real (ajustat sezonier), @{ur.first}--@{ur.last}; una și două rupturi în nivel și în trend; distribuții sub $H_0$ dintr-un bootstrap sieve (AR pe $\\Delta y_t$, @{ur.B} de replicări)')], h='0.5\\textheight')

interp(('the unit-root tests with breaks', 'testelor de rădăcină unitară cu rupturi'), [
    T('ADF with trend: @{ur.adf} ($p$ @{ur.adfp}); Zivot--Andrews: @{ur.za} at @{ur.zad} (5\\%: @{ur.zacv}; bootstrap $p$ @{ur.pone})', 'ADF cu trend: @{ur.adf} ($p$ @{ur.adfp}); Zivot--Andrews: @{ur.za} în @{ur.zad} (5\\%: @{ur.zacv}; $p$ bootstrap @{ur.pone})'),
    (T('Two breaks (@{ur.twod}): min-$t$ = @{ur.two}, bootstrap 5\\% value @{ur.cvtwo}, $p$ @{ur.ptwo}', 'Două rupturi (@{ur.twod}): min-$t$ = @{ur.two}, valoarea bootstrap de 5\\% @{ur.cvtwo}, $p$ @{ur.ptwo}'),
     [T('the more breaks we allow, the more negative the critical value: the apparent gain disappears', 'cu cît admitem mai multe rupturi, cu atît valoarea critică este mai negativă: cîștigul aparent dispare')]),
    T('With about 30 years of quarterly data a unit root cannot be rejected; the convergence story (fast growth, then a 2009 break) remains a hypothesis', 'Cu aproximativ 30 de ani de date trimestriale, rădăcina unitară nu poate fi respinsă; povestea convergenței (creștere rapidă, apoi o ruptură în 2009) rămîne o ipoteză')])

D.recap(('Breaks in variance and unit roots', 'rupturile în varianță și rădăcinile unitare'), [
    T('ICSS needs the $\\kappa_2$ correction for fat tails and GARCH', 'ICSS are nevoie de corecția $\\kappa_2$ pentru cozi groase și GARCH'),
    T('EUR/RON: a handful of genuine variance regimes, not dozens', 'EUR/RON: cîteva regimuri reale de varianță, nu zeci'),
    T('Unit-root tests with breaks: allow breaks under the null or pre-test them; bootstrap the critical values', 'Testele de rădăcină unitară cu rupturi: admiteți rupturi sub ipoteza nulă sau testați-le în prealabil; folosiți valori critice bootstrap')])

# =============================================================================
# 7. PROGNOZA ÎN PREZENȚA RUPTURILOR
# =============================================================================
D.section('Forecasting under breaks', 'Prognoza în prezența rupturilor')

D.frame(T('Location shifts cause forecast failure', 'Schimbările de nivel produc eșecul prognozelor'), items(
    (T('\\refCHa, \\refCHb: in equilibrium-correction models, a shift of the equilibrium mean is the main source of systematic forecast errors', '\\refCHa, \\refCHb: în modelele cu corecția erorii, deplasarea mediei de echilibru este principala sursă de erori sistematice de prognoză'),
     [T('after the shift, the model keeps pulling the forecast towards the old mean', 'după deplasare, modelul continuă să tragă prognoza spre vechea medie')]),
    (T('Robust devices', 'Instrumente robuste'),
     [T('\\textbf{intercept correction}: add the last observed error to the forecast', '\\textbf{corecția termenului liber}: adăugăm la prognoză ultima eroare observată'),
      T('\\textbf{differencing}: forecast $\\Delta y$; adapts after one period, at the cost of a larger variance', '\\textbf{diferențierea}: prognozăm $\\Delta y$; se adaptează după o perioadă, cu prețul unei varianțe mai mari'),
      T('\\textbf{shorter windows}: rolling estimation, or the post-break sample', '\\textbf{ferestre mai scurte}: estimare cu fereastră mobilă sau eșantionul de după ruptură')]),
    T('Survey of the evidence: \\refRos; window choice with time-varying parameters \\refIJR', 'Sinteza dovezilor: \\refRos; alegerea ferestrei cu parametri variabili în timp \\refIJR')), 'small')

D.frame(T('The choice of the estimation window', 'Alegerea ferestrei de estimare'), items(
    (T('Mean shift $\\delta$ after $n_1$ pre-break observations, $n_2$ post-break; forecast with the last $w \\ge n_2$ observations \\refPT', 'Schimbare de medie $\\delta$ după $n_1$ observații înainte de ruptură, $n_2$ după; prognozăm cu ultimele $w \\ge n_2$ observații \\refPT'),
     [T('$\\mathrm{MSFE}(w) = \\sigma^2\\big(1 + \\tfrac1w\\big) + \\Big(\\dfrac{(w - n_2)\\delta}{w}\\Big)^2$: variance falls with $w$, squared bias grows', '$\\mathrm{MSFE}(w) = \\sigma^2\\big(1 + \\tfrac1w\\big) + \\Big(\\dfrac{(w - n_2)\\delta}{w}\\Big)^2$: varianța scade cu $w$, pătratul deplasării crește'),
      T('the optimal window includes \\emph{some} pre-break data when $\\delta/\\sigma$ is small or $n_2$ short (Seminar 2, A8)', 'fereastra optimă include \\emph{cîteva} date dinaintea rupturii cînd $\\delta/\\sigma$ este mic sau $n_2$ scurt (Seminarul 2, A8)')]),
    (T('Feasible rules: estimate the date (Bai--Perron) and use the post-break sample; cross-validate $w$ \\refPT; average forecasts across windows (AveW) \\refPP', 'Reguli aplicabile: estimăm data (Bai--Perron) și folosim eșantionul de după ruptură; alegem $w$ prin validare încrucișată \\refPT; mediem prognozele peste ferestre (AveW) \\refPP'),
     [T('the date is estimated with error exactly when the break is small: post-break windows are then too short', 'data este estimată cu eroare exact cînd ruptura este mică: ferestrele de după ruptură sînt atunci prea scurte')])), 'small')

chart(T('Window choice: simulation and Romanian inflation', 'Alegerea ferestrei: simulare și inflația din România'), 'ats_ch2_forecast_windows', 'ATS_ch2_forecast_windows', [
    T('Left: $T = 200$, break $n_2 = 20$ periods before the end, @{wi.reps} replications, MSFE relative to the post-break mean with the true date; right: AR(2), one month ahead, cumulated squared-error gains over the expanding window',
      'Stînga: $T = 200$, ruptura cu $n_2 = 20$ de perioade înainte de final, @{wi.reps} de replicări, MSFE relativ la media de după ruptură cu data adevărată; dreapta: AR(2), o lună înainte, cîștigurile cumulate în eroarea pătratică față de fereastra extinsă')], h='0.5\\textheight')

interp(('the window choice', 'alegerii ferestrei'), [
    (T('Simulation: without a break the expanding window wins (@{wi.exp0}); with $\\delta = 1$: expanding @{wi.exp1}, rolling @{wi.roll1}, AveW @{wi.ave1}, estimated post-break @{wi.est1}', 'Simulare: fără ruptură cîștigă fereastra extinsă (@{wi.exp0}); cu $\\delta = 1$: extinsă @{wi.exp1}, mobilă @{wi.roll1}, AveW @{wi.ave1}, după ruptura estimată @{wi.est1}'),
     [T('$\\delta = 2$: @{wi.exp2}, @{wi.roll2}, @{wi.ave2}, @{wi.est2}: estimating the date pays when the break is large', '$\\delta = 2$: @{wi.exp2}, @{wi.roll2}, @{wi.ave2}, @{wi.est2}: estimarea datei merită cînd ruptura este mare')]),
    (T('Romania, $P = @{wr.n}$ months: RMSE expanding @{wr.exp}, rolling 60: @{wr.r60}, rolling 120: @{wr.r120}, AveW @{wr.ave} pp', 'România, $P = @{wr.n}$ de luni: RMSE extinsă @{wr.exp}, mobilă 60: @{wr.r60}, mobilă 120: @{wr.r120}, AveW @{wr.ave} pp'),
     [T('HLN against expanding: AveW @{wd.ave} ($p$ @{wd.avep}), rolling 60 @{wd.r60} ($p$ @{wd.r60p}); all gains arrive in 2022, the RMSE in 2021--2023 falls from @{wr.exps} to @{wr.aves}', 'HLN față de fereastra extinsă: AveW @{wd.ave} ($p$ @{wd.avep}), mobilă 60 @{wd.r60} ($p$ @{wd.r60p}); toate cîștigurile apar în 2022, RMSE în 2021--2023 scade de la @{wr.exps} la @{wr.aves}')]),
    T('Averaging across windows is a cheap insurance: never far from the best window, without estimating any date', 'Medierea peste ferestre este o asigurare ieftină: niciodată departe de cea mai bună fereastră, fără a estima vreo dată')])

D.recap(('Forecasting under breaks', 'prognoza în prezența rupturilor'), [
    T('Location shifts drive forecast failure; intercept correction and differencing make forecasts robust', 'Schimbările de nivel produc eșecul prognozelor; corecția termenului liber și diferențierea fac prognozele robuste'),
    T('Optimal window: a bias--variance trade-off that may include pre-break data', 'Fereastra optimă: un compromis deplasare--varianță care poate include date dinaintea rupturii'),
    T('AveW is robust when the break is uncertain; post-break windows when it is large and well dated', 'AveW este robustă cînd ruptura este incertă; ferestrele de după ruptură, cînd ea este mare și bine datată'),
    T('Evaluate the window choice out of sample with DM--HLN \\refDM, \\refHLN\\ (Chapter 1)', 'Evaluați alegerea ferestrei în afara eșantionului cu DM--HLN \\refDM, \\refHLN\\ (Capitolul 1)')])

# =============================================================================
# 8. MODELE CU PRAG
# =============================================================================
D.section('Threshold autoregression', 'Autoregresia cu prag')

D.frame(T('Why nonlinear dynamics', 'Motivația modelelor neliniare'), two(
    ph('lynx', T('Canada lynx', 'Linx canadian'), h='0.36\\textheight'),
    items((T('Linear models are symmetric: a shock of $-1$ has the mirror effect of a shock of $+1$, at every state', 'Modelele liniare sînt simetrice: un șoc de $-1$ are efectul în oglindă al unui șoc de $+1$, în orice stare'),
           [T('business cycles: unemployment rises fast in recessions and falls slowly in expansions \\refNef', 'ciclurile economice: șomajul crește repede în recesiuni și scade lent în expansiuni \\refNef'),
            T('arbitrage: real exchange rates move freely inside a band of transaction costs, revert outside it \\refMNP', 'arbitrajul: cursurile reale se mișcă liber în interiorul unei benzi a costurilor de tranzacție și revin în afara ei \\refMNP')]),
          (T('Ecology: the 9--10 year cycle of the Canadian lynx is asymmetric (slow rise, fast fall); a linear AR cannot produce a stable cycle without noise', 'Ecologie: ciclul de 9--10 ani al linxului canadian este asimetric (creștere lentă, scădere rapidă); un AR liniar nu poate produce un ciclu stabil fără zgomot'), []),
          T('A nonlinear model can: limit cycles, asymmetry, state-dependent persistence and impulse responses', 'Un model neliniar poate: cicluri limită, asimetrie, persistență și răspunsuri la impuls care depind de stare')), '0.36', '0.62'), 'footnotesize')

D.frame(T('Threshold and self-exciting threshold autoregression', 'Autoregresia cu prag și autoregresia cu prag autoexcitată'), items(
    (T('Two-regime \\textbf{TAR}: $y_t = (\\phi_{1,0} + \\phi_1\'\\mathbf y_{t-1})\\mathbf 1\\{q_{t-1} \\le \\gamma\\} + (\\phi_{2,0} + \\phi_2\'\\mathbf y_{t-1})\\mathbf 1\\{q_{t-1} > \\gamma\\} + \\varepsilon_t$', '\\textbf{TAR} cu două regimuri: $y_t = (\\phi_{1,0} + \\phi_1\'\\mathbf y_{t-1})\\mathbf 1\\{q_{t-1} \\le \\gamma\\} + (\\phi_{2,0} + \\phi_2\'\\mathbf y_{t-1})\\mathbf 1\\{q_{t-1} > \\gamma\\} + \\varepsilon_t$'),
     [T('$\\mathbf y_{t-1} = (y_{t-1}, \\dots, y_{t-p})\'$, threshold variable $q_{t-1}$, threshold $\\gamma$; variances may differ across regimes', '$\\mathbf y_{t-1} = (y_{t-1}, \\dots, y_{t-p})\'$, variabila de prag $q_{t-1}$, pragul $\\gamma$; varianțele pot diferi între regimuri'),
      T('\\textbf{SETAR}: $q_{t-1} = y_{t-d}$, the series itself with \\textbf{delay} $d$; notation SETAR$(k; p_1, \\dots, p_k)$ \\refTL', '\\textbf{SETAR}: $q_{t-1} = y_{t-d}$, seria însăși cu \\textbf{decalajul} $d$; notația SETAR$(k; p_1, \\dots, p_k)$ \\refTL')]),
    (T('Dynamics: the \\textbf{skeleton} $y_t = F(\\mathbf y_{t-1})$ (noise switched off) can converge to a point, a limit cycle or a chaotic attractor', 'Dinamica: \\textbf{scheletul} $y_t = F(\\mathbf y_{t-1})$ (fără zgomot) poate converge către un punct, un ciclu limită sau un atractor haotic'),
     [T('SETAR(2; 1, 1) is ergodic iff $\\phi_1 < 1$, $\\phi_2 < 1$ and $\\phi_1\\phi_2 < 1$: a regime may be explosive on its own (Seminar 2, A5)', 'SETAR(2; 1, 1) este ergodic dacă și numai dacă $\\phi_1 < 1$, $\\phi_2 < 1$ și $\\phi_1\\phi_2 < 1$: un regim poate fi exploziv luat separat (Seminarul 2, A5)')]),
    T('Survey of threshold models in economics: \\refHe', 'Sinteza modelelor cu prag în economie: \\refHe')), 'small')

D.frame(T('Estimation and inference', 'Estimare și inferență'), items(
    (T('Concentrated least squares: for each $\\gamma$ (and $d$) run OLS in both regimes; $\\hat\\gamma = \\arg\\min_\\gamma S_T(\\gamma)$ over the central 70\\% of the values of $q$', 'Cele mai mici pătrate concentrate: pentru fiecare $\\gamma$ (și $d$) aplicăm OLS în ambele regimuri; $\\hat\\gamma = \\arg\\min_\\gamma S_T(\\gamma)$ peste cele 70\\% centrale ale valorilor lui $q$'),
     [T('$\\hat\\gamma$ is super-consistent, $T(\\hat\\gamma - \\gamma) = O_p(1)$, with a nonstandard limit \\refChan; the slopes are asymptotically Normal as if $\\gamma$ were known', '$\\hat\\gamma$ este superconsistent, $T(\\hat\\gamma - \\gamma) = O_p(1)$, cu o limită nestandard \\refChan; pantele sînt asimptotic Normale ca și cum $\\gamma$ ar fi cunoscut')]),
    (T('Testing linearity: $\\gamma$ is not identified under $H_0$: $\\phi_1 = \\phi_2$ (the Davies problem again) \\refHa', 'Testarea liniarității: $\\gamma$ nu este identificat sub $H_0$: $\\phi_1 = \\phi_2$ (din nou problema Davies) \\refHa'),
     [T('$\\sup_\\gamma W_T(\\gamma)$ has a limit that depends on the data; \\textbf{fixed-regressor bootstrap}: $y_t^* = \\hat e_t\\eta_t$, $\\eta_t \\sim N(0, 1)$, same regressors, recompute $\\sup W^*$', '$\\sup_\\gamma W_T(\\gamma)$ are o limită care depinde de date; \\textbf{bootstrap cu regresori ficși}: $y_t^* = \\hat e_t\\eta_t$, $\\eta_t \\sim N(0, 1)$, aceiași regresori, recalculăm $\\sup W^*$')]),
    (T('Confidence set for the threshold \\refHc: invert $\\mathrm{LR}_T(\\gamma) = T\\,\\dfrac{S_T(\\gamma) - S_T(\\hat\\gamma)}{S_T(\\hat\\gamma)}$', 'Mulțimea de încredere pentru prag \\refHc: inversăm $\\mathrm{LR}_T(\\gamma) = T\\,\\dfrac{S_T(\\gamma) - S_T(\\hat\\gamma)}{S_T(\\hat\\gamma)}$'),
     [T('limit $\\xi = \\max_s[2W(s) - |s|]$, $P(\\xi \\le x) = (1 - e^{-x/2})^2$; 95\\% value $-2\\ln(1 - \\sqrt{0.95}) = 7.35$; divide LR by $\\hat\\eta^2$ under heteroskedasticity', 'limita $\\xi = \\max_s[2W(s) - |s|]$, $P(\\xi \\le x) = (1 - e^{-x/2})^2$; valoarea de 95\\% $-2\\ln(1 - \\sqrt{0{,}95}) = 7{,}35$; împărțim LR la $\\hat\\eta^2$ sub heteroscedasticitate')])), 'small')

D.frame(T('Case study: Tong and Lim (1980), the Canadian lynx', 'Studiu de caz: Tong și Lim (1980), linxul canadian'), items(
    (T('The paper, Section 9: $\\log_{10}$ of the yearly lynx trappings, 1821--1934; SETAR(2; 7, 2) with $d = 2$, threshold 3.116 \\refTL', 'Lucrarea, secțiunea 9: $\\log_{10}$ din numărul anual de linxi capturați, 1821--1934; SETAR(2; 7, 2) cu $d = 2$, pragul 3,116 \\refTL'),
     [T('$d = 2$ has an ecological reading: a lynx is fully grown in the autumn of its second year', '$d = 2$ are o interpretare ecologică: un linx devine adult în toamna celui de-al doilea an')]),
    (T('Our replication with the threshold of the paper: lower regime $y_t = @{ly.a0} + @{ly.a1}y_{t-1} @{ly.a2}y_{t-2} + \\dots$ (seven lags), upper regime $@{ly.b0} + @{ly.b1}y_{t-1} @{ly.b2}y_{t-2}$', 'Replicarea noastră cu pragul din lucrare: regimul inferior $y_t = @{ly.a0} + @{ly.a1}y_{t-1} @{ly.a2}y_{t-2} + \\dots$ (șapte decalaje), regimul superior $@{ly.b0} + @{ly.b1}y_{t-1} @{ly.b2}y_{t-2}$'),
     [T('the lower regime reproduces the published coefficients to three decimals; the free least-squares threshold is @{ly.g} (SSR @{ly.ssr} against @{ly.ssrtl})', 'regimul inferior reproduce coeficienții publicați cu trei zecimale; pragul liber, după cele mai mici pătrate, este @{ly.g} (SSR @{ly.ssr} față de @{ly.ssrtl})')]),
    T('Question: does the fitted model generate the lynx cycle by itself?', 'Întrebarea: generează modelul estimat, singur, ciclul linxului?')), 'small')

chart(T('The lynx cycle and the SETAR skeleton', 'Ciclul linxului și scheletul SETAR'), 'ats_ch2_lynx', 'ATS_ch2_lynx', [
    T('Left: data and the estimated threshold; right: the skeleton iterated 60 years from the last observations, noise switched off',
      'Stînga: datele și pragul estimat; dreapta: scheletul iterat 60 de ani pornind de la ultimele observații, fără zgomot')], h='0.5\\textheight')

interp(('the lynx SETAR', 'modelului SETAR pentru linx'), [
    (T('The skeleton settles on a stable limit cycle of period @{ly.per} years: the model produces the cycle without any noise', 'Scheletul se stabilizează pe un ciclu limită stabil cu perioada de @{ly.per} ani: modelul produce ciclul fără niciun zgomot'),
     [T('a linear AR(11) needs noise to sustain the oscillation; its skeleton converges to the mean', 'un AR(11) liniar are nevoie de zgomot pentru a întreține oscilația; scheletul lui converge la medie')]),
    T('The rise is slow (lower regime, seven lags), the fall is fast (upper regime, an explosive AR(2) on its own): the asymmetry of the data', 'Creșterea este lentă (regimul inferior, șapte decalaje), scăderea rapidă (regimul superior, un AR(2) exploziv luat separat): asimetria din date'),
    T('Residual variance @{ly.v1} against @{ly.v2} for AR(11): a small in-sample gain, a large gain in the description of the dynamics', 'Varianța reziduală @{ly.v1} față de @{ly.v2} pentru AR(11): un cîștig mic în eșantion, un cîștig mare în descrierea dinamicii')])

D.frame(T('Case study: Hansen (1997), US unemployment', 'Studiu de caz: Hansen (1997), șomajul din SUA'), items(
    (T('The paper, Section 5: unemployment rate of men aged 20 and over (unemployed / labour force), monthly 1959.1--1996.7; $\\Delta y_t$ on a constant and 12 lags \\refHb', 'Lucrarea, secțiunea 5: rata șomajului bărbaților de 20 de ani și peste (șomeri / forța de muncă), lunar 1959.1--1996.7; $\\Delta y_t$ pe o constantă și 12 decalaje \\refHb'),
     [T('threshold variable $q_{t-1} = y_{t-1} - y_{t-d}$, $d = 2, \\dots, 12$: the recent trend of unemployment; trimming 15\\%', 'variabila de prag $q_{t-1} = y_{t-1} - y_{t-d}$, $d = 2, \\dots, 12$: tendința recentă a șomajului; trunchiere 15\\%'),
      T('robust sup-Wald test, bootstrap $p$-values (1000 replications); the LS estimate $\\hat d = 12$, $\\hat\\gamma = 0.302$, 95\\% interval [0.213; 0.340], 314 and 124 observations', 'test sup-Wald robust, valori $p$ bootstrap (1000 de replicări); estimarea LS $\\hat d = 12$, $\\hat\\gamma = 0{,}302$, intervalul de 95\\% [0,213; 0,340], 314 și 124 de observații')]),
    (T('Our replication: the same construction from the BLS series on FRED (today\'s seasonal adjustment), the same model, $d = 12$', 'Replicarea noastră: aceeași construcție din seriile BLS de pe FRED (ajustarea sezonieră de azi), același model, $d = 12$'), []),
    T('Question: is there a ``recession regime\'\' with different dynamics, and how precisely is its threshold estimated?', 'Întrebarea: există un „regim de recesiune” cu altă dinamică și cît de precis este estimat pragul lui?')), 'small')

chart(T('A threshold model for US unemployment', 'Un model cu prag pentru șomajul din SUA'), 'ats_ch2_unemp_tar', 'ATS_ch2_unemp_tar', [
    T('Left: heteroskedasticity-adjusted $\\mathrm{LR}^*(\\gamma)$, $d = 12$; the 95\\% set is where the curve lies below 7.35. Right: months in the rising-unemployment regime ($q_{t-1} > \\hat\\gamma$)',
      'Stînga: $\\mathrm{LR}^*(\\gamma)$ ajustat pentru heteroscedasticitate, $d = 12$; mulțimea de 95\\% este acolo unde curba se află sub 7,35. Dreapta: lunile din regimul cu șomaj în creștere ($q_{t-1} > \\hat\\gamma$)')], h='0.5\\textheight')

interp(('the unemployment TAR', 'modelului TAR pentru șomaj'), [
    (T('$\\hat\\gamma = @{ta.g}$ pp (paper: 0.302), regimes of @{ta.n1} and @{ta.n2} months, exactly the split of the paper; 95\\% set [@{ta.ci0}; @{ta.ci1}]', '$\\hat\\gamma = @{ta.g}$ pp (lucrarea: 0,302), regimuri de @{ta.n1} și @{ta.n2} de luni, exact împărțirea din lucrare; mulțimea de 95\\% [@{ta.ci0}; @{ta.ci1}]'),
     [T('sup-Wald @{ta.W}, bootstrap $p$ @{ta.p}; linearity is rejected at 5\\% for @{ta.nsig} of the 11 delays', 'sup-Wald @{ta.W}, $p$ bootstrap @{ta.p}; liniaritatea este respinsă la 5\\% pentru @{ta.nsig} din cele 11 decalaje')]),
    (T('Rising regime: intercept @{ta.b20}, AR(1) @{ta.b21}, AR(2) @{ta.b22}; other months: @{ta.b10}, @{ta.b11}, @{ta.b12}', 'Regimul de creștere: termen liber @{ta.b20}, AR(1) @{ta.b21}, AR(2) @{ta.b22}; celelalte luni: @{ta.b10}, @{ta.b11}, @{ta.b12}'),
     [T('increases feed on themselves; in expansions unemployment is close to a random walk with a slight downward drift', 'creșterile se autoalimentează; în expansiune șomajul este aproape un mers aleator cu o ușoară tendință descendentă')]),
    T('With today\'s data the SSR is smallest at $d = @{ta.dhat}$ ($\\hat\\gamma = @{ta.gd}$): the delay is fragile, the threshold effect is not; 1959--2019: $\\hat\\gamma = @{ta.xg}$, $p$ @{ta.xp}', 'Cu datele de azi, SSR este minim la $d = @{ta.dhat}$ ($\\hat\\gamma = @{ta.gd}$): decalajul este fragil, efectul de prag nu; 1959--2019: $\\hat\\gamma = @{ta.xg}$, $p$ @{ta.xp}')], 'footnotesize')

D.recap(('Threshold autoregression', 'autoregresia cu prag'), [
    T('A piecewise-linear AR switching on an observed variable; can generate limit cycles', 'Un AR liniar pe porțiuni care comută după o variabilă observată; poate genera cicluri limită'),
    T('$\\hat\\gamma$ super-consistent; slopes as if $\\gamma$ were known', '$\\hat\\gamma$ superconsistent; pantele ca și cum $\\gamma$ ar fi cunoscut'),
    T('Linearity tests need the bootstrap; threshold intervals invert LR with the value 7.35', 'Testele de liniaritate au nevoie de bootstrap; intervalele pentru prag inversează LR cu valoarea 7,35'),
    T('Lynx and unemployment: both landmark results replicate', 'Linxul și șomajul: ambele rezultate de referință se replică')])

# =============================================================================
# 9. TRANZIȚIE NETEDĂ
# =============================================================================
D.section('Smooth transition autoregression', 'Autoregresia cu tranziție netedă')

D.frame(T('STAR models', 'Modelele STAR'), items(
    (T('$y_t = \\phi_1\'\\mathbf x_t[1 - G(s_t; \\gamma, c)] + \\phi_2\'\\mathbf x_t G(s_t; \\gamma, c) + \\varepsilon_t$, $\\mathbf x_t = (1, y_{t-1}, \\dots, y_{t-p})\'$, $0 \\le G \\le 1$ \\refTer', '$y_t = \\phi_1\'\\mathbf x_t[1 - G(s_t; \\gamma, c)] + \\phi_2\'\\mathbf x_t G(s_t; \\gamma, c) + \\varepsilon_t$, $\\mathbf x_t = (1, y_{t-1}, \\dots, y_{t-p})\'$, $0 \\le G \\le 1$ \\refTer'),
     [T('\\textbf{LSTAR}: $G = [1 + \\exp\\{-\\gamma(s_t - c)/\\hat\\sigma_s\\}]^{-1}$: low and high values of $s_t$; $\\gamma \\to \\infty$ gives the TAR, $\\gamma \\to 0$ the linear AR', '\\textbf{LSTAR}: $G = [1 + \\exp\\{-\\gamma(s_t - c)/\\hat\\sigma_s\\}]^{-1}$: valori mici și mari ale lui $s_t$; $\\gamma \\to \\infty$ dă TAR, $\\gamma \\to 0$ dă AR liniar'),
      T('\\textbf{ESTAR}: $G = 1 - \\exp\\{-\\gamma(s_t - c)^2\\}$: small and large \\emph{deviations} from $c$, symmetric', '\\textbf{ESTAR}: $G = 1 - \\exp\\{-\\gamma(s_t - c)^2\\}$: \\emph{abateri} mici și mari de la $c$, simetric')]),
    (T('A continuum of regimes: smooth aggregation of many agents with different thresholds, or time aggregation, produces smooth switching', 'Un continuu de regimuri: agregarea mai multor agenți cu praguri diferite sau agregarea temporală produc o comutare netedă'),
     [T('dividing by $\\hat\\sigma_s$ makes $\\gamma$ scale free and easier to estimate', 'împărțirea la $\\hat\\sigma_s$ face ca $\\gamma$ să nu depindă de scală și să fie mai ușor de estimat')]),
    T('Survey with the modelling cycle (specification, estimation, evaluation): \\refVDTF', 'Sinteză cu ciclul de modelare (specificare, estimare, evaluare): \\refVDTF')), 'small')

D.frame(T('Testing linearity against STAR', 'Testarea liniarității față de STAR'), items(
    (T('Under $H_0$: $\\gamma = 0$, the parameters $c$ and $\\phi_2$ are not identified: replace $G$ by a third-order Taylor expansion around $\\gamma = 0$ \\refLST', 'Sub $H_0$: $\\gamma = 0$, parametrii $c$ și $\\phi_2$ nu sînt identificați: înlocuim $G$ printr-o dezvoltare Taylor de ordinul trei în jurul lui $\\gamma = 0$ \\refLST'),
     [T('auxiliary regression $\\hat\\varepsilon_t = \\beta_0\'\\mathbf x_t + \\beta_1\'\\tilde{\\mathbf x}_t s_t + \\beta_2\'\\tilde{\\mathbf x}_t s_t^2 + \\beta_3\'\\tilde{\\mathbf x}_t s_t^3 + v_t$, $\\tilde{\\mathbf x}_t$ without the constant', 'regresia auxiliară $\\hat\\varepsilon_t = \\beta_0\'\\mathbf x_t + \\beta_1\'\\tilde{\\mathbf x}_t s_t + \\beta_2\'\\tilde{\\mathbf x}_t s_t^2 + \\beta_3\'\\tilde{\\mathbf x}_t s_t^3 + v_t$, $\\tilde{\\mathbf x}_t$ fără constantă'),
      T('LM3: $\\beta_1 = \\beta_2 = \\beta_3 = 0$, an $F$ test with $3p$ restrictions; repeat for each candidate $s_t$ and take the smallest $p$-value', 'LM3: $\\beta_1 = \\beta_2 = \\beta_3 = 0$, un test $F$ cu $3p$ restricții; repetăm pentru fiecare $s_t$ candidat și alegem cea mai mică valoare $p$')]),
    (T('\\textbf{Choice of the family} \\refTer: test $H_{04}$: $\\beta_3 = 0$, then $H_{03}$: $\\beta_2 = 0 \\mid \\beta_3 = 0$, then $H_{02}$: $\\beta_1 = 0 \\mid \\beta_2 = \\beta_3 = 0$', '\\textbf{Alegerea familiei} \\refTer: testăm $H_{04}$: $\\beta_3 = 0$, apoi $H_{03}$: $\\beta_2 = 0 \\mid \\beta_3 = 0$, apoi $H_{02}$: $\\beta_1 = 0 \\mid \\beta_2 = \\beta_3 = 0$'),
     [T('strongest rejection of $H_{03}$: ESTAR; of $H_{04}$ or $H_{02}$: LSTAR (an ESTAR has no cubic term in its expansion)', 'cea mai puternică respingere pentru $H_{03}$: ESTAR; pentru $H_{04}$ sau $H_{02}$: LSTAR (un ESTAR nu are termen cubic în dezvoltare)')]),
    T('Estimation by nonlinear least squares, linear parameters concentrated out; evaluation by LM tests of no remaining nonlinearity and parameter constancy \\refET', 'Estimarea prin cele mai mici pătrate neliniare, cu parametrii liniari concentrați; evaluarea prin teste LM pentru neliniaritate reziduală și constanța parametrilor \\refET')), 'small')

D.frame(T('Case study: van Dijk, Teräsvirta and Franses (2002)', 'Studiu de caz: van Dijk, Teräsvirta și Franses (2002)'), items(
    (T('The paper, Section 7: unadjusted unemployment rate of US men aged 20+, June 1968--December 1999; estimation to 1989, forecasts for 1990--1999 \\refVDTF', 'Lucrarea, secțiunea 7: rata neajustată a șomajului bărbaților de 20 de ani și peste din SUA, iunie 1968--decembrie 1999; estimare pînă în 1989, prognoze pentru 1990--1999 \\refVDTF'),
     [T('$\\Delta y_t$ on a constant, 11 monthly dummies, $y_{t-1}$ and 15 lags of $\\Delta y_t$; transition variable $s_t = \\Delta_{12}y_{t-d}$, $d = 1, \\dots, 6$', '$\\Delta y_t$ pe o constantă, 11 variabile dummy lunare, $y_{t-1}$ și 15 decalaje ale lui $\\Delta y_t$; variabila de tranziție $s_t = \\Delta_{12}y_{t-d}$, $d = 1, \\dots, 6$'),
      T('their LSTAR with $d = 1$: $\\hat\\gamma = 23.15$, $\\hat c = 0.27$, residual s.d.\\ 0.92 of the AR', 'LSTAR-ul lor cu $d = 1$: $\\hat\\gamma = 23{,}15$, $\\hat c = 0{,}27$, abaterea standard reziduală 0,92 din cea a AR')]),
    (T('Our replication: the same series (BLS via FRED), sample, regressors and transition; the unrestricted lags, without their pruning of insignificant terms', 'Replicarea noastră: aceeași serie (BLS prin FRED), același eșantion, aceiași regresori și aceeași tranziție; decalajele nerestricționate, fără eliminarea termenilor nesemnificativi din lucrare'), []),
    T('Question: does an LSTAR beat the linear model out of sample?', 'Întrebarea: bate un LSTAR modelul liniar în afara eșantionului?')), 'small')

chart(T('An LSTAR for US unemployment', 'Un LSTAR pentru șomajul din SUA'), 'ats_ch2_unemp_lstar', 'ATS_ch2_unemp_lstar', [
    T('Left: the estimated transition function over time with the unemployment rate; right: $G$ as a function of $s_t = \\Delta_{12}y_{t-1}$, ours and the published one',
      'Stînga: funcția de tranziție estimată în timp, împreună cu rata șomajului; dreapta: $G$ ca funcție de $s_t = \\Delta_{12}y_{t-1}$, a noastră și cea publicată')], h='0.5\\textheight')

interp(('the LSTAR', 'modelului LSTAR'), [
    (T('LM3 $p$-values: $d = 1$: @{ls.p1}, $d = 2$: @{ls.p2}, $d = 3$: @{ls.p3}; for $d = 2$: $H_{04}$ @{ls.p24}, $H_{03}$ @{ls.p23}, $H_{02}$ @{ls.p22}: LSTAR', 'Valorile $p$ LM3: $d = 1$: @{ls.p1}, $d = 2$: @{ls.p2}, $d = 3$: @{ls.p3}; pentru $d = 2$: $H_{04}$ @{ls.p24}, $H_{03}$ @{ls.p23}, $H_{02}$ @{ls.p22}: LSTAR'),
     [T('as in the paper: weak evidence, strongest for $d = 2$, and it points to the logistic family', 'ca în lucrare: dovezi slabe, cele mai puternice pentru $d = 2$, care indică familia logistică')]),
    (T('$\\hat\\gamma = @{ls.g}$, $\\hat c = @{ls.c}$, residual s.d.\\ ratio @{ls.ratio}; the regime switches when unemployment has risen by about 0.3 pp in a year ($G > 0.5$ in @{ls.share}\\% of months)', '$\\hat\\gamma = @{ls.g}$, $\\hat c = @{ls.c}$, raportul abaterilor standard reziduale @{ls.ratio}; regimul se schimbă cînd șomajul a crescut cu aproximativ 0,3 pp într-un an ($G > 0{,}5$ în @{ls.share}\\% din luni)'),
     [T('AIC prefers the LSTAR (@{ls.aics} against @{ls.aicl}); BIC the linear model (@{ls.bicl} against @{ls.bics}): 18 extra parameters without pruning', 'AIC preferă LSTAR (@{ls.aics} față de @{ls.aicl}); BIC, modelul liniar (@{ls.bicl} față de @{ls.bics}): 18 parametri în plus, fără eliminare')]),
    T('1990--1999, one step: RMSE @{ls.rs} (LSTAR) against @{ls.rl} (AR), HLN @{ls.dm}, $p$ @{ls.dmp}: better, not significantly', '1990--1999, un pas: RMSE @{ls.rs} (LSTAR) față de @{ls.rl} (AR), HLN @{ls.dm}, $p$ @{ls.dmp}: mai bun, dar nu semnificativ')], 'footnotesize')

D.frame(T('Real exchange rates and purchasing power parity', 'Cursurile reale și paritatea puterii de cumpărare'), two(
    ph('cassel', T('Gustav Cassel (1866--1945)', 'Gustav Cassel (1866--1945)'), h='0.24\\textheight') + '\\\\[1mm]'
    + ph('bretton', T('Bretton Woods, July 1944', 'Bretton Woods, iulie 1944'), h='0.15\\textheight'),
    items((T('PPP (Cassel, 1918): $q_t = s_t - p_t + p_t^*$ should be stationary; after Bretton Woods ended (1973) unit-root tests rarely reject', 'PPC (Cassel, 1918): $q_t = s_t - p_t + p_t^*$ ar trebui să fie staționar; după sfîrșitul sistemului Bretton Woods (1973), testele de rădăcină unitară resping rar'),
           [T('first PPP puzzle: no mean reversion; second: half-lives of 3--5 years, too slow for nominal shocks', 'primul paradox PPC: nicio revenire la medie; al doilea: timpi de înjumătățire de 3--5 ani, prea lenți pentru șocuri nominale')]),
          (T('Transaction costs create a band of inaction: near parity $q_t$ is close to a random walk, far from it arbitrage pulls it back \\refMNP', 'Costurile de tranzacție creează o bandă de inacțiune: aproape de paritate $q_t$ este aproape un mers aleator, departe de ea arbitrajul îl trage înapoi \\refMNP'),
           [T('\\refTPS: ESTAR $q_t - \\mu = (q_{t-1} - \\mu)\\exp\\{-\\theta^2(q_{t-1} - \\mu)^2\\} + \\varepsilon_t$', '\\refTPS: ESTAR $q_t - \\mu = (q_{t-1} - \\mu)\\exp\\{-\\theta^2(q_{t-1} - \\mu)^2\\} + \\varepsilon_t$')]),
          T('PPP: purchasing power parity', 'PPC (PPP): paritatea puterii de cumpărare')), '0.34', '0.64'), 'footnotesize')

D.frame(T('Case study: Taylor, Peel and Sarno (2001)', 'Studiu de caz: Taylor, Peel și Sarno (2001)'), items(
    (T('The paper: monthly real dollar rates of sterling, mark, franc and yen, 1973M01--1996M12, IMF IFS data, $q(1973M01) = 0$; ESTAR with $p = d = 1$ and $\\beta_1 = -\\beta_1^* = 1$ (eq.\\ 8) \\refTPS', 'Lucrarea: cursurile reale lunare ale lirei sterline, mărcii, francului și yenului față de dolar, 1973M01--1996M12, date FMI IFS, $q(1973M01) = 0$; ESTAR cu $p = d = 1$ și $\\beta_1 = -\\beta_1^* = 1$ (ec.\\ 8) \\refTPS'),
     [T('dollar--sterling: $\\hat\\theta^2 = 0.452$, $\\hat\\mu = -0.149$, $s = 0.033$; Monte Carlo $p$-value of $\\hat\\theta$ under a random walk 0.002', 'dolar--liră: $\\hat\\theta^2 = 0{,}452$, $\\hat\\mu = -0{,}149$, $s = 0{,}033$; valoarea $p$ Monte Carlo a lui $\\hat\\theta$ sub un mers aleator 0,002'),
      T('half-lives from generalised impulse responses conditional on the average history: under one year for a 40\\% shock, just under three years for 1\\%', 'timpi de înjumătățire din răspunsuri la impuls generalizate, condiționate de istoria medie: sub un an pentru un șoc de 40\\%, puțin sub trei ani pentru 1\\%')]),
    (T('Our replication for dollar--sterling: end-of-month DEXUSUK, US CPI (CPIAUCNS), UK CPI (OECD to 1987, then ONS); same model, same half-life procedure; extension to @{es.last}', 'Replicarea noastră pentru dolar--liră: DEXUSUK la sfîrșit de lună, IPC SUA (CPIAUCNS), IPC britanic (OECD pînă în 1987, apoi ONS); același model, aceeași procedură pentru timpii de înjumătățire; extensie pînă în @{es.last}'), []),
    T('Question: is the real exchange rate nonlinearly mean reverting, and how fast?', 'Întrebarea: revine cursul real neliniar la medie și cît de repede?')), 'small')

chart(T('Nonlinear mean reversion of the real dollar--sterling rate', 'Revenirea neliniară la medie a cursului real dolar--liră'), 'ats_ch2_ppp_estar', 'ATS_ch2_ppp_estar', [
    T('Left: $q_t$ and the estimated equilibria; right: generalised impulse responses of the 1973--1996 ESTAR, shocks of 1--40\\%, averaged over the observed histories',
      'Stînga: $q_t$ și echilibrele estimate; dreapta: răspunsurile la impuls generalizate ale ESTAR 1973--1996, șocuri de 1--40\\%, mediate peste istoriile observate')], h='0.5\\textheight')

interp(('the ESTAR', 'modelului ESTAR'), [
    (T('1973--1996: $\\hat\\theta^2 = @{es.th}$ (s.e.\\ @{es.thse}), $\\hat\\mu = @{es.mu}$, $s = @{es.s}$; Monte Carlo $p$-value of the $t$-ratio @{es.pmc} (paper: 0.002)', '1973--1996: $\\hat\\theta^2 = @{es.th}$ (eroarea standard @{es.thse}), $\\hat\\mu = @{es.mu}$, $s = @{es.s}$; valoarea $p$ Monte Carlo a raportului $t$ @{es.pmc} (lucrarea: 0,002)'),
     [T('$\\theta^2$ and $s$ are close to the paper; $\\mu$ differs because the UK CPI of the paper (IFS) is not the series published today', '$\\theta^2$ și $s$ sînt apropiate de lucrare; $\\mu$ diferă pentru că IPC britanic din lucrare (IFS) nu este seria publicată astăzi')]),
    (T('Half-lives: 1\\% shock @{es.h01} months, 10\\% @{es.h10}, 40\\% @{es.h40}; linear AR(1): @{es.hlar} months; from equilibrium: @{es.e01} months for 1\\%', 'Timpi de înjumătățire: șoc de 1\\% @{es.h01} luni, 10\\% @{es.h10}, 40\\% @{es.h40}; AR(1) liniar: @{es.hlar} de luni; din echilibru: @{es.e01} de luni pentru 1\\%'),
     [T('large deviations die out fast: the second PPP puzzle is a feature of small shocks', 'abaterile mari se sting repede: al doilea paradox PPC este o trăsătură a șocurilor mici')]),
    T('Dickey--Fuller: @{es.df} ($p$ @{es.dfp}); its power against our ESTAR is @{es.pow}\\%; KSS \\refKSS: @{es.kss} ($p$ @{es.ksp}) to 1996, @{es.kssx} ($p$ @{es.ksxp}) to 2026', 'Dickey--Fuller: @{es.df} ($p$ @{es.dfp}); puterea lui față de ESTAR-ul nostru este @{es.pow}\\%; KSS \\refKSS: @{es.kss} ($p$ @{es.ksp}) pînă în 1996, @{es.kssx} ($p$ @{es.ksxp}) pînă în 2026')], 'footnotesize')

D.recap(('Smooth transition', 'tranziția netedă'), [
    T('LSTAR: asymmetry between low and high states; ESTAR: small and large deviations', 'LSTAR: asimetrie între stările joase și înalte; ESTAR: abateri mici și mari'),
    T('LM tests from a Taylor expansion avoid the identification problem; the sequence $H_{04}$, $H_{03}$, $H_{02}$ chooses the family', 'Testele LM dintr-o dezvoltare Taylor evită problema identificării; secvența $H_{04}$, $H_{03}$, $H_{02}$ alege familia'),
    T('Unemployment: the published LSTAR replicates; its forecast gain is small', 'Șomajul: LSTAR-ul publicat se replică; cîștigul lui de prognoză este mic'),
    T('PPP: half-lives depend on the size of the shock; the evidence for nonlinearity depends on the sample', 'PPC: timpii de înjumătățire depind de mărimea șocului; dovezile de neliniaritate depind de eșantion')])

# =============================================================================
# 10. TESTE DE NELINIARITATE
# =============================================================================
D.section('Nonlinearity tests', 'Teste de neliniaritate')

D.frame(T('General and specific tests', 'Teste generale și teste specifice'), items(
    (T('\\textbf{BDS} \\refBDSL: correlation integral $C_{m}(\\varepsilon)$ of $m$-histories; under i.i.d.\\ $C_m = C_1^m$; applied to the residuals of a linear model', '\\textbf{BDS} \\refBDSL: integrala de corelație $C_{m}(\\varepsilon)$ a istoriilor de lungime $m$; sub i.i.d.\\ $C_m = C_1^m$; se aplică reziduurilor unui model liniar'),
     [T('power against any dependence left in the residuals, including ARCH: a rejection does not say which nonlinearity', 'putere împotriva oricărei dependențe rămase în reziduuri, inclusiv ARCH: o respingere nu spune ce neliniaritate este')]),
    (T('\\textbf{Keenan} (squared fitted values) and the test of \\refTsa\\ (all cross products $y_{t-i}y_{t-j}$, orthogonalised): $F$ tests of second-order Volterra terms', '\\textbf{Keenan} (valorile ajustate la pătrat) și testul din \\refTsa\\ (toate produsele $y_{t-i}y_{t-j}$, ortogonalizate): teste $F$ pentru termeni Volterra de ordinul doi'),
     [T('Tsay\'s arranged-autoregression test targets the TAR alternative \\refTsb', 'testul lui Tsay cu autoregresie ordonată vizează alternativa TAR \\refTsb')]),
    (T('\\textbf{LM3} (STAR) and \\textbf{sup-Wald} (TAR): specific alternatives, more power when they are right', '\\textbf{LM3} (STAR) și \\textbf{sup-Wald} (TAR): alternative specifice, mai multă putere cînd sînt corecte'),
     [T('caution: structural breaks, outliers and heteroskedasticity also reject linearity \\refCar', 'atenție: rupturile structurale, valorile extreme și heteroscedasticitatea resping și ele liniaritatea \\refCar')])), 'small')

chart(T('Five series, five tests', 'Cinci serii, cinci teste'), 'ats_ch2_nonlinearity_tests', 'ATS_ch2_nonlinearity_tests', [
    T('$p$-values; darker: stronger rejection of linearity. BDS on the AR residuals ($m = 3$, $\\varepsilon = \\hat\\sigma$); LM3 and sup-Wald with $s = q = y_{t-d}$; sup-Wald with 200 bootstrap replications',
      'Valori $p$; mai închis: respingere mai puternică a liniarității. BDS pe reziduurile AR ($m = 3$, $\\varepsilon = \\hat\\sigma$); LM3 și sup-Wald cu $s = q = y_{t-d}$; sup-Wald cu 200 de replicări bootstrap')], h='0.5\\textheight')

interp(('the test battery', 'bateriei de teste'), [
    T('Lynx and unemployment: every specific test rejects; the nonlinearity is real and of the threshold type', 'Linxul și șomajul: toate testele specifice resping; neliniaritatea este reală și de tipul cu prag'),
    (T('EUR/RON returns: BDS, Keenan, Tsay and LM3 all reject with $p$ @{nl.4.lm3_p}, yet the TAR sup-Wald does not ($p$ @{nl.4.supW_p})', 'Randamentele EUR/RON: BDS, Keenan, Tsay și LM3 resping toate cu $p$ @{nl.4.lm3_p}, dar sup-Wald pentru TAR nu ($p$ @{nl.4.supW_p})'),
     [T('volatility clustering and outliers, not a nonlinear conditional mean: the heteroskedasticity-robust test is the honest one', 'volatility clustering și valori extreme, nu o medie condiționată neliniară: testul robust la heteroscedasticitate este cel onest')]),
    T('Romanian GDP growth: only BDS and sup-Wald reject ($p$ @{nl.2.supW_p}): the 2009 and 2020 quarters act as a ``regime\'\'; a break or an outlier model may explain the same data', 'Creșterea PIB din România: doar BDS și sup-Wald resping ($p$ @{nl.2.supW_p}): trimestrele din 2009 și 2020 acționează ca un „regim”; un model cu ruptură sau cu valori extreme poate explica aceleași date')])

D.frame(T('Threshold cointegration', 'Cointegrarea cu prag'), items(
    (T('\\refBF: the error-correction term $z_t = y_t - \\beta x_t$ adjusts only outside a band: $\\Delta z_t = \\rho\\,z_{t-1}\\mathbf 1\\{|z_{t-1}| > \\gamma\\} + \\varepsilon_t$', '\\refBF: termenul de corecție a erorii $z_t = y_t - \\beta x_t$ se ajustează doar în afara unei benzi: $\\Delta z_t = \\rho\\,z_{t-1}\\mathbf 1\\{|z_{t-1}| > \\gamma\\} + \\varepsilon_t$'),
     [T('the same transaction-cost argument as ESTAR, for a pair of prices: commodity prices in two markets, interest-rate pass-through, the law of one price', 'același argument al costurilor de tranzacție ca la ESTAR, pentru o pereche de prețuri: prețul unei mărfuri pe două piețe, transmiterea dobînzilor, legea prețului unic')]),
    (T('Asymmetric adjustment (momentum TAR) \\refES; the test of linear against threshold VECM with a bootstrap \\refHS', 'Ajustare asimetrică (TAR cu momentum) \\refES; testul VECM liniar față de VECM cu prag, cu bootstrap \\refHS'),
     [T('Chapter 4 introduces the linear VECM and ARDL; threshold versions are a natural project extension', 'Capitolul 4 introduce VECM liniar și ARDL; variantele cu prag sînt o extensie naturală de proiect')]),
    T('Romanian example: pass-through from the BNR policy rate to ROBOR and to lending rates, with a band where banks do not adjust', 'Exemplu românesc: transmiterea de la dobînda de politică monetară a BNR la ROBOR și la dobînzile la credite, cu o bandă în care băncile nu se ajustează')), 'small')

# =============================================================================
# 11. PROGNOZE NELINIARE
# =============================================================================
D.section('Forecasting with nonlinear models', 'Prognoza cu modele neliniare')

D.frame(T('Multi-step forecasts are not the skeleton', 'Prognozele pe mai mulți pași nu sînt scheletul'), items(
    (T('For $h = 1$: $\\E(y_{t+1}\\mid\\mathcal F_t) = F(\\mathbf y_t)$; for $h \\ge 2$: $\\E[F(F(\\mathbf y_t) + \\varepsilon_{t+1}, \\dots)] \\ne F(F(\\mathbf y_t))$ (Jensen)', 'Pentru $h = 1$: $\\E(y_{t+1}\\mid\\mathcal F_t) = F(\\mathbf y_t)$; pentru $h \\ge 2$: $\\E[F(F(\\mathbf y_t) + \\varepsilon_{t+1}, \\dots)] \\ne F(F(\\mathbf y_t))$ (Jensen)'),
     [T('iterating the skeleton (the ``naive\'\' forecast) is biased; simulate paths with bootstrapped residuals and average them \\refCFS', 'iterarea scheletului (prognoza „naivă”) este deplasată; simulăm traiectorii cu reziduuri bootstrap și le mediem \\refCFS'),
      T('the predictive density can be skewed or bimodal: report densities, scored by the CRPS or the log score (Chapter 1)', 'densitatea predictivă poate fi asimetrică sau bimodală: raportați densități, evaluate cu CRPS sau scorul logaritmic (Capitolul 1)')]),
    (T('Evidence: nonlinear models rarely beat linear ones on average; gains concentrate in particular regimes (recessions) \\refMZTT, \\refTDM', 'Dovezi: modelele neliniare bat rar modelele liniare în medie; cîștigurile se concentrează în anumite regimuri (recesiuni) \\refMZTT, \\refTDM'),
     [T('evaluate conditionally: GW tests with the regime as instrument (Chapter 1); asymmetric dynamics in US unemployment \\refKPo', 'evaluați condiționat: teste GW cu regimul ca instrument (Capitolul 1); dinamica asimetrică a șomajului din SUA \\refKPo')])), 'small')

chart(T('TAR and AR forecasts of US unemployment', 'Prognoze TAR și AR pentru șomajul din SUA'), 'ats_ch2_nonlinear_forecasts', 'ATS_ch2_nonlinear_forecasts', [
    T('Hansen\'s TAR ($d = 12$) and a linear AR(12) in differences, parameters fixed at 1959--1996; forecasts of the level by 500 simulated paths, origins 1996--2019. Left: 12-month densities from @{nf.origin}',
      'TAR-ul lui Hansen ($d = 12$) și un AR(12) liniar în diferențe, parametri ficși din 1959--1996; prognoze ale nivelului prin 500 de traiectorii simulate, origini 1996--2019. Stînga: densitățile la 12 luni din @{nf.origin}')], h='0.5\\textheight')

interp(('the nonlinear forecasts', 'prognozelor neliniare'), [
    (T('From @{nf.origin} (before the 2008--2009 surge): TAR mean @{nf.tm}\\%, 90\\% range [@{nf.tq0}; @{nf.tq1}]; AR mean @{nf.am}\\%, [@{nf.aq0}; @{nf.aq1}]; outcome @{nf.actual}\\%', 'Din @{nf.origin} (înainte de creșterea din 2008--2009): media TAR @{nf.tm}\\%, intervalul de 90\\% [@{nf.tq0}; @{nf.tq1}]; media AR @{nf.am}\\%, [@{nf.aq0}; @{nf.aq1}]; realizarea @{nf.actual}\\%'),
     [T('the TAR density is skewed upwards once unemployment starts rising; neither model foresaw the size of the recession', 'densitatea TAR este asimetrică spre valori mari odată ce șomajul începe să crească; niciun model nu a anticipat mărimea recesiunii')]),
    (T('$P = @{nf.n}$ months: RMSE at 1 month @{nf.1.t} (TAR) against @{nf.1.a} (AR), HLN @{nf.1.dm} ($p$ @{nf.1.p}); at 12 months @{nf.12.t} against @{nf.12.a} ($p$ @{nf.12.p})', '$P = @{nf.n}$ de luni: RMSE la o lună @{nf.1.t} (TAR) față de @{nf.1.a} (AR), HLN @{nf.1.dm} ($p$ @{nf.1.p}); la 12 luni @{nf.12.t} față de @{nf.12.a} ($p$ @{nf.12.p})'),
     [T('in the @{nf.n2} rising-regime months the two are equal at 12 months (@{nf.12.t2} and @{nf.12.a2}): no regime-specific gain out of sample', 'în cele @{nf.n2} de luni din regimul de creștere cele două sînt egale la 12 luni (@{nf.12.t2} și @{nf.12.a2}): niciun cîștig specific regimului în afara eșantionului')]),
    T('A good in-sample nonlinearity is not a forecasting gain: pre-register the comparison', 'O neliniaritate bună în eșantion nu este un cîștig de prognoză: preînregistrați comparația')])

D.recap(('Nonlinearity tests and forecasts', 'testele de neliniaritate și prognozele'), [
    T('General tests (BDS, Keenan, Tsay) detect, specific ones (LM3, sup-Wald) describe', 'Testele generale (BDS, Keenan, Tsay) detectează, cele specifice (LM3, sup-Wald) descriu'),
    T('Heteroskedasticity, outliers and breaks also reject linearity', 'Heteroscedasticitatea, valorile extreme și rupturile resping și ele liniaritatea'),
    T('Multi-step nonlinear forecasts need simulation; report densities', 'Prognozele neliniare pe mai mulți pași cer simulare; raportați densități'),
    T('Out of sample, nonlinear models gain little on average; test where they should gain', 'În afara eșantionului, modelele neliniare cîștigă puțin în medie; testați acolo unde ar trebui să cîștige')])

# =============================================================================
# 12. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Nonlinearity or breaks? A few shifts of the mean can look like nonlinear mean reversion, and a threshold model can look like a sequence of breaks \\refCar, \\refDI', 'Neliniaritate sau rupturi? Cîteva schimbări ale mediei pot arăta ca o revenire neliniară la medie, iar un model cu prag poate arăta ca un șir de rupturi \\refCar, \\refDI'),
     [T('formal: is the KSS (ESTAR) rejection for the real dollar--sterling rate robust to Bai--Perron mean regimes estimated on the same data?', 'formal: rezistă respingerea KSS (ESTAR) pentru cursul real dolar--liră la regimurile de medie Bai--Perron estimate pe aceleași date?'),
      T('falsified if the rejection disappears once the null distribution accounts for the estimated breaks', 'infirmată dacă respingerea dispare odată ce distribuția sub ipoteza nulă ține cont de rupturile estimate')]),
    (T('Why it matters: half-lives, PPP and the credibility of exchange-rate models depend on which story is true', 'De ce contează: timpii de înjumătățire, PPC și credibilitatea modelelor de curs depind de povestea adevărată'),
     [T('literature to start from: \\refTPS, \\refKSS, \\refMNP, \\refCar, \\refBPb', 'literatura de pornire: \\refTPS, \\refKSS, \\refMNP, \\refCar, \\refBPb')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T('\\textbf{literature}: \\aiprompt{List peer-reviewed papers that test ESTAR real exchange rate models allowing for breaks in the mean; give DOIs.} Then check every DOI on Crossref', '\\textbf{literatura}: \\aiprompt{Listează articole recenzate care testează modele ESTAR pentru cursul real permițînd rupturi în medie; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T('\\textbf{hypothesis}: \\aiprompt{Propose a data-generating process with mean breaks and no nonlinearity that makes the KSS test reject.}', '\\textbf{ipoteza}: \\aiprompt{Propune un proces generator de date cu rupturi în medie și fără neliniaritate care face testul KSS să respingă.}'),
      T('\\textbf{code and replication}: reproduce first a number of this lecture (the KSS statistic to 2026), then the new procedure', '\\textbf{cod și replicare}: reproduceți întîi o cifră din acest curs (statistica KSS pînă în 2026), apoi noua procedură'),
      T('\\textbf{robustness and critique}: \\aiprompt{Act as a referee: list every way in which estimating breaks on the same data biases the test.}', '\\textbf{robustețe și critică}: \\aiprompt{Joacă rolul unui recenzent: enumeră toate felurile în care estimarea rupturilor pe aceleași date deplasează testul.}')]),
    T('Report: what was asked, what was kept, what was rejected (AI\\_USE.md, AI\\_ERRORS.md)', 'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\\_USE.md, AI\\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The null distribution reproduces the whole procedure: breaks estimated on each simulated series, not fixed at the observed dates', 'Distribuția sub ipoteza nulă reproduce întreaga procedură: rupturile se estimează pe fiecare serie simulată, nu se fixează la datele observate'),
    T('The number of breaks, the trimming and the criterion (BIC) are fixed before seeing the test result', 'Numărul rupturilor, trunchierea și criteriul (BIC) sînt fixate înainte de a vedea rezultatul testului'),
    T('The data are the published series (vintage, deflator, end of month); differences from the paper are reported', 'Datele sînt seriile publicate (versiunea, deflatorul, sfîrșitul lunii); diferențele față de lucrare sînt raportate'),
    T('``Not significant within regimes\'\' is not ``linear\'\': report the power of the procedure', '„Nesemnificativ în interiorul regimurilor” nu înseamnă „liniar”: raportați puterea procedurii')), 'small')

chart(T('Mini-case: ESTAR evidence or mean shifts?', 'Mini studiu de caz: dovezi ESTAR sau schimbări de medie?'), 'ats_ch2_ai_case', 'ATS_ch2_ai_case', [
    T('Left: real dollar--sterling rate with Bai--Perron mean regimes (BIC: three breaks, @{ai.dates}); right: KSS null distributions from @{ai.reps} random walks put through the same steps',
      'Stînga: cursul real dolar--liră cu regimurile de medie Bai--Perron (BIC: trei rupturi, @{ai.dates}); dreapta: distribuțiile KSS sub ipoteza nulă din @{ai.reps} de mersuri aleatoare trecute prin aceiași pași'),
    T('Demeaned: KSS @{ai.kr}, $p$ @{ai.pr} (5\\%: @{ai.cvr}); within regimes: @{ai.ks}, $p$ @{ai.ps} (5\\%: @{ai.cvs}): the evidence for ESTAR disappears once the break search is part of the null',
      'Cu media scăzută: KSS @{ai.kr}, $p$ @{ai.pr} (5\\%: @{ai.cvr}); în interiorul regimurilor: @{ai.ks}, $p$ @{ai.ps} (5\\%: @{ai.cvs}): dovezile pentru ESTAR dispar odată ce căutarea rupturilor face parte din ipoteza nulă')],
    h='0.46\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T('\\textbf{Regimes in Romanian inflation and the policy rate}: breaks, thresholds or both?', '\\textbf{Regimuri în inflația din România și în dobînda de politică monetară}: rupturi, praguri sau ambele?'),
     [T('replicate first: the Bai--Perron dates of this lecture and the TAR test of \\refHb\\ on the US data', 'replicați întîi: datele Bai--Perron din acest curs și testul TAR din \\refHb\\ pe datele din SUA'),
      T('extension: an AR model of Romanian inflation with a partial break in the intercept against an LSTAR in the 12-month change of inflation; pre-register the comparison (1--12 months, CRPS, Holm)', 'extensie: un model AR al inflației din România cu o ruptură parțială în termenul liber, față de un LSTAR în variația pe 12 luni a inflației; preînregistrați comparația (1--12 luni, CRPS, Holm)'),
      T('optional: threshold pass-through from the BNR rate to ROBOR (Chapter 4)', 'opțional: transmiterea cu prag de la dobînda BNR la ROBOR (Capitolul 4)')]),
    T('Deliverables follow the course rules: repository, report, AI\\_USE.md, AI\\_ERRORS.md, oral defence', 'Livrabilele urmează regulile cursului: repository, raport, AI\\_USE.md, AI\\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('A break date chosen from the data is a nuisance parameter: use sup/exp/ave tests with their own critical values', 'O dată a rupturii aleasă din date este un parametru neidentificat: folosiți testele sup/exp/ave cu valorile lor critice'),
    T('Bai--Perron: global LS by dynamic programming, UDmax and sequential tests, BIC/LWZ, intervals for the dates', 'Bai--Perron: cele mai mici pătrate globale prin programare dinamică, UDmax și teste secvențiale, BIC/LWZ, intervale pentru date'),
    T('Monitor with a CSW boundary; test variance breaks with $\\kappa_2$; bootstrap unit-root tests with breaks', 'Monitorizați cu o frontieră CSW; testați rupturile în varianță cu $\\kappa_2$; folosiți bootstrap pentru testele de rădăcină unitară cu rupturi'),
    T('TAR and STAR: test with the bootstrap or LM expansions, estimate by concentrated (N)LS, forecast by simulation', 'TAR și STAR: testați cu bootstrap sau cu dezvoltări LM, estimați prin (N)LS concentrate, prognozați prin simulare'),
    T('Breaks and nonlinearity mimic each other: test one allowing for the other', 'Rupturile și neliniaritatea se imită reciproc: testați-o pe una ținînd cont de cealaltă')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('Why is the 5\\% critical value of sup-Wald with one coefficient above 8, not 3.84?', 'De ce este valoarea critică de 5\\% a sup-Wald cu un coeficient peste 8, nu 3,84?'),
        T('What does dynamic programming save in the Bai--Perron estimator?', 'Ce economisește programarea dinamică în estimatorul Bai--Perron?'),
        T('Why does a repeated 5\\% test eventually raise a false alarm?', 'De ce dă pînă la urmă o alarmă falsă un test de 5\\% repetat?'),
        T('Why is the threshold of a TAR estimated at rate $T$?', 'De ce se estimează pragul unui TAR cu rata $T$?'),
        T('When does the half-life of an ESTAR depend on the shock?', 'Cînd depinde timpul de înjumătățire al unui ESTAR de șoc?'))),
    block(T('Next: SVAR and local projections', 'Urmează: VAR structural și proiecții locale'), items(
        T('Structural VAR and local projections: identification of shocks', 'Modele VAR structurale și proiecții locale: identificarea șocurilor'),
        T('State-dependent local projections extend this chapter\'s nonlinear models to impulse responses', 'Proiecțiile locale dependente de stare extind modelele neliniare din acest capitol la răspunsurile la impuls'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the limit of the sup-Wald statistic', 'Anexă: limita statisticii sup-Wald'), items(
    T('Mean shift, $\\sigma^2$ known: $W_T(\\pi) = \\dfrac{T\\pi(1 - \\pi)(\\bar y_1 - \\bar y_2)^2}{\\sigma^2}$, $\\bar y_1$, $\\bar y_2$ the means before and after $[\\pi T]$', 'Schimbare de medie, $\\sigma^2$ cunoscut: $W_T(\\pi) = \\dfrac{T\\pi(1 - \\pi)(\\bar y_1 - \\bar y_2)^2}{\\sigma^2}$, $\\bar y_1$, $\\bar y_2$ mediile înainte și după $[\\pi T]$'),
    T('With $S_T(r) = \\sigma^{-1}T^{-1/2}\\sum_{t \\le [rT]}(y_t - \\mu) \\Rightarrow B(r)$ (FCLT, Chapter 0): $\\bar y_1 - \\bar y_2 = \\dfrac{\\sigma}{\\sqrt T}\\Big[\\dfrac{S_T(\\pi)}{\\pi} - \\dfrac{S_T(1) - S_T(\\pi)}{1 - \\pi}\\Big]$', 'Cu $S_T(r) = \\sigma^{-1}T^{-1/2}\\sum_{t \\le [rT]}(y_t - \\mu) \\Rightarrow B(r)$ (FCLT, Capitolul 0): $\\bar y_1 - \\bar y_2 = \\dfrac{\\sigma}{\\sqrt T}\\Big[\\dfrac{S_T(\\pi)}{\\pi} - \\dfrac{S_T(1) - S_T(\\pi)}{1 - \\pi}\\Big]$'),
    T('The bracket equals $\\dfrac{S_T(\\pi) - \\pi S_T(1)}{\\pi(1 - \\pi)}$, so $W_T(\\pi) \\Rightarrow \\dfrac{[B(\\pi) - \\pi B(1)]^2}{\\pi(1 - \\pi)}$, a squared Brownian bridge over its variance', 'Paranteza este egală cu $\\dfrac{S_T(\\pi) - \\pi S_T(1)}{\\pi(1 - \\pi)}$, deci $W_T(\\pi) \\Rightarrow \\dfrac{[B(\\pi) - \\pi B(1)]^2}{\\pi(1 - \\pi)}$, o punte browniană la pătrat împărțită la varianța ei'),
    T('The continuous mapping theorem gives the limit of $\\sup_{\\pi \\in \\Pi}$; with $p$ coefficients, $B$ is $p$-dimensional; with an unknown $\\sigma^2$ or a HAC variance the limit is the same', 'Teorema funcțiilor continue dă limita lui $\\sup_{\\pi \\in \\Pi}$; cu $p$ coeficienți, $B$ este $p$-dimensională; cu $\\sigma^2$ necunoscut sau cu varianță HAC limita este aceeași')), 'small')

D.frame(T('Appendix: the critical value 7.35 of the threshold LR', 'Anexă: valoarea critică 7,35 a LR pentru prag'), items(
    T('\\refHc: with a shrinking threshold effect, $\\mathrm{LR}_T(\\gamma_0) \\to_d \\eta^2\\xi$, $\\xi = \\max_{s}[2W(s) - |s|]$, $W$ a two-sided Brownian motion', '\\refHc: cu un efect de prag care scade, $\\mathrm{LR}_T(\\gamma_0) \\to_d \\eta^2\\xi$, $\\xi = \\max_{s}[2W(s) - |s|]$, $W$ o mișcare browniană bilaterală'),
    T('For one side, $\\max_{s \\ge 0}[2W(s) - s]$ is exponential with mean 2: $P(\\cdot \\le x) = 1 - e^{-x/2}$ (the maximum of a Brownian motion with drift)', 'Pentru o parte, $\\max_{s \\ge 0}[2W(s) - s]$ este exponențial cu media 2: $P(\\cdot \\le x) = 1 - e^{-x/2}$ (maximul unei mișcări browniene cu derivă)'),
    T('The two sides are independent: $P(\\xi \\le x) = (1 - e^{-x/2})^2$; solving $(1 - e^{-x/2})^2 = 1 - \\alpha$ gives $c(\\alpha) = -2\\ln(1 - \\sqrt{1 - \\alpha})$', 'Cele două părți sînt independente: $P(\\xi \\le x) = (1 - e^{-x/2})^2$; din $(1 - e^{-x/2})^2 = 1 - \\alpha$ rezultă $c(\\alpha) = -2\\ln(1 - \\sqrt{1 - \\alpha})$'),
    T('$c(0.10) = 5.94$, $c(0.05) = 7.35$, $c(0.01) = 10.59$; under heteroskedasticity divide LR by $\\hat\\eta^2$ before comparing', '$c(0{,}10) = 5{,}94$, $c(0{,}05) = 7{,}35$, $c(0{,}01) = 10{,}59$; sub heteroscedasticitate împărțim LR la $\\hat\\eta^2$ înainte de comparare')), 'small')

D.frame(T('Appendix: the Taylor expansion behind LM3', 'Anexă: dezvoltarea Taylor din spatele LM3'), items(
    T('LSTAR: $G(s; \\gamma, c) - \\tfrac12 = \\tfrac14\\gamma(s - c) - \\tfrac{1}{48}\\gamma^3(s - c)^3 + O(\\gamma^5)$ around $\\gamma = 0$ (with $\\hat\\sigma_s = 1$)', 'LSTAR: $G(s; \\gamma, c) - \\tfrac12 = \\tfrac14\\gamma(s - c) - \\tfrac{1}{48}\\gamma^3(s - c)^3 + O(\\gamma^5)$ în jurul lui $\\gamma = 0$ (cu $\\hat\\sigma_s = 1$)'),
    T('Substituting in $\\phi_1\'\\mathbf x_t + (\\phi_2 - \\phi_1)\'\\mathbf x_t G$ and collecting powers of $s_t$ gives $\\beta_0\'\\mathbf x_t + \\sum_{k=1}^3\\beta_k\'\\tilde{\\mathbf x}_t s_t^k$, every $\\beta_k$ proportional to $\\gamma$', 'Înlocuind în $\\phi_1\'\\mathbf x_t + (\\phi_2 - \\phi_1)\'\\mathbf x_t G$ și grupînd puterile lui $s_t$ obținem $\\beta_0\'\\mathbf x_t + \\sum_{k=1}^3\\beta_k\'\\tilde{\\mathbf x}_t s_t^k$, fiecare $\\beta_k$ proporțional cu $\\gamma$'),
    T('So $H_0$: $\\gamma = 0$ becomes $\\beta_1 = \\beta_2 = \\beta_3 = 0$, testable without estimating $c$; the first-order expansion (LM1) has no power when only the intercept switches \\refLST', 'Deci $H_0$: $\\gamma = 0$ devine $\\beta_1 = \\beta_2 = \\beta_3 = 0$, testabilă fără a estima $c$; dezvoltarea de ordinul întîi (LM1) nu are putere cînd comută doar termenul liber \\refLST'),
    T('ESTAR: $1 - e^{-\\gamma(s - c)^2} = \\gamma(s - c)^2 + O(\\gamma^2)$: squares only, hence the decision rule of \\refTer', 'ESTAR: $1 - e^{-\\gamma(s - c)^2} = \\gamma(s - c)^2 + O(\\gamma^2)$: doar pătrate, de aici regula de decizie din \\refTer')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
