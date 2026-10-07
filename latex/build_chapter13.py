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
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch13_common import REFS, QLURL, T, V2, day, month, bib, finalize, load, minus_fix   # noqa: E402


def _merge(x):
    """(text, [display, ...]): a displayed formula placed first among the sub-items is written inside the item itself."""
    if isinstance(x, tuple) and x[1] and x[1][0].lstrip('⟦').startswith('\\['):
        x = (x[0] + ' ' + x[1][0].replace("\\'", "'"), x[1][1:])
    return x[0] if isinstance(x, tuple) and not x[1] else x


def items(*xs):
    return _items(*[_merge(x) for x in xs])


def dm(tex):
    """Displayed formula; in RO the decimal points become commas, as in inline math."""
    return T(r'\[ ' + tex + r' \]', r'\[ ' + re.sub(r'(\d)\.(\d)', r'\1{,}\2', tex) + r' \]')


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
    (T('Prerequisites; Seminar 13 comes before this lecture', 'Cunoștințe necesare; Seminarul 13 are loc înaintea acestui curs'),
     [T('TSA, Chapter 11: Chronos, TimesFM, Moirai, zero-shot tests, CRPS and WQL', 'TSA, Capitolul 11: Chronos, TimesFM, Moirai, teste zero-shot, CRPS și WQL'),
      T('Chapter 1 (scoring rules, DM, MCS), Chapter 9 (VaR backtests, ACI for VaR), Chapter 12 (deep architectures)',
        'Capitolul 1 (reguli de scor, DM, MCS), Capitolul 9 (backtesting VaR, ACI pentru VaR), Capitolul 12 (arhitecturi deep)')])), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Explain how a time series foundation model is pretrained: corpus, scaling, tokenisation or patching, output head and loss',
      'Explicați cum se preantrenează un foundation model pentru serii de timp: corpus, scalare, tokenizare sau patching, stratul de ieșire și funcția de pierdere'),
    T('Compare model families and choose between zero-shot use, fine-tuning and in-context covariates',
      'Comparați familiile de modele și alegeți între folosirea zero-shot, fine-tuning și covariabilele în context'),
    T('Design a benchmark without leakage or contamination and test differences across many series with corrections for multiplicity',
      'Proiectați un benchmark fără leakage sau contaminare și testați diferențele pe multe serii cu corecții pentru testarea multiplă'),
    T('Prove the coverage of split conformal and CQR, and state what conformal prediction cannot guarantee',
      'Demonstrați acoperirea metodelor split conformal și CQR și precizați ce nu poate garanta predicția conformală'),
    T('Apply weighted conformal, EnbPI, ACI and conformal PID to dependent data, diagnose coverage and calibrate foundation-model intervals',
      'Aplicați predicția conformală ponderată, EnbPI, ACI și PID conformal pe date dependente, diagnosticați acoperirea și calibrați intervalele produse de foundation models')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T('Foundation models and benchmarks', 'Foundation models și benchmark-uri'),
     [T(r'models: \refAns; \refAnsB; \refDas; \refWoo; \refAue', r'modele: \refAns; \refAnsB; \refDas; \refWoo; \refAue'),
      T(r'benchmarks: \refAks; \refShc; critique and evaluation: \refTan; \refHAB', r'benchmark-uri: \refAks; \refShc; critică și evaluare: \refTan; \refHAB')]),
    (T('Conformal prediction', 'Predicție conformală'),
     [T(r'theory: \refVGSb; \refAB; \refRPC; \refBar', r'teorie: \refVGSb; \refAB; \refRPC; \refBar'),
      T(r'time series: \refGC; \refACT; \refXX; survey of forecasting practice: \refPet', r'serii de timp: \refGC; \refACT; \refXX; sinteză despre practica prognozei: \refPet')]),
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
    (T('Known (TSA, Chapter 11)', 'Cunoscut (TSA, Capitolul 11)'),
     [T('zero-shot use of Chronos, TimesFM, Moirai and Lag-Llama; mean scaling and quantisation in brief',
        'folosirea zero-shot a modelelor Chronos, TimesFM, Moirai și Lag-Llama; scalarea prin medie și cuantizarea, pe scurt'),
      T('pinball loss, CRPS, WQL, MASE; first warnings about contamination', 'pierderea pinball, CRPS, WQL, MASE; primele avertismente despre contaminare')]),
    (T('New: the research toolkit', 'Nou: instrumentele de cercetare'),
     [T('design choices and their consequences (range limits, quantile heads, patching, covariates in context), scaling evidence',
        'alegerile de proiectare și consecințele lor (limitele de domeniu, straturi de cuantile, patching, covariabile în context), dovezile de scalare'),
      T('benchmarks with pre-registered windows after the model releases, tests across many series with Holm and BH corrections',
        'benchmark-uri cu ferestre preînregistrate după lansarea modelelor, teste pe multe serii cu corecțiile Holm și BH'),
      T('conformal theory with proofs, its failure under dependence and the online methods that repair it, with coverage diagnostics',
        'teoria conformală cu demonstrații, eșecul ei sub dependență și metodele online care o corectează, cu diagnosticarea acoperirii')]),
    (T('Case studies: the designs of the papers, on our data', 'Studii de caz: designul din lucrări, pe datele noastre'),
     [T(r'foundation models: \refAns; \refTan', r'foundation models: \refAns; \refTan'),
      T(r'conformal prediction: \refRPC; \refGC; \refBar; \refACT; \refXX', r'predicție conformală: \refRPC; \refGC; \refBar; \refACT; \refXX')])), 'small')

# =============================================================================
# 1. PREANTRENAREA
# =============================================================================
D.section('Pretraining for time series', 'Preantrenarea pentru serii de timp')

D.frame(T('A foundation model as an amortised forecaster (1/2)', 'Un foundation model ca prognozator amortizat (1/2)'), items(
    (T(r'\textbf{Pretraining}: one network is fitted once, by minimising the forecast loss summed over all series and all origins of a large corpus',
       r'\textbf{Preantrenarea}: o singură rețea este estimată o singură dată, prin minimizarea pierderii de prognoză însumate pe toate seriile și pe toate originile unui corpus mare'),
     [r'\[ \hat\theta = \arg\min_\theta \sum_{s \in \mathcal D_{\mathrm{pre}}}\sum_t \ell\big(y^{(s)}_{t+1:t+H},\; f_\theta(y^{(s)}_{t-C+1:t})\big) \]']),
    (T('Notation', 'Notațiile'),
     [T(r'$\mathcal D_{\mathrm{pre}}$: the pretraining corpus, a collection of many series; $s$ indexes the series, $t$ the forecast origin', r'$\mathcal D_{\mathrm{pre}}$: corpusul de preantrenare, o colecție de multe serii; $s$ indexează seriile, $t$ originea prognozei'),
      T(r'$y^{(s)}_{t-C+1:t}$: the last $C$ values of series $s$ (the \textbf{context}); $y^{(s)}_{t+1:t+H}$: its next $H$ values (the \textbf{horizon})', r'$y^{(s)}_{t-C+1:t}$: ultimele $C$ valori ale seriei $s$ (\textbf{contextul}); $y^{(s)}_{t+1:t+H}$: următoarele $H$ valori (\textbf{orizontul})'),
      T(r'$f_\theta$: the network with weights $\theta$; it maps a context to a forecast of the next $H$ values (a distribution or a set of quantiles)', r'$f_\theta$: rețeaua cu ponderile $\theta$; transformă un context într-o prognoză a următoarelor $H$ valori (o distribuție sau un set de cuantile)'),
      T(r'$\ell$: a scoring rule (cross-entropy, pinball, negative log-likelihood); $\hat\theta$: the estimated weights', r'$\ell$: o regulă de scor (entropie încrucișată, pinball, log-verosimilitate negativă); $\hat\theta$: ponderile estimate')]),
    T(r'The term \textbf{foundation model} \refBom: trained once on broad data, then adapted to many tasks', r'Termenul \textbf{foundation model} \refBom: model antrenat o singură dată pe date diverse, apoi adaptat la multe sarcini')), 'small')

D.frame(T('A foundation model as an amortised forecaster (2/2)', 'Un foundation model ca prognozator amortizat (2/2)'), items(
    (T(r'\textbf{Zero-shot} use: the weights stay at $\hat\theta$ and the forecast for a new series $y_1, \dots, y_T$ is the network applied to its last $C$ values',
       r'Folosirea \textbf{zero-shot}: ponderile rămîn $\hat\theta$, iar prognoza pentru o serie nouă $y_1, \dots, y_T$ este rețeaua aplicată ultimelor ei $C$ valori'),
     [r'\[ \hat y_{T+1:T+H} = f_{\hat\theta}(y_{T-C+1:T}) \]',
      T(r'$T$: the last observed period of the target series; no parameter is estimated on it', r'$T$: ultima perioadă observată a seriei-țintă; niciun parametru nu se estimează pe ea')]),
    (T('\\textbf{Amortised inference}', '\\textbf{Inferența amortizată}'),
     [T('a classical model is re-estimated on every new series; here the network performs the estimation step inside its forward pass', 'un model clasic este reestimat pe fiecare serie nouă; aici rețeaua face pasul de estimare în interiorul trecerii înainte (forward pass)'),
      T('the cost of estimation is paid once, during pretraining, and shared by every later forecast', 'costul estimării este plătit o singură dată, la preantrenare, și împărțit între toate prognozele ulterioare')]),
    (T('Global model and foundation model', 'Modelul global și foundation model'),
     [T('a global model of Chapter 12 is trained on the series of one data set', 'un model global din Capitolul 12 este antrenat pe seriile unui singur set de date'),
      T('a foundation model is trained on many data sets, frequencies and domains', 'un foundation model este antrenat pe multe seturi de date, frecvențe și domenii')])), 'small')

D.frame(T('Structure shared across series', 'Structuri comune între serii'), items(
    (T('Shapes recur across domains: seasonal profiles, damped trends, level shifts, volatility clusters, intermittency', 'Formele se repetă între domenii: profiluri sezoniere, tendințe amortizate, salturi de nivel, volatility clustering, intermitență'),
     [T('after scaling, a load curve and a web-traffic curve can look alike: the model learns a prior over shapes', 'după scalare, o curbă de consum și una de trafic web pot arăta la fel: modelul învață o distribuție a priori asupra formelor')]),
    (T('Not shared: the economics of a particular series (a tax change, a policy rule, a holiday calendar)', 'Elemente care nu se transferă: economia unei serii anume (o modificare de taxe, o regulă de politică, un calendar al sărbătorilor)'),
     [T('unless it is passed as a covariate in the context (Chronos-2) or learned by fine-tuning', 'decît dacă este transmisă ca o covariabilă în context (Chronos-2) sau învățată prin fine-tuning')]),
    (T('A no-free-lunch caveat: averaged over all processes no forecaster wins; pretraining helps only if the target resembles the corpus', 'O rezervă de tip „no free lunch”: în medie pe toate procesele niciun prognozator nu cîștigă; preantrenarea ajută doar dacă seria-țintă seamănă cu corpusul'),
     [T('financial returns are close to a martingale difference: little shape to transfer, much to overfit', 'randamentele financiare sînt aproape de o diferență de martingală: puțină structură transferabilă și un risc mare de supraajustare')])), 'small')

D.frame(T('Pretraining data: scale and composition', 'Datele de preantrenare: volum și compoziție'), items(
    (T(r'Chronos \refAns', r'Chronos \refAns'),
     [T('public data sets plus two augmentations', 'seturi de date publice plus două augmentări'),
      T(r'\textbf{TSMixup}: convex mixtures of real series; \textbf{KernelSynth}: series drawn from Gaussian processes with random composite kernels',
        r'\textbf{TSMixup}: combinații convexe de serii reale; \textbf{KernelSynth}: serii extrase din procese gaussiene cu nuclee compuse aleatoare')]),
    (T(r'TimesFM \refDas; Moirai \refWoo', r'TimesFM \refDas; Moirai \refWoo'),
     [T(r'TimesFM: about $10^{11}$ time points: Google Trends, Wikipedia page views, synthetic and public series', r'TimesFM: aproximativ $10^{11}$ momente de timp: Google Trends, accesări Wikipedia, serii sintetice și publice'),
      T('Moirai: LOTSA, over 27 billion observations in nine domains', 'Moirai: LOTSA, peste 27 de miliarde de observații din nouă domenii')]),
    (T(r'Toto \refCoh; GIFT-Eval \refAks', r'Toto \refCoh; GIFT-Eval \refAks'),
     [T('Toto: observability metrics of a cloud provider, a corpus 4--10 times larger than those of earlier models', 'Toto: metrici de observabilitate ale unui furnizor cloud, un corpus de 4--10 ori mai mare decît al modelelor anterioare'),
      T(r'GIFT-Eval: a \textbf{non-leaking} pretraining set of about 230 billion points', r'GIFT-Eval: un set de preantrenare \textbf{fără leakage} de circa 230 de miliarde de puncte')]),
    T('Composition matters more than size for us: economic and financial series are a small, low-frequency share of every corpus',
      'Pentru noi compoziția contează mai mult decît volumul: seriile economice și financiare sînt o parte mică, de frecvență joasă, a oricărui corpus')), 'small')

D.frame(T('Tokenisation: from real values to a vocabulary (1/2)', 'Tokenizarea: de la valori reale la un vocabular (1/2)'), items(
    (T(r'Chronos \refAns, step 1, \textbf{mean scaling}: every value of the context is divided by the mean absolute value of the context',
       r'Chronos \refAns, pasul 1, \textbf{scalarea prin medie}: fiecare valoare din context se împarte la media valorilor absolute din context'),
     [r'\[ \tilde x_t = x_t / s, \qquad s = \frac1C\sum_{t = 1}^{C}|x_t| \]',
      T(r'$x_1, \dots, x_C$: the context values; $s$: the scale, computed on the context only; $\tilde x_t$: the scaled value, close to 1 in absolute value on average',
        r'$x_1, \dots, x_C$: valorile din context; $s$: scala, calculată doar pe context; $\tilde x_t$: valoarea scalată, în medie apropiată de 1 în valoare absolută')]),
    (T(r'Step 2, \textbf{uniform bins}: the interval $[-15, 15]$ is covered by equally spaced bins, one token per bin; with the special tokens the vocabulary has 4096 tokens',
       r'Pasul 2, \textbf{intervale egale}: intervalul $[-15, 15]$ este acoperit de intervale egale, cîte un token pentru fiecare; împreună cu token-urile speciale, vocabularul are 4096 de token-uri'),
     [T(r'each scaled value is replaced by the token of the bin that contains it', r'fiecare valoare scalată este înlocuită cu token-ul intervalului care o conține')]),
    (T(r'Step 3: a language model (T5) trained with \textbf{cross-entropy} predicts the next token',
       r'Pasul 3: un model de limbaj (T5) antrenat cu \textbf{entropia încrucișată} prezice token-ul următor'),
     [T('the forecast is a categorical distribution over bins, sampled autoregressively (one token at a time)', 'prognoza este o distribuție categorială pe intervale, eșantionată autoregresiv (cîte un token o dată)'),
      T('no notion of distance between tokens: neighbouring bins are as different as distant ones, unless the data teach otherwise', 'nu există o noțiune de distanță între token-uri: intervalele vecine sînt la fel de diferite ca cele îndepărtate, dacă datele nu arată altceva')])), 'small')

