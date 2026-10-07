r"""
build_chapter8.py -- Capitolul 8 (Modelarea avansată a volatilității: măsuri realizate, HAR și GARCH multivariat), EN + RO
=======================================================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_08/ch8_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice și a constantelor publicate, cu sursa citată). TSA, Capitolul 5 a
predat GARCH(1,1), GJR, EGARCH, curba de impact a știrilor, QLIKE și o primă privire asupra VaR; TSA, Capitolul 14 a
predat bazele DCC; MFM, Capitolele 5--9 aplică volatilitatea în finanțe. Aici: teoria QML, componente de termen lung
(component GARCH, GARCH-MIDAS), teoria măsurilor realizate (CLT, zgomot, kernel-uri, salturi), HAR și HARQ, Realized
GARCH și HEAVY, funcții de pierdere robuste, BEKK/DCC/cDCC/DCC-NL și covarianța realizată.
Ieșire:
  EN/Courses/chapter8_advanced_volatility.tex
  RO/Cursuri/capitol8_volatilitate_avansata.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_08/generate_all_charts.py
  python3 latex/build_chapter8.py && python3 latex/ats_build.py compile 8
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch8_common import REFS, QLURL, BIN_URL, T, bib, finalize, load, minus_fix   # noqa: E402


def M(tex):
    """Displayed formula with decimals: decimal comma in RO (the renderer converts only inline math)."""
    return T(tex, re.sub(r'(\d)\.(\d)', r'\1{,}\2', tex))


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(8, 'lecture', refs=REFS)
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
    'bn': ('ch8_barndorff_nielsen_2007.jpg', C + 'Ole-Barndorff-Nielsen.jpg',
           FOTO + ': Thomas Steiner (2007); CC BY-SA 2.5; Wikimedia Commons'),
    'ghysels': ('ch8_ghysels_2019.jpg', C + 'EricGhysels.jpg', FOTO + ': Eghysels (2019); CC BY-SA 4.0; Wikimedia Commons'),
    'nyse': ('ch8_nyse_floor_1908.jpg', C + 'Stockexchange.jpg',
             FOTO + ": Helen D. Van Eaton, Leslie's Monthly Magazine (1908); public domain; Wikimedia Commons"),
    'bvb': ('ch8_bvb_palace_1928.jpg', C + 'Nicolae_Ionescu_-_The_Stock_Exchange_Palace_in_March_1928.jpg',
            FOTO + ': Nicolae Ionescu (1928); public domain; Wikimedia Commons'),
    'engle': ('ch4_engle_2017.jpg', C + 'Robert_Engle_SantiagoWEAI2017.png', FOTO + ': Econterms (2017); CC BY-SA 4.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


TB = '>{\\raggedright\\arraybackslash}'


def dt(s):
    """2008-06-30 -> 30.06.2008 (EN and RO alike)."""
    y, m, d = s[:10].split('-')
    return f'{d}.{m}.{y}'


# =============================================================================
# CIFRE
# =============================================================================
qs = N['qmle_sim']
for inn in ('normal', 't5'):
    for k in ('h', 'bw'):
        for j, par in enumerate(('o', 'a', 'b')):
            P(f'qs.{inn}.{k}.{par}', 100 * qs[inn][k][j], 1)
V.raw('qs.reps', str(qs['reps']))
V.int('qs.T', qs['T'])
qm = N['qmle']
for nm in ('sp500', 'dax', 'bet', 'eurron', 'btc'):
    r_ = qm[nm]
    V.int(f'qm.{nm}.T', r_['T'])
    for j, par in enumerate(('o', 'a', 'b')):
        P(f'qm.{nm}.{par}', r_['theta'][j], 3)
        P(f'qm.{nm}.{par}.h', r_['se_h'][j], 3)
        P(f'qm.{nm}.{par}.bw', r_['se_bw'][j], 3)
        P(f'qm.{nm}.{par}.r', r_['ratio'][j], 2)
    P(f'qm.{nm}.k', r_['kurt'], 1)
    P(f'qm.{nm}.nu', r_['nu'], 1)
    P(f'qm.{nm}.pers', r_['pers'], 3)
    P(f'qm.{nm}.dll', r_['ll_t'] - r_['ll_n'], 1)
    P(f'qm.{nm}.th', ((r_['kurt'] - 1) / 2) ** 0.5, 2)
cg = N['cgarch']
for j, par in enumerate(('om', 'rho', 'phi', 'a', 'b')):
    P(f'cg.{par}', cg['theta'][j], 4 if par == 'om' else 3)
P('cg.ab', cg['theta'][3] + cg['theta'][4], 3)
P('cg.LR', cg['LR'], 1)
P('cg.hll', cg['hl_long'], 0)
P('cg.hls', cg['hl_short'], 1)
P('cg.hlg', cg['hl_garch'], 0)
P('cg.gp', cg['garch_pers'], 3)
V.int('cg.T', cg['T'])
md = N['midas']
for nm in ('ip', 'ppi', 'rv'):
    m_ = md[nm]
    for j, par in enumerate(('a', 'b', 'm', 'th', 'w')):
        P(f'md.{nm}.{par}', m_['theta'][j], 4 if (nm == 'rv' and par == 'th') else 3)
        P(f'md.{nm}.{par}.se', m_['se'][j], 4 if (nm == 'rv' and par == 'th') else 3)
    P(f'md.{nm}.vr', 100 * m_['vr'], 1)
    P(f'md.{nm}.ll', m_['ll'], 1)
    P(f'md.{nm}.bic', md['bic'][nm], 1)
    P(f'md.{nm}.t', m_['theta'][3] / m_['se'][3], 2)
P('md.gll', md['garch_ll'], 1)
P('md.gbic', md['bic_garch'], 1)
V.int('md.T', md['ip']['T'])
V.raw('md.K', str(md['K']))
V.raw('md.first', dt(md['ip']['first']))
cl = N['clt']
for lab in ('clean', 'noisy'):
    for kind in ('raw', 'log'):
        for j, n_ in enumerate(cl['n']):
            P(f'cl.{lab}.{kind}.{n_}', 100 * cl[lab][kind][j], 1)
V.raw('cl.days', str(cl['days']))
kn = N['kernels']
for k_, nm in (('RV 1 s', 'rv1s'), ('RV 1 min', 'rv1m'), ('RV 5 min', 'rv5'), ('RV 5 min, subsampled', 'rvss'),
               ('TSRV', 'tsrv'), ('realised kernel', 'rk')):
    P(f'kn.{nm}.b', 100 * kn[k_]['bias'], 1)
    P(f'kn.{nm}.r', 100 * kn[k_]['rmse'], 1)
P('kn.H', kn['H_med'], 0)
P('kn.nb', kn['noise_bias_1s'], 2)
P('kn.js', 100 * kn['jshare'], 1)
V.raw('kn.days', str(kn['days']))
sg = N['signature']
for k_ in ('1', '60', '300', '1800'):
    P(f'sg.b{k_}', sg['btc'][k_], 2)
    P(f'sg.e{k_}', sg['eth'][k_], 2)
    P(f'sg.c{k_}', sg['corr'][k_], 2)
P('sg.rk', sg['rk'], 2)
P('sg.H', sg['H'], 0)
P('sg.zero', 100 * sg['zero'], 0)
P('sg.ratio', sg['ratio_1s_5m'], 2)
V.raw('sg.days', str(sg['days']))
ov = N['overview']
for k_, nm in (('.SPX', 'spx'), ('.GDAXI', 'dax'), ('.N225', 'nk'), ('btc', 'btc')):
    P(f'ov.{nm}', ov[k_]['mean'], 1)
V.int('ov.spx.T', ov['.SPX']['T'])
V.int('ov.btc.T', ov['btc']['T'])
js = N['jumpsim']
for lab in ('clean', 'noisy'):
    for nm in ('5m', '1m', '5s'):
        P(f'js.{lab}.{nm}', 100 * js[f'size_{lab}_{nm}'], 1)
for j, s_ in enumerate(js['sizes']):
    P(f'js.p5.{j}', 100 * js['power']['5m'][j], 0)
    P(f'js.p1.{j}', 100 * js['power']['1m'][j], 0)
V.int('js.days', js['days'])
ju = N['jumps']
for c_ in ('btc', 'eth'):
    P(f'ju.{c_}.share', 100 * ju[c_]['share'], 1)
    V.raw(f'ju.{c_}.n', str(ju[c_]['n_jump']))
    P(f'ju.{c_}.exp', ju[c_]['expected_false'], 1)
    P(f'ju.{c_}.jv', 100 * ju[c_]['jv_share'], 1)
    P(f'ju.{c_}.mz', ju[c_]['mean_z'], 2)
V.int('ju.T', ju['btc']['T'])
hr = N['har']
for j, par in enumerate(('0', 'd', 'w', 'm')):
    P(f'hr.{par}', hr['b'][j], 3)
    P(f'hr.{par}.se', hr['se'][j], 3)
    P(f'hr.l{par}', hr['bl'][j], 3)
    P(f'hr.l{par}.se', hr['sel'][j], 3)
P('hr.r2', hr['r2'], 3)
P('hr.r22', hr['r2_22'], 3)
P('hr.r2l', hr['r2l'], 3)
P('hr.sum', hr['sum'], 3)
P('hr.suml', hr['suml'], 3)
V.int('hr.T', hr['T'])
ho = N['haroos']
OMIS = [('.SPX', 'spx'), ('.GDAXI', 'dax'), ('.FTSE', 'ftse'), ('.N225', 'nk'), ('.STOXX50E', 'sx5e'), ('.FCHI', 'cac')]
for k_, nm in OMIS + [('btc', 'btc'), ('eth', 'eth')]:
    for m_ in ('harcj', 'loghar') + (('harq',) if k_ in ('btc', 'eth') else ()):
        P(f'ho.{nm}.{m_}', ho[k_][m_]['qlike'], 3)
        P(f'ho.{nm}.{m_}.m', ho[k_][m_]['mse'], 3)
        P(f'ho.{nm}.{m_}.dm', ho[k_][m_]['dm'], 2)
nlog_better = sum(ho[k_]['loghar']['qlike'] < 1 for k_, _ in OMIS)
V.raw('ho.nlog', str(nlog_better))
V.raw('ho.ncj', str(sum(ho[k_]['harcj']['qlike'] < 1 for k_, _ in OMIS)))
V.raw('ho.btc.first', dt(ho['btc']['first']))
hq = N['harq']
for j, par in enumerate(('0', 'd', 'q', 'w', 'm')):
    P(f'hq.{par}', hq['b'][j], 5 if par == 'q' else 3)
    P(f'hq.{par}.se', hq['se'][j], 5 if par == 'q' else 3)
for j, par in enumerate(('0', 'd', 'w', 'm')):
    P(f'hq.h{par}', hq['bh'][j], 3)
    P(f'hq.h{par}.se', hq['seh'][j], 3)
P('hq.q01', hq['q01'], 2)
P('hq.wmin', hq['wmin'], 2)
P('hq.q50', hq['q50'], 2)
P('hq.tq', hq['b'][2] / hq['se'][2], 1)
rg = N['rgarch']
for j, par in enumerate(('om', 'b', 'g', 'xi', 'phi', 't1', 't2', 'su')):
    P(f'rg.{par}', rg['theta'][j], 3)
    P(f'rg.{par}.se', rg['se'][j], 3)
P('rg.pers', rg['pers'], 3)
for k_ in ('ll_r', 'll_garch', 'll_gjr', 'll_heavy'):
    P(f'rg.{k_}', rg[k_], 1)
for j, par in enumerate(('om', 'a', 'b')):
    P(f'rg.hv.{par}', rg['heavy'][j], 3)
P('rg.gp', rg['garch'][1] + rg['garch'][2], 3)
P('rg.gain', rg['ll_r'] - rg['ll_garch'], 1)
V.int('rg.T', rg['T'])
pt = N['patton']
for kind, nm in (('MSE', 'mse'), ('QLIKE', 'ql'), ('MAE', 'mae'), ('MSE-log', 'ml')):
    for j, n_ in enumerate(pt['n']):
        P(f'pt.{nm}.{n_}', 100 * pt[kind][j], 1)
P('pt.c', pt['c'], 1)
P('pt.copt', pt['c_opt_mselog_n1'], 2)
vo = N['voloos']
for k_, nm in (('GARCH', 'g'), ('GJR', 'gjr'), ('GARCH-t', 'gt'), ('RGARCH', 'rg'), ('HEAVY', 'hv'), ('HAR', 'har'), ('log-HAR', 'lh')):
    P(f'vo.{nm}.q', vo['res'][k_]['qlike'], 3)
    P(f'vo.{nm}.m', vo['res'][k_]['mse'], 2)
    P(f'vo.{nm}.dq', vo['res'][k_]['dm_q'], 2)
    P(f'vo.{nm}.dm', vo['res'][k_]['dm_m'], 2)
V.int('vo.T', vo['T_oos'])
np_ = N['nparams']
for k_ in ('2', '5', '10', '25', '50', '100'):
    for m_ in ('vec', 'bekk', 'dbekk', 'sbekk', 'dcc'):
        V.int(f'np.{k_}.{m_}', np_[k_][m_])
ds = N['dccsim']
for k_, nm in (('DCC', 'd'), ('cDCC', 'c')):
    for j, par in enumerate(('a', 'b')):
        P(f'ds.{nm}.{par}', ds['mean'][k_][j], 4)
        P(f'ds.{nm}.{par}.sd', ds['sd'][k_][j], 4)
        P(f'ds.{nm}.{par}.rmse', ds['rmse'][k_][j], 4)
V.raw('ds.reps', str(ds['reps']))
V.int('ds.T', ds['T'])
gm = N['gmv']
for k_, nm in (('1/N', 'ew'), ('sample', 's'), ('LW linear', 'lw'), ('NL shrinkage', 'nl'), ('DCC', 'dcc'), ('DCC-NL', 'dccnl'),
               ('sample, short', 's250'), ('NL, short', 'nl250')):
    P(f'gm.{nm}', gm['sd'][k_], 2)
V.int('gm.short', gm['short'])
P('gm.cond', gm['cond_med'], 0)
P('gm.gain250', 100 * (1 - gm['sd']['NL, short'] / gm['sd']['sample, short']), 1)
V.raw('gm.N', str(gm['N']))
V.int('gm.win', gm['win'])
V.raw('gm.first', dt(gm['first_oos']))
V.raw('gm.n', str(gm['n_rebal']))
P('gm.a', gm['ab']['DCC'][0], 3)
P('gm.b', gm['ab']['DCC'][1], 3)
P('gm.gain', 100 * (1 - gm['sd']['DCC-NL'] / gm['sd']['sample']), 1)
cc = N['corr']
P('cc.a', cc['a'], 3)
P('cc.b', cc['b'], 3)
P('cc.rc', cc['rc_mean'], 2)
P('cc.dcc', cc['dcc_mean'], 2)
P('cc.cor', cc['corr_rc_dcc'], 2)
P('cc.q05', cc['rc_q05'], 2)
ai = N['ai']
P('ai.min', ai['min'], 3)
P('ai.max', ai['max'], 3)
P('ai.better', 100 * ai['share_better'], 0)
P('ai.sig', 100 * ai['share_sig'], 0)
P('ai.wsig', 100 * ai['share_worse_sig'], 0)
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: how precisely can we measure, model and forecast a variance that is never observed?',
       r'\textbf{Întrebarea}: cît de precis putem măsura, modela și prognoza o varianță care nu se observă niciodată?'),
     [T('and which of our tools still work when the data are noisy, jumpy or high-dimensional?',
        'și care dintre instrumentele noastre funcționează în continuare cînd datele sînt zgomotoase, au salturi sau au multe dimensiuni?'),
      T('two routes to volatility: a parametric filter of daily returns (GARCH) and a nonparametric measurement from intraday prices (realised measures); the frontier combines them',
        'două căi către volatilitate: un filtru parametric al randamentelor zilnice (GARCH) și o măsurare neparametrică din prețurile intraday (măsurile realizate); cercetarea actuală le combină')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('quasi-maximum likelihood for GARCH and robust inference; long-run components: component GARCH and GARCH-MIDAS with macroeconomic drivers',
        'verosimilitatea cvasi-maximă pentru GARCH și inferența robustă; componente de termen lung: component GARCH și GARCH-MIDAS cu factori macroeconomici'),
      T('realised measures: asymptotics of realised variance, microstructure noise, realised kernels, bipower variation and jump tests',
        'măsuri realizate: asimptotica varianței realizate, zgomotul de microstructură, realised kernels, variația bipower și testele de salt'),
      T('forecasting with realised measures: HAR, HARQ, Realized GARCH, HEAVY; robust loss functions',
        'prognoza cu măsuri realizate: HAR, HARQ, Realized GARCH, HEAVY; funcții de pierdere robuste'),
      T('multivariate: BEKK, DCC and cDCC, the curse of dimensionality and DCC-NL, realised covariance',
        'cazul multivariat: BEKK, DCC și cDCC, blestemul dimensionalității și DCC-NL, covarianța realizată')]),
    (T('We build on TSA, Chapter 5 (GARCH, GJR, EGARCH, news impact, QLIKE) and TSA, Chapter 14 (DCC basics)',
       'Pornim de la TSA, Capitolul 5 (GARCH, GJR, EGARCH, curba de impact a știrilor, QLIKE) și TSA, Capitolul 14 (bazele DCC)'),
     [T('MFM, Chapters 5--9 apply these tools to market risk; Seminar 8 comes before this lecture',
        'MFM, Capitolele 5--9 aplică aceste instrumente riscului de piață; Seminarul 8 are loc înaintea acestui curs')])), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('State the conditions under which Gaussian QML for GARCH is consistent and asymptotically normal, and compute Bollerslev--Wooldridge standard errors',
      'Enunțați condițiile în care QML gaussian pentru GARCH este consistent și asimptotic normal și calculați erorile standard Bollerslev--Wooldridge'),
    T('Separate short-run from long-run volatility with component GARCH and GARCH-MIDAS, and judge whether a macroeconomic driver matters',
      'Separați volatilitatea de termen scurt de cea de termen lung cu component GARCH și GARCH-MIDAS și evaluați dacă un factor macroeconomic contează'),
    T('Derive the limit theory of realised variance, explain the effect of noise and jumps, and choose among RV, realised kernels and bipower variation',
      'Derivați teoria asimptotică a varianței realizate, explicați efectul zgomotului și al salturilor și alegeți între RV, realised kernels și variația bipower'),
    T('Forecast volatility with HAR, HARQ and Realized GARCH, and compare forecasts with losses that are robust to a noisy proxy',
      'Prognozați volatilitatea cu HAR, HARQ și Realized GARCH și comparați prognozele cu funcții de pierdere robuste la un proxy zgomotos'),
    T('Estimate DCC and cDCC models, explain why large covariance matrices need shrinkage, and measure correlation from intraday data',
      'Estimați modele DCC și cDCC, explicați de ce matricele de covarianță mari au nevoie de shrinkage și măsurați corelația din date intraday')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Backbone: \refFZ; \refABDL; \refBNSa; \refBNHLSa',
       r'Bibliografia de bază: \refFZ; \refABDL; \refBNSa; \refBNHLSa'),
     [T(r'forecasting and the multivariate case: \refCor; \refHHS; \refEngD; \refPat',
        r'prognoza și cazul multivariat: \refCor; \refHHS; \refEngD; \refPat'),
      T(r'case studies: \refEGS\ (GARCH-MIDAS), \refBPQ\ (HARQ), \refHHS\ (Realized GARCH), \refELW\ (DCC-NL)',
        r'studii de caz: \refEGS\ (GARCH-MIDAS), \refBPQ\ (HARQ), \refHHS\ (Realized GARCH), \refELW\ (DCC-NL)')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_08}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_08}'),
     [T(r'QML with sandwich standard errors, component GARCH, GARCH-MIDAS, realised kernels, jump tests, HAR/HARQ, Realized GARCH, DCC/cDCC and nonlinear shrinkage written out in \texttt{numpy}',
        r'QML cu erori standard sandwich, component GARCH, GARCH-MIDAS, realised kernels, teste de salt, HAR/HARQ, Realized GARCH, DCC/cDCC și shrinkage neliniar scrise explicit în \texttt{numpy}')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter8_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter8_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{4.6cm}' + TB + 'p{4.9cm}' + TB + 'p{2.4cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizare}'),
    [T('Daily realised measures of six equity indices (5-minute RV, BV, realised kernel, open-to-close return), 2000--2022', 'Măsuri realizate zilnice pentru șase indici bursieri (RV la 5 minute, BV, realised kernel, randamentul deschidere--închidere), 2000--2022')
     + r' & \refOMI, v0.3 & HAR, RGARCH',
     T('Bitcoin and Ether: one-minute prices 2018--2026, one-second prices August 2026', 'Bitcoin și Ether: prețuri la un minut 2018--2026, prețuri la o secundă în august 2026')
     + r' & ' + T(r'Binance public data (\href{' + BIN_URL + r'}{data.binance.vision}); measures computed by us', r'datele publice Binance (\href{' + BIN_URL + r'}{data.binance.vision}); măsuri calculate de noi') + ' & ' + T('noise, jumps, HARQ', 'zgomot, salturi, HARQ'),
     T('S\\&P 500, DAX, BET, Bitcoin, 14 US stocks and 3 equity ETFs, daily', 'S\\&P 500, DAX, BET, Bitcoin, 14 acțiuni și 3 ETF-uri pe acțiuni din SUA, zilnic') + ' & EODHD & ' + T('QML, MIDAS, DCC', 'QML, MIDAS, DCC'),
     T('EUR/RON reference rate', 'cursul de referință EUR/RON') + ' & BNR & QML',
     T('US industrial production, PPI finished goods (monthly)', 'producția industrială și IPP pentru bunuri finite ale SUA (lunar)') + ' & FRED (INDPRO, WPSFD49207) & GARCH-MIDAS'],
    size='scriptsize') + items(
    T('The Oxford-Man library ended in February 2022 (archived copy, cited as its terms require); Binance one-minute data extend the realised measures to 18 September 2026; a calibrated simulation gives the theory a known truth',
      'Biblioteca Oxford-Man nu mai este actualizată din februarie 2022 (copie arhivată, citată conform condițiilor ei); datele Binance la un minut extind măsurile realizate pînă la 18 septembrie 2026; o simulare calibrată oferă teoriei un adevăr cunoscut'),
    T('RV: realised variance; BV: bipower variation; PPI: producer price index', 'RV: varianța realizată; BV: variația bipower; IPP (PPI): indicele prețurilor producției')), 'footnotesize')

D.frame(T('From the trading floor to the tick', 'De la sala de tranzacționare la fiecare tranzacție'), two(
    ph('nyse', T('New York Stock Exchange, 1908', 'Bursa din New York, 1908'), h='0.34\\textheight'),
    items(T(r'1982--1986: ARCH and GARCH \refEng, \refBol: volatility as a filtered conditional variance of daily returns', r'1982--1986: ARCH și GARCH \refEng, \refBol: volatilitatea ca varianță condiționată filtrată a randamentelor zilnice'),
          T(r'1992--2004: QML theory \refBW, \refLH, \refLum, \refFZa; components \refEL; DCC \refEngD', r'1992--2004: teoria QML \refBW, \refLH, \refLum, \refFZa; componente \refEL; DCC \refEngD'),
          T(r'1998--2008: realised variance \refAB, \refABDL, \refBNSa; bipower variation \refBNSb; noise and kernels \refZMA, \refBNHLSa', r'1998--2008: varianța realizată \refAB, \refABDL, \refBNSa; variația bipower \refBNSb; zgomot și kernel-uri \refZMA, \refBNHLSa'),
          T(r'2009--2019: HAR \refCor, Realized GARCH \refHHS, GARCH-MIDAS \refEGS, HARQ \refBPQ, DCC-NL \refELW', r'2009--2019: HAR \refCor, Realized GARCH \refHHS, GARCH-MIDAS \refEGS, HARQ \refBPQ, DCC-NL \refELW'),
          T('Today: high-frequency data are cheap; the questions are statistical (noise, jumps, dimension, evaluation)', 'Astăzi: datele de înaltă frecvență sînt ieftine; întrebările sînt statistice (zgomot, salturi, dimensiune, evaluare)')), '0.42', '0.56'), 'footnotesize')

# =============================================================================
# 1. QML
# =============================================================================
D.section('Quasi-maximum likelihood for GARCH', 'Verosimilitatea cvasi-maximă pentru GARCH')

D.frame(T('From TSA to this chapter', 'De la TSA la acest capitol'), items(
    (T(r'Known (TSA, Chapter 5): GARCH(1,1), GJR, EGARCH, the news impact curve, ML with Gaussian and Student-$t$ errors, QLIKE; (TSA, Chapter 14): CCC and DCC',
       r'Cunoscut (TSA, Capitolul 5): GARCH(1,1), GJR, EGARCH, curba de impact a știrilor, ML cu erori gaussiene și Student-$t$, QLIKE; (TSA, Capitolul 14): CCC și DCC'),
     []),
    (T('New here', 'Nou aici'),
     [T('why Gaussian ML still works when returns are not Gaussian, and which standard errors are then valid',
        'de ce ML gaussian funcționează și cînd randamentele nu sînt gaussiene și ce erori standard sînt atunci valide'),
      T('volatility with a slow, macro-driven component; volatility measured from intraday prices, with its own sampling error',
        'volatilitate cu o componentă lentă, determinată de factori macroeconomici; volatilitate măsurată din prețurile intraday, cu propria eroare de eșantionare'),
      T('models that use realised measures; evaluation against a noisy target; covariance matrices with many assets',
        'modele care folosesc măsuri realizate; evaluarea față de o țintă zgomotoasă; matrice de covarianță cu multe active')]),
    T('Stochastic volatility (a latent log-variance with its own shock): Chapter 6; Markov-switching GARCH: Chapter 7; VaR and ES backtesting: Chapter 9; rough volatility: Chapter 10',
      'Volatilitatea stochastică (un logaritm al varianței latent, cu propriul șoc): Capitolul 6; GARCH cu schimbare de regim: Capitolul 7; backtesting pentru VaR și ES: Capitolul 9; rough volatility: Capitolul 10')), 'small')

D.frame(T('The Gaussian quasi-likelihood (1/2): the model', 'Cvasi-verosimilitatea gaussiană (1/2): modelul'), items(
    T(r'The return shock is a volatility times a standardised shock; the variance follows a GARCH(1,1) recursion',
      r'Șocul randamentului este produsul dintre volatilitate și un șoc standardizat; varianța urmează recursia GARCH(1,1)'
      ) + r'''
    \[ \varepsilon_t = \sigma_t(\theta_0)\,\eta_t, \qquad \sigma^2_t(\theta) = \omega + \alpha\varepsilon^2_{t-1} + \beta\sigma^2_{t-1}(\theta) \]''',
    (T('Notation', 'Notațiile'),
     [T(r'$\varepsilon_t$: the demeaned return of day $t$; $\sigma^2_t(\theta)$: its variance conditional on the past $\mathcal F_{t-1}$ (the information up to day $t-1$)',
        r'$\varepsilon_t$: randamentul centrat al zilei $t$; $\sigma^2_t(\theta)$: varianța lui condiționată de trecutul $\mathcal F_{t-1}$ (informația pînă în ziua $t-1$)'),
      T(r'$\eta_t$: i.i.d. standardised shock, $\E\eta_t = 0$, $\E\eta_t^2 = 1$; its law (Normal, Student-$t$, skewed) is unknown',
        r'$\eta_t$: șoc standardizat i.i.d., $\E\eta_t = 0$, $\E\eta_t^2 = 1$; legea lui (distribuția Normală, Student-$t$, asimetrică) este necunoscută'),
      T(r'$\theta = (\omega, \alpha, \beta)$, true value $\theta_0$: $\omega > 0$ sets the level, $\alpha \ge 0$ the reaction to yesterday\'s squared shock, $\beta \ge 0$ the persistence of yesterday\'s variance',
        r'$\theta = (\omega, \alpha, \beta)$, cu valoarea adevărată $\theta_0$: $\omega > 0$ fixează nivelul, $\alpha \ge 0$ reacția la pătratul șocului de ieri, $\beta \ge 0$ persistența varianței de ieri')]),
    T(r'The recursion starts from an arbitrary $\sigma^2_1$; the effect of the start vanishes geometrically when $\beta < 1$',
      r'Recursia pornește de la un $\sigma^2_1$ arbitrar; efectul valorii de start dispare geometric cînd $\beta < 1$')), 'small')

D.frame(T('The Gaussian quasi-likelihood (2/2): estimator and score', 'Cvasi-verosimilitatea gaussiană (2/2): estimatorul și scorul'), items(
    (T(r'QMLE: maximise the Gaussian log-likelihood, used as an estimating equation even if $\eta_t$ is not Gaussian',
       r'QMLE: se maximizează log-verosimilitatea gaussiană, folosită ca ecuație de estimare chiar dacă $\eta_t$ nu este gaussian'
       ) + r'''
    \[ \hat\theta = \arg\max_\theta \sum_{t=1}^T \ell_t(\theta), \qquad \ell_t(\theta) = -\frac12\Big(\ln\sigma^2_t(\theta) + \frac{\varepsilon_t^2}{\sigma^2_t(\theta)}\Big) \]''',
     [T(r'$\ell_t$: the Gaussian log-density of day $t$ without its constant; $T$: number of days; $\hat\theta$: the estimate',
        r'$\ell_t$: log-densitatea gaussiană a zilei $t$, fără constantă; $T$: numărul de zile; $\hat\theta$: valoarea estimată')]),
    (T(r'The score, the gradient of $\ell_t$, has conditional mean zero at the true value',
       r'Scorul, adică gradientul lui $\ell_t$, are media condiționată zero în valoarea adevărată'
       ) + r'''
    \[ s_t(\theta) = \frac{\partial\ell_t}{\partial\theta} = \frac12\Big(\frac{\varepsilon_t^2}{\sigma_t^2} - 1\Big)\frac{1}{\sigma^2_t}\frac{\partial\sigma^2_t}{\partial\theta} \]''',
     [T(r'at $\theta_0$, $\varepsilon_t^2/\sigma_t^2 = \eta_t^2$, hence $\E(s_t | \mathcal F_{t-1}) = 0$ because $\E\eta_t^2 = 1$',
        r'în $\theta_0$, $\varepsilon_t^2/\sigma_t^2 = \eta_t^2$, deci $\E(s_t | \mathcal F_{t-1}) = 0$, pentru că $\E\eta_t^2 = 1$'),
      T('only the conditional variance must be right; the shape of the law of $\\eta_t$ is never used', 'doar varianța condiționată trebuie să fie corect specificată; forma legii lui $\\eta_t$ nu se folosește niciodată')]),
    (T(r'The score is a martingale difference (conditional mean zero given the past)',
       r'Scorul este o diferență de martingal (media condiționată de trecut este zero)'),
     [T(r'a CLT for martingales gives asymptotic normality without independence of $\varepsilon_t$',
        r'o TLC pentru martingale dă normalitatea asimptotică fără independența lui $\varepsilon_t$')])), 'small')

D.frame(T('Consistency and asymptotic normality (1/2): stationarity and consistency', 'Consistența și normalitatea asimptotică (1/2): staționaritatea și consistența'), items(
    (T(r'GARCH(1,1) is strictly stationary if and only if the log of the daily variance multiplier has a negative mean',
       r'GARCH(1,1) este strict staționar dacă și numai dacă logaritmul multiplicatorului zilnic al varianței are media negativă'
       ) + r'''
    \[ \E\ln(\alpha_0\eta_t^2 + \beta_0) < 0 \]''',
     [T(r'$\alpha_0\eta_t^2 + \beta_0$: the factor by which a shock to the variance is carried from one day to the next; $\alpha_0, \beta_0$: true values',
        r'$\alpha_0\eta_t^2 + \beta_0$: factorul cu care un șoc al varianței este transmis de la o zi la următoarea; $\alpha_0, \beta_0$: valorile adevărate'),
      T(r'by Jensen\'s inequality, weaker than $\alpha_0 + \beta_0 < 1$ (finite variance): IGARCH ($\alpha_0 + \beta_0 = 1$) is strictly stationary, and $\E\varepsilon_t^2$ may be infinite',
        r'prin inegalitatea lui Jensen, condiția este mai slabă decît $\alpha_0 + \beta_0 < 1$ (varianță finită): IGARCH ($\alpha_0 + \beta_0 = 1$) este strict staționar, iar $\E\varepsilon_t^2$ poate fi infinită'),
      T(r'\refLH, \refLum: GARCH(1,1), including IGARCH; \refBHK, \refFZa: GARCH($p,q$) under strict stationarity', r'\refLH, \refLum: GARCH(1,1), inclusiv IGARCH; \refBHK, \refFZa: GARCH($p,q$) sub staționaritate strictă')]),
    (T(r'Consistency of $\hat\theta$ \refFZa', r'Consistența lui $\hat\theta$ \refFZa'),
     [T(r'conditions: strict stationarity, $\theta_0$ in a compact parameter set, identifiability ($\eta_t^2$ is not a constant)',
        r'condiții: staționaritate strictă, $\theta_0$ într-o mulțime compactă de parametri, identificabilitate ($\eta_t^2$ nu este o constantă)'),
      T(r'no moment of $\varepsilon_t$ is needed', r'nu este nevoie de niciun moment al lui $\varepsilon_t$')]),
    T(r'Even explosive GARCH ($\E\ln(\alpha_0\eta^2 + \beta_0) > 0$): $(\hat\alpha, \hat\beta)$ remain consistent and asymptotically normal, $\omega$ is not identified \refJR',
      r'Chiar și pentru GARCH exploziv ($\E\ln(\alpha_0\eta^2 + \beta_0) > 0$), $(\hat\alpha, \hat\beta)$ rămîn consistenți și asimptotic normali, iar $\omega$ nu este identificat \refJR')), 'small')

D.frame(T('Consistency and asymptotic normality (2/2): the limit law', 'Consistența și normalitatea asimptotică (2/2): legea limită'), items(
    (T(r'With $\theta_0$ interior to the parameter set and a finite fourth moment of $\eta_t$, the estimator is asymptotically normal',
       r'Dacă $\theta_0$ este interior mulțimii parametrilor și $\eta_t$ are momentul de ordinul patru finit, estimatorul este asimptotic normal'
       ) + r'''
    \[ \sqrt T(\hat\theta - \theta_0) \to N\big(0, (\kappa_\eta - 1)J^{-1}\big), \qquad J = \E\Big[\frac{1}{\sigma^4_t}\frac{\partial\sigma^2_t}{\partial\theta}\frac{\partial\sigma^2_t}{\partial\theta'}\Big] \]''',
     [T(r'$\kappa_\eta = \E\eta_t^4$: kurtosis of the shock ($3$ for the Normal distribution); $\kappa_\eta - 1 = \Var(\eta_t^2)$',
        r'$\kappa_\eta = \E\eta_t^4$: kurtosis-ul șocului ($3$ pentru distribuția Normală); $\kappa_\eta - 1 = \Var(\eta_t^2)$'),
      T(r'$J$: a $3 \times 3$ matrix, the mean outer product of the relative sensitivities $\sigma_t^{-2}\partial\sigma^2_t/\partial\theta$; $\to$: convergence in distribution as $T \to \infty$',
        r'$J$: o matrice $3 \times 3$, media produsului exterior al sensibilităților relative $\sigma_t^{-2}\partial\sigma^2_t/\partial\theta$; $\to$: convergența în distribuție cînd $T \to \infty$'),
      T(r'reading: the sampling variance of $\hat\theta$ grows linearly with the kurtosis of the shocks',
        r'interpretare: varianța de eșantionare a lui $\hat\theta$ crește liniar cu kurtosis-ul șocurilor')]),
    (T(r'Boundary: if $\alpha_0 = 0$, $\theta_0$ is not interior and the limit is the projection of a normal vector on a cone',
       r'Frontiera: dacă $\alpha_0 = 0$, $\theta_0$ nu este interior, iar limita este proiecția unui vector normal pe un con'),
     [T(r'this is why TSA, Chapter 5 tests ARCH effects one-sided', r'de aceea TSA, Capitolul 5 testează efectele ARCH unilateral')])), 'small')

D.frame(T('The sandwich and the Bollerslev--Wooldridge standard errors (1/2)', 'Sandwich-ul și erorile standard Bollerslev--Wooldridge (1/2)'), items(
    (T(r'General QML result: the asymptotic variance is a ``sandwich\'\' of two matrices',
       r'Rezultatul general QML: varianța asimptotică este un „sandwich” format din două matrice'
       ) + r'''
    \[ \sqrt T(\hat\theta - \theta_0) \to N(0, A^{-1}B\,A^{-1}), \qquad A = -\E\frac{\partial^2\ell_t}{\partial\theta\,\partial\theta'}, \qquad B = \E\,s_ts_t' \]''',
     [T(r'$A$: the expected negative Hessian (curvature of the log-likelihood); $B$: the variance of the score $s_t$',
        r'$A$: hessiana negativă așteptată (curbura log-verosimilității); $B$: varianța scorului $s_t$'),
      T(r'if the likelihood is the true one, $A = B$ (information equality) and the variance reduces to $A^{-1}$; under QML, $A \ne B$',
        r'dacă verosimilitatea este cea adevărată, $A = B$ (egalitatea informațională), iar varianța devine $A^{-1}$; sub QML, $A \ne B$')]),
    (T(r'For GARCH both matrices are proportional to $J$ (Appendix)', r'Pentru GARCH, ambele matrice sînt proporționale cu $J$ (Anexa)'
       ) + r'''
    \[ A = \tfrac12J, \qquad B = \tfrac{\kappa_\eta - 1}{4}J, \qquad A^{-1}B\,A^{-1} = (\kappa_\eta - 1)J^{-1} \]''',
     [T(r'the sandwich recovers the limit law of the previous slide, for any law of $\eta_t$ with $\kappa_\eta < \infty$',
        r'sandwich-ul regăsește legea limită de pe slide-ul anterior, pentru orice lege a lui $\eta_t$ cu $\kappa_\eta < \infty$')])), 'small')

D.frame(T('The sandwich and the Bollerslev--Wooldridge standard errors (2/2)', 'Sandwich-ul și erorile standard Bollerslev--Wooldridge (2/2)'), items(
    (T(r'Three ways to compute standard errors (s.e.)', r'Trei moduri de a calcula erorile standard'),
     [T(r'Hessian only: $A^{-1} = 2J^{-1}$, correct only if $\kappa_\eta = 3$; too small by the factor $\sqrt{(\kappa_\eta - 1)/2}$ when $\kappa_\eta > 3$',
        r'doar din hessiană: $A^{-1} = 2J^{-1}$, corect doar dacă $\kappa_\eta = 3$; prea mici cu factorul $\sqrt{(\kappa_\eta - 1)/2}$ cînd $\kappa_\eta > 3$'),
      T(r'outer product of the scores (OPG): $B^{-1} = \frac{4}{\kappa_\eta - 1}J^{-1}$, even smaller when $\kappa_\eta > 3$',
        r'din produsul exterior al scorurilor (OPG): $B^{-1} = \frac{4}{\kappa_\eta - 1}J^{-1}$, și mai mici cînd $\kappa_\eta > 3$'),
      T(r'sandwich \refBW: $\hat A^{-1}\hat B\hat A^{-1}$, valid whatever the law of $\eta_t$ (with $\kappa_\eta < \infty$)',
        r'sandwich \refBW: $\hat A^{-1}\hat B\hat A^{-1}$, valabil oricare ar fi legea lui $\eta_t$ (cu $\kappa_\eta < \infty$)')]),
    (T(r'Estimates used by Bollerslev and Wooldridge', r'Estimațiile folosite de Bollerslev și Wooldridge'),
     [T(r'$\hat A$: the observed Hessian of $-\frac1T\sum_t\ell_t$ at $\hat\theta$; $\hat B = \frac1T\sum_t\hat s_t\hat s_t\'$, with $\hat s_t = s_t(\hat\theta)$ the estimated score',
        r'$\hat A$: hessiana observată a lui $-\frac1T\sum_t\ell_t$ în $\hat\theta$; $\hat B = \frac1T\sum_t\hat s_t\hat s_t\'$, cu $\hat s_t = s_t(\hat\theta)$ scorul estimat')]),
    (T(r'Robust Wald and score tests use the sandwich', r'Testele Wald și de tip scor robuste folosesc sandwich-ul'),
     [T(r'the quasi-likelihood-ratio (quasi-LR) statistic is no longer $\chi^2$, but a weighted sum of $\chi^2_1$ variables (chi-square with one degree of freedom)',
        r'statistica raportului de cvasi-verosimilitate (cvasi-LR) nu mai are distribuția $\chi^2$, ci este o sumă ponderată de variabile $\chi^2_1$ (hi-pătrat cu un grad de libertate)')])), 'small')

chart(T('Hessian against sandwich: a Monte Carlo', 'Hessiana față de sandwich: un experiment Monte Carlo'), 'ats_ch8_qmle_sim', 'ATS_ch8_qmle', [
    T(r'GARCH(1,1) with $(\omega, \alpha, \beta) = (0.05, 0.08, 0.90)$, $T = @{qs.T}$, @{qs.reps} replications; Gaussian QML in each; histogram of $(\hat\alpha - \alpha_0)/\widehat{\mathrm{se}}$',
      r'GARCH(1,1) cu $(\omega, \alpha, \beta) = (0.05, 0.08, 0.90)$, $T = @{qs.T}$, @{qs.reps} de replicări; QML gaussian în fiecare; histograma lui $(\hat\alpha - \alpha_0)/\widehat{\mathrm{se}}$')],
    h='0.6\\textheight')

interp(('the Monte Carlo', 'experimentului Monte Carlo'), [
    T(r'Gaussian $\eta$: coverage of nominal 95\% intervals for $\alpha$ is @{qs.normal.h.a}\% (Hessian) and @{qs.normal.bw.a}\% (sandwich): both fine',
      r'$\eta$ gaussian: acoperirea intervalelor de 95\% pentru $\alpha$ este @{qs.normal.h.a}\% (hessiană) și @{qs.normal.bw.a}\% (sandwich): ambele corecte'),
    T(r'Student-$t(5)$, $\kappa_\eta = 9$: Hessian intervals cover @{qs.t5.h.a}\% for $\alpha$ and @{qs.t5.h.b}\% for $\beta$; sandwich intervals @{qs.t5.bw.a}\% and @{qs.t5.bw.b}\%',
      r'Student-$t(5)$, $\kappa_\eta = 9$: intervalele din hessiană acoperă @{qs.t5.h.a}\% pentru $\alpha$ și @{qs.t5.h.b}\% pentru $\beta$; intervalele sandwich @{qs.t5.bw.a}\% și @{qs.t5.bw.b}\%'),
    T(r'The theory predicts the factor $\sqrt{(9 - 1)/2} = 2$ between the two standard errors; the point estimates are the same',
      r'Teoria prezice factorul $\sqrt{(9 - 1)/2} = 2$ între cele două erori standard; estimațiile punctuale sînt aceleași'),
    T('With fat tails, a Hessian-based $t$-test of $\\alpha$ rejects far too often: report sandwich standard errors by default',
      'Cu cozi groase, un test $t$ pentru $\\alpha$ construit cu erorile standard din hessiană respinge mult prea des: raportați implicit erorile standard sandwich')])

chart(T('Robust and naive standard errors in five markets', 'Erori standard robuste și naive pe cinci piețe'), 'ats_ch8_qmle_markets', 'ATS_ch8_qmle', [
    T(r'Gaussian QML of GARCH(1,1), daily returns 2010--2026; bars: sandwich s.e. divided by Hessian s.e.; labels: kurtosis $\hat\kappa_\eta$ of the standardised residuals',
      r'QML gaussian pentru GARCH(1,1), randamente zilnice 2010--2026; bare: eroarea standard sandwich împărțită la eroarea standard din hessiană; etichete: kurtosis-ul $\hat\kappa_\eta$ al reziduurilor standardizate')],
    h='0.6\\textheight')

interp(('the five markets', 'celor cinci piețe'), [
    T(r'S\&P 500: $\hat\alpha = @{qm.sp500.a}$ with s.e. @{qm.sp500.a.h} (Hessian) against @{qm.sp500.a.bw} (sandwich); $\hat\kappa_\eta = @{qm.sp500.k}$, theoretical factor @{qm.sp500.th}',
      r'S\&P 500: $\hat\alpha = @{qm.sp500.a}$, cu eroarea standard @{qm.sp500.a.h} (hessiană) față de @{qm.sp500.a.bw} (sandwich); $\hat\kappa_\eta = @{qm.sp500.k}$, factorul teoretic @{qm.sp500.th}'),
    T(r'BET: $\hat\kappa_\eta = @{qm.bet.k}$, the sandwich s.e. of $\hat\alpha$ is @{qm.bet.a.r} times larger; EUR/RON (managed float): @{qm.eurron.a.r} times, $\hat\kappa_\eta = @{qm.eurron.k}$',
      r'BET: $\hat\kappa_\eta = @{qm.bet.k}$, eroarea standard sandwich a lui $\hat\alpha$ este de @{qm.bet.a.r} ori mai mare; EUR/RON (managed float): de @{qm.eurron.a.r} ori, $\hat\kappa_\eta = @{qm.eurron.k}$'),
    T(r'The ratios track $\sqrt{(\hat\kappa_\eta - 1)/2}$ only roughly: in the data $\eta_t$ is not i.i.d., and the sandwich does not need it to be',
      r'Rapoartele urmează doar aproximativ $\sqrt{(\hat\kappa_\eta - 1)/2}$: în date, $\eta_t$ nu este i.i.d., iar sandwich-ul nu are nevoie de această ipoteză'),
    T(r'Student-$t$ ML raises the log-likelihood by @{qm.sp500.dll} (S\&P 500) and @{qm.bet.dll} (BET), but is consistent only if the $t$ shape is right; QML needs only the variance equation',
      r'ML Student-$t$ crește log-verosimilitatea cu @{qm.sp500.dll} (S\&P 500) și @{qm.bet.dll} (BET), dar este consistent doar dacă forma $t$ este corectă; QML are nevoie doar de ecuația varianței')])

D.recap(('QML for GARCH', 'QML pentru GARCH'), [
    T('Gaussian QML is consistent if the variance equation is right, whatever the shape of the innovations', 'QML gaussian este consistent dacă ecuația varianței este corectă, oricare ar fi forma inovațiilor'),
    T('Strict stationarity, not finite variance, is what the theory needs; IGARCH and even explosive GARCH are covered', 'Teoria are nevoie de staționaritate strictă, nu de varianță finită; IGARCH și chiar GARCH exploziv sînt acoperite'),
    T(r'With fat tails, Hessian standard errors are too small by $\sqrt{(\kappa_\eta - 1)/2}$; use Bollerslev--Wooldridge', r'Cu cozi groase, erorile standard din hessiană sînt prea mici cu factorul $\sqrt{(\kappa_\eta - 1)/2}$; folosiți Bollerslev--Wooldridge')])

# =============================================================================
# 2. COMPONENTE: GARCH-X, COMPONENT GARCH, GARCH-MIDAS
# =============================================================================
D.section('Long-run and short-run volatility', 'Volatilitatea de termen lung și de termen scurt')

D.frame(T('GARCH with exogenous variables', 'GARCH cu variabile exogene'), items(
    (T(r'GARCH-X: yesterday\'s value of an observed variable enters the variance equation',
       r'GARCH-X: valoarea de ieri a unei variabile observate intră în ecuația varianței'
       ) + r'''
    \[ \sigma^2_t = \omega + \alpha\varepsilon^2_{t-1} + \beta\sigma^2_{t-1} + \pi'x_{t-1} \]''',
     [T(r'$x_{t-1}$: vector of exogenous variables known at the end of day $t-1$; $\pi$: their loadings ($\pi\'x$: the weighted sum)',
        r'$x_{t-1}$: vectorul variabilelor exogene cunoscute la sfîrșitul zilei $t-1$; $\pi$: coeficienții lor ($\pi\'x$: suma ponderată)'),
      T(r'positivity of $\sigma^2_t$: $x_{t-1} \ge 0$ and $\pi \ge 0$, or a specification in logs',
        r'pozitivitatea lui $\sigma^2_t$: $x_{t-1} \ge 0$ și $\pi \ge 0$ sau o specificare în logaritmi')]),
    (T(r'Candidates for $x_t$: a realised measure (leads to HEAVY and Realized GARCH below), the VIX, a macro or policy-uncertainty index, trading volume',
       r'Candidați pentru $x_t$: o măsură realizată (duce la HEAVY și Realized GARCH, mai jos), VIX, un indice macroeconomic sau de incertitudine a politicilor, volumul tranzacțiilor'),
     [T(r'QML theory carries over if $x_t$ is stationary and ergodic; its own dynamics need not be modelled for one-step forecasts',
        r'teoria QML se păstrează dacă $x_t$ este staționar și ergodic; dinamica lui nu trebuie modelată pentru prognoze cu un pas'),
      T(r'multi-step forecasts need a model for $x_t$: this is exactly what Realized GARCH and HEAVY add',
        r'prognozele cu mai mulți pași au nevoie de un model pentru $x_t$: exact acest lucru adaugă Realized GARCH și HEAVY')]),
    T(r'A slow variable (a monthly macro series) cannot enter a daily recursion at its own frequency: one needs a component structure (next slides)',
      r'O variabilă lentă (o serie macroeconomică lunară) nu poate intra în recursia zilnică la frecvența ei: este nevoie de o structură pe componente (slide-urile următoare)')), 'small')

D.frame(T('The component GARCH of Engle and Lee (1/2): the model', 'Component GARCH al lui Engle și Lee (1/2): modelul'), items(
    (T(r'\refEL: the variance is a slowly moving long-run level $q_t$ plus a transitory deviation from it',
       r'\refEL: varianța este suma dintre un nivel de termen lung $q_t$, care se mișcă lent, și o abatere tranzitorie de la acest nivel'
       ) + r'''
    \[ \sigma^2_t = q_t + \alpha(\varepsilon^2_{t-1} - q_{t-1}) + \beta(\sigma^2_{t-1} - q_{t-1}) \]
    \[ q_t = \omega + \rho q_{t-1} + \phi(\varepsilon^2_{t-1} - \sigma^2_{t-1}) \]''',
     [T(r'$q_t$: long-run (permanent) component; $\rho$: its persistence, close to 1; $\omega$: its intercept',
        r'$q_t$: componenta de termen lung (permanentă); $\rho$: persistența ei, apropiată de 1; $\omega$: termenul ei liber'),
      T(r'$\sigma^2_t - q_t$: transitory component; $\alpha$, $\beta$: its reaction and persistence, with $\alpha + \beta < \rho$',
        r'$\sigma^2_t - q_t$: componenta tranzitorie; $\alpha$, $\beta$: reacția și persistența ei, cu $\alpha + \beta < \rho$'),
      T(r'$\varepsilon^2_{t-1} - \sigma^2_{t-1}$: the variance surprise of yesterday (mean zero); $\phi$: how much of it moves the long-run level',
        r'$\varepsilon^2_{t-1} - \sigma^2_{t-1}$: surpriza de varianță de ieri (cu media zero); $\phi$: cît din această surpriză mută nivelul de termen lung')]),
    T(r'Both components are driven by the same shock: the model is a restricted GARCH(2,2)',
      r'Ambele componente sînt determinate de același șoc: modelul este un GARCH(2,2) restricționat')), 'small')

D.frame(T('The component GARCH of Engle and Lee (2/2): two speeds', 'Component GARCH al lui Engle și Lee (2/2): două viteze'), items(
    (T(r'Half-life: the number of days after which half of a shock to a component has died out',
       r'Timpul de înjumătățire: numărul de zile după care jumătate dintr-un șoc al unei componente a dispărut'
       ) + r'''
    \[ \mathrm{HL}_q = \frac{\ln(1/2)}{\ln\rho}, \qquad \mathrm{HL}_{\sigma - q} = \frac{\ln(1/2)}{\ln(\alpha + \beta)} \]''',
     [T(r'$\mathrm{HL}_q$: half-life of the long-run component; $\mathrm{HL}_{\sigma - q}$: half-life of the transitory component',
        r'$\mathrm{HL}_q$: timpul de înjumătățire al componentei de termen lung; $\mathrm{HL}_{\sigma - q}$: al componentei tranzitorii'),
      T(r'a persistence $\rho = 0.99$ gives about 69 days; $\alpha + \beta = 0.9$ gives about 6.6 days',
        r'o persistență $\rho = 0.99$ dă aproximativ 69 de zile; $\alpha + \beta = 0.9$ dă aproximativ 6,6 zile'),
      T(r'GARCH(1,1) forces a single half-life, $\ln 0.5/\ln(\alpha + \beta)$', r'GARCH(1,1) impune un singur timp de înjumătățire, $\ln 0.5/\ln(\alpha + \beta)$')]),
    (T(r'Two exponentials approximate a slowly decaying (hyperbolic) autocorrelation of squared returns over a finite range of lags',
       r'Două exponențiale aproximează, pe un interval finit de laguri, o autocorelație a pătratelor randamentelor care scade lent (hiperbolic)'),
     [T('long memory proper: Chapter 10', 'memoria lungă propriu-zisă: Capitolul 10')])), 'small')

chart(T('Component GARCH for the S\\&P 500', 'Component GARCH pentru S\\&P 500'), 'ats_ch8_cgarch', 'ATS_ch8_components', [
    T(r'Daily returns since 1990, $T = @{cg.T}$; Gaussian QML; annualised total volatility $\sqrt{252\sigma^2_t}$ and long-run component $\sqrt{252q_t}$',
      r'Randamente zilnice din 1990, $T = @{cg.T}$; QML gaussian; volatilitatea totală anualizată $\sqrt{252\sigma^2_t}$ și componenta de termen lung $\sqrt{252q_t}$')],
    h='0.6\\textheight')

interp(('the component model', 'modelului cu componente'), [
    T(r'$\hat\rho = @{cg.rho}$, $\hat\phi = @{cg.phi}$; transitory part $\hat\alpha + \hat\beta = @{cg.ab}$: half-lives @{cg.hll} days (long run) and @{cg.hls} days (short run)',
      r'$\hat\rho = @{cg.rho}$, $\hat\phi = @{cg.phi}$; partea tranzitorie $\hat\alpha + \hat\beta = @{cg.ab}$: timpi de înjumătățire de @{cg.hll} zile (termen lung) și @{cg.hls} zile (termen scurt)'),
    T(r'GARCH(1,1) on the same data: persistence @{cg.gp}, one half-life of @{cg.hlg} days, a compromise between the two',
      r'GARCH(1,1) pe aceleași date: persistența @{cg.gp}, un singur timp de înjumătățire de @{cg.hlg} zile, un compromis între cele două'),
    T(r'Quasi-LR statistic against GARCH(1,1): @{cg.LR}; under the null $\phi = 0$ the parameter $\rho$ is not identified (Davies problem), so the $\chi^2_2$ reference is only indicative',
      r'Statistica cvasi-LR față de GARCH(1,1): @{cg.LR}; sub ipoteza nulă $\phi = 0$ parametrul $\rho$ nu este identificat (problema Davies), deci referința $\chi^2_2$ este doar orientativă'),
    T('After 2008, 2020 and 2025 the long-run level stays high for months while daily volatility has already fallen: this matters for horizons beyond a few weeks',
      'După 2008, 2020 și 2025, nivelul de termen lung rămîne ridicat luni de zile, deși volatilitatea zilnică a scăzut deja: acest lucru contează pentru orizonturi de peste cîteva săptămîni')])

D.frame(T('GARCH-MIDAS (1/3): a macro-driven long-run component', 'GARCH-MIDAS (1/3): o componentă de termen lung determinată macroeconomic'), two(
    ph('ghysels', T('Eric Ghysels, 2019', 'Eric Ghysels, 2019'), h='0.26\\textheight'),
    items((T(r'\refEGS: the daily variance is the product of a monthly level $\tau_t$ and a daily factor $g_{i,t}$',
             r'\refEGS: varianța zilnică este produsul dintre un nivel lunar $\tau_t$ și un factor zilnic $g_{i,t}$'
             ) + r'''
    \[ r_{i,t} = \mu + \sqrt{\tau_t\,g_{i,t}}\;\eta_{i,t} \]''',
           [T(r'$r_{i,t}$: return of day $i$ of month $t$; $\mu$: mean return; $\eta_{i,t}$: i.i.d. shock with mean 0 and variance 1',
              r'$r_{i,t}$: randamentul zilei $i$ din luna $t$; $\mu$: randamentul mediu; $\eta_{i,t}$: șoc i.i.d. cu media 0 și varianța 1')]),
          (T(r'Short run: a GARCH(1,1) with mean 1, re-scaled by $\tau_t$', r'Termenul scurt: un GARCH(1,1) cu media 1, rescalat cu $\tau_t$'
             ) + r'''
    \[ g_{i,t} = (1 - \alpha - \beta) + \alpha\frac{(r_{i-1,t} - \mu)^2}{\tau_t} + \beta g_{i-1,t} \]''',
           [T(r'$\alpha$, $\beta$: reaction and persistence of the daily component, as in GARCH(1,1)',
              r'$\alpha$, $\beta$: reacția și persistența componentei zilnice, ca în GARCH(1,1)')])), '0.3', '0.68'), 'footnotesize')

D.frame(T('GARCH-MIDAS (2/3): the long-run component', 'GARCH-MIDAS (2/3): componenta de termen lung'), items(
    (T(r'Long run: MIDAS (mixed-data sampling) regression of $\ln\tau_t$ on $K$ lags of a monthly variable',
       r'Termenul lung: o regresie MIDAS (mixed-data sampling, eșantionare cu frecvențe mixte) a lui $\ln\tau_t$ pe $K$ laguri ale unei variabile lunare'
       ) + r'''
    \[ \ln\tau_t = m + \theta\sum_{k=1}^K\varphi_k(w)\,X_{t-k}, \qquad \varphi_k(w) \propto (1 - k/K)^{w - 1} \]''',
     [T(r'$X_{t-k}$: the monthly driver $k$ months ago; $m$: intercept; $\theta$: effect of the driver (sign: pro- or countercyclical)',
        r'$X_{t-k}$: factorul lunar de acum $k$ luni; $m$: termenul liber; $\theta$: efectul factorului (semnul arată dacă este prociclic sau anticiclic)'),
      T(r'$\varphi_k(w)$: beta lag weights, normalised to sum to 1 and restricted to decay \refGSV; $w \ge 1$: the larger $w$, the faster the decay; $w = 1$: equal weights',
        r'$\varphi_k(w)$: ponderi beta pe laguri, normalizate să însumeze 1 și restricționate să scadă \refGSV; $w \ge 1$: cu cît $w$ este mai mare, cu atît scad mai repede; $w = 1$: ponderi egale')]),
    (T(r'Choices of $X$', r'Alegeri pentru $X$'),
     [T(r'realised variance of past months, in levels: $\tau_t = m + \theta\sum_k\varphi_k(w)\mathrm{RV}_{t-k}$, with $\mathrm{RV}_{t-k}$ the sum of squared daily returns of month $t-k$',
        r'varianța realizată din lunile anterioare, în nivel: $\tau_t = m + \theta\sum_k\varphi_k(w)\mathrm{RV}_{t-k}$, cu $\mathrm{RV}_{t-k}$ suma pătratelor randamentelor zilnice din luna $t-k$'),
      T('macro data: industrial production growth, PPI inflation', 'date macroeconomice: creșterea producției industriale, inflația IPP')])), 'small')

D.frame(T('GARCH-MIDAS (3/3): identification, estimation and the variance ratio', 'GARCH-MIDAS (3/3): identificare, estimare și raportul de varianță'), items(
    (T(r'$\tau_t$ is constant within the month and $\E g_{i,t} = 1$: the split is identified by the different frequencies, without a filter for a latent variable',
       r'$\tau_t$ este constant în cadrul lunii, iar $\E g_{i,t} = 1$: descompunerea este identificată prin frecvențele diferite, fără un filtru pentru o variabilă latentă'),
     [T(r'Gaussian QML of all parameters $(\mu, \alpha, \beta, m, \theta, w)$ in one step; sandwich standard errors', r'QML gaussian pentru toți parametrii $(\mu, \alpha, \beta, m, \theta, w)$ într-un singur pas; erori standard sandwich')]),
    (T(r'Variance ratio: the share of the variation of log volatility explained by the long-run component',
       r'Raportul de varianță: ponderea variației logaritmului volatilității explicată de componenta de termen lung'
       ) + r'''
    \[ \mathrm{VR} = \frac{\Var(\ln\tau_t)}{\Var(\ln(\tau_t\,g_{i,t}))} \in [0, 1] \]''',
     [T(r'VR close to 0: the long-run component is almost flat; close to 1: it carries most of the variation',
        r'VR apropiat de 0: componenta de termen lung este aproape constantă; apropiat de 1: ea preia cea mai mare parte a variației'),
      T(r'a macro variable can be significant ($\hat\theta \ne 0$) and still explain little of daily volatility (small VR)', r'o variabilă macroeconomică poate fi semnificativă ($\hat\theta \ne 0$) și totuși să explice puțin din volatilitatea zilnică (VR mic)')]),
    T(r'Inference on $w$ is nonstandard when $\theta = 0$ ($w$ is then not identified) and at the boundary $w = 1$',
      r'Inferența asupra lui $w$ este nestandard cînd $\theta = 0$ ($w$ nu este atunci identificat) și la frontiera $w = 1$'),
    T(r'Extensions: two-sided weights, several regressors, a second (daily) component \refCK; forecasts beyond one month use only the long-run part',
      r'Extensii: ponderi nerestricționate, mai mulți regresori, o a doua componentă (zilnică) \refCK; prognozele de peste o lună folosesc doar partea de termen lung')), 'small')

D.frame(T('Case study: Engle, Ghysels and Sohn (2013) on our data', 'Studiu de caz: Engle, Ghysels și Sohn (2013) pe datele noastre'), items(
    (T(r'\textbf{Question} of \refEGS: does the stock market\'s long-run volatility move with macroeconomic fundamentals (output growth, inflation)?',
       r'\textbf{Întrebarea} din \refEGS: se mișcă volatilitatea de termen lung a pieței de acțiuni împreună cu fundamentele macroeconomice (creșterea producției, inflația)?'),
     [T('their sample of US stock returns is much longer than ours; their benchmark long-run component is a fixed-window realised variance',
        'eșantionul lor de randamente ale acțiunilor din SUA este mult mai lung decît al nostru; componenta lor de termen lung de referință este o varianță realizată pe ferestre fixe')]),
    (T(r'\textbf{Our replication}: S\&P 500 daily returns, common sample from @{md.first}, $T = @{md.T}$; $K = @{md.K}$ monthly lags; restricted beta weights',
       r'\textbf{Replicarea noastră}: randamentele zilnice ale S\&P 500, eșantion comun din @{md.first}, $T = @{md.T}$; $K = @{md.K}$ laguri lunare; ponderi beta restricționate'),
     [T(r'three long-run drivers: monthly realised variance (sum of squared daily returns), industrial production growth (FRED INDPRO), PPI inflation (FRED WPSFD49207)',
        r'trei factori de termen lung: varianța realizată lunară (suma pătratelor randamentelor zilnice), creșterea producției industriale (FRED INDPRO), inflația IPP (FRED WPSFD49207)'),
      T('all models against GARCH(1,1) on the same days; QML with sandwich standard errors', 'toate modelele comparate cu GARCH(1,1) pe aceleași zile; QML cu erori standard sandwich')]),
    T('Extension for a project: Romanian industrial production and the BET (Seminar 8, B5); real-time vintages of the macro data',
      'Extindere pentru un proiect: producția industrială a României și BET (Seminarul 8, B5); edițiile în timp real ale datelor macroeconomice')), 'small')

chart(T('GARCH-MIDAS for the S\\&P 500', 'GARCH-MIDAS pentru S\\&P 500'), 'ats_ch8_garch_midas', 'ATS_ch8_components', [
    T(r'Annualised $\sqrt{252\tau_tg_{i,t}}$ of the industrial-production model and the long-run components $\sqrt{252\tau_t}$ of the three models',
      r'$\sqrt{252\tau_tg_{i,t}}$ anualizat pentru modelul cu producția industrială și componentele de termen lung $\sqrt{252\tau_t}$ ale celor trei modele')],
    h='0.6\\textheight')

D.frame(T('GARCH-MIDAS estimates', 'Estimațiile GARCH-MIDAS'), table(
    'lcccccc', T(r'\textbf{Long-run driver}', r'\textbf{Factorul de termen lung}') + r' & $\hat\alpha$ & $\hat\beta$ & $\hat\theta$ (s.e.) & $\hat w$ & VR (\%) & BIC',
    [T('realised variance (levels)', 'varianța realizată (nivel)') + r' & @{md.rv.a} & @{md.rv.b} & @{md.rv.th} (@{md.rv.th.se}) & @{md.rv.w} & @{md.rv.vr} & @{md.rv.bic}',
     T('industrial production growth', 'creșterea producției industriale') + r' & @{md.ip.a} & @{md.ip.b} & @{md.ip.th} (@{md.ip.th.se}) & @{md.ip.w} & @{md.ip.vr} & @{md.ip.bic}',
     T('PPI inflation', 'inflația IPP') + r' & @{md.ppi.a} & @{md.ppi.b} & @{md.ppi.th} (@{md.ppi.th.se}) & @{md.ppi.w} & @{md.ppi.vr} & @{md.ppi.bic}',
     r'GARCH(1,1) & & & & & & @{md.gbic}'], size='scriptsize') + items(
    T(r'Same days for all models; BIC $= -2\ln L + k\ln T$ (lower is better); s.e.: Bollerslev--Wooldridge', r'Aceleași zile pentru toate modelele; BIC $= -2\ln L + k\ln T$ (mai mic este mai bine); erori standard: Bollerslev--Wooldridge')), 'small')

interp(('GARCH-MIDAS', 'modelului GARCH-MIDAS'), [
    T(r'Realised variance as the slow driver: $\hat\theta = @{md.rv.th}$ ($t = @{md.rv.t}$), VR = @{md.rv.vr}\%, BIC below GARCH(1,1): a long-run component exists',
      r'Varianța realizată ca factor lent: $\hat\theta = @{md.rv.th}$ ($t = @{md.rv.t}$), VR = @{md.rv.vr}\%, BIC sub GARCH(1,1): o componentă de termen lung există'),
    T(r'Industrial production: $\hat\theta = @{md.ip.th}$ ($t = @{md.ip.t}$), the countercyclical sign of \refEGS, but VR only @{md.ip.vr}\% and a higher BIC than GARCH(1,1)',
      r'Producția industrială: $\hat\theta = @{md.ip.th}$ ($t = @{md.ip.t}$), semnul anticiclic din \refEGS, dar VR doar @{md.ip.vr}\% și un BIC mai mare decît GARCH(1,1)'),
    T(r'PPI inflation: $\hat w$ at the boundary 1 (flat weights) and $\hat\theta$ imprecise: no evidence in 1993--2026',
      r'Inflația IPP: $\hat w$ la frontiera 1 (ponderi egale) și $\hat\theta$ imprecis: nicio dovadă în 1993--2026'),
    T('Replication verdict: the qualitative sign survives, the strength does not; macro effects need long samples with deep recessions, which is why the original study uses a much longer history',
      'Verdictul replicării: semnul calitativ se păstrează, intensitatea nu; efectele macroeconomice au nevoie de eșantioane lungi, cu recesiuni adînci, motiv pentru care studiul original folosește o istorie mult mai lungă')])

D.recap(('Long-run components', 'componentele de termen lung'), [
    T('Volatility has at least two speeds; a single GARCH persistence averages them', 'Volatilitatea are cel puțin două viteze; o singură persistență GARCH le face media'),
    T('GARCH-MIDAS lets a monthly variable drive the long-run level; identification comes from the mixed frequencies', 'GARCH-MIDAS permite unei variabile lunare să determine nivelul de termen lung; identificarea vine din frecvențele mixte'),
    T('Report VR and BIC next to $\\hat\\theta$: significance is not importance', 'Raportați VR și BIC alături de $\\hat\\theta$: semnificația statistică nu înseamnă importanță')])

# =============================================================================
# 3. MĂSURI REALIZATE: TEORIE, ZGOMOT, KERNEL-URI
# =============================================================================
D.section('Realised measures: theory, noise and kernels', 'Măsuri realizate: teorie, zgomot și kernel-uri')

D.frame(T('Prices as Itô semimartingales (1/2): the model', 'Prețurile ca semimartingale Itô (1/2): modelul'), items(
    (T(r'Within day $t$, the log price moves by a drift, a Brownian part scaled by the spot volatility, and jumps',
       r'În cursul zilei $t$, logaritmul prețului se modifică printr-un drift, o componentă browniană scalată cu volatilitatea instantanee și salturi'
       ) + r'''
    \[ dX_s = \mu_s\,ds + \sigma_s\,dW_s + dJ_s, \qquad s \in [0, 1] \]''',
     [T(r'$X_s$: log price at intraday time $s$ (the day is rescaled to $[0, 1]$); $\mu_s$: drift; $W_s$: standard Brownian motion',
        r'$X_s$: logaritmul prețului la momentul intraday $s$ (ziua este rescalată la $[0, 1]$); $\mu_s$: drift-ul; $W_s$: mișcarea browniană standard'),
      T(r'$\sigma_s$: stochastic spot (instantaneous) volatility; $J_s$: a jump process with finitely many jumps per day, $\Delta J_s$: the jump at time $s$',
        r'$\sigma_s$: volatilitatea instantanee (spot), stochastică; $J_s$: un proces de salturi cu un număr finit de salturi pe zi, $\Delta J_s$: saltul din momentul $s$')]),
    (T(r'Quadratic variation of the day: the diffusive part plus the squared jumps',
       r'Variația pătratică a zilei: partea de difuzie plus pătratele salturilor'
       ) + r'''
    \[ \mathrm{QV}_t = \mathrm{IV}_t + \sum_{s \le 1}(\Delta J_s)^2, \qquad \mathrm{IV}_t = \int_0^1\sigma^2_s\,ds \]''',
     [T(r'$\mathrm{IV}_t$: integrated variance, the average of the spot variance over the day',
        r'$\mathrm{IV}_t$: varianța integrată, media varianței instantanee pe parcursul zilei'),
      T(r'without jumps and with $\sigma$ independent of $W$: $r_t | \mathrm{IV}_t \sim N(\int_0^1\mu_s\,ds, \mathrm{IV}_t)$, so IV is the variance that matters for the daily return $r_t$',
        r'fără salturi și cu $\sigma$ independent de $W$: $r_t | \mathrm{IV}_t \sim N(\int_0^1\mu_s\,ds, \mathrm{IV}_t)$, deci IV este varianța relevantă pentru randamentul zilnic $r_t$')])), 'small')

D.frame(T('Prices as Itô semimartingales (2/2): realised variance', 'Prețurile ca semimartingale Itô (2/2): varianța realizată'), items(
    (T(r'Realised variance: the sum of the $n$ squared intraday returns of the day',
       r'Varianța realizată: suma pătratelor celor $n$ randamente intraday ale zilei'
       ) + r'''
    \[ \mathrm{RV}_t = \sum_{i=1}^n r_{t,i}^2, \qquad r_{t,i} = X_{i/n} - X_{(i-1)/n} \]''',
     [T(r'$n$: number of intraday intervals (78 five-minute returns in a 6.5-hour session); $r_{t,i}$: log return over the $i$-th interval',
        r'$n$: numărul intervalelor intraday (78 de randamente la 5 minute într-o ședință de 6,5 ore); $r_{t,i}$: randamentul logaritmic din intervalul $i$'),
      T(r'$\mathrm{RV}_t \to \mathrm{QV}_t$ in probability as $n \to \infty$: RV measures the total (diffusive plus jump) variation',
        r'$\mathrm{RV}_t \to \mathrm{QV}_t$ în probabilitate cînd $n \to \infty$: RV măsoară variația totală (difuzie plus salturi)')]),
    (T(r'The drift does not matter in the limit: it is $O(1/n)$ per interval, while the Brownian part is $O(n^{-1/2})$',
       r'Drift-ul nu contează la limită: este $O(1/n)$ pe interval, în timp ce partea browniană este $O(n^{-1/2})$'),
     [T(r'volatility becomes observable \emph{ex post}, without a model \refABDL, \refBNSa',
        r'volatilitatea devine observabilă \emph{ex post}, fără model \refABDL, \refBNSa')])), 'small')

D.frame(T('The central limit theorem for realised variance (1/2)', 'Teorema limită centrală pentru varianța realizată (1/2)'), items(
    (T(r'\refBNSa: without jumps, the error of RV shrinks at rate $\sqrt n$ and is mixed normal',
       r'\refBNSa: fără salturi, eroarea lui RV scade cu rata $\sqrt n$ și este mixt normală'
       ) + r'''
    \[ \sqrt n\,(\mathrm{RV}_t - \mathrm{IV}_t) \to MN(0, 2\,\mathrm{IQ}_t), \qquad \mathrm{IQ}_t = \int_0^1\sigma^4_s\,ds \]''',
     [T(r'$\mathrm{IQ}_t$: integrated quarticity, the daily average of $\sigma^4_s$; it sets the size of the error',
        r'$\mathrm{IQ}_t$: cuarticitatea integrată, media zilnică a lui $\sigma^4_s$; ea stabilește mărimea erorii'),
      T(r'$MN$ (mixed normal): normal given the path of $\sigma$, with a random variance $2\,\mathrm{IQ}_t$',
        r'$MN$ (mixt normală): normală condiționat de traiectoria lui $\sigma$, cu o varianță aleatoare $2\,\mathrm{IQ}_t$'),
      T(r'the convergence is \emph{stable} in law: one may divide by a random, consistently estimated $\sqrt{\mathrm{IQ}_t}$ and keep the limit',
        r'convergența este \emph{stabilă} în lege: putem împărți la $\sqrt{\mathrm{IQ}_t}$, aleator și estimat consistent, fără a schimba limita')]),
    (T(r'Rate $\sqrt n$: with $n = 78$ and volatility constant within the day, the relative error is about $\sqrt{2/78} \approx 16\%$',
       r'Rata $\sqrt n$: cu $n = 78$ și volatilitate constantă în cursul zilei, eroarea relativă este de aproximativ $\sqrt{2/78} \approx 16\%$'),
     [T(r'the measurement error $\mathrm{RV}_t - \mathrm{IV}_t$ is heteroskedastic (it scales with $\mathrm{IQ}_t$): HARQ, below, is built on this fact',
        r'eroarea de măsurare $\mathrm{RV}_t - \mathrm{IV}_t$ este heteroscedastică (crește cu $\mathrm{IQ}_t$): pe acest fapt se bazează HARQ, mai jos')])), 'small')

D.frame(T('The central limit theorem for realised variance (2/2): feasible intervals', 'Teorema limită centrală pentru varianța realizată (2/2): intervale fezabile'), items(
    (T(r'Feasible version: estimate IQ by the realised quarticity RQ, then studentise',
       r'Varianta fezabilă: estimăm IQ prin cuarticitatea realizată RQ, apoi studentizăm'
       ) + r'''
    \[ \widehat{\mathrm{IQ}}_t = \mathrm{RQ}_t = \frac n3\sum_{i=1}^n r_{t,i}^4, \qquad \frac{\mathrm{RV}_t - \mathrm{IV}_t}{\sqrt{\frac23\sum_i r_{t,i}^4}} \to N(0, 1) \]''',
     [T(r'the factor $\frac n3$ makes RQ unbiased under constant volatility, because $\E Z^4 = 3$ for $Z \sim N(0, 1)$',
        r'factorul $\frac n3$ face RQ nedeplasat la volatilitate constantă, deoarece $\E Z^4 = 3$ pentru $Z \sim N(0, 1)$'),
      T(r'95\% interval for $\mathrm{IV}_t$: $\mathrm{RV}_t \pm 1.96\sqrt{\frac23\sum_i r_{t,i}^4}$; it may contain negative values',
        r'interval de 95\% pentru $\mathrm{IV}_t$: $\mathrm{RV}_t \pm 1.96\sqrt{\frac23\sum_i r_{t,i}^4}$; poate conține valori negative')]),
    (T(r'Log version (delta method): an interval for $\ln\mathrm{IV}_t$', r'Versiunea în logaritmi (metoda delta): un interval pentru $\ln\mathrm{IV}_t$'
       ) + M(r'''
    \[ \ln\mathrm{RV}_t \pm 1.96\,\frac{\sqrt{\frac23\sum_i r_{t,i}^4}}{\mathrm{RV}_t} \]'''),
     [T(r'exponentiated, it never contains negative values and has better coverage in finite samples',
        r'după exponențiere nu conține niciodată valori negative și are o acoperire mai bună în eșantioane finite')])), 'small')

D.frame(T('A simulated market with a known truth', 'O piață simulată cu adevărul cunoscut'), items(
    (T(r'One-second grid, $n = 23\,400$ seconds a day; the log spot variance is the sum of two Gaussian AR(1) factors',
       r'Grilă la o secundă, $n = 23\,400$ de secunde pe zi; logaritmul varianței instantanee este suma a doi factori AR(1) gaussieni'
       ) + r'''
    \[ \ln\sigma^2_s = c + f^{(1)}_s + f^{(2)}_s \]''',
     [T(r'$c$: constant fixing the mean; $f^{(1)}$: slow factor (half-life 60 days, stationary s.d. 0.75); $f^{(2)}$: fast factor (half-life 2 days, s.d. 0.45)',
        r'$c$: constanta care fixează media; $f^{(1)}$: factorul lent (timp de înjumătățire de 60 de zile, abaterea standard staționară 0,75); $f^{(2)}$: factorul rapid (2 zile, abaterea standard 0,45)'),
      T(r'mean IV = 1 (\%$^2$ a day), the mean of the S\&P 500 realised kernel in 2000--2022; leverage: correlation $-0.6$ between price shocks and shocks to the fast factor',
        r'media IV = 1 (\%$^2$ pe zi), media realised kernel-ului pentru S\&P 500 în 2000--2022; efectul de levier: corelația $-0{,}6$ între șocurile prețului și șocurile factorului rapid')]),
    T(r'Jumps: Poisson with 0.08 jumps a day, sizes $N(0, 0.8^2)$ (\%): jumps make about @{kn.js}\% of quadratic variation',
      r'Salturi: proces Poisson cu 0,08 salturi pe zi, mărimi $N(0, 0{,}8^2)$ (\%): salturile reprezintă aproximativ @{kn.js}\% din variația pătratică'),
    (T(r'Noise: we observe $Y_s = X_s + u_s$, with $u_s$ i.i.d. $N(0, \omega^2)$ and $\omega = 0.004\%$',
       r'Zgomot: observăm $Y_s = X_s + u_s$, cu $u_s$ i.i.d. $N(0, \omega^2)$ și $\omega = 0{,}004\%$'),
     [T(r'$Y_s$: observed log price; $X_s$: efficient log price; $u_s$: microstructure noise with standard deviation $\omega$; at one second, $2n\omega^2 = @{kn.nb}$ (next slides)',
        r'$Y_s$: logaritmul prețului observat; $X_s$: logaritmul prețului eficient; $u_s$: zgomotul de microstructură, cu abaterea standard $\omega$; la o secundă, $2n\omega^2 = @{kn.nb}$ (slide-urile următoare)')]),
    T('Each estimator below is compared with the true IV or QV of the same simulated day', 'Fiecare estimator de mai jos este comparat cu IV sau QV adevărate din aceeași zi simulată')), 'small')

chart(T('Coverage of the feasible CLT', 'Acoperirea TLC fezabile'), 'ats_ch8_rv_clt', 'ATS_ch8_realised_measures', [
    T(r'@{cl.days} simulated days without jumps; 95\% intervals for $\mathrm{IV}_t$ (raw and log) from returns sampled every 30 minutes to every 5 seconds, without and with noise',
      r'@{cl.days} de zile simulate fără salturi; intervale de 95\% pentru $\mathrm{IV}_t$ (în nivel și în logaritmi) din randamente eșantionate la 30 de minute pînă la 5 secunde, fără și cu zgomot')],
    h='0.6\\textheight')

interp(('the CLT coverage', 'acoperirii TLC'), [
    T(r'Without noise, coverage approaches 95\% as $n$ grows: raw interval @{cl.clean.raw.13}\% at $n = 13$ and @{cl.clean.raw.390}\% at $n = 390$; the log interval is closer at small $n$ (@{cl.clean.log.13}\%)',
      r'Fără zgomot, acoperirea se apropie de 95\% cînd $n$ crește: intervalul în nivel are @{cl.clean.raw.13}\% la $n = 13$ și @{cl.clean.raw.390}\% la $n = 390$; intervalul în logaritmi este mai aproape pentru $n$ mic (@{cl.clean.log.13}\%)'),
    T(r'With noise, coverage collapses once sampling is too fine: @{cl.noisy.raw.1560}\% at 15 seconds and @{cl.noisy.raw.4680}\% at 5 seconds; at 1 minute it is still @{cl.noisy.raw.390}\%',
      r'Cu zgomot, acoperirea se prăbușește cînd eșantionarea este prea fină: @{cl.noisy.raw.1560}\% la 15 secunde și @{cl.noisy.raw.4680}\% la 5 secunde; la un minut este încă @{cl.noisy.raw.390}\%'),
    T(r'The interval shrinks like $n^{-1/2}$ while the noise bias grows like $n$: the CLT is a statement about the efficient price, not about the observed one',
      r'Intervalul se îngustează ca $n^{-1/2}$, iar deplasarea din zgomot crește ca $n$: TLC este o afirmație despre prețul eficient, nu despre cel observat'),
    T('Practical rule: 5-minute returns for liquid assets unless a noise-robust estimator is used', 'Regula practică: randamente la 5 minute pentru active lichide, cu excepția cazului în care se folosește un estimator robust la zgomot')])

D.frame(T('Where the realised measures come from', 'Sursa măsurilor realizate'), two(
    ph('bn', T('Ole E. Barndorff-Nielsen, 2007', 'Ole E. Barndorff-Nielsen, 2007'), h='0.34\\textheight'),
    items(T(r'\refOMI, version 0.3: daily RV, BV, realised kernels and open-to-close returns for 31 indices, 2000 to 25 February 2022, built from cleaned tick data',
            r'\refOMI, versiunea 0.3: RV, BV, realised kernels și randamente deschidere--închidere zilnice pentru 31 de indici, din 2000 pînă la 25 februarie 2022, construite din date tick curățate'),
          T(r'its terms: free use if the library and its version are cited; the archived copy keeps the 2022 file available after the shutdown',
            r'condițiile ei: utilizare liberă dacă biblioteca și versiunea ei sînt citate; copia arhivată păstrează fișierul din 2022 disponibil după închidere'),
          T(r'Bitcoin and Ether trade 24/7 and Binance publishes all one-minute and one-second prices: we compute RV, BV, RQ, tripower quarticity and a realised kernel for each UTC day, 2018--2026',
            r'Bitcoin și Ether se tranzacționează 24/7, iar Binance publică toate prețurile la un minut și la o secundă: calculăm RV, BV, RQ, cuarticitatea tripower și un realised kernel pentru fiecare zi UTC, 2018--2026'),
          T('No free source covers equity intraday data after 2022: a project can rebuild them from a licensed feed', 'Nicio sursă gratuită nu acoperă datele intraday pentru acțiuni după 2022: un proiect le poate reconstrui dintr-o sursă cu licență')), '0.36', '0.62'), 'footnotesize')

chart(T('Realised volatility across markets', 'Volatilitatea realizată pe mai multe piețe'), 'ats_ch8_rk_overview', 'ATS_ch8_realised_measures', [
    T(r'Annualised realised kernel, 5-day means: S\&P 500, DAX and Nikkei 225 (Oxford-Man, 2000--2022); Bitcoin (Binance one-minute prices, 2018--2026, 365 days a year)',
      r'Realised kernel anualizat, medii pe 5 zile: S\&P 500, DAX și Nikkei 225 (Oxford-Man, 2000--2022); Bitcoin (prețuri Binance la un minut, 2018--2026, 365 de zile pe an)')],
    h='0.6\\textheight')

interp(('the realised volatilities', 'volatilităților realizate'), [
    T(r'Average annualised volatility from the kernel: S\&P 500 @{ov.spx}\%, DAX @{ov.dax}\%, Nikkei @{ov.nk}\%, Bitcoin @{ov.btc}\%',
      r'Volatilitatea anualizată medie din kernel: S\&P 500 @{ov.spx}\%, DAX @{ov.dax}\%, Nikkei @{ov.nk}\%, Bitcoin @{ov.btc}\%'),
    T('The equity series move together (2002, 2008, 2011, 2020): a common long-run factor, the multivariate theme of the last section', 'Seriile de acțiuni se mișcă împreună (2002, 2008, 2011, 2020): un factor comun de termen lung, tema multivariată din ultima secțiune'),
    T('Open-to-close measures miss the overnight return: for daily risk one adds the squared overnight return or scales the measure', 'Măsurile deschidere--închidere omit randamentul de peste noapte: pentru riscul zilnic se adaugă pătratul randamentului de peste noapte sau se scalează măsura'),
    T('Bitcoin has no overnight gap, but its daily volatility is three to four times higher and falls after 2023', 'Bitcoin nu are perioade fără tranzacționare, dar volatilitatea lui zilnică este de trei pînă la patru ori mai mare și scade după 2023')])

D.frame(T('Microstructure noise (1/2): the bias of RV', 'Zgomotul de microstructură (1/2): deplasarea lui RV'), items(
    (T(r'The observed log price is the efficient price plus a noise term', r'Logaritmul prețului observat este prețul eficient plus un termen de zgomot'
       ) + r'''
    \[ Y_{i/n} = X_{i/n} + u_i \]''',
     [T(r'$u_i$: i.i.d. noise with variance $\omega^2$, independent of $X$; sources: bid--ask bounce, price discreteness, stale quotes',
        r'$u_i$: zgomot i.i.d. cu varianța $\omega^2$, independent de $X$; surse: oscilația între bid și ask, discretizarea prețului, cotațiile stale (neactualizate)')]),
    (T(r'RV computed from the observed prices at $n$ intervals, $\mathrm{RV}^{(n)}_t$, is biased upwards, and the bias grows with $n$',
       r'RV calculat din prețurile observate la $n$ intervale, $\mathrm{RV}^{(n)}_t$, este deplasat în sus, iar deplasarea crește cu $n$'
       ) + r'''
    \[ \E(\mathrm{RV}^{(n)}_t | X) = \mathrm{IV}_t + 2n\omega^2, \qquad \Var(\mathrm{RV}^{(n)}_t | X) \approx 4n\,\E u^4 \]''',
     [T(r'each observed return contains $u_i - u_{i-1}$, with variance $2\omega^2$; summed over $n$ returns this gives $2n\omega^2$',
        r'fiecare randament observat conține $u_i - u_{i-1}$, cu varianța $2\omega^2$; însumat pe $n$ randamente, aceasta dă $2n\omega^2$'),
      T(r'RV diverges as $n \to \infty$: sampling as often as possible is not optimal',
        r'RV diverge cînd $n \to \infty$: eșantionarea cît mai deasă nu este optimă'),
      T(r'derivation of the bias and of the variance: Appendix  % applink: the noise bias of realised variance',
        r'derivarea deplasării și a varianței: Anexa  % applink: deplasarea din zgomot a varianței realizate')])), 'small')

D.frame(T('Microstructure noise (2/2): diagnostics', 'Zgomotul de microstructură (2/2): diagnostice'), items(
    (T(r'Two consequences of i.i.d. noise', r'Două consecințe ale zgomotului i.i.d.'),
     [T(r'$\hat\omega^2 = \mathrm{RV}^{(n)}_t/(2n)$ at the highest frequency estimates the noise variance, since $2n\omega^2$ dominates IV there',
        r'$\hat\omega^2 = \mathrm{RV}^{(n)}_t/(2n)$, la frecvența cea mai mare, estimează varianța zgomotului, deoarece acolo $2n\omega^2$ domină IV'),
      T(r'returns of the observed price have first-order autocovariance $-\omega^2$: negative autocorrelation is the signature of i.i.d. noise',
        r'randamentele prețului observat au autocovarianța de ordinul întîi $-\omega^2$: autocorelația negativă este amprenta zgomotului i.i.d.')]),
    (T(r'Signature plot: average $\mathrm{RV}^{(n)}$ against the sampling interval', r'Signature plot: media $\mathrm{RV}^{(n)}$ în funcție de intervalul de eșantionare'),
     [T('a flat region shows the intervals where noise no longer matters', 'o zonă plată arată intervalele la care zgomotul nu mai contează')]),
    T(r'Real noise is not i.i.d.: it is autocorrelated and correlated with the efficient price, especially in quote data \refHLc',
      r'Zgomotul real nu este i.i.d.: este autocorelat și corelat cu prețul eficient, mai ales în datele de cotații \refHLc')), 'small')

D.frame(T('Optimal sparse sampling', 'Eșantionarea rară optimă'), items(
    (T(r'Mean square error (MSE) of $\mathrm{RV}^{(n)}$ as an estimator of IV: sampling variance falls, noise bias rises with $n$',
       r'Eroarea pătratică medie (MSE) a lui $\mathrm{RV}^{(n)}$ ca estimator al lui IV: varianța de eșantionare scade, deplasarea din zgomot crește cu $n$'
       ) + T(r'''
    \[ \mathrm{MSE}(n) \approx \underbrace{\frac{2\,\mathrm{IQ}}{n}}_{\text{variance}} + \underbrace{(2n\omega^2)^2}_{\text{bias}^2} + 4n\,\E u^4 + \dots \]''', r'''
    \[ \mathrm{MSE}(n) \approx \underbrace{\frac{2\,\mathrm{IQ}}{n}}_{\text{varianța}} + \underbrace{(2n\omega^2)^2}_{\text{deplasarea}^2} + 4n\,\E u^4 + \dots \]'''),
     []),
    (T(r'Minimising the first two terms gives the optimal number of intervals \refBR', r'Minimizarea primilor doi termeni dă numărul optim de intervale \refBR'
       ) + r'''
    \[ n^* \approx \Big(\frac{\mathrm{IQ}}{4\omega^4}\Big)^{1/3} \]''',
     [T(r'the optimal grid is coarser when noise ($\omega^2$) is large relative to volatility ($\mathrm{IQ}$)',
        r'grila optimă este mai rară cînd zgomotul ($\omega^2$) este mare față de volatilitate ($\mathrm{IQ}$)'),
      T(r'example (Seminar 8, A3): IV = IQ = 1, $\omega^2 = 1.6\times10^{-5}$ gives $n^* \approx 990$, a return every 24 seconds', r'exemplu (Seminarul 8, A3): IV = IQ = 1, $\omega^2 = 1{,}6\times10^{-5}$ dă $n^* \approx 990$, un randament la fiecare 24 de secunde')]),
    T(r'The best sparse RV converges only at rate $n^{1/6}$ and discards most data: this motivates estimators that use all observations',
      r'Cel mai bun RV rar converge doar cu rata $n^{1/6}$ și renunță la majoritatea datelor: de aici estimatorii care folosesc toate observațiile'),
    T(r'Subsampling: average the RV of the $K$ offset grids (starting at second $0, 1, \dots, K-1$); same bias, smaller variance',
      r'Subeșantionarea: media RV pe cele $K$ grile decalate (cu start în secunda $0, 1, \dots, K-1$); aceeași deplasare, varianță mai mică')), 'small')

D.frame(T('Two scales and realised kernels (1/2)', 'Două scale de timp și realised kernels (1/2)'), items(
    (T(r'Two-scales RV \refZMA: the fast scale estimates the noise bias of the slow one and removes it',
       r'RV cu două scale \refZMA: scala rapidă estimează deplasarea din zgomot a celei lente și o elimină'
       ) + r'''
    \[ \mathrm{TSRV} = \overline{\mathrm{RV}}^{(K)} - \frac{\bar n}{n}\,\mathrm{RV}^{(n)}, \qquad \bar n = \frac{n - K + 1}{K} \]''',
     [T(r'$\overline{\mathrm{RV}}^{(K)}$: subsampled RV on $K$ offset sparse grids (slow scale), each with about $\bar n$ returns; $\mathrm{RV}^{(n)}$: RV on all $n$ returns (fast scale)',
        r'$\overline{\mathrm{RV}}^{(K)}$: RV subeșantionat pe $K$ grile rare decalate (scala lentă), fiecare cu aproximativ $\bar n$ randamente; $\mathrm{RV}^{(n)}$: RV pe toate cele $n$ randamente (scala rapidă)'),
      T(r'the bias of the slow scale is $2\bar n\omega^2 = \frac{\bar n}{n}\cdot 2n\omega^2$: the correction subtracts it; rate $n^{1/6}$',
        r'deplasarea scalei lente este $2\bar n\omega^2 = \frac{\bar n}{n}\cdot 2n\omega^2$: corecția o scade; rata $n^{1/6}$')]),
    (T(r'Pre-averaging \refJLMPV: average returns over blocks before squaring', r'Pre-averaging \refJLMPV: mediem randamentele pe blocuri înainte de ridicarea la pătrat'),
     [T(r'rate $n^{1/4}$, the optimal one in the presence of noise; in practice similar to the realised kernel',
        r'rata $n^{1/4}$, cea optimă în prezența zgomotului; în practică, apropiat de realised kernel')])), 'small')

D.frame(T('Two scales and realised kernels (2/2): the realised kernel', 'Două scale de timp și realised kernels (2/2): realised kernel-ul'), items(
    (T(r'Realised kernel \refBNHLSa: RV plus weighted realised autocovariances', r'Realised kernel \refBNHLSa: RV plus autocovarianțele realizate, ponderate'
       ) + r'''
    \[ \mathrm{RK}_t = \gamma_0 + \sum_{h=1}^H k\Big(\frac{h}{H+1}\Big)(\gamma_h + \gamma_{-h}), \qquad \gamma_h = \sum_i r_{t,i}\,r_{t,i-h} \]''',
     [T(r'$\gamma_h$: realised autocovariance at lag $h$ ($\gamma_0 = \mathrm{RV}$); $H$: bandwidth, the number of lags used; $k(\cdot)$: weight function with $k(0) = 1$, $k(1) = 0$',
        r'$\gamma_h$: autocovarianța realizată la lagul $h$ ($\gamma_0 = \mathrm{RV}$); $H$: lățimea de bandă, numărul de laguri folosite; $k(\cdot)$: funcția de ponderare, cu $k(0) = 1$, $k(1) = 0$'),
      T(r'Parzen weights: $k(x) = 1 - 6x^2 + 6x^3$ for $x \le \frac12$ and $2(1-x)^3$ for $\frac12 < x \le 1$',
        r'ponderile Parzen: $k(x) = 1 - 6x^2 + 6x^3$ pentru $x \le \frac12$ și $2(1-x)^3$ pentru $\frac12 < x \le 1$'),
      T(r'the negative $\gamma_1$ created by noise cancels the bias $2n\omega^2$: the same idea as HAC variance estimation (Chapter 0)',
        r'$\gamma_1$ negativ creat de zgomot anulează deplasarea $2n\omega^2$: aceeași idee ca la estimarea HAC a varianței (Capitolul 0)')]),
    (T(r'Properties', r'Proprietăți'),
     [T(r'nonnegative by construction; rate $n^{1/5}$ with $H = c^*\xi^{4/5}n^{3/5}$, where $\xi^2 = \omega^2/\sqrt{\mathrm{IQ}}$ is the noise-to-signal ratio and $c^* = 3.51$ for Parzen \refBNHLSb',
        r'nenegativ prin construcție; rata $n^{1/5}$ cu $H = c^*\xi^{4/5}n^{3/5}$, unde $\xi^2 = \omega^2/\sqrt{\mathrm{IQ}}$ este raportul zgomot/semnal, iar $c^* = 3{,}51$ pentru Parzen \refBNHLSb'),
      T(r'it also corrects serially dependent noise of short range, of either sign', r'corectează și zgomotul cu dependență serială pe distanțe scurte, de orice semn')])), 'small')

chart(T('Estimators against the true quadratic variation', 'Estimatorii comparați cu variația pătratică adevărată'), 'ats_ch8_kernels', 'ATS_ch8_realised_measures', [
    T(r'@{kn.days} simulated days with jumps and noise; bias and root mean square error relative to the mean QV; TSRV with $K = 300$ seconds; RK with the BNHLS bandwidth (median $H = @{kn.H}$)',
      r'@{kn.days} de zile simulate cu salturi și zgomot; deplasarea și rădăcina erorii pătratice medii, relativ la media QV; TSRV cu $K = 300$ de secunde; RK cu lățimea de bandă BNHLS (mediana $H = @{kn.H}$)')],
    h='0.6\\textheight')

interp(('the estimator comparison', 'comparației estimatorilor'), [
    T(r'RV at one second is dominated by noise: bias @{kn.rv1s.b}\% of QV; at one minute the bias is @{kn.rv1m.b}\% and the RMSE @{kn.rv1m.r}\%',
      r'RV la o secundă este dominat de zgomot: deplasarea este @{kn.rv1s.b}\% din QV; la un minut deplasarea este @{kn.rv1m.b}\%, iar RMSE @{kn.rv1m.r}\%'),
    T(r'Five-minute RV is unbiased but noisy (RMSE @{kn.rv5.r}\%); subsampling and TSRV reduce it to @{kn.rvss.r}\% and @{kn.tsrv.r}\%',
      r'RV la cinci minute este nedeplasat, dar zgomotos (RMSE @{kn.rv5.r}\%); subeșantionarea și TSRV îl reduc la @{kn.rvss.r}\% și @{kn.tsrv.r}\%'),
    T(r'The realised kernel uses all 23\,400 returns: bias @{kn.rk.b}\%, RMSE @{kn.rk.r}\%, the best of the six',
      r'Realised kernel-ul folosește toate cele 23\,400 de randamente: deplasarea @{kn.rk.b}\%, RMSE @{kn.rk.r}\%, cel mai bun dintre cei șase'),
    T('All estimators here target QV, jumps included; separating the jump part needs the next section', 'Toți estimatorii de aici au ca țintă QV, inclusiv salturile; separarea salturilor cere secțiunea următoare')])

chart(T('Signature plot and Epps effect: Bitcoin and Ether', 'Signature plot și efectul Epps: Bitcoin și Ether'), 'ats_ch8_signature', 'ATS_ch8_realised_measures', [
    T(r'Binance one-second prices, August 2026 (@{sg.days} days); average daily RV by sampling interval (subsampled); realised correlation of the two coins by interval',
      r'Prețuri Binance la o secundă, august 2026 (@{sg.days} de zile); RV zilnic mediu în funcție de intervalul de eșantionare (subeșantionat); corelația realizată a celor două monede în funcție de interval')],
    h='0.6\\textheight')

interp(('the signature plot', 'signature plot-ului'), [
    T(r'Bitcoin: RV is @{sg.b1} at one second, @{sg.b60} at one minute, @{sg.b300} at five minutes: the signature \emph{rises}, the opposite of the i.i.d.-noise prediction',
      r'Bitcoin: RV este @{sg.b1} la o secundă, @{sg.b60} la un minut, @{sg.b300} la cinci minute: signature plot-ul \emph{crește}, opusul predicției pentru zgomot i.i.d.'),
    T(r'Reason: @{sg.zero}\% of one-second returns are zero (no trade or the same price) and prices adjust gradually, so one-second returns are positively autocorrelated',
      r'Motivul: @{sg.zero}\% dintre randamentele la o secundă sînt zero (nicio tranzacție sau același preț), iar prețurile se ajustează treptat, deci randamentele la o secundă sînt autocorelate pozitiv'),
    T(r'The realised kernel on one-second data (@{sg.rk}, median $H = @{sg.H}$) adds the positive autocovariances back and lands on the flat region of 1--30 minutes',
      r'Realised kernel-ul pe date la o secundă (@{sg.rk}, mediana $H = @{sg.H}$) adaugă înapoi autocovarianțele pozitive și ajunge în zona plată de 1--30 de minute'),
    T(r'Epps effect \refEpp: realised correlation @{sg.c1} at one second against @{sg.c300} at five minutes; asynchronous trading biases covariances towards zero at high frequency',
      r'Efectul Epps \refEpp: corelația realizată @{sg.c1} la o secundă față de @{sg.c300} la cinci minute; tranzacționarea asincronă deplasează covarianțele spre zero la frecvență înaltă')])

D.recap(('Realised measures', 'măsurile realizate'), [
    T(r'RV estimates QV with error $\sqrt{2\mathrm{IQ}/n}$; the log interval behaves better; stable convergence makes studentization valid', r'RV estimează QV cu eroarea $\sqrt{2\mathrm{IQ}/n}$; intervalul în logaritmi se comportă mai bine; convergența stabilă face validă studentizarea'),
    T('Noise biases RV at high frequency; its sign and size are empirical: look at the signature plot first', 'Zgomotul deplasează RV la frecvență înaltă; semnul și mărimea acestui efect sînt empirice: priviți întîi signature plot-ul'),
    T('Realised kernels use all the data and correct short-range dependent noise; 5-minute RV remains a robust benchmark', 'Realised kernels folosesc toate datele și corectează zgomotul cu dependență pe distanțe scurte; RV la 5 minute rămîne un reper robust')])

# =============================================================================
# 4. SALTURI
# =============================================================================
D.section('Jumps: bipower variation and tests', 'Salturi: variația bipower și teste')

D.frame(T('Bipower variation (1/2)', 'Variația bipower (1/2)'), items(
    (T(r'\refBNSb: sum of products of adjacent absolute returns, rescaled', r'\refBNSb: suma produselor valorilor absolute ale randamentelor adiacente, rescalată'
       ) + r'''
    \[ \mathrm{BV}_t = \mu_1^{-2}\,\frac{n}{n-1}\sum_{i=2}^n\lvert r_{t,i}\rvert\,\lvert r_{t,i-1}\rvert, \qquad \mu_1 = \E|Z| = \sqrt{2/\pi} \]''',
     [T(r'$Z \sim N(0, 1)$; $\mu_1^{-2}$ makes $\mathrm{BV}_t$ consistent for $\mathrm{IV}_t$; $\frac{n}{n-1}$ corrects for the $n-1$ products',
        r'$Z \sim N(0, 1)$; $\mu_1^{-2}$ face $\mathrm{BV}_t$ consistent pentru $\mathrm{IV}_t$; $\frac{n}{n-1}$ corectează pentru cele $n-1$ produse'),
      T(r'$\mathrm{BV}_t \to \mathrm{IV}_t$ even with (finite-activity) jumps: a jump enters only two products, each multiplied by a return of order $n^{-1/2}$',
        r'$\mathrm{BV}_t \to \mathrm{IV}_t$ chiar și cu salturi (cu activitate finită): un salt intră doar în două produse, fiecare înmulțit cu un randament de ordinul $n^{-1/2}$')]),
    T(r'Hence $\mathrm{RV}_t - \mathrm{BV}_t \to \sum_{s \le 1}(\Delta J_s)^2$: a nonparametric estimate of the jump variation of the day',
      r'Deci $\mathrm{RV}_t - \mathrm{BV}_t \to \sum_{s \le 1}(\Delta J_s)^2$: o estimație neparametrică a variației din salturi a zilei')), 'small')

D.frame(T('Bipower variation (2/2): related estimators', 'Variația bipower (2/2): estimatori înrudiți'), items(
    (T(r'Jump-robust quarticity: the tripower quarticity', r'Cuarticitatea robustă la salturi: cuarticitatea tripower'
       ) + r'''
    \[ \mathrm{TQ}_t = n\,\mu_{4/3}^{-3}\,\frac{n}{n-2}\sum_{i=3}^n\prod_{j=0}^2|r_{t,i-j}|^{4/3}, \qquad \mu_{4/3} = \E|Z|^{4/3} \]''',
     [T(r'products of three adjacent absolute returns, each to the power $4/3$; $\mathrm{TQ}_t \to \mathrm{IQ}_t$ even with jumps (RQ does not)',
        r'produse a trei valori absolute ale randamentelor adiacente, fiecare la puterea $4/3$; $\mathrm{TQ}_t \to \mathrm{IQ}_t$ chiar și cu salturi (RQ, nu)')]),
    T(r'Nearest-neighbour truncation (MedRV, MinRV) \refADS: smaller finite-sample bias from a jump and from zero returns',
      r'Trunchierea prin vecinii cei mai apropiați (MedRV, MinRV) \refADS: deplasare mai mică în eșantioane finite din cauza unui salt și a randamentelor nule'),
    (T(r'Threshold (truncated) RV: drop the returns above $c\,n^{-\varpi}$', r'RV cu prag (trunchiat): se elimină randamentele peste $c\,n^{-\varpi}$'),
     [T(r'$c > 0$: a constant (a multiple of the local volatility); $\varpi \in (0, \frac12)$: the threshold shrinks more slowly than a diffusive return, so only jumps are removed',
        r'$c > 0$: o constantă (un multiplu al volatilității locale); $\varpi \in (0, \frac12)$: pragul scade mai lent decît un randament de difuzie, deci sînt eliminate doar salturile')])), 'small')

D.frame(T('Testing for jumps (1/2): the ratio statistic', 'Testarea salturilor (1/2): statistica raport'), items(
    (T(r'\refBNSc: without jumps, the difference RV $-$ BV is also mixed normal', r'\refBNSc: fără salturi, diferența RV $-$ BV este și ea mixt normală'
       ) + M(r'''
    \[ \sqrt n(\mathrm{RV}_t - \mathrm{BV}_t) \to MN(0, \vartheta\,\mathrm{IQ}_t), \qquad \vartheta = \mu_1^{-4} + 2\mu_1^{-2} - 5 = \frac{\pi^2}{4} + \pi - 5 \approx 0.609 \]'''),
     [T(r'$\vartheta$: a constant that measures how much less efficient BV is than RV', r'$\vartheta$: o constantă care măsoară cu cît este BV mai puțin eficient decît RV')]),
    (T(r'Ratio statistic \refHT: the relative jump contribution, studentised', r'Statistica raport \refHT: contribuția relativă a salturilor, studentizată'
       ) + r'''
    \[ z_t = \frac{(\mathrm{RV}_t - \mathrm{BV}_t)/\mathrm{RV}_t}{\sqrt{\frac{\vartheta}{n}\max\big(1, \mathrm{TQ}_t/\mathrm{BV}_t^2\big)}} \to N(0, 1) \]''',
     [T(r'one-sided test: reject ``no jump on day $t$\'\' for large $z_t$', r'test unilateral: respingem ipoteza „niciun salt în ziua $t$” pentru $z_t$ mare'),
      T(r'the ratio form and the max adjustment give the best size in their simulations; $\mathrm{TQ}_t/\mathrm{BV}_t^2 \ge 1$ by Jensen when volatility varies within the day',
        r'forma de raport și ajustarea prin max dau cea mai bună mărime a testului în simulările lor; $\mathrm{TQ}_t/\mathrm{BV}_t^2 \ge 1$ prin Jensen cînd volatilitatea variază în cursul zilei')])), 'small')

D.frame(T('Testing for jumps (2/2): in practice', 'Testarea salturilor (2/2): aplicarea practică'), items(
    T(r'A daily test answers ``was there a jump today?\'\'; locating it within the day needs a test on each return standardised by local BV \refLM',
      r'Un test zilnic răspunde la întrebarea „a existat un salt azi?”; localizarea lui în cursul zilei cere un test pe fiecare randament standardizat cu BV local \refLM'),
    (T(r'Multiple testing: at level $\alpha$ over $T$ days one expects $\alpha T$ false jump days',
       r'Testare multiplă: la nivelul $\alpha$, pe $T$ zile ne așteptăm la $\alpha T$ zile cu salturi false'),
     [T(r'use a small $\alpha$ (0.1\%) or a family-wise (FWER) or false-discovery-rate (FDR) correction (Chapter 1)',
        r'folosiți un $\alpha$ mic (0,1\%) sau o corecție de tip FWER sau FDR (Capitolul 1)')]),
    (T(r'Separating the continuous and jump parts of RV \refABD', r'Separarea părților continuă și de salt ale lui RV \refABD'
       ) + r'''
    \[ J_t = \mathbb 1(z_t > z_{1-\alpha})\,(\mathrm{RV}_t - \mathrm{BV}_t), \qquad C_t = \mathrm{RV}_t - J_t \]''',
     [T(r'$\mathbb 1(\cdot)$: indicator, 1 if the test rejects and 0 otherwise; $z_{1-\alpha}$: the $1-\alpha$ quantile of $N(0, 1)$',
        r'$\mathbb 1(\cdot)$: indicatorul, 1 dacă testul respinge și 0 altfel; $z_{1-\alpha}$: cuantila $1-\alpha$ a distribuției $N(0, 1)$'),
      T(r'$J_t$: jump part, nonzero only on significant days; $C_t$: continuous part', r'$J_t$: partea de salt, nenulă doar în zilele semnificative; $C_t$: partea continuă')])), 'small')

chart(T('Size and power of the ratio test', 'Mărimea și puterea testului raport'), 'ats_ch8_jump_power', 'ATS_ch8_jumps', [
    T(r'@{js.days} simulated days (two-factor SV, no jumps), then one jump of size $c\sqrt{\mathrm{IV}_t}$ at a random time; one-sided test at 0.1\% with 5-minute and 1-minute returns',
      r'@{js.days} de zile simulate (SV cu doi factori, fără salturi), apoi un salt de mărime $c\sqrt{\mathrm{IV}_t}$ la un moment aleator; test unilateral la 0,1\% cu randamente la 5 minute și la 1 minut')],
    h='0.6\\textheight')

interp(('the size and power', 'mărimii și puterii'), [
    T(r'Size without jumps: @{js.clean.5m}\% (5 minutes) and @{js.clean.1m}\% (1 minute) against the nominal 0.1\%; with i.i.d. noise of the calibrated size still @{js.noisy.1m}\% at 1 minute',
      r'Mărimea fără salturi: @{js.clean.5m}\% (5 minute) și @{js.clean.1m}\% (1 minut) față de 0,1\% nominal; cu zgomot i.i.d. de mărimea calibrată, tot @{js.noisy.1m}\% la 1 minut'),
    T(r'Power for a jump of half a daily standard deviation: @{js.p5.1}\% with 5-minute returns, @{js.p1.1}\% with 1-minute returns; for one standard deviation @{js.p5.3}\% and @{js.p1.3}\%',
      r'Puterea pentru un salt de o jumătate de abatere standard zilnică: @{js.p5.1}\% cu randamente la 5 minute, @{js.p1.1}\% cu randamente la 1 minut; pentru o abatere standard @{js.p5.3}\% și @{js.p1.3}\%'),
    T(r'The power depends on $c\sqrt n$: small jumps are absorbed into the diffusion at coarse sampling (Seminar 8, A6 gives the detection threshold)',
      r'Puterea depinde de $c\sqrt n$: salturile mici sînt absorbite în difuzie la o eșantionare rară (Seminarul 8, A6 dă pragul de detectare)'),
    T('The trade-off with noise is the same as for RV: finer sampling raises power until noise and zero returns distort the statistic', 'Compromisul cu zgomotul este același ca pentru RV: o eșantionare mai fină crește puterea pînă cînd zgomotul și randamentele nule distorsionează statistica')])

chart(T('Jump days of Bitcoin and Ether', 'Zilele cu salturi pentru Bitcoin și Ether'), 'ats_ch8_jumps_crypto', 'ATS_ch8_jumps', [
    T(r'Huang--Tauchen test with 5-minute returns ($n = 288$ a UTC day), 2018--2026, $T = @{ju.T}$ days; left: share of jump days at 0.1\% by year; right: distribution of $z_t$ against $N(0, 1)$',
      r'Testul Huang--Tauchen cu randamente la 5 minute ($n = 288$ pe zi UTC), 2018--2026, $T = @{ju.T}$ de zile; stînga: ponderea zilelor cu salturi la 0,1\% pe an; dreapta: distribuția lui $z_t$ față de $N(0, 1)$')],
    h='0.6\\textheight')

interp(('the crypto jump tests', 'testelor de salt pentru criptomonede'), [
    T(r'Bitcoin: @{ju.btc.n} jump days (@{ju.btc.share}\%) where about @{ju.btc.exp} false rejections are expected; Ether: @{ju.eth.n} days (@{ju.eth.share}\%)',
      r'Bitcoin: @{ju.btc.n} zile cu salturi (@{ju.btc.share}\%), unde ne așteptăm la aproximativ @{ju.btc.exp} respingeri false; Ether: @{ju.eth.n} zile (@{ju.eth.share}\%)'),
    T(r'Yet the jumps are small: they make @{ju.btc.jv}\% (Bitcoin) and @{ju.eth.jv}\% (Ether) of total variation; the rest is continuous',
      r'Totuși, salturile sînt mici: reprezintă @{ju.btc.jv}\% (Bitcoin) și @{ju.eth.jv}\% (Ether) din variația totală; restul este continuu'),
    T(r'The whole distribution of $z_t$ is shifted (mean @{ju.btc.mz}, not 0): besides jumps, 24-hour intraday seasonality, zero returns and flash moves violate the assumptions of the null',
      r'Întreaga distribuție a lui $z_t$ este deplasată (media @{ju.btc.mz}, nu 0): pe lîngă salturi, sezonalitatea intraday pe 24 de ore, randamentele nule și mișcările bruște încalcă ipotezele nulei'),
    T('Before calling a day a jump day: standardise returns by an intraday volatility pattern, check zero returns, and control the number of tests', 'Înainte de a declara o zi drept zi cu salt: standardizați randamentele cu un profil al volatilității intraday, verificați randamentele nule și controlați numărul de teste')])

D.recap(('Jumps', 'salturile'), [
    T('BV estimates the continuous part; RV $-$ BV the jump part; TQ makes the test robust to jumps in the quarticity', 'BV estimează partea continuă; RV $-$ BV partea de salt; TQ face testul robust la salturi în cuarticitate'),
    T('The ratio test has good size in simulations; its power grows with $c\\sqrt n$', 'Testul raport are o mărime bună în simulări; puterea lui crește cu $c\\sqrt n$'),
    T('In real data the null is fragile: many rejections, little jump variation; treat jump counts as model-dependent', 'În datele reale, ipoteza nulă este fragilă: multe respingeri, puțină variație din salturi; tratați numărul de salturi ca dependent de model')])

# =============================================================================
# 5. HAR ȘI HARQ
# =============================================================================
D.section('Forecasting realised variance: HAR and HARQ', 'Prognoza varianței realizate: HAR și HARQ')

D.frame(T('The HAR model of Corsi (1/2): the regression', 'Modelul HAR al lui Corsi (1/2): regresia'), items(
    (T(r'\refCor: tomorrow\'s RV is a linear function of the daily, weekly and monthly averages of past RV',
       r'\refCor: RV de mîine este o funcție liniară de mediile zilnică, săptămînală și lunară ale RV din trecut'
       ) + r'''
    \[ \mathrm{RV}_{t+1} = \beta_0 + \beta_d\mathrm{RV}_t + \beta_w\mathrm{RV}^{(w)}_t + \beta_m\mathrm{RV}^{(m)}_t + u_{t+1} \]
    \[ \mathrm{RV}^{(w)}_t = \frac15\sum_{j=0}^4\mathrm{RV}_{t-j}, \qquad \mathrm{RV}^{(m)}_t = \frac1{22}\sum_{j=0}^{21}\mathrm{RV}_{t-j} \]''',
     [T(r'$\mathrm{RV}^{(w)}_t$, $\mathrm{RV}^{(m)}_t$: averages over the last 5 trading days (a week) and the last 22 (a month)',
        r'$\mathrm{RV}^{(w)}_t$, $\mathrm{RV}^{(m)}_t$: mediile pe ultimele 5 zile de tranzacționare (o săptămînă) și pe ultimele 22 (o lună)'),
      T(r'$\beta_d, \beta_w, \beta_m \ge 0$: weights of the three horizons; $\beta_0$: intercept; $u_{t+1}$: forecast error with mean zero',
        r'$\beta_d, \beta_w, \beta_m \ge 0$: ponderile celor trei orizonturi; $\beta_0$: termenul liber; $u_{t+1}$: eroarea de prognoză, cu media zero'),
      T(r'$\beta_d + \beta_w + \beta_m$: the persistence; the closer to 1, the slower volatility returns to its mean',
        r'$\beta_d + \beta_w + \beta_m$: persistența; cu cît este mai aproape de 1, cu atît volatilitatea revine mai lent la medie')]),
    (T('Heterogeneous market hypothesis: daily, weekly and monthly traders react to volatility at their own horizon',
       'Ipoteza pieței eterogene: participanții cu orizont zilnic, săptămînal și lunar reacționează la volatilitate la propriul orizont'),
     [T('the cascade produces slowly decaying autocorrelations', 'cascada produce autocorelații care scad lent')])), 'small')

D.frame(T('The HAR model of Corsi (2/2): estimation and variants', 'Modelul HAR al lui Corsi (2/2): estimare și variante'), items(
    (T(r'Statistically, HAR is an AR(22) with 19 linear restrictions (step-shaped coefficients)', r'Statistic, HAR este un AR(22) cu 19 restricții liniare (coeficienți în trepte)'),
     [T(r'short memory, but it mimics long memory over a month', r'memorie scurtă, dar imită memoria lungă pe orizontul unei luni')]),
    (T(r'OLS is consistent; the errors are heteroskedastic and, for multi-day targets, overlapping', r'OLS este consistent; erorile sînt heteroscedastice și, pentru ținte pe mai multe zile, suprapuse'),
     [T(r'use Newey--West \refNW\ (HAC) standard errors', r'folosiți erorile standard Newey--West \refNW\ (HAC)')]),
    (T(r'Variants', r'Variante'),
     [T(r'log-HAR: the same regression on $\ln\mathrm{RV}$, with near-Gaussian errors; the forecast of RV is $\exp(\hat\mu + \frac12\hat\sigma^2_u)$, with $\hat\mu$ the fitted log value and $\hat\sigma^2_u$ the residual variance',
        r'log-HAR: aceeași regresie pe $\ln\mathrm{RV}$, cu erori aproape gaussiene; prognoza lui RV este $\exp(\hat\mu + \frac12\hat\sigma^2_u)$, cu $\hat\mu$ valoarea ajustată în logaritmi și $\hat\sigma^2_u$ varianța reziduurilor'),
      T(r'HAR on $\sqrt{\mathrm{RV}}$; $h$-day targets (the average RV over the next $h$ days)', r'HAR pe $\sqrt{\mathrm{RV}}$; ținte pe $h$ zile (RV mediu pe următoarele $h$ zile)')]),
    T(r'Extensions: continuous and jump parts, HAR-CJ \refABD; positive and negative semivariances \refPS; implied volatility; leverage terms',
      r'Extensii: părțile continuă și de salt, HAR-CJ \refABD; semivarianțele pozitivă și negativă \refPS; volatilitatea implicită; termeni de levier')), 'small')

chart(T('HAR as a restricted AR(22)', 'HAR ca AR(22) restricționat'), 'ats_ch8_har_weights', 'ATS_ch8_har', [
    T(r'S\&P 500 (Oxford-Man, 5-minute RV, 2000--2022, $T = @{hr.T}$): coefficients of an unrestricted AR(22) by OLS and the step weights implied by the HAR estimates',
      r'S\&P 500 (Oxford-Man, RV la 5 minute, 2000--2022, $T = @{hr.T}$): coeficienții unui AR(22) nerestricționat estimat prin OLS și ponderile în trepte implicate de estimațiile HAR')],
    h='0.6\\textheight')

interp(('the HAR estimates', 'estimațiilor HAR'), [
    T(r'HAR: $\hat\beta_d = @{hr.d}$ (@{hr.d.se}), $\hat\beta_w = @{hr.w}$ (@{hr.w.se}), $\hat\beta_m = @{hr.m}$ (@{hr.m.se}), Newey--West s.e.; $R^2 = @{hr.r2}$; persistence $\sum\hat\beta = @{hr.sum}$',
      r'HAR: $\hat\beta_d = @{hr.d}$ (@{hr.d.se}), $\hat\beta_w = @{hr.w}$ (@{hr.w.se}), $\hat\beta_m = @{hr.m}$ (@{hr.m.se}), erori standard Newey--West; $R^2 = @{hr.r2}$; persistența $\sum\hat\beta = @{hr.sum}$'),
    T(r'The AR(22) with 23 coefficients reaches $R^2 = @{hr.r22}$ in sample, with erratic coefficients; HAR captures the shape with 4',
      r'AR(22) cu 23 de coeficienți ajunge la $R^2 = @{hr.r22}$ în eșantion, cu coeficienți neregulați; HAR surprinde forma cu 4'),
    T(r'Log-HAR: $\hat\beta_d = @{hr.ld}$, $\hat\beta_w = @{hr.lw}$, $\hat\beta_m = @{hr.lm}$, $R^2 = @{hr.r2l}$ on $\ln\mathrm{RV}$; in logs the monthly component matters more',
      r'Log-HAR: $\hat\beta_d = @{hr.ld}$, $\hat\beta_w = @{hr.lw}$, $\hat\beta_m = @{hr.lm}$, $R^2 = @{hr.r2l}$ pe $\ln\mathrm{RV}$; în logaritmi, componenta lunară contează mai mult'),
    T(r'In levels a few crisis days dominate OLS: large standard errors on $\beta_d$ and $\beta_m$; weighted least squares or logs give more stable estimates',
      r'În nivel, cîteva zile de criză domină OLS: erori standard mari pentru $\beta_d$ și $\beta_m$; metoda celor mai mici pătrate ponderate sau logaritmii dau estimații mai stabile')])

D.frame(T('Forecasting design', 'Schema de prognoză'), items(
    T(r'One day ahead, rolling window of 1\,000 days, re-estimated every day; target $\mathrm{RV}_{t+1}$',
      r'Un pas înainte, fereastră mobilă de 1\,000 de zile, reestimare zilnică; ținta $\mathrm{RV}_{t+1}$'),
    (T(r'Losses: MSE $= (\mathrm{RV} - f)^2$ and QLIKE, both robust to the noise in RV (see below)', r'Funcțiile de pierdere: MSE $= (\mathrm{RV} - f)^2$ și QLIKE, ambele robuste la zgomotul din RV (vezi mai jos)'
       ) + r'''
    \[ \mathrm{QLIKE} = \frac{\mathrm{RV}}{f} - \ln\frac{\mathrm{RV}}{f} - 1 \ge 0 \]''',
     [T(r'$f$: the variance forecast; QLIKE is 0 when $f = \mathrm{RV}$ and penalises under-prediction more than over-prediction',
        r'$f$: prognoza varianței; QLIKE este 0 cînd $f = \mathrm{RV}$ și penalizează subestimarea mai mult decît supraestimarea')]),
    (T(r'Insanity filter \refBPQ: a forecast outside the range of the in-sample RV is replaced by the in-sample mean',
       r'Filtrul de plauzibilitate („insanity filter”) \refBPQ: o prognoză din afara intervalului RV din eșantionul de estimare este înlocuită cu media din eșantion'),
     [T('linear HAR-type forecasts can be negative after a spike; QLIKE is then undefined', 'prognozele liniare de tip HAR pot fi negative după un vîrf; QLIKE nu mai este atunci definită'),
      T('the filter is part of the method and must be reported', 'filtrul face parte din metodă și trebuie raportat')]),
    (T(r'Diebold--Mariano \refDM\ $t$-statistic of the loss differential against HAR', r'Statistica $t$ Diebold--Mariano \refDM\ pentru diferența pierderilor față de HAR'),
     [T(r'Newey--West variance; negative = better than HAR, below $-1.96$ significant at 5\%; several models: the model confidence set \refHLN, Chapter 1',
        r'varianță Newey--West; negativă = mai bun decît HAR, sub $-1{,}96$ semnificativ la 5\%; mai multe modele: setul de modele de încredere \refHLN, Capitolul 1')]),
    T(r'Models: HAR, HAR-CJ (continuous part and jump part, from BV), log-HAR; for Bitcoin and Ether also HARQ',
      r'Modele: HAR, HAR-CJ (partea continuă și partea de salt, din BV), log-HAR; pentru Bitcoin și Ether și HARQ')), 'small')

chart(T('HAR extensions out of sample', 'Extensiile HAR în afara eșantionului'), 'ats_ch8_har_oos', 'ATS_ch8_har', [
    T(r'Average QLIKE relative to HAR (below 1 = better), six Oxford-Man indices (2004--2022) and two cryptocurrencies (from @{ho.btc.first}); 1\,000-day rolling window',
      r'QLIKE mediu relativ la HAR (sub 1 = mai bun), șase indici Oxford-Man (2004--2022) și două criptomonede (din @{ho.btc.first}); fereastră mobilă de 1\,000 de zile')],
    h='0.6\\textheight')

interp(('the out-of-sample HAR comparison', 'comparației HAR în afara eșantionului'), [
    T(r'Log-HAR beats HAR in QLIKE for @{ho.nlog} of 6 indices: S\&P 500 @{ho.spx.loghar} (DM @{ho.spx.loghar.dm}), CAC 40 @{ho.cac.loghar} (DM @{ho.cac.loghar.dm}), FTSE @{ho.ftse.loghar} (DM @{ho.ftse.loghar.dm})',
      r'Log-HAR este mai bun decît HAR după QLIKE pentru @{ho.nlog} din 6 indici: S\&P 500 @{ho.spx.loghar} (DM @{ho.spx.loghar.dm}), CAC 40 @{ho.cac.loghar} (DM @{ho.cac.loghar.dm}), FTSE @{ho.ftse.loghar} (DM @{ho.ftse.loghar.dm})'),
    T(r'HAR-CJ helps in @{ho.ncj} of 6 indices, but not for the S\&P 500 (@{ho.spx.harcj}): separating jumps adds estimation noise when jumps are small',
      r'HAR-CJ ajută pentru @{ho.ncj} din 6 indici, dar nu pentru S\&P 500 (@{ho.spx.harcj}): separarea salturilor adaugă zgomot de estimare cînd salturile sînt mici'),
    T(r'The ranking depends on the loss: in MSE the gains of log-HAR are smaller (S\&P 500: @{ho.spx.loghar.m}); MSE weighs the crisis days most',
      r'Ordinea depinde de funcția de pierdere: după MSE, cîștigurile log-HAR sînt mai mici (S\&P 500: @{ho.spx.loghar.m}); MSE pune cea mai mare pondere pe zilele de criză'),
    T('Six indices from one data vendor and one period: report all of them, not the best one (data snooping, Chapter 1)', 'Șase indici de la un singur furnizor de date și o singură perioadă: raportați-i pe toți, nu doar pe cel mai bun (data snooping, Capitolul 1)')])

D.frame(T('HARQ (1/2): the measurement error of RV', 'HARQ (1/2): eroarea de măsurare a lui RV'), items(
    (T(r'RV is the latent IV plus a measurement error whose variance changes every day',
       r'RV este IV latent plus o eroare de măsurare a cărei varianță se schimbă în fiecare zi'
       ) + r'''
    \[ \mathrm{RV}_t = \mathrm{IV}_t + e_t, \qquad \Var(e_t | \mathrm{IQ}_t) \approx \frac{2\,\mathrm{IQ}_t}{n} \]''',
     [T(r'$e_t$: measurement error of day $t$; on volatile days ($\mathrm{IQ}_t$ large) RV is less precise',
        r'$e_t$: eroarea de măsurare din ziua $t$; în zilele volatile ($\mathrm{IQ}_t$ mare), RV este mai puțin precis')]),
    (T(r'Errors in variables: in an AR(1) for IV with coefficient $\phi$, the OLS slope on RV is attenuated (Appendix)',
       r'Erori în variabile: într-un AR(1) pentru IV cu coeficientul $\phi$, panta OLS pe RV este atenuată (Anexa)'
       ) + r'''
    \[ \mathrm{plim}\,\hat\phi = \phi\lambda, \qquad \lambda = \frac{\Var(\mathrm{IV})}{\Var(\mathrm{IV}) + \E\Var(e)} \in (0, 1) \]''',
     [T(r'$\lambda$: reliability ratio, the share of the variance of RV that is signal', r'$\lambda$: raportul de fiabilitate, ponderea semnalului în varianța lui RV'),
      T(r'one constant $\beta_d$ is a compromise: too high on noisy days, too low on precise days', r'un singur $\beta_d$ constant este un compromis: prea mare în zilele zgomotoase, prea mic în zilele precise')])), 'small')

D.frame(T('HARQ (2/2): a weight that depends on precision', 'HARQ (2/2): o pondere care depinde de precizie'), items(
    (T(r'\refBPQ: the weight of yesterday\'s RV moves with its estimated precision', r'\refBPQ: ponderea RV de ieri variază cu precizia lui estimată'
       ) + r'''
    \[ \mathrm{RV}_{t+1} = \beta_0 + \big(\beta_d + \beta_{dQ}\sqrt{\mathrm{RQ}_t}\big)\mathrm{RV}_t + \beta_w\mathrm{RV}^{(w)}_t + \beta_m\mathrm{RV}^{(m)}_t + u_{t+1} \]''',
     [T(r'$\mathrm{RQ}_t$: realised quarticity, the estimate of $\mathrm{IQ}_t$; $\sqrt{\mathrm{RQ}_t}$ is proportional to the standard deviation of $e_t$',
        r'$\mathrm{RQ}_t$: cuarticitatea realizată, estimația lui $\mathrm{IQ}_t$; $\sqrt{\mathrm{RQ}_t}$ este proporțional cu abaterea standard a lui $e_t$'),
      T(r'$\beta_{dQ} < 0$ expected: the less precise yesterday\'s RV, the lower its weight', r'ne așteptăm la $\beta_{dQ} < 0$: cu cît RV de ieri este mai puțin precis, cu atît ponderea lui este mai mică'),
      T(r'$\sqrt{\mathrm{RQ}_t}$ is demeaned, so $\beta_d$ is the weight on a day of average precision', r'$\sqrt{\mathrm{RQ}_t}$ este centrat, astfel încît $\beta_d$ este ponderea unei zile cu precizie medie')]),
    T(r'One extra parameter, still OLS', r'Un singur parametru în plus, tot OLS'),
    (T(r'The original paper: S\&P 500 futures and 27 Dow Jones stocks, gains over HAR in and out of sample',
       r'Lucrarea originală: futures pe S\&P 500 și 27 de acțiuni din Dow Jones, cîștiguri față de HAR în eșantion și în afara lui'),
     [T(r'our replication extends it to Bitcoin and Ether, 2018--2026, where RQ is available from our one-minute data',
        r'replicarea noastră o extinde la Bitcoin și Ether, 2018--2026, unde RQ este disponibil din datele noastre la un minut')])), 'small')

chart(T('HARQ for Bitcoin: a weight that moves with precision', 'HARQ pentru Bitcoin: o pondere care se schimbă cu precizia'), 'ats_ch8_harq', 'ATS_ch8_har', [
    T(r'Full-sample HARQ on Bitcoin 5-minute RV and RQ: daily weight $\hat\beta_d + \hat\beta_{dQ}(\sqrt{\mathrm{RQ}_t} - \overline{\sqrt{\mathrm{RQ}}})$ against the constant HAR weight',
      r'HARQ pe tot eșantionul, pentru RV și RQ la 5 minute ale Bitcoin: ponderea zilnică $\hat\beta_d + \hat\beta_{dQ}(\sqrt{\mathrm{RQ}_t} - \overline{\sqrt{\mathrm{RQ}}})$ față de ponderea constantă din HAR')],
    h='0.6\\textheight')

interp(('HARQ', 'modelului HARQ'), [
    T(r'$\hat\beta_{dQ} = @{hq.q}$ ($t = @{hq.tq}$, Newey--West): negative, as predicted; the daily weight at average precision is @{hq.d}, against @{hq.hd} in HAR',
      r'$\hat\beta_{dQ} = @{hq.q}$ ($t = @{hq.tq}$, Newey--West): negativ, cum prezice teoria; ponderea zilnică la precizie medie este @{hq.d}, față de @{hq.hd} în HAR'),
    T(r'On most days the weight is near @{hq.q50}; on the noisiest days it falls (1\% quantile @{hq.q01}, minimum @{hq.wmin}): yesterday\'s RV is trusted only when it is precise',
      r'În majoritatea zilelor ponderea este în jur de @{hq.q50}; în zilele cele mai zgomotoase scade (cuantila de 1\% @{hq.q01}, minimul @{hq.wmin}): RV de ieri primește încredere doar cînd este precis'),
    T(r'Out of sample, QLIKE relative to HAR: Bitcoin @{ho.btc.harq} (DM @{ho.btc.harq.dm}), Ether @{ho.eth.harq} (DM @{ho.eth.harq.dm}): the gain of the original study carries over to crypto',
      r'În afara eșantionului, QLIKE relativ la HAR: Bitcoin @{ho.btc.harq} (DM @{ho.btc.harq.dm}), Ether @{ho.eth.harq} (DM @{ho.eth.harq.dm}): cîștigul din studiul original se regăsește la criptomonede'),
    T(r'In MSE the picture differs (Bitcoin @{ho.btc.harq.m}): MSE is dominated by a few extreme days, where HARQ shrinks the most; the AI mini-case checks how fragile the gain is',
      r'După MSE imaginea diferă (Bitcoin @{ho.btc.harq.m}): MSE este dominat de cîteva zile extreme, unde HARQ micșorează cel mai mult ponderea; mini studiul de caz AI verifică cît de fragil este cîștigul')])

D.recap(('HAR and HARQ', 'HAR și HARQ'), [
    T('HAR is a parsimonious restricted AR(22) estimated by OLS; logs stabilise it', 'HAR este un AR(22) restricționat și parcimonios, estimat prin OLS; logaritmii îl stabilizează'),
    T('Out-of-sample gains are loss- and market-specific: report all series, the filter and DM tests', 'Cîștigurile în afara eșantionului depind de funcția de pierdere și de piață: raportați toate seriile, filtrul și testele DM'),
    T('HARQ lets the measurement error of RV set the weight of yesterday: one parameter, a robust gain in QLIKE', 'HARQ lasă eroarea de măsurare a RV să stabilească ponderea zilei de ieri: un parametru, un cîștig robust după QLIKE')])

# =============================================================================
# 6. REALIZED GARCH ȘI HEAVY
# =============================================================================
D.section('Realized GARCH and HEAVY', 'Realized GARCH și HEAVY')

D.frame(T('Realized GARCH (1/2): the three equations', 'Realized GARCH (1/2): cele trei ecuații'), items(
    (T(r'\refHHS, log-linear form: a return equation, a GARCH equation driven by the realised measure, and a measurement equation',
       r'\refHHS, forma log-liniară: o ecuație a randamentului, o ecuație GARCH determinată de măsura realizată și o ecuație de măsurare'
       ) + r'''
    \[ r_t = \sqrt{h_t}\,z_t, \qquad \ln h_t = \omega + \beta\ln h_{t-1} + \gamma\ln x_{t-1} \]
    \[ \ln x_t = \xi + \varphi\ln h_t + \tau(z_t) + u_t \]''',
     [T(r'$h_t$: conditional variance of the return $r_t$; $z_t$: i.i.d. standardised shock; $x_t$: realised measure of day $t$ (here the realised kernel RK)',
        r'$h_t$: varianța condiționată a randamentului $r_t$; $z_t$: șoc standardizat i.i.d.; $x_t$: măsura realizată din ziua $t$ (aici realised kernel-ul RK)'),
      T(r'$\beta$: persistence of $\ln h_t$; $\gamma$: weight of yesterday\'s realised measure (the news variable that replaces $\varepsilon^2_{t-1}$)',
        r'$\beta$: persistența lui $\ln h_t$; $\gamma$: ponderea măsurii realizate de ieri (variabila de știri care înlocuiește $\varepsilon^2_{t-1}$)'),
      T(r'$u_t$: measurement error, i.i.d. $N(0, \sigma^2_u)$, independent of $z_t$', r'$u_t$: eroarea de măsurare, i.i.d. $N(0, \sigma^2_u)$, independentă de $z_t$')]),
    (T(r'Measurement equation: $x_t$ is a noisy, possibly biased signal of $h_t$', r'Ecuația de măsurare: $x_t$ este un semnal zgomotos, posibil deplasat, al lui $h_t$'),
     [T(r'$\varphi = 1$: $x_t$ proportional to $h_t$; $\xi$ absorbs the scale (open-to-close measure against close-to-close variance)',
        r'$\varphi = 1$: $x_t$ proporțional cu $h_t$; $\xi$ preia diferența de scală (măsura deschidere--închidere față de varianța închidere--închidere)'),
      T(r'leverage function $\tau(z) = \tau_1z + \tau_2(z^2 - 1)$: with $\tau_1 < 0$, negative returns raise the next realised measure (news impact, TSA, Chapter 5)',
        r'funcția de levier $\tau(z) = \tau_1z + \tau_2(z^2 - 1)$: cu $\tau_1 < 0$, randamentele negative cresc următoarea măsură realizată (impactul știrilor, TSA, Capitolul 5)')])), 'footnotesize')

D.frame(T('Realized GARCH (2/2): reduced form and estimation', 'Realized GARCH (2/2): forma redusă și estimarea'), items(
    (T(r'Substituting the measurement equation into the GARCH equation: $\ln h_t$ is an AR(1)', r'Înlocuind ecuația de măsurare în ecuația GARCH: $\ln h_t$ este un AR(1)'
       ) + r'''
    \[ \ln h_t = (\omega + \gamma\xi) + \pi\ln h_{t-1} + \gamma\big(\tau(z_{t-1}) + u_{t-1}\big), \qquad \pi = \beta + \varphi\gamma \]''',
     [T(r'$\pi$: persistence of the log variance; multi-step forecasts follow, because $x_t$ has its own equation',
        r'$\pi$: persistența logaritmului varianței; prognozele cu mai mulți pași decurg din ea, pentru că $x_t$ are propria ecuație')]),
    (T(r'Joint QML: the log-likelihood sums a return part and a measurement part', r'QML comun: log-verosimilitatea însumează o parte pentru randamente și o parte pentru măsurare'
       ) + r'''
    \[ \ell = -\frac12\sum_t\Big[\underbrace{\ln h_t + z_t^2}_{r_t} + \underbrace{\ln\sigma^2_u + u_t^2/\sigma^2_u}_{x_t}\Big] \]''',
     [T(r'comparison with GARCH only through the partial likelihood of $r_t$ (the first part), since GARCH does not model $x_t$',
        r'comparația cu GARCH se face doar prin verosimilitatea parțială a lui $r_t$ (prima parte), deoarece GARCH nu modelează $x_t$')])), 'small')

D.frame(T('HEAVY and the family of realised-measure models', 'HEAVY și familia modelelor cu măsuri realizate'), items(
    (T(r'HEAVY \refSS: two GARCH-type equations, one for the return variance and one for the mean of the realised measure',
       r'HEAVY \refSS: două ecuații de tip GARCH, una pentru varianța randamentului și una pentru media măsurii realizate'
       ) + r'''
    \[ h_t = \Var(r_t | \mathcal F_{t-1}) = \omega + \alpha\mathrm{RM}_{t-1} + \beta h_{t-1} \]
    \[ \mu_t = \E(\mathrm{RM}_t | \mathcal F_{t-1}) = \omega_R + \alpha_R\mathrm{RM}_{t-1} + \beta_R\mu_{t-1} \]''',
     [T(r'$\mathrm{RM}_t$: realised measure of day $t$; $(\omega, \alpha, \beta)$ and $(\omega_R, \alpha_R, \beta_R)$: the parameters of the two equations',
        r'$\mathrm{RM}_t$: măsura realizată din ziua $t$; $(\omega, \alpha, \beta)$ și $(\omega_R, \alpha_R, \beta_R)$: parametrii celor două ecuații'),
      T(r'each equation is estimated separately by QML; momentum: after a shock, $h_t$ keeps rising while $\mu_t$ catches up',
        r'fiecare ecuație se estimează separat prin QML; „momentum”: după un șoc, $h_t$ continuă să crească pînă cînd $\mu_t$ îl ajunge din urmă'),
      T(r'when the realised measure is in the variance equation, the squared return usually adds nothing ($\varepsilon^2_{t-1}$ gets a zero coefficient)',
        r'cînd măsura realizată intră în ecuația varianței, pătratul randamentului de obicei nu mai adaugă nimic ($\varepsilon^2_{t-1}$ primește coeficientul zero)')]),
    T(r'Realized EGARCH \refHH: several realised measures and a richer leverage; score-driven versions exist for fat tails',
      r'Realized EGARCH \refHH: mai multe măsuri realizate și un efect de levier mai bogat; există versiuni de tip score-driven pentru cozi groase'),
    T(r'Compared with HAR: returns and realised measures are modelled jointly, so densities and VaR/ES forecasts are available (Chapter 9)',
      r'Comparativ cu HAR: randamentele și măsurile realizate sînt modelate împreună, deci sînt disponibile prognoze de densitate și de VaR/ES (Capitolul 9)')), 'footnotesize')

chart(T('Case study: Realized GARCH for the S\\&P 500', 'Studiu de caz: Realized GARCH pentru S\\&P 500'), 'ats_ch8_rgarch', 'ATS_ch8_realized_garch', [
    T(r'Open-to-close returns and the Parzen realised kernel (Oxford-Man), 2000--2022, $T = @{rg.T}$, as in \refHHS; left: the 2008 crisis; right: the estimated leverage function',
      r'Randamente deschidere--închidere și realised kernel-ul Parzen (Oxford-Man), 2000--2022, $T = @{rg.T}$, ca în \refHHS; stînga: criza din 2008; dreapta: funcția de levier estimată')],
    h='0.6\\textheight')

D.frame(T('Realized GARCH estimates', 'Estimațiile Realized GARCH'), table(
    'cccccccc', r'$\omega$ & $\beta$ & $\gamma$ & $\xi$ & $\varphi$ & $\tau_1$ & $\tau_2$ & $\sigma_u$',
    [r'@{rg.om} & @{rg.b} & @{rg.g} & @{rg.xi} & @{rg.phi} & @{rg.t1} & @{rg.t2} & @{rg.su}',
     r'(@{rg.om.se}) & (@{rg.b.se}) & (@{rg.g.se}) & (@{rg.xi.se}) & (@{rg.phi.se}) & (@{rg.t1.se}) & (@{rg.t2.se}) & (@{rg.su.se})'],
    size='footnotesize') + items(
    T(r'Bollerslev--Wooldridge s.e. in brackets; persistence $\hat\pi = \hat\beta + \hat\varphi\hat\gamma = @{rg.pers}$ (GARCH(1,1) on the same returns: @{rg.gp})',
      r'Erori standard Bollerslev--Wooldridge în paranteze; persistența $\hat\pi = \hat\beta + \hat\varphi\hat\gamma = @{rg.pers}$ (GARCH(1,1) pe aceleași randamente: @{rg.gp})'),
    T(r'Partial log-likelihood of the returns: Realized GARCH @{rg.ll_r}, HEAVY @{rg.ll_heavy}, GJR @{rg.ll_gjr}, GARCH(1,1) @{rg.ll_garch}',
      r'Log-verosimilitatea parțială a randamentelor: Realized GARCH @{rg.ll_r}, HEAVY @{rg.ll_heavy}, GJR @{rg.ll_gjr}, GARCH(1,1) @{rg.ll_garch}'),
    T(r'HEAVY variance equation: $\hat\alpha = @{rg.hv.a}$ on $\mathrm{RK}_{t-1}$, $\hat\beta = @{rg.hv.b}$', r'Ecuația varianței HEAVY: $\hat\alpha = @{rg.hv.a}$ pentru $\mathrm{RK}_{t-1}$, $\hat\beta = @{rg.hv.b}$')), 'small')

interp(('Realized GARCH', 'modelului Realized GARCH'), [
    T(r'$\hat\varphi = @{rg.phi}$: the kernel is proportional to the conditional variance; $\hat\xi = @{rg.xi}$ with $\hat\sigma_u = @{rg.su}$: on average the kernel lies below the conditional variance of the open-to-close return',
      r'$\hat\varphi = @{rg.phi}$: kernel-ul este proporțional cu varianța condiționată; $\hat\xi = @{rg.xi}$, cu $\hat\sigma_u = @{rg.su}$: în medie, kernel-ul se află sub varianța condiționată a randamentului deschidere--închidere'),
    T(r'$\hat\gamma = @{rg.g}$ is large and $\hat\beta = @{rg.b}$ smaller than in GARCH: the realised measure brings information faster than squared returns (left panel, autumn 2008)',
      r'$\hat\gamma = @{rg.g}$ este mare, iar $\hat\beta = @{rg.b}$ mai mic decît în GARCH: măsura realizată aduce informația mai repede decît pătratele randamentelor (panoul din stînga, toamna lui 2008)'),
    T(r'Leverage: $\hat\tau_1 = @{rg.t1}$, $\hat\tau_2 = @{rg.t2}$: an asymmetric parabola, larger for negative $z$',
      r'Levierul: $\hat\tau_1 = @{rg.t1}$, $\hat\tau_2 = @{rg.t2}$: o parabolă asimetrică, mai mare pentru $z$ negativ'),
    T(r'The gain in the partial likelihood over GARCH(1,1) (@{rg.gain} points) has the direction of the original paper; HEAVY is almost as good with three parameters',
      r'Cîștigul în verosimilitatea parțială față de GARCH(1,1), egal cu @{rg.gain}, are direcția din lucrarea originală; HEAVY este aproape la fel de bun, cu trei parametri')])

D.recap(('Realised-measure GARCH', 'modelele GARCH cu măsuri realizate'), [
    T('A realised measure in the variance equation beats squared returns as the news variable', 'O măsură realizată în ecuația varianței este o variabilă de știri mai bună decît pătratul randamentului'),
    T('Realized GARCH adds a measurement equation: multi-step forecasts, leverage and a joint likelihood', 'Realized GARCH adaugă o ecuație de măsurare: prognoze cu mai mulți pași, levier și o verosimilitate comună'),
    T('Compare with GARCH only on the partial likelihood of returns', 'Comparația cu GARCH se face doar pe verosimilitatea parțială a randamentelor')])

# =============================================================================
# 7. EVALUAREA PROGNOZELOR
# =============================================================================
D.section('Evaluating volatility forecasts with a noisy target', 'Evaluarea prognozelor de volatilitate față de o țintă zgomotoasă')

D.frame(T('The proxy problem and robust losses (1/2)', 'Problema proxy-ului și funcțiile de pierdere robuste (1/2)'), items(
    (T(r'We never see $\sigma^2_t$: a forecast $h_t$ is compared with a proxy $\hat\sigma^2_t$ (squared return, RV, RK)',
       r'Nu observăm niciodată $\sigma^2_t$: o prognoză $h_t$ este comparată cu un proxy $\hat\sigma^2_t$ (pătratul randamentului, RV, RK)'),
     [T(r'the proxy is conditionally unbiased, $\E(\hat\sigma^2_t | \mathcal F_{t-1}) = \sigma^2_t$, but noisy',
        r'proxy-ul este nedeplasat condiționat, $\E(\hat\sigma^2_t | \mathcal F_{t-1}) = \sigma^2_t$, dar zgomotos')]),
    (T(r'A loss $L$ is \emph{robust} \refPat\ if the ranking of forecasts by $\E L(\hat\sigma^2_t, h_t)$ equals the ranking by $\E L(\sigma^2_t, h_t)$, for every unbiased proxy \refHLb',
       r'O funcție de pierdere $L$ este \emph{robustă} \refPat\ dacă ordinea prognozelor după $\E L(\hat\sigma^2_t, h_t)$ coincide cu ordinea după $\E L(\sigma^2_t, h_t)$, pentru orice proxy nedeplasat \refHLb'),
     []),
    (T(r'Necessary and sufficient condition: a Bregman form (Chapter 1, consistent scoring functions for the mean)',
       r'Condiția necesară și suficientă: o formă Bregman (Capitolul 1, funcții de scor consistente pentru medie)'
       ) + r'''
    \[ L(\hat\sigma^2, h) = \tilde C(h) + B(\hat\sigma^2) + C(h)(\hat\sigma^2 - h), \qquad C'(h) < 0 \]''',
     [T(r'$C$: a decreasing function of the forecast; $\tilde C$: its antiderivative, $\tilde C\' = C$; $B$: any function of the proxy alone (it does not affect the ranking)',
        r'$C$: o funcție descrescătoare de prognoză; $\tilde C$: primitiva ei, $\tilde C\' = C$; $B$: orice funcție doar de proxy (nu influențează ordinea)')])), 'small')

D.frame(T('The proxy problem and robust losses (2/2)', 'Problema proxy-ului și funcțiile de pierdere robuste (2/2)'), items(
    (T(r'Robust: MSE and QLIKE, the members of degree 2 and degree 0 of the homogeneous robust family', r'Robuste: MSE și QLIKE, membrii de grad 2 și de grad 0 ai familiei omogene robuste'
       ) + r'''
    \[ \mathrm{MSE} = (\hat\sigma^2 - h)^2, \qquad \mathrm{QLIKE} = \frac{\hat\sigma^2}{h} - \ln\frac{\hat\sigma^2}{h} - 1 \]''',
     [T(r'degree: how the loss scales when proxy and forecast are multiplied by the same constant; QLIKE (degree 0) is scale-free and penalises under-prediction more',
        r'gradul: cum se scalează pierderea cînd proxy-ul și prognoza sînt înmulțite cu aceeași constantă; QLIKE (grad 0) nu depinde de scală și penalizează mai mult subestimarea')]),
    (T(r'Not robust: MAE $= |\hat\sigma^2 - h|$, MSE on logs $(\ln\hat\sigma^2 - \ln h)^2$, MSE on standard deviations',
       r'Nerobuste: MAE $= |\hat\sigma^2 - h|$, MSE pe logaritmi $(\ln\hat\sigma^2 - \ln h)^2$, MSE pe abateri standard'),
     [T(r'with a noisy proxy they reward forecasts that are biased downwards', r'cu un proxy zgomotos, ele recompensează prognozele deplasate în jos')]),
    (T(r'Example: with $\hat\sigma^2 = r^2$, the MSE-log optimum is $h^* = \exp(\E\ln r^2) = @{pt.copt}\,\sigma^2$',
       r'Exemplu: cu $\hat\sigma^2 = r^2$, optimul MSE-log este $h^* = \exp(\E\ln r^2) = @{pt.copt}\,\sigma^2$'),
     [T(r'because $r^2 = \sigma^2\chi^2_1$ for a Gaussian return and $\E\ln\chi^2_1 = -1.27$: MSE-log prefers a forecast far below the truth',
        r'pentru că $r^2 = \sigma^2\chi^2_1$ pentru un randament gaussian, iar $\E\ln\chi^2_1 = -1{,}27$: MSE-log preferă o prognoză mult sub valoarea adevărată')])), 'small')

chart(T('Robust and non-robust losses', 'Funcții de pierdere robuste și nerobuste'), 'ats_ch8_patton', 'ATS_ch8_robust_loss', [
    T(r'True variance against a forecast biased down by the factor @{pt.c}; proxy = RV from $n$ intraday returns ($n = 1$: squared daily return); relative gap of expected losses, above zero = the true variance wins',
      r'Varianța adevărată față de o prognoză deplasată în jos cu factorul @{pt.c}; proxy = RV din $n$ randamente intraday ($n = 1$: pătratul randamentului zilnic); diferența relativă a pierderilor așteptate, peste zero = cîștigă varianța adevărată')],
    h='0.6\\textheight')

interp(('the robustness experiment', 'experimentului de robustețe'), [
    T(r'With the squared return as proxy, MAE prefers the biased forecast (gap @{pt.mae.1}\%) and so does MSE-log (@{pt.ml.1}\%); MSE (@{pt.mse.1}\%) and QLIKE (@{pt.ql.1}\%) do not',
      r'Cu pătratul randamentului ca proxy, MAE preferă prognoza deplasată (diferența @{pt.mae.1}\%) la fel ca MSE-log (@{pt.ml.1}\%); MSE (@{pt.mse.1}\%) și QLIKE (@{pt.ql.1}\%) nu'),
    T(r'With $n = 5$ intraday returns all four losses rank correctly: a precise proxy makes non-robust losses ``almost'' robust \refHLb',
      r'Cu $n = 5$ randamente intraday, toate cele patru funcții ordonează corect: un proxy precis face funcțiile nerobuste „aproape” robuste \refHLb'),
    T('The danger is largest exactly where realised measures are unavailable: daily data, emerging markets, long histories', 'Pericolul este cel mai mare exact acolo unde nu există măsuri realizate: date zilnice, piețe emergente, istorii lungi'),
    T('Rule: evaluate volatility forecasts with QLIKE (and MSE), against the best available proxy', 'Regula: evaluați prognozele de volatilitate cu QLIKE (și MSE), față de cel mai bun proxy disponibil')])

chart(T('Seven forecasts of S\\&P 500 volatility', 'Șapte prognoze ale volatilității S\\&P 500'), 'ats_ch8_vol_oos', 'ATS_ch8_robust_loss', [
    T(r'Open-to-close variance, one day ahead, 2016--2022 ($@{vo.T}$ days); expanding window from 2000, parameters re-estimated every 250 days; proxy: realised kernel',
      r'Varianța deschidere--închidere, un pas înainte, 2016--2022 ($@{vo.T}$ zile); fereastră extinsă din 2000, parametrii reestimați la fiecare 250 de zile; proxy: realised kernel')],
    h='0.6\\textheight')

interp(('the forecast comparison', 'comparației prognozelor'), [
    T(r'QLIKE: HAR @{vo.har.q}, log-HAR @{vo.lh.q}, Realized GARCH @{vo.rg.q}, HEAVY @{vo.hv.q}, GARCH-$t$ @{vo.gt.q}, GJR @{vo.gjr.q}, GARCH @{vo.g.q}',
      r'QLIKE: HAR @{vo.har.q}, log-HAR @{vo.lh.q}, Realized GARCH @{vo.rg.q}, HEAVY @{vo.hv.q}, GARCH-$t$ @{vo.gt.q}, GJR @{vo.gjr.q}, GARCH @{vo.g.q}'),
    T(r'DM against HAR (QLIKE): GARCH @{vo.g.dq}, GJR @{vo.gjr.dq}, Realized GARCH @{vo.rg.dq}, log-HAR @{vo.lh.dq}: realised-measure models beat return-only models clearly; among them the differences are small',
      r'DM față de HAR (QLIKE): GARCH @{vo.g.dq}, GJR @{vo.gjr.dq}, Realized GARCH @{vo.rg.dq}, log-HAR @{vo.lh.dq}: modelele cu măsuri realizate sînt clar mai bune decît cele doar cu randamente; între ele diferențele sînt mici'),
    T(r'In MSE, HAR (@{vo.har.m}) leads and the DM statistics are smaller: the 2020 crash dominates the squared errors',
      r'După MSE, HAR (@{vo.har.m}) conduce, iar statisticile DM sînt mai mici: crahul din 2020 domină erorile pătratice'),
    T('One proxy (RK) for all models: the HAR family is fitted to that same measure, which favours it; a fair comparison also tries another proxy (RV, BV)', 'Un singur proxy (RK) pentru toate modelele: familia HAR este estimată pe aceeași măsură, ceea ce o avantajează; o comparație corectă încearcă și alt proxy (RV, BV)')])

D.recap(('Evaluation', 'evaluarea'), [
    T('Only losses of the Patton class keep the ranking under a noisy unbiased proxy: MSE and QLIKE', 'Doar funcțiile din clasa Patton păstrează ordinea cu un proxy nedeplasat zgomotos: MSE și QLIKE'),
    T('Realised-measure models beat return-only GARCH one day ahead; DM and the MCS of Chapter 1 quantify by how much', 'La un pas, modelele cu măsuri realizate depășesc modelele GARCH care folosesc doar randamentele; DM și MCS din Capitolul 1 cuantifică diferența'),
    T('State the proxy, the loss, the window and the filter: each can change the ranking', 'Precizați proxy-ul, funcția de pierdere, fereastra și filtrul: fiecare poate schimba ordinea')])

# =============================================================================
# 8. GARCH MULTIVARIAT
# =============================================================================
D.section('Multivariate GARCH and large covariance matrices', 'GARCH multivariat și matrice de covarianță mari')

D.frame(T('From one variance to a covariance matrix (1/2)', 'De la o varianță la o matrice de covarianță (1/2)'), items(
    (T(r'The vector of $N$ return shocks is a matrix square root of the conditional covariance times a standardised vector',
       r'Vectorul celor $N$ șocuri ale randamentelor este produsul dintre o rădăcină pătrată matriceală a covarianței condiționate și un vector standardizat'
       ) + r'''
    \[ \varepsilon_t = H_t^{1/2}\eta_t, \qquad \eta_t \ \text{i.i.d.}\ (0, I_N) \]''',
     [T(r'$H_t = \Var(\varepsilon_t | \mathcal F_{t-1})$: $N \times N$ conditional covariance matrix; $I_N$: identity matrix',
        r'$H_t = \Var(\varepsilon_t | \mathcal F_{t-1})$: matricea de covarianță condiționată, $N \times N$; $I_N$: matricea identitate'),
      T(r'$H_t$ must be symmetric positive definite for every $t$ and every parameter value',
        r'$H_t$ trebuie să fie simetrică și pozitiv definită pentru orice $t$ și orice valoare a parametrilor')]),
    (T(r'VEC: every element of $H_t$ depends on all past squares and cross-products', r'VEC: fiecare element al lui $H_t$ depinde de toate pătratele și produsele încrucișate din trecut'
       ) + r'''
    \[ \mathrm{vech}(H_t) = c + A\,\mathrm{vech}(\varepsilon_{t-1}\varepsilon_{t-1}') + B\,\mathrm{vech}(H_{t-1}) \]''',
     [T(r'$\mathrm{vech}$: stacks the $N(N+1)/2$ distinct elements of a symmetric matrix; $c$: vector, $A$, $B$: square matrices of that size',
        r'$\mathrm{vech}$: așază într-un vector cele $N(N+1)/2$ elemente distincte ale unei matrice simetrice; $c$: vector, $A$, $B$: matrice pătrate de această dimensiune'),
      T('general, but positivity is hard to impose', 'general, dar pozitivitatea este greu de impus')])), 'small')

D.frame(T('From one variance to a covariance matrix (2/2): BEKK, CCC and DCC', 'De la o varianță la o matrice de covarianță (2/2): BEKK, CCC și DCC'), items(
    (T(r'BEKK \refEK: quadratic forms guarantee positive definiteness', r'BEKK \refEK: formele pătratice garantează caracterul pozitiv definit'
       ) + r'''
    \[ H_t = CC' + A'\varepsilon_{t-1}\varepsilon_{t-1}'A + B'H_{t-1}B \]''',
     [T(r'$C$: lower-triangular $N \times N$; $A$, $B$: $N \times N$ matrices; diagonal and scalar versions restrict $A$, $B$',
        r'$C$: matrice inferior triunghiulară $N \times N$; $A$, $B$: matrice $N \times N$; versiunile diagonală și scalară restricționează $A$, $B$'),
      T(r'identification: $(A, B)$ and $(-A, -B)$ give the same $H_t$; fix the sign of one element', r'identificarea: $(A, B)$ și $(-A, -B)$ dau aceeași $H_t$; se fixează semnul unui element')]),
    (T(r'CCC \refBolC\ and DCC \refEngD: variances from univariate GARCH, correlations modelled separately', r'CCC \refBolC\ și DCC \refEngD: varianțele din GARCH univariate, corelațiile modelate separat'
       ) + r'''
    \[ H_t = D_tRD_t\ \ (\text{CCC}), \qquad H_t = D_tR_tD_t\ \ (\text{DCC}), \qquad D_t = \mathrm{diag}(\sigma_{1t}, \dots, \sigma_{Nt}) \]''',
     [T(r'$\sigma_{it}$: conditional standard deviation of asset $i$ from its own GARCH; $R$: constant correlation matrix; $R_t$: time-varying correlation matrix',
        r'$\sigma_{it}$: abaterea standard condiționată a activului $i$, din propriul GARCH; $R$: matricea de corelație constantă; $R_t$: matricea de corelație variabilă în timp')])), 'small')

D.frame(T('The curse of dimensionality in numbers', 'Blestemul dimensionalității în cifre'), table(
    'rrrrrr', r'$N$ & VEC & BEKK & ' + T('diagonal BEKK', 'BEKK diagonal') + ' & ' + T('scalar BEKK', 'BEKK scalar') + r' & DCC',
    [f'{k} & @{{np.{k}.vec}} & @{{np.{k}.bekk}} & @{{np.{k}.dbekk}} & @{{np.{k}.sbekk}} & @{{np.{k}.dcc}}' for k in ('2', '5', '10', '25', '50', '100')],
    size='footnotesize') + items(
    T(r'Counts of free parameters of the (1,1) versions; DCC: $3N$ univariate GARCH parameters, 2 correlation parameters and the $N(N-1)/2$ elements of the target',
      r'Numărul parametrilor liberi ai versiunilor (1,1); DCC: $3N$ parametri GARCH univariați, 2 parametri ai corelației și cele $N(N-1)/2$ elemente ale țintei'),
    T(r'The DCC target is estimated by moments (correlation targeting), so the numerical search has only 2 parameters at any $N$; the price: $N(N-1)/2$ estimated correlations',
      r'Ținta DCC este estimată prin momente (correlation targeting), deci căutarea numerică are doar 2 parametri pentru orice $N$; prețul: $N(N-1)/2$ corelații estimate')), 'small')

D.frame(T('Asymptotic theory for multivariate GARCH', 'Teoria asimptotică pentru GARCH multivariat'), items(
    T(r'Gaussian QML is the standard estimator; consistency and asymptotic normality: VEC and BEKK \refCL, \refHP; CCC with ARMA means \refLMc',
      r'QML gaussian este estimatorul standard; consistența și normalitatea asimptotică: VEC și BEKK \refCL, \refHP; CCC cu medii ARMA \refLMc'),
    (T(r'Conditions are stronger than in the univariate case (moments of order 6 or 8 for BEKK in early results); the sandwich of the univariate section carries over',
       r'Condițiile sînt mai puternice decît în cazul univariat (momente de ordinul 6 sau 8 pentru BEKK în primele rezultate); sandwich-ul din secțiunea univariată se păstrează'),
     []),
    (T(r'DCC is estimated in two steps \refES: (1) univariate GARCH for each series; (2) QML of the correlation part given the standardised residuals $z_t = D_t^{-1}\varepsilon_t$',
       r'DCC se estimează în doi pași \refES: (1) GARCH univariat pentru fiecare serie; (2) QML pentru partea de corelație, condiționat de reziduurile standardizate $z_t = D_t^{-1}\varepsilon_t$'),
     [T(r'second-step standard errors must account for the first step (a GMM-type correction); naive second-step s.e. are too small',
        r'erorile standard din pasul al doilea trebuie să țină seama de primul pas (o corecție de tip GMM); erorile standard naive din pasul al doilea sînt prea mici')]),
    T(r'Large $N$: the full likelihood needs $R_t^{-1}$ and $|R_t|$ at each $t$ ($O(N^3)$) and the score is dominated by noise; composite likelihood over pairs \refPSSE\ avoids both',
      r'$N$ mare: verosimilitatea completă cere $R_t^{-1}$ și $|R_t|$ la fiecare $t$ ($O(N^3)$), iar scorul este dominat de zgomot; verosimilitatea compusă pe perechi \refPSSE\ le evită pe amîndouă')), 'small')

D.frame(T('DCC and its corrected version cDCC (1/2): DCC', 'DCC și versiunea corectată cDCC (1/2): DCC'), two(
    ph('engle', T('Robert F. Engle, 2017', 'Robert F. Engle, 2017'), h='0.3\\textheight'),
    items((T(r'DCC: a GARCH(1,1)-type recursion for a quasi-correlation matrix $Q_t$, rescaled into a correlation matrix',
             r'DCC: o recursie de tip GARCH(1,1) pentru o matrice de cvasi-corelație $Q_t$, rescalată apoi într-o matrice de corelație'
             ) + r'''
    \[ Q_t = (1 - a - b)S + a\,z_{t-1}z_{t-1}' + b\,Q_{t-1} \]
    \[ R_t = \mathrm{diag}(Q_t)^{-1/2}\,Q_t\,\mathrm{diag}(Q_t)^{-1/2} \]''',
           [T(r'$z_t = D_t^{-1}\varepsilon_t$: standardised residuals of the univariate GARCH models; $S$: their sample correlation matrix (the target)',
              r'$z_t = D_t^{-1}\varepsilon_t$: reziduurile standardizate ale modelelor GARCH univariate; $S$: matricea lor de corelație de eșantion (ținta)'),
            T(r'$a \ge 0$: reaction of correlations to yesterday\'s co-movement; $b \ge 0$: persistence; $a + b < 1$',
              r'$a \ge 0$: reacția corelațiilor la co-mișcarea de ieri; $b \ge 0$: persistența; $a + b < 1$'),
            T(r'$\mathrm{diag}(Q_t)$: the diagonal matrix of the diagonal elements of $Q_t$; the rescaling puts ones on the diagonal of $R_t$',
              r'$\mathrm{diag}(Q_t)$: matricea diagonală formată din elementele de pe diagonala lui $Q_t$; rescalarea pune valoarea 1 pe diagonala lui $R_t$')])), '0.3', '0.68'), 'footnotesize')

D.frame(T('DCC and its corrected version cDCC (2/2): cDCC', 'DCC și versiunea corectată cDCC (2/2): cDCC'), items(
    (T(r'\refAie: the DCC target is estimated inconsistently', r'\refAie: ținta DCC este estimată inconsistent'),
     [T(r'$\E(z_tz_t\' | \mathcal F_{t-1}) = R_t \ne Q_t$, so in general $\E Q_t \ne \E z_tz_t\'$',
        r'$\E(z_tz_t\' | \mathcal F_{t-1}) = R_t \ne Q_t$, deci în general $\E Q_t \ne \E z_tz_t\'$'),
      T(r'the moment estimator of $S$ is inconsistent, and so is $(\hat a, \hat b)$', r'estimatorul prin momente al lui $S$ este inconsistent, la fel și $(\hat a, \hat b)$')]),
    (T(r'cDCC: rescale the residuals by the diagonal of $Q_{t-1}$ before they enter the recursion', r'cDCC: reziduurile sînt rescalate cu diagonala lui $Q_{t-1}$ înainte de a intra în recursie'
       ) + r'''
    \[ z^*_{t-1} = \mathrm{diag}(Q_{t-1})^{1/2}z_{t-1}, \qquad Q_t = (1 - a - b)S + a\,z^*_{t-1}z^{*\prime}_{t-1} + b\,Q_{t-1} \]''',
     [T(r'then $\E(z^*_tz^{*\prime}_t | \mathcal F_{t-1}) = Q_t$, and $S = \E z^*_tz^{*\prime}_t$ is a valid target',
        r'atunci $\E(z^*_tz^{*\prime}_t | \mathcal F_{t-1}) = Q_t$, iar $S = \E z^*_tz^{*\prime}_t$ este o țintă validă'),
      T(r'the cDCC target depends on $(a, b)$: it is estimated iteratively inside the likelihood', r'ținta cDCC depinde de $(a, b)$: se estimează iterativ, în interiorul verosimilității')])), 'small')

chart(T('DCC against cDCC: a simulation', 'DCC față de cDCC: o simulare'), 'ats_ch8_dcc_sim', 'ATS_ch8_mgarch', [
    T(r'Bivariate cDCC process with $a = 0.05$, $b = 0.93$, target correlation 0.5, unit variances; $T = @{ds.T}$, @{ds.reps} replications; both estimators on each sample',
      r'Proces cDCC bivariat cu $a = 0{,}05$, $b = 0{,}93$, corelația-țintă 0,5, varianțe unitare; $T = @{ds.T}$, @{ds.reps} de replicări; ambii estimatori pe fiecare eșantion')],
    h='0.6\\textheight')

interp(('the DCC simulation', 'simulării DCC'), [
    T(r'Mean estimates: DCC $\hat a = @{ds.d.a}$, $\hat b = @{ds.d.b}$; cDCC $\hat a = @{ds.c.a}$, $\hat b = @{ds.c.b}$ (true 0.05 and 0.93)',
      r'Estimațiile medii: DCC $\hat a = @{ds.d.a}$, $\hat b = @{ds.d.b}$; cDCC $\hat a = @{ds.c.a}$, $\hat b = @{ds.c.b}$ (valorile adevărate 0,05 și 0,93)'),
    T(r'RMSE of $\hat a$: @{ds.d.a.rmse} (DCC) and @{ds.c.a.rmse} (cDCC); of $\hat b$: @{ds.d.b.rmse} and @{ds.c.b.rmse}: the inconsistency is real but small at these persistence levels',
      r'RMSE pentru $\hat a$: @{ds.d.a.rmse} (DCC) și @{ds.c.a.rmse} (cDCC); pentru $\hat b$: @{ds.d.b.rmse} și @{ds.c.b.rmse}: inconsistența este reală, dar mică la aceste niveluri de persistență'),
    T('Sampling error dominates the bias with two thousand observations; the difference matters more for the target in large systems and for inference on $(a, b)$',
      'Eroarea de eșantionare domină deplasarea la două mii de observații; diferența contează mai mult pentru țintă în sisteme mari și pentru inferența asupra lui $(a, b)$'),
    T('A proof of inconsistency does not tell you the size of the bias: simulate it in your own design before choosing an estimator', 'O demonstrație a inconsistenței nu spune cît de mare este deplasarea: simulați-o în propria configurație înainte de a alege estimatorul')])

D.frame(T('Large covariance matrices: shrinkage and DCC-NL (1/2)', 'Matrice de covarianță mari: shrinkage și DCC-NL (1/2)'), items(
    (T(r'With $N/T$ not small, the eigenvalues of a sample covariance $S$ are too dispersed', r'Cînd $N/T$ nu este mic, valorile proprii ale unei covarianțe de eșantion $S$ sînt prea dispersate'),
     [T(r'$N$: number of assets; $T$: number of observations; the largest eigenvalues are too large, the smallest too small; the inverse $S^{-1}$ amplifies the error',
        r'$N$: numărul de active; $T$: numărul de observații; cele mai mari valori proprii sînt prea mari, cele mai mici, prea mici; inversa $S^{-1}$ amplifică eroarea')]),
    (T(r'Global minimum-variance (GMV) portfolio: the weights with the smallest variance that sum to 1', r'Portofoliul de varianță minimă globală (GMV): ponderile cu cea mai mică varianță care însumează 1'
       ) + r'''
    \[ w = \frac{\Sigma^{-1}\mathbf 1}{\mathbf 1'\Sigma^{-1}\mathbf 1} \]''',
     [T(r'$\Sigma$: covariance matrix of the returns; $\mathbf 1$: vector of ones', r'$\Sigma$: matricea de covarianță a randamentelor; $\mathbf 1$: vectorul cu toate elementele egale cu 1'),
      T(r'it loads on the directions with the smallest, most underestimated eigenvalues', r'pune ponderi mari pe direcțiile cu valorile proprii cele mai mici, cel mai mult subestimate'),
      T(r'it depends only on $\Sigma$, so its realised risk measures the quality of the covariance forecast without noise from expected returns',
        r'depinde doar de $\Sigma$, deci riscul lui realizat măsoară calitatea prognozei covarianței fără zgomotul randamentelor așteptate')])), 'small')

D.frame(T('Large covariance matrices: shrinkage and DCC-NL (2/2)', 'Matrice de covarianță mari: shrinkage și DCC-NL (2/2)'), items(
    (T(r'Linear shrinkage \refLWa: a weighted average of $S$ and a scaled identity', r'Shrinkage liniar \refLWa: o medie ponderată între $S$ și o matrice identitate scalată'
       ) + r'''
    \[ \hat\Sigma = \delta\,\mu I + (1 - \delta)\,S \]''',
     [T(r'$\mu$: average eigenvalue of $S$; $\delta \in [0, 1]$: shrinkage intensity, estimated from the data (larger when $N/T$ is larger)',
        r'$\mu$: media valorilor proprii ale lui $S$; $\delta \in [0, 1]$: intensitatea shrinkage-ului, estimată din date (mai mare cînd $N/T$ este mai mare)')]),
    (T(r'Nonlinear shrinkage \refLWb: keep the eigenvectors of $S$, replace each eigenvalue $\lambda_i$ by $d(\lambda_i)$',
       r'Shrinkage neliniar \refLWb: se păstrează vectorii proprii ai lui $S$ și se înlocuiește fiecare valoare proprie $\lambda_i$ cu $d(\lambda_i)$'),
     [T(r'$d(\cdot)$: an analytical kernel formula that pulls small eigenvalues up and large ones down, by different amounts',
        r'$d(\cdot)$: o formulă analitică de tip kernel care ridică valorile proprii mici și le coboară pe cele mari, cu intensități diferite')]),
    (T(r'DCC-NL \refELW: in DCC, the target $S$ of the standardised residuals is itself a large sample covariance: replace it by its nonlinear shrinkage',
       r'DCC-NL \refELW: în DCC, ținta $S$ a reziduurilor standardizate este ea însăși o covarianță de eșantion mare: o înlocuim cu versiunea ei cu shrinkage neliniar'),
     [T('composite likelihood for $(a, b)$, univariate GARCH for the variances; evaluated by the out-of-sample s.d. of GMV portfolios', 'verosimilitate compusă pentru $(a, b)$, GARCH univariat pentru varianțe; evaluat prin abaterea standard în afara eșantionului a portofoliilor GMV')])), 'small')

chart(T('Case study: Engle, Ledoit and Wolf (2019) on US equities', 'Studiu de caz: Engle, Ledoit și Wolf (2019) pe acțiuni din SUA'), 'ats_ch8_gmv', 'ATS_ch8_mgarch', [
    T(r'@{gm.N} assets: 14 US stocks and three equity ETFs (SPY, QQQ, RSP), which are portfolios of stocks; GMV weights rebalanced every 21 days from @{gm.first} (@{gm.n} rebalancings); window @{gm.win} days, and @{gm.short} days for the last two bars; annualised out-of-sample s.d.',
      r'@{gm.N} active: 14 acțiuni din SUA și trei ETF-uri pe acțiuni (SPY, QQQ, RSP), care sînt ele însele portofolii de acțiuni; ponderi GMV rebalansate la fiecare 21 de zile din @{gm.first} (@{gm.n} rebalansări); fereastra de @{gm.win} de zile, respectiv @{gm.short} de zile pentru ultimele două bare; abaterea standard anualizată în afara eșantionului')],
    h='0.6\\textheight')

D.frame(T('Interpreting the GMV comparison (1/2)', 'Interpretarea comparației GMV (1/2)'), items(
    T(r'Out-of-sample s.d. (\% p.a.): 1/N @{gm.ew}, sample @{gm.s}, linear shrinkage @{gm.lw}, nonlinear shrinkage @{gm.nl}, DCC @{gm.dcc}, DCC-NL @{gm.dccnl}',
      r'Abaterea standard în afara eșantionului (\% anual): 1/N @{gm.ew}, eșantion @{gm.s}, shrinkage liniar @{gm.lw}, shrinkage neliniar @{gm.nl}, DCC @{gm.dcc}, DCC-NL @{gm.dccnl}'),
    (T(r'With $N/T = @{gm.N}/@{gm.win}$ the sample covariance is already accurate', r'Cu $N/T = @{gm.N}/@{gm.win}$, covarianța de eșantion este deja precisă'),
     [T(r'nonlinear shrinkage changes little (@{gm.nl} against @{gm.s}); DCC-NL is no better than DCC',
        r'shrinkage-ul neliniar schimbă puțin (@{gm.nl} față de @{gm.s}); DCC-NL nu este mai bun decît DCC')]),
    (T(r'Here the dynamics hurt: DCC gives @{gm.dcc} against @{gm.s}', r'Aici dinamica dăunează: DCC dă @{gm.dcc} față de @{gm.s}'),
     [T('DCC uses GARCH variances, with forecasts averaged over the 21-day holding period',
        'DCC folosește varianțe GARCH, cu prognoze mediate pe perioada de deținere de 21 de zile'),
      T('one-month-ahead variance forecasts of single stocks such as MSTR and TSLA are noisy, and GMV amplifies their errors',
        'prognozele de varianță pe o lună pentru acțiuni individuale precum MSTR și TSLA sînt zgomotoase, iar GMV le amplifică erorile')])), 'small')

D.frame(T('Interpreting the GMV comparison (2/2)', 'Interpretarea comparației GMV (2/2)'), items(
    (T(r'A window of @{gm.short} days makes $N/T$ five times larger', r'O fereastră de @{gm.short} de zile face $N/T$ de cinci ori mai mare'),
     [T(r's.d. of the sample GMV @{gm.s250}, with nonlinear shrinkage @{gm.nl250}: only @{gm.gain250}\% lower',
        r'abaterea standard a portofoliului GMV din eșantion este @{gm.s250}, cu shrinkage neliniar @{gm.nl250}: doar cu @{gm.gain250}\% mai mică'),
      T(r'yet the ETFs make the correlation matrix nearly singular (median condition number @{gm.cond})',
        r'deși ETF-urile fac matricea de corelație aproape singulară (numărul de condiționare median @{gm.cond})'),
      T('the shorter window itself lowers the risk: a crude form of time variation',
        'fereastra mai scurtă reduce ea însăși riscul: o formă rudimentară de variație în timp')]),
    (T('The original study uses hundreds of stocks, where $N/T$ is large', 'Studiul original folosește sute de acțiuni, unde $N/T$ este mare'),
     [T('there the DCC-NL gains are substantial', 'acolo cîștigurile DCC-NL sînt substanțiale'),
      T('with our $N$ the lesson is when shrinkage matters, not how much it gains',
        'cu $N$-ul nostru, lecția este cînd contează shrinkage-ul, nu cît cîștigă')])), 'small')

D.frame(T('Realised covariance', 'Covarianța realizată'), items(
    (T(r'The multivariate RV: the sum of outer products of the intraday return vectors', r'RV multivariat: suma produselor exterioare ale vectorilor de randamente intraday'
       ) + r'''
    \[ \mathrm{RCov}_t = \sum_{i=1}^n r_{t,i}\,r_{t,i}' \to \int_0^1\Sigma_s\,ds \]''',
     [T(r'$r_{t,i}$: $N \times 1$ vector of intraday returns; $\Sigma_s$: spot covariance matrix; the limit adds the co-jumps (simultaneous jumps); with synchronous, noise-free prices it inherits the CLT of RV',
        r'$r_{t,i}$: vectorul $N \times 1$ al randamentelor intraday; $\Sigma_s$: matricea de covarianță instantanee; la limită se adaugă salturile comune; cu prețuri sincrone și fără zgomot, moștenește TLC a lui RV')]),
    (T(r'Asynchronous trading: previous-tick prices create zero returns for the asset that has not traded; covariances shrink towards zero as the interval falls (the Epps effect)',
       r'Tranzacționarea asincronă: prețurile „previous-tick” creează randamente nule pentru activul care nu a fost tranzacționat; covarianțele se apropie de zero cînd intervalul scade (efectul Epps)'),
     [T(r'refresh-time sampling (all assets have traded) and the multivariate realised kernel \refBNHLSc: consistent and positive semi-definite',
        r'eșantionarea la timpul de reîmprospătare (toate activele au fost tranzacționate) și realised kernel-ul multivariat \refBNHLSc: consistent și pozitiv semidefinit')]),
    T(r'Forecasting: HAR on the elements of the Cholesky factor of $\mathrm{RCov}_t$ keeps forecasts positive definite \refCV; HEAVY and Realized GARCH have multivariate versions',
      r'Prognoza: HAR pe elementele factorului Cholesky al lui $\mathrm{RCov}_t$ păstrează prognozele pozitiv definite \refCV; HEAVY și Realized GARCH au versiuni multivariate'),
    (T(r'Evaluating covariance forecasts $H_t$ against a matrix proxy $\Sigma_t$: robust losses \refLRV', r'Evaluarea prognozelor de covarianță $H_t$ față de un proxy matriceal $\Sigma_t$: funcții de pierdere robuste \refLRV'),
     [T(r'matrix QLIKE $\ln|H_t| + \mathrm{tr}(H_t^{-1}\Sigma_t)$, with $|\cdot|$ the determinant and $\mathrm{tr}$ the trace; Frobenius MSE, the sum of squared element-wise errors',
        r'QLIKE matriceal $\ln|H_t| + \mathrm{tr}(H_t^{-1}\Sigma_t)$, cu $|\cdot|$ determinantul și $\mathrm{tr}$ urma; MSE Frobenius, suma pătratelor erorilor pe elemente')])), 'small')

chart(T('Bitcoin and Ether: realised and DCC correlation', 'Bitcoin și Ether: corelația realizată și corelația DCC'), 'ats_ch8_corr_crypto', 'ATS_ch8_mgarch', [
    T(r'Daily realised correlation from 5-minute returns (5-day means) and the DCC correlation of daily close-to-close (UTC) returns, 2018--2026',
      r'Corelația realizată zilnică din randamente la 5 minute (medii pe 5 zile) și corelația DCC a randamentelor zilnice închidere--închidere (UTC), 2018--2026')],
    h='0.6\\textheight')

interp(('the correlations', 'corelațiilor'), [
    T(r'Average realised correlation @{cc.rc}, average DCC correlation @{cc.dcc}; correlation between the two series @{cc.cor}',
      r'Corelația realizată medie @{cc.rc}, corelația DCC medie @{cc.dcc}; corelația dintre cele două serii @{cc.cor}'),
    T(r'DCC uses one observation a day ($\hat a = @{cc.a}$, $\hat b = @{cc.b}$): it smooths and reacts with a lag; the realised measure moves daily and drops quickly in idiosyncratic episodes (5\% quantile @{cc.q05})',
      r'DCC folosește o observație pe zi ($\hat a = @{cc.a}$, $\hat b = @{cc.b}$): netezește și reacționează cu întîrziere; măsura realizată se mișcă zilnic și scade repede în episoadele specifice unei monede (cuantila de 5\% @{cc.q05})'),
    T('Combining both (a realised measure in the correlation equation) is the multivariate analogue of Realized GARCH', 'Combinarea lor (o măsură realizată în ecuația corelației) este analogul multivariat al Realized GARCH'),
    T('Five-minute sampling sits on the flat part of the Epps curve for these two coins (signature slide): the realised correlation is not biased towards zero', 'Eșantionarea la cinci minute se află pe partea plată a curbei Epps pentru aceste două monede (slide-ul cu signature plot): corelația realizată nu este deplasată spre zero')])

D.recap(('Multivariate', 'cazul multivariat'), [
    T('BEKK guarantees positivity at a quadratic parameter cost; DCC separates variances and correlations and scales to large $N$', 'BEKK garantează pozitivitatea cu un cost pătratic în parametri; DCC separă varianțele de corelații și funcționează pentru $N$ mare'),
    T('cDCC fixes the inconsistency of the DCC target; in moderate designs the difference is small', 'cDCC corectează inconsistența țintei DCC; în configurații moderate, diferența este mică'),
    T('In high dimension, the target needs shrinkage (DCC-NL); evaluate with GMV risk or robust matrix losses', 'În dimensiune mare, ținta are nevoie de shrinkage (DCC-NL); evaluați prin riscul GMV sau prin funcții de pierdere matriceale robuste')])

# =============================================================================
# 9. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Does exploiting the measurement error of realised variance (HARQ) improve volatility forecasts robustly, or only under particular design choices?', 'Îmbunătățește exploatarea erorii de măsurare a varianței realizate (HARQ) prognozele de volatilitate în mod robust sau doar pentru anumite alegeri de specificare?'),
     [T(r'formal: the QLIKE ratio HARQ/HAR and its DM statistic across a pre-registered grid (window, filter, realised measure, asset); falsified if the ratio exceeds 1 or the DM test is insignificant for most cells',
        r'formal: raportul QLIKE HARQ/HAR și statistica DM pe o grilă preînregistrată (fereastră, filtru, măsură realizată, activ); infirmată dacă raportul depășește 1 sau testul DM este nesemnificativ în majoritatea celulelor'),
      T('the measure of precision (RQ) is itself noisy and fat-tailed, so the gain may be fragile', 'măsura preciziei (RQ) este ea însăși zgomotoasă și cu cozi groase, deci cîștigul poate fi fragil')]),
    (T('Why it matters: risk systems use one-day volatility forecasts every day; a small but robust gain is worth more than a large fragile one', 'Miza: sistemele de risc folosesc zilnic prognoze de volatilitate pe o zi; un cîștig mic, dar robust valorează mai mult decît unul mare și fragil'),
     [T(r'literature to start from: \refBPQ, \refCor, \refPat, \refHLb, \refHLN', r'literatura de pornire: \refBPQ, \refCor, \refPat, \refHLb, \refHLN')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers since 2016 that test HARQ-type models out of sample on assets other than US equities; give DOIs.} Then check every DOI on Crossref',
        r'\textbf{literatura}: \aiprompt{Listează lucrări recenzate din 2016 încoace care testează în afara eșantionului modele de tip HARQ pe alte active decît acțiunile din SUA; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Under which data features (24/7 trading, jumps, zero returns) should the HARQ gain shrink or grow? Give testable predictions.}',
        r'\textbf{ipoteza}: \aiprompt{În ce condiții ale datelor (tranzacționare 24/7, salturi, randamente nule) ar trebui să scadă sau să crească cîștigul HARQ? Dă predicții testabile.}'),
      T(r'\textbf{code and replication}: ask for HAR and HARQ rolling forecasts, then reproduce a known number first (the Bitcoin QLIKE ratio of this lecture)',
        r'\textbf{cod și replicare}: cereți prognoze HAR și HARQ pe fereastră mobilă, apoi reproduceți întîi o cifră cunoscută (raportul QLIKE pentru Bitcoin din acest curs)'),
      T(r'\textbf{robustness and critique}: \aiprompt{Act as a hostile referee: which choices in a HARQ forecast comparison could produce a spurious gain?}',
        r'\textbf{robustețe și critică}: \aiprompt{Joacă rolul unui recenzent ostil: ce alegeri dintr-o comparație a prognozelor HARQ ar putea produce un cîștig fals?}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The forecast at $t$ uses only data up to $t$: windows, demeaning of RQ, the insanity filter and the bias correction of log forecasts are all computed in the estimation window', 'Prognoza din $t$ folosește doar date pînă la $t$: ferestrele, centrarea lui RQ, filtrul de plauzibilitate și corecția deplasării prognozelor în logaritmi sînt calculate în fereastra de estimare'),
    T('The loss is robust (QLIKE, MSE) and the proxy is stated; DM statistics use HAC variances', 'Funcția de pierdere este robustă (QLIKE, MSE), iar proxy-ul este precizat; statisticile DM folosesc varianțe HAC'),
    T('All cells of the grid are reported, not the best one; the number of comparisons is stated', 'Toate celulele grilei sînt raportate, nu doar cea mai bună; numărul comparațiilor este precizat'),
    T('Realised measures are recomputed from raw prices and agree with an independent source on overlapping assets and dates', 'Măsurile realizate sînt recalculate din prețurile brute și concordă cu o sursă independentă pentru activele și datele comune')), 'small')

chart(T('Mini-case: twelve choices, one conclusion?', 'Mini studiu de caz: douăsprezece alegeri, o singură concluzie?'), 'ats_ch8_ai_case', 'ATS_ch8_ai_robustness', [
    T(r'QLIKE ratio HARQ/HAR for Bitcoin and Ether: window 500, 1\,000 or 1\,500 days; insanity filter or a floor at the smallest in-sample RV; target 5-minute RV or realised kernel',
      r'Raportul QLIKE HARQ/HAR pentru Bitcoin și Ether: fereastră de 500, 1\,000 sau 1\,500 de zile; filtrul de plauzibilitate sau o limită inferioară egală cu cel mai mic RV din eșantion; ținta RV la 5 minute sau realised kernel'),
    T(r'Ratios from @{ai.min} to @{ai.max}; HARQ better in @{ai.better}\% of the 24 cells, significantly better (DM $< -1.96$) in @{ai.sig}\%, significantly worse in @{ai.wsig}\%: an AI summary reporting one cell would hide most of this',
      r'Rapoarte între @{ai.min} și @{ai.max}; HARQ mai bun în @{ai.better}\% dintre cele 24 de celule, semnificativ mai bun (DM $< -1{,}96$) în @{ai.sig}\%, semnificativ mai slab în @{ai.wsig}\%: un rezumat AI care raportează o singură celulă ar ascunde cea mai mare parte din acest tablou')],
    h='0.6\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Realised volatility of crypto-assets: does the equity toolkit transfer?}: replicate first, then extend', r'\textbf{Volatilitatea realizată a criptoactivelor: se transferă instrumentele de la acțiuni?}: întîi replicare, apoi extindere'),
     [T(r'replicate: HAR and HARQ of this lecture for Bitcoin (QLIKE ratio @{ho.btc.harq}) and Realized GARCH for the S\&P 500 (persistence @{rg.pers})',
        r'replicați: HAR și HARQ din acest curs pentru Bitcoin (raportul QLIKE @{ho.btc.harq}) și Realized GARCH pentru S\&P 500 (persistența @{rg.pers})'),
      T(r'extend: ten coins from the Binance archive; noise-robust measures from one-second data',
        r'extindeți: zece monede din arhiva Binance; măsuri robuste la zgomot din date la o secundă'),
      T(r'extend the tests: an intraday seasonality correction before jump tests; Realized GARCH with the realised kernel',
        r'extindeți testele: o corecție a sezonalității intraday înaintea testelor de salt; Realized GARCH cu realised kernel'),
      T(r'use the spot-ETF date (January 2024) as a natural break', r'folosiți data ETF-urilor spot (ianuarie 2024) ca ruptură naturală'),
      T(r'pre-register: assets, sample, measures, models, windows, losses, the DM/MCS tests and the robustness grid',
        r'preînregistrați: activele, eșantionul, măsurile, modelele, ferestrele, funcțiile de pierdere, testele DM/MCS și grila de robustețe')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Gaussian QML needs only the variance equation; with fat tails, use sandwich standard errors', 'QML gaussian are nevoie doar de ecuația varianței; cu cozi groase, folosiți erorile standard sandwich'),
    T('Volatility has fast and slow components; macro drivers of the slow one need long samples and honest variance ratios', 'Volatilitatea are componente rapide și lente; factorii macroeconomici ai celei lente au nevoie de eșantioane lungi și de rapoarte de varianță raportate fără selecție'),
    T('Realised measures make volatility observable with a known error; noise and jumps decide the estimator', 'Măsurile realizate fac volatilitatea observabilă, cu o eroare cunoscută; zgomotul și salturile decid estimatorul'),
    T('HAR, HARQ and Realized GARCH beat return-only models one day ahead; evaluate with QLIKE or MSE', 'La un pas, HAR, HARQ și Realized GARCH depășesc modelele care folosesc doar randamentele; evaluați cu QLIKE sau MSE'),
    T('In many dimensions the correlation target needs shrinkage (DCC-NL); whether the dynamics help must be checked out of sample', 'În multe dimensiuni, ținta de corelație are nevoie de shrinkage (DCC-NL); dacă dinamica ajută trebuie verificat în afara eșantionului')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T(r'Why are Hessian standard errors too small for GARCH when $\kappa_\eta > 3$?', r'De ce sînt prea mici erorile standard din hessiană pentru GARCH cînd $\kappa_\eta > 3$?'),
        T('What does the variance ratio of GARCH-MIDAS measure?', 'Ce măsoară raportul de varianță din GARCH-MIDAS?'),
        T('Why does stable convergence matter for the CLT of RV?', 'De ce contează convergența stabilă pentru TLC a lui RV?'),
        T('Why can a signature plot rise at high frequency?', 'De ce poate crește un signature plot la frecvență înaltă?'),
        T(r'Why is $\beta_{dQ}$ expected to be negative in HARQ?', r'De ce ne așteptăm ca $\beta_{dQ}$ să fie negativ în HARQ?'),
        T('Which losses keep the ranking under a noisy proxy?', 'Ce funcții de pierdere păstrează ordinea cu un proxy zgomotos?'))),
    block(T('Next: Chapter 9', 'Urmează: Capitolul 9'), items(
        T('VaR, ES and backtesting: elicitability, scoring and model risk', 'VaR, ES și backtesting: elicitabilitate, funcții de scor și riscul de model'),
        T('From volatility forecasts to tail forecasts: VaR 1\\% and ES 2.5\\%, their scoring functions and backtests', 'De la prognozele de volatilitate la prognozele de coadă: VaR 1\\% și ES 2,5\\%, funcțiile lor de scor și backtesting-ul'))),
    '0.58', '0.38'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the GARCH sandwich', 'Anexă: sandwich-ul GARCH'), items(
    T(r'$\ell_t = -\frac12(\ln\sigma^2_t + \varepsilon^2_t/\sigma^2_t)$, $d_t = \sigma_t^{-2}\partial\sigma^2_t/\partial\theta$: $s_t = \frac12(\eta^2_t - 1)d_t$ at $\theta_0$',
      r'$\ell_t = -\frac12(\ln\sigma^2_t + \varepsilon^2_t/\sigma^2_t)$, $d_t = \sigma_t^{-2}\partial\sigma^2_t/\partial\theta$: $s_t = \frac12(\eta^2_t - 1)d_t$ în $\theta_0$'),
    T(r'$B = \E s_ts_t\' = \frac14\E(\eta^2_t - 1)^2\,\E d_td_t\' = \frac{\kappa_\eta - 1}{4}J$, because $\eta_t$ is independent of $d_t \in \mathcal F_{t-1}$',
      r'$B = \E s_ts_t\' = \frac14\E(\eta^2_t - 1)^2\,\E d_td_t\' = \frac{\kappa_\eta - 1}{4}J$, deoarece $\eta_t$ este independent de $d_t \in \mathcal F_{t-1}$'),
    T(r'$\partial s_t/\partial\theta\' = -\frac12\eta^2_td_td_t\' + \frac12(\eta^2_t - 1)\partial d_t/\partial\theta\'$; the second term has mean zero, so $A = \frac12J$',
      r'$\partial s_t/\partial\theta\' = -\frac12\eta^2_td_td_t\' + \frac12(\eta^2_t - 1)\partial d_t/\partial\theta\'$; al doilea termen are media zero, deci $A = \frac12J$'),
    T(r'$A^{-1}B\,A^{-1} = 4J^{-1}\cdot\frac{\kappa_\eta - 1}{4}J\cdot J^{-1} = (\kappa_\eta - 1)J^{-1}$; Hessian only: $A^{-1} = 2J^{-1}$; OPG: $B^{-1} = \frac{4}{\kappa_\eta - 1}J^{-1}$',
      r'$A^{-1}B\,A^{-1} = 4J^{-1}\cdot\frac{\kappa_\eta - 1}{4}J\cdot J^{-1} = (\kappa_\eta - 1)J^{-1}$; doar hessiana: $A^{-1} = 2J^{-1}$; OPG: $B^{-1} = \frac{4}{\kappa_\eta - 1}J^{-1}$')), 'small')

D.frame(T('Appendix: the noise bias of realised variance', 'Anexă: deplasarea din zgomot a varianței realizate'), items(
    T(r'$\tilde r_i = Y_{i/n} - Y_{(i-1)/n} = r_i + u_i - u_{i-1}$, with $u$ i.i.d. $(0, \omega^2)$ independent of $X$',
      r'$\tilde r_i = Y_{i/n} - Y_{(i-1)/n} = r_i + u_i - u_{i-1}$, cu $u$ i.i.d. $(0, \omega^2)$, independent de $X$'),
    T(r'$\sum_i\tilde r_i^2 = \sum_ir_i^2 + 2\sum_ir_i(u_i - u_{i-1}) + \sum_i(u_i - u_{i-1})^2$; the cross term has mean zero, the last has mean $2n\omega^2$',
      r'$\sum_i\tilde r_i^2 = \sum_ir_i^2 + 2\sum_ir_i(u_i - u_{i-1}) + \sum_i(u_i - u_{i-1})^2$; termenul mixt are media zero, ultimul are media $2n\omega^2$'),
    T(r'$\Cov(\tilde r_i, \tilde r_{i-1}) = -\omega^2$: first-order negative autocorrelation; the realised kernel adds $2\gamma_1 \approx -2n\omega^2$ back and removes the bias',
      r'$\Cov(\tilde r_i, \tilde r_{i-1}) = -\omega^2$: autocorelație negativă de ordinul întîi; realised kernel-ul adaugă $2\gamma_1 \approx -2n\omega^2$ și elimină deplasarea'),
    T(r'Positively autocorrelated returns (gradual price adjustment, stale prices) give $\gamma_1 > 0$ and a signature plot that rises with the interval; the kernel corrects both signs',
      r'Randamentele autocorelate pozitiv (ajustarea treptată a prețului, prețuri stale (neactualizate)) dau $\gamma_1 > 0$ și un signature plot care crește cu intervalul; kernel-ul corectează ambele semne')), 'small')

D.frame(T('Appendix: attenuation and HARQ', 'Anexă: atenuarea și HARQ'), items(
    T(r'$\mathrm{IV}_{t+1} = c + \phi\,\mathrm{IV}_t + v_{t+1}$, observed $\mathrm{RV}_t = \mathrm{IV}_t + e_t$, $e_t$ uncorrelated with $\mathrm{IV}_t$ and $v_{t+1}$',
      r'$\mathrm{IV}_{t+1} = c + \phi\,\mathrm{IV}_t + v_{t+1}$, observăm $\mathrm{RV}_t = \mathrm{IV}_t + e_t$, $e_t$ necorelat cu $\mathrm{IV}_t$ și $v_{t+1}$'),
    T(r'OLS of $\mathrm{RV}_{t+1}$ on $\mathrm{RV}_t$: $\mathrm{plim}\,\hat\phi = \frac{\Cov(\mathrm{IV}_{t+1}, \mathrm{IV}_t)}{\Var(\mathrm{IV}_t) + \Var(e_t)} = \phi\lambda$, $\lambda = \frac{\Var(\mathrm{IV})}{\Var(\mathrm{IV}) + \E\Var(e_t)}$',
      r'OLS pentru $\mathrm{RV}_{t+1}$ pe $\mathrm{RV}_t$: $\mathrm{plim}\,\hat\phi = \frac{\Cov(\mathrm{IV}_{t+1}, \mathrm{IV}_t)}{\Var(\mathrm{IV}_t) + \Var(e_t)} = \phi\lambda$, $\lambda = \frac{\Var(\mathrm{IV})}{\Var(\mathrm{IV}) + \E\Var(e_t)}$'),
    T(r'The best linear predictor given today\'s precision uses $\phi\lambda_t$, $\lambda_t = \frac{\Var(\mathrm{IV})}{\Var(\mathrm{IV}) + 2\mathrm{IQ}_t/n}$: decreasing in $\mathrm{IQ}_t$',
      r'Cel mai bun predictor liniar, dată precizia de azi, folosește $\phi\lambda_t$, $\lambda_t = \frac{\Var(\mathrm{IV})}{\Var(\mathrm{IV}) + 2\mathrm{IQ}_t/n}$: descrescător în $\mathrm{IQ}_t$'),
    T(r'A first-order expansion in $\sqrt{\mathrm{IQ}_t}$ gives $\beta_d + \beta_{dQ}\sqrt{\mathrm{RQ}_t}$ with $\beta_{dQ} < 0$: the HARQ specification \refBPQ',
      r'O dezvoltare de ordinul întîi în $\sqrt{\mathrm{IQ}_t}$ dă $\beta_d + \beta_{dQ}\sqrt{\mathrm{RQ}_t}$, cu $\beta_{dQ} < 0$: specificarea HARQ \refBPQ')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
