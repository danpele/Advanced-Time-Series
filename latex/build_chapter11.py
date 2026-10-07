r"""
build_chapter11.py -- Capitolul 11 (Analiză spectrală și analiză wavelet), EN + RO
=================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_11/ch11_numbers.json (generate_all_charts.py). Nicio cifră nu este
scrisă de mînă (în afara exemplelor teoretice și a constantelor publicate ale nucleelor, citate ca atare).
TSA, Capitolul 12 a predat periodograma, netezirea, testul lui Fisher și coerența de bază; aici: teoria reprezentării
spectrale, teoria estimării (consistență, compromisul deplasare--varianță, lățimea de bandă, multitaper), spectre
multivariate, cauzalitatea în domeniul frecvenței, filtrele trece-bandă și critica lui Hamilton, sincronizarea ciclurilor,
spectre evolutive, wavelets (MODWT, varianță și corelație pe scale, coerența wavelet cu semnificație Monte Carlo).
Ieșire:
  EN/Courses/chapter11_spectral_wavelet_analysis.tex
  RO/Cursuri/capitol11_analiza_spectrala_analiza_wavelet.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_11/generate_all_charts.py
  python3 latex/build_chapter11.py && python3 latex/ats_build.py compile 11
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch11_common import REFS, QLURL, T, V2, day, bib, finalize, load, minus_fix   # noqa: E402


def M(tex):
    """Displayed formula with decimals: decimal comma in RO (the renderer converts only inline math)."""
    return T(tex, re.sub(r'(\d)\.(\d)', r'\1{,}\2', tex))


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(11, 'lecture', refs=REFS)
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
    'cramer': ('ch11_cramer_1951.jpg', C + 'Harald_Cram' + chr(92) + '%C3' + chr(92) + '%A9r.jpg',
               FOTO + ': ' + T('unknown photographer', 'fotograf necunoscut') + ', Svenska Dagbladet (1951); ' + PD + '; Wikimedia Commons'),
    'wiener': ('ch11_wiener.jpg', C + 'Norbert_wiener.jpg', FOTO + ': Konrad Jacobs, MFO; CC BY-SA 2.0 de; Wikimedia Commons'),
    'daub': ('ch11_daubechies_2005.jpg', C + 'Ingrid_Daubechies_(2005)_(cropped).jpg', FOTO + ': ' + T('own work of the uploader', 'lucrarea autorului încărcării') + ' (2005); ' + PD + '; Wikimedia Commons'),
    'prescott': ('ch11_prescott_2015.jpg', C + 'Edward_C_Prescott_2015_(cropped).jpg', FOTO + ': Narodowy Bank Polski (2015); CC BY-SA 2.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


def pv(key, x, d=3):
    """p-value with its relation sign: '= 0.012' or '< 0.0001' (written after $p$)."""
    if x < 10 ** (-d):
        V.raw(key, '$<$ ' + n(10 ** (-d), d))
    else:
        V.raw(key, '= ' + n(x, d))


def pct(key, x, d=0):
    P(key, 100 * x, d)


def quarter(s):
    y, q = s.split('Q')
    return V2(f'{y}Q{q}', f'T{q} {y}')


# =============================================================================
# CIFRE
# =============================================================================
b = N['bands']
LB = {'long (> 32)': 'lo', 'business cycle (6-32)': 'bc', 'short (< 6)': 'sh'}
for k, kk in LB.items():
    pct(f'bd.t.{kk}', b['theory'][k])
    pct(f'bd.s.{kk}', b['sample'][k])
P('bd.peak', b['peak'], 1)
bv = N['biasvar']
V.raw('bv.mmc', str(bv['M_mc']))
P('bv.mth', bv['M_th'], 0)
P('bv.r12', bv['rmse_12'], 2)
P('bv.ropt', bv['rmse_opt'], 2)
P('bv.b12', bv['bias_12'], 2)
P('bv.sd96', bv['sd_96'], 2)
P('bv.peak', bv['peak_period'], 1)
V.raw('bv.reps', str(bv['reps']))
lk = N['leakage']
P('lk.range', lk['range_db'], 0)
for k in ('raw', 'hann', 'mt', 'mta'):
    P(f'lk.{k}', lk[f'bias_{k}'], 1)
V.raw('lk.reps', str(lk['reps']))
mc = N['mtmc']
for k, kk in (('periodogram', 'pg'), ('Daniell, L = 7', 'dn'), ('Parzen, M = 32', 'pz'), ('Welch, segments of 64', 'we'),
              ('multitaper, K = 7', 'mt')):
    P(f'mc.{kk}.b', mc[k]['bias_all'], 1)
    P(f'mc.{kk}.bp', mc[k]['bias_peak'], 1)
    P(f'mc.{kk}.sd', mc[k]['sd'], 1)
for k, kk in (('periodogram', 'pg'), ('Daniell, L = 7', 'dn'), ('multitaper, K = 7', 'mt'), ('adaptive multitaper', 'ma')):
    pct(f'mc.{kk}.cov', mc[k]['cov_all'], 1)
V.raw('mc.reps', str(mc['reps']))
lam = N['dpss']['lam']
P('dp.l6', lam[6], 3)
P('dp.l7', lam[7], 2)
P('dp.l8', lam[8], 2)
ip = N['ipspec']
for g in ('RO', 'EA20'):
    P(f'ip.{g}.sd', ip[g]['sd'], 2)
    pct(f'ip.{g}.bc', ip[g]['share_bc'], 1)
    pct(f'ip.{g}.sh', ip[g]['share_short'], 0)
V.raw('ip.n', str(ip['RO']['n']))
ft = N['ftest']
V.raw('ft.nsa', str(ft['NSA']['n_sig']))
_k = ft['SCA']['n_sig']
V.raw('ft.sca', V2('none of the six harmonics is significant', 'niciuna dintre cele șase armonici nu este semnificativă') if _k == 0 else V2(f'{_k} of the six harmonics are significant', f'{_k} dintre cele șase armonici sînt semnificative'))
pv('ft.td', ft['NSA']['p_td'], 4)
P('ft.tds', ft['SCA']['p_td'], 2)
pv('ft.p2', ft['NSA']['p'][1], 4)
pv('ft.p3', ft['NSA']['p'][2], 4)
P('ft.p1', ft['NSA']['p'][0], 3)
P('ft.p5', ft['NSA']['p'][4], 2)
V.raw('ft.oth', str(ft['NSA']['n_other']))
V.raw('ft.nf', str(ft['NSA']['n_freq']))
co = N['coh']
P('co.thr', co['thr'], 2)
P('co.bc', co['coh_bc'], 2)
P('co.sh', co['coh_short'], 2)
pct('co.sbc', co['share_sig_bc'])
pct('co.ssh', co['share_sig_short'])
P('co.lead', abs(co['lead_med']), 1)
P('co.gbc', co['gain_bc'], 2)
P('co.gsh', co['gain_short'], 2)
P('co.corr', co['corr'], 2)
V.raw('co.K', str(co['K']))
dc = N['dyncorr']
for g in ('RO', 'PL', 'HU', 'CZ'):
    for s in ('pre', 'full'):
        P(f'dc.{g}.{s}.bc', dc[g][s]['bc'], 2)
        P(f'dc.{g}.{s}.sh', dc[g][s]['short'], 2)
        P(f'dc.{g}.{s}.c', dc[g][s]['corr'], 2)
ca = N['caus']
V.raw('ca.p', str(ca['p']))
P('ca.F1', ca['F_ea_ro'], 3)
P('ca.F2', ca['F_ro_ea'], 3)
P('ca.int', ca['int_ea_ro'], 3)
P('ca.bc', ca['M_bc'], 3)
P('ca.sh', ca['M_short'], 3)
P('ca.crit', ca['crit'], 2)
pct('ca.r1', ca['share_rej'])
pct('ca.r2', ca['share_rej2'])
V.raw('ca.r2t', V2('at no frequency', 'la nicio frecvență') if ca['share_rej2'] == 0 else V2(f"at {100 * ca['share_rej2']:.0f}% of them", f"la {100 * ca['share_rej2']:.0f}\\% dintre ele"))
ga = N['gains']
for k in ('hp32', 'hp40', 'hp60', 'bk_peak', 'bk_40', 'ham16', 'ham_e16', 'ham_e8', 'bk_a0'):
    P('ga.' + k.replace('_', ''), ga[k], 2)
P('ga.ham8', ga['ham8'], 2)
hb = ga['ham_b']
P('ga.sumb', sum(hb[1:]), 2)
cn = N['cn']
P('cn.pth', cn['p_th'], 1)
P('cn.pmc', cn['p_mc'], 1)
P('cn.yr', cn['p_th'] / 4, 1)
cy = N['cycles']
KC = {'HP': 'hp', 'Baxter-King': 'bk', 'Christiano-Fitzgerald': 'cf', 'Hamilton': 'ham'}
for k, kk in KC.items():
    P(f'cy.sd.{kk}', cy['sd'][k], 1)
    P(f'cy.last.{kk}', cy['last'][k], 1)
    V.raw(f'cy.lq.{kk}', quarter(cy['last_q'][k]))
    P(f'cy.min.{kk}', cy['min09'][k], 1)
    V.raw(f'cy.mq.{kk}', quarter(cy['minq09'][k]))
    P(f'cy.max.{kk}', cy['max08'][k], 1)
P('cy.c.bkhp', cy['corr']['Baxter-King|HP'], 2)
P('cy.c.hpham', cy['corr']['HP|Hamilton'], 2)
P('cy.c.cfham', cy['corr']['Christiano-Fitzgerald|Hamilton'], 2)
P('cy.c.bkcf', cy['corr']['Baxter-King|Christiano-Fitzgerald'], 2)
V.raw('cy.end', quarter(cy['end']))
ep = N['endpoint']
P('ep.rhp', ep['rms_hp'], 1)
P('ep.rham', ep['rms_ham'], 1)
P('ep.chp', ep['corr_hp'], 2)
P('ep.cham', ep['corr_ham'], 2)
pct('ep.shp', ep['sign_hp'])
pct('ep.sham', ep['sign_ham'])
P('ep.sdhp', ep['sd_hp'], 1)
V.raw('ep.start', quarter(ep['start']))
sy = N['sync']
for k in ('corr', 'c_pre', 'c_gfc', 'c_post', 'c_cov', 'conc', 'conc0'):
    P('sy.' + k.replace('_', ''), sy[k], 2)
V.raw('sy.start', quarter(sy['start']))
V.raw('sy.end', quarter(sy['end']))
P('sy.sdro', sy['sd_ro'], 1)
P('sy.sdea', sy['sd_ea'], 1)
sg = N['spectrogram']
P('sg.res', sg['res'], 3)
mr = N['mra']
for j in range(6):
    pct(f'mr.s{j + 1}', mr['share'][j], 1)
    pct(f'mr.w{j + 1}', 0.5 ** (j + 1), 1)
V.int('mr.n', mr['n'])
wv = N['wvar']
for nm in ('bet', 'dax', 'sp500'):
    P(f'wv.{nm}.r6', wv[nm]['ratio'][5], 2)
    P(f'wv.{nm}.r8', wv[nm]['ratio'][7], 2)
    P(f'wv.{nm}.r3', wv[nm]['ratio'][2], 2)
wc = N['wcorr']
for k in ('bet_dax', 'bet_sp500', 'dax_sp500', 'bet_dax_2000', 'bet_dax_2013'):
    for j in (1, 3, 6, 8):
        P(f'wc.{k}.{j}', wc[k]['r'][j - 1], 2)
for j in (1, 6, 8):
    P(f'wc.beta.{j}', wc['bet_dax']['beta'][j - 1], 2)
P('wc.corr', wc['bet_dax']['corr'], 2)
V.int('wc.n', wc['n'])
cw = N['cwt']
P('cw.ar1', cw['ar1'], 2)
V.raw('cw.date', day(cw['max_date']))
P('cw.per', cw['max_per'], 1)
pct('cw.sig', cw['share_sig'])
V.int('cw.n', cw['n'])
for key, nm in (('wtc_dax', 'wd'), ('wtc_spx', 'ws'), ('wtc_oil', 'wo')):
    w = N[key]
    pct(f'{nm}.obs', w['share_obs'])
    pct(f'{nm}.q95', w['null_q95'], 1)
    for k, v in w.items():
        if k in ('gfc', 'calm', 'early', 'covid', 'war', 'short_all'):
            P(f'{nm}.{k}', v, 2)
            P(f'{nm}.{k}ph', w[k + '_ph'], 2)
    P(f'{nm}.ph', w['phase_sig'], 2)
    V.raw(f'{nm}.reps', str(w['reps']))
for g in ('RO', 'PL'):
    w = N['wtc_infl'][g]
    gg = g.lower()
    pct(f'wi.{gg}.obs', w['share_obs'])
    pct(f'wi.{gg}.q95', w['null_q95'], 1)
    for k in ('post', 'pre', 'surge'):
        P(f'wi.{gg}.{k}', w[k], 2)
        P(f'wi.{gg}.{k}ph', w[k + '_ph'], 2)
    P(f'wi.{gg}.corr', w['corr'], 2)
    P(f'wi.{gg}.ar', w['ax'], 2)
ai = N['ai']
pct('ai.obs', ai['obs'], 1)
pct('ai.mean', ai['mean'], 1)
pct('ai.q95', ai['q95'], 1)
pct('ai.max', ai['max'], 1)
pct('ai.any', ai['any'])
V.raw('ai.reps', str(ai['reps']))
minus_fix(V)

TB = '>{\\raggedright\\arraybackslash}'
BC = T('business-cycle band', 'banda ciclului economic')

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: how is the variance of a time series, and the co-movement of two series, distributed over frequencies, and how does this distribution change over time?',
       r'\textbf{Întrebarea}: cum se distribuie pe frecvențe varianța unei serii de timp și co-mișcarea a două serii și cum se schimbă această distribuție în timp?'),
     [T('cycles of different lengths answer different economic questions: the business cycle, seasonality, the reaction of markets within a week',
        'ciclurile de lungimi diferite răspund unor întrebări economice diferite: ciclul economic, sezonalitatea, reacția piețelor într-o săptămînă')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('the spectral representation; estimation theory: consistency, bandwidth, multitaper',
        'reprezentarea spectrală; teoria estimării: consistență, lățime de bandă, multitaper'),
      T('two series: coherence, phase, dynamic correlation, frequency-domain causality',
        'două serii: coerență, fază, corelație dinamică, cauzalitate în domeniul frecvenței'),
      T('band-pass filters and Hamilton\'s critique of the HP filter; Romania and the euro area',
        'filtre trece-bandă și critica lui Hamilton la adresa filtrului HP; România și zona euro'),
      T('evolutionary spectra; wavelets: MODWT, variance and correlation by scale, wavelet coherence',
        'spectre evolutive; wavelets: MODWT, varianța și corelația pe scale, coerența wavelet')]),
    T('We build on TSA, Chapter 12 (periodogram, smoothing, Fisher\'s test, coherence), Chapter 6 (state space) and Chapter 10 (the spectral pole of long memory); Seminar 11 comes before this lecture',
      'Pornim de la TSA, Capitolul 12 (periodogramă, netezire, testul lui Fisher, coerență), de la Capitolul 6 (spațiul stărilor) și de la Capitolul 10 (polul spectral al memoriei lungi); Seminarul 11 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('State the spectral representation of a stationary process and derive the spectrum of a filtered process',
      'Enunțați reprezentarea spectrală a unui proces staționar și derivați spectrul unui proces filtrat'),
    T('Derive the bias and variance of lag-window estimators, choose the bandwidth, and build multitaper estimates with valid confidence bands',
      'Derivați deplasarea și varianța estimatorilor cu fereastră de laguri, alegeți lățimea de bandă și construiți estimări multitaper cu benzi de încredere valide'),
    T('Estimate and test coherence, phase, gain and dynamic correlation, and test Granger causality at a given frequency',
      'Estimați și testați coerența, faza, cîștigul și corelația dinamică și testați cauzalitatea Granger la o frecvență dată'),
    T('Evaluate trend--cycle filters by their gain, and measure business-cycle synchronisation',
      'Evaluați filtrele de tendință și ciclu prin funcția lor de cîștig și măsurați sincronizarea ciclurilor economice'),
    T('Decompose variance and correlation by scale with the MODWT and test wavelet coherence by Monte Carlo',
      'Descompuneți varianța și corelația pe scale prin MODWT și testați coerența wavelet prin Monte Carlo')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Spectral theory and estimation: \refBD; \refPWa; \refSS; \refTho', r'Teoria și estimarea spectrală: \refBD; \refPWa; \refSS; \refTho'),
     [T(r'Wavelets: \refPWb; \refTC; \refGMJ; \refACS', r'Wavelets: \refPWb; \refTC; \refGMJ; \refACS'),
      T(r'Business cycles: \refBK; \refCF; \refHam; \refCFR', r'Ciclul economic: \refBK; \refCF; \refHam; \refCFR'),
      T(r'Survey of forecasting practice: \refPet', r'Sinteză despre practica prognozei: \refPet')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_11}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_11}'),
     [T(r'spectra, multitaper, cross-spectra, Geweke and Breitung--Candelon, filters, MODWT, Morlet transform and wavelet coherence written in \texttt{numpy}/\texttt{scipy}; \texttt{PyWavelets} gives the wavelet filters',
        r'spectre, multitaper, spectre încrucișate, Geweke și Breitung--Candelon, filtre, MODWT, transformata Morlet și coerența wavelet scrise în \texttt{numpy}/\texttt{scipy}; \texttt{PyWavelets} furnizează filtrele wavelet')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter11_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter11_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{3.6cm}' + TB + 'p{5.0cm}' + TB + 'p{3.4cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Sample}', r'\textbf{Eșantionul}'),
    [T('Real GDP: Romania, euro area, Poland, Hungary, Czechia', 'PIB real: România, zona euro, Polonia, Ungaria, Cehia') + ' & ' + T('Eurostat, chain-linked volumes, seasonally and calendar adjusted, quarterly', 'Eurostat, volume înlănțuite, ajustate sezonier și pentru zilele lucrătoare, trimestrial') + ' & ' + T('1995Q1 -- 2026Q2', 'T1 1995 -- T2 2026'),
     T('Industrial production: Romania, euro area', 'Producția industrială: România, zona euro') + ' & ' + T('Eurostat, monthly, adjusted and unadjusted', 'Eurostat, lunar, ajustată și neajustată') + ' & ' + T('January 2000 -- July 2026', 'ianuarie 2000 -- iulie 2026'),
     T('HICP annual inflation: Romania, Poland, euro area', 'Inflația anuală HICP: România, Polonia, zona euro') + ' & ' + T('Eurostat, monthly', 'Eurostat, lunar') + ' & ' + T('January 2001 -- August 2026', 'ianuarie 2001 -- august 2026'),
     'BET, DAX, S\\&P 500 & ' + T('EODHD daily closes; weekly returns from Friday closes', 'închideri zilnice EODHD; randamente săptămînale din închiderile de vineri') + ' & 2000 -- 2026',
     T('Brent crude oil', 'Petrol Brent') + ' & ' + T('FRED (US Energy Information Administration), daily', 'FRED (US Energy Information Administration), zilnic') + ' & 2000 -- 2026'],
    size='scriptsize') + items(
    T('Growth rates and returns are 100 times log differences; cycles are in \\% of trend; markets are aligned on common trading days',
      'Ratele de creștere și randamentele sînt diferențe logaritmice înmulțite cu 100; ciclurile sînt în \\% din tendință; piețele sînt aliniate pe zilele comune de tranzacționare')), 'footnotesize')

D.frame(T('From harmonic analysis to time series', 'De la analiza armonică la seriile de timp'), two(
    ph('wiener', T('Norbert Wiener', 'Norbert Wiener'), h='0.42\\textheight'),
    items(T('1930: Wiener\'s generalised harmonic analysis; 1934: Khinchin; autocovariance and spectrum are a Fourier pair',
            '1930: analiza armonică generalizată a lui Wiener; 1934: Hincin; autocovarianța și spectrul formează o pereche Fourier'),
          T('1942: Cramér\'s representation of a stationary process as a random superposition of sinusoids',
            '1942: reprezentarea lui Cramér a unui proces staționar ca suprapunere aleatoare de sinusoide'),
          T(r'1961--1966: lag windows \refPar; the typical spectral shape of economic variables \refGra', r'1961--1966: ferestre de laguri \refPar; forma spectrală tipică a variabilelor economice \refGra'),
          T(r'1982: multitaper estimation \refTho; frequency-domain causality \refGew', r'1982: estimarea multitaper \refTho; cauzalitatea în domeniul frecvenței \refGew'),
          T(r'1984--1989: wavelets \refGM, \refDau, \refMal; 1998: the practical guide \refTC', r'1984--1989: wavelets \refGM, \refDau, \refMal; 1998: ghidul practic \refTC')), '0.32', '0.66'), 'footnotesize')

D.frame(T('Known from TSA and new here', 'Cunoscut din TSA și elemente noi'), items(
    (T('Known (TSA, Chapter 12): Fourier frequencies, the spectrum of ARMA models, the periodogram and its $\\chi^2_2$ law, Daniell smoothing, tapering, Fisher\'s test, a first look at coherence and wavelets',
       'Cunoscut (TSA, Capitolul 12): frecvențele Fourier, spectrul modelelor ARMA, periodograma și legea ei $\\chi^2_2$, netezirea Daniell, ponderarea datelor (taper), testul lui Fisher, o primă privire asupra coerenței și a wavelets'), []),
    (T('New: the research toolkit', 'Nou: instrumentele de cercetare'),
     [T('asymptotic theory of spectral estimators: bias, variance, optimal bandwidth, valid confidence bands, multitaper',
        'teoria asimptotică a estimatorilor spectrali: deplasare, varianță, lățime de bandă optimă, benzi de încredere valide, multitaper'),
      T('inference on co-movement: coherence thresholds, phase errors, dynamic correlation, causality by frequency',
        'inferență asupra co-mișcării: praguri pentru coerență, erorile fazei, corelația dinamică, cauzalitatea pe frecvențe'),
      T('filters judged by their gain; time--frequency analysis with significance tests that control false discoveries',
        'filtre judecate după cîștig; analiză timp--frecvență cu teste de semnificație care controlează descoperirile false')]),
    (T('Case studies, with the specifications of the papers, on our data', 'Studii de caz, cu specificațiile din lucrări, pe datele noastre'),
     [T(r'spectral: \refTho; \refCFR; \refBC', r'spectrale: \refTho; \refCFR; \refBC'),
      T(r'filters and wavelets: \refBK; \refCN; \refHam; \refTC; \refGMJ', r'filtre și wavelets: \refBK; \refCN; \refHam; \refTC; \refGMJ')])), 'small')

# =============================================================================
# 1. REPREZENTAREA SPECTRALĂ
# =============================================================================
D.section('The spectral representation', 'Reprezentarea spectrală')

D.frame(T('Autocovariance and spectral distribution (1/2)', 'Autocovarianța și distribuția spectrală (1/2)'), items(
    (T(r'\textbf{Herglotz} \refBD: $\gamma(\cdot)$ is the autocovariance of a stationary process if and only if', r'\textbf{Herglotz} \refBD: $\gamma(\cdot)$ este autocovarianța unui proces staționar dacă și numai dacă'
       ) + r'''
    \[ \gamma(h) = \int_{(-\pi, \pi]} e^{i\omega h}\,dF(\omega) \]''',
     [T(r'$\gamma(h) = \Cov(X_{t+h}, X_t)$; $\omega$: angular frequency in radians per period; $F$: the \textbf{spectral distribution}, non-decreasing, right-continuous and bounded',
        r'$\gamma(h) = \Cov(X_{t+h}, X_t)$; $\omega$: frecvența unghiulară, în radiani pe perioadă; $F$: \textbf{distribuția spectrală}, nedescrescătoare, continuă la dreapta și mărginită')]),
    (T(r'If $\sum_h|\gamma(h)| < \infty$, $F$ has a density, the \textbf{spectral density}', r'Dacă $\sum_h|\gamma(h)| < \infty$, $F$ are o densitate, \textbf{densitatea spectrală}'
       ) + r'''
    \[ dF(\omega) = f(\omega)\,d\omega, \qquad f(\omega) = \frac{1}{2\pi}\sum_h\gamma(h)e^{-i\omega h} \]''',
     [])), 'small')

D.frame(T('Autocovariance and spectral distribution (2/2)', 'Autocovarianța și distribuția spectrală (2/2)'), items(
    (T(r'At $h = 0$: the spectrum is a \textbf{decomposition of variance by frequency}', r'Pentru $h = 0$: spectrul este o \textbf{descompunere a varianței pe frecvențe}'
       ) + r'''
    \[ \gamma(0) = \Var(X_t) = \int_{-\pi}^{\pi}f(\omega)\,d\omega \]''',
     [T(r'$f(\omega)\,d\omega$: the variance contributed by cycles with frequency near $\omega$; period $2\pi/\omega$',
        r'$f(\omega)\,d\omega$: varianța adusă de ciclurile cu frecvența apropiată de $\omega$; perioada $2\pi/\omega$'),
      T(r'quarterly data: the business-cycle band of 6--32 quarters is $\omega \in [\pi/16, \pi/3]$', r'date trimestriale: banda ciclului economic de 6--32 de trimestre este $\omega \in [\pi/16, \pi/3]$')]),
    T(r'A jump of $F$ at $\pm\omega_0$ is a deterministic cycle (a \textbf{line spectrum}); long memory is a pole of $f$ at $\omega = 0$ (Chapter 10)',
      r'Un salt al lui $F$ în $\pm\omega_0$ este un ciclu determinist (un \textbf{spectru de linii}); memoria lungă este un pol al lui $f$ în $\omega = 0$ (Capitolul 10)')), 'small')

D.frame(T('Cramér\'s representation', 'Reprezentarea lui Cramér'), two(
    ph('cramer', T('Harald Cramér, 1951', 'Harald Cramér, 1951'), h='0.4\\textheight'),
    items((T(r'Every zero-mean stationary process is a sum of sinusoids with random amplitudes \refBD', r'Orice proces staționar de medie zero este o sumă de sinusoide cu amplitudini aleatoare \refBD'
             ) + r'''
    \[ X_t = \int_{(-\pi, \pi]} e^{i\omega t}\,dZ(\omega) \]''',
           [T(r'$dZ(\omega)$: the random amplitude at frequency $\omega$; $Z$ has \textbf{orthogonal increments}: $\E[dZ(\omega)\overline{dZ(\lambda)}] = 0$ for $\omega \ne \lambda$, $\E|dZ(\omega)|^2 = dF(\omega)$',
              r'$dZ(\omega)$: amplitudinea aleatoare la frecvența $\omega$; $Z$ are \textbf{creșteri ortogonale}: $\E[dZ(\omega)\overline{dZ(\lambda)}] = 0$ pentru $\omega \ne \lambda$, $\E|dZ(\omega)|^2 = dF(\omega)$')]),
          T('Random amplitudes at different frequencies are uncorrelated: the frequency components can be studied one by one',
            'Amplitudinile aleatoare de la frecvențe diferite sînt necorelate: componentele de frecvență se pot studia separat'),
          (T(r'The discrete Fourier transform (DFT) at the Fourier frequencies $\omega_j = 2\pi j/n$',
             r'Transformata Fourier discretă (DFT) în frecvențele Fourier $\omega_j = 2\pi j/n$') + r'''
    \[ d(\omega_j) = n^{-1/2}\sum_{t=1}^n x_te^{-i\omega_jt} \]''',
           [T(r'the sample analogue of $dZ(\omega_j)$: nearly uncorrelated across Fourier frequencies',
              r'analogul de eșantion al lui $dZ(\omega_j)$: aproape necorelată între frecvențele Fourier')])), '0.32', '0.66'), 'small')

D.frame(T('Linear filters in the frequency domain', 'Filtre liniare în domeniul frecvenței'), items(
    (T(r'A linear filter multiplies each frequency component by the \textbf{transfer function} $A(\omega)$', r'Un filtru liniar înmulțește fiecare componentă de frecvență cu \textbf{funcția de transfer} $A(\omega)$'
       ) + r'''
    \[ Y_t = \sum_j a_jX_{t-j} \ \Rightarrow\ dZ_Y(\omega) = A(\omega)\,dZ_X(\omega), \quad A(\omega) = \sum_j a_je^{-i\omega j} \]
    \[ f_Y(\omega) = |A(\omega)|^2f_X(\omega) \]''',
     [T(r'$a_j$: filter weights, $\sum_j|a_j| < \infty$; $|A(\omega)|$: the \textbf{gain}; $\arg A(\omega)$: the \textbf{phase shift}', r'$a_j$: ponderile filtrului, $\sum_j|a_j| < \infty$; $|A(\omega)|$: \textbf{cîștigul}; $\arg A(\omega)$: \textbf{defazajul}'),
      T(r'symmetric weights $a_j = a_{-j}$: $A(\omega)$ is real, no phase shift; the property every trend--cycle filter wants', r'ponderi simetrice $a_j = a_{-j}$: $A(\omega)$ este real, fără defazaj; proprietatea dorită de orice filtru de tendință și ciclu')]),
    (T(r'First difference: $|1 - e^{-i\omega}|^2 = 2(1 - \cos\omega)$, zero at $\omega = 0$', r'Prima diferență: $|1 - e^{-i\omega}|^2 = 2(1 - \cos\omega)$, nulă în $\omega = 0$'),
     [T(r'differencing removes the long cycles and amplifies the short ones', r'diferențierea elimină ciclurile lungi și le amplifică pe cele scurte')]),
    T(r'Slutsky effect: a moving sum of white noise has a peak in its spectrum, i.e.\ \textbf{cycles created by the filter}; the HP critique of Section 4 is the same phenomenon',
      r'Efectul Slutsky: o sumă mobilă a unui zgomot alb are un vîrf în spectru, adică \textbf{cicluri create de filtru}; critica filtrului HP din secțiunea 4 este același fenomen')), 'small')

D.frame(T('The spectral density matrix (1/2)', 'Matricea densităților spectrale (1/2)'), items(
    (T(r'Vector process $\mathbf X_t$ of dimension $k$: the Fourier transform of the autocovariance matrices', r'Proces vectorial $\mathbf X_t$ de dimensiune $k$: transformata Fourier a matricelor de autocovarianță'
       ) + r'''
    \[ \mathbf f(\omega) = \frac{1}{2\pi}\sum_h\Gamma(h)e^{-i\omega h}, \qquad \Gamma(h) = \Cov(\mathbf X_{t+h}, \mathbf X_t) \]''',
     [T(r'$\mathbf f(\omega)$: a $k \times k$ Hermitian ($\mathbf f = \mathbf f^*$, the conjugate transpose) non-negative definite matrix at each frequency',
        r'$\mathbf f(\omega)$: o matrice $k \times k$ hermitică ($\mathbf f = \mathbf f^*$, transpusa conjugată) și nenegativ definită la fiecare frecvență')]),
    (T(r'VARMA $\Phi(L)\mathbf X_t = \Theta(L)\boldsymbol\varepsilon_t$: the multivariate analogue of the ARMA spectrum', r'VARMA $\Phi(L)\mathbf X_t = \Theta(L)\boldsymbol\varepsilon_t$: analogul multivariat al spectrului ARMA'
       ) + r'''
    \[ \mathbf f(\omega) = \frac{1}{2\pi}\Phi(e^{-i\omega})^{-1}\Theta(e^{-i\omega})\,\bSigma\,\Theta(e^{-i\omega})^*\Phi(e^{-i\omega})^{-*} \]''',
     [T(r'$\Phi$, $\Theta$: matrix AR and MA polynomials; $\bSigma$: covariance of the innovations $\boldsymbol\varepsilon_t$; $^{-*}$: inverse of the conjugate transpose',
        r'$\Phi$, $\Theta$: polinoamele matriceale AR și MA; $\bSigma$: covarianța inovațiilor $\boldsymbol\varepsilon_t$; $^{-*}$: inversa transpusei conjugate')])), 'small')

D.frame(T('The spectral density matrix (2/2): cross-spectra', 'Matricea densităților spectrale (2/2): spectrele încrucișate'), items(
    (T(r'Off-diagonal elements: the \textbf{cross-spectrum}, complex-valued', r'Elementele din afara diagonalei: \textbf{spectrul încrucișat}, cu valori complexe'
       ) + r'''
    \[ f_{xy}(\omega) = c_{xy}(\omega) - i\,q_{xy}(\omega) \]''',
     [T(r'$c_{xy}$: co-spectrum, even in $\omega$ (contemporaneous co-movement), $\int c_{xy} = \Cov(X_t, Y_t)$', r'$c_{xy}$: cospectrul, par în $\omega$ (co-mișcare simultană), $\int c_{xy} = \Cov(X_t, Y_t)$'),
      T(r'$q_{xy}$: quadrature spectrum, odd in $\omega$ (lead--lag between the series)', r'$q_{xy}$: spectrul în cuadratură, impar în $\omega$ (avans--întîrziere între serii)')]),
    T('Section 2 estimates the diagonal, Section 3 the off-diagonal, Section 4 factorises $\\mathbf f$ to measure causality',
      'Secțiunea 2 estimează diagonala, secțiunea 3 elementele din afara diagonalei, iar secțiunea 4 factorizează $\\mathbf f$ pentru a măsura cauzalitatea')), 'small')

chart(T('Variance by frequency band', 'Varianța pe benzi de frecvență'), 'ats_ch11_bands', 'ATS_ch11_spectral_estimation', [
    T(r'An AR(2) path, $X_t = 1.3X_{t-1} - 0.7X_{t-2} + \varepsilon_t$, 240 ``quarters\'\', split by the DFT into three bands; shares of variance in the sample and $2\int_{\mathrm{band}}f/\gamma(0)$ in theory',
      r'O traiectorie AR(2), $X_t = 1.3X_{t-1} - 0.7X_{t-2} + \varepsilon_t$, 240 de „trimestre”, separată prin DFT în trei benzi; ponderile varianței în eșantion și $2\int_{\mathrm{banda}}f/\gamma(0)$ în teorie')],
    h='0.52\\textheight')

interp(('the band decomposition', 'descompunerii pe benzi'), [
    T(r'The spectral peak is at a period of @{bd.peak}: @{bd.t.bc}\% of the variance lies in the band of 6--32 periods (sample: @{bd.s.bc}\%)',
      r'Vîrful spectral se află la perioada @{bd.peak}: @{bd.t.bc}\% din varianță se află în banda de 6--32 de perioade (în eșantion: @{bd.s.bc}\%)'),
    T(r'Long and short cycles carry @{bd.t.lo}\% and @{bd.t.sh}\% in theory: the three components are uncorrelated by Cramér\'s theorem, so the shares add up',
      r'Ciclurile lungi și cele scurte au @{bd.t.lo}\% și @{bd.t.sh}\% în teorie: cele trei componente sînt necorelate conform teoremei lui Cramér, deci ponderile se adună'),
    T('The ``business cycle\'\' of an AR(2) is a stochastic pseudo-cycle: irregular amplitude and length, no line in the spectrum',
      '„Ciclul economic” al unui AR(2) este un pseudo-ciclu stochastic: amplitudine și lungime neregulate, fără linie în spectru'),
    T('Band-pass filters (Section 4) estimate exactly this middle component from a finite sample',
      'Filtrele trece-bandă (secțiunea 4) estimează exact această componentă din mijloc pe un eșantion finit')])

D.recap(('The spectral representation', 'reprezentarea spectrală'), [
    T('The spectrum decomposes variance by frequency; Cramér: uncorrelated random amplitudes at each frequency', 'Spectrul descompune varianța pe frecvențe; Cramér: amplitudini aleatoare necorelate la fiecare frecvență'),
    T('A linear filter multiplies the spectrum by its squared gain; symmetric filters do not shift phase', 'Un filtru liniar înmulțește spectrul cu pătratul cîștigului; filtrele simetrice nu defazează'),
    T('The spectral matrix contains cross-spectra: co-movement and lead--lag by frequency', 'Matricea spectrală conține spectrele încrucișate: co-mișcarea și relațiile de avans--întîrziere pe frecvențe')])

# =============================================================================
# 2. TEORIA ESTIMĂRII
# =============================================================================
D.section('Spectral estimation theory', 'Teoria estimării spectrale')

D.frame(T('Why the periodogram is not enough', 'Limitele periodogramei'), items(
    (T(r'For a linear process the periodogram ordinates are asymptotically scaled $\chi^2_2$ variables \refBD', r'Pentru un proces liniar, ordonatele periodogramei sînt asimptotic variabile $\chi^2_2$ scalate \refBD'
       ) + r'''
    \[ X_t = \sum_j\psi_j\varepsilon_{t-j} \ \Rightarrow\ I(\omega_j) \Rightarrow f(\omega_j)\,\frac{\chi^2_2}{2} \]''',
     [T(r'$\psi_j$: weights with $\sum_j|j|^{1/2}|\psi_j| < \infty$; $\varepsilon_t$: i.i.d. innovations; $f > 0$; asymptotically independent over fixed Fourier frequencies $\omega_j$',
        r'$\psi_j$: ponderi cu $\sum_j|j|^{1/2}|\psi_j| < \infty$; $\varepsilon_t$: inovații i.i.d.; $f > 0$; asimptotic independente pe frecvențe Fourier $\omega_j$ fixate'),
      T(r'$\E I(\omega_j) \to f(\omega_j)$ but $\Var I(\omega_j) \to f(\omega_j)^2$: \textbf{inconsistent}, the variance does not fall with $n$', r'$\E I(\omega_j) \to f(\omega_j)$, dar $\Var I(\omega_j) \to f(\omega_j)^2$: \textbf{inconsistentă}, varianța nu scade cu $n$'),
      T('derivation for white noise and for a linear process: Appendix  % applink: the distribution of the periodogram', 'derivarea pentru zgomot alb și pentru un proces liniar: Anexa  % applink: distribuția periodogramei')]),
    (T(r'Leakage: the mean periodogram is the true spectrum smoothed by the Fejér kernel $F_n$', r'Leakage-ul spectral: media periodogramei este spectrul adevărat netezit cu nucleul Fejér $F_n$'
       ) + r'''
    \[ \E I(\omega) = \int F_n(\omega - \lambda)f(\lambda)\,d\lambda \]''',
     [T(r'the side lobes of $F_n$ decay only like $1/(n\omega^2)$, so power \textbf{leaks} from strong to weak frequencies', r'lobii laterali ai lui $F_n$ scad doar ca $1/(n\omega^2)$, deci puterea se \textbf{scurge} de la frecvențele puternice spre cele slabe')]),
    T(r'Two remedies: \textbf{average} neighbouring frequencies (consistency) and \textbf{taper} the data (bias); multitaper does both',
      r'Două remedii: \textbf{medierea} frecvențelor vecine (consistență) și \textbf{ponderarea} datelor cu un taper (deplasare); estimatorul multitaper le face pe amîndouă')), 'small')

D.frame(T('Lag-window estimators (1/2)', 'Estimatori cu fereastră de laguri (1/2)'), items(
    (T(r'Down-weight the noisy sample autocovariances at long lags \refPar', r'Se reduc ponderile autocovarianțelor de eșantion zgomotoase de la laguri mari \refPar'
       ) + r'''
    \[ \hat f(\omega) = \frac{1}{2\pi}\sum_{|h| < n}k(h/M)\,\hat\gamma(h)e^{-i\omega h} \]''',
     [T(r'$\hat\gamma(h)$: sample autocovariance; $k$: the \textbf{lag window}, $k(0) = 1$, decreasing in $|u|$; $M$: the truncation (bandwidth) parameter',
        r'$\hat\gamma(h)$: autocovarianța de eșantion; $k$: \textbf{fereastra de laguri}, $k(0) = 1$, descrescătoare în $|u|$; $M$: parametrul de trunchiere (lățimea de bandă)')]),
    (T(r'Equivalently: a weighted average of the periodogram with the \textbf{spectral window} $W_M$', r'Echivalent: o medie ponderată a periodogramei cu \textbf{fereastra spectrală} $W_M$'
       ) + r'''
    \[ \hat f(\omega) = \int W_M(\omega - \lambda)I(\lambda)\,d\lambda, \qquad W_M(\omega) = \frac{1}{2\pi}\sum_h k(h/M)e^{-i\omega h} \]''',
     [T(r'a large $M$ gives a narrow $W_M$: little smoothing', r'un $M$ mare dă o fereastră $W_M$ îngustă: netezire redusă')])), 'small')

D.frame(T('Lag-window estimators (2/2): the kernels', 'Estimatori cu fereastră de laguri (2/2): nucleele'), items(
    (T(r'Bartlett $k(u) = 1 - |u|$; Parzen; Tukey--Hanning; quadratic spectral (QS): the same kernels as the HAC estimators of Chapter 0 at $\omega = 0$',
       r'Bartlett $k(u) = 1 - |u|$; Parzen; Tukey--Hanning; pătratic spectral (QS): aceleași nuclee ca estimatorii HAC din Capitolul 0 în $\omega = 0$'),
     [T(r'a non-negative $W_M$ guarantees $\hat f \ge 0$ (Bartlett, Parzen, QS); Tukey--Hanning can go negative',
        r'un $W_M$ nenegativ garantează $\hat f \ge 0$ (Bartlett, Parzen, QS); Tukey--Hanning poate deveni negativ')]),
    (T(r'Characteristic exponent $q$: how flat the kernel is at zero', r'Exponentul caracteristic $q$: cît de plat este nucleul în zero'
       ) + r'''
    \[ k_q = \lim_{u \to 0}\frac{1 - k(u)}{|u|^q} \]''',
     [T(r'Bartlett $q = 1$, $k_1 = 1$; Parzen $q = 2$, $k_2 = 6$; QS $q = 2$, $k_2 = 1.42$; a larger $q$ means smaller bias (next slides)',
        r'Bartlett $q = 1$, $k_1 = 1$; Parzen $q = 2$, $k_2 = 6$; QS $q = 2$, $k_2 = 1.42$; un $q$ mai mare înseamnă deplasare mai mică (slide-urile următoare)')])), 'small')

chart(T('Lag windows and spectral windows', 'Ferestre de laguri și ferestre spectrale'), 'ats_ch11_kernels', 'ATS_ch11_spectral_estimation', [
    T(r'Left: $k(u)$; right: the spectral window $W_M(\omega)$ for $M = 10$, the weights that each estimator gives to the periodogram around $\omega$',
      r'Stînga: $k(u)$; dreapta: fereastra spectrală $W_M(\omega)$ pentru $M = 10$, ponderile pe care fiecare estimator le dă periodogramei în jurul lui $\omega$')],
    h='0.5\\textheight')

interp(('the windows', 'ferestrelor'), [
    (T(r'A narrow $W_M$ means low bias and high variance', r'O fereastră $W_M$ îngustă înseamnă deplasare mică și varianță mare'),
     [T(r'at $M = 10$, Parzen is the widest (its $\int k^2 = 0.54$ is the smallest) and QS the narrowest',
        r'la $M = 10$, Parzen este cea mai largă ($\int k^2 = 0{,}54$ este cel mai mic), iar QS cea mai îngustă')]),
    T('Bartlett has side lobes (leakage through the window itself); Tukey--Hanning has negative weights',
      'Bartlett are lobi laterali (leakage prin fereastra însăși); Tukey--Hanning are ponderi negative'),
    T('Comparing kernels at the same $M$ is misleading: compare them at the same variance (the same equivalent degrees of freedom)',
      'Compararea nucleelor la același $M$ este înșelătoare: comparați-le la aceeași varianță (același număr echivalent de grade de libertate)'),
    T('The QS kernel is optimal in MSE among kernels with non-negative estimates \\refAnd',
      'Nucleul QS este optim în MSE printre nucleele cu estimări nenegative \\refAnd')])

D.frame(T('Bias, variance and the optimal bandwidth (1/2)', 'Deplasare, varianță și lățimea de bandă optimă (1/2)'), items(
    (T(r'If $M \to \infty$ and $M/n \to 0$: $\hat f(\omega) \to_p f(\omega)$ (\textbf{consistency}) \refPar; variance and bias', r'Dacă $M \to \infty$ și $M/n \to 0$: $\hat f(\omega) \to_p f(\omega)$ (\textbf{consistență}) \refPar; varianța și deplasarea'
       ) + r'''
    \[ \Var\hat f(\omega) \approx \frac{M}{n}f(\omega)^2\int k^2(u)\,du, \qquad \E\hat f(\omega) - f(\omega) \approx -k_qM^{-q}f^{(q)}(\omega) \]''',
     [T(r'the variance grows with $M$ (doubled at $\omega = 0, \pm\pi$); the bias falls with $M$', r'varianța crește cu $M$ (se dublează în $\omega = 0, \pm\pi$); deplasarea scade cu $M$'),
      T(r'$f^{(q)}(\omega) = \frac{1}{2\pi}\sum_h|h|^q\gamma(h)e^{-i\omega h}$: a generalised $q$-th derivative of $f$, large where the spectrum is curved (peaks)',
        r'$f^{(q)}(\omega) = \frac{1}{2\pi}\sum_h|h|^q\gamma(h)e^{-i\omega h}$: o derivată generalizată de ordinul $q$ a lui $f$, mare unde spectrul este curbat (vîrfuri)')])), 'small')

D.frame(T('Bias, variance and the optimal bandwidth (2/2)', 'Deplasare, varianță și lățimea de bandă optimă (2/2)'), items(
    (T(r'Minimising MSE = squared bias + variance over $M$', r'Minimizarea MSE = pătratul deplasării + varianța, în raport cu $M$'
       ) + r'''
    \[ M^* = \Big(\frac{qk_q^2f^{(q)}(\omega)^2\,n}{f(\omega)^2\int k^2}\Big)^{1/(2q+1)} \propto n^{1/(2q+1)}, \qquad \mathrm{MSE} \propto n^{-2q/(2q+1)} \]''',
     [T(r'$q = 2$ kernels converge faster ($n^{-4/5}$) than Bartlett ($n^{-2/3}$)', r'nucleele cu $q = 2$ converg mai repede ($n^{-4/5}$) decît Bartlett ($n^{-2/3}$)')]),
    (T(r'Inference: a scaled $\chi^2$ with equivalent degrees of freedom $\nu$', r'Inferența: o variabilă $\chi^2$ scalată, cu $\nu$ grade de libertate echivalente'
       ) + r'''
    \[ \frac{\nu\hat f(\omega)}{f(\omega)} \approx \chi^2_\nu, \qquad \nu = \frac{2n}{M\int k^2} \]''',
     [T(r'the confidence band $[\nu\hat f/\chi^2_{\nu,0.975}, \nu\hat f/\chi^2_{\nu,0.025}]$ has constant width in log scale', r'banda de încredere $[\nu\hat f/\chi^2_{\nu;0,975}, \nu\hat f/\chi^2_{\nu;0,025}]$ are lățime constantă pe scară logaritmică')])), 'small')

chart(T('The bias--variance trade-off at a spectral peak', 'Compromisul deplasare--varianță într-un vîrf spectral'), 'ats_ch11_bias_variance', 'ATS_ch11_spectral_estimation', [
    T(r'Parzen estimator at the peak (period @{bv.peak}) of $X_t = 1.6X_{t-1} - 0.9X_{t-2} + \varepsilon_t$, $n = 512$, @{bv.reps} simulations; curves divided by $f(\mathrm{peak})^2$; dashed: the asymptotic formulas',
      r'Estimatorul Parzen în vîrful (perioada @{bv.peak}) lui $X_t = 1.6X_{t-1} - 0.9X_{t-2} + \varepsilon_t$, $n = 512$, @{bv.reps} de simulări; curbele sînt împărțite la $f(\text{vîrf})^2$; linii întrerupte: formulele asimptotice')],
    h='0.5\\textheight')

interp(('the trade-off', 'compromisului'), [
    T(r'With $M = 12$ the relative RMSE is @{bv.r12}, almost all of it bias (@{bv.b12}): heavy smoothing flattens the peak',
      r'Cu $M = 12$, RMSE relativ este @{bv.r12}, aproape în întregime deplasare (@{bv.b12}): o netezire puternică aplatizează vîrful'),
    T(r'The Monte Carlo optimum is $M = @{bv.mmc}$ (relative RMSE @{bv.ropt}); the asymptotic formula gives $M^* = @{bv.mth}$: same order, but the formula ignores higher-order bias terms',
      r'Optimul Monte Carlo este $M = @{bv.mmc}$ (RMSE relativ @{bv.ropt}); formula asimptotică dă $M^* = @{bv.mth}$: același ordin de mărime, dar formula ignoră termenii de deplasare de ordin superior'),
    T('The asymptotic variance is accurate only once the window is narrower than the peak; the asymptotic bias explodes for small $M$',
      'Varianța asimptotică este precisă doar cînd fereastra este mai îngustă decît vîrful; deplasarea asimptotică explodează pentru $M$ mic'),
    T('A sharp spectral peak needs a much larger $M$ than the HAC rule for $\\omega = 0$ would suggest: bandwidth is local',
      'Un vîrf spectral ascuțit cere un $M$ mult mai mare decît ar sugera regula HAC pentru $\\omega = 0$: lățimea de bandă este locală')])

D.frame(T('Choosing the bandwidth', 'Alegerea lățimii de bandă'), items(
    (T(r'\textbf{Plug-in} \refAnd: approximate $f^{(q)}/f$ by a parametric (AR(1)) model, then use $M^*$', r'\textbf{Plug-in} \refAnd: aproximăm $f^{(q)}/f$ printr-un model parametric (AR(1)), apoi folosim $M^*$'
       ) + M(r'''
    \[ M = 1.1447\,(\hat\alpha(1)\,n)^{1/3} \ \text{(Bartlett)}, \qquad M = 1.3221\,(\hat\alpha(2)\,n)^{1/5} \ \text{(QS)}, \qquad \omega = 0 \]'''),
     [T(r'$\hat\alpha(q)$: the ratio $(f^{(q)}(0)/f(0))^2$ computed from the fitted AR(1), e.g.\ $\hat\alpha(2) = 4\hat\rho^2/(1 - \hat\rho)^4$ ($\hat\rho$: AR coefficient)',
        r'$\hat\alpha(q)$: raportul $(f^{(q)}(0)/f(0))^2$ calculat din AR(1) estimat, de exemplu $\hat\alpha(2) = 4\hat\rho^2/(1 - \hat\rho)^4$ ($\hat\rho$: coeficientul AR)'),
      T('good for long-run variances (Chapter 0); poor near sharp peaks, where the AR(1) approximation is wrong', 'bun pentru varianțele pe termen lung (Capitolul 0); slab lîngă vîrfuri ascuțite, unde aproximarea AR(1) este greșită')]),
    (T(r'\textbf{Cross-validation} \refHur: minimise over $M$ a leave-one-out Whittle criterion', r'\textbf{Validare încrucișată} \refHur: minimizăm în $M$ un criteriu Whittle fără observația $j$'
       ) + r'''
    \[ \mathrm{CV}(M) = \sum_j\Big[\log\hat f_{-j}(\omega_j) + \frac{I(\omega_j)}{\hat f_{-j}(\omega_j)}\Big] \]''',
     [T(r'$\hat f_{-j}$: the smoothed estimate computed without the ordinate $I(\omega_j)$', r'$\hat f_{-j}$: estimația netezită calculată fără ordonata $I(\omega_j)$')]),
    (T('\\textbf{Resolution}: two peaks closer than the bandwidth (about $1/M$ cycles) merge; decide the resolution you need before looking at the data',
       '\\textbf{Rezoluția}: două vîrfuri mai apropiate decît lățimea de bandă (circa $1/M$ cicluri) se contopesc; stabiliți rezoluția necesară înainte de a privi datele'),
     [T('report the estimate for two or three bandwidths: conclusions that depend on $M$ are not conclusions', 'raportați estimarea pentru două sau trei lățimi de bandă: concluziile care depind de $M$ nu sînt concluzii')])), 'small')

D.frame(T('Multitaper estimation (1/2): Slepian tapers', 'Estimarea multitaper (1/2): taper-ele Slepian'), items(
    (T(r'\textbf{Slepian (DPSS) tapers} $v^{(k)}$, $k = 0, \dots, K - 1$ \refTho', r'\textbf{Taper-ele Slepian (DPSS)} $v^{(k)}$, $k = 0, \dots, K - 1$ \refTho'),
     [T(r'orthonormal weight sequences of length $n$ that maximise the share $\lambda_k$ of their spectral energy inside $[-W, W]$; $W$: half-bandwidth in cycles',
        r'șiruri de ponderi ortonormate de lungime $n$ care maximizează ponderea $\lambda_k$ a energiei lor spectrale în intervalul $[-W, W]$; $W$: semilățimea de bandă în cicluri'),
      T(r'about $2nW$ of them have $\lambda_k \approx 1$; usually $K = 2NW - 1$ with $NW = nW$ (e.g.\ $NW = 4$, $K = 7$)',
        r'aproximativ $2nW$ dintre ele au $\lambda_k \approx 1$; de obicei $K = 2NW - 1$, cu $NW = nW$ (de exemplu $NW = 4$, $K = 7$)')]),
    (T(r'Eigenspectra: one tapered periodogram per taper; the estimate is their average', r'Spectrele proprii: cîte o periodogramă ponderată pentru fiecare taper; estimația este media lor'
       ) + r'''
    \[ \hat S_k(\omega) = \frac{1}{2\pi}\Big|\sum_tv_t^{(k)}x_te^{-i\omega t}\Big|^2, \qquad \hat f^{\mathrm{mt}}(\omega) = \frac1K\sum_{k=0}^{K-1}\hat S_k(\omega) \]''',
     [T(r'the $\hat S_k$ are nearly uncorrelated: $2K\hat f^{\mathrm{mt}}/f \approx \chi^2_{2K}$; variance $f^2/K$, bias controlled by the taper concentration',
        r'$\hat S_k$ sînt aproape necorelate: $2K\hat f^{\mathrm{mt}}/f \approx \chi^2_{2K}$; varianța $f^2/K$, deplasarea controlată de concentrarea taper-elor')])), 'small')

D.frame(T('Multitaper estimation (2/2): adaptive weights', 'Estimarea multitaper (2/2): ponderi adaptive'), items(
    (T(r'\textbf{Adaptive weights} \refPWa: down-weight leaky tapers where $f$ is small', r'\textbf{Ponderi adaptive} \refPWa: se reduce ponderea taper-elor cu leakage mare acolo unde $f$ este mic'
       ) + r'''
    \[ d_k(\omega) = \frac{\sqrt{\lambda_k}\,f(\omega)}{\lambda_kf(\omega) + (1 - \lambda_k)\sigma^2} \]''',
     [T(r'$\sigma^2$: the variance of the series; $1 - \lambda_k$: the leakage of taper $k$; the weights depend on the unknown $f$, so they are iterated from $\hat f^{\mathrm{mt}}$',
        r'$\sigma^2$: varianța seriei; $1 - \lambda_k$: leakage-ul taper-ului $k$; ponderile depind de $f$ necunoscut, deci se iterează pornind de la $\hat f^{\mathrm{mt}}$')]),
    T(r'Alternatives with the same logic: sine tapers \refRS; Welch\'s averaging of tapered segments \refWel',
      r'Alternative cu aceeași logică: taper-ele sinus \refRS; medierea Welch a segmentelor ponderate \refWel')), 'small')

chart(T('Slepian tapers', 'Taper-ele Slepian'), 'ats_ch11_dpss', 'ATS_ch11_spectral_estimation', [
    T(r'$n = 512$, $NW = 4$: the first four tapers and the leakage $1 - \lambda_k$ of the first ten (blue: $k < 2NW - 1$)',
      r'$n = 512$, $NW = 4$: primele patru taper-e și leakage-ul $1 - \lambda_k$ a primelor zece (albastru: $k < 2NW - 1$)')],
    h='0.48\\textheight')

interp(('the tapers', 'taper-elor'), [
    T('Taper $k$ has $k$ zero crossings: higher tapers weight the ends of the sample, so together they use all the data',
      'Taper-ul $k$ are $k$ treceri prin zero: taper-ele de ordin mare ponderează capetele eșantionului, deci împreună folosesc toate datele'),
    T(r'Leakage grows fast with $k$: $\lambda_6 = @{dp.l6}$, but $\lambda_7 = @{dp.l7}$ and $\lambda_8 = @{dp.l8}$; beyond $2NW - 1$ the tapers are useless',
      r'Leakage-ul crește repede cu $k$: $\lambda_6 = @{dp.l6}$, dar $\lambda_7 = @{dp.l7}$ și $\lambda_8 = @{dp.l8}$; dincolo de $2NW - 1$ taper-ele nu mai sînt utile'),
    T('The single Hann taper throws away the ends; multitapering recovers that information as extra degrees of freedom',
      'Un singur taper Hann aruncă extremitățile; estimarea multitaper recuperează această informație ca grade de libertate suplimentare'),
    T('$NW$ is the only tuning choice: it fixes the resolution $2W = 2NW/n$ and the variance $f^2/K$ together',
      '$NW$ este singura alegere de calibrare: fixează împreună rezoluția $2W = 2NW/n$ și varianța $f^2/K$')])

chart(T('Leakage on a spectrum with a high dynamic range', 'Leakage-ul spectral pe un spectru cu domeniu dinamic mare'), 'ats_ch11_leakage', 'ATS_ch11_spectral_estimation', [
    T(r'The AR(4) of Percival and Walden (1993), $n = 1024$, range of @{lk.range} dB between peak and trough; one simulated path (median leakage of 21)',
      r'Modelul AR(4) al lui Percival și Walden (1993), $n = 1024$, @{lk.range} dB între vîrf și minim; o traiectorie simulată (cu leakage-ul median din 21)')],
    h='0.5\\textheight')

interp(('leakage', 'leakage-ului'), [
    T(r'Mean bias at frequencies above 0.3 cycles (@{lk.reps} simulations): periodogram +@{lk.raw} dB, Hann taper @{lk.hann} dB, multitaper +@{lk.mt} dB, adaptive multitaper @{lk.mta} dB',
      r'Deplasarea medie la frecvențe peste 0,3 cicluri (@{lk.reps} de simulări): periodograma +@{lk.raw} dB, taper Hann @{lk.hann} dB, multitaper +@{lk.mt} dB, multitaper adaptiv @{lk.mta} dB'),
    T('The raw periodogram fills the trough with power leaked from the peaks: averaging it more would not help, the bias is in each ordinate',
      'Periodograma brută umple minimul cu putere scursă din vîrfuri: o mediere suplimentară nu ar ajuta, deplasarea este în fiecare ordonată'),
    T('With equal weights the leaky high-order tapers still contaminate the trough; the adaptive weights remove it',
      'Cu ponderi egale, taper-ele de ordin mare, care au leakage mare, contaminează încă minimul; ponderile adaptive o elimină'),
    T('Economic data rarely have 60 dB ranges, but spectra of levels with a unit-root-like peak at zero do: taper or prewhiten before estimating',
      'Datele economice au rareori domenii de 60 dB, dar spectrele nivelurilor, cu un vîrf în zero ca la o rădăcină unitară, le au: aplicați un taper sau o prealbire înainte de estimare')])

chart(T('Five estimators in a Monte Carlo', 'Cinci estimatori într-un experiment Monte Carlo'), 'ats_ch11_mt_mc', 'ATS_ch11_spectral_estimation', [
    T(r'$X_t = 1.6X_{t-1} - 0.9X_{t-2} + \varepsilon_t$, $n = 512$, @{mc.reps} simulations: mean log-bias by frequency and coverage of the nominal 95\% $\chi^2$ bands',
      r'$X_t = 1.6X_{t-1} - 0.9X_{t-2} + \varepsilon_t$, $n = 512$, @{mc.reps} de simulări: deplasarea medie în logaritmi pe frecvențe și acoperirea benzilor $\chi^2$ nominale de 95\%')],
    h='0.5\\textheight')

interp(('the Monte Carlo', 'experimentului Monte Carlo'), [
    T(r'Standard deviation of $10\log_{10}(\hat f/f)$: periodogram @{mc.pg.sd} dB, Daniell @{mc.dn.sd}, multitaper @{mc.mt.sd}, Parzen @{mc.pz.sd}, Welch @{mc.we.sd}',
      r'Abaterea standard a lui $10\log_{10}(\hat f/f)$: periodograma @{mc.pg.sd} dB, Daniell @{mc.dn.sd}, multitaper @{mc.mt.sd}, Parzen @{mc.pz.sd}, Welch @{mc.we.sd}'),
    T(r'At the peak: Parzen @{mc.pz.bp} dB, Welch @{mc.we.bp} dB, multitaper @{mc.mt.bp} dB; the periodogram\'s @{mc.pg.b} dB is the mean of $\log\chi^2_2/2$, not a bias in levels',
      r'În vîrf: Parzen @{mc.pz.bp} dB, Welch @{mc.we.bp} dB, multitaper @{mc.mt.bp} dB; valoarea @{mc.pg.b} dB a periodogramei este media lui $\log\chi^2_2/2$, nu o deplasare în niveluri'),
    T(r'Coverage of the 95\% band: multitaper @{mc.mt.cov}\%, adaptive @{mc.ma.cov}\%, Daniell @{mc.dn.cov}\% (its band ignores the bias on the slopes)',
      r'Acoperirea benzii de 95\%: multitaper @{mc.mt.cov}\%, adaptiv @{mc.ma.cov}\%, Daniell @{mc.dn.cov}\% (banda lui ignoră deplasarea de pe pante)'),
    T('Multitaper is the only estimator here with small bias, small variance and honest bands at once',
      'Multitaper este singurul estimator de aici care are simultan deplasare mică, varianță mică și benzi corecte')])

chart(T('Industrial production: Romania and the euro area', 'Producția industrială: România și zona euro'), 'ats_ch11_ip_spectrum', 'ATS_ch11_ip_spectrum', [
    T(r'Monthly growth of industrial production (seasonally and calendar adjusted), February 2000 -- July 2026, @{ip.n} months; multitaper $NW = 4$ with 95\% bands',
      r'Creșterea lunară a producției industriale (ajustată sezonier și pentru zilele lucrătoare), februarie 2000 -- iulie 2026, @{ip.n} luni; multitaper $NW = 4$ cu benzi de 95\%')],
    h='0.5\\textheight')

interp(('the industrial production spectra', 'spectrelor producției industriale'), [
    T(r'Monthly growth is dominated by short periods: cycles under 6 months carry @{ip.RO.sh}\% of the variance in Romania and @{ip.EA20.sh}\% in the euro area',
      r'Creșterea lunară este dominată de perioadele scurte: ciclurile sub 6 luni au @{ip.RO.sh}\% din varianță în România și @{ip.EA20.sh}\% în zona euro'),
    T(r'The business-cycle band (18--96 months) holds @{ip.RO.bc}\% (Romania) and @{ip.EA20.bc}\% (euro area): growth rates hide cycles that levels show (the first-difference gain)',
      r'Banda ciclului economic (18--96 de luni) are @{ip.RO.bc}\% (România) și @{ip.EA20.bc}\% (zona euro): ratele de creștere ascund ciclurile vizibile în niveluri (cîștigul primei diferențe)'),
    T(r'Romania is more volatile (standard deviation @{ip.RO.sd} against @{ip.EA20.sd}), and the excess is at high frequencies, where the bands do not overlap: noise, revisions and residual calendar effects',
      r'România este mai volatilă (abaterea standard @{ip.RO.sd} față de @{ip.EA20.sd}), iar surplusul este la frecvențe înalte, unde benzile nu se suprapun: zgomot, revizuiri și efecte de calendar reziduale'),
    T('At periods above 12 months the two spectra cannot be told apart within the bands', 'La perioade de peste 12 luni, cele două spectre nu se pot distinge în interiorul benzilor')])

D.frame(T('Lines in the spectrum: Thomson\'s F test (1/2)', 'Linii în spectru: testul F al lui Thomson (1/2)'), items(
    (T(r'Model: a sinusoid plus noise with a smooth spectrum \refTho', r'Modelul: o sinusoidă plus un zgomot cu spectru neted \refTho'
       ) + r'''
    \[ x_t = \mu\cos(\omega_0t + \phi) + e_t \]''',
     [T(r'$\mu$: amplitude; $\omega_0$: frequency of the line; $\phi$: phase; $e_t$: stationary noise',
        r'$\mu$: amplitudinea; $\omega_0$: frecvența liniei; $\phi$: faza; $e_t$: zgomot staționar'),
      T(r'under a line, each tapered DFT is $Y_k(\omega_0) \approx \mu\,U_k(0)$, with $U_k(0) = \sum_tv^{(k)}_t$ the sum of taper $k$',
        r'sub o linie, fiecare DFT ponderat este $Y_k(\omega_0) \approx \mu\,U_k(0)$, cu $U_k(0) = \sum_tv^{(k)}_t$ suma taper-ului $k$')]),
    T('A regression of the eigencoefficients $Y_k$ on the taper sums $U_k(0)$, frequency by frequency: it separates a deterministic line from a stochastic peak, which Fisher\'s test (TSA) cannot',
      'O regresie a coeficienților proprii $Y_k$ pe sumele taper-elor $U_k(0)$, frecvență cu frecvență: separă o linie deterministă de un vîrf stochastic, ceea ce testul lui Fisher (TSA) nu poate')), 'small')

D.frame(T('Lines in the spectrum: Thomson\'s F test (2/2)', 'Linii în spectru: testul F al lui Thomson (2/2)'), items(
    (T(r'Estimated amplitude and the F statistic: explained against residual variation', r'Amplitudinea estimată și statistica F: variația explicată față de cea reziduală'
       ) + r'''
    \[ \hat\mu(\omega) = \frac{\sum_kU_k(0)Y_k(\omega)}{\sum_kU_k(0)^2}, \qquad F(\omega) = \frac{(K - 1)\,|\hat\mu|^2\sum_kU_k(0)^2}{\sum_k|Y_k - \hat\mu U_k(0)|^2} \sim F_{2, 2K - 2} \]''',
     [T(r'a large $F(\omega)$: a line at $\omega$; $K$: number of tapers', r'un $F(\omega)$ mare: o linie în $\omega$; $K$: numărul de taper-e')]),
    T('Application: residual seasonality is a set of lines at $k/12$ cycles per month; trading-day effects are lines at 0.348 and 0.432 cycles per month',
      'Aplicație: sezonalitatea reziduală este o mulțime de linii la $k/12$ cicluri pe lună; efectele zilelor lucrătoare sînt linii la 0,348 și 0,432 cicluri pe lună'),
    T('Testing at hundreds of frequencies: expect about 1\\% false rejections at the 1\\% level; test only pre-specified frequencies',
      'Testarea la sute de frecvențe: așteptați circa 1\\% respingeri false la nivelul de 1\\%; testați doar frecvențe stabilite dinainte')), 'small')

chart(T('Residual seasonality in Romanian industrial production', 'Sezonalitatea reziduală în producția industrială a României'), 'ats_ch11_ftest', 'ATS_ch11_ip_spectrum', [
    T(r'Harmonic F test ($NW = 4$, $K = 7$) on monthly growth, unadjusted and adjusted series; dotted lines: the six seasonal frequencies',
      r'Testul F armonic ($NW = 4$, $K = 7$) pe creșterea lunară, seria neajustată și seria ajustată; liniile punctate: cele șase frecvențe sezoniere')],
    h='0.5\\textheight')

interp(('the F test', 'testului F'), [
    T(r'Unadjusted: @{ft.nsa} of 6 seasonal harmonics are lines at 1\% ($p$ @{ft.p2} and @{ft.p3} at 2 and 3 cycles per year); the annual harmonic is borderline ($p$ = @{ft.p1})',
      r'Seria neajustată: @{ft.nsa} din 6 armonici sezoniere sînt linii la 1\% ($p$ @{ft.p2} și @{ft.p3} la 2 și 3 cicluri pe an); armonica anuală este la limită ($p$ = @{ft.p1})'),
    T(r'A strong line at 4.18 cycles per year ($p$ @{ft.td}): the trading-day frequency, a calendar effect, not seasonality',
      r'O linie puternică la 4,18 cicluri pe an ($p$ @{ft.td}): frecvența zilelor lucrătoare, un efect de calendar, nu sezonalitate'),
    T(r'Adjusted series: @{ft.sca}, and there is no line at the trading-day frequency ($p$ = @{ft.tds}): the adjustment passes this check',
      r'Seria ajustată: @{ft.sca} și nu există nicio linie la frecvența zilelor lucrătoare ($p$ = @{ft.tds}): ajustarea trece această verificare'),
    T(r'The annual harmonic is weak because Romanian seasonality is not a pure sinusoid: its power sits at the higher harmonics', r'Armonica anuală este slabă deoarece sezonalitatea românească nu este o sinusoidă pură: puterea ei se află în armonicile superioare')])

D.recap(('Spectral estimation theory', 'teoria estimării spectrale'), [
    T('The periodogram is unbiased in the limit but inconsistent and leaky; smoothing buys consistency, tapering buys low bias', 'Periodograma este asimptotic nedeplasată, dar inconsistentă și afectată de leakage; netezirea aduce consistență, iar taper-ul aduce deplasare mică'),
    T('Bandwidth is a bias--variance choice with $M^* \\propto n^{1/(2q+1)}$; peaks need narrow windows', 'Lățimea de bandă este o alegere deplasare--varianță cu $M^* \\propto n^{1/(2q+1)}$; vîrfurile cer ferestre înguste'),
    T('Multitaper: $\\chi^2_{2K}$ bands that hold, adaptive weights against leakage, and an F test for lines', 'Multitaper: benzi $\\chi^2_{2K}$ care își respectă nivelul, ponderi adaptive împotriva leakage-ului și un test F pentru linii')])

# =============================================================================
# 3. DOUĂ SERII
# =============================================================================
D.section('Two series: coherence, phase and causality', 'Două serii: coerență, fază și cauzalitate')

D.frame(T('Coherence, phase and gain (1/2): coherence', 'Coerența, faza și cîștigul (1/2): coerența'), items(
    (T(r'\textbf{Squared coherence}: the $R^2$ of the regression of $dZ_y(\omega)$ on $dZ_x(\omega)$', r'\textbf{Coerența pătratică}: $R^2$ al regresiei lui $dZ_y(\omega)$ pe $dZ_x(\omega)$'
       ) + r'''
    \[ \kappa^2_{xy}(\omega) = \frac{|f_{xy}(\omega)|^2}{f_x(\omega)f_y(\omega)} \in [0, 1] \]''',
     [T(r'$f_x$, $f_y$: the two spectra; $f_{xy}$: the cross-spectrum; $\kappa^2 = 1$: $y$ is an exact linear filter of $x$ at frequency $\omega$; $\kappa^2 = 0$: no linear relation at that frequency',
        r'$f_x$, $f_y$: cele două spectre; $f_{xy}$: spectrul încrucișat; $\kappa^2 = 1$: $y$ este exact un filtru liniar al lui $x$ la frecvența $\omega$; $\kappa^2 = 0$: nicio relație liniară la acea frecvență'),
      T(r'invariant to filtering each series by an invertible filter: coherence does not depend on how the series are transformed (Appendix)  % applink: two filter facts',
        r'invariantă la filtrarea fiecărei serii cu un filtru inversabil: coerența nu depinde de felul în care sînt transformate seriile (Anexa)  % applink: două proprietăți ale filtrelor')]),
    T(r'\textbf{Gain} $|f_{xy}(\omega)|/f_x(\omega)$: the regression coefficient of $y$ on $x$ at frequency $\omega$',
      r'\textbf{Cîștigul} $|f_{xy}(\omega)|/f_x(\omega)$: coeficientul de regresie al lui $y$ pe $x$ la frecvența $\omega$')), 'small')

D.frame(T('Coherence, phase and gain (2/2): phase', 'Coerența, faza și cîștigul (2/2): faza'), items(
    (T(r'\textbf{Phase}: the angle of the cross-spectrum, with $\gamma_{xy}(h) = \Cov(x_{t+h}, y_t)$', r'\textbf{Faza}: unghiul spectrului încrucișat, cu $\gamma_{xy}(h) = \Cov(x_{t+h}, y_t)$'
       ) + r'''
    \[ \phi_{xy}(\omega) = \arg f_{xy}(\omega) \]''',
     [T(r'example: if $y_t = x_{t-d}$, then $f_{xy} = e^{i\omega d}f_x$, phase $\omega d > 0$: $x$ leads by $\phi/\omega$ periods',
        r'exemplu: dacă $y_t = x_{t-d}$, atunci $f_{xy} = e^{i\omega d}f_x$, faza $\omega d > 0$: $x$ conduce cu $\phi/\omega$ perioade'),
      T(r'the phase is defined modulo $2\pi$: a lead of $d$ and a lag of $2\pi/\omega - d$ are the same phase', r'faza este definită modulo $2\pi$: un avans de $d$ și o întîrziere de $2\pi/\omega - d$ dau aceeași fază')]),
    T('Interpret the phase only where coherence is significant', 'Interpretați faza doar unde coerența este semnificativă')), 'small')

D.frame(T('Inference on coherence and phase', 'Inferență pentru coerență și fază'), items(
    (T(r'The raw cross-periodogram gives $\hat\kappa^2 \equiv 1$ at every frequency: coherence \textbf{must} be smoothed (here: averaged over $K$ tapers)',
       r'Periodograma încrucișată brută dă $\hat\kappa^2 \equiv 1$ la orice frecvență: coerența \textbf{trebuie} netezită (aici: mediată pe $K$ taper-e)'
       ) + M(r'''
    \[ \Pr(\hat\kappa^2 > c \mid \kappa^2 = 0) = (1 - c)^{L-1} \ \Rightarrow\ c_{0.05} = 1 - 0.05^{1/(L-1)} \]'''),
     [T(r'$L$: number of independent ordinates averaged ($L = K$ for multitaper); $c$: threshold; $\hat\kappa^2$ above $c_{0.05}$ is significant at 5\%',
        r'$L$: numărul ordonatelor independente mediate ($L = K$ pentru multitaper); $c$: pragul; un $\hat\kappa^2$ peste $c_{0{,}05}$ este semnificativ la 5\%')]),
    (T(r'$\hat\kappa^2$ is biased upwards when $\kappa^2$ is small; confidence intervals via the Fisher transform $\tanh^{-1}\hat\kappa$ \refSS', r'$\hat\kappa^2$ este deplasat în sus cînd $\kappa^2$ este mic; intervale de încredere prin transformarea Fisher $\tanh^{-1}\hat\kappa$ \refSS'),
     [T(r'phase: $\mathrm{se}(\hat\phi) \approx \sqrt{(1/\hat\kappa^2 - 1)/(2L)}$; it explodes as coherence falls', r'faza: $\mathrm{se}(\hat\phi) \approx \sqrt{(1/\hat\kappa^2 - 1)/(2L)}$; crește foarte mult cînd coerența scade')]),
    T(r'Misalignment bias: a long delay $d$ rotates the phase within the smoothing band and lowers $\hat\kappa^2$; align the series (or prewhiten) first',
      r'Deplasarea din nealiniere: o întîrziere mare $d$ rotește faza în interiorul benzii de netezire și scade $\hat\kappa^2$; aliniați seriile (sau aplicați o prealbire) mai întîi')), 'small')

chart(T('Romania and the euro area: coherence, phase and gain', 'România și zona euro: coerență, fază și cîștig'), 'ats_ch11_coherence', 'ATS_ch11_cross_spectrum', [
    T(r'Monthly industrial production growth, euro area ($x$) and Romania ($y$); multitaper $NW = 6$, $K = @{co.K}$; shaded: 18--96 months',
      r'Creșterea lunară a producției industriale, zona euro ($x$) și România ($y$); multitaper $NW = 6$, $K = @{co.K}$; zona colorată: 18--96 de luni')],
    h='0.48\\textheight')

interp(('the cross-spectrum', 'spectrului încrucișat'), [
    T(r'Coherence averages @{co.bc} in the business-cycle band and @{co.sh} below 12 months; the 5\% threshold is @{co.thr}: significant at @{co.sbc}\% of business-cycle frequencies and @{co.ssh}\% of short ones',
      r'Coerența medie este @{co.bc} în banda ciclului economic și @{co.sh} sub 12 luni; pragul de 5\% este @{co.thr}: semnificativă la @{co.sbc}\% din frecvențele ciclului economic și la @{co.ssh}\% din cele scurte'),
    T(r'The phase is near zero: the median implied lead is @{co.lead} months, inside two standard errors: Romanian industry moves with the euro area within the month',
      r'Faza este aproape de zero: avansul median implicat este de @{co.lead} luni, în interiorul a două erori standard: industria românească se mișcă odată cu zona euro în aceeași lună'),
    T(r'Gain @{co.gbc} at business-cycle frequencies, @{co.gsh} at short ones: Romania amplifies euro-area shocks only at high frequencies',
      r'Cîștigul este @{co.gbc} la frecvențele ciclului economic și @{co.gsh} la cele scurte: România amplifică șocurile din zona euro doar la frecvențe înalte'),
    T(r'The simple correlation (@{co.corr}) mixes these bands; the coherence separates where co-movement is strong from where it is noise',
      r'Corelația simplă (@{co.corr}) amestecă aceste benzi; coerența separă zonele cu co-mișcare puternică de cele cu zgomot')])

D.frame(T('Dynamic correlation', 'Corelația dinamică'), items(
    (T(r'\refCFR: the correlation of the in-phase (real) components at frequency $\omega$', r'\refCFR: corelația componentelor în fază (reale) la frecvența $\omega$'
       ) + r'''
    \[ \rho_{xy}(\omega) = \frac{c_{xy}(\omega)}{\sqrt{f_x(\omega)f_y(\omega)}} \in [-1, 1] \]
    \[ \kappa^2 = \rho^2 + \Big(\frac{q_{xy}}{\sqrt{f_xf_y}}\Big)^2 \]''',
     [T(r'$c_{xy}$, $q_{xy}$: co-spectrum and quadrature spectrum; unlike coherence, $\rho_{xy}$ has a \textbf{sign} and is not increased by out-of-phase movement',
        r'$c_{xy}$, $q_{xy}$: cospectrul și spectrul în cuadratură; spre deosebire de coerență, $\rho_{xy}$ are \textbf{semn} și nu este mărit artificial de mișcarea defazată')]),
    (T(r'Over a band $\Lambda$ of frequencies', r'Pe o bandă $\Lambda$ de frecvențe'
       ) + r'''
    \[ \rho_{xy}(\Lambda) = \frac{\int_\Lambda c_{xy}}{\sqrt{\int_\Lambda f_x\int_\Lambda f_y}} \]''',
     [T('over $[0, \\pi]$ it is the ordinary correlation; over a band it equals the correlation of the band-pass filtered series (Section 4)',
        'pe $[0, \\pi]$ este corelația obișnuită; pe o bandă este egală cu corelația seriilor filtrate trece-bandă (secțiunea 4)')]),
    T(r'\textbf{Cohesion}: a weighted average of pairwise $\rho_{xy}(\omega)$ inside a group of countries; CFR use it for euro-area business cycles',
      r'\textbf{Coeziunea}: o medie ponderată a corelațiilor $\rho_{xy}(\omega)$ pe perechi într-un grup de țări; CFR o folosesc pentru ciclurile economice din zona euro')), 'small')

D.frame(T('Granger causality by frequency (1/2): the Geweke measure', 'Cauzalitatea Granger pe frecvențe (1/2): măsura Geweke'), items(
    (T(r'\refGew: in a bivariate VAR, normalise the innovations so that $x$\'s innovation is uncorrelated with the transformed $y$ innovation; then', r'\refGew: într-un VAR bivariat, normalizăm inovațiile astfel încît inovația lui $x$ să fie necorelată cu inovația transformată a lui $y$; atunci'
       ) + r'''
    \[ f_x(\omega) = \frac{1}{2\pi}\Big(|\tilde H_{xx}(\omega)|^2\tilde\sigma_{xx} + |\tilde H_{xy}(\omega)|^2\tilde\sigma_{yy}\Big) \]''',
     [T(r'$\tilde H$: the transfer function (moving-average representation) of the normalised VAR; $\tilde\sigma_{xx}$, $\tilde\sigma_{yy}$: variances of the two orthogonal innovations',
        r'$\tilde H$: funcția de transfer (reprezentarea de medie mobilă) a VAR normalizat; $\tilde\sigma_{xx}$, $\tilde\sigma_{yy}$: varianțele celor două inovații ortogonale')]),
    (T(r'The share of $f_x(\omega)$ that comes from $y$', r'Partea din $f_x(\omega)$ care provine de la $y$'
       ) + r'''
    \[ M_{y \to x}(\omega) = \ln\frac{2\pi f_x(\omega)}{|\tilde H_{xx}(\omega)|^2\tilde\sigma_{xx}} \ge 0 \]
    \[ \frac{1}{\pi}\int_0^\pi M_{y \to x}(\omega)\,d\omega = \ln\frac{\sigma^2_{x|x}}{\sigma^2_{x|x,y}} \]''',
     [T(r'the integral is the time-domain Granger measure (under a mild condition): $\sigma^2_{x|x}$, $\sigma^2_{x|x,y}$ are the one-step forecast variances of $x$ without and with the past of $y$',
        r'integrala este măsura Granger din domeniul timpului (sub o condiție slabă): $\sigma^2_{x|x}$, $\sigma^2_{x|x,y}$ sînt varianțele prognozei cu un pas a lui $x$ fără și cu trecutul lui $y$')])), 'footnotesize')

D.frame(T('Granger causality by frequency (2/2): the Breitung--Candelon test', 'Cauzalitatea Granger pe frecvențe (2/2): testul Breitung--Candelon'), items(
    (T(r'\refBC: no causality at frequency $\omega$ is two linear restrictions on the coefficients of $y$ in the $x$ equation', r'\refBC: lipsa cauzalității la frecvența $\omega$ înseamnă două restricții liniare asupra coeficienților lui $y$ din ecuația lui $x$'
       ) + T(r'''
    \[ M_{y \to x}(\omega) = 0 \iff \sum_{j=1}^p\psi_j\cos(j\omega) = 0 \ \text{ and } \ \sum_{j=1}^p\psi_j\sin(j\omega) = 0 \]''', r'''
    \[ M_{y \to x}(\omega) = 0 \iff \sum_{j=1}^p\psi_j\cos(j\omega) = 0 \ \text{ și } \ \sum_{j=1}^p\psi_j\sin(j\omega) = 0 \]'''),
     [T(r'$\psi_j$: coefficient of $y_{t-j}$ in the $x$ equation; $p$: VAR order; an $F(2, T - 2p - 1)$ test at each $\omega$, $T$: number of observations',
        r'$\psi_j$: coeficientul lui $y_{t-j}$ în ecuația lui $x$; $p$: ordinul VAR; un test $F(2, T - 2p - 1)$ la fiecare $\omega$, $T$: numărul de observații'),
      T(r'with $p \le 2$ the two restrictions fix all $\psi_j$, so the test is the same at every frequency', r'cu $p \le 2$ cele două restricții fixează toți $\psi_j$, deci testul este același la orice frecvență')]),
    T('BC show that the test extends to cointegrated VARs (long-run causality at $\\omega = 0$); pointwise tests across frequencies are not a joint test',
      'BC arată că testul se extinde la VAR cointegrate (cauzalitate pe termen lung în $\\omega = 0$); testele punctuale pe frecvențe nu sînt un test comun')), 'small')

chart(T('Does the euro area cause Romanian industry, and at which frequencies?', 'Cauzează zona euro industria românească și la ce frecvențe?'), 'ats_ch11_causality', 'ATS_ch11_causality', [
    T(r'VAR(@{ca.p}) in monthly industrial production growth (order by AIC, at least 3); left: Geweke measures; right: Breitung--Candelon $F$ with its 5\% critical value @{ca.crit}',
      r'VAR(@{ca.p}) pentru creșterea lunară a producției industriale (ordinul ales prin AIC, cel puțin 3); stînga: măsurile Geweke; dreapta: statistica $F$ Breitung--Candelon cu valoarea critică de 5\% @{ca.crit}')],
    h='0.48\\textheight')

interp(('frequency-domain causality', 'cauzalității în domeniul frecvenței'), [
    T(r'Euro area $\to$ Romania: total Geweke measure @{ca.F1} (integral of the curve: @{ca.int}); Romania $\to$ euro area: @{ca.F2}',
      r'Zona euro $\to$ România: măsura Geweke totală @{ca.F1} (integrala curbei: @{ca.int}); România $\to$ zona euro: @{ca.F2}'),
    T(r'The measure is @{ca.bc} in the business-cycle band and @{ca.sh} at periods under 6 months: past euro-area growth predicts Romanian growth mostly at short horizons',
      r'Măsura este @{ca.bc} în banda ciclului economic și @{ca.sh} la perioade sub 6 luni: creșterea trecută din zona euro prezice creșterea românească mai ales la orizonturi scurte'),
    T(r'The BC test rejects at @{ca.r1}\% of frequencies for euro area $\to$ Romania and @{ca.r2t} in the other direction',
      r'Testul BC respinge la @{ca.r1}\% din frecvențe pentru zona euro $\to$ România și @{ca.r2t} în cealaltă direcție'),
    T('A small open economy follows its main market, not the reverse; the frequency profile says which kind of shock transmits fastest',
      'O economie mică și deschisă își urmează piața principală, nu invers; profilul pe frecvențe arată ce tip de șoc se transmite cel mai repede')])

D.recap(('Two series', 'două serii'), [
    T('Coherence is an $R^2$ by frequency; it must be smoothed and tested against $1 - \\alpha^{1/(L-1)}$', 'Coerența este un $R^2$ pe frecvențe; trebuie netezită și testată față de $1 - \\alpha^{1/(L-1)}$'),
    T('Phase gives leads and lags, modulo $2\\pi$, only where coherence is significant; dynamic correlation keeps the sign', 'Faza dă avansurile și întîrzierile, modulo $2\\pi$, doar unde coerența este semnificativă; corelația dinamică păstrează semnul'),
    T('Geweke decomposes Granger causality by frequency; Breitung--Candelon tests it with two linear restrictions', 'Geweke descompune cauzalitatea Granger pe frecvențe; Breitung--Candelon o testează prin două restricții liniare')])

# =============================================================================
# 4. FILTRE
# =============================================================================
D.section('Filters and the business cycle', 'Filtre și ciclul economic')

D.frame(T('Band-pass filters', 'Filtre trece-bandă'), items(
    (T(r'Ideal filter for periods $[p_l, p_u]$: gain 1 on the frequencies $[\omega_1, \omega_2] = [2\pi/p_u, 2\pi/p_l]$, 0 elsewhere; its weights are infinitely many',
       r'Filtrul ideal pentru perioadele $[p_l, p_u]$: cîștig 1 pe frecvențele $[\omega_1, \omega_2] = [2\pi/p_u, 2\pi/p_l]$, 0 în rest; ponderile lui sînt în număr infinit'
       ) + r'''
    \[ b_0 = \frac{\omega_2 - \omega_1}{\pi}, \qquad b_j = \frac{\sin j\omega_2 - \sin j\omega_1}{\pi j}, \quad j = \pm1, \pm2, \dots \]''',
     []),
    (T(r'\refBK: truncate at $K$ lags and add a constant so that $\sum_{j=-K}^Ka_j = 0$', r'\refBK: trunchiem la $K$ laguri și adăugăm o constantă astfel încît $\sum_{j=-K}^Ka_j = 0$'),
     [T(r'$a_j$: the adjusted weights; the zero sum removes a unit root and a linear trend; symmetric, no phase shift',
        r'$a_j$: ponderile ajustate; suma nulă elimină o rădăcină unitară și o tendință liniară; simetric, fără defazaj'),
      T(r'quarterly recommendation: BK(6, 32, $K = 12$); the price: $K$ observations lost at each end; $a_0 = @{ga.bka0}$',
        r'recomandarea trimestrială: BK(6, 32, $K = 12$); prețul: $K$ observații pierdute la fiecare capăt; $a_0 = @{ga.bka0}$')]),
    (T(r'\refCF: minimise $\E[(y^{\mathrm{ideal}}_t - \hat y_t)^2 \mid y_1, \dots, y_n]$ assuming a random walk',
       r'\refCF: minimizăm $\E[(y^{\mathrm{ideal}}_t - \hat y_t)^2 \mid y_1, \dots, y_n]$, presupunînd un mers aleator'),
     [T(r'$y^{\mathrm{ideal}}_t$: the ideal band-pass component; asymmetric, time-varying weights that use the whole sample: no lost observations, but phase shifts near the ends',
        r'$y^{\mathrm{ideal}}_t$: componenta trece-bandă ideală; ponderi asimetrice, variabile în timp, care folosesc tot eșantionul: nicio observație pierdută, dar defazaje lîngă capete')]),
    T(r'The business-cycle band of 6--32 quarters (1.5--8 years) follows Burns and Mitchell, as adopted by \refBK',
      r'Banda ciclului economic de 6--32 de trimestre (1,5--8 ani) urmează definiția Burns și Mitchell, preluată de \refBK')), 'small')

D.frame(T('The Hodrick--Prescott filter', 'Filtrul Hodrick--Prescott'), two(
    ph('prescott', T('Edward C.\\ Prescott, 2015', 'Edward C.\\ Prescott, 2015'), h='0.4\\textheight'),
    items((T(r'\refHP: the trend balances fit against smoothness', r'\refHP: tendința echilibrează potrivirea cu netezimea'
             ) + r'''
    \[ \hat\tau = \arg\min_\tau\sum_t(y_t - \tau_t)^2 + \lambda\sum_t(\Delta^2\tau_t)^2 = (I + \lambda D'D)^{-1}y \]''',
           [T(r'$\tau_t$: trend; $\Delta^2\tau_t$: its second difference; $\lambda$: smoothness penalty; $D$: the second-difference matrix; cycle $y_t - \hat\tau_t$',
              r'$\tau_t$: tendința; $\Delta^2\tau_t$: diferența ei de ordinul doi; $\lambda$: penalizarea pentru lipsa de netezime; $D$: matricea diferențelor de ordinul doi; ciclul $y_t - \hat\tau_t$')]),
          (T(r'Infinite-sample gain of the cycle: a high-pass filter', r'Cîștigul ciclului pe un eșantion infinit: un filtru trece-sus'
             ) + r'''
    \[ G(\omega) = \frac{4\lambda(1 - \cos\omega)^2}{1 + 4\lambda(1 - \cos\omega)^2} \]''',
           [T(r'the Kalman smoother of a local linear trend with signal-to-noise ratio $1/\lambda$ (Chapter 6); $\lambda = 1600$ for quarters; Ravn--Uhlig scaling $\lambda \propto s^4$ ($s$: observations per quarter): 129\,600 for months, 6.25 for years \refRU',
              r'netezitorul Kalman al unei tendințe liniare locale cu raportul semnal--zgomot $1/\lambda$ (Capitolul 6); $\lambda = 1600$ pentru trimestre; scalarea Ravn--Uhlig $\lambda \propto s^4$ ($s$: numărul de observații pe trimestru): 129\,600 pentru luni, 6,25 pentru ani \refRU')])), '0.27', '0.71'), 'footnotesize')

D.frame(T('Hamilton\'s critique', 'Critica lui Hamilton'), items(
    (T(r'\refHam: ``why you should never use the HP filter\'\'', r'\refHam: „de ce nu ar trebui să folosiți niciodată filtrul HP”'),
     [T(r'(1) applied to a random walk, HP produces a cycle with dynamics that are artefacts of the filter \refCN', r'(1) aplicat unui mers aleator, HP produce un ciclu cu o dinamică creată de filtru \refCN'),
      T('(2) end-of-sample values are very different from the values the same filter gives once more data arrive (one-sided against two-sided)', '(2) valorile de la sfîrșitul eșantionului diferă mult de cele pe care același filtru le dă după ce sosesc date noi (unilateral față de bilateral)'),
      T(r'(3) the $\lambda$ implied by a statistical model fitted to the data is far from 1600', r'(3) $\lambda$ implicat de un model statistic estimat pe date este departe de 1600')]),
    (T(r'Alternative: the \textbf{regression filter}, the cycle is the error of an $h$-step-ahead regression forecast', r'Alternativa: \textbf{filtrul de regresie}, ciclul este eroarea unei prognoze prin regresie cu $h$ pași înainte'
       ) + T(r'''
    \[ y_{t+h} = \beta_0 + \beta_1y_t + \dots + \beta_py_{t-p+1} + v_{t+h}, \qquad \text{cycle}_{t+h} = \hat v_{t+h} \]''', r'''
    \[ y_{t+h} = \beta_0 + \beta_1y_t + \dots + \beta_py_{t-p+1} + v_{t+h}, \qquad \text{ciclul}_{t+h} = \hat v_{t+h} \]'''),
     [T(r'quarterly $h = 8$, $p = 4$; one-sided by construction; for a random walk $v_{t+h} = y_{t+h} - y_t$', r'trimestrial $h = 8$, $p = 4$; unilateral prin construcție; pentru un mers aleator $v_{t+h} = y_{t+h} - y_t$')]),
    T(r'Replies: boosting the HP filter \refPS; a modified Hamilton filter for real time \refQW; the debate is about which gain you want',
      r'Răspunsuri: filtrul HP iterat (boosting) \refPS; un filtru Hamilton modificat pentru timp real \refQW; dezbaterea privește ce cîștig doriți')), 'small')

chart(T('Filters judged by their gain', 'Filtre judecate după cîștig'), 'ats_ch11_gains', 'ATS_ch11_filters', [
    T(r'Gain from the level to the cycle, by period in quarters; Christiano--Fitzgerald: the weights in the middle of a 126-quarter sample; Hamilton: $h = 8$, $p = 4$',
      r'Cîștigul de la nivel la ciclu, pe perioade în trimestre; Christiano--Fitzgerald: ponderile din mijlocul unui eșantion de 126 de trimestre; Hamilton: $h = 8$, $p = 4$')],
    h='0.5\\textheight')

interp(('the gains', 'cîștigurilor'), [
    T(r'HP is a high-pass filter: gain @{ga.hp32} at 32 quarters, @{ga.hp40} at 40 and still @{ga.hp60} at 60: the ``HP cycle\'\' contains cycles longer than 8 years',
      r'HP este un filtru trece-sus: cîștig @{ga.hp32} la 32 de trimestre, @{ga.hp40} la 40 și încă @{ga.hp60} la 60: „ciclul HP” conține cicluri mai lungi de 8 ani'),
    T(r'BK ripples around 1 (maximum @{ga.bkpeak}) and lets in @{ga.bk40} of the 40-quarter cycle; CF is closer to the ideal shape in mid-sample',
      r'BK oscilează în jurul lui 1 (maximum @{ga.bkpeak}) și lasă să treacă @{ga.bk40} din ciclul de 40 de trimestre; CF este mai aproape de forma ideală în mijlocul eșantionului'),
    T(r'Hamilton\'s filter is not a band-pass: gain @{ga.ham16} at 16 quarters and @{ga.ham8} at 8 (for random-walk weights); the estimated Romanian weights (sum @{ga.sumb}) give @{ga.hame16} and @{ga.hame8}',
      r'Filtrul lui Hamilton nu este trece-bandă: cîștig @{ga.ham16} la 16 trimestre și @{ga.ham8} la 8 (pentru ponderile mersului aleator); ponderile estimate pentru România (suma @{ga.sumb}) dau @{ga.hame16} și @{ga.hame8}'),
    T('Every filter defines its own cycle: compare cycles only after comparing gains', 'Fiecare filtru își definește propriul ciclu: comparați ciclurile doar după ce ați comparat cîștigurile')])

chart(T('A cycle made by the filter', 'Un ciclu creat de filtru'), 'ats_ch11_cogley_nason', 'ATS_ch11_filters', [
    T(r'Spectrum of the HP ($\lambda = 1600$) cycle of a random walk: $G(\omega)^2/(2\pi\cdot2(1 - \cos\omega))$, and the average periodogram of HP-filtered simulated random walks',
      r'Spectrul ciclului HP ($\lambda = 1600$) al unui mers aleator: $G(\omega)^2/(2\pi\cdot2(1 - \cos\omega))$ și periodograma medie a unor mersuri aleatoare simulate filtrate HP')],
    h='0.5\\textheight')

interp(('the spurious cycle', 'ciclului fals'), [
    T(r'A random walk has no cycle, yet its HP cycle peaks at a period of @{cn.pth} quarters (@{cn.yr} years); simulation: @{cn.pmc}',
      r'Un mers aleator nu are niciun ciclu, totuși ciclul lui HP are un vîrf la perioada de @{cn.pth} trimestre (@{cn.yr} ani); simulare: @{cn.pmc}'),
    T(r'Derivation (Seminar 11, A1): maximise $u^3/(1 + 4\lambda u^2)^2$ in $u = 1 - \cos\omega$: $u^* = \sqrt{3/(4\lambda)}$; replicates \refCN',
      r'Derivarea (Seminarul 11, A1): maximizăm $u^3/(1 + 4\lambda u^2)^2$ în $u = 1 - \cos\omega$: $u^* = \sqrt{3/(4\lambda)}$; replică \refCN'),
    T('The peak sits inside the business-cycle band: ``stylised facts\'\' computed from HP cycles can be properties of the filter',
      'Vîrful se află în banda ciclului economic: „faptele stilizate” calculate din ciclurile HP pot fi proprietăți ale filtrului'),
    T('Ravn--Uhlig scaling keeps the peak near 7.5 years at monthly and annual frequency too (Seminar 11, A2)',
      'Scalarea Ravn--Uhlig păstrează vîrful în jur de 7,5 ani și la frecvențele lunară și anuală (Seminarul 11, A2)')])

chart(T('Romanian business cycles by four filters', 'Ciclurile economice ale României după patru filtre'), 'ats_ch11_ro_cycles', 'ATS_ch11_filters', [
    T(r'100 $\times$ log real GDP of Romania, 1995Q1 -- @{cy.end}; HP ($\lambda = 1600$), BK(6, 32, 12), CF(6, 32, random walk with drift), Hamilton ($h = 8$, $p = 4$)',
      r'100 $\times$ logaritmul PIB-ului real al României, T1 1995 -- @{cy.end}; HP ($\lambda = 1600$), BK(6, 32, 12), CF(6, 32, mers aleator cu derivă), Hamilton ($h = 8$, $p = 4$)')],
    h='0.5\\textheight')

interp(('the Romanian cycles', 'ciclurilor României'), [
    T(r'All four place the 2008 peak (HP @{cy.max.hp}\%, BK @{cy.max.bk}\%) and the trough of @{cy.mq.hp} (HP @{cy.min.hp}\%, BK @{cy.min.bk}\%) at the same time',
      r'Toate cele patru filtre situează la fel vîrful din 2008 (HP @{cy.max.hp}\%, BK @{cy.max.bk}\%) și minimul din @{cy.mq.hp} (HP @{cy.min.hp}\%, BK @{cy.min.bk}\%)'),
    T(r'Amplitudes differ: standard deviation HP @{cy.sd.hp}, BK @{cy.sd.bk}, CF @{cy.sd.cf}, Hamilton @{cy.sd.ham}; the Hamilton cycle is an 8-quarter forecast error, with a trough of @{cy.min.ham}\%',
      r'Amplitudinile diferă: abaterea standard HP @{cy.sd.hp}, BK @{cy.sd.bk}, CF @{cy.sd.cf}, Hamilton @{cy.sd.ham}; ciclul Hamilton este o eroare de prognoză la 8 trimestre, cu un minim de @{cy.min.ham}\%'),
    T(r'Correlations: BK--HP @{cy.c.bkhp}, BK--CF @{cy.c.bkcf}, HP--Hamilton @{cy.c.hpham}, CF--Hamilton @{cy.c.cfham}',
      r'Corelații: BK--HP @{cy.c.bkhp}, BK--CF @{cy.c.bkcf}, HP--Hamilton @{cy.c.hpham}, CF--Hamilton @{cy.c.cfham}'),
    T(r'Today\'s position is uncertain: HP @{cy.last.hp}\%, CF @{cy.last.cf}\%, Hamilton @{cy.last.ham}\% in @{cy.lq.hp}; BK stops at @{cy.lq.bk}',
      r'Poziția de azi este incertă: HP @{cy.last.hp}\%, CF @{cy.last.cf}\%, Hamilton @{cy.last.ham}\% în @{cy.lq.hp}; BK se oprește în @{cy.lq.bk}')], size='footnotesize')

chart(T('The end-point problem', 'Problema capetelor de eșantion'), 'ats_ch11_endpoint', 'ATS_ch11_filters', [
    T(r'Romanian GDP: the cycle at each date computed with the data available at that date (real time) and with the full sample (final), from @{ep.start}',
      r'PIB-ul României: ciclul la fiecare dată calculat cu datele disponibile la acea dată (timp real) și cu tot eșantionul (final), din @{ep.start}')],
    h='0.5\\textheight')

interp(('the real-time revisions', 'revizuirilor în timp real'), [
    T(r'HP: root mean square revision @{ep.rhp} points, as large as the cycle itself (standard deviation @{ep.sdhp}); correlation of real-time and final cycles @{ep.chp}; sign wrong in @{ep.shp}\% of quarters',
      r'HP: revizuirea medie pătratică @{ep.rhp} puncte, cît ciclul însuși (abaterea standard @{ep.sdhp}); corelația dintre ciclul în timp real și cel final @{ep.chp}; semnul greșit în @{ep.shp}\% din trimestre'),
    T(r'Hamilton: correlation @{ep.cham}, sign wrong in @{ep.sham}\% of quarters; but the revision is @{ep.rham} points, because the regression is re-estimated on short samples in a transition economy',
      r'Hamilton: corelația @{ep.cham}, semnul greșit în @{ep.sham}\% din trimestre; dar revizuirea este de @{ep.rham} puncte, deoarece regresia se reestimează pe eșantioane scurte într-o economie în tranziție'),
    T('The real-time HP filter saw only a small part of the 2008 boom: the output gap that policy needed was the one it measured worst',
      'Filtrul HP în timp real a văzut doar o mică parte din boom-ul din 2008: deviația PIB-ului de la potențial de care avea nevoie politica economică era tocmai cea pe care o măsura cel mai prost'),
    T('Report real-time properties of any gap estimate; the final estimate is not information that anyone had', 'Raportați proprietățile în timp real ale oricărei estimări a deviației; estimarea finală nu este o informație pe care o avea cineva')], size='footnotesize')

D.frame(T('Measuring business-cycle synchronisation', 'Măsurarea sincronizării ciclurilor economice'), items(
    (T(r'Correlation of filtered cycles; it depends on the filter (gain) and on a few large episodes', r'Corelația ciclurilor filtrate; depinde de filtru (cîștig) și de cîteva episoade mari'), []),
    (T(r'\textbf{Concordance} \refHPa: the share of periods in which the two economies are in the same phase', r'\textbf{Concordanța} \refHPa: ponderea perioadelor în care cele două economii se află în aceeași fază'
       ) + r'''
    \[ C = \frac1T\sum_t\big[S_{xt}S_{yt} + (1 - S_{xt})(1 - S_{yt})\big] \]''',
     [T(r'$S_{xt} = 1$ if $x$ is in expansion (here: cycle above trend), 0 otherwise; under independence $\E C = p_xp_y + (1 - p_x)(1 - p_y)$, $p_x$, $p_y$: shares of expansion periods',
        r'$S_{xt} = 1$ dacă $x$ este în expansiune (aici: ciclul peste tendință), 0 altfel; sub independență $\E C = p_xp_y + (1 - p_x)(1 - p_y)$, $p_x$, $p_y$: ponderile perioadelor de expansiune')]),
    (T(r'Dynamic correlation over the business-cycle band \refCFR, which needs no filter', r'Corelația dinamică pe banda ciclului economic \refCFR, care nu cere niciun filtru'), []),
    (T(r'Evidence for Central and Eastern Europe: a meta-analysis of 35 publications \refFK', r'Evidența pentru Europa Centrală și de Est: o meta-analiză a 35 de publicații \refFK'),
     [T('some countries already had high correlations with the euro area', 'unele țări aveau deja corelații mari cu zona euro'),
      T('the estimation method changes the correlation significantly', 'metoda de estimare schimbă semnificativ corelația')])), 'small')

chart(T('Romania and the euro area: synchronisation over time', 'România și zona euro: sincronizarea în timp'), 'ats_ch11_sync', 'ATS_ch11_filters', [
    T(r'Baxter--King cycles of real GDP, @{sy.start} -- @{sy.end}, and their rolling 20-quarter correlation',
      r'Ciclurile Baxter--King ale PIB-ului real, @{sy.start} -- @{sy.end}, și corelația lor mobilă pe 20 de trimestre')],
    h='0.5\\textheight')

interp(('synchronisation', 'sincronizării'), [
    T(r'Correlation of the cycles: @{sy.corr} over the whole sample; @{sy.cpre} before 2008, @{sy.cgfc} in 2008--2012, @{sy.cpost} in 2013--2019, @{sy.ccov} from 2020',
      r'Corelația ciclurilor: @{sy.corr} pe tot eșantionul; @{sy.cpre} înainte de 2008, @{sy.cgfc} în 2008--2012, @{sy.cpost} în 2013--2019, @{sy.ccov} din 2020'),
    T(r'Concordance @{sy.conc} against @{sy.conc0} under independence: the two economies are above or below trend together most of the time',
      r'Concordanța @{sy.conc} față de @{sy.conc0} sub independență: cele două economii sînt împreună peste sau sub tendință în majoritatea timpului'),
    T(r'The Romanian cycle is larger (standard deviation @{sy.sdro} against @{sy.sdea}): synchronised in timing, not in amplitude',
      r'Ciclul României este mai amplu (abaterea standard @{sy.sdro} față de @{sy.sdea}): sincronizat ca moment, nu ca amplitudine'),
    T('The post-2020 correlation is driven by one common shock (the pandemic): a few quarters can make a decade look synchronised',
      'Corelația de după 2020 este determinată de un singur șoc comun (pandemia): cîteva trimestre pot face un deceniu să pară sincronizat')])

chart(T('Dynamic correlation with the euro area', 'Corelația dinamică cu zona euro'), 'ats_ch11_dyncorr', 'ATS_ch11_cross_spectrum', [
    T(r'Quarterly GDP growth, multitaper $NW = 3$; left: $\rho(\omega)$ for 1995--2019; right: band averages for 6--32 quarters (bars) and 2--6 quarters (diamonds), without and with 2020--2026',
      r'Creșterea trimestrială a PIB, multitaper $NW = 3$; stînga: $\rho(\omega)$ pentru 1995--2019; dreapta: mediile pe banda de 6--32 de trimestre (bare) și 2--6 trimestre (romburi), fără și cu 2020--2026')],
    h='0.48\\textheight')

interp(('the dynamic correlations', 'corelațiilor dinamice'), [
    T(r'Before 2020, business-cycle dynamic correlation: Hungary @{dc.HU.pre.bc}, Czechia @{dc.CZ.pre.bc}, Poland @{dc.PL.pre.bc}, Romania @{dc.RO.pre.bc}',
      r'Înainte de 2020, corelația dinamică pe banda ciclului economic: Ungaria @{dc.HU.pre.bc}, Cehia @{dc.CZ.pre.bc}, Polonia @{dc.PL.pre.bc}, România @{dc.RO.pre.bc}'),
    T(r'Poland\'s short-run correlation is @{dc.PL.pre.sh}: its growth co-moved with the euro area only through the business cycle',
      r'Corelația pe termen scurt a Poloniei este @{dc.PL.pre.sh}: creșterea ei s-a mișcat împreună cu zona euro doar prin ciclul economic'),
    T(r'With 2020--2026 every number rises (Romania @{dc.RO.full.bc}, Poland @{dc.PL.full.bc}): the pandemic quarter dominates every cross-periodogram',
      r'Cu 2020--2026 toate valorile cresc (România @{dc.RO.full.bc}, Polonia @{dc.PL.full.bc}): trimestrul pandemiei domină orice periodogramă încrucișată'),
    T('Report synchronisation with and without extreme common shocks; robust (trimmed or rank-based) spectra are a research topic',
      'Raportați sincronizarea cu și fără șocurile comune extreme; spectrele robuste (trunchiate sau pe ranguri) sînt o temă de cercetare')])

D.recap(('Filters and the business cycle', 'filtre și ciclul economic'), [
    T('A cycle is defined by a gain: HP is high-pass, BK and CF approximate a band-pass, Hamilton\'s regression filter is neither', 'Un ciclu este definit de un cîștig: HP este trece-sus, BK și CF aproximează un filtru trece-bandă, filtrul de regresie al lui Hamilton nu este niciunul'),
    T('HP creates a 30-quarter cycle from a random walk and is unreliable in real time', 'HP creează dintr-un mers aleator un ciclu de 30 de trimestre și nu este fiabil în timp real'),
    T('Romania is synchronised with the euro area in timing since 2010, with a larger amplitude', 'România este sincronizată cu zona euro ca moment din 2010, cu o amplitudine mai mare')])

# =============================================================================
# 5. SPECTRE NESTAȚIONARE
# =============================================================================
D.section('Spectra that change over time', 'Spectre care se schimbă în timp')

D.frame(T('Evolutionary spectra and local stationarity', 'Spectre evolutive și staționaritate locală'), items(
    (T(r'\refPri: Cramér\'s representation with a slowly changing amplitude', r'\refPri: reprezentarea lui Cramér cu o amplitudine care se schimbă lent'
       ) + r'''
    \[ X_t = \int A_t(\omega)e^{i\omega t}\,dZ(\omega), \qquad f_t(\omega) = |A_t(\omega)|^2f(\omega) \]''',
     [T(r'$A_t(\omega)$: time-varying amplitude; $f_t(\omega)$: the \textbf{evolutionary spectrum} at time $t$', r'$A_t(\omega)$: amplitudinea variabilă în timp; $f_t(\omega)$: \textbf{spectrul evolutiv} la momentul $t$')]),
    (T(r'\refDah: \textbf{locally stationary} processes $X_{t,T}$ with $A(t/T, \omega)$ smooth in rescaled time $u = t/T$',
       r'\refDah: procese \textbf{local staționare} $X_{t,T}$, cu $A(t/T, \omega)$ netedă în timpul rescalat $u = t/T$'),
     [T(r'$T$: sample size; a time-varying spectrum $f(u, \omega)$ that can be estimated consistently by a tapered spectrum on a moving window (spectrogram)',
        r'$T$: mărimea eșantionului; un spectru variabil în timp $f(u, \omega)$ care se poate estima consistent printr-un spectru cu taper pe o fereastră mobilă (spectrograma)')]),
    T(r'\textbf{Uncertainty principle}: a window of length $L$ resolves frequencies only to about $1/L$; long windows blur time, short windows blur frequency',
      r'\textbf{Principiul incertitudinii}: o fereastră de lungime $L$ separă frecvențele doar pînă la circa $1/L$; ferestrele lungi estompează timpul, cele scurte estompează frecvența'),
    T('Wavelets (next sections) let the window length change with the frequency: short for high frequencies, long for low ones',
      'Wavelets (secțiunile următoare) lasă lungimea ferestrei să varieze cu frecvența: scurtă pentru frecvențele înalte, lungă pentru cele joase')), 'small')

chart(T('A spectrum that drifts', 'Un spectru care alunecă'), 'ats_ch11_spectrogram', 'ATS_ch11_evolutionary', [
    T(r'$X_t = 2r\cos(\theta_t)X_{t-1} - r^2X_{t-2} + \varepsilon_t$, $r = 0.95$, peak period moving from 20 to 5 over 2048 observations; short-time multitaper on windows of 256 (step 16)',
      r'$X_t = 2r\cos(\theta_t)X_{t-1} - r^2X_{t-2} + \varepsilon_t$, $r = 0.95$, perioada vîrfului trece de la 20 la 5 pe 2048 de observații; multitaper pe ferestre de 256 (pas 16)')],
    h='0.5\\textheight')

interp(('the spectrogram', 'spectrogramei'), [
    T('The spectrogram follows the moving peak: a single spectrum of the whole sample would show a smeared band from 0.05 to 0.2 cycles',
      'Spectrograma urmărește vîrful care se deplasează: un singur spectru al întregului eșantion ar arăta o bandă estompată de la 0,05 la 0,2 cicluri'),
    T(r'Resolution $2NW/L = @{sg.res}$ cycles: fine at high frequencies, coarse for the long periods at the start',
      r'Rezoluția $2NW/L = @{sg.res}$ cicluri: bună la frecvențe înalte, grosieră pentru perioadele lungi de la început'),
    T('The first and last 128 observations have no estimate: every time--frequency method loses the edges (the cone of influence of wavelets)',
      'Primele și ultimele 128 de observații nu au estimare: orice metodă timp--frecvență pierde marginile (conul de influență al wavelets)'),
    T('Economic examples: changing business-cycle length, the shortening of trading cycles, regime changes in volatility',
      'Exemple economice: lungimea variabilă a ciclului economic, scurtarea ciclurilor de tranzacționare, schimbări de regim în volatilitate')])

D.frame(T('Singular spectrum analysis in one slide', 'Analiza spectrului singular pe un slide'), items(
    (T(r'Embed $x_1, \dots, x_n$ in the $L \times (n - L + 1)$ trajectory (Hankel) matrix $\mathbf X$; SVD $\mathbf X = \sum_i\sigma_i\mathbf u_i\mathbf v_i\'$ \refVG',
       r'Scufundăm $x_1, \dots, x_n$ în matricea traiectoriilor (Hankel) $\mathbf X$, de dimensiune $L \times (n - L + 1)$; descompunerea SVD $\mathbf X = \sum_i\sigma_i\mathbf u_i\mathbf v_i\'$ \refVG'), []),
    (T('Group eigentriples (trend: slowly varying $\\mathbf u_i$; oscillations: pairs with equal $\\sigma_i$ and shifted sines) and reconstruct each group by averaging anti-diagonals',
       'Grupăm tripletele proprii (tendința: $\\mathbf u_i$ care variază lent; oscilațiile: perechi cu $\\sigma_i$ egale și sinusoide decalate) și reconstruim fiecare grup prin medierea antidiagonalelor'), []),
    T('Data-adaptive basis instead of fixed sinusoids or wavelets; no model, no stationarity assumption; inference is less developed',
      'O bază adaptată la date în locul sinusoidelor sau al wavelets fixe; fără model și fără ipoteza de staționaritate; inferența este mai puțin dezvoltată'),
    T('A code sketch (\\texttt{ssa}) is in the Quantlet engine of this chapter; it is a natural benchmark for wavelet multiresolution',
      'O schiță de cod (\\texttt{ssa}) se află în nucleul Quantlet al capitolului; este un reper natural pentru analiza multirezoluție wavelet')), 'small')

D.recap(('Spectra that change over time', 'spectre care se schimbă în timp'), [
    T('Priestley and Dahlhaus give a meaning to a time-varying spectrum', 'Priestley și Dahlhaus dau un sens unui spectru variabil în timp'),
    T('A fixed window trades time against frequency resolution', 'O fereastră fixă schimbă rezoluția în timp pe rezoluția în frecvență'),
    T('Wavelets adapt the window to the frequency; SSA adapts the basis to the data', 'Wavelets adaptează fereastra la frecvență; SSA adaptează baza la date')])

# =============================================================================
# 6. WAVELETS: MODWT
# =============================================================================
D.section('Wavelets: decomposition by scale', 'Wavelets: descompunerea pe scale')

D.frame(T('From sinusoids to wavelets', 'De la sinusoide la wavelets'), two(
    ph('daub', T('Ingrid Daubechies, 2005', 'Ingrid Daubechies, 2005'), h='0.36\\textheight'),
    items((T(r'A \textbf{wavelet} $\psi$: a short wave, localised in time and frequency \refGM', r'Un \textbf{wavelet} $\psi$: o undă scurtă, localizată în timp și în frecvență \refGM'),
           [T(r'$\int\psi = 0$, $\int\psi^2 = 1$; admissible if $C_\psi = \int|\hat\psi(\omega)|^2/|\omega|\,d\omega < \infty$, with $\hat\psi$ the Fourier transform of $\psi$',
              r'$\int\psi = 0$, $\int\psi^2 = 1$; admisibil dacă $C_\psi = \int|\hat\psi(\omega)|^2/|\omega|\,d\omega < \infty$, cu $\hat\psi$ transformata Fourier a lui $\psi$')]),
          (T(r'Continuous wavelet transform (CWT): correlate the series with stretched and shifted copies of $\psi$', r'Transformata wavelet continuă (CWT): corelăm seria cu copii dilatate și translatate ale lui $\psi$'
             ) + r'''
    \[ W(s, \tau) = \int x(t)\,\frac{1}{\sqrt s}\,\psi^*\Big(\frac{t - \tau}{s}\Big)dt \]''',
           [T(r'$s > 0$: scale (inversely related to frequency); $\tau$: location in time; $\psi^*$: complex conjugate',
              r'$s > 0$: scala (invers legată de frecvență); $\tau$: poziția în timp; $\psi^*$: conjugatul complex')]),
          T(r'Compactly supported orthonormal wavelets \refDau and the pyramid algorithm \refMal give the DWT: $n$ coefficients for $n$ observations; applications: \refCro; \refGSWb; \refACS',
            r'Wavelets ortonormate cu suport compact \refDau și algoritmul piramidal \refMal dau DWT: $n$ coeficienți pentru $n$ observații; aplicații: \refCro; \refGSWb; \refACS')), '0.28', '0.7'), 'footnotesize')

D.frame(T('DWT, MODWT and multiresolution (1/2)', 'DWT, MODWT și analiza multirezoluție (1/2)'), items(
    (T(r'Two filters of length $L$ \refPWb', r'Două filtre de lungime $L$ \refPWb'
       ) + T(r'''
    \[ \text{scaling (low-pass): } g_l, \qquad \text{wavelet (high-pass): } h_l = (-1)^lg_{L-1-l} \]''', r'''
    \[ \text{de scalare (trece-jos): } g_l, \qquad \text{wavelet (trece-sus): } h_l = (-1)^lg_{L-1-l} \]'''),
     [T(r'Haar $L = 2$; Daubechies least-asymmetric LA(8) $L = 8$; level $j$ captures periods $[2^j, 2^{j+1}]$: an \textbf{octave} band; $J$ levels plus a smooth',
        r'Haar $L = 2$; Daubechies cel mai puțin asimetric LA(8) $L = 8$; nivelul $j$ captează perioadele $[2^j, 2^{j+1}]$: o bandă de o \textbf{octavă}; $J$ niveluri plus o componentă netedă')]),
    (T(r'\textbf{MODWT} (maximal overlap DWT): no downsampling, rescaled filters', r'\textbf{MODWT} (DWT cu suprapunere maximă): fără eșantionare redusă, cu filtre rescalate'
       ) + r'''
    \[ \tilde h = h/\sqrt2, \quad \tilde g = g/\sqrt2, \qquad \tilde W_{j,t} = \sum_l\tilde h_{j,l}X_{t-l \bmod n} \]''',
     [T(r'$\tilde h_{j,l}$: the level-$j$ wavelet filter; $\tilde W_{j,t}$: wavelet coefficient of level $j$ at time $t$; $\bmod n$: the sample is treated as circular',
        r'$\tilde h_{j,l}$: filtrul wavelet de nivel $j$; $\tilde W_{j,t}$: coeficientul wavelet de nivel $j$ la momentul $t$; $\bmod n$: eșantionul este tratat circular')])), 'small')

D.frame(T('DWT, MODWT and multiresolution (2/2)', 'DWT, MODWT și analiza multirezoluție (2/2)'), items(
    (T('MODWT properties', 'Proprietățile MODWT'),
     [T('any sample size, shift-invariant (moving the start date does not change the coefficients), $J \\times n$ coefficients',
        'orice mărime a eșantionului, invariantă la translații (mutarea datei de început nu schimbă coeficienții), $J \\times n$ coeficienți'),
      T('energy preserved: $\\|X\\|^2 = \\sum_j\\|\\tilde W_j\\|^2 + \\|\\tilde V_J\\|^2$, with $\\tilde V_J$ the scaling (smooth) coefficients',
        'energia se conservă: $\\|X\\|^2 = \\sum_j\\|\\tilde W_j\\|^2 + \\|\\tilde V_J\\|^2$, cu $\\tilde V_J$ coeficienții de scalare (netezi)')]),
    (T(r'\textbf{Multiresolution analysis (MRA)}: the series is the sum of its details and a smooth', r'\textbf{Analiza multirezoluție (MRA)}: seria este suma detaliilor și a unei componente netede'
       ) + r'''
    \[ X_t = \sum_{j=1}^J\mathcal D_{j,t} + \mathcal S_{J,t} \]''',
     [T(r'$\mathcal D_j$: the inverse MODWT of level $j$ alone; $\mathcal S_J$: the smooth; zero-phase, aligned with the data',
        r'$\mathcal D_j$: inversa MODWT a nivelului $j$ singur; $\mathcal S_J$: componenta netedă; fără defazaj, aliniate cu datele')]),
    T(r'Boundary: the first $L_j - 1 = (2^j - 1)(L - 1)$ coefficients wrap around the sample (circular filtering) and are excluded from estimation',
      r'Marginile: primii $L_j - 1 = (2^j - 1)(L - 1)$ coeficienți folosesc date de la celălalt capăt (filtrare circulară) și se exclud din estimare')), 'small')

chart(T('Wavelet filters and the Morlet wavelet', 'Filtre wavelet și wavelet-ul Morlet'), 'ats_ch11_wavelets', 'ATS_ch11_wavelets', [
    T(r'Left: squared gains of the MODWT LA(8) filters of levels 1--5; right: the Morlet wavelet $\psi_0(\eta) = \pi^{-1/4}e^{i\omega_0\eta}e^{-\eta^2/2}$, $\omega_0 = 6$',
      r'Stînga: pătratele cîștigurilor filtrelor MODWT LA(8) pentru nivelurile 1--5; dreapta: wavelet-ul Morlet $\psi_0(\eta) = \pi^{-1/4}e^{i\omega_0\eta}e^{-\eta^2/2}$, $\omega_0 = 6$')],
    h='0.48\\textheight')

interp(('the wavelet filters', 'filtrelor wavelet'), [
    T('Each MODWT level is an approximate band-pass filter for one octave; the bands overlap, so leakage between neighbouring levels is part of the design',
      'Fiecare nivel MODWT este un filtru trece-bandă aproximativ pentru o octavă; benzile se suprapun, deci leakage-ul între niveluri vecine face parte din construcție'),
    T('The bandwidth grows with frequency: fine frequency resolution for long cycles, fine time resolution for short ones',
      'Lățimea benzii crește cu frecvența: rezoluție fină în frecvență pentru ciclurile lungi, rezoluție fină în timp pentru cele scurte'),
    T(r'Morlet is complex: its modulus gives amplitude, its argument gives phase; Fourier period $= 1.033\times$ scale for $\omega_0 = 6$',
      r'Morlet este complex: modulul dă amplitudinea, argumentul dă faza; perioada Fourier $= 1{,}033\times$ scala pentru $\omega_0 = 6$'),
    T('Orthonormal filters (MODWT) serve variance decomposition and correlation by scale; the Morlet CWT serves time--frequency maps and phase',
      'Filtrele ortonormate (MODWT) servesc descompunerii varianței și corelației pe scale; CWT Morlet servește hărților timp--frecvență și fazei')])

chart(T('The BET return decomposed by scale', 'Randamentul BET descompus pe scale'), 'ats_ch11_mra', 'ATS_ch11_wavelets', [
    T(r'MODWT multiresolution analysis, LA(8), $J = 6$, daily BET returns 2000--2026 (@{mr.n} days); four of the six details and the smooth',
      r'Analiza multirezoluție MODWT, LA(8), $J = 6$, randamentele zilnice BET 2000--2026 (@{mr.n} zile); patru dintre cele șase detalii și componenta netedă')],
    h='0.68\\textheight')

interp(('the multiresolution analysis', 'analizei multirezoluție'), [
    T(r'Energy shares of levels 1--6: @{mr.s1}, @{mr.s2}, @{mr.s3}, @{mr.s4}, @{mr.s5}, @{mr.s6}\%; white noise would give @{mr.w1}, @{mr.w2}, @{mr.w3}, @{mr.w4}, @{mr.w5}, @{mr.w6}\%',
      r'Ponderile energiei pe nivelurile 1--6: @{mr.s1}, @{mr.s2}, @{mr.s3}, @{mr.s4}, @{mr.s5}, @{mr.s6}\%; un zgomot alb ar da @{mr.w1}, @{mr.w2}, @{mr.w3}, @{mr.w4}, @{mr.w5}, @{mr.w6}\%'),
    T('Less energy at the shortest scale and more at the longer ones than white noise: positive autocorrelation of BET returns at short horizons',
      'Mai puțină energie la scala cea mai scurtă și mai multă la scalele lungi decît un zgomot alb: autocorelația pozitivă a randamentelor BET la orizonturi scurte'),
    T('Volatility clustering appears at every scale in 2008 and 2020, but the slow components ($\\mathcal D_6$, $\\mathcal S_6$) move only in the 2008--2009 crisis',
      'Volatility clustering apare la toate scalele în 2008 și 2020, dar componentele lente ($\\mathcal D_6$, $\\mathcal S_6$) se mișcă doar în criza din 2008--2009'),
    T('The details add up exactly to the series: a lossless, zero-phase decomposition', 'Detaliile se adună exact la serie: o descompunere fără pierderi și fără defazaj')])

D.frame(T('Wavelet variance, correlation and beta by scale (1/2)', 'Varianța, corelația și beta wavelet pe scale (1/2)'), items(
    (T(r'\textbf{Wavelet variance}: the variance of the level-$j$ coefficients; the levels add up to the variance of the series \refPer', r'\textbf{Varianța wavelet}: varianța coeficienților de nivel $j$; nivelurile însumează varianța seriei \refPer'
       ) + r'''
    \[ \nu_X^2(\tau_j) = \Var\tilde W_{j,t}, \qquad \sum_j\nu^2_X(\tau_j) = \Var X \]''',
     [T(r'$\tau_j = 2^{j-1}$: the scale of level $j$; an octave-band version of the spectrum; white noise: $\nu^2(\tau_j) = \sigma^2/2^j$, halving at each level',
        r'$\tau_j = 2^{j-1}$: scala nivelului $j$; o versiune pe octave a spectrului; zgomot alb: $\nu^2(\tau_j) = \sigma^2/2^j$, se înjumătățește la fiecare nivel'),
      T(r'unbiased estimator: average of $\tilde W^2_{j,t}$ over the $M_j = n - L_j + 1$ non-boundary coefficients; $\eta\hat\nu^2/\nu^2 \approx \chi^2_\eta$, $\eta = \max(M_j/2^j, 1)$ equivalent degrees of freedom',
        r'estimatorul nedeplasat: media lui $\tilde W^2_{j,t}$ pe cei $M_j = n - L_j + 1$ coeficienți din afara marginilor; $\eta\hat\nu^2/\nu^2 \approx \chi^2_\eta$, cu $\eta = \max(M_j/2^j, 1)$ grade de libertate echivalente')])), 'small')

D.frame(T('Wavelet variance, correlation and beta by scale (2/2)', 'Varianța, corelația și beta wavelet pe scale (2/2)'), items(
    (T(r'\textbf{Wavelet correlation} \refWGP\ and \textbf{wavelet beta} \refGSW', r'\textbf{Corelația wavelet} \refWGP\ și \textbf{beta wavelet} \refGSW'
       ) + r'''
    \[ \rho_{XY}(\tau_j) = \frac{\Cov(\tilde W^X_j, \tilde W^Y_j)}{\nu_X(\tau_j)\nu_Y(\tau_j)} \]
    \[ \beta(\tau_j) = \frac{\Cov(\tilde W^r_j, \tilde W^m_j)}{\Var\tilde W^m_j} \]''',
     [T(r'$\tilde W^r_j$, $\tilde W^m_j$: coefficients of an asset return and of the market return; $\beta(\tau_j)$: systematic risk at the investment horizon $\tau_j$',
        r'$\tilde W^r_j$, $\tilde W^m_j$: coeficienții randamentului unui activ și ai randamentului pieței; $\beta(\tau_j)$: riscul sistematic la orizontul de investiție $\tau_j$'),
      T(r'95\% interval for the correlation: $\tanh\big(\tanh^{-1}\hat\rho \pm z/\sqrt{M_j/2^j - 3}\big)$, $z = 1.96$', r'intervalul de 95\% pentru corelație: $\tanh\big(\tanh^{-1}\hat\rho \pm z/\sqrt{M_j/2^j - 3}\big)$, $z = 1{,}96$')]),
    T('Effective sample size falls by half at each level: long-scale estimates are wide even with 25 years of daily data',
      'Mărimea efectivă a eșantionului se înjumătățește la fiecare nivel: estimările pe scale lungi sînt largi chiar și cu 25 de ani de date zilnice')), 'small')

chart(T('Wavelet variance of three equity indices', 'Varianța wavelet a trei indici bursieri'), 'ats_ch11_wvar', 'ATS_ch11_wavelets', [
    T(r'Daily log returns 2000--2026, MODWT LA(8), levels 1--8 with 95\% intervals; dashed: white noise with the same level-1 variance',
      r'Randamente logaritmice zilnice 2000--2026, MODWT LA(8), nivelurile 1--8 cu intervale de 95\%; linii întrerupte: zgomot alb cu aceeași varianță la nivelul 1')],
    h='0.5\\textheight')

interp(('the wavelet variances', 'varianțelor wavelet'), [
    T(r'Ratio of the variance at level 6 (64--128 days) to the white-noise line: BET @{wv.bet.r6}, DAX @{wv.dax.r6}, S\&P 500 @{wv.sp500.r6}',
      r'Raportul dintre varianța de la nivelul 6 (64--128 de zile) și linia zgomotului alb: BET @{wv.bet.r6}, DAX @{wv.dax.r6}, S\&P 500 @{wv.sp500.r6}'),
    T(r'BET has more long-horizon variance than its daily variance implies (level 8: @{wv.bet.r8}): momentum, a thin market; the S\&P 500 has less (@{wv.sp500.r8}): mean reversion of daily moves',
      r'BET are mai multă varianță pe orizonturi lungi decît implică varianța zilnică (nivelul 8: @{wv.bet.r8}): momentum, o piață mică; S\&P 500 are mai puțină (@{wv.sp500.r8}): revenirea la medie a mișcărilor zilnice'),
    T('This is the variance-ratio test of market efficiency, done scale by scale with valid intervals',
      'Este testul raportului varianțelor pentru eficiența pieței, făcut scală cu scală, cu intervale valide'),
    T('Risk measured on daily data and scaled by $\\sqrt{h}$ understates BET risk at long horizons', 'Riscul măsurat pe date zilnice și scalat cu $\\sqrt{h}$ subestimează riscul BET pe orizonturi lungi')])

chart(T('Co-movement by scale: BET, DAX and S\\&P 500', 'Co-mișcarea pe scale: BET, DAX și S\\&P 500'), 'ats_ch11_wcorr', 'ATS_ch11_wavelets', [
    T(r'Daily returns on @{wc.n} common trading days, MODWT LA(8); left: three pairs, 2000--2026; right: BET--DAX in two halves; 95\% Fisher-$z$ intervals',
      r'Randamente zilnice în @{wc.n} zile comune de tranzacționare, MODWT LA(8); stînga: trei perechi, 2000--2026; dreapta: BET--DAX în două jumătăți; intervale Fisher-$z$ de 95\%')],
    h='0.5\\textheight')

interp(('the wavelet correlations', 'corelațiilor wavelet'), [
    T(r'BET--DAX rises from @{wc.bet_dax.1} (2--4 days) to @{wc.bet_dax.8} (256--512 days); the daily correlation (@{wc.corr}) understates long-run integration',
      r'BET--DAX crește de la @{wc.bet_dax.1} (2--4 zile) la @{wc.bet_dax.8} (256--512 zile); corelația zilnică (@{wc.corr}) subestimează integrarea pe termen lung'),
    T(r'BET--S\&P 500 at level 1 is only @{wc.bet_sp500.1}, DAX--S\&P 500 @{wc.dax_sp500.1}: New York closes after Europe, so daily co-movement shows up a day late; it vanishes at longer scales',
      r'BET--S\&P 500 la nivelul 1 este doar @{wc.bet_sp500.1}, DAX--S\&P 500 @{wc.dax_sp500.1}: New York închide după Europa, deci co-mișcarea zilnică apare cu o zi întîrziere; dispare la scale mai lungi'),
    T(r'BET--DAX at 8--16 days: @{wc.bet_dax_2000.3} in 2000--2012 against @{wc.bet_dax_2013.3} in 2013--2026 (level 3): integration has increased at short and medium scales',
      r'BET--DAX la 8--16 zile: @{wc.bet_dax_2000.3} în 2000--2012 față de @{wc.bet_dax_2013.3} în 2013--2026 (nivelul 3): integrarea a crescut la scale scurte și medii'),
    T(r'Wavelet beta of BET on DAX: @{wc.beta.1} at level 1, @{wc.beta.6} at level 6: the diversification benefit of the BET shrinks with the horizon (\refGSW; \refRN)',
      r'Beta wavelet a BET față de DAX: @{wc.beta.1} la nivelul 1, @{wc.beta.6} la nivelul 6: beneficiul diversificării prin BET scade cu orizontul (\refGSW; \refRN)')], size='footnotesize')

D.recap(('Wavelets: decomposition by scale', 'wavelets: descompunerea pe scale'), [
    T('The MODWT splits variance and covariance into octave bands, for any $n$ and without phase shift', 'MODWT împarte varianța și covarianța pe benzi de o octavă, pentru orice $n$ și fără defazaj'),
    T('Wavelet variance is a scale-by-scale variance-ratio test; wavelet correlation and beta show integration by horizon', 'Varianța wavelet este un test al raportului varianțelor scală cu scală; corelația și beta wavelet arată integrarea pe orizonturi'),
    T('Drop boundary coefficients and use equivalent degrees of freedom for intervals', 'Excludeți coeficienții de margine și folosiți grade de libertate echivalente pentru intervale')])

# =============================================================================
# 7. COERENȚA WAVELET
# =============================================================================
D.section('Time--frequency co-movement: wavelet coherence', 'Co-mișcarea timp--frecvență: coerența wavelet')

D.frame(T('The Morlet transform and its significance (1/2)', 'Transformata Morlet și semnificația ei (1/2)'), items(
    (T(r'\refTC: the CWT computed by FFT on a grid of scales', r'\refTC: CWT calculată prin FFT pe o grilă de scale'
       ) + r'''
    \[ W_n(s) = \sum_k\hat x_k\,\hat\psi^*(s\omega_k)\,e^{i\omega_kn\delta t}, \qquad s_j = s_02^{j\delta j} \]''',
     [T(r'$\hat x_k$: the DFT of the series at frequency $\omega_k$; $\hat\psi$: the Fourier transform of the Morlet wavelet; $\delta t$: time step; $s_0$: smallest scale; $\delta j$: scale step in octaves',
        r'$\hat x_k$: DFT al seriei la frecvența $\omega_k$; $\hat\psi$: transformata Fourier a wavelet-ului Morlet; $\delta t$: pasul de timp; $s_0$: scala cea mai mică; $\delta j$: pasul scalelor, în octave'),
      T(r'wavelet power $|W_n(s)|^2$: the variance of the series at time $n$ and scale $s$', r'puterea wavelet $|W_n(s)|^2$: varianța seriei la momentul $n$ și scala $s$')]),
    (T(r'\textbf{Cone of influence} (COI): where the wavelet at scale $s$ reaches the edge, within $\sqrt2\,s$ of either end', r'\textbf{Conul de influență} (COI): zona în care wavelet-ul de scală $s$ atinge marginea, la mai puțin de $\sqrt2\,s$ de oricare capăt'),
     [T('results inside the COI are biased and are not interpreted', 'rezultatele din COI sînt deplasate și nu se interpretează')])), 'small')

D.frame(T('The Morlet transform and its significance (2/2)', 'Transformata Morlet și semnificația ei (2/2)'), items(
    (T(r'Null of red noise, an AR(1) with lag-1 autocorrelation $a$: the power is a scaled $\chi^2_2$', r'Ipoteza nulă de zgomot roșu, un AR(1) cu autocorelația de ordinul 1 egală cu $a$: puterea este o variabilă $\chi^2_2$ scalată'
       ) + r'''
    \[ \frac{|W_n(s)|^2}{\sigma^2} \sim P_k\,\frac{\chi^2_2}{2}, \qquad P_k = \frac{1 - a^2}{1 + a^2 - 2a\cos(2\pi k/N)} \]''',
     [T(r'$\sigma^2$: variance of the series; $P_k$: the red-noise spectrum at the Fourier index $k$ matching scale $s$; $N$: number of observations',
        r'$\sigma^2$: varianța seriei; $P_k$: spectrul zgomotului roșu la indicele Fourier $k$ care corespunde scalei $s$; $N$: numărul de observații')]),
    (T(r'Global wavelet spectrum: the time average of the power, a smoothed Fourier spectrum', r'Spectrul wavelet global: media în timp a puterii, un spectru Fourier netezit'
       ) + T(r'''
    \[ \bar W^2(s) = \frac1n\sum_n|W_n(s)|^2, \qquad \nu = 2\sqrt{1 + \Big(\frac{n\delta t}{2.32\,s}\Big)^2} \ \text{degrees of freedom} \]''', r'''
    \[ \bar W^2(s) = \frac1n\sum_n|W_n(s)|^2, \qquad \nu = 2\sqrt{1 + \Big(\frac{n\delta t}{2{,}32\,s}\Big)^2} \ \text{grade de libertate} \]'''),
     []),
    T(r'Rectify the power by $1/s$ when comparing scales \refLLW; the pointwise test runs at thousands of points: expect 5\% false patches \refMK',
      r'Rectificați puterea prin $1/s$ cînd comparați scalele \refLLW; testul punctual se aplică în mii de puncte: așteptați 5\% zone false \refMK')), 'small')

chart(T('Wavelet power of the BET', 'Puterea wavelet a BET'), 'ats_ch11_cwt_bet', 'ATS_ch11_wavelet_coherence', [
    T(r'Weekly BET returns (standardised), @{cw.n} weeks 2000--2026, Morlet $\omega_0 = 6$, $\delta j = 1/12$; black contours: 5\% red-noise test; hatched: cone of influence; right: global wavelet spectrum',
      r'Randamente săptămînale BET (standardizate), @{cw.n} de săptămîni 2000--2026, Morlet $\omega_0 = 6$, $\delta j = 1/12$; contururi negre: testul de 5\% față de zgomotul roșu; hașurat: conul de influență; dreapta: spectrul wavelet global')],
    h='0.48\\textheight')

interp(('the wavelet power', 'puterii wavelet'), [
    T(r'Maximum power at a period of @{cw.per} weeks on @{cw.date}: the Lehman weeks; significant power in 2007--2011 at periods of 32 to 128 weeks',
      r'Puterea maximă la perioada de @{cw.per} săptămîni, la @{cw.date}: săptămînile Lehman; putere semnificativă în 2007--2011 la perioade de 32--128 de săptămîni'),
    T(r'Lag-1 autocorrelation @{cw.ar1}: the red-noise null is almost white; @{cw.sig}\% of the reliable area is significant at 5\%',
      r'Autocorelația de ordinul 1 este @{cw.ar1}: ipoteza nulă de zgomot roșu este aproape albă; @{cw.sig}\% din aria fiabilă este semnificativă la 5\%'),
    T('Power in returns is variance, not a cycle: the map shows when volatility was concentrated at which horizons',
      'Puterea în randamente este varianță, nu un ciclu: harta arată cînd s-a concentrat volatilitatea și la ce orizonturi'),
    T('The global spectrum stays inside the red-noise band: no persistent cycle in BET returns, as efficiency predicts',
      'Spectrul global rămîne în interiorul benzii zgomotului roșu: niciun ciclu persistent în randamentele BET, cum prezice eficiența pieței')])

D.frame(T('Wavelet coherence and phase (1/2)', 'Coerența și faza wavelet (1/2)'), items(
    (T(r'Cross-wavelet transform and \textbf{squared wavelet coherence} \refTW, \refGMJ', r'Transformata wavelet încrucișată și \textbf{coerența wavelet pătratică} \refTW, \refGMJ'
       ) + r'''
    \[ W^{xy}_n(s) = W^x_n(s)W^{y*}_n(s) \]
    \[ R^2_n(s) = \frac{|\mathcal S(s^{-1}W^{xy}_n(s))|^2}{\mathcal S(s^{-1}|W^x_n(s)|^2)\,\mathcal S(s^{-1}|W^y_n(s)|^2)} \in [0, 1] \]''',
     [T(r'$\mathcal S$: smoothing, Gaussian in time (width $s$) and a boxcar of 0.6 octaves in scale; $R^2_n(s)$: a local $R^2$ at time $n$ and scale $s$',
        r'$\mathcal S$: netezirea, gaussiană în timp (lățime $s$) și o medie pe 0,6 octave în scală; $R^2_n(s)$: un $R^2$ local la momentul $n$ și scala $s$'),
      T(r'without smoothing $R^2 \equiv 1$, as for the raw coherence: smoothing is what makes it an estimator', r'fără netezire $R^2 \equiv 1$, ca pentru coerența brută: netezirea o face un estimator')])), 'small')

D.frame(T('Wavelet coherence and phase (2/2)', 'Coerența și faza wavelet (2/2)'), items(
    (T(r'Phase $\arg\mathcal S(s^{-1}W^{xy})$, shown as arrows', r'Faza $\arg\mathcal S(s^{-1}W^{xy})$, reprezentată prin săgeți'),
     [T(r'right = in phase, left = anti-phase, up = $x$ leads; lead in time = phase $\times$ period$/2\pi$',
        r'spre dreapta = în fază, spre stînga = în antifază, în sus = $x$ conduce; avansul în timp = faza $\times$ perioada$/2\pi$')]),
    (T(r'Significance by \textbf{Monte Carlo} \refGMJ', r'Semnificația prin \textbf{Monte Carlo} \refGMJ'),
     [T(r'simulate pairs of independent AR(1) series with the data\'s lag-1 autocorrelations; the 95th percentile of $R^2$ at each scale is the 5\% threshold',
        r'simulăm perechi de serii AR(1) independente cu autocorelațiile de ordinul 1 ale datelor; percentila 95 a lui $R^2$ la fiecare scală este pragul de 5\%')]),
    T(r'Extensions: partial and multiple wavelet coherence, phase differences with confidence bands \refACS; monetary policy \refAAS; energy \refVB',
      r'Extensii: coerența wavelet parțială și multiplă, diferențe de fază cu benzi de încredere \refACS; politica monetară \refAAS; energie \refVB')), 'small')

chart(T('BET and DAX in time and frequency', 'BET și DAX în timp și frecvență'), 'ats_ch11_wtc_bet_dax', 'ATS_ch11_wavelet_coherence', [
    T(r'Weekly returns 2000--2026; contours: 5\% significance from @{wd.reps} AR(1) pairs; arrows only where significant',
      r'Randamente săptămînale 2000--2026; contururi: semnificația de 5\% din @{wd.reps} de perechi AR(1); săgeți doar unde coerența este semnificativă')],
    h='0.52\\textheight')

interp(('BET--DAX coherence', 'coerenței BET--DAX'), [
    T(r'@{wd.obs}\% of the reliable area is significant (null 95th percentile @{wd.q95}\%): the co-movement is real, but concentrated',
      r'@{wd.obs}\% din aria fiabilă este semnificativă (percentila 95 sub ipoteza nulă: @{wd.q95}\%): co-mișcarea este reală, dar concentrată'),
    T(r'Average $R^2$ at 8--64 weeks: @{wd.early} in 2000--2006, @{wd.gfc} in 2008--2009, @{wd.calm} in 2014--2019, @{wd.covid} in 2020--June 2021',
      r'$R^2$ mediu la 8--64 de săptămîni: @{wd.early} în 2000--2006, @{wd.gfc} în 2008--2009, @{wd.calm} în 2014--2019, @{wd.covid} în 2020--iunie 2021'),
    T(r'Phase near zero in crises (@{wd.gfcph} rad in 2008--2009), negative before 2007 (@{wd.earlyph} rad): the DAX led the BET by weeks when the Bucharest market was young',
      r'Faza aproape zero în crize (@{wd.gfcph} rad în 2008--2009), negativă înainte de 2007 (@{wd.earlyph} rad): DAX conducea BET cu cîteva săptămîni cînd piața de la București era tînără'),
    T(r'Crises raise coherence: is it contagion or only higher volatility? Correlations rise mechanically with volatility \refFR, and so does $R^2$',
      r'Crizele cresc coerența: este contagiune sau doar volatilitate mai mare? Corelațiile cresc mecanic cu volatilitatea \refFR, la fel și $R^2$')], size='footnotesize')

chart(T('BET and S\\&P 500 in time and frequency', 'BET și S\\&P 500 în timp și frecvență'), 'ats_ch11_wtc_bet_spx', 'ATS_ch11_wavelet_coherence', [
    T(r'Weekly returns 2000--2026; Monte Carlo significance as before',
      r'Randamente săptămînale 2000--2026; semnificația Monte Carlo ca mai înainte')],
    h='0.52\\textheight')

interp(('BET--S\\&P 500 coherence', 'coerenței BET--S\\&P 500'), [
    T(r'Significant area @{ws.obs}\% (null 95th percentile @{ws.q95}\%); $R^2$ at 8--64 weeks @{ws.gfc} in 2008--2009 and @{ws.calm} in 2014--2019',
      r'Aria semnificativă @{ws.obs}\% (percentila 95 sub ipoteza nulă: @{ws.q95}\%); $R^2$ la 8--64 de săptămîni @{ws.gfc} în 2008--2009 și @{ws.calm} în 2014--2019'),
    T(r'In 2000--2006 the phase is @{ws.earlyph} rad: the S\&P 500 led by about a fifth of the cycle; in crises the markets move in phase',
      r'În 2000--2006 faza este @{ws.earlyph} rad: S\&P 500 conducea cu circa o cincime din ciclu; în crize piețele se mișcă în fază'),
    T('Weekly data remove the one-day lag of the daily wavelet correlation: frequency choice matters for lead--lag claims',
      'Datele săptămînale elimină întîrzierea de o zi din corelația wavelet zilnică: alegerea frecvenței datelor contează pentru afirmațiile despre avans și întîrziere'),
    T(r'Our picture matches the international evidence: co-movement is strongest at low frequencies and in crises \refRN',
      r'Imaginea noastră confirmă evidența internațională: co-mișcarea este cea mai puternică la frecvențe joase și în crize \refRN')])

chart(T('Oil and stocks', 'Petrolul și acțiunile'), 'ats_ch11_wtc_oil', 'ATS_ch11_wavelet_coherence', [
    T(r'Weekly returns of Brent crude oil (FRED) and the S\&P 500, 2000--2026; Monte Carlo significance from @{wo.reps} AR(1) pairs',
      r'Randamente săptămînale ale petrolului Brent (FRED) și ale S\&P 500, 2000--2026; semnificația Monte Carlo din @{wo.reps} de perechi AR(1)')],
    h='0.52\\textheight')

interp(('oil--stock coherence', 'coerenței petrol--acțiuni'), [
    T(r'Significant area @{wo.obs}\% (null 95th percentile @{wo.q95}\%): oil and stocks are linked only in episodes',
      r'Aria semnificativă @{wo.obs}\% (percentila 95 sub ipoteza nulă: @{wo.q95}\%): petrolul și acțiunile sînt legate doar în anumite episoade'),
    T(r'Before 2007: $R^2$ @{wo.early} with phase @{wo.earlyph} rad, neither in phase nor in anti-phase: a weak lead--lag link; 2008--2010: @{wo.gfc}, in phase (@{wo.gfcph} rad): a common demand shock',
      r'Înainte de 2007: $R^2$ @{wo.early}, cu faza @{wo.earlyph} rad, nici în fază, nici în antifază: o legătură slabă, de tip avans--întîrziere; 2008--2010: @{wo.gfc}, în fază (@{wo.gfcph} rad): un șoc comun de cerere'),
    T(r'2020--2021: @{wo.covid} in phase; 2022--2023: phase @{wo.warph} rad, closer to anti-phase: the energy-price shock of the war in Ukraine',
      r'2020--2021: @{wo.covid} în fază; 2022--2023: faza @{wo.warph} rad, mai aproape de antifază: șocul prețurilor energiei din timpul războiului din Ucraina'),
    T(r'The sign of the oil--stock link depends on the type of shock \refKP; wavelet phase shows the switch without identifying it',
      r'Semnul legăturii petrol--acțiuni depinde de tipul de șoc \refKP; faza wavelet arată schimbarea fără să o identifice')], size='footnotesize')

chart(T('Inflation in Romania and the euro area', 'Inflația în România și în zona euro'), 'ats_ch11_wtc_infl_ro', 'ATS_ch11_wavelet_coherence', [
    T(r'Annual HICP inflation (monthly), January 2001 -- August 2026; Monte Carlo significance against AR(1) pairs with lag-1 autocorrelation @{wi.ro.ar}',
      r'Inflația anuală HICP (lunar), ianuarie 2001 -- august 2026; semnificația Monte Carlo față de perechi AR(1) cu autocorelația de ordinul 1 egală cu @{wi.ro.ar}')],
    h='0.5\\textheight')

interp(('inflation co-movement', 'co-mișcării inflației'), [
    T(r'Romania--euro area: $R^2$ at 24--64 months @{wi.ro.pre} in 2002--2012, @{wi.ro.post} from 2015; significant area @{wi.ro.obs}\% (null 95th percentile @{wi.ro.q95}\%)',
      r'România--zona euro: $R^2$ la 24--64 de luni @{wi.ro.pre} în 2002--2012, @{wi.ro.post} din 2015; aria semnificativă @{wi.ro.obs}\% (percentila 95 sub ipoteza nulă: @{wi.ro.q95}\%)'),
    T(r'Poland: @{wi.pl.pre} and @{wi.pl.post}; simple correlations @{wi.ro.corr} (Romania) and @{wi.pl.corr} (Poland): Romanian disinflation to 2012 was domestic, the cycle since 2015 is common',
      r'Polonia: @{wi.pl.pre} și @{wi.pl.post}; corelații simple @{wi.ro.corr} (România) și @{wi.pl.corr} (Polonia): dezinflația României pînă în 2012 a fost internă, ciclul de după 2015 este comun'),
    T(r'2021--2024 surge, 12--48 months: $R^2$ @{wi.ro.surge}, phase @{wi.ro.surgeph} rad: no detectable lead, a common energy shock',
      r'Creșterea din 2021--2024, 12--48 de luni: $R^2$ @{wi.ro.surge}, faza @{wi.ro.surgeph} rad: niciun avans detectabil, un șoc energetic comun'),
    T('Annual rates overlap twelve months: short periods are smoothed away by construction; only cycles longer than a year are informative',
      'Ratele anuale se suprapun pe douăsprezece luni: perioadele scurte sînt netezite prin construcție; doar ciclurile mai lungi de un an sînt informative')], size='footnotesize')

D.recap(('Wavelet coherence', 'coerența wavelet'), [
    T('Wavelet coherence is a smoothed, time-local coherence; without smoothing it is identically one', 'Coerența wavelet este o coerență locală în timp, netezită; fără netezire este identic egală cu unu'),
    T('Test it by Monte Carlo against AR(1) pairs; read phase only inside significant regions and outside the cone of influence', 'Testați-o prin Monte Carlo față de perechi AR(1); citiți faza doar în zonele semnificative și în afara conului de influență'),
    T('Equity co-movement peaks in crises and at long horizons; oil--stock phase flips with the type of shock', 'Co-mișcarea acțiunilor este maximă în crize și pe orizonturi lungi; faza petrol--acțiuni se inversează cu tipul de șoc')])

# =============================================================================
# 8. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Is the rise of stock-market coherence in crises contagion, or the mechanical effect of higher volatility on a time-local $R^2$?',
       'Este creșterea coerenței dintre piețele bursiere în crize contagiune sau efectul mecanic al volatilității mai mari asupra unui $R^2$ local în timp?'),
     [T(r'formal: $H_0$: the wavelet coherence of BET and DAX in the pre-registered crisis windows equals its value under a model with the same time-varying volatilities and constant dependence',
        r'formal: $H_0$: coerența wavelet dintre BET și DAX în ferestrele de criză preînregistrate este egală cu valoarea ei într-un model cu aceleași volatilități variabile în timp și dependență constantă'),
      T('falsified if the crisis coherence exceeds the 95th percentile of a bootstrap from a DCC-GARCH with constant correlation (Chapter 8), at pre-registered scales',
        'infirmată dacă coerența din criză depășește percentila 95 a unui bootstrap dintr-un DCC-GARCH cu corelație constantă (Capitolul 8), la scale preînregistrate')]),
    (T('Why it matters: diversification fails when it is needed; the Forbes--Rigobon correction exists for correlations, not for wavelet coherence',
       'Miza: diversificarea eșuează tocmai cînd este nevoie de ea; corecția Forbes--Rigobon există pentru corelații, nu și pentru coerența wavelet'),
     [T(r'literature to start from: \refFR, \refRN, \refMK, \refSch, \refACS', r'literatura de pornire: \refFR, \refRN, \refMK, \refSch, \refACS')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature',
       'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers since 2009 that test wavelet coherence between stock markets against a volatility-matched null; give DOIs.} Then check every DOI on Crossref',
        r'\textbf{literatura}: \aiprompt{Listează articole recenzate din 2009 încoace care testează coerența wavelet dintre piețe bursiere față de o ipoteză nulă cu aceeași volatilitate; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Derive the bias of the smoothed wavelet coherence when both series have a common GARCH volatility and constant correlation.}',
        r'\textbf{ipoteza}: \aiprompt{Derivează deplasarea coerenței wavelet netezite cînd ambele serii au o volatilitate GARCH comună și corelație constantă.}'),
      T(r'\textbf{code and replication}: ask for the Grinsted smoothing operator, then reproduce a known case first (two AR(1) series: 5\% significant area)',
        r'\textbf{cod și replicare}: cereți operatorul de netezire Grinsted, apoi reproduceți întîi un caz cunoscut (două serii AR(1): 5\% arie semnificativă)'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee: list the ways a significant wavelet-coherence island can arise without any change in dependence.}',
        r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră felurile în care poate apărea o insulă semnificativă de coerență wavelet fără nicio schimbare a dependenței.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('Conventions: angular frequency or cycles, $2\\pi$ factors, period $=$ $1.033\\times$ scale for Morlet, the sign convention of the phase', 'Convențiile: frecvență unghiulară sau cicluri, factorii $2\\pi$, perioada $=$ $1{,}033\\times$ scala pentru Morlet, convenția de semn a fazei'),
    T('Coherence is smoothed; its threshold and the Monte Carlo null are stated; nothing is read inside the cone of influence', 'Coerența este netezită; pragul ei și ipoteza nulă Monte Carlo sînt precizate; nimic nu se interpretează în conul de influență'),
    T('Pointwise significance is not areawise significance: count how many islands the null produces', 'Semnificația punctuală nu este semnificație pe arii: numărați cîte insule produce ipoteza nulă'),
    T('Filters: gain stated; real-time and final cycles separated; results with and without extreme common shocks', 'Filtre: cîștigul precizat; ciclul în timp real separat de cel final; rezultate cu și fără șocurile comune extreme')), 'small')

chart(T('Mini-case: how many islands does chance produce?', 'Mini studiu de caz: cîte insule produce întîmplarea?'), 'ats_ch11_ai_case', 'ATS_ch11_wavelet_coherence', [
    T(r'Share of the reliable time--period area of a wavelet-coherence map that is pointwise significant at 5\%: @{ai.reps} new pairs of independent AR(1) series with the BET and DAX autocorrelations, and the observed BET--DAX map',
      r'Ponderea ariei timp--perioadă fiabile dintr-o hartă de coerență wavelet care este semnificativă punctual la 5\%: @{ai.reps} de perechi noi de serii AR(1) independente, cu autocorelațiile BET și DAX, și harta observată BET--DAX'),
    T(r'Null: mean @{ai.mean}\%, 95th percentile @{ai.q95}\%, maximum @{ai.max}\%; @{ai.any}\% of null maps contain significant islands; BET--DAX: @{ai.obs}\%. An AI summary that reads every island as a contagion episode is wrong; the overall excess is real',
      r'Ipoteza nulă: media @{ai.mean}\%, percentila 95 @{ai.q95}\%, maximum @{ai.max}\%; @{ai.any}\% din hărțile nule conțin insule semnificative; BET--DAX: @{ai.obs}\%. Un rezumat AI care citește fiecare insulă ca un episod de contagiune greșește; surplusul total este real')],
    h='0.42\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Contagion or volatility? Wavelet coherence of Central and Eastern European stock markets under a volatility-matched null}',
       r'\textbf{Contagiune sau volatilitate? Coerența wavelet a piețelor bursiere din Europa Centrală și de Est sub o ipoteză nulă cu aceeași volatilitate}'),
     [T(r'replicate: the Monte Carlo test of \refGMJ and the international co-movement maps of \refRN on BET, WIG20, BUX, PX against the DAX',
        r'replicați: testul Monte Carlo al lui \refGMJ și hărțile de co-mișcare internațională ale lui \refRN pe BET, WIG20, BUX, PX față de DAX'),
      T('extend: a DCC-GARCH bootstrap null (constant dependence, time-varying volatility); areawise tests \\refSch; partial coherence controlling for the S\\&P 500 \\refACS',
        'extindeți: o ipoteză nulă bootstrap dintr-un DCC-GARCH (dependență constantă, volatilitate variabilă); teste pe arii \\refSch; coerență parțială controlînd pentru S\\&P 500 \\refACS'),
      T('pre-register: markets, sampling frequency, crisis windows, scales, the null model and the number of replications',
        'preînregistrați: piețele, frecvența datelor, ferestrele de criză, scalele, modelul nul și numărul de replicări')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('The spectrum decomposes variance by frequency; filters act on it through their squared gain', 'Spectrul descompune varianța pe frecvențe; filtrele acționează asupra lui prin pătratul cîștigului'),
    T('Estimation is a bias--variance choice; multitaper gives low leakage, stable variance and honest bands', 'Estimarea este o alegere deplasare--varianță; multitaper dă leakage mic, varianță stabilă și benzi corecte'),
    T('Coherence, phase, dynamic correlation and Breitung--Candelon tests describe co-movement and causality by frequency', 'Coerența, faza, corelația dinamică și testele Breitung--Candelon descriu co-mișcarea și cauzalitatea pe frecvențe'),
    T('A business cycle is whatever the filter\'s gain lets through; HP adds spurious cycles and fails in real time', 'Un ciclu economic este ceea ce lasă să treacă cîștigul filtrului; HP adaugă cicluri false și eșuează în timp real'),
    T('Wavelets localise variance and co-movement in time and scale; significance needs Monte Carlo and areawise thinking', 'Wavelets localizează varianța și co-mișcarea în timp și pe scale; semnificația cere Monte Carlo și o judecată pe arii')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('Why is the periodogram inconsistent although it is asymptotically unbiased?', 'De ce este periodograma inconsistentă, deși este asimptotic nedeplasată?'),
        T('How does the optimal bandwidth grow with $n$ for a kernel with $q = 2$?', 'Cum crește lățimea de bandă optimă cu $n$ pentru un nucleu cu $q = 2$?'),
        T('Why is raw (unsmoothed) coherence always equal to one?', 'De ce este coerența brută (nenetezită) întotdeauna egală cu unu?'),
        T('Where does the peak of the HP cycle of a random walk come from?', 'De unde provine vîrful ciclului HP al unui mers aleator?'),
        T('Why is the MODWT preferred to the DWT for wavelet variance?', 'De ce este preferată MODWT față de DWT pentru varianța wavelet?'))),
    block(T('Next: Chapter 12', 'Urmează: Capitolul 12'), items(
        T('Machine learning and deep learning for time series', 'Machine learning și deep learning pentru serii de timp'),
        T('global models, leakage-free validation, deep architectures', 'modele globale, validare fără leakage, arhitecturi deep'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the distribution of the periodogram', 'Anexă: distribuția periodogramei'), items(
    T(r'Gaussian white noise: $a_j = \sqrt{2/n}\sum_tx_t\cos(\omega_jt)$, $b_j = \sqrt{2/n}\sum_tx_t\sin(\omega_jt)$ are i.i.d.\ $N(0, \sigma^2)$ for $0 < \omega_j < \pi$ (orthogonality of the Fourier basis)',
      r'Zgomot alb gaussian: $a_j = \sqrt{2/n}\sum_tx_t\cos(\omega_jt)$, $b_j = \sqrt{2/n}\sum_tx_t\sin(\omega_jt)$ sînt i.i.d.\ $N(0, \sigma^2)$ pentru $0 < \omega_j < \pi$ (ortogonalitatea bazei Fourier)'),
    T(r'$I(\omega_j) = (a_j^2 + b_j^2)/(4\pi) = \frac{\sigma^2}{2\pi}\cdot\frac{\chi^2_2}{2}$: mean $f = \sigma^2/(2\pi)$, variance $f^2$, whatever $n$',
      r'$I(\omega_j) = (a_j^2 + b_j^2)/(4\pi) = \frac{\sigma^2}{2\pi}\cdot\frac{\chi^2_2}{2}$: media $f = \sigma^2/(2\pi)$, varianța $f^2$, oricare ar fi $n$'),
    T(r'Linear process: $d_X(\omega_j) = \Psi(e^{-i\omega_j})d_\varepsilon(\omega_j) + o_p(1)$, so $I_X(\omega_j) \approx |\Psi(e^{-i\omega_j})|^2I_\varepsilon(\omega_j) = f(\omega_j)\chi^2_2/2$',
      r'Proces liniar: $d_X(\omega_j) = \Psi(e^{-i\omega_j})d_\varepsilon(\omega_j) + o_p(1)$, deci $I_X(\omega_j) \approx |\Psi(e^{-i\omega_j})|^2I_\varepsilon(\omega_j) = f(\omega_j)\chi^2_2/2$'),
    T(r'Averaging $L$ such ordinates: mean $f$, variance $f^2/L$; this is the logic of every smoothed and multitaper estimator',
      r'Medierea a $L$ astfel de ordonate: media $f$, varianța $f^2/L$; aceasta este logica oricărui estimator netezit sau multitaper')), 'small')

D.frame(T('Appendix: two filter facts', 'Anexă: două proprietăți ale filtrelor'), items(
    T(r'\textbf{Coherence is filter-invariant}: $\tilde x = A(L)x$, $\tilde y = B(L)y$ give $f_{\tilde x\tilde y} = A(\omega)\overline{B(\omega)}f_{xy}$, $f_{\tilde x} = |A|^2f_x$, $f_{\tilde y} = |B|^2f_y$, so $\kappa^2_{\tilde x\tilde y} = \kappa^2_{xy}$ where $A, B \ne 0$',
      r'\textbf{Coerența este invariantă la filtrare}: $\tilde x = A(L)x$, $\tilde y = B(L)y$ dau $f_{\tilde x\tilde y} = A(\omega)\overline{B(\omega)}f_{xy}$, $f_{\tilde x} = |A|^2f_x$, $f_{\tilde y} = |B|^2f_y$, deci $\kappa^2_{\tilde x\tilde y} = \kappa^2_{xy}$ acolo unde $A, B \ne 0$'),
    T(r'The phase changes by $\arg A - \arg B$: prewhitening with different filters shifts the phase; use the same filter on both series',
      r'Faza se schimbă cu $\arg A - \arg B$: o prealbire cu filtre diferite mută faza; folosiți același filtru pentru ambele serii'),
    T(r'\textbf{HP cycle of a random walk}: $\Delta y = \varepsilon$, so $f_c(\omega) = G(\omega)^2\sigma^2/(2\pi\cdot2(1 - \cos\omega))$; with $u = 1 - \cos\omega$ this is proportional to $u^3/(1 + 4\lambda u^2)^2$',
      r'\textbf{Ciclul HP al unui mers aleator}: $\Delta y = \varepsilon$, deci $f_c(\omega) = G(\omega)^2\sigma^2/(2\pi\cdot2(1 - \cos\omega))$; cu $u = 1 - \cos\omega$, aceasta este proporțională cu $u^3/(1 + 4\lambda u^2)^2$'),
    T(r'Setting the derivative to zero: $3(1 + 4\lambda u^2) = 16\lambda u^2$, so $u^* = \sqrt{3/(4\lambda)}$ and the period $2\pi/\arccos(1 - u^*)$',
      r'Anulînd derivata: $3(1 + 4\lambda u^2) = 16\lambda u^2$, deci $u^* = \sqrt{3/(4\lambda)}$, iar perioada este $2\pi/\arccos(1 - u^*)$')), 'small')

D.references(bib(), per=16)

if __name__ == '__main__':
    finalize(D.write(V))