D.frame(T('Tokenisation: from real values to a vocabulary (2/2)', 'Tokenizarea: de la valori reale la un vocabular (2/2)'), items(
    (T(r'\textbf{Resolution}: neighbouring bin centres are $30/4092$ apart on the scaled axis, i.e.\ $30s/4092$ in the units of the series',
       r'\textbf{Rezoluția}: centrele a două intervale vecine sînt la distanța $30/4092$ pe axa scalată, adică $30s/4092$ în unitățile seriei'),
     [T(r'$30 = 15 - (-15)$ is the length of the covered range; the quantisation error is at most half of this spacing', r'$30 = 15 - (-15)$ este lungimea domeniului acoperit; eroarea de cuantizare este cel mult jumătate din această distanță')]),
    (T(r'\textbf{Hard range}: a value above $15s$ (or below $-15s$) has no token and cannot be predicted', r'\textbf{Domeniu limitat}: o valoare peste $15s$ (sau sub $-15s$) nu are token și nu poate fi prognozată'), []),
    (T(r'\textbf{Scale invariance}: multiplying the series by $c > 0$ multiplies $s$ by $c$ and leaves the tokens unchanged',
       r'\textbf{Invarianța la scală}: înmulțirea seriei cu $c > 0$ înmulțește $s$ cu $c$ și lasă token-urile neschimbate'), []),
    (T('Other input representations', 'Alte reprezentări ale intrării'),
     [T(r'LLMTime \refGru: the digits of each value as text tokens', r'LLMTime \refGru: cifrele fiecărei valori, ca token-uri de text'),
      T(r'Lag-Llama \refRas: lagged values as features', r'Lag-Llama \refRas: valorile cu lag ca variabile'),
      T('patch models: no vocabulary at all (next slides)', 'modelele cu patch-uri: fără vocabular (slide-urile următoare)')])), 'small')

chart(T('The Chronos tokeniser on real data', 'Tokenizatorul Chronos pe date reale'), 'ats_ch13_tokens', 'ATS_ch13_pretraining', [
    T(r'Left: BET closes, @{tok.first} -- @{tok.last} ($C = @{tok.n}$), and a 64-bin quantisation (illustration); right: a context near 1 followed by a rise to 25 times that level',
      r'Stînga: închiderile BET, @{tok.first} -- @{tok.last} ($C = @{tok.n}$), și o cuantizare cu 64 de intervale (ilustrare); dreapta: un context în jurul valorii 1, urmat de o creștere pînă la un nivel de 25 de ori mai mare')],
    h='0.5\\textheight')

interp(('the tokeniser', 'tokenizatorului'), [
    T(r'BET: $s = @{tok.s}$ points, bin width @{tok.w} points, maximum quantisation error @{tok.err} points: negligible for prices, but a fixed share of the level',
      r'BET: $s = @{tok.s}$ puncte, lățimea intervalului @{tok.w} puncte, eroarea maximă de cuantizare @{tok.err} puncte: neglijabilă pentru prețuri, dar o pondere fixă din nivel'),
    T(r'Right panel: the scale is set by the context, so the path that rises beyond $15s$ is clipped: @{tok.clip}\% of the future steps are unreachable, the last one by @{tok.jerr}\%',
      r'Panoul din dreapta: scala este fixată de context, deci traiectoria care urcă peste $15s$ este trunchiată: @{tok.clip}\% dintre pașii viitori nu pot fi atinși, ultimul are o eroare de @{tok.jerr}\%'),
    T('Explosive series (bubbles, Chapter 16; hyperinflation) are outside the support of a mean-scaled vocabulary; Chronos-2 replaces it by an arcsinh transform and quantile outputs',
      'Seriile explozive (bule, Capitolul 16; hiperinflație) sînt în afara suportului unui vocabular scalat prin medie; Chronos-2 îl înlocuiește cu o transformare arcsinh și ieșiri sub formă de cuantile')])

D.frame(T('Patching and the output head', 'Patching și stratul de ieșire'), items(
    (T(r'\textbf{Patching} \refNie: the context is split into patches of $P$ consecutive values and each patch becomes one input token',
       r'\textbf{Patching} \refNie: contextul se împarte în patch-uri de $P$ valori consecutive, iar fiecare patch devine un token de intrare'),
     [T(r'$P$: the patch length; a context of $C$ values gives $C/P$ tokens', r'$P$: lungimea unui patch; un context de $C$ valori dă $C/P$ token-uri'),
      T(r'attention compares every pair of tokens, so its cost grows as $O((C/P)^2)$ instead of $O(C^2)$; $O(\cdot)$: order of magnitude', r'atenția compară fiecare pereche de token-uri, deci costul ei crește ca $O((C/P)^2)$ în loc de $O(C^2)$; $O(\cdot)$: ordinul de mărime'),
      T(r'TimesFM \refDas: input patches of 32, output patches of 128 (fewer autoregressive steps); Chronos-Bolt and Chronos-2: patches of 16; Moirai \refWoo: several sizes by frequency',
        r'TimesFM \refDas: patch-uri de intrare de 32, de ieșire de 128 (mai puțini pași autoregresivi); Chronos-Bolt și Chronos-2: patch-uri de 16; Moirai \refWoo: mai multe mărimi, după frecvență')]),
    (T('Output heads', 'Straturi de ieșire'),
     [T(r'categorical over bins (Chronos)', r'distribuție categorială pe intervale (Chronos)'),
      T(r'\textbf{quantile head} trained by the pinball loss (Chronos-Bolt: 10\%--90\%; Chronos-2: 1\%--99\%; TimesFM 2.5, TiRex: deciles)',
        r'\textbf{strat de cuantile} antrenat cu pierderea pinball (Chronos-Bolt: 10\%--90\%; Chronos-2: 1\%--99\%; TimesFM 2.5, TiRex: decile)'),
      T(r'parametric: Student-$t$ (Lag-Llama \refRas), a mixture of distributions (Moirai)', r'parametric: Student-$t$ (Lag-Llama \refRas), un amestec de distribuții (Moirai)')]),
    (T(r'\textbf{Direct multi-step quantiles}: one pass gives the quantiles of all $H$ steps',
       r'\textbf{Cuantile directe pe mai mulți pași}: o singură trecere dă cuantilele pentru toți cei $H$ pași'),
     [T('no accumulation of errors from step to step', 'erorile nu se acumulează de la un pas la altul'),
      T('but the output is the marginal distribution of each step, not their joint distribution: a path functional (a maximum, a sum over the horizon) cannot be read from it',
        'dar ieșirea este distribuția marginală a fiecărui pas, nu distribuția lor comună: o funcțională de traiectorie (un maxim, o sumă pe orizont) nu se poate citi din ea')])), 'small')

D.frame(T('Scaling laws', 'Legi de scalare'), items(
    (T(r'Language models \refKap, \refHof: the test loss falls as a power law of the model size, and similarly of the data size and of the compute, over several orders of magnitude',
       r'Modelele de limbaj \refKap, \refHof: pierderea pe datele de test scade ca o lege de putere în mărimea modelului și, la fel, în volumul datelor și în calcul, pe mai multe ordine de mărime'),
     [r'\[ L(N) \approx (N_c/N)^{\alpha_N} \]',
      T(r'$L(N)$: test loss of a model with $N$ parameters; $N_c$: a fitted scale constant; $\alpha_N > 0$: the fitted exponent', r'$L(N)$: pierderea pe datele de test a unui model cu $N$ parametri; $N_c$: o constantă de scală estimată; $\alpha_N > 0$: exponentul estimat'),
      T(r'reading: doubling $N$ multiplies the loss by $2^{-\alpha_N}$; on a log--log plot the relation is a straight line of slope $-\alpha_N$', r'interpretare: dublarea lui $N$ înmulțește pierderea cu $2^{-\alpha_N}$; pe un grafic log--log relația este o dreaptă cu panta $-\alpha_N$')]),
    (T(r'Time series: decoder-only Transformers show the same power laws in parameters, data and compute \refEdw; the look-back length interacts with data size \refShi',
       r'Serii de timp: Transformers de tip decoder-only arată aceleași legi de putere în parametri, date și calcul \refEdw; lungimea contextului interacționează cu volumul datelor \refShi'),
     [T(r'out-of-distribution: the log-likelihood scales similarly in and out of distribution, but architecture matters; tweaks that help in distribution can reduce OOD scalability \refYao',
        r'în afara distribuției: log-verosimilitatea se scalează asemănător în și în afara distribuției, dar arhitectura contează; ajustările care ajută în distribuție pot reduce scalabilitatea OOD \refYao')]),
    (T('A scaling law concerns the average loss on the corpus distribution', 'O lege de scalare privește pierderea medie pe distribuția corpusului'),
     [T('it says nothing about one particular Romanian series', 'ea nu spune nimic despre o serie românească anume'),
      T('small models (TiRex, 35 million parameters) beat larger ones on public leaderboards \\refAue', 'modele mici (TiRex, 35 de milioane de parametri) le întrec pe cele mari în clasamentele publice \\refAue')])), 'small')

chart(T('Size and accuracy on our three tasks', 'Mărimea și acuratețea pe cele trei sarcini ale noastre'), 'ats_ch13_scaling', 'ATS_ch13_pretraining', [
    T(r'Losses relative to the baseline of each task: Romanian load (MAE / expert ARX, 2025--2026), EU inflation (MAE / random walk, $h = 12$, geometric mean over 27 countries), Bitcoin log RV (MSE / HAR)',
      r'Pierderi relative la modelul de referință al fiecărei sarcini: consumul României (MAE / ARX expert, 2025--2026), inflația UE (MAE / mers aleator, $h = 12$, medie geometrică pe 27 de țări), log RV Bitcoin (MSE / HAR)'),
    T('Parameters counted in the loaded checkpoints; a value below 1 means the model beats the baseline', 'Parametrii sînt numărați în modelele încărcate; o valoare sub 1 înseamnă că modelul întrece modelul de referință')],
    h='0.5\\textheight')

interp(('size against accuracy', 'relației dintre mărime și acuratețe'), [
    T(r'Chronos-Bolt family (@{sc.ptiny}--@{sc.pbase} M parameters): load @{sc.l.tiny} $\to$ @{sc.l.base}, inflation @{sc.i.tiny} $\to$ @{sc.i.base}, Bitcoin @{sc.r.tiny} $\to$ @{sc.r.base}',
      r'Familia Chronos-Bolt (@{sc.ptiny}--@{sc.pbase} M parametri): consum @{sc.l.tiny} $\to$ @{sc.l.base}, inflație @{sc.i.tiny} $\to$ @{sc.i.base}, Bitcoin @{sc.r.tiny} $\to$ @{sc.r.base}'),
    T(r'Across families size is not the ranking: Chronos-2 (@{sc.pc2} M) @{sc.l.c2} on load; TiRex (@{sc.ptx} M) @{sc.l.tx}; TimesFM 2.5 (@{sc.ptf} M) @{sc.l.tf}',
      r'Între familii, mărimea nu determină clasamentul: Chronos-2 (@{sc.pc2} M) @{sc.l.c2} la consum; TiRex (@{sc.ptx} M) @{sc.l.tx}; TimesFM 2.5 (@{sc.ptf} M) @{sc.l.tf}'),
    (T('Within the Chronos-Bolt family the loss falls with size on all three tasks (one exception: mini on inflation)', 'În familia Chronos-Bolt pierderea scade odată cu mărimea pe toate cele trei sarcini (o excepție: mini la inflație)'),
     [T('across families, architecture, corpus and training procedure change together', 'între familii, arhitectura, corpusul și procedura de antrenare se schimbă simultan'),
      T('so three tasks are not a scaling study', 'deci trei sarcini nu constituie un studiu de scalare')])])

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
     r'Lag-Llama \refRas & ' + T('decoder-only on lag features', 'decoder-only pe valori cu lag') + ' & ' + T('small', 'mic') + ' & Student-$t$',
     r'MOMENT \refGos & ' + T('masked T5 encoder, multi-task', 'encoder T5 mascat, multi-sarcină') + ' & 40--385 M & ' + T('reconstruction; heads per task', 'reconstrucție; straturi pe sarcină'),
     r'TiRex \refAue & xLSTM & @{sc.ptx} M & ' + T('deciles', 'decile')],
    size='scriptsize') + items(
    T(r'Toto \refCoh (151 M, observability data) and Moirai 2.0 \refLiu are open as well; TimeGPT \refGar is reached only through a paid API', r'Toto \refCoh (151 M, date de observabilitate) și Moirai 2.0 \refLiu sînt și ele deschise; TimeGPT \refGar este accesibil doar printr-un API cu plată')), 'footnotesize')

D.frame(T('The Chronos family', 'Familia Chronos'), items(
    (T(r'\textbf{Chronos} \refAns', r'\textbf{Chronos} \refAns'),
     [T('the training procedure of language models, unchanged; forecasts by sampling token paths', 'procedura de antrenare a modelelor de limbaj, nemodificată; prognoze prin eșantionarea traiectoriilor de token-uri'),
      T('zero-shot results comparable to models trained on the target data (their Benchmark II)', 'rezultate zero-shot comparabile cu cele ale modelelor antrenate pe datele-țintă (Benchmark II din lucrare)')]),
    (T(r'\textbf{Chronos-Bolt}', r'\textbf{Chronos-Bolt}'),
     [T('patch inputs and a direct quantile decoder: much faster than Chronos', 'intrări sub formă de patch-uri și un decodor direct de cuantile: mult mai rapid decît Chronos'),
      T('context up to 2048, 64 steps; quantiles only between 10\\% and 90\\%', 'context de pînă la 2048, 64 de pași; cuantile doar între 10\\% și 90\\%'),
      T('a 95\\% interval or a VaR 1\\% cannot be read from its output: the request is clipped to the nearest trained level', 'un interval de 95\\% sau un VaR 1\\% nu se pot citi din ieșirea lui: cererea este trunchiată la cel mai apropiat nivel antrenat')]),
    (T(r'\textbf{Chronos-2} \refAnsB', r'\textbf{Chronos-2} \refAnsB'),
     [T('group attention shares information across the series of a group (variates, related series, covariates)', 'atenția de grup împarte informația între seriile unui grup (variabile, serii înrudite, covariabile)'),
      T(r'\textbf{in-context learning} of covariate effects, without re-estimation', r'\textbf{învățare în context} a efectelor covariabilelor, fără reestimare'),
      T('trained largely on synthetic multivariate structures imposed on univariate series', 'antrenat în mare parte pe structuri multivariate sintetice impuse unor serii univariate'),
      T('context 8192; 21 quantiles from 1\\% to 99\\%; arcsinh scaling', 'context de 8192; 21 de cuantile de la 1\\% la 99\\%; scalare arcsinh')])), 'small')

D.frame(T('TimesFM, Moirai, Lag-Llama, MOMENT (1/2)', 'TimesFM, Moirai, Lag-Llama, MOMENT (1/2)'), items(
    (T(r'\textbf{TimesFM} \refDas', r'\textbf{TimesFM} \refDas'),
     [T('decoder-only, with patches; the output patch is longer than the input patch', 'decoder-only, cu patch-uri; patch-ul de ieșire este mai lung decît cel de intrare'),
      T('trained on many granularities; version 2.5 adds a quantile head and long contexts', 'antrenat pe multe frecvențe; versiunea 2.5 adaugă un strat de cuantile și contexte lungi')]),
    (T(r'\textbf{Moirai} \refWoo', r'\textbf{Moirai} \refWoo'),
     [T('masked encoder; frequency-specific patch sizes', 'encoder mascat; mărimi de patch specifice frecvenței'),
      T('any-variate attention flattens multivariate inputs into one sequence', 'atenția pe orice număr de variabile aplatizează intrările multivariate într-o singură secvență'),
      T(r'mixture output: Student-$t$, log-normal, negative binomial', r'ieșire sub formă de amestec: Student-$t$, log-normală, binomială negativă'),
      T(r'Moirai 2.0 \refLiu: a decoder-only simplification, smaller and better on GIFT-Eval', r'Moirai 2.0 \refLiu: o simplificare decoder-only, mai mică și mai bună pe GIFT-Eval')])), 'small')

