r"""
build_chapter0.py -- Capitolul 0 (Recapitulare și inferență pentru date dependente), EN + RO dintr-o singură sursă
==================================================================================================================
Generator bilingv (Deck din latex/ats_build.py, text ⟦EN||RO⟧). Două părți:
  * organizarea cursului: cursul pe scurt, locul cursului, evaluarea, manualele, harta celor 17 capitole, seminariile,
    proiectul, politica AI, materialele;
  * conținutul: harta recapitulării din TSA (doar trimiteri), asimptotică pentru date dependente (ergodicitate,
    mixing, LGN și TLC), varianța de termen lung, estimatori HAC (Newey--West, Andrews, nuclee, fixed-b, LLSW),
    consecințele autocorelației pentru testele t, Monte Carlo pentru mărimea testelor, bootstrap pe blocuri
    (mobile, circulare, staționar) și wild bootstrap, observații suprapuse (marja la termen și creșterea), data
    snooping (Reality Check), cercetare reproductibilă, AI în descoperirea științifică.
Cifrele @{cheie} vin din Quantlets/Ch_00/ch0_numbers.json (generate_all_charts.py). Nicio cifră nu este scrisă de mînă.
Fotografii: photos/ch0_*.jpg (licențe verificate prin API-ul Wikimedia Commons; vezi photos/CREDITS.md).
Ieșire:
  EN/Courses/chapter0_refresher_inference.tex
  RO/Cursuri/capitol0_recapitulare_inferenta.tex
Rulare:  python3 Quantlets/Ch_00/generate_all_charts.py
         python3 latex/build_chapter0.py   apoi   python3 latex/ats_build.py compile 0
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, items, cols, table, photo, ql   # noqa: E402
from ats_chapters import TITLES, SELF_STUDY                         # noqa: E402
from ch0_common import BIB, REFS, T, day, finalize, load, month, quarter   # noqa: E402

SITE = 'https://danpele.github.io/Advanced-Time-Series/'
TSA_SITE = 'https://danpele.github.io/Time-Series-Analysis/'
MFM_SITE = 'https://danpele.github.io/MFM/'
C = 'https://commons.wikimedia.org/wiki/File:'
FOTO = '⟦Photo||Foto⟧'
PD = '⟦public domain||domeniu public⟧'
PH = {
    'ase': ('ch0_ase_2014.jpg', C + 'Bucharest_-_Academie_de_Studii_Economice_01.jpg', f'{FOTO}: Joe Mabel (2014); CC BY 3.0; Wikimedia Commons'),
    'bnr': ('ch0_bnr_palace_2015.jpg', C + 'Bucharest_-_BNR_Palace_(19644434340).jpg', f'{FOTO}: Ștefan Jurcă (2015); CC BY 2.0; Wikimedia Commons'),
    'fed': ('ch0_eccles_2011.jpg', C + 'Eccles_Building_(26088200676).jpg', f'{FOTO}: Federal Reserve (2011); {PD}; Wikimedia Commons'),
    'birkhoff': ('ch0_birkhoff_1910.jpg', C + 'George_David_Birkhoff_1.jpg', f'{FOTO}: ⟦unknown author||autor necunoscut⟧ (c.\\ 1910); {PD}; Wikimedia Commons'),
    'efron': ('ch0_efron_2007.jpg', C + 'Bradley_Efron_National_Medal_of_Science_2007_(cropped).jpg', f'{FOTO}: Ryan K. Morris, NSTMF (2007); {PD}; Wikimedia Commons'),
    'kunsch': ('ch0_kunsch_2007.jpg', C + 'Hans-Rudolf_Künsch.jpg', f'{FOTO}: Renate Schmid (2007); CC BY-SA 2.0 de; Wikimedia Commons'),
}


def ph(key, cap, h='0.46\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def ch_rows(rng):
    """Rows of the course-map table: number, title (EN || RO), self-study mark."""
    rows = []
    for k in rng:
        en, ro = TITLES[k]
        mark = ' ⟦(self-study)||(studiu individual)⟧' if k in SELF_STUDY else ''
        rows.append(f'{k} & ⟦{en}||{ro}⟧{mark}')
    return rows


# =============================================================================
# CIFRE (Quantlets/Ch_00/ch0_numbers.json)
# =============================================================================
N = load()
V = Values()


def raw2(key, both):
    """A bilingual value ⟦EN||RO⟧ stored as two keys, key.en and key.ro (no nesting inside ⟦..||..⟧)."""
    en, ro = both[1:-1].split('||')
    V.raw(key + '.en', en)
    V.raw(key + '.ro', ro)


P = V.put
DA = N['dash']
raw2('d.if', month(DA['infl_first']))
raw2('d.il', month(DA['infl_last']))
V.int('d.in', DA['infl_n'])
P('d.imax', DA['infl_max'], 1)
raw2('d.imaxd', month(DA['infl_max_d']))
P('d.imin', DA['infl_min'], 1)
raw2('d.imind', month(DA['infl_min_d']))
P('d.ilast', DA['infl_last_v'], 1)
V.raw('d.gf', quarter(DA['gdp_first']))
V.raw('d.gl', quarter(DA['gdp_last']))
V.int('d.gn', DA['gdp_n'])
P('d.gmin', DA['gdp_min'], 1)
V.raw('d.gmind', quarter(DA['gdp_min_d']))
raw2('d.ef', day(DA['eur_first']))
V.int('d.en', DA['eur_n'])
V.int('d.sn', DA['sp_n'])
V.int('d.bn', DA['bet_n'])
raw2('d.last', day(DA['last_daily']))

AC = N['acf']
for tag, k in (('sp', 'S&P 500 returns'), ('sq', 'S&P 500 squared returns'), ('eur', 'EUR/RON returns'),
               ('bet', 'BET returns'), ('gdp', 'RO GDP growth (q/q)'), ('inf', 'RO HICP inflation (annual rate)')):
    P(f'a.{tag}.r1', AC[k]['r1'], 2)
    P(f'a.{tag}.r12', AC[k]['r12'], 2)
    V.raw(f'a.{tag}.out', str(AC[k]['n_out']))
    P(f'a.{tag}.ra', AC[k]['ratio_andrews'], 1)
    P(f'a.{tag}.band', AC[k]['band'], 3)

LR = N['lrv']
P('l.f05', LR['f05'], 0)
P('l.f09', LR['f09'], 0)
P('l.fm05', LR['fm05'], 2)
P('l.s03', 100 * LR['size03'], 0)
P('l.s05', 100 * LR['size05'], 0)
P('l.s09', 100 * LR['size09'], 0)
P('l.c05', 100 * (1 - LR['size05']), 0)
P('l.sim05', LR['sim05'], 2)
P('l.sim09', LR['sim09'], 1)
V.int('l.reps', LR['reps'])
V.raw('l.T', str(LR['T']))
P('k.qsmin', N['kern']['qs_min'], 3)
NG = N['neg']
for k in ('g0', 'g1', 'g2', 'trunc_S1', 'bart_S2'):
    P(f'n.{k}', NG[k], 1)

BW = N['bw']
for tag, k in (('sp', 'S&P 500 returns'), ('sq', 'S&P 500 squared returns'), ('eur', 'EUR/RON returns'),
               ('inf', 'RO HICP inflation'), ('gdp', 'RO GDP growth')):
    P(f'bw.{tag}.ra', BW[k]['r_and'], 2)
    P(f'bw.{tag}.Sa', BW[k]['S_and'], 0)
    P(f'bw.{tag}.rn', BW[k]['r_nw'], 2)
    V.raw(f'bw.{tag}.Sn', str(BW[k]['S_nw']))
    P(f'bw.{tag}.rmax', BW[k]['r_max'], 2)
FB = N['fixedb']
for b in ('0.1', '0.2', '0.5', '1.0'):
    P(f'fb.b{b}', FB['bart'][b], 2)
    P(f'fb.q{b}', FB['qs'][b], 2)

MC = N['mc']['res']
for TT in ('100', '400'):
    for ph_ in ('0.0', '0.5', '0.9'):
        for k, v in MC[TT][ph_].items():
            P(f'mc.{TT}.{ph_[2]}.{k}', 100 * v, 1)
V.int('mc.reps', N['mc']['reps'])
V.int('mc.breps', N['mc']['breps'])

BO = N['boot']
for k in ('mean', 'se_naive', 'se_iid', 'se_mbb', 'se_cbb', 'se_sb', 'se_and', 'se_qs'):
    P(f'bo.{k}', BO[k], 3)
P('bo.bsb', BO['b_sb'], 0)
P('bo.bcb', BO['b_cb'], 0)
P('bo.rsb', BO['se_sb'] / BO['se_naive'], 1)
P('bo.rand', BO['se_and'] / BO['se_naive'], 1)
BL = N['blk']
P('bl.inf.b', BL['RO HICP inflation']['b_cb'], 0)
P('bl.inf.r', BL['RO HICP inflation']['r_pw'], 1)
P('bl.gdp.b', BL['RO GDP growth']['b_sb'], 1)

TB = N['tab']
for k, r in TB.items():
    P(f't.{k}.mean', r['mean'], 3)
    P(f't.{k}.rho', r['rho1'], 2)
    for m in ('naive', 'andrews', 'llsw', 'ewc', 'sb'):
        P(f't.{k}.se_{m}', r[f'se_{m}'], 4 if k in ('sp', 'bet', 'eur') else 3)
    for m in ('naive', 'andrews', 'llsw', 'ewc'):
        P(f't.{k}.t_{m}', r[f't_{m}'], 2)
    P(f't.{k}.ra', r['ratio_and'], 2)
    P(f't.{k}.rs', r['ratio_sb'], 2)
    V.int(f't.{k}.T', r['T'])
P('t.sp.cv', TB['sp']['cv_llsw'], 2)
P('t.sp.ann', 252 * TB['sp']['mean'], 1)

TS = N['ts']
for k in ('b0', 'b1', 'se_classic', 'se_white', 'se_nw', 'se_hh', 'se_and', 'se_ll', 'cv_ll', 't_classic', 't_nw',
          't_and', 't_ll', 'rho1', 'rho3', 'rho4', 'r2'):
    P(f'ts.{k}', TS[k], 2)
P('ts.Sa', TS['S_and'], 0)
P('ts.Sl', TS['S_ll'], 0)
V.raw('ts.T', str(TS['T']))
V.raw('ts.first', quarter(TS['first']))
V.raw('ts.last', quarter(TS['last']))
for s in ('early', 'late'):
    P(f'ts.{s}.b', TS['sub'][s]['b'], 2)
    P(f'ts.{s}.se', TS['sub'][s]['se'], 2)
    P(f'ts.{s}.t', TS['sub'][s]['t'], 1)

SN = N['snoop']
P('sn.i20', 100 * SN['indep']['20'], 0)
P('sn.i100', 100 * SN['indep']['100'], 1)
P('sn.c20', 100 * SN['0.5']['20'], 0)
P('sn.c100', 100 * SN['0.5']['100'], 0)
P('sn.h100', 100 * SN['0.9']['100'], 0)
RC = N['rc']
for tag, k in (('e', '2000-2012'), ('l', '2013-2026')):
    r = RC[k]
    V.raw(f'rc.{tag}.n', str(r['best_n']))
    P(f'rc.{tag}.m', r['best_mean'], 3)
    P(f'rc.{tag}.t', r['t_best'], 2)
    P(f'rc.{tag}.p', r['p_naive'], 3)
    P(f'rc.{tag}.prc', r['p_rc'], 2)
    V.raw(f'rc.{tag}.ns', str(r['n_sig']))
    V.int(f'rc.{tag}.N', r['n'])
    V.raw(f'rc.{tag}.K', str(r['K']))

AI = N['ai']
for k in ('mean', 'phi', 'cv_llsw', 'cv_ewc', 't_naive', 't_nw', 't_andrews', 't_llsw', 't_ewc', 'lo_nw', 'hi_nw',
          'lo_llsw', 'hi_llsw', 'lo_naive', 'hi_naive', 'lo_ewc', 'hi_ewc', 'lo_andrews', 'hi_andrews'):
    P(f'ai.{k}', AI[k], 2)
P('ai.Sa', AI['S_and'], 0)
V.raw('ai.T', str(AI['T']))
V.raw('ai.nu', str(AI['nu']))
raw2('ai.last', month(AI['last']))
for k, v in AI['mc'].items():
    P(f'ai.mc.{k}', 100 * v, 0)
finalize(V)

# =============================================================================
D = Deck(0, 'lecture', refs=REFS)


def frame(title, body, size='small'):
    D.frame(title, body, size)


def chart(title, fig, folder, bullets, h='0.60\\textheight', size='footnotesize'):
    D.chart(title, fig, folder, bullets, height=h, size=size)


def interp(en, ro, bullets, size='small'):
    D.frame(f'⟦Interpreting {en}||Interpretarea {ro}⟧', items(*bullets), size)


# ===============================================================================================================
D.section('Course organisation', 'Organizarea cursului')
# ===============================================================================================================
frame('⟦The course at a glance||Cursul pe scurt⟧', cols(
    items(('⟦\\textbf{Programme}||\\textbf{Program}⟧',
           ["⟦Master's programme Applied Statistics and Data Science (ASDS), year 1, semester 2||Programul de master Statistică aplicată și data science (ASDS), anul I, semestrul 2⟧",
            '⟦Faculty of Cybernetics, Statistics and Economic Informatics, ASE Bucharest||Facultatea de Cibernetică, Statistică și Informatică Economică, ASE București⟧',
            '⟦7 ECTS credits; 2 hours of lecture and 2 hours of seminar a week; academic year 2026/2027||7 credite ECTS; 2 ore de curs și 2 ore de seminar pe săptămînă; anul universitar 2026/2027⟧']),
          ('⟦\\textbf{Lecturer}||\\textbf{Titular}⟧',
           ['Prof.\\ Daniel Traian Pele, \\href{mailto:danpele@ase.ro}{danpele@ase.ro}']),
          ('⟦\\textbf{Course website}||\\textbf{Site-ul cursului}⟧',
           [f'\\href{{{SITE}}}{{danpele.github.io/Advanced-Time-Series}}',
            '⟦slides, seminars, notebooks, Quantlets and the graded quizzes||slide-uri, seminarii, notebook-uri, Quantlets și quiz-urile notate⟧'])),
    ph('ase', '⟦The Bucharest University of Economic Studies (ASE)||Academia de Studii Economice din București (ASE)⟧'),
    '0.56', '0.40'), 'footnotesize')

frame('⟦Position in the curriculum||Locul cursului în program⟧', items(
    ('⟦\\textbf{Before}: \\href{%s}{Time Series Analysis} (TSA, bachelor), Chapters 0--10 of TSA||\\textbf{Înainte}: \\href{%s}{Serii de timp} (TSA, licență), capitolele 0--10 din TSA⟧' % (TSA_SITE, TSA_SITE),
     ['⟦ARMA, ARIMA and unit roots, SARIMA, GARCH, VAR and Granger causality, cointegration and VECM, long memory, machine learning, state space models||ARMA, ARIMA și rădăcini unitare, SARIMA, GARCH, VAR și cauzalitate Granger, cointegrare și VECM, memorie lungă, machine learning, modele în spațiul stărilor⟧',
      '⟦assumed known: this course starts from them and does not repeat them||sînt considerate cunoscute: cursul pornește de la ele și nu le reia⟧']),
    ('⟦\\textbf{This course}: ATS, master, year 1, semester 2||\\textbf{Acest curs}: ATS, master, anul I, semestrul 2⟧',
     ['⟦methodology for forecasting, identification and inference with dependent data||metodologia prognozei, a identificării și a inferenței pentru date dependente⟧',
      '⟦macroeconomic (Romanian and EU), energy, climate and financial series||serii macroeconomice (România și Uniunea Europeană), energetice, climatice și financiare⟧']),
    ('⟦\\textbf{After}: \\href{%s}{Modelling Financial Markets} (MFM, master, year 2, semester 1)||\\textbf{După}: \\href{%s}{Modelarea piețelor financiare} (MFM, master, anul II, semestrul 1)⟧' % (MFM_SITE, MFM_SITE),
     ['⟦the same methods applied to market risk, portfolios, microstructure and digital assets||aceleași metode aplicate riscului de piață, portofoliilor, microstructurii și activelor digitale⟧'])),
    'footnotesize')

frame('⟦Evaluation||Evaluare⟧', items(
    ('⟦\\textbf{Team project and individual oral defence: 70\\%}||\\textbf{Proiect de echipă și susținere orală individuală: 70\\%}⟧',
     ['⟦proposal and pre-registration (team): 5\\%||propunerea și preînregistrarea (echipă): 5\\%⟧',
      '⟦replication and extension: repository, report, AI\\_USE.md and AI\\_ERRORS.md (team): 15\\%||replicarea și extensia: repository, raport, AI\\_USE.md și AI\\_ERRORS.md (echipă): 15\\%⟧',
      '⟦individual oral defence: 50\\%||susținerea orală individuală: 50\\%⟧']),
    ('⟦\\textbf{Chapter quizzes: 20\\%}||\\textbf{Quiz-uri pe capitole: 20\\%}⟧',
     ['⟦online, on the course website, with the ASE Google account||online, pe site-ul cursului, cu contul Google ASE⟧']),
    ('⟦\\textbf{Attendance: 10\\%}||\\textbf{Prezență: 10\\%}⟧',
     ['⟦recorded with the attendance form or the QR code||înregistrată prin formularul de prezență sau prin codul QR⟧']),
    '⟦There is no written exam||Cursul nu are examen scris⟧'))

frame('⟦Textbooks||Manuale⟧', items(
    ('⟦\\textbf{Main references}||\\textbf{Referințe principale}⟧',
     ['\\refHamilton: ⟦the theory of linear time series, unit roots and VAR||teoria seriilor de timp liniare, rădăcini unitare și modele VAR⟧',
      '\\refKL: ⟦structural VAR analysis and identification||analiza VAR structurală și identificarea⟧',
      '\\refDK: ⟦state space methods||metode în spațiul stărilor⟧',
      '\\refPetropoulos: ⟦forecasting theory and practice, open access||teoria și practica prognozei, cu acces liber⟧']),
    ('⟦\\textbf{Bridge from the bachelor course}||\\textbf{Legătura cu cursul de licență}⟧',
     ['\\refHP; \\refFPP']),
    ('⟦\\textbf{Specialised}||\\textbf{Lucrări de specialitate}⟧',
     ['\\refLutkepohl; \\refSS; \\refBaltagi; \\refAB; ⟦for this chapter also||pentru acest capitol și⟧ \\refLahiri',
      '⟦each chapter adds its landmark papers as case studies||fiecare capitol adaugă lucrările de referință folosite ca studii de caz⟧'])))

D.frame('⟦Course map (1/2)||Harta cursului (1/2)⟧',
        table('rl', '⟦\\textbf{Ch.}||\\textbf{Cap.}⟧ & ⟦\\textbf{Topic}||\\textbf{Tema}⟧', ch_rows(range(0, 9)), size='footnotesize'),
        size=None)
D.frame('⟦Course map (2/2)||Harta cursului (2/2)⟧',
        table('rl', '⟦\\textbf{Ch.}||\\textbf{Cap.}⟧ & ⟦\\textbf{Topic}||\\textbf{Tema}⟧', ch_rows(range(9, 17)), size='footnotesize'),
        size=None)

frame('⟦Lectures and seminars||Cursuri și seminarii⟧', items(
    ('⟦\\textbf{Lectures}||\\textbf{Cursuri}⟧',
     ['⟦one chapter a week, built around landmark papers replicated on our data||cîte un capitol pe săptămînă, construit în jurul unor lucrări de referință replicate pe datele noastre⟧',
      '⟦each lecture ends with a section on AI for scientific discovery||fiecare curs se încheie cu o secțiune despre AI în descoperirea științifică⟧']),
    ('⟦\\textbf{Seminars}: each seminar comes \\emph{before} its lecture and opens with the notions it needs||\\textbf{Seminarii}: fiecare seminar are loc \\emph{înaintea} cursului și începe cu noțiunile necesare⟧',
     ['⟦Part A: derivations; Part B: estimation and inference on data, each exercise closing with an interpretation question; Part C: open problems that can seed the project||Partea A: derivări; Partea B: estimare și inferență pe date, fiecare exercițiu încheindu-se cu o întrebare de interpretare; Partea C: probleme deschise, care pot deveni idei de proiect⟧',
      '⟦[Solved] exercises with full solutions and [Proposed] exercises discussed in class||exerciții [Rezolvat], cu soluții complete, și exerciții [Propus], discutate la seminar⟧',
      '⟦every seminar includes the critique of an answer given by an AI tool||fiecare seminar include analiza critică a unui răspuns dat de un instrument AI⟧']),
    '⟦Seminars are practice and are not graded; the solutions of the [Proposed] exercises are discussed in class||Seminarul are rol de exercițiu și nu se notează; rezolvările cerințelor [Propus] se discută la seminar⟧'),
    'footnotesize')

frame('⟦The team project||Proiectul de echipă⟧', items(
    ('⟦\\textbf{Teams of up to 3 students}||\\textbf{Echipe de cel mult 3 studenți}⟧',
     ['⟦replicate a landmark paper of the course, or another paper approved by the lecturer||replicarea unei lucrări de referință a cursului sau a unei alte lucrări aprobate de titular⟧',
      '⟦extend it with the methods of the course, preferably on Romanian or EU data||extinderea ei cu metodele cursului, de preferință pe date din România sau din Uniunea Europeană⟧']),
    ('⟦\\textbf{Stages}||\\textbf{Etape}⟧',
     ['⟦Stage 1: research question, data and an evaluation design fixed before any estimation (pre-registration)||Etapa 1: întrebarea de cercetare, datele și un plan de evaluare fixat înaintea oricărei estimări (preînregistrare)⟧',
      '⟦Stage 2: replication, extension and a GitHub repository that reproduces every number (Colab)||Etapa 2: replicarea, extensia și un repository GitHub care reproduce fiecare rezultat (Colab)⟧',
      '⟦Stage 3: presentation and individual oral defence||Etapa 3: prezentarea și susținerea orală individuală⟧']),
    '⟦Inference that is valid for dependent data (this chapter) is part of every project||Inferența validă pentru date dependente (acest capitol) face parte din fiecare proiect⟧',
    '⟦The project can be written and defended in Romanian or in English||Proiectul poate fi redactat și susținut în limba română sau în limba engleză⟧'),
    'footnotesize')

frame('⟦AI policy||Politica privind AI⟧', items(
    ('⟦\\textbf{Allowed and declared}||\\textbf{Permis și declarat}⟧',
     ['⟦AI\\_USE.md: tool, purpose, prompts, what was kept and what was changed||AI\\_USE.md: instrumentul, scopul, prompturile, ce s-a păstrat și ce s-a modificat⟧',
      '⟦AI\\_ERRORS.md: at least three errors of AI tools caught by the team, and how each was detected||AI\\_ERRORS.md: cel puțin trei erori ale instrumentelor AI depistate de echipă și modul în care a fost depistată fiecare⟧',
      '⟦undeclared use counts as plagiarism||folosirea nedeclarată este considerată plagiat⟧']),
    ('⟦\\textbf{Checked}||\\textbf{Verificat}⟧',
     ['⟦every reference against its DOI, every number against the data and the code||fiecare referință după DOI, fiecare rezultat numeric pe date și pe cod⟧']),
    ('⟦\\textbf{Oral defence without AI}||\\textbf{Susținerea orală fără AI}⟧',
     ['⟦each member explains the methods, the code and the results||fiecare membru explică metodele, codul și rezultatele⟧'])))

frame('⟦Materials and tools||Materiale și instrumente⟧', items(
    ('⟦\\textbf{For every chapter}||\\textbf{Pentru fiecare capitol}⟧',
     ['⟦lecture and seminar slides in English and Romanian||slide-urile cursului și ale seminarului, în engleză și în română⟧',
      '⟦lecture and seminar notebooks in English, runnable in Google Colab||notebook-uri de curs și de seminar în engleză, rulabile în Google Colab⟧',
      '⟦a Quantlet with the code of every chart, and a quiz||un Quantlet cu codul fiecărui grafic și un quiz⟧']),
    ('⟦\\textbf{Data}||\\textbf{Date}⟧',
     ['⟦daily market data from EODHD (EOD Historical Data), saved in the course repository||date zilnice de piață de la EODHD (EOD Historical Data), salvate în repository-ul cursului⟧',
      '⟦public macroeconomic data: INS, BNR, Eurostat, the ECB and FRED||date macroeconomice publice: INS, BNR, Eurostat, BCE și FRED⟧']),
    ('⟦\\textbf{Software}||\\textbf{Programe}⟧',
     ['⟦Python: statsmodels, arch, linearmodels, scikit-learn, PyTorch||Python: statsmodels, arch, linearmodels, scikit-learn, PyTorch⟧'])))

# ===============================================================================================================
D.section('Chapter 0: the plan', 'Capitolul 0: planul')
# ===============================================================================================================
frame('⟦Learning outcomes||Rezultatele învățării⟧', items(
    '⟦State the limit theorems behind every standard error used with time series: ergodic LLN, martingale-difference and mixing CLT||Să enunțați teoremele limită din spatele oricărei erori standard folosite pentru serii de timp: LGN ergodică, TLC pentru diferențe de martingală și pentru procese mixing⟧',
    '⟦Derive the long-run variance and its consequences for $t$-tests and confidence intervals||Să derivați varianța de termen lung și consecințele ei pentru testele $t$ și intervalele de încredere⟧',
    '⟦Choose and defend a HAC estimator: kernel, bandwidth, critical values (standard or fixed-$b$)||Să alegeți și să argumentați un estimator HAC: nucleul, lățimea de bandă, valorile critice (standard sau fixed-$b$)⟧',
    '⟦Use block bootstraps (moving, circular, stationary) and know when the wild bootstrap is not enough||Să folosiți bootstrap-ul pe blocuri (mobile, circulare, staționar) și să știți cînd wild bootstrap-ul nu este suficient⟧',
    '⟦Measure size distortions by Monte Carlo and control data snooping||Să măsurați distorsiunile de mărime prin Monte Carlo și să controlați data snooping⟧',
    '⟦Build a replication package that reproduces every number of a project||Să construiți un pachet de replicare care reproduce fiecare rezultat al unui proiect⟧'))

frame('⟦Data used in this chapter||Datele folosite în acest capitol⟧', table(
    'p{3.3cm}p{5.4cm}p{2.6cm}p{2.0cm}',
    '\\textbf{⟦Series||Seria⟧} & \\textbf{⟦Definition||Definiție⟧} & \\textbf{⟦Period||Perioada⟧} & \\textbf{⟦Source||Sursa⟧}', [
        '⟦Romanian inflation||Inflația în România⟧ & ⟦HICP, annual rate of change, \\%, monthly||IAPC, rata anuală de variație, \\%, lunar⟧ & ⟦@{d.if.en} -- @{d.il.en}||@{d.if.ro} -- @{d.il.ro}⟧ & Eurostat',
        '⟦Romanian real GDP||PIB-ul real al României⟧ & ⟦chain-linked volumes, seasonally adjusted; growth q/q, \\%||volume înlănțuite, ajustate sezonier; creștere t/t, \\%⟧ & @{d.gf} -- @{d.gl} & Eurostat',
        'EUR/RON & ⟦BNR reference rate; daily log change, \\%||cursul de referință BNR; variația logaritmică zilnică, \\%⟧ & ⟦@{d.ef.en} -- @{d.last.en}||@{d.ef.ro} -- @{d.last.ro}⟧ & BNR',
        'S\\&P 500, BET & ⟦daily log returns and squared returns, \\%||randamente logaritmice zilnice și pătratele lor, \\%⟧ & ⟦2000 -- @{d.last.en}||2000 -- @{d.last.ro}⟧ & EODHD',
        '⟦US macro||Macro SUA⟧ & ⟦real GDP; 10-year and 3-month Treasury yields||PIB real; randamentele titlurilor de stat la 10 ani și la 3 luni⟧ & 1962 -- 2026 & FRED'], 'scriptsize') +
    items('⟦Daily series on their own trading calendars; Eurostat and FRED series read online at the build date||Seriile zilnice pe calendarele lor de tranzacționare; seriile Eurostat și FRED citite online la data generării⟧',
          '⟦HICP: harmonised index of consumer prices; the BNR target is defined on the national CPI, close to the HICP||IAPC: indicele armonizat al prețurilor de consum; ținta BNR este definită pe IPC național, apropiat de IAPC⟧'), 'footnotesize')

frame('⟦Where the data come from||Proveniența datelor⟧', cols(
    ph('bnr', '⟦The National Bank of Romania (BNR), Bucharest: reference rates and the inflation target||Banca Națională a României (BNR), București: cursurile de referință și ținta de inflație⟧', '0.40\\textheight'),
    ph('fed', '⟦The Eccles Building, Washington: the Federal Reserve Board; FRED is run by the St.\\ Louis Fed||Clădirea Eccles, Washington: Consiliul Rezervei Federale; FRED este administrat de Fed St.\\ Louis⟧', '0.40\\textheight'),
    '0.48', '0.48') + items(
    '⟦A central bank publishes the series we test: the inflation target of the BNR is 2.5\\% $\\pm$ 1 pp since 2013 (the AI mini-case at the end)||O bancă centrală publică seriile pe care le testăm: ținta de inflație a BNR este 2,5\\% $\\pm$ 1 pp din 2013 (mini-studiul de caz de la final)⟧'), 'footnotesize')

frame('⟦Notation (1/2)||Notații (1/2)⟧', items(
    ('⟦$\\{x_t\\}$, $t = 1, \\dots, T$: a weakly stationary series observed over $T$ periods||$\\{x_t\\}$, $t = 1, \\dots, T$: o serie slab staționară observată pe $T$ perioade⟧',
     ['⟦$\\mu = E x_t$: its mean; $\\gamma_j = \\Cov(x_t, x_{t-j})$: the autocovariance at lag $j$, the same for every $t$||$\\mu = E x_t$: media seriei; $\\gamma_j = \\Cov(x_t, x_{t-j})$: autocovarianța la lagul $j$, aceeași pentru orice $t$⟧',
      '⟦$\\gamma_0 = \\Var(x_t)$; $\\rho_j = \\gamma_j/\\gamma_0 \\in [-1, 1]$: the autocorrelation at lag $j$||$\\gamma_0 = \\Var(x_t)$; $\\rho_j = \\gamma_j/\\gamma_0 \\in [-1, 1]$: autocorelația la lagul $j$⟧']),
    ('⟦Sample counterparts (a hat marks an estimated value)||Estimatorii de selecție (accentul circumflex marchează o valoare estimată)⟧',
     ['⟦sample mean $\\bar{x} = T^{-1}\\sum_{t=1}^{T} x_t$||media de selecție $\\bar{x} = T^{-1}\\sum_{t=1}^{T} x_t$⟧',
      '⟦sample autocovariance $\\hat\\gamma_j = T^{-1}\\sum_{t=j+1}^{T}(x_t - \\bar x)(x_{t-j} - \\bar x)$||autocovarianța de selecție $\\hat\\gamma_j = T^{-1}\\sum_{t=j+1}^{T}(x_t - \\bar x)(x_{t-j} - \\bar x)$⟧',
      '⟦$\\hat\\gamma_j$ averages the products of deviations from the mean that lie $j$ periods apart||$\\hat\\gamma_j$ face media produselor abaterilor de la medie aflate la distanța de $j$ perioade⟧']),
    ('⟦Long-run variance $\\Omega = \\sum_{j=-\\infty}^{\\infty}\\gamma_j = 2\\pi f(0)$||Varianța de termen lung $\\Omega = \\sum_{j=-\\infty}^{\\infty}\\gamma_j = 2\\pi f(0)$⟧',
     ['⟦the sum of all autocovariances ($\\gamma_{-j} = \\gamma_j$); it governs the precision of $\\bar x$ (next section)||suma tuturor autocovarianțelor ($\\gamma_{-j} = \\gamma_j$); ea determină precizia lui $\\bar x$ (secțiunea următoare)⟧',
      '⟦$f(\\omega)$: the spectral density at frequency $\\omega$; $f(0)$ measures the variance of the slow, long-run movements||$f(\\omega)$: densitatea spectrală la frecvența $\\omega$; $f(0)$ măsoară varianța mișcărilor lente, de termen lung⟧'])))

frame('⟦Notation (2/2)||Notații (2/2)⟧', items(
    ('⟦Kernel $k(\\cdot)$: a weight function with $k(0) = 1$; lag $j$ receives the weight $k(j/S)$||Nucleul $k(\\cdot)$: o funcție de ponderare cu $k(0) = 1$; lagul $j$ primește ponderea $k(j/S)$⟧',
     ['⟦bandwidth $S$: the scale of the weights; lags much longer than $S$ get (almost) zero weight||lățimea de bandă $S$: scala ponderilor; lagurile mult mai lungi decît $S$ primesc pondere (aproape) zero⟧',
      '⟦Newey--West: $L = S - 1$ lags for the Bartlett kernel; $b = S/T$: the bandwidth as a share of the sample||Newey--West: $L = S - 1$ laguri pentru nucleul Bartlett; $b = S/T$: lățimea de bandă ca proporție din eșantion⟧']),
    ('⟦Size of a test: the probability of rejecting a true $H_0$||Mărimea testului: probabilitatea de a respinge o ipoteză $H_0$ adevărată⟧',
     ['⟦nominal level $5\\%$ unless stated; a test over-rejects when its actual size exceeds the nominal level||nivelul nominal este $5\\%$, dacă nu se precizează altfel; un test respinge prea des cînd mărimea lui efectivă depășește nivelul nominal⟧']),
    ('⟦HAC: heteroskedasticity and autocorrelation consistent (an estimator of $\\Omega$)||HAC: consistent la heteroscedasticitate și autocorelație (un estimator al lui $\\Omega$)⟧',
     ['⟦HAR: heteroskedasticity and autocorrelation robust (the test built on a HAC estimator)||HAR: robust la heteroscedasticitate și autocorelație (testul construit pe un estimator HAC)⟧'])))

# ===============================================================================================================
D.section('A refresher map of TSA', 'Harta recapitulării din TSA')
# ===============================================================================================================
D.frame('⟦What you already know (TSA, bachelor)||Cunoștințe din TSA (licență)⟧', table(
    'p{3.2cm}p{2.6cm}p{7.2cm}',
    '\\textbf{⟦Topic||Tema⟧} & \\textbf{TSA} & \\textbf{⟦Used in ATS for||Folosit în ATS pentru⟧}', [
        '⟦Stationarity, ACF, Wold||Staționaritate, ACF, Wold⟧ & ⟦TSA, Chapter 1||TSA, Capitolul 1⟧ & ⟦long-run variance, HAC, bootstrap (this chapter)||varianța de termen lung, HAC, bootstrap (acest capitol)⟧',
        'ARMA & ⟦TSA, Chapter 2||TSA, Capitolul 2⟧ & ⟦benchmarks, Monte Carlo designs, sieve bootstrap||modele de referință, planuri Monte Carlo, sieve bootstrap⟧',
        '⟦Unit roots, ARIMA||Rădăcini unitare, ARIMA⟧ & ⟦TSA, Chapter 3||TSA, Capitolul 3⟧ & ⟦nonstandard asymptotics, spurious regression, Chapters 2, 4, 16||asimptotică nestandard, regresie falsă, capitolele 2, 4, 16⟧',
        'GARCH & ⟦TSA, Chapter 5||TSA, Capitolul 5⟧ & ⟦martingale differences, Chapters 8--9||diferențe de martingală, capitolele 8--9⟧',
        '⟦VAR, Granger||VAR, Granger⟧ & ⟦TSA, Chapter 6||TSA, Capitolul 6⟧ & ⟦structural VAR, local projections, BVAR (Chapters 3, 5)||VAR structural, proiecții locale, BVAR (capitolele 3, 5)⟧',
        '⟦Cointegration, VECM||Cointegrare, VECM⟧ & ⟦TSA, Chapter 7||TSA, Capitolul 7⟧ & ⟦ARDL, panel cointegration (Chapter 4)||ARDL, cointegrare panel (Capitolul 4)⟧',
        '⟦Long memory||Memorie lungă⟧ & ⟦TSA, Chapter 8||TSA, Capitolul 8⟧ & ⟦local Whittle, rough volatility (Chapter 10)||local Whittle, rough volatility (Capitolul 10)⟧',
        '⟦State space, Markov switching||Spațiul stărilor, Markov switching⟧ & ⟦TSA, Chapter 10||TSA, Capitolul 10⟧ & ⟦filtering and regimes (Chapters 6, 7)||filtrare și regimuri (capitolele 6, 7)⟧'], 'scriptsize') +
    items('⟦Slides of the bachelor course: TSA, Chapter 1 to TSA, Chapter 10; each ATS chapter links to the TSA chapter it extends||Slide-urile cursului de licență: de la TSA, Capitolul 1 la TSA, Capitolul 10; fiecare capitol ATS trimite la capitolul TSA pe care îl continuă⟧'),
    'footnotesize')

frame('⟦Stationarity and the Wold representation||Staționaritatea și reprezentarea Wold⟧', items(
    ('⟦TSA, Chapter 1. Weak stationarity: constant mean and $\\gamma_j$ depending only on $j$||TSA, Capitolul 1. Staționaritate slabă: medie constantă și $\\gamma_j$ care depinde doar de $j$⟧',
     ['⟦strict stationarity: all finite-dimensional distributions are invariant to a shift in time||staționaritate strictă: toate distribuțiile finit-dimensionale sînt invariante la o translație în timp⟧',
      '⟦neither implies the other without moment conditions: Cauchy i.i.d.\\ is strictly but not weakly stationary (no variance)||niciuna nu o implică pe cealaltă fără condiții de momente: Cauchy i.i.d.\\ este strict, dar nu slab staționar (nu are varianță)⟧']),
    ('⟦Wold theorem \\refHamilton: every weakly stationary, purely nondeterministic series is a weighted sum of past innovations||Teorema lui Wold \\refHamilton: orice serie slab staționară, pur nedeterministă, este o sumă ponderată de inovații trecute⟧',
     ['$x_t - \\mu = \\sum_{j\\ge 0}\\psi_j\\varepsilon_{t-j}$, $\\quad \\psi_0 = 1$, $\\quad \\sum_j\\psi_j^2 < \\infty$',
      '⟦$\\varepsilon_t$: white noise with variance $\\sigma^2$, the one-step forecast error; $\\psi_j$: the effect of a shock after $j$ periods||$\\varepsilon_t$: zgomot alb cu varianța $\\sigma^2$, eroarea prognozei pe un pas; $\\psi_j$: efectul unui șoc după $j$ perioade⟧',
      '⟦$\\varepsilon_t$ is uncorrelated, not necessarily independent: GARCH innovations are Wold innovations||$\\varepsilon_t$ este necorelat, nu neapărat independent: inovațiile GARCH sînt inovații Wold⟧']),
    ('⟦Hence white noise is not enough for i.i.d.-based inference on squares or on extremes||De aceea, zgomotul alb nu este suficient pentru inferența de tip i.i.d.\\ pe pătrate sau pe valori extreme⟧',
     ['⟦In this chapter: $\\Omega = \\sigma^2 \\big(\\sum_j \\psi_j\\big)^2$; $\\sum_j\\psi_j$ is the cumulative (long-run) effect of a shock, so $\\Omega$ is the variance of the permanent component||În acest capitol: $\\Omega = \\sigma^2 \\big(\\sum_j \\psi_j\\big)^2$; $\\sum_j\\psi_j$ este efectul cumulat (de termen lung) al unui șoc, deci $\\Omega$ este varianța componentei permanente⟧'])))

frame('⟦ARMA and unit roots (1/2)||ARMA și rădăcini unitare (1/2)⟧', items(
    ('⟦TSA, Chapter 2. ARMA$(p,q)$: $\\phi(L)x_t = \\theta(L)\\varepsilon_t$||TSA, Capitolul 2. ARMA$(p,q)$: $\\phi(L)x_t = \\theta(L)\\varepsilon_t$⟧',
     ['⟦$L$: the lag operator, $Lx_t = x_{t-1}$; $\\phi(L) = 1 - \\phi_1L - \\dots - \\phi_pL^p$; $\\theta(L) = 1 + \\theta_1L + \\dots + \\theta_qL^q$||$L$: operatorul lag, $Lx_t = x_{t-1}$; $\\phi(L) = 1 - \\phi_1L - \\dots - \\phi_pL^p$; $\\theta(L) = 1 + \\theta_1L + \\dots + \\theta_qL^q$⟧',
      '⟦stationary if the roots of $\\phi(z)$ lie outside the unit circle; invertible if those of $\\theta(z)$ do||staționar dacă rădăcinile lui $\\phi(z)$ sînt în afara cercului unitate; inversabil dacă și rădăcinile lui $\\theta(z)$ sînt⟧']),
    ('⟦Long-run variance in closed form: $\\Omega = \\sigma^2\\,\\theta(1)^2/\\phi(1)^2$||Varianța de termen lung în formă închisă: $\\Omega = \\sigma^2\\,\\theta(1)^2/\\phi(1)^2$⟧',
     ['⟦$\\phi(1) = 1 - \\sum_i\\phi_i$ and $\\theta(1) = 1 + \\sum_i\\theta_i$: the two polynomials evaluated at $z = 1$||$\\phi(1) = 1 - \\sum_i\\phi_i$ și $\\theta(1) = 1 + \\sum_i\\theta_i$: cele două polinoame evaluate în $z = 1$⟧',
      '⟦AR(1): $\\Omega = \\sigma^2/(1-\\phi)^2$; the closer $\\phi(1)$ is to 0 (more persistence), the larger $\\Omega$||AR(1): $\\Omega = \\sigma^2/(1-\\phi)^2$; cu cît $\\phi(1)$ este mai aproape de 0 (persistență mai mare), cu atît $\\Omega$ este mai mare⟧'])))

frame('⟦ARMA and unit roots (2/2)||ARMA și rădăcini unitare (2/2)⟧', items(
    ('⟦TSA, Chapter 3. Unit root, $\\phi(1) = 0$: $\\Omega = \\infty$ and the mean is not defined||TSA, Capitolul 3. Rădăcină unitară, $\\phi(1) = 0$: $\\Omega = \\infty$, iar media nu este definită⟧',
     ['⟦the $t$-statistic has a nonstandard (Dickey--Fuller) limit||statistica $t$ are o limită nestandard (Dickey--Fuller)⟧']),
    ('⟦Spurious regression: one random walk regressed on an independent one||Regresia falsă: un mers aleator regresat pe altul, independent⟧',
     ['⟦$|t| > 2$ in 76 of 100 regressions in \\refGN||$|t| > 2$ în 76 din 100 de regresii la \\refGN⟧',
      '⟦the $t$-statistic diverges at rate $\\sqrt{T}$ \\refPhillips||statistica $t$ diverge cu viteza $\\sqrt{T}$ \\refPhillips⟧',
      '⟦no HAC estimator repairs a spurious regression (Seminar 0, B5)||niciun estimator HAC nu corectează o regresie falsă (Seminarul 0, B5)⟧']),
    ('⟦Near unit roots ($\\phi$ close to 1) are the hard case of this chapter||Rădăcinile aproape unitare ($\\phi$ aproape de 1) sînt cazul dificil al acestui capitol⟧',
     ['⟦every HAC method over-rejects there (Monte Carlo section)||acolo, toate metodele HAC resping prea des (secțiunea Monte Carlo)⟧'])))

frame('⟦GARCH, VAR, cointegration, state space||GARCH, VAR, cointegrare, spațiul stărilor⟧', items(
    ('⟦GARCH (TSA, Chapter 5): $r_t = \\sigma_t z_t$ is a martingale difference; $r_t^2$ is an ARMA(1,1) with strong, slowly decaying autocorrelation||GARCH (TSA, Capitolul 5): $r_t = \\sigma_t z_t$ este o diferență de martingală; $r_t^2$ este un ARMA(1,1) cu autocorelație puternică, care scade lent⟧',
     ['⟦$r_t$: the return; $\\sigma_t$: its conditional volatility; $z_t$: i.i.d.\\ with mean 0 and variance 1||$r_t$: randamentul; $\\sigma_t$: volatilitatea lui condiționată; $z_t$: i.i.d.\\ cu media 0 și varianța 1⟧',
      '⟦Means of returns: HAC barely matters; means of squared returns (variances, risk premia): HAC matters a lot||Mediile randamentelor: HAC contează puțin; mediile pătratelor (varianțe, prime de risc): HAC contează mult⟧']),
    ('⟦VAR (TSA, Chapter 6): Granger causality tests are Wald tests; with heteroskedastic errors they need robust covariances||VAR (TSA, Capitolul 6): testele de cauzalitate Granger sînt teste Wald; cu erori heteroscedastice au nevoie de covarianțe robuste⟧',
     ['⟦Local projections (Chapter 3) have serially correlated errors by construction: HAC is part of the method||Proiecțiile locale (Capitolul 3) au erori autocorelate prin construcție: HAC face parte din metodă⟧']),
    '⟦Cointegration (TSA, Chapter 7): long-run relations; the long-run variance reappears in FM-OLS and in the KPSS statistic||Cointegrare (TSA, Capitolul 7): relații de termen lung; varianța de termen lung reapare în FM-OLS și în statistica KPSS⟧',
    '⟦State space (TSA, Chapter 10): the Kalman filter gives the Gaussian likelihood; its standard errors still need the sandwich form under misspecification||Spațiul stărilor (TSA, Capitolul 10): filtrul Kalman dă verosimilitatea gaussiană; erorile standard cer tot forma sandwich dacă modelul este greșit specificat⟧'), 'footnotesize')

chart('⟦The series of this chapter||Seriile acestui capitol⟧', 'ats_ch0_data_dashboard', 'ATS_ch0_dependence_data', [
    '⟦Romanian HICP inflation, @{d.if.en} -- @{d.il.en}: from $@{d.imin}\\%$ (@{d.imind.en}) to $@{d.imax}\\%$ (@{d.imaxd.en}); last value $@{d.ilast}\\%$||Inflația IAPC în România, @{d.if.ro} -- @{d.il.ro}: de la $@{d.imin}\\%$ (@{d.imind.ro}) la $@{d.imax}\\%$ (@{d.imaxd.ro}); ultima valoare $@{d.ilast}\\%$⟧',
    '⟦Romanian GDP growth: @{d.gn} quarters, minimum $@{d.gmin}\\%$ in @{d.gmind}; daily: @{d.en} EUR/RON and @{d.sn} S\\&P 500 observations||Creșterea PIB în România: @{d.gn} trimestre, minimum $@{d.gmin}\\%$ în @{d.gmind}; zilnic: @{d.en} observații EUR/RON și @{d.sn} S\\&P 500⟧'],
    h='0.56\\textheight')

interp('the four series', 'celor patru serii', [
    ('⟦Inflation moves in long swings: years above and years below the 2.5\\% line||Inflația evoluează în cicluri lungi: ani peste linia de 2,5\\% și ani sub ea⟧',
     ['⟦Each monthly value shares eleven months with the previous one (annual rate): overlap adds to persistence||Fiecare valoare lunară are unsprezece luni comune cu precedenta (rata anuală): suprapunerea mărește persistența⟧']),
    ('⟦GDP growth looks close to white noise, apart from two crisis quarters||Creșterea PIB pare apropiată de un zgomot alb, cu excepția a două trimestre de criză⟧',
     ['⟦With $T = @{d.gn}$, two outliers dominate the sample variance||Cu $T = @{d.gn}$, două valori extreme domină varianța de selecție⟧']),
    '⟦EUR/RON and the S\\&P 500: volatility clusters (calm years, crisis bursts): dependence in the second moment||EUR/RON și S\\&P 500: volatility clustering (ani calmi, episoade de criză): dependență în momentul de ordinul doi⟧',
    '⟦What do you think? Which of the four series has the largest long-run variance relative to its variance?||Ce credeți? Care dintre cele patru serii are cea mai mare varianță de termen lung raportată la varianța ei?⟧'])

chart('⟦Autocorrelation in six series||Autocorelația în șase serii⟧', 'ats_ch0_acf_panel', 'ATS_ch0_dependence_data', [
    '⟦Sample ACF, lags 1--24, with the $\\pm 1.96/\\sqrt{T}$ band of the i.i.d.\\ hypothesis (shaded)||ACF de selecție, lagurile 1--24, cu banda $\\pm 1.96/\\sqrt{T}$ a ipotezei i.i.d.\\ (zona hașurată)⟧',
    '⟦$\\hat\\rho_1$: S\\&P 500 $@{a.sp.r1}$, squared $@{a.sq.r1}$, EUR/RON $@{a.eur.r1}$, BET $@{a.bet.r1}$, GDP $@{a.gdp.r1}$, inflation $@{a.inf.r1}$||$\\hat\\rho_1$: S\\&P 500 $@{a.sp.r1}$, pătrate $@{a.sq.r1}$, EUR/RON $@{a.eur.r1}$, BET $@{a.bet.r1}$, PIB $@{a.gdp.r1}$, inflație $@{a.inf.r1}$⟧'],
    h='0.55\\textheight')

interp('the autocorrelations', 'autocorelațiilor', [
    ('⟦S\\&P 500 returns: small negative $\\hat\\rho_1$; squared returns: all 24 lags above the band, $\\hat\\rho_{12} = @{a.sq.r12}$||Randamentele S\\&P 500: $\\hat\\rho_1$ mic și negativ; pătratele: toate cele 24 de laguri peste bandă, $\\hat\\rho_{12} = @{a.sq.r12}$⟧',
     ['⟦Long-run variance over variance (Andrews bandwidth): $@{a.sp.ra}$ for returns, $@{a.sq.ra}$ for squared returns||Raportul dintre varianța de termen lung și varianță (lățimea Andrews): $@{a.sp.ra}$ pentru randamente, $@{a.sq.ra}$ pentru pătrate⟧']),
    ('⟦BET and EUR/RON: positive $\\hat\\rho_1$ (thin trading, central-bank smoothing of the reference rate)||BET și EUR/RON: $\\hat\\rho_1$ pozitiv (tranzacționare redusă, netezirea cursului de referință de către banca centrală)⟧',
     ['⟦Ratios $@{a.bet.ra}$ and $@{a.eur.ra}$: modest, but enough to move a borderline $t$-statistic||Rapoarte de $@{a.bet.ra}$ și $@{a.eur.ra}$: modeste, dar suficiente pentru a schimba o statistică $t$ aflată la limită⟧']),
    '⟦Inflation: $\\hat\\rho_1 = @{a.inf.r1}$ and a ratio of $@{a.inf.ra}$: a naive standard error is about five times too small||Inflația: $\\hat\\rho_1 = @{a.inf.r1}$ și un raport de $@{a.inf.ra}$: o eroare standard naivă este de aproximativ cinci ori prea mică⟧',
    '⟦The rest of the chapter: what these ratios mean, how to estimate them, and when the estimates fail||Restul capitolului: ce înseamnă aceste rapoarte, cum le estimăm și cînd estimările eșuează⟧'])

D.recap(('the refresher map', 'harta recapitulării'), [
    '⟦TSA gave the models; ATS needs the inference that goes with dependent data||TSA a dat modelele; ATS are nevoie de inferența potrivită pentru date dependente⟧',
    '⟦White noise is not independence: GARCH returns are uncorrelated, their squares are not||Zgomotul alb nu înseamnă independență: randamentele GARCH sînt necorelate, pătratele lor nu⟧',
    '⟦The long-run variance $\\Omega = \\sigma^2\\theta(1)^2/\\phi(1)^2$ links ARMA models to the precision of a sample mean||Varianța de termen lung $\\Omega = \\sigma^2\\theta(1)^2/\\phi(1)^2$ leagă modelele ARMA de precizia unei medii de selecție⟧',
    '⟦In our data the dependence ranges from negligible (GDP growth) to extreme (inflation, squared returns)||În datele noastre, dependența variază de la neglijabilă (creșterea PIB) la extremă (inflația, pătratele randamentelor)⟧'])

# ===============================================================================================================
D.section('Asymptotics for dependent data', 'Asimptotică pentru date dependente')
# ===============================================================================================================
frame('⟦The variance of a mean under dependence||Varianța unei medii în prezența dependenței⟧', items(
    ('⟦Exact, for any weakly stationary series: the variance of the scaled mean adds up the covariances of all pairs of observations||Exact, pentru orice serie slab staționară: varianța mediei scalate adună covarianțele tuturor perechilor de observații⟧',
     ['$\\Var(\\sqrt{T}\\,\\bar x) = \\dfrac{1}{T}\\sum_{t=1}^{T}\\sum_{s=1}^{T}\\gamma_{t-s} = \\sum_{|j| < T}\\Big(1 - \\dfrac{|j|}{T}\\Big)\\gamma_j$',
      '⟦$\\gamma_{t-s}$: the covariance of $x_t$ and $x_s$; $T - |j|$ pairs lie at distance $j$, hence the weight $1 - |j|/T$||$\\gamma_{t-s}$: covarianța dintre $x_t$ și $x_s$; $T - |j|$ perechi se află la distanța $j$, de unde ponderea $1 - |j|/T$⟧']),
    ('⟦If $\\sum_j |\\gamma_j| < \\infty$, the weights tend to 1 (dominated convergence):||Dacă $\\sum_j |\\gamma_j| < \\infty$, ponderile tind la 1 (convergență dominată):⟧',
     ['$\\Var(\\sqrt{T}\\,\\bar x) \\to \\Omega = \\gamma_0 + 2\\sum_{j\\ge 1}\\gamma_j = 2\\pi f(0)$']),
    ('⟦The i.i.d.\\ formula uses $\\gamma_0$ only; the error factor is $\\Omega/\\gamma_0 = 1 + 2\\sum_{j\\ge1}\\rho_j$||Formula i.i.d.\\ folosește doar $\\gamma_0$; factorul de eroare este $\\Omega/\\gamma_0 = 1 + 2\\sum_{j\\ge1}\\rho_j$⟧',
     ['⟦factor above 1: the naive standard error is too small; below 1: too large||factor peste 1: eroarea standard naivă este prea mică; sub 1: prea mare⟧',
      '⟦effective sample size $T\\gamma_0/\\Omega$: the number of independent observations with the same precision||mărimea efectivă a eșantionului $T\\gamma_0/\\Omega$: numărul de observații independente care dau aceeași precizie⟧',
      '⟦AR(1) with $\\phi = 0.9$: 1000 observations are worth about 53 independent ones||AR(1) cu $\\phi = 0.9$: 1000 de observații echivalează cu aproximativ 53 de observații independente⟧']),
    ('⟦Two questions for the rest of the section||Două întrebări pentru restul secțiunii⟧',
     ['⟦LLN: when does $\\bar x \\to \\mu$?||LGN: cînd are loc $\\bar x \\to \\mu$?⟧',
      '⟦CLT: when is $\\sqrt{T}(\\bar x - \\mu)/\\sqrt{\\Omega}$ asymptotically $N(0,1)$?||TLC: cînd este $\\sqrt{T}(\\bar x - \\mu)/\\sqrt{\\Omega}$ asimptotic $N(0,1)$?⟧'])))

frame('⟦Ergodicity||Ergodicitate⟧', cols(
    items(
        ('⟦A strictly stationary $\\{x_t\\}$ is \\textbf{ergodic} if every shift-invariant event (unchanged when the whole path is shifted in time) has probability 0 or 1||Un proces strict staționar $\\{x_t\\}$ este \\textbf{ergodic} dacă orice eveniment invariant la translație (neschimbat cînd întreaga traiectorie este deplasată în timp) are probabilitatea 0 sau 1⟧',
         ['⟦Intuition: one long path visits the whole distribution; time averages equal ensemble averages||Intuiție: o singură traiectorie lungă parcurge întreaga distribuție; mediile în timp sînt egale cu mediile pe ansamblu⟧']),
        ('⟦\\textbf{Ergodic theorem} \\refBirkhoff: stationary, ergodic, $E|x_t| < \\infty$ $\\Rightarrow$ $\\bar x \\to E x_t$ almost surely||\\textbf{Teorema ergodică} \\refBirkhoff: staționar, ergodic, $E|x_t| < \\infty$ $\\Rightarrow$ $\\bar x \\to E x_t$ aproape sigur⟧',
         ['⟦Functions of finitely many lags of an ergodic process are ergodic: sample moments, autocovariances, OLS||Funcțiile de un număr finit de laguri ale unui proces ergodic sînt ergodice: momente de selecție, autocovarianțe, MCMMP⟧']),
        ('⟦Counterexample: $x_t = Z + \\varepsilon_t$, with $Z$ a random level drawn once and $\\varepsilon_t$ i.i.d.: stationary, not ergodic, $\\bar x \\to Z$||Contraexemplu: $x_t = Z + \\varepsilon_t$, cu $Z$ un nivel aleator extras o singură dată și $\\varepsilon_t$ i.i.d.: staționar, nu ergodic, $\\bar x \\to Z$⟧',
         ['⟦A single history of one economy is a single draw of $Z$: why regime and break questions matter (Chapters 2, 7)||Istoria unei singure economii este o singură extragere a lui $Z$: de aceea contează rupturile și regimurile (capitolele 2, 7)⟧'])),
    ph('birkhoff', 'George David Birkhoff (1884--1944)', '0.42\\textheight'), '0.66', '0.30'), 'footnotesize')

frame('⟦Mixing: dependence that fades (1/2)||Mixing: dependență care se stinge (1/2)⟧', items(
    ('⟦Strong ($\\alpha$-) mixing coefficient \\refRosenblatt:||Coeficientul de mixing tare ($\\alpha$) \\refRosenblatt:⟧',
     ['$\\alpha(m) = \\sup_t\\,\\sup\\{|P(A\\cap B) - P(A)P(B)|: A \\in \\mathcal{F}_{-\\infty}^{t}, B \\in \\mathcal{F}_{t+m}^{\\infty}\\}$',
      '⟦$\\mathcal{F}_{-\\infty}^{t}$: the events determined by $x_s$, $s \\le t$ (the past); $\\mathcal{F}_{t+m}^{\\infty}$: those determined by $x_s$, $s \\ge t + m$ (the future after a gap of $m$ periods)||$\\mathcal{F}_{-\\infty}^{t}$: evenimentele determinate de $x_s$, $s \\le t$ (trecutul); $\\mathcal{F}_{t+m}^{\\infty}$: cele determinate de $x_s$, $s \\ge t + m$ (viitorul de după un interval de $m$ perioade)⟧',
      '⟦$|P(A\\cap B) - P(A)P(B)|$ is 0 when $A$ and $B$ are independent: $\\alpha(m)$ is the largest dependence between a past and a future event $m$ periods apart||$|P(A\\cap B) - P(A)P(B)|$ este 0 cînd $A$ și $B$ sînt independente: $\\alpha(m)$ este cea mai mare dependență dintre un eveniment trecut și unul viitor aflate la $m$ perioade distanță⟧']),
    ('⟦$\\alpha$-mixing: $\\alpha(m) \\to 0$ as $m \\to \\infty$, i.e.\\ the distant past and future become independent||$\\alpha$-mixing: $\\alpha(m) \\to 0$ cînd $m \\to \\infty$, adică trecutul și viitorul îndepărtat devin independente⟧',
     ['⟦$\\beta$- and $\\phi$-mixing are stronger; mixing implies ergodicity \\refBradley||$\\beta$-mixing și $\\phi$-mixing sînt mai tari; mixing implică ergodicitate \\refBradley⟧'])))

frame('⟦Mixing: dependence that fades (2/2)||Mixing: dependență care se stinge (2/2)⟧', items(
    ('⟦Models that are mixing||Modele care sînt mixing⟧',
     ['⟦stationary ARMA with continuous innovations: geometrically $\\beta$-mixing \\refMokkadem||ARMA staționar cu inovații continue: $\\beta$-mixing geometric \\refMokkadem⟧',
      '⟦strictly stationary GARCH(1,1), stochastic volatility: geometrically $\\beta$-mixing \\refCC||GARCH(1,1) strict staționar, volatilitate stochastică: $\\beta$-mixing geometric \\refCC⟧',
      '⟦geometric: $\\beta(m) \\le C\\lambda^m$ for some constants $C > 0$ and $0 < \\lambda < 1$||geometric: $\\beta(m) \\le C\\lambda^m$ pentru niște constante $C > 0$ și $0 < \\lambda < 1$⟧']),
    ('⟦Models that are not||Modele care nu sînt mixing⟧',
     ['⟦unit roots, long memory with $d > 0$ (TSA, Chapter 8), some deterministic chaos||rădăcini unitare, memorie lungă cu $d > 0$ (TSA, Capitolul 8), unele procese haotice deterministe⟧',
      '⟦there mixing fails, or is too slow for the standard CLT||în aceste cazuri, mixing nu are loc sau este prea lent pentru TLC standard⟧']),
    ('⟦Mixing coefficients cannot be estimated from one path||Coeficienții de mixing nu pot fi estimați dintr-o singură traiectorie⟧',
     ['⟦the assumption is checked through the model, not tested||ipoteza se verifică prin model, nu se testează⟧'])))

frame('⟦Laws of large numbers for dependent data||Legi ale numerelor mari pentru date dependente⟧', items(
    ('⟦\\textbf{$L^2$ law}: weakly stationary with $\\gamma_j \\to 0$ $\\Rightarrow$ $E(\\bar x - \\mu)^2 \\to 0$||\\textbf{Legea în $L^2$}: slab staționar cu $\\gamma_j \\to 0$ $\\Rightarrow$ $E(\\bar x - \\mu)^2 \\to 0$⟧',
     ['⟦Proof: $E(\\bar x - \\mu)^2 = T^{-1}\\sum_{|j|<T}(1 - |j|/T)\\gamma_j$, and the Cesàro mean (the average of the first terms) of the sequence $\\gamma_j \\to 0$ tends to 0||Demonstrație: $E(\\bar x - \\mu)^2 = T^{-1}\\sum_{|j|<T}(1 - |j|/T)\\gamma_j$, iar media Cesàro (media aritmetică a primilor termeni) a șirului $\\gamma_j \\to 0$ tinde la 0⟧']),
    ('⟦\\textbf{Ergodic law} \\refBirkhoff: almost sure convergence, only $E|x_t| < \\infty$, no second moment||\\textbf{Legea ergodică} \\refBirkhoff: convergență aproape sigură, doar $E|x_t| < \\infty$, fără moment de ordinul doi⟧',
     ['⟦Covers squared returns of a GARCH with infinite fourth moment: means converge, but the CLT may fail||Acoperă pătratele randamentelor unui GARCH cu moment de ordinul patru infinit: mediile converg, dar TLC poate să nu aibă loc⟧']),
    '⟦\\textbf{Mixingale and near-epoch dependence}: the versions used in econometric theory for functions of mixing processes \\refHamilton||\\textbf{Mixingale și dependență near-epoch}: variantele folosite în teoria econometrică pentru funcții de procese mixing \\refHamilton⟧',
    '⟦Consistency (LLN) is cheap; valid standard errors (CLT plus a consistent $\\hat\\Omega$) are the hard part||Consistența (LGN) se obține ușor; erorile standard valide (TLC plus un $\\hat\\Omega$ consistent) sînt partea dificilă⟧'))

frame('⟦Martingale differences and their central limit theorem||Diferențele de martingală și teorema limită centrală⟧', items(
    ('⟦$\\{u_t\\}$ is a \\textbf{martingale difference sequence} (MDS) if $E(u_t \\mid \\mathcal{F}_{t-1}) = 0$||$\\{u_t\\}$ este o \\textbf{secvență de diferențe de martingală} (MDS) dacă $E(u_t \\mid \\mathcal{F}_{t-1}) = 0$⟧',
     ['⟦$\\mathcal{F}_{t-1}$: the information available at $t-1$; the past does not predict $u_t$ on average||$\\mathcal{F}_{t-1}$: informația disponibilă la $t-1$; în medie, trecutul nu prognozează $u_t$⟧',
      '⟦Uncorrelated with every function of the past, but may be conditionally heteroskedastic: GARCH returns, scores of a correct likelihood, one-step forecast errors of an optimal forecast||Necorelat cu orice funcție de trecut, dar poate fi condiționat heteroscedastic: randamente GARCH, scoruri ale unei verosimilități corecte, erorile prognozelor optime pe un pas⟧']),
    ('⟦\\textbf{MDS CLT} \\refBillingsley: stationary, ergodic MDS with $E u_t^2 = \\sigma^2 < \\infty$ $\\Rightarrow$ $\\sqrt{T}\\,\\bar u \\to_d N(0, \\sigma^2)$||\\textbf{TLC pentru MDS} \\refBillingsley: MDS staționară, ergodică, cu $E u_t^2 = \\sigma^2 < \\infty$ $\\Rightarrow$ $\\sqrt{T}\\,\\bar u \\to_d N(0, \\sigma^2)$⟧',
     ['⟦$\\to_d$: convergence in distribution; nonstationary MDS: Lindeberg-type conditions \\refBrown||$\\to_d$: convergență în distribuție; MDS nestaționare: condiții de tip Lindeberg \\refBrown⟧',
      '⟦Here $\\Omega = \\gamma_0$: no autocorrelation correction is needed, only heteroskedasticity-robust errors \\refWhiteH||Aici $\\Omega = \\gamma_0$: nu este nevoie de corecție pentru autocorelație, doar de erori robuste la heteroscedasticitate \\refWhiteH⟧']),
    '⟦Overlapping $h$-step forecast errors are not an MDS: they follow an MA$(h-1)$ (Section ``Overlapping observations\'\')||Erorile prognozelor pe $h$ pași, suprapuse, nu sînt MDS: urmează un MA$(h-1)$ (secțiunea „Observații suprapuse”)⟧'))

frame('⟦Central limit theorems beyond martingale differences (1/2)||Teoreme limită centrală dincolo de diferențele de martingală (1/2)⟧', items(
    ('⟦\\textbf{Mixing CLT} \\refIbragimov: if $x_t$ is stationary and||\\textbf{TLC pentru procese mixing} \\refIbragimov: dacă $x_t$ este staționar și⟧',
     ['$E|x_t|^{2+\\delta} < \\infty$, $\\quad \\sum_m \\alpha(m)^{\\delta/(2+\\delta)} < \\infty$, $\\quad \\Omega > 0$ $\\;\\Rightarrow\\;$ $\\sqrt{T}(\\bar x - \\mu) \\to_d N(0, \\Omega)$',
      '⟦$\\delta > 0$: the number of moments beyond the second; $\\alpha(m)$: the mixing coefficient of the previous section||$\\delta > 0$: numărul de momente peste ordinul doi; $\\alpha(m)$: coeficientul de mixing din secțiunea anterioară⟧',
      '⟦trade-off: more moments (larger $\\delta$) allow slower mixing; the first CLT under strong mixing is \\refRosenblatt||compromis: mai multe momente ($\\delta$ mai mare) permit un mixing mai lent; prima TLC sub mixing tare este \\refRosenblatt⟧']),
    ('⟦\\textbf{Linear processes} \\refPS: $x_t - \\mu = \\sum\\psi_j\\varepsilon_{t-j}$ with i.i.d.\\ or MDS $\\varepsilon_t$ and $\\sum j|\\psi_j| < \\infty$||\\textbf{Procese liniare} \\refPS: $x_t - \\mu = \\sum\\psi_j\\varepsilon_{t-j}$ cu $\\varepsilon_t$ i.i.d.\\ sau MDS și $\\sum j|\\psi_j| < \\infty$⟧',
     ['⟦the condition on $\\psi_j$ requires the effect of a shock to die out fast enough||condiția asupra lui $\\psi_j$ cere ca efectul unui șoc să se stingă suficient de repede⟧'])))

frame('⟦Central limit theorems beyond martingale differences (2/2)||Teoreme limită centrală dincolo de diferențele de martingală (2/2)⟧', items(
    ('⟦Beveridge--Nelson decomposition of the lag polynomial $\\psi(L) = \\sum_j\\psi_jL^j$:||Descompunerea Beveridge--Nelson a polinomului de laguri $\\psi(L) = \\sum_j\\psi_jL^j$:⟧',
     ['$\\psi(L) = \\psi(1) - (1-L)\\tilde\\psi(L)$, $\\quad$ ⟦so||deci⟧ $\\quad \\sqrt{T}(\\bar x - \\mu) = \\psi(1)\\sqrt{T}\\bar\\varepsilon + o_p(1)$',
      '⟦$\\psi(1) = \\sum_j\\psi_j$: the long-run effect of a shock; $\\tilde\\psi(L)$: the polynomial of the transitory part; $o_p(1)$: a term that tends to 0 in probability||$\\psi(1) = \\sum_j\\psi_j$: efectul de termen lung al unui șoc; $\\tilde\\psi(L)$: polinomul componentei tranzitorii; $o_p(1)$: un termen care tinde în probabilitate la 0⟧',
      '⟦the mean of $x_t$ behaves like $\\psi(1)$ times the mean of the innovations, hence $\\Omega = \\sigma^2\\psi(1)^2$||media lui $x_t$ se comportă ca $\\psi(1)$ înmulțit cu media inovațiilor, de unde $\\Omega = \\sigma^2\\psi(1)^2$⟧']),
    ('⟦Functional versions (invariance principles) give the Brownian-motion limits||Versiunile funcționale (principii de invarianță) dau limitele de tip mișcare browniană⟧',
     ['⟦they underlie the unit-root theory and the fixed-$b$ theory (next section)||pe ele se sprijină teoria rădăcinilor unitare și teoria fixed-$b$ (secțiunea următoare)⟧']),
    ('⟦All three CLTs need $0 < \\Omega < \\infty$||Toate cele trei TLC cer $0 < \\Omega < \\infty$⟧',
     ['⟦unit roots give $\\Omega = \\infty$; over-differencing gives $\\Omega = 0$||rădăcinile unitare dau $\\Omega = \\infty$; supradiferențierea dă $\\Omega = 0$⟧'])))

chart('⟦How much information does dependence remove?||Cîtă informație elimină dependența?⟧', 'ats_ch0_lrv_ar1', 'ATS_ch0_long_run_variance', [
    '⟦Left: $T\\Var(\\bar x)/\\gamma_0$ for an AR(1), theory $(1+\\phi)/(1-\\phi)$ and @{l.reps} simulations with $T = @{l.T}$; right: asymptotic size of the naive 5\\% test, $2[1 - \\Phi(1.96/\\sqrt{(1+\\phi)/(1-\\phi)})]$, with $\\Phi$ the standard normal distribution function||Stînga: $T\\Var(\\bar x)/\\gamma_0$ pentru un AR(1), teoria $(1+\\phi)/(1-\\phi)$ și @{l.reps} simulări cu $T = @{l.T}$; dreapta: mărimea asimptotică a testului naiv de 5\\%, $2[1 - \\Phi(1.96/\\sqrt{(1+\\phi)/(1-\\phi)})]$, unde $\\Phi$ este funcția de repartiție a distribuției Normale standard⟧'],
    h='0.56\\textheight')

interp('the variance inflation', 'creșterii varianței', [
    ('⟦$\\phi = 0.5$: the factor is $@{l.f05}$ (simulated $@{l.sim05}$); $\\phi = 0.9$: $@{l.f09}$ (simulated $@{l.sim09}$, the finite-$T$ factor $1 - |j|/T$ lowers it)||$\\phi = 0,5$: factorul este $@{l.f05}$ (simulat $@{l.sim05}$); $\\phi = 0,9$: $@{l.f09}$ (simulat $@{l.sim09}$; factorul $1 - |j|/T$ al eșantionului finit îl reduce)⟧',
     ['⟦The naive test rejects a true $H_0$ with probability $@{l.s03}\\%$ at $\\phi = 0.3$, $@{l.s05}\\%$ at $0.5$ and $@{l.s09}\\%$ at $0.9$||Testul naiv respinge o ipoteză $H_0$ adevărată cu probabilitatea $@{l.s03}\\%$ la $\\phi = 0,3$, $@{l.s05}\\%$ la $0,5$ și $@{l.s09}\\%$ la $0,9$⟧']),
    ('⟦Negative dependence works the other way: $\\phi = -0.5$ gives a factor $@{l.fm05}$, a conservative naive test||Dependența negativă acționează invers: $\\phi = -0,5$ dă un factor de $@{l.fm05}$, deci un test naiv conservator⟧',
     ['⟦The S\\&P 500 mean return is an example: its HAC standard error is smaller than the naive one||Media randamentelor S\\&P 500 este un exemplu: eroarea ei standard HAC este mai mică decît cea naivă⟧']),
    '⟦Confidence intervals inherit the factor: a naive 95\\% interval covers $\\mu$ only about $@{l.c05}\\%$ of the time at $\\phi = 0.5$||Intervalele de încredere moștenesc factorul: un interval naiv de 95\\% acoperă $\\mu$ doar în aproximativ $@{l.c05}\\%$ din cazuri la $\\phi = 0,5$⟧'])

frame('⟦Regression with dependent errors (1/2)||Regresia cu erori dependente (1/2)⟧', items(
    ('⟦Model $y_t = x_t\'\\beta + u_t$ with $E(x_t u_t) = 0$||Modelul $y_t = x_t\'\\beta + u_t$, cu $E(x_t u_t) = 0$⟧',
     ['⟦$x_t$: the vector of regressors; $\\beta$: the coefficients; $u_t$: the error, uncorrelated with $x_t$; $\'$ denotes transposition||$x_t$: vectorul regresorilor; $\\beta$: coeficienții; $u_t$: eroarea, necorelată cu $x_t$; $\'$ notează transpunerea⟧']),
    ('⟦Under a CLT for the products $x_t u_t$, the OLS estimator is asymptotically normal:||Sub o TLC pentru produsele $x_t u_t$, estimatorul MCMMP este asimptotic normal:⟧',
     ['$\\sqrt{T}(\\hat\\beta - \\beta) \\to_d N\\big(0,\\; Q^{-1}\\Omega_{xu} Q^{-1}\\big)$, $\\quad Q = E(x_t x_t\'),\\quad \\Omega_{xu} = \\sum_{j}E(x_t u_t u_{t-j} x_{t-j}\')$',
      '⟦$Q$: the second-moment matrix of the regressors; $\\Omega_{xu}$: the long-run variance of $x_t u_t$||$Q$: matricea momentelor de ordinul doi ale regresorilor; $\\Omega_{xu}$: varianța de termen lung a lui $x_t u_t$⟧',
      '⟦the form $Q^{-1}\\Omega_{xu}Q^{-1}$ is called a sandwich: $\\Omega_{xu}$ between two copies of $Q^{-1}$||forma $Q^{-1}\\Omega_{xu}Q^{-1}$ se numește sandwich: $\\Omega_{xu}$ între două copii ale lui $Q^{-1}$⟧'])))

frame('⟦Regression with dependent errors (2/2)||Regresia cu erori dependente (2/2)⟧', items(
    ('⟦Scalar slope, $x_t$ and $u_t$ independent stationary series: the error factor is||Panta scalară, $x_t$ și $u_t$ serii staționare independente: factorul de eroare este⟧',
     ['$\\Omega_{xu}/(\\gamma_{x,0}\\gamma_{u,0}) = 1 + 2\\sum_{j\\ge 1}\\rho_{x}(j)\\rho_{u}(j)$',
      '⟦$\\gamma_{x,0}, \\gamma_{u,0}$: the variances of $x_t$ and $u_t$; $\\rho_x(j), \\rho_u(j)$: their autocorrelations at lag $j$||$\\gamma_{x,0}, \\gamma_{u,0}$: varianțele lui $x_t$ și $u_t$; $\\rho_x(j), \\rho_u(j)$: autocorelațiile lor la lagul $j$⟧']),
    ('⟦A large distortion needs both a persistent regressor and a persistent error||O distorsiune mare cere atît un regresor persistent, cît și o eroare persistentă⟧',
     ['⟦if either autocorrelation is zero, the factor is 1; a persistent predictor with persistent errors is the worst case||dacă una dintre autocorelații este zero, factorul este 1; un predictor persistent cu erori persistente este cazul cel mai nefavorabil⟧']),
    ('⟦The Newey--West covariance matrix \\refNW: the sandwich $\\hat Q^{-1}\\hat\\Omega_{xu}\\hat Q^{-1}$||Matricea de covarianță Newey--West \\refNW: forma sandwich $\\hat Q^{-1}\\hat\\Omega_{xu}\\hat Q^{-1}$⟧',
     ['⟦$\\hat Q$: the sample mean of $x_tx_t\'$; $\\hat\\Omega_{xu}$: a kernel estimate of $\\Omega_{xu}$ (next section)||$\\hat Q$: media de selecție a lui $x_tx_t\'$; $\\hat\\Omega_{xu}$: o estimare prin nucleu a lui $\\Omega_{xu}$ (secțiunea următoare)⟧'])))

D.recap(('asymptotics for dependent data', 'asimptotică pentru date dependente'), [
    '⟦$\\Var(\\sqrt{T}\\bar x) \\to \\Omega = \\sum_j\\gamma_j = 2\\pi f(0)$; the i.i.d.\\ formula keeps only $\\gamma_0$||$\\Var(\\sqrt{T}\\bar x) \\to \\Omega = \\sum_j\\gamma_j = 2\\pi f(0)$; formula i.i.d.\\ păstrează doar $\\gamma_0$⟧',
    '⟦Ergodicity gives the LLN; mixing or martingale structure plus moments give the CLT||Ergodicitatea dă LGN; mixing sau structura de martingală, plus momente, dau TLC⟧',
    '⟦For an MDS, $\\Omega = \\gamma_0$: heteroskedasticity-robust errors suffice||Pentru o MDS, $\\Omega = \\gamma_0$: erorile robuste la heteroscedasticitate sînt suficiente⟧',
    '⟦Positive persistence makes naive tests over-reject; negative persistence makes them conservative||Persistența pozitivă face ca testele naive să respingă prea des; persistența negativă le face conservatoare⟧'])

# ===============================================================================================================
D.section('HAC estimation', 'Estimarea HAC')
# ===============================================================================================================
frame('⟦Estimating the long-run variance||Estimarea varianței de termen lung⟧', items(
    ('⟦Plugging in all sample autocovariances fails: $\\sum_{|j|<T}\\hat\\gamma_j = 0$ identically for demeaned data||Înlocuirea tuturor autocovarianțelor de selecție eșuează: $\\sum_{|j|<T}\\hat\\gamma_j = 0$ identic pentru datele centrate⟧',
     ['⟦high-order $\\hat\\gamma_j$ use few pairs and are mostly noise||autocovarianțele $\\hat\\gamma_j$ de ordin mare folosesc puține perechi și sînt în mare parte zgomot⟧']),
    ('⟦\\textbf{Kernel estimator}: a weighted sum of sample autocovariances||\\textbf{Estimatorul prin nucleu}: o sumă ponderată a autocovarianțelor de selecție⟧',
     ['$\\hat\\Omega = \\sum_{|j|<T} k(j/S)\\,\\hat\\gamma_j$, $\\quad k(0) = 1$, $\\quad k(x)$ ⟦decreasing in $|x|$||descrescătoare în $|x|$⟧',
      '⟦$k(j/S)$: the weight of lag $j$; $S$: the bandwidth; equivalently a smoothed periodogram at frequency 0, $\\hat\\Omega = 2\\pi\\hat f(0)$ \\refSS||$k(j/S)$: ponderea lagului $j$; $S$: lățimea de bandă; echivalent, o periodogramă netezită la frecvența 0, $\\hat\\Omega = 2\\pi\\hat f(0)$ \\refSS⟧']),
    ('⟦Consistency: $S \\to \\infty$ and $S/T \\to 0$, under mixing and moment conditions \\refAndrews||Consistență: $S \\to \\infty$ și $S/T \\to 0$, sub condiții de mixing și de momente \\refAndrews⟧',
     ['⟦the down-weighted lags create bias, the included ones create variance: $S$ balances the two||lagurile subponderate produc deplasare, cele incluse produc varianță: $S$ echilibrează cele două⟧']),
    '⟦A variance estimator must be nonnegative: not every kernel guarantees this||Un estimator de varianță trebuie să fie nenegativ: nu orice nucleu garantează acest lucru⟧'))

frame('⟦Case study: Newey and West (1987) (1/2)||Studiu de caz: Newey și West (1987) (1/2)⟧', items(
    ('⟦\\refNW, Econometrica 55(3): the Bartlett kernel $k(x) = 1 - |x|$ for $|x| \\le 1$, with $L$ lags||\\refNW, Econometrica 55(3): nucleul Bartlett $k(x) = 1 - |x|$ pentru $|x| \\le 1$, cu $L$ laguri⟧',
     ['$\\hat\\Omega_{NW} = \\hat\\Gamma_0 + \\sum_{j=1}^{L}\\Big(1 - \\dfrac{j}{L+1}\\Big)\\big(\\hat\\Gamma_j + \\hat\\Gamma_j\'\\big)$, $\\quad\\hat\\Gamma_j = T^{-1}\\sum_{t>j}\\hat h_t\\hat h_{t-j}\'$']),
    ('⟦Notation||Notațiile⟧',
     ['⟦$\\hat h_t = x_t\\hat u_t$: regressor times OLS residual $\\hat u_t$ (the score of observation $t$)||$\\hat h_t = x_t\\hat u_t$: regresorul înmulțit cu reziduul MCMMP $\\hat u_t$ (scorul observației $t$)⟧',
      '⟦$\\hat\\Gamma_j$: the sample autocovariance matrix of $\\hat h_t$ at lag $j$; $\\hat\\Gamma_0$: its variance matrix||$\\hat\\Gamma_j$: matricea autocovarianțelor de selecție ale lui $\\hat h_t$ la lagul $j$; $\\hat\\Gamma_0$: matricea ei de varianță⟧',
      '⟦$1 - j/(L+1)$: weights that decrease linearly from 1 to $1/(L+1)$; lags beyond $L$ get weight 0||$1 - j/(L+1)$: ponderi care scad liniar de la 1 la $1/(L+1)$; lagurile de după $L$ primesc pondere 0⟧'])))

frame('⟦Case study: Newey and West (1987) (2/2)||Studiu de caz: Newey și West (1987) (2/2)⟧', items(
    ('⟦\\textbf{Positive semi-definite by construction}: Bartlett weights are the autocovariances of a moving sum||\\textbf{Pozitiv semidefinit prin construcție}: ponderile Bartlett sînt autocovarianțele unei sume mobile⟧',
     ['⟦up to end effects, $\\hat\\Omega_{NW} = \\frac{1}{(L+1)T}\\sum_t\\big(\\sum_{i=0}^{L}\\hat h_{t-i}\\big)\\big(\\sum_{i=0}^{L}\\hat h_{t-i}\\big)\'$||pînă la efectele de capăt, $\\hat\\Omega_{NW} = \\frac{1}{(L+1)T}\\sum_t\\big(\\sum_{i=0}^{L}\\hat h_{t-i}\\big)\\big(\\sum_{i=0}^{L}\\hat h_{t-i}\\big)\'$⟧',
      '⟦a sum of outer products $vv\'$, each positive semi-definite, so the sum is too||o sumă de produse exterioare $vv\'$, fiecare pozitiv semidefinit, deci și suma este⟧',
      '⟦spectral view: the Bartlett (Fejér) window is nonnegative at every frequency||perspectiva spectrală: fereastra Bartlett (Fejér) este nenegativă la orice frecvență⟧']),
    ('⟦Consistency with $L \\to \\infty$, $L = o(T^{1/4})$ in the original paper||Consistență cu $L \\to \\infty$, $L = o(T^{1/4})$ în lucrarea originală⟧',
     ['⟦$L = o(T^{1/4})$: $L$ grows more slowly than $T^{1/4}$; Andrews (1991) refines the rates||$L = o(T^{1/4})$: $L$ crește mai lent decît $T^{1/4}$; Andrews (1991) rafinează ratele⟧']),
    '⟦One page of algebra, now the default robust standard error in every econometrics package||O pagină de algebră, astăzi eroarea standard robustă implicită în orice pachet econometric⟧'))

frame('⟦A truncated kernel can give a negative variance||Un nucleu trunchiat poate da o varianță negativă⟧', items(
    ('⟦Truncated (uniform) kernel: $k(x) = 1$ for $|x| \\le 1$: $\\hat\\Omega = \\hat\\gamma_0 + 2\\sum_{j=1}^{L}\\hat\\gamma_j$ (used by \\refHH for overlapping forecasts)||Nucleul trunchiat (uniform): $k(x) = 1$ pentru $|x| \\le 1$: $\\hat\\Omega = \\hat\\gamma_0 + 2\\sum_{j=1}^{L}\\hat\\gamma_j$ (folosit de \\refHH pentru prognozele suprapuse)⟧',
     ['⟦Exactly right when $\\gamma_j = 0$ for $j > L$, e.g.\\ an MA$(h-1)$ forecast error with $L = h - 1$||Exact corect cînd $\\gamma_j = 0$ pentru $j > L$, de exemplu o eroare de prognoză MA$(h-1)$ cu $L = h - 1$⟧']),
    ('⟦Ten observations alternating in sign, $(1, -1, 1, -1, 1, -1, 1, -1, 2, -2)$: $\\hat\\gamma_0 = @{n.g0}$, $\\hat\\gamma_1 = @{n.g1}$, $\\hat\\gamma_2 = @{n.g2}$||Zece observații cu semn alternant, $(1, -1, 1, -1, 1, -1, 1, -1, 2, -2)$: $\\hat\\gamma_0 = @{n.g0}$, $\\hat\\gamma_1 = @{n.g1}$, $\\hat\\gamma_2 = @{n.g2}$⟧',
     ['⟦Truncated, $L = 1$: $\\hat\\gamma_0 + 2\\hat\\gamma_1 = @{n.trunc_S1} < 0$||Trunchiat, $L = 1$: $\\hat\\gamma_0 + 2\\hat\\gamma_1 = @{n.trunc_S1} < 0$⟧',
      '⟦Bartlett, $L = 1$: $\\hat\\gamma_0 + \\hat\\gamma_1 = @{n.bart_S2} > 0$||Bartlett, $L = 1$: $\\hat\\gamma_0 + \\hat\\gamma_1 = @{n.bart_S2} > 0$⟧']),
    '⟦Lesson: a negative variance is not a numerical accident; it is a property of the kernel (Seminar 0, A3--A4)||Lecția: o varianță negativă nu este un accident numeric; este o proprietate a nucleului (Seminarul 0, A3--A4)⟧'))

chart('⟦Kernels||Nucleele⟧', 'ats_ch0_kernels', 'ATS_ch0_long_run_variance', [
    '⟦Weight $k(x)$ against $x = j/S$, the lag relative to the bandwidth; Bartlett: $1 - |x|$ ($|x| \\le 1$)||Ponderea $k(x)$ în funcție de $x = j/S$, lagul raportat la lățimea de bandă; Bartlett: $1 - |x|$ ($|x| \\le 1$)⟧',
    '⟦Parzen: $1 - 6x^2 + 6|x|^3$ ($|x| \\le 1/2$), $2(1-|x|)^3$ ($1/2 < |x| \\le 1$); QS (quadratic spectral): $\\frac{25}{12\\pi^2x^2}\\big[\\frac{\\sin(6\\pi x/5)}{6\\pi x/5} - \\cos(6\\pi x/5)\\big]$, all lags||Parzen: $1 - 6x^2 + 6|x|^3$ ($|x| \\le 1/2$), $2(1-|x|)^3$ ($1/2 < |x| \\le 1$); QS (quadratic spectral): $\\frac{25}{12\\pi^2x^2}\\big[\\frac{\\sin(6\\pi x/5)}{6\\pi x/5} - \\cos(6\\pi x/5)\\big]$, toate lagurile⟧'],
    h='0.52\\textheight')

interp('the kernels', 'nucleelor', [
    ('⟦Bartlett, Parzen and QS have nonnegative spectral windows (the Fourier transform of the weights): $\\hat\\Omega \\ge 0$ always||Bartlett, Parzen și QS au ferestre spectrale (transformata Fourier a ponderilor) nenegative: întotdeauna $\\hat\\Omega \\ge 0$⟧',
     ['⟦QS takes small negative weights (minimum $@{k.qsmin}$) yet stays positive semi-definite||QS are ponderi negative mici (minimum $@{k.qsmin}$), dar rămîne pozitiv semidefinit⟧']),
    ('⟦Kernel order $q$: $1 - k(x) \\sim c|x|^q$ near 0, with $c > 0$ a constant; Bartlett $q = 1$, Parzen and QS $q = 2$||Ordinul nucleului $q$: $1 - k(x) \\sim c|x|^q$ lîngă 0, cu $c > 0$ o constantă; Bartlett $q = 1$, Parzen și QS $q = 2$⟧',
     ['⟦bias of order $S^{-q}$, variance of order $S/T$: the optimal $S$ grows like $T^{1/(2q+1)}$||deplasare de ordinul $S^{-q}$, varianță de ordinul $S/T$: $S$ optim crește ca $T^{1/(2q+1)}$⟧',
      '⟦i.e.\\ $T^{1/3}$ for Bartlett and $T^{1/5}$ for QS||adică $T^{1/3}$ pentru Bartlett și $T^{1/5}$ pentru QS⟧']),
    '⟦\\refAndrews: QS minimises the asymptotic MSE among kernels with nonnegative estimates||\\refAndrews: QS minimizează eroarea pătratică medie asimptotică printre nucleele cu estimări nenegative⟧'])

frame('⟦Case study: Andrews (1991) and the choice of bandwidth (1/2)||Studiu de caz: Andrews (1991) și alegerea lățimii de bandă (1/2)⟧', items(
    ('⟦MSE-optimal bandwidth \\refAndrews: the $S$ that minimises the mean squared error of $\\hat\\Omega$||Lățimea optimă în sensul erorii pătratice medii \\refAndrews: valoarea $S$ care minimizează eroarea pătratică medie a lui $\\hat\\Omega$⟧',
     ['$S^* = c_k\\,(\\alpha(q)\\,T)^{1/(2q+1)}$',
      '⟦$q$: the order of the kernel; $c_k$: a constant of the kernel; $\\alpha(q)$: a function of the unknown spectrum, large for persistent series||$q$: ordinul nucleului; $c_k$: o constantă a nucleului; $\\alpha(q)$: o funcție de spectrul necunoscut, mare pentru seriile persistente⟧',
      '⟦Bartlett: $S^* = 1.1447(\\hat\\alpha(1)T)^{1/3}$; Parzen: $2.6614(\\hat\\alpha(2)T)^{1/5}$; QS: $1.3221(\\hat\\alpha(2)T)^{1/5}$||Bartlett: $S^* = 1.1447(\\hat\\alpha(1)T)^{1/3}$; Parzen: $2.6614(\\hat\\alpha(2)T)^{1/5}$; QS: $1.3221(\\hat\\alpha(2)T)^{1/5}$⟧']),
    ('⟦\\textbf{AR(1) plug-in}: fit an AR(1) with coefficient $\\hat\\rho$ to $\\hat h_t$, then||\\textbf{Metoda plug-in AR(1)}: estimăm un AR(1) cu coeficientul $\\hat\\rho$ pe $\\hat h_t$, apoi⟧',
     ['$\\hat\\alpha(1) = \\dfrac{4\\hat\\rho^2}{(1-\\hat\\rho)^2(1+\\hat\\rho)^2}$, $\\qquad \\hat\\alpha(2) = \\dfrac{4\\hat\\rho^2}{(1-\\hat\\rho)^4}$',
      '⟦both grow without bound as $\\hat\\rho \\to 1$: more persistence, wider bandwidth||ambele cresc nemărginit cînd $\\hat\\rho \\to 1$: persistență mai mare, lățime de bandă mai mare⟧'])))

frame('⟦Case study: Andrews (1991) and the choice of bandwidth (2/2)||Studiu de caz: Andrews (1991) și alegerea lățimii de bandă (2/2)⟧', items(
    ('⟦Newey--West rule of thumb: $L = \\lfloor 4(T/100)^{2/9}\\rfloor$||Regula practică Newey--West: $L = \\lfloor 4(T/100)^{2/9}\\rfloor$⟧',
     ['⟦$\\lfloor\\cdot\\rfloor$: the integer part; $L$ depends only on $T$, not on the data||$\\lfloor\\cdot\\rfloor$: partea întreagă; $L$ depinde doar de $T$, nu de date⟧',
      '⟦their nonparametric automatic selection \\refNWb estimates the spectrum instead||selecția lor automată neparametrică \\refNWb estimează în schimb spectrul⟧']),
    ('⟦Prewhitening with a VAR(1), then recolouring \\refAM||Prealbirea cu un VAR(1), apoi recolorarea \\refAM⟧',
     ['⟦filter out the AR(1) part, estimate $\\Omega$ on the residuals, then undo the filter: less bias for persistent series||se elimină componenta AR(1), se estimează $\\Omega$ pe reziduuri, apoi se inversează filtrul: deplasare mai mică pentru seriile persistente⟧']),
    ('⟦The MSE criterion targets $\\hat\\Omega$, not the test||Criteriul erorii pătratice medii vizează $\\hat\\Omega$, nu testul⟧',
     ['⟦this is the source of the size distortions of the next sections||de aici provin distorsiunile de mărime din secțiunile următoare⟧'])))

chart('⟦HAC standard errors as a function of the bandwidth||Erorile standard HAC în funcție de lățimea de bandă⟧', 'ats_ch0_hac_bandwidth', 'ATS_ch0_hac', [
    '⟦Ratio of the Bartlett HAC standard error of the mean to the naive one, $S$ from 1 to $\\min(400, T/2)$; dots: Andrews AR(1) plug-in||Raportul dintre eroarea standard HAC Bartlett a mediei și cea naivă, $S$ de la 1 la $\\min(400, T/2)$; puncte: metoda plug-in AR(1) a lui Andrews⟧'],
    h='0.56\\textheight')

interp('the bandwidth paths', 'traiectoriilor în funcție de lățimea de bandă', [
    ('⟦Squared S\\&P 500 returns: ratio $@{bw.sq.rn}$ with the rule of thumb ($S = @{bw.sq.Sn}$), $@{bw.sq.ra}$ with Andrews ($S = @{bw.sq.Sa}$), still rising to $@{bw.sq.rmax}$ at $S = 400$||Pătratele randamentelor S\\&P 500: raport $@{bw.sq.rn}$ cu regula practică ($S = @{bw.sq.Sn}$), $@{bw.sq.ra}$ cu Andrews ($S = @{bw.sq.Sa}$), în creștere pînă la $@{bw.sq.rmax}$ la $S = 400$⟧',
     ['⟦No plateau: the AR(1) plug-in misses the slow decay of volatility autocorrelation (long memory, Chapter 10)||Fără platou: metoda plug-in AR(1) nu surprinde scăderea lentă a autocorelației volatilității (memorie lungă, Capitolul 10)⟧']),
    ('⟦Romanian inflation: $@{bw.inf.rn}$ with the rule of thumb, $@{bw.inf.ra}$ with Andrews ($S = @{bw.inf.Sa}$ months)||Inflația în România: $@{bw.inf.rn}$ cu regula practică, $@{bw.inf.ra}$ cu Andrews ($S = @{bw.inf.Sa}$ luni)⟧',
     ['⟦The rule of thumb ignores the data: with $T$ fixed it gives the same $S$ for white noise and for a near unit root||Regula practică ignoră datele: la $T$ fix dă același $S$ pentru un zgomot alb și pentru o rădăcină aproape unitară⟧']),
    '⟦S\\&P 500 returns: ratio below 1 at every $S$ (negative $\\hat\\rho_1$); EUR/RON: flat near $@{bw.eur.ra}$||Randamentele S\\&P 500: raport sub 1 la orice $S$ ($\\hat\\rho_1$ negativ); EUR/RON: aproape constant, în jur de $@{bw.eur.ra}$⟧'])

frame('⟦Fixed-$b$ asymptotics||Asimptotica fixed-$b$⟧', items(
    ('⟦Standard theory: $S/T \\to 0$, $\\hat\\Omega \\to_p \\Omega$, the $t$-statistic is $N(0,1)$||Teoria standard: $S/T \\to 0$, $\\hat\\Omega \\to_p \\Omega$, statistica $t$ este $N(0,1)$⟧',
     ['⟦$\\to_p$: convergence in probability; the sampling error of $\\hat\\Omega$ is ignored||$\\to_p$: convergență în probabilitate; eroarea de selecție a lui $\\hat\\Omega$ este ignorată⟧',
      '⟦with 100--300 observations, $\\hat\\Omega$ is noisy and biased downwards: the normal critical values are too small||cu 100--300 de observații, $\\hat\\Omega$ este zgomotos și deplasat în jos: valorile critice normale sînt prea mici⟧']),
    ('⟦\\textbf{Fixed-$b$} \\refKVB, \\refKVb, \\refKV: keep $b = S/T$ fixed as $T \\to \\infty$||\\textbf{Fixed-$b$} \\refKVB, \\refKVb, \\refKV: păstrăm $b = S/T$ fix cînd $T \\to \\infty$⟧',
     ['$\\hat\\Omega/\\Omega \\to_d Q_k(b)$, $\\qquad t \\to_d W(1)/\\sqrt{Q_k(b)}$',
      '⟦$W(r)$: a standard Brownian motion on $r \\in [0,1]$ ($r$: the fraction of the sample); $Q_k(b)$: a random functional of the Brownian bridge $\\tilde W(r) = W(r) - rW(1)$||$W(r)$: o mișcare browniană standard pe $r \\in [0,1]$ ($r$: fracțiunea din eșantion); $Q_k(b)$: o funcțională aleatoare a punții browniene $\\tilde W(r) = W(r) - rW(1)$⟧',
      '⟦nonstandard but pivotal (free of unknown parameters): critical values depend only on the kernel and on $b$||nestandard, dar pivotal (nu depinde de parametri necunoscuți): valorile critice depind doar de nucleu și de $b$⟧']),
    '⟦Higher-order theory: fixed-$b$ critical values remove the leading size distortion of the normal approximation \\refSPJ||Teoria de ordin superior: valorile critice fixed-$b$ elimină termenul principal al distorsiunii de mărime din aproximarea normală \\refSPJ⟧'))

chart('⟦Fixed-$b$ critical values||Valorile critice fixed-$b$⟧', 'ats_ch0_fixed_b', 'ATS_ch0_hac', [
    '⟦Two-sided 5\\% critical values of the $t$-test for a mean with $S = bT$, simulated (20\\,000 i.i.d.\\ normal samples, $T = 500$)||Valori critice bilaterale de 5\\% ale testului $t$ pentru medie cu $S = bT$, simulate (20\\,000 de eșantioane normale i.i.d., $T = 500$)⟧'],
    h='0.55\\textheight')

interp('the fixed-$b$ critical values', 'valorilor critice fixed-$b$', [
    ('⟦Bartlett: $@{fb.b0.1}$ at $b = 0.1$, $@{fb.b0.5}$ at $b = 0.5$, $@{fb.b1.0}$ at $b = 1$ (Kiefer--Vogelsang--Bunzel statistic)||Bartlett: $@{fb.b0.1}$ la $b = 0,1$, $@{fb.b0.5}$ la $b = 0,5$, $@{fb.b1.0}$ la $b = 1$ (statistica Kiefer--Vogelsang--Bunzel)⟧',
     ['⟦Close to the cubic approximation reported in \\refKV for the Bartlett kernel||Apropiate de aproximarea cubică raportată de \\refKV pentru nucleul Bartlett⟧']),
    '⟦QS: $@{fb.q0.1}$ at $b = 0.1$ and $@{fb.q0.5}$ at $b = 0.5$: QS with a large $b$ is very noisy||QS: $@{fb.q0.1}$ la $b = 0,1$ și $@{fb.q0.5}$ la $b = 0,5$: QS cu $b$ mare este foarte zgomotos⟧',
    '⟦Larger $b$: less bias in $\\hat\\Omega$, more variance, compensated by a larger critical value: better size, lower power||$b$ mai mare: deplasare mai mică a lui $\\hat\\Omega$, varianță mai mare, compensată de o valoare critică mai mare: mărime mai bună, putere mai mică⟧',
    '⟦What do you think? Why does the critical value at $b \\to 0$ tend to 1.96?||Ce credeți? De ce tinde valoarea critică la 1,96 cînd $b \\to 0$?⟧'])

frame('⟦Recommendations for practice: Lazarus, Lewis, Stock and Watson (2018) (1/2)||Recomandări practice: Lazarus, Lewis, Stock și Watson (2018) (1/2)⟧', items(
    ('⟦\\refLLSW choose the bandwidth for the \\emph{test}: a size--power frontier, not the MSE of $\\hat\\Omega$||\\refLLSW aleg lățimea de bandă pentru \\emph{test}: o frontieră mărime--putere, nu eroarea pătratică medie a lui $\\hat\\Omega$⟧',
     ['⟦first recommendation: Newey--West with $S = 1.3\\sqrt{T}$ and fixed-$b$ critical values||prima recomandare: Newey--West cu $S = 1.3\\sqrt{T}$ și valori critice fixed-$b$⟧']),
    ('⟦Second recommendation: the equal-weighted cosine (EWC) estimator||A doua recomandare: estimatorul cosinus cu ponderi egale (EWC)⟧',
     ['$\\hat\\Omega = \\nu^{-1}\\sum_{j=1}^{\\nu}\\hat\\Lambda_j^2$, $\\qquad \\hat\\Lambda_j = \\sqrt{2/T}\\sum_t \\cos[\\pi j(t - 1/2)/T]\\,\\hat h_t$, $\\qquad \\nu = 0.4T^{2/3}$',
      '⟦$\\hat\\Lambda_j$: the projection of $\\hat h_t$ on the $j$-th cosine, a low-frequency component; each $\\hat\\Lambda_j^2$ estimates $\\Omega$||$\\hat\\Lambda_j$: proiecția lui $\\hat h_t$ pe cosinusul $j$, o componentă de frecvență joasă; fiecare $\\hat\\Lambda_j^2$ estimează $\\Omega$⟧',
      '⟦$\\nu$: the number of cosines averaged, also the degrees of freedom: critical values from Student $t_\\nu$||$\\nu$: numărul de cosinusuri mediate, egal cu numărul de grade de libertate: valori critice din distribuția Student $t_\\nu$⟧'])))

frame('⟦Recommendations for practice: Lazarus, Lewis, Stock and Watson (2018) (2/2)||Recomandări practice: Lazarus, Lewis, Stock și Watson (2018) (2/2)⟧', items(
    ('⟦The size--power trade-off is unavoidable||Compromisul mărime--putere este inevitabil⟧',
     ['⟦\\refLLS give the frontier for kernel tests||\\refLLS dau frontiera pentru testele cu nucleu⟧']),
    ('⟦Very persistent series ($\\phi$ near 1): no kernel or EWC rule is reliable||Serii foarte persistente ($\\phi$ aproape de 1): nicio regulă cu nucleu sau EWC nu este fiabilă⟧',
     ['⟦\\refMuller proposes tests valid under local-to-unity dependence (a root that tends to 1 as $T$ grows)||\\refMuller propune teste valide sub dependență de tip local-to-unity (o rădăcină care tinde la 1 odată cu creșterea lui $T$)⟧']),
    '⟦These are the defaults of the course from Chapter 1 on||Acestea sînt opțiunile implicite ale cursului începînd cu Capitolul 1⟧'))

D.recap(('HAC estimation', 'estimarea HAC'), [
    '⟦Kernel estimators down-weight distant lags; Bartlett (Newey--West), Parzen and QS are always nonnegative; the truncated kernel is not||Estimatorii prin nucleu subponderează lagurile îndepărtate; Bartlett (Newey--West), Parzen și QS sînt întotdeauna nenegativi; nucleul trunchiat nu este⟧',
    '⟦Andrews (1991) bandwidths are MSE-optimal for $\\hat\\Omega$ and adapt to persistence; the rule of thumb does not||Lățimile Andrews (1991) sînt optime pentru eroarea pătratică medie a lui $\\hat\\Omega$ și se adaptează persistenței; regula practică nu⟧',
    '⟦Fixed-$b$ critical values account for the noise in $\\hat\\Omega$; LLSW: NW with $S = 1.3\\sqrt{T}$ or EWC with $\\nu = 0.4T^{2/3}$||Valorile critice fixed-$b$ țin cont de zgomotul din $\\hat\\Omega$; LLSW: NW cu $S = 1.3\\sqrt{T}$ sau EWC cu $\\nu = 0.4T^{2/3}$⟧'])

# ===============================================================================================================
D.section('Size distortions: a Monte Carlo study', 'Distorsiuni de mărime: un studiu Monte Carlo')
# ===============================================================================================================
frame('⟦Monte Carlo design||Planul Monte Carlo⟧', items(
    ('⟦DGP: $x_t = \\phi x_{t-1} + \\varepsilon_t$, $\\varepsilon_t \\sim N(0,1)$ i.i.d., 200 burn-in values; $H_0: \\mu = 0$ is true||DGP: $x_t = \\phi x_{t-1} + \\varepsilon_t$, $\\varepsilon_t \\sim N(0,1)$ i.i.d., 200 de valori inițiale eliminate; $H_0: \\mu = 0$ este adevărată⟧',
     ['⟦$\\phi$: the AR(1) coefficient, i.e.\\ the persistence; burn-in: initial values dropped so that the series starts from its stationary distribution||$\\phi$: coeficientul AR(1), adică persistența; valorile inițiale se elimină pentru ca seria să pornească din distribuția ei staționară⟧',
      '⟦$\\phi \\in \\{0, 0.3, 0.5, 0.7, 0.9\\}$, $T \\in \\{100, 400\\}$; @{mc.reps} replications (@{mc.breps} for the bootstrap, 399 resamples each); seed 2026||$\\phi \\in \\{0; 0,3; 0,5; 0,7; 0,9\\}$, $T \\in \\{100; 400\\}$; @{mc.reps} de replicări (@{mc.breps} pentru bootstrap, cu cîte 399 de reeșantionări); sămînța 2026⟧']),
    ('⟦Seven tests at nominal 5\\%||Șapte teste la nivelul nominal de 5\\%⟧',
     ['⟦naive i.i.d.; NW rule of thumb; NW and QS with the Andrews AR(1) bandwidth (normal critical values)||naiv i.i.d.; NW cu regula practică; NW și QS cu lățimea Andrews AR(1) (valori critice normale)⟧',
      '⟦NW with $S = 1.3\\sqrt{T}$ and fixed-$b$ values; EWC with $t_\\nu$; circular block bootstrap with the Politis--White block length||NW cu $S = 1.3\\sqrt{T}$ și valori fixed-$b$; EWC cu $t_\\nu$; bootstrap circular pe blocuri cu lungimea Politis--White⟧']),
    ('⟦Monte Carlo standard error of a rejection rate $p$ estimated from $R$ replications: $\\sqrt{p(1-p)/R}$||Eroarea standard Monte Carlo a unei rate de respingere $p$ estimate din $R$ replicări: $\\sqrt{p(1-p)/R}$⟧',
     ['⟦about $0.3$ percentage points (pp) at $p = 5\\%$ and $R = 5000$||aproximativ $0,3$ puncte procentuale (pp) la $p = 5\\%$ și $R = 5000$⟧']),
    '⟦The same design as the Monte Carlo sections of \\refAndrews and \\refKV: AR(1) data, rejection rates under the null||Același plan ca în secțiunile Monte Carlo din \\refAndrews și \\refKV: date AR(1), rate de respingere sub ipoteza nulă⟧'))

chart('⟦Size of seven tests under AR(1) dependence||Mărimea a șapte teste sub dependență AR(1)⟧', 'ats_ch0_mc_size', 'ATS_ch0_size_monte_carlo', [
    '⟦Rejection rate of $H_0: \\mu = 0$ (true) against $\\phi$; dotted line: 5\\%||Rata de respingere a ipotezei $H_0: \\mu = 0$ (adevărată) în funcție de $\\phi$; linia punctată: 5\\%⟧'],
    h='0.58\\textheight')

D.frame('⟦Size in numbers (\\%)||Mărimea în cifre (\\%)⟧', table(
    'lrrrrrr', '& \\multicolumn{3}{c}{$T = 100$} & \\multicolumn{3}{c}{$T = 400$} \\\\\n⟦Test||Testul⟧ & $\\phi = 0$ & $0.5$ & $0.9$ & $\\phi = 0$ & $0.5$ & $0.9$', [
        f'{lab} & ' + ' & '.join(f'@{{mc.{TT}.{p}.{k}}}' for TT in ('100', '400') for p in ('0', '5', '9'))
        for k, lab in (('naive', '⟦naive i.i.d.||naiv i.i.d.⟧'), ('nw', '⟦NW, rule of thumb||NW, regula practică⟧'),
                       ('andrews', '⟦NW, Andrews||NW, Andrews⟧'), ('qs', '⟦QS, Andrews||QS, Andrews⟧'),
                       ('llsw', '⟦NW, $1.3\\sqrt{T}$, fixed-$b$||NW, $1.3\\sqrt{T}$, fixed-$b$⟧'), ('ewc', 'EWC, $t_\\nu$'),
                       ('cbb', '⟦circular block bootstrap||bootstrap circular pe blocuri⟧'))], 'footnotesize') +
    items('⟦Monte Carlo standard errors: about 0.3 pp near 5\\%, about 0.7 pp near 30\\% (bootstrap rows: about twice as large)||Erori standard Monte Carlo: aproximativ 0,3 pp în jurul valorii de 5\\%, aproximativ 0,7 pp în jurul valorii de 30\\% (rîndurile bootstrap: de aproximativ două ori mai mari)⟧'),
    'footnotesize')

interp('the Monte Carlo', 'studiului Monte Carlo', [
    ('⟦Naive test: $@{mc.100.5.naive}\\%$ at $\\phi = 0.5$ and $@{mc.100.9.naive}\\%$ at $\\phi = 0.9$; more data do not help ($@{mc.400.9.naive}\\%$ at $T = 400$)||Testul naiv: $@{mc.100.5.naive}\\%$ la $\\phi = 0,5$ și $@{mc.100.9.naive}\\%$ la $\\phi = 0,9$; mai multe date nu ajută ($@{mc.400.9.naive}\\%$ la $T = 400$)⟧',
     ['⟦The distortion is a property of the estimator, not of the sample size||Distorsiunea este o proprietate a estimatorului, nu a mărimii eșantionului⟧']),
    ('⟦NW with the rule of thumb: $@{mc.100.9.nw}\\%$ at $\\phi = 0.9$, $T = 100$; Andrews bandwidths halve the excess; fixed-$b$ and EWC come closest ($@{mc.100.9.llsw}\\%$, $@{mc.100.9.ewc}\\%$)||NW cu regula practică: $@{mc.100.9.nw}\\%$ la $\\phi = 0,9$, $T = 100$; lățimile Andrews reduc excesul la jumătate; fixed-$b$ și EWC se apropie cel mai mult ($@{mc.100.9.llsw}\\%$, $@{mc.100.9.ewc}\\%$)⟧',
     ['⟦At $T = 400$ and $\\phi = 0.5$: $@{mc.400.5.llsw}\\%$ and $@{mc.400.5.ewc}\\%$, essentially exact||La $T = 400$ și $\\phi = 0,5$: $@{mc.400.5.llsw}\\%$ și $@{mc.400.5.ewc}\\%$, practic exacte⟧']),
    '⟦The block bootstrap is not a free lunch: $@{mc.100.9.cbb}\\%$ at $\\phi = 0.9$, $T = 100$, between NW and fixed-$b$||Bootstrap-ul pe blocuri nu rezolvă totul: $@{mc.100.9.cbb}\\%$ la $\\phi = 0,9$, $T = 100$, între NW și fixed-$b$⟧',
    '⟦Our inflation series has $\\hat\\rho_1 = @{a.inf.r1}$: outside the range where any of these tests is reliable (AI mini-case)||Seria noastră de inflație are $\\hat\\rho_1 = @{a.inf.r1}$: în afara domeniului în care vreunul dintre aceste teste este fiabil (mini-studiul de caz AI)⟧'], 'footnotesize')

D.recap(('size distortions', 'distorsiunile de mărime'), [
    '⟦Always report the actual size of the procedure you use, at the persistence of your data||Raportați întotdeauna mărimea efectivă a procedurii folosite, la persistența datelor analizate⟧',
    '⟦Fixed-$b$ NW and EWC (LLSW 2018) dominate the classical choices in size at a modest cost in power||NW fixed-$b$ și EWC (LLSW 2018) domină alegerile clasice în privința mărimii, cu un cost modest în putere⟧',
    '⟦A Monte Carlo is an experiment: fix the seed, report $R$ and the Monte Carlo standard error||Un studiu Monte Carlo este un experiment: fixați sămînța, raportați $R$ și eroarea standard Monte Carlo⟧'])

# ===============================================================================================================
D.section('Bootstrap for dependent data', 'Bootstrap pentru date dependente')
# ===============================================================================================================
frame('⟦Why the i.i.d.\\ bootstrap fails||Eșecul bootstrap-ului i.i.d.⟧', cols(
    items(
        ('⟦Efron\'s bootstrap \\refEfron resamples single observations: the dependence is destroyed||Bootstrap-ul lui Efron \\refEfron reeșantionează observații individuale: dependența este distrusă⟧',
         ['⟦a star marks a bootstrap quantity: $\\bar x^*$ is the mean of one resample, $\\Var^*$ the variance over resamples||asteriscul marchează o mărime bootstrap: $\\bar x^*$ este media unui eșantion reeșantionat, $\\Var^*$ varianța pe reeșantionări⟧',
          '$\\Var^*(\\sqrt{T}\\bar x^*) = \\hat\\gamma_0$, ⟦not||nu⟧ $\\Omega$: ⟦the i.i.d.\\ bootstrap reproduces the naive standard error||bootstrap-ul i.i.d.\\ reproduce eroarea standard naivă⟧']),
        ('⟦\\refSingh: even for $m$-dependent data (independent beyond distance $m$) the i.i.d.\\ bootstrap of the mean is inconsistent||\\refSingh: chiar pentru date $m$-dependente (independente la distanțe mai mari de $m$), bootstrap-ul i.i.d.\\ al mediei este inconsistent⟧',
         ['⟦Idea of the block bootstrap: resample blocks long enough to keep the dependence inside them||Ideea bootstrap-ului pe blocuri: reeșantionăm blocuri suficient de lungi pentru a păstra dependența în interiorul lor⟧']),
        '⟦Price to pay: dependence across block joints is lost, and the block length becomes a tuning parameter||Prețul: dependența de la granițele blocurilor se pierde, iar lungimea blocului devine un parametru de reglaj⟧'),
    ph('efron', 'Bradley Efron (2007)', '0.40\\textheight'), '0.66', '0.30'), 'footnotesize')

frame('⟦Case study: the moving-block bootstrap of Künsch (1989)||Studiu de caz: bootstrap pe blocuri mobile, Künsch (1989)⟧', cols(
    items(
        ('⟦\\refKunsch: overlapping blocks $B_i = (x_i, \\dots, x_{i+l-1})$ of length $l$, $i = 1, \\dots, T - l + 1$||\\refKunsch: blocuri suprapuse $B_i = (x_i, \\dots, x_{i+l-1})$ de lungime $l$, $i = 1, \\dots, T - l + 1$⟧',
         ['⟦draw $k = \\lceil T/l\\rceil$ blocks with replacement ($\\lceil\\cdot\\rceil$: rounding up), concatenate, keep the first $T$ values||extragem $k = \\lceil T/l\\rceil$ blocuri cu întoarcere ($\\lceil\\cdot\\rceil$: rotunjire în sus), le concatenăm și păstrăm primele $T$ valori⟧']),
        ('⟦Consistency for smooth functions of means if $l \\to \\infty$, $l/T \\to 0$||Consistent pentru funcții netede de medii, dacă $l \\to \\infty$, $l/T \\to 0$⟧',
         ['$\\Var^*(\\sqrt{T}\\bar x^*) \\approx \\sum_{|j|<l}(1 - |j|/l)\\hat\\gamma_j$: ⟦a Bartlett estimate with $S = l$||o estimare Bartlett cu $S = l$⟧',
          '⟦Optimal $l \\propto T^{1/3}$ for variance and bias, as for the Bartlett bandwidth \\refLahiri||$l$ optim $\\propto T^{1/3}$ pentru varianță și deplasare, ca pentru lățimea Bartlett \\refLahiri⟧']),
        ('⟦Edge effect: end observations enter fewer blocks, so $E^*\\bar x^* \\ne \\bar x$||Efect de capăt: observațiile de la margini intră în mai puține blocuri, deci $E^*\\bar x^* \\ne \\bar x$⟧',
         ['⟦$E^*$: the expectation over resamples; centre the bootstrap statistics at $E^*\\bar x^*$||$E^*$: media pe reeșantionări; statisticile bootstrap se centrează în $E^*\\bar x^*$⟧'])),
    ph('kunsch', 'Hans Rudolf Künsch (2007)', '0.34\\textheight'), '0.64', '0.32'), 'footnotesize')

frame('⟦Circular and stationary bootstrap||Bootstrap circular și bootstrap staționar⟧', items(
    ('⟦\\textbf{Circular block bootstrap} (Politis and Romano, 1992; \\refLahiri): wrap the data on a circle, $x_{T+i} = x_i$||\\textbf{Bootstrap circular pe blocuri} (Politis și Romano, 1992; \\refLahiri): așezăm datele pe un cerc, $x_{T+i} = x_i$⟧',
     ['⟦Every observation enters $l$ blocks: $E^*\\bar x^* = \\bar x$ exactly (Seminar 0, A5--A6)||Fiecare observație intră în $l$ blocuri: $E^*\\bar x^* = \\bar x$ exact (Seminarul 0, A5--A6)⟧']),
    ('⟦\\textbf{Stationary bootstrap} \\refPR: block lengths geometric with mean $1/p$, uniform starting points, data wrapped on a circle||\\textbf{Bootstrap-ul staționar} \\refPR: lungimile blocurilor au distribuție geometrică cu media $1/p$, începuturile sînt uniforme, datele sînt așezate pe cerc⟧',
     ['⟦Equivalently: each step continues the block with probability $1 - p$ or jumps to a random point with probability $p$||Echivalent: la fiecare pas blocul continuă cu probabilitatea $1 - p$ sau sare într-un punct aleator cu probabilitatea $p$⟧',
      '⟦The resampled series is stationary; the method is less sensitive to the choice of $1/p$ than MBB to $l$||Seria reeșantionată este staționară; metoda este mai puțin sensibilă la alegerea lui $1/p$ decît MBB la alegerea lui $l$⟧']),
    '⟦Efficiency: MBB and CBB have a smaller asymptotic MSE for the variance than the stationary bootstrap at their optimal lengths \\refLahiri||Eficiență: MBB și CBB au eroarea pătratică medie asimptotică mai mică pentru varianță decît bootstrap-ul staționar, la lungimile optime \\refLahiri⟧',
    '⟦The stationary bootstrap is the engine of the Reality Check (White 2000) and of the SPA test (Chapter 1)||Bootstrap-ul staționar stă la baza testului Reality Check (White 2000) și a testului SPA (Capitolul 1)⟧'), 'footnotesize')

frame('⟦Choosing the block length (1/2)||Alegerea lungimii blocului (1/2)⟧', items(
    ('⟦\\refPW, corrected by \\refPPW: plug-in estimate of the MSE-optimal mean block length||\\refPW, corectată de \\refPPW: estimarea plug-in a lungimii medii optime a blocului⟧',
     ['$\\hat b_{opt} = \\Big(\\dfrac{2\\hat G^2}{\\hat D}\\Big)^{1/3} T^{1/3}$, $\\quad \\hat G = \\sum_{|k|\\le M}\\lambda(k/M)\\,|k|\\,\\hat\\gamma_k$, $\\quad \\hat g = \\sum_{|k|\\le M}\\lambda(k/M)\\,\\hat\\gamma_k$',
      '$\\hat D_{SB} = 2\\hat g^2$ ⟦(stationary)||(staționar)⟧, $\\hat D_{CB} = \\tfrac{4}{3}\\hat g^2$ ⟦(circular)||(circular)⟧']),
    ('⟦Notation||Notațiile⟧',
     ['⟦$\\hat G$: autocovariances weighted by their lag, the bias term; $\\hat g$: an estimate of $\\Omega$; $\\hat D$: the variance term||$\\hat G$: autocovarianțele ponderate cu lagul lor, termenul de deplasare; $\\hat g$: o estimare a lui $\\Omega$; $\\hat D$: termenul de varianță⟧',
      '⟦$\\lambda$: the flat-top (trapezoid) kernel; $M = 2\\hat m$: the truncation lag||$\\lambda$: nucleul flat-top (trapez); $M = 2\\hat m$: lagul de trunchiere⟧',
      '⟦$\\hat m$: the first lag after which $K_T$ consecutive autocorrelations are insignificant||$\\hat m$: primul lag după care $K_T$ autocorelații consecutive sînt nesemnificative⟧'])))

frame('⟦Choosing the block length (2/2)||Alegerea lungimii blocului (2/2)⟧', items(
    ('⟦The same structure as the Andrews bandwidth||Aceeași structură ca lățimea Andrews⟧',
     ['⟦bias term $G$ over variance term $D$, rate $T^{1/3}$: persistent series get longer blocks||termenul de deplasare $G$ raportat la termenul de varianță $D$, rata $T^{1/3}$: seriile persistente primesc blocuri mai lungi⟧']),
    ('⟦Implemented in the Python package \\texttt{arch} (\\texttt{optimal\\_block\\_length})||Implementat în pachetul Python \\texttt{arch} (\\texttt{optimal\\_block\\_length})⟧',
     ['⟦our code gives the same block lengths||codul nostru dă aceleași lungimi ale blocurilor⟧']),
    ('⟦Our data||Datele noastre⟧',
     ['⟦about @{bo.bsb} days for squared S\\&P 500 returns, @{bl.inf.b} months for inflation||aproximativ @{bo.bsb} zile pentru pătratele randamentelor S\\&P 500, @{bl.inf.b} luni pentru inflație⟧',
      '⟦@{bl.gdp.b} for GDP growth, i.e.\\ the i.i.d.\\ bootstrap||@{bl.gdp.b} pentru creșterea PIB, adică bootstrap-ul i.i.d.⟧'])))

frame('⟦The wild bootstrap and its limits (1/2)||Wild bootstrap și limitele lui (1/2)⟧', items(
    ('⟦\\textbf{Wild bootstrap} \\refWu, \\refLiu, \\refMammen: each residual is multiplied by a random sign-like weight||\\textbf{Wild bootstrap} \\refWu, \\refLiu, \\refMammen: fiecare reziduu este înmulțit cu o pondere aleatoare de tip semn⟧',
     ['$y_t^* = x_t\'\\hat\\beta + \\hat u_t\\eta_t$, $\\quad \\eta_t$ ⟦i.i.d., $E\\eta_t = 0$, $E\\eta_t^2 = 1$||i.i.d., $E\\eta_t = 0$, $E\\eta_t^2 = 1$⟧',
      '⟦$y_t^*$: the bootstrap observation; $\\eta_t$: Rademacher ($\\pm 1$ with probability $1/2$ each) or the Mammen two-point distribution||$y_t^*$: observația bootstrap; $\\eta_t$: Rademacher ($\\pm 1$, fiecare cu probabilitatea $1/2$) sau distribuția în două puncte a lui Mammen⟧']),
    ('⟦It keeps the heteroskedasticity of each $\\hat u_t$ and destroys every autocorrelation||Păstrează heteroscedasticitatea fiecărui $\\hat u_t$ și distruge orice autocorelație⟧',
     ['⟦valid when the scores are an MDS: AR models with GARCH-type errors \\refGK||valid cînd scorurile sînt o MDS: modele AR cu erori de tip GARCH \\refGK⟧',
      '⟦\\textbf{not} valid for overlapping forecasts, local projections or the mean of squared returns||\\textbf{nu} este valid pentru prognoze suprapuse, proiecții locale sau media pătratelor randamentelor⟧'])))

frame('⟦The wild bootstrap and its limits (2/2)||Wild bootstrap și limitele lui (2/2)⟧', items(
    ('⟦Dependent wild bootstrap \\refShao: $\\eta_t$ drawn from a stationary process||Dependent wild bootstrap \\refShao: $\\eta_t$ extrase dintr-un proces staționar⟧',
     ['⟦$\\Corr(\\eta_t, \\eta_s) = a(|t-s|/l)$, with $a(\\cdot)$ a kernel and $l$ a bandwidth||$\\Corr(\\eta_t, \\eta_s) = a(|t-s|/l)$, cu $a(\\cdot)$ un nucleu și $l$ o lățime de bandă⟧',
      '⟦wild in form, block-like in effect: neighbouring residuals keep their joint signs||wild ca formă, de tip bloc ca efect: reziduurile apropiate își păstrează semnele comune⟧']),
    ('⟦Sieve bootstrap \\refBuhlmann: fit an AR$(p)$ with $p \\to \\infty$, resample its residuals||Sieve bootstrap \\refBuhlmann: estimăm un AR$(p)$ cu $p \\to \\infty$ și reeșantionăm reziduurile⟧',
     ['⟦efficient for linear processes, fragile for nonlinear ones||eficient pentru procesele liniare, fragil pentru cele neliniare⟧'])))

chart('⟦Three bootstraps of one mean||Trei bootstrap-uri ale aceleiași medii⟧', 'ats_ch0_bootstrap', 'ATS_ch0_block_bootstrap', [
    '⟦Mean of squared daily S\\&P 500 returns ($@{bo.mean}$, $T = @{t.sq.T}$); 1999 resamples each; block lengths from Politis--White||Media pătratelor randamentelor zilnice S\\&P 500 ($@{bo.mean}$, $T = @{t.sq.T}$); cîte 1999 de reeșantionări; lungimile blocurilor Politis--White⟧'],
    h='0.56\\textheight')

interp('the three bootstraps', 'celor trei bootstrap-uri', [
    ('⟦i.i.d.\\ bootstrap: standard error $@{bo.se_iid}$, equal to the naive $@{bo.se_naive}$, as theory says||Bootstrap i.i.d.: eroare standard $@{bo.se_iid}$, egală cu cea naivă, $@{bo.se_naive}$, cum spune teoria⟧',
     ['⟦Block bootstraps: MBB $@{bo.se_mbb}$, CBB $@{bo.se_cbb}$, stationary $@{bo.se_sb}$: about @{bo.rsb} times the naive value||Bootstrap-urile pe blocuri: MBB $@{bo.se_mbb}$, CBB $@{bo.se_cbb}$, staționar $@{bo.se_sb}$: de aproximativ @{bo.rsb} ori valoarea naivă⟧']),
    ('⟦HAC with the Andrews bandwidth: $@{bo.se_and}$ (about @{bo.rand} times the naive value): smaller than the block bootstraps||HAC cu lățimea Andrews: $@{bo.se_and}$ (de aproximativ @{bo.rand} ori valoarea naivă): mai mică decît la bootstrap-urile pe blocuri⟧',
     ['⟦Block length @{bo.bsb} against an Andrews bandwidth of @{bw.sq.Sa}: two plug-in rules, two different views of the same slowly decaying ACF||Lungimea blocului @{bo.bsb} față de lățimea Andrews de @{bw.sq.Sa}: două reguli plug-in, două imagini diferite ale aceleiași ACF care scade lent⟧']),
    '⟦When two valid methods disagree by a factor of two, report both and explain why: here, the volatility of volatility has long memory||Cînd două metode valide diferă de două ori, raportați-le pe amîndouă și explicați diferența: aici, volatilitatea volatilității are memorie lungă⟧'])

chart('⟦Bootstrap standard error against the block length||Eroarea standard bootstrap în funcție de lungimea blocului⟧', 'ats_ch0_block_length', 'ATS_ch0_block_bootstrap', [
    '⟦Circular block bootstrap, 999 resamples per length; ratio to the naive standard error||Bootstrap circular pe blocuri, 999 de reeșantionări pentru fiecare lungime; raportul față de eroarea standard naivă⟧'],
    h='0.55\\textheight')

interp('the block-length paths', 'traiectoriilor în funcție de lungimea blocului', [
    ('⟦$l = 1$ is the i.i.d.\\ bootstrap (ratio 1); the ratio grows with $l$ while $l$ is shorter than the memory of the series||$l = 1$ este bootstrap-ul i.i.d.\\ (raport 1); raportul crește odată cu $l$ cît timp $l$ este mai scurt decît memoria seriei⟧',
     ['⟦Inflation: ratio @{bl.inf.r} at the Politis--White length of @{bl.inf.b} months||Inflația: raportul @{bl.inf.r} la lungimea Politis--White de @{bl.inf.b} luni⟧']),
    '⟦GDP growth: flat near 1 (and slightly below for long blocks): no dependence to capture||Creșterea PIB: aproape constant în jurul lui 1 (și puțin sub 1 pentru blocuri lungi): nu există dependență de captat⟧',
    '⟦Very long blocks: few distinct blocks, noisy and downward-biased variance (the bias of $\\hat\\gamma_j$ at large lags)||Blocuri foarte lungi: puține blocuri distincte, varianță zgomotoasă și deplasată în jos (deplasarea lui $\\hat\\gamma_j$ la laguri mari)⟧',
    '⟦What do you think? Why does the inflation curve keep rising until $l$ is about a quarter of the sample?||Ce credeți? De ce curba inflației continuă să crească pînă cînd $l$ ajunge la aproximativ un sfert din eșantion?⟧'])

ROWS = (('sp', 'S\\&P 500 ⟦returns||randamente⟧'), ('sq', 'S\\&P 500 ⟦squared||pătrate⟧'), ('bet', '⟦BET returns||randamente BET⟧'),
        ('eur', 'EUR/RON'), ('gdp', '⟦RO GDP growth||Creșterea PIB RO⟧'), ('infl', '⟦RO inflation||Inflația RO⟧'))
D.frame('⟦Means of six series: standard errors by method||Mediile a șase serii: erori standard pe metode⟧', table(
    'lrrrrrrr', '⟦Series||Seria⟧ & $T$ & ⟦Mean||Media⟧ & $\\hat\\rho_1$ & ⟦naive||naivă⟧ & NW-A & ⟦stat.\\ boot.||boot.\\ staț.⟧ & $t_{naive}$ / $t_{EWC}$', [
        f'{lab} & @{{t.{k}.T}} & @{{t.{k}.mean}} & @{{t.{k}.rho}} & @{{t.{k}.se_naive}} & @{{t.{k}.se_andrews}} & @{{t.{k}.se_sb}} & @{{t.{k}.t_naive}} / @{{t.{k}.t_ewc}}'
        for k, lab in ROWS], 'footnotesize') +
    items('⟦NW-A: Newey--West with the Andrews bandwidth; stationary bootstrap with the Politis--White mean block; returns and changes in \\% per day, GDP in \\% per quarter, inflation in \\%||NW-A: Newey--West cu lățimea Andrews; bootstrap staționar cu blocul mediu Politis--White; randamentele și variațiile în \\% pe zi, PIB-ul în \\% pe trimestru, inflația în \\%⟧'),
    'footnotesize')

interp('the table', 'tabelului', [
    ('⟦S\\&P 500: $t$ rises from $@{t.sp.t_naive}$ (naive) to $@{t.sp.t_llsw}$ (fixed-$b$, critical value $@{t.sp.cv}$) and $@{t.sp.t_ewc}$ (EWC): the mean return ($@{t.sp.ann}\\%$ a year) becomes borderline significant||S\\&P 500: $t$ crește de la $@{t.sp.t_naive}$ (naiv) la $@{t.sp.t_llsw}$ (fixed-$b$, valoarea critică $@{t.sp.cv}$) și $@{t.sp.t_ewc}$ (EWC): randamentul mediu ($@{t.sp.ann}\\%$ pe an) devine semnificativ la limită⟧',
     ['⟦Negative autocorrelation shrinks the standard error: robust inference is not always more conservative||Autocorelația negativă reduce eroarea standard: inferența robustă nu este întotdeauna mai conservatoare⟧']),
    '⟦EUR/RON: mean depreciation of the leu not significant at 5\\% by any method ($t$ between $@{t.eur.t_ewc}$ and $@{t.eur.t_naive}$)||EUR/RON: deprecierea medie a leului nu este semnificativă la 5\\% prin nicio metodă ($t$ între $@{t.eur.t_ewc}$ și $@{t.eur.t_naive}$)⟧',
    '⟦Inflation: $t$ falls from $@{t.infl.t_naive}$ to $@{t.infl.t_ewc}$ for $H_0: \\mu = 0$; standard errors grow by a factor of about 4--5||Inflația: $t$ scade de la $@{t.infl.t_naive}$ la $@{t.infl.t_ewc}$ pentru $H_0: \\mu = 0$; erorile standard cresc de aproximativ 4--5 ori⟧',
    '⟦GDP growth: all methods agree; the question there is the two crisis quarters, not the dependence (Seminar 0, B2)||Creșterea PIB: toate metodele sînt de acord; problema acolo sînt cele două trimestre de criză, nu dependența (Seminarul 0, B2)⟧'], 'footnotesize')

D.recap(('the bootstrap for dependent data', 'bootstrap pentru date dependente'), [
    '⟦The i.i.d.\\ bootstrap reproduces the naive standard error; resample blocks instead||Bootstrap-ul i.i.d.\\ reproduce eroarea standard naivă; reeșantionați în schimb blocuri⟧',
    '⟦MBB (Künsch 1989) is a Bartlett HAC estimator in disguise; CBB removes the edge bias; the stationary bootstrap keeps stationarity||MBB (Künsch 1989) este, în esență, un estimator HAC Bartlett; CBB elimină deplasarea de capăt; bootstrap-ul staționar păstrează staționaritatea⟧',
    '⟦Block length $\\propto T^{1/3}$, chosen by Politis--White; the wild bootstrap handles heteroskedasticity only||Lungimea blocului $\\propto T^{1/3}$, aleasă prin Politis--White; wild bootstrap-ul tratează doar heteroscedasticitatea⟧'])

# ===============================================================================================================
D.section('Overlapping observations: the term spread and growth', 'Observații suprapuse: marja la termen și creșterea')
# ===============================================================================================================
frame('⟦Case study: Estrella and Hardouvelis (1991) (1/2)||Studiu de caz: Estrella și Hardouvelis (1991) (1/2)⟧', items(
    ('⟦\\refEH: does the slope of the yield curve predict US real growth?||\\refEH: prognozează panta curbei randamentelor creșterea reală din SUA?⟧',
     ['⟦regression of the average growth over the next $h$ quarters on the term spread||regresia creșterii medii pe următoarele $h$ trimestre pe marja la termen⟧',
      '$y_t^{(h)} = \\dfrac{400}{h}\\ln\\dfrac{\\mathrm{GDP}_{t+h}}{\\mathrm{GDP}_t} = \\beta_0 + \\beta_1 (i^{10y}_t - i^{3m}_t) + u_t$, $\\quad h = 4$']),
    ('⟦Notation||Notațiile⟧',
     ['⟦$y_t^{(h)}$: real GDP growth from quarter $t$ to $t + h$, annualised, in \\%; the factor $400/h$ turns a log change over $h$ quarters into \\% a year||$y_t^{(h)}$: creșterea PIB-ului real din trimestrul $t$ pînă în $t + h$, anualizată, în \\%; factorul $400/h$ transformă o variație logaritmică pe $h$ trimestre în \\% pe an⟧',
      '⟦$i^{10y}_t$, $i^{3m}_t$: the 10-year and 3-month Treasury yields; their difference is the term spread||$i^{10y}_t$, $i^{3m}_t$: randamentele titlurilor de stat la 10 ani și la 3 luni; diferența lor este marja la termen⟧',
      '⟦$\\beta_1 > 0$: a steeper curve announces faster growth; $u_t$: the forecast error||$\\beta_1 > 0$: o curbă mai abruptă anunță o creștere mai rapidă; $u_t$: eroarea de prognoză⟧'])))

frame('⟦Case study: Estrella and Hardouvelis (1991) (2/2)||Studiu de caz: Estrella și Hardouvelis (1991) (2/2)⟧', items(
    ('⟦Overlap: $y_t^{(4)}$ and $y_{t+1}^{(4)}$ share three quarters||Suprapunere: $y_t^{(4)}$ și $y_{t+1}^{(4)}$ au trei trimestre comune⟧',
     ['⟦so $u_t$ is at least MA(3) under $H_0$, even if quarterly shocks are independent||deci $u_t$ este cel puțin MA(3) sub $H_0$, chiar dacă șocurile trimestriale sînt independente⟧',
      '⟦classical remedy: \\refHH (truncated kernel, $h - 1$ lags) or Newey--West with $L = h - 1$||soluția clasică: \\refHH (nucleu trunchiat, $h - 1$ laguri) sau Newey--West cu $L = h - 1$⟧']),
    ('⟦Our data: FRED real GDP, 10-year and 3-month Treasury yields (quarterly averages)||Datele noastre: PIB real, randamentele titlurilor de stat la 10 ani și la 3 luni (medii trimestriale) din FRED⟧',
     ['@{ts.first} -- @{ts.last}, $T = @{ts.T}$']),
    '⟦Same design for local projections (Chapter 3) and for long-horizon return regressions (MFM)||Același plan pentru proiecțiile locale (Capitolul 3) și pentru regresiile randamentelor pe orizonturi lungi (MFM)⟧'))

chart('⟦The spread and future growth||Marja la termen și creșterea viitoare⟧', 'ats_ch0_term_spread', 'ATS_ch0_term_spread', [
    '⟦Left: the two series; right: ACF of the OLS residuals, $\\hat\\rho_1 = @{ts.rho1}$, $\\hat\\rho_3 = @{ts.rho3}$, $\\hat\\rho_4 = @{ts.rho4}$||Stînga: cele două serii; dreapta: ACF a reziduurilor MCMMP, $\\hat\\rho_1 = @{ts.rho1}$, $\\hat\\rho_3 = @{ts.rho3}$, $\\hat\\rho_4 = @{ts.rho4}$⟧'],
    h='0.55\\textheight')

D.frame('⟦One slope, five standard errors||O pantă, cinci erori standard⟧', table(
    'lrrr', '⟦Standard error||Eroarea standard⟧ & $\\widehat{se}(\\hat\\beta_1)$ & $t$ & ⟦Critical value||Valoarea critică⟧', [
        '⟦Classical OLS||MCMMP clasic⟧ & @{ts.se_classic} & @{ts.t_classic} & 1.96',
        '⟦White (heteroskedasticity only)||White (doar heteroscedasticitate)⟧ & @{ts.se_white} & -- & 1.96',
        '⟦Hansen--Hodrick, 3 lags||Hansen--Hodrick, 3 laguri⟧ & @{ts.se_hh} & -- & 1.96',
        '⟦Newey--West, 3 lags||Newey--West, 3 laguri⟧ & @{ts.se_nw} & @{ts.t_nw} & 1.96',
        '⟦NW, Andrews ($S = @{ts.Sa}$)||NW, Andrews ($S = @{ts.Sa}$)⟧ & @{ts.se_and} & @{ts.t_and} & 1.96',
        '⟦NW, $S = 1.3\\sqrt{T} = @{ts.Sl}$, fixed-$b$||NW, $S = 1.3\\sqrt{T} = @{ts.Sl}$, fixed-$b$⟧ & @{ts.se_ll} & @{ts.t_ll} & @{ts.cv_ll}'], 'footnotesize') +
    items('⟦$\\hat\\beta_1 = @{ts.b1}$ pp of annual growth per pp of spread, $R^2 = @{ts.r2}$||$\\hat\\beta_1 = @{ts.b1}$ pp de creștere anuală la fiecare pp de marjă, $R^2 = @{ts.r2}$⟧'), 'footnotesize')

interp('the term-spread regression', 'regresiei marjei la termen', [
    ('⟦The residuals are more persistent than the MA(3) implied by overlap ($\\hat\\rho_4 = @{ts.rho4}$): 3 lags are not enough||Reziduurile sînt mai persistente decît MA(3) implicat de suprapunere ($\\hat\\rho_4 = @{ts.rho4}$): 3 laguri nu sînt suficiente⟧',
     ['⟦The standard error doubles from classical OLS to fixed-$b$: $t$ from $@{ts.t_classic}$ to $@{ts.t_ll}$, just below the critical value $@{ts.cv_ll}$||Eroarea standard se dublează de la MCMMP clasic la fixed-$b$: $t$ scade de la $@{ts.t_classic}$ la $@{ts.t_ll}$, puțin sub valoarea critică $@{ts.cv_ll}$⟧']),
    ('⟦Subsamples (NW, 3 lags): 1962--1988 $\\hat\\beta_1 = @{ts.early.b}$ ($t = @{ts.early.t}$); 1989--2025 $\\hat\\beta_1 = @{ts.late.b}$ ($t = @{ts.late.t}$)||Subeșantioane (NW, 3 laguri): 1962--1988 $\\hat\\beta_1 = @{ts.early.b}$ ($t = @{ts.early.t}$); 1989--2025 $\\hat\\beta_1 = @{ts.late.b}$ ($t = @{ts.late.t}$)⟧',
     ['⟦The predictive power of the spread weakened after the original sample: a break question (Chapter 2) and an out-of-sample question (Chapter 1)||Puterea predictivă a marjei a scăzut după eșantionul original: o problemă de rupturi (Capitolul 2) și o problemă de evaluare în afara eșantionului (Capitolul 1)⟧']),
    '⟦Robust inference first, then stability: a full-sample $t$ of $@{ts.t_classic}$ hides both problems||Întîi inferența robustă, apoi stabilitatea: un $t$ de $@{ts.t_classic}$ pe întregul eșantion ascunde ambele probleme⟧'], 'footnotesize')

# ===============================================================================================================
D.section('Multiple testing in forecasting research', 'Testarea multiplă în cercetarea privind prognoza')
# ===============================================================================================================
frame('⟦Data snooping||Data snooping⟧', items(
    ('⟦\\textbf{Data snooping}: reusing one data set to select a model, a rule or a specification, then testing it on the same data as if it were chosen in advance||\\textbf{Data snooping}: refolosirea aceluiași set de date pentru a alege un model, o regulă sau o specificație, testat apoi pe aceleași date ca și cum ar fi fost ales dinainte⟧',
     ['⟦\\refLM: sorting portfolios on characteristics already known to be related to returns biases asset-pricing tests||\\refLM: sortarea portofoliilor după caracteristici despre care se știe deja că sînt legate de randamente deplasează testele de evaluare a activelor⟧',
      '⟦\\refHLZ: more than 300 published return factors; a new factor needs $t > 3$, not $t > 2$||\\refHLZ: peste 300 de factori de randament publicați; un factor nou are nevoie de $t > 3$, nu de $t > 2$⟧']),
    ('⟦Error rates for $K$ tests||Ratele de eroare pentru $K$ teste⟧',
     ['⟦FWER (family-wise error rate): probability of at least one false rejection among the $K$ tests at level $\\alpha$||FWER (rata de eroare la nivelul familiei de teste): probabilitatea a cel puțin unei respingeri false printre cele $K$ teste la nivelul $\\alpha$⟧',
      '⟦Bonferroni tests each hypothesis at $\\alpha/K$; Holm (step-down) relaxes the threshold step by step; both control the FWER||Bonferroni testează fiecare ipoteză la $\\alpha/K$; Holm (descendent, pas cu pas) relaxează pragul treptat; ambele controlează FWER⟧',
      '⟦FDR (false discovery rate): expected share of false rejections among rejections, controlled by \\refBH||FDR (false discovery rate): proporția așteptată a respingerilor false printre respingeri, controlată de \\refBH⟧']),
    ('⟦In forecasting: many models, many horizons, many samples||În prognoză: multe modele, multe orizonturi, multe eșantioane⟧',
     ['⟦the honest $p$-value is the one of the \\emph{search}, not of the winner||p-value-ul corect este cel al \\emph{căutării}, nu cel al modelului cîștigător⟧'])), 'footnotesize')

chart('⟦The best of $K$ tests||Cel mai bun dintre $K$ teste⟧', 'ats_ch0_snooping', 'ATS_ch0_data_snooping', [
    '⟦Probability that the largest $|t|$ of $K$ tests exceeds 1.96 when all nulls are true: independent and equicorrelated statistics (20\\,000 simulations)||Probabilitatea ca cel mai mare $|t|$ din $K$ teste să depășească 1,96 cînd toate ipotezele nule sînt adevărate: statistici independente și echicorelate (20\\,000 de simulări)⟧'],
    h='0.55\\textheight')

interp('the family-wise error', 'erorii la nivelul familiei de teste', [
    ('⟦Independent tests: FWER $@{sn.i20}\\%$ with $K = 20$ and $@{sn.i100}\\%$ with $K = 100$||Teste independente: FWER $@{sn.i20}\\%$ cu $K = 20$ și $@{sn.i100}\\%$ cu $K = 100$⟧',
     ['⟦Bonferroni would test each at $0.05/20 = 0.0025$||Bonferroni ar testa fiecare ipoteză la $0,05/20 = 0,0025$⟧']),
    ('⟦Correlated statistics (similar rules, overlapping samples): FWER $@{sn.c20}\\%$ ($K = 20$) and $@{sn.c100}\\%$ ($K = 100$) at correlation 0.5; $@{sn.h100}\\%$ at 0.9||Statistici corelate (reguli asemănătoare, eșantioane suprapuse): FWER $@{sn.c20}\\%$ ($K = 20$) și $@{sn.c100}\\%$ ($K = 100$) la corelația 0,5; $@{sn.h100}\\%$ la 0,9⟧',
     ['⟦Bonferroni ignores the correlation and is conservative: the bootstrap of the maximum (next slide) uses it||Bonferroni ignoră corelația și este conservator: bootstrap-ul maximului (slide-ul următor) o folosește⟧']),
    '⟦What do you think? With 50 moving-average rules, how many ``significant\'\' rules do you expect by chance at 5\\%?||Ce credeți? Cu 50 de reguli de medie mobilă, cîte reguli „semnificative” vă așteptați să obțineți din întîmplare la 5\\%?⟧'])

frame('⟦Case study: the Reality Check of White (2000) (1/2)||Studiu de caz: testul Reality Check, White (2000) (1/2)⟧', items(
    ('⟦$K$ models against a benchmark, evaluated on $n$ periods \\refWhite||$K$ modele comparate cu un reper, evaluate pe $n$ perioade \\refWhite⟧',
     ['⟦$f_{k,t}$: the performance difference of model $k$ at $t$ (e.g.\\ return of rule $k$ minus buy-and-hold); $\\bar f_k$: its mean over the $n$ periods||$f_{k,t}$: diferența de performanță a modelului $k$ la momentul $t$ (de exemplu randamentul regulii $k$ minus buy-and-hold); $\\bar f_k$: media ei pe cele $n$ perioade⟧']),
    ('⟦Hypothesis and statistic||Ipoteza și statistica⟧',
     ['$H_0: \\max_k E f_{k,t} \\le 0$ ⟦(no model beats the benchmark)||(niciun model nu bate reperul)⟧; $\\quad \\bar V = \\max_k \\sqrt{n}\\,\\bar f_k$',
      '⟦$\\bar V$: the scaled average outperformance of the best model; a large $\\bar V$ is evidence against $H_0$||$\\bar V$: avantajul mediu, scalat, al celui mai bun model; o valoare $\\bar V$ mare este o dovadă împotriva lui $H_0$⟧'])))

frame('⟦Case study: the Reality Check of White (2000) (2/2)||Studiu de caz: testul Reality Check, White (2000) (2/2)⟧', items(
    ('⟦Null distribution by the stationary bootstrap of the whole vector $f_t$ (keeps the correlation across rules and over time):||Distribuția sub $H_0$ prin bootstrap-ul staționar al întregului vector $f_t$ (păstrează corelația dintre reguli și în timp):⟧',
     ['$\\bar V^*_b = \\max_k \\sqrt{n}\\,(\\bar f^*_{k,b} - \\bar f_k)$, $\\quad p = B^{-1}\\sum_b \\mathbf{1}\\{\\bar V^*_b > \\bar V\\}$',
      '⟦$b = 1, \\dots, B$: the resamples; $\\bar f^*_{k,b}$: the mean of rule $k$ in resample $b$; $\\mathbf{1}\\{\\cdot\\}$: 1 if the condition holds, 0 otherwise||$b = 1, \\dots, B$: reeșantionările; $\\bar f^*_{k,b}$: media regulii $k$ în reeșantionarea $b$; $\\mathbf{1}\\{\\cdot\\}$: 1 dacă este îndeplinită condiția, 0 altfel⟧',
      '⟦$p$: the share of resamples with a larger maximum than the observed one, i.e.\\ a $p$-value for the whole search||$p$: proporția reeșantionărilor cu un maxim mai mare decît cel observat, adică un p-value pentru întreaga căutare⟧']),
    '⟦\\refSTW apply it to 7846 technical rules on the Dow Jones; \\refHansen (SPA) and \\refRW (StepM) refine it: Chapter 1||\\refSTW îl aplică pentru 7846 de reguli tehnice pe Dow Jones; \\refHansen (SPA) și \\refRW (StepM) îl rafinează: Capitolul 1⟧',
    ('⟦Our application: 50 rules ``long if the close is above its $n$-day moving average\'\', $n = 5, 10, \\dots, 250$, on the BET||Aplicația noastră: 50 de reguli „poziție lungă dacă închiderea este peste media mobilă pe $n$ zile”, $n = 5, 10, \\dots, 250$, pe BET⟧',
     ['⟦against buy-and-hold, no costs; mean block of 10 days||comparate cu buy-and-hold, fără costuri; bloc mediu de 10 zile⟧'])))

chart('⟦The Reality Check on the BET||Testul Reality Check pe BET⟧', 'ats_ch0_reality_check', 'ATS_ch0_data_snooping', [
    '⟦Bootstrap distribution of $\\bar V^*$ under $H_0$ (999 stationary-bootstrap resamples) and the observed $\\bar V$; two subsamples||Distribuția bootstrap a lui $\\bar V^*$ sub $H_0$ (999 de reeșantionări prin bootstrap staționar) și valoarea observată $\\bar V$; două subeșantioane⟧'],
    h='0.55\\textheight')

interp('the Reality Check', 'testului Reality Check', [
    ('⟦2001--2012 ($n = @{rc.e.N}$ days): the best rule MA(@{rc.e.n}) beats buy-and-hold by $@{rc.e.m}\\%$ a day, $t = @{rc.e.t}$, naive one-sided $p = @{rc.e.p}$||2001--2012 ($n = @{rc.e.N}$ zile): cea mai bună regulă, MA(@{rc.e.n}), bate buy-and-hold cu $@{rc.e.m}\\%$ pe zi, $t = @{rc.e.t}$, p-value naiv unilateral $= @{rc.e.p}$⟧',
     ['⟦Reality Check $p = @{rc.e.prc}$: not significant at 5\\% once the search over 50 rules is accounted for||p-value Reality Check $= @{rc.e.prc}$: nesemnificativ la 5\\% după ce se ține seama de căutarea printre 50 de reguli⟧']),
    '⟦2014--2026: the same rule, $t = @{rc.l.t}$, Reality Check $p = @{rc.l.prc}$: whatever existed did not survive||2014--2026: aceeași regulă, $t = @{rc.l.t}$, p-value Reality Check $= @{rc.l.prc}$: avantajul, dacă a existat, a dispărut⟧',
    ('⟦The short-MA winner fits the positive $\\hat\\rho_1$ of BET returns (stale prices)||Regula cîștigătoare, cu medie mobilă scurtă, exploatează $\\hat\\rho_1$ pozitiv al randamentelor BET (prețuri stale, neactualizate)⟧',
     ['⟦transaction costs would eat the gain||costurile de tranzacționare ar anula cîștigul⟧']),
    '⟦Pre-register the rule universe and the sample split before looking at the results (Stage 1 of the project)||Preînregistrați universul de reguli și împărțirea eșantionului înainte de a vedea rezultatele (Etapa 1 a proiectului)⟧'], 'footnotesize')

D.recap(('multiple testing', 'testarea multiplă'), [
    '⟦The $p$-value of the best of $K$ is not the $p$-value of a pre-specified test||P-value-ul celui mai bun dintre $K$ teste nu este p-value-ul unui test specificat dinainte⟧',
    '⟦FWER (Bonferroni, Holm) or FDR (Benjamini--Hochberg); for correlated forecasts: bootstrap the maximum (Reality Check)||FWER (Bonferroni, Holm) sau FDR (Benjamini--Hochberg); pentru prognoze corelate: bootstrap pentru maxim (Reality Check)⟧',
    '⟦Forecast comparison tests (Diebold--Mariano, SPA, Model Confidence Set) are the subject of Chapter 1||Testele de comparare a prognozelor (Diebold--Mariano, SPA, Model Confidence Set) sînt subiectul Capitolului 1⟧'])

# ===============================================================================================================
D.section('Reproducible research practice', 'Practica cercetării reproductibile')
# ===============================================================================================================
frame('⟦Seeds and Monte Carlo experiments||Semințe și experimente Monte Carlo⟧', items(
    ('⟦One seed per project, set once: \\texttt{rng = np.random.default\\_rng(2026)}; pass \\texttt{rng} to every function||O singură sămînță pe proiect, fixată o dată: \\texttt{rng = np.random.default\\_rng(2026)}; transmiteți \\texttt{rng} fiecărei funcții⟧',
     ['⟦Parallel runs: \\texttt{np.random.SeedSequence(2026).spawn(k)} gives independent streams; never reuse a global state||Rulări paralele: \\texttt{np.random.SeedSequence(2026).spawn(k)} dă fluxuri independente; nu refolosiți niciodată o stare globală⟧']),
    ('⟦Report what makes a simulation checkable||Raportați ce face o simulare verificabilă⟧',
     ['⟦DGP, $T$, number of replications $R$, burn-in, seed, Monte Carlo standard error $\\sqrt{p(1-p)/R}$||DGP, $T$, numărul de replicări $R$, valorile inițiale eliminate, sămînța, eroarea standard Monte Carlo $\\sqrt{p(1-p)/R}$⟧',
      '⟦Results must not depend on the seed beyond the Monte Carlo error: rerun with a second seed||Rezultatele nu trebuie să depindă de sămînță peste eroarea Monte Carlo: rulați din nou cu o a doua sămînță⟧']),
    '⟦Every chart and every number of this chapter is produced by one script with seed 2026 (Quantlets/Ch\\_00)||Fiecare grafic și fiecare cifră din acest capitol sînt produse de un singur script cu sămînța 2026 (Quantlets/Ch\\_00)⟧'))

frame('⟦Versioned data||Date versionate⟧', items(
    ('⟦Macro data are revised: the GDP you download today is not the GDP a forecaster saw in real time||Datele macro sînt revizuite: PIB-ul descărcat azi nu este PIB-ul pe care l-a văzut un prognozator în timp real⟧',
     ['⟦Real-time vintages: \\refCS (Philadelphia Fed), ALFRED for FRED series; Eurostat revises national accounts every quarter||Vintage-uri în timp real: \\refCS (Fed Philadelphia), ALFRED pentru seriile FRED; Eurostat revizuiește conturile naționale în fiecare trimestru⟧']),
    ('⟦Save a dated snapshot of every series used, with the query that produced it||Salvați un instantaneu datat al fiecărei serii folosite, împreună cu interogarea care l-a produs⟧',
     ['⟦Record the download date, the dataset code (e.g.\\ \\texttt{namq\\_10\\_gdp}) and a checksum (\\texttt{sha256}) of the file||Notați data descărcării, codul setului de date (de exemplu \\texttt{namq\\_10\\_gdp}) și o sumă de control (\\texttt{sha256}) a fișierului⟧',
      '⟦The course market data are saved once and end on @{d.last.en}: every student gets the same numbers||Datele de piață ale cursului sînt salvate o singură dată și se termină pe @{d.last.ro}: fiecare student obține aceleași cifre⟧']),
    '⟦A forecast evaluated on revised data answers a different question than the one asked in real time||O prognoză evaluată pe date revizuite răspunde la altă întrebare decît cea pusă în timp real⟧'))

frame('⟦Replication packages||Pachete de replicare⟧', items(
    ('⟦What economics journals now require \\refVilhuber, \\refCM||Cerințele actuale ale revistelor de economie \\refVilhuber, \\refCM⟧',
     ['⟦a README with a data availability statement, the order of the scripts and the expected run time||un README cu declarația de disponibilitate a datelor, ordinea scripturilor și timpul de rulare estimat⟧',
      '⟦code that regenerates every table and figure from raw data, without manual steps||cod care regenerează fiecare tabel și grafic din datele brute, fără pași manuali⟧',
      '⟦the computational environment: \\texttt{requirements.txt} with versions, or a Colab notebook||mediul de calcul: \\texttt{requirements.txt} cu versiuni sau un notebook Colab⟧']),
    ('⟦For the ATS project (Stage 2)||Pentru proiectul ATS (Etapa 2)⟧',
     ['⟦a GitHub repository: \\texttt{data/}, \\texttt{code/}, \\texttt{output/}, README, AI\\_USE.md, AI\\_ERRORS.md||un repository GitHub: \\texttt{data/}, \\texttt{code/}, \\texttt{output/}, README, AI\\_USE.md, AI\\_ERRORS.md⟧',
      '⟦one command or one notebook reproduces every number in the report||o singură comandă sau un singur notebook reproduce fiecare rezultat din raport⟧']),
    '⟦Test: a colleague clones the repository on a clean machine and gets the same numbers||Testul: un coleg clonează repository-ul pe un calculator curat și obține aceleași cifre⟧'))

frame('⟦Pre-registration and the analysis plan||Preînregistrarea și planul de analiză⟧', items(
    ('⟦Stage 1 of the project fixes, before any estimation:||Etapa 1 a proiectului fixează, înaintea oricărei estimări:⟧',
     ['⟦the hypothesis, the sample and its split (estimation, evaluation), the benchmark||ipoteza, eșantionul și împărțirea lui (estimare, evaluare), reperul⟧',
      '⟦the inference method (HAC rule, bootstrap, critical values) and the multiple-testing correction||metoda de inferență (regula HAC, bootstrap, valorile critice) și corecția pentru testarea multiplă⟧',
      '⟦the list of specifications that will be reported, all of them||lista specificațiilor care vor fi raportate, toate⟧']),
    ('⟦Why: the garden of forking paths turns many small choices into an implicit search||Motivul: multitudinea de alegeri mici transformă analiza într-o căutare implicită⟧',
     ['⟦Every deviation from the plan is allowed but reported, with its reason||Orice abatere de la plan este permisă, dar raportată, cu motivul ei⟧']),
    '⟦An AI assistant makes the search cheaper: AI\\_USE.md records the prompts that shaped a decision||Un asistent AI face căutarea mai ieftină: AI\\_USE.md consemnează prompturile care au influențat o decizie⟧'))

D.recap(('reproducible research', 'cercetarea reproductibilă'), [
    '⟦Seed once, pass the generator, report $R$ and the Monte Carlo error||Fixați sămînța o dată, transmiteți generatorul, raportați $R$ și eroarea Monte Carlo⟧',
    '⟦Dated, checksummed data snapshots; real-time vintages when the question is about real-time forecasting||Instantanee de date datate, cu sumă de control; vintage-uri în timp real cînd întrebarea privește prognoza în timp real⟧',
    '⟦A replication package that runs from raw data to every number; a plan fixed before the results||Un pachet de replicare care rulează de la datele brute pînă la fiecare cifră; un plan fixat înaintea rezultatelor⟧'])

# ===============================================================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')
# ===============================================================================================================
frame('⟦An open question: valid inference for a near-integrated mean||O întrebare deschisă: inferență validă pentru media unei serii aproape integrate⟧', items(
    ('⟦Has Romanian inflation averaged the BNR target since 2013? Formally, $H_0: \\mu = 2.5$ for the HICP annual rate, @{ai.T} months to @{ai.last.en}||A fost inflația din România, în medie, la nivelul țintei BNR din 2013? Formal, $H_0: \\mu = 2,5$ pentru rata anuală IAPC, @{ai.T} luni pînă în @{ai.last.ro}⟧',
     ['⟦$\\hat\\rho_1 = @{ai.phi}$: the series is close to a unit root, and overlapping by construction||$\\hat\\rho_1 = @{ai.phi}$: seria este aproape de o rădăcină unitară și suprapusă prin construcție⟧']),
    ('⟦Open: no kernel, EWC or bootstrap rule controls size at this persistence (Monte Carlo above)||Deschis: nicio regulă cu nucleu, EWC sau bootstrap nu controlează mărimea la această persistență (studiul Monte Carlo de mai sus)⟧',
     ['⟦\\refMuller and \\refLLS map the frontier; which test should a central-bank watcher use with 10--15 years of data?||\\refMuller și \\refLLS descriu frontiera; ce test ar trebui să folosească un analist al băncii centrale cu 10--15 ani de date?⟧']),
    '⟦A question with policy content (credibility of the target) and a methodological core (HAR inference at $\\phi \\approx 1$)||O întrebare cu conținut de politică economică (credibilitatea țintei) și un nucleu metodologic (inferență HAR la $\\phi \\approx 1$)⟧'))

frame('⟦The AI-assisted discovery loop||Bucla de descoperire asistată de AI⟧', items(
    ('⟦\\textbf{Literature}: \\aiprompt{"List peer-reviewed tests for the mean of a highly persistent series since 2010, with DOI and the Monte Carlo design."}||\\textbf{Literatura}: \\aiprompt{"Listează testele publicate pentru media unei serii foarte persistente, din 2010 încoace, cu DOI și planul Monte Carlo."}⟧',
     ['⟦Check: resolve every DOI on Crossref; read the size tables yourself (Semantic Scholar, Elicit for search)||Verificare: rezolvați fiecare DOI în Crossref; citiți personal tabelele de mărime (Semantic Scholar, Elicit pentru căutare)⟧']),
    ('⟦\\textbf{Hypothesis and code}: \\aiprompt{"Write Python for NW fixed-b and EWC tests of a mean, and a Monte Carlo of their size at phi = 0.98, T = 164."}||\\textbf{Ipoteză și cod}: \\aiprompt{"Scrie cod Python pentru testele NW fixed-b și EWC ale unei medii și un Monte Carlo al mărimii lor la phi = 0,98, T = 164."}⟧',
     ['⟦Check: reproduce a published size number first (e.g.\\ the LLSW tables), then change one thing at a time||Verificare: reproduceți întîi o mărime publicată (de exemplu tabelele LLSW), apoi modificați un singur element pe rînd⟧']),
    ('⟦\\textbf{Robustness and critique}: \\aiprompt{"Act as a hostile referee: why could this test of the inflation mean be misleading?"}||\\textbf{Robustețe și critică}: \\aiprompt{"Joacă rolul unui recenzent ostil: de ce ar putea acest test al mediei inflației să inducă în eroare?"}⟧',
     ['⟦Expect: breaks in the mean (2013, 2022), the CPI--HICP gap, overlap, the choice of start date||De așteptat: rupturi în medie (2013, 2022), diferența IPC--IAPC, suprapunerea, alegerea datei de început⟧']),
    '⟦\\textbf{The human checks}: formulas, timing of information (no look-ahead), every number against the code; the tools are generic (Claude, ChatGPT, Gemini, Copilot)||\\textbf{Verificările făcute de om}: formulele, momentul în care informația devine disponibilă (fără look-ahead), fiecare cifră pe cod; instrumentele sînt generice (Claude, ChatGPT, Gemini, Copilot)⟧'), 'footnotesize')

chart('⟦Mini-case: one hypothesis, six answers||Mini-studiu de caz: o ipoteză, șase răspunsuri⟧', 'ats_ch0_ai_minicase', 'ATS_ch0_ai_discovery', [
    '⟦Left: 95\\% intervals for the mean HICP inflation since 2013 (mean $@{ai.mean}\\%$); right: size of each test in a Monte Carlo with the fitted AR(1), $\\phi = @{ai.phi}$, $T = @{ai.T}$||Stînga: intervale de 95\\% pentru media inflației IAPC din 2013 (media $@{ai.mean}\\%$); dreapta: mărimea fiecărui test într-un Monte Carlo cu AR(1) estimat, $\\phi = @{ai.phi}$, $T = @{ai.T}$⟧'],
    h='0.52\\textheight')

interp('the mini-case', 'mini-studiului de caz', [
    ('⟦A typical assistant proposal: ``NW with $\\lfloor 4(T/100)^{2/9}\\rfloor$ lags\'\' gives $t = @{ai.t_nw}$ and rejects $\\mu = 2.5$||O propunere tipică a unui asistent AI: „NW cu $\\lfloor 4(T/100)^{2/9}\\rfloor$ laguri” dă $t = @{ai.t_nw}$ și respinge $\\mu = 2,5$⟧',
     ['⟦Its actual size at this persistence: $@{ai.mc.nw}\\%$ instead of 5\\%; the naive test: $@{ai.mc.naive}\\%$||Mărimea lui efectivă la această persistență: $@{ai.mc.nw}\\%$ în loc de 5\\%; testul naiv: $@{ai.mc.naive}\\%$⟧']),
    ('⟦NW-Andrews ($t = @{ai.t_andrews}$), fixed-$b$ ($t = @{ai.t_llsw}$, critical value $@{ai.cv_llsw}$) and EWC ($t = @{ai.t_ewc}$, $\\nu = @{ai.nu}$) do not reject||NW-Andrews ($t = @{ai.t_andrews}$), fixed-$b$ ($t = @{ai.t_llsw}$, valoarea critică $@{ai.cv_llsw}$) și EWC ($t = @{ai.t_ewc}$, $\\nu = @{ai.nu}$) nu resping⟧',
     ['⟦But their sizes are still $@{ai.mc.andrews}\\%$--$@{ai.mc.ewc}\\%$: a non-rejection is not evidence for the target either||Dar mărimile lor sînt tot $@{ai.mc.andrews}\\%$--$@{ai.mc.ewc}\\%$: nici nerespingerea nu este o dovadă în favoarea țintei⟧']),
    '⟦Honest conclusion: with 14 years of a near-integrated series the data cannot settle the question; that is the open part||Concluzia prudentă: cu 14 ani dintr-o serie aproape integrată, datele nu pot tranșa întrebarea; aceasta este partea deschisă⟧'], 'footnotesize')

frame('⟦Project idea||Idee de proiect⟧', items(
    ('⟦\\textbf{Question}: which HAR test is reliable for the mean of Romanian and euro-area inflation, 2005--2026?||\\textbf{Întrebarea}: ce test HAR este fiabil pentru media inflației din România și din zona euro, 2005--2026?⟧',
     ['⟦Replicate first: one size table of \\refLLSW (their AR(1) design); explain every gap||Replicați întîi: un tabel de mărime din \\refLLSW (planul lor AR(1)); explicați orice diferență⟧']),
    ('⟦\\textbf{Extension}||\\textbf{Extensia}⟧',
     ['⟦add the tests of \\refMuller; calibrate the Monte Carlo to HICP data of all EU countries (Eurostat)||adăugați testele din \\refMuller; calibrați studiul Monte Carlo pe datele IAPC ale tuturor țărilor UE (Eurostat)⟧',
      '⟦report size and power on one frontier per country; test the target hypothesis with the test that controls size||raportați mărimea și puterea pe o frontieră pentru fiecare țară; testați ipoteza țintei cu testul care controlează mărimea⟧']),
    '⟦\\textbf{Deliverables}: a dated pre-analysis plan; a replication package; AI\\_USE.md with the prompts that shaped decisions; AI\\_ERRORS.md with each invented reference or wrong number caught||\\textbf{Livrabile}: un plan de analiză datat; un pachet de replicare; AI\\_USE.md cu prompturile care au influențat decizii; AI\\_ERRORS.md cu fiecare referință inventată sau cifră greșită depistată⟧'), 'footnotesize')

# ===============================================================================================================
D.section('Conclusions', 'Concluzii')
# ===============================================================================================================
frame('⟦Key takeaways||Idei de reținut⟧', items(
    '⟦The precision of a mean or a slope is governed by the long-run variance $\\Omega = 2\\pi f(0)$, not by $\\gamma_0$||Precizia unei medii sau a unei pante este dată de varianța de termen lung $\\Omega = 2\\pi f(0)$, nu de $\\gamma_0$⟧',
    '⟦Ergodicity gives consistency; MDS or mixing structure gives the CLT; the HAC estimator gives the standard error||Ergodicitatea dă consistența; structura MDS sau mixing dă TLC; estimatorul HAC dă eroarea standard⟧',
    '⟦Kernel, bandwidth and critical values are one decision: NW with $1.3\\sqrt{T}$ and fixed-$b$, or EWC, by default||Nucleul, lățimea de bandă și valorile critice sînt o singură decizie: implicit, NW cu $1.3\\sqrt{T}$ și fixed-$b$ sau EWC⟧',
    '⟦Block bootstraps resample dependence; the wild bootstrap does not||Bootstrap-ul pe blocuri reeșantionează dependența; wild bootstrap-ul nu o face⟧',
    '⟦Near unit roots defeat all of them: measure the size of your test by Monte Carlo at your persistence||În prezența rădăcinilor aproape unitare toate aceste metode eșuează: măsurați mărimea testului prin Monte Carlo, la persistența datelor analizate⟧',
    '⟦Searches need search-adjusted $p$-values; projects need replication packages and a plan fixed in advance||Căutările cer p-value-uri ajustate pentru căutare; proiectele au nevoie de pachete de replicare și de un plan fixat dinainte⟧'))

frame('⟦Self-assessment||Autoevaluare⟧', items(
    '⟦What is the long-run variance of an MA(1) with $\\theta = -0.5$ and $\\sigma^2 = 1$?||Care este varianța de termen lung a unui MA(1) cu $\\theta = -0,5$ și $\\sigma^2 = 1$?⟧',
    '⟦Why can the truncated kernel give a negative variance while the Bartlett kernel cannot?||De ce poate nucleul trunchiat să dea o varianță negativă, iar nucleul Bartlett nu?⟧',
    '⟦Which standard error would you use for the mean of daily S\\&P 500 returns?||Ce eroare standard ați folosi pentru media randamentelor zilnice S\\&P 500?⟧',
    '⟦Which standard error would you use for the mean of their squares?||Ce eroare standard ați folosi pentru media pătratelor lor?⟧',
    '⟦Why is the wild bootstrap invalid for a regression with overlapping four-quarter growth?||De ce este wild bootstrap-ul invalid pentru o regresie cu creșteri pe patru trimestre suprapuse?⟧',
    '⟦You tried 40 specifications and report the best one: which $p$-value should you report?||Ați încercat 40 de specificații și o raportați pe cea mai bună: ce p-value ar trebui să raportați?⟧'))

frame('⟦Next chapter and further reading||Capitolul următor și lecturi suplimentare⟧', items(
    ('⟦\\textbf{Next}: Chapter 1, forecast evaluation, scoring rules and combination||\\textbf{Urmează}: Capitolul 1, evaluarea prognozelor, reguli de scor și combinarea prognozelor⟧',
     ['⟦Diebold--Mariano is a HAC $t$-test on loss differentials; SPA and the Model Confidence Set use the stationary bootstrap of this chapter||Diebold--Mariano este un test $t$ HAC pe diferențele de pierdere; SPA și Model Confidence Set folosesc bootstrap-ul staționar din acest capitol⟧']),
    ('⟦\\textbf{Further reading}||\\textbf{Lecturi suplimentare}⟧',
     ['⟦Theory: \\refHamilton (Ch.\\ 7 and 10), \\refBradley, \\refLahiri||Teorie: \\refHamilton (cap.\\ 7 și 10), \\refBradley, \\refLahiri⟧',
      '⟦Practice: \\refLLSW, \\refLLS, \\refMuller||Practică: \\refLLSW, \\refLLS, \\refMuller⟧',
      '⟦Snooping: \\refWhite, \\refHansen, \\refRW, \\refHLZ||Data snooping: \\refWhite, \\refHansen, \\refRW, \\refHLZ⟧']),
    ('⟦\\textbf{Code}||\\textbf{Cod}⟧',
     ['⟦Quantlets: \\href{https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_00}{github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch\\_00}||Quantlets: \\href{https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_00}{github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch\\_00}⟧',
      '⟦Python: \\texttt{statsmodels} (\\texttt{cov\\_type="HAC"}), \\texttt{arch.bootstrap} (\\texttt{StationaryBootstrap}, \\texttt{optimal\\_block\\_length}, \\texttt{SPA})||Python: \\texttt{statsmodels} (\\texttt{cov\\_type="HAC"}), \\texttt{arch.bootstrap} (\\texttt{StationaryBootstrap}, \\texttt{optimal\\_block\\_length}, \\texttt{SPA})⟧'])))

D.references(BIB, per=15)
D.write(V)
