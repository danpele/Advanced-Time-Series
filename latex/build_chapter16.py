r"""
build_chapter16.py -- Capitolul 16 (Rădăcini explozive și bule speculative; studiu individual), EN + RO
======================================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_16/ch16_numbers.json (generate_all_charts.py). Nicio cifră nu este
scrisă de mînă, în afara exemplelor teoretice (parametrii simulărilor, calcule de verificat pe hîrtie).
TSA, Capitolul 13 (studiu individual) a prezentat bulele în istorie, SADF/GSADF/BSADF pe scurt, modelul LPPL cu
estimarea Filimonov--Sornette și o evaluare onestă a prognozei crahurilor; MFM, Capitolul 17 aplică testele pe
piețe. Aici: teoria bulelor raționale (Blanchard--Watson, Diba--Grossman, Evans), asimptotica proceselor explozive
(White, Anderson, Phillips--Magdalinos), teoria și nivelul testelor PSY (wild bootstrap, testare multiplă pe date),
acuratețea datării și evaluarea alarmelor timpurii, fundamentele față de prețuri (chirii), extensii (HLST,
monitorizare în timp real, LPPLS cu verosimilitate profil), aplicații cu frecvențe de bază ale alarmelor false.
Ieșire:
  EN/Courses/chapter16_explosive_roots_bubbles.tex
  RO/Cursuri/capitol16_radacini_explozive_bule_speculative.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_16/generate_all_charts.py
  python3 latex/build_chapter16.py && python3 latex/ats_build.py compile 16
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch16_common import REFS, QLURL, T, V2, day, month, bib, finalize, load, minus_fix   # noqa: E402


def _merge(x):
    """(text, [display, ...]): a displayed formula placed first among the sub-items is written inside the item itself."""
    if isinstance(x, tuple) and x[1] and x[1][0].lstrip('⟦').startswith('\\['):
        x = (x[0] + ' ' + x[1][0].replace("\\'", "'"), x[1][1:])
    return x[0] if isinstance(x, tuple) and not x[1] else x


def items(*xs):
    return _items(*[_merge(x) for x in xs])


N = load()
V = Values()
D = Deck(16, 'lecture', refs=REFS)
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
PH = {
    'blanchard': ('ch16_blanchard_2008.jpg', C + 'Oliver_Blanchard_(cropped).jpg',
                  FOTO + ': Eugene Salazar, IMF (2008); public domain; Wikimedia Commons'),
    'nasdaq': ('ch16_nasdaq_marketsite_2021.jpg', C + 'Nasdaq_MarketSite_(51494550508).jpg',
               FOTO + ': ajay\\_suresh (2021); CC BY 2.0; Wikimedia Commons'),
    'foreclosure': ('ch16_foreclosure_2008.jpg', C + 'Foreclosedhome.JPG',
                    FOTO + ': Brendel (2008); CC BY-SA 3.0; Wikimedia Commons'),
    'sornette': ('ch16_sornette_2012.jpg', C + 'Didier_Sornette.jpg',
                 FOTO + ': Didier Sornette (2012); CC BY-SA 3.0 de; Wikimedia Commons'),
    'shanghai': ('ch16_shanghai_se_2008.jpg', C + 'Shanghai_Stock_Exchange_Building.jpg',
                 FOTO + ': Baycrest (2008); CC BY-SA 2.5; Wikimedia Commons'),
    'bvb': ('ch16_bvb_palace_1928.jpg', C + 'Nicolae_Ionescu_-_The_Stock_Exchange_Palace_in_March_1928.jpg',
            FOTO + ': Nicolae Ionescu (1928); public domain; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.36', wr='0.62'):
    return cols(left, right, wl, wr)


def pv(key, x, d=3):
    if x < 10 ** (-d):
        V.raw(key, '$<$ ' + n(10 ** (-d), d))
    else:
        V.raw(key, '= ' + n(x, d))


def pct(key, x, d=0):
    P(key, 100 * x, d)


def dd(key, s):
    V.raw(key, day(s) if s else T('none', 'niciuna'))


def mm(key, s):
    V.raw(key, month(s) if s else T('none', 'niciuna'))


# =============================================================================
# CIFRE
# =============================================================================
ra = N['rational']
V.raw('ra.T', str(ra['T']))
P('ra.adf', ra['adf'], 2)
P('ra.sadf', ra['sadf'], 2)
P('ra.gsadf', ra['gsadf'], 2)
P('ra.cvadf', ra['cv']['adf']['95'], 2)
P('ra.cvsadf', ra['cv']['sadf']['95'], 2)
P('ra.cvgsadf', ra['cv']['gsadf']['95'], 2)
V.raw('ra.nep', str(ra['n_ep']))
V.raw('ra.coll', str(ra['collapses']))
V.raw('ra.L', str(ra['L']))
V.int('ra.R', ra['R'])
P('ra.dur', ra['bw_dur'], 0)
asy = N['asymptotics']
V.int('as.R', asy['R'])
P('as.rho', asy['mild_normal']['rho'], 4)
P('as.k', asy['k'], 1)
for kk in ('mild_normal', 'mild_exp', 'fixed_normal', 'fixed_exp', 'mild_big_normal', 'mild_big_exp'):
    key = kk.replace('_', '')
    P(f'as.{key}.ks', asy[kk]['ks'], 3)
    pv(f'as.{key}.p', asy[kk]['ks_p'])
    pct(f'as.{key}.cov', asy[kk]['cover'], 1)
P('as.rhobig', asy['mild_big_normal']['rho'], 4)
nu = N['null']
for T_ in ('100', '200', '400', '800'):
    for k in ('adf', 'sadf', 'gsadf'):
        P(f'nu.{T_}.{k}', nu[T_][k]['95'], 2)
    P(f'nu.{T_}.bs', nu[T_]['bsadf_end'], 2)
    V.raw(f'nu.{T_}.w0', str(nu[T_]['w0']))
    V.int(f'nu.{T_}.win', nu[T_]['windows'])
sz = N['size']
V.raw('sz.T', str(sz['T']))
V.raw('sz.N', str(sz['N']))
V.raw('sz.B', str(sz['B']))
V.raw('sz.L', str(sz['L']))
for k in ('iid', 'up', 'down', 'garch'):
    for m in ('rej_mc', 'rej_wild', 'ep_mc', 'ep_wild', 'ep_fw'):
        pct(f'sz.{k}.{m.replace("_", "")}', sz['rates'][k][m], 1)
dt = N['dating']
V.raw('dt.T', str(dt['T']))
V.int('dt.N', dt['N'])
V.raw('dt.te', str(dt['te']))
V.raw('dt.tf', str(dt['tf']))
V.raw('dt.dur', str(dt['dur']))
V.raw('dt.L', str(dt['L']))
for r, kk in (('1.005', 'a'), ('1.01', 'b'), ('1.02', 'c')):
    pct(f'dt.{kk}.det', dt[r]['det'], 1)
    P(f'dt.{kk}.med', dt[r]['med_start'], 0)
    P(f'dt.{kk}.q25', dt[r]['q25'], 0)
    P(f'dt.{kk}.q75', dt[r]['q75'], 0)
    P(f'dt.{kk}.conf', dt[r]['med_conf'], 0)
    pct(f'dt.{kk}.fb', dt[r]['false_before'], 0)
    P(f'dt.{kk}.g', dt[r]['growth'], 2)
mo = N['monitor']
P('mo.a', mo['a'], 2)
P('mo.a2', mo['a'] ** 2, 2)
pct('mo.size', mo['size']['iid'], 1)
pct('mo.sizeg', mo['size']['garch'], 1)
V.int('mo.Ns', mo['Nsize'])
for k in ('ndx', 'btc'):
    dd(f'mo.{k}.cus', mo[k]['cusum_alarm'])
    dd(f'mo.{k}.bs', mo[k]['bsadf_conf'])
    dd(f'mo.{k}.peak', mo[k]['peak'])
    V.raw(f'mo.{k}.n', str(mo[k]['n']))
ho = N['housing']
for k in ('us_ratio', 'us_rent', 'us_price', 'ro_ratio', 'ro_rent', 'ro_price'):
    kk = k.replace('_', '')
    P(f'ho.{kk}.g', ho[k]['gsadf'], 2)
    P(f'ho.{kk}.cv', ho[k]['cv'], 2)
    V.raw(f'ho.{kk}.k', str(ho[k]['k']))
    V.raw(f'ho.{kk}.T', str(ho[k]['T']))
    V.raw(f'ho.{kk}.nep', str(len(ho[k]['episodes'])))
e0 = ho['us_ratio']['episodes'][0]
mm('ho.e1a', e0[0])
mm('ho.e1b', e0[1])
V.raw('ho.usep', ', '.join(V2(f'{month(a)}--{month(b)}', f'{month(a)}--{month(b)}') for a, b, _ in ho['us_ratio']['episodes']))
V.raw('ho.rentep', '; '.join(f'{month(a)}--{month(b)}' for a, b, _ in ho['us_rent']['episodes']))
V.raw('ho.priceep', '; '.join(f'{month(a)}--{month(b)}' for a, b, _ in ho['us_price']['episodes']))
mm('ho.uslast', ho['us_ratio']['last'])
_rl = pd.Timestamp(ho['ro_ratio']['last']) + pd.offsets.MonthBegin(2)
mm('ho.rolast', _rl.strftime('%Y-%m-%d'))
V.int('ho.B', ho['B'])
ep = N['episodes']
LAB = {'sp500': r'S\&P 500', 'ndx': 'Nasdaq 100', 'ssec': 'Shanghai', 'btc': 'Bitcoin', 'bet': 'BET'}
for k in ('sp500', 'ndx', 'ssec', 'btc', 'bet'):
    e = ep[k]
    P(f'ep.{k}.g', e['gsadf'], 2)
    P(f'ep.{k}.mc', e['cv_mc'], 2)
    P(f'ep.{k}.w', e['cv_wild'], 2)
    V.raw(f'ep.{k}.T', str(e['T']))
    V.raw(f'ep.{k}.nmc', str(e['n_mc']))
    V.raw(f'ep.{k}.nw', str(e['n_wild']))
    V.raw(f'ep.{k}.nfw', str(e['n_fw']))
    V.raw(f'ep.{k}.wkmc', str(e['weeks_mc']))
    V.raw(f'ep.{k}.wkw', str(e['weeks_wild']))
    for j, pk in enumerate(e['peaks']):
        dd(f'ep.{k}.{j}.peak', pk['peak'])
        dd(f'ep.{k}.{j}.conf', pk['conf'])
        V.raw(f'ep.{k}.{j}.lead', str(pk['lead']) if pk['lead'] is not None else '--')
        V.raw(f'ep.{k}.{j}.flead', str(pk['fw_lead']) if pk['fw_lead'] is not None else '--')
        V.raw(f'ep.{k}.{j}.act', T('yes', 'da') if pk['active'] else T('no', 'nu'))
        V.raw(f'ep.{k}.{j}.fact', T('yes', 'da') if pk['fw_active'] else T('no', 'nu'))
        pct(f'ep.{k}.{j}.fall', -pk['fall'], 0)
V.raw('ep.R', str(ep['R']))
V.raw('ep.B', str(ep['B']))
lp = N['lppls']
for k in ('low', 'peak', 't2', 'tc', 'tc_prof', 'lo', 'hi', 'ci_max_date', 'first_ci'):
    dd(f'lp.{k}', lp[k])
V.raw('lp.n', str(lp['n']))
P('lp.m', lp['m'], 2)
P('lp.w', lp['w'], 2)
P('lp.osc', lp['osc'], 1)
P('lp.damp', lp['damping'], 2)
P('lp.width', lp['width'], 0)
P('lp.cimax', lp['ci_max'], 2)
V.raw('lp.win', str(lp['windows']))
ev = N['evaluation']
for k in ('sp500', 'btc'):
    e = ev[k]
    for sc in ('ci', 'bsadf', 'mom'):
        P(f'ev.{k}.{sc}', e[sc]['auc'], 2)
        P(f'ev.{k}.{sc}.lo', e[sc]['lo'], 2)
        P(f'ev.{k}.{sc}.hi', e[sc]['hi'], 2)
    pct(f'ev.{k}.base', e['base'], 1)
    V.int(f'ev.{k}.n', e['n'])
    pct(f'ev.{k}.cipos', e['share_ci_pos'], 1)
    for al in ('ci_any', 'bsadf_alarm', 'mom_q90'):
        a = e[al]
        pct(f'ev.{k}.{al}.hit', a['hit'], 0)
        pct(f'ev.{k}.{al}.fa', a['false_alarm'], 0)
        pct(f'ev.{k}.{al}.prec', a['precision'] if a['precision'] == a['precision'] else 0, 0)
V.raw('ev.B', str(ev['B']))
ai = N['ai_case']
V.raw('ai.K', str(ai['K']))
V.raw('ai.B', str(ai['B']))
V.raw('ai.mc', str(ai['rej_mc']))
V.raw('ai.wild', str(ai['rej_wild']))
V.raw('ai.holm', str(ai['holm']))
V.raw('ai.bh', str(ai['bh']))
P('ai.exp', ai['expected'], 1)
P('ai.minp', ai['min_p'], 4)
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T('The question of the chapter and the route', 'Întrebarea capitolului și traseul'), items(
    (T(r'\textbf{Question}: when does a price series contain an explosive component, how precisely can we date it, and how much is an alarm worth once false alarms and base rates are counted?',
       r'\textbf{Întrebarea}: cînd conține o serie de prețuri o componentă explozivă, cît de precis o putem data și cît valorează o alarmă după ce numărăm alarmele false și frecvențele de bază?'),
     [T('three layers: economic theory of rational bubbles, asymptotic theory of explosive autoregressions, statistical evaluation of detectors',
        'trei niveluri: teoria economică a bulelor raționale, teoria asimptotică a proceselor autoregresive explozive, evaluarea statistică a detectorilor')]),
    (T(r'\textbf{Route}', r'\textbf{Traseul}'),
     [T('rational bubbles: present value, Blanchard--Watson, the Diba--Grossman critique, Evans bubbles',
        'bulele raționale: valoarea actualizată, Blanchard--Watson, critica Diba--Grossman, bulele Evans'),
      T('explosive autoregressions: Cauchy limits, mildly explosive roots; SADF, GSADF, BSADF and their size',
        'procese autoregresive explozive: limite Cauchy, rădăcini ușor explozive; SADF, GSADF, BSADF și nivelul lor'),
      T('date-stamping, real-time monitoring, evaluation of early warnings; fundamentals against prices (rents)',
        'datarea episoadelor, monitorizarea în timp real, evaluarea alarmelor timpurii; fundamentele față de prețuri (chirii)'),
      T('LPPLS as a competing detector; applications: dot-com, Shanghai 2015, Bitcoin, BET 2007, housing',
        'LPPLS ca detector alternativ; aplicații: dot-com, Shanghai 2015, Bitcoin, BET 2007, piața locuințelor')]),
    (T('Prerequisites and continuation', 'Cunoștințe necesare și continuare'),
     [T(r'TSA, Chapter 13 (slide \hyperlink{c16known}{\textcolor{MainBlue}{Known from TSA and new here}}); Chapter 2: unit roots, structural breaks', r'TSA, Capitolul 13 (slide-ul \hyperlink{c16known}{\textcolor{MainBlue}{Cunoscut din TSA și elemente noi}}); Capitolul 2: rădăcini unitare, rupturi structurale'),
      T('MFM, Chapter 17 applies the tests to markets', 'MFM, Capitolul 17 aplică testele pe piețe')])), 'small')

D.frame(T('Self-study guide', 'Ghid de studiu individual'), items(
    (T(r'This chapter is for \textbf{self-study}: there is no seminar; every section ends with a recap', r'Acest capitol este pentru \textbf{studiu individual}: nu are seminar; fiecare secțiune se încheie cu o recapitulare'),
     [T('redo each worked derivation on paper before reading the next slide', 'refaceți pe hîrtie fiecare derivare rezolvată înainte de a citi slide-ul următor'),
      T('after each chart, write your own reading of it, then compare it with the interpretation slide', 'după fiecare grafic, scrieți propria lectură a lui, apoi comparați-o cu slide-ul de interpretare')]),
    (T('Run the lecture notebook: it reproduces every chart and number with smaller Monte Carlo sizes', 'Rulați notebook-ul cursului: reproduce fiecare grafic și fiecare cifră, cu simulări Monte Carlo mai mici'),
     [T('change one design choice (the minimum window, the lag order, the critical value, the crash threshold) and record how the conclusion changes', 'modificați o alegere (fereastra minimă, numărul de laguri, valoarea critică, pragul de crah) și notați cum se schimbă concluzia')]),
    T('The self-assessment at the end has answers; the quiz of this chapter on the course site is graded', 'Autoevaluarea de la final are răspunsuri; quiz-ul capitolului de pe site-ul cursului se notează'),
    T('Prerequisites: Dickey--Fuller asymptotics (Hamilton, Chapter 17), the functional central limit theorem, bootstrap for dependent data (Chapter 0)',
      'Cunoștințe necesare: asimptotica Dickey--Fuller (Hamilton, capitolul 17), teorema limită centrală funcțională, bootstrap pentru date dependente (Capitolul 0)')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Derive the general solution of the present-value model and state the restrictions of Diba and Grossman on rational bubbles',
      'Derivați soluția generală a modelului valorii actualizate și enunțați restricțiile lui Diba și Grossman asupra bulelor raționale'),
    T('Derive the Cauchy limit of the OLS estimator under an explosive root and explain why the mildly explosive limit is invariant to the error law',
      'Derivați limita Cauchy a estimatorului OLS sub o rădăcină explozivă și explicați de ce limita în cazul ușor exploziv nu depinde de legea erorilor'),
    T('Compute SADF, GSADF and BSADF with Monte Carlo and wild-bootstrap critical values, and control false alarms across dates',
      'Calculați SADF, GSADF și BSADF cu valori critice Monte Carlo și wild bootstrap și controlați alarmele false de-a lungul datelor'),
    T('Measure date-stamping delays and evaluate early-warning signals with hit rates, false-alarm rates, precision and ROC curves',
      'Măsurați întîrzierile datării și evaluați semnalele de avertizare timpurie prin rata de detecție, rata alarmelor false, precizie și curbe ROC'),
    T('Separate explosive prices from explosive fundamentals, and compare PSY with LPPLS confidence indicators on real episodes',
      'Separați prețurile explozive de fundamentele explozive și comparați PSY cu indicatorii de încredere LPPLS pe episoade reale')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Theory: \refBW; \refDGa; \refEv; \refPM; \refPSYa; \refPSYb', r'Teorie: \refBW; \refDGa; \refEv; \refPM; \refPSYa; \refPSYb'),
     [T(r'Inference and monitoring: \refPS; \refHLST; \refHB; \refAHLST; survey: \refGur', r'Inferență și monitorizare: \refPS; \refHLST; \refHB; \refAHLST; sinteză: \refGur'),
      T(r'LPPLS: \refJLS; \refFS; \refFDS; \refSZ; critique: \refFei; \refGF', r'LPPLS: \refJLS; \refFS; \refFDS; \refSZ; critică: \refFei; \refGF')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_16}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_16}'),
     [T(r'every window regression written out in \texttt{numpy} (cumulated cross-products); the R package \texttt{exuber} \refVPM implements the same statistics',
        r'fiecare regresie pe fereastră scrisă în \texttt{numpy} (produse încrucișate cumulate); pachetul R \texttt{exuber} \refVPM implementează aceleași statistici')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter16_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter16_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{4.2cm}' + TB + 'p{5.0cm}' + TB + 'p{2.9cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Sample}', r'\textbf{Eșantionul}'),
    [T(r'S\&P 500, Nasdaq 100, Shanghai Composite, BET, Bitcoin', r'S\&P 500, Nasdaq 100, Shanghai Composite, BET, Bitcoin') + ' & ' + T('EODHD daily closes (weekly: Friday close)', 'închideri zilnice EODHD (săptămînal: închiderea de vineri)') + ' & 1990 -- 2026',
     T('US house prices, rents, consumer prices', 'Prețurile locuințelor, chiriile și prețurile de consum în SUA') + ' & ' + T('FRED: S\\&P CoreLogic Case--Shiller national index, CPI rent of primary residence, CPI (seasonally adjusted)', 'FRED: indicele național S\\&P CoreLogic Case--Shiller, componenta chirie din CPI, CPI (ajustate sezonier)') + ' & 1987 -- @{ho.uslast}',
     T('Romanian house prices, rents, consumer prices', 'Prețurile locuințelor, chiriile și prețurile de consum în România') + ' & ' + T('Eurostat: house price index; HICP actual rentals and all items', 'Eurostat: indicele prețurilor locuințelor; HICP chirii efective și total') + ' & 2009 -- @{ho.rolast}',
     T('All price series of the course data', 'Toate seriile de prețuri din datele cursului') + ' & ' + T('EODHD, monthly closes (screen of the AI mini-case)', 'EODHD, închideri lunare (analiza din mini studiul de caz AI)') + ' & 1990 -- 2026'],
    size='scriptsize') + items(
    T('Tests run on log prices or log ratios; weekly data for stock indices and Bitcoin, monthly or quarterly data for housing',
      'Testele se aplică logaritmilor prețurilor sau ai rapoartelor; date săptămînale pentru indici și Bitcoin, lunare sau trimestriale pentru locuințe')), 'footnotesize')

D.frame(T('Known from TSA and new here', 'Cunoscut din TSA și elemente noi'), two(
    ph('nasdaq', T('Nasdaq MarketSite, Times Square, 2021', 'Nasdaq MarketSite, Times Square, 2021'), h='0.4\\textheight'),
    items((T(r'\hypertarget{c16known}{}Known (TSA, Chapter 13)', r'\hypertarget{c16known}{}Cunoscut (TSA, Capitolul 13)'),
           [T('manias in history; the right-tailed ADF, SADF, GSADF and BSADF with Monte Carlo critical values', 'maniile din istorie; ADF pe coada din dreapta, SADF, GSADF și BSADF cu valori critice Monte Carlo'),
            T('the LPPL equation, the two-step calibration, the confidence indicator', 'ecuația LPPL, calibrarea în doi pași, indicatorul de încredere')]),
          (T('New: the research layer', 'Nou: nivelul de cercetare'),
           [T('why rational bubbles must explode and why they are hard to see', 'de ce bulele raționale trebuie să explodeze și de ce sînt greu de văzut'),
            T('the limit theory behind the tests, their size under changing volatility and across many dates', 'teoria asimptotică din spatele testelor, nivelul lor sub volatilitate variabilă și pe multe date'),
            T('how early, how often and how wrongly the detectors raise alarms', 'cît de devreme, cît de des și cît de greșit dau alarma detectorii')]),
          (T('Case studies, on our data', 'Studii de caz, pe datele noastre'),
           [T(r'\refPWY; \refPSYa; \refPY', r'\refPWY; \refPSYa; \refPY'),
            T(r'\refHB; \refHLST; \refSha', r'\refHB; \refHLST; \refSha')]))), 'footnotesize')

# =============================================================================
# 1. BULE RAȚIONALE
# =============================================================================
D.section('Rational bubbles', 'Bule raționale')

D.frame(T('The present-value model and its bubble solutions (1/2)', 'Modelul valorii actualizate și soluțiile cu bulă (1/2)'), items(
    (T(r'\textbf{No-arbitrage} with a constant required return $r > 0$: today\'s price is the discounted expected value of tomorrow\'s price plus dividend',
       r'\textbf{Lipsa arbitrajului} cu un randament cerut constant $r > 0$: prețul de azi este valoarea actualizată a prețului de mîine plus dividendul așteptat'),
     [r'\[ P_t = (1 + r)^{-1}\E_t[P_{t+1} + D_{t+1}] \]',
      T(r'$P_t$: price; $D_t$: dividend (or rent); $\E_t$: expectation given the information available at $t$', r'$P_t$: prețul; $D_t$: dividendul (sau chiria); $\E_t$: speranța condiționată de informația disponibilă la $t$')]),
    (T(r'\textbf{Forward substitution} $k$ times: the price is the discounted dividends of the next $k$ periods plus the discounted price at $t + k$',
       r'\textbf{Substituția înainte} de $k$ ori: prețul este suma dividendelor actualizate din următoarele $k$ perioade plus prețul actualizat de la $t + k$'),
     [r'\[ P_t = \sum_{i=1}^{k}(1 + r)^{-i}\E_t D_{t+i} + (1 + r)^{-k}\E_t P_{t+k} \]']),
    (T(r'If the \textbf{transversality condition} $\lim_{k\to\infty} (1 + r)^{-k}\E_t P_{t+k} = 0$ holds, the price equals the \textbf{fundamental value}',
       r'Dacă \textbf{condiția de transversalitate} $\lim_{k\to\infty} (1 + r)^{-k}\E_t P_{t+k} = 0$ este îndeplinită, prețul este egal cu \textbf{valoarea fundamentală}'),
     [r'\[ P_t = F_t := \sum_{i \ge 1}(1 + r)^{-i}\E_t D_{t+i} \]'])), 'small')

D.frame(T('The present-value model and its bubble solutions (2/2)', 'Modelul valorii actualizate și soluțiile cu bulă (2/2)'), items(
    (T(r'\textbf{General solution}: the fundamental plus a \textbf{bubble} $B_t$ whose expected value grows at the rate $r$',
       r'\textbf{Soluția generală}: fundamentul plus o \textbf{bulă} $B_t$, a cărei valoare așteptată crește cu rata $r$'),
     [r'\[ P_t = F_t + B_t, \qquad \E_t B_{t+1} = (1 + r)B_t, \qquad \E_t B_{t+k} = (1 + r)^k B_t \]',
      T(r'$B_t$ is a submartingale with an explosive mean: it satisfies the no-arbitrage equation but violates transversality', r'$B_t$ este o submartingală cu medie explozivă: satisface ecuația de lipsă a arbitrajului, dar încalcă transversalitatea')]),
    (T(r'\textbf{Econometric content}: $B_t$ follows $(1 - (1 + r)L)B_t = z_t$, an AR(1) with coefficient $1 + r > 1$',
       r'\textbf{Conținutul econometric}: $B_t$ urmează $(1 - (1 + r)L)B_t = z_t$, un AR(1) cu coeficientul $1 + r > 1$'),
     [T(r'$L$: the lag operator ($LB_t = B_{t-1}$); $z_t$: a martingale difference ($\E_{t-1}z_t = 0$); an \textbf{explosive autoregressive root}', r'$L$: operatorul lag ($LB_t = B_{t-1}$); $z_t$: o diferență de martingală ($\E_{t-1}z_t = 0$); o \textbf{rădăcină autoregresivă explozivă}')]),
    (T(r'General equilibrium limits \refTir; \refSW', r'Limitele de echilibru general \refTir; \refSW'),
     [T('with infinitely lived agents bubbles are ruled out in most economies', 'cu agenți cu viață infinită, bulele sînt excluse în majoritatea economiilor'),
      T(r'with overlapping generations they can exist if growth exceeds $r$', r'cu generații suprapuse pot exista dacă creșterea depășește $r$')])), 'small')

D.frame(T('Worked example: the fundamental value with random-walk dividends', 'Exemplu rezolvat: valoarea fundamentală cu dividende de tip mers aleator'), items(
    (T(r'Let dividends be a random walk with drift, $D_t = \mu + D_{t-1} + \varepsilon_t$: then $\E_t D_{t+i} = D_t + i\mu$', r'Fie dividendele un mers aleator cu derivă, $D_t = \mu + D_{t-1} + \varepsilon_t$: atunci $\E_t D_{t+i} = D_t + i\mu$'),
     [T(r'$\mu$: the expected change per period (drift); $\varepsilon_t$: a zero-mean shock', r'$\mu$: variația așteptată pe perioadă (deriva); $\varepsilon_t$: un șoc cu media zero')]),
    (T(r'Summing the discounted expected dividends', r'Însumînd dividendele așteptate actualizate'),
     [r'\[ F_t = D_t\sum_{i \ge 1}(1 + r)^{-i} + \mu\sum_{i \ge 1} i(1 + r)^{-i} = \dfrac{D_t}{r} + \dfrac{\mu(1 + r)}{r^2} \]',
      T(r'using $\sum_{i \ge 1} x^i = x/(1 - x)$ and $\sum_{i \ge 1} i x^i = x/(1 - x)^2$ with $x = (1 + r)^{-1}$',
        r'folosind $\sum_{i \ge 1} x^i = x/(1 - x)$ și $\sum_{i \ge 1} i x^i = x/(1 - x)^2$ cu $x = (1 + r)^{-1}$')]),
    (T(r'Implications: $F_t$ is I(1) like $D_t$; $P_t - D_t/r$ is stationary without a bubble: price and dividend are \textbf{cointegrated} with vector $(1, -1/r)$ \refCS',
       r'Implicații: $F_t$ este I(1), ca și $D_t$; $P_t - D_t/r$ este staționar în absența bulei: prețul și dividendul sînt \textbf{cointegrate} cu vectorul $(1, -1/r)$ \refCS'),
     [T(r'with a bubble, $P_t - D_t/r - \mu(1 + r)/r^2 = B_t$ inherits the explosive root: no difference $\Delta^d P_t$ is stationary \refDGb',
        r'cu bulă, $P_t - D_t/r - \mu(1 + r)/r^2 = B_t$ moștenește rădăcina explozivă: nicio diferență $\Delta^d P_t$ nu este staționară \refDGb')]),
    T(r'Check on paper: $r = 0.05$, $\mu = 0.04$, $D_t = 2$ give $F_t = 40 + 16.8 = 56.8$; the price-dividend ratio $28.4$ is constant only if $\mu = 0$',
      r'Verificați pe hîrtie: $r = 0.05$, $\mu = 0.04$, $D_t = 2$ dau $F_t = 40 + 16.8 = 56.8$; raportul preț/dividend $28.4$ este constant doar dacă $\mu = 0$')), 'small')

D.frame(T('Blanchard--Watson: a bubble that can burst', 'Blanchard--Watson: o bulă care se poate sparge'), two(
    ph('blanchard', T('Olivier Blanchard, IMF, 2008', 'Olivier Blanchard, FMI, 2008'), h='0.42\\textheight'),
    items((T(r'\refBW: each period the bubble survives with probability $\pi$ and bursts with probability $1 - \pi$', r'\refBW: în fiecare perioadă bula supraviețuiește cu probabilitatea $\pi$ și se sparge cu probabilitatea $1 - \pi$'),
           [r'\[ B_{t+1} = \begin{cases} \dfrac{1 + r}{\pi}B_t + \varepsilon_{t+1} & \text{' + T('with probability', 'cu probabilitatea') + r'}\ \pi \\[2mm] \varepsilon_{t+1} & \text{' + T('with probability', 'cu probabilitatea') + r'}\ 1 - \pi \end{cases} \]',
            T(r'$\varepsilon_{t+1}$: a zero-mean shock; $\pi \in (0, 1)$: the survival probability', r'$\varepsilon_{t+1}$: un șoc cu media zero; $\pi \in (0, 1)$: probabilitatea de supraviețuire')]),
          T(r'Check: $\E_t B_{t+1} = \pi\cdot\frac{1 + r}{\pi}B_t = (1 + r)B_t$: a valid rational bubble',
            r'Verificare: $\E_t B_{t+1} = \pi\cdot\frac{1 + r}{\pi}B_t = (1 + r)B_t$: o bulă rațională validă'),
          T(r'Survival time is geometric: expected duration $1/(1 - \pi)$; $\pi = 0.98$ gives @{ra.dur} periods',
            r'Durata de supraviețuire este geometrică: durata așteptată $1/(1 - \pi)$; $\pi = 0.98$ dă @{ra.dur} de perioade'),
          T(r'While it survives it grows at $(1 + r)/\pi - 1 > r$: the extra return pays for the crash risk',
            r'Cît timp supraviețuiește, crește cu $(1 + r)/\pi - 1 > r$: randamentul suplimentar compensează riscul de crah'),
          T(r'After a burst it restarts from noise, which can be negative: the next slide shows why that is a problem',
            r'După spargere repornește din zgomot, care poate fi negativ: slide-ul următor arată de ce este o problemă')), '0.32', '0.66'), 'small')

D.frame(T('The Diba--Grossman critique', 'Critica Diba--Grossman'), items(
    (T(r'Write $B_{t+1} = (1 + r)B_t + z_{t+1}$ with $\E_t z_{t+1} = 0$ \refDGa',
       r'Scriem $B_{t+1} = (1 + r)B_t + z_{t+1}$ cu $\E_t z_{t+1} = 0$ \refDGa'), []),
    (T(r'\textbf{No negative bubbles}: if $B_t < 0$, then $\E_t B_{t+k} = (1 + r)^k B_t \to -\infty$, so the expected price eventually becomes negative; free disposal ($P \ge 0$) rules this out',
       r'\textbf{Nu există bule negative}: dacă $B_t < 0$, atunci $\E_t B_{t+k} = (1 + r)^k B_t \to -\infty$, deci prețul așteptat devine la un moment dat negativ; posibilitatea renunțării gratuite la activ ($P \ge 0$) exclude acest lucru'), []),
    (T(r'\textbf{No birth}: if $B_t = 0$, then $\E_t B_{t+1} = 0$ and $B_{t+1} \ge 0$, hence $B_{t+1} = 0$ almost surely; a bubble that exists today existed on the first trading day',
       r'\textbf{Nu apar ulterior}: dacă $B_t = 0$, atunci $\E_t B_{t+1} = 0$ și $B_{t+1} \ge 0$, deci $B_{t+1} = 0$ aproape sigur; o bulă care există azi exista din prima zi de tranzacționare'),
     [T('the Blanchard--Watson restart from noise violates both points; a bubble can still burst, but not restart',
        'repornirea din zgomot a bulei Blanchard--Watson încalcă ambele puncte; o bulă se poate totuși sparge, dar nu poate reporni')]),
    (T(r'\textbf{Test} \refDGb: no bubble $\Rightarrow$ $P_t$ and $D_t$ cointegrated and $\Delta P_t$ stationary; on annual US data they found no explosive component',
       r'\textbf{Testul} \refDGb: fără bulă $\Rightarrow$ $P_t$ și $D_t$ cointegrate, iar $\Delta P_t$ staționar; pe date anuale din SUA nu au găsit o componentă explozivă'),
     [T(r'unobserved fundamentals or a time-varying $r$ make the test a joint test of the bubble and of the pricing model \refGur',
        r'fundamentele neobservate sau un $r$ variabil în timp fac din test un test comun al bulei și al modelului de evaluare \refGur')])), 'small')

D.frame(T('Evans: periodically collapsing bubbles', 'Evans: bule care se prăbușesc periodic'), items(
    (T(r'Parameters $0 < \delta < (1 + r)\alpha$, $u_{t+1} > 0$ i.i.d.\ with $\E u = 1$, $\theta_{t+1} \sim$ Bernoulli($\pi$) \refEv',
       r'Parametrii $0 < \delta < (1 + r)\alpha$, $u_{t+1} > 0$ i.i.d.\ cu $\E u = 1$, $\theta_{t+1} \sim$ Bernoulli($\pi$) \refEv'),
     [T(r'$B_{t+1} = (1 + r)B_t u_{t+1}$ if $B_t \le \alpha$ (slow growth phase)', r'$B_{t+1} = (1 + r)B_t u_{t+1}$ dacă $B_t \le \alpha$ (faza de creștere lentă)'),
      T(r'$B_{t+1} = \big[\delta + \pi^{-1}(1 + r)\theta_{t+1}\big(B_t - \delta/(1 + r)\big)\big]u_{t+1}$ if $B_t > \alpha$ (fast phase that collapses to $\delta$)',
        r'$B_{t+1} = \big[\delta + \pi^{-1}(1 + r)\theta_{t+1}\big(B_t - \delta/(1 + r)\big)\big]u_{t+1}$ dacă $B_t > \alpha$ (faza rapidă, care se prăbușește la $\delta$)')]),
    (T(r'Exercise: show $\E_t B_{t+1} = (1 + r)B_t$ in both regimes (use $\E\theta = \pi$); the bubble is positive and never dies, consistent with Diba--Grossman',
       r'Exercițiu: arătați că $\E_t B_{t+1} = (1 + r)B_t$ în ambele regimuri (folosiți $\E\theta = \pi$); bula este pozitivă și nu dispare, în acord cu Diba--Grossman'), []),
    (T(r'Evans\' point: on the whole sample, frequent collapses make $P_t$ look like an I(1) or even stationary process; unit-root and cointegration tests have almost no power',
       r'Observația lui Evans: pe tot eșantionul, prăbușirile frecvente fac ca $P_t$ să arate ca un proces I(1) sau chiar staționar; testele de rădăcină unitară și de cointegrare aproape nu au putere'),
     [T(r'the full-sample OLS slope pairs the largest falls with the highest lagged levels: collapses pull $\hat\delta$ down',
        r'panta OLS pe tot eșantionul împerechează cele mai mari scăderi cu cele mai mari niveluri anterioare: prăbușirile trag $\hat\delta$ în jos')]),
    T(r'The remedy of \refPWY and \refPSYa: estimate on sub-samples (windows) and take the supremum, so that some windows contain the expansion but not the collapse',
      r'Remediul din \refPWY și \refPSYa: estimarea pe subeșantioane (ferestre) și supremul statisticilor, astfel încît unele ferestre să conțină expansiunea, dar nu și prăbușirea')), 'small')

chart(T('Simulated rational bubbles and their detection', 'Bule raționale simulate și detectarea lor'), 'ats_ch16_rational', 'ATS_ch16_rational_bubbles', [
    T(r'Left: Blanchard--Watson, $r = 0.02$, $\pi = 0.98$; middle: Evans bubble times 20 on the fundamental of the worked example ($r = 0.05$, $\alpha = 1$, $\delta = 0.5$, $\pi = 0.85$); right: BSADF of the Evans price against its pointwise 95\% critical value (@{ra.R} Monte Carlo paths)',
      r'Stînga: Blanchard--Watson, $r = 0.02$, $\pi = 0.98$; mijloc: bula Evans înmulțită cu 20 peste fundamentul din exemplul rezolvat ($r = 0.05$, $\alpha = 1$, $\delta = 0.5$, $\pi = 0.85$); dreapta: BSADF al prețului Evans față de valoarea critică punctuală de 95\% (@{ra.R} de traiectorii Monte Carlo)'),
    T(r'Whole-sample ADF $@{ra.adf}$ (95\% critical value $@{ra.cvadf}$); SADF $@{ra.sadf}$ ($@{ra.cvsadf}$); GSADF $@{ra.gsadf}$ ($@{ra.cvgsadf}$); @{ra.nep} dated episodes',
      r'ADF pe tot eșantionul $@{ra.adf}$ (valoarea critică de 95\% $@{ra.cvadf}$); SADF $@{ra.sadf}$ ($@{ra.cvsadf}$); GSADF $@{ra.gsadf}$ ($@{ra.cvgsadf}$); @{ra.nep} episoade datate')],
    h='0.56\\textheight')

interp(('the simulated bubbles', 'bulelor simulate'), [
    T(r'The Blanchard--Watson path restarts below zero after a burst and then explodes downwards: exactly the negative bubble that Diba and Grossman exclude',
      r'Traiectoria Blanchard--Watson repornește sub zero după spargere și apoi explodează în jos: exact bula negativă pe care Diba și Grossman o exclud'),
    T(r'The Evans price looks like its fundamental most of the time; the whole-sample ADF ($@{ra.adf}$) is even below its 95\% critical value: Evans\' pitfall in one number',
      r'Prețul Evans arată de cele mai multe ori ca fundamentul său; ADF pe tot eșantionul ($@{ra.adf}$) este chiar sub valoarea critică de 95\%: capcana lui Evans într-o singură cifră'),
    T(r'The window statistics see the large expansions: GSADF $@{ra.gsadf}$ against $@{ra.cvgsadf}$; the BSADF sequence crosses its critical value only in the long runs',
      r'Statisticile pe ferestre văd expansiunile mari: GSADF $@{ra.gsadf}$ față de $@{ra.cvgsadf}$; șirul BSADF depășește valoarea critică doar în episoadele lungi'),
    T(r'The minimum-duration rule ($@{ra.L}$ consecutive exceedances) keeps @{ra.nep} episodes and drops the short bursts: power is traded for fewer false alarms',
      r'Regula duratei minime ($@{ra.L}$ depășiri consecutive) păstrează @{ra.nep} episoade și elimină exploziile scurte: puterea se sacrifică pentru mai puține alarme false')])

D.recap(('rational bubbles', 'bulele raționale'), [
    T(r'Price = fundamental + bubble, with $\E_t B_{t+1} = (1 + r)B_t$: a bubble is an explosive autoregressive component',
      r'Prețul = fundamentul + bula, cu $\E_t B_{t+1} = (1 + r)B_t$: bula este o componentă autoregresivă explozivă'),
    T('Diba--Grossman: bubbles cannot be negative and cannot start later; they can only grow or burst',
      'Diba--Grossman: bulele nu pot fi negative și nu pot apărea ulterior; pot doar să crească sau să se spargă'),
    T('Evans: periodic collapses hide the bubble from whole-sample tests; recursive window tests restore the power',
      'Evans: prăbușirile periodice ascund bula de testele pe tot eșantionul; testele recursive pe ferestre refac puterea'),
    T('Every bubble test is a joint test with the model of the fundamental (a constant $r$, observed dividends or rents)',
      'Orice test de bulă este un test comun cu modelul fundamentului (un $r$ constant, dividende sau chirii observate)')])

# =============================================================================
# 2. ASIMPTOTICA PROCESELOR EXPLOZIVE
# =============================================================================
D.section('Explosive autoregressions', 'Procese autoregresive explozive')

D.frame(T('Three regimes of the AR(1) estimator (1/2)', 'Trei regimuri ale estimatorului AR(1) (1/2)'), '{\\renewcommand{\\arraystretch}{2.0}' + table(
    '@{}lll@{}',
    T(r'\textbf{Root}', r'\textbf{Rădăcina}') + ' & ' + T(r'\textbf{Rate and limit of} $\hat\rho - \rho$', r'\textbf{Rata și limita lui} $\hat\rho - \rho$') + ' & ' + T(r'\textbf{Invariance}', r'\textbf{Invarianța}'),
    [T(r'$|\rho| < 1$', r'$|\rho| < 1$') + r' & $\sqrt n(\hat\rho - \rho) \Rightarrow N(0, 1 - \rho^2)$ & ' + T('yes (CLT)', 'da (CLT)'),
     T(r'$\rho = 1$', r'$\rho = 1$') + r' & $n(\hat\rho - 1) \Rightarrow \int_0^1 W\,dW \big/ \int_0^1 W^2$ & ' + T('yes (FCLT)', 'da (FCLT)'),
     T(r'$\rho = 1 + c/k_n$, $k_n \to \infty$, $k_n = o(n)$', r'$\rho = 1 + c/k_n$, $k_n \to \infty$, $k_n = o(n)$') + r' & $\dfrac{k_n\rho_n^{\,n}}{2c}(\hat\rho - \rho_n) \Rightarrow \mathcal C$ & ' + T('yes \\refPM', 'da \\refPM'),
     T(r'$|\rho| > 1$ fixed', r'$|\rho| > 1$ fix') + r' & $\dfrac{\rho^n}{\rho^2 - 1}(\hat\rho - \rho) \Rightarrow \mathcal C$ & ' + T('only Gaussian errors \\refWhi; \\refAnd', 'doar erori gaussiene \\refWhi; \\refAnd')],
    size='footnotesize') + '}' + items(
    (T(r'Model: $y_t = \rho y_{t-1} + u_t$, $y_0 = 0$, $u_t$ i.i.d.\ $(0, \sigma^2)$; $\hat\rho$: OLS without intercept',
       r'Modelul: $y_t = \rho y_{t-1} + u_t$, $y_0 = 0$, $u_t$ i.i.d.\ $(0, \sigma^2)$; $\hat\rho$: OLS fără termen liber'),
     [T(r'$n$: sample size; $W$: a standard Brownian motion; $\mathcal C$: the standard Cauchy law; $\Rightarrow$: convergence in distribution',
        r'$n$: mărimea eșantionului; $W$: o mișcare browniană standard; $\mathcal C$: legea Cauchy standard; $\Rightarrow$: convergență în distribuție'),
      T(r'CLT/FCLT: (functional) central limit theorem', r'CLT/FCLT: teorema limită centrală (funcțională)')])), 'small')

D.frame(T('Three regimes of the AR(1) estimator (2/2)', 'Trei regimuri ale estimatorului AR(1) (2/2)'), items(
    (T(r'Mildly explosive root: $\rho_n = 1 + c/k_n$', r'Rădăcină ușor explozivă: $\rho_n = 1 + c/k_n$'),
     [T(r'$c > 0$, and $k_n \to \infty$ more slowly than $n$: $k_n = o(n)$, i.e.\ $k_n/n \to 0$', r'$c > 0$, iar $k_n \to \infty$ mai lent decît $n$: $k_n = o(n)$, adică $k_n/n \to 0$'),
      T(r'the Cauchy limit is derived in the Appendix % applink: the mildly explosive Cauchy limit', r'limita Cauchy este derivată în Anexă % applink: limita Cauchy în cazul ușor exploziv')]),
    (T(r'The rate grows from $\sqrt n$ to $n$ to the exponential $\rho^n$', r'Rata crește de la $\sqrt n$ la $n$ și la exponențialul $\rho^n$'),
     [T(r'the further from unity, the faster we learn $\rho$', r'cu cît sîntem mai departe de 1, cu atît învățăm mai repede $\rho$'),
      T(r'unit roots: Chapter 2 and \refHam, Chapter 17', r'rădăcini unitare: Capitolul 2 și \refHam, capitolul 17')]),
    (T('Mildly explosive roots are the realistic case for bubbles', 'Rădăcinile ușor explozive sînt cazul realist pentru bule'),
     [T('faster than any local-to-unity root $1 + c/n$', 'mai rapide decît orice rădăcină locală la unitate $1 + c/n$'),
      T('slower than any fixed explosive root', 'mai lente decît orice rădăcină explozivă fixă'),
      T('their limit theory is invariant to the error law, unlike the fixed explosive case', 'teoria lor asimptotică nu depinde de legea erorilor, spre deosebire de cazul exploziv fix')])), 'small')

D.frame(T('Worked derivation: where the Cauchy law comes from', 'Derivare rezolvată: de unde vine legea Cauchy'), items(
    (T(r'$\hat\rho - \rho = \sum_{t} y_{t-1}u_t \big/ \sum_t y_{t-1}^2$ and $y_t = \sum_{j \le t}\rho^{t-j}u_j$', r'$\hat\rho - \rho = \sum_{t} y_{t-1}u_t \big/ \sum_t y_{t-1}^2$ și $y_t = \sum_{j \le t}\rho^{t-j}u_j$'), []),
    (T(r'Define $Y_n = \sum_{j=1}^{n}\rho^{-j}u_j$ (dominated by the \textbf{first} shocks) and $X_n = \sum_{j=1}^{n}\rho^{-(n-j)-1}u_j$ (dominated by the \textbf{last} shocks)',
       r'Definim $Y_n = \sum_{j=1}^{n}\rho^{-j}u_j$ (dominat de \textbf{primele} șocuri) și $X_n = \sum_{j=1}^{n}\rho^{-(n-j)-1}u_j$ (dominat de \textbf{ultimele} șocuri)'),
     [T(r'then $\rho^{-n}y_n \approx Y_n$, $\rho^{-2n}\sum_t y_{t-1}^2 \approx Y_n^2/(\rho^2 - 1)$ and $\rho^{-n}\sum_t y_{t-1}u_t \approx X_nY_n$',
        r'atunci $\rho^{-n}y_n \approx Y_n$, $\rho^{-2n}\sum_t y_{t-1}^2 \approx Y_n^2/(\rho^2 - 1)$ și $\rho^{-n}\sum_t y_{t-1}u_t \approx X_nY_n$')]),
    (T(r'Hence $\dfrac{\rho^n}{\rho^2 - 1}(\hat\rho - \rho) \approx \dfrac{X_n}{Y_n}$',
       r'Deci $\dfrac{\rho^n}{\rho^2 - 1}(\hat\rho - \rho) \approx \dfrac{X_n}{Y_n}$'),
     [T(r'$X_n$ and $Y_n$ use disjoint blocks of shocks asymptotically: independent, with equal variances $\sigma^2/(\rho^2 - 1)$', r'$X_n$ și $Y_n$ folosesc asimptotic blocuri disjuncte de șocuri: independente, cu dispersii egale $\sigma^2/(\rho^2 - 1)$'),
      T(r'\textbf{fixed} $\rho$: each sum is dominated by a few shocks; it is Gaussian only if the $u_j$ are Gaussian, so the ratio is Cauchy only then \refAnd',
        r'$\rho$ \textbf{fix}: fiecare sumă este dominată de cîteva șocuri; este gaussiană doar dacă $u_j$ sînt gaussiene, deci raportul este Cauchy doar atunci \refAnd'),
      T(r'\textbf{mildly explosive} $\rho_n$: about $k_n \to \infty$ shocks enter each sum with comparable weights, a CLT applies, and $X_n/Y_n \Rightarrow \mathcal C$ for any i.i.d.\ errors with finite variance \refPM',
        r'$\rho_n$ \textbf{ușor exploziv}: aproximativ $k_n \to \infty$ șocuri intră în fiecare sumă cu ponderi comparabile, se aplică o teoremă limită centrală, iar $X_n/Y_n \Rightarrow \mathcal C$ pentru orice erori i.i.d.\ cu dispersie finită \refPM')]),
    T(r'Pivotal inference: the 95\% interval $\hat\rho \pm (\hat\rho^2 - 1)\hat\rho^{-n}\tan(0.475\pi)$, with $\tan(0.475\pi) \approx 12.71$, replaces $\rho$ by $\hat\rho$ in the norming factor',
      r'Inferență pivotală: intervalul de 95\% $\hat\rho \pm (\hat\rho^2 - 1)\hat\rho^{-n}\tan(0.475\pi)$, cu $\tan(0.475\pi) \approx 12.71$, înlocuiește $\rho$ cu $\hat\rho$ în factorul de normare')), 'footnotesize')

chart(T('Cauchy limits in finite samples', 'Limitele Cauchy în eșantioane finite'), 'ats_ch16_asymptotics', 'ATS_ch16_explosive_asymptotics', [
    T(r'@{as.R} samples; normalised error $\rho^n(\hat\rho - \rho)/(\rho^2 - 1)$ with Gaussian and centred exponential errors (skewed), against the Cauchy density',
      r'@{as.R} de eșantioane; eroarea normată $\rho^n(\hat\rho - \rho)/(\rho^2 - 1)$ cu erori gaussiene și exponențiale centrate (asimetrice), față de densitatea Cauchy'),
    T(r'Kolmogorov--Smirnov distance to Cauchy: mild, $n = 200$: @{as.mildnormal.ks} and @{as.mildexp.ks}; $n = 2000$ ($\rho = @{as.rhobig}$): @{as.mildbignormal.ks} ($p$ @{as.mildbignormal.p}) and @{as.mildbigexp.ks} ($p$ @{as.mildbigexp.p}); fixed $\rho = 2$: @{as.fixednormal.ks} ($p$ @{as.fixednormal.p}) and @{as.fixedexp.ks} ($p$ @{as.fixedexp.p})',
      r'Distanța Kolmogorov--Smirnov față de Cauchy: ușor exploziv, $n = 200$: @{as.mildnormal.ks} și @{as.mildexp.ks}; $n = 2000$ ($\rho = @{as.rhobig}$): @{as.mildbignormal.ks} ($p$ @{as.mildbignormal.p}) și @{as.mildbigexp.ks} ($p$ @{as.mildbigexp.p}); $\rho = 2$ fix: @{as.fixednormal.ks} ($p$ @{as.fixednormal.p}) și @{as.fixedexp.ks} ($p$ @{as.fixedexp.p})')],
    h='0.55\\textheight')

interp(('the Cauchy limits', 'limitelor Cauchy'), [
    T(r'Fixed root: with Gaussian errors the Cauchy law fits ($p$ @{as.fixednormal.p}); with skewed errors it is rejected ($p$ @{as.fixedexp.p}): no invariance principle, as Anderson showed',
      r'Rădăcină fixă: cu erori gaussiene legea Cauchy se potrivește ($p$ @{as.fixednormal.p}); cu erori asimetrice este respinsă ($p$ @{as.fixedexp.p}): nu există un principiu de invarianță, cum a arătat Anderson'),
    T(r'Mildly explosive root: at $n = 2000$ both error laws give the Cauchy law; at $n = 200$ ($k_n = @{as.k}$) the approximation is still rough for both: the CLT inside $X_n$ and $Y_n$ needs many effective shocks',
      r'Rădăcină ușor explozivă: la $n = 2000$ ambele legi ale erorilor dau legea Cauchy; la $n = 200$ ($k_n = @{as.k}$) aproximarea este încă grosieră pentru ambele: teorema limită centrală din $X_n$ și $Y_n$ cere multe șocuri efective'),
    T(r'Coverage of the 95\% Cauchy interval: @{as.mildnormal.cov}\% and @{as.mildexp.cov}\% ($n = 200$), @{as.mildbignormal.cov}\% and @{as.mildbigexp.cov}\% ($n = 2000$): conservative in small samples, accurate in large ones',
      r'Acoperirea intervalului Cauchy de 95\%: @{as.mildnormal.cov}\% și @{as.mildexp.cov}\% ($n = 200$), @{as.mildbignormal.cov}\% și @{as.mildbigexp.cov}\% ($n = 2000$): conservator în eșantioane mici, precis în eșantioane mari'),
    T('For bubble tests this is good news: the explosive alternative is learned at an exponential rate, so the window statistics diverge fast once a window sits inside a bubble',
      'Pentru testele de bulă aceasta este o veste bună: alternativa explozivă se învață cu rată exponențială, deci statisticile pe ferestre diverg repede cînd o fereastră se află în interiorul bulei')])

D.frame(T('From limit theory to bubble tests', 'De la teoria asimptotică la testele de bulă'), items(
    (T(r'Under a mildly explosive alternative the ADF $t$-statistic diverges to $+\infty$: right-tailed tests are \textbf{consistent} \refPSYb',
       r'Sub o alternativă ușor explozivă statistica $t$ ADF diverge la $+\infty$: testele pe coada din dreapta sînt \textbf{consistente} \refPSYb'), []),
    (T(r'Levels against logs: a rational bubble is explosive in the \textbf{level}; in logs a pure bubble path $\ln B_0 + t\ln(1 + r)$ is a linear trend',
       r'Niveluri față de logaritmi: o bulă rațională este explozivă în \textbf{nivel}; în logaritmi, o traiectorie pură $\ln B_0 + t\ln(1 + r)$ este o tendință liniară'),
     [T(r'$\ln(F_t + B_t)$ \textbf{accelerates} while the bubble share rises: log-price tests target accelerating log prices, which is what PWY and PSY test in practice',
        r'$\ln(F_t + B_t)$ \textbf{accelerează} cît timp ponderea bulei crește: testele pe logaritmul prețului vizează accelerarea, ceea ce testează în practică PWY și PSY')]),
    (T(r'Specification matters: the intercept, a weak drift $dT^{-\eta}$ ($\eta > 1/2$) in the null, and the lag order change the null limit and the size \refPSYs',
       r'Specificația contează: termenul liber, o derivă slabă $dT^{-\eta}$ ($\eta > 1/2$) sub ipoteza nulă și numărul de laguri schimbă limita sub ipoteza nulă și nivelul testului \refPSYs'), []),
    T(r'Collapses: a sudden fall is a mildly \textbf{integrated} or stationary phase after the explosive one; \refPSi date the implosion with a reverse regression',
      r'Prăbușirile: o scădere bruscă este o fază ușor \textbf{integrată} sau staționară după cea explozivă; \refPSi datează implozia cu o regresie inversă')), 'small')

D.recap(('explosive autoregressions', 'procesele autoregresive explozive'), [
    T(r'Explosive roots are learned at rate $\rho^n$; the limit is Cauchy, a ratio of two independent normals built from the first and the last shocks',
      r'Rădăcinile explozive se învață cu rata $\rho^n$; limita este Cauchy, un raport de două normale independente construite din primele și ultimele șocuri'),
    T('Fixed explosive roots have no invariance principle; mildly explosive roots do, which makes them the working model for bubbles',
      'Rădăcinile explozive fixe nu au un principiu de invarianță; cele ușor explozive au, de aceea sînt modelul de lucru pentru bule'),
    T('The Cauchy interval for $\\rho$ is pivotal but needs large samples; right-tailed tests are consistent against mildly explosive alternatives',
      'Intervalul Cauchy pentru $\\rho$ este pivotal, dar cere eșantioane mari; testele pe coada din dreapta sînt consistente față de alternative ușor explozive')])

# =============================================================================
# 3. TESTELE PSY: TEORIE ȘI NIVEL
# =============================================================================
D.section('Recursive tests: theory and size', 'Testele recursive: teorie și nivel')

D.frame(T('The recursive statistics (1/2)', 'Statisticile recursive (1/2)'), items(
    (T(r'\textbf{Window regression} on the log price $y_t$, over the sample fractions $[r_1, r_2]$', r'\textbf{Regresia pe fereastră} pentru logaritmul prețului $y_t$, pe fracțiunile de eșantion $[r_1, r_2]$'),
     [r'\[ \Delta y_t = a + \delta y_{t-1} + \sum_{j=1}^{k}\phi_j\Delta y_{t-j} + e_t, \qquad t = \lfloor r_1T\rfloor, \dots, \lfloor r_2T\rfloor \]',
      T(r'$\Delta y_t = y_t - y_{t-1}$; $a$: intercept; $\delta$: the coefficient tested; $\phi_j$: coefficients of $k$ lagged differences; $e_t$: error; $T$: sample size; $\lfloor\cdot\rfloor$: integer part',
        r'$\Delta y_t = y_t - y_{t-1}$; $a$: termenul liber; $\delta$: coeficientul testat; $\phi_j$: coeficienții celor $k$ diferențe cu lag; $e_t$: eroarea; $T$: mărimea eșantionului; $\lfloor\cdot\rfloor$: partea întreagă'),
      T(r'$\mathrm{ADF}_{r_1}^{r_2}$: the $t$-statistic of $\delta$ on this window', r'$\mathrm{ADF}_{r_1}^{r_2}$: statistica $t$ a lui $\delta$ pe această fereastră')]),
    (T(r'$H_0$: $\delta = 0$ (unit root) against $H_1$: $\delta > 0$ (explosive): a \textbf{right-tailed} test', r'$H_0$: $\delta = 0$ (rădăcină unitară) față de $H_1$: $\delta > 0$ (explozivă): un test pe \textbf{coada din dreapta}'),
     [T(r'minimum window fraction $r_0 = 0.01 + 1.8/\sqrt T$', r'fracțiunea minimă a ferestrei $r_0 = 0.01 + 1.8/\sqrt T$')]),
    (T('\\textbf{Suprema} over windows \\refPWY, \\refPSYa', '\\textbf{Supremele} pe ferestre \\refPWY, \\refPSYa'),
     [r'\[ \mathrm{SADF} = \sup_{r_2 \in [r_0, 1]}\mathrm{ADF}_0^{r_2}, \quad \mathrm{BSADF}_{r_2} = \sup_{r_1 \in [0, r_2 - r_0]}\mathrm{ADF}_{r_1}^{r_2}, \quad \mathrm{GSADF} = \sup_{r_2}\mathrm{BSADF}_{r_2} \]',
      T(r'SADF: windows starting at the first observation; BSADF: all windows ending at $r_2$ (used to date); GSADF: all windows', r'SADF: ferestre care încep cu prima observație; BSADF: toate ferestrele care se termină în $r_2$ (folosit la datare); GSADF: toate ferestrele')])), 'small')

D.frame(T('The recursive statistics (2/2)', 'Statisticile recursive (2/2)'), items(
    (T(r'Null limit (PSY, Theorem 1), with $r_w = r_2 - r_1$ and integrals over $[r_1, r_2]$:',
       r'Limita sub ipoteza nulă (PSY, teorema 1), cu $r_w = r_2 - r_1$ și integrale pe $[r_1, r_2]$:'),
     [r'\[ \mathrm{ADF}_{r_1}^{r_2} \Rightarrow \dfrac{\frac12 r_w\left[W(r_2)^2 - W(r_1)^2 - r_w\right] - \int W\,dr\,\left[W(r_2) - W(r_1)\right]}{r_w^{1/2}\left\{r_w\int W^2dr - \left(\int W\,dr\right)^2\right\}^{1/2}} \]',
      T(r'$W$: a standard Brownian motion; $\Rightarrow$: convergence in distribution as $T \to \infty$', r'$W$: o mișcare browniană standard; $\Rightarrow$: convergență în distribuție cînd $T \to \infty$'),
      T('pivotal: free of $\\sigma$ and of the drift, so critical values depend only on $r_0$, the deterministic terms and $T$ in finite samples',
        'pivotală: nu depinde de $\\sigma$ și de derivă, deci valorile critice depind doar de $r_0$, de termenii determiniști și, în eșantioane finite, de $T$')]),
    T(r'Computation: for $T = 400$ there are @{nu.400.win} window regressions; cumulated cross-products give all of them in $O(T^2)$ operations',
      r'Calcul: pentru $T = 400$ există @{nu.400.win} de regresii pe ferestre; produsele încrucișate cumulate le dau pe toate în $O(T^2)$ operații')), 'small')

chart(T('Null distributions and critical values', 'Distribuțiile sub ipoteza nulă și valorile critice'), 'ats_ch16_null', 'ATS_ch16_recursive_tests', [
    T(r'Null model $y_t = T^{-1} + y_{t-1} + e_t$, $e_t \sim N(0, 1)$, no lags; 95\% critical values at $T = 100, 200, 400, 800$: SADF @{nu.100.sadf}, @{nu.200.sadf}, @{nu.400.sadf}, @{nu.800.sadf}; GSADF @{nu.100.gsadf}, @{nu.200.gsadf}, @{nu.400.gsadf}, @{nu.800.gsadf}',
      r'Modelul nul $y_t = T^{-1} + y_{t-1} + e_t$, $e_t \sim N(0, 1)$, fără laguri; valori critice de 95\% la $T = 100, 200, 400, 800$: SADF @{nu.100.sadf}, @{nu.200.sadf}, @{nu.400.sadf}, @{nu.800.sadf}; GSADF @{nu.100.gsadf}, @{nu.200.gsadf}, @{nu.400.gsadf}, @{nu.800.gsadf}')],
    h='0.65\\textheight')

interp(('the null distributions', 'distribuțiilor sub ipoteza nulă'), [
    T(r'The whole-sample ADF has a negative 95\% quantile (@{nu.400.adf} at $T = 400$): using 1.645 would almost never reject, the right tail of the Dickey--Fuller law is short',
      r'ADF pe tot eșantionul are cuantila de 95\% negativă (@{nu.400.adf} la $T = 400$): folosind 1,645 nu s-ar respinge aproape niciodată, coada dreaptă a legii Dickey--Fuller este scurtă'),
    T('Each supremum shifts the distribution to the right: SADF searches over end points, GSADF over start and end points; the GSADF bar is the price of the search',
      'Fiecare suprem mută distribuția spre dreapta: SADF caută pe punctele de sfîrșit, GSADF pe punctele de început și de sfîrșit; pragul GSADF este prețul căutării'),
    T(r'The GSADF critical value rises with $T$ (@{nu.100.gsadf} to @{nu.800.gsadf}) although $r_0$ falls: more windows, a larger maximum; tabulate critical values for your own $T$, $r_0$ and lag order',
      r'Valoarea critică GSADF crește cu $T$ (de la @{nu.100.gsadf} la @{nu.800.gsadf}) deși $r_0$ scade: mai multe ferestre, un maxim mai mare; simulați valorile critice pentru propriile $T$, $r_0$ și număr de laguri'),
    T(r'The pointwise 95\% quantile of BSADF at the last date (@{nu.400.bs} at $T = 400$) is far below the GSADF one: a single date is tested at 5\%, the whole path is not',
      r'Cuantila punctuală de 95\% a BSADF la ultima dată (@{nu.400.bs} la $T = 400$) este mult sub cea GSADF: o singură dată este testată la 5\%, întreaga traiectorie nu')])

D.frame(T('Changing volatility and the wild bootstrap', 'Volatilitate variabilă și wild bootstrap'), items(
    (T(r'The pivotal limit assumes homoskedastic shocks; with a volatility shift the limit involves the variance profile, and Monte Carlo critical values give the wrong size \refHLST',
       r'Limita pivotală presupune șocuri homoscedastice; cu o schimbare a volatilității limita depinde de profilul dispersiei, iar valorile critice Monte Carlo dau un nivel greșit \refHLST'),
     [T('a late rise in volatility looks like acceleration; a fall in volatility makes the test conservative', 'o creștere tîrzie a volatilității arată ca o accelerare; o scădere a volatilității face testul conservator')]),
    (T(r'\textbf{Wild bootstrap} \refPS: fit the null $\Delta y_t = \mu + \sum_j\phi_j\Delta y_{t-j} + e_t$, draw Rademacher signs $w_t = \pm 1$, build $\Delta y^*_t = \sum_j\hat\phi_j\Delta y^*_{t-j} + w_t\hat e_t$, cumulate, recompute the statistics',
       r'\textbf{Wild bootstrap} \refPS: estimăm modelul nul $\Delta y_t = \mu + \sum_j\phi_j\Delta y_{t-j} + e_t$, extragem semne Rademacher $w_t = \pm 1$, construim $\Delta y^*_t = \sum_j\hat\phi_j\Delta y^*_{t-j} + w_t\hat e_t$, cumulăm și recalculăm statisticile'),
     [T(r'the bootstrap series has a unit root by construction and the \textbf{same volatility pattern} $|\hat e_t|$ as the data', r'seria bootstrap are prin construcție o rădăcină unitară și \textbf{același tipar al volatilității} $|\hat e_t|$ ca datele'),
      T('critical values: pointwise quantiles of BSADF, the quantile of the maximum (GSADF), or the quantile of the maximum over a moving window', 'valori critice: cuantilele punctuale ale BSADF, cuantila maximului (GSADF) sau cuantila maximului pe o fereastră mobilă')]),
    T(r'Alternatives for non-stationary volatility: weighted and sign-based statistics \refHLZ; end-of-sample tests \refAHLT',
      r'Alternative pentru volatilitatea nestaționară: statistici ponderate și statistici pe baza semnelor \refHLZ; teste pentru finalul eșantionului \refAHLT')), 'small')

D.frame(T('Many dates, one false alarm', 'Multe date, o alarmă falsă'), items(
    (T(r'Date-stamping compares $\mathrm{BSADF}_{r_2}$ with a \textbf{pointwise} critical value at every date: each date has a 5\% false-alarm chance, but a sample has hundreds of dates',
       r'Datarea compară $\mathrm{BSADF}_{r_2}$ cu o valoare critică \textbf{punctuală} la fiecare dată: fiecare dată are o probabilitate de 5\% de alarmă falsă, dar un eșantion are sute de date'),
     [T('BSADF is highly autocorrelated in $r_2$, so false alarms come in runs: the minimum-duration rule removes the shortest runs only',
        'BSADF este puternic autocorelat în $r_2$, deci alarmele false vin în serii: regula duratei minime elimină doar seriile cele mai scurte')]),
    (T(r'\textbf{Family-wise error rate} (FWER): the probability of at least one false alarm over a set of dates', r'\textbf{Rata erorii de familie} (FWER): probabilitatea a cel puțin unei alarme false pe o mulțime de date'),
     [T(r'over the whole sample: compare BSADF with the 95\% quantile of its maximum, i.e.\ the GSADF critical value', r'pe tot eșantionul: comparăm BSADF cu cuantila de 95\% a maximului său, adică valoarea critică GSADF'),
      T(r'over a moving window of $\tau_b$ dates \refPS: the 95\% bootstrap quantile of $\max_{s \in (t - \tau_b, t]}\mathrm{BSADF}_s$; here $\tau_b = 52$ weeks', r'pe o fereastră mobilă de $\tau_b$ date \refPS: cuantila bootstrap de 95\% a lui $\max_{s \in (t - \tau_b, t]}\mathrm{BSADF}_s$; aici $\tau_b = 52$ de săptămîni')]),
    T(r'Asymptotically, consistent dating needs critical values that diverge slowly, so that the false-alarm probability vanishes \refPSYb; in practice a fixed 5\% at every date is used, and its cost must be measured',
      r'Asimptotic, datarea consistentă cere valori critice care diverg încet, astfel încît probabilitatea alarmei false să dispară \refPSYb; în practică se folosește un 5\% fix la fiecare dată, iar costul lui trebuie măsurat')), 'small')

chart(T('Size under changing volatility and across dates', 'Nivelul testelor sub volatilitate variabilă și pe multe date'), 'ats_ch16_size', 'ATS_ch16_size_wild_bootstrap', [
    T(r'@{sz.N} null paths of $T = @{sz.T}$ per design, each with its own wild bootstrap (@{sz.B} draws); a dated episode needs @{sz.L} consecutive exceedances; nominal level 5\%',
      r'@{sz.N} de traiectorii sub ipoteza nulă cu $T = @{sz.T}$ pentru fiecare design, fiecare cu propriul wild bootstrap (@{sz.B} de extrageri); un episod datat cere @{sz.L} depășiri consecutive; nivelul nominal 5\%')],
    h='0.65\\textheight')

interp(('the size study', 'studiului de nivel'), [
    T(r'GSADF with Monte Carlo critical values: @{sz.iid.rejmc}\% with constant volatility, @{sz.up.rejmc}\% after a late tripling, @{sz.garch.rejmc}\% under GARCH; the wild bootstrap gives @{sz.iid.rejwild}\%, @{sz.up.rejwild}\% and @{sz.garch.rejwild}\%',
      r'GSADF cu valori critice Monte Carlo: @{sz.iid.rejmc}\% cu volatilitate constantă, @{sz.up.rejmc}\% după o triplare tîrzie, @{sz.garch.rejmc}\% sub GARCH; wild bootstrap dă @{sz.iid.rejwild}\%, @{sz.up.rejwild}\% și @{sz.garch.rejwild}\%'),
    T(r'Pointwise dating finds at least one episode in @{sz.iid.epmc}\% (Monte Carlo) and @{sz.iid.epwild}\% (wild) of paths \textbf{without any bubble}, even with constant volatility',
      r'Datarea punctuală găsește cel puțin un episod în @{sz.iid.epmc}\% (Monte Carlo) și @{sz.iid.epwild}\% (wild) dintre traiectoriile \textbf{fără nicio bulă}, chiar cu volatilitate constantă'),
    T(r'With the family-wise threshold over the whole sample, false episodes fall to @{sz.iid.epfw}\%--@{sz.down.epfw}\%: below 5\%, because an episode also needs @{sz.L} consecutive exceedances; the cost is power and later dates',
      r'Cu pragul de familie pe tot eșantionul, episoadele false scad la @{sz.iid.epfw}\%--@{sz.down.epfw}\%: sub 5\%, fiindcă un episod cere și @{sz.L} depășiri consecutive; costul este puterea și datări mai tîrzii'),
    T('Lesson: report which error rate a dated episode controls; a 5\\% pointwise test on every week is not a 5\\% test of the sample',
      'Concluzia: raportați ce rată de eroare controlează un episod datat; un test punctual de 5\\% în fiecare săptămînă nu este un test de 5\\% pentru eșantion')])

D.recap(('recursive tests', 'testele recursive'), [
    T('SADF, GSADF and BSADF are suprema of window ADF statistics with a pivotal null limit; critical values must match $T$, $r_0$, the deterministic terms and the lags',
      'SADF, GSADF și BSADF sînt supreme ale statisticilor ADF pe ferestre, cu o limită pivotală sub ipoteza nulă; valorile critice trebuie să corespundă lui $T$, $r_0$, termenilor determiniști și lagurilor'),
    T('Changing volatility distorts the size; the wild bootstrap keeps the volatility pattern and restores it',
      'Volatilitatea variabilă distorsionează nivelul; wild bootstrap păstrează tiparul volatilității și îl reface'),
    T('Pointwise dating has a high false-episode rate over a sample; family-wise thresholds control it at the cost of power',
      'Datarea punctuală are o rată mare de episoade false pe un eșantion; pragurile de familie o controlează, cu prețul puterii')])

# =============================================================================
# 4. DATARE ȘI AVERTIZARE TIMPURIE
# =============================================================================
D.section('Date-stamping and early warning', 'Datarea și avertizarea timpurie')

D.frame(T('Date-stamping rules and their accuracy', 'Regulile de datare și acuratețea lor'), items(
    (T(r'\textbf{Origination and termination} \refPSYa: the first date where BSADF exceeds its critical value, and the first later date where it falls back below',
       r'\textbf{Începutul și sfîrșitul} \refPSYa: prima dată la care BSADF depășește valoarea critică și prima dată ulterioară la care coboară sub ea'),
     [r'\[ \hat r_e = \inf\{r_2 \ge r_0: \mathrm{BSADF}_{r_2} > cv_{r_2}\}, \qquad \hat r_f = \inf\{r_2 \ge \hat r_e + \delta\ln(T)/T: \mathrm{BSADF}_{r_2} < cv_{r_2}\} \]',
      T(r'$cv_{r_2}$: the pointwise 95\% critical value at $r_2$; $\delta\ln(T)/T$: a minimum duration (with $\delta$ a tuning constant)', r'$cv_{r_2}$: valoarea critică punctuală de 95\% la $r_2$; $\delta\ln(T)/T$: o durată minimă (cu $\delta$ o constantă de calibrare)'),
      T(r'here: an episode is a run of at least $\lceil\ln T\rceil$ consecutive exceedances, dated from the first to the last one (as in \texttt{exuber} \refVPM)',
        r'aici: un episod este o serie de cel puțin $\lceil\ln T\rceil$ depășiri consecutive, datată de la prima la ultima (ca în \texttt{exuber} \refVPM)')]),
    (T(r'In real time an episode is \textbf{confirmed} only after the minimum duration: the alarm date is the start plus $\lceil\ln T\rceil - 1$',
       r'În timp real, un episod este \textbf{confirmat} doar după durata minimă: data alarmei este începutul plus $\lceil\ln T\rceil - 1$'), []),
    (T(r'Consistency of $(\hat r_e, \hat r_f)$ holds for mildly explosive bubbles of fixed fractional duration \refPSYb',
       r'Consistența lui $(\hat r_e, \hat r_f)$ este valabilă pentru bule ușor explozive cu durată fracționară fixă \refPSYb'),
     [T('the start is dated late, because a window must first accumulate explosive observations', 'începutul este datat tîrziu, fiindcă o fereastră trebuie să acumuleze întîi observații explozive'),
      T(r'improved start and end estimators that use the whole bubble period: \refHLS', r'estimatori îmbunătățiți ai începutului și sfîrșitului, care folosesc toată perioada bulei: \refHLS')])), 'small')

D.frame(T('Date-stamping: design of the experiment', 'Datarea: designul experimentului'), items(
    (T(r'Simulated paths: random walk from $y_0 = 100$, then an explosive phase, a collapse, and a random walk again', r'Traiectorii simulate: mers aleator de la $y_0 = 100$, apoi o fază explozivă, o prăbușire și din nou mers aleator'),
     [T(r'explosive phase $y_t = \rho y_{t-1} + e_t$, $\rho > 1$, on periods @{dt.te}--@{dt.tf}; $e_t$: Normal noise', r'faza explozivă $y_t = \rho y_{t-1} + e_t$, $\rho > 1$, în perioadele @{dt.te}--@{dt.tf}; $e_t$: zgomot cu distribuția Normală'),
      T('collapse to the pre-bubble level at the end of the explosive phase', 'prăbușire la nivelul de dinaintea bulei la sfîrșitul fazei explozive'),
      T(r'$T = @{dt.T}$, @{dt.N} paths for each value of $\rho$', r'$T = @{dt.T}$, @{dt.N} traiectorii pentru fiecare valoare a lui $\rho$')]),
    T('Questions: how often is the bubble found, how late is its start dated, how often is a false episode dated before it?', 'Întrebările: cît de des este găsită bula, cît de tîrziu este datat începutul ei, cît de des este datat un episod fals înaintea ei?')), 'small')

chart(T('How late is the start dated?', 'Cît de tîrziu este datat începutul?'), 'ats_ch16_dating', 'ATS_ch16_date_stamping', [
    T(r'Delay of the first dated exceedance after the true start (periods); pointwise 95\% Monte Carlo critical values; growth over the bubble $\rho^{@{dt.dur}}$: @{dt.a.g}, @{dt.b.g} and @{dt.c.g}',
      r'Întîrzierea primei depășiri datate după începutul adevărat (perioade); valori critice punctuale de 95\% Monte Carlo; creșterea pe durata bulei $\rho^{@{dt.dur}}$: @{dt.a.g}, @{dt.b.g} și @{dt.c.g}')],
    h='0.65\\textheight')

interp(('the date-stamping experiment', 'experimentului de datare'), [
    T(r'Detection rates @{dt.a.det}\%, @{dt.b.det}\% and @{dt.c.det}\% for $\rho = 1.005, 1.01, 1.02$: a bubble of @{dt.dur} periods is almost always found',
      r'Ratele de detecție @{dt.a.det}\%, @{dt.b.det}\% și @{dt.c.det}\% pentru $\rho = 1.005, 1.01, 1.02$: o bulă de @{dt.dur} de perioade este găsită aproape întotdeauna'),
    T(r'Median start delays @{dt.a.med}, @{dt.b.med} and @{dt.c.med} periods (interquartile ranges @{dt.a.q25}--@{dt.a.q75}, @{dt.b.q25}--@{dt.b.q75}, @{dt.c.q25}--@{dt.c.q75}); confirmation adds @{dt.L} $-$ 1 periods: medians @{dt.a.conf}, @{dt.b.conf}, @{dt.c.conf}',
      r'Întîrzieri mediane ale începutului @{dt.a.med}, @{dt.b.med} și @{dt.c.med} perioade (intervale intercuartilice @{dt.a.q25}--@{dt.a.q75}, @{dt.b.q25}--@{dt.b.q75}, @{dt.c.q25}--@{dt.c.q75}); confirmarea adaugă @{dt.L} $-$ 1 perioade: mediane @{dt.a.conf}, @{dt.b.conf}, @{dt.c.conf}'),
    T(r'For the slowest bubble the alarm comes after about a third of its life: a detector of \textbf{ongoing} exuberance, not of its birth',
      r'Pentru bula cea mai lentă, alarma vine după aproximativ o treime din viața ei: un detector al exuberanței \textbf{în desfășurare}, nu al nașterii ei'),
    T(r'In @{dt.a.fb}\%--@{dt.c.fb}\% of paths a false episode is dated \textbf{before} the bubble starts: the multiplicity of the previous section, now inside a true-bubble design',
      r'În @{dt.a.fb}\%--@{dt.c.fb}\% dintre traiectorii este datat un episod fals \textbf{înainte} de începutul bulei: multiplicitatea din secțiunea anterioară, acum într-un design cu bulă reală')])

D.frame(T('Real-time monitoring (1/2)', 'Monitorizarea în timp real (1/2)'), items(
    (T(r'Monitoring: a training sample of $n$ observations without a bubble, then a decision at each new date $t > n$; the error rate is over the \textbf{whole} monitoring horizon \refCSW',
       r'Monitorizarea: un eșantion de antrenare de $n$ observații fără bulă, apoi o decizie la fiecare dată nouă $t > n$; rata de eroare se referă la \textbf{întregul} orizont de monitorizare \refCSW'), []),
    (T(r'\textbf{CUSUM} of returns: cumulated deviations of the new returns from the training mean, in units of the training volatility',
       r'\textbf{CUSUM} al randamentelor: abaterile cumulate ale randamentelor noi de la media din perioada de antrenare, în unități ale volatilității din antrenare'),
     [r'\[ S_t = \sum_{j=n+1}^{t}\frac{r_j - \bar r_n}{\hat\sigma_n\sqrt n}, \qquad \text{' + T('alarm when', 'alarmă cînd') + r'}\ S_t > b_t = \sqrt{\tfrac{t - n}{n}\cdot\tfrac{t}{n}\left[a^2 + \ln\tfrac{t}{t - n}\right]} \]',
      T(r'$r_j$: return of period $j$; $\bar r_n$, $\hat\sigma_n$: mean and standard deviation of the training returns; $b_t$: the boundary, which widens with $t$; $a$: a constant that sets the error rate', r'$r_j$: randamentul perioadei $j$; $\bar r_n$, $\hat\sigma_n$: media și abaterea standard a randamentelor din antrenare; $b_t$: frontiera, care se lărgește cu $t$; $a$: o constantă care fixează rata de eroare')]),
    (T(r'Error rate over the whole horizon (proof in the Appendix)', r'Rata de eroare pe întregul orizont (demonstrația în Anexă)'),
     [T(r'$\Pr\{S_t > b_t$ for some $t\} \to 1 - \Phi(a) + a\varphi(a)$; $\Phi$, $\varphi$: standard Normal distribution and density functions', r'$\Pr\{S_t > b_t$ pentru un $t\} \to 1 - \Phi(a) + a\varphi(a)$; $\Phi$, $\varphi$: funcția de repartiție și densitatea distribuției Normale standard'),
      T(r'5\% gives $a = @{mo.a}$, $a^2 = @{mo.a2}$', r'5\% dă $a = @{mo.a}$, $a^2 = @{mo.a2}$')])), 'small')

D.frame(T('Real-time monitoring (2/2)', 'Monitorizarea în timp real (2/2)'), items(
    (T(r'Simulated size, $n = 100$, horizon $5n$, @{mo.Ns} paths', r'Nivelul simulat, $n = 100$, orizont $5n$, @{mo.Ns} de traiectorii'),
     [T(r'@{mo.size}\% with i.i.d.\ returns, @{mo.sizeg}\% with GARCH returns', r'@{mo.size}\% cu randamente i.i.d., @{mo.sizeg}\% cu randamente GARCH')]),
    (T(r'\refHB compare bubble tests and monitoring schemes and recommend monitoring of this kind for real time', r'\refHB compară testele de bulă și schemele de monitorizare și recomandă în timp real monitorizarea de acest tip'),
     [T(r'\refAHLST give monitoring statistics with controlled size for explosive bubbles', r'\refAHLST propun statistici de monitorizare cu nivel controlat pentru bule explozive')]),
    T(r'BSADF in real time is also a monitor: $\mathrm{BSADF}_t$ uses only data up to $t$, but its pointwise critical values do not control the error over the horizon',
      r'BSADF în timp real este și el un monitor: $\mathrm{BSADF}_t$ folosește doar datele pînă la $t$, dar valorile lui critice punctuale nu controlează eroarea pe orizont')), 'small')

chart(T('Monitoring the Nasdaq 100 and Bitcoin', 'Monitorizarea Nasdaq 100 și Bitcoin'), 'ats_ch16_monitor', 'ATS_ch16_monitoring', [
    T(r'Weekly log returns; training: 1990--1994 (Nasdaq 100, $n = @{mo.ndx.n}$) and September 2014 -- June 2016 (Bitcoin, $n = @{mo.btc.n}$); BSADF with pointwise Monte Carlo critical values',
      r'Randamente logaritmice săptămînale; antrenare: 1990--1994 (Nasdaq 100, $n = @{mo.ndx.n}$) și septembrie 2014 -- iunie 2016 (Bitcoin, $n = @{mo.btc.n}$); BSADF cu valori critice punctuale Monte Carlo')],
    h='0.65\\textheight')

interp(('the monitoring charts', 'graficelor de monitorizare'), [
    T(r'Nasdaq 100: the CUSUM alarm comes on @{mo.ndx.cus}, three months before the peak of @{mo.ndx.peak}; the first confirmed BSADF alarm after training comes on @{mo.ndx.bs}, more than four years earlier',
      r'Nasdaq 100: alarma CUSUM apare pe @{mo.ndx.cus}, cu trei luni înaintea maximului din @{mo.ndx.peak}; prima alarmă BSADF confirmată după antrenare apare pe @{mo.ndx.bs}, cu peste patru ani mai devreme'),
    (T(r'Bitcoin: CUSUM on @{mo.btc.cus}, at the top of the 2017 run-up; BSADF on @{mo.btc.bs}',
       r'Bitcoin: CUSUM pe @{mo.btc.cus}, la vîrful creșterii din 2017; BSADF pe @{mo.btc.bs}'),
     [T(r'the boundary widens with $\sqrt{t\ln t}$, so after 2018 the 2021 rally cannot reach it', r'frontiera se lărgește ca $\sqrt{t\ln t}$, deci după 2018 creșterea din 2021 nu o mai poate atinge')]),
    T('CUSUM detects a change in the mean return (persistent acceleration), not explosiveness as such; it is slow, but its size is controlled over the whole horizon',
      'CUSUM detectează o schimbare a randamentului mediu (o accelerare persistentă), nu explozivitatea ca atare; este lent, dar nivelul lui este controlat pe tot orizontul'),
    T('BSADF reacts early and often: an early alarm that is followed by years of further gains is costly to anyone who acts on it',
      'BSADF reacționează devreme și des: o alarmă timpurie urmată de ani de creșteri suplimentare este costisitoare pentru oricine acționează pe baza ei')])

D.frame(T('Evaluating early warnings honestly', 'Evaluarea onestă a avertizărilor timpurii'), items(
    (T(r'Define the \textbf{event} before looking at alarms: here a fall of at least 20\% within 182 days after the date; define the \textbf{alarm} rule and the evaluation dates (every fifth trading day)',
       r'Definiți \textbf{evenimentul} înainte de a vă uita la alarme: aici o scădere de cel puțin 20\% în următoarele 182 de zile; definiți regula de \textbf{alarmă} și datele de evaluare (fiecare a cincea zi de tranzacționare)'), []),
    (T(r'Hit rate $H = \Pr(\text{alarm} \mid \text{event})$, false-alarm rate $F = \Pr(\text{alarm} \mid \text{no event})$, base rate $\pi_0 = \Pr(\text{event})$',
       r'Rata de detecție $H = \Pr(\text{alarmă} \mid \text{eveniment})$, rata alarmelor false $F = \Pr(\text{alarmă} \mid \text{fără eveniment})$, frecvența de bază $\pi_0 = \Pr(\text{eveniment})$'),
     [T(r'\textbf{precision} by Bayes: $\Pr(\text{event} \mid \text{alarm}) = H\pi_0 / [H\pi_0 + F(1 - \pi_0)]$; with $\pi_0 = 5\%$, $H = 80\%$, $F = 20\%$ it is only 17\%',
        r'\textbf{precizia} din regula lui Bayes: $\Pr(\text{eveniment} \mid \text{alarmă}) = H\pi_0 / [H\pi_0 + F(1 - \pi_0)]$; cu $\pi_0 = 5\%$, $H = 80\%$, $F = 20\%$ este doar 17\%'),
      T(r'the noise-to-signal ratio $F/H$ of the early-warning literature \refKLR', r'raportul zgomot/semnal $F/H$ din literatura avertizărilor timpurii \refKLR')]),
    (T(r'\textbf{ROC curve}: $(F, H)$ for every threshold of a continuous score; \textbf{AUC} $= \Pr(\text{score of an event date} > \text{score of a non-event date})$; 0.5 means no skill',
       r'\textbf{Curba ROC}: $(F, H)$ pentru fiecare prag al unui scor continuu; \textbf{AUC} $= \Pr(\text{scorul unei date cu eveniment} > \text{scorul unei date fără eveniment})$; 0,5 înseamnă lipsa abilității'), []),
    T(r'Overlapping horizons make evaluation dates strongly dependent: intervals for the AUC need a moving-block bootstrap (Chapter 0), and a few crashes carry the whole sample',
      r'Orizonturile suprapuse fac datele de evaluare puternic dependente: intervalele pentru AUC cer un moving-block bootstrap (Capitolul 0), iar cîteva crahuri poartă tot eșantionul')), 'small')

D.recap(('date-stamping and early warning', 'datarea și avertizarea timpurie'), [
    T('BSADF dates the start late (after a run of explosive observations) and confirms it later still; slow bubbles are found after a large part of their life',
      'BSADF datează începutul tîrziu (după o serie de observații explozive) și îl confirmă și mai tîrziu; bulele lente sînt găsite după o parte mare din viața lor'),
    T('Monitoring with a boundary controls the error over the whole horizon; pointwise BSADF does not',
      'Monitorizarea cu o frontieră controlează eroarea pe tot orizontul; BSADF punctual nu o face'),
    T('Evaluate alarms with hit rate, false-alarm rate, precision at the base rate and ROC/AUC, with block-bootstrap intervals',
      'Evaluați alarmele prin rata de detecție, rata alarmelor false, precizia la frecvența de bază și ROC/AUC, cu intervale prin block bootstrap')])

# =============================================================================
# 5. FUNDAMENTE ȘI PREȚURI
# =============================================================================
D.section('Fundamentals against prices', 'Fundamentele față de prețuri')

D.frame(T('Testing the ratio, the price and the fundamental', 'Testarea raportului, a prețului și a fundamentului'), two(
    ph('foreclosure', T('A foreclosed home in the United States, 2008', 'O locuință executată silit în SUA, 2008'), h='0.36\\textheight'),
    items(T(r'Under the present-value model the price-to-rent (or price-dividend) ratio is stationary; an explosive \textbf{ratio} with a non-explosive \textbf{fundamental} points to a bubble',
            r'În modelul valorii actualizate, raportul preț/chirie (sau preț/dividend) este staționar; un \textbf{raport} exploziv cu un \textbf{fundament} neexploziv indică o bulă'),
          T(r'If rents themselves explode, an explosive price is not evidence of a bubble: test both (the logic of \refDGb applied with PSY)',
            r'Dacă chiriile explodează ele însele, un preț exploziv nu dovedește o bulă: testați ambele (logica din \refDGb aplicată cu PSY)'),
          T(r'Landmarks: \refPY date the US price-to-rent exuberance before the subprime crisis; \refPav apply GSADF to the international housing panel of the Dallas Fed',
            r'Lucrări de referință: \refPY datează exuberanța raportului preț/chirie din SUA dinaintea crizei subprime; \refPav aplică GSADF pe baza de date internațională a prețurilor locuințelor a Fed din Dallas'),
          T(r'Monthly house prices are smoothed (repeat-sales indices, appraisals): their changes are autocorrelated, so the lag order $k$ matters; here $k$ by BIC, up to 6 months',
            r'Prețurile lunare ale locuințelor sînt netezite (indici de vînzări repetate, evaluări): variațiile lor sînt autocorelate, deci numărul de laguri $k$ contează; aici $k$ după BIC, pînă la 6 luni')), '0.34', '0.64'), 'footnotesize')

chart(T('US and Romanian housing: ratio and fundamental', 'Locuințele din SUA și din România: raportul și fundamentul'), 'ats_ch16_housing', 'ATS_ch16_housing', [
    T(r'Log price-to-rent and log real rent; BSADF with $k$ lags (US ratio $k = @{ho.usratio.k}$, rent $k = @{ho.usrent.k}$) and pointwise 95\% wild-bootstrap critical values (@{ho.B} draws); shaded: dated episodes of the ratio',
      r'Logaritmul raportului preț/chirie și al chiriei reale; BSADF cu $k$ laguri (raportul SUA $k = @{ho.usratio.k}$, chiria $k = @{ho.usrent.k}$) și valori critice punctuale de 95\% prin wild bootstrap (@{ho.B} de extrageri); zonele colorate: episoadele datate ale raportului')],
    h='0.65\\textheight')

interp(('the housing tests', 'testelor pe locuințe'), [
    T(r'US price-to-rent: GSADF @{ho.usratio.g} against the wild-bootstrap value @{ho.usratio.cv}; the main episode runs from @{ho.e1a} to @{ho.e1b}, the boom before the subprime crisis found by \refPY',
      r'Raportul preț/chirie din SUA: GSADF @{ho.usratio.g} față de valoarea wild bootstrap @{ho.usratio.cv}; episodul principal durează din @{ho.e1a} pînă în @{ho.e1b}, boom-ul dinaintea crizei subprime găsit de \refPY'),
    T(r'US real rent: GSADF @{ho.usrent.g} against @{ho.usrent.cv}, with episodes @{ho.rentep}: the fundamental also accelerated, so the 2014--2022 price rise is partly a rent story',
      r'Chiria reală în SUA: GSADF @{ho.usrent.g} față de @{ho.usrent.cv}, cu episoadele @{ho.rentep}: și fundamentul a accelerat, deci creșterea prețurilor din 2014--2022 ține parțial de chirii'),
    T(r'US real house price alone: episodes @{ho.priceep}; the 2020--2022 surge is explosive in the price but not in the ratio, unlike 1998--2006',
      r'Prețul real al locuințelor din SUA, singur: episoadele @{ho.priceep}; creșterea din 2020--2022 este explozivă în preț, dar nu în raport, spre deosebire de 1998--2006'),
    T(r'Romania (quarterly, $T = @{ho.roratio.T}$): GSADF of the ratio @{ho.roratio.g} against @{ho.roratio.cv}, of the real price @{ho.roprice.g} against @{ho.roprice.cv}: no explosive episode since 2009; the HICP rent index jumps by 33\% in April 2026, so the sample ends in March 2026',
      r'România (trimestrial, $T = @{ho.roratio.T}$): GSADF al raportului @{ho.roratio.g} față de @{ho.roratio.cv}, al prețului real @{ho.roprice.g} față de @{ho.roprice.cv}: niciun episod exploziv din 2009; indicele HICP al chiriilor crește cu 33\% în aprilie 2026, de aceea eșantionul se încheie în martie 2026')], size='footnotesize')

D.recap(('fundamentals against prices', 'fundamentele față de prețuri'), [
    T('Test the ratio and the fundamental separately: an explosive ratio with a calm fundamental is the bubble signature',
      'Testați separat raportul și fundamentul: un raport exploziv cu un fundament liniștit este semnătura bulei'),
    T('Smoothed housing indices need lag augmentation and a bootstrap under the AR null; without lags the tests reject almost everywhere',
      'Indicii neteziți ai locuințelor cer laguri în regresie și un bootstrap sub ipoteza nulă AR; fără laguri testele resping aproape peste tot'),
    T('Short samples (Romania since 2009) have little power: no rejection is not evidence of no bubble',
      'Eșantioanele scurte (România din 2009) au putere mică: lipsa respingerii nu dovedește lipsa bulei')])

# =============================================================================
# 6. LPPLS
# =============================================================================
D.section('LPPLS as a competing detector', 'LPPLS ca detector alternativ')

D.frame(T('LPPLS in one slide', 'LPPLS într-un singur slide'), two(
    ph('sornette', T('Didier Sornette, 2012', 'Didier Sornette, 2012'), h='0.36\\textheight'),
    items((T(r'\refJLS: the log price grows faster than exponentially towards a critical time $t_c$, with oscillations that speed up', r'\refJLS: logaritmul prețului crește mai repede decît exponențial spre un timp critic $t_c$, cu oscilații care se accelerează'),
           [r'\[ \ln p(t) = A + B(t_c - t)^m + C_1(t_c - t)^m\cos(\omega\ln(t_c - t)) + C_2(t_c - t)^m\sin(\omega\ln(t_c - t)) \]',
            T(r'$A$: log price at $t_c$; $B < 0$ and $0 < m < 1$: super-exponential growth; $C_1$, $C_2$: amplitudes of the oscillations; $\omega$: their log-frequency', r'$A$: logaritmul prețului la $t_c$; $B < 0$ și $0 < m < 1$: creștere superexponențială; $C_1$, $C_2$: amplitudinile oscilațiilor; $\omega$: frecvența lor logaritmică')]),
          T(r'Two steps \refFS: for given $(t_c, m, \omega)$ the four linear parameters are OLS; minimise the concentrated sum of squares over three nonlinear parameters',
            r'Doi pași \refFS: pentru $(t_c, m, \omega)$ date, cei patru parametri liniari se obțin prin OLS; se minimizează suma de pătrate concentrată pe trei parametri neliniari'),
          T(r'Qualified fits: the filter of \refSZ (bounds on $m$, $\omega$, $t_c$, number of oscillations, damping, relative error, Lomb test, stationary residuals)',
            r'Ajustări calificate: filtrul din \refSZ (limite pentru $m$, $\omega$, $t_c$, numărul de oscilații, amortizare, eroarea relativă, testul Lomb, reziduuri staționare)'),
          T(r'\textbf{Confidence indicator}: the share of qualified fits over many windows ending at the same date (here @{lp.win} windows of 50--750 days)',
            r'\textbf{Indicatorul de încredere}: ponderea ajustărilor calificate pe multe ferestre care se încheie la aceeași dată (aici @{lp.win} de ferestre de 50--750 de zile)')), '0.3', '0.68'), 'footnotesize')

D.frame(T('Inference on the critical time', 'Inferența asupra timpului critic'), items(
    (T(r'The point estimate $\hat t_c$ moves with the window and the data; an \textbf{interval} is needed',
       r'Estimația punctuală $\hat t_c$ se mută odată cu fereastra și datele; este nevoie de un \textbf{interval}'), []),
    (T(r'\textbf{Profile likelihood}: for each $t_c$, the other parameters are set to their best values; with Gaussian errors',
       r'\textbf{Verosimilitatea profil}: pentru fiecare $t_c$, ceilalți parametri iau valorile cele mai bune; cu erori gaussiene'),
     [r'\[ \ell(t_c) = -\frac n2\ln\big[\mathrm{SSR}(t_c)/n\big], \qquad \text{' + T('95\\% interval', 'intervalul de 95\\%') + r'}: \{t_c: 2[\ell(\hat t_c) - \ell(t_c)] \le ' + T(r'\chi^2_{1;0.95} = 3.84', r'\chi^2_{1;0{,}95} = 3{,}84') + r'\} \]',
      T(r'$n$: number of days in the window; $\mathrm{SSR}(t_c)$: the smallest sum of squared residuals for this $t_c$', r'$n$: numărul de zile din fereastră; $\mathrm{SSR}(t_c)$: cea mai mică sumă a pătratelor reziduurilor pentru acest $t_c$'),
      T('too narrow when residuals are autocorrelated or when nuisance parameters are many', 'prea îngust cînd reziduurile sînt autocorelate sau parametrii de deranj sînt mulți')]),
    (T(r'\refFDS: the modified profile likelihood (Barndorff-Nielsen) corrects for the nuisance parameters; intervals for $t_c$ become wider and asymmetric',
       r'\refFDS: verosimilitatea profil modificată (Barndorff-Nielsen) corectează pentru parametrii de deranj; intervalele pentru $t_c$ devin mai largi și asimetrice'), []),
    T(r'\refDS ask whether the birth or the burst of a bubble is easier to diagnose: the start time is far better constrained by the data than $t_c$',
      r'\refDS se întreabă dacă nașterea sau spargerea unei bule este mai ușor de diagnosticat: momentul de început este mult mai bine determinat de date decît $t_c$')), 'small')

chart(T('Shanghai 2015: indicator and critical time', 'Shanghai 2015: indicatorul și timpul critic'), 'ats_ch16_lppls', 'ATS_ch16_lppls_inference', [
    T(r'Left: confidence indicator every fifth trading day; right: profile likelihood of $t_c$ for the window from the low of @{lp.low} to @{lp.t2} (@{lp.n} days), as in the real-time analysis of \refSha',
      r'Stînga: indicatorul de încredere în fiecare a cincea zi de tranzacționare; dreapta: verosimilitatea profil a lui $t_c$ pentru fereastra de la minimul din @{lp.low} pînă la @{lp.t2} (@{lp.n} de zile), ca în analiza în timp real din \refSha')],
    h='0.61\\textheight')

interp(('the Shanghai fit', 'ajustării pentru Shanghai'), [
    T(r'The fit ending on @{lp.t2} passes the whole filter: $m = @{lp.m}$, $\omega = @{lp.w}$, @{lp.osc} oscillations, damping @{lp.damp}; $\hat t_c$ = @{lp.tc}',
      r'Ajustarea care se încheie pe @{lp.t2} trece de tot filtrul: $m = @{lp.m}$, $\omega = @{lp.w}$, @{lp.osc} oscilații, amortizare @{lp.damp}; $\hat t_c$ = @{lp.tc}'),
    T(r'Profile-likelihood interval: @{lp.lo} to @{lp.hi} (@{lp.width} days); the peak of @{lp.peak} lies at its left edge: a good call that is fragile to the window',
      r'Intervalul din verosimilitatea profil: @{lp.lo} -- @{lp.hi} (@{lp.width} de zile); maximul din @{lp.peak} se află la marginea lui stîngă: o prognoză bună, dar fragilă la alegerea ferestrei'),
    T(r'The indicator is low: at most @{lp.cimax} (on @{lp.ci_max_date}); few windows qualify at once, so the indicator flags a regime, not a date',
      r'Indicatorul este mic: cel mult @{lp.cimax} (pe @{lp.ci_max_date}); puține ferestre se califică simultan, deci indicatorul semnalează un regim, nu o dată'),
    T('One success is an anecdote: the next section counts alarms over decades, with base rates', 'Un succes este o anecdotă: secțiunea următoare numără alarmele pe decenii, cu frecvențele de bază')])

D.frame(T('Spectral views of log-periodicity and the critique', 'Abordări spectrale ale log-periodicității și critica'), items(
    (T(r'The oscillation $\cos(\omega\ln(t_c - t))$ is periodic in $\ln(t_c - t)$', r'Oscilația $\cos(\omega\ln(t_c - t))$ este periodică în $\ln(t_c - t)$'),
     [T(r'test: the Lomb periodogram of the detrended residual against $\ln(t_c - t)$ \refLom', r'testul: periodograma Lomb a reziduului fără tendință, în funcție de $\ln(t_c - t)$ \refLom'),
      T(r'nonparametric alternative: the $(H, q)$-derivative analysis \refZS', r'alternativa neparametrică: analiza cu derivata $(H, q)$ \refZS'),
      T(r'in calendar time its instantaneous frequency is $\omega/[2\pi(t_c - t)]$: oscillations speed up towards $t_c$; the Hilbert transform of the residual gives this phase directly (Chapter 11 for the tools)',
        r'în timp calendaristic frecvența ei instantanee este $\omega/[2\pi(t_c - t)]$: oscilațiile se accelerează spre $t_c$; transformata Hilbert a reziduului dă direct această fază (instrumentele în Capitolul 11)')]),
    (T('Critique', 'Critica'),
     [T(r'log-periodic peaks appear in noise after fitting and detrending \refFei', r'vîrfurile log-periodice apar și în zgomot după ajustare și eliminarea tendinței \refFei'),
      T(r'out-of-sample crash calls perform poorly \refBJ; estimation is fragile \refGF', r'prognozele de crah în afara eșantionului sînt slabe \refBJ; estimarea este fragilă \refGF'),
      T(r'replies on the stochastic formulation, filters and multi-window indicators: \refSWYZ', r'răspunsuri privind formularea stochastică, filtrele și indicatorii pe multe ferestre: \refSWYZ')]),
    T('A fair comparison with PSY uses the same events, dates and error measures: next section', 'O comparație corectă cu PSY folosește aceleași evenimente, date și măsuri de eroare: secțiunea următoare')), 'small')

D.recap(('LPPLS', 'LPPLS'), [
    T('LPPLS models super-exponential growth with log-periodic oscillations towards a critical time; the confidence indicator aggregates qualified fits over windows',
      'LPPLS modelează creșterea superexponențială cu oscilații log-periodice spre un timp critic; indicatorul de încredere agregă ajustările calificate pe ferestre'),
    T('The critical time needs an interval: profile or modified profile likelihood; the birth of a bubble is easier to pin down than its burst',
      'Timpul critic cere un interval: verosimilitate profil sau profil modificată; nașterea unei bule se determină mai ușor decît spargerea ei'),
    T('Spectral tests of log-periodicity are easy to fool; judge LPPLS by its alarms, not by its fits', 'Testele spectrale ale log-periodicității pot fi păcălite ușor; judecați LPPLS după alarmele lui, nu după ajustări')])

# =============================================================================
# 7. APLICAȚII CU FRECVENȚE DE BAZĂ
# =============================================================================
D.section('Applications with base rates', 'Aplicații cu frecvențe de bază')

D.frame(T('Five episodes, one protocol', 'Cinci episoade, un singur protocol'), two(
    ph('shanghai', T('Shanghai Stock Exchange, Pudong, 2008', 'Bursa din Shanghai, Pudong, 2008'), h='0.4\\textheight'),
    items(T(r'Weekly log prices (Friday close): S\&P 500 and Nasdaq 100 1990--2004, Shanghai Composite 2010--2018, Bitcoin September 2014 -- 2023, BET 2000--2012',
            r'Logaritmul prețurilor săptămînale (închiderea de vineri): S\&P 500 și Nasdaq 100 1990--2004, Shanghai Composite 2010--2018, Bitcoin septembrie 2014 -- 2023, BET 2000--2012'),
          T(r'No lags; $r_0 = 0.01 + 1.8/\sqrt T$; minimum duration $\lceil\ln T\rceil$ weeks; Monte Carlo (@{ep.R} paths) and wild-bootstrap (@{ep.B} draws) critical values',
            r'Fără laguri; $r_0 = 0.01 + 1.8/\sqrt T$; durata minimă $\lceil\ln T\rceil$ săptămîni; valori critice Monte Carlo (@{ep.R} de traiectorii) și wild bootstrap (@{ep.B} de extrageri)'),
          T(r'Episodes dated with pointwise wild values and with the family-wise wild threshold over 52 weeks; the alarm date is the confirmation date',
            r'Episoade datate cu valori wild punctuale și cu pragul wild de familie pe 52 de săptămîni; data alarmei este data confirmării'),
          T(r'Case studies: \refPWY (Nasdaq), \refPSYa (S\&P 500), \refSha (Shanghai), \refGDS (Bitcoin); for the BET 2007 see also the further reading \refPMM',
            r'Studii de caz: \refPWY (Nasdaq), \refPSYa (S\&P 500), \refSha (Shanghai), \refGDS (Bitcoin); pentru BET 2007, vezi și lectura suplimentară \refPMM')), '0.34', '0.64'), 'footnotesize')

chart(T('BSADF of the five episodes', 'BSADF pentru cele cinci episoade'), 'ats_ch16_episodes', 'ATS_ch16_episodes', [
    T(r'Shaded: episodes dated with the pointwise wild bootstrap; dotted vertical lines: price peaks',
      r'Zonele colorate: episoade datate cu wild bootstrap punctual; liniile verticale punctate: maximele prețurilor')],
    h='0.68\\textheight')

D.frame(T('Interpreting the five tests', 'Interpretarea celor cinci teste'), table(
    'lrrrrrr',
    T(r'\textbf{Series}', r'\textbf{Seria}') + r' & $T$ & GSADF & ' + T(r'\textbf{cv MC}', r'\textbf{vc MC}') + ' & ' + T(r'\textbf{cv wild}', r'\textbf{vc wild}') + ' & ' + T(r'\textbf{episodes: MC / wild / FW}', r'\textbf{episoade: MC / wild / FW}') + ' & ' + T(r'\textbf{weeks: MC / wild}', r'\textbf{săptămîni: MC / wild}'),
    [f'{LAB[k]} & @{{ep.{k}.T}} & @{{ep.{k}.g}} & @{{ep.{k}.mc}} & @{{ep.{k}.w}} & @{{ep.{k}.nmc}} / @{{ep.{k}.nw}} / @{{ep.{k}.nfw}} & @{{ep.{k}.wkmc}} / @{{ep.{k}.wkw}}'
     for k in ('sp500', 'ndx', 'ssec', 'btc', 'bet')], size='scriptsize') + items(
    T(r'S\&P 500: GSADF below both critical values, yet pointwise dating marks @{ep.sp500.nw} episodes: the multiplicity trap on real data; no family-wise episode',
      r'S\&P 500: GSADF sub ambele valori critice, totuși datarea punctuală marchează @{ep.sp500.nw} episoade: capcana multiplicității pe date reale; niciun episod de familie'),
    T(r'The wild critical values exceed the Monte Carlo ones for every series (volatility clusters): Bitcoin and BET still reject; the Nasdaq (@{ep.ndx.g} against @{ep.ndx.w}) and Shanghai (@{ep.ssec.g} against @{ep.ssec.w}) do not',
      r'Valorile critice wild depășesc valorile Monte Carlo pentru toate seriile (volatility clustering): Bitcoin și BET resping în continuare; Nasdaq (@{ep.ndx.g} față de @{ep.ndx.w}) și Shanghai (@{ep.ssec.g} față de @{ep.ssec.w}) nu resping'),
    T('MC: Monte Carlo; FW: family-wise wild threshold over 52 weeks; cv: 95\\% critical value of GSADF',
      'MC: Monte Carlo; FW: pragul wild de familie pe 52 de săptămîni; vc: valoarea critică de 95\\% a GSADF')), 'footnotesize')

D.frame(T('Alarms before the peaks', 'Alarmele dinaintea maximelor'), table(
    'lrrrrr',
    T(r'\textbf{Peak}', r'\textbf{Maximul}') + ' & ' + T(r'\textbf{first alarm (2 years before)}', r'\textbf{prima alarmă (2 ani înainte)}') + ' & ' + T(r'\textbf{lead (weeks)}', r'\textbf{avans (săpt.)}') + ' & ' + T(r'\textbf{active at peak}', r'\textbf{activă la maxim}') + ' & ' + T(r'\textbf{FW lead}', r'\textbf{avans FW}') + ' & ' + T(r'\textbf{fall in 1 year}', r'\textbf{scădere în 1 an}'),
    [f'{LAB[k]}, @{{ep.{k}.{j}.peak}} & @{{ep.{k}.{j}.conf}} & @{{ep.{k}.{j}.lead}} & @{{ep.{k}.{j}.act}} & @{{ep.{k}.{j}.flead}} & @{{ep.{k}.{j}.fall}}\\%'
     for k, j in (('sp500', 0), ('ndx', 0), ('ssec', 0), ('btc', 0), ('btc', 1), ('bet', 0))], size='scriptsize') + items(
    T(r'Every major peak is preceded by a pointwise alarm except Bitcoin 2021; leads of half a year to two years: too early to time a crash, informative about the regime',
      r'Fiecare maxim important este precedat de o alarmă punctuală, cu excepția Bitcoin 2021; avansuri între o jumătate de an și doi ani: prea devreme pentru a anticipa un crah, informativ despre regim'),
    T(r'BET 2007: the alarm of @{ep.bet.0.conf} is followed by almost two years of gains before the peak and a fall of @{ep.bet.0.fall}\%; family-wise control removes most alarms',
      r'BET 2007: alarma din @{ep.bet.0.conf} este urmată de aproape doi ani de creșteri pînă la maxim și de o scădere de @{ep.bet.0.fall}\%; controlul de familie elimină majoritatea alarmelor'),
    T('Counting only peaks hides the false alarms: alarms that were not followed by a crash appear only when every date is evaluated',
      'Numărarea doar a maximelor ascunde alarmele false: alarmele care nu au fost urmate de un crah apar doar cînd evaluăm fiecare dată')), 'footnotesize')

chart(T('Early-warning value over decades', 'Valoarea avertizării timpurii pe decenii'), 'ats_ch16_evaluation', 'ATS_ch16_early_warning', [
    T(r'Event: a fall of 20\% within 182 days; evaluation every fifth trading day (S\&P 500 @{ev.sp500.n} dates, Bitcoin @{ev.btc.n}); scores: LPPLS confidence indicator, BSADF minus its pointwise 95\% critical value (weekly, real time), trailing one-year return',
      r'Evenimentul: o scădere de 20\% în 182 de zile; evaluare în fiecare a cincea zi de tranzacționare (S\&P 500 @{ev.sp500.n} de date, Bitcoin @{ev.btc.n}); scoruri: indicatorul de încredere LPPLS, BSADF minus valoarea critică punctuală de 95\% (săptămînal, în timp real), randamentul din ultimul an')],
    h='0.61\\textheight')

interp(('the early-warning evaluation', 'evaluării avertizărilor timpurii'), [
    T(r'Base rates: @{ev.sp500.base}\% of S\&P 500 dates and @{ev.btc.base}\% of Bitcoin dates are followed by a 20\% fall: the same alarm means very different things in the two markets',
      r'Frecvențe de bază: @{ev.sp500.base}\% dintre datele S\&P 500 și @{ev.btc.base}\% dintre datele Bitcoin sînt urmate de o scădere de 20\%: aceeași alarmă înseamnă lucruri foarte diferite pe cele două piețe'),
    T(r'S\&P 500, AUC with 90\% block-bootstrap intervals: indicator @{ev.sp500.ci} [@{ev.sp500.ci.lo}, @{ev.sp500.ci.hi}], BSADF @{ev.sp500.bsadf} [@{ev.sp500.bsadf.lo}, @{ev.sp500.bsadf.hi}], momentum @{ev.sp500.mom} [@{ev.sp500.mom.lo}, @{ev.sp500.mom.hi}]: all below 0.5',
      r'S\&P 500, AUC cu intervale block bootstrap de 90\%: indicatorul @{ev.sp500.ci} [@{ev.sp500.ci.lo}, @{ev.sp500.ci.hi}], BSADF @{ev.sp500.bsadf} [@{ev.sp500.bsadf.lo}, @{ev.sp500.bsadf.hi}], momentum @{ev.sp500.mom} [@{ev.sp500.mom.lo}, @{ev.sp500.mom.hi}]: toate sub 0,5'),
    (T(r'Most S\&P 500 dates followed by a 20\% fall lie inside bear markets (2000--2002, 2008), when exuberance scores are low, and few at the top of a run-up',
       r'Cele mai multe date S\&P 500 urmate de o scădere de 20\% se află în piețe în declin (2000--2002, 2008), cînd scorurile de exuberanță sînt mici, și puține la vîrful unei creșteri'),
     [T(r'so the scores are \textbf{lower} before the events; BSADF alarms have precision @{ev.sp500.bsadf_alarm.prec}\% against a base rate of @{ev.sp500.base}\%', r'deci scorurile sînt \textbf{mai mici} înaintea evenimentelor; alarmele BSADF au precizia @{ev.sp500.bsadf_alarm.prec}\%, față de o frecvență de bază de @{ev.sp500.base}\%')], []),
    (T(r'Bitcoin: BSADF has skill, AUC @{ev.btc.bsadf} [@{ev.btc.bsadf.lo}, @{ev.btc.bsadf.hi}], above momentum @{ev.btc.mom}; its alarms reach precision @{ev.btc.bsadf_alarm.prec}\% against a base rate of @{ev.btc.base}\% (hit rate @{ev.btc.bsadf_alarm.hit}\%, false alarms @{ev.btc.bsadf_alarm.fa}\%)',
       r'Bitcoin: BSADF are putere predictivă, AUC @{ev.btc.bsadf} [@{ev.btc.bsadf.lo}, @{ev.btc.bsadf.hi}], peste momentum @{ev.btc.mom}; alarmele lui ating precizia @{ev.btc.bsadf_alarm.prec}\%, față de o frecvență de bază de @{ev.btc.base}\% (rata de detecție @{ev.btc.bsadf_alarm.hit}\%, alarme false @{ev.btc.bsadf_alarm.fa}\%)'), []),
    (T(r'The LPPLS indicator is positive on @{ev.sp500.cipos}\% of S\&P 500 dates and @{ev.btc.cipos}\% of Bitcoin dates; its AUC is @{ev.sp500.ci} and @{ev.btc.ci}: under this protocol it does not separate pre-crash dates from the rest',
       r'Indicatorul LPPLS este pozitiv în @{ev.sp500.cipos}\% dintre datele S\&P 500 și în @{ev.btc.cipos}\% dintre datele Bitcoin; AUC este @{ev.sp500.ci} și @{ev.btc.ci}: în acest protocol nu separă datele dinaintea crahurilor de celelalte'), [])], size='footnotesize')

D.recap(('the applications', 'aplicațiile'), [
    T('Wild-bootstrap critical values are higher than Monte Carlo ones on real data; some textbook rejections do not survive',
      'Valorile critice wild bootstrap sînt mai mari decît cele Monte Carlo pe date reale; unele respingeri clasice nu rezistă'),
    T('Major peaks are usually preceded by alarms, but with long and variable leads; family-wise control removes most of them',
      'Maximele importante sînt de obicei precedate de alarme, dar cu avansuri lungi și variabile; controlul de familie elimină majoritatea lor'),
    (T('Over decades, precision must be read against the base rate', 'Pe decenii, precizia trebuie citită față de frecvența de bază'),
     [T('exuberance scores help for Bitcoin, where crashes follow run-ups', 'scorurile de exuberanță ajută pentru Bitcoin, unde crahurile urmează creșterilor'),
      T('they fail for the S\\&P 500, where most pre-crash dates lie inside bear markets', 'ele eșuează pentru S\\&P 500, unde majoritatea datelor dinaintea crahurilor se află în piețe în declin')])])

# =============================================================================
# 8. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('The question', 'Întrebarea'),
     [T('do explosive-root and LPPLS alarms carry information about large falls beyond momentum and volatility?', 'conțin alarmele bazate pe rădăcini explozive și pe LPPLS informație despre scăderile mari dincolo de momentum și volatilitate?'),
      T('once base rates, overlapping horizons and the search over assets are accounted for', 'după ce ținem seama de frecvențele de bază, de orizonturile suprapuse și de căutarea pe multe active')]),
    (T('A testable form', 'O formă testabilă'),
     [T(r'formal: in a logit or probit of the event on lagged momentum, volatility and the alarm score, $H_0$: the alarm coefficient is zero, with block-bootstrap inference and a pre-registered panel of assets',
        r'formal: într-un model logit sau probit al evenimentului pe momentum, volatilitate și scorul alarmei (cu lag), $H_0$: coeficientul alarmei este zero, cu inferență block bootstrap și un panel de active preînregistrat'),
      T('falsified by a significant out-of-sample gain in a proper score (log score, Brier) over the momentum-volatility model, pooled across assets',
        'infirmată de un cîștig semnificativ în afara eșantionului într-o regulă de scor proprie (log score, Brier) față de modelul cu momentum și volatilitate, agregat pe active')]),
    (T('Why it matters', 'Miza'),
     [T('regulators and investors read bubble indicators as warnings', 'autoritățile și investitorii citesc indicatorii de bulă ca avertismente'),
      T('most evidence comes from a few famous episodes chosen after the fact', 'majoritatea dovezilor provin din cîteva episoade celebre, alese după ce s-au produs'),
      T(r'literature to start from: \refPS, \refAHLST, \refDS, \refBJ, \refHB', r'literatura de pornire: \refPS, \refAHLST, \refDS, \refBJ, \refHB')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature',
       'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers since 2015 that evaluate bubble detectors out of sample with false-alarm rates; give DOIs.} Then check every DOI and the reported numbers',
        r'\textbf{literatura}: \aiprompt{Listează articole recenzate din 2015 încoace care evaluează detectoarele de bule în afara eșantionului, cu rate ale alarmelor false; dă DOI-urile.} Apoi verificați fiecare DOI și cifrele raportate'),
      T(r'\textbf{hypothesis}: \aiprompt{Write a pre-registration: assets, sample, event definition, scores, baseline model, proper score, test and block length.}',
        r'\textbf{ipoteza}: \aiprompt{Scrie o preînregistrare: activele, eșantionul, definiția evenimentului, scorurile, modelul de referință, regula de scor, testul și lungimea blocurilor.}'),
      T(r'\textbf{code and replication}: ask for a vectorised BSADF; reproduce a known number first (the GSADF of the Nasdaq 100 here, or PSY critical values)',
        r'\textbf{cod și replicare}: cereți un BSADF vectorizat; reproduceți întîi o cifră cunoscută (GSADF pentru Nasdaq 100 de aici sau valorile critice PSY)'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee: list every way this evaluation could overstate the value of the alarms.}',
        r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră toate felurile în care această evaluare ar putea supraestima valoarea alarmelor.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, the title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('Right tail, not left: an AI-written ADF often uses left-tail critical values or the 1.645 normal quantile', 'Coada dreaptă, nu cea stîngă: un ADF scris de un AI folosește adesea valorile critice ale cozii stîngi sau cuantila normală 1,645'),
    T('Critical values simulated for the same $T$, $r_0$, lags and deterministic terms; wild bootstrap when volatility changes', 'Valori critice simulate pentru aceleași $T$, $r_0$, laguri și termeni determiniști; wild bootstrap cînd volatilitatea se schimbă'),
    T('No look-ahead: the minimum window, the lag order and the scaling are fixed from data available at each date', 'Fără informație din viitor: fereastra minimă, numărul de laguri și scalarea se stabilesc din datele disponibile la fiecare dată'),
    T('Multiplicity over dates and over assets: which error rate does a reported bubble control?', 'Multiplicitatea pe date și pe active: ce rată de eroare controlează o bulă raportată?')), 'small')

chart(T('Mini-case: how many bubbles does a screen find?', 'Mini studiu de caz: cîte bule găsește o analiză pe multe active?'), 'ats_ch16_ai_case', 'ATS_ch16_ai_screen', [
    T(r'GSADF on the monthly log price of @{ai.K} series of the course data (from 1990 or the first month), p-values from @{ai.B} wild-bootstrap and @{ai.B} Monte Carlo draws (smallest attainable p-value: @{ai.minp})',
      r'GSADF pe logaritmul prețului lunar pentru @{ai.K} serii din datele cursului (din 1990 sau din prima lună disponibilă), p-value-uri din @{ai.B} de extrageri wild bootstrap și @{ai.B} Monte Carlo (cel mai mic p-value posibil: @{ai.minp})'),
    T(r'Rejections at 5\%: @{ai.mc} with Monte Carlo, @{ai.wild} with the wild bootstrap (@{ai.exp} expected by chance); after Holm @{ai.holm}, after Benjamini--Hochberg @{ai.bh}. An AI summary such as \textquotedblleft bubbles in @{ai.mc} assets\textquotedblright{} is wrong twice: wrong null and no correction',
      r'Respingeri la 5\%: @{ai.mc} cu Monte Carlo, @{ai.wild} cu wild bootstrap (@{ai.exp} așteptate din întîmplare); după Holm @{ai.holm}, după Benjamini--Hochberg @{ai.bh}. Un rezumat AI precum „bule în @{ai.mc} dintre active” greșește de două ori: ipoteză nulă greșită și nicio corecție')],
    h='0.52\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{A pre-registered evaluation of bubble alarms on Central and Eastern European markets}',
       r'\textbf{O evaluare preînregistrată a alarmelor de bulă pe piețele din Europa Centrală și de Est}'),
     [T(r'replicate: the date-stamping of \refPSYa and the wild bootstrap with family-wise control of \refPS on BET, WIG20, BUX, PX and on housing price-to-rent ratios (Eurostat)',
        r'replicați: datarea din \refPSYa și wild bootstrap cu control de familie din \refPS pe BET, WIG20, BUX, PX și pe rapoartele preț/chirie ale locuințelor (Eurostat)'),
      T('extend: compare BSADF, monitoring with a boundary and the LPPLS indicator as predictors of 20\\% falls, against momentum and volatility, with proper scores and block bootstrap',
        'extindeți: comparați BSADF, monitorizarea cu frontieră și indicatorul LPPLS ca predictori ai scăderilor de 20\\%, față de momentum și volatilitate, cu reguli de scor proprii și block bootstrap'),
      T('pre-register: assets, event definition, scores, horizons, tests and the decision rule, before running anything after 1 November 2026',
        'preînregistrați: activele, definiția evenimentului, scorurile, orizonturile, testele și regula de decizie, înainte de orice rulare după 1 noiembrie 2026')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('A rational bubble is an explosive autoregressive component; it cannot be negative or start later, and periodic collapses hide it from whole-sample tests',
      'O bulă rațională este o componentă autoregresivă explozivă; nu poate fi negativă și nu poate apărea ulterior, iar prăbușirile periodice o ascund de testele pe tot eșantionul'),
    T('Explosive roots are learned at an exponential rate with Cauchy limits; mildly explosive asymptotics are invariant and justify the window tests',
      'Rădăcinile explozive se învață cu rată exponențială, cu limite Cauchy; asimptotica ușor explozivă este invariantă și justifică testele pe ferestre'),
    T('Critical values must match the design; the wild bootstrap handles changing volatility; date-stamping needs family-wise control',
      'Valorile critice trebuie să corespundă designului; wild bootstrap tratează volatilitatea variabilă; datarea cere controlul erorii de familie'),
    T('Dated starts are late, alarms are early relative to peaks, and precision depends on the base rate', 'Începuturile datate sînt tîrzii, alarmele sînt timpurii față de maxime, iar precizia depinde de frecvența de bază'),
    T('Test fundamentals as well as prices; judge LPPLS and PSY by the same alarms, events and scores', 'Testați fundamentele, nu doar prețurile; judecați LPPLS și PSY după aceleași alarme, evenimente și scoruri')), 'small')

D.frame(T('Key formulas', 'Formule de reținut'), '{\\renewcommand{\\arraystretch}{1.4}' + table(
    'll',
    T(r'\textbf{Object}', r'\textbf{Obiectul}') + ' & ' + T(r'\textbf{Formula}', r'\textbf{Formula}'),
    [T('Bubble', 'Bula') + r' & $P_t = F_t + B_t$, $\E_t B_{t+1} = (1 + r)B_t$',
     T('Fundamental, random-walk dividends', 'Fundamentul, dividende mers aleator') + r' & $F_t = D_t/r + \mu(1 + r)/r^2$',
     T('Explosive OLS limit', 'Limita OLS explozivă') + r' & $\rho^n(\hat\rho - \rho)/(\rho^2 - 1) \Rightarrow \mathcal C$',
     T('Recursive statistics', 'Statisticile recursive') + r' & $\mathrm{BSADF}_{r_2} = \sup_{r_1}\mathrm{ADF}_{r_1}^{r_2}$, $\mathrm{GSADF} = \sup_{r_2}\mathrm{BSADF}_{r_2}$',
     T('Minimum window', 'Fereastra minimă') + r' & $r_0 = 0.01 + 1.8/\sqrt T$',
     T('Monitoring boundary', 'Frontiera de monitorizare') + r' & $b_t = \sqrt{\tfrac{t - n}{n}\tfrac{t}{n}[a^2 + \ln\tfrac{t}{t - n}]}$, $1 - \Phi(a) + a\varphi(a) = \alpha$',
     T('Precision of an alarm', 'Precizia unei alarme') + r' & $H\pi_0/[H\pi_0 + F(1 - \pi_0)]$',
     T('LPPLS', 'LPPLS') + r' & $\ln p = A + B f + C_1 f\cos(\omega\ln(t_c - t)) + C_2 f\sin(\omega\ln(t_c - t))$, $f = (t_c - t)^m$'],
    size='footnotesize') + '}', 'small')

D.frame(T('Self-assessment (1/2)', 'Autoevaluare (1/2)'), items(
    T(r'Derive $F_t$ when dividends follow $D_t = \mu + D_{t-1} + \varepsilon_t$; what is $F_t$ for $r = 0.04$, $\mu = 0.1$, $D_t = 3$?',
      r'Derivați $F_t$ cînd dividendele urmează $D_t = \mu + D_{t-1} + \varepsilon_t$; cît este $F_t$ pentru $r = 0.04$, $\mu = 0.1$, $D_t = 3$?'),
    T('Why can a rational bubble not start after the first trading day?', 'De ce nu poate o bulă rațională să apară după prima zi de tranzacționare?'),
    T(r'Why does the whole-sample ADF fail against an Evans bubble?', r'De ce eșuează ADF pe tot eșantionul în fața unei bule Evans?'),
    T(r'Why is the limit of $\hat\rho$ for a fixed explosive root Cauchy only with Gaussian errors?', r'De ce este limita lui $\hat\rho$ pentru o rădăcină explozivă fixă Cauchy doar cu erori gaussiene?'),
    T(r'A sample has $T = 400$ weeks. What are $r_0$ and the minimum window?', r'Un eșantion are $T = 400$ de săptămîni. Cît sînt $r_0$ și fereastra minimă?'),
    T('Why is the GSADF critical value larger than the SADF one?', 'De ce este valoarea critică GSADF mai mare decît cea SADF?')), 'small')

D.frame(T('Self-assessment (2/2)', 'Autoevaluare (2/2)'), items(
    T('What does the wild bootstrap keep from the data, and what does it remove?', 'Ce păstrează wild bootstrap din date și ce elimină?'),
    T(r'An alarm has $H = 0.7$ and $F = 0.1$; the base rate is 4\%. What is its precision?', r'O alarmă are $H = 0.7$ și $F = 0.1$; frecvența de bază este 4\%. Cît este precizia ei?'),
    T('Why must the alarm date be the confirmation date and not the dated start?', 'De ce trebuie ca data alarmei să fie data confirmării și nu începutul datat?'),
    T('The price-to-rent ratio is explosive and real rents are explosive too. What do you conclude?', 'Raportul preț/chirie este exploziv, iar chiriile reale sînt și ele explozive. Ce concluzie trageți?'),
    T(r'Why is a profile-likelihood interval for $t_c$ too narrow with autocorrelated residuals?', r'De ce este prea îngust un interval din verosimilitatea profil pentru $t_c$ cu reziduuri autocorelate?'),
    T('A screen of 80 assets finds 20 GSADF rejections at 5\\%. Which two checks come first?', 'O analiză pe 80 de active găsește 20 de respingeri GSADF la 5\\%. Care sînt primele două verificări?')), 'small')

D.frame(T('Self-assessment: answers (1/2)', 'Autoevaluare: răspunsuri (1/2)'), items(
    T(r'$F_t = D_t/r + \mu(1 + r)/r^2 = 75 + 65 = 140$', r'$F_t = D_t/r + \mu(1 + r)/r^2 = 75 + 65 = 140$'),
    T(r'If $B_t = 0$, then $\E_t B_{t+1} = 0$ and $B_{t+1} \ge 0$ (no negative bubbles), so $B_{t+1} = 0$ almost surely; by induction the bubble stays at zero',
      r'Dacă $B_t = 0$, atunci $\E_t B_{t+1} = 0$ și $B_{t+1} \ge 0$ (nu există bule negative), deci $B_{t+1} = 0$ aproape sigur; prin inducție, bula rămîne zero'),
    T('Collapses pair the largest falls with the highest levels and pull the OLS slope down; over the whole sample the series looks I(1) or stationary',
      'Prăbușirile împerechează cele mai mari scăderi cu cele mai mari niveluri și trag panta OLS în jos; pe tot eșantionul seria arată I(1) sau staționară'),
    T(r'$\rho^n(\hat\rho - \rho)/(\rho^2 - 1) \approx X_n/Y_n$ with $X_n$, $Y_n$ dominated by a few shocks: they are normal only if the shocks are normal; no CLT acts inside them',
      r'$\rho^n(\hat\rho - \rho)/(\rho^2 - 1) \approx X_n/Y_n$, cu $X_n$, $Y_n$ dominate de cîteva șocuri: sînt normale doar dacă șocurile sînt normale; nicio teoremă limită centrală nu acționează în interiorul lor'),
    T(r'$r_0 = 0.01 + 1.8/20 = 0.1$; minimum window $\lfloor 0.1 \cdot 400\rfloor = 40$ weeks',
      r'$r_0 = 0.01 + 1.8/20 = 0.1$; fereastra minimă $\lfloor 0.1 \cdot 400\rfloor = 40$ de săptămîni'),
    T('GSADF takes a supremum over more windows (all starts and ends), so under the null its maximum is larger',
      'GSADF ia supremul pe mai multe ferestre (toate începuturile și sfîrșiturile), deci sub ipoteza nulă maximul lui este mai mare')), 'small')

D.frame(T('Self-assessment: answers (2/2)', 'Autoevaluare: răspunsuri (2/2)'), items(
    T('It keeps the volatility pattern $|\\hat e_t|$ (and the short-run dynamics of the null model); random signs remove any explosive or predictable component',
      'Păstrează tiparul volatilității $|\\hat e_t|$ (și dinamica pe termen scurt a modelului nul); semnele aleatoare elimină orice componentă explozivă sau predictibilă'),
    T(r'$0.7 \cdot 0.04/(0.7 \cdot 0.04 + 0.1 \cdot 0.96) = 0.028/0.124 \approx 0.23$', r'$0.7 \cdot 0.04/(0.7 \cdot 0.04 + 0.1 \cdot 0.96) = 0.028/0.124 \approx 0.23$'),
    T('The start is known only after the minimum number of exceedances; using it as the alarm date would use future information',
      'Începutul este cunoscut doar după numărul minim de depășiri; folosirea lui ca dată a alarmei ar folosi informație din viitor'),
    T('No evidence of a bubble from these tests: the fundamental explains the acceleration; one would test whether the ratio explodes beyond what rents imply',
      'Aceste teste nu arată o bulă: fundamentul explică accelerarea; ar trebui testat dacă raportul explodează peste ce implică chiriile'),
    T('Autocorrelated residuals carry less information than $n$ independent errors, and nuisance parameters are ignored: the likelihood is too sharp',
      'Reziduurile autocorelate conțin mai puțină informație decît $n$ erori independente, iar parametrii de deranj sînt ignorați: verosimilitatea este prea ascuțită'),
    T(r'Whether the critical values allow for changing volatility (wild bootstrap); whether the number of rejections survives a multiple-testing correction (4 are expected by chance)',
      r'Dacă valorile critice țin seama de volatilitatea variabilă (wild bootstrap); dacă numărul respingerilor rezistă unei corecții pentru testare multiplă (4 sînt așteptate din întîmplare)')), 'small')

D.frame(T('Further reading and links', 'Lecturi suplimentare și legături'), two(
    ph('bvb', T('The Bucharest Stock Exchange Palace, March 1928', 'Palatul Bursei din București, martie 1928'), h='0.4\\textheight'),
    items((T('Surveys', 'Sinteze'),
           [T(r'\refGur; \refShi; \refKA', r'\refGur; \refShi; \refKA'),
            T(r'bubbles and later returns: \refGSY', r'bulele și randamentele ulterioare: \refGSY')]),
          (T(r'Implementation: the R package \texttt{exuber} \refVPM', r'Implementare: pachetul R \texttt{exuber} \refVPM'),
           [T('our Quantlets reproduce its statistics in Python', 'Quantlet-urile noastre reproduc statisticile lui în Python')]),
          T('Applications to markets, risk and policy: MFM, Chapter 17', 'Aplicații pe piețe, în risc și politici: MFM, Capitolul 17'),
          T(r'Further reading on the Bucharest Stock Exchange: \refPMM', r'Lectură suplimentară despre Bursa de Valori București: \refPMM'),
          T('The course ends here; the project defence is described in Chapter 15', 'Cursul se încheie aici; susținerea proiectelor este descrisă în Capitolul 15')), '0.34', '0.64'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the mildly explosive Cauchy limit', 'Anexă: limita Cauchy în cazul ușor exploziv'), items(
    T(r'$\rho_n = 1 + c/k_n$; $X_n = k_n^{-1/2}\sum_{j=1}^{n}\rho_n^{-(n-j)-1}u_j$, $Y_n = k_n^{-1/2}\sum_{j=1}^{n}\rho_n^{-j}u_j$; weights $\rho_n^{-j} \approx e^{-cj/k_n}$ decay over $O(k_n)$ terms',
      r'$\rho_n = 1 + c/k_n$; $X_n = k_n^{-1/2}\sum_{j=1}^{n}\rho_n^{-(n-j)-1}u_j$, $Y_n = k_n^{-1/2}\sum_{j=1}^{n}\rho_n^{-j}u_j$; ponderile $\rho_n^{-j} \approx e^{-cj/k_n}$ scad pe $O(k_n)$ termeni'),
    T(r'Lindeberg: no single weight dominates, so $(X_n, Y_n) \Rightarrow (X, Y)$, independent $N(0, \sigma^2/2c)$ ($\sum_j\rho_n^{-2j} \approx k_n/2c$); independence because $X_n$ and $Y_n$ load on the two ends of the sample and $k_n = o(n)$',
      r'Lindeberg: nicio pondere nu domină, deci $(X_n, Y_n) \Rightarrow (X, Y)$, independente $N(0, \sigma^2/2c)$ ($\sum_j\rho_n^{-2j} \approx k_n/2c$); independența vine din faptul că $X_n$ și $Y_n$ se sprijină pe cele două capete ale eșantionului și $k_n = o(n)$'),
    T(r'$(k_n\rho_n^n)^{-2}\sum_t y_{t-1}^2 \Rightarrow Y^2/2c$ and $(k_n\rho_n^n)^{-1}\sum_t y_{t-1}u_t \Rightarrow XY$, so $\dfrac{k_n\rho_n^n}{2c}(\hat\rho - \rho_n) \Rightarrow X/Y \sim \mathcal C$ \refPM',
      r'$(k_n\rho_n^n)^{-2}\sum_t y_{t-1}^2 \Rightarrow Y^2/2c$ și $(k_n\rho_n^n)^{-1}\sum_t y_{t-1}u_t \Rightarrow XY$, deci $\dfrac{k_n\rho_n^n}{2c}(\hat\rho - \rho_n) \Rightarrow X/Y \sim \mathcal C$ \refPM'),
    T(r'A ratio of two independent centred normals with equal variances is standard Cauchy: $X/Y = \tan\Theta$ with $\Theta$ uniform on $(-\pi/2, \pi/2)$',
      r'Raportul a două normale centrate independente cu dispersii egale este Cauchy standard: $X/Y = \tan\Theta$, cu $\Theta$ uniform pe $(-\pi/2, \pi/2)$')), 'small')

D.frame(T('Appendix: the monitoring boundary', 'Anexă: frontiera de monitorizare'), items(
    T(r'Under the null, $S_t \approx n^{-1/2}\sigma^{-1}[\sum_{j \le t}\varepsilon_j - (t/n)\sum_{j \le n}\varepsilon_j]$; with $s = (t - n)/n$: $S \Rightarrow Z(s) = W(1 + s) - (1 + s)W(1)$, $\Var Z(s) = s(1 + s)$',
      r'Sub ipoteza nulă, $S_t \approx n^{-1/2}\sigma^{-1}[\sum_{j \le t}\varepsilon_j - (t/n)\sum_{j \le n}\varepsilon_j]$; cu $s = (t - n)/n$: $S \Rightarrow Z(s) = W(1 + s) - (1 + s)W(1)$, $\Var Z(s) = s(1 + s)$'),
    T(r'Time inversion: $Z(s) = s\,B(1 + 1/s)$ for a standard Brownian motion $B$; with $u = 1/s$ the event $Z(s) > \sqrt{s(1 + s)[a^2 + \ln((1 + s)/s)]}$ becomes $B(1 + u) > \sqrt{(1 + u)[a^2 + \ln(1 + u)]}$',
      r'Inversarea timpului: $Z(s) = s\,B(1 + 1/s)$ pentru o mișcare browniană standard $B$; cu $u = 1/s$, evenimentul $Z(s) > \sqrt{s(1 + s)[a^2 + \ln((1 + s)/s)]}$ devine $B(1 + u) > \sqrt{(1 + u)[a^2 + \ln(1 + u)]}$'),
    T(r'Robbins--Siegmund: $\Pr\{B(1 + u) > \sqrt{(1 + u)[a^2 + \ln(1 + u)]}$ for some $u \ge 0\} = 1 - \Phi(a) + a\varphi(a)$; the two-sided version doubles it, the form used by \refCSW',
      r'Robbins--Siegmund: $\Pr\{B(1 + u) > \sqrt{(1 + u)[a^2 + \ln(1 + u)]}$ pentru un $u \ge 0\} = 1 - \Phi(a) + a\varphi(a)$; versiunea bilaterală o dublează, forma folosită de \refCSW'),
    T(r'In $t$: $s(1 + s) = \frac{t - n}{n}\cdot\frac{t}{n}$ and $(1 + s)/s = t/(t - n)$, which gives $b_t$; a finite horizon makes the test conservative',
      r'În $t$: $s(1 + s) = \frac{t - n}{n}\cdot\frac{t}{n}$ și $(1 + s)/s = t/(t - n)$, de unde rezultă $b_t$; un orizont finit face testul conservator')), 'small')

D.references(bib(), per=13)

if __name__ == '__main__':
    finalize(D.write(V))
