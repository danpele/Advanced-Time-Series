r"""
build_chapter13.py -- Capitolul 13 (Foundation models și predicție conformală), EN + RO
=======================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_13/ch13_numbers.json (generate_all_charts.py). Nicio cifră nu este
scrisă de mînă (în afara exemplelor teoretice și a caracteristicilor publicate ale modelelor, citate ca atare).
TSA, Capitolul 11 (studiu individual) a prezentat Chronos, TimesFM, Moirai și Lag-Llama, testele zero-shot pe serii
românești, CRPS/WQL și contaminarea; aici: preantrenarea (date, tokenizare, patching, legi de scalare), familiile de
modele și alegerile de proiectare, zero-shot, fine-tuning și covariabile în context, metodologia benchmark-urilor și
testarea statistică pe multe serii, LLM pentru serii de timp și critica lor; predicția conformală (interschimbabilitate,
split conformal, CQR), metodele pentru date dependente (ponderare, EnbPI, ACI, PID conformal), diagnosticarea acoperirii
și calibrarea intervalelor produse de foundation models.
Ieșire:
  EN/Courses/chapter13_foundation_models_conformal.tex
  RO/Cursuri/capitol13_foundation_models_conformal.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_13/generate_all_charts.py
  python3 latex/build_chapter13.py && python3 latex/ats_build.py compile 13
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch13_common import REFS, QLURL, T, V2, day, month, bib, finalize, load, minus_fix   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(13, 'lecture', refs=REFS)
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
    'gammerman': ('ch13_gammerman_2018.jpg', C + 'Alexander-Gammerman-professor-at-RHUL.jpg',
                  FOTO + ': Jaguar224 (2018); CC BY-SA 4.0; Wikimedia Commons'),
    'holloway': ('ch13_royal_holloway.jpg', C + "Founder's_Building,_Royal_Holloway,_University_of_London_-_Diliff.jpg",
                 FOTO + ': Diliff (2015); CC BY-SA 3.0; Wikimedia Commons'),
    'candes': ('ch13_candes_2012.jpg', C + 'Emmanuel_Cand' + chr(92) + '%C3' + chr(92) + '%A8s.jpg',
               FOTO + ': Renate Schmid, MFO (2012); CC BY-SA 2.0 de; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


def pv(key, x, d=3):
    """p-value with its relation sign: '= 0.012' or '< 0.001' (written after $p$)."""
    if x < 10 ** (-d):
        V.raw(key, '$<$ ' + n(10 ** (-d), d))
    else:
        V.raw(key, '= ' + n(x, d))


def pct(key, x, d=0):
    P(key, 100 * x, d)


# =============================================================================
# CIFRE
# =============================================================================
FMK = {'Chronos-Bolt small': 'bolt', 'Chronos-2': 'c2', 'TimesFM 2.5': 'tf', 'TiRex': 'tx'}
t = N['tokens']
V.raw('tok.n', str(t['n']))
V.raw('tok.first', day(t['first']))
V.raw('tok.last', day(t['last']))
V.int('tok.s', round(t['scale']))
P('tok.w', t['width'], 1)
P('tok.err', t['maxerr'], 1)
pct('tok.clip', t['clip_share'], 0)
pct('tok.jerr', t['jump_err'], 0)
ld = N['load']
V.raw('data.load_end', day(ld['last']))
V.raw('ld.first', day(ld['first']))
V.raw('ld.last', day(ld['last']))
V.raw('ld.n', str(ld['n_days']))
for k, kk in (('Chronos-2', 'c2'), ('expert ARX', 'arx'), ('TiRex', 'tx'), ('Chronos-Bolt small', 'bolt'), ('TimesFM 2.5', 'tf'),
              ('DLinear', 'dl'), ('N-BEATS', 'nb'), ('weekly naive', 'naive')):
    P(f'ld.mae.{kk}', ld['mae'][k], 3)
for k, kk in (('Chronos-2', 'c2'), ('Chronos-Bolt small', 'bolt'), ('TimesFM 2.5', 'tf'), ('expert ARX', 'arx')):
    pct(f'ld.cov.{kk}', ld['cov80'][k], 1)
P('ld.dm.c2', ld['dm']['Chronos-2']['t'], 2)
pv('ld.dmp.c2', ld['dm']['Chronos-2']['p'])
V.raw('ld.mcs', V2('\\{' + ', '.join(ld['mcs']) + '\\}', '\\{' + ', '.join(ld['mcs']) + '\\}'))
cv = N['covariates']
V.raw('cv.nh', str(cv['n_hol']))
for lab, kk in (('univariate', 'u'), ('+ calendar', 'c'), ('+ calendar + temperature', 't')):
    P(f'cv.{kk}.hol', cv['mae'][lab]['hol'], 3)
    P(f'cv.{kk}.oth', cv['mae'][lab]['other'], 3)
P('cv.dmc', cv['dm_cal']['t'], 2)
pv('cv.dmcp', cv['dm_cal']['p'])
P('cv.dmt', cv['dm_tmp']['t'], 2)
pv('cv.dmtp', cv['dm_tmp']['p'])
zs = N['zeroshot']
P('zs.var', -zs['BET daily log return (%)']['q01'], 2)
inf = N['inflation']
V.raw('inf.first', month(inf['first']))
V.raw('inf.last', month(inf['last']))
V.raw('data.hicp_end', month(inf['end']))
for k, kk in (('AR(p)', 'ar'), ('Chronos-2', 'c2'), ('TimesFM 2.5', 'tf'), ('TiRex', 'tx')):
    P(f'inf.h1.{kk}', inf['rel'][k]['h1'], 3)
for k, kk in (('AR(p)', 'ar'), ('ETS', 'ets'), ('Chronos-2', 'c2'), ('TimesFM 2.5', 'tf'), ('TiRex', 'tx'), ('Chronos-Bolt small', 'bolt'),
              ('DLinear', 'dl'), ('N-BEATS', 'nb'), ('Chronos-2 cross-learning', 'cl')):
    P(f'inf.h12.{kk}', inf['rel'][k]['h12'], 3)
for k, kk in (('Chronos-2', 'c2'), ('TimesFM 2.5', 'tf'), ('TiRex', 'tx'), ('ETS', 'ets')):
    P(f'inf.crps.{kk}', inf['crps_rel'][k], 3)
ri = N['ro_inflation']
for j, o in enumerate(ri['origins']):
    V.raw(f'ri.o{j + 1}', month(o))
    c2, ar = ri['fc'][f'Chronos-2|{j}'], ri['fc'][f'AR(p)|{j}']
    P(f'ri.a{j + 1}', c2['act12'], 1)
    P(f'ri.c{j + 1}', c2['med12'], 1)
    P(f'ri.r{j + 1}', ar['med12'], 1)
P('ri.c1l', ri['fc']['Chronos-2|0']['lo12'], 1)
P('ri.c1h', ri['fc']['Chronos-2|0']['hi12'], 1)
P('ri.peak', ri['peak'], 1)
V.raw('ri.pd', month(ri['peak_date']))
P('ri.last', ri['last'], 1)
V.raw('ri.ld', month(ri['last_date']))
mt = N['multiple']
V.raw('mt.model', mt['model'])
V.raw('mt.h', str(mt['h']))
for k in ('neg', 'rej', 'rej_fm', 'rej_ar', 'rej_holm', 'rej_bh'):
    V.raw('mt.' + k.replace('_', '').replace('rejholm', 'holm').replace('rejbh', 'bh'), str(mt[k]))
P('mt.rot', mt['ro_t'], 2)
pv('mt.rop', mt['ro_p'])
rv = N['rv']
for ser, kk in (('btc', 'b'), ('spx', 's')):
    r = rv[ser]
    V.raw(f'rv.{kk}.first', day(r['first']))
    V.raw(f'rv.{kk}.last', day(r['last']))
    V.int(f'rv.{kk}.n', r['n'])
    for k, k2 in FMK.items():
        P(f'rv.{kk}.{k2}', r['qlike'][k] / r['qlike']['HAR'], 3)
    V.raw(f'rv.{kk}.mcs', '\\{' + ', '.join(r['mcs']) + '\\}')
ct = N['contamination']
P('ct.l.c2a', ct['load']['Chronos-2'][0], 3)
P('ct.l.c2b', ct['load']['Chronos-2'][1], 3)
P('ct.l.tfa', ct['load']['TimesFM 2.5'][0], 3)
P('ct.l.tfb', ct['load']['TimesFM 2.5'][1], 3)
P('ct.b.c2a', ct['btc']['Chronos-2'][0], 3)
P('ct.b.c2b', ct['btc']['Chronos-2'][1], 3)
P('ct.b.txa', ct['btc']['TiRex'][0], 3)
P('ct.b.txb', ct['btc']['TiRex'][1], 3)
V.raw('ct.nl', str(ct['n_load'][1]))
V.raw('ct.nb', str(ct['n_btc'][1]))
sc = N['scaling']
pp = sc['params']
for k, kk in (('Chronos-Bolt tiny', 'tiny'), ('Chronos-Bolt base', 'base'), ('Chronos-2', 'c2'), ('TimesFM 2.5', 'tf'), ('TiRex', 'tx')):
    P(f'sc.p{kk}', pp[k], 0)
for k, kk in (('Chronos-Bolt tiny', 'tiny'), ('Chronos-Bolt base', 'base')):
    P(f'sc.l.{kk}', sc['load'][k], 3)
    P(f'sc.i.{kk}', sc['infl'][k], 3)
    P(f'sc.r.{kk}', sc['rv'][k], 3)
for k, kk in (('Chronos-2', 'c2'), ('TimesFM 2.5', 'tf'), ('TiRex', 'tx')):
    P(f'sc.l.{kk}', sc['load'][k], 3)
sp = N['split_coverage']
V.raw('sp.reps', str(sp['reps']))
for nn, kk in (('n50', '50'), ('n500', '500')):
    P(f'sp.m{kk}', sp[nn]['mean'], 3)
    P(f'sp.t{kk}', sp[nn]['theory_mean'], 3)
    P(f'sp.s{kk}', sp[nn]['sd'], 3)
    pct(f'sp.b{kk}', sp[nn]['p_below88'], 0)
cq = N['cqr']
P('cq.sc', cq['split']['cov'], 3)
P('cq.cc', cq['cqr']['cov'], 3)
P('cq.rc', cq['raw']['cov'], 3)
P('cq.sw', cq['split']['width'], 2)
P('cq.cw', cq['cqr']['width'], 2)
P('cq.rw', cq['raw']['width'], 2)
pct('cq.ratio', cq['split']['width'] / cq['cqr']['width'] - 1, 0)
P('cq.cmin', min(cq['cqr']['bins']), 3)
P('cq.smin', min(cq['split']['bins']), 3)
wt = N['weighted']
for m, kk in (('standard', 's'), ('weighted', 'w')):
    P(f'wt.{kk}c', wt[m]['cov'], 3)
    P(f'wt.{kk}min', wt[m]['min'], 2)
    P(f'wt.{kk}w', wt[m]['w'], 2)
ac = N['aci']
V.raw('ac.sp.first', day(ac['sp500']['first']))
for nm, kk in (('sp500', 'sp'), ('bet', 'bet'), ('nvda', 'nv')):
    for m, mm in (('static', 'st'), ('rolling', 'ro'), ('aci', 'ac')):
        P(f'ac.{kk}.{mm}', ac[nm][m]['cov'], 3)
P('ac.sp.stmin', ac['sp500']['static']['lc_min'], 3)
P('ac.sp.stmax', ac['sp500']['static']['lc_max'], 3)
P('ac.sp.acmin', ac['sp500']['aci']['lc_min'], 3)
P('ac.sp.acmax', ac['sp500']['aci']['lc_max'], 3)
pv('ac.sp.stcc', ac['sp500']['static']['cc'])
pv('ac.sp.accc', ac['sp500']['aci']['cc'])
ag = N['aci_gamma']
for g, kk in (('0.001', '1'), ('0.005', '2'), ('0.05', '3')):
    P(f'ag.m{kk}', ag[g]['miss'], 4)
    P(f'ag.b{kk}', ag[g]['bound'], 4)
V.raw('ag.T', str(ag['0.005']['T']))
P('ag.lo3', ag['0.05']['amin'], 2)
P('ag.hi3', ag['0.05']['amax'], 2)
pct('ag.inf3', ag['0.05']['inf'], 1)
cc = N['condcov']
for m, mm in (('static', 'st'), ('aci', 'ac')):
    P(f'cc.{mm}0', cc[m][0], 3)
    P(f'cc.{mm}2', cc[m][2], 3)
    P(f'cc.{mm}3', cc[m][3], 3)
pdd = N['pid']
V.raw('pd.first', day(pdd['first']))
for m, mm in (('static', 'st'), ('rolling', 'ro'), ('aci', 'ac'), ('qt', 'qt'), ('pid', 'pid'), ('enbpi', 'en')):
    P(f'pd.{mm}', pdd[m]['cov'], 3)
    P(f'pd.w{mm}', pdd[m]['width'], 2)
P('pd.lst', pdd['static']['lc_min'], 3)
P('pd.lpid', pdd['pid']['lc_min'], 3)
fc = N['fm_calib']
for tk, kk in (('load', 'l'), ('btc', 'b'), ('infl', 'i'), ('bet', 'r')):
    raws = [v['raw'] for v in fc[tk].values()]
    pct(f'fc.{kk}.lo', min(raws), 0)
    pct(f'fc.{kk}.hi', max(raws), 0)
c80 = [v['c80'] for t_ in fc.values() for v in t_.values()]
c95 = [v['c95'] for t_ in fc.values() for v in t_.values()]
pct('fc.c80lo', min(c80), 0)
pct('fc.c80hi', max(c80), 0)
pct('fc.c95lo', min(c95), 1)
wr = [v['wratio'] for t_ in fc.values() for v in t_.values()]
P('fc.wlo', min(wr), 2)
P('fc.whi', max(wr), 2)
pct('fc.c95hi', max(c95), 1)
fv = N['fm_var']
V.raw('fv.first', day(fv['bet']['first']))
V.int('fv.n', fv['bet']['n'])
for nm, kk in (('bet', 'b'), ('sp500', 's')):
    r1 = fv[nm]['0.01']
    pct(f'fv.{kk}.g', r1['GARCH-t']['hit'], 2)
    pct(f'fv.{kk}.c', r1['Chronos-2 raw']['hit'], 2)
    pct(f'fv.{kk}.a', r1['Chronos-2 + ACI']['hit'], 2)
    pct(f'fv.{kk}.t', r1['TimesFM 2.5 + conformal']['hit'], 2)
    pv(f'fv.{kk}.gk', r1['GARCH-t']['kup'])
    pv(f'fv.{kk}.ck', r1['Chronos-2 raw']['kup'])
    pv(f'fv.{kk}.ak', r1['Chronos-2 + ACI']['kup'])
    pv(f'fv.{kk}.acc', r1['Chronos-2 + ACI']['cc'])
    P(f'fv.{kk}.adm', r1['Chronos-2 + ACI']['dm'], 2)
    P(f'fv.{kk}.bdm', r1['Chronos-Bolt small + conformal']['dm'], 2)
ai = N['ai_case']
V.raw('ai.reps', str(ai['reps']))
V.raw('ai.k', str(ai['k']))
V.raw('ai.y', str(ai['years']))
pct('ai.win', ai['win'], 1)
pct('ai.lose', ai['lose'], 1)
P('ai.t', ai['full_t'], 2)
pv('ai.p', ai['full_p'])
minus_fix(V)

TB = '>{\\raggedright\\arraybackslash}'

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: can one pretrained model forecast series it has never seen, and how do we turn any forecast, pretrained or not, into intervals whose coverage we can guarantee or at least control?',
       r'\textbf{Întrebarea}: poate un model preantrenat să prognozeze serii pe care nu le-a văzut niciodată și cum transformăm orice prognoză, preantrenată sau nu, în intervale a căror acoperire o putem garanta sau măcar controla?'),
     [T('two halves of one problem: point and quantile accuracy (foundation models), then honest uncertainty (conformal prediction)',
        'două jumătăți ale aceleiași probleme: acuratețea punctuală și a cuantilelor (foundation models), apoi o incertitudine onestă (predicția conformală)')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('pretraining: data, tokens, patches, scaling laws; model families and design choices',
        'preantrenarea: date, token-uri, patch-uri, legi de scalare; familiile de modele și alegerile de proiectare'),
      T('benchmarks, contamination and testing across many series; evidence on Romanian and EU data; LLMs and their critique',
        'benchmark-uri, contaminare și testare pe multe serii; dovezi pe date românești și europene; LLM și critica lor'),
      T('conformal prediction: exchangeability, split conformal, CQR, the limits of conditional coverage',
        'predicția conformală: interschimbabilitate, split conformal, CQR, limitele acoperirii condiționate'),
      T('dependent data: weights, EnbPI, ACI, conformal PID; diagnostics; calibrating foundation-model intervals and VaR',
        'date dependente: ponderi, EnbPI, ACI, PID conformal; diagnosticare; calibrarea intervalelor produse de foundation models și VaR')]),
    T('We build on TSA, Chapter 11 (Chronos, TimesFM, Moirai, zero-shot tests, CRPS and WQL), on Chapter 1 (scoring rules, DM, MCS), Chapter 9 (VaR backtests, ACI for VaR) and Chapter 12 (deep architectures); Seminar 13 comes before this lecture',
      'Pornim de la TSA, Capitolul 11 (Chronos, TimesFM, Moirai, teste zero-shot, CRPS și WQL), de la Capitolul 1 (reguli de scor, DM, MCS), Capitolul 9 (backtesting VaR, ACI pentru VaR) și Capitolul 12 (arhitecturi deep); Seminarul 13 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Explain how a time series foundation model is pretrained: corpus, scaling, tokenisation or patching, output head and loss',
      'Explicați cum se preantrenează un foundation model pentru serii de timp: corpus, scalare, tokenizare sau patching, stratul de ieșire și funcția de pierdere'),
    T('Compare model families and choose between zero-shot use, fine-tuning and in-context covariates',
      'Comparați familiile de modele și alegeți între folosirea zero-shot, fine-tuning și covariabilele în context'),
    T('Design a benchmark without leakage or contamination and test differences across many series with corrections for multiplicity',
      'Proiectați un benchmark fără scurgere de informație sau contaminare și testați diferențele pe multe serii cu corecții pentru testarea multiplă'),
    T('Prove the coverage of split conformal and CQR, and state what conformal prediction cannot guarantee',
      'Demonstrați acoperirea metodelor split conformal și CQR și precizați ce nu poate garanta predicția conformală'),
    T('Apply weighted conformal, EnbPI, ACI and conformal PID to dependent data, diagnose coverage and calibrate foundation-model intervals',
      'Aplicați predicția conformală ponderată, EnbPI, ACI și PID conformal pe date dependente, diagnosticați acoperirea și calibrați intervalele produse de foundation models')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Foundation models: \refAns; \refAnsB; \refDas; \refWoo; \refAue; benchmarks: \refAks; \refShc', r'Foundation models: \refAns; \refAnsB; \refDas; \refWoo; \refAue; benchmark-uri: \refAks; \refShc'),
     [T(r'Conformal prediction: \refVGSb; \refAB; \refRPC; \refBar; \refGC; \refACT; \refXX', r'Predicție conformală: \refVGSb; \refAB; \refRPC; \refBar; \refGC; \refACT; \refXX'),
      T(r'Critique and evaluation: \refTan; \refHAB; survey of forecasting practice: \refPet', r'Critică și evaluare: \refTan; \refHAB; sinteză despre practica prognozei: \refPet')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_13}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_13}'),
     [T(r'open checkpoints on a CPU: \texttt{chronos-forecasting} (Chronos-Bolt, Chronos-2), \texttt{timesfm} (TimesFM 2.5), \texttt{tirex-ts} (TiRex); conformal methods, DM, MCS and backtests written in \texttt{numpy}',
        r'modele deschise pe un CPU: \texttt{chronos-forecasting} (Chronos-Bolt, Chronos-2), \texttt{timesfm} (TimesFM 2.5), \texttt{tirex-ts} (TiRex); metodele conformale, DM, MCS și backtesting-ul scrise în \texttt{numpy}')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter13_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter13_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{3.9cm}' + TB + 'p{5.3cm}' + TB + 'p{2.9cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Sample}', r'\textbf{Eșantionul}'),
    [T('Romanian electricity load, hourly', 'Consumul de electricitate al României, orar') + ' & ' + T('Energy-Charts (ENTSO-E transparency data)', 'Energy-Charts (date de transparență ENTSO-E)') + ' & 2022 -- @{data.load_end}',
     T('Bucharest air temperature, hourly', 'Temperatura aerului la București, orar') + ' & ' + T('Open-Meteo historical archive', 'arhiva istorică Open-Meteo') + ' & 2022 -- 2026',
     T('HICP annual inflation, 27 EU countries', 'Inflația anuală HICP, 27 de țări UE') + ' & ' + T('Eurostat, monthly', 'Eurostat, lunar') + ' & 2000 -- @{data.hicp_end}',
     T('Realised variance, 5-minute returns', 'Varianța realizată, randamente de 5 minute') + ' & ' + T(r'Bitcoin: Binance; S\&P 500: Oxford-Man \refOMI', r'Bitcoin: Binance; S\&P 500: Oxford-Man \refOMI') + ' & 2018 -- 2026; 2000 -- 2022',
     T(r'BET, S\&P 500, NVIDIA, daily', r'BET, S\&P 500, NVIDIA, zilnic') + ' & ' + T('EODHD daily closes', 'închideri zilnice EODHD') + ' & 2000 -- 2026'],
    size='scriptsize') + items(
    T('Returns are 100 times log differences; the realised variance is in squared percent; every forecast uses only data available at its origin',
      'Randamentele sînt diferențe logaritmice înmulțite cu 100; varianța realizată este în procente la pătrat; orice prognoză folosește doar datele disponibile la momentul emiterii ei')), 'footnotesize')

D.frame(T('Two lines of research that met', 'Două direcții de cercetare care s-au întîlnit'), two(
    ph('holloway', T("Royal Holloway, University of London: the Founder's Building", "Royal Holloway, Universitatea din Londra: Founder's Building"), h='0.36\\textheight'),
    items(T(r'1990s--2005: conformal prediction at Royal Holloway: Vovk, Gammerman and Shafer, rooted in Kolmogorov\'s algorithmic randomness \refVGS',
            r'Anii 1990--2005: predicția conformală la Royal Holloway: Vovk, Gammerman și Shafer, cu rădăcini în aleatorismul algoritmic al lui Kolmogorov \refVGS'),
          T(r'2002--2018: split (inductive) conformal \refPap; distribution-free regression \refLei; 2019: CQR \refRPC',
            r'2002--2018: split conformal (inductiv) \refPap; regresie fără ipoteze de distribuție \refLei; 2019: CQR \refRPC'),
          T(r'2021--2023: time series: ACI \refGC, EnbPI \refXX, conformal PID \refACT, beyond exchangeability \refBar',
            r'2021--2023: serii de timp: ACI \refGC, EnbPI \refXX, PID conformal \refACT, dincolo de interschimbabilitate \refBar'),
          T(r'2017--2025: Transformers \refVas, foundation models \refBom; for series: Lag-Llama, TimesFM, Moirai, Chronos (2023--2024), TiRex, Chronos-2 (2025)',
            r'2017--2025: Transformers \refVas, foundation models \refBom; pentru serii: Lag-Llama, TimesFM, Moirai, Chronos (2023--2024), TiRex, Chronos-2 (2025)')), '0.4', '0.58'), 'footnotesize')

D.frame(T('Known from TSA and new here', 'Cunoscut din TSA și elemente noi'), items(
    (T('Known (TSA, Chapter 11): zero-shot use of Chronos, TimesFM, Moirai and Lag-Llama; mean scaling and quantisation in brief; pinball loss, CRPS, WQL, MASE; first warnings about contamination',
       'Cunoscut (TSA, Capitolul 11): folosirea zero-shot a modelelor Chronos, TimesFM, Moirai și Lag-Llama; scalarea prin medie și cuantizarea, pe scurt; pierderea pinball, CRPS, WQL, MASE; primele avertismente despre contaminare'), []),
    (T('New: the research toolkit', 'Nou: instrumentele de cercetare'),
     [T('design choices and their consequences (range limits, quantile heads, patching, covariates in context), scaling evidence',
        'alegerile de proiectare și consecințele lor (limitele de domeniu, straturi de cuantile, patching, covariabile în context), dovezile de scalare'),
      T('benchmarks with pre-registered windows after the model releases, tests across many series with Holm and BH corrections',
        'benchmark-uri cu ferestre preînregistrate după lansarea modelelor, teste pe multe serii cu corecțiile Holm și BH'),
      T('conformal theory with proofs, its failure under dependence and the online methods that repair it, with coverage diagnostics',
        'teoria conformală cu demonstrații, eșecul ei sub dependență și metodele online care o repară, cu diagnosticarea acoperirii')]),
    T('Case studies: Ansari et al.\\ (2024), Tan et al.\\ (2024), Romano--Patterson--Candès (2019), Gibbs--Candès (2021), Barber et al.\\ (2023), Angelopoulos--Candès--Tibshirani (2023), Xu--Xie (2021), with the designs of the papers, on our data',
      'Studii de caz: Ansari et al.\\ (2024), Tan et al.\\ (2024), Romano--Patterson--Candès (2019), Gibbs--Candès (2021), Barber et al.\\ (2023), Angelopoulos--Candès--Tibshirani (2023), Xu--Xie (2021), cu designul din lucrări, pe datele noastre')), 'small')

# =============================================================================
# 1. PREANTRENAREA
# =============================================================================
D.section('Pretraining for time series', 'Preantrenarea pentru serii de timp')

D.frame(T('A foundation model as an amortised forecaster', 'Un foundation model ca prognozator amortizat'), items(
    (T(r'\textbf{Pretraining}: $\hat\theta = \arg\min_\theta \sum_{s \in \mathcal D_{\mathrm{pre}}}\sum_t \ell\big(y^{(s)}_{t+1:t+H}, f_\theta(y^{(s)}_{t-C+1:t})\big)$ over a corpus $\mathcal D_{\mathrm{pre}}$ of many series',
       r'\textbf{Preantrenarea}: $\hat\theta = \arg\min_\theta \sum_{s \in \mathcal D_{\mathrm{pre}}}\sum_t \ell\big(y^{(s)}_{t+1:t+H}, f_\theta(y^{(s)}_{t-C+1:t})\big)$ pe un corpus $\mathcal D_{\mathrm{pre}}$ format din multe serii'),
     [T(r'$C$: context length; $H$: horizon; $\ell$: a scoring rule (cross-entropy, pinball, negative log-likelihood)', r'$C$: lungimea contextului; $H$: orizontul; $\ell$: o regulă de scor (entropie încrucișată, pinball, log-verosimilitate negativă)'),
      T(r'the term \textbf{foundation model} \refBom: trained once on broad data, then adapted to many tasks', r'termenul \textbf{foundation model} \refBom: antrenat o singură dată pe date diverse, apoi adaptat la multe sarcini')]),
    (T(r'\textbf{Zero-shot} use: $\hat\theta$ fixed, the forecast for a new series is $f_{\hat\theta}(y_{T-C+1:T})$; no parameter is estimated on the target',
       r'Folosirea \textbf{zero-shot}: $\hat\theta$ fixat, prognoza pentru o serie nouă este $f_{\hat\theta}(y_{T-C+1:T})$; niciun parametru nu se estimează pe seria-țintă'),
     [T('the network performs the estimation step inside its forward pass: inference is amortised over the corpus', 'rețeaua face pasul de estimare în interiorul trecerii înainte: inferența este amortizată pe corpus')]),
    T('A global model of Chapter 12 is trained on the series of one data set; a foundation model on many data sets, frequencies and domains',
      'Un model global din Capitolul 12 este antrenat pe seriile unui singur set de date; un foundation model, pe multe seturi de date, frecvențe și domenii')), 'small')

D.frame(T('Structure shared across series', 'Structuri comune între serii'), items(
    (T('Shapes recur across domains: seasonal profiles, damped trends, level shifts, volatility clusters, intermittency', 'Formele se repetă între domenii: profiluri sezoniere, tendințe amortizate, salturi de nivel, grupări ale volatilității, intermitență'),
     [T('after scaling, a load curve and a web-traffic curve can look alike: the model learns a prior over shapes', 'după scalare, o curbă de consum și una de trafic web pot arăta la fel: modelul învață o distribuție a priori asupra formelor')]),
    (T('Not shared: the economics of a particular series (a tax change, a policy rule, a holiday calendar)', 'Elemente care nu se transferă: economia unei serii anume (o modificare de taxe, o regulă de politică, un calendar al sărbătorilor)'),
     [T('unless it is passed as a covariate in the context (Chronos-2) or learned by fine-tuning', 'decît dacă este transmisă ca o covariabilă în context (Chronos-2) sau învățată prin fine-tuning')]),
    (T('A no-free-lunch caveat: averaged over all processes no forecaster wins; pretraining helps only if the target resembles the corpus', 'O rezervă de tip „no free lunch”: în medie pe toate procesele niciun prognozator nu cîștigă; preantrenarea ajută doar dacă seria-țintă seamănă cu corpusul'),
     [T('financial returns are close to a martingale difference: little shape to transfer, much to overfit', 'randamentele financiare sînt aproape de o diferență de martingală: puțină formă de transferat, mult de supraajustat')])), 'small')

D.frame(T('Pretraining data: scale and composition', 'Datele de preantrenare: volum și compoziție'), items(
    (T(r'Chronos \refAns: public data sets plus two augmentations: \textbf{TSMixup} (convex mixtures of real series) and \textbf{KernelSynth} (series drawn from Gaussian processes with random composite kernels)',
       r'Chronos \refAns: seturi de date publice plus două augmentări: \textbf{TSMixup} (combinații convexe de serii reale) și \textbf{KernelSynth} (serii extrase din procese gaussiene cu nuclee compuse aleatoare)'), []),
    (T(r'TimesFM \refDas: about $10^{11}$ time points: Google Trends, Wikipedia page views, synthetic and public series; Moirai \refWoo: LOTSA, over 27 billion observations in nine domains',
       r'TimesFM \refDas: aproximativ $10^{11}$ momente de timp: Google Trends, accesări Wikipedia, serii sintetice și publice; Moirai \refWoo: LOTSA, peste 27 de miliarde de observații din nouă domenii'), []),
    (T(r'Toto \refCoh: observability metrics of a cloud provider, a corpus 4--10 times larger than those of earlier models; GIFT-Eval \refAks: a \textbf{non-leaking} pretraining set of about 230 billion points',
       r'Toto \refCoh: metrici de observabilitate ale unui furnizor cloud, un corpus de 4--10 ori mai mare decît al modelelor anterioare; GIFT-Eval \refAks: un set de preantrenare \textbf{fără scurgere} de circa 230 de miliarde de puncte'), []),
    T('Composition matters more than size for us: economic and financial series are a small, low-frequency share of every corpus',
      'Pentru noi compoziția contează mai mult decît volumul: seriile economice și financiare sînt o parte mică, de frecvență joasă, a oricărui corpus')), 'small')

D.frame(T('Tokenisation: from real values to a vocabulary', 'Tokenizarea: de la valori reale la un vocabular'), items(
    (T(r'Chronos \refAns: \textbf{mean scaling} $\tilde x_t = x_t/s$, $s = \frac1C\sum_{t \le C}|x_t|$ (context only), then \textbf{uniform bins} on $[-15, 15]$; 4096 tokens including special ones',
       r'Chronos \refAns: \textbf{scalarea prin medie} $\tilde x_t = x_t/s$, $s = \frac1C\sum_{t \le C}|x_t|$ (doar contextul), apoi \textbf{intervale egale} pe $[-15, 15]$; 4096 de token-uri, inclusiv cele speciale'),
     [T(r'the model is a language model (T5) trained with \textbf{cross-entropy}: the forecast is a categorical distribution over bins, sampled autoregressively',
        r'modelul este un model de limbaj (T5) antrenat cu \textbf{entropia încrucișată}: prognoza este o distribuție categorială pe intervale, eșantionată autoregresiv'),
      T('no notion of distance between tokens: neighbouring bins are as different as distant ones, unless the data teach otherwise', 'nicio noțiune de distanță între token-uri: intervalele vecine sînt la fel de diferite ca cele îndepărtate, dacă datele nu arată altceva')]),
    (T(r'Consequences: resolution $30s/4092$; values above $15s$ cannot be predicted; scale-invariant by construction', r'Consecințe: rezoluția $30s/4092$; valorile peste $15s$ nu pot fi prognozate; invarianță la scală prin construcție'), []),
    T(r'LLMTime \refGru: digits as text tokens; Lag-Llama \refRas: lagged values as features; patch models: no vocabulary at all',
      r'LLMTime \refGru: cifrele ca token-uri de text; Lag-Llama \refRas: valori decalate ca variabile; modelele cu patch-uri: fără vocabular')), 'small')

chart(T('The Chronos tokeniser on real data', 'Tokenizatorul Chronos pe date reale'), 'ats_ch13_tokens', 'ATS_ch13_pretraining', [
    T(r'Left: BET closes, @{tok.first} -- @{tok.last} ($C = @{tok.n}$), and a 64-bin quantisation (illustration); right: a context near 1 followed by a rise to 25 times that level',
      r'Stînga: închiderile BET, @{tok.first} -- @{tok.last} ($C = @{tok.n}$), și o cuantizare cu 64 de intervale (ilustrare); dreapta: un context în jurul valorii 1, urmat de o creștere pînă la un nivel de 25 de ori mai mare')],
    h='0.5\\textheight')

interp(('the tokeniser', 'tokenizatorului'), [
    T(r'BET: $s = @{tok.s}$ points, bin width @{tok.w} points, maximum quantisation error @{tok.err} points: negligible for prices, but a fixed share of the level',
      r'BET: $s = @{tok.s}$ puncte, lățimea intervalului @{tok.w} puncte, eroarea maximă de cuantizare @{tok.err} puncte: neglijabilă pentru prețuri, dar o pondere fixă din nivel'),
    T(r'Right panel: the scale is set by the context, so the path that rises beyond $15s$ is clipped: @{tok.clip}\% of the future steps are unreachable, the last one by @{tok.jerr}\%',
      r'Panoul din dreapta: scala este fixată de context, deci traiectoria care urcă peste $15s$ este tăiată: @{tok.clip}\% dintre pașii viitori sînt de neatins, ultimul cu o eroare de @{tok.jerr}\%'),
    T('Explosive series (bubbles, Chapter 16; hyperinflation) are outside the support of a mean-scaled vocabulary; Chronos-2 replaces it by an arcsinh transform and quantile outputs',
      'Seriile explozive (bule, Capitolul 16; hiperinflație) sînt în afara suportului unui vocabular scalat prin medie; Chronos-2 îl înlocuiește cu o transformare arcsinh și ieșiri sub formă de cuantile')])

D.frame(T('Patching and the output head', 'Patching și stratul de ieșire'), items(
    (T(r'\textbf{Patching} \refNie: split the context into patches of $P$ consecutive values, embed each patch as one token; attention costs $O((C/P)^2)$ instead of $O(C^2)$',
       r'\textbf{Patching} \refNie: contextul se împarte în patch-uri de $P$ valori consecutive, iar fiecare patch devine un token; atenția costă $O((C/P)^2)$ în loc de $O(C^2)$'),
     [T(r'TimesFM \refDas: input patches of 32, output patches of 128 (fewer autoregressive steps); Chronos-Bolt and Chronos-2: patches of 16; Moirai \refWoo: several patch sizes by frequency',
        r'TimesFM \refDas: patch-uri de intrare de 32, de ieșire de 128 (mai puțini pași autoregresivi); Chronos-Bolt și Chronos-2: patch-uri de 16; Moirai \refWoo: mai multe mărimi, după frecvență')]),
    (T('Output heads', 'Straturi de ieșire'),
     [T(r'categorical over bins (Chronos); \textbf{quantile head} trained by the pinball loss (Chronos-Bolt: 10\%--90\%; Chronos-2: 1\%--99\%; TimesFM 2.5, TiRex: deciles)',
        r'distribuție categorială pe intervale (Chronos); \textbf{strat de cuantile} antrenat cu pierderea pinball (Chronos-Bolt: 10\%--90\%; Chronos-2: 1\%--99\%; TimesFM 2.5, TiRex: decile)'),
      T(r'parametric: Student-$t$ (Lag-Llama \refRas), a mixture of distributions (Moirai)', r'parametric: Student-$t$ (Lag-Llama \refRas), un amestec de distribuții (Moirai)')]),
    T(r'Direct multi-step quantiles (one pass for $H$ steps) avoid error accumulation but give marginal, not joint, predictive distributions: path functionals (a maximum, a sum) need care',
      r'Cuantilele directe pe mai mulți pași (o singură trecere pentru $H$ pași) evită acumularea erorilor, dar dau distribuții predictive marginale, nu comune: funcționalele de traiectorie (un maxim, o sumă) cer atenție')), 'small')

D.frame(T('Scaling laws', 'Legi de scalare'), items(
    (T(r'Language models \refKap, \refHof: test loss falls as a power law, $L(N) \approx (N_c/N)^{\alpha_N}$, in the number of parameters $N$, data and compute, over orders of magnitude',
       r'Modelele de limbaj \refKap, \refHof: pierderea pe datele de test scade ca o lege de putere, $L(N) \approx (N_c/N)^{\alpha_N}$, în numărul de parametri $N$, în date și în calcul, pe mai multe ordine de mărime'), []),
    (T(r'Time series: decoder-only Transformers show the same power laws in parameters, data and compute \refEdw; the look-back length interacts with data size \refShi',
       r'Serii de timp: Transformers de tip decoder-only arată aceleași legi de putere în parametri, date și calcul \refEdw; lungimea contextului interacționează cu volumul datelor \refShi'),
     [T(r'out-of-distribution: the log-likelihood scales similarly in and out of distribution, but architecture matters; tweaks that help in distribution can reduce OOD scalability \refYao',
        r'în afara distribuției: log-verosimilitatea se scalează asemănător în și în afara distribuției, dar arhitectura contează; ajustările care ajută în distribuție pot reduce scalabilitatea OOD \refYao')]),
    T('A scaling law is a statement about average loss on the corpus distribution, not about one Romanian series; small models (TiRex, 35 million parameters) beat larger ones on public leaderboards \\refAue',
      'O lege de scalare este o afirmație despre pierderea medie pe distribuția corpusului, nu despre o serie românească anume; modele mici (TiRex, 35 de milioane de parametri) le întrec pe cele mari în clasamentele publice \\refAue')), 'small')

chart(T('Size and accuracy on our three tasks', 'Mărimea și acuratețea pe cele trei sarcini ale noastre'), 'ats_ch13_scaling', 'ATS_ch13_pretraining', [
    T(r'Losses relative to the task baseline: Romanian load (MAE / expert ARX, 2025--2026), EU inflation (MAE / random walk, $h = 12$, geometric mean over 27 countries), Bitcoin log RV (MSE / HAR); parameters counted in the loaded checkpoints',
      r'Pierderi relative la modelul de referință al fiecărei sarcini: consumul României (MAE / ARX expert, 2025--2026), inflația UE (MAE / mers aleator, $h = 12$, medie geometrică pe 27 de țări), log RV Bitcoin (MSE / HAR); parametrii numărați în modelele încărcate')],
    h='0.5\\textheight')

interp(('size against accuracy', 'relației dintre mărime și acuratețe'), [
    T(r'Chronos-Bolt family (@{sc.ptiny}--@{sc.pbase} M parameters): load @{sc.l.tiny} $\to$ @{sc.l.base}, inflation @{sc.i.tiny} $\to$ @{sc.i.base}, Bitcoin @{sc.r.tiny} $\to$ @{sc.r.base}',
      r'Familia Chronos-Bolt (@{sc.ptiny}--@{sc.pbase} M parametri): consum @{sc.l.tiny} $\to$ @{sc.l.base}, inflație @{sc.i.tiny} $\to$ @{sc.i.base}, Bitcoin @{sc.r.tiny} $\to$ @{sc.r.base}'),
    T(r'Across families size is not the ranking: Chronos-2 (@{sc.pc2} M) @{sc.l.c2} on load; TiRex (@{sc.ptx} M) @{sc.l.tx}; TimesFM 2.5 (@{sc.ptf} M) @{sc.l.tf}',
      r'Între familii, mărimea nu dă clasamentul: Chronos-2 (@{sc.pc2} M) @{sc.l.c2} la consum; TiRex (@{sc.ptx} M) @{sc.l.tx}; TimesFM 2.5 (@{sc.ptf} M) @{sc.l.tf}'),
    T('Within the Chronos-Bolt family the loss falls with size on all three tasks (one exception: mini on inflation); across families architecture, corpus and training recipe change together, so three tasks are not a scaling study',
      'În familia Chronos-Bolt pierderea scade odată cu mărimea pe toate cele trei sarcini (o excepție: mini la inflație); între familii, arhitectura, corpusul și rețeta de antrenare se schimbă împreună, deci trei sarcini nu fac un studiu de scalare')])

D.recap(('pretraining', 'preantrenarea'), [
    T('Pretraining amortises estimation over a corpus; zero-shot use runs the estimator inside one forward pass', 'Preantrenarea amortizează estimarea pe un corpus; folosirea zero-shot rulează estimatorul într-o singură trecere înainte'),
    T('Mean scaling and binning give scale invariance but a hard range; patching and quantile heads trade it for direct multi-step quantiles', 'Scalarea prin medie și intervalele dau invarianță la scală, dar un domeniu limitat; patching și straturile de cuantile le înlocuiesc cu cuantile directe pe mai mulți pași'),
    T('Scaling laws hold on average over corpora; on a given economic series, design and data matter more than size', 'Legile de scalare sînt valabile în medie pe corpusuri; pe o serie economică dată, proiectarea și datele contează mai mult decît mărimea')])

# =============================================================================
# 2. FAMILII DE MODELE
# =============================================================================
D.section('Model families and design choices', 'Familii de modele și alegeri de proiectare')

D.frame(T('The main open models', 'Principalele modele deschise'), table(
    TB + 'p{2.2cm}' + TB + 'p{3.4cm}' + TB + 'p{2.0cm}' + TB + 'p{3.9cm}',
    T(r'\textbf{Model}', r'\textbf{Modelul}') + ' & ' + T(r'\textbf{Architecture}', r'\textbf{Arhitectura}') + ' & ' + T(r'\textbf{Parameters}', r'\textbf{Parametri}') + ' & ' + T(r'\textbf{Output}', r'\textbf{Ieșirea}'),
    [r'Chronos \refAns & ' + T('T5 encoder--decoder on tokens', 'T5 encoder--decoder pe token-uri') + ' & 20--710 M & ' + T('categorical, sampled paths', 'categorială, traiectorii eșantionate'),
     r'Chronos-Bolt & ' + T('T5 on patches of 16', 'T5 pe patch-uri de 16') + ' & @{sc.ptiny}--@{sc.pbase} M & ' + T('9 quantiles, 10\\%--90\\%, 64 steps', '9 cuantile, 10\\%--90\\%, 64 de pași'),
     r'Chronos-2 \refAnsB & ' + T('encoder with group attention', 'encoder cu atenție de grup') + ' & @{sc.pc2} M & ' + T('21 quantiles, 1\\%--99\\%; covariates', '21 de cuantile, 1\\%--99\\%; covariabile'),
     r'TimesFM 2.5 \refDas & ' + T('decoder-only, patches', 'decoder-only, patch-uri') + ' & @{sc.ptf} M & ' + T('mean and deciles', 'media și decilele'),
     r'Moirai \refWoo & ' + T('masked encoder, any-variate attention', 'encoder mascat, atenție pe orice număr de variabile') + ' & 14--311 M & ' + T('mixture distribution', 'amestec de distribuții'),
     r'Lag-Llama \refRas & ' + T('decoder-only on lag features', 'decoder-only pe valori decalate') + ' & ' + T('small', 'mic') + ' & Student-$t$',
     r'MOMENT \refGos & ' + T('masked T5 encoder, multi-task', 'encoder T5 mascat, multi-sarcină') + ' & 40--385 M & ' + T('reconstruction; heads per task', 'reconstrucție; straturi pe sarcină'),
     r'TiRex \refAue & xLSTM & @{sc.ptx} M & ' + T('deciles', 'decile')],
    size='scriptsize') + items(
    T(r'Toto \refCoh (151 M, observability data) and Moirai 2.0 \refLiu are open as well; TimeGPT \refGar is reached only through a paid API', r'Toto \refCoh (151 M, date de observabilitate) și Moirai 2.0 \refLiu sînt și ele deschise; TimeGPT \refGar este accesibil doar printr-un API cu plată')), 'footnotesize')

D.frame(T('The Chronos family', 'Familia Chronos'), items(
    (T(r'\textbf{Chronos} \refAns: language-model recipe without changes; forecasts by sampling token paths; zero-shot results comparable to models trained on the target data (their Benchmark II)',
       r'\textbf{Chronos} \refAns: rețeta modelelor de limbaj fără modificări; prognoze prin eșantionarea traiectoriilor de token-uri; rezultate zero-shot comparabile cu modele antrenate pe datele-țintă (Benchmark II din lucrare)'), []),
    (T(r'\textbf{Chronos-Bolt}: patch inputs, a direct quantile decoder; much faster; context up to 2048, 64 steps; quantiles only between 10\% and 90\%',
       r'\textbf{Chronos-Bolt}: intrări sub formă de patch-uri, decodor direct de cuantile; mult mai rapid; context de pînă la 2048, 64 de pași; cuantile doar între 10\% și 90\%'),
     [T('a 95\\% interval or a VaR 1\\% cannot be read from its output: the request is clipped to the nearest trained level', 'un interval de 95\\% sau un VaR 1\\% nu se pot citi din ieșirea lui: cererea este tăiată la cel mai apropiat nivel antrenat')]),
    (T(r'\textbf{Chronos-2} \refAnsB: group attention shares information across the series of a group (variates, related series, covariates); \textbf{in-context learning} of covariate effects',
       r'\textbf{Chronos-2} \refAnsB: atenția de grup împarte informația între seriile unui grup (variabile, serii înrudite, covariabile); \textbf{învățare în context} a efectelor covariabilelor'),
     [T('trained largely on synthetic multivariate structures imposed on univariate series; context 8192; 21 quantiles from 1\\% to 99\\%; arcsinh scaling',
        'antrenat în mare parte pe structuri multivariate sintetice impuse unor serii univariate; context de 8192; 21 de cuantile de la 1\\% la 99\\%; scalare arcsinh')])), 'small')

D.frame(T('TimesFM, Moirai, Lag-Llama, MOMENT', 'TimesFM, Moirai, Lag-Llama, MOMENT'), items(
    (T(r'\textbf{TimesFM} \refDas: decoder-only, patches; output patch longer than input patch; trained on many granularities; version 2.5 adds a quantile head and long contexts',
       r'\textbf{TimesFM} \refDas: decoder-only, patch-uri; patch-ul de ieșire mai lung decît cel de intrare; antrenat pe multe frecvențe; versiunea 2.5 adaugă un strat de cuantile și contexte lungi'), []),
    (T(r'\textbf{Moirai} \refWoo: masked encoder; frequency-specific patch sizes; any-variate attention flattens multivariate inputs; mixture output (Student-$t$, log-normal, negative binomial)',
       r'\textbf{Moirai} \refWoo: encoder mascat; mărimi de patch specifice frecvenței; atenția pe orice număr de variabile aplatizează intrările multivariate; ieșire sub formă de amestec (Student-$t$, log-normală, binomială negativă)'),
     [T(r'Moirai 2.0 \refLiu: a decoder-only simplification, smaller and better on GIFT-Eval', r'Moirai 2.0 \refLiu: o simplificare decoder-only, mai mică și mai bună pe GIFT-Eval')]),
    (T(r'\textbf{Lag-Llama} \refRas: a LLaMA-type decoder whose tokens are vectors of lagged values at many seasonal lags; Student-$t$ head; strong after fine-tuning',
       r'\textbf{Lag-Llama} \refRas: un decodor de tip LLaMA ale cărui token-uri sînt vectori de valori decalate la multe decalaje sezoniere; strat Student-$t$; puternic după fine-tuning'), []),
    T(r'\textbf{MOMENT} \refGos: masked reconstruction on the Time series Pile; one encoder for forecasting, classification, anomaly detection and imputation',
      r'\textbf{MOMENT} \refGos: reconstrucție mascată pe Time series Pile; un singur encoder pentru prognoză, clasificare, detectarea anomaliilor și imputare')), 'small')

D.frame(T('Recurrent again, observability, and a closed API', 'Din nou recurente, observabilitate și un API închis'), items(
    (T(r'\textbf{TiRex} \refAue: an xLSTM (Chapter 12 recurrent cells with exponential gating and matrix memory) keeps a state across the context: state tracking for long horizons',
       r'\textbf{TiRex} \refAue: un xLSTM (celulele recurente din Capitolul 12, cu porți exponențiale și memorie matriceală) păstrează o stare de-a lungul contextului: urmărirea stării pe orizonturi lungi'),
     [T('contiguous patch masking (CPM) in training: the model learns to forecast with missing patches, i.e.\\ several steps without feedback',
        'mascarea patch-urilor contigue (CPM) la antrenare: modelul învață să prognozeze cu patch-uri lipsă, adică mai mulți pași fără reacție')]),
    (T(r'\textbf{Toto} \refCoh: decoder-only for multivariate observability metrics; the BOOM benchmark (2807 series); shows that domain composition of the corpus drives results',
       r'\textbf{Toto} \refCoh: decoder-only pentru metrici multivariate de observabilitate; benchmark-ul BOOM (2807 serii); arată că alcătuirea pe domenii a corpusului determină rezultatele'), []),
    (T(r'\textbf{TimeGPT} \refGar: closed weights and undisclosed corpus behind a paid API', r'\textbf{TimeGPT} \refGar: ponderi închise și corpus nedezvăluit, în spatele unui API cu plată'),
     [T('contamination cannot be audited; results are not reproducible if the service changes the model; data leave your institution', 'contaminarea nu poate fi verificată; rezultatele nu sînt reproductibile dacă serviciul schimbă modelul; datele ies din instituția dumneavoastră')])), 'small')

D.frame(T('Zero-shot, fine-tuning, in-context covariates', 'Zero-shot, fine-tuning, covariabile în context'), items(
    (T(r'\textbf{Zero-shot}: $f_{\hat\theta}(y_{T-C+1:T})$; no training, no tuning risk; the only choices are $C$ and the model',
       r'\textbf{Zero-shot}: $f_{\hat\theta}(y_{T-C+1:T})$; fără antrenare, fără riscul ajustării; singurele alegeri sînt $C$ și modelul'), []),
    (T(r'\textbf{Fine-tuning}: $\theta$ initialised at $\hat\theta$, a few gradient steps on the target data (all weights, or adapters such as LoRA)',
       r'\textbf{Fine-tuning}: $\theta$ pornește de la $\hat\theta$, cîțiva pași de gradient pe datele-țintă (toate ponderile sau adaptoare precum LoRA)'),
     [T('needs a validation split respecting time (Chapter 12); can forget the prior; with short economic series it rarely pays', 'cere o împărțire de validare care respectă timpul (Capitolul 12); poate uita distribuția a priori; pe serii economice scurte rareori merită')]),
    (T(r'\textbf{In-context covariates} (Chronos-2): pass past values of $x_t$ and future values of known regressors; the model infers their effect inside the forward pass',
       r'\textbf{Covariabile în context} (Chronos-2): se transmit valorile trecute ale lui $x_t$ și valorile viitoare ale regresorilor cunoscuți; modelul deduce efectul lor în timpul trecerii înainte'),
     [T('cross-learning: forecasting a batch of related series jointly (all 27 EU countries at one origin)', 'învățarea încrucișată: prognoza în comun a unui lot de serii înrudite (toate cele 27 de țări UE la aceeași origine)')]),
    T('Known future covariates must really be known at the origin: weather forecasts, not realised weather, unless an upper bound is the goal',
      'Covariabilele viitoare cunoscute trebuie să fie chiar cunoscute la origine: prognoze meteo, nu vremea realizată, cu excepția cazului în care se urmărește o limită superioară')), 'small')

chart(T('Four zero-shot forecasts from one model', 'Patru prognoze zero-shot cu același model'), 'ats_ch13_zeroshot', 'ATS_ch13_zero_shot', [
    T(r'Chronos-2 from the last origin of each data set: Romanian load (48 hours), Romanian HICP inflation (12 months), Bitcoin log realised variance and BET daily returns (22 days); bands 10--90\% and 1--99\%',
      r'Chronos-2 de la ultima origine a fiecărui set de date: consumul României (48 de ore), inflația HICP a României (12 luni), logaritmul varianței realizate Bitcoin și randamentele zilnice BET (22 de zile); benzi 10--90\% și 1--99\%')],
    h='0.55\\textheight')

interp(('the four forecasts', 'celor patru prognoze'), [
    T('Load: the daily and weekly shapes are continued with narrow bands: shape transfer at its best', 'Consumul: formele zilnice și săptămînale sînt continuate cu benzi înguste: transferul de formă în cel mai bun caz'),
    T('Inflation: a smooth path towards the recent level with bands that widen with the horizon: close to what an AR model with persistence would give', 'Inflația: o traiectorie netedă spre nivelul recent, cu benzi care se lărgesc cu orizontul: aproape de ce ar da un model AR persistent'),
    T('Log RV of Bitcoin: a weekly pattern (lower variance at weekends) around a level set by the context; returns: a flat median and a symmetric band, i.e.\\ an unconditional distribution', 'Log RV pentru Bitcoin: un tipar săptămînal (varianță mai mică la sfîrșit de săptămînă) în jurul unui nivel stabilit de context; randamentele: o mediană constantă și o bandă simetrică, adică o distribuție necondiționată'),
    T(r'Return bands from the 1\% and 99\% quantiles: Chronos-2 VaR 1\% for the next day is @{zs.var} (\% of value); Section 8 checks whether such numbers are calibrated',
      r'Benzile randamentelor din cuantilele de 1\% și 99\%: VaR 1\% Chronos-2 pentru ziua următoare este @{zs.var} (\% din valoare); secțiunea 8 verifică dacă astfel de cifre sînt calibrate')])

D.recap(('model families', 'familiile de modele'), [
    T('Families differ in input (tokens, patches, lags), architecture (encoder, decoder, recurrent) and output (categorical, quantiles, parametric)', 'Familiile diferă prin intrare (token-uri, patch-uri, decalaje), arhitectură (encoder, decoder, recurentă) și ieșire (categorială, cuantile, parametrică)'),
    T('Quantile range is a design constraint: deciles only, except Chronos-2', 'Domeniul cuantilelor este o constrîngere de proiectare: doar decile, cu excepția Chronos-2'),
    T('Zero-shot is the default; covariates in context and cross-learning are the new levers; closed APIs cannot be audited', 'Zero-shot este varianta implicită; covariabilele în context și învățarea încrucișată sînt noile pîrghii; API-urile închise nu pot fi verificate')])

# =============================================================================
# 3. BENCHMARK-URI ȘI TESTARE
# =============================================================================
D.section('Benchmarks, contamination and testing', 'Benchmark-uri, contaminare și testare')

D.frame(T('Benchmarks for pretrained models', 'Benchmark-uri pentru modelele preantrenate'), items(
    (T(r'\textbf{GIFT-Eval} \refAks: 23 data sets, over 144\,000 series, 177 million points, seven domains, ten frequencies, short to long horizons; a non-leaking pretraining set',
       r'\textbf{GIFT-Eval} \refAks: 23 de seturi de date, peste 144\,000 de serii, 177 de milioane de puncte, șapte domenii, zece frecvențe, orizonturi scurte și lungi; un set de preantrenare fără scurgere'), []),
    (T(r'\textbf{fev-bench} \refShc: 100 tasks in seven domains, 46 with covariates; win rates and skill scores with bootstrap confidence intervals',
       r'\textbf{fev-bench} \refShc: 100 de sarcini în șapte domenii, 46 cu covariabile; rate de cîștig și scoruri de abilitate cu intervale de încredere bootstrap'), []),
    (T(r'\textbf{Live benchmarks}: forecasts registered before the outcomes exist, e.g.\ TS-Arena \refMey and Impermanent \refGarB: the only design immune to contamination by construction',
       r'\textbf{Benchmark-uri live}: prognoze înregistrate înainte să existe rezultatele, de exemplu TS-Arena \refMey și Impermanent \refGarB: singurul design imun la contaminare prin construcție'), []),
    T(r'Classical references for what a fair comparison needs: M5 \refMak; pitfalls catalogued by \refHAB',
      r'Repere clasice pentru ce cere o comparație corectă: M5 \refMak; capcanele catalogate de \refHAB')), 'small')

D.frame(T('Aggregating scores across series', 'Agregarea scorurilor pe mai multe serii'), items(
    (T(r'Scale-free scores: MASE $= \frac{1}{H}\sum_h|y_{T+h} - \hat y_{T+h}| \big/ \frac{1}{T-m}\sum_t|y_t - y_{t-m}|$ \refHK; WQL $= 2\sum_{t,\tau}\rho_\tau(y_t - \hat q_{\tau,t})\big/\sum_t|y_t|$',
       r'Scoruri fără scală: MASE $= \frac{1}{H}\sum_h|y_{T+h} - \hat y_{T+h}| \big/ \frac{1}{T-m}\sum_t|y_t - y_{t-m}|$ \refHK; WQL $= 2\sum_{t,\tau}\rho_\tau(y_t - \hat q_{\tau,t})\big/\sum_t|y_t|$'),
     [T(r'$\rho_\tau(u) = u(\tau - \mathbf 1\{u < 0\})$ (pinball); the average over $\tau$ approximates the CRPS (Chapter 1)', r'$\rho_\tau(u) = u(\tau - \mathbf 1\{u < 0\})$ (pinball); media pe $\tau$ aproximează CRPS (Capitolul 1)')]),
    (T(r'Relative scores $r_s = L_s(\text{model})/L_s(\text{baseline})$ combined by the \textbf{geometric mean} \refFW: invariant to the choice of baseline in rankings, symmetric in gains and losses',
       r'Scorurile relative $r_s = L_s(\text{model})/L_s(\text{referință})$ se combină prin \textbf{media geometrică} \refFW: clasamentele nu depind de alegerea modelului de referință, iar cîștigurile și pierderile sînt tratate simetric'),
     [T(r'skill score $1 - \bar r_{\mathrm{geo}}$; win rate: share of series on which a model beats another', r'scorul de abilitate $1 - \bar r_{\mathrm{geo}}$; rata de cîștig: ponderea seriilor pe care un model îl întrece pe altul')]),
    T('The arithmetic mean of ratios rewards the baseline\'s weak series; the mean of raw errors is dominated by the series with the largest scale',
      'Media aritmetică a rapoartelor recompensează seriile slabe ale modelului de referință; media erorilor brute este dominată de seria cu scala cea mai mare')), 'small')

D.frame(T('Leakage and contamination', 'Scurgerea de informație și contaminarea'), items(
    (T(r'\textbf{Series leakage}: an evaluation series (or a near copy) is in the pretraining corpus; Chronos separates in-domain (Benchmark I) from zero-shot (Benchmark II) results for this reason \refAns',
       r'\textbf{Scurgerea seriilor}: o serie de evaluare (sau o copie apropiată) se află în corpusul de preantrenare; Chronos separă din acest motiv rezultatele în domeniu (Benchmark I) de cele zero-shot (Benchmark II) \refAns'), []),
    (T(r'\textbf{Temporal contamination}: the test window precedes the training cutoff; the model may have seen the outcomes of other, correlated series in the same period',
       r'\textbf{Contaminarea temporală}: fereastra de test precede data-limită a antrenării; modelul poate să fi văzut rezultatele altor serii, corelate, din aceeași perioadă'),
     [T(r'LLMs recall exact economic values from before their cutoff \refLTZ; a two-data-set design against contamination for electricity prices \refPE', r'LLM-urile reproduc valori economice exacte din perioada dinaintea datei-limită \refLTZ; un design cu două seturi de date împotriva contaminării, pentru prețurile electricității \refPE')]),
    (T('Designs that help', 'Designuri care ajută'),
     [T('evaluate only after the release (or the declared cutoff) of every model in the comparison; we use 1 November 2025, after the last of our models (Chronos-2, 30 October 2025)',
        'evaluați doar după lansarea (sau data-limită declarată) a fiecărui model din comparație; folosim 1 noiembrie 2025, după ultimul dintre modelele noastre (Chronos-2, 30 octombrie 2025)'),
      T('compare the relative skill before and after: a large drop after the release is a warning sign', 'comparați abilitatea relativă înainte și după: o scădere mare după lansare este un semnal de alarmă'),
      T('pre-register origins, horizons, metrics and baselines before looking at the results', 'preînregistrați originile, orizonturile, metricile și modelele de referință înainte de a vedea rezultatele')])), 'small')

D.frame(T('Testing across many series', 'Testarea pe multe serii'), items(
    (T(r'One series: DM with HLN correction \refDM, \refHLN; conditional ability \refGW; many models: MCS \refHLNa (all in Chapter 1)',
       r'O serie: DM cu corecția HLN \refDM, \refHLN; capacitatea condiționată \refGW; multe modele: MCS \refHLNa (toate în Capitolul 1)'), []),
    (T(r'$S$ series tested separately: at 5\% each, about $0.05S$ false rejections are expected under the null',
       r'$S$ serii testate separat: la 5\% fiecare, sub ipoteza nulă se așteaptă aproximativ $0{,}05S$ respingeri false'),
     [T(r'\textbf{Holm} \refHol (FWER): order $p_{(1)} \le \dots \le p_{(S)}$, reject while $p_{(k)} \le \alpha/(S - k + 1)$',
        r'\textbf{Holm} \refHol (FWER): ordonați $p_{(1)} \le \dots \le p_{(S)}$, respingeți cît timp $p_{(k)} \le \alpha/(S - k + 1)$'),
      T(r'\textbf{Benjamini--Hochberg} \refBH (FDR): reject the $k^*$ smallest, $k^* = \max\{k: p_{(k)} \le k\alpha/S\}$; valid under independence or positive dependence',
        r'\textbf{Benjamini--Hochberg} \refBH (FDR): respingeți cele mai mici $k^*$, $k^* = \max\{k: p_{(k)} \le k\alpha/S\}$; valid sub independență sau dependență pozitivă')]),
    (T(r'Pooled tests: average the loss differential across series at each origin, then one DM test with HAC variance: the cross-sectional correlation is kept in the time dimension',
       r'Teste agregate: mediați diferența de pierdere pe serii la fiecare origine, apoi un singur test DM cu varianță HAC: corelația dintre serii este păstrată în dimensiunea timpului'), []),
    T(r'Ranks over many data sets: Friedman and Nemenyi tests \refDem; they ignore the size of differences and assume independent data sets',
      r'Ranguri pe multe seturi de date: testele Friedman și Nemenyi \refDem; ele ignoră mărimea diferențelor și presupun seturi de date independente')), 'small')

D.recap(('benchmarks and testing', 'benchmark-urile și testarea'), [
    T('Aggregate scale-free relative scores by geometric means and report uncertainty over series', 'Agregați scoruri relative fără scală prin medii geometrice și raportați incertitudinea pe serii'),
    T('Contamination is a property of the pair (model, test window): evaluate after the release or live', 'Contaminarea este o proprietate a perechii (model, fereastră de test): evaluați după lansare sau live'),
    T('Many series mean many tests: correct with Holm or BH, or pool before testing', 'Multe serii înseamnă multe teste: corectați cu Holm sau BH sau agregați înainte de testare')])

# =============================================================================
# 4. DOVEZI PE DATELE NOASTRE
# =============================================================================
D.section('Evidence on our data', 'Dovezi pe datele noastre')

D.frame(T('The design of our comparisons', 'Designul comparațiilor noastre'), items(
    (T(r'\textbf{Romanian load}: day-ahead, 24 hours, every day from @{ld.first} to @{ld.last} (@{ld.n} days); context 2048 hours for the foundation models',
       r'\textbf{Consumul României}: pentru ziua următoare, 24 de ore, în fiecare zi de la @{ld.first} la @{ld.last} (@{ld.n} zile); context de 2048 de ore pentru foundation models'),
     [T(r'baselines: weekly naive; the expert ARX of \refZW for each hour (Chapter 1); DLinear \refZen and N-BEATS \refOre trained globally (Chapter 12)',
        r'modele de referință: naiv săptămînal; modelul ARX expert al lui \refZW pentru fiecare oră (Capitolul 1); DLinear \refZen și N-BEATS \refOre antrenate global (Capitolul 12)')]),
    (T(r'\textbf{EU inflation}: 27 countries, rolling monthly origins @{inf.first} -- @{inf.last}, $h = 1, \dots, 12$; random walk, AR($p$) by AIC, damped ETS \refHKSG, DLinear and N-BEATS trained on the panel',
       r'\textbf{Inflația UE}: 27 de țări, origini lunare mobile @{inf.first} -- @{inf.last}, $h = 1, \dots, 12$; mers aleator, AR($p$) după AIC, ETS amortizat \refHKSG, DLinear și N-BEATS antrenate pe panel'), []),
    (T(r'\textbf{Realised variance}: one day ahead, log RV; HAR \refCor on a rolling 1000-day window; QLIKE \refPat',
       r'\textbf{Varianța realizată}: o zi înainte, log RV; HAR \refCor pe o fereastră mobilă de 1000 de zile; QLIKE \refPat'), []),
    T('Foundation models: Chronos-Bolt small, Chronos-2, TimesFM 2.5, TiRex, zero-shot, on a CPU; Moirai and Lag-Llama were not run (their libraries need older software versions)',
      'Foundation models: Chronos-Bolt small, Chronos-2, TimesFM 2.5, TiRex, zero-shot, pe un CPU; Moirai și Lag-Llama nu au fost rulate (bibliotecile lor cer versiuni software mai vechi)')), 'small')

chart(T('Romanian load: day-ahead accuracy', 'Consumul României: acuratețea pentru ziua următoare'), 'ats_ch13_load', 'ATS_ch13_zero_shot', [
    T(r'Left: MAE (GW) over 24 hours and @{ld.n} days, models in the 10\% MCS marked; right: the last week of the sample, expert ARX and Chronos-2 with its 80\% band',
      r'Stînga: MAE (GW) pe 24 de ore și @{ld.n} zile, modelele din MCS de 10\% marcate; dreapta: ultima săptămînă din eșantion, ARX expert și Chronos-2 cu banda lui de 80\%')],
    h='0.5\\textheight')

interp(('the load comparison', 'comparației pentru consum'), [
    T(r'MAE: Chronos-2 @{ld.mae.c2}, expert ARX @{ld.mae.arx}, TiRex @{ld.mae.tx}, Chronos-Bolt @{ld.mae.bolt}, TimesFM @{ld.mae.tf}; DLinear @{ld.mae.dl}, N-BEATS @{ld.mae.nb}, weekly naive @{ld.mae.naive} GW',
      r'MAE: Chronos-2 @{ld.mae.c2}, ARX expert @{ld.mae.arx}, TiRex @{ld.mae.tx}, Chronos-Bolt @{ld.mae.bolt}, TimesFM @{ld.mae.tf}; DLinear @{ld.mae.dl}, N-BEATS @{ld.mae.nb}, naiv săptămînal @{ld.mae.naive} GW'),
    T(r'DM against the expert ARX: Chronos-2 $t = @{ld.dm.c2}$ ($p$ @{ld.dmp.c2}); the other three foundation models are significantly worse; the 10\% MCS is @{ld.mcs}',
      r'DM față de ARX expert: Chronos-2 $t = @{ld.dm.c2}$ ($p$ @{ld.dmp.c2}); celelalte trei foundation models sînt semnificativ mai slabe; MCS de 10\% este @{ld.mcs}'),
    T(r'80\% interval coverage: Chronos-2 @{ld.cov.c2}\%, Chronos-Bolt @{ld.cov.bolt}\%, TimesFM @{ld.cov.tf}\%, expert ARX @{ld.cov.arx}\%: none is far off, none is exact',
      r'Acoperirea intervalului de 80\%: Chronos-2 @{ld.cov.c2}\%, Chronos-Bolt @{ld.cov.bolt}\%, TimesFM @{ld.cov.tf}\%, ARX expert @{ld.cov.arx}\%: niciunul nu este departe, niciunul nu este exact'),
    T('A univariate zero-shot model matches an established domain model on a series with strong, regular shapes; the global deep models trained on three years lose to both',
      'Un model univariat zero-shot egalează un model de domeniu consacrat pe o serie cu forme puternice și regulate; modelele deep globale antrenate pe trei ani pierd în fața ambelor')])

chart(T('In-context covariates: calendar and temperature', 'Covariabile în context: calendarul și temperatura'), 'ats_ch13_covariates', 'ATS_ch13_zero_shot', [
    T(r'Chronos-2 MAE on all days, on ordinary days and on the @{cv.nh} public holidays: univariate, with weekend and holiday flags, and with flags plus Bucharest hourly temperature (realised values for the forecast day: an upper bound)',
      r'MAE Chronos-2 pe toate zilele, pe zilele obișnuite și pe cele @{cv.nh} zile de sărbătoare legală: univariat, cu indicatori de weekend și de sărbătoare și cu indicatori plus temperatura orară la București (valorile realizate pentru ziua prognozată: o limită superioară)')],
    h='0.5\\textheight')

interp(('the covariate experiment', 'experimentului cu covariabile'), [
    T(r'Holidays: MAE @{cv.u.hol} univariate, @{cv.c.hol} with the calendar, @{cv.t.hol} with temperature; ordinary days: @{cv.u.oth}, @{cv.c.oth}, @{cv.t.oth}',
      r'Sărbători: MAE @{cv.u.hol} univariat, @{cv.c.hol} cu calendarul, @{cv.t.hol} cu temperatura; zile obișnuite: @{cv.u.oth}, @{cv.c.oth}, @{cv.t.oth}'),
    T(r'Calendar against univariate: DM $t = @{cv.dmc}$ ($p$ @{cv.dmcp}); temperature on top: $t = @{cv.dmt}$ ($p$ @{cv.dmtp})',
      r'Calendarul față de varianta univariată: DM $t = @{cv.dmc}$ ($p$ @{cv.dmcp}); temperatura în plus: $t = @{cv.dmt}$ ($p$ @{cv.dmtp})'),
    T('The holiday effect is learned in context from a few earlier holidays in the 2048-hour window; no parameter was estimated',
      'Efectul sărbătorilor este învățat în context din cîteva sărbători anterioare aflate în fereastra de 2048 de ore; niciun parametru nu a fost estimat'),
    T('Realised temperature is not available at the origin: an operational test needs archived weather forecasts', 'Temperatura realizată nu este disponibilă la origine: un test operațional cere prognoze meteo arhivate')])

chart(T('EU inflation: 27 countries, 12 horizons', 'Inflația UE: 27 de țări, 12 orizonturi'), 'ats_ch13_inflation', 'ATS_ch13_benchmark', [
    T(r'Left: MAE relative to the random walk by horizon, geometric mean over countries; right: $h = 12$ with 95\% bootstrap intervals over countries; origins @{inf.first} -- @{inf.last}',
      r'Stînga: MAE relativ la mersul aleator pe orizonturi, medie geometrică pe țări; dreapta: $h = 12$ cu intervale bootstrap de 95\% pe țări; origini @{inf.first} -- @{inf.last}')],
    h='0.5\\textheight')

interp(('the inflation panel', 'panelului de inflație'), [
    T(r'$h = 1$: AR @{inf.h1.ar}, Chronos-2 @{inf.h1.c2}, TimesFM @{inf.h1.tf}, TiRex @{inf.h1.tx}; $h = 12$: AR @{inf.h12.ar}, ETS @{inf.h12.ets}, Chronos-2 @{inf.h12.c2}, TimesFM @{inf.h12.tf}, TiRex @{inf.h12.tx}, Bolt @{inf.h12.bolt}',
      r'$h = 1$: AR @{inf.h1.ar}, Chronos-2 @{inf.h1.c2}, TimesFM @{inf.h1.tf}, TiRex @{inf.h1.tx}; $h = 12$: AR @{inf.h12.ar}, ETS @{inf.h12.ets}, Chronos-2 @{inf.h12.c2}, TimesFM @{inf.h12.tf}, TiRex @{inf.h12.tx}, Bolt @{inf.h12.bolt}'),
    T(r'Global deep models at $h = 12$: DLinear @{inf.h12.dl}, N-BEATS @{inf.h12.nb}; Chronos-2 with cross-learning across the 27 countries: @{inf.h12.cl}',
      r'Modelele deep globale la $h = 12$: DLinear @{inf.h12.dl}, N-BEATS @{inf.h12.nb}; Chronos-2 cu învățare încrucișată pe cele 27 de țări: @{inf.h12.cl}'),
    T(r'CRPS relative to AR (geometric mean over countries): Chronos-2 @{inf.crps.c2}, TimesFM @{inf.crps.tf}, TiRex @{inf.crps.tx}, ETS @{inf.crps.ets}',
      r'CRPS relativ la AR (medie geometrică pe țări): Chronos-2 @{inf.crps.c2}, TimesFM @{inf.crps.tf}, TiRex @{inf.crps.tx}, ETS @{inf.crps.ets}'),
    T('The 2021--2023 surge dominates every average: no univariate method foresaw it, so differences are about the speed of adaptation, not about foresight',
      'Creșterea din 2021--2023 domină orice medie: nicio metodă univariată nu a anticipat-o, deci diferențele țin de viteza de adaptare, nu de anticipare')])

chart(T('Romania: forecasts from three origins', 'România: prognoze din trei origini'), 'ats_ch13_ro_inflation', 'ATS_ch13_benchmark', [
    T(r'Romanian HICP annual inflation and 12-month forecasts with 80\% bands from Chronos-2 and AR($p$), from @{ri.o1}, @{ri.o2} and @{ri.o3}',
      r'Inflația anuală HICP a României și prognoze pe 12 luni cu benzi de 80\% din Chronos-2 și AR($p$), de la @{ri.o1}, @{ri.o2} și @{ri.o3}')],
    h='0.5\\textheight')

interp(('the Romanian paths', 'traiectoriilor pentru România'), [
    T(r'From @{ri.o1}: 12 months later inflation was @{ri.a1}\%; Chronos-2 median @{ri.c1}\% (80\%: @{ri.c1l} -- @{ri.c1h}), AR @{ri.r1}\%',
      r'De la @{ri.o1}: după 12 luni inflația a fost @{ri.a1}\%; mediana Chronos-2 @{ri.c1}\% (80\%: @{ri.c1l} -- @{ri.c1h}), AR @{ri.r1}\%'),
    T(r'From @{ri.o2}, near the peak (@{ri.peak}\% in @{ri.pd}): outcome @{ri.a2}\%; Chronos-2 @{ri.c2}\%, AR @{ri.r2}\%',
      r'De la @{ri.o2}, aproape de vîrf (@{ri.peak}\% în @{ri.pd}): rezultat @{ri.a2}\%; Chronos-2 @{ri.c2}\%, AR @{ri.r2}\%'),
    T(r'From @{ri.o3}: outcome @{ri.a3}\%; Chronos-2 @{ri.c3}\%, AR @{ri.r3}\%; the latest observation is @{ri.last}\% (@{ri.ld})',
      r'De la @{ri.o3}: rezultat @{ri.a3}\%; Chronos-2 @{ri.c3}\%, AR @{ri.r3}\%; ultima observație este @{ri.last}\% (@{ri.ld})'),
    T('Both methods extrapolate persistence; turning points come from information outside the series (energy prices, the end of the price caps, the VAT increase of August 2025, whose effect on annual inflation lasts exactly 12 months): known in advance, hence natural covariates',
      'Ambele metode extrapolează persistența; punctele de întoarcere vin din informații din afara seriei (prețurile energiei, sfîrșitul plafonării prețurilor, majorarea TVA din august 2025, al cărei efect asupra inflației anuale durează exact 12 luni): cunoscute dinainte, deci covariabile naturale')])

chart(T('Twenty-seven tests at once', 'Douăzeci și șapte de teste deodată'), 'ats_ch13_multiple', 'ATS_ch13_benchmark', [
    T(r'Country-level DM--HLN statistics (HAC with $h - 1$ lags) of the absolute errors of @{mt.model} minus AR($p$) at $h = @{mt.h}$; negative: @{mt.model} better',
      r'Statisticile DM--HLN pe țări (HAC cu $h - 1$ decalaje) ale erorilor absolute @{mt.model} minus AR($p$) la $h = @{mt.h}$; negativ: @{mt.model} este mai bun')],
    h='0.48\\textheight')

interp(('the multiple tests', 'testelor multiple'), [
    T(r'@{mt.neg} of 27 statistics are negative; @{mt.rej} are significant at 5\% without correction (@{mt.rejfm} in favour of @{mt.model}, @{mt.rejar} in favour of AR)',
      r'@{mt.neg} din 27 de statistici sînt negative; @{mt.rej} sînt semnificative la 5\% fără corecție (@{mt.rejfm} în favoarea @{mt.model}, @{mt.rejar} în favoarea AR)'),
    T(r'With Holm: @{mt.holm} rejections; with Benjamini--Hochberg: @{mt.bh}; Romania: $t = @{mt.rot}$, $p$ @{mt.rop}',
      r'Cu Holm: @{mt.holm} respingeri; cu Benjamini--Hochberg: @{mt.bh}; România: $t = @{mt.rot}$, $p$ @{mt.rop}'),
    T(r'Pooled over the 27 countries (average loss differential at each origin, HAC variance): $t = @{ai.t}$, $p$ @{ai.p}; the bootstrap intervals of the previous chart treat countries as independent and look sharper than they are',
      r'Agregat pe cele 27 de țări (diferența medie de pierdere la fiecare origine, varianță HAC): $t = @{ai.t}$, $p$ @{ai.p}; intervalele bootstrap din graficul anterior tratează țările ca independente și par mai precise decît sînt'),
    T('A paper that reports the countries where its model wins at 5\\% reports noise; the pooled test and the multiplicity-adjusted counts are the honest summary',
      'O lucrare care raportează țările în care modelul ei cîștigă la 5\\% raportează zgomot; testul agregat și numerele ajustate pentru multiplicitate sînt rezumatul onest')])

chart(T('Realised variance: foundation models against HAR', 'Varianța realizată: foundation models față de HAR'), 'ats_ch13_rv', 'ATS_ch13_benchmark', [
    T(r'One-day-ahead log RV: MSE and QLIKE relative to HAR; Bitcoin (Binance, @{rv.b.first} -- @{rv.b.last}, $n = @{rv.b.n}$), S\&P 500 (Oxford-Man, @{rv.s.first} -- @{rv.s.last}, $n = @{rv.s.n}$)',
      r'Log RV pentru ziua următoare: MSE și QLIKE relativ la HAR; Bitcoin (Binance, @{rv.b.first} -- @{rv.b.last}, $n = @{rv.b.n}$), S\&P 500 (Oxford-Man, @{rv.s.first} -- @{rv.s.last}, $n = @{rv.s.n}$)')],
    h='0.5\\textheight')

interp(('the volatility comparison', 'comparației pentru volatilitate'), [
    T(r'Bitcoin, QLIKE relative to HAR: Chronos-2 @{rv.b.c2}, TimesFM @{rv.b.tf}, TiRex @{rv.b.tx}, Bolt @{rv.b.bolt}; MCS (10\%): @{rv.b.mcs}',
      r'Bitcoin, QLIKE relativ la HAR: Chronos-2 @{rv.b.c2}, TimesFM @{rv.b.tf}, TiRex @{rv.b.tx}, Bolt @{rv.b.bolt}; MCS (10\%): @{rv.b.mcs}'),
    T(r'S\&P 500: Chronos-2 @{rv.s.c2}, TimesFM @{rv.s.tf}, TiRex @{rv.s.tx}, Bolt @{rv.s.bolt}; MCS (10\%): @{rv.s.mcs}',
      r'S\&P 500: Chronos-2 @{rv.s.c2}, TimesFM @{rv.s.tf}, TiRex @{rv.s.tx}, Bolt @{rv.s.bolt}; MCS (10\%): @{rv.s.mcs}'),
    T(r'Three of the four zero-shot models beat HAR on both assets and HAR is outside both MCS: the slowly decaying memory of log RV (Chapter 10) is a shape a corpus can teach; the gain is large for Bitcoin, small for the S\&P 500',
      r'Trei dintre cele patru modele zero-shot întrec HAR pe ambele active, iar HAR nu intră în niciun MCS: memoria lentă a lui log RV (Capitolul 10) este o formă pe care un corpus o poate preda; cîștigul este mare pentru Bitcoin și mic pentru S\&P 500'),
    T(r'Recent studies reach mixed verdicts \refGoe, \refBri, \refRNW: gains depend on the asset, the horizon and the loss, and fine-tuning or pretraining on financial data often matters', r'Studii recente ajung la verdicte mixte \refGoe, \refBri, \refRNW: cîștigurile depind de activ, de orizont și de funcția de pierdere, iar fine-tuning-ul sau preantrenarea pe date financiare contează adesea')])

chart(T('Before and after the releases', 'Înainte și după lansări'), 'ats_ch13_contamination', 'ATS_ch13_benchmark', [
    T(r'Relative loss of each model in an earlier window and in the window after every release (from 1 November 2025): load (MAE / expert ARX) and Bitcoin (QLIKE / HAR)',
      r'Pierderea relativă a fiecărui model într-o fereastră anterioară și în fereastra de după toate lansările (din 1 noiembrie 2025): consum (MAE / ARX expert) și Bitcoin (QLIKE / HAR)')],
    h='0.5\\textheight')

interp(('the contamination check', 'verificării contaminării'), [
    T(r'Load, Chronos-2: @{ct.l.c2a} before, @{ct.l.c2b} after; TimesFM: @{ct.l.tfa}, @{ct.l.tfb}; the earlier window (January--October 2025) precedes both releases',
      r'Consum, Chronos-2: @{ct.l.c2a} înainte, @{ct.l.c2b} după; TimesFM: @{ct.l.tfa}, @{ct.l.tfb}; fereastra anterioară (ianuarie--octombrie 2025) precede ambele lansări'),
    T(r'Bitcoin, Chronos-2: @{ct.b.c2a} (2021 -- 24 November 2024) and @{ct.b.c2b} (after); TiRex: @{ct.b.txa}, @{ct.b.txb}; post-release windows have @{ct.nl} and @{ct.nb} days',
      r'Bitcoin, Chronos-2: @{ct.b.c2a} (2021 -- 24 noiembrie 2024) și @{ct.b.c2b} (după); TiRex: @{ct.b.txa}, @{ct.b.txb}; ferestrele de după lansare au @{ct.nl} și @{ct.nb} zile'),
    T('No deterioration after the releases (for Bitcoin the ratios are even lower): no evidence of contamination here; but the absence of a drop does not prove absence of leakage, and markets change between windows',
      'Nicio deteriorare după lansări (pentru Bitcoin rapoartele sînt chiar mai mici): nicio dovadă de contaminare aici; dar absența unei scăderi nu dovedește absența scurgerii, iar piețele se schimbă între ferestre')])

D.recap(('the evidence', 'dovezile'), [
    T('Strong shapes (load): the best foundation model matches or beats the domain model; weak shapes (returns): little to transfer', 'Forme puternice (consum): cel mai bun foundation model egalează sau întrece modelul de domeniu; forme slabe (randamente): puțin de transferat'),
    T('Inflation: ahead of AR and ETS in the panel average (most with cross-learning), but no country difference survives Holm or BH and the pooled test is not significant', 'Inflația: înaintea modelelor AR și ETS în media panelului (cel mai mult cu învățarea încrucișată), dar nicio diferență pe țară nu rezistă corecțiilor Holm sau BH, iar testul agregat nu este semnificativ'),
    T('Realised variance: zero-shot models beat HAR, clearly for Bitcoin, narrowly for the S\\&P 500', 'Varianța realizată: modelele zero-shot întrec HAR, clar pentru Bitcoin, la limită pentru S\\&P 500'),
    T('Covariates in context help where the calendar matters; post-release windows show no sign of contamination', 'Covariabilele în context ajută acolo unde calendarul contează; ferestrele de după lansare nu arată semne de contaminare')])

# =============================================================================
# 5. LLM
# =============================================================================
D.section('Language models for time series', 'Modele de limbaj pentru serii de timp')

D.frame(T('LLMTime: numbers as text', 'LLMTime: numerele ca text'), items(
    (T(r'\refGru: rescale, round to a fixed number of digits, write values as digits separated by spaces and commas; an off-the-shelf LLM continues the string',
       r'\refGru: se rescalează, se rotunjește la un număr fix de cifre, valorile se scriu ca cifre separate prin spații și virgule; un LLM obișnuit continuă șirul'),
     [T('digit-by-digit probabilities define a hierarchical (multi-bin) density over continuous values; repeated sampling gives quantiles', 'probabilitățile cifră cu cifră definesc o densitate ierarhică (pe mai multe intervale) pentru valori continue; eșantionarea repetată dă cuantile')]),
    (T('Findings of the paper: competitive zero-shot on some benchmarks; tokenisation of numbers matters (a newer model could do worse because of how it splits digits); alignment (RLHF) hurts calibration',
       'Rezultatele lucrării: competitiv zero-shot pe unele benchmark-uri; tokenizarea numerelor contează (un model mai nou putea fi mai slab din cauza felului în care împarte cifrele); alinierea (RLHF) strică calibrarea'), []),
    T('Costs: thousands of tokens per series and many samples per forecast; the context window limits the history; the LLM may have memorised the data',
      'Costuri: mii de token-uri pe serie și multe eșantioane pentru o prognoză; fereastra de context limitează istoria; LLM-ul poate să fi memorat datele')), 'small')

D.frame(T('Reprogramming a frozen LLM', 'Reprogramarea unui LLM înghețat'), items(
    (T(r'\textbf{Time-LLM} \refJin: patches of the series are mapped onto text prototypes (word embeddings), a prompt prefix describes the task and statistics; the LLM stays frozen, a projection reads the forecast',
       r'\textbf{Time-LLM} \refJin: patch-urile seriei sînt proiectate pe prototipuri de text (embedding-uri de cuvinte), un prefix de prompt descrie sarcina și statisticile; LLM-ul rămîne înghețat, o proiecție citește prognoza'), []),
    (T(r'\textbf{One Fits All} (GPT4TS) \refZho: a frozen GPT-2 with trained input embedding, layer norms and output layer, for forecasting, classification and anomaly detection',
       r'\textbf{One Fits All} (GPT4TS) \refZho: un GPT-2 înghețat, cu embedding-ul de intrare, normalizările de strat și stratul de ieșire antrenate, pentru prognoză, clasificare și detectarea anomaliilor'), []),
    T('The claim: knowledge from language transfers to series; the test of the claim is an ablation that removes the language model',
      'Afirmația: cunoașterea din limbaj se transferă la serii; testul afirmației este o ablație care elimină modelul de limbaj')), 'small')

D.frame(T('Case study: are language models actually useful?', 'Studiu de caz: sînt modelele de limbaj chiar utile?'), two(
    items(T(r'\refTan: three LLM-based forecasters (including Time-LLM and GPT4TS), the same benchmarks, three ablations',
            r'\refTan: trei prognozatori pe bază de LLM (inclusiv Time-LLM și GPT4TS), aceleași benchmark-uri, trei ablații'),
          (T('Ablations', 'Ablațiile'),
           [T('remove the LLM; replace it by one attention layer; replace it by a basic Transformer block', 'eliminarea LLM-ului; înlocuirea lui cu un strat de atenție; înlocuirea cu un bloc Transformer simplu')]),
          T('Result: no degradation, often an improvement; pretrained LLMs do no better than the same model trained from scratch, do not model sequential dependence, do not help in few-shot settings',
            'Rezultat: nicio degradare, adesea o îmbunătățire; LLM-urile preantrenate nu sînt mai bune decît același model antrenat de la zero, nu modelează dependența secvențială, nu ajută cînd datele sînt puține'),
          T('Training and inference cost orders of magnitude more', 'Antrenarea și inferența costă cu ordine de mărime mai mult')),
    items(T('The method matters more than the result', 'Metoda contează mai mult decît rezultatul'),
          T('an architecture claim needs an ablation with matched compute and tuning', 'o afirmație despre arhitectură cere o ablație cu calcul și ajustare comparabile'),
          T('time-series foundation models trained on series (Chronos, TimesFM, TiRex) are not affected by this critique; LLMs used as forecasters are', 'foundation models antrenate pe serii (Chronos, TimesFM, TiRex) nu sînt vizate de această critică; LLM-urile folosite ca prognozatori sînt'),
          T(r'LLMs remain useful around forecasting: code, literature, critique (Section 9)', r'LLM-urile rămîn utile în jurul prognozei: cod, literatură, critică (secțiunea 9)')), '0.56', '0.42'), 'small')

D.frame(T('Memorisation and look-ahead', 'Memorare și anticiparea viitorului'), items(
    (T(r'\refLTZ: LLMs reproduce macroeconomic and market values from their training period with high precision, even when asked not to use future information',
       r'\refLTZ: LLM-urile reproduc cu mare precizie valori macroeconomice și de piață din perioada lor de antrenare, chiar și cînd li se cere să nu folosească informații viitoare'),
     [T('a backtest before the training cutoff measures recall, not forecasting', 'un backtest înainte de data-limită a antrenării măsoară memoria, nu capacitatea de prognoză')]),
    (T('For time-series foundation models the same logic applies to public series in the corpus (electricity, traffic, M4)', 'Pentru foundation models pe serii de timp, aceeași logică se aplică seriilor publice din corpus (electricitate, trafic, M4)'),
     [T('our evidence: windows after every release (Section 4); the strongest evidence: live, pre-registered forecasts', 'dovezile noastre: ferestre de după toate lansările (secțiunea 4); cele mai puternice dovezi: prognoze live, preînregistrate')]),
    T('A practical rule: state the training cutoff of every model and the start of the evaluation window in the same table', 'O regulă practică: precizați data-limită de antrenare a fiecărui model și începutul ferestrei de evaluare în același tabel')), 'small')

D.recap(('LLMs', 'LLM'), [
    T('LLMTime and reprogramming show that text models can be bent to series; ablations show the language part is rarely what helps', 'LLMTime și reprogramarea arată că modelele de text pot fi adaptate la serii; ablațiile arată că partea de limbaj rareori este cea care ajută'),
    T('Memorisation makes pre-cutoff evaluation of LLM forecasts invalid', 'Memorarea face ca evaluarea prognozelor LLM înainte de data-limită să nu fie validă')])

# =============================================================================
# 6. PREDICȚIA CONFORMALĂ
# =============================================================================
D.section('Conformal prediction', 'Predicția conformală')

D.frame(T('Where conformal prediction comes from', 'Originea predicției conformale'), two(
    ph('gammerman', T('Alexander Gammerman, Royal Holloway, 2018', 'Alexander Gammerman, Royal Holloway, 2018'), h='0.36\\textheight'),
    items(T(r'Vovk, Gammerman and Shafer \refVGS, \refVGSb: prediction sets valid in finite samples under exchangeability only, for any predictive model',
            r'Vovk, Gammerman și Shafer \refVGS, \refVGSb: mulțimi de predicție valide în eșantioane finite doar sub interschimbabilitate, pentru orice model predictiv'),
          T('The idea: how "conforming" a candidate value is to the data seen, measured by a rank', 'Ideea: cît de „conformă” este o valoare candidat cu datele văzute, măsurat printr-un rang'),
          T(r'Modern statistics adopted it as a wrapper around machine learning \refLei, \refAB', r'Statistica modernă a adoptat-o ca înveliș în jurul metodelor de machine learning \refLei, \refAB')), '0.42', '0.56'), 'small')

D.frame(T('Exchangeability and the target guarantee', 'Interschimbabilitatea și garanția urmărită'), items(
    (T(r'$Z_1, \dots, Z_{n+1}$, $Z_i = (X_i, Y_i)$, are \textbf{exchangeable} if $(Z_{\pi(1)}, \dots, Z_{\pi(n+1)}) \overset{d}{=} (Z_1, \dots, Z_{n+1})$ for every permutation $\pi$',
       r'$Z_1, \dots, Z_{n+1}$, $Z_i = (X_i, Y_i)$, sînt \textbf{interschimbabile} dacă $(Z_{\pi(1)}, \dots, Z_{\pi(n+1)}) \overset{d}{=} (Z_1, \dots, Z_{n+1})$ pentru orice permutare $\pi$'),
     [T('i.i.d.\\ implies exchangeable; draws without replacement are exchangeable but dependent; a stationary AR(1) is not exchangeable', 'i.i.d.\\ implică interschimbabilitate; extragerile fără întoarcere sînt interschimbabile, dar dependente; un AR(1) staționar nu este interschimbabil')]),
    (T(r'\textbf{Marginal coverage}: $\Pr\{Y_{n+1} \in \hat C(X_{n+1})\} \ge 1 - \alpha$, the probability taken over the calibration data and the test point together',
       r'\textbf{Acoperire marginală}: $\Pr\{Y_{n+1} \in \hat C(X_{n+1})\} \ge 1 - \alpha$, probabilitatea fiind luată împreună pe datele de calibrare și pe punctul de test'),
     [T(r'not \textbf{conditional} coverage $\Pr\{Y \in \hat C(x) \mid X = x\} \ge 1 - \alpha$ for every $x$, and not coverage given the calibration sample', r'nu acoperirea \textbf{condiționată} $\Pr\{Y \in \hat C(x) \mid X = x\} \ge 1 - \alpha$ pentru orice $x$ și nici acoperirea condiționată de eșantionul de calibrare')]),
    T(r'A \textbf{nonconformity score} $s(x, y)$: large when $y$ is unusual given $x$, e.g.\ $|y - \hat\mu(x)|$, $|y - \hat\mu(x)|/\hat\sigma(x)$, or the CQR score below',
      r'Un \textbf{scor de neconformitate} $s(x, y)$: mare cînd $y$ este neobișnuit dat fiind $x$, de exemplu $|y - \hat\mu(x)|$, $|y - \hat\mu(x)|/\hat\sigma(x)$ sau scorul CQR de mai jos')), 'small')

D.frame(T('Split conformal prediction', 'Predicția split conformal'), items(
    (T(r'Fit $\hat\mu$ on a training set; compute $S_i = s(X_i, Y_i)$ on $n$ calibration points \refPap, \refLei',
       r'Se estimează $\hat\mu$ pe un set de antrenare; se calculează $S_i = s(X_i, Y_i)$ pe $n$ puncte de calibrare \refPap, \refLei'),
     [T(r'$\hat q = S_{(k)}$, $k = \lceil (n + 1)(1 - \alpha) \rceil$ (the $k$-th smallest; $+\infty$ if $k > n$); $\hat C(x) = \{y: s(x, y) \le \hat q\}$',
        r'$\hat q = S_{(k)}$, $k = \lceil (n + 1)(1 - \alpha) \rceil$ (a $k$-a cea mai mică valoare; $+\infty$ dacă $k > n$); $\hat C(x) = \{y: s(x, y) \le \hat q\}$')]),
    (T(r'\textbf{Theorem}: if $(X_i, Y_i)_{i \le n+1}$ are exchangeable, $\Pr\{Y_{n+1} \in \hat C(X_{n+1})\} \ge 1 - \alpha$; with no ties, also $\le 1 - \alpha + 1/(n + 1)$',
       r'\textbf{Teoremă}: dacă $(X_i, Y_i)_{i \le n+1}$ sînt interschimbabile, $\Pr\{Y_{n+1} \in \hat C(X_{n+1})\} \ge 1 - \alpha$; fără egalități, și $\le 1 - \alpha + 1/(n + 1)$'),
     [T(r'proof: given $\hat\mu$, the scores $S_1, \dots, S_{n+1}$ are exchangeable, so the rank of $S_{n+1}$ is uniform on $\{1, \dots, n + 1\}$; $Y_{n+1} \in \hat C \iff$ rank $\le k$, probability $k/(n + 1) \ge 1 - \alpha$ (Appendix)',
        r'demonstrație: dat fiind $\hat\mu$, scorurile $S_1, \dots, S_{n+1}$ sînt interschimbabile, deci rangul lui $S_{n+1}$ este uniform pe $\{1, \dots, n + 1\}$; $Y_{n+1} \in \hat C \iff$ rangul $\le k$, cu probabilitatea $k/(n + 1) \ge 1 - \alpha$ (Anexă)')]),
    T('No assumption on the model or on the distribution: a bad model gives wide, not invalid, intervals', 'Nicio ipoteză asupra modelului sau a distribuției: un model slab dă intervale largi, nu invalide')), 'small')

chart(T('Coverage given the calibration set', 'Acoperirea condiționată de setul de calibrare'), 'ats_ch13_split_coverage', 'ATS_ch13_conformal_basics', [
    T(r'Coverage $F(\hat q)$ of the next point for @{sp.reps} calibration sets of $n = 50$ and $n = 500$ scores, $\alpha = 0.1$, and the exact law Beta($k$, $n + 1 - k$)',
      r'Acoperirea $F(\hat q)$ a punctului următor pentru @{sp.reps} de seturi de calibrare de $n = 50$ și $n = 500$ scoruri, $\alpha = 0{,}1$, și legea exactă Beta($k$, $n + 1 - k$)')],
    h='0.48\\textheight')

interp(('the coverage distribution', 'distribuției acoperirii'), [
    T(r'Mean coverage @{sp.m50} ($n = 50$) and @{sp.m500} ($n = 500$), as the theory gives (@{sp.t50}, @{sp.t500}): the marginal guarantee holds on average over calibration sets',
      r'Acoperirea medie @{sp.m50} ($n = 50$) și @{sp.m500} ($n = 500$), cum dă teoria (@{sp.t50}, @{sp.t500}): garanția marginală este valabilă în medie pe seturile de calibrare'),
    T(r'One calibration set is one draw: s.d.\ @{sp.s50} and @{sp.s500}; with $n = 50$, @{sp.b50}\% of the sets give coverage below 0.88, with $n = 500$ only @{sp.b500}\%',
      r'Un set de calibrare este o singură extragere: abaterea standard @{sp.s50} și @{sp.s500}; cu $n = 50$, @{sp.b50}\% dintre seturi dau acoperire sub 0,88, cu $n = 500$ doar @{sp.b500}\%'),
    T(r'Since $F(\hat q) \sim$ Beta($k$, $n + 1 - k$), choosing $n$ is a sample-size calculation: the s.d.\ is about $\sqrt{\alpha(1 - \alpha)/n}$',
      r'Deoarece $F(\hat q) \sim$ Beta($k$, $n + 1 - k$), alegerea lui $n$ este un calcul de mărime a eșantionului: abaterea standard este aproximativ $\sqrt{\alpha(1 - \alpha)/n}$')])

D.frame(T('Conformalized quantile regression', 'Regresia cuantilică conformalizată'), two(
    ph('candes', T('Emmanuel Candès, 2012', 'Emmanuel Candès, 2012'), h='0.34\\textheight'),
    items(T(r'\refRPC: fit quantile regressions \refKB $\hat q_{\alpha/2}(x)$, $\hat q_{1-\alpha/2}(x)$ on the training set',
            r'\refRPC: se estimează regresii cuantilice \refKB $\hat q_{\alpha/2}(x)$, $\hat q_{1-\alpha/2}(x)$ pe setul de antrenare'),
          T(r'Score $s(x, y) = \max\{\hat q_{\alpha/2}(x) - y,\; y - \hat q_{1-\alpha/2}(x)\}$: negative inside the band', r'Scorul $s(x, y) = \max\{\hat q_{\alpha/2}(x) - y,\; y - \hat q_{1-\alpha/2}(x)\}$: negativ în interiorul benzii'),
          T(r'$\hat C(x) = [\hat q_{\alpha/2}(x) - \hat q,\; \hat q_{1-\alpha/2}(x) + \hat q]$: the band is shifted outwards (or inwards if $\hat q < 0$)',
            r'$\hat C(x) = [\hat q_{\alpha/2}(x) - \hat q,\; \hat q_{1-\alpha/2}(x) + \hat q]$: banda este deplasată spre exterior (sau spre interior dacă $\hat q < 0$)'),
          T('Marginal coverage by the split theorem; the width adapts to heteroskedasticity through the quantile models', 'Acoperirea marginală rezultă din teorema split; lățimea se adaptează la heteroscedasticitate prin modelele cuantilice'),
          T('The same score calibrates the quantiles of any foundation model (Section 8)', 'Același scor calibrează cuantilele oricărui foundation model (secțiunea 8)')), '0.32', '0.66'), 'small')

chart(T('CQR on the design of Romano, Patterson and Candès', 'CQR pe designul lui Romano, Patterson și Candès'), 'ats_ch13_cqr', 'ATS_ch13_conformal_basics', [
    T(r'$Y = \mathrm{Pois}(\sin^2 X + 0.1) + 0.03X\varepsilon_1 + 25\cdot\mathbf 1\{U < 0.01\}\varepsilon_2$, $X \sim U[0, 5]$ (their Figure 1); 1000 training and 1000 calibration points; gradient boosting for the mean and for the 5\% and 95\% quantiles',
      r'$Y = \mathrm{Pois}(\sin^2 X + 0{,}1) + 0{,}03X\varepsilon_1 + 25\cdot\mathbf 1\{U < 0{,}01\}\varepsilon_2$, $X \sim U[0, 5]$ (Figura 1 din lucrare); 1000 de puncte de antrenare și 1000 de calibrare; gradient boosting pentru medie și pentru cuantilele de 5\% și 95\%')],
    h='0.48\\textheight')

interp(('CQR', 'CQR'), [
    T(r'Test coverage: split conformal @{cq.sc}, CQR @{cq.cc}, the raw quantile models @{cq.rc}; mean width @{cq.sw}, @{cq.cw} and @{cq.rw}',
      r'Acoperirea pe datele de test: split conformal @{cq.sc}, CQR @{cq.cc}, modelele cuantilice brute @{cq.rc}; lățimea medie @{cq.sw}, @{cq.cw} și @{cq.rw}'),
    T(r'The raw quantile regressions undercover; CQR repairs them at almost no extra width, while the constant-width split band is @{cq.ratio}\% wider',
      r'Regresiile cuantilice brute acoperă prea puțin; CQR le repară aproape fără lățime suplimentară, în timp ce banda split de lățime constantă este cu @{cq.ratio}\% mai largă'),
    T(r'By $X$ bins both stay within a few points of 90\% (worst bins: CQR @{cq.cmin}, split @{cq.smin}); the gain of CQR is in width: narrow where $Y$ is concentrated, wide where the Poisson noise is large',
      r'Pe intervale ale lui $X$, ambele rămîn la cîteva puncte de 90\% (cele mai slabe intervale: CQR @{cq.cmin}, split @{cq.smin}); cîștigul CQR este în lățime: îngust acolo unde $Y$ este concentrat, larg acolo unde zgomotul Poisson este mare')])

D.frame(T('The limits of conditional coverage', 'Limitele acoperirii condiționate'), items(
    (T(r'\textbf{Impossibility} \refVov, \refLW, \refBarB: if $\hat C$ has conditional coverage $\ge 1 - \alpha$ at almost every $x$ for every distribution with a continuous $X$, then its expected length is infinite',
       r'\textbf{Imposibilitate} \refVov, \refLW, \refBarB: dacă $\hat C$ are acoperire condiționată $\ge 1 - \alpha$ în aproape orice $x$, pentru orice distribuție cu $X$ continuu, atunci lungimea lui așteptată este infinită'),
     [T('no finite-sample method can certify coverage at each point of a continuous covariate without assumptions', 'nicio metodă nu poate certifica în eșantioane finite acoperirea în fiecare punct al unei covariabile continue fără ipoteze')]),
    (T(r'What is achievable: coverage within a finite set of groups (Mondrian conformal: calibrate separately by group); approximate conditional coverage under smoothness; coverage conditional on the calibration set with high probability (Beta law)',
       r'Rezultate posibile: acoperire în cadrul unui număr finit de grupuri (conformal Mondrian: calibrare separată pe grupuri); acoperire condiționată aproximativă sub ipoteze de netezime; acoperire condiționată de setul de calibrare cu probabilitate mare (legea Beta)'), []),
    T('For time series the relevant condition is the past: $\\Pr\\{Y_t \\in \\hat C_t \\mid \\mathcal F_{t-1}\\}$; a VaR backtest (Chapter 9) tests exactly this property for one-sided sets',
      'Pentru serii de timp, condiția relevantă este trecutul: $\\Pr\\{Y_t \\in \\hat C_t \\mid \\mathcal F_{t-1}\\}$; un backtest VaR (Capitolul 9) testează exact această proprietate pentru mulțimi unilaterale')), 'small')

D.recap(('conformal prediction', 'predicția conformală'), [
    T('Split conformal: a rank argument gives finite-sample marginal coverage under exchangeability, for any model', 'Split conformal: un argument de rang dă acoperire marginală în eșantioane finite sub interschimbabilitate, pentru orice model'),
    T('CQR adds adaptivity; the calibration sample size controls the variability of realised coverage', 'CQR adaugă adaptivitate; mărimea eșantionului de calibrare controlează variabilitatea acoperirii realizate'),
    T('Conditional coverage is impossible in general: test it, do not claim it', 'Acoperirea condiționată este imposibilă în general: testați-o, nu o afirmați')])

# =============================================================================
# 7. CONFORMAL PENTRU DATE DEPENDENTE
# =============================================================================
D.section('Conformal prediction for dependent data', 'Predicția conformală pentru date dependente')

D.frame(T('Exchangeability violated: what survives', 'Interschimbabilitatea încălcată: rezultatele care rămîn valabile'), items(
    (T('Time series violate exchangeability three ways: serial dependence, changing volatility, structural change; the last two break coverage most', 'Seriile de timp încalcă interschimbabilitatea în trei feluri: dependența serială, volatilitatea variabilă, schimbările structurale; ultimele două strică cel mai mult acoperirea'), []),
    (T(r'\textbf{Stationary and mixing}: split conformal remains approximately valid, with a coverage gap controlled by $\beta$-mixing coefficients and the calibration size \refOli',
       r'\textbf{Staționar și mixing}: split conformal rămîne aproximativ valid, cu o abatere a acoperirii controlată de coeficienții $\beta$-mixing și de mărimea calibrării \refOli'),
     [T(r'block permutations restore exactness under weaker conditions \refCWZ', r'permutările pe blocuri refac exactitatea sub condiții mai slabe \refCWZ')]),
    (T(r'\textbf{Non-stationary}: no static method can work; the threshold must move with the data: weights (Barber et al.), refitting (EnbPI), feedback on errors (ACI, PID)',
       r'\textbf{Nestaționar}: nicio metodă statică nu poate funcționa; pragul trebuie să se miște odată cu datele: ponderi (Barber et al.), reestimare (EnbPI), reacție la erori (ACI, PID)'), []),
    T(r'A common online frame: scores $S_t = s(X_t, Y_t)$ computed from out-of-sample forecasts; at $t$ choose a threshold $q_t$ from $S_1, \dots, S_{t-1}$; miss $\mathrm{err}_t = \mathbf 1\{S_t > q_t\}$',
      r'Un cadru online comun: scorurile $S_t = s(X_t, Y_t)$ calculate din prognoze în afara eșantionului; la momentul $t$ se alege un prag $q_t$ din $S_1, \dots, S_{t-1}$; ratarea $\mathrm{err}_t = \mathbf 1\{S_t > q_t\}$')), 'small')

D.frame(T('Conformal prediction beyond exchangeability', 'Predicția conformală dincolo de interschimbabilitate'), items(
    (T(r'\refBar: fixed weights $w_i \in [0, 1]$, chosen before seeing the data; $\hat q$ = the $(1 - \alpha)$ quantile of $\sum_i \tilde w_i\delta_{S_i} + \tilde w_{n+1}\delta_{+\infty}$, $\tilde w_i = w_i/(1 + \sum_j w_j)$, $w_{n+1} = 1$',
       r'\refBar: ponderi fixe $w_i \in [0, 1]$, alese înainte de a vedea datele; $\hat q$ = cuantila $(1 - \alpha)$ a lui $\sum_i \tilde w_i\delta_{S_i} + \tilde w_{n+1}\delta_{+\infty}$, $\tilde w_i = w_i/(1 + \sum_j w_j)$, $w_{n+1} = 1$'),
     [T(r'\textbf{Theorem}: coverage $\ge 1 - \alpha - \sum_i \tilde w_i\, d_{\mathrm{TV}}(Z, Z^i)$, where $Z^i$ swaps the test point with point $i$',
        r'\textbf{Teoremă}: acoperirea $\ge 1 - \alpha - \sum_i \tilde w_i\, d_{\mathrm{TV}}(Z, Z^i)$, unde $Z^i$ schimbă punctul de test cu punctul $i$')]),
    (T(r'Under exchangeability the gap is zero; under drift, $d_{\mathrm{TV}}$ is small for recent points, so geometric weights $w_i = \rho^{n+1-i}$ keep it small',
       r'Sub interschimbabilitate abaterea este zero; sub o derivă lentă, $d_{\mathrm{TV}}$ este mic pentru punctele recente, deci ponderile geometrice $w_i = \rho^{n+1-i}$ o păstrează mică'),
     [T(r'effective sample size $\approx 1/(1 - \rho)$: $\rho = 0.99$ uses about 100 recent scores; robustness against variance of the threshold', r'mărimea efectivă a eșantionului $\approx 1/(1 - \rho)$: $\rho = 0{,}99$ folosește aproximativ 100 de scoruri recente; robustețe în schimbul variabilității pragului')]),
    T(r'Covariate shift with known likelihood ratio: weights $w(x) = dP_{\mathrm{test}}/dP_{\mathrm{train}}$ give exact coverage \refTBCR',
      r'Schimbarea distribuției covariabilelor cu raport de verosimilitate cunoscut: ponderile $w(x) = dP_{\mathrm{test}}/dP_{\mathrm{train}}$ dau acoperire exactă \refTBCR')), 'small')

chart(T('Weighted conformal under changepoints', 'Predicția conformală ponderată la puncte de schimbare'), 'ats_ch13_weighted', 'ATS_ch13_conformal_time', [
    T(r'$Y_t = X_t\'\beta_t + \varepsilon_t$, $X_t \sim N(0, I_4)$, $\beta$ changes at $t = 500$ and $t = 1500$; least squares on all past data; prequential absolute residuals as scores; coverage averaged over 200 runs (20-step moving average)',
      r'$Y_t = X_t\'\beta_t + \varepsilon_t$, $X_t \sim N(0, I_4)$, $\beta$ se schimbă la $t = 500$ și $t = 1500$; cele mai mici pătrate pe toate datele trecute; reziduurile absolute prequential ca scoruri; acoperirea mediată pe 200 de rulări (medie mobilă pe 20 de pași)')],
    h='0.48\\textheight')

interp(('the weighted method', 'metodei ponderate'), [
    T(r'Average coverage after the burn-in: standard @{wt.sc}, weighted ($\rho = 0.99$) @{wt.wc}; worst 20-step average @{wt.smin} against @{wt.wmin}',
      r'Acoperirea medie după perioada inițială: standard @{wt.sc}, ponderat ($\rho = 0{,}99$) @{wt.wc}; cea mai slabă medie pe 20 de pași @{wt.smin} față de @{wt.wmin}'),
    T(r'Both collapse at a break, because the least-squares fit is wrong for a while; the weighted threshold forgets the old scores and recovers within about 100 steps',
      r'Ambele se prăbușesc la o ruptură, pentru că estimarea prin cele mai mici pătrate este greșită o vreme; pragul ponderat uită scorurile vechi și își revine în aproximativ 100 de pași'),
    T(r'Price: mean width @{wt.ww} against @{wt.sw}; the guarantee is a bound in terms of $d_{\mathrm{TV}}$, not exact coverage', r'Prețul: lățimea medie @{wt.ww} față de @{wt.sw}; garanția este o margine exprimată prin $d_{\mathrm{TV}}$, nu o acoperire exactă')])

D.frame(T('EnbPI: ensembles without data splitting', 'EnbPI: ansambluri fără împărțirea datelor'), items(
    (T(r'\refXX, \refXXb: fit $B$ models on bootstrap samples (blocks, to respect dependence) of the training period',
       r'\refXX, \refXXb: se estimează $B$ modele pe eșantioane bootstrap (pe blocuri, pentru a respecta dependența) ale perioadei de antrenare'),
     [T(r'leave-one-out residuals: for point $i$, aggregate only the models whose bootstrap sample excluded $i$', r'reziduuri leave-one-out: pentru punctul $i$ se agregă doar modelele al căror eșantion bootstrap l-a exclus pe $i$'),
      T(r'interval at $t$: $\hat f(x_t) \pm$ the $(1 - \alpha)$ quantile of the last $T$ absolute residuals; after $y_t$ is observed, its residual enters the window and the oldest leaves',
        r'intervalul la $t$: $\hat f(x_t) \pm$ cuantila $(1 - \alpha)$ a ultimelor $T$ reziduuri absolute; după ce $y_t$ este observat, reziduul lui intră în fereastră, iar cel mai vechi iese')]),
    (T('No refitting at each step, no calibration split: efficient for long streams', 'Fără reestimare la fiecare pas, fără împărțire pentru calibrare: eficient pe fluxuri lungi'), []),
    T('Guarantee: asymptotic, conditional coverage if the errors are stationary and strongly mixing and the ensemble is consistent; designed for energy series (solar and wind)',
      'Garanția: acoperire asimptotică, condiționată, dacă erorile sînt staționare și puternic mixing, iar ansamblul este consistent; gîndit pentru serii de energie (solară și eoliană)')), 'small')

D.frame(T('Adaptive conformal inference', 'Inferența conformală adaptivă'), items(
    (T(r'\refGC: use level $\alpha_t$ at time $t$, $q_t$ = the conformal $(1 - \alpha_t)$ quantile of recent scores, then $\alpha_{t+1} = \alpha_t + \gamma(\alpha - \mathrm{err}_t)$',
       r'\refGC: se folosește nivelul $\alpha_t$ la momentul $t$, $q_t$ = cuantila conformală $(1 - \alpha_t)$ a scorurilor recente, apoi $\alpha_{t+1} = \alpha_t + \gamma(\alpha - \mathrm{err}_t)$'),
     [T(r'a miss lowers $\alpha_t$ (wider sets); a hit raises it; $\alpha_t \le 0$ gives $q_t = +\infty$ (the whole line), $\alpha_t \ge 1$ the empty set',
        r'o ratare scade $\alpha_t$ (mulțimi mai largi); o acoperire îl crește; $\alpha_t \le 0$ dă $q_t = +\infty$ (toată dreapta), $\alpha_t \ge 1$ mulțimea vidă')]),
    (T(r'\textbf{Theorem}: for any sequence of data, $\Big|\frac1T\sum_{t=1}^T\mathrm{err}_t - \alpha\Big| \le \frac{\max\{\alpha_1, 1 - \alpha_1\} + \gamma}{\gamma T}$',
       r'\textbf{Teoremă}: pentru orice șir de date, $\Big|\frac1T\sum_{t=1}^T\mathrm{err}_t - \alpha\Big| \le \frac{\max\{\alpha_1, 1 - \alpha_1\} + \gamma}{\gamma T}$'),
     [T(r'proof: $\alpha_t$ stays in $[-\gamma, 1 + \gamma]$ and $\alpha_{T+1} - \alpha_1 = \gamma\sum_t(\alpha - \mathrm{err}_t)$; divide by $\gamma T$',
        r'demonstrație: $\alpha_t$ rămîne în $[-\gamma, 1 + \gamma]$ și $\alpha_{T+1} - \alpha_1 = \gamma\sum_t(\alpha - \mathrm{err}_t)$; se împarte la $\gamma T$')]),
    T(r'Long-run frequency, not conditional coverage: an adversary-proof average. Choosing $\gamma$ adaptively: AgACI \refZaf, DtACI \refGCb; ACI for VaR: Chapter 9',
      r'Frecvență pe termen lung, nu acoperire condiționată: o medie rezistentă la orice adversar. Alegerea adaptivă a lui $\gamma$: AgACI \refZaf, DtACI \refGCb; ACI pentru VaR: Capitolul 9')), 'small')

chart(T('ACI on stock-market volatility', 'ACI pe volatilitatea bursieră'), 'ats_ch13_aci', 'ATS_ch13_conformal_time', [
    T(r'Design of \refGC: $V_t = r_t^2$, $\hat\sigma_t^2$ from a GARCH(1,1) fitted on the previous 1250 days, score $|V_t - \hat\sigma_t^2|/\hat\sigma_t^2$, $\alpha = 0.1$, $\gamma = 0.005$; local coverage over 500 days; evaluation from @{ac.sp.first}',
      r'Designul din \refGC: $V_t = r_t^2$, $\hat\sigma_t^2$ dintr-un GARCH(1,1) estimat pe ultimele 1250 de zile, scorul $|V_t - \hat\sigma_t^2|/\hat\sigma_t^2$, $\alpha = 0{,}1$, $\gamma = 0{,}005$; acoperirea locală pe 500 de zile; evaluare din @{ac.sp.first}')],
    h='0.46\\textheight')

interp(('ACI on volatility', 'ACI pe volatilitate'), [
    T(r'Overall coverage, S\&P 500: static @{ac.sp.st}, rolling @{ac.sp.ro}, ACI @{ac.sp.ac}; BET: @{ac.bet.st}, @{ac.bet.ro}, @{ac.bet.ac}; NVIDIA: @{ac.nv.st}, @{ac.nv.ro}, @{ac.nv.ac}',
      r'Acoperirea totală, S\&P 500: static @{ac.sp.st}, mobil @{ac.sp.ro}, ACI @{ac.sp.ac}; BET: @{ac.bet.st}, @{ac.bet.ro}, @{ac.bet.ac}; NVIDIA: @{ac.nv.st}, @{ac.nv.ro}, @{ac.nv.ac}'),
    T(r'Local coverage of the static method ranges from @{ac.sp.stmin} to @{ac.sp.stmax} (S\&P 500); ACI stays within @{ac.sp.acmin} -- @{ac.sp.acmax}',
      r'Acoperirea locală a metodei statice variază între @{ac.sp.stmin} și @{ac.sp.stmax} (S\&P 500); ACI rămîne între @{ac.sp.acmin} și @{ac.sp.acmax}'),
    T(r'Christoffersen conditional coverage of the misses (S\&P 500): static $p$ @{ac.sp.stcc}, ACI $p$ @{ac.sp.accc}: a calibration fixed on 2005--2009 is too wide afterwards; updating restores both the frequency and the independence of misses',
      r'Acoperirea condiționată Christoffersen pentru ratări (S\&P 500): static $p$ @{ac.sp.stcc}, ACI $p$ @{ac.sp.accc}: o calibrare fixată pe 2005--2009 este prea largă ulterior; actualizarea reface atît frecvența, cît și independența ratărilor')])

chart(T('The step size of ACI', 'Pasul ACI'), 'ats_ch13_aci_gamma', 'ATS_ch13_conformal_time', [
    T(r'S\&P 500 scores of the previous chart: the level $\alpha_t$ for $\gamma = 0.001$, 0.005 and 0.05',
      r'Scorurile S\&P 500 din graficul anterior: nivelul $\alpha_t$ pentru $\gamma = 0{,}001$, 0,005 și 0,05')],
    h='0.46\\textheight')

interp(('the step size', 'pasului'), [
    T(r'Miss rates @{ag.m1}, @{ag.m2}, @{ag.m3} against the bounds @{ag.b1}, @{ag.b2}, @{ag.b3} ($T = @{ag.T}$): the theorem holds with room to spare',
      r'Frecvențele ratărilor @{ag.m1}, @{ag.m2}, @{ag.m3} față de marginile @{ag.b1}, @{ag.b2}, @{ag.b3} ($T = @{ag.T}$): teorema este respectată cu o marjă largă'),
    T(r'Large $\gamma$: $\alpha_t$ ranges @{ag.lo3} -- @{ag.hi3}, infinite intervals on @{ag.inf3}\% of days; small $\gamma$: slow reaction, long runs of misses after a shock',
      r'$\gamma$ mare: $\alpha_t$ variază între @{ag.lo3} și @{ag.hi3}, intervale infinite în @{ag.inf3}\% din zile; $\gamma$ mic: reacție lentă, serii lungi de ratări după un șoc'),
    T('$\\gamma$ trades adaptivity against stability: tune it on a past window, or let DtACI aggregate several values', '$\\gamma$ echilibrează adaptivitatea și stabilitatea: alegeți-l pe o fereastră trecută sau lăsați DtACI să agrege mai multe valori')])

D.frame(T('Conformal PID control', 'Controlul PID conformal'), items(
    (T(r'\refACT: \textbf{quantile tracking} (P): $q_{t+1} = q_t + \eta(\mathrm{err}_t - \alpha)$, i.e.\ online gradient descent on the pinball loss of the score',
       r'\refACT: \textbf{urmărirea cuantilei} (P): $q_{t+1} = q_t + \eta(\mathrm{err}_t - \alpha)$, adică coborîre pe gradient online pe pierderea pinball a scorului'),
     [T(r'\textbf{Proposition}: if $S_t \in [0, B]$, then $\big|\frac1T\sum_t(\mathrm{err}_t - \alpha)\big| \le (B + \eta)/(\eta T)$: the threshold moves on the scale of the scores, not of $\alpha$',
        r'\textbf{Propoziție}: dacă $S_t \in [0, B]$, atunci $\big|\frac1T\sum_t(\mathrm{err}_t - \alpha)\big| \le (B + \eta)/(\eta T)$: pragul se mișcă pe scala scorurilor, nu a lui $\alpha$')]),
    (T(r'\textbf{Integrator} (I): add $r_t\big(\sum_{i \le t}(\mathrm{err}_i - \alpha)\big)$, $r_t(x) = K_I\tan\big(x\log t/(tC_{\mathrm{sat}})\big)$: reacts to accumulated coverage error, saturates to keep the guarantee',
       r'\textbf{Integratorul} (I): se adaugă $r_t\big(\sum_{i \le t}(\mathrm{err}_i - \alpha)\big)$, $r_t(x) = K_I\tan\big(x\log t/(tC_{\mathrm{sat}})\big)$: reacționează la eroarea de acoperire acumulată și se saturează pentru a păstra garanția'), []),
    (T(r'\textbf{Scorecaster} (D-like): a model that forecasts the next score from its past (seasonality, trends in the errors) and is added to the threshold',
       r'\textbf{Prognozatorul de scor} (asemănător termenului D): un model care prognozează scorul următor din trecutul lui (sezonalitate, tendințe ale erorilor) și se adaugă la prag'), []),
    T('ACI is the special case that tracks the level instead of the quantile; PID borrows its vocabulary from control engineering: proportional, integral, derivative',
      'ACI este cazul particular care urmărește nivelul în loc de cuantilă; PID își ia vocabularul din ingineria controlului: proporțional, integral, derivat')), 'small')

chart(T('Online methods on Romanian load', 'Metode online pe consumul României'), 'ats_ch13_pid', 'ATS_ch13_conformal_time', [
    T(r'90\% day-ahead intervals around the Chronos-Bolt median, one score stream per hour (24 streams), calibration window 91 days; EnbPI on the expert ARX regressors (ridge, 20 block-bootstrap models); evaluation from @{pd.first}',
      r'Intervale de 90\% pentru ziua următoare în jurul medianei Chronos-Bolt, cîte un flux de scoruri pe oră (24 de fluxuri), fereastra de calibrare 91 de zile; EnbPI pe regresorii ARX expert (ridge, 20 de modele bootstrap pe blocuri); evaluare din @{pd.first}')],
    h='0.48\\textheight')

interp(('the online methods', 'metodelor online'), [
    T(r'Coverage: static @{pd.st}, rolling @{pd.ro}, ACI @{pd.ac}, quantile tracking @{pd.qt}, PID @{pd.pid}, EnbPI @{pd.en}',
      r'Acoperirea: static @{pd.st}, mobil @{pd.ro}, ACI @{pd.ac}, urmărirea cuantilei @{pd.qt}, PID @{pd.pid}, EnbPI @{pd.en}'),
    T(r'Mean width (GW): @{pd.wst}, @{pd.wro}, @{pd.wac}, @{pd.wqt}, @{pd.wpid}, @{pd.wen}; worst 30-day coverage: static @{pd.lst}, PID @{pd.lpid}',
      r'Lățimea medie (GW): @{pd.wst}, @{pd.wro}, @{pd.wac}, @{pd.wqt}, @{pd.wpid}, @{pd.wen}; cea mai slabă acoperire pe 30 de zile: static @{pd.lst}, PID @{pd.lpid}'),
    T(r'Over the whole period every method except EnbPI is close to 90\%; the differences are in the dips after seasonal transitions and in width, where PID is best on both counts',
      r'Pe toată perioada, toate metodele în afară de EnbPI sînt aproape de 90\%; diferențele țin de scăderile după tranzițiile sezoniere și de lățime, iar PID este cel mai bun la ambele'),
    T('EnbPI centres the band on its own ridge ensemble, less accurate than the base forecast: narrower intervals, lower coverage', 'EnbPI centrează banda pe propriul ansamblu ridge, mai puțin precis decît prognoza de bază: intervale mai înguste, acoperire mai mică')])

D.frame(T('Coverage diagnostics', 'Diagnosticarea acoperirii'), items(
    (T(r'\textbf{Unconditional}: miss rate and Kupiec \refKup; \textbf{independence} of misses: Christoffersen \refChr (Chapter 9)', r'\textbf{Necondiționat}: frecvența ratărilor și testul Kupiec \refKup; \textbf{independența} ratărilor: Christoffersen \refChr (Capitolul 9)'),
     [T(r'regression check in the spirit of the DQ test \refEM: regress $\mathrm{err}_t - \alpha$ on lagged misses and on the predicted width', r'o verificare prin regresie în spiritul testului DQ \refEM: regresia lui $\mathrm{err}_t - \alpha$ pe ratările decalate și pe lățimea prognozată')]),
    (T('\\textbf{Local}: rolling coverage; coverage by bins of a variable known at the origin (predicted volatility, hour, regime): the empirical counterpart of conditional coverage', '\\textbf{Local}: acoperirea pe ferestre mobile; acoperirea pe clase ale unei variabile cunoscute la origine (volatilitatea prognozată, ora, regimul): echivalentul empiric al acoperirii condiționate'), []),
    (T(r'\textbf{Sharpness}: mean width and the interval score $W + \frac{2}{\alpha}(\ell - y)\mathbf 1\{y < \ell\} + \frac{2}{\alpha}(y - u)\mathbf 1\{y > u\}$ \refWin, \refGR, a proper score for central intervals',
       r'\textbf{Precizia}: lățimea medie și scorul de interval $W + \frac{2}{\alpha}(\ell - y)\mathbf 1\{y < \ell\} + \frac{2}{\alpha}(y - u)\mathbf 1\{y > u\}$ \refWin, \refGR, un scor propriu pentru intervale centrale'), []),
    T('Report all three: a method that is valid but twice as wide is not a better method', 'Raportați toate trei: o metodă validă, dar de două ori mai largă, nu este o metodă mai bună')), 'small')

chart(T('Coverage by volatility regime', 'Acoperirea pe regimuri de volatilitate'), 'ats_ch13_condcov', 'ATS_ch13_conformal_time', [
    T(r'S\&P 500, 90\% volatility intervals of the ACI chart: coverage by tercile of the GARCH variance forecast and on the day after a miss',
      r'S\&P 500, intervalele de volatilitate de 90\% din graficul ACI: acoperirea pe terțile ale varianței prognozate de GARCH și în ziua de după o ratare')],
    h='0.46\\textheight')

interp(('conditional coverage', 'acoperirii condiționate'), [
    T(r'Static: @{cc.st0} (low variance), @{cc.st2} (high), @{cc.st3} after a miss; ACI: @{cc.ac0}, @{cc.ac2}, @{cc.ac3}',
      r'Static: @{cc.st0} (varianță mică), @{cc.st2} (mare), @{cc.st3} după o ratare; ACI: @{cc.ac0}, @{cc.ac2}, @{cc.ac3}'),
    T('Coverage is almost flat across volatility terciles and after a miss, for every method: dividing by the GARCH variance makes the score close to pivotal',
      'Acoperirea este aproape constantă pe terțile de volatilitate și după o ratare, pentru toate metodele: împărțirea la varianța GARCH face scorul aproape pivotal'),
    T('Contrast: with the raw score $|r_t|$ (Seminar 13, B3) misses cluster in turbulent years whatever the calibration; conditional coverage is a property of the score, not of the conformal step',
      'Contrast: cu scorul brut $|r_t|$ (Seminarul 13, B3) ratările se grupează în anii agitați, oricare ar fi calibrarea; acoperirea condiționată este o proprietate a scorului, nu a pasului conformal')])

D.recap(('conformal methods for time series', 'metodele conformale pentru serii de timp'), [
    T('Weighted conformal: a coverage bound in total variation; geometric weights adapt to drift', 'Conformal ponderat: o margine a acoperirii exprimată prin variația totală; ponderile geometrice se adaptează derivei'),
    T('EnbPI: bootstrap ensembles and a sliding residual window, asymptotic validity under mixing', 'EnbPI: ansambluri bootstrap și o fereastră mobilă de reziduuri, validitate asimptotică sub mixing'),
    T('ACI and PID: feedback on misses gives long-run coverage for any sequence; conditional coverage must still be tested', 'ACI și PID: reacția la ratări dă acoperire pe termen lung pentru orice șir; acoperirea condiționată trebuie totuși testată')])

# =============================================================================
# 8. CALIBRAREA FOUNDATION MODELS
# =============================================================================
D.section('Calibrating foundation-model intervals', 'Calibrarea intervalelor produse de foundation models')

D.frame(T('The need to calibrate foundation-model quantiles', 'Nevoia de calibrare a cuantilelor foundation models'), items(
    (T(r'Pretrained quantiles are calibrated on the corpus distribution, not on your series: miscalibration is the default, in either direction',
       r'Cuantilele preantrenate sînt calibrate pe distribuția corpusului, nu pe seria dumneavoastră: calibrarea greșită este situația implicită, în ambele sensuri'), []),
    (T(r'Most models output only 10\%--90\%: a 95\% interval or VaR 1\% requires extrapolation beyond the trained levels',
       r'Majoritatea modelelor dau doar cuantile de 10\%--90\%: un interval de 95\% sau VaR 1\% cere extrapolare dincolo de nivelurile antrenate'), []),
    (T(r'Recipe: online CQR on the model\'s own band, score $S_t = \max\{\hat q_{0.1,t} - y_t, y_t - \hat q_{0.9,t}\}$; ACI chooses the threshold for any target level ($80\%$ or $95\%$)',
       r'Rețeta: CQR online pe banda proprie a modelului, scorul $S_t = \max\{\hat q_{0.1,t} - y_t, y_t - \hat q_{0.9,t}\}$; ACI alege pragul pentru orice nivel-țintă ($80\%$ sau $95\%$)'),
     [T(r'one-sided version for VaR: $S_t = \hat q_{0.1,t} - y_t$, threshold at level $\alpha$; the VaR is $-(\hat q_{0.1,t} - q_t)$', r'varianta unilaterală pentru VaR: $S_t = \hat q_{0.1,t} - y_t$, pragul la nivelul $\alpha$; VaR este $-(\hat q_{0.1,t} - q_t)$')]),
    T(r'Further reading on conformal VaR recalibration of foundation models: \refCO; \refTV', r'Lectură suplimentară despre recalibrarea conformală a VaR pentru foundation models: \refCO; \refTV')), 'small')

chart(T('Raw and conformal coverage of foundation models', 'Acoperirea brută și cea conformală a foundation models'), 'ats_ch13_fm_calib', 'ATS_ch13_calibration', [
    T(r'Coverage of the raw 10--90\% band and of the online-CQR 80\% and 95\% intervals (ACI, window 250, $\gamma = 0.005$): Romanian load (24 hourly streams), Bitcoin log RV, EU inflation at $h = 1$ (27 streams), BET daily returns',
      r'Acoperirea benzii brute de 10--90\% și a intervalelor CQR online de 80\% și 95\% (ACI, fereastra 250, $\gamma = 0{,}005$): consumul României (24 de fluxuri orare), log RV Bitcoin, inflația UE la $h = 1$ (27 de fluxuri), randamentele zilnice BET')],
    h='0.48\\textheight')

interp(('the calibration', 'calibrării'), [
    T(r'Raw 80\% bands: load @{fc.l.lo}--@{fc.l.hi}\%, Bitcoin @{fc.b.lo}--@{fc.b.hi}\%, inflation @{fc.i.lo}--@{fc.i.hi}\%, BET returns @{fc.r.lo}--@{fc.r.hi}\% across the four models',
      r'Benzile brute de 80\%: consum @{fc.l.lo}--@{fc.l.hi}\%, Bitcoin @{fc.b.lo}--@{fc.b.hi}\%, inflație @{fc.i.lo}--@{fc.i.hi}\%, randamente BET @{fc.r.lo}--@{fc.r.hi}\% pentru cele patru modele'),
    T(r'After online CQR: 80\% intervals cover @{fc.c80lo}--@{fc.c80hi}\%, 95\% intervals @{fc.c95lo}--@{fc.c95hi}\% in every task',
      r'După CQR online: intervalele de 80\% acoperă @{fc.c80lo}--@{fc.c80hi}\%, cele de 95\% @{fc.c95lo}--@{fc.c95hi}\% în toate sarcinile'),
    T(r'Raw bands miss in both directions (too narrow: Chronos-2 on load; too wide: TimesFM on inflation); the conformal step widens or narrows them, with a mean width between @{fc.wlo} and @{fc.whi} times the raw width, and reaches 95\% from models that output only deciles',
      r'Benzile brute greșesc în ambele sensuri (prea înguste: Chronos-2 la consum; prea largi: TimesFM la inflație); pasul conformal le lărgește sau le îngustează, cu o lățime medie între @{fc.wlo} și @{fc.whi} ori lățimea brută, și ajunge la 95\% pornind de la modele care produc doar decile')])

chart(T('Value at Risk from foundation models', 'Valoarea la risc din foundation models'), 'ats_ch13_fm_var', 'ATS_ch13_calibration', [
    T(r'VaR 1\% exceedances, BET and S\&P 500 from @{fv.first} (@{fv.n} days): GARCH-$t$ (rolling 1000 days, Chapter 9), Chronos-2 raw and with ACI, deciles of the other models extended by a one-sided conformal shift',
      r'Depășirile VaR 1\%, BET și S\&P 500 din @{fv.first} (@{fv.n} zile): GARCH-$t$ (fereastră mobilă de 1000 de zile, Capitolul 9), Chronos-2 brut și cu ACI, decilele celorlalte modele extinse printr-o deplasare conformală unilaterală')],
    h='0.48\\textheight')

interp(('the VaR backtest', 'backtesting-ului VaR'), [
    T(r'BET, VaR 1\%: GARCH-$t$ @{fv.b.g}\% (Kupiec $p$ @{fv.b.gk}), Chronos-2 raw @{fv.b.c}\% ($p$ @{fv.b.ck}), Chronos-2 + ACI @{fv.b.a}\% ($p$ @{fv.b.ak}), TimesFM + conformal @{fv.b.t}\%',
      r'BET, VaR 1\%: GARCH-$t$ @{fv.b.g}\% (Kupiec $p$ @{fv.b.gk}), Chronos-2 brut @{fv.b.c}\% ($p$ @{fv.b.ck}), Chronos-2 + ACI @{fv.b.a}\% ($p$ @{fv.b.ak}), TimesFM + conformal @{fv.b.t}\%'),
    T(r'S\&P 500: GARCH-$t$ @{fv.s.g}\% (Kupiec $p$ @{fv.s.gk}), Chronos-2 raw @{fv.s.c}\% ($p$ @{fv.s.ck}), + ACI @{fv.s.a}\% ($p$ @{fv.s.ak}, Christoffersen $p$ @{fv.s.acc})',
      r'S\&P 500: GARCH-$t$ @{fv.s.g}\% (Kupiec $p$ @{fv.s.gk}), Chronos-2 brut @{fv.s.c}\% ($p$ @{fv.s.ck}), + ACI @{fv.s.a}\% ($p$ @{fv.s.ak}, $p$ Christoffersen @{fv.s.acc})'),
    T(r'Calibration fixes the exceedance rate of every model; it does not add tail information: the conformally extended deciles have a larger quantile loss than GARCH-$t$ (BET, Chronos-Bolt: DM $t = @{fv.b.bdm}$), while Chronos-2, trained on 1\% quantiles, does not ($t = @{fv.b.adm}$)',
      r'Calibrarea corectează rata de depășire a oricărui model; nu adaugă informație despre coadă: decilele extinse conformal au o pierdere cuantilică mai mare decît GARCH-$t$ (BET, Chronos-Bolt: DM $t = @{fv.b.bdm}$), în timp ce Chronos-2, antrenat pe cuantile de 1\%, nu are ($t = @{fv.b.adm}$)')])

D.recap(('calibration', 'calibrarea'), [
    T('Treat foundation-model quantiles as scores to be calibrated, not as probabilities', 'Tratați cuantilele foundation models ca scoruri de calibrat, nu ca probabilități'),
    T('Online CQR with ACI gives target coverage at any level, including beyond the trained quantiles', 'CQR online cu ACI dă acoperirea-țintă la orice nivel, inclusiv dincolo de cuantilele antrenate'),
    T('Backtest calibrated VaR as in Chapter 9: frequency, independence and loss', 'Testați VaR calibrat ca în Capitolul 9: frecvență, independență și pierdere')])

# =============================================================================
# 9. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Do time-series foundation models beat domain-specific econometric models on Central and Eastern European data after their release dates, once multiplicity is accounted for?',
       'Întrec foundation models pentru serii de timp modelele econometrice de domeniu pe datele din Europa Centrală și de Est, într-o fereastră de după lansarea lor și cu corecție pentru testarea multiplă?'),
     [T(r'formal: $H_0$: equal expected loss (pooled over pre-registered series) of the best foundation model and the best domain model, in a window that starts after every model release',
        r'formal: $H_0$: pierderea așteptată egală (agregată pe serii preînregistrate) a celui mai bun foundation model și a celui mai bun model de domeniu, într-o fereastră care începe după lansarea tuturor modelelor'),
      T('falsified by a pooled DM test at 5\\% and an MCS that excludes one side, on series and horizons fixed before the data arrive',
        'infirmată de un test DM agregat la 5\\% și de un MCS care exclude una dintre părți, pe serii și orizonturi fixate înainte de sosirea datelor')]),
    (T('Why it matters: central banks and grid operators consider replacing tuned models by zero-shot ones; published wins often come from a favourable choice of series',
       'De ce contează: băncile centrale și operatorii de rețea iau în calcul înlocuirea modelelor ajustate cu modele zero-shot; cîștigurile publicate provin adesea dintr-o alegere favorabilă a seriilor'),
     [T(r'literature to start from: \refAks, \refShc, \refMey, \refPE, \refBri', r'literatura de pornire: \refAks, \refShc, \refMey, \refPE, \refBri')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature',
       'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed or arXiv papers since 2024 that evaluate time-series foundation models only after their release dates; give arXiv IDs or DOIs.} Then check every identifier',
        r'\textbf{literatura}: \aiprompt{Listează articole recenzate sau de pe arXiv din 2024 încoace care evaluează foundation models pentru serii de timp doar după datele lor de lansare; dă identificatorii arXiv sau DOI.} Apoi verificați fiecare identificator'),
      T(r'\textbf{hypothesis}: \aiprompt{Write a pre-registration: series, origins, horizons, losses, baselines, the pooled test and the MCS level.}',
        r'\textbf{ipoteza}: \aiprompt{Scrie o preînregistrare: seriile, originile, orizonturile, funcțiile de pierdere, modelele de referință, testul agregat și nivelul MCS.}'),
      T(r'\textbf{code and replication}: ask for a wrapper that returns quantiles at fixed levels for each model; replicate a known number first (the Chronos-Bolt quantile range, our load MAE)',
        r'\textbf{cod și replicare}: cereți o funcție care întoarce cuantile la niveluri fixe pentru fiecare model; reproduceți întîi o cifră cunoscută (domeniul cuantilelor Chronos-Bolt, MAE-ul nostru pentru consum)'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee: list every way this benchmark could favour the foundation models.}',
        r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră toate felurile în care acest benchmark ar putea favoriza foundation models.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (arXiv ID or DOI resolves, the title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (identificatorul arXiv sau DOI funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('Release dates and training cutoffs of every model, from the model cards, against the start of the evaluation window', 'Datele de lansare și datele-limită de antrenare ale fiecărui model, din fișele modelelor, comparate cu începutul ferestrei de evaluare'),
    T('Quantile levels actually produced by each model (a request for 1\\% may silently return 10\\%)', 'Nivelurile de cuantile produse efectiv de fiecare model (o cerere pentru 1\\% poate întoarce, fără avertisment, 10\\%)'),
    T('Baselines tuned with the same care; the context available to every model is the same', 'Modelele de referință ajustate cu aceeași grijă; contextul disponibil este același pentru toate modelele'),
    T('Multiplicity: number of series, horizons and models tested; the pooled test and adjusted $p$-values reported', 'Multiplicitatea: numărul de serii, orizonturi și modele testate; raportarea testului agregat și a valorilor $p$ ajustate')), 'small')

chart(T('Mini-case: how much can the choice of benchmark change the verdict?', 'Mini studiu de caz: cît poate schimba verdictul alegerea benchmark-ului?'), 'ats_ch13_ai_case', 'ATS_ch13_benchmark', [
    T(r'DM--HLN statistics of Chronos-2 against AR($p$) at $h = 12$ on @{ai.reps} random benchmarks of @{ai.k} EU countries and @{ai.y} years of origins, and on the full panel',
      r'Statisticile DM--HLN ale Chronos-2 față de AR($p$) la $h = 12$ pe @{ai.reps} de benchmark-uri aleatoare cu @{ai.k} țări UE și @{ai.y} ani de origini și pe întregul panel'),
    T(r'@{ai.win}\% of the random benchmarks declare Chronos-2 significantly better and @{ai.lose}\% significantly worse; the full panel gives $t = @{ai.t}$ ($p$ @{ai.p}). An AI summary of one such paper as evidence for (or against) foundation models is wrong; only the pre-registered panel answers',
      r'@{ai.win}\% dintre benchmark-urile aleatoare declară Chronos-2 semnificativ mai bun, iar @{ai.lose}\% semnificativ mai slab; panelul întreg dă $t = @{ai.t}$ ($p$ @{ai.p}). Un rezumat AI care prezintă o astfel de lucrare ca dovadă pentru (sau împotriva) foundation models greșește; doar panelul preînregistrat răspunde')],
    h='0.4\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{A pre-registered, post-release benchmark of foundation models for CEE macro and risk, with conformal calibration}',
       r'\textbf{Un benchmark preînregistrat, de după lansare, al foundation models pentru macroeconomia și riscul din Europa Centrală și de Est, cu calibrare conformală}'),
     [T(r'replicate: the zero-shot protocol of \refAns (WQL, MASE, geometric means) and the ACI volatility design of \refGC on our data',
        r'replicați: protocolul zero-shot din \refAns (WQL, MASE, medii geometrice) și designul ACI pentru volatilitate din \refGC pe datele noastre'),
      T('extend: Romanian, Polish, Hungarian and Czech inflation, load and stock indices; covariates in context (energy prices, calendars); online CQR to 95\\% and VaR 1\\%; pooled tests with Holm and BH',
        'extindeți: inflația, consumul și indicii bursieri din România, Polonia, Ungaria și Cehia; covariabile în context (prețurile energiei, calendare); CQR online pentru 95\\% și VaR 1\\%; teste agregate cu Holm și BH'),
      T('pre-register: series, origins after 1 November 2025, horizons, losses, baselines and the decision rule; forecasts for the next months written down before the data arrive',
        'preînregistrați: seriile, originile după 1 noiembrie 2025, orizonturile, funcțiile de pierdere, modelele de referință și regula de decizie; prognozele pentru lunile următoare se notează înainte de sosirea datelor')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Foundation models amortise estimation over a corpus; design choices (scaling, patches, quantile range) set what they can and cannot forecast', 'Foundation models amortizează estimarea pe un corpus; alegerile de proiectare (scalarea, patch-urile, domeniul cuantilelor) stabilesc ce pot și ce nu pot prognoza'),
    T('On our data the best zero-shot model is competitive with domain models; gains depend on the task and do not survive cherry-picking', 'Pe datele noastre cel mai bun model zero-shot este competitiv cu modelele de domeniu; cîștigurile depind de sarcină și nu rezistă alegerii selective'),
    T('Evaluate after the release, pool across series, correct for multiplicity', 'Evaluați după lansare, agregați pe serii, corectați pentru multiplicitate'),
    T('Conformal prediction gives finite-sample marginal coverage under exchangeability; under dependence, weights, ensembles and feedback restore long-run coverage', 'Predicția conformală dă acoperire marginală în eșantioane finite sub interschimbabilitate; sub dependență, ponderile, ansamblurile și reacția la erori refac acoperirea pe termen lung'),
    T('Conditional coverage is impossible in general: diagnose it with Christoffersen tests and coverage by regime', 'Acoperirea condiționată este imposibilă în general: diagnosticați-o cu testele Christoffersen și cu acoperirea pe regimuri')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('Why can Chronos not forecast a value above $15s$?', 'De ce nu poate Chronos să prognozeze o valoare peste $15s$?'),
        T('Why does a stationary AR(1) violate exchangeability?', 'De ce încalcă un AR(1) staționar interschimbabilitatea?'),
        T('What is the law of the coverage of split conformal given the calibration set?', 'Care este legea acoperirii split conformal condiționată de setul de calibrare?'),
        T('Which quantity stays bounded in the proof of the ACI theorem?', 'Ce mărime rămîne mărginită în demonstrația teoremei ACI?'),
        T('Why is a post-release window necessary in a foundation-model benchmark?', 'De ce este necesară o fereastră de după lansare într-un benchmark al foundation models?'))),
    block(T('Next: Chapter 14', 'Urmează: Capitolul 14'), items(
        T('Causal inference for time series', 'Inferență cauzală pentru serii de timp'),
        T('Granger and structural causality, causal discovery, policy evaluation', 'cauzalitatea Granger și cea structurală, descoperirea relațiilor cauzale, evaluarea politicilor'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: proof of split conformal coverage', 'Anexă: demonstrația acoperirii split conformal'), items(
    T(r'Condition on the training set, so $\hat\mu$ and $s$ are fixed; exchangeability of $Z_1, \dots, Z_{n+1}$ implies exchangeability of $S_1, \dots, S_{n+1}$',
      r'Condiționăm pe setul de antrenare, astfel încît $\hat\mu$ și $s$ sînt fixate; interschimbabilitatea lui $Z_1, \dots, Z_{n+1}$ implică interschimbabilitatea lui $S_1, \dots, S_{n+1}$'),
    T(r'With no ties, the rank $R$ of $S_{n+1}$ among $S_1, \dots, S_{n+1}$ is uniform on $\{1, \dots, n + 1\}$ (every ordering is equally likely)',
      r'Fără egalități, rangul $R$ al lui $S_{n+1}$ printre $S_1, \dots, S_{n+1}$ este uniform pe $\{1, \dots, n + 1\}$ (orice ordonare este la fel de probabilă)'),
    T(r'$S_{n+1} \le S_{(k)}$ (order statistic of the first $n$) $\iff R \le k$; so $\Pr\{Y_{n+1} \in \hat C\} = k/(n + 1)$',
      r'$S_{n+1} \le S_{(k)}$ (statistica de ordine a primelor $n$) $\iff R \le k$; deci $\Pr\{Y_{n+1} \in \hat C\} = k/(n + 1)$'),
    T(r'$k = \lceil (n + 1)(1 - \alpha)\rceil$ gives $1 - \alpha \le k/(n + 1) < 1 - \alpha + 1/(n + 1)$; ties only increase coverage',
      r'$k = \lceil (n + 1)(1 - \alpha)\rceil$ dă $1 - \alpha \le k/(n + 1) < 1 - \alpha + 1/(n + 1)$; egalitățile doar cresc acoperirea'),
    T(r'Given the calibration set, coverage is $F(S_{(k)})$ with $F$ the score distribution; $F(S_i)$ are i.i.d.\ uniform, so $F(S_{(k)}) \sim$ Beta($k$, $n + 1 - k$)',
      r'Condiționat de setul de calibrare, acoperirea este $F(S_{(k)})$, unde $F$ este distribuția scorului; $F(S_i)$ sînt uniforme i.i.d., deci $F(S_{(k)}) \sim$ Beta($k$, $n + 1 - k$)')), 'small')

D.frame(T('Appendix: the two online guarantees', 'Anexă: cele două garanții online'), items(
    (T(r'\textbf{ACI}: if $\alpha_t < 0$ then $q_t = +\infty$ and $\mathrm{err}_t = 0$, so $\alpha_{t+1} = \alpha_t + \gamma\alpha > \alpha_t$; if $\alpha_t > 1$, $\mathrm{err}_t = 1$ and $\alpha_t$ falls',
       r'\textbf{ACI}: dacă $\alpha_t < 0$, atunci $q_t = +\infty$ și $\mathrm{err}_t = 0$, deci $\alpha_{t+1} = \alpha_t + \gamma\alpha > \alpha_t$; dacă $\alpha_t > 1$, $\mathrm{err}_t = 1$ și $\alpha_t$ scade'),
     [T(r'hence $\alpha_t \in [-\gamma, 1 + \gamma]$ for all $t$; summing the updates, $\gamma\big|\sum_{t \le T}(\alpha - \mathrm{err}_t)\big| = |\alpha_{T+1} - \alpha_1| \le \max\{\alpha_1, 1 - \alpha_1\} + \gamma$',
        r'deci $\alpha_t \in [-\gamma, 1 + \gamma]$ pentru orice $t$; însumînd actualizările, $\gamma\big|\sum_{t \le T}(\alpha - \mathrm{err}_t)\big| = |\alpha_{T+1} - \alpha_1| \le \max\{\alpha_1, 1 - \alpha_1\} + \gamma$')]),
    (T(r'\textbf{Quantile tracking}: if $q_t > B$ then $\mathrm{err}_t = 0$ and $q_t$ falls by $\eta\alpha$; if $q_t < 0$ then $\mathrm{err}_t = 1$ and $q_t$ rises',
       r'\textbf{Urmărirea cuantilei}: dacă $q_t > B$, atunci $\mathrm{err}_t = 0$ și $q_t$ scade cu $\eta\alpha$; dacă $q_t < 0$, atunci $\mathrm{err}_t = 1$ și $q_t$ crește'),
     [T(r'hence $q_t \in [-\eta, B + \eta]$ (starting inside); $\eta\sum_{t \le T}(\mathrm{err}_t - \alpha) = q_{T+1} - q_1$, so the average gap is at most $(B + \eta)/(\eta T)$',
        r'deci $q_t \in [-\eta, B + \eta]$ (pornind din interior); $\eta\sum_{t \le T}(\mathrm{err}_t - \alpha) = q_{T+1} - q_1$, deci abaterea medie este cel mult $(B + \eta)/(\eta T)$')]),
    T('Neither proof uses any probability: the guarantees hold for every sequence, which is why they say nothing about conditional coverage',
      'Niciuna dintre demonstrații nu folosește probabilități: garanțiile sînt valabile pentru orice șir, motiv pentru care nu spun nimic despre acoperirea condiționată')), 'small')

D.references(bib(), per=14)

if __name__ == '__main__':
    finalize(D.write(V))
