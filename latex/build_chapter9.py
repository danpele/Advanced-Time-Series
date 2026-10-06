r"""
build_chapter9.py -- Capitolul 9 (VaR, ES și backtesting: elicitabilitate, funcții de scor și riscul de model), EN + RO
=========================================================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_09/ch9_numbers.json (generate_all_charts.py). Nicio cifră nu este
scrisă de mînă (în afara exemplelor teoretice și a valorilor publicate de Patton, Ziegel și Chen 2019, citate ca atare).
MFM, Capitolele 7-8 tratează VaR și ES pentru piețele financiare; aici: VaR și ES ca probleme de prognoză (funcționale,
elicitabilitate, funcții de scor), estimarea modelelor dinamice de cuantilă și ES (CAViaR, GAS-FZ, regresia comună),
backtesting ca test de calibrare condiționată, compararea prognozelor, orizontul, riscul de model și de estimare.
Ieșire:
  EN/Courses/chapter9_var_es_backtesting.tex
  RO/Cursuri/capitol9_var_es_backtesting.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_09/generate_all_charts.py
  python3 latex/build_chapter9.py && python3 latex/ats_build.py compile 9
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch9_common import REFS, QLURL, T, V2, day, bib, finalize, load, minus_fix   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(9, 'lecture', refs=REFS)
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
    'crash': ('ch9_crash_1987.png', C + 'S'+chr(92)+'%26P_500_index_around_the_time_of_the_crash.png',
              T('Figure', 'Figură') + ': Mark Carlson, Federal Reserve Board (2006); ' + PD + '; Wikimedia Commons'),
    'bis': ('ch9_bis_basel_2018.jpg', C + 'Bank_for_International_Settlements_in_the_late_afternoon.jpg',
            FOTO + ': Michal Pleskowicz (2018); CC BY-SA 4.0; Wikimedia Commons'),
    'koenker': ('ch9_koenker_2012.jpg', C + '17224_Roger_W._Koenker.jpeg',
                FOTO + ': Ivonne Vetter, MFO (2012); CC BY-SA 2.0 de; Wikimedia Commons'),
    'engle': ('ch9_engle_2022.jpg', C + '0603-Kraneshares_KRBN-RobertEngle-JonDemske-13.jpg',
              FOTO + ': Jon Demske (2022); CC BY-SA 4.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


def pv(key, x, d=3):
    """p-value: '<0.001' below 0.001."""
    if x < 10 ** (-d):
        V.raw(key, '$<$' + n(10 ** (-d), d))
    else:
        P(key, x, d)


# =============================================================================
# CIFRE
# =============================================================================
MODELS = ['RW-125', 'RW-250', 'RW-500', 'GCH-N', 'GCH-Skt', 'GCH-EDF', 'FZ-2F', 'FZ-1F', 'GCH-FZ', 'Hybrid']
MK = {m: m.replace('-', '').lower() for m in MODELS}
ASSETS = ['sp500', 'dax', 'bet', 'eurron', 'btc']
c = N['contour']
P('ct.v0', c['v0'], 2)
P('ct.e0', c['e0'], 2)
P('ct.vmin', c['vmin'], 2)
P('ct.zmin', c['zmin'], 3)
ls = N['levelsets']
P('ls.zq', ls['zq'], 2)
P('ls.es', ls['es_n'], 3)
P('ls.dev', abs(ls['es_dev']), 3)
P('ls.lam', ls['lam_dev'], 2)
P('ls.mid', ls['es_mid'], 3)
o = N['overview']
P('ov.min', o['es_min'], 1)
V.raw('ov.day', day(o['es_min_day']))
P('ov.med', o['es_med'], 2)
# CAViaR
cv = N['caviar']
V.raw('cv.d0', day(cv['dates'][0]))
V.raw('cv.d1', day(cv['dates'][1]))
V.raw('cv.d2', day(cv['dates'][2]))
V.raw('cv.d3', day(cv['dates'][3]))
for s in ('SAV', 'AS', 'IG', 'ADAPT'):
    r = cv[s]
    b = [abs(x) for x in r['b']] if s == 'ADAPT' else r['b']
    for i, (bb, se) in enumerate(zip(b, r['se'])):
        P(f'cv.{s}.b{i}', bb, 3)
        P(f'cv.{s}.s{i}', se, 3)
    P(f'cv.{s}.rq', 100 * r['rq'], 3)
    P(f'cv.{s}.hi', 100 * r['hit_in'], 2)
    P(f'cv.{s}.ho', 100 * r['hit_out'], 1)
    P(f'cv.{s}.dq', r['dq_out'][0], 1)
    pv(f'cv.{s}.dqp', r['dq_out'][1])
    P(f'cv.{s}.pin', 100 * r['pin_out'], 2)
nic = N['nic']
P('nic.ratio', nic['as_ratio'], 0)
P('nic.med', nic['median']['AS'], 2)
# PZC
rep = N['pzcrep']
V.raw('pz.order', f"ARMA({rep['order'][0]}, {rep['order'][1]})")
P('pz.alpha', rep['garch'][1], 3)
P('pz.beta', rep['garch'][2], 3)
P('pz.nu', rep['nu'], 2)
P('pz.lam', rep['lam'], 3)
V.raw('pz.nin', str(rep['n_in']))
V.int('pz.T', rep['0.05']['T'])
PAPER = {0.05: [0.914, 0.959, 1.023, 0.876, 0.866, 0.862, 0.856, 0.853, 0.862, 0.869],
         0.025: [1.119, 1.164, 1.245, 1.089, 1.043, 1.028, 1.041, 1.032, 1.020, 1.034]}
PAPER_DM = [3.912, 4.423, 5.483, 1.986, 1.421, 1.198, 0.582, None, 1.266, 1.978]     # PZC Table 9, column FZ-1F
for a, k in ((0.05, '5'), (0.025, '25')):
    r = rep[str(a)]
    for i, m in enumerate(MODELS):
        P(f'pz{k}.{MK[m]}', r['loss'][m], 3)
        P(f'pp{k}.{MK[m]}', PAPER[a][i], 3)
        pv(f'pg{k}.{MK[m]}.v', r['gof'][m][0])
        pv(f'pg{k}.{MK[m]}.e', r['gof'][m][1])
    P(f'pz{k}.dev', N['pzctable']['maxdev'][str(a)], 3)
f1 = rep['0.05']['fz']['FZ-1F']
hy = rep['0.05']['fz']['Hybrid']
P('pz.f1.b', f1[0], 3)
P('pz.f1.g', f1[1], 4)
P('pz.hy.b', hy[0], 3)
P('pz.hy.g', hy[1], 4)
P('pz.hy.d', hy[2], 3)
P('pz.min', N['pzcpaths']['min_es'], 1)
dmc = N['dm']['fz1f_col']
for i, m in enumerate(MODELS):
    if m != 'FZ-1F':
        P(f'dm.{MK[m]}', dmc[m], 2)
        P(f'dmp.{MK[m]}', PAPER_DM[i], 2)
mu = N['murphy']
P('mu.fz', 100 * mu['fz_better'], 0)
P('mu.edf', 100 * mu['edf_vs_rw'], 0)
for m in ('RW-250', 'GCH-EDF', 'FZ-1F'):
    P(f'mu.pin.{MK[m]}', 100 * mu['pin'][m], 2)
er = N['esreg']
V.int('er.T', er['T'])
for i in range(2):
    P(f'er.b{i}', er['b'][i], 3)
    P(f'er.g{i}', er['g'][i], 3)
    P(f'er.bs{i}', er['se'][i], 3)
    P(f'er.gs{i}', er['se'][2 + i], 3)
    P(f'er.q{i}', er['b_qr'][i], 3)
P('er.hit', 100 * er['hit'], 2)
P('er.b1a', abs(er['b'][1]), 2)
P('er.g1a', abs(er['g'][1]), 2)
P('er.ratio', er['ratio'], 2)
pv('er.pv', er['gof']['p_var'])
pv('er.pe', er['gof']['p_es'])
# backtests
bt = N['backtests']['table']
for nm in ASSETS:
    for m in MODELS:
        r = bt[nm][m]
        P(f'bt.{nm}.{MK[m]}.hit', 100 * r['hit'], 1)
        pv(f'bt.{nm}.{MK[m]}.dq', r['dq'])
        pv(f'bt.{nm}.{MK[m]}.dur', r['dur'])
        P(f'bt.{nm}.{MK[m]}.loss', r['loss'], 3)
        if 'mf' in r:
            pv(f'bt.{nm}.{MK[m]}.mf', r['mf'])
V.raw('bt.npass', str(N['backtests']['n_pass']))
du = N['durations']
for m in ('RW-250', 'GCH-EDF', 'FZ-1F'):
    P(f'du.{MK[m]}.b', du[m]['b'], 2)
    pv(f'du.{MK[m]}.p', du[m]['p'])
    P(f'du.{MK[m]}.s5', 100 * du[m]['share5'], 0)
    P(f'du.{MK[m]}.med', du[m]['med'], 0)
    V.raw(f'du.{MK[m]}.n', str(du[m]['n']))
P('du.geo5', 100 * du['geo5'], 0)
es = N['estrisk']
for k, v in es.items():
    if k == 'reps':
        continue
    for kk in ('kup', 'kup0', 'dq', 'dq0'):
        P(f'mc.{k}.{kk}', 100 * v[kk], 0)
    P(f'mc.{k}.sd', 100 * v['hit_sd'], 2)
V.raw('mc.reps', str(es['reps']))
# comparison
st_ = N['stress']
cmpd = st_['cmp']
for nm in ASSETS:
    V.raw(f'cmp.{nm}.start', day(cmpd[nm]['start']))
    V.int(f'cmp.{nm}.T', cmpd[nm]['T'])
    for k, w in st_['best'][nm].items():
        V.raw(f'best.{nm}.{k}', w)
    for k, v in cmpd[nm]['periods'].items():
        V.raw(f'cmp.{nm}.{k}.T', str(v['T']))
        V.raw(f'cmp.{nm}.{k}.h', str(v['hits']))
sz = N['mcs']['sizes']
for k in sz:
    for nm in ASSETS:
        V.raw(f'mcs.{k}.{nm}', str(sz[k][nm]))
sq = N['sqrt']
for k in ('r_lo', 'r_hi', 'r_med', 'r_min', 'r_max'):
    P(f'sq.{k}', sq[k], 2)
V.raw('sq.n', str(sq['n']))
V.raw('sq.nf', str(sq['n_fhs']))
V.raw('sq.ns', str(sq['n_sqrt']))
P('sq.exp', 0.01 * sq['n'], 1)
P('sq.kf', sq['kup_fhs'], 2)
P('sq.ks', sq['kup_sqrt'], 2)
rr = N['riskratio']
for nm in ('sp500', 'bet'):
    r = rr[nm]
    for k in ('med', 'q90', 'mx', 's2008', 's2020', 'calm'):
        P(f'rr.{nm}.{k}', r[k], 1)
    V.raw(f'rr.{nm}.day', day(r['mx_day']))
    for k, v in r['hits'].items():
        P(f'rr.{nm}.h.{k}', 100 * v, 1)
    P(f'rr.{nm}.hsmax', 100 * r['argmax'].get('HS', 0), 0)
    P(f'rr.{nm}.ewmin', 100 * r['argmin'].get('EWMA', 0), 0)
ci = N['esci']
P('ci.med', 100 * ci['rel_med'], 0)
P('ci.max', 100 * ci['rel_max'], 0)
P('ci.min', 100 * ci['rel_min'], 0)
row20 = [r for r in ci['rows'] if r['date'] == '2020-06-30'][0]
P('ci.20', row20['es'], 2)
P('ci.20lo', row20['lo'], 2)
P('ci.20hi', row20['hi'], 2)
ex = N['extremal']
for nm in ASSETS:
    P(f'ex.{nm}.r', ex[nm]['raw'], 2)
    P(f'ex.{nm}.f', ex[nm]['filt'], 2)
cf = N['conformal']
for nm in ('btc', 'bet'):
    r = cf[nm]
    P(f'cf.{nm}.b', 100 * r['base'], 2)
    P(f'cf.{nm}.a', 100 * r['aci'], 2)
    pv(f'cf.{nm}.kb', r['kup_base'])
    pv(f'cf.{nm}.ka', r['kup_aci'])
    pv(f'cf.{nm}.cb', r['cc_base'])
    pv(f'cf.{nm}.ca', r['cc_aci'])
    P(f'cf.{nm}.rb', 100 * r['rmax_base'], 1)
    P(f'cf.{nm}.ra', 100 * r['rmax_aci'], 1)
    V.int(f'cf.{nm}.T', r['T'])
ai = N['ai']
V.raw('ai.n', str(ai['n']))
V.raw('ai.nw', str(ai['n_win_models']))
V.raw('ai.skt', str(ai['wins'].get('GCH-Skt', 0)))
V.raw('ai.fz1', str(ai['wins'].get('FZ-1F', 0)))
V.raw('ai.smin', str(ai['size_min']))
V.raw('ai.smax', str(ai['size_max']))
P('ai.smed', ai['size_med'], 0)
V.raw('ai.fzin', str(ai['fz1f_in']))
V.raw('ai.nde', V2('', ' de') if ai['n'] >= 20 else '')
V.raw('ai.fzde', V2('', ' de') if ai['fz1f_in'] >= 20 else '')
minus_fix(V)

TB = '>{\\raggedright\\arraybackslash}'

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: a VaR or an ES forecast is a point forecast of a tail functional; how do we estimate dynamic models for it, test whether it is calibrated and decide which forecast is better?',
       r'\textbf{Întrebarea}: o prognoză VaR sau ES este o prognoză punctuală a unei funcționale de coadă; cum estimăm modele dinamice pentru ea, cum testăm dacă este calibrată și cum decidem care prognoză este mai bună?'),
     [T('the tail is observed rarely: a forecast must be judged with a loss that is consistent for its target, on few informative days',
        'coada se observă rar: o prognoză se judecă cu o pierdere consistentă pentru ținta ei, pe puține zile informative')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('risk measures as functionals; elicitability, the Fissler--Ziegel class, FZ0 and Murphy diagrams',
        'măsurile de risc ca funcționale; elicitabilitate, clasa Fissler--Ziegel, FZ0 și diagramele Murphy'),
      T('quantile regression and CAViaR; semiparametric (VaR, ES) models and joint regression',
        'regresia cuantilică și CAViaR; modele semiparametrice pentru perechea (VaR, ES) și regresia comună'),
      T('backtesting as conditional calibration; estimation risk in backtests; comparison with the MCS in stress periods',
        'backtesting ca test de calibrare condiționată; riscul de estimare în backtesting; comparația prin MCS în perioadele de criză'),
      T('the horizon (square-root-of-time), model risk, extremes under dependence, conformal calibration',
        'orizontul (regula rădăcinii pătrate a timpului), riscul de model, extremele sub dependență, calibrarea conformală')]),
    T('We build on Chapter 1 (scoring rules, elicitability, DM, MCS), Chapter 0 (HAC, bootstrap), Chapter 8 (volatility) and TSA, Chapter 5 (GARCH); Seminar 9 comes before this lecture',
      'Pornim de la Capitolul 1 (reguli de scor, elicitabilitate, DM, MCS), Capitolul 0 (HAC, bootstrap), Capitolul 8 (volatilitate) și TSA, Capitolul 5 (GARCH); Seminarul 9 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Characterise the scoring functions consistent for quantiles and for the pair (VaR, ES), and prove that ES alone is not elicitable',
      'Caracterizați funcțiile de scor consistente pentru cuantile și pentru perechea (VaR, ES) și demonstrați că ES singur nu este elicitabil'),
    T('Estimate CAViaR models with the Engle--Manganelli procedure, compute their standard errors and run the DQ test',
      'Estimați modele CAViaR cu procedura Engle--Manganelli, calculați erorile lor standard și aplicați testul DQ'),
    T('Estimate semiparametric dynamic (VaR, ES) models by FZ0 minimisation and replicate the out-of-sample comparison of Patton, Ziegel and Chen',
      'Estimați modele dinamice semiparametrice pentru (VaR, ES) prin minimizarea pierderii FZ0 și replicați comparația în afara eșantionului a lui Patton, Ziegel și Chen'),
    T('Test conditional calibration with identification functions, account for estimation risk, and compare risk models with DM tests, Murphy diagrams and the MCS',
      'Testați calibrarea condiționată cu funcții de identificare, țineți cont de riscul de estimare și comparați modelele de risc prin teste DM, diagrame Murphy și MCS'),
    T('Quantify horizon, model and estimation risk, and correct a miscalibrated VaR by adaptive conformal inference',
      'Cuantificați riscul de orizont, de model și de estimare și corectați un VaR necalibrat prin inferență conformală adaptivă')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Theory: \refGn; \refFZ; \refEGJK; \refNZ', r'Teorie: \refGn; \refFZ; \refEGJK; \refNZ'),
     [T(r'Models: \refKB; \refEM; \refPZC; \refDB', r'Modele: \refKB; \refEM; \refPZC; \refDB'),
      T(r'Survey of forecasting practice: \refPet', r'Sinteză despre practica prognozei: \refPet')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_09}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_09}'),
     [T(r'CAViaR, the GAS-FZ models, the joint regression, the backtests, DM and the MCS written in \texttt{numpy}/\texttt{scipy}; \texttt{numba} only speeds up the recursions',
        r'CAViaR, modelele GAS-FZ, regresia comună, testele de backtesting, DM și MCS scrise în \texttt{numpy}/\texttt{scipy}; \texttt{numba} doar accelerează recursiile')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter9_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter9_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{3.0cm}' + TB + 'p{4.6cm}' + TB + 'p{4.4cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source, sample}', r'\textbf{Sursa, eșantionul}') + ' & ' + T(r'\textbf{In sample / out of sample}', r'\textbf{În eșantion / în afara eșantionului}'),
    ['S\\&P 500, DAX & ' + T('EODHD daily closes, January 1990 -- September 2026', 'închideri zilnice EODHD, ianuarie 1990 -- septembrie 2026') + ' & 1990--1999 / 2000--2026',
     'BET & ' + T('EODHD, official closes, 2000--2026', 'EODHD, închideri oficiale, 2000--2026') + ' & 2000--2009 / 2010--2026',
     'EUR/RON & ' + T('BNR reference rate, July 2005 -- September 2026', 'cursul de referință BNR, iulie 2005 -- septembrie 2026') + ' & ' + T('to June 2015 / from July 2015', 'pînă în iunie 2015 / din iulie 2015'),
     'Bitcoin & ' + T('EODHD, 7 days a week, September 2014 -- September 2026', 'EODHD, 7 zile pe săptămînă, septembrie 2014 -- septembrie 2026') + ' & 2014--2019 / 2020--2026',
     'VIX & ' + T('EODHD daily closes', 'închideri zilnice EODHD') + ' & ' + T('regressor of the joint (VaR, ES) regression', 'regresor în regresia comună (VaR, ES)')],
    size='scriptsize') + items(
    T('Daily log returns in \\%; ten in-sample years as in Patton, Ziegel and Chen (2019), five for Bitcoin; stress periods: September 2008 -- March 2009, February -- June 2020, 2022, March -- June 2025',
      'Randamente logaritmice zilnice în \\%; zece ani în eșantion, ca la Patton, Ziegel și Chen (2019), cinci pentru Bitcoin; perioade de criză: septembrie 2008 -- martie 2009, februarie -- iunie 2020, 2022, martie -- iunie 2025')), 'footnotesize')

D.frame(T('From a crash to a regulatory functional', 'De la un crah la o funcțională de reglementare'), two(
    ph('crash', T('The S\\&P 500 around 19 October 1987', 'S\\&P 500 în jurul datei de 19 octombrie 1987'), h='0.36\\textheight'),
    items(T('1987: a one-day fall of about 20\\% in US equities shows that the tail, not the variance, decides solvency',
            '1987: o cădere de circa 20\\% într-o singură zi pe piața acțiunilor din SUA arată că solvabilitatea o decide coada, nu varianța'),
          T(r'1996: the Basel Committee adopts VaR for market risk and a traffic-light backtest of its hits \refBCBS',
            r'1996: Comitetul de la Basel adoptă VaR pentru riscul de piață și un backtest de tip semafor pentru depășiri \refBCBS'),
          T(r'1999--2002: VaR is not coherent; ES is \refADEH, \refAT', r'1999--2002: VaR nu este coerent; ES este coerent \refADEH, \refAT'),
          T(r'2011--2016: ES is not elicitable \refGn, but (VaR, ES) is jointly elicitable \refFZ', r'2011--2016: ES nu este elicitabil \refGn, dar perechea (VaR, ES) este elicitabilă împreună \refFZ'),
          T(r'FRTB: capital on ES 2.5\%, backtests on VaR 1\% and VaR 2.5\% \refMAR', r'FRTB: capitalul pe baza ES 2,5\%, backtesting pe VaR 1\% și VaR 2,5\% \refMAR')), '0.42', '0.56'), 'footnotesize')

D.frame(T('Basel: the forecaster and the referee', 'Basel: prognozatorul și arbitrul'), two(
    ph('bis', T('Bank for International Settlements, Basel, 2018', 'Banca Reglementelor Internaționale, Basel, 2018'), h='0.5\\textheight'),
    items(T('A bank issues a daily forecast of its own tail; the supervisor checks it after the fact', 'O bancă emite zilnic o prognoză a propriei cozi; supraveghetorul o verifică ulterior'),
          T('Two questions that statistics separates: is the forecast \\textbf{calibrated} (backtest) and is it \\textbf{better} than another (comparison)?',
            'Două întrebări pe care statistica le separă: este prognoza \\textbf{calibrată} (backtesting) și este ea \\textbf{mai bună} decît alta (comparație)?'),
          T(r'Elicitability decides which forecasts can be compared at all \refNZ', r'Elicitabilitatea decide care prognoze pot fi comparate \refNZ'),
          T('The incentive matters: a scoring rule rewards honest reporting only if it is strictly consistent for the target',
            'Contează stimulentul: o regulă de scor răsplătește raportarea onestă doar dacă este strict consistentă pentru țintă')), '0.36', '0.62'), 'small')

# =============================================================================
# 1. MĂSURILE DE RISC CA FUNCȚIONALE
# =============================================================================
D.section('Risk measures as forecast functionals', 'Măsurile de risc ca funcționale de prognoză')

D.frame(T('Known from TSA and MFM, and new here', 'Cunoscut din TSA și MFM și elemente noi'), items(
    (T('Known: VaR and ES by historical simulation, parametric, filtered HS and EVT; Kupiec and Christoffersen tests; the Basel traffic light (TSA, Chapter 5; MFM, Chapters 7--8)',
       'Cunoscut: VaR și ES prin simulare istorică, metode parametrice, FHS și EVT; testele Kupiec și Christoffersen; semaforul Basel (TSA, Capitolul 5; MFM, Capitolele 7--8)'),
     []),
    (T('New: the forecasting view', 'Nou: perspectiva prognozei'),
     [T('which losses are consistent for a quantile and for (VaR, ES); what elicitability buys and what it does not',
        'ce pierderi sînt consistente pentru o cuantilă și pentru perechea (VaR, ES); ce aduce elicitabilitatea și ce nu aduce'),
      T('M-estimation of dynamic quantile and ES models: identification, asymptotics, non-smooth objectives',
        'M-estimarea modelelor dinamice de cuantilă și de ES: identificare, asimptotică, funcții obiectiv nenetede'),
      T('backtests as moment tests of conditional calibration, with estimation risk; comparisons that survive multiple testing',
        'backtesting ca teste de momente ale calibrării condiționate, cu risc de estimare; comparații valide sub testare multiplă')]),
    T('Replications: Engle and Manganelli (2004) and Patton, Ziegel and Chen (2019), with the specifications of the papers, on our data',
      'Replicări: Engle și Manganelli (2004) și Patton, Ziegel și Chen (2019), cu specificațiile din lucrări, pe datele noastre')), 'small')

D.frame(T('VaR and ES as functionals', 'VaR și ES ca funcționale'), items(
    (T(r'Return $Y$ with distribution $F$; level $\alpha$ (VaR 1\%: $\alpha = 0.01$); quantile $q_\alpha(F) = \inf\{y: F(y) \ge \alpha\}$',
       r'Randamentul $Y$ cu distribuția $F$; nivelul $\alpha$ (VaR 1\%: $\alpha = 0{,}01$); cuantila $q_\alpha(F) = \inf\{y: F(y) \ge \alpha\}$'),
     [T(r'$\mathrm{VaR}_\alpha(F) = -q_\alpha(F)$; target hit rate $\Pr(Y < -\mathrm{VaR}_\alpha) = \alpha$', r'$\mathrm{VaR}_\alpha(F) = -q_\alpha(F)$; rata de depășire țintă $\Pr(Y < -\mathrm{VaR}_\alpha) = \alpha$')]),
    (T(r'$\mathrm{ES}_\alpha(F) = -\dfrac{1}{\alpha}\displaystyle\int_0^\alpha q_u(F)\,du$ \refAT; for continuous $F$: $\mathrm{ES}_\alpha = -\E[Y \mid Y \le q_\alpha]$',
       r'$\mathrm{ES}_\alpha(F) = -\dfrac{1}{\alpha}\displaystyle\int_0^\alpha q_u(F)\,du$ \refAT; pentru $F$ continuă: $\mathrm{ES}_\alpha = -\E[Y \mid Y \le q_\alpha]$'),
     [T(r'ES is coherent (subadditive) \refADEH; VaR is not; ES needs $\E|Y| < \infty$', r'ES este coerent (subaditiv) \refADEH; VaR nu este; ES cere $\E|Y| < \infty$')]),
    T(r'In formulas we work with the return-scale pair $(v, e) = (q_\alpha, -\mathrm{ES}_\alpha)$, both negative: $e \le v < 0$',
      r'În formule lucrăm cu perechea pe scala randamentelor $(v, e) = (q_\alpha, -\mathrm{ES}_\alpha)$, ambele negative: $e \le v < 0$'),
    T(r'Both are \textbf{functionals} $\mathrm T(F)$: a forecast of them is a point forecast of the predictive distribution, as in Chapter 1',
      r'Ambele sînt \textbf{funcționale} $\mathrm T(F)$: o prognoză a lor este o prognoză punctuală a distribuției predictive, ca în Capitolul 1')), 'small')

D.frame(T('Conditional risk forecasts: three routes', 'Prognoze condiționate de risc: trei căi'), items(
    T(r'Target: $(v_t, e_t) = \mathrm T(F_{t|t-1})$, with $F_{t|t-1}$ the distribution of $Y_t$ given $\mathcal F_{t-1}$', r'Ținta: $(v_t, e_t) = \mathrm T(F_{t|t-1})$, unde $F_{t|t-1}$ este distribuția lui $Y_t$ condiționată de $\mathcal F_{t-1}$'),
    (T(r'\textbf{Location--scale}: $Y_t = \mu_t + \sigma_t\eta_t$, $\eta_t$ i.i.d.\ $\Rightarrow v_t = \mu_t + \sigma_t q_\alpha(\eta)$, $e_t = \mu_t + \sigma_t\E[\eta \mid \eta \le q_\alpha(\eta)]$', r'\textbf{Poziție--scală}: $Y_t = \mu_t + \sigma_t\eta_t$, $\eta_t$ i.i.d.\ $\Rightarrow v_t = \mu_t + \sigma_t q_\alpha(\eta)$, $e_t = \mu_t + \sigma_t\E[\eta \mid \eta \le q_\alpha(\eta)]$'),
     [T('GARCH with Normal, skewed-t \\refHan\\ or empirical (EDF) innovations; the ratio $e_t/v_t$ is then constant over time', 'GARCH cu inovații din distribuția Normală, t asimetrică \\refHan\\ sau empirice (EDF); raportul $e_t/v_t$ este atunci constant în timp')]),
    (T(r'\textbf{Direct quantile dynamics}: $v_t = v(\mathcal F_{t-1}; \beta)$ estimated by quantile loss, no distribution \refEM', r'\textbf{Dinamica directă a cuantilei}: $v_t = v(\mathcal F_{t-1}; \beta)$ estimat prin pierderea cuantilică, fără distribuție \refEM'), []),
    (T(r'\textbf{Joint semiparametric}: $(v_t, e_t) = (v, e)(\mathcal F_{t-1}; \theta)$ estimated by a Fissler--Ziegel loss \refPZC, \refDB', r'\textbf{Semiparametric comun}: $(v_t, e_t) = (v, e)(\mathcal F_{t-1}; \theta)$ estimat printr-o pierdere Fissler--Ziegel \refPZC, \refDB'), []),
    T('Every route produces a point forecast of a functional; the scoring function of the next section is what makes them comparable',
      'Fiecare cale produce o prognoză punctuală a unei funcționale; funcția de scor din secțiunea următoare le face comparabile')), 'small')

chart(T('Thirty-six years of tail forecasts', 'Treizeci și șase de ani de prognoze ale cozii'), 'ats_ch9_overview', 'ATS_ch9_pzc', [
    T(r'S\&P 500 daily returns; the GAS-1F model of Patton, Ziegel and Chen, parameters estimated once on 1990--1999 and then only filtered; shaded: the four stress periods',
      r'Randamentele zilnice ale S\&P 500; modelul GAS-1F al lui Patton, Ziegel și Chen, cu parametrii estimați o singură dată pe 1990--1999 și apoi doar filtrați; zonele colorate: cele patru perioade de criză')],
    h='0.5\\textheight')

interp(('the long-run forecasts', 'prognozelor pe termen lung'), [
    T(r'The ES 2.5\% forecast ranges from about @{ov.med}\% (median) to @{ov.min}\% on @{ov.day}: tail risk moves as much as volatility', r'Prognoza ES 2,5\% variază de la circa @{ov.med}\% (mediana) la @{ov.min}\% la @{ov.day}: riscul de coadă se mișcă la fel de mult ca volatilitatea'),
    T('The forecasts react only on hit days and decay smoothly otherwise: the score-driven update of the GAS model', 'Prognozele reacționează doar în zilele cu depășiri și scad lin în rest: actualizarea prin scor a modelului GAS'),
    T('Parameters fixed in 1999 still track 2008, 2020 and 2025: the dynamics generalise, the level does not need re-estimation', 'Parametrii fixați în 1999 urmăresc încă anii 2008, 2020 și 2025: dinamica se generalizează, nivelul nu cere reestimare'),
    T('Whether this is good enough is a testing question (Sections 5--6), not a visual one', 'Dacă aceasta este suficient este o întrebare de testare (secțiunile 5--6), nu una vizuală')])

D.recap(('Risk measures as functionals', 'măsurile de risc ca funcționale'), [
    T('VaR is a quantile, ES an integral of quantiles; both are functionals of the predictive distribution', 'VaR este o cuantilă, ES o integrală de cuantile; ambele sînt funcționale ale distribuției predictive'),
    T('Three routes: location--scale, direct quantile dynamics, joint semiparametric models', 'Trei căi: poziție--scală, dinamica directă a cuantilei, modele semiparametrice comune'),
    T('The convention: VaR 1\\%, ES 2.5\\%, $\\alpha$ is the target hit rate', 'Convenția: VaR 1\\%, ES 2,5\\%, $\\alpha$ este rata de depășire țintă')])

# =============================================================================
# 2. ELICITABILITATE
# =============================================================================
D.section('Elicitability and scoring functions', 'Elicitabilitate și funcții de scor')

D.frame(T('Consistency, elicitability, identification', 'Consistență, elicitabilitate, identificare'), items(
    (T(r'A scoring function $S(x, y)$ is \textbf{consistent} for $\mathrm T$ on a class $\mathcal F$ if $\E_F S(\mathrm T(F), Y) \le \E_F S(x, Y)$ for all $x$, $F \in \mathcal F$; \textbf{strictly} if equality forces $x = \mathrm T(F)$ \refGn',
       r'O funcție de scor $S(x, y)$ este \textbf{consistentă} pentru $\mathrm T$ pe o clasă $\mathcal F$ dacă $\E_F S(\mathrm T(F), Y) \le \E_F S(x, Y)$ pentru orice $x$ și $F \in \mathcal F$; \textbf{strict} dacă egalitatea impune $x = \mathrm T(F)$ \refGn'),
     [T(r'$\mathrm T$ is \textbf{elicitable} if a strictly consistent $S$ exists (Chapter 1)', r'$\mathrm T$ este \textbf{elicitabilă} dacă există o funcție $S$ strict consistentă (Capitolul 1)')]),
    (T(r'\textbf{Identification function}: $V(x, y)$ with $\E_F V(x, Y) = 0 \iff x = \mathrm T(F)$', r'\textbf{Funcție de identificare}: $V(x, y)$ cu $\E_F V(x, Y) = 0 \iff x = \mathrm T(F)$'),
     [T(r'quantile: $V(x, y) = \mathbf 1\{y \le x\} - \alpha$; mean: $V(x, y) = x - y$', r'cuantila: $V(x, y) = \mathbf 1\{y \le x\} - \alpha$; media: $V(x, y) = x - y$'),
      T(r'Osband\'s principle: $\partial_x\E_F S(x, Y) = h(x)\,\E_F V(x, Y)$, $h > 0$; scores are integrated identification functions \refFZ', r'Principiul lui Osband: $\partial_x\E_F S(x, Y) = h(x)\,\E_F V(x, Y)$, $h > 0$; scorurile sînt funcții de identificare integrate \refFZ')]),
    T('Identification functions give \\textbf{backtests} (is the forecast calibrated?); scoring functions give \\textbf{comparisons} (which forecast is better?) \\refNZ',
      'Funcțiile de identificare dau \\textbf{backtesting} (este prognoza calibrată?); funcțiile de scor dau \\textbf{comparații} (care prognoză este mai bună?) \\refNZ')), 'small')

D.frame(T('Quantiles: all consistent scores', 'Cuantilele: toate scorurile consistente'), items(
    (T(r'\textbf{Theorem} \refGn: under mild conditions, $S$ is consistent for $q_\alpha$ iff $S(x, y) = (\mathbf 1\{y \le x\} - \alpha)(G(x) - G(y))$ with $G$ non-decreasing (generalised piecewise linear, GPL)',
       r'\textbf{Teoremă} \refGn: în condiții slabe, $S$ este consistentă pentru $q_\alpha$ dacă și numai dacă $S(x, y) = (\mathbf 1\{y \le x\} - \alpha)(G(x) - G(y))$, cu $G$ nedescrescătoare (liniară pe porțiuni generalizată, GPL)'),
     [T(r'$G(x) = x$: the pinball loss; $G$ strictly increasing gives strict consistency', r'$G(x) = x$: pierderea pinball; $G$ strict crescătoare dă consistența strictă')]),
    (T(r'Why: $\partial_x\E_F S(x, Y) = G\'(x)\,(F(x) - \alpha)$, negative below $q_\alpha$, positive above (Appendix)', r'Motivul: $\partial_x\E_F S(x, Y) = G\'(x)\,(F(x) - \alpha)$, negativă sub $q_\alpha$, pozitivă deasupra (Anexă)'),
     [T(r'$G(x) = \ln x$ on positive variables gives a scale-free (zero-homogeneous) score', r'$G(x) = \ln x$ pentru variabile pozitive dă un scor independent de scală (omogen de grad zero)')]),
    T('Different $G$ give the same optimal forecast but can rank two misspecified forecasts differently: the choice of $G$ is a modelling choice',
      'Funcții $G$ diferite dau aceeași prognoză optimă, dar pot ordona diferit două prognoze greșite: alegerea lui $G$ este o decizie de modelare'),
    T(r'Expectiles (asymmetric squared loss) are the only elicitable coherent risk measures \refZie; \refTayA\ uses them for VaR and ES', r'Expectilele (pierdere pătratică asimetrică) sînt singurele măsuri de risc coerente și elicitabile \refZie; \refTayA\ le folosește pentru VaR și ES')), 'small')

D.frame(T('ES is not elicitable', 'ES nu este elicitabil'), items(
    (T(r'\textbf{Necessary condition} \refGn: if $\mathrm T$ is elicitable, its level sets $\{F: \mathrm T(F) = t\}$ are convex', r'\textbf{Condiție necesară} \refGn: dacă $\mathrm T$ este elicitabilă, mulțimile ei de nivel $\{F: \mathrm T(F) = t\}$ sînt convexe'),
     [T(r'proof: if $\E_{F_0}S(t, Y) \le \E_{F_0}S(x, Y)$ and the same for $F_1$, the inequality holds for $\lambda F_0 + (1 - \lambda)F_1$ (expectations are linear in $F$)', r'demonstrație: dacă $\E_{F_0}S(t, Y) \le \E_{F_0}S(x, Y)$ și la fel pentru $F_1$, inegalitatea rămîne pentru $\lambda F_0 + (1 - \lambda)F_1$ (media este liniară în $F$)')]),
    (T(r'Quantiles pass: if $F_0(t) = F_1(t) = \alpha$, then every mixture has $F_\lambda(t) = \alpha$', r'Cuantilele trec testul: dacă $F_0(t) = F_1(t) = \alpha$, orice amestec are $F_\lambda(t) = \alpha$'), []),
    (T(r'ES fails: the mixture changes the quantile, so it changes which part of each component enters the tail mean \refWeb', r'ES nu trece: amestecul schimbă cuantila, deci schimbă partea din fiecare componentă care intră în media cozii \refWeb'),
     [T('consequence: no loss function can rank ES forecasts alone; average losses of ES forecasts are not meaningful by themselves', 'consecință: nicio funcție de pierdere nu poate ordona prognoze ES singure; pierderile medii ale prognozelor ES nu au sens luate separat')]),
    T(r'Variance fails for the same reason; (mean, second moment) and (VaR, ES) are elicitable as pairs (\refFZ, ``higher order elicitability\'\')', r'Varianța nu trece din același motiv; perechile (medie, al doilea moment) și (VaR, ES) sînt elicitabile (\refFZ, „elicitabilitate de ordin superior”)')), 'small')

chart(T('Level sets under mixing', 'Mulțimile de nivel la amestecare'), 'ats_ch9_level_sets', 'ATS_ch9_scoring', [
    T(r'Left: $N(0, 1)$ and a $t(3)$ rescaled to the same 2.5\% quantile; right: $N(0, 1)$ and a $t(3)$ rescaled to the same ES 2.5\%; curves: the functional of the mixture',
      r'Stînga: $N(0, 1)$ și o $t(3)$ rescalată la aceeași cuantilă de 2,5\%; dreapta: $N(0, 1)$ și o $t(3)$ rescalată la același ES 2,5\%; curbele: funcționala amestecului')],
    h='0.5\\textheight')

interp(('the level sets', 'mulțimilor de nivel'), [
    T(r'The quantile of every mixture stays at @{ls.zq}: the level set of $q_{0.025}$ is convex', r'Cuantila oricărui amestec rămîne @{ls.zq}: mulțimea de nivel a lui $q_{0{,}025}$ este convexă'),
    T(r'Both components have tail mean @{ls.es}; the mixture moves away by up to @{ls.dev} (at weight @{ls.lam}): the level set of ES is not convex', r'Ambele componente au media cozii @{ls.es}; amestecul se îndepărtează cu pînă la @{ls.dev} (la ponderea @{ls.lam}): mulțimea de nivel a ES nu este convexă'),
    T('The gap is small in numbers but decisive in logic: one counterexample rules out every strictly consistent loss for ES alone', 'Diferența este mică numeric, dar decisivă logic: un singur contraexemplu exclude orice pierdere strict consistentă pentru ES singur'),
    T('The way out is to forecast the quantile together with ES: the pair has a convex level set', 'Soluția este prognoza cuantilei împreună cu ES: perechea are mulțimi de nivel convexe')])

D.frame(T('Joint elicitability: the Fissler--Ziegel class', 'Elicitabilitatea comună: clasa Fissler--Ziegel'), items(
    (T(r'\textbf{Theorem} \refFZ, in the form of \refPZC, eq.~(4): for $e \le v$,', r'\textbf{Teoremă} \refFZ, în forma din \refPZC, ec.~(4): pentru $e \le v$,'),
     [r'$S(v, e, y) = (\mathbf 1\{y \le v\} - \alpha)\big(G_1(v) - G_1(y)\big) + G_2(e)\Big(v - e + \tfrac{1}{\alpha}\mathbf 1\{y \le v\}(y - v)\Big) - \mathcal G_2(e)$',
      T(r'is consistent for $(q_\alpha, -\mathrm{ES}_\alpha)$ if $G_1$ is non-decreasing and $\mathcal G_2\' = G_2$ is positive and increasing; strictly so under mild conditions', r'este consistentă pentru $(q_\alpha, -\mathrm{ES}_\alpha)$ dacă $G_1$ este nedescrescătoare și $\mathcal G_2\' = G_2$ este pozitivă și crescătoare; strict consistentă în condiții slabe')]),
    (T(r'Identification function of the pair: $V_1 = \mathbf 1\{y \le v\} - \alpha$, $V_2 = e - v + \tfrac{1}{\alpha}\mathbf 1\{y \le v\}(v - y)$', r'Funcția de identificare a perechii: $V_1 = \mathbf 1\{y \le v\} - \alpha$, $V_2 = e - v + \tfrac{1}{\alpha}\mathbf 1\{y \le v\}(v - y)$'),
     [T(r'$\E V_2 = 0$ at the true quantile is the Acerbi--Tasche formula: ES is the tail mean only together with the right quantile', r'$\E V_2 = 0$ la cuantila corectă este formula Acerbi--Tasche: ES este media cozii doar împreună cu cuantila corectă')]),
    T(r'Consequence \refFZG: ES can be \textbf{compared} through the pair; traditional ES backtests still need more than ES (Section 5)', r'Consecință \refFZG: ES poate fi \textbf{comparat} prin pereche; backtesting-ul clasic al ES cere în continuare mai mult decît ES (secțiunea 5)')), 'small')

D.frame(T('FZ0: the zero-homogeneous member', 'FZ0: membrul omogen de grad zero'), items(
    (T(r'\refPZC, Proposition 1: with $v, e < 0$, loss \textbf{differences} are invariant to rescaling $Y$ iff $G_1 = 0$, $G_2(e) = -1/e$:', r'\refPZC, Propoziția 1: cu $v, e < 0$, \textbf{diferențele} de pierdere sînt invariante la rescalarea lui $Y$ dacă și numai dacă $G_1 = 0$, $G_2(e) = -1/e$:'),
     [r'$L_{\mathrm{FZ0}}(y, v, e; \alpha) = -\dfrac{1}{\alpha e}\mathbf 1\{y \le v\}(v - y) + \dfrac{v}{e} + \ln(-e) - 1$',
      T(r'the VaR part resembles the pinball loss; the ES part resembles QLIKE (Chapter 8)', r'partea de VaR seamănă cu pierderea pinball; partea de ES seamănă cu QLIKE (Capitolul 8)')]),
    (T('Why zero homogeneity matters for time series', 'De ce contează omogenitatea de grad zero pentru serii de timp'),
     [T('with a non-homogeneous score, volatile days dominate the average loss and the DM test (heteroskedastic loss differences)', 'cu un scor neomogen, zilele volatile domină pierderea medie și testul DM (diferențe de pierdere heteroscedastice)'),
      T(r'FZ0 ranks forecasts in \% and in basis points identically; its value can be negative (EUR/RON)', r'FZ0 ordonează la fel prognozele în \% și în puncte de bază; valoarea ei poate fi negativă (EUR/RON)')]),
    T(r'Iso-expected-loss contours are convex under mild conditions, which helps numerical minimisation \refPZC', r'Contururile de pierdere așteptată constantă sînt convexe în condiții slabe, ceea ce ajută minimizarea numerică \refPZC')), 'small')

chart(T('Expected losses around the truth', 'Pierderile așteptate în jurul valorii corecte'), 'ats_ch9_fz0_contour', 'ATS_ch9_scoring', [
    T(r'Student $t(5)$ with unit variance, $\alpha = 0.025$, expectations by simulation ($4\times10^5$ draws): left, expected pinball loss; right, contours of the expected FZ0 loss',
      r'Distribuția Student $t(5)$ cu varianță unitară, $\alpha = 0{,}025$, mediile prin simulare ($4\times10^5$ extrageri): stînga, pierderea pinball așteptată; dreapta, contururile pierderii FZ0 așteptate')],
    h='0.5\\textheight')

interp(('the expected losses', 'pierderilor așteptate'), [
    T(r'The pinball curve is minimal at @{ct.vmin}, the true quantile @{ct.v0}: consistency in action', r'Curba pinball este minimă la @{ct.vmin}, cuantila corectă fiind @{ct.v0}: consistența în acțiune'),
    T(r'The FZ0 surface is minimal at (@{ct.v0}, @{ct.e0}), minimum @{ct.zmin}; contours are convex and elongated', r'Suprafața FZ0 este minimă în (@{ct.v0}; @{ct.e0}), cu minimul @{ct.zmin}; contururile sînt convexe și alungite'),
    T('Both surfaces are flat near the optimum: large forecast differences cost little expected loss, so tests need many tail days', 'Ambele suprafețe sînt plate lîngă optim: diferențe mari între prognoze costă puțin în pierdere așteptată, deci testele cer multe zile din coadă'),
    T('Forecasts with $e > v$ are inadmissible: estimation must enforce the ordering', 'Prognozele cu $e > v$ sînt inadmisibile: estimarea trebuie să impună ordinea')])

D.frame(T('Murphy diagrams: ranking for all consistent scores', 'Diagramele Murphy: ordonarea pentru toate scorurile consistente'), items(
    (T(r'\refEGJK: every GPL quantile score is a mixture of \textbf{elementary scores}', r'\refEGJK: orice scor GPL pentru cuantile este un amestec de \textbf{scoruri elementare}'),
     [r'$S_\theta(x, y) = (\mathbf 1\{y < x\} - \alpha)\big(\mathbf 1\{\theta < x\} - \mathbf 1\{\theta < y\}\big)$, $\quad S(x, y) = \int S_\theta(x, y)\,dH(\theta)$',
      T(r'$S_\theta$ is the loss of a binary decision with threshold $\theta$; $H$ non-decreasing corresponds to $G$', r'$S_\theta$ este pierderea unei decizii binare cu pragul $\theta$; $H$ nedescrescătoare corespunde lui $G$')]),
    (T(r'\textbf{Murphy diagram}: the average $\bar S_\theta$ of each forecast against $\theta$', r'\textbf{Diagrama Murphy}: media $\bar S_\theta$ a fiecărei prognoze în funcție de $\theta$'),
     [T('forecast A dominates B for every consistent score iff its curve is below for all $\\theta$', 'prognoza A domină B pentru orice scor consistent dacă și numai dacă curba ei este dedesubt pentru orice $\\theta$'),
      T('crossing curves: the ranking depends on $G$, i.e.\\ on which thresholds the user cares about', 'curbe care se intersectează: ordonarea depinde de $G$, adică de pragurile care contează pentru utilizator')]),
    T('A check on the pinball ranking that costs one line of code', 'O verificare a ordonării pinball care costă o singură linie de cod')), 'small')

chart(T('A Murphy diagram for VaR 2.5\\%', 'O diagramă Murphy pentru VaR 2,5\\%'), 'ats_ch9_murphy', 'ATS_ch9_scoring', [
    T(r'S\&P 500, out of sample 2000--2016 (PZC design); mean elementary scores of three VaR 2.5\% forecasts against the threshold $\theta$',
      r'S\&P 500, în afara eșantionului 2000--2016 (designul PZC); scorurile elementare medii ale celor trei prognoze VaR 2,5\% în funcție de pragul $\theta$')],
    h='0.5\\textheight')

interp(('the Murphy diagram', 'diagramei Murphy'), [
    T(r'GARCH-EDF lies below RW-250 at @{mu.edf}\% of the thresholds: the dynamic forecast dominates almost uniformly', r'GARCH-EDF este sub RW-250 la @{mu.edf}\% din praguri: prognoza dinamică domină aproape uniform'),
    T(r'GAS-1F and GARCH-EDF cross: GAS-1F is better at only @{mu.fz}\% of the thresholds; average pinball @{mu.pin.fz1f} and @{mu.pin.gchedf} ($\times 10^{-2}$)', r'GAS-1F și GARCH-EDF se intersectează: GAS-1F este mai bun doar la @{mu.fz}\% din praguri; pinball mediu @{mu.pin.fz1f} și @{mu.pin.gchedf} ($\times 10^{-2}$)'),
    T('The two good models differ in deep thresholds (below $-4\\%$), where data are scarce', 'Cele două modele bune diferă la pragurile adînci (sub $-4\\%$), unde datele sînt puține'),
    T('A claim that ``model A is better\'\' should say for which scores; the diagram answers it', 'O afirmație de tipul „modelul A este mai bun” trebuie să precizeze pentru ce scoruri; diagrama răspunde')])

D.recap(('Elicitability', 'elicitabilitate'), [
    T('Scores compare, identification functions test; both come from the same theory', 'Scorurile compară, funcțiile de identificare testează; ambele provin din aceeași teorie'),
    T('Quantiles: GPL scores; ES: not alone; (VaR, ES): the Fissler--Ziegel class', 'Cuantilele: scoruri GPL; ES: nu singur; (VaR, ES): clasa Fissler--Ziegel'),
    T('FZ0 is scale-free; Murphy diagrams check rankings for all consistent scores', 'FZ0 nu depinde de scală; diagramele Murphy verifică ordonarea pentru toate scorurile consistente')])

# =============================================================================
# 3. REGRESIA CUANTILICĂ ȘI CAViaR
# =============================================================================
D.section('Quantile regression and CAViaR', 'Regresia cuantilică și CAViaR')

D.frame(T('Quantile regression as M-estimation', 'Regresia cuantilică ca M-estimare'), two(
    ph('koenker', T('Roger Koenker, Oberwolfach, 2012', 'Roger Koenker, Oberwolfach, 2012'), h='0.26\\textheight'),
    items((T(r'\refKB: $\hat\beta(\alpha) = \arg\min_\beta \sum_t \rho_\alpha(y_t - x_t\'\beta)$, a linear program', r'\refKB: $\hat\beta(\alpha) = \arg\min_\beta \sum_t \rho_\alpha(y_t - x_t\'\beta)$, o problemă de programare liniară'),
           [T(r'first-order condition: $\sum_t x_t(\mathbf 1\{y_t \le x_t\'\hat\beta\} - \alpha) \approx 0$, the identification function', r'condiția de ordinul întîi: $\sum_t x_t(\mathbf 1\{y_t \le x_t\'\hat\beta\} - \alpha) \approx 0$, funcția de identificare')]),
          (T(r'$\sqrt T(\hat\beta - \beta) \to N\big(0, \alpha(1 - \alpha)D^{-1}\Omega D^{-1}\big)$, $\Omega = \E[x_tx_t\']$, $D = \E[f_t(q_t)x_tx_t\']$ \refKoe', r'$\sqrt T(\hat\beta - \beta) \to N\big(0, \alpha(1 - \alpha)D^{-1}\Omega D^{-1}\big)$, $\Omega = \E[x_tx_t\']$, $D = \E[f_t(q_t)x_tx_t\']$ \refKoe'),
           [T(r'the conditional density at the quantile (the ``sparsity\'\') enters $D$: estimate it with a kernel and a bandwidth', r'densitatea condiționată în cuantilă (inversul „sparsity”) intră în $D$: se estimează cu un nucleu și o lățime de bandă')]),
          T(r'Time series: quantile autoregression \refKX\ lets AR coefficients vary across quantiles; CAViaR makes the quantile itself autoregressive',
            r'Serii de timp: autoregresia cuantilică \refKX\ permite coeficienților AR să varieze între cuantile; CAViaR face cuantila însăși autoregresivă')), '0.27', '0.71'), 'small')

D.frame(T('CAViaR: the four specifications', 'CAViaR: cele patru specificații'), two(
    ph('engle', T('Robert Engle, 2022', 'Robert Engle, 2022'), h='0.38\\textheight'),
    items(T(r'\refEM, written for $\mathrm{VaR}_t = -q_t(\alpha) > 0$:', r'\refEM, scrise pentru $\mathrm{VaR}_t = -q_t(\alpha) > 0$:'),
          T(r'\textbf{SAV}: $\mathrm{VaR}_t = \beta_1 + \beta_2\mathrm{VaR}_{t-1} + \beta_3|y_{t-1}|$', r'\textbf{SAV}: $\mathrm{VaR}_t = \beta_1 + \beta_2\mathrm{VaR}_{t-1} + \beta_3|y_{t-1}|$'),
          T(r'\textbf{AS}: $\mathrm{VaR}_t = \beta_1 + \beta_2\mathrm{VaR}_{t-1} + \beta_3(y_{t-1})^+ + \beta_4(y_{t-1})^-$', r'\textbf{AS}: $\mathrm{VaR}_t = \beta_1 + \beta_2\mathrm{VaR}_{t-1} + \beta_3(y_{t-1})^+ + \beta_4(y_{t-1})^-$'),
          T(r'\textbf{IG}: $\mathrm{VaR}_t = (\beta_1 + \beta_2\mathrm{VaR}_{t-1}^2 + \beta_3y_{t-1}^2)^{1/2}$ (a GARCH(1,1) with i.i.d.\ innovations)', r'\textbf{IG}: $\mathrm{VaR}_t = (\beta_1 + \beta_2\mathrm{VaR}_{t-1}^2 + \beta_3y_{t-1}^2)^{1/2}$ (un GARCH(1,1) cu inovații i.i.d.)'),
          T(r'\textbf{Adaptive}: $\mathrm{VaR}_t = \mathrm{VaR}_{t-1} + \beta_1\big([1 + e^{G(y_{t-1} + \mathrm{VaR}_{t-1})}]^{-1} - \alpha\big)$, $G = 10$: raise after a hit, lower slowly otherwise', r'\textbf{Adaptiv}: $\mathrm{VaR}_t = \mathrm{VaR}_{t-1} + \beta_1\big([1 + e^{G(y_{t-1} + \mathrm{VaR}_{t-1})}]^{-1} - \alpha\big)$, $G = 10$: crește după o depășire, scade lent în rest'),
          T(r'$\beta_2$ is the persistence of the tail; no distribution is assumed', r'$\beta_2$ este persistența cozii; nu se presupune nicio distribuție')), '0.3', '0.68'), 'small')

D.frame(T('Estimation and inference', 'Estimare și inferență'), items(
    (T(r'Regression-quantile criterion: $\hat\beta = \arg\min_\beta T^{-1}\sum_t \rho_\alpha\big(y_t + \mathrm{VaR}_t(\beta)\big)$; non-differentiable and non-convex in $\beta$', r'Criteriul de regresie cuantilică: $\hat\beta = \arg\min_\beta T^{-1}\sum_t \rho_\alpha\big(y_t + \mathrm{VaR}_t(\beta)\big)$; nediferențiabil și neconvex în $\beta$'),
     [T(r'EM procedure (empirical section): $\mathrm{VaR}_1$ = the empirical quantile of the first 300 days; $10^4$ random vectors, the 10 best refined by alternating simplex and quasi-Newton steps',
        r'Procedura EM (secțiunea empirică): $\mathrm{VaR}_1$ = cuantila empirică din primele 300 de zile; $10^4$ vectori aleatori, cei mai buni 10 rafinați alternînd pași simplex și cvasi-Newton')]),
    (T(r'Consistency and $\sqrt T(\hat\beta - \beta) \to N(0, \alpha(1 - \alpha)D^{-1}AD^{-1})$, $A = \E[\nabla q_t\nabla q_t\']$, $D = \E[f_t(q_t)\nabla q_t\nabla q_t\']$', r'Consistență și $\sqrt T(\hat\beta - \beta) \to N(0, \alpha(1 - \alpha)D^{-1}AD^{-1})$, $A = \E[\nabla q_t\nabla q_t\']$, $D = \E[f_t(q_t)\nabla q_t\nabla q_t\']$'),
     [T(r'$\hat D = (2T\hat c)^{-1}\sum_t\mathbf 1\{|y_t - \hat q_t| < \hat c\}\nabla\hat q_t\nabla\hat q_t\'$; we take $\hat c$ from the Hall--Sheather rule on the residual scale \refKoe', r'$\hat D = (2T\hat c)^{-1}\sum_t\mathbf 1\{|y_t - \hat q_t| < \hat c\}\nabla\hat q_t\nabla\hat q_t\'$; luăm $\hat c$ din regula Hall--Sheather pe scala reziduurilor \refKoe')]),
    T(r'Gradients $\nabla q_t$ follow their own recursion (or numerical differentiation of the path): the dynamic model is a recursive M-estimator',
      r'Gradienții $\nabla q_t$ urmează propria recursie (sau derivarea numerică a traiectoriei): modelul dinamic este un M-estimator recursiv')), 'small')

D.frame(T('The dynamic quantile (DQ) test', 'Testul dinamic pe cuantile (DQ)'), items(
    (T(r'$\mathrm{Hit}_t = \mathbf 1\{y_t < q_t\} - \alpha$: under correct specification a martingale difference, $\E[\mathrm{Hit}_t \mid \mathcal F_{t-1}] = 0$', r'$\mathrm{Hit}_t = \mathbf 1\{y_t < q_t\} - \alpha$: sub specificarea corectă este o diferență de martingală, $\E[\mathrm{Hit}_t \mid \mathcal F_{t-1}] = 0$'),
     [T(r'regress $\mathrm{Hit}_t$ on $X_t$ = (1, $\mathrm{Hit}_{t-1}, \dots, \mathrm{Hit}_{t-4}$, $q_t$), all in $\mathcal F_{t-1}$ \refEM', r'regresăm $\mathrm{Hit}_t$ pe $X_t$ = (1, $\mathrm{Hit}_{t-1}, \dots, \mathrm{Hit}_{t-4}$, $q_t$), toate din $\mathcal F_{t-1}$ \refEM')]),
    (T(r'Out of sample: $\mathrm{DQ} = \dfrac{\mathrm{Hit}\'X(X\'X)^{-1}X\'\mathrm{Hit}}{\alpha(1 - \alpha)} \to \chi^2_6$', r'În afara eșantionului: $\mathrm{DQ} = \dfrac{\mathrm{Hit}\'X(X\'X)^{-1}X\'\mathrm{Hit}}{\alpha(1 - \alpha)} \to \chi^2_6$'),
     [T('in sample the estimated $\\beta$ makes the hits orthogonal to the gradients: the covariance needs the correction derived by EM', 'în eșantion, $\\beta$ estimat face depășirile ortogonale pe gradienți: covarianța cere corecția derivată de EM')]),
    T('Kupiec (constant only) and Christoffersen (one lagged hit) are special cases; the VaR regressor adds power against level-dependent misspecification',
      'Testele Kupiec (doar constanta) și Christoffersen (o depășire întîrziată) sînt cazuri particulare; regresorul VaR adaugă putere împotriva erorilor care depind de nivel'),
    T('With $\\alpha = 1\\%$ and a few hundred days the $\\chi^2$ approximation is poor (Section 5): report simulated or exact $p$-values when possible',
      'Cu $\\alpha = 1\\%$ și cîteva sute de zile, aproximarea $\\chi^2$ este slabă (secțiunea 5): raportați valori $p$ simulate sau exacte cînd se poate')), 'small')

D.frame(T('Case study: Engle and Manganelli (2004) on today\'s data', 'Studiu de caz: Engle și Manganelli (2004) pe datele de azi'), items(
    (T('The design of the empirical section of EM: 3,392 daily returns, the first 2,892 for estimation, the last 500 out of sample; VaR 1\\% and 5\\%', 'Designul din secțiunea empirică a lucrării EM: 3\\,392 de randamente zilnice, primele 2\\,892 pentru estimare, ultimele 500 în afara eșantionului; VaR 1\\% și 5\\%'),
     [T(r'EM used 1986--1999 (GM, IBM, S\&P 500); we use the S\&P 500 from @{cv.d0} to @{cv.d3}, out of sample from @{cv.d2}', r'EM au folosit 1986--1999 (GM, IBM, S\&P 500); noi folosim S\&P 500 de la @{cv.d0} la @{cv.d3}, în afara eșantionului din @{cv.d2}')]),
    (T('Same specifications, starting values and search; the April 2025 tariff shock falls in the out-of-sample period', 'Aceleași specificații, valori de pornire și căutare; șocul tarifelor din aprilie 2025 cade în perioada din afara eșantionului'), []),
    T('Questions: which specification fits the 1\\% tail, are the forecasts calibrated out of sample, and is the response to bad news asymmetric?',
      'Întrebări: ce specificație descrie coada de 1\\%, sînt prognozele calibrate în afara eșantionului și este răspunsul la veștile proaste asimetric?')), 'small')

chart(T('CAViaR VaR 1\\% of the S\\&P 500', 'VaR 1\\% CAViaR pentru S\\&P 500'), 'ats_ch9_caviar', 'ATS_ch9_caviar', [
    T(r'The last year of the estimation sample and the 500 out-of-sample days; lines: the 1\% return quantile $q_t = -\mathrm{VaR}_t$ of the four specifications',
      r'Ultimul an al eșantionului de estimare și cele 500 de zile din afara lui; liniile: cuantila de 1\% a randamentelor $q_t = -\mathrm{VaR}_t$ pentru cele patru specificații')],
    h='0.5\\textheight')

D.frame(T('Estimates, standard errors and DQ tests', 'Estimații, erori standard și teste DQ'), table(
    'lccccc' + TB + 'p{1.25cm}' + TB + 'p{1.35cm}' + TB + 'p{1.5cm}', T(r'\textbf{Model}', r'\textbf{Modelul}') + r' & $\beta_1$ & $\beta_2$ & $\beta_3$ & $\beta_4$ & RQ$\times10^2$ & ' + T(r'hits in sample (\%)', r'depășiri în eșantion (\%)') + ' & ' + T(r'hits out of sample (\%)', r'depășiri în afara eșantionului (\%)') + ' & ' + T('DQ out of sample ($p$)', 'DQ în afara eșantionului ($p$)'),
    [r'SAV & @{cv.SAV.b0} (@{cv.SAV.s0}) & @{cv.SAV.b1} (@{cv.SAV.s1}) & @{cv.SAV.b2} (@{cv.SAV.s2}) & -- & @{cv.SAV.rq} & @{cv.SAV.hi} & @{cv.SAV.ho} & @{cv.SAV.dq} (@{cv.SAV.dqp})',
     r'AS & @{cv.AS.b0} (@{cv.AS.s0}) & @{cv.AS.b1} (@{cv.AS.s1}) & @{cv.AS.b2} (@{cv.AS.s2}) & @{cv.AS.b3} (@{cv.AS.s3}) & @{cv.AS.rq} & @{cv.AS.hi} & @{cv.AS.ho} & @{cv.AS.dq} (@{cv.AS.dqp})',
     r'IG & @{cv.IG.b0} (@{cv.IG.s0}) & @{cv.IG.b1} (@{cv.IG.s1}) & @{cv.IG.b2} (@{cv.IG.s2}) & -- & @{cv.IG.rq} & @{cv.IG.hi} & @{cv.IG.ho} & @{cv.IG.dq} (@{cv.IG.dqp})',
     r'ADAPT & @{cv.ADAPT.b0} (@{cv.ADAPT.s0}) & -- & -- & -- & @{cv.ADAPT.rq} & @{cv.ADAPT.hi} & @{cv.ADAPT.ho} & @{cv.ADAPT.dq} (@{cv.ADAPT.dqp})'],
    size='tiny') + items(
    T(r'Standard errors from the asymptotic covariance of EM; RQ: the minimised in-sample criterion; DQ out of sample with four lagged hits and the VaR, $\chi^2_6$; 500 days give 5 expected hits',
      r'Erorile standard din covarianța asimptotică EM; RQ: criteriul minimizat în eșantion; DQ în afara eșantionului cu patru depășiri întîrziate și VaR, $\chi^2_6$; 500 de zile dau 5 depășiri așteptate'),
    T(r'Out-of-sample average pinball loss ($\times10^2$): SAV @{cv.SAV.pin}, AS @{cv.AS.pin}, IG @{cv.IG.pin}, adaptive @{cv.ADAPT.pin}', r'Pierderea pinball medie în afara eșantionului ($\times10^2$): SAV @{cv.SAV.pin}, AS @{cv.AS.pin}, IG @{cv.IG.pin}, adaptiv @{cv.ADAPT.pin}')), 'footnotesize')

interp(('the CAViaR estimates', 'estimațiilor CAViaR'), [
    T(r'All three autoregressive models fit the in-sample rate (about 1\%) by construction: the quantile loss calibrates the level', r'Toate cele trei modele autoregresive reproduc rata din eșantion (circa 1\%) prin construcție: pierderea cuantilică calibrează nivelul'),
    T(r'AS: a negative return moves VaR about @{nic.ratio} times more than a positive one of the same size; $\beta_3$ is not distinguishable from zero', r'AS: un randament negativ mută VaR de circa @{nic.ratio} ori mai mult decît unul pozitiv de aceeași mărime; $\beta_3$ nu se deosebește de zero'),
    T(r'Out of sample IG passes DQ ($p$ = @{cv.IG.dqp}); SAV ($p$ = @{cv.SAV.dqp}) and AS ($p$ = @{cv.AS.dqp}) are rejected at 5\%, the adaptive model clearly ($p$ @{cv.ADAPT.dqp})', r'În afara eșantionului IG trece testul DQ ($p$ = @{cv.IG.dqp}); SAV ($p$ = @{cv.SAV.dqp}) și AS ($p$ = @{cv.AS.dqp}) sînt respinse la 5\%, modelul adaptiv clar ($p$ @{cv.ADAPT.dqp})'),
    T('Five expected hits in 500 days: rejections come from clustered hits in April 2025, not from the count; such evidence is fragile', 'Cinci depășiri așteptate în 500 de zile: respingerile vin din depășirile grupate din aprilie 2025, nu din numărul lor; o astfel de evidență este fragilă'),
    T('The adaptive model reacts only to hits, like a slow thermostat: after the April 2025 cluster it stays too high for months', 'Modelul adaptiv reacționează doar la depășiri, ca un termostat lent: după grupul de depășiri din aprilie 2025 rămîne prea sus timp de luni de zile')])

chart(T('News impact curves', 'Curbele de impact al știrilor'), 'ats_ch9_nic', 'ATS_ch9_caviar', [
    T(r'$\mathrm{VaR}_t$ as a function of $y_{t-1}$, with $\mathrm{VaR}_{t-1}$ at its in-sample median (@{nic.med}\% for AS); estimated parameters of the table',
      r'$\mathrm{VaR}_t$ în funcție de $y_{t-1}$, cu $\mathrm{VaR}_{t-1}$ la mediana din eșantion (@{nic.med}\% pentru AS); parametrii estimați din tabel')],
    h='0.5\\textheight')

interp(('the news impact curves', 'curbelor de impact'), [
    T('SAV and IG are symmetric by design: a 5\\% rally raises the 1\\% VaR as much as a 5\\% fall', 'SAV și IG sînt simetrice prin construcție: o creștere de 5\\% ridică VaR 1\\% la fel de mult ca o cădere de 5\\%'),
    T('AS is almost flat for gains and steep for losses: the leverage effect estimated directly in the tail', 'AS este aproape plat pentru cîștiguri și abrupt pentru pierderi: efectul de levier estimat direct în coadă'),
    T('The adaptive curve is a step: only the sign of the hit matters, not its size', 'Curba adaptivă este o treaptă: contează doar semnul depășirii, nu mărimea ei'),
    T('The shape of the curve is a testable restriction: AS nests SAV ($\\beta_3 = \\beta_4$), a Wald test with the asymptotic covariance of EM', 'Forma curbei este o restricție testabilă: AS include SAV ($\\beta_3 = \\beta_4$), un test Wald cu covarianța asimptotică EM')])

D.recap(('CAViaR', 'CAViaR'), [
    T('Quantile regression is M-estimation with the pinball loss; its covariance needs the density at the quantile', 'Regresia cuantilică este M-estimare cu pierderea pinball; covarianța ei cere densitatea în cuantilă'),
    T('CAViaR makes the quantile autoregressive; estimation needs many starts', 'CAViaR face cuantila autoregresivă; estimarea cere multe puncte de pornire'),
    T('DQ tests hits against information; the asymmetric model fits equity tails', 'DQ testează depășirile față de informație; modelul asimetric descrie coada acțiunilor')])

# =============================================================================
# 4. MODELE COMUNE (VaR, ES)
# =============================================================================
D.section('Semiparametric models for (VaR, ES)', 'Modele semiparametrice pentru (VaR, ES)')

D.frame(T('M-estimation with the FZ0 loss', 'M-estimarea cu pierderea FZ0'), items(
    (T(r'Model $(v_t, e_t) = (v, e)(\mathcal F_{t-1}; \theta)$; estimator $\hat\theta = \arg\min_\theta T^{-1}\sum_t L_{\mathrm{FZ0}}(y_t, v_t(\theta), e_t(\theta); \alpha)$ \refPZC', r'Modelul $(v_t, e_t) = (v, e)(\mathcal F_{t-1}; \theta)$; estimatorul $\hat\theta = \arg\min_\theta T^{-1}\sum_t L_{\mathrm{FZ0}}(y_t, v_t(\theta), e_t(\theta); \alpha)$ \refPZC'),
     [T('consistency follows from the strict consistency of FZ0 and identification of $\\theta$; asymptotic normality as for CAViaR, with a sandwich covariance', 'consistența rezultă din consistența strictă a FZ0 și din identificarea lui $\\theta$; normalitatea asimptotică ca la CAViaR, cu o covarianță de tip sandwich')]),
    (T('Why not maximum likelihood?', 'De ce nu verosimilitate maximă?'),
     [T('MLE needs the whole distribution; a wrong body or right tail distorts the left tail estimates', 'Verosimilitatea maximă cere întreaga distribuție; un corp sau o coadă dreaptă greșite distorsionează estimațiile cozii stîngi'),
      T('FZ estimation targets exactly the two tail functionals: less efficient if the model is right, robust if it is not (PZC, Tables 3--4)', 'Estimarea FZ țintește exact cele două funcționale de coadă: mai puțin eficientă dacă modelul este corect, robustă dacă nu este (PZC, Tabelele 3--4)')]),
    T(r'Related: the asymmetric Laplace quasi-likelihood \refTayB; ES regressions \refDB; score-driven (GAS) dynamics \refCKL', r'Înrudite: cvasi-verosimilitatea Laplace asimetrică \refTayB; regresiile pentru ES \refDB; dinamica determinată de scor (GAS) \refCKL')), 'small')

D.frame(T('The two-factor GAS model', 'Modelul GAS cu doi factori'), items(
    (T(r'\refPZC, eq.~(9)--(16): $\begin{pmatrix} v_{t+1} \\ e_{t+1}\end{pmatrix} = w + B\begin{pmatrix} v_t \\ e_t\end{pmatrix} + A\lambda_t$, $B$ diagonal, $A$ a $2\times2$ matrix', r'\refPZC, ec.~(9)--(16): $\begin{pmatrix} v_{t+1} \\ e_{t+1}\end{pmatrix} = w + B\begin{pmatrix} v_t \\ e_t\end{pmatrix} + A\lambda_t$, $B$ diagonală, $A$ o matrice $2\times2$'),
     [T(r'forcing variables from the FZ0 score: $\lambda_{v,t} = -v_t(\mathbf 1\{y_t \le v_t\} - \alpha)$, $\lambda_{e,t} = \tfrac{1}{\alpha}\mathbf 1\{y_t \le v_t\}y_t - e_t$', r'variabilele de impuls din scorul FZ0: $\lambda_{v,t} = -v_t(\mathbf 1\{y_t \le v_t\} - \alpha)$, $\lambda_{e,t} = \tfrac{1}{\alpha}\mathbf 1\{y_t \le v_t\}y_t - e_t$'),
      T(r'both are identification functions: zero conditional mean under correct specification', r'ambele sînt funcții de identificare: medie condiționată nulă sub specificarea corectă')]),
    (T(r'The Hessian is scaled with $f_t(v_t) \approx k_\alpha/v_t$ (exact for location--scale returns), so no density is estimated', r'Hessiana se scalează cu $f_t(v_t) \approx k_\alpha/v_t$ (exact pentru randamente de tip poziție--scală), deci nu se estimează nicio densitate'), []),
    T('Eight parameters; on non-hit days $\\lambda_{e,t} = -e_t$ and both risk measures decay deterministically towards their means', 'Opt parametri; în zilele fără depășire $\\lambda_{e,t} = -e_t$, iar ambele măsuri de risc scad determinist spre mediile lor')), 'small')

D.frame(T('One-factor, GARCH-FZ and Hybrid models', 'Modelele cu un factor, GARCH-FZ și Hybrid'), items(
    (T(r'\textbf{GAS-1F}, eq.~(20): $v_t = a e^{\kappa_t}$, $e_t = b e^{\kappa_t}$, $b < a < 0$, $\kappa_t = \beta\kappa_{t-1} + \gamma\,\dfrac{-1}{e_{t-1}}\Big(\tfrac{1}{\alpha}\mathbf 1\{y_{t-1} \le v_{t-1}\}y_{t-1} - e_{t-1}\Big)$', r'\textbf{GAS-1F}, ec.~(20): $v_t = a e^{\kappa_t}$, $e_t = b e^{\kappa_t}$, $b < a < 0$, $\kappa_t = \beta\kappa_{t-1} + \gamma\,\dfrac{-1}{e_{t-1}}\Big(\tfrac{1}{\alpha}\mathbf 1\{y_{t-1} \le v_{t-1}\}y_{t-1} - e_{t-1}\Big)$'),
     [T(r'one latent log-scale; the intercept $\omega$ is not identified with $(a, b)$ and is fixed at 0', r'o singură log-scală latentă; termenul liber $\omega$ nu este identificat împreună cu $(a, b)$ și se fixează la 0')]),
    (T(r'\textbf{GARCH-FZ}, eq.~(25)--(26): $\kappa_t^2 = 1 + \beta\kappa_{t-1}^2 + \gamma y_{t-1}^2$, $(v_t, e_t) = (a, b)\kappa_t$: a GARCH tuned to the tail', r'\textbf{GARCH-FZ}, ec.~(25)--(26): $\kappa_t^2 = 1 + \beta\kappa_{t-1}^2 + \gamma y_{t-1}^2$, $(v_t, e_t) = (a, b)\kappa_t$: un GARCH ajustat pentru coadă'), []),
    (T(r'\textbf{Hybrid}, eq.~(27): GAS-1F plus $\delta\ln|y_{t-1}|$: reacts every day, more strongly on hit days', r'\textbf{Hybrid}, ec.~(27): GAS-1F plus $\delta\ln|y_{t-1}|$: reacționează în fiecare zi, mai puternic în zilele cu depășiri'), []),
    T(r'In all three the ratio $e_t/v_t = b/a$ is constant: the shape of the tail is fixed, only its scale moves', r'În toate trei raportul $e_t/v_t = b/a$ este constant: forma cozii este fixă, doar scala ei se mișcă')), 'small')

D.frame(T('Estimating non-smooth recursive models', 'Estimarea modelelor recursive nenetede'), items(
    (T(r'The FZ0 objective is discontinuous in $\theta$ (through $\mathbf 1\{y_t \le v_t(\theta)\}$) and the recursion propagates every jump', r'Funcția obiectiv FZ0 este discontinuă în $\theta$ (prin $\mathbf 1\{y_t \le v_t(\theta)\}$), iar recursia propagă fiecare salt'), []),
    (T(r'Appendix C of the paper \refPZC: replace the indicator by $\Gamma(y, v; \tau) = [1 + e^{\tau(y - v)}]^{-1}$ in the loss and in the forcing variable', r'Anexa C a lucrării \refPZC: înlocuim indicatorul cu $\Gamma(y, v; \tau) = [1 + e^{\tau(y - v)}]^{-1}$ în pierdere și în variabila de impuls'),
     [T(r'quasi-Newton with $\tau = 5$, then $\tau = 20$, then the exact loss with the simplex method, each step starting from the previous one', r'cvasi-Newton cu $\tau = 5$, apoi $\tau = 20$, apoi pierderea exactă cu metoda simplex, fiecare pas pornind din cel anterior')]),
    (T('Our starting values: random dynamic parameters with $(a, b)$ matched to the in-sample VaR and ES; the four best are refined', 'Valorile noastre de pornire: parametri dinamici aleatori, cu $(a, b)$ potriviți la VaR și ES din eșantion; cei mai buni patru sînt rafinați'), []),
    T('Constraints enforced by penalty: $e_t \\le v_t$, $e_t < 0$, stationarity of the recursion', 'Restricții impuse prin penalizare: $e_t \\le v_t$, $e_t < 0$, staționaritatea recursiei')), 'small')

D.frame(T('Case study: Patton, Ziegel and Chen (2019), Section 5', 'Studiu de caz: Patton, Ziegel și Chen (2019), secțiunea 5'), items(
    (T(r'Data: daily S\&P 500 returns, January 1990 -- December 2016; estimation on the first ten years, parameters kept fixed for 2000--2016 ($T = @{pz.T}$)', r'Date: randamentele zilnice ale S\&P 500, ianuarie 1990 -- decembrie 2016; estimare pe primii zece ani, parametrii păstrați ficși pentru 2000--2016 ($T = @{pz.T}$)'),
     []),
    (T('Ten models, as in the paper', 'Zece modele, ca în lucrare'),
     [T('rolling windows of 125, 250 and 500 days (RW); ARMA (order by BIC) -- GARCH(1,1) with Normal, skewed-t or empirical innovations', 'ferestre mobile de 125, 250 și 500 de zile (RW); ARMA (ordinul după BIC) -- GARCH(1,1) cu inovații din distribuția Normală, t asimetrică sau empirice'),
      T('GAS-2F, GAS-1F, GARCH-FZ and Hybrid estimated by FZ0 minimisation', 'GAS-2F, GAS-1F, GARCH-FZ și Hybrid estimate prin minimizarea FZ0')]),
    (T(r'Outputs replicated: average out-of-sample FZ0 losses (Table 8, $\alpha$ = 5\%; Table S5, $\alpha$ = 2.5\%), DM statistics (Table 9), goodness-of-fit tests (eq.~41)', r'Rezultate replicate: pierderile FZ0 medii în afara eșantionului (Tabelul 8, $\alpha$ = 5\%; Tabelul S5, $\alpha$ = 2,5\%), statisticile DM (Tabelul 9), testele de adecvare (ec.~41)'), []),
    T('Our data: EODHD closes of the same index; differences of a few thousandths are expected from data revisions and optimiser paths', 'Datele noastre: închiderile EODHD ale aceluiași indice; diferențe de cîteva miimi sînt de așteptat din revizuiri ale datelor și din traseele optimizatorului')), 'small')

chart(T('Three ways to forecast the tail', 'Trei moduri de a prognoza coada'), 'ats_ch9_pzc_paths', 'ATS_ch9_pzc', [
    T(r'VaR and ES 5\% of the S\&P 500 in 2015--2016 (PZC, Figure 5 on our data): RW-125, GARCH-EDF and GAS-1F',
      r'VaR și ES 5\% pentru S\&P 500 în 2015--2016 (PZC, Figura 5 pe datele noastre): RW-125, GARCH-EDF și GAS-1F')],
    h='0.5\\textheight')

interp(('the three forecasts', 'celor trei prognoze'), [
    T('The rolling window moves in steps as extreme days enter and leave the window, months after the shock', 'Fereastra mobilă se mișcă în trepte, pe măsură ce zilele extreme intră și ies din fereastră, la luni după șoc'),
    T('GARCH-EDF moves every day with squared returns; GAS-1F moves only on hit days and then decays smoothly', 'GARCH-EDF se mișcă în fiecare zi cu pătratele randamentelor; GAS-1F se mișcă doar în zilele cu depășiri și apoi scade lin'),
    T(r'August 2015: GARCH reacts most, GAS-1F jumps less but stays; in 2008 the GAS-1F ES 5\% reached @{pz.min}\%', r'August 2015: GARCH reacționează cel mai mult, GAS-1F sare mai puțin, dar rămîne; în 2008, ES 5\% GAS-1F a ajuns la @{pz.min}\%'),
    T('Which reaction is right is decided by the FZ0 loss, not by the look of the path', 'Ce reacție este corectă decide pierderea FZ0, nu aspectul traiectoriei')])

chart(T('Replication: average out-of-sample FZ0 loss', 'Replicare: pierderea FZ0 medie în afara eșantionului'), 'ats_ch9_pzc_table', 'ATS_ch9_pzc', [
    T(r'Bars: our data and code, same design; diamonds: the values printed in PZC, Table 8 ($\alpha$ = 5\%) and Table S5 ($\alpha$ = 2.5\%)',
      r'Bare: datele și codul nostru, același design; romburi: valorile tipărite în PZC, Tabelul 8 ($\alpha$ = 5\%) și Tabelul S5 ($\alpha$ = 2,5\%)')],
    h='0.5\\textheight')

D.frame(T('Replication in numbers', 'Replicarea în cifre'), table(
    'lcccccc', T(r'\textbf{Model}', r'\textbf{Modelul}') + r' & \multicolumn{2}{c}{$\alpha = 5\%$} & \multicolumn{2}{c}{$\alpha = 2.5\%$} & \multicolumn{2}{c}{GoF $p$, $\alpha = 5\%$} \\ & ' + T('ours', 'noi') + ' & PZC & ' + T('ours', 'noi') + ' & PZC & VaR & ES',
    [f'{m} & @{{pz5.{MK[m]}}} & @{{pp5.{MK[m]}}} & @{{pz25.{MK[m]}}} & @{{pp25.{MK[m]}}} & @{{pg5.{MK[m]}.v}} & @{{pg5.{MK[m]}.e}}' for m in MODELS],
    size='scriptsize') + items(
    T(r'Largest gap: @{pz5.dev} at 5\%, @{pz25.dev} at 2.5\%; BIC picks @{pz.order} for the mean (PZC: ARMA(1,1)); GARCH $\alpha$ = @{pz.alpha}, $\beta$ = @{pz.beta}',
      r'Cea mai mare diferență: @{pz5.dev} la 5\%, @{pz25.dev} la 2,5\%; BIC alege @{pz.order} pentru medie (PZC: ARMA(1,1)); GARCH $\alpha$ = @{pz.alpha}, $\beta$ = @{pz.beta}')), 'footnotesize')

interp(('the replication', 'replicării'), [
    T(r'The ranking of the paper is reproduced: GAS-1F lowest at 5\% (@{pz5.fz1f}, paper @{pp5.fz1f}), RW-500 worst, GARCH-N behind the other GARCH models', r'Ordonarea din lucrare se reproduce: GAS-1F cel mai mic la 5\% (@{pz5.fz1f}, lucrarea @{pp5.fz1f}), RW-500 cel mai slab, GARCH-N în urma celorlalte modele GARCH'),
    T(r'GAS-1F estimates: $\beta$ = @{pz.f1.b}, $\gamma$ = @{pz.f1.g} (PZC, Table 7: 0.990 and $-0.010$); Hybrid $\delta$ = @{pz.hy.d} (0.018)', r'Estimațiile GAS-1F: $\beta$ = @{pz.f1.b}, $\gamma$ = @{pz.f1.g} (PZC, Tabelul 7: 0,990 și $-0{,}010$); Hybrid $\delta$ = @{pz.hy.d} (0,018)'),
    T(r'Not reproduced: the goodness-of-fit tests; PZC find GAS-1F passing ($p$ 0.242 and 0.313), on our data it is rejected (@{pg5.fz1f.v}; @{pg5.fz1f.e})', r'Nereprodus: testele de adecvare; PZC găsesc că GAS-1F trece ($p$ 0,242 și 0,313), pe datele noastre este respins (@{pg5.fz1f.v}; @{pg5.fz1f.e})'),
    T('Average losses are robust to small data differences; tests on a handful of tail days are not, and the covariance choice of the regression matters', 'Pierderile medii sînt robuste la mici diferențe ale datelor; testele pe cîteva zile din coadă nu sînt, iar alegerea covarianței regresiei contează')])

chart(T('Diebold--Mariano tests on FZ0 losses', 'Teste Diebold--Mariano pe pierderile FZ0'), 'ats_ch9_dm', 'ATS_ch9_pzc', [
    T(r'S\&P 500, 2000--2016, $\alpha$ = 5\%: DM statistic of row minus column, Newey--West variance; red: the row model is worse (PZC, Table 9)',
      r'S\&P 500, 2000--2016, $\alpha$ = 5\%: statistica DM a rîndului minus coloana, varianță Newey--West; roșu: modelul de pe rînd este mai slab (PZC, Tabelul 9)')],
    h='0.56\\textheight')

interp(('the DM matrix', 'matricei DM'), [
    T(r'Column GAS-1F, ours against PZC: RW-125 @{dm.rw125} (@{dmp.rw125}), RW-500 @{dm.rw500} (@{dmp.rw500}), GARCH-N @{dm.gchn} (@{dmp.gchn}), GARCH-EDF @{dm.gchedf} (@{dmp.gchedf})', r'Coloana GAS-1F, noi față de PZC: RW-125 @{dm.rw125} (@{dmp.rw125}), RW-500 @{dm.rw500} (@{dmp.rw500}), GARCH-N @{dm.gchn} (@{dmp.gchn}), GARCH-EDF @{dm.gchedf} (@{dmp.gchedf})'),
    T('The worst models are easily separated; the best few are not (GARCH-Skt, GARCH-EDF, FZ-2F against GAS-1F below 1.96)', 'Modelele cele mai slabe se separă ușor; primele cîteva nu (GARCH-Skt, GARCH-EDF, FZ-2F față de GAS-1F sub 1,96)'),
    T(r'One difference: GARCH-FZ against GAS-1F, @{dm.gchfz} here and @{dmp.gchfz} in the paper; the scale normalisation of GARCH-FZ makes its estimates fragile', r'O diferență: GARCH-FZ față de GAS-1F, @{dm.gchfz} aici și @{dmp.gchfz} în lucrare; normalizarea scalei la GARCH-FZ face estimațiile fragile'),
    T('Ninety pairwise tests need a multiple-testing answer: the MCS (Section 6)', 'Nouăzeci de teste pe perechi cer un răspuns la testarea multiplă: MCS (secțiunea 6)')])

D.frame(T('Joint (VaR, ES) regression', 'Regresia comună (VaR, ES)'), items(
    (T(r'\refDB: $q_\alpha(Y_t \mid x_t) = x_t\'\beta$, $-\mathrm{ES}_\alpha(Y_t \mid x_t) = x_t\'\gamma$, estimated jointly by minimising a Fissler--Ziegel loss', r'\refDB: $q_\alpha(Y_t \mid x_t) = x_t\'\beta$, $-\mathrm{ES}_\alpha(Y_t \mid x_t) = x_t\'\gamma$, estimate împreună prin minimizarea unei pierderi Fissler--Ziegel'),
     [T(r'M-estimator: consistent and asymptotically normal for any member of the class; the choice of $(G_1, G_2)$ affects only efficiency', r'M-estimator: consistent și asimptotic normal pentru orice membru al clasei; alegerea lui $(G_1, G_2)$ afectează doar eficiența')]),
    (T('Uses', 'Utilizări'),
     [T(r'which variables move the tail and by how much: the ES analogue of quantile regression', r'ce variabile mișcă coada și cît: analogul pentru ES al regresiei cuantilice'),
      T(r'ES backtests: regress realised returns on the ES forecast and test intercept 0, slope 1 \refBD\ (MFM, Chapter 8)', r'backtesting pentru ES: regresăm randamentele realizate pe prognoza ES și testăm termen liber 0, pantă 1 \refBD\ (MFM, Capitolul 8)')]),
    T(r'Application: S\&P 500 returns 2000--2026 on the VIX of the previous close, $\alpha$ = 2.5\%, FZ0 loss, moving-block bootstrap standard errors (blocks of 20 days)',
      r'Aplicație: randamentele S\&P 500 2000--2026 pe VIX-ul închiderii anterioare, $\alpha$ = 2,5\%, pierderea FZ0, erori standard prin bootstrap pe blocuri mobile (blocuri de 20 de zile)')), 'small')

chart(T('The tail of the S\\&P 500 against the VIX', 'Coada S\\&P 500 în funcție de VIX'), 'ats_ch9_esreg', 'ATS_ch9_esreg', [
    T(r'Daily returns against the VIX of the previous close, $T = @{er.T}$; lines: fitted 2.5\% quantile and tail mean of the joint regression',
      r'Randamentele zilnice în funcție de VIX-ul închiderii anterioare, $T = @{er.T}$; liniile: cuantila de 2,5\% și media cozii estimate prin regresia comună')],
    h='0.5\\textheight')

interp(('the joint regression', 'regresiei comune'), [
    T(r'Quantile: $@{er.b0} @{er.b1}\,\mathrm{VIX}$ (s.e.\ @{er.bs0}; @{er.bs1}); tail mean: $@{er.g0} @{er.g1}\,\mathrm{VIX}$ (s.e.\ @{er.gs0}; @{er.gs1})', r'Cuantila: $@{er.b0} @{er.b1}\,\mathrm{VIX}$ (erori standard @{er.bs0}; @{er.bs1}); media cozii: $@{er.g0} @{er.g1}\,\mathrm{VIX}$ (erori standard @{er.gs0}; @{er.gs1})'),
    T(r'One VIX point lowers the 2.5\% quantile by @{er.b1a} and the tail mean by @{er.g1a} percentage points: the tail fans out @{er.ratio} times faster in ES', r'Un punct de VIX coboară cuantila de 2,5\% cu @{er.b1a} și media cozii cu @{er.g1a} puncte procentuale: coada se deschide de @{er.ratio} ori mai repede în ES'),
    T(r'The quantile part is close to quantile regression ($@{er.q0}$, $@{er.q1}$); in-sample hit rate @{er.hit}\%; the PZC tests do not reject ($p$ = @{er.pv}; @{er.pe})', r'Partea de cuantilă este apropiată de regresia cuantilică ($@{er.q0}$, $@{er.q1}$); rata de depășire în eșantion @{er.hit}\%; testele PZC nu resping ($p$ = @{er.pv}; @{er.pe})'),
    T('The VIX is a market forecast of volatility: the regression says that the option market prices the left tail almost linearly', 'VIX este o prognoză de piață a volatilității: regresia arată că piața opțiunilor evaluează coada stîngă aproape liniar')])

D.recap(('Semiparametric (VaR, ES) models', 'modelele semiparametrice (VaR, ES)'), [
    T('FZ0 minimisation estimates the tail pair without a distribution', 'Minimizarea FZ0 estimează perechea din coadă fără o distribuție'),
    T('GAS forcing variables are identification functions: the model corrects itself only when the tail speaks', 'Variabilele de impuls GAS sînt funcții de identificare: modelul se corectează doar cînd vorbește coada'),
    T('The PZC ranking replicates; their goodness-of-fit results do not; joint regression links the tail to covariates', 'Ordonarea PZC se replică; rezultatele testelor de adecvare nu; regresia comună leagă coada de covariabile')])

# =============================================================================
# 5. BACKTESTING
# =============================================================================
D.section('Backtesting as a test of calibration', 'Backtesting ca test de calibrare')

D.frame(T('Recap: counting hits', 'Recapitulare: numărarea depășirilor'), items(
    (T(r'Hits $I_t = \mathbf 1\{y_t < v_t\}$; correct VaR $\Rightarrow I_t$ i.i.d.\ Bernoulli($\alpha$) (MFM, Chapter 8)', r'Depășirile $I_t = \mathbf 1\{y_t < v_t\}$; VaR corect $\Rightarrow I_t$ i.i.d.\ Bernoulli($\alpha$) (MFM, Capitolul 8)'),
     [T(r'\refKup: unconditional coverage, LR $\sim \chi^2_1$; \refChr: independence of consecutive hits and conditional coverage, $\chi^2_2$', r'\refKup: acoperirea necondiționată, LR $\sim \chi^2_1$; \refChr: independența depășirilor consecutive și acoperirea condiționată, $\chi^2_2$'),
      T(r'Basel traffic light \refBCBS: green up to 4 hits of VaR 1\% in 250 days, yellow 5--9, red from 10', r'Semaforul Basel \refBCBS: verde pînă la 4 depășiri ale VaR 1\% în 250 de zile, galben 5--9, roșu de la 10')]),
    (T('What counting misses', 'Ce nu vede numărarea'),
     [T('hits that depend on information other than the last hit (DQ)', 'depășirile care depind de altă informație decît ultima depășire (DQ)'),
      T('the size of tail losses (ES backtests); the spacing of hits (duration tests)', 'mărimea pierderilor din coadă (backtesting pentru ES); distanța dintre depășiri (teste de durată)'),
      T('the effect of estimated parameters on the null distribution', 'efectul parametrilor estimați asupra distribuției sub ipoteza nulă')])), 'small')

D.frame(T('Conditional calibration', 'Calibrarea condiționată'), items(
    (T(r'A forecast $x_t$ of $\mathrm T$ is \textbf{conditionally calibrated} if $\E[V(x_t, Y_t) \mid \mathcal F_{t-1}] = 0$, with $V$ the identification function \refNZ', r'O prognoză $x_t$ a lui $\mathrm T$ este \textbf{calibrată condiționat} dacă $\E[V(x_t, Y_t) \mid \mathcal F_{t-1}] = 0$, unde $V$ este funcția de identificare \refNZ'),
     [T(r'for any instruments $h_{t-1} \in \mathcal F_{t-1}$: $\E[h_{t-1}V(x_t, Y_t)] = 0$, a moment test (Wald, $\chi^2$)', r'pentru orice instrumente $h_{t-1} \in \mathcal F_{t-1}$: $\E[h_{t-1}V(x_t, Y_t)] = 0$, un test de momente (Wald, $\chi^2$)')]),
    (T(r'PZC, eq.~(40)--(41): standardised generalised residuals $\lambda^s_{v,t} = \mathbf 1\{y_t \le v_t\} - \alpha$ and $\lambda^s_{e,t} = \dfrac{\mathbf 1\{y_t \le v_t\}y_t}{\alpha e_t} - 1$', r'PZC, ec.~(40)--(41): reziduurile generalizate standardizate $\lambda^s_{v,t} = \mathbf 1\{y_t \le v_t\} - \alpha$ și $\lambda^s_{e,t} = \dfrac{\mathbf 1\{y_t \le v_t\}y_t}{\alpha e_t} - 1$'),
     [T(r'regress each on (1, its own lag, $v_t$ or $e_t$) and test that all three coefficients are zero; we use a White (HC0) covariance', r'regresăm fiecare pe (1, propriul decalaj, $v_t$ sau $e_t$) și testăm că toți cei trei coeficienți sînt zero; folosim covarianța White (HC0)')]),
    T('DQ is the special case for VaR; the ES regression tests ES only jointly with VaR, as elicitability predicts', 'DQ este cazul particular pentru VaR; regresia pentru ES testează ES doar împreună cu VaR, cum prevede elicitabilitatea'),
    T('Power comes from the instruments: lagged hits detect clustering, the forecast level detects scale errors', 'Puterea vine din instrumente: depășirile întîrziate detectează gruparea, nivelul prognozei detectează erorile de scală')), 'small')

D.frame(T('Duration-based backtests', 'Teste pe baza duratelor'), items(
    (T(r'\refCP: under a correct VaR the durations $d_i$ between hits are geometric, memoryless, mean $1/\alpha$', r'\refCP: pentru un VaR corect, duratele $d_i$ dintre depășiri sînt geometrice, fără memorie, cu media $1/\alpha$'),
     [T(r'alternative: Weibull hazard $\lambda(d) = a^b b\,d^{b-1}$; $b < 1$ is a decreasing hazard, i.e.\ hits cluster', r'alternativa: hazardul Weibull $\lambda(d) = a^b b\,d^{b-1}$; $b < 1$ înseamnă hazard descrescător, adică depășirile se grupează')]),
    (T(r'Likelihood with censoring: the first and last spells are incomplete, they enter through the survival function $S(d) = e^{-(ad)^b}$', r'Verosimilitatea cu cenzurare: primul și ultimul interval sînt incomplete și intră prin funcția de supraviețuire $S(d) = e^{-(ad)^b}$'),
     [T(r'$\mathrm{LR} = 2[\ln L(\hat a, \hat b) - \ln L(\tilde a, 1)] \to \chi^2_1$; small-sample $p$-values by simulation are advisable', r'$\mathrm{LR} = 2[\ln L(\hat a, \hat b) - \ln L(\tilde a, 1)] \to \chi^2_1$; pentru eșantioane mici se recomandă valori $p$ prin simulare')]),
    T('Durations see clustering at any distance, not only on consecutive days as Christoffersen\'s test does', 'Duratele văd gruparea la orice distanță, nu doar în zile consecutive, ca testul lui Christoffersen')), 'small')

chart(T('How far apart are the hits?', 'Cît de departe sînt depășirile una de alta?'), 'ats_ch9_durations', 'ATS_ch9_backtests', [
    T(r'S\&P 500, VaR 2.5\%, out of sample 2000--2026; empirical survival of the durations between hits (log scale) against the geometric law of a correct model',
      r'S\&P 500, VaR 2,5\%, în afara eșantionului 2000--2026; funcția de supraviețuire empirică a duratelor dintre depășiri (scară logaritmică) față de legea geometrică a unui model corect')],
    h='0.5\\textheight')

interp(('the durations', 'duratelor'), [
    T(r'RW-250: @{du.rw250.s5}\% of the durations are at most 5 days (geometric: @{du.geo5}\%); Weibull $b$ = @{du.rw250.b}, $p$ @{du.rw250.p}: strong clustering', r'RW-250: @{du.rw250.s5}\% din durate sînt de cel mult 5 zile (geometric: @{du.geo5}\%); Weibull $b$ = @{du.rw250.b}, $p$ @{du.rw250.p}: grupare puternică'),
    T(r'GARCH-EDF: $b$ = @{du.gchedf.b}, $p$ = @{du.gchedf.p}; GAS-1F: $b$ = @{du.fz1f.b}, $p$ = @{du.fz1f.p}: dynamic models remove most of the clustering', r'GARCH-EDF: $b$ = @{du.gchedf.b}, $p$ = @{du.gchedf.p}; GAS-1F: $b$ = @{du.fz1f.b}, $p$ = @{du.fz1f.p}: modelele dinamice elimină cea mai mare parte a grupării'),
    T('The long tail of RW-250 (calm years without hits) is the other face of clustering: the window remembers old crises', 'Coada lungă a RW-250 (ani calmi fără depășiri) este cealaltă față a grupării: fereastra își amintește crizele vechi'),
    T('All models have too many hits overall (Section 5 table): parameters fixed in 1999 are too optimistic after 2000', 'Toate modelele au prea multe depășiri în total (tabelul din secțiunea 5): parametrii fixați în 1999 sînt prea optimiști după 2000')])

D.frame(T('Backtesting ES: what each test needs', 'Backtesting pentru ES: ce cere fiecare test'), table(
    TB + 'p{3.2cm}' + TB + 'p{4.5cm}' + TB + 'p{3.8cm}',
    T(r'\textbf{Test}', r'\textbf{Testul}') + ' & ' + T(r'\textbf{Statistic}', r'\textbf{Statistica}') + ' & ' + T(r'\textbf{Inputs}', r'\textbf{Date necesare}'),
    [r'\refMF & ' + T(r'mean of $(y_t - e_t)/\sigma_t$ on hit days, bootstrap', r'media lui $(y_t - e_t)/\sigma_t$ în zilele cu depășiri, bootstrap') + ' & ' + T(r'$v_t$, $e_t$, $\sigma_t$', r'$v_t$, $e_t$, $\sigma_t$'),
     r'\refAS\ $Z_2$ & $1 - \frac{1}{T\alpha}\sum_t \frac{y_tI_t}{e_t}$ & ' + T('$v_t$, $e_t$ and the forecast distribution (simulated $p$-value)', '$v_t$, $e_t$ și distribuția prognozată (valoare $p$ simulată)'),
     r'\refDE & ' + T(r'cumulative violations $H_t = \frac{1}{\alpha}(\alpha - u_t)\mathbf 1\{u_t \le \alpha\}$', r'depășirile cumulate $H_t = \frac{1}{\alpha}(\alpha - u_t)\mathbf 1\{u_t \le \alpha\}$') + ' & ' + T(r'the PIT $u_t = F_{t|t-1}(y_t)$', r'PIT $u_t = F_{t|t-1}(y_t)$'),
     r'\refKLM & ' + T('multinomial test of several VaR levels', 'test multinomial pentru mai multe niveluri VaR') + ' & ' + T('the PIT, or VaR at several levels', 'PIT sau VaR la mai multe niveluri'),
     r'\refPZC, \refBD & ' + T('regression on $(v_t, e_t)$', 'regresie pe $(v_t, e_t)$') + r' & $v_t$, $e_t$'],
    size='scriptsize') + items(
    T('Only the regression tests use nothing beyond the pair (VaR, ES): the others are tests of a distribution, which ES alone does not supply', 'Doar testele prin regresie nu folosesc nimic în plus față de perechea (VaR, ES): celelalte testează o distribuție, pe care ES singur nu o furnizează')), 'footnotesize')

D.frame(T('Estimation risk in backtests', 'Riscul de estimare în backtesting'), items(
    (T(r'Backtests assume the VaR is known; in practice $\hat v_t = v_t(\hat\theta_R)$, with $\hat\theta_R$ estimated on $R$ days and tested on $P$ days \refEO', r'Testele presupun că VaR este cunoscut; în practică $\hat v_t = v_t(\hat\theta_R)$, cu $\hat\theta_R$ estimat pe $R$ zile și testat pe $P$ zile \refEO'),
     [T(r'$P^{-1/2}\sum_t(\hat I_t - \alpha) = P^{-1/2}\sum_t(I_t - \alpha) + \underbrace{\sqrt{P/R}\cdot\E[f_t(v_t)\nabla v_t\']\sqrt R(\hat\theta_R - \theta)}_{\text{estimation term}}$', r'$P^{-1/2}\sum_t(\hat I_t - \alpha) = P^{-1/2}\sum_t(I_t - \alpha) + \underbrace{\sqrt{P/R}\cdot\E[f_t(v_t)\nabla v_t\']\sqrt R(\hat\theta_R - \theta)}_{\text{termenul de estimare}}$')]),
    (T(r'The estimation term vanishes only if $P/R \to 0$; with a fixed window it grows with the test sample', r'Termenul de estimare dispare doar dacă $P/R \to 0$; cu o fereastră fixă crește odată cu eșantionul de test'),
     [T('the Kupiec variance $\\alpha(1 - \\alpha)$ is then too small and the test over-rejects a correct model', 'varianța Kupiec $\\alpha(1 - \\alpha)$ este atunci prea mică, iar testul respinge prea des un model corect'),
      T('fixes: the corrected variance of Escanciano and Olmo, a subsampling or bootstrap of the whole estimate-and-test procedure', 'remedii: varianța corectată a lui Escanciano și Olmo, subeșantionarea sau bootstrap pentru întreaga procedură de estimare și testare')]),
    T('A Monte Carlo shows the size of the problem for the windows banks actually use', 'Un experiment Monte Carlo arată mărimea problemei pentru ferestrele folosite efectiv de bănci')), 'small')

chart(T('Size of backtests with estimated parameters', 'Mărimea testelor cu parametri estimați'), 'ats_ch9_estrisk_mc', 'ATS_ch9_backtests', [
    T(r'GARCH(1,1) data ($\omega$ = 0.02, $\alpha$ = 0.08, $\beta$ = 0.90, Normal), the correct model estimated by QML on $R$ days, VaR 1\% on the next $P$ days; @{mc.reps} replications; nominal size 5\%',
      r'Date GARCH(1,1) ($\omega$ = 0,02, $\alpha$ = 0,08, $\beta$ = 0,90, distribuția Normală), modelul corect estimat prin QML pe $R$ zile, VaR 1\% pe următoarele $P$ zile; @{mc.reps} de replicări; mărimea nominală 5\%')],
    h='0.5\\textheight')

interp(('the Monte Carlo', 'experimentului Monte Carlo'), [
    T(r'Known parameters: Kupiec rejects @{mc.250_250.kup0}\%, @{mc.250_1000.kup0}\% and @{mc.250_2500.kup0}\% for $P$ = 250, 1000, 2500: close to 5\% except with few hits', r'Parametri cunoscuți: Kupiec respinge @{mc.250_250.kup0}\%, @{mc.250_1000.kup0}\% și @{mc.250_2500.kup0}\% pentru $P$ = 250, 1000, 2500: aproape de 5\%, cu excepția cazului cu puține depășiri'),
    T(r'Estimated on $R$ = 250: @{mc.250_250.kup}\%, @{mc.250_1000.kup}\%, @{mc.250_2500.kup}\%: a correct model is rejected more often the longer we test', r'Estimat pe $R$ = 250: @{mc.250_250.kup}\%, @{mc.250_1000.kup}\%, @{mc.250_2500.kup}\%: un model corect este respins mai des cu cît testăm mai mult'),
    T(r'With $R$ = 1000 the distortion shrinks (@{mc.1000_2500.kup}\% at $P$ = 2500); the hit rate across replications has s.d.\ @{mc.250_2500.sd} pp against @{mc.1000_2500.sd} pp', r'Cu $R$ = 1000 distorsiunea scade (@{mc.1000_2500.kup}\% la $P$ = 2500); rata de depășire între replicări are abaterea standard @{mc.250_2500.sd} pp față de @{mc.1000_2500.sd} pp'),
    T(r'DQ is oversized even with known parameters (@{mc.1000_2500.dq0}\%): rare hits make the $\chi^2_6$ approximation poor', r'DQ respinge prea des chiar cu parametri cunoscuți (@{mc.1000_2500.dq0}\%): depășirile rare fac aproximarea $\chi^2_6$ slabă')])

chart(T('Calibration tests across assets', 'Teste de calibrare pe active'), 'ats_ch9_backtests', 'ATS_ch9_backtests', [
    T(r'PZC goodness-of-fit regressions for VaR and ES 2.5\%, ten models, parameters estimated on the first ten years (five for Bitcoin) and kept fixed to 18 September 2026',
      r'Regresiile de adecvare PZC pentru VaR și ES 2,5\%, zece modele, parametri estimați pe primii zece ani (cinci pentru Bitcoin) și păstrați ficși pînă la 18 septembrie 2026')],
    h='0.52\\textheight')

interp(('the calibration tests', 'testelor de calibrare'), [
    T(r'Only @{bt.npass} of 50 asset--model pairs pass both regressions at 10\%: over 10--26 years with fixed parameters almost every model is miscalibrated somewhere', r'Doar @{bt.npass} din 50 de perechi activ--model trec ambele regresii la 10\%: pe 10--26 de ani cu parametri ficși, aproape orice model este necalibrat undeva'),
    T(r'S\&P 500 hit rates at 2.5\%: GAS-1F @{bt.sp500.fz1f.hit}\%, GARCH-EDF @{bt.sp500.gchedf.hit}\%, RW-250 @{bt.sp500.rw250.hit}\%: the level drifts after the estimation decade', r'Ratele de depășire S\&P 500 la 2,5\%: GAS-1F @{bt.sp500.fz1f.hit}\%, GARCH-EDF @{bt.sp500.gchedf.hit}\%, RW-250 @{bt.sp500.rw250.hit}\%: nivelul derivă după deceniul de estimare'),
    T(r'EUR/RON: estimated on 2005--2015 (crisis and float), the GARCH models over-predict risk afterwards (GARCH-EDF @{bt.eurron.gchedf.hit}\% hits): miscalibration in the safe direction is rejected too', r'EUR/RON: estimate pe 2005--2015 (criză și flotare), modelele GARCH supraestimează apoi riscul (GARCH-EDF @{bt.eurron.gchedf.hit}\% depășiri): și necalibrarea în direcția prudentă este respinsă'),
    T(r'Bitcoin: short history and noisy tail, low power; the simple models pass (RW-500 @{bt.btc.rw500.hit}\%)', r'Bitcoin: istorie scurtă și coadă zgomotoasă, putere redusă; modelele simple trec (RW-500 @{bt.btc.rw500.hit}\%)'),
    T('A backtest answers ``is it calibrated?\'\'; whether to prefer one failing model to another is a comparison question', 'Un backtest răspunde la „este calibrat?”; dacă un model respins este preferabil altuia este o întrebare de comparație')], size='footnotesize')

D.recap(('Backtesting', 'backtesting'), [
    T('Backtests are moment tests of the identification function with chosen instruments', 'Backtesting-ul înseamnă teste de momente ale funcției de identificare cu instrumente alese'),
    T('Durations catch clustering at any distance; ES tests need more than ES, except the regression tests', 'Duratele surprind gruparea la orice distanță; testele ES cer mai mult decît ES, cu excepția testelor prin regresie'),
    T('Estimated parameters inflate the size; long, fixed-parameter evaluations reject almost everything', 'Parametrii estimați cresc mărimea testelor; evaluările lungi, cu parametri ficși, resping aproape totul')])

# =============================================================================
# 6. COMPARAȚIE
# =============================================================================
D.section('Comparing risk forecasts', 'Compararea prognozelor de risc')

D.frame(T('From backtests to comparative backtests', 'De la backtesting la backtesting comparativ'), items(
    (T(r'\refNZ: a traditional backtest tests $H_0$: ``the bank\'s model is calibrated\'\'; a comparative backtest tests the bank\'s model against a standard one with a consistent score', r'\refNZ: backtesting-ul tradițional testează $H_0$: „modelul băncii este calibrat”; backtesting-ul comparativ testează modelul băncii față de unul standard cu un scor consistent'),
     [T(r'$H_0^-$: internal at least as good as standard; $H_0^+$: at most as good; green if $H_0^+$ is rejected, red if $H_0^-$ is rejected, yellow otherwise', r'$H_0^-$: modelul intern cel puțin la fel de bun ca cel standard; $H_0^+$: cel mult la fel de bun; verde dacă $H_0^+$ se respinge, roșu dacă $H_0^-$ se respinge, galben altfel')]),
    (T('Information sets matter \\refHE: a calibrated forecast based on more information has a lower expected consistent score', 'Contează mulțimea de informații \\refHE: o prognoză calibrată care folosește mai multă informație are un scor consistent așteptat mai mic'),
     [T('so a ranking by FZ0 rewards both calibration and information, which a backtest cannot do', 'deci o ordonare prin FZ0 răsplătește și calibrarea, și informația, ceea ce un backtest nu poate face')]),
    T(r'Tools from Chapter 1: DM with HAC variance \refDM, Giacomini--White for estimated forecasting methods \refGW, the MCS \refHLN', r'Instrumente din Capitolul 1: DM cu varianță HAC \refDM, Giacomini--White pentru metode de prognoză estimate \refGW, MCS \refHLN')), 'small')

D.frame(T('Design of the comparison', 'Designul comparației'), items(
    (T(r'Ten PZC models, $\alpha$ = 2.5\%, FZ0 losses out of sample: S\&P 500 and DAX from 2000, BET from 2010, EUR/RON from July 2015, Bitcoin from 2020', r'Cele zece modele PZC, $\alpha$ = 2,5\%, pierderi FZ0 în afara eșantionului: S\&P 500 și DAX din 2000, BET din 2010, EUR/RON din iulie 2015, Bitcoin din 2020'), []),
    (T(r'90\% MCS with the $T_{\max}$ statistic, moving-block bootstrap (blocks of 10 days over the whole period, 5 days in a stress period), 1000 replications', r'MCS de 90\% cu statistica $T_{\max}$, bootstrap pe blocuri mobile (blocuri de 10 zile pe toată perioada, 5 zile într-o perioadă de criză), 1000 de replicări'), []),
    (T('Stress periods fixed before looking at the losses', 'Perioadele de criză fixate înainte de a vedea pierderile'),
     [T('2008: September 2008 -- March 2009; 2020: 19 February -- 30 June 2020; 2022: the calendar year; 2025: March -- June 2025', '2008: septembrie 2008 -- martie 2009; 2020: 19 februarie -- 30 iunie 2020; 2022: anul calendaristic; 2025: martie -- iunie 2025'),
      T(r'S\&P 500 in 2020: @{cmp.sp500.2020.T} days, of which @{cmp.sp500.2020.h} GAS-1F hits; in 2025: @{cmp.sp500.2025.T} days, @{cmp.sp500.2025.h} hits', r'S\&P 500 în 2020: @{cmp.sp500.2020.T} zile, dintre care @{cmp.sp500.2020.h} depășiri GAS-1F; în 2025: @{cmp.sp500.2025.T} zile, @{cmp.sp500.2025.h} depășiri')]),
    T('A stress window holds a few tail days: expect wide MCS sets and unstable winners', 'O fereastră de criză conține puține zile din coadă: ne așteptăm la mulțimi MCS largi și la cîștigători instabili')), 'small')

chart(T('Losses in stress periods', 'Pierderile în perioadele de criză'), 'ats_ch9_stress', 'ATS_ch9_comparison', [
    T(r'Average FZ0 loss of each model minus that of the best model in the same period (symmetric log scale); bars missing when the period is not out of sample',
      r'Pierderea FZ0 medie a fiecărui model minus cea a celui mai bun model din aceeași perioadă (scară logaritmică simetrică); barele lipsesc cînd perioada nu este în afara eșantionului')],
    h='0.52\\textheight')

interp(('the stress-period losses', 'pierderilor din perioadele de criză'), [
    T(r'Winners over the whole period: S\&P 500 @{best.sp500.full}, DAX @{best.dax.full}, BET @{best.bet.full}, EUR/RON @{best.eurron.full}, Bitcoin @{best.btc.full}', r'Cîștigătorii pe toată perioada: S\&P 500 @{best.sp500.full}, DAX @{best.dax.full}, BET @{best.bet.full}, EUR/RON @{best.eurron.full}, Bitcoin @{best.btc.full}'),
    T(r'In 2020 the winner changes: S\&P 500 @{best.sp500.2020}, BET @{best.bet.2020}, Bitcoin @{best.btc.2020}; rolling windows lose most in every crash', r'În 2020 cîștigătorul se schimbă: S\&P 500 @{best.sp500.2020}, BET @{best.bet.2020}, Bitcoin @{best.btc.2020}; ferestrele mobile pierd cel mai mult în fiecare criză'),
    T('Crashes separate models by an order of magnitude more than calm years: an average over the whole period is dominated by a few weeks', 'Crizele separă modelele cu un ordin de mărime mai mult decît anii calmi: o medie pe toată perioada este dominată de cîteva săptămîni'),
    T('No model wins every crisis; the semiparametric models are competitive but not dominant out of sample after 2016', 'Niciun model nu cîștigă fiecare criză; modelele semiparametrice sînt competitive, dar nu domină în afara eșantionului după 2016')], size='footnotesize')

chart(T('Model confidence sets', 'Mulțimi de încredere ale modelelor'), 'ats_ch9_mcs', 'ATS_ch9_comparison', [
    T(r'MCS $p$-values (FZ0 loss, $\alpha$ = 2.5\%); green: in the 90\% MCS', r'Valorile $p$ MCS (pierderea FZ0, $\alpha$ = 2,5\%); verde: în MCS de 90\%')],
    h='0.52\\textheight')

interp(('the MCS', 'mulțimilor MCS'), [
    T(r'Whole period, MCS sizes: S\&P 500 @{mcs.full.sp500}, DAX @{mcs.full.dax}, BET @{mcs.full.bet}, EUR/RON @{mcs.full.eurron}, Bitcoin @{mcs.full.btc} of 10', r'Toată perioada, mărimea MCS: S\&P 500 @{mcs.full.sp500}, DAX @{mcs.full.dax}, BET @{mcs.full.bet}, EUR/RON @{mcs.full.eurron}, Bitcoin @{mcs.full.btc} din 10'),
    T(r'Rolling windows are eliminated on the long equity samples; in 2020 and 2022 almost everything survives (2020: @{mcs.2020.sp500} on the S\&P 500; 2022: @{mcs.2022.sp500})', r'Ferestrele mobile sînt eliminate pe eșantioanele lungi de acțiuni; în 2020 și 2022 aproape totul rămîne (2020: @{mcs.2020.sp500} pe S\&P 500; 2022: @{mcs.2022.sp500})'),
    T(r'EUR/RON in 2020 is the exception: only @{mcs.2020.eurron} models survive, the rolling windows and the Hybrid', r'EUR/RON în 2020 este excepția: rămîn doar @{mcs.2020.eurron} modele, ferestrele mobile și Hybrid'),
    T('A large MCS is a result, not a failure: the crisis windows are too short to separate tail forecasts', 'O mulțime MCS mare este un rezultat, nu un eșec: ferestrele de criză sînt prea scurte pentru a separa prognozele cozii')])

D.recap(('Comparison', 'compararea'), [
    T('Comparative backtests put the burden of proof on the model, and reward information', 'Backtesting-ul comparativ pune sarcina probei pe model și răsplătește informația'),
    T('Rankings change in crises; whole-period averages hide this', 'Ordonările se schimbă în crize; mediile pe toată perioada ascund acest lucru'),
    T('Report the MCS, not the winner', 'Raportați MCS, nu cîștigătorul')])

# =============================================================================
# 7. ORIZONTUL
# =============================================================================
D.section('The horizon: multi-period risk', 'Orizontul: riscul pe mai multe perioade')

D.frame(T('Why the square-root-of-time rule fails', 'Limitele regulii rădăcinii pătrate a timpului'), items(
    (T(r'$\mathrm{VaR}^{(h)} = \sqrt h\,\mathrm{VaR}^{(1)}$ holds for i.i.d.\ Normal returns with zero mean (stable laws: $h^{1/\gamma}$)', r'$\mathrm{VaR}^{(h)} = \sqrt h\,\mathrm{VaR}^{(1)}$ este valabilă pentru randamente i.i.d.\ din distribuția Normală cu media zero (legi stabile: $h^{1/\gamma}$)'),
     [T(r'fat tails that are not stable: the $h$-day sum is closer to Normal than the daily return, so $\sqrt h$ overstates the quantile at long horizons \refDZ', r'cozi groase care nu sînt stabile: suma pe $h$ zile este mai apropiată de distribuția Normală decît randamentul zilnic, deci $\sqrt h$ supraestimează cuantila la orizonturi lungi \refDZ')]),
    (T(r'Volatility clustering: $\mathrm{Var}_t(\sum_{k=1}^h y_{t+k}) = \sum_{k=0}^{h-1}\big[\bar\sigma^2 + (\alpha + \beta)^k(\sigma_{t+1}^2 - \bar\sigma^2)\big]$ for GARCH(1,1)', r'Volatility clustering: $\mathrm{Var}_t(\sum_{k=1}^h y_{t+k}) = \sum_{k=0}^{h-1}\big[\bar\sigma^2 + (\alpha + \beta)^k(\sigma_{t+1}^2 - \bar\sigma^2)\big]$ pentru GARCH(1,1)'),
     [T(r'in calm times $\sqrt h$ understates risk, in crises it overstates it: mean reversion of volatility', r'în perioade calme $\sqrt h$ subestimează riscul, în crize îl supraestimează: revenirea volatilității la medie')]),
    T('Leverage (GJR) makes multi-day losses more skewed than daily ones: the left tail of the sum is thicker than the scaled daily tail', 'Efectul de levier (GJR) face pierderile pe mai multe zile mai asimetrice decît cele zilnice: coada stîngă a sumei este mai groasă decît coada zilnică scalată'),
    T('Remedies: simulate the $h$-day distribution (FHS), or forecast the $h$-day quantile directly (quantile regression on $h$-day returns)', 'Remedii: simularea distribuției pe $h$ zile (FHS) sau prognoza directă a cuantilei pe $h$ zile (regresie cuantilică pe randamentele pe $h$ zile)')), 'small')

D.frame(T('Multi-day forecasts and their backtests', 'Prognozele pe mai multe zile și testarea lor'), items(
    (T(r'FHS: GJR-GARCH(1,1) by QML on a rolling 2000-day window (re-estimated every 250 days); 2000 paths of 10 days with bootstrapped standardised residuals \refBoll, \refGJR', r'FHS: GJR-GARCH(1,1) prin QML pe o fereastră mobilă de 2000 de zile (reestimat la fiecare 250 de zile); 2000 de traiectorii de 10 zile cu reziduuri standardizate extrase prin bootstrap \refBoll, \refGJR'), []),
    (T('Backtesting 10-day VaR', 'Backtesting pentru VaR pe 10 zile'),
     [T(r'daily 10-day forecasts overlap: hits are MA(9) even under $H_0$; counting them as independent inflates the size (Chapter 0, overlapping observations)', r'prognozele zilnice pe 10 zile se suprapun: depășirile sînt MA(9) chiar sub $H_0$; tratarea lor ca independente crește mărimea testului (Capitolul 0, observații suprapuse)'),
      T('options: non-overlapping windows (every 10th day, few hits), or HAC variance on overlapping hits', 'variante: ferestre fără suprapunere (fiecare a zecea zi, puține depășiri) sau varianță HAC pentru depășirile suprapuse')]),
    T('Basel uses 10-day horizons and liquidity-adjusted horizons for ES (MAR33): the horizon problem is regulatory, not academic', 'Basel folosește orizonturi de 10 zile și orizonturi ajustate pentru lichiditate la ES (MAR33): problema orizontului este una de reglementare, nu academică')), 'small')

chart(T('10-day VaR 1\\% against the square-root-of-time rule', 'VaR 1\\% pe 10 zile față de regula rădăcinii pătrate'), 'ats_ch9_sqrt', 'ATS_ch9_horizon', [
    T(r'S\&P 500, 2001--2026: ratio of the 10-day VaR 1\% by FHS to $\sqrt{10}$ times the 1-day VaR 1\% of the same model; right: the ratio against today\'s forecast volatility',
      r'S\&P 500, 2001--2026: raportul dintre VaR 1\% pe 10 zile prin FHS și $\sqrt{10}$ înmulțit cu VaR 1\% pe o zi al aceluiași model; dreapta: raportul în funcție de volatilitatea prognozată azi')],
    h='0.5\\textheight')

interp(('the horizon ratio', 'raportului de orizont'), [
    T(r'Median ratio @{sq.r_med}, range @{sq.r_min} to @{sq.r_max}: $\sqrt{10}$ scaling usually understates the 10-day VaR 1\% of the S\&P 500', r'Raportul median @{sq.r_med}, între @{sq.r_min} și @{sq.r_max}: scalarea cu $\sqrt{10}$ subestimează de obicei VaR 1\% pe 10 zile pentru S\&P 500'),
    T(r'Low-volatility days: median @{sq.r_lo}; high-volatility days: @{sq.r_hi}: mean reversion pushes the ratio towards 1 in crises', r'Zilele cu volatilitate scăzută: mediana @{sq.r_lo}; zilele cu volatilitate ridicată: @{sq.r_hi}: revenirea la medie împinge raportul spre 1 în crize'),
    T(r'Non-overlapping backtest (@{sq.n} windows, @{sq.exp} expected hits): FHS @{sq.nf}, $\sqrt{10}$ rule @{sq.ns}; Kupiec $p$ @{sq.kf} and @{sq.ks}', r'Backtesting fără suprapunere (@{sq.n} ferestre, @{sq.exp} depășiri așteptate): FHS @{sq.nf}, regula $\sqrt{10}$ @{sq.ns}; Kupiec $p$ @{sq.kf} și @{sq.ks}'),
    T('So few hits cannot separate the two: horizon errors of this size are invisible to a non-overlapping backtest', 'Atît de puține depășiri nu le pot separa: erori de orizont de această mărime sînt invizibile pentru un backtest fără suprapunere')])

D.recap(('The horizon', 'orizontul'), [
    T('The square-root rule needs i.i.d.\\ Normal returns; clustering, leverage and fat tails break it in opposite directions', 'Regula rădăcinii pătrate cere randamente i.i.d.\\ din distribuția Normală; volatility clustering, efectul de levier și cozile groase o contrazic în direcții opuse'),
    T('Simulate the horizon or model it directly; backtest with non-overlapping windows or HAC variances', 'Simulați orizontul sau modelați-l direct; testați cu ferestre fără suprapunere sau cu varianțe HAC'),
    T('Multi-day tests have very little power', 'Testele pe mai multe zile au o putere foarte mică')])

# =============================================================================
# 8. RISCUL DE MODEL ȘI DE ESTIMARE
# =============================================================================
D.section('Model risk and estimation risk', 'Riscul de model și riscul de estimare')

D.frame(T('Model risk of risk models', 'Riscul de model al modelelor de risc'), items(
    (T(r'\refDJVZ: \textbf{risk ratio} $\mathrm{RR}_t = \max_m\mathrm{VaR}_{m,t}/\min_m\mathrm{VaR}_{m,t}$ across standard models: the disagreement a regulator should expect', r'\refDJVZ: \textbf{raportul de risc} $\mathrm{RR}_t = \max_m\mathrm{VaR}_{m,t}/\min_m\mathrm{VaR}_{m,t}$ între modele standard: dezacordul la care trebuie să se aștepte un supraveghetor'),
     [T('they find the ratio largest exactly in crises, when risk numbers matter most', 'ei găsesc raportul cel mai mare tocmai în crize, cînd cifrele de risc contează cel mai mult')]),
    (T(r'\refBDKM: \textbf{risk models-at-risk}: quantify the model risk of a VaR forecast and adjust the forecast for estimation and specification errors', r'\refBDKM: \textbf{risk models-at-risk}: cuantificăm riscul de model al unei prognoze VaR și ajustăm prognoza pentru erorile de estimare și de specificare'), []),
    (T(r'\refKR: ES carries more model risk than VaR at comparable levels: it extrapolates further into the tail', r'\refKR: ES are mai mult risc de model decît VaR la niveluri comparabile: extrapolează mai departe în coadă'), []),
    T('Our six models, rolling 1000-day windows: historical simulation, Normal with window volatility, EWMA ($\\lambda$ = 0.94), GARCH-N, GARCH-t, filtered HS', 'Cele șase modele ale noastre, ferestre mobile de 1000 de zile: simulare istorică, distribuția Normală cu volatilitatea ferestrei, EWMA ($\\lambda$ = 0,94), GARCH-N, GARCH-t, FHS')), 'small')

chart(T('How much do standard models disagree?', 'Cît de mult diferă modelele standard?'), 'ats_ch9_riskratio', 'ATS_ch9_modelrisk', [
    T(r'Risk ratio of six VaR 1\% forecasts, 21-day rolling median, S\&P 500 and BET, 2002--2026 (BET from 2004); shaded: stress periods',
      r'Raportul de risc al celor șase prognoze VaR 1\%, mediana mobilă pe 21 de zile, S\&P 500 și BET, 2002--2026 (BET din 2004); zonele colorate: perioadele de criză')],
    h='0.5\\textheight')

interp(('the risk ratio', 'raportului de risc'), [
    T(r'Median risk ratio @{rr.sp500.med} (S\&P 500) and @{rr.bet.med} (BET); 90th percentile @{rr.sp500.q90} and @{rr.bet.q90}; maximum @{rr.sp500.mx} on @{rr.sp500.day}', r'Raportul de risc median @{rr.sp500.med} (S\&P 500) și @{rr.bet.med} (BET); percentila 90 @{rr.sp500.q90} și @{rr.bet.q90}; maximul @{rr.sp500.mx} la @{rr.sp500.day}'),
    T(r'Spring 2020: median @{rr.sp500.s2020} (S\&P 500), @{rr.bet.s2020} (BET): the slow historical simulation and the fast EWMA diverge most after a jump', r'Primăvara 2020: mediana @{rr.sp500.s2020} (S\&P 500), @{rr.bet.s2020} (BET): simularea istorică lentă și EWMA rapid diverg cel mai mult după un salt'),
    T(r'HS is the most conservative model on @{rr.sp500.hsmax}\% of S\&P 500 days, EWMA the least on @{rr.sp500.ewmin}\%', r'HS este cel mai prudent model în @{rr.sp500.hsmax}\% din zilele S\&P 500, EWMA cel mai puțin prudent în @{rr.sp500.ewmin}\%'),
    T(r'Hit rates for VaR 1\% (S\&P 500): HS @{rr.sp500.h.HS}\%, GARCH-N @{rr.sp500.h.GARCH-N}\%, GARCH-t @{rr.sp500.h.GARCH-t}\%, FHS @{rr.sp500.h.FHS}\%: the disagreement is not noise, the Normal models are wrong', r'Ratele de depășire VaR 1\% (S\&P 500): HS @{rr.sp500.h.HS}\%, GARCH-N @{rr.sp500.h.GARCH-N}\%, GARCH-t @{rr.sp500.h.GARCH-t}\%, FHS @{rr.sp500.h.FHS}\%: dezacordul nu este zgomot, modelele cu distribuția Normală greșesc')], size='footnotesize')

D.frame(T('Estimation risk in tail forecasts', 'Riscul de estimare în prognozele cozii'), items(
    (T(r'\refGS: for GARCH VaR and ES, $\sqrt T(\widehat{\mathrm{ES}}_t - \mathrm{ES}_t)$ is asymptotically normal; the variance has a volatility part and a tail-shape part', r'\refGS: pentru VaR și ES din GARCH, $\sqrt T(\widehat{\mathrm{ES}}_t - \mathrm{ES}_t)$ este asimptotic normal; varianța are o parte din volatilitate și una din forma cozii'), []),
    (T(r'Bootstrap \refCG: re-estimate the model on simulated paths and recompute the forecast \textbf{conditional on the observed history}', r'Bootstrap \refCG: reestimăm modelul pe traiectorii simulate și recalculăm prognoza \textbf{condiționat de istoria observată}'),
     [T(r'algorithm: fit GARCH-t on 2000 days; simulate 150 paths of 2000 days from the fit; re-estimate on each; filter the observed returns with each $\hat\theta^*$; ES$^*$ for tomorrow', r'algoritm: estimăm GARCH-t pe 2000 de zile; simulăm 150 de traiectorii de 2000 de zile din modelul estimat; reestimăm pe fiecare; filtrăm randamentele observate cu fiecare $\hat\theta^*$; ES$^*$ pentru ziua următoare'),
      T(r'90\% interval: the 5\% and 95\% quantiles of ES$^*$', r'intervalul de 90\%: cuantilele de 5\% și 95\% ale ES$^*$')]),
    T('The interval measures parameter uncertainty only: it is conditional on the model being right, so it is a lower bound on total uncertainty', 'Intervalul măsoară doar incertitudinea parametrilor: este condiționat de corectitudinea modelului, deci este o limită inferioară a incertitudinii totale')), 'small')

chart(T('An ES forecast with its estimation error', 'O prognoză ES cu eroarea ei de estimare'), 'ats_ch9_es_ci', 'ATS_ch9_modelrisk', [
    T(r'S\&P 500, GARCH-t ES 2.5\% for the next day at half-year ends 2019--2026, with 90\% parametric bootstrap intervals (150 re-estimations each)',
      r'S\&P 500, ES 2,5\% GARCH-t pentru ziua următoare la sfîrșitul fiecărui semestru 2019--2026, cu intervale bootstrap parametric de 90\% (cîte 150 de reestimări)')],
    h='0.5\\textheight')

interp(('the estimation error', 'erorii de estimare'), [
    T(r'Interval width relative to the forecast: median @{ci.med}\%, from @{ci.min}\% to @{ci.max}\%', r'Lățimea intervalului raportată la prognoză: mediana @{ci.med}\%, între @{ci.min}\% și @{ci.max}\%'),
    T(r'June 2020: ES @{ci.20}\% with interval [@{ci.20lo}; @{ci.20hi}]: two thousand days of data still leave a band of several tenths of a percent', r'Iunie 2020: ES @{ci.20}\% cu intervalul [@{ci.20lo}; @{ci.20hi}]: două mii de zile de date lasă totuși o bandă de cîteva zecimi de procent'),
    T('Estimation risk is small next to model risk (risk ratios near 2): the choice of model matters more than its precision', 'Riscul de estimare este mic față de riscul de model (rapoarte de risc în jur de 2): alegerea modelului contează mai mult decît precizia lui'),
    T('Capital rules that multiply a point forecast ignore both: reporting the interval is the honest minimum', 'Regulile de capital care multiplică o prognoză punctuală le ignoră pe amîndouă: raportarea intervalului este minimul onest')])

D.recap(('Model and estimation risk', 'riscul de model și de estimare'), [
    T('Standard models disagree by a factor of about two, more in crises', 'Modelele standard diferă cu un factor de circa doi, mai mult în crize'),
    T('Bootstrap intervals for ES are narrow next to that disagreement', 'Intervalele bootstrap pentru ES sînt înguste față de acest dezacord'),
    T('Report both: the forecast, its interval and the spread across models', 'Raportați ambele: prognoza, intervalul ei și dispersia între modele')])

# =============================================================================
# 9. EXTREME ȘI CALIBRARE CONFORMALĂ
# =============================================================================
D.section('Extremes under dependence and conformal calibration', 'Extreme sub dependență și calibrare conformală')

D.frame(T('Extremes of dependent series', 'Extremele seriilor dependente'), items(
    (T(r'For a stationary series, $\Pr(\max_{t \le n} X_t \le u_n) \approx F(u_n)^{n\theta}$, $\theta \in (0, 1]$ the \textbf{extremal index} \refEKM', r'Pentru o serie staționară, $\Pr(\max_{t \le n} X_t \le u_n) \approx F(u_n)^{n\theta}$, $\theta \in (0, 1]$ fiind \textbf{indicele extremal} \refEKM'),
     [T(r'$1/\theta$ = mean cluster size of exceedances; $\theta = 1$: no clustering of extremes', r'$1/\theta$ = mărimea medie a unui grup de depășiri; $\theta = 1$: extremele nu se grupează')]),
    (T(r'Intervals estimator \refFS: from the gaps $T_i$ between exceedances, $\hat\theta = \min\Big(1, \dfrac{2\big(\sum(T_i - 1)\big)^2}{(N - 1)\sum(T_i - 1)(T_i - 2)}\Big)$ (when $\max T_i > 2$)', r'Estimatorul pe intervale \refFS: din distanțele $T_i$ dintre depășiri, $\hat\theta = \min\Big(1, \dfrac{2\big(\sum(T_i - 1)\big)^2}{(N - 1)\sum(T_i - 1)(T_i - 2)}\Big)$ (cînd $\max T_i > 2$)'), []),
    T(r'\refMF: fit GARCH, apply EVT to the standardised residuals; it works if filtering removes the clustering ($\theta$ near 1 after filtering)', r'\refMF: estimăm GARCH, aplicăm EVT reziduurilor standardizate; metoda funcționează dacă filtrarea elimină gruparea ($\theta$ aproape de 1 după filtrare)')), 'small')

chart(T('Extremal index before and after filtering', 'Indicele extremal înainte și după filtrare'), 'ats_ch9_extremal', 'ATS_ch9_extremes', [
    T(r'Exceedances of daily losses over their 95\% quantile, whole samples; raw losses and GARCH-standardised losses (in-sample ARMA-GARCH parameters)',
      r'Depășiri ale pierderilor zilnice peste cuantila lor de 95\%, eșantioanele întregi; pierderi brute și pierderi standardizate prin GARCH (parametri ARMA-GARCH din eșantion)')],
    h='0.48\\textheight')

interp(('the extremal index', 'indicelui extremal'), [
    T(r'Raw losses: $\hat\theta$ = @{ex.sp500.r} (S\&P 500), @{ex.bet.r} (BET), @{ex.eurron.r} (EUR/RON): extremes come in clusters of two to eight days', r'Pierderi brute: $\hat\theta$ = @{ex.sp500.r} (S\&P 500), @{ex.bet.r} (BET), @{ex.eurron.r} (EUR/RON): extremele vin în grupuri de două pînă la opt zile'),
    T(r'After filtering: @{ex.sp500.f}, @{ex.dax.f}, @{ex.btc.f} for the S\&P 500, DAX and Bitcoin: GARCH removes most of the clustering, as McNeil and Frey assume', r'După filtrare: @{ex.sp500.f}, @{ex.dax.f}, @{ex.btc.f} pentru S\&P 500, DAX și Bitcoin: GARCH elimină cea mai mare parte a grupării, cum presupun McNeil și Frey'),
    T(r'EUR/RON stays clustered (@{ex.eurron.f}) and BET partly (@{ex.bet.f}): a managed exchange rate and a thin market have dependence that GARCH does not capture', r'EUR/RON rămîne grupat (@{ex.eurron.f}) și BET parțial (@{ex.bet.f}): un curs administrat și o piață mică au o dependență pe care GARCH nu o surprinde'),
    T('With fixed in-sample parameters the filter is imperfect after the estimation period: part of the remaining clustering is drift', 'Cu parametri ficși din eșantion, filtrul este imperfect după perioada de estimare: o parte din gruparea rămasă este derivă')])

D.frame(T('Conformal calibration of VaR', 'Calibrarea conformală a VaR'), items(
    (T(r'Split conformal quantiles guarantee coverage under exchangeability (Chapter 13); returns are not exchangeable, so the guarantee fails', r'Cuantilele conformale split garantează acoperirea sub interschimbabilitate (Capitolul 13); randamentele nu sînt interschimbabile, deci garanția nu mai este valabilă'), []),
    (T(r'\textbf{Adaptive conformal inference} \refGC: forecast at level $\alpha_t$ and update $\alpha_{t+1} = \alpha_t + \gamma(\alpha - \mathrm{err}_t)$, $\mathrm{err}_t = \mathbf 1\{y_t < q_t(\alpha_t)\}$', r'\textbf{Inferența conformală adaptivă} \refGC: prognozăm la nivelul $\alpha_t$ și actualizăm $\alpha_{t+1} = \alpha_t + \gamma(\alpha - \mathrm{err}_t)$, $\mathrm{err}_t = \mathbf 1\{y_t < q_t(\alpha_t)\}$'),
     [T(r'deterministic guarantee: $\big|T^{-1}\sum_t\mathrm{err}_t - \alpha\big| \le \dfrac{\max(\alpha_1, 1 - \alpha_1) + \gamma}{\gamma T}$ for \textbf{any} sequence of returns', r'garanție deterministă: $\big|T^{-1}\sum_t\mathrm{err}_t - \alpha\big| \le \dfrac{\max(\alpha_1, 1 - \alpha_1) + \gamma}{\gamma T}$ pentru \textbf{orice} șir de randamente'),
      T('long-run frequency only: no conditional calibration, no statement about ES', 'doar frecvența pe termen lung: nici calibrare condiționată, nici vreo afirmație despre ES')]),
    T(r'Further reading: conformal recalibration of extreme tail quantiles under dependence \refCO', r'Lectură suplimentară: recalibrarea conformală a cuantilelor extreme sub dependență \refCO')), 'small')

chart(T('Adaptive conformal correction of VaR 1\\%', 'Corecția conformală adaptivă a VaR 1\\%'), 'ats_ch9_conformal', 'ATS_ch9_conformal', [
    T(r'GARCH-N VaR 1\% (rolling 1000-day window, re-estimated every 250 days) from 2016, and its ACI correction with $\gamma$ = 0.005; rolling 250-day hit rates',
      r'VaR 1\% GARCH-N (fereastră mobilă de 1000 de zile, reestimat la fiecare 250 de zile) din 2016 și corecția ACI cu $\gamma$ = 0,005; ratele de depășire pe 250 de zile')],
    h='0.5\\textheight')

interp(('the conformal correction', 'corecției conformale'), [
    T(r'BET: GARCH-N hits @{cf.bet.b}\% of @{cf.bet.T} days (Kupiec $p$ @{cf.bet.kb}); with ACI @{cf.bet.a}\% ($p$ = @{cf.bet.ka}), conditional coverage $p$ = @{cf.bet.ca}', r'BET: GARCH-N are depășiri în @{cf.bet.b}\% din @{cf.bet.T} de zile (Kupiec $p$ @{cf.bet.kb}); cu ACI @{cf.bet.a}\% ($p$ = @{cf.bet.ka}), acoperire condiționată $p$ = @{cf.bet.ca}'),
    T(r'Bitcoin: @{cf.btc.b}\% to @{cf.btc.a}\%; the rolling hit rate is not smoothed: its maximum rises from @{cf.btc.rb}\% to @{cf.btc.ra}\% after over-correction', r'Bitcoin: de la @{cf.btc.b}\% la @{cf.btc.a}\%; rata mobilă nu se netezește: maximul crește de la @{cf.btc.rb}\% la @{cf.btc.ra}\% după o supracorecție'),
    T(r'ACI fixes the frequency, not the dynamics: the adapted level can go below zero (VaR then infinite) after a run of quiet days', r'ACI corectează frecvența, nu dinamica: nivelul adaptat poate coborî sub zero (VaR devine atunci infinit) după un șir de zile liniștite'),
    T('A useful wrapper for a regulator\'s count; a calibrated model is still needed for DQ and for ES', 'Un înveliș util pentru numărătoarea supraveghetorului; pentru DQ și pentru ES este în continuare nevoie de un model calibrat')])

D.recap(('Extremes and conformal calibration', 'extreme și calibrare conformală'), [
    T('Extremes cluster; filtering removes most clustering for liquid markets, not for managed rates', 'Extremele se grupează; filtrarea elimină cea mai mare parte a grupării pe piețele lichide, nu și pentru cursurile administrate'),
    T('ACI guarantees the long-run hit frequency for any data, nothing more', 'ACI garantează frecvența pe termen lung a depășirilor pentru orice date, nimic mai mult'),
    T('Both are corrections of a model, not replacements for one', 'Ambele sînt corecții ale unui model, nu înlocuitori ai lui')])

# =============================================================================
# 10. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Do semiparametric (VaR, ES) models beat location--scale models out of sample once estimation is repeated, and is the advantage concentrated in crises?', 'Bat modelele semiparametrice (VaR, ES) modelele de tip poziție--scală în afara eșantionului atunci cînd estimarea se repetă și este avantajul concentrat în crize?'),
     [T(r'formal: $H_0$: equal expected FZ0 loss of GAS-1F and GARCH-EDF with rolling re-estimation, on pre-registered assets, periods and levels', r'formal: $H_0$: pierdere FZ0 așteptată egală pentru GAS-1F și GARCH-EDF cu reestimare mobilă, pe active, perioade și niveluri preînregistrate'),
      T('falsified by a significant GW statistic in the pre-registered crisis windows, robust across $\\alpha$ = 1\\%, 2.5\\%, 5\\%', 'infirmată de o statistică GW semnificativă în ferestrele de criză preînregistrate, robustă pentru $\\alpha$ = 1\\%, 2,5\\%, 5\\%')]),
    (T('Why it matters: Basel requires ES models; the PZC evidence comes from fixed parameters and four indices', 'De ce contează: Basel cere modele ES; evidența PZC provine din parametri ficși și patru indici'),
     [T(r'literature to start from: \refPZC, \refTayB, \refNZ, \refDB', r'literatura de pornire: \refPZC, \refTayB, \refNZ, \refDB')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers since 2017 that compare dynamic ES models out of sample with FZ losses; give DOIs.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează articole recenzate din 2017 încoace care compară modele dinamice pentru ES în afara eșantionului cu pierderi FZ; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Under which data-generating processes should a one-factor GAS model beat GARCH with empirical innovations for ES 2.5\%?}', r'\textbf{ipoteza}: \aiprompt{În ce procese generatoare ar trebui ca un model GAS cu un factor să bată GARCH cu inovații empirice pentru ES 2,5\%?}'),
      T(r'\textbf{code and replication}: ask for the GAS-1F recursion, then reproduce a published number first (PZC, Table 8: @{pp5.fz1f})', r'\textbf{cod și replicare}: cereți recursia GAS-1F, apoi reproduceți întîi o cifră publicată (PZC, Tabelul 8: @{pp5.fz1f})'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee: list the ways an FZ0 ranking could be an artefact of the sample, the level or the starting values.}', r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră felurile în care o ordonare FZ0 poate fi un artefact al eșantionului, al nivelului sau al valorilor de pornire.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The loss is consistent for the target: no ``average ES error\'\', no MSE of VaR forecasts', 'Pierderea este consistentă pentru țintă: fără „eroarea medie a ES”, fără MSE pentru prognozele VaR'),
    T('The convention is right: VaR 1\\% is minus the 1\\% quantile of returns, never ``VaR 99\\%\'\'; signs of $v$ and $e$ are consistent', 'Convenția este corectă: VaR 1\\% este cuantila de 1\\% a randamentelor cu semn schimbat, niciodată „VaR 99\\%”; semnele lui $v$ și $e$ sînt consecvente'),
    T('Forecasts use only information available at $t - 1$; the estimation window and re-estimation scheme are stated', 'Prognozele folosesc doar informația disponibilă la $t - 1$; fereastra de estimare și schema de reestimare sînt precizate'),
    T('Rankings are reported with DM or MCS uncertainty and checked on a Murphy diagram', 'Ordonările se raportează cu incertitudinea DM sau MCS și se verifică pe o diagramă Murphy')), 'small')

chart(T('Mini-case: is there a best ES model?', 'Mini studiu de caz: există un cel mai bun model ES?'), 'ats_ch9_ai_case', 'ATS_ch9_comparison', [
    T(r'@{ai.n} cells: five assets $\times$ two levels (2.5\%, 5\%) $\times$ up to three periods (whole, before 2020, from 2020); left: the model with the lowest FZ0 loss; right: size of the 90\% MCS',
      r'@{ai.n}@{ai.nde} celule: cinci active $\times$ două niveluri (2,5\%, 5\%) $\times$ pînă la trei perioade (toată, înainte de 2020, din 2020); stînga: modelul cu cea mai mică pierdere FZ0; dreapta: mărimea MCS de 90\%'),
    T(r'@{ai.nw} different winners; GARCH-Skt wins @{ai.skt} cells, GAS-1F @{ai.fz1}; MCS sizes from @{ai.smin} to @{ai.smax}, median @{ai.smed}; GAS-1F is in the MCS in @{ai.fzin} cells: an AI summary that names ``the best ES model\'\' is wrong',
      r'@{ai.nw} cîștigători diferiți; GARCH-Skt cîștigă @{ai.skt} celule, GAS-1F @{ai.fz1}; mărimea MCS între @{ai.smin} și @{ai.smax}, mediana @{ai.smed}; GAS-1F este în MCS în @{ai.fzin}@{ai.fzde} celule: un rezumat AI care numește „cel mai bun model ES” greșește')],
    h='0.44\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{ES models for Central and Eastern European markets under rolling re-estimation}: replicate first, then extend', r'\textbf{Modele ES pentru piețele din Europa Centrală și de Est cu reestimare mobilă}: întîi replicare, apoi extindere'),
     [T(r'replicate: PZC Table 8 and Table S5 for the S\&P 500 (GAS-1F @{pp5.fz1f} and @{pp25.fz1f}) and the EM design with VaR 1\%', r'replicați: Tabelele 8 și S5 din PZC pentru S\&P 500 (GAS-1F @{pp5.fz1f} și @{pp25.fz1f}) și designul EM cu VaR 1\%'),
      T('extend: BET, WIG20, BUX, PX and EUR/RON; rolling re-estimation; joint (VaR, ES) regressions with VIX and the BNR rate; ACI as a wrapper', 'extindeți: BET, WIG20, BUX, PX și EUR/RON; reestimare mobilă; regresii comune (VaR, ES) cu VIX și dobînda BNR; ACI ca înveliș'),
      T('pre-register: samples, levels, models, windows, the stress periods and the MCS design', 'preînregistrați: eșantioanele, nivelurile, modelele, ferestrele, perioadele de criză și designul MCS')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('A risk forecast is a point forecast of a functional; judge it with a loss consistent for that functional', 'O prognoză de risc este o prognoză punctuală a unei funcționale; judecați-o cu o pierdere consistentă pentru acea funcțională'),
    T('VaR is elicitable, ES only with VaR; FZ0 is the scale-free choice for time series', 'VaR este elicitabil, ES doar împreună cu VaR; FZ0 este alegerea independentă de scală pentru serii de timp'),
    T('CAViaR and GAS-FZ models estimate the tail directly; their published rankings replicate, their published tests do not', 'Modelele CAViaR și GAS-FZ estimează direct coada; ordonările publicate se replică, testele publicate nu'),
    T('Backtests are moment tests with estimation risk; comparisons need DM, MCS and Murphy diagrams', 'Backtesting-ul înseamnă teste de momente cu risc de estimare; comparațiile cer DM, MCS și diagrame Murphy'),
    T('Horizon, model and estimation risk are larger than most reported confidence suggests', 'Riscul de orizont, de model și de estimare sînt mai mari decît sugerează majoritatea rezultatelor raportate')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T(r'Why does a non-convex level set rule out a strictly consistent loss for ES?', r'De ce exclude o mulțime de nivel neconvexă existența unei pierderi strict consistente pentru ES?'),
        T('Which choice of $(G_1, G_2)$ gives FZ0, and what does zero homogeneity buy?', 'Ce alegere a lui $(G_1, G_2)$ dă FZ0 și ce aduce omogenitatea de grad zero?'),
        T('Why is the DQ test with a VaR regressor more powerful than Christoffersen\'s test?', 'De ce este testul DQ cu regresorul VaR mai puternic decît testul lui Christoffersen?'),
        T('Why does a fixed estimation window inflate the size of the Kupiec test?', 'De ce crește o fereastră fixă de estimare mărimea testului Kupiec?'),
        T('When does $\\sqrt{10}$ scaling overstate the 10-day VaR?', 'Cînd supraestimează scalarea cu $\\sqrt{10}$ VaR pe 10 zile?'))),
    block(T('Next: Chapter 10', 'Urmează: Capitolul 10'), items(
        T('Long memory and rough volatility', 'Memorie lungă și rough volatility'),
        T('ARFIMA, fractional cointegration, rough volatility', 'ARFIMA, cointegrare fracționară, rough volatility'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: consistency of GPL quantile scores', 'Anexă: consistența scorurilor GPL pentru cuantile'), items(
    T(r'$\E_F S(x, Y) = \int_{-\infty}^x(1 - \alpha)(G(x) - G(y))\,dF(y) + \int_x^\infty \alpha(G(y) - G(x))\,dF(y)$', r'$\E_F S(x, Y) = \int_{-\infty}^x(1 - \alpha)(G(x) - G(y))\,dF(y) + \int_x^\infty \alpha(G(y) - G(x))\,dF(y)$'),
    T(r'Differentiate (Leibniz; the boundary terms vanish): $\dfrac{d}{dx}\E_F S(x, Y) = G\'(x)\big[(1 - \alpha)F(x) - \alpha(1 - F(x))\big] = G\'(x)(F(x) - \alpha)$', r'Derivăm (Leibniz; termenii de frontieră se anulează): $\dfrac{d}{dx}\E_F S(x, Y) = G\'(x)\big[(1 - \alpha)F(x) - \alpha(1 - F(x))\big] = G\'(x)(F(x) - \alpha)$'),
    T(r'$G\' \ge 0$: the derivative is $\le 0$ for $x < q_\alpha$ and $\ge 0$ for $x > q_\alpha$, so $q_\alpha$ minimises; strictly if $G$ is strictly increasing and $F$ has a unique $\alpha$-quantile', r'$G\' \ge 0$: derivata este $\le 0$ pentru $x < q_\alpha$ și $\ge 0$ pentru $x > q_\alpha$, deci $q_\alpha$ minimizează; strict dacă $G$ este strict crescătoare și $F$ are o singură cuantilă de nivel $\alpha$'),
    T(r'The same computation with $G(x) = x$ is the first-order condition of quantile regression', r'Același calcul cu $G(x) = x$ este condiția de ordinul întîi a regresiei cuantilice')), 'small')

D.frame(T('Appendix: FZ0, consistency and homogeneity', 'Anexă: FZ0, consistență și omogenitate'), items(
    T(r'Fix $e$; in $v$, FZ0 is $-\frac{1}{\alpha e}\big[\mathbf 1\{y \le v\}(v - y) - \alpha v\big]$ plus terms free of $v$: since $-1/(\alpha e) > 0$, a positive multiple of the pinball loss, minimised at $q_\alpha$', r'Fixăm $e$; în $v$, FZ0 este $-\frac{1}{\alpha e}\big[\mathbf 1\{y \le v\}(v - y) - \alpha v\big]$ plus termeni fără $v$: deoarece $-1/(\alpha e) > 0$, un multiplu pozitiv al pierderii pinball, minimizat în $q_\alpha$'),
    T(r'At $v = q_\alpha$: $\E\,L = \dfrac{c}{e} + \ln(-e) - 1$ with $c = v - \frac1\alpha\E[\mathbf 1\{Y \le v\}(v - Y)] = \E[Y \mid Y \le q_\alpha] = -\mathrm{ES}_\alpha$; the derivative $-c/e^2 + 1/e$ vanishes at $e = c$', r'La $v = q_\alpha$: $\E\,L = \dfrac{c}{e} + \ln(-e) - 1$ cu $c = v - \frac1\alpha\E[\mathbf 1\{Y \le v\}(v - Y)] = \E[Y \mid Y \le q_\alpha] = -\mathrm{ES}_\alpha$; derivata $-c/e^2 + 1/e$ se anulează în $e = c$'),
    T(r'Homogeneity: replacing $(y, v, e)$ by $(sy, sv, se)$, $s > 0$, changes FZ0 only by $\ln s$, the same for every forecast: loss differences are scale-free', r'Omogenitate: înlocuind $(y, v, e)$ cu $(sy, sv, se)$, $s > 0$, FZ0 se schimbă doar cu $\ln s$, la fel pentru orice prognoză: diferențele de pierdere nu depind de scală'),
    T(r'Joint minimisation over $(v, e)$ with $e \le v < 0$ therefore returns $(q_\alpha, -\mathrm{ES}_\alpha)$', r'Minimizarea comună în $(v, e)$ cu $e \le v < 0$ dă deci $(q_\alpha, -\mathrm{ES}_\alpha)$')), 'small')

D.references(bib(), per=13)

if __name__ == '__main__':
    finalize(D.write(V))
