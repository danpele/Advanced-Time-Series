r"""
build_chapter10.py -- Capitolul 10 (Memorie lungă și rough volatility), EN + RO
================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_10/ch10_numbers.json (generate_all_charts.py). Nicio cifră nu este
scrisă de mînă, în afara exemplelor teoretice.
TSA, Capitolul 8 a predat ARFIMA, R/S, DFA, GPH, local Whittle, FIGARCH și HAR pe scurt și memoria lungă aparentă;
aici: caracterizarea spectrală, teoria asimptotică a estimatorilor semiparametrici și alegerea lățimii de bandă, testul
Qu (2011), cointegrarea fracționară (FCVAR), memoria lungă a volatilității (FIGARCH, HYGARCH, LMSV, HAR ca aproximare),
rough volatility (fBm, simulare, Gatheral, Jaisson și Rosenbaum 2018, critici) și prognoza volatilității realizate.
Ieșire:
  EN/Courses/chapter10_long_memory_rough_volatility.tex
  RO/Cursuri/capitol10_memorie_lunga_rough_volatility.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_10/generate_all_charts.py
  python3 latex/build_chapter10.py && python3 latex/ats_build.py compile 10
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch10_common import REFS, QLURL, T, V2, day, month, bib, finalize, load, minus_fix   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(10, 'lecture', refs=REFS)
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
    'hurst': ('ch10_hurst_1953.jpg', C + 'Harold_Edwin_Hurst_in_1953.jpg', FOTO + ': Elliott \\& Fry (1953); ' + PD + '; Wikimedia Commons'),
    'nilo': ('ch10_nilometer_2009.jpg', C + 'Nilometer._Roda_Innen.JPG', FOTO + ': Willyman (2009); CC BY-SA 4.0; Wikimedia Commons'),
    'aswan': ('ch10_aswan_low_dam_2010.jpg', C + 'Aswan_Low_Dam_Egypt_1.jpg', FOTO + ': Karelj (2010); ' + PD + '; Wikimedia Commons'),
    'mandel': ('ch10_mandelbrot_2010.jpg', C + 'Benoit_Mandelbrot,_TED_2010_(3x4_cropped).jpg', FOTO + ': Steve Jurvetson (2010); CC BY 2.0; Wikimedia Commons'),
    'kolmo': ('ch10_kolmogorov.jpg', C + 'Andrej_Nikolajewitsch_Kolmogorov.jpg', FOTO + ': Konrad Jacobs; CC BY-SA 2.0 de; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


def pv(key, x, d=3):
    if x < 10 ** (-d):
        V.raw(key, '$<$' + n(10 ** (-d), d))
    else:
        P(key, x, d)


# =============================================================================
# CIFRE
# =============================================================================
o = N['overview']
V.int('ov.n', o['n'])
V.int('ov.nb', o['nb'])
V.raw('ov.end', day(o['end']))
V.raw('ov.bend', day(o['bend']))
for k in ('acf1', 'acf22', 'acf250', 'acf500', 'd_acf'):
    P('ov.' + k, o[k], 2)
P('ov.slope', o['slope'], 2)
ad = N['assets_d']
P('ov.dlw', ad['sp500']['rv'], 2)
a = N['acf_spec']['0.4']
P('ac.r1', a['r1'], 3)
P('ac.r10', a['r10'], 3)
P('ac.r100', a['r100'], 3)
P('ac.sum100', a['sum100'], 1)
P('ac.sum200', a['sum200'], 1)
V.raw('ac.ar100', str(int(round(-__import__('math').log10(a['ar100'])))))
P('ac2.r100', N['acf_spec']['0.2']['r100'], 3)
g = N['aggregation']
P('ag.d0', g['d0'], 1)
for k in ('1', '10', '100', '3000'):
    P(f'ag.m{k}', g['med'][k], 2)
P('ag.lo', g['lo']['3000'], 2)
P('ag.hi', g['hi']['3000'], 2)
V.raw('ag.m', str(g['m']))
V.raw('ag.reps', str(g['reps']))
mc = N['mc']
V.raw('mc.m', str(mc['m']))
V.raw('mc.reps', str(mc['reps']))
P('mc.seg', mc['se_gph'], 3)
P('mc.sel', mc['se_lw'], 3)
for dd, kk in (('0.3', 's'), ('1.2', 'n')):
    for e in ('GPH', 'LW', 'ELW'):
        r = mc[dd][e]
        P(f'mc.{kk}.{e}.m', r['mean'], 3)
        P(f'mc.{kk}.{e}.s', r['sd'], 3)
        P(f'mc.{kk}.{e}.c', 100 * r['cover'], 0)
b = N['bandwidth']
P('bw.C', b['C'], 1)
P('bw.mopt', b['mopt'], 0)
P('bw.aopt', b['aopt'], 2)
V.raw('bw.bestm', str(b['best_m']))
P('bw.besta', b['best_a'], 2)
P('bw.b80', b['bias'][-1], 2)
P('bw.r80', b['rmse'][-1], 2)
P('bw.rmin', min(b['rmse']), 3)
P('bw.b40', b['bias'][0], 3)
P('bw.r40', b['rmse'][0], 2)
P('bw.th80', b['th_bias'][-1], 2)
q = N['qu']
for e, kk in (('0.02', 'a'), ('0.05', 'b')):
    for p_ in ('0.9', '0.95', '0.99'):
        P(f'qu.{kk}.{p_[2:]}', q['crit'][e][p_], 2)
QN = list(q['rej'])
for i, k in enumerate(QN):
    P(f'qu.r{i}', 100 * q['rej'][k], 0)
    P(f'qu.d{i}', q['dbar'][k], 2)
P('qu.W', q['W_spx'], 2)
P('qu.slo', min(q['spx']), 2)
P('qu.shi', max(q['spx']), 2)
V.raw('qu.m', str(q['m']))
V.raw('qu.reps', str(q['reps']))
P('qu.l0', q['curves'][QN[2]][0], 2)
P('qu.l1', q['curves'][QN[2]][-1], 2)
fi = N['inflation']
for c_ in ('us', 'ro'):
    for s_ in ('full', 'post'):
        r = fi[c_][s_]
        P(f'in.{c_}.{s_}.d', r['d'], 2)
        P(f'in.{c_}.{s_}.lw', r['lw'], 2)
        P(f'in.{c_}.{s_}.se', r['se'], 2)
        P(f'in.{c_}.{s_}.W', r['W'], 2)
        V.raw(f'in.{c_}.{s_}.n', str(r['n']))
    V.raw(f'in.{c_}.end', month(fi[c_]['full']['end']))
for p_ in ('0.9', '0.95', '0.99'):
    P(f'in.c.{p_[2:]}', fi['crit'][p_], 2)
P('in.ro.lo', min(fi['ro']['post']['curve']), 2)
P('in.ro.hi', max(fi['ro']['post']['curve']), 2)
f = N['fcvar']
V.int('fc.n', f['n'])
V.raw('fc.end', day(f['end']))
for k in ('d', 'b', 'beta2', 'd_rv', 'd_iv', 'd_spread', 'se', 'nbls', 'trace0', 'trace1', 'd0'):
    P(f'fc.{k}', f[k], 2)
P('fc.a1', f['alpha'][0], 2)
P('fc.a2', f['alpha'][1], 3)
pv('fc.p0', f['p0'])
pv('fc.p1', f['p1'])
P('fc.ib', 1 / f['beta2'], 2)
fg = N['figarch']
for nm in ('sp500', 'bet', 'btc'):
    r = fg[nm]
    P(f'fg.{nm}.ga', r['garch']['par'][1], 3)
    P(f'fg.{nm}.gb', r['garch']['par'][2], 3)
    P(f'fg.{nm}.d', r['figarch']['par'][1], 2)
    P(f'fg.{nm}.phi', r['figarch']['par'][2], 2)
    P(f'fg.{nm}.beta', r['figarch']['par'][3], 2)
    P(f'fg.{nm}.nu', r['figarch']['par'][4], 1)
    P(f'fg.{nm}.amp', r['hygarch']['par'][4], 2)
    P(f'fg.{nm}.lr1', r['lr_fig_garch'], 1)
    P(f'fg.{nm}.lr2', r['lr_hy_fig'], 2)
    P(f'fg.{nm}.bg', r['garch']['bic'], 0)
    P(f'fg.{nm}.bf', r['figarch']['bic'], 0)
    P(f'fg.{nm}.bh', r['hygarch']['bic'], 0)
    P(f'fg.{nm}.w22f', 100 * r['figarch']['w22'], 0)
    P(f'fg.{nm}.w250f', 100 * r['figarch']['w250'], 1)
    P(f'fg.{nm}.w22g', 100 * r['garch']['w22'], 0)
    V.int(f'fg.{nm}.n', r['n'])
for nm in ('sp500', 'dax', 'bet', 'eurron', 'btc'):
    r = ad[nm]
    for k in ('abs', 'lsq', 'lwn', 'qu'):
        P(f'ad.{nm}.{k}', r[k], 2)
    if 'rv' in r:
        P(f'ad.{nm}.rv', r['rv'], 2)
for p_ in ('0.9', '0.95', '0.99'):
    P(f'ad.c.{p_[2:]}', ad['crit'][p_], 2)
h = N['har']
for i, k in enumerate(('b0', 'bd', 'bw', 'bm')):
    P(f'har.{k}', h['b'][i], 2)
P('har.d', h['d'], 2)
P('har.pers', h['persistence'], 3)
for k in ('k100', 'k250', 'k500'):
    P(f'har.s.{k}', h['acf_s'][k], 2)
    P(f'har.h.{k}', h['acf_h'][k], 3)
V.raw('har.half', str(h['half_lag']))
fb = N['fbm']
for H_ in ('0.1', '0.3', '0.7'):
    P(f'fb.{H_[2:]}', fb[H_]['rho1'], 3)
hy = N['hybrid']
P('hy.r05', hy['riemann'][0], 2)
P('hy.r1', hy['riemann'][1], 2)
P('hy.h05', hy['hybrid'][0], 2)
P('hy.h1', hy['hybrid'][1], 2)
V.raw('hy.n', str(hy['n']))
V.int('hy.paths', hy['paths'])
gj = N['gjr']
for i, z in enumerate(gj['zeta']):
    P(f'gj.z{i}', z, 3)
P('gj.H', gj['H'], 3)
P('gj.H2', gj['H2'], 3)
P('gj.nu', gj['nu'], 2)
P('gj.s1', gj['sub']['2000-2010'], 3)
P('gj.s2', gj['sub']['2011-2022'], 3)
P('gj.c', gj['c'], 3)
P('gj.dH', gj['H'] + 0.5, 2)
ga = N['gjr_assets']
GA = {'.SPX': 'spx', '.GDAXI': 'dax', '.FTSE': 'ftse', '.N225': 'nik', '.STOXX50E': 'sx', '.FCHI': 'cac', 'btc': 'btc'}
for k, kk in GA.items():
    r = ga[k]
    P(f'ga.{kk}.H', r['H'], 3)    # three decimals, as in Seminar 10 (B3, B4)
    P(f'ga.{kk}.Hn', r['Hn'], 3)
    P(f'ga.{kk}.d', r['d'], 2)
    if 'Hp' in r:
        P(f'ga.{kk}.Hp', r['Hp'], 2)
        P(f'ga.{kk}.Hpn', r['Hpn'], 2)
        P(f'ga.{kk}.sh', 100 * r['sharep'], 0)
Hs_ = [ga[k]['H'] for k in GA]
P('ga.min', min(Hs_), 3)
P('ga.max', max(Hs_), 3)
P('ga.ftsesh', 100 * ga['.FTSE']['share'], 0)
nz = N['noise']
for H_ in ('0.1', '0.3', '0.5'):
    for k in ('iv', 'rv', 'rvn'):
        P(f'nz.{H_[2:]}.{k}', nz[H_][k]['mean'], 2)
V.int('nz.days', nz['design']['n_days'])
V.raw('nz.reps', str(nz['design']['reps']))
dc = N['decouple']
P('dc.H', dc['H_short'], 2)
P('dc.2H', 2 * dc['H_short'], 2)
P('dc.sl', dc['slope_long'], 2)
P('dc.dl', dc['d_long'], 2)
P('dc.dacf', dc['d_acf'], 2)
P('dc.dlw', dc['d_lw'], 2)
V.raw('dc.mlw', str(dc['m_lw']))
kr = N['kernel']
P('kr.H', kr['H'], 2)
P('kr.1.w1', 100 * kr['1']['w1'], 0)
P('kr.1.w5', 100 * kr['1']['w5'], 0)
P('kr.1.w22', 100 * kr['1']['w22'], 0)
P('kr.22.w1', 100 * kr['22']['w1'], 0)
P('kr.22.w22', 100 * kr['22']['w22'], 0)
P('kr.22.w100', 100 * kr['22']['w100'], 0)
P('kr.har.w1', 100 * kr['har']['w1'], 0)
P('kr.har.w5', 100 * kr['har']['w5'], 0)
fcst = N['forecast']
FK = {'.SPX': 'spx', '.GDAXI': 'dax', 'btc': 'btc'}
for k, kk in FK.items():
    r = fcst[k]
    V.int(f'fo.{kk}.T', r['T'])
    V.raw(f'fo.{kk}.start', day(r['start']))
    V.raw(f'fo.{kk}.end', day(r['end']))
    P(f'fo.{kk}.Hm', r['H_med'], 2)
    P(f'fo.{kk}.Hlo', r['H_min'], 2)
    P(f'fo.{kk}.Hhi', r['H_max'], 2)
    for hh in ('1', '5', '22'):
        e = r['eval'][hh]
        for m_ in ('arf', 'rfsv'):
            P(f'fo.{kk}.{hh}.{m_}', e[m_]['rel_q'], 3)
            P(f'fo.{kk}.{hh}.{m_}.t', e[m_]['dm_q'][0], 2)
            pv(f'fo.{kk}.{hh}.{m_}.p', e[m_]['dm_q'][1], 2)
            P(f'fo.{kk}.{hh}.{m_}.mt', e[m_]['dm_m'][0], 2)
        P(f'fo.{kk}.{hh}.har', e['har']['qlike'], 3)
rels = [abs(1 - fcst[k]['eval'][hh]['arf']['rel_q']) for k in FK for hh in ('1', '5', '22')]
P('fo.arfdev', 100 * max(rels), 1)
nsig = sum(fcst[k]['eval'][hh][m_]['dm_q'][1] < 0.05 for k in FK for hh in ('1', '5', '22') for m_ in ('arf', 'rfsv'))
V.raw('fo.nsig', V2(['none', 'one', 'two', 'three'][nsig] if nsig < 4 else str(nsig), ['niciuna', 'una', 'două', 'trei'][nsig] if nsig < 4 else str(nsig)))
gains = [100 * (1 - fcst[k]['eval'][hh]['rfsv']['rel_q']) for k in ('.SPX', '.GDAXI') for hh in ('5', '22')]
P('fo.glo', min(gains), 1)
P('fo.ghi', max(gains), 1)
ai = N['ai']
V.raw('ai.n', str(ai['n']))
V.raw('ai.cells', str(ai['n_cells']))
for k in ('H_min', 'H_max', 'H_med', 'H_med_mom', 'H_med_int', 'd_min', 'd_max', 'd_med', 'corr'):
    P('ai.' + k.replace('_', ''), ai[k], 2)
P('ai.sh', 100 * ai['share02'], 0)
minus_fix(V)

TB = '>{\\raggedright\\arraybackslash}'

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: how slowly do shocks to volatility and inflation die out, how rough is volatility at short horizons, and how do we tell genuine long memory from breaks and from measurement error?',
       r'\textbf{Întrebarea}: cît de încet se sting șocurile asupra volatilității și inflației, cît de neregulată (rough) este volatilitatea pe orizonturi scurte și cum deosebim memoria lungă reală de rupturi și de erorile de măsurare?'),
     [T('two scales of the same object: the persistence of log volatility over months, its roughness over days',
        'două scări ale aceluiași obiect: persistența logaritmului volatilității pe luni și neregularitatea lui pe zile')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('spectral characterisation and fractional processes; asymptotics of GPH, local Whittle and exact local Whittle; bandwidth and bias',
        'caracterizarea spectrală și procesele fracționare; asimptotica estimatorilor GPH, local Whittle și local Whittle exact; lățimea de bandă și deplasarea'),
      T('testing long memory against level shifts (Qu 2011); fractional cointegration (FCVAR)', 'testarea memoriei lungi împotriva salturilor de nivel (Qu 2011); cointegrarea fracționară (FCVAR)'),
      T('long memory in volatility: FIGARCH, HYGARCH, LMSV, HAR as an approximation', 'memoria lungă a volatilității: FIGARCH, HYGARCH, LMSV, HAR ca aproximare'),
      T('rough volatility: fBm, simulation, the evidence of Gatheral, Jaisson and Rosenbaum, critiques, forecasting', 'rough volatility: fBm, simulare, evidența lui Gatheral, Jaisson și Rosenbaum, critici, prognoză')]),
    T('We build on TSA, Chapter 8 (ARFIMA, R/S, GPH), Chapter 1 (forecast evaluation), Chapter 2 (breaks) and Chapter 8 (realised measures, HAR); Seminar 10 comes before this lecture',
      'Pornim de la TSA, Capitolul 8 (ARFIMA, R/S, GPH), Capitolul 1 (evaluarea prognozelor), Capitolul 2 (rupturi) și Capitolul 8 (măsuri realizate, HAR); Seminarul 10 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Characterise long memory in the time and frequency domains and derive the autocorrelations and spectrum of ARFIMA processes',
      'Caracterizați memoria lungă în domeniul timpului și al frecvenței și deduceți autocorelațiile și spectrul proceselor ARFIMA'),
    T('State the asymptotic theory of GPH, local Whittle and exact local Whittle, and choose the bandwidth from the bias--variance trade-off',
      'Enunțați teoria asimptotică a estimatorilor GPH, local Whittle și local Whittle exact și alegeți lățimea de bandă din compromisul deplasare--varianță'),
    T('Test long memory against short memory with level shifts (Qu 2011) and estimate a fractionally cointegrated VAR',
      'Testați memoria lungă față de memoria scurtă cu salturi de nivel (Qu 2011) și estimați un VAR cointegrat fracționar'),
    T('Estimate FIGARCH and HYGARCH models, and long memory in volatility robust to measurement noise',
      'Estimați modele FIGARCH și HYGARCH, precum și memoria lungă a volatilității robust la zgomotul de măsurare'),
    T('Simulate fractional Brownian motion, replicate the roughness evidence on realised variance, and evaluate rough-volatility forecasts honestly out of sample',
      'Simulați mișcarea browniană fracționară, replicați evidența neregularității pe varianța realizată și evaluați riguros, în afara eșantionului, prognozele de rough volatility')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Long memory: \refGJ; \refHos; \refRobC; \refSP; \refBFGK', r'Memorie lungă: \refGJ; \refHos; \refRobC; \refSP; \refBFGK'),
     [T(r'Breaks and co-memory: \refQu; \refPQ; \refJN', r'Rupturi și memorie comună: \refQu; \refPQ; \refJN'),
      T(r'Volatility: \refBBM; \refCor; \refGJR; \refBLPb', r'Volatilitate: \refBBM; \refCor; \refGJR; \refBLPb')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_10}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_10}'),
     [T(r'periodogram estimators, the Qu test, FCVAR, FIGARCH, circulant embedding, the hybrid scheme and the RFSV predictor written in \texttt{numpy}/\texttt{scipy}',
        r'estimatorii pe periodogramă, testul Qu, FCVAR, FIGARCH, scufundarea circulantă, schema hibridă și predictorul RFSV scrise în \texttt{numpy}/\texttt{scipy}')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter10_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter10_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{3.2cm}' + TB + 'p{5.4cm}' + TB + 'p{3.6cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source, sample}', r'\textbf{Sursa, eșantionul}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizarea}'),
    [T('Realised variance of six equity indices', 'Varianța realizată a șase indici bursieri') + r' & \refOMI: ' + T('5-minute RV, January 2000 -- February 2022 (end of the library)', 'RV din randamente de 5 minute, ianuarie 2000 -- februarie 2022 (sfîrșitul bibliotecii)') + ' & ' + T('memory, roughness, forecasts', 'memorie, neregularitate, prognoze'),
     T('Bitcoin realised variance', 'Varianța realizată a Bitcoin') + ' & ' + T('Binance one-minute prices (public data), our measures, January 2018 -- September 2026', 'prețuri Binance la un minut (date publice), măsurile noastre, ianuarie 2018 -- septembrie 2026') + ' & ' + T('roughness, forecasts', 'neregularitate, prognoze'),
     'S\\&P 500, DAX, BET, Bitcoin, VIX & ' + T('EODHD daily OHLC and closes, 2000 -- September 2026', 'EODHD, prețuri zilnice OHLC și de închidere, 2000 -- septembrie 2026') + ' & ' + T('FIGARCH, $|r|$, ranges, FCVAR', 'FIGARCH, $|r|$, amplitudini, FCVAR'),
     'EUR/RON & ' + T('BNR reference rate, July 2005 -- September 2026', 'cursul de referință BNR, iulie 2005 -- septembrie 2026') + ' & ' + T('memory of $|r|$', 'memoria lui $|r|$'),
     T('Inflation', 'Inflația') + ' & ' + T('US CPI (FRED CPIAUCSL), Romanian HICP (Eurostat prc\\_hicp\\_minr), monthly', 'IPC SUA (FRED CPIAUCSL), IAPC România (Eurostat prc\\_hicp\\_minr), lunar') + ' & ' + T('persistence and breaks', 'persistență și rupturi')],
    size='scriptsize') + items(
    T('Where no intraday data exist (BET, EUR/RON) volatility is proxied by $|r_t|$ and $\\log r_t^2$; the Parkinson range is used to show how a noisier proxy distorts roughness',
      'Acolo unde nu există date intraday (BET, EUR/RON), volatilitatea este aproximată prin $|r_t|$ și $\\log r_t^2$; amplitudinea Parkinson arată cum un proxy mai zgomotos distorsionează neregularitatea')), 'footnotesize')

D.frame(T('From the Nile to long memory', 'De la Nil la memoria lungă'), two(
    ph('hurst', T('Harold Edwin Hurst, 1953', 'Harold Edwin Hurst, 1953'), h='0.42\\textheight'),
    items(T(r'Hurst studied centuries of Nile levels to size the reservoirs above Aswan \refHur', r'Hurst a studiat secole de niveluri ale Nilului pentru a dimensiona rezervoarele de deasupra Aswanului \refHur'),
          T(r'The adjusted range of cumulated inflows grew like $n^H$ with $H \approx 0.7$, not $n^{1/2}$: the \textbf{Hurst effect}', r'Amplitudinea ajustată a afluxurilor cumulate creștea ca $n^H$ cu $H \approx 0{,}7$, nu ca $n^{1/2}$: \textbf{efectul Hurst}'),
          T('Wet years follow wet years in long runs: dependence that no finite ARMA reproduces', 'Anii ploioși urmează anilor ploioși în serii lungi: o dependență pe care niciun ARMA finit nu o reproduce'),
          (T('Two explanations followed', 'Au urmat două explicații'),
           [T(r'fractional Gaussian noise \refMVN', r'zgomotul gaussian fracționar \refMVN'),
            T(r'fractional differencing \refGJ, \refHos', r'diferențierea fracționară \refGJ, \refHos')])), '0.36', '0.62'), 'small')

D.frame(T('Records of the river', 'Înregistrările fluviului'), two(
    ph('nilo', T('The Nilometer on Roda Island, Cairo', 'Nilometrul de pe insula Roda, Cairo'), h='0.5\\textheight'),
    items(T('The Roda Nilometer recorded annual Nile minima from the seventh century on: one of the oldest time series', 'Nilometrul de pe Roda a înregistrat minimele anuale ale Nilului începînd cu secolul al VII-lea: una dintre cele mai vechi serii de timp'),
          T(r'These minima are the classic long-memory data set \refBFGK', r'Aceste minime sînt setul clasic de date cu memorie lungă \refBFGK'),
          T('Today the same question is asked of volatility, inflation and interest rates: does a shock fade geometrically or hyperbolically?', 'Azi aceeași întrebare se pune pentru volatilitate, inflație și dobînzi: se stinge un șoc geometric sau hiperbolic?'),
          T('And a newer one: at short horizons, is volatility smoother or rougher than Brownian motion?', 'Și una mai nouă: pe orizonturi scurte, este volatilitatea mai netedă sau mai neregulată decît mișcarea browniană?')), '0.34', '0.64'), 'small')

chart(T('Twenty-two years of log realised variance', 'Douăzeci și doi de ani de logaritm al varianței realizate'), 'ats_ch10_overview', 'ATS_ch10_memory', [
    T(r'Left: S\&P 500 (Oxford-Man, $n = @{ov.n}$ days to @{ov.end}) and Bitcoin ($n = @{ov.nb}$ days to @{ov.bend}); right: sample ACF of S\&P 500 log RV, lags 1--500, log-log',
      r'Stînga: S\&P 500 (Oxford-Man, $n = @{ov.n}$ zile pînă la @{ov.end}) și Bitcoin ($n = @{ov.nb}$ zile pînă la @{ov.bend}); dreapta: ACF de eșantion a logaritmului RV pentru S\&P 500, laguri 1--500, scară log-log')], h='0.53\\textheight')

interp(('the long view', 'imaginii de ansamblu'), [
    T(r'ACF @{ov.acf1} at lag 1, @{ov.acf22} at lag 22, still @{ov.acf250} at lag 250: an AR(1) with the same first lag would give about $10^{-22}$ at lag 250', r'ACF @{ov.acf1} la lagul 1, @{ov.acf22} la 22, încă @{ov.acf250} la 250: un AR(1) cu același prim lag ar da circa $10^{-22}$ la lagul 250'),
    T(r'On lags 5--200 the ACF is a straight line in log-log, slope @{ov.slope}: hyperbolic decay $k^{2d-1}$ with $d \approx @{ov.d_acf}$', r'Pe lagurile 5--200, ACF este o dreaptă în scara log-log, cu panta @{ov.slope}: o descreștere hiperbolică $k^{2d-1}$ cu $d \approx @{ov.d_acf}$'),
    T(r'The local Whittle estimate is larger, @{ov.dlw}: the sample ACF is biased down at long lags under long memory', r'Estimația local Whittle este mai mare, @{ov.dlw}: sub memorie lungă, ACF de eșantion este deplasată în jos la laguri mari'),
    T('The rest of the chapter asks which of these numbers to trust, and why the same series also looks rough', 'Restul capitolului întreabă în care dintre aceste cifre putem avea încredere și de ce aceeași serie pare și neregulată')])

# =============================================================================
# 1. MEMORIA LUNGĂ: CARACTERIZARE SPECTRALĂ
# =============================================================================
D.section('Long memory: spectral characterisation', 'Memoria lungă: caracterizare spectrală')

D.frame(T('Known from TSA, and new here', 'Cunoscut din TSA și elemente noi'), items(
    (T('Known (TSA, Chapter 8): fractional differencing, ARFIMA$(p,d,q)$, R/S and DFA, GPH and local Whittle as recipes, FIGARCH and HAR in brief, spurious long memory by example', 'Cunoscut (TSA, Capitolul 8): diferențierea fracționară, ARFIMA$(p,d,q)$, R/S și DFA, GPH și local Whittle ca rețete, FIGARCH și HAR pe scurt, memoria lungă aparentă prin exemple'), []),
    (T('New: the theory behind the recipes', 'Nou: teoria din spatele rețetelor'),
     [T('equivalent definitions, aggregation, the variance of the sample mean', 'definiții echivalente, agregare, varianța mediei de eșantion'),
      T('limit laws of the semiparametric estimators, non-stationary $d$, bias and the choice of $m$', 'legile limită ale estimatorilor semiparametrici, $d$ nestaționar, deplasarea și alegerea lui $m$'),
      T('a formal test against level shifts; fractional cointegration; rough volatility', 'un test formal împotriva salturilor de nivel; cointegrarea fracționară; rough volatility')]),
    T('Replications: Granger (1980) aggregation, Qu (2011) design, Gatheral, Jaisson and Rosenbaum (2018, Section 2) scaling on the Oxford-Man data they used',
      'Replicări: agregarea Granger (1980), schema Qu (2011), scalarea Gatheral, Jaisson și Rosenbaum (2018, secțiunea 2) pe datele Oxford-Man folosite de ei')), 'small')

D.frame(T('Two definitions of long memory (1/2)', 'Două definiții ale memoriei lungi (1/2)'), items(
    (T(r'\textbf{Time domain}: the autocovariances decay hyperbolically and are not summable', r'\textbf{Domeniul timpului}: autocovarianțele scad hiperbolic și nu sînt sumabile'
       ) + r'''
    \[ \gamma(k) \sim c_\gamma\,k^{2d-1} \ \ (k \to \infty), \quad 0 < d < 1/2 \ \Rightarrow\ \sum_k|\gamma(k)| = \infty \]''',
     [T(r'$\gamma(k)$: autocovariance at lag $k$; $d$: memory parameter; $c_\gamma > 0$: a constant; $a_k \sim b_k$ means $a_k/b_k \to 1$',
        r'$\gamma(k)$: autocovarianța la lagul $k$; $d$: parametrul de memorie; $c_\gamma > 0$: o constantă; $a_k \sim b_k$ înseamnă $a_k/b_k \to 1$'),
      T(r'short memory: $\sum_k|\gamma(k)| < \infty$ (e.g.\ ARMA, with geometric decay)', r'memorie scurtă: $\sum_k|\gamma(k)| < \infty$ (de exemplu ARMA, cu descreștere geometrică)')]),
    (T(r'\textbf{Frequency domain}: the spectral density has a pole at frequency zero', r'\textbf{Domeniul frecvenței}: densitatea spectrală are un pol în frecvența zero'
       ) + r'''
    \[ f(\lambda) \sim c_f\,\lambda^{-2d} \quad (\lambda \to 0^+) \]''',
     [T(r'$f(\lambda)$: spectral density at frequency $\lambda \in (0, \pi]$; $c_f > 0$: a constant',
        r'$f(\lambda)$: densitatea spectrală la frecvența $\lambda \in (0, \pi]$; $c_f > 0$: o constantă'),
      T(r'$d < 0$: antipersistence, $f(0) = 0$, $\sum_k\gamma(k) = 0$; $d = 0$: short memory', r'$d < 0$: antipersistență, $f(0) = 0$, $\sum_k\gamma(k) = 0$; $d = 0$: memorie scurtă')])), 'small')

D.frame(T('Two definitions of long memory (2/2)', 'Două definiții ale memoriei lungi (2/2)'), items(
    (T(r'Equivalence: for quasi-monotone $\gamma$ the constants are linked (Abelian--Tauberian theorems) \refBFGK', r'Echivalența: pentru $\gamma$ cvasi-monotonă, constantele sînt legate (teoreme abeliene--tauberiene) \refBFGK'
       ) + r'''
    \[ c_f = c_\gamma\,\Gamma(2d)\,\frac{\sin(\pi/2 - \pi d)}{\pi} \]''',
     [T(r'$\Gamma(\cdot)$: the gamma function; without such regularity the two definitions differ', r'$\Gamma(\cdot)$: funcția gamma; fără această regularitate, cele două definiții diferă'),
      T('semiparametric estimators use only the frequency-domain definition', 'estimatorii semiparametrici folosesc doar definiția din domeniul frecvenței')]),
    (T(r'Hurst scale: $H = d + 1/2$ for the stationary series', r'Scara Hurst: $H = d + 1/2$ pentru seria staționară'),
     [T(r'$H > 1/2$: persistent; $H < 1/2$: antipersistent; $H = 1/2$: short memory', r'$H > 1/2$: persistentă; $H < 1/2$: antipersistentă; $H = 1/2$: memorie scurtă')])), 'small')

D.frame(T('Fractional integration and ARFIMA (1/2)', 'Integrarea fracționară și ARFIMA (1/2)'), items(
    (T(r'The fractional difference operator is a power series in the lag operator $L$ ($LX_t = X_{t-1}$) \refGJ, \refHos', r'Operatorul de diferențiere fracționară este o serie de puteri în operatorul lag $L$ ($LX_t = X_{t-1}$) \refGJ, \refHos'
       ) + r'''
    \[ (1 - L)^d = \sum_{k\ge0}\pi_k L^k, \qquad \pi_0 = 1, \quad \pi_k = \pi_{k-1}\frac{k - 1 - d}{k}, \quad \pi_k \sim \frac{k^{-d-1}}{\Gamma(-d)} \]''',
     [T(r'$\pi_k$: the weight of $X_{t-k}$; it decays hyperbolically, so the filter has infinite memory; $d = 1$ gives the usual difference $1 - L$',
        r'$\pi_k$: ponderea lui $X_{t-k}$; scade hiperbolic, deci filtrul are memorie infinită; $d = 1$ dă diferența obișnuită $1 - L$')]),
    (T(r'ARFIMA$(p,d,q)$: an ARMA for the fractionally differenced series', r'ARFIMA$(p,d,q)$: un ARMA pentru seria diferențiată fracționar'
       ) + r'''
    \[ \phi(L)(1 - L)^d(X_t - \mu) = \theta(L)\varepsilon_t \]''',
     [T(r'$\phi(L)$, $\theta(L)$: AR and MA polynomials of orders $p$, $q$; $\mu$: mean; $\varepsilon_t$: white noise with variance $\sigma^2$',
        r'$\phi(L)$, $\theta(L)$: polinoamele AR și MA de ordinele $p$, $q$; $\mu$: media; $\varepsilon_t$: zgomot alb cu varianța $\sigma^2$'),
      T(r'stationary and invertible for $-1/2 < d < 1/2$', r'staționar și inversabil pentru $-1/2 < d < 1/2$')])), 'small')

D.frame(T('Fractional integration and ARFIMA (2/2)', 'Integrarea fracționară și ARFIMA (2/2)'), items(
    (T(r'Spectrum: a pole at zero times the spectrum of the ARMA part', r'Spectrul: un pol în zero înmulțit cu spectrul părții ARMA'
       ) + r'''
    \[ f(\lambda) = \frac{\sigma^2}{2\pi}\,\big|2\sin(\lambda/2)\big|^{-2d}\,\frac{|\theta(e^{-i\lambda})|^2}{|\phi(e^{-i\lambda})|^2} = |2\sin(\lambda/2)|^{-2d}f^*(\lambda) \]''',
     [T(r'$f^*$: the smooth short-memory (ARMA) part; near zero $|2\sin(\lambda/2)| \approx \lambda$, so $f(\lambda) \approx f^*(0)\lambda^{-2d}$',
        r'$f^*$: partea netedă de memorie scurtă (ARMA); lîngă zero $|2\sin(\lambda/2)| \approx \lambda$, deci $f(\lambda) \approx f^*(0)\lambda^{-2d}$')]),
    (T(r'ARFIMA$(0,d,0)$: variance and autocorrelations in closed form', r'ARFIMA$(0,d,0)$: varianța și autocorelațiile în formă închisă'
       ) + r'''
    \[ \gamma(0) = \sigma^2\frac{\Gamma(1 - 2d)}{\Gamma(1 - d)^2}, \qquad \rho(k) = \frac{\Gamma(k + d)\Gamma(1 - d)}{\Gamma(k - d + 1)\Gamma(d)} \sim \frac{\Gamma(1 - d)}{\Gamma(d)}k^{2d-1} \]''',
     [T(r'recursion $\rho(k) = \rho(k - 1)\,(k - 1 + d)/(k - d)$, $\rho(1) = d/(1 - d)$', r'recursia $\rho(k) = \rho(k - 1)\,(k - 1 + d)/(k - d)$, $\rho(1) = d/(1 - d)$')])), 'small')

chart(T('Hyperbolic and geometric decay', 'Descreștere hiperbolică și geometrică'), 'ats_ch10_acf_spec', 'ATS_ch10_memory', [
    T(r'Left: ACF of ARFIMA$(0,d,0)$ and of an AR(1) with the same $\rho(1)$, log-log; right: spectral densities near zero, the AR(1) scaled to the same variance',
      r'Stînga: ACF pentru ARFIMA$(0,d,0)$ și pentru un AR(1) cu același $\rho(1)$, scară log-log; dreapta: densitățile spectrale lîngă zero, AR(1) scalat la aceeași varianță')], h='0.63\\textheight')

interp(('the two decays', 'celor două descreșteri'), [
    T(r'$d = 0.4$: $\rho(1) = @{ac.r1}$, $\rho(10) = @{ac.r10}$, $\rho(100) = @{ac.r100}$; the matching AR(1) has $\rho(100)$ of order $10^{-@{ac.ar100}}$', r'$d = 0{,}4$: $\rho(1) = @{ac.r1}$, $\rho(10) = @{ac.r10}$, $\rho(100) = @{ac.r100}$; AR(1) corespunzător are $\rho(100)$ de ordinul $10^{-@{ac.ar100}}$'),
    T(r'Partial sums $\sum_{k\le100}\rho(k) = @{ac.sum100}$ and $\sum_{k\le200}\rho(k) = @{ac.sum200}$: they keep growing, like $K^{2d}$', r'Sumele parțiale $\sum_{k\le100}\rho(k) = @{ac.sum100}$ și $\sum_{k\le200}\rho(k) = @{ac.sum200}$: continuă să crească, precum $K^{2d}$'),
    T('In the spectrum the difference is a pole against a plateau: long memory lives at the lowest frequencies, where few periodogram ordinates exist', 'În spectru diferența este un pol față de un platou: memoria lungă se află la frecvențele cele mai joase, unde există puține ordonate ale periodogramei'),
    T('Hence all semiparametric estimators look only at the $m$ lowest Fourier frequencies', 'De aceea toți estimatorii semiparametrici privesc doar cele mai joase $m$ frecvențe Fourier')])

D.frame(T('Where long memory comes from: aggregation', 'Originea memoriei lungi: agregarea'), items(
    (T(r'\refGra: the scaled sum of $N$ independent AR(1) series with random coefficients', r'\refGra: suma scalată a $N$ serii AR(1) independente, cu coeficienți aleatori'
       ) + r'''
    \[ X_t = \frac{1}{\sqrt N}\sum_{i=1}^N x_{it}, \qquad x_{it} = \phi_i x_{i,t-1} + \varepsilon_{it}, \qquad \phi_i^2 \sim \mathrm{Beta}(p, q) \]''',
     [T(r'$\phi_i$: persistence of unit $i$, drawn once; Beta density $\propto \phi^{2p-1}(1 - \phi^2)^{q-1}$ on $(0, 1)$; $q$ controls the mass near the unit root',
        r'$\phi_i$: persistența unității $i$, extrasă o singură dată; densitatea Beta $\propto \phi^{2p-1}(1 - \phi^2)^{q-1}$ pe $(0, 1)$; $q$ controlează masa din apropierea rădăcinii unitare')]),
    (T(r'Derivation: average the AR(1) autocovariances over the distribution of $\phi$', r'Derivare: mediem autocovarianțele AR(1) după distribuția lui $\phi$'
       ) + r'''
    \[ \gamma_X(k) = \E\Big[\frac{\phi^k}{1 - \phi^2}\Big] \propto \int_0^1\phi^{k+2p-1}(1 - \phi^2)^{q-2}d\phi \propto B\Big(\frac{k}{2} + p, q - 1\Big) \sim c\,k^{-(q-1)} \]''',
     [T(r'$B(\cdot, \cdot)$: the beta function; matching $k^{2d-1}$ gives $d = 1 - q/2$, long memory for $1 < q < 2$', r'$B(\cdot, \cdot)$: funcția beta; identificînd cu $k^{2d-1}$ obținem $d = 1 - q/2$, memorie lungă pentru $1 < q < 2$')]),
    T('Economic reading: aggregate inflation, volatility or output mixes many short-memory agents with heterogeneous persistence; a few near-unit-root units dominate the low frequencies',
      'Lectura economică: inflația, volatilitatea sau producția agregată combină mulți agenți cu memorie scurtă și persistență eterogenă; cîteva unități apropiate de rădăcina unitară domină frecvențele joase'),
    T('Long memory can therefore be structural, not a curiosity of the estimator', 'Memoria lungă poate fi deci structurală, nu o curiozitate a estimatorului')), 'small')

chart(T('Aggregation of AR(1) series', 'Agregarea seriilor AR(1)'), 'ats_ch10_aggregation', 'ATS_ch10_memory', [
    T(r'$\phi_i^2 \sim \mathrm{Beta}(1, 1.4)$, so $d = 1 - q/2 = @{ag.d0}$; $n = 4000$; local Whittle with $m = @{ag.m}$, @{ag.reps} replications per $N$; left: periodogram of one aggregate of 3000 series',
      r'$\phi_i^2 \sim \mathrm{Beta}(1; 1{,}4)$, deci $d = 1 - q/2 = @{ag.d0}$; $n = 4000$; local Whittle cu $m = @{ag.m}$, @{ag.reps} replicări pentru fiecare $N$; stînga: periodograma unui agregat de 3000 de serii')], h='0.54\\textheight')

interp(('aggregation', 'agregării'), [
    T(r'One AR(1): median $\hat d = @{ag.m1}$; ten series: @{ag.m10}; 100 series: @{ag.m100}; 3000 series: @{ag.m3000} (10\%--90\%: @{ag.lo} to @{ag.hi})', r'Un singur AR(1): mediana $\hat d = @{ag.m1}$; zece serii: @{ag.m10}; 100 de serii: @{ag.m100}; 3000 de serii: @{ag.m3000} (10\%--90\%: între @{ag.lo} și @{ag.hi})'),
    T(r'The estimate settles above the limit @{ag.d0}: the aggregate spectrum is $\lambda^{-2d}$ only very close to zero, and $m = n^{0.65}$ reaches into the region where it is not', r'Estimația se stabilizează peste limita @{ag.d0}: spectrul agregatului este $\lambda^{-2d}$ doar foarte aproape de zero, iar $m = n^{0{,}65}$ intră în zona în care nu mai este'),
    T('This is the bias problem of Section 2 in its purest form: a semiparametric estimator is only as good as its bandwidth', 'Aceasta este problema deplasării din secțiunea 2 în forma ei cea mai pură: un estimator semiparametric este atît de bun cît îi este lățimea de bandă'),
    T('The direction of the effect, from no memory to clear long memory, is the point of Granger\'s theorem', 'Direcția efectului, de la lipsa memoriei la memorie lungă clară, este esența teoremei lui Granger')])

D.frame(T('Consequences for inference: the sample mean', 'Consecințe pentru inferență: media de eșantion'), items(
    (T(r'The variance of the sample mean $\bar X_n$ decays more slowly than $1/n$', r'Varianța mediei de eșantion $\bar X_n$ scade mai lent decît $1/n$'
       ) + r'''
    \[ \Var(\bar X_n) = \frac1n\sum_{|k|<n}\Big(1 - \frac{|k|}{n}\Big)\gamma(k) \sim \frac{c_\gamma}{d(2d + 1)}\,n^{2d-1} \]''',
     [T(r'the mean converges at rate $n^{1/2-d}$, not $n^{1/2}$; with $d = 0.4$: $n^{0.1}$', r'media converge cu viteza $n^{1/2-d}$, nu $n^{1/2}$; cu $d = 0{,}4$: $n^{0{,}1}$')]),
    (T('HAC standard errors (Chapter 0) assume $\\sum_k|\\gamma(k)| < \\infty$: under long memory the long-run variance is infinite and Newey--West intervals are too narrow', 'Erorile standard HAC (Capitolul 0) presupun $\\sum_k|\\gamma(k)| < \\infty$: sub memorie lungă, varianța de termen lung este infinită, iar intervalele Newey--West sînt prea înguste'),
     [T('the same holds for DM tests (Chapter 1) on loss differences that inherit long memory', 'la fel pentru testele DM (Capitolul 1) aplicate diferențelor de pierderi care moștenesc memoria lungă')]),
    (T(r'Regression with long-memory regressors and errors: OLS slopes converge slowly', r'Regresie cu regresori și erori cu memorie lungă: pantele OLS converg încet'),
     [T(r'spurious regression between independent fractional series when $d_x + d_u > 1/2$ ($d_x$, $d_u$: memory of the regressor and of the error)', r'regresie falsă între serii fracționare independente cînd $d_x + d_u > 1/2$ ($d_x$, $d_u$: memoria regresorului și a erorii)')]),
    T('Every test of this course built on $\\sqrt n$ asymptotics needs a second look when $d > 0$', 'Fiecare test din acest curs construit pe asimptotica $\\sqrt n$ trebuie reexaminat cînd $d > 0$')), 'small')

D.recap(('Long memory', 'memoria lungă'), [
    T(r'Long memory: hyperbolic ACF $k^{2d-1}$ and a spectral pole $\lambda^{-2d}$; $H = d + 1/2$', r'Memoria lungă: ACF hiperbolică $k^{2d-1}$ și un pol spectral $\lambda^{-2d}$; $H = d + 1/2$'),
    T('ARFIMA separates the pole $|2\\sin(\\lambda/2)|^{-2d}$ from the short-memory part $f^*$', 'ARFIMA separă polul $|2\\sin(\\lambda/2)|^{-2d}$ de partea de memorie scurtă $f^*$'),
    T('Aggregation of heterogeneous AR(1) units produces long memory; the mean converges at $n^{1/2-d}$', 'Agregarea unităților AR(1) eterogene produce memorie lungă; media converge cu $n^{1/2-d}$')])

# =============================================================================
# 2. ESTIMARE SEMIPARAMETRICĂ
# =============================================================================
D.section('Semiparametric estimation and its asymptotics', 'Estimarea semiparametrică și asimptotica ei')

D.frame(T('The periodogram near frequency zero', 'Periodograma lîngă frecvența zero'), items(
    (T(r'The periodogram: the squared modulus of the discrete Fourier transform, at the Fourier frequencies', r'Periodograma: pătratul modulului transformatei Fourier discrete, la frecvențele Fourier'
       ) + r'''
    \[ I(\lambda_j) = \frac{1}{2\pi n}\Big|\sum_{t=1}^n X_te^{-i\lambda_jt}\Big|^2, \qquad \lambda_j = \frac{2\pi j}{n}, \quad j = 1, \dots, m \]''',
     [T(r'$n$: sample size; $m$: bandwidth, the number of lowest frequencies used; short memory: $I(\lambda_j)/f(\lambda_j)$ asymptotically i.i.d.\ $\mathrm{Exp}(1)$',
        r'$n$: mărimea eșantionului; $m$: lățimea de bandă, numărul frecvențelor celor mai joase folosite; memorie scurtă: $I(\lambda_j)/f(\lambda_j)$ asimptotic i.i.d.\ $\mathrm{Exp}(1)$')]),
    (T(r'Long memory: for fixed $j$, $\E\,I(\lambda_j)/f(\lambda_j) \not\to 1$ and the ordinates stay correlated \refRobB', r'Memorie lungă: pentru $j$ fix, $\E\,I(\lambda_j)/f(\lambda_j) \not\to 1$, iar ordonatele rămîn corelate \refRobB'),
     [T(r'the distortion vanishes as $j \to \infty$: the proofs need $m \to \infty$, $m/n \to 0$, and handle the first frequencies separately', r'distorsiunea dispare cînd $j \to \infty$: demonstrațiile cer $m \to \infty$, $m/n \to 0$ și tratează separat primele frecvențe')]),
    (T(r'Semiparametric model: only the behaviour near zero is specified', r'Modelul semiparametric: se specifică doar comportamentul lîngă zero'
       ) + r'''
    \[ f(\lambda) = G\lambda^{-2d}\big(1 + O(\lambda^\beta)\big), \qquad \lambda \to 0, \quad \beta \in (0, 2] \]''',
     [T(r'$G > 0$: level of the spectrum at low frequencies; $\beta$: smoothness of the remainder; $\beta = 2$ for ARFIMA, because $f^*$ is smooth and even',
        r'$G > 0$: nivelul spectrului la frecvențe joase; $\beta$: netezimea restului; $\beta = 2$ pentru ARFIMA, deoarece $f^*$ este netedă și pară')])), 'small')

D.frame(T('GPH: the log-periodogram regression', 'GPH: regresia pe logaritmul periodogramei'), items(
    (T(r'Taking logs of $I = f\xi$ gives a linear regression in $\log\lambda_j$ with slope $-2d$ \refGPH', r'Logaritmînd $I = f\xi$ obținem o regresie liniară în $\log\lambda_j$, cu panta $-2d$ \refGPH'
       ) + r'''
    \[ \log I(\lambda_j) = \log G - 2d\log\lambda_j + \log\xi_j, \qquad \xi_j = \frac{I(\lambda_j)}{f(\lambda_j)} \]''',
     [T(r'OLS on $j = 1, \dots, m$; with $\xi_j \sim \mathrm{Exp}(1)$: $\E\log\xi_j = -\gamma_E$ ($\gamma_E \approx 0.577$, Euler\'s constant), $\Var\log\xi_j = \pi^2/6$',
        r'OLS pe $j = 1, \dots, m$; cu $\xi_j \sim \mathrm{Exp}(1)$: $\E\log\xi_j = -\gamma_E$ ($\gamma_E \approx 0{,}577$, constanta lui Euler), $\Var\log\xi_j = \pi^2/6$')]),
    (T(r'\refRobB: for $|d| < 1/2$ and Gaussian $X$, if $m \to \infty$ and $m^5/n^4 \to 0$', r'\refRobB: pentru $|d| < 1/2$ și $X$ gaussian, dacă $m \to \infty$ și $m^5/n^4 \to 0$'
       ) + r'''
    \[ \sqrt m(\hat d_{GPH} - d) \to N(0, \pi^2/24) \]''',
     [T(r'origin of $\pi^2/24$: $\Var(\hat d) = \dfrac{\pi^2/6}{4\sum_j\nu_j^2}$, with $\nu_j = \log j - \overline{\log j}$ the centred regressor and $\sum_j\nu_j^2 \sim m$',
        r'originea lui $\pi^2/24$: $\Var(\hat d) = \dfrac{\pi^2/6}{4\sum_j\nu_j^2}$, cu $\nu_j = \log j - \overline{\log j}$ regresorul centrat și $\sum_j\nu_j^2 \sim m$')]),
    (T(r'Bias of order $(m/n)^2$ (formula on the bandwidth slide below)', r'Deplasarea este de ordinul $(m/n)^2$ (formula pe slide-ul despre lățimea de bandă, mai jos)'),
     [T('the condition $m^5/n^4 \\to 0$ makes the bias negligible relative to the standard deviation $m^{-1/2}$', 'condiția $m^5/n^4 \\to 0$ face deplasarea neglijabilă față de abaterea standard $m^{-1/2}$')])), 'small')

D.frame(T('Local Whittle (1/2): the objective', 'Local Whittle (1/2): funcția obiectiv'), items(
    (T(r'Whittle approximation of the Gaussian log-likelihood, restricted to $j \le m$, with $f(\lambda_j) = G\lambda_j^{-2d}$', r'Aproximarea Whittle a log-verosimilității gaussiene, restrînsă la $j \le m$, cu $f(\lambda_j) = G\lambda_j^{-2d}$'
       ) + r'''
    \[ Q(G, d) = \frac1m\sum_{j=1}^m\Big[\log\big(G\lambda_j^{-2d}\big) + \frac{I(\lambda_j)}{G\lambda_j^{-2d}}\Big] \]''',
     [T(r'the same form as QLIKE (Chapter 8): the model spectrum $G\lambda_j^{-2d}$ is fitted to the periodogram ordinate by ordinate',
        r'aceeași formă ca QLIKE (Capitolul 8): spectrul modelului $G\lambda_j^{-2d}$ este ajustat la periodogramă, ordonată cu ordonată')]),
    (T(r'Concentrate out $G$ \refRobC: for given $d$ the optimal level is the average of $\lambda_j^{2d}I(\lambda_j)$', r'Eliminăm $G$ prin concentrare \refRobC: pentru $d$ dat, nivelul optim este media lui $\lambda_j^{2d}I(\lambda_j)$'
       ) + r'''
    \[ \hat G(d) = \frac1m\sum_j\lambda_j^{2d}I(\lambda_j), \qquad \hat d_{LW} = \arg\min_d R(d) \]
    \[ R(d) = \log\hat G(d) - \frac{2d}{m}\sum_{j=1}^m\log\lambda_j \]''',
     [T(r'a one-dimensional minimisation in $d$', r'o minimizare unidimensională în $d$')])), 'small')

D.frame(T('Local Whittle (2/2): the variance', 'Local Whittle (2/2): varianța'), items(
    (T(r'Score at the truth: a weighted sum of $\xi_j - 1$', r'Scorul în valoarea adevărată: o sumă ponderată de $\xi_j - 1$'
       ) + r'''
    \[ R'(d) = \frac{2}{m}\sum_j\nu_j\Big(\frac{\lambda_j^{2d}I(\lambda_j)}{\hat G(d)} - 1\Big) \]''',
     [T(r'$\nu_j = \log\lambda_j - \overline{\log\lambda}$: centred log frequency; with $\Var(\xi_j) = 1$ and $R\'\'(d) \to 4$: $\sqrt m(\hat d - d) \to N(0, 4/16) = N(0, 1/4)$',
        r'$\nu_j = \log\lambda_j - \overline{\log\lambda}$: logaritmul centrat al frecvenței; cu $\Var(\xi_j) = 1$ și $R\'\'(d) \to 4$: $\sqrt m(\hat d - d) \to N(0, 4/16) = N(0, 1/4)$')]),
    (T(r'No distributional assumption beyond a linear process with martingale-difference innovations', r'Nicio ipoteză de distribuție în afara unui proces liniar cu inovații diferențe de martingal'),
     [T(r'efficiency relative to GPH: $(\pi^2/24)/(1/4) = \pi^2/6 \approx 1.64$', r'eficiența relativă față de GPH: $(\pi^2/24)/(1/4) = \pi^2/6 \approx 1{,}64$'),
      T('derivation step by step: Appendix  % applink: the variance of local Whittle', 'derivarea pas cu pas: Anexa  % applink: varianța estimatorului local Whittle')])), 'small')

D.frame(T('Local Whittle: the theorem and its limits', 'Local Whittle: teorema și limitele ei'), items(
    (T(r'\refRobC: for $d \in (-1/2, 1/2)$, $f(\lambda) = G\lambda^{-2d}(1 + O(\lambda^\beta))$ and a bandwidth with $1/m + m^{1+2\beta}(\log m)^2/n^{2\beta} \to 0$', r'\refRobC: pentru $d \in (-1/2, 1/2)$, $f(\lambda) = G\lambda^{-2d}(1 + O(\lambda^\beta))$ și o lățime de bandă cu $1/m + m^{1+2\beta}(\log m)^2/n^{2\beta} \to 0$'),
     [T(r'$\hat d \to_p d$ and $\sqrt m(\hat d - d) \to N(0, 1/4)$; the condition on $m$: it grows, but slowly enough for the bias to vanish', r'$\hat d \to_p d$ și $\sqrt m(\hat d - d) \to N(0, 1/4)$; condiția pentru $m$: crește, dar suficient de lent pentru ca deplasarea să dispară')]),
    (T(r'Non-stationary $d$: consistent for $d < 1$, asymptotically Normal for $d < 3/4$ \refVel', r'$d$ nestaționar: consistent pentru $d < 1$, asimptotic normal pentru $d < 3/4$ \refVel'),
     [T(r'for $d > 1$ it converges in probability to 1; between $3/4$ and 1 the limit is non-Normal \refPS', r'pentru $d > 1$ converge în probabilitate la 1; între $3/4$ și 1 limita nu este normală \refPS')]),
    (T('Remedies: difference the data first (needs knowing $d > 1/2$), taper the periodogram (variance cost), or estimate exactly', 'Remedii: diferențiem întîi datele (trebuie să știm că $d > 1/2$), aplicăm o fereastră periodogramei (cu cost în varianță) sau estimăm exact'),
     [])), 'small')

D.frame(T('Exact local Whittle', 'Local Whittle exact'), items(
    (T(r'\refSP: replace $\lambda_j^{2d}I_X(\lambda_j)$ by the periodogram of the fractionally differenced data', r'\refSP: înlocuim $\lambda_j^{2d}I_X(\lambda_j)$ prin periodograma datelor diferențiate fracționar'
       ) + r'''
    \[ \Delta^dX_t = \sum_{k=0}^{t-1}\pi_kX_{t-k}, \qquad R_E(d) = \log\Big(\frac1m\sum_jI_{\Delta^dX}(\lambda_j)\Big) - \frac{2d}{m}\sum_j\log\lambda_j \]''',
     [T(r'$\Delta^d = (1 - L)^d$ truncated at the start of the sample; $I_{\Delta^dX}$: periodogram of the differenced series',
        r'$\Delta^d = (1 - L)^d$, trunchiat la începutul eșantionului; $I_{\Delta^dX}$: periodograma seriei diferențiate'),
      T(r'$\lambda^{2d}I_X(\lambda)$ approximates $I_{\Delta^dX}(\lambda)$ only for $d < 1/2$; the exact version removes the error that breaks LW for large $d$: $\sqrt m(\hat d_{ELW} - d) \to N(0, 1/4)$ on any search interval of width $< 9/2$',
        r'$\lambda^{2d}I_X(\lambda)$ aproximează $I_{\Delta^dX}(\lambda)$ doar pentru $d < 1/2$; versiunea exactă elimină eroarea care strică LW pentru $d$ mare: $\sqrt m(\hat d_{ELW} - d) \to N(0, 1/4)$ pe orice interval de căutare de lățime $< 9/2$')]),
    (T(r'Unknown mean \refShi: subtract $\hat\mu(d) = w(d)\bar X + (1 - w(d))X_1$', r'Media necunoscută \refShi: se scade $\hat\mu(d) = w(d)\bar X + (1 - w(d))X_1$'),
     [T(r'$w(d) = 1$ for $d \le 1/2$, $0$ for $d \ge 3/4$, smooth in between: the sample mean is a bad estimator of the level when $d > 1/2$', r'$w(d) = 1$ pentru $d \le 1/2$, $0$ pentru $d \ge 3/4$, netedă între ele: media de eșantion estimează prost nivelul cînd $d > 1/2$')]),
    T('Cost: one fractional difference per evaluation, $O(n\\log n)$ by FFT', 'Costul: o diferență fracționară pentru fiecare evaluare, $O(n\\log n)$ prin FFT')), 'small')

chart(T('GPH, local Whittle and exact local Whittle by Monte Carlo', 'GPH, local Whittle și local Whittle exact prin Monte Carlo'), 'ats_ch10_mc_estimators', 'ATS_ch10_estimation', [
    T(r'@{mc.reps} Gaussian ARFIMA$(0,d,0)$ paths, $n = 2000$, $m = n^{0.65} = @{mc.m}$; asymptotic SD: GPH @{mc.seg}, local Whittle @{mc.sel}; $d = 1.2$ is simulated as the partial sum of an ARFIMA$(0, 0.2, 0)$',
      r'@{mc.reps} de traiectorii ARFIMA$(0,d,0)$ gaussiene, $n = 2000$, $m = n^{0{,}65} = @{mc.m}$; abaterea standard asimptotică: GPH @{mc.seg}, local Whittle @{mc.sel}; $d = 1{,}2$ se simulează ca sumă parțială a unui ARFIMA$(0; 0{,}2; 0)$')], h='0.63\\textheight')

interp(('the Monte Carlo', 'experimentului Monte Carlo'), [
    T(r'$d = 0.3$: means @{mc.s.GPH.m}, @{mc.s.LW.m}, @{mc.s.ELW.m}; SD @{mc.s.GPH.s}, @{mc.s.LW.s}, @{mc.s.ELW.s}; 95\% coverage @{mc.s.GPH.c}\%, @{mc.s.LW.c}\%, @{mc.s.ELW.c}\% (GPH, LW, ELW)', r'$d = 0{,}3$: medii @{mc.s.GPH.m}, @{mc.s.LW.m}, @{mc.s.ELW.m}; abateri standard @{mc.s.GPH.s}, @{mc.s.LW.s}, @{mc.s.ELW.s}; acoperirea de 95\%: @{mc.s.GPH.c}\%, @{mc.s.LW.c}\%, @{mc.s.ELW.c}\% (GPH, LW, ELW)'),
    T(r'The asymptotic laws are accurate at $n = 2000$; local Whittle is about $\sqrt{\pi^2/6}$ times tighter than GPH', r'Legile asimptotice sînt precise la $n = 2000$; local Whittle este de circa $\sqrt{\pi^2/6}$ ori mai strîns decît GPH'),
    T(r'$d = 1.2$: GPH @{mc.n.GPH.m} and LW @{mc.n.LW.m} collapse towards 1 (coverage @{mc.n.GPH.c}\% and @{mc.n.LW.c}\%); ELW @{mc.n.ELW.m}, coverage @{mc.n.ELW.c}\%', r'$d = 1{,}2$: GPH @{mc.n.GPH.m} și LW @{mc.n.LW.m} se strîng spre 1 (acoperire @{mc.n.GPH.c}\% și @{mc.n.LW.c}\%); ELW @{mc.n.ELW.m}, acoperire @{mc.n.ELW.c}\%'),
    T('For series that may be non-stationary (prices, inflation in levels, log RV with $d$ near 0.5) report ELW', 'Pentru seriile care pot fi nestaționare (prețuri, inflația în nivel, logaritmul RV cu $d$ aproape de 0,5) raportați ELW')])

D.frame(T('Bandwidth: bias against variance', 'Lățimea de bandă: deplasare și varianță'), items(
    (T(r'Leading bias (GPH and LW) \refHDB: the curvature of $\log f^*$ near zero leaks into the slope', r'Deplasarea principală (GPH și LW) \refHDB: curbura lui $\log f^*$ lîngă zero trece în pantă'
       ) + r'''
    \[ \E\hat d - d \approx -\frac{2\pi^2}{9}\,\frac{f^{*\prime\prime}(0)}{f^*(0)}\Big(\frac mn\Big)^2 = C\Big(\frac mn\Big)^2 \]''',
     [T(r'from regressing $\log f^*(\lambda_j) \approx \log f^*(0) + b\lambda_j^2$, $b = \tfrac12f^{*\prime\prime}(0)/f^*(0)$, on $-2\nu_j$; $C$: the bias constant',
        r'din regresia lui $\log f^*(\lambda_j) \approx \log f^*(0) + b\lambda_j^2$, $b = \tfrac12f^{*\prime\prime}(0)/f^*(0)$, pe $-2\nu_j$; $C$: constanta deplasării'),
      T(r'ARFIMA$(1,d,0)$: $f^{*\prime\prime}(0)/f^*(0) = -2\phi/(1 - \phi)^2$, upward bias for $\phi > 0$', r'ARFIMA$(1,d,0)$: $f^{*\prime\prime}(0)/f^*(0) = -2\phi/(1 - \phi)^2$, deplasare în sus pentru $\phi > 0$')]),
    (T(r'MSE: squared bias plus variance; minimising over $m$ gives the optimal bandwidth \refHR', r'MSE: pătratul deplasării plus varianța; minimizarea în $m$ dă lățimea de bandă optimă \refHR'
       ) + r'''
    \[ \mathrm{MSE}(m) \approx C^2\Big(\frac mn\Big)^4 + \frac{1}{4m}, \qquad m^* = \Big(\frac{n^4}{16C^2}\Big)^{1/5} \propto n^{4/5} \]''',
     [T(r'$C$ is unknown: plug-in rules estimate it; local polynomial Whittle \refAnSu\ removes the $\lambda^2$ term at a variance cost', r'$C$ este necunoscută: regulile plug-in o estimează; local Whittle polinomial \refAnSu\ elimină termenul în $\lambda^2$ cu un cost în varianță')]),
    T(r'At $m^*$ bias and SD are of the same order, so nominal intervals undercover; practice: plot $\hat d(m)$ over a range and report it with the intervals', r'La $m^*$ deplasarea și abaterea standard sînt de același ordin, deci intervalele nominale acoperă prea puțin; în practică: graficul lui $\hat d(m)$ pe un interval de valori, raportat împreună cu intervalele')), 'small')

chart(T('Bias and RMSE across bandwidths', 'Deplasarea și RMSE în funcție de lățimea de bandă'), 'ats_ch10_bandwidth', 'ATS_ch10_estimation', [
    T(r'Local Whittle, ARFIMA$(1, 0.3, 0)$ with $\phi = 0.6$, $n = 2000$, 300 replications, $m = n^a$ for $a = 0.40, \dots, 0.80$; dashed: the leading bias $C(m/n)^2$ with $C = @{bw.C}$ and the asymptotic RMSE',
      r'Local Whittle, ARFIMA$(1; 0{,}3; 0)$ cu $\phi = 0{,}6$, $n = 2000$, 300 de replicări, $m = n^a$ pentru $a = 0{,}40, \dots, 0{,}80$; linie întreruptă: deplasarea principală $C(m/n)^2$ cu $C = @{bw.C}$ și RMSE asimptotic')], h='0.55\\textheight')

interp(('the bandwidth trade-off', 'compromisului lățimii de bandă'), [
    T(r'Small $m$ ($a = 0.40$): bias @{bw.b40}, RMSE @{bw.r40}, dominated by variance; large $m$ ($a = 0.80$): bias @{bw.b80}, RMSE @{bw.r80}', r'$m$ mic ($a = 0{,}40$): deplasare @{bw.b40}, RMSE @{bw.r40}, dominat de varianță; $m$ mare ($a = 0{,}80$): deplasare @{bw.b80}, RMSE @{bw.r80}'),
    T(r'Smallest Monte Carlo RMSE @{bw.rmin} at $m = @{bw.bestm}$ ($a = @{bw.besta}$); theory: $m^* = @{bw.mopt}$ ($a = @{bw.aopt}$)', r'Cel mai mic RMSE Monte Carlo, @{bw.rmin}, la $m = @{bw.bestm}$ ($a = @{bw.besta}$); teoria: $m^* = @{bw.mopt}$ ($a = @{bw.aopt}$)'),
    T(r'The leading term overstates the bias at large $m$ (@{bw.th80} against @{bw.b80}): the $\lambda^2$ expansion is local', r'Termenul principal supraestimează deplasarea la $m$ mare (@{bw.th80} față de @{bw.b80}): dezvoltarea în $\lambda^2$ este locală'),
    T('A fixed rule such as $m = n^{0.8}$ can turn a short-memory AR component into apparent long memory', 'O regulă fixă precum $m = n^{0{,}8}$ poate transforma o componentă AR de memorie scurtă în memorie lungă aparentă')])

D.frame(T('Parametric alternative: Whittle and exact ML', 'Alternativa parametrică: Whittle și ML exact'), items(
    (T(r'Whittle: fit a fully specified spectral density over all frequencies \refFT', r'Whittle: se ajustează o densitate spectrală complet specificată pe toate frecvențele \refFT'
       ) + r'''
    \[ \hat\vartheta = \arg\min_\vartheta\sum_{j=1}^{\lfloor (n-1)/2\rfloor}\Big[\log f(\lambda_j; \vartheta) + \frac{I(\lambda_j)}{f(\lambda_j; \vartheta)}\Big] \]''',
     [T(r'$\vartheta$: all ARFIMA$(p,d,q)$ parameters ($d$, the AR and MA coefficients, $\sigma^2$); $\sqrt n$-consistent and efficient if the model is right; $\Var(\hat d) \approx 6/(\pi^2n)$ for $(0,d,0)$',
        r'$\vartheta$: toți parametrii ARFIMA$(p,d,q)$ ($d$, coeficienții AR și MA, $\sigma^2$); consistent cu viteza $\sqrt n$ și eficient dacă modelul este corect; $\Var(\hat d) \approx 6/(\pi^2n)$ pentru $(0,d,0)$')]),
    (T('The trade-off is robustness against efficiency: a wrong $(p, q)$ biases $\\hat d$ for every $n$', 'Compromisul este între robustețe și eficiență: un $(p, q)$ greșit deplasează $\\hat d$ pentru orice $n$'),
     [T('semiparametric: rate $\\sqrt m$, robust to $f^*$; parametric: rate $\\sqrt n$, exposed to misspecification', 'semiparametric: viteza $\\sqrt m$, robust la $f^*$; parametric: viteza $\\sqrt n$, expus la specificarea greșită')]),
    T('Common practice: semiparametric $\\hat d$ first, then a parametric model whose $d$ falls inside its interval, then forecasts', 'Practica obișnuită: întîi $\\hat d$ semiparametric, apoi un model parametric al cărui $d$ cade în intervalul lui, apoi prognoze')), 'small')

D.recap(('Semiparametric estimation', 'estimarea semiparametrică'), [
    T(r'GPH: $N(d, \pi^2/(24m))$; local Whittle: $N(d, 1/(4m))$; exact local Whittle keeps $N(d, 1/(4m))$ for non-stationary $d$', r'GPH: $N(d, \pi^2/(24m))$; local Whittle: $N(d, 1/(4m))$; local Whittle exact păstrează $N(d, 1/(4m))$ pentru $d$ nestaționar'),
    T(r'Bias $\propto (m/n)^2$, SD $\propto m^{-1/2}$: MSE-optimal $m \propto n^{4/5}$, with an unknown constant', r'Deplasarea $\propto (m/n)^2$, abaterea standard $\propto m^{-1/2}$: $m$ optim în MSE $\propto n^{4/5}$, cu o constantă necunoscută'),
    T('Always report $\\hat d(m)$ across bandwidths', 'Raportați întotdeauna $\\hat d(m)$ pentru mai multe lățimi de bandă')])

# =============================================================================
# 3. MEMORIE SCURTĂ SAU LUNGĂ
# =============================================================================
D.section('Short or long memory: testing against level shifts', 'Memorie scurtă sau lungă: testarea împotriva salturilor de nivel')

D.frame(T('Mechanisms of spurious long memory', 'Mecanismele memoriei lungi aparente'), items(
    (T(r'\refDI: Markov switching in the mean with switching probability $p_n \to 0$ as $n \to \infty$ produces $\Var(\sum_{t\le n}X_t) = O(n^{2d+1})$, like an I($d$) process', r'\refDI: schimbarea de regim markoviană în medie, cu probabilitatea de comutare $p_n \to 0$ cînd $n \to \infty$, produce $\Var(\sum_{t\le n}X_t) = O(n^{2d+1})$, ca un proces I($d$)'),
     [T(r'rare breaks are invisible at high frequencies and look like a pole at low ones \refGH', r'rupturile rare sînt invizibile la frecvențe înalte și arată ca un pol la frecvențe joase \refGH')]),
    (T(r'Random level shifts \refLP: a short-memory series $u_t$ around a level that jumps rarely', r'Salturi aleatoare de nivel \refLP: o serie cu memorie scurtă $u_t$ în jurul unui nivel care sare rar'
       ) + r'''
    \[ X_t = \mu_t + u_t, \qquad \mu_t = \mu_{t-1} + \delta_t\eta_t, \qquad \delta_t \sim \mathrm{Bernoulli}(p) \]''',
     [T(r'$\delta_t$: 1 on the (rare) days with a shift; $\eta_t$: shift size, variance $\sigma^2_\eta$; spectrum $\approx p\sigma_\eta^2/(2\pi\lambda^2)$ above frequency $\approx p$, plus the flat $f_u$: a slope $-2$ that fades into a plateau',
        r'$\delta_t$: 1 în zilele (rare) cu salt; $\eta_t$: mărimea saltului, cu varianța $\sigma^2_\eta$; spectrul $\approx p\sigma_\eta^2/(2\pi\lambda^2)$ peste frecvența $\approx p$, plus $f_u$ plat: o pantă $-2$ care trece într-un platou')]),
    (T(r'Signature \refPQ: under level shifts $\hat d(m)$ falls steeply as $m$ grows; under true long memory it is flat', r'Semnătura \refPQ: sub salturi de nivel, $\hat d(m)$ scade abrupt cînd $m$ crește; sub memorie lungă reală este plat'),
     [T('the same reasoning applies to trends, regime switches and deterministic seasonality left in the data', 'același raționament se aplică trendurilor, schimbărilor de regim și sezonalității deterministe rămase în date')]),
    T('TSA, Chapter 8 showed the phenomenon by example; here: a formal test with known size', 'TSA, Capitolul 8 a arătat fenomenul prin exemple; aici: un test formal cu mărime cunoscută')), 'small')

D.frame(T('The Qu (2011) test', 'Testul Qu (2011)'), items(
    (T(r'Under $H_0$ (stationary long memory) the LW score has mean zero in every frequency band; under level shifts the low frequencies are over-weighted \refQu', r'Sub $H_0$ (memorie lungă staționară) scorul LW are media zero în orice bandă de frecvențe; sub salturi de nivel, frecvențele joase sînt supraponderate \refQu'
       ) + r'''
    \[ W = \sup_{r\in[\varepsilon, 1]}\Big(\sum_{j=1}^m\nu_j^2\Big)^{-1/2}\Big|\sum_{j=1}^{\lfloor mr\rfloor}\nu_j\Big(\frac{I(\lambda_j)}{\hat G\lambda_j^{-2\hat d}} - 1\Big)\Big| \]''',
     [T(r'$\hat d, \hat G$: local Whittle on the same $m$; $\nu_j = \log\lambda_j - \overline{\log\lambda}$; $r$: the share of the $m$ frequencies included; $\varepsilon$: trimming of the lowest band',
        r'$\hat d, \hat G$: local Whittle pe aceleași $m$ frecvențe; $\nu_j = \log\lambda_j - \overline{\log\lambda}$; $r$: fracțiunea din cele $m$ frecvențe inclusă; $\varepsilon$: trimming-ul benzii celei mai joase'),
      T(r'the partial sum at $r = 1$ is zero by the first-order condition; $W$: the largest standardised partial sum', r'suma parțială în $r = 1$ este zero prin condiția de ordinul întîi; $W$: cea mai mare sumă parțială standardizată')]),
    (T(r'Limit: the supremum of a Gaussian process free of $d$ and $G$; Qu recommends $m = n^{0.7}$, $\varepsilon = 0.02$ (large $n$) or $0.05$', r'Limita: supremul unui proces gaussian care nu depinde de $d$ și $G$; Qu recomandă $m = n^{0{,}7}$, $\varepsilon = 0{,}02$ (pentru $n$ mare) sau $0{,}05$'),
     [T(r'our simulated critical values: $\varepsilon = 0.02$: @{qu.a.9}, @{qu.a.95}, @{qu.a.99}; $\varepsilon = 0.05$: @{qu.b.9}, @{qu.b.95}, @{qu.b.99} (10\%, 5\%, 1\%)', r'valorile critice simulate de noi: $\varepsilon = 0{,}02$: @{qu.a.9}; @{qu.a.95}; @{qu.a.99}; $\varepsilon = 0{,}05$: @{qu.b.9}; @{qu.b.95}; @{qu.b.99} (10\%, 5\%, 1\%)'),
      T('reject for large $W$: evidence against stationary long memory, typically breaks, level shifts or trends', 'respingem pentru $W$ mare: evidență împotriva memoriei lungi staționare, de obicei rupturi, salturi de nivel sau trenduri')])), 'small')

chart(T('Size, power and the bandwidth signature', 'Mărime, putere și semnătura lățimii de bandă'), 'ats_ch10_qu', 'ATS_ch10_qu_test', [
    T(r'$n = 2000$, @{qu.reps} replications, $m = n^{0.7} = @{qu.m}$, $\varepsilon = 0.02$; left: mean local Whittle $\hat d(m)$ (100 paths) and the S\&P 500 log RV; right: rejection rates at 5\%',
      r'$n = 2000$, @{qu.reps} de replicări, $m = n^{0{,}7} = @{qu.m}$, $\varepsilon = 0{,}02$; stînga: media $\hat d(m)$ local Whittle (100 de traiectorii) și logaritmul RV pentru S\&P 500; dreapta: ratele de respingere la 5\%')], h='0.54\\textheight')

interp(('the Qu test', 'testului Qu'), [
    T(r'Size: @{qu.r0}\% under ARFIMA$(0, 0.3, 0)$, @{qu.r1}\% when an AR(1) with $\phi = 0.5$ is added: short-run dynamics distort size in finite samples', r'Mărimea: @{qu.r0}\% sub ARFIMA$(0; 0{,}3; 0)$, @{qu.r1}\% cînd se adaugă un AR(1) cu $\phi = 0{,}5$: dinamica de termen scurt distorsionează mărimea în eșantioane finite'),
    T(r'Power: @{qu.r2}\% against level shifts and @{qu.r3}\% against one break, although LW reports $\hat d = @{qu.d2}$ and @{qu.d3}', r'Puterea: @{qu.r2}\% împotriva salturilor de nivel și @{qu.r3}\% împotriva unei singure rupturi, deși LW raportează $\hat d = @{qu.d2}$ și @{qu.d3}'),
    T(r'Signature: under level shifts $\hat d(m)$ drops from @{qu.l0} to @{qu.l1}; S\&P 500 log RV stays between @{qu.slo} and @{qu.shi}, and $W = @{qu.W}$ is far below the 10\% value', r'Semnătura: sub salturi de nivel, $\hat d(m)$ scade de la @{qu.l0} la @{qu.l1}; logaritmul RV pentru S\&P 500 rămîne între @{qu.slo} și @{qu.shi}, iar $W = @{qu.W}$ este mult sub valoarea de 10\%'),
    T('The memory of realised variance survives this test; Section 5 shows that $|r_t|$ of the BET and EUR/RON does not', 'Memoria varianței realizate trece acest test; secțiunea 5 arată că $|r_t|$ pentru BET și EUR/RON nu îl trece')])

chart(T('Inflation persistence and the disinflation', 'Persistența inflației și dezinflația'), 'ats_ch10_inflation', 'ATS_ch10_qu_test', [
    T(r'Monthly inflation, \% annualised: US CPI (seasonally adjusted) to @{in.us.end}, Romanian HICP (monthly means removed) to @{in.ro.end}; exact local Whittle with unknown mean, 95\% bands; full sample and after the disinflation (US from 1985, Romania from 2005)',
      r'Inflația lunară, \% anualizat: IPC SUA (ajustat sezonier) pînă în @{in.us.end}, IAPC România (fără mediile lunare) pînă în @{in.ro.end}; local Whittle exact cu media necunoscută, benzi de 95\%; eșantionul complet și după dezinflație (SUA din 1985, România din 2005)')], h='0.54\\textheight')

interp(('inflation persistence', 'persistenței inflației'), [
    T(r'US: $\hat d = @{in.us.full.d}$ (SE @{in.us.full.se}) on 1960--2026 but @{in.us.post.d} after 1985; Qu $W = @{in.us.full.W}$ (1\% value @{in.c.99}) rejects for the full sample, $W = @{in.us.post.W}$ after 1985', r'SUA: $\hat d = @{in.us.full.d}$ (SE @{in.us.full.se}) pe 1960--2026, dar @{in.us.post.d} după 1985; Qu $W = @{in.us.full.W}$ (valoarea de 1\%: @{in.c.99}) respinge pentru eșantionul complet, $W = @{in.us.post.W}$ după 1985'),
    T(r'Romania: $\hat d = @{in.ro.full.d}$ with the 1997--2004 disinflation, @{in.ro.post.d} from 2005 (range @{in.ro.lo} to @{in.ro.hi} across bandwidths); $W = @{in.ro.full.W}$ and @{in.ro.post.W} with only @{in.ro.full.n} and @{in.ro.post.n} months', r'România: $\hat d = @{in.ro.full.d}$ cu dezinflația din 1997--2004, @{in.ro.post.d} din 2005 (între @{in.ro.lo} și @{in.ro.hi} după lățimea de bandă); $W = @{in.ro.full.W}$ și @{in.ro.post.W}, cu doar @{in.ro.full.n} și @{in.ro.post.n} luni'),
    T(r'Plain local Whittle on the full Romanian sample gives @{in.ro.full.lw}: with a trend-like level shift only the exact version with the Shimotsu mean is reliable', r'Local Whittle simplu pe eșantionul complet pentru România dă @{in.ro.full.lw}: cu un salt de nivel asemănător unui trend, doar versiunea exactă cu media Shimotsu este de încredere'),
    T(r'Within a stable monetary regime inflation keeps moderate long memory, $\hat d$ = @{in.us.post.d} and @{in.ro.post.d} \refHW, \refBCT; the large estimates belong to regime changes', r'În interiorul unui regim monetar stabil, inflația păstrează o memorie lungă moderată, $\hat d$ = @{in.us.post.d} și @{in.ro.post.d} \refHW, \refBCT; estimațiile mari aparțin schimbărilor de regim')])

D.recap(('Short or long memory', 'memorie scurtă sau lungă'), [
    T('Breaks, level shifts and rare regime switches create a spectral pole and a large $\\hat d$', 'Rupturile, salturile de nivel și schimbările rare de regim creează un pol spectral și un $\\hat d$ mare'),
    T('Diagnostic: $\\hat d(m)$ falling with $m$; test: Qu (2011), with simulated critical values', 'Diagnostic: $\\hat d(m)$ scade cu $m$; test: Qu (2011), cu valori critice simulate'),
    T('US inflation: long memory is mostly the Great Inflation; log RV passes the test', 'Inflația din SUA: memoria lungă provine în mare parte din Marea Inflație; logaritmul RV trece testul')])

# =============================================================================
# 4. COINTEGRARE FRACȚIONARĂ
# =============================================================================
D.section('Fractional cointegration', 'Cointegrarea fracționară')

D.frame(T('Fractional cointegration and the FCVAR (1/2)', 'Cointegrarea fracționară și FCVAR (1/2)'), items(
    (T(r'$X_t \in \mathbb R^p$ is I($d$); it is \textbf{fractionally cointegrated} if $\beta\'X_t$ is I($d - b$), $b > 0$', r'$X_t \in \mathbb R^p$ este I($d$); este \textbf{cointegrat fracționar} dacă $\beta\'X_t$ este I($d - b$), $b > 0$'),
     [T(r'$d$: memory of the series; $b$: reduction of memory achieved by the combination $\beta\'X_t$; Chapter 4 is the case $d = b = 1$',
        r'$d$: memoria seriilor; $b$: reducerea memoriei obținută prin combinația $\beta\'X_t$; Capitolul 4 este cazul $d = b = 1$')]),
    (T(r'FCVAR \refJN: the VECM with the difference $\Delta$ replaced by fractional differences', r'FCVAR \refJN: VECM în care diferența $\Delta$ este înlocuită cu diferențe fracționare'
       ) + r'''
    \[ \Delta^dX_t = \alpha\beta'L_b\Delta^{d-b}X_t + \sum_{i=1}^k\Gamma_i\Delta^dL_b^iX_t + \varepsilon_t, \qquad L_b = 1 - \Delta^b \]''',
     [T(r'$\Delta^d = (1 - L)^d$; $L_b$: fractional lag operator ($L_1 = L$), so $d = b = 1$ gives the VECM',
        r'$\Delta^d = (1 - L)^d$; $L_b$: operatorul lag fracționar ($L_1 = L$), deci $d = b = 1$ dă VECM'),
      T(r'$\alpha$ ($p \times r$): adjustment; $\beta$ ($p \times r$): cointegrating vectors, rank $r$; $\Gamma_i$: short-run matrices, $k$ lags; $\varepsilon_t$: i.i.d. errors',
        r'$\alpha$ ($p \times r$): ajustarea; $\beta$ ($p \times r$): vectorii de cointegrare, rangul $r$; $\Gamma_i$: matricele de termen scurt, $k$ laguri; $\varepsilon_t$: erori i.i.d.')])), 'small')

D.frame(T('Fractional cointegration and the FCVAR (2/2): estimation and rank', 'Cointegrarea fracționară și FCVAR (2/2): estimare și rang'), items(
    (T(r'For fixed $(d, b)$: a reduced-rank regression of $Z_0 = \Delta^dX$ on $Z_1 = L_b\Delta^{d-b}X$; then profile the likelihood over $(d, b)$', r'Pentru $(d, b)$ fixat: o regresie de rang redus a lui $Z_0 = \Delta^dX$ pe $Z_1 = L_b\Delta^{d-b}X$; apoi profilăm verosimilitatea în $(d, b)$'
       ) + r'''
    \[ \ell_r(d, b) = -\frac T2\Big[\log\det S_{00} + \sum_{i\le r}\log(1 - \hat\lambda_i)\Big] \]''',
     [T(r'$S_{00}$: residual covariance of $Z_0$ (after the short-run terms); $\hat\lambda_i$: the Johansen eigenvalues, in decreasing order; $T$: sample size',
        r'$S_{00}$: covarianța reziduală a lui $Z_0$ (după termenii de termen scurt); $\hat\lambda_i$: valorile proprii Johansen, în ordine descrescătoare; $T$: mărimea eșantionului')]),
    (T(r'Rank tests: the LR trace statistic for rank $r$ against $p$', r'Testele de rang: statistica trace LR pentru rangul $r$ față de $p$'),
     [T(r'for $b < 1/2$ it is asymptotically $\chi^2_{(p-r)^2}$; for $b > 1/2$ use the fractional Dickey--Fuller distributions of \refMN', r'pentru $b < 1/2$ este asimptotic $\chi^2_{(p-r)^2}$; pentru $b > 1/2$ se folosesc distribuțiile Dickey--Fuller fracționare din \refMN')])), 'small')

D.frame(T('Semiparametric co-memory', 'Memorie comună semiparametrică'), items(
    (T(r'Narrow-band least squares (NBLS) \refRobA, \refCN: regress $y$ on $x$ using only the $m$ lowest frequencies', r'Cele mai mici pătrate în bandă îngustă (NBLS) \refRobA, \refCN: regresăm $y$ pe $x$ folosind doar cele mai joase $m$ frecvențe'
       ) + r'''
    \[ \hat\beta = \frac{\mathrm{Re}\sum_{j=1}^mI_{xy}(\lambda_j)}{\sum_{j=1}^mI_{xx}(\lambda_j)} \]''',
     [T(r'$I_{xy}$: cross-periodogram of $x$ and $y$; $I_{xx}$: periodogram of $x$; $\mathrm{Re}$: real part',
        r'$I_{xy}$: periodograma încrucișată a lui $x$ și $y$; $I_{xx}$: periodograma lui $x$; $\mathrm{Re}$: partea reală'),
      T('only the low frequencies, where the common long-memory component lives: robust to short-run correlation between $x$ and the error that biases OLS', 'doar frecvențele joase, acolo unde se află componenta comună cu memorie lungă: robust la corelația de termen scurt dintre $x$ și eroare, care deplasează OLS')]),
    (T(r'Rank by ELW \refNS: estimate $d$ of each series, test equal $d$, then count the small eigenvalues of the low-frequency spectral matrix', r'Rangul prin ELW \refNS: estimăm $d$ pentru fiecare serie, testăm egalitatea lui $d$, apoi numărăm valorile proprii mici ale matricei spectrale de frecvență joasă'),
     []),
    (T(r'Implied and realised variance \refBP: does the VIX contain the long-memory component of future realised variance?', r'Varianța implicită și cea realizată \refBP: conține VIX componenta cu memorie lungă a varianței realizate viitoare?'),
     [T('if $\\log RV$ and $\\log VIX^2$ share one fractional trend, a combination has lower $d$ and the VIX forecasts the persistent part', 'dacă $\\log RV$ și $\\log VIX^2$ au un trend fracționar comun, o combinație are $d$ mai mic, iar VIX prognozează partea persistentă')])), 'small')

chart(T('FCVAR: realised and implied variance', 'FCVAR: varianța realizată și cea implicită'), 'ats_ch10_fcvar', 'ATS_ch10_fcvar', [
    T(r'S\&P 500 log 5-minute RV and $\log(\mathrm{VIX}^2/252)$, $n = @{fc.n}$ common days to @{fc.end}; right: profile log-likelihood of the rank-one FCVAR with $k = 0$ over $(d, b)$, the 60 log-points below the maximum',
      r'Logaritmul RV de 5 minute pentru S\&P 500 și $\log(\mathrm{VIX}^2/252)$, $n = @{fc.n}$ zile comune pînă la @{fc.end}; dreapta: log-verosimilitatea profilată a FCVAR de rang unu cu $k = 0$ în $(d, b)$, ultimele 60 de puncte logaritmice sub maxim')], h='0.55\\textheight')

interp(('the FCVAR', 'modelului FCVAR'), [
    T(r'Local Whittle: $d$ = @{fc.d_rv} for log RV, @{fc.d_iv} for log VIX$^2$, @{fc.d_spread} for the spread $\beta\'X_t$ (SE @{fc.se}): the combination is less persistent', r'Local Whittle: $d$ = @{fc.d_rv} pentru logaritmul RV, @{fc.d_iv} pentru logaritmul VIX$^2$, @{fc.d_spread} pentru combinația $\beta\'X_t$ (SE @{fc.se}): combinația este mai puțin persistentă'),
    T(r'FCVAR: $\hat d = @{fc.d}$, $\hat b = @{fc.b}$, $\beta = (1, -@{fc.beta2})$, $\alpha = (@{fc.a1}, @{fc.a2})$: realised variance adjusts, the VIX does not (weak exogeneity)', r'FCVAR: $\hat d = @{fc.d}$, $\hat b = @{fc.b}$, $\beta = (1; -@{fc.beta2})$, $\alpha = (@{fc.a1}; @{fc.a2})$: varianța realizată se ajustează, VIX nu (exogenitate slabă)'),
    T(r'Trace tests ($\hat b < 1/2$, so $\chi^2$): rank 0 against 2: @{fc.trace0} ($p$ @{fc.p0}); rank 1 against 2: @{fc.trace1} ($p$ @{fc.p1}): with $k = 0$ the data also reject a single relation', r'Testele trace ($\hat b < 1/2$, deci $\chi^2$): rangul 0 față de 2: @{fc.trace0} ($p$ @{fc.p0}); rangul 1 față de 2: @{fc.trace1} ($p$ @{fc.p1}): cu $k = 0$ datele resping și ipoteza unei singure relații'),
    T(r'NBLS slope of log RV on log VIX$^2$: @{fc.nbls}, against $1/@{fc.beta2} = @{fc.ib}$ implied by FCVAR: short-run dynamics ($k > 0$) and the overnight gap of RV are left out; a project question', r'Panta NBLS a logaritmului RV pe logaritmul VIX$^2$: @{fc.nbls}, față de $1/@{fc.beta2} = @{fc.ib}$ implicată de FCVAR: dinamica de termen scurt ($k > 0$) și intervalul overnight al RV lipsesc; o întrebare de proiect')])

D.recap(('Fractional cointegration', 'cointegrarea fracționară'), [
    T('FCVAR generalises the VECM with two memory parameters $d$ and $b$, estimated by profile likelihood and reduced-rank regression', 'FCVAR generalizează VECM cu doi parametri de memorie, $d$ și $b$, estimați prin verosimilitate profilată și regresie de rang redus'),
    T('Rank tests are $\\chi^2$ only for $b < 1/2$; NBLS and ELW give semiparametric checks', 'Testele de rang sînt $\\chi^2$ doar pentru $b < 1/2$; NBLS și ELW dau verificări semiparametrice'),
    T('Realised and implied variance share persistent components; the exact structure needs short-run dynamics', 'Varianța realizată și cea implicită au componente persistente comune; structura exactă cere dinamica de termen scurt')])

# =============================================================================
# 5. MEMORIA LUNGĂ A VOLATILITĂȚII
# =============================================================================
D.section('Long memory in volatility', 'Memoria lungă a volatilității')

D.frame(T('FIGARCH (1/2): hyperbolic ARCH weights', 'FIGARCH (1/2): ponderi ARCH hiperbolice'), items(
    (T(r'GARCH(1,1) as ARCH($\infty$): the weights on past squared shocks decay geometrically', r'GARCH(1,1) ca ARCH($\infty$): ponderile pătratelor șocurilor trecute scad geometric'
       ) + r'''
    \[ \sigma_t^2 = \frac{\omega}{1 - \beta} + \sum_{k\ge1}\alpha\beta^{k-1}\varepsilon_{t-k}^2 \]''',
     []),
    (T(r'FIGARCH(1,$d$,1) \refBBM: a fractional difference makes them decay hyperbolically', r'FIGARCH(1,$d$,1) \refBBM: o diferență fracționară le face să scadă hiperbolic'
       ) + r'''
    \[ \sigma_t^2 = \frac{\omega}{1 - \beta} + \Big[1 - \frac{(1 - \phi L)(1 - L)^d}{1 - \beta L}\Big]\varepsilon_t^2 = \frac{\omega}{1 - \beta} + \sum_{k\ge1}\lambda_k\varepsilon_{t-k}^2 \]''',
     [T(r'$d \in (0, 1)$: memory of volatility; $\phi$, $\beta$: short-run ARCH and GARCH terms; $\lambda_k \sim c\,k^{-d-1}$: the ARCH($\infty$) weights',
        r'$d \in (0, 1)$: memoria volatilității; $\phi$, $\beta$: termenii ARCH și GARCH de termen scurt; $\lambda_k \sim c\,k^{-d-1}$: ponderile ARCH($\infty$)'),
      T(r'positivity of all $\lambda_k$ needs restrictions, e.g.\ $\beta - d \le \phi \le (2 - d)/3$', r'pozitivitatea tuturor $\lambda_k$ cere restricții, de exemplu $\beta - d \le \phi \le (2 - d)/3$')])), 'small')

D.frame(T('FIGARCH (2/2): the variance paradox and HYGARCH', 'FIGARCH (2/2): paradoxul varianței și HYGARCH'), items(
    (T(r'Paradox: $\sum_k\lambda_k = 1$, so $\E\varepsilon_t^2 = \infty$', r'Paradoxul: $\sum_k\lambda_k = 1$, deci $\E\varepsilon_t^2 = \infty$'),
     [T(r'FIGARCH is not covariance stationary for any $d > 0$, yet strictly stationary', r'FIGARCH nu este staționar în covarianță pentru niciun $d > 0$, deși este strict staționar'),
      T('the long memory of $\\varepsilon_t^2$ is therefore not defined by an autocovariance', 'memoria lungă a lui $\\varepsilon_t^2$ nu este deci definită printr-o autocovarianță')]),
    (T(r'HYGARCH \refDav: $(1 - L)^d$ is replaced by $1 + a\big((1 - L)^d - 1\big)$', r'HYGARCH \refDav: $(1 - L)^d$ este înlocuit cu $1 + a\big((1 - L)^d - 1\big)$'),
     [T(r'$a \ge 0$: amplitude of the hyperbolic part; $a < 1$ gives a finite variance and hyperbolic memory, $a = 1$ is FIGARCH, $a = 0$ is GARCH',
        r'$a \ge 0$: amplitudinea părții hiperbolice; $a < 1$ dă o varianță finită și memorie hiperbolică, $a = 1$ este FIGARCH, $a = 0$ este GARCH')])), 'small')

chart(T('ARCH weights: geometric and hyperbolic', 'Ponderi ARCH: geometrice și hiperbolice'), 'ats_ch10_figarch', 'ATS_ch10_figarch', [
    T(r'S\&P 500 daily returns 2000--2026 ($n = @{fg.sp500.n}$), Student $t$ QML, ARCH($\infty$) truncated at 1000 lags; GARCH $(\alpha, \beta) = (@{fg.sp500.ga}, @{fg.sp500.gb})$, FIGARCH $d = @{fg.sp500.d}$, $\phi = @{fg.sp500.phi}$, $\beta = @{fg.sp500.beta}$',
      r'Randamentele zilnice ale S\&P 500, 2000--2026 ($n = @{fg.sp500.n}$), QML cu distribuția Student $t$, ARCH($\infty$) trunchiat la 1000 de laguri; GARCH $(\alpha, \beta) = (@{fg.sp500.ga}; @{fg.sp500.gb})$, FIGARCH $d = @{fg.sp500.d}$, $\phi = @{fg.sp500.phi}$, $\beta = @{fg.sp500.beta}$')], h='0.65\\textheight')

D.frame(T('Interpreting the FIGARCH estimates', 'Interpretarea estimațiilor FIGARCH'), table(
    'lcccccc', T(r'\textbf{Market}', r'\textbf{Piața}') + r' & $\hat d$ & LR & $\hat a$ & BIC GARCH & BIC FIGARCH & ' + T('weight after lag 22', 'ponderea după lagul 22'),
    [f'{lab} & @{{fg.{k}.d}} & @{{fg.{k}.lr1}} & @{{fg.{k}.amp}} & @{{fg.{k}.bg}} & @{{fg.{k}.bf}} & @{{fg.{k}.w22f}}\\% / @{{fg.{k}.w22g}}\\%'
     for lab, k in (('S\\&P 500', 'sp500'), ('BET', 'bet'), ('Bitcoin', 'btc'))], size='scriptsize') + items(
    T(r'LR of FIGARCH against GARCH (one more parameter): @{fg.sp500.lr1}, @{fg.bet.lr1}, @{fg.btc.lr1}; BIC prefers FIGARCH in all three markets', r'LR pentru FIGARCH față de GARCH (un parametru în plus): @{fg.sp500.lr1}, @{fg.bet.lr1}, @{fg.btc.lr1}; BIC preferă FIGARCH pe toate cele trei piețe'),
    T(r'Weight on squared shocks older than 22 days: FIGARCH @{fg.sp500.w22f}\%, GARCH @{fg.sp500.w22g}\% (S\&P 500); after 250 days @{fg.sp500.w250f}\% against practically zero', r'Ponderea șocurilor pătratice mai vechi de 22 de zile: FIGARCH @{fg.sp500.w22f}\%, GARCH @{fg.sp500.w22g}\% (S\&P 500); după 250 de zile @{fg.sp500.w250f}\% față de practic zero'),
    T(r'HYGARCH amplitude $\hat a$ = @{fg.sp500.amp} and @{fg.bet.amp}: no evidence against $a = 1$ (LR @{fg.sp500.lr2} and @{fg.bet.lr2}); Bitcoin $\hat d = @{fg.btc.d}$ sits at the integrated edge', r'Amplitudinea HYGARCH $\hat a$ = @{fg.sp500.amp} și @{fg.bet.amp}: nicio evidență împotriva lui $a = 1$ (LR @{fg.sp500.lr2} și @{fg.bet.lr2}); pentru Bitcoin $\hat d = @{fg.btc.d}$ se află la marginea integrată'),
    T(r'LR: likelihood-ratio statistic of FIGARCH against GARCH; $\hat a$: HYGARCH amplitude; last column: FIGARCH / GARCH', r'LR: statistica raportului de verosimilitate pentru FIGARCH față de GARCH; $\hat a$: amplitudinea HYGARCH; ultima coloană: FIGARCH / GARCH')), 'footnotesize')

D.frame(T('Long-memory stochastic volatility and noise', 'Volatilitate stochastică cu memorie lungă și zgomot'), items(
    (T(r'LMSV \refBCL: log variance is a long-memory process; squaring and taking logs makes the model linear', r'LMSV \refBCL: logaritmul varianței este un proces cu memorie lungă; ridicarea la pătrat și logaritmarea fac modelul liniar'
       ) + r'''
    \[ r_t = \sigma_t\eta_t, \quad \log\sigma_t^2 = \mu + h_t \ \Rightarrow\ \log r_t^2 = \mu + \E\log\eta^2 + h_t + \xi_t \]''',
     [T(r'$h_t$: ARFIMA$(p,d,q)$; $\eta_t$: i.i.d. shock; $\xi_t = \log\eta_t^2 - \E\log\eta^2$: i.i.d.\ noise with variance $\pi^2/2$ for Gaussian $\eta$, often larger than $\Var(h_t)$',
        r'$h_t$: ARFIMA$(p,d,q)$; $\eta_t$: șoc i.i.d.; $\xi_t = \log\eta_t^2 - \E\log\eta^2$: zgomot i.i.d.\ cu varianța $\pi^2/2$ pentru $\eta$ gaussian, adesea mai mare decît $\Var(h_t)$')]),
    (T(r'Spectrum of $\log r_t^2$: a pole plus a flat noise floor', r'Spectrul lui $\log r_t^2$: un pol plus un nivel plat al zgomotului'
       ) + r'''
    \[ f(\lambda) = G\lambda^{-2d} + \frac{\sigma_\xi^2}{2\pi} \]''',
     [T(r'the flat noise flattens the low-frequency slope and biases $\hat d$ down', r'zgomotul plat aplatizează panta de frecvență joasă și deplasează $\hat d$ în jos'),
      T(r'LW with noise \refHMS: $f(\lambda) = G(\lambda^{-2d} + \theta)$, with the noise-to-signal ratio $\theta \ge 0$ estimated jointly; consistent, at a slower rate', r'LW cu zgomot \refHMS: $f(\lambda) = G(\lambda^{-2d} + \theta)$, cu raportul zgomot/semnal $\theta \ge 0$ estimat simultan; consistent, cu o viteză mai mică')]),
    T(r'Realised variance reduces the noise by averaging intraday returns \refABDL: $\log RV_t = \log IV_t + $ small error', r'Varianța realizată reduce zgomotul prin medierea randamentelor intraday \refABDL: $\log RV_t = \log IV_t + $ o eroare mică'),
    T(r'Continuous-time long memory in volatility: \refCR; the rough alternative follows in Section 6', r'Memoria lungă a volatilității în timp continuu: \refCR; alternativa rough volatility urmează în secțiunea 6')), 'small')

chart(T('Memory of volatility proxies across markets', 'Memoria proxy-urilor de volatilitate pe mai multe piețe'), 'ats_ch10_assets_d', 'ATS_ch10_figarch', [
    T(r'Local Whittle $\hat d$ with $m = n^{0.65}$ of $|r_t|$ and $\log(r_t^2 + c)$, $c$ = 1\% of the variance; LW with noise on $\log(r_t^2 + c)$ with $m = n^{0.8}$; log RV where realised measures exist (S\&P 500, DAX to 2022; Bitcoin to 2026)',
      r'$\hat d$ local Whittle cu $m = n^{0{,}65}$ pentru $|r_t|$ și $\log(r_t^2 + c)$, $c$ = 1\% din varianță; LW cu zgomot pentru $\log(r_t^2 + c)$ cu $m = n^{0{,}8}$; logaritmul RV acolo unde există măsuri realizate (S\&P 500, DAX pînă în 2022; Bitcoin pînă în 2026)')], h='0.59\\textheight')

interp(('volatility memory across markets', 'memoriei volatilității pe mai multe piețe'), [
    T(r'S\&P 500: $|r|$ @{ad.sp500.abs}, $\log r^2$ @{ad.sp500.lsq}, with noise @{ad.sp500.lwn}, log RV @{ad.sp500.rv}: the noise correction moves $\log r^2$ to the RV level', r'S\&P 500: $|r|$ @{ad.sp500.abs}, $\log r^2$ @{ad.sp500.lsq}, cu zgomot @{ad.sp500.lwn}, logaritmul RV @{ad.sp500.rv}: corecția de zgomot aduce $\log r^2$ la nivelul RV'),
    T(r'Bitcoin: $\log r^2$ @{ad.btc.lsq}, with noise @{ad.btc.lwn}, log RV @{ad.btc.rv}; DAX: @{ad.dax.lsq}, @{ad.dax.lwn}, @{ad.dax.rv}', r'Bitcoin: $\log r^2$ @{ad.btc.lsq}, cu zgomot @{ad.btc.lwn}, logaritmul RV @{ad.btc.rv}; DAX: @{ad.dax.lsq}, @{ad.dax.lwn}, @{ad.dax.rv}'),
    T(r'Qu test on $|r_t|$ (1\% value @{ad.c.99}): S\&P 500 @{ad.sp500.qu}, DAX @{ad.dax.qu}, Bitcoin @{ad.btc.qu}; BET @{ad.bet.qu} and EUR/RON @{ad.eurron.qu} reject', r'Testul Qu pe $|r_t|$ (valoarea de 1\%: @{ad.c.99}): S\&P 500 @{ad.sp500.qu}, DAX @{ad.dax.qu}, Bitcoin @{ad.btc.qu}; BET @{ad.bet.qu} și EUR/RON @{ad.eurron.qu} resping'),
    T('For the BET and the leu, part of the apparent memory comes from regime changes (2008, the managed float): model the breaks first (Chapter 2)', 'Pentru BET și leu, o parte a memoriei aparente vine din schimbări de regim (2008, regimul de managed float): modelați întîi rupturile (Capitolul 2)')])

D.frame(T('HAR as an approximation of long memory', 'HAR ca aproximare a memoriei lungi'), items(
    (T(r'HAR \refCor\ on $y = \log RV$ (Chapter 8)', r'HAR \refCor\ pentru $y = \log RV$ (Capitolul 8)'
       ) + r'''
    \[ y_{t+1} = \beta_0 + \beta_dy_t + \beta_w\bar y_t^{(5)} + \beta_m\bar y_t^{(22)} + u_{t+1} \]''',
     [T(r'$\bar y_t^{(5)}$, $\bar y_t^{(22)}$: averages of $y$ over the last 5 and 22 days; an AR(22) with three free slopes: a step-function approximation of hyperbolically decaying AR weights',
        r'$\bar y_t^{(5)}$, $\bar y_t^{(22)}$: mediile lui $y$ pe ultimele 5 și 22 de zile; un AR(22) cu trei pante libere: o aproximare în trepte a ponderilor AR cu descreștere hiperbolică')]),
    (T(r'Formally short memory: its ACF decays geometrically, but over horizons up to a few months it mimics $k^{2d-1}$', r'Formal, memorie scurtă: ACF scade geometric, dar pe orizonturi de pînă la cîteva luni imită $k^{2d-1}$'),
     [T('cascade interpretation: traders with daily, weekly and monthly horizons (heterogeneous market hypothesis)', 'interpretarea în cascadă: participanți cu orizonturi zilnice, săptămînale și lunare (ipoteza pieței eterogene)')]),
    T('Estimated by OLS, easy to extend (jumps, semivariances, Chapter 8): the benchmark every long-memory or rough model must beat', 'Estimat prin OLS, ușor de extins (salturi, semivarianțe, Capitolul 8): reperul pe care orice model cu memorie lungă sau de tip rough volatility trebuie să îl depășească')), 'small')

chart(T('HAR weights and the ACF it implies', 'Ponderile HAR și ACF implicată'), 'ats_ch10_har_approx', 'ATS_ch10_figarch', [
    T(r'S\&P 500 log RV; HAR by OLS: $\beta_d = @{har.bd}$, $\beta_w = @{har.bw}$, $\beta_m = @{har.bm}$; left: implied AR weights and ARFIMA $-\pi_k$ with $d = @{har.d}$; right: ACF of a long simulation of the fitted HAR and the sample ACF',
      r'Logaritmul RV pentru S\&P 500; HAR prin OLS: $\beta_d = @{har.bd}$, $\beta_w = @{har.bw}$, $\beta_m = @{har.bm}$; stînga: ponderile AR implicate și $-\pi_k$ ARFIMA cu $d = @{har.d}$; dreapta: ACF a unei simulări lungi a HAR estimat și ACF de eșantion')], h='0.54\\textheight')

interp(('the HAR approximation', 'aproximării HAR'), [
    T(r'Sum of HAR weights @{har.pers}: close to a unit root, which is how a short-memory model buys persistence', r'Suma ponderilor HAR @{har.pers}: aproape de o rădăcină unitară, așa își obține persistența un model de memorie scurtă'),
    T(r'ACF at lag 100: sample @{har.s.k100}, HAR @{har.h.k100}; at lag 250: @{har.s.k250} against @{har.h.k250}', r'ACF la lagul 100: eșantion @{har.s.k100}, HAR @{har.h.k100}; la 250: @{har.s.k250} față de @{har.h.k250}'),
    T(r'The implied ACF falls below half the sample ACF after lag @{har.half}: HAR captures memory up to about half a year', r'ACF implicată scade sub jumătatea ACF de eșantion după lagul @{har.half}: HAR captează memoria pînă la circa o jumătate de an'),
    T('For forecasts up to a month this is enough, which is why HAR is hard to beat (Section 7)', 'Pentru prognoze de pînă la o lună aceasta ajunge, de aceea HAR este greu de depășit (secțiunea 7)')])

D.recap(('Long memory in volatility', 'memoria lungă a volatilității'), [
    T('FIGARCH has hyperbolic ARCH weights but infinite variance; HYGARCH nests it', 'FIGARCH are ponderi ARCH hiperbolice, dar varianță infinită; HYGARCH îl include'),
    T('$\\log r_t^2$ is long memory plus large noise: use the noise-robust LW or realised measures', '$\\log r_t^2$ este memorie lungă plus zgomot mare: folosiți LW robust la zgomot sau măsurile realizate'),
    T('HAR is a short-memory model that mimics long memory over the horizons that matter for forecasting', 'HAR este un model cu memorie scurtă care imită memoria lungă pe orizonturile relevante pentru prognoză')])

# =============================================================================
# 6. ROUGH VOLATILITY
# =============================================================================
D.section('Rough volatility', 'Rough volatility')

D.frame(T('Fractional Brownian motion (1/2)', 'Mișcarea browniană fracționară (1/2)'), two(
    ph('kolmo', T('A. N. Kolmogorov', 'A. N. Kolmogorov'), h='0.25\\textheight') + '\\\\[1mm]' +
    ph('mandel', T('B. B. Mandelbrot, TED 2010', 'B. B. Mandelbrot, TED 2010'), h='0.15\\textheight'),
    items((T(r'fBm $W^H_t$ \refMVN: a centred Gaussian process with $W^H_0 = 0$ and covariance', r'fBm $W^H_t$ \refMVN: un proces gaussian centrat, cu $W^H_0 = 0$ și covarianța'
             ) + r'''
    \[ \E W^H_tW^H_s = \frac12\big(t^{2H} + s^{2H} - |t - s|^{2H}\big), \qquad H \in (0, 1) \]''',
           [T(r'$H$: the Hurst exponent; $H = 1/2$ gives standard Brownian motion', r'$H$: exponentul Hurst; $H = 1/2$ dă mișcarea browniană standard'),
            T(r'stationary increments with $\E|W^H_{t+\Delta} - W^H_t|^2 = \Delta^{2H}$', r'creșteri staționare, cu $\E|W^H_{t+\Delta} - W^H_t|^2 = \Delta^{2H}$'),
            T(r'self-similar: $W^H_{ct} \overset{d}{=} c^HW^H_t$ (equal in distribution) for $c > 0$', r'autosimilar: $W^H_{ct} \overset{d}{=} c^HW^H_t$ (egalitate în distribuție) pentru $c > 0$')])), '0.32', '0.66'), 'footnotesize')

D.frame(T('Fractional Brownian motion (2/2)', 'Mișcarea browniană fracționară (2/2)'), items(
    (T(r'Paths are Hölder continuous of every order $< H$', r'Traiectoriile sînt continue Hölder de orice ordin $< H$'),
     [T(r'Hölder order: how fast $|W^H_{t+\Delta} - W^H_t|$ can shrink with $\Delta$; $H < 1/2$: rougher (more irregular), $H > 1/2$: smoother than Brownian motion',
        r'ordinul Hölder: cît de repede poate scădea $|W^H_{t+\Delta} - W^H_t|$ cu $\Delta$; $H < 1/2$: traiectorii mai neregulate, $H > 1/2$: mai netede decît mișcarea browniană')]),
    (T(r'The increments, fractional Gaussian noise (fGn), have autocorrelations', r'Creșterile, zgomotul gaussian fracționar (fGn), au autocorelațiile'
       ) + r'''
    \[ \rho(k) = \frac12\big(|k + 1|^{2H} - 2|k|^{2H} + |k - 1|^{2H}\big) \sim H(2H - 1)k^{2H-2} \]''',
     [T(r'long memory for $H > 1/2$ ($d = H - 1/2$); negative correlation for $H < 1/2$', r'memorie lungă pentru $H > 1/2$ ($d = H - 1/2$); corelație negativă pentru $H < 1/2$')])), 'small')

chart(T('Fractional Brownian paths', 'Traiectorii browniene fracționare'), 'ats_ch10_fbm_paths', 'ATS_ch10_simulation', [
    T(r'One path each on 1000 steps, exact simulation by circulant embedding; $H = 0.5$ is Brownian motion', r'O traiectorie pentru fiecare valoare, pe 1000 de pași, simulare exactă prin scufundare circulantă; $H = 0{,}5$ este mișcarea browniană')], h='0.65\\textheight')

interp(('the paths', 'traiectoriilor'), [
    T(r'Lag-one correlation of the increments: @{fb.1} for $H = 0.1$, @{fb.3} for $H = 0.3$, 0 for $H = 0.5$, @{fb.7} for $H = 0.7$', r'Corelația de ordinul unu a creșterilor: @{fb.1} pentru $H = 0{,}1$, @{fb.3} pentru $H = 0{,}3$, 0 pentru $H = 0{,}5$, @{fb.7} pentru $H = 0{,}7$'),
    T(r'$H = 0.1$: every rise is likely to be followed by a fall, so the path is jagged at all scales but wanders little', r'$H = 0{,}1$: fiecare creștere este probabil urmată de o scădere, deci traiectoria este zimțată la toate scările, dar se abate puțin'),
    T(r'$H = 0.7$: trends persist; this is the fBm reading of the Hurst effect', r'$H = 0{,}7$: trendurile persistă; aceasta este lectura fBm a efectului Hurst'),
    T('Roughness is a statement about small scales, persistence about large ones: keep the two apart', 'Neregularitatea este o afirmație despre scările mici, persistența despre cele mari: păstrați-le separate')])

D.frame(T('Simulating fBm: Cholesky, circulant embedding', 'Simularea fBm: Cholesky, scufundarea circulantă'), items(
    (T(r'Cholesky: $\Gamma = LL\'$, $X = LZ$; exact but $O(n^3)$ time and $O(n^2)$ memory', r'Cholesky: $\Gamma = LL\'$, $X = LZ$; exact, dar cu timp $O(n^3)$ și memorie $O(n^2)$'),
     [T(r'$\Gamma$: the $n \times n$ covariance matrix of the path; $L$: its lower-triangular Cholesky factor; $Z$: a vector of i.i.d. $N(0, 1)$',
        r'$\Gamma$: matricea de covarianță $n \times n$ a traiectoriei; $L$: factorul ei Cholesky inferior triunghiular; $Z$: un vector de variabile i.i.d. $N(0, 1)$')]),
    (T(r'Davies--Harte \refDH, \refDN: embed the Toeplitz $\Gamma$ of fGn in a circulant matrix of order $M = 2(n - 1)$ with first row $c = (\gamma_0, \dots, \gamma_{n-1}, \gamma_{n-2}, \dots, \gamma_1)$', r'Davies--Harte \refDH, \refDN: scufundăm matricea Toeplitz $\Gamma$ a fGn într-o matrice circulantă de ordin $M = 2(n - 1)$, cu primul rînd $c = (\gamma_0, \dots, \gamma_{n-1}, \gamma_{n-2}, \dots, \gamma_1)$'),
     [T(r'$\gamma_k$: autocovariances of fGn; a circulant matrix is diagonalised by the discrete Fourier transform: eigenvalues $\Lambda = \mathrm{FFT}(c)$', r'$\gamma_k$: autocovarianțele fGn; o matrice circulantă este diagonalizată de transformata Fourier discretă: valorile proprii $\Lambda = \mathrm{FFT}(c)$'),
      T(r'if $\Lambda \ge 0$: $Y = \mathrm{FFT}\big(\sqrt{\Lambda/M}\,(Z_1 + iZ_2)\big)$, $Z_1, Z_2$ independent standard Gaussian vectors; $\mathrm{Re}\,Y$ and $\mathrm{Im}\,Y$ are two independent exact paths', r'dacă $\Lambda \ge 0$: $Y = \mathrm{FFT}\big(\sqrt{\Lambda/M}\,(Z_1 + iZ_2)\big)$, cu $Z_1, Z_2$ vectori gaussieni standard independenți; $\mathrm{Re}\,Y$ și $\mathrm{Im}\,Y$ sînt două traiectorii exacte independente')]),
    (T(r'$O(n\log n)$; for fGn $\Lambda \ge 0$ for every $H$ (Seminar 10, A7); fBm = cumulated fGn', r'$O(n\log n)$; pentru fGn $\Lambda \ge 0$ pentru orice $H$ (Seminarul 10, A7); fBm = fGn cumulat'), []),
    T('The same algorithm simulates ARFIMA$(0,d,0)$ exactly (used in every Monte Carlo of this chapter)', 'Același algoritm simulează exact ARFIMA$(0,d,0)$ (folosit în fiecare experiment Monte Carlo din acest capitol)')), 'small')

D.frame(T('The hybrid scheme for Volterra processes', 'Schema hibridă pentru procesele Volterra'), items(
    (T(r'Rough volatility models use Volterra processes, not stationary-increment fBm \refBFG', r'Modelele de rough volatility folosesc procese Volterra, nu fBm cu creșteri staționare \refBFG'
       ) + r'''
    \[ X_t = \int_0^tg(t - s)\,dW_s, \qquad g(x) = x^{H-1/2} \ \ \text{(Riemann--Liouville)} \]''',
     [T(r'$g$: the kernel, singular at 0 when $H < 1/2$; $W$: Brownian motion; circulant embedding does not apply (non-stationary, possibly non-Gaussian when driven by a correlated price)',
        r'$g$: nucleul, singular în 0 cînd $H < 1/2$; $W$: mișcarea browniană; scufundarea circulantă nu se aplică (proces nestaționar, posibil negaussian cînd este cuplat cu un preț corelat)')]),
    (T(r'Hybrid scheme \refBLPa: integrate the kernel exactly on the last step, use a Riemann sum at optimal points further away', r'Schema hibridă \refBLPa: integrăm nucleul exact pe ultimul pas și folosim o sumă Riemann în puncte optime mai departe'
       ) + r'''
    \[ X_i \approx \int_{t_{i-1}}^{t_i}(t_i - s)^{H-1/2}dW_s + \sum_{k\ge2}\Big(\frac{b_k}{n}\Big)^{H-1/2}\Delta W_{i-k+1} \]
    \[ b_k = \Big(\frac{k^{H+1/2} - (k - 1)^{H+1/2}}{H + 1/2}\Big)^{1/(H-1/2)} \]''',
     [T(r'$n$: steps per unit of time; $\Delta W_i$: Brownian increments; $b_k$: the optimal evaluation point in cell $k$; the first term and $\Delta W_i$ are jointly Gaussian and simulated exactly',
        r'$n$: numărul de pași pe unitatea de timp; $\Delta W_i$: creșterile browniene; $b_k$: punctul optim de evaluare din celula $k$; primul termen și $\Delta W_i$ sînt gaussiene împreună și se simulează exact')]),
    T('The sum is a convolution: $O(n\\log n)$ by FFT; the scheme extends to Brownian semistationary processes', 'Suma este o convoluție: $O(n\\log n)$ prin FFT; schema se extinde la procesele browniene semistaționare')), 'footnotesize')

chart(T('Riemann sum against the hybrid scheme', 'Suma Riemann și schema hibridă'), 'ats_ch10_hybrid', 'ATS_ch10_simulation', [
    T(r'$\Var X(1)$ of the Riemann--Liouville process, exact value $1/(2H)$; $n = @{hy.n}$ steps, @{hy.paths} paths', r'$\Var X(1)$ pentru procesul Riemann--Liouville, valoarea exactă $1/(2H)$; $n = @{hy.n}$ pași, @{hy.paths} de traiectorii')], h='0.67\\textheight')

interp(('the simulation schemes', 'schemelor de simulare'), [
    T(r'Forward Riemann sum: @{hy.r05} of the true variance at $H = 0.05$ and @{hy.r1} at $H = 0.1$: it misses the mass of the kernel near the singularity', r'Suma Riemann înainte: @{hy.r05} din varianța adevărată la $H = 0{,}05$ și @{hy.r1} la $H = 0{,}1$: ratează masa nucleului de lîngă singularitate'),
    T(r'Hybrid scheme: @{hy.h05} and @{hy.h1}, within Monte Carlo error of 1', r'Schema hibridă: @{hy.h05} și @{hy.h1}, în limita erorii Monte Carlo față de 1'),
    T('The error of the naive scheme grows exactly where rough volatility lives ($H \\approx 0.1$): option prices from it would be biased', 'Eroarea schemei naive crește exact acolo unde se află rough volatility ($H \\approx 0{,}1$): prețurile opțiunilor obținute cu ea ar fi deplasate')])

D.frame(T('The evidence: scaling of log volatility (1/2)', 'Evidența: scalarea logaritmului volatilității (1/2)'), items(
    (T(r'\refGJR, Section 2: from daily $\sigma_t = \sqrt{RV_t}$ (Oxford-Man library), the empirical moments of the increments of $\log\sigma$', r'\refGJR, secțiunea 2: din $\sigma_t = \sqrt{RV_t}$ zilnic (biblioteca Oxford-Man), momentele empirice ale creșterilor lui $\log\sigma$'
       ) + r'''
    \[ m(q, \Delta) = \frac1N\sum_t|\log\sigma_{t+\Delta} - \log\sigma_t|^q \]''',
     [T(r'$\Delta$: lag in days; $q > 0$: order of the moment; $N$: number of pairs; $m(2, \Delta)$ is the variogram',
        r'$\Delta$: lagul în zile; $q > 0$: ordinul momentului; $N$: numărul de perechi; $m(2, \Delta)$ este variograma')]),
    (T(r'If $\log\sigma$ has fBm-like increments, the moments scale as a power of $\Delta$ (monofractal scaling)', r'Dacă $\log\sigma$ are creșteri de tip fBm, momentele se scalează ca o putere a lui $\Delta$ (scalare monofractală)'
       ) + r'''
    \[ m(q, \Delta) = K_q\nu^q\Delta^{\zeta_q}, \qquad \zeta_q = qH \]''',
     [T(r'$\nu$: volatility of volatility; $K_q = \E|Z|^q$, $Z \sim N(0, 1)$; $\zeta_q$: scaling exponent, linear in $q$ with slope $H$',
        r'$\nu$: volatilitatea volatilității; $K_q = \E|Z|^q$, $Z \sim N(0, 1)$; $\zeta_q$: exponentul de scalare, liniar în $q$, cu panta $H$'),
      T('derivation and deviations from this scaling: Appendix  % applink: scaling of fBm moments', 'derivarea și abaterile de la această scalare: Anexa  % applink: scalarea momentelor fBm')])), 'small')

D.frame(T('The evidence: scaling of log volatility (2/2)', 'Evidența: scalarea logaritmului volatilității (2/2)'), items(
    (T(r'Procedure: OLS of $\log m(q, \Delta)$ on $\log\Delta$ for each $q$ gives $\zeta_q$; regress $\zeta_q$ on $q$ through the origin to get $H$', r'Procedura: OLS al lui $\log m(q, \Delta)$ pe $\log\Delta$ pentru fiecare $q$ dă $\zeta_q$; regresăm $\zeta_q$ pe $q$ prin origine pentru a obține $H$'),
     [T(r'we use $q \in \{0.5, 1, 1.5, 2, 3\}$ and $\Delta = 1, \dots, 50$ days', r'folosim $q \in \{0{,}5; 1; 1{,}5; 2; 3\}$ și $\Delta = 1, \dots, 50$ de zile')]),
    T(r'Their finding: linear $\zeta_q$ and $H$ of order 0.1 for all indices; the increments of log volatility are close to Gaussian', r'Rezultatul lor: $\zeta_q$ liniar și $H$ de ordinul 0,1 pentru toți indicii; creșterile logaritmului volatilității sînt apropiate de distribuția Normală'),
    T(r'This contradicts every Markovian SV model (Heston, log-OU), whose log volatility has $H = 1/2$ at short lags', r'Aceasta contrazice orice model SV markovian (Heston, log-OU), al cărui logaritm al volatilității are $H = 1/2$ la laguri scurte')), 'small')

chart(T('Replicating the scaling on the S\\&P 500', 'Replicarea scalării pe S\\&P 500'), 'ats_ch10_gjr', 'ATS_ch10_rough', [
    T(r'Oxford-Man 5-minute RV of the S\&P 500, January 2000 -- February 2022; left: $\log m(q, \Delta)$ and OLS lines; right: $\zeta_q$ and the line $qH$',
      r'RV de 5 minute Oxford-Man pentru S\&P 500, ianuarie 2000 -- februarie 2022; stînga: $\log m(q, \Delta)$ și dreptele OLS; dreapta: $\zeta_q$ și dreapta $qH$')], h='0.54\\textheight')

interp(('the scaling', 'scalării'), [
    T(r'$\zeta_q$ = @{gj.z0}, @{gj.z1}, @{gj.z2}, @{gj.z3}, @{gj.z4} for $q$ = 0.5, 1, 1.5, 2, 3: linear in $q$, $\hat H = @{gj.H}$', r'$\zeta_q$ = @{gj.z0}; @{gj.z1}; @{gj.z2}; @{gj.z3}; @{gj.z4} pentru $q$ = 0,5; 1; 1,5; 2; 3: liniar în $q$, $\hat H = @{gj.H}$'),
    T(r'Vol-of-vol $\hat\nu = @{gj.nu}$ from $m(2, \Delta) = \nu^2\Delta^{2H}$; subsamples: @{gj.s1} (2000--2010), @{gj.s2} (2011--2022)', r'Volatilitatea volatilității $\hat\nu = @{gj.nu}$ din $m(2, \Delta) = \nu^2\Delta^{2H}$; subeșantioane: @{gj.s1} (2000--2010), @{gj.s2} (2011--2022)'),
    T(r'The paper\'s result replicates: roughly $H \approx 0.1$ to 0.15, stable over time', r'Rezultatul lucrării se replică: aproximativ $H \approx 0{,}1$--0,15, stabil în timp')])

D.frame(T('The RFSV model', 'Modelul RFSV'), items(
    (T(r'\refGJR: rough fractional stochastic volatility (RFSV), log volatility a fractional Ornstein--Uhlenbeck (OU) process', r'\refGJR: rough fractional stochastic volatility (RFSV), logaritmul volatilității este un proces Ornstein--Uhlenbeck (OU) fracționar'
       ) + r'''
    \[ \sigma_t = \exp(X_t), \qquad dX_t = \nu\,dW^H_t - \alpha(X_t - m)\,dt, \qquad H < 1/2 \]''',
     [T(r'$\nu$: volatility of volatility; $m$: long-run mean of $X$; $\alpha > 0$: speed of mean reversion, very small',
        r'$\nu$: volatilitatea volatilității; $m$: media de termen lung a lui $X$; $\alpha > 0$: viteza revenirii la medie, foarte mică'),
      T(r'for $\alpha T \ll 1$ ($T$: sample span) the increments behave like those of $\nu W^H$; stationarity only shows at horizons of order $1/\alpha$', r'pentru $\alpha T \ll 1$ ($T$: lungimea eșantionului) creșterile se comportă ca ale lui $\nu W^H$; staționaritatea apare doar pe orizonturi de ordinul $1/\alpha$')]),
    (T(r'The link with long memory: over observable horizons $\log\sigma$ is close to a non-stationary fBm with $H \approx 0.1$, whose ARFIMA reading is $d = H + 1/2$ (@{gj.dH} for the S\&P 500, close to the local Whittle $\hat d$ of log RV)', r'Legătura cu memoria lungă: pe orizonturile observabile, $\log\sigma$ este aproape de o fBm nestaționară cu $H \approx 0{,}1$, a cărei lectură ARFIMA este $d = H + 1/2$ (@{gj.dH} pentru S\&P 500, aproape de $\hat d$ local Whittle al logaritmului RV)'),
     [T('GJR show that local Whittle and similar estimators applied to RFSV simulations return the ``long-memory\'\' values found in the literature', 'GJR arată că local Whittle și estimatori similari aplicați simulărilor RFSV dau valorile de „memorie lungă” găsite în literatură')]),
    (T(r'Pricing: rough Bergomi \refBFG\ and rough Heston \refER', r'Evaluarea opțiunilor: rough Bergomi \refBFG\ și rough Heston \refER'),
     [T(r'both fit the term structure of the implied-volatility skew, $\propto \tau^{H-1/2}$ ($\tau$: option maturity), with few parameters',
        r'ambele reproduc structura la termen a pantei volatilității implicite, $\propto \tau^{H-1/2}$ ($\tau$: scadența opțiunii), cu puțini parametri'),
      T(r'option-based estimates also give small $H$ \refLMPR', r'estimările din opțiuni dau tot $H$ mic \refLMPR'),
      T('the pricing side belongs to MFM; here we test the time-series claim', 'partea de evaluare aparține MFM; aici testăm afirmația de serie de timp')])), 'small')

chart(T('Roughness across markets and proxies', 'Neregularitatea pe mai multe piețe și proxy-uri'), 'ats_ch10_gjr_assets', 'ATS_ch10_rough', [
    T(r'$H$ from 5-minute RV (Oxford-Man; Bitcoin: Binance) by the moment regression and with a measurement-error intercept; Parkinson range of EODHD daily highs and lows over the same days, where available',
      r'$H$ din RV de 5 minute (Oxford-Man; Bitcoin: Binance) prin regresia momentelor și cu un termen liber pentru eroarea de măsurare; amplitudinea Parkinson din maximele și minimele zilnice EODHD pe aceleași zile, acolo unde există')], h='0.59\\textheight')

interp(('roughness across markets', 'neregularității pe mai multe piețe'), [
    T(r'RV: $H$ from @{ga.min} to @{ga.max} for six indices and Bitcoin (S\&P 500 @{ga.spx.H}, DAX @{ga.dax.H}, Euro Stoxx 50 @{ga.sx.H}, Bitcoin @{ga.btc.H})', r'RV: $H$ între @{ga.min} și @{ga.max} pentru șase indici și Bitcoin (S\&P 500 @{ga.spx.H}, DAX @{ga.dax.H}, Euro Stoxx 50 @{ga.sx.H}, Bitcoin @{ga.btc.H})'),
    T(r'The error intercept changes little (S\&P 500 @{ga.spx.Hn}); only for the FTSE 100 does it absorb @{ga.ftsesh}\% of $m(2, 1)$', r'Termenul liber pentru eroare schimbă puțin (S\&P 500 @{ga.spx.Hn}); doar pentru FTSE 100 absoarbe @{ga.ftsesh}\% din $m(2, 1)$'),
    T(r'Parkinson range, a much noisier proxy: S\&P 500 @{ga.spx.Hp}, DAX @{ga.dax.Hp}; with the intercept @{ga.spx.Hpn} and @{ga.dax.Hpn} (noise share @{ga.spx.sh}\% and @{ga.dax.sh}\%)', r'Amplitudinea Parkinson, un proxy mult mai zgomotos: S\&P 500 @{ga.spx.Hp}, DAX @{ga.dax.Hp}; cu termenul liber @{ga.spx.Hpn} și @{ga.dax.Hpn} (ponderea zgomotului @{ga.spx.sh}\% și @{ga.dax.sh}\%)'),
    T('Measurement error pushes $H$ down; the correction brings the range back near the RV estimate, but not above it', 'Eroarea de măsurare împinge $H$ în jos; corecția aduce amplitudinea aproape de estimația din RV, dar nu peste ea')])

D.frame(T('Critiques: is roughness an artefact?', 'Critici: este neregularitatea un artefact?'), items(
    (T(r'RV is an estimate of integrated variance: $\log RV_t = \log\int_{t-1}^t\sigma_s^2ds + \epsilon_t$', r'RV este o estimație a varianței integrate: $\log RV_t = \log\int_{t-1}^t\sigma_s^2ds + \epsilon_t$'),
     [T(r'two opposite biases: daily integration smooths (pushes $\hat H$ up), the error $\epsilon_t$ adds a nugget to $m(2, \Delta)$ (pushes $\hat H$ down)', r'două deplasări opuse: integrarea pe zi netezește (împinge $\hat H$ în sus), eroarea $\epsilon_t$ adaugă un salt la origine în $m(2, \Delta)$ (împinge $\hat H$ în jos)')]),
    (T(r'\refFTW: a Whittle-type estimator consistent under high-frequency asymptotics with measurement error; volatility remains rough, $H$ even below 0.1', r'\refFTW: un estimator de tip Whittle consistent sub asimptotica de înaltă frecvență cu eroare de măsurare; volatilitatea rămîne neregulată, $H$ chiar sub 0,1'),
     [T(r'\refBCPV: GMM on the moments of integrated variance with noise; also small $H$', r'\refBCPV: GMM pe momentele varianței integrate cu zgomot; tot $H$ mic')]),
    (T(r'\refCD: the roughness estimators applied to RV can report small $H$ even for smooth (Markovian) volatility: a finite-sample artefact of the proxy', r'\refCD: estimatorii neregularității aplicați RV pot raporta $H$ mic chiar și pentru o volatilitate netedă (markoviană): un artefact de eșantion finit al proxy-ului'),
     [T('the answer depends on the size of the error relative to the daily variation of log volatility: simulate it', 'răspunsul depinde de mărimea erorii față de variația zilnică a logaritmului volatilității: simulați-o')])), 'small')

chart(T('Measurement error and the estimate of $H$', 'Eroarea de măsurare și estimația lui $H$'), 'ats_ch10_noise_sim', 'ATS_ch10_rough', [
    T(r'Log volatility a fractional OU on 78 intraday steps a day, @{nz.days} days, @{nz.reps} replications; daily IV (no error) and RV from the 78 squared returns; GJR estimator',
      r'Logaritmul volatilității este un OU fracționar pe 78 de pași intraday pe zi, @{nz.days} de zile, @{nz.reps} replicări; IV zilnic (fără eroare) și RV din cele 78 de randamente pătratice; estimatorul GJR')], h='0.65\\textheight')

interp(('the simulation', 'simulării'), [
    T(r'True $H = 0.1$: from IV @{nz.1.iv}, from RV @{nz.1.rv}, RV with intercept @{nz.1.rvn}: the integration bias and the error bias almost cancel', r'$H$ adevărat $= 0{,}1$: din IV @{nz.1.iv}, din RV @{nz.1.rv}, RV cu termen liber @{nz.1.rvn}: deplasarea de integrare și cea de eroare aproape se anulează'),
    T(r'True $H = 0.5$: IV @{nz.5.iv}, RV @{nz.5.rv}, with intercept @{nz.5.rvn}; true $H = 0.3$: @{nz.3.iv}, @{nz.3.rv}, @{nz.3.rvn}', r'$H$ adevărat $= 0{,}5$: IV @{nz.5.iv}, RV @{nz.5.rv}, cu termen liber @{nz.5.rvn}; $H$ adevărat $= 0{,}3$: @{nz.3.iv}, @{nz.3.rv}, @{nz.3.rvn}'),
    T('With 5-minute RV the error is too small to turn $H = 0.5$ into the 0.1--0.15 seen in the data', 'Cu RV de 5 minute, eroarea este prea mică pentru a transforma $H = 0{,}5$ în valorile 0,1--0,15 observate în date'),
    T('A noisier proxy (Parkinson, squared returns) or a different volatility model could; the conclusion is conditional on this design', 'Un proxy mai zgomotos (Parkinson, randamente pătratice) sau un alt model de volatilitate ar putea; concluzia depinde de această schemă')])

D.frame(T('Roughness and persistence', 'Neregularitate și persistență'), items(
    (T(r'In fBm one parameter fixes both: small $H$ means rough paths and (for increments) antipersistence', r'În fBm un singur parametru le fixează pe amîndouă: $H$ mic înseamnă traiectorii neregulate și (pentru creșteri) antipersistență'),
     [T(r'Cauchy and gamma-kernel models separate the fractal dimension (short scales) from the Hurst effect (long scales) \refGS', r'modelele Cauchy și cu nucleu gamma separă dimensiunea fractală (scări mici) de efectul Hurst (scări mari) \refGS')]),
    (T(r'\refBLPb: Brownian semistationary model $X_t = \int_{-\infty}^tg(t - s)\,dW_s$, $g(x) \approx x^\alpha$ near 0 (roughness, $H = \alpha + 1/2$), $g(x) \approx x^{-\beta}$ at infinity (memory)', r'\refBLPb: modelul brownian semistaționar $X_t = \int_{-\infty}^tg(t - s)\,dW_s$, $g(x) \approx x^\alpha$ lîngă 0 (neregularitate, $H = \alpha + 1/2$), $g(x) \approx x^{-\beta}$ la infinit (memorie)'),
     [T('their finding: log volatility is both rough ($\\alpha < 0$) and persistent ($\\beta < 1$); the two are estimated separately', 'rezultatul lor: logaritmul volatilității este atît neregulat ($\\alpha < 0$), cît și persistent ($\\beta < 1$); cele două se estimează separat')]),
    T(r'Empirical check: slope of the variogram at short lags against the decay of the ACF at long lags', r'Verificarea empirică: panta variogramei la laguri scurte față de descreșterea ACF la laguri lungi')), 'small')

chart(T('Short scales and long scales', 'Scări mici și scări mari'), 'ats_ch10_decouple', 'ATS_ch10_rough', [
    T(r'S\&P 500 log volatility, lags 1--1000 days; left: variogram $m(2, \Delta)$ with slopes on lags 1--10 and 100--1000; right: sample ACF with a $k^{2d-1}$ fit on lags 10--250',
      r'Logaritmul volatilității pentru S\&P 500, laguri 1--1000 de zile; stînga: variograma $m(2, \Delta)$ cu pantele pe lagurile 1--10 și 100--1000; dreapta: ACF de eșantion cu o ajustare $k^{2d-1}$ pe lagurile 10--250')], h='0.54\\textheight')

interp(('the two scales', 'celor două scări'), [
    T(r'Short lags: slope $2H = @{dc.2H}$, $H = @{dc.H}$; long lags: slope @{dc.sl}, still rising at 1000 days, above $2\Var(\log\sigma)$', r'Laguri scurte: panta $2H = @{dc.2H}$, $H = @{dc.H}$; laguri lungi: panta @{dc.sl}, încă în creștere la 1000 de zile, peste $2\Var(\log\sigma)$'),
    T(r'Read as a non-stationary fractional process, the long-lag slope $2d - 1$ gives $d = @{dc.dl}$; local Whittle with $m = @{dc.mlw}$ gives @{dc.dlw}', r'Citită ca proces fracționar nestaționar, panta la laguri lungi $2d - 1$ dă $d = @{dc.dl}$; local Whittle cu $m = @{dc.mlw}$ dă @{dc.dlw}'),
    T(r'The ACF fit gives only $d = @{dc.dacf}$: the sample ACF is biased down when $d$ is near or above 1/2', r'Ajustarea ACF dă doar $d = @{dc.dacf}$: ACF de eșantion este deplasată în jos cînd $d$ este aproape de 1/2 sau peste'),
    T('Rough at short scales, highly persistent at long scales: both claims hold for the same series', 'Neregulată la scări mici, foarte persistentă la scări mari: ambele afirmații sînt valabile pentru aceeași serie')])

D.recap(('Rough volatility', 'rough volatility'), [
    T('fBm with $H < 1/2$: rough paths; simulate it exactly by circulant embedding, Volterra versions by the hybrid scheme', 'fBm cu $H < 1/2$: traiectorii neregulate; se simulează exact prin scufundare circulantă, versiunile Volterra prin schema hibridă'),
    T('The scaling of log RV gives $H \\approx 0.1$--0.15 on every market we tried, stable over time', 'Scalarea logaritmului RV dă $H \\approx 0{,}1$--0,15 pe toate piețele încercate, stabil în timp'),
    T('Measurement error and daily integration bias $\\hat H$ in opposite directions; roughness and persistence are separate properties', 'Eroarea de măsurare și integrarea zilnică deplasează $\\hat H$ în direcții opuse; neregularitatea și persistența sînt proprietăți separate')])

# =============================================================================
# 7. PROGNOZA
# =============================================================================
D.section('Forecasting realised variance: rough, long memory, HAR', 'Prognoza varianței realizate: rough volatility, memorie lungă, HAR')

D.frame(T('The RFSV predictor (1/2)', 'Predictorul RFSV (1/2)'), items(
    (T(r'For fBm (Nuzman--Poor), with $\alpha \approx 0$, \refGJR, Section 5: the forecast of log variance is a weighted average of its past', r'Pentru fBm (Nuzman--Poor), cu $\alpha \approx 0$, \refGJR, secțiunea 5: prognoza logaritmului varianței este o medie ponderată a trecutului său'
       ) + r'''
    \[ \E[\log\sigma^2_{t+h} \mid \mathcal F_t] = \frac{\cos(H\pi)}{\pi}\,h^{H+1/2}\int_{-\infty}^t\frac{\log\sigma_s^2}{(t - s + h)(t - s)^{H+1/2}}\,ds \]''',
     [T(r'$h$: forecast horizon; $\mathcal F_t$: the past of volatility up to $t$; the kernel integrates to one, with more weight on the recent past for small $H$',
        r'$h$: orizontul prognozei; $\mathcal F_t$: trecutul volatilității pînă la $t$; nucleul are integrala unu, cu mai multă pondere pe trecutul recent pentru $H$ mic'),
      T('discretised on days: $w_k = \\int_k^{k+1}du/((u + h)u^{H+1/2})$, truncated at 500 days and normalised', 'discretizat pe zile: $w_k = \\int_k^{k+1}du/((u + h)u^{H+1/2})$, trunchiat la 500 de zile și normalizat')])), 'small')

D.frame(T('The RFSV predictor (2/2): the variance forecast', 'Predictorul RFSV (2/2): prognoza varianței'), items(
    (T(r'From log variance to variance: a lognormal correction', r'De la logaritmul varianței la varianță: o corecție lognormală'
       ) + r'''
    \[ \E[\sigma^2_{t+h} \mid \mathcal F_t] = \exp\big(\E[\log\sigma^2_{t+h} \mid \mathcal F_t] + 2c\nu^2h^{2H}\big) \]
    \[ c = \frac{\Gamma(3/2 - H)}{\Gamma(H + 1/2)\Gamma(2 - 2H)} \]''',
     [T(r'$2c\nu^2h^{2H}$: half the conditional variance of $\log\sigma^2_{t+h}$, which grows with the horizon; with the S\&P 500 values $c = @{gj.c}$',
        r'$2c\nu^2h^{2H}$: jumătate din varianța condiționată a lui $\log\sigma^2_{t+h}$, care crește cu orizontul; cu valorile pentru S\&P 500, $c = @{gj.c}$')]),
    T('Two parameters ($H$, $\\nu$), both from the variogram: no likelihood, no optimisation', 'Doi parametri ($H$, $\\nu$), ambii din variogramă: fără verosimilitate, fără optimizare')), 'small')

chart(T('How far back the forecasts look', 'Cît de departe privesc prognozele'), 'ats_ch10_rfsv_kernel', 'ATS_ch10_forecast', [
    T(r'RFSV kernel with $H = @{kr.H}$ (S\&P 500) for $h = 1$ and $h = 22$ days, against the normalised HAR weights for $h = 1$', r'Nucleul RFSV cu $H = @{kr.H}$ (S\&P 500) pentru $h = 1$ și $h = 22$ de zile, față de ponderile HAR normalizate pentru $h = 1$')], h='0.64\\textheight')

interp(('the kernels', 'nucleelor'), [
    T(r'$h = 1$: RFSV puts @{kr.1.w1}\% on the last day, @{kr.1.w5}\% on the last week, @{kr.1.w22}\% on the last month; HAR: @{kr.har.w1}\% and @{kr.har.w5}\%', r'$h = 1$: RFSV pune @{kr.1.w1}\% pe ultima zi, @{kr.1.w5}\% pe ultima săptămînă, @{kr.1.w22}\% pe ultima lună; HAR: @{kr.har.w1}\% și @{kr.har.w5}\%'),
    T(r'$h = 22$: only @{kr.22.w1}\% on the last day, @{kr.22.w22}\% on the last month, @{kr.22.w100}\% within 100 days: longer horizons look further back', r'$h = 22$: doar @{kr.22.w1}\% pe ultima zi, @{kr.22.w22}\% pe ultima lună, @{kr.22.w100}\% în ultimele 100 de zile: orizonturile mai lungi privesc mai departe în trecut'),
    T('The kernel adapts its memory to the horizon automatically; HAR needs a separate regression for each horizon', 'Nucleul își adaptează automat memoria la orizont; HAR cere o regresie separată pentru fiecare orizont'),
    T('RFSV has no mean reversion: in long calm periods it does not pull forecasts towards a long-run level', 'RFSV nu are revenire la medie: în perioadele calme lungi nu trage prognozele spre un nivel de termen lung')])

D.frame(T('An honest out-of-sample comparison', 'O comparație riguroasă în afara eșantionului'), items(
    (T(r'Design fixed in advance: rolling window of 1000 days, parameters re-estimated every 20 days with data up to $t$ only; target $RV_{t+h}$, $h \in \{1, 5, 22\}$', r'Schema fixată dinainte: fereastră mobilă de 1000 de zile, parametrii reestimați la fiecare 20 de zile doar cu datele pînă la $t$; ținta $RV_{t+h}$, $h \in \{1, 5, 22\}$'),
     [T(r'HAR: direct regression of $\log RV_{t+h}$; ARFIMA$(0,d,0)$: local Whittle $d$ (capped at 0.49), AR($\infty$) iterated; RFSV: $H$, $\nu$ from the window', r'HAR: regresie directă a lui $\log RV_{t+h}$; ARFIMA$(0,d,0)$: $d$ local Whittle (limitat la 0,49), AR($\infty$) iterat; RFSV: $H$, $\nu$ din fereastră')]),
    (T(r'Loss: QLIKE $L = RV/F - \log(RV/F) - 1$, robust to the noise in the RV proxy \refPat; also MSE of logs', r'Pierderea: QLIKE $L = RV/F - \log(RV/F) - 1$, robustă la zgomotul proxy-ului RV \refPat; și MSE al logaritmilor'),
     [T(r'level forecasts from log forecasts need the lognormal correction: $\exp(\hat\mu + \hat s^2/2)$ for HAR and ARFIMA, $2c\nu^2h^{2H}$ for RFSV', r'prognozele de nivel din prognoze logaritmice cer corecția lognormală: $\exp(\hat\mu + \hat s^2/2)$ pentru HAR și ARFIMA, $2c\nu^2h^{2H}$ pentru RFSV')]),
    T(r'Inference: DM with Newey--West variance (Chapter 1) \refDM; the loss differences are themselves persistent, so the $p$-values are optimistic', r'Inferența: DM cu varianță Newey--West (Capitolul 1) \refDM; diferențele de pierderi sînt ele însele persistente, deci p-value-urile sînt optimiste')), 'small')

chart(T('RFSV and ARFIMA against HAR', 'RFSV și ARFIMA față de HAR'), 'ats_ch10_forecast', 'ATS_ch10_forecast', [
    T(r'Average QLIKE relative to HAR (below 1: better than HAR); a star marks a DM $p$-value below 5\%; S\&P 500 @{fo.spx.start} -- @{fo.spx.end} ($T = @{fo.spx.T}$), DAX ($T = @{fo.dax.T}$), Bitcoin @{fo.btc.start} -- @{fo.btc.end} ($T = @{fo.btc.T}$)',
      r'QLIKE mediu relativ la HAR (sub 1: mai bun decît HAR); o stea marchează un p-value DM sub 5\%; S\&P 500 @{fo.spx.start} -- @{fo.spx.end} ($T = @{fo.spx.T}$), DAX ($T = @{fo.dax.T}$), Bitcoin @{fo.btc.start} -- @{fo.btc.end} ($T = @{fo.btc.T}$)')], h='0.56\\textheight')

D.frame(T('Interpreting the forecast comparison', 'Interpretarea comparației prognozelor'), table(
    'lcccccc', T(r'\textbf{QLIKE / HAR}', r'\textbf{QLIKE / HAR}') + r' & \multicolumn{2}{c}{S\&P 500} & \multicolumn{2}{c}{DAX} & \multicolumn{2}{c}{Bitcoin} \\ & ARFIMA & RFSV & ARFIMA & RFSV & ARFIMA & RFSV',
    [f'$h = {hh}$ & ' + ' & '.join(f'@{{fo.{a}.{hh}.{m}}}' for a in ('spx', 'dax', 'btc') for m in ('arf', 'rfsv')) for hh in ('1', '5', '22')],
    size='scriptsize') + items(
    T(r'S\&P 500 and DAX: RFSV is @{fo.glo}\% to @{fo.ghi}\% better than HAR at 5 and 22 days but worse at 1 day; DM at 5 days: @{fo.spx.5.rfsv.t} ($p$ @{fo.spx.5.rfsv.p}) and @{fo.dax.5.rfsv.t} ($p$ @{fo.dax.5.rfsv.p})', r'S\&P 500 și DAX: RFSV este cu @{fo.glo}\% pînă la @{fo.ghi}\% mai bun decît HAR la 5 și 22 de zile, dar mai slab la o zi; DM la 5 zile: @{fo.spx.5.rfsv.t} ($p$ @{fo.spx.5.rfsv.p}) și @{fo.dax.5.rfsv.t} ($p$ @{fo.dax.5.rfsv.p})'),
    T(r'Bitcoin: RFSV is worse at every horizon (@{fo.btc.5.rfsv} at 5 days); rolling $\hat H$ ranges from @{fo.btc.Hlo} to @{fo.btc.Hhi}, median @{fo.btc.Hm}', r'Bitcoin: RFSV este mai slab la toate orizonturile (@{fo.btc.5.rfsv} la 5 zile); $\hat H$ mobil variază între @{fo.btc.Hlo} și @{fo.btc.Hhi}, cu mediana @{fo.btc.Hm}'),
    T(r'ARFIMA is within @{fo.arfdev}\% of HAR everywhere; of the 18 QLIKE comparisons, @{fo.nsig} is significant at 5\%', r'ARFIMA se află peste tot la cel mult @{fo.arfdev}\% de HAR; dintre cele 18 comparații QLIKE, @{fo.nsig} este semnificativă la 5\%'),
    T('Roughness is a robust stylised fact; its forecasting gain over HAR is small and horizon-dependent, as in \\refGJR\\ and \\refWXY', 'Neregularitatea este un fapt stilizat robust; cîștigul ei în prognoză față de HAR este mic și depinde de orizont, ca în \\refGJR\\ și \\refWXY')), 'footnotesize')

D.recap(('Forecasting', 'prognoza'), [
    T('RFSV forecasts with a horizon-dependent power kernel and a lognormal correction, from two variogram parameters', 'RFSV prognozează cu un nucleu putere dependent de orizont și o corecție lognormală, din doi parametri ai variogramei'),
    T('Out of sample, RFSV, ARFIMA and HAR are close; RFSV gains a few percent at weekly and monthly horizons for equity indices', 'În afara eșantionului, RFSV, ARFIMA și HAR sînt apropiate; RFSV cîștigă cîteva procente la orizonturi săptămînale și lunare pentru indicii bursieri'),
    T('Pre-register the design, use QLIKE, and treat DM $p$-values with care under persistent loss differences', 'Preînregistrați schema, folosiți QLIKE și tratați cu prudență p-value-urile DM cînd diferențele de pierderi sînt persistente')])

# =============================================================================
# AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Is the roughness of volatility a property of the volatility process, or of the way we measure it?', 'Este neregularitatea volatilității o proprietate a procesului de volatilitate sau a felului în care o măsurăm?'),
     [T(r'formal: $H_0$: $H \ge 0.3$ for integrated variance; tested with estimators that are consistent under measurement error, on pre-registered assets, measures and samples', r'formal: $H_0$: $H \ge 0{,}3$ pentru varianța integrată; testat cu estimatori consistenți sub eroare de măsurare, pe active, măsuri și eșantioane preînregistrate'),
      T('falsified if the corrected estimates stay below 0.2 across sampling frequencies and markets', 'infirmată dacă estimațiile corectate rămîn sub 0,2 pentru toate frecvențele de eșantionare și piețele')]),
    (T('Why it matters: rough models change option pricing and hedging; if roughness is an artefact, Markovian models suffice', 'Miza: modelele de tip rough volatility schimbă evaluarea opțiunilor și acoperirea; dacă neregularitatea este un artefact, modelele markoviene sînt suficiente'),
     [T(r'literature to start from: \refGJR, \refFTW, \refBCPV, \refCD, \refBLPb', r'literatura de pornire: \refGJR, \refFTW, \refBCPV, \refCD, \refBLPb')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers since 2018 that estimate the Hurst exponent of volatility with methods robust to measurement error; give DOIs.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează articole recenzate din 2018 încoace care estimează exponentul Hurst al volatilității cu metode robuste la eroarea de măsurare; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Which data-generating processes with H = 0.5 would make the moment estimator on 5-minute RV return H near 0.1?}', r'\textbf{ipoteza}: \aiprompt{Ce procese generatoare cu H = 0,5 ar face ca estimatorul momentelor pe RV de 5 minute să dea H aproape de 0,1?}'),
      T(r'\textbf{code and replication}: ask for the variogram regression, then reproduce first the S\&P 500 value (@{gj.H} here) and the simulation table', r'\textbf{cod și replicare}: cereți regresia pe variogramă, apoi reproduceți întîi valoarea pentru S\&P 500 (@{gj.H} aici) și tabelul de simulare'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee: list how lag choice, overnight returns, jumps and microstructure noise could bias H.}', r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră cum ar putea alegerea lagurilor, randamentele overnight, salturile și zgomotul de microstructură să deplaseze H.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The scale is stated: $H$ of fBm, $d$ of ARFIMA, $H = d + 1/2$ for stationary series; log volatility or log variance', 'Scara este precizată: $H$ pentru fBm, $d$ pentru ARFIMA, $H = d + 1/2$ pentru seriile staționare; logaritmul volatilității sau al varianței'),
    T('Bandwidths, lags and trimming are reported, with estimates across a range, not one convenient choice', 'Lățimile de bandă, lagurile și trimming-ul sînt raportate, cu estimații pe un interval de valori, nu o singură alegere convenabilă'),
    T('Breaks and level shifts are tested (Qu) before long memory is claimed', 'Rupturile și salturile de nivel sînt testate (Qu) înainte de a afirma memoria lungă'),
    T('Forecast comparisons are out of sample, pre-registered, with QLIKE and DM', 'Comparațiile prognozelor sînt în afara eșantionului, preînregistrate, cu QLIKE și DM')), 'small')

chart(T('Mini-case: how robust is ``$H$ of order 0.1\'\'?', 'Mini studiu de caz: cît de robust este „$H$ de ordinul 0,1”?'), 'ats_ch10_ai_case', 'ATS_ch10_rough', [
    T(r'@{ai.cells} cells: seven assets $\times$ five realised measures $\times$ two halves of the sample; two estimators each (@{ai.n} estimates); right: $H$ against the local Whittle $d$ of the same cell',
      r'@{ai.cells} de celule: șapte active $\times$ cinci măsuri realizate $\times$ două jumătăți ale eșantionului; doi estimatori pentru fiecare (@{ai.n} de estimații); dreapta: $H$ față de $d$ local Whittle din aceeași celulă'),
    T(r'$H$ from @{ai.Hmin} to @{ai.Hmax}, median @{ai.Hmed} (moments @{ai.Hmedmom}, with intercept @{ai.Hmedint}); @{ai.sh}\% below 0.2; $d$ from @{ai.dmin} to @{ai.dmax}; correlation of $H$ and $d$ @{ai.corr}: an AI summary that calls volatility ``short memory because $H < 1/2$\'\' is wrong',
      r'$H$ între @{ai.Hmin} și @{ai.Hmax}, mediana @{ai.Hmed} (momente @{ai.Hmedmom}, cu termen liber @{ai.Hmedint}); @{ai.sh}\% sub 0,2; $d$ între @{ai.dmin} și @{ai.dmax}; corelația dintre $H$ și $d$ @{ai.corr}: un rezumat AI care numește volatilitatea „cu memorie scurtă pentru că $H < 1/2$” greșește')],
    h='0.52\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Roughness and persistence of volatility in Central and Eastern European markets}: replicate first, then extend', r'\textbf{Neregularitatea și persistența volatilității pe piețele din Europa Centrală și de Est}: întîi replicare, apoi extindere'),
     [T(r'replicate: \refGJR, Section 2 on the Oxford-Man S\&P 500 ($H = @{gj.H}$ here) and the forecasting comparison of their Section 5', r'replicați: \refGJR, secțiunea 2 pe datele Oxford-Man pentru S\&P 500 ($H = @{gj.H}$ aici) și comparația prognozelor din secțiunea 5'),
      T('extend: intraday data for the BET, WIG20 and EUR/RON; estimators robust to noise (FTW, GMM); Qu tests; a BSS model with separate roughness and memory', 'extindeți: date intraday pentru BET, WIG20 și EUR/RON; estimatori robuști la zgomot (FTW, GMM); teste Qu; un model BSS cu neregularitate și memorie separate'),
      T('pre-register: assets, measures, lags, bandwidths, the forecast design and the loss', 'preînregistrați: activele, măsurile, lagurile, lățimile de bandă, schema prognozei și pierderea')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Long memory is a pole at frequency zero; estimate it with local Whittle or exact local Whittle and report $\\hat d(m)$', 'Memoria lungă este un pol în frecvența zero; estimați-o cu local Whittle sau local Whittle exact și raportați $\\hat d(m)$'),
    T('Level shifts mimic long memory: test with Qu (2011) and look at the bandwidth signature', 'Salturile de nivel imită memoria lungă: testați cu Qu (2011) și urmăriți semnătura lățimii de bandă'),
    T('Volatility is persistent over months (FIGARCH, LMSV, HAR) and rough over days ($H \\approx 0.1$)', 'Volatilitatea este persistentă pe luni (FIGARCH, LMSV, HAR) și neregulată pe zile ($H \\approx 0{,}1$)'),
    T('Proxies matter: noise lowers $\\hat d$ and $\\hat H$; corrections exist and should be reported', 'Proxy-urile contează: zgomotul scade $\\hat d$ și $\\hat H$; corecțiile există și trebuie raportate'),
    T('In forecasting, HAR remains a tough benchmark; rough models gain little and only at some horizons', 'În prognoză, HAR rămîne un reper greu de depășit; modelele de tip rough volatility cîștigă puțin și doar la unele orizonturi')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T(r'Why is the asymptotic variance of local Whittle $1/(4m)$ and that of GPH $\pi^2/(24m)$?', r'De ce este varianța asimptotică a local Whittle $1/(4m)$, iar a GPH $\pi^2/(24m)$?'),
        T('Why does local Whittle fail for $d > 1$, and how does exact local Whittle fix it?', 'De ce eșuează local Whittle pentru $d > 1$ și cum corectează local Whittle exact problema?'),
        T('Which spectral shape does a random level shift produce?', 'Ce formă spectrală produce un salt aleator de nivel?'),
        T('Why is FIGARCH not covariance stationary?', 'De ce nu este FIGARCH staționar în covarianță?'),
        T('How can a series be rough and long-memory at the same time?', 'Cum poate o serie să fie neregulată și cu memorie lungă în același timp?'))),
    block(T('Next: Chapter 11', 'Urmează: Capitolul 11'), items(
        T('Spectral and wavelet analysis', 'Analiză spectrală și analiză wavelet'),
        T('multitaper, coherence, wavelets: the frequency tools behind this chapter', 'multitaper, coerență, wavelets: instrumentele de frecvență din spatele acestui capitol'))),
    '0.58', '0.38'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the variance of local Whittle', 'Anexă: varianța estimatorului local Whittle'), items(
    T(r'Expand $R\'(\hat d) = 0$ around $d$: $\sqrt m(\hat d - d) = -\sqrt m\,R\'(d)/R\'\'(\bar d)$', r'Dezvoltăm $R\'(\hat d) = 0$ în jurul lui $d$: $\sqrt m(\hat d - d) = -\sqrt m\,R\'(d)/R\'\'(\bar d)$'),
    T(r'$\sqrt m\,R\'(d) = \dfrac{2}{\sqrt m}\sum_j\nu_j(\xi_j - 1) + o_p(1)$, $\xi_j = \lambda_j^{2d}I(\lambda_j)/G$; with $\Var\xi_j \to 1$ and $\frac1m\sum\nu_j^2 \to 1$: $\to N(0, 4)$', r'$\sqrt m\,R\'(d) = \dfrac{2}{\sqrt m}\sum_j\nu_j(\xi_j - 1) + o_p(1)$, $\xi_j = \lambda_j^{2d}I(\lambda_j)/G$; cu $\Var\xi_j \to 1$ și $\frac1m\sum\nu_j^2 \to 1$: $\to N(0, 4)$'),
    T(r'$R\'\'(d) = \dfrac4m\sum_j\nu_j^2\xi_j/\bar\xi - \big(\dfrac2m\sum_j\nu_j\xi_j/\bar\xi\big)^2 \to_p 4$', r'$R\'\'(d) = \dfrac4m\sum_j\nu_j^2\xi_j/\bar\xi - \big(\dfrac2m\sum_j\nu_j\xi_j/\bar\xi\big)^2 \to_p 4$'),
    T(r'Hence $\sqrt m(\hat d - d) \to N(0, 4/16) = N(0, 1/4)$; for GPH the same weights multiply $\log\xi_j$ with variance $\pi^2/6$: $N(0, \pi^2/24)$', r'Deci $\sqrt m(\hat d - d) \to N(0, 4/16) = N(0, 1/4)$; la GPH aceleași ponderi înmulțesc $\log\xi_j$ cu varianța $\pi^2/6$: $N(0, \pi^2/24)$')), 'small')

D.frame(T('Appendix: scaling of fBm moments', 'Anexă: scalarea momentelor fBm'), items(
    T(r'$W^H_{t+\Delta} - W^H_t \sim N(0, \Delta^{2H})$, so $\E|W^H_{t+\Delta} - W^H_t|^q = \Delta^{qH}\E|Z|^q$, $\E|Z|^q = 2^{q/2}\Gamma\big(\tfrac{q+1}{2}\big)/\sqrt\pi$', r'$W^H_{t+\Delta} - W^H_t \sim N(0, \Delta^{2H})$, deci $\E|W^H_{t+\Delta} - W^H_t|^q = \Delta^{qH}\E|Z|^q$, $\E|Z|^q = 2^{q/2}\Gamma\big(\tfrac{q+1}{2}\big)/\sqrt\pi$'),
    T(r'With $\log\sigma_t = \nu W^H_t$: $\log m(q, \Delta) = q\log\nu + \log\E|Z|^q + qH\log\Delta$: slope $\zeta_q = qH$', r'Cu $\log\sigma_t = \nu W^H_t$: $\log m(q, \Delta) = q\log\nu + \log\E|Z|^q + qH\log\Delta$: panta $\zeta_q = qH$'),
    T(r'Departures: concave $\zeta_q$ signals multifractality or heavy tails; an intercept in $m(2, \Delta) = \nu^2\Delta^{2H} + 2s^2$ signals i.i.d.\ measurement error of variance $s^2$', r'Abateri: $\zeta_q$ concav semnalează multifractalitate sau cozi groase; un termen liber în $m(2, \Delta) = \nu^2\Delta^{2H} + 2s^2$ semnalează o eroare de măsurare i.i.d.\ cu varianța $s^2$'),
    T(r'fGn spectrum near zero: $f(\lambda) \propto |\lambda|^{1-2H}$, i.e.\ the increments are ARFIMA-like with $d = H - 1/2$', r'Spectrul fGn lîngă zero: $f(\lambda) \propto |\lambda|^{1-2H}$, adică creșterile sînt de tip ARFIMA cu $d = H - 1/2$')), 'small')

D.references(bib(), per=14)

if __name__ == '__main__':
    finalize(D.write(V))