D.frame(T('TimesFM, Moirai, Lag-Llama, MOMENT (2/2)', 'TimesFM, Moirai, Lag-Llama, MOMENT (2/2)'), items(
    (T(r'\textbf{Lag-Llama} \refRas', r'\textbf{Lag-Llama} \refRas'),
     [T('a LLaMA-type decoder whose tokens are vectors of lagged values at many seasonal lags', 'un decodor de tip LLaMA ale cărui token-uri sînt vectori de valori cu lag, la multe laguri sezoniere'),
      T(r'Student-$t$ output head; strong after fine-tuning', r'strat de ieșire Student-$t$; puternic după fine-tuning')]),
    (T(r'\textbf{MOMENT} \refGos', r'\textbf{MOMENT} \refGos'),
     [T('pretrained by masked reconstruction on the Time series Pile', 'preantrenat prin reconstrucție mascată pe Time series Pile'),
      T('one encoder for forecasting, classification, anomaly detection and imputation', 'un singur encoder pentru prognoză, clasificare, detectarea anomaliilor și imputare')]),
    ), 'small')

D.frame(T('Recurrent again, observability, and a closed API', 'Din nou recurente, observabilitate și un API închis'), items(
    (T(r'\textbf{TiRex} \refAue', r'\textbf{TiRex} \refAue'),
     [T('an xLSTM keeps a state across the context, which allows state tracking over long horizons', 'un xLSTM păstrează o stare de-a lungul contextului, ceea ce permite urmărirea stării pe orizonturi lungi'),
      T('xLSTM: the recurrent cells of Chapter 12 with exponential gating and a matrix memory', 'xLSTM: celulele recurente din Capitolul 12, cu porți exponențiale și memorie matriceală'),
      T('contiguous patch masking (CPM) in training: the model learns to forecast several steps without feedback',
        'mascarea patch-urilor contigue (CPM) la antrenare: modelul învață să prognozeze mai mulți pași fără reacție')]),
    (T(r'\textbf{Toto} \refCoh', r'\textbf{Toto} \refCoh'),
     [T('decoder-only, for multivariate observability metrics; the BOOM benchmark (2807 series)', 'decoder-only, pentru metrici multivariate de observabilitate; benchmark-ul BOOM (2807 serii)'),
      T('the domain composition of the corpus drives the results', 'alcătuirea pe domenii a corpusului determină rezultatele')]),
    (T(r'\textbf{TimeGPT} \refGar', r'\textbf{TimeGPT} \refGar'),
     [T('closed weights and an undisclosed corpus, behind a paid API', 'ponderi închise și un corpus nedezvăluit, în spatele unui API cu plată'),
      T('contamination cannot be audited; results are not reproducible if the service changes the model', 'contaminarea nu poate fi verificată; rezultatele nu sînt reproductibile dacă serviciul schimbă modelul'),
      T('the data leave your institution', 'datele ies din instituția dumneavoastră')])), 'small')

D.frame(T('Zero-shot, fine-tuning, in-context covariates', 'Zero-shot, fine-tuning, covariabile în context'), items(
    (T(r'\textbf{Zero-shot}: the forecast is $f_{\hat\theta}(y_{T-C+1:T})$', r'\textbf{Zero-shot}: prognoza este $f_{\hat\theta}(y_{T-C+1:T})$'),
     [T('no training, hence no risk of overfitting the target; the only choices are $C$ and the model', 'fără antrenare, deci fără risc de supraajustare pe seria-țintă; singurele alegeri sînt $C$ și modelul')]),
    (T(r'\textbf{Fine-tuning}: the weights start at $\hat\theta$ and take a few gradient steps on the target data', r'\textbf{Fine-tuning}: ponderile pornesc de la $\hat\theta$ și fac cîțiva pași de gradient pe datele-țintă'),
     [T('all weights, or low-rank adapters (LoRA) added to frozen weights', 'toate ponderile sau adaptoare de rang mic (LoRA) adăugate ponderilor înghețate'),
      T('needs a validation split respecting time (Chapter 12); can forget the prior; with short economic series it rarely pays', 'cere o împărțire de validare care respectă timpul (Capitolul 12); poate uita distribuția a priori; pe serii economice scurte rareori merită')]),
    (T(r'\textbf{In-context covariates} (Chronos-2)', r'\textbf{Covariabile în context} (Chronos-2)'),
     [T(r'past values of a covariate $x_t$ (e.g.\ temperature) and future values of regressors known in advance enter the context', r'valorile trecute ale unei covariabile $x_t$ (de exemplu temperatura) și valorile viitoare ale regresorilor cunoscuți dinainte intră în context'),
      T('the model infers their effect inside the forward pass, with no parameter estimated', 'modelul deduce efectul lor în timpul trecerii înainte, fără niciun parametru estimat'),
      T('cross-learning: forecasting a batch of related series jointly (all 27 EU countries at one origin)', 'învățarea încrucișată: prognoza în comun a unui lot de serii înrudite (toate cele 27 de țări UE la aceeași origine)')]),
    (T('Known future covariates must really be known at the origin', 'Covariabilele viitoare cunoscute trebuie să fie chiar cunoscute la origine'),
     [T('weather forecasts, not realised weather, unless an upper bound is the goal', 'prognoze meteo, nu vremea realizată, cu excepția cazului în care se urmărește o limită superioară')])), 'small')

chart(T('Four zero-shot forecasts from one model', 'Patru prognoze zero-shot cu același model'), 'ats_ch13_zeroshot', 'ATS_ch13_zero_shot', [
    T(r'Chronos-2 from the last origin of each data set: Romanian load (48 hours), Romanian HICP inflation (12 months), Bitcoin log realised variance and BET daily returns (22 days); bands 10--90\% and 1--99\%',
      r'Chronos-2 de la ultima origine a fiecărui set de date: consumul României (48 de ore), inflația HICP a României (12 luni), logaritmul varianței realizate Bitcoin și randamentele zilnice BET (22 de zile); benzi 10--90\% și 1--99\%')],
    h='0.55\\textheight')

interp(('the four forecasts', 'celor patru prognoze'), [
    T('Load: the daily and weekly shapes are continued with narrow bands: the most favourable case for shape transfer', 'Consumul: profilurile zilnice și săptămînale sînt continuate cu benzi înguste: cazul cel mai favorabil pentru transferul de formă'),
    T('Inflation: a smooth path towards the recent level with bands that widen with the horizon: close to what an AR model with persistence would give', 'Inflația: o traiectorie netedă spre nivelul recent, cu benzi care se lărgesc cu orizontul: aproape de ce ar da un model AR persistent'),
    T('Log RV of Bitcoin: a weekly pattern (lower variance at weekends) around a level set by the context', 'Log RV pentru Bitcoin: un tipar săptămînal (varianță mai mică la sfîrșit de săptămînă) în jurul unui nivel stabilit de context'),
    T('Returns: a flat median and a symmetric band, i.e.\\ an unconditional distribution', 'Randamentele: o mediană constantă și o bandă simetrică, adică o distribuție necondiționată'),
    T(r'Return bands from the 1\% and 99\% quantiles: Chronos-2 VaR 1\% for the next day is @{zs.var} (\% of value); Section 8 checks whether such numbers are calibrated',
      r'Benzile randamentelor din cuantilele de 1\% și 99\%: VaR 1\% Chronos-2 pentru ziua următoare este @{zs.var} (\% din valoare); secțiunea 8 verifică dacă astfel de cifre sînt calibrate')])

D.recap(('model families', 'familiile de modele'), [
    T('Families differ in input (tokens, patches, lags), architecture (encoder, decoder, recurrent) and output (categorical, quantiles, parametric)', 'Familiile diferă prin intrare (token-uri, patch-uri, laguri), arhitectură (encoder, decoder, recurentă) și ieșire (categorială, cuantile, parametrică)'),
    T('Quantile range is a design constraint: deciles only, except Chronos-2', 'Domeniul cuantilelor este o constrîngere de proiectare: doar decile, cu excepția Chronos-2'),
    T('Zero-shot is the default; covariates in context and cross-learning are the new levers; closed APIs cannot be audited', 'Zero-shot este varianta implicită; covariabilele în context și învățarea încrucișată sînt noile pîrghii; API-urile închise nu pot fi verificate')])

# =============================================================================
# 3. BENCHMARK-URI ȘI TESTARE
# =============================================================================
D.section('Benchmarks, contamination and testing', 'Benchmark-uri, contaminare și testare')

D.frame(T('Benchmarks for pretrained models', 'Benchmark-uri pentru modelele preantrenate'), items(
    (T(r'\textbf{GIFT-Eval} \refAks: 23 data sets, over 144\,000 series, 177 million points, seven domains, ten frequencies, short to long horizons; a non-leaking pretraining set',
       r'\textbf{GIFT-Eval} \refAks: 23 de seturi de date, peste 144\,000 de serii, 177 de milioane de puncte, șapte domenii, zece frecvențe, orizonturi scurte și lungi; un set de preantrenare fără leakage'), []),
    (T(r'\textbf{fev-bench} \refShc: 100 tasks in seven domains, 46 with covariates; win rates and skill scores with bootstrap confidence intervals',
       r'\textbf{fev-bench} \refShc: 100 de sarcini în șapte domenii, 46 cu covariabile; rate de cîștig și scoruri de abilitate cu intervale de încredere bootstrap'), []),
    (T(r'\textbf{Live benchmarks}: forecasts registered before the outcomes exist, e.g.\ TS-Arena \refMey and Impermanent \refGarB: the only design immune to contamination by construction',
       r'\textbf{Benchmark-uri live}: prognoze înregistrate înainte să existe rezultatele, de exemplu TS-Arena \refMey și Impermanent \refGarB: singurul design imun la contaminare prin construcție'), []),
    T(r'Classical references for what a fair comparison needs: M5 \refMak; pitfalls catalogued by \refHAB',
      r'Repere clasice pentru ce cere o comparație corectă: M5 \refMak; capcanele catalogate de \refHAB')), 'small')

D.frame(T('Aggregating scores across series (1/2)', 'Agregarea scorurilor pe mai multe serii (1/2)'), items(
    (T(r'\textbf{MASE} \refHK: the mean absolute forecast error divided by the in-sample mean absolute error of the seasonal naive forecast',
       r'\textbf{MASE} \refHK: eroarea absolută medie a prognozei împărțită la eroarea absolută medie, în eșantion, a prognozei naive sezoniere'),
     [r'\[ \mathrm{MASE} = \frac{\frac{1}{H}\sum_{h=1}^{H}|y_{T+h} - \hat y_{T+h}|}{\frac{1}{T-m}\sum_{t=m+1}^{T}|y_t - y_{t-m}|} \]',
      T(r'$\hat y_{T+h}$: the forecast $h$ steps after the origin $T$; $m$: the seasonal period (1 without seasonality)', r'$\hat y_{T+h}$: prognoza la $h$ pași după originea $T$; $m$: perioada sezonieră (1 fără sezonalitate)'),
      T(r'MASE $< 1$: better than the naive forecast in sample; free of the units of $y$', r'MASE $< 1$: mai bun decît prognoza naivă în eșantion; nu depinde de unitățile lui $y$')]),
    (T(r'\textbf{WQL} (weighted quantile loss): the pinball losses of the forecast quantiles, summed and divided by the total absolute level of the series',
       r'\textbf{WQL} (pierderea cuantilică ponderată): pierderile pinball ale cuantilelor prognozate, însumate și împărțite la nivelul absolut total al seriei'),
     [r'\[ \mathrm{WQL} = \frac{2\sum_{t}\sum_{\tau}\rho_\tau(y_t - \hat q_{\tau,t})}{\sum_t|y_t|}, \qquad \rho_\tau(u) = u\big(\tau - \mathbf 1\{u < 0\}\big) \]',
      T(r'$\hat q_{\tau,t}$: the forecast quantile of level $\tau \in (0, 1)$ for period $t$; $\mathbf 1\{\cdot\}$: 1 if the condition holds, 0 otherwise', r'$\hat q_{\tau,t}$: cuantila prognozată de nivel $\tau \in (0, 1)$ pentru perioada $t$; $\mathbf 1\{\cdot\}$: 1 dacă condiția este îndeplinită, 0 altfel'),
      T(r'$\rho_\tau$: the pinball loss; its average over $\tau$ approximates the CRPS (Chapter 1); WQL $= 0$ only for perfect quantiles', r'$\rho_\tau$: pierderea pinball; media ei pe $\tau$ aproximează CRPS (Capitolul 1); WQL $= 0$ doar pentru cuantile perfecte')])), 'small')

D.frame(T('Aggregating scores across series (2/2)', 'Agregarea scorurilor pe mai multe serii (2/2)'), items(
    (T(r'\textbf{Relative score} of series $s$: the loss of the model divided by the loss of a baseline on the same series',
       r'\textbf{Scorul relativ} al seriei $s$: pierderea modelului împărțită la pierderea unui model de referință pe aceeași serie'),
     [r'\[ r_s = \frac{L_s(\text{model})}{L_s(\text{baseline})}, \qquad \bar r_{\mathrm{geo}} = \Big(\prod_{s=1}^{S} r_s\Big)^{1/S} \]',
      T(r'$L_s$: a loss (MAE, MASE, WQL) on series $s$; $S$: the number of series; $r_s < 1$: the model beats the baseline on series $s$', r'$L_s$: o pierdere (MAE, MASE, WQL) pe seria $s$; $S$: numărul de serii; $r_s < 1$: modelul întrece modelul de referință pe seria $s$')]),
    (T(r'\textbf{Geometric mean} $\bar r_{\mathrm{geo}}$ \refFW: the rankings do not depend on the choice of baseline, and a gain and a loss of the same ratio cancel',
       r'\textbf{Media geometrică} $\bar r_{\mathrm{geo}}$ \refFW: clasamentele nu depind de alegerea modelului de referință, iar un cîștig și o pierdere de același raport se compensează'),
     [T(r'\textbf{skill score} $1 - \bar r_{\mathrm{geo}}$: the average proportional gain over the baseline (0: no gain)', r'\textbf{scorul de abilitate} (skill score) $1 - \bar r_{\mathrm{geo}}$: cîștigul proporțional mediu față de modelul de referință (0: niciun cîștig)'),
      T(r'\textbf{win rate}: the share of series on which a model beats another', r'\textbf{rata de cîștig} (win rate): ponderea seriilor pe care un model îl întrece pe altul')]),
    (T('Two aggregations to avoid', 'Două agregări de evitat'),
     [T('the arithmetic mean of ratios: dominated by the series on which the baseline is weak', 'media aritmetică a rapoartelor: dominată de seriile pe care modelul de referință este slab'),
      T('the mean of raw errors: dominated by the series with the largest scale', 'media erorilor brute: dominată de seria cu scala cea mai mare')])), 'small')

