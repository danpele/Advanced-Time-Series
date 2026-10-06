r"""
build_chapter3.py -- Capitolul 3 (Modele VAR structurale și proiecții locale), EN + RO
=====================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_03/ch3_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice). TSA, Capitolul 6 a predat VAR în formă redusă, cauzalitatea
Granger, răspunsurile Cholesky și FEVD; aici construim identificarea structurală și proiecțiile locale.
Ieșire:
  EN/Courses/chapter3_structural_var_local_projections.tex
  RO/Cursuri/capitol3_modele_var_structurale_proiectii_locale.tex
Rulare:
  python3 Quantlets/Ch_03/generate_all_charts.py
  python3 latex/build_chapter3.py && python3 latex/ats_build.py compile 3
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch3_common import REFS, QLURL, T, bib, finalize, load, minus_fix, pv, month   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(3, 'lecture', refs=REFS)
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
    'sims': ('ch3_sims_nobel_lecture_2011.jpg', C + 'Nobel_Prize_2011-Nobel_lectures_KVA-DSC_8085.jpg',
             FOTO + ': Holger Motzkau (2011); CC BY-SA 3.0; Wikimedia Commons'),
    'volcker': ('ch3_volcker_2014.jpg', C + 'Paul_Volcker_-_2014_(13896577879)_(cropped).jpg',
                FOTO + ': Federal Reserve (2014); ' + PD + '; Wikimedia Commons'),
    'kuwait': ('ch3_kuwait_oil_fires_1991.jpg', C + 'Disabled_Iraqi_T-54A,_T-55,_Type_59_or_Type_69_tank_and_burning_Kuwaiti_oil_field.jpg',
               FOTO + ': JO1 Gawlowicz, US Navy (1991); ' + PD + '; Wikimedia Commons'),
    'bnr': ('ch0_bnr_palace_2015.jpg', C + 'Bucharest_-_BNR_Palace_(19644434340).jpg',
            FOTO + ': Ștefan Jurcă (2015); CC BY 2.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


# =============================================================================
# CIFRE
# =============================================================================
c = N['cee']
V.int('cee.T', c['T'])
P('cee.sd', c['sd'], 2)
P('cee.ipmin', c['ip_min'], 2)
V.raw('cee.iparg', str(c['ip_argmin']))
P('cee.iplo', c['ip_lo'], 2)
P('cee.iphi', c['ip_hi'], 2)
P('cee.pmax', c['p_max'], 3)
V.raw('cee.parg', str(c['p_argmax']))
P('cee.p48', c['p48'], 2)
P('cee.p48lo', c['p48_lo'], 2)
P('cee.p48hi', c['p48_hi'], 2)
P('cee.umax', c['u_max'], 2)
P('cee.fe24', 100 * c['fevd_ip24'], 1)
P('cee.fe48', 100 * c['fevd_ip48'], 1)
P('cee.feffr24', 100 * c['fevd_ffr24'], 0)
P('cee.root', c['root'], 4)
V.raw('cee.B', str(c['B']))
k = N['kilian']
V.raw('kil.T', str(k['T']))
V.raw('kil.first', month(k['first']))
V.raw('kil.T2', str(k['T2']))
V.raw('kil.last2', month(k['last2']))
for a in ('sup_p0', 'sup_p12', 'sup_p12_lo', 'sup_p12_hi', 'ad_p0', 'ad_p12', 'ad_p12_lo', 'ad_p12_hi', 'os_p0', 'os_p12',
          'os_p12_lo', 'sup_q0', 'ad_p12_2', 'os_p12_2', 'sup_p12_2'):
    P(f'kil.{a}', k[a], 1)
for i, s in enumerate(('sup', 'ad', 'os')):
    P(f'kil.fe.{s}', 100 * k['fevd_p60'][i], 0)
P('kil.root', k['root'], 3)
hd = N['kilian_hd']
for per in ('c2003_2008', 'c2008_2009', 'c2020', 'c2022'):
    for s in ('sup', 'ad', 'os'):
        P(f'hd.{per}.{s}', hd[per][s], 0)
kb = N['kbias']
P('kb.p12', kb['p12'][2], 2)
P('kb.p12c', kb['p12c'][2], 2)
P('kb.ad12', kb['p12'][1], 2)
P('kb.ad12c', kb['p12c'][1], 2)
P('kb.lo', kb['p12c_lo'][2], 1)
P('kb.hi', kb['p12c_hi'][2], 1)
P('kb.root', kb['root'], 3)
P('kb.rootc', kb['root_c'], 4)
P('kb.mean', kb['bias_mean'], 3)
b = N['bq']
V.raw('bq.T', str(b['T']))
P('bq.dpeak', b['dem_y_peak'], 2)
V.raw('bq.dpeakq', str(b['dem_y_argpeak']))
P('bq.dumin', b['dem_u_min'], 2)
V.raw('bq.dumq', str(b['dem_u_argmin']))
P('bq.s40', b['sup_y40'], 2)
P('bq.s40lo', b['sup_y40_lo'], 2)
P('bq.s40hi', b['sup_y40_hi'], 2)
P('bq.su0', b['sup_u0'], 2)
P('bq.fe4', 100 * b['fevd_y4_dem'], 0)
P('bq.fe40', 100 * b['fevd_y40_dem'], 0)
P('bq.feu4', 100 * b['fevd_u4_dem'], 0)
r = N['rot']
P('rot.thhi', r['th_hi'], 2)
P('rot.share', 100 * r['share'], 0)
P('rot.plo', r['p_lo'], 2)
P('rot.qlo', r['q_lo'], 2)
P('rot.qhi', r['q_hi'], 2)
u = N['uhlig']
V.int('uh.n', u['n_keep'])
V.int('uh.nd', u['ndraw'])
P('uh.acc', 100 * u['acc_rate'], 1)
P('uh.ip12', u['ip12'], 2)
P('uh.ip12lo', u['ip12_lo'], 2)
P('uh.ip12hi', u['ip12_hi'], 2)
P('uh.neg', 100 * u['ip_share_neg12'], 0)
P('uh.s12lo', u['set12_lo'], 2)
P('uh.s12hi', u['set12_hi'], 2)
P('uh.s0lo', u['set_ip0_lo'], 2)
P('uh.s0hi', u['set_ip0_hi'], 2)
P('uh.p24', u['p24'], 2)
P('uh.ffr0', u['ffr0'], 2)
V.raw('uh.T', str(u['T']))
g = N['gk']
V.raw('gk.T', str(g['T']))
V.raw('gk.Tz', str(g['Tz']))
P('gk.F', g['F'], 1)
P('gk.Fh', g['F_hom'], 1)
P('gk.r2', 100 * g['r2'], 1)
P('gk.ebp0', g['ebp0'], 2)
P('gk.ebp0lo', g['ebp0_lo'], 2)
P('gk.ebp0hi', g['ebp0_hi'], 2)
P('gk.ipmin', g['ip_min'], 2)
V.raw('gk.iparg', str(g['ip_argmin']))
P('gk.ipminlo', g['ip_min_lo'], 2)
P('gk.ipminhi', g['ip_min_hi'], 2)
P('gk.cpi24', g['cpi24'], 2)
P('gk.cpi24lo', g['cpi24_lo'], 2)
P('gk.cpi24hi', g['cpi24_hi'], 2)
P('gk.gs12', g['gs1_12'], 2)
lg = N['lpgk']
P('lg.F0', lg['F0'], 1)
P('lg.ip24', lg['ip24'], 2)
P('lg.ip24se', lg['ip24_se'], 2)
P('lg.cpi24', lg['cpi24'], 2)
P('lg.cpi24se', lg['cpi24_se'], 2)
P('lg.svip24', lg['svar_ip24'], 2)
P('lg.svcpi24', lg['svar_cpi24'], 2)
V.raw('lg.T', str(lg['T']))
ls = N['lpsim']
V.raw('ls.reps', str(ls['reps']))
V.raw('ls.T', str(ls['T']))
P('ls.true8', ls['true8'], 2)
for kk in ('VAR(2)', 'VAR(12)', 'LP(2)'):
    tag = kk.replace('(', '').replace(')', '')
    for s in ('bias', 'sd', 'rmse'):
        for h in (8, 16):
            P(f'ls.{tag}.{s}{h}', abs(ls[f'{kk}_{s}_{h}']), 2)
z = N['rz']
for kk in ('lin', 'slack', 'normal'):
    for h in (8, 16):
        P(f'rz.{kk}{h}', z[f'{kk}{h}'], 2)
        P(f'rz.{kk}{h}se', z[f'{kk}{h}_se'], 2)
P('rz.share', 100 * z['share_slack'], 0)
rd = N['rodata']
V.raw('rd.first', month(rd['first']))
V.raw('rd.last', month(rd['last']))
V.raw('rd.n', str(rd['n']))
P('rd.imax', rd['infl_max'], 1)
V.raw('rd.imaxd', month(rd['infl_max_d']))
P('rd.ilast', rd['infl_last'], 1)
P('rd.rmax', rd['robor_max'], 1)
P('rd.fx0', rd['fx_first'], 2)
P('rd.fx1', rd['fx_last'], 2)
rv = N['rovar']
V.raw('rv.T', str(rv['T']))
V.raw('rv.aic', str(rv['ic']['aic']))
V.raw('rv.bic', str(rv['ic']['bic']))
V.raw('rv.hq', str(rv['ic']['hq']))
P('rv.root', rv['root'], 3)
P('rv.sdro', rv['sd_ro'], 2)
P('rv.sdea', rv['sd_ea'], 2)
for tag in ('ro', 'ea'):
    for name in ('ip', 'p', 'fx', 'r'):
        for h in (12, 24):
            for suf in ('', '.lo', '.hi'):
                P(f'rv.{tag}.{name}{h}{suf}', rv[f'{tag}.{name}{h}{suf}'], 2)
for name in ('ip', 'p', 'fx', 'r'):
    for h in (12, 36):
        for s in ('ea', 'own', 'r_ro'):
            P(f'rv.fe.{name}{h}.{s}', 100 * rv[f'fevd.{name}{h}.{s}'], 0)
rl = N['rolp']
P('rl.sd', rl['sd_bp'], 1)
V.raw('rl.n', str(rl['n']))
for h in ('0', '1', '2'):
    P(f'rl.F{h}', rl[f'F{h}'], 1)
for v in ('y1_ea', 'r_ro', 'ip_ro', 'p_ro', 'fx'):
    for h in (0, 6, 12, 24):
        P(f'rl.{v}{h}', rl[f'{v}{h}'], 2)
        P(f'rl.{v}{h}se', rl[f'{v}{h}.se'], 2)
    V.raw(f'rl.{v}.ns', str(rl[f'{v}.nsig']))
ai = N['ai']
P('ai.min', ai['vmin'], 2)
P('ai.max', ai['vmax'], 2)
V.raw('ai.npos', str(ai['n_pos']))
V.raw('ai.n', str(ai['n']))
minus_fix(V)

TB = '>{\\raggedright\\arraybackslash}'

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: what does a monetary policy shock, an oil supply shock or a fiscal shock \emph{cause}, and how sure can we be?',
       r'\textbf{Întrebarea}: ce \emph{provoacă} un șoc de politică monetară, un șoc de ofertă pe piața petrolului sau un șoc fiscal și cît de siguri putem fi?'),
     [T('a reduced-form VAR describes correlations; a causal answer needs an identifying assumption, stated and defended',
        'un VAR în formă redusă descrie corelații; un răspuns cauzal cere o ipoteză de identificare, enunțată și apărată')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('the identification problem; short-run (recursive and non-recursive) and long-run restrictions', 'problema identificării; restricții pe termen scurt (recursive și nerecursive) și pe termen lung'),
      T('sign, narrative and heteroskedasticity-based identification; set identification', 'identificarea prin semne, prin restricții narative și prin heteroscedasticitate; identificarea pe mulțimi'),
      T('external instruments and high-frequency surprises; inference for impulse responses', 'instrumente externe și surprize de frecvență înaltă; inferența pentru funcțiile de răspuns la impuls'),
      T('local projections: LP against VAR, LP-IV, state dependence; Romania and euro-area spillovers', 'proiecții locale: LP comparat cu VAR, LP-IV, dependența de stare; România și efectele de propagare din zona euro')]),
    T('We build on TSA, Chapter 6 (reduced-form VAR, Granger causality, Cholesky responses, FEVD) and on Chapter 0 (HAC, bootstrap); Seminar 3 comes before this lecture',
      'Pornim de la TSA, Capitolul 6 (VAR în formă redusă, cauzalitate Granger, răspunsuri Cholesky, FEVD) și de la Capitolul 0 (HAC, bootstrap); Seminarul 3 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('State the identification problem of a structural VAR, count the restrictions it needs and explain observational equivalence through rotations',
      'Enunțați problema identificării într-un VAR structural, numărați restricțiile necesare și explicați echivalența observațională prin rotații'),
    T('Identify shocks by short-run, long-run, sign, narrative and heteroskedasticity restrictions, and say what each assumes about the economy',
      'Identificați șocuri prin restricții pe termen scurt, pe termen lung, de semn, narative și prin heteroscedasticitate și spuneți ce presupune fiecare despre economie'),
    T('Estimate a proxy SVAR with an external instrument, check its relevance and use inference that stays valid with weak instruments',
      'Estimați un proxy SVAR cu un instrument extern, verificați relevanța instrumentului și folosiți o inferență valabilă și cu instrumente slabe'),
    T('Build bootstrap bands for impulse responses (residual, wild, block; Kilian bias correction) and read them correctly',
      'Construiți benzi bootstrap pentru răspunsurile la impuls (pe reziduuri, wild, pe blocuri; corecția deplasării Kilian) și interpretați-le corect'),
    T('Estimate local projections, LP-IV and state-dependent LP with HAC or lag-augmented inference, and choose between LP and VAR by the bias--variance trade-off',
      'Estimați proiecții locale, LP-IV și LP dependente de stare cu inferență HAC sau cu decalaje suplimentare și alegeți între LP și VAR după compromisul deplasare--varianță')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Backbone: \refKL, Ch.~8--15 (identification, inference, LP); \refHam, Ch.~11; \refLut', r'Manualul de bază: \refKL, cap.~8--15 (identificare, inferență, LP); \refHam, cap.~11; \refLut'),
     [T(r'surveys: \refRam\ (shocks and their propagation), \refSWc\ (external instruments), \refSWa', r'sinteze: \refRam\ (șocuri și propagarea lor), \refSWc\ (instrumente externe), \refSWa')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_03}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_03}'),
     [T(r'VAR, Cholesky, long-run and sign identification, proxy SVAR, bootstraps, LP, LP-IV written out in \texttt{numpy}',
        r'VAR, identificarea Cholesky, de termen lung și prin semne, proxy SVAR, metodele bootstrap, LP și LP-IV scrise explicit în \texttt{numpy}')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter3_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter3_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{4.6cm}' + TB + 'p{4.9cm}' + TB + 'p{2.4cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizare}'),
    [T('US monthly macro data, FF4 surprises, Romer--Romer shocks', 'date macro lunare SUA, surprizele FF4, șocurile Romer--Romer') + ' & ' + T(r'replication files of \refRam\ (public)', r'fișierele de replicare din \refRam\ (publice)') + ' & CEE, ' + T('sign, proxy, LP', 'semne, proxy, LP'),
     T('world crude oil production; refiner acquisition cost', 'producția mondială de țiței; costul de achiziție al rafinăriilor') + ' & ' + T('EIA (bulk file, Monthly Energy Review)', 'EIA (fișier bulk, Monthly Energy Review)') + ' & Kilian',
     T('global real activity index; US CPI; real GNP; unemployment of men 20+', 'indicele activității reale globale; IPC SUA; PNB real; șomajul bărbaților de 20+ ani') + ' & FRED (IGREA, CPIAUCSL, GNPC96, LNS14000025) & Kilian, BQ',
     T('US quarterly fiscal data 1889--2015', 'date fiscale trimestriale SUA 1889--2015') + ' & ' + T(r'replication files of \refRZ', r'fișierele de replicare din \refRZ') + ' & ' + T('state-dependent LP', 'LP dependente de stare'),
     T('IP, HICP, 3-month rates (RO, EA); EUR/RON', 'IP, IAPC, dobînzi la 3 luni (RO, ZE); EUR/RON') + ' & ' + T('Eurostat; BNR reference rate', 'Eurostat; cursul de referință BNR') + ' & ' + T('Romanian VAR', 'VAR pentru România'),
     T('ECB monetary policy shocks; EA 1-year rate', 'șocuri de politică monetară BCE; dobînda la 1 an ZE') + ' & ' + T(r'\refJK\ (authors\' update); ECB Data Portal', r'\refJK\ (actualizarea autorilor); ECB Data Portal') + ' & ' + T('spillovers', 'propagare')],
    size='scriptsize') + items(
    T('All sources are public and need no account or key; monthly data up to mid-2026, except the replication files',
      'Toate sursele sînt publice și nu cer cont sau cheie; datele lunare merg pînă la mijlocul lui 2026, cu excepția fișierelor de replicare'),
    T('IP: industrial production; HICP: harmonised index of consumer prices; FF4: surprise in the fourth federal funds futures contract',
      'IP: producția industrială; IAPC (HICP): indicele armonizat al prețurilor de consum; FF4: surpriza din al patrulea contract futures pe dobînda federal funds')), 'footnotesize')

D.frame(T('From correlations to shocks', 'De la corelații la șocuri'), two(
    ph('sims', T('Christopher Sims, Nobel lecture, 2011', 'Christopher Sims, prelegerea Nobel, 2011'), h='0.36\\textheight'),
    items((T(r'1980: \refSims\ proposes VARs instead of large models with ``incredible\'\' exclusion restrictions', r'1980: \refSims\ propune modelele VAR în locul modelelor mari cu restricții de excludere „incredibile”'),
           [T('the Cholesky ordering was his first identification scheme, and the first target of criticism', 'ordonarea Cholesky a fost prima lui schemă de identificare și prima țintă a criticilor')]),
          T(r'1989: long-run restrictions \refBQ; 1999: the recursive monetary VAR \refCEE', r'1989: restricțiile de termen lung \refBQ; 1999: VAR-ul monetar recursiv \refCEE'),
          T(r'2005: sign restrictions \refUhl\ and local projections \refJorda; 2012--2018: external instruments \refSWb, \refMR, \refGK', r'2005: restricțiile de semn \refUhl\ și proiecțiile locale \refJorda; 2012--2018: instrumentele externe \refSWb, \refMR, \refGK'),
          T('2011: Sims and Sargent share the Nobel Prize ``for their empirical research on cause and effect in the macroeconomy\'\'', '2011: Sims și Sargent primesc Premiul Nobel „pentru cercetarea empirică a cauzei și efectului în macroeconomie”'),
          T('The question has stayed the same; the identifying assumptions have become weaker and more transparent', 'Întrebarea a rămas aceeași; ipotezele de identificare au devenit mai slabe și mai transparente')), '0.40', '0.58'), 'footnotesize')

# =============================================================================
# 1. PROBLEMA IDENTIFICĂRII
# =============================================================================
D.section('The identification problem', 'Problema identificării')

D.frame(T('Reduced form and structural form', 'Forma redusă și forma structurală'), items(
    (T(r'Reduced form (TSA, Chapter 6): $y_t = \nu + A_1y_{t-1} + \dots + A_py_{t-p} + u_t$, $\E u_tu_t\' = \Sigma_u$', r'Forma redusă (TSA, Capitolul 6): $y_t = \nu + A_1y_{t-1} + \dots + A_py_{t-p} + u_t$, $\E u_tu_t\' = \Sigma_u$'),
     [T(r'$u_t$ are one-step forecast errors: they mix all the economic shocks that hit in period $t$', r'$u_t$ sînt erorile de prognoză la un pas: ele amestecă toate șocurile economice din perioada $t$')]),
    (T(r'Structural form: $u_t = B_0\varepsilon_t$, with structural shocks $\varepsilon_t$ mutually uncorrelated, $\E\varepsilon_t\varepsilon_t\' = I_n$', r'Forma structurală: $u_t = B_0\varepsilon_t$, cu șocurile structurale $\varepsilon_t$ necorelate între ele, $\E\varepsilon_t\varepsilon_t\' = I_n$'),
     [T(r'equivalently $B_0^{-1}y_t = B_0^{-1}\nu + B_0^{-1}A_1y_{t-1} + \dots + \varepsilon_t$: contemporaneous relations among the variables', r'echivalent $B_0^{-1}y_t = B_0^{-1}\nu + B_0^{-1}A_1y_{t-1} + \dots + \varepsilon_t$: relații contemporane între variabile'),
      T(r'a \textbf{shock} is primitive, exogenous, uncorrelated with other shocks and economically meaningful \refRam', r'un \textbf{șoc} este primitiv, exogen, necorelat cu celelalte șocuri și are sens economic \refRam')]),
    (T(r'Structural impulse responses: $\Theta_h = \Phi_hB_0$, with $\Phi_h$ the reduced-form MA coefficients', r'Răspunsurile structurale la impuls: $\Theta_h = \Phi_hB_0$, cu $\Phi_h$ coeficienții MA ai formei reduse'),
     [T(r'element $(i, j)$ of $\Theta_h$: effect of a one-standard-deviation shock $j$ on variable $i$ after $h$ periods', r'elementul $(i, j)$ al $\Theta_h$: efectul unui șoc $j$ de o abatere standard asupra variabilei $i$ după $h$ perioade')])), 'small')

D.frame(T('Counting: the data do not pin down $B_0$', 'Numărătoarea: datele nu determină $B_0$'), items(
    (T(r'The data identify $\Sigma_u = B_0B_0\'$: $n(n + 1)/2$ distinct moments; $B_0$ has $n^2$ unknowns', r'Datele identifică $\Sigma_u = B_0B_0\'$: $n(n + 1)/2$ momente distincte; $B_0$ are $n^2$ necunoscute'),
     [T(r'order condition: at least $n(n - 1)/2$ restrictions (3 for $n = 3$, 28 for $n = 8$)', r'condiția de ordin: cel puțin $n(n - 1)/2$ restricții (3 pentru $n = 3$, 28 pentru $n = 8$)'),
      T(r'the rank condition must also hold locally \refRWZ: counting is necessary, not sufficient', r'trebuie să fie îndeplinită și condiția de rang, local \refRWZ: numărătoarea este necesară, nu suficientă')]),
    (T(r'\textbf{Observational equivalence}: for any orthogonal $Q$ ($QQ\' = I$), $\tilde B_0 = B_0Q$ gives $\tilde B_0\tilde B_0\' = \Sigma_u$', r'\textbf{Echivalența observațională}: pentru orice $Q$ ortogonală ($QQ\' = I$), $\tilde B_0 = B_0Q$ dă $\tilde B_0\tilde B_0\' = \Sigma_u$'),
     [T('the two models fit the data equally well and imply different impulse responses', 'cele două modele descriu datele la fel de bine și implică răspunsuri la impuls diferite'),
      T(r'identification = a rule that selects one $Q$ (point identification) or a set of $Q$ (set identification)', r'identificarea = o regulă care alege un singur $Q$ (identificare punctuală) sau o mulțime de matrice $Q$ (identificare pe mulțimi)')]),
    T(r'A useful parametrisation: $B_0 = PQ$ with $P$ the Cholesky factor of $\Sigma_u$; every identification scheme is a choice of $Q$', r'O parametrizare utilă: $B_0 = PQ$ cu $P$ factorul Cholesky al lui $\Sigma_u$; orice schemă de identificare este o alegere a lui $Q$')), 'small')

D.frame(T('Invertibility and the limits of a VAR', 'Inversabilitatea și limitele unui VAR'), items(
    (T(r'A VAR recovers $\varepsilon_t$ from current and past $y_t$ only if the shocks are \textbf{invertible} (fundamental)', r'Un VAR recuperează $\varepsilon_t$ din valorile curente și trecute ale lui $y_t$ doar dacă șocurile sînt \textbf{inversabile} (fundamentale)'),
     [T('news shocks and fiscal foresight break invertibility: agents react before the econometrician sees the shock', 'șocurile de tip știre și anticiparea fiscală distrug inversabilitatea: agenții reacționează înainte ca econometricianul să vadă șocul'),
      T(r'remedy: add forward-looking variables (asset prices, forecasts) or use the shock directly \refRam', r'remediu: adăugați variabile anticipative (prețuri de active, prognoze) sau folosiți direct șocul \refRam')]),
    (T(r'With an external instrument we need only \emph{partial} invertibility of the shock of interest \refSWc', r'Cu un instrument extern avem nevoie doar de inversabilitatea \emph{parțială} a șocului de interes \refSWc'),
     [T(r'local projections with the shock as regressor do not need invertibility at all \refPW', r'proiecțiile locale cu șocul ca regresor nu au deloc nevoie de inversabilitate \refPW')]),
    T(r'Practical rule: a small VAR omitting information the agents use (expectations, commodity prices) produces ``puzzles\'\'', r'Regula practică: un VAR mic, care omite informații folosite de agenți (așteptări, prețuri ale materiilor prime), produce „anomalii”')), 'small')

D.recap(('The identification problem', 'problema identificării'), [
    T(r'$\Sigma_u$ fixes $B_0$ only up to an orthogonal rotation $Q$', r'$\Sigma_u$ fixează $B_0$ doar pînă la o rotație ortogonală $Q$'),
    T(r'Point identification needs at least $n(n - 1)/2$ restrictions and the rank condition', r'Identificarea punctuală cere cel puțin $n(n - 1)/2$ restricții și condiția de rang'),
    T('Every scheme is an economic assumption: state it, defend it, test what can be tested', 'Orice schemă este o ipoteză economică: enunțați-o, apărați-o, testați ce se poate testa'),
    T('Invertibility is a separate assumption; instruments and LP relax it', 'Inversabilitatea este o ipoteză separată; instrumentele și LP o relaxează')])

# =============================================================================
# 2. RESTRICȚII PE TERMEN SCURT
# =============================================================================
D.section('Short-run restrictions', 'Restricții pe termen scurt')

D.frame(T('Recursive identification', 'Identificarea recursivă'), items(
    (T(r'$B_0 = P$ lower triangular: variable $i$ does not respond within the period to shocks ordered after it', r'$B_0 = P$ inferior triunghiulară: variabila $i$ nu răspunde în aceeași perioadă la șocurile ordonate după ea'),
     [T(r'exactly $n(n - 1)/2$ zeros: just identified; the ordering is the assumption (TSA, Chapter 6 showed that it matters)', r'exact $n(n - 1)/2$ zerouri: identificare exactă; ordonarea este ipoteza (TSA, Capitolul 6 a arătat că ea contează)')]),
    (T(r'Monetary block of \refCEE: slow variables (output, prices), the policy rate, fast variables (reserves, money)', r'Blocul monetar din \refCEE: variabile lente (producție, prețuri), dobînda de politică, variabile rapide (rezerve, masa monetară)'),
     [T('assumption: within a month, output and prices do not react to policy, and policy reacts to them', 'ipoteza: într-o lună, producția și prețurile nu reacționează la politica monetară, iar politica reacționează la ele'),
      T('only the position of the policy variable matters for its shock; the ordering inside the blocks is irrelevant', 'pentru șocul de politică contează doar poziția variabilei de politică; ordonarea în interiorul blocurilor este irelevantă')]),
    T('Plausible at a monthly frequency with slow-moving real variables; implausible for asset prices or for quarterly data', 'Plauzibilă la frecvență lunară pentru variabile reale lente; neplauzibilă pentru prețurile activelor sau pentru date trimestriale')), 'small')

D.frame(T('Case study: Christiano, Eichenbaum and Evans (1999)', 'Studiu de caz: Christiano, Eichenbaum și Evans (1999)'), items(
    (T(r'The paper: the benchmark recursive monetary VAR; US monthly data, the federal funds rate shock ordered after output, prices and commodity prices \refCEE', r'Lucrarea: VAR-ul monetar recursiv de referință; date lunare SUA, șocul dobînzii federal funds ordonat după producție, prețuri și prețurile materiilor prime \refCEE'),
     [T(r'we use the specification of \refRam, Figure 1: VAR(12) in log IP, unemployment, log CPI, log commodity prices, funds rate, log nonborrowed and total reserves, log M1', r'folosim specificația din \refRam, Figura 1: VAR(12) cu log IP, șomaj, log IPC, log prețuri ale materiilor prime, dobînda federal funds, log rezerve neîmprumutate și totale, log M1')]),
    (T(r'Sample 1965:1--1995:6 ($T = @{cee.T}$), constant, Cholesky with the funds rate fifth; 90\% bands from @{cee.B} residual-bootstrap replications', r'Eșantion 1965:1--1995:6 ($T = @{cee.T}$), termen liber, Cholesky cu dobînda federal funds pe locul cinci; benzi de 90\% din @{cee.B} de replicări bootstrap pe reziduuri'),
     [T(r'the largest root of the companion matrix is @{cee.root}: a VAR in levels, consistent for responses at short and medium horizons \refKL', r'cea mai mare rădăcină a matricei companion este @{cee.root}: un VAR în niveluri, consistent pentru răspunsurile pe orizonturi scurte și medii \refKL')]),
    T('Question: how do output and prices respond to an unexpected tightening?', 'Întrebarea: cum răspund producția și prețurile la o înăsprire neașteptată?')), 'small')

chart(T('A recursive monetary policy shock (CEE specification)', 'Un șoc de politică monetară recursiv (specificația CEE)'), 'ats_ch3_cee_irf', 'ATS_ch3_recursive_var', [
    T(r'Responses to a one-standard-deviation funds-rate shock (@{cee.sd} pp); 90\% residual-bootstrap bands', r'Răspunsuri la un șoc al dobînzii federal funds de o abatere standard (@{cee.sd} pp); benzi bootstrap de 90\%')],
    h='0.52\\textheight')

interp(('the CEE responses', 'răspunsurilor CEE'), [
    (T(r'Industrial production falls slowly: trough @{cee.ipmin}\% after @{cee.iparg} months (band [@{cee.iplo}, @{cee.iphi}]); unemployment rises by up to @{cee.umax} pp', r'Producția industrială scade lent: minimum @{cee.ipmin}\% după @{cee.iparg} luni (banda [@{cee.iplo}, @{cee.iphi}]); șomajul crește cu cel mult @{cee.umax} pp'),
     [T('the hump shape and the delay are the classic ``long and variable lags\'\' of monetary policy', 'forma de cocoașă și întîrzierea sînt clasicele „decalaje lungi și variabile” ale politicii monetare')]),
    (T(r'Prices first rise slightly (@{cee.pmax}\% after @{cee.parg} months), then fall to @{cee.p48}\% after four years', r'Prețurile cresc întîi ușor (@{cee.pmax}\% după @{cee.parg} luni), apoi scad la @{cee.p48}\% după patru ani'),
     [T(r'the initial rise is the \textbf{price puzzle}: the Fed tightens when it expects inflation; commodity prices in the VAR reduce but do not remove it', r'creșterea inițială este \textbf{anomalia prețurilor} (price puzzle): Fed înăsprește politica atunci cînd anticipează inflație; prețurile materiilor prime din VAR o reduc, dar nu o elimină')]),
    T(r'Monetary shocks explain little of output: @{cee.fe24}\% of the 24-month forecast error variance of IP', r'Șocurile monetare explică puțin din producție: @{cee.fe24}\% din varianța erorii de prognoză a IP la 24 de luni')])

D.frame(T('Non-recursive short-run restrictions', 'Restricții nerecursive pe termen scurt'), items(
    (T(r'\textbf{AB model} \refLut, \refKL: $Au_t = B\varepsilon_t$; zeros and known values anywhere in $A$ and $B$', r'\textbf{Modelul AB} \refLut, \refKL: $Au_t = B\varepsilon_t$; zerouri și valori cunoscute oriunde în $A$ și $B$'),
     [T(r'estimated by maximum likelihood: maximise $-\frac T2\ln|A^{-1}BB\'A^{-1\prime}| - \frac T2\mathrm{tr}[(A^{-1}BB\'A^{-1\prime})^{-1}\hat\Sigma_u]$', r'estimat prin verosimilitate maximă: maximizăm $-\frac T2\ln|A^{-1}BB\'A^{-1\prime}| - \frac T2\mathrm{tr}[(A^{-1}BB\'A^{-1\prime})^{-1}\hat\Sigma_u]$'),
      T('over-identifying restrictions can be tested by a likelihood-ratio test against the just-identified model', 'restricțiile de supraidentificare se testează cu un test al raportului de verosimilitate față de modelul exact identificat')]),
    (T(r'\textbf{Blanchard--Perotti} \refBP: the automatic response of taxes to output is an \emph{external} elasticity (from tax codes)', r'\textbf{Blanchard--Perotti} \refBP: răspunsul automat al taxelor la producție este o elasticitate \emph{externă} (din legislația fiscală)'),
     [T('with that elasticity fixed, the cyclically adjusted tax innovation is an instrument for the remaining coefficients', 'cu această elasticitate fixată, inovația taxelor ajustată ciclic este un instrument pentru coeficienții rămași'),
      T('government spending is predetermined within the quarter (decision lags): a zero restriction with an institutional argument', 'cheltuielile publice sînt predeterminate în trimestru (decalaje de decizie): o restricție zero cu un argument instituțional')]),
    T('Seminar 3, A2: one known elasticity identifies a $2\\times2$ system by instrumental variables', 'Seminarul 3, A2: o elasticitate cunoscută identifică un sistem $2\\times2$ prin variabile instrumentale')), 'small')

D.frame(T('What the recursive assumption cannot do', 'Limitele ipotezei recursive'), items(
    (T('Simultaneity: interest rates and asset prices react to each other within the day', 'Simultaneitatea: dobînzile și prețurile activelor reacționează unele la altele în aceeași zi'),
     [T('no ordering of stock prices and the policy rate is credible at a monthly frequency', 'nicio ordonare a prețurilor acțiunilor și a dobînzii de politică nu este credibilă la frecvență lunară')]),
    (T('Omitted information: the policy shock absorbs the Fed\'s forecasts', 'Informația omisă: șocul de politică absoarbe prognozele Fed'),
     [T(r'narrative shocks \refRR\ purge the intended rate change of the Greenbook forecasts', r'șocurile narative \refRR\ curăță modificarea intenționată a dobînzii de prognozele din Greenbook')]),
    (T(r'Sample dependence: the post-1983 responses are weaker and often puzzling \refRam', r'Dependența de eșantion: după 1983 răspunsurile sînt mai slabe și deseori anormale \refRam'),
     [T('the remedies of the next sections: weaker restrictions (signs) or outside information (instruments)', 'remediile din secțiunile următoare: restricții mai slabe (semne) sau informație externă (instrumente)')])), 'small')

D.recap(('Short-run restrictions', 'restricții pe termen scurt'), [
    T('Cholesky = timing assumptions; only the position of the shock variable matters for its responses', 'Cholesky = ipoteze despre momentul reacției; pentru răspunsurile unui șoc contează doar poziția variabilei lui'),
    T(r'CEE: output falls with a lag of about @{cee.iparg} months; the price puzzle remains', r'CEE: producția scade cu o întîrziere de aproximativ @{cee.iparg} luni; anomalia prețurilor rămîne'),
    T('Non-recursive schemes use institutional knowledge (tax elasticities, decision lags) and can be over-identified and tested', 'Schemele nerecursive folosesc cunoștințe instituționale (elasticități fiscale, decalaje de decizie) și pot fi supraidentificate și testate'),
    T('Short-run zeros are least credible exactly where they matter most: fast markets', 'Zerourile pe termen scurt sînt cel mai puțin credibile exact acolo unde contează mai mult: pe piețele rapide')])

# =============================================================================
# 3. KILIAN 2009
# =============================================================================
D.section('Case study: oil supply and demand shocks', 'Studiu de caz: șocuri de ofertă și de cerere pe piața petrolului')

D.frame(T('Not all oil price shocks are alike', 'Nu toate șocurile prețului petrolului sînt la fel'), two(
    ph('kuwait', T('Burning Kuwaiti oil field, March 1991', 'Cîmp petrolier în flăcări, Kuweit, martie 1991'), h='0.36\\textheight'),
    items((T(r'\refKilB: monthly VAR(24) in (i) the percent change of world crude oil production, (ii) global real activity, (iii) the log real price of oil', r'\refKilB: VAR(24) lunar cu (i) variația procentuală a producției mondiale de țiței, (ii) activitatea reală globală, (iii) logaritmul prețului real al petrolului'),
           [T('recursive: oil supply does not respond within the month to demand (adjustment costs); real activity does not respond within the month to oil-specific demand', 'recursiv: oferta de petrol nu răspunde în aceeași lună la cerere (costuri de ajustare); activitatea reală nu răspunde în aceeași lună la cererea specifică petrolului')]),
          (T('Three shocks: oil supply, aggregate demand, oil-specific (precautionary) demand', 'Trei șocuri: oferta de petrol, cererea agregată, cererea specifică petrolului (de precauție)'),
           [T(r'real activity: the index of \refKilB\ as corrected in \refKilC\ (FRED IGREA); price: refiner acquisition cost of imported crude, deflated by the US CPI', r'activitatea reală: indicele din \refKilB\ corectat în \refKilC\ (FRED IGREA); prețul: costul de achiziție al țițeiului importat de rafinării, deflatat cu IPC din SUA')]),
          T(r'Our sample starts in 1974 (first month of the price series), effective sample from @{kil.first}, $T = @{kil.T}$; extension to @{kil.last2}', r'Eșantionul nostru începe în 1974 (prima lună a seriei de prețuri), eșantionul efectiv din @{kil.first}, $T = @{kil.T}$; extindere pînă în @{kil.last2}')), '0.38', '0.60'), 'footnotesize')

chart(T('Responses to oil supply and demand shocks', 'Răspunsuri la șocurile de ofertă și de cerere pe piața petrolului'), 'ats_ch3_kilian_irf', 'ATS_ch3_oil_shocks', [
    T(r'One-standard-deviation shocks, production cumulated; 68\% and 95\% recursive-design wild-bootstrap bands \refGoK; dashed: sample extended to 2026', r'Șocuri de o abatere standard, producția cumulată; benzi bootstrap wild cu design recursiv de 68\% și 95\% \refGoK; linia întreruptă: eșantionul extins pînă în 2026')],
    h='0.64\\textheight')

interp(('the oil responses', 'răspunsurilor pe piața petrolului'), [
    (T(r'Supply shock: production falls by @{kil.sup_q0}\% on impact, the real price barely moves (@{kil.sup_p12}\% after 12 months, band [@{kil.sup_p12_lo}, @{kil.sup_p12_hi}])', r'Șocul de ofertă: producția scade cu @{kil.sup_q0}\% la impact, prețul real aproape nu se mișcă (@{kil.sup_p12}\% după 12 luni, banda [@{kil.sup_p12_lo}, @{kil.sup_p12_hi}])'),
     [T(r'in the extended sample the effect is larger (@{kil.sup_p12_2}\%): the post-2008 market reacts more to supply news', r'în eșantionul extins efectul este mai mare (@{kil.sup_p12_2}\%): piața de după 2008 reacționează mai mult la veștile despre ofertă')]),
    T(r'Aggregate demand: a delayed, persistent rise of the price (@{kil.ad_p12}\% after 12 months, band [@{kil.ad_p12_lo}, @{kil.ad_p12_hi}])', r'Cererea agregată: o creștere întîrziată și persistentă a prețului (@{kil.ad_p12}\% după 12 luni, banda [@{kil.ad_p12_lo}, @{kil.ad_p12_hi}])'),
    T(r'Oil-specific demand: an immediate jump (@{kil.os_p0}\%) that persists (@{kil.os_p12}\% after 12 months)', r'Cererea specifică petrolului: un salt imediat (@{kil.os_p0}\%) care persistă (@{kil.os_p12}\% după 12 luni)'),
    T(r'At 60 months, supply shocks explain @{kil.fe.sup}\% of the price variance, aggregate demand @{kil.fe.ad}\%, oil-specific demand @{kil.fe.os}\%: oil prices are mostly demand-driven', r'La 60 de luni, șocurile de ofertă explică @{kil.fe.sup}\% din varianța prețului, cererea agregată @{kil.fe.ad}\%, cererea specifică @{kil.fe.os}\%: prețul petrolului este determinat mai ales de cerere')])

chart(T('Historical decomposition of the real price of oil', 'Descompunerea istorică a prețului real al petrolului'), 'ats_ch3_kilian_hd', 'ATS_ch3_oil_shocks', [
    T(r'Cumulative contribution of each structural shock, 1976--2026 (recursive VAR(24), extended sample); log points $\times 100$', r'Contribuția cumulată a fiecărui șoc structural, 1976--2026 (VAR(24) recursiv, eșantionul extins); puncte logaritmice $\times 100$')],
    h='0.54\\textheight')

interp(('the historical decomposition', 'descompunerii istorice'), [
    T(r'2003--mid-2008: aggregate demand adds @{hd.c2003_2008.ad} log points, supply @{hd.c2003_2008.sup}: the boom was a global demand boom', r'2003--mijlocul lui 2008: cererea agregată adaugă @{hd.c2003_2008.ad} puncte logaritmice, oferta @{hd.c2003_2008.sup}: boom-ul a fost unul al cererii globale'),
    T(r'Mid-2008 to early 2009: oil-specific demand @{hd.c2008_2009.os}, aggregate demand @{hd.c2008_2009.ad}; early 2020: oil-specific demand @{hd.c2020.os}', r'De la mijlocul lui 2008 la începutul lui 2009: cererea specifică @{hd.c2008_2009.os}, cererea agregată @{hd.c2008_2009.ad}; începutul lui 2020: cererea specifică @{hd.c2020.os}'),
    T(r'Mid-2021 to mid-2022: oil-specific demand @{hd.c2022.os}, supply @{hd.c2022.sup}: the model reads the 2022 surge as precautionary demand', r'De la mijlocul lui 2021 la mijlocul lui 2022: cererea specifică @{hd.c2022.os}, oferta @{hd.c2022.sup}: modelul citește saltul din 2022 drept cerere de precauție'),
    (T(r'Caveat: the zero restriction on the supply response is strong; \refBHb\ allow a small but non-zero elasticity and find a larger role for supply', r'Rezervă: restricția zero pentru răspunsul ofertei este puternică; \refBHb\ permit o elasticitate mică, dar nenulă, și găsesc un rol mai mare pentru ofertă'),
     [T('a decomposition is only as good as the identifying assumption behind it', 'o descompunere este la fel de bună ca ipoteza de identificare din spatele ei')])])

# =============================================================================
# 4. RESTRICȚII PE TERMEN LUNG
# =============================================================================
D.section('Long-run restrictions', 'Restricții pe termen lung')

D.frame(T('Blanchard and Quah: the long-run multiplier', 'Blanchard și Quah: multiplicatorul de termen lung'), items(
    (T(r'For $y_t = (\Delta\text{output}_t, u_t)\'$, the cumulative response of output is $\Theta(1) = \sum_h\Theta_h = (I - A_1 - \dots - A_p)^{-1}B_0 = A(1)^{-1}B_0$', r'Pentru $y_t = (\Delta\text{producție}_t, u_t)\'$, răspunsul cumulat al producției este $\Theta(1) = \sum_h\Theta_h = (I - A_1 - \dots - A_p)^{-1}B_0 = A(1)^{-1}B_0$'),
     [T(r'restriction \refBQ: demand shocks have no long-run effect on the level of output, $[\Theta(1)]_{12} = 0$', r'restricția \refBQ: șocurile de cerere nu au efect pe termen lung asupra nivelului producției, $[\Theta(1)]_{12} = 0$')]),
    (T(r'Algorithm: $\Theta(1)\Theta(1)\' = A(1)^{-1}\Sigma_uA(1)^{-1\prime}$; take its Cholesky factor $L$, then $B_0 = A(1)L$', r'Algoritmul: $\Theta(1)\Theta(1)\' = A(1)^{-1}\Sigma_uA(1)^{-1\prime}$; luăm factorul lui Cholesky $L$, apoi $B_0 = A(1)L$'),
     [T('the zero is placed on the long-run matrix, not on the impact matrix; derivation in the Appendix and in Seminar 3, A3', 'zeroul este pus pe matricea de termen lung, nu pe matricea de impact; derivarea în Anexă și în Seminarul 3, A3')]),
    T(r'Interpretation: ``supply\'\' = all shocks with permanent effects (technology, labour supply); \refGali\ uses the same idea for technology shocks and hours', r'Interpretare: „oferta” = toate șocurile cu efecte permanente (tehnologie, oferta de muncă); \refGali\ folosește aceeași idee pentru șocurile tehnologice și orele lucrate')), 'small')

D.frame(T('Case study: Blanchard and Quah (1989)', 'Studiu de caz: Blanchard și Quah (1989)'), items(
    (T(r'The paper: US real GNP growth and the unemployment rate (men aged 20 and over), quarterly, VAR(8), 1950:2--1987:4 \refBQ', r'Lucrarea: creșterea PNB real în SUA și rata șomajului (bărbați de 20 de ani și peste), trimestrial, VAR(8), 1950:2--1987:4 \refBQ'),
     [T('data treatment: separate means of output growth before and after 1973:4 (the productivity slowdown), a linear trend removed from unemployment', 'tratarea datelor: medii separate ale creșterii producției înainte și după 1973:4 (încetinirea productivității), trend liniar eliminat din șomaj')]),
    T(r'Our replication: the same specification on today\'s vintage (FRED GNPC96, LNS14000025), $T = @{bq.T}$; 90\% residual-bootstrap bands', r'Replicarea noastră: aceeași specificație pe versiunea actuală a datelor (FRED GNPC96, LNS14000025), $T = @{bq.T}$; benzi bootstrap de 90\%'),
    T('Question: do demand shocks drive the business cycle, and how long do their effects last?', 'Întrebarea: determină șocurile de cerere ciclul economic și cît durează efectele lor?')), 'small')

chart(T('Supply and demand shocks identified by a long-run restriction', 'Șocuri de ofertă și de cerere identificate printr-o restricție de termen lung'), 'ats_ch3_bq', 'ATS_ch3_long_run', [
    T(r'Output level (cumulated growth) and unemployment; one-standard-deviation shocks; 90\% bootstrap bands', r'Nivelul producției (creșterea cumulată) și șomajul; șocuri de o abatere standard; benzi bootstrap de 90\%')],
    h='0.54\\textheight')

interp(('the Blanchard--Quah responses', 'răspunsurilor Blanchard--Quah'), [
    T(r'Demand shock: output peaks at @{bq.dpeak}\% after @{bq.dpeakq} quarters and returns to zero by construction; unemployment falls by @{bq.dumin} pp', r'Șocul de cerere: producția atinge un maxim de @{bq.dpeak}\% după @{bq.dpeakq} trimestre și revine la zero prin construcție; șomajul scade cu @{bq.dumin} pp'),
    T(r'Supply shock: output rises permanently (@{bq.s40}\% after ten years, band [@{bq.s40lo}, @{bq.s40hi}]), unemployment first \emph{rises} (@{bq.su0} pp)', r'Șocul de ofertă: producția crește permanent (@{bq.s40}\% după zece ani, banda [@{bq.s40lo}, @{bq.s40hi}]), iar șomajul întîi \emph{crește} (@{bq.su0} pp)'),
    T(r'Demand shocks explain @{bq.fe4}\% of the output-level variance at one year and @{bq.fe40}\% at ten years: as in the paper, demand dominates at business-cycle horizons', r'Șocurile de cerere explică @{bq.fe4}\% din varianța nivelului producției la un an și @{bq.fe40}\% la zece ani: ca în lucrare, cererea domină la orizonturile ciclului economic'),
    T('Seminar 3, B5: without the break and the trend, the shares change dramatically', 'Seminarul 3, B5: fără ruptură și fără trend, ponderile se schimbă radical')])

D.frame(T('How reliable are long-run restrictions?', 'Cît de fiabile sînt restricțiile de termen lung?'), items(
    (T(r'\refFL: the long-run multiplier $A(1)^{-1}$ is estimated imprecisely from finite samples', r'\refFL: multiplicatorul de termen lung $A(1)^{-1}$ se estimează imprecis din eșantioane finite'),
     [T('a shock with a tiny but permanent effect is indistinguishable from a transitory one: inference can be arbitrarily distorted', 'un șoc cu un efect permanent foarte mic nu se poate distinge de unul tranzitoriu: inferența poate fi distorsionată oricît de mult'),
      T('the near-unit-root behaviour of unemployment makes the problem worse', 'comportamentul de rădăcină aproape unitară al șomajului agravează problema')]),
    (T('Results depend on the treatment of low frequencies: breaks in mean growth, trends, the lag length', 'Rezultatele depind de tratarea frecvențelor joase: rupturi în creșterea medie, trenduri, numărul de decalaje'),
     [T('Chapter 2 tests for such breaks; Chapter 4 treats cointegration, where long-run restrictions become restrictions on the VECM', 'Capitolul 2 testează astfel de rupturi; Capitolul 4 tratează cointegrarea, unde restricțiile de termen lung devin restricții asupra VECM')]),
    T('Use long-run restrictions with a sensitivity table, never alone', 'Folosiți restricțiile de termen lung împreună cu un tabel de sensibilitate, niciodată singure')), 'small')

D.recap(('Long-run restrictions', 'restricții pe termen lung'), [
    T(r'Restrict $\Theta(1) = A(1)^{-1}B_0$ instead of $B_0$: identification from permanence', r'Restricționăm $\Theta(1) = A(1)^{-1}B_0$ în loc de $B_0$: identificare prin permanență'),
    T('BQ: demand dominates business-cycle fluctuations in output, supply the long run', 'BQ: cererea domină fluctuațiile producției pe orizontul ciclului, oferta termenul lung'),
    T('Fragile: low-frequency treatment and the imprecise long-run multiplier drive the answer', 'Fragile: tratarea frecvențelor joase și multiplicatorul de termen lung imprecis determină răspunsul')])

# =============================================================================
# 5. RESTRICȚII DE SEMN
# =============================================================================
D.section('Sign restrictions and set identification', 'Restricții de semn și identificarea pe mulțimi')

D.frame(T('Identification by signs', 'Identificarea prin semne'), items(
    (T(r'Restrict only the \textbf{signs} of some responses for some horizons: a contractionary monetary shock raises the rate and lowers prices \refUhl', r'Restricționăm doar \textbf{semnele} unor răspunsuri pe anumite orizonturi: un șoc monetar contracționist crește dobînda și scade prețurile \refUhl'),
     [T('the response of interest (output) is left unrestricted: an ``agnostic\'\' procedure', 'răspunsul de interes (producția) rămîne nerestricționat: o procedură „agnostică”')]),
    (T(r'Algorithm \refRWZ: draw $X$ with i.i.d.\ $N(0, 1)$ entries, $X = QR$, normalise the signs of $\mathrm{diag}(R)$; $Q$ is Haar-uniform on the orthogonal group', r'Algoritmul \refRWZ: extragem $X$ cu elemente i.i.d.\ $N(0, 1)$, $X = QR$, normalizăm semnele lui $\mathrm{diag}(R)$; $Q$ este uniformă Haar pe grupul ortogonal'),
     [T(r'compute $\Theta_h = \Phi_hPQ$ and keep $Q$ if all signs hold; repeat for draws of $(A, \Sigma_u)$ from the posterior', r'calculăm $\Theta_h = \Phi_hPQ$ și păstrăm $Q$ dacă toate semnele sînt respectate; repetăm pentru extrageri ale lui $(A, \Sigma_u)$ din distribuția a posteriori'),
      T(r'zero restrictions together with signs need the importance-sampling algorithm of \refARW', r'restricțiile zero împreună cu semne cer algoritmul cu eșantionare de importanță din \refARW')]),
    T('The result is a \\textbf{set} of models consistent with the data and the restrictions, not a point', 'Rezultatul este o \\textbf{mulțime} de modele compatibile cu datele și cu restricțiile, nu un punct')), 'small')

chart(T('Sign restrictions in two dimensions', 'Restricții de semn în două dimensiuni'), 'ats_ch3_rotation', 'ATS_ch3_sign_restrictions', [
    T(r'Price and quantity innovations with variances 1 and 0.5 and covariance 0.3; impact responses $P(\cos\theta, \sin\theta)\'$ to shock 1 as the rotation angle varies; demand: $(+, +)$, supply: $(+, -)$', r'Inovații ale prețului și cantității cu varianțele 1 și 0,5 și covarianța 0,3; răspunsurile la impact $P(\cos\theta, \sin\theta)\'$ la șocul 1 cînd variază unghiul de rotație; cererea: $(+, +)$, oferta: $(+, -)$')],
    h='0.54\\textheight')

interp(('the rotation set', 'mulțimii de rotații'), [
    T(r'All signs hold for $\theta \in (0, @{rot.thhi})$, @{rot.share}\% of the circle: a whole interval of models is equally consistent with the data', r'Toate semnele sînt respectate pentru $\theta \in (0; @{rot.thhi})$, @{rot.share}\% din cerc: un interval întreg de modele este la fel de compatibil cu datele'),
    T(r'The impact effect of demand on quantity lies anywhere in $[@{rot.qlo}, @{rot.qhi}]$: the \textbf{identified set}', r'Efectul la impact al cererii asupra cantității se află oriunde în $[@{rot.qlo}; @{rot.qhi}]$: \textbf{mulțimea identificată}'),
    (T('A uniform draw of $\\theta$ puts a prior on this interval: the posterior inside the set is the prior, not information from data', 'O extragere uniformă a lui $\\theta$ pune o distribuție a priori pe acest interval: distribuția a posteriori în interiorul mulțimii este cea a priori, nu informație din date'),
     [T(r'this is the point of \refBHa: Haar draws are informative about the responses', r'acesta este argumentul din \refBHa: extragerile Haar sînt informative pentru răspunsuri')])])

D.frame(T('Case study: Uhlig (2005)', 'Studiu de caz: Uhlig (2005)'), items(
    (T(r'The paper: six-variable monthly US VAR(12), no constant, 1965:1--2003:12; a contractionary shock raises the funds rate and lowers prices, commodity prices and nonborrowed reserves for months 0--5 \refUhl', r'Lucrarea: VAR(12) lunar pentru SUA cu șase variabile, fără termen liber, 1965:1--2003:12; un șoc contracționist crește dobînda federal funds și scade prețurile, prețurile materiilor prime și rezervele neîmprumutate în lunile 0--5 \refUhl'),
     [T('output is not restricted: the question is its sign', 'producția nu este restricționată: întrebarea este chiar semnul ei')]),
    (T(r'Our replication: the same restrictions and sample; IP and CPI replace the interpolated monthly GDP and deflator of the paper (data of \refRam)', r'Replicarea noastră: aceleași restricții și același eșantion; IP și IPC înlocuiesc PIB-ul și deflatorul interpolate lunar din lucrare (datele din \refRam)'),
     [T(r'flat Normal--inverse-Wishart posterior, @{uh.nd} draws, Haar impulse vectors; accepted: @{uh.n} draws; at the OLS estimate @{uh.acc}\% of rotations satisfy the signs', r'distribuție a posteriori Normal--inverse-Wishart cu prior plat, @{uh.nd} extrageri, vectori de impuls Haar; acceptate: @{uh.n} extrageri; la estimația OLS, @{uh.acc}\% dintre rotații respectă semnele')]),
    T('Question: does a contractionary monetary shock lower output when output is left free?', 'Întrebarea: scade un șoc monetar contracționist producția atunci cînd producția este lăsată liberă?')), 'small')

chart(T('An agnostic monetary policy shock', 'Un șoc de politică monetară agnostic'), 'ats_ch3_uhlig', 'ATS_ch3_sign_restrictions', [
    T(r'One-standard-deviation shock; posterior median and 16--84\% band; dashed: 1--99\% range of the identified set at the OLS estimate; shaded: restricted months', r'Șoc de o abatere standard; mediana a posteriori și banda 16--84\%; linia întreruptă: intervalul 1--99\% al mulțimii identificate la estimația OLS; zona colorată: lunile restricționate')],
    h='0.52\\textheight')

interp(('the agnostic responses', 'răspunsurilor agnostice'), [
    T(r'Output after 12 months: median @{uh.ip12}\%, band [@{uh.ip12lo}, @{uh.ip12hi}]; @{uh.neg}\% of draws negative: no evidence that output falls', r'Producția după 12 luni: mediana @{uh.ip12}\%, banda [@{uh.ip12lo}, @{uh.ip12hi}]; @{uh.neg}\% dintre extrageri negative: nicio dovadă că producția scade'),
    T(r'The identified set at the OLS estimate spans [@{uh.s12lo}, @{uh.s12hi}]: the data with the signs cannot sign output', r'Mulțimea identificată la estimația OLS acoperă [@{uh.s12lo}, @{uh.s12hi}]: datele împreună cu semnele nu pot determina semnul producției'),
    T(r'Prices fall persistently (@{uh.p24}\% after 24 months) without a price puzzle, because the restriction rules it out', r'Prețurile scad persistent (@{uh.p24}\% după 24 de luni), fără anomalia prețurilor, pentru că restricția o exclude'),
    T('Uhlig\'s conclusion, confirmed: neutrality of monetary policy shocks for output is not inconsistent with the data', 'Concluzia lui Uhlig, confirmată: neutralitatea șocurilor de politică monetară pentru producție nu este incompatibilă cu datele')])

D.frame(T('Inference under set identification', 'Inferența sub identificarea pe mulțimi'), items(
    (T(r'The posterior median is not a structural model: at each horizon it can come from a different rotation \refFP', r'Mediana a posteriori nu este un model structural: la fiecare orizont poate proveni dintr-o altă rotație \refFP'),
     [T('report a single admissible model close to the median (median target) or, better, the whole set', 'raportați un singur model admisibil apropiat de mediană (median target) sau, mai bine, întreaga mulțime')]),
    (T(r'The Haar prior is informative about the responses \refBHa; \refGKi\ propose robust Bayes: report the range of posterior means over all priors on $Q$', r'Distribuția a priori Haar este informativă pentru răspunsuri \refBHa; \refGKi\ propun Bayes robust: raportați intervalul mediilor a posteriori peste toate distribuțiile a priori pentru $Q$'),
     [T('the robust band is wider and honest: it separates what the data say from what the prior says', 'banda robustă este mai largă și onestă: separă ce spun datele de ce spune distribuția a priori')]),
    T('Tighten the set with more information: more signs, zeros \\refARW, narrative events, elasticity bounds \\refBHb', 'Restrîngeți mulțimea cu mai multă informație: mai multe semne, zerouri \\refARW, evenimente narative, limite pentru elasticități \\refBHb')), 'small')

D.frame(T('Narrative restrictions', 'Restricții narative'), two(
    ph('volcker', T('Paul Volcker, Fed Chairman 1979--1987', 'Paul Volcker, președintele Fed 1979--1987'), h='0.34\\textheight'),
    items((T(r'\refADRR: restrict the structural shocks at specific dates, not the responses', r'\refADRR: restricționăm șocurile structurale la anumite date, nu răspunsurile'),
           [T('October 1979 (the Volcker shift to reserve targeting) was a positive monetary policy shock', 'octombrie 1979 (trecerea lui Volcker la țintirea rezervelor) a fost un șoc pozitiv de politică monetară'),
            T('and it was the main contributor to the unexpected change of the funds rate that month', 'și a fost principalul factor al modificării neașteptate a dobînzii federal funds în acea lună')]),
          (T('A few credible events remove most of the rotations that sign restrictions alone leave', 'Cîteva evenimente credibile elimină majoritatea rotațiilor lăsate de restricțiile de semn singure'),
           [T('the likelihood must be reweighted by the probability of satisfying the narrative (importance sampling)', 'verosimilitatea trebuie reponderată cu probabilitatea respectării restricției narative (eșantionare de importanță)')]),
          T('With narrative restrictions output falls after a contractionary shock, unlike in the agnostic set', 'Cu restricții narative, producția scade după un șoc contracționist, spre deosebire de mulțimea agnostică')), '0.36', '0.62'), 'footnotesize')

D.frame(T('Identification through heteroskedasticity', 'Identificarea prin heteroscedasticitate'), items(
    (T(r'If the variances of the structural shocks change across regimes while $B_0$ stays fixed: $\Sigma_1 = B_0B_0\'$, $\Sigma_2 = B_0\Lambda B_0\'$, $\Lambda$ diagonal \refRig', r'Dacă varianțele șocurilor structurale se schimbă între regimuri, iar $B_0$ rămîne fix: $\Sigma_1 = B_0B_0\'$, $\Sigma_2 = B_0\Lambda B_0\'$, $\Lambda$ diagonală \refRig'),
     [T(r'then $\Sigma_1^{-1}\Sigma_2 = B_0^{-1\prime}\Lambda B_0\'$: the columns of $B_0$ follow from an eigendecomposition, unique if the $\lambda_i$ are distinct', r'atunci $\Sigma_1^{-1}\Sigma_2 = B_0^{-1\prime}\Lambda B_0\'$: coloanele lui $B_0$ rezultă dintr-o descompunere în valori proprii, unică dacă $\lambda_i$ sînt distincte'),
      T(r'regimes: known dates (crises, policy announcements) or estimated (Markov switching, GARCH) \refLL', r'regimuri: date cunoscute (crize, anunțuri de politică) sau estimate (Markov switching, GARCH) \refLL')]),
    (T('Statistical identification gives shocks without names: labelling them still needs economics (signs)', 'Identificarea statistică dă șocuri fără nume: etichetarea lor cere tot argumente economice (semne)'),
     [T('the assumption that $B_0$ is the same in both regimes is strong and testable only partly', 'ipoteza că $B_0$ este același în ambele regimuri este puternică și se poate testa doar parțial')]),
    T('Seminar 3, A8 recovers $B_0$ from two covariance matrices by hand; Chapter 7 develops regime switching', 'Seminarul 3, A8 recuperează $B_0$ din două matrice de covarianță de mînă; Capitolul 7 dezvoltă modelele cu schimbare de regim')), 'small')

D.recap(('Sign restrictions and set identification', 'restricții de semn și identificarea pe mulțimi'), [
    T('Signs give a set of models; report the set, not only the posterior median', 'Semnele dau o mulțime de modele; raportați mulțimea, nu doar mediana a posteriori'),
    T('Uhlig: with prices, rates and reserves restricted, output can go either way', 'Uhlig: cu prețurile, dobînzile și rezervele restricționate, producția poate evolua în orice sens'),
    T('The Haar prior matters; robust Bayes and narrative restrictions sharpen honest conclusions', 'Distribuția a priori Haar contează; Bayes robust și restricțiile narative întăresc concluziile oneste'),
    T('Heteroskedasticity identifies statistically; economics still names the shocks', 'Heteroscedasticitatea identifică statistic; economia dă încă numele șocurilor')])

# =============================================================================
# 6. INSTRUMENTE EXTERNE
# =============================================================================
D.section('External instruments', 'Instrumente externe')

D.frame(T('The proxy SVAR', 'Modelul proxy SVAR'), items(
    (T(r'An external variable $z_t$ (the proxy) with \textbf{relevance} $\E z_t\varepsilon_{1t} = \alpha \ne 0$ and \textbf{exogeneity} $\E z_t\varepsilon_{jt} = 0$, $j \ne 1$', r'O variabilă externă $z_t$ (proxy) cu \textbf{relevanță} $\E z_t\varepsilon_{1t} = \alpha \ne 0$ și \textbf{exogenitate} $\E z_t\varepsilon_{jt} = 0$, $j \ne 1$'),
     [T(r'then $\E u_tz_t = B_0\E\varepsilon_tz_t = \alpha b_1$: the covariance of the residuals with the proxy is proportional to the impact column $b_1$', r'atunci $\E u_tz_t = B_0\E\varepsilon_tz_t = \alpha b_1$: covarianța reziduurilor cu proxy-ul este proporțională cu coloana de impact $b_1$')]),
    (T(r'Normalise $b_{11} = 1$ (or a 25 bp rate increase): $b_{i1}/b_{11} = \E(u_{it}z_t)/\E(u_{1t}z_t)$, a 2SLS of $u_{it}$ on $u_{1t}$ with instrument $z_t$ \refSWb, \refMR', r'Normalizăm $b_{11} = 1$ (sau o creștere a dobînzii de 25 bp): $b_{i1}/b_{11} = \E(u_{it}z_t)/\E(u_{1t}z_t)$, o regresie 2SLS a lui $u_{it}$ pe $u_{1t}$ cu instrumentul $z_t$ \refSWb, \refMR'),
     [T(r'responses $\Theta_{h,\cdot1} = \Phi_hb_1$; the proxy may be noisy, short or available only for a sub-sample', r'răspunsurile $\Theta_{h,\cdot1} = \Phi_hb_1$; proxy-ul poate fi zgomotos, scurt sau disponibil doar pe un subeșantion')]),
    T('Only one column of $B_0$ is identified, and no zero restriction is needed', 'Se identifică o singură coloană a lui $B_0$, fără nicio restricție zero')), 'small')

D.frame(T('High-frequency identification of monetary policy', 'Identificarea politicii monetare la frecvență înaltă'), items(
    (T(r'Surprise = change of futures-implied rates in a narrow window (30 minutes) around an FOMC announcement \refKut, \refGSS', r'Surpriza = modificarea dobînzilor implicite din futures într-o fereastră îngustă (30 de minute) în jurul unui anunț FOMC \refKut, \refGSS'),
     [T('within 30 minutes nothing else systematic happens: exogeneity by design', 'în 30 de minute nu se întîmplă nimic altceva sistematic: exogenitate prin construcție'),
      T(r'FF4: the three-month-ahead federal funds futures; it captures forward guidance as well as the current decision \refGK', r'FF4: contractul futures federal funds peste trei luni; surprinde atît deciziile curente, cît și forward guidance \refGK')]),
    (T(r'Complications: the \textbf{information effect} \refNS: a tightening can signal good news about the economy', r'Complicații: \textbf{efectul informațional} \refNS: o înăsprire poate semnala vești bune despre economie'),
     [T(r'\refJK\ separate pure policy and information shocks with the co-movement of rates and stock prices (sign restrictions on surprises)', r'\refJK\ separă șocurile pure de politică de cele informaționale prin co-mișcarea dobînzilor și a prețurilor acțiunilor (restricții de semn asupra surprizelor)'),
      T(r'surprises are predictable from past macro news \refBS: orthogonalise them before use', r'surprizele sînt previzibile din știrile macro anterioare \refBS: ortogonalizați-le înainte de folosire')])), 'small')

D.frame(T('Case study: Gertler and Karadi (2015)', 'Studiu de caz: Gertler și Karadi (2015)'), items(
    (T(r'The paper: the 1-year Treasury yield as policy indicator (it captures forward guidance), log IP, log CPI and the excess bond premium of Gilchrist and Zakrajšek; VAR(12), 1979:7--2012:6 \refGK', r'Lucrarea: randamentul titlurilor de stat la 1 an ca indicator de politică (surprinde forward guidance), log IP, log IPC și prima de risc excedentară a obligațiunilor (Gilchrist și Zakrajšek); VAR(12), 1979:7--2012:6 \refGK'),
     [T('instrument: FF4 surprises, monthly, 1991:1--2012:6; the residuals of the full sample are used for the proxy regression on the overlap', 'instrumentul: surprizele FF4, lunar, 1991:1--2012:6; reziduurile eșantionului complet sînt folosite în regresia pe proxy pe perioada comună')]),
    (T(r'Our replication: the same variables, sample and instrument (replication files of \refRam), $T = @{gk.T}$, $@{gk.Tz}$ months with the instrument', r'Replicarea noastră: aceleași variabile, același eșantion și același instrument (fișierele de replicare din \refRam), $T = @{gk.T}$, $@{gk.Tz}$ de luni cu instrument'),
     [T(r'first stage: robust $F = @{gk.F}$ (homoskedastic @{gk.Fh}), $R^2 = @{gk.r2}\%$; 90\% moving-block bootstrap bands \refJL', r'prima etapă: $F$ robust $= @{gk.F}$ (homoscedastic @{gk.Fh}), $R^2 = @{gk.r2}\%$; benzi bootstrap pe blocuri mobile de 90\% \refJL')]),
    T('Question: does a policy surprise move credit spreads, and with what effect on activity?', 'Întrebarea: mișcă o surpriză de politică prima de risc a creditului și ce efect are asupra activității?')), 'small')

chart(T('A monetary policy shock identified with FF4 surprises', 'Un șoc de politică monetară identificat cu surprizele FF4'), 'ats_ch3_gk', 'ATS_ch3_proxy_svar', [
    T(r'Shock normalised to raise the 1-year yield by 25 bp on impact; 68\% and 90\% moving-block bootstrap bands', r'Șoc normalizat să crească randamentul la 1 an cu 25 bp la impact; benzi bootstrap pe blocuri mobile de 68\% și 90\%')],
    h='0.52\\textheight')

interp(('the proxy SVAR', 'modelului proxy SVAR'), [
    T(r'The excess bond premium jumps by @{gk.ebp0} pp on impact (band [@{gk.ebp0lo}, @{gk.ebp0hi}]): monetary policy works through credit costs, as in the paper', r'Prima de risc excedentară crește cu @{gk.ebp0} pp la impact (banda [@{gk.ebp0lo}, @{gk.ebp0hi}]): politica monetară acționează prin costul creditului, ca în lucrare'),
    T(r'IP reaches @{gk.ipmin}\% after @{gk.iparg} months (band [@{gk.ipminlo}, @{gk.ipminhi}]); CPI is @{gk.cpi24}\% after two years (band [@{gk.cpi24lo}, @{gk.cpi24hi}]), with no price puzzle', r'IP ajunge la @{gk.ipmin}\% după @{gk.iparg} luni (banda [@{gk.ipminlo}, @{gk.ipminhi}]); IPC este @{gk.cpi24}\% după doi ani (banda [@{gk.cpi24lo}, @{gk.cpi24hi}]), fără anomalia prețurilor'),
    T(r'$F = @{gk.F}$ passes the rule of thumb $F > 10$, but the price response is imprecise: weak-instrument-robust bands are wider \refMSW', r'$F = @{gk.F}$ trece pragul empiric $F > 10$, dar răspunsul prețurilor este imprecis: benzile robuste la instrumente slabe sînt mai largi \refMSW')])

D.frame(T('Inference with an external instrument', 'Inferența cu un instrument extern'), items(
    (T(r'Weak instruments: when $\alpha$ is small, the ratio $\E(u_iz)/\E(u_1z)$ is badly estimated and delta-method bands undercover', r'Instrumente slabe: cînd $\alpha$ este mic, raportul $\E(u_iz)/\E(u_1z)$ se estimează prost, iar benzile prin metoda delta au acoperire prea mică'),
     [T(r'\refMSW: Anderson--Rubin-type confidence sets, valid for any strength; they can be unbounded', r'\refMSW: mulțimi de încredere de tip Anderson--Rubin, valabile pentru orice tărie a instrumentului; pot fi nemărginite'),
      T(r'report the first-stage $F$ with HAC variance; the rule $F > 10$ is a heuristic, not a test', r'raportați statistica $F$ din prima etapă cu varianță HAC; regula $F > 10$ este o euristică, nu un test')]),
    (T(r'Bootstrap: the wild bootstrap of \refMR\ is invalid for proxy SVARs; use the moving-block bootstrap of residuals and instrument jointly \refJL', r'Bootstrap: bootstrap-ul wild din \refMR\ nu este valid pentru proxy SVAR; folosiți bootstrap-ul pe blocuri mobile al reziduurilor și al instrumentului împreună \refJL'),
     [T('the block keeps the dependence between the squared shock and the instrument', 'blocul păstrează dependența dintre pătratul șocului și instrument')]),
    T('Seminar 3, A5 computes relative impacts and $F$ by hand; C1 builds an Anderson--Rubin set for Romania', 'Seminarul 3, A5 calculează de mînă impacturile relative și $F$; C1 construiește o mulțime Anderson--Rubin pentru România')), 'small')

D.recap(('External instruments', 'instrumente externe'), [
    T('Relevance + exogeneity of a proxy identify one column of $B_0$, with no zeros', 'Relevanța și exogenitatea unui proxy identifică o coloană a lui $B_0$, fără zerouri'),
    T('High-frequency surprises are the best proxies we have; check the information effect and predictability', 'Surprizele de frecvență înaltă sînt cele mai bune proxy-uri disponibile; verificați efectul informațional și previzibilitatea'),
    T(r'GK replicated: credit spreads jump, output falls; $F = @{gk.F}$', r'GK replicat: prima de risc a creditului crește, producția scade; $F = @{gk.F}$'),
    T('Use weak-IV-robust sets and the block bootstrap', 'Folosiți mulțimi robuste la instrumente slabe și bootstrap-ul pe blocuri')])

# =============================================================================
# 7. INFERENȚA PENTRU IRF
# =============================================================================
D.section('Inference for impulse responses', 'Inferența pentru funcțiile de răspuns la impuls')

D.frame(T('Delta method and its limits', 'Metoda delta și limitele ei'), items(
    (T(r'$\hat\Theta_h = g(\hat\beta, \hat\sigma)$ is a smooth function of the VAR estimates: $\sqrt T(\hat\Theta_h - \Theta_h) \to N(0, G\Sigma G\')$ \refLut', r'$\hat\Theta_h = g(\hat\beta, \hat\sigma)$ este o funcție netedă de estimațiile VAR: $\sqrt T(\hat\Theta_h - \Theta_h) \to N(0, G\Sigma G\')$ \refLut'),
     [T(r'$G = \partial g/\partial(\beta, \sigma)$ in closed form; quick, but symmetric bands', r'$G = \partial g/\partial(\beta, \sigma)$ în formă închisă; rapid, dar cu benzi simetrice')]),
    (T('It fails where we need it most', 'Eșuează exact unde avem cea mai mare nevoie de ea'),
     [T('near unit roots and at long horizons the distribution of $\\hat\\Theta_h$ is skewed and non-Normal', 'în apropierea rădăcinilor unitare și la orizonturi lungi distribuția lui $\\hat\\Theta_h$ este asimetrică și ne-Normală'),
      T('the covariance $G\\Sigma G\'$ can be singular (e.g.\\ when a response is zero by construction)', 'covarianța $G\\Sigma G\'$ poate fi singulară (de exemplu cînd un răspuns este zero prin construcție)'),
      T('OLS slope estimates are biased towards zero in small samples, so responses decay too fast', 'estimațiile OLS ale pantelor sînt deplasate spre zero în eșantioane mici, deci răspunsurile scad prea repede')]),
    T('Hence the bootstrap, and the bias correction', 'De aici bootstrap-ul și corecția deplasării')), 'small')

D.frame(T('Bootstrap schemes for VARs', 'Scheme bootstrap pentru VAR'), items(
    (T(r'\textbf{Residual (recursive-design)}: resample $\hat u_t$ i.i.d., rebuild $y^*_t$ recursively from the estimated VAR, re-estimate, identify, repeat', r'\textbf{Pe reziduuri (design recursiv)}: reeșantionăm $\hat u_t$ i.i.d., reconstruim $y^*_t$ recursiv din VAR-ul estimat, reestimăm, identificăm, repetăm'),
     [T('valid with i.i.d.\\ innovations; the percentile (or Hall) interval of the $B$ responses gives the band', 'valid cu inovații i.i.d.; intervalul percentilelor (sau Hall) al celor $B$ răspunsuri dă banda')]),
    (T(r'\textbf{Wild}: $u^*_t = \eta_t\hat u_t$, $\eta_t = \pm1$ with probability $1/2$: robust to conditional heteroskedasticity \refGoK', r'\textbf{Wild}: $u^*_t = \eta_t\hat u_t$, $\eta_t = \pm1$ cu probabilitatea $1/2$: robust la heteroscedasticitate condiționată \refGoK'),
     [T('used for the oil VAR: commodity markets have volatility clustering', 'folosit pentru VAR-ul petrolului: piețele de materii prime au volatility clustering')]),
    (T(r'\textbf{Moving block}: resample blocks of consecutive $(\hat u_t, z_t)$; needed whenever higher moments matter (proxy SVAR) \refJL', r'\textbf{Pe blocuri mobile}: reeșantionăm blocuri de valori consecutive $(\hat u_t, z_t)$; necesar ori de cîte ori contează momentele de ordin superior (proxy SVAR) \refJL'),
     [T('block length of order $T^{1/4}$; Chapter 0 covered the choice', 'lungimea blocului de ordinul $T^{1/4}$; Capitolul 0 a tratat alegerea ei')])), 'small')

D.frame(T("Kilian's bias-corrected bootstrap", 'Bootstrap-ul cu corecția deplasării al lui Kilian'), items(
    (T(r'\refKilA: (1) bootstrap the bias $\hat b = \bar A^* - \hat A$; (2) correct $\tilde A = \hat A - \hat b$, shrinking the correction if $\tilde A$ is not stationary; (3) bootstrap again from $\tilde A$ and correct each replicate', r'\refKilA: (1) estimăm prin bootstrap deplasarea $\hat b = \bar A^* - \hat A$; (2) corectăm $\tilde A = \hat A - \hat b$, micșorînd corecția dacă $\tilde A$ nu este staționar; (3) aplicăm din nou bootstrap-ul pornind de la $\tilde A$ și corectăm fiecare replicare'),
     [T('the ``bootstrap after bootstrap\'\' recentres the distribution where OLS bias is large: persistent series, short samples', '„bootstrap după bootstrap” recentrează distribuția acolo unde deplasarea OLS este mare: serii persistente, eșantioane scurte')]),
    (T(r'Oil VAR: mean absolute bias @{kb.mean} per coefficient; largest root @{kb.root} before, @{kb.rootc} after the (shrunk) correction', r'VAR-ul petrolului: deplasarea absolută medie @{kb.mean} pe coeficient; cea mai mare rădăcină @{kb.root} înainte și @{kb.rootc} după corecția (micșorată)'),
     [T(r'12-month response of the price to oil-specific demand: @{kb.p12}\% (OLS), @{kb.p12c}\% (corrected), band [@{kb.lo}, @{kb.hi}]; to aggregate demand: @{kb.ad12}\% and @{kb.ad12c}\%', r'răspunsul prețului după 12 luni la cererea specifică: @{kb.p12}\% (OLS), @{kb.p12c}\% (corectat), banda [@{kb.lo}, @{kb.hi}]; la cererea agregată: @{kb.ad12}\% și @{kb.ad12c}\%')]),
    T('The correction makes responses more persistent; when the VAR in levels has a root above one, the rule of Kilian leaves it uncorrected (Romanian VAR, Section 9)', 'Corecția face răspunsurile mai persistente; cînd VAR-ul în niveluri are o rădăcină peste unu, regula lui Kilian îl lasă necorectat (VAR-ul pentru România, secțiunea 9)')), 'small')

D.frame(T('Pointwise and joint bands', 'Benzi punctuale și benzi simultane'), items(
    (T(r'A pointwise 90\% band covers $\Theta_h$ at each $h$ separately; the whole path lies inside it with much lower probability', r'O bandă punctuală de 90\% acoperă $\Theta_h$ la fiecare $h$ separat; întreaga traiectorie se află în ea cu o probabilitate mult mai mică'),
     [T(r'questions about the \emph{shape} (``output falls for two years\'\') need simultaneous bands \refMOPa', r'întrebările despre \emph{formă} („producția scade doi ani”) cer benzi simultane \refMOPa'),
      T('sup-$t$ band: scale the pointwise standard errors by the $1 - \\alpha$ quantile of $\\max_h|t_h|$ from the bootstrap', 'banda sup-$t$: înmulțim erorile standard punctuale cu cuantila $1 - \\alpha$ a lui $\\max_h|t_h|$ din bootstrap')]),
    (T('Bayesian bands (posterior quantiles) answer a different question: probability statements given the prior', 'Benzile bayesiene (cuantile a posteriori) răspund la o altă întrebare: afirmații probabilistice date fiind distribuțiile a priori'),
     [T('Chapter 5 builds them with Minnesota and Normal--inverse-Wishart priors; with set identification they mix prior and data (previous section)', 'Capitolul 5 le construiește cu distribuții a priori Minnesota și Normal--inverse-Wishart; la identificarea pe mulțimi ele amestecă distribuția a priori și datele (secțiunea anterioară)')]),
    T('Always state: pointwise or joint, frequentist or Bayesian, the level (68\\%, 90\\%, 95\\%)', 'Precizați întotdeauna: punctuală sau simultană, frecventistă sau bayesiană, nivelul (68\\%, 90\\%, 95\\%)')), 'small')

D.recap(('Inference for impulse responses', 'inferența pentru răspunsurile la impuls'), [
    T('Delta-method bands are symmetric and fail near unit roots', 'Benzile prin metoda delta sînt simetrice și eșuează în apropierea rădăcinilor unitare'),
    T('Residual, wild and block bootstraps match i.i.d., heteroskedastic and proxy settings', 'Bootstrap-ul pe reziduuri, wild și pe blocuri corespunde cazurilor i.i.d., heteroscedastic și proxy'),
    T('Kilian\'s correction removes small-sample bias; it is not applied to explosive estimates', 'Corecția lui Kilian elimină deplasarea din eșantioane mici; nu se aplică estimațiilor explozive'),
    T('Shape questions need joint bands; Bayesian bands come in Chapter 5', 'Întrebările despre formă cer benzi simultane; benzile bayesiene vin în Capitolul 5')])

# =============================================================================
# 8. PROIECȚII LOCALE
# =============================================================================
D.section('Local projections', 'Proiecții locale')

D.frame(T('Local projections', 'Proiecțiile locale'), items(
    (T(r'\refJorda: one regression per horizon, $y_{i,t+h} = \mu_h + \beta_hx_t + \gamma_h\'w_t + \xi_{t+h}$, $h = 0, 1, \dots, H$', r'\refJorda: o regresie pentru fiecare orizont, $y_{i,t+h} = \mu_h + \beta_hx_t + \gamma_h\'w_t + \xi_{t+h}$, $h = 0, 1, \dots, H$'),
     [T(r'$x_t$: the shock (or the policy variable with controls $w_t$ that make it as good as random); $\hat\beta_h$ is the impulse response', r'$x_t$: șocul (sau variabila de politică cu controalele $w_t$ care o fac practic aleatoare); $\hat\beta_h$ este răspunsul la impuls'),
      T(r'no iteration of a model: a misspecified dynamic does not compound across horizons', r'nicio iterare a unui model: o dinamică greșit specificată nu se acumulează de la un orizont la altul')]),
    (T(r'The error $\xi_{t+h}$ is serially correlated (an MA($h - 1$) at least): HAC standard errors with $h + 1$ lags, or', r'Eroarea $\xi_{t+h}$ este autocorelată (cel puțin MA($h - 1$)): erori standard HAC cu $h + 1$ decalaje, sau'),
     [T(r'\textbf{lag augmentation} \refMOPb: add one more lag of the controls and use Eicker--Huber--White errors; valid uniformly over persistence, even near a unit root', r'\textbf{decalaje suplimentare} \refMOPb: adăugăm încă un decalaj al controalelor și folosim erori Eicker--Huber--White; valid uniform după persistență, chiar lîngă o rădăcină unitară')]),
    T('Flexible: nonlinear terms, state dependence, panel data, cumulative outcomes all enter as regressors', 'Flexibile: termenii neliniari, dependența de stare, datele panel și variabilele cumulate intră toate ca regresori')), 'small')

D.frame(T('LP and VAR estimate the same responses', 'LP și VAR estimează aceleași răspunsuri'), items(
    (T(r'\refPW: in population, an LP with $p$ lags of all variables as controls and a VAR($p$) with the same ordering give \emph{identical} responses up to horizon $p$', r'\refPW: în populație, o LP cu $p$ decalaje ale tuturor variabilelor drept controale și un VAR($p$) cu aceeași ordonare dau răspunsuri \emph{identice} pînă la orizontul $p$'),
     [T(r'with unrestricted lags ($p \to \infty$) they coincide at all horizons: the choice is about estimation, not identification', r'cu decalaje nerestricționate ($p \to \infty$) coincid la toate orizonturile: alegerea privește estimarea, nu identificarea'),
      T(r'any VAR identification scheme (recursive, external instrument) has an LP counterpart, and vice versa', r'orice schemă de identificare VAR (recursivă, instrument extern) are un echivalent LP și invers')]),
    (T('In finite samples they differ: the VAR extrapolates the first $p$ autocovariances, the LP uses the raw $h$-step covariance', 'În eșantioane finite diferă: VAR-ul extrapolează primele $p$ autocovarianțe, LP folosește direct covarianța la $h$ pași'),
     [T('the next slide quantifies this', 'slide-ul următor cuantifică această diferență')])), 'small')

chart(T('Bias and variance: LP against VAR (simulation)', 'Deplasare și varianță: LP comparat cu VAR (simulare)'), 'ats_ch3_lp_sim', 'ATS_ch3_lp_vs_var', [
    T(r'DGP: $x_t = 0.5x_{t-1} + e_t$, $y_t = 0.6y_{t-1} + \sum_{j=0}^{11}\psi_je_{t-j} + u_t$ (hump-shaped $\psi_j$), $T = @{ls.T}$, @{ls.reps} replications; a VAR(2) is misspecified', r'DGP: $x_t = 0.5x_{t-1} + e_t$, $y_t = 0.6y_{t-1} + \sum_{j=0}^{11}\psi_je_{t-j} + u_t$ ($\psi_j$ în formă de cocoașă), $T = @{ls.T}$, @{ls.reps} de replicări; un VAR(2) este greșit specificat')],
    h='0.52\\textheight')

interp(('the bias--variance trade-off', 'compromisului deplasare--varianță'), [
    (T(r'At $h = 8$ (true response @{ls.true8}): VAR(2) bias @{ls.VAR2.bias8}, LP(2) bias @{ls.LP2.bias8}; RMSE @{ls.VAR2.rmse8} and @{ls.LP2.rmse8}', r'La $h = 8$ (răspunsul adevărat @{ls.true8}): deplasarea VAR(2) @{ls.VAR2.bias8}, a LP(2) @{ls.LP2.bias8}; RMSE @{ls.VAR2.rmse8} și @{ls.LP2.rmse8}'),
     [T('where the short VAR misses the hump, its bias dominates the error', 'acolo unde VAR-ul scurt ratează cocoașa, deplasarea lui domină eroarea')]),
    T(r'At $h = 16$: standard deviation @{ls.VAR2.sd16} (VAR(2)) against @{ls.LP2.sd16} (LP(2)); RMSE @{ls.VAR2.rmse16} against @{ls.LP2.rmse16}: the biased VAR wins', r'La $h = 16$: abaterea standard @{ls.VAR2.sd16} (VAR(2)) față de @{ls.LP2.sd16} (LP(2)); RMSE @{ls.VAR2.rmse16} față de @{ls.LP2.rmse16}: VAR-ul deplasat cîștigă'),
    T(r'The general lesson of \refLPW\ (thousands of DGPs): LP has low bias and high variance; VAR (and shrinkage VARs) have lower MSE unless the analyst cares almost only about bias', r'Lecția generală din \refLPW\ (mii de DGP): LP are deplasare mică și varianță mare; VAR (și VAR-urile cu shrinkage) au MSE mai mic, cu excepția cazului în care analistul ține aproape doar la deplasare'),
    T('A long VAR(12) behaves like LP: few lags = more bias, less variance', 'Un VAR(12) lung se comportă ca LP: puține decalaje = mai multă deplasare, mai puțină varianță')])

D.frame(T('LP-IV', 'LP-IV'), items(
    (T(r'\refSWc: $y_{i,t+h} = \theta_{h,i}\,y_{1t} + \gamma\'w_t + \xi_{t+h}$, with $y_{1t}$ (the policy rate) instrumented by $z_t$', r'\refSWc: $y_{i,t+h} = \theta_{h,i}\,y_{1t} + \gamma\'w_t + \xi_{t+h}$, cu $y_{1t}$ (dobînda de politică) instrumentată prin $z_t$'),
     [T(r'$\theta_{h,i}$ = response of $y_i$ after $h$ periods to a shock that raises $y_1$ by one unit on impact', r'$\theta_{h,i}$ = răspunsul lui $y_i$ după $h$ perioade la un șoc care crește $y_1$ cu o unitate la impact'),
      T(r'conditions: relevance, contemporaneous exogeneity and \textbf{lead-lag exogeneity} $\E z_t\varepsilon_{t+j} = 0$ for $j \ne 0$, given $w_t$', r'condiții: relevanța, exogenitatea contemporană și \textbf{exogenitatea pe decalaje și avansuri} $\E z_t\varepsilon_{t+j} = 0$ pentru $j \ne 0$, dat fiind $w_t$')]),
    (T('Same identifying information as the proxy SVAR; different estimator', 'Aceeași informație de identificare ca proxy SVAR; alt estimator'),
     [T(r'the proxy SVAR needs invertibility of the shock; LP-IV does not, but pays in variance', r'proxy SVAR cere inversabilitatea șocului; LP-IV nu, dar plătește prin varianță'),
      T(r'cumulative LP-IV gives multipliers: $\sum_{j\le h}y_{t+j}$ on $\sum_{j\le h}g_{t+j}$ instrumented by $z_t$ \refRZ', r'LP-IV cumulat dă multiplicatori: $\sum_{j\le h}y_{t+j}$ pe $\sum_{j\le h}g_{t+j}$, instrumentat prin $z_t$ \refRZ')])), 'small')

chart(T('The same instrument, two estimators', 'Același instrument, doi estimatori'), 'ats_ch3_lp_gk', 'ATS_ch3_lp_vs_var', [
    T(r'LP-IV with FF4 as instrument for the 1-year yield, 2 lags of all variables and of the instrument as controls, origins 1990:1--2012:6 ($T = @{lg.T}$) \refRam; dashed: the proxy SVAR', r'LP-IV cu FF4 ca instrument pentru randamentul la 1 an, 2 decalaje ale tuturor variabilelor și ale instrumentului drept controale, origini 1990:1--2012:6 ($T = @{lg.T}$) \refRam; linia întreruptă: proxy SVAR')],
    h='0.52\\textheight')

interp(('LP-IV against the proxy SVAR', 'comparației LP-IV cu proxy SVAR'), [
    T(r'Impact first stage $F = @{lg.F0}$; after 24 months IP: LP-IV @{lg.ip24}\% (SE @{lg.ip24se}), proxy SVAR @{lg.svip24}\%', r'Prima etapă la impact: $F = @{lg.F0}$; după 24 de luni IP: LP-IV @{lg.ip24}\% (SE @{lg.ip24se}), proxy SVAR @{lg.svip24}\%'),
    T(r'CPI after 24 months: LP-IV @{lg.cpi24}\% (SE @{lg.cpi24se}), proxy SVAR @{lg.svcpi24}\%: the LP bands contain the VAR path almost everywhere', r'IPC după 24 de luni: LP-IV @{lg.cpi24}\% (SE @{lg.cpi24se}), proxy SVAR @{lg.svcpi24}\%: benzile LP conțin traiectoria VAR aproape peste tot'),
    (T(r'LP-IV implies a much more persistent rise of the yield: the two estimators answer slightly different questions when the policy path differs', r'LP-IV implică o creștere mult mai persistentă a randamentului: cei doi estimatori răspund la întrebări ușor diferite cînd traiectoria dobînzii diferă'),
     [T(r'the positive LP output response, noted by \refRam, is imprecise and sensitive to the sample: do not read it as expansionary tightening', r'răspunsul pozitiv al producției în LP, semnalat de \refRam, este imprecis și sensibil la eșantion: nu îl citiți ca o înăsprire expansionistă')])])

D.frame(T('State-dependent local projections', 'Proiecții locale dependente de stare'), items(
    (T(r'Interact everything with a lagged state indicator $I_{t-1}$: $y_{t+h} = I_{t-1}[\alpha_{A,h} + \beta_{A,h}x_t + \dots] + (1 - I_{t-1})[\alpha_{B,h} + \beta_{B,h}x_t + \dots] + \xi_{t+h}$', r'Interacționăm totul cu un indicator de stare decalat $I_{t-1}$: $y_{t+h} = I_{t-1}[\alpha_{A,h} + \beta_{A,h}x_t + \dots] + (1 - I_{t-1})[\alpha_{B,h} + \beta_{B,h}x_t + \dots] + \xi_{t+h}$'),
     [T('the state may change after the shock: LP measures the average response given the initial state, including transitions', 'starea se poate schimba după șoc: LP măsoară răspunsul mediu dată fiind starea inițială, inclusiv tranzițiile'),
      T('no need to model the state dynamics, unlike a threshold or a smooth-transition VAR (Chapter 2)', 'nu este nevoie să modelăm dinamica stării, spre deosebire de un VAR cu prag sau cu tranziție netedă (Capitolul 2)')]),
    (T(r'Case study \refRZ: are government spending multipliers larger in slack times?', r'Studiu de caz \refRZ: sînt multiplicatorii cheltuielilor publice mai mari în perioadele de subutilizare a resurselor?'),
     [T(r'US quarterly data 1889--2015; military news shock (Ramey) scaled by potential GDP; slack = unemployment $\ge 6.5\%$ in $t - 1$ (@{rz.share}\% of quarters)', r'date trimestriale SUA 1889--2015; șocul de știri militare (Ramey) scalat la PIB-ul potențial; subutilizare = șomaj $\ge 6{,}5\%$ în $t - 1$ (@{rz.share}\% dintre trimestre)'),
      T('cumulative LP-IV of output on government spending, 4 lags of news, output and spending, Newey--West with $h + 1$ lags', 'LP-IV cumulat al producției pe cheltuielile publice, 4 decalaje ale știrilor, producției și cheltuielilor, Newey--West cu $h + 1$ decalaje')])), 'small')

chart(T('Government spending multipliers by state of the economy', 'Multiplicatorii cheltuielilor publice după starea economiei'), 'ats_ch3_rz', 'ATS_ch3_state_dependent_lp', [
    T(r'Cumulative multiplier $\sum_{j\le h}\Delta y_{t+j}/\sum_{j\le h}\Delta g_{t+j}$ by horizon; 95\% Newey--West bands; dashed: multiplier of one', r'Multiplicatorul cumulat $\sum_{j\le h}\Delta y_{t+j}/\sum_{j\le h}\Delta g_{t+j}$ pe orizonturi; benzi Newey--West de 95\%; linia întreruptă: multiplicatorul egal cu unu')],
    h='0.54\\textheight')

interp(('the state-dependent multipliers', 'multiplicatorilor dependenți de stare'), [
    T(r'Linear: @{rz.lin8} at two years (SE @{rz.lin8se}) and @{rz.lin16} at four years (SE @{rz.lin16se})', r'Liniar: @{rz.lin8} la doi ani (SE @{rz.lin8se}) și @{rz.lin16} la patru ani (SE @{rz.lin16se})'),
    T(r'High unemployment: @{rz.slack8} and @{rz.slack16}; low unemployment: @{rz.normal8} and @{rz.normal16}', r'Șomaj ridicat: @{rz.slack8} și @{rz.slack16}; șomaj scăzut: @{rz.normal8} și @{rz.normal16}'),
    T('As in the paper: multipliers below one in both states and no significant difference between them', 'Ca în lucrare: multiplicatori sub unu în ambele stări și nicio diferență semnificativă între ele'),
    T('The case for LP here: a VAR would impose the same dynamics in both states unless the state transitions are modelled', 'Argumentul pentru LP aici: un VAR ar impune aceeași dinamică în ambele stări dacă tranzițiile între stări nu sînt modelate')])

D.recap(('Local projections', 'proiecții locale'), [
    T('LP = one regression per horizon; HAC or lag-augmented inference', 'LP = o regresie pe orizont; inferență HAC sau cu decalaje suplimentare'),
    T('LP and VAR target the same responses; finite samples trade bias for variance', 'LP și VAR țintesc aceleași răspunsuri; eșantioanele finite schimbă deplasare pe varianță'),
    T('LP-IV uses external instruments without invertibility, at a cost in precision', 'LP-IV folosește instrumente externe fără inversabilitate, cu un cost în precizie'),
    T('State dependence is natural in LP: RZ find multipliers below one in slack and in normal times', 'Dependența de stare este naturală în LP: RZ găsesc multiplicatori sub unu și în perioade de subutilizare, și în perioade normale')])

# =============================================================================
# 9. ROMÂNIA
# =============================================================================
D.section('Romania and euro-area spillovers', 'România și efectele de propagare din zona euro')

D.frame(T('Monetary policy in a small open economy', 'Politica monetară într-o economie mică și deschisă'), two(
    ph('bnr', T('The National Bank of Romania, Bucharest', 'Banca Națională a României, București'), h='0.34\\textheight'),
    items((T('The BNR targets inflation since August 2005 (target 2.5\\% $\\pm$ 1 pp since 2013) under a managed float of the leu', 'BNR țintește inflația din august 2005 (ținta 2,5\\% $\\pm$ 1 pp din 2013), cu un curs de schimb flotant administrat al leului'),
           [T('the interbank rate ROBOR 3M transmits the policy rate and liquidity conditions; we use it as the policy indicator', 'dobînda interbancară ROBOR 3M transmite dobînda de politică monetară și condițiile de lichiditate; o folosim ca indicator de politică')]),
          (T('Identification problems specific to Romania', 'Probleme de identificare specifice României'),
           [T('short sample (20 years), structural change (2008--2009, 2020, 2022), administered prices and excise changes', 'eșantion scurt (20 de ani), schimbări structurale (2008--2009, 2020, 2022), prețuri administrate și modificări de accize'),
            T('external shocks dominate: the euro area takes most Romanian exports; ECB policy moves Romanian rates and the leu', 'șocurile externe domină: zona euro preia majoritatea exporturilor românești; politica BCE mișcă dobînzile românești și leul')]),
          T('Our approach: a transparent recursive VAR with the euro area first, then an external ECB shock with LP', 'Abordarea noastră: un VAR recursiv transparent, cu zona euro pe primul loc, apoi un șoc extern BCE cu LP')), '0.36', '0.62'), 'footnotesize')

chart(T('Romanian and euro-area data', 'Date pentru România și zona euro'), 'ats_ch3_ro_data', 'ATS_ch3_romania', [
    T(r'Monthly, @{rd.first}--@{rd.last}: IP (SCA), HICP, 3-month money-market rates (Eurostat), EUR/RON (BNR reference rate, monthly average)', r'Lunar, @{rd.first}--@{rd.last}: IP (ajustată sezonier), IAPC, dobînzile pieței monetare la 3 luni (Eurostat), EUR/RON (cursul de referință BNR, media lunară)')],
    h='0.5\\textheight')

interp(('the Romanian data', 'datelor pentru România'), [
    T(r'HICP inflation peaked at @{rd.imax}\% in @{rd.imaxd} and is @{rd.ilast}\% in the last month; ROBOR 3M reached @{rd.rmax}\% in the 2008 liquidity squeeze', r'Inflația IAPC a atins maximul de @{rd.imax}\% în @{rd.imaxd} și este @{rd.ilast}\% în ultima lună; ROBOR 3M a ajuns la @{rd.rmax}\% în criza de lichiditate din 2008'),
    T(r'EUR/RON rose from @{rd.fx0} to @{rd.fx1}: a trend depreciation with long managed-float plateaus', r'EUR/RON a crescut de la @{rd.fx0} la @{rd.fx1}: o depreciere tendențială cu platouri lungi de flotare administrată'),
    T('Romanian and euro-area IP co-move closely, including the 2020 collapse: a strong case for an external block', 'IP din România și din zona euro evoluează împreună, inclusiv prăbușirea din 2020: un argument puternic pentru un bloc extern'),
    T('Sharp outliers (2008, 2020, 2022) will dominate the estimates of a small VAR: check robustness without them', 'Valorile extreme (2008, 2020, 2022) vor domina estimațiile unui VAR mic: verificați robustețea fără ele')])

D.frame(T('A VAR for Romania with a euro-area block', 'Un VAR pentru România cu un bloc al zonei euro'), items(
    (T(r'$y_t$ = (EA IP, EA HICP, Euribor 3M, RO IP, RO HICP, ROBOR 3M, EUR/RON), logs $\times 100$ except rates; constant and monthly dummies (HICP is not seasonally adjusted)', r'$y_t$ = (IP ZE, IAPC ZE, Euribor 3M, IP RO, IAPC RO, ROBOR 3M, EUR/RON), logaritmi $\times 100$ cu excepția dobînzilor; termen liber și variabile dummy lunare (IAPC nu este ajustat sezonier)'),
     [T(r'lag length: BIC and HQ choose @{rv.bic}, AIC @{rv.aic}; we use 2 ($T = @{rv.T}$); largest root @{rv.root}: levels, near-unit-root, no bias correction', r'numărul de decalaje: BIC și HQ aleg @{rv.bic}, AIC @{rv.aic}; folosim 2 ($T = @{rv.T}$); cea mai mare rădăcină @{rv.root}: niveluri, rădăcină aproape unitară, fără corecția deplasării')]),
    (T('Identification (Cholesky, in this order): the euro area does not react to Romania within the month; ROBOR reacts to Romanian activity and prices within the month; the exchange rate reacts to everything', 'Identificarea (Cholesky, în această ordine): zona euro nu reacționează la România în aceeași lună; ROBOR reacționează în aceeași lună la activitatea și prețurile din România; cursul de schimb reacționează la toate'),
     [T('the zero restriction on the euro area is credible (Romania is small); the position of ROBOR before EUR/RON is debatable', 'restricția zero pentru zona euro este credibilă (România este mică); poziția ROBOR înaintea EUR/RON este discutabilă'),
      T('a block-exogenous VAR would also set the lagged Romanian effects on the euro area to zero (Seminar 3, B2 discusses orderings)', 'un VAR cu exogenitate pe blocuri ar anula și efectele decalate ale României asupra zonei euro (Seminarul 3, B2 discută ordonările)')])), 'small')

chart(T('Responses to a domestic and a euro-area rate shock', 'Răspunsuri la un șoc al dobînzii interne și la unul al zonei euro'), 'ats_ch3_ro_var', 'ATS_ch3_romania', [
    T(r'VAR(2), Cholesky with the euro-area block first; one-standard-deviation shocks (ROBOR @{rv.sdro} pp, Euribor @{rv.sdea} pp); 90\% residual-bootstrap bands', r'VAR(2), Cholesky cu blocul zonei euro pe primul loc; șocuri de o abatere standard (ROBOR @{rv.sdro} pp, Euribor @{rv.sdea} pp); benzi bootstrap de 90\%')],
    h='0.62\\textheight')

interp(('the Romanian responses', 'răspunsurilor pentru România'), [
    (T(r'ROBOR shock: IP @{rv.ro.ip12}\% after 12 months (band [@{rv.ro.ip12.lo}, @{rv.ro.ip12.hi}]); HICP @{rv.ro.p12}\% (band [@{rv.ro.p12.lo}, @{rv.ro.p12.hi}]); EUR/RON @{rv.ro.fx12}\%', r'Șocul ROBOR: IP @{rv.ro.ip12}\% după 12 luni (banda [@{rv.ro.ip12.lo}, @{rv.ro.ip12.hi}]); IAPC @{rv.ro.p12}\% (banda [@{rv.ro.p12.lo}, @{rv.ro.p12.hi}]); EUR/RON @{rv.ro.fx12}\%'),
     [T('a price puzzle and an exchange-rate puzzle (depreciation after a tightening): the ROBOR innovation still contains the BNR\'s reaction to inflation and to pressure on the leu', 'o anomalie a prețurilor și una a cursului de schimb (depreciere după o înăsprire): inovația ROBOR conține încă reacția BNR la inflație și la presiunea asupra leului')]),
    T(r'Euribor shock: Romanian IP @{rv.ea.ip12}\% after 12 months (band [@{rv.ea.ip12.lo}, @{rv.ea.ip12.hi}]); HICP @{rv.ea.p12}\%; ROBOR @{rv.ea.r12} pp', r'Șocul Euribor: IP din România @{rv.ea.ip12}\% după 12 luni (banda [@{rv.ea.ip12.lo}, @{rv.ea.ip12.hi}]); IAPC @{rv.ea.p12}\%; ROBOR @{rv.ea.r12} pp'),
    T('Honest summary: the recursive VAR identifies the euro-area block credibly and the domestic policy shock poorly', 'Rezumat onest: VAR-ul recursiv identifică credibil blocul zonei euro și slab șocul de politică internă')])

D.frame(T('How much of Romania comes from the euro area?', 'Cît din evoluția României vine din zona euro?'), table(
    'lcccc', T(r'\textbf{Variable}', r'\textbf{Variabila}') + ' & ' + T(r'\textbf{EA shocks, 12 m}', r'\textbf{șocuri ZE, 12 luni}') + ' & ' + T(r'\textbf{EA shocks, 36 m}', r'\textbf{șocuri ZE, 36 de luni}') + ' & ' + T(r'\textbf{ROBOR shock, 12 m}', r'\textbf{șoc ROBOR, 12 luni}') + ' & ' + T(r'\textbf{own shock, 12 m}', r'\textbf{șoc propriu, 12 luni}'),
    [T('IP Romania', 'IP România') + r' & @{rv.fe.ip12.ea}\% & @{rv.fe.ip36.ea}\% & @{rv.fe.ip12.r_ro}\% & @{rv.fe.ip12.own}\%',
     T('HICP Romania', 'IAPC România') + r' & @{rv.fe.p12.ea}\% & @{rv.fe.p36.ea}\% & @{rv.fe.p12.r_ro}\% & @{rv.fe.p12.own}\%',
     r'ROBOR 3M & @{rv.fe.r12.ea}\% & @{rv.fe.r36.ea}\% & @{rv.fe.r12.r_ro}\% & --',
     r'EUR/RON & @{rv.fe.fx12.ea}\% & @{rv.fe.fx36.ea}\% & @{rv.fe.fx12.r_ro}\% & @{rv.fe.fx12.own}\%'],
    size='scriptsize') + items(
    T('Forecast error variance decomposition of the recursive VAR(2); EA shocks = the three euro-area shocks together', 'Descompunerea varianței erorii de prognoză din VAR(2) recursiv; șocuri ZE = cele trei șocuri ale zonei euro împreună'),
    T(r'Euro-area shocks explain @{rv.fe.ip12.ea}\% of Romanian IP and @{rv.fe.p36.ea}\% of HICP at three years; the domestic rate shock explains less than a tenth of either', r'Șocurile zonei euro explică @{rv.fe.ip12.ea}\% din IP din România și @{rv.fe.p36.ea}\% din IAPC la trei ani; șocul dobînzii interne explică mai puțin de o zecime din fiecare'),
    T('The shares are as credible as the ordering; with a block-exogenous VAR they are a lower bound for external influence', 'Ponderile sînt la fel de credibile ca ordonarea; cu un VAR cu exogenitate pe blocuri ele sînt o limită inferioară a influenței externe')), 'small')

chart(T('ECB policy shocks and Romania: local projections', 'Șocuri de politică BCE și România: proiecții locale'), 'ats_ch3_ro_lp', 'ATS_ch3_romania', [
    T(r'Shock: the pure monetary policy shock of \refJK\ (authors\' update, one s.d. = @{rl.sd} bp); 3 lags of all variables and of the shock (lag augmentation), monthly dummies; origins 2005:8--2025:10', r'Șocul: șocul pur de politică monetară din \refJK\ (actualizarea autorilor, o abatere standard = @{rl.sd} bp); 3 decalaje ale tuturor variabilelor și ale șocului (decalaje suplimentare), variabile dummy lunare; origini 2005:8--2025:10')],
    h='0.48\\textheight')

interp(('the spillover projections', 'proiecțiilor de propagare'), [
    (T(r'Relevance first: the euro-area 1-year rate rises by @{rl.y1_ea0} pp on impact (SE @{rl.y1_ea0se}); first-stage $F = @{rl.F0}$ (impact) and @{rl.F1} (one month)', r'Întîi relevanța: dobînda la 1 an din zona euro crește cu @{rl.y1_ea0} pp la impact (SE @{rl.y1_ea0se}); statistica $F$ din prima etapă $= @{rl.F0}$ (impact) și @{rl.F1} (o lună)'),
     [T('monthly averages dilute an announcement-day surprise: the shock is a weak instrument for monthly euro-area rates', 'mediile lunare diluează o surpriză din ziua anunțului: șocul este un instrument slab pentru dobînzile lunare din zona euro')]),
    T(r'Romanian HICP: @{rl.p_ro12}\% after 12 months (SE @{rl.p_ro12se}), @{rl.p_ro24}\% after 24 (SE @{rl.p_ro24se}); EUR/RON @{rl.fx6}\% after 6 months (SE @{rl.fx6se})', r'IAPC din România: @{rl.p_ro12}\% după 12 luni (SE @{rl.p_ro12se}), @{rl.p_ro24}\% după 24 (SE @{rl.p_ro24se}); EUR/RON @{rl.fx6}\% după 6 luni (SE @{rl.fx6se})'),
    T('Honest conclusion: with a weak external shock and 20 years of data, the spillovers to Romanian prices are not determined; a weak-IV-robust set is wide (Seminar 3, C1)', 'Concluzia onestă: cu un șoc extern slab și 20 de ani de date, efectele de propagare asupra prețurilor din România nu sînt determinate; o mulțime robustă la instrumente slabe este largă (Seminarul 3, C1)')])

D.frame(T('Conclusions for Romania', 'Concluzii pentru România'), items(
    (T('Robust findings', 'Rezultate robuste'),
     [T('euro-area shocks account for a large share of Romanian output and price fluctuations', 'șocurile din zona euro explică o parte mare din fluctuațiile producției și ale prețurilor din România'),
      T('a euro-area tightening lowers Romanian IP within a year in the recursive VAR', 'o înăsprire în zona euro scade IP din România în decurs de un an în VAR-ul recursiv')]),
    (T('Fragile findings', 'Rezultate fragile'),
     [T('the effect of a domestic ROBOR shock on prices and the leu: puzzles signal an identification failure, not a fact about Romania', 'efectul unui șoc ROBOR intern asupra prețurilor și leului: anomaliile semnalează un eșec al identificării, nu un fapt despre România'),
      T('the size of ECB spillovers to Romanian inflation: the instrument is weak at a monthly frequency', 'mărimea efectelor politicii BCE asupra inflației din România: instrumentul este slab la frecvență lunară')]),
    (T('Next steps (projects)', 'Pașii următori (proiecte)'),
     [T('BNR policy-meeting surprises from ROBOR or FRA quotes around announcements, used as a proxy', 'surprize la ședințele de politică monetară ale BNR, din cotațiile ROBOR sau FRA în jurul anunțurilor, folosite ca proxy'),
      T('sign restrictions (a tightening appreciates the leu and lowers prices) and a Bayesian VAR with shrinkage (Chapter 5)', 'restricții de semn (o înăsprire apreciază leul și scade prețurile) și un VAR bayesian cu shrinkage (Capitolul 5)')])), 'small')

D.recap(('Romania and euro-area spillovers', 'efectele de propagare din zona euro asupra României'), [
    T('Put the large neighbour first: the euro-area block is credibly exogenous within the month', 'Puneți vecinul mare pe primul loc: blocul zonei euro este credibil exogen în aceeași lună'),
    T('A recursive ROBOR shock produces price and exchange-rate puzzles', 'Un șoc ROBOR recursiv produce anomalii ale prețurilor și ale cursului de schimb'),
    T('External ECB shocks are weak instruments at a monthly frequency: report the uncertainty, do not hide it', 'Șocurile externe BCE sînt instrumente slabe la frecvență lunară: raportați incertitudinea, nu o ascundeți')])

# =============================================================================
# 10. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('How strongly does ECB monetary policy pass through to Romanian inflation, and has the pass-through changed since 2022?', 'Cît de puternic se transmite politica monetară a BCE asupra inflației din România și s-a schimbat această transmisie după 2022?'),
     [T(r'formal: $H_0$: $\theta_{12} = 0$, the 12-month response of Romanian HICP to a 25 bp euro-area rate shock, tested by an Anderson--Rubin set that is valid with weak instruments', r'formal: $H_0$: $\theta_{12} = 0$, răspunsul IAPC din România după 12 luni la un șoc de 25 bp al dobînzii din zona euro, testat cu o mulțime Anderson--Rubin valabilă și pentru instrumente slabe'),
      T('falsified by a bounded 90\\% set that excludes zero for a pre-registered shock, horizon and sample', 'infirmată de o mulțime de 90\\% mărginită care exclude zero, pentru un șoc, un orizont și un eșantion preînregistrate')]),
    (T('Why it matters: Romania plans to join the euro area; the BNR needs to know how much of its inflation is imported', 'De ce contează: România pregătește aderarea la zona euro; BNR trebuie să știe cîtă inflație este importată'),
     [T(r'literature to start from: \refJK, \refSWc, \refMSW, \refPW, \refLPW', r'literatura de pornire: \refJK, \refSWc, \refMSW, \refPW, \refLPW')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers that estimate euro-area monetary spillovers to Romania or Central and Eastern Europe with high-frequency shocks; give DOIs.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează articole recenzate care estimează efectele de propagare ale politicii monetare din zona euro asupra României sau a Europei Centrale și de Est cu șocuri de frecvență înaltă; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Propose three channels (trade, exchange rate, bank funding) and one observable implication of each.}', r'\textbf{ipoteza}: \aiprompt{Propune trei canale (comerț, curs de schimb, finanțarea băncilor) și cîte o implicație observabilă pentru fiecare.}'),
      T(r'\textbf{code and replication}: ask for an LP-IV function, then reproduce a known number first (the first-stage $F$ of this lecture)', r'\textbf{cod și replicare}: cereți o funcție LP-IV, apoi reproduceți întîi o cifră cunoscută (statistica $F$ din prima etapă din acest curs)'),
      T(r'\textbf{robustness and critique}: \aiprompt{Act as a hostile referee: list every way this identification of ECB spillovers could fail.}', r'\textbf{robustețe și critică}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră toate felurile în care această identificare a efectelor BCE ar putea eșua.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The shock is dated correctly: announcement-day surprises are summed within the month, never shifted forward', 'Șocul este datat corect: surprizele din zilele anunțurilor se adună în interiorul lunii, nu se mută niciodată înainte'),
    T('Relevance is reported (first-stage $F$ with HAC variance) before any response is interpreted', 'Relevanța se raportează (statistica $F$ din prima etapă cu varianță HAC) înainte de interpretarea oricărui răspuns'),
    T('Lags, horizons, sample and the treatment of 2020 are fixed before the results; all variants are reported', 'Decalajele, orizonturile, eșantionul și tratarea anului 2020 sînt fixate înaintea rezultatelor; toate variantele sînt raportate'),
    T('An AI summary of a ``significant spillover\'\' is checked against the confidence set, not against the point estimate', 'Un rezumat AI despre un „efect de propagare semnificativ” se verifică pe mulțimea de încredere, nu pe estimația punctuală')), 'small')

chart(T('Mini-case: how robust is one number?', 'Mini studiu de caz: cît de robustă este o singură cifră?'), 'ats_ch3_ai_case', 'ATS_ch3_romania', [
    T(r'Response of Romanian HICP after 12 months to a 25 bp Euribor shock: recursive VAR and recursive LP (90\% Newey--West bars), lag length $p$, samples ending in 2019 and in 2026', r'Răspunsul IAPC din România după 12 luni la un șoc Euribor de 25 bp: VAR recursiv și LP recursivă (bare Newey--West de 90\%), numărul de decalaje $p$, eșantioane care se încheie în 2019 și în 2026'),
    T(r'@{ai.n} estimates range from @{ai.min}\% to @{ai.max}\%, @{ai.npos} of them positive: the sign depends on the lag length and on the post-2020 data; an AI assistant that reports one of them ``with confidence\'\' is wrong', r'Cele @{ai.n} de estimații variază între @{ai.min}\% și @{ai.max}\%, iar @{ai.npos} dintre ele sînt pozitive: semnul depinde de numărul de decalaje și de datele de după 2020; un asistent AI care raportează una dintre ele „cu încredere” greșește')],
    h='0.5\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Euro-area monetary spillovers to Romania}: replicate first, then extend', r'\textbf{Efectele politicii monetare din zona euro asupra României}: întîi replicare, apoi extindere'),
     [T(r'replicate: the proxy SVAR of \refGK\ (this lecture: $F = @{gk.F}$, the bond-premium jump) and the Romanian LP of this lecture', r'replicați: modelul proxy SVAR din \refGK\ (în acest curs: $F = @{gk.F}$, saltul primei de risc) și LP pentru România din acest curs'),
      T('extend: daily ECB surprises aggregated to monthly with the Gertler--Karadi averaging; a quarterly GDP version; Anderson--Rubin sets; sign restrictions on the surprises (JK)', 'extindeți: surprizele zilnice BCE agregate lunar cu metoda de mediere Gertler--Karadi; o versiune trimestrială cu PIB; mulțimi Anderson--Rubin; restricții de semn pe surprize (JK)'),
      T('pre-register: shock, outcomes, horizons 0--24, lag rule, the 2020 treatment and the Holm correction across outcomes', 'preînregistrați: șocul, variabilele de rezultat, orizonturile 0--24, regula pentru decalaje, tratarea anului 2020 și corecția Holm pentru mai multe variabile')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('A structural VAR is a reduced form plus an identifying assumption; the assumption is the economics', 'Un VAR structural este o formă redusă plus o ipoteză de identificare; ipoteza este partea economică'),
    T('Zeros (short or long run), signs, narratives, heteroskedasticity and instruments each buy identification with a different assumption', 'Zerourile (pe termen scurt sau lung), semnele, restricțiile narative, heteroscedasticitatea și instrumentele cumpără fiecare identificarea cu o altă ipoteză'),
    T('Set identification is honest: report the set and the role of the prior', 'Identificarea pe mulțimi este onestă: raportați mulțimea și rolul distribuției a priori'),
    T('Inference: bootstrap matched to the setting, bias correction, joint bands, weak-IV-robust sets', 'Inferența: bootstrap potrivit cazului, corecția deplasării, benzi simultane, mulțimi robuste la instrumente slabe'),
    T('LP and VAR estimate the same responses; choose by bias and variance, and use LP for state dependence', 'LP și VAR estimează aceleași răspunsuri; alegeți după deplasare și varianță și folosiți LP pentru dependența de stare')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('How many restrictions identify a five-variable SVAR exactly?', 'Cîte restricții identifică exact un SVAR cu cinci variabile?'),
        T(r'Why does $\E u_tz_t$ identify the impact column of a proxy SVAR?', r'De ce identifică $\E u_tz_t$ coloana de impact a unui proxy SVAR?'),
        T('What does the posterior median of a sign-restricted response fail to represent?', 'Ce nu reprezintă mediana a posteriori a unui răspuns identificat prin semne?'),
        T('When does a VAR beat LP in mean squared error?', 'Cînd bate un VAR proiecțiile locale în eroarea medie pătratică?'),
        T('Why is the wild bootstrap invalid for a proxy SVAR?', 'De ce nu este valid bootstrap-ul wild pentru un proxy SVAR?'))),
    block(T('Next: Chapter 4', 'Urmează: Capitolul 4'), items(
        T('Cointegration revisited: VECM, ARDL and panel data', 'Cointegrare: VECM, ARDL și date panel'),
        T('Long-run restrictions become restrictions on cointegrating vectors and on the common trends', 'Restricțiile de termen lung devin restricții asupra vectorilor de cointegrare și asupra trendurilor comune'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the long-run restriction in closed form', 'Anexă: restricția de termen lung în formă închisă'), items(
    T(r'Stable VAR: $\sum_{h\ge0}\Phi_h = A(1)^{-1}$, so the long-run response matrix is $\Theta(1) = A(1)^{-1}B_0$', r'VAR stabil: $\sum_{h\ge0}\Phi_h = A(1)^{-1}$, deci matricea răspunsurilor de termen lung este $\Theta(1) = A(1)^{-1}B_0$'),
    T(r'$\Theta(1)\Theta(1)\' = A(1)^{-1}B_0B_0\'A(1)^{-1\prime} = A(1)^{-1}\Sigma_uA(1)^{-1\prime}$, known from the reduced form', r'$\Theta(1)\Theta(1)\' = A(1)^{-1}B_0B_0\'A(1)^{-1\prime} = A(1)^{-1}\Sigma_uA(1)^{-1\prime}$, cunoscută din forma redusă'),
    T(r'$[\Theta(1)]_{12} = 0$ makes $\Theta(1)$ lower triangular: $\Theta(1) = \mathrm{chol}(A(1)^{-1}\Sigma_uA(1)^{-1\prime})$, unique with a positive diagonal', r'$[\Theta(1)]_{12} = 0$ face $\Theta(1)$ inferior triunghiulară: $\Theta(1) = \mathrm{chol}(A(1)^{-1}\Sigma_uA(1)^{-1\prime})$, unică pentru o diagonală pozitivă'),
    T(r'Hence $B_0 = A(1)\Theta(1)$; check $B_0B_0\' = \Sigma_u$; signs are then normalised (supply raises output in the long run)', r'Deci $B_0 = A(1)\Theta(1)$; verificăm $B_0B_0\' = \Sigma_u$; semnele se normalizează apoi (oferta crește producția pe termen lung)')), 'small')

D.frame(T('Appendix: how the proxy identifies $b_1$', 'Anexă: identificarea coloanei $b_1$ prin proxy'), items(
    T(r'$u_t = B_0\varepsilon_t = b_1\varepsilon_{1t} + \sum_{j\ge2}b_j\varepsilon_{jt}$', r'$u_t = B_0\varepsilon_t = b_1\varepsilon_{1t} + \sum_{j\ge2}b_j\varepsilon_{jt}$'),
    T(r'$\E u_tz_t = b_1\E\varepsilon_{1t}z_t + \sum_{j\ge2}b_j\E\varepsilon_{jt}z_t = \alpha b_1$ by exogeneity', r'$\E u_tz_t = b_1\E\varepsilon_{1t}z_t + \sum_{j\ge2}b_j\E\varepsilon_{jt}z_t = \alpha b_1$ din exogenitate'),
    T(r'Relative impacts $b_{i1}/b_{11} = \E u_{it}z_t/\E u_{1t}z_t$ need $\alpha \ne 0$ (relevance); the scale of $b_1$ follows from $b_1\'\Sigma_u^{-1}b_1 = 1$', r'Impacturile relative $b_{i1}/b_{11} = \E u_{it}z_t/\E u_{1t}z_t$ cer $\alpha \ne 0$ (relevanța); scala lui $b_1$ rezultă din $b_1\'\Sigma_u^{-1}b_1 = 1$'),
    T(r'Equivalent 2SLS: regress $u_{it}$ on $u_{1t}$ with instrument $z_t$; the first stage is the regression of $u_{1t}$ on $z_t$', r'2SLS echivalent: regresăm $u_{it}$ pe $u_{1t}$ cu instrumentul $z_t$; prima etapă este regresia lui $u_{1t}$ pe $z_t$')), 'small')

D.frame(T('Appendix: LP and VAR agree up to horizon $p$', 'Anexă: LP și VAR coincid pînă la orizontul $p$'), items(
    T(r'Let $w_t = (y_{t-1}, \dots, y_{t-p})$ and the shock be the innovation $\tilde x_t = x_t - \mathrm{proj}(x_t\mid w_t)$', r'Fie $w_t = (y_{t-1}, \dots, y_{t-p})$, iar șocul inovația $\tilde x_t = x_t - \mathrm{proj}(x_t\mid w_t)$'),
    T(r'LP coefficient: $\beta_h = \Cov(y_{t+h}, \tilde x_t)/\Var(\tilde x_t)$ (Frisch--Waugh)', r'Coeficientul LP: $\beta_h = \Cov(y_{t+h}, \tilde x_t)/\Var(\tilde x_t)$ (Frisch--Waugh)'),
    T(r'The VAR($p$) reproduces the autocovariances $\Gamma_0, \dots, \Gamma_p$ exactly; for $h \le p$, $\Cov(y_{t+h}, \tilde x_t)$ depends only on them, so both give the same $\beta_h$ \refPW', r'VAR($p$) reproduce exact autocovarianțele $\Gamma_0, \dots, \Gamma_p$; pentru $h \le p$, $\Cov(y_{t+h}, \tilde x_t)$ depinde doar de ele, deci ambele dau același $\beta_h$ \refPW'),
    T(r'For $h > p$ the VAR extrapolates its own autocovariances: the source of the bias of a short VAR, and of the lower variance', r'Pentru $h > p$, VAR-ul își extrapolează propriile autocovarianțe: sursa deplasării unui VAR scurt și a varianței mai mici')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
