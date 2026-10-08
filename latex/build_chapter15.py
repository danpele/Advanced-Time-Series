r"""
build_chapter15.py -- Capitolul 15 (Recapitulare și susținerea proiectelor), EN + RO dintr-o singură sursă
=========================================================================================================
Harta cursului, cîte un slide de recapitulare pentru fiecare capitol 0--14 și pentru capitolul de studiu individual 16
(idei-cheie, formula-cheie, rezultatul replicării, greșeli frecvente), trusa de metode, fluxul de cercetare al
proiectului, replicarea unei lucrări de referință (inclusiv replicările din curs care NU au reușit și motivele),
lista de verificare a reproductibilității, erorile frecvente (data snooping, scurgerea de informație, look-ahead,
afirmații exagerate, p-hacking), susținerea orală (format, întrebări, criterii individuale, răspunsuri-model),
AI în cercetare (AI_USE.md, AI_ERRORS.md) și secțiunea finală „AI în descoperirea științifică: alegerea proiectului”.
Cursul nu are examen scris: 70% proiect (5% propunere și preînregistrare, 15% replicare și extensie, 50% susținere
orală individuală), 20% quiz-uri, 10% prezență.
Cifre: recapitulările citesc fișierele de cifre ale capitolelor (ch15_common.facts, aceleași rotunjiri ca în
capitole); simulările noi vin din Quantlets/Ch_15/ch15_numbers.json (generate_all_charts.py).
Ieșire:
  EN/Courses/chapter15_review_project_defence.tex
  RO/Cursuri/capitol15_recapitulare_proiecte.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_15/generate_all_charts.py
  python3 latex/build_chapter15.py && python3 latex/ats_build.py compile 15
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import run_acronyms, Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch15_common import REFS, T, bib, facts, finalize, load, minus_fix   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
OK14 = facts(V)
P = V.put
D = Deck(15, 'lecture', refs=REFS)
C = 'https://commons.wikimedia.org/wiki/File:'
TB = '>{\\raggedright\\arraybackslash}'
QLB = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets'


def ql(folder, ch=15):
    return f'\\quantlet{{{folder.replace("_", chr(92) + "_")}}}{{{QLB}/Ch_{ch:02d}/{folder}}}'


def chart(title, fig, folder, bullets, h='0.56\\textheight', size='footnotesize', ch=15):
    body = (f'\\begin{{center}}\n\\includegraphics[width=0.97\\textwidth,height={h},keepaspectratio]{{{fig}.pdf}}\n'
            f'\\end{{center}}\n\\vspace{{-0.25cm}}\n' + items(*bullets) + '\n' + ql(folder, ch))
    D.frame(title, body, size)


def interp(title, bullets, size='small'):
    D.frame(T(f'Interpreting {title[0]}', f'Interpretarea {title[1]}'), items(*bullets), size)


FOTO = T('Photo', 'Foto')
PH = {
    'ase': ('ch0_ase_2014.jpg', C + 'Bucharest_-_Academie_de_Studii_Economice_01.jpg', FOTO + ': Joe Mabel (2014); CC BY 3.0; Wikimedia Commons'),
    'granger': ('ch1_granger_2008.jpg', C + 'Clive_Granger_by_Olaf_Storbeck.jpg', FOTO + ': Olaf Storbeck (2008); CC BY-SA 2.0; Wikimedia Commons'),
    'efron': ('ch0_efron_2007.jpg', C + 'Bradley_Efron_National_Medal_of_Science_2007_(cropped).jpg',
              FOTO + ': Ryan K. Morris, NSTMF (2007); ' + T('public domain', 'domeniu public') + '; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.58', wr='0.38'):
    return cols(left, right, wl, wr)


IDEA = T(r'\textbf{Key ideas}', r'\textbf{Idei-cheie}')
FORM = T(r'\textbf{Key formula}', r'\textbf{Formula-cheie}')
REPL = T(r'\textbf{Replication}', r'\textbf{Replicarea}')
MIST = T(r'\textbf{Common mistakes}', r'\textbf{Greșeli frecvente}')


# Notation of the key formula of each chapter (each symbol defined where the formula is recalled)
NOTA = {
    0: [T(r'$\gamma_j$: autocovariance at lag $j$; $f(0)$: spectral density at frequency zero; $\Omega$: long-run variance', r'$\gamma_j$: autocovarianța la lagul $j$; $f(0)$: densitatea spectrală la frecvența zero; $\Omega$: varianța de termen lung'),
        T(r'$\hat\Gamma_j$: sample autocovariance matrix at lag $j$; $L$: number of lags (bandwidth); $1 - j/(L + 1)$: Bartlett weights', r'$\hat\Gamma_j$: matricea de autocovarianță de selecție la lagul $j$; $L$: numărul de laguri (lățimea de bandă); $1 - j/(L + 1)$: ponderile Bartlett')],
    1: [T(r'$\bar d$: mean loss differential of the two forecasts; $\hat\Omega_d$: its long-run variance; $P$: number of out-of-sample forecasts; $h$: horizon', r'$\bar d$: diferența medie a pierderilor celor două prognoze; $\hat\Omega_d$: varianța ei de termen lung; $P$: numărul de prognoze în afara eșantionului; $h$: orizontul'),
        T(r'$\mathrm{DM}^*$: the HLN small-sample correction, compared with Student-$t$ with $P - 1$ degrees of freedom', r'$\mathrm{DM}^*$: corecția HLN pentru eșantioane mici, comparată cu Student-$t$ cu $P - 1$ grade de libertate')],
    2: [T(r'$W_T(\pi)$: Wald statistic for a break at the sample fraction $\pi$; $B_p$: a $p$-dimensional Brownian motion; $\Rightarrow$: convergence in distribution', r'$W_T(\pi)$: statistica Wald pentru o ruptură la fracțiunea $\pi$ a eșantionului; $B_p$: o mișcare browniană $p$-dimensională; $\Rightarrow$: convergență în distribuție'),
        T(r'TAR: $\phi_1$, $\phi_2$: coefficients of the two regimes; $x_t$: lagged regressors; $q_{t-d}$: threshold variable with delay $d$; $\gamma$: the threshold', r'TAR: $\phi_1$, $\phi_2$: coeficienții celor două regimuri; $x_t$: regresorii cu lag; $q_{t-d}$: variabila de prag cu lagul $d$; $\gamma$: pragul')],
    3: [T(r'$u_t$: reduced-form residuals; $\varepsilon_t$: structural shocks; $B_0$: impact matrix; $\Phi_h$: reduced-form responses; $\Theta_h$: structural responses at horizon $h$', r'$u_t$: reziduurile formei reduse; $\varepsilon_t$: șocurile structurale; $B_0$: matricea de impact; $\Phi_h$: răspunsurile formei reduse; $\Theta_h$: răspunsurile structurale la orizontul $h$'),
        T(r'proxy: $z_t$ instrument, $b_1$ first column of $B_0$, $\alpha$ relevance; LP: $\beta_h$ response at $h$ to $x_t$, $w_t$ controls, $\xi_{t+h}$ error', r'proxy: $z_t$ instrumentul, $b_1$ prima coloană a lui $B_0$, $\alpha$ relevanța; LP: $\beta_h$ răspunsul la $h$ față de $x_t$, $w_t$ controalele, $\xi_{t+h}$ eroarea')],
    4: [T(r'$\Delta$: first difference; $\beta$: cointegrating vectors; $\alpha$: adjustment coefficients; $\Gamma_i$: short-run matrices; $D_t$: deterministic terms with coefficients $\Phi$', r'$\Delta$: diferența de ordinul întîi; $\beta$: vectorii de cointegrare; $\alpha$: coeficienții de ajustare; $\Gamma_i$: matricele de termen scurt; $D_t$: termenii deterministi, cu coeficienții $\Phi$'),
        T(r'$LR_{tr}(r)$: trace statistic for rank at most $r$; $\hat\lambda_i$: ordered eigenvalues; $T$: sample size', r'$LR_{tr}(r)$: statistica urmei pentru rangul cel mult $r$; $\hat\lambda_i$: valorile proprii ordonate; $T$: mărimea eșantionului')],
    5: [T(r'$(A_l)_{ij}$: effect of variable $j$ at lag $l$ on variable $i$; the prior variance shrinks with $l^2$', r'$(A_l)_{ij}$: efectul variabilei $j$ cu lagul $l$ asupra variabilei $i$; varianța a priori scade cu $l^2$'),
        T(r'$\lambda$: overall tightness; $\vartheta$: extra tightness on other variables; $\sigma_i^2$: residual scale of variable $i$', r'$\lambda$: strîngerea generală; $\vartheta$: strîngerea suplimentară pentru celelalte variabile; $\sigma_i^2$: scala reziduală a variabilei $i$')],
    6: [T(r'$a_t$, $P_t$: predicted state and its variance; $v_t$, $F_t$: prediction error and its variance; $K_t$: Kalman gain', r'$a_t$, $P_t$: starea prezisă și varianța ei; $v_t$, $F_t$: eroarea de predicție și varianța ei; $K_t$: cîștigul Kalman'),
        T(r'$Z_t$: measurement matrix; $T_t$: transition matrix; $H_t$: measurement noise variance', r'$Z_t$: matricea de măsurare; $T_t$: matricea de tranziție; $H_t$: varianța zgomotului de măsurare')],
    7: [T(r'$\hat\xi_{t|t}$: filtered regime probabilities; $\eta_t$: densities of $y_t$ in each regime; $\odot$: elementwise product; $\mathbf 1$: vector of ones', r'$\hat\xi_{t|t}$: probabilitățile filtrate ale regimurilor; $\eta_t$: densitățile lui $y_t$ în fiecare regim; $\odot$: produsul element cu element; $\mathbf 1$: vectorul de unu'),
        T(r'$\mathbf P$: transition matrix; $p_{ii}$: probability of staying in regime $i$; $\E D_i$: expected duration of regime $i$', r'$\mathbf P$: matricea de tranziție; $p_{ii}$: probabilitatea de a rămîne în regimul $i$; $\E D_i$: durata așteptată a regimului $i$')],
    8: [T(r'$\mathrm{RV}_t$: realised variance; $\mathrm{RV}^{(w)}_t$, $\mathrm{RV}^{(m)}_t$: its averages over 5 and 22 days; $\mathrm{RQ}_t$: realised quarticity, which measures the error of $\mathrm{RV}_t$', r'$\mathrm{RV}_t$: varianța realizată; $\mathrm{RV}^{(w)}_t$, $\mathrm{RV}^{(m)}_t$: mediile ei pe 5 și 22 de zile; $\mathrm{RQ}_t$: cvarticitatea realizată, care măsoară eroarea lui $\mathrm{RV}_t$'),
        T(r'$\beta_{dQ} < 0$: the daily weight falls when $\mathrm{RV}_t$ is measured with a large error', r'$\beta_{dQ} < 0$: ponderea zilnică scade cînd $\mathrm{RV}_t$ este măsurat cu o eroare mare')],
    9: [T(r'$y$: realised return; $v$: VaR forecast and $e$: ES forecast, both as (negative) return quantities; $\alpha$: the level (e.g.\ 0.025)', r'$y$: randamentul realizat; $v$: prognoza VaR și $e$: prognoza ES, ambele ca randamente (negative); $\alpha$: nivelul (de exemplu 0,025)'),
        T(r'$L_{\mathrm{FZ0}}$: a consistent loss for the pair (VaR, ES), lower is better; $q_\alpha$: the $\alpha$-quantile of the return', r'$L_{\mathrm{FZ0}}$: o pierdere consistentă pentru perechea (VaR, ES), o valoare mai mică este mai bună; $q_\alpha$: cuantila de nivel $\alpha$ a randamentului')],
    10: [T(r'$f(\lambda)$: spectral density at frequency $\lambda$; $\gamma(k)$: autocovariance at lag $k$; $d$: memory parameter; $c_f$, $c_\gamma$: constants; $\sim$: asymptotic equivalence', r'$f(\lambda)$: densitatea spectrală la frecvența $\lambda$; $\gamma(k)$: autocovarianța la lagul $k$; $d$: parametrul de memorie; $c_f$, $c_\gamma$: constante; $\sim$: echivalență asimptotică'),
         T(r'$H$: Hurst exponent of log volatility, which measures how rough the path is; $\Delta$: time step; $q$: moment order; $H < 1/2$: rough paths', r'$H$: exponentul Hurst al logaritmului volatilității, care măsoară cît de rough este traiectoria; $\Delta$: pasul de timp; $q$: ordinul momentului; $H < 1/2$: traiectorii rough')],
    11: [T(r'$\omega$: frequency; $\lambda$: HP smoothing parameter; $G(\omega) \in [0, 1]$: share of the variance at $\omega$ passed to the cycle', r'$\omega$: frecvența; $\lambda$: parametrul de netezire HP; $G(\omega) \in [0, 1]$: proporția din varianța de la $\omega$ transmisă ciclului'),
         T(r'$f_x$, $f_y$: spectra; $f_{xy}$: cross-spectrum; $\kappa^2(\omega) \in [0, 1]$: squared correlation of $x$ and $y$ at frequency $\omega$', r'$f_x$, $f_y$: spectrele; $f_{xy}$: spectrul încrucișat; $\kappa^2(\omega) \in [0, 1]$: corelația la pătrat a lui $x$ și $y$ la frecvența $\omega$')],
    12: [T(r'OWA: the M4 score, relative to the Naive2 benchmark (below 1: better); sMAPE: symmetric mean absolute percentage error', r'OWA: scorul M4, relativ la reperul Naive2 (sub 1: mai bun); sMAPE: eroarea procentuală absolută medie simetrică'),
         T(r'$Q$, $K$, $V$: query, key and value matrices; $d_k$: key dimension; softmax normalises each row to weights that sum to 1', r'$Q$, $K$, $V$: matricele de interogare (query), cheie (key) și valoare (value); $d_k$: dimensiunea cheilor; softmax normalizează fiecare rînd în ponderi care însumează 1')],
    13: [T(r'$S_{(k)}$: the $k$-th smallest of $n$ calibration scores; $\alpha$: the target miss rate; $\hat q$: the conformal threshold', r'$S_{(k)}$: al $k$-lea cel mai mic dintre $n$ scoruri de calibrare; $\alpha$: rata-țintă a ratărilor; $\hat q$: pragul conformal'),
         T(r'ACI: $\alpha_t$ working level; $\gamma$: step; $\mathrm{err}_t = 1$ after a miss', r'ACI: $\alpha_t$ nivelul de lucru; $\gamma$: pasul; $\mathrm{err}_t = 1$ după o ratare')],
    14: [T(r'$X_1$, $X_0$: pre-treatment predictors of the treated unit and of the donors; $V$: predictor weights; $w_j$: donor weights', r'$X_1$, $X_0$: predictorii anteriori tratamentului ai unității tratate și ai donatorilor; $V$: ponderile predictorilor; $w_j$: ponderile donatorilor'),
         T(r'$r_j$: post/pre RMSPE ratio of unit $j$; $J$: number of donors; $\#\{\cdot\}$: count', r'$r_j$: raportul RMSPE după/înainte al unității $j$; $J$: numărul de donatori; $\#\{\cdot\}$: numărul de elemente')],
    16: [T(r'$\mathrm{ADF}_{r_1}^{r_2}$: ADF statistic on the sample fraction $[r_1, r_2]$; BSADF: its sup over the start $r_1$; GSADF: the sup of BSADF over the end $r_2$', r'$\mathrm{ADF}_{r_1}^{r_2}$: statistica ADF pe fracțiunea de eșantion $[r_1, r_2]$; BSADF: supremumul ei după începutul $r_1$; GSADF: supremumul BSADF după sfîrșitul $r_2$'),
         T(r'$B_t$: bubble component of the price; $r$: interest rate; $\E_t$: expectation given information at $t$', r'$B_t$: componenta de bulă a prețului; $r$: rata dobînzii; $\E_t$: speranța condiționată de informația de la $t$')],
}


def review(k, title, ideas, formula, repl, mistakes, size='footnotesize'):
    """Two recap slides per chapter: key ideas and the key formula with its notation; the replication result and common mistakes."""
    D.frame(T(f'Chapter {k}: {title[0]} (1/2)', f'Capitolul {k}: {title[1]} (1/2)'),
            items((IDEA, ideas), (FORM, list(formula) + NOTA.get(k, []))), size)
    D.frame(T(f'Chapter {k}: {title[0]} (2/2)', f'Capitolul {k}: {title[1]} (2/2)'),
            items((REPL, repl), (MIST, mistakes)), 'small')


# =============================================================================
# CIFRE NOI (Quantlets/Ch_15)
# =============================================================================
SN = {r['K']: r for r in N['snooping']['rows']}
for K in (1, 5, 20, 50):
    P(f'sn.{K}.n', 100 * SN[K]['naive'], 0)
    P(f'sn.{K}.b', 100 * SN[K]['bonf'], 0)
    P(f'sn.{K}.m', 100 * SN[K]['maxt'], 0)
V.int('sn.reps', N['snooping']['reps'])
V.raw('sn.T', str(N['snooping']['T']))
LK = N['leakage']
for k in ('leaky_mean', 'honest_mean'):
    P('lk.' + k.split('_')[0], 100 * LK[k], 1)
P('lk.lpos', 100 * LK['leaky_pos'], 0)
P('lk.hpos', 100 * LK['honest_pos'], 0)
V.int('lk.reps', LK['reps'])
for k in ('T', 'n_test', 'P', 'k'):
    V.raw('lk.' + k, str(LK[k]))
PW = N['power']
V.int('pw.reps', PW['reps'])
PS = PW['P']
for d, kk in (('0.1', 'a'), ('0.2', 'b'), ('0.3', 'c')):
    r = PW['res'][d]
    for j, Pn in enumerate(PS):
        P(f'pw.{kk}.{Pn}', 100 * r['mc'][j], 0)
    P(f'pw.{kk}.p80', r['p80'], 0)
for j, Pn in enumerate(PS):
    P(f'pw.s.{Pn}', 100 * PW['res']['size'][j], 1)
P('pw.om', (1 + PW['rho']) / (1 - PW['rho']), 2)
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), two(items(
    (T(r'\textbf{Question}: what does the whole course give you for a research project, and how is the project defended?',
       r'\textbf{Întrebarea}: ce vă oferă întregul curs pentru un proiect de cercetare și cum se susține proiectul?'),
     [T('one chapter that ties Chapters 0--14 and the self-study Chapter 16 to the team project', 'un capitol care leagă Capitolele 0--14 și Capitolul 16 (studiu individual) de proiectul de echipă')]),
    (T(r'\textbf{Route}', r'\textbf{Traseul}'),
     [T('Part I: the course map, one recap per chapter, the toolbox of methods', 'Partea I: harta cursului, cîte o recapitulare pentru fiecare capitol, trusa de metode'),
      T('Part II: the research workflow, replicating a landmark paper, reproducibility, failure modes', 'Partea a II-a: fluxul de cercetare, replicarea unei lucrări de referință, reproductibilitatea, erorile frecvente'),
      T('Part III: the oral defence, AI in research, and choosing a project', 'Partea a III-a: susținerea orală, AI în cercetare și alegerea proiectului')]),
    T('There is no written exam: the project and its defence carry 70\\% of the grade', 'Cursul nu are examen scris: proiectul și susținerea lui reprezintă 70\\% din notă')),
    ph('ase', T('Bucharest University of Economic Studies', 'Academia de Studii Economice din București'), h='0.40\\textheight')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Place every chapter on the map of methods and state its key idea, key formula and replication result', 'Plasați fiecare capitol pe harta metodelor și formulați ideea-cheie, formula-cheie și rezultatul replicării'),
    T('Choose the right tool for a research question about dependent data', 'Alegeți instrumentul potrivit pentru o întrebare de cercetare despre date dependente'),
    T('Plan a project from the question to the report, with a pre-registration and a power calculation for the evaluation', 'Planificați un proiect de la întrebare la raport, cu preînregistrare și calculul puterii evaluării'),
    T('Replicate a landmark paper, explain a failed replication and make every number reproducible', 'Replicați o lucrare de referință, explicați o replicare nereușită și faceți reproductibil fiecare rezultat numeric'),
    T('Recognise data snooping, leakage, look-ahead, p-hacking and overclaiming in your own work', 'Recunoașteți data snooping, leakage, look-ahead, p-hacking și afirmațiile exagerate în propria lucrare'),
    T('Prepare the individual oral defence and document the use of AI tools', 'Pregătiți susținerea orală individuală și documentați folosirea instrumentelor AI')))

D.frame(T('Assessment at a glance', 'Evaluarea pe scurt'), table(
    TB + 'p{3.4cm}' + '>{\\raggedleft\\arraybackslash}p{1.2cm}' + TB + 'p{1.5cm}' + TB + 'p{6.1cm}',
    T(r'\textbf{Component}', r'\textbf{Componenta}') + ' & ' + T(r'\textbf{Weight}', r'\textbf{Pondere}') + ' & ' + T(r'\textbf{Who}', r'\textbf{Cine}') + ' & ' + T(r'\textbf{Content}', r'\textbf{Conținut}'),
    [T('Proposal and pre-registration', 'Propunerea și preînregistrarea') + r' & 5\% & ' + T('team', 'echipa') + ' & ' + T('question, paper to replicate, data, evaluation design fixed before estimation', 'întrebarea, lucrarea replicată, datele, designul evaluării fixat înaintea estimării'),
     T('Replication and extension', 'Replicarea și extensia') + r' & 15\% & ' + T('team', 'echipa') + ' & ' + T('repository, report in the form of a paper, AI\\_USE.md, AI\\_ERRORS.md', 'repository, raport în forma unui articol, AI\\_USE.md, AI\\_ERRORS.md'),
     T('Oral defence', 'Susținerea orală') + r' & 50\% & ' + T('each student', 'fiecare student') + ' & ' + T('about 15 minutes: 5 minutes presenting one\'s own contribution, 10 minutes of questions on the code, the method and the results', 'circa 15 minute: 5 minute de prezentare a contribuției proprii și 10 minute de întrebări despre cod, metodă și rezultate'),
     T('Chapter quizzes', 'Quiz-uri pe capitole') + r' & 20\% & ' + T('each student', 'fiecare student') + ' & ' + T('online, first attempt graded', 'online, se notează prima încercare'),
     T('Attendance', 'Prezență') + r' & 10\% & ' + T('each student', 'fiecare student') + ' & ' + T('lectures and seminars', 'cursuri și seminarii')],
    size='footnotesize') + items(
    T('Teams of at most three students; the project can be written and defended in Romanian or in English', 'Echipe de cel mult trei studenți; proiectul se poate redacta și susține în română sau în engleză'),
    T('Grades of team members can differ: half of the final grade is individual', 'Notele membrilor unei echipe pot fi diferite: jumătate din nota finală este individuală')))

# =============================================================================
# HARTA CURSULUI
# =============================================================================
D.section('The course map', 'Harta cursului')


def box(name, x, y, num, en, ro, style='box'):
    return f'\\node[{style}] ({name}) at ({x},{y}) {{\\textbf{{{num}}} {T(en, ro)}}};\n'


MAP = (r'''\hyphenpenalty=10000\relax
\begin{center}
\begin{tikzpicture}[font=\tiny, box/.style={draw=MainBlue, rounded corners=2pt, fill=MainBlue!6, align=center, text width=2.75cm, minimum height=0.55cm, inner sep=2pt},
  base/.style={box, draw=Forest, fill=Forest!8, text width=3.6cm}, proj/.style={box, draw=IDAred, fill=IDAred!8, text width=3.2cm, font=\scriptsize},
  head/.style={font=\scriptsize\bfseries, text=MainBlue, align=center, text width=2.9cm}, ar/.style={-{Stealth[length=1.6mm]}, MainBlue!70, thick}]
''' + box('c0', -2.1, 2.75, 0, 'Inference for dependent data', 'Inferență pentru date dependente', 'base')
    + box('c1', 2.1, 2.75, 1, 'Forecast evaluation and combination', 'Evaluarea și combinarea prognozelor', 'base')
    + f'\\node[head] (h1) at (-4.95,1.85) {{{T("Structure and identification", "Structură și identificare")}}};\n'
    + f'\\node[head] (h2) at (-1.65,1.85) {{{T("Latent states", "Stări latente")}}};\n'
    + f'\\node[head] (h3) at (1.65,1.85) {{{T("Volatility and risk", "Volatilitate și risc")}}};\n'
    + f'\\node[head] (h4) at (4.95,1.85) {{{T("Frequency and learning", "Frecvență și învățare")}}};\n'
    + box('c2', -4.95, 1.2, 2, 'Breaks and nonlinear models', 'Rupturi și modele neliniare')
    + box('c3', -4.95, 0.5, 3, 'SVAR and local projections', 'SVAR și proiecții locale')
    + box('c4', -4.95, -0.2, 4, 'Cointegration, VECM, ARDL, panels', 'Cointegrare, VECM, ARDL, panel')
    + box('c5', -4.95, -0.9, 5, 'BVAR, factors, nowcasting', 'BVAR, factori, nowcasting')
    + box('c6', -1.65, 1.2, 6, 'State space and Bayesian filtering', 'Spațiul stărilor și filtrare bayesiană')
    + box('c7', -1.65, 0.5, 7, 'Regime switching', 'Schimbare de regim')
    + box('c8', 1.65, 1.2, 8, 'Realised measures, HAR, MGARCH', 'Măsuri realizate, HAR, MGARCH')
    + box('c9', 1.65, 0.5, 9, 'VaR, ES and backtesting', 'VaR, ES și backtesting')
    + box('c10', 1.65, -0.2, 10, 'Long memory and rough volatility', 'Memorie lungă și rough volatility')
    + box('c11', 4.95, 1.2, 11, 'Spectral and wavelet analysis', 'Analiză spectrală și wavelet')
    + box('c12', 4.95, 0.5, 12, 'Machine and deep learning', 'Machine și deep learning')
    + box('c13', 4.95, -0.2, 13, 'Foundation models, conformal', 'Foundation models, conformal')
    + box('c14', -3.3, -1.95, 14, 'Causal inference for time series', 'Inferență cauzală pentru serii de timp')
    + box('c16', 0, -1.95, 16, 'Explosive roots and bubbles (self-study)', 'Rădăcini explozive și bule (studiu individual)')
    + box('c15', 3.6, -1.95, 15, 'Project: replication, extension, defence', 'Proiect: replicare, extensie, susținere', 'proj')
    + r'''\draw[ar] (c0.south) -- (h1.north); \draw[ar] (c0.south) -- (h2.north); \draw[ar] (c1.south) -- (h3.north); \draw[ar] (c1.south) -- (h4.north);
\draw[ar] (c0) -- (c1);
\draw[ar] (c16) -- (c15); \draw[ar] (c14.north east) to[out=20, in=160] (c15.north west);
\draw[ar, dashed] (c5.south) to[out=-90, in=150] (c14.north west);
\draw[ar, dashed] (c13.south) to[out=-90, in=60] (c15.north);
\end{tikzpicture}
\end{center}
''')
D.frame(T('The course map', 'Harta cursului'), MAP + items(
    T(r'Chapters 0 and 1 are used everywhere: inference for dependent data and honest out-of-sample evaluation', r'Capitolele 0 și 1 se folosesc peste tot: inferența pentru date dependente și evaluarea corectă în afara eșantionului'),
    T('Every chapter feeds the project: one landmark paper to replicate and one extension', 'Fiecare capitol alimentează proiectul: o lucrare de referință de replicat și o extensie')), 'footnotesize')

D.frame(T('Five questions for every analysis', 'Cinci întrebări pentru orice analiză'), items(
    (T(r'\textbf{Target}: which functional is forecast or estimated (mean, quantile, distribution, causal effect)?', r'\textbf{Ținta}: ce funcțională se prognozează sau se estimează (medie, cuantilă, distribuție, efect cauzal)?'),
     [T('the loss or score must be consistent for it (Chapters 1 and 9)', 'funcția de pierdere sau de scor trebuie să fie consistentă pentru ea (Capitolele 1 și 9)')]),
    (T(r'\textbf{Dependence}: which standard errors are valid with autocorrelation, heteroskedasticity and persistence?', r'\textbf{Dependența}: ce erori standard sînt valide cu autocorelație, heteroscedasticitate și persistență?'),
     [T('HAC with fixed-$b$ or EWC, block bootstrap, Monte Carlo size at your persistence (Chapter 0)', 'HAC cu fixed-$b$ sau EWC, bootstrap pe blocuri, mărimea testului prin Monte Carlo la persistența seriei (Capitolul 0)')]),
    (T(r'\textbf{Identification}: what assumption turns a correlation into the claim you make?', r'\textbf{Identificarea}: ce ipoteză transformă o corelație în afirmația pe care o faceți?'),
     [T('ordering, sign, instrument, donor pool, regime labels (Chapters 3, 7, 14)', 'ordonarea, semnul, instrumentul, grupul de donatori, etichetarea regimurilor (Capitolele 3, 7, 14)')]),
    (T(r'\textbf{Evaluation}: is the design fixed before the results, in real time, with a test that fits?', r'\textbf{Evaluarea}: este designul fixat înaintea rezultatelor, în timp real, cu un test potrivit?'),
     [T('DM--HLN, Clark--West for nested models, MCS and SPA for many', 'DM--HLN, Clark--West pentru modele imbricate, MCS și SPA pentru mai multe modele')]),
    (T(r'\textbf{Robustness}: does the conclusion survive the forks of the analysis?', r'\textbf{Robustețea}: rezistă concluzia la bifurcațiile analizei?'),
     [T('every chapter ends with a mini-case that varies the specification', 'fiecare capitol se încheie cu un mini studiu de caz care variază specificația')])), 'footnotesize')

D.frame(T('Three threads across the course', 'Trei fire comune ale cursului'), items(
    (T(r'\textbf{Inference under dependence}', r'\textbf{Inferența sub dependență}'),
     [T(r'long-run variance $\Omega = 2\pi f(0)$ (Chapter 0), with $f(0)$ the spectral density at frequency zero: the variance of a sum of $n$ dependent terms is about $n\Omega$', r'varianța de termen lung $\Omega = 2\pi f(0)$ (Capitolul 0), unde $f(0)$ este densitatea spectrală la frecvența zero: varianța unei sume de $n$ termeni dependenți este aproximativ $n\Omega$'),
      T(r'it reappears in DM tests (Chapter 1), local projections (Chapter 3), cumulative effects (Chapter 14)', r'ea reapare în testele DM (Capitolul 1), proiecțiile locale (Capitolul 3), efectele cumulate (Capitolul 14)'),
      T('non-standard limits: sup-tests for breaks, Johansen trace, regime tests, GSADF; critical values from the right distribution', 'limite nestandard: teste sup pentru rupturi, testul urmei Johansen, teste pentru regimuri, GSADF; valori critice din distribuția corectă')]),
    (T(r'\textbf{Honest out-of-sample evaluation}', r'\textbf{Evaluarea corectă în afara eșantionului}'),
     [T('proper scores and consistent losses, real-time data, blocked validation, evaluation after model release (Chapters 1, 9, 12, 13)', 'reguli de scor proprii și funcții de pierdere consistente, date în timp real, validare pe blocuri, evaluare după lansarea modelelor (Capitolele 1, 9, 12, 13)')]),
    (T(r'\textbf{Identification and replication}', r'\textbf{Identificarea și replicarea}'),
     [T('structural shocks, latent states and causal effects are model-dependent; landmark results were replicated on today\'s data, and some did not survive', 'șocurile structurale, stările latente și efectele cauzale depind de model; rezultatele de referință au fost replicate pe datele de azi, iar unele nu au rezistat')])))

# =============================================================================
# RECAPITULAREA CAPITOLELOR
# =============================================================================
D.section('Chapter recaps', 'Recapitularea capitolelor')

review(0, ('Inference for dependent data', 'Inferență pentru date dependente'),
       [T(r'The precision of a mean or a slope is governed by the long-run variance, not by $\gamma_0$', r'Precizia unei medii sau a unei pante este dată de varianța de termen lung, nu de $\gamma_0$'),
        T('HAC with fixed-$b$ or EWC critical values; block bootstraps resample dependence, the wild bootstrap does not', 'HAC cu valori critice fixed-$b$ sau EWC; bootstrap-ul pe blocuri reeșantionează dependența, wild bootstrap nu')],
       [T(r'$\Omega = \gamma_0 + 2\sum_{j\ge1}\gamma_j = 2\pi f(0)$; $\hat\Omega_{NW} = \hat\Gamma_0 + \sum_{j=1}^{L}\big(1 - \frac{j}{L+1}\big)(\hat\Gamma_j + \hat\Gamma_j\')$', r'$\Omega = \gamma_0 + 2\sum_{j\ge1}\gamma_j = 2\pi f(0)$; $\hat\Omega_{NW} = \hat\Gamma_0 + \sum_{j=1}^{L}\big(1 - \frac{j}{L+1}\big)(\hat\Gamma_j + \hat\Gamma_j\')$')],
       [T(r'\refEH: slope @{c0.b1} with classical $t$ = @{c0.tcl}, but fixed-$b$ $t$ = @{c0.tll} below its critical value @{c0.cvll}; @{c0.early} before 1989, @{c0.late} afterwards: \textbf{partly replicated}', r'\refEH: panta @{c0.b1}, cu $t$ clasic = @{c0.tcl}, dar $t$ fixed-$b$ = @{c0.tll}, sub valoarea critică @{c0.cvll}; @{c0.early} înainte de 1989, @{c0.late} după: \textbf{replicare parțială}'),
        T(r'\refWhite on 50 moving-average rules for the BET: naive $p$ = @{c0.rcpn}, Reality Check $p$ = @{c0.rcp}', r'\refWhite pe 50 de reguli cu medii mobile pentru BET: $p$ naiv = @{c0.rcpn}, $p$ Reality Check = @{c0.rcp}')],
       [T(r'i.i.d.\ standard errors: the naive test rejects @{c0.naive1}\% of true nulls at $\phi = 0.9$, $T = 100$, and still @{c0.naive4}\% at $T = 400$', r'erori standard i.i.d.: testul naiv respinge @{c0.naive1}\% din ipotezele nule adevărate la $\phi = 0{,}9$, $T = 100$, și tot @{c0.naive4}\% la $T = 400$'),
        T('the best of many specifications reported without a search-adjusted p-value', 'cea mai bună dintre multe specificații, raportată fără un p-value ajustat pentru căutare')])

review(1, ('Forecast evaluation and combination', 'Evaluarea și combinarea prognozelor'),
       [T('Choose the loss or score first: it defines the target (mean, median, quantile, distribution)', 'Alegeți întîi funcția de pierdere sau de scor: ea definește ținta (medie, mediană, cuantilă, distribuție)'),
        T('Calibration with PIT, ranking with proper scores; DM--HLN, Clark--West for nested models, SPA and MCS for many', 'Calibrare cu PIT, ierarhizare cu reguli de scor proprii; DM--HLN, Clark--West pentru modele imbricate, SPA și MCS pentru mai multe')],
       [T(r'$\mathrm{DM} = \bar d/\sqrt{\hat\Omega_d/P}$, $\mathrm{DM}^* = \mathrm{DM}\sqrt{(P + 1 - 2h + h(h - 1)/P)/P}$ against $t_{P-1}$', r'$\mathrm{DM} = \bar d/\sqrt{\hat\Omega_d/P}$, $\mathrm{DM}^* = \mathrm{DM}\sqrt{(P + 1 - 2h + h(h - 1)/P)/P}$, comparat cu $t_{P-1}$')],
       [T(r'\refMR on EUR/RON: AR(1) RMSE @{c1.ar} times the random walk, drift @{c1.drift} (Clark--West $p$ = @{c1.cwp}): \textbf{replicated}', r'\refMR pe EUR/RON: RMSE AR(1) de @{c1.ar} ori cel al mersului aleator, drift @{c1.drift} (Clark--West $p$ = @{c1.cwp}): \textbf{replicat}'),
        T(r'\refGKMT on the SPF: median @{c1.med}, previous best @{c1.prev} (HLN $p$ = @{c1.prevp}); \refAO: ratio @{c1.ao} but $p$ = @{c1.aop}', r'\refGKMT pe SPF: mediana @{c1.med}, cel mai bun anterior @{c1.prev} (HLN $p$ = @{c1.prevp}); \refAO: raport @{c1.ao}, dar $p$ = @{c1.aop}')],
       [T(r'plain DM with few multi-step forecasts: size @{c1.dm}\% at $h = 8$, $P = 16$ (HLN: @{c1.hln}\%)', r'testul DM simplu cu puține prognoze pe mai mulți pași: mărimea @{c1.dm}\% la $h = 8$, $P = 16$ (HLN: @{c1.hln}\%)'),
        T('DM on nested models; estimated combination weights for similar forecasts', 'DM pentru modele imbricate; ponderi de combinare estimate pentru prognoze asemănătoare')])

review(2, ('Structural breaks and nonlinear models', 'Rupturi structurale și modele neliniare'),
       [T('A break date chosen from the data is a nuisance parameter: sup, exp and ave tests with their own critical values', 'O dată a rupturii aleasă din date este un parametru de deranj: teste sup, exp și ave cu valori critice proprii'),
        T('Breaks and nonlinearity mimic each other: test one allowing for the other', 'Rupturile și neliniaritatea se imită reciproc: testați una ținînd cont de cealaltă')],
       [T(r'$\sup_{\pi}W_T(\pi) \Rightarrow \sup_\pi \|B_p(\pi) - \pi B_p(1)\|^2/[\pi(1 - \pi)]$; TAR: $y_t = \phi_1\'x_t\mathbf 1\{q_{t-d} \le \gamma\} + \phi_2\'x_t\mathbf 1\{q_{t-d} > \gamma\} + \varepsilon_t$', r'$\sup_{\pi}W_T(\pi) \Rightarrow \sup_\pi \|B_p(\pi) - \pi B_p(1)\|^2/[\pi(1 - \pi)]$; TAR: $y_t = \phi_1\'x_t\mathbf 1\{q_{t-d} \le \gamma\} + \phi_2\'x_t\mathbf 1\{q_{t-d} > \gamma\} + \varepsilon_t$')],
       [T(r'\refMPQ: break in @{c2.mpqd}, sup-$W$ = @{c2.mpq}; on the sample to 2026 only @{c2.mpqx}; \refBP: @{c2.bpm} breaks at the published dates', r'\refMPQ: ruptură în @{c2.mpqd}, sup-$W$ = @{c2.mpq}; pe eșantionul pînă în 2026 doar @{c2.mpqx}; \refBP: @{c2.bpm} rupturi la datele publicate'),
        T(r'\refHanB: $\hat\gamma$ = @{c2.gam} (paper @{pub.hansen_gamma}); \refTPS: Monte Carlo $p$ = @{c2.tpsp} (paper @{pub.tps_p}): \textbf{not replicated}', r'\refHanB: $\hat\gamma$ = @{c2.gam} (lucrarea: @{pub.hansen_gamma}); \refTPS: $p$ Monte Carlo = @{c2.tpsp} (lucrarea: @{pub.tps_p}): \textbf{nereplicat}')],
       [T(r'Chow test at a data-chosen date: size @{c2.chow0}--@{c2.chow1}\%; the sup critical value is @{c2.supcv}, not 3.84', r'testul Chow la o dată aleasă din date: mărimea @{c2.chow0}--@{c2.chow1}\%; valoarea critică sup este @{c2.supcv}, nu 3,84'),
        T('in-sample nonlinearity read as a forecasting gain', 'neliniaritatea din eșantion citită drept cîștig de prognoză')])

review(3, ('Structural VAR and local projections', 'Modele VAR structurale și proiecții locale'),
       [T('A structural VAR is a reduced form plus an identifying assumption; the assumption is the economics', 'Un VAR structural este o formă redusă plus o ipoteză de identificare; ipoteza este partea economică'),
        T('Zeros, signs, narratives, heteroskedasticity and instruments buy identification with different assumptions; LP and VAR estimate the same responses', 'Zerourile, semnele, narațiunile, heteroscedasticitatea și instrumentele identifică prin ipoteze diferite; LP și VAR estimează aceleași răspunsuri')],
       [T(r'$u_t = B_0\varepsilon_t$, $\Theta_h = \Phi_hB_0$; proxy: $\E(u_tz_t) = \alpha b_1$; LP: $y_{t+h} = \mu_h + \beta_hx_t + \gamma_h\'w_t + \xi_{t+h}$', r'$u_t = B_0\varepsilon_t$, $\Theta_h = \Phi_hB_0$; proxy: $\E(u_tz_t) = \alpha b_1$; LP: $y_{t+h} = \mu_h + \beta_hx_t + \gamma_h\'w_t + \xi_{t+h}$')],
       [T(r'\refCEE: industrial production trough @{c3.ip}\% after @{c3.ipm} months, with the price puzzle; \refGK: $F$ = @{c3.gkF}, excess bond premium +@{c3.ebp}: \textbf{replicated}', r'\refCEE: minimul producției industriale @{c3.ip}\% după @{c3.ipm} luni, cu puzzle-ul prețurilor; \refGK: $F$ = @{c3.gkF}, prima de risc a obligațiunilor +@{c3.ebp}: \textbf{replicat}'),
        T(r'\refKil: oil-price variance at 60 months: supply @{c3.k1}\%, aggregate demand @{c3.k2}\%, oil-specific demand @{c3.k3}\%', r'\refKil: varianța prețului petrolului la 60 de luni: oferta @{c3.k1}\%, cererea agregată @{c3.k2}\%, cererea specifică @{c3.k3}\%')],
       [T('a recursive ordering read as a fact; the wild bootstrap for a proxy SVAR (use the moving-block bootstrap)', 'o ordonare recursivă citită ca fapt; wild bootstrap pentru un proxy SVAR (folosiți bootstrap-ul pe blocuri mobile)'),
        T(r'a short VAR at long horizons: bias @{c3.vb} at $h = 8$ against @{c3.lb} for LP, at a higher variance', r'un VAR scurt la orizonturi lungi: deplasarea @{c3.vb} la $h = 8$, față de @{c3.lb} pentru LP, cu o varianță mai mare')])

review(4, ('Cointegration: VECM, ARDL and panel data', 'Cointegrare: VECM, ARDL și date panel'),
       [T(r'Johansen is reduced-rank regression; the rank test is non-standard, depends on the deterministic case and over-rejects in small samples', r'Johansen este o regresie de rang redus; testul rangului este nestandard, depinde de cazul determinist și respinge prea des în eșantioane mici'),
        T(r'Given the rank, tests on $\beta$ and $\alpha$ are $\chi^2$; ARDL is a conditional VECM; panels need cross-section dependence first', r'Dat rangul, testele pe $\beta$ și $\alpha$ sînt $\chi^2$; ARDL este un VECM condiționat; la panel se verifică întîi dependența transversală')],
       [T(r'$\Delta y_t = \alpha\beta\'y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\Delta y_{t-i} + \Phi D_t + \varepsilon_t$, $LR_{tr}(r) = -T\sum_{i>r}\ln(1 - \hat\lambda_i)$', r'$\Delta y_t = \alpha\beta\'y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\Delta y_{t-i} + \Phi D_t + \varepsilon_t$, $LR_{tr}(r) = -T\sum_{i>r}\ln(1 - \hat\lambda_i)$')],
       [T(r'\refKPSW: two cointegrating relations, but the great ratios rejected (LR @{c4.kplr}, $p$ @{c4.kpp}): \textbf{partly replicated}', r'\refKPSW: două relații de cointegrare, dar rapoartele mari sînt respinse (LR @{c4.kplr}, $p$ @{c4.kpp}): \textbf{replicare parțială}'),
        T(r'\refPSS on EU-27 consumption: income elasticity @{c4.pmg}, Hausman $p$ = @{c4.pH}; the inflation effect is not robust', r'\refPSS pe consumul din UE-27: elasticitatea în raport cu venitul @{c4.pmg}, Hausman $p$ = @{c4.pH}; efectul inflației nu este robust')],
       [T(r'asymptotic critical values at $T = 50$: size @{c4.sa}\% against @{c4.sw}\% for the wild bootstrap', r'valori critice asimptotice la $T = 50$: mărimea @{c4.sa}\%, față de @{c4.sw}\% pentru wild bootstrap'),
        T(r'the rank read as a measurement: Romanian pass-through, wild bootstrap $p$ = @{c4.bo4} with four lags', r'rangul citit ca o măsurătoare: transmiterea dobînzilor în România, $p$ wild bootstrap = @{c4.bo4} cu patru laguri')])

review(5, ('Bayesian VAR, factor models and nowcasting', 'Modele VAR bayesiene, modele factoriale și nowcasting'),
       [T('Many series and few observations: shrink (priors) or compress (factors); bigger systems need tighter priors', 'Multe serii și puține observații: shrinkage (distribuții a priori) sau comprimare (factori); sistemele mai mari cer distribuții a priori mai strînse'),
        T('Nowcasting is Kalman filtering with a ragged edge; every revision is a sum of news', 'Nowcasting-ul este filtrare Kalman cu marginea neregulată; fiecare revizuire este o sumă de știri')],
       [T(r'Minnesota: $\Var[(A_l)_{ij}] = \lambda^2/l^2$ if $j = i$, $\vartheta\lambda^2\sigma_i^2/(l^2\sigma_j^2)$ otherwise', r'Minnesota: $\Var[(A_l)_{ij}] = \lambda^2/l^2$ dacă $j = i$, $\vartheta\lambda^2\sigma_i^2/(l^2\sigma_j^2)$ altfel')],
       [T(r'\refBGR, employment, $h = 1$: @{c5.s}, @{c5.m}, @{c5.l} for small, medium, large (paper @{pub.bgr_small}, @{pub.bgr_medium}, @{pub.bgr_large}): \textbf{replicated} for 1971--2003', r'\refBGR, ocuparea, $h = 1$: @{c5.s}, @{c5.m}, @{c5.l} pentru sistemul mic, mediu, mare (lucrarea: @{pub.bgr_small}, @{pub.bgr_medium}, @{pub.bgr_large}): \textbf{replicat} pentru 1971--2003'),
        T(r'\refSW: industrial production, $h = 12$: @{c5.di1} in 1970--1998, but @{c5.di2} in 1999--2019: the gain vanishes', r'\refSW: producția industrială, $h = 12$: @{c5.di1} în 1970--1998, dar @{c5.di2} în 1999--2019: cîștigul dispare')],
       [T(r'a homoskedastic BVAR through 2020: relative MSFE @{c5.x} at 12 months', r'un BVAR homoscedastic care include 2020: MSFE relativ @{c5.x} la 12 luni'),
        T(r'``better nowcasts\'\' from a lower RMSE without a test: Romanian GDP, DM $t$ = @{c5.dmt}, $p$ = @{c5.dmp}', r'„nowcast-uri mai bune” pe baza unui RMSE mai mic, fără test: PIB-ul României, DM $t$ = @{c5.dmt}, $p$ = @{c5.dmp}')])

review(6, ('State space models and Bayesian filtering', 'Modele în spațiul stărilor și filtrare bayesiană'),
       [T('The Kalman filter is Gaussian conditioning applied recursively; smoother, likelihood and simulation smoother follow from it', 'Filtrul Kalman este condiționare gaussiană aplicată recursiv; netezirea, verosimilitatea și netezirea prin simulare decurg din el'),
        T('Initialise nonstationary states exactly; stochastic volatility is not GARCH; latent quantities come with model-dependent bands', 'Inițializați exact stările nestaționare; volatilitatea stochastică nu este GARCH; mărimile latente au benzi care depind de model')],
       [T(r'$v_t = y_t - Z_ta_t$, $F_t = Z_tP_tZ_t\' + H_t$, $K_t = T_tP_tZ_t\'F_t^{-1}$, $a_{t+1} = T_ta_t + K_tv_t$', r'$v_t = y_t - Z_ta_t$, $F_t = Z_tP_tZ_t\' + H_t$, $K_t = T_tP_tZ_t\'F_t^{-1}$, $a_{t+1} = T_ta_t + K_tv_t$')],
       [T(r'\refMNZ on today\'s GDP vintage: $\hat\rho$ = @{c6.rho}, correlation with the Beveridge--Nelson cycle @{c6.corr}; cycle s.d.\ @{c6.sd0} (UC0) against @{c6.sd1}: \textbf{replicated}', r'\refMNZ pe ediția de azi a PIB: $\hat\rho$ = @{c6.rho}, corelația cu ciclul Beveridge--Nelson @{c6.corr}; abaterea standard a ciclului @{c6.sd0} (UC0), față de @{c6.sd1}: \textbf{replicat}'),
        T(r'Stochastic volatility beats GARCH on the S\&P 500 by @{c6.dll} log-likelihood points', r'Volatilitatea stochastică depășește GARCH pe S\&P 500 cu @{c6.dll} puncte de log-verosimilitate')],
       [T(r'a zero variance estimate read as a constant level: @{c6.pu}\% of estimates are exactly zero when the true variance is zero (pile-up)', r'o varianță estimată zero citită ca nivel constant: @{c6.pu}\% din estimații sînt exact zero cînd varianța reală este zero (pile-up)'),
        T('a ``big kappa\'\' initialisation; an output gap without its band', 'inițializarea cu „kappa mare”; un output gap fără banda lui')])

review(7, ('Regime-switching models', 'Modele cu schimbare de regim'),
       [T('The Hamilton filter and the Kim smoother are exact recursions for a discrete latent state; EM finds local and degenerate maxima', 'Filtrul Hamilton și netezirea Kim sînt recursii exacte pentru o stare latentă discretă; EM găsește maxime locale și degenerate'),
        T('The number of regimes is a non-standard testing problem; regimes, breaks and long memory are observationally close', 'Numărul de regimuri este o problemă de testare nestandard; regimurile, rupturile și memoria lungă sînt greu de deosebit în date')],
       [T(r'$\hat\xi_{t|t} = \hat\xi_{t|t-1}\odot\eta_t/\mathbf 1\'(\hat\xi_{t|t-1}\odot\eta_t)$, $\hat\xi_{t+1|t} = \mathbf P\'\hat\xi_{t|t}$, $\E D_i = 1/(1 - p_{ii})$', r'$\hat\xi_{t|t} = \hat\xi_{t|t-1}\odot\eta_t/\mathbf 1\'(\hat\xi_{t|t-1}\odot\eta_t)$, $\hat\xi_{t+1|t} = \mathbf P\'\hat\xi_{t|t}$, $\E D_i = 1/(1 - p_{ii})$')],
       [T(r'\refHam on his data: log-likelihood @{c7.ll} with two implementations, QPS @{c7.qps}: \textbf{replicated exactly}', r'\refHam pe datele lui: log-verosimilitatea @{c7.ll} cu două implementări, QPS @{c7.qps}: \textbf{replicat exact}'),
        T(r'On today\'s data the low regime becomes sharp falls: 2008Q4 probability @{c7.p08}, 2001 at most @{c7.p01}', r'Pe datele de azi regimul scăzut devine o succesiune de căderi bruște: probabilitatea pentru T4 2008 @{c7.p08}, pentru 2001 cel mult @{c7.p01}')],
       [T(r'$\chi^2$ critical values for the number of regimes: LR @{c7.LR}, bootstrap 95\% quantile @{c7.q95}, not @{c7.c2}', r'valori critice $\chi^2$ pentru numărul de regimuri: LR @{c7.LR}, cuantila bootstrap de 95\% @{c7.q95}, nu @{c7.c2}'),
        T('statistical regimes read as economic regimes; smoothed probabilities used to judge real-time dating', 'regimuri statistice citite ca regimuri economice; probabilități netezite folosite pentru a judeca datarea în timp real')])

review(8, ('Advanced volatility modelling', 'Modelarea avansată a volatilității'),
       [T('Gaussian QML needs only the variance equation; with fat tails, use sandwich standard errors', 'QML gaussian are nevoie doar de ecuația varianței; cu cozi groase, folosiți erori standard sandwich'),
        T('Realised measures make volatility observable with a known error; HAR, HARQ and Realized GARCH win one day ahead', 'Măsurile realizate fac volatilitatea observabilă, cu o eroare cunoscută; HAR, HARQ și Realized GARCH cîștigă la o zi')],
       [T(r'HARQ: $\mathrm{RV}_{t+1} = \beta_0 + (\beta_d + \beta_{dQ}\sqrt{\mathrm{RQ}_t})\mathrm{RV}_t + \beta_w\mathrm{RV}^{(w)}_t + \beta_m\mathrm{RV}^{(m)}_t + u_{t+1}$', r'HARQ: $\mathrm{RV}_{t+1} = \beta_0 + (\beta_d + \beta_{dQ}\sqrt{\mathrm{RQ}_t})\mathrm{RV}_t + \beta_w\mathrm{RV}^{(w)}_t + \beta_m\mathrm{RV}^{(m)}_t + u_{t+1}$')],
       [T(r'\refBPQ on crypto: QLIKE relative to HAR @{c8.qb} (Bitcoin), @{c8.qe} (Ether)', r'\refBPQ pe cripto: QLIKE relativ la HAR @{c8.qb} (Bitcoin), @{c8.qe} (Ether)'),
        T(r'\refEGS: industrial production $t$ = @{c8.ipt}; only the realised-variance driver works ($t$ = @{c8.rvt})', r'\refEGS: producția industrială $t$ = @{c8.ipt}; funcționează doar varianța realizată ($t$ = @{c8.rvt})'),
        T(r'\refELW: GMV volatility @{c8.gdnl} (DCC-NL) against @{c8.gd} (DCC): the gain does not appear here: \textbf{not replicated}', r'\refELW: volatilitatea GMV @{c8.gdnl} (DCC-NL), față de @{c8.gd} (DCC): cîștigul nu apare aici: \textbf{nereplicat}')],
       [T(r'Hessian standard errors with Student-$t(5)$ errors: coverage @{c8.hc}\% against @{c8.bw}\% for the sandwich', r'erori standard din hessiană cu erori Student-$t(5)$: acoperire @{c8.hc}\%, față de @{c8.bw}\% pentru sandwich'),
        T('non-robust losses (MAE, MSE on logs) with a noisy volatility proxy', 'funcții de pierdere nerobuste (MAE, MSE pe logaritmi) cu un indicator zgomotos al volatilității')])

review(9, ('VaR, ES and backtesting', 'VaR, ES și backtesting'),
       [T('A risk forecast is a point forecast of a functional: judge it with a consistent loss; VaR is elicitable, ES only jointly with VaR', 'O prognoză de risc este o prognoză punctuală a unei funcționale: judecați-o cu o funcție de pierdere consistentă; VaR este elicitabil, ES doar împreună cu VaR'),
        T('Backtests are moment tests with estimation risk; comparisons need DM, MCS and Murphy diagrams', 'Backtest-urile sînt teste de momente cu risc de estimare; comparațiile cer DM, MCS și diagrame Murphy')],
       [T(r'$L_{\mathrm{FZ0}}(y, v, e; \alpha) = -\frac{1}{\alpha e}\mathbf 1\{y \le v\}(v - y) + \frac{v}{e} + \ln(-e) - 1$; $\mathrm{VaR}_\alpha = -q_\alpha$', r'$L_{\mathrm{FZ0}}(y, v, e; \alpha) = -\frac{1}{\alpha e}\mathbf 1\{y \le v\}(v - y) + \frac{v}{e} + \ln(-e) - 1$; $\mathrm{VaR}_\alpha = -q_\alpha$')],
       [T(r'\refPZC: GAS-1F loss @{c9.loss} (paper @{pub.pzc_loss}): the ranking \textbf{replicates}; its goodness-of-fit p-values @{c9.gv} and @{c9.ge} (paper @{pub.pzc_gof_var} and @{pub.pzc_gof_es}) \textbf{do not}', r'\refPZC: pierderea GAS-1F @{c9.loss} (lucrarea: @{pub.pzc_loss}): ierarhia \textbf{se replică}; p-value-urile testelor de adecvare @{c9.gv} și @{c9.ge} (lucrarea: @{pub.pzc_gof_var} și @{pub.pzc_gof_es}) \textbf{nu}'),
        T(r'\refEM out of sample: only IG passes the DQ test ($p$ = @{c9.ig}; SAV @{c9.sav})', r'\refEM în afara eșantionului: doar IG trece testul DQ ($p$ = @{c9.ig}; SAV @{c9.sav})')],
       [T(r'ranking ES forecasts alone; Normal VaR 1\% with a hit rate of @{c9.gn}\%', r'ierarhizarea prognozelor ES singure; VaR 1\% Normal cu o rată a depășirilor de @{c9.gn}\%'),
        T(r'the $\sqrt{h}$ rule under volatility clustering; ``the best ES model\'\' instead of the MCS', r'regula $\sqrt{h}$ în prezența volatility clustering; „cel mai bun model ES” în locul MCS')])

review(10, ('Long memory and rough volatility', 'Memorie lungă și rough volatility'),
       [T(r'Long memory is a pole at frequency zero; estimate $d$ by (exact) local Whittle and report $\hat d(m)$ across bandwidths', r'Memoria lungă este un pol la frecvența zero; estimați $d$ prin local Whittle (exact) și raportați $\hat d(m)$ pentru mai multe lățimi de bandă'),
        T(r'Volatility is persistent over months and rough over days ($H \approx 0.1$); level shifts mimic long memory', r'Volatilitatea este persistentă la scara lunilor și rough la scara zilelor ($H \approx 0{,}1$); salturile de nivel imită memoria lungă')],
       [T(r'$f(\lambda) \sim c_f\lambda^{-2d}$, $\gamma(k) \sim c_\gamma k^{2d-1}$; $\E|\ln\sigma_{t+\Delta} - \ln\sigma_t|^q \propto \Delta^{qH}$', r'$f(\lambda) \sim c_f\lambda^{-2d}$, $\gamma(k) \sim c_\gamma k^{2d-1}$; $\E|\ln\sigma_{t+\Delta} - \ln\sigma_t|^q \propto \Delta^{qH}$')],
       [T(r'\refGJR on the S\&P 500: $\hat H$ = @{c10.H} (@{c10.H1} and @{c10.H2} in two halves): \textbf{replicated}; \refQu: $W$ = @{c10.W}, the memory of realised variance survives', r'\refGJR pe S\&P 500: $\hat H$ = @{c10.H} (@{c10.H1} și @{c10.H2} pe cele două jumătăți): \textbf{replicat}; \refQu: $W$ = @{c10.W}, memoria varianței realizate rezistă'),
        T(r'Rough forecasting gain over HAR at 5 days: QLIKE ratio @{c10.rq}, $p$ = @{c10.rqp}: small and horizon-dependent', r'Cîștigul de prognoză rough față de HAR la 5 zile: raportul QLIKE @{c10.rq}, $p$ = @{c10.rqp}: mic și dependent de orizont')],
       [T(r'one bandwidth, one $\hat d$; ``short memory because $H < 1/2$\'\' (roughness and persistence are different properties)', r'o singură lățime de bandă, un singur $\hat d$; „memorie scurtă pentru că $H < 1/2$” (caracterul rough și persistența sînt proprietăți diferite)')])

review(11, ('Spectral and wavelet analysis', 'Analiză spectrală și analiză wavelet'),
       [T('The spectrum decomposes variance by frequency; filters act on it through their squared gain; multitaper gives low leakage and honest bands', 'Spectrul descompune varianța pe frecvențe; filtrele acționează prin pătratul cîștigului; multitaper dă un leakage spectral redus și benzi corecte'),
        T('Wavelets localise variance and co-movement in time and scale; significance needs Monte Carlo and areawise thinking', 'Wavelet-urile localizează varianța și co-mișcarea în timp și pe scale; semnificația cere Monte Carlo și raționament pe arii')],
       [T(r'HP cycle gain $G(\omega) = \dfrac{4\lambda(1 - \cos\omega)^2}{1 + 4\lambda(1 - \cos\omega)^2}$; coherence $\kappa^2(\omega) = |f_{xy}|^2/(f_xf_y)$', r'cîștigul ciclului HP $G(\omega) = \dfrac{4\lambda(1 - \cos\omega)^2}{1 + 4\lambda(1 - \cos\omega)^2}$; coerența $\kappa^2(\omega) = |f_{xy}|^2/(f_xf_y)$')],
       [T(r'\refCN: HP applied to a random walk peaks at @{c11.cn} quarters (@{c11.cny} years; simulation @{c11.cnmc}): \textbf{replicated}', r'\refCN: HP aplicat unui mers aleator are vîrful la @{c11.cn} trimestre (@{c11.cny} ani; simulare @{c11.cnmc}): \textbf{replicat}'),
        T(r'\refHamB on Romanian GDP: the real-time HP gap correlates @{c11.hpc} with the final one and has the wrong sign in @{c11.hps}\% of quarters', r'\refHamB pe PIB-ul României: output gap-ul HP în timp real are corelația @{c11.hpc} cu cel final și semnul greșit în @{c11.hps}\% din trimestre')],
       [T(r'every wavelet-coherence island read as contagion: BET--DAX @{c11.wo}\% significant area against a null 95\% quantile of @{c11.wq}\%', r'fiecare insulă de coerență wavelet citită drept contagiune: BET--DAX @{c11.wo}\% arie semnificativă, față de cuantila de 95\% sub ipoteza nulă @{c11.wq}\%'),
        T('pointwise tests across frequencies read as a joint test', 'teste punctuale pe frecvențe citite drept test comun')])

review(12, ('Machine learning and deep learning', 'Machine learning și deep learning'),
       [T('Validation must respect dependence: K-fold only for well-specified autoregressions; otherwise block, purge and keep a final test period', 'Validarea trebuie să respecte dependența: K-fold doar pentru autoregresii bine specificate; altfel blocuri, purjare și o perioadă finală de test'),
        T('Trees and networks rarely beat strong structured baselines alone; global models pool series; seeds and searches are hidden multiple testing', 'Arborii și rețelele depășesc rar singure modelele de referință structurate; modelele globale combină seriile; seed-urile și căutările sînt testare multiplă ascunsă')],
       [T(r'$\mathrm{OWA} = \frac12\big(\mathrm{sMAPE}/\mathrm{sMAPE}_{\mathrm{Naive2}} + \mathrm{MASE}/\mathrm{MASE}_{\mathrm{Naive2}}\big)$; $\mathrm{Att}(Q, K, V) = \mathrm{softmax}(QK\'/\sqrt{d_k})V$', r'$\mathrm{OWA} = \frac12\big(\mathrm{sMAPE}/\mathrm{sMAPE}_{\mathrm{Naive2}} + \mathrm{MASE}/\mathrm{MASE}_{\mathrm{Naive2}}\big)$; $\mathrm{Att}(Q, K, V) = \mathrm{softmax}(QK\'/\sqrt{d_k})V$')],
       [T(r'\refBHK: 5-fold CV error @{c12.cv} against @{c12.oos} out of sample: \textbf{replicated}', r'\refBHK: eroarea validării 5-fold @{c12.cv}, față de @{c12.oos} în afara eșantionului: \textbf{replicat}'),
        T(r'\refZeng and \refNie on Romanian load, $H = 96$: point-token Transformer @{c12.pt}, DLinear @{c12.dl}, patches @{c12.patch}: both papers \textbf{replicate}', r'\refZeng și \refNie pe consumul de energie al României, $H = 96$: Transformer cu tokeni punctuali @{c12.pt}, DLinear @{c12.dl}, patch-uri @{c12.patch}: ambele lucrări \textbf{se replică}')],
       [T(r'random K-fold with autocorrelated residuals: validation-to-test error ratio @{c12.lk} (leakage)', r'K-fold aleator cu reziduuri autocorelate: raportul dintre eroarea de validare și cea de test @{c12.lk} (leakage)'),
        T('attention weights read as importance; the best of many seeds reported as the model', 'ponderile atenției citite ca importanță; cel mai bun dintre multe seed-uri raportat drept model')])

review(13, ('Foundation models and conformal prediction', 'Foundation models și predicție conformală'),
       [T('Foundation models amortise estimation over a corpus; evaluate after release, pool across series, correct for multiplicity', 'Foundation models amortizează estimarea pe un corpus; evaluați după lansare, agregați pe serii, corectați pentru testarea multiplă'),
        T('Conformal prediction gives finite-sample marginal coverage under exchangeability; under dependence, ACI restores long-run coverage', 'Predicția conformală dă acoperire marginală în eșantion finit sub interschimbabilitate; sub dependență, ACI restabilește acoperirea pe termen lung')],
       [T(r'$\hat q = S_{(\lceil(n + 1)(1 - \alpha)\rceil)}$; ACI: $\alpha_{t+1} = \alpha_t + \gamma(\alpha - \mathrm{err}_t)$', r'$\hat q = S_{(\lceil(n + 1)(1 - \alpha)\rceil)}$; ACI: $\alpha_{t+1} = \alpha_t + \gamma(\alpha - \mathrm{err}_t)$')],
       [T(r'\refGC on the S\&P 500 (target 0.90): static coverage @{c13.st}, ACI @{c13.aci}; \refRPC: raw quantiles @{c13.raw}, CQR @{c13.cqr}: \textbf{replicated}', r'\refGC pe S\&P 500 (ținta 0,90): acoperirea statică @{c13.st}, ACI @{c13.aci}; \refRPC: cuantilele brute @{c13.raw}, CQR @{c13.cqr}: \textbf{replicat}'),
        T(r'Romanian load: Chronos-2 MAE @{c13.c2} against @{c13.arx} for the expert ARX', r'Consumul de energie al României: MAE Chronos-2 @{c13.c2}, față de @{c13.arx} pentru ARX expert')],
       [T(r'cherry-picked countries: Chronos-2 better in @{c13.neg} of 27 inflation series, significant in @{c13.holm} after Holm', r'țări alese convenabil: Chronos-2 mai bun în @{c13.neg} din 27 de serii de inflație, semnificativ în @{c13.holm} după Holm'),
        T('evaluation windows before the model release; conditional coverage claimed instead of tested', 'ferestre de evaluare dinaintea lansării modelului; acoperirea condiționată afirmată în loc de testată')])

if OK14:
    review(14, ('Causal inference for time series', 'Inferență cauzală pentru serii de timp'),
           [T('Granger causality and its relatives (TE, PCMCI, CCM) describe predictive structure; causal claims need assumptions about the assignment', 'Cauzalitatea Granger și metodele înrudite (TE, PCMCI, CCM) descriu structura predictivă; afirmațiile cauzale cer ipoteze despre alocarea tratamentului'),
            T('Synthetic control uses other units: placebos are the inference, a long pre-period fit is the justification', 'Controlul sintetic folosește alte unități: testele placebo sînt inferența, potrivirea pe o perioadă anterioară lungă este justificarea')],
           [T(r'$w^* = \arg\min_w(X_1 - X_0w)\'V(X_1 - X_0w)$, $w_j \ge 0$, $\sum_jw_j = 1$; placebo $p = \#\{j: r_j \ge r_1\}/(J + 1)$', r'$w^* = \arg\min_w(X_1 - X_0w)\'V(X_1 - X_0w)$, $w_j \ge 0$, $\sum_jw_j = 1$; placebo $p = \#\{j: r_j \ge r_1\}/(J + 1)$')],
           [T(r'\refADH: West German GDP per capita @{c14.ge} USD a year (@{c14.gerel}\%) below its synthetic control, placebo $p$ = @{c14.gp}: \textbf{replicated}', r'\refADH: PIB-ul pe locuitor al Germaniei de Vest cu @{c14.ge} USD pe an (@{c14.gerel}\%) sub controlul sintetic, $p$ placebo = @{c14.gp}: \textbf{replicat}'),
            T(r'\refBMSS on revised data: gap $-$@{c14.bx}\% in 2018Q4 (paper $-$@{pub.brexit_gap}\%), UK rank @{c14.rk} of @{c14.nu}: \textbf{not replicated in strength}', r'\refBMSS pe date revizuite: diferența $-$@{c14.bx}\% în T4 2018 (lucrarea: $-$@{pub.brexit_gap}\%), Regatul Unit pe locul @{c14.rk} din @{c14.nu}: \textbf{nereplicat ca mărime}')],
           [T('Granger causality read as causation; a common driver produces it', 'cauzalitatea Granger citită drept cauzalitate; un factor comun o produce'),
            T(r'synthetic control outside the convex hull: classic SC gives @{c14.sc} pp for Romania, the robust estimators @{c14.lo}--@{c14.hi} pp', r'control sintetic în afara înfășurătorii convexe: SC clasic dă @{c14.sc} pp pentru România, estimatorii robuști @{c14.lo}--@{c14.hi} pp')])
else:
    D.frame(T('Chapter 14: Causal inference for time series', 'Capitolul 14: Inferență cauzală pentru serii de timp'), items(
        (IDEA, [T('Granger causality and structural causality; conditional, nonlinear and frequency-domain tests; transfer entropy', 'Cauzalitatea Granger și cauzalitatea structurală; teste condiționate, neliniare și în domeniul frecvenței; entropia de transfer'),
                T('Causal discovery (PCMCI, convergent cross mapping); interrupted time series, synthetic control, CausalImpact', 'Descoperirea relațiilor cauzale (PCMCI, convergent cross mapping); serii de timp întrerupte, control sintetic, CausalImpact')]),
        (MIST, [T('Granger causality read as causation', 'cauzalitatea Granger citită drept cauzalitate')])), 'footnotesize')

review(16, ('Explosive roots and bubbles (self-study)', 'Rădăcini explozive și bule speculative (studiu individual)'),
       [T('A rational bubble is an explosive component; periodically collapsing bubbles hide from whole-sample tests', 'O bulă rațională este o componentă explozivă; bulele care se prăbușesc periodic scapă testelor pe întregul eșantion'),
        T('Critical values must match the design: wild bootstrap under changing volatility, family-wise control for date-stamping', 'Valorile critice trebuie să corespundă designului: wild bootstrap sub volatilitate variabilă, control la nivel de familie pentru datare')],
       [T(r'$\mathrm{BSADF}_{r_2} = \sup_{r_1}\mathrm{ADF}_{r_1}^{r_2}$, $\mathrm{GSADF} = \sup_{r_2}\mathrm{BSADF}_{r_2}$; bubble: $\E_tB_{t+1} = (1 + r)B_t$', r'$\mathrm{BSADF}_{r_2} = \sup_{r_1}\mathrm{ADF}_{r_1}^{r_2}$, $\mathrm{GSADF} = \sup_{r_2}\mathrm{BSADF}_{r_2}$; bula: $\E_tB_{t+1} = (1 + r)B_t$')],
       [T(r'\refPY: US price-to-rent GSADF @{c16.hg} against the wild critical value @{c16.hcv}: \textbf{replicated}', r'\refPY: raportul preț/chirie în SUA, GSADF @{c16.hg}, față de valoarea critică wild @{c16.hcv}: \textbf{replicat}'),
        T(r'\refPWY Nasdaq: @{c16.ndx.g} rejects with Monte Carlo (@{c16.ndx.mc}) but not with the wild bootstrap (@{c16.ndx.w}); \refPSY S\&P 500: @{c16.sp500.g} below both: \textbf{not replicated}', r'\refPWY Nasdaq: @{c16.ndx.g} respinge cu valoarea Monte Carlo (@{c16.ndx.mc}), dar nu cu wild bootstrap (@{c16.ndx.w}); \refPSY S\&P 500: @{c16.sp500.g} sub ambele: \textbf{nereplicat}')],
       [T(r'Monte Carlo critical values after a volatility shift: size @{c16.szmc}\% (wild bootstrap @{c16.szw}\%)', r'valori critice Monte Carlo după o schimbare a volatilității: mărimea @{c16.szmc}\% (wild bootstrap @{c16.szw}\%)'),
        T(r'pointwise date-stamping read as a 5\% test: false episodes in @{c16.ep}\% of no-bubble paths', r'datarea punctuală citită ca test de 5\%: episoade false în @{c16.ep}\% din traiectoriile fără bulă')])

D.recap(('the sixteen chapters', 'cele șaisprezece capitole'), [
    T('Most landmark results replicate in direction on today\'s data; their strength and their tests often do not', 'Majoritatea rezultatelor de referință se replică în sens pe datele de azi; mărimea și testele lor adesea nu'),
    T('The same mistakes recur: i.i.d.\\ inference on dependent data, the wrong critical values, a search reported as one test', 'Aceleași greșeli revin: inferență i.i.d.\\ pe date dependente, valori critice greșite, o căutare raportată ca un singur test'),
    T('Every chapter offers a replication and an extension for the project (Appendix)', 'Fiecare capitol oferă o replicare și o extensie pentru proiect (Anexă)')])

# =============================================================================
# TRUSA DE METODE
# =============================================================================
D.section('The methods toolbox', 'Trusa de metode')

QH = T(r'\textbf{Research question}', r'\textbf{Întrebarea de cercetare}') + ' & ' + T(r'\textbf{Tool}', r'\textbf{Instrumentul}') + ' & ' + T(r'\textbf{Ch.}', r'\textbf{Cap.}')
SPEC = TB + 'p{4.9cm}' + TB + 'p{5.6cm}' + TB + 'p{0.8cm}'

D.frame(T('Which tool for which question (1/3): inference and evaluation', 'Instrumentul potrivit fiecărei întrebări (1/3): inferență și evaluare'), table(SPEC, QH, [
    T('Is a mean, a slope or a predictive coefficient different from zero?', 'Este o medie, o pantă sau un coeficient predictiv diferit de zero?') + ' & ' + T('HAC with fixed-$b$ or EWC; block bootstrap; Monte Carlo size check', 'HAC cu fixed-$b$ sau EWC; bootstrap pe blocuri; verificarea mărimii prin Monte Carlo') + ' & 0',
    T('Does one of many rules or models beat a benchmark?', 'Depășește una dintre multe reguli sau modele un reper?') + ' & ' + T('Reality Check, SPA, StepM; MCS', 'Reality Check, SPA, StepM; MCS') + ' & 0, 1',
    T('Is forecast A more accurate than forecast B?', 'Este prognoza A mai precisă decît prognoza B?') + ' & ' + T('DM--HLN with HAC; Clark--West if nested; Giacomini--White for methods', 'DM--HLN cu HAC; Clark--West pentru modele imbricate; Giacomini--White pentru metode') + ' & 1',
    T('Is a density or interval forecast calibrated?', 'Este calibrată o prognoză de densitate sau de interval?') + ' & ' + T('PIT, Berkowitz; coverage and independence tests; CRPS, log score', 'PIT, Berkowitz; teste de acoperire și independență; CRPS, scorul logaritmic') + ' & 1, 13',
    T('Is a VaR or (VaR, ES) forecast adequate, and which is best?', 'Este adecvată o prognoză VaR sau (VaR, ES) și care este cea mai bună?') + ' & ' + T('Kupiec, Christoffersen, DQ; FZ0 loss, DM, MCS, Murphy diagrams', 'Kupiec, Christoffersen, DQ; pierderea FZ0, DM, MCS, diagrame Murphy') + ' & 9',
    T('Do my intervals keep their coverage under dependence?', 'Își păstrează intervalele acoperirea sub dependență?') + ' & ' + T('split conformal, CQR, ACI, conformal PID; coverage by regime', 'split conformal, CQR, ACI, PID conformal; acoperire pe regimuri') + ' & 13'],
    size='footnotesize'), 'small')

D.frame(T('Which tool for which question (2/3): structure and dynamics', 'Instrumentul potrivit fiecărei întrebări (2/3): structură și dinamică'), table(SPEC, QH, [
    T('Did the parameters change, and when?', 'S-au schimbat parametrii și cînd?') + ' & ' + T('sup/exp/ave tests, Bai--Perron, CSW monitoring, variance-break tests', 'teste sup/exp/ave, Bai--Perron, monitorizare CSW, teste pentru rupturi în varianță') + ' & 2',
    T('Is the dynamics nonlinear or state-dependent?', 'Este dinamica neliniară sau dependentă de stare?') + ' & ' + T('TAR, STAR with bootstrap or LM tests; Markov switching with bootstrap LR', 'TAR, STAR cu teste bootstrap sau LM; schimbare de regim Markov cu LR bootstrap') + ' & 2, 7',
    T('What is the effect of a structural shock?', 'Care este efectul unui șoc structural?') + ' & ' + T('SVAR (zeros, signs, proxies), local projections, LP-IV', 'SVAR (zerouri, semne, proxy), proiecții locale, LP-IV') + ' & 3',
    T('Is there a long-run equilibrium, and who adjusts?', 'Există un echilibru pe termen lung și cine se ajustează?') + ' & ' + T('Johansen with bootstrap; tests on $\\beta$ and $\\alpha$; ARDL bounds; panel CCE and PMG', 'Johansen cu bootstrap; teste pe $\\beta$ și $\\alpha$; testul limitelor ARDL; CCE și PMG pentru panel') + ' & 4',
    T('How to forecast with many predictors or mixed frequencies?', 'Cum prognozăm cu mulți predictori sau frecvențe mixte?') + ' & ' + T('BVAR with optimised shrinkage, factors, DFM nowcasting, MIDAS', 'BVAR cu shrinkage optimizat, factori, nowcasting DFM, MIDAS') + ' & 5',
    T('What is the unobserved trend, gap or time-varying slope?', 'Care este trendul, output gap-ul sau panta variabilă neobservate?') + ' & ' + T('state space by ML or Gibbs, simulation smoother, UC-SV, particle filters', 'spațiul stărilor prin verosimilitate maximă sau Gibbs, netezire prin simulare, UC-SV, filtre de particule') + ' & 6'],
    size='footnotesize'), 'small')

D.frame(T('Which tool for which question (3/3): volatility, frequency, learning, causality', 'Instrumentul potrivit fiecărei întrebări (3/3): volatilitate, frecvență, învățare, cauzalitate'), table(SPEC, QH, [
    T('How to forecast volatility or a covariance matrix?', 'Cum prognozăm volatilitatea sau o matrice de covarianță?') + ' & ' + T('HAR, HARQ, Realized GARCH; DCC with shrinkage; QLIKE', 'HAR, HARQ, Realized GARCH; DCC cu shrinkage; QLIKE') + ' & 8',
    T('Is the memory long, or is it shifts?', 'Este memoria lungă sau sînt salturi de nivel?') + ' & ' + T('local Whittle $\\hat d(m)$, Qu test, scaling of log volatility', 'local Whittle $\\hat d(m)$, testul Qu, scalarea logaritmului volatilității') + ' & 10',
    T('At which frequencies do two series move together?', 'La ce frecvențe se mișcă împreună două serii?') + ' & ' + T('multitaper coherence and phase, Breitung--Candelon, wavelet coherence', 'coerență și fază multitaper, Breitung--Candelon, coerență wavelet') + ' & 11',
    T('Do flexible learners or foundation models beat the baseline?', 'Depășesc metodele flexibile sau foundation models reperul?') + ' & ' + T('blocked validation, strong baselines, pooled tests, Holm and BH', 'validare pe blocuri, repere puternice, teste agregate, Holm și BH') + ' & 12, 13',
    T('Does $x$ help predict $y$, and did a policy have an effect?', 'Ajută $x$ la prognoza lui $y$ și a avut o politică un efect?') + ' & ' + T('conditional Granger, PCMCI; ITS, synthetic control with placebos, CausalImpact', 'Granger condiționat, PCMCI; ITS, control sintetic cu placebo, CausalImpact') + ' & 14',
    T('Is there a bubble, and when did it start?', 'Există o bulă și cînd a început?') + ' & ' + T('GSADF and BSADF with wild bootstrap, family-wise dating', 'GSADF și BSADF cu wild bootstrap, datare cu control la nivel de familie') + ' & 16'],
    size='footnotesize'), 'small')

# =============================================================================
# FLUXUL DE CERCETARE
# =============================================================================
D.section('The research workflow', 'Fluxul de cercetare')

STEPS = [('Question', 'Întrebarea'), ('Literature', 'Literatura'), ('Pre-registration', 'Preînregistrarea'), ('Data', 'Datele'),
         ('Replication', 'Replicarea'), ('Extension', 'Extensia'), ('Robustness', 'Robustețea'), ('Reporting', 'Raportarea')]
FLOW = ('\\begin{center}\n\\begin{tikzpicture}[font=\\scriptsize, st/.style={draw=MainBlue, rounded corners=3pt, fill=MainBlue!6, '
        'minimum width=2.6cm, minimum height=0.8cm, align=center}, ar/.style={-{Stealth[length=1.8mm]}, MainBlue!70, thick}]\n')
for i, (en, ro) in enumerate(STEPS):
    x = (i if i < 4 else 7 - i) * 3.2
    y = 0 if i < 4 else -1.5
    FLOW += f'\\node[st] (s{i}) at ({x},{y}) {{\\textbf{{{i + 1}}}. {T(en, ro)}}};\n'
FLOW += ('\\draw[ar] (s0) -- (s1); \\draw[ar] (s1) -- (s2); \\draw[ar] (s2) -- (s3); \\draw[ar] (s3) -- (s4); '
         '\\draw[ar] (s4) -- (s5); \\draw[ar] (s5) -- (s6); \\draw[ar] (s6) -- (s7);\n'
         f'\\draw[decorate, decoration={{brace, amplitude=4pt}}, IDAred] (-1.3,0.6) -- (7.7,0.6) node[midway, above=4pt, text=IDAred] {{{T("proposal and pre-registration: 5%", "propunerea și preînregistrarea: 5%").replace("%", chr(92) + "%")}}};\n'
         f'\\draw[decorate, decoration={{brace, amplitude=4pt, mirror}}, IDAred] (-1.3,-2.1) -- (10.9,-2.1) node[midway, below=4pt, text=IDAred] {{{T("repository, report, AI_USE.md, AI_ERRORS.md: 15%; defence of every step: 50%", "repository, raport, AI_USE.md, AI_ERRORS.md: 15%; susținerea fiecărei etape: 50%").replace("%", chr(92) + "%").replace("_", chr(92) + "_")}}};\n'
         '\\end{tikzpicture}\n\\end{center}\n')
D.frame(T('The project in eight steps', 'Proiectul în opt etape'), FLOW + items(
    T('The order matters: the evaluation design is fixed before the first estimate, the replication comes before the extension', 'Ordinea contează: designul evaluării se fixează înaintea primei estimări, replicarea vine înaintea extensiei'),
    T('Each step leaves a trace in the repository (a file, a commit, a section of the report)', 'Fiecare etapă lasă o urmă în repository (un fișier, un commit, o secțiune a raportului)')), 'small')

D.frame(T('Steps 1--2: the question and the literature', 'Etapele 1--2: întrebarea și literatura'), items(
    (T(r'\textbf{A good question} is narrow, falsifiable and answerable with public data', r'\textbf{O întrebare bună} este îngustă, falsificabilă și are răspuns cu date publice'),
     [T('``Does the Meese--Rogoff result hold for EUR/RON at horizons of 1--12 months after 2015?\'\' rather than ``Can we forecast exchange rates?\'\'', '„Se menține rezultatul Meese--Rogoff pentru EUR/RON la orizonturi de 1--12 luni după 2015?” în loc de „Putem prognoza cursul de schimb?”')]),
    (T(r'\textbf{The landmark paper}: one of the case studies of Chapters 0--16, or another paper approved in advance', r'\textbf{Lucrarea de referință}: unul dintre studiile de caz ale Capitolelor 0--16 sau o altă lucrare aprobată în prealabil'),
     [T('identify the table or figure you will reproduce, the sample, the data source and the code, if published', 'identificați tabelul sau figura pe care le veți reproduce, eșantionul, sursa datelor și codul, dacă este publicat')]),
    (T(r'\textbf{The literature}: what was found since, and what is still open', r'\textbf{Literatura}: ce s-a găsit de atunci și ce rămîne deschis'),
     [T('every reference checked against its DOI; an AI-suggested reference is a hypothesis until verified \\refWW', 'fiecare referință verificată după DOI; o referință sugerată de AI este o ipoteză pînă la verificare \\refWW')]),
    T('The extension answers a new question: new data (Romania, the EU, recent years), a new method from the course, or a new test', 'Extensia răspunde unei întrebări noi: date noi (România, UE, anii recenți), o metodă nouă din curs sau un test nou')), 'small')

D.frame(T('Step 3: the pre-registration', 'Etapa 3: preînregistrarea'), items(
    (T(r'A pre-registration fixes the analysis before the data can influence it \refNos', r'Preînregistrarea fixează analiza înainte ca datele să o poată influența \refNos'),
     [T('the hypotheses and the primary outcome', 'ipotezele și rezultatul principal'),
      T('the data: sources, vintages, sample, transformations, exclusions', 'datele: surse, ediții, eșantion, transformări, excluderi'),
      T('the evaluation: estimation and test windows, horizons, losses, tests, the benchmark', 'evaluarea: ferestrele de estimare și de test, orizonturile, funcțiile de pierdere, testele, reperul'),
      T('the multiplicity plan: how many comparisons, which correction (\\refHolm, MCS, SPA)', 'planul pentru testarea multiplă: cîte comparații, ce corecție (\\refHolm, MCS, SPA)'),
      T('the robustness rule: which variations, and what counts as a robust result', 'regula de robustețe: ce variații și ce înseamnă un rezultat robust')]),
    T(r'A power calculation for the evaluation: is the test sample long enough to detect the published gain? (mini-case at the end)', r'Un calcul al puterii evaluării: este eșantionul de test destul de lung pentru a detecta cîștigul publicat? (mini studiul de caz de la final)'),
    T('Deviations are allowed but reported: the pre-registration is a commitment to transparency, not a prison', 'Abaterile sînt permise, dar se raportează: preînregistrarea este un angajament de transparență, nu o constrîngere rigidă'),
    T('A template with the seven sections (Appendix) % applink: a pre-registration template', 'Un model cu cele șapte secțiuni (Anexă) % applink: un model de preînregistrare')), 'small')

D.frame(T('Steps 4--6: data, replication, extension', 'Etapele 4--6: datele, replicarea, extensia'), items(
    (T(r'\textbf{Data}: official sources, documented once', r'\textbf{Datele}: surse oficiale, documentate o singură dată'),
     [T('market data from the course repository (EODHD); FRED, Eurostat, ECB, INS, BNR online; record the download date (vintage)', 'date de piață din repository-ul cursului (EODHD); FRED, Eurostat, BCE, INS, BNR online; notați data descărcării (ediția)'),
      T('real-time questions need real-time data: revised data flatter forecasts (Chapters 1 and 5)', 'întrebările în timp real cer date în timp real: datele revizuite avantajează prognozele (Capitolele 1 și 5)')]),
    (T(r'\textbf{Replication}: first the original sample and specification, then today\'s data', r'\textbf{Replicarea}: întîi eșantionul și specificația originale, apoi datele de azi'),
     [T('a table that puts the published numbers next to yours, with the differences explained', 'un tabel care pune rezultatele publicate lîngă ale dumneavoastră, cu diferențele explicate')]),
    (T(r'\textbf{Extension}: one new question, answered with the same care', r'\textbf{Extensia}: o singură întrebare nouă, tratată cu aceeași grijă'),
     [T('new sample, new country, new method of the course, or a stronger test of the original claim', 'eșantion nou, țară nouă, o metodă nouă din curs sau un test mai puternic al afirmației originale')])), 'small')

D.frame(T('Steps 7--8: robustness and reporting', 'Etapele 7--8: robustețea și raportarea'), items(
    (T(r'\textbf{Robustness}: show the distribution of results over reasonable choices, not the best one', r'\textbf{Robustețea}: arătați distribuția rezultatelor pe alegeri rezonabile, nu pe cea mai bună'),
     [T('specification curve or multiverse \\refSSN, \\refSte: windows, lags, donor pools, losses, bandwidths', 'curba specificațiilor sau multiversul \\refSSN, \\refSte: ferestre, laguri, grupuri de donatori, funcții de pierdere, lățimi de bandă'),
      T('164 teams testing the same hypotheses on the same data disagree as much as the standard errors suggest \\refMen', '164 de echipe care testează aceleași ipoteze pe aceleași date diferă cît sugerează erorile standard \\refMen')]),
    (T(r'\textbf{Report} in the form of a paper: introduction, data, method, replication, extension, robustness, conclusion', r'\textbf{Raportul} în forma unui articol: introducere, date, metodă, replicare, extensie, robustețe, concluzie'),
     [T('every number in the text produced by the code; figures with the course chart rules', 'fiecare rezultat numeric din text produs de cod; figurile după regulile de grafice ale cursului'),
      T('effect sizes with confidence intervals, not stars; limits stated explicitly', 'mărimi ale efectelor cu intervale de încredere, nu steluțe; limitele formulate explicit')]),
    T('AI\\_USE.md and AI\\_ERRORS.md in the repository (section on AI in research)', 'AI\\_USE.md și AI\\_ERRORS.md în repository (secțiunea despre AI în cercetare)')), 'small')

D.recap(('the research workflow', 'fluxul de cercetare'), [
    T('Question, literature and pre-registration come before any estimate', 'Întrebarea, literatura și preînregistrarea preced orice estimare'),
    T('Replicate on the original sample first; extend with one new question', 'Replicați întîi pe eșantionul original; extindeți cu o singură întrebare nouă'),
    T('Report the distribution over specifications and every deviation from the plan', 'Raportați distribuția pe specificații și orice abatere de la plan')])

# =============================================================================
# REPLICAREA UNEI LUCRĂRI DE REFERINȚĂ
# =============================================================================
D.section('Replicating a landmark paper', 'Replicarea unei lucrări de referință')

D.frame(T('Reproduction, replication, robustness', 'Reproducere, replicare, robustețe'), items(
    (T(r'\refCle distinguishes', r'\refCle distinge'),
     [T(r'\textbf{verification}: same data, same code, same numbers (a computational check)', r'\textbf{verificarea}: aceleași date, același cod, aceleași rezultate (un control de calcul)'),
      T(r'\textbf{reproduction}: same specification and population, re-coded or with re-collected data', r'\textbf{reproducerea}: aceeași specificație și populație, cu cod rescris sau date recolectate'),
      T(r'\textbf{robustness}: a different specification, sample or population: an extension, not a failure if it differs', r'\textbf{robustețea}: altă specificație, alt eșantion sau altă populație: o extensie, nu un eșec dacă diferă')]),
    T(r'In economics, about half of the papers can be reproduced from the authors\' files without their help \refCL; anomalies in finance often fail on extended samples \refHXZ', r'În economie, aproximativ jumătate din lucrări pot fi reproduse din fișierele autorilor fără ajutorul lor \refCL; anomaliile din finanțe eșuează adesea pe eșantioane extinse \refHXZ'),
    T(r'A spreadsheet error changed a policy debate: \refHAP', r'O eroare într-o foaie de calcul a schimbat o dezbatere de politică economică: \refHAP'),
    T('In the course, almost every replication was a reproduction on today\'s data, followed by a robustness check', 'În curs, aproape fiecare replicare a fost o reproducere pe datele de azi, urmată de o verificare a robusteții')), 'small')

VERD = {'r': T('replicated', 'replicat'), 'p': T('partly', 'parțial'), 'n': T('not replicated', 'nereplicat')}
SH = T(r'\textbf{Paper}', r'\textbf{Lucrarea}') + r' & \textbf{' + T('Ch.', 'Cap.') + r'} & \textbf{' + T('Verdict', 'Verdict') + r'} & \textbf{' + T('What decided it', 'Ce a decis') + '}'
SSPEC = TB + 'p{4.3cm}l' + TB + 'p{1.7cm}' + TB + 'p{6.2cm}'
D.frame(T('Scoreboard of the course replications (1/2)', 'Tabloul replicărilor din curs (1/2)'), table(SSPEC, SH, [
    r'\refEH & 0 & ' + VERD['p'] + ' & ' + T('robust inference and a later sample remove the significance', 'inferența robustă și un eșantion mai recent elimină semnificația'),
    r'\refMR, \refGKMT & 1 & ' + VERD['r'] + ' & ' + T('random walk and the simple average are hard to beat', 'mersul aleator și media simplă sînt greu de depășit'),
    r'\refMPQ, \refBP & 2 & ' + VERD['r'] + ' & ' + T('dates reproduced; the 2020 outliers weaken the extension', 'datele reproduse; valorile extreme din 2020 slăbesc extensia'),
    r'\refHanB & 2 & ' + VERD['p'] + ' & ' + T('threshold close, delay fragile on revised data', 'pragul apropiat, lagul variabilei de prag fragil pe date revizuite'),
    r'\refTPS & 2 & ' + VERD['n'] + ' & ' + T('Monte Carlo p-value; the price index of the paper is not published today', 'p-value-ul Monte Carlo; indicele de preț din lucrare nu mai este publicat azi'),
    r'\refCEE, \refKil, \refGK & 3 & ' + VERD['r'] + ' & ' + T('public replication files; same identification', 'fișiere de replicare publice; aceeași identificare'),
    r'\refKPSW & 4 & ' + VERD['p'] + ' & ' + T('rank reproduced, great ratios depend on the deterministic case', 'rangul reprodus, rapoartele mari depind de cazul determinist'),
    r'\refBGR & 5 & ' + VERD['r'] + ' & ' + T('to 2003; fails after 2020 without stochastic volatility', 'pînă în 2003; eșuează după 2020 fără volatilitate stochastică'),
    r'\refSW & 5 & ' + VERD['p'] + ' & ' + T('gains vanish on 1999--2019', 'cîștigurile dispar pe 1999--2019'),
    r'\refMNZ, \refHam & 6, 7 & ' + VERD['r'] + ' & ' + T('same data; Hamilton\'s dating does not survive today\'s sample', 'aceleași date; datarea lui Hamilton nu rezistă pe eșantionul de azi')],
    size='scriptsize'), 'small')

D.frame(T('Scoreboard of the course replications (2/2)', 'Tabloul replicărilor din curs (2/2)'), table(SSPEC, SH, [
    r'\refBPQ & 8 & ' + VERD['r'] + ' & ' + T('in QLIKE; the ranking changes in MSE', 'în QLIKE; ierarhia se schimbă în MSE'),
    r'\refEGS & 8 & ' + VERD['p'] + ' & ' + T('the sign survives, the macro effect is not significant', 'semnul rezistă, efectul macro nu este semnificativ'),
    r'\refELW & 8 & ' + VERD['n'] + ' & ' + T('few assets relative to the sample: shrinkage has little to do', 'puține active raportat la eșantion: shrinkage-ul are puțin de corectat'),
    r'\refPZC & 9 & ' + VERD['p'] + ' & ' + T('average losses reproduced; tests on a few tail days do not', 'pierderile medii reproduse; testele pe cîteva zile din coadă nu'),
    r'\refGJR, \refQu & 10 & ' + VERD['r'] + ' & ' + T('scaling stable across halves and markets', 'scalarea stabilă pe jumătăți ale eșantionului și pe piețe'),
    r'\refCN, \refHamB & 11 & ' + VERD['r'] + ' & ' + T('a property of the filter, not of the data', 'o proprietate a filtrului, nu a datelor'),
    r'\refBHK, \refZeng & 12 & ' + VERD['r'] + ' & ' + T('protocols reproduced on Romanian load', 'protocoalele reproduse pe consumul de energie al României'),
    r'\refGC, \refRPC & 13 & ' + VERD['r'] + ' & ' + T('finite-sample guarantees hold by construction', 'garanțiile în eșantion finit sînt valabile prin construcție'),
    r'\refADH & 14 & ' + VERD['r'] + ' & ' + T('public data and code; weights to two decimals', 'date și cod publice; ponderi identice la două zecimale'),
    r'\refBMSS & 14 & ' + VERD['n'] + ' & ' + T('data revisions, no covariates, permutation inference', 'revizuirea datelor, fără covariate, inferență prin permutare'),
    r'\refPY; \refPSY & 16 & ' + VERD['r'] + '; ' + VERD['n'] + ' & ' + T('wild bootstrap critical values decide', 'valorile critice wild bootstrap decid')],
    size='scriptsize'), 'small')

chart(T('A replication that worked: Patton, Ziegel and Chen (2019)', 'O replicare reușită: Patton, Ziegel și Chen (2019)'), 'ats_ch9_pzc_table', 'ATS_ch9_pzc', [
    T(r'Average FZ0 loss of ten (VaR, ES) models, S\&P 500, 2000--2016, the design of \refPZC: our data (bars) against their Table 8 (diamonds)', r'Pierderea FZ0 medie a zece modele (VaR, ES), S\&P 500, 2000--2016, designul \refPZC: datele noastre (bare), față de tabelul 8 al lucrării (romburi)')],
    h='0.62\\textheight', ch=9)

interp(('the two kinds of outcome', 'celor două tipuri de rezultat'), [
    T(r'Average losses over 4\,000 days are robust to small data differences: GAS-1F @{c9.loss} against @{pub.pzc_loss}', r'Pierderile medii pe 4\,000 de zile sînt robuste la mici diferențe de date: GAS-1F @{c9.loss}, față de @{pub.pzc_loss}'),
    T(r'Tests that rest on a few dozen tail days are not: goodness-of-fit $p$ = @{c9.gv} against @{pub.pzc_gof_var}', r'Testele care se bazează pe cîteva zeci de zile din coadă nu sînt: p-value-ul testului de adecvare @{c9.gv}, față de @{pub.pzc_gof_var}'),
    T(r'The same pattern in Chapter 2 (\refTPS: $p$ = @{c2.tpsp} against @{pub.tps_p}) and Chapter 14 (\refBMSS: $-$@{c14.bx}\% against $-$@{pub.brexit_gap}\%)' if OK14 else r'The same pattern in Chapter 2 (\refTPS: $p$ = @{c2.tpsp} against @{pub.tps_p})',
      r'Același tipar în Capitolul 2 (\refTPS: $p$ = @{c2.tpsp}, față de @{pub.tps_p}) și în Capitolul 14 (\refBMSS: $-$@{c14.bx}\%, față de $-$@{pub.brexit_gap}\%)' if OK14 else r'Același tipar în Capitolul 2 (\refTPS: $p$ = @{c2.tpsp}, față de @{pub.tps_p})'),
    T('Lesson: replicate the estimate and the inference separately; report which of the two survives', 'Lecția: replicați separat estimația și inferența; raportați care dintre ele rezistă')])

D.frame(T('Five sources of discrepancy', 'Cinci surse de diferențe'), items(
    (T(r'\textbf{Data vintage}: revised GDP, rebased price indices, series that no longer exist', r'\textbf{Ediția datelor}: PIB revizuit, indici de preț cu altă bază, serii care nu mai există'),
     [T('Brexit gap (Chapter 14), the UK CPI of TPS (Chapter 2), the decimals of MNZ (Chapter 6)', 'diferența Brexit (Capitolul 14), IPC-ul britanic din TPS (Capitolul 2), zecimalele MNZ (Capitolul 6)')]),
    (T(r'\textbf{Sample}: the effect was a feature of its period', r'\textbf{Eșantionul}: efectul era o trăsătură a perioadei lui'),
     [T('the term spread (Chapter 0), diffusion indexes (Chapter 5), Hamilton\'s recessions (Chapter 7)', 'marja la termen (Capitolul 0), indicii de difuzie (Capitolul 5), recesiunile lui Hamilton (Capitolul 7)')]),
    (T(r'\textbf{Implementation}: optimiser, starting values, default options, the deterministic case', r'\textbf{Implementarea}: optimizatorul, valorile de start, opțiunile implicite, cazul determinist'),
     [T('EM maxima (Chapter 7), the great ratios (Chapter 4), diffuse initialisation (Chapter 6)', 'maximele EM (Capitolul 7), rapoartele mari (Capitolul 4), inițializarea difuză (Capitolul 6)')]),
    (T(r'\textbf{Inference}: the estimate survives, its standard error or critical value does not', r'\textbf{Inferența}: estimația rezistă, eroarea standard sau valoarea critică nu'),
     [T('fixed-$b$ (Chapter 0), goodness-of-fit tests (Chapter 9), wild bootstrap (Chapter 16)', 'fixed-$b$ (Capitolul 0), testele de adecvare (Capitolul 9), wild bootstrap (Capitolul 16)')]),
    (T(r'\textbf{Design}: the setting of the paper differs from yours', r'\textbf{Designul}: cadrul lucrării diferă de al dumneavoastră'),
     [T('dimension relative to sample for DCC-NL (Chapter 8); the loss function for HARQ (Chapter 8)', 'dimensiunea raportată la eșantion pentru DCC-NL (Capitolul 8); funcția de pierdere pentru HARQ (Capitolul 8)')])), 'footnotesize')

D.frame(T('How to replicate well', 'Replicarea corectă'), items(
    T('Obtain the replication package; if none exists, write down every choice the paper leaves open', 'Obțineți pachetul de replicare; dacă nu există, notați fiecare alegere lăsată deschisă de lucrare'),
    T('Reproduce one number first (a coefficient, a test statistic), then the table, then the figure', 'Reproduceți întîi un singur rezultat (un coeficient, o statistică de test), apoi tabelul, apoi figura'),
    T('Keep the original sample as a separate run before extending it; change one thing at a time', 'Păstrați eșantionul original ca rulare separată înainte de a-l extinde; schimbați un singur lucru odată'),
    T('Use two implementations when possible (your code and a package), as for Hamilton\'s model in Chapter 7', 'Folosiți două implementări cînd este posibil (codul propriu și un pachet), ca pentru modelul lui Hamilton în Capitolul 7'),
    T('Put published and replicated numbers side by side, with the absolute and relative differences', 'Puneți rezultatele publicate și cele replicate alături, cu diferențele absolute și relative'),
    T('A failed replication is a result: report the source of the difference, test the competing explanations, contact the authors politely if needed', 'O replicare nereușită este un rezultat: raportați sursa diferenței, testați explicațiile concurente, contactați politicos autorii dacă este nevoie')))

# =============================================================================
# REPRODUCTIBILITATEA
# =============================================================================
D.section('The reproducibility checklist', 'Lista de verificare a reproductibilității')

TREE = table(TB + 'p{5.4cm}' + TB + 'p{6.8cm}', T(r'\textbf{Path}', r'\textbf{Calea}') + ' & ' + T(r'\textbf{Content}', r'\textbf{Conținut}'), [
    r'\texttt{README.md} & ' + T('question, data statement, how to run, run time', 'întrebarea, descrierea datelor, modul de rulare, durata'),
    r'\texttt{requirements.txt} & ' + T('package versions', 'versiunile pachetelor'),
    r'\texttt{data/raw/}, \texttt{data/processed/} & ' + T('raw files never edited by hand', 'fișierele brute nu se editează manual'),
    r'\texttt{code/01\_data.py}, \texttt{02\_replication.py}, \dots & ' + T('numbered scripts, run in order', 'scripturi numerotate, rulate în ordine'),
    r'\texttt{notebooks/main.ipynb} & ' + T('runs in Colab from start to end', 'rulează integral în Colab'),
    r'\texttt{output/tables/}, \texttt{output/figures/} & ' + T('generated by the code, never typed', 'generate de cod, niciodată scrise de mînă'),
    r'\texttt{report/report.pdf} & ' + T('the paper', 'articolul'),
    r'\texttt{preregistration.md}, \texttt{AI\_USE.md}, \texttt{AI\_ERRORS.md} & ' + T('the plan and the AI record', 'planul și evidența folosirii AI')],
    size='scriptsize')
D.frame(T('The repository', 'Repository-ul'), TREE + '\n\\vspace{2mm}\n' + items(
    T(r'The structure follows the data editors of economics journals \refVil; replication packages are now a condition of publication \refCM', r'Structura urmează cerințele editorilor de date ai revistelor de economie \refVil; pachetele de replicare sînt acum o condiție de publicare \refCM'),
    T('The preregistration.md file is committed before the first estimation commit: the history shows it', 'Fișierul preregistration.md este salvat (commit) înaintea primului commit cu estimări: istoricul o arată')), 'small')

D.frame(T('Reproducibility checklist', 'Lista de verificare a reproductibilității'), cols(
    block(T('Data and code', 'Date și cod'), items(
        T('every series: source, code, download date', 'fiecare serie: sursa, codul, data descărcării'),
        T('no manual step between raw data and results', 'niciun pas manual între datele brute și rezultate'),
        T('one command or one notebook runs everything', 'o singură comandă sau un singur notebook rulează totul'),
        T('random seeds fixed and reported; results stable across seeds', 'seed-urile fixate și raportate; rezultatele stabile la schimbarea seed-ului'),
        T('functions tested on a case with a known answer (a simulated process, a published number)', 'funcțiile testate pe un caz cu răspuns cunoscut (un proces simulat, un rezultat publicat)'))),
    block(T('Numbers and report', 'Rezultate și raport'), items(
        T('every number in the report traceable to a file in output/', 'fiecare rezultat din raport provine dintr-un fișier din output/'),
        T('package versions in requirements.txt', 'versiunile pachetelor în requirements.txt'),
        T('the clean-machine test: a colleague clones and gets the same numbers \\refPeng', 'testul calculatorului curat: un coleg clonează repository-ul și obține aceleași rezultate \\refPeng'),
        T('deviations from the pre-registration listed', 'abaterile de la preînregistrare enumerate'),
        T('AI\\_USE.md and AI\\_ERRORS.md complete', 'AI\\_USE.md și AI\\_ERRORS.md complete'))), '0.48', '0.48'), 'small')

# =============================================================================
# ERORI FRECVENTE
# =============================================================================
D.section('Failure modes', 'Erori frecvente')

D.frame(T('Data snooping and p-hacking', 'Data snooping și p-hacking'), items(
    (T(r'\textbf{Data snooping}: the same data are used to choose and to test a model; the reported p-value ignores the search \refWhite', r'\textbf{Data snooping}: aceleași date se folosesc pentru a alege și pentru a testa un model; p-value-ul raportat ignoră căutarea \refWhite'),
     [T('remedies: Reality Check, SPA \\refHansen, StepM \\refRW, MCS \\refHLNa, a hold-out period never touched', 'remedii: Reality Check, SPA \\refHansen, StepM \\refRW, MCS \\refHLNa, o perioadă rezervată, neatinsă')]),
    (T(r'\textbf{p-hacking}: undisclosed flexibility (samples, controls, transformations, outliers) until $p < 0.05$ \refSNS', r'\textbf{p-hacking}: flexibilitate nedeclarată (eșantioane, variabile de control, transformări, valori extreme) pînă cînd $p < 0{,}05$ \refSNS'),
     [T('the ``garden of forking paths\'\': no conscious search is needed, data-dependent choices suffice \\refGL', '„grădina potecilor care se bifurcă”: nu este nevoie de o căutare conștientă, ajung alegerile dependente de date \\refGL'),
      T('published $z$-statistics bunch just above 1.96 \\refBLSZ; in finance, a new factor needs $t > 3$ \\refHLZ', 'statisticile $z$ publicate se aglomerează imediat peste 1,96 \\refBLSZ; în finanțe, un factor nou are nevoie de $t > 3$ \\refHLZ')]),
    T('Persistent predictors add a second problem: HAC tests over-reject, as in Chapter 0 \\refStam', 'Predictorii persistenți adaugă o a doua problemă: testele HAC resping prea des, ca în Capitolul 0 \\refStam')), 'small')

chart(T('A specification search on a series with no predictability', 'O căutare de specificații pe o serie fără predictibilitate'), 'ats_ch15_snooping', 'ATS_ch15_pitfalls', [
    T(r'@{sn.reps} simulated data sets, $T$ = @{sn.T}; $K$ persistent candidate predictors ($\rho = 0.9$, a common factor); HAC $t$-tests; the share of data sets with at least one ``discovery\'\'', r'@{sn.reps} seturi de date simulate, $T$ = @{sn.T}; $K$ predictori candidați persistenți ($\rho = 0{,}9$, un factor comun); teste $t$ HAC; proporția seturilor cu cel puțin o „descoperire”')],
    h='0.66\\textheight')

interp(('the specification search', 'căutării de specificații'), [
    T(r'Reporting the best of $K$ as if it were the only one: @{sn.5.n}\% false positives with 5 predictors, @{sn.20.n}\% with 20, @{sn.50.n}\% with 50', r'Raportarea celui mai bun dintre $K$ ca și cum ar fi singurul încercat: @{sn.5.n}\% rezultate fals pozitive cu 5 predictori, @{sn.20.n}\% cu 20, @{sn.50.n}\% cu 50'),
    T(r'Bonferroni does not fix it: @{sn.20.b}\% at $K = 20$, because each HAC test is already oversized with persistent predictors (@{sn.1.n}\% at $K = 1$)', r'Bonferroni nu rezolvă problema: @{sn.20.b}\% la $K = 20$, pentru că fiecare test HAC este deja supradimensionat cu predictori persistenți (@{sn.1.n}\% la $K = 1$)'),
    T(r'The max-$t$ critical value simulated under the null with the same dependence keeps the rate near 5\%: @{sn.20.m}\% at $K = 20$ (the logic of the Reality Check)', r'Valoarea critică max-$t$ simulată sub ipoteza nulă, cu aceeași dependență, păstrează rata aproape de 5\%: @{sn.20.m}\% la $K = 20$ (logica Reality Check)'),
    T(r'The BET in Chapter 0: naive $p$ = @{c0.rcpn}, Reality Check $p$ = @{c0.rcp}', r'BET în Capitolul 0: $p$ naiv = @{c0.rcpn}, $p$ Reality Check = @{c0.rcp}'),
    T('Pre-register $K$; report all $K$ results', 'Preînregistrați $K$; raportați toate cele $K$ rezultate')])

D.frame(T('Leakage and look-ahead', 'Leakage și look-ahead'), items(
    (T(r'\textbf{Leakage}: information from the evaluation period enters the model \refKau', r'\textbf{Leakage}: informația din perioada de evaluare intră în model \refKau'),
     [T('selection of predictors, lags or hyperparameters on the whole sample', 'selecția predictorilor, a lagurilor sau a hiperparametrilor pe întregul eșantion'),
      T('scaling, detrending, filtering (HP, wavelets) or imputing with full-sample statistics', 'scalare, eliminarea trendului, filtrare (HP, wavelet) sau imputare cu statistici din întregul eșantion'),
      T('random K-fold with dependent residuals or overlapping targets (Chapter 12)', 'K-fold aleator cu reziduuri dependente sau ținte suprapuse (Capitolul 12)')]),
    (T(r'\textbf{Look-ahead}: using data that were not available at the forecast date', r'\textbf{Look-ahead}: folosirea datelor care nu erau disponibile la data prognozei'),
     [T('revised data instead of real-time vintages; publication lags ignored', 'date revizuite în locul edițiilor în timp real; întîrzierile de publicare ignorate'),
      T('pretrained models whose training data cover the test period (Chapter 13)', 'modele preantrenate ale căror date de antrenare acoperă perioada de test (Capitolul 13)')]),
    T('Test: could I have computed this forecast on that date, with that information?', 'Testul: aș fi putut calcula această prognoză la acea dată, cu acea informație?')), 'small')

chart(T('Predictor selection with look-ahead', 'Selecția predictorilor cu look-ahead'), 'ats_ch15_leakage', 'ATS_ch15_pitfalls', [
    T(r'@{lk.reps} simulations: $T$ = @{lk.T}, last @{lk.n_test} periods for testing, @{lk.P} pure-noise candidate predictors, the @{lk.k} most correlated kept, OLS on the training sample', r'@{lk.reps} de simulări: $T$ = @{lk.T}, ultimele @{lk.n_test} de perioade pentru test, @{lk.P} de predictori candidați de tip zgomot pur, se păstrează cei @{lk.k} mai corelați, MCO pe eșantionul de antrenare')],
    h='0.66\\textheight')

interp(('the leakage experiment', 'experimentului cu leakage'), [
    T(r'Honest selection: mean out-of-sample $R^2$ = @{lk.honest}\%, positive in @{lk.hpos}\% of runs: noise does not forecast', r'Selecție corectă: $R^2$ mediu în afara eșantionului = @{lk.honest}\%, pozitiv în @{lk.hpos}\% din rulări: zgomotul nu prognozează'),
    T(r'Selection on the whole sample: mean @{lk.leaky}\%, positive in @{lk.lpos}\% of runs: a ``forecasting gain\'\' created by the test period itself', r'Selecție pe întregul eșantion: media @{lk.leaky}\%, pozitiv în @{lk.lpos}\% din rulări: un „cîștig de prognoză” creat chiar de perioada de test'),
    T('Out-of-sample evaluation protects you only if every choice is made inside the training window \\refIK', 'Evaluarea în afara eșantionului vă protejează doar dacă fiecare alegere se face în fereastra de antrenare \\refIK'),
    T('The same mechanism inflated the validation scores of Chapter 12 (ratio @{c12.lk})', 'Același mecanism a supraestimat scorurile de validare din Capitolul 12 (raport @{c12.lk})')])

D.frame(T('Overclaiming', 'Afirmații exagerate'), two(items(
    (T(r'\textbf{Causal language for predictive results}', r'\textbf{Limbaj cauzal pentru rezultate predictive}'),
     [T('``Granger-causes\'\' is not ``causes\'\'; a common driver or timing produces it (Chapter 14)', '„cauzează în sens Granger” nu înseamnă „cauzează”; un factor comun sau momentul observării o produc (Capitolul 14)')]),
    (T(r'\textbf{Significance for size}', r'\textbf{Semnificația în locul mărimii}'),
     [T('a significant DM test with a 0.3\\% loss reduction is a small gain; report the effect and its interval', 'un test DM semnificativ cu o reducere a pierderii de 0,3\\% este un cîștig mic; raportați efectul și intervalul lui')]),
    (T(r'\textbf{Generality for one sample}', r'\textbf{Generalitate pe baza unui singur eșantion}'),
     [T('one market, one period, one specification; say so in the title and the abstract', 'o piață, o perioadă, o specificație; spuneți-o în titlu și în rezumat')]),
    (T(r'\textbf{Absence of evidence for evidence of absence}', r'\textbf{Absența dovezii drept dovadă a absenței}'),
     [T(r'a non-rejection with low power says little: compute the power (Romanian nowcast, $p$ = @{c5.dmp})', r'o nerespingere cu putere mică spune puțin: calculați puterea (nowcast-ul României, $p$ = @{c5.dmp})')])),
    ph('granger', T('Clive Granger (2008)', 'Clive Granger (2008)'), h='0.40\\textheight')), 'footnotesize')

D.recap(('failure modes', 'erorile frecvente'), [
    T('A search reported as a single test produces discoveries from noise; pre-register $K$ and correct for it', 'O căutare raportată ca un singur test produce descoperiri din zgomot; preînregistrați $K$ și corectați'),
    T('Every choice inside the training window, every datum available at the forecast date', 'Fiecare alegere în fereastra de antrenare, fiecare dată disponibilă la data prognozei'),
    T('Claims no stronger than the design: prediction is not causation, significance is not size', 'Afirmații nu mai puternice decît designul: predicția nu este cauzalitate, semnificația nu este mărime')])

# =============================================================================
# SUSȚINEREA ORALĂ
# =============================================================================
D.section('The oral defence', 'Susținerea orală')

D.frame(T('Format of the defence', 'Formatul susținerii'), two(items(
    (T('Individual, about 15 minutes per student', 'Individuală, circa 15 minute pentru fiecare student'),
     [T('each member is examined separately and receives a separate grade (50\\% of the final grade)', 'fiecare membru este examinat separat și primește o notă separată (50\\% din nota finală)')]),
    T('5 minutes: presentation of one\'s own contribution, the part of the project the student led, on the report and the repository', '5 minute: prezentarea contribuției proprii, adică a părții de proiect coordonate de student, pe baza raportului și a repository-ului'),
    (T('10 minutes: questions on the code, the method and the results', '10 minute: întrebări despre cod, metodă și rezultate'),
     [T('the code: open a file, explain a function, say what changes if a choice changes', 'codul: deschideți un fișier, explicați o funcție, spuneți ce se schimbă dacă se schimbă o alegere'),
      T('the method: the theory behind it, its assumptions and its alternatives', 'metoda: teoria din spatele ei, ipotezele și alternativele'),
      T('the results: interpret a number, a test, a figure; defend the inference', 'rezultatele: interpretați un rezultat, un test, o figură; apărați inferența')]),
    T('Graded with the rubric on the next slide', 'Se notează după criteriile de pe slide-ul următor'),
    T('Every member must be able to answer questions on the whole project, not only on their part', 'Fiecare membru trebuie să poată răspunde la întrebări despre întregul proiect, nu doar despre partea proprie'),
    T('No AI tools during the defence; Romanian or English', 'Fără instrumente AI în timpul susținerii; în română sau în engleză')),
    ph('ase', T('Bucharest University of Economic Studies', 'Academia de Studii Economice din București'), h='0.36\\textheight'), '0.6', '0.36'), 'small')

D.frame(T('Grading rubric of the individual defence', 'Criteriile de evaluare a susținerii individuale'), table(
    TB + 'p{3.2cm}' + '>{\\raggedleft\\arraybackslash}p{1.1cm}' + TB + 'p{7.2cm}',
    T(r'\textbf{Criterion}', r'\textbf{Criteriul}') + ' & ' + T(r'\textbf{Points}', r'\textbf{Puncte}') + ' & ' + T(r'\textbf{What earns the points}', r'\textbf{Ce aduce punctele}'),
    [T('Mastery of the method', 'Stăpînirea metodei') + ' & 25 & ' + T('states the model and its assumptions, derives the key result, knows when the method fails', 'formulează modelul și ipotezele, derivă rezultatul-cheie, știe cînd metoda nu funcționează'),
     T('Ownership of the code and data', 'Stăpînirea codului și a datelor') + ' & 20 & ' + T('explains any function of the repository, the data source and vintage, the effect of changing a setting', 'explică orice funcție din repository, sursa și ediția datelor, efectul schimbării unei setări'),
     T('Inference and interpretation', 'Inferența și interpretarea') + ' & 25 & ' + T('valid standard errors for dependent data, effect sizes with intervals, correct reading of tests and of non-rejections', 'erori standard valide pentru date dependente, mărimi ale efectelor cu intervale, citirea corectă a testelor și a nerespingerilor'),
     T('Replication and robustness', 'Replicarea și robustețea') + ' & 20 & ' + T('explains differences from the paper, the robustness design and the limits of the conclusion', 'explică diferențele față de lucrare, designul de robustețe și limitele concluziei'),
     T('Research integrity and AI use', 'Integritatea cercetării și folosirea AI') + ' & 10 & ' + T('describes what AI did, which errors were caught and how; deviations from the pre-registration', 'descrie ce a făcut AI, ce erori au fost depistate și cum; abaterile de la preînregistrare')],
    size='scriptsize') + items(
    T('The defence grade is the score out of 100 divided by 10; a member who cannot explain the code they submitted cannot pass', 'Nota la susținere este punctajul din 100 împărțit la 10; un membru care nu poate explica codul predat nu poate promova')), 'small')

D.frame(T('What distinguishes the grades', 'Criteriile care diferențiază notele'), items(
    (T(r'\textbf{9--10}', r'\textbf{9--10}'),
     [T('answers ``why\'\' and ``what if\'\', not only ``what\'\'; anticipates the weak points and has tested them', 'răspunde la „de ce” și „ce s-ar întîmpla dacă”, nu doar la „ce”; anticipează punctele slabe și le-a testat')]),
    (T(r'\textbf{7--8}', r'\textbf{7--8}'),
     [T('correct methods and interpretation; hesitates on alternatives or on the asymptotics', 'metode și interpretare corecte; ezită la alternative sau la asimptotică')]),
    (T(r'\textbf{5--6}', r'\textbf{5--6}'),
     [T('can run and describe the code; reads p-values mechanically; limited link to the theory', 'poate rula și descrie codul; citește mecanic p-value-urile; legătură limitată cu teoria')]),
    (T(r'\textbf{below 5}', r'\textbf{sub 5}'),
     [T('cannot explain own code or numbers; claims not supported by the results; undeclared AI use', 'nu poate explica propriul cod sau propriile rezultate; afirmații nesusținute de rezultate; folosire nedeclarată a AI')])))

QA = T(r'\textbf{Question}', r'\textbf{Întrebare}')
AN = T(r'\textbf{Model answer}', r'\textbf{Răspuns-model}')


def qa(title, pairs):
    D.frame(title, items(*[(QA + ': ' + q, [AN + ': ' + a]) for q, a in pairs]), 'footnotesize')


qa(T('Typical questions with model answers (1/3): the code', 'Întrebări tipice cu răspunsuri-model (1/3): codul'), [
    (T('Where in your code is the information set of the forecast for date $t$ fixed?', 'Unde se fixează în codul dumneavoastră mulțimea de informație a prognozei pentru data $t$?'),
     T('In the walk-forward loop: the estimation window ends at $t - h$, and scaling, selection and tuning are recomputed inside the loop (shows the lines)', 'În bucla walk-forward: fereastra de estimare se termină la $t - h$, iar scalarea, selecția și calibrarea hiperparametrilor se recalculează în buclă (arată liniile)')),
    (T('How many HAC lags do you use, and why?', 'Cîte laguri HAC folosiți și de ce?'),
     T(r'The Newey--West rule $\lfloor 4(T/100)^{2/9}\rfloor$ ($T$: sample size; $\lfloor\cdot\rfloor$: integer part), at least $h - 1$ for overlapping $h$-step errors; checked with fixed-$b$ critical values (Chapter 0)', r'Regula Newey--West $\lfloor 4(T/100)^{2/9}\rfloor$ ($T$: mărimea eșantionului; $\lfloor\cdot\rfloor$: partea întreagă), cel puțin $h - 1$ pentru erori suprapuse la $h$ pași; verificat cu valori critice fixed-$b$ (Capitolul 0)')),
    (T('What happens if you change the seed?', 'Ce se întîmplă dacă schimbați seed-ul?'),
     T('We reran with ten seeds: the ranking is unchanged, the loss changes by less than its standard error (a table in the report)', 'Am rulat din nou cu zece seed-uri: ierarhia nu se schimbă, pierderea variază cu mai puțin decît eroarea ei standard (un tabel în raport)'))])

qa(T('Typical questions with model answers (2/3): the results', 'Întrebări tipice cu răspunsuri-model (2/3): rezultatele'), [
    (T('Your DM test gives $p = 0.03$: is your model better?', 'Testul DM dă $p = 0{,}03$: este modelul dumneavoastră mai bun?'),
     T('Better in the pre-registered loss over this sample: the mean loss differential is X with a HAC interval; the models are not nested, so DM is valid; with several models we report the MCS', 'Mai bun pentru funcția de pierdere preînregistrată, pe acest eșantion: diferența medie a pierderilor este X, cu un interval HAC; modelele nu sînt imbricate, deci DM este valid; pentru mai multe modele raportăm MCS')),
    (T('Your replication differs from Table 2 of the paper. Why?', 'Replicarea diferă de tabelul 2 din lucrare. De ce?'),
     T('On the original sample we match to two decimals; the difference appears with the current data vintage, so it is revision, not code (shows the two runs)', 'Pe eșantionul original coincidem la două zecimale; diferența apare cu ediția actuală a datelor, deci este revizuire, nu cod (arată cele două rulări)')),
    (T('What result would have made you reject your hypothesis?', 'Ce rezultat v-ar fi făcut să respingeți ipoteza?'),
     T('The pre-registration states it: a placebo date with a similar effect, or an effect that changes sign across the donor pools', 'Preînregistrarea o spune: o dată placebo cu un efect asemănător sau un efect care își schimbă semnul între grupurile de donatori'))])

qa(T('Typical questions with model answers (3/3): the chapters', 'Întrebări tipice cu răspunsuri-model (3/3): capitolele'), [
    (T('Why can you not use $\\chi^2$ critical values to test two regimes against one?', 'De ce nu puteți folosi valori critice $\\chi^2$ pentru a testa două regimuri față de unul?'),
     T('Under the null the transition probabilities are not identified, a parameter is on the boundary and the score is zero: the bootstrap or Hansen\'s and Garcia\'s methods are needed (Chapter 7)', 'Sub ipoteza nulă, probabilitățile de tranziție nu sînt identificate, un parametru este la limită și scorul este zero: este nevoie de bootstrap sau de metodele lui Hansen și Garcia (Capitolul 7)')),
    (T('Why is K-fold cross-validation acceptable for your AR model but not for your random forest?', 'De ce este acceptabilă validarea K-fold pentru modelul AR, dar nu pentru random forest?'),
     T('For a well-specified autoregression the residuals are uncorrelated, so the folds are valid \\refBHK; the forest\'s residuals are autocorrelated, so we block and purge (Chapter 12)', 'Pentru o autoregresie bine specificată reziduurile sînt necorelate, deci partițiile sînt valide \\refBHK; reziduurile random forest sînt autocorelate, deci folosim blocuri și purjare (Capitolul 12)')),
    (T('Is a significant Granger test a causal effect?', 'Este un test Granger semnificativ un efect cauzal?'),
     T('No: it is predictive relative to an information set; a causal claim needs an identifying assumption about the assignment, such as an instrument or a synthetic control with placebos (Chapter 14)', 'Nu: este predictiv, relativ la o mulțime de informație; o afirmație cauzală cere o ipoteză de identificare despre alocare, de exemplu un instrument sau un control sintetic cu placebo (Capitolul 14)'))])

D.frame(T('Where defences go wrong', 'Unde greșesc susținerile'), items(
    T('Code written by someone else (a colleague or an AI assistant) that the presenter cannot explain', 'Cod scris de altcineva (un coleg sau un asistent AI) pe care cel care prezintă nu îl poate explica'),
    T('A p-value read as the probability that the hypothesis is true', 'Un p-value citit drept probabilitatea ca ipoteza să fie adevărată'),
    T('A forecasting gain without a test, or a test without the size of the gain', 'Un cîștig de prognoză fără test sau un test fără mărimea cîștigului'),
    T('Not knowing the data: source, frequency, vintage, transformations, sample dates', 'Necunoașterea datelor: sursa, frecvența, ediția, transformările, datele eșantionului'),
    T('Numbers in the report that the repository does not reproduce', 'Rezultate din raport pe care repository-ul nu le reproduce'),
    T('Defending every result instead of explaining its limits', 'Apărarea fiecărui rezultat în loc de explicarea limitelor lui')))

# =============================================================================
# AI ÎN CERCETARE
# =============================================================================
D.section('AI in research', 'AI în cercetare')

D.frame(T('AI\\_USE.md: what was asked and what was kept', 'AI\\_USE.md: ce s-a cerut și ce s-a păstrat'), items(
    (T('AI tools are allowed and declared; undeclared use counts as plagiarism', 'Instrumentele AI sînt permise și se declară; folosirea nedeclarată este considerată plagiat'), []),
    (T('For each use, one entry', 'Pentru fiecare folosire, o intrare'),
     [T('the tool and version, the date, the step of the workflow', 'instrumentul și versiunea, data, etapa din fluxul de cercetare'),
      T('the prompt (or a faithful summary of it)', 'promptul (sau un rezumat fidel al lui)'),
      T('what was kept, changed or rejected, and how it was checked', 'ce s-a păstrat, ce s-a modificat sau respins și cum s-a verificat')]),
    (T('Useful uses', 'Folosiri utile'),
     [T('literature search with verified DOIs; first drafts of code with tests; a hostile-referee critique of the design \\refKor', 'căutarea literaturii cu DOI verificate; prime variante de cod, cu teste; critica designului în rolul unui recenzent ostil \\refKor')]),
    (T('Risky uses', 'Folosiri riscante'),
     [T('references, numbers and dates taken without checking \\refWW; text that claims more than the results', 'referințe, rezultate și date preluate fără verificare \\refWW; text care afirmă mai mult decît rezultatele'),
      T('the illusion of understanding: fluent output mistaken for knowledge \\refMC', 'iluzia înțelegerii: un text fluent confundat cu cunoașterea \\refMC')])), 'small')

D.frame(T('AI\\_ERRORS.md: at least three errors caught', 'AI\\_ERRORS.md: cel puțin trei erori depistate'), table(
    TB + 'p{2.6cm}' + TB + 'p{5.0cm}' + TB + 'p{4.8cm}',
    T(r'\textbf{Type}', r'\textbf{Tipul}') + ' & ' + T(r'\textbf{Example from the course}', r'\textbf{Exemplu din curs}') + ' & ' + T(r'\textbf{How it is caught}', r'\textbf{Cum se depistează}'),
    [T('invented reference', 'referință inventată') + ' & ' + T('a plausible title with a DOI that resolves to another paper', 'un titlu plauzibil cu un DOI care duce la altă lucrare') + ' & ' + T('Crossref lookup: title and authors must match', 'căutare în Crossref: titlul și autorii trebuie să coincidă'),
     T('wrong formula', 'formulă greșită') + ' & ' + T('ES scored alone with a quantile loss (Chapter 9)', 'ES evaluat singur cu o pierdere de cuantilă (Capitolul 9)') + ' & ' + T('derivation on paper; a simulation with known answer', 'derivare pe hîrtie; o simulare cu răspuns cunoscut'),
     T('leakage in code', 'leakage în cod') + ' & ' + T('a scaler fitted on the whole sample before the split', 'o scalare estimată pe întregul eșantion înainte de împărțire') + ' & ' + T('the date test: recompute a forecast with data up to its date only', 'testul datei: recalculați o prognoză doar cu datele de pînă la data ei'),
     T('wrong default', 'opțiune implicită greșită') + ' & ' + T('a $\\chi^2$ critical value for a sup-test (Chapter 2)', 'o valoare critică $\\chi^2$ pentru un test sup (Capitolul 2)') + ' & ' + T('read the documentation and the paper; reproduce a published value', 'citiți documentația și lucrarea; reproduceți o valoare publicată'),
     T('overclaiming', 'afirmație exagerată') + ' & ' + T('``Granger causality proves that ...\'\' (Chapter 14)', '„cauzalitatea Granger dovedește că ...” (Capitolul 14)') + ' & ' + T('compare each sentence with the design', 'comparați fiecare frază cu designul')],
    size='scriptsize') + items(
    T('Each entry: what the tool produced, why it was wrong, how it was detected, what replaced it', 'Fiecare intrare: ce a produs instrumentul, de ce era greșit, cum a fost depistat, ce l-a înlocuit')), 'small')

D.frame(T('A verification protocol', 'Un protocol de verificare'), items(
    T('References: every DOI resolved and the title matched; the claimed result found in the paper', 'Referințele: fiecare DOI verificat și titlul confirmat; rezultatul invocat găsit în lucrare'),
    T('Code: run on a simulated process with known parameters before the real data; compare with a second implementation', 'Codul: rulat pe un proces simulat cu parametri cunoscuți înainte de datele reale; comparat cu o a doua implementare'),
    T('Numbers: every number in the report regenerated by the repository; none copied from a chat', 'Rezultatele: fiecare rezultat din raport regenerat de repository; niciunul copiat dintr-o conversație'),
    T('Dates and facts: from official sources (Eurostat, BNR, Monitorul Oficial), not from the model\'s memory', 'Datele calendaristice și faptele: din surse oficiale (Eurostat, BNR, Monitorul Oficial), nu din memoria modelului'),
    T('Text: each claim checked against the design (prediction, association or causation)', 'Textul: fiecare afirmație verificată față de design (predicție, asociere sau cauzalitate)'),
    T('At the defence you explain everything yourself: what you cannot explain should not be in the project', 'La susținere explicați totul singur: ce nu puteți explica nu ar trebui să fie în proiect')))

# =============================================================================
# AI ÎN DESCOPERIREA ȘTIINȚIFICĂ
# =============================================================================
D.section('AI for scientific discovery: choosing a project', 'AI în descoperirea științifică: alegerea proiectului')

D.frame(T('The open question', 'Întrebarea deschisă'), items(
    (T(r'\textbf{Which landmark results in time series econometrics survive on new data, and why do some not?}', r'\textbf{Ce rezultate de referință din econometria seriilor de timp rezistă pe date noi și de ce unele nu?}'),
     [T('the course replications point to vintages, samples and inference; a systematic answer across papers does not exist', 'replicările din curs indică edițiile datelor, eșantioanele și inferența; un răspuns sistematic, pentru mai multe lucrări, nu există')]),
    (T('AI tools change the cost of each step', 'Instrumentele AI schimbă costul fiecărei etape'),
     [T('literature maps and code drafts in hours \\refWang; fully automated pipelines have been proposed \\refLu', 'hărți ale literaturii și variante de cod în cîteva ore \\refWang; s-au propus fluxuri complet automatizate \\refLu'),
      T('the scarce resource becomes judgement: the design, the checks, the interpretation', 'resursa rară devine judecata: designul, verificările, interpretarea')]),
    T('Your project is one data point in this question: a replication with a clear verdict and a documented reason', 'Proiectul dumneavoastră este un punct de date pentru această întrebare: o replicare cu un verdict clar și un motiv documentat')), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List replications of Meese and Rogoff (1983) for Central and Eastern European currencies since 2010, with DOIs, horizons and verdicts.} Then check every DOI', r'\textbf{literatura}: \aiprompt{Listează replicările lucrării Meese și Rogoff (1983) pentru monedele din Europa Centrală și de Est din 2010 încoace, cu DOI, orizonturi și verdicte.} Apoi verificați fiecare DOI'),
      T(r'\textbf{design}: \aiprompt{Given a loss differential with autocorrelation 0.3, how many out-of-sample months are needed for 80\% power to detect a mean gain of 0.2 standard deviations?}', r'\textbf{designul}: \aiprompt{Pentru o diferență a pierderilor cu autocorelația 0,3, cîte luni în afara eșantionului sînt necesare pentru o putere de 80\% la detectarea unui cîștig mediu de 0,2 abateri standard?}'),
      T(r'\textbf{code and replication}: ask for a DM--HLN function, then test it on simulated data with a known answer', r'\textbf{cod și replicare}: cereți o funcție DM--HLN, apoi testați-o pe date simulate cu răspuns cunoscut'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee of this pre-registration: where can the results leak into the design?}', r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil al acestei preînregistrări: unde pot rezultatele să influențeze designul?}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('The paper exists, says what is claimed, and its data are available today', 'Lucrarea există, spune ce se afirmă, iar datele ei sînt disponibile azi'),
    T('The power calculation uses the dependence of your own loss differential, estimated on the training period', 'Calculul puterii folosește dependența propriei diferențe a pierderilor, estimată pe perioada de antrenare'),
    T('The formula behind an AI answer: a power claim without the long-run variance is wrong for dependent data', 'Formula din spatele unui răspuns AI: o afirmație despre putere fără varianța de termen lung este greșită pentru date dependente'),
    T('The extension is feasible in one semester with the course tools', 'Extensia este realizabilă într-un semestru cu instrumentele cursului'),
    T('The verdict criteria (replicated, partly, not) are written before the replication is run', 'Criteriile verdictului (replicat, parțial, nereplicat) sînt scrise înainte de a rula replicarea')), 'small')

chart(T('Mini-case: is the evaluation sample long enough?', 'Mini studiu de caz: este eșantionul de evaluare destul de lung?'), 'ats_ch15_power', 'ATS_ch15_power', [
    T(r'Rejection rate of the DM--HLN test (5\%, two-sided, @{pw.reps} simulations) when the loss differential is a mean gain $\delta$ plus an AR(1) noise with coefficient $\rho = 0.3$ and unit variance', r'Rata de respingere a testului DM--HLN (5\%, bilateral, @{pw.reps} de simulări) cînd diferența pierderilor este un cîștig mediu $\delta$ plus un zgomot AR(1) cu coeficientul $\rho = 0{,}3$ și varianța 1'),
    T(r'Dotted: the approximation $\Phi\big(\delta\sqrt{P/\Omega} - 1.96\big)$; $\Phi$: standard Normal distribution function; $P$: number of out-of-sample observations; $\Omega$: long-run variance of the differential', r'Punctat: aproximarea $\Phi\big(\delta\sqrt{P/\Omega} - 1{,}96\big)$; $\Phi$: funcția de repartiție a distribuției Normale standard; $P$: numărul de observații în afara eșantionului; $\Omega$: varianța de termen lung a diferenței')],
    h='0.56\\textheight')

interp(('the mini-case', 'mini studiului de caz'), [
    T(r'A gain of 0.2 standard deviations is detected with probability @{pw.b.100}\% at $P = 100$ and @{pw.b.500}\% at $P = 500$; 80\% power needs about @{pw.b.p80} observations', r'Un cîștig de 0,2 abateri standard este detectat cu probabilitatea @{pw.b.100}\% la $P = 100$ și @{pw.b.500}\% la $P = 500$; o putere de 80\% cere aproximativ @{pw.b.p80} de observații'),
    T(r'A gain of 0.1 needs about @{pw.a.p80}: more than 120 years of monthly data; a gain of 0.3 about @{pw.c.p80}', r'Un cîștig de 0,1 cere aproximativ @{pw.a.p80}: mai mult de 120 de ani de date lunare; un cîștig de 0,3 aproximativ @{pw.c.p80}'),
    (T(r'The sample-size rule $P \approx \Omega\,(z_{0.975} + z_{0.8})^2/\delta^2$, with $\Omega = (1 + \rho)/(1 - \rho)$ = @{pw.om}: dependence multiplies the sample you need', r'Regula de mărime a eșantionului $P \approx \Omega\,(z_{0{,}975} + z_{0{,}8})^2/\delta^2$, cu $\Omega = (1 + \rho)/(1 - \rho)$ = @{pw.om}: dependența multiplică eșantionul necesar'),
     [T(r'$z_{0.975} = 1.96$, $z_{0.8} = 0.84$: Normal quantiles for a 5\% two-sided test and 80\% power; $\delta$: the mean gain in standard deviations', r'$z_{0{,}975} = 1{,}96$, $z_{0{,}8} = 0{,}84$: cuantilele distribuției Normale pentru un test bilateral de 5\% și o putere de 80\%; $\delta$: cîștigul mediu, în abateri standard')]),
    T(r'With few observations the test is also oversized: @{pw.s.50}\% at $P = 50$', r'Cu puține observații testul este și supradimensionat: @{pw.s.50}\% la $P = 50$'),
    T('Choose a question your data can answer: monthly macro data rarely detect small gains, daily or intraday data can', 'Alegeți o întrebare la care datele pot răspunde: datele macro lunare detectează rar cîștiguri mici, datele zilnice sau intrazilnice pot')])

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Choosing the project: four criteria}', r'\textbf{Alegerea proiectului: patru criterii}'),
     [T('a landmark paper with public data or a precise data description, and a number to match', 'o lucrare de referință cu date publice sau o descriere precisă a datelor și un rezultat de reprodus'),
      T('an extension that answers one new question, preferably on Romanian or EU data', 'o extensie care răspunde unei întrebări noi, de preferință pe date din România sau din UE'),
      T('enough power for the evaluation you plan (the mini-case)', 'suficientă putere pentru evaluarea planificată (mini studiul de caz)'),
      T('a verdict rule written before the first estimate', 'o regulă a verdictului scrisă înaintea primei estimări')]),
    (T(r'\textbf{Example}: why do some replications fail? A replication audit of three course papers', r'\textbf{Exemplu}: de ce eșuează unele replicări? Un audit de replicare pentru trei lucrări din curs'),
     [T(r'replicate \refTPS, \refPZC and \refBMSS on the original and on today\'s data; attribute each difference to vintage, sample, implementation or inference', r'replicați \refTPS, \refPZC și \refBMSS pe datele originale și pe cele de azi; atribuiți fiecare diferență ediției, eșantionului, implementării sau inferenței'),
      T('extend: archived vintages (ALFRED, OECD Economic Outlook), a specification curve, a power analysis of each original test', 'extindeți: ediții arhivate ale datelor (ALFRED, OECD Economic Outlook), o curbă a specificațiilor, o analiză a puterii fiecărui test original')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Five questions for every analysis: target, dependence, identification, evaluation, robustness', 'Cinci întrebări pentru orice analiză: ținta, dependența, identificarea, evaluarea, robustețea'),
    T('Most landmark results replicate in direction; their strength and their tests depend on vintage, sample and inference', 'Majoritatea rezultatelor de referință se replică în sens; mărimea și testele lor depind de ediția datelor, de eșantion și de inferență'),
    T('Pre-register the design, compute the power, and make every number reproducible from one command', 'Preînregistrați designul, calculați puterea și faceți fiecare rezultat reproductibil dintr-o singură comandă'),
    T('Searches, leakage and look-ahead create discoveries from noise; causal words need causal designs', 'Căutările, leakage-ul și look-ahead creează descoperiri din zgomot; cuvintele cauzale cer designuri cauzale'),
    T('The defence is individual: explain the method, the code, the inference and the limits yourself', 'Susținerea este individuală: explicați singur metoda, codul, inferența și limitele')))

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('Which assumption identifies the main result of your project?', 'Ce ipoteză identifică rezultatul principal al proiectului dumneavoastră?'),
        T('How many specifications did you try, and how does your inference account for them?', 'Cîte specificații ați încercat și cum ține cont inferența dumneavoastră de ele?'),
        T('Could each forecast have been computed on its date?', 'Ar fi putut fi calculată fiecare prognoză la data ei?'),
        T('What is the power of your main test?', 'Care este puterea testului principal?'),
        T('Which of your numbers would change with a new data vintage?', 'Care dintre rezultatele dumneavoastră s-ar schimba cu o nouă ediție a datelor?'))),
    block(T('Further study', 'Studiu suplimentar'), items(
        T(r'\refCM; \refCle; \refMen', r'\refCM; \refCle; \refMen'),
        T(r'\refDiebold; \refLLSW', r'\refDiebold; \refLLSW'),
        T('Self-study Chapter 16 and its quiz', 'Capitolul 16 (studiu individual) și quiz-ul lui'))),
    '0.58', '0.38'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: project seeds by chapter (1/2)', 'Anexă: idei de proiect pe capitole (1/2)'), table(
    'l' + TB + 'p{5.0cm}' + TB + 'p{6.6cm}',
    T(r'\textbf{Ch.}', r'\textbf{Cap.}') + ' & ' + T(r'\textbf{Replicate}', r'\textbf{Replicați}') + ' & ' + T(r'\textbf{Extend}', r'\textbf{Extindeți}'),
    [r'0 & \refEH & ' + T('the euro area and Romania; fixed-$b$ inference; stability across decades', 'zona euro și România; inferență fixed-$b$; stabilitatea pe decenii'),
     r'1 & \refMR & ' + T('CEE currencies, density forecasts, real-time macro fundamentals', 'monedele din ECE, prognoze de densitate, fundamente macro în timp real'),
     r'2 & \refBP & ' + T('breaks in Romanian inflation and the policy rate; real-time monitoring', 'rupturi în inflația României și în dobînda de politică monetară; monitorizare în timp real'),
     r'3 & \refGK & ' + T('ECB surprises and Romanian financial conditions with LP-IV', 'surprizele BCE și condițiile financiare din România cu LP-IV'),
     r'4 & \refPSS & ' + T('interest-rate pass-through in the EU with CCE', 'transmiterea dobînzilor în UE cu CCE'),
     r'5 & \refBGR & ' + T('a large BVAR with stochastic volatility for Romania, nowcasting with news', 'un BVAR mare cu volatilitate stochastică pentru România, nowcasting cu știri'),
     r'6 & \refMNZ & ' + T('the Romanian output gap and its real-time revisions', 'output gap-ul României și revizuirile lui în timp real'),
     r'7 & \refHam & ' + T('real-time recession probabilities for the euro area', 'probabilități de recesiune în timp real pentru zona euro'),
     r'8 & \refBPQ & ' + T('HARQ for the BET and EUR/RON with realised measures', 'HARQ pentru BET și EUR/RON cu măsuri realizate')],
    size='scriptsize'), 'small')

D.frame(T('Appendix: project seeds by chapter (2/2)', 'Anexă: idei de proiect pe capitole (2/2)'), table(
    'l' + TB + 'p{5.0cm}' + TB + 'p{6.6cm}',
    T(r'\textbf{Ch.}', r'\textbf{Cap.}') + ' & ' + T(r'\textbf{Replicate}', r'\textbf{Replicați}') + ' & ' + T(r'\textbf{Extend}', r'\textbf{Extindeți}'),
    [r'9 & \refPZC & ' + T('CEE indices; the power of the backtests', 'indicii din ECE; puterea backtest-urilor'),
     r'10 & \refGJR & ' + T('roughness of CEE and crypto volatility; robustness to noise', 'caracterul rough al volatilității în ECE și pe cripto; robustețea la zgomot'),
     r'11 & \refCN, \refHamB & ' + T('real-time output gaps of the EU members', 'output gap-uri în timp real pentru statele membre UE'),
     r'12 & \refZeng & ' + T('EU electricity load; global models; honest benchmarks', 'consumul de electricitate din UE; modele globale; comparații oneste'),
     r'13 & \refGC & ' + T('conformal VaR for the BET; coverage by regime', 'VaR conformal pentru BET; acoperire pe regimuri'),
     r'14 & \refADH, \refBMSS & ' + T('tax and energy measures in CEE with synthetic controls', 'măsuri fiscale și energetice în ECE cu controale sintetice'),
     r'16 & \refPY & ' + T('house prices and rents in EU capitals', 'prețurile și chiriile locuințelor în capitalele UE'),
     r'15 & \refTPS, \refPZC, \refBMSS & ' + T('a replication audit (the project idea of this chapter)', 'un audit de replicare (ideea de proiect a acestui capitol)')],
    size='scriptsize') + items(
    T('Part C of every seminar contains a further project seed with its data', 'Partea C a fiecărui seminar conține încă o idee de proiect, cu datele ei')), 'small')

D.frame(T('Appendix: a pre-registration template', 'Anexă: un model de preînregistrare'), items(
    T(r'\textbf{1. Question and hypotheses}: the primary hypothesis, in one sentence; secondary hypotheses', r'\textbf{1. Întrebarea și ipotezele}: ipoteza principală, într-o frază; ipotezele secundare'),
    T(r'\textbf{2. Paper to replicate}: the table or figure, the sample, what counts as ``replicated\'\', ``partly\'\', ``not replicated\'\'', r'\textbf{2. Lucrarea replicată}: tabelul sau figura, eșantionul, ce înseamnă „replicat”, „parțial”, „nereplicat”'),
    T(r'\textbf{3. Data}: series, sources, vintage date, frequency, transformations, exclusions', r'\textbf{3. Datele}: seriile, sursele, data ediției, frecvența, transformările, excluderile'),
    T(r'\textbf{4. Models}: benchmark and competitors, estimation method, how hyperparameters are chosen (inside the training window)', r'\textbf{4. Modelele}: reperul și modelele concurente, metoda de estimare, alegerea hiperparametrilor (în fereastra de antrenare)'),
    T(r'\textbf{5. Evaluation}: windows (rolling or expanding), horizons, losses, tests, multiplicity correction, power calculation', r'\textbf{5. Evaluarea}: ferestrele (mobile sau extinse), orizonturile, funcțiile de pierdere, testele, corecția pentru testarea multiplă, calculul puterii'),
    T(r'\textbf{6. Robustness}: the list of variations and the rule for a robust result', r'\textbf{6. Robustețea}: lista variațiilor și regula pentru un rezultat robust'),
    T(r'\textbf{7. Team}: who leads which part (the basis of the individual defence)', r'\textbf{7. Echipa}: cine coordonează fiecare parte (baza susținerii individuale)')), 'small')

D.references(bib(), per=13)

if __name__ == '__main__':
    finalize(D.write(V))
    run_acronyms(15)   # the glossary again, after the bilingual values are resolved
