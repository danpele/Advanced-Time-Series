# ATS — reguli pentru fiecare capitol (stabilite de titular, 5 octombrie 2026)

Curs: „Analiza avansată a seriilor de timp și previziune” / „Advanced Time Series Analysis and Forecasting” (ATS), programul de master Statistică aplicată și data science (ASDS), anul I, semestrul 2, 7 ECTS, 2 ore de curs și 2 ore de seminar pe săptămînă, Facultatea CSIE, ASE București. Titular: Prof. dr. Daniel Traian Pele. Întregul curs apare pe site și pe slide-uri sub numele titularului: niciun co-titular, niciun titular de seminar numit (`AUTHOR_SEMINAR = AUTHOR_LECTURE` în `latex/ats_build.py`, `seminar: null` în `assets/course-data.js`).

Repo local: `~/Documents/Teaching/ATS - Modelarea avansata a seriilor de timp/repo` (branch `main`, fără remote). Repo public viitor: `danpele/Advanced-Time-Series`, site https://danpele.github.io/Advanced-Time-Series/ (numele `danpele/ATS` NU se folosește: este redirecționarea repo-ului TSA redenumit). Nu se creează repo-ul pe GitHub și nu se face push pînă la aprobarea titularului. Cadrul tehnic este copiat din TSA (care l-a preluat din SFM și MFM); vezi `README_BUILD.md`.

