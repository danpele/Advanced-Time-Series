r"""
build_chapter7.py -- Capitolul 7 (Modele cu schimbare de regim), EN + RO
=========================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_07/ch7_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice). TSA, Capitolul 10 a introdus modelul Hamilton (1989) cu
statsmodels; Capitolul 2 a tratat modelele cu prag (TAR, STAR) și rupturile; aici: filtrul Hamilton și netezitorul
Kim derivate, EM și verosimilitate maximă, identificare, testarea numărului de regimuri, TVTP, MS-VAR, MS-GARCH,
estimare bayesiană, memorie lungă, prognoză.
Ieșire:
  EN/Courses/chapter7_regime_switching_models.tex
  RO/Cursuri/capitol7_modele_schimbare_regim.tex
Rulare:
  python3 Quantlets/Ch_07/generate_all_charts.py
  python3 latex/build_chapter7.py && python3 latex/ats_build.py compile 7
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch7_common import REFS, QLURL, T, V2, day, bib, finalize, load, minus_fix, month, quarter   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(7, 'lecture', refs=REFS)
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
PD = T('public domain', 'domeniu public')
PH = {
    'markov': ('ch7_markov_1886.jpg', C + 'Andrei_Markov.jpg', T('Photo', 'Foto') + ': unknown author (1886); ' + PD + '; Wikimedia Commons'),
    'soup': ('ch7_soup_kitchen_1931.jpg', C + 'Unemployed_men_queued_outside_a_depression_soup_kitchen_opened_in_Chicago_by_Al_Capone,_02-1931_-_NARA_-_541927.jpg',
             FOTO + ': US National Archives (1931); ' + PD + '; Wikimedia Commons'),
    'lehman': ('ch7_lehman_2007.jpg', C + 'Lehman_Brothers_Times_Square_by_David_Shankbone.jpg',
               FOTO + ': David Shankbone (2007); CC BY-SA 3.0; Wikimedia Commons'),
    'bvb': ('ch7_bvb_2024.jpg', C + 'Bursa_de_Valori_București.jpg', FOTO + ': Corina Chitu (2024); CC BY-SA 4.0; Wikimedia Commons'),
    'bnr': ('ch7_bnr_2014.jpg', C + 'Banca_Nationala_National_Bank_Bucharest_Bucuresti_Romania_2.JPG',
            FOTO + ': Crislia (2014); CC BY-SA 4.0; Wikimedia Commons'),
}
PH['markov'] = (PH['markov'][0], PH['markov'][1], T('Photo', 'Foto') + ': ' + T('unknown author', 'autor necunoscut') + ' (1886); ' + PD + '; Wikimedia Commons')


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


# =============================================================================
# CIFRE
# =============================================================================
def de(k):
    """RO: the numeral with 'de' when it is >= 20 (29 de trimestre); 'trimestre' is not in ats_build.RO_NOUNS."""
    k = int(k)
    return f'{k} de' if k >= 20 and (k % 100 >= 20 or k % 100 == 0) else str(k)


def put(key, x, d=2):
    P(key, x, d)


c = N['chain']
put('ch.pi', c['pi1'], 3)
put('ch.lam', c['lam'], 2)
put('ch.d1', c['d1'], 0)
put('ch.d2', c['d2'], 0)
h = N['hamilton']
hp = h['paper']
for i, v in enumerate(hp['mu']):
    put(f'hp.mu{i}', v, 3)
for i, v in enumerate(hp['phi']):
    put(f'hp.phi{i + 1}', v, 3)
for i, v in enumerate(hp['se']):
    put(f'hp.se{i}', v, 3)
put('hp.sig', hp['sigma'], 3)
put('hp.p00', hp['p00'], 3)
put('hp.p11', hp['p11'], 3)
put('hp.ll', hp['loglik'], 2)
put('hp.d0', hp['dur'][0], 1)
put('hp.d1', hp['dur'][1], 1)
V.raw('hp.T', str(hp['T']))
hs = h['sm']
for i, v in enumerate(hs['mu']):
    put(f'hs.mu{i}', v, 3)
for i, v in enumerate(hs['phi']):
    put(f'hs.phi{i + 1}', v, 3)
put('hs.sig', hs['sigma'], 3)
put('hs.p00', hs['p00'], 3)
put('hs.p11', hs['p11'], 3)
put('hs.ll', hs['loglik'], 2)
V.raw('hs.diff', f"$<10^{{-{int(-__import__('math').floor(__import__('math').log10(hs['maxdiff'])) - 1)}}}$")
put('hq.qps', h['qps_paper'], 3)
put('hq.conc', 100 * h['conc_paper'], 0)
ht = h['today']
put('ht.mu0', ht['mu'][0], 2)
put('ht.mu1', ht['mu'][1], 2)
for i, v in enumerate(ht['phi']):
    put(f'ht.phi{i + 1}', v, 2)
put('ht.sig', ht['sigma'], 2)
put('ht.p00', ht['p00'], 2)
put('ht.p11', ht['p11'], 3)
put('ht.d0', ht['dur'][0], 1)
put('ht.d1', ht['dur'][1], 1)
put('ht.qps', ht['qps'], 3)
put('ht.conc', 100 * ht['conc'], 0)
put('ht.p2008', ht['p2008'], 2)
put('ht.p2001', ht['p2001max'], 2)
put('ht.p2020', ht['p2020'], 2)
V.raw('ht.T', str(ht['T']))
V.raw('ht.nrec', str(ht['nrec']))
V.raw('ht.nrec.ro', de(ht['nrec']))
put('ht.last', ht['last'], 3)
V.raw('ht.lastq', quarter(ht['lastq']))
rt = N['realtime']
put('rt.qps', rt['qps'], 3)
put('rt.qpss', rt['qps_smooth'], 3)
for k, v in rt['signals'].items():
    V.raw(f'rt.{k}', quarter(v['first']) if v['first'] != 'none' else V2('none', 'niciunul'))
    put(f'rt.{k}.max', v['maxp'], 2)
V.raw('rt.false', str(rt['false']))
em = N['em']
V.raw('em.groups', '; '.join(f'{n(g_, 2)} ({c_})'.replace('⁅-', '⁅\\ensuremath{-}') for g_, c_ in zip(em['groups'], em['counts'])))
V.raw('em.ng', str(len(em['groups'])))
put('em.top', max(em['groups']), 2)
V.raw('em.n', str(em['n']))
V.raw('em.n.ro', de(em['n']))
V.raw('em.itmed', str(int(em['iters_med'])))
V.raw('em.itmax', str(em['iters_max']))
put('em.sm', em['sm_llf'], 2)
dg = em['degenerate']
put('em.dg.s', dg['sig2'][0], 3)
put('em.dg.s2', dg['sig2'][1], 2)
V.raw('em.dg.p', '$<10^{-9}$')
put('em.dg.mu', dg['beta'][0], 2)
V.raw('em.dg.n', str(dg['n_hi']))
V.raw('em.dg.n.ro', de(dg['n_hi']))
lr = N['lrtest']
put('lr.LR', lr['LR'], 1)
put('lr.p', lr['p'], 3)
put('lr.q95', lr['q95'], 2)
put('lr.c2', lr['c2'], 2)
put('lr.c4', lr['c4'], 2)
V.raw('lr.B', str(lr['B']))
put('lr.mean', lr['mean_sim'], 2)
put('lr.zero', 100 * lr['share_zero'], 0)
V.raw('lr.T', str(lr['T']))
for k in ('1', '2', '3'):
    for c_ in ('AIC', 'BIC', 'HQ', 'loglik'):
        put(f'lr.{c_}{k}', lr['ic'][k][c_], 1)
    V.raw(f'lr.k{k}', str(lr['ic'][k]['npar']))
put('lr.s0', lr['sig'][0], 2)
put('lr.s1', lr['sig'][1], 2)
put('lr.P0', lr['P'][0], 3)
put('lr.P1', lr['P'][1], 3)
put('lr.m0', lr['mu'][0], 2)
put('lr.m1', lr['mu'][1], 2)
tv = N['tvtp']
put('tv.ll', tv['loglik'], 2)
put('tv.llc', tv['loglik_const'], 2)
put('tv.sm', tv['sm_llf'], 2)
put('tv.LR', tv['LR'], 2)
put('tv.p', tv['pLR'], 3)
put('tv.mu0', tv['mu'][0], 2)
put('tv.mu1', tv['mu'][1], 2)
for i, (g, s) in enumerate(zip(tv['gamma'], tv['se_gamma'])):
    put(f'tv.g{i}', g, 2)
    put(f'tv.s{i}', s, 2)
put('tv.min', tv['stay_exp_min'], 2)
put('tv.med', tv['stay_exp_med'], 3)
put('tv.pc0', tv['p_const'][0], 3)
put('tv.pc1', tv['p_const'][1], 2)
put('tv.mc1', tv['mu_const'][1], 2)
put('tv.qps', tv['qps'], 3)
put('tv.conc', 100 * tv['conc'], 0)
V.raw('tv.T', str(tv['T']))
mv = N['msvar']
for i in (0, 1):
    put(f'mv.P{i}', mv['P'][i], 2)
    put(f'mv.d{i}', mv['dur'][i], 1)
    put(f'mv.sy{i}', mv['sd_y'][i], 2)
    put(f'mv.su{i}', mv['sd_u'][i], 2)
    put(f'mv.c{i}', mv['corr'][i], 2)
for i, k in enumerate(('lo', 'hi', 'lin')):
    put(f'mv.u4{k}', mv['u_h4'][i], 2)
    put(f'mv.u12{k}', mv['u_h12'][i], 2)
    put(f'mv.sh{k}', mv['shock'][i], 2)
put('mv.share', 100 * mv['share_lo'], 0)
put('mv.rec', 100 * mv['rec_in_vol'], 0)
put('mv.pre', 100 * mv['vol_pre84'], 0)
put('mv.post', 100 * mv['vol_post84'], 0)
put('mv.qps', mv['qps'], 3)
put('mv.ll', mv['loglik'], 1)
put('mv.lll', mv['ll_lin'], 1)
V.raw('mv.T', str(mv['T']))
V.raw('mv.k', str(mv['npar']))
V.raw('mv.k.ro', de(mv['npar']))
mg = N['msgarch']
lo_, hi_ = mg['lo'], mg['hi']
put('mg.gp', mg['garch']['pers'][0], 3)
put('mg.ga', mg['garch']['alpha'][0], 3)
put('mg.gb', mg['garch']['beta'][0], 3)
for k in ('garch', 'hmp', 'gray'):
    put(f'mg.{k}.ll', mg[k]['loglik'], 1)
    put(f'mg.{k}.bic', mg[k]['bic'], 1)
for nm, j in (('lo', lo_), ('hi', hi_)):
    for k in ('hmp', 'gray'):
        put(f'mg.{k}.p.{nm}', mg[k]['pers'][j], 3)
        put(f'mg.{k}.a.{nm}', mg[k]['alpha'][j], 3)
        put(f'mg.{k}.b.{nm}', mg[k]['beta'][j], 3)
        put(f'mg.{k}.P.{nm}', mg[k]['P'][j], 3)
put('mg.vlo', mg['uncond'][0], 1)
put('mg.vhi', mg['uncond'][1], 1)
put('mg.share', 100 * mg['share_hi'], 0)
put('mg.dlo', mg['dur'][0], 0)
put('mg.dhi', mg['dur'][1], 0)
V.int('mg.T', mg['T'])
bb = N['bullbear']
for nm in ('sp500', 'bet'):
    b = bb[nm]
    for j in (0, 1):
        put(f'bb.{nm}.m{j}', b['ann_mu'][j], 1)
        put(f'bb.{nm}.s{j}', b['ann_sd'][j], 1)
        put(f'bb.{nm}.d{j}', b['dur'][j], 0)
        put(f'bb.{nm}.w{j}', b['w'][j], 2)
    put(f'bb.{nm}.share', 100 * b['share_turb'], 0)
    put(f'bb.{nm}.wc', b['w_const'], 2)
    put(f'bb.{nm}.wmin', b['w_t_min'], 2)
    put(f'bb.{nm}.wmax', b['w_t_max'], 2)
    put(f'bb.{nm}.ll', b['loglik'], 1)
    put(f'bb.{nm}.sm', b['sm_llf'], 1)
    put(f'bb.{nm}.last', b['last'], 2)
    V.int(f'bb.{nm}.T', b['T'])
put('bb.corr', bb['corr_turb'], 2)
put('bb.both', 100 * bb['both_turb'], 0)
V.raw('bb.gamma', str(int(bb['gamma'])))
gb = N['gibbs']
for k in ('mu1', 'mu2', 'sd1', 'sd2', 'p11', 'p22'):
    for i, s in enumerate(('m', 'lo', 'hi')):
        put(f'gb.{k}.{s}', gb[k][i], 2)
put('gb.em.mu0', gb['em_mu'][0], 2)
put('gb.em.mu1', gb['em_mu'][1], 2)
put('gb.em.s0', gb['em_sd'][0], 2)
put('gb.em.s1', gb['em_sd'][1], 2)
put('gb.em.p0', gb['em_P'][0], 2)
put('gb.em.p1', gb['em_P'][1], 2)
put('gb.swap', 100 * gb['share_swapped'], 0)
put('gb.corr', gb['corr_em'], 2)
put('gb.acf', gb['acf1'], 2)
V.int('gb.n', gb['n_kept'])
V.raw('gb.T', str(gb['T']))
V.raw('gb.nlo', str(gb['n_lo']))
V.raw('gb.start', quarter(gb['start']))
V.raw('gb.end', quarter(gb['end']))
lm = N['longmem']
for i, Tn in enumerate(lm['Ts']):
    put(f'lm.r{i}', lm['rare'][i][0], 2)
    put(f'lm.f{i}', lm['fixed'][i][0], 2)
    V.int(f'lm.T{i}', Tn)
put('lm.a50', lm['acf50'], 2)
put('lm.a200', lm['acf200'], 2)
V.raw('lm.sw', str(lm['switches']))
V.raw('lm.reps', str(lm['reps']))
ri = N['roinfl']
for j in range(3):
    put(f'ri.l{j}', ri['level'][j], 1)
    put(f'ri.s{j}', ri['sd'][j], 2)
    put(f'ri.d{j}', ri['dur'][j], 0)
    put(f'ri.lp{j}', ri['last_probs'][j], 2)
put('ri.phi', ri['phi'], 3)
put('ri.max', ri['max'], 0)
V.raw('ri.maxd', month(ri['maxdate'] + '-01'))
put('ri.last', ri['last'], 1)
V.raw('ri.lastd', month(ri['lastdate'] + '-01'))
V.raw('ri.start', month(ri['start'] + '-01'))
for k, v in ri['ic'].items():
    put(f'ri.bic.{k}', v['BIC'], 1)
put('ri.ll', ri['loglik'], 1)
for k, v in ri['ll_cp'].items():
    put(f'ri.llcp{k}', v, 1)
V.raw('ri.breaks', ', '.join(month(b + '-01') for b in ri['breaks4']))
V.raw('ri.T', str(ri['T']))
eu = N['eurron']
for j in range(3):
    put(f'eu.s{j}', eu['sd'][j], 2)
    put(f'eu.d{j}', eu['dur'][j], 0)
put('eu.tpre', 100 * eu['share_turb_pre'], 0)
put('eu.tpost', 100 * eu['share_turb_post'], 0)
put('eu.cpre', 100 * eu['share_calm_pre'], 0)
put('eu.cpost', 100 * eu['share_calm_post'], 0)
put('eu.p08', eu['p_turb_2008'], 2)
put('eu.mu2', eu['mu'][2], 2)
put('eu.p25', eu['p_turb_2025'], 2)
put('eu.big', eu['big2025_val'], 2)
put('eu.lvl04', eu['lvl_2025_04'], 4)
put('eu.last', eu['lvl_last'], 4)
V.raw('eu.bigd', day(eu['big2025']))
V.int('eu.T', eu['T'])
fc = N['forecast']
for k in ('rmse_ar', 'rmse_ms', 'ls_ar', 'ls_ms', 'dm', 'p_dm', 'qps_lowmean', 'qps_const', 'cum_pre08', 'cum_post08', 'ks_ar', 'ks_ms'):
    put(f'fc.{k}', fc[k], 3 if k in ('rmse_ar', 'rmse_ms', 'ls_ar', 'ls_ms', 'qps_lowmean', 'qps_const') else 2)
V.raw('fc.n', str(fc['n']))
V.raw('fc.n.ro', de(fc['n']))
for k_ in ('ks_ar', 'ks_ms'):   # '$p < 0.001$' or '$p = 0.01$'
    V.raw(f'fc.{k_}', '$p < ⁅0.001⁆$' if fc[k_] < 0.001 else '$p = ' + n(fc[k_], 2) + '$')
ai = N['ai']
put('ai.qmin', ai['qmin'], 3)
put('ai.qmax', ai['qmax'], 3)
put('ai.qc', ai['qconst'], 3)
V.raw('ai.n', str(ai['n']))
V.raw('ai.both', str(ai['n_both']))
V.raw('ai.nf', str(ai['n_false']))
V.raw('ai.n01', str(ai['n2001']))
V.raw('ai.n08', str(ai['n2008']))
minus_fix(V)

TB = '>{\\raggedright\\arraybackslash}'

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: when the data-generating process itself changes (recession and expansion, calm and panic, a peg and a float), how do we infer the regime, estimate the model, test it and forecast with it?',
       r'\textbf{Întrebarea}: cînd procesul generator al datelor se schimbă el însuși (recesiune și expansiune, calm și panică, curs fix și curs floating), cum deducem regimul, estimăm modelul, îl testăm și prognozăm cu el?'),
     [T('the regime is never observed: everything rests on its probability given the data', 'regimul nu este observat niciodată: totul se sprijină pe probabilitatea lui condiționată de date')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('the Hamilton filter and the Kim smoother derived; EM and numerical maximum likelihood; identification and label switching',
        'filtrul Hamilton și netezitorul Kim derivate; EM și verosimilitatea maximă numerică; identificare și schimbarea etichetelor'),
      T('testing the number of regimes; time-varying transition probabilities; Markov-switching VAR; Markov-switching GARCH',
        'testarea numărului de regimuri; probabilități de tranziție variabile în timp; VAR cu schimbare de regim; GARCH cu schimbare de regim'),
      T('Bayesian estimation by Gibbs sampling; regimes, long memory and breaks; forecasting and its evaluation',
        'estimarea bayesiană prin eșantionare Gibbs; regimuri, memorie lungă și rupturi; prognoza și evaluarea ei'),
      T('applications: US business cycles, Romanian inflation and GDP, S\\&P 500 and BET, EUR/RON',
        'aplicații: ciclul economic din SUA, inflația și PIB-ul României, S\\&P 500 și BET, EUR/RON')]),
    T('We build on TSA, Chapter 10 (Hamilton\'s model with statsmodels), Chapter 2 (threshold models, breaks) and Chapter 6 (state space, Bayesian filtering); Seminar 7 comes before this lecture',
      'Pornim de la TSA, Capitolul 10 (modelul lui Hamilton cu statsmodels), Capitolul 2 (modele cu prag, rupturi) și Capitolul 6 (spațiul stărilor, filtrare bayesiană); Seminarul 7 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Derive the Hamilton filter, the likelihood and the Kim smoother, and write them in numpy with a numerically stable recursion',
      'Derivați filtrul Hamilton, verosimilitatea și netezitorul Kim și scrieți-le în numpy cu o recursie stabilă numeric'),
    T('Estimate Markov-switching regressions, autoregressions and VARs by EM and by numerical maximum likelihood, and diagnose local and degenerate maxima',
      'Estimați regresii, modele autoregresive și VAR cu schimbare de regim prin EM și prin verosimilitate maximă numerică și diagnosticați maximele locale și degenerate'),
    T('Explain why the likelihood-ratio test for the number of regimes is non-standard, and test by bootstrap and by information criteria',
      'Explicați de ce testul raportului de verosimilitate pentru numărul de regimuri este nestandard și testați prin bootstrap și prin criterii informaționale'),
    T('Specify time-varying transition probabilities, regime-dependent impulse responses and MS-GARCH models without path dependence',
      'Specificați probabilități de tranziție variabile în timp, răspunsuri la impuls dependente de regim și modele MS-GARCH fără dependență de traiectorie'),
    T('Estimate a switching model by Gibbs sampling, handle label switching, and evaluate regime forecasts with scores and probability scores',
      'Estimați un model cu schimbare de regim prin eșantionare Gibbs, tratați schimbarea etichetelor și evaluați prognozele cu reguli de scor și scoruri ale probabilităților')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Backbone: \refHam, Ch.~22; \refKN; \refKro; \refFSb', r'Manualele de bază: \refHam, cap.~22; \refKN; \refKro; \refFSb'),
     [T(r'Surveys: \refHamC; \refAT', r'Sinteze: \refHamC; \refAT')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_07}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_07}'),
     [T(r'Hamilton filter, Kim smoother, EM, expanded-state ML, TVTP, MS-VAR, MS-GARCH and the Gibbs sampler written in \texttt{numpy}',
        r'filtrul Hamilton, netezitorul Kim, EM, verosimilitatea maximă pe starea extinsă, TVTP, MS-VAR, MS-GARCH și eșantionatorul Gibbs scrise în \texttt{numpy}'),
      T(r'comparison: \texttt{statsmodels} \texttt{MarkovRegression} and \texttt{MarkovAutoregression}',
        r'comparație: \texttt{statsmodels} \texttt{MarkovRegression} și \texttt{MarkovAutoregression}')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter7_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter7_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{5.0cm}' + TB + 'p{4.4cm}' + TB + 'p{2.6cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizare}'),
    [T('US real GNP growth, 1951Q2--1984Q4 (Hamilton\'s data); US industrial production and leading indicator, 1948--1991 (Filardo\'s data)',
       'creșterea PNB real al SUA, T2 1951--T4 1984 (datele lui Hamilton); producția industrială și indicatorul avansat din SUA, 1948--1991 (datele lui Filardo)') + ' & ' +
     T('data sets distributed with statsmodels', 'seturi de date distribuite cu statsmodels') + ' & ' + T('replication', 'replicare'),
     T('US real GDP, unemployment rate, NBER recession quarters', 'PIB-ul real și rata șomajului din SUA, trimestrele de recesiune NBER') + ' & FRED (GDPC1, UNRATE, USRECQ) & ' + T('dating, MS-VAR, forecasts', 'datare, MS-VAR, prognoze'),
     T('Romanian real GDP (quarterly) and HICP (monthly)', 'PIB-ul real (trimestrial) și IAPC (lunar) ale României') + ' & Eurostat (namq\\_10\\_gdp, prc\\_hicp\\_minr) & ' + T('Gibbs, inflation regimes', 'Gibbs, regimuri ale inflației'),
     T('S\\&P 500, BET: daily closes', 'S\\&P 500, BET: închideri zilnice') + ' & EODHD (data/market) & MS-GARCH, bull/bear',
     'EUR/RON & ' + T('ECB reference rate to June 2005, BNR reference rate from July 2005', 'cursul de referință BCE pînă în iunie 2005, cursul de referință BNR din iulie 2005') + ' & ' + T('volatility regimes', 'regimuri de volatilitate')],
    size='scriptsize') + items(
    T('All sources are public and need no account or key', 'Toate sursele sînt publice și nu cer cont sau cheie')), 'footnotesize')

D.frame(T('From Markov to Hamilton', 'De la Markov la Hamilton'), two(
    ph('markov', T('Andrey Markov (1856--1922), around 1886', 'Andrei Markov (1856--1922), în jurul anului 1886'), h='0.42\\textheight'),
    items(T('1906--1913: Markov chains, a dependence that needs only the present state', '1906--1913: lanțurile Markov, o dependență care cere doar starea prezentă'),
          T(r'1970: \refBPSW: maximum likelihood for hidden Markov models (the Baum--Welch algorithm, an EM before EM); speech recognition \refRab', r'1970: \refBPSW: verosimilitatea maximă pentru modele Markov ascunse (algoritmul Baum--Welch, un EM înainte de EM); recunoașterea vorbirii \refRab'),
          T(r'1973: \refGQ: switching regressions in econometrics', r'1973: \refGQ: regresii cu schimbare de regim în econometrie'),
          T(r'1989--1990: \refHamA dates US recessions from GNP alone; \refHamB gives the EM algorithm; \refKim the smoother', r'1989--1990: \refHamA datează recesiunile din SUA doar din PNB; \refHamB dă algoritmul EM; \refKim netezitorul'),
          T(r'1993--2006: Bayesian estimation \refAC, \refChibB, \refFSa; MS-VAR \refKro; MS-GARCH \refGray, \refHMP', r'1993--2006: estimarea bayesiană \refAC, \refChibB, \refFSa; MS-VAR \refKro; MS-GARCH \refGray, \refHMP')), '0.34', '0.64'), 'footnotesize')

# =============================================================================
# 1. MODELUL
# =============================================================================
D.section('The model and the Markov chain', 'Modelul și lanțul Markov')

D.frame(T('Known from TSA and new here', 'Cunoscut din TSA și elemente noi'), items(
    (T('Known (TSA, Chapter 10): $y_t = \\mu_{S_t} + \\varepsilon_t$, transition matrix, expected durations, ergodic probabilities, filtered and smoothed probabilities from \\texttt{statsmodels}',
       'Cunoscut (TSA, Capitolul 10): $y_t = \\mu_{S_t} + \\varepsilon_t$, matricea de tranziție, duratele așteptate, probabilitățile ergodice, probabilitățile filtrate și netezite din \\texttt{statsmodels}'),
     [T('US recessions from GDP, Romanian growth regimes, the effect of 2020', 'recesiunile din SUA din PIB, regimurile creșterii din România, efectul anului 2020')]),
    (T('New: every step derived and coded; estimation as an optimisation problem with traps; inference on the number of regimes',
       'Nou: fiecare pas derivat și scris în cod; estimarea ca problemă de optimizare cu capcane; inferența asupra numărului de regimuri'),
     [T('extensions: transitions that depend on covariates, systems (MS-VAR), volatility dynamics (MS-GARCH), Bayesian estimation',
        'extensii: tranziții care depind de covariabile, sisteme (MS-VAR), dinamica volatilității (MS-GARCH), estimare bayesiană')]),
    T('Chapter 2 split the sample by an observed threshold (TAR, STAR) or a date (breaks); here the switch is a latent Markov chain',
      'Capitolul 2 a împărțit eșantionul după un prag observat (TAR, STAR) sau după o dată (rupturi); aici comutarea este un lanț Markov latent')), 'small')

D.frame(T('The model family (Krolzig\'s notation)', 'Familia de modele (notația Krolzig)'), items(
    (T(r'MS($K$)-AR($p$): $y_t = \nu_{S_t} + \sum_{k=1}^p \phi_{k,S_t} y_{t-k} + \sigma_{S_t}\varepsilon_t$, $\varepsilon_t \sim$ i.i.d.\ $N(0, 1)$, $S_t \in \{1, \dots, K\}$',
       r'MS($K$)-AR($p$): $y_t = \nu_{S_t} + \sum_{k=1}^p \phi_{k,S_t} y_{t-k} + \sigma_{S_t}\varepsilon_t$, $\varepsilon_t \sim$ i.i.d.\ $N(0, 1)$, $S_t \in \{1, \dots, K\}$'),
     [T(r'$S_t$: the regime at $t$, one of $K$ values; $\nu_{S_t}$, $\phi_{k,S_t}$, $\sigma_{S_t}$: the intercept, the AR($p$) coefficients and the shock s.d.\ of the current regime', r'$S_t$: regimul la momentul $t$, una dintre $K$ valori; $\nu_{S_t}$, $\phi_{k,S_t}$, $\sigma_{S_t}$: termenul liber, coeficienții AR($p$) și abaterea standard a șocului în regimul curent'),
      T(r'$S_t$ a homogeneous Markov chain, $p_{ij} = \Pr(S_t = j \mid S_{t-1} = i)$, independent of $\varepsilon$ \refKro; $\mathbf{P} = (p_{ij})$: the transition matrix, rows sum to 1', r'$S_t$ un lanț Markov omogen, $p_{ij} = \Pr(S_t = j \mid S_{t-1} = i)$, independent de $\varepsilon$ \refKro; $\mathbf{P} = (p_{ij})$: matricea de tranziție, cu suma pe fiecare rînd egală cu 1')]),
    (T('Which parameters switch gives the name:', 'Parametrii care comută dau numele:'),
     [T(r'\textbf{MSI}: intercept $\nu$; \textbf{MSIH}: intercept and variance; \textbf{MSIAH}: intercept, AR coefficients and variance', r'\textbf{MSI}: termenul liber $\nu$; \textbf{MSIH}: termenul liber și varianța; \textbf{MSIAH}: termenul liber, coeficienții AR și varianța'),
      T(r'\textbf{MSM} (Hamilton 1989): the \emph{mean} $\mu_{S_t}$ switches, $y_t - \mu_{S_t} = \sum_k \phi_k(y_{t-k} - \mu_{S_{t-k}}) + \sigma\varepsilon_t$', r'\textbf{MSM} (Hamilton 1989): comută \emph{media} $\mu_{S_t}$, $y_t - \mu_{S_t} = \sum_k \phi_k(y_{t-k} - \mu_{S_{t-k}}) + \sigma\varepsilon_t$')]),
    T('MSI: after a switch the mean adjusts gradually; MSM: it jumps at once; MSM needs the regimes of $p + 1$ periods', 'MSI: după o comutare media se ajustează treptat; MSM: sare imediat; MSM cere regimurile a $p + 1$ perioade'),
    T(r'Special cases: $p_{ij} = \pi_j$ for all $i$ is an i.i.d.\ mixture; an upper-triangular $\mathbf{P}$ is a change-point model \refChibC', r'Cazuri particulare: $p_{ij} = \pi_j$ pentru orice $i$ dă un amestec i.i.d.; o matrice $\mathbf{P}$ superior triunghiulară dă un model cu puncte de schimbare \refChibC')), 'small')

D.frame(T('The chain: ergodicity, durations, persistence', 'Lanțul: ergodicitate, durate, persistență'), items(
    (T(r'Ergodic probabilities: $\boldsymbol\pi\'\mathbf{P} = \boldsymbol\pi\'$, $\mathbf{1}\'\boldsymbol\pi = 1$; with $K = 2$, $\pi_1 = (1 - p_{22})/(2 - p_{11} - p_{22})$', r'Probabilitățile ergodice: $\boldsymbol\pi\'\mathbf{P} = \boldsymbol\pi\'$, $\mathbf{1}\'\boldsymbol\pi = 1$; pentru $K = 2$, $\pi_1 = (1 - p_{22})/(2 - p_{11} - p_{22})$'),
     [T(r'$\boldsymbol\pi$: the long-run share of time spent in each regime; $\mathbf{1}$: a vector of ones', r'$\boldsymbol\pi$: proporția pe termen lung a timpului petrecut în fiecare regim; $\mathbf{1}$: un vector de unități'),
      T(r'durations are geometric: $\Pr(D_i = d) = p_{ii}^{d-1}(1 - p_{ii})$, $\E D_i = 1/(1 - p_{ii})$ (memoryless); $D_i$: the number of periods a visit to regime $i$ lasts', r'duratele sînt geometrice: $\Pr(D_i = d) = p_{ii}^{d-1}(1 - p_{ii})$, $\E D_i = 1/(1 - p_{ii})$ (fără memorie); $D_i$: numărul de perioade cît durează o vizită în regimul $i$')]),
    (T(r'AR(1) representation \refHam, \S22.2: $\xi_t = \mathbf{1}\{S_t = 1\}$ satisfies $\xi_t = (1 - p_{22}) + \lambda\xi_{t-1} + v_t$, $\lambda = p_{11} + p_{22} - 1$', r'Reprezentarea AR(1) \refHam, \S22.2: $\xi_t = \mathbf{1}\{S_t = 1\}$ verifică $\xi_t = (1 - p_{22}) + \lambda\xi_{t-1} + v_t$, $\lambda = p_{11} + p_{22} - 1$'),
     [T(r'$\mathbf{1}\{\cdot\}$: the indicator (1 if true, 0 otherwise); $v_t$: the innovation; it is a martingale difference, not independent of the past (its variance depends on $S_{t-1}$)', r'$\mathbf{1}\{\cdot\}$: indicatorul (1 dacă este adevărat, 0 altfel); $v_t$: inovația; este o diferență de martingală, dar nu este independentă de trecut (varianța ei depinde de $S_{t-1}$)'),
      T(r'$\Pr(S_{t+h} = 1 \mid S_t) \to \pi_1$ at the rate $\lambda^h$: $\lambda$ is the persistence of the regime process', r'$\Pr(S_{t+h} = 1 \mid S_t) \to \pi_1$ cu viteza $\lambda^h$: $\lambda$ este persistența procesului de regim')]),
    T(r'Duration dependence (recessions that are more likely to end the longer they last) needs an extended state or a semi-Markov chain \refMM', r'Dependența de durată (recesiuni care se încheie mai probabil cu cît durează mai mult) cere o stare extinsă sau un lanț semi-Markov \refMM')), 'small')

chart(T('Durations and the speed of mixing', 'Duratele și viteza de amestecare'), 'ats_ch7_chain', 'ATS_ch7_hamilton', [
    T(r'$p_{11} = 0.9$, $p_{22} = 0.75$: expected durations @{ch.d1} and @{ch.d2} periods; $\pi_1 = @{ch.pi}$; $\lambda = @{ch.lam}$',
      r'$p_{11} = 0{,}9$, $p_{22} = 0{,}75$: durate așteptate de @{ch.d1} și @{ch.d2} perioade; $\pi_1 = @{ch.pi}$; $\lambda = @{ch.lam}$'),
    T('The gap to the ergodic probability shrinks by the factor $\\lambda$ each period: after 10 periods the starting regime is almost forgotten', 'Distanța față de probabilitatea ergodică scade cu factorul $\\lambda$ în fiecare perioadă: după 10 perioade regimul de pornire este aproape uitat')],
    h='0.48\\textheight')

D.recap(('The model', 'modelul'), [
    T('A latent Markov chain selects the parameters of the observation equation', 'Un lanț Markov latent alege parametrii ecuației observațiilor'),
    T('Krolzig\'s letters say what switches; MSM needs the expanded state', 'Literele lui Krolzig spun ce comută; MSM cere starea extinsă'),
    T('Durations are geometric; $\\lambda = p_{11} + p_{22} - 1$ measures persistence', 'Duratele sînt geometrice; $\\lambda = p_{11} + p_{22} - 1$ măsoară persistența')])

# =============================================================================
# 2. FILTRUL HAMILTON ȘI NETEZITORUL KIM
# =============================================================================
D.section('The Hamilton filter and the Kim smoother', 'Filtrul Hamilton și netezitorul Kim')

D.frame(T('The Hamilton filter, derived', 'Filtrul Hamilton, derivat'), items(
    (T(r'Notation: $Y_t = (y_1, \dots, y_t)$, $\hat\xi_{t|s}$ the $K$-vector $\Pr(S_t = j \mid Y_s)$, $\eta_t$ the vector of densities $f(y_t \mid S_t = j, Y_{t-1})$', r'Notație: $Y_t = (y_1, \dots, y_t)$, $\hat\xi_{t|s}$ vectorul $\Pr(S_t = j \mid Y_s)$ de dimensiune $K$, $\eta_t$ vectorul densităților $f(y_t \mid S_t = j, Y_{t-1})$'),
     [T(r'\textbf{prediction} (law of total probability, Markov property): $\hat\xi_{t|t-1} = \mathbf{P}\'\hat\xi_{t-1|t-1}$', r'\textbf{predicția} (probabilitatea totală, proprietatea Markov): $\hat\xi_{t|t-1} = \mathbf{P}\'\hat\xi_{t-1|t-1}$'),
      T(r'\textbf{update} (Bayes): $\hat\xi_{t|t} = \dfrac{\hat\xi_{t|t-1}\odot\eta_t}{\mathbf{1}\'(\hat\xi_{t|t-1}\odot\eta_t)}$', r'\textbf{actualizarea} (Bayes): $\hat\xi_{t|t} = \dfrac{\hat\xi_{t|t-1}\odot\eta_t}{\mathbf{1}\'(\hat\xi_{t|t-1}\odot\eta_t)}$'),
      T(r'\textbf{likelihood}: $f(y_t \mid Y_{t-1}) = \mathbf{1}\'(\hat\xi_{t|t-1}\odot\eta_t)$, so $\ln L = \sum_t \ln f(y_t \mid Y_{t-1})$', r'\textbf{verosimilitatea}: $f(y_t \mid Y_{t-1}) = \mathbf{1}\'(\hat\xi_{t|t-1}\odot\eta_t)$, deci $\ln L = \sum_t \ln f(y_t \mid Y_{t-1})$')]),
    T(r'Start: $\hat\xi_{1|0} = \boldsymbol\pi$ (ergodic) or a free parameter; $\odot$ is the element-wise product', r'Pornire: $\hat\xi_{1|0} = \boldsymbol\pi$ (ergodic) sau un parametru liber; $\odot$ este produsul element cu element'),
    T(r'Same structure as the Kalman filter (Chapter 6): predict, update, prediction-error decomposition; here the state is discrete and the update is exact', r'Aceeași structură ca filtrul Kalman (Capitolul 6): predicție, actualizare, descompunerea erorilor de predicție; aici starea este discretă, iar actualizarea este exactă')), 'small')

D.frame(T('Numerics and cost', 'Aspecte numerice și cost'), items(
    (T(r'Densities underflow (e.g.\ $10^{-300}$ after a large outlier): work with $\ln\eta_t$ and subtract $m_t = \max_j \ln\eta_{jt}$', r'Densitățile ajung sub limita reprezentabilă (de exemplu $10^{-300}$ după o valoare extremă): lucrăm cu $\ln\eta_t$ și scădem $m_t = \max_j \ln\eta_{jt}$'),
     [T(r'$\ln f(y_t \mid Y_{t-1}) = m_t + \ln\sum_j \hat\xi_{j,t|t-1}e^{\ln\eta_{jt} - m_t}$ (log-sum-exp); the filtered vector is unchanged', r'$\ln f(y_t \mid Y_{t-1}) = m_t + \ln\sum_j \hat\xi_{j,t|t-1}e^{\ln\eta_{jt} - m_t}$ (log-sum-exp); vectorul filtrat nu se schimbă')]),
    (T(r'Cost: $O(TK^2)$; with MSM-AR($p$) the state is $(S_t, \dots, S_{t-p})$, $M = K^{p+1}$ ($32$ for Hamilton\'s $K = 2$, $p = 4$)', r'Cost: $O(TK^2)$; la MSM-AR($p$) starea este $(S_t, \dots, S_{t-p})$, $M = K^{p+1}$ ($32$ pentru $K = 2$, $p = 4$ ale lui Hamilton)'),
     [T(r'the expanded transition matrix is sparse: from $(i_0, \dots, i_p)$ only to $(j, i_0, \dots, i_{p-1})$, with probability $p_{i_0 j}$', r'matricea de tranziție extinsă este rară: din $(i_0, \dots, i_p)$ se trece doar în $(j, i_0, \dots, i_{p-1})$, cu probabilitatea $p_{i_0 j}$'),
      T(r'MSI-AR($p$) needs only $K$ states: the lagged $y$ enter as regressors', r'MSI-AR($p$) cere doar $K$ stări: valorile cu lag ale lui $y$ intră ca regresori')]),
    T(r'Our numpy filter and \texttt{statsmodels} give the same log-likelihood to machine precision when the initial distribution is the same', r'Filtrul nostru numpy și \texttt{statsmodels} dau aceeași log-verosimilitate, la precizia mașinii, cînd distribuția inițială este aceeași')), 'small')

D.frame(T('The Kim smoother, derived', 'Netezitorul Kim, derivat'), items(
    (T(r'Goal: $\hat\xi_{t|T}$, the regime probabilities given the whole sample \refKim', r'Scopul: $\hat\xi_{t|T}$, probabilitățile regimurilor date fiind toate datele \refKim'),
     [T(r'key step: $\Pr(S_t = i \mid S_{t+1} = j, Y_T) = \Pr(S_t = i \mid S_{t+1} = j, Y_t)$: given $S_{t+1}$, future $y$ carry no extra information on $S_t$', r'pasul-cheie: $\Pr(S_t = i \mid S_{t+1} = j, Y_T) = \Pr(S_t = i \mid S_{t+1} = j, Y_t)$: dat fiind $S_{t+1}$, valorile viitoare ale lui $y$ nu aduc informație suplimentară despre $S_t$'),
      T(r'exact for MSI/MSIH/MSM on the expanded state; an approximation only when the state also has a continuous part (Kim 1994, Chapter 6)', r'exact pentru MSI/MSIH/MSM pe starea extinsă; aproximare doar cînd starea are și o parte continuă (Kim 1994, Capitolul 6)'),
      T(r'proof of the key step: Appendix  % applink: Kim smoother, the Markov step', r'demonstrația pasului-cheie: Anexa  % applink: netezitorul Kim, pasul Markov')]),
    (T(r'Bayes on the pair: $\Pr(S_t = i, S_{t+1} = j \mid Y_T) = \dfrac{\hat\xi_{i,t|t}\,p_{ij}}{\hat\xi_{j,t+1|t}}\,\hat\xi_{j,t+1|T}$', r'Bayes pentru pereche: $\Pr(S_t = i, S_{t+1} = j \mid Y_T) = \dfrac{\hat\xi_{i,t|t}\,p_{ij}}{\hat\xi_{j,t+1|t}}\,\hat\xi_{j,t+1|T}$'),
     [T(r'sum over $j$: $\hat\xi_{t|T} = \hat\xi_{t|t}\odot\left[\mathbf{P}(\hat\xi_{t+1|T}\oslash\hat\xi_{t+1|t})\right]$, backwards from $\hat\xi_{T|T}$; $\oslash$: element-wise division', r'sumăm după $j$: $\hat\xi_{t|T} = \hat\xi_{t|t}\odot\left[\mathbf{P}(\hat\xi_{t+1|T}\oslash\hat\xi_{t+1|t})\right]$, înapoi de la $\hat\xi_{T|T}$; $\oslash$: împărțirea element cu element')]),
    T(r'The joint probabilities of $(S_t, S_{t+1})$ are the E-step of EM; sampling instead of summing gives FFBS (Section 7)', r'Probabilitățile comune ale perechii $(S_t, S_{t+1})$ sînt pasul E al algoritmului EM; eșantionarea în locul sumării dă FFBS (secțiunea 7)')), 'small')

D.frame(T('Three probabilities, three questions', 'Trei probabilități, trei întrebări'), items(
    (T(r'\textbf{Predicted} $\hat\xi_{t+1|t}$: what a forecaster expects for next period; it enters the forecast density', r'Probabilitatea \textbf{prezisă} $\hat\xi_{t+1|t}$: ce așteaptă un prognozator pentru perioada următoare; intră în densitatea de prognoză'),
     []),
    (T(r'\textbf{Filtered} $\hat\xi_{t|t}$: what could be known at $t$; the real-time signal (Chauvet and Piger 2008)', r'Probabilitatea \textbf{filtrată} $\hat\xi_{t|t}$: ce se putea ști la $t$; semnalul în timp real (Chauvet și Piger 2008)'),
     [T('evaluate real-time dating with filtered probabilities and data vintages, never with smoothed ones', 'datarea în timp real se evaluează cu probabilități filtrate și cu edițiile datelor, niciodată cu cele netezite')]),
    (T(r'\textbf{Smoothed} $\hat\xi_{t|T}$: the historian\'s answer; it uses the future and is revised as data arrive', r'Probabilitatea \textbf{netezită} $\hat\xi_{t|T}$: răspunsul istoricului; folosește viitorul și se revizuiește pe măsură ce sosesc date'),
     [T('the dating of past regimes, and the weights of the M-step', 'datarea regimurilor trecute și ponderile pasului M')]),
    T('Confusing them is the most common error in applied work: a smoothed probability is not a forecast', 'Confuzia lor este cea mai frecventă eroare în lucrările aplicate: o probabilitate netezită nu este o prognoză')), 'small')

D.recap(('Filter and smoother', 'filtru și netezitor'), [
    T('Filter: predict with $\\mathbf{P}\'$, update with Bayes, accumulate the log-likelihood', 'Filtrul: predicție cu $\\mathbf{P}\'$, actualizare cu Bayes, acumularea log-verosimilității'),
    T('Smoother: one backward pass with the ratio of smoothed to predicted probabilities', 'Netezitorul: o trecere înapoi cu raportul dintre probabilitățile netezite și cele prezise'),
    T('Work in logs; expand the state only when the mean switches', 'Se lucrează în logaritmi; starea se extinde doar cînd comută media')])

# =============================================================================
# 3. ESTIMARE
# =============================================================================
D.section('Estimation: EM and numerical maximum likelihood', 'Estimarea: EM și verosimilitatea maximă numerică')

D.frame(T('EM: the complete-data likelihood', 'EM: verosimilitatea datelor complete'), items(
    (T(r'If $S_1, \dots, S_T$ were observed, the log-likelihood would split \refDLR, \refHamB:', r'Dacă $S_1, \dots, S_T$ ar fi observate, log-verosimilitatea s-ar separa \refDLR, \refHamB:'),
     [T(r'$\ln L_c = \sum_j \mathbf{1}\{S_1 = j\}\ln\rho_j + \sum_{t\ge2}\sum_{i,j}\mathbf{1}\{S_{t-1} = i, S_t = j\}\ln p_{ij} + \sum_t\sum_j \mathbf{1}\{S_t = j\}\ln\eta_{jt}(\theta_j)$', r'$\ln L_c = \sum_j \mathbf{1}\{S_1 = j\}\ln\rho_j + \sum_{t\ge2}\sum_{i,j}\mathbf{1}\{S_{t-1} = i, S_t = j\}\ln p_{ij} + \sum_t\sum_j \mathbf{1}\{S_t = j\}\ln\eta_{jt}(\theta_j)$'),
      T(r'$\rho_j = \Pr(S_1 = j)$: initial probabilities; $\eta_{jt}(\theta_j)$: the density of $y_t$ in regime $j$, with parameters $\theta_j$', r'$\rho_j = \Pr(S_1 = j)$: probabilitățile inițiale; $\eta_{jt}(\theta_j)$: densitatea lui $y_t$ în regimul $j$, cu parametrii $\theta_j$'),
      T(r'transition counts and regime-by-regime regressions: closed forms', r'numărarea tranzițiilor și regresii regim cu regim: forme închise')]),
    (T(r'\textbf{E-step}: replace the indicators by their expectations given $Y_T$ and the current $\theta^{(m)}$ ($m$: the iteration)', r'\textbf{Pasul E}: înlocuim indicatorii cu speranțele lor condiționate de $Y_T$ și de $\theta^{(m)}$ curent ($m$: iterația)'),
     [T(r'$\hat\xi_{j,t|T}$ and $\hat\xi_{ij,t|T} = \Pr(S_{t-1} = i, S_t = j \mid Y_T)$: exactly the output of the Kim smoother', r'$\hat\xi_{j,t|T}$ și $\hat\xi_{ij,t|T} = \Pr(S_{t-1} = i, S_t = j \mid Y_T)$: exact ieșirea netezitorului Kim')]),
    T('Baum et al.\\ (1970) derived the same recursion for hidden Markov models (the forward--backward algorithm)', 'Baum et al.\\ (1970) au derivat aceeași recursie pentru modelele Markov ascunse (algoritmul forward--backward)')), 'small')

D.frame(T('EM: the M-step in closed form', 'EM: pasul M în formă închisă'), items(
    T(r'Transitions: $p_{ij}^{(m+1)} = \dfrac{\sum_{t=2}^T \hat\xi_{ij,t|T}}{\sum_{t=2}^T \hat\xi_{i,t-1|T}}$ (expected transitions over expected visits); $\rho^{(m+1)} = \hat\xi_{1|T}$', r'Tranzițiile: $p_{ij}^{(m+1)} = \dfrac{\sum_{t=2}^T \hat\xi_{ij,t|T}}{\sum_{t=2}^T \hat\xi_{i,t-1|T}}$ (tranziții așteptate raportate la vizite așteptate); $\rho^{(m+1)} = \hat\xi_{1|T}$'),
    T(r'Switching coefficients (MSIAH): weighted least squares $\beta_j^{(m+1)} = (X\'W_jX)^{-1}X\'W_jy$, $W_j = \mathrm{diag}(\hat\xi_{j,t|T})$; $X$: rows $x_t\'$ (constant and lags), $y$: the observations; each date weighs by its probability of being in regime $j$', r'Coeficienți care comută (MSIAH): cele mai mici pătrate ponderate $\beta_j^{(m+1)} = (X\'W_jX)^{-1}X\'W_jy$, $W_j = \mathrm{diag}(\hat\xi_{j,t|T})$; $X$: liniile $x_t\'$ (constanta și lagurile), $y$: observațiile; fiecare dată contează cu probabilitatea de a fi în regimul $j$'),
    T(r'Variances: $\sigma_j^{2(m+1)} = \sum_t\hat\xi_{j,t|T}(y_t - x_t\'\beta_j)^2/\sum_t\hat\xi_{j,t|T}$; MS-VAR: the same with matrices', r'Varianțele: $\sigma_j^{2(m+1)} = \sum_t\hat\xi_{j,t|T}(y_t - x_t\'\beta_j)^2/\sum_t\hat\xi_{j,t|T}$; MS-VAR: același lucru cu matrice'),
    T(r'Common coefficients (MSIH-AR): one stacked weighted regression with weights $\hat\xi_{j,t|T}/\sigma_j^2$ (a conditional M-step, ECM)', r'Coeficienți comuni (MSIH-AR): o singură regresie ponderată stivuită, cu ponderile $\hat\xi_{j,t|T}/\sigma_j^2$ (un pas M condiționat, ECM)'),
    T(r'MSM-AR: $\mu$ and $\phi$ enter as products, so no closed form: numerical maximisation (or EM with a numerical M-step)', r'MSM-AR: $\mu$ și $\phi$ apar ca produse, deci nu există formă închisă: maximizare numerică (sau EM cu un pas M numeric)'),
    T(r'Derivation of the M-step for $\mathbf{P}$ and of the monotonicity of EM: Appendix  % applink: EM for the Markov chain', r'Derivarea pasului M pentru $\mathbf{P}$ și a monotoniei EM: Anexa  % applink: EM pentru lanțul Markov')), 'small')

D.frame(T('EM and numerical ML in practice', 'EM și verosimilitatea maximă numerică în practică'), items(
    (T('EM never lowers the likelihood, is robust far from the optimum, but slow near it (linear convergence)', 'EM nu scade niciodată verosimilitatea, este robust departe de optim, dar lent în apropierea lui (convergență liniară)'),
     [T(r'monotonicity needs $\rho$ as a free parameter; with $\rho = \boldsymbol\pi(\mathbf{P})$ the M-step for $\mathbf{P}$ is only approximate', r'monotonia cere ca $\rho$ să fie un parametru liber; cu $\rho = \boldsymbol\pi(\mathbf{P})$ pasul M pentru $\mathbf{P}$ este doar aproximativ')]),
    (T(r'Numerical ML: BFGS on unconstrained parameters ($\ln\sigma_j^2$, logits of $p_{ij}$); standard errors from the Hessian by the delta method', r'Verosimilitatea maximă numerică: BFGS pe parametri fără restricții ($\ln\sigma_j^2$, logit-urile lui $p_{ij}$); erorile standard din hessiană prin metoda delta'),
     [T('practice: EM from many starts, then a Newton-type polish and the Hessian', 'în practică: EM din multe puncte de pornire, apoi o rafinare de tip Newton și hessiana')]),
    (T(r'The likelihood is unbounded: $\sigma_j \to 0$ around one observation with $p_{jj} \to 0$ gives $\ln L \to \infty$', r'Verosimilitatea este nemărginită: $\sigma_j \to 0$ în jurul unei observații, cu $p_{jj} \to 0$, dă $\ln L \to \infty$'),
     [T(r'remedies: a lower bound on $\sigma_j/\sigma_k$ \refHath, priors (Section 7), or reject regimes that last one period', r'remedii: o limită inferioară pentru $\sigma_j/\sigma_k$ \refHath, distribuții a priori (secțiunea 7) sau respingerea regimurilor care durează o singură perioadă')]),
    T('Standard errors near the boundary ($p_{ii} \\approx 1$) are unreliable: report profile likelihoods or bootstrap intervals', 'Erorile standard lîngă frontieră ($p_{ii} \\approx 1$) nu sînt de încredere: raportați verosimilitatea de profil sau intervale bootstrap')), 'small')

chart(T('EM from @{em.n} starting values', 'EM din @{em.n.ro} puncte de pornire'), 'ats_ch7_em', 'ATS_ch7_estimation', [
    T(r'MSIH(2)-AR(1) on Hamilton\'s GNP data: switching intercept and variance, common AR(1) coefficient; random starting values; log scale for iterations',
      r'MSIH(2)-AR(1) pe datele PNB ale lui Hamilton: termen liber și varianță care comută, coeficient AR(1) comun; puncte de pornire aleatoare; scară logaritmică pentru iterații')],
    h='0.5\\textheight')

interp(('the EM paths', 'traiectoriilor EM'), [
    T(r'@{em.ng} limits (log-likelihood, number of starts): @{em.groups}; median @{em.itmed} iterations, at most @{em.itmax}', r'@{em.ng} limite (log-verosimilitatea, numărul de puncte de pornire): @{em.groups}; în mediană @{em.itmed} de iterații, cel mult @{em.itmax}'),
    T(r'The highest (@{em.top}) is \textbf{degenerate}: a regime with $\sigma^2 = @{em.dg.s}$, $p_{11}$ @{em.dg.p} and mean @{em.dg.mu}, used by @{em.dg.n} isolated quarters', r'Cea mai înaltă (@{em.top}) este \textbf{degenerată}: un regim cu $\sigma^2 = @{em.dg.s}$, $p_{11}$ @{em.dg.p} și media @{em.dg.mu}, folosit de @{em.dg.n.ro} trimestre izolate'),
    T(r'\texttt{statsmodels} (20 random searches) reports @{em.sm}, a third local maximum that none of our starts reached', r'\texttt{statsmodels} (20 de căutări aleatoare) raportează @{em.sm}, un al treilea maxim local, pe care niciunul dintre punctele noastre de pornire nu l-a atins'),
    T('Lesson: report the starting-value design, all local maxima, and why the chosen one is economically meaningful', 'Lecția: raportați schema punctelor de pornire, toate maximele locale și motivul pentru care cel ales are sens economic')])

D.frame(T('Identification and label switching', 'Identificare și schimbarea etichetelor'), items(
    (T(r'The likelihood is invariant to the $K!$ permutations of the labels: $(\theta_1, \theta_2, \mathbf{P})$ and $(\theta_2, \theta_1, \mathbf{\Pi P\Pi}\')$ fit equally well', r'Verosimilitatea este invariantă la cele $K!$ permutări ale etichetelor: $(\theta_1, \theta_2, \mathbf{P})$ și $(\theta_2, \theta_1, \mathbf{\Pi P\Pi}\')$ se potrivesc la fel de bine'),
     [T('for ML this is harmless: pick one mode and name the regimes by an ordering ($\\mu_1 < \\mu_2$ or $\\sigma_1 < \\sigma_2$)', 'pentru verosimilitatea maximă este inofensiv: alegem un mod și numim regimurile după o ordonare ($\\mu_1 < \\mu_2$ sau $\\sigma_1 < \\sigma_2$)'),
      T(r'for MCMC it is not: the sampler jumps between modes and posterior means of $\mu_1$ average the regimes \refCHR, \refSte', r'pentru MCMC nu este: eșantionatorul sare între moduri, iar media a posteriori a lui $\mu_1$ amestecă regimurile \refCHR, \refSte')]),
    (T(r'Identification also fails locally: $K$ regimes with $\theta_i = \theta_j$, or a regime never visited, leave $\mathbf{P}$ unidentified', r'Identificarea eșuează și local: $K$ regimuri cu $\theta_i = \theta_j$ sau un regim nevizitat lasă $\mathbf{P}$ neidentificat'),
     [T('this is the root of the testing problem of the next section', 'aceasta este rădăcina problemei de testare din secțiunea următoare')]),
    T('Statistical regimes need not be economic regimes: the same GDP data give recessions (MSM), volatility eras (MSIH) or single outliers', 'Regimurile statistice nu sînt neapărat regimuri economice: aceleași date de PIB dau recesiuni (MSM), ere de volatilitate (MSIH) sau valori extreme izolate')), 'small')

D.recap(('Estimation', 'estimarea'), [
    T('EM = Kim smoother + weighted regressions + transition counts', 'EM = netezitorul Kim + regresii ponderate + numărarea tranzițiilor'),
    T('Many starts, then a numerical polish; inspect every local maximum', 'Multe puncte de pornire, apoi o rafinare numerică; inspectați fiecare maxim local'),
    T('Degenerate maxima and label switching are features of mixtures, not bugs of the code', 'Maximele degenerate și schimbarea etichetelor sînt trăsături ale amestecurilor, nu erori ale codului')])

# =============================================================================
# 4. NUMĂRUL DE REGIMURI
# =============================================================================
D.section('The number of regimes: testing and selection', 'Numărul de regimuri: testare și selecție')

D.frame(T('The non-standard LR test', 'Testul LR nestandard'), items(
    (T(r'$H_0$: one regime ($\mu_1 = \mu_2$, $\sigma_1 = \sigma_2$) against $H_1$: two regimes', r'$H_0$: un singur regim ($\mu_1 = \mu_2$, $\sigma_1 = \sigma_2$) față de $H_1$: două regimuri'),
     [T(r'(i) under $H_0$, $p_{11}$ and $p_{22}$ are \textbf{not identified}: nuisance parameters present only under $H_1$, the Davies problem of Chapter 2 \refDav', r'(i) sub $H_0$, $p_{11}$ și $p_{22}$ \textbf{nu sînt identificați}: parametri de perturbare prezenți doar sub $H_1$, problema Davies din Capitolul 2 \refDav'),
      T(r'(ii) the null can be written as $p_{11} = 1$: a parameter on the \textbf{boundary}', r'(ii) ipoteza nulă se poate scrie $p_{11} = 1$: un parametru pe \textbf{frontieră}'),
      T(r'(iii) the score with respect to $\mu_2 - \mu_1$ is \textbf{identically zero} at $H_0$: the information matrix is singular', r'(iii) scorul în raport cu $\mu_2 - \mu_1$ este \textbf{identic zero} sub $H_0$: matricea informațională este singulară')]),
    T(r'Each of the three breaks one of the conditions for $2\ln\Lambda \to \chi^2_q$ ($\Lambda$: the likelihood ratio; $q$: the number of restrictions): counting parameters does not give the critical value', r'Fiecare dintre cele trei încalcă una dintre condițiile pentru $2\ln\Lambda \to \chi^2_q$ ($\Lambda$: raportul de verosimilitate; $q$: numărul de restricții): numărarea parametrilor nu dă valoarea critică'),
    T('Same structure as testing linearity against TAR or STAR (Chapter 2), with a latent instead of an observed switch', 'Aceeași structură ca testarea liniarității față de TAR sau STAR (Capitolul 2), cu o comutare latentă în locul uneia observate')), 'small')

D.frame(T('Solutions in the literature', 'Soluțiile din literatură'), items(
    (T(r'\refHan: treat the likelihood as an empirical process in the nuisance parameters and bound the standardised LR; conservative, heavy to compute', r'\refHan: tratează verosimilitatea ca un proces empiric în parametrii de perturbare și mărginește LR standardizat; conservator, greu de calculat'),
     [T(r'applied to Hamilton\'s GNP model: no evidence against one regime at conventional levels', r'aplicat modelului PNB al lui Hamilton: nicio dovadă împotriva unui singur regim la nivelurile uzuale')]),
    T(r'\refGar: the asymptotic null distribution of the sup-LR for MS models with switching mean (and variance), with tabulated critical values', r'\refGar: distribuția asimptotică sub $H_0$ a statisticii sup-LR pentru modele cu medie (și varianță) care comută, cu valori critice tabelate'),
    T(r'\refCW: quasi-LR against a two-component mixture (an i.i.d.\ switch has the same null behaviour)', r'\refCW: quasi-LR față de un amestec cu două componente (o comutare i.i.d.\ are același comportament sub $H_0$)'),
    T(r'\refCHP: an optimal score-type test against Markov switching that needs only the null model', r'\refCHP: un test optim de tip scor față de schimbarea de regim de tip Markov, care cere doar modelul nul'),
    (T(r'Practice: \textbf{parametric bootstrap} of the LR', r'În practică: \textbf{bootstrap parametric} al LR'),
     [T('simulate from the estimated null; re-estimate both models (with several starts) on each sample', 'simulăm din modelul nul estimat; reestimăm ambele modele (cu mai multe puncte de pornire) pe fiecare eșantion'),
      T(r'$p = (1 + \#\{LR^* \ge LR\})/(B + 1)$; $LR^*$: the $B$ bootstrap statistics; $\#$: their count above $LR$', r'$p = (1 + \#\{LR^* \ge LR\})/(B + 1)$; $LR^*$: cele $B$ statistici bootstrap; $\#$: numărul celor mai mari decît $LR$')]),
    T(r'Selection rather than testing: AIC, BIC, HQ, or Bayes factors through the marginal likelihood \refChibA', r'Selecție în loc de testare: AIC, BIC, HQ sau factori Bayes prin verosimilitatea marginală \refChibA')), 'small')

chart(T('The bootstrap null distribution of the LR statistic', 'Distribuția bootstrap a statisticii LR sub ipoteza nulă'), 'ats_ch7_lrtest', 'ATS_ch7_estimation', [
    T(r'US GDP growth, 1947Q2--2019Q4 ($T = @{lr.T}$): $H_0$ Gaussian AR(1), $H_1$ MSIH(2)-AR(1); @{lr.B} samples simulated from the estimated AR(1), both models re-estimated, EM with 4 starts',
      r'Creșterea PIB-ului SUA, T2 1947--T4 2019 ($T = @{lr.T}$): $H_0$ AR(1) Gaussian, $H_1$ MSIH(2)-AR(1); @{lr.B} de eșantioane simulate din AR(1) estimat, ambele modele reestimate, EM cu 4 puncte de pornire')],
    h='0.5\\textheight')

interp(('the test', 'testului'), [
    T(r'Bootstrap 95\% quantile @{lr.q95}, against @{lr.c2} ($\chi^2_2$) and @{lr.c4} ($\chi^2_4$); mean of the null draws @{lr.mean}: counting parameters gets the critical value wrong', r'Cuantila bootstrap de 95\% este @{lr.q95}, față de @{lr.c2} ($\chi^2_2$) și @{lr.c4} ($\chi^2_4$); media extragerilor sub $H_0$ @{lr.mean}: numărarea parametrilor dă o valoare critică greșită'),
    T(r'Observed LR = @{lr.LR}, bootstrap $p$-value @{lr.p} (the smallest possible with $B = @{lr.B}$): two regimes', r'LR observat = @{lr.LR}, p-value-ul bootstrap @{lr.p} (cea mai mică posibilă cu $B = @{lr.B}$): două regimuri'),
    T(r'But which regimes? Standard deviations @{lr.s0} and @{lr.s1} pp, $p_{ii}$ = @{lr.P0} and @{lr.P1}: volatility eras (the Great Moderation), not recessions', r'Dar ce regimuri? Abaterile standard @{lr.s0} și @{lr.s1} pp, $p_{ii}$ = @{lr.P0} și @{lr.P1}: ere de volatilitate (Marea Moderație), nu recesiuni'),
    T(r'BIC: @{lr.BIC1} ($K = 1$), @{lr.BIC2} ($K = 2$), @{lr.BIC3} ($K = 3$); AIC: @{lr.AIC1}, @{lr.AIC2}, @{lr.AIC3}', r'BIC: @{lr.BIC1} ($K = 1$), @{lr.BIC2} ($K = 2$), @{lr.BIC3} ($K = 3$); AIC: @{lr.AIC1}; @{lr.AIC2}; @{lr.AIC3}')])

D.recap(('The number of regimes', 'numărul de regimuri'), [
    T('Unidentified nuisance parameters, a boundary and a zero score: no chi-square limit', 'Parametri de perturbare neidentificați, o frontieră și un scor nul: nicio limită chi-pătrat'),
    T('Use bootstrap $p$-values or Garcia-type critical values; information criteria for selection', 'Folosiți p-value-uri bootstrap sau valori critice de tip Garcia; criterii informaționale pentru selecție'),
    T('A significant test says that the model fits better, not that the regimes mean what we hoped', 'Un test semnificativ spune că modelul se potrivește mai bine, nu că regimurile înseamnă ce am sperat')])

# =============================================================================
# 5. STUDIU DE CAZ: HAMILTON (1989)
# =============================================================================
D.section('Case study: Hamilton (1989) and the business cycle', 'Studiu de caz: Hamilton (1989) și ciclul economic')

D.frame(T('The paper', 'Lucrarea'), two(
    ph('soup', T('Chicago, February 1931: the regime every forecaster fears', 'Chicago, februarie 1931: regimul de care se teme orice prognozator'), h='0.34\\textheight'),
    items(T(r'\refHamA, Section 4: US real GNP, 100 $\times$ log change, 1951Q2--1984Q4, MSM(2)-AR(4)', r'\refHamA, secțiunea 4: PNB real al SUA, 100 $\times$ variația logaritmului, T2 1951--T4 1984, MSM(2)-AR(4)'),
          T('Equation (4.3): $y_t - \\mu_{S_t} = \\sum_{k=1}^4\\phi_k(y_{t-k} - \\mu_{S_{t-k}}) + \\sigma\\varepsilon_t$; estimates in Table I', 'Ecuația (4.3): $y_t - \\mu_{S_t} = \\sum_{k=1}^4\\phi_k(y_{t-k} - \\mu_{S_{t-k}}) + \\sigma\\varepsilon_t$; estimațiile în Tabelul I'),
          T('The claim: the dates where the low-growth regime is likely match the NBER recessions, although the NBER dates were never used', 'Afirmația: datele în care regimul de creștere scăzută este probabil coincid cu recesiunile NBER, deși datele NBER nu au fost folosite'),
          T(r'We replicate on his data set, compare numpy with \texttt{statsmodels}, then re-estimate on today\'s GDP', r'Replicăm pe setul lui de date, comparăm numpy cu \texttt{statsmodels}, apoi reestimăm pe PIB-ul de azi')), '0.36', '0.62'), 'footnotesize')

D.frame(T('Replication: Hamilton\'s data, two implementations', 'Replicare: datele lui Hamilton, două implementări'), table(
    'lcccccccc', T(r'\textbf{Estimate}', r'\textbf{Estimarea}') + r' & $\mu_0$ & $\mu_1$ & $\phi_1$ & $\phi_2$ & $\phi_3$ & $\phi_4$ & $\sigma$ & $\ln L$',
    [r'numpy & @{hp.mu0} & @{hp.mu1} & @{hp.phi1} & @{hp.phi2} & @{hp.phi3} & @{hp.phi4} & @{hp.sig} & @{hp.ll}',
     T('(standard error)', '(eroarea standard)') + r' & (@{hp.se0}) & (@{hp.se1}) & (@{hp.se2}) & (@{hp.se3}) & (@{hp.se4}) & (@{hp.se5}) & & ',
     r'statsmodels & @{hs.mu0} & @{hs.mu1} & @{hs.phi1} & @{hs.phi2} & @{hs.phi3} & @{hs.phi4} & @{hs.sig} & @{hs.ll}'],
    size='scriptsize') + items(
    T(r'Transitions: $p_{00} = @{hp.p00}$ (stay in the low regime), $p_{11} = @{hp.p11}$; expected durations @{hp.d0} and @{hp.d1} quarters; $T = @{hp.T}$ after 4 lags',
      r'Tranziții: $p_{00} = @{hp.p00}$ (rămînerea în regimul scăzut), $p_{11} = @{hp.p11}$; durate așteptate de @{hp.d0} și @{hp.d1} trimestre; $T = @{hp.T}$ după 4 laguri'),
    T(r'Largest difference between the two smoothed probability paths: @{hs.diff}', r'Cea mai mare diferență între cele două traiectorii ale probabilităților netezite: @{hs.diff}'),
    T('Estimation: BFGS on the expanded state of 32 regime combinations, 8 random starts; standard errors from the numerical Hessian', 'Estimarea: BFGS pe starea extinsă de 32 de combinații de regimuri, 8 puncte de pornire aleatoare; erorile standard din hessiana numerică')), 'small')

chart(T('Hamilton\'s regimes then and now', 'Regimurile lui Hamilton atunci și acum'), 'ats_ch7_hamilton89', 'ATS_ch7_hamilton', [
    T(r'Left: smoothed probability of the low-growth regime on Hamilton\'s data. Right: the same specification on today\'s GDPC1, estimated on 1953Q2--2019Q4 ($T = @{ht.T}$), probabilities to @{ht.lastq} with the same parameters',
      r'Stînga: probabilitatea netezită a regimului de creștere scăzută pe datele lui Hamilton. Dreapta: aceeași specificație pe GDPC1 de azi, estimată pe T2 1953--T4 2019 ($T = @{ht.T}$), probabilități pînă în @{ht.lastq} cu aceiași parametri')],
    h='0.5\\textheight')

interp(('the replication', 'replicării'), [
    T(r'On his data, the regime tracks the NBER: QPS @{hq.qps} and @{hq.conc}\% concordance (probability above 0.5 against the NBER quarters) \refDR, \refHP', r'Pe datele lui, regimul urmărește datările NBER: QPS @{hq.qps} și concordanță de @{hq.conc}\% (probabilitate peste 0,5 comparată cu trimestrele NBER) \refDR, \refHP'),
    T(r'On today\'s data the low regime changes nature: mean @{ht.mu0}\%, $p_{00} = @{ht.p00}$ (duration @{ht.d0} quarters): single sharp falls, not recessions', r'Pe datele de azi, regimul scăzut își schimbă natura: media @{ht.mu0}\%, $p_{00} = @{ht.p00}$ (durata @{ht.d0} trimestre): căderi bruște izolate, nu recesiuni'),
    T(r'It catches 2008Q4 (@{ht.p2008}) and 2020Q2 (@{ht.p2020}) but not 2001 (at most @{ht.p2001}); QPS @{ht.qps} on @{ht.nrec} NBER quarters', r'Prinde T4 2008 (@{ht.p2008}) și T2 2020 (@{ht.p2020}), dar nu 2001 (cel mult @{ht.p2001}); QPS @{ht.qps} pe @{ht.nrec.ro} trimestre NBER'),
    T('After 1984 recessions are rarer and milder (the Great Moderation): a fixed two-mean model loses its grip; this motivates TVTP, MSIH and three regimes', 'După 1984 recesiunile sînt mai rare și mai blînde (Marea Moderație): un model fix cu două medii își pierde puterea; de aici TVTP, MSIH și trei regimuri')])

chart(T('Dating in pseudo real time', 'Datarea în pseudo timp real'), 'ats_ch7_realtime', 'ATS_ch7_hamilton', [
    T(r'Hamilton\'s model re-estimated every year on the data available then (current vintage, no data revisions); filtered probability of each quarter with information up to that quarter, 1990--2026',
      r'Modelul lui Hamilton reestimat în fiecare an pe datele disponibile atunci (ediția curentă, fără revizuiri ale datelor); probabilitatea filtrată a fiecărui trimestru cu informația de pînă la acel trimestru, 1990--2026')],
    h='0.48\\textheight')

interp(('real-time dating', 'datării în timp real'), [
    T(r'First quarter above 0.5: 1990--91 @{rt.1990} (maximum @{rt.1990.max}), 2001 @{rt.2001} (maximum @{rt.2001.max}), 2008 @{rt.2008}, 2020 @{rt.2020}', r'Primul trimestru peste 0,5: 1990--91 @{rt.1990} (maximum @{rt.1990.max}), 2001 @{rt.2001} (maximum @{rt.2001.max}), 2008 @{rt.2008}, 2020 @{rt.2020}'),
    T(r'QPS before 2020: @{rt.qps} in real time against @{rt.qpss} smoothed; @{rt.false} false signals above 0.5', r'QPS înainte de 2020: @{rt.qps} în timp real față de @{rt.qpss} netezit; @{rt.false} semnale false peste 0,5'),
    T(r'\refCP: with real-time vintages, MS models call the start of recessions faster than the NBER announcement, but mild recessions are missed', r'\refCP: cu ediții în timp real, modelele MS semnalează începutul recesiunilor mai repede decît anunțul NBER, dar recesiunile ușoare sînt ratate'),
    T('Our exercise flatters the model: today\'s revised GDP was not available in 2001', 'Exercițiul nostru avantajează modelul: PIB-ul revizuit de azi nu era disponibil în 2001')])

D.recap(('Hamilton (1989)', 'studiul de caz Hamilton (1989)'), [
    T('Replicated exactly on his data with two independent implementations', 'Replicat exact pe datele lui cu două implementări independente'),
    T('The same model on today\'s data finds short sharp contractions and misses 2001', 'Același model pe datele de azi găsește contracții scurte și bruște și ratează 2001'),
    T('Judge dating in real time with filtered probabilities, not with smoothed ones', 'Datarea se judecă în timp real cu probabilități filtrate, nu cu cele netezite')])

# =============================================================================
# 6. TVTP
# =============================================================================
D.section('Time-varying transition probabilities', 'Probabilități de tranziție variabile în timp')

D.frame(T('Letting the chain depend on observables', 'Lanțul dependent de variabile observate'), items(
    (T(r'\refDLW, \refFil: $p_{ii,t} = \Pr(S_t = i \mid S_{t-1} = i, z_{t-1}) = \dfrac{\exp(z_{t-1}\'\gamma_i)}{1 + \exp(z_{t-1}\'\gamma_i)}$', r'\refDLW, \refFil: $p_{ii,t} = \Pr(S_t = i \mid S_{t-1} = i, z_{t-1}) = \dfrac{\exp(z_{t-1}\'\gamma_i)}{1 + \exp(z_{t-1}\'\gamma_i)}$'),
     [T(r'$z_{t-1}$: observed variables known at $t - 1$ (with a constant); $\gamma_i$: their coefficients; the logistic function keeps $p_{ii,t}$ in $(0, 1)$', r'$z_{t-1}$: variabile observate cunoscute la $t - 1$ (cu o constantă); $\gamma_i$: coeficienții lor; funcția logistică menține $p_{ii,t}$ în $(0, 1)$'),
      T('a leading indicator, the term spread or a policy rate can make a recession more or less likely to begin or end', 'un indicator avansat, panta curbei randamentelor sau dobînda de politică pot face mai probabil sau mai puțin probabil începutul sau sfîrșitul unei recesiuni'),
      T('expected durations now vary over time; the chain is no longer homogeneous', 'duratele așteptate variază acum în timp; lanțul nu mai este omogen')]),
    (T(r'Filter and smoother unchanged, with $\mathbf{P}_t$ in place of $\mathbf{P}$; EM: the M-step for $\gamma_i$ is a weighted logit (DLW)', r'Filtrul și netezitorul rămîn neschimbate, cu $\mathbf{P}_t$ în locul lui $\mathbf{P}$; EM: pasul M pentru $\gamma_i$ este un logit ponderat (DLW)'),
     [T(r'$z_{t-1}$ must be predetermined and must not depend on $S_t$; if $z$ reacts to the regime, the model is misspecified (endogenous switching)', r'$z_{t-1}$ trebuie să fie predeterminat și să nu depindă de $S_t$; dacă $z$ reacționează la regim, modelul este greșit specificat (comutare endogenă)')]),
    T(r'Test of constant transitions: $H_0$: slopes of $\gamma_i = 0$ is a standard LR test, since the regimes exist under both hypotheses', r'Testul tranzițiilor constante: $H_0$: pantele lui $\gamma_i$ sînt zero este un test LR standard, deoarece regimurile există sub ambele ipoteze')), 'small')

D.frame(T('Replication: Filardo (1994)', 'Replicare: Filardo (1994)'), table(
    'lcccccc', T(r'\textbf{Model}', r'\textbf{Modelul}') + r' & $\mu_0$ & $\mu_1$ & $\gamma_0$ & $\gamma_1$ & $\ln L$ & statsmodels',
    [T('TVTP, numpy', 'TVTP, numpy') + r' & @{tv.mu0} & @{tv.mu1} & (@{tv.g0}; @{tv.g1}) & (@{tv.g2}; @{tv.g3}) & @{tv.ll} & @{tv.sm}',
     T('(standard error)', '(eroarea standard)') + r' & & & (@{tv.s0}; @{tv.s1}) & (@{tv.s2}; @{tv.s3}) & & ',
     T('constant transitions', 'tranziții constante') + r' & & @{tv.mc1} & $p_{00} = @{tv.pc0}$ & $p_{11} = @{tv.pc1}$ & @{tv.llc} & '],
    size='scriptsize') + items(
    T(r'US industrial production growth, monthly, $T = @{tv.T}$ (Filardo\'s data); MSM(2)-AR(4); $z_{t-1}$ = (1, growth of the composite leading indicator)', r'Creșterea producției industriale din SUA, lunar, $T = @{tv.T}$ (datele lui Filardo); MSM(2)-AR(4); $z_{t-1}$ = (1, creșterea indicatorului compozit avansat)'),
    T(r'LR of TVTP against constant transitions: @{tv.LR} ($p = @{tv.p}$, 2 restrictions)', r'LR pentru TVTP față de tranziții constante: @{tv.LR} ($p = @{tv.p}$, 2 restricții)'),
    T(r'The constant-transition maximum is not a business cycle: a high-mean regime (@{tv.mc1}\% per month) that lasts about one month', r'Maximul cu tranziții constante nu este un ciclu economic: un regim cu medie mare (@{tv.mc1}\% pe lună) care durează aproximativ o lună')), 'small')

chart(T('Transition probabilities driven by the leading indicator', 'Probabilități de tranziție determinate de indicatorul avansat'), 'ats_ch7_tvtp', 'ATS_ch7_tvtp', [
    T('Top: smoothed probability of the low-growth regime; bottom: the probabilities of staying in each regime, month by month', 'Sus: probabilitatea netezită a regimului de creștere scăzută; jos: probabilitățile de rămînere în fiecare regim, lună de lună')],
    h='0.5\\textheight')

interp(('TVTP', 'TVTP'), [
    T(r'Stay in expansion: median @{tv.med}, but down to @{tv.min} when the leading indicator falls sharply: expansions end when the indicator turns', r'Rămînerea în expansiune: mediana @{tv.med}, dar coboară pînă la @{tv.min} cînd indicatorul avansat scade puternic: expansiunile se încheie cînd indicatorul se întoarce'),
    T(r'Stay in recession falls when the indicator rises ($\gamma$ slope @{tv.g1}): recoveries are announced by the indicator', r'Rămînerea în recesiune scade cînd indicatorul crește (panta $\gamma$ @{tv.g1}): revenirile sînt anunțate de indicator'),
    T(r'QPS against the NBER months @{tv.qps}, concordance @{tv.conc}\%', r'QPS față de lunile NBER @{tv.qps}, concordanță @{tv.conc}\%'),
    T('Caveat: the leading indicator was built knowing the NBER dates; a real-time test needs its vintages', 'Atenție: indicatorul avansat a fost construit cunoscînd datele NBER; un test în timp real cere edițiile lui')])

# =============================================================================
# 7. MS-VAR
# =============================================================================
D.section('Markov-switching VARs', 'Modele VAR cu schimbare de regim')

D.frame(T('MS-VAR and regime-dependent responses', 'MS-VAR și răspunsuri dependente de regim'), items(
    (T(r'MSIAH($K$)-VAR($p$): $y_t = \nu_{S_t} + \sum_{k=1}^p A_{k,S_t}y_{t-k} + \Sigma_{S_t}^{1/2}\varepsilon_t$, $y_t \in \R^n$ \refKro', r'MSIAH($K$)-VAR($p$): $y_t = \nu_{S_t} + \sum_{k=1}^p A_{k,S_t}y_{t-k} + \Sigma_{S_t}^{1/2}\varepsilon_t$, $y_t \in \R^n$ \refKro'),
     [T(r'$\nu_{S_t}$, $A_{k,S_t}$, $\Sigma_{S_t}$: intercept vector, lag matrices and error covariance of the current regime; $\varepsilon_t \sim N(0, I_n)$', r'$\nu_{S_t}$, $A_{k,S_t}$, $\Sigma_{S_t}$: vectorul termenilor liberi, matricele lagurilor și covarianța erorilor în regimul curent; $\varepsilon_t \sim N(0, I_n)$'),
      T(r'EM: the M-step is multivariate weighted least squares by regime; $\Sigma_j = \sum_t\hat\xi_{j,t|T}\hat u_{jt}\hat u_{jt}\'/\sum_t\hat\xi_{j,t|T}$ ($\hat u_{jt}$: residuals of regime $j$)', r'EM: pasul M este o regresie multivariată ponderată pe fiecare regim; $\Sigma_j = \sum_t\hat\xi_{j,t|T}\hat u_{jt}\hat u_{jt}\'/\sum_t\hat\xi_{j,t|T}$ ($\hat u_{jt}$: reziduurile regimului $j$)'),
      T(r'parameters grow as $K(n + n^2p + n(n + 1)/2)$: shrinkage or restricted switching (MSIH) in larger systems (Chapter 5)', r'parametrii cresc ca $K(n + n^2p + n(n + 1)/2)$: shrinkage sau comutare restrînsă (MSIH) în sistemele mai mari (Capitolul 5)')]),
    (T(r'\textbf{Regime-dependent impulse responses} \refEEV: $\partial y_{t+h}/\partial\varepsilon_t$ computed with $(A_j, \Sigma_j)$, assuming regime $j$ persists over the horizon', r'\textbf{Răspunsuri la impuls dependente de regim} \refEEV: $\partial y_{t+h}/\partial\varepsilon_t$ calculat cu $(A_j, \Sigma_j)$, presupunînd că regimul $j$ persistă pe orizont'),
     [T('the full response averages over future regime paths and depends on the current regime probabilities; simulate it', 'răspunsul complet face media pe traiectoriile viitoare ale regimurilor și depinde de probabilitățile curente ale regimurilor; se obține prin simulare')]),
    T(r'Switching in $\Sigma$ alone identifies structural shocks by heteroskedasticity (Chapter 3); \refSZ ask whether US monetary policy switched, and find mainly variance switches', r'Comutarea doar în $\Sigma$ identifică șocurile structurale prin heteroscedasticitate (Capitolul 3); \refSZ întreabă dacă politica monetară a SUA a comutat și găsesc mai ales comutări de varianță')), 'small')

chart(T('A two-regime VAR for output and unemployment', 'Un VAR cu două regimuri pentru producție și șomaj'), 'ats_ch7_msvar', 'ATS_ch7_msvar', [
    T(r'MSIAH(2)-VAR(1) for US GDP growth and the change of the unemployment rate, 1960Q1--2019Q4 ($T = @{mv.T}$, @{mv.k} parameters), EM from 12 starts; Cholesky order: output first; responses scaled to a 1 pp output shock',
      r'MSIAH(2)-VAR(1) pentru creșterea PIB-ului SUA și variația ratei șomajului, T1 1960--T4 2019 ($T = @{mv.T}$, @{mv.k.ro} parametri), EM din 12 puncte de pornire; ordinea Cholesky: producția prima; răspunsuri scalate la un șoc de producție de 1 pp')],
    h='0.5\\textheight')

interp(('the MS-VAR', 'modelului MS-VAR'), [
    (T('The regimes are calm and volatile', 'Regimurile sînt calm și volatil'),
     [T(r'output shock s.d.\ @{mv.sy0} against @{mv.sy1} pp; durations @{mv.d0} and @{mv.d1} quarters', r'abaterea standard a șocului de producție @{mv.sy0} față de @{mv.sy1} pp; durate de @{mv.d0} și @{mv.d1} trimestre'),
      T(r'the volatile regime holds @{mv.pre}\% of quarters before 1984, @{mv.post}\% after, and @{mv.rec}\% of NBER quarters', r'regimul volatil acoperă @{mv.pre}\% din trimestre înainte de 1984, @{mv.post}\% după și @{mv.rec}\% din trimestrele NBER')]),
    T(r'Unemployment 12 quarters after a 1 pp output shock: @{mv.u12lo} pp (calm), @{mv.u12hi} pp (volatile), @{mv.u12lin} pp (linear VAR)', r'Șomajul la 12 trimestre după un șoc de producție de 1 pp: @{mv.u12lo} pp (calm), @{mv.u12hi} pp (volatil), @{mv.u12lin} pp (VAR liniar)'),
    (T(r'Okun\'s law is regime-dependent', r'Legea lui Okun depinde de regim'),
     [T(r'in the calm regime output surprises barely move unemployment (correlation of shocks @{mv.c0}, against @{mv.c1})', r'în regimul calm surprizele de producție aproape nu mișcă șomajul (corelația șocurilor @{mv.c0}, față de @{mv.c1})'),
      T('a linear VAR averages two transmissions', 'un VAR liniar face media a două transmisii')]),
    T(r'$\ln L$: @{mv.ll} (MS-VAR) against @{mv.lll} (linear VAR); regime-dependent responses assume the regime persists over the horizon', r'$\ln L$: @{mv.ll} (MS-VAR) față de @{mv.lll} (VAR liniar); răspunsurile dependente de regim presupun că regimul persistă pe orizont')])

# =============================================================================
# 8. MS-GARCH
# =============================================================================
D.section('Volatility regimes and MS-GARCH', 'Regimuri de volatilitate și MS-GARCH')

D.frame(T('Regimes in volatility', 'Regimuri în volatilitate'), two(
    ph('lehman', T('Lehman Brothers, Times Square, 2007: a calm regime about to end', 'Lehman Brothers, Times Square, 2007: un regim calm aproape de sfîrșit'), h='0.42\\textheight'),
    items(T(r'\refLL: structural shifts in the variance bias GARCH persistence $\alpha + \beta$ towards 1', r'\refLL: schimbările structurale ale varianței deplasează persistența GARCH $\alpha + \beta$ spre 1'),
          T(r'\refHS: SWARCH, an ARCH whose scale switches with a Markov chain; most of the persistence moves into the chain', r'\refHS: SWARCH, un ARCH a cărui scală comută după un lanț Markov; mare parte din persistență trece în lanț'),
          T(r'MSIH on returns: the simplest volatility-regime model, already a useful benchmark for GARCH \refBoll', r'MSIH pe randamente: cel mai simplu model cu regimuri de volatilitate, deja un reper util pentru GARCH \refBoll'),
          T('Chapter 8 develops realised measures and multivariate GARCH; here: what regimes do to GARCH', 'Capitolul 8 dezvoltă măsurile realizate și GARCH multivariat; aici: ce fac regimurile cu GARCH')), '0.3', '0.68'), 'footnotesize')

D.frame(T('The path-dependence problem', 'Problema dependenței de traiectorie'), items(
    (T(r'Naive MS-GARCH: $h_t = \omega_{S_t} + \alpha_{S_t}\varepsilon_{t-1}^2 + \beta_{S_t}h_{t-1}$', r'MS-GARCH naiv: $h_t = \omega_{S_t} + \alpha_{S_t}\varepsilon_{t-1}^2 + \beta_{S_t}h_{t-1}$'),
     [T(r'$h_t$: the conditional variance; $\varepsilon_{t-1}$: the last return shock; $\omega$, $\alpha$, $\beta$: the GARCH parameters of the regime', r'$h_t$: varianța condiționată; $\varepsilon_{t-1}$: ultimul șoc al randamentului; $\omega$, $\alpha$, $\beta$: parametrii GARCH ai regimului'),
      T(r'$h_{t-1}$ is itself regime-dependent', r'$h_{t-1}$ depinde la rîndul lui de regim'),
      T(r'$h_t$ depends on the whole path $(S_1, \dots, S_t)$: $K^t$ histories, so the Hamilton filter cannot be applied ($2^{100} \approx 10^{30}$)', r'$h_t$ depinde de întreaga traiectorie $(S_1, \dots, S_t)$: $K^t$ istorii, deci filtrul Hamilton nu se poate aplica ($2^{100} \approx 10^{30}$)')]),
    (T(r'\refGray: collapse the past into $h_{t-1} = \E[\varepsilon_{t-1}^2 \mid Y_{t-2}]$, the variance of the mixture: $h_{j,t} = \omega_j + \alpha_j\varepsilon_{t-1}^2 + \beta_j h_{t-1}$', r'\refGray: comprimă trecutul în $h_{t-1} = \E[\varepsilon_{t-1}^2 \mid Y_{t-2}]$, varianța amestecului: $h_{j,t} = \omega_j + \alpha_j\varepsilon_{t-1}^2 + \beta_j h_{t-1}$'),
     [T(r'\refKla: condition on $S_t$ as well, using $\Pr(S_{t-1} \mid S_t, Y_{t-1})$', r'\refKla: condiționează și pe $S_t$, folosind $\Pr(S_{t-1} \mid S_t, Y_{t-1})$')]),
    (T(r'\refHMP: $K$ GARCH processes run in parallel, $h_{j,t} = \omega_j + \alpha_j\varepsilon_{t-1}^2 + \beta_j h_{j,t-1}$; the chain picks one', r'\refHMP: $K$ procese GARCH rulează în paralel, $h_{j,t} = \omega_j + \alpha_j\varepsilon_{t-1}^2 + \beta_j h_{j,t-1}$; lanțul îl alege pe unul'),
     [T('no path dependence, exact likelihood, explicit stationarity conditions; asymptotics in \\refBPR', 'fără dependență de traiectorie, verosimilitate exactă, condiții explicite de staționaritate; asimptotica în \\refBPR')])), 'small')

D.frame(T('S\\&P 500: GARCH against MS-GARCH', 'S\\&P 500: GARCH comparat cu MS-GARCH'), table(
    'lccccc', T(r'\textbf{Model}', r'\textbf{Modelul}') + r' & $\alpha + \beta$, ' + T('regime 1', 'regimul 1') + r' & $\alpha + \beta$, ' + T('regime 2', 'regimul 2') + r' & $p_{ii}$ & $\ln L$ & BIC',
    [r'GARCH(1,1) & @{mg.gp} & & & @{mg.garch.ll} & @{mg.garch.bic}',
     r'MS-GARCH (HMP) & @{mg.hmp.p.lo} & @{mg.hmp.p.hi} & @{mg.hmp.P.lo}; @{mg.hmp.P.hi} & @{mg.hmp.ll} & @{mg.hmp.bic}',
     r'MS-GARCH (Gray) & @{mg.gray.p.lo} & @{mg.gray.p.hi} & @{mg.gray.P.lo}; @{mg.gray.P.hi} & @{mg.gray.ll} & @{mg.gray.bic}'],
    size='scriptsize') + items(
    T(r'Daily log returns (\%), January 2000 -- September 2026, $T = @{mg.T}$; Normal innovations, common mean; numerical ML in numpy from several starting values',
      r'Randamente logaritmice zilnice (\%), ianuarie 2000 -- septembrie 2026, $T = @{mg.T}$; inovații Normale, medie comună; verosimilitate maximă numerică în numpy din mai multe puncte de pornire'),
    T(r'HMP regimes: average conditional volatility while in the regime @{mg.vlo}\% and @{mg.vhi}\% per year; expected durations @{mg.dlo} and @{mg.dhi} days',
      r'Regimurile HMP: volatilitatea condiționată medie cît timp regimul este activ @{mg.vlo}\% și @{mg.vhi}\% pe an; durate așteptate de @{mg.dlo} și @{mg.dhi} zile')), 'small')

chart(T('Conditional volatility and the high-volatility regime', 'Volatilitatea condiționată și regimul de volatilitate ridicată'), 'ats_ch7_msgarch', 'ATS_ch7_msgarch', [
    T('Top: annualised conditional volatility, GARCH(1,1) and MS-GARCH (HMP, mixture variance); bottom: filtered probability of the high-volatility regime', 'Sus: volatilitatea condiționată anualizată, GARCH(1,1) și MS-GARCH (HMP, varianța amestecului); jos: probabilitatea filtrată a regimului de volatilitate ridicată')],
    h='0.5\\textheight')

interp(('MS-GARCH', 'modelului MS-GARCH'), [
    T(r'BIC prefers HMP (@{mg.hmp.bic}) to GARCH (@{mg.garch.bic}); the high-volatility regime is active on @{mg.share}\% of days', r'BIC preferă HMP (@{mg.hmp.bic}) față de GARCH (@{mg.garch.bic}); regimul de volatilitate ridicată este activ în @{mg.share}\% din zile'),
    T(r'Single-regime persistence @{mg.gp}; within the regimes @{mg.hmp.p.lo} (calm) and @{mg.hmp.p.hi} (high volatility): regimes do not remove persistence automatically, they move it to where it belongs', r'Persistența cu un singur regim @{mg.gp}; în interiorul regimurilor @{mg.hmp.p.lo} (calm) și @{mg.hmp.p.hi} (volatilitate ridicată): regimurile nu elimină automat persistența, ci o mută acolo unde îi este locul'),
    T(r'Gray\'s collapsing fits worse here (@{mg.gray.ll}): the approximation is not innocuous', r'Comprimarea lui Gray se potrivește mai slab aici (@{mg.gray.ll}): aproximarea nu este inofensivă'),
    T('Local maxima are frequent: different starts give different regime splits (always report the starting design)', 'Maximele locale sînt frecvente: puncte de pornire diferite dau împărțiri diferite în regimuri (raportați întotdeauna schema punctelor de pornire)')])

D.recap(('Volatility regimes', 'regimurile de volatilitate'), [
    T('Variance regimes and GARCH persistence are entangled: report the persistence inside each regime and of the chain', 'Regimurile de varianță și persistența GARCH sînt legate: raportați persistența din fiecare regim și pe cea a lanțului'),
    T('Path dependence: collapse (Gray, Klaassen) or run GARCH processes in parallel (HMP)', 'Dependența de traiectorie: comprimare (Gray, Klaassen) sau procese GARCH paralele (HMP)'),
    T('Chapter 8 compares these models with realised measures', 'Capitolul 8 compară aceste modele cu măsurile realizate')])

# =============================================================================
# 9. BULL ȘI BEAR
# =============================================================================
D.section('Bull and bear markets', 'Piețe bull și bear')

D.frame(T('Equity regimes: S\\&P 500 and BET', 'Regimuri pe piața de acțiuni: S\\&P 500 și BET'), two(
    ph('bvb', T('Bucharest Stock Exchange, 2024', 'Bursa de Valori București, 2024'), h='0.34\\textheight'),
    items(T(r'Weekly log returns, 2000--2026, MSIH(2): $r_t = \mu_{S_t} + \sigma_{S_t}\varepsilon_t$ \refMM, \refAT', r'Randamente logaritmice săptămînale, 2000--2026, MSIH(2): $r_t = \mu_{S_t} + \sigma_{S_t}\varepsilon_t$ \refMM, \refAT'),
          T(r'S\&P 500 (annualised): calm @{bb.sp500.m0}\% mean, @{bb.sp500.s0}\% volatility; turbulent @{bb.sp500.m1}\%, @{bb.sp500.s1}\%', r'S\&P 500 (anualizat): calm, media @{bb.sp500.m0}\%, volatilitatea @{bb.sp500.s0}\%; agitat @{bb.sp500.m1}\%, @{bb.sp500.s1}\%'),
          T(r'BET: calm @{bb.bet.m0}\%, @{bb.bet.s0}\%; turbulent @{bb.bet.m1}\%, @{bb.bet.s1}\%', r'BET: calm @{bb.bet.m0}\%, @{bb.bet.s0}\%; agitat @{bb.bet.m1}\%, @{bb.bet.s1}\%'),
          T(r'Durations (weeks), calm and turbulent: S\&P 500 @{bb.sp500.d0} and @{bb.sp500.d1}; BET @{bb.bet.d0} and @{bb.bet.d1}', r'Durate (săptămîni), calm și agitat: S\&P 500 @{bb.sp500.d0} și @{bb.sp500.d1}; BET @{bb.bet.d0} și @{bb.bet.d1}')), '0.36', '0.62'), 'footnotesize')

chart(T('Turbulent regimes on two markets', 'Regimuri agitate pe două piețe'), 'ats_ch7_bullbear', 'ATS_ch7_bullbear', [
    T(r'Log index levels (first week = 100); shaded: smoothed probability of the turbulent regime above 0.5; EM from 15 starts and a numerical polish (\texttt{statsmodels}: same $\ln L$)', r'Nivelurile indicilor pe scară logaritmică (prima săptămînă = 100); hașurat: probabilitatea netezită a regimului agitat peste 0,5; EM din 15 puncte de pornire și rafinare numerică (\texttt{statsmodels}: același $\ln L$)')],
    h='0.52\\textheight')

interp(('the equity regimes', 'regimurilor pieței de acțiuni'), [
    T(r'Turbulent share: S\&P 500 @{bb.sp500.share}\%, BET @{bb.bet.share}\%; correlation of the two turbulent probabilities @{bb.corr}; both turbulent in @{bb.both}\% of weeks', r'Ponderea regimului agitat: S\&P 500 @{bb.sp500.share}\%, BET @{bb.bet.share}\%; corelația celor două probabilități @{bb.corr}; ambele agitate în @{bb.both}\% din săptămîni'),
    T('The regimes are mostly volatility regimes: the turbulent mean is lower but estimated with large error', 'Regimurile sînt mai ales regimuri de volatilitate: media regimului agitat este mai mică, dar estimată cu eroare mare'),
    T(r'$\ln L$: S\&P 500 @{bb.sp500.ll} (numpy) and @{bb.sp500.sm} (\texttt{statsmodels}); BET @{bb.bet.ll} and @{bb.bet.sm}', r'$\ln L$: S\&P 500 @{bb.sp500.ll} (numpy) și @{bb.sp500.sm} (\texttt{statsmodels}); BET @{bb.bet.ll} și @{bb.bet.sm}'),
    T('The BET has its own turbulent episodes (local politics, the 2007--2009 crash), not only imported ones', 'BET are episoade agitate proprii (politică internă, prăbușirea din 2007--2009), nu doar importate')])

D.frame(T('Regimes and asset allocation, briefly', 'Regimuri și alocarea activelor, pe scurt'), items(
    (T(r'\refAB', r'\refAB'),
     [T('with regime switching, optimal portfolios depend on the current regime probabilities', 'cu schimbare de regim, portofoliile optime depind de probabilitățile curente ale regimurilor'),
      T('home bias and the value of international diversification change across regimes', 'preferința pentru piața internă și valoarea diversificării internaționale se schimbă de la un regim la altul')]),
    (T(r'Mean-variance weight of equity against cash, risk aversion $\gamma = @{bb.gamma}$: $w = \mu/(\gamma\sigma^2)$; $\mu$, $\sigma^2$: weekly mean and variance of the return in the regime', r'Ponderea acțiunilor față de numerar în portofoliul medie--varianță, cu aversiunea la risc $\gamma = @{bb.gamma}$: $w = \mu/(\gamma\sigma^2)$; $\mu$, $\sigma^2$: media și varianța săptămînale ale randamentului în regim'),
     [T(r'S\&P 500: @{bb.sp500.w0} in the calm regime, @{bb.sp500.w1} in the turbulent one, @{bb.sp500.wc} with constant moments', r'S\&P 500: @{bb.sp500.w0} în regimul calm, @{bb.sp500.w1} în cel agitat, @{bb.sp500.wc} cu momente constante'),
      T(r'with one-step mixture moments the weight moves between @{bb.sp500.wmin} and @{bb.sp500.wmax}', r'cu momentele amestecului la un pas, ponderea se mișcă între @{bb.sp500.wmin} și @{bb.sp500.wmax}')]),
    T('Caveats: estimation error in regime means is large; out-of-sample gains must be tested (Chapter 1) and transaction costs included', 'Rezerve: eroarea de estimare a mediilor pe regimuri este mare; cîștigurile în afara eșantionului trebuie testate (Capitolul 1), iar costurile de tranzacționare incluse'),
    T('Market-risk applications (VaR and ES with regimes) are in MFM, Chapter 7', 'Aplicațiile de risc de piață (VaR și ES cu regimuri) sînt în MFM, Capitolul 7')), 'small')

# =============================================================================
# 10. ESTIMARE BAYESIANĂ
# =============================================================================
D.section('Bayesian estimation', 'Estimarea bayesiană')

D.frame(T('Gibbs sampling with data augmentation', 'Eșantionarea Gibbs cu augmentarea datelor'), items(
    (T(r'Treat $S = (S_1, \dots, S_T)$ as parameters \refAC: given $S$, the model is a set of regressions; given $\theta$, $S$ is a hidden Markov chain', r'Tratăm $S = (S_1, \dots, S_T)$ ca parametri \refAC: dat fiind $S$, modelul este un set de regresii; dat fiind $\theta$, $S$ este un lanț Markov ascuns'),
     [T(r'1. $S \mid \theta, Y$; 2. $\mathbf{P} \mid S$: rows $\sim$ Dirichlet$(a_{i\cdot} + n_{i\cdot})$, $n_{ij}$ the transition counts, $a_{ij}$ the prior Dirichlet parameters', r'1. $S \mid \theta, Y$; 2. $\mathbf{P} \mid S$: rîndurile $\sim$ Dirichlet$(a_{i\cdot} + n_{i\cdot})$, $n_{ij}$ numărul de tranziții, $a_{ij}$ parametrii Dirichlet a priori'),
      T(r'3. $\mu_j \mid \sigma_j^2, S, Y \sim$ Normal and $\sigma_j^2 \mid \mu_j, S, Y \sim$ inverse gamma: conjugate updates on the observations of regime $j$ (Chapter 5)', r'3. $\mu_j \mid \sigma_j^2, S, Y \sim$ Normală și $\sigma_j^2 \mid \mu_j, S, Y \sim$ inverse gamma: actualizări conjugate pe observațiile regimului $j$ (Capitolul 5)')]),
    (T(r'\textbf{FFBS} \refChibB: draw the whole path at once: $S_T \sim \hat\xi_{T|T}$, then $\Pr(S_t = i \mid S_{t+1} = j, Y_t) \propto \hat\xi_{i,t|t}p_{ij}$ backwards', r'\textbf{FFBS} \refChibB: extragem toată traiectoria odată: $S_T \sim \hat\xi_{T|T}$, apoi înapoi $\Pr(S_t = i \mid S_{t+1} = j, Y_t) \propto \hat\xi_{i,t|t}p_{ij}$'),
     [T('single-move sampling of $S_t$ given $S_{t-1}, S_{t+1}$ mixes very slowly when regimes are persistent', 'eșantionarea cîte un $S_t$, dat fiind $S_{t-1}$ și $S_{t+1}$, are o amestecare (mixing) foarte lentă cînd regimurile sînt persistente'),
      T(r'the discrete analogue of the simulation smoother of Chapter 6 \refCK', r'analogul discret al simulation smoother-ului din Capitolul 6 \refCK')]),
    T('Priors keep $\\sigma_j$ away from 0 and $p_{ii}$ away from the boundary: the degenerate maxima of ML disappear', 'Distribuțiile a priori țin $\\sigma_j$ departe de 0 și $p_{ii}$ departe de frontieră: maximele degenerate ale verosimilității dispar')), 'small')

D.frame(T('Label switching in MCMC, and choosing $K$', 'Schimbarea etichetelor în MCMC și alegerea lui $K$'), items(
    (T(r'\textbf{Random permutation sampler} \refFSa: permute the labels at random after each sweep; the sampler then visits all $K!$ modes', r'\textbf{Eșantionatorul cu permutări aleatoare} \refFSa: permutăm aleator etichetele după fiecare iterație; eșantionatorul vizitează astfel toate cele $K!$ moduri'),
     [T('the unconstrained output shows which parameters separate the regimes; identify afterwards by the constraint that does', 'rezultatul nerestricționat arată ce parametri separă regimurile; identificăm apoi prin restricția care le separă'),
      T(r'a bad constraint (e.g.\ on parameters that barely differ) cuts a mode in half and biases both regimes \refCHR', r'o restricție nepotrivită (de exemplu pe parametri aproape egali) taie un mod în două și deplasează ambele regimuri \refCHR')]),
    (T(r'Choosing $K$: marginal likelihood $p(Y \mid K)$ from the Gibbs output \refChibA, $\ln p(Y) = \ln f(Y \mid \theta^*) + \ln p(\theta^*) - \ln p(\theta^* \mid Y)$', r'Alegerea lui $K$: verosimilitatea marginală $p(Y \mid K)$ din rezultatele Gibbs \refChibA, $\ln p(Y) = \ln f(Y \mid \theta^*) + \ln p(\theta^*) - \ln p(\theta^* \mid Y)$'),
     [T('the likelihood ordinate comes from the Hamilton filter; the posterior ordinate from reduced Gibbs runs', 'ordonata verosimilității vine din filtrul Hamilton; ordonata a posteriori din rulări Gibbs reduse')]),
    T('Change-point models (Chib 1998) are the same sampler with an upper-triangular $\\mathbf{P}$', 'Modelele cu puncte de schimbare (Chib 1998) folosesc același eșantionator cu o matrice $\\mathbf{P}$ superior triunghiulară')), 'small')

chart(T('Romanian GDP growth: two regimes by Gibbs sampling', 'Creșterea PIB-ului României: două regimuri prin eșantionare Gibbs'), 'ats_ch7_gibbs', 'ATS_ch7_bayes', [
    T(r'Quarterly growth, @{gb.start}--@{gb.end} ($T = @{gb.T}$), MSIH(2) without AR term; @{gb.n} draws after burn-in; left: permutation sampler, right: sampler identified by $\mu_1 < \mu_2$',
      r'Creșterea trimestrială, @{gb.start}--@{gb.end} ($T = @{gb.T}$), MSIH(2) fără termen AR; @{gb.n} extrageri după burn-in; stînga: eșantionatorul cu permutări, dreapta: eșantionatorul identificat prin $\mu_1 < \mu_2$')],
    h='0.5\\textheight')

interp(('the posterior', 'distribuției a posteriori'), [
    T(r'Permutation sampler: label 1 carries the larger mean in @{gb.swap}\% of draws: the bimodal histogram is the two regimes, not two answers', r'Eșantionatorul cu permutări: eticheta 1 are media mai mare în @{gb.swap}\% din extrageri: histograma bimodală reprezintă cele două regimuri, nu două răspunsuri'),
    T(r'Identified: $\mu_1$ @{gb.mu1.m} [@{gb.mu1.lo}; @{gb.mu1.hi}], $\sigma_1$ @{gb.sd1.m}; $\mu_2$ @{gb.mu2.m} [@{gb.mu2.lo}; @{gb.mu2.hi}], $\sigma_2$ @{gb.sd2.m} (90\% credible intervals)', r'Identificat: $\mu_1$ @{gb.mu1.m} [@{gb.mu1.lo}; @{gb.mu1.hi}], $\sigma_1$ @{gb.sd1.m}; $\mu_2$ @{gb.mu2.m} [@{gb.mu2.lo}; @{gb.mu2.hi}], $\sigma_2$ @{gb.sd2.m} (intervale credibile de 90\%)'),
    T(r'$p_{11}$ @{gb.p11.m} [@{gb.p11.lo}; @{gb.p11.hi}], $p_{22}$ @{gb.p22.m}; EM: $\mu$ = @{gb.em.mu0} and @{gb.em.mu1}, $p_{ii}$ = @{gb.em.p0} and @{gb.em.p1}', r'$p_{11}$ @{gb.p11.m} [@{gb.p11.lo}; @{gb.p11.hi}], $p_{22}$ @{gb.p22.m}; EM: $\mu$ = @{gb.em.mu0} și @{gb.em.mu1}, $p_{ii}$ = @{gb.em.p0} și @{gb.em.p1}'),
    T(r'The means overlap, the standard deviations do not: the regimes are a volatile era (1995--2000, 2009--2012, 2020) and a stable one; the variance is the better identifying constraint', r'Mediile se suprapun, abaterile standard nu: regimurile sînt o eră volatilă (1995--2000, 2009--2012, 2020) și una stabilă; varianța este restricția de identificare mai bună'),
    T(r'Posterior and EM regime probabilities correlate at @{gb.corr}; the posterior also carries the parameter uncertainty that the EM path ignores', r'Probabilitățile regimurilor a posteriori și cele din EM au corelația @{gb.corr}; distribuția a posteriori include și incertitudinea parametrilor, pe care traiectoria EM o ignoră')], 'footnotesize')

D.recap(('Bayesian estimation', 'estimarea bayesiană'), [
    T('Data augmentation turns the switching model into conjugate regressions plus FFBS', 'Augmentarea datelor transformă modelul cu schimbare de regim în regresii conjugate plus FFBS'),
    T('Let the sampler switch labels, then identify with the parameter that separates regimes', 'Lăsați eșantionatorul să schimbe etichetele, apoi identificați cu parametrul care separă regimurile'),
    T('Marginal likelihoods compare $K$ and change-point models on the same footing', 'Verosimilitățile marginale compară valorile lui $K$ și modelele cu puncte de schimbare pe aceeași bază')])

# =============================================================================
# 11. MEMORIE LUNGĂ ȘI RUPTURI
# =============================================================================
D.section('Regimes, long memory and breaks', 'Regimuri, memorie lungă și rupturi')

D.frame(T('Rare switches look like long memory', 'Comutările rare arată ca memoria lungă'), items(
    (T(r'\refDI: $y_t = \mu_{S_t} + \varepsilon_t$ with $p_{ii} = 1 - c/T^\delta$', r'\refDI: $y_t = \mu_{S_t} + \varepsilon_t$ cu $p_{ii} = 1 - c/T^\delta$'),
     [T(r'$c, \delta > 0$: switches become rarer as $T$ grows', r'$c, \delta > 0$: comutările devin mai rare cînd $T$ crește'),
      T(r'the variance of partial sums grows like that of an I($d$) process, $d > 0$', r'varianța sumelor parțiale crește ca la un proces I($d$), $d > 0$'),
      T(r'the autocorrelations $\propto\lambda^k$ with $\lambda \to 1$ decay so slowly that, in any finite sample, they look hyperbolic', r'autocorelațiile $\propto\lambda^k$, cu $\lambda \to 1$, scad atît de lent încît, în orice eșantion finit, par hiperbolice')]),
    (T('Consequences', 'Consecințe'),
     [T('a significant GPH or local Whittle estimate (Chapter 10) does not discriminate fractional integration from occasional breaks or regimes', 'o estimație GPH sau Whittle locală semnificativă (Capitolul 10) nu deosebește integrarea fracționară de rupturile ocazionale sau de regimuri'),
      T('the same holds for GARCH persistence (previous section) and for unit-root tests with breaks (Chapter 2)', 'același lucru este valabil pentru persistența GARCH (secțiunea anterioară) și pentru testele de rădăcină unitară cu rupturi (Capitolul 2)')]),
    T('Which description is "true" matters less than which one forecasts better out of sample', 'Care descriere este „adevărată” contează mai puțin decît care prognozează mai bine în afara eșantionului')), 'small')

chart(T('Simulation: GPH estimates of $d$ under regime switching', 'Simulare: estimații GPH ale lui $d$ cu schimbare de regim'), 'ats_ch7_longmem', 'ATS_ch7_longmem', [
    T(r'$y_t = \mu_{S_t} + \varepsilon_t$, $\mu \in \{0, 1\}$, $\sigma = 1$; mean GPH estimate ($m = T^{0.5}$) over @{lm.reps} replications, $\pm 2$ standard errors',
      r'$y_t = \mu_{S_t} + \varepsilon_t$, $\mu \in \{0, 1\}$, $\sigma = 1$; media estimațiilor GPH ($m = T^{0{,}5}$) pe @{lm.reps} de replicări, $\pm 2$ erori standard')],
    h='0.5\\textheight')

interp(('the simulation', 'simulării'), [
    T(r'Rare switches ($p = 1 - 5/T$): mean $\hat d$ = @{lm.r0}, @{lm.r1}, @{lm.r2}, @{lm.r3} for $T$ = @{lm.T0}, @{lm.T1}, @{lm.T2}, @{lm.T3}: it does not vanish as $T$ grows', r'Comutări rare ($p = 1 - 5/T$): media $\hat d$ = @{lm.r0}; @{lm.r1}; @{lm.r2}; @{lm.r3} pentru $T$ = @{lm.T0}; @{lm.T1}; @{lm.T2}; @{lm.T3}: nu dispare cînd $T$ crește'),
    T(r'Fixed $p = 0.95$: @{lm.f0}, @{lm.f1}, @{lm.f2}, @{lm.f3}: short memory, $\hat d \to 0$ as the frequencies used approach zero', r'$p = 0{,}95$ fix: @{lm.f0}; @{lm.f1}; @{lm.f2}; @{lm.f3}: memorie scurtă, $\hat d \to 0$ pe măsură ce frecvențele folosite se apropie de zero'),
    T(r'The path on the left has @{lm.sw} switches in 4000 observations; its autocorrelation is @{lm.a50} at lag 50 and @{lm.a200} at lag 200', r'Traiectoria din stînga are @{lm.sw} comutări în 4000 de observații; autocorelația ei este @{lm.a50} la lagul 50 și @{lm.a200} la lagul 200')])

D.frame(T('Regimes or breaks?', 'Regimuri sau rupturi?'), items(
    (T(r'A break (Chapter 2) is a regime that never returns: $\mathbf{P}$ upper bidiagonal, $S_1 = 1$ \refChibC', r'O ruptură (Capitolul 2) este un regim care nu revine niciodată: $\mathbf{P}$ superior bidiagonală, $S_1 = 1$ \refChibC'),
     [T('the Hamilton filter and EM apply unchanged; the transition mask keeps the forbidden transitions at zero', 'filtrul Hamilton și EM se aplică neschimbate; masca tranzițiilor ține tranzițiile interzise la zero')]),
    (T('Recurrent regimes pool information across episodes: the second high-inflation episode reuses the parameters of the first', 'Regimurile recurente pun în comun informația din episoade: al doilea episod de inflație ridicată folosește parametrii primului'),
     [T('breaks need a new parameter set for every episode, and say nothing about the future', 'rupturile cer un nou set de parametri pentru fiecare episod și nu spun nimic despre viitor')]),
    T(r'Compare the two by BIC or marginal likelihood; \refGP: the US real interest rate is better described by three recurrent regimes than by a stable process', r'Comparăm cele două prin BIC sau verosimilitatea marginală; \refGP: rata reală a dobînzii din SUA este descrisă mai bine prin trei regimuri recurente decît printr-un proces stabil')), 'small')

chart(T('Romanian inflation regimes since 1997', 'Regimurile inflației din România din 1997'), 'ats_ch7_ro_infl', 'ATS_ch7_ro_inflation', [
    T(r'Annual HICP inflation, $100\ln(P_t/P_{t-12})$, from @{ri.start} ($T = @{ri.T}$); MSIH(3)-AR(1), EM from 25 starts; dashed: change points of the 4-regime change-point model; symmetric log scale',
      r'Inflația anuală IAPC, $100\ln(P_t/P_{t-12})$, din @{ri.start} ($T = @{ri.T}$); MSIH(3)-AR(1), EM din 25 de puncte de pornire; linii întrerupte: punctele de schimbare ale modelului cu 4 regimuri; scară logaritmică simetrică')],
    h='0.52\\textheight')

interp(('the inflation regimes', 'regimurilor inflației'), [
    T(r'Regime levels $\nu_j/(1 - \phi)$: @{ri.l0}\%, @{ri.l1}\% and @{ri.l2}\%; shock s.d.\ @{ri.s0}, @{ri.s1} and @{ri.s2} pp; $\phi = @{ri.phi}$: after 2001 the two lower regimes differ mainly in volatility', r'Nivelurile regimurilor $\nu_j/(1 - \phi)$: @{ri.l0}\%, @{ri.l1}\% și @{ri.l2}\%; abaterea standard a șocurilor @{ri.s0}; @{ri.s1} și @{ri.s2} pp; $\phi = @{ri.phi}$: după 2001 cele două regimuri inferioare diferă mai ales prin volatilitate'),
    T(r'The volatile regime returns in the 2010 VAT increase, in 2022 and in 2025; filtered probabilities in @{ri.lastd} (inflation @{ri.last}\%): @{ri.lp0}, @{ri.lp1}, @{ri.lp2}', r'Regimul volatil revine la creșterea TVA din 2010, în 2022 și în 2025; probabilitățile filtrate în @{ri.lastd} (inflația @{ri.last}\%): @{ri.lp0}; @{ri.lp1}; @{ri.lp2}'),
    T(r'BIC prefers change points: 3 segments @{ri.bic.CP3}, 4 segments @{ri.bic.CP4}, Markov switching @{ri.bic.MS3}; the change points of the 4-segment model: @{ri.breaks}', r'BIC preferă punctele de schimbare: 3 segmente @{ri.bic.CP3}, 4 segmente @{ri.bic.CP4}, schimbare de regim @{ri.bic.MS3}; punctele de schimbare ale modelului cu 4 segmente: @{ri.breaks}'),
    (T('Reading: disinflation was a one-way process', 'Interpretare: dezinflația a fost un proces într-un singur sens'),
     [T('after 2000 a single, very persistent segment absorbs the 2022 and 2025 surges as shocks', 'după 2000 un singur segment, foarte persistent, absoarbe creșterile din 2022 și 2025 ca șocuri'),
      T('whether they are a recurrent regime is decided out of sample', 'dacă ele sînt un regim recurent se decide în afara eșantionului')])])

D.recap(('Regimes, memory and breaks', 'regimuri, memorie și rupturi'), [
    T('Rare switches mimic long memory: memory tests cannot tell them apart', 'Comutările rare imită memoria lungă: testele de memorie nu le pot deosebi'),
    T('Breaks are non-recurrent regimes: same filter, restricted $\\mathbf{P}$', 'Rupturile sînt regimuri nerecurente: același filtru, $\\mathbf{P}$ restricționată'),
    T('Model choice is an out-of-sample question', 'Alegerea modelului este o întrebare de performanță în afara eșantionului')])

# =============================================================================
# 12. EUR/RON
# =============================================================================
D.section('EUR/RON: exchange-rate regimes', 'EUR/RON: regimuri ale cursului de schimb')

D.frame(T('Romania\'s exchange-rate regimes', 'Regimurile cursului de schimb din România'), two(
    ph('bnr', T('National Bank of Romania, Bucharest, 2014', 'Banca Națională a României, București, 2014'), h='0.34\\textheight'),
    items(T('1999--2005: crawling depreciation of the old leu under a managed float', '1999--2005: depreciere graduală a leului vechi într-un regim de managed float'),
          T('July 2005: redenomination (10\\,000 ROL = 1 RON); August 2005: inflation targeting with a managed float; capital account fully liberalised in 2006', 'Iulie 2005: denominarea (10\\,000 ROL = 1 RON); august 2005: țintirea inflației, cu un regim de managed float; contul de capital complet liberalizat în 2006'),
          T('Episodes: October 2008, 2011--2012, March 2020, May 2025 (presidential election and fiscal stress)', 'Episoade: octombrie 2008, 2011--2012, martie 2020, mai 2025 (alegerile prezidențiale și tensiunile fiscale)'),
          T(r'Model: weekly log changes, MSIH(3) ordered by volatility; regimes are policy outcomes, not the announced regime', r'Modelul: variații logaritmice săptămînale, MSIH(3) ordonat după volatilitate; regimurile sînt rezultate ale politicii, nu regimul anunțat')), '0.36', '0.62'), 'footnotesize')

chart(T('EUR/RON volatility regimes, 1999--2026', 'Regimurile de volatilitate ale EUR/RON, 1999--2026'), 'ats_ch7_eurron', 'ATS_ch7_eurron', [
    T(r'Top: EUR/RON (ECB reference rate to June 2005, BNR from July 2005); bottom: smoothed probabilities of the calm, intermediate and turbulent regimes; $T = @{eu.T}$ weeks',
      r'Sus: EUR/RON (cursul de referință BCE pînă în iunie 2005, BNR din iulie 2005); jos: probabilitățile netezite ale regimurilor calm, intermediar și agitat; $T = @{eu.T}$ de săptămîni')],
    h='0.52\\textheight')

interp(('the EUR/RON regimes', 'regimurilor EUR/RON'), [
    T(r'Weekly s.d.\ by regime: @{eu.s0}, @{eu.s1} and @{eu.s2}\%; expected durations @{eu.d0}, @{eu.d1} and @{eu.d2} weeks', r'Abaterea standard săptămînală pe regim: @{eu.s0}; @{eu.s1} și @{eu.s2}\%; durate așteptate de @{eu.d0}; @{eu.d1} și @{eu.d2} săptămîni'),
    T(r'Before July 2005 the turbulent regime holds @{eu.tpre}\% of weeks (the steady depreciation of the old leu, mean @{eu.mu2}\% per week), after it @{eu.tpost}\%; the calm regime goes from @{eu.cpre}\% to @{eu.cpost}\%', r'Înainte de iulie 2005 regimul agitat cuprinde @{eu.tpre}\% din săptămîni (deprecierea continuă a leului vechi, media @{eu.mu2}\% pe săptămînă), după aceea @{eu.tpost}\%; regimul calm trece de la @{eu.cpre}\% la @{eu.cpost}\%'),
    T(r'Turbulent probability peaks at @{eu.p08} in October 2008--March 2009 and at @{eu.p25} in spring 2025; the largest 2025 weekly change, @{eu.big}\%, in the week ending @{eu.bigd}', r'Probabilitatea regimului agitat atinge @{eu.p08} în octombrie 2008--martie 2009 și @{eu.p25} în primăvara lui 2025; cea mai mare variație săptămînală din 2025, @{eu.big}\%, în săptămîna încheiată la @{eu.bigd}'),
    T(r'EUR/RON averaged @{eu.lvl04} in April 2025 and stood at @{eu.last} at the end of the sample: a level shift followed by a return to calm, as a managed float predicts', r'EUR/RON a avut media @{eu.lvl04} în aprilie 2025 și era @{eu.last} la sfîrșitul eșantionului: o schimbare de nivel urmată de revenirea la calm, cum prevede un regim de managed float')])

# =============================================================================
# 13. PROGNOZĂ
# =============================================================================
D.section('Forecasting with regime models', 'Prognoza cu modele cu schimbare de regim')

D.frame(T('Forecasts from a switching model', 'Prognozele unui model cu schimbare de regim'), items(
    (T(r'Regime forecast: $\hat\xi_{T+h|T} = (\mathbf{P}\')^h\hat\xi_{T|T}$, converging to $\boldsymbol\pi$ at the rate $\lambda^h$', r'Prognoza regimului: $\hat\xi_{T+h|T} = (\mathbf{P}\')^h\hat\xi_{T|T}$, care converge spre $\boldsymbol\pi$ cu viteza $\lambda^h$'),
     [T(r'one step: $f(y_{T+1} \mid Y_T) = \sum_j \hat\xi_{j,T+1|T}\,N(x_{T+1}\'\beta_j, \sigma_j^2)$, a \textbf{mixture}: skewed, fat-tailed, possibly bimodal', r'la un pas: $f(y_{T+1} \mid Y_T) = \sum_j \hat\xi_{j,T+1|T}\,N(x_{T+1}\'\beta_j, \sigma_j^2)$, un \textbf{amestec}: asimetric, cu cozi groase, posibil bimodal')]),
    (T(r'Several steps with AR terms: the mean is not linear in past regimes (MSM) or needs the regime path; simulate paths of $(S, y)$', r'La mai mulți pași, cu termeni AR: media nu este liniară în regimurile trecute (MSM) sau cere traiectoria regimurilor; simulăm traiectorii ale perechii $(S, y)$'),
     []),
    (T('Evaluation (Chapter 1): point forecasts by RMSE and Diebold--Mariano; densities by log score, PIT and CRPS; regime probabilities by QPS', 'Evaluarea (Capitolul 1): prognozele punctuale prin RMSE și Diebold--Mariano; densitățile prin scorul logaritmic, PIT și CRPS; probabilitățile regimurilor prin QPS'),
     [T(r'QPS $= \frac2T\sum_t(\hat p_t - d_t)^2$ \refDR: the Brier score of a recession probability $\hat p_t$ against the NBER indicator $d_t$ (1 in recession); 0 is perfect, 2 the worst', r'QPS $= \frac2T\sum_t(\hat p_t - d_t)^2$ \refDR: scorul Brier al unei probabilități de recesiune $\hat p_t$ față de indicatorul NBER $d_t$ (1 în recesiune); 0 este perfect, 2 cel mai slab')]),
    T(r'\refCKr: MS models rarely beat linear AR in point forecasts of GDP; their value is in densities and in turning-point probabilities', r'\refCKr: modelele MS sînt rareori superioare modelelor AR liniare în prognozele punctuale ale PIB; valoarea lor stă în densități și în probabilitățile punctelor de întoarcere')), 'small')

chart(T('US GDP: one-step density forecasts, 1990--2019', 'PIB-ul SUA: prognoze de densitate la un pas, 1990--2019'), 'ats_ch7_forecast', 'ATS_ch7_forecast', [
    T(r'Expanding window from 1947Q2, @{fc.n} quarters, AR(1) re-estimated each quarter, MSIH(2)-AR(1) every 4 quarters (EM, warm start); left: cumulative log-score difference; right: PIT histograms (dashed: uniform)',
      r'Fereastră extinsă din T2 1947, @{fc.n.ro} trimestre, AR(1) reestimat în fiecare trimestru, MSIH(2)-AR(1) la fiecare 4 trimestre (EM, pornind de la soluția anterioară); stînga: diferența cumulată a scorurilor logaritmice; dreapta: histogramele PIT (linia întreruptă: uniformă)')],
    h='0.5\\textheight')

interp(('the forecast comparison', 'comparației prognozelor'), [
    T(r'RMSE: AR(1) @{fc.rmse_ar}, MSIH(2)-AR(1) @{fc.rmse_ms}: the point forecasts are almost the same, as Clements and Krolzig found', r'RMSE: AR(1) @{fc.rmse_ar}, MSIH(2)-AR(1) @{fc.rmse_ms}: prognozele punctuale sînt aproape identice, cum au găsit Clements și Krolzig'),
    T(r'Mean log score: @{fc.ls_ar} against @{fc.ls_ms}; Diebold--Mariano on the difference @{fc.dm} ($p = @{fc.p_dm}$)', r'Scorul logaritmic mediu: @{fc.ls_ar} față de @{fc.ls_ms}; Diebold--Mariano pe diferență @{fc.dm} ($p = @{fc.p_dm}$)'),
    T(r'The gain comes from the variance regime: the AR(1) density is too wide after 1984 (PIT piled in the middle, KS @{fc.ks_ar}); the MS density is closer to uniform but not calibrated either (KS @{fc.ks_ms})', r'Cîștigul vine din regimul de varianță: densitatea AR(1) este prea largă după 1984 (PIT concentrat la mijloc, KS @{fc.ks_ar}); densitatea MS este mai aproape de uniformă, dar nici ea nu este calibrată (KS @{fc.ks_ms})'),
    T(r'Cumulative log-score gain before 2008: @{fc.cum_pre08}; from 2008: @{fc.cum_post08}: the regime model pays in calm times and loses in the crisis', r'Cîștigul cumulat de scor logaritmic înainte de 2008: @{fc.cum_pre08}; din 2008: @{fc.cum_post08}: modelul cu regimuri cîștigă în perioadele calme și pierde în criză')])

D.recap(('Forecasting', 'prognoza'), [
    T('Forecast densities are mixtures; regime forecasts decay to the ergodic probabilities', 'Densitățile de prognoză sînt amestecuri; prognozele regimurilor converg spre probabilitățile ergodice'),
    T('Evaluate densities and regime probabilities, not only RMSE', 'Evaluați densitățile și probabilitățile regimurilor, nu doar RMSE'),
    T('Gains are episodic: test them over time (fluctuation tests, Chapter 1)', 'Cîștigurile sînt episodice: testați-le în timp (teste de fluctuație, Capitolul 1)')])

# =============================================================================
# 14. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Can a regime model date Romanian recessions and inflation regimes in real time better than simple rules, and is the 2025 episode a new regime?', 'Poate un model cu schimbare de regim să dateze în timp real recesiunile și regimurile inflației din România mai bine decît regulile simple și este episodul din 2025 un regim nou?'),
     [T(r'formal: $H_0$: equal QPS of the filtered regime probability and of a two-negative-quarters rule against a reference chronology, on pre-registered quarters', r'formal: $H_0$: QPS egal pentru probabilitatea filtrată a regimului și pentru regula celor două trimestre negative, față de o cronologie de referință, pe trimestre preînregistrate'),
      T('falsified by a significant difference on quarters the model never saw, with GDP vintages', 'infirmată de o diferență semnificativă pe trimestre pe care modelul nu le-a văzut, cu ediții ale PIB')]),
    (T('Why it matters: Romania has no official business-cycle dating committee; policy reacts to regimes it can see only with delay', 'Miza: România nu are un comitet oficial de datare a ciclului economic; politica reacționează la regimuri pe care le vede doar cu întîrziere'),
     [T(r'literature to start from: \refHamA, \refCP, \refCKr, \refHamC', r'literatura de pornire: \refHamA, \refCP, \refCKr, \refHamC')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers that date business cycles of Central and Eastern European countries with Markov-switching models; give DOIs.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează articole recenzate care datează ciclurile economice ale țărilor din Europa Centrală și de Est cu modele Markov switching; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Which specification (MSM, MSIH, TVTP with which leading indicator) should separate recessions from volatility eras in Romanian GDP?}', r'\textbf{ipoteza}: \aiprompt{Ce specificație (MSM, MSIH, TVTP cu ce indicator avansat) ar trebui să separe recesiunile de erele de volatilitate în PIB-ul României?}'),
      T(r'\textbf{code and replication}: ask for a Hamilton filter, then reproduce a known number first (Hamilton\'s log-likelihood @{hp.ll})', r'\textbf{cod și replicare}: cereți un filtru Hamilton, apoi reproduceți întîi o cifră cunoscută (log-verosimilitatea lui Hamilton @{hp.ll})'),
      T(r'\textbf{robustness and critique}: \aiprompt{Act as a hostile referee: list the ways a regime dating could be an artefact of the specification or of the starting values.}', r'\textbf{robustețe și critică}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră felurile în care o datare a regimurilor poate fi un artefact al specificației sau al punctelor de pornire.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The likelihood is the global maximum among many starts, and the chosen regime is not degenerate', 'Verosimilitatea este maximul global dintre multe puncte de pornire, iar regimul ales nu este degenerat'),
    T('Real-time claims use filtered probabilities and data vintages, never smoothed probabilities', 'Afirmațiile despre timpul real folosesc probabilități filtrate și ediții ale datelor, niciodată probabilități netezite'),
    T('The number of regimes is tested by bootstrap or chosen by a criterion fixed in advance, not by a $\\chi^2$ count', 'Numărul de regimuri se testează prin bootstrap sau se alege printr-un criteriu fixat dinainte, nu prin numărarea gradelor de libertate ale unui $\\chi^2$'),
    T('The meaning of each regime is checked against external events, not assumed from its label', 'Semnificația fiecărui regim se verifică față de evenimente externe, nu se presupune din eticheta lui')), 'small')

chart(T('Mini-case: how robust is a recession dating?', 'Mini studiu de caz: cît de robustă este o datare a recesiunilor?'), 'ats_ch7_ai_case', 'ATS_ch7_hamilton', [
    T(r'US GDP growth: four specifications $\times$ three sample starts, all ending in 2019Q4; QPS of the smoothed low-mean-regime probability against the NBER quarters, 1985--2019',
      r'Creșterea PIB-ului SUA: patru specificații $\times$ trei începuturi ale eșantionului, toate pînă în T4 2019; QPS al probabilității netezite a regimului cu media scăzută față de trimestrele NBER, 1985--2019'),
    (T(r'QPS from @{ai.qmin} to @{ai.qmax} (a constant probability scores @{ai.qc})', r'QPS între @{ai.qmin} și @{ai.qmax} (o probabilitate constantă are scorul @{ai.qc})'),
     [T(r'@{ai.nf} variants flag most quarters: their low-mean regime is the Great Moderation', r'@{ai.nf} variante semnalează majoritatea trimestrelor: regimul lor cu media scăzută este Marea Moderație'),
      T(r'@{ai.both} of @{ai.n} dates both 2001 and 2008 without false alarms: an AI summary that reports one variant as ``the\'\' dating is wrong', r'@{ai.both} din @{ai.n} datează atît 2001, cît și 2008 fără alarme false: un rezumat AI care raportează o singură variantă drept „datarea” greșește')])],
    h='0.46\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{A regime-based business-cycle chronology for Romania}: replicate first, then extend', r'\textbf{O cronologie a ciclului economic din România pe baza regimurilor}: întîi replicare, apoi extindere'),
     [T(r'replicate: Hamilton\'s Table I on his data (log-likelihood @{hp.ll}) and the Filardo TVTP model (@{tv.ll})', r'replicați: Tabelul I al lui Hamilton pe datele lui (log-verosimilitatea @{hp.ll}) și modelul TVTP al lui Filardo (@{tv.ll})'),
      T('extend: Romanian GDP and industrial production, MSM against MSIH, TVTP with the ESI as leading indicator, Bayesian $K$ selection, real-time filtered probabilities', 'extindeți: PIB-ul și producția industrială ale României, MSM față de MSIH, TVTP cu ESI drept indicator avansat, alegerea bayesiană a lui $K$, probabilități filtrate în timp real'),
      T('pre-register: sample, specifications, starting-value design, the reference chronology and the QPS comparison', 'preînregistrați: eșantionul, specificațiile, schema punctelor de pornire, cronologia de referință și comparația QPS')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('The Hamilton filter and the Kim smoother are exact Bayesian recursions for a discrete latent state', 'Filtrul Hamilton și netezitorul Kim sînt recursii bayesiene exacte pentru o stare latentă discretă'),
    T('EM and numerical ML find local and degenerate maxima: many starts, then judgement', 'EM și verosimilitatea maximă numerică găsesc maxime locale și degenerate: multe puncte de pornire, apoi judecată'),
    T('The number of regimes is a non-standard testing problem: bootstrap, Garcia, CHP or information criteria', 'Numărul de regimuri este o problemă de testare nestandard: bootstrap, Garcia, CHP sau criterii informaționale'),
    T('TVTP, MS-VAR and MS-GARCH make the regimes economic; Gibbs sampling makes the uncertainty visible', 'TVTP, MS-VAR și MS-GARCH dau regimurilor un conținut economic; eșantionarea Gibbs face vizibilă incertitudinea'),
    T('Regimes, breaks and long memory are observationally close; forecasts decide', 'Regimurile, rupturile și memoria lungă sînt apropiate observațional; prognozele decid')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T(r'Why does the Kim smoother need $\hat\xi_{t+1|t}$ in the denominator?', r'De ce are nevoie netezitorul Kim de $\hat\xi_{t+1|t}$ la numitor?'),
        T(r'Why does Hamilton\'s MSM-AR(4) need 32 states?', r'De ce are nevoie modelul MSM-AR(4) al lui Hamilton de 32 de stări?'),
        T('Which three conditions of the LR asymptotics fail when testing one regime against two?', 'Ce trei condiții ale asimptoticii LR nu sînt îndeplinite la testarea unui regim față de două?'),
        T('Why is the naive MS-GARCH likelihood path-dependent?', 'De ce depinde de traiectorie verosimilitatea modelului MS-GARCH naiv?'),
        T('Why can a regime-switching mean produce a positive GPH estimate?', 'De ce poate o medie cu schimbare de regim să producă o estimație GPH pozitivă?'))),
    block(T('Next: Chapter 8', 'Urmează: Capitolul 8'), items(
        T('Advanced volatility modelling', 'Modelarea avansată a volatilității'),
        T('Realised measures, HAR and multivariate GARCH', 'Măsuri realizate, HAR și GARCH multivariat'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: EM for the Markov chain, step by step', 'Anexă: EM pentru lanțul Markov, pas cu pas'), items(
    T(r'Expected complete-data log-likelihood: $Q(\theta \mid \theta^{(m)}) = \sum_j\hat\xi_{j,1|T}\ln\rho_j + \sum_{t\ge2}\sum_{i,j}\hat\xi_{ij,t|T}\ln p_{ij} + \sum_t\sum_j\hat\xi_{j,t|T}\ln\eta_{jt}$', r'Log-verosimilitatea așteptată a datelor complete: $Q(\theta \mid \theta^{(m)}) = \sum_j\hat\xi_{j,1|T}\ln\rho_j + \sum_{t\ge2}\sum_{i,j}\hat\xi_{ij,t|T}\ln p_{ij} + \sum_t\sum_j\hat\xi_{j,t|T}\ln\eta_{jt}$'),
    T(r'Maximise $\sum_{t,j}\hat\xi_{ij,t|T}\ln p_{ij}$ subject to $\sum_j p_{ij} = 1$: Lagrangian $\Rightarrow p_{ij} = \sum_t\hat\xi_{ij,t|T}/\sum_t\sum_k\hat\xi_{ik,t|T}$', r'Maximizăm $\sum_{t,j}\hat\xi_{ij,t|T}\ln p_{ij}$ cu $\sum_j p_{ij} = 1$: lagrangianul $\Rightarrow p_{ij} = \sum_t\hat\xi_{ij,t|T}/\sum_t\sum_k\hat\xi_{ik,t|T}$'),
    T(r'and $\sum_k\hat\xi_{ik,t|T} = \hat\xi_{i,t-1|T}$; the Gaussian part gives weighted least squares', r'iar $\sum_k\hat\xi_{ik,t|T} = \hat\xi_{i,t-1|T}$; partea Gaussiană dă cele mai mici pătrate ponderate'),
    T(r'Monotonicity: $\ln L(\theta) = Q(\theta \mid \theta^{(m)}) - H(\theta \mid \theta^{(m)})$, and $H$ is maximised at $\theta^{(m)}$ (Gibbs inequality) \refDLR', r'Monotonia: $\ln L(\theta) = Q(\theta \mid \theta^{(m)}) - H(\theta \mid \theta^{(m)})$, iar $H$ este maxim în $\theta^{(m)}$ (inegalitatea Gibbs) \refDLR')), 'small')

D.frame(T('Appendix: the Kim smoother, the Markov step', 'Anexă: netezitorul Kim, pasul Markov'), items(
    T(r'$\Pr(S_t = i \mid S_{t+1} = j, Y_T) = \dfrac{f(y_{t+1:T} \mid S_t = i, S_{t+1} = j, Y_t)\Pr(S_t = i \mid S_{t+1} = j, Y_t)}{f(y_{t+1:T} \mid S_{t+1} = j, Y_t)}$', r'$\Pr(S_t = i \mid S_{t+1} = j, Y_T) = \dfrac{f(y_{t+1:T} \mid S_t = i, S_{t+1} = j, Y_t)\Pr(S_t = i \mid S_{t+1} = j, Y_t)}{f(y_{t+1:T} \mid S_{t+1} = j, Y_t)}$'),
    T(r'If $y_{t+1:T}$ depends on $S_t$ only through $S_{t+1}$ (true on the expanded state), the density ratio is 1', r'Dacă $y_{t+1:T}$ depinde de $S_t$ doar prin $S_{t+1}$ (adevărat pe starea extinsă), raportul densităților este 1'),
    T(r'Then $\Pr(S_t = i \mid S_{t+1} = j, Y_t) = \hat\xi_{i,t|t}p_{ij}/\hat\xi_{j,t+1|t}$; multiply by $\hat\xi_{j,t+1|T}$ and sum over $j$', r'Atunci $\Pr(S_t = i \mid S_{t+1} = j, Y_t) = \hat\xi_{i,t|t}p_{ij}/\hat\xi_{j,t+1|t}$; înmulțim cu $\hat\xi_{j,t+1|T}$ și sumăm după $j$'),
    T('With a continuous state (MS state space, Chapter 6) the ratio is not 1: Kim\'s smoother is then an approximation', 'Cu o stare continuă (spațiul stărilor cu schimbare de regim, Capitolul 6) raportul nu este 1: netezitorul Kim devine o aproximare')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
