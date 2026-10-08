r"""
build_chapter6.py -- Capitolul 6 (Modele în spațiul stărilor și filtrare bayesiană), EN + RO
==============================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_06/ch6_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice și a constantelor publicate, cu sursa citată). TSA, Capitolul 10
a predat modelul liniar gaussian, filtrul Kalman de mînă, netezirea, local level/trend, output gap-ul UC și
modelul Markov switching de bază; aici construim inițializarea difuză exactă, verosimilitatea, eșantionarea bayesiană
a stărilor, volatilitatea stochastică, filtrele neliniare și de particule, TVP, DFM și descompunerile trend--ciclu.
Ieșire:
  EN/Courses/chapter6_state_space_models_bayesian_filtering.tex
  RO/Cursuri/capitol6_modele_spatiul_starilor_filtrare_bayesiana.tex
Rulare:
  python3 Quantlets/Ch_06/generate_all_charts.py
  python3 latex/build_chapter6.py && python3 latex/ats_build.py compile 6
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch6_common import REFS, QLURL, T, bib, finalize, load, minus_fix, month, pv, quarter   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(6, 'lecture', refs=REFS)
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
    'kalman': ('ch6_kalman_2007.jpg', C + 'ETH-BIB-Kalman,_Rudolf_E._(1930-2016)-HK_04-01925.jpg',
               FOTO + ': ETH-Bibliothek Zürich, Bildarchiv (2007); CC BY-SA 4.0; Wikimedia Commons'),
    'bayes': ('ch6_bayes.png', C + 'Thomas_Bayes.gif', T('Portrait: unknown author; public domain; Wikimedia Commons',
                                                          'Portret: autor necunoscut; domeniu public; Wikimedia Commons')),
    'shephard': ('ch6_shephard_2004.jpg', C + 'Shephard,_Neil_(1964).jpeg',
                 FOTO + ': Renate Schmid (2004), MFO; CC BY-SA 2.0 de; Wikimedia Commons'),
    'ulam': ('ch6_ulam_fermiac.jpg', C + 'STAN_ULAM_HOLDING_THE_FERMIAC.jpg',
             FOTO + ': Los Alamos National Laboratory (LA-UR-00-2532); public domain; Wikimedia Commons'),
    'sargent': ('ch6_sargent_2011.jpg', C + 'Thomas_J._Sargent_close-up_(cropped).jpg',
                FOTO + ': Holger Motzkau (2011); CC BY-SA 3.0; Wikimedia Commons'),
    'bnr': ('ch0_bnr_palace_2015.jpg', C + 'Bucharest_-_BNR_Palace_(19644434340).jpg',
            FOTO + ': Ștefan Jurcă (2015); CC BY 2.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


TB = '>{\\raggedright\\arraybackslash}'


def q(s):
    return quarter(s)


# =============================================================================
# CIFRE
# =============================================================================
ll = N['ll']
V.raw('ll.T', str(ll['T']))
V.raw('ll.first', q(ll['first']))
V.raw('ll.last', q(ll['last']))
P('ll.s2e', ll['s2eps'], 3)
P('ll.s2h', ll['s2eta'], 3)
P('ll.q', ll['q'], 3)
P('ll.ll', ll['ll'], 2)
P('ll.smll', ll['sm_ll'], 2)
P('ll.sms2e', ll['sm_s2eps'], 3)
P('ll.sms2h', ll['sm_s2eta'], 3)
P('ll.gap', -ll['ll_gap'], 3)
P('ll.K', ll['steady_K'], 3)
P('ll.Kp', 100 * ll['steady_K'], 0)
P('ll.lev', ll['last_level'], 2)
P('ll.levsd', ll['last_sd'], 2)
P('ll.se0', ll['se_log'][0], 3)
P('ll.se1', ll['se_log'][1], 3)
df = N['diffuse']
P('df.exact', df['exact'], 2)
kap = df['kap']
i7, i14, i16 = kap.index(1e7), kap.index(1e14), kap.index(1e16)
P('df.raw7', df['raw'][i7], 2)
P('df.raw14', df['raw'][i14], 2)
P('df.adj7', df['adj'][i7], 2)
P('df.ea8', df['ea'][kap.index(1e8)], 7)
P('df.ev8', df['ev'][kap.index(1e8)], 2)
P('df.ev16', df['ev'][i16], 0)
V.raw('df.ev16e', str(int(round(__import__('math').log10(df['ev'][i16])))))
P('df.ev4', df['ev'][kap.index(1e4)], 6)
P('df.ea4', df['ea'][kap.index(1e4)], 3)
V.raw('df.Tg', str(df['T_gdp']))
pu = N['pileup']
for k_, nm in (('0.0', '0'), ('0.01', '1'), ('0.05', '5')):
    P(f'pu.z{nm}', 100 * pu[k_]['zero'], 0)
    P(f'pu.m{nm}', pu[k_]['median'], 4)
V.int('pu.reps', pu['reps'])
V.raw('pu.n', str(pu['n']))
sm = N['simsm']
for k_ in ('ck', 'dk', 'pr'):
    P(f'sm.{k_}.err', sm['res'][k_]['mean_err'], 3)
    P(f'sm.{k_}.lo', sm['res'][k_]['sd_ratio_min'], 2)
    P(f'sm.{k_}.hi', sm['res'][k_]['sd_ratio_max'], 2)
    P(f'sm.{k_}.t4000', sm['ms'][k_][-1], 1 if k_ != 'pr' else 2)
V.int('sm.draws', sm['draws'])
gb = N['gibbs']
P('gb.qmed', gb['post_q_med'], 2)
P('gb.qlo', gb['q_lo'], 2)
P('gb.qhi', gb['q_hi'], 2)
P('gb.qratio', gb['q_hi'] / gb['q_lo'], 1)
P('gb.mlq', gb['ml_q'], 2)
P('gb.ie0', gb['ineff'][0], 1)
P('gb.ie1', gb['ineff'][1], 1)
P('gb.m0', gb['post_mean'][0], 3)
P('gb.m1', gb['post_mean'][1], 3)
V.int('gb.draws', gb['draws'])
ks = N['ksc']
P('ks.mean', ks['mean_mix'], 4)
P('ks.var', ks['var_mix'], 3)
P('ks.errm', ks['maxerr_mix'], 3)
P('ks.errg', ks['maxerr_gauss'], 3)
sv = N['sv']
for nm in ('sp500', 'bet'):
    s_ = sv[nm]
    V.raw(f'sv.{nm}.T', str(s_['T']))
    for j, par in enumerate(('mu', 'phi', 'sig')):
        P(f'sv.{nm}.{par}', s_['mean'][j], 3)
        P(f'sv.{nm}.{par}.lo', s_['lo'][j], 3)
        P(f'sv.{nm}.{par}.hi', s_['hi'][j], 3)
        P(f'sv.{nm}.{par}.ie', s_['ineff'][j], 0)
    P(f'sv.{nm}.a', s_['garch']['alpha'], 3)
    P(f'sv.{nm}.b', s_['garch']['beta'], 3)
    P(f'sv.{nm}.ab', s_['garch']['alpha'] + s_['garch']['beta'], 3)
    P(f'sv.{nm}.corr', s_['corr_vol'], 2)
    P(f'sv.{nm}.kurt', s_['kurt'], 1)
V.int('sv.draws', sv['draws'])
pf = N['pf']
P('pf.llsv', pf['ll_sv'], 1)
P('pf.llga', pf['ll_garch'], 1)
P('pf.dll', pf['ll_sv'] - pf['ll_garch'], 1)
for k_ in ('100', '500', '2000'):
    P(f'pf.sd{k_}', pf['sd'][k_], 2)
P('pf.essmin', pf['ess_min'], 0)
P('pf.essmed', pf['ess_med'], 0)
P('pf.corr', pf['corr_pf_garch'], 2)
V.raw('pf.reps', str(pf['reps']))
pm = N['pmmh']
V.raw('pm.n', str(pm['n']))
V.raw('pm.N', str(pm['N']))
V.int('pm.iter', pm['n_iter'])
P('pm.acc', 100 * pm['acc'], 0)
P('pm.sdll', pm['sd_ll'], 2)
for j, par in enumerate(('mu', 'phi', 'sig')):
    P(f'pm.g.{par}', pm['gibbs_mean'][j], 3)
    P(f'pm.p.{par}', pm['pmmh_mean'][j], 3)
    P(f'pm.gs.{par}', pm['gibbs_sd'][j], 3)
    P(f'pm.ps.{par}', pm['pmmh_sd'][j], 3)
    P(f'pm.ie.{par}', pm['ineff_pmmh'][j], 0)
P('pm.min', pm['secs'] / 60, 1)
uk = N['ukf']
for k_ in ('ex_m', 'lin_m', 'ut_m', 'ex_sd', 'lin_sd', 'ut_sd'):
    P(f'uk.{k_}', uk[k_], 3)
pc = N['pfc']
for kind, a in (('bootstrap', 'b'), ('auxiliary', 'a')):
    for k_ in ('50', '200', '1000'):
        P(f'pc.{a}{k_}.m', pc[kind][k_]['mean'], 2)
        P(f'pc.{a}{k_}.s', pc[kind][k_]['sd'], 2)
V.raw('pc.reps', str(pc['reps']))
tv = N['tvp']
V.raw('tv.T', str(tv['T']))
V.raw('tv.first', q(tv['first']))
V.raw('tv.last', q(tv['last']))
P('tv.s2c', tv['par'][0], 3)
P('tv.s2b', tv['par'][1], 4)
P('tv.s2e', tv['par'][2], 2)
P('tv.ll', tv['ll'], 2)
P('tv.smll', tv['sm_ll'], 2)
P('tv.LR', tv['LR'], 3)
V.raw('tv.pboot', pv(tv['pboot']))
V.raw('tv.pmix', pv(tv['pmix']))
V.raw('tv.B', str(tv['B']))
P('tv.q95', tv['lr_q95'], 2)
P('tv.zero', 100 * tv['zero_share'], 0)
for k_, nm in (('2008-07-01', '08'), ('2015-07-01', '15'), ('2022-10-01', '22')):
    P(f'tv.b{nm}', tv['b_at'][k_][0], 2)
    P(f'tv.sb{nm}', tv['b_at'][k_][1], 2)
P('tv.blast', tv['b_last'][0], 2)
P('tv.sblast', tv['b_last'][1], 2)
fm = N['dfm']
V.raw('fm.first', month(fm['first']))
V.raw('fm.last', month(fm['last']))
V.raw('fm.full', month(fm['last_full']))
V.raw('fm.T', str(fm['T']))
for j in range(4):
    P(f'fm.l{j}', fm['lam'][j], 2)
P('fm.a', fm['a'], 2)
P('fm.sdfull', fm['sd_full'], 2)
P('fm.sdlast', fm['sd_last'], 2)
mz = N['mnz']
V.raw('mz.T', str(mz['T']))
for nm, src in (('u0', mz['u0']['par']), ('ur', mz['ur']['par'])):
    for j, par in enumerate(('mu', 'p1', 'p2', 'se', 'sc', 'rho')):
        P(f'mz.{nm}.{par}', src[j], 3 if par != 'rho' else 3)
    P(f'mz.{nm}.ll', mz[nm]['loglik'], 2)
P('mz.LR', mz['LR'], 2)
V.raw('mz.p', pv(mz['p']))
P('mz.corr', mz['corr_ur_bn'], 3)
P('mz.sd0', mz['sd_c0'], 2)
P('mz.sd1', mz['sd_c1'], 2)
P('mz.sdbn', mz['sd_bn'], 2)
P('mz.sdham', mz['sd_ham'], 2)
P('mz.bn1', mz['bnp']['ar'][0], 3)
P('mz.bn2', mz['bnp']['ar'][1], 3)
rg = N['rogap']
V.raw('rg.T', str(rg['T']))
V.raw('rg.last', q(rg['last']))
for j, par in enumerate(('mu', 'p1', 'p2', 'se', 'sc')):
    P(f'rg.u0.{par}', rg['u0']['par'][j], 3)
P('rg.ur.rho', rg['ur']['par'][5], 2)
P('rg.LR', rg['LR'], 2)
P('rg.st.z', rg['st']['par'][0], 4)
P('rg.st.e', rg['st']['par'][1], 2)
P('rg.st.p1', rg['st']['par'][2], 2)
P('rg.st.p2', rg['st']['par'][3], 2)
for k_, nm in (('2008-07-01', '08'), ('2010-07-01', '10'), ('2019-10-01', '19')):
    P(f'rg.g{nm}', rg['gap_at'][k_][0], 1)
    P(f'rg.sd{nm}', rg['gap_at'][k_][1], 1)
    P(f'rg.f{nm}', rg['gap_at'][k_][2], 1)
P('rg.lasts', rg['last_s'], 1)
P('rg.lastsd', rg['last_sd'], 1)
P('rg.lastham', rg['last_ham'], 1)
P('rg.sdgap', rg['sd_gap'], 1)
P('rg.sduc0', rg['sd_uc0'], 2)
P('rg.sdham', rg['sd_ham'], 1)
P('rg.corr', rg['corr_gap_ham'], 2)
P('rg.rev', rg['rev_sd'], 1)
us = N['ucsv_us']
V.raw('us.T', str(us['T']))
V.raw('us.last', q(us['last']))
for k_, nm in (('1975-01-01', '75'), ('1995-01-01', '95'), ('2019-10-01', '19'), ('2022-04-01', '22')):
    P(f'us.t{nm}', us['tau_at'][k_][1], 1)
    P(f'us.tl{nm}', us['tau_at'][k_][0], 1)
    P(f'us.th{nm}', us['tau_at'][k_][2], 1)
    P(f'us.s1{nm}', us['s1_at'][k_], 2)
    P(f'us.s2{nm}', us['s2_at'][k_], 2)
    P(f'us.theta{nm}', us['theta_at'][k_], 2)
P('us.tlast', us['tau_last'][1], 1)
P('us.tllast', us['tau_last'][0], 1)
P('us.thlast', us['tau_last'][2], 1)
P('us.pi4', us['pi_4q'], 1)
ro = N['ucsv_ro']
V.raw('ro.T', str(ro['T']))
V.raw('ro.last', q(ro['last']))
for k_, nm in (('2005-07-01', '05'), ('2015-07-01', '15'), ('2019-10-01', '19'), ('2023-01-01', '23')):
    P(f'ro.t{nm}', ro['tau_at'][k_][1], 1)
P('ro.tlast', ro['tau_last'][1], 1)
P('ro.tllast', ro['tau_last'][0], 1)
P('ro.thlast', ro['tau_last'][2], 1)
P('ro.pin', 100 * ro['post_in_band'], 0)
ai = N['ai']
for g_, nm in (('0.05', '05'), ('0.1', '1'), ('0.2', '2'), ('0.4', '4')):
    P(f'ai.pk{nm}', ai[g_]['peak'], 1)
    P(f'ai.last{nm}', ai[g_]['last'], 1)
P('ai.pi', ai['pi_peak'], 1)
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: how do we learn about quantities we never observe (trend inflation, the output gap, volatility, time-varying coefficients) and how much should we trust what we learn?',
       r'\textbf{Întrebarea}: cum învățăm despre mărimi pe care nu le observăm niciodată (inflația de trend, output gap-ul, volatilitatea, coeficienți variabili în timp) și cît ne putem baza pe ce aflăm?'),
     [T('one framework: a state equation for the hidden quantity, a measurement equation for the data, and a filter that updates beliefs as data arrive',
        'un singur cadru: o ecuație de stare pentru mărimea ascunsă, o ecuație de măsurare pentru date și un filtru care actualizează convingerile pe măsură ce sosesc datele')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('the general linear Gaussian model, exact diffuse initialisation, the exact likelihood and inference at the boundary',
        'modelul liniar gaussian general, inițializarea difuză exactă, verosimilitatea exactă și inferența la frontieră'),
      T('Bayesian state space: simulation smoothers and Gibbs sampling; stochastic volatility',
        'spațiul stărilor bayesian: simulation smoothers și eșantionare Gibbs; volatilitatea stochastică'),
      T('nonlinear filters: extended and unscented Kalman filters, particle filters, particle MCMC',
        'filtre neliniare: filtrul Kalman extins și unscented, filtre de particule, particle MCMC'),
      T('time-varying parameters, dynamic factors, trend--cycle decompositions and trend inflation with stochastic volatility',
        'parametri variabili în timp, factori dinamici, descompuneri trend--ciclu și inflația de trend cu volatilitate stochastică')]),
    T('We build on TSA, Chapter 10 (state space form, Kalman filter by hand, smoothing, local level and trend, the UC output gap, Markov switching basics); Seminar 6 comes before this lecture',
      'Pornim de la TSA, Capitolul 10 (forma în spațiul stărilor, filtrul Kalman de mînă, netezirea, modelele local level și local trend, output gap-ul UC, bazele modelelor Markov switching); Seminarul 6 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Derive the Kalman filter and smoother for the general linear Gaussian model, with exact diffuse initialisation, and write them in \\texttt{numpy}',
      'Derivați filtrul și netezitorul Kalman pentru modelul liniar gaussian general, cu inițializare difuză exactă, și scrieți-le în \\texttt{numpy}'),
    T('Maximise the exact likelihood and judge inference on variances that may sit on the boundary (pile-up, bootstrap LR tests)',
      'Maximizați verosimilitatea exactă și evaluați inferența asupra varianțelor care pot ajunge pe frontieră (pile-up, teste LR bootstrap)'),
    T('Sample states with the Carter--Kohn, Durbin--Koopman and precision samplers inside a Gibbs sampler; estimate stochastic volatility by the KSC mixture',
      'Eșantionați stările cu metodele Carter--Kohn, Durbin--Koopman și cu eșantionarea pe baza matricei de precizie, într-un eșantionator Gibbs; estimați volatilitatea stochastică prin mixtura KSC'),
    T('Run extended, unscented and particle filters; use the particle likelihood in PMMH and choose the number of particles',
      'Aplicați filtrele Kalman extins, unscented și de particule; folosiți verosimilitatea din filtrul de particule în PMMH și alegeți numărul de particule'),
    T('Estimate TVP regressions, UC models with correlated shocks and UC-SV trend inflation, and report how fragile the latent estimates are',
      'Estimați regresii TVP, modele UC cu șocuri corelate și inflația de trend UC-SV și raportați cît de fragile sînt estimațiile componentelor latente')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Backbone: \refDK, Ch.~2--9 and 11--14; \refHar; \refKN; \refHam, Ch.~13; \refCP',
       r'Bibliografia de bază: \refDK, cap.~2--9 și 11--14; \refHar; \refKN; \refHam, cap.~13; \refCP'),
     [T(r'original papers: \refKal, \refKoo, \refCK, \refDKa, \refKSC, \refGSS, \refPS, \refADH, \refPri, \refMNZ, \refSWb',
        r'lucrările originale: \refKal, \refKoo, \refCK, \refDKa, \refKSC, \refGSS, \refPS, \refADH, \refPri, \refMNZ, \refSWb')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_06}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_06}'),
     [T(r'Kalman filter and smoother with exact diffuse initialisation, simulation smoothers, KSC Gibbs sampler, bootstrap and auxiliary particle filters, PMMH and UC-SV written out in \texttt{numpy}; checked against \texttt{statsmodels}',
        r'filtrul și netezitorul Kalman cu inițializare difuză exactă, simulation smoothers, eșantionatorul Gibbs KSC, filtrele de particule bootstrap și auxiliar, PMMH și UC-SV scrise explicit în \texttt{numpy}; verificate cu \texttt{statsmodels}')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter6_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter6_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{5.0cm}' + TB + 'p{4.4cm}' + TB + 'p{2.5cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizare}'),
    [T('US GDP price deflator, real GDP (quarterly)', 'deflatorul PIB și PIB-ul real al SUA (trimestrial)') + ' & FRED (GDPDEF, GDPC1) & ' + T('likelihood, MNZ, UC-SV', 'verosimilitate, MNZ, UC-SV'),
     T('S\\&P 500 and BET, daily closes', 'S\\&P 500 și BET, închideri zilnice') + ' & EODHD & ' + T('stochastic volatility', 'volatilitate stochastică'),
     T('HICP of Romania and of the euro area (monthly index, 2025 = 100)', 'IAPC pentru România și zona euro (indice lunar, 2025 = 100)') + ' & Eurostat prc\\_hicp\\_minr & TVP, UC-SV',
     T('Romanian real GDP, seasonally and calendar adjusted', 'PIB-ul real al României, ajustat sezonier și cu numărul de zile lucrătoare') + ' & Eurostat namq\\_10\\_gdp & ' + T('output gap', 'output gap-ul'),
     T('US industrial production, payrolls, real income less transfers, real sales (monthly)', 'producția industrială, numărul de salariați, venitul real fără transferuri, vînzările reale ale SUA (lunar)') + ' & FRED (INDPRO, PAYEMS, W875RX1, CMRMTSPL) & DFM'],
    size='scriptsize') + items(
    T('All sources are public and need no account or key; quarterly series to 2026Q2, monthly series to August or September 2026, daily data to 18 September 2026',
      'Toate sursele sînt publice și nu cer cont sau cheie; seriile trimestriale pînă în T2 2026, cele lunare pînă în august sau septembrie 2026, datele zilnice pînă la 18 septembrie 2026'),
    T('HICP: harmonised index of consumer prices; DFM: dynamic factor model', 'IAPC (HICP): indicele armonizat al prețurilor de consum; DFM: model cu factori dinamici')), 'footnotesize')

D.frame(T('From Apollo navigation to trend inflation', 'De la navigația Apollo la inflația de trend'), two(
    ph('kalman', T('Rudolf E. Kálmán, 2007', 'Rudolf E. Kálmán, 2007'), h='0.36\\textheight'),
    items(T(r'1960: \refKal\ gives the recursive linear filter; it guides the Apollo missions within a decade', r'1960: \refKal\ dă filtrul liniar recursiv; în mai puțin de un deceniu, el ghidează misiunile Apollo'),
          T(r'1982--1997: EM for state space models \refSS; structural time series \refHar; exact diffuse filtering \refKoo', r'1982--1997: algoritmul EM pentru modele în spațiul stărilor \refSS; serii de timp structurale \refHar; filtrarea difuză exactă \refKoo'),
          T(r'1993--1999: particle filters \refGSS, \refPS; Gibbs sampling of states \refCK, \refFS; stochastic volatility \refKSC', r'1993--1999: filtre de particule \refGSS, \refPS; eșantionarea Gibbs a stărilor \refCK, \refFS; volatilitate stochastică \refKSC'),
          T(r'2002--2010: the simulation smoother \refDKa; TVP-VAR with stochastic volatility \refPri, \refCSb; particle MCMC \refADH', r'2002--2010: simulation smoother-ul \refDKa; TVP-VAR cu volatilitate stochastică \refPri, \refCSb; particle MCMC \refADH'),
          T(r'Today: central banks track trend inflation and the output gap with these tools \refSWb, \refMNZ', r'Astăzi: băncile centrale urmăresc inflația de trend și output gap-ul cu aceste instrumente \refSWb, \refMNZ')), '0.36', '0.62'), 'footnotesize')

# =============================================================================
# 1. MODELUL GENERAL
# =============================================================================
D.section('The general linear Gaussian model', 'Modelul liniar gaussian general')

D.frame(T('From TSA to this chapter', 'De la TSA la acest capitol'), items(
    (T(r'Known (TSA, Chapter 10): the state space form, the Kalman filter for the local level by hand, smoothing, ML by the prediction error decomposition, the HP filter as a smoother, Hamilton (2018), Markov switching',
       r'Cunoscut (TSA, Capitolul 10): forma în spațiul stărilor, filtrul Kalman pentru modelul local level de mînă, netezirea, verosimilitatea maximă prin descompunerea erorilor de predicție, filtrul HP ca netezitor, Hamilton (2018), modelele Markov switching'),
     []),
    (T('New here', 'Nou aici'),
     [T('the filter and smoother for any linear Gaussian model, with nonstationary states initialised exactly (not with a large variance)',
        'filtrul și netezitorul pentru orice model liniar gaussian, cu stări nestaționare inițializate exact (nu cu o varianță mare)'),
      T('inference when a variance may be zero; Bayesian sampling of whole state paths', 'inferența cînd o varianță poate fi zero; eșantionarea bayesiană a traiectoriilor întregi ale stărilor'),
      T('nonlinear and non-Gaussian models: stochastic volatility, particle filters, particle MCMC', 'modele neliniare și negaussiene: volatilitate stochastică, filtre de particule, particle MCMC'),
      T('applications at research level: MNZ, UC-SV, TVP regressions, the ragged edge of a DFM', 'aplicații la nivel de cercetare: MNZ, UC-SV, regresii TVP, ragged edge într-un DFM')]),
    T('Markov switching in depth: Chapter 7; nowcasting with factors: Chapter 5', 'Modelele Markov switching în detaliu: Capitolul 7; nowcasting cu factori: Capitolul 5')), 'small')

D.frame(T('The general state space form (1/2)', 'Forma generală în spațiul stărilor (1/2)'), items(
    T(r'Two equations: the data are a noisy linear function of an unobserved state, and the state follows a first-order linear dynamic \[ y_t = Z_t\alpha_t + \varepsilon_t, \qquad \alpha_{t+1} = c_t + T_t\alpha_t + R_t\eta_t, \qquad t = 1, \dots, n \]',
      r'Două ecuații: datele sînt o funcție liniară cu zgomot a unei stări neobservate, iar starea urmează o dinamică liniară de ordinul întîi \[ y_t = Z_t\alpha_t + \varepsilon_t, \qquad \alpha_{t+1} = c_t + T_t\alpha_t + R_t\eta_t, \qquad t = 1, \dots, n \]'),
    (T('Notation', 'Notațiile'),
     [T(r'$y_t$ ($p\times 1$): the observations; $\alpha_t$ ($m\times 1$): the state; $n$: the sample length', r'$y_t$ ($p\times 1$): observațiile; $\alpha_t$ ($m\times 1$): starea; $n$: lungimea eșantionului'),
      T(r'$Z_t$ ($p\times m$): the measurement matrix; $T_t$ ($m\times m$): the transition matrix; $c_t$: a known intercept', r'$Z_t$ ($p\times m$): matricea de măsurare; $T_t$ ($m\times m$): matricea de tranziție; $c_t$: un termen liber cunoscut'),
      T(r'$\varepsilon_t \sim N(0, H_t)$: measurement noise; $\eta_t \sim N(0, Q_t)$: state shocks; $R_t$ ($m\times r$) selects the states that receive shocks', r'$\varepsilon_t \sim N(0, H_t)$: zgomotul de măsurare; $\eta_t \sim N(0, Q_t)$: șocurile stării; $R_t$ ($m\times r$) alege stările care primesc șocuri'),
      T(r'$\varepsilon_t$ and $\eta_s$ are independent of each other and over time', r'$\varepsilon_t$ și $\eta_s$ sînt independente între ele și în timp')]),
    (T(r'Initial state $\alpha_1 \sim N(a_1, P_1)$', r'Starea inițială $\alpha_1 \sim N(a_1, P_1)$'),
     [T(r'nonstationary or unknown fixed elements: $P_1 = \kappa P_\infty + P_*$, $\kappa \to \infty$; $P_\infty$ marks the diffuse elements, $P_*$ the covariance of the others', r'elementele nestaționare sau fixe necunoscute: $P_1 = \kappa P_\infty + P_*$, $\kappa \to \infty$; $P_\infty$ marchează elementele difuze, $P_*$ este covarianța celorlalte')])), 'small')

D.frame(T('The general state space form (2/2)', 'Forma generală în spațiul stărilor (2/2)'), items(
    (T(r'The system matrices $Z_t, T_t, R_t, H_t, Q_t$ depend on parameters $\psi$; time variation in $Z_t$ gives regressions with time-varying coefficients',
       r'Matricele sistemului $Z_t, T_t, R_t, H_t, Q_t$ depind de parametrii $\psi$; variația în timp a lui $Z_t$ dă regresii cu coeficienți variabili în timp'),
     [T(r'ARMA, UC, TVP regressions, DFM, VAR with missing data, ETS: all are special cases \refDK',
        r'ARMA, UC, regresii TVP, DFM, VAR cu date lipsă, ETS: toate sînt cazuri particulare \refDK')]),
    (T(r'Notation for the estimates', r'Notațiile pentru estimații'),
     [T(r'$Y_t = (y_1, \dots, y_t)$: the data up to $t$', r'$Y_t = (y_1, \dots, y_t)$: datele pînă la $t$'),
      T(r'predicted state: $a_t = \E(\alpha_t | Y_{t-1})$, $P_t = \Var(\alpha_t | Y_{t-1})$; filtered: $a_{t|t}$, $P_{t|t}$ (after $y_t$)', r'starea prezisă: $a_t = \E(\alpha_t | Y_{t-1})$, $P_t = \Var(\alpha_t | Y_{t-1})$; filtrată: $a_{t|t}$, $P_{t|t}$ (după $y_t$)'),
      T(r'smoothed: $\hat\alpha_t = \E(\alpha_t | Y_n)$, $V_t = \Var(\alpha_t | Y_n)$ (all the data)', r'netezită: $\hat\alpha_t = \E(\alpha_t | Y_n)$, $V_t = \Var(\alpha_t | Y_n)$ (toate datele)')])), 'small')

D.frame(T('The Kalman filter from one lemma', 'Filtrul Kalman dintr-o singură lemă'), items(
    (T(r'Lemma (conditioning of jointly normal vectors): if $(x, y)$ is Gaussian, $\E(x | y) = \mu_x + \Sigma_{xy}\Sigma_{yy}^{-1}(y - \mu_y)$, $\Var(x | y) = \Sigma_{xx} - \Sigma_{xy}\Sigma_{yy}^{-1}\Sigma_{yx}$',
       r'Lema (condiționarea vectorilor normali comuni): dacă $(x, y)$ este gaussian, $\E(x | y) = \mu_x + \Sigma_{xy}\Sigma_{yy}^{-1}(y - \mu_y)$, $\Var(x | y) = \Sigma_{xx} - \Sigma_{xy}\Sigma_{yy}^{-1}\Sigma_{yx}$'),
     [T(r'$\mu_x$, $\mu_y$: the means; $\Sigma_{xy} = \Cov(x, y)$, $\Sigma_{yy} = \Var(y)$: the covariance blocks', r'$\mu_x$, $\mu_y$: mediile; $\Sigma_{xy} = \Cov(x, y)$, $\Sigma_{yy} = \Var(y)$: blocurile de covarianță'),
      T(r'apply it to $x = \alpha_t$ and $y = y_t$, conditional on $Y_{t-1}$: $v_t = y_t - Z_ta_t$ is the new information (the prediction error)',
        r'o aplicăm pentru $x = \alpha_t$ și $y = y_t$, condiționat de $Y_{t-1}$: $v_t = y_t - Z_ta_t$ este informația nouă (eroarea de predicție)')]),
    T(r'Prediction-error variance $\Var(v_t | Y_{t-1}) = F_t = Z_tP_tZ_t\' + H_t$; $\Cov(\alpha_t, v_t | Y_{t-1}) = P_tZ_t\'$; $v_t$ is independent of $Y_{t-1}$',
      r'Varianța erorii de predicție $\Var(v_t | Y_{t-1}) = F_t = Z_tP_tZ_t\' + H_t$; $\Cov(\alpha_t, v_t | Y_{t-1}) = P_tZ_t\'$; $v_t$ este independent de $Y_{t-1}$'),
    T(r'Update: $a_{t|t} = a_t + P_tZ_t\'F_t^{-1}v_t$, $P_{t|t} = P_t - P_tZ_t\'F_t^{-1}Z_tP_t$',
      r'Actualizarea: $a_{t|t} = a_t + P_tZ_t\'F_t^{-1}v_t$, $P_{t|t} = P_t - P_tZ_t\'F_t^{-1}Z_tP_t$'),
    T(r'Prediction: $a_{t+1} = c_t + T_ta_{t|t}$, $P_{t+1} = T_tP_{t|t}T_t\' + R_tQ_tR_t\'$',
      r'Predicția: $a_{t+1} = c_t + T_ta_{t|t}$, $P_{t+1} = T_tP_{t|t}T_t\' + R_tQ_tR_t\'$'),
    T(r'Without normality the same recursions give the best \emph{linear} predictor (minimum mean square error among linear functions of $Y_t$)',
      r'Fără normalitate, aceleași recursii dau cel mai bun predictor \emph{liniar} (eroare pătratică medie minimă printre funcțiile liniare de $Y_t$)')), 'small')

D.frame(T('The filter in one pass', 'Filtrul într-o singură trecere'), items(
    T(r'$v_t = y_t - Z_ta_t$, $\quad F_t = Z_tP_tZ_t\' + H_t$, $\quad K_t = T_tP_tZ_t\'F_t^{-1}$ (Kalman gain), $\quad L_t = T_t - K_tZ_t$',
      r'$v_t = y_t - Z_ta_t$, $\quad F_t = Z_tP_tZ_t\' + H_t$, $\quad K_t = T_tP_tZ_t\'F_t^{-1}$ (cîștigul Kalman), $\quad L_t = T_t - K_tZ_t$'),
    T(r'$a_{t+1} = c_t + T_ta_t + K_tv_t$, $\quad P_{t+1} = T_tP_tL_t\' + R_tQ_tR_t\'$',
      r'$a_{t+1} = c_t + T_ta_t + K_tv_t$, $\quad P_{t+1} = T_tP_tL_t\' + R_tQ_tR_t\'$'),
    (T(r'Cost: $O(n(m^3 + p^3))$; with time-invariant matrices $P_t$ converges to the steady state of the Riccati equation',
       r'Costul: $O(n(m^3 + p^3))$; cu matrice constante, $P_t$ converge către starea staționară a ecuației Riccati'),
     [T(r'$P_t$ and $K_t$ do not depend on $y$: they can be computed before the data arrive', r'$P_t$ și $K_t$ nu depind de $y$: se pot calcula înainte de sosirea datelor')]),
    (T(r'Missing $y_t$: set $Z_t = 0$ (or drop the missing rows): $v_t$ and $K_t$ vanish and the filter only predicts',
       r'$y_t$ lipsă: punem $Z_t = 0$ (sau eliminăm rîndurile lipsă): $v_t$ și $K_t$ dispar, iar filtrul doar prezice'),
     [T(r'mixed frequencies and the ragged edge of real-time data are therefore free (Chapter 5)', r'frecvențele mixte și ragged edge al datelor în timp real se tratează deci fără cost suplimentar (Capitolul 5)')]),
    T(r'Multivariate $y_t$ with diagonal $H_t$: process the $p$ elements one at a time (univariate treatment \refKD): no $p\times p$ inversion',
      r'$y_t$ multivariat cu $H_t$ diagonală: prelucrăm cele $p$ elemente pe rînd (tratarea univariată \refKD): fără inversarea unei matrice $p\times p$')), 'small')

D.frame(T('Smoothing: backward recursions', 'Netezirea: recursii înapoi'), items(
    T(r'State smoother \refDK: $r_{t-1} = Z_t\'F_t^{-1}v_t + L_t\'r_t$, $\quad N_{t-1} = Z_t\'F_t^{-1}Z_t + L_t\'N_tL_t$, $\quad r_n = 0$, $N_n = 0$',
      r'Netezitorul stărilor \refDK: $r_{t-1} = Z_t\'F_t^{-1}v_t + L_t\'r_t$, $\quad N_{t-1} = Z_t\'F_t^{-1}Z_t + L_t\'N_tL_t$, $\quad r_n = 0$, $N_n = 0$'),
    (T(r'Smoothed state: $\hat\alpha_t = a_t + P_tr_{t-1}$, $\quad V_t = P_t - P_tN_{t-1}P_t$', r'Starea netezită: $\hat\alpha_t = a_t + P_tr_{t-1}$, $\quad V_t = P_t - P_tN_{t-1}P_t$'),
     [T(r'$r_{t-1}$: a weighted sum of the innovations from $t$ on; $N_{t-1} = \Var(r_{t-1})$', r'$r_{t-1}$: o sumă ponderată a inovațiilor de la $t$ încolo; $N_{t-1} = \Var(r_{t-1})$'),
      T(r'$\hat\alpha_t$ corrects $a_t$ by everything learned from $t$ on', r'$\hat\alpha_t$ corectează $a_t$ cu tot ce aflăm de la momentul $t$ încolo')]),
    T(r'Disturbance smoother: $\hat\varepsilon_t = H_t(F_t^{-1}v_t - K_t\'r_t)$, $\hat\eta_t = Q_tR_t\'r_t$: auxiliary residuals for outliers and breaks, and the score of the likelihood',
      r'Netezitorul perturbațiilor: $\hat\varepsilon_t = H_t(F_t^{-1}v_t - K_t\'r_t)$, $\hat\eta_t = Q_tR_t\'r_t$: reziduuri auxiliare pentru valori extreme și rupturi și scorul verosimilității'),
    T(r'Derivation from the same lemma, now conditioning on $v_t, \dots, v_n$, which are independent (Appendix)',
      r'Derivarea folosește aceeași lemă, acum condiționînd pe $v_t, \dots, v_n$, care sînt independente (Anexa)')), 'small')

D.frame(T('Diffuse initialisation (1/2)', 'Inițializarea difuză (1/2)'), items(
    (T(r'Random walks, trends and regression coefficients have no stationary distribution: $P_1 = \kappa P_\infty + P_*$, $\kappa \to \infty$',
       r'Mersurile aleatoare, trendurile și coeficienții de regresie nu au distribuție staționară: $P_1 = \kappa P_\infty + P_*$, $\kappa \to \infty$'),
     [T(r'``big kappa\'\' ($\kappa = 10^6$--$10^7$) is an approximation with two failures: the likelihood contains $-\frac12\ln\kappa$ terms, and round-off errors grow with $\kappa$',
        r'„big kappa” ($\kappa = 10^6$--$10^7$) este o aproximare cu două defecte: verosimilitatea conține termeni $-\frac12\ln\kappa$, iar erorile de rotunjire cresc cu $\kappa$')]),
    (T(r'Exact diffuse filter \refKoo, \refAK, \refdJa', r'Filtrul difuz exact \refKoo, \refAK, \refdJa'),
     [T(r'expand $P_t = \kappa P_{\infty,t} + P_{*,t} + O(\kappa^{-1})$ and keep both parts while $P_{\infty,t} \ne 0$', r'dezvoltăm $P_t = \kappa P_{\infty,t} + P_{*,t} + O(\kappa^{-1})$ și păstrăm ambele părți cît timp $P_{\infty,t} \ne 0$'),
      T(r'$P_{\infty,t}$ reaches zero after $d$ steps ($d$ = number of diffuse elements, if they are identified)', r'$P_{\infty,t}$ ajunge la zero după $d$ pași ($d$ = numărul elementelor difuze, dacă sînt identificate)'),
      T('then the ordinary filter takes over', 'apoi preia filtrul obișnuit')])), 'small')

D.frame(T('Diffuse initialisation (2/2)', 'Inițializarea difuză (2/2)'), items(
    (T('The exact diffuse recursions', 'Recursiile difuze exacte'),
     [T(r'$F_{\infty,t}$, $F_{*,t}$: the diffuse and finite parts of $F_t$; $K^{(0)}_t$, $K^{(1)}_t$: the matching gains; $L^{(0)}_t = T_t - K^{(0)}_tZ_t$, $L^{(1)}_t = -K^{(1)}_tZ_t$', r'$F_{\infty,t}$, $F_{*,t}$: părțile difuză și finită ale lui $F_t$; $K^{(0)}_t$, $K^{(1)}_t$: cîștigurile corespunzătoare; $L^{(0)}_t = T_t - K^{(0)}_tZ_t$, $L^{(1)}_t = -K^{(1)}_tZ_t$'),
      T(r'univariate $y_t$, $F_{\infty,t} = Z_tP_{\infty,t}Z_t\' > 0$: $K^{(0)}_t = T_tP_{\infty,t}Z_t\'/F_{\infty,t}$, $K^{(1)}_t = T_t(P_{*,t}Z_t\' - P_{\infty,t}Z_t\'F_{*,t}/F_{\infty,t})/F_{\infty,t}$',
        r'$y_t$ univariat, $F_{\infty,t} = Z_tP_{\infty,t}Z_t\' > 0$: $K^{(0)}_t = T_tP_{\infty,t}Z_t\'/F_{\infty,t}$, $K^{(1)}_t = T_t(P_{*,t}Z_t\' - P_{\infty,t}Z_t\'F_{*,t}/F_{\infty,t})/F_{\infty,t}$'),
      T(r'$a_{t+1} = c_t + T_ta_t + K^{(0)}_tv_t$; $P_{\infty,t+1} = T_tP_{\infty,t}L^{(0)\prime}_t$; $P_{*,t+1} = T_tP_{\infty,t}L^{(1)\prime}_t + T_tP_{*,t}L^{(0)\prime}_t + R_tQ_tR_t\'$',
        r'$a_{t+1} = c_t + T_ta_t + K^{(0)}_tv_t$; $P_{\infty,t+1} = T_tP_{\infty,t}L^{(0)\prime}_t$; $P_{*,t+1} = T_tP_{\infty,t}L^{(1)\prime}_t + T_tP_{*,t}L^{(0)\prime}_t + R_tQ_tR_t\'$')]),
    T(r'The smoother has matching diffuse recursions for $r^{(0)}, r^{(1)}, N^{(0)}, N^{(1)}, N^{(2)}$ \refDK, Section 5.3; in the Quantlet both are checked against \texttt{statsmodels}',
      r'Netezitorul are recursii difuze corespunzătoare pentru $r^{(0)}, r^{(1)}, N^{(0)}, N^{(1)}, N^{(2)}$ \refDK, secțiunea 5.3; în Quantlet ambele sînt comparate cu \texttt{statsmodels}')), 'footnotesize')

chart(T('Exact diffuse against big kappa', 'Inițializarea difuză exactă față de big kappa'), 'ats_ch6_diffuse', 'ATS_ch6_kalman_mle', [
    T(r'Left: local level for US GDP-deflator inflation at the ML variances; right: local linear trend for 100$\times$log Romanian real GDP, $T = @{df.Tg}$; both against the exact diffuse filter',
      r'Stînga: modelul local level pentru inflația deflatorului PIB din SUA, la varianțele ML; dreapta: local linear trend pentru 100$\times$log PIB real al României, $T = @{df.Tg}$; ambele comparate cu filtrul difuz exact')],
    h='0.65\\textheight')

interp(('the diffuse initialisation', 'inițializării difuze'), [
    T(r'With all terms, the big-kappa log-likelihood falls by $\frac12\ln 10$ per decade of $\kappa$: @{df.raw7} at $\kappa = 10^7$, @{df.raw14} at $10^{14}$; the exact value is @{df.exact}',
      r'Cu toți termenii, log-verosimilitatea big kappa scade cu $\frac12\ln 10$ la fiecare ordin de mărime al lui $\kappa$: @{df.raw7} la $\kappa = 10^7$, @{df.raw14} la $10^{14}$; valoarea exactă este @{df.exact}'),
    T(r'Replacing the first term by its diffuse limit repairs the level (@{df.adj7} at $10^7$), but only because $d = 1$ is known; ML over $\psi$ is unaffected, model comparison across different $d$ is not',
      r'Înlocuirea primului termen cu limita lui difuză repară nivelul (@{df.adj7} la $10^7$), dar doar pentru că știm că $d = 1$; estimarea ML după $\psi$ nu este afectată, compararea modelelor cu $d$ diferit este'),
    T(r'Smoothed variances: error @{df.ev4} at $\kappa = 10^4$, @{df.ev8} at $10^8$ and $10^{@{df.ev16e}}$ at $10^{16}$: no single $\kappa$ is safe for both states and variances',
      r'Varianțele netezite: eroarea este @{df.ev4} la $\kappa = 10^4$, @{df.ev8} la $10^8$ și $10^{@{df.ev16e}}$ la $10^{16}$: niciun $\kappa$ nu este sigur simultan pentru stări și pentru varianțe'),
    T('Practical rule: use the exact diffuse filter whenever the model has nonstationary or fixed unknown states', 'Regula practică: folosiți filtrul difuz exact ori de cîte ori modelul are stări nestaționare sau fixe necunoscute')])

D.recap(('The general linear Gaussian model', 'modelul liniar gaussian general'), [
    T('One lemma (Gaussian conditioning) gives the filter, the smoother and the disturbance smoother', 'O singură lemă (condiționarea gaussiană) dă filtrul, netezitorul și netezitorul perturbațiilor'),
    T('Missing data, mixed frequencies and multivariate observations are handled inside the same recursions', 'Datele lipsă, frecvențele mixte și observațiile multivariate se tratează în aceleași recursii'),
    T('Nonstationary states need the exact diffuse filter; big kappa breaks the likelihood level and the smoothed variances', 'Stările nestaționare cer filtrul difuz exact; big kappa denaturează nivelul verosimilității și varianțele netezite')])

# =============================================================================
# 2. VEROSIMILITATE
# =============================================================================
D.section('The exact likelihood and its maximisation', 'Verosimilitatea exactă și maximizarea ei')

D.frame(T('The prediction error decomposition, diffuse case', 'Descompunerea erorilor de predicție, cazul difuz'), items(
    T(r'$p(y_1, \dots, y_n) = \prod_t p(y_t | Y_{t-1})$, and $y_t | Y_{t-1} \sim N(Z_ta_t, F_t)$: the likelihood is a by-product of the filter',
      r'$p(y_1, \dots, y_n) = \prod_t p(y_t | Y_{t-1})$, iar $y_t | Y_{t-1} \sim N(Z_ta_t, F_t)$: verosimilitatea este un produs secundar al filtrului'),
    T(r'Diffuse log-likelihood \refDK, eq.~(7.4): $\ln L_d = -\frac{np}{2}\ln 2\pi - \frac12\sum_{t=1}^d w_t - \frac12\sum_{t=d+1}^n(\ln|F_t| + v_t\'F_t^{-1}v_t)$',
      r'Log-verosimilitatea difuză \refDK, ec.~(7.4): $\ln L_d = -\frac{np}{2}\ln 2\pi - \frac12\sum_{t=1}^d w_t - \frac12\sum_{t=d+1}^n(\ln|F_t| + v_t\'F_t^{-1}v_t)$'),
    (T(r'$w_t = \ln F_{\infty,t}$ if $F_{\infty,t} > 0$, otherwise $w_t = \ln F_{*,t} + v_t^2/F_{*,t}$: the first $d$ observations only pin down the diffuse states',
       r'$w_t = \ln F_{\infty,t}$ dacă $F_{\infty,t} > 0$, altfel $w_t = \ln F_{*,t} + v_t^2/F_{*,t}$: primele $d$ observații doar fixează stările difuze'),
     [T(r'equivalent to the marginal likelihood of \refdJa\ and to treating the diffuse states as fixed and concentrating them out',
        r'echivalentă cu verosimilitatea marginală din \refdJa\ și cu tratarea stărilor difuze ca parametri ficși, eliminați prin concentrare')]),
    T(r'Scale: write $H_t = \sigma^2H^*_t$, $Q_t = \sigma^2Q^*_t$; then $F_t = \sigma^2F^*_t$ and $\hat\sigma^2 = \frac{1}{p(n - d)}\sum_{t>d}v_t\'F_t^{*-1}v_t$: one parameter fewer in the numerical search',
      r'Scala: scriem $H_t = \sigma^2H^*_t$, $Q_t = \sigma^2Q^*_t$; atunci $F_t = \sigma^2F^*_t$ și $\hat\sigma^2 = \frac{1}{p(n - d)}\sum_{t>d}v_t\'F_t^{*-1}v_t$: un parametru mai puțin în căutarea numerică')), 'small')

D.frame(T('Maximising the likelihood', 'Maximizarea verosimilității'), items(
    (T(r'Parameterise variances as $\exp(\cdot)$, correlations as $\tanh(\cdot)$, AR coefficients through partial autocorrelations: unconstrained search, stationary models only',
       r'Parametrizăm varianțele prin $\exp(\cdot)$, corelațiile prin $\tanh(\cdot)$, coeficienții AR prin autocorelațiile parțiale: căutare fără restricții, doar modele staționare'),
     [T('several starting values: UC likelihoods are often multimodal (MNZ below)', 'mai multe puncte de pornire: verosimilitățile UC sînt adesea multimodale (MNZ, mai jos)')]),
    T(r'Score in one filter-smoother pass: $\partial\ln L/\partial\psi = \frac12\sum_t\mathrm{tr}\{(\hat\varepsilon_t\hat\varepsilon_t\' + \Var(\varepsilon_t|Y_n) - H_t)H_t^{-1}\tfrac{\partial H_t}{\partial\psi}H_t^{-1}\} + \dots$ \refDK, Section 7.3',
      r'Scorul într-o singură trecere filtru--netezitor: $\partial\ln L/\partial\psi = \frac12\sum_t\mathrm{tr}\{(\hat\varepsilon_t\hat\varepsilon_t\' + \Var(\varepsilon_t|Y_n) - H_t)H_t^{-1}\tfrac{\partial H_t}{\partial\psi}H_t^{-1}\} + \dots$ \refDK, secțiunea 7.3'),
    T(r'EM algorithm \refSS: the E-step is the smoother, the M-step has closed forms for $H$ and $Q$; slow near the optimum but robust from poor starts (large DFM)',
      r'Algoritmul EM \refSS: pasul E este netezitorul, pasul M are formule explicite pentru $H$ și $Q$; lent lîngă optim, dar robust la puncte de pornire slabe (DFM mari)'),
    T(r'Standard errors: inverse Hessian at $\hat\psi$ (numerical); valid only for interior points; report them on the transformed scale',
      r'Erorile standard: inversa hessianei în $\hat\psi$ (numerică); valabile doar pentru puncte interioare; le raportăm pe scala transformată'),
    T(r'Identification: some UC models are observationally equivalent to ARIMA models with fewer parameters; check the reduced form before interpreting the components',
      r'Identificarea: unele modele UC sînt echivalente observațional cu modele ARIMA cu mai puțini parametri; verificați forma redusă înainte de a interpreta componentele')), 'small')

chart(T('Local level for US inflation: numpy against statsmodels', 'Local level pentru inflația din SUA: numpy față de statsmodels'), 'ats_ch6_local_level', 'ATS_ch6_kalman_mle', [
    T(r'GDP-deflator inflation, @{ll.first}--@{ll.last}, $T = @{ll.T}$; exact diffuse ML; the smoothed level with a 90\% band and the one-sided (filtered) level',
      r'Inflația deflatorului PIB, @{ll.first}--@{ll.last}, $T = @{ll.T}$; ML difuz exact; nivelul netezit cu o bandă de 90\% și nivelul unilateral (filtrat)')],
    h='0.65\\textheight')

interp(('the local level estimates', 'estimațiilor local level'), [
    T(r'numpy: $\hat\sigma^2_\varepsilon = @{ll.s2e}$, $\hat\sigma^2_\eta = @{ll.s2h}$, $\hat q = @{ll.q}$; statsmodels: @{ll.sms2e} and @{ll.sms2h}: the same optimum',
      r'numpy: $\hat\sigma^2_\varepsilon = @{ll.s2e}$, $\hat\sigma^2_\eta = @{ll.s2h}$, $\hat q = @{ll.q}$; statsmodels: @{ll.sms2e} și @{ll.sms2h}: același optim'),
    T(r'Log-likelihoods @{ll.ll} and @{ll.smll}: they differ by exactly $\frac12\ln 2\pi = @{ll.gap}$, the constant that \texttt{statsmodels} omits for the $d = 1$ diffuse observation',
      r'Log-verosimilitățile @{ll.ll} și @{ll.smll}: diferă exact cu $\frac12\ln 2\pi = @{ll.gap}$, constanta pe care \texttt{statsmodels} o omite pentru observația difuză ($d = 1$)'),
    T(r'Steady-state gain @{ll.K}: each new quarter moves the level estimate by @{ll.Kp}\% of the surprise; inflation is closer to a random walk than to white noise around a mean',
      r'Cîștigul în starea staționară este @{ll.K}: fiecare trimestru nou mută estimația nivelului cu @{ll.Kp}\% din surpriză; inflația este mai aproape de un mers aleator decît de un zgomot alb în jurul unei medii'),
    T(r'Last smoothed level @{ll.lev}\% (s.d. @{ll.levsd}): at the end of the sample the smoothed and filtered estimates coincide, and so does their uncertainty',
      r'Ultimul nivel netezit este @{ll.lev}\% (abatere standard @{ll.levsd}): la finalul eșantionului estimațiile netezite și filtrate coincid, la fel și incertitudinea lor'),
    T(r'One constant variance for 1953--2026 is implausible (Great Inflation, Great Moderation): this motivates UC-SV in the last section',
      r'O singură varianță constantă pentru 1953--2026 este neplauzibilă (Marea Inflație, Marea Moderație): de aici modelul UC-SV din ultima secțiune')])

D.frame(T('Inference at the boundary: the pile-up problem', 'Inferența la frontieră: problema pile-up'), items(
    (T(r'Local level with $q = \sigma^2_\eta/\sigma^2_\varepsilon$: the ML estimate equals exactly zero with positive probability even when $q > 0$ \refSH',
       r'Modelul local level cu $q = \sigma^2_\eta/\sigma^2_\varepsilon$: estimația ML este exact zero cu probabilitate pozitivă chiar dacă $q > 0$ \refSH'),
     [T(r'the score at $q = 0$ is often negative because a smooth trend fits the data better than a slightly wandering one',
        r'scorul în $q = 0$ este adesea negativ, pentru că un trend neted se potrivește datelor mai bine decît unul care rătăcește puțin')]),
    (T('Consequences', 'Consecințele'),
     [T('the confidence interval computed from the Hessian is invalid', 'intervalul de încredere calculat din hessiană nu este valid'),
      T(r'the LR test of $q = 0$ is not $\chi^2_1$, not even $\frac12\chi^2_0 + \frac12\chi^2_1$: the model under the alternative is nonstationary', r'testul LR pentru $q = 0$ nu este $\chi^2_1$, nici măcar $\frac12\chi^2_0 + \frac12\chi^2_1$: modelul sub alternativă este nestaționar'),
      T(r'remedies: median-unbiased estimation of a coefficient variance \refSWa; parametric bootstrap of the LR statistic (TVP section); Bayesian priors that keep $q$ away from zero',
        r'remedii: estimarea median-nedeplasată a varianței coeficienților \refSWa; bootstrap parametric pentru statistica LR (secțiunea TVP); distribuții a priori care țin $q$ departe de zero')]),
    T(r'Same issue in TVP regressions (is the coefficient constant?) and in UC models (is the trend deterministic?)',
      r'Aceeași problemă apare în regresiile TVP (este coeficientul constant?) și în modelele UC (este trendul determinist?)')), 'small')

chart(T('How often is the estimated level variance exactly zero?', 'Cît de des este varianța estimată a nivelului exact zero?'), 'ats_ch6_pileup', 'ATS_ch6_kalman_mle', [
    T(r'@{pu.reps} simulated local level series of length $T = @{pu.n}$ for each true $q$; ML of $q$ on a fine grid with $\sigma^2_\varepsilon$ concentrated out',
      r'Cîte @{pu.reps} de serii local level simulate de lungime $T = @{pu.n}$ pentru fiecare $q$ adevărat; ML pentru $q$ pe o grilă fină, cu $\sigma^2_\varepsilon$ eliminat prin concentrare')],
    h='0.65\\textheight')

interp(('the pile-up simulation', 'simulării pile-up'), [
    T(r'True $q = 0$: @{pu.z0}\% of the estimates are exactly zero; the rest spread over several orders of magnitude',
      r'Pentru $q = 0$ adevărat: @{pu.z0}\% dintre estimații sînt exact zero; restul se împrăștie pe mai multe ordine de mărime'),
    T(r'True $q = 0.01$: still @{pu.z1}\% zeros; median estimate @{pu.m1}; with $q = 0.05$: @{pu.z5}\% zeros',
      r'Pentru $q = 0{,}01$: tot @{pu.z1}\% zerouri; mediana estimațiilor este @{pu.m1}; pentru $q = 0{,}05$: @{pu.z5}\% zerouri'),
    T(r'A reported $\hat\sigma^2_\eta = 0$ is therefore not evidence of a constant level; a small positive value is compatible with a deterministic one',
      r'Un $\hat\sigma^2_\eta = 0$ raportat nu este deci o dovadă a unui nivel constant; o valoare pozitivă mică este compatibilă cu un nivel determinist'),
    T('Report the profile likelihood or the posterior of $q$, not a point estimate with a Hessian standard error', 'Raportați verosimilitatea profil sau distribuția a posteriori a lui $q$, nu o estimație punctuală cu o eroare standard din hessiană')])

D.recap(('The exact likelihood', 'verosimilitatea exactă'), [
    T('The filter delivers the Gaussian likelihood; with diffuse states the first $d$ terms are replaced by their diffuse limits', 'Filtrul dă verosimilitatea gaussiană; cu stări difuze, primii $d$ termeni sînt înlocuiți cu limitele lor difuze'),
    T('Concentrate the scale, parameterise without constraints, use several starts, and check the numbers against a second implementation', 'Concentrați scala, parametrizați fără restricții, folosiți mai multe puncte de pornire și verificați cifrele cu o a doua implementare'),
    T('Variances near zero pile up at zero: standard errors and $\\chi^2$ tests fail at the boundary', 'Varianțele apropiate de zero se acumulează în zero: erorile standard și testele $\\chi^2$ nu funcționează la frontieră')])

# =============================================================================
# 3. SIMULARE ȘI GIBBS
# =============================================================================
D.section('Bayesian state space: simulation smoothing and Gibbs sampling', 'Spațiul stărilor bayesian: simulation smoothing și eșantionare Gibbs')

D.frame(T('Why sample the states?', 'Eșantionarea stărilor'), two(
    ph('bayes', T('Portrait traditionally identified as Thomas Bayes (identification uncertain)', 'Portret identificat tradițional cu Thomas Bayes (identificare incertă)'), h='0.34\\textheight'),
    items(T(r'Target: $p(\alpha_1, \dots, \alpha_n, \psi | Y_n)$; the filter gives $p(\alpha_t | Y_t, \psi)$ for one $t$ and one $\psi$ only',
            r'Ținta: $p(\alpha_1, \dots, \alpha_n, \psi | Y_n)$; filtrul dă $p(\alpha_t | Y_t, \psi)$ doar pentru un $t$ și un $\psi$'),
          T(r'Gibbs sampler: alternate $\alpha_{1:n} \sim p(\alpha_{1:n} | \psi, Y_n)$ and $\psi \sim p(\psi | \alpha_{1:n}, Y_n)$; given the states, $\psi$ is often a conjugate regression problem',
            r'Eșantionatorul Gibbs: alternăm $\alpha_{1:n} \sim p(\alpha_{1:n} | \psi, Y_n)$ și $\psi \sim p(\psi | \alpha_{1:n}, Y_n)$; dată fiind starea, $\psi$ este adesea o problemă de regresie conjugată'),
          T(r'Uncertainty about $\psi$ enters the bands of the states (ML bands ignore it)', r'Incertitudinea despre $\psi$ intră în benzile stărilor (benzile ML o ignoră)'),
          T(r'Functions of whole paths become easy: the date of a peak, the probability that a trend stays inside a target band',
            r'Funcțiile de traiectorii întregi devin ușor de calculat: data unui maxim, probabilitatea ca un trend să rămînă într-o bandă-țintă'),
          T(r'Sampling the whole path in one block (not $\alpha_t$ one at a time) is what makes the sampler mix', r'Eșantionarea întregii traiectorii într-un singur bloc (nu cîte un $\alpha_t$) asigură o bună amestecare (mixing) a eșantionatorului')), '0.3', '0.68'), 'footnotesize')

D.frame(T('Forward filtering, backward sampling', 'Filtrare înainte, eșantionare înapoi'), items(
    T(r'Factorisation: $p(\alpha_{1:n} | Y_n) = p(\alpha_n | Y_n)\prod_{t=1}^{n-1}p(\alpha_t | \alpha_{t+1}, Y_t)$ (Markov property of the state)',
      r'Factorizarea: $p(\alpha_{1:n} | Y_n) = p(\alpha_n | Y_n)\prod_{t=1}^{n-1}p(\alpha_t | \alpha_{t+1}, Y_t)$ (proprietatea Markov a stării)'),
    T(r'Forward: run the filter, store $a_{t|t}, P_{t|t}$; draw $\alpha_n \sim N(a_{n|n}, P_{n|n})$ \refCK, \refFS',
      r'Înainte: rulăm filtrul și păstrăm $a_{t|t}, P_{t|t}$; extragem $\alpha_n \sim N(a_{n|n}, P_{n|n})$ \refCK, \refFS'),
    (T(r'Backward: $\alpha_t | \alpha_{t+1}, Y_t \sim N(m_t, S_t)$ by the lemma, with the smoothing gain $G_t = P_{t|t}T_t\'P_{t+1}^{-1}$ ($m_t$, $S_t$: conditional mean and variance):',
       r'Înapoi: $\alpha_t | \alpha_{t+1}, Y_t \sim N(m_t, S_t)$ din lemă, cu cîștigul de netezire $G_t = P_{t|t}T_t\'P_{t+1}^{-1}$ ($m_t$, $S_t$: media și varianța condiționate):'),
     [T(r'$m_t = a_{t|t} + G_t(\alpha_{t+1} - c_t - T_ta_{t|t})$, $\quad S_t = P_{t|t} - G_tT_tP_{t|t}$',
        r'$m_t = a_{t|t} + G_t(\alpha_{t+1} - c_t - T_ta_{t|t})$, $\quad S_t = P_{t|t} - G_tT_tP_{t|t}$')]),
    T(r'Issues: $P_{t+1}$ is singular when $R_tQ_tR_t\'$ is (lags in the state): use the rows with shocks only; $n$ draws of dimension $m$',
      r'Probleme: $P_{t+1}$ este singulară cînd $R_tQ_tR_t\'$ este singulară (laguri în stare): folosim doar rîndurile cu șocuri; $n$ extrageri de dimensiune $m$'),
    T(r'Same output as the Gibbs step in the Bayesian VAR and DFM samplers of Chapter 5', r'Același rezultat ca pasul Gibbs din eșantionatoarele BVAR și DFM din Capitolul 5')), 'small')

D.frame(T('The Durbin--Koopman simulation smoother', 'Simulation smoother-ul Durbin--Koopman'), items(
    T(r'Idea \refDKa: $\alpha - \hat\alpha(y)$ has the same conditional distribution for every $y$ (Gaussian model): simulate it once from the model',
      r'Ideea \refDKa: $\alpha - \hat\alpha(y)$ are aceeași distribuție condiționată pentru orice $y$ (modelul gaussian): o simulăm o singură dată din model'),
    (T('Algorithm (mean correction):', 'Algoritmul (corecția mediei):'),
     [T(r'1. draw $\alpha^+_{1:n}, y^+_{1:n}$ from the model (shocks and initial state); keep the missing pattern of $y$',
        r'1. extragem $\alpha^+_{1:n}, y^+_{1:n}$ din model (șocuri și stare inițială); păstrăm structura valorilor lipsă din $y$'),
      T(r'2. run one state smoother on $y - y^+$ (zero intercepts): $\hat\alpha(y - y^+) = \hat\alpha(y) - \hat\alpha(y^+)$',
        r'2. rulăm o singură dată netezitorul stărilor pe $y - y^+$ (termeni liberi nuli): $\hat\alpha(y - y^+) = \hat\alpha(y) - \hat\alpha(y^+)$'),
      T(r'3. $\tilde\alpha = \alpha^+ + \hat\alpha(y) - \hat\alpha(y^+)$ is a draw from $p(\alpha | Y_n)$',
        r'3. $\tilde\alpha = \alpha^+ + \hat\alpha(y) - \hat\alpha(y^+)$ este o extragere din $p(\alpha | Y_n)$')]),
    T(r'Only the mean smoother is needed: no $P_{t|t}$ inversions, no singularity problems, diffuse states handled by the exact diffuse smoother (proof of exactness: Appendix)  % applink: exactness of the Durbin',
      r'Este nevoie doar de netezitorul mediei: fără inversarea lui $P_{t|t}$, fără probleme de singularitate, stările difuze sînt tratate de netezitorul difuz exact (demonstrația: Anexa)  % applink: exactitatea simulation smoother'),
    T(r'Precursor: the disturbance simulation smoother of \refdJS; same idea for the disturbances $\varepsilon_t, \eta_t$',
      r'Precursor: simulation smoother-ul perturbațiilor din \refdJS; aceeași idee pentru perturbațiile $\varepsilon_t, \eta_t$')), 'small')

D.frame(T('The precision sampler', 'Eșantionarea pe baza matricei de precizie'), items(
    (T(r'Stack the model \refCJ: $y = X\alpha + \varepsilon$, $D\alpha = \eta$', r'Scriem modelul matriceal \refCJ: $y = X\alpha + \varepsilon$, $D\alpha = \eta$'),
     [T(r'$D$: a banded difference matrix (first differences for a random walk)', r'$D$: o matrice de diferențe în bandă (diferențe de ordinul întîi pentru un mers aleator)'),
      T(r'then $\alpha | y \sim N(\hat\alpha, K^{-1})$ with $K = D\'\Sigma_\eta^{-1}D + X\'\Sigma_\varepsilon^{-1}X$', r'atunci $\alpha | y \sim N(\hat\alpha, K^{-1})$, cu $K = D\'\Sigma_\eta^{-1}D + X\'\Sigma_\varepsilon^{-1}X$')]),
    (T(r'$K$ is banded (tridiagonal for a random walk): one banded Cholesky factor $K = U\'U$ costs $O(n)$',
       r'$K$ este în bandă (tridiagonală pentru un mers aleator): un singur factor Cholesky în bandă $K = U\'U$ costă $O(n)$'),
     [T(r'$\alpha$, $y$: all states and observations stacked; $X$: block-diagonal of the $Z_t$; $\Sigma_\varepsilon$, $\Sigma_\eta$: the stacked noise covariances; $K$: the posterior precision (inverse covariance)', r'$\alpha$, $y$: toate stările și observațiile așezate una sub alta; $X$: matricea bloc-diagonală a lui $Z_t$; $\Sigma_\varepsilon$, $\Sigma_\eta$: covarianțele zgomotelor; $K$: precizia a posteriori (inversa covarianței)'),
      T(r'$\hat\alpha$ solves $K\hat\alpha = X\'\Sigma_\varepsilon^{-1}y$; a draw is $\hat\alpha + U^{-1}z$, $z \sim N(0, I)$',
        r'$\hat\alpha$ rezolvă $K\hat\alpha = X\'\Sigma_\varepsilon^{-1}y$; o extragere este $\hat\alpha + U^{-1}z$, $z \sim N(0, I)$')]),
    T(r'Time-varying variances (stochastic volatility) only change the diagonal weights: ideal inside Gibbs samplers for UC-SV and SV',
      r'Varianțele variabile în timp (volatilitatea stochastică) schimbă doar ponderile de pe diagonală: ideal în eșantionatoarele Gibbs pentru UC-SV și SV'),
    T(r'Three samplers, one target: FFBS, DK and precision sampling draw from the same $p(\alpha | Y_n, \psi)$; they differ in cost and generality',
      r'Trei eșantionatoare, o singură țintă: FFBS, DK și eșantionarea pe baza preciziei extrag din aceeași $p(\alpha | Y_n, \psi)$; diferă prin cost și generalitate')), 'small')

chart(T('Three samplers of the same posterior', 'Trei eșantionatoare pentru aceeași distribuție a posteriori'), 'ats_ch6_simsmoother', 'ATS_ch6_simulation_smoother', [
    T(r'Local level for US inflation at the ML variances, proper prior $\mu_1 \sim N(y_1, 100)$; left: s.d. of @{sm.draws} draws against the exact smoother; right: time per draw for simulated samples',
      r'Local level pentru inflația din SUA la varianțele ML, a priori propriu $\mu_1 \sim N(y_1, 100)$; stînga: abaterea standard a @{sm.draws} de extrageri față de netezitorul exact; dreapta: timpul pe extragere pentru eșantioane simulate')],
    h='0.65\\textheight')

interp(('the three samplers', 'celor trei eșantionatoare'), [
    T(r'Ratios of draw s.d. to exact s.d. lie in [@{sm.ck.lo}; @{sm.ck.hi}] (FFBS), [@{sm.dk.lo}; @{sm.dk.hi}] (DK) and [@{sm.pr.lo}; @{sm.pr.hi}] (precision): Monte Carlo noise only',
      r'Rapoartele dintre abaterea standard a extragerilor și cea exactă se află în [@{sm.ck.lo}; @{sm.ck.hi}] (FFBS), [@{sm.dk.lo}; @{sm.dk.hi}] (DK) și [@{sm.pr.lo}; @{sm.pr.hi}] (precizie): doar zgomot Monte Carlo'),
    T(r'Largest error of the draw means: @{sm.ck.err}, @{sm.dk.err}, @{sm.pr.err}, of the order of the Monte Carlo standard error',
      r'Cea mai mare eroare a mediilor extragerilor: @{sm.ck.err}, @{sm.dk.err}, @{sm.pr.err}, de ordinul erorii standard Monte Carlo'),
    T(r'For $T = 4000$: @{sm.ck.t4000} ms (FFBS), @{sm.dk.t4000} ms (DK), @{sm.pr.t4000} ms (precision) per draw; all linear in $T$, the banded solver has no Python loop',
      r'Pentru $T = 4000$: @{sm.ck.t4000} ms (FFBS), @{sm.dk.t4000} ms (DK), @{sm.pr.t4000} ms (precizie) pe extragere; toate sînt liniare în $T$, rezolvarea în bandă nu are buclă Python'),
    T('Choose DK for general models with diffuse states, precision sampling for random walks with time-varying variances', 'Alegeți DK pentru modele generale cu stări difuze și eșantionarea pe baza preciziei pentru mersuri aleatoare cu varianțe variabile în timp')])

D.frame(T('A Gibbs sampler for the local level model', 'Un eșantionator Gibbs pentru modelul local level'), items(
    T(r'Model: $y_t = \mu_t + \varepsilon_t$, $\mu_{t+1} = \mu_t + \eta_t$; $\mu_t$: the level; $IG(a_0, b_0)$: inverse gamma prior with shape $a_0$ and scale $b_0$; $q = \sigma^2_\eta/\sigma^2_\varepsilon$', r'Modelul: $y_t = \mu_t + \varepsilon_t$, $\mu_{t+1} = \mu_t + \eta_t$; $\mu_t$: nivelul; $IG(a_0, b_0)$: distribuția a priori inverse gamma cu formă $a_0$ și scală $b_0$; $q = \sigma^2_\eta/\sigma^2_\varepsilon$'),
    T(r'Block 1: $\mu_{1:n} | \sigma^2_\varepsilon, \sigma^2_\eta, Y_n$ by the DK simulation smoother (exact diffuse $\mu_1$)',
      r'Blocul 1: $\mu_{1:n} | \sigma^2_\varepsilon, \sigma^2_\eta, Y_n$ prin simulation smoother-ul DK (cu $\mu_1$ difuz exact)'),
    T(r'Block 2: $\sigma^2_\varepsilon | \mu, Y_n \sim IG(a_0 + \frac n2, b_0 + \frac12\sum_t(y_t - \mu_t)^2)$; $\sigma^2_\eta | \mu \sim IG(a_0 + \frac{n-1}{2}, b_0 + \frac12\sum_t(\Delta\mu_t)^2)$',
      r'Blocul 2: $\sigma^2_\varepsilon | \mu, Y_n \sim IG(a_0 + \frac n2, b_0 + \frac12\sum_t(y_t - \mu_t)^2)$; $\sigma^2_\eta | \mu \sim IG(a_0 + \frac{n-1}{2}, b_0 + \frac12\sum_t(\Delta\mu_t)^2)$'),
    (T(r'Prior $IG(2.5, 0.25)$ for both: proper, weak, and it rules out $\sigma^2_\eta = 0$ exactly',
       r'A priori $IG(2{,}5; 0{,}25)$ pentru ambele: propriu, slab și exclude exact $\sigma^2_\eta = 0$'),
     [T(r'the prior is not innocent near the boundary: a conjugate IG pushes small variances up; the non-centred parameterisation of \refFSW\ allows a normal prior on $\pm\sigma_\eta$ instead',
        r'distribuția a priori nu este neutră lîngă frontieră: un IG conjugat împinge în sus varianțele mici; parametrizarea necentrată din \refFSW\ permite în schimb o distribuție a priori Normală pentru $\pm\sigma_\eta$')]),
    T(r'Convergence: trace plots, several chains, inefficiency factor $1 + 2\sum_k\rho_k$ (Parzen weights): the number of draws worth one independent draw \refKSC',
      r'Convergența: grafice ale traiectoriilor, mai multe lanțuri, factorul de ineficiență $1 + 2\sum_k\rho_k$ (ponderi Parzen): numărul de extrageri care valorează cît o extragere independentă \refKSC')), 'small')

chart(T('Gibbs posterior of the signal-to-noise ratio', 'Distribuția a posteriori Gibbs a raportului semnal--zgomot'), 'ats_ch6_gibbs_ll', 'ATS_ch6_simulation_smoother', [
    T(r'US inflation, local level, @{gb.draws} draws after burn-in; left: posterior of $\log_{10}q$ and the ML value; right: traces of the two variances',
      r'Inflația din SUA, local level, @{gb.draws} de extrageri după perioada de ardere; stînga: distribuția a posteriori a lui $\log_{10}q$ și valoarea ML; dreapta: traiectoriile celor două varianțe')],
    h='0.65\\textheight')

interp(('the Gibbs output', 'rezultatelor Gibbs'), [
    T(r'Posterior median of $q$: @{gb.qmed}, 90\% credible interval [@{gb.qlo}; @{gb.qhi}]; ML: @{gb.mlq}',
      r'Mediana a posteriori a lui $q$: @{gb.qmed}, intervalul de credibilitate de 90\% [@{gb.qlo}; @{gb.qhi}]; ML: @{gb.mlq}'),
    T(r'Posterior means @{gb.m0} and @{gb.m1} against ML @{ll.s2e} and @{ll.s2h}: with $n = @{ll.T}$ the prior barely matters away from the boundary',
      r'Mediile a posteriori @{gb.m0} și @{gb.m1} față de ML @{ll.s2e} și @{ll.s2h}: cu $n = @{ll.T}$, a priori contează foarte puțin departe de frontieră'),
    T(r'Inefficiency factors @{gb.ie0} and @{gb.ie1}: the variance draws inherit the autocorrelation of the state draws',
      r'Factorii de ineficiență @{gb.ie0} și @{gb.ie1}: extragerile varianțelor moștenesc autocorelația extragerilor stărilor'),
    T('The interval for $q$ excludes zero: the trend of US inflation moves, but the upper end of the interval is @{gb.qratio} times the lower end', 'Intervalul pentru $q$ exclude zero: trendul inflației din SUA se mișcă, dar capătul superior al intervalului este de @{gb.qratio} ori mai mare decît cel inferior')])

D.recap(('Bayesian state space', 'spațiul stărilor bayesian'), [
    T('Gibbs: states as one block given the parameters, parameters given the states', 'Gibbs: stările ca un singur bloc, dați parametrii; parametrii, date stările'),
    T('FFBS, the DK simulation smoother and the precision sampler draw from the same distribution', 'FFBS, simulation smoother-ul DK și eșantionarea pe baza preciziei extrag din aceeași distribuție'),
    T('Priors regularise boundary problems but must be reported and varied', 'Distribuțiile a priori regularizează problemele de frontieră, dar trebuie raportate și variate')])

# =============================================================================
# 4. VOLATILITATE STOCHASTICĂ
# =============================================================================
D.section('Stochastic volatility', 'Volatilitatea stochastică')

D.frame(T('The stochastic volatility model', 'Modelul de volatilitate stochastică'), two(
    ph('shephard', T('Neil Shephard, 2004', 'Neil Shephard, 2004'), h='0.30\\textheight'),
    items(T(r'$y_t = \exp(h_t/2)\,\epsilon_t$, $\quad h_{t+1} = \mu + \phi(h_t - \mu) + \sigma_\eta\eta_t$, $\quad \epsilon_t, \eta_t \sim$ i.i.d. $N(0, 1)$ \refTay',
            r'$y_t = \exp(h_t/2)\,\epsilon_t$, $\quad h_{t+1} = \mu + \phi(h_t - \mu) + \sigma_\eta\eta_t$, $\quad \epsilon_t, \eta_t \sim$ i.i.d. $N(0, 1)$ \refTay'),
          T(r'$h_t$: log-variance, a latent AR(1) state; $\phi$: persistence; $\sigma_\eta$: volatility of volatility; $\exp(\mu/2)$: typical volatility',
            r'$h_t$: logaritmul varianței, o stare latentă AR(1); $\phi$: persistența; $\sigma_\eta$: volatilitatea volatilității; $\exp(\mu/2)$: volatilitatea tipică'),
          T(r'A state space model with a nonlinear measurement equation: the Kalman filter does not apply directly',
            r'Un model în spațiul stărilor cu ecuația de măsurare neliniară: filtrul Kalman nu se aplică direct'),
          T(r'Continuous-time counterpart: the log-variance as an Ornstein--Uhlenbeck process (option pricing, realised measures in Chapter 8)',
            r'Corespondentul în timp continuu: logaritmul varianței ca proces Ornstein--Uhlenbeck (evaluarea opțiunilor, măsurile realizate din Capitolul 8)')), '0.3', '0.68'), 'footnotesize')

D.frame(T('Stochastic volatility is not GARCH (1/2)', 'Volatilitatea stochastică nu este GARCH (1/2)'), items(
    (T(r'GARCH \refBol: $\sigma^2_t = \omega + \alpha y^2_{t-1} + \beta\sigma^2_{t-1}$, $\omega > 0$, $\alpha, \beta \ge 0$', r'GARCH \refBol: $\sigma^2_t = \omega + \alpha y^2_{t-1} + \beta\sigma^2_{t-1}$, $\omega > 0$, $\alpha, \beta \ge 0$'),
     [T(r'$\sigma^2_t$ is known at $t-1$ (a function of past returns): one source of randomness', r'$\sigma^2_t$ este cunoscută la $t-1$ (o funcție de randamentele trecute): o singură sursă de aleatoriu'),
      T(r'the likelihood is a product of known densities: one pass, exact ML', r'verosimilitatea este un produs de densități cunoscute: o singură trecere, ML exact')]),
    (T(r'SV: $h_t$ has its own shock $\eta_t$; even with all past returns, today\'s variance is uncertain',
       r'SV: $h_t$ are propriul șoc $\eta_t$; chiar cu toate randamentele trecute, varianța de azi este incertă'),
     [T(r'$p(y_{1:n} | \psi) = \int\prod_t N(y_t; 0, e^{h_t})\,p(h_{1:n} | \psi)\,dh_{1:n}$: an $n$-dimensional integral without closed form',
        r'$p(y_{1:n} | \psi) = \int\prod_t N(y_t; 0, e^{h_t})\,p(h_{1:n} | \psi)\,dh_{1:n}$: o integrală $n$-dimensională fără formă închisă')]),
    T(r'Comparison on the likelihood scale is possible only after the integral is computed: particle filter (next section) or importance sampling \refKSC',
      r'Compararea pe scala verosimilității este posibilă doar după calculul integralei: filtrul de particule (secțiunea următoare) sau eșantionarea prin importanță \refKSC')), 'small')

D.frame(T('Stochastic volatility is not GARCH (2/2)', 'Volatilitatea stochastică nu este GARCH (2/2)'), items(
    (T(r'Moments, with $\sigma^2_h = \sigma^2_\eta/(1 - \phi^2)$ the unconditional variance of $h_t$', r'Momentele, cu $\sigma^2_h = \sigma^2_\eta/(1 - \phi^2)$ varianța necondiționată a lui $h_t$'),
     [T(r'kurtosis of $y_t$: $3\exp(\sigma^2_h) > 3$ even with Gaussian $\epsilon_t$: fat tails come from the random variance', r'kurtosis-ul lui $y_t$: $3\exp(\sigma^2_h) > 3$ chiar cu $\epsilon_t$ gaussian: cozile groase provin din varianța aleatoare'),
      T(r'$\Corr(y^2_t, y^2_{t-k}) = (e^{\sigma^2_h\phi^k} - 1)/(3e^{\sigma^2_h} - 1)$: volatility clustering that decays with $\phi^k$', r'$\Corr(y^2_t, y^2_{t-k}) = (e^{\sigma^2_h\phi^k} - 1)/(3e^{\sigma^2_h} - 1)$: volatility clustering care scade odată cu $\phi^k$')]),
    T(r'Leverage enters as $\Corr(\epsilon_t, \eta_t) = \rho < 0$ \refOCSN; GARCH needs an asymmetric term for the same effect',
      r'Efectul de levier intră prin $\Corr(\epsilon_t, \eta_t) = \rho < 0$ \refOCSN; GARCH are nevoie de un termen asimetric pentru același efect')), 'small')

D.frame(T('A linear state space form: log-squared returns', 'O formă liniară în spațiul stărilor: logaritmul pătratelor randamentelor'), items(
    T(r'$y^*_t = \ln y^2_t = h_t + \xi_t$, $\xi_t = \ln\epsilon^2_t$: linear in $h_t$, but $\xi_t$ follows a $\ln\chi^2_1$ law with mean $-1.2704$ and variance $\pi^2/2 \approx 4.93$',
      r'$y^*_t = \ln y^2_t = h_t + \xi_t$, $\xi_t = \ln\epsilon^2_t$: liniar în $h_t$, dar $\xi_t$ are o lege $\ln\chi^2_1$ cu media $-1{,}2704$ și varianța $\pi^2/2 \approx 4{,}93$'),
    (T(r'QML \refHRS: run the Kalman filter as if $\xi_t$ were $N(-1.2704, \pi^2/2)$; consistent, but inefficient',
       r'QML \refHRS: rulăm filtrul Kalman ca și cum $\xi_t$ ar fi $N(-1{,}2704; \pi^2/2)$; consistent, dar ineficient'),
     [T(r'$y^*_t$ is ARMA(1,1): $\Corr(y^*_t, y^*_{t-k}) = \phi^k\sigma^2_h/(\sigma^2_h + \pi^2/2)$, small because the noise dominates the signal',
        r'$y^*_t$ este ARMA(1,1): $\Corr(y^*_t, y^*_{t-k}) = \phi^k\sigma^2_h/(\sigma^2_h + \pi^2/2)$, mică pentru că zgomotul domină semnalul')]),
    T(r'Zero returns: $\ln 0 = -\infty$; use $y^*_t = \ln(y^2_t + c)$ with a small offset $c$ (here $c = 10^{-3}\Var(y)$, scaled to the series)',
      r'Randamentele nule: $\ln 0 = -\infty$; folosim $y^*_t = \ln(y^2_t + c)$ cu o constantă mică $c$ (aici $c = 10^{-3}\Var(y)$, scalată la serie)'),
    T(r'Multivariate extension of the same idea: factor SV models \refHRS', r'Extensia multivariată a aceleiași idei: modele SV factoriale \refHRS')), 'small')

D.frame(T('The KSC mixture: a conditionally Gaussian model', 'Mixtura KSC: un model condiționat gaussian'), cols(
    items(T(r'\refKSC: approximate $\ln\chi^2_1$ by a mixture of seven normals; given the component $s_t$, the model is linear and Gaussian',
            r'\refKSC: aproximăm $\ln\chi^2_1$ printr-o mixtură de șapte distribuții Normale; dată componenta $s_t$, modelul este liniar și gaussian'),
          T(r'$y^*_t = h_t + m_{s_t} - 1.2704 + \sqrt{v_{s_t}}\,u_t$, $u_t \sim N(0, 1)$, $P(s_t = i) = p_i$; $s_t \in \{1, \dots, 7\}$: the component; $p_i$, $m_i$, $v_i$: its probability, mean and variance (table)',
            r'$y^*_t = h_t + m_{s_t} - 1{,}2704 + \sqrt{v_{s_t}}\,u_t$, $u_t \sim N(0, 1)$, $P(s_t = i) = p_i$; $s_t \in \{1, \dots, 7\}$: componenta; $p_i$, $m_i$, $v_i$: probabilitatea, media și varianța ei (tabelul)'),
          T(r'Mixture mean @{ks.mean} and variance @{ks.var}, against $-1.2704$ and 4.935 for the exact law',
            r'Media mixturii @{ks.mean} și varianța @{ks.var}, față de $-1{,}2704$ și 4,935 pentru legea exactă'),
          T(r'The residual approximation error can be removed by reweighting the draws (importance weights) \refKSC; finer 10-component mixtures \refOCSN',
            r'Eroarea de aproximare rămasă se poate elimina prin reponderarea extragerilor (ponderi de importanță) \refKSC; mixturi mai fine cu 10 componente \refOCSN')),
    table('cccc', r'$i$ & $p_i$ & $m_i$ & $v_i$',
          [r'1 & $0.00730$ & $-10.12999$ & $5.79596$', r'2 & $0.10556$ & $-3.97281$ & $2.61369$', r'3 & $0.00002$ & $-8.56686$ & $5.17950$', r'4 & $0.04395$ & $2.77786$ & $0.16735$', r'5 & $0.34001$ & $0.61942$ & $0.64009$', r'6 & $0.24566$ & $1.79518$ & $0.34023$', r'7 & $0.25750$ & $-1.08819$ & $1.26261$'], size='scriptsize') + items(T(r'Source: \refKSC, Table 4', r'Sursa: \refKSC, tabelul 4')),
    '0.55', '0.42'), 'footnotesize')

chart(T('The log chi-square law and its approximations', 'Legea log chi-pătrat și aproximările ei'), 'ats_ch6_ksc', 'ATS_ch6_stochastic_volatility', [
    T(r'Left: density of $\ln\epsilon^2$ (exact), the KSC mixture and the normal with the same two moments used by QML; right: the two approximation errors',
      r'Stînga: densitatea lui $\ln\epsilon^2$ (exactă), mixtura KSC și distribuția Normală cu aceleași două momente folosită de QML; dreapta: cele două erori de aproximare')],
    h='0.65\\textheight')

interp(('the mixture approximation', 'aproximării prin mixtură'), [
    T(r'The law is strongly skewed to the left: small returns produce very negative $\ln y^2_t$; the normal approximation misses both the skew and the peak',
      r'Legea are o asimetrie puternică la stînga: randamentele mici produc valori foarte negative pentru $\ln y^2_t$; aproximarea prin distribuția Normală ratează atît asimetria, cît și vîrful'),
    T(r'Largest density error: @{ks.errm} for the mixture, @{ks.errg} for the normal (QML)',
      r'Cea mai mare eroare a densității: @{ks.errm} pentru mixtură, @{ks.errg} pentru distribuția Normală (QML)'),
    T(r'QML treats a skewed noise as symmetric: the filter overreacts to near-zero returns; the mixture fixes this at the cost of one extra Gibbs block',
      r'QML tratează un zgomot asimetric ca pe unul simetric: filtrul reacționează excesiv la randamentele apropiate de zero; mixtura corectează acest lucru cu prețul unui bloc Gibbs suplimentar')])

D.frame(T('Gibbs sampling of the SV model', 'Eșantionarea Gibbs a modelului SV'), items(
    T(r'Block 1: $s_t | y^*_t, h_t$ independently, $P(s_t = i) \propto p_i\,N(y^*_t - h_t;\ m_i - 1.2704, v_i)$',
      r'Blocul 1: $s_t | y^*_t, h_t$ independent, $P(s_t = i) \propto p_i\,N(y^*_t - h_t;\ m_i - 1{,}2704, v_i)$'),
    T(r'Block 2: $h_{1:n} | s, \psi, y^*$ in one draw: a linear Gaussian model with known time-varying measurement variances $v_{s_t}$ (precision sampler or DK)',
      r'Blocul 2: $h_{1:n} | s, \psi, y^*$ într-o singură extragere: un model liniar gaussian cu varianțe de măsurare cunoscute și variabile în timp $v_{s_t}$ (precizie sau DK)'),
    T(r'Block 3: $\sigma^2_\eta | h, \mu, \phi$ inverse gamma; $\phi$ by Metropolis--Hastings with the AR(1) regression as proposal; $\mu$ normal',
      r'Blocul 3: $\sigma^2_\eta | h, \mu, \phi$ invers gamma; $\phi$ prin Metropolis--Hastings, cu regresia AR(1) ca propunere; $\mu$ din distribuția Normală'),
    T(r'Priors \refKSC: $(\phi + 1)/2 \sim \mathrm{Beta}(20, 1.5)$, $\sigma^2_\eta \sim IG(2.5, 0.025)$, $\mu \sim N(0, 10)$',
      r'Distribuțiile a priori \refKSC: $(\phi + 1)/2 \sim \mathrm{Beta}(20; 1{,}5)$, $\sigma^2_\eta \sim IG(2{,}5; 0{,}025)$, $\mu \sim N(0, 10)$'),
    T(r'Single-move samplers (one $h_t$ at a time, \refJPR) mix very slowly because consecutive $h_t$ are highly correlated: sample the path as a block',
      r'Eșantionatoarele cu o singură mișcare (cîte un $h_t$, \refJPR) au o amestecare (mixing) foarte lentă, pentru că valorile consecutive $h_t$ sînt puternic corelate: eșantionați traiectoria ca bloc')), 'small')

chart(T('Stochastic volatility of the S\\&P 500 and the BET', 'Volatilitatea stochastică pentru S\\&P 500 și BET'), 'ats_ch6_sv', 'ATS_ch6_stochastic_volatility', [
    T(r'Daily log returns in \%, demeaned, 2016--2026 ($T = @{sv.sp500.T}$ and @{sv.bet.T}); KSC Gibbs sampler, @{sv.draws} draws; GARCH(1,1) by ML on the same data',
      r'Randamente logaritmice zilnice în \%, centrate, 2016--2026 ($T = @{sv.sp500.T}$ și @{sv.bet.T}); eșantionatorul Gibbs KSC, @{sv.draws} de extrageri; GARCH(1,1) prin ML pe aceleași date')],
    h='0.65\\textheight')

D.frame(T('Interpreting the SV estimates', 'Interpretarea estimațiilor SV'), table(
    'lcccccc', T('Index', 'Indice') + r' & $\phi$ & $\sigma_\eta$ & $\mu$ & ' + T('ineff.', 'inef.') + r' $\phi$, $\sigma_\eta$ & GARCH $\alpha + \beta$ & ' + T('corr. vol.', 'corel. vol.'),
    [r'S\&P 500 & @{sv.sp500.phi} & @{sv.sp500.sig} & @{sv.sp500.mu} & @{sv.sp500.phi.ie} / @{sv.sp500.sig.ie} & @{sv.sp500.ab} & @{sv.sp500.corr}',
     r'BET & @{sv.bet.phi} & @{sv.bet.sig} & @{sv.bet.mu} & @{sv.bet.phi.ie} / @{sv.bet.sig.ie} & @{sv.bet.ab} & @{sv.bet.corr}'],
    size='footnotesize') + items(
    T(r'90\% intervals for $\phi$: [@{sv.sp500.phi.lo}; @{sv.sp500.phi.hi}] (S\&P 500), [@{sv.bet.phi.lo}; @{sv.bet.phi.hi}] (BET): very persistent log-variance, as in \refKSC',
      r'Intervalele de 90\% pentru $\phi$: [@{sv.sp500.phi.lo}; @{sv.sp500.phi.hi}] (S\&P 500), [@{sv.bet.phi.lo}; @{sv.bet.phi.hi}] (BET): logaritmul varianței este foarte persistent, ca în \refKSC'),
    T(r'The two volatility paths are close (correlation in the last column), but SV reacts less to a single large return than GARCH, whose variance jumps by $\alpha y^2_{t-1}$',
      r'Cele două traiectorii ale volatilității sînt apropiate (corelația din ultima coloană), dar SV reacționează mai puțin decît GARCH la un singur randament mare, la care varianța GARCH sare cu $\alpha y^2_{t-1}$'),
    T(r'Large inefficiency factors for $\sigma_\eta$ are typical: $\sigma_\eta$ and the path $h_{1:n}$ are strongly dependent; long chains or interweaving are needed',
      r'Factorii de ineficiență mari pentru $\sigma_\eta$ sînt tipici: $\sigma_\eta$ și traiectoria $h_{1:n}$ sînt puternic dependente; sînt necesare lanțuri lungi sau tehnici de interweaving'),
    T(r'Kurtosis of returns: @{sv.sp500.kurt} (S\&P 500) and @{sv.bet.kurt} (BET); with Gaussian $\epsilon_t$, SV explains only part of it (SV-$t$ errors are the usual extension)',
      r'Kurtosis-ul randamentelor: @{sv.sp500.kurt} (S\&P 500) și @{sv.bet.kurt} (BET); cu $\epsilon_t$ gaussian, SV explică doar o parte (extensia uzuală: erori SV-$t$)')), 'footnotesize')

D.recap(('Stochastic volatility', 'volatilitatea stochastică'), [
    T('SV adds a shock to the variance: its likelihood is an integral over the volatility path', 'SV adaugă un șoc varianței: verosimilitatea este o integrală după traiectoria volatilității'),
    T('Log-squared returns make the model linear; the KSC mixture makes it conditionally Gaussian, so the whole path can be drawn in one block', 'Logaritmul pătratelor randamentelor face modelul liniar; mixtura KSC îl face condiționat gaussian, deci întreaga traiectorie se poate extrage într-un singur bloc'),
    T('On daily index returns SV and GARCH give similar volatility paths but different reactions to single large returns', 'Pe randamentele zilnice ale indicilor, SV și GARCH dau traiectorii apropiate ale volatilității, dar reacții diferite la un singur randament mare')])

# =============================================================================
# 5. FILTRARE NELINIARĂ
# =============================================================================
D.section('Nonlinear and non-Gaussian filtering', 'Filtrarea neliniară și negaussiană')

D.frame(T('The Bayes filter', 'Filtrul Bayes'), items(
    T(r'General model: $y_t \sim g(y_t | x_t, \psi)$, $x_t \sim f(x_t | x_{t-1}, \psi)$; $g$: measurement density, $f$: transition density, $x_t$: the state; target $p(x_t | Y_t)$ and $p(y_t | Y_{t-1})$',
      r'Modelul general: $y_t \sim g(y_t | x_t, \psi)$, $x_t \sim f(x_t | x_{t-1}, \psi)$; $g$: densitatea de măsurare, $f$: densitatea de tranziție, $x_t$: starea; ținta: $p(x_t | Y_t)$ și $p(y_t | Y_{t-1})$'),
    T(r'Prediction: $p(x_t | Y_{t-1}) = \int f(x_t | x_{t-1})\,p(x_{t-1} | Y_{t-1})\,dx_{t-1}$',
      r'Predicția: $p(x_t | Y_{t-1}) = \int f(x_t | x_{t-1})\,p(x_{t-1} | Y_{t-1})\,dx_{t-1}$'),
    T(r'Update: $p(x_t | Y_t) = g(y_t | x_t)\,p(x_t | Y_{t-1}) / p(y_t | Y_{t-1})$, $\quad p(y_t | Y_{t-1}) = \int g(y_t | x_t)\,p(x_t | Y_{t-1})\,dx_t$',
      r'Actualizarea: $p(x_t | Y_t) = g(y_t | x_t)\,p(x_t | Y_{t-1}) / p(y_t | Y_{t-1})$, $\quad p(y_t | Y_{t-1}) = \int g(y_t | x_t)\,p(x_t | Y_{t-1})\,dx_t$'),
    (T(r'Closed form only in two cases: linear Gaussian (Kalman) and finite state spaces (the Hamilton filter of Markov switching, Chapter 7)',
       r'Formă închisă doar în două cazuri: liniar gaussian (Kalman) și spații finite de stări (filtrul Hamilton al modelelor Markov switching, Capitolul 7)'),
     [T('otherwise: approximate the model (EKF), approximate the densities by points (UKF), or by weighted samples (particle filters)',
        'altfel: aproximăm modelul (EKF), aproximăm densitățile prin puncte (UKF) sau prin eșantioane ponderate (filtre de particule)')])), 'small')

D.frame(T('The extended Kalman filter', 'Filtrul Kalman extins'), items(
    T(r'Nonlinear model $y_t = Z(x_t) + \varepsilon_t$, $x_{t+1} = T(x_t) + R\eta_t$: linearise around the current estimates, $\dot Z_t = \partial Z/\partial x\,|_{a_t}$, $\dot T_t = \partial T/\partial x\,|_{a_{t|t}}$',
      r'Modelul neliniar $y_t = Z(x_t) + \varepsilon_t$, $x_{t+1} = T(x_t) + R\eta_t$: liniarizăm în jurul estimațiilor curente, $\dot Z_t = \partial Z/\partial x\,|_{a_t}$, $\dot T_t = \partial T/\partial x\,|_{a_{t|t}}$'),
    T(r'Run the Kalman recursions with $\dot Z_t, \dot T_t$ for the variances and the exact functions for the means \refDK, Section 10.2',
      r'Rulăm recursiile Kalman cu $\dot Z_t, \dot T_t$ pentru varianțe și cu funcțiile exacte pentru medii \refDK, secțiunea 10.2'),
    (T(r'A failure that teaches: in SV, $\E(y_t | h_t) = 0$ for every $h_t$, so $\partial\E(y_t | h_t)/\partial h_t = 0$: the EKF gain is zero and the filter never learns $h_t$',
       r'Un eșec instructiv: în SV, $\E(y_t | h_t) = 0$ pentru orice $h_t$, deci $\partial\E(y_t | h_t)/\partial h_t = 0$: cîștigul EKF este zero, iar filtrul nu învață niciodată $h_t$'),
     [T(r'the information about $h_t$ is in $y^2_t$, a second moment; linearisation keeps only first moments',
        r'informația despre $h_t$ se află în $y^2_t$, un moment de ordinul doi; liniarizarea păstrează doar momentele de ordinul întîi')]),
    T(r'Rule: transform the model first ($\ln y^2_t$), or use a method that propagates the whole distribution',
      r'Regula: transformăm întîi modelul ($\ln y^2_t$) sau folosim o metodă care propagă întreaga distribuție')), 'small')

D.frame(T('The unscented Kalman filter', 'Filtrul Kalman unscented'), items(
    (T(r'Unscented transform \refJU: $N(m, P)$ in $n$ dimensions is represented by $2n + 1$ sigma points', r'Transformarea unscented \refJU: $N(m, P)$ în $n$ dimensiuni este reprezentată prin $2n + 1$ puncte sigma'),
     [T(r'$\mathcal X_0 = m$, $\mathcal X_{\pm i} = m \pm (\sqrt{(n + \lambda)P})_i$; $(\sqrt{A})_i$: the $i$-th column of a matrix square root', r'$\mathcal X_0 = m$, $\mathcal X_{\pm i} = m \pm (\sqrt{(n + \lambda)P})_i$; $(\sqrt{A})_i$: coloana $i$ a unei rădăcini pătrate a matricei'),
      T(r'weights $w_0 = \lambda/(n + \lambda)$, $w_{\pm i} = 1/(2(n + \lambda))$; $\lambda$: a spread parameter', r'ponderile $w_0 = \lambda/(n + \lambda)$, $w_{\pm i} = 1/(2(n + \lambda))$; $\lambda$: un parametru de împrăștiere'),
      T(r'push each point through $g$ and take weighted means and covariances', r'trecem fiecare punct prin $g$ și calculăm medii și covarianțe ponderate')]),
    T(r'Exact for the mean to second order of the Taylor expansion of $g$ (the EKF: first order); no Jacobians needed',
      r'Exactă pentru medie pînă la ordinul doi al dezvoltării Taylor a lui $g$ (EKF: ordinul întîi); nu sînt necesari iacobieni'),
    T(r'UKF: apply the transform in the prediction and in the update step; cost similar to the EKF',
      r'UKF: aplicăm transformarea în pasul de predicție și în cel de actualizare; cost similar cu EKF'),
    T(r'Still Gaussian at each step: multimodal or heavy-tailed filtering densities need particles',
      r'Rămîne gaussian la fiecare pas: densitățile de filtrare multimodale sau cu cozi groase cer particule')), 'small')

chart(T('Linearisation against the unscented transform', 'Liniarizarea față de transformarea unscented'), 'ats_ch6_ukf', 'ATS_ch6_nonlinear_filters', [
    T(r'Volatility from log-variance: mean and s.d. of $\exp(h/2)$ for $h \sim N(0, s^2)$; exact lognormal moments, first-order linearisation (EKF) and the unscented transform with three sigma points',
      r'Volatilitatea din logaritmul varianței: media și abaterea standard a lui $\exp(h/2)$ pentru $h \sim N(0, s^2)$; momentele lognormale exacte, liniarizarea de ordinul întîi (EKF) și transformarea unscented cu trei puncte sigma')],
    h='0.65\\textheight')

interp(('the unscented transform', 'transformării unscented'), [
    T(r'At $s = 1$: exact mean @{uk.ex_m}, linearisation @{uk.lin_m}, unscented @{uk.ut_m}; exact s.d. @{uk.ex_sd}, linearisation @{uk.lin_sd}, unscented @{uk.ut_sd}',
      r'Pentru $s = 1$: media exactă @{uk.ex_m}, liniarizarea @{uk.lin_m}, unscented @{uk.ut_m}; abaterea standard exactă @{uk.ex_sd}, liniarizarea @{uk.lin_sd}, unscented @{uk.ut_sd}'),
    T('Linearisation ignores the convexity of $\\exp$: it underestimates expected volatility, more so when $h$ is uncertain', 'Liniarizarea ignoră convexitatea funcției $\\exp$: subestimează volatilitatea așteptată, cu atît mai mult cu cît $h$ este mai incert'),
    T('Three sigma points capture the convexity almost exactly for the mean; the variance is off for large $s$', 'Trei puncte sigma surprind convexitatea aproape exact pentru medie; varianța se abate pentru valori mari ale lui $s$'),
    T('Same bias in practice: an EKF forecast of volatility or of an option price is too low when the state is uncertain', 'Aceeași deplasare apare în practică: o prognoză EKF a volatilității sau a prețului unei opțiuni este prea mică atunci cînd starea este incertă')])

D.frame(T('Particle filters', 'Filtre de particule'), two(
    ph('ulam', T('Stanisław Ulam with the FERMIAC, a Monte Carlo device', 'Stanisław Ulam cu FERMIAC, un dispozitiv Monte Carlo'), h='0.32\\textheight'),
    items(T(r'Represent $p(x_t | Y_t)$ by particles $x^{(i)}_t$ with weights $W^{(i)}_t$, $i = 1, \dots, N$; Monte Carlo goes back to Ulam and Metropolis (1949)',
            r'Reprezentăm $p(x_t | Y_t)$ prin particule $x^{(i)}_t$ cu ponderi $W^{(i)}_t$, $i = 1, \dots, N$; metoda Monte Carlo provine de la Ulam și Metropolis (1949)'),
          (T(r'Bootstrap filter \refGSS, \refKit', r'Filtrul bootstrap \refGSS, \refKit'),
           [T(r'propagate: $x^{(i)}_t \sim f(\cdot | x^{(i)}_{t-1})$', r'propagăm: $x^{(i)}_t \sim f(\cdot | x^{(i)}_{t-1})$'),
            T(r'weight: $w^{(i)}_t = g(y_t | x^{(i)}_t)$', r'ponderăm: $w^{(i)}_t = g(y_t | x^{(i)}_t)$'),
            T(r'resample $N$ particles with probabilities $W^{(i)}_t \propto w^{(i)}_t$', r'reeșantionăm $N$ particule cu probabilitățile $W^{(i)}_t \propto w^{(i)}_t$')]),
          T(r'Without resampling the weights degenerate (one particle takes all the weight); effective sample size $\mathrm{ESS}_t = 1/\sum_i(W^{(i)}_t)^2$',
            r'Fără reeșantionare ponderile degenerează (o singură particulă preia toată ponderea); mărimea efectivă a eșantionului $\mathrm{ESS}_t = 1/\sum_i(W^{(i)}_t)^2$'),
          T(r'Systematic resampling: one uniform $U$, points $(U + i - 1)/N$ on the cumulative weights: lower variance than multinomial',
            r'Reeșantionarea sistematică: o singură variabilă uniformă $U$, punctele $(U + i - 1)/N$ pe ponderile cumulate: varianță mai mică decît reeșantionarea multinomială')), '0.3', '0.68'), 'footnotesize')

D.frame(T('The particle likelihood', 'Verosimilitatea din filtrul de particule'), items(
    T(r'$\hat p(y_t | Y_{t-1}) = \frac1N\sum_i w^{(i)}_t$ and $\hat L(\psi) = \prod_t\hat p(y_t | Y_{t-1})$',
      r'$\hat p(y_t | Y_{t-1}) = \frac1N\sum_i w^{(i)}_t$ și $\hat L(\psi) = \prod_t\hat p(y_t | Y_{t-1})$'),
    (T(r'$\E\hat L(\psi) = L(\psi)$ exactly, for any $N \ge 1$ \refDM (Appendix)  % applink: unbiasedness of the particle likelihood',
       r'$\E\hat L(\psi) = L(\psi)$ exact, pentru orice $N \ge 1$ \refDM (Anexa)  % applink: nedeplasarea verosimilității'),
     [T(r'$\hat L$ is unbiased on the level scale', r'$\hat L$ este nedeplasat pe scala nivelului'),
      T(r'not on the log scale: if $\ln\hat L \approx N(\ln L - \tau^2/2, \tau^2)$, then $\E\ln\hat L = \ln L - \tau^2/2$; $\tau^2 = \Var\ln\hat L$',
        r'nu și pe scala logaritmică: dacă $\ln\hat L \approx N(\ln L - \tau^2/2, \tau^2)$, atunci $\E\ln\hat L = \ln L - \tau^2/2$; $\tau^2 = \Var\ln\hat L$')]),
    T(r'$\Var\ln\hat L$ grows roughly linearly in $n$ and falls like $1/N$: double the sample, double the particles',
      r'$\Var\ln\hat L$ crește aproximativ liniar în $n$ și scade ca $1/N$: un eșantion de două ori mai lung cere de două ori mai multe particule'),
    T(r'$\hat L(\psi)$ is not smooth in $\psi$ (resampling is discontinuous): do not maximise it by gradient methods; use it inside MCMC',
      r'$\hat L(\psi)$ nu este netedă în $\psi$ (reeșantionarea este discontinuă): nu o maximizați prin metode de gradient; folosiți-o într-un MCMC')), 'small')

chart(T('Particle filter for the S\\&P 500 SV model', 'Filtrul de particule pentru modelul SV al S\\&P 500'), 'ats_ch6_pf', 'ATS_ch6_stochastic_volatility', [
    T(r'Left: filtered volatility $\E[\exp(h_t/2) | Y_t]$ (bootstrap filter, $N = 20\,000$, Gibbs posterior mean of $\psi$) against GARCH(1,1) and the smoothed SV path, last two years; right: log-likelihood estimates, @{pf.reps} runs per $N$',
      r'Stînga: volatilitatea filtrată $\E[\exp(h_t/2) | Y_t]$ (filtrul bootstrap, $N = 20\,000$, media a posteriori Gibbs pentru $\psi$) față de GARCH(1,1) și traiectoria SV netezită, ultimii doi ani; dreapta: estimații ale log-verosimilității, cîte @{pf.reps} de rulări pentru fiecare $N$')],
    h='0.61\\textheight')

interp(('the particle filter', 'filtrului de particule'), [
    T(r'Monte Carlo s.d. of $\ln\hat L$: @{pf.sd100} ($N = 100$), @{pf.sd500} ($N = 500$), @{pf.sd2000} ($N = 2000$); small $N$ also biases $\ln\hat L$ downwards',
      r'Abaterea standard Monte Carlo a lui $\ln\hat L$: @{pf.sd100} ($N = 100$), @{pf.sd500} ($N = 500$), @{pf.sd2000} ($N = 2000$); un $N$ mic deplasează și $\ln\hat L$ în jos'),
    T(r'SV log-likelihood @{pf.llsv} against the GARCH(1,1) maximum @{pf.llga}: a difference of @{pf.dll} with the same number of parameters',
      r'Log-verosimilitatea SV @{pf.llsv} față de maximul GARCH(1,1) @{pf.llga}: o diferență de @{pf.dll} cu același număr de parametri'),
    T(r'The comparison favours SV even at the posterior mean (not the maximum) of its likelihood; \refKSC\ compare SV with ARCH models on the same likelihood scale',
      r'Comparația favorizează SV chiar și la media a posteriori (nu la maximul) verosimilității sale; \refKSC\ compară SV cu modelele ARCH pe aceeași scală a verosimilității'),
    T(r'The filtered SV volatility is a one-sided estimate, like GARCH: correlation @{pf.corr}; the smoothed path anticipates turning points because it uses future data',
      r'Volatilitatea SV filtrată este o estimație unilaterală, ca GARCH: corelația @{pf.corr}; traiectoria netezită anticipează punctele de întoarcere pentru că folosește date viitoare'),
    T(r'Effective sample size over the sample: minimum @{pf.essmin}, median @{pf.essmed} of 20\,000 particles', r'Mărimea efectivă a eșantionului pe parcursul eșantionului: minimum @{pf.essmin}, mediana @{pf.essmed} din 20\,000 de particule')], 'footnotesize')

D.frame(T('The auxiliary particle filter', 'Filtrul de particule auxiliar'), items(
    T(r'Bootstrap weakness: particles are propagated blind to $y_t$; an outlier leaves few particles with weight',
      r'Slăbiciunea filtrului bootstrap: particulele sînt propagate fără a ține cont de $y_t$; o valoare extremă lasă puține particule cu pondere'),
    (T(r'APF \refPS: look ahead before propagating', r'APF \refPS: privim înainte de propagare'),
     [T(r'first stage: resample $x^{(i)}_{t-1}$ with weights $\propto W^{(i)}_{t-1}\,g(y_t | \mu^{(i)}_t)$, $\mu^{(i)}_t = \E(x_t | x^{(i)}_{t-1})$', r'prima etapă: reeșantionăm $x^{(i)}_{t-1}$ cu ponderi $\propto W^{(i)}_{t-1}\,g(y_t | \mu^{(i)}_t)$, $\mu^{(i)}_t = \E(x_t | x^{(i)}_{t-1})$'),
      T(r'second stage: propagate, then weight by $g(y_t | x^{(i)}_t)/g(y_t | \mu^{(k_i)}_t)$ to correct the look-ahead',
        r'a doua etapă: propagăm, apoi ponderăm cu $g(y_t | x^{(i)}_t)/g(y_t | \mu^{(k_i)}_t)$ pentru a corecta privirea înainte'),
      T(r'$k_i$: the index of the particle selected in the first stage', r'$k_i$: indicele particulei alese în prima etapă')]),
    T(r'Fully adapted case: first-stage weights $p(y_t | x_{t-1})$ and proposal $p(x_t | x_{t-1}, y_t)$: second-stage weights are equal (locally optimal)',
      r'Cazul complet adaptat: ponderi în prima etapă $p(y_t | x_{t-1})$ și propunerea $p(x_t | x_{t-1}, y_t)$: ponderile din etapa a doua sînt egale (optim local)'),
    T(r'The likelihood estimate stays unbiased: $\hat p(y_t | Y_{t-1}) = \big(\sum_iW^{(i)}_{t-1}g(y_t | \mu^{(i)}_t)\big)\cdot\frac1N\sum_i\omega^{(i)}_t$; $\omega^{(i)}_t$: the second-stage weights',
      r'Estimația verosimilității rămîne nedeplasată: $\hat p(y_t | Y_{t-1}) = \big(\sum_iW^{(i)}_{t-1}g(y_t | \mu^{(i)}_t)\big)\cdot\frac1N\sum_i\omega^{(i)}_t$; $\omega^{(i)}_t$: ponderile din etapa a doua')), 'small')

chart(T('Particle likelihoods against the exact Kalman likelihood', 'Verosimilitățile din filtrele de particule față de verosimilitatea Kalman exactă'), 'ats_ch6_pf_check', 'ATS_ch6_nonlinear_filters', [
    T(r'Local level model for US inflation at the ML variances: error of $\ln\hat L$ (given $y_1$) for the bootstrap and the auxiliary filter, @{pc.reps} runs per $N$',
      r'Modelul local level pentru inflația din SUA, la varianțele ML: eroarea lui $\ln\hat L$ (condiționat de $y_1$) pentru filtrul bootstrap și pentru cel auxiliar, cîte @{pc.reps} de rulări pentru fiecare $N$')],
    h='0.65\\textheight')

interp(('the particle check', 'verificării filtrelor de particule'), [
    T(r'Mean error of $\ln\hat L$: @{pc.b50.m}, @{pc.b200.m}, @{pc.b1000.m} (bootstrap, $N = 50, 200, 1000$) and @{pc.a50.m}, @{pc.a200.m}, @{pc.a1000.m} (auxiliary)',
      r'Eroarea medie a lui $\ln\hat L$: @{pc.b50.m}, @{pc.b200.m}, @{pc.b1000.m} (bootstrap, $N = 50, 200, 1000$) și @{pc.a50.m}, @{pc.a200.m}, @{pc.a1000.m} (auxiliar)'),
    T(r'Standard deviations: @{pc.b1000.s} (bootstrap) and @{pc.a1000.s} (auxiliary) at $N = 1000$: the look-ahead buys precision because the signal-to-noise ratio is high',
      r'Abaterile standard: @{pc.b1000.s} (bootstrap) și @{pc.a1000.s} (auxiliar) pentru $N = 1000$: privirea înainte crește precizia, pentru că raportul semnal--zgomot este mare'),
    T(r'The negative mean is the Jensen bias of a log of an unbiased estimator: it shrinks like $\Var(\ln\hat L)/2$',
      r'Media negativă este deplasarea Jensen a logaritmului unui estimator nedeplasat: scade ca $\Var(\ln\hat L)/2$'),
    T('Always test a particle filter on a model with a known likelihood before using it where none is available', 'Testați întotdeauna un filtru de particule pe un model cu verosimilitate cunoscută înainte de a-l folosi acolo unde aceasta nu este disponibilă')])

D.frame(T('Particle MCMC', 'Particle MCMC'), items(
    T(r'Pseudo-marginal idea \refAR: run Metropolis--Hastings with an unbiased, positive estimate $\hat L(\psi)$ in place of $L(\psi)$; the chain still targets the exact posterior $p(\psi | Y_n)$',
      r'Ideea pseudo-marginală \refAR: rulăm Metropolis--Hastings cu o estimație nedeplasată și pozitivă $\hat L(\psi)$ în locul lui $L(\psi)$; lanțul are ca țintă tot distribuția a posteriori exactă $p(\psi | Y_n)$'),
    (T(r'PMMH \refADH', r'PMMH \refADH'),
     [T(r'propose $\psi\'$ from a proposal density $q(\cdot | \psi)$; run a particle filter for $\hat L(\psi\')$', r'propunem $\psi\'$ din densitatea de propunere $q(\cdot | \psi)$; rulăm un filtru de particule pentru $\hat L(\psi\')$'),
      T(r'accept with probability $\min\{1, \hat L(\psi\')p(\psi\')q(\psi | \psi\') / [\hat L(\psi)p(\psi)q(\psi\' | \psi)]\}$; $p(\cdot)$: the prior', r'acceptăm cu probabilitatea $\min\{1, \hat L(\psi\')p(\psi\')q(\psi | \psi\') / [\hat L(\psi)p(\psi)q(\psi\' | \psi)]\}$; $p(\cdot)$: distribuția a priori'),
      T(r'keep $\hat L$ of the current point (do not recompute it)', r'păstrăm $\hat L$ al punctului curent (nu îl recalculăm)')]),
    (T(r'Choosing $N$ \refPSGK, \refDPDK', r'Alegerea lui $N$ \refPSGK, \refDPDK'),
     [T('too few particles make the chain stick; too many waste time', 'prea puține particule blochează lanțul; prea multe irosesc timpul'),
      T(r'target: $\Var(\ln\hat L) \approx 1$--$2$ at the posterior mean', r'ținta: $\Var(\ln\hat L) \approx 1$--$2$ la media a posteriori'),
      T('particle Gibbs (conditional SMC) samples the state path too; useful when no conditionally Gaussian structure exists',
        'particle Gibbs (SMC condiționat) eșantionează și traiectoria stării; util atunci cînd nu există o structură condiționat gaussiană')]),
    T(r'Works for any model you can simulate and whose measurement density you can evaluate: SV with jumps, DSGE models, nonlinear UC models',
      r'Funcționează pentru orice model pe care îl puteți simula și a cărui densitate de măsurare o puteți evalua: SV cu salturi, modele DSGE, modele UC neliniare')), 'small')

chart(T('PMMH against the KSC Gibbs sampler', 'PMMH față de eșantionatorul Gibbs KSC'), 'ats_ch6_pmmh', 'ATS_ch6_stochastic_volatility', [
    T(r'Last @{pm.n} S\&P 500 returns; PMMH with a bootstrap filter of $N = @{pm.N}$ particles, @{pm.iter} iterations, random walk on $(\mu, \operatorname{atanh}\phi, \ln\sigma_\eta)$; Gibbs with the KSC mixture',
      r'Ultimele @{pm.n} de randamente S\&P 500; PMMH cu un filtru bootstrap de $N = @{pm.N}$ particule, @{pm.iter} de iterații, mers aleator pe $(\mu, \operatorname{atanh}\phi, \ln\sigma_\eta)$; Gibbs cu mixtura KSC')],
    h='0.65\\textheight')

interp(('the PMMH run', 'rulării PMMH'), [
    T(r'Posterior means of $\phi$: @{pm.g.phi} (Gibbs) and @{pm.p.phi} (PMMH); of $\sigma_\eta$: @{pm.g.sig} and @{pm.p.sig}; posterior s.d. @{pm.gs.sig} and @{pm.ps.sig}',
      r'Mediile a posteriori ale lui $\phi$: @{pm.g.phi} (Gibbs) și @{pm.p.phi} (PMMH); ale lui $\sigma_\eta$: @{pm.g.sig} și @{pm.p.sig}; abaterile standard a posteriori @{pm.gs.sig} și @{pm.ps.sig}'),
    T(r'Two exact algorithms, one posterior: the KSC mixture approximation has no visible effect here',
      r'Doi algoritmi exacți, aceeași distribuție a posteriori: aproximarea prin mixtura KSC nu are aici un efect vizibil'),
    T(r'$N = @{pm.N}$ gives s.d. of $\ln\hat L$ equal to @{pm.sdll} at the posterior mean, inside the recommended range; acceptance rate @{pm.acc}\%',
      r'$N = @{pm.N}$ dă o abatere standard a lui $\ln\hat L$ de @{pm.sdll} la media a posteriori, în intervalul recomandat; rata de acceptare este @{pm.acc}\%'),
    T(r'Cost: @{pm.min} minutes for PMMH against seconds for Gibbs: use PMMH when there is no conditionally Gaussian representation',
      r'Costul: @{pm.min} minute pentru PMMH, față de cîteva secunde pentru Gibbs: folosiți PMMH cînd nu există o reprezentare condiționat gaussiană')])

D.recap(('Nonlinear filtering', 'filtrarea neliniară'), [
    T('EKF linearises the model, UKF propagates sigma points, particle filters propagate weighted samples', 'EKF liniarizează modelul, UKF propagă puncte sigma, filtrele de particule propagă eșantioane ponderate'),
    T('The particle likelihood is unbiased in levels; its log variance decides the number of particles', 'Verosimilitatea din filtrul de particule este nedeplasată în nivel; varianța logaritmului ei decide numărul de particule'),
    T('PMMH turns any simulable model into an exact Bayesian procedure, at a computational price', 'PMMH transformă orice model care poate fi simulat într-o procedură bayesiană exactă, cu un cost de calcul')])

# =============================================================================
# 6. PARAMETRI VARIABILI ÎN TIMP
# =============================================================================
D.section('Time-varying parameters', 'Parametri variabili în timp')

D.frame(T('A TVP regression in state space form', 'O regresie TVP în forma în spațiul stărilor'), items(
    (T(r'$y_t = c_t + b_tx_t + D_t\'\gamma + \varepsilon_t$, $\quad c_{t+1} = c_t + \eta_{c,t}$, $\quad b_{t+1} = b_t + \eta_{b,t}$', r'$y_t = c_t + b_tx_t + D_t\'\gamma + \varepsilon_t$, $\quad c_{t+1} = c_t + \eta_{c,t}$, $\quad b_{t+1} = b_t + \eta_{b,t}$'),
     [T(r'$c_t$, $b_t$: intercept and slope, random walks with variances $\sigma^2_c$, $\sigma^2_b$; $D_t$: dummies with fixed $\gamma$', r'$c_t$, $b_t$: termenul liber și panta, mersuri aleatoare cu varianțele $\sigma^2_c$, $\sigma^2_b$; $D_t$: variabile dummy cu $\gamma$ fix'),
      T(r'state $\alpha_t = (c_t, b_t, \gamma\')\'$; $Z_t = (1, x_t, D_t\')$', r'starea $\alpha_t = (c_t, b_t, \gamma\')\'$; $Z_t = (1, x_t, D_t\')$')]),
    (T(r'Fixed coefficients ($\gamma$, here quarterly seasonal dummies) are states with zero variance and a diffuse start: $d$ = number of states = 5',
       r'Coeficienții ficși ($\gamma$, aici variabile dummy sezoniere trimestriale) sînt stări cu varianță zero și start difuz: $d$ = numărul stărilor = 5'),
     [T(r'with $\sigma^2_c = \sigma^2_b = 0$ the smoother returns the OLS estimates (recursive least squares)', r'cu $\sigma^2_c = \sigma^2_b = 0$, netezitorul dă estimațiile OLS (cele mai mici pătrate recursive)')]),
    T(r'Question: has the co-movement of Romanian inflation with euro-area inflation changed since inflation targeting began (2005)?',
      r'Întrebarea: s-a schimbat co-mișcarea inflației din România cu inflația din zona euro de la introducerea țintirii inflației (2005)?'),
    T(r'$y_t$: Romanian HICP inflation, quarterly, \% a.r., not seasonally adjusted; $x_t$: euro-area HICP inflation net of its seasonal pattern; @{tv.first}--@{tv.last}, $T = @{tv.T}$',
      r'$y_t$: inflația IAPC din România, trimestrial, \% anualizat, neajustată sezonier; $x_t$: inflația IAPC din zona euro fără componenta sezonieră; @{tv.first}--@{tv.last}, $T = @{tv.T}$'),
    T(r'Test of a constant slope: $H_0$: $\sigma^2_b = 0$ on the boundary; parametric bootstrap of the LR statistic from the restricted model (@{tv.B} samples)',
      r'Testul pantei constante: $H_0$: $\sigma^2_b = 0$ pe frontieră; bootstrap parametric pentru statistica LR din modelul restricționat (@{tv.B} de eșantioane)')), 'small')

chart(T('Romanian on euro-area inflation: a time-varying slope?', 'Inflația din România și inflația din zona euro: o pantă variabilă în timp?'), 'ats_ch6_tvp', 'ATS_ch6_tvp_inflation', [
    T(r'Top: the two inflation rates; bottom: smoothed $b_t$ with a 90\% band (exact diffuse ML) and the slope of a rolling 12-quarter regression with the same dummies',
      r'Sus: cele două rate ale inflației; jos: $b_t$ netezit cu o bandă de 90\% (ML difuz exact) și panta unei regresii mobile pe 12 trimestre cu aceleași variabile dummy')],
    h='0.65\\textheight')

interp(('the TVP regression', 'regresiei TVP'), [
    T(r'ML: $\hat\sigma^2_c = @{tv.s2c}$, $\hat\sigma^2_b = @{tv.s2b}$, $\hat\sigma^2_\varepsilon = @{tv.s2e}$; numpy and \texttt{statsmodels} log-likelihoods @{tv.ll} and @{tv.smll}',
      r'ML: $\hat\sigma^2_c = @{tv.s2c}$, $\hat\sigma^2_b = @{tv.s2b}$, $\hat\sigma^2_\varepsilon = @{tv.s2e}$; log-verosimilitățile numpy și \texttt{statsmodels} sînt @{tv.ll} și @{tv.smll}'),
    T(r'$b_t$ drifts from @{tv.b08} (s.e. @{tv.sb08}) in 2008Q3 to @{tv.b22} (s.e. @{tv.sb22}) in 2022Q4: a slope close to one, but no significant change',
      r'$b_t$ se deplasează de la @{tv.b08} (eroare standard @{tv.sb08}) în T3 2008 la @{tv.b22} (eroare standard @{tv.sb22}) în T4 2022: o pantă apropiată de unu, dar fără o schimbare semnificativă'),
    T(r'LR $= @{tv.LR}$; bootstrap $p = @{tv.pboot}$ (95\% quantile @{tv.q95}; @{tv.zero}\% of bootstrap statistics are exactly zero: pile-up again); the $\frac12\chi^2_1$ rule gives $p = @{tv.pmix}$',
      r'LR $= @{tv.LR}$; p-value-ul bootstrap $= @{tv.pboot}$ (cuantila de 95\% este @{tv.q95}; @{tv.zero}\% dintre statisticile bootstrap sînt exact zero: din nou pile-up); regula $\frac12\chi^2_1$ dă $p = @{tv.pmix}$'),
    T('The rolling regression swings between negative values and 1.5: that is sampling noise of 12-quarter windows, not time variation; the state space model averages it out with an explicit variance',
      'Regresia mobilă oscilează între valori negative și 1,5: acesta este zgomotul de eșantionare al ferestrelor de 12 trimestre, nu variație în timp; modelul în spațiul stărilor îl mediază printr-o varianță explicită')])

D.frame(T('TVP-VAR with stochastic volatility', 'TVP-VAR cu volatilitate stochastică'), two(
    ph('sargent', T('Thomas J. Sargent, 2011', 'Thomas J. Sargent, 2011'), h='0.36\\textheight'),
    items((T(r'\refCSa, \refCSb, \refPri: $y_t = X_t\'\beta_t + A_t^{-1}\Sigma_t\epsilon_t$', r'\refCSa, \refCSb, \refPri: $y_t = X_t\'\beta_t + A_t^{-1}\Sigma_t\epsilon_t$'),
           [T(r'$X_t$: the lags; $\beta_t$: the coefficients; $\epsilon_t \sim N(0, I)$', r'$X_t$: lagurile; $\beta_t$: coeficienții; $\epsilon_t \sim N(0, I)$'),
            T(r'$A_t$: lower triangular with free elements $a_t$; $\Sigma_t = \mathrm{diag}(\sigma_{j,t})$', r'$A_t$: inferior triunghiulară, cu elementele libere $a_t$; $\Sigma_t = \mathrm{diag}(\sigma_{j,t})$'),
            T(r'$\beta_t$, $a_t$ and $\ln\sigma_{j,t}$ follow random walks', r'$\beta_t$, $a_t$ și $\ln\sigma_{j,t}$ urmează mersuri aleatoare')]),
          T(r'Question: did US monetary policy change (drifting coefficients) or did the shocks shrink (falling volatilities) after 1980?',
            r'Întrebarea: s-a schimbat politica monetară a SUA (coeficienți care derivă) sau s-au micșorat șocurile (volatilități în scădere) după 1980?'),
          T(r'Answer of \refPri: the systematic response of policy did change, but these changes explain little of the 1970s; the variance of non-policy shocks matters more',
            r'Răspunsul din \refPri: reacția sistematică a politicii monetare s-a schimbat, dar aceste schimbări explică puțin din anii 1970; varianța șocurilor care nu țin de politica monetară contează mai mult'),
          T(r'Without stochastic volatility, falling shock variances are wrongly attributed to changing coefficients', r'Fără volatilitate stochastică, scăderea varianțelor șocurilor este atribuită greșit schimbării coeficienților')), '0.3', '0.68'), 'footnotesize')

D.frame(T('Estimating a TVP-VAR-SV', 'Estimarea unui TVP-VAR-SV'), items(
    (T('Gibbs blocks, each one of the samplers of this chapter:', 'Blocurile Gibbs, fiecare fiind unul dintre eșantionatoarele din acest capitol:'),
     [T(r'$\beta_{1:n}$ | rest: simulation smoother of a linear Gaussian model with known time-varying covariances', r'$\beta_{1:n}$ | rest: simulation smoother pentru un model liniar gaussian cu covarianțe cunoscute, variabile în timp'),
      T(r'$a_{1:n}$ | rest: equation by equation, the same smoother', r'$a_{1:n}$ | rest: ecuație cu ecuație, același netezitor'),
      T(r'$\ln\sigma_{j,1:n}$ | rest: the KSC mixture with its indicators', r'$\ln\sigma_{j,1:n}$ | rest: mixtura KSC cu indicatorii ei'),
      T(r'covariances of the random walks: inverse Wishart', r'covarianțele mersurilor aleatoare: invers Wishart')]),
    T(r'The order of the Gibbs steps matters: the original algorithm drew the mixture indicators at the wrong point of the cycle; \refDNP\ give the corrected order, and the substantive results change little',
      r'Ordinea pașilor Gibbs contează: algoritmul inițial extrăgea indicatorii mixturii într-un punct greșit al ciclului; \refDNP\ dau ordinea corectă, iar rezultatele de fond se schimbă puțin'),
    T(r'Priors from a training sample at the start of the data, as in \refPri, with small scales for the random-walk covariances: the prior decides how much variation is allowed',
      r'Distribuții a priori dintr-un eșantion de antrenare de la începutul datelor, ca în \refPri, cu scale mici pentru covarianțele mersurilor aleatoare: a priori decide cîtă variație este permisă'),
    T(r'Overparameterisation: with $k$ coefficients per equation, shrink the variances, or select which coefficients vary (non-centred parameterisation, \refFSW)',
      r'Supraparametrizarea: cu $k$ coeficienți pe ecuație, aplicăm shrinkage varianțelor sau selectăm coeficienții care variază (parametrizarea necentrată, \refFSW)')), 'small')

D.recap(('Time-varying parameters', 'parametri variabili în timp'), [
    T('A TVP regression is a state space model with $Z_t$ built from the regressors; fixed coefficients are diffuse states without shocks', 'O regresie TVP este un model în spațiul stărilor cu $Z_t$ construit din regresori; coeficienții ficși sînt stări difuze fără șocuri'),
    T('Rolling windows exaggerate time variation; test it at the boundary with a bootstrap', 'Ferestrele mobile exagerează variația în timp; testați-o la frontieră cu un bootstrap'),
    T('TVP-VAR-SV combines the simulation smoother and the KSC mixture in one Gibbs sampler', 'TVP-VAR-SV combină simulation smoother-ul și mixtura KSC într-un singur eșantionator Gibbs')])

# =============================================================================
# 7. DFM
# =============================================================================
D.section('Dynamic factor models in state space form', 'Modele cu factori dinamici în forma în spațiul stărilor')

D.frame(T('The DFM as a state space model (1/2)', 'DFM ca model în spațiul stărilor (1/2)'), items(
    (T(r'$x_{it} = \lambda_i\'f_t + e_{it}$, $\quad f_t = \Phi f_{t-1} + u_t$, $\quad e_{it} = \rho_ie_{i,t-1} + \nu_{it}$', r'$x_{it} = \lambda_i\'f_t + e_{it}$, $\quad f_t = \Phi f_{t-1} + u_t$, $\quad e_{it} = \rho_ie_{i,t-1} + \nu_{it}$'),
     [T(r'$f_t$: the factors, a VAR(1) with matrix $\Phi$; $\lambda_i$: the loadings of series $i$, stacked in $\Lambda$', r'$f_t$: factorii, un VAR(1) cu matricea $\Phi$; $\lambda_i$: ponderile factoriale ale seriei $i$, așezate în $\Lambda$'),
      T(r'$e_{it}$: idiosyncratic AR(1) errors with coefficients $\rho_i$; $u_t$, $\nu_{it}$: shocks', r'$e_{it}$: erori idiosincratice AR(1) cu coeficienții $\rho_i$; $u_t$, $\nu_{it}$: șocurile'),
      T(r'state $(f_t\', f_{t-1}\', e_t\')\'$; measurement matrix $Z = (\Lambda, 0, I)$', r'starea $(f_t\', f_{t-1}\', e_t\')\'$; matricea de măsurare $Z = (\Lambda, 0, I)$')]),
    (T('Mixed frequencies \\refMM', 'Frecvențele mixte \\refMM'),
     [T('a quarterly growth rate is a weighted sum of monthly states', 'o rată de creștere trimestrială este o sumă ponderată a stărilor lunare'),
      T('missing months are simply skipped by the filter', 'filtrul sare pur și simplu peste lunile lipsă')])), 'small')

D.frame(T('The DFM as a state space model (2/2)', 'DFM ca model în spațiul stărilor (2/2)'), items(
    (T('Estimation', 'Estimarea'),
     [T(r'two steps \refDGR: principal components give $\Lambda$, $\Phi$, $\Sigma_e$; then the Kalman smoother re-estimates $f_t$ on the full panel; consistent as $N, T \to \infty$',
        r'în doi pași \refDGR: componentele principale dau $\Lambda$, $\Phi$, $\Sigma_e$; apoi netezitorul Kalman reestimează $f_t$ pe panelul complet; consistent cînd $N, T \to \infty$'),
      T(r'ML by EM \refSS, \refBM: the E-step is the smoother, arbitrary missing patterns are allowed', r'ML prin EM \refSS, \refBM: pasul E este netezitorul, sînt permise structuri arbitrare de date lipsă'),
      T(r'large $N$: collapse the $N$ observations into an $r$-dimensional vector before filtering \refJK; the cost no longer grows with $N^3$',
        r'$N$ mare: comprimăm cele $N$ observații într-un vector de dimensiune $r$ înainte de filtrare \refJK; costul nu mai crește ca $N^3$')]),
    T(r'Nowcasting \refGRS: the ragged edge, news decomposition and real-time evaluation are in Chapter 5; this section shows the state space engine',
      r'Nowcasting \refGRS: ragged edge, descompunerea pe știri și evaluarea în timp real se află în Capitolul 5; această secțiune arată mecanismul în spațiul stărilor')), 'small')

chart(T('A one-factor model of the US coincident indicators', 'Un model cu un factor pentru indicatorii coincidenți ai SUA'), 'ats_ch6_dfm', 'ATS_ch6_dfm_ragged_edge', [
    T(r'Monthly growth of industrial production, payrolls, real income less transfers and real sales (FRED), standardised, @{fm.first}--@{fm.last}; two-step estimator, univariate treatment of the observation vector; last 36 months',
      r'Creșterea lunară a producției industriale, a numărului de salariați, a venitului real fără transferuri și a vînzărilor reale (FRED), standardizate, @{fm.first}--@{fm.last}; estimatorul în doi pași, tratarea univariată a vectorului de observații; ultimele 36 de luni')],
    h='0.61\\textheight')

interp(('the ragged edge', 'datelor incomplete la sfîrșitul eșantionului (ragged edge)'), [
    T(r'Loadings @{fm.l0}, @{fm.l1}, @{fm.l2}, @{fm.l3}; factor AR coefficient @{fm.a}: monthly growth rates have little persistence, so the factor is mostly a weighted average of the month',
      r'Încărcările factoriale @{fm.l0}, @{fm.l1}, @{fm.l2}, @{fm.l3}; coeficientul AR al factorului @{fm.a}: ratele lunare de creștere sînt puțin persistente, deci factorul este în principal o medie ponderată a lunii'),
    T(r'The last complete month is @{fm.full}: the factor s.d. is @{fm.sdfull}; in @{fm.last}, with one series of four available, it rises to @{fm.sdlast}',
      r'Ultima lună completă este @{fm.full}: abaterea standard a factorului este @{fm.sdfull}; în @{fm.last}, cu o singură serie din patru disponibilă, crește la @{fm.sdlast}'),
    T('The filter weighs each series by its signal-to-noise ratio; no series is dropped, no gap is filled by hand', 'Filtrul ponderează fiecare serie după raportul ei semnal--zgomot; nicio serie nu este eliminată, niciun gol nu este completat de mînă'),
    T('Forecasting the factor beyond the data is the same recursion with all observations missing', 'Prognoza factorului dincolo de date este aceeași recursie, cu toate observațiile lipsă')])

# =============================================================================
# 8. TREND--CICLU
# =============================================================================
D.section('Trend--cycle decompositions revisited', 'Descompuneri trend--ciclu, revizitate')

D.frame(T('Three definitions of the cycle', 'Trei definiții ale ciclului'), items(
    (T(r'Beveridge--Nelson \refBN: trend = long-horizon forecast net of drift', r'Beveridge--Nelson \refBN: trendul = prognoza pe orizont lung fără drift'),
     [T(r'$\tau^{BN}_t = y_t + \sum_{j\ge1}\E_t(\Delta y_{t+j} - \mu)$; cycle $c^{BN}_t = y_t - \tau^{BN}_t$', r'$\tau^{BN}_t = y_t + \sum_{j\ge1}\E_t(\Delta y_{t+j} - \mu)$; ciclul $c^{BN}_t = y_t - \tau^{BN}_t$'),
      T(r'$\E_t$: expectation given data to $t$; $\mu$: mean growth; the trend is where $y$ is expected to settle once the predictable growth has died out', r'$\E_t$: speranța condiționată de datele pînă la $t$; $\mu$: creșterea medie; trendul este nivelul la care se așteaptă să ajungă $y$ după ce creșterea previzibilă s-a stins'),
      T(r'for an AR(1) in growth: $c^{BN}_t = -\frac{\phi}{1 - \phi}(\Delta y_t - \mu)$; one-sided, depends on the ARMA chosen; reliable versions: \refKMW',
        r'pentru un AR(1) în creștere: $c^{BN}_t = -\frac{\phi}{1 - \phi}(\Delta y_t - \mu)$; unilateral, depinde de modelul ARMA ales; versiuni fiabile: \refKMW')]),
    T(r'Unobserved components \refCla, \refWat, \refHJ: $y_t = \tau_t + c_t$ with a random-walk (or smooth) trend and an AR(2) cycle; two-sided after smoothing',
      r'Componente neobservate \refCla, \refWat, \refHJ: $y_t = \tau_t + c_t$, cu trend mers aleator (sau neted) și ciclu AR(2); bilateral după netezire'),
    T(r'Hamilton \refHamB: $c_{t+h}$ = residual of $y_{t+h}$ on $(1, y_t, \dots, y_{t-3})$, $h = 8$ quarters; model-free and one-sided (TSA, Chapter 10)',
      r'Hamilton \refHamB: $c_{t+h}$ = reziduul regresiei lui $y_{t+h}$ pe $(1, y_t, \dots, y_{t-3})$, $h = 8$ trimestre; fără model și unilateral (TSA, Capitolul 10)'),
    T(r'For US GDP the BN cycle is small and noisy, the UC cycle large and smooth: the same data, two stories. Why?',
      r'Pentru PIB-ul SUA ciclul BN este mic și zgomotos, ciclul UC mare și neted: aceleași date, două povești. De ce?')), 'small')

D.frame(T('Unobserved components with correlated shocks', 'Componente neobservate cu șocuri corelate'), items(
    (T(r'\refMNZ, the UC-UR model', r'\refMNZ, modelul UC-UR'),
     [T(r'$y_t = \tau_t + c_t$, $\tau_t = \mu + \tau_{t-1} + \eta_t$, $c_t = \phi_1c_{t-1} + \phi_2c_{t-2} + \varepsilon_t$, $\Corr(\eta_t, \varepsilon_t) = \rho$', r'$y_t = \tau_t + c_t$, $\tau_t = \mu + \tau_{t-1} + \eta_t$, $c_t = \phi_1c_{t-1} + \phi_2c_{t-2} + \varepsilon_t$, $\Corr(\eta_t, \varepsilon_t) = \rho$'),
      T(r'$\tau_t$: the stochastic trend with drift $\mu$ and shocks $\eta_t$ (s.d. $\sigma_\eta$); $c_t$: an AR(2) cycle with shocks $\varepsilon_t$ (s.d. $\sigma_\varepsilon$); $\rho$: the correlation of the two shocks', r'$\tau_t$: trendul stochastic cu driftul $\mu$ și șocurile $\eta_t$ (abaterea standard $\sigma_\eta$); $c_t$: un ciclu AR(2) cu șocurile $\varepsilon_t$ (abaterea standard $\sigma_\varepsilon$); $\rho$: corelația celor două șocuri')]),
    (T(r'Clark\'s UC0 imposes $\rho = 0$; with an AR(2) cycle, $\rho$ is identified: the reduced form is an ARIMA(2,1,2) with as many parameters as UC-UR',
       r'Modelul UC0 al lui Clark impune $\rho = 0$; cu un ciclu AR(2), $\rho$ este identificat: forma redusă este un ARIMA(2,1,2), cu tot atîția parametri cît UC-UR'),
     [T(r'with an AR(1) cycle, $\rho$ is not identified', r'cu un ciclu AR(1), $\rho$ nu este identificat')]),
    T(r'Result: if $\rho$ is free, the filtered UC cycle equals the BN cycle of the ARIMA(2,1,2): the difference between BN and UC was the restriction $\rho = 0$',
      r'Rezultatul: dacă $\rho$ este liber, ciclul UC filtrat coincide cu ciclul BN al modelului ARIMA(2,1,2): diferența dintre BN și UC era restricția $\rho = 0$'),
    T(r'State $(\tau_t, c_t, c_{t-1})$: $\tau$ diffuse, the cycle block stationary (mixed initialisation); case study below: their sample, 1947Q1--1998Q2, today\'s data vintage',
      r'Starea $(\tau_t, c_t, c_{t-1})$: $\tau$ difuz, blocul ciclului staționar (inițializare mixtă); studiul de caz de mai jos: eșantionul lor, T1 1947--T2 1998, datele din ediția actuală')), 'small')

chart(T('Replicating Morley, Nelson and Zivot (2003)', 'Replicarea Morley, Nelson și Zivot (2003)'), 'ats_ch6_mnz', 'ATS_ch6_trend_cycle', [
    T(r'100$\times$log US real GDP (FRED GDPC1), $T = @{mz.T}$; UC0 and UC-UR by exact diffuse ML; BN cycle from an ARIMA(2,1,2); Hamilton (2018) cycle for comparison',
      r'100$\times$log PIB real al SUA (FRED GDPC1), $T = @{mz.T}$; UC0 și UC-UR prin ML difuz exact; ciclul BN dintr-un ARIMA(2,1,2); ciclul Hamilton (2018) pentru comparație')],
    h='0.65\\textheight')

D.frame(T('Interpreting the MNZ replication', 'Interpretarea replicării MNZ'), table(
    'lccccccc', T('Model', 'Model') + r' & $\mu$ & $\phi_1$ & $\phi_2$ & $\sigma_\eta$ & $\sigma_\varepsilon$ & $\rho$ & $\ln L$',
    [r'UC0 & @{mz.u0.mu} & @{mz.u0.p1} & @{mz.u0.p2} & @{mz.u0.se} & @{mz.u0.sc} & 0 & @{mz.u0.ll}',
     r'UC-UR & @{mz.ur.mu} & @{mz.ur.p1} & @{mz.ur.p2} & @{mz.ur.se} & @{mz.ur.sc} & @{mz.ur.rho} & @{mz.ur.ll}'],
    size='footnotesize') + items(
    T(r'$\hat\rho = @{mz.ur.rho}$: trend and cycle shocks are almost perfectly negatively correlated; trend shocks are larger than cycle shocks ($\hat\sigma_\eta > \hat\sigma_\varepsilon$)',
      r'$\hat\rho = @{mz.ur.rho}$: șocurile trendului și ale ciclului sînt corelate negativ aproape perfect; șocurile trendului sînt mai mari decît cele ale ciclului ($\hat\sigma_\eta > \hat\sigma_\varepsilon$)'),
    T(r'Correlation of the UC-UR filtered cycle with the BN cycle (ARIMA AR roots @{mz.bn1}, @{mz.bn2} as in UC-UR): @{mz.corr}; s.d. of the cycles: UC0 @{mz.sd0}, UC-UR @{mz.sd1}, BN @{mz.sdbn}, Hamilton @{mz.sdham}',
      r'Corelația ciclului UC-UR filtrat cu ciclul BN (coeficienții AR ai ARIMA @{mz.bn1}, @{mz.bn2}, ca în UC-UR): @{mz.corr}; abaterile standard ale ciclurilor: UC0 @{mz.sd0}, UC-UR @{mz.sd1}, BN @{mz.sdbn}, Hamilton @{mz.sdham}'),
    T(r'LR test of $\rho = 0$: @{mz.LR}, $p = @{mz.p}$ ($\chi^2_1$); the cycle of UC0 is large because it is assumed orthogonal to the trend, not because the data demand it',
      r'Testul LR pentru $\rho = 0$: @{mz.LR}, $p = @{mz.p}$ ($\chi^2_1$); ciclul UC0 este mare pentru că este presupus ortogonal pe trend, nu pentru că datele o cer'),
    T(r'Our numbers use today\'s GDP vintage; the paper\'s estimates differ in the decimals, not in the conclusion', r'Cifrele noastre folosesc ediția actuală a datelor PIB; estimațiile din lucrare diferă la zecimale, nu în concluzie')), 'footnotesize')

D.frame(T('Romania: the cycle is the trend', 'România: ciclul este trendul'), two(
    ph('bnr', T('The BNR palace, Bucharest', 'Palatul BNR, București'), h='0.30\\textheight'),
    items(T(r'Emerging economies have volatile trend shocks \refAG: a random-walk trend absorbs most of the movement in GDP',
            r'Economiile emergente au șocuri de trend volatile \refAG: un trend de tip mers aleator absoarbe cea mai mare parte a mișcării PIB'),
          T(r'Romanian UC0, 2000Q1--@{rg.last} (2020Q2--Q4 treated as missing): $\hat\sigma_\eta = @{rg.u0.se}$, $\hat\sigma_\varepsilon = @{rg.u0.sc}$, $\hat\phi_1 = @{rg.u0.p1}$, $\hat\phi_2 = @{rg.u0.p2}$: a short, weak cycle',
            r'UC0 pentru România, T1 2000--@{rg.last} (T2--T4 2020 tratate ca lipsă): $\hat\sigma_\eta = @{rg.u0.se}$, $\hat\sigma_\varepsilon = @{rg.u0.sc}$, $\hat\phi_1 = @{rg.u0.p1}$, $\hat\phi_2 = @{rg.u0.p2}$: un ciclu scurt și slab'),
          T(r'UC-UR: $\hat\rho = @{rg.ur.rho}$ at the boundary, LR $= @{rg.LR}$: in @{rg.T} quarters the correlation is poorly determined',
            r'UC-UR: $\hat\rho = @{rg.ur.rho}$ la frontieră, LR $= @{rg.LR}$: în @{rg.T} trimestre corelația este slab determinată'),
          T(r'Alternative: a smooth trend (integrated random walk, the HP model \refHJ) with an AR(2) cycle: $\hat\sigma^2_\zeta = @{rg.st.z}$, $\hat\sigma^2_\varepsilon = @{rg.st.e}$, $\hat\phi = (@{rg.st.p1}, @{rg.st.p2})$',
            r'Alternativa: un trend neted (mers aleator integrat, modelul HP \refHJ) cu un ciclu AR(2): $\hat\sigma^2_\zeta = @{rg.st.z}$, $\hat\sigma^2_\varepsilon = @{rg.st.e}$, $\hat\phi = (@{rg.st.p1}, @{rg.st.p2})$')), '0.3', '0.68'), 'footnotesize')

chart(T('The Romanian output gap', 'Output gap-ul României'), 'ats_ch6_ro_gap', 'ATS_ch6_trend_cycle', [
    T(r'100$\times$log real GDP, Eurostat, seasonally and calendar adjusted; smooth-trend UC (smoothed, with 90\% band, and filtered), random-walk-trend UC0, Hamilton (2018) on the full series',
      r'100$\times$log PIB real, Eurostat, ajustat sezonier și cu numărul de zile lucrătoare; UC cu trend neted (netezit, cu bandă de 90\%, și filtrat), UC0 cu trend mers aleator, Hamilton (2018) pe seria completă')],
    h='0.65\\textheight')

interp(('the Romanian output gap', 'output gap-ului României'), [
    T(r'Smooth-trend gap: @{rg.g08}\% in 2008Q3 (s.d. @{rg.sd08}), @{rg.g10}\% in 2010Q3, @{rg.g19}\% in 2019Q4; last quarter @{rg.lasts}\% (s.d. @{rg.lastsd})',
      r'Output gap-ul cu trend neted: @{rg.g08}\% în T3 2008 (abatere standard @{rg.sd08}), @{rg.g10}\% în T3 2010, @{rg.g19}\% în T4 2019; ultimul trimestru @{rg.lasts}\% (abatere standard @{rg.lastsd})'),
    T(r'Real time is different: the filtered gap was only @{rg.f08}\% in 2008Q3 and @{rg.f19}\% in 2019Q4; s.d. of the revisions (smoothed minus filtered): @{rg.rev} pp \refOvN',
      r'În timp real situația este alta: output gap-ul filtrat era doar @{rg.f08}\% în T3 2008 și @{rg.f19}\% în T4 2019; abaterea standard a revizuirilor (netezit minus filtrat): @{rg.rev} pp \refOvN'),
    T(r'Model choice dominates: s.d. of the gap @{rg.sdgap} (smooth trend), @{rg.sduc0} (UC0), @{rg.sdham} (Hamilton); correlation smooth trend--Hamilton @{rg.corr}',
      r'Alegerea modelului domină: abaterea standard a output gap-ului este @{rg.sdgap} (trend neted), @{rg.sduc0} (UC0), @{rg.sdham} (Hamilton); corelația trend neted--Hamilton @{rg.corr}'),
    T('A Romanian output gap without its band and without the model behind it is not information', 'Un output gap pentru România fără banda lui și fără modelul din spatele lui nu este o informație')])

D.recap(('Trend--cycle decompositions', 'descompunerile trend--ciclu'), [
    T('BN, UC and Hamilton define the cycle differently; MNZ show that BN and UC agree once trend and cycle shocks may correlate', 'BN, UC și Hamilton definesc ciclul diferit; MNZ arată că BN și UC coincid odată ce șocurile trendului și ale ciclului pot fi corelate'),
    T('In short, volatile samples (Romania) the correlation is not identified and the trend specification decides the gap', 'În eșantioane scurte și volatile (România) corelația nu este identificată, iar specificarea trendului decide output gap-ul'),
    T('Report filtered and smoothed estimates: the end-of-sample gap is the least reliable number', 'Raportați estimațiile filtrate și netezite: output gap-ul de la finalul eșantionului este cifra cea mai puțin fiabilă')])

# =============================================================================
# 9. UC-SV
# =============================================================================
D.section('Trend inflation with stochastic volatility', 'Inflația de trend cu volatilitate stochastică')

D.frame(T('The UC-SV model of Stock and Watson (2007)', 'Modelul UC-SV al lui Stock și Watson (2007)'), items(
    (T(r'$\pi_t = \tau_t + \sigma_{\eta,t}\eta_t$, $\quad \tau_t = \tau_{t-1} + \sigma_{\varepsilon,t}\varepsilon_t$, $\quad \ln\sigma^2_{j,t} = \ln\sigma^2_{j,t-1} + \nu_{j,t}$, $\nu_{j,t} \sim N(0, \gamma)$ \refSWb',
       r'$\pi_t = \tau_t + \sigma_{\eta,t}\eta_t$, $\quad \tau_t = \tau_{t-1} + \sigma_{\varepsilon,t}\varepsilon_t$, $\quad \ln\sigma^2_{j,t} = \ln\sigma^2_{j,t-1} + \nu_{j,t}$, $\nu_{j,t} \sim N(0, \gamma)$ \refSWb'),
     [T(r'$\pi_t$: inflation; $\tau_t$: trend inflation (a random walk); $\sigma_{\eta,t}$, $\sigma_{\varepsilon,t}$: the time-varying s.d. of the transitory and trend shocks ($j \in \{\eta, \varepsilon\}$); $\eta_t, \varepsilon_t \sim N(0, 1)$', r'$\pi_t$: inflația; $\tau_t$: inflația de trend (un mers aleator); $\sigma_{\eta,t}$, $\sigma_{\varepsilon,t}$: abaterile standard variabile în timp ale șocurilor tranzitorii și de trend ($j \in \{\eta, \varepsilon\}$); $\eta_t, \varepsilon_t \sim N(0, 1)$')]),
    (T(r'$\gamma = 0.2$ is fixed, not estimated: the only tuning parameter; it governs how fast the volatilities can move',
       r'$\gamma = 0{,}2$ este fixat, nu estimat: singurul parametru de calibrare; el guvernează cît de repede se pot mișca volatilitățile'),
     [T(r'reduced form: IMA(1,1) with a time-varying MA coefficient $\theta_t$, a function of $\sigma_{\varepsilon,t}/\sigma_{\eta,t}$',
        r'forma redusă: IMA(1,1) cu un coeficient MA variabil în timp $\theta_t$, funcție de $\sigma_{\varepsilon,t}/\sigma_{\eta,t}$')]),
    (T(r'Gibbs: $\tau_{1:n}$ by the precision sampler (time-varying weights); each $\ln\sigma^2_{j,1:n}$ by the KSC mixture on $\ln(\hat\eta^2_t + c)$ and $\ln(\Delta\tau^2_t + c)$',
       r'Gibbs: $\tau_{1:n}$ prin eșantionarea pe baza preciziei (ponderi variabile în timp); fiecare $\ln\sigma^2_{j,1:n}$ prin mixtura KSC pe $\ln(\hat\eta^2_t + c)$ și $\ln(\Delta\tau^2_t + c)$'),
     [T('for Romania: three quarterly seasonal coefficients as an extra Gibbs block (weighted regression); the HICP is not seasonally adjusted',
        'pentru România: trei coeficienți sezonieri trimestriali ca bloc Gibbs suplimentar (regresie ponderată); IAPC nu este ajustat sezonier')]),
    T(r'Why it matters: the share of trend shocks decides how much of an inflation surge is permanent and how much a forecaster should extrapolate',
      r'Miza: ponderea șocurilor de trend decide cît dintr-un salt al inflației este permanent și cît ar trebui să extrapoleze cel care face prognoze')), 'small')

chart(T('US trend inflation, 1953--2026', 'Inflația de trend în SUA, 1953--2026'), 'ats_ch6_ucsv_us', 'ATS_ch6_ucsv_inflation', [
    T(r'GDP-deflator inflation, $T = @{us.T}$ quarters; UC-SV with $\gamma = 0.2$, Gibbs sampler; top: trend with 68\% band; bottom: posterior means of $\sigma_{\varepsilon,t}$ (trend) and $\sigma_{\eta,t}$ (transitory)',
      r'Inflația deflatorului PIB, $T = @{us.T}$ trimestre; UC-SV cu $\gamma = 0{,}2$, eșantionator Gibbs; sus: trendul cu bandă de 68\%; jos: mediile a posteriori ale lui $\sigma_{\varepsilon,t}$ (trend) și $\sigma_{\eta,t}$ (tranzitoriu)')],
    h='0.65\\textheight')

interp(('US trend inflation', 'inflației de trend din SUA'), [
    T(r'Trend: @{us.t75}\% in 1975Q1, @{us.t95}\% in 1995Q1, @{us.t19}\% in 2019Q4, @{us.t22}\% [@{us.tl22}; @{us.th22}] in 2022Q2, @{us.tlast}\% [@{us.tllast}; @{us.thlast}] in @{us.last}',
      r'Trendul: @{us.t75}\% în T1 1975, @{us.t95}\% în T1 1995, @{us.t19}\% în T4 2019, @{us.t22}\% [@{us.tl22}; @{us.th22}] în T2 2022, @{us.tlast}\% [@{us.tllast}; @{us.thlast}] în @{us.last}'),
    T(r'Trend shocks: s.d. @{us.s275} in 1975, @{us.s295} in 1995, @{us.s222} in 2022; transitory shocks: @{us.s175}, @{us.s195}, @{us.s122}',
      r'Șocurile de trend: abaterea standard @{us.s275} în 1975, @{us.s295} în 1995, @{us.s222} în 2022; șocurile tranzitorii: @{us.s175}, @{us.s195}, @{us.s122}'),
    T(r'Implied MA coefficient $\theta_t$: @{us.theta75} (1975), @{us.theta95} (1995), @{us.theta19} (2019), @{us.theta22} (2022): inflation became more like a random walk again in 2021--2022',
      r'Coeficientul MA implicit $\theta_t$: @{us.theta75} (1975), @{us.theta95} (1995), @{us.theta19} (2019), @{us.theta22} (2022): inflația a devenit din nou mai apropiată de un mers aleator în 2021--2022'),
    T(r'This is the forecasting lesson of \refSWb: in calm periods smooth heavily; when trend volatility rises, a fixed-coefficient model reacts too slowly',
      r'Aceasta este lecția de prognoză din \refSWb: în perioade calme netezim puternic; cînd volatilitatea trendului crește, un model cu coeficienți ficși reacționează prea lent')], 'footnotesize')

chart(T('Romanian trend inflation and the BNR target', 'Inflația de trend din România și ținta BNR'), 'ats_ch6_ucsv_ro', 'ATS_ch6_ucsv_inflation', [
    T(r'Quarterly HICP inflation (quarterly averages of the monthly index), $T = @{ro.T}$, 2001Q1--@{ro.last}; UC-SV with $\gamma = 0.2$ and quarterly seasonal dummies; inflation-target band of the BNR since 2013',
      r'Inflația IAPC trimestrială (medii trimestriale ale indicelui lunar), $T = @{ro.T}$, T1 2001--@{ro.last}; UC-SV cu $\gamma = 0{,}2$ și variabile dummy sezoniere trimestriale; banda-țintă a BNR din 2013')],
    h='0.64\\textheight')

interp(('Romanian trend inflation', 'inflației de trend din România'), [
    T(r'Trend: @{ro.t05}\% when inflation targeting began (2005Q3), @{ro.t15}\% in 2015Q3, @{ro.t19}\% in 2019Q4, @{ro.t23}\% in 2023Q1',
      r'Trendul: @{ro.t05}\% la începutul țintirii inflației (T3 2005), @{ro.t15}\% în T3 2015, @{ro.t19}\% în T4 2019, @{ro.t23}\% în T1 2023'),
    T(r'Last quarter: @{ro.tlast}\% [@{ro.tllast}; @{ro.thlast}]; posterior probability that the trend lies inside 1.5--3.5\%: @{ro.pin}\%',
      r'Ultimul trimestru: @{ro.tlast}\% [@{ro.tllast}; @{ro.thlast}]; probabilitatea a posteriori ca trendul să se afle în intervalul 1,5--3,5\%: @{ro.pin}\%'),
    T('Since 2013 the trend has been inside the band only part of the time: below it in 2015--2016 (VAT cuts), above it since 2021', 'Din 2013, trendul s-a aflat în bandă doar o parte din timp: sub ea în 2015--2016 (reducerile de TVA), peste ea din 2021'),
    T('Caveats: administered prices (energy caps, VAT changes) enter as trend shocks in a univariate model; a project can add them as regressors or as a separate component', 'Rezerve: prețurile administrate (plafonările la energie, modificările TVA) intră ca șocuri de trend într-un model univariat; un proiect le poate adăuga ca regresori sau ca o componentă separată')])

D.frame(T('Beyond: BSTS and regime switching', 'Mai departe: BSTS și modele cu schimbare de regim'), items(
    (T(r'Bayesian structural time series \refSV: local linear trend + seasonal + regression with a spike-and-slab prior on many regressors (Google Trends)',
       r'Serii de timp structurale bayesiene \refSV: local linear trend + componentă sezonieră + regresie cu a priori spike-and-slab pe mulți regresori (Google Trends)'),
     [T(r'the same simulation smoother inside a Gibbs sampler; variable selection on the regression block', r'același simulation smoother într-un eșantionator Gibbs; selecția variabilelor pe blocul de regresie'),
      T(r'counterfactuals for policy evaluation (CausalImpact, \refBro): Chapter 14', r'contrafactuali pentru evaluarea politicilor (CausalImpact, \refBro): Capitolul 14')]),
    (T(r'Discrete states: $s_t \in \{1, \dots, K\}$ with a Markov chain; the Hamilton filter is the Bayes filter with sums instead of integrals',
       r'Stări discrete: $s_t \in \{1, \dots, K\}$ cu un lanț Markov; filtrul Hamilton este filtrul Bayes cu sume în loc de integrale'),
     [T(r'state space models with regime switching (Kim filter, Gibbs sampling) \refKN: Chapter 7', r'modele în spațiul stărilor cu schimbare de regim (filtrul Kim, eșantionare Gibbs) \refKN: Capitolul 7')]),
    T(r'Forecast evaluation of all these models (density forecasts, scoring rules): Chapter 1', r'Evaluarea prognozelor tuturor acestor modele (prognoze de densitate, reguli de scor): Capitolul 1')), 'small')

D.recap(('Trend inflation', 'inflația de trend'), [
    T('UC-SV lets the split between permanent and transitory shocks change over time', 'UC-SV permite ca împărțirea dintre șocurile permanente și cele tranzitorii să se schimbe în timp'),
    T('Two KSC blocks and one precision sampler make the Gibbs sampler fast', 'Două blocuri KSC și o eșantionare pe baza preciziei fac eșantionatorul Gibbs rapid'),
    T('US trend inflation rose sharply in 2021--2022; Romanian trend inflation is still above the target band', 'Inflația de trend din SUA a crescut puternic în 2021--2022; inflația de trend din România este încă peste banda-țintă')])

# =============================================================================
# 10. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('How much of the 2021--2023 inflation surge was a shift in trend inflation, in the US and in Romania, and has it been reversed?', 'Cît din saltul inflației din 2021--2023 a fost o deplasare a inflației de trend, în SUA și în România, și s-a inversat aceasta?'),
     [T(r'formal: the posterior of $\tau_t$ and of $\sigma_{\varepsilon,t}/\sigma_{\eta,t}$ in UC-SV; falsified if the trend has returned to its 2019 level with high posterior probability under every pre-registered specification',
        r'formal: distribuția a posteriori a lui $\tau_t$ și a raportului $\sigma_{\varepsilon,t}/\sigma_{\eta,t}$ în UC-SV; infirmată dacă trendul a revenit la nivelul din 2019 cu probabilitate a posteriori mare sub orice specificare preînregistrată'),
      T('the univariate answer depends on one fixed parameter, $\\gamma$: the mini-case below', 'răspunsul univariat depinde de un parametru fixat, $\\gamma$: mini studiul de caz de mai jos')]),
    (T('Why it matters: a central bank reacts differently to a transitory and to a persistent surge; anchoring is a statement about the trend, not about headline inflation', 'Miza: o bancă centrală reacționează diferit la un salt tranzitoriu și la unul persistent; ancorarea este o afirmație despre trend, nu despre inflația totală'),
     [T(r'literature to start from: \refSWb, \refCSb, \refPri, \refMNZ', r'literatura de pornire: \refSWb, \refCSb, \refPri, \refMNZ')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers that estimate trend inflation with stochastic volatility for European countries after 2021; give DOIs.} Then check every DOI on Crossref',
        r'\textbf{literatura}: \aiprompt{Listează lucrări recenzate care estimează inflația de trend cu volatilitate stochastică pentru țări europene după 2021; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Propose three observable implications that distinguish a trend shift from a sequence of large transitory shocks.}',
        r'\textbf{ipoteza}: \aiprompt{Propune trei implicații observabile care deosebesc o deplasare a trendului de o succesiune de șocuri tranzitorii mari.}'),
      T(r'\textbf{code and replication}: ask for a UC-SV Gibbs sampler, then reproduce a known number first (the US trend of this lecture)',
        r'\textbf{cod și replicare}: cereți un eșantionator Gibbs pentru UC-SV, apoi reproduceți întîi o cifră cunoscută (trendul pentru SUA din acest curs)'),
      T(r'\textbf{robustness and critique}: \aiprompt{Act as a hostile referee: which fixed choices of a UC-SV model could change the conclusion about 2022?}',
        r'\textbf{robustețe și critică}: \aiprompt{Joacă rolul unui recenzent ostil: ce alegeri fixate ale unui model UC-SV ar putea schimba concluzia despre 2022?}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T(r'The sampler targets the stated posterior: test it on a model with a known answer (the Kalman smoother, as in the three-sampler check)', r'Eșantionatorul are ca țintă distribuția a posteriori declarată: testați-l pe un model cu răspuns cunoscut (netezitorul Kalman, ca în verificarea celor trei eșantionatoare)'),
    T(r'Convergence is reported: several chains, inefficiency factors, the effect of doubling the draws', r'Convergența este raportată: mai multe lanțuri, factori de ineficiență, efectul dublării numărului de extrageri'),
    T(r'Fixed choices ($\gamma$, the KSC offset, priors, seasonal treatment, start date) are listed and varied before conclusions are drawn', r'Alegerile fixate ($\gamma$, constanta KSC, distribuțiile a priori, tratarea sezonalității, data de început) sînt enumerate și variate înaintea concluziilor'),
    T('End-of-sample estimates are reported as filtered values with their bands, not as smoothed point estimates', 'Estimațiile de la finalul eșantionului sînt raportate ca valori filtrate, cu benzile lor, nu ca estimații punctuale netezite')), 'small')

chart(T('Mini-case: one fixed parameter, four trends', 'Mini studiu de caz: un parametru fixat, patru trenduri'), 'ats_ch6_ai_case', 'ATS_ch6_ai_robustness', [
    T(r'US UC-SV trend since 2015 for $\gamma \in \{0.05, 0.1, 0.2, 0.4\}$: trend in 2022Q2 @{ai.pk05}, @{ai.pk1}, @{ai.pk2}, @{ai.pk4}\% (inflation @{ai.pi}\%); in the last quarter @{ai.last05}, @{ai.last1}, @{ai.last2}, @{ai.last4}\%',
      r'Trendul UC-SV pentru SUA din 2015, pentru $\gamma \in \{0{,}05; 0{,}1; 0{,}2; 0{,}4\}$: trendul în T2 2022 @{ai.pk05}, @{ai.pk1}, @{ai.pk2}, @{ai.pk4}\% (inflația @{ai.pi}\%); în ultimul trimestru @{ai.last05}, @{ai.last1}, @{ai.last2}, @{ai.last4}\%'),
    T(r'The ranking is stable but the level of the 2022 trend is not: an AI summary that reports ``trend inflation peaked at X\%\'\' without $\gamma$ hides a modelling choice',
      r'Ordinea este stabilă, dar nivelul trendului din 2022 nu este: un rezumat AI care raportează „inflația de trend a atins un maxim de X\%” fără $\gamma$ ascunde o alegere de modelare')],
    h='0.55\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Trend inflation and anchoring in Central and Eastern Europe}: replicate first, then extend', r'\textbf{Inflația de trend și ancorarea în Europa Centrală și de Est}: întîi replicare, apoi extindere'),
     [T(r'replicate: the US UC-SV trend of this lecture (2022Q2: @{us.t22}\%) and the Romanian trend (@{ro.tlast}\% in @{ro.last})',
        r'replicați: trendul UC-SV pentru SUA din acest curs (T2 2022: @{us.t22}\%) și trendul pentru România (@{ro.tlast}\% în @{ro.last})'),
      T(r'extend: Romania, Hungary, Poland and Czechia; a multivariate UC-SV with a common euro-area trend; administered prices as a separate component; $\gamma$ estimated with a prior instead of fixed',
        r'extindeți: România, Ungaria, Polonia și Cehia; un UC-SV multivariat cu un trend comun al zonei euro; prețurile administrate ca o componentă separată; $\gamma$ estimat cu o distribuție a priori în loc să fie fixat'),
      T(r'pre-register: data, sample, priors, the anchoring statistic (posterior probability inside the target band), the real-time exercise and the robustness grid',
        r'preînregistrați: datele, eșantionul, distribuțiile a priori, statistica de ancorare (probabilitatea a posteriori de a fi în banda-țintă), exercițiul în timp real și grila de robustețe')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('The Kalman filter is Gaussian conditioning applied recursively; the smoother, the likelihood and the simulation smoother follow from it', 'Filtrul Kalman este condiționarea gaussiană aplicată recursiv; netezitorul, verosimilitatea și simulation smoother-ul decurg din ea'),
    T('Initialise nonstationary states exactly; treat zero variances as boundary problems', 'Inițializați exact stările nestaționare; tratați varianțele nule ca probleme de frontieră'),
    T('Bayesian state space: sample whole paths; FFBS, DK and precision samplers are interchangeable', 'Spațiul stărilor bayesian: eșantionați traiectorii întregi; FFBS, DK și eșantionarea pe baza preciziei sînt interschimbabile'),
    T('Stochastic volatility is not GARCH; the KSC mixture and particle filters make it tractable', 'Volatilitatea stochastică nu este GARCH; mixtura KSC și filtrele de particule o fac tratabilă'),
    T('Latent quantities (gaps, trends, time-varying slopes) come with model-dependent uncertainty: report bands, filtered values and alternatives', 'Mărimile latente (output gap-uri, trenduri, pante variabile în timp) au o incertitudine care depinde de model: raportați benzi, valori filtrate și alternative')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T(r'Why does a big-kappa likelihood fall without bound as $\kappa$ grows?', r'De ce scade nelimitat log-verosimilitatea big kappa cînd $\kappa$ crește?'),
        T(r'What does an ML estimate $\hat\sigma^2_\eta = 0$ tell you about a local level?', r'Ce vă spune o estimație ML $\hat\sigma^2_\eta = 0$ despre un model local level?'),
        T('Why does the DK simulation smoother need only a mean smoother?', 'De ce are nevoie simulation smoother-ul DK doar de netezitorul mediei?'),
        T('Why is the EKF gain zero in the SV model?', 'De ce este zero cîștigul EKF în modelul SV?'),
        T(r'Why is $\ln\hat L$ biased although $\hat L$ is unbiased?', r'De ce este $\ln\hat L$ deplasat, deși $\hat L$ este nedeplasat?'),
        T('Which restriction makes the UC cycle differ from the BN cycle?', 'Ce restricție face ca ciclul UC să difere de ciclul BN?'))),
    block(T('Next: Chapter 7', 'Urmează: Capitolul 7'), items(
        T('Regime-switching models', 'Modele cu schimbare de regim'),
        T('Discrete hidden states: the Hamilton filter, the Kim smoother, EM and Gibbs for Markov switching, and state space models with regimes', 'Stări ascunse discrete: filtrul Hamilton, netezitorul Kim, EM și Gibbs pentru modelele Markov switching și modele în spațiul stărilor cu regimuri'))),
    '0.58', '0.38'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the Kalman filter from the lemma', 'Anexă: filtrul Kalman din lemă'), items(
    T(r'Given $Y_{t-1}$: $\begin{pmatrix}\alpha_t\\ y_t\end{pmatrix} \sim N\left(\begin{pmatrix}a_t\\ Z_ta_t\end{pmatrix}, \begin{pmatrix}P_t & P_tZ_t\'\\ Z_tP_t & F_t\end{pmatrix}\right)$, $F_t = Z_tP_tZ_t\' + H_t$',
      r'Dat $Y_{t-1}$: $\begin{pmatrix}\alpha_t\\ y_t\end{pmatrix} \sim N\left(\begin{pmatrix}a_t\\ Z_ta_t\end{pmatrix}, \begin{pmatrix}P_t & P_tZ_t\'\\ Z_tP_t & F_t\end{pmatrix}\right)$, $F_t = Z_tP_tZ_t\' + H_t$'),
    T(r'Conditioning on $y_t$ (equivalently on $v_t$, since $Y_t = (Y_{t-1}, v_t)$ and $v_t$ is independent of $Y_{t-1}$) gives $a_{t|t}$ and $P_{t|t}$',
      r'Condiționarea pe $y_t$ (echivalent pe $v_t$, deoarece $Y_t = (Y_{t-1}, v_t)$, iar $v_t$ este independent de $Y_{t-1}$) dă $a_{t|t}$ și $P_{t|t}$'),
    T(r'$\alpha_{t+1} = c_t + T_t\alpha_t + R_t\eta_t$ with $\eta_t$ independent of $Y_t$: $a_{t+1} = c_t + T_ta_{t|t}$, $P_{t+1} = T_tP_{t|t}T_t\' + R_tQ_tR_t\'$',
      r'$\alpha_{t+1} = c_t + T_t\alpha_t + R_t\eta_t$ cu $\eta_t$ independent de $Y_t$: $a_{t+1} = c_t + T_ta_{t|t}$, $P_{t+1} = T_tP_{t|t}T_t\' + R_tQ_tR_t\'$'),
    T(r'Smoother: $\hat\alpha_t = a_t + \sum_{j=t}^n\Cov(\alpha_t, v_j)F_j^{-1}v_j$ (the $v_j$ are independent); $\Cov(\alpha_t, v_j) = P_tL_t\'\cdots L_{j-1}\'Z_j\'$ gives $\hat\alpha_t = a_t + P_tr_{t-1}$',
      r'Netezitorul: $\hat\alpha_t = a_t + \sum_{j=t}^n\Cov(\alpha_t, v_j)F_j^{-1}v_j$ (variabilele $v_j$ sînt independente); $\Cov(\alpha_t, v_j) = P_tL_t\'\cdots L_{j-1}\'Z_j\'$ dă $\hat\alpha_t = a_t + P_tr_{t-1}$')), 'small')

D.frame(T('Appendix: exactness of the Durbin--Koopman simulation smoother', 'Anexă: exactitatea simulation smoother-ului Durbin--Koopman'), items(
    T(r'Gaussian model: $\alpha | y \sim N(\hat\alpha(y), V)$ with $V$ independent of $y$, and $\hat\alpha(y)$ linear in $y$ (affine with the intercepts)',
      r'Modelul gaussian: $\alpha | y \sim N(\hat\alpha(y), V)$, cu $V$ independent de $y$, iar $\hat\alpha(y)$ liniar în $y$ (afin, cu termenii liberi)'),
    T(r'For a draw $(\alpha^+, y^+)$ from the joint law, $\alpha^+ - \hat\alpha(y^+) \sim N(0, V)$ and is independent of $y^+$ (and of $y$)',
      r'Pentru o extragere $(\alpha^+, y^+)$ din legea comună, $\alpha^+ - \hat\alpha(y^+) \sim N(0, V)$ și este independentă de $y^+$ (și de $y$)'),
    T(r'Hence $\tilde\alpha = \hat\alpha(y) + \alpha^+ - \hat\alpha(y^+) \sim N(\hat\alpha(y), V)$; linearity gives $\hat\alpha(y) - \hat\alpha(y^+) = \hat\alpha_0(y - y^+)$, one smoother pass with zero intercepts',
      r'Deci $\tilde\alpha = \hat\alpha(y) + \alpha^+ - \hat\alpha(y^+) \sim N(\hat\alpha(y), V)$; liniaritatea dă $\hat\alpha(y) - \hat\alpha(y^+) = \hat\alpha_0(y - y^+)$, o singură trecere a netezitorului cu termeni liberi nuli'),
    T(r'Diffuse states: the exact diffuse smoother is invariant to the diffuse part of $\alpha_1^+$, so it can be set to $a_1$',
      r'Stările difuze: netezitorul difuz exact este invariant la partea difuză a lui $\alpha_1^+$, deci aceasta poate fi fixată la $a_1$')), 'small')

D.frame(T('Appendix: unbiasedness of the particle likelihood', 'Anexă: nedeplasarea verosimilității din filtrul de particule'), items(
    T(r'Bootstrap filter, one step: $\E[\frac1N\sum_iw^{(i)}_t\,|\,\mathcal F_{t-1}] = \int g(y_t | x)\,\hat p_{N}(x | Y_{t-1})\,dx$, with $\hat p_N$ the empirical predictive law of the particles',
      r'Filtrul bootstrap, un pas: $\E[\frac1N\sum_iw^{(i)}_t\,|\,\mathcal F_{t-1}] = \int g(y_t | x)\,\hat p_{N}(x | Y_{t-1})\,dx$, unde $\hat p_N$ este legea predictivă empirică a particulelor'),
    T(r'Telescoping the conditional expectations over $t = n, n-1, \dots, 1$ with multinomial or systematic resampling gives $\E\prod_t\hat p(y_t | Y_{t-1}) = p(y_{1:n})$ \refDM',
      r'Aplicînd succesiv speranțele condiționate pentru $t = n, n-1, \dots, 1$, cu reeșantionare multinomială sau sistematică, obținem $\E\prod_t\hat p(y_t | Y_{t-1}) = p(y_{1:n})$ \refDM'),
    T(r'Each factor is a ratio estimate, but the product is unbiased because resampling preserves the expected weights; normalised quantities (filtered means) are only consistent',
      r'Fiecare factor este o estimație de tip raport, dar produsul este nedeplasat, pentru că reeșantionarea păstrează ponderile așteptate; mărimile normalizate (mediile filtrate) sînt doar consistente'),
    T(r'Jensen: $\E\ln\hat L \le \ln\E\hat L = \ln L$; under a CLT for $\ln\hat L$ the bias is $-\frac12\Var(\ln\hat L)$',
      r'Jensen: $\E\ln\hat L \le \ln\E\hat L = \ln L$; sub o TLC pentru $\ln\hat L$, deplasarea este $-\frac12\Var(\ln\hat L)$')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