D.frame(T('Leakage and contamination', 'Leakage și contaminare'), items(
    (T(r'\textbf{Series leakage}', r'\textbf{Leakage-ul seriilor}'),
     [T('an evaluation series (or a near copy) is in the pretraining corpus', 'o serie de evaluare (sau o copie apropiată) se află în corpusul de preantrenare'),
      T(r'Chronos separates in-domain (Benchmark I) from zero-shot (Benchmark II) results for this reason \refAns', r'Chronos separă din acest motiv rezultatele în domeniu (Benchmark I) de cele zero-shot (Benchmark II) \refAns')]),
    (T(r'\textbf{Temporal contamination}', r'\textbf{Contaminarea temporală}'),
     [T('the test window precedes the training cutoff: the model may have seen the outcomes of other, correlated series in the same period', 'fereastra de test precede data-limită a antrenării: modelul poate să fi văzut rezultatele altor serii, corelate, din aceeași perioadă'),
      T(r'LLMs recall exact economic values from before their cutoff \refLTZ', r'LLM-urile reproduc valori economice exacte din perioada dinaintea datei-limită \refLTZ'),
      T(r'a two-data-set design against contamination, for electricity prices \refPE', r'un design cu două seturi de date împotriva contaminării, pentru prețurile electricității \refPE')]),
    (T('Designs that help', 'Designuri care ajută'),
     [T('evaluate only after the release (or the declared cutoff) of every model in the comparison; we use 1 November 2025, after the last of our models (Chronos-2, 30 October 2025)',
        'evaluați doar după lansarea (sau data-limită declarată) a fiecărui model din comparație; folosim 1 noiembrie 2025, după ultimul dintre modelele noastre (Chronos-2, 30 octombrie 2025)'),
      T('compare the relative skill before and after: a large drop after the release is a warning sign', 'comparați abilitatea relativă înainte și după: o scădere mare după lansare este un semnal de alarmă'),
      T('pre-register origins, horizons, metrics and baselines before looking at the results', 'preînregistrați originile, orizonturile, metricile și modelele de referință înainte de a vedea rezultatele')])), 'small')

D.frame(T('Testing across many series (1/2)', 'Testarea pe multe serii (1/2)'), items(
    (T('One series (all in Chapter 1)', 'O serie (toate în Capitolul 1)'),
     [T(r'DM with HLN correction \refDM, \refHLN; conditional ability \refGW', r'DM cu corecția HLN \refDM, \refHLN; capacitatea condiționată \refGW'),
      T(r'many models: MCS \refHLNa', r'multe modele: MCS \refHLNa')]),
    (T(r'$S$ series tested separately, each at level 5\%: under the null hypothesis about $0.05S$ false rejections are expected',
       r'$S$ serii testate separat, fiecare la nivelul de 5\%: sub ipoteza nulă se așteaptă aproximativ $0{,}05S$ respingeri false'),
     [T(r'with $S = 27$ countries, about one or two ``significant'' countries by chance alone', r'cu $S = 27$ de țări, aproximativ una sau două țări „semnificative” doar din întîmplare')]),
    (T('Two error rates for a family of tests', 'Două rate de eroare pentru o familie de teste'),
     [T(r'\textbf{FWER} (family-wise error rate): the probability of at least one false rejection', r'\textbf{FWER} (family-wise error rate): probabilitatea a cel puțin unei respingeri false'),
      T(r'\textbf{FDR} (false discovery rate): the expected share of false rejections among all rejections', r'\textbf{FDR} (false discovery rate): proporția așteptată a respingerilor false printre toate respingerile')]),
    (T(r'Notation: $p_{(1)} \le \dots \le p_{(S)}$ are the $S$ p-values sorted increasingly; $\alpha$: the target level of the family (e.g.\ 5\%)',
       r'Notațiile: $p_{(1)} \le \dots \le p_{(S)}$ sînt cele $S$ p-value-uri ordonate crescător; $\alpha$: nivelul-țintă al familiei (de exemplu 5\%)'), [])), 'small')

D.frame(T('Testing across many series (2/2)', 'Testarea pe multe serii (2/2)'), items(
    (T(r'\textbf{Holm} \refHol, controls the FWER: go up the sorted list and reject while', r'\textbf{Holm} \refHol, controlează FWER: se parcurge lista ordonată și se respinge cît timp'),
     [r'\[ p_{(k)} \le \frac{\alpha}{S - k + 1}, \qquad k = 1, 2, \dots \]',
      T(r'the smallest p-value faces the Bonferroni threshold $\alpha/S$, the next ones gradually looser thresholds; stop at the first failure', r'cel mai mic p-value este comparat cu pragul Bonferroni $\alpha/S$, următoarele cu praguri treptat mai permisive; se oprește la primul eșec')]),
    (T(r'\textbf{Benjamini--Hochberg} \refBH, controls the FDR: reject the $k^*$ smallest p-values, with', r'\textbf{Benjamini--Hochberg} \refBH, controlează FDR: se resping cele mai mici $k^*$ p-value-uri, unde'),
     [r'\[ k^* = \max\{k: p_{(k)} \le k\alpha/S\} \]',
      T('more rejections than Holm; valid under independence or positive dependence between the tests', 'mai multe respingeri decît Holm; valid sub independență sau dependență pozitivă între teste')]),
    (T(r'\textbf{Pooled test}: average the loss differential across series at each origin, then run one DM test with HAC variance',
       r'\textbf{Test agregat}: se mediază diferența de pierdere pe serii la fiecare origine, apoi se aplică un singur test DM cu varianță HAC'),
     [T('the correlation between series stays in the averaged time series, so the HAC variance accounts for it', 'corelația dintre serii rămîne în seria de timp mediată, deci varianța HAC o ia în calcul')]),
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
    (T('Both methods extrapolate persistence; turning points come from information outside the series', 'Ambele metode extrapolează persistența; punctele de întoarcere vin din informații din afara seriei'),
     [T('energy prices, the end of the price caps, the VAT increase of August 2025 (its effect on annual inflation lasts exactly 12 months)', 'prețurile energiei, sfîrșitul plafonării prețurilor, majorarea TVA din august 2025 (efectul ei asupra inflației anuale durează exact 12 luni)'),
      T('these are known in advance, hence natural covariates', 'acestea sînt cunoscute dinainte, deci sînt covariabile naturale')])])

chart(T('Twenty-seven tests at once', 'Douăzeci și șapte de teste deodată'), 'ats_ch13_multiple', 'ATS_ch13_benchmark', [
    T(r'Country-level DM--HLN statistics (HAC with $h - 1$ lags) of the absolute errors of @{mt.model} minus AR($p$) at $h = @{mt.h}$; negative: @{mt.model} better',
      r'Statisticile DM--HLN pe țări (HAC cu $h - 1$ laguri) ale erorilor absolute @{mt.model} minus AR($p$) la $h = @{mt.h}$; negativ: @{mt.model} este mai bun')],
    h='0.48\\textheight')

interp(('the multiple tests', 'testelor multiple'), [
    T(r'@{mt.neg} of 27 statistics are negative; @{mt.rej} are significant at 5\% without correction (@{mt.rejfm} in favour of @{mt.model}, @{mt.rejar} in favour of AR)',
      r'@{mt.neg} din 27 de statistici sînt negative; @{mt.rej} sînt semnificative la 5\% fără corecție (@{mt.rejfm} în favoarea @{mt.model}, @{mt.rejar} în favoarea AR)'),
    T(r'With Holm: @{mt.holm} rejections; with Benjamini--Hochberg: @{mt.bh}; Romania: $t = @{mt.rot}$, $p$ @{mt.rop}',
      r'Cu Holm: @{mt.holm} respingeri; cu Benjamini--Hochberg: @{mt.bh}; România: $t = @{mt.rot}$, $p$ @{mt.rop}'),
    (T(r'Pooled over the 27 countries (average loss differential at each origin, HAC variance): $t = @{ai.t}$, $p$ @{ai.p}', r'Agregat pe cele 27 de țări (diferența medie de pierdere la fiecare origine, varianță HAC): $t = @{ai.t}$, $p$ @{ai.p}'),
     [T('the bootstrap intervals of the previous chart treat countries as independent and look sharper than they are', 'intervalele bootstrap din graficul anterior tratează țările ca independente și par mai precise decît sînt')]),
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
    (T(r'Three of the four zero-shot models beat HAR on both assets, and HAR is outside both MCS', r'Trei dintre cele patru modele zero-shot întrec HAR pe ambele active, iar HAR nu intră în niciun MCS'),
     [T(r'the slowly decaying memory of log RV (Chapter 10) is a shape a model can learn from a corpus', r'memoria lentă a lui log RV (Capitolul 10) este o structură pe care modelul o poate învăța din corpus'),
      T(r'the gain is large for Bitcoin, small for the S\&P 500', r'cîștigul este mare pentru Bitcoin și mic pentru S\&P 500')]),
    (T(r'Recent studies reach mixed verdicts \refGoe, \refBri, \refRNW', r'Studii recente ajung la verdicte mixte \refGoe, \refBri, \refRNW'),
     [T('gains depend on the asset, the horizon and the loss; fine-tuning or pretraining on financial data often matters', 'cîștigurile depind de activ, de orizont și de funcția de pierdere; fine-tuning-ul sau preantrenarea pe date financiare contează adesea')])])

chart(T('Before and after the releases', 'Înainte și după lansări'), 'ats_ch13_contamination', 'ATS_ch13_benchmark', [
    T(r'Relative loss of each model in an earlier window and in the window after every release (from 1 November 2025): load (MAE / expert ARX) and Bitcoin (QLIKE / HAR)',
      r'Pierderea relativă a fiecărui model într-o fereastră anterioară și în fereastra de după toate lansările (din 1 noiembrie 2025): consum (MAE / ARX expert) și Bitcoin (QLIKE / HAR)')],
    h='0.5\\textheight')

interp(('the contamination check', 'verificării contaminării'), [
    T(r'Load, Chronos-2: @{ct.l.c2a} before, @{ct.l.c2b} after; TimesFM: @{ct.l.tfa}, @{ct.l.tfb}; the earlier window (January--October 2025) precedes both releases',
      r'Consum, Chronos-2: @{ct.l.c2a} înainte, @{ct.l.c2b} după; TimesFM: @{ct.l.tfa}, @{ct.l.tfb}; fereastra anterioară (ianuarie--octombrie 2025) precede ambele lansări'),
    T(r'Bitcoin, Chronos-2: @{ct.b.c2a} (2021 -- 24 November 2024) and @{ct.b.c2b} (after); TiRex: @{ct.b.txa}, @{ct.b.txb}; post-release windows have @{ct.nl} and @{ct.nb} days',
      r'Bitcoin, Chronos-2: @{ct.b.c2a} (2021 -- 24 noiembrie 2024) și @{ct.b.c2b} (după); TiRex: @{ct.b.txa}, @{ct.b.txb}; ferestrele de după lansare au @{ct.nl} și @{ct.nb} zile'),
    (T('No deterioration after the releases (for Bitcoin the ratios are even lower): no evidence of contamination here', 'Nicio deteriorare după lansări (pentru Bitcoin rapoartele sînt chiar mai mici): nicio dovadă de contaminare aici'),
     [T('but the absence of a drop does not prove the absence of leakage, and markets change between windows', 'dar absența unei scăderi nu dovedește absența leakage-ului, iar piețele se schimbă între ferestre')])])

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
    (T('Findings of the paper', 'Rezultatele lucrării'),
     [T('competitive zero-shot on some benchmarks', 'competitiv zero-shot pe unele benchmark-uri'),
      T('the tokenisation of numbers matters: a newer model could do worse because of how it splits digits', 'tokenizarea numerelor contează: un model mai nou putea fi mai slab din cauza felului în care împarte cifrele'),
      T('alignment (RLHF) hurts calibration', 'alinierea (RLHF) deteriorează calibrarea')]),
    T('Costs: thousands of tokens per series and many samples per forecast; the context window limits the history; the LLM may have memorised the data',
      'Costuri: mii de token-uri pe serie și multe eșantioane pentru o prognoză; fereastra de context limitează istoria; LLM-ul poate să fi memorat datele')), 'small')

D.frame(T('Reprogramming a frozen LLM', 'Reprogramarea unui LLM înghețat'), items(
    (T(r'\textbf{Time-LLM} \refJin', r'\textbf{Time-LLM} \refJin'),
     [T('patches of the series are mapped onto text prototypes (word embeddings)', 'patch-urile seriei sînt proiectate pe prototipuri de text (embedding-uri de cuvinte)'),
      T('a prompt prefix describes the task and the statistics of the series', 'un prefix de prompt descrie sarcina și statisticile seriei'),
      T('the LLM stays frozen; a trained projection reads the forecast', 'LLM-ul rămîne înghețat; o proiecție antrenată citește prognoza')]),
    (T(r'\textbf{One Fits All} (GPT4TS) \refZho', r'\textbf{One Fits All} (GPT4TS) \refZho'),
     [T('a frozen GPT-2; only the input embedding, the layer norms and the output layer are trained', 'un GPT-2 înghețat; se antrenează doar embedding-ul de intrare, normalizările de strat și stratul de ieșire'),
      T('one model for forecasting, classification and anomaly detection', 'un singur model pentru prognoză, clasificare și detectarea anomaliilor')]),
    (T('The claim: knowledge from language transfers to series', 'Afirmația: cunoașterea din limbaj se transferă la serii'),
     [T('the test of the claim is an ablation that removes the language model', 'testul afirmației este o ablație care elimină modelul de limbaj')])), 'small')

D.frame(T('Case study: are language models actually useful?', 'Studiu de caz: sînt modelele de limbaj chiar utile?'), two(
    items(T(r'\refTan: three LLM-based forecasters (including Time-LLM and GPT4TS), the same benchmarks, three ablations',
            r'\refTan: trei prognozatori pe bază de LLM (inclusiv Time-LLM și GPT4TS), aceleași benchmark-uri, trei ablații'),
          (T('Ablations', 'Ablațiile'),
           [T('remove the LLM; replace it by one attention layer; replace it by a basic Transformer block', 'eliminarea LLM-ului; înlocuirea lui cu un strat de atenție; înlocuirea cu un bloc Transformer simplu')]),
          (T('Result: no degradation, often an improvement', 'Rezultat: nicio degradare, adesea o îmbunătățire'),
           [T('pretrained LLMs do no better than the same model trained from scratch', 'LLM-urile preantrenate nu sînt mai bune decît același model antrenat de la zero'),
            T('they do not model sequential dependence and do not help in few-shot settings', 'nu modelează dependența secvențială și nu ajută cînd datele sînt puține')]),
          T('Training and inference cost orders of magnitude more', 'Antrenarea și inferența costă cu ordine de mărime mai mult')),
    items((T('The method matters more than the result', 'Metoda contează mai mult decît rezultatul'),
           [T('an architecture claim needs an ablation with matched compute and tuning', 'o afirmație despre arhitectură cere o ablație cu calcul și ajustare comparabile')]),
          (T('Scope of the critique', 'Ce vizează critica'),
           [T('LLMs used as forecasters are affected', 'LLM-urile folosite ca prognozatori sînt vizate'),
            T('foundation models trained on series (Chronos, TimesFM, TiRex) are not', 'foundation models antrenate pe serii (Chronos, TimesFM, TiRex) nu sînt vizate'),
            T(r'LLMs remain useful around forecasting: code, literature, critique (Section 9)', r'LLM-urile rămîn utile în jurul prognozei: cod, literatură, critică (secțiunea 9)')])), '0.56', '0.42'), 'small')

D.frame(T('Memorisation and look-ahead', 'Memorare și anticiparea viitorului'), items(
    (T(r'LLMs recall their training period \refLTZ', r'LLM-urile își amintesc perioada de antrenare \refLTZ'),
     [T('they reproduce macroeconomic and market values from that period with high precision, even when asked not to use future information', 'reproduc cu mare precizie valori macroeconomice și de piață din acea perioadă, chiar și cînd li se cere să nu folosească informații viitoare'),
      T('a backtest before the training cutoff measures recall, not forecasting', 'un backtest înainte de data-limită a antrenării măsoară memoria, nu capacitatea de prognoză')]),
    (T('The same logic for time-series foundation models', 'Aceeași logică pentru foundation models pe serii de timp'),
     [T('it applies to public series in the corpus (electricity, traffic, M4)', 'ea se aplică seriilor publice din corpus (electricitate, trafic, M4)'),
      T('our evidence: windows after every release (Section 4)', 'dovezile noastre: ferestre de după toate lansările (secțiunea 4)'),
      T('the strongest evidence: live, pre-registered forecasts', 'cele mai puternice dovezi: prognoze live, preînregistrate')]),
    (T('A practical rule', 'O regulă practică'),
     [T('state the training cutoff of every model and the start of the evaluation window in the same table', 'precizați data-limită de antrenare a fiecărui model și începutul ferestrei de evaluare în același tabel')])), 'small')

