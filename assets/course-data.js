// ============================================================
// ATS course data (EN + RO). Rendered by assets/site.js.
// Analiza avansată a seriilor de timp și previziune / Advanced Time Series Analysis and Forecasting
// Master's programme Applied Statistics and Data Science (ASDS), year 1, semester 2, 7 ECTS.
// Chapter links: { type, href[, colab][, label] } for an existing file,
// { type, soon: true } for an item still in preparation (shown greyed, no link).
// A chapter with no existing file in a language shows "in preparation" only.
// Each chapter switches from soon(...) to real links when it is built (names: python3 latex/ats_chapters.py).
// ============================================================
(function () {
    const REPO = 'https://github.com/danpele/Advanced-Time-Series';
    const TREE = REPO + '/tree/main/';
    const COLAB = 'https://colab.research.google.com/github/danpele/Advanced-Time-Series/blob/main/';
    const TSA_SITE = 'https://danpele.github.io/Time-Series-Analysis/';

    // Quantinar courses, referenced by key from the chapters (URLs checked: HTTP 200, as on the TSA site)
    const Q = {
        tsaPython: ['Applied Time Series Analysis with Python', 'https://quantinar.com/course/137/applied-time-series-analysis-with-python'],
        sfm: ['Statistics of Financial Markets', 'https://quantinar.com/course/103/statistics-of-financial-markets'],
        statRisk: ['Measuring Statistical Risk', 'https://quantinar.com/course/100080/measuring-statistical-risk'],
        kalman: ['Kalman Filter', 'https://quantinar.com/course/42/methodology'],
        rf: ['Random Forests', 'https://quantinar.com/course/68/RF'],
        mlRisk: ['Machine learning in Financial Risk', 'https://quantinar.com/course/934/machine-learning-in-financial-risk'],
        nextWord: ['The Next Word Problem', 'https://quantinar.com/course/100100/the-next-word-problem-full-course'],
        xfg: ['XFG Advanced Methods in Quantitative Finance', 'https://quantinar.com/course/100067/xfg-advanced-methods-in-quantitative-finance']
    };
    const q = (...keys) => keys.map(k => ({ title: Q[k][0], url: Q[k][1] }));

    // helpers for chapter links
    const pdf = (type, href, label) => (label ? { type, href, label } : { type, href });
    const soon = type => ({ type, soon: true });
    const nb = (path, label) => Object.assign({ type: 'notebook', href: REPO + '/blob/main/' + path, colab: COLAB + path }, label ? { label } : {});
    const NB_LECT = { en: 'Lecture notebook', ro: 'Notebook curs' };
    const NB_SEM = { en: 'Seminar notebook', ro: 'Notebook seminar' };
    const ql = path => ({ type: 'quantlets', href: TREE + path });
    // a chapter still in preparation: every item greyed out, the same list on both pages
    const SOON = () => {
        const l = [soon('slides'), soon('seminar'), Object.assign(soon('notebook'), { label: NB_LECT }),
            Object.assign(soon('notebook'), { label: NB_SEM }), soon('quantlets')];
        return { en: l, ro: l };
    };
    // nb(...) and ql(...) give the notebook (with Colab) and Quantlet links when a chapter goes live

    window.ATS_DATA = {
        repo: REPO,

        // ---------------------------------------------------------------
        // UI strings
        // ---------------------------------------------------------------
        ui: {
            en: {
                pageTitle: 'Advanced Time Series Analysis and Forecasting - Course Website',
                courseTitle: 'Advanced Time Series Analysis and Forecasting',
                subtitle: "Master's programme Applied Statistics and Data Science, year 1, semester 2 | Faculty of Cybernetics, Statistics and Economic Informatics | Bucharest University of Economic Studies",
                nav: { home: 'Home', chapters: 'Chapters', project: 'Project', quizzes: 'Quizzes', resources: 'Resources', contact: 'Contact' },
                overview: 'Course Overview',
                objectives: 'Learning Objectives',
                heroTag: 'Forecast evaluation, structural identification, state space and regime models, volatility and risk, machine learning, foundation models and causal inference: advanced methods for dependent data, applied to real data in Python.',
                heroCta1: 'Explore the chapters',
                heroCta2: 'Team project',
                heroCta3: 'Attendance form',
                qrTeachers: 'For instructors: attendance QR code',
                qrLecture: 'lecture',
                qrSeminar: 'seminar',
                teacherBtn: 'Instructor access',
                teacherPrompt: 'Sign in with the instructor Google account to see the attendance QR code.',
                teacherDenied: 'This account has no instructor access.',
                close: 'Close',
                formulas: 'Key Formulas',
                chapters: 'Course Chapters',
                chapter: 'Chapter',
                chapterShort: 'Ch',
                comingSoon: 'In preparation',
                comingSoonShort: 'in preparation',
                chapterSoon: 'The materials of this chapter are in preparation.',
                selfStudy: 'Self-study',
                quantinar: 'Go deeper on Quantinar',
                links: {
                    slides: 'Lecture Slides', slidesExtra: 'Additional Slides', seminar: 'Seminar', seminarExtra: 'Additional Seminar',
                    notebook: 'Notebook', quantlets: 'Quantlets', colab: 'Open in Colab'
                },
                projectTitle: 'Team Project',
                aiTitle: 'Using AI in this course',
                quizzes: 'Chapter Quizzes',
                quizIntro: 'Each attempt draws up to 20 questions at random from the chapter bank and shuffles the answers. An answer is locked once selected. The quizzes count for 20% of the final grade; only your first attempt at each quiz is graded, later attempts are practice. A score is recorded only when you are signed in with your ASE account.',
                loginPrompt: 'Sign in with your ASE Google account (@ase.ro or @stud.ase.ro) to take the quizzes.',
                loginRequired: 'Sign in above with your ASE Google account to see this quiz.',
                loginWrongDomain: 'Please use your ASE account (@ase.ro or @stud.ase.ro).',
                saving: 'Saving your score...',
                saved: 'Your score has been recorded.',
                saveExpired: 'Your session has expired: sign out, sign in again and recalculate.',
                saveFailed: 'The score could not be saved. Please try again or tell the instructor.',
                loggedAs: 'Logged in as',
                logout: 'Logout',
                quizSoon: 'The quiz for this chapter will be published together with its materials.',
                question: 'Question',
                correct: 'Correct!',
                incorrect: 'Incorrect.',
                correctIs: 'The correct answer is',
                calc: 'Calculate Score',
                reset: 'New attempt',
                score: 'Score',
                unanswered: 'questions unanswered',
                verdicts: ['Keep practising!', 'Keep studying!', 'Good job!', 'Excellent!'],
                detailed: 'Detailed Results',
                colQ: 'Q', colQuestion: 'Question', colCorrect: 'Correct answer', colYours: 'Your answer', colResult: 'Result',
                resources: 'Resources',
                bibliography: 'Bibliography',
                dataSources: 'Data sources',
                contact: 'Contact',
                instructor: 'Lecturer',
                seminarCard: 'Seminar',
                seminarRole: 'Seminar instructor',
                office: 'Office Hours',
                officeText: 'By appointment',
                footer: 'Advanced Time Series Analysis and Forecasting | Faculty of Cybernetics, Statistics and Economic Informatics | Bucharest University of Economic Studies'
            },
            ro: {
                pageTitle: 'Analiza avansată a seriilor de timp și previziune - Site-ul cursului',
                courseTitle: 'Analiza avansată a seriilor de timp și previziune',
                subtitle: 'Programul de master Statistică aplicată și data science, anul I, semestrul 2 | Facultatea de Cibernetică, Statistică și Informatică Economică | Academia de Studii Economice din București',
                nav: { home: 'Acasă', chapters: 'Capitole', project: 'Proiect', quizzes: 'Quiz-uri', resources: 'Resurse', contact: 'Contact' },
                overview: 'Prezentarea cursului',
                objectives: 'Obiective de învățare',
                heroTag: 'Evaluarea prognozelor, identificare structurală, modele în spațiul stărilor și cu schimbare de regim, volatilitate și risc, machine learning, foundation models și inferență cauzală: metode avansate pentru date dependente, aplicate pe date reale în Python.',
                heroCta1: 'Explorați capitolele',
                heroCta2: 'Proiect de echipă',
                heroCta3: 'Formular de prezență',
                qrTeachers: 'Pentru cadre didactice: cod QR de prezență',
                qrLecture: 'curs',
                qrSeminar: 'seminar',
                teacherBtn: 'Acces cadre didactice',
                teacherPrompt: 'Autentificați-vă cu contul Google de cadru didactic pentru a vedea codul QR de prezență.',
                teacherDenied: 'Acest cont nu are acces de cadru didactic.',
                close: 'Închide',
                formulas: 'Formule-cheie',
                chapters: 'Capitolele cursului',
                chapter: 'Capitolul',
                chapterShort: 'Cap.',
                comingSoon: 'În pregătire',
                comingSoonShort: 'în pregătire',
                chapterSoon: 'Materialele acestui capitol sînt în pregătire.',
                selfStudy: 'Studiu individual',
                quantinar: 'Aprofundare pe Quantinar',
                links: {
                    slides: 'Slide-urile cursului', slidesExtra: 'Slide-uri suplimentare', seminar: 'Seminar', seminarExtra: 'Seminar suplimentar',
                    notebook: 'Notebook', quantlets: 'Quantlets', colab: 'Deschide în Colab'
                },
                projectTitle: 'Proiect de echipă',
                aiTitle: 'Utilizarea instrumentelor AI',
                quizzes: 'Quiz-uri pe capitole',
                quizIntro: 'La fiecare încercare se extrag aleator cel mult 20 de întrebări din banca de întrebări a capitolului, iar ordinea variantelor de răspuns se schimbă. Un răspuns ales nu mai poate fi modificat. Quiz-urile reprezintă 20% din nota finală; se notează doar prima încercare la fiecare quiz, celelalte sînt pentru exercițiu. Scorul se înregistrează numai dacă sînteți autentificat cu contul ASE.',
                loginPrompt: 'Autentificați-vă cu contul Google ASE (@ase.ro sau @stud.ase.ro) pentru a rezolva quiz-urile.',
                loginRequired: 'Autentificați-vă mai sus cu contul Google ASE pentru a vedea acest quiz.',
                loginWrongDomain: 'Folosiți contul ASE (@ase.ro sau @stud.ase.ro).',
                saving: 'Se salvează scorul...',
                saved: 'Scorul a fost înregistrat.',
                saveExpired: 'Sesiunea a expirat: deconectați-vă, autentificați-vă din nou și recalculați scorul.',
                saveFailed: 'Scorul nu a putut fi salvat. Încercați din nou sau anunțați titularul de curs.',
                loggedAs: 'Autentificat ca',
                logout: 'Deconectare',
                quizSoon: 'Quiz-ul acestui capitol va fi publicat odată cu materialele capitolului.',
                question: 'Întrebarea',
                correct: 'Corect!',
                incorrect: 'Greșit.',
                correctIs: 'Răspunsul corect este',
                calc: 'Calculează scorul',
                reset: 'Încercare nouă',
                score: 'Scor',
                unanswered: 'întrebări fără răspuns',
                verdicts: ['Mai exersați!', 'Mai studiați!', 'Bine!', 'Excelent!'],
                detailed: 'Rezultate detaliate',
                colQ: 'Nr.', colQuestion: 'Întrebare', colCorrect: 'Răspuns corect', colYours: 'Răspunsul ales', colResult: 'Rezultat',
                resources: 'Resurse',
                bibliography: 'Bibliografie',
                dataSources: 'Surse de date',
                contact: 'Contact',
                instructor: 'Titular de curs',
                seminarCard: 'Seminar',
                seminarRole: 'Titular de seminar',
                office: 'Program de consultații',
                officeText: 'Pe bază de programare',
                footer: 'Analiza avansată a seriilor de timp și previziune | Facultatea de Cibernetică, Statistică și Informatică Economică | Academia de Studii Economice din București'
            }
        },

        // ---------------------------------------------------------------
        // Overview cards and objectives
        // ---------------------------------------------------------------
        overview: {
            en: [
                { h: 'Course', p: ['Advanced Time Series Analysis and Forecasting', "Master's programme Applied Statistics and Data Science", 'Year 1, semester 2, academic year 2026/2027', '2 hours of lecture and 2 hours of seminar per week; 7 ECTS'] },
                { h: 'Prerequisites', p: [`<a href="${TSA_SITE}" target="_blank" rel="noopener">Time Series Analysis</a> (bachelor, Chapters 0–10) or an equivalent course: ARMA, ARIMA, GARCH, VAR, cointegration, state space models`, 'Mathematical statistics and econometrics at master level', 'Python (pandas, statsmodels)'] },
                { h: 'Assessment', p: ['Team project and individual oral defence: 70%', 'Chapter quizzes: 20%', 'Attendance: 10%', 'No written exam'] },
                { h: 'Main textbooks', p: ['Hamilton, <a href="https://doi.org/10.2307/j.ctv14jx6sm" target="_blank" rel="noopener"><em>Time Series Analysis</em></a>, Princeton University Press, 1994', 'Kilian &amp; Lütkepohl, <a href="https://doi.org/10.1017/9781108164818" target="_blank" rel="noopener"><em>Structural Vector Autoregressive Analysis</em></a>, Cambridge University Press, 2017', 'Durbin &amp; Koopman, <a href="https://doi.org/10.1093/acprof:oso/9780199641178.001.0001" target="_blank" rel="noopener"><em>Time Series Analysis by State Space Methods</em></a> (2nd ed.), Oxford University Press, 2012', 'Petropoulos et al., <a href="https://doi.org/10.1016/j.ijforecast.2021.11.001" target="_blank" rel="noopener">Forecasting: theory and practice</a>, <em>International Journal of Forecasting</em>, 2022 (open access)'] },
                { h: 'Tools', p: ['Python (statsmodels, arch, linearmodels, scikit-learn, PyTorch), Jupyter / Google Colab', 'GitHub, Quantlet, Quantinar'] }
            ],
            ro: [
                { h: 'Curs', p: ['Analiza avansată a seriilor de timp și previziune', 'Programul de master Statistică aplicată și data science', 'Anul I, semestrul 2, anul universitar 2026/2027', '2 ore de curs și 2 ore de seminar pe săptămînă; 7 credite ECTS'] },
                { h: 'Cunoștințe prealabile', p: [`<a href="${TSA_SITE}" target="_blank" rel="noopener">Serii de timp</a> (licență, capitolele 0–10) sau un curs echivalent: ARMA, ARIMA, GARCH, VAR, cointegrare, modele în spațiul stărilor`, 'Statistică matematică și econometrie la nivel de master', 'Programare în Python (pandas, statsmodels)'] },
                { h: 'Evaluare', p: ['Proiect de echipă și susținere orală individuală: 70%', 'Quiz-uri pe capitole: 20%', 'Prezență: 10%', 'Fără examen scris'] },
                { h: 'Manuale de bază', p: ['Hamilton, <a href="https://doi.org/10.2307/j.ctv14jx6sm" target="_blank" rel="noopener"><em>Time Series Analysis</em></a>, Princeton University Press, 1994', 'Kilian și Lütkepohl, <a href="https://doi.org/10.1017/9781108164818" target="_blank" rel="noopener"><em>Structural Vector Autoregressive Analysis</em></a>, Cambridge University Press, 2017', 'Durbin și Koopman, <a href="https://doi.org/10.1093/acprof:oso/9780199641178.001.0001" target="_blank" rel="noopener"><em>Time Series Analysis by State Space Methods</em></a> (ediția a 2-a), Oxford University Press, 2012', 'Petropoulos et al., <a href="https://doi.org/10.1016/j.ijforecast.2021.11.001" target="_blank" rel="noopener">Forecasting: theory and practice</a>, <em>International Journal of Forecasting</em>, 2022 (acces liber)'] },
                { h: 'Instrumente', p: ['Python (statsmodels, arch, linearmodels, scikit-learn, PyTorch), Jupyter / Google Colab', 'GitHub, Quantlet, Quantinar'] }
            ]
        },
        objectives: {
            en: [
                'Carry out valid inference with dependent data: long-run variances and HAC standard errors, block bootstrap, simulation-based inference',
                'Design, evaluate and combine point, interval and density forecasts with proper scoring rules and formal tests of predictive ability',
                'Identify structural shocks with SVARs and local projections, and model cointegrated, high-dimensional and mixed-frequency systems',
                'Build state space, regime-switching, long-memory and volatility models, and estimate them by maximum likelihood and Bayesian methods',
                'Apply machine learning, foundation models and conformal prediction to time series, with a fair comparison against statistical baselines',
                'Replicate and extend a landmark paper reproducibly, using AI tools in research while documenting and checking their output'
            ],
            ro: [
                'Realizarea unei inferențe valide pentru date dependente: varianța de termen lung și erorile standard HAC, bootstrap pe blocuri, inferență prin simulare',
                'Construirea, evaluarea și combinarea prognozelor punctuale, de interval și de densitate, cu reguli de scor proprii și teste formale ale capacității predictive',
                'Identificarea șocurilor structurale cu modele SVAR și proiecții locale; modelarea sistemelor cointegrate, de dimensiuni mari și cu frecvențe mixte',
                'Construirea modelelor în spațiul stărilor, a modelelor cu schimbare de regim, cu memorie lungă și de volatilitate, estimate prin verosimilitate maximă și prin metode bayesiene',
                'Aplicarea metodelor de machine learning, a foundation models și a predicției conformale pe serii de timp, comparate corect cu modelele statistice de referință',
                'Replicarea și extinderea reproductibilă a unei lucrări de referință, cu instrumente AI folosite în cercetare, documentate și verificate'
            ]
        },
        // ---------------------------------------------------------------
        // Key formulas (shown in a collapsible box on the chapter card); added chapter by chapter
        // ---------------------------------------------------------------
        formulas: [],
        // ---------------------------------------------------------------
        // Chapters 0-16. `id` is the stable key (quizzes, anchors, tabs);
        // `num` is only the display order. RO page -> RO files, EN page -> EN files.
        // Chapter 16 is self-study (selfStudy: true).
        // ---------------------------------------------------------------
        chapters: [
            {
                id: 'refresher', num: 0,
                title: { en: 'Refresher and inference for dependent data', ro: 'Recapitulare și inferență pentru date dependente' },
                topics: {
                    en: ['Course organisation and the project workflow; a refresher map of TSA (stationarity, ARMA, unit roots, GARCH, VAR, cointegration, state space)', 'Ergodicity and mixing; LLN and CLT for dependent data; the long-run variance; HAC estimators (Newey–West, Andrews bandwidth, kernels, fixed-b, LLSW/EWC) and the size of t-tests by Monte Carlo', 'Block bootstraps (moving, circular, stationary) and the wild bootstrap; overlapping observations; data snooping and White\'s Reality Check; reproducible research and replication packages'],
                    ro: ['Organizarea cursului și etapele proiectului; harta recapitulării din TSA (staționaritate, ARMA, rădăcini unitare, GARCH, VAR, cointegrare, spațiul stărilor)', 'Ergodicitate și mixing; legea numerelor mari și teorema limită centrală pentru date dependente; varianța pe termen lung; estimatori HAC (Newey–West, lățimea de bandă Andrews, nuclee, fixed-b, LLSW/EWC) și mărimea testelor t prin Monte Carlo', 'Bootstrap pe blocuri (mobile, circulare, staționar) și wild bootstrap; observații suprapuse; data snooping și testul Reality Check al lui White; cercetare reproductibilă și pachete de replicare']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter0_refresher_inference.pdf'), pdf('seminar', 'EN/Seminars/seminar0_refresher_inference.pdf'),
                         nb('notebooks/EN/chapter0_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter0_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_00')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol0_recapitulare_inferenta.pdf'), pdf('seminar', 'RO/Seminarii/seminar0_recapitulare_inferenta_ro.pdf'),
                         nb('notebooks/EN/chapter0_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter0_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_00')]
                },
                quantinar: q('tsaPython')
            },
            {
                id: 'forecast-evaluation', num: 1,
                title: { en: 'Forecast evaluation, scoring rules and combination', ro: 'Evaluarea prognozelor, reguli de scor și combinarea prognozelor' },
                topics: {
                    en: ['Loss functions, consistency and Bregman losses; calibration, PIT and proper scoring rules (log score, CRPS, interval and energy scores), elicitability', 'Comparing forecasts: Diebold–Mariano with HAC and HLN, Giacomini–White, Clark–West, Mincer–Zarnowitz, encompassing, reality check, SPA and the Model Confidence Set', 'Forecast combination: Bates–Granger, the combination puzzle, density pools, SPF combinations, M4/M5 lessons; real-time data'],
                    ro: ['Funcții de pierdere, consistență și pierderi Bregman; calibrare, PIT și reguli de scor proprii (scorul logaritmic, CRPS, scorul de interval, energy score), elicitabilitate', 'Compararea prognozelor: Diebold–Mariano cu HAC și HLN, Giacomini–White, Clark–West, Mincer–Zarnowitz, testul de încadrare (encompassing), reality check, SPA și Model Confidence Set', 'Combinarea prognozelor: Bates–Granger, paradoxul combinării, combinarea densităților, combinări pentru SPF, lecțiile M4/M5; date în timp real']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter1_forecast_evaluation.pdf'), pdf('seminar', 'EN/Seminars/seminar1_forecast_evaluation.pdf'),
                         nb('notebooks/EN/chapter1_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter1_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_01')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol1_evaluarea_prognozelor.pdf'), pdf('seminar', 'RO/Seminarii/seminar1_evaluarea_prognozelor_ro.pdf'),
                         nb('notebooks/EN/chapter1_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter1_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_01')]
                }
            },
            {
                id: 'breaks-nonlinear', num: 2,
                title: { en: 'Structural breaks and nonlinear models', ro: 'Rupturi structurale și modele neliniare' },
                topics: {
                    en: ['Breaks at unknown dates: Chow, sup/exp/ave-Wald, Bai–Perron multiple breaks with confidence intervals; real-time CUSUM monitoring and ICSS variance breaks (US real rate, Romanian inflation, EUR/RON)', 'Threshold and smooth-transition models: SETAR, LSTAR, ESTAR; Hansen\'s bootstrap and LR threshold intervals, LM linearity tests (lynx, US unemployment, PPP)', 'Forecasting under instability: estimation windows, averaging across windows, nonlinear forecasts by simulation; breaks versus nonlinearity'],
                    ro: ['Rupturi la date necunoscute: Chow, sup/exp/ave-Wald, rupturi multiple Bai–Perron cu intervale de încredere; monitorizare CUSUM în timp real și rupturi în varianță ICSS (rata reală din SUA, inflația din România, EUR/RON)', 'Modele cu prag și cu tranziție netedă: SETAR, LSTAR, ESTAR; bootstrap-ul lui Hansen și intervalele LR pentru prag, teste LM de liniaritate (linxul, șomajul din SUA, paritatea puterii de cumpărare)', 'Prognoza în condiții de instabilitate: ferestre de estimare, medierea peste ferestre, prognoze neliniare prin simulare; rupturi sau neliniaritate']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter2_structural_breaks_nonlinear_models.pdf'), pdf('seminar', 'EN/Seminars/seminar2_structural_breaks_nonlinear_models.pdf'),
                         nb('notebooks/EN/chapter2_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter2_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_02')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol2_rupturi_structurale_modele_neliniare.pdf'), pdf('seminar', 'RO/Seminarii/seminar2_rupturi_structurale_modele_neliniare_ro.pdf'),
                         nb('notebooks/EN/chapter2_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter2_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_02')]
                }
            },
            {
                id: 'svar-lp', num: 3,
                title: { en: 'Structural VAR and local projections', ro: 'Modele VAR structurale și proiecții locale' },
                topics: {
                    en: ['Identification in structural VARs: recursive and non-recursive short-run, long-run (Blanchard–Quah), sign, narrative and heteroskedasticity-based restrictions; set identification and its inference', 'External instruments (proxy SVAR) and high-frequency monetary policy surprises; bootstrap, bias-corrected and weak-instrument-robust inference for impulse responses', 'Local projections and VARs: the bias–variance trade-off, LP-IV, lag-augmented inference, state-dependent multipliers; Romania and euro-area spillovers'],
                    ro: ['Identificarea în modelele VAR structurale: restricții pe termen scurt recursive și nerecursive, restricții pe termen lung (Blanchard–Quah), de semn, narative și prin heteroscedasticitate; identificarea pe mulțimi și inferența corespunzătoare', 'Instrumente externe (proxy SVAR) și surprize de politică monetară la frecvență înaltă; inferență bootstrap, cu corecția deplasării și robustă la instrumente slabe pentru funcțiile de răspuns la impuls', 'Proiecții locale comparate cu modelele VAR: compromisul dintre deplasare și varianță, LP-IV, inferență cu decalaje suplimentare, multiplicatori dependenți de stare; România și efectele de propagare din zona euro']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter3_structural_var_local_projections.pdf'), pdf('seminar', 'EN/Seminars/seminar3_structural_var_local_projections.pdf'),
                         nb('notebooks/EN/chapter3_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter3_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_03')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol3_modele_var_structurale_proiectii_locale.pdf'), pdf('seminar', 'RO/Seminarii/seminar3_modele_var_structurale_proiectii_locale_ro.pdf'),
                         nb('notebooks/EN/chapter3_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter3_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_03')]
                }
            },
            {
                id: 'cointegration-panel', num: 4,
                title: { en: 'Cointegration revisited: VECM, ARDL and panel data', ro: 'Cointegrare: VECM, ARDL și date panel' },
                topics: {
                    en: ['Johansen maximum likelihood in depth: reduced-rank regression, the five deterministic cases, small-sample corrections and wild-bootstrap rank tests; identification and LR tests on cointegrating vectors and adjustment coefficients; the common-trends structural VECM (King–Plosser–Stock–Watson)', 'ARDL bounds testing (Pesaran–Shin–Smith) with small-sample critical values, ARDL against VECM, Toda–Yamamoto, nonlinear ARDL; interest-rate pass-through in Romania', 'Panel time series: cross-section dependence (CD), LLC, IPS and CIPS, Pedroni and Westerlund tests, MG, PMG and CCE estimators; EU-27 consumption'],
                    ro: ['Metoda verosimilității maxime a lui Johansen în detaliu: regresia de rang redus, cele cinci cazuri deterministe, corecții pentru eșantioane mici și teste de rang cu wild bootstrap; identificarea și testele LR asupra vectorilor de cointegrare și a coeficienților de ajustare; VECM structural cu trenduri comune (King–Plosser–Stock–Watson)', 'Testul bounds ARDL (Pesaran–Shin–Smith) cu valori critice pentru eșantioane mici, ARDL comparat cu VECM, Toda–Yamamoto, ARDL neliniar; transmiterea dobînzilor în România', 'Serii de timp panel: dependența între unități (testul CD), testele LLC, IPS și CIPS, testele Pedroni și Westerlund, estimatorii MG, PMG și CCE; consumul în UE-27']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter4_cointegration_vecm_ardl_panel.pdf'), pdf('seminar', 'EN/Seminars/seminar4_cointegration_vecm_ardl_panel.pdf'),
                         nb('notebooks/EN/chapter4_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter4_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_04')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol4_cointegrare_vecm_ardl_panel.pdf'), pdf('seminar', 'RO/Seminarii/seminar4_cointegrare_vecm_ardl_panel_ro.pdf'),
                         nb('notebooks/EN/chapter4_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter4_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_04')]
                }
            },
            {
                id: 'bvar-nowcasting', num: 5,
                title: { en: 'Bayesian VAR, factor models and nowcasting', ro: 'Modele VAR bayesiene, modele factoriale și nowcasting' },
                topics: {
                    en: ['Bayesian inference for VARs: conjugate Normal–inverse-Wishart and Minnesota priors, dummy observations, Gibbs sampling and MCMC diagnostics, shrinkage chosen by the marginal likelihood (GLP); large BVARs (Bańbura–Giannone–Reichlin) with posterior impulse-response bands', 'Approximate factor models: principal components with EM, Bai–Ng criteria, diffusion-index forecasts, FAVAR; the FRED-MD database', 'Nowcasting Romanian GDP with mixed frequencies and a ragged edge: bridge equations, MIDAS, dynamic factor models with the Kalman filter (two-step and EM), the news decomposition'],
                    ro: ['Inferență bayesiană pentru VAR: distribuții a priori Normal–inverse-Wishart și Minnesota, observații fictive, eșantionarea Gibbs și diagnosticarea MCMC, shrinkage ales prin verosimilitatea marginală (GLP); modele BVAR mari (Bańbura–Giannone–Reichlin) cu benzi a posteriori pentru răspunsurile la impuls', 'Modele factoriale aproximative: componente principale cu EM, criteriile Bai–Ng, prognoze cu indici de difuziune, FAVAR; baza de date FRED-MD', 'Nowcasting pentru PIB-ul României cu frecvențe mixte și date incomplete la sfîrșitul eșantionului: ecuații punte, MIDAS, modele factoriale dinamice cu filtrul Kalman (în doi pași și EM), descompunerea pe știri']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter5_bvar_factor_models_nowcasting.pdf'), pdf('seminar', 'EN/Seminars/seminar5_bvar_factor_models_nowcasting.pdf'),
                         nb('notebooks/EN/chapter5_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter5_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_05')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol5_bvar_modele_factoriale_nowcasting.pdf'), pdf('seminar', 'RO/Seminarii/seminar5_bvar_modele_factoriale_nowcasting_ro.pdf'),
                         nb('notebooks/EN/chapter5_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter5_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_05')]
                }
            },
            {
                id: 'state-space', num: 6,
                title: { en: 'State space models and Bayesian filtering', ro: 'Modele în spațiul stărilor și filtrare bayesiană' },
                topics: {
                    en: ['The general linear Gaussian model: Kalman filter and smoother with exact diffuse initialisation, the exact likelihood and inference at the boundary (pile-up); simulation smoothers and Gibbs sampling', 'Stochastic volatility (KSC mixture) and why it is not GARCH; extended, unscented and particle filters (bootstrap, auxiliary), particle MCMC', 'TVP regressions and TVP-VAR-SV, the DFM in state-space form, trend–cycle decompositions (Beveridge–Nelson, Morley–Nelson–Zivot), UC-SV trend inflation in the US and Romania'],
                    ro: ['Modelul liniar gaussian general: filtrul și netezitorul Kalman cu inițializare difuză exactă, verosimilitatea exactă și inferența la frontieră (pile-up); simulation smoothers și eșantionare Gibbs', 'Volatilitatea stochastică (mixtura KSC) și diferența față de GARCH; filtrele Kalman extins și unscented, filtre de particule (bootstrap, auxiliar), particle MCMC', 'Regresii TVP și TVP-VAR-SV, DFM în spațiul stărilor, descompuneri trend–ciclu (Beveridge–Nelson, Morley–Nelson–Zivot), inflația de trend UC-SV pentru SUA și România']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter6_state_space_models_bayesian_filtering.pdf'), pdf('seminar', 'EN/Seminars/seminar6_state_space_models_bayesian_filtering.pdf'),
                         nb('notebooks/EN/chapter6_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter6_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_06')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol6_modele_spatiul_starilor_filtrare_bayesiana.pdf'), pdf('seminar', 'RO/Seminarii/seminar6_modele_spatiul_starilor_filtrare_bayesiana_ro.pdf'),
                         nb('notebooks/EN/chapter6_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter6_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_06')]
                },
                quantinar: q('kalman')
            },
            {
                id: 'regime-switching', num: 7,
                title: { en: 'Regime-switching models', ro: 'Modele cu schimbare de regim' },
                topics: {
                    en: ['The Hamilton filter and Kim smoother derived; estimation by EM and numerical ML; identification, label switching and testing the number of regimes', 'Time-varying transition probabilities, Markov-switching VARs and MS-GARCH; Bayesian estimation by Gibbs sampling', 'Regimes, breaks and long memory; forecasting and its evaluation; US business cycles, Romanian inflation and GDP, S&P 500, BET and EUR/RON'],
                    ro: ['Filtrul Hamilton și netezitorul Kim, cu derivare completă; estimarea prin EM și verosimilitate maximă numerică; identificare, schimbarea etichetelor (label switching) și testarea numărului de regimuri', 'Probabilități de tranziție variabile în timp, modele VAR și GARCH cu schimbare de regim; estimarea bayesiană prin eșantionare Gibbs', 'Regimuri, rupturi și memorie lungă; prognoza și evaluarea ei; ciclul economic din SUA, inflația și PIB-ul României, S&P 500, BET și EUR/RON']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter7_regime_switching_models.pdf'), pdf('seminar', 'EN/Seminars/seminar7_regime_switching_models.pdf'),
                         nb('notebooks/EN/chapter7_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter7_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_07')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol7_modele_schimbare_regim.pdf'), pdf('seminar', 'RO/Seminarii/seminar7_modele_schimbare_regim_ro.pdf'),
                         nb('notebooks/EN/chapter7_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter7_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_07')]
                }
            },
            {
                id: 'volatility', num: 8,
                title: { en: 'Advanced volatility modelling: realised measures, HAR and multivariate GARCH', ro: 'Modelarea avansată a volatilității: măsuri realizate, HAR și GARCH multivariat' },
                topics: {
                    en: ['Quasi-maximum likelihood for GARCH and robust standard errors; long-run components: component GARCH and GARCH-MIDAS with macroeconomic drivers', 'Realised measures: the CLT of realised variance, microstructure noise and realised kernels, bipower variation and jump tests', 'HAR, HARQ, Realized GARCH and HEAVY; robust loss functions; DCC, cDCC, DCC-NL and realised covariance'],
                    ro: ['Verosimilitatea cvasi-maximă pentru GARCH și erorile standard robuste; componente de termen lung: component GARCH și GARCH-MIDAS cu factori macroeconomici', 'Măsuri realizate: teorema limită centrală pentru varianța realizată, zgomotul de microstructură și realised kernels, variația bipower și testele de salt', 'HAR, HARQ, Realized GARCH și HEAVY; funcții de pierdere robuste; DCC, cDCC, DCC-NL și covarianța realizată']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter8_advanced_volatility.pdf'), pdf('seminar', 'EN/Seminars/seminar8_advanced_volatility.pdf'),
                         nb('notebooks/EN/chapter8_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter8_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_08')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol8_volatilitate_avansata.pdf'), pdf('seminar', 'RO/Seminarii/seminar8_volatilitate_avansata_ro.pdf'),
                         nb('notebooks/EN/chapter8_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter8_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_08')]
                },
                quantinar: q('sfm')
            },
            {
                id: 'var-es', num: 9,
                title: { en: 'VaR, ES and backtesting: elicitability, scoring and model risk', ro: 'VaR, ES și backtesting: elicitabilitate, funcții de scor și riscul de model' },
                topics: {
                    en: ['VaR 1% and ES 2.5% as forecast functionals; elicitability, the Fissler–Ziegel class, the FZ0 loss and Murphy diagrams', 'Quantile regression and CAViaR (Engle–Manganelli), semiparametric GAS models for (VaR, ES) (Patton–Ziegel–Chen) and joint VaR–ES regression, replicated on S&P 500, DAX, BET, EUR/RON and Bitcoin', 'Backtesting as conditional calibration with estimation risk; MCS comparisons in the 2008, 2020, 2022 and 2025 stress periods; square-root-of-time, model risk, the extremal index and conformal calibration'],
                    ro: ['VaR 1% și ES 2,5% ca funcționale de prognoză; elicitabilitate, clasa Fissler–Ziegel, pierderea FZ0 și diagramele Murphy', 'Regresia cuantilică și CAViaR (Engle–Manganelli), modele GAS semiparametrice pentru (VaR, ES) (Patton–Ziegel–Chen) și regresia comună VaR–ES, replicate pe S&P 500, DAX, BET, EUR/RON și Bitcoin', 'Backtesting ca test de calibrare condiționată, cu risc de estimare; comparații MCS în perioadele de criză 2008, 2020, 2022 și 2025; regula rădăcinii pătrate a timpului, riscul de model, indicele extremal și calibrarea conformală']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter9_var_es_backtesting.pdf'), pdf('seminar', 'EN/Seminars/seminar9_var_es_backtesting.pdf'),
                         nb('notebooks/EN/chapter9_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter9_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_09')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol9_var_es_backtesting.pdf'), pdf('seminar', 'RO/Seminarii/seminar9_var_es_backtesting_ro.pdf'),
                         nb('notebooks/EN/chapter9_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter9_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_09')]
                },
                quantinar: q('statRisk', 'xfg')
            },
            {
                id: 'long-memory', num: 10,
                title: { en: 'Long memory and rough volatility', ro: 'Memorie lungă și rough volatility' },
                topics: {
                    en: ['Spectral characterisation of long memory; asymptotics of GPH, local Whittle and exact local Whittle; bandwidth and bias', 'Testing long memory against level shifts (Qu 2011); inflation persistence; fractional cointegration (FCVAR); FIGARCH, HYGARCH, LMSV and HAR as an approximation', 'Rough volatility: fractional Brownian motion and its simulation, the Gatheral–Jaisson–Rosenbaum evidence and its critiques, RFSV forecasts against HAR'],
                    ro: ['Caracterizarea spectrală a memoriei lungi; asimptotica estimatorilor GPH, local Whittle și local Whittle exact; lățimea de bandă și deplasarea', 'Testarea memoriei lungi față de salturile de nivel (Qu 2011); persistența inflației; cointegrarea fracționară (FCVAR); FIGARCH, HYGARCH, LMSV și HAR ca aproximare', 'Rough volatility: mișcarea browniană fracționară și simularea ei, dovezile Gatheral–Jaisson–Rosenbaum și criticile lor, prognoze RFSV comparate cu HAR']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter10_long_memory_rough_volatility.pdf'), pdf('seminar', 'EN/Seminars/seminar10_long_memory_rough_volatility.pdf'),
                         nb('notebooks/EN/chapter10_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter10_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_10')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol10_memorie_lunga_rough_volatility.pdf'), pdf('seminar', 'RO/Seminarii/seminar10_memorie_lunga_rough_volatility_ro.pdf'),
                         nb('notebooks/EN/chapter10_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter10_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_10')]
                }
            },
            {
                id: 'spectral-wavelet', num: 11,
                title: { en: 'Spectral and wavelet analysis', ro: 'Analiză spectrală și analiză wavelet' },
                topics: {
                    en: ['Spectral estimation theory: bias–variance and bandwidth, multitaper estimation and Thomson\'s F test; coherence, phase, gain and dynamic correlation', 'Granger causality by frequency (Geweke; Breitung–Candelon); band-pass filters (Baxter–King, Christiano–Fitzgerald), Hamilton\'s critique of the HP filter and business-cycle synchronisation of Romania with the euro area', 'Evolutionary spectra; wavelets: MODWT, variance, correlation and beta by scale; wavelet coherence with Monte Carlo significance (BET, DAX, S&P 500, oil, CEE inflation)'],
                    ro: ['Teoria estimării spectrale: deplasare–varianță și lățimea de bandă, estimarea multitaper și testul F al lui Thomson; coerența, faza, cîștigul și corelația dinamică', 'Cauzalitatea Granger pe frecvențe (Geweke; Breitung–Candelon); filtre trece-bandă (Baxter–King, Christiano–Fitzgerald), critica lui Hamilton la adresa filtrului HP și sincronizarea ciclului economic al României cu zona euro', 'Spectre evolutive; wavelets: MODWT, varianța, corelația și beta pe scale; coerența wavelet cu semnificație Monte Carlo (BET, DAX, S&P 500, petrol, inflația din Europa Centrală și de Est)']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter11_spectral_wavelet_analysis.pdf'), pdf('seminar', 'EN/Seminars/seminar11_spectral_wavelet_analysis.pdf'),
                         nb('notebooks/EN/chapter11_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter11_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_11')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol11_analiza_spectrala_analiza_wavelet.pdf'), pdf('seminar', 'RO/Seminarii/seminar11_analiza_spectrala_analiza_wavelet_ro.pdf'),
                         nb('notebooks/EN/chapter11_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter11_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_11')]
                }
            },
            {
                id: 'ml-dl', num: 12,
                title: { en: 'Machine learning and deep learning for time series', ro: 'Machine learning și deep learning pentru serii de timp' },
                topics: {
                    en: ['Learning from dependent data: mixing, when cross-validation is valid (Bergmeir–Hyndman–Koo), leakage; global and local models; lasso, adaptive lasso, elastic net and post-selection inference', 'Tree ensembles in depth (QRF, boosting with monotone constraints); RNN/LSTM/GRU and vanishing gradients, TCN, attention and Transformers, the Zeng et al. critique, DLinear and PatchTST; N-BEATS, N-HiTS, DeepAR, TFT', 'Interpretation (Shapley values, attention is not explanation) and honest benchmarks: strong baselines, DM/MCS/SPA, seeds and data snooping; M4 and M5 lessons'],
                    ro: ['Învățarea din date dependente: mixing, condițiile în care validarea încrucișată este validă (Bergmeir–Hyndman–Koo), scurgerea de informație; modele globale și locale; lasso, lasso adaptiv, elastic net și inferența după selecție', 'Ansambluri de arbori în profunzime (QRF, boosting cu restricții de monotonie); RNN/LSTM/GRU și stingerea gradienților, TCN, atenție și Transformers, critica lui Zeng et al., DLinear și PatchTST; N-BEATS, N-HiTS, DeepAR, TFT', 'Interpretare (valori Shapley; atenția nu este explicație) și comparații oneste: modele de referință puternice, DM/MCS/SPA, seed-uri și data snooping; lecțiile M4 și M5']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter12_machine_learning_deep_learning.pdf'), pdf('seminar', 'EN/Seminars/seminar12_machine_learning_deep_learning.pdf'),
                         nb('notebooks/EN/chapter12_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter12_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_12')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol12_machine_learning_deep_learning.pdf'), pdf('seminar', 'RO/Seminarii/seminar12_machine_learning_deep_learning_ro.pdf'),
                         nb('notebooks/EN/chapter12_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter12_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_12')]
                },
                quantinar: q('rf', 'mlRisk')
            },
            {
                id: 'foundation-conformal', num: 13,
                title: { en: 'Foundation models and conformal prediction', ro: 'Foundation models și predicție conformală' },
                topics: {
                    en: ['Time series foundation models: pretraining data, tokenisation and patching, scaling evidence; Chronos, Chronos-Bolt and Chronos-2, TimesFM, Moirai, Lag-Llama, MOMENT, Toto, TiRex; zero-shot use, fine-tuning and covariates in context; language models for time series and their critique', 'Benchmark methodology: GIFT-Eval and fev-bench, leakage and contamination, evaluation after model release, tests across many series (DM, MCS, Holm, Benjamini–Hochberg); evidence on Romanian load, EU inflation and realised volatility', 'Conformal prediction: exchangeability, split conformal, CQR and the limits of conditional coverage; for dependent data: weighted conformal, EnbPI, ACI and conformal PID; coverage diagnostics; calibrating foundation-model intervals and VaR'],
                    ro: ['Foundation models pentru serii de timp: datele de preantrenare, tokenizare și patching, dovezi de scalare; Chronos, Chronos-Bolt și Chronos-2, TimesFM, Moirai, Lag-Llama, MOMENT, Toto, TiRex; zero-shot, fine-tuning și covariabile în context; modele de limbaj pentru serii de timp și critica lor', 'Metodologia benchmark-urilor: GIFT-Eval și fev-bench, scurgerea de informație și contaminarea, evaluarea după lansarea modelelor, testarea pe multe serii (DM, MCS, Holm, Benjamini–Hochberg); dovezi pe consumul de energie electrică al României, inflația din UE și volatilitatea realizată', 'Predicția conformală: interschimbabilitate, split conformal, CQR și limitele acoperirii condiționate; pentru date dependente: conformal ponderat, EnbPI, ACI și PID conformal; diagnosticarea acoperirii; calibrarea intervalelor produse de foundation models și a VaR']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter13_foundation_models_conformal.pdf'), pdf('seminar', 'EN/Seminars/seminar13_foundation_models_conformal.pdf'),
                         nb('notebooks/EN/chapter13_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter13_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_13')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol13_foundation_models_conformal.pdf'), pdf('seminar', 'RO/Seminarii/seminar13_foundation_models_conformal_ro.pdf'),
                         nb('notebooks/EN/chapter13_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter13_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_13')]
                },
                quantinar: q('nextWord')
            },
            {
                id: 'causal', num: 14,
                title: { en: 'Causal inference for time series', ro: 'Inferență cauzală pentru serii de timp' },
                topics: {
                    en: ['Granger causality against causal effects: potential outcomes for time series, conditional tests with HAC, transfer entropy; PCMCI and convergent cross mapping', 'Interrupted time series and event studies with dependent errors; synthetic control (replication of German reunification and of the Brexit doppelganger), augmented SC, synthetic DiD, staggered DiD', 'CausalImpact (BSTS) and DML; the 2025 VAT increase and the end of the electricity price cap in Romania; the spot Bitcoin ETFs'],
                    ro: ['Cauzalitatea Granger comparată cu efectele cauzale: rezultate potențiale pentru serii de timp, teste condiționate cu HAC, entropia de transfer; PCMCI și convergent cross mapping', 'Serii de timp întrerupte și studii de eveniment cu erori dependente; controlul sintetic (replicarea reunificării Germaniei și a dublurii Brexit), controlul sintetic augmentat, DiD sintetic, DiD eșalonat', 'CausalImpact (BSTS) și DML; majorarea TVA și încheierea plafonării prețului energiei electrice în România în 2025; ETF-urile spot pe Bitcoin']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter14_causal_inference_time_series.pdf'), pdf('seminar', 'EN/Seminars/seminar14_causal_inference_time_series.pdf'),
                         nb('notebooks/EN/chapter14_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter14_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_14')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol14_inferenta_cauzala_serii_timp.pdf'), pdf('seminar', 'RO/Seminarii/seminar14_inferenta_cauzala_serii_timp_ro.pdf'),
                         nb('notebooks/EN/chapter14_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter14_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_14')]
                }
            },
            {
                id: 'review', num: 15,
                title: { en: 'Review and project defence', ro: 'Recapitulare și susținerea proiectelor' },
                topics: {
                    en: ['The course map: one synthesis per chapter with its key formula, replication result and common mistakes; a toolbox of methods by research question', 'The project: the research workflow from question to report, pre-registration and the power of the evaluation, replicating a landmark paper (what replicated in the course, what did not and why), reproducibility, data snooping, leakage, look-ahead and overclaiming', 'The individual oral defence: format, grading criteria, typical questions with model answers; AI_USE.md and AI_ERRORS.md'],
                    ro: ['Harta cursului: o sinteză pentru fiecare capitol, cu formula-cheie, rezultatul replicării și greșelile frecvente; trusa de metode după întrebarea de cercetare', 'Proiectul: fluxul de cercetare de la întrebare la raport, preînregistrarea și puterea evaluării, replicarea unei lucrări de referință (ce s-a replicat în curs, ce nu și de ce), reproductibilitatea, data snooping, scurgerea de informație, look-ahead și afirmațiile exagerate', 'Susținerea orală individuală: format, criterii de evaluare, întrebări tipice cu răspunsuri-model; AI_USE.md și AI_ERRORS.md']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter15_review_project_defence.pdf'), pdf('seminar', 'EN/Seminars/seminar15_review_project_defence.pdf'),
                         nb('notebooks/EN/chapter15_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter15_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_15')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol15_recapitulare_proiecte.pdf'), pdf('seminar', 'RO/Seminarii/seminar15_recapitulare_proiecte_ro.pdf'),
                         nb('notebooks/EN/chapter15_lecture_notebook.ipynb', NB_LECT), nb('notebooks/EN/chapter15_seminar_notebook.ipynb', NB_SEM), ql('Quantlets/Ch_15')]
                }
            },
            {
                id: 'bubbles', num: 16, selfStudy: true,
                title: { en: 'Explosive roots and bubbles', ro: 'Rădăcini explozive și bule speculative' },
                topics: {
                    en: ['Rational bubbles (Blanchard–Watson, Diba–Grossman, Evans) and explosive autoregressions: Cauchy limits, mildly explosive asymptotics', 'SADF, GSADF and BSADF: critical values, wild bootstrap under changing volatility, family-wise control of false alarms, date-stamping accuracy and real-time monitoring', 'Fundamentals against prices (US and Romanian price-to-rent), LPPLS confidence indicators and critical-time inference, early-warning evaluation with base rates'],
                    ro: ['Bule raționale (Blanchard–Watson, Diba–Grossman, Evans) și procese autoregresive explozive: limite Cauchy, asimptotica proceselor slab explozive', 'SADF, GSADF și BSADF: valori critice, wild bootstrap sub volatilitate variabilă, controlul alarmelor false la nivel de familie, acuratețea datării și monitorizarea în timp real', 'Fundamentele comparate cu prețurile (raportul preț/chirie în SUA și România), indicatorii de încredere LPPLS și inferența asupra timpului critic, evaluarea avertizărilor timpurii pe baza frecvențelor de bază']
                },
                links: {
                    en: [pdf('slides', 'EN/Courses/chapter16_explosive_roots_bubbles.pdf'),
                         nb('notebooks/EN/chapter16_lecture_notebook.ipynb', NB_LECT), ql('Quantlets/Ch_16')],
                    ro: [pdf('slides', 'RO/Cursuri/capitol16_radacini_explozive_bule_speculative.pdf'),
                         nb('notebooks/EN/chapter16_lecture_notebook.ipynb', NB_LECT), ql('Quantlets/Ch_16')]
                }
            }
        ],

        // ---------------------------------------------------------------
        // Team project (section #project) and AI policy
        // ---------------------------------------------------------------
        project: {
            en: [
                { h: 'The project', p: ['Teams of up to 3 students replicate a landmark paper of the course (one of the case studies of the chapters, or another paper approved by the instructor) and extend it with the methods of ATS, preferably on Romanian or EU data.', 'The project can be written and defended in Romanian or in English.'] },
                { h: 'Deliverables and weights (70% of the final grade)', p: ['<strong>Proposal and pre-registration: 5%</strong> (team). The research question, the paper to replicate, the data, and the forecast evaluation design (loss functions, tests, sample split), fixed before any estimation.', '<strong>Replication and extension: 15%</strong> (team). A GitHub repository whose code reproduces every number and chart (runnable in Colab), a short report in the format of a paper, <code>AI_USE.md</code> and <code>AI_ERRORS.md</code>.', '<strong>Individual oral defence: 50%</strong>. Each member is examined separately (format and rubric below).'] },
                { h: 'The oral defence', p: ['Individual, about 15 minutes per student: 5 minutes of presentation of the student\'s own contribution (the part of the project the student led), then 10 minutes of questions on the code, the method and the results.', 'Rubric (100 points; the defence grade is the score divided by 10): mastery of the method 25; ownership of the code and data 20; inference and interpretation 25; replication and robustness 20; research integrity and AI use 10.', 'A student who cannot explain the code they submitted cannot pass. No AI tools during the defence.'] },
                { h: 'Grading criteria', p: ['A faithful replication, or a documented explanation of why a published number cannot be reproduced; an extension that answers a new question; an honest out-of-sample evaluation with the tools of Chapter 1; valid inference for dependent data.', 'Grades can differ between the members of a team, following the oral defence.'] },
                { h: 'Rest of the grade', p: ['Chapter quizzes: 20% (online, with the ASE account; the first attempt at each quiz is graded).', 'Attendance: 10%.', 'There is no written exam.'] }
            ],
            ro: [
                { h: 'Proiectul', p: ['Echipe de cel mult 3 studenți replică o lucrare de referință a cursului (unul dintre studiile de caz ale capitolelor sau o altă lucrare aprobată de titular) și o extind cu metodele cursului, de preferință pe date din România sau din Uniunea Europeană.', 'Proiectul poate fi redactat și susținut în limba română sau în limba engleză.'] },
                { h: 'Livrabile și ponderi (70% din nota finală)', p: ['<strong>Propunerea și preînregistrarea: 5%</strong> (echipă). Întrebarea de cercetare, lucrarea replicată, datele și planul de evaluare a prognozelor (funcții de pierdere, teste, împărțirea eșantionului), fixate înaintea oricărei estimări.', '<strong>Replicarea și extensia: 15%</strong> (echipă). Un repository GitHub cu codul care reproduce fiecare rezultat numeric și fiecare grafic (rulabil în Colab), un raport scurt în forma unui articol, <code>AI_USE.md</code> și <code>AI_ERRORS.md</code>.', '<strong>Susținerea orală individuală: 50%</strong>. Fiecare membru este examinat separat (formatul și criteriile sînt descrise mai jos).'] },
                { h: 'Susținerea orală', p: ['Individuală, circa 15 minute pentru fiecare student: 5 minute de prezentare a contribuției proprii (partea de proiect coordonată de student), apoi 10 minute de întrebări despre cod, metodă și rezultate.', 'Criterii de evaluare (100 de puncte; nota la susținere este punctajul împărțit la 10): stăpînirea metodei 25; stăpînirea codului și a datelor 20; inferența și interpretarea 25; replicarea și robustețea 20; integritatea cercetării și folosirea AI 10.', 'Un student care nu poate explica codul predat nu poate promova. În timpul susținerii nu se folosesc instrumente AI.'] },
                { h: 'Criterii de evaluare', p: ['O replicare fidelă sau o explicație documentată a motivului pentru care un rezultat publicat nu poate fi reprodus; o extensie care răspunde unei întrebări noi; o evaluare corectă în afara eșantionului, cu instrumentele din capitolul 1; o inferență validă pentru date dependente.', 'Notele membrilor unei echipe pot fi diferite, în funcție de susținerea orală.'] },
                { h: 'Restul notei', p: ['Quiz-uri pe capitole: 20% (online, cu contul ASE; se notează prima încercare la fiecare quiz).', 'Prezență: 10%.', 'Cursul nu are examen scris.'] }
            ]
        },
        aiPolicy: {
            en: ['AI tools are allowed and must be declared in <code>AI_USE.md</code>: the tool, the purpose, the prompts, and what was kept or changed', '<code>AI_ERRORS.md</code> documents at least three errors of AI tools caught by the team (a wrong formula, an invented reference, information leakage, wrong code) and how each was detected', 'Undeclared use of AI tools counts as plagiarism', 'Every number, piece of code and reference obtained with AI is checked by the team: references against their DOI, code against the data', 'No AI tools during the oral defence: each member must explain the methods, the code and the results', 'Every lecture ends with a section on AI for scientific discovery, and every seminar includes the critique of an AI answer'],
            ro: ['Instrumentele AI sînt permise și se declară în <code>AI_USE.md</code>: instrumentul, scopul, prompturile și ce s-a păstrat sau modificat', '<code>AI_ERRORS.md</code> documentează cel puțin trei erori ale instrumentelor AI depistate de echipă (o formulă greșită, o referință inventată, o scurgere de informație, cod greșit) și modul în care a fost depistată fiecare', 'Folosirea nedeclarată a instrumentelor AI este considerată plagiat', 'Fiecare rezultat numeric, fiecare secvență de cod și fiecare referință obținute cu AI sînt verificate de echipă: referințele după DOI, codul pe date', 'La susținerea orală nu se folosesc instrumente AI: fiecare membru explică metodele, codul și rezultatele', 'Fiecare curs se încheie cu o secțiune despre AI în descoperirea științifică, iar fiecare seminar include analiza critică a unui răspuns dat de AI']
        },

        // ---------------------------------------------------------------
        // Resources
        // ---------------------------------------------------------------
        resources: [
            { icon: '&#128187;', href: REPO, en: ['GitHub Repository', 'Slides, seminars, notebooks and Quantlets'], ro: ['Repository GitHub', 'Slide-uri, seminarii, notebook-uri și Quantlets'] },
            { icon: '&#128218;', href: TSA_SITE, en: ['Time Series Analysis (TSA)', 'The prerequisite bachelor course: Chapters 0–10'], ro: ['Serii de timp (TSA)', 'Cursul de licență prealabil: capitolele 0–10'] },
            { icon: '&#128214;', href: 'https://doi.org/10.1016/j.ijforecast.2021.11.001', en: ['Forecasting: theory and practice', 'Petropoulos et al. (2022), open-access review'], ro: ['Forecasting: theory and practice', 'Petropoulos et al. (2022), sinteză cu acces liber'] },
            { icon: '&#128214;', href: 'https://otexts.com/fpp3/', en: ['FPP3 (free online)', 'Hyndman &amp; Athanasopoulos, Forecasting: Principles and Practice'], ro: ['FPP3 (gratuit, online)', 'Hyndman și Athanasopoulos, Forecasting: Principles and Practice'] },
            { icon: '&#127891;', img: 'logos/qr_logo.png', href: 'https://quantinar.com', en: ['Quantinar', 'P2P platform with advanced courses'], ro: ['Quantinar', 'Platformă P2P cu cursuri avansate'] },
            { icon: '&#128190;', img: 'logos/ql_logo.png', href: 'https://quantlet.com', en: ['Quantlet', 'Reproducible code for every chart'], ro: ['Quantlet', 'Cod reproductibil pentru fiecare grafic'] },
            { icon: '&#127963;', img: 'logos/ida_square.png', href: 'https://theida.net', en: ['IDA', 'Institute for Digital Assets'], ro: ['IDA', 'Institute for Digital Assets'] }
        ],

        dataSources: [
            { name: 'INS TEMPO', href: 'http://statistici.insse.ro:8077/tempo-online/', en: 'National Institute of Statistics (Romania): GDP, prices, unemployment', ro: 'Institutul Național de Statistică: PIB, prețuri, șomaj' },
            { name: 'BNR', href: 'https://www.bnr.ro', en: 'National Bank of Romania: reference exchange rates, interest rates', ro: 'Banca Națională a României: cursuri de referință, dobînzi' },
            { name: 'Eurostat', href: 'https://ec.europa.eu/eurostat/data/database', en: 'European macroeconomic series (GDP, HICP, unemployment)', ro: 'Serii macroeconomice europene (PIB, IAPC, șomaj)' },
            { name: 'ECB Data Portal', href: 'https://data.ecb.europa.eu/', en: 'European Central Bank: exchange rates, interest rates, euro-area series', ro: 'Banca Centrală Europeană: cursuri de schimb, dobînzi, serii pentru zona euro' },
            { name: 'FRED', href: 'https://fred.stlouisfed.org', en: 'US macroeconomic and financial data (St. Louis Fed), including the FRED-MD database', ro: 'Date macroeconomice și financiare pentru SUA (St. Louis Fed), inclusiv baza de date FRED-MD' },
            { name: 'BVB', href: 'https://www.bvb.ro', en: 'Bucharest Stock Exchange', ro: 'Bursa de Valori București' }
        ],

        bibliography: [
            'Hamilton, J. D. (1994). <a href="https://doi.org/10.2307/j.ctv14jx6sm" target="_blank" rel="noopener"><em>Time Series Analysis</em></a>. Princeton University Press.',
            'Kilian, L., &amp; Lütkepohl, H. (2017). <a href="https://doi.org/10.1017/9781108164818" target="_blank" rel="noopener"><em>Structural Vector Autoregressive Analysis</em></a>. Cambridge University Press.',
            'Durbin, J., &amp; Koopman, S. J. (2012). <a href="https://doi.org/10.1093/acprof:oso/9780199641178.001.0001" target="_blank" rel="noopener"><em>Time Series Analysis by State Space Methods</em></a> (2nd ed.). Oxford University Press.',
            'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al. (2022). <a href="https://doi.org/10.1016/j.ijforecast.2021.11.001" target="_blank" rel="noopener">Forecasting: theory and practice</a>. <em>International Journal of Forecasting</em>, 38(3), 705–871.',
            'Huang, C., &amp; Petukhina, A. (2022). <a href="https://doi.org/10.1007/978-3-031-13584-2" target="_blank" rel="noopener"><em>Applied Time Series Analysis and Forecasting with Python</em></a>. Springer.',
            'Hyndman, R. J., &amp; Athanasopoulos, G. (2021). <a href="https://otexts.com/fpp3/" target="_blank" rel="noopener"><em>Forecasting: Principles and Practice</em></a> (3rd ed.). OTexts.',
            'Lütkepohl, H. (2005). <a href="https://doi.org/10.1007/978-3-540-27752-1" target="_blank" rel="noopener"><em>New Introduction to Multiple Time Series Analysis</em></a>. Springer.',
            'Shumway, R. H., &amp; Stoffer, D. S. (2017). <a href="https://doi.org/10.1007/978-3-319-52452-8" target="_blank" rel="noopener"><em>Time Series Analysis and Its Applications</em></a> (4th ed.). Springer.',
            'Baltagi, B. H. (2021). <a href="https://doi.org/10.1007/978-3-030-53953-5" target="_blank" rel="noopener"><em>Econometric Analysis of Panel Data</em></a> (6th ed.). Springer.',
            'Angelopoulos, A. N., &amp; Bates, S. (2023). <a href="https://doi.org/10.1561/2200000101" target="_blank" rel="noopener">Conformal prediction: a gentle introduction</a>. <em>Foundations and Trends in Machine Learning</em>, 16(4), 494–591.'
        ],

        contact: {
            name: 'Prof. dr. Daniel Traian Pele',
            email: 'danpele@ase.ro',
            en: ['Bucharest University of Economic Studies', 'Department of Statistics and Econometrics', 'Faculty of Cybernetics, Statistics and Economic Informatics'],
            ro: ['Academia de Studii Economice din București', 'Departamentul de Statistică și Econometrie', 'Facultatea de Cibernetică, Statistică și Informatică Economică'],
            // The whole course is published under the lecturer's name: no seminar card
            seminar: null
        },

        footerLogos: [
            ['https://www.ase.ro', 'logos/ase_logo.png', 'ASE'],
            ['https://www.theida.net/', 'logos/ida_logo.png', 'IDA'],
            ['https://quantinar.com', 'logos/qr_logo.png', 'Quantinar'],
            ['https://quantlet.com', 'logos/ql_logo.png', 'Quantlet'],
            ['https://ai4efin.ase.ro', 'logos/ai4efin_logo.png', 'AI4EFin'],
            ['https://www.digital-finance-msca.com/', 'logos/msca_logo.png', 'MSCA Digital Finance'],
            ['https://blockchain-research-center.com/', 'logos/brc_logo.png', 'Blockchain Research Center'],
            ['https://ipe.ro/new/', 'logos/acad_logo.png', 'Romanian Academy']
        ],

        // Quiz banks register themselves here by chapter id (see assets/quizzes/<id>.js)
        quizzes: {}
    };
})();