## Nivel și public
- Master, anul I: nivel de cercetare, ca în MFM. Ipoteze și teste formale, identificare, asimptotică pentru date dependente, data snooping și testare multiplă, evaluare în afara eșantionului fixată dinainte, literatura recentă din reviste de top și arXiv. Fără explicații de nivel începător; acronimele și termenii noi se definesc totuși la prima folosire, pe scurt.
- Prerechizit: TSA (licență), capitolele 0–10 (site https://danpele.github.io/Time-Series-Analysis/). Ce s-a predat acolo nu se repetă: se trimite la capitolul TSA corespunzător („TSA, Capitolul 7” / „TSA, Chapter 7”; `appendix_links.py` face legătura).
- Continuare: MFM (master, anul II, semestrul 1). ATS predă metodologia; aplicațiile de risc de piață sînt în MFM. Trimiterile „MFM, Capitolul N” / „MFM Chapter N” devin linkuri.
- Capitolul 16 este de studiu individual (`selfStudy: true`, `SELF_STUDY = {16}`): material mai scurt și quiz.
- Manuale: Hamilton (1994); Kilian și Lütkepohl (2017); Durbin și Koopman (2012); Petropoulos et al. (2022, *IJF*, acces liber). Legătura cu licența: Huang și Petukhina (2022), FPP3. De specialitate: Lütkepohl (2005), Shumway și Stoffer (2017), Baltagi (2021), Angelopoulos și Bates (2023).

## Structura cursului (EN + RO)
- 17 capitole (0–16) cu `id` stabil în `assets/course-data.js`; titlurile identice în `latex/ats_chapters.py` (TITLES); numerotarea în subtitlu: „Chapter N” / „Capitolul N”.
- Fișiere: `EN/Courses/chapterN_<slug>.tex`, `RO/Cursuri/capitolN_<slug>.tex`, `EN/Seminars/seminarN_<slug>.tex`, `RO/Seminarii/seminarN_<slug>_ro.tex`, cu `\input{../../latex/preamble}`; pentru RO `\def\atslang{ro}`. Numele exacte: `python3 latex/ats_chapters.py`.
- Paritate completă RO + EN: slide cu slide, aceleași cifre. Notebook-urile sînt doar în engleză.
- Fiecare capitol: curs de 70–90 de slide-uri (mai lung dacă nivelul o cere), seminar A/B/C (versiunea studenților și versiunea profesorului), notebook-uri de curs și de seminar (EN, executate), Quantlets, quiz de 24 de întrebări (`draw: 20`).

## Curs
- O idee pe slide (cel mult 5–6 bullets); tot textul în bullets de nivel 1–2; fiecare grafic pe slide-ul lui, urmat de un slide „Interpretarea …”; recapitulare la finalul fiecărei secțiuni; glosar de acronime după pagina de titlu; bibliografie în ordine alfabetică.
- Acronimele: glosarul este generat de `python3 latex/acronyms.py N` (rulat automat de `Deck.write`); acronimele noi ale capitolului N se adaugă doar în `latex/acronyms_extra/chN.py`; 0 acronime „NOT IN DICTIONARY”. Acronimele rămîn în forma originală și în RO (CI, CLT, VAR, SVAR, HAC).
- Studii de caz = lucrări de referință din domeniu (landmark papers), replicate pe datele noastre, cu specificațiile exacte din lucrare (secțiunea, tabelul sau ecuația citate pe slide); nu variante proprii „în spiritul” lucrării. Lucrările titularului (Conformal_Oracle, TSFM_VaR_CEE, NAJEF 2025) apar cel mult ca lectură suplimentară, niciodată ca studiu de caz.
- Orice citare este clickabilă, cu DOI verificat prin Crossref (titlul trebuie să coincidă), arXiv sau o pagină oficială cu HTTP 200. Nu se inventează referințe; lucrările retrase se înlocuiesc.
- Imagini reale (portrete, momente istorice, locuri): doar licență liberă verificată prin API-ul Wikimedia Commons, cu credit vizibil `\imgcredit{url}{text}` și intrare în `photos/CREDITS.md`.
- `\quantlet{ATS\_chN\_<name>}{https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_NN/ATS_chN_<name>}` sub fiecare grafic (`D.chart` îl pune automat).
- Secțiunea finală a fiecărui curs: „AI în descoperirea științifică” / „AI for scientific discovery” (4–6 slide-uri, aceeași structură): întrebarea deschisă a capitolului → bucla de descoperire asistată de AI (literatură cu referințe verificate, ipoteză, cod și replicare, robustețe, critică, raport) cu prompturi concrete → ce verifică omul → mini-caz calculat pe datele cursului → idee de proiect. Instrumente generice (asistent AI / LLM; exemple: Claude, ChatGPT, Gemini, Copilot; Semantic Scholar, Elicit). Nu se prezintă transcrieri AI inventate ca reale.

## Limba română
- „sînt/sîntem/sînteți”; „î” în interiorul cuvintelor („â” doar în familia „român”); „nicio/niciun”; ș și ț cu virgulă dedesubt; diacritice complete.
- Titluri și etichete: grupuri nominale, cu literă mare doar la început. Fără „Ce + verb” („Ce predați”, „Ce măsurăm”) și fără titluri „De ce …”. Titluri recurente: „Noțiuni necesare azi”, „Rezultatele învățării”, „Verificări necesare”, „Idei de reținut”, „Idee de proiect”, „Contribuția posibilă a AI”, „Autoevaluare”, „Exemplu rezolvat”, „Interpretarea …”.
- Fără „vs” în textul RO („față de”, „și”, „comparat cu”); fără calcuri („bazat pe” → „pe baza”, „per” → „pe”, „a realiza” pentru „to do”). „mers aleator”, „stochastic” (nu „stocastic”), „termenul liber” (nu „interceptul”), „nestaționaritate”.
- „distribuția Normală” (N mare), niciodată „Normala” substantivizat; „boltire”, „excesul de boltire”.
- Jargonul consacrat rămîne în engleză: drawdown, volatility clustering, backtesting, bootstrap, nowcasting, shrinkage, data snooping, notebook, repository, foundation models, machine learning, deep learning. Fără calcuri inventate.
- Întrebări către sală: „Întrebare pentru sală” / „Ce credeți?” + „Răspuns”; niciodată „preziceți”. O singură întrebare pe bullet.
- Numere: virgulă zecimală; „de” după numerale ≥ 20; intervale cu „;” ([1,38; 1,45]); date „2 octombrie 2026”.
- Adresare formală (dumneavoastră).

## VaR / ES — convenția nivelului
- „VaR 1%”, „ES 2,5%” (RO) / „VaR 1%”, „ES 2.5%” (EN); niciodată „VaR 99%”. $\mathrm{VaR}_\alpha(X) = -q_\alpha(X)$; rata de depășire țintă = $\alpha$.

## Fără remarci despre procesul de lucru
- Fără „verificat în Quantlet”, „exact ca în lucrare”, „orice noțiune este definită”, „aceleași cifre ca pachetul”.
- Fără note de durată sau de ședință („2 × 80 de minute”, „Ședința 1”); se folosesc „Partea I/II”, „Etapa 1/2”.

## Date
- Serii de piață: doar din `data/market/<SYMBOL>.csv` (lista în `data/manifest.csv`, copiate din TSA, pînă la 18.09.2026), citite prin `Quantlets/common/ats_data.py` (local sau din `https://raw.githubusercontent.com/danpele/Advanced-Time-Series/main/data/market/<SYMBOL>.csv`). Furnizorul se numește: EODHD (EOD Historical Data). Fără API cu cheie, fără yfinance, fără pandas_datareader.
- Surse publice fără cheie, citite online: FRED (și FRED-MD), Eurostat, BCE (`read_ecb`), INS (TEMPO), BNR (cursul de referință; EUR/RON = cursul BNR, nu seria EODHD), seturile de date din statsmodels.
- Date intraday pentru măsurile realizate (capitolul 8): sursa nu este încă stabilită (decizie deschisă).
- În materiale nu se descrie cum se încarcă datele; doar numele seriei și sursa oficială. Nu se afirmă nicio cifră necalculată din date sau fără sursă verificată. Seriile externe se extind pînă la zi.

## Grafice
- Fundal transparent; legenda întotdeauna în afara graficului, jos (`legend_outside_bottom`); paleta din `ats_style.py`; niciodată serii sau text în gri (griul doar pentru linii de referință, benzi de încredere, grilă); etichete în engleză.
- `Quantlets/Ch_NN/generate_all_charts.py` + `build_quantlets.py` (foldere `ATS_chN_*` cu Metainfo.txt, notebook Colab autonom, copii ale graficelor).
- Text lizibil pe slide: orice text al unui grafic are cel puțin 6 pt la mărimea la care graficul apare pe slide (textul slide-ului are 8 pt). `ats_style.save_fig` dimensionează automat figura pentru caseta ei de pe slide (`Quantlets/common/chart_boxes.json`, scris de `python3 tools/chart_boxes.py` din fișierele .tex); după schimbarea înălțimii unui grafic într-un generator se rulează `tools/chart_boxes.py` și apoi din nou scriptul graficului. Benzile de încredere au opacitatea de cel puțin 0,3. Figurile cu multe panouri pe un rînd scund se rearanjează (un rînd, titluri în locul legendelor) sau se împart.

## Seminar
- 2 ore pe săptămînă: părțile A (derivări), B (estimare, verificare și inferență pe date: erori standard, bootstrap, teste robuste, cazuri în care metoda standard greșește; fiecare problemă se încheie cu o întrebare de interpretare), C (deschisă, idee de proiect; include exercițiul C2 „Analiza critică a unui răspuns AI”, cu soluția doar la profesor).
- Probleme „[Rezolvat]” / „[Solved]” (soluții vizibile) și „[Propus]” / „[Proposed]” (fiecare cu „Model:” spre problema rezolvată analogă; soluții doar la profesor). Slide inițial „Noțiuni necesare azi”; cerințe explicite (context, sub-cerințe numerotate, ce se raportează) și rezolvări pas cu pas.
- Două PDF-uri din același .tex (`\ifsolutions`): studenți (pe site) și profesor (`*_solutions.tex`, exclus din git).
- Linia de final: „Seminarul are rol de exercițiu și nu se notează; rezolvările cerințelor [Propus] se discută la seminar”. Studenții nu predau nimic la seminar.

## Notebook-uri
- Doar EN: `notebooks/EN/chapterN_lecture_notebook.ipynb`, `chapterN_seminar_notebook.ipynb`, executate cu 0 erori; banner Colab „Save a copy in Drive” și celula de salvare în `MyDrive/ATS/Chapter_N` (`notebooks/add_colab_banner.py`); seminarele separate în versiunea studenților și cea completă (`split_seminar_notebooks.py N`).

## Quiz (notat: 20% din nota finală)
- `assets/quizzes/<id>.js`, înregistrat ca `window.ATS_DATA.quizzes['<id>']`: 24 de întrebări EN+RO, `draw: 20`, `correct` = index 0–3, explicațiile nu numesc litere; include întrebări de tip „găsiți eroarea din răspunsul AI”. Fișierul se creează odată cu capitolul și se adaugă ca `<script>` în ambele `index*.html`.
- Quiz-urile sînt notate, deci backend-ul de scoruri (`QUIZ_SCORES_URL` în `assets/config.js`) trebuie configurat înainte de semestru.

## Evaluare și AI
- 70% proiect: propunere și preînregistrare 5% (echipă), replicare și extensie cu repository, raport, `AI_USE.md` și `AI_ERRORS.md` 15% (echipă), susținere orală individuală 50%. 20% quiz-uri. 10% prezență. Fără examen scris și fără bancă de subiecte de examen.
- Echipe de cel mult 3 studenți; replicarea și extinderea unei lucrări de referință; proiectul se poate redacta și susține în română sau în engleză.
- AI permis și declarat (`AI_USE.md`); `AI_ERRORS.md` cu cel puțin trei erori AI depistate; folosirea nedeclarată = plagiat; fără AI la susținerea orală.

## Material privat (niciodată în repo)
- Materialele private nu se publică niciodată: proiecte și lucrări ale studenților, manuscrise nepublicate ale colegilor, capitole de carte nepublicate, PDF-uri de cărți și note de curs ale altor autori, rezultate cu proveniență neclară. Lista exactă a fișierelor este doar locală, în `.git/info/exclude`.

## Verificare finală
- Fiecare deck se compilează de două ori: 0 erori, 0 „Overfull \vbox” (`python3 latex/ats_build.py compile N`); randarea paginilor (pymupdf) și verificare vizuală; fișierele auxiliare sînt ignorate de git.
- Commit-uri locale cu `git add <căi>` explicite; fără push; fără linii Co-Authored-By / Generated-with.