D.recap(('LLMs', 'LLM'), [
    T('LLMTime and reprogramming show that text models can be bent to series; ablations show the language part is rarely what helps', 'LLMTime și reprogramarea arată că modelele de text pot fi adaptate la serii; ablațiile arată că partea de limbaj rareori este cea care ajută'),
    T('Memorisation makes pre-cutoff evaluation of LLM forecasts invalid', 'Memorarea face ca evaluarea prognozelor LLM înainte de data-limită să nu fie validă'),
    T('For forecasting, foundation models trained on series are the default; LLMs remain useful for code, literature and critique', 'Pentru prognoză, foundation models antrenate pe serii sînt alegerea implicită; LLM-urile rămîn utile pentru cod, literatură și critică')])

# =============================================================================
# 6. PREDICȚIA CONFORMALĂ
# =============================================================================
D.section('Conformal prediction', 'Predicția conformală')

D.frame(T('Where conformal prediction comes from', 'Originea predicției conformale'), two(
    ph('gammerman', T('Alexander Gammerman, Royal Holloway, 2018', 'Alexander Gammerman, Royal Holloway, 2018'), h='0.36\\textheight'),
    items((T(r'\refVGS; \refVGSb', r'\refVGS; \refVGSb'),
           [T('prediction sets valid in finite samples', 'mulțimi de predicție valide în eșantioane finite'),
            T('only exchangeability is assumed, for any predictive model', 'se presupune doar interschimbabilitatea, pentru orice model predictiv')]),
          (T('The idea', 'Ideea'),
           [T("how ``conforming'' a candidate value is to the data seen, measured by a rank", 'cît de „conformă” este o valoare candidat cu datele văzute, măsurat printr-un rang')]),
          (T(r'Modern statistics \refLei; \refAB', r'Statistica modernă \refLei; \refAB'),
           [T('adopted it as a wrapper around machine learning methods', 'a adoptat-o ca înveliș în jurul metodelor de machine learning')])), '0.42', '0.56'), 'small')

D.frame(T('Exchangeability and the target guarantee (1/2)', 'Interschimbabilitatea și garanția urmărită (1/2)'), items(
    (T(r'Data: $n$ calibration points and one test point, $Z_i = (X_i, Y_i)$, $i = 1, \dots, n + 1$',
       r'Datele: $n$ puncte de calibrare și un punct de test, $Z_i = (X_i, Y_i)$, $i = 1, \dots, n + 1$'),
     [T(r'$X_i$: the predictors (features, lags, a model forecast); $Y_i$: the value to be covered; $Z_{n+1}$: the test point, whose $Y_{n+1}$ is unknown',
        r'$X_i$: predictorii (variabile, laguri, o prognoză de model); $Y_i$: valoarea care trebuie acoperită; $Z_{n+1}$: punctul de test, al cărui $Y_{n+1}$ este necunoscut')]),
    (T(r'\textbf{Exchangeability}: any reordering of the points has the same joint distribution',
       r'\textbf{Interschimbabilitatea}: orice reordonare a punctelor are aceeași distribuție comună'),
     [r'\[ (Z_{\pi(1)}, \dots, Z_{\pi(n+1)}) \overset{d}{=} (Z_1, \dots, Z_{n+1}) \quad \text{' + T('for every permutation', 'pentru orice permutare') + r'} \ \pi \]',
      T(r'$\pi$: a permutation (reordering) of $\{1, \dots, n + 1\}$; $\overset{d}{=}$: equal in distribution', r'$\pi$: o permutare (reordonare) a mulțimii $\{1, \dots, n + 1\}$; $\overset{d}{=}$: egalitate în distribuție')]),
    (T('Examples', 'Exemple'),
     [T('i.i.d.\\ data are exchangeable', 'datele i.i.d.\\ sînt interschimbabile'),
      T('draws without replacement are exchangeable but dependent', 'extragerile fără întoarcere sînt interschimbabile, dar dependente'),
      T(r'a stationary AR(1) $y_t = \phi y_{t-1} + \varepsilon_t$, $0 < |\phi| < 1$, is not: $\mathrm{corr}(y_1, y_2) = \phi \ne \phi^2 = \mathrm{corr}(y_1, y_3)$, so swapping $y_2$ and $y_3$ changes the joint law',
        r'un AR(1) staționar $y_t = \phi y_{t-1} + \varepsilon_t$, $0 < |\phi| < 1$, nu este: $\mathrm{corr}(y_1, y_2) = \phi \ne \phi^2 = \mathrm{corr}(y_1, y_3)$, deci schimbarea între ele a lui $y_2$ și $y_3$ modifică legea comună')])), 'small')

D.frame(T('Exchangeability and the target guarantee (2/2)', 'Interschimbabilitatea și garanția urmărită (2/2)'), items(
    (T(r'\textbf{Marginal coverage}: the prediction set contains the test value with probability at least $1 - \alpha$',
       r'\textbf{Acoperirea marginală}: mulțimea de predicție conține valoarea de test cu probabilitatea de cel puțin $1 - \alpha$'),
     [r'\[ \Pr\{Y_{n+1} \in \hat C(X_{n+1})\} \ge 1 - \alpha \]',
      T(r'$\hat C(x)$: the prediction set (usually an interval) built from the calibration data; $\alpha$: the allowed miss rate, e.g.\ 0.1 for a 90\% interval',
        r'$\hat C(x)$: mulțimea de predicție (de obicei un interval) construită din datele de calibrare; $\alpha$: rata de ratare admisă, de exemplu 0,1 pentru un interval de 90\%'),
      T('the probability is taken over the calibration data and the test point together', 'probabilitatea este luată împreună pe datele de calibrare și pe punctul de test')]),
    (T(r'What it is not', r'Ce nu garantează'),
     [T(r'\textbf{conditional} coverage, $\Pr\{Y \in \hat C(x) \mid X = x\} \ge 1 - \alpha$ for every value $x$', r'acoperirea \textbf{condiționată}, $\Pr\{Y \in \hat C(x) \mid X = x\} \ge 1 - \alpha$ pentru orice valoare $x$'),
      T('coverage given one particular calibration sample', 'acoperirea condiționată de un anumit eșantion de calibrare')]),
    (T(r'A \textbf{nonconformity score} $s(x, y)$: a number that is large when $y$ is unusual given $x$',
       r'Un \textbf{scor de neconformitate} $s(x, y)$: un număr care este mare cînd $y$ este neobișnuit dat fiind $x$'),
     [T(r'examples: $|y - \hat\mu(x)|$, $|y - \hat\mu(x)|/\hat\sigma(x)$, or the CQR score below', r'exemple: $|y - \hat\mu(x)|$, $|y - \hat\mu(x)|/\hat\sigma(x)$ sau scorul CQR de mai jos'),
      T(r'$\hat\mu(x)$: a point forecast of $y$ given $x$; $\hat\sigma(x)$: a forecast of its spread (e.g.\ a GARCH volatility)', r'$\hat\mu(x)$: o prognoză punctuală a lui $y$ dat fiind $x$; $\hat\sigma(x)$: o prognoză a dispersiei (de exemplu o volatilitate GARCH)')])), 'small')

D.frame(T('Split conformal prediction (1/2)', 'Predicția split conformal (1/2)'), items(
    (T(r'Step 1: fit a forecasting model $\hat\mu$ on a training set \refPap, \refLei', r'Pasul 1: se estimează un model de prognoză $\hat\mu$ pe un set de antrenare \refPap, \refLei'), []),
    (T(r'Step 2: compute the scores of the $n$ calibration points, which were not used in step 1', r'Pasul 2: se calculează scorurile celor $n$ puncte de calibrare, nefolosite la pasul 1'),
     [r'\[ S_i = s(X_i, Y_i), \qquad i = 1, \dots, n \]']),
    (T(r'Step 3: the threshold $\hat q$ is the $k$-th smallest calibration score', r'Pasul 3: pragul $\hat q$ este al $k$-lea cel mai mic scor de calibrare'),
     [r'\[ \hat q = S_{(k)}, \qquad k = \lceil (n + 1)(1 - \alpha) \rceil \]',
      T(r'$S_{(k)}$: the $k$-th order statistic of $S_1, \dots, S_n$; $\lceil\cdot\rceil$: rounding up to an integer; $\hat q = +\infty$ if $k > n$', r'$S_{(k)}$: statistica de ordine $k$ a scorurilor $S_1, \dots, S_n$; $\lceil\cdot\rceil$: rotunjirea în sus la un întreg; $\hat q = +\infty$ dacă $k > n$'),
      T(r'example: $n = 99$, $\alpha = 0.1$ gives $k = 90$, the 90th smallest of the 99 scores', r'exemplu: $n = 99$, $\alpha = 0{,}1$ dă $k = 90$, al 90-lea cel mai mic dintre cele 99 de scoruri')]),
    (T(r'Step 4: the prediction set keeps every candidate value whose score does not exceed the threshold', r'Pasul 4: mulțimea de predicție păstrează orice valoare candidată al cărei scor nu depășește pragul'),
     [r'\[ \hat C(x) = \{y: s(x, y) \le \hat q\} \]',
      T(r'with $s(x, y) = |y - \hat\mu(x)|$: the interval $\hat\mu(x) \pm \hat q$', r'cu $s(x, y) = |y - \hat\mu(x)|$: intervalul $\hat\mu(x) \pm \hat q$')])), 'small')

D.frame(T('Split conformal prediction (2/2)', 'Predicția split conformal (2/2)'), items(
    (T(r'\textbf{Theorem}: if the points $(X_i, Y_i)$, $i = 1, \dots, n + 1$, are exchangeable, then', r'\textbf{Teoremă}: dacă punctele $(X_i, Y_i)$, $i = 1, \dots, n + 1$, sînt interschimbabile, atunci'),
     [r'\[ 1 - \alpha \le \Pr\{Y_{n+1} \in \hat C(X_{n+1})\} \le 1 - \alpha + \frac{1}{n + 1} \]',
      T('the upper bound requires no ties among the scores (continuous scores)', 'marginea superioară cere ca scorurile să nu aibă egalități (scoruri continue)')]),
    (T(r'Idea of the proof (Appendix)', r'Ideea demonstrației (Anexă)'),
     [T(r'given $\hat\mu$, the scores $S_1, \dots, S_{n+1}$ are exchangeable, so the rank of $S_{n+1}$ among them is uniform on $\{1, \dots, n + 1\}$',
        r'dat fiind $\hat\mu$, scorurile $S_1, \dots, S_{n+1}$ sînt interschimbabile, deci rangul lui $S_{n+1}$ printre ele este uniform pe $\{1, \dots, n + 1\}$'),
      T(r'$Y_{n+1} \in \hat C(X_{n+1})$ exactly when this rank is at most $k$, which has probability $k/(n + 1) \ge 1 - \alpha$',
        r'$Y_{n+1} \in \hat C(X_{n+1})$ exact atunci cînd acest rang este cel mult $k$, ceea ce are probabilitatea $k/(n + 1) \ge 1 - \alpha$')]),
    (T('No assumption on the model or on the distribution', 'Nicio ipoteză asupra modelului sau a distribuției'),
     [T('a bad model gives wide intervals, not invalid ones', 'un model slab dă intervale largi, nu intervale invalide')])), 'small')

chart(T('Coverage given the calibration set', 'Acoperirea condiționată de setul de calibrare'), 'ats_ch13_split_coverage', 'ATS_ch13_conformal_basics', [
    T(r'Coverage $F(\hat q)$ of the next point for @{sp.reps} calibration sets of $n = 50$ and $n = 500$ scores, $\alpha = 0.1$, and the exact law Beta($k$, $n + 1 - k$)',
      r'Acoperirea $F(\hat q)$ a punctului următor pentru @{sp.reps} de seturi de calibrare cu $n = 50$ și cu $n = 500$ de scoruri, $\alpha = 0{,}1$, și legea exactă Beta($k$, $n + 1 - k$)'),
    T(r'$F$: the distribution function of the scores, so $F(\hat q) = \Pr\{S_{n+1} \le \hat q \mid \text{calibration set}\}$ is the coverage obtained with one given calibration set',
      r'$F$: funcția de repartiție a scorurilor, deci $F(\hat q) = \Pr\{S_{n+1} \le \hat q \mid \text{setul de calibrare}\}$ este acoperirea obținută cu un anumit set de calibrare')],
    h='0.48\\textheight')

interp(('the coverage distribution', 'distribuției acoperirii'), [
    T(r'Mean coverage @{sp.m50} ($n = 50$) and @{sp.m500} ($n = 500$), as the theory gives (@{sp.t50}, @{sp.t500}): the marginal guarantee holds on average over calibration sets',
      r'Acoperirea medie @{sp.m50} ($n = 50$) și @{sp.m500} ($n = 500$), cum dă teoria (@{sp.t50}, @{sp.t500}): garanția marginală este valabilă în medie pe seturile de calibrare'),
    T(r'One calibration set is one draw: s.d.\ @{sp.s50} and @{sp.s500}; with $n = 50$, @{sp.b50}\% of the sets give coverage below 0.88, with $n = 500$ only @{sp.b500}\%',
      r'Un set de calibrare este o singură extragere: abaterea standard @{sp.s50} și @{sp.s500}; cu $n = 50$, @{sp.b50}\% dintre seturi dau acoperire sub 0,88, cu $n = 500$ doar @{sp.b500}\%'),
    (T(r'Since $F(\hat q) \sim$ Beta($k$, $n + 1 - k$), choosing $n$ is a sample-size calculation', r'Deoarece $F(\hat q) \sim$ Beta($k$, $n + 1 - k$), alegerea lui $n$ este un calcul de mărime a eșantionului'),
     [T(r'the standard deviation of the realised coverage is about $\sqrt{\alpha(1 - \alpha)/n}$: quadrupling $n$ halves it',
        r'abaterea standard a acoperirii realizate este aproximativ $\sqrt{\alpha(1 - \alpha)/n}$: pentru a o înjumătăți, $n$ trebuie înmulțit cu 4')])])

D.frame(T('Conformalized quantile regression', 'Regresia cuantilică conformalizată'), two(
    ph('candes', T('Emmanuel Candès, 2012', 'Emmanuel Candès, 2012'), h='0.34\\textheight'),
    items((T(r'\refRPC: fit two quantile regressions \refKB on the training set', r'\refRPC: se estimează două regresii cuantilice \refKB pe setul de antrenare'),
           [T(r'$\hat q_{\alpha/2}(x)$, $\hat q_{1-\alpha/2}(x)$: the estimated lower and upper conditional quantiles of $Y$ given $X = x$', r'$\hat q_{\alpha/2}(x)$, $\hat q_{1-\alpha/2}(x)$: cuantilele condiționate inferioară și superioară ale lui $Y$ dat fiind $X = x$, estimate')]),
          (T(r'\textbf{CQR score}: the signed distance of $y$ outside the band', r'\textbf{Scorul CQR}: distanța cu semn a lui $y$ în afara benzii'),
           [r'\[ s(x, y) = \max\{\hat q_{\alpha/2}(x) - y,\; y - \hat q_{1-\alpha/2}(x)\} \]',
            T('negative inside the band, positive outside', 'negativ în interiorul benzii, pozitiv în afara ei')]),
          (T(r'\textbf{Interval}: the band widened on both sides by the conformal threshold $\hat q$ of these scores', r'\textbf{Intervalul}: banda lărgită pe ambele părți cu pragul conformal $\hat q$ al acestor scoruri'),
           [r'\[ \hat C(x) = [\hat q_{\alpha/2}(x) - \hat q,\; \hat q_{1-\alpha/2}(x) + \hat q] \]',
            T(r'$\hat q < 0$: the band was too wide and is narrowed', r'$\hat q < 0$: banda era prea largă și este îngustată')]),
          (T('Properties', 'Proprietăți'),
           [T('marginal coverage by the split theorem; the width adapts to heteroskedasticity through the quantile models', 'acoperirea marginală rezultă din teorema split; lățimea se adaptează la heteroscedasticitate prin modelele cuantilice'),
            T('the same score calibrates the quantiles of any foundation model (Section 8)', 'același scor calibrează cuantilele oricărui foundation model (secțiunea 8)')])), '0.32', '0.66'), 'footnotesize')

