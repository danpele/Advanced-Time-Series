r"""
build_chapter4.py -- Capitolul 4 (Cointegrare: VECM, ARDL și date panel), EN + RO
==================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_04/ch4_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice). TSA, Capitolul 7 a predat Engle--Granger, ECM, ideea VECM,
testele Johansen și pairs trading; aici construim verosimilitatea, inferența, identificarea, ARDL și datele panel.
Ieșire:
  EN/Courses/chapter4_cointegration_vecm_ardl_panel.tex
  RO/Cursuri/capitol4_cointegrare_vecm_ardl_panel.tex
Rulare:
  python3 Quantlets/Ch_04/generate_all_charts.py
  python3 latex/build_chapter4.py && python3 latex/ats_build.py compile 4
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch4_common import REFS, QLURL, T, bib, finalize, load, minus_fix, pv, month   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(4, 'lecture', refs=REFS)
C = 'https://commons.wikimedia.org/wiki/File:'
P = V.put


def ql(folder):
    return f'\\quantlet{{{folder.replace("_", chr(92) + "_")}}}{{\\qlurl{{{folder}}}}}'


def chart(title, fig, folder, bullets, h='0.56\\textheight', size='footnotesize'):
    body = (f'\\begin{{center}}\n\\includegraphics[width=0.97\\textwidth,height={h},keepaspectratio]{{{fig}.pdf}}\n'
            f'\\end{{center}}\n\\vspace{{-0.25cm}}\n' + items(*bullets) + '\n' + ql(folder))
    D.frame(title, body, size)


def interp(title, bullets, size='small'):
    D.frame(T(f'Interpreting {title[0]}', f'Interpretarea {title[1]}'), items(*bullets), size)


FOTO = T('Photo', 'Foto')
PH = {
    'engle': ('ch4_engle_2017.jpg', C + 'Robert_Engle_SantiagoWEAI2017.png',
              FOTO + ': Econterms (2017); CC BY-SA 4.0; Wikimedia Commons'),
    'granger': ('ch1_granger_2008.jpg', C + 'Clive_Granger_by_Olaf_Storbeck.jpg',
                FOTO + ': Olaf Storbeck (2008); CC BY-SA 2.0; Wikimedia Commons'),
    'bnr': ('ch0_bnr_palace_2015.jpg', C + 'Bucharest_-_BNR_Palace_(19644434340).jpg',
            FOTO + ': Ștefan Jurcă (2015); CC BY 2.0; Wikimedia Commons'),
    'ecb': ('ch4_ecb_frankfurt_2015.jpg', C + 'Seat_of_the_European_Central_Bank_and_Frankfurt_Skyline_at_dawn_20150422_1.jpg',
            FOTO + ': DXR (2015); CC BY-SA 4.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


TB = '>{\\raggedright\\arraybackslash}'

# =============================================================================
# CIFRE
# =============================================================================
tab = N['trace']['table']
for c in range(1, 6):
    for m in range(1, 5):
        P(f'cv.{c}.{m}', tab[f'{c}|{m}'][1], 2)
V.int('sim.reps', N['trace']['reps'])
s = N['size']
for kind in ('iid', 'garch'):
    for Tn in ('50', '100', '200'):
        for i, k in enumerate(('as', 'ra', 'bo')):
            P(f'mc.{kind}.{Tn}.{k}', 100 * s[kind][Tn][i], 1)
V.raw('mc.reps', str(s['reps']))
V.raw('mc.B', str(s['B']))
pt = N['pt']
V.raw('pt.first', month(pt['first']))
V.raw('pt.last', month(pt['last']))
V.raw('pt.T', str(pt['T']))
V.raw('pt.p', str(pt['p']))
for k in ('aic', 'bic', 'hq'):
    V.raw(f'pt.ic.{k}', str(pt['ic'][k]))
for r in range(3):
    P(f'pt.tr{r}', pt['trace2'][r], 1)
    P(f'pt.cv{r}', pt['cv2'][r], 1)
    P(f'pt.ra{r}', pt['ra'][r], 1)
    V.raw(f'pt.bo{r}', pv(pt['boot'][r]))
    P(f'pt.tr4{r}', pt['trace4'][r], 1)
    P(f'pt.ra4{r}', pt['ra4'][r], 1)
    V.raw(f'pt.bo4{r}', pv(pt['boot4'][r]))
    P(f'pt.lam{r}', pt['lam'][r], 3)
P('pt.thl', pt['theta_l'], 2)
P('pt.thd', pt['theta_d'], 2)
P('pt.mkl', pt['mk_l'], 2)
P('pt.mkd', pt['mk_d'], 2)
P('pt.LRc', pt['LRc'], 2)
V.raw('pt.pc', pv(pt['pc']))
P('pt.LRl', pt['LRl'], 2)
V.raw('pt.pl', pv(pt['pl']))
P('pt.LRw', pt['LRw'], 2)
V.raw('pt.pw', pv(pt['pw']))
for i, nm in enumerate(('l', 'd', 'm')):
    for j in range(2):
        P(f'pt.a.{nm}{j}', pt['alpha'][i][j], 3)
P('pt.s0', pt['spread0'], 1)
P('pt.s1', pt['spread1'], 1)
P('pt.lmax', pt['lend_max'], 1)
P('pt.mmax', pt['mm_max'], 1)
P('pt.mmin', pt['mm_min'], 2)
P('pt.thl4', pt['theta_l4'], 2)
V.raw('pt.pl4', pv(pt['pl4']))
V.raw('pt.pc4', pv(pt['pc4']))
V.raw('pt.pw4', pv(pt['pw4']))
k = N['kpsw']
V.raw('kp.T', str(k['T']))
V.raw('kp.p', str(k['p']))
for r in range(3):
    P(f'kp.tr{r}', k['trace'][r], 1)
    P(f'kp.cv{r}', k['cv3'][r], 1)
    P(f'kp.tr4{r}', k['trace4'][r], 1)
    P(f'kp.cv4{r}', k['cv4'][r], 1)
P('kp.lr', k['lr'], 1)
V.raw('kp.plr', pv(k['plr']))
P('kp.lr4', k['lr4'], 2)
V.raw('kp.plr4', pv(k['plr4']))
P('kp.lrun', k['lrun'][0], 2)
P('kp.tr4c', k['tr4'][0], 3)
P('kp.tr4i', k['tr4'][1], 3)
for nm in ('c', 'i', 'y'):
    for j, h in enumerate((1, 4, 8, 12, 24)):
        P(f'kp.{nm}{h}', 100 * k['share'][nm][j], 0)
        P(f'kp.{nm}{h}lo', 100 * k['share_lo'][nm][j], 0)
        P(f'kp.{nm}{h}hi', 100 * k['share_hi'][nm][j], 0)
        P(f'kp.e.{nm}{h}', 100 * k['share_e'][nm][j], 0)
for yr in ('2019', '2025'):
    e = k['ext'][yr]
    for j, h in enumerate((1, 4, 8, 24)):
        P(f'kp.x{yr}.{h}', 100 * e['share_y'][j], 0)
    P(f'kp.x{yr}.lr', e['lr'], 1)
    V.raw(f'kp.x{yr}.T', str(e['T']))
P('kp.r0c', k['resp0'][0], 2)
P('kp.r0i', k['resp0'][1], 2)
P('kp.r0y', k['resp0'][2], 2)
V.raw('kp.B', str(k['B']))
i2 = N['i2']
P('i2.all', i2['t_all'], 2)
P('i2.it', i2['t_it'], 2)
P('i2.d2', i2['t_d2'], 2)
b = N['bounds']
for key in ('2|1', '3|1', '3|2', '3|3'):
    c_, kk = key.split('|')
    for q in ('0.90', '0.95', '0.99'):
        P(f'bd.{c_}.{kk}.{q[2:]}.lo', b['asym'][key][q][0], 2)
        P(f'bd.{c_}.{kk}.{q[2:]}.hi', b['asym'][key][q][1], 2)
P('bd.t.lo', b['tq']['0.05'][0], 2)
P('bd.t.hi', b['tq']['0.05'][1], 2)
for Tn in ('30', '50', '80', '250'):
    P(f'bd.s{Tn}.lo', b['small'][Tn]['0.95'][0], 2)
    P(f'bd.s{Tn}.hi', b['small'][Tn]['0.95'][1], 2)
P('bd.sT.lo', b['small_T']['0.95'][0], 2)
P('bd.sT.hi', b['small_T']['0.95'][1], 2)
P('bd.sT2.lo', b['small_T2']['0.95'][0], 2)
P('bd.sT2.hi', b['small_T2']['0.95'][1], 2)
V.int('bd.reps', b['reps'])
for nm in ('lend2', 'dep2'):
    r = b[nm]
    tag = nm[:-1]
    for kk in ('F', 't', 'theta', 'se'):
        P(f'ar.{tag}.{kk}', r[kk], 2)
    P(f'ar.{tag}.phi', r['phi'], 3)
    P(f'ar.{tag}.sephi', r['se_phi'], 3)
    P(f'ar.{tag}.hl', r['hl'], 0)
    V.raw(f'ar.{tag}.p', str(r['p']))
    V.raw(f'ar.{tag}.q', str(r['q']))
    V.raw(f'ar.{tag}.n', str(r['n']))
P('ar.lend3.F', b['lend3']['F'], 2)
for j, h in enumerate((0, 1, 3, 6, 12, 24, 36, 60)):
    P(f'ar.m{h}', b['mult'][j], 2)
pn = N['panel']
for kk in ('N', 'T', 'first', 'last', 'nobs'):
    V.raw(f'pn.{kk}', str(pn[kk]))
for v in ('c', 'y', 'pi'):
    P(f'pn.cd.{v}', pn['cd'][v]['CD'], 1)
    P(f'pn.rho.{v}', pn['cd'][v]['mean_abs_rho'], 2)
    for t_ in ('llc', 'ips', 'cips'):
        P(f'pn.{v}.{t_}', pn['ur'][f'{v}.{t_}']['stat'], 2)
        V.raw(f'pn.{v}.{t_}.p', pv(pn['ur'][f'{v}.{t_}']['p']))
        P(f'pn.{v}.{t_}.cv', pn['ur'][f'{v}.{t_}']['cv5'], 2)
for t_ in ('ped', 'wgt'):
    P(f'pn.{t_}', pn[t_]['stat'], 2)
    V.raw(f'pn.{t_}.p', pv(pn[t_]['p']))
    P(f'pn.{t_}.cv', pn[t_]['cv5'], 2)
for est in ('mg', 'pmg', 'dfe', 'cce', 'dols'):
    for j, nm in enumerate(('y', 'pi')):
        P(f'pn.{est}.{nm}', pn[est]['theta'][j], 2)
        P(f'pn.{est}.{nm}.se', pn[est]['se'][j], 2)
    if est in ('mg', 'pmg', 'dfe'):
        P(f'pn.{est}.phi', pn[est]['phi'], 2)
        P(f'pn.{est}.phi.se', pn[est]['phi_se'], 3)
P('pn.H', pn['H'], 2)
V.raw('pn.pH', pv(pn['pH']))
P('pn.cdpmg', pn['cd_pmg']['CD'], 1)
P('pn.thmin', pn['th_min'], 2)
P('pn.thmax', pn['th_max'], 2)
P('pn.thro', pn['th_ro'], 2)
V.int('pn.reps', pn['reps'])
ai = N['ai']
P('ai.min', ai['tmin'], 2)
P('ai.max', ai['tmax'], 2)
V.raw('ai.nrej', str(ai['nrej']))
V.raw('ai.n', str(ai['n']))
minus_fix(V)
for _k, _v in list(V.items()):   # '$p = 0.011$' or '$p < 0.001$' (never '$p = $<$0.001$')
    if isinstance(_v, str):
        V.raw(_k + '.e', '$p < ⁅0.001⁆$' if _v.startswith('$<$') else '$p = ' + _v + '$')

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: when do non-stationary series share a long-run equilibrium, which restrictions on it can we test, and how far can we trust the answer in samples of 100--300 observations or across 27 countries?',
       r'\textbf{Întrebarea}: cînd au serii nestaționare un echilibru comun pe termen lung, ce restricții asupra lui putem testa și cît ne putem baza pe răspuns în eșantioane de 100--300 de observații sau pentru 27 de țări?'),
     [T('cointegration is a statement about the likelihood of a reduced-rank VAR; inference on it is non-standard and fragile',
        'cointegrarea este o afirmație despre verosimilitatea unui VAR de rang redus; inferența asupra ei este nestandard și fragilă')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('the cointegrated VAR as a likelihood problem; the five deterministic cases; small-sample corrections and the bootstrap',
        'VAR-ul cointegrat ca problemă de verosimilitate; cele cinci cazuri deterministe; corecții pentru eșantioane mici și bootstrap'),
      T(r'identification and tests on $\beta$ and $\alpha$; interest-rate pass-through in Romania; I(2) in brief; common trends',
        r'identificarea și testele asupra lui $\beta$ și $\alpha$; transmiterea dobînzilor în România; I(2) pe scurt; trendurile comune'),
      T('ARDL and the bounds test; panel unit roots, panel cointegration and heterogeneous panel estimators',
        'ARDL și testul bounds; rădăcini unitare și cointegrare în panel; estimatori pentru panele eterogene')]),
    T('We build on TSA, Chapter 7 (Engle--Granger, ECM, the VECM, Johansen tests, pairs trading) and on Chapter 3 (structural identification); Seminar 4 comes before this lecture',
      'Pornim de la TSA, Capitolul 7 (Engle--Granger, ECM, VECM, testele Johansen, pairs trading) și de la Capitolul 3 (identificarea structurală); Seminarul 4 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Derive the Johansen estimator as a reduced-rank regression, state the asymptotic distribution of the trace statistic and choose the deterministic case',
      'Derivați estimatorul Johansen ca regresie de rang redus, enunțați distribuția asimptotică a statisticii trace și alegeți cazul determinist'),
    T('Correct the rank test in small samples (Reinsel--Ahn, Bartlett, wild bootstrap) and report the sensitivity of the rank to the lag length',
      'Corectați testul de rang în eșantioane mici (Reinsel--Ahn, Bartlett, bootstrap wild) și raportați sensibilitatea rangului la numărul de laguri'),
    T(r'Identify cointegrating vectors, test economic restrictions on $\beta$ and weak exogeneity through $\alpha$, and build a common-trends structural VECM',
      r'Identificați vectorii de cointegrare, testați restricții economice asupra lui $\beta$ și exogenitatea slabă prin $\alpha$ și construiți un VECM structural cu trenduri comune'),
    T('Run the ARDL bounds test with correct (and small-sample) critical values, and decide between ARDL and VECM',
      'Aplicați testul bounds ARDL cu valori critice corecte (și pentru eșantioane mici) și alegeți între ARDL și VECM'),
    T('Test for cross-section dependence, panel unit roots and panel cointegration, and estimate long-run panel relations by MG, PMG and CCE',
      'Testați dependența între unități, rădăcinile unitare și cointegrarea în panel și estimați relațiile de termen lung în panel prin MG, PMG și CCE')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Backbone: \refJohD; \refJus; \refKL, Ch.~3 and 10; \refPesD, Ch.~22--31; \refLut, Ch.~6--9', r'Bibliografia de bază: \refJohD; \refJus; \refKL, cap.~3 și 10; \refPesD, cap.~22--31; \refLut, cap.~6--9'),
     [T(r'original papers: \refJohA, \refJohB, \refPSSb, \refPSSa, \refPesA, \refPesB; survey: \refBrP', r'lucrările originale: \refJohA, \refJohB, \refPSSb, \refPSSa, \refPesA, \refPesB; sinteză: \refBrP')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_04}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_04}'),
     [T(r'Johansen in five cases, restricted ML, bootstrap rank tests, ARDL bounds, LLC/IPS/CIPS, Pedroni, Westerlund, MG, PMG and CCE written out in \texttt{numpy}',
        r'Johansen în cinci cazuri, ML cu restricții, teste de rang bootstrap, ARDL bounds, LLC/IPS/CIPS, Pedroni, Westerlund, MG, PMG și CCE scrise explicit în \texttt{numpy}')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter4_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter4_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{4.9cm}' + TB + 'p{4.6cm}' + TB + 'p{2.4cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizare}'),
    [T('Romanian lending and deposit rates (lei); ROBOR 3M', 'dobînzile la credite și la depozite în lei; ROBOR 3M') + ' & ' + T('IMF International Financial Statistics (BNR data); Eurostat irt\\_st\\_m', 'FMI, International Financial Statistics (date BNR); Eurostat irt\\_st\\_m') + ' & VECM, ARDL',
     T('US consumption of nondurables and services, fixed investment, GDP, deflator, population', 'consumul SUA de bunuri nedurabile și servicii, investițiile fixe, PIB, deflatorul, populația') + ' & FRED (PCND, PCESV, FPI, GDP, GDPDEF, B230RC0Q173SBEA) & ' + T('common trends', 'trenduri comune'),
     T('Romanian HICP, monthly', 'IAPC România, lunar') + ' & Eurostat prc\\_hicp\\_minr & I(2)',
     T('EU-27 household consumption, disposable income, consumption deflator, population', 'UE-27: consumul gospodăriilor, venitul disponibil, deflatorul consumului, populația') + ' & Eurostat nama\\_10\\_gdp, nasa\\_10\\_nf\\_tr, nama\\_10\\_pe & ' + T('panel', 'panel')],
    size='scriptsize') + items(
    T('All sources are public and need no account or key; monthly rates to March 2026, US data to 2025, EU annual data to 2024',
      'Toate sursele sînt publice și nu cer cont sau cheie; dobînzile lunare pînă în martie 2026, datele SUA pînă în 2025, datele anuale UE pînă în 2024'),
    T('HICP: harmonised index of consumer prices; NPISH: non-profit institutions serving households (included with households)',
      'IAPC (HICP): indicele armonizat al prețurilor de consum; consumul și venitul includ instituțiile fără scop lucrativ în serviciul gospodăriilor')), 'footnotesize')

D.frame(T('From spurious regressions to a likelihood theory', 'De la regresii false la o teorie a verosimilității'), two(
    ph('engle', T('Robert Engle, 2017', 'Robert Engle, 2017'), h='0.36\\textheight'),
    items(T(r'1987: \refEG\ define cointegration and prove the representation theorem; estimation is a two-step regression', r'1987: \refEG\ definesc cointegrarea și demonstrează teorema de reprezentare; estimarea este o regresie în doi pași'),
          T(r'1988--1991: \refJohA\ and \refJohB\ turn it into maximum likelihood for a VAR with reduced rank: several relations, tests on their coefficients', r'1988--1991: \refJohA\ și \refJohB\ o transformă în verosimilitate maximă pentru un VAR de rang redus: mai multe relații, teste asupra coeficienților lor'),
          T(r'1999--2001: Pesaran, Shin and Smith add ARDL bounds tests \refPSSb\ and pooled panels \refPSSa', r'1999--2001: Pesaran, Shin și Smith adaugă testele bounds ARDL \refPSSb\ și panelurile cu coeficienți comuni \refPSSa'),
          T('2003: Engle and Granger share the Nobel Prize; Granger ``for methods of analyzing economic time series with common trends (cointegration)\'\'', '2003: Engle și Granger primesc Premiul Nobel; Granger „pentru metode de analiză a seriilor de timp economice cu trenduri comune (cointegrare)”'),
          T('Since then: bootstrap rank tests, cross-section dependence in panels, common factors', 'De atunci: teste de rang bootstrap, dependența între unități în panel, factori comuni')), '0.36', '0.62'), 'footnotesize')

# =============================================================================
# 1. VAR COINTEGRAT
# =============================================================================
D.section('The cointegrated VAR as a likelihood problem', 'VAR-ul cointegrat ca problemă de verosimilitate')

D.frame(T('From TSA to this chapter', 'De la TSA la acest capitol'), items(
    (T(r'Known (TSA, Chapter 7): $y_t \sim$ I(1), $\beta\'y_t \sim$ I(0); Engle--Granger two-step; the ECM; $\Pi = \alpha\beta\'$; trace and max-eigenvalue tests with tabulated critical values',
       r'Cunoscut (TSA, Capitolul 7): $y_t \sim$ I(1), $\beta\'y_t \sim$ I(0); metoda Engle--Granger în doi pași; ECM; $\Pi = \alpha\beta\'$; testele trace și max-eigenvalue cu valori critice tabelate'),
     []),
    (T('New here', 'Nou aici'),
     [T('why the eigenvalue problem is the maximum likelihood estimator, and what its limit distribution looks like', 'de ce problema de valori proprii este estimatorul de verosimilitate maximă și cum arată distribuția ei limită'),
      T('which deterministic case to use, and what goes wrong in samples of 100--300 months', 'ce caz determinist folosim și ce probleme apar în eșantioane de 100--300 de luni'),
      T(r'restrictions on $\beta$ (economic hypotheses) and on $\alpha$ (weak exogeneity); structural shocks with permanent effects', r'restricții asupra lui $\beta$ (ipoteze economice) și asupra lui $\alpha$ (exogenitate slabă); șocuri structurale cu efecte permanente'),
      T('single equations (ARDL) and panels of countries when the system approach is too demanding', 'ecuații individuale (ARDL) și panele de țări atunci cînd abordarea de sistem cere prea mult')])), 'small')

D.frame(T(r'The VECM and the hypothesis $H(r)$ (1/2)', r'VECM și ipoteza $H(r)$ (1/2)'), items(
    T(r'The VECM: this month\'s change of each variable responds to last month\'s levels, to past changes and to deterministic terms \[ \Delta y_t = \Pi y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\Delta y_{t-i} + \Phi D_t + \varepsilon_t \]',
      r'VECM: modificarea de azi a fiecărei variabile depinde de nivelurile din perioada anterioară, de modificările trecute și de termenii determiniști \[ \Delta y_t = \Pi y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\Delta y_{t-i} + \Phi D_t + \varepsilon_t \]'),
    (T('Notation', 'Notațiile'),
     [T(r'$y_t \in \R^n$: the vector of the $n$ I(1) variables; $\Delta y_t = y_t - y_{t-1}$: their changes', r'$y_t \in \R^n$: vectorul celor $n$ variabile I(1); $\Delta y_t = y_t - y_{t-1}$: modificările lor'),
      T(r'$\Pi$ ($n\times n$): the long-run (levels) matrix; $\Gamma_i$ ($n\times n$): the short-run matrices; $p$: the lag order of the VAR in levels', r'$\Pi$ ($n\times n$): matricea de termen lung (a nivelurilor); $\Gamma_i$ ($n\times n$): matricele de termen scurt; $p$: ordinul de lag al VAR-ului în niveluri'),
      T(r'$D_t$: deterministic terms (constant, trend, dummies) with coefficients $\Phi$', r'$D_t$: termenii determiniști (constantă, trend, variabile dummy), cu coeficienții $\Phi$'),
      T(r'$\varepsilon_t \sim$ i.i.d. $N(0, \Omega)$: the innovations, with covariance matrix $\Omega$', r'$\varepsilon_t \sim$ i.i.d. $N(0, \Omega)$: inovațiile, cu matricea de covarianță $\Omega$')]),
    T(r'Gaussian likelihood conditional on the first $p$ observations: the estimator is ML, the tests are likelihood ratios \refJohA, \refJohB',
      r'Verosimilitate gaussiană condiționată de primele $p$ observații: estimatorul este ML, testele sînt rapoarte de verosimilitate \refJohA, \refJohB')), 'small')

D.frame(T(r'The VECM and the hypothesis $H(r)$ (2/2)', r'VECM și ipoteza $H(r)$ (2/2)'), items(
    (T(r'$H(r)$: $\Pi$ has rank at most $r$, so it factors as $\Pi = \alpha\beta\'$ with $\alpha, \beta$ of dimension $n\times r$',
       r'$H(r)$: $\Pi$ are rangul cel mult $r$, deci se scrie $\Pi = \alpha\beta\'$, cu $\alpha, \beta$ de dimensiune $n\times r$'),
     [T(r'$r$: the number of cointegrating relations, $0 \le r \le n$', r'$r$: numărul relațiilor de cointegrare, $0 \le r \le n$'),
      T(r'$\beta$: its columns are the $r$ cointegrating vectors; $\beta\'y_t$ is stationary (the long run)', r'$\beta$: coloanele sale sînt cei $r$ vectori de cointegrare; $\beta\'y_t$ este staționar (termenul lung)'),
      T(r'$\alpha$: the adjustment (loading) coefficients; $\alpha_{ij}$ is the response of $\Delta y_{i,t}$ to the deviation $\beta_j\'y_{t-1}$', r'$\alpha$: coeficienții de ajustare; $\alpha_{ij}$ este reacția lui $\Delta y_{i,t}$ la abaterea $\beta_j\'y_{t-1}$')]),
    (T(r'The models are nested: $H(0) \subset H(1) \subset \dots \subset H(n)$', r'Modelele sînt imbricate: $H(0) \subset H(1) \subset \dots \subset H(n)$'),
     [T(r'$H(n)$: unrestricted VAR in levels; $H(0)$: VAR in differences', r'$H(n)$: VAR nerestricționat în niveluri; $H(0)$: VAR în diferențe')]),
    (T(r'Only $\Pi$ is identified, not $\alpha$ and $\beta$ separately: $\alpha\beta\' = (\alpha\xi)(\beta\xi^{-1\prime})\'$',
       r'Doar $\Pi$ este identificat, nu și $\alpha$ și $\beta$ separat: $\alpha\beta\' = (\alpha\xi)(\beta\xi^{-1\prime})\'$'),
     [T(r'$\xi$: any invertible $r\times r$ matrix; $\xi^{-1\prime}$: the transpose of its inverse', r'$\xi$: orice matrice inversabilă de $r\times r$; $\xi^{-1\prime}$: transpusa inversei sale')])), 'small')

D.frame(T('Step 1: concentrating out the short run', 'Pasul 1: eliminarea dinamicii pe termen scurt'), items(
    (T(r'Regress $\Delta y_t$ and $y_{t-1}$ on $Z_{2t} = (\Delta y_{t-1}\', \dots, \Delta y_{t-p+1}\', D_t\')\'$ and keep the residuals (Frisch--Waugh)',
       r'Regresăm $\Delta y_t$ și $y_{t-1}$ pe $Z_{2t} = (\Delta y_{t-1}\', \dots, \Delta y_{t-p+1}\', D_t\')\'$ și păstrăm reziduurile (Frisch--Waugh)'),
     [T(r'$Z_{2t}$: all short-run regressors (lagged changes and deterministic terms)', r'$Z_{2t}$: toți regresorii de termen scurt (modificările cu lag și termenii determiniști)'),
      T(r'$R_{0t}$, $R_{1t}$: the residuals of $\Delta y_t$ and of $y_{t-1}$, i.e.\ both purged of the short run', r'$R_{0t}$, $R_{1t}$: reziduurile lui $\Delta y_t$ și ale lui $y_{t-1}$, adică ambele curățate de dinamica pe termen scurt')]),
    T(r'The concentrated model is a regression with a reduced-rank coefficient: $R_{0t} = \alpha\beta\'R_{1t} + \hat\varepsilon_t$',
      r'Modelul concentrat este o regresie cu un coeficient de rang redus: $R_{0t} = \alpha\beta\'R_{1t} + \hat\varepsilon_t$'),
    (T(r'Moment matrices $S_{ij} = T^{-1}\sum_t R_{it}R_{jt}\'$, $i, j \in \{0, 1\}$',
       r'Matricele de momente $S_{ij} = T^{-1}\sum_t R_{it}R_{jt}\'$, $i, j \in \{0, 1\}$'),
     [T(r'$T$: the number of observations used; $S_{00}$, $S_{11}$: the covariance matrices of $R_{0t}$, $R_{1t}$; $S_{01} = S_{10}\'$: their cross-covariance', r'$T$: numărul de observații folosite; $S_{00}$, $S_{11}$: matricele de covarianță ale lui $R_{0t}$, $R_{1t}$; $S_{01} = S_{10}\'$: covarianța lor încrucișată')]),
    (T(r'For fixed $\beta$, OLS of $R_{0t}$ on $\beta\'R_{1t}$ gives $\alpha$ and $\Omega$ in closed form:', r'Pentru $\beta$ fixat, OLS a lui $R_{0t}$ pe $\beta\'R_{1t}$ dă $\alpha$ și $\Omega$ în formă închisă:'),
     [T(r'$\hat\alpha(\beta) = S_{01}\beta(\beta\'S_{11}\beta)^{-1}$, $\hat\Omega(\beta) = S_{00} - S_{01}\beta(\beta\'S_{11}\beta)^{-1}\beta\'S_{10}$',
        r'$\hat\alpha(\beta) = S_{01}\beta(\beta\'S_{11}\beta)^{-1}$, $\hat\Omega(\beta) = S_{00} - S_{01}\beta(\beta\'S_{11}\beta)^{-1}\beta\'S_{10}$'),
      T(r'$L_{\max}(\beta)$: the likelihood maximised over all parameters except $\beta$; $L_{\max}^{-2/T}(\beta) \propto |\hat\Omega(\beta)|$ ($|\cdot|$: determinant)', r'$L_{\max}(\beta)$: verosimilitatea maximizată după toți parametrii, în afară de $\beta$; $L_{\max}^{-2/T}(\beta) \propto |\hat\Omega(\beta)|$ ($|\cdot|$: determinantul)'),
      T(r'what remains is a problem in $\beta$ alone: minimise $|\hat\Omega(\beta)|$', r'rămîne o problemă doar în $\beta$: minimizăm $|\hat\Omega(\beta)|$')])), 'small')

D.frame(T('Step 2: the eigenvalue problem', 'Pasul 2: problema de valori proprii'), items(
    T(r'Determinant identity: $|\hat\Omega(\beta)| = |S_{00}|\,\dfrac{|\beta\'(S_{11} - S_{10}S_{00}^{-1}S_{01})\beta|}{|\beta\'S_{11}\beta|}$',
      r'Identitatea determinanților: $|\hat\Omega(\beta)| = |S_{00}|\,\dfrac{|\beta\'(S_{11} - S_{10}S_{00}^{-1}S_{01})\beta|}{|\beta\'S_{11}\beta|}$'),
    (T(r'Minimising this ratio of quadratic forms is the generalised eigenvalue problem $|\lambda S_{11} - S_{10}S_{00}^{-1}S_{01}| = 0$',
       r'Minimizarea acestui raport de forme pătratice este problema generalizată de valori proprii $|\lambda S_{11} - S_{10}S_{00}^{-1}S_{01}| = 0$'),
     [T(r'its $n$ roots, ordered, are the eigenvalues $1 > \hat\lambda_1 > \dots > \hat\lambda_n > 0$; $\hat v_i$: the eigenvector of $\hat\lambda_i$', r'cele $n$ rădăcini, ordonate, sînt valorile proprii $1 > \hat\lambda_1 > \dots > \hat\lambda_n > 0$; $\hat v_i$: vectorul propriu al lui $\hat\lambda_i$')]),
    (T(r'$\hat\beta$ = the eigenvectors $\hat v_1, \dots, \hat v_r$ of the $r$ largest eigenvalues; then $L_{\max}^{-2/T} = |S_{00}|\prod_{i=1}^r(1 - \hat\lambda_i)$',
       r'$\hat\beta$ = vectorii proprii $\hat v_1, \dots, \hat v_r$ ai celor mai mari $r$ valori proprii; atunci $L_{\max}^{-2/T} = |S_{00}|\prod_{i=1}^r(1 - \hat\lambda_i)$'),
     [T(r'normalisation $\hat\beta\'S_{11}\hat\beta = I_r$ ($I_r$: the $r\times r$ identity matrix)', r'normalizarea $\hat\beta\'S_{11}\hat\beta = I_r$ ($I_r$: matricea identitate de $r\times r$)')]),
    T(r'$\hat\lambda_i$ are the squared canonical correlations between $R_{0t}$ and $R_{1t}$: large $\hat\lambda_i$ = a linear combination of levels that predicts the changes',
      r'$\hat\lambda_i$ sînt corelațiile canonice la pătrat dintre $R_{0t}$ și $R_{1t}$: un $\hat\lambda_i$ mare = o combinație liniară de niveluri care prezice modificările'),
    T(r'One eigen-decomposition gives the ML estimates for every $r$ at once (proof: Appendix)', r'O singură descompunere în valori proprii dă estimațiile ML pentru toate valorile lui $r$ deodată (demonstrația: Anexa)')), 'small')

D.frame(T('Likelihood ratio tests of the rank (1/2)', 'Teste de raport de verosimilitate pentru rang (1/2)'), items(
    (T(r'\textbf{Trace}: $H(r)$ against $H(n)$: $LR_{tr}(r) = -T\sum_{i=r+1}^{n}\ln(1 - \hat\lambda_i)$',
       r'\textbf{Trace}: $H(r)$ față de $H(n)$: $LR_{tr}(r) = -T\sum_{i=r+1}^{n}\ln(1 - \hat\lambda_i)$'),
     [T(r'sums the $n - r$ smallest eigenvalues, those that $H(r)$ sets to zero', r'însumează cele mai mici $n - r$ valori proprii, pe care $H(r)$ le consideră zero'),
      T(r'$\hat\lambda_i \approx 0$ gives $-\ln(1 - \hat\lambda_i) \approx 0$: a small statistic supports $H(r)$; large values reject it', r'$\hat\lambda_i \approx 0$ dă $-\ln(1 - \hat\lambda_i) \approx 0$: o statistică mică susține $H(r)$; valorile mari o resping')]),
    (T(r'\textbf{Maximum eigenvalue}: $H(r)$ against $H(r + 1)$: $LR_{\max}(r) = -T\ln(1 - \hat\lambda_{r+1})$',
       r'\textbf{Valoarea proprie maximă}: $H(r)$ față de $H(r + 1)$: $LR_{\max}(r) = -T\ln(1 - \hat\lambda_{r+1})$'),
     [T(r'uses only the next eigenvalue, $\hat\lambda_{r+1}$: is there one more relation?', r'folosește doar valoarea proprie următoare, $\hat\lambda_{r+1}$: mai există o relație?')]),
    T(r'Rank determination: test $r = 0, 1, \dots$ in turn and stop at the first non-rejection; this sequence is consistent for the true rank at a fixed level \refJohD',
      r'Determinarea rangului: testăm pe rînd $r = 0, 1, \dots$ și ne oprim la prima nerespingere; această secvență este consistentă pentru rangul adevărat la un nivel fixat \refJohD')), 'small')

D.frame(T('Likelihood ratio tests of the rank (2/2)', 'Teste de raport de verosimilitate pentru rang (2/2)'), items(
    T(r'Limit under $H(r)$: \[ LR_{tr} \Rightarrow \mathrm{tr}\Big\{\int_0^1 (dB)F\'\Big(\int_0^1 FF\'du\Big)^{-1}\int_0^1 F(dB)\'\Big\} \]',
      r'Limita sub $H(r)$: \[ LR_{tr} \Rightarrow \mathrm{tr}\Big\{\int_0^1 (dB)F\'\Big(\int_0^1 FF\'du\Big)^{-1}\int_0^1 F(dB)\'\Big\} \]'),
    (T('Notation', 'Notațiile'),
     [T(r'$\Rightarrow$: convergence in distribution as $T \to \infty$; $\mathrm{tr}$: the trace (sum of the diagonal elements)', r'$\Rightarrow$: convergența în distribuție cînd $T \to \infty$; $\mathrm{tr}$: urma matricei (suma elementelor diagonale)'),
      T(r'$B(u)$, $u \in [0, 1]$: an $(n - r)$-dimensional standard Brownian motion, the limit of the rescaled common trends', r'$B(u)$, $u \in [0, 1]$: o mișcare browniană standard de dimensiune $n - r$, limita trendurilor comune rescalate'),
      T(r'$F = B$ corrected for the deterministic terms of the case', r'$F = B$ corectat pentru termenii determiniști ai cazului')]),
    (T(r'The limit depends only on $n - r$ and the case, not on $\alpha, \beta, \Gamma_i, \Omega$',
       r'Limita depinde doar de $n - r$ și de caz, nu de $\alpha, \beta, \Gamma_i, \Omega$'),
     [T(r'a multivariate Dickey--Fuller distribution: quantiles by simulation \refOL, \refMHM', r'o distribuție Dickey--Fuller multivariată: cuantilele se obțin prin simulare \refOL, \refMHM'),
      T(r'non-standard: neither $\chi^2$ nor Normal', r'nestandard: nici $\chi^2$, nici distribuția Normală')])), 'small')

D.frame(T('The Granger representation theorem (1/3)', 'Teorema de reprezentare Granger (1/3)'), two(
    ph('granger', T('Clive Granger, 2008', 'Clive Granger, 2008'), h='0.33\\textheight'),
    items(T(r'The theorem writes a cointegrated VAR as random-walk trends plus stationary deviations',
            r'Teorema scrie un VAR cointegrat ca trenduri de tip mers aleator plus abateri staționare'),
          (T(r'VAR in levels: $y_t = \sum_{i=1}^{p}A_iy_{t-i} + \Phi D_t + \varepsilon_t$', r'VAR-ul în niveluri: $y_t = \sum_{i=1}^{p}A_iy_{t-i} + \Phi D_t + \varepsilon_t$'),
           [T(r'$A_i$ ($n\times n$): its lag matrices; $A(z) = I - \sum_{i=1}^{p}A_iz^i$: its characteristic polynomial', r'$A_i$ ($n\times n$): matricele lui de lag; $A(z) = I - \sum_{i=1}^{p}A_iz^i$: polinomul lui caracteristic'),
            T(r'$\Pi = -A(1)$, $\Gamma_i = -\sum_{j>i}A_j$: the VECM matrices; $\Gamma = I - \sum_i\Gamma_i$', r'$\Pi = -A(1)$, $\Gamma_i = -\sum_{j>i}A_j$: matricele VECM; $\Gamma = I - \sum_i\Gamma_i$')]),
          (T('Conditions', 'Condițiile'),
           [T(r'the roots of $|A(z)| = 0$ satisfy $|z| > 1$ or $z = 1$ (no explosive or seasonal roots)', r'rădăcinile lui $|A(z)| = 0$ satisfac $|z| > 1$ sau $z = 1$ (fără rădăcini explozive sau sezoniere)'),
            T(r'$\mathrm{rank}\,\Pi = r$, so $\Pi = \alpha\beta\'$', r'$\mathrm{rang}\,\Pi = r$, deci $\Pi = \alpha\beta\'$'),
            T(r'$\alpha_\perp\'\Gamma\beta_\perp$ has full rank $n - r$', r'$\alpha_\perp\'\Gamma\beta_\perp$ are rang complet, $n - r$'),
            T(r'$\alpha_\perp$, $\beta_\perp$ ($n\times(n - r)$): orthogonal complements, $\alpha\'\alpha_\perp = 0$, $\beta\'\beta_\perp = 0$', r'$\alpha_\perp$, $\beta_\perp$ ($n\times(n - r)$): complementele ortogonale, $\alpha\'\alpha_\perp = 0$, $\beta\'\beta_\perp = 0$')])), '0.30', '0.68'), 'footnotesize')

D.frame(T('The Granger representation theorem (2/3)', 'Teorema de reprezentare Granger (2/3)'), items(
    T(r'Under these conditions $y_t$ is I(1), $\beta\'y_t$ is I(0), and \[ y_t = C\sum_{i=1}^{t}(\varepsilon_i + \Phi D_i) + C^*(L)(\varepsilon_t + \Phi D_t) + A_0 \]',
      r'În aceste condiții $y_t$ este I(1), $\beta\'y_t$ este I(0), iar \[ y_t = C\sum_{i=1}^{t}(\varepsilon_i + \Phi D_i) + C^*(L)(\varepsilon_t + \Phi D_t) + A_0 \]'),
    (T('Notation', 'Notațiile'),
     [T(r'$C = \beta_\perp(\alpha_\perp\'\Gamma\beta_\perp)^{-1}\alpha_\perp\'$: the long-run impact matrix, of rank $n - r$ (derivation: Appendix)  % applink: long-run impact matrix', r'$C = \beta_\perp(\alpha_\perp\'\Gamma\beta_\perp)^{-1}\alpha_\perp\'$: matricea impactului pe termen lung, de rang $n - r$ (derivarea: Anexa)  % applink: matricei impactului'),
      T(r'$C^*(L) = \sum_{j\ge 0}C_j^*L^j$: a polynomial in the lag operator $L$ ($Ly_t = y_{t-1}$) with summable coefficients, the stationary part', r'$C^*(L) = \sum_{j\ge 0}C_j^*L^j$: un polinom în operatorul lag $L$ ($Ly_t = y_{t-1}$) cu coeficienți sumabili, partea staționară'),
      T(r'$A_0$: a constant that depends on the initial values, with $\beta\'A_0 = 0$', r'$A_0$: o constantă care depinde de valorile inițiale, cu $\beta\'A_0 = 0$')]),
    T(r'First term: random walks plus deterministic trends; second term: stationary deviations from them',
      r'Primul termen: mersuri aleatoare plus trenduri deterministe; al doilea termen: abateri staționare de la ele')), 'small')

D.frame(T('The Granger representation theorem (3/3)', 'Teorema de reprezentare Granger (3/3)'), items(
    (T('Interpretation', 'Interpretarea'),
     [T(r'$\beta\'C = 0$: the relations do not contain the stochastic trends', r'$\beta\'C = 0$: relațiile nu conțin trendurile stochastice'),
      T(r'$C\alpha = 0$: an equilibrium error has no permanent effect', r'$C\alpha = 0$: o eroare de echilibru nu are efect permanent'),
      T(r'common trends: the $n - r$ random walks $\alpha_\perp\'\sum_i\varepsilon_i$', r'trendurile comune: cele $n - r$ mersuri aleatoare $\alpha_\perp\'\sum_i\varepsilon_i$')]),
    (T(r'If $\alpha_\perp\'\Gamma\beta_\perp$ is singular, the theorem fails', r'Dacă $\alpha_\perp\'\Gamma\beta_\perp$ este singulară, teorema nu se mai aplică'),
     [T(r'$C$ does not exist and some trends are I(2) (see the I(2) section)', r'$C$ nu există, iar unele trenduri sînt I(2) (vezi secțiunea despre I(2))')])), 'small')

D.recap(('The cointegrated VAR', 'VAR-ul cointegrat'), [
    T(r'Concentrate out the short run, then maximise over $\beta$: a generalised eigenvalue problem', r'Eliminăm dinamica pe termen scurt, apoi maximizăm după $\beta$: o problemă generalizată de valori proprii'),
    T('The eigenvalues are squared canonical correlations; the trace and max-eigenvalue statistics are likelihood ratios', 'Valorile proprii sînt corelații canonice la pătrat; statisticile trace și max-eigenvalue sînt rapoarte de verosimilitate'),
    T(r'Their limits are Brownian functionals that depend on $n - r$ and on the deterministic terms only', r'Limitele lor sînt funcționale browniene care depind doar de $n - r$ și de termenii determiniști'),
    T(r'Granger representation: $C = \beta_\perp(\alpha_\perp\'\Gamma\beta_\perp)^{-1}\alpha_\perp\'$ links $\alpha, \beta$ to the common trends', r'Reprezentarea Granger: $C = \beta_\perp(\alpha_\perp\'\Gamma\beta_\perp)^{-1}\alpha_\perp\'$ leagă $\alpha, \beta$ de trendurile comune')])

# =============================================================================
# 2. TERMENI DETERMINIȘTI
# =============================================================================
D.section('Deterministic terms', 'Termenii determiniști')

D.frame(T('Five ways to place a constant and a trend', 'Cinci moduri de a plasa constanta și trendul'), items(
    (T(r'$\mu_t = \mu_0 + \mu_1t$ with $\mu_j = \alpha\rho_j + \alpha_\perp\gamma_j$: the $\alpha$ part sits in the relations, the $\alpha_\perp$ part drives the levels \refJohD',
       r'$\mu_t = \mu_0 + \mu_1t$ cu $\mu_j = \alpha\rho_j + \alpha_\perp\gamma_j$: partea $\alpha$ intră în relații, partea $\alpha_\perp$ determină nivelurile \refJohD'),
     [T(r'$\mu_t$: constant $\mu_0$ plus trend $\mu_1t$ in the VECM; $\rho_j$ ($r\times 1$), $\gamma_j$ ($(n - r)\times 1$): their coordinates in the two directions', r'$\mu_t$: constanta $\mu_0$ plus trendul $\mu_1t$ din VECM; $\rho_j$ ($r\times 1$), $\gamma_j$ ($(n - r)\times 1$): coordonatele lor pe cele două direcții')]),
    table('clll', T(r'\textbf{Case}', r'\textbf{Cazul}') + ' & ' + T(r'\textbf{Restriction}', r'\textbf{Restricția}') + ' & ' + T(r'\textbf{Levels $y_t$}', r'\textbf{Nivelurile $y_t$}') + ' & ' + T(r'\textbf{Relations $\beta\'y_t$}', r'\textbf{Relațiile $\beta\'y_t$}'),
          [r'1 ($H_2$) & $\mu_0 = \mu_1 = 0$ & ' + T('no drift', 'fără drift') + ' & ' + T('zero mean', 'medie zero'),
           r'2 ($H_1^*$) & $\mu_0 = \alpha\rho_0$, $\mu_1 = 0$ & ' + T('no drift', 'fără drift') + ' & ' + T('constant', 'constantă'),
           r'3 ($H_1$) & $\mu_1 = 0$ & ' + T('linear trend', 'trend liniar') + ' & ' + T('constant', 'constantă'),
           r'4 ($H^*$) & $\mu_1 = \alpha\rho_1$ & ' + T('linear trend', 'trend liniar') + ' & ' + T('linear trend', 'trend liniar'),
           r'5 ($H$) & ' + T('none', 'niciuna') + ' & ' + T('quadratic trend', 'trend pătratic') + ' & ' + T('linear trend', 'trend liniar')],
          size='scriptsize'),
    T(r'``Restricted\'\' terms enter $Z_{1t}$ (the regressors multiplied by $\Pi$) with $y_{t-1}$, as part of $\beta$; ``unrestricted\'\' terms enter $Z_{2t}$ and are concentrated out',
      r'Termenii „restricționați” intră în $Z_{1t}$ (regresorii înmulțiți cu $\Pi$) alături de $y_{t-1}$, ca parte a lui $\beta$; cei „nerestricționați” intră în $Z_{2t}$ și sînt eliminați prin concentrare'),
    T('Interest rates: case 2; trending macro aggregates: case 3 or 4; case 5 is rarely plausible', 'Dobînzi: cazul 2; agregate macro cu trend: cazul 3 sau 4; cazul 5 este rar plauzibil')), 'small')

chart(T('The case changes the null distribution', 'Cazul schimbă distribuția sub ipoteza nulă'), 'ats_ch4_trace_dists', 'ATS_ch4_johansen_asymptotics', [
    T(r'Trace statistic under $H(r)$ with $n - r = 2$, simulated from random walks (@{sim.reps} replications, $T = 400$; drift in cases 3 and 5)', r'Statistica trace sub $H(r)$ cu $n - r = 2$, simulată din mersuri aleatoare (@{sim.reps} de replicări, $T = 400$; drift în cazurile 3 și 5)'),
    T(r'95\% quantiles: @{cv.1.2} (case 1), @{cv.2.2} (2), @{cv.3.2} (3), @{cv.4.2} (4), @{cv.5.2} (5)', r'Cuantilele de 95\%: @{cv.1.2} (cazul 1), @{cv.2.2} (2), @{cv.3.2} (3), @{cv.4.2} (4), @{cv.5.2} (5)')],
    h='0.5\\textheight')

interp(('the five distributions', 'celor cinci distribuții'), [
    T('Each restricted deterministic term adds a regressor to the reduced-rank problem and shifts the distribution to the right', 'Fiecare termen determinist restricționat adaugă un regresor problemei de rang redus și deplasează distribuția spre dreapta'),
    T(r'A trend in the levels (cases 3 and 5) makes one direction of the common trend deterministic: for $n - r = 1$ the limit is $\chi^2(1)$, 95\% quantile @{cv.3.1}', r'Un trend în niveluri (cazurile 3 și 5) face deterministă o direcție a trendului comun: pentru $n - r = 1$ limita este $\chi^2(1)$, cuantila de 95\% @{cv.3.1}'),
    T(r'Using case-3 critical values in a case-2 model over-rejects: the 95\% quantile for $n - r = 1$ is @{cv.2.1} in case 2 and @{cv.3.1} in case 3', r'Folosirea valorilor critice ale cazului 3 într-un model al cazului 2 respinge prea des: cuantila de 95\% pentru $n - r = 1$ este @{cv.2.1} în cazul 2 și @{cv.3.1} în cazul 3'),
    T(r'Our simulated quantiles differ from the published tables \refMHM\ by a few tenths at most; the Quantlet gives all cases and $n - r = 1, \dots, 4$', r'Cuantilele simulate diferă de tabelele publicate \refMHM\ cu cel mult cîteva zecimi; Quantlet-ul dă toate cazurile și $n - r = 1, \dots, 4$')])

D.frame(T('Simulated 95\\% quantiles of the trace statistic', 'Cuantilele simulate de 95\\% ale statisticii trace'), table(
    'lccccc', r'$n - r$ & ' + ' & '.join(T(f'case {c}', f'cazul {c}') for c in range(1, 6)),
    [f'{m} & ' + ' & '.join(f'@{{cv.{c}.{m}}}' for c in range(1, 6)) for m in range(1, 5)], size='footnotesize') + items(
    T(r'Simulated with @{sim.reps} replications of a VAR(1) test regression on $T = 400$ observations; the response-surface critical values of \refMHM\ differ by at most a few tenths',
      r'Simulate cu @{sim.reps} de replicări ale unei regresii de test VAR(1) pe $T = 400$ de observații; valorile critice din suprafețele de răspuns \refMHM\ diferă cu cel mult cîteva zecimi'),
    T(r'Choosing the case: plot the data first; if unsure between 2 and 3 (or 3 and 4), test the joint hypothesis on rank and case in the order of the Pantula principle \refPan, \refJohC',
      r'Alegerea cazului: întîi graficul datelor; dacă ezitați între 2 și 3 (sau între 3 și 4), testați ipoteza comună asupra rangului și a cazului în ordinea principiului Pantula \refPan, \refJohC'),
    T(r'Breaks in the deterministic terms shift the distribution again: use the critical values of \refJMN\ for broken trends',
      r'Rupturile în termenii determiniști deplasează din nou distribuția: folosiți valorile critice din \refJMN\ pentru trenduri cu rupturi')), 'small')

D.recap(('Deterministic terms', 'termenii determiniști'), [
    T(r'Split each deterministic term into an $\alpha$ part (in the relations) and an $\alpha_\perp$ part (in the levels)', r'Descompunem fiecare termen determinist într-o parte $\alpha$ (în relații) și una $\alpha_\perp$ (în niveluri)'),
    T('The five cases have five different null distributions; mixing them up changes the rank', 'Cele cinci cazuri au cinci distribuții nule diferite; confundarea lor schimbă rangul'),
    T('Plot the data, choose the case on economic grounds and use the Pantula principle when in doubt', 'Faceți graficul datelor, alegeți cazul pe criterii economice și folosiți principiul Pantula cînd aveți dubii')])

# =============================================================================
# 3. EȘANTIOANE MICI
# =============================================================================
D.section('Small samples: corrections and the bootstrap', 'Eșantioane mici: corecții și bootstrap')

D.frame(T('Over-rejection of the asymptotic test (1/2)', 'Respingerile excesive ale testului asimptotic (1/2)'), items(
    (T(r'The VECM spends many parameters on the short run', r'VECM-ul consumă mulți parametri pentru termenul scurt'),
     [T(r'$n^2(p - 1)$ elements of $\Gamma_1, \dots, \Gamma_{p-1}$, plus the deterministic terms', r'$n^2(p - 1)$ elemente ale matricelor $\Gamma_1, \dots, \Gamma_{p-1}$, plus termenii determiniști'),
      T(r'with $T = 100$, $n = 3$ and $p = 4$: 27 short-run parameters, a large share of the information', r'cu $T = 100$, $n = 3$ și $p = 4$: 27 de parametri de termen scurt, o parte mare din informație')]),
    (T('The distortion grows with persistence', 'Distorsiunea crește cu persistența'),
     [T(r'persistent short-run dynamics: roots of the stationary part close to the unit circle', r'dinamica pe termen scurt persistentă: rădăcini ale părții staționare apropiate de cercul unitate'),
      T('the asymptotic test then finds too many cointegrating relations', 'testul asimptotic găsește atunci prea multe relații de cointegrare')]),
    (T(r'Conditional heteroskedasticity \refCRTa', r'Heteroscedasticitatea condiționată \refCRTa'),
     [T('leaves the limit distribution unchanged', 'nu schimbă distribuția limită'),
      T('but worsens the finite-sample size: use the wild bootstrap', 'dar înrăutățește nivelul efectiv al testului în eșantioane finite: folosiți bootstrap-ul wild')])), 'small')

D.frame(T('Over-rejection of the asymptotic test (2/2)', 'Respingerile excesive ale testului asimptotic (2/2)'), items(
    (T(r'\textbf{Reinsel--Ahn} \refRA', r'\textbf{Reinsel--Ahn} \refRA'),
     [T(r'multiply the statistic by $(T - np)/T$: a degrees-of-freedom correction', r'înmulțim statistica cu $(T - np)/T$: o corecție pentru gradele de libertate'),
      T('simple, often too conservative', 'simplă, adesea prea conservatoare')]),
    (T(r'\textbf{Bartlett correction} \refJohG', r'\textbf{Corecția Bartlett} \refJohG'),
     [T(r'$\E LR_{tr} \approx f\,(1 + a(\theta)/T)$; the corrected statistic is $LR_{tr}/(1 + a(\theta)/T)$', r'$\E LR_{tr} \approx f\,(1 + a(\theta)/T)$; statistica corectată este $LR_{tr}/(1 + a(\theta)/T)$'),
      T(r'$f$: the mean of the limit distribution; $\theta$: the VECM parameters', r'$f$: media distribuției limită; $\theta$: parametrii VECM-ului'),
      T(r'$a(\theta)$: an analytic function of $\theta$, evaluated at the estimates', r'$a(\theta)$: o funcție analitică de $\theta$, evaluată în estimații')]),
    (T(r'\textbf{Bootstrap} \refSwe, \refCRT', r'\textbf{Bootstrap} \refSwe, \refCRT'),
     [T(r'simulate the null distribution from the model estimated under $H(r)$', r'simulăm distribuția nulă din modelul estimat sub $H(r)$')])), 'small')

D.frame(T('The bootstrap rank test, step by step', 'Testul de rang bootstrap, pas cu pas'), items(
    T(r'1. Estimate the VECM under $H(r)$: $\hat\alpha^{(r)}, \hat\beta^{(r)}, \hat\Gamma_i^{(r)}, \hat\Phi^{(r)}$ and residuals $\hat\varepsilon_t^{(r)}$',
      r'1. Estimăm VECM sub $H(r)$: $\hat\alpha^{(r)}, \hat\beta^{(r)}, \hat\Gamma_i^{(r)}, \hat\Phi^{(r)}$ și reziduurile $\hat\varepsilon_t^{(r)}$'),
    T(r'2. Generate $\Delta y_t^* = \hat\alpha^{(r)}\hat\beta^{(r)\prime}y_{t-1}^* + \sum_i\hat\Gamma_i^{(r)}\Delta y_{t-i}^* + \hat\Phi^{(r)}D_t + \varepsilon_t^*$ from the observed initial values',
      r'2. Generăm $\Delta y_t^* = \hat\alpha^{(r)}\hat\beta^{(r)\prime}y_{t-1}^* + \sum_i\hat\Gamma_i^{(r)}\Delta y_{t-i}^* + \hat\Phi^{(r)}D_t + \varepsilon_t^*$ pornind de la valorile inițiale observate'),
    (T(r'3. Innovations: $\varepsilon_t^* = \hat\varepsilon_t^{(r)}w_t$, $w_t \sim$ i.i.d. $N(0, 1)$ (wild) or resampled residuals (i.i.d. bootstrap)',
       r'3. Inovațiile: $\varepsilon_t^* = \hat\varepsilon_t^{(r)}w_t$, $w_t \sim$ i.i.d. $N(0, 1)$ (wild) sau reziduuri reeșantionate (bootstrap i.i.d.)'),
     [T(r'the star marks bootstrap quantities; $w_t$: a random sign-and-scale weight; the wild version keeps the volatility pattern of each date', r'steluța marchează mărimile bootstrap; $w_t$: o pondere aleatoare de semn și scală; varianta wild păstrează tiparul de volatilitate al fiecărei date')]),
    T(r'4. Compute $LR_{tr}^*(r)$ on each sample; p-value = share of $LR_{tr}^* \ge LR_{tr}(r)$; test $r = 0, 1, \dots$ and stop at the first non-rejection',
      r'4. Calculăm $LR_{tr}^*(r)$ pe fiecare eșantion; p-value-ul = proporția eșantioanelor cu $LR_{tr}^* \ge LR_{tr}(r)$; testăm $r = 0, 1, \dots$ și ne oprim la prima nerespingere'),
    T(r'Estimating under $H(r)$ (not under $H(n)$) is essential: the bootstrap data must have exactly $n - r$ unit roots \refCRT',
      r'Estimarea sub $H(r)$ (nu sub $H(n)$) este esențială: datele bootstrap trebuie să aibă exact $n - r$ rădăcini unitare \refCRT')), 'small')

chart(T('Size of the rank test in small samples (simulation)', 'Nivelul efectiv al testului de rang în eșantioane mici (simulare)'), 'ats_ch4_size_mc', 'ATS_ch4_johansen_asymptotics', [
    T(r'Three-variable VECM, true rank 1, $\Gamma_1 = 0.8I$, case 2, VAR(2); test of $H(1)$ at 5\%; @{mc.reps} replications, @{mc.B} bootstrap samples each', r'VECM cu trei variabile, rangul adevărat 1, $\Gamma_1 = 0.8I$, cazul 2, VAR(2); testul lui $H(1)$ la 5\%; @{mc.reps} de replicări, cîte @{mc.B} de eșantioane bootstrap'),
    T(r'$T = 50$, i.i.d. errors: asymptotic @{mc.iid.50.as}\%, Reinsel--Ahn @{mc.iid.50.ra}\%, wild bootstrap @{mc.iid.50.bo}\%', r'$T = 50$, erori i.i.d.: asimptotic @{mc.iid.50.as}\%, Reinsel--Ahn @{mc.iid.50.ra}\%, bootstrap wild @{mc.iid.50.bo}\%')],
    h='0.5\\textheight')

interp(('the size simulation', 'simulării nivelului efectiv'), [
    T(r'With persistent short-run dynamics the asymptotic test finds a spurious second relation in @{mc.iid.50.as}\% of samples of 50 and @{mc.iid.100.as}\% of samples of 100', r'Cu dinamică persistentă pe termen scurt, testul asimptotic găsește o a doua relație falsă în @{mc.iid.50.as}\% din eșantioanele de 50 și în @{mc.iid.100.as}\% din cele de 100'),
    T(r'Reinsel--Ahn halves the distortion; the wild bootstrap is close to 5\% at every $T$, also under GARCH errors (@{mc.garch.50.bo}\% at $T = 50$, asymptotic @{mc.garch.50.as}\%)', r'Reinsel--Ahn înjumătățește distorsiunea; bootstrap-ul wild este aproape de 5\% pentru orice $T$, și cu erori GARCH (@{mc.garch.50.bo}\% la $T = 50$, asimptotic @{mc.garch.50.as}\%)'),
    T(r'At $T = 200$ all three are acceptable: the problem is the ratio of parameters to observations, not the method', r'La $T = 200$ toate trei sînt acceptabile: problema este raportul dintre numărul de parametri și numărul de observații, nu metoda'),
    T('Practice: report asymptotic and bootstrap $p$-values side by side, and the rank for neighbouring lag lengths', 'În practică: raportați p-value-urile asimptotice și bootstrap una lîngă alta și rangul pentru numere de laguri apropiate')])

D.recap(('Small samples', 'eșantioane mici'), [
    T('The asymptotic trace test over-rejects when parameters are many and the short run is persistent', 'Testul trace asimptotic respinge prea des cînd parametrii sînt mulți și dinamica pe termen scurt este persistentă'),
    T('Reinsel--Ahn and the Bartlett correction rescale the statistic; the bootstrap rebuilds its distribution', 'Reinsel--Ahn și corecția Bartlett rescalează statistica; bootstrap-ul îi reconstruiește distribuția'),
    T(r'Bootstrap from the model estimated under $H(r)$; use wild weights when volatility changes over time', r'Bootstrap din modelul estimat sub $H(r)$; ponderi wild cînd volatilitatea se schimbă în timp')])

# =============================================================================
# 4. IDENTIFICARE ȘI TESTE
# =============================================================================
D.section(r'Identification and tests on $\beta$ and $\alpha$', r'Identificarea și testele asupra lui $\beta$ și $\alpha$')

D.frame(T('Normalisation is not identification (1/2)', 'Normalizarea nu înseamnă identificare (1/2)'), items(
    (T(r'The eigenvectors give one basis of the cointegration space $\mathrm{sp}(\beta)$; any $\beta\xi$ spans the same space and fits equally well',
       r'Vectorii proprii dau o bază a spațiului de cointegrare $\mathrm{sp}(\beta)$; orice $\beta\xi$ generează același spațiu și descrie datele la fel de bine'),
     [T(r'$\mathrm{sp}(\beta)$: the space spanned by the columns of $\beta$; $\xi$: an invertible $r\times r$ matrix (a rotation)', r'$\mathrm{sp}(\beta)$: spațiul generat de coloanele lui $\beta$; $\xi$: o matrice inversabilă de $r\times r$ (o rotație)')]),
    (T(r'Dividing each vector by one coefficient fixes the scale ($r$ restrictions), but not the rotation',
       r'Împărțirea fiecărui vector la un coeficient fixează scala ($r$ restricții), dar nu și rotația'),
     [T(r'$r(r - 1)$ further restrictions are needed, $r - 1$ per vector', r'mai sînt necesare $r(r - 1)$ restricții, cîte $r - 1$ pentru fiecare vector')]),
    T('Identification rests on economic theory: each restriction is a statement such as ``the lending rate does not depend on the deposit rate in the long run\'\'',
      'Identificarea se sprijină pe teoria economică: fiecare restricție este o afirmație de tipul „pe termen lung, dobînda la credite nu depinde de dobînda la depozite”')), 'small')

D.frame(T('Normalisation is not identification (2/2)', 'Normalizarea nu înseamnă identificare (2/2)'), items(
    (T(r'Linear restrictions vector by vector: $\beta = (H_1\varphi_1, \dots, H_r\varphi_r)$',
       r'Restricții liniare vector cu vector: $\beta = (H_1\varphi_1, \dots, H_r\varphi_r)$'),
     [T(r'$n_1$: the length of each vector ($n$ plus the restricted deterministic terms)', r'$n_1$: lungimea fiecărui vector ($n$ plus termenii determiniști restricționați)'),
      T(r'$H_i$ ($n_1\times s_i$, known): the design matrix of vector $i$; $\varphi_i$ ($s_i\times 1$): its $s_i$ free coefficients', r'$H_i$ ($n_1\times s_i$, cunoscută): matricea de restricții a vectorului $i$; $\varphi_i$ ($s_i\times 1$): cei $s_i$ coeficienți liberi ai săi'),
      T(r'$R_i = H_{i\perp}$: the restrictions written as $R_i\'\beta_i = 0$', r'$R_i = H_{i\perp}$: restricțiile scrise sub forma $R_i\'\beta_i = 0$')]),
    (T(r'Rank condition \refJohE: for every $i$ and every set of $k$ other vectors $i_1, \dots, i_k$', r'Condiția de rang \refJohE: pentru orice $i$ și orice mulțime de $k$ alți vectori $i_1, \dots, i_k$'),
     [T(r'$\mathrm{rank}(R_i\'(H_{i_1}, \dots, H_{i_k})) \ge k$, $k = 1, \dots, r - 1$', r'$\mathrm{rang}(R_i\'(H_{i_1}, \dots, H_{i_k})) \ge k$, $k = 1, \dots, r - 1$'),
      T(r'meaning: no combination of other vectors satisfies the restrictions of vector $i$', r'sensul: nicio combinație a altor vectori nu satisface restricțiile vectorului $i$'),
      T(r'the cointegration analogue of the rank condition in simultaneous equations; the order condition alone is not enough',
        r'analogul condiției de rang din sistemele de ecuații simultane; condiția de ordin singură nu este suficientă')])), 'small')

D.frame(T(r'Testing restrictions on $\beta$ (1/2)', r'Testarea restricțiilor asupra lui $\beta$ (1/2)'), items(
    (T(r'\textbf{The same restriction on all vectors}, $\beta = H\varphi$: solve $|\lambda H\'S_{11}H - H\'S_{10}S_{00}^{-1}S_{01}H| = 0$',
       r'\textbf{Aceeași restricție pentru toți vectorii}, $\beta = H\varphi$: rezolvăm $|\lambda H\'S_{11}H - H\'S_{10}S_{00}^{-1}S_{01}H| = 0$'),
     [T(r'$H$ ($n_1\times s$, known): the restriction; $\varphi$ ($s\times r$): the free coefficients; e.g.\ excluding one variable from all relations', r'$H$ ($n_1\times s$, cunoscută): restricția; $\varphi$ ($s\times r$): coeficienții liberi; de exemplu, excluderea unei variabile din toate relațiile'),
      T(r'$\tilde\lambda_i$: the eigenvalues of the restricted problem; $\hat\lambda_i$: the unrestricted ones', r'$\tilde\lambda_i$: valorile proprii ale problemei cu restricții; $\hat\lambda_i$: cele fără restricții')]),
    (T(r'Test statistic: $LR = T\sum_{i=1}^r\ln\{(1 - \tilde\lambda_i)/(1 - \hat\lambda_i)\} \to \chi^2(r(n_1 - s))$',
       r'Statistica testului: $LR = T\sum_{i=1}^r\ln\{(1 - \tilde\lambda_i)/(1 - \hat\lambda_i)\} \to \chi^2(r(n_1 - s))$'),
     [T(r'$LR \ge 0$; it is large when the restriction lowers the canonical correlations, i.e.\ when the data reject it', r'$LR \ge 0$; este mare cînd restricția reduce corelațiile canonice, adică atunci cînd datele o resping'),
      T(r'degrees of freedom $r(n_1 - s)$: $n_1 - s$ restrictions on each of the $r$ vectors', r'gradele de libertate $r(n_1 - s)$: cîte $n_1 - s$ restricții pentru fiecare dintre cei $r$ vectori')]),
    T(r'Given the rank, $\hat\beta$ is super-consistent and mixed Gaussian: LR tests on $\beta$ are $\chi^2$, unlike the rank test \refJohB',
      r'Pentru un rang dat, $\hat\beta$ este superconsistent și mixt gaussian: testele LR asupra lui $\beta$ sînt $\chi^2$, spre deosebire de testul de rang \refJohB')), 'small')

D.frame(T(r'Testing restrictions on $\beta$ (2/2)', r'Testarea restricțiilor asupra lui $\beta$ (2/2)'), items(
    (T(r'\textbf{Different restrictions per vector}, $\beta = (H_1\varphi_1, \dots, H_r\varphi_r)$: no closed form',
       r'\textbf{Restricții diferite pe vectori}, $\beta = (H_1\varphi_1, \dots, H_r\varphi_r)$: fără formă închisă'),
     [T(r'maximise the concentrated log-likelihood $-\tfrac{T}{2}\ln|\hat\Omega(\beta)|$ by the switching algorithm (one vector at a time) or numerically', r'maximizăm logaritmul verosimilității concentrate $-\tfrac{T}{2}\ln|\hat\Omega(\beta)|$ prin algoritmul de comutare (cîte un vector) sau numeric'),
      T(r'over-identifying restrictions: $LR \to \chi^2(\sum_i(n_1 - r + 1 - s_i))$; each vector has $n_1 - r + 1 - s_i$ restrictions beyond the $r - 1$ needed to identify it', r'restricții de supraidentificare: $LR \to \chi^2(\sum_i(n_1 - r + 1 - s_i))$; fiecare vector are $n_1 - r + 1 - s_i$ restricții peste cele $r - 1$ necesare identificării')]),
    (T(r'\textbf{Fully known} $\beta = \beta_0$ (e.g.\ the great ratios): \[ LR = T\Big\{\ln|\hat\Omega(\beta_0)| - \ln|S_{00}| - \sum_{i\le r}\ln(1 - \hat\lambda_i)\Big\} \to \chi^2(r(n_1 - r)) \]',
       r'$\beta = \beta_0$ \textbf{complet cunoscut} (de exemplu, rapoartele de echilibru, great ratios): \[ LR = T\Big\{\ln|\hat\Omega(\beta_0)| - \ln|S_{00}| - \sum_{i\le r}\ln(1 - \hat\lambda_i)\Big\} \to \chi^2(r(n_1 - r)) \]'),
     [T(r'compares the fit with $\beta_0$ imposed ($\hat\Omega(\beta_0)$) to the unrestricted fit; $\beta_0$: the hypothesised matrix', r'compară potrivirea cu $\beta_0$ impus ($\hat\Omega(\beta_0)$) cu potrivirea fără restricții; $\beta_0$: matricea din ipoteză')])), 'small')

D.frame(T(r'Restrictions on $\alpha$ and weak exogeneity', r'Restricții asupra lui $\alpha$ și exogenitatea slabă'), items(
    (T(r'$\alpha = A\psi$: only $m$ combinations of the equations adjust to the relations',
       r'$\alpha = A\psi$: doar $m$ combinații ale ecuațiilor se ajustează la relații'),
     [T(r'$A$ ($n\times m$, known): the restriction; $\psi$ ($m\times r$): the free adjustment coefficients; $A_\perp$: its orthogonal complement', r'$A$ ($n\times m$, cunoscută): restricția; $\psi$ ($m\times r$): coeficienții de ajustare liberi; $A_\perp$: complementul ei ortogonal'),
      T(r'condition the system on $A_\perp\'R_{0t}$ and solve the eigenvalue problem of the remaining $m$ equations (eigenvalues $\tilde\lambda_i$)', r'condiționăm sistemul pe $A_\perp\'R_{0t}$ și rezolvăm problema de valori proprii a celor $m$ ecuații rămase (valorile proprii $\tilde\lambda_i$)'),
      T(r'$LR = T\sum_{i\le r}\ln\{(1 - \tilde\lambda_i)/(1 - \hat\lambda_i)\} \to \chi^2(r(n - m))$', r'$LR = T\sum_{i\le r}\ln\{(1 - \tilde\lambda_i)/(1 - \hat\lambda_i)\} \to \chi^2(r(n - m))$')]),
    (T(r'\textbf{Weak exogeneity} of $x_t$ for $\beta$: the row of $\alpha$ for $x_t$ is zero (a zero row of $\alpha$, $r$ restrictions)',
       r'\textbf{Exogenitatea slabă} a lui $x_t$ pentru $\beta$: rîndul lui $\alpha$ corespunzător lui $x_t$ este zero ($r$ restricții)'),
     [T(r'$x_t$ does not adjust to past disequilibria; it is a common trend (a column of $\alpha_\perp$)', r'$x_t$ nu se ajustează la dezechilibrele trecute; este un trend comun (o coloană a lui $\alpha_\perp$)'),
      T(r'the conditional model of $\Delta y_t$ given $\Delta x_t$ is then fully efficient for $\beta$: the basis of single-equation ECM and ARDL', r'atunci modelul condiționat al lui $\Delta y_t$ dat $\Delta x_t$ este complet eficient pentru $\beta$: baza ECM și ARDL pe o singură ecuație')]),
    (T('Long-run structural hypotheses are joint restrictions on $\\beta$ and $\\alpha$', 'Ipotezele structurale de termen lung sînt restricții comune asupra lui $\\beta$ și $\\alpha$'),
     [T('PPP: $(1, -1, -1)$ on (price, foreign price, exchange rate); Fisher: $(1, -1)$ on (interest rate, inflation); complete pass-through: $(1, -1)$ on (retail rate, policy or market rate)',
        'PPP: $(1, -1, -1)$ pentru (preț, preț extern, curs de schimb); Fisher: $(1, -1)$ pentru (dobîndă, inflație); transmitere completă: $(1, -1)$ pentru (dobînda bancară, dobînda de politică sau de piață)')])), 'small')

D.recap((r'Identification and tests', 'identificarea și testele'), [
    T(r'Identify $\beta$ with $r - 1$ economically motivated restrictions per vector; check the rank condition', r'Identificați $\beta$ cu cîte $r - 1$ restricții motivate economic pe vector; verificați condiția de rang'),
    T(r'Given the rank, LR tests on $\beta$ and $\alpha$ are $\chi^2$ with known degrees of freedom', r'Pentru un rang dat, testele LR asupra lui $\beta$ și $\alpha$ sînt $\chi^2$ cu grade de libertate cunoscute'),
    T(r'A zero row of $\alpha$ = weak exogeneity = permission to condition on that variable', r'Un rînd zero al lui $\alpha$ = exogenitate slabă = permisiunea de a condiționa pe acea variabilă')])

# =============================================================================
# 5. APLICAȚIE: TRANSMITEREA DOBÎNZILOR
# =============================================================================
D.section('Application: interest-rate pass-through in Romania', 'Aplicație: transmiterea dobînzilor în România')

D.frame(T('How fast and how fully do banks follow ROBOR?', 'Cît de repede și cît de complet urmează băncile ROBOR?'), two(
    ph('bnr', T('The BNR palace, Bucharest', 'Palatul BNR, București'), h='0.34\\textheight'),
    items(T(r'Monetary policy reaches households and firms only through bank rates; ROBOR 3M is the reference for most variable-rate loans in lei',
            r'Politica monetară ajunge la gospodării și firme doar prin dobînzile bancare; ROBOR 3M este referința pentru majoritatea creditelor în lei cu dobîndă variabilă'),
          T(r'Euro area: long-run pass-through to lending rates often complete, to deposit rates incomplete \refdB; CEE: faster and fuller pass-through after the early transition \refECR',
            r'Zona euro: transmiterea pe termen lung către dobînzile la credite este adesea completă, către cele la depozite incompletă \refdB; ECE: transmitere mai rapidă și mai completă după prima parte a tranziției \refECR'),
          T(r'Hypotheses: $H_\beta$: lending and deposit rates move one for one with ROBOR in the long run; $H_\alpha$: ROBOR does not adjust to bank rates',
            r'Ipoteze: $H_\beta$: pe termen lung, dobînzile la credite și la depozite se mișcă unu la unu cu ROBOR; $H_\alpha$: ROBOR nu se ajustează la dobînzile bancare'),
          T(r'Data: @{pt.first} -- @{pt.last}, $T = @{pt.T}$ months (inflation targeting)', r'Date: @{pt.first} -- @{pt.last}, $T = @{pt.T}$ de luni (perioada țintirii inflației)')), '0.36', '0.62'), 'footnotesize')

chart(T('Lending rate, deposit rate and ROBOR 3M', 'Dobînda la credite, dobînda la depozite și ROBOR 3M'), 'ats_ch4_rates', 'ATS_ch4_passthrough_vecm', [
    T(r'Monthly, \% per year; lending and deposit rates in lei (IMF IFS, reported by the BNR); ROBOR 3M (Eurostat)', r'Lunar, \% pe an; dobînzile la credite și la depozite în lei (FMI IFS, raportate de BNR); ROBOR 3M (Eurostat)'),
    T(r'ROBOR ranges from @{pt.mmin}\% to @{pt.mmax}\%; the lending--ROBOR spread falls from @{pt.s0} pp to @{pt.s1} pp', r'ROBOR variază între @{pt.mmin}\% și @{pt.mmax}\%; diferența dintre dobînda la credite și ROBOR scade de la @{pt.s0} pp la @{pt.s1} pp')],
    h='0.5\\textheight')

interp(('the three rates', 'celor trei dobînzi'), [
    T('All three rates wander far from any mean over twenty years: treat them as I(1) within the sample, even if interest rates are bounded in theory', 'Toate trei se îndepărtează mult de orice medie în douăzeci de ani: le tratăm ca I(1) în eșantion, chiar dacă dobînzile sînt mărginite teoretic'),
    T('They move together after 2008, in 2014--2015 and in 2022: the visual case for cointegration', 'Se mișcă împreună după 2008, în 2014--2015 și în 2022: argumentul vizual pentru cointegrare'),
    T('The falling spread in 2005--2010 is the end of the transition (competition, falling risk premia), not a policy effect', 'Scăderea diferenței în 2005--2010 este finalul tranziției (concurență, prime de risc în scădere), nu un efect al politicii monetare'),
    T('No trend in levels is plausible for rates: case 2, constant restricted to the relations', 'Un trend în niveluri nu este plauzibil pentru dobînzi: cazul 2, constanta restricționată la relații')])

D.frame(T('Rank of the pass-through system', 'Rangul sistemului de transmitere'), table(
    'lccccccc', r'$H(r)$ & $LR_{tr}$ & RA & cv 5\% & ' + T('wild', 'wild') + r' $p$ & $LR_{tr}$, $p{=}4$ & RA, $p{=}4$ & ' + T('wild', 'wild') + r' $p$, $p{=}4$',
    [r'$r = 0$ & @{pt.tr0} & @{pt.ra0} & @{pt.cv0} & @{pt.bo0} & @{pt.tr40} & @{pt.ra40} & @{pt.bo40}',
     r'$r \le 1$ & @{pt.tr1} & @{pt.ra1} & @{pt.cv1} & @{pt.bo1} & @{pt.tr41} & @{pt.ra41} & @{pt.bo41}',
     r'$r \le 2$ & @{pt.tr2} & @{pt.ra2} & @{pt.cv2} & @{pt.bo2} & @{pt.tr42} & @{pt.ra42} & @{pt.bo42}'], size='scriptsize') + items(
    T(r'Case 2; RA: Reinsel--Ahn; cv: simulated 95\% quantile; wild $p$: 399 wild-bootstrap samples under $H(r)$; lag order by BIC = @{pt.ic.bic}, HQ = @{pt.ic.hq}, AIC = @{pt.ic.aic}',
      r'Cazul 2; RA: Reinsel--Ahn; cv: cuantila simulată de 95\%; $p$ wild: 399 de eșantioane bootstrap wild sub $H(r)$; numărul de laguri după BIC = @{pt.ic.bic}, HQ = @{pt.ic.hq}, AIC = @{pt.ic.aic}'),
    T(r'With @{pt.p.e} all three methods give $r = 2$; with $p = 4$ the asymptotic test gives $r = 1$ and the wild bootstrap rejects nothing',
      r'Cu @{pt.p.e} toate cele trei metode dau $r = 2$; cu $p = 4$ testul asimptotic dă $r = 1$, iar bootstrap-ul wild nu respinge nimic')), 'small')

interp(('the rank tests', 'testelor de rang'), [
    T(r'Two relations are what theory predicts: one for lending rates, one for deposit rates, both anchored to ROBOR', r'Două relații sînt exact ceea ce prezice teoria: una pentru dobînzile la credite, una pentru cele la depozite, ambele ancorate de ROBOR'),
    T(r'The result is fragile: two extra lags and heteroskedasticity-robust inference remove the evidence; the 2008--2009 volatility dominates the sample', r'Rezultatul este fragil: două laguri în plus și o inferență robustă la heteroscedasticitate elimină dovezile; volatilitatea din 2008--2009 domină eșantionul'),
    T('We continue with $r = 2$ because theory and the parsimonious model agree, and we report the sensitivity', 'Continuăm cu $r = 2$ pentru că teoria și modelul parcimonios coincid și raportăm sensibilitatea'),
    T('A rank chosen this way is a modelling decision, not a measurement: state it before testing restrictions', 'Un rang ales astfel este o decizie de modelare, nu o măsurătoare: enunțați-o înainte de a testa restricțiile')])

D.frame(T('Identified relations and the tests', 'Relațiile identificate și testele'), items(
    T(r'Just-identified (one exclusion per vector): $\text{lend}_t = @{pt.thl}\,\text{ROBOR}_t + @{pt.mkl}$, $\text{dep}_t = @{pt.thd}\,\text{ROBOR}_t + @{pt.mkd}$',
      r'Exact identificate (o excludere pe vector): $\text{credit}_t = @{pt.thl}\,\text{ROBOR}_t + @{pt.mkl}$, $\text{depozit}_t = @{pt.thd}\,\text{ROBOR}_t + @{pt.mkd}$'),
    T(r'Adjustment: lending rate $\alpha_{11} = @{pt.a.l0}$ (to its own relation), deposit rate $\alpha_{22} = @{pt.a.d1}$; ROBOR: @{pt.a.m0} and @{pt.a.m1}',
      r'Ajustarea: dobînda la credite $\alpha_{11} = @{pt.a.l0}$ (la propria relație), dobînda la depozite $\alpha_{22} = @{pt.a.d1}$; ROBOR: @{pt.a.m0} și @{pt.a.m1}'),
    table('lccc', T(r'\textbf{Hypothesis}', r'\textbf{Ipoteza}') + r' & $LR$ & ' + T('df', 'gl') + r' & $p$',
          [T('complete pass-through to both rates', 'transmitere completă către ambele dobînzi') + r' & @{pt.LRc} & 2 & @{pt.pc}',
           T('complete pass-through to the lending rate', 'transmitere completă către dobînda la credite') + r' & @{pt.LRl} & 1 & @{pt.pl}',
           T('ROBOR weakly exogenous (zero row of $\\alpha$)', 'ROBOR slab exogen (rînd zero în $\\alpha$)') + r' & @{pt.LRw} & 2 & @{pt.pw}'], size='scriptsize'),
    T(r'With $p = 4$: lending pass-through @{pt.thl4}, $p$-value of complete pass-through to lending @{pt.pl4}, of weak exogeneity @{pt.pw4}',
      r'Cu $p = 4$: transmiterea către credite @{pt.thl4}, p-value-ul pentru transmiterea completă către credite @{pt.pl4}, pentru exogenitatea slabă @{pt.pw4}')), 'small')

chart(T('The two equilibrium errors', 'Cele două erori de echilibru'), 'ats_ch4_pt_ect', 'ATS_ch4_passthrough_vecm', [
    T(r'$\hat\beta_i\'y_t$ for the just-identified relations, demeaned; they should look stationary if the rank and $\beta$ are right', r'$\hat\beta_i\'y_t$ pentru relațiile exact identificate, centrate; ar trebui să arate staționar dacă rangul și $\beta$ sînt corecte')],
    h='0.52\\textheight')

interp(('the pass-through VECM', 'VECM-ului de transmitere'), [
    T(r'Lending rates over-react slightly in the long run (@{pt.thl} per point of ROBOR), deposit rates under-react (@{pt.thd}): the bank margin widens when ROBOR rises', r'Dobînzile la credite reacționează ușor peste unu pe termen lung (@{pt.thl} pentru un punct de ROBOR), cele la depozite sub unu (@{pt.thd}): marja băncilor crește cînd crește ROBOR'),
    T(r'Joint complete pass-through is rejected (@{pt.pc.e}), driven by deposits; for lending rates alone the verdict depends on the lag length', r'Transmiterea completă comună este respinsă (@{pt.pc.e}), din cauza depozitelor; pentru dobînzile la credite verdictul depinde de numărul de laguri'),
    T(r'ROBOR is weakly exogenous (@{pt.pw.e}): money-market rates lead, bank rates follow; this justifies a single-equation ARDL', r'ROBOR este slab exogen (@{pt.pw.e}): dobînzile pieței monetare se mișcă primele, iar dobînzile bancare le urmează; aceasta justifică un ARDL pe o singură ecuație'),
    T('The lending equilibrium error is persistent before 2010: the transition-era spread is not a stable markup, a candidate for a broken constant \\refJMN', 'Eroarea de echilibru pentru credite este persistentă înainte de 2010: diferența din perioada tranziției nu este o marjă stabilă, un candidat pentru o constantă cu ruptură \\refJMN')])

D.recap(('Pass-through in Romania', 'transmiterea în România'), [
    T('Two cointegrating relations with ROBOR as the common trend, but the rank is sensitive to lags and to heteroskedasticity', 'Două relații de cointegrare cu ROBOR ca trend comun, dar rangul este sensibil la numărul de laguri și la heteroscedasticitate'),
    T('Lending pass-through close to (slightly above) one, deposit pass-through below one', 'Transmiterea către credite este apropiată de unu (ușor peste), cea către depozite sub unu'),
    T('Weak exogeneity of ROBOR is not rejected: a conditional single-equation model is legitimate', 'Exogenitatea slabă a lui ROBOR nu este respinsă: un model condiționat pe o singură ecuație este legitim')])

# =============================================================================
# 6. I(2)
# =============================================================================
D.section('I(2) in brief', 'I(2) pe scurt')

D.frame(T('When the I(1) model is not enough', 'Cînd modelul I(1) nu este suficient'), items(
    (T(r'If $\alpha_\perp\'\Gamma\beta_\perp$ has reduced rank $s < n - r$, the Granger representation fails', r'Dacă $\alpha_\perp\'\Gamma\beta_\perp$ are rang redus $s < n - r$, reprezentarea Granger nu se mai aplică'),
     [T(r'some common trends are I(2): $y_t$ contains double sums $\sum_{j\le t}\sum_{i\le j}\varepsilon_i$', r'unele trenduri comune sînt I(2): $y_t$ conține sume duble $\sum_{j\le t}\sum_{i\le j}\varepsilon_i$'),
      T('typical candidates: nominal prices and nominal money when inflation changes; inflation is then I(1)', 'candidați tipici: prețurile și masa monetară nominale cînd inflația variază; inflația este atunci I(1)')]),
    (T(r'The I(2) model \refJohF, \refJus', r'Modelul I(2) \refJohF, \refJus'),
     [T(r'two reduced-rank conditions: $\Pi = \alpha\beta\'$ and $\alpha_\perp\'\Gamma\beta_\perp = \xi\eta\'$', r'două condiții de rang redus: $\Pi = \alpha\beta\'$ și $\alpha_\perp\'\Gamma\beta_\perp = \xi\eta\'$'),
      T(r'$\xi$, $\eta$ ($(n - r)\times s$, full rank): the factors of the second reduced-rank matrix', r'$\xi$, $\eta$ ($(n - r)\times s$, de rang complet): factorii celei de-a doua matrice de rang redus'),
      T(r'polynomial cointegration: $\beta\'y_t + \delta\'\Delta y_t \sim$ I(0); $\delta$ ($n\times r$): the weights of the differences', r'cointegrare polinomială: $\beta\'y_t + \delta\'\Delta y_t \sim$ I(0); $\delta$ ($n\times r$): ponderile diferențelor'),
      T('example: real money plus a multiple of inflation', 'exemplu: masa monetară reală plus un multiplu al inflației')]),
    (T('Practical check', 'Verificarea practică'),
     [T(r'test $\Delta y_t$ for a unit root; a root near one in the stationary part of the I(1) VECM is a warning', r'testați rădăcina unitară pentru $\Delta y_t$; o rădăcină aproape de unu în partea staționară a VECM-ului I(1) este un semnal de alarmă'),
      T('the usual fix: model real (deflated) variables and inflation', 'soluția uzuală: modelarea variabilelor reale (deflatate) și a inflației')])), 'small')

chart(T('Is the Romanian price level I(2)?', 'Este nivelul prețurilor din România I(2)?'), 'ats_ch4_i2', 'ATS_ch4_i2_check', [
    T(r'Left: $100\ln$ HICP; right: monthly inflation, annualised; dashed line: inflation targeting from August 2005', r'Stînga: $100\ln$ IAPC; dreapta: inflația lunară, anualizată; linia punctată: țintirea inflației din august 2005'),
    T(r'ADF $t$ on monthly inflation (12 lags): @{i2.all} for 1997--2026, @{i2.it} since 2005 (5\% critical value $-2.87$); on its change: @{i2.d2}', r'ADF $t$ pentru inflația lunară (12 laguri): @{i2.all} pentru 1997--2026, @{i2.it} din 2005 (valoarea critică 5\%: $-2.87$); pentru modificarea ei: @{i2.d2}')],
    h='0.48\\textheight')

interp(('the I(2) check', 'verificării I(2)'), [
    T('Over 1997--2026, disinflation looks like mean reversion and inflation tests as stationary: the price level is I(1)', 'Pe 1997--2026, dezinflația arată ca revenire la medie, iar inflația apare staționară: nivelul prețurilor este I(1)'),
    T('Since 2005 a unit root in inflation is not rejected: within the inflation-targeting sample the price level behaves like I(2)', 'Din 2005, o rădăcină unitară în inflație nu este respinsă: în eșantionul țintirii inflației, nivelul prețurilor se comportă ca I(2)'),
    T('The answer depends on the sample, as for the rank: this is why systems with nominal levels are usually rewritten in real terms and inflation', 'Răspunsul depinde de eșantion, ca și pentru rang: de aceea sistemele cu niveluri nominale se rescriu de obicei în termeni reali și inflație'),
    T('Our pass-through system uses rates, which are at most I(1): the I(2) issue does not arise there', 'Sistemul nostru de transmitere folosește dobînzi, cel mult I(1): problema I(2) nu apare acolo')])

# =============================================================================
# 7. VECM STRUCTURAL
# =============================================================================
D.section('Structural VECM: common trends', 'VECM structural: trenduri comune')

D.frame(T('Permanent and transitory shocks (1/2)', 'Șocuri permanente și tranzitorii (1/2)'), items(
    T(r'Granger representation: the long-run effect of $\varepsilon_t$ on $y_{t+h}$, $h \to \infty$, is $C\varepsilon_t$, and $\mathrm{rank}\,C = n - r$',
      r'Reprezentarea Granger: efectul pe termen lung al lui $\varepsilon_t$ asupra lui $y_{t+h}$, $h \to \infty$, este $C\varepsilon_t$, iar $\mathrm{rang}\,C = n - r$'),
    (T(r'Structural shocks: $\varepsilon_t = Bu_t$, $\E u_tu_t\' = I$', r'Șocurile structurale: $\varepsilon_t = Bu_t$, $\E u_tu_t\' = I$'),
     [T(r'$u_t$: $n$ uncorrelated shocks with unit variance; $B$ ($n\times n$): their impact effects, $BB\' = \Omega$', r'$u_t$: $n$ șocuri necorelate, de varianță unu; $B$ ($n\times n$): efectele lor la impact, $BB\' = \Omega$'),
      T(r'the long-run impact $CB$ has at most $n - r$ non-zero columns: $k = n - r$ permanent and $r$ transitory shocks', r'impactul pe termen lung $CB$ are cel mult $n - r$ coloane nenule: $k = n - r$ șocuri permanente și $r$ tranzitorii')]),
    (T(r'Counting (Chapter 3 needed $n(n - 1)/2$ restrictions): cointegration gives $rk$ zero long-run restrictions for free', r'Numărătoarea (în Capitolul 3 erau necesare $n(n - 1)/2$ restricții): cointegrarea dă gratuit $rk$ restricții zero pe termen lung'),
     [T(r'still needed: $k(k - 1)/2$ among the permanent shocks and $r(r - 1)/2$ among the transitory shocks \refKL, \refGN',
        r'mai sînt necesare: $k(k - 1)/2$ între șocurile permanente și $r(r - 1)/2$ între cele tranzitorii \refKL, \refGN')])), 'small')

D.frame(T('Permanent and transitory shocks (2/2)', 'Șocuri permanente și tranzitorii (2/2)'), items(
    (T(r'With one common trend ($k = 1$) the permanent shock is identified without further assumptions',
       r'Cu un singur trend comun ($k = 1$), șocul permanent este identificat fără alte ipoteze'),
     [T(r'the shock: $u_t^P = \alpha_\perp\'\varepsilon_t/(\alpha_\perp\'\Omega\alpha_\perp)^{1/2}$, the innovation of the common trend scaled to unit variance', r'șocul: $u_t^P = \alpha_\perp\'\varepsilon_t/(\alpha_\perp\'\Omega\alpha_\perp)^{1/2}$, inovația trendului comun scalată la varianța unu'),
      T(r'its impact: $b^P = \Omega\alpha_\perp(\alpha_\perp\'\Omega\alpha_\perp)^{-1/2}$, the column of $B$ that moves the $n$ variables on impact', r'impactul său: $b^P = \Omega\alpha_\perp(\alpha_\perp\'\Omega\alpha_\perp)^{-1/2}$, coloana lui $B$ care mișcă cele $n$ variabile la impact')]),
    T(r'This generalises Blanchard--Quah (Chapter 3): there the long-run zero was imposed; here it comes from the cointegration rank',
      r'Aceasta generalizează Blanchard--Quah (Capitolul 3): acolo zeroul de termen lung era impus; aici provine din rangul de cointegrare')), 'small')

D.frame(T('Case study: King, Plosser, Stock and Watson (1991) (1/2)', 'Studiu de caz: King, Plosser, Stock și Watson (1991) (1/2)'), items(
    (T(r'\refKPSW', r'\refKPSW'),
     [T('a real business-cycle model with a stochastic productivity trend', 'un model de ciclu real cu trend stochastic al productivității'),
      T('consumption, investment and output share one common trend', 'consumul, investițiile și producția au un singur trend comun'),
      T(r'the great ratios $c - y$ and $i - y$ are stationary ($c$, $i$, $y$: logarithms per capita)', r'rapoartele de echilibru (great ratios) $c - y$ și $i - y$ sînt staționare ($c$, $i$, $y$: logaritmi pe locuitor)')]),
    (T('In VECM terms', 'În termenii VECM'),
     [T(r'$n = 3$, $r = 2$, $\beta = \begin{pmatrix}1 & 0\\ 0 & 1\\ -1 & -1\end{pmatrix}$ imposed for $(c, i, y)$', r'$n = 3$, $r = 2$, $\beta = \begin{pmatrix}1 & 0\\ 0 & 1\\ -1 & -1\end{pmatrix}$ impus pentru $(c, i, y)$'),
      T(r'$k = n - r = 1$: one permanent ``balanced-growth\'\' shock', r'$k = n - r = 1$: un singur șoc permanent de „creștere echilibrată”')]),
    T('Question: how much of the business cycle does the permanent shock explain?', 'Întrebarea: cît din ciclul economic explică șocul permanent?')), 'small')

D.frame(T('Case study: King, Plosser, Stock and Watson (1991) (2/2)', 'Studiu de caz: King, Plosser, Stock și Watson (1991) (2/2)'), items(
    (T(r'Our replication: US quarterly data, 1949Q1--1988Q4 (the paper\'s sample), $T = @{kp.T}$', r'Replicarea noastră: date trimestriale SUA, 1949T1--1988T4 (eșantionul lucrării), $T = @{kp.T}$'),
     [T(r'$c$: nondurables and services; $i$: fixed investment; $y$: GDP', r'$c$: bunuri nedurabile și servicii; $i$: investiții fixe; $y$: PIB'),
      T('all per capita, deflated by the GDP deflator', 'toate pe locuitor, deflatate cu deflatorul PIB')]),
    (T('Rank', 'Rangul'),
     [T(r'VAR($@{kp.p}$) in levels (all criteria), case 3', r'VAR($@{kp.p}$) în niveluri (toate criteriile), cazul 3'),
      T(r'trace: @{kp.tr0}, @{kp.tr1}, @{kp.tr2} against 95\% quantiles @{kp.cv0}, @{kp.cv1}, @{kp.cv2}: $r = 2$', r'trace: @{kp.tr0}, @{kp.tr1}, @{kp.tr2} față de cuantilele de 95\% @{kp.cv0}, @{kp.cv1}, @{kp.cv2}: $r = 2$')]),
    (T(r'Test of $\beta = \beta_0$ (the exact great ratios)', r'Testul lui $\beta = \beta_0$ (rapoartele de echilibru exacte)'),
     [T(r'case 3: rejected, $LR = @{kp.lr}$, $\chi^2(2)$, @{kp.plr.e}', r'cazul 3: respins, $LR = @{kp.lr}$, $\chi^2(2)$, @{kp.plr.e}'),
      T(r'with a restricted trend (case 4): not rejected, $LR = @{kp.lr4}$, @{kp.plr4.e}', r'cu trend restricționat (cazul 4): nerespins, $LR = @{kp.lr4}$, @{kp.plr4.e}')])), 'small')

chart(T('The balanced-growth shock', 'Șocul de creștere echilibrată'), 'ats_ch4_kpsw', 'ATS_ch4_common_trends', [
    T(r'Great ratios imposed (case 3); one-standard-deviation permanent shock; 90\% residual-bootstrap bands (@{kp.B} samples, $\beta$ fixed)', r'Rapoartele de echilibru impuse (cazul 3); șoc permanent de o abatere standard; benzi bootstrap pe reziduuri de 90\% (@{kp.B} de eșantioane, $\beta$ fixat)'),
    T(r'Long-run effect @{kp.lrun}\% on all three; share in output variance: @{kp.y1}\% at 1 quarter, @{kp.y8}\% at 8, @{kp.y24}\% at 24 [@{kp.y24lo}; @{kp.y24hi}]', r'Efectul pe termen lung @{kp.lrun}\% pentru toate trei; ponderea în varianța producției: @{kp.y1}\% la 1 trimestru, @{kp.y8}\% la 8, @{kp.y24}\% la 24 [@{kp.y24lo}; @{kp.y24hi}]')],
    h='0.48\\textheight')

interp(('the common-trends model', 'modelului cu trenduri comune'), [
    T(r'Balanced growth holds by construction in the long run: the shock moves $c$, $i$ and $y$ by the same @{kp.lrun}\%; investment overshoots in the short run', r'Creșterea echilibrată are loc prin construcție pe termen lung: șocul mișcă $c$, $i$ și $y$ cu același @{kp.lrun}\%; investițiile depășesc nivelul final pe termen scurt'),
    T(r'The permanent shock dominates consumption (@{kp.c8}\% at 8 quarters, the permanent-income logic) but explains a minority of output fluctuations at business-cycle horizons', r'Șocul permanent domină consumul (@{kp.c8}\% la 8 trimestre, logica venitului permanent), dar explică o minoritate a fluctuațiilor producției la orizonturile ciclului economic'),
    T(r'Bands are wide: with $T = @{kp.T}$ the data barely separate permanent from transitory variation', r'Benzile sînt largi: cu $T = @{kp.T}$ datele abia separă variația permanentă de cea tranzitorie'),
    T('As in Chapter 3, the economics is in the identifying assumption: here, which relations are stationary', 'Ca în Capitolul 3, partea economică este ipoteza de identificare: aici, care relații sînt staționare')])

D.frame(T('How robust is the answer?', 'Cît de robust este răspunsul?'), table(
    'lcccc', T(r'\textbf{Specification}', r'\textbf{Specificația}') + r' & $h = 1$ & $h = 4$ & $h = 8$ & $h = 24$',
    [T('great ratios, case 3, 1949--1988', 'rapoarte de echilibru, cazul 3, 1949--1988') + r' & @{kp.y1}\% & @{kp.y4}\% & @{kp.y8}\% & @{kp.y24}\%',
     T('great ratios with trend, case 4, 1949--1988', 'rapoarte de echilibru cu trend, cazul 4, 1949--1988') + r' & @{kp.e.y1}\% & @{kp.e.y4}\% & @{kp.e.y8}\% & @{kp.e.y24}\%',
     T('great ratios, case 3, 1949--2019', 'rapoarte de echilibru, cazul 3, 1949--2019') + r' & @{kp.x2019.1}\% & @{kp.x2019.4}\% & @{kp.x2019.8}\% & @{kp.x2019.24}\%',
     T('great ratios, case 3, 1949--2025', 'rapoarte de echilibru, cazul 3, 1949--2025') + r' & @{kp.x2025.1}\% & @{kp.x2025.4}\% & @{kp.x2025.8}\% & @{kp.x2025.24}\%'],
    size='footnotesize') + items(
    T('Share of the permanent shock in the forecast error variance of output, $h$ quarters ahead', 'Ponderea șocului permanent în varianța erorii de prognoză a producției, la $h$ trimestre'),
    T(r'Allowing the ratios to trend (services gaining share) raises the role of the permanent shock considerably at short horizons; extending the sample changes it again; the great-ratio LR rises to @{kp.x2025.lr} on data to 2025',
      r'Permițînd un trend în rapoarte (creșterea ponderii serviciilor), rolul șocului permanent crește considerabil la orizonturi scurte; extinderea eșantionului îl schimbă din nou; statistica LR a rapoartelor de echilibru crește la @{kp.x2025.lr} pe date pînă în 2025'),
    T('Conclusion: the size of ``trend shocks\'\' in the cycle is not pinned down by the data alone', 'Concluzie: importanța „șocurilor de trend” în ciclu nu este determinată doar de date')), 'small')

D.recap(('Structural VECM', 'VECM structural'), [
    T(r'Cointegration splits shocks into $n - r$ permanent and $r$ transitory ones and supplies $rk$ long-run zeros', r'Cointegrarea împarte șocurile în $n - r$ permanente și $r$ tranzitorii și furnizează $rk$ zerouri de termen lung'),
    T(r'With one common trend the permanent shock is $\alpha_\perp\'\varepsilon_t$, scaled', r'Cu un singur trend comun, șocul permanent este $\alpha_\perp\'\varepsilon_t$, scalat'),
    T('KPSW: balanced growth gives a clean identification, but the variance shares depend on the deterministic case and the sample', 'KPSW: creșterea echilibrată dă o identificare curată, dar ponderile varianței depind de cazul determinist și de eșantion')])

# =============================================================================
# 8. ARDL
# =============================================================================
D.section('ARDL and the bounds test', 'ARDL și testul bounds')

D.frame(T('From a VECM to a conditional ECM (1/2)', 'De la VECM la un ECM condiționat (1/2)'), items(
    T(r'Partition $y_t = (y_t, x_t\')\'$, $x_t$ of dimension $k$; if $x_t$ is weakly exogenous and there is one relation involving $y_t$, the conditional model is \[ \Delta y_t = c_0 + c_1t + \pi_{yy}y_{t-1} + \pi_{yx}\'x_{t-1} + \sum_{i=1}^{p-1}\psi_i\Delta y_{t-i} + \sum_{j=0}^{q-1}\omega_j\'\Delta x_{t-j} + u_t \]',
      r'Partiționăm $y_t = (y_t, x_t\')\'$, $x_t$ de dimensiune $k$; dacă $x_t$ este slab exogen și există o singură relație care îl conține pe $y_t$, modelul condiționat este \[ \Delta y_t = c_0 + c_1t + \pi_{yy}y_{t-1} + \pi_{yx}\'x_{t-1} + \sum_{i=1}^{p-1}\psi_i\Delta y_{t-i} + \sum_{j=0}^{q-1}\omega_j\'\Delta x_{t-j} + u_t \]'),
    (T(r'Notation \refPSSb', r'Notațiile \refPSSb'),
     [T(r'$y_t$: the dependent variable; $x_t$: the $k$ forcing variables; $c_0$, $c_1$: intercept and trend coefficient', r'$y_t$: variabila dependentă; $x_t$: cele $k$ variabile explicative; $c_0$, $c_1$: termenul liber și coeficientul trendului'),
      T(r'$\pi_{yy}$ (scalar), $\pi_{yx}$ ($k\times 1$): the coefficients on the lagged levels, i.e.\ the long-run part', r'$\pi_{yy}$ (scalar), $\pi_{yx}$ ($k\times 1$): coeficienții nivelurilor cu lag, adică partea de termen lung'),
      T(r'$\psi_i$, $\omega_j$: short-run coefficients; $p$, $q$: lag orders; $u_t$: the error, uncorrelated with $\Delta x_t$', r'$\psi_i$, $\omega_j$: coeficienții de termen scurt; $p$, $q$: ordinele de lag; $u_t$: eroarea, necorelată cu $\Delta x_t$')])), 'small')

D.frame(T('From a VECM to a conditional ECM (2/2)', 'De la VECM la un ECM condiționat (2/2)'), items(
    (T(r'This is an ARDL($p, q$) in levels, rewritten', r'Este un ARDL($p, q$) în niveluri, rescris'),
     [T(r'long-run coefficients $\theta = -\pi_{yx}/\pi_{yy}$: the equilibrium is $y = \theta\'x$ (plus constant)', r'coeficienții de termen lung $\theta = -\pi_{yx}/\pi_{yy}$: echilibrul este $y = \theta\'x$ (plus o constantă)'),
      T(r'speed of adjustment $\pi_{yy} \in (-1, 0)$: the share of last period\'s disequilibrium corrected this period; half-life $\ln 0.5/\ln(1 + \pi_{yy})$', r'viteza de ajustare $\pi_{yy} \in (-1, 0)$: proporția din dezechilibrul perioadei anterioare corectată în perioada curentă; timpul de înjumătățire $\ln 0.5/\ln(1 + \pi_{yy})$')]),
    (T('Inference', 'Inferența'),
     [T(r'OLS is consistent and $\hat\theta$ has a mixed-Gaussian limit when the lags absorb the endogeneity of $x_t$ \refPSa', r'OLS este consistent, iar $\hat\theta$ are o limită mixt gaussiană cînd lagurile absorb endogenitatea lui $x_t$ \refPSa'),
      T(r'standard errors of $\hat\theta$ by the delta method; $t$-tests on $\theta$ are asymptotically valid', r'erorile standard ale lui $\hat\theta$ prin metoda delta; testele $t$ asupra lui $\theta$ sînt valabile asimptotic')]),
    T(r'The attraction: $x_t$ may be I(0), I(1) or a mix, and we need not pre-test it', r'Avantajul: $x_t$ poate fi I(0), I(1) sau un amestec și nu trebuie testat în prealabil')), 'small')

D.frame(T('The bounds test (1/2)', 'Testul bounds (1/2)'), items(
    (T(r'$H_0$: no level relationship, $\pi_{yy} = 0$ and $\pi_{yx} = 0$', r'$H_0$: nu există relație în niveluri, $\pi_{yy} = 0$ și $\pi_{yx} = 0$'),
     [T(r'$F$: the Wald statistic of these $k + 1$ restrictions, divided by $k + 1$', r'$F$: statistica Wald a acestor $k + 1$ restricții, împărțită la $k + 1$'),
      T(r'$t$: the $t$ ratio of $\hat\pi_{yy}$; it excludes the degenerate case $\pi_{yy} = 0 \ne \pi_{yx}$', r'$t$: raportul $t$ al lui $\hat\pi_{yy}$; exclude cazul degenerat $\pi_{yy} = 0 \ne \pi_{yx}$')]),
    (T(r'The null distribution depends on the integration order of $x_t$', r'Distribuția nulă depinde de ordinul de integrare al lui $x_t$'),
     [T(r'lower bound: all of $x_t$ is I(0); upper bound: all of $x_t$ is I(1)', r'limita inferioară: tot $x_t$ este I(0); limita superioară: tot $x_t$ este I(1)')]),
    (T('Decision', 'Decizia'),
     [T('$F$ above the upper bound: reject, there is a level relationship', '$F$ peste limita superioară: respingem, există relație în niveluri'),
      T('$F$ below the lower bound: do not reject', '$F$ sub limita inferioară: nu respingem'),
      T('between the bounds: inconclusive, the order of integration of $x_t$ matters', 'între limite: neconcludent, ordinul de integrare al lui $x_t$ contează')])), 'small')

D.frame(T('The bounds test (2/2)', 'Testul bounds (2/2)'), items(
    (T('Five cases, as in Johansen', 'Cinci cazuri, ca la Johansen'),
     [T('I: no deterministic terms; II: restricted intercept', 'I: fără termeni determiniști; II: termen liber restricționat'),
      T('III: unrestricted intercept; IV: unrestricted intercept, restricted trend', 'III: termen liber nerestricționat; IV: termen liber nerestricționat, trend restricționat'),
      T('V: unrestricted intercept and trend', 'V: termen liber și trend nerestricționate'),
      T(r'in cases II and IV the restricted terms are part of $H_0$; the $t$-bounds exist for cases I, III, V', r'în cazurile II și IV termenii restricționați fac parte din $H_0$; limitele pentru $t$ există pentru cazurile I, III, V')]),
    (T(r'Simulated 5\% bounds, $k = 1$ ($T = 1000$, @{bd.reps} replications)', r'Limite simulate de 5\%, $k = 1$ ($T = 1000$, @{bd.reps} de replicări)'),
     [T(r'$F$: case II [@{bd.2.1.95.lo}; @{bd.2.1.95.hi}], case III [@{bd.3.1.95.lo}; @{bd.3.1.95.hi}]', r'$F$: cazul II [@{bd.2.1.95.lo}; @{bd.2.1.95.hi}], cazul III [@{bd.3.1.95.lo}; @{bd.3.1.95.hi}]'),
      T(r'$t$, case III: [@{bd.t.lo}; @{bd.t.hi}]', r'$t$, cazul III: [@{bd.t.lo}; @{bd.t.hi}]')])), 'small')

D.frame(T('Critical values in small samples', 'Valori critice în eșantioane mici'), items(
    T(r'PSS tabulate asymptotic bounds ($T = 1000$); with 30--80 annual observations they are too low \refNar',
      r'PSS tabelează limite asimptotice ($T = 1000$); cu 30--80 de observații anuale acestea sînt prea mici \refNar'),
    T(r'Our simulation, case III, $k = 1$, 5\%: $T = 30$: [@{bd.s30.lo}; @{bd.s30.hi}], $T = 80$: [@{bd.s80.lo}; @{bd.s80.hi}], $T = 250$: [@{bd.s250.lo}; @{bd.s250.hi}], asymptotic: [@{bd.3.1.95.lo}; @{bd.3.1.95.hi}]',
      r'Simularea noastră, cazul III, $k = 1$, 5\%: $T = 30$: [@{bd.s30.lo}; @{bd.s30.hi}], $T = 80$: [@{bd.s80.lo}; @{bd.s80.hi}], $T = 250$: [@{bd.s250.lo}; @{bd.s250.hi}], asimptotic: [@{bd.3.1.95.lo}; @{bd.3.1.95.hi}]'),
    T(r'Response-surface regressions give critical values and approximate $p$-values for any $T$, $k$ and lag order \refKS: use them instead of the asymptotic table',
      r'Regresiile de suprafață de răspuns dau valori critice și p-value-uri aproximative pentru orice $T$, $k$ și număr de laguri \refKS: folosiți-le în locul tabelului asimptotic'),
    (T('Frequent misuses in applied work', 'Greșeli frecvente în lucrările aplicate'),
     [T('the wrong case (case III bounds for a model estimated in case II); I(2) regressors, for which the bounds are invalid', 'cazul greșit (limitele cazului III pentru un model estimat în cazul II); regresori I(2), pentru care limitele nu sînt valabile'),
      T(r'feedback from $y_t$ to $x_t$ (no weak exogeneity), or more than one relation among the variables', r'feedback de la $y_t$ la $x_t$ (fără exogenitate slabă) sau mai multe relații între variabile')])), 'small')

D.frame(T('ARDL or VECM?', 'ARDL sau VECM?'), table(
    TB + 'p{3.0cm}' + TB + 'p{4.4cm}' + TB + 'p{4.4cm}', r' & \textbf{ARDL} & \textbf{VECM}',
    [T('Relations', 'Relații') + ' & ' + T('one, normalised on $y_t$', 'una, normalizată pe $y_t$') + ' & ' + T('$r$, rank estimated', '$r$, rangul estimat'),
     T('Regressors', 'Regresori') + ' & ' + T('I(0), I(1) or mixed; weakly exogenous', 'I(0), I(1) sau amestecați; slab exogeni') + ' & ' + T('all I(1); all endogenous', 'toți I(1); toți endogeni'),
     T('Inference', 'Inferență') + ' & ' + T('bounds $F$ and $t$; $\\theta$ by the delta method', 'bounds $F$ și $t$; $\\theta$ prin metoda delta') + ' & ' + T('trace/max-eigenvalue; $\\chi^2$ tests on $\\beta$, $\\alpha$', 'trace/max-eigenvalue; teste $\\chi^2$ pentru $\\beta$, $\\alpha$'),
     T('Small samples', 'Eșantioane mici') + ' & ' + T('few parameters; small-sample bounds needed', 'puțini parametri; necesită limite pentru eșantioane mici') + ' & ' + T('many parameters; bootstrap needed', 'mulți parametri; necesită bootstrap'),
     T('Structural use', 'Utilizare structurală') + ' & ' + T('multipliers of $x$ on $y$', 'multiplicatorii lui $x$ asupra lui $y$') + ' & ' + T('common trends, identified shocks', 'trenduri comune, șocuri identificate')],
    size='scriptsize') + items(
    (T('Rule: estimate the VECM first when you can', 'Regula: estimați întîi VECM cînd este posibil'),
     [T('weakly exogenous regressors and a unique relation: the ARDL is efficient and simpler', 'regresori slab exogeni și o relație unică: ARDL este eficient și mai simplu'),
      T('feedback from $y_t$ to $x_t$: the ARDL estimates are inconsistent', 'feedback de la $y_t$ la $x_t$: estimațiile ARDL sînt inconsistente')])), 'small')

D.frame(T('ARDL pass-through of ROBOR to the lending rate', 'ARDL: transmiterea ROBOR către dobînda la credite'), items(
    T(r'ARDL(@{ar.lend.p}, @{ar.lend.q}) selected by BIC, case II (ROBOR weakly exogenous in the VECM), $n = @{ar.lend.n}$',
      r'ARDL(@{ar.lend.p}, @{ar.lend.q}) ales după BIC, cazul II (ROBOR slab exogen în VECM), $n = @{ar.lend.n}$'),
    (T(r'Bounds $F = @{ar.lend.F}$; 5\% bounds asymptotic [@{bd.2.1.95.lo}; @{bd.2.1.95.hi}], at our $T$ [@{bd.sT2.lo}; @{bd.sT2.hi}]: a level relationship',
       r'Bounds $F = @{ar.lend.F}$; limite de 5\% asimptotice [@{bd.2.1.95.lo}; @{bd.2.1.95.hi}], la $T$-ul nostru [@{bd.sT2.lo}; @{bd.sT2.hi}]: există relație în niveluri'),
     [T(r'the same regression in case III: $F = @{ar.lend3.F}$ against [@{bd.sT.lo}; @{bd.sT.hi}]: inconclusive; $t = @{ar.lend.t}$ against [@{bd.t.lo}; @{bd.t.hi}]',
        r'aceeași regresie în cazul III: $F = @{ar.lend3.F}$ față de [@{bd.sT.lo}; @{bd.sT.hi}]: neconcludent; $t = @{ar.lend.t}$ față de [@{bd.t.lo}; @{bd.t.hi}]')]),
    T(r'Long-run pass-through $\hat\theta = @{ar.lend.theta}$ (SE @{ar.lend.se}): complete pass-through not rejected by the $t$-test; speed $\hat\pi_{yy} = @{ar.lend.phi}$ (SE @{ar.lend.sephi}), half-life @{ar.lend.hl} months',
      r'Transmiterea pe termen lung $\hat\theta = @{ar.lend.theta}$ (SE @{ar.lend.se}): transmiterea completă nu este respinsă de testul $t$; viteza $\hat\pi_{yy} = @{ar.lend.phi}$ (SE @{ar.lend.sephi}), timpul de înjumătățire @{ar.lend.hl} luni'),
    T(r'Deposit rate: $F = @{ar.dep.F}$, $\hat\theta = @{ar.dep.theta}$ (SE @{ar.dep.se}), half-life @{ar.dep.hl} months: incomplete but faster',
      r'Dobînda la depozite: $F = @{ar.dep.F}$, $\hat\theta = @{ar.dep.theta}$ (SE @{ar.dep.se}), timpul de înjumătățire @{ar.dep.hl} luni: incompletă, dar mai rapidă')), 'small')

chart(T('Small-sample bounds and the dynamic multipliers', 'Limitele pentru eșantioane mici și multiplicatorii dinamici'), 'ats_ch4_bounds', 'ATS_ch4_ardl_bounds', [
    T(r'Left: simulated 5\% bounds, case III, $k = 1$, against $T$ (dashed: $T = 1000$); right: cumulative response of the lending rate to a permanent 1 pp rise of ROBOR (dashed: $\hat\theta$)', r'Stînga: limite simulate de 5\%, cazul III, $k = 1$, în funcție de $T$ (punctat: $T = 1000$); dreapta: răspunsul cumulat al dobînzii la credite la o creștere permanentă de 1 pp a ROBOR (punctat: $\hat\theta$)'),
    T(r'Multipliers: @{ar.m0} on impact, @{ar.m6} after 6 months, @{ar.m12} after 12, @{ar.m24} after 24, @{ar.m60} after 60', r'Multiplicatori: @{ar.m0} la impact, @{ar.m6} după 6 luni, @{ar.m12} după 12, @{ar.m24} după 24, @{ar.m60} după 60')],
    h='0.48\\textheight')

interp(('the ARDL results', 'rezultatelor ARDL'), [
    T(r'The upper bound falls from @{bd.s30.hi} at $T = 30$ to @{bd.s250.hi} at $T = 250$: with annual data the asymptotic table over-rejects', r'Limita superioară scade de la @{bd.s30.hi} la $T = 30$ la @{bd.s250.hi} la $T = 250$: cu date anuale tabelul asimptotic respinge prea des'),
    T('The verdict on a level relationship depends on the case: decide case II or III from economics (no drift in rates) before looking at $F$', 'Verdictul asupra relației în niveluri depinde de caz: alegeți cazul II sau III pe criterii economice (dobînzile nu au drift) înainte de a vă uita la $F$'),
    T(r'ARDL and VECM agree on the size of the lending pass-through (@{ar.lend.theta} and @{pt.thl}) but not on the test of $\theta = 1$: different nuisance parameters, different power', r'ARDL și VECM coincid asupra mărimii transmiterii către credite (@{ar.lend.theta} și @{pt.thl}), dar nu asupra testului $\theta = 1$: alți parametri de perturbare, altă putere'),
    T(r'About half of the long-run effect arrives within six months (@{ar.m6}); the rest is slow, with a half-life of the disequilibrium of @{ar.lend.hl} months, consistent with fixed-rate periods and contract repricing', r'Aproximativ jumătate din efectul de termen lung apare în șase luni (@{ar.m6}); restul este lent, cu un timp de înjumătățire a dezechilibrului de @{ar.lend.hl} luni, în acord cu perioadele cu dobîndă fixă și cu reevaluarea contractelor')])

D.frame(T('Two related tools (1/2)', 'Două instrumente înrudite (1/2)'), items(
    (T(r'\textbf{Toda--Yamamoto causality} \refTY', r'\textbf{Cauzalitatea Toda--Yamamoto} \refTY'),
     [T('a VAR of possibly integrated or cointegrated variables', 'un VAR cu variabile posibil integrate sau cointegrate'),
      T(r'fit $p + d_{\max}$ lags in levels and test only the first $p$; $d_{\max}$: the highest suspected order of integration', r'estimăm $p + d_{\max}$ laguri în niveluri și testăm doar primele $p$; $d_{\max}$: ordinul maxim de integrare presupus'),
      T(r'the Wald statistic is asymptotically $\chi^2(p)$ whatever the integration and cointegration properties', r'statistica Wald este asimptotic $\chi^2(p)$ oricare ar fi proprietățile de integrare și cointegrare'),
      T('the price: lower power than a correctly specified VECM', 'prețul: putere mai mică decît un VECM corect specificat')]),
    (T(r'\textbf{Nonlinear ARDL} \refSYG', r'\textbf{ARDL neliniar} \refSYG'),
     [T(r'partial sums of increases: $x_t^+ = \sum_{j\le t}\max(\Delta x_j, 0)$', r'sumele parțiale ale creșterilor: $x_t^+ = \sum_{j\le t}\max(\Delta x_j, 0)$'),
      T(r'partial sums of decreases: $x_t^- = \sum_{j\le t}\min(\Delta x_j, 0)$, so that $x_t = x_0 + x_t^+ + x_t^-$', r'sumele parțiale ale scăderilor: $x_t^- = \sum_{j\le t}\min(\Delta x_j, 0)$, astfel încît $x_t = x_0 + x_t^+ + x_t^-$')])), 'small')

D.frame(T('Two related tools (2/2)', 'Două instrumente înrudite (2/2)'), items(
    (T(r'Nonlinear ARDL: $x_t^+$ and $x_t^-$ as two regressors', r'ARDL neliniar: $x_t^+$ și $x_t^-$ ca doi regresori'),
     [T(r'$x_t^+$ and $x_t^-$ enter the ARDL as two regressors, with long-run coefficients $\theta^+$, $\theta^-$ and short-run coefficients $\omega_j^+$, $\omega_j^-$', r'$x_t^+$ și $x_t^-$ intră în ARDL ca doi regresori, cu coeficienții de termen lung $\theta^+$, $\theta^-$ și cei de termen scurt $\omega_j^+$, $\omega_j^-$'),
      T(r'long-run asymmetry: $\theta^+ \ne \theta^-$; short-run asymmetry: different $\omega_j^+$ and $\omega_j^-$', r'asimetrie pe termen lung: $\theta^+ \ne \theta^-$; asimetrie pe termen scurt: $\omega_j^+$ și $\omega_j^-$ diferiți'),
      T(r'both tested by Wald tests; the bounds test uses $k = 2$', r'ambele se testează prin teste Wald; testul bounds folosește $k = 2$')]),
    (T(r'Classic use: ``rockets and feathers\'\' \refBac', r'Utilizarea clasică: „rockets and feathers” \refBac'),
     [T('retail fuel prices rise fast with oil and fall slowly', 'prețurile carburanților cresc repede cu petrolul și scad încet'),
      T('Seminar 4 tests it for Romania', 'Seminarul 4 testează acest lucru pentru România')])), 'small')

D.recap(('ARDL and the bounds test', 'ARDL și testul bounds'), [
    T('The conditional ECM is an ARDL rewritten; it needs weak exogeneity and a single relation', 'ECM-ul condiționat este un ARDL rescris; necesită exogenitate slabă și o singură relație'),
    T('The bounds test avoids pre-testing the regressors, at the price of an inconclusive zone', 'Testul bounds evită testarea prealabilă a regresorilor, cu prețul unei zone neconcludente'),
    T('Use the right case and small-sample (response-surface) critical values', 'Folosiți cazul corect și valori critice pentru eșantioane mici (suprafețe de răspuns)'),
    T('Toda--Yamamoto for causality without pre-testing; NARDL for asymmetric adjustment', 'Toda--Yamamoto pentru cauzalitate fără testare prealabilă; NARDL pentru ajustare asimetrică')])

# =============================================================================
# 9. PANEL
# =============================================================================
D.section('Panel time series', 'Serii de timp panel')

D.frame(T('Panels: the gain and the new problems', 'Datele panel: cîștigul și problemele noi'), two(
    ph('ecb', T('The ECB seat, Frankfurt', 'Sediul BCE, Frankfurt'), h='0.27\\textheight'),
    items((T('The gain: $N$ countries add information', 'Cîștigul: $N$ țări adaugă informație'),
           [T('country series are short: 20--30 years of annual data', 'seriile pe țări sînt scurte: 20--30 de ani de date anuale'),
            T('a single-country rank or bounds test has little power', 'un test de rang sau bounds pentru o singură țară are putere mică')]),
          (T(r'Asymptotics in two dimensions \refPM, \refKao', r'Asimptotică în două dimensiuni \refPM, \refKao'),
           [T(r'sequential ($T \to \infty$, then $N \to \infty$) or joint, with $N/T \to 0$', r'secvențială ($T \to \infty$, apoi $N \to \infty$) sau comună, cu $N/T \to 0$'),
            T('a panel regression of I(1) series estimates an average long-run relation even without cointegration', 'o regresie panel cu serii I(1) estimează o relație medie de termen lung chiar fără cointegrare')]),
          (T('Two new problems', 'Două probleme noi'),
           [T(r'\textbf{heterogeneity}: the dynamics differ across countries', r'\textbf{eterogenitatea}: dinamica diferă între țări'),
            T(r'\textbf{cross-section dependence}: common shocks (2009, COVID-19, the euro)', r'\textbf{dependența între unități}: șocuri comune (2009, COVID-19, euro)'),
            T(r'first-generation tests assume independent units; second-generation tests model the dependence \refBrP', r'testele de primă generație presupun unități independente; cele de generația a doua modelează dependența \refBrP')])), '0.30', '0.68'), 'footnotesize')

D.frame(T('Measuring cross-section dependence', 'Măsurarea dependenței între unități'), items(
    (T(r'\textbf{CD} statistic \refPesE: the scaled sum of all pairwise correlations \[ CD = \sqrt{\dfrac{2T}{N(N - 1)}}\sum_{i<j}\hat\rho_{ij} \to N(0, 1) \]',
       r'Statistica \textbf{CD} \refPesE: suma scalată a tuturor corelațiilor pe perechi \[ CD = \sqrt{\dfrac{2T}{N(N - 1)}}\sum_{i<j}\hat\rho_{ij} \to N(0, 1) \]'),
     [T(r'$\hat\rho_{ij}$: the correlation over time between the residuals (or demeaned series) of units $i$ and $j$; $N$: number of units; $T$: number of periods', r'$\hat\rho_{ij}$: corelația în timp dintre reziduurile (sau seriile centrate) unităților $i$ și $j$; $N$: numărul de unități; $T$: numărul de perioade'),
      T(r'reading: $CD \approx 0$ under the null; $|CD| > 1.96$ rejects it at 5\%', r'citirea: $CD \approx 0$ sub ipoteza nulă; $|CD| > 1.96$ o respinge la 5\%')]),
    (T(r'The null is \emph{weak} dependence \refPesC', r'Ipoteza nulă este dependența \emph{slabă} \refPesC'),
     [T(r'correlation that vanishes on average as $N$ grows', r'o corelație care dispare în medie cînd $N$ crește'),
      T(r'a common factor with non-zero mean loadings gives $|CD| \to \infty$', r'un factor comun cu încărcări de medie nenulă dă $|CD| \to \infty$'),
      T('valid for fixed $T$ and large $N$, also in dynamic and unit-root panels', 'valabilă pentru $T$ fix și $N$ mare, și în panele dinamice sau cu rădăcini unitare'),
      T(r'positive and negative correlations can offset each other: report the mean $|\hat\rho_{ij}|$ as well', r'corelațiile pozitive și negative se pot compensa: raportați și media $|\hat\rho_{ij}|$')])), 'small')

D.frame(T('Cross-section dependence in EU-27 data', 'Dependența între unități în panelul UE-27'), items(
    (T(r'EU-27, $T = @{pn.T}$ (@{pn.first}--@{pn.last})', r'UE-27, $T = @{pn.T}$ (@{pn.first}--@{pn.last})'),
     [T(r'consumption growth: CD = @{pn.cd.c}, mean $|\hat\rho_{ij}| = @{pn.rho.c}$', r'creșterea consumului: CD = @{pn.cd.c}, media $|\hat\rho_{ij}| = @{pn.rho.c}$'),
      T(r'income growth: CD = @{pn.cd.y}; inflation: CD = @{pn.cd.pi}', r'creșterea venitului: CD = @{pn.cd.y}; inflația: CD = @{pn.cd.pi}')]),
    (T('Interpretation', 'Interpretarea'),
     [T(r'every statistic is far above 1.96: strong dependence everywhere', r'fiecare statistică depășește cu mult 1,96: dependență puternică peste tot'),
      T('first-generation panel tests are not reliable for these data', 'testele panel de primă generație nu sînt fiabile pentru aceste date')])), 'small')

D.frame(T('Panel unit-root tests (1/2)', 'Teste de rădăcină unitară în panel (1/2)'), items(
    (T(r'\textbf{LLC} \refLLC: one ADF regression per unit with a common $\rho$ \[ \Delta y_{it} = \mu_i + \rho y_{i,t-1} + \sum_j\gamma_{ij}\Delta y_{i,t-j} + e_{it} \]',
       r'\textbf{LLC} \refLLC: cîte o regresie ADF pe unitate, cu $\rho$ comun \[ \Delta y_{it} = \mu_i + \rho y_{i,t-1} + \sum_j\gamma_{ij}\Delta y_{i,t-j} + e_{it} \]'),
     [T(r'$y_{it}$: unit $i$ at time $t$; $\mu_i$: unit intercepts; $\gamma_{ij}$: unit-specific lag coefficients; $e_{it}$: errors', r'$y_{it}$: unitatea $i$ la momentul $t$; $\mu_i$: termenii liberi ai unităților; $\gamma_{ij}$: coeficienții lagurilor, specifici unității; $e_{it}$: erorile'),
      T(r'$H_0$: $\rho = 0$ (unit root in every unit); $H_1$: $\rho < 0$, all units stationary with the same $\rho$', r'$H_0$: $\rho = 0$ (rădăcină unitară în fiecare unitate); $H_1$: $\rho < 0$, toate unitățile staționare cu același $\rho$'),
      T('pooled $t$ on orthogonalised, variance-normalised residuals, adjusted by tabulated mean and variance', '$t$ comun pe reziduuri ortogonalizate și normalizate, ajustat cu media și varianța tabelate')]),
    (T(r'\textbf{IPS} \refIPS: heterogeneous $\rho_i$; average the individual ADF statistics $t_i$ and standardise \[ \bar t = N^{-1}\sum_i t_i, \qquad Z = \sqrt N(\bar t - \E t)/\sqrt{\Var(t)} \to N(0, 1) \]',
       r'\textbf{IPS} \refIPS: $\rho_i$ eterogeni; facem media statisticilor ADF individuale $t_i$ și o standardizăm \[ \bar t = N^{-1}\sum_i t_i, \qquad Z = \sqrt N(\bar t - \E t)/\sqrt{\Var(t)} \to N(0, 1) \]'),
     [T(r'$\E t$, $\Var(t)$: the mean and variance of one ADF $t$ under the null (tabulated); a very negative $Z$ rejects', r'$\E t$, $\Var(t)$: media și varianța unei statistici ADF $t$ sub ipoteza nulă (tabelate); un $Z$ foarte negativ respinge'),
      T(r'$H_1$: a non-zero fraction of units is stationary; rejection does not say which', r'$H_1$: o fracțiune nenulă de unități este staționară; respingerea nu spune care')])), 'small')

D.frame(T('Panel unit-root tests (2/2)', 'Teste de rădăcină unitară în panel (2/2)'), items(
    (T(r'\textbf{CIPS} \refPesB: one common factor $f_t$ in the errors; augment each ADF with $\bar y_{t-1}$ and $\Delta\bar y_{t-j}$ (CADF), average the $t$-ratios',
       r'\textbf{CIPS} \refPesB: un factor comun $f_t$ în erori; augmentăm fiecare ADF cu $\bar y_{t-1}$ și $\Delta\bar y_{t-j}$ (CADF) și facem media rapoartelor $t$'),
     [T(r'$\bar y_t = N^{-1}\sum_i y_{it}$: the cross-section average at time $t$; $f_t$: an unobserved shock common to all units', r'$\bar y_t = N^{-1}\sum_i y_{it}$: media pe secțiune la momentul $t$; $f_t$: un șoc neobservat comun tuturor unităților'),
      T(r'the cross-section averages proxy $f_t$; the distribution is non-standard and tabulated', r'mediile pe secțiune aproximează $f_t$; distribuția este nestandard și tabelată')]),
    T(r'Under strong dependence LLC and IPS over-reject: they treat 27 correlated countries as 27 independent pieces of evidence',
      r'În prezența unei dependențe puternice, LLC și IPS resping prea des: tratează 27 de țări corelate ca 27 de dovezi independente')), 'small')

D.frame(T('Panel unit roots in EU-27 data', 'Rădăcini unitare în panelul UE-27'), table(
    'lccc', T(r'\textbf{Variable}', r'\textbf{Variabila}') + r' & LLC & IPS $\bar t$ & CIPS',
    [T('consumption (trend)', 'consum (trend)') + r' & @{pn.c.llc} (@{pn.c.llc.p}) & @{pn.c.ips} (@{pn.c.ips.p}) & @{pn.c.cips} (@{pn.c.cips.p})',
     T('income (trend)', 'venit (trend)') + r' & @{pn.y.llc} (@{pn.y.llc.p}) & @{pn.y.ips} (@{pn.y.ips.p}) & @{pn.y.cips} (@{pn.y.cips.p})',
     T('inflation (constant)', 'inflație (constantă)') + r' & @{pn.pi.llc} (@{pn.pi.llc.p}) & @{pn.pi.ips} (@{pn.pi.ips.p}) & @{pn.pi.cips} (@{pn.pi.cips.p})'],
    size='footnotesize') + items(
    T(r'$c$, $y$: $100\ln$ real per capita household consumption and disposable income; $\pi$: consumption-deflator inflation; $N = @{pn.N}$, $T = @{pn.T}$, one lag',
      r'$c$, $y$: $100\ln$ consumul real și venitul disponibil real pe locuitor ale gospodăriilor; $\pi$: inflația deflatorului consumului; $N = @{pn.N}$, $T = @{pn.T}$, un lag'),
    T(r'$p$-values in brackets from @{pn.reps} simulations of the null with independent units, for our $N$ and $T$ (replacing the tabulated moments)',
      r'P-value-urile din paranteze provin din @{pn.reps} de simulări ale ipotezei nule cu unități independente, pentru $N$ și $T$ ale noastre (în locul momentelor tabelate)'),
    T(r'Consumption: IPS rejects the unit root (@{pn.c.ips.p.e}), CIPS does not (@{pn.c.cips.p.e}): the ``stationarity\'\' was a common factor; inflation is stationary by every test',
      r'Consumul: IPS respinge rădăcina unitară (@{pn.c.ips.p.e}), CIPS nu (@{pn.c.cips.p.e}): „staționaritatea” era un factor comun; inflația este staționară după toate testele')), 'small')

D.frame(T('Panel cointegration tests (1/2)', 'Teste de cointegrare în panel (1/2)'), items(
    (T(r'\textbf{Residual-based} \refPedA, \refPedC: estimate $y_{it} = a_i + \delta_it + \beta_i\'x_{it} + e_{it}$ country by country and test the residuals for a unit root',
       r'\textbf{Pe reziduuri} \refPedA, \refPedC: estimăm $y_{it} = a_i + \delta_it + \beta_i\'x_{it} + e_{it}$ țară cu țară și testăm rădăcina unitară a reziduurilor'),
     [T(r'$a_i$, $\delta_i$: country intercept and trend; $\beta_i$: country cointegrating coefficients; $e_{it}$: the equilibrium error, I(1) under $H_0$', r'$a_i$, $\delta_i$: termenul liber și trendul țării; $\beta_i$: coeficienții de cointegrare ai țării; $e_{it}$: eroarea de echilibru, I(1) sub $H_0$'),
      T('seven statistics: four ``panel\'\' (within, common AR coefficient) and three ``group\'\' (between, heterogeneous); $H_0$: no cointegration in any unit', 'șapte statistici: patru „panel” (within, coeficient AR comun) și trei „group” (between, eterogene); $H_0$: nicio unitate nu este cointegrată'),
      T(r'they impose a common-factor restriction (short-run dynamics of $x$ and $y$ alike); \refKao\ is the homogeneous special case', r'impun o restricție de factor comun (dinamica pe termen scurt a lui $x$ și $y$ la fel); \refKao\ este cazul particular omogen')]),
    (T(r'\textbf{ECM-based} \refWes: test whether each country\'s ECM has error correction \[ \Delta y_{it} = d_i + \alpha_iy_{i,t-1} + \lambda_i\'x_{i,t-1} + \sum_j a_{ij}\Delta y_{i,t-j} + \sum_j\gamma_{ij}\'\Delta x_{i,t-j} + e_{it} \]',
       r'\textbf{Pe ECM} \refWes: testăm dacă ECM-ul fiecărei țări are corecție a erorii \[ \Delta y_{it} = d_i + \alpha_iy_{i,t-1} + \lambda_i\'x_{i,t-1} + \sum_j a_{ij}\Delta y_{i,t-j} + \sum_j\gamma_{ij}\'\Delta x_{i,t-j} + e_{it} \]'),
     [T(r'$\alpha_i$: the speed of adjustment of country $i$; $\lambda_i$: its level coefficients on $x$; $d_i$, $a_{ij}$, $\gamma_{ij}$: deterministic and short-run terms', r'$\alpha_i$: viteza de ajustare a țării $i$; $\lambda_i$: coeficienții nivelurilor lui $x$; $d_i$, $a_{ij}$, $\gamma_{ij}$: termenii determiniști și de termen scurt'),
      T(r'$H_0$: $\alpha_i = 0$ for all $i$ (no error correction anywhere); negative statistics reject', r'$H_0$: $\alpha_i = 0$ pentru orice $i$ (nicio corecție a erorii); statisticile negative resping')])), 'small')

D.frame(T('Panel cointegration tests (2/2)', 'Teste de cointegrare în panel (2/2)'), items(
    (T(r'Westerlund statistics', r'Statisticile Westerlund'),
     [T(r'group: $G_t = N^{-1}\sum_i\hat\alpha_i/\mathrm{SE}(\hat\alpha_i)$, $G_a = N^{-1}\sum_i T\hat\alpha_i/\hat\alpha_i(1)$; $H_1$: some countries adjust', r'de grup: $G_t = N^{-1}\sum_i\hat\alpha_i/\mathrm{SE}(\hat\alpha_i)$, $G_a = N^{-1}\sum_i T\hat\alpha_i/\hat\alpha_i(1)$; $H_1$: unele țări se ajustează'),
      T(r'$\hat\alpha_i(1) = 1 - \sum_j\hat a_{ij}$: scales $\hat\alpha_i$ to the long-run adjustment', r'$\hat\alpha_i(1) = 1 - \sum_j\hat a_{ij}$: scalează $\hat\alpha_i$ la ajustarea pe termen lung'),
      T(r'panel: $P_t$, $P_a$, the same ratios for a common $\alpha$; $H_1$: all countries adjust', r'panel: $P_t$, $P_a$, aceleași rapoarte pentru un $\alpha$ comun; $H_1$: toate țările se ajustează'),
      T('bootstrap critical values under cross-section dependence', 'valori critice bootstrap în prezența dependenței între unități')]),
    (T(r'EU-27, $c$ on $y$ and $\pi$ (null distributions simulated)', r'UE-27, $c$ pe $y$ și $\pi$ (distribuții nule simulate)'),
     [T(r'Pedroni group ADF (the mean of the country ADF $t$-ratios of $\hat e_{it}$): @{pn.ped}, 5\% critical value @{pn.ped.cv}, @{pn.ped.p.e}', r'Pedroni group ADF (media rapoartelor $t$ ADF ale lui $\hat e_{it}$ pe țări): @{pn.ped}, valoarea critică 5\% @{pn.ped.cv}, @{pn.ped.p.e}'),
      T(r'Westerlund $G_t$: @{pn.wgt}, 5\% critical value @{pn.wgt.cv}, @{pn.wgt.p.e}', r'Westerlund $G_t$: @{pn.wgt}, valoarea critică 5\% @{pn.wgt.cv}, @{pn.wgt.p.e}')]),
    (T('The two families disagree', 'Cele două familii nu sînt de acord'),
     [T(r'the residual-based test rejects, the ECM test does not', r'testul pe reziduuri respinge, testul ECM nu'),
      T(r'with $T = @{pn.T}$ and strong dependence, neither verdict is secure', r'cu $T = @{pn.T}$ și dependență puternică, niciun verdict nu este sigur')])), 'small')

D.frame(T('Estimators of the long-run relation (1/3)', 'Estimatori ai relației de termen lung (1/3)'), items(
    (T(r'\textbf{Panel FMOLS/DOLS} \refPedB', r'\textbf{FMOLS/DOLS panel} \refPedB'),
     [T(r'FMOLS: fully modified OLS, corrected for endogeneity and serial correlation \refPH', r'FMOLS: OLS complet modificat, corectat pentru endogenitate și autocorelare \refPH'),
      T(r'DOLS: OLS with leads and lags of $\Delta x$ \refSai, \refSWa', r'DOLS: OLS cu valori viitoare (leads) și laguri ale lui $\Delta x$ \refSai, \refSWa'),
      T('estimated per country and averaged (group mean)', 'estimate pe țări și apoi mediate (group mean)')]),
    (T(r'\textbf{Mean group (MG)} \refPSm', r'\textbf{Mean group (MG)} \refPSm'),
     [T(r'estimate each country\'s ARDL and average the long-run coefficients: $\hat\theta_{MG} = N^{-1}\sum_i\hat\theta_i$', r'estimăm ARDL pentru fiecare țară și facem media coeficienților de termen lung: $\hat\theta_{MG} = N^{-1}\sum_i\hat\theta_i$'),
      T(r'consistent under full heterogeneity; SE $= s_\theta/\sqrt N$, $s_\theta$: the cross-country standard deviation of $\hat\theta_i$', r'consistent sub eterogenitate completă; SE $= s_\theta/\sqrt N$, $s_\theta$: abaterea standard a lui $\hat\theta_i$ între țări'),
      T('pooled fixed effects with common slopes are inconsistent when the true slopes differ, even for large $T$; for small $T$ the Nickell bias adds \\refNic',
        'efectele fixe cu pante comune sînt inconsistente cînd pantele reale diferă, chiar pentru $T$ mare; pentru $T$ mic se adaugă deplasarea Nickell \\refNic')])), 'small')

D.frame(T('Estimators of the long-run relation (2/3)', 'Estimatori ai relației de termen lung (2/3)'), items(
    (T(r'\textbf{CCE} \refPesA', r'\textbf{CCE} \refPesA'),
     [T(r'model: $y_{it} = \alpha_i + \beta_i\'x_{it} + \gamma_i\'f_t + e_{it}$', r'modelul: $y_{it} = \alpha_i + \beta_i\'x_{it} + \gamma_i\'f_t + e_{it}$'),
      T(r'estimation: add the cross-section averages $\bar y_t, \bar x_t$ to each regression', r'estimarea: adăugăm mediile pe secțiune $\bar y_t, \bar x_t$ în fiecare regresie'),
      T(r'$f_t$: unobserved common factors; $\gamma_i$: the country loadings on them; the averages $\bar y_t, \bar x_t$ absorb $f_t$', r'$f_t$: factori comuni neobservați; $\gamma_i$: încărcările țării pe acești factori; mediile $\bar y_t, \bar x_t$ preiau $f_t$'),
      T(r'valid with non-stationary factors \refKPY; dynamic version CS-ARDL \refCP', r'valabil și cu factori nestaționari \refKPY; versiunea dinamică CS-ARDL \refCP')])), 'small')

D.frame(T('Estimators of the long-run relation (3/3)', 'Estimatori ai relației de termen lung (3/3)'), items(
    (T(r'\textbf{Pooled mean group (PMG)} \refPSSa: a common long run inside country-specific ECMs \[ \Delta y_{it} = \phi_i(y_{i,t-1} - \theta\'x_{i,t-1}) + \sum_j\lambda_{ij}\Delta y_{i,t-j} + \sum_j\delta_{ij}\'\Delta x_{i,t-j} + \mu_i + \varepsilon_{it} \]',
       r'\textbf{Pooled mean group (PMG)} \refPSSa: un termen lung comun în ECM-uri specifice fiecărei țări \[ \Delta y_{it} = \phi_i(y_{i,t-1} - \theta\'x_{i,t-1}) + \sum_j\lambda_{ij}\Delta y_{i,t-j} + \sum_j\delta_{ij}\'\Delta x_{i,t-j} + \mu_i + \varepsilon_{it} \]'),
     [T(r'$\theta$: the long-run coefficients, common to all countries; $\phi_i$: the country speed of adjustment, $\phi_i < 0$ required', r'$\theta$: coeficienții de termen lung, comuni tuturor țărilor; $\phi_i$: viteza de ajustare a țării, cu condiția $\phi_i < 0$'),
      T(r'$\lambda_{ij}$, $\delta_{ij}$, $\mu_i$, $\sigma_i^2 = \Var\varepsilon_{it}$: short run, intercept and error variance, all country-specific', r'$\lambda_{ij}$, $\delta_{ij}$, $\mu_i$, $\sigma_i^2 = \Var\varepsilon_{it}$: termenul scurt, termenul liber și varianța erorii, toate specifice țării'),
      T(r'ML: maximise $-\sum_i\tfrac{T_i}{2}\ln\hat\sigma_i^2(\theta)$ over $\theta$; $T_i$: the sample length of country $i$ (derivation: Appendix)  % applink: PMG likelihood', r'ML: maximizăm $-\sum_i\tfrac{T_i}{2}\ln\hat\sigma_i^2(\theta)$ după $\theta$; $T_i$: lungimea eșantionului țării $i$ (derivarea: Anexa)  % applink: verosimilitatea PMG')]),
    (T(r'Hausman test of $\theta_{MG} = \theta_{PMG}$', r'Testul Hausman pentru $\theta_{MG} = \theta_{PMG}$'),
     [T(r'$H = (\hat\theta_{MG} - \hat\theta_{PMG})\'[\widehat\Var(\hat\theta_{MG}) - \widehat\Var(\hat\theta_{PMG})]^{-1}(\hat\theta_{MG} - \hat\theta_{PMG}) \to \chi^2(\dim\theta)$', r'$H = (\hat\theta_{MG} - \hat\theta_{PMG})\'[\widehat\Var(\hat\theta_{MG}) - \widehat\Var(\hat\theta_{PMG})]^{-1}(\hat\theta_{MG} - \hat\theta_{PMG}) \to \chi^2(\dim\theta)$'),
      T(r'PMG is efficient under homogeneity, MG consistent in both cases: a small $H$ (large p-value) supports pooling', r'PMG este eficient sub omogenitate, MG consistent în ambele cazuri: un $H$ mic (p-value mare) susține coeficienții comuni')])), 'small')

D.frame(T('Case study: Pesaran, Shin and Smith (1999)', 'Studiu de caz: Pesaran, Shin și Smith (1999)'), items(
    (T(r'\refPSSa', r'\refPSSa'),
     [T('consumption functions for OECD countries, annual data', 'funcții de consum pentru țări OCDE, date anuale'),
      T('ARDL in log real per capita consumption, log real per capita disposable income and inflation', 'ARDL pentru logaritmul consumului real pe locuitor, logaritmul venitului disponibil real pe locuitor și inflație'),
      T('they compare MG, PMG and dynamic fixed effects and use Hausman tests to decide whether the long-run income and inflation effects can be pooled',
        'compară MG, PMG și efectele fixe dinamice și folosesc teste Hausman pentru a decide dacă efectele pe termen lung ale venitului și inflației pot fi comune'),
      T('their argument: theory (permanent income) restricts the long run; adjustment speeds, habits and credit constraints differ across countries',
        'argumentul lor: teoria (venitul permanent) restricționează termenul lung; vitezele de ajustare, obiceiurile și constrîngerile de credit diferă între țări')]),
    (T(r'Our replication of the specification on EU-27, @{pn.first}--@{pn.last}, ARDL(1,1,1) for every country, $@{pn.nobs}$ observations',
       r'Replicarea specificației pe UE-27, @{pn.first}--@{pn.last}, ARDL(1,1,1) pentru fiecare țară, $@{pn.nobs}$ de observații'),
     [T(r'$c_{it}$ on $y_{it}$ and $\pi_{it}$ as defined above; national currencies (country intercepts absorb the units)', r'$c_{it}$ pe $y_{it}$ și $\pi_{it}$ ca mai sus; monede naționale (termenii liberi pe țări absorb unitățile)')]),
    T(r'We start in 2000 to avoid the inflation episodes of the 1990s in Bulgaria and Romania, which would dominate a pooled inflation coefficient',
      r'Pornim din 2000 pentru a evita episoadele de inflație din anii 1990 din Bulgaria și România, care ar domina un coeficient comun al inflației')), 'small')

chart(T('Heterogeneity across the EU', 'Eterogenitatea în UE'), 'ats_ch4_panel', 'ATS_ch4_panel', [
    T(r'Left: consumption growth (Romania in red, cross-section average in dark blue); right: country long-run income elasticities from the individual ARDLs, with MG, PMG and CCEMG', r'Stînga: creșterea consumului (România cu roșu, media pe secțiune cu albastru închis); dreapta: elasticitățile de termen lung față de venit din ARDL-urile individuale, cu MG, PMG și CCEMG'),
    T(r'Country elasticities range from @{pn.thmin} to @{pn.thmax}; Romania @{pn.thro}', r'Elasticitățile pe țări variază între @{pn.thmin} și @{pn.thmax}; România @{pn.thro}')],
    h='0.5\\textheight')

D.frame(T('Long-run estimates for EU-27', 'Estimații de termen lung pentru UE-27'), table(
    'lccc', T(r'\textbf{Estimator}', r'\textbf{Estimatorul}') + r' & $\theta_y$ & $\theta_\pi$ & $\phi$',
    [r'MG & @{pn.mg.y} (@{pn.mg.y.se}) & @{pn.mg.pi} (@{pn.mg.pi.se}) & @{pn.mg.phi} (@{pn.mg.phi.se})',
     r'PMG & @{pn.pmg.y} (@{pn.pmg.y.se}) & @{pn.pmg.pi} (@{pn.pmg.pi.se}) & @{pn.pmg.phi} (@{pn.pmg.phi.se})',
     T('dynamic FE', 'efecte fixe dinamice') + r' & @{pn.dfe.y} (@{pn.dfe.y.se}) & @{pn.dfe.pi} (@{pn.dfe.pi.se}) & @{pn.dfe.phi} (@{pn.dfe.phi.se})',
     T('group-mean DOLS', 'DOLS group mean') + r' & @{pn.dols.y} (@{pn.dols.y.se}) & @{pn.dols.pi} (@{pn.dols.pi.se}) & --',
     r'CCEMG & @{pn.cce.y} (@{pn.cce.y.se}) & @{pn.cce.pi} (@{pn.cce.pi.se}) & --'],
    size='footnotesize') + items(
    T(r'Standard errors in brackets (MG, DOLS, CCEMG: dispersion of country estimates; PMG: likelihood; FE: clustered by country)',
      r'Erorile standard în paranteze (MG, DOLS, CCEMG: dispersia estimațiilor pe țări; PMG: verosimilitatea; FE: grupate pe țări)'),
    T(r'Hausman MG against PMG: $H = @{pn.H}$, $\chi^2(2)$, @{pn.pH.e}; CD of the PMG residuals: @{pn.cdpmg}',
      r'Hausman MG față de PMG: $H = @{pn.H}$, $\chi^2(2)$, @{pn.pH.e}; CD pentru reziduurile PMG: @{pn.cdpmg}')), 'small')

interp(('the panel estimates', 'estimațiilor panel'), [
    T(r'The income elasticity lies between @{pn.mg.y} (MG) and @{pn.dfe.y} (FE), clearly below one: consumption does not track income one for one over 2001--2022', r'Elasticitatea față de venit se află între @{pn.mg.y} (MG) și @{pn.dfe.y} (FE), clar sub unu: consumul nu urmează venitul unu la unu în 2001--2022'),
    T('The Hausman test does not reject pooling, so PMG is the efficient choice for the income effect', 'Testul Hausman nu respinge coeficienții comuni, deci PMG este alegerea eficientă pentru efectul venitului'),
    T(r'The inflation effect is not robust: its sign and size change with the estimator; do not report one of them alone', r'Efectul inflației nu este robust: semnul și mărimea lui se schimbă cu estimatorul; nu raportați doar unul dintre ele'),
    T(r'PMG residuals remain strongly dependent (CD = @{pn.cdpmg}): standard errors that ignore common shocks are too small; CCEMG is the safer benchmark', r'Reziduurile PMG rămîn puternic dependente (CD = @{pn.cdpmg}): erorile standard care ignoră șocurile comune sînt prea mici; CCEMG este reperul mai sigur')])

D.frame(T('Panel VAR in one slide', 'VAR panel pe scurt'), items(
    (T(r'$y_{it} = \mu_i + \sum_{j=1}^pA_jy_{i,t-j} + \varepsilon_{it}$: common dynamics, country fixed effects \refHNR',
       r'$y_{it} = \mu_i + \sum_{j=1}^pA_jy_{i,t-j} + \varepsilon_{it}$: dinamică comună, efecte fixe pe țări \refHNR'),
     [T(r'$y_{it}$: the vector of variables of country $i$; $A_j$: lag matrices common to all countries; $\mu_i$: country fixed effects; $\varepsilon_{it}$: innovations', r'$y_{it}$: vectorul variabilelor țării $i$; $A_j$: matricele lagurilor, comune tuturor țărilor; $\mu_i$: efectele fixe ale țărilor; $\varepsilon_{it}$: inovațiile')]),
    T(r'With small $T$ the within estimator is biased by $O(1/T)$ (Nickell); estimate by GMM on forward-orthogonal deviations with lagged levels as instruments \refAL',
      r'Pentru $T$ mic estimatorul within are o deplasare de ordinul $1/T$ (Nickell); estimăm prin GMM pe abateri ortogonale înainte, cu niveluri cu lag ca instrumente \refAL'),
    T('Identification of shocks as in Chapter 3 (Cholesky, signs); impulse responses and FEVD are common to all countries',
      'Identificarea șocurilor ca în Capitolul 3 (Cholesky, semne); răspunsurile la impuls și FEVD sînt comune tuturor țărilor'),
    T('Homogeneity of $A_j$ is the strong assumption: with macro panels of moderate $T$, mean-group VARs or CCE-augmented VARs are the heterogeneous alternatives',
      'Omogenitatea lui $A_j$ este ipoteza puternică: în panelurile macro cu $T$ moderat, VAR-urile mean group sau VAR-urile augmentate CCE sînt alternativele eterogene')), 'small')

D.recap(('Panel time series', 'serii de timp panel'), [
    T('Test for cross-section dependence first; with strong dependence use CIPS and CCE, not LLC/IPS and pooled OLS', 'Testați întîi dependența între unități; dacă este puternică, folosiți CIPS și CCE, nu LLC/IPS și OLS comun'),
    T('Panel cointegration tests differ in their null and in the common-factor restriction; disagreement is informative', 'Testele de cointegrare în panel diferă prin ipoteza nulă și prin restricția de factor comun; dezacordul este informativ'),
    T('MG for heterogeneity, PMG when theory pools the long run, Hausman to decide, CCE against common factors', 'MG pentru eterogenitate, PMG cînd teoria impune un termen lung comun, Hausman pentru decizie, CCE contra factorilor comuni')])

# =============================================================================
# 10. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Is the long-run pass-through of money-market rates to bank lending rates complete in Romania, and did it change after the 2022 tightening?', 'Este completă transmiterea pe termen lung a dobînzilor pieței monetare către dobînzile la credite în România și s-a schimbat după înăsprirea din 2022?'),
     [T(r'formal: $H_0$: $\theta_{\text{lend}} = 1$ in a rank-2 VECM with ROBOR weakly exogenous; against a break in $\theta$ or in the markup in 2022',
        r'formal: $H_0$: $\theta_{\text{credit}} = 1$ într-un VECM de rang 2 cu ROBOR slab exogen; față de o ruptură în $\theta$ sau în marjă în 2022'),
      T('falsified by a robust rejection: across pre-registered lag lengths, deterministic cases and bootstrap inference', 'infirmată de o respingere robustă: pentru numere de laguri, cazuri deterministe și inferență bootstrap preînregistrate')]),
    (T('Why it matters: the speed and completeness of pass-through decide how much the BNR must move its rate to move credit conditions', 'Miza: viteza și completitudinea transmiterii decid cît trebuie să miște BNR dobînda de politică pentru a schimba condițiile de creditare'),
     [T(r'literature to start from: \refdB, \refECR, \refJohD, \refCRT, \refPSSb', r'literatura de pornire: \refdB, \refECR, \refJohD, \refCRT, \refPSSb')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed studies of interest-rate pass-through in Central and Eastern Europe that use cointegrated VARs or ARDL; give DOIs.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează studii recenzate despre transmiterea dobînzilor în Europa Centrală și de Est care folosesc VAR cointegrate sau ARDL; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Propose three reasons why lending-rate pass-through could exceed one, and one testable implication of each.}', r'\textbf{ipoteza}: \aiprompt{Propune trei motive pentru care transmiterea către dobînzile la credite ar putea depăși unu și cîte o implicație testabilă pentru fiecare.}'),
      T(r'\textbf{code and replication}: ask for a Johansen function with restricted constant, then reproduce a known number first (the eigenvalues of this lecture)', r'\textbf{cod și replicare}: cereți o funcție Johansen cu constantă restricționată, apoi reproduceți întîi o cifră cunoscută (valorile proprii din acest curs)'),
      T(r'\textbf{robustness and critique}: \aiprompt{Act as a hostile referee: list every specification choice that could flip the complete pass-through test.}', r'\textbf{robustețe și critică}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră toate alegerile de specificare care ar putea inversa testul transmiterii complete.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The deterministic case of the critical values matches the estimated model (a frequent AI error: case-3 values for a case-2 model)', 'Cazul determinist al valorilor critice corespunde modelului estimat (o eroare AI frecventă: valori ale cazului 3 pentru un model al cazului 2)'),
    T(r'The degrees of freedom of every LR test on $\beta$ and $\alpha$ are counted by hand', r'Gradele de libertate ale fiecărui test LR asupra lui $\beta$ și $\alpha$ se numără de mînă'),
    T('Lag length, case, sample and the treatment of 2008--2009 are fixed before the results; all variants are reported', 'Numărul de laguri, cazul, eșantionul și tratarea perioadei 2008--2009 sînt fixate înaintea rezultatelor; toate variantele sînt raportate'),
    T('A claim of ``complete pass-through\'\' is checked against the confidence set of $\\theta$, not against one $p$-value', 'O afirmație de „transmitere completă” se verifică pe mulțimea de încredere a lui $\\theta$, nu pe un singur p-value')), 'small')

chart(T('Mini-case: the estimate is robust, the verdict is not', 'Mini studiu de caz: estimația este robustă, verdictul nu'), 'ats_ch4_ai_case', 'ATS_ch4_ai_robustness', [
    T(r'Long-run pass-through to the lending rate in the rank-2 VECM: lags $p = 2, \dots, 6$, cases 2 and 3, samples ending in 2019 and in 2026; filled markers: $\theta = 1$ rejected at 5\%', r'Transmiterea pe termen lung către dobînda la credite în VECM de rang 2: laguri $p = 2, \dots, 6$, cazurile 2 și 3, eșantioane care se încheie în 2019 și în 2026; marcaje pline: $\theta = 1$ respins la 5\%'),
    T(r'All @{ai.n} estimates lie between @{ai.min} and @{ai.max}, yet complete pass-through is rejected in @{ai.nrej} of them: an AI summary that reports one $p$-value ``with confidence\'\' is wrong', r'Toate cele @{ai.n} de estimații se află între @{ai.min} și @{ai.max}, dar transmiterea completă este respinsă în @{ai.nrej} dintre ele: un rezumat AI care raportează un singur p-value „cu încredere” greșește')],
    h='0.5\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Interest-rate pass-through in Central and Eastern Europe}: replicate first, then extend', r'\textbf{Transmiterea dobînzilor în Europa Centrală și de Est}: întîi replicare, apoi extindere'),
     [T(r'replicate: the Romanian rank-2 VECM of this lecture (eigenvalues @{pt.lam0}, @{pt.lam1}, @{pt.lam2}) and the ARDL pass-through @{ar.lend.theta}', r'replicați: VECM-ul de rang 2 pentru România din acest curs (valorile proprii @{pt.lam0}, @{pt.lam1}, @{pt.lam2}) și transmiterea ARDL @{ar.lend.theta}'),
      T(r'extend: Romania, Hungary, Czechia and Poland; broken constants \refJMN\ in 2008 and 2022; wild-bootstrap rank tests; PMG across countries with a Hausman test; NARDL for asymmetric pass-through', r'extindeți: România, Ungaria, Cehia și Polonia; constante cu rupturi \refJMN\ în 2008 și 2022; teste de rang cu bootstrap wild; PMG între țări cu test Hausman; NARDL pentru transmitere asimetrică'),
      T('pre-register: variables, sample, case, lag rule, rank procedure, the restrictions to test and the multiple-testing correction', 'preînregistrați: variabilele, eșantionul, cazul, regula pentru numărul de laguri, procedura pentru rang, restricțiile de testat și corecția pentru testare multiplă')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Johansen = reduced-rank regression; the rank test is non-standard, depends on the case and over-rejects in small samples', 'Johansen = regresie de rang redus; testul de rang este nestandard, depinde de caz și respinge prea des în eșantioane mici'),
    T(r'Given the rank, restrictions on $\beta$ (economics) and $\alpha$ (weak exogeneity) are ordinary $\chi^2$ tests', r'Pentru un rang dat, restricțiile asupra lui $\beta$ (economie) și $\alpha$ (exogenitate slabă) sînt teste $\chi^2$ obișnuite'),
    T('Cointegration supplies long-run zeros for structural analysis: permanent and transitory shocks', 'Cointegrarea furnizează zerouri de termen lung pentru analiza structurală: șocuri permanente și tranzitorii'),
    T('ARDL is a conditional VECM: valid under weak exogeneity and a single relation, with small-sample bounds', 'ARDL este un VECM condiționat: valabil sub exogenitate slabă și o singură relație, cu limite pentru eșantioane mici'),
    T('Panels add power but bring heterogeneity and cross-section dependence: CD first, then CIPS, MG/PMG and CCE', 'Panelurile adaugă putere, dar aduc eterogenitate și dependență între unități: întîi CD, apoi CIPS, MG/PMG și CCE')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T(r'Why does one eigen-decomposition give the ML estimator of $\beta$ for every rank?', r'De ce dă o singură descompunere în valori proprii estimatorul ML al lui $\beta$ pentru orice rang?'),
        T('Which deterministic case fits two interest rates without drift?', 'Ce caz determinist se potrivește pentru două dobînzi fără drift?'),
        T(r'How many degrees of freedom has the test of a known $\beta$ with $n_1 = 3$, $r = 2$?', r'Cîte grade de libertate are testul unui $\beta$ cunoscut cu $n_1 = 3$, $r = 2$?'),
        T('What does weak exogeneity of ROBOR allow you to do?', 'Ce vă permite exogenitatea slabă a lui ROBOR?'),
        T('Why can IPS reject a unit root that CIPS does not reject?', 'De ce poate IPS să respingă o rădăcină unitară pe care CIPS nu o respinge?'))),
    block(T('Next: Chapter 5', 'Urmează: Capitolul 5'), items(
        T('Bayesian VAR, factor models and nowcasting', 'Modele VAR bayesiene, modele factoriale și nowcasting'),
        T('Shrinkage handles the parameter problem we met in small samples; factors generalise the cross-section averages of CCE', 'Shrinkage rezolvă problema numărului de parametri întîlnită în eșantioanele mici; factorii generalizează mediile pe secțiune din CCE'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: from the likelihood to the eigenvalues', 'Anexă: de la verosimilitate la valorile proprii'), items(
    T(r'For fixed $\beta$: $|\hat\Omega(\beta)| = |S_{00} - S_{01}\beta(\beta\'S_{11}\beta)^{-1}\beta\'S_{10}|$; apply the partitioned determinant to $\begin{pmatrix}S_{00} & S_{01}\beta\\ \beta\'S_{10} & \beta\'S_{11}\beta\end{pmatrix}$ in both orders',
      r'Pentru $\beta$ fixat: $|\hat\Omega(\beta)| = |S_{00} - S_{01}\beta(\beta\'S_{11}\beta)^{-1}\beta\'S_{10}|$; aplicăm determinantul partiționat matricei $\begin{pmatrix}S_{00} & S_{01}\beta\\ \beta\'S_{10} & \beta\'S_{11}\beta\end{pmatrix}$ în ambele ordini'),
    T(r'$|\hat\Omega(\beta)|\,|\beta\'S_{11}\beta| = |S_{00}|\,|\beta\'(S_{11} - S_{10}S_{00}^{-1}S_{01})\beta|$, which gives the ratio on the slide',
      r'$|\hat\Omega(\beta)|\,|\beta\'S_{11}\beta| = |S_{00}|\,|\beta\'(S_{11} - S_{10}S_{00}^{-1}S_{01})\beta|$, de unde raportul de pe slide'),
    T(r'Write $\beta = S_{11}^{-1/2}\eta$: the ratio becomes $|\eta\'(I - M)\eta|/|\eta\'\eta|$ with $M = S_{11}^{-1/2}S_{10}S_{00}^{-1}S_{01}S_{11}^{-1/2}$; it is minimised by the eigenvectors of $M$ with the $r$ largest eigenvalues',
      r'Scriem $\beta = S_{11}^{-1/2}\eta$: raportul devine $|\eta\'(I - M)\eta|/|\eta\'\eta|$ cu $M = S_{11}^{-1/2}S_{10}S_{00}^{-1}S_{01}S_{11}^{-1/2}$; minimul se obține cu vectorii proprii ai lui $M$ pentru cele mai mari $r$ valori proprii'),
    T(r'The minimum is $\prod_{i\le r}(1 - \lambda_i)$; nested ranks share eigenvectors, so the LR statistics are sums of $-T\ln(1 - \hat\lambda_i)$',
      r'Minimul este $\prod_{i\le r}(1 - \lambda_i)$; rangurile imbricate au aceiași vectori proprii, deci statisticile LR sînt sume de termeni $-T\ln(1 - \hat\lambda_i)$')), 'small')

D.frame(T('Appendix: deriving the long-run impact matrix $C$', 'Anexă: derivarea matricei impactului pe termen lung $C$'), items(
    T(r'Multiply the VECM by $\alpha_\perp\'$: $\alpha_\perp\'\Delta y_t = \alpha_\perp\'\sum_i\Gamma_i\Delta y_{t-i} + \alpha_\perp\'\varepsilon_t$; summing gives $\alpha_\perp\'\Gamma y_t \approx \alpha_\perp\'\sum_{s\le t}\varepsilon_s$ up to stationary terms',
      r'Înmulțim VECM cu $\alpha_\perp\'$: $\alpha_\perp\'\Delta y_t = \alpha_\perp\'\sum_i\Gamma_i\Delta y_{t-i} + \alpha_\perp\'\varepsilon_t$; prin însumare $\alpha_\perp\'\Gamma y_t \approx \alpha_\perp\'\sum_{s\le t}\varepsilon_s$ pînă la termeni staționari'),
    T(r'Decompose $y_t = \beta(\beta\'\beta)^{-1}\beta\'y_t + \beta_\perp(\beta_\perp\'\beta_\perp)^{-1}\beta_\perp\'y_t$; the first part is stationary',
      r'Descompunem $y_t = \beta(\beta\'\beta)^{-1}\beta\'y_t + \beta_\perp(\beta_\perp\'\beta_\perp)^{-1}\beta_\perp\'y_t$; prima parte este staționară'),
    T(r'Hence $\alpha_\perp\'\Gamma\beta_\perp\,(\beta_\perp\'\beta_\perp)^{-1}\beta_\perp\'y_t \approx \alpha_\perp\'\sum_s\varepsilon_s$; invert $\alpha_\perp\'\Gamma\beta_\perp$ (the I(1) condition) and premultiply by $\beta_\perp$',
      r'Deci $\alpha_\perp\'\Gamma\beta_\perp\,(\beta_\perp\'\beta_\perp)^{-1}\beta_\perp\'y_t \approx \alpha_\perp\'\sum_s\varepsilon_s$; inversăm $\alpha_\perp\'\Gamma\beta_\perp$ (condiția I(1)) și înmulțim la stînga cu $\beta_\perp$'),
    T(r'Result: the non-stationary part of $y_t$ is $\beta_\perp(\alpha_\perp\'\Gamma\beta_\perp)^{-1}\alpha_\perp\'\sum_s\varepsilon_s = C\sum_s\varepsilon_s$',
      r'Rezultatul: partea nestaționară a lui $y_t$ este $\beta_\perp(\alpha_\perp\'\Gamma\beta_\perp)^{-1}\alpha_\perp\'\sum_s\varepsilon_s = C\sum_s\varepsilon_s$')), 'small')

D.frame(T('Appendix: the PMG likelihood', 'Anexă: verosimilitatea PMG'), items(
    T(r'$\ell(\theta, \phi, \sigma^2) = -\sum_{i=1}^N\frac{T_i}{2}\ln(2\pi\sigma_i^2) - \sum_{i=1}^N\frac{1}{2\sigma_i^2}(\Delta y_i - \phi_i\xi_i(\theta))\'H_i(\Delta y_i - \phi_i\xi_i(\theta))$',
      r'$\ell(\theta, \phi, \sigma^2) = -\sum_{i=1}^N\frac{T_i}{2}\ln(2\pi\sigma_i^2) - \sum_{i=1}^N\frac{1}{2\sigma_i^2}(\Delta y_i - \phi_i\xi_i(\theta))\'H_i(\Delta y_i - \phi_i\xi_i(\theta))$'),
    (T('Notation', 'Notațiile'),
     [T(r'$\Delta y_i$, $y_{i,-1}$ ($T_i\times 1$), $X_{i,-1}$ ($T_i\times k$): the changes, the lagged levels of $y$ and of $x$ for country $i$', r'$\Delta y_i$, $y_{i,-1}$ ($T_i\times 1$), $X_{i,-1}$ ($T_i\times k$): modificările, nivelurile cu lag ale lui $y$ și ale lui $x$ pentru țara $i$'),
      T(r'$\xi_i(\theta) = y_{i,-1} - X_{i,-1}\theta$: the equilibrium error of country $i$', r'$\xi_i(\theta) = y_{i,-1} - X_{i,-1}\theta$: eroarea de echilibru a țării $i$'),
      T(r'$H_i = I - W_i(W_i\'W_i)^{-1}W_i\'$; $W_i$: the country\'s short-run regressors and intercept, which $H_i$ projects out', r'$H_i = I - W_i(W_i\'W_i)^{-1}W_i\'$; $W_i$: regresorii pe termen scurt și termenul liber ai țării, eliminați prin $H_i$')]),
    T(r'Given $\theta$, $\phi_i$ and $\sigma_i^2$ are country OLS; the concentrated likelihood $-\sum_i\frac{T_i}{2}\ln\hat\sigma_i^2(\theta)$ is maximised over $\theta$ (back-substitution or Newton)',
      r'Pentru $\theta$ dat, $\phi_i$ și $\sigma_i^2$ sînt OLS pe țări; verosimilitatea concentrată $-\sum_i\frac{T_i}{2}\ln\hat\sigma_i^2(\theta)$ se maximizează după $\theta$ (substituție înapoi sau Newton)'),
    T(r'$\hat\theta_{PMG}$ is consistent and asymptotically normal if $\phi_i < 0$ for all $i$ and the long run is homogeneous; the I(0)/I(1) status of $x$ does not matter, as in ARDL',
      r'$\hat\theta_{PMG}$ este consistent și asimptotic normal dacă $\phi_i < 0$ pentru orice $i$ și termenul lung este omogen; statutul I(0)/I(1) al lui $x$ nu contează, ca în ARDL')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
