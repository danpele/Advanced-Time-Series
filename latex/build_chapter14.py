r"""
build_chapter14.py -- Capitolul 14 (Inferență cauzală pentru serii de timp), EN + RO
=====================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_14/ch14_numbers.json (generate_all_charts.py). Nicio cifră nu este
scrisă de mînă, în afara exemplelor teoretice și a valorilor publicate citate din lucrări.
Capitolul 3 a predat SVAR, proiecțiile locale și proxy-SVAR; Capitolul 6 filtrul Kalman și BSTS; Capitolul 0 HAC.
Aici: cauzalitatea Granger față de efectele cauzale (rezultate potențiale pentru serii de timp), entropia de transfer,
descoperirea cauzală (PCMCI, convergent cross mapping), serii de timp întrerupte și studii de eveniment cu erori
dependente, metoda controlului sintetic (replicarea Abadie, Diamond și Hainmueller 2015; dublura Brexit a lui Born et al.
2019), controlul sintetic augmentat, DiD sintetic, DiD eșalonat, CausalImpact (BSTS), DML, identificarea onestă;
aplicația românească: efectul încheierii plafonării prețului electricității și al majorării TVA din 2025 asupra inflației.
Ieșire:
  EN/Courses/chapter14_causal_inference_time_series.tex
  RO/Cursuri/capitol14_inferenta_cauzala_serii_timp.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_14/generate_all_charts.py
  python3 latex/build_chapter14.py && python3 latex/ats_build.py compile 14
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import run_acronyms, Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch14_common import REFS, QLURL, T, V2, day, month, quarter, bib, finalize, load, minus_fix   # noqa: E402


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
D = Deck(14, 'lecture', refs=REFS)
C = 'https://commons.wikimedia.org/wiki/File:'
P = V.put
TB = '>{\\raggedright\\arraybackslash}'


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
    'pearl': ('ch14_pearl_2013.jpg', C + 'Judea_Pearl_at_NIPS_2013_(11781981594)_(cropped).jpg',
              FOTO + ': Better Than Bacon (2013); CC BY 2.0; Wikimedia Commons'),
    'imbens': ('ch14_imbens_2022.jpg', C + 'Guido_Imbens_Lemley_Lecture_1_(cropped).jpg',
               FOTO + ': Filetime (2022); CC0; Wikimedia Commons'),
    'granger': ('ch1_granger_2008.jpg', C + 'Clive_Granger_by_Olaf_Storbeck.jpg', FOTO + ': Olaf Storbeck (2008); CC BY-SA 2.0; Wikimedia Commons'),
    'sugihara': ('ch14_sugihara_2015.jpg', C + 'Sugihara_George.png', FOTO + ': J Park (2015); CC BY-SA 4.0; Wikimedia Commons'),
    'gate': ('ch14_brandenburg_gate_1989.jpg', C + 'Bundesarchiv_Bild_183-1989-1111-009,_Berlin,_Brandenburger_Tor,_Polizeiabsperrung.jpg',
             FOTO + ': Peer Grimm, Bundesarchiv Bild 183-1989-1111-009 (1989); CC BY-SA 3.0 de; Wikimedia Commons'),
    'brexit': ('ch14_brexit_count_2016.jpg', C + 'At_the_Brexit_referendum_count_in_Borehamwood_(28176894300).jpg',
               FOTO + ': Steve Bowbrick (2016); CC BY 2.0; Wikimedia Commons'),
    'parliament': ('ch14_parliament_bucharest_2017.jpg', C + 'Palace_of_the_Parliament_in_Bucharest_(51878975552).jpg',
                   FOTO + ': William John Gauthier (2017); CC BY-SA 2.0; Wikimedia Commons'),
    'atm': ('ch14_bitcoin_atm_2016.jpg', C + 'Bitcoin_ATM_Prague.jpg', FOTO + ': Perituss (2016); CC0; Wikimedia Commons'),
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


CN = {'AT': ('Austria', 'Austria'), 'BE': ('Belgium', 'Belgia'), 'BG': ('Bulgaria', 'Bulgaria'), 'CY': ('Cyprus', 'Cipru'),
      'CZ': ('Czechia', 'Cehia'), 'DE': ('Germany', 'Germania'), 'DK': ('Denmark', 'Danemarca'), 'EE': ('Estonia', 'Estonia'),
      'EL': ('Greece', 'Grecia'), 'ES': ('Spain', 'Spania'), 'FI': ('Finland', 'Finlanda'), 'FR': ('France', 'Franța'),
      'HR': ('Croatia', 'Croația'), 'HU': ('Hungary', 'Ungaria'), 'IE': ('Ireland', 'Irlanda'), 'IT': ('Italy', 'Italia'),
      'LT': ('Lithuania', 'Lituania'), 'LU': ('Luxembourg', 'Luxemburg'), 'LV': ('Latvia', 'Letonia'), 'MT': ('Malta', 'Malta'),
      'NL': ('Netherlands', 'Țările de Jos'), 'PL': ('Poland', 'Polonia'), 'PT': ('Portugal', 'Portugalia'), 'RO': ('Romania', 'România'),
      'SE': ('Sweden', 'Suedia'), 'SI': ('Slovenia', 'Slovenia'), 'SK': ('Slovakia', 'Slovacia'),
      'USA': ('United States', 'Statele Unite'), 'JPN': ('Japan', 'Japonia'), 'CAN': ('Canada', 'Canada'), 'HUN': ('Hungary', 'Ungaria'),
      'PRT': ('Portugal', 'Portugalia'), 'IRL': ('Ireland', 'Irlanda'), 'ITA': ('Italy', 'Italia'), 'FIN': ('Finland', 'Finlanda'),
      'LUX': ('Luxembourg', 'Luxemburg'), 'DEU': ('Germany', 'Germania'), 'NZL': ('New Zealand', 'Noua Zeelandă'), 'ISL': ('Iceland', 'Islanda'),
      'FRA': ('France', 'Franța'), 'BEL': ('Belgium', 'Belgia'), 'GBR': ('United Kingdom', 'Regatul Unit'),
      'Austria': ('Austria', 'Austria'), 'Japan': ('Japan', 'Japonia'), 'Netherlands': ('Netherlands', 'Țările de Jos'),
      'Switzerland': ('Switzerland', 'Elveția'), 'Norway': ('Norway', 'Norvegia'), 'Italy': ('Italy', 'Italia'),
      'Greece': ('Greece', 'Grecia'), 'Australia': ('Australia', 'Australia'), 'New Zealand': ('New Zealand', 'Noua Zeelandă')}
CN['USA_'] = ('USA', 'SUA')


def cname(k):
    a, b = CN.get(k, (k, k))
    return V2(a, b)


def wlist(w, top=None, d=2):
    """'Austria 0.42, ...' sorted by weight."""
    ks = sorted(w, key=lambda k: -w[k])[:top]
    return '; '.join(f'{cname(k)} {n(w[k], d)}' for k in ks)


# =============================================================================
# CIFRE
# =============================================================================
o = N['overview']
V.raw('ov.hend', month(o['hicp_end']))
P('ov.ro25', o['ro_jun25'], 1)
P('ov.roaug', o['ro_aug25'], 1)
P('ov.romax', o['ro_max'], 1)
V.raw('ov.romaxd', month(o['ro_max_date']))
P('ov.rolast', o['ro_last'], 1)
P('ov.eulast', o['eu_med_last'], 1)
V.raw('ov.oecd', quarter(o['oecd_end'].replace('-', '')))

g = N['granger_sim']
V.raw('gs.reps', str(g['reps']))
for T_ in ('100', '250', '500', '1000'):
    for k, kk in (('pairwise', 'pw'), ('conditional', 'c'), ('reverse', 'r')):
        P(f'gs.{T_}.{kk}', 100 * g['res'][T_][k], 0)
g = N['granger_markets']
V.int('gm.T', g['T'])
V.raw('gm.start', day(g['start']))
V.raw('gm.end', day(g['end']))
for k in ('sp_bet', 'bet_sp', 'sp_bet_dax', 'dax_bet', 'sp_dax', 'sp_bet_cl'):
    P(f'gm.{k}.W', g[k]['W'], 1)
    pv(f'gm.{k}.p', g[k]['p'], 3)
P('gm.te', 1000 * g['sp_bet']['te'], 1)
for k in ('cc_sp1', 'cc_sp0', 'cc_dax0', 'cc_dax1'):
    P(f'gm.{k}', g[k], 2)
g = N['te']
pv('te.linp', g['lin_p'], 2)
P('te.gauss', 1000 * g['gauss_te'], 2)
P('te.xy', g['te_xy'], 3)
pv('te.pxy', g['p_xy'], 3)
P('te.yx', g['te_yx'], 3)
P('te.pyx', g['p_yx'], 2)
P('te.null', g['te_null'], 3)
P('te.pnull', g['p_null'], 2)
V.raw('te.B', str(g['B']))
V.int('te.T', g['T'])

g = N['pcmci_sim']
V.raw('ps.reps', str(g['reps']))
for sk, kk in (('N6_T500', 'lo'), ('N20_T150', 'hi')):
    for m, mm in (('pairwise correlation', 'pc'), ('full VAR', 'var'), ('PCMCI', 'pm')):
        P(f'ps.{kk}.{mm}.t', g['rates'][sk][m]['tpr'], 2)
        P(f'ps.{kk}.{mm}.f', g['rates'][sk][m]['fpr'], 3)
g = N['pcmci_vol']
V.raw('pv.T', str(g['T']))
V.raw('pv.start', day(g['start']))
V.raw('pv.end', day(g['end']))
V.raw('pv.n', str(g['n_links']))
V.raw('pv.ncorr', str(g['n_corr']))
V.raw('pv.npos', str(g['n_possible']))
g = N['ccm']
P('cc.axy0', g['a_xy'][0], 2)
P('cc.axy', g['a_xy'][-1], 2)
P('cc.ayx', g['a_yx'][-1], 2)
P('cc.bxy', min(g['b_xy'][-1], 0.999), 3)
P('cc.byx', min(g['b_yx'][-1], 0.999), 3)
V.raw('cc.L0', str(g['libs'][0]))
V.raw('cc.L1', str(g['libs'][-1]))

g = N['its']
P('its.cum', g['hac']['cum'], 1)
P('its.se', g['iid']['cum_se'], 2)
P('its.sehac', g['hac']['cum_se'], 2)
P('its.lrv', g['hac']['lrv_ratio'], 2)
P('its.jul', g['eff']['2025-07'], 2)
P('its.aug', g['eff']['2025-08'], 2)
P('its.rest', g['rest'], 2)
P('its.rho', g['rho'], 2)
V.raw('its.Tpre', str(g['T_pre']))
P('its.surge', g['surge'], 2)
ev = N['event']['events']
for i, e in enumerate(ev):
    P(f'ev{i}.car', e['car'], 1, sign=True)
    P(f'ev{i}.t', e['t_iid'], 2)
    P(f'ev{i}.th', e['t_hac'], 2)
    P(f'ev{i}.b', e['beta'], 2)

g = N['germany']
V.raw('ge.w', wlist({k: v for k, v in g['weights'].items() if v > 0.005}))
P('ge.rmspe', g['rmspe_pre'], 0)
P('ge.gap03', abs(g['gap2003']), 0)
P('ge.avg', abs(g['avg_post']), 0)
P('ge.rel', 100 * abs(g['rel_post']), 1)
P('ge.rel03', 100 * abs(g['rel2003']), 1)
pr = g['pred']
for i, k in enumerate(('gdp', 'trade', 'inf', 'ind', 'sch', 'inv')):
    for src, s_ in (('treated', 't'), ('synth', 's'), ('avg', 'a')):
        P(f'ge.{k}.{s_}', pr[src][i], 0 if k == 'gdp' else 1)
for k in ('USA', 'Austria', 'Netherlands', 'Switzerland', 'Japan'):
    P(f'ge.w.{k.lower()}', g['weights'][k], 2)
    P(f'ge.pub.{k.lower()}', g['published'][k], 2)
g = N['germany_placebo']
P('gp.p', g['p'], 3)
V.raw('gp.n', str(g['n_units']))
P('gp.r', g['ratio_wg'], 1)
V.raw('gp.second', cname(g['second']))
P('gp.r2', g['ratios'][g['second']], 1)
P('gp.rel75', 100 * g['rel75'], 1)
P('gp.rm75', g['rmspe75'], 0)
V.raw('gp.v1', ', '.join(cname(k) for k in g['v_starts']['1']['donors']))
V.raw('gp.v8', ', '.join(cname(k) for k in g['v_starts']['8']['donors']))
lo_ = g['loo_gap2003']
P('gp.loomin', min(abs(x) for x in lo_.values()), 0)
P('gp.loomax', max(abs(x) for x in lo_.values()), 0)
g = N['brexit']
V.raw('bx.w', wlist(g['weights'], top=5))
V.raw('bx.pub', wlist(g['published'], top=5))
P('bx.g18', abs(g['gap2018']), 1)
P('bx.g19', abs(g['gap2019']), 1)
P('bx.g17', g['gap2017'], 1)
P('bx.sd', g['pre_sd'], 2)
V.raw('bx.rank', str(g['rank_uk']))
V.raw('bx.n', str(g['n_units']))
P('bx.tpmin', g['tp_min'], 1)
P('bx.tpmax', g['tp_max'], 1)
V.raw('bx.ntp', str(g['n_tp']))
V.raw('bx.top', ', '.join(cname(k) for k in g['top']))

g = N['ro_sc']
V.raw('ro.npre', str(g['n_pre']))
V.raw('ro.end', month(g['end']))
for k, kk in (('SC', 'sc'), ('demeaned SC', 'dsc'), ('augmented SC', 'asc'), ('SDID', 'sdid')):
    e = g['est'][k]
    P(f'ro.{kk}', e['avg'], 2)
    P(f'ro.{kk}.aug26', e['aug26'], 2)
    P(f'ro.{kk}.aug25', e['aug25'], 2)
    P(f'ro.{kk}.jul25', e['jul25'], 2)
    if e['rmspe_pre'] is not None:
        P(f'ro.{kk}.rm', e['rmspe_pre'], 2)
V.raw('ro.sc.w', wlist(g['est']['SC']['weights']))
V.raw('ro.dsc.w', wlist(g['est']['demeaned SC']['weights'], top=4))
V.raw('ro.asc.neg', str(sum(1 for v in g['est']['augmented SC']['weights'].values() if v < 0)))
P('ro.sdse', g['sdid_se'], 2)
_three = [g['est'][k]['avg'] for k in ('demeaned SC', 'augmented SC', 'SDID')]
P('ro.lo', min(_three), 1)
P('ro.hi', max(_three), 1)
P('ro.zeta', g['zeta'], 2)
V.raw('ro.lam', str(g['lambda']))
g = N['ro_placebo']
P('rp.p', g['p'], 3)
V.raw('rp.n', str(g['n']))
P('rp.r', g['ratio_ro'], 1)
V.raw('rp.second', cname(g['second']))
P('rp.r2', g['ratio_second'], 1)
g = N['ro_tax']
P('rt.tot', g['avg_total'], 2)
P('rt.ct', g['avg_ct'], 2)
P('rt.tax', g['avg_tax'], 2)
P('rt.aug', g['tax_aug25'], 2)
P('rt.ctjul', g['ct_jul25'], 2)
P('rt.share', 100 * g['avg_tax'] / g['avg_total'], 0)

g = N['staggered']
P('sg.tw', g['twfe_static'], 2)
P('sg.cs', g['cs_all'], 2)
P('sg.true', g['true_att'], 2)
P('sg.tw8', g['tw_8'], 2)
P('sg.cs8', g['cs_8'], 2)
P('sg.true8', g['true_8'], 2)

g = N['btc']
P('bt.avg', g['avg'], 2)
P('bt.lo', g['avg_lo'], 2)
P('bt.hi', g['avg_hi'], 2)
P('bt.p', g['p'], 2)
P('bt.pct', g['pct'], 0)
V.raw('bt.npre', str(g['n_pre']))
V.raw('bt.npost', str(g['n_post']))
P('bt.eth', g['eth_avg'], 2)
P('bt.ethlo', g['eth_lo'], 2)
P('bt.ethhi', g['eth_hi'], 2)
P('bt.ant', g['ant_avg'], 2)
P('bt.antlo', g['ant_lo'], 2)
P('bt.anthi', g['ant_hi'], 2)
P('bt.s2l', g['params']['sigma2.level'], 3)
P('bt.s2e', g['params']['sigma2.irregular'], 2)
V.raw('bt.draws', str(g['draws']))
g = N['btc_placebo']
V.raw('bp.n', str(g['n']))
V.raw('bp.ex', str(g['n_excl0']))
V.raw('bp.verb_en', 'excludes' if g['n_excl0'] == 1 else 'exclude')
V.raw('bp.verb_ro', 'exclude' if g['n_excl0'] == 1 else 'exclud')
P('bp.sd', g['sd_placebo'], 2)
g = N['dml']
P('dml.ols', g['mean']['OLS with linear controls'], 2)
P('dml.dml', g['mean']['DML, random forest, blocked folds'], 2)
P('dml.sd', g['sd']['DML, random forest, blocked folds'], 2)
P('dml.cov', 100 * g['cover'], 0)
V.raw('dml.reps', str(g['reps']))
V.int('dml.T', g['T'])
g = N['ai']
V.raw('ai.n', str(g['n']))
P('ai.min', g['min_noSC'], 2)
P('ai.max', g['max_noSC'], 2)
P('ai.med', g['med_noSC'], 2)
P('ai.sc', g['by_method']['SC'], 2)
V.raw('ai.neg', str(g['n_neg']))
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: when does a time-series analysis tell us what \textit{would have happened} without a shock or a policy, and how sure can we be?',
       r'\textbf{Întrebarea}: cînd ne spune o analiză de serii de timp \textit{ce s-ar fi întîmplat} fără un șoc sau fără o politică și cît de siguri putem fi?'),
     [T('prediction is not intervention: a variable can forecast another without causing it', 'predicția nu este intervenție: o variabilă o poate prognoza pe alta fără să o cauzeze')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('Granger causality, potential outcomes for time series, transfer entropy', 'cauzalitatea Granger, rezultate potențiale pentru serii de timp, entropia de transfer'),
      T('causal discovery: PCMCI and convergent cross mapping, with their limits', 'descoperirea relațiilor cauzale: PCMCI și convergent cross mapping, cu limitele lor'),
      T('interrupted time series and event studies with dependent errors', 'serii de timp întrerupte și studii de eveniment cu erori dependente'),
      T('synthetic control and its successors; staggered DiD; CausalImpact; DML', 'controlul sintetic și succesorii lui; DiD eșalonat; CausalImpact; DML')]),
    T(r'Prerequisites: Seminar 14 and the slide \hyperlink{c14known}{\textcolor{MainBlue}{Known from TSA and Chapter 3, and new here}}',
      r'Cunoștințe necesare: Seminarul 14 și slide-ul \hyperlink{c14known}{\textcolor{MainBlue}{Cunoscut din TSA și din Capitolul 3 și elemente noi}}')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Distinguish Granger causality from a dynamic causal effect, and state the conditions under which a time-series estimand has a causal meaning',
      'Distingeți cauzalitatea Granger de un efect cauzal dinamic și enunțați condițiile în care o mărime estimată din serii de timp are sens cauzal'),
    T('Run conditional Granger tests with HAC covariance, estimate transfer entropy, and read the output of PCMCI and convergent cross mapping critically',
      'Aplicați teste Granger condiționate cu covarianță HAC, estimați entropia de transfer și citiți critic rezultatele PCMCI și convergent cross mapping'),
    T('Estimate interrupted-time-series and event-study effects with standard errors that respect serial dependence',
      'Estimați efecte din serii de timp întrerupte și din studii de eveniment cu erori standard care respectă dependența serială'),
    T('Build synthetic controls (classic, demeaned, augmented, synthetic DiD), run placebo inference, and replicate a published result',
      'Construiți controale sintetice (clasic, cu termen liber, augmentat, DiD sintetic), aplicați inferența prin placebo și replicați un rezultat publicat'),
    T('Use CausalImpact-type state space counterfactuals and judge the identifying assumptions of every method honestly',
      'Folosiți contrafactuale în spațiul stărilor de tip CausalImpact și judecați onest ipotezele de identificare ale fiecărei metode')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Causality and time series: \refGra; \refSims; \refRS; \refBoS; \refAJK; \refSW', r'Cauzalitate și serii de timp: \refGra; \refSims; \refRS; \refBoS; \refAJK; \refSW'),
     [T(r'discovery: \refSch; \refPCMCI; \refRunE; \refSug', r'descoperire: \refSch; \refPCMCI; \refRunE; \refSug')]),
    (T('Policy evaluation', 'Evaluarea politicilor'),
     [T(r'synthetic control: \refADHa; \refADHb; \refAba; \refASCM; \refSDID', r'control sintetic: \refADHa; \refADHb; \refAba; \refASCM; \refSDID'),
      T(r'staggered DiD and CausalImpact: \refCSA; \refCI; survey \refAI', r'DiD eșalonat și CausalImpact: \refCSA; \refCI; sinteza \refAI')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_14}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_14}'),
     [T(r'\texttt{numpy}, \texttt{scipy} (synthetic control weights by quadratic programming) and \texttt{statsmodels} (state space); every estimator written out, no black box',
        r'\texttt{numpy}, \texttt{scipy} (ponderile controlului sintetic prin programare pătratică) și \texttt{statsmodels} (spațiul stărilor); fiecare estimator este scris explicit, fără cutii negre')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter14_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter14_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{3.3cm}' + TB + 'p{5.6cm}' + TB + 'p{3.4cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source, sample}', r'\textbf{Sursa, eșantionul}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizarea}'),
    [T('HICP inflation, 27 EU countries; HICP at constant tax rates', 'Inflația IAPC, 27 de țări UE; IAPC la cote de taxare constante') + r' & \refEuroH, \refEuroCT: ' + T(r'monthly, 2015 -- @{ov.hend}', r'lunar, 2015 -- @{ov.hend}') + ' & ' + T('ITS, synthetic control for Romania', 'ITS, control sintetic pentru România'),
     T('GDP per capita, West Germany and 16 OECD countries', 'PIB pe locuitor, Germania de Vest și 16 țări OCDE') + r' & \refADHd: 1960--2003 & ' + T('replication of ADH (2015)', 'replicarea ADH (2015)'),
     T('Real GDP, UK and 23 OECD countries', 'PIB real, Regatul Unit și 23 de țări OCDE') + r' & \refOECD: ' + T(r'quarterly, 1995--2019', r'trimestrial, 1995--2019') + ' & ' + T('Brexit doppelganger', 'dublura Brexit'),
     T('Daily index and crypto prices; EUR/RON', 'Prețuri zilnice ale indicilor și criptoactivelor; EUR/RON') + ' & ' + T('EODHD; BNR reference rate; to 18 September 2026', 'EODHD; cursul de referință BNR; pînă la 18 septembrie 2026') + ' & ' + T('Granger, PCMCI, event study, CausalImpact', 'Granger, PCMCI, studiu de eveniment, CausalImpact')],
    size='scriptsize'), 'footnotesize')

D.frame(T('Two languages of causality', 'Două limbaje ale cauzalității'), cols(
    ph('pearl', T('Judea Pearl, Turing Award 2011', 'Judea Pearl, Premiul Turing 2011'), h='0.28\\textheight') + '\\\\[1mm]' +
    ph('imbens', T('Guido Imbens, Nobel Prize in Economics 2021', 'Guido Imbens, Premiul Nobel pentru economie 2021'), h='0.20\\textheight'),
    items((T(r'\textbf{Structural causal models} \refPea', r'\textbf{Modele cauzale structurale} \refPea'),
           [T(r'graphs and the $do(\cdot)$ operator: $do(X = x)$ sets $X$ by intervention instead of observing it', r'grafuri și operatorul $do(\cdot)$: $do(X = x)$ fixează $X$ prin intervenție, în loc să îl observe'),
            T('conditions under which a causal effect is identified from observational data', 'condiții în care un efect cauzal este identificat din date observaționale')]),
          (T(r'\textbf{Potential outcomes} \refRub, \refIR', r'\textbf{Rezultate potențiale} \refRub, \refIR'),
           [T(r'$Y(1)$, $Y(0)$: the outcomes of one unit with and without treatment; only one of them is observed', r'$Y(1)$, $Y(0)$: rezultatele unei unități cu și fără tratament; doar unul dintre ele este observat'),
            T('assignment mechanisms; design before analysis', 'mecanisme de alocare; designul înaintea analizei')]),
          (T(r'\textbf{Time series} add order, dependence and a single realisation', r'\textbf{Seriile de timp} adaugă ordinea, dependența și o singură realizare'),
           [T('one country, one history, one treatment path', 'o țară, o istorie, un singur drum al tratamentului'),
            T('Granger and PCMCI speak the graph language; synthetic control, DiD and CausalImpact speak potential outcomes', 'Granger și PCMCI vorbesc limbajul grafurilor; controlul sintetic, DiD și CausalImpact vorbesc limbajul rezultatelor potențiale')])), '0.36', '0.62'), 'small')

chart(T('Four case studies', 'Patru studii de caz'), 'ats_ch14_overview', 'ATS_ch14_romania', [
    T(r'Romanian inflation against 26 EU countries; West Germany against the OECD sample; UK real GDP against 23 OECD countries; Bitcoin realised variance around the spot ETF approval',
      r'Inflația României față de 26 de țări UE; Germania de Vest față de eșantionul OCDE; PIB-ul real al Regatului Unit față de 23 de țări OCDE; varianța realizată a Bitcoin în jurul aprobării ETF-urilor spot')], h='0.66\\textheight')

interp(('the four case studies', 'celor patru studii de caz'), [
    T(r'Romania: annual HICP inflation @{ov.ro25}\% in June 2025, @{ov.roaug}\% in August 2025, peak @{ov.romax}\% in @{ov.romaxd}; @{ov.rolast}\% in @{ov.hend} (EU median @{ov.eulast}\%)',
      r'România: inflația IAPC anuală @{ov.ro25}\% în iunie 2025, @{ov.roaug}\% în august 2025, maximum @{ov.romax}\% în @{ov.romaxd}; @{ov.rolast}\% în @{ov.hend} (mediana UE @{ov.eulast}\%)'),
    T('Each case has one treated unit and a pool of untreated units or controls observed over a long pre-period: the comparative-case-study design', 'Fiecare caz are o singură unitate tratată și un grup de unități netratate sau de serii de control observate pe o perioadă lungă înainte: designul studiului de caz comparativ'),
    T('Romania is outside the range of the donors before the treatment (the highest inflation in the EU): a warning for every method that interpolates', 'România se află în afara intervalului donatorilor înaintea tratamentului (cea mai mare inflație din UE): un avertisment pentru orice metodă care interpolează'),
    T('Bitcoin volatility is noisy and the controls are weak: the setting where an honest analysis may find nothing', 'Volatilitatea Bitcoin este zgomotoasă, iar seriile de control sînt slabe: cadrul în care o analiză onestă poate să nu găsească nimic')])

# =============================================================================
# 1. GRANGER ȘI EFECTE CAUZALE
# =============================================================================
D.section('Granger causality and causal effects', 'Cauzalitatea Granger și efectele cauzale')

D.frame(T('Known from TSA and Chapter 3, and new here', 'Cunoscut din TSA și din Capitolul 3 și elemente noi'), items(
    (T(r'\hypertarget{c14known}{}Known: the bivariate Granger test in a VAR (TSA, Chapter 6); SVAR identification, local projections and proxy SVAR (Chapter 3); HAC (Chapter 0); Kalman filter and BSTS (Chapter 6)',
       r'\hypertarget{c14known}{}Cunoscut: testul Granger bivariat într-un VAR (TSA, Capitolul 6); identificarea SVAR, proiecțiile locale și proxy SVAR (Capitolul 3); HAC (Capitolul 0); filtrul Kalman și BSTS (Capitolul 6)'), []),
    (T('New: what these tools can and cannot say about interventions', 'Nou: ce pot și ce nu pot spune aceste instrumente despre intervenții'),
     [T('potential outcomes for time series; non-anticipation; when an impulse response is a causal effect', 'rezultate potențiale pentru serii de timp; non-anticipare; cînd un răspuns la impuls este un efect cauzal'),
      T('nonlinear and graph-based discovery; comparative case studies with one treated unit', 'descoperire neliniară și pe grafuri; studii de caz comparative cu o singură unitate tratată')]),
    T('Replications: Abadie, Diamond and Hainmueller (2015, Table 1, Figures 2--5); Born et al.\\ (2019, Table 2, Figure 2); Sugihara et al.\\ (2012, Figure 3)',
      'Replicări: Abadie, Diamond și Hainmueller (2015, tabelul 1, figurile 2--5); Born et al.\\ (2019, tabelul 2, figura 2); Sugihara et al.\\ (2012, figura 3)')), 'small')

D.frame(T('Granger causality: the definition (1/2)', 'Cauzalitatea Granger: definiția (1/2)'), items(
    (T(r'\refGra: $x$ \textbf{Granger-causes} $y$ if the past of $x$ lowers the mean squared error of the best one-step forecast of $y$',
       r'\refGra: $x$ \textbf{cauzează în sens Granger} pe $y$ dacă trecutul lui $x$ reduce eroarea pătratică medie a celei mai bune prognoze la un pas a lui $y$'),
     [r'\[ \E\big[(y_{t+1} - \E[y_{t+1}\mid \mathcal I_t])^2\big] < \E\big[(y_{t+1} - \E[y_{t+1}\mid \mathcal I_t\setminus x])^2\big] \]',
      T(r'$\mathcal I_t$: all the information available up to $t$; $\mathcal I_t\setminus x$: the same information without the past of $x$', r'$\mathcal I_t$: toată informația disponibilă pînă la $t$; $\mathcal I_t\setminus x$: aceeași informație, fără trecutul lui $x$'),
      T(r'$\E[y_{t+1}\mid\cdot]$: the conditional mean, i.e.\ the best forecast in mean squared error', r'$\E[y_{t+1}\mid\cdot]$: media condiționată, adică cea mai bună prognoză în sensul erorii pătratice medii')]),
    (T(r'In practice $\mathcal I_t$ is a finite set of lags in a regression', r'În practică, $\mathcal I_t$ este o mulțime finită de laguri dintr-o regresie'),
     [r'\[ y_t = c + \sum_{j=1}^p a_jy_{t-j} + \sum_{j=1}^p b_jx_{t-j} + \sum_{j=1}^p \gamma_j\'z_{t-j} + u_t \]',
      T(r'$p$: the number of lags; $a_j$, $b_j$: coefficients on the lags of $y$ and of $x$; $z_t$: a vector of other conditioning series, with coefficient vectors $\gamma_j$; $u_t$: the error',
        r'$p$: numărul de laguri; $a_j$, $b_j$: coeficienții lagurilor lui $y$ și ale lui $x$; $z_t$: un vector de alte serii de condiționare, cu vectorii de coeficienți $\gamma_j$; $u_t$: eroarea'),
      T(r'null hypothesis of Granger non-causality: $H_0$: $b_1 = \dots = b_p = 0$', r'ipoteza nulă de non-cauzalitate Granger: $H_0$: $b_1 = \dots = b_p = 0$')])), 'small')

D.frame(T('Granger causality: the definition (2/2)', 'Cauzalitatea Granger: definiția (2/2)'), items(
    (T(r'\textbf{Wald statistic}: a quadratic form of the estimated lag coefficients of $x$', r'\textbf{Statistica Wald}: o formă pătratică a coeficienților estimați ai lagurilor lui $x$'),
     [r'\[ W = \hat b\'\hat V_b^{-1}\hat b \;\to\; \chi^2_p \quad \text{' + T('under', 'sub') + r'} \ H_0 \]',
      T(r'$\hat b = (\hat b_1, \dots, \hat b_p)\'$; $\hat V_b$: its estimated covariance matrix; reject $H_0$ for a large $W$ (small p-value)', r'$\hat b = (\hat b_1, \dots, \hat b_p)\'$; $\hat V_b$: matricea ei de covarianță estimată; $H_0$ se respinge pentru un $W$ mare (p-value mic)'),
      T(r'$\hat V_b$ HAC (Chapter 0) when $u_t$ is heteroskedastic, as for returns \refNW', r'$\hat V_b$ HAC (Capitolul 0) cînd $u_t$ este heteroscedastic, ca pentru randamente \refNW')]),
    (T(r'Integrated or cointegrated series \refTY', r'Serii integrate sau cointegrate \refTY'),
     [T(r'add as many extra lags as the maximal order of integration and test only the first $p$ lags', r'se adaugă atîtea laguri suplimentare cît este ordinul maxim de integrare și se testează doar primele $p$ laguri')]),
    (T(r'\textbf{Strength}: the Geweke measure \refGew, decomposable by frequency \refBrC (Chapter 11)', r'\textbf{Intensitatea}: măsura Geweke \refGew, care se poate descompune pe frecvențe \refBrC (Capitolul 11)'),
     [r'\[ F_{x\to y} = \ln\big(\sigma^2_{\mathrm{' + T('restricted', 'restrîns') + r'}}/\sigma^2_{\mathrm{' + T('full', 'complet') + r'}}\big) \]',
      T(r'$\sigma^2_{\mathrm{restricted}}$, $\sigma^2_{\mathrm{full}}$: residual variances of the regression without and with the lags of $x$; $F_{x\to y} \ge 0$, and 0 means no Granger causality',
        r'$\sigma^2_{\mathrm{restrîns}}$, $\sigma^2_{\mathrm{complet}}$: varianțele reziduale ale regresiei fără și cu lagurile lui $x$; $F_{x\to y} \ge 0$, iar 0 înseamnă absența cauzalității Granger')])), 'small')

D.frame(T('Granger causality is about prediction', 'Cauzalitatea Granger privește predicția'), two(
    ph('granger', T('Clive Granger, Nobel Prize in Economics 2003', 'Clive Granger, Premiul Nobel pentru economie 2003'), h='0.44\\textheight'),
    items((T(r'Four ways in which $x$ Granger-causes $y$ without causing it', r'Patru moduri în care $x$ cauzează în sens Granger pe $y$ fără să îl cauzeze'),
           [T(r'\textbf{common driver} $z$, omitted, reaching $x$ and $y$ at different lags', r'\textbf{un factor comun} $z$, omis, care ajunge la $x$ și la $y$ cu laguri diferite'),
            T(r'\textbf{expectations}: asset prices move before the events they anticipate (stock prices ``cause\'\' GDP; \refSims)', r'\textbf{anticipări}: prețurile activelor se mișcă înaintea evenimentelor anticipate (acțiunile „cauzează” PIB-ul; \refSims)'),
            T(r'\textbf{timing}: different closing hours, aggregation and sampling turn instantaneous links into lagged ones', r'\textbf{momentul observării}: ore de închidere diferite, agregarea și eșantionarea transformă legături instantanee în legături cu lag'),
            T(r'\textbf{measurement error} in $y$ that $x$ helps to filter', r'\textbf{erori de măsurare} în $y$, pe care $x$ ajută să le filtreze')]),
          (T('And the reverse: a true effect can be invisible to the test', 'Și invers: un efect real poate fi invizibil pentru test'),
           [T('nonlinear, contemporaneous, or offset by policy feedback', 'neliniar, contemporan sau compensat de reacția politicii')])), '0.36', '0.62'), 'small')

chart(T('A common driver creates Granger causality', 'Un factor comun creează cauzalitate Granger'), 'ats_ch14_granger_sim', 'ATS_ch14_granger', [
    T(r'Simulated system: a driver $w_t = 0.9w_{t-1} + \eta_t$ (AR(1), $\phi = 0.9$); $x_t = w_{t-1} + e_t$, $y_t = w_{t-3} + u_t$; $\eta_t, e_t, u_t$: independent noise',
      r'Sistem simulat: un factor $w_t = 0{,}9w_{t-1} + \eta_t$ (AR(1), $\phi = 0{,}9$); $x_t = w_{t-1} + e_t$, $y_t = w_{t-3} + u_t$; $\eta_t, e_t, u_t$: zgomot independent'),
    T(r'$x$ has no effect on $y$; tests with $p = 2$ lags (pairwise) and $p = 4$ (conditional on $w$), @{gs.reps} replications', r'$x$ nu are niciun efect asupra lui $y$; teste cu $p = 2$ laguri (pe perechi) și $p = 4$ (condiționat de $w$), @{gs.reps} de repetări')], h='0.59\\textheight')

interp(('the common-driver experiment', 'experimentului cu factor comun'), [
    T(r'Pairwise, $x$ ``Granger-causes\'\' $y$ in @{gs.100.pw}\% of the samples already at $T = 100$: $x$ carries news about $w$ two periods before $y$ does', r'Pe perechi, $x$ „cauzează în sens Granger” pe $y$ în @{gs.100.pw}\% din eșantioane încă de la $T = 100$: $x$ aduce informație despre $w$ cu două perioade înaintea lui $y$'),
    T(r'Conditional on the driver the rejection rate falls to the nominal level (@{gs.1000.c}\% at $T = 1000$): Granger causality is relative to the information set', r'Condiționat de factorul comun, rata de respingere scade la nivelul nominal (@{gs.1000.c}\% la $T = 1000$): cauzalitatea Granger este relativă la mulțimea de informație'),
    T(r'The reverse test also rejects more and more (@{gs.100.r}\% at $T = 100$, @{gs.1000.r}\% at $T = 1000$): the past of $y$ is informative about the persistent driver as well', r'Testul invers respinge și el tot mai des (@{gs.100.r}\% la $T = 100$, @{gs.1000.r}\% la $T = 1000$): trecutul lui $y$ este și el informativ despre factorul persistent'),
    T('Larger samples make a spurious finding more certain, not less: power is not validity', 'Eșantioanele mai mari fac o concluzie falsă mai sigură, nu mai puțin sigură: puterea nu înseamnă validitate')])

chart(T('Lead and lag between New York, Frankfurt and Bucharest', 'Relații lead--lag între New York, Frankfurt și București'), 'ats_ch14_granger_markets', 'ATS_ch14_granger', [
    T(r'Daily log returns, common trading days @{gm.start} -- @{gm.end} ($T = @{gm.T}$); correlation of the BET at $t$ with the S\&P 500 and the DAX at $t - k$',
      r'Randamente logaritmice zilnice, zile comune de tranzacționare @{gm.start} -- @{gm.end} ($T = @{gm.T}$); corelația BET la $t$ cu S\&P 500 și DAX la $t - k$')], h='0.65\\textheight')

D.frame(T('Granger tests on the three indices', 'Teste Granger pe cei trei indici'), table(
    'lccc', T(r'\textbf{Hypothesis} ($p = 2$) & \textbf{Wald (HAC)} & $p$\textbf{-value} & \textbf{conditioning}', r'\textbf{Ipoteza} ($p = 2$) & \textbf{Wald (HAC)} & \textbf{p-value} & \textbf{condiționare}'),
    [T('S\\&P 500 $\\not\\to$ BET', 'S\\&P 500 $\\not\\to$ BET') + ' & @{gm.sp_bet.W} & @{gm.sp_bet.p} & --',
     T('BET $\\not\\to$ S\\&P 500', 'BET $\\not\\to$ S\\&P 500') + ' & @{gm.bet_sp.W} & @{gm.bet_sp.p} & --',
     T('S\\&P 500 $\\not\\to$ BET', 'S\\&P 500 $\\not\\to$ BET') + ' & @{gm.sp_bet_dax.W} & @{gm.sp_bet_dax.p} & DAX',
     T('DAX $\\not\\to$ BET', 'DAX $\\not\\to$ BET') + ' & @{gm.dax_bet.W} & @{gm.dax_bet.p} & --',
     T('S\\&P 500 $\\not\\to$ DAX', 'S\\&P 500 $\\not\\to$ DAX') + ' & @{gm.sp_dax.W} & @{gm.sp_dax.p} & --'],
    size='footnotesize') + items(
    T(r'The classical (non-HAC) Wald for S\&P 500 $\to$ BET is @{gm.sp_bet_cl.W}: ignoring heteroskedasticity would artificially double the evidence', r'Statistica Wald clasică (fără HAC) pentru S\&P 500 $\to$ BET este @{gm.sp_bet_cl.W}: ignorarea heteroscedasticității ar dubla în mod artificial dovezile'),
    T(r'Interpretation: New York closes after Bucharest and Frankfurt; the lag-1 correlation (@{gm.cc_sp1}) is news that arrives after the Bucharest close, not an effect of US prices on Romanian firms', r'Interpretare: New York se închide după București și Frankfurt; corelația la lagul 1 (@{gm.cc_sp1}) este informație sosită după închiderea Bucureștiului, nu un efect al prețurilor americane asupra firmelor românești'),
    T(r'The DAX, which closes with Bucharest, shows contemporaneous correlation (@{gm.cc_dax0}) and no lagged effect: timing creates the Granger result', r'DAX, care se închide odată cu Bucureștiul, are corelație contemporană (@{gm.cc_dax0}) și niciun efect cu lag: momentul observării creează rezultatul Granger')), 'small')

D.frame(T('Potential outcomes for time series (1/2)', 'Rezultate potențiale pentru serii de timp (1/2)'), items(
    (T(r'\textbf{Assignment path}: the sequence of treatments (or shocks) $w_{1:T} = (w_1, \dots, w_T)$ \refRS, \refBoS', r'\textbf{Traiectoria tratamentului}: șirul tratamentelor (sau al șocurilor) $w_{1:T} = (w_1, \dots, w_T)$ \refRS, \refBoS'),
     [T(r'$w_t$: the treatment at $t$, binary (policy on or off) or continuous (the size of a shock)', r'$w_t$: tratamentul la $t$, binar (politica aplicată sau nu) sau continuu (mărimea unui șoc)')]),
    (T(r'\textbf{Potential outcome} $Y_t(w_{1:T})$: the value $Y_t$ would take if the treatment path were $w_{1:T}$', r'\textbf{Rezultatul potențial} $Y_t(w_{1:T})$: valoarea pe care ar avea-o $Y_t$ dacă traiectoria tratamentului ar fi $w_{1:T}$'),
     [T('only the potential outcome of the path that actually happened is observed', 'se observă doar rezultatul potențial al traiectoriei care a avut loc efectiv')]),
    (T(r'\textbf{Non-anticipation}: the outcome today depends only on treatments up to today', r'\textbf{Non-anticiparea}: rezultatul de azi depinde doar de tratamentele de pînă azi'),
     [r'\[ Y_t(w_{1:T}) = Y_t(w_{1:t}) \]',
      T('announcements violate it, unless the announcement itself is defined as the treatment', 'anunțurile o încalcă, dacă anunțul însuși nu este definit ca tratament')])), 'small')

D.frame(T('Potential outcomes for time series (2/2)', 'Rezultate potențiale pentru serii de timp (2/2)'), items(
    (T(r'\textbf{Dynamic causal effect} at horizon $h$: the change in $Y_{t+h}$ when only the treatment at $t$ changes from $w\'$ to $w$',
       r'\textbf{Efectul cauzal dinamic} la orizontul $h$: modificarea lui $Y_{t+h}$ cînd se schimbă doar tratamentul de la $t$, din $w\'$ în $w$'),
     [r'\[ \tau_{t,h} = Y_{t+h}(w_{1:t-1}, w, w_{t+1:t+h}) - Y_{t+h}(w_{1:t-1}, w\', w_{t+1:t+h}) \]',
      T(r'the past treatments $w_{1:t-1}$ and the later ones $w_{t+1:t+h}$ are kept fixed', r'tratamentele anterioare $w_{1:t-1}$ și cele ulterioare $w_{t+1:t+h}$ sînt menținute fixe'),
      T('one history is observed: only averages over time (or over units) of $\\tau_{t,h}$ are estimable', 'se observă o singură istorie: doar mediile în timp (sau pe unități) ale lui $\\tau_{t,h}$ sînt estimabile')]),
    (T(r'\refRS: suppose $w_t$ is \textbf{sequentially as good as random}, i.e.\ independent of the potential outcomes given the past', r'\refRS: presupunem că $w_t$ este \textbf{secvențial la fel de bun ca aleator}, adică independent de rezultatele potențiale, condiționat de trecut'),
     [T(r'then the impulse response and the local projection coefficient are weighted averages of $\tau_{t,h}$, without assuming linearity', r'atunci răspunsul la impuls și coeficientul proiecției locale sînt medii ponderate ale lui $\tau_{t,h}$, fără a presupune liniaritatea')]),
    T('The hard part is never the regression; it is the claim that the shock is unpredictable from the potential outcomes', 'Partea dificilă nu este niciodată regresia, ci afirmația că șocul nu poate fi prezis din rezultatele potențiale')), 'small')

D.frame(T('Identifying dynamic causal effects in macroeconomics', 'Identificarea efectelor cauzale dinamice în macroeconomie'), items(
    (T(r'\textbf{Narrative and high-frequency shocks} as instruments: local projections \refJor and proxy SVAR \refSW (Chapter 3)', r'\textbf{Șocuri narative și de înaltă frecvență} ca instrumente: proiecții locale \refJor și proxy SVAR \refSW (Capitolul 3)'),
     [T(r'the instrument must be relevant, contemporaneously exogenous and uncorrelated with leads and lags of the other shocks \refSW', r'instrumentul trebuie să fie relevant, exogen contemporan și necorelat cu valorile anterioare și viitoare ale celorlalte șocuri \refSW')]),
    (T(r'\textbf{Propensity scores for policy}: \refAJK model the Fed\'s decision given the forecasts it saw, and reweight outcomes (inverse probability weighting)', r'\textbf{Scoruri de propensitate pentru politică}: \refAJK modelează decizia Fed pe baza prognozelor pe care le avea și reponderează rezultatele (ponderare prin inversul probabilității)'),
     [T('identification by selection on observables: the Fed\'s information set is observed through the Greenbook', 'identificare prin selecție pe variabile observate: mulțimea de informație a Fed este observată prin Greenbook')]),
    (T(r'\textbf{Time-series experiments}: \refBoS give exact randomisation tests for one unit treated at random times (trading experiments)', r'\textbf{Experimente pe serii de timp}: \refBoS dau teste exacte de randomizare pentru o unitate tratată la momente aleatoare (experimente de tranzacționare)'), []),
    T(r'Local projections and VARs estimate the same population responses \refPMW: the choice is about bias and variance, not identification', r'Proiecțiile locale și VAR estimează aceleași răspunsuri în populație \refPMW: alegerea privește deplasarea și varianța, nu identificarea')), 'small')

D.frame(T('Transfer entropy (1/2)', 'Entropia de transfer (1/2)'), items(
    (T(r'\refSch: the information that the past of $x$ adds about $y_t$, beyond the past of $y$', r'\refSch: informația pe care trecutul lui $x$ o adaugă despre $y_t$, dincolo de trecutul lui $y$'),
     [r'\[ TE_{x\to y} = I\big(y_t;\, x_{t-1}^{(l)} \mid y_{t-1}^{(k)}\big) = \E\Big[\ln\dfrac{p(y_t\mid y^{(k)}_{t-1}, x^{(l)}_{t-1})}{p(y_t\mid y^{(k)}_{t-1})}\Big] \ge 0 \]']),
    (T('Notation', 'Notațiile'),
     [T(r'$y^{(k)}_{t-1} = (y_{t-1}, \dots, y_{t-k})$: the last $k$ values of $y$; $x^{(l)}_{t-1}$: the last $l$ values of $x$', r'$y^{(k)}_{t-1} = (y_{t-1}, \dots, y_{t-k})$: ultimele $k$ valori ale lui $y$; $x^{(l)}_{t-1}$: ultimele $l$ valori ale lui $x$'),
      T(r'$p(\cdot\mid\cdot)$: a conditional density; $I(A; B\mid C)$: the conditional mutual information of $A$ and $B$ given $C$, in nats (natural logarithm)', r'$p(\cdot\mid\cdot)$: o densitate condiționată; $I(A; B\mid C)$: informația mutuală condiționată a lui $A$ și $B$, dat $C$, în nats (logaritm natural)')]),
    (T(r'$TE_{x\to y} = 0$ if and only if $x$ adds nothing to the predictive distribution of $y$', r'$TE_{x\to y} = 0$ dacă și numai dacă $x$ nu adaugă nimic distribuției predictive a lui $y$'),
     [T('Granger non-causality in distribution, not only in the mean', 'non-cauzalitate Granger în distribuție, nu doar în medie')])), 'small')

D.frame(T('Transfer entropy (2/2)', 'Entropia de transfer (2/2)'), items(
    (T(r'\textbf{Gaussian case} \refBBS: transfer entropy is half the Geweke measure, so the linear Granger test is a TE test', r'\textbf{Cazul gaussian} \refBBS: entropia de transfer este jumătate din măsura Geweke, deci testul Granger liniar este un test TE'),
     [r'\[ TE_{x\to y} = \tfrac12\ln\big(\sigma^2_{\mathrm{' + T('restricted', 'restrîns') + r'}}/\sigma^2_{\mathrm{' + T('full', 'complet') + r'}}\big) = \tfrac12 F_{x\to y} \]',
      T('proof in the Appendix', 'demonstrația în Anexă')]),
    (T(r'\textbf{Nonparametric estimation}: $k$-nearest-neighbour estimators \refKSG, \refFrP', r'\textbf{Estimarea neparametrică}: estimatori cu $k$ cei mai apropiați vecini \refKSG, \refFrP'),
     [T('densities are replaced by distances to the nearest neighbours in the joint space', 'densitățile sînt înlocuite cu distanțele pînă la cei mai apropiați vecini în spațiul comun'),
      T('significance by permuting the source in blocks, which keeps its autocorrelation', 'semnificația prin permutarea sursei pe blocuri, care păstrează autocorelația ei')]),
    T('The same caveats as for Granger: an information flow is not an intervention', 'Aceleași rezerve ca la Granger: un flux de informație nu este o intervenție')), 'small')

chart(T('A nonlinear coupling that linear Granger misses', 'O legătură neliniară pe care testul Granger liniar o ratează'), 'ats_ch14_te', 'ATS_ch14_granger', [
    T(r'Simulated: $y_t = 0.4y_{t-1} + 0.6(x_{t-1}^2 - 1) + u_t$, $x$ a Gaussian AR(1) with unit variance, $u_t$ standard Normal noise, $T = @{te.T}$', r'Simulare: $y_t = 0{,}4y_{t-1} + 0{,}6(x_{t-1}^2 - 1) + u_t$, $x$ un AR(1) gaussian cu varianța 1, $u_t$ zgomot cu distribuția Normală standard, $T = @{te.T}$'),
    T(r'$x_{t-1}^2 - 1$ has mean zero and no correlation with $x_{t-1}$; kNN TE with $k = 5$ neighbours, @{te.B} block permutations', r'$x_{t-1}^2 - 1$ are media zero și nu este corelat cu $x_{t-1}$; TE kNN cu $k = 5$ vecini, @{te.B} de permutări pe blocuri')], h='0.59\\textheight')

interp(('transfer entropy', 'entropiei de transfer'), [
    T(r'Linear Granger: p-value @{te.linp}; Gaussian TE @{te.gauss}$\times10^{-3}$ nats: the symmetric effect averages out in a linear regression', r'Granger liniar: p-value @{te.linp}; TE gaussiană @{te.gauss}$\times10^{-3}$ nats: efectul simetric se anulează în medie într-o regresie liniară'),
    T(r'kNN TE $x\to y$: @{te.xy} nats, permutation $p$ @{te.pxy}; reverse direction @{te.yx} ($p$ @{te.pyx}); without coupling @{te.null} ($p$ @{te.pnull})', r'TE kNN $x\to y$: @{te.xy} nats, $p$ prin permutare @{te.pxy}; direcția inversă @{te.yx} ($p$ @{te.pyx}); fără legătură @{te.null} ($p$ @{te.pnull})'),
    T(r'On the markets of the previous slide the Gaussian TE from the S\&P 500 to the BET is @{gm.te}$\times10^{-3}$ nats: significant, but tiny as information', r'Pe piețele de pe slide-ul anterior, TE gaussiană de la S\&P 500 la BET este @{gm.te}$\times10^{-3}$ nats: semnificativă, dar foarte mică ca informație'),
    T('TE needs much more data than Granger and a careful choice of $k$, history lengths and permutation blocks; pre-register them', 'TE cere mult mai multe date decît Granger și o alegere atentă a lui $k$, a lungimii istoriilor și a blocurilor de permutare; preînregistrați-le')])

D.recap(('Granger causality and causal effects', 'cauzalitatea Granger și efectele cauzale'), [
    T('Granger causality is incremental predictability relative to an information set; enlarging the set can create or destroy it', 'Cauzalitatea Granger înseamnă predictibilitate suplimentară relativ la o mulțime de informație; lărgirea mulțimii o poate crea sau distruge'),
    T('A causal effect needs potential outcomes, non-anticipation and an assignment that is as good as random given the past', 'Un efect cauzal cere rezultate potențiale, non-anticipare și o alocare la fel de bună ca una aleatoare, condiționat de trecut'),
    T('Transfer entropy extends Granger to distributions; for Gaussian processes the two coincide', 'Entropia de transfer extinde Granger la distribuții; pentru procese gaussiene cele două coincid')])

# =============================================================================
# 2. DESCOPERIRE CAUZALĂ
# =============================================================================
D.section('Causal discovery in time series', 'Descoperirea relațiilor cauzale în serii de timp')

D.frame(T('Time series graphs (1/2)', 'Grafurile seriilor de timp (1/2)'), items(
    (T(r'\textbf{Nodes} $X^i_t$: variable $i$ at time $t$; an \textbf{arrow} $X^i_{t-\tau}\to X^j_t$ when $X^i_{t-\tau}$ is a direct cause of $X^j_t$ given the rest of the past \refRunE',
       r'\textbf{Nodurile} $X^i_t$: variabila $i$ la momentul $t$; o \textbf{săgeată} $X^i_{t-\tau}\to X^j_t$ cînd $X^i_{t-\tau}$ este o cauză directă a lui $X^j_t$, dat fiind restul trecutului \refRunE'),
     [T(r'$\tau \ge 1$: the lag of the link; $\tau_{\max}$: the largest lag considered', r'$\tau \ge 1$: lagul legăturii; $\tau_{\max}$: lagul maxim considerat'),
      T('the graph is the same at every $t$ (causal stationarity); arrows only go forward in time', 'graful este același la orice $t$ (staționaritate cauzală); săgețile merg doar înainte în timp')]),
    (T(r'Three assumptions turn independences into arrows \refSGS', r'Trei ipoteze transformă independențele în săgeți \refSGS'),
     [T(r'\textbf{causal Markov}: each variable is independent of its non-effects given its parents (direct causes)', r'\textbf{Markov cauzal}: fiecare variabilă este independentă de non-efectele ei, dați părinții ei (cauzele directe)'),
      T(r'\textbf{faithfulness}: no independence arises by cancellation of effects', r'\textbf{fidelitatea}: nicio independență nu apare prin compensarea efectelor'),
      T(r'\textbf{causal sufficiency}: no hidden common causes', r'\textbf{suficiența cauzală}: nu există cauze comune ascunse')])), 'small')

D.frame(T('Time series graphs (2/2)', 'Grafurile seriilor de timp (2/2)'), items(
    (T(r'Under these assumptions an arrow is a conditional dependence given the whole past', r'Sub aceste ipoteze, o săgeată este o dependență condiționată de întregul trecut'),
     [r'\[ X^i_{t-\tau}\to X^j_t \iff X^i_{t-\tau} \not\perp X^j_t \mid \mathbf X^-_t\setminus\{X^i_{t-\tau}\} \]',
      T(r'$\perp$: independence ($\not\perp$: dependence); $\mathbf X^-_t$: all variables at lags $1, \dots, \tau_{\max}$ before $t$', r'$\perp$: independență ($\not\perp$: dependență); $\mathbf X^-_t$: toate variabilele la lagurile $1, \dots, \tau_{\max}$ înainte de $t$'),
      T('this is the full conditional (VAR) Granger test', 'acesta este testul Granger condiționat complet (VAR)')]),
    (T(r'With $N$ variables and $\tau_{\max}$ lags the conditioning set has $N\tau_{\max}$ elements', r'Cu $N$ variabile și $\tau_{\max}$ laguri, mulțimea de condiționare are $N\tau_{\max}$ elemente'),
     [T('the power of the test collapses in high dimension: the motivation for PCMCI', 'puterea testului scade drastic în dimensiune mare: motivația pentru PCMCI')])), 'small')

D.frame(T('PCMCI', 'PCMCI'), items(
    (T(r'\refPCMCI: two steps, each a sequence of conditional independence tests (partial correlation here; nonlinear tests possible)', r'\refPCMCI: doi pași, fiecare o succesiune de teste de independență condiționată (aici corelația parțială; sînt posibile și teste neliniare)'), []),
    (T(r'\textbf{PC1} (condition selection), for each $X^j_t$', r'\textbf{PC1} (selecția condițiilor), pentru fiecare $X^j_t$'),
     [T(r'start from all lagged candidates; remove those independent of $X^j_t$ given the $p$ strongest others, $p = 1, 2, \dots$', r'se pornește de la toți candidații cu lag; se elimină cei independenți de $X^j_t$, dați cei mai puternici $p$ dintre ceilalți, $p = 1, 2, \dots$'),
      T(r'the result $\hat{\mathcal P}(X^j_t)$ is a superset of the parents of $X^j_t$', r'rezultatul $\hat{\mathcal P}(X^j_t)$ este o supramulțime a părinților lui $X^j_t$')]),
    (T(r'\textbf{MCI} (momentary conditional independence): test each link given the parents of both ends', r'\textbf{MCI} (independența condiționată momentană): fiecare legătură se testează dați părinții ambelor capete'),
     [r'\[ X^i_{t-\tau} \perp X^j_t \mid \hat{\mathcal P}(X^j_t)\setminus\{X^i_{t-\tau}\},\ \hat{\mathcal P}(X^i_{t-\tau}) \]',
      T(r'conditioning on the parents of the \textbf{source} $X^i_{t-\tau}$ removes its autocorrelation: false positives stay near $\alpha$', r'condiționarea pe părinții \textbf{sursei} $X^i_{t-\tau}$ îi elimină autocorelația: rata alarmelor false rămîne aproape de $\alpha$'),
      T('conditioning sets stay small, so power is kept in high dimension', 'mulțimile de condiționare rămîn mici, deci puterea se păstrează în dimensiune mare')]),
    T('Hidden confounders, contemporaneous links, nonstationarity and measurement error break the guarantees; the output is a hypothesis about a graph', 'Factorii de confuzie ascunși, legăturile contemporane, nestaționaritatea și erorile de măsurare anulează garanțiile; rezultatul este o ipoteză despre un graf')), 'small')

chart(T('PCMCI against correlation and the full VAR', 'PCMCI față de corelație și VAR complet'), 'ats_ch14_pcmci_sim', 'ATS_ch14_discovery', [
    T(r'A known lagged system (a persistent common driver, chains and a collider), $\tau_{\max} = 3$, $\alpha = 0.01$, @{ps.reps} replications; right: 14 extra independent AR(1) series', r'Un sistem cunoscut cu laguri (un factor comun persistent, lanțuri și un colizor), $\tau_{\max} = 3$, $\alpha = 0{,}01$, @{ps.reps} de repetări; dreapta: 14 serii AR(1) independente în plus')], h='0.65\\textheight')

interp(('the discovery experiment', 'experimentului de descoperire'), [
    T(r'Lagged correlations find most true links but flag @{ps.lo.pc.f} of the absent ones: autocorrelation and the common driver make everything correlated', r'Corelațiile cu lag găsesc majoritatea legăturilor reale, dar semnalează @{ps.lo.pc.f} dintre cele absente: autocorelația și factorul comun fac totul corelat'),
    T(r'Six variables, $T = 500$: the full VAR and PCMCI are equivalent (power @{ps.lo.var.t} and @{ps.lo.pm.t}; false positives @{ps.lo.var.f} and @{ps.lo.pm.f})', r'Șase variabile, $T = 500$: VAR complet și PCMCI sînt echivalente (putere @{ps.lo.var.t} și @{ps.lo.pm.t}; alarme false @{ps.lo.var.f} și @{ps.lo.pm.f})'),
    T(r'Twenty variables, $T = 150$: the VAR conditions on 60 regressors and its power falls to @{ps.hi.var.t}; PCMCI keeps @{ps.hi.pm.t} with false positives @{ps.hi.pm.f}', r'Douăzeci de variabile, $T = 150$: VAR condiționează pe 60 de regresori, iar puterea lui scade la @{ps.hi.var.t}; PCMCI păstrează @{ps.hi.pm.t}, cu alarme false @{ps.hi.pm.f}'),
    T('The advantage of PCMCI is a high-dimensional one; in small systems a well-specified VAR is enough', 'Avantajul PCMCI ține de dimensiunea mare; în sisteme mici un VAR bine specificat este suficient')])

chart(T('A discovered graph of market volatility', 'Un graf descoperit al volatilității piețelor'), 'ats_ch14_pcmci_vol', 'ATS_ch14_discovery', [
    T(r'PCMCI on weekly log realised variances (sum of squared daily returns), @{pv.start} -- @{pv.end}, $T = @{pv.T}$ weeks, $\tau_{\max} = 2$, $\alpha = 0.01$; weeks remove the ordering of daily closes',
      r'PCMCI pe logaritmul varianțelor realizate săptămînale (suma pătratelor randamentelor zilnice), @{pv.start} -- @{pv.end}, $T = @{pv.T}$ de săptămîni, $\tau_{\max} = 2$, $\alpha = 0{,}01$; săptămînile elimină ordinea închiderilor zilnice')], h='0.65\\textheight')

interp(('the volatility graph', 'grafului volatilității'), [
    T(r'Lagged correlation tests are significant for @{pv.ncorr} of the @{pv.npos} possible lagged cross links; PCMCI keeps @{pv.n}', r'Testele de corelație cu lag sînt semnificative pentru @{pv.ncorr} dintre cele @{pv.npos} de legături încrucișate posibile; PCMCI păstrează @{pv.n}'),
    T('Volatility is a common factor: most of the raw dependence is explained by each market\'s own past and by the shared global shock within the week', 'Volatilitatea este un factor comun: cea mai mare parte a dependenței brute se explică prin propriul trecut al fiecărei piețe și prin șocul global comun din aceeași săptămînă'),
    T('The surviving arrows are small partial correlations; contemporaneous spillovers within the week are invisible to a lagged-only analysis', 'Săgețile rămase sînt corelații parțiale mici; transmiterile contemporane din aceeași săptămînă sînt invizibile pentru o analiză doar cu laguri'),
    T('A hidden global factor (news, VIX) violates causal sufficiency: read the graph as a map of predictive links, not of spillover mechanisms', 'Un factor global ascuns (știri, VIX) încalcă suficiența cauzală: citiți graful ca pe o hartă a legăturilor predictive, nu a mecanismelor de transmitere')])

D.frame(T('Convergent cross mapping', 'Convergent cross mapping'), two(
    ph('sugihara', T('George Sugihara', 'George Sugihara'), h='0.42\\textheight'),
    items(T(r'Deterministic coupled dynamics: Granger\'s separability fails, because the information of the cause is already in the effect \refSug', r'Dinamici deterministe cuplate: separabilitatea lui Granger nu mai funcționează, deoarece informația cauzei se află deja în efect \refSug'),
          (T(r'Takens \refTak: the delay vectors of $y$ reconstruct the attractor of the whole system', r'Takens \refTak: vectorii cu întîrziere ai lui $y$ reconstruiesc atractorul întregului sistem'),
           [r'\[ M_y = \{(y_t, y_{t-\tau}, \dots, y_{t-(E-1)\tau})\} \]',
            T(r'$E$: the embedding dimension; $\tau$: the delay between coordinates', r'$E$: dimensiunea de scufundare; $\tau$: întîrzierea dintre coordonate')]),
          (T(r'If $x$ drives $y$, the neighbours of a point on $M_y$ identify $x_t$: \textbf{cross-map} $x$ from $M_y$', r'Dacă $x$ îl influențează pe $y$, vecinii unui punct de pe $M_y$ identifică $x_t$: se \textbf{estimează încrucișat} $x$ din $M_y$'),
           [T(r'simplex projection: a weighted average of $x$ at the $E + 1$ nearest neighbours; skill: the correlation $\rho$ between estimate and truth', r'proiecția simplex: o medie ponderată a lui $x$ în cei $E + 1$ vecini cei mai apropiați; abilitatea: corelația $\rho$ dintre estimație și valoarea reală')]),
          T(r'Criterion: the skill must \textbf{converge} (increase) with the library size $L$, the number of points used to build $M_y$', r'Criteriul: abilitatea trebuie să \textbf{conveargă} (să crească) cu dimensiunea bibliotecii $L$, numărul de puncte folosite pentru $M_y$'),
          T(r'Note the direction: skill of $M_y \to x$ is evidence for $x \to y$', r'Atenție la direcție: abilitatea $M_y \to x$ este dovadă pentru $x \to y$')), '0.3', '0.68'), 'footnotesize')

chart(T('Cross mapping: a coupling and a common forcing', 'Estimarea încrucișată: o cuplare și un factor periodic comun'), 'ats_ch14_ccm', 'ATS_ch14_discovery', [
    T(r'Coupled logistic maps of \refSug: $x_{t+1} = x_t(r_x - r_xx_t - \beta_{xy}y_t)$, $y_{t+1} = y_t(r_y - r_yy_t - \beta_{yx}x_t)$', r'Aplicațiile logistice cuplate din \refSug: $x_{t+1} = x_t(r_x - r_xx_t - \beta_{xy}y_t)$, $y_{t+1} = y_t(r_y - r_yy_t - \beta_{yx}x_t)$'),
    T(r'$r_x = 3.8$, $r_y = 3.5$: growth rates (chaotic regime); $\beta_{yx} = 0.32$: effect of $x$ on $y$; $\beta_{xy} = 0$: no effect of $y$ on $x$; right: two uncoupled maps with the same periodic forcing; $E = 2$',
      r'$r_x = 3{,}8$, $r_y = 3{,}5$: ratele de creștere (regim haotic); $\beta_{yx} = 0{,}32$: efectul lui $x$ asupra lui $y$; $\beta_{xy} = 0$: niciun efect al lui $y$ asupra lui $x$; dreapta: două aplicații necuplate cu același factor periodic; $E = 2$')], h='0.59\\textheight')

interp(('cross mapping', 'estimării încrucișate'), [
    T(r'Left: skill for $x\to y$ rises from @{cc.axy0} ($L = @{cc.L0}$) to @{cc.axy} ($L = @{cc.L1}$); the reverse stays near @{cc.ayx}: the published pattern', r'Stînga: abilitatea pentru $x\to y$ crește de la @{cc.axy0} ($L = @{cc.L0}$) la @{cc.axy} ($L = @{cc.L1}$); direcția inversă rămîne în jur de @{cc.ayx}: tiparul publicat'),
    T(r'Right: no coupling at all, yet both directions reach @{cc.bxy} and @{cc.byx}: a shared periodic driver synchronises the maps and CCM reports bidirectional causality', r'Dreapta: nicio cuplare, totuși ambele direcții ajung la @{cc.bxy} și @{cc.byx}: un factor periodic comun sincronizează aplicațiile, iar CCM raportează cauzalitate în ambele sensuri'),
    T(r'Known critiques: seasonality and synchrony \refBaC, noise and external forcing \refMon, the choice of lag \refYDGS', r'Critici cunoscute: sezonalitate și sincronizare \refBaC, zgomot și factori externi \refMon, alegerea lagului \refYDGS'),
    T('Use CCM for low-noise nonlinear systems, with surrogate tests that preserve seasonality; never as a black-box causality detector for economic series', 'Folosiți CCM pentru sisteme neliniare cu zgomot redus, cu teste pe serii surogat care păstrează sezonalitatea; niciodată ca detector automat de cauzalitate pentru serii economice')])

D.recap(('Causal discovery', 'descoperirea relațiilor cauzale'), [
    T('A discovered graph is only as good as causal Markov, faithfulness and sufficiency; hidden common drivers are the rule in economics', 'Un graf descoperit este la fel de bun ca ipotezele Markov cauzal, fidelitate și suficiență; factorii comuni ascunși sînt regula în economie'),
    T('PCMCI controls false positives under autocorrelation and keeps power in high dimension', 'PCMCI controlează alarmele false sub autocorelație și păstrează puterea în dimensiune mare'),
    T('CCM targets deterministic coupling; synchrony and common forcing produce false bidirectional links', 'CCM vizează cuplarea deterministă; sincronizarea și factorii comuni produc legături false în ambele sensuri')])

# =============================================================================
# 3. ITS ȘI STUDII DE EVENIMENT
# =============================================================================
D.section('Interrupted time series and event studies', 'Serii de timp întrerupte și studii de eveniment')

D.frame(T('Interrupted time series (1/2)', 'Serii de timp întrerupte (1/2)'), items(
    (T(r'One series, an intervention at $T_0$ \refLCG; step 1: model the pre-period', r'O singură serie, o intervenție la $T_0$ \refLCG; pasul 1: se modelează perioada anterioară'),
     [r'\[ y_t = f(t, \text{' + T('season', 'sezon') + r'}, x_t; \theta) + u_t, \qquad t \le T_0 \]',
      T(r'$f$: trend, seasonal effects and covariates $x_t$, with parameters $\theta$; $u_t$: the error', r'$f$: trendul, efectele sezoniere și covariatele $x_t$, cu parametrii $\theta$; $u_t$: eroarea')]),
    (T(r'Step 2: the effect is the gap between the outcome and the extrapolated model', r'Pasul 2: efectul este diferența dintre rezultat și modelul extrapolat'),
     [r'\[ \hat\tau_t = y_t - f(t, \cdot\,; \hat\theta), \qquad t > T_0 \]',
      T('segmented regression is the special case with level and slope dummies after $T_0$', 'regresia segmentată este cazul particular cu variabile dummy de nivel și de pantă după $T_0$')]),
    (T(r'\textbf{Identification}', r'\textbf{Identificarea}'),
     [T(r'nothing else changes at $T_0$; the pre-period model would have continued; no anticipation', r'nimic altceva nu se schimbă la $T_0$; modelul perioadei anterioare ar fi continuat; nicio anticipare')])), 'small')

D.frame(T('Interrupted time series (2/2)', 'Serii de timp întrerupte (2/2)'), items(
    (T(r'\textbf{Inference with dependent errors}: the variance of the cumulative effect over $n$ periods', r'\textbf{Inferența cu erori dependente}: varianța efectului cumulat pe $n$ perioade'),
     [r'\[ \mathrm{Var}\Big(\sum_{t=T_0+1}^{T_0+n}\hat\tau_t\Big) \approx n\,\Omega + a\'\hat V_\theta a \]',
      T(r'$\Omega$: the long-run variance of $u_t$ (Chapter 0); $\hat V_\theta$: the covariance of $\hat\theta$; $a$: the sum of the regressors of $f$ over the $n$ periods', r'$\Omega$: varianța pe termen lung a lui $u_t$ (Capitolul 0); $\hat V_\theta$: covarianța lui $\hat\theta$; $a$: suma regresorilor lui $f$ pe cele $n$ perioade'),
      T(r'first term: noise of the outcomes; second term: estimation error of the counterfactual', r'primul termen: zgomotul rezultatelor; al doilea: eroarea de estimare a contrafactualului')]),
    (T(r'With AR(1) errors, autocorrelation $\rho$ and $\sigma^2 = \mathrm{Var}(u_t)$', r'Cu erori AR(1), autocorelația $\rho$ și $\sigma^2 = \mathrm{Var}(u_t)$'),
     [r'\[ \Omega = \sigma^2\,\frac{1 + \rho}{1 - \rho} \]',
      T(r'i.i.d.\ standard errors are too small by the factor $\sqrt{(1 + \rho)/(1 - \rho)}$, e.g.\ 1.7 for $\rho = 0.5$', r'erorile standard i.i.d.\ sînt prea mici cu factorul $\sqrt{(1 + \rho)/(1 - \rho)}$, de exemplu 1,7 pentru $\rho = 0{,}5$')])), 'small')

D.frame(T('Romania 2025: two measures one month apart', 'România 2025: două măsuri la o lună distanță'), two(
    ph('parliament', T('Palace of the Parliament, Bucharest', 'Palatul Parlamentului, București'), h='0.40\\textheight'),
    items((T(r'\textbf{1 July 2025}', r'\textbf{1 iulie 2025}'),
           [T('the cap on household electricity prices (in force since 2022) ends', 'se încheie plafonarea prețului electricității pentru gospodării (în vigoare din 2022)'),
            T('the household gas cap continues', 'plafonarea prețului gazelor continuă')]),
          (T(r'\textbf{7 July 2025}', r'\textbf{7 iulie 2025}'),
           [T('the government assumes responsibility for a fiscal package in Parliament (Law 141/2025, published 25 July)', 'guvernul își asumă răspunderea în Parlament pentru un pachet fiscal (Legea 141/2025, publicată pe 25 iulie)')]),
          (T(r'\textbf{1 August 2025}', r'\textbf{1 august 2025}'),
           [T(r'standard VAT 19\% $\to$ 21\%; reduced rates 5\% and 9\% $\to$ 11\%; excise duties up', r'cota standard de TVA 19\% $\to$ 21\%; cotele reduse 5\% și 9\% $\to$ 11\%; accize majorate')]),
          T('Timing alone cannot separate the two; the HICP at constant tax rates can isolate the tax part', 'Momentul singur nu le poate separa; IAPC la cote de taxare constante poate izola partea fiscală'),
          T('Question: how much did the two measures add to Romanian inflation over the following year?', 'Întrebarea: cît au adăugat cele două măsuri la inflația din România în anul următor?')), '0.4', '0.58'), 'small')

chart(T('An interrupted time series for Romanian inflation', 'O serie de timp întreruptă pentru inflația României'), 'ats_ch14_its', 'ATS_ch14_its_event', [
    T(r'Monthly HICP inflation (log change); pre-period model: 12 month effects and a step for July 2021 -- June 2023, fitted on @{its.Tpre} months to June 2025; effects July 2025 -- June 2026',
      r'Inflația IAPC lunară (variația logaritmică); modelul perioadei anterioare: 12 efecte lunare și o treaptă pentru iulie 2021 -- iunie 2023, estimat pe @{its.Tpre} luni pînă în iunie 2025; efectele iulie 2025 -- iunie 2026')], h='0.63\\textheight')

interp(('the interrupted time series', 'seriei de timp întrerupte'), [
    T(r'July 2025: +@{its.jul} pp above the seasonal norm; August 2025: +@{its.aug} pp; later months +@{its.rest} pp on average', r'Iulie 2025: +@{its.jul} pp peste norma sezonieră; august 2025: +@{its.aug} pp; lunile următoare, în medie +@{its.rest} pp'),
    T(r'Cumulative effect over twelve months @{its.cum} pp; standard error @{its.se} with i.i.d. errors, @{its.sehac} with HAC (residual autocorrelation @{its.rho}, long-run variance @{its.lrv} times $\sigma^2$)', r'Efectul cumulat pe douăsprezece luni @{its.cum} pp; eroarea standard @{its.se} cu erori i.i.d., @{its.sehac} cu HAC (autocorelația reziduurilor @{its.rho}, varianța pe termen lung de @{its.lrv} ori $\sigma^2$)'),
    T('The ITS counterfactual is Romania\'s own seasonal norm: it ignores everything else that happened in Europe after June 2025', 'Contrafactualul ITS este norma sezonieră proprie a României: ignoră tot ce s-a mai întîmplat în Europa după iunie 2025'),
    T('A control group is needed to remove common shocks: the synthetic control of Section 5 uses 26 EU countries', 'Pentru a elimina șocurile comune este nevoie de un grup de control: controlul sintetic din secțiunea 5 folosește 26 de țări UE')])

D.frame(T('Event studies with dependent errors', 'Studii de eveniment cu erori dependente'), items(
    (T(r'\refMac, the \textbf{market model} estimated on days $[-250, -11]$ before the event', r'\refMac, \textbf{modelul de piață} estimat pe zilele $[-250, -11]$ dinaintea evenimentului'),
     [r'\[ r_t = \alpha + \beta r^m_t + \varepsilon_t, \qquad AR_t = r_t - \hat\alpha - \hat\beta r^m_t, \qquad CAR[0, k] = \sum_{t=0}^k AR_t \]',
      T(r'$r_t$: the return of the asset; $r^m_t$: the market return; $AR_t$: the abnormal return; $CAR[0, k]$: the cumulative abnormal return over days 0 to $k$', r'$r_t$: randamentul activului; $r^m_t$: randamentul pieței; $AR_t$: randamentul anormal; $CAR[0, k]$: randamentul anormal cumulat pe zilele 0--$k$')]),
    (T(r'Variance of the CAR', r'Varianța CAR'),
     [T(r'$(k + 1)\sigma^2$ under i.i.d.\ errors; $(k + 1)\Omega$ with serial correlation ($\Omega$: long-run variance)', r'$(k + 1)\sigma^2$ sub erori i.i.d.; $(k + 1)\Omega$ cu corelație serială ($\Omega$: varianța pe termen lung)'),
      T('event-induced variance and clustered events need cross-sectional or bootstrap corrections', 'varianța indusă de eveniment și evenimentele grupate cer corecții transversale sau bootstrap')]),
    (T('Identification: the event is a surprise on day 0 and nothing else happened', 'Identificarea: evenimentul este o surpriză în ziua 0 și nimic altceva nu s-a întîmplat'),
     [T('anticipated news is priced before the window', 'știrile anticipate sînt încorporate în preț înaintea ferestrei')]),
    T(r'Here: the BET index against the Euro Stoxx 50, four Romanian political and fiscal events of 2024--2025, window $[0, 2]$', r'Aici: indicele BET față de Euro Stoxx 50, patru evenimente politice și fiscale din România în 2024--2025, fereastra $[0, 2]$')), 'small')

chart(T('Romanian stocks around political and fiscal news', 'Acțiunile românești în jurul știrilor politice și fiscale'), 'ats_ch14_event', 'ATS_ch14_its_event', [
    T(r'Cumulative abnormal return of the BET, normalised at day $-1$; market model on the Euro Stoxx 50; rating actions announced after the close on a Friday are dated on the next Monday', r'Randamentul anormal cumulat al BET, normalizat în ziua $-1$; modelul de piață pe Euro Stoxx 50; acțiunile de rating anunțate după închidere, într-o vineri, sînt datate în lunea următoare')], h='0.65\\textheight')

interp(('the event study', 'studiului de eveniment'), [
    T(r'Annulment of the presidential election (6 December 2024): CAR[0, 2] @{ev0.car}\%, $t$ = @{ev0.t} (i.i.d.) and @{ev0.th} (HAC): the market priced a lower political risk', r'Anularea alegerilor prezidențiale (6 decembrie 2024): CAR[0, 2] @{ev0.car}\%, $t$ = @{ev0.t} (i.i.d.) și @{ev0.th} (HAC): piața a încorporat un risc politic mai mic'),
    T(r'S\&P negative outlook: @{ev1.car}\% ($t$ = @{ev1.th}); ECOFIN decision: @{ev2.car}\% ($t$ = @{ev2.th}); fiscal package: @{ev3.car}\% ($t$ = @{ev3.th})', r'Perspectiva negativă S\&P: @{ev1.car}\% ($t$ = @{ev1.th}); decizia ECOFIN: @{ev2.car}\% ($t$ = @{ev2.th}); pachetul fiscal: @{ev3.car}\% ($t$ = @{ev3.th})'),
    T('Fiscal news had been discussed for months: no surprise on day 0, no abnormal return; a null result here says nothing about the economic effect of the measures', 'Știrile fiscale erau discutate de luni de zile: nicio surpriză în ziua 0, niciun randament anormal; un rezultat nul aici nu spune nimic despre efectul economic al măsurilor'),
    T('HAC and i.i.d.\\ standard errors are close for daily returns (little autocorrelation); they differ for monthly macro data (previous section)', 'Erorile standard HAC și i.i.d.\\ sînt apropiate pentru randamente zilnice (autocorelație mică); diferă pentru date macro lunare (secțiunea anterioară)')])

D.recap(('Interrupted time series and event studies', 'serii de timp întrerupte și studii de eveniment'), [
    T('ITS and event studies compare a series with its own extrapolated past: valid only if nothing else changed at the same time', 'ITS și studiile de eveniment compară o serie cu propriul trecut extrapolat: valide doar dacă nimic altceva nu s-a schimbat în același timp'),
    T('Cumulative effects need the long-run variance of the errors, not $\\sigma^2$', 'Efectele cumulate cer varianța pe termen lung a erorilor, nu $\\sigma^2$'),
    T('Anticipation moves the effect before the window: dating the news is part of the identification', 'Anticiparea mută efectul înaintea ferestrei: datarea știrii face parte din identificare')])

# =============================================================================
# 4. CONTROLUL SINTETIC
# =============================================================================
D.section('Synthetic control', 'Metoda controlului sintetic')

D.frame(T('The synthetic control estimator (1/2)', 'Estimatorul controlului sintetic (1/2)'), items(
    (T(r'Units: $j = 1$ treated, $j = 2, \dots, J + 1$ the \textbf{donor pool}; treatment after period $T_0$ \refAbG, \refADHa', r'Unitățile: $j = 1$ tratată, $j = 2, \dots, J + 1$ \textbf{grupul donatorilor}; tratamentul după perioada $T_0$ \refAbG, \refADHa'),
     [T(r'$Y_{jt}(1)$, $Y_{jt}(0)$: potential outcomes of unit $j$ at $t$ with and without the treatment', r'$Y_{jt}(1)$, $Y_{jt}(0)$: rezultatele potențiale ale unității $j$ la $t$, cu și fără tratament')]),
    (T(r'Target: the effect on the treated unit after $T_0$', r'Ținta: efectul asupra unității tratate după $T_0$'),
     [r'\[ \tau_{1t} = Y_{1t}(1) - Y_{1t}(0), \qquad t > T_0 \]',
      T(r'$Y_{1t}(1) = Y_{1t}$ is observed; $Y_{1t}(0)$ must be estimated', r'$Y_{1t}(1) = Y_{1t}$ este observat; $Y_{1t}(0)$ trebuie estimat')]),
    (T(r'\textbf{Synthetic control}: a weighted average of the donors stands in for $Y_{1t}(0)$', r'\textbf{Controlul sintetic}: o medie ponderată a donatorilor ține locul lui $Y_{1t}(0)$'),
     [r'\[ \hat Y_{1t}(0) = \sum_{j=2}^{J+1} w_jY_{jt}, \qquad \hat\tau_{1t} = Y_{1t} - \hat Y_{1t}(0) \]',
      T(r'$w_j \ge 0$: the weight of donor $j$, with $\sum_j w_j = 1$', r'$w_j \ge 0$: ponderea donatorului $j$, cu $\sum_j w_j = 1$')])), 'small')

D.frame(T('The synthetic control estimator (2/2)', 'Estimatorul controlului sintetic (2/2)'), items(
    (T(r'\textbf{Weights}: the convex combination of donors closest to the treated unit in the pre-treatment predictors', r'\textbf{Ponderile}: combinația convexă de donatori cea mai apropiată de unitatea tratată după predictorii anteriori tratamentului'),
     [r'\[ w^*(V) = \arg\min_w\, (X_1 - X_0w)\'V(X_1 - X_0w), \qquad w_j \ge 0,\ \sum_j w_j = 1 \]',
      T(r'$X_1$: the vector of pre-treatment predictors of the treated unit (outcome averages, covariates); $X_0$: the matrix of the same predictors for the donors', r'$X_1$: vectorul predictorilor anteriori tratamentului ai unității tratate (medii ale rezultatului, covariate); $X_0$: matricea acelorași predictori pentru donatori'),
      T(r'a quadratic programme on the simplex: weights are sparse and interpretable; no extrapolation outside the donors\' range', r'o problemă de programare pătratică pe simplex: ponderile sînt rare și interpretabile; nicio extrapolare în afara domeniului donatorilor')]),
    (T(r'$V = \mathrm{diag}(v)$: the importance of each predictor', r'$V = \mathrm{diag}(v)$: importanța fiecărui predictor'),
     [T(r'chosen to minimise the pre-period $\mathrm{MSPE} = \frac{1}{T_0}\sum_{t \le T_0}(Y_{1t} - \sum_j w_j^*(V)Y_{jt})^2$ (nested optimisation, \refADHs)', r'aleasă pentru a minimiza în perioada anterioară $\mathrm{MSPE} = \frac{1}{T_0}\sum_{t \le T_0}(Y_{1t} - \sum_j w_j^*(V)Y_{jt})^2$ (optimizare imbricată, \refADHs)'),
      T(r'MSPE: mean squared prediction error of the outcome; alternative: cross-validation on a training and a validation period \refADHb', r'MSPE: eroarea pătratică medie de predicție a rezultatului; alternativa: validarea încrucișată pe o perioadă de antrenare și una de validare \refADHb'),
      T(r'with all pre-period outcomes in $X$, the covariates get no weight \refKKPS', r'cu toate rezultatele anterioare în $X$, covariatele nu primesc nicio pondere \refKKPS')])), 'small')

D.frame(T('Why it works: the factor model', 'Fundamentul: modelul factorial'), items(
    (T(r'\refADHa: the untreated outcomes follow a factor model (interactive fixed effects \refBai)', r'\refADHa: rezultatele fără tratament urmează un model factorial (efecte fixe interactive \refBai)'),
     [r'\[ Y_{jt}(0) = \delta_t + \theta_tZ_j + \lambda_t\mu_j + \varepsilon_{jt} \]',
      T(r'$\delta_t$: a common time effect; $Z_j$: observed covariates with time-varying coefficients $\theta_t$; $\lambda_t$: unobserved common factors; $\mu_j$: unobserved loadings of unit $j$; $\varepsilon_{jt}$: transitory shocks',
        r'$\delta_t$: un efect comun al perioadei; $Z_j$: covariate observate, cu coeficienții variabili în timp $\theta_t$; $\lambda_t$: factori comuni neobservați; $\mu_j$: încărcările neobservate ale unității $j$; $\varepsilon_{jt}$: șocuri tranzitorii'),
      T(r'DiD assumes $\lambda_t$ constant (parallel trends); SC lets the common factors vary over time', r'DiD presupune $\lambda_t$ constant (trenduri paralele); SC permite factorilor comuni să varieze în timp')]),
    (T(r'If the weights reproduce the treated unit before $T_0$, $\sum_j w_jY_{jt} = Y_{1t}$ for all $t \le T_0$ and $\sum_j w_jZ_j = Z_1$, then',
       r'Dacă ponderile reproduc unitatea tratată înainte de $T_0$, $\sum_j w_jY_{jt} = Y_{1t}$ pentru orice $t \le T_0$ și $\sum_j w_jZ_j = Z_1$, atunci'),
     [T(r'the bias of $\hat\tau_{1t}$ is bounded by a term that \textbf{shrinks as $T_0$ grows}, relative to the scale of $\varepsilon$ (Appendix)', r'deplasarea lui $\hat\tau_{1t}$ este mărginită de un termen care \textbf{scade cînd $T_0$ crește}, relativ la scala lui $\varepsilon$ (Anexă)'),
      T(r'a good fit over a long pre-period is evidence that the loadings $\mu_j$ are matched', r'o potrivire bună pe o perioadă anterioară lungă arată că încărcările $\mu_j$ sînt reproduse')]),
    T(r'A short pre-period with a perfect fit can be overfitting the noise: the bound is then weak \refAba', r'O perioadă anterioară scurtă cu potrivire perfectă poate însemna supraajustarea zgomotului: marginea este atunci slabă \refAba')), 'small')

D.frame(T('Feasibility conditions', 'Condiții de aplicabilitate'), items(
    (T(r'\textbf{Convex hull} \refAba', r'\textbf{Înfășurătoarea convexă} \refAba'),
     [T('the treated unit must lie inside the range of the donors; otherwise no convex combination fits it', 'unitatea tratată trebuie să se afle în domeniul donatorilor; altfel nicio combinație convexă nu o reproduce')]),
    (T(r'\textbf{Donor pool}', r'\textbf{Grupul donatorilor}'),
     [T(r'units with similar structure, not affected by the treatment (no spillovers), without large shocks of their own after $T_0$', r'unități cu structură asemănătoare, neafectate de tratament (fără efecte de propagare), fără șocuri mari proprii după $T_0$')]),
    (T(r'\textbf{No anticipation}', r'\textbf{Nicio anticipare}'),
     [T(r'effects must not start before $T_0$; backdate $T_0$ to the announcement if needed', r'efectele nu trebuie să înceapă înainte de $T_0$; mutați $T_0$ la anunț dacă este nevoie')]),
    (T(r'\textbf{Long pre-period} with a good fit', r'\textbf{Perioadă anterioară lungă}, cu potrivire bună'),
     [T(r'\textbf{interpolation bias}: a mix of very different donors may not resemble the treated unit even if the averages match', r'\textbf{deplasarea de interpolare}: un amestec de donatori foarte diferiți poate să nu semene cu unitatea tratată chiar dacă mediile coincid')]),
    (T('Report', 'Raportați'),
     [T('weights, predictor balance, pre-period RMSPE, the placebo distribution, leave-one-out', 'ponderile, echilibrul predictorilor, RMSPE în perioada anterioară, distribuția placebo, omiterea pe rînd a donatorilor')])), 'small')

D.frame(T('Inference with one treated unit', 'Inferența cu o singură unitate tratată'), items(
    (T(r'\textbf{In-space placebos} \refADHa: reassign the treatment to every donor in turn, refit, and compute the ratio', r'\textbf{Placebo în spațiu} \refADHa: tratamentul se atribuie pe rînd fiecărui donator, se reestimează și se calculează raportul'),
     [r'\[ r_j = \mathrm{RMSPE}_{\mathrm{post}}/\mathrm{RMSPE}_{\mathrm{pre}}, \qquad \text{p-value} = \#\{j: r_j \ge r_1\}/(J + 1) \]',
      T(r'RMSPE: root mean squared prediction error of the synthetic control, before (pre) and after (post) $T_0$; a large $r_j$: a large post-treatment gap relative to the pre-fit',
        r'RMSPE: rădăcina erorii pătratice medii de predicție a controlului sintetic, înainte (pre) și după (post) $T_0$; un $r_j$ mare: o diferență mare după tratament, relativ la potrivirea anterioară'),
      T(r'$\#\{\cdot\}$: the number of units; the smallest attainable p-value is $1/(J + 1)$; exact only under random assignment across units, otherwise a descriptive ranking \refFiP',
        r'$\#\{\cdot\}$: numărul de unități; cel mai mic p-value posibil este $1/(J + 1)$; exact doar dacă tratamentul este atribuit aleator între unități, altfel o ordonare descriptivă \refFiP')]),
    (T(r'\textbf{Other robustness checks}', r'\textbf{Alte verificări de robustețe}'),
     [T(r'in-time placebos: a fictitious $T_0$ inside the pre-period should give no effect', r'placebo în timp: un $T_0$ fictiv în perioada anterioară nu trebuie să dea niciun efect'),
      T(r'leave-one-out: drop each donor with positive weight and refit', r'omiterea pe rînd: se elimină fiecare donator cu pondere pozitivă și se reestimează')]),
    (T(r'\textbf{Conformal inference} \refCWZ: test $H_0$: $\tau_{1t} = \tau_0$ by permuting the residuals over time', r'\textbf{Inferența conformală} \refCWZ: se testează $H_0$: $\tau_{1t} = \tau_0$ permutînd reziduurile în timp'),
     [T(r'block permutations for dependence; confidence sets by inverting the test over $\tau_0$', r'permutări pe blocuri pentru dependență; intervale de încredere prin inversarea testului după $\tau_0$')])), 'small')

D.frame(T('Case study: the economic cost of German reunification', 'Studiu de caz: costul economic al reunificării Germaniei'), two(
    ph('gate', T('Brandenburg Gate, Berlin, 11 November 1989', 'Poarta Brandenburg, Berlin, 11 noiembrie 1989'), h='0.42\\textheight'),
    items((T(r'\refADHb', r'\refADHb'),
           [T('did the 1990 reunification lower West German GDP per capita?', 'a scăzut reunificarea din 1990 PIB-ul pe locuitor al Germaniei de Vest?')]),
          (T(r'Data \refADHd', r'Datele \refADHd'),
           [T('West Germany and 16 OECD countries, 1960--2003', 'Germania de Vest și 16 țări OCDE, 1960--2003'),
            T('predictors: GDP per capita, trade openness, inflation, industry share, schooling, investment rate', 'predictori: PIB pe locuitor, deschiderea comercială, inflația, ponderea industriei, școlarizarea, rata investițiilor')]),
          (T(r'$V$ by cross-validation (Section 4 and the replication code)', r'$V$ prin validare încrucișată (secțiunea 4 și codul de replicare)'),
           [T('training predictors 1971--1980, validation outcomes 1981--1990', 'predictori de antrenare 1971--1980, rezultate de validare 1981--1990'),
            T(r'final weights from the 1981--1990 predictors with that $V$', r'ponderile finale din predictorii 1981--1990 cu acest $V$')]),
          (T('Erratum (2026)', 'Erată (2026)'),
           [T(r'the outcome is GDP per capita in PPP \textit{current} USD, not 2002 USD as labelled in the article', r'rezultatul este PIB-ul pe locuitor în USD PPC \textit{curenți}, nu în USD 2002 cum este etichetat în articol')])), '0.38', '0.6'), 'small')

D.frame(T('Replication: weights and predictor balance', 'Replicare: ponderile și echilibrul predictorilor'), cols(
    table('lrr', T(r'\textbf{Donor} & \textbf{ours} & \textbf{ADH, Table 1}', r'\textbf{Donator} & \textbf{replicare} & \textbf{ADH, tabelul 1}'),
          [f'{cname(k)} & @{{ge.w.{k.lower()}}} & @{{ge.pub.{k.lower()}}}' for k in ('Austria', 'USA', 'Japan', 'Switzerland', 'Netherlands')],
          size='footnotesize'),
    table('lrrr', T(r'\textbf{Predictor} & \textbf{West Germany} & \textbf{synthetic} & \textbf{OECD avg.}', r'\textbf{Predictor} & \textbf{Germania de Vest} & \textbf{sintetic} & \textbf{media OCDE}'),
          [T('GDP per capita', 'PIB pe locuitor') + ' & @{ge.gdp.t} & @{ge.gdp.s} & @{ge.gdp.a}',
           T('Trade openness', 'Deschidere comercială') + ' & @{ge.trade.t} & @{ge.trade.s} & @{ge.trade.a}',
           T('Inflation', 'Inflația') + ' & @{ge.inf.t} & @{ge.inf.s} & @{ge.inf.a}',
           T('Industry share', 'Ponderea industriei') + ' & @{ge.ind.t} & @{ge.ind.s} & @{ge.ind.a}',
           T('Schooling', 'Școlarizare') + ' & @{ge.sch.t} & @{ge.sch.s} & @{ge.sch.a}',
           T('Investment rate', 'Rata investițiilor') + ' & @{ge.inv.t} & @{ge.inv.s} & @{ge.inv.a}'], size='footnotesize'),
    '0.38', '0.6') + items(
    T('The cross-validated $V$ and the quadratic programme reproduce the published weights to two decimals; all other donors get zero weight', '$V$ ales prin validare încrucișată și programarea pătratică reproduc ponderile publicate cu două zecimale; toți ceilalți donatori primesc pondere zero'),
    T('The simple OECD average differs on every predictor: the unweighted comparison would be biased', 'Media simplă OCDE diferă la fiecare predictor: comparația neponderată ar fi deplasată')), 'small')

chart(T('West Germany and its synthetic control', 'Germania de Vest și controlul ei sintetic'), 'ats_ch14_germany', 'ATS_ch14_germany', [
    T(r'Left: GDP per capita (PPP, current USD); right: the gap; pre-1990 RMSPE @{ge.rmspe} USD', r'Stînga: PIB pe locuitor (PPC, USD curenți); dreapta: diferența; RMSPE înainte de 1990: @{ge.rmspe} USD')], h='0.66\\textheight')

interp(('the German replication', 'replicării germane'), [
    T(r'The synthetic West Germany tracks the actual series for thirty years (1960--1989), then grows faster', r'Germania de Vest sintetică urmărește seria reală timp de treizeci de ani (1960--1989), apoi crește mai repede'),
    T(r'Average gap 1990--2003: $-$@{ge.avg} USD per capita a year ($-$@{ge.rel}\% of the synthetic level); in 2003: $-$@{ge.gap03} USD ($-$@{ge.rel03}\%)', r'Diferența medie 1990--2003: $-$@{ge.avg} USD pe locuitor pe an ($-$@{ge.rel}\% din nivelul sintetic); în 2003: $-$@{ge.gap03} USD ($-$@{ge.rel03}\%)'),
    T('The paper reports a reduction of about 1,600 USD a year on average: the replication matches', 'Lucrarea raportează o reducere de aproximativ 1600 USD pe an, în medie: replicarea coincide'),
    T('The donors (Austria, USA, Japan, Switzerland, Netherlands) are rich, industrial economies: the weights make economic sense, a check no algorithm does for us', 'Donatorii (Austria, SUA, Japonia, Elveția, Țările de Jos) sînt economii bogate, industrializate: ponderile au sens economic, o verificare pe care niciun algoritm nu o face în locul nostru')])

chart(T('Placebos for the German case', 'Testele placebo pentru cazul german'), 'ats_ch14_germany_placebo', 'ATS_ch14_germany', [
    T('Left: post/pre-1990 RMSPE ratio when each country is treated in turn (ADH 2015, Figure 6); centre: reunification moved to 1975 (as in Figure 4, outcome-only SC); right: one donor left out at a time (Figure 5)', 'Stînga: raportul RMSPE după/înainte de 1990 cînd fiecare țară este tratată pe rînd (ADH 2015, figura 6); centru: reunificarea mutată în 1975 (ca în figura 4, SC doar pe rezultat); dreapta: cîte un donator omis (figura 5)')], h='0.54\\textheight')

interp(('the German placebos', 'testelor placebo germane'), [
    T(r'West Germany has the largest ratio (@{gp.r}; next: @{gp.second}, @{gp.r2}): permutation p-value $1/@{gp.n}$ = @{gp.p}, the smallest attainable', r'Germania de Vest are cel mai mare raport (@{gp.r}; următoarea: @{gp.second}, @{gp.r2}): p-value-ul prin permutare $1/@{gp.n}$ = @{gp.p}, cea mai mică posibilă'),
    T(r'Placebo reunification in 1975 (outcome-only SC on 1960--1974, pre-RMSPE @{gp.rm75} USD): West Germany grows faster than its synthetic control (average gap +@{gp.rel75}\% to 1990): no spurious cost appears', r'Reunificare placebo în 1975 (SC doar pe rezultat, 1960--1974, RMSPE anterior @{gp.rm75} USD): Germania de Vest crește mai repede decît controlul sintetic (diferența medie +@{gp.rel75}\% pînă în 1990): nu apare niciun cost fals'),
    T(r'With the published 1975 predictors the cross-validated $V$ is not identified: one starting value gives @{gp.v1} as the donor, the best of eight gives @{gp.v8} \refKPSb', r'Cu predictorii publicați pentru 1975, $V$ ales prin validare încrucișată nu este identificat: un punct de pornire dă ca donator @{gp.v1}, cel mai bun dintre opt dă @{gp.v8} \refKPSb'),
    T(r'Leaving out any donor keeps a negative gap in 2003, between @{gp.loomin} and @{gp.loomax} USD: the result does not hinge on one country', r'Omiterea oricărui donator păstrează o diferență negativă în 2003, între @{gp.loomin} și @{gp.loomax} USD: rezultatul nu depinde de o singură țară'),
    T('With 17 units the permutation test cannot give $p < 0.059$', 'Cu 17 unități, testul de permutare nu poate da $p < 0{,}059$')])

D.frame(T('Case study: the Brexit doppelganger', 'Studiu de caz: dublura Brexit'), two(
    ph('brexit', T('Counting the votes of the EU referendum, 23 June 2016', 'Numărarea voturilor la referendumul privind UE, 23 iunie 2016'), h='0.32\\textheight'),
    items((T(r'\refBMSS', r'\refBMSS'),
           [T('the referendum of 23 June 2016 as a natural experiment; outcome: UK real GDP', 'referendumul din 23 iunie 2016 ca experiment natural; rezultatul: PIB-ul real al Regatului Unit')]),
          (T('Design (Section 2.1)', 'Designul (secțiunea 2.1)'),
           [T('23 OECD donors; quarterly real GDP, normalised to 1 in 1995', '23 de donatori OCDE; PIB real trimestrial, normalizat la 1 în 1995'),
            T('pre-period 1995Q1--2016Q2; six covariate averages', 'perioada anterioară T1 1995 -- T2 2016; mediile a șase covariate'),
            T(r'published weights (Table 2): @{bx.pub}', r'ponderile publicate (tabelul 2): @{bx.pub}')]),
          (T('Published result', 'Rezultatul publicat'),
           [T('UK output 2.4\\% below the doppelganger by the end of 2018', 'producția Regatului Unit cu 2,4\\% sub dublură la sfîrșitul lui 2018'),
            T('significant by the end-of-sample instability test of \\refAnd', 'semnificativ după testul de instabilitate la sfîrșitul eșantionului al lui \\refAnd')]),
          (T('Our replication', 'Replicarea noastră'),
           [T(r'the same donors and window; the current OECD vintage (to @{ov.oecd}); the GDP path only (no covariates)', r'aceiași donatori și aceeași fereastră; ediția curentă a datelor OCDE (pînă în @{ov.oecd}); doar traiectoria PIB (fără covariate)')])), '0.3', '0.68'), 'small')

chart(T('The doppelganger on today\'s data', 'Dublura pe datele de azi'), 'ats_ch14_brexit', 'ATS_ch14_brexit', [
    T(r'Left: UK real GDP and its doppelganger (\% from 2016Q2), with the doppelgangers of fictitious votes in every quarter 2010Q1--2016Q1; right: the 12 largest post/pre RMSPE ratios of the 24 countries', r'Stînga: PIB-ul real al Regatului Unit și dublura lui (\% față de T2 2016), cu dublurile voturilor fictive din fiecare trimestru T1 2010 -- T1 2016; dreapta: cele mai mari 12 rapoarte RMSPE după/înainte dintre cele 24 de țări')], h='0.65\\textheight')

interp(('the Brexit replication', 'replicării Brexit'), [
    T(r'Weights on today\'s data: @{bx.w}; the doppelganger changes with the data vintage', r'Ponderile pe datele de azi: @{bx.w}; dublura se schimbă odată cu ediția datelor'),
    T(r'Gap: @{bx.g17}\% in 2017Q4, $-$@{bx.g18}\% in 2018Q4 (published: $-$2.4\%), $-$@{bx.g19}\% in 2019Q4; pre-vote standard deviation @{bx.sd}\%', r'Diferența: @{bx.g17}\% în T4 2017, $-$@{bx.g18}\% în T4 2018 (publicat: $-$2,4\%), $-$@{bx.g19}\% în T4 2019; abaterea standard înainte de vot @{bx.sd}\%'),
    T(r'The UK ranks @{bx.rank} of @{bx.n} in the country placebos; the @{bx.ntp} time placebos give 2018Q4 gaps from @{bx.tpmin}\% to @{bx.tpmax}\%: on revised data the evidence is much weaker', r'Regatul Unit este pe locul @{bx.rank} din @{bx.n} în testele placebo pe țări; cele @{bx.ntp} de teste placebo în timp dau diferențe în T4 2018 între @{bx.tpmin}\% și @{bx.tpmax}\%: pe datele revizuite dovezile sînt mult mai slabe'),
    T('A replication changes the data (revisions), the specification (no covariates) and the inference (permutation instead of an end-of-sample test): report each deviation separately', 'O replicare schimbă datele (revizuiri), specificația (fără covariate) și inferența (permutare în locul testului de la sfîrșitul eșantionului): raportați fiecare abatere separat')])

D.recap(('Synthetic control', 'controlul sintetic'), [
    T('A convex combination of donors fitted on a long pre-period; justified by a factor model; transparent sparse weights', 'O combinație convexă de donatori ajustată pe o perioadă lungă anterioară; justificată de un model factorial; ponderi rare și transparente'),
    T('Inference by placebos in space and time, leave-one-out, conformal methods; $p \\ge 1/(J + 1)$', 'Inferența prin placebo în spațiu și în timp, omiterea pe rînd a donatorilor, metode conformale; $p \\ge 1/(J + 1)$'),
    T('German reunification replicates exactly; the Brexit gap is sensitive to data revisions and specification', 'Reunificarea Germaniei se replică exact; diferența Brexit este sensibilă la revizuirea datelor și la specificație')])

# =============================================================================
# 5. DUPĂ CONTROLUL SINTETIC
# =============================================================================
D.section('Beyond synthetic control', 'Dincolo de controlul sintetic')

D.frame(T('Intercepts and augmentation', 'Termenul liber și augmentarea'), items(
    (T(r'\textbf{Demeaned SC} \refDI, \refFP: allows a constant level difference $c$ between the treated unit and the donors', r'\textbf{SC cu termen liber} \refDI, \refFP: permite o diferență constantă de nivel $c$ între unitatea tratată și donatori'),
     [r'\[ \hat Y_{1t}(0) = c + \sum_j w_jY_{jt} \]',
      T('the weights are fitted on pre-period outcomes minus the pre-period mean of each unit', 'ponderile se ajustează pe rezultatele anterioare minus media anterioară a fiecărei unități'),
      T('solves the level part of the convex-hull problem; consistent under imperfect pre-fit when the factors are stationary \\refFP', 'rezolvă partea de nivel a problemei înfășurătorii convexe; consistent cu potrivire imperfectă cînd factorii sînt staționari \\refFP')]),
    (T(r'\textbf{Augmented SC} \refASCM: corrects the SC estimate by the remaining predictor imbalance, through a ridge regression', r'\textbf{SC augmentat} \refASCM: corectează estimația SC cu dezechilibrul rămas al predictorilor, printr-o regresie ridge'),
     [r'\[ \hat Y^{\mathrm{aug}}_{1t}(0) = \sum_j\hat w_jY_{jt} + \Big(X_1 - \sum_j\hat w_jX_j\Big)\'\hat\eta_t \]',
      T(r'$\hat w_j$: the SC weights; $X_j$: the pre-period outcomes of unit $j$; $\hat\eta_t$: coefficients of a ridge regression of $Y_{jt}$ on $X_j$ across donors, with penalty $\lambda$', r'$\hat w_j$: ponderile SC; $X_j$: rezultatele anterioare ale unității $j$; $\hat\eta_t$: coeficienții regresiei ridge a lui $Y_{jt}$ pe $X_j$, între donatori, cu penalizarea $\lambda$'),
      T(r'equivalent to weights $\hat w + X_0(X_0\'X_0 + \lambda I)^{-1}(X_1 - X_0\'\hat w)$, which can be negative (controlled extrapolation)', r'echivalent cu ponderile $\hat w + X_0(X_0\'X_0 + \lambda I)^{-1}(X_1 - X_0\'\hat w)$, care pot fi negative (extrapolare controlată)'),
      T(r'$\lambda \to \infty$ gives SC; $\lambda \to 0$ gives an outcome regression; the bias falls with the remaining imbalance', r'$\lambda \to \infty$ dă SC; $\lambda \to 0$ dă o regresie a rezultatului; deplasarea scade odată cu dezechilibrul rămas')])), 'small')

D.frame(T('Synthetic difference in differences (1/2)', 'Diferența în diferențe sintetică (1/2)'), items(
    (T(r'\refSDID: a two-way fixed-effects regression in which units and periods are weighted', r'\refSDID: o regresie cu efecte fixe pe unități și pe perioade, în care unitățile și perioadele sînt ponderate'),
     [r'\[ (\hat\tau, \hat\mu, \hat\alpha, \hat\beta) = \arg\min\sum_{j,t}\big(Y_{jt} - \mu - \alpha_j - \beta_t - W_{jt}\tau\big)^2\hat\omega_j\hat\lambda_t \]',
      T(r'$W_{jt} = 1$ for the treated unit after $T_0$, 0 otherwise; $\tau$: the effect; $\mu$: the overall mean; $\alpha_j$: unit fixed effects; $\beta_t$: period fixed effects',
        r'$W_{jt} = 1$ pentru unitatea tratată după $T_0$, 0 altfel; $\tau$: efectul; $\mu$: media generală; $\alpha_j$: efectele fixe ale unităților; $\beta_t$: efectele fixe ale perioadelor')]),
    (T(r'\textbf{Unit weights} $\hat\omega_j$: SC with an intercept and a ridge penalty', r'\textbf{Ponderile unităților} $\hat\omega_j$: SC cu termen liber și penalizare ridge'),
     [T(r'penalty $\zeta^2T_0\|\omega\|^2$ with $\zeta = (N_{\mathrm{tr}}T_{\mathrm{post}})^{1/4}\hat\sigma$; $N_{\mathrm{tr}}$: treated units; $T_{\mathrm{post}}$: post-periods; $\hat\sigma$: the noise level of the controls',
        r'penalizarea $\zeta^2T_0\|\omega\|^2$, cu $\zeta = (N_{\mathrm{tr}}T_{\mathrm{post}})^{1/4}\hat\sigma$; $N_{\mathrm{tr}}$: unitățile tratate; $T_{\mathrm{post}}$: perioadele de după; $\hat\sigma$: nivelul zgomotului controalelor')]),
    (T(r'\textbf{Time weights} $\hat\lambda_t$: the pre-periods that best predict the post-period mean of the controls', r'\textbf{Ponderile perioadelor} $\hat\lambda_t$: perioadele anterioare care prezic cel mai bine media controalelor după tratament'), [])), 'small')

D.frame(T('Synthetic difference in differences (2/2)', 'Diferența în diferențe sintetică (2/2)'), items(
    (T('Three estimators as special cases', 'Trei estimatori ca și cazuri particulare'),
     [T(r'DiD: $\omega$ and $\lambda$ uniform', r'DiD: $\omega$ și $\lambda$ uniforme'),
      T(r'SC: unit weights $\omega$ only (uniform $\lambda$), no unit fixed effect', r'SC: doar ponderile unităților $\omega$ ($\lambda$ uniforme), fără efect fix al unității'),
      T('SDID: both sets of weights, both fixed effects', 'SDID: ambele seturi de ponderi, ambele efecte fixe')]),
    (T(r'One treated unit: placebo standard error', r'O singură unitate tratată: eroarea standard prin placebo'),
     [T('each control in turn plays the treated unit; the standard deviation of the placebo estimates is the standard error (Algorithm 4)', 'fiecare control joacă pe rînd rolul unității tratate; abaterea standard a estimațiilor placebo este eroarea standard (algoritmul 4)')])), 'small')

D.frame(T('Romania 2025: design of the synthetic control', 'România 2025: designul controlului sintetic'), items(
    (T(r'Outcome: annual HICP inflation (pp), $100(\ln P_t - \ln P_{t-12})$, Eurostat; treated: Romania; donors: the other 26 EU countries', r'Rezultatul: inflația IAPC anuală (pp), $100(\ln P_t - \ln P_{t-12})$, Eurostat; unitatea tratată: România; donatori: celelalte 26 de țări UE'),
     [T(r'$P_t$: the HICP price index in month $t$; pp: percentage points', r'$P_t$: indicele prețurilor IAPC în luna $t$; pp: puncte procentuale'),
      T('the annual rate removes seasonality and makes a price-level shock visible for exactly twelve months', 'rata anuală elimină sezonalitatea și face vizibil un șoc al nivelului prețurilor exact douăsprezece luni')]),
    (T(r'Pre-period: July 2023 -- June 2025 (@{ro.npre} months, after the 2021--2023 surge); treatment from July 2025; effect window July 2025 -- June 2026', r'Perioada anterioară: iulie 2023 -- iunie 2025 (@{ro.npre} de luni, după valul 2021--2023); tratament din iulie 2025; fereastra efectului iulie 2025 -- iunie 2026'),
     [T(r'a built-in falsification: once the price-level jump leaves the 12-month window (August 2026), the gap must close', r'o falsificare încorporată: după ce saltul nivelului prețurilor iese din fereastra de 12 luni (august 2026), diferența trebuie să dispară')]),
    T('Estimators: SC, demeaned SC, ridge-augmented demeaned SC, SDID; inference: in-space placebos', 'Estimatori: SC, SC cu termen liber, SC augmentat ridge cu termen liber, SDID; inferența: placebo în spațiu'),
    T('Threats: other countries\' own energy and tax measures; anticipation of the VAT increase; Romania outside the donors\' range', 'Amenințări: măsurile proprii de energie și fiscale ale altor țări; anticiparea majorării TVA; România în afara domeniului donatorilor')), 'small')

chart(T('Four counterfactuals for Romanian inflation', 'Patru contrafactuale pentru inflația României'), 'ats_ch14_ro_sc', 'ATS_ch14_romania', [
    T(r'Left: Romania and the four estimated counterfactuals; right: the gaps; vertical line: June 2025; data to @{ro.end}', r'Stînga: România și cele patru contrafactuale estimate; dreapta: diferențele; linia verticală: iunie 2025; date pînă în @{ro.end}')], h='0.65\\textheight')

D.frame(T('Interpreting the four estimators', 'Interpretarea celor patru estimatori'), table(
    'lcccc', T(r'\textbf{Estimator} & \textbf{pre RMSPE} & \textbf{August 2025} & \textbf{avg. Jul 2025 -- Jun 2026} & \textbf{August 2026}', r'\textbf{Estimator} & \textbf{RMSPE anterior} & \textbf{august 2025} & \textbf{media iul. 2025 -- iun. 2026} & \textbf{august 2026}'),
    ['SC & @{ro.sc.rm} & @{ro.sc.aug25} & @{ro.sc} & @{ro.sc.aug26}',
     T('demeaned SC', 'SC cu termen liber') + ' & @{ro.dsc.rm} & @{ro.dsc.aug25} & @{ro.dsc} & @{ro.dsc.aug26}',
     T('augmented SC', 'SC augmentat') + ' & @{ro.asc.rm} & @{ro.asc.aug25} & @{ro.asc} & @{ro.asc.aug26}',
     'SDID & -- & @{ro.sdid.aug25} & @{ro.sdid} ($se$ @{ro.sdse}) & @{ro.sdid.aug26}'],
    size='scriptsize') + items(
    T(r'Classic SC puts all weight on @{ro.sc.w}: Romania is outside the convex hull, the pre-fit is poor and the effect is overstated', r'SC clasic pune toată ponderea pe @{ro.sc.w}: România se află în afara înfășurătorii convexe, potrivirea anterioară este slabă, iar efectul este supraestimat'),
    T(r'With an intercept the fit is good (weights @{ro.dsc.w}, ...); augmented SC ($\lambda = @{ro.lam}$, @{ro.asc.neg} negative weights) and SDID agree: @{ro.lo}--@{ro.hi} pp over twelve months', r'Cu termen liber potrivirea este bună (ponderi @{ro.dsc.w}, ...); SC augmentat ($\lambda = @{ro.lam}$, @{ro.asc.neg} ponderi negative) și SDID sînt de acord: @{ro.lo}--@{ro.hi} pp pe douăsprezece luni'),
    T(r'Falsification: in August 2026 the gap falls to @{ro.dsc.aug26} (demeaned SC) and @{ro.sdid.aug26} (SDID); the augmented SC keeps @{ro.asc.aug26}, the price of extrapolating with negative weights', r'Falsificarea: în august 2026 diferența scade la @{ro.dsc.aug26} (SC cu termen liber) și @{ro.sdid.aug26} (SDID); SC augmentat păstrează @{ro.asc.aug26}, prețul extrapolării cu ponderi negative')), 'small')

chart(T('Placebo inference for Romania', 'Inferența prin placebo pentru România'), 'ats_ch14_ro_placebo', 'ATS_ch14_romania', [
    T('Demeaned SC applied to every EU country in turn; left: gaps; right: the 12 largest post/pre RMSPE ratios over July 2025 -- June 2026', 'SC cu termen liber aplicat pe rînd fiecărei țări UE; stînga: diferențele; dreapta: cele mai mari 12 rapoarte RMSPE după/înainte pe iulie 2025 -- iunie 2026')], h='0.63\\textheight')

interp(('the Romanian placebos', 'testelor placebo pentru România'), [
    T(r'Romania has the largest ratio (@{rp.r}; next @{rp.second}, @{rp.r2}): $p = 1/@{rp.n}$ = @{rp.p}', r'România are cel mai mare raport (@{rp.r}; următoarea @{rp.second}, @{rp.r2}): $p = 1/@{rp.n}$ = @{rp.p}'),
    T('No placebo country shows a jump of this size in July--August 2025: the effect is not a common European shock', 'Nicio țară placebo nu are un salt de această mărime în iulie--august 2025: efectul nu este un șoc european comun'),
    T('The permutation p-value treats Romania as one of 27 exchangeable units; it is a measure of rarity, not a sampling-based confidence statement', 'P-value-ul prin permutare tratează România ca pe una dintre 27 de unități interschimbabile; este o măsură a rarității, nu o afirmație de încredere care decurge din eșantionare'),
    T('Other countries\' measures in the window (tax changes, the end of their own caps) bias the effect towards zero if they raised inflation there', 'Măsurile altor țări din fereastră (schimbări fiscale, încheierea propriilor plafonări) deplasează efectul spre zero dacă au crescut inflația acolo')])

chart(T('How much was the tax?', 'Ponderea componentei fiscale'), 'ats_ch14_ro_tax', 'ATS_ch14_romania', [
    T(r'Left: Romanian HICP and HICP at constant tax rates (\refEuroCT); right: the total gap, the gap of the constant-tax inflation (same demeaned SC on all countries) and the tax wedge', r'Stînga: IAPC al României și IAPC la cote de taxare constante (\refEuroCT); dreapta: diferența totală, diferența inflației la taxe constante (același SC cu termen liber pe toate țările) și componenta fiscală')], h='0.62\\textheight')

interp(('the tax decomposition', 'descompunerii fiscale'), [
    T(r'The constant-tax index assumes full and immediate pass-through of tax changes: the tax wedge jumps by @{rt.aug} pp in August 2025, when the VAT rose', r'Indicele la taxe constante presupune transmiterea completă și imediată a modificărilor fiscale: componenta fiscală crește cu @{rt.aug} pp în august 2025, cînd a crescut TVA'),
    T(r'Average over twelve months: total @{rt.tot} pp = tax wedge @{rt.tax} pp + constant-tax gap @{rt.ct} pp: about @{rt.share}\% of the effect is mechanical tax', r'Media pe douăsprezece luni: total @{rt.tot} pp = componenta fiscală @{rt.tax} pp + diferența la taxe constante @{rt.ct} pp: aproximativ @{rt.share}\% din efect este fiscal mecanic'),
    T(r'The non-tax part peaks in July 2025 (@{rt.ctjul} pp): the end of the electricity cap, which is a price, not a tax', r'Partea nefiscală are maximul în iulie 2025 (@{rt.ctjul} pp): încheierea plafonării electricității, care este un preț, nu o taxă'),
    T(r'Pass-through of VAT to consumer prices is often incomplete and asymmetric \refBMKW; the constant-tax index is an accounting benchmark, not a measured pass-through', r'Transmiterea TVA în prețurile de consum este adesea incompletă și asimetrică \refBMKW; indicele la taxe constante este un reper contabil, nu o transmitere măsurată')])

D.frame(T('Staggered adoption and two-way fixed effects (1/2)', 'Adoptarea eșalonată și efectele fixe bidirecționale (1/2)'), items(
    (T(r'Many units adopt at different dates $g$ (their cohort); the static TWFE regression', r'Multe unități adoptă la date diferite $g$ (cohorta lor); regresia TWFE statică'),
     [r'\[ Y_{it} = \alpha_i + \beta_t + \tau D_{it} + u_{it} \]',
      T(r'$D_{it} = 1$ if unit $i$ is treated at $t$; $\alpha_i$, $\beta_t$: unit and period fixed effects; $\tau$: a single treatment effect', r'$D_{it} = 1$ dacă unitatea $i$ este tratată la $t$; $\alpha_i$, $\beta_t$: efectele fixe ale unităților și ale perioadelor; $\tau$: un singur efect al tratamentului')]),
    (T(r'\refGB: $\hat\tau$ is a weighted average of all 2$\times$2 DiDs', r'\refGB: $\hat\tau$ este o medie ponderată a tuturor DiD 2$\times$2'),
     [T(r'including ``forbidden\'\' ones that use already-treated units as controls', r'inclusiv a celor „interzise”, care folosesc unități deja tratate drept control'),
      T(r'with effects that grow over time some weights are negative \refdCDH: $\hat\tau$ can even have the wrong sign', r'cu efecte care cresc în timp, unele ponderi sînt negative \refdCDH: $\hat\tau$ poate avea chiar semnul greșit')])), 'small')

D.frame(T('Staggered adoption and two-way fixed effects (2/2)', 'Adoptarea eșalonată și efectele fixe bidirecționale (2/2)'), items(
    (T(r'\refCSA: group-time effects, each compared only with never-treated units', r'\refCSA: efecte pe grup și perioadă, fiecare comparat doar cu unitățile niciodată tratate'),
     [r'\[ ATT(g, t) = \E[Y_t - Y_{g-1}\mid G = g] - \E[Y_t - Y_{g-1}\mid \text{' + T('never treated', 'niciodată tratat') + r'}] \]',
      T(r'$G$: the adoption date of a unit; $Y_{g-1}$: the outcome in the last period before adoption; $ATT$: average treatment effect on the treated', r'$G$: data de adoptare a unei unități; $Y_{g-1}$: rezultatul din ultima perioadă dinaintea adoptării; $ATT$: efectul mediu al tratamentului asupra unităților tratate'),
      T('then aggregate by exposure ($t - g$) or by cohort', 'apoi agregare după expunere ($t - g$) sau după cohortă')]),
    (T(r'Related: interaction-weighted event studies \refSA; a guide to the new DiD literature \refRSBP', r'Metode înrudite: studii de eveniment ponderate prin interacțiuni \refSA; un ghid al noii literaturi DiD \refRSBP'), []),
    T('Pre-trend tests have low power; report the sensitivity of the effect to violations of parallel trends', 'Testele trendurilor anterioare au putere mică; raportați sensibilitatea efectului la încălcarea trendurilor paralele')), 'small')

chart(T('TWFE against Callaway and Sant\'Anna', 'TWFE față de Callaway și Sant\'Anna'), 'ats_ch14_staggered', 'ATS_ch14_did_dml', [
    T(r'Simulated panel: three cohorts adopting in periods 6, 11 and 16 and a never-treated group; effects grow with exposure, faster for early adopters', r'Panel simulat: trei cohorte care adoptă în perioadele 6, 11 și 16 și un grup niciodată tratat; efectele cresc cu expunerea, mai repede pentru cei care adoptă devreme')], h='0.65\\textheight')

interp(('staggered adoption', 'adoptării eșalonate'), [
    T(r'Static TWFE: @{sg.tw}; true average effect on the treated: @{sg.true}; Callaway--Sant\'Anna: @{sg.cs}', r'TWFE static: @{sg.tw}; efectul mediu real asupra tratatelor: @{sg.true}; Callaway--Sant\'Anna: @{sg.cs}'),
    T(r'TWFE uses early adopters as controls for late adopters while their effect is still growing: those comparisons subtract part of the effect', r'TWFE folosește pe cei care adoptă devreme drept control pentru cei care adoptă tîrziu, în timp ce efectul lor încă crește: aceste comparații scad o parte din efect'),
    T(r'The TWFE event study is distorted at long exposures (binned endpoint @{sg.tw8} against @{sg.true8}); CS gives @{sg.cs8}', r'Studiul de eveniment TWFE este distorsionat la expuneri lungi (capătul grupat @{sg.tw8} față de @{sg.true8}); CS dă @{sg.cs8}'),
    T('With one treated country (Romania) there is no staggering; with EU-wide policies adopted at different dates, there is', 'Cu o singură țară tratată (România) nu există eșalonare; cu politici la nivelul UE adoptate la date diferite, există')])

D.recap(('Beyond synthetic control', 'dincolo de controlul sintetic'), [
    T('An intercept fixes level differences; ridge augmentation corrects the remaining imbalance; SDID combines unit and time weights', 'Termenul liber corectează diferențele de nivel; augmentarea ridge corectează dezechilibrul rămas; SDID combină ponderile unităților și ale perioadelor'),
    T('Romania 2025: @{ro.lo}--@{ro.hi} pp more annual inflation for twelve months, most of it the mechanical VAT effect, and a falsification that holds', 'România 2025: @{ro.lo}--@{ro.hi} pp de inflație anuală în plus timp de douăsprezece luni, în mare parte efectul mecanic al TVA, și o falsificare confirmată'),
    T('Staggered adoption breaks TWFE; use group-time estimators', 'Adoptarea eșalonată invalidează TWFE; folosiți estimatori pe grup și perioadă')])

# =============================================================================
# 6. BSTS ȘI CAUSALIMPACT
# =============================================================================
D.section('Bayesian structural time series and CausalImpact', 'Serii de timp structurale bayesiene și CausalImpact')

D.frame(T('The CausalImpact model (1/2)', 'Modelul CausalImpact (1/2)'), items(
    (T(r'\refCI: the outcome is a trend plus a seasonal component plus a regression on control series', r'\refCI: rezultatul este un trend plus o componentă sezonieră plus o regresie pe serii de control'),
     [r'\[ y_t = \mu_t + \gamma_t + \beta\'x_t + \varepsilon_t, \qquad \mu_{t+1} = \mu_t + \delta_t + \eta_t, \qquad \delta_{t+1} = \delta_t + \zeta_t \]',
      T(r'$\mu_t$: local level; $\delta_t$: local slope; $\gamma_t$: seasonal component; $x_t$: control series with coefficients $\beta$; $\varepsilon_t, \eta_t, \zeta_t$: independent Normal noises', r'$\mu_t$: nivelul local; $\delta_t$: panta locală; $\gamma_t$: componenta sezonieră; $x_t$: serii de control cu coeficienții $\beta$; $\varepsilon_t, \eta_t, \zeta_t$: zgomote independente cu distribuția Normală')]),
    (T(r'A structural time series model \refHar in state space form, filtered and smoothed by Kalman (Chapter 6, \refDK)', r'Un model structural de serii de timp \refHar în formă de spațiu al stărilor, filtrat și netezit prin Kalman (Capitolul 6, \refDK)'),
     [T(r'a spike-and-slab prior on $\beta$ selects the controls \refSV; the posterior is computed by MCMC', r'o distribuție a priori spike-and-slab pe $\beta$ selectează seriile de control \refSV; distribuția a posteriori se calculează prin MCMC')])), 'small')

D.frame(T('The CausalImpact model (2/2)', 'Modelul CausalImpact (2/2)'), items(
    (T(r'Fit on the pre-period; simulate the post-period counterfactual $y^{(s)}_t(0)$ from the posterior predictive, given the observed $x_t$', r'Estimare pe perioada anterioară; se simulează contrafactualul de după $y^{(s)}_t(0)$ din distribuția predictivă a posteriori, dați $x_t$ observați'),
     [T(r'$s$: the index of a simulated path; effects $y_t - y^{(s)}_t(0)$, pointwise and cumulative', r'$s$: indicele unei traiectorii simulate; efectele $y_t - y^{(s)}_t(0)$, punctuale și cumulate'),
      T('credible intervals from the quantiles of the simulated effects', 'intervale de credibilitate din cuantilele efectelor simulate')]),
    (T(r'\textbf{Identification}', r'\textbf{Identificarea}'),
     [T(r'the controls are \textbf{not affected} by the treatment', r'seriile de control \textbf{nu sînt afectate} de tratament'),
      T(r'their relation with $y$ is stable after $T_0$', r'relația lor cu $y$ rămîne stabilă după $T_0$')])), 'small')

D.frame(T('Our implementation', 'Implementarea folosită'), items(
    (T(r'\texttt{statsmodels} \texttt{UnobservedComponents}: local level + regression on the controls, maximum likelihood on the pre-period', r'\texttt{statsmodels} \texttt{UnobservedComponents}: nivel local + regresie pe seriile de control, verosimilitate maximă pe perioada anterioară'),
     [T(r'@{bt.draws} counterfactual paths: parameters drawn from their asymptotic normal distribution, then the state simulated forward from the end of the pre-period given the observed controls', r'@{bt.draws} de traiectorii contrafactuale: parametrii extrași din distribuția lor normală asimptotică, apoi starea simulată înainte de la sfîrșitul perioadei anterioare, dați seriile de control observate')]),
    (T('Differences from the R package: no spike-and-slab selection, no MCMC; parameter uncertainty by a Gaussian approximation', 'Diferențe față de pachetul R: fără selecție spike-and-slab, fără MCMC; incertitudinea parametrilor printr-o aproximare gaussiană'),
     [T('the transparent version keeps every step visible; with few controls the two give similar intervals', 'versiunea transparentă păstrează fiecare pas vizibil; cu puține serii de control cele două dau intervale asemănătoare')]),
    T('Outputs: average effect with a 95\\% interval, cumulative effect, and the tail probability that the counterfactual mean exceeds the observed one', 'Rezultate: efectul mediu cu un interval de 95\\%, efectul cumulat și probabilitatea din coadă ca media contrafactuală să depășească media observată')), 'small')

D.frame(T('Case study: the US spot Bitcoin ETFs', 'Studiu de caz: ETF-urile spot pe Bitcoin din SUA'), two(
    ph('atm', T('A Bitcoin ATM, Prague', 'Un bancomat Bitcoin, Praga'), h='0.40\\textheight'),
    items((T(r'\textbf{10 January 2024} \refSEC', r'\textbf{10 ianuarie 2024} \refSEC'),
           [T('the SEC approves eleven spot Bitcoin ETPs (exchange-traded products); trading starts on 11 January', 'SEC aprobă unsprezece ETP-uri (produse tranzacționate la bursă) spot pe Bitcoin; tranzacționarea începe pe 11 ianuarie')]),
          (T('Question', 'Întrebarea'),
           [T('did the approval change Bitcoin volatility (institutional demand, arbitrage between spot and ETF)?', 'a schimbat aprobarea volatilitatea Bitcoin (cererea instituțională, arbitrajul între spot și ETF)?')]),
          (T('Design', 'Designul'),
           [T('outcome: weekly log realised variance of Bitcoin', 'rezultatul: logaritmul varianței realizate săptămînale a Bitcoin'),
            T(r'controls: the same measure for the S\&P 500, Nasdaq 100, gold and EUR/USD', r'serii de control: aceeași măsură pentru S\&P 500, Nasdaq 100, aur și EUR/USD'),
            T(r'pre-period January 2023 -- 7 January 2024 (@{bt.npre} weeks); post: @{bt.npost} weeks to June 2024', r'perioada anterioară ianuarie 2023 -- 7 ianuarie 2024 (@{bt.npre} de săptămîni); după: @{bt.npost} de săptămîni pînă în iunie 2024')]),
          (T('Anticipation (dotted lines)', 'Anticipare (liniile punctate)'),
           [T('BlackRock filed on 15 June 2023; a court ruled for Grayscale on 29 August 2023', 'BlackRock a depus cererea pe 15 iunie 2023; o instanță a decis în favoarea Grayscale pe 29 august 2023')])), '0.34', '0.64'), 'small')

chart(T('CausalImpact for the spot ETF approval', 'CausalImpact pentru aprobarea ETF-urilor spot'), 'ats_ch14_btc', 'ATS_ch14_causalimpact', [
    T('Top: observed and counterfactual log RV with a 95\\% interval; middle: pointwise effect; bottom: cumulative effect', 'Sus: log RV observat și contrafactual, cu interval de 95\\%; mijloc: efectul punctual; jos: efectul cumulat')], h='0.68\\textheight')

interp(('the ETF analysis', 'analizei ETF'), [
    T(r'Average effect on weekly log RV: @{bt.avg} (95\% interval [@{bt.lo}, @{bt.hi}]), tail probability @{bt.p}: no detectable change', r'Efectul mediu asupra log RV săptămînal: @{bt.avg} (interval de 95\% [@{bt.lo}, @{bt.hi}]), probabilitatea din coadă @{bt.p}: nicio schimbare detectabilă'),
    T(r'The level variance is small (@{bt.s2l}) against the irregular one (@{bt.s2e}): weekly crypto volatility is mostly noise, and the controls explain little', r'Varianța nivelului este mică (@{bt.s2l}) față de cea neregulată (@{bt.s2e}): volatilitatea cripto săptămînală este în mare parte zgomot, iar seriile de control explică puțin'),
    T(r'The finding agrees with a peer-reviewed study: no effect on Bitcoin\'s own volatility \refBBG', r'Rezultatul este în acord cu un studiu publicat: niciun efect asupra volatilității proprii a Bitcoin \refBBG'),
    T('Absence of evidence is not evidence of absence: with this noise, a 50\\% change in volatility would not be detected', 'Lipsa dovezilor nu este dovada lipsei: cu acest zgomot, o modificare de 50\\% a volatilității nu ar fi detectată')])

chart(T('Placebo dates and the choice of controls', 'Date placebo și alegerea seriilor de control'), 'ats_ch14_btc_placebo', 'ATS_ch14_causalimpact', [
    T(r'The same analysis with @{bp.n} fictitious approval dates in 2019--2022 (53 pre-weeks, 25 post-weeks each) and the true date with the same window lengths', r'Aceeași analiză cu @{bp.n} date fictive de aprobare în 2019--2022 (cîte 53 de săptămîni înainte și 25 după) și data reală cu aceleași lungimi ale ferestrelor')], h='0.65\\textheight')

interp(('the placebo dates', 'datelor placebo'), [
    T(r'Only @{bp.ex} of the @{bp.n} placebo intervals @{bp.verb_en} zero; the placebo estimates have a standard deviation of @{bp.sd}: the real estimate is inside their range', r'Doar @{bp.ex} dintre cele @{bp.n} intervale placebo @{bp.verb_ro} zero; estimațiile placebo au abaterea standard @{bp.sd}: estimația reală se află în domeniul lor'),
    T(r'With Ether as an extra control: @{bt.eth} [@{bt.ethlo}, @{bt.ethhi}]; but Ether may itself respond to the approval: a treated control biases the effect towards zero', r'Cu Ether ca serie de control suplimentară: @{bt.eth} [@{bt.ethlo}, @{bt.ethhi}]; dar Ether poate răspunde el însuși la aprobare: un control tratat deplasează efectul spre zero'),
    T(r'Moving $T_0$ back to the BlackRock filing (June 2023): @{bt.ant} [@{bt.antlo}, @{bt.anthi}]: still nothing, so anticipation does not hide a large effect', r'Mutarea lui $T_0$ la depunerea cererii BlackRock (iunie 2023): @{bt.ant} [@{bt.antlo}, @{bt.anthi}]: tot nimic, deci anticiparea nu ascunde un efect mare'),
    T('Placebo dates calibrate the credible intervals: if many placebos look ``significant\'\', the model is misspecified', 'Datele placebo calibrează intervalele de credibilitate: dacă multe teste placebo par „semnificative”, modelul este greșit specificat')])

D.recap(('BSTS and CausalImpact', 'BSTS și CausalImpact'), [
    T('A state space forecast of the untreated path from control series; uncertainty from parameters and states', 'O prognoză în spațiul stărilor a traiectoriei netratate pe baza seriilor de control; incertitudinea vine din parametri și din stări'),
    T('Its key assumption is about the controls: unaffected and stably related; check with placebo dates', 'Ipoteza esențială privește seriile de control: neafectate și într-o relație stabilă; verificați cu date placebo'),
    T('The spot ETF approval did not change Bitcoin volatility detectably; the design could not see small effects', 'Aprobarea ETF-urilor spot nu a schimbat detectabil volatilitatea Bitcoin; designul nu ar fi putut vedea efecte mici')])

# =============================================================================
# 7. DML ȘI IDENTIFICARE ONESTĂ
# =============================================================================
D.section('Double machine learning and honest identification', 'Double machine learning și identificarea onestă')

D.frame(T('Double/debiased machine learning for time series (1/2)', 'Double/debiased machine learning pentru serii de timp (1/2)'), items(
    (T(r'\refDML: the \textbf{partially linear model}', r'\refDML: \textbf{modelul parțial liniar}'),
     [r'\[ y_t = \theta d_t + g(X_t) + u_t, \qquad d_t = m(X_t) + v_t \]',
      T(r'$d_t$: the treatment; $\theta$: its effect; $X_t$: control variables; $g$, $m$: unknown \textbf{nuisance functions}, learned by machine learning; $u_t, v_t$: errors',
        r'$d_t$: tratamentul; $\theta$: efectul lui; $X_t$: variabilele de control; $g$, $m$: \textbf{funcții auxiliare} necunoscute, învățate prin machine learning; $u_t, v_t$: erori')]),
    (T(r'\textbf{Orthogonal score}: regress the residual of $y$ on the residual of $d$', r'\textbf{Scorul ortogonal}: se regresează reziduul lui $y$ pe reziduul lui $d$'),
     [r'\[ \psi = \big(y_t - \ell(X_t) - \theta(d_t - m(X_t))\big)\big(d_t - m(X_t)\big), \qquad \ell(X) = \E[y\mid X] \]',
      T(r'$\hat\theta$ solves $\frac1T\sum_t\psi_t = 0$; first-order insensitive to errors in $\ell$ and $m$', r'$\hat\theta$ rezolvă $\frac1T\sum_t\psi_t = 0$; insensibil de ordinul întîi la erorile din $\ell$ și $m$')])), 'small')

D.frame(T('Double/debiased machine learning for time series (2/2)', 'Double/debiased machine learning pentru serii de timp (2/2)'), items(
    (T(r'\textbf{Cross-fitting}: the nuisance functions are fitted on other folds than the one where $\psi$ is evaluated', r'\textbf{Cross-fitting}: funcțiile auxiliare sînt estimate pe alte subeșantioane decît cel pe care se evaluează $\psi$'),
     [T(r'for time series use \textbf{contiguous blocks} with a gap around the held-out block', r'pentru serii de timp se folosesc \textbf{blocuri contigue}, cu un interval de separare în jurul blocului omis'),
      T(r'standard error from a HAC variance of $\psi$', r'eroarea standard dintr-o varianță HAC a lui $\psi$')]),
    (T('DML removes regularisation and overfitting bias; it does not create identification', 'DML elimină deplasarea din regularizare și supraajustare; nu creează identificare'),
     [T(r'$d_t$ must be unconfounded given $X_t$', r'$d_t$ trebuie să fie neconfundat, dat $X_t$')])), 'small')

chart(T('DML against a linear adjustment', 'DML față de o ajustare liniară'), 'ats_ch14_dml', 'ATS_ch14_did_dml', [
    T(r'Simulated dependent data: 10 VAR(1) covariates, nonlinear $g$ and $m$, AR(1) errors, $\theta = 0.5$, $T = @{dml.T}$, @{dml.reps} replications; random forests with five blocked folds', r'Date dependente simulate: 10 covariate VAR(1), $g$ și $m$ neliniare, erori AR(1), $\theta = 0{,}5$, $T = @{dml.T}$, @{dml.reps} de repetări; păduri aleatoare cu cinci blocuri')], h='0.65\\textheight')

interp(('the DML experiment', 'experimentului DML'), [
    T(r'OLS with linear controls: mean estimate @{dml.ols}, far from 0.5: the nonlinear confounding is not removed', r'OLS cu controale liniare: estimația medie @{dml.ols}, departe de 0,5: confuzia neliniară nu este eliminată'),
    T(r'DML: mean @{dml.dml}, standard deviation @{dml.sd}; 95\% HAC intervals cover the true value in @{dml.cov}\% of the replications', r'DML: media @{dml.dml}, abaterea standard @{dml.sd}; intervalele HAC de 95\% acoperă valoarea reală în @{dml.cov}\% din repetări'),
    T('The remaining bias comes from the forests\' errors on a finite sample; it shrinks with $T$', 'Deplasarea rămasă provine din erorile pădurilor pe un eșantion finit; scade cînd $T$ crește'),
    T('In macro time series the treatment is rarely unconfounded given observables: DML is a tool for the estimation step, after identification is argued', 'În seriile de timp macro, tratamentul este rar neconfundat, dați factorii observați: DML este un instrument pentru etapa de estimare, după ce identificarea a fost argumentată')])

D.frame(T('Identification, method by method', 'Identificarea, metodă cu metodă'), table(
    TB + 'p{2.6cm}' + TB + 'p{5.4cm}' + TB + 'p{4.4cm}',
    T(r'\textbf{Method} & \textbf{Key assumption} & \textbf{Check}', r'\textbf{Metoda} & \textbf{Ipoteza esențială} & \textbf{Verificarea}'),
    [T('Granger, PCMCI', 'Granger, PCMCI') + ' & ' + T('no hidden common causes; correct timing; faithfulness', 'nicio cauză comună ascunsă; momentul observării corect; fidelitate') + ' & ' + T('add candidate confounders; change the frequency', 'adăugați posibili factori de confuzie; schimbați frecvența'),
     T('ITS, event study', 'ITS, studiu de eveniment') + ' & ' + T('nothing else changes at $T_0$; no anticipation', 'nimic altceva nu se schimbă la $T_0$; nicio anticipare') + ' & ' + T('placebo dates; news timeline', 'date placebo; cronologia știrilor'),
     T('Synthetic control, SDID', 'Control sintetic, SDID') + ' & ' + T('factor model; donors unaffected; treated unit in the donors\' range', 'model factorial; donatori neafectați; unitatea tratată în domeniul donatorilor') + ' & ' + T('pre-fit, placebos, leave-one-out', 'potrivirea anterioară, placebo, omiterea pe rînd'),
     T('DiD (staggered)', 'DiD (eșalonat)') + ' & ' + T('parallel trends; no anticipation', 'trenduri paralele; nicio anticipare') + ' & ' + T('pre-trends with sensitivity analysis', 'trenduri anterioare cu analiză de sensibilitate'),
     'CausalImpact & ' + T('controls unaffected; stable relation', 'controale neafectate; relație stabilă') + ' & ' + T('placebo dates; alternative control sets', 'date placebo; alte seturi de controale'),
     'SVAR, LP, DML & ' + T('as good as random given the past or an instrument', 'la fel de bun ca aleator, dat trecutul sau un instrument') + ' & ' + T('narrative evidence; instrument strength', 'dovezi narative; puterea instrumentului')],
    size='scriptsize'), 'small')

D.frame(T('Honest reporting', 'Raportarea onestă'), items(
    T('State the estimand (which effect, on which unit, over which horizon) before choosing the method', 'Precizați mărimea țintă (ce efect, asupra cărei unități, pe ce orizont) înainte de a alege metoda'),
    T('Fix treatment dates, windows, donors and estimators before looking at post-treatment data; publish the pre-registration', 'Fixați datele tratamentului, ferestrele, donatorii și estimatorii înainte de a privi datele de după tratament; publicați preînregistrarea'),
    T('Report every placebo, every specification and every deviation from the published design; a specification curve shows them together', 'Raportați fiecare placebo, fiecare specificație și fiecare abatere de la designul publicat; o curbă a specificațiilor le arată împreună'),
    T('Separate statistical uncertainty (intervals) from identification uncertainty (assumptions); the second is usually larger', 'Separați incertitudinea statistică (intervalele) de incertitudinea identificării (ipotezele); a doua este de obicei mai mare'),
    T(r'Read \refAI and \refAba before writing a policy evaluation', r'Citiți \refAI și \refAba înainte de a scrie o evaluare de politică')), 'small')

# =============================================================================
# AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('The question', 'Întrebarea'),
     [T('how much of Romania\'s 2025--2026 inflation surge was caused by the end of the electricity cap and the VAT increase?', 'cît din creșterea inflației din România în 2025--2026 a fost cauzată de încheierea plafonării electricității și de majorarea TVA?'),
      T('how robust is the answer to the choice of method?', 'cît de robust este răspunsul la alegerea metodei?')]),
    (T('A testable form', 'O formă testabilă'),
     [T(r'formal: $H_0$: the average gap over July 2025 -- June 2026 is zero; the claim ``between 2 and 3.5 pp\'\' must hold for every pre-registered estimator with a good pre-fit', r'formal: $H_0$: diferența medie pe iulie 2025 -- iunie 2026 este zero; afirmația „între 2 și 3,5 pp” trebuie să fie valabilă pentru orice estimator preînregistrat cu potrivire anterioară bună'),
      T('falsified if a reasonable specification gives less than 2 pp or a placebo country matches Romania', 'infirmată dacă o specificație rezonabilă dă mai puțin de 2 pp sau dacă o țară placebo egalează România')]),
    (T('Why it matters', 'Miza'),
     [T('monetary policy must tell one-off price-level effects from persistent inflation', 'politica monetară trebuie să distingă efectele unice asupra nivelului prețurilor de inflația persistentă'),
      T('second-round effects decide interest rates', 'efectele de runda a doua determină deciziile privind dobînzile'),
      T(r'literature to start from: \refADHb, \refASCM, \refSDID, \refBMKW', r'literatura de pornire: \refADHb, \refASCM, \refSDID, \refBMKW')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed studies since 2015 that estimate VAT pass-through to consumer prices with synthetic control or DiD; give DOIs and the estimated pass-through.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează studii recenzate din 2015 încoace care estimează transmiterea TVA în prețurile de consum cu control sintetic sau DiD; dă DOI-urile și transmiterea estimată.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{design}: \aiprompt{Write a pre-registration: outcome, donors, exclusions, pre-period, estimators, placebo tests, what counts as a robust effect.}', r'\textbf{designul}: \aiprompt{Scrie o preînregistrare: rezultatul, donatorii, excluderile, perioada anterioară, estimatorii, testele placebo, ce înseamnă un efect robust.}'),
      T(r'\textbf{code and replication}: reproduce first the German weights (Austria @{ge.w.austria}; USA @{ge.w.usa}; ...) before running anything on Romania', r'\textbf{cod și replicare}: reproduceți întîi ponderile germane (Austria @{ge.w.austria}; SUA @{ge.w.usa}; ...) înainte de a rula ceva pe România'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee: which EU countries had their own energy or tax measures in 2025--2026, and how would each bias the estimate?}', r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil: ce țări UE au avut propriile măsuri de energie sau fiscale în 2025--2026 și cum ar deplasa fiecare estimația?}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('Policy dates are taken from official sources (Monitorul Oficial, Eurostat, SEC), not from the assistant\'s memory', 'Datele politicilor se iau din surse oficiale (Monitorul Oficial, Eurostat, SEC), nu din memoria asistentului'),
    T('The donor pool excludes countries with their own large shocks in the window, and the exclusions are written before the results are seen', 'Grupul donatorilor exclude țările cu propriile șocuri mari în fereastră, iar excluderile sînt scrise înainte de a vedea rezultatele'),
    T('Placebo tests are run with exactly the same code and settings as the main estimate', 'Testele placebo sînt rulate cu exact același cod și aceleași setări ca estimația principală'),
    T('An AI claim that ``the synthetic control proves the VAT caused 3 pp of inflation\'\' is rewritten as an estimate with assumptions', 'O afirmație AI de tipul „controlul sintetic dovedește că TVA a cauzat 3 pp de inflație” se reformulează ca o estimație cu ipoteze')), 'small')

chart(T('Mini-case: a specification curve for Romania', 'Mini studiu de caz: curba specificațiilor pentru România'), 'ats_ch14_ai_case', 'ATS_ch14_ai_case', [
    T(r'@{ai.n} specifications: four estimators $\times$ three donor pools (EU-26, euro area, non-euro EU) $\times$ four pre-periods (from 2017, 2019, July 2023, 2024; the 2021--2023 surge excluded)', r'@{ai.n} de specificații: patru estimatori $\times$ trei grupuri de donatori (UE-26, zona euro, UE din afara zonei euro) $\times$ patru perioade anterioare (din 2017, 2019, iulie 2023, 2024; valul 2021--2023 exclus)'),
    T(r'Without classic SC: from @{ai.min} to @{ai.max} pp, median @{ai.med}; classic SC: median @{ai.sc} (poor pre-fit); @{ai.neg} specifications give a non-positive effect: the hypothesis survives', r'Fără SC clasic: între @{ai.min} și @{ai.max} pp, mediana @{ai.med}; SC clasic: mediana @{ai.sc} (potrivire anterioară slabă); @{ai.neg} specificații dau un efect nepozitiv: ipoteza rezistă')],
    h='0.56\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Tax pass-through in Central and Eastern Europe with synthetic controls}: replicate first, then extend', r'\textbf{Transmiterea taxelor în Europa Centrală și de Est cu controale sintetice}: întîi replicare, apoi extindere'),
     [T(r'replicate: \refADHb (Table 1, Figures 2--5) with the public data, then this chapter\'s Romanian estimate', r'replicați: \refADHb (tabelul 1, figurile 2--5) cu datele publice, apoi estimația pentru România din acest capitol'),
      T('extend: product-level HICP (food, energy, services) to measure pass-through by VAT rate', 'extindeți: IAPC pe grupe de produse (alimente, energie, servicii) pentru a măsura transmiterea pe cote de TVA'),
      T('other episodes (Hungary 2012, Croatia 2023 euro adoption); conformal intervals \\refCWZ', 'alte episoade (Ungaria 2012, adoptarea euro în Croația în 2023); intervale conformale \\refCWZ'),
      T('pre-register: donors and exclusions, windows, estimators, placebos, the robustness rule', 'preînregistrați: donatorii și excluderile, ferestrele, estimatorii, testele placebo, regula de robustețe')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Granger causality and its relatives (TE, PCMCI, CCM) describe predictive structure; causal claims need assumptions about the assignment', 'Cauzalitatea Granger și metodele înrudite (TE, PCMCI, CCM) descriu structura predictivă; afirmațiile cauzale cer ipoteze despre alocarea tratamentului'),
    T('Interrupted series and event studies use the unit\'s own past; dependence enlarges their standard errors', 'Seriile întrerupte și studiile de eveniment folosesc propriul trecut al unității; dependența le mărește erorile standard'),
    T('Synthetic control and its successors use other units; placebos are the inference, a long pre-fit is the justification', 'Controlul sintetic și succesorii lui folosesc alte unități; testele placebo sînt inferența, potrivirea pe o perioadă lungă este justificarea'),
    T('Replication exposes fragility: German reunification holds, the Brexit gap depends on data vintage', 'Replicarea arată fragilitatea: rezultatul reunificării Germaniei se menține, diferența Brexit depinde de ediția datelor'),
    T('Romania 2025: a robust @{ro.lo}--@{ro.hi} pp twelve-month effect, mostly mechanical VAT; Bitcoin ETFs: no detectable effect on volatility', 'România 2025: un efect robust de @{ro.lo}--@{ro.hi} pp pe douăsprezece luni, în mare parte TVA mecanic; ETF-urile Bitcoin: niciun efect detectabil asupra volatilității')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('Why can adding a variable to the information set remove a Granger causality?', 'De ce poate adăugarea unei variabile la mulțimea de informație să elimine o cauzalitate Granger?'),
        T('What does conditioning on the parents of the source achieve in the MCI test?', 'Ce obține condiționarea pe părinții sursei în testul MCI?'),
        T('Why does classic synthetic control fail for Romanian inflation?', 'De ce eșuează controlul sintetic clasic pentru inflația României?'),
        T('What is the smallest placebo p-value with 23 donors?', 'Care este cel mai mic p-value placebo cu 23 de donatori?'),
        T('Why can a static TWFE estimate have the wrong sign under staggered adoption?', 'De ce poate o estimație TWFE statică să aibă semnul greșit în cazul adoptării eșalonate?'))),
    block(T('Next: Chapter 15', 'Urmează: Capitolul 15'), items(
        T('Review and project defence', 'Recapitulare și susținerea proiectelor'),
        T('one synthesis per chapter; the replication project and the oral defence', 'o sinteză pentru fiecare capitol; proiectul de replicare și susținerea orală'))),
    '0.58', '0.38'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the bias bound of synthetic control', 'Anexă: marginea deplasării controlului sintetic'), items(
    T(r'Factor model $Y_{jt}(0) = \delta_t + \lambda_t\mu_j + \varepsilon_{jt}$ ($F$ factors); weights with $\sum_jw_jY_{jt} = Y_{1t}$, $t \le T_0$', r'Modelul factorial $Y_{jt}(0) = \delta_t + \lambda_t\mu_j + \varepsilon_{jt}$ ($F$ factori); ponderi cu $\sum_jw_jY_{jt} = Y_{1t}$, $t \le T_0$'),
    T(r'Stack the pre-period: $\lambda^P(\mu_1 - \sum_jw_j\mu_j) = -(\varepsilon^P_1 - \sum_jw_j\varepsilon^P_j)$; if $\lambda^{P\prime}\lambda^P$ is invertible, solve for the loading imbalance', r'Stivuim perioada anterioară: $\lambda^P(\mu_1 - \sum_jw_j\mu_j) = -(\varepsilon^P_1 - \sum_jw_j\varepsilon^P_j)$; dacă $\lambda^{P\prime}\lambda^P$ este inversabilă, obținem dezechilibrul încărcărilor'),
    T(r'Then $Y_{1t}(0) - \sum_jw_jY_{jt} = \lambda_t(\lambda^{P\prime}\lambda^P)^{-1}\lambda^{P\prime}\sum_jw_j\varepsilon^P_j - \dots + (\varepsilon_{1t} - \sum_jw_j\varepsilon_{jt})$', r'Atunci $Y_{1t}(0) - \sum_jw_jY_{jt} = \lambda_t(\lambda^{P\prime}\lambda^P)^{-1}\lambda^{P\prime}\sum_jw_j\varepsilon^P_j - \dots + (\varepsilon_{1t} - \sum_jw_j\varepsilon_{jt})$'),
    T(r'The first term has mean zero only approximately (the weights depend on the $\varepsilon^P$); ADH (2010, Appendix B) bound it by a quantity of order $J^{1/p}\bar m_p^{1/p}F\,\bar\lambda^2/(\xi T_0^{1 - 1/p})$: small when $T_0$ is large relative to $J$', r'Primul termen are media zero doar aproximativ (ponderile depind de $\varepsilon^P$); ADH (2010, anexa B) îl mărginesc printr-o mărime de ordinul $J^{1/p}\bar m_p^{1/p}F\,\bar\lambda^2/(\xi T_0^{1 - 1/p})$: mică atunci cînd $T_0$ este mare relativ la $J$')), 'small')

D.frame(T('Appendix: Gaussian transfer entropy equals half the Geweke measure', 'Anexă: entropia de transfer gaussiană este jumătate din măsura Geweke'), items(
    T(r'For jointly Gaussian variables $I(Y; X\mid Z) = \frac12\ln\dfrac{\mathrm{Var}(Y\mid Z)}{\mathrm{Var}(Y\mid X, Z)}$ (the entropy of a Gaussian is $\frac12\ln(2\pi e\sigma^2)$)', r'Pentru variabile gaussiene comune, $I(Y; X\mid Z) = \frac12\ln\dfrac{\mathrm{Var}(Y\mid Z)}{\mathrm{Var}(Y\mid X, Z)}$ (entropia unei variabile gaussiene este $\frac12\ln(2\pi e\sigma^2)$)'),
    T(r'With $Y = y_t$, $X = x^{(l)}_{t-1}$, $Z = y^{(k)}_{t-1}$, the conditional variances are the residual variances of the restricted and full Granger regressions', r'Cu $Y = y_t$, $X = x^{(l)}_{t-1}$, $Z = y^{(k)}_{t-1}$, varianțele condiționate sînt varianțele reziduale ale regresiilor Granger restrînsă și completă'),
    T(r'Hence $TE_{x\to y} = \frac12F_{x\to y}$, and $2T\cdot\widehat{TE} \approx T\hat F \approx W$, the likelihood-ratio form of the Granger Wald test \refBBS', r'Deci $TE_{x\to y} = \frac12F_{x\to y}$, iar $2T\cdot\widehat{TE} \approx T\hat F \approx W$, forma de raport de verosimilitate a testului Wald Granger \refBBS'),
    T('Non-Gaussian data break the equality: TE then detects dependence that a linear test misses (Section 1)', 'Datele negaussiene anulează egalitatea: TE detectează atunci dependențe pe care un test liniar le ratează (secțiunea 1)')), 'small')

D.references(bib(), per=14)

if __name__ == '__main__':
    finalize(D.write(V))
    run_acronyms(14)   # the glossary again, after the bilingual values are resolved