chart(T('CQR on the design of Romano, Patterson and Candès', 'CQR pe designul lui Romano, Patterson și Candès'), 'ats_ch13_cqr', 'ATS_ch13_conformal_basics', [
    T(r'Simulated data (their Figure 1): $Y = \mathrm{Pois}(\sin^2 X + 0.1) + 0.03X\varepsilon_1 + 25\cdot\mathbf 1\{U < 0.01\}\varepsilon_2$, $X \sim U[0, 5]$',
      r'Date simulate (Figura 1 din lucrare): $Y = \mathrm{Pois}(\sin^2 X + 0{,}1) + 0{,}03X\varepsilon_1 + 25\cdot\mathbf 1\{U < 0{,}01\}\varepsilon_2$, $X \sim U[0, 5]$'),
    T(r'$\mathrm{Pois}(\lambda)$: a Poisson draw with mean $\lambda$; $\varepsilon_1, \varepsilon_2$: standard Normal noise; $U \sim U[0, 1]$, so 1\% of the points get a large outlier; noise grows with $X$',
      r'$\mathrm{Pois}(\lambda)$: o extragere Poisson cu media $\lambda$; $\varepsilon_1, \varepsilon_2$: zgomot cu distribuția Normală standard; $U \sim U[0, 1]$, deci 1\% dintre puncte primesc o valoare extremă mare; zgomotul crește cu $X$'),
    T(r'1000 training and 1000 calibration points; gradient boosting for the mean and for the 5\% and 95\% quantiles',
      r'1000 de puncte de antrenare și 1000 de calibrare; gradient boosting pentru medie și pentru cuantilele de 5\% și 95\%')],
    h='0.44\\textheight')

interp(('CQR', 'CQR'), [
    T(r'Test coverage: split conformal @{cq.sc}, CQR @{cq.cc}, the raw quantile models @{cq.rc}; mean width @{cq.sw}, @{cq.cw} and @{cq.rw}',
      r'Acoperirea pe datele de test: split conformal @{cq.sc}, CQR @{cq.cc}, modelele cuantilice brute @{cq.rc}; lățimea medie @{cq.sw}, @{cq.cw} și @{cq.rw}'),
    T(r'The raw quantile regressions undercover; CQR repairs them at almost no extra width, while the constant-width split band is @{cq.ratio}\% wider',
      r'Regresiile cuantilice brute au o acoperire prea mică; CQR le corectează aproape fără lățime suplimentară, în timp ce banda split de lățime constantă este cu @{cq.ratio}\% mai largă'),
    (T(r'By $X$ bins both stay within a few points of 90\% (worst bins: CQR @{cq.cmin}, split @{cq.smin})', r'Pe intervale ale lui $X$, ambele rămîn la cîteva puncte de 90\% (cele mai slabe intervale: CQR @{cq.cmin}, split @{cq.smin})'),
     [T(r'the gain of CQR is in width: narrow where $Y$ is concentrated, wide where the Poisson noise is large', r'cîștigul CQR este în lățime: îngust acolo unde $Y$ este concentrat, larg acolo unde zgomotul Poisson este mare')])])

D.frame(T('The limits of conditional coverage', 'Limitele acoperirii condiționate'), items(
    (T(r'\textbf{Impossibility} \refVov; \refLW; \refBarB', r'\textbf{Imposibilitate} \refVov; \refLW; \refBarB'),
     [T(r'if $\hat C$ has conditional coverage $\ge 1 - \alpha$ at almost every $x$, for every distribution with a continuous $X$, its expected length is infinite',
        r'dacă $\hat C$ are acoperire condiționată $\ge 1 - \alpha$ în aproape orice $x$, pentru orice distribuție cu $X$ continuu, lungimea lui așteptată este infinită'),
      T('no finite-sample method can certify coverage at each point of a continuous covariate without assumptions', 'nicio metodă nu poate certifica în eșantioane finite acoperirea în fiecare punct al unei covariabile continue fără ipoteze')]),
    (T(r'What is achievable', r'Rezultate posibile'),
     [T('coverage within each of a finite set of groups (Mondrian conformal: calibrate separately by group)', 'acoperire în fiecare dintre un număr finit de grupuri (conformal Mondrian: calibrare separată pe grupuri)'),
      T('approximate conditional coverage under smoothness assumptions', 'acoperire condiționată aproximativă, sub ipoteze de netezime'),
      T('coverage conditional on the calibration set, with high probability (Beta law)', 'acoperire condiționată de setul de calibrare, cu probabilitate mare (legea Beta)')]),
    (T('For time series the relevant condition is the past: the target is $\\Pr\\{Y_t \\in \\hat C_t \\mid \\mathcal F_{t-1}\\} = 1 - \\alpha$',
       'Pentru serii de timp, condiția relevantă este trecutul: ținta este $\\Pr\\{Y_t \\in \\hat C_t \\mid \\mathcal F_{t-1}\\} = 1 - \\alpha$'),
     [T(r'$\mathcal F_{t-1}$: the information available at $t - 1$; $\hat C_t$: the set built at $t - 1$ for period $t$', r'$\mathcal F_{t-1}$: informația disponibilă la $t - 1$; $\hat C_t$: mulțimea construită la $t - 1$ pentru perioada $t$'),
      T('a VaR backtest (Chapter 9) tests exactly this property for one-sided sets', 'un backtest VaR (Capitolul 9) testează exact această proprietate pentru mulțimi unilaterale')])), 'small')

D.recap(('conformal prediction', 'predicția conformală'), [
    T('Split conformal: a rank argument gives finite-sample marginal coverage under exchangeability, for any model', 'Split conformal: un argument de rang dă acoperire marginală în eșantioane finite sub interschimbabilitate, pentru orice model'),
    T('CQR adds adaptivity; the calibration sample size controls the variability of realised coverage', 'CQR adaugă adaptivitate; mărimea eșantionului de calibrare controlează variabilitatea acoperirii realizate'),
    T('Conditional coverage is impossible in general: test it, do not claim it', 'Acoperirea condiționată este imposibilă în general: testați-o, nu o afirmați')])

# =============================================================================
# 7. CONFORMAL PENTRU DATE DEPENDENTE
# =============================================================================
D.section('Conformal prediction for dependent data', 'Predicția conformală pentru date dependente')

D.frame(T('Exchangeability violated: what survives', 'Interschimbabilitatea încălcată: rezultatele care rămîn valabile'), items(
    (T('Time series violate exchangeability three ways: serial dependence, changing volatility, structural change; the last two break coverage most', 'Seriile de timp încalcă interschimbabilitatea în trei feluri: dependența serială, volatilitatea variabilă, schimbările structurale; ultimele două afectează cel mai mult acoperirea'), []),
    (T(r'\textbf{Stationary and mixing}: split conformal remains approximately valid \refOli',
       r'\textbf{Staționar și mixing}: split conformal rămîne aproximativ valid \refOli'),
     [T(r'the coverage gap shrinks with the calibration size and with the $\beta$-mixing coefficients, which measure how fast the dependence between distant observations dies out',
        r'abaterea acoperirii scade cu mărimea calibrării și cu coeficienții $\beta$-mixing, care măsoară cît de repede dispare dependența dintre observațiile îndepărtate'),
      T(r'block permutations restore exactness under weaker conditions \refCWZ', r'permutările pe blocuri refac exactitatea sub condiții mai slabe \refCWZ')]),
    (T(r'\textbf{Non-stationary}: no static method can work; the threshold must move with the data',
       r'\textbf{Nestaționar}: nicio metodă statică nu poate funcționa; pragul trebuie să se miște odată cu datele'),
     [T('weights (Barber et al.), refitting (EnbPI), feedback on errors (ACI, PID)', 'ponderi (Barber et al.), reestimare (EnbPI), reacție la erori (ACI, PID)')]),
    (T(r'\textbf{A common online frame} for the next slides', r'\textbf{Un cadru online comun} pentru slide-urile următoare'),
     [T(r'$S_t = s(X_t, Y_t)$: the score of period $t$, computed from an out-of-sample forecast', r'$S_t = s(X_t, Y_t)$: scorul perioadei $t$, calculat dintr-o prognoză în afara eșantionului'),
      T(r'$q_t$: the threshold used at $t$, chosen from the past scores $S_1, \dots, S_{t-1}$; the set is $\hat C_t = \{y: s(X_t, y) \le q_t\}$', r'$q_t$: pragul folosit la $t$, ales din scorurile trecute $S_1, \dots, S_{t-1}$; mulțimea este $\hat C_t = \{y: s(X_t, y) \le q_t\}$'),
      T(r'$\mathrm{err}_t = \mathbf 1\{S_t > q_t\}$: the miss indicator, 1 if $Y_t$ falls outside $\hat C_t$', r'$\mathrm{err}_t = \mathbf 1\{S_t > q_t\}$: indicatorul ratării, 1 dacă $Y_t$ cade în afara lui $\hat C_t$')])), 'small')

D.frame(T('Conformal prediction beyond exchangeability (1/2)', 'Predicția conformală dincolo de interschimbabilitate (1/2)'), items(
    (T(r'\refBar: each calibration score gets a fixed weight $w_i \in [0, 1]$, chosen before seeing the data; the test point gets weight $w_{n+1} = 1$',
       r'\refBar: fiecare scor de calibrare primește o pondere fixă $w_i \in [0, 1]$, aleasă înainte de a vedea datele; punctul de test primește ponderea $w_{n+1} = 1$'),
     [T(r'normalised weights $\tilde w_i = w_i/(1 + \sum_{j=1}^n w_j)$, $i = 1, \dots, n + 1$; they sum to 1', r'ponderile normalizate $\tilde w_i = w_i/(1 + \sum_{j=1}^n w_j)$, $i = 1, \dots, n + 1$; însumează 1')]),
    (T(r'The threshold $\hat q$ is the $(1 - \alpha)$ quantile of the weighted distribution of the scores, with the test point placed at $+\infty$',
       r'Pragul $\hat q$ este cuantila $(1 - \alpha)$ a distribuției ponderate a scorurilor, cu punctul de test plasat la $+\infty$'),
     [r'\[ \hat q = Q_{1-\alpha}\Big(\sum_{i=1}^n \tilde w_i\,\delta_{S_i} + \tilde w_{n+1}\,\delta_{+\infty}\Big) \]',
      T(r'$\delta_a$: a unit point mass at $a$; $Q_{1-\alpha}(\cdot)$: the $(1 - \alpha)$ quantile of a distribution', r'$\delta_a$: o masă de probabilitate unitară în punctul $a$; $Q_{1-\alpha}(\cdot)$: cuantila $(1 - \alpha)$ a unei distribuții'),
      T(r'with all $w_i = 1$ this is the split conformal threshold', r'cu toate $w_i = 1$, acesta este pragul split conformal')]),
    (T(r'\textbf{Covariate shift} with a known likelihood ratio: the weights $w(x) = dP_{\mathrm{test}}/dP_{\mathrm{train}}$ give exact coverage \refTBCR',
       r'\textbf{Schimbarea distribuției covariabilelor} cu raport de verosimilitate cunoscut: ponderile $w(x) = dP_{\mathrm{test}}/dP_{\mathrm{train}}$ dau acoperire exactă \refTBCR'),
     [T(r'$dP_{\mathrm{test}}/dP_{\mathrm{train}}$: the ratio of the densities of $X$ in the test and in the training population', r'$dP_{\mathrm{test}}/dP_{\mathrm{train}}$: raportul densităților lui $X$ în populația de test și în cea de antrenare')])), 'small')

D.frame(T('Conformal prediction beyond exchangeability (2/2)', 'Predicția conformală dincolo de interschimbabilitate (2/2)'), items(
    (T(r'\textbf{Theorem} \refBar: the coverage loss is bounded by the weighted distance from exchangeability',
       r'\textbf{Teoremă} \refBar: pierderea de acoperire este mărginită de distanța ponderată față de interschimbabilitate'),
     [r'\[ \Pr\{Y_{n+1} \in \hat C(X_{n+1})\} \ge 1 - \alpha - \sum_{i=1}^n \tilde w_i\, d_{\mathrm{TV}}(Z, Z^i) \]',
      T(r'$Z = (Z_1, \dots, Z_{n+1})$: the data; $Z^i$: the same data with the test point and point $i$ swapped', r'$Z = (Z_1, \dots, Z_{n+1})$: datele; $Z^i$: aceleași date, cu punctul de test și punctul $i$ schimbate între ele'),
      T(r'$d_{\mathrm{TV}}$: the total variation distance between two distributions, in $[0, 1]$; 0 when they coincide', r'$d_{\mathrm{TV}}$: distanța în variație totală dintre două distribuții, în $[0, 1]$; 0 cînd coincid')]),
    (T(r'Under exchangeability every $d_{\mathrm{TV}}(Z, Z^i) = 0$ and the gap vanishes', r'Sub interschimbabilitate, toți termenii $d_{\mathrm{TV}}(Z, Z^i)$ sînt 0, iar abaterea dispare'), []),
    (T(r'Under slow drift, $d_{\mathrm{TV}}$ is small for recent points: give them the largest weights', r'Sub o derivă lentă, $d_{\mathrm{TV}}$ este mic pentru punctele recente: acestea primesc ponderile cele mai mari'),
     [T(r'geometric weights $w_i = \rho^{n+1-i}$, $\rho \in (0, 1)$: the weight halves every $\ln 2/|\ln\rho|$ steps', r'ponderi geometrice $w_i = \rho^{n+1-i}$, $\rho \in (0, 1)$: ponderea se înjumătățește la fiecare $\ln 2/|\ln\rho|$ pași'),
      T(r'effective sample size $\approx 1/(1 - \rho)$: $\rho = 0.99$ uses about 100 recent scores', r'mărimea efectivă a eșantionului $\approx 1/(1 - \rho)$: $\rho = 0{,}99$ folosește aproximativ 100 de scoruri recente'),
      T(r'a smaller $\rho$ adapts faster but makes the threshold more variable', r'un $\rho$ mai mic se adaptează mai repede, dar face pragul mai variabil')])), 'small')

