r"""
build_chapter1.py -- Capitolul 1 (Evaluarea prognozelor, reguli de scor și combinarea prognozelor), EN + RO
==========================================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_01/ch1_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice). Capitol nou: TSA, capitolele 0 și 4 au predat MAE, RMSE, MASE,
validarea încrucișată pe serii de timp și testul Diebold--Mariano de bază; aici construim pe ele.
Ieșire:
  EN/Courses/chapter1_forecast_evaluation.tex
  RO/Cursuri/capitol1_evaluarea_prognozelor.tex
Rulare:
  python3 Quantlets/Ch_01/generate_all_charts.py
  python3 latex/build_chapter1.py && python3 latex/ats_build.py compile 1
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch1_common import REFS, QLURL, T, bib, finalize, load, minus_fix, pv, quarter, month, date   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(1, 'lecture', refs=REFS)
C = 'https://commons.wikimedia.org/wiki/File:'
P = V.put


def ql(folder):
    return f'\\quantlet{{{folder.replace("_", chr(92) + "_")}}}{{\\qlurl{{{folder}}}}}'


def chart(title, fig, folder, bullets, h='0.58\\textheight', size='footnotesize'):
    body = (f'\\begin{{center}}\n\\includegraphics[width=0.97\\textwidth,height={h},keepaspectratio]{{{fig}.pdf}}\n'
            f'\\end{{center}}\n\\vspace{{-0.25cm}}\n' + items(*bullets) + '\n' + ql(folder))
    D.frame(title, body, size)


def interp(title, bullets, size='small'):
    D.frame(T(f'Interpreting {title[0]}', f'Interpretarea {title[1]}'), items(*bullets), size)


FOTO = T('Photo', 'Foto')
PD = T('public domain', 'domeniu public')
PH = {
    'fitzroy': ('ch1_fitzroy_1910.jpg', C + 'Robert_Fitzroy.jpg', T('Portrait', 'Portret') + ': Charles Hemus (c.\\ 1910); ' + PD + '; Wikimedia Commons'),
    'richardson': ('ch1_richardson.png', C + 'Lewis_Fry_Richardson.png', FOTO + ': NOAA; ' + PD + '; Wikimedia Commons'),
    'granger': ('ch1_granger_2008.jpg', C + 'Clive_Granger_by_Olaf_Storbeck.jpg', FOTO + ': Olaf Storbeck (2008); CC BY-SA 2.0; Wikimedia Commons'),
    'fed': ('ch1_fed_philadelphia_2013.jpg', C + 'Federal_Reserve_Bank_Building_Philadelphia.jpg', FOTO + ': Beyond My Ken (2013); CC BY-SA 4.0; Wikimedia Commons'),
    'pylon': ('ch1_pylon_predelus_2018.jpg', C + 'Delta_pylon_Pasul_Predelu\\%C8\\%99_RO_2018_-_1.jpg', FOTO + ': Drprv (2018); CC BY-SA 3.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


# =============================================================================
# CIFRE
# =============================================================================
L = N['loss']
P('l.mean', L['mean'], 2)
P('l.q90', L['q90'], 2)
P('l.s', L['sigma'], 1)
PI = N['pit']
P('pit.tail.sharp', 100 * PI['too sharp']['share_tails'], 0)
P('pit.tail.wide', 100 * PI['too wide']['share_tails'], 1)
P('pit.tail.ideal', 100 * PI['ideal']['share_tails'], 0)
for k, tag in [('ideal', 'id'), ('too sharp', 'sh'), ('too wide', 'wi'), ('biased', 'bi')]:
    P(f'pit.{tag}.crps', PI[k]['crps'], 3)
    P(f'pit.{tag}.logs', PI[k]['logs'], 3)
G = N['dgt']
V.int('dgt.n', G['n_eval'])
for k, tag in [('iid Normal', 'iid'), ('GARCH-N', 'gn'), ('GARCH-t', 'gt')]:
    g = G[k]
    P(f'dgt.{tag}.lr', g['berk_lr'], 1)
    V.raw(f'dgt.{tag}.p', pv(g['berk_p']))
    P(f'dgt.{tag}.sig', g['berk_sigma'], 2)
    P(f'dgt.{tag}.tails', 100 * g['tails'], 1)
    P(f'dgt.{tag}.logs', g['logs'], 3)
    P(f'dgt.{tag}.crps', g['crps'], 3)
P('dgt.nu', G['GARCH-t']['nu'], 1)
P('dgt.ab', G['GARCH-t']['params'][3] + G['GARCH-t']['params'][4], 3)
P('dgt.th', G['GARCH-t']['params'][1], 3)
for a, b, tag in [('GARCH-t', 'GARCH-N', 'tn'), ('GARCH-N', 'iid Normal', 'ni'), ('GARCH-t', 'iid Normal', 'ti')]:
    P(f'dgt.ls.{tag}', G[f'ls_{a}_{b}']['hln'], 1)
    P(f'dgt.cr.{tag}', G[f'crps_{a}_{b}']['hln'], 1)
PO = N['pool']
P('pool.w1', PO['GARCH-t|iid Normal']['w_opt'], 2)
P('pool.ls1', PO['GARCH-t|iid Normal']['ls_opt'], 4)
P('pool.lsa', PO['GARCH-t|iid Normal']['ls_a'], 4)
P('pool.w2', PO['GARCH-t|GARCH-N']['w_opt'], 2)
RI = N['roinf']
V.raw('ri.n', str(RI['n']))
V.raw('ri.first', month(RI['first']))
V.raw('ri.last', month(RI['last']))
for k in ('rw', 'ar', 'target_fc', 'comb'):
    P(f'ri.rmse.{k}', RI[f'rmse_{k}'], 2)
for k in ('ar', 'target_fc', 'comb'):
    P(f'ri.dm.{k}', RI[f'dm_{k}']['dm'], 2)
    P(f'ri.hln.{k}', RI[f'dm_{k}']['hln'], 2)
    V.raw(f'ri.p.{k}', pv(RI[f'dm_{k}']['p_hln']))
    P(f'ri.nw.{k}', RI[f'dmnw_{k}']['hln'], 2)
    V.raw(f'ri.pabs.{k}', pv(RI[f'dmabs_{k}']['p_hln']))
P('ri.gw', RI['gw']['stat'], 2)
V.raw('ri.gwp', pv(RI['gw']['p']))
P('ri.pre', RI['sub_pre2021'], 2)
P('ri.post', RI['sub_post2021'], 2)
P('ri.lasty', RI['last_y'], 1)
DS = N['dmsize']
for h in (1, 4, 8):
    for Tn in (16, 32, 64, 256):
        P(f'ds.{h}.{Tn}.dm', 100 * DS[f'{h}_{Tn}']['dm'], 1)
        P(f'ds.{h}.{Tn}.hln', 100 * DS[f'{h}_{Tn}']['hln'], 1)
V.int('ds.reps', DS['reps'])
AO = N['ao']
V.raw('ao.n', str(AO['n']))
V.raw('ao.first', quarter(AO['first']))
V.raw('ao.last', quarter(AO['last']))
P('ao.rn', AO['rmse_naive'], 2)
P('ao.rp', AO['rmse_pc'], 2)
P('ao.ratio', AO['ratio'], 2)
P('ao.hln', AO['dm']['hln'], 2)
V.raw('ao.p', pv(AO['dm']['p_hln']))
P('ao.gw', AO['gw']['stat'], 2)
V.raw('ao.gwp', pv(AO['gw']['p']))
P('ao.gwu', AO['gw_u']['stat'], 2)
V.raw('ao.gwup', pv(AO['gw_u']['p']))
V.raw('ao.encn', pv(AO['enc_naive']['p_one']))
V.raw('ao.encp', pv(AO['enc_pc']['p_one']))
for a in ('1985', '2008', '2020'):
    P(f'ao.r{a}', AO[f'ratio_{a}'], 2)
P('ao.relmax', AO['rel_max'], 1)
V.raw('ao.relmaxd', quarter(AO['rel_max_d']))
FX = N['fx']
V.raw('fx.n', str(FX['n']))
V.raw('fx.first', month(FX['first']))
V.raw('fx.last', month(FX['last']))
P('fx.rmse', FX['rmse_rw'], 2)
FXM = [('drift', 'drift', 'deriva'), ('AR(1)', 'AR(1)', 'AR(1)'), ('AR(4)', 'AR(4)', 'AR(4)'),
       ('UIP regression', 'UIP regression', 'regresia UIP'), ('UIP imposed', 'UIP imposed', 'UIP impusă'),
       ('momentum', 'momentum', 'momentum'), ('average', 'average', 'media modelelor')]
for i, (k, _, _) in enumerate(FXM):
    P(f'fx.{i}.rel', FX[k]['rel_rmse'], 3)
    P(f'fx.{i}.dm', FX[k]['dm']['hln'], 2)
    if 'cw' in FX[k]:
        P(f'fx.{i}.cw', FX[k]['cw']['cw'], 2)
        V.raw(f'fx.{i}.cwp', pv(FX[k]['cw']['p']))
    else:
        V.raw(f'fx.{i}.cw', '--')
        V.raw(f'fx.{i}.cwp', '--')
for k in ('lower', 'consistent', 'upper'):
    P(f'fx.spa.{k}', FX['spa'][k], 2)
V.raw('fx.spa.k', str(FX['spa']['k']))
LO = N['load']
V.raw('lo.n', str(LO['n_days']))
V.raw('lo.first', date(LO['first']))
V.raw('lo.last', date(LO['last']))
P('lo.mean', LO['mean_load'], 2)
P('lo.max', LO['max_load'], 2)
LN = [('naive day', 'naive (day $d$)', 'naiv (ziua $d$)'), ('naive week', 'weekly naive', 'naiv săptămînal'),
      ('mean 4 weeks', 'mean of 4 weeks', 'media pe 4 săptămîni'), ('expert ARX', 'expert ARX', 'ARX expert'),
      ('ARX + mean 4 weeks', 'ARX + mean of 4 weeks', 'ARX + media pe 4 săptămîni')]
for i, (k, _, _) in enumerate(LN):
    P(f'lo.{i}.pin', 1000 * LO['pin'][k], 0)
    P(f'lo.{i}.mae', 1000 * LO['mae'][k], 0)
    P(f'lo.{i}.cov', 100 * LO['cov90'][k], 1)
    V.raw(f'lo.{i}.mcs', pv(LO['mcs_pin']['p'][k]) if LO['mcs_pin']['p'][k] < 1 else '⁅1.000⁆')
P('lo.dmc', LO['dm_arx_comb']['hln'], 1)
P('lo.dmw', LO['dm_arx_week']['hln'], 1)
V.raw('lo.worst', ', '.join(date(d) for d in LO['worst_days'][:3]))
PZ = N['puzzle']
P('pz.w1', PZ['1.1_0.5']['w_opt'], 2)
P('pz.pop1', PZ['1.1_0.5']['pop'], 3)
P('pz.r10', PZ['1.1_0.5']['ratios']['10'], 2)
P('pz.r40', PZ['1.1_0.5']['ratios']['40'], 3)
P('pz.w2', PZ['1.5_0.5']['w_opt'], 2)
P('pz.pop2', PZ['1.5_0.5']['pop'], 3)
P('pz.r2_10', PZ['1.5_0.5']['ratios']['10'], 2)
P('pz.r2_40', PZ['1.5_0.5']['ratios']['40'], 3)
P('pz.w3', PZ['4.0_0.3']['w_opt'], 2)
P('pz.pop3', PZ['4.0_0.3']['pop'], 2)
V.int('pz.reps', PZ['reps'])
SP = N['spf']
V.raw('sp.n', str(SP['n']))
V.raw('sp.first', quarter(SP['first']))
V.raw('sp.last', quarter(SP['last']))
V.raw('sp.nf', str(SP['n_forecasters']))
P('sp.panel', SP['avg_panel'], 0)
P('sp.ok', SP['avg_ok'], 0)
P('sp.rmse', SP['rmse']['mean'], 2)
for i, s in enumerate(['median', 'trimmed 10%', 'mean of eligible', 'shrink 0.50', 'shrink 1.00', 'previous best']):
    P(f'sp.{i}.rel', SP['rel'][s], 3)
    P(f'sp.{i}.dm', SP[f'dm_{s}']['hln'], 2)
    V.raw(f'sp.{i}.p', pv(SP[f'dm_{s}']['p_hln']))
P('sp.mza', SP['mz']['a'], 2)
P('sp.mzb', SP['mz']['b'], 2)
P('sp.mzsb', SP['mz']['se_b'], 2)
V.raw('sp.mzp', pv(SP['mz']['p']))
P('sp.mzr2', SP['mz']['r2'], 3)
V.raw('sp.indn', str(SP['ind_n']))
P('sp.indbeat', 100 * SP['ind_share_beat'], 0)
P('sp.indmed', SP['ind_median'], 2)
AI = N['ai']
for per in ('1990_2007', '2008_2019', '2020_2025', '1990_2025'):
    for l in ('0.00', '1.00'):
        P(f'ai.{per}.{l}', AI[per][l], 3)
    V.raw(f'ai.{per}.n', str(AI[per]['n']))
V.raw('ai.p1', pv(AI['dm_1.00']['p_hln']))
P('ai.h1', AI['dm_1.00']['hln'], 2)
RT = N['rt']
V.raw('rt.n', str(RT['n']))
P('rt.mean', RT['mean_rev'], 2)
P('rt.sd', RT['sd_rev'], 2)
P('rt.mad', RT['mad_rev'], 2)
P('rt.corr', RT['corr'], 3)
P('rt.rf', RT['rmse_first'], 2)
P('rt.rl', RT['rmse_latest'], 2)
V.raw('rt.nspf', str(RT['n_spf']))
P('rt.bf', RT['mz_first']['b'], 2)
P('rt.bl', RT['mz_latest']['b'], 2)
V.raw('rt.big0', quarter(RT['big'][0][0]))
P('rt.big0v', RT['big'][0][1], 1)
V.raw('rt.big1', quarter(RT['big'][1][0]))
P('rt.big1v', RT['big'][1][1], 1)
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T('\\textbf{Question}: when is one forecast \\emph{really} better than another, and what do we gain by combining them?',
       '\\textbf{Întrebarea}: cînd este o prognoză \\emph{cu adevărat} mai bună decît alta și ce cîștigăm combinîndu-le?'),
     [T('``better\'\' needs a loss or a score, a reference distribution of the comparison and an honest evaluation design',
        '„mai bună” cere o funcție de pierdere sau un scor, o distribuție de referință pentru comparație și un plan de evaluare corect, fixat dinainte')]),
    (T('\\textbf{Route} of the chapter', '\\textbf{Traseul} capitolului'),
     [T('point forecasts: which functional a loss function rewards (consistency, Bregman losses)', 'prognoze punctuale: ce funcțională răsplătește o funcție de pierdere (consistență, pierderi Bregman)'),
      T('probabilistic forecasts: calibration, sharpness, PIT, proper scoring rules, elicitability', 'prognoze probabilistice: calibrare, sharpness, PIT, reguli de scor proprii, elicitabilitate'),
      T('comparing forecasts: DM with HAC and small-sample corrections, GW, Clark--West, MZ, encompassing, RC, SPA, MCS', 'compararea prognozelor: DM cu HAC și corecții de eșantion mic, GW, Clark--West, MZ, încadrare, RC, SPA, MCS'),
      T('combination: Bates--Granger, the combination puzzle, density pools, the M4 and M5 lessons; real-time data', 'combinare: Bates--Granger, paradoxul combinării, combinarea densităților, lecțiile M4 și M5; date în timp real')]),
    T('We build on TSA, Chapter 0 and TSA, Chapter 4 (MAE, RMSE, MASE, rolling-origin evaluation, the basic DM test) and on Chapter 0 (HAC, bootstrap); Seminar 1 comes before this lecture',
      'Pornim de la TSA, Capitolul 0 și TSA, Capitolul 4 (MAE, RMSE, MASE, evaluarea cu origine mobilă, testul DM de bază) și de la Capitolul 0 (HAC, bootstrap); Seminarul 1 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Derive the optimal point forecast under squared, absolute, pinball and asymmetric losses, and recognise the losses consistent for the mean (Bregman)',
      'Deduceți prognoza punctuală optimă pentru pierderile pătratică, absolută, pinball și asimetrice și recunoașteți pierderile consistente pentru medie (Bregman)'),
    T('Assess the calibration of density forecasts with PIT histograms and tests, and rank them with proper scores (log score, CRPS, interval and energy scores)',
      'Evaluați calibrarea prognozelor de densitate cu histograme PIT și teste și ierarhizați-le cu scoruri proprii (scorul logaritmic, CRPS, scorul de interval și energy score)'),
    T('Explain elicitability and why VaR is elicitable while ES is elicitable only jointly with VaR',
      'Explicați elicitabilitatea și de ce VaR este elicitabil, iar ES este elicitabil doar împreună cu VaR'),
    T('Test equal predictive ability correctly: DM--HLN with HAC variance, GW, Clark--West for nested models, MZ, encompassing, SPA and the MCS',
      'Testați corect egalitatea capacității predictive: DM--HLN cu varianță HAC, GW, Clark--West pentru modele imbricate, MZ, încadrare, SPA și MCS'),
    T('Combine point and density forecasts and explain the forecast combination puzzle; evaluate forecasts with real-time data',
      'Combinați prognoze punctuale și de densitate și explicați paradoxul combinării prognozelor; evaluați prognoze cu date în timp real')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T('Surveys: \\refPetro\\ (open access), \\refGK, \\refET, \\refTim, \\refWHLK', 'Sinteze: \\refPetro\\ (acces liber), \\refGK, \\refET, \\refTim, \\refWHLK'),
     [T('textbooks: \\refHam, Ch.~4 (forecasting); \\refKL; bridge: \\refHP', 'manuale: \\refHam, cap.~4 (prognoza); \\refKL; legătura cu licența: \\refHP')]),
    (T('Python Quantlets of this chapter: \\href{' + QLURL + '}{Quantlets/Ch\\_01}', 'Quantlet-urile Python ale capitolului: \\href{' + QLURL + '}{Quantlets/Ch\\_01}'),
     [T('DM--HLN, GW, Clark--West, MZ, encompassing, Berkowitz, CRPS and the MCS written out in \\texttt{numpy}; Hansen\'s SPA from the \\texttt{arch} package',
        'DM--HLN, GW, Clark--West, MZ, încadrare, Berkowitz, CRPS și MCS scrise explicit în \\texttt{numpy}; SPA a lui Hansen din pachetul \\texttt{arch}')]),
    T('Lecture notebook: \\href{\\colaburl{notebooks/EN/chapter1_lecture_notebook.ipynb}}{open in Google Colab}',
      'Notebook-ul cursului: \\href{\\colaburl{notebooks/EN/chapter1_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

TB = '>{\\raggedright\\arraybackslash}'
D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{4.2cm}' + TB + 'p{4.6cm}' + TB + 'p{2.6cm}',
    T('\\textbf{Series}', '\\textbf{Seria}') + ' & ' + T('\\textbf{Source}', '\\textbf{Sursa}') + ' & ' + T('\\textbf{Use}', '\\textbf{Utilizare}'),
    [T('HICP inflation, Romania (y/y, monthly)', 'Inflația IAPC, România (anuală, lunar)') + ' & Eurostat (prc\\_hicp\\_minr) & DM, GW',
     T('CPI and unemployment, US (quarterly)', 'IPC și șomajul, SUA (trimestrial)') + ' & FRED (CPIAUCSL, UNRATE) & ' + T('Atkeson--Ohanian', 'Atkeson--Ohanian'),
     T('EUR/RON and 3-month rates RO, EA (monthly)', 'EUR/RON și dobînzile la 3 luni RO, ZE (lunar)') + ' & ' + T('BNR reference rate; Eurostat (irt\\_st\\_m)', 'cursul de referință BNR; Eurostat (irt\\_st\\_m)') + ' & Clark--West, SPA',
     T('S\\&P 500, daily close', 'S\\&P 500, închidere zilnică') + ' & EODHD & ' + T('PIT, scores', 'PIT, scoruri'),
     T('Electricity load, Romania (hourly)', 'Consumul de electricitate, România (orar)') + ' & ' + T('Energy-Charts (Fraunhofer ISE), ENTSO-E data', 'Energy-Charts (Fraunhofer ISE), date ENTSO-E') + ' & ' + T('pinball, MCS', 'pinball, MCS'),
     T('Individual forecasts, US SPF', 'Prognoze individuale, SPF din SUA') + ' & ' + T('Federal Reserve Bank of Philadelphia', 'Federal Reserve Bank of Philadelphia') + ' & ' + T('combination', 'combinare'),
     T('US real GDP, all releases', 'PIB real SUA, toate versiunile publicate') + ' & ' + T('Philadelphia Fed, RTDSM', 'Philadelphia Fed, RTDSM') + ' & ' + T('real time', 'timp real')],
    size='scriptsize') + items(
    T('All sources are public and need no account or key; daily and monthly data up to September 2026',
      'Toate sursele sînt publice și nu cer cont sau cheie; datele zilnice și lunare merg pînă în septembrie 2026'),
    T('HICP: harmonised index of consumer prices; CPI: consumer price index; SPF: Survey of Professional Forecasters; RTDSM: Real-Time Data Set for Macroeconomists',
      'IAPC (HICP): indicele armonizat al prețurilor de consum; IPC (CPI): indicele prețurilor de consum; SPF: Survey of Professional Forecasters; RTDSM: Real-Time Data Set for Macroeconomists')), 'footnotesize')

D.frame(T('From weather forecasts to forecast verification', 'De la prognoza vremii la verificarea prognozelor'), two(
    ph('fitzroy', T('Robert FitzRoy (1805--1865)', 'Robert FitzRoy (1805--1865)'), h='0.27\\textheight') + '\\\\[1mm]'
    + ph('richardson', T('Lewis Fry Richardson (1881--1953)', 'Lewis Fry Richardson (1881--1953)'), h='0.22\\textheight'),
    items((T('1861: FitzRoy, head of the new Meteorological Office, publishes daily ``forecasts\'\' in The Times', '1861: FitzRoy, conducătorul noului Meteorological Office, publică zilnic „prognoze” în The Times'),
           [T('he coined the word in its modern sense; the forecasts were often wrong and publicly mocked', 'el a dat cuvîntului sensul modern; prognozele greșeau des și erau ironizate public')]),
          T('1922: Richardson computes a weather forecast by numerical integration of the equations of motion, by hand', '1922: Richardson calculează o prognoză meteo prin integrarea numerică a ecuațiilor de mișcare, de mînă'),
          (T('1950: \\refBrier\\ proposes a score for probability forecasts of rain; meteorology leads forecast verification for the next fifty years', '1950: \\refBrier\\ propune un scor pentru prognozele probabilistice de ploaie; meteorologia conduce verificarea prognozelor în următorii cincizeci de ani'),
           [T('economics adopts the same tools late: PIT \\refDGT, proper scores \\refGRa, calibration \\refGBR', 'economia adoptă aceleași instrumente tîrziu: PIT \\refDGT, scoruri proprii \\refGRa, calibrare \\refGBR')]),
          T('Lesson: a forecast is only as useful as the way we evaluate it', 'Lecția: o prognoză este utilă doar în măsura în care știm să o evaluăm')), '0.36', '0.62'), 'footnotesize')

# =============================================================================
# 1. PIERDERI
# =============================================================================
D.section('Point forecasts and loss functions', 'Prognoze punctuale și funcții de pierdere')

D.frame(T('Setting and notation', 'Cadrul și notațiile'), items(
    (T('Target $Y_{t+h}$, information set $\\mathcal{F}_t$, horizon $h$; a \\textbf{point forecast} $\\hat y_{t+h|t}$ is $\\mathcal{F}_t$-measurable', 'Ținta $Y_{t+h}$, mulțimea de informații $\\mathcal{F}_t$, orizontul $h$; o \\textbf{prognoză punctuală} $\\hat y_{t+h|t}$ este măsurabilă în raport cu $\\mathcal{F}_t$'),
     [T('$\\mathcal{F}_t$-measurable: computed only from information available at $t$', 'măsurabilă în raport cu $\\mathcal{F}_t$: calculată doar din informația disponibilă la momentul $t$'),
      T('a \\textbf{probabilistic forecast} is a predictive distribution $F_{t+h|t}$ (density, quantiles, interval, ensemble)', 'o \\textbf{prognoză probabilistică} este o distribuție predictivă $F_{t+h|t}$ (densitate, cuantile, interval, ansamblu)')]),
    (T('Out-of-sample design: $R$ observations to estimate, $P$ forecasts to evaluate, $R + P + h - 1 = T$', 'Plan în afara eșantionului: $R$ observații pentru estimare, $P$ prognoze pentru evaluare, $R + P + h - 1 = T$'),
     [T('schemes: \\textbf{fixed} (estimate once), \\textbf{rolling} (last $R$), \\textbf{recursive} (all past); TSA, Chapter 4 called this rolling-origin evaluation', 'scheme: \\textbf{fixă} (o singură estimare), \\textbf{mobilă} (ultimele $R$), \\textbf{recursivă} (tot trecutul); în TSA, Capitolul 4 aceasta este evaluarea cu origine mobilă'),
      T('$T$: the total sample; the last forecast, made at $R + P - 1$, targets $T$; the scheme matters for inference: West (1996) vs Giacomini--White (2006), Section 4', '$T$: eșantionul total; ultima prognoză, făcută la $R + P - 1$, are ținta $T$; schema contează pentru inferență: West (1996) față de Giacomini--White (2006), secțiunea 4')]),
    (T('Known from TSA, Chapter 0: MAE, RMSE, MAPE and the scale-free MASE \\refHK', 'Cunoscute din TSA, Capitolul 0: MAE, RMSE, MAPE și MASE, independentă de scală \\refHK'),
     [T('here the question is different: \\emph{which} loss, and what does it reward?', 'aici întrebarea este alta: \\emph{ce} pierdere și ce răsplătește ea?')])), 'small')

D.frame(T('The optimal point forecast and consistency (1/2)', 'Prognoza punctuală optimă și consistența (1/2)'), items(
    (T('Given a loss $L(x, y)$ and a predictive distribution $F$, the \\textbf{optimal} (Bayes) forecast minimises the expected loss:', 'Dată o pierdere $L(x, y)$ și o distribuție predictivă $F$, prognoza \\textbf{optimă} (Bayes) minimizează pierderea așteptată:'),
     ['$x^* = \\arg\\min_x \\E_F[L(x, Y)]$',
      T('$x$: the point forecast; $y$: the outcome; $L(x, y) \\ge 0$: the penalty; $\\E_F$: the expectation when $Y \\sim F$', '$x$: prognoza punctuală; $y$: realizarea; $L(x, y) \\ge 0$: penalizarea; $\\E_F$: media calculată cînd $Y \\sim F$')]),
    (T('A \\textbf{functional} $\\mathrm{T}(F)$ maps a distribution to a number: the mean, the median, a quantile', 'O \\textbf{funcțională} $\\mathrm{T}(F)$ asociază unei distribuții un număr: media, mediana, o cuantilă'),
     [T('$L$ is \\textbf{consistent} for $\\mathrm{T}$ if $\\E_F L(\\mathrm{T}(F), Y) \\le \\E_F L(x, Y)$ for all $x$ and $F$ \\refGnaa', '$L$ este \\textbf{consistentă} pentru $\\mathrm{T}$ dacă $\\E_F L(\\mathrm{T}(F), Y) \\le \\E_F L(x, Y)$ pentru orice $x$ și $F$ \\refGnaa'),
      T('i.e.\\ reporting $\\mathrm{T}(F)$ is optimal whatever $F$ is; \\textbf{strictly} consistent: equality only at $x = \\mathrm{T}(F)$', 'adică raportarea lui $\\mathrm{T}(F)$ este optimă oricare ar fi $F$; consistentă \\textbf{strict}: egalitate doar pentru $x = \\mathrm{T}(F)$')])))

D.frame(T('The optimal point forecast and consistency (2/2)', 'Prognoza punctuală optimă și consistența (2/2)'), items(
    (T('Three classical cases, with the forecast error $e = y - x$; set the derivative of the expected loss to zero', 'Trei cazuri clasice, cu eroarea de prognoză $e = y - x$; anulăm derivata pierderii așteptate'),
     [T('squared $e^2$: $\\frac{d}{dx}\\E(Y - x)^2 = -2\\E(Y - x) = 0 \\Rightarrow x^* = \\E Y$ (the mean)', 'pătratică $e^2$: $\\frac{d}{dx}\\E(Y - x)^2 = -2\\E(Y - x) = 0 \\Rightarrow x^* = \\E Y$ (media)'),
      T('absolute $|e|$: $\\frac{d}{dx}\\E|Y - x| = F(x) - (1 - F(x)) = 0 \\Rightarrow F(x^*) = 1/2$ (the median)', 'absolută $|e|$: $\\frac{d}{dx}\\E|Y - x| = F(x) - (1 - F(x)) = 0 \\Rightarrow F(x^*) = 1/2$ (mediana)'),
      T('pinball $\\rho_\\tau(e) = (\\tau - \\mathbf 1\\{e < 0\\})e$: $F(x) - \\tau = 0 \\Rightarrow x^* = F^{-1}(\\tau)$ (the $\\tau$-quantile)', 'pinball $\\rho_\\tau(e) = (\\tau - \\mathbf 1\\{e < 0\\})e$: $F(x) - \\tau = 0 \\Rightarrow x^* = F^{-1}(\\tau)$ (cuantila $\\tau$)')]),
    (T('Notation of the pinball loss', 'Notațiile pierderii pinball'),
     [T('$\\tau \\in (0, 1)$: the quantile level; $\\mathbf 1\\{e < 0\\}$: 1 if the forecast is too high, 0 otherwise; $F^{-1}$: the quantile function', '$\\tau \\in (0, 1)$: nivelul cuantilei; $\\mathbf 1\\{e < 0\\}$: 1 dacă prognoza este prea mare, 0 altfel; $F^{-1}$: funcția cuantilă'),
      T('under-forecasts cost $\\tau|e|$, over-forecasts $(1 - \\tau)|e|$: a high $\\tau$ pushes the forecast up', 'prognozele prea mici costă $\\tau|e|$, cele prea mari $(1 - \\tau)|e|$: un $\\tau$ mare împinge prognoza în sus')]),
    T('Consequence: announce the loss \\emph{before} asking for a forecast; a median forecast judged by RMSE is judged unfairly \\refGnaa', 'Consecință: anunțați pierderea \\emph{înainte} de a cere o prognoză; o prognoză-mediană judecată prin RMSE este judecată nedrept \\refGnaa')), 'small')

chart(T('Three losses, three optimal forecasts', 'Trei pierderi, trei prognoze optime'), 'ats_ch1_loss_minimizers', 'ATS_ch1_loss_functions', [
    T('$Y$ log-normal with $\\ln Y \\sim N(0, @{l.s}^2)$; expected loss as a function of the point forecast $x$ (simulation, $2 \\times 10^5$ draws)',
      '$Y$ log-normal cu $\\ln Y \\sim N(0, @{l.s}^2)$; pierderea așteptată ca funcție de prognoza punctuală $x$ (simulare, $2 \\times 10^5$ extrageri)')], h='0.52\\textheight')

interp(('the three minimisers', 'celor trei puncte de minim'), [
    (T('Mean @{l.mean}, median 1, 0.9-quantile @{l.q90}: three different ``best\'\' forecasts of the same variable', 'Media @{l.mean}, mediana 1, cuantila 0,9 @{l.q90}: trei prognoze „cele mai bune” diferite pentru aceeași variabilă'),
     [T('for a right-skewed target (wages, loads, prices, volatility) the gap is large', 'pentru o țintă asimetrică la dreapta (salarii, consum de energie, prețuri, volatilitate) diferența este mare')]),
    T('The pinball curve is flat near its minimum: quantile forecasts are hard to separate with few observations', 'Curba pinball este plată în jurul minimului: prognozele de cuantilă se deosebesc greu cu puține observații'),
    T('A forecaster who knows the loss reports the matching functional; ranking forecasts by another loss rewards the wrong behaviour', 'Un prognozator care cunoaște pierderea raportează funcționala potrivită; ierarhizarea cu altă pierdere răsplătește un comportament greșit')])

D.frame(T('Bregman losses: all losses consistent for the mean (1/2)', 'Pierderile Bregman: toate pierderile consistente pentru medie (1/2)'), items(
    (T('\\textbf{Theorem} \\refSav, \\refGnaa: under regularity, $L$ is consistent for the mean iff it is a \\textbf{Bregman} loss', '\\textbf{Teoremă} \\refSav, \\refGnaa: în condiții de regularitate, $L$ este consistentă pentru medie dacă și numai dacă este o pierdere \\textbf{Bregman}'),
     ['$L(x, y) = \\phi(y) - \\phi(x) - \\phi\'(x)(y - x)$',
      T('$\\phi$: a convex function, $\\phi\'$ its derivative; $L$ is the gap between $\\phi(y)$ and the tangent of $\\phi$ at $x$, so $L \\ge 0$ (up to terms in $y$ only)', '$\\phi$: o funcție convexă, $\\phi\'$ derivata ei; $L$ este distanța dintre $\\phi(y)$ și tangenta la $\\phi$ în $x$, deci $L \\ge 0$ (pînă la termeni care depind doar de $y$)')]),
    (T('Two members of the family', 'Doi membri ai familiei'),
     [T('$\\phi(x) = x^2$: the squared error $(y - x)^2$', '$\\phi(x) = x^2$: eroarea pătratică $(y - x)^2$'),
      T('$\\phi(x) = -\\ln x$: \\textbf{QLIKE} $y/x - \\ln(y/x) - 1$, for a variance forecast $x > 0$ and a variance proxy $y > 0$ (Chapter 8)', '$\\phi(x) = -\\ln x$: \\textbf{QLIKE} $y/x - \\ln(y/x) - 1$, pentru o prognoză de varianță $x > 0$ și un indicator al varianței $y > 0$ (Capitolul 8)'),
      T('the conditional mean is optimal for every Bregman loss \\refBGW; proof for the quantile in the Appendix', 'media condiționată este optimă pentru orice pierdere Bregman \\refBGW; demonstrația pentru cuantilă în Anexă')])))

D.frame(T('Bregman losses: all losses consistent for the mean (2/2)', 'Pierderile Bregman: toate pierderile consistente pentru medie (2/2)'), items(
    (T('Proof sketch, with $\\mu = \\E Y$:', 'Schița demonstrației, cu $\\mu = \\E Y$:'),
     ['$\\E L(x, Y) - \\E L(\\mu, Y) = \\phi(\\mu) - \\phi(x) - \\phi\'(x)(\\mu - x) \\ge 0$',
      T('the linear term vanishes because $\\E(Y - \\mu) = 0$; the inequality is convexity of $\\phi$', 'termenul liniar dispare deoarece $\\E(Y - \\mu) = 0$; inegalitatea este convexitatea lui $\\phi$')]),
    (T('Correctly specified forecasts rank the same under every Bregman loss; misspecified ones need not \\refPatbz', 'Prognozele corect specificate se ierarhizează la fel sub orice pierdere Bregman; cele greșit specificate nu neapărat \\refPatbz'),
     [T('Murphy diagrams \\refEGJK\\ plot the score over the whole family: one forecast dominates only if its curve is lower everywhere', 'diagramele Murphy \\refEGJK\\ reprezintă scorul pe toată familia: o prognoză domină doar dacă este mai jos peste tot'),
      T('robust proxies for volatility: only some losses keep the ranking with a noisy proxy \\refPataa', 'pentru volatilitate cu un indicator zgomotos, doar unele pierderi păstrează ierarhia \\refPataa')])))

D.frame(T('Asymmetric loss', 'Pierderi asimetrice'), items(
    (T('\\textbf{LinEx} loss $L(e) = b[\\exp(ae) - ae - 1]$, $e = y - x$: linear on one side, exponential on the other', 'Pierderea \\textbf{LinEx} $L(e) = b[\\exp(ae) - ae - 1]$, $e = y - x$: liniară de o parte, exponențială de cealaltă'),
     [T('$b > 0$: a scale; $a$: the asymmetry; $a > 0$ penalises under-forecasts ($e > 0$) exponentially, over-forecasts about linearly', '$b > 0$: o scală; $a$: asimetria; $a > 0$ penalizează exponențial prognozele prea mici ($e > 0$) și aproximativ liniar pe cele prea mari'),
      T('optimal forecast $x^* = a^{-1}\\ln\\E e^{aY}$; with $Y \\mid \\mathcal F_t \\sim N(\\mu_t, \\sigma_t^2)$ (conditional mean $\\mu_t$, variance $\\sigma_t^2$): $x^* = \\mu_t + a\\sigma^2_t/2$ \\refCD', 'prognoza optimă $x^* = a^{-1}\\ln\\E e^{aY}$; cu $Y \\mid \\mathcal F_t \\sim N(\\mu_t, \\sigma_t^2)$: $x^* = \\mu_t + a\\sigma^2_t/2$ \\refCD'),
      T('the optimal forecast is \\textbf{biased} and its bias moves with the conditional variance', 'prognoza optimă este \\textbf{deplasată}, iar deplasarea se mișcă odată cu varianța condiționată')]),
    (T('Consequences for evaluation', 'Consecințe pentru evaluare'),
     [T('a rational forecaster under asymmetric loss fails the MZ unbiasedness test (Section 4)', 'un prognozator rațional cu pierdere asimetrică pică testul MZ de nedeplasare (secțiunea 4)'),
      T('the pinball loss is the piecewise-linear member: the optimal forecast is a quantile', 'pierderea pinball este cazul liniar pe porțiuni: prognoza optimă este o cuantilă')]),
    T('Examples: a grid operator (under-forecasting load is costlier than over-forecasting), a central bank with asymmetric inflation costs, the capital buffer of a bank (Chapter 9)', 'Exemple: un operator de rețea (subestimarea consumului costă mai mult decît supraestimarea), o bancă centrală cu costuri asimetrice ale inflației, capitalul unei bănci (Capitolul 9)')), 'small')

D.recap(('Point forecasts and loss functions', 'prognoze punctuale și funcții de pierdere'), [
    T('A loss defines the target functional: squared $\\to$ mean, absolute $\\to$ median, pinball $\\to$ quantile', 'Pierderea definește funcționala-țintă: pătratică $\\to$ medie, absolută $\\to$ mediană, pinball $\\to$ cuantilă'),
    T('Bregman losses are exactly those consistent for the mean; QLIKE is one of them', 'Pierderile Bregman sînt exact cele consistente pentru medie; QLIKE este una dintre ele'),
    T('Under asymmetric loss the optimal forecast is biased by design', 'Sub pierdere asimetrică prognoza optimă este deplasată prin construcție'),
    T('With misspecified models the ranking can depend on the loss: fix it in advance', 'Cu modele greșit specificate ierarhia poate depinde de pierdere: fixați-o dinainte')])

# =============================================================================
# 2. CALIBRARE
# =============================================================================
D.section('Probabilistic forecasts: calibration and sharpness', 'Prognoze probabilistice: calibrare și sharpness')

D.frame(T('Maximise sharpness subject to calibration', 'Sharpness maxim sub condiția de calibrare'), items(
    (T('\\textbf{Calibration}: statistical consistency between the forecasts $F_t$ and the outcomes $y_t$ (a joint property) \\refGBR', '\\textbf{Calibrarea}: consistența statistică dintre prognozele $F_t$ și realizările $y_t$ (o proprietate comună a lor) \\refGBR'),
     [T('\\textbf{probabilistic} calibration: the PIT (probability integral transform) $u_t = F_t(y_t)$, the forecast probability of an outcome below $y_t$, is uniform on average', 'calibrare \\textbf{probabilistică}: PIT (probability integral transform) $u_t = F_t(y_t)$, probabilitatea prognozată a unei realizări sub $y_t$, este în medie uniform'),
      T('\\textbf{marginal} calibration: $\\frac1T\\sum_t F_t(x) \\to G(x)$ for every $x$, with $G$ the limit of the empirical distribution of $y_t$', 'calibrare \\textbf{marginală}: $\\frac1T\\sum_t F_t(x) \\to G(x)$ pentru orice $x$, cu $G$ limita distribuției empirice a lui $y_t$')]),
    (T('\\textbf{Sharpness}: concentration of the predictive distributions; a property of the forecasts only', '\\textbf{Sharpness}: concentrarea distribuțiilor predictive; o proprietate doar a prognozelor'),
     [T('measured by the average width of central intervals or the average predictive variance', 'măsurată prin lățimea medie a intervalelor centrale sau prin varianța predictivă medie')]),
    (T('Paradigm \\refGBR: among calibrated forecasts, prefer the sharpest', 'Paradigma \\refGBR: dintre prognozele calibrate, o preferăm pe cea mai concentrată'),
     [T('the climatological forecast (the unconditional distribution) is calibrated but not sharp', 'prognoza climatologică (distribuția necondiționată) este calibrată, dar nu este concentrată'),
      T('proper scores (next section) reward both at once', 'scorurile proprii (secțiunea următoare) le răsplătesc pe amîndouă deodată')])), 'small')

D.frame(T('The probability integral transform', 'Transformarea integrală de probabilitate (PIT)'), items(
    (T('\\textbf{Theorem} \\refDawid, \\refDGT: if $F_t$ is the true conditional distribution of $Y_t$ given $\\mathcal{F}_{t-1}$ and continuous, then $u_t = F_t(y_t)$ are i.i.d.\\ $U(0, 1)$', '\\textbf{Teoremă} \\refDawid, \\refDGT: dacă $F_t$ este adevărata distribuție condiționată a lui $Y_t$ dată fiind $\\mathcal{F}_{t-1}$ și este continuă, atunci $u_t = F_t(y_t)$ sînt i.i.d.\\ $U(0, 1)$'),
     [T('uniform: for every $v \\in (0,1)$, $P(u_t \\le v \\mid \\mathcal{F}_{t-1}) = P(Y_t \\le F_t^{-1}(v) \\mid \\mathcal F_{t-1}) = v$, whatever the past', 'uniform: pentru orice $v \\in (0,1)$, $P(u_t \\le v \\mid \\mathcal{F}_{t-1}) = P(Y_t \\le F_t^{-1}(v) \\mid \\mathcal F_{t-1}) = v$, oricare ar fi trecutul'),
      T('independent: a conditional distribution that does not depend on the past implies independence of the sequence', 'independent: o distribuție condiționată care nu depinde de trecut implică independența șirului')]),
    (T('For $h > 1$ the PITs are uniform but serially dependent up to lag $h - 1$ (overlapping horizons)', 'Pentru $h > 1$, valorile PIT sînt uniforme, dar dependente pînă la lagul $h - 1$ (orizonturi care se suprapun)'),
     [T('tests must allow this dependence \\refRS', 'testele trebuie să permită această dependență \\refRS')]),
    (T('Uniformity is necessary, not sufficient: \\refHamill\\ and \\refGBR\\ build uncalibrated forecasters whose PIT is uniform on average', 'Uniformitatea este necesară, nu suficientă: \\refHamill\\ și \\refGBR\\ construiesc prognozatori necalibrați al căror PIT este uniform în medie'),
     [T('check PIT conditionally: by sub-sample, by regime, by horizon', 'verificați PIT condiționat: pe subeșantioane, pe regimuri, pe orizonturi')])), 'small')

chart(T('What PIT histograms reveal', 'Interpretarea histogramelor PIT'), 'ats_ch1_pit_shapes', 'ATS_ch1_calibration_scores', [
    T('$Y \\sim N(0, 1)$, 5000 draws; four Normal forecasts; dashed line: the uniform density',
      '$Y \\sim N(0, 1)$, 5000 de extrageri; patru prognoze Normale; linia întreruptă: densitatea uniformă')], h='0.48\\textheight')

interp(('the PIT shapes', 'formelor PIT'), [
    T('\\textbf{U-shape}: too many outcomes in both tails (@{pit.tail.sharp}\\% outside the central 90\\%, against @{pit.tail.ideal}\\%): the forecast is too sharp, intervals too narrow',
      '\\textbf{Forma de U}: prea multe realizări în ambele cozi (@{pit.tail.sharp}\\% în afara intervalului central de 90\\%, față de @{pit.tail.ideal}\\%): prognoza este prea concentrată, intervalele prea înguste'),
    T('\\textbf{Hump}: too few outcomes in the tails (@{pit.tail.wide}\\%): the forecast is too wide, the intervals waste information',
      '\\textbf{Cocoașă}: prea puține realizări în cozi (@{pit.tail.wide}\\%): prognoza este prea largă, intervalele risipesc informație'),
    T('\\textbf{Slope}: a biased location; here the forecast mean is too high, so PIT values cluster near 0',
      '\\textbf{Pantă}: poziție deplasată; aici media prognozei este prea mare, deci valorile PIT se adună lîngă 0'),
    T('CRPS (lower is better): ideal @{pit.id.crps}, too sharp @{pit.sh.crps}, too wide @{pit.wi.crps}, biased @{pit.bi.crps}: the proper score ranks the ideal forecast first',
      'CRPS (mai mic este mai bine): ideală @{pit.id.crps}, prea concentrată @{pit.sh.crps}, prea largă @{pit.wi.crps}, deplasată @{pit.bi.crps}: scorul propriu pune prognoza ideală pe primul loc')])

D.frame(T('Testing calibration (1/2)', 'Testarea calibrării (1/2)'), items(
    (T('\\textbf{Berkowitz (2001)} \\refBerk: if the PITs are i.i.d.\\ uniform, $z_t = \\Phi^{-1}(u_t)$ is i.i.d.\\ $N(0, 1)$', '\\textbf{Berkowitz (2001)} \\refBerk: dacă valorile PIT sînt i.i.d.\\ uniforme, $z_t = \\Phi^{-1}(u_t)$ este i.i.d.\\ $N(0, 1)$'),
     [T('$\\Phi^{-1}$: the quantile function of the standard Normal distribution', '$\\Phi^{-1}$: funcția cuantilă a distribuției Normale standard')]),
    (T('Fit a Gaussian AR(1) to $z_t$ and test its parameters:', 'Estimăm un AR(1) gaussian pentru $z_t$ și îi testăm parametrii:'),
     ['$z_t = \\mu + \\rho(z_{t-1} - \\mu) + \\varepsilon_t$, $\\quad \\varepsilon_t \\sim N(0, \\sigma^2(1 - \\rho^2))$',
      T('$\\mu$: the mean of $z_t$; $\\sigma^2$: its variance; $\\rho$: its first-order autocorrelation; calibration means $\\mu = 0$, $\\sigma = 1$, $\\rho = 0$', '$\\mu$: media lui $z_t$; $\\sigma^2$: varianța lui; $\\rho$: autocorelația de ordinul întîi; calibrarea înseamnă $\\mu = 0$, $\\sigma = 1$, $\\rho = 0$'),
      T('LR (likelihood ratio) statistic $2(\\ell_1 - \\ell_0) \\sim \\chi^2(3)$ under $H_0$; $\\ell_1, \\ell_0$: maximised log-likelihoods without and with the restrictions', 'statistica LR (raportul de verosimilitate) $2(\\ell_1 - \\ell_0) \\sim \\chi^2(3)$ sub $H_0$; $\\ell_1, \\ell_0$: log-verosimilitățile maxime fără și cu restricții'),
      T('the transformation to $z$ makes the tails visible; the test checks only the first two moments and AR(1) dependence', 'transformarea în $z$ face cozile vizibile; testul verifică doar primele două momente și dependența AR(1)')])), 'small')

D.frame(T('Testing calibration (2/2)', 'Testarea calibrării (2/2)'), items(
    (T('\\textbf{Correlograms} of $(u_t - \\bar u)^k$, $k = 1, 2$ \\refDGT: dependence in level and in volatility', '\\textbf{Corelogramele} lui $(u_t - \\bar u)^k$, $k = 1, 2$ \\refDGT: dependență în nivel și în volatilitate'),
     [T('$\\bar u$: the mean PIT; Ljung--Box on $(u_t - \\bar u)^2$ detects missing volatility dynamics', '$\\bar u$: media valorilor PIT; testul Ljung--Box pe $(u_t - \\bar u)^2$ detectează dinamica de volatilitate omisă')]),
    (T('Parameter estimation changes the null distribution of PIT tests', 'Estimarea parametrilor schimbă distribuția sub ipoteza nulă a testelor PIT'),
     [T('with $P/R$ small (few forecasts relative to the estimation sample) it can be ignored, otherwise use \\refRS', 'cu $P/R$ mic (puține prognoze față de eșantionul de estimare) efectul poate fi ignorat, altfel folosiți \\refRS')]),
    (T('Interval forecasts: coverage and independence of the hits \\refChr', 'Prognozele de interval: acoperirea și independența depășirilor \\refChr'),
     [T('hit: an outcome outside the interval; for VaR this becomes backtesting (Chapter 9)', 'depășire: o realizare în afara intervalului; pentru VaR aceasta devine backtesting (Capitolul 9)')])))

D.frame(T('Case study: Diebold, Gunther and Tay (1998)', 'Studiu de caz: Diebold, Gunther și Tay (1998)'), items(
    (T('The paper: daily S\\&P 500 returns; parameters estimated once on the first part of the sample, density forecasts evaluated on the second part with PIT histograms and correlograms of $(u - \\bar u)^k$ \\refDGT', 'Lucrarea: randamente zilnice S\\&P 500; parametrii estimați o singură dată pe prima parte a eșantionului, prognozele de densitate evaluate pe partea a doua cu histograme PIT și corelograme ale lui $(u - \\bar u)^k$ \\refDGT'),
     [T('their models: i.i.d.\\ Normal; MA(1)-GARCH(1,1) with Normal and with Student-$t$ innovations \\refBoll', 'modelele lor: i.i.d.\\ Normal; MA(1)-GARCH(1,1) cu inovații Normale și cu inovații Student-$t$ \\refBoll')]),
    (T('Our replication: the same three models, estimated by maximum likelihood on 2000--2012, fixed parameters, one-day density forecasts for 2013--2026 ($@{dgt.n}$ days)', 'Replicarea noastră: aceleași trei modele, estimate prin verosimilitate maximă pe 2000--2012, parametri ficși, prognoze de densitate la o zi pentru 2013--2026 ($@{dgt.n}$ zile)'),
     [T('model: $r_t = c + \\varepsilon_t + \\theta\\varepsilon_{t-1}$, $\\varepsilon_t = \\sigma_tz_t$, $\\sigma_t^2 = \\omega + \\alpha\\varepsilon_{t-1}^2 + \\beta\\sigma_{t-1}^2$; $z_t$ Normal or Student-$t$ with $\\nu$ degrees of freedom', 'modelul: $r_t = c + \\varepsilon_t + \\theta\\varepsilon_{t-1}$, $\\varepsilon_t = \\sigma_tz_t$, $\\sigma_t^2 = \\omega + \\alpha\\varepsilon_{t-1}^2 + \\beta\\sigma_{t-1}^2$; $z_t$ Normal sau Student-$t$ cu $\\nu$ grade de libertate'),
      T('GARCH-$t$: $\\hat\\theta = @{dgt.th}$, $\\hat\\alpha + \\hat\\beta = @{dgt.ab}$ (the persistence of volatility), $\\hat\\nu = @{dgt.nu}$ (fat tails)', 'GARCH-$t$: $\\hat\\theta = @{dgt.th}$, $\\hat\\alpha + \\hat\\beta = @{dgt.ab}$ (persistența volatilității), $\\hat\\nu = @{dgt.nu}$ (cozi groase)')]),
    T('Question: which density forecast is calibrated, and do the proper scores agree with the PIT diagnosis?', 'Întrebarea: care prognoză de densitate este calibrată și sînt de acord scorurile proprii cu diagnosticul PIT?')), 'small')

chart(T('PIT diagnostics of three S\\&P 500 density forecasts', 'Diagnosticul PIT pentru trei prognoze de densitate ale S\\&P 500'), 'ats_ch1_dgt', 'ATS_ch1_density_forecasts', [
    T('Top: PIT histograms (20 bins); bottom: autocorrelations of $(u - \\bar u)$ and $(u - \\bar u)^2$ with $\\pm 2/\\sqrt{T}$ bands', 'Sus: histograme PIT (20 de intervale); jos: autocorelațiile lui $(u - \\bar u)$ și $(u - \\bar u)^2$, cu benzile $\\pm 2/\\sqrt{T}$')],
    h='0.60\\textheight')

interp(('the S\\&P 500 diagnostics', 'diagnosticului pentru S\\&P 500'), [
    (T('i.i.d.\\ Normal: a hump and strong autocorrelation of $(u - \\bar u)^2$: the forecast ignores volatility clustering; Berkowitz LR @{dgt.iid.lr} ($p$ @{dgt.iid.p})', 'i.i.d.\\ Normal: o cocoașă și autocorelație puternică a lui $(u - \\bar u)^2$: prognoza ignoră volatility clustering; Berkowitz LR @{dgt.iid.lr} ($p$ @{dgt.iid.p})'),
     [T('too wide in calm periods, too narrow in turbulent ones: the two errors average into a hump', 'prea largă în perioadele calme, prea îngustă în cele agitate: cele două erori se compun într-o cocoașă')]),
    (T('GARCH removes most of the dependence; the $t$ version has the better left tail', 'GARCH elimină cea mai mare parte a dependenței; varianta $t$ are o coadă stîngă mai bună'),
     [T('Berkowitz: GARCH-N LR @{dgt.gn.lr} ($p$ @{dgt.gn.p}), GARCH-$t$ LR @{dgt.gt.lr} ($p$ @{dgt.gt.p}); estimated $\\sigma_z$ @{dgt.gt.sig} $< 1$', 'Berkowitz: GARCH-N LR @{dgt.gn.lr} ($p$ @{dgt.gn.p}), GARCH-$t$ LR @{dgt.gt.lr} ($p$ @{dgt.gt.p}); $\\sigma_z$ estimat @{dgt.gt.sig} $< 1$'),
      T('outside the central 90\\%: @{dgt.gt.tails}\\% of days: with parameters frozen in 2012 the forecasts are slightly too wide after 2013', 'în afara intervalului central de 90\\%: @{dgt.gt.tails}\\% din zile: cu parametri înghețați în 2012, prognozele sînt puțin prea largi după 2013')]),
    T('In line with \\refDGT: conditional heteroskedasticity is essential, fat tails help; a small residual miscalibration remains', 'În acord cu \\refDGT: heteroscedasticitatea condiționată este esențială, cozile groase ajută; rămîne o mică necalibrare reziduală')])

D.recap(('Calibration', 'calibrarea'), [
    T('Calibration is a joint property of forecasts and outcomes; sharpness is a property of the forecasts', 'Calibrarea este o proprietate comună a prognozelor și a realizărilor; sharpness este o proprietate a prognozelor'),
    T('Correct one-step densities give i.i.d.\\ uniform PITs; for $h > 1$ they are dependent', 'Densitățile corecte la un pas dau valori PIT i.i.d.\\ uniforme; pentru $h > 1$ ele sînt dependente'),
    T('U-shape: too sharp; hump: too wide; slope: bias; correlogram of $(u - \\bar u)^2$: missing volatility dynamics', 'Forma de U: prea concentrată; cocoașa: prea largă; panta: deplasare; corelograma lui $(u - \\bar u)^2$: dinamica de volatilitate omisă'),
    T('The S\\&P 500: GARCH-$t$ is close to calibrated, the i.i.d.\\ Normal is not', 'S\\&P 500: GARCH-$t$ este aproape calibrat, i.i.d.\\ Normal nu este')])

# =============================================================================
# 3. SCORURI
# =============================================================================
D.section('Proper scoring rules and elicitability', 'Reguli de scor proprii și elicitabilitate')

D.frame(T('Proper scoring rules', 'Reguli de scor proprii'), items(
    (T('A \\textbf{scoring rule} $S(F, y)$ assigns a penalty to the forecast $F$ when $y$ occurs (negatively oriented: lower is better)', 'O \\textbf{regulă de scor} $S(F, y)$ atribuie o penalizare prognozei $F$ cînd se realizează $y$ (orientare negativă: mai mic este mai bine)'),
     [T('\\textbf{proper}: $\\E_G S(G, Y) \\le \\E_G S(F, Y)$ for all $F, G$ \\refGRa', '\\textbf{proprie}: $\\E_G S(G, Y) \\le \\E_G S(F, Y)$ pentru orice $F, G$ \\refGRa'),
      T('$G$: the distribution the forecaster believes; $\\E_G$: the expectation under $G$; reporting the true belief is optimal', '$G$: distribuția în care crede prognozatorul; $\\E_G$: media sub $G$; raportarea convingerii adevărate este optimă'),
      T('\\textbf{strictly proper}: equality only if $F = G$; then the score cannot be manipulated', '\\textbf{strict proprie}: egalitate doar dacă $F = G$; atunci scorul nu poate fi manipulat')]),
    (T('Proper scores reward calibration and sharpness together: the expected score decomposes into uncertainty, minus resolution, plus reliability', 'Scorurile proprii răsplătesc calibrarea și sharpness împreună: scorul așteptat se descompune în incertitudine, minus rezoluție, plus fiabilitate'),
     [T('the Brier score $(p - \\mathbf 1\\{\\text{event}\\})^2$, with $p$ the forecast probability of a binary event, is the oldest example \\refBrier', 'scorul Brier $(p - \\mathbf 1\\{\\text{eveniment}\\})^2$, cu $p$ probabilitatea prognozată a unui eveniment binar, este cel mai vechi exemplu \\refBrier')]),
    T('A proper score of a probabilistic forecast reduces to a consistent loss of a point forecast when $F$ is a point mass (CRPS $\\to$ absolute error)', 'Un scor propriu al unei prognoze probabilistice devine o pierdere consistentă a unei prognoze punctuale cînd $F$ este o masă punctuală (CRPS $\\to$ eroarea absolută)')), 'small')

D.frame(T('The logarithmic score', 'Scorul logaritmic'), items(
    (T('$\\mathrm{LogS}(f, y) = -\\ln f(y)$ \\refGood: the only proper score that is \\textbf{local} (depends on $f$ only at $y$, up to equivalence)', '$\\mathrm{LogS}(f, y) = -\\ln f(y)$ \\refGood: singurul scor propriu \\textbf{local} (depinde de $f$ doar în $y$, pînă la echivalență)'),
     [T('$f$: the forecast density; $g$: the true density; properness: $\\E_g[\\mathrm{LogS}(f, Y)] - \\E_g[\\mathrm{LogS}(g, Y)] = \\int g \\ln(g/f) = \\mathrm{KL}(g \\| f) \\ge 0$', '$f$: densitatea prognozată; $g$: densitatea adevărată; caracterul propriu: $\\E_g[\\mathrm{LogS}(f, Y)] - \\E_g[\\mathrm{LogS}(g, Y)] = \\int g \\ln(g/f) = \\mathrm{KL}(g \\| f) \\ge 0$'),
      T('$\\mathrm{KL}$: the Kullback--Leibler divergence, nonnegative and zero only if $f = g$ (Gibbs inequality)', '$\\mathrm{KL}$: divergența Kullback--Leibler, nenegativă și nulă doar dacă $f = g$ (inegalitatea Gibbs)')]),
    (T('Links: average log score = minus the out-of-sample log-likelihood; the difference of two log scores is a predictive likelihood ratio', 'Legături: scorul logaritmic mediu = minus log-verosimilitatea în afara eșantionului; diferența a două scoruri logaritmice este un raport de verosimilitate predictivă'),
     [T('Bayes factors and the predictive model choice of \\refGA\\ are built on it', 'factorii Bayes și alegerea predictivă a modelelor din \\refGA\\ se construiesc pe el')]),
    (T('Weaknesses: infinite if $f(y) = 0$; very sensitive to tail events; needs a density', 'Slăbiciuni: infinit dacă $f(y) = 0$; foarte sensibil la evenimentele din coadă; cere o densitate'),
     [T('cannot score ensembles or quantile forecasts directly', 'nu poate evalua direct ansambluri sau prognoze de cuantile')])), 'small')

D.frame(T('The continuous ranked probability score (1/2)', 'Scorul probabilistic continuu (CRPS) (1/2)'), items(
    (T('Definition \\refMW: the squared distance between the forecast distribution function and the step function of the outcome', 'Definiția \\refMW: distanța pătratică dintre funcția de repartiție prognozată și funcția treaptă a realizării'),
     ['$\\mathrm{CRPS}(F, y) = \\int_{-\\infty}^{\\infty}(F(z) - \\mathbf 1\\{y \\le z\\})^2dz$',
      T('$z$: a threshold; $\\mathbf 1\\{y \\le z\\}$: the ``distribution function\'\' of the outcome, 0 below $y$ and 1 above; units: those of $y$', '$z$: un prag; $\\mathbf 1\\{y \\le z\\}$: „funcția de repartiție” a realizării, 0 sub $y$ și 1 peste $y$; unitatea de măsură: cea a lui $y$')]),
    (T('Kernel form \\refGRa\\ (proof in the Appendix):', 'Forma cu nucleu \\refGRa\\ (demonstrația în Anexă):'),
     ['$\\mathrm{CRPS}(F, y) = \\E_F|X - y| - \\frac12\\E_F|X - X\'|$, $\\quad X, X\' \\sim F$ ⟦independent||independente⟧',
      T('first term: accuracy; second: a reward for spread that stops the score from favouring point masses', 'primul termen: acuratețea; al doilea: o recompensă pentru dispersie care împiedică scorul să favorizeze masele punctuale'),
      T('for a point forecast ($F$ a point mass at $x$) it reduces to the absolute error $|y - x|$', 'pentru o prognoză punctuală ($F$ masă punctuală în $x$) devine eroarea absolută $|y - x|$')])))

D.frame(T('The continuous ranked probability score (2/2)', 'Scorul probabilistic continuu (CRPS) (2/2)'), items(
    (T('Closed form for $F = N(\\mu, \\sigma^2)$, with $z = (y - \\mu)/\\sigma$:', 'Forma închisă pentru $F = N(\\mu, \\sigma^2)$, cu $z = (y - \\mu)/\\sigma$:'),
     ['$\\mathrm{CRPS} = \\sigma\\left[z(2\\Phi(z) - 1) + 2\\varphi(z) - 1/\\sqrt\\pi\\right]$',
      T('$\\Phi$, $\\varphi$: the distribution and density functions of $N(0,1)$; a closed form exists also for Student $t$ (Quantlet)', '$\\Phi$, $\\varphi$: funcția de repartiție și densitatea lui $N(0,1)$; există o formă închisă și pentru Student $t$ (Quantlet)'),
      T('ensembles: plug in the empirical distribution of the members', 'ansambluri: înlocuim $F$ cu distribuția empirică a membrilor')]),
    (T('Decompositions:', 'Descompuneri:'),
     ['$\\mathrm{CRPS} = \\int \\mathrm{BS}_z\\,dz = 2\\int_0^1 \\rho_\\tau(y - F^{-1}(\\tau))\\,d\\tau$',
      T('$\\mathrm{BS}_z$: the Brier score of the event $\\{y \\le z\\}$; $\\rho_\\tau$: the pinball loss at level $\\tau$', '$\\mathrm{BS}_z$: scorul Brier al evenimentului $\\{y \\le z\\}$; $\\rho_\\tau$: pierderea pinball la nivelul $\\tau$'),
      T('so the average pinball over the 99 percentiles (GEFCom2014) approximates CRPS/2 \\refGEF', 'deci media pinball pe cele 99 de percentile (GEFCom2014) aproximează CRPS/2 \\refGEF')])))

D.frame(T('Quantile, interval and multivariate scores (1/2)', 'Scoruri pentru cuantile, intervale și vectori (1/2)'), items(
    (T('\\textbf{Quantile score}: $\\rho_\\tau(y - q)$ for a forecast $q$ of the $\\tau$-quantile, strictly consistent \\refGnaa', '\\textbf{Scorul de cuantilă}: $\\rho_\\tau(y - q)$ pentru o prognoză $q$ a cuantilei $\\tau$, strict consistent \\refGnaa'),
     [T('any increasing $g$ gives another consistent score: $(\\mathbf 1\\{y \\le q\\} - \\tau)(g(q) - g(y))$', 'orice funcție crescătoare $g$ dă un alt scor consistent: $(\\mathbf 1\\{y \\le q\\} - \\tau)(g(q) - g(y))$')]),
    (T('\\textbf{Interval score} of a central $(1 - \\alpha)$ interval $[l, u]$ \\refGRa', '\\textbf{Scorul de interval} al unui interval central $(1 - \\alpha)$, $[l, u]$ \\refGRa'),
     ['$\\mathrm{IS}_\\alpha = (u - l) + \\frac2\\alpha(l - y)\\mathbf 1\\{y < l\\} + \\frac2\\alpha(y - u)\\mathbf 1\\{y > u\\}$',
      T('$l, u$: the lower and upper limits; width plus a penalty $2/\\alpha$ per unit of miss', '$l, u$: limitele inferioară și superioară; lățimea plus o penalizare $2/\\alpha$ pe unitatea de ratare'),
      T('it equals $\\frac2\\alpha[\\rho_{\\alpha/2}(y - l) + \\rho_{1 - \\alpha/2}(y - u)]$; coverage alone is not a score', 'este egal cu $\\frac2\\alpha[\\rho_{\\alpha/2}(y - l) + \\rho_{1 - \\alpha/2}(y - u)]$; acoperirea singură nu este un scor')])))

D.frame(T('Quantile, interval and multivariate scores (2/2)', 'Scoruri pentru cuantile, intervale și vectori (2/2)'), items(
    (T('\\textbf{Energy score} for vectors, the multivariate CRPS:', '\\textbf{Energy score} pentru vectori, CRPS multivariat:'),
     ['$\\mathrm{ES}(F, \\mathbf y) = \\E\\|\\mathbf X - \\mathbf y\\| - \\frac12\\E\\|\\mathbf X - \\mathbf X\'\\|$',
      T('$\\mathbf y$: the outcome vector; $\\mathbf X, \\mathbf X\'$: independent draws from the forecast $F$; $\\|\\cdot\\|$: the Euclidean norm', '$\\mathbf y$: vectorul realizărilor; $\\mathbf X, \\mathbf X\'$: extrageri independente din prognoza $F$; $\\|\\cdot\\|$: norma euclidiană'),
      T('weak at detecting wrong correlations; the \\textbf{variogram score} \\refSH\\ targets the dependence structure (24 hourly loads, a VAR path)', 'slab în detectarea corelațiilor greșite; \\textbf{variogram score} \\refSH\\ vizează structura de dependență (24 de consumuri orare, o traiectorie VAR)')]),
    (T('Tails: threshold-weighted CRPS stays proper \\refGRjaa', 'Cozile: CRPS ponderat pe praguri rămîne propriu \\refGRjaa'),
     ['$\\int (F(z) - \\mathbf 1\\{y \\le z\\})^2w(z)dz$',
      T('$w(z) \\ge 0$: a weight that emphasises the thresholds of interest (e.g.\\ the left tail); the weighted likelihood ratio of \\refAG\\ does not stay proper \\refGRjaa', '$w(z) \\ge 0$: o pondere care accentuează pragurile de interes (de exemplu coada stîngă); raportul de verosimilitate ponderat din \\refAG\\ nu rămîne propriu \\refGRjaa')])))

chart(T('Proper and improper scores', 'Scoruri proprii și improprii'), 'ats_ch1_proper_scores', 'ATS_ch1_calibration_scores', [
    T('Truth $Y \\sim N(0, 1)$; forecast $N(0, s^2)$; expected score as a function of the spread $s$ (closed forms)', 'Adevărul $Y \\sim N(0, 1)$; prognoza $N(0, s^2)$; scorul așteptat ca funcție de dispersia $s$ (forme închise)'),
    T('Log score and CRPS: minimum at $s = 1$; linear score $-f(y)$: $\\E f(Y) = [2\\pi(1 + s^2)]^{-1/2}$ grows as $s \\to 0$: it rewards overconfidence', 'Scorul logaritmic și CRPS: minim la $s = 1$; scorul liniar $-f(y)$: $\\E f(Y) = [2\\pi(1 + s^2)]^{-1/2}$ crește cînd $s \\to 0$: răsplătește excesul de încredere')],
    h='0.48\\textheight')

interp(('the expected scores', 'scorurilor așteptate'), [
    T('The log score and the CRPS are minimised by the true spread: a forecaster maximises the expected reward by reporting what she believes', 'Scorul logaritmic și CRPS sînt minime pentru dispersia adevărată: prognozatorul își maximizează recompensa așteptată raportînd ceea ce crede'),
    T('The log score punishes overconfidence much more than excess spread (steep left branch); the CRPS is more symmetric and bounded by the absolute error', 'Scorul logaritmic penalizează excesul de încredere mult mai mult decît dispersia prea mare (ramura stîngă abruptă); CRPS este mai simetric și mărginit de eroarea absolută'),
    T('The linear score is maximised by a point mass: it would reward a forecaster who always reports a spike, so it must not be used for evaluation', 'Scorul liniar este optimizat de o masă punctuală: ar răsplăti un prognozator care raportează mereu un vîrf, deci nu trebuie folosit la evaluare')])

D.frame(T('Elicitability', 'Elicitabilitate'), items(
    (T('A functional $\\mathrm T$ is \\textbf{elicitable} if a strictly consistent loss exists for it \\refGnaa', 'O funcțională $\\mathrm T$ este \\textbf{elicitabilă} dacă există o pierdere strict consistentă pentru ea \\refGnaa'),
     [T('mean, quantiles, expectiles, ratios of expectations: elicitable', 'media, cuantilele, expectilele, rapoartele de medii: elicitabile'),
      T('only elicitable functionals can be compared and ranked meaningfully with point forecasts', 'doar funcționalele elicitabile pot fi comparate și ierarhizate cu sens prin prognoze punctuale')]),
    (T('\\textbf{Necessary condition} (Osband): convex level sets: $\\mathrm T(F_0) = \\mathrm T(F_1) = t \\Rightarrow \\mathrm T(\\lambda F_0 + (1 - \\lambda)F_1) = t$', '\\textbf{Condiție necesară} (Osband): mulțimi de nivel convexe: $\\mathrm T(F_0) = \\mathrm T(F_1) = t \\Rightarrow \\mathrm T(\\lambda F_0 + (1 - \\lambda)F_1) = t$'),
     [T('$F_0, F_1$: two distributions with the same value $t$; $\\lambda \\in [0,1]$: the mixing weight', '$F_0, F_1$: două distribuții cu aceeași valoare $t$; $\\lambda \\in [0,1]$: ponderea mixturii'),
      T('the \\textbf{variance} fails it, so it is not elicitable; the pair (mean, second moment) is', '\\textbf{varianța} nu o îndeplinește, deci nu este elicitabilă; perechea (medie, al doilea moment) este')]),
    (T('Risk measures with $\\mathrm{VaR}_\\alpha(X) = -q_\\alpha(X)$, $q_\\alpha$ the $\\alpha$-quantile of the return $X$ (VaR 1\\%: $\\alpha = 0.01$)', 'Măsurile de risc cu $\\mathrm{VaR}_\\alpha(X) = -q_\\alpha(X)$, $q_\\alpha$ cuantila de ordin $\\alpha$ a randamentului $X$ (VaR 1\\%: $\\alpha = 0{,}01$)'),
     [T('VaR is a quantile: elicitable by the pinball loss', 'VaR este o cuantilă: elicitabil prin pierderea pinball'),
      T('ES (expected shortfall, the mean loss beyond VaR) has non-convex level sets: \\textbf{not elicitable} alone \\refWeber, \\refGnaa; (VaR, ES) is \\textbf{jointly} elicitable \\refFZ', 'ES (expected shortfall, pierderea medie dincolo de VaR) are mulțimi de nivel neconvexe: \\textbf{nu este elicitabil} singur \\refWeber, \\refGnaa; perechea (VaR, ES) este elicitabilă \\textbf{împreună} \\refFZ'),
      T('the Fissler--Ziegel scores and the backtests built on them: Chapter 9', 'funcțiile de scor Fissler--Ziegel și testele construite pe ele: Capitolul 9')])), 'small')

D.frame(T('Scores of the S\\&P 500 density forecasts', 'Scorurile prognozelor de densitate pentru S\\&P 500'), table(
    'lcccc', T('\\textbf{Model}', '\\textbf{Model}') + ' & ' + T('\\textbf{Log score}', '\\textbf{Scor logaritmic}') + ' & \\textbf{CRPS} & ' + T('\\textbf{Outside 90\\%}', '\\textbf{În afara 90\\%}') + ' & \\textbf{Berkowitz $p$}',
    ['i.i.d.\\ Normal & @{dgt.iid.logs} & @{dgt.iid.crps} & @{dgt.iid.tails}\\% & @{dgt.iid.p}',
     'MA(1)-GARCH(1,1)-N & @{dgt.gn.logs} & @{dgt.gn.crps} & @{dgt.gn.tails}\\% & @{dgt.gn.p}',
     'MA(1)-GARCH(1,1)-$t$ & @{dgt.gt.logs} & @{dgt.gt.crps} & @{dgt.gt.tails}\\% & @{dgt.gt.p}'], size='footnotesize') + items(
    (T('Score differences tested with DM on the daily scores (\\refAG, unweighted)', 'Diferențele de scor testate cu DM pe scorurile zilnice (\\refAG, neponderat)'),
     [T('GARCH-$t$ against GARCH-N: HLN @{dgt.ls.tn} (log score), @{dgt.cr.tn} (CRPS); GARCH-N against i.i.d.: @{dgt.ls.ni} and @{dgt.cr.ni}', 'GARCH-$t$ față de GARCH-N: HLN @{dgt.ls.tn} (scor logaritmic), @{dgt.cr.tn} (CRPS); GARCH-N față de i.i.d.: @{dgt.ls.ni} și @{dgt.cr.ni}')]),
    T('Both scores rank the models in the same order as the PIT diagnosis; the log score separates the tails more sharply', 'Ambele scoruri ordonează modelele ca diagnosticul PIT; scorul logaritmic separă mai net cozile'),
    T('Ranking and calibration are different questions: the best-scoring model can still fail a calibration test', 'Ierarhizarea și calibrarea sînt întrebări diferite: modelul cu cel mai bun scor poate pica totuși un test de calibrare')), 'footnotesize')

D.recap(('Proper scores and elicitability', 'scoruri proprii și elicitabilitate'), [
    T('Proper scores make honesty optimal; strictly proper scores cannot be gamed', 'Scorurile proprii fac optimă raportarea sinceră; cele strict proprii nu pot fi manipulate'),
    T('LogS: local, tail-sensitive; CRPS: robust, works for ensembles, equals twice the integrated pinball loss', 'LogS: local, sensibil la cozi; CRPS: robust, merge pentru ansambluri, egal cu dublul pierderii pinball integrate'),
    T('Interval score for intervals, energy and variogram scores for vectors', 'Scorul de interval pentru intervale, energy și variogram score pentru vectori'),
    T('Elicitable: mean, quantile (VaR); not elicitable: variance, ES alone; (VaR, ES) jointly', 'Elicitabile: media, cuantila (VaR); neelicitabile: varianța, ES singur; (VaR, ES) împreună')])

# =============================================================================
# 4. COMPARAREA PROGNOZELOR
# =============================================================================
D.section('Comparing forecasts', 'Compararea prognozelor')

D.frame(T('Two questions about predictive ability', 'Două întrebări despre capacitatea predictivă'), items(
    (T('\\textbf{Population} (West 1996): are the \\emph{models}, at their pseudo-true parameters, equally accurate? \\refWest', '\\textbf{Populație} (West 1996): sînt \\emph{modelele}, la parametrii lor pseudo-adevărați, la fel de precise? \\refWest'),
     [T('estimation error enters the asymptotic variance unless $P/R \\to 0$ or the loss is the one used in estimation', 'eroarea de estimare intră în varianța asimptotică, cu excepția cazului $P/R \\to 0$ sau cînd pierderea este cea folosită la estimare')]),
    (T('\\textbf{Finite sample} (Giacomini--White 2006): are the \\emph{forecasting methods}, with their estimation windows, equally accurate? \\refGW', '\\textbf{Eșantion finit} (Giacomini--White 2006): sînt \\emph{metodele de prognoză}, cu ferestrele lor de estimare, la fel de precise? \\refGW'),
     [T('rolling window of fixed size $R$: estimation noise is part of the method; nested models allowed', 'fereastră mobilă de dimensiune fixă $R$: zgomotul de estimare face parte din metodă; modelele imbricate sînt permise')]),
    (T('\\textbf{Diebold--Mariano} \\refDM\\ treats the forecasts as given (``primitives\'\'): it compares forecasts, not models \\refDie', '\\textbf{Diebold--Mariano} \\refDM\\ tratează prognozele ca date („primitive”): compară prognoze, nu modele \\refDie'),
     [T('using DM to compare models with estimated parameters needs the West or GW framework', 'folosirea DM pentru a compara modele cu parametri estimați cere cadrul West sau GW')])), 'small')

D.frame(T('The Diebold--Mariano test with HAC variance (1/2)', 'Testul Diebold--Mariano cu varianță HAC (1/2)'), items(
    (T('Loss differential $d_t = L(e_{1t}) - L(e_{2t})$; $H_0$: $\\E d_t = 0$ (equal accuracy)', 'Diferențialul de pierdere $d_t = L(e_{1t}) - L(e_{2t})$; $H_0$: $\\E d_t = 0$ (acuratețe egală)'),
     [T('$e_{it}$: the error of forecast $i$ at $t$; $d_t > 0$: forecast 2 did better at $t$; $d_t$ assumed covariance stationary', '$e_{it}$: eroarea prognozei $i$ la momentul $t$; $d_t > 0$: prognoza 2 a fost mai bună la $t$; presupunem $d_t$ staționar în covarianță')]),
    (T('The statistic: the mean differential over its HAC standard error', 'Statistica: diferențialul mediu împărțit la eroarea lui standard HAC'),
     ['$\\mathrm{DM} = \\bar d/\\sqrt{\\hat\\sigma^2_{LR}/P} \\to N(0, 1)$, $\\quad \\sigma^2_{LR} = \\gamma_0 + 2\\sum_{k \\ge 1}\\gamma_k$',
      T('$\\bar d$: the mean of $d_t$ over the $P$ forecasts; $\\gamma_k$: the autocovariances of $d_t$; $\\sigma^2_{LR}$: its long-run variance (Chapter 0)', '$\\bar d$: media lui $d_t$ pe cele $P$ prognoze; $\\gamma_k$: autocovarianțele lui $d_t$; $\\sigma^2_{LR}$: varianța lui de termen lung (Capitolul 0)'),
      T('a large positive DM: forecast 2 is more accurate; reject at 5\\% if $|\\mathrm{DM}| > 1.96$', 'un DM mare și pozitiv: prognoza 2 este mai precisă; respingem la 5\\% dacă $|\\mathrm{DM}| > 1{,}96$')])))

D.frame(T('The Diebold--Mariano test with HAC variance (2/2)', 'Testul Diebold--Mariano cu varianță HAC (2/2)'), items(
    (T('Optimal $h$-step errors are at most MA($h - 1$), so DM truncate at $h - 1$ lags with a \\textbf{rectangular} kernel', 'Erorile optime la $h$ pași sînt cel mult MA($h - 1$), deci DM trunchiază la $h - 1$ laguri cu un nucleu \\textbf{dreptunghiular}'),
     [T('the rectangular estimate can be \\textbf{negative}; Newey--West (Bartlett) weights keep it positive \\refNW, at the cost of downward bias', 'estimarea dreptunghiulară poate fi \\textbf{negativă}; ponderile Newey--West (Bartlett) o păstrează pozitivă \\refNW, cu prețul unei deplasări în jos'),
      T('suboptimal forecasts have errors with longer memory: use a data-driven bandwidth (Chapter 0)', 'prognozele suboptimale au erori cu memorie mai lungă: folosiți o lățime de bandă aleasă din date (Capitolul 0)')]),
    (T('\\textbf{HLN correction} \\refHLNig: a small-sample rescaling of DM', '\\textbf{Corecția HLN} \\refHLNig: o rescalare a lui DM pentru eșantioane mici'),
     ['$\\mathrm{DM}^* = \\mathrm{DM}\\sqrt{(P + 1 - 2h + h(h - 1)/P)/P}$, ⟦compared with||comparat cu⟧ $t_{P-1}$',
      T('the factor (below 1) removes the bias of the variance estimator for MA($h - 1$) errors; $t_{P-1}$: Student $t$ with $P - 1$ degrees of freedom, for small $P$', 'factorul (sub 1) elimină deplasarea estimatorului varianței pentru erori MA($h - 1$); $t_{P-1}$: distribuția Student $t$ cu $P - 1$ grade de libertate, pentru $P$ mic')])))

chart(T('Size of DM and HLN in small samples', 'Mărimea testelor DM și HLN în eșantioane mici'), 'ats_ch1_dm_size', 'ATS_ch1_dm_tests', [
    T('Two independent MA($h - 1$) error series with equal variance, squared loss; share of rejections at 5\\% in @{ds.reps} replications', 'Două serii de erori MA($h - 1$) independente, cu varianțe egale, pierdere pătratică; proporția respingerilor la 5\\% în @{ds.reps} de replicări')],
    h='0.64\\textheight')

interp(('the size experiment', 'experimentului de mărime'), [
    (T('$h = 1$: both tests are close to 5\\%; DM over-rejects only at $P = 16$ (@{ds.1.16.dm}\\%)', '$h = 1$: ambele teste sînt aproape de 5\\%; DM respinge prea des doar la $P = 16$ (@{ds.1.16.dm}\\%)'), []),
    (T('$h = 8$, $P = 16$: DM rejects a true null @{ds.8.16.dm}\\% of the time, HLN @{ds.8.16.hln}\\%; at $P = 64$: @{ds.8.64.dm}\\% and @{ds.8.64.hln}\\%', '$h = 8$, $P = 16$: DM respinge o ipoteză nulă adevărată în @{ds.8.16.dm}\\% din cazuri, HLN în @{ds.8.16.hln}\\%; la $P = 64$: @{ds.8.64.dm}\\% și @{ds.8.64.hln}\\%'),
     [T('the HAC variance with few observations and many lags is noisy and biased down', 'varianța HAC cu puține observații și multe laguri este zgomotoasă și deplasată în jos')]),
    T('Rule: at multi-step horizons with fewer than about 100 forecasts, use HLN and treat $p$-values near 5\\% as inconclusive; fixed-$b$ critical values (Chapter 0) are an alternative',
      'Regulă: la orizonturi de mai mulți pași și cu mai puțin de aproximativ 100 de prognoze, folosiți HLN și tratați p-value-urile din jurul lui 5\\% ca neconcludente; valorile critice fixed-$b$ (Capitolul 0) sînt o alternativă')])

D.frame(T('Romanian inflation one year ahead: the design', 'Inflația din România cu un an înainte: planul de evaluare'), items(
    (T('Target: HICP inflation, y/y, 12 months ahead; forecast origins from January 2013, targets @{ri.first} to @{ri.last}, $P = @{ri.n}$ forecasts', 'Ținta: inflația IAPC, anuală, cu 12 luni înainte; originile prognozelor din ianuarie 2013, ținte de la @{ri.first} pînă în @{ri.last}, $P = @{ri.n}$ prognoze'),
     [T('HICP inflation in August 2026: @{ri.lasty}\\%', 'inflația IAPC în august 2026: @{ri.lasty}\\%')]),
    (T('Forecasts', 'Prognozele'),
     [T('\\textbf{no change}: $\\hat\\pi_{t+12} = \\pi_t$; \\textbf{direct AR(3)}: $\\pi_{t+12}$ on $1, \\pi_t, \\pi_{t-1}, \\pi_{t-2}$, OLS on a 10-year rolling window', '\\textbf{fără schimbare}: $\\hat\\pi_{t+12} = \\pi_t$; \\textbf{AR(3) direct}: $\\pi_{t+12}$ pe $1, \\pi_t, \\pi_{t-1}, \\pi_{t-2}$, OLS pe o fereastră mobilă de 10 ani'),
      T('\\textbf{target}: the BNR inflation target, 2.5\\%; \\textbf{average} of AR(3) and no change', '\\textbf{ținta}: ținta de inflație a BNR, 2,5\\%; \\textbf{media} dintre AR(3) și fără schimbare')]),
    T('Overlapping 12-month targets: errors are serially correlated up to lag 11; DM with $h = 12$', 'Ținte de 12 luni care se suprapun: erorile sînt autocorelate pînă la lagul 11; DM cu $h = 12$')), 'small')

chart(T('Romanian inflation forecasts one year ahead', 'Prognoze ale inflației din România cu un an înainte'), 'ats_ch1_ro_inflation', 'ATS_ch1_dm_tests', [
    T('Left: inflation and the forecasts made 12 months earlier; right: cumulative sum of $e_{\\mathrm{nc},t}^2 - e_{m,t}^2$ (falling: model $m$ loses to no change)', 'Stînga: inflația și prognozele făcute cu 12 luni înainte; dreapta: suma cumulată a $e_{\\mathrm{nc},t}^2 - e_{m,t}^2$ (scade: modelul $m$ pierde în fața prognozei fără schimbare)')],
    h='0.50\\textheight')

D.frame(T('Interpreting the Romanian inflation comparison', 'Interpretarea comparației pentru inflația din România'), table(
    'lccccc', T('\\textbf{Forecast}', '\\textbf{Prognoza}') + ' & \\textbf{RMSE} & \\textbf{DM} & \\textbf{HLN} & ' + T('\\textbf{$p$ (HLN)}', '\\textbf{$p$ (HLN)}') + ' & ' + T('\\textbf{$p$, abs.\\ loss}', '\\textbf{$p$, pierdere abs.}'),
    [T('no change', 'fără schimbare') + ' & @{ri.rmse.rw} & -- & -- & -- & --',
     'AR(3) & @{ri.rmse.ar} & @{ri.dm.ar} & @{ri.hln.ar} & @{ri.p.ar} & @{ri.pabs.ar}',
     T('BNR target', 'ținta BNR') + ' & @{ri.rmse.target_fc} & @{ri.dm.target_fc} & @{ri.hln.target_fc} & @{ri.p.target_fc} & @{ri.pabs.target_fc}',
     T('average', 'media') + ' & @{ri.rmse.comb} & @{ri.dm.comb} & @{ri.hln.comb} & @{ri.p.comb} & @{ri.pabs.comb}'], size='footnotesize') + items(
    T('Every model has a higher RMSE than no change, yet no difference is significant: with $P = @{ri.n}$ overlapping targets the effective sample is small', 'Fiecare model are RMSE mai mare decît prognoza fără schimbare, totuși nicio diferență nu este semnificativă: cu $P = @{ri.n}$ ținte suprapuse, eșantionul efectiv este mic'),
    T('Newey--West instead of the rectangular kernel: HLN @{ri.nw.ar} for AR(3); the conclusion does not depend on the kernel', 'Newey--West în locul nucleului dreptunghiular: HLN @{ri.nw.ar} pentru AR(3); concluzia nu depinde de nucleu'),
    T('Relative RMSE of AR(3): @{ri.pre} before July 2021, @{ri.post} after: the ranking is not stable over time \\refGRaz', 'RMSE relativ al AR(3): @{ri.pre} înainte de iulie 2021, @{ri.post} după: ierarhia nu este stabilă în timp \\refGRaz')), 'footnotesize')

D.frame(T('Conditional predictive ability: Giacomini--White (1/2)', 'Capacitatea predictivă condiționată: Giacomini--White (1/2)'), items(
    (T('$H_0$: $\\E[d_{t+h} \\mid \\mathcal{G}_t] = 0$ \\refGW', '$H_0$: $\\E[d_{t+h} \\mid \\mathcal{G}_t] = 0$ \\refGW'),
     [T('$\\mathcal{G}_t$: the information at the forecast origin; $H_0$: no instrument $h_t \\in \\mathcal{G}_t$ predicts which method wins', '$\\mathcal{G}_t$: informația de la originea prognozei; $H_0$: niciun instrument $h_t \\in \\mathcal{G}_t$ nu prezice care metodă cîștigă'),
      T('$h_t$: a $q \\times 1$ vector of instruments (not the horizon $h$), e.g.\\ a constant and the last loss differential', '$h_t$: un vector de $q$ instrumente (nu orizontul $h$), de exemplu o constantă și ultimul diferențial de pierdere')]),
    (T('The statistic: a Wald test that the instruments do not predict $d_{t+h}$', 'Statistica: un test Wald că instrumentele nu prezic $d_{t+h}$'),
     ['$\\mathrm{GW} = P\\,\\bar Z\'\\hat\\Omega^{-1}\\bar Z \\to \\chi^2(q)$, $\\quad Z_t = h_t d_{t+h}$',
      T('$\\bar Z$: the mean of $Z_t$; $\\hat\\Omega$: its HAC covariance matrix with $h - 1$ lags; $\\chi^2(q)$: chi-squared with $q$ degrees of freedom', '$\\bar Z$: media lui $Z_t$; $\\hat\\Omega$: matricea ei de covarianță HAC cu $h - 1$ laguri; $\\chi^2(q)$: distribuția hi-pătrat cu $q$ grade de libertate'),
      T('$h_t = 1$ gives the unconditional test; adding $d_t$ or a state variable tests whether the past predicts the winner', '$h_t = 1$ dă testul necondiționat; adăugînd $d_t$ sau o variabilă de stare testăm dacă trecutul prezice cîștigătorul')])))

D.frame(T('Conditional predictive ability: Giacomini--White (2/2)', 'Capacitatea predictivă condiționată: Giacomini--White (2/2)'), items(
    (T('Valid with a \\textbf{rolling} window of fixed size, nested or non-nested models, any loss; invalid with a recursive window', 'Valid cu o fereastră \\textbf{mobilă} de dimensiune fixă, modele imbricate sau nu, orice pierdere; nevalid cu o fereastră recursivă'),
     [T('a rejection suggests a decision rule: use model 1 when $\\hat\\delta\'h_t > 0$, with $\\hat\\delta$ the regression of $d_{t+h}$ on $h_t$', 'o respingere sugerează o regulă de decizie: folosiți modelul 1 cînd $\\hat\\delta\'h_t > 0$, cu $\\hat\\delta$ coeficienții regresiei lui $d_{t+h}$ pe $h_t$')]),
    (T('Romanian inflation, AR(3) against no change, $h_t = (1, d_t, \\pi_t - 2.5)$', 'Inflația din România, AR(3) față de fără schimbare, $h_t = (1, d_t, \\pi_t - 2{,}5)$'),
     [T('$\\pi_t - 2.5$: the distance of inflation from the BNR target', '$\\pi_t - 2{,}5$: distanța inflației față de ținta BNR'),
      T('$\\mathrm{GW} = @{ri.gw}$, $p$ @{ri.gwp}: neither the recent loss nor the distance from the target predicts the winner', '$\\mathrm{GW} = @{ri.gw}$, p-value @{ri.gwp}: nici pierderea recentă, nici distanța față de țintă nu prezic cîștigătorul')])))

D.frame(T('Nested models: why DM fails and Clark--West (1/2)', 'Modele imbricate: de ce eșuează DM și testul Clark--West (1/2)'), items(
    (T('Model 1 (small, e.g.\\ the random walk) is nested in model 2; under $H_0$ the extra coefficients are zero', 'Modelul 1 (mic, de exemplu mersul aleator) este imbricat în modelul 2; sub $H_0$ coeficienții suplimentari sînt nuli'),
     [T('MSPE: the mean squared prediction error; population MSPEs are equal, and $d_t$ is degenerate', 'MSPE: eroarea medie pătratică de prognoză; în populație, MSPE-urile sînt egale, iar $d_t$ este degenerat'),
      T('so the DM statistic is not asymptotically Normal \\refCM', 'de aceea statistica DM nu este asimptotic Normală \\refCM')]),
    (T('In finite samples model 2 estimates zero coefficients with noise', 'În eșantion finit, modelul 2 estimează cu zgomot niște coeficienți nuli'),
     [T('its MSPE is \\textbf{larger} than that of model 1: DM is undersized (rejects too rarely) and has little power', 'MSPE-ul lui este \\textbf{mai mare} decît al modelului 1: DM respinge prea rar și are putere mică')])))

D.frame(T('Nested models: why DM fails and Clark--West (2/2)', 'Modele imbricate: de ce eșuează DM și testul Clark--West (2/2)'), items(
    (T('\\textbf{Clark--West} \\refCW: adjust the larger model for the noise it adds', '\\textbf{Clark--West} \\refCW: corectăm modelul mare pentru zgomotul pe care îl adaugă'),
     ['$f_t = e_{1t}^2 - [e_{2t}^2 - (\\hat y_{1t} - \\hat y_{2t})^2]$',
      T('$e_{1t}, e_{2t}$: the errors of the small and large model; $\\hat y_{1t}, \\hat y_{2t}$: their forecasts; the squared gap between forecasts is the noise added by model 2', '$e_{1t}, e_{2t}$: erorile modelului mic și ale celui mare; $\\hat y_{1t}, \\hat y_{2t}$: prognozele lor; diferența la pătrat dintre prognoze este zgomotul adăugat de modelul 2'),
      T('one-sided $t$ test of $\\E f_t = 0$ against $\\E f_t > 0$ (model 2 better) with Normal critical values', 'test $t$ unilateral pentru $\\E f_t = 0$ față de $\\E f_t > 0$ (modelul 2 mai bun), cu valori critice Normale')]),
    (T('Why the adjustment works', 'De ce funcționează corecția'),
     [T('under $H_0$, $\\E e_1^2 - \\E e_2^2 = -\\E(\\hat y_1 - \\hat y_2)^2$: the adjustment recentres the differential (Appendix)', 'sub $H_0$, $\\E e_1^2 - \\E e_2^2 = -\\E(\\hat y_1 - \\hat y_2)^2$: corecția recentrează diferențialul (Anexă)'),
      T('approximately Normal for rolling and recursive schemes; the exact critical values of \\refCM\\ are non-standard', 'aproximativ Normal pentru schemele mobile și recursive; valorile critice exacte din \\refCM\\ sînt nestandard')])))

D.frame(T('Case study: Meese and Rogoff on EUR/RON', 'Studiu de caz: Meese și Rogoff pentru EUR/RON'), items(
    (T('\\refMR: structural exchange-rate models do not beat the random walk out of sample at horizons up to one year', '\\refMR: modelele structurale ale cursului de schimb nu bat mersul aleator în afara eșantionului la orizonturi de pînă la un an'),
     [T('their design: rolling out-of-sample forecasts, RMSE against the random walk; the result has survived forty years', 'planul lor: prognoze în afara eșantionului cu origine mobilă, RMSE față de mersul aleator; rezultatul a rezistat patruzeci de ani')]),
    (T('Our data: monthly EUR/RON (BNR reference rate, end of month), $\\Delta s_{t+1} = 100\\Delta\\ln S_{t+1}$; recursive estimation, forecasts @{fx.first} to @{fx.last} ($P = @{fx.n}$)', 'Datele noastre: EUR/RON lunar (cursul de referință BNR, sfîrșitul lunii), $\\Delta s_{t+1} = 100\\Delta\\ln S_{t+1}$; estimare recursivă, prognoze din @{fx.first} pînă în @{fx.last} ($P = @{fx.n}$)'),
     [T('$S_t$: the rate (lei per euro); $\\Delta s_{t+1}$: its monthly log change in \\%, positive when the leu depreciates', '$S_t$: cursul (lei pentru un euro); $\\Delta s_{t+1}$: variația lui logaritmică lunară, în \\%, pozitivă cînd leul se depreciază'),
      T('nested in the random walk ($\\Delta\\hat s = 0$): drift, AR($p$), the UIP regression $\\Delta s_{t+1} = a + b(i^{RO}_t - i^{EA}_t)/12 + u$ \\refFama', 'imbricate în mersul aleator ($\\Delta\\hat s = 0$): deriva, AR($p$), regresia UIP $\\Delta s_{t+1} = a + b(i^{RO}_t - i^{ZE}_t)/12 + u$ \\refFama'),
      T('$i^{RO}_t, i^{EA}_t$: 3-month interest rates in \\% a year (divided by 12: per month); $a, b$: regression coefficients', '$i^{RO}_t, i^{ZE}_t$: dobînzile la 3 luni, în \\% pe an (împărțite la 12: pe lună); $a, b$: coeficienții regresiei'),
      T('no estimated parameters: UIP imposed ($a = 0, b = 1$), momentum (mean of the last three changes)', 'fără parametri estimați: UIP impusă ($a = 0, b = 1$), momentum (media ultimelor trei variații)')]),
    T('UIP: uncovered interest parity, the expected depreciation equals the interest differential', 'UIP: paritatea neacoperită a dobînzilor, deprecierea așteptată este egală cu diferențialul de dobîndă')), 'small')

chart(T('EUR/RON: models against the random walk', 'EUR/RON: modele față de mersul aleator'), 'ats_ch1_eurron', 'ATS_ch1_nested_spa', [
    T('Cumulative $\\sum_t(e^2_{RW,t} - e^2_{m,t})$ \\refGWel: a line below zero means model $m$ has accumulated more squared error than the random walk', 'Suma cumulată $\\sum_t(e^2_{RW,t} - e^2_{m,t})$ \\refGWel: o linie sub zero arată că modelul $m$ a acumulat mai multă eroare pătratică decît mersul aleator')],
    h='0.52\\textheight')

D.frame(T('Interpreting the EUR/RON tests', 'Interpretarea testelor pentru EUR/RON'), table(
    'lcccc', T('\\textbf{Model}', '\\textbf{Model}') + ' & ' + T('\\textbf{RMSE / RW}', '\\textbf{RMSE / RW}') + ' & ' + T('\\textbf{DM (HLN)}', '\\textbf{DM (HLN)}') + ' & \\textbf{CW} & ' + T('\\textbf{$p$ (CW, one-sided)}', '\\textbf{$p$ (CW, unilateral)}'),
    [T(e, r) + f' & @{{fx.{i}.rel}} & @{{fx.{i}.dm}} & @{{fx.{i}.cw}} & @{{fx.{i}.cwp}}' for i, (_, e, r) in enumerate(FXM)], size='scriptsize') + items(
    T('Every model has a higher RMSE than the random walk (random-walk RMSE @{fx.rmse} pp a month); the Meese--Rogoff result holds for the leu', 'Toate modelele au RMSE mai mare decît mersul aleator (RMSE al mersului aleator: @{fx.rmse} puncte procentuale pe lună); rezultatul Meese--Rogoff se confirmă pentru leu'),
    T('Clark--West does not reject either: the adjustment is not enough to make AR or UIP useful; only the drift gets close', 'Nici Clark--West nu respinge: corecția nu este suficientă pentru ca AR sau UIP să devină utile; doar deriva se apropie'),
    T('Managed float: the BNR smooths EUR/RON, so monthly changes are small and close to unpredictable from these predictors', 'Managed float: BNR netezește cursul EUR/RON, deci variațiile lunare sînt mici și aproape imprevizibile cu acești predictori')), 'footnotesize')

D.frame(T('Rationality: Mincer--Zarnowitz and encompassing (1/2)', 'Raționalitate: Mincer--Zarnowitz și încadrarea (1/2)'), items(
    (T('\\textbf{Mincer--Zarnowitz} \\refMZ: regress the outcome on the forecast', '\\textbf{Mincer--Zarnowitz} \\refMZ: regresăm realizarea pe prognoză'),
     ['$y_{t+h} = a + b\\hat y_{t+h|t} + u_{t+h}$',
      T('under squared loss an optimal forecast has $(a, b) = (0, 1)$: no bias, and a one-unit forecast change predicts a one-unit outcome change', 'sub pierdere pătratică o prognoză optimă are $(a, b) = (0, 1)$: fără deplasare, iar o variație cu o unitate a prognozei anunță o variație cu o unitate a realizării'),
      T('Wald test of $(a, b) = (0, 1)$ with HAC errors ($u$ is MA($h - 1$)); $b < 1$: forecasts too volatile; $b > 1$: too timid', 'test Wald pentru $(a, b) = (0, 1)$ cu erori HAC ($u$ este MA($h - 1$)); $b < 1$: prognoze prea volatile; $b > 1$: prea timide'),
      T('extended version: add variables in $\\mathcal{F}_t$; a significant coefficient means unused information', 'versiunea extinsă: adăugăm variabile din $\\mathcal{F}_t$; un coeficient semnificativ înseamnă informație nefolosită')]),
    T('MZ assumes squared loss: under asymmetric loss a rational forecast is biased (Section 1)', 'MZ presupune pierdere pătratică: sub pierdere asimetrică o prognoză rațională este deplasată (secțiunea 1)')))

D.frame(T('Rationality: Mincer--Zarnowitz and encompassing (2/2)', 'Raționalitate: Mincer--Zarnowitz și încadrarea (2/2)'), items(
    (T('\\textbf{Encompassing} \\refChH, \\refHLNih: forecast 1 encompasses forecast 2 if 2 adds nothing to 1', '\\textbf{Încadrarea} \\refChH, \\refHLNih: prognoza 1 o încadrează pe prognoza 2 dacă 2 nu adaugă nimic la 1'),
     ['$y = (1 - \\lambda)\\hat y_1 + \\lambda\\hat y_2 + \\varepsilon$, $\\quad H_0$: $\\lambda = 0$',
      T('$\\lambda$: the weight of forecast 2 in the best combination; $\\lambda = 0$: forecast 2 is useless given forecast 1', '$\\lambda$: ponderea prognozei 2 în cea mai bună combinație; $\\lambda = 0$: prognoza 2 este inutilă dacă avem prognoza 1'),
      T('HLN test: DM--HLN on $d_t = e_{1t}(e_{1t} - e_{2t})$, one-sided ($\\E d_t > 0$ means $\\lambda > 0$)', 'testul HLN: DM--HLN pe $d_t = e_{1t}(e_{1t} - e_{2t})$, unilateral ($\\E d_t > 0$ înseamnă $\\lambda > 0$)')]),
    T('If neither encompasses the other, a combination beats both (Section 5)', 'Dacă niciuna nu o încadrează pe cealaltă, o combinație le bate pe amîndouă (secțiunea 5)')))

D.frame(T('Case study: Atkeson and Ohanian (2001)', 'Studiu de caz: Atkeson și Ohanian (2001)'), items(
    (T('\\refAO: a naive forecast, ``inflation over the next four quarters equals inflation over the last four quarters\'\', beats Phillips-curve forecasts in the US after 1984', '\\refAO: o prognoză naivă, „inflația din următoarele patru trimestre este egală cu inflația din ultimele patru”, bate prognozele pe baza curbei Phillips în SUA după 1984'),
     [T('the Phillips curve of \\refSWii: $\\pi^4_{t+4} - \\pi^4_t = a + \\beta(L)u_t + \\gamma(L)\\Delta\\pi_t + e_{t+4}$', 'curba Phillips din \\refSWii: $\\pi^4_{t+4} - \\pi^4_t = a + \\beta(L)u_t + \\gamma(L)\\Delta\\pi_t + e_{t+4}$'),
      T('$\\pi^4_t$: inflation over the last four quarters; $\\pi_t$: quarterly inflation; $u_t$: the unemployment rate; $\\beta(L), \\gamma(L)$: lag polynomials (four lags each)', '$\\pi^4_t$: inflația pe ultimele patru trimestre; $\\pi_t$: inflația trimestrială; $u_t$: rata șomajului; $\\beta(L), \\gamma(L)$: polinoame de laguri (cîte patru laguri)')]),
    (T('Our update: CPI (quarterly average) and the unemployment rate (FRED); four lags of each, rolling window of 15 years; targets @{ao.first} to @{ao.last} ($P = @{ao.n}$)', 'Actualizarea noastră: IPC (media trimestrială) și rata șomajului (FRED); cîte patru laguri, fereastră mobilă de 15 ani; ținte din @{ao.first} pînă în @{ao.last} ($P = @{ao.n}$)'),
     [T('October 2025 CPI was not published; the 2025Q4 average uses two months', 'IPC pentru octombrie 2025 nu a fost publicat; media pentru T4 2025 folosește două luni')]),
    T('Tests: DM--HLN with $h = 4$; GW with $h_t = (1, d_{t})$ and $h_t = (1, u_t)$; encompassing in both directions', 'Teste: DM--HLN cu $h = 4$; GW cu $h_t = (1, d_t)$ și $h_t = (1, u_t)$; încadrare în ambele direcții')), 'small')

chart(T('The naive forecast against the Phillips curve', 'Prognoza naivă față de curba Phillips'), 'ats_ch1_ao', 'ATS_ch1_dm_tests', [
    T('Left: four-quarter CPI inflation and the two forecasts made four quarters earlier; right: MSE ratio on a moving 10-year window', 'Stînga: inflația IPC pe patru trimestre și cele două prognoze făcute cu patru trimestre înainte; dreapta: raportul MSE pe o fereastră mobilă de 10 ani')],
    h='0.50\\textheight')

interp(('the Atkeson--Ohanian update', 'actualizării Atkeson--Ohanian'), [
    T('RMSE: naive @{ao.rn}, Phillips curve @{ao.rp} (ratio @{ao.ratio}); by period: @{ao.r1985} (1985--2007), @{ao.r2008} (2008--2019), @{ao.r2020} (2020--2026)', 'RMSE: naivă @{ao.rn}, curba Phillips @{ao.rp} (raport @{ao.ratio}); pe perioade: @{ao.r1985} (1985--2007), @{ao.r2008} (2008--2019), @{ao.r2020} (2020--2026)'),
    (T('Yet DM--HLN = @{ao.hln}, $p$ @{ao.p}: the large post-2020 errors inflate the HAC variance as much as the mean', 'Totuși DM--HLN = @{ao.hln}, p-value @{ao.p}: erorile mari de după 2020 măresc varianța HAC la fel de mult ca media'),
     [T('the moving ratio peaks at @{ao.relmax} in @{ao.relmaxd}: the Phillips curve extrapolated the pandemic unemployment spike', 'raportul pe fereastră mobilă atinge @{ao.relmax} în @{ao.relmaxd}: curba Phillips a extrapolat saltul șomajului din pandemie')]),
    T('GW: $p$ @{ao.gwp} with the lagged differential, $p$ @{ao.gwup} with unemployment; encompassing: $H_0$ ``naive encompasses PC\'\' $p$ @{ao.encn}; ``PC encompasses naive\'\' $p$ @{ao.encp}', 'GW: p-value @{ao.gwp} cu diferențialul din perioada anterioară, $p$ @{ao.gwup} cu șomajul; încadrare: $H_0$ „naiva încadrează PC” $p$ @{ao.encn}; „PC încadrează naiva” $p$ @{ao.encp}'),
    T('The AO conclusion holds in point estimates, and a test on 41 years of overlapping data cannot separate the two', 'Concluzia AO se păstrează în estimările punctuale, iar un test pe 41 de ani de date suprapuse nu le poate separa')])

D.frame(T('Many models: data snooping, the reality check and SPA', 'Multe modele: data snooping, reality check și SPA'), items(
    (T('Testing $k$ models against a benchmark and reporting the best $p$-value is \\textbf{data snooping}', 'Testarea a $k$ modele față de un reper și raportarea celui mai mic p-value înseamnă \\textbf{data snooping}'),
     [T('$H_0$: $\\max_{j \\le k}\\E[d_{j,t}] \\le 0$ with $d_{j,t} = L_{0,t} - L_{j,t}$: no model beats the benchmark', '$H_0$: $\\max_{j \\le k}\\E[d_{j,t}] \\le 0$ cu $d_{j,t} = L_{0,t} - L_{j,t}$: niciun model nu bate reperul'),
      T('$L_{0,t}$: the loss of the benchmark; $L_{j,t}$: the loss of model $j$; $d_{j,t} > 0$: model $j$ did better at $t$', '$L_{0,t}$: pierderea reperului; $L_{j,t}$: pierderea modelului $j$; $d_{j,t} > 0$: modelul $j$ a fost mai bun la $t$')]),
    (T('\\textbf{Reality check} \\refWhite: statistic $\\max_j\\sqrt P\\bar d_j$, $p$-value from the stationary bootstrap (Chapter 0) under the least favourable configuration', '\\textbf{Reality check} \\refWhite: statistica $\\max_j\\sqrt P\\bar d_j$, p-value-ul din bootstrap-ul staționar (Capitolul 0) sub configurația cea mai puțin favorabilă'),
     [T('conservative: very poor models inflate the null distribution', 'conservator: modelele foarte slabe deplasează în sus distribuția sub ipoteza nulă')]),
    (T('\\textbf{SPA} \\refHan: studentise each $\\bar d_j$ and drop clearly inferior models from the null distribution (consistent $p$-value)', '\\textbf{SPA} \\refHan: studentizăm fiecare $\\bar d_j$ și scoatem modelele clar inferioare din distribuția sub ipoteza nulă (p-value consistent)'),
     [T('lower and upper $p$-values bracket it; the upper one equals the RC with studentisation', 'p-value-urile inferior și superior îl încadrează; cel superior este RC cu studentizare'),
      T('StepM \\refRWze\\ identifies \\emph{which} models beat the benchmark', 'StepM \\refRWze\\ identifică \\emph{care} modele bat reperul')]),
    T('EUR/RON, $k = @{fx.spa.k}$ models against the random walk: SPA $p$ = @{fx.spa.lower} (lower), @{fx.spa.consistent} (consistent), @{fx.spa.upper} (upper): no model beats it', 'EUR/RON, $k = @{fx.spa.k}$ modele față de mersul aleator: p-value SPA = @{fx.spa.lower} (inferior), @{fx.spa.consistent} (consistent), @{fx.spa.upper} (superior): niciun model nu îl bate')), 'small')

D.frame(T('The model confidence set (1/2)', 'Mulțimea de încredere a modelelor (MCS) (1/2)'), items(
    (T('\\textbf{MCS} \\refHLNaa: the set $\\hat{\\mathcal M}_{1-\\alpha}$ that contains the best model(s) with probability at least $1 - \\alpha$ asymptotically', '\\textbf{MCS} \\refHLNaa: mulțimea $\\hat{\\mathcal M}_{1-\\alpha}$ care conține cel mai bun model (sau modelele cele mai bune) cu probabilitatea de cel puțin $1 - \\alpha$, asimptotic'),
     [T('no benchmark: all models are treated symmetrically; analogous to a confidence interval for a parameter', 'fără reper: toate modelele sînt tratate simetric; analog unui interval de încredere pentru un parametru')]),
    (T('Equivalence test on the $m$ models still in the set', 'Testul de echivalență pentru cele $m$ modele rămase în mulțime'),
     ['$H_0$: $\\E[d_{i\\cdot,t}] = 0$ ⟦for all||pentru orice⟧ $i$, $\\quad d_{i\\cdot,t} = L_{i,t} - \\frac1m\\sum_j L_{j,t}$',
      T('$d_{i\\cdot,t}$: the loss of model $i$ minus the average loss of all models; positive: model $i$ is worse than average', '$d_{i\\cdot,t}$: pierderea modelului $i$ minus pierderea medie a tuturor modelelor; pozitiv: modelul $i$ este mai slab decît media'),
      T('statistic $T_{\\max} = \\max_i t_i$, $t_i = \\bar d_{i\\cdot}/\\widehat{\\mathrm{se}}(\\bar d_{i\\cdot})$: the worst model relative to the average, standardised', 'statistica $T_{\\max} = \\max_i t_i$, $t_i = \\bar d_{i\\cdot}/\\widehat{\\mathrm{se}}(\\bar d_{i\\cdot})$: cel mai slab model față de medie, standardizat')])))

D.frame(T('The model confidence set (2/2)', 'Mulțimea de încredere a modelelor (MCS) (2/2)'), items(
    (T('Algorithm: start with all models', 'Algoritmul: pornim cu toate modelele'),
     [T('if the equivalence test rejects, \\textbf{eliminate} the model with the largest $t_i$ and repeat; stop at the first non-rejection', 'dacă testul de echivalență respinge, \\textbf{eliminăm} modelul cu cel mai mare $t_i$ și repetăm; ne oprim la prima nerespingere'),
      T('a block bootstrap gives the null distribution and the standard errors', 'un bootstrap pe blocuri dă distribuția sub $H_0$ și erorile standard'),
      T('MCS $p$-value of a model: the largest test $p$-value up to its elimination; it stays in $\\hat{\\mathcal M}_{1-\\alpha}$ if this is above $\\alpha$', 'p-value-ul MCS al unui model: cel mai mare p-value al testelor pînă la eliminarea lui; modelul rămîne în $\\hat{\\mathcal M}_{1-\\alpha}$ dacă acesta depășește $\\alpha$')]),
    (T('A large MCS is a finding too', 'O mulțime MCS mare este și ea un rezultat'),
     [T('the data cannot separate the models (a weak sample, not equal models)', 'datele nu pot separa modelele (un eșantion slab, nu modele egale)')])))

D.frame(T('Case study: day-ahead electricity load in Romania', 'Studiu de caz: consumul de electricitate din România pentru ziua următoare'), two(
    ph('pylon', T('A 400 kV line, Predeluș Pass (2018)', 'O linie de 400 kV, Pasul Predeluș (2018)'), h='0.36\\textheight'),
    items((T('Target: the 24 hourly loads of day $d + 1$ with data up to day $d$; @{lo.first} to @{lo.last} ($@{lo.n}$ days); mean @{lo.mean} GW', 'Ținta: cele 24 de consumuri orare ale zilei $d + 1$, cu date pînă în ziua $d$; @{lo.first} -- @{lo.last} ($@{lo.n}$ zile); media @{lo.mean} GW'),
           [T('quantile forecasts at the 99 percentiles, scored by the average pinball loss as in GEFCom2014 \\refGEF, \\refHF', 'prognoze de cuantile la cele 99 de percentile, evaluate prin pierderea pinball medie ca în GEFCom2014 \\refGEF, \\refHF')]),
          (T('Models: naive day, weekly naive, mean of 4 weeks; the \\textbf{expert ARX} of \\refZW\\ for each hour', 'Modele: naiv zi, naiv săptămînal, media pe 4 săptămîni; \\textbf{ARX expert} din \\refZW\\ pentru fiecare oră'),
           [T('regressors: $y_{d,h}, y_{d-1,h}, y_{d-6,h}$, min and max of day $d$, last hour of $d$, Monday, Saturday, Sunday; one-year rolling window', 'regresori: $y_{d,h}, y_{d-1,h}, y_{d-6,h}$, minimul și maximul zilei $d$, ultima oră din $d$, luni, sîmbătă, duminică; fereastră mobilă de un an'),
            T('quantiles: point forecast plus the empirical quantiles of the last 182 errors at the same hour', 'cuantile: prognoza punctuală plus cuantilele empirice ale ultimelor 182 de erori la aceeași oră')]),
          T('ARX: autoregression with exogenous variables (here calendar dummies)', 'ARX: autoregresie cu variabile exogene (aici variabile calendaristice)')), '0.36', '0.62'), 'footnotesize')

chart(T('A winter week of load forecasts', 'O săptămînă de iarnă cu prognoze de consum'), 'ats_ch1_load_week', 'ATS_ch1_load_mcs', [
    T('12--18 January 2026; the weekly naive forecast copies the holiday week of 5--9 January (Orthodox Epiphany and St John, 6--7 January)', '12--18 ianuarie 2026; prognoza naivă săptămînală copiază săptămîna cu sărbători 5--9 ianuarie (Boboteaza și Sfîntul Ion, 6--7 ianuarie)')],
    h='0.50\\textheight')

chart(T('Average pinball loss and the 90\\% MCS', 'Pierderea pinball medie și MCS de 90\\%'), 'ats_ch1_load_mcs', 'ATS_ch1_load_mcs', [
    T('Daily average losses; MCS with $T_{\\max}$, moving-block bootstrap (blocks of 7 days), 2000 replications; green: in the MCS', 'Pierderi medii zilnice; MCS cu $T_{\\max}$, bootstrap pe blocuri mobile (blocuri de 7 zile), 2000 de replicări; verde: în MCS')],
    h='0.46\\textheight')

D.frame(T('Interpreting the load comparison', 'Interpretarea comparației pentru consumul de electricitate'), table(
    'lcccc', T('\\textbf{Model}', '\\textbf{Model}') + ' & ' + T('\\textbf{Pinball (MW)}', '\\textbf{Pinball (MW)}') + ' & \\textbf{MAE (MW)} & ' + T('\\textbf{90\\% coverage}', '\\textbf{Acoperire 90\\%}') + ' & ' + T('\\textbf{MCS $p$}', '\\textbf{$p$ MCS}'),
    [T(e, r) + f' & @{{lo.{i}.pin}} & @{{lo.{i}.mae}} & @{{lo.{i}.cov}}\\% & @{{lo.{i}.mcs}}' for i, (_, e, r) in enumerate(LN)], size='scriptsize') + items(
    T('The expert ARX halves the losses of the naive rules and is alone in the MCS; DM--HLN against the ARX + mean combination: @{lo.dmc}', 'ARX expert înjumătățește pierderile regulilor naive și este singur în MCS; DM--HLN față de combinația ARX + medie: @{lo.dmc}'),
    T('Here combining with a much worse forecast hurts: equal weights help only when the forecasts are of similar quality (Section 5)', 'Aici combinarea cu o prognoză mult mai slabă strică: ponderile egale ajută doar cînd prognozele au calitate asemănătoare (secțiunea 5)'),
    T('All intervals under-cover slightly; the largest losses fall on and right after public holidays (@{lo.worst}): calendar effects are the next improvement', 'Toate intervalele acoperă puțin sub nivelul nominal; cele mai mari pierderi cad în zilele de sărbătoare legală și imediat după ele (@{lo.worst}): efectele calendaristice sînt următoarea îmbunătățire')), 'footnotesize')

D.recap(('Comparing forecasts', 'compararea prognozelor'), [
    T('DM compares forecasts; with estimated models choose West (population) or GW (methods, rolling window)', 'DM compară prognoze; pentru modele estimate alegeți West (populație) sau GW (metode, fereastră mobilă)'),
    T('Multi-step, small $P$: HAC variance plus the HLN correction and $t_{P-1}$', 'Mai mulți pași, $P$ mic: varianță HAC plus corecția HLN și $t_{P-1}$'),
    T('Nested models: Clark--West; many models: SPA or the MCS, never the best $p$-value', 'Modele imbricate: Clark--West; multe modele: SPA sau MCS, niciodată cel mai mic p-value'),
    T('Romanian inflation, US inflation, EUR/RON: the simple benchmark is hard to beat and differences are rarely significant', 'Inflația din România, inflația din SUA, EUR/RON: reperul simplu se bate greu, iar diferențele sînt rareori semnificative')])

# =============================================================================
# 5. COMBINARE
# =============================================================================
D.section('Forecast combination', 'Combinarea prognozelor')

D.frame(T('Bates and Granger (1969)', 'Bates și Granger (1969)'), two(
    ph('granger', T('Clive W.~J.\\ Granger (1934--2009), Nobel Memorial Prize 2003', 'Clive W.~J.\\ Granger (1934--2009), Premiul Nobel pentru Economie 2003'), h='0.32\\textheight'),
    items((T('Two unbiased forecasts with error variances $\\sigma_1^2, \\sigma_2^2$ and covariance $\\sigma_{12}$; combination $w\\hat y_1 + (1 - w)\\hat y_2$ \\refBG', 'Două prognoze nedeplasate cu varianțele erorilor $\\sigma_1^2, \\sigma_2^2$ și covarianța $\\sigma_{12}$; combinația $w\\hat y_1 + (1 - w)\\hat y_2$ \\refBG'),
           [T('error variance $w^2\\sigma_1^2 + (1 - w)^2\\sigma_2^2 + 2w(1 - w)\\sigma_{12}$, minimised at', 'varianța erorii $w^2\\sigma_1^2 + (1 - w)^2\\sigma_2^2 + 2w(1 - w)\\sigma_{12}$, minimă pentru'),
            T('$w^* = \\dfrac{\\sigma_2^2 - \\sigma_{12}}{\\sigma_1^2 + \\sigma_2^2 - 2\\sigma_{12}}$, \\quad $\\sigma^2_c = \\dfrac{\\sigma_1^2\\sigma_2^2 - \\sigma_{12}^2}{\\sigma_1^2 + \\sigma_2^2 - 2\\sigma_{12}} \\le \\min(\\sigma_1^2, \\sigma_2^2)$', '$w^* = \\dfrac{\\sigma_2^2 - \\sigma_{12}}{\\sigma_1^2 + \\sigma_2^2 - 2\\sigma_{12}}$, \\quad $\\sigma^2_c = \\dfrac{\\sigma_1^2\\sigma_2^2 - \\sigma_{12}^2}{\\sigma_1^2 + \\sigma_2^2 - 2\\sigma_{12}} \\le \\min(\\sigma_1^2, \\sigma_2^2)$'),
            T('$\\sigma^2_c$: the error variance of the optimal combination, never above that of the better forecast; the less precise forecast gets the smaller weight', '$\\sigma^2_c$: varianța erorii combinației optime, niciodată peste cea a prognozei mai bune; prognoza mai puțin precisă primește ponderea mai mică')]),
          (T('$N$ forecasts: $\\mathbf w^* = \\Sigma^{-1}\\iota/(\\iota\'\\Sigma^{-1}\\iota)$, with $\\Sigma$ the covariance matrix of the errors and $\\iota$ a vector of ones; \\refGRm: regress $y$ on the forecasts, with or without a constant and the sum-to-one restriction', '$N$ prognoze: $\\mathbf w^* = \\Sigma^{-1}\\iota/(\\iota\'\\Sigma^{-1}\\iota)$, cu $\\Sigma$ matricea de covarianță a erorilor și $\\iota$ un vector de unu; \\refGRm: regresia lui $y$ pe prognoze, cu sau fără termen liber și restricția ca ponderile să însumeze 1'),
           [T('combination diversifies model risk, structural breaks and the private information of forecasters \\refTim', 'combinarea diversifică riscul de model, rupturile structurale și informația privată a prognozatorilor \\refTim')])), '0.30', '0.68'), 'footnotesize')

D.frame(T('The forecast combination puzzle', 'Paradoxul combinării prognozelor'), items(
    (T('Empirical regularity: the simple average beats the ``optimal\'\' estimated weights \\refSWzd, \\refTim, \\refGKMT', 'Regularitate empirică: media simplă bate ponderile „optime” estimate \\refSWzd, \\refTim, \\refGKMT'),
     [T('Stock--Watson: across 7 countries and many predictors of output growth, equal weights and the median are among the best combinations', 'Stock--Watson: în 7 țări și cu mulți predictori ai creșterii economice, ponderile egale și mediana sînt printre cele mai bune combinații')]),
    (T('\\textbf{Explanation} \\refSWal, \\refCMVW: the weights are estimated', '\\textbf{Explicația} \\refSWal, \\refCMVW: ponderile sînt estimate'),
     [T('$\\E[\\mathrm{MSE}(\\hat w)] = \\mathrm{MSE}(w^*) + \\E(\\hat w - w^*)^2 D$, $D = \\sigma_1^2 + \\sigma_2^2 - 2\\sigma_{12}$ (the variance of $e_1 - e_2$)', '$\\E[\\mathrm{MSE}(\\hat w)] = \\mathrm{MSE}(w^*) + \\E(\\hat w - w^*)^2 D$, $D = \\sigma_1^2 + \\sigma_2^2 - 2\\sigma_{12}$ (varianța lui $e_1 - e_2$)'),
      T('$\\hat w$: the weight estimated from $n$ past errors; MSE: the mean squared error of the combination', '$\\hat w$: ponderea estimată din $n$ erori trecute; MSE: eroarea pătratică medie a combinației'),
      T('gain of $w^*$ over $1/2$: $(w^* - 1/2)^2D$; loss from estimating: $\\mathrm{Var}(\\hat w)D$, of order $1/n$', 'cîștigul lui $w^*$ față de $1/2$: $(w^* - 1/2)^2D$; pierderea din estimare: $\\mathrm{Var}(\\hat w)D$, de ordinul $1/n$'),
      T('equal weights win when $(w^* - 1/2)^2 < \\mathrm{Var}(\\hat w)$: similar forecasts, short samples, correlated errors', 'ponderile egale cîștigă cînd $(w^* - 1/2)^2 < \\mathrm{Var}(\\hat w)$: prognoze asemănătoare, eșantioane scurte, erori corelate')]),
    T('Also: weights move with breaks, so long windows are biased and short ones noisy', 'În plus: ponderile se schimbă la rupturi, deci ferestrele lungi sînt deplasate, iar cele scurte zgomotoase')), 'small')

chart(T('The puzzle by simulation', 'Paradoxul prin simulare'), 'ats_ch1_puzzle', 'ATS_ch1_combination', [
    T('Bivariate Normal errors with $\\sigma_1^2 = 1$; weights estimated from $n$ past errors; @{pz.reps} replications; dotted: population ratio $\\mathrm{MSE}(w^*)/\\mathrm{MSE}(1/2)$', 'Erori Normale bivariate cu $\\sigma_1^2 = 1$; ponderi estimate din $n$ erori trecute; @{pz.reps} de replicări; punctat: raportul în populație $\\mathrm{MSE}(w^*)/\\mathrm{MSE}(1/2)$')],
    h='0.64\\textheight')

interp(('the puzzle simulation', 'simulării paradoxului'), [
    T('Similar forecasts ($w^* = @{pz.w1}$): the optimal weight lowers the population MSE only to @{pz.pop1} of the equal-weight MSE, while estimating it costs: ratio @{pz.r10} at $n = 10$, @{pz.r40} at $n = 40$', 'Prognoze asemănătoare ($w^* = @{pz.w1}$): ponderea optimă reduce MSE-ul din populație doar la @{pz.pop1} din MSE-ul ponderilor egale, iar estimarea ei costă: raport @{pz.r10} la $n = 10$, @{pz.r40} la $n = 40$'),
    T('Moderately different ($w^* = @{pz.w2}$): estimated weights need about 20 past errors to break even (@{pz.r2_10} at $n = 10$, @{pz.r2_40} at $n = 40$)', 'Moderat diferite ($w^* = @{pz.w2}$): ponderile estimate au nevoie de aproximativ 20 de erori trecute ca să nu piardă (@{pz.r2_10} la $n = 10$, @{pz.r2_40} la $n = 40$)'),
    T('Very different ($w^* = @{pz.w3}$): estimate the weights, or drop the weak forecast; the load case of Section 4 is of this kind', 'Foarte diferite ($w^* = @{pz.w3}$): estimați ponderile sau renunțați la prognoza slabă; cazul consumului de electricitate din secțiunea 4 este de acest tip')])

D.frame(T('Between equal and optimal: shrinkage and robust combinations', 'Între ponderi egale și optime: shrinkage și combinări robuste'), items(
    (T('\\textbf{Shrinkage}: $\\hat w_\\lambda = \\lambda\\hat w + (1 - \\lambda)\\iota/N$ \\refDP, \\refSWzd', '\\textbf{Shrinkage}: $\\hat w_\\lambda = \\lambda\\hat w + (1 - \\lambda)\\iota/N$ \\refDP, \\refSWzd'),
     [T('$\\hat w$: the estimated weights; $\\iota/N$: equal weights for $N$ forecasts; $\\lambda \\in [0,1]$: $\\lambda = 0$ gives the mean, $\\lambda = 1$ the estimated weights', '$\\hat w$: ponderile estimate; $\\iota/N$: ponderi egale pentru $N$ prognoze; $\\lambda \\in [0,1]$: $\\lambda = 0$ dă media, $\\lambda = 1$ ponderile estimate'),
      T('a Bayesian prior centred on equal weights; $\\lambda$ falls with the number of forecasts and rises with the sample', 'un prior bayesian centrat pe ponderile egale; $\\lambda$ scade cu numărul de prognoze și crește cu eșantionul')]),
    (T('\\textbf{Performance weights}: $w_i \\propto 1/\\mathrm{MSE}_i$ on a recent window, ignoring correlations; discounting gives recent errors more weight', '\\textbf{Ponderi după performanță}: $w_i \\propto 1/\\mathrm{MSE}_i$ pe o fereastră recentă, ignorînd corelațiile; actualizarea dă erorilor recente o pondere mai mare'),
     [T('\\textbf{previous best}: select the forecaster with the lowest past MSE (a weight of one)', '\\textbf{cel mai bun anterior}: alegem prognozatorul cu cel mai mic MSE trecut (o pondere egală cu 1)')]),
    (T('\\textbf{Robust}: median, trimmed mean: protect against outlying forecasters', '\\textbf{Robuste}: mediana, media trunchiată: protejează împotriva prognozatorilor extremi'), []),
    (T('Panels of experts change: forecasters enter and exit, so $\\Sigma$ is never fully observed \\refCT', 'Panelurile de experți se schimbă: prognozatorii intră și ies, deci $\\Sigma$ nu este niciodată observată complet \\refCT'),
     [T('performance weights need a minimum record; a review of 50 years of practice: \\refWHLK', 'ponderile după performanță cer un istoric minim; o sinteză a 50 de ani de practică: \\refWHLK')])), 'small')

D.frame(T('Combining density forecasts', 'Combinarea prognozelor de densitate'), items(
    (T('\\textbf{Linear pool}: $p(y) = \\sum_i w_ip_i(y)$, $w_i \\ge 0$, $\\sum w_i = 1$ \\refHM', '\\textbf{Combinarea liniară} (linear pool): $p(y) = \\sum_i w_ip_i(y)$, $w_i \\ge 0$, $\\sum w_i = 1$ \\refHM'),
     [T('$p_i$: the density forecast of model $i$; $w_i$: its weight; the pool is a mixture of the densities', '$p_i$: prognoza de densitate a modelului $i$; $w_i$: ponderea ei; combinarea este o mixtură de densități'),
      T('weights that minimise the average log score: \\textbf{optimal prediction pools} \\refGA', 'ponderile care minimizează scorul logaritmic mediu: \\textbf{optimal prediction pools} \\refGA'),
      T('interior weights even when every model is misspecified: a pool is not a model average in the Bayesian sense', 'ponderi interioare chiar dacă toate modelele sînt greșit specificate: o combinare nu este o medie de modele în sens bayesian')]),
    (T('The linear pool of calibrated densities is \\textbf{over-dispersed} \\refGRjac', 'Combinarea liniară a unor densități calibrate este \\textbf{supradispersată} \\refGRjac'),
     [T('the mixture adds the variance of the means; remedy: a beta-transformed pool or quantile averaging (Vincentisation)', 'mixtura adaugă varianța mediilor; remediul: o combinare transformată beta sau medierea cuantilelor (vincentizare)')]),
    T('Proper scores (Section 3) are the natural criteria for estimating and comparing pools', 'Scorurile proprii (secțiunea 3) sînt criteriile naturale pentru estimarea și compararea combinărilor')), 'small')

chart(T('Optimal pools for the S\\&P 500 densities', 'Combinări optime pentru densitățile S\\&P 500'), 'ats_ch1_pool', 'ATS_ch1_density_forecasts', [
    T('Average log score of $wp_{\\mathrm{GARCH}\\text{-}t} + (1 - w)p_2$ on 2013--2026; dots: minima', 'Scorul logaritmic mediu al $wp_{\\mathrm{GARCH}\\text{-}t} + (1 - w)p_2$ pe 2013--2026; punctele: minimele'),
    T('With the i.i.d.\\ Normal: $w^* = @{pool.w1}$, score @{pool.ls1} against @{pool.lsa} for GARCH-$t$ alone; with GARCH-N: $w^* = @{pool.w2}$: GARCH-$t$ dominates, the pool adds almost nothing', 'Cu i.i.d.\\ Normal: $w^* = @{pool.w1}$, scorul @{pool.ls1} față de @{pool.lsa} pentru GARCH-$t$ singur; cu GARCH-N: $w^* = @{pool.w2}$: GARCH-$t$ domină, combinarea nu adaugă aproape nimic')],
    h='0.46\\textheight')

interp(('the optimal pools', 'combinărilor optime'), [
    T('The pool with the i.i.d.\\ Normal puts almost all weight on GARCH-$t$: a small Normal component only insures against extreme days', 'Combinarea cu i.i.d.\\ Normal pune aproape toată ponderea pe GARCH-$t$: o mică componentă Normală doar asigură împotriva zilelor extreme'),
    T('With GARCH-N the optimum is the corner $w = 1$: the two GARCH densities carry the same information, the $t$ tails are simply better', 'Cu GARCH-N optimul este colțul $w = 1$: cele două densități GARCH conțin aceeași informație, cozile $t$ sînt pur și simplu mai bune'),
    T('Weights estimated on the evaluation sample are optimistic; in practice estimate them on a past window and evaluate on the next', 'Ponderile estimate pe eșantionul de evaluare sînt optimiste; în practică estimați-le pe o fereastră trecută și evaluați pe următoarea')])

D.frame(T('Case study: can anything beat the simple average?', 'Studiu de caz: poate ceva să bată media simplă?'), two(
    ph('fed', T('Federal Reserve Bank of Philadelphia, home of the SPF since 1990', 'Federal Reserve Bank of Philadelphia, unde se află SPF din 1990'), h='0.30\\textheight'),
    items((T('\\refGKMT\\ compare combination schemes on the ECB Survey of Professional Forecasters: equal weights, median, trimmed mean, performance-based weights, shrinkage, and others', '\\refGKMT\\ compară scheme de combinare pe Survey of Professional Forecasters al BCE: ponderi egale, mediana, media trunchiată, ponderi după performanță, shrinkage și altele'),
           [T('their answer: rarely, and not robustly over time', 'răspunsul lor: rareori și nu robust în timp')]),
          (T('We apply their schemes to the US SPF: CPI inflation (annualised q/q) four quarters after the survey quarter; surveys @{sp.first}--@{sp.last} ($P = @{sp.n}$, @{sp.nf} forecasters, on average @{sp.panel} per survey)', 'Aplicăm schemele lor pe SPF din SUA: inflația IPC (anualizată, trimestrială) la patru trimestre după trimestrul anchetei; anchete @{sp.first}--@{sp.last} ($P = @{sp.n}$, @{sp.nf} prognozatori, în medie @{sp.panel} pe anchetă)'),
           [T('performance weights: inverse MSE over the last 20 surveys with a known outcome, at least 8 past forecasts (on average @{sp.ok} eligible); trimmed mean: 10\\% on each side', 'ponderi după performanță: inversul MSE pe ultimele 20 de anchete cu realizare cunoscută, cel puțin 8 prognoze trecute (în medie @{sp.ok} eligibili); media trunchiată: 10\\% din fiecare parte')])), '0.32', '0.66'), 'footnotesize')

chart(T('Individual SPF forecasts and the outcome', 'Prognozele individuale SPF și realizarea'), 'ats_ch1_spf', 'ATS_ch1_spf_combination', [
    T('Each dot: one forecaster\'s CPI forecast for the quarter four quarters ahead, placed at the target quarter; the outcome is far more volatile than any forecast', 'Fiecare punct: prognoza IPC a unui prognozator pentru trimestrul de peste patru trimestre, plasată la trimestrul-țintă; realizarea este mult mai volatilă decît orice prognoză')],
    h='0.64\\textheight')

chart(T('Combination schemes against the mean', 'Scheme de combinare față de medie'), 'ats_ch1_spf_schemes', 'ATS_ch1_spf_combination', [
    T('RMSE relative to the equal-weight mean (RMSE @{sp.rmse} pp); blue: at least as good as the mean', 'RMSE relativ la media cu ponderi egale (RMSE @{sp.rmse} puncte procentuale); albastru: cel puțin la fel de bun ca media')],
    h='0.44\\textheight')

D.frame(T('Interpreting the SPF combination', 'Interpretarea combinării SPF'), items(
    (T('Median @{sp.0.rel}, trimmed mean @{sp.1.rel}, inverse-MSE @{sp.4.rel}, previous best @{sp.5.rel} (relative RMSE)', 'Mediana @{sp.0.rel}, media trunchiată @{sp.1.rel}, inversul MSE @{sp.4.rel}, cel mai bun anterior @{sp.5.rel} (RMSE relativ)'),
     [T('DM--HLN against the mean: median $p$ @{sp.0.p}; inverse MSE $p$ @{sp.4.p}; previous best HLN @{sp.5.dm}, $p$ @{sp.5.p}', 'DM--HLN față de medie: mediana $p$ @{sp.0.p}; inversul MSE $p$ @{sp.4.p}; cel mai bun anterior HLN @{sp.5.dm}, $p$ @{sp.5.p}'),
      T('Genre et al.\'s answer holds on US data: nothing beats the average significantly, and chasing the past winner loses', 'Răspunsul lui Genre et al.\\ se confirmă pe datele SUA: nimic nu bate media semnificativ, iar urmărirea cîștigătorului trecut pierde')]),
    (T('Yet @{sp.indbeat}\\% of the @{sp.indn} forecasters with at least 20 forecasts have a lower RMSE than the mean', 'Totuși @{sp.indbeat}\\% dintre cei @{sp.indn} prognozatori cu cel puțin 20 de prognoze au RMSE mai mic decît media'),
     [T('they are known only ex post, over different and shorter samples: survivorship and luck, not skill one could have selected', 'sînt cunoscuți doar ex post, pe eșantioane diferite și mai scurte: supraviețuire și noroc, nu abilitate care putea fi selectată')]),
    T('Mincer--Zarnowitz on the mean: $\\hat b = @{sp.mzb}$ (SE @{sp.mzsb}), $R^2 = @{sp.mzr2}$, $p$ @{sp.mzp}: one-year-ahead quarterly CPI inflation is almost unpredictable; the forecasts are smooth, the outcomes noisy', 'Mincer--Zarnowitz pentru medie: $\\hat b = @{sp.mzb}$ (SE @{sp.mzsb}), $R^2 = @{sp.mzr2}$, $p$ @{sp.mzp}: inflația IPC trimestrială cu un an înainte este aproape imprevizibilă; prognozele sînt netede, realizările zgomotoase')), 'footnotesize')

D.frame(T('Lessons from the M4 and M5 competitions', 'Lecțiile competițiilor M4 și M5'), items(
    (T('\\textbf{M4} (2018) \\refMd: 100{,}000 series, 61 methods, point forecasts and 95\\% intervals', '\\textbf{M4} (2018) \\refMd: 100.000 de serii, 61 de metode, prognoze punctuale și intervale de 95\\%'),
     [T('the winner was a hybrid of exponential smoothing and a recurrent neural network; the second, a combination of statistical methods with weights learned by a meta-learner', 'cîștigătorul a fost un hibrid între netezirea exponențială și o rețea neuronală recurentă; locul doi, o combinație de metode statistice cu ponderi învățate de un meta-model'),
      T('combinations dominated the top places; pure machine learning methods did poorly; prediction intervals were too narrow for most methods', 'combinațiile au dominat primele locuri; metodele de machine learning pure au avut rezultate slabe; intervalele de predicție au fost prea înguste pentru majoritatea metodelor')]),
    (T('\\textbf{M5} (2020) \\refMe: 42{,}840 hierarchical Walmart sales series, weighted scaled errors', '\\textbf{M5} (2020) \\refMe: 42.840 de serii ierarhice de vînzări Walmart, erori scalate ponderate'),
     [T('gradient-boosted trees (LightGBM) trained \\emph{across} series won; exogenous variables (prices, events) and cross-learning mattered', 'arborii cu gradient boosting (LightGBM) antrenați \\emph{pe toate} seriile au cîștigat; variabilele exogene (prețuri, evenimente) și învățarea între serii au contat'),
      T('again, ensembles of many models were at the top (Chapter 12)', 'din nou, ansamblurile de multe modele au fost în frunte (Capitolul 12)')]),
    T('Common lesson: combine, evaluate with scale-free scores (MASE, Chapter 0 of TSA) and proper scores, and report uncertainty that is calibrated', 'Lecția comună: combinați, evaluați cu scoruri independente de scală (MASE, TSA, Capitolul 0) și cu scoruri proprii și raportați o incertitudine calibrată')), 'small')

D.recap(('Combination', 'combinarea'), [
    T('Optimal weights reduce the error variance; estimated weights add a cost of order $1/n$', 'Ponderile optime reduc varianța erorii; ponderile estimate adaugă un cost de ordinul $1/n$'),
    T('The puzzle: when forecasts are similar, equal weights, the median and the trimmed mean win', 'Paradoxul: cînd prognozele sînt asemănătoare, cîștigă ponderile egale, mediana și media trunchiată'),
    T('Linear pools of densities are over-dispersed; estimate them by the log score', 'Combinările liniare de densități sînt supradispersate; estimați-le prin scorul logaritmic'),
    T('US SPF: no scheme beats the mean significantly; selecting the past winner loses', 'SPF din SUA: nicio schemă nu bate media semnificativ; alegerea cîștigătorului trecut pierde')])

# =============================================================================
# 6. DATE ÎN TIMP REAL
# =============================================================================
D.section('Real-time data', 'Date în timp real')

D.frame(T('Vintages and revisions', 'Versiuni ale datelor și revizuiri'), items(
    (T('Macroeconomic data are revised: US GDP is first published about 30 days after the quarter and revised for years (benchmark revisions, new methods)', 'Datele macroeconomice se revizuiesc: PIB-ul SUA este publicat prima dată la aproximativ 30 de zile după trimestru și revizuit ani la rînd (revizuiri de referință, metode noi)'),
     [T('a \\textbf{vintage} is the data set as available on a given date; the real-time data set stores all vintages \\refCS', 'o \\textbf{versiune} este setul de date așa cum era disponibil la o anumită dată; setul de date în timp real păstrează toate versiunile \\refCS')]),
    (T('Sources without a key: ALFRED (St.\\ Louis Fed, vintages of FRED series), the Philadelphia Fed RTDSM; the ECB keeps a real-time database for the euro area; INS publishes a flash estimate of GDP and later revised estimates', 'Surse fără cheie: ALFRED (St.\\ Louis Fed, versiunile seriilor FRED), RTDSM al Philadelphia Fed; BCE păstrează o bază de date în timp real pentru zona euro; INS publică o estimare semnal a PIB și estimări revizuite ulterior'),
     [T('forecasts made with latest-vintage data overstate what was predictable in real time \\refSC, \\refCr', 'prognozele făcute cu ultima versiune a datelor exagerează ce se putea prezice în timp real \\refSC, \\refCr')]),
    T('Question for the evaluation: which vintage is the ``truth\'\'? The first release (what forecasters target) or the latest (the best estimate of reality)?', 'Întrebarea pentru evaluare: ce versiune este „adevărul”? Prima publicare (ținta prognozatorilor) sau ultima (cea mai bună estimare a realității)?')), 'small')

chart(T('US real GDP growth: first release and latest vintage', 'Creșterea PIB real în SUA: prima publicare și ultima versiune'), 'ats_ch1_realtime', 'ATS_ch1_real_time', [
    T('Annualised q/q growth, 1990--2026; revisions = latest minus first release (Philadelphia Fed RTDSM); the 2025Q4 first release is missing (government shutdown)', 'Creșterea trimestrială anualizată, 1990--2026; revizuirile = ultima versiune minus prima publicare (Philadelphia Fed RTDSM); prima publicare pentru T4 2025 lipsește (închiderea guvernului federal)')],
    h='0.48\\textheight')

interp(('the revisions', 'revizuirilor'), [
    (T('Mean revision @{rt.mean} pp, standard deviation @{rt.sd} pp, mean absolute revision @{rt.mad} pp over @{rt.n} quarters; correlation first--latest @{rt.corr}', 'Revizuirea medie @{rt.mean} pp, abaterea standard @{rt.sd} pp, revizuirea absolută medie @{rt.mad} pp pe @{rt.n} trimestre; corelația prima--ultima @{rt.corr}'),
     [T('largest: @{rt.big0} (@{rt.big0v} pp) and @{rt.big1} (@{rt.big1v} pp): revisions are large exactly at turning points', 'cele mai mari: @{rt.big0} (@{rt.big0v} pp) și @{rt.big1} (@{rt.big1v} pp): revizuirile sînt mari exact la punctele de cotitură')]),
    T('SPF current-quarter nowcast ($P = @{rt.nspf}$): RMSE @{rt.rf} against the first release, @{rt.rl} against the latest; MZ slope @{rt.bf} and @{rt.bl}', 'Nowcast-ul SPF pentru trimestrul curent ($P = @{rt.nspf}$): RMSE @{rt.rf} față de prima publicare, @{rt.rl} față de ultima; panta MZ @{rt.bf} și @{rt.bl}'),
    T('The ranking of forecasters and models can change with the vintage: state the choice in the pre-registration', 'Ierarhia prognozatorilor și a modelelor se poate schimba cu versiunea: precizați alegerea în preînregistrare')])

D.frame(T('A pre-registered evaluation design', 'Un plan de evaluare preînregistrat'), items(
    (T('Fix \\textbf{before} looking at the out-of-sample results', 'Fixați \\textbf{înainte} de a vedea rezultatele în afara eșantionului'),
     [T('target, horizons, loss or score (Sections 1--3), vintage of the outcome, evaluation period, estimation scheme and window', 'ținta, orizonturile, pierderea sau scorul (secțiunile 1--3), versiunea realizării, perioada de evaluare, schema și fereastra de estimare'),
      T('benchmark (random walk, seasonal naive, survey mean) and the full list of competing models', 'reperul (mersul aleator, naiv sezonier, media anchetei) și lista completă a modelelor concurente'),
      T('tests: DM--HLN or GW; Clark--West if nested; SPA or MCS for many models; a correction for several horizons (Holm)', 'testele: DM--HLN sau GW; Clark--West pentru modele imbricate; SPA sau MCS pentru multe modele; o corecție pentru mai multe orizonturi (Holm)')]),
    (T('Report everything that was tried; a model selected on the test period has a biased error', 'Raportați tot ce s-a încercat; un model selectat pe perioada de test are o eroare deplasată'),
     [T('the project of this course starts with exactly such a plan (proposal and pre-registration, 5\\%)', 'proiectul acestui curs începe exact cu un astfel de plan (propunerea și preînregistrarea, 5\\%)')])), 'small')

D.recap(('Real-time data', 'date în timp real'), [
    T('Evaluate forecasts with the data that existed when they were made', 'Evaluați prognozele cu datele care existau cînd au fost făcute'),
    T('Revisions are large at turning points; the choice of the ``truth\'\' vintage changes RMSE and rankings', 'Revizuirile sînt mari la punctele de cotitură; alegerea versiunii „adevărate” schimbă RMSE și ierarhiile'),
    T('Pre-register targets, losses, benchmarks, tests and the vintage', 'Preînregistrați țintele, pierderile, reperele, testele și versiunea datelor')])

# =============================================================================
# 7. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Does the forecast combination puzzle survive when the panel of experts changes over time and the outcome distribution shifts (2020--2023)?', 'Rezistă paradoxul combinării cînd panelul de experți se schimbă în timp, iar distribuția realizărilor se deplasează (2020--2023)?'),
     [T('formal: $H_0$: $\\E[(y - \\hat y_{\\lambda})^2 - (y - \\bar y)^2] \\ge 0$ for every shrinkage factor $\\lambda$ fixed in advance, in every sub-period', 'formal: $H_0$: $\\E[(y - \\hat y_{\\lambda})^2 - (y - \\bar y)^2] \\ge 0$ pentru orice factor de shrinkage $\\lambda$ fixat dinainte, în fiecare subperioadă'),
      T('$\\hat y_\\lambda$: the shrinkage combination with factor $\\lambda$; $\\bar y$: the mean of all forecasters', '$\\hat y_\\lambda$: combinația shrinkage cu factorul $\\lambda$; $\\bar y$: media tuturor prognozatorilor'),
      T('falsified by a pre-registered $\\lambda$ that beats the mean with DM--HLN $p < 0.05$ after a Holm correction across sub-periods', 'infirmată de un $\\lambda$ preînregistrat care bate media cu DM--HLN și p-value $< 0{,}05$ după o corecție Holm pe subperioade')]),
    (T('Why it matters: central banks publish the survey mean; a better combination would change the published expectations', 'De ce contează: băncile centrale publică media anchetelor; o combinare mai bună ar schimba așteptările publicate'),
     [T('literature to start from: \\refGKMT, \\refCT, \\refSWal, \\refCMVW, \\refWHLK', 'literatura de pornire: \\refGKMT, \\refCT, \\refSWal, \\refCMVW, \\refWHLK')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T('\\textbf{literature}: \\aiprompt{List peer-reviewed papers on combining SPF forecasts with entry and exit of forecasters; give DOIs.} Then check every DOI on Crossref', '\\textbf{literatura}: \\aiprompt{Listează articole recenzate despre combinarea prognozelor SPF cu intrarea și ieșirea prognozatorilor; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T('\\textbf{hypothesis}: \\aiprompt{Propose three reasons why inverse-MSE weights could beat the mean after 2020, each with a test.}', '\\textbf{ipoteza}: \\aiprompt{Propune trei motive pentru care ponderile după inversul MSE ar putea bate media după 2020, fiecare cu un test.}'),
      T('\\textbf{code and replication}: ask for a function, then reproduce a known number first (the relative RMSE of the median in this lecture)', '\\textbf{cod și replicare}: cereți o funcție, apoi reproduceți întîi o cifră cunoscută (RMSE relativ al medianei din acest curs)'),
      T('\\textbf{robustness and critique}: \\aiprompt{Act as a hostile referee: list every way this evaluation could be data-snooped.}', '\\textbf{robustețe și critică}: \\aiprompt{Joacă rolul unui recenzent ostil: enumeră toate felurile în care această evaluare ar putea fi afectată de data snooping.}')]),
    T('Report: what was asked, what was kept, what was rejected (AI\\_USE.md, AI\\_ERRORS.md)', 'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\\_USE.md, AI\\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('No look-ahead: weights at survey $s$ use only outcomes known at $s$ (here, forecasts from at least five surveys earlier, whose target quarter has ended)', 'Fără informație din viitor: ponderile la ancheta $s$ folosesc doar realizări cunoscute la $s$ (aici, prognoze din anchete cu cel puțin cinci trimestre mai vechi, al căror trimestru-țintă s-a încheiat)'),
    T('The HAC lag matches the overlap of the targets ($h - 1$); the HLN correction is applied', 'Numărul de laguri HAC corespunde suprapunerii țintelor ($h - 1$); corecția HLN este aplicată'),
    T('$\\lambda$, sub-periods and the minimum record are fixed before the results; all variants are reported', '$\\lambda$, subperioadele și istoricul minim sînt fixate înaintea rezultatelor; toate variantele sînt raportate'),
    T('The interpretation separates ``not significant\'\' from ``equal\'\'', 'Interpretarea separă „nesemnificativ” de „egal”')), 'small')

chart(T('Mini-case: shrinkage across sub-periods', 'Mini-studiu de caz: shrinkage pe subperioade'), 'ats_ch1_ai_case', 'ATS_ch1_spf_combination', [
    T('RMSE of $\\lambda\\cdot$(inverse-MSE weights) + $(1 - \\lambda)\\cdot$(equal weights among eligible forecasters), relative to the mean of all forecasters; US SPF, CPI four quarters ahead', 'RMSE al combinației $\\lambda\\cdot$(ponderi după inversul MSE) + $(1 - \\lambda)\\cdot$(ponderi egale între prognozatorii eligibili), relativ la media tuturor prognozatorilor; SPF din SUA, IPC la patru trimestre'),
    T('$\\lambda = 1$: @{ai.1990_2007.1.00} (1990--2007, $P = @{ai.1990_2007.n}$), @{ai.2008_2019.1.00} (2008--2019), @{ai.2020_2025.1.00} (2020--2025); full sample HLN @{ai.h1}, $p$ @{ai.p1}', '$\\lambda = 1$: @{ai.1990_2007.1.00} (1990--2007, $P = @{ai.1990_2007.n}$), @{ai.2008_2019.1.00} (2008--2019), @{ai.2020_2025.1.00} (2020--2025); eșantionul complet HLN @{ai.h1}, $p$ @{ai.p1}'),
    T('Every sub-period: the more weight on past performance, the worse; the puzzle survives the 2020--2023 inflation surge', 'În fiecare subperioadă: cu cît ponderea performanței trecute este mai mare, cu atît rezultatul este mai slab; paradoxul rezistă valului inflaționist din 2020--2023')],
    h='0.46\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T('\\textbf{Combining Romanian inflation forecasts}: models (AR, Phillips curve with the output gap, BNR target), surveys and market-based expectations', '\\textbf{Combinarea prognozelor inflației din România}: modele (AR, curba Phillips cu deviația PIB, ținta BNR), anchete și așteptări din piață'),
     [T('pre-register horizons 1--12 months, the pinball loss at 5\\%, 50\\%, 95\\% and the CRPS, the Holm correction across horizons', 'preînregistrați orizonturile de 1--12 luni, pierderea pinball la 5\\%, 50\\%, 95\\% și CRPS, corecția Holm pe orizonturi'),
      T('replicate first: the Romanian inflation table of this lecture (Seminar 1, C1 does it by horizon)', 'replicați întîi: tabelul pentru inflația din România din acest curs (Seminarul 1, C1 îl face pe orizonturi)'),
      T('extension: density combination by optimal pools; GW test of whether the 2022 shock changed the winner', 'extensie: combinarea densităților prin optimal pools; testul GW pentru a vedea dacă șocul din 2022 a schimbat cîștigătorul')]),
    T('Deliverables follow the course rules: repository, report, AI\\_USE.md, AI\\_ERRORS.md, oral defence', 'Livrabilele urmează regulile cursului: repository, raport, AI\\_USE.md, AI\\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Choose the loss or score first: it defines what a ``good\'\' forecast is (mean, median, quantile, distribution)', 'Alegeți întîi pierderea sau scorul: ele definesc ce este o prognoză „bună” (medie, mediană, cuantilă, distribuție)'),
    T('Density forecasts: check calibration with PIT, rank with proper scores; ES needs VaR to be scored', 'Prognozele de densitate: verificați calibrarea cu PIT, ierarhizați cu scoruri proprii; ES are nevoie de VaR pentru a fi evaluat'),
    T('Tests: DM--HLN with HAC, GW for methods, Clark--West for nested models, SPA and MCS for many', 'Teste: DM--HLN cu HAC, GW pentru metode, Clark--West pentru modele imbricate, SPA și MCS pentru multe modele'),
    T('Combine similar forecasts with equal weights; estimated weights pay off only with very different forecasts and long records', 'Combinați prognozele asemănătoare cu ponderi egale; ponderile estimate merită doar pentru prognoze foarte diferite și istoric lung'),
    T('Evaluate in real time and pre-register the design', 'Evaluați în timp real și preînregistrați planul')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('Which functional does the pinball loss with $\\tau = 0.05$ elicit?', 'Ce funcțională elicitează pierderea pinball cu $\\tau = 0{,}05$?'),
        T('What does a U-shaped PIT histogram say about the intervals?', 'Ce spune o histogramă PIT în formă de U despre intervale?'),
        T('Why is DM not valid for nested models with estimated parameters?', 'De ce nu este valid testul DM pentru modele imbricate cu parametri estimați?'),
        T('When do estimated combination weights beat equal weights?', 'Cînd bat ponderile de combinare estimate ponderile egale?'),
        T('Why can ES not be ranked on its own?', 'De ce nu poate fi ierarhizat ES singur?'))),
    block(T('Next: Chapter 2', 'Urmează: Capitolul 2'), items(
        T('Structural breaks and nonlinear models: tests for breaks, threshold models', 'Rupturi structurale și modele neliniare: teste pentru rupturi, modele cu prag'),
        T('Forecast evaluation under instability: rolling windows, forecast breakdowns, the fluctuation test \\refGRaz', 'Evaluarea prognozelor sub instabilitate: ferestre mobile, eșecul prognozelor, testul de fluctuație \\refGRaz'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: consistency of the pinball loss', 'Anexă: consistența pierderii pinball'), items(
    T('$\\E\\rho_\\tau(Y - x) = \\tau\\int_x^\\infty(y - x)dF(y) + (1 - \\tau)\\int_{-\\infty}^x(x - y)dF(y)$', '$\\E\\rho_\\tau(Y - x) = \\tau\\int_x^\\infty(y - x)dF(y) + (1 - \\tau)\\int_{-\\infty}^x(x - y)dF(y)$'),
    T('Derivative (Leibniz): $-\\tau(1 - F(x)) + (1 - \\tau)F(x) = F(x) - \\tau$; zero at $x = F^{-1}(\\tau)$; second derivative $f(x) \\ge 0$', 'Derivata (Leibniz): $-\\tau(1 - F(x)) + (1 - \\tau)F(x) = F(x) - \\tau$; nulă în $x = F^{-1}(\\tau)$; derivata a doua $f(x) \\ge 0$'),
    T('For $\\tau = 1/2$: $\\rho_{1/2}(e) = |e|/2$, so the median; for $x$ off the quantile the excess loss is $\\int_q^x(F(z) - \\tau)dz > 0$', 'Pentru $\\tau = 1/2$: $\\rho_{1/2}(e) = |e|/2$, deci mediana; pentru $x$ diferit de cuantilă, pierderea suplimentară este $\\int_q^x(F(z) - \\tau)dz > 0$'),
    T('Generalised piecewise linear losses $(\\mathbf 1\\{y \\le x\\} - \\tau)(g(x) - g(y))$, $g$ increasing, are the whole class of consistent losses for the quantile \\refGnaa', 'Pierderile liniare pe porțiuni generalizate $(\\mathbf 1\\{y \\le x\\} - \\tau)(g(x) - g(y))$, $g$ crescătoare, formează întreaga clasă de pierderi consistente pentru cuantilă \\refGnaa')), 'small')

D.frame(T('Appendix: the kernel form of the CRPS', 'Anexă: forma cu nucleu a CRPS'), items(
    T('Write $(F(z) - \\mathbf 1\\{y \\le z\\})^2 = F(z)^2 - 2F(z)\\mathbf 1\\{y \\le z\\} + \\mathbf 1\\{y \\le z\\}$', 'Scriem $(F(z) - \\mathbf 1\\{y \\le z\\})^2 = F(z)^2 - 2F(z)\\mathbf 1\\{y \\le z\\} + \\mathbf 1\\{y \\le z\\}$'),
    T('With $X, X\' \\sim F$ i.i.d.: $F(z)^2 = P(X \\le z, X\' \\le z)$ and $\\E|X - y| = \\int[F(z)(1 - \\mathbf 1\\{y \\le z\\}) + (1 - F(z))\\mathbf 1\\{y \\le z\\}]dz$', 'Cu $X, X\' \\sim F$ i.i.d.: $F(z)^2 = P(X \\le z, X\' \\le z)$ și $\\E|X - y| = \\int[F(z)(1 - \\mathbf 1\\{y \\le z\\}) + (1 - F(z))\\mathbf 1\\{y \\le z\\}]dz$'),
    T('$\\frac12\\E|X - X\'| = \\int F(z)(1 - F(z))dz$; subtracting gives $\\int(F(z) - \\mathbf 1\\{y \\le z\\})^2dz$', '$\\frac12\\E|X - X\'| = \\int F(z)(1 - F(z))dz$; prin scădere obținem $\\int(F(z) - \\mathbf 1\\{y \\le z\\})^2dz$'),
    T('Propriety: $\\E_G\\mathrm{CRPS}(F, Y) - \\E_G\\mathrm{CRPS}(G, Y) = \\int(F(z) - G(z))^2dz \\ge 0$, zero only if $F = G$', 'Proprietatea: $\\E_G\\mathrm{CRPS}(F, Y) - \\E_G\\mathrm{CRPS}(G, Y) = \\int(F(z) - G(z))^2dz \\ge 0$, zero doar dacă $F = G$')), 'small')

D.frame(T('Appendix: the Clark--West adjustment', 'Anexă: corecția Clark--West'), items(
    T('Under $H_0$ the larger model\'s extra coefficients $\\beta_2 = 0$; its forecast is $\\hat y_2 = \\hat y_1 + \\hat\\beta_2\'x_{2}$ approximately, with $\\hat\\beta_2$ pure estimation noise', 'Sub $H_0$ coeficienții suplimentari ai modelului mare sînt $\\beta_2 = 0$; prognoza lui este aproximativ $\\hat y_2 = \\hat y_1 + \\hat\\beta_2\'x_{2}$, cu $\\hat\\beta_2$ zgomot de estimare pur'),
    T('$e_2 = e_1 - (\\hat y_2 - \\hat y_1)$, so $e_1^2 - e_2^2 = 2e_1(\\hat y_2 - \\hat y_1) - (\\hat y_2 - \\hat y_1)^2$', '$e_2 = e_1 - (\\hat y_2 - \\hat y_1)$, deci $e_1^2 - e_2^2 = 2e_1(\\hat y_2 - \\hat y_1) - (\\hat y_2 - \\hat y_1)^2$'),
    T('$\\E[e_1(\\hat y_2 - \\hat y_1)] = 0$ under $H_0$ ($e_1$ is a martingale difference), hence $\\E(e_1^2 - e_2^2) = -\\E(\\hat y_2 - \\hat y_1)^2 < 0$', '$\\E[e_1(\\hat y_2 - \\hat y_1)] = 0$ sub $H_0$ ($e_1$ este o diferență de martingală), deci $\\E(e_1^2 - e_2^2) = -\\E(\\hat y_2 - \\hat y_1)^2 < 0$'),
    T('Adding $(\\hat y_1 - \\hat y_2)^2$ recentres the differential at zero: $f_t = 2e_{1t}(\\hat y_{2t} - \\hat y_{1t})$, the encompassing statistic of \\refHLNih\\ in disguise', 'Adunarea lui $(\\hat y_1 - \\hat y_2)^2$ recentrează diferențialul în zero: $f_t = 2e_{1t}(\\hat y_{2t} - \\hat y_{1t})$, statistica de încadrare din \\refHLNih\\ sub altă formă')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