chart(T('Weighted conformal under changepoints', 'Predicția conformală ponderată la puncte de schimbare'), 'ats_ch13_weighted', 'ATS_ch13_conformal_time', [
    T(r'Simulated regression $Y_t = X_t\'\beta_t + \varepsilon_t$: $X_t \sim N(0, I_4)$, four independent standard Normal regressors ($I_4$: the $4 \times 4$ identity matrix); $\varepsilon_t$: Normal noise; the coefficient vector $\beta_t$ changes at $t = 500$ and $t = 1500$',
      r'Regresie simulată $Y_t = X_t\'\beta_t + \varepsilon_t$: $X_t \sim N(0, I_4)$, patru regresori independenți cu distribuția Normală standard ($I_4$: matricea unitate $4 \times 4$); $\varepsilon_t$: zgomot cu distribuția Normală; vectorul de coeficienți $\beta_t$ se schimbă la $t = 500$ și $t = 1500$'),
    T(r'Least squares on all past data; scores: absolute one-step-ahead residuals (prequential: each computed before $Y_t$ is used); coverage averaged over 200 runs (20-step moving average)',
      r'Cele mai mici pătrate pe toate datele trecute; scorurile: reziduurile absolute la un pas (prequential: fiecare calculat înainte ca $Y_t$ să fie folosit); acoperirea mediată pe 200 de rulări (medie mobilă pe 20 de pași)')],
    h='0.42\\textheight')

interp(('the weighted method', 'metodei ponderate'), [
    T(r'Average coverage after the burn-in: standard @{wt.sc}, weighted ($\rho = 0.99$) @{wt.wc}; worst 20-step average @{wt.smin} against @{wt.wmin}',
      r'Acoperirea medie după perioada inițială: standard @{wt.sc}, ponderat ($\rho = 0{,}99$) @{wt.wc}; cea mai slabă medie pe 20 de pași @{wt.smin} față de @{wt.wmin}'),
    T(r'Both collapse at a break, because the least-squares fit is wrong for a while; the weighted threshold forgets the old scores and recovers within about 100 steps',
      r'Acoperirea ambelor metode scade brusc la o ruptură, pentru că estimarea prin cele mai mici pătrate rămîne greșită o perioadă; pragul ponderat uită scorurile vechi și își revine în aproximativ 100 de pași'),
    T(r'Price: mean width @{wt.ww} against @{wt.sw}; the guarantee is a bound in terms of $d_{\mathrm{TV}}$, not exact coverage', r'Costul: lățimea medie @{wt.ww} față de @{wt.sw}; garanția este o margine exprimată prin $d_{\mathrm{TV}}$, nu o acoperire exactă')])

D.frame(T('EnbPI: ensembles without data splitting', 'EnbPI: ansambluri fără împărțirea datelor'), items(
    (T(r'\refXX, \refXXb: fit $B$ models on $B$ bootstrap samples of the training period (blocks of consecutive observations, to respect dependence)',
       r'\refXX, \refXXb: se estimează $B$ modele pe $B$ eșantioane bootstrap ale perioadei de antrenare (blocuri de observații consecutive, pentru a respecta dependența)'),
     [T(r'leave-one-out residuals: for point $i$, aggregate only the models whose bootstrap sample excluded $i$', r'reziduuri leave-one-out: pentru punctul $i$ se agregă doar modelele al căror eșantion bootstrap l-a exclus pe $i$')]),
    (T(r'Interval at $t$: the ensemble forecast plus or minus a quantile of recent absolute residuals', r'Intervalul la $t$: prognoza ansamblului plus sau minus o cuantilă a reziduurilor absolute recente'),
     [r'\[ \hat C_t = \hat f(x_t) \pm Q_{1-\alpha}\big(|e_{t-W}|, \dots, |e_{t-1}|\big) \]',
      T(r'$\hat f(x_t)$: the aggregated forecast of the $B$ models given the predictors $x_t$; $e_s$: the residual of period $s$; $W$: the window length',
        r'$\hat f(x_t)$: prognoza agregată a celor $B$ modele, dați predictorii $x_t$; $e_s$: reziduul perioadei $s$; $W$: lungimea ferestrei'),
      T(r'after $y_t$ is observed, its residual enters the window and the oldest one leaves', r'după ce $y_t$ este observat, reziduul lui intră în fereastră, iar cel mai vechi iese')]),
    (T('No refitting at each step, no calibration split: efficient for long streams', 'Fără reestimare la fiecare pas, fără împărțire pentru calibrare: eficient pe fluxuri lungi'), []),
    T('Guarantee: asymptotic, conditional coverage if the errors are stationary and strongly mixing and the ensemble is consistent; designed for energy series (solar and wind)',
      'Garanția: acoperire asimptotică, condiționată, dacă erorile sînt staționare și puternic mixing, iar ansamblul este consistent; gîndit pentru serii de energie (solară și eoliană)')), 'small')

D.frame(T('Adaptive conformal inference (1/2)', 'Inferența conformală adaptivă (1/2)'), items(
    (T(r'\refGC: the nominal level is replaced by a working level $\alpha_t$ that is updated after every observation',
       r'\refGC: nivelul nominal este înlocuit cu un nivel de lucru $\alpha_t$, actualizat după fiecare observație'),
     [T(r'$q_t$: the conformal $(1 - \alpha_t)$ quantile of the recent scores; $\alpha$: the target miss rate (e.g.\ 0.1)', r'$q_t$: cuantila conformală $(1 - \alpha_t)$ a scorurilor recente; $\alpha$: rata-țintă a ratărilor (de exemplu 0,1)')]),
    (T(r'\textbf{Update}: after observing $Y_t$, move the working level against the last error', r'\textbf{Actualizarea}: după observarea lui $Y_t$, nivelul de lucru se mută în sens opus ultimei erori'),
     [r'\[ \alpha_{t+1} = \alpha_t + \gamma\,(\alpha - \mathrm{err}_t) \]',
      T(r'$\gamma > 0$: the step size; $\mathrm{err}_t \in \{0, 1\}$: the miss indicator of the previous slides', r'$\gamma > 0$: pasul; $\mathrm{err}_t \in \{0, 1\}$: indicatorul ratării de pe slide-urile anterioare')]),
    (T('Reading the update', 'Interpretarea actualizării'),
     [T(r'a miss ($\mathrm{err}_t = 1$) lowers $\alpha_t$ by $\gamma(1 - \alpha)$: the next set is wider', r'o ratare ($\mathrm{err}_t = 1$) scade $\alpha_t$ cu $\gamma(1 - \alpha)$: mulțimea următoare este mai largă'),
      T(r'a hit ($\mathrm{err}_t = 0$) raises $\alpha_t$ by $\gamma\alpha$: the next set is narrower', r'o acoperire ($\mathrm{err}_t = 0$) crește $\alpha_t$ cu $\gamma\alpha$: mulțimea următoare este mai îngustă'),
      T(r'$\alpha_t \le 0$ gives $q_t = +\infty$ (the whole real line); $\alpha_t \ge 1$ gives the empty set', r'$\alpha_t \le 0$ dă $q_t = +\infty$ (toată dreapta reală); $\alpha_t \ge 1$ dă mulțimea vidă')])), 'small')

D.frame(T('Adaptive conformal inference (2/2)', 'Inferența conformală adaptivă (2/2)'), items(
    (T(r'\textbf{Theorem} \refGC: for any sequence of data, the miss rate over $T$ periods is close to $\alpha$',
       r'\textbf{Teoremă} \refGC: pentru orice șir de date, frecvența ratărilor pe $T$ perioade este apropiată de $\alpha$'),
     [r'\[ \Big|\frac1T\sum_{t=1}^T\mathrm{err}_t - \alpha\Big| \le \frac{\max\{\alpha_1, 1 - \alpha_1\} + \gamma}{\gamma T} \]',
      T(r'$\alpha_1$: the starting level; the bound falls as $1/T$, and is tighter for a larger $\gamma$', r'$\alpha_1$: nivelul de pornire; marginea scade ca $1/T$ și este mai strînsă pentru un $\gamma$ mai mare')]),
    (T(r'Idea of the proof (Appendix) % applink: the two online guarantees', r'Ideea demonstrației (Anexă) % applink: cele două garanții online'),
     [T(r'$\alpha_t$ always stays in $[-\gamma, 1 + \gamma]$', r'$\alpha_t$ rămîne mereu în $[-\gamma, 1 + \gamma]$'),
      T(r'summing the updates, $\alpha_{T+1} - \alpha_1 = \gamma\sum_t(\alpha - \mathrm{err}_t)$; divide by $\gamma T$', r'însumînd actualizările, $\alpha_{T+1} - \alpha_1 = \gamma\sum_t(\alpha - \mathrm{err}_t)$; se împarte la $\gamma T$')]),
    (T('A long-run frequency, not conditional coverage', 'O frecvență pe termen lung, nu o acoperire condiționată'),
     [T('the guarantee holds even for an adversarially chosen sequence', 'garanția este valabilă și pentru un șir de date ales advers'),
      T(r'choosing $\gamma$ adaptively: AgACI \refZaf, DtACI \refGCb; ACI for VaR: Chapter 9', r'alegerea adaptivă a lui $\gamma$: AgACI \refZaf, DtACI \refGCb; ACI pentru VaR: Capitolul 9')])), 'small')

chart(T('ACI on stock-market volatility', 'ACI pe volatilitatea bursieră'), 'ats_ch13_aci', 'ATS_ch13_conformal_time', [
    T(r'Design of \refGC: the target is $V_t = r_t^2$, the squared daily return; $\hat\sigma_t^2$: its GARCH(1,1) forecast, fitted on the previous 1250 days',
      r'Designul din \refGC: ținta este $V_t = r_t^2$, randamentul zilnic la pătrat; $\hat\sigma_t^2$: prognoza ei dintr-un GARCH(1,1) estimat pe ultimele 1250 de zile'),
    T(r'Score $|V_t - \hat\sigma_t^2|/\hat\sigma_t^2$ (relative error of the variance forecast), $\alpha = 0.1$, $\gamma = 0.005$; local coverage over 500 days; evaluation from @{ac.sp.first}',
      r'Scorul $|V_t - \hat\sigma_t^2|/\hat\sigma_t^2$ (eroarea relativă a prognozei de varianță), $\alpha = 0{,}1$, $\gamma = 0{,}005$; acoperirea locală pe 500 de zile; evaluare din @{ac.sp.first}')],
    h='0.42\\textheight')

interp(('ACI on volatility', 'ACI pe volatilitate'), [
    (T('Three thresholds compared', 'Trei praguri comparate'),
     [T('static: split conformal calibrated once, on the first 1250 scores', 'static: split conformal calibrat o singură dată, pe primele 1250 de scoruri'),
      T('rolling: split conformal on the last 1250 scores, with the fixed level $\\alpha$', 'mobil: split conformal pe ultimele 1250 de scoruri, cu nivelul fix $\\alpha$'),
      T('ACI: the same rolling window, with the level $\\alpha_t$', 'ACI: aceeași fereastră mobilă, cu nivelul $\\alpha_t$')]),
    T(r'Overall coverage, S\&P 500: static @{ac.sp.st}, rolling @{ac.sp.ro}, ACI @{ac.sp.ac}; BET: @{ac.bet.st}, @{ac.bet.ro}, @{ac.bet.ac}; NVIDIA: @{ac.nv.st}, @{ac.nv.ro}, @{ac.nv.ac}',
      r'Acoperirea totală, S\&P 500: static @{ac.sp.st}, mobil @{ac.sp.ro}, ACI @{ac.sp.ac}; BET: @{ac.bet.st}, @{ac.bet.ro}, @{ac.bet.ac}; NVIDIA: @{ac.nv.st}, @{ac.nv.ro}, @{ac.nv.ac}'),
    T(r'Local coverage of the static method ranges from @{ac.sp.stmin} to @{ac.sp.stmax} (S\&P 500); ACI stays within @{ac.sp.acmin} -- @{ac.sp.acmax}',
      r'Acoperirea locală a metodei statice variază între @{ac.sp.stmin} și @{ac.sp.stmax} (S\&P 500); ACI rămîne între @{ac.sp.acmin} și @{ac.sp.acmax}'),
    (T(r'Christoffersen conditional coverage of the misses (S\&P 500): static $p$ @{ac.sp.stcc}, ACI $p$ @{ac.sp.accc}', r'Testul Christoffersen de acoperire condiționată a ratărilor (S\&P 500): static $p$ @{ac.sp.stcc}, ACI $p$ @{ac.sp.accc}'),
     [T('a calibration fixed on 2005--2009 is too wide afterwards', 'o calibrare fixată pe 2005--2009 este prea largă ulterior'),
      T('updating restores both the frequency and the independence of misses', 'actualizarea reface atît frecvența, cît și independența ratărilor')])])

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

D.frame(T('Conformal PID control (1/2)', 'Controlul PID conformal (1/2)'), items(
    (T(r'\refACT, \textbf{quantile tracking} (the P term): the threshold itself is updated after every observation',
       r'\refACT, \textbf{urmărirea cuantilei} (termenul P): pragul însuși este actualizat după fiecare observație'),
     [r'\[ q_{t+1} = q_t + \eta\,(\mathrm{err}_t - \alpha) \]',
      T(r'$\eta > 0$: the step size, in the units of the scores; a miss raises the threshold by $\eta(1 - \alpha)$, a hit lowers it by $\eta\alpha$',
        r'$\eta > 0$: pasul, în unitățile scorurilor; o ratare ridică pragul cu $\eta(1 - \alpha)$, o acoperire îl coboară cu $\eta\alpha$'),
      T('this is online gradient descent on the pinball loss of the score at level $1 - \\alpha$', 'este coborîrea pe gradient online pe pierderea pinball a scorului la nivelul $1 - \\alpha$')]),
    (T(r'\textbf{Proposition}: if the scores lie in $[0, B]$, the miss rate is close to $\alpha$ for any sequence',
       r'\textbf{Propoziție}: dacă scorurile sînt în $[0, B]$, frecvența ratărilor este apropiată de $\alpha$ pentru orice șir'),
     [r'\[ \Big|\frac1T\sum_{t=1}^T(\mathrm{err}_t - \alpha)\Big| \le \frac{B + \eta}{\eta T} \]',
      T(r'$B$: an upper bound of the scores; the threshold moves on the scale of the scores, not of $\alpha$ as in ACI', r'$B$: o margine superioară a scorurilor; pragul se mișcă pe scala scorurilor, nu pe cea a lui $\alpha$, ca la ACI')]),
    T('ACI is the special case that tracks the level instead of the quantile', 'ACI este cazul particular care urmărește nivelul în loc de cuantilă')), 'small')

D.frame(T('Conformal PID control (2/2)', 'Controlul PID conformal (2/2)'), items(
    (T(r'\textbf{Integrator} (the I term): adds a correction driven by the accumulated coverage error',
       r'\textbf{Integratorul} (termenul I): adaugă o corecție determinată de eroarea de acoperire acumulată'),
     [r'\[ r_t\Big(\sum_{i \le t}(\mathrm{err}_i - \alpha)\Big), \qquad r_t(x) = K_I\tan\big(x\log t/(tC_{\mathrm{sat}})\big) \]',
      T(r'$\sum_{i \le t}(\mathrm{err}_i - \alpha)$: misses in excess of the target, accumulated up to $t$', r'$\sum_{i \le t}(\mathrm{err}_i - \alpha)$: ratările peste țintă, acumulate pînă la $t$'),
      T(r'$K_I > 0$: the gain of the integrator; $C_{\mathrm{sat}} > 0$: the saturation constant; the $\tan$ grows without bound near its pole, which keeps the long-run guarantee',
        r'$K_I > 0$: cîștigul integratorului; $C_{\mathrm{sat}} > 0$: constanta de saturație; $\tan$ crește nemărginit lîngă polul său, ceea ce păstrează garanția pe termen lung')]),
    (T(r'\textbf{Scorecaster} (a D-like term): a model that forecasts the next score from its past and is added to the threshold',
       r'\textbf{Prognozatorul de scor} (un termen asemănător lui D): un model care prognozează scorul următor din trecutul lui și se adaugă la prag'),
     [T('it anticipates predictable patterns in the errors: seasonality, trends', 'anticipează tiparele previzibile ale erorilor: sezonalitate, tendințe')]),
    (T('The name comes from control theory', 'Denumirea vine din teoria controlului automat'),
     [T('proportional (react to the last error), integral (to the accumulated error), derivative (to the expected change)', 'proporțional (reacție la ultima eroare), integral (la eroarea acumulată), derivativ (la schimbarea anticipată)')])), 'small')

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
    (T(r'\textbf{Frequency and independence} of the misses (Chapter 9)', r'\textbf{Frecvența și independența} ratărilor (Capitolul 9)'),
     [T(r'miss rate and the Kupiec test \refKup (is the rate equal to $\alpha$?); Christoffersen test \refChr (are misses independent over time?)', r'frecvența ratărilor și testul Kupiec \refKup (este frecvența egală cu $\alpha$?); testul Christoffersen \refChr (sînt ratările independente în timp?)'),
      T(r'regression check in the spirit of the DQ test \refEM: regress $\mathrm{err}_t - \alpha$ on lagged misses and on the predicted width', r'o verificare prin regresie în spiritul testului DQ \refEM: regresia lui $\mathrm{err}_t - \alpha$ pe ratările cu lag și pe lățimea prognozată')]),
    (T('\\textbf{Local coverage}: the empirical counterpart of conditional coverage', '\\textbf{Acoperirea locală}: echivalentul empiric al acoperirii condiționate'),
     [T('coverage over rolling windows', 'acoperirea pe ferestre mobile'),
      T('coverage by classes of a variable known at the origin (predicted volatility, hour, regime)', 'acoperirea pe clase ale unei variabile cunoscute la origine (volatilitatea prognozată, ora, regimul)')]),
    (T(r'\textbf{Sharpness}: the mean width, and the \textbf{interval score} \refWin, \refGR, which adds a penalty for every miss',
       r'\textbf{Precizia} (sharpness): lățimea medie și \textbf{scorul de interval} \refWin, \refGR, care adaugă o penalizare pentru fiecare ratare'),
     [r'\[ \mathrm{IS} = (u - \ell) + \frac{2}{\alpha}(\ell - y)\mathbf 1\{y < \ell\} + \frac{2}{\alpha}(y - u)\mathbf 1\{y > u\} \]',
      T(r'$[\ell, u]$: the central $(1 - \alpha)$ interval; $u - \ell$: its width; $y$: the outcome; lower is better', r'$[\ell, u]$: intervalul central de $(1 - \alpha)$; $u - \ell$: lățimea lui; $y$: valoarea realizată; o valoare mai mică este mai bună'),
      T('a proper scoring rule: it rewards narrow intervals only if they keep the nominal coverage', 'o regulă de scor proprie: recompensează intervalele înguste doar dacă își păstrează acoperirea nominală')]),
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

D.frame(T('The need to calibrate foundation-model quantiles (1/2)', 'Nevoia de calibrare a cuantilelor foundation models (1/2)'), items(
    (T(r'Pretrained quantiles are calibrated on the corpus distribution, not on your series',
       r'Cuantilele preantrenate sînt calibrate pe distribuția corpusului, nu pe seria dumneavoastră'),
     [T('miscalibration is the default, in either direction (bands too narrow or too wide)', 'calibrarea greșită este situația implicită, în ambele sensuri (benzi prea înguste sau prea largi)')]),
    (T(r'Most models output only the 10\%--90\% quantiles', r'Majoritatea modelelor dau doar cuantilele de 10\%--90\%'),
     [T(r'a 95\% interval or a VaR 1\% requires extrapolation beyond the trained levels', r'un interval de 95\% sau un VaR 1\% cere extrapolare dincolo de nivelurile antrenate')]),
    (T(r'Procedure: online CQR on the model\'s own 10\%--90\% band',
       r'Procedura: CQR online pe banda proprie de 10\%--90\% a modelului'),
     [dm(r'S_t = \max\{\hat q_{0.1,t} - y_t,\; y_t - \hat q_{0.9,t}\}, \qquad \hat C_t = [\hat q_{0.1,t} - q_t,\; \hat q_{0.9,t} + q_t]'),
      T(r'$\hat q_{0.1,t}$, $\hat q_{0.9,t}$: the 10\% and 90\% quantiles forecast by the model for period $t$; $S_t$: the CQR score', r'$\hat q_{0.1,t}$, $\hat q_{0.9,t}$: cuantilele de 10\% și 90\% prognozate de model pentru perioada $t$; $S_t$: scorul CQR'),
      T(r'$q_t$: the threshold chosen by ACI for any target level (80\% or 95\%)', r'$q_t$: pragul ales de ACI pentru orice nivel-țintă (80\% sau 95\%)')])), 'small')

D.frame(T('The need to calibrate foundation-model quantiles (2/2)', 'Nevoia de calibrare a cuantilelor foundation models (2/2)'), items(
    (T(r'One-sided version for VaR', r'Varianta unilaterală pentru VaR'),
     [T(r'score $S_t = \hat q_{0.1,t} - y_t$; threshold $q_t$ tracked at level $\alpha$', r'scorul $S_t = \hat q_{0.1,t} - y_t$; pragul $q_t$ urmărit la nivelul $\alpha$'),
      T(r'the calibrated quantile is $\hat q_{0.1,t} - q_t$', r'cuantila calibrată este $\hat q_{0.1,t} - q_t$'),
      T(r'$\mathrm{VaR}_t = -(\hat q_{0.1,t} - q_t)$: VaR expressed as a positive loss', r'$\mathrm{VaR}_t = -(\hat q_{0.1,t} - q_t)$: VaR exprimat ca pierdere pozitivă')]),
    (T('What the shift changes', 'Ce schimbă deplasarea'),
     [T(r'$q_t > 0$ lowers the quantile (a larger VaR); $q_t < 0$ raises it', r'$q_t > 0$ coboară cuantila (un VaR mai mare); $q_t < 0$ o ridică'),
      T('the model itself is not re-estimated: only its output is recalibrated', 'modelul însuși nu este reestimat: doar ieșirea lui este recalibrată')]),
    (T('Further reading', 'Lectură suplimentară'),
     [T(r'conformal VaR recalibration of foundation models: \refCO; \refTV', r'recalibrarea conformală a VaR pentru foundation models: \refCO; \refTV')])), 'small')

chart(T('Raw and conformal coverage of foundation models', 'Acoperirea brută și cea conformală a foundation models'), 'ats_ch13_fm_calib', 'ATS_ch13_calibration', [
    T(r'Coverage of the raw 10--90\% band and of the online-CQR 80\% and 95\% intervals (ACI, window 250, $\gamma = 0.005$): Romanian load (24 hourly streams), Bitcoin log RV, EU inflation at $h = 1$ (27 streams), BET daily returns',
      r'Acoperirea benzii brute de 10--90\% și a intervalelor CQR online de 80\% și 95\% (ACI, fereastra 250, $\gamma = 0{,}005$): consumul României (24 de fluxuri orare), log RV Bitcoin, inflația UE la $h = 1$ (27 de fluxuri), randamentele zilnice BET')],
    h='0.48\\textheight')

interp(('the calibration', 'calibrării'), [
    T(r'Raw 80\% bands: load @{fc.l.lo}--@{fc.l.hi}\%, Bitcoin @{fc.b.lo}--@{fc.b.hi}\%, inflation @{fc.i.lo}--@{fc.i.hi}\%, BET returns @{fc.r.lo}--@{fc.r.hi}\% across the four models',
      r'Benzile brute de 80\%: consum @{fc.l.lo}--@{fc.l.hi}\%, Bitcoin @{fc.b.lo}--@{fc.b.hi}\%, inflație @{fc.i.lo}--@{fc.i.hi}\%, randamente BET @{fc.r.lo}--@{fc.r.hi}\% pentru cele patru modele'),
    T(r'After online CQR: 80\% intervals cover @{fc.c80lo}--@{fc.c80hi}\%, 95\% intervals @{fc.c95lo}--@{fc.c95hi}\% in every task',
      r'După CQR online: intervalele de 80\% acoperă @{fc.c80lo}--@{fc.c80hi}\%, cele de 95\% @{fc.c95lo}--@{fc.c95hi}\% în toate sarcinile'),
    (T(r'Raw bands are miscalibrated in both directions: too narrow (Chronos-2 on load), too wide (TimesFM on inflation)', r'Benzile brute sînt necalibrate în ambele sensuri: prea înguste (Chronos-2 la consum), prea largi (TimesFM la inflație)'),
     [T(r'the conformal step widens or narrows them: mean width between @{fc.wlo} and @{fc.whi} times the raw width', r'pasul conformal le lărgește sau le îngustează: lățimea medie este între @{fc.wlo} și @{fc.whi} ori lățimea brută'),
      T(r'and it reaches 95\% from models that output only deciles', r'și ajunge la 95\% pornind de la modele care produc doar decile')])])

chart(T('Value at Risk from foundation models', 'Valoarea la risc din foundation models'), 'ats_ch13_fm_var', 'ATS_ch13_calibration', [
    T(r'VaR 1\% exceedances, BET and S\&P 500 from @{fv.first} (@{fv.n} days): GARCH-$t$ (rolling 1000 days, Chapter 9), Chronos-2 raw and with ACI, deciles of the other models extended by a one-sided conformal shift',
      r'Depășirile VaR 1\%, BET și S\&P 500 din @{fv.first} (@{fv.n} zile): GARCH-$t$ (fereastră mobilă de 1000 de zile, Capitolul 9), Chronos-2 brut și cu ACI, decilele celorlalte modele extinse printr-o deplasare conformală unilaterală')],
    h='0.48\\textheight')

interp(('the VaR backtest', 'backtesting-ului VaR'), [
    T(r'BET, VaR 1\%: GARCH-$t$ @{fv.b.g}\% (Kupiec $p$ @{fv.b.gk}), Chronos-2 raw @{fv.b.c}\% ($p$ @{fv.b.ck}), Chronos-2 + ACI @{fv.b.a}\% ($p$ @{fv.b.ak}), TimesFM + conformal @{fv.b.t}\%',
      r'BET, VaR 1\%: GARCH-$t$ @{fv.b.g}\% (Kupiec $p$ @{fv.b.gk}), Chronos-2 brut @{fv.b.c}\% ($p$ @{fv.b.ck}), Chronos-2 + ACI @{fv.b.a}\% ($p$ @{fv.b.ak}), TimesFM + conformal @{fv.b.t}\%'),
    T(r'S\&P 500: GARCH-$t$ @{fv.s.g}\% (Kupiec $p$ @{fv.s.gk}), Chronos-2 raw @{fv.s.c}\% ($p$ @{fv.s.ck}), + ACI @{fv.s.a}\% ($p$ @{fv.s.ak}, Christoffersen $p$ @{fv.s.acc})',
      r'S\&P 500: GARCH-$t$ @{fv.s.g}\% (Kupiec $p$ @{fv.s.gk}), Chronos-2 brut @{fv.s.c}\% ($p$ @{fv.s.ck}), + ACI @{fv.s.a}\% ($p$ @{fv.s.ak}, $p$ Christoffersen @{fv.s.acc})'),
    (T(r'Calibration fixes the exceedance rate of every model, but it does not add information about the tail', r'Calibrarea corectează rata de depășire a oricărui model, dar nu adaugă informație despre coadă'),
     [T(r'the conformally extended deciles have a larger quantile loss than GARCH-$t$ (BET, Chronos-Bolt: DM $t = @{fv.b.bdm}$)', r'decilele extinse conformal au o pierdere cuantilică mai mare decît GARCH-$t$ (BET, Chronos-Bolt: DM $t = @{fv.b.bdm}$)'),
      T(r'Chronos-2, trained on 1\% quantiles, does not ($t = @{fv.b.adm}$)', r'Chronos-2, antrenat pe cuantile de 1\%, nu are o pierdere mai mare ($t = @{fv.b.adm}$)')])])

D.recap(('calibration', 'calibrarea'), [
    T('Treat foundation-model quantiles as scores to be calibrated, not as probabilities', 'Tratați cuantilele foundation models ca scoruri de calibrat, nu ca probabilități'),
    T('Online CQR with ACI gives target coverage at any level, including beyond the trained quantiles', 'CQR online cu ACI dă acoperirea-țintă la orice nivel, inclusiv dincolo de cuantilele antrenate'),
    T('Backtest calibrated VaR as in Chapter 9: frequency, independence and loss', 'Testați VaR calibrat ca în Capitolul 9: frecvență, independență și pierdere')])

# =============================================================================
# 9. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('The question', 'Întrebarea'),
     [T('do time-series foundation models beat domain-specific econometric models on Central and Eastern European data?', 'întrec foundation models pentru serii de timp modelele econometrice de domeniu pe datele din Europa Centrală și de Est?'),
      T('in a window after their release dates, and once multiplicity is accounted for', 'într-o fereastră de după lansarea lor și cu corecție pentru testarea multiplă')]),
    (T('A testable form', 'O formă testabilă'),
     [T(r'formal: $H_0$: equal expected loss (pooled over pre-registered series) of the best foundation model and the best domain model, in a window that starts after every model release',
        r'formal: $H_0$: pierderea așteptată egală (agregată pe serii preînregistrate) a celui mai bun foundation model și a celui mai bun model de domeniu, într-o fereastră care începe după lansarea tuturor modelelor'),
      T('falsified by a pooled DM test at 5\\% and an MCS that excludes one side, on series and horizons fixed before the data arrive',
        'infirmată de un test DM agregat la 5\\% și de un MCS care exclude una dintre părți, pe serii și orizonturi fixate înainte de sosirea datelor')]),
    (T('Why it matters', 'Miza'),
     [T('central banks and grid operators consider replacing tuned models by zero-shot ones', 'băncile centrale și operatorii de rețea iau în calcul înlocuirea modelelor ajustate cu modele zero-shot'),
      T('published wins often come from a favourable choice of series', 'cîștigurile publicate provin adesea dintr-o alegere favorabilă a seriilor'),
      T(r'literature to start from: \refAks, \refShc, \refMey, \refPE, \refBri', r'literatura de pornire: \refAks, \refShc, \refMey, \refPE, \refBri')])), 'small')

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
    T('Multiplicity: number of series, horizons and models tested; the pooled test and adjusted p-values reported', 'Multiplicitatea: numărul de serii, orizonturi și modele testate; raportarea testului agregat și a p-value-urilor ajustate')), 'small')

chart(T('Mini-case: how much can the choice of benchmark change the verdict?', 'Mini studiu de caz: cît poate schimba verdictul alegerea benchmark-ului?'), 'ats_ch13_ai_case', 'ATS_ch13_benchmark', [
    T(r'DM--HLN statistics of Chronos-2 against AR($p$) at $h = 12$ on @{ai.reps} random benchmarks of @{ai.k} EU countries and @{ai.y} years of origins, and on the full panel',
      r'Statisticile DM--HLN ale Chronos-2 față de AR($p$) la $h = 12$ pe @{ai.reps} de benchmark-uri aleatoare cu @{ai.k} țări UE și @{ai.y} ani de origini și pe întregul panel'),
    T(r'@{ai.win}\% of the random benchmarks declare Chronos-2 significantly better and @{ai.lose}\% significantly worse; the full panel gives $t = @{ai.t}$ ($p$ @{ai.p})',
      r'@{ai.win}\% dintre benchmark-urile aleatoare declară Chronos-2 semnificativ mai bun, iar @{ai.lose}\% semnificativ mai slab; panelul întreg dă $t = @{ai.t}$ ($p$ @{ai.p})'),
    T('An AI summary that presents one such paper as evidence for (or against) foundation models is wrong; only the pre-registered panel answers the question',
      'Un rezumat AI care prezintă o astfel de lucrare ca dovadă pentru (sau împotriva) foundation models greșește; doar panelul preînregistrat răspunde la întrebare')],
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
