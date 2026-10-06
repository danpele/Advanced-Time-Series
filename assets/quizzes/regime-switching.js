// ============================================================
// Chapter 7 quiz bank: Regime-switching models (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['regime-switching'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Prediction step of the Hamilton filter",
                "text": "In the Hamilton filter with transition matrix $\\mathbf{P}$, $p_{ij} = \\Pr(S_t = j \\mid S_{t-1} = i)$, how is $\\hat\\xi_{t|t-1}$ obtained from $\\hat\\xi_{t-1|t-1}$?",
                "options": [
                    "$\\hat\\xi_{t|t-1} = \\mathbf{P}'\\hat\\xi_{t-1|t-1}$",
                    "$\\hat\\xi_{t|t-1} = \\mathbf{P}\\hat\\xi_{t-1|t-1}$",
                    "$\\hat\\xi_{t|t-1} = \\hat\\xi_{t-1|t-1}\\odot\\eta_t$",
                    "$\\hat\\xi_{t|t-1}$ equals the ergodic probabilities at every $t$"
                ],
                "correctExplanation": "By the law of total probability, $\\Pr(S_t = j \\mid Y_{t-1}) = \\sum_i p_{ij}\\Pr(S_{t-1} = i \\mid Y_{t-1})$, which is the $j$-th element of $\\mathbf{P}'\\hat\\xi_{t-1|t-1}$.",
                "incorrectExplanation": "Multiplying by $\\mathbf{P}$ instead of its transpose sums over the wrong index; the product with $\\eta_t$ is the update step; the ergodic probabilities are only the starting value."
            },
            "ro": {
                "title": "Pasul de predicție al filtrului Hamilton",
                "text": "În filtrul Hamilton cu matricea de tranziție $\\mathbf{P}$, $p_{ij} = \\Pr(S_t = j \\mid S_{t-1} = i)$, cum se obține $\\hat\\xi_{t|t-1}$ din $\\hat\\xi_{t-1|t-1}$?",
                "options": [
                    "$\\hat\\xi_{t|t-1} = \\mathbf{P}'\\hat\\xi_{t-1|t-1}$",
                    "$\\hat\\xi_{t|t-1} = \\mathbf{P}\\hat\\xi_{t-1|t-1}$",
                    "$\\hat\\xi_{t|t-1} = \\hat\\xi_{t-1|t-1}\\odot\\eta_t$",
                    "$\\hat\\xi_{t|t-1}$ este egal cu probabilitățile ergodice la orice $t$"
                ],
                "correctExplanation": "Din formula probabilității totale, $\\Pr(S_t = j \\mid Y_{t-1}) = \\sum_i p_{ij}\\Pr(S_{t-1} = i \\mid Y_{t-1})$, adică elementul $j$ al lui $\\mathbf{P}'\\hat\\xi_{t-1|t-1}$.",
                "incorrectExplanation": "Înmulțirea cu $\\mathbf{P}$ în locul transpusei sumează după indicele greșit; produsul cu $\\eta_t$ este pasul de actualizare; probabilitățile ergodice sînt doar valoarea de pornire."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Likelihood contribution",
                "text": "What is the contribution of observation $t$ to the log-likelihood of a Markov-switching model?",
                "options": [
                    "$\\sum_j \\hat\\xi_{j,t|t}\\ln\\eta_{jt}$",
                    "$\\ln\\sum_j \\hat\\xi_{j,t|t-1}\\,\\eta_{jt}$",
                    "$\\ln\\max_j \\eta_{jt}$",
                    "$\\sum_j \\hat\\xi_{j,t|T}\\ln\\eta_{jt}$"
                ],
                "correctExplanation": "The predictive density of $y_t$ is a mixture of the regime densities weighted by the predicted probabilities; the log-likelihood is the sum of the logs of these predictive densities (prediction-error decomposition).",
                "incorrectExplanation": "Weighting log-densities by filtered or smoothed probabilities gives the expected complete-data log-likelihood used inside EM, not the likelihood; the maximum density ignores the regime uncertainty."
            },
            "ro": {
                "title": "Contribuția la verosimilitate",
                "text": "Care este contribuția observației $t$ la log-verosimilitatea unui model cu schimbare de regim?",
                "options": [
                    "$\\sum_j \\hat\\xi_{j,t|t}\\ln\\eta_{jt}$",
                    "$\\ln\\sum_j \\hat\\xi_{j,t|t-1}\\,\\eta_{jt}$",
                    "$\\ln\\max_j \\eta_{jt}$",
                    "$\\sum_j \\hat\\xi_{j,t|T}\\ln\\eta_{jt}$"
                ],
                "correctExplanation": "Densitatea predictivă a lui $y_t$ este un amestec al densităților regimurilor, ponderat cu probabilitățile prezise; log-verosimilitatea este suma logaritmilor acestor densități (descompunerea erorilor de predicție).",
                "incorrectExplanation": "Ponderarea logaritmilor densităților cu probabilități filtrate sau netezite dă log-verosimilitatea așteptată a datelor complete din EM, nu verosimilitatea; densitatea maximă ignoră incertitudinea regimului."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Ergodic probability",
                "text": "A two-regime chain has $p_{11} = 0.9$ and $p_{22} = 0.75$. What is the ergodic probability of regime 1?",
                "options": [
                    "0.9",
                    "$0.1/0.35 \\approx 0.286$",
                    "$0.25/0.35 \\approx 0.714$",
                    "0.5"
                ],
                "correctExplanation": "$\\pi_1 = (1 - p_{22})/(2 - p_{11} - p_{22}) = 0.25/0.35 \\approx 0.714$: the share of time spent in regime 1 in the long run.",
                "incorrectExplanation": "0.9 is the probability of staying in regime 1; 0.286 is the ergodic probability of regime 2; 0.5 would require $p_{11} = p_{22}$."
            },
            "ro": {
                "title": "Probabilitatea ergodică",
                "text": "Un lanț cu două regimuri are $p_{11} = 0{,}9$ și $p_{22} = 0{,}75$. Care este probabilitatea ergodică a regimului 1?",
                "options": [
                    "0,9",
                    "$0{,}1/0{,}35 \\approx 0{,}286$",
                    "$0{,}25/0{,}35 \\approx 0{,}714$",
                    "0,5"
                ],
                "correctExplanation": "$\\pi_1 = (1 - p_{22})/(2 - p_{11} - p_{22}) = 0{,}25/0{,}35 \\approx 0{,}714$: fracțiunea de timp petrecută pe termen lung în regimul 1.",
                "incorrectExplanation": "0,9 este probabilitatea de rămînere în regimul 1; 0,286 este probabilitatea ergodică a regimului 2; 0,5 ar cere $p_{11} = p_{22}$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Persistence of the chain",
                "text": "For a two-regime chain, at what rate does $\\Pr(S_{t+h} = 1 \\mid S_t)$ converge to the ergodic probability?",
                "options": [
                    "$p_{11}^h$",
                    "$(1 - p_{22})^h$",
                    "It converges in one step",
                    "$\\lambda^h$ with $\\lambda = p_{11} + p_{22} - 1$"
                ],
                "correctExplanation": "The indicator of regime 1 follows an AR(1) with coefficient $\\lambda = p_{11} + p_{22} - 1$, the second eigenvalue of $\\mathbf{P}$; the distance to $\\pi_1$ shrinks by $\\lambda$ each period.",
                "incorrectExplanation": "$p_{11}^h$ is the probability of staying $h$ periods without leaving; $(1 - p_{22})^h$ has no role; one-step convergence happens only when $\\lambda = 0$ (an i.i.d. mixture)."
            },
            "ro": {
                "title": "Persistența lanțului",
                "text": "Pentru un lanț cu două regimuri, cu ce viteză converge $\\Pr(S_{t+h} = 1 \\mid S_t)$ către probabilitatea ergodică?",
                "options": [
                    "$p_{11}^h$",
                    "$(1 - p_{22})^h$",
                    "Converge într-un singur pas",
                    "$\\lambda^h$, cu $\\lambda = p_{11} + p_{22} - 1$"
                ],
                "correctExplanation": "Indicatorul regimului 1 urmează un AR(1) cu coeficientul $\\lambda = p_{11} + p_{22} - 1$, a doua valoare proprie a lui $\\mathbf{P}$; distanța față de $\\pi_1$ scade cu factorul $\\lambda$ în fiecare perioadă.",
                "incorrectExplanation": "$p_{11}^h$ este probabilitatea de a rămîne $h$ perioade fără a ieși; $(1 - p_{22})^h$ nu are niciun rol; convergența într-un pas apare doar pentru $\\lambda = 0$ (un amestec i.i.d.)."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The Kim smoother",
                "text": "Which quantity appears in the denominator of the Kim smoother, $\\Pr(S_t = i, S_{t+1} = j \\mid Y_T) = \\hat\\xi_{i,t|t}p_{ij}\\hat\\xi_{j,t+1|T}/(\\cdot)$?",
                "options": [
                    "$\\hat\\xi_{j,t+1|t}$, the predicted probability",
                    "$\\hat\\xi_{j,t+1|t+1}$, the filtered probability",
                    "$\\pi_j$, the ergodic probability",
                    "$f(y_{t+1} \\mid Y_t)$, the predictive density"
                ],
                "correctExplanation": "Given $S_{t+1} = j$, $\\Pr(S_t = i \\mid S_{t+1} = j, Y_t) = \\hat\\xi_{i,t|t}p_{ij}/\\hat\\xi_{j,t+1|t}$ by Bayes; multiplying by $\\hat\\xi_{j,t+1|T}$ gives the joint smoothed probability.",
                "incorrectExplanation": "The filtered probability already contains $y_{t+1}$; the ergodic probability ignores the data; the predictive density belongs to the likelihood, not to the backward pass."
            },
            "ro": {
                "title": "Netezitorul Kim",
                "text": "Ce mărime apare la numitorul netezitorului Kim, $\\Pr(S_t = i, S_{t+1} = j \\mid Y_T) = \\hat\\xi_{i,t|t}p_{ij}\\hat\\xi_{j,t+1|T}/(\\cdot)$?",
                "options": [
                    "$\\hat\\xi_{j,t+1|t}$, probabilitatea prezisă",
                    "$\\hat\\xi_{j,t+1|t+1}$, probabilitatea filtrată",
                    "$\\pi_j$, probabilitatea ergodică",
                    "$f(y_{t+1} \\mid Y_t)$, densitatea predictivă"
                ],
                "correctExplanation": "Dat fiind $S_{t+1} = j$, $\\Pr(S_t = i \\mid S_{t+1} = j, Y_t) = \\hat\\xi_{i,t|t}p_{ij}/\\hat\\xi_{j,t+1|t}$ din regula lui Bayes; înmulțind cu $\\hat\\xi_{j,t+1|T}$ obținem probabilitatea comună netezită.",
                "incorrectExplanation": "Probabilitatea filtrată conține deja $y_{t+1}$; probabilitatea ergodică ignoră datele; densitatea predictivă aparține verosimilității, nu trecerii înapoi."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Real-time evaluation",
                "text": "A paper evaluates how fast a Markov-switching model signals recessions 'in real time' using smoothed probabilities from the full sample. What is wrong?",
                "options": [
                    "Nothing, smoothed probabilities are more accurate",
                    "Smoothed probabilities use future data; real-time evaluation needs filtered probabilities and data vintages",
                    "Smoothed probabilities cannot be computed for the last quarter",
                    "Real-time evaluation should use ergodic probabilities"
                ],
                "correctExplanation": "$\\hat\\xi_{t|T}$ conditions on observations after $t$; what a forecaster knew at $t$ is $\\hat\\xi_{t|t}$, computed with parameters and data available then (Chauvet and Piger 2008).",
                "incorrectExplanation": "Higher accuracy of smoothed probabilities comes precisely from using the future; at $t = T$ smoothed and filtered coincide; ergodic probabilities contain no information on the current regime."
            },
            "ro": {
                "title": "Evaluarea în timp real",
                "text": "O lucrare evaluează cît de repede semnalează un model Markov switching recesiunile „în timp real” folosind probabilitățile netezite din tot eșantionul. Ce este greșit?",
                "options": [
                    "Nimic, probabilitățile netezite sînt mai precise",
                    "Probabilitățile netezite folosesc date viitoare; evaluarea în timp real cere probabilități filtrate și ediții ale datelor",
                    "Probabilitățile netezite nu se pot calcula pentru ultimul trimestru",
                    "Evaluarea în timp real trebuie să folosească probabilitățile ergodice"
                ],
                "correctExplanation": "$\\hat\\xi_{t|T}$ condiționează pe observații de după $t$; ce știa un prognozator la $t$ este $\\hat\\xi_{t|t}$, calculat cu parametrii și datele disponibile atunci (Chauvet și Piger 2008).",
                "incorrectExplanation": "Precizia mai mare a probabilităților netezite vine tocmai din folosirea viitorului; la $t = T$ cele netezite și cele filtrate coincid; probabilitățile ergodice nu conțin informație despre regimul curent."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "M-step for the transition probabilities",
                "text": "In the EM algorithm of Hamilton (1990), how is $p_{ij}$ updated?",
                "options": [
                    "Number of periods with filtered probability of $j$ above 0.5",
                    "Weighted least squares of $\\hat\\xi_{j,t|T}$ on $\\hat\\xi_{i,t-1|T}$",
                    "Expected number of transitions $i \\to j$ divided by expected number of visits to $i$, both from the Kim smoother",
                    "It is kept fixed; only the regression parameters are updated"
                ],
                "correctExplanation": "$p_{ij} = \\sum_t\\Pr(S_{t-1} = i, S_t = j \\mid Y_T)/\\sum_t\\Pr(S_{t-1} = i \\mid Y_T)$: the maximiser of the expected complete-data log-likelihood under the row constraint.",
                "incorrectExplanation": "Hard classification at 0.5 is not an EM step; a regression of probabilities is not the M-step; EM updates the transition probabilities as well."
            },
            "ro": {
                "title": "Pasul M pentru probabilitățile de tranziție",
                "text": "În algoritmul EM al lui Hamilton (1990), cum se actualizează $p_{ij}$?",
                "options": [
                    "Numărul de perioade cu probabilitatea filtrată a lui $j$ peste 0,5",
                    "Regresia ponderată a lui $\\hat\\xi_{j,t|T}$ pe $\\hat\\xi_{i,t-1|T}$",
                    "Numărul așteptat de tranziții $i \\to j$ împărțit la numărul așteptat de vizite în $i$, ambele din netezitorul Kim",
                    "Rămîne fix; se actualizează doar parametrii regresiei"
                ],
                "correctExplanation": "$p_{ij} = \\sum_t\\Pr(S_{t-1} = i, S_t = j \\mid Y_T)/\\sum_t\\Pr(S_{t-1} = i \\mid Y_T)$: maximul log-verosimilității așteptate a datelor complete sub restricția pe rînduri.",
                "incorrectExplanation": "Clasificarea la pragul 0,5 nu este un pas EM; o regresie a probabilităților nu este pasul M; EM actualizează și probabilitățile de tranziție."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Degenerate maxima",
                "text": "EM on a two-regime model with switching variance converges to a solution with $\\sigma_2^2 \\approx 0.05$, $p_{22} \\approx 0$ and the highest log-likelihood. What is it?",
                "options": [
                    "The global maximum, which should be reported as the business cycle",
                    "Evidence of three regimes",
                    "A numerical overflow of the Hamilton filter",
                    "A degenerate maximum: a regime that fits isolated observations; the likelihood is unbounded as $\\sigma_j \\to 0$"
                ],
                "correctExplanation": "Mixture likelihoods grow without bound when a component collapses on single points; such solutions must be rejected by a variance bound, a prior or an economic criterion (Hathaway 1985).",
                "incorrectExplanation": "The highest likelihood is not economically meaningful here; it says nothing about a third regime; the filter works in logs and does not overflow."
            },
            "ro": {
                "title": "Maxime degenerate",
                "text": "EM pentru un model cu două regimuri și varianță care comută converge la o soluție cu $\\sigma_2^2 \\approx 0{,}05$, $p_{22} \\approx 0$ și cea mai mare log-verosimilitate. Ce este?",
                "options": [
                    "Maximul global, care trebuie raportat drept ciclul economic",
                    "O evidență pentru trei regimuri",
                    "O depășire numerică a filtrului Hamilton",
                    "Un maxim degenerat: un regim care potrivește observații izolate; verosimilitatea este nemărginită cînd $\\sigma_j \\to 0$"
                ],
                "correctExplanation": "Verosimilitățile amestecurilor cresc nelimitat cînd o componentă se strînge pe puncte izolate; astfel de soluții se resping printr-o limită a varianței, o distribuție a priori sau un criteriu economic (Hathaway 1985).",
                "incorrectExplanation": "Cea mai mare verosimilitate nu are aici sens economic; nu spune nimic despre un al treilea regim; filtrul lucrează în logaritmi și nu produce depășiri."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Label switching",
                "text": "Why does label switching matter for MCMC but not for maximum likelihood?",
                "options": [
                    "ML picks one of the $K!$ equivalent modes; a sampler can visit all of them, so posterior means of regime parameters mix the regimes",
                    "ML imposes $\\mu_1 < \\mu_2$ automatically",
                    "Label switching changes the likelihood value",
                    "MCMC uses a different likelihood"
                ],
                "correctExplanation": "The likelihood is invariant to permutations of the labels; an optimiser stops in one mode, while the posterior is symmetric and the draws must be identified afterwards (Frühwirth-Schnatter 2001).",
                "incorrectExplanation": "No ordering is imposed by the likelihood; the value is identical under permutation; MCMC targets the same likelihood times the prior."
            },
            "ro": {
                "title": "Schimbarea etichetelor",
                "text": "De ce contează schimbarea etichetelor pentru MCMC, dar nu pentru verosimilitatea maximă?",
                "options": [
                    "Verosimilitatea maximă alege unul dintre cele $K!$ moduri echivalente; un eșantionator le poate vizita pe toate, deci mediile a posteriori ale parametrilor amestecă regimurile",
                    "Verosimilitatea maximă impune automat $\\mu_1 < \\mu_2$",
                    "Schimbarea etichetelor modifică valoarea verosimilității",
                    "MCMC folosește o altă verosimilitate"
                ],
                "correctExplanation": "Verosimilitatea este invariantă la permutarea etichetelor; un optimizator se oprește într-un mod, pe cînd distribuția a posteriori este simetrică, iar extragerile trebuie identificate ulterior (Frühwirth-Schnatter 2001).",
                "incorrectExplanation": "Verosimilitatea nu impune nicio ordonare; valoarea ei este aceeași după permutare; MCMC folosește aceeași verosimilitate înmulțită cu distribuția a priori."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Testing one regime against two",
                "text": "Why is the LR statistic for one regime against two not asymptotically $\\chi^2$?",
                "options": [
                    "Because the errors are not Normal",
                    "Under the null the transition probabilities are not identified, a parameter is on the boundary and the score is identically zero",
                    "Because the sample is always too small",
                    "Because the LR statistic can be negative"
                ],
                "correctExplanation": "The three standard regularity conditions fail at once (Hansen 1992; Garcia 1998); critical values must come from the bootstrap or from tabulated non-standard distributions.",
                "incorrectExplanation": "Normality is assumed in the model; the problem persists in large samples; a correctly computed LR is non-negative."
            },
            "ro": {
                "title": "Testarea unui regim față de două",
                "text": "De ce statistica LR pentru un regim față de două nu are asimptotic distribuția $\\chi^2$?",
                "options": [
                    "Pentru că erorile nu sînt Normale",
                    "Sub ipoteza nulă probabilitățile de tranziție nu sînt identificate, un parametru este pe frontieră, iar scorul este identic zero",
                    "Pentru că eșantionul este întotdeauna prea mic",
                    "Pentru că statistica LR poate fi negativă"
                ],
                "correctExplanation": "Cele trei condiții standard de regularitate nu sînt îndeplinite simultan (Hansen 1992; Garcia 1998); valorile critice trebuie obținute prin bootstrap sau din distribuții nestandard tabelate.",
                "incorrectExplanation": "Normalitatea este presupusă în model; problema persistă în eșantioane mari; o statistică LR calculată corect este nenegativă."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Parametric bootstrap of the LR",
                "text": "Which procedure gives a valid bootstrap $p$-value for $K = 1$ against $K = 2$?",
                "options": [
                    "Resample the residuals of the two-regime model and re-estimate only $K = 2$",
                    "Simulate from the two-regime model and count rejections",
                    "Simulate from the estimated one-regime model, re-estimate both models on each sample with several starts, compare the LR values",
                    "Use the $\\chi^2$ distribution with the number of extra parameters"
                ],
                "correctExplanation": "The null distribution must be generated under $H_0$, and each simulated LR must be computed exactly as the observed one, including the search over starting values.",
                "incorrectExplanation": "Resampling under the alternative or re-estimating one model only does not reproduce the null distribution; simulating from $K = 2$ gives power, not size; the $\\chi^2$ count is invalid here."
            },
            "ro": {
                "title": "Bootstrap parametric pentru LR",
                "text": "Ce procedură dă o valoare $p$ bootstrap validă pentru $K = 1$ față de $K = 2$?",
                "options": [
                    "Reeșantionăm reziduurile modelului cu două regimuri și reestimăm doar $K = 2$",
                    "Simulăm din modelul cu două regimuri și numărăm respingerile",
                    "Simulăm din modelul estimat cu un regim, reestimăm ambele modele pe fiecare eșantion cu mai multe puncte de pornire, comparăm valorile LR",
                    "Folosim distribuția $\\chi^2$ cu numărul de parametri suplimentari"
                ],
                "correctExplanation": "Distribuția sub ipoteza nulă trebuie generată sub $H_0$, iar fiecare LR simulat trebuie calculat exact ca cel observat, inclusiv căutarea după punctele de pornire.",
                "incorrectExplanation": "Reeșantionarea sub alternativă sau reestimarea unui singur model nu reproduce distribuția sub $H_0$; simularea din $K = 2$ dă puterea, nu mărimea testului; numărarea gradelor de libertate ale $\\chi^2$ nu este validă aici."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Hamilton's expanded state",
                "text": "Why does Hamilton's switching-mean AR(4) with two regimes require a filter over 32 states?",
                "options": [
                    "Because there are 32 parameters",
                    "Because the AR(4) has 32 roots",
                    "Because the sample has 32 recessions",
                    "The density of $y_t$ depends on $\\mu_{S_t}, \\dots, \\mu_{S_{t-4}}$, so the state is $(S_t, \\dots, S_{t-4})$ with $2^5 = 32$ values"
                ],
                "correctExplanation": "In the MSM form the lagged deviations $y_{t-k} - \\mu_{S_{t-k}}$ involve past regimes; switching-intercept models (MSI) need only $K$ states.",
                "incorrectExplanation": "The parameter count is 9; an AR(4) has 4 roots; the number of recessions is irrelevant."
            },
            "ro": {
                "title": "Starea extinsă a lui Hamilton",
                "text": "De ce modelul AR(4) cu medie care comută al lui Hamilton, cu două regimuri, cere un filtru pe 32 de stări?",
                "options": [
                    "Pentru că există 32 de parametri",
                    "Pentru că AR(4) are 32 de rădăcini",
                    "Pentru că eșantionul are 32 de recesiuni",
                    "Densitatea lui $y_t$ depinde de $\\mu_{S_t}, \\dots, \\mu_{S_{t-4}}$, deci starea este $(S_t, \\dots, S_{t-4})$ cu $2^5 = 32$ de valori"
                ],
                "correctExplanation": "În forma MSM abaterile întîrziate $y_{t-k} - \\mu_{S_{t-k}}$ implică regimurile trecute; modelele cu termen liber care comută (MSI) cer doar $K$ stări.",
                "incorrectExplanation": "Modelul are 9 parametri; un AR(4) are 4 rădăcini; numărul de recesiuni nu contează."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Hamilton (1989) on today's data",
                "text": "Re-estimated on today's US GDP (1953–2019), Hamilton's model gives a low regime with mean about $-1.2\\%$ and $p_{00} \\approx 0.26$. What does this mean?",
                "options": [
                    "The low regime now captures short sharp contractions (about one quarter), not recessions of several quarters, and it misses 2001",
                    "The model dates every NBER recession better than in 1989",
                    "The low regime is the Great Moderation",
                    "The estimation failed and the result must be discarded"
                ],
                "correctExplanation": "An expected duration of $1/(1 - 0.26) \\approx 1.4$ quarters means single deep quarters; after 1984 recessions are rarer and milder, so the fixed two-mean model loses its business-cycle interpretation.",
                "incorrectExplanation": "The fit to the NBER dates is worse, not better; the Great Moderation is a variance regime, which an MSM model with constant variance cannot capture; a valid but different maximum is not a failure."
            },
            "ro": {
                "title": "Hamilton (1989) pe datele de azi",
                "text": "Reestimat pe PIB-ul actual al SUA (1953–2019), modelul lui Hamilton dă un regim scăzut cu media aproximativ $-1{,}2\\%$ și $p_{00} \\approx 0{,}26$. Ce înseamnă aceasta?",
                "options": [
                    "Regimul scăzut prinde acum contracții scurte și bruște (aproximativ un trimestru), nu recesiuni de mai multe trimestre, și ratează 2001",
                    "Modelul datează fiecare recesiune NBER mai bine decît în 1989",
                    "Regimul scăzut este Marea Moderație",
                    "Estimarea a eșuat, iar rezultatul trebuie eliminat"
                ],
                "correctExplanation": "O durată așteptată de $1/(1 - 0{,}26) \\approx 1{,}4$ trimestre înseamnă trimestre adînci izolate; după 1984 recesiunile sînt mai rare și mai blînde, deci modelul fix cu două medii își pierde interpretarea de ciclu economic.",
                "incorrectExplanation": "Potrivirea cu datările NBER este mai slabă, nu mai bună; Marea Moderație este un regim de varianță, pe care un model MSM cu varianță constantă nu îl poate capta; un maxim valid, dar diferit, nu este un eșec."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Time-varying transition probabilities",
                "text": "In a TVTP model, $p_{ii,t} = \\text{logistic}(z_{t-1}'\\gamma_i)$. Which condition on $z$ is needed?",
                "options": [
                    "$z$ must be stationary with zero mean",
                    "$z_{t-1}$ must be predetermined and must not respond to the current regime",
                    "$z$ must be one of the regressors of the mean equation",
                    "$z$ must be a dummy variable"
                ],
                "correctExplanation": "If $z$ reacts to $S_t$ the transition equation is endogenous and the filter is misspecified (Diebold, Lee and Weinbach 1994; Filardo 1994).",
                "incorrectExplanation": "Centering helps interpretation but is not required; $z$ need not appear in the mean equation; continuous covariates such as a leading indicator are the usual case."
            },
            "ro": {
                "title": "Probabilități de tranziție variabile în timp",
                "text": "Într-un model TVTP, $p_{ii,t} = \\text{logistic}(z_{t-1}'\\gamma_i)$. Ce condiție trebuie să îndeplinească $z$?",
                "options": [
                    "$z$ trebuie să fie staționar cu media zero",
                    "$z_{t-1}$ trebuie să fie predeterminat și să nu reacționeze la regimul curent",
                    "$z$ trebuie să fie unul dintre regresorii ecuației mediei",
                    "$z$ trebuie să fie o variabilă dummy"
                ],
                "correctExplanation": "Dacă $z$ reacționează la $S_t$, ecuația de tranziție este endogenă, iar filtrul este greșit specificat (Diebold, Lee și Weinbach 1994; Filardo 1994).",
                "incorrectExplanation": "Centrarea ajută interpretarea, dar nu este necesară; $z$ nu trebuie să apară în ecuația mediei; covariabilele continue, precum un indicator avansat, sînt cazul obișnuit."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Testing constant transition probabilities",
                "text": "Why is the LR test of TVTP against constant transitions ($H_0$: slopes of $\\gamma_i$ equal zero) standard, unlike the test of the number of regimes?",
                "options": [
                    "Because the logistic function is bounded",
                    "Because the leading indicator is exogenous",
                    "The regimes exist under both hypotheses, so all parameters are identified under $H_0$ and the restriction is in the interior",
                    "It is not standard either"
                ],
                "correctExplanation": "The non-standard features of the regime-number test come from regimes disappearing under $H_0$; here only two slopes are set to zero, so $2\\ln\\Lambda \\to \\chi^2_2$.",
                "incorrectExplanation": "Boundedness of the link and exogeneity are not the issue; the test is standard because identification holds under the null."
            },
            "ro": {
                "title": "Testarea probabilităților de tranziție constante",
                "text": "De ce testul LR al modelului TVTP față de tranziții constante ($H_0$: pantele lui $\\gamma_i$ sînt zero) este standard, spre deosebire de testul numărului de regimuri?",
                "options": [
                    "Pentru că funcția logistică este mărginită",
                    "Pentru că indicatorul avansat este exogen",
                    "Regimurile există sub ambele ipoteze, deci toți parametrii sînt identificați sub $H_0$, iar restricția este în interiorul spațiului parametrilor",
                    "Nici acesta nu este standard"
                ],
                "correctExplanation": "Caracteristicile nestandard ale testului numărului de regimuri vin din dispariția regimurilor sub $H_0$; aici doar două pante sînt fixate la zero, deci $2\\ln\\Lambda \\to \\chi^2_2$.",
                "incorrectExplanation": "Mărginirea funcției de legătură și exogenitatea nu sînt problema; testul este standard pentru că identificarea are loc sub ipoteza nulă."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Regime-dependent impulse responses",
                "text": "What do the regime-dependent impulse responses of Ehrmann, Ellison and Valla (2003) assume?",
                "options": [
                    "That regimes switch every period",
                    "That the shock changes the regime",
                    "That the VAR coefficients are the same in all regimes",
                    "That the regime in which the shock occurs persists over the whole horizon"
                ],
                "correctExplanation": "They are computed with the coefficients and covariance of one regime; the full response averages over future regime paths and must be simulated.",
                "incorrectExplanation": "Switching every period or shocks that move the regime are different (and harder) exercises; with common coefficients only the impact matrix would differ."
            },
            "ro": {
                "title": "Răspunsuri la impuls dependente de regim",
                "text": "Ce presupun răspunsurile la impuls dependente de regim ale lui Ehrmann, Ellison și Valla (2003)?",
                "options": [
                    "Că regimurile comută în fiecare perioadă",
                    "Că șocul schimbă regimul",
                    "Că coeficienții VAR sînt aceiași în toate regimurile",
                    "Că regimul în care apare șocul persistă pe tot orizontul"
                ],
                "correctExplanation": "Se calculează cu coeficienții și covarianța unui singur regim; răspunsul complet face media pe traiectoriile viitoare ale regimurilor și se obține prin simulare.",
                "incorrectExplanation": "Comutarea în fiecare perioadă sau șocurile care schimbă regimul sînt exerciții diferite (și mai dificile); cu coeficienți comuni ar diferi doar matricea de impact."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Path dependence in MS-GARCH",
                "text": "Why can the Hamilton filter not be applied to the naive MS-GARCH $h_t = \\omega_{S_t} + \\alpha_{S_t}\\varepsilon_{t-1}^2 + \\beta_{S_t}h_{t-1}$?",
                "options": [
                    "$h_t$ depends on the entire regime history, so the number of states grows as $K^t$",
                    "Because GARCH is not Gaussian",
                    "Because $\\alpha + \\beta$ may exceed 1",
                    "Because the filter needs constant variances"
                ],
                "correctExplanation": "The lagged $h_{t-1}$ depends on $S_{t-1}$, which depends on $S_{t-2}$, and so on; Gray (1996) collapses the history, Haas, Mittnik and Paolella (2004) run regime-specific GARCH recursions in parallel.",
                "incorrectExplanation": "Gaussianity is assumed; the stationarity condition is separate; the filter handles regime-dependent variances as long as they depend on a finite number of regimes."
            },
            "ro": {
                "title": "Dependența de traiectorie în MS-GARCH",
                "text": "De ce nu se poate aplica filtrul Hamilton modelului MS-GARCH naiv $h_t = \\omega_{S_t} + \\alpha_{S_t}\\varepsilon_{t-1}^2 + \\beta_{S_t}h_{t-1}$?",
                "options": [
                    "$h_t$ depinde de întreaga istorie a regimurilor, deci numărul de stări crește ca $K^t$",
                    "Pentru că GARCH nu este Gaussian",
                    "Pentru că $\\alpha + \\beta$ poate depăși 1",
                    "Pentru că filtrul cere varianțe constante"
                ],
                "correctExplanation": "$h_{t-1}$ depinde de $S_{t-1}$, care depinde de $S_{t-2}$ și așa mai departe; Gray (1996) comprimă istoria, Haas, Mittnik și Paolella (2004) rulează în paralel recursii GARCH specifice regimurilor.",
                "incorrectExplanation": "Normalitatea este presupusă; condiția de staționaritate este o problemă separată; filtrul tratează varianțe dependente de regim atîta timp cît depind de un număr finit de regimuri."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "FFBS",
                "text": "In the Gibbs sampler of Chib (1996), how is the regime path drawn?",
                "options": [
                    "Draw each $S_t$ independently from the smoothed probabilities",
                    "Run the Hamilton filter forward, draw $S_T$ from $\\hat\\xi_{T|T}$, then draw backwards $S_t$ with probabilities proportional to $\\hat\\xi_{t|t}\\odot\\mathbf{P}_{\\cdot,S_{t+1}}$",
                    "Draw each $S_t$ from the ergodic distribution",
                    "Set $S_t$ to the most likely regime"
                ],
                "correctExplanation": "Forward filtering, backward sampling draws the whole path from its joint posterior in one block, which mixes much faster than single-move updates.",
                "incorrectExplanation": "Independent draws from marginal smoothed probabilities ignore the Markov dependence between regimes; ergodic draws ignore the data; the most likely regime is not a draw."
            },
            "ro": {
                "title": "FFBS",
                "text": "În eșantionatorul Gibbs al lui Chib (1996), cum se extrage traiectoria regimurilor?",
                "options": [
                    "Extragem fiecare $S_t$ independent din probabilitățile netezite",
                    "Rulăm filtrul Hamilton înainte, extragem $S_T$ din $\\hat\\xi_{T|T}$, apoi extragem înapoi $S_t$ cu probabilități proporționale cu $\\hat\\xi_{t|t}\\odot\\mathbf{P}_{\\cdot,S_{t+1}}$",
                    "Extragem fiecare $S_t$ din distribuția ergodică",
                    "Fixăm $S_t$ la regimul cel mai probabil"
                ],
                "correctExplanation": "Filtrarea înainte și eșantionarea înapoi extrag toată traiectoria din distribuția ei comună a posteriori dintr-un singur bloc, care se amestecă mult mai repede decît actualizările pas cu pas.",
                "incorrectExplanation": "Extragerile independente din probabilitățile netezite marginale ignoră dependența Markov dintre regimuri; extragerile ergodice ignoră datele; regimul cel mai probabil nu este o extragere."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Long memory and regime switching",
                "text": "Diebold and Inoue (2001) show that a switching mean with $p_{ii} = 1 - c/T$ produces:",
                "options": [
                    "A unit root in every sample",
                    "Estimates of $d$ that converge to zero",
                    "Positive estimates of the memory parameter $d$ that do not vanish as $T$ grows",
                    "Negative autocorrelations at long lags"
                ],
                "correctExplanation": "Rare switches make the variance of partial sums grow like that of an I($d$) process; memory estimators such as GPH then report $d > 0$, so they cannot separate long memory from regimes.",
                "incorrectExplanation": "There is no unit root: the process is mean-reverting given the regimes; with fixed $p_{ii}$ (short memory) the estimates do go to zero, but not with $p_{ii} \\to 1$; the autocorrelations are positive."
            },
            "ro": {
                "title": "Memorie lungă și schimbare de regim",
                "text": "Diebold și Inoue (2001) arată că o medie care comută, cu $p_{ii} = 1 - c/T$, produce:",
                "options": [
                    "O rădăcină unitară în orice eșantion",
                    "Estimații ale lui $d$ care converg la zero",
                    "Estimații pozitive ale parametrului de memorie $d$ care nu dispar cînd $T$ crește",
                    "Autocorelații negative la decalaje mari"
                ],
                "correctExplanation": "Comutările rare fac ca varianța sumelor parțiale să crească la fel ca la un proces I($d$); estimatorii de memorie precum GPH raportează atunci $d > 0$, deci nu pot deosebi memoria lungă de regimuri.",
                "incorrectExplanation": "Nu există rădăcină unitară: procesul revine la medie, date fiind regimurile; cu $p_{ii}$ fix (memorie scurtă) estimațiile tind la zero, dar nu cu $p_{ii} \\to 1$; autocorelațiile sînt pozitive."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Breaks as regimes",
                "text": "How is a change-point model with three segments (Chib 1998) written as a Markov-switching model?",
                "options": [
                    "Three regimes with a symmetric $\\mathbf{P}$",
                    "Three regimes with $p_{ii} = 1$ for all $i$",
                    "It cannot be written in this form",
                    "Three regimes, $S_1 = 1$, and an upper bidiagonal $\\mathbf{P}$: each regime can only stay or move to the next one"
                ],
                "correctExplanation": "Forbidding returns and skips turns recurrent regimes into consecutive segments; the Hamilton filter and EM apply unchanged with the restricted $\\mathbf{P}$.",
                "incorrectExplanation": "A symmetric matrix allows returns; $p_{ii} = 1$ for every regime would never switch; the change-point model is a special case of Markov switching."
            },
            "ro": {
                "title": "Rupturi ca regimuri",
                "text": "Cum se scrie un model cu puncte de schimbare cu trei segmente (Chib 1998) ca model Markov switching?",
                "options": [
                    "Trei regimuri cu o matrice $\\mathbf{P}$ simetrică",
                    "Trei regimuri cu $p_{ii} = 1$ pentru orice $i$",
                    "Nu se poate scrie în această formă",
                    "Trei regimuri, $S_1 = 1$ și o matrice $\\mathbf{P}$ superior bidiagonală: fiecare regim poate doar să rămînă sau să treacă în următorul"
                ],
                "correctExplanation": "Interzicerea revenirilor și a salturilor transformă regimurile recurente în segmente consecutive; filtrul Hamilton și EM se aplică neschimbate cu $\\mathbf{P}$ restricționată.",
                "incorrectExplanation": "O matrice simetrică permite reveniri; $p_{ii} = 1$ pentru fiecare regim nu ar comuta niciodată; modelul cu puncte de schimbare este un caz particular al schimbării de regim."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Forecasting with regime models",
                "text": "Clements and Krolzig (1998) and the lecture's US GDP exercise both find that, compared with a linear AR:",
                "options": [
                    "Point forecasts are hardly better, while density forecasts can improve through the variance regime",
                    "Point forecasts are always much better",
                    "Density forecasts are always worse",
                    "Regime models cannot produce density forecasts"
                ],
                "correctExplanation": "In the lecture the RMSEs of AR(1) and MSIH(2)-AR(1) are almost equal, while the log score improves, mainly in calm periods; gains must be tested with Diebold–Mariano-type tests.",
                "incorrectExplanation": "Large point-forecast gains are rare; the predictive density is a mixture and is often better calibrated; regime models naturally produce predictive densities."
            },
            "ro": {
                "title": "Prognoza cu modele cu regimuri",
                "text": "Clements și Krolzig (1998) și exercițiul din curs pentru PIB-ul SUA găsesc amîndouă că, față de un AR liniar:",
                "options": [
                    "Prognozele punctuale sînt abia mai bune, iar prognozele de densitate se pot îmbunătăți prin regimul de varianță",
                    "Prognozele punctuale sînt întotdeauna mult mai bune",
                    "Prognozele de densitate sînt întotdeauna mai slabe",
                    "Modelele cu regimuri nu pot produce prognoze de densitate"
                ],
                "correctExplanation": "În curs, RMSE pentru AR(1) și MSIH(2)-AR(1) sînt aproape egale, iar scorul logaritmic se îmbunătățește, mai ales în perioadele calme; cîștigurile trebuie testate cu teste de tip Diebold–Mariano.",
                "incorrectExplanation": "Cîștigurile mari în prognozele punctuale sînt rare; densitatea predictivă este un amestec și este adesea mai bine calibrată; modelele cu regimuri produc în mod natural densități predictive."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the error in the AI answer: regimes and recessions",
                "text": "An AI assistant writes: 'The MSIH(2)-AR(1) model of US GDP is significant by the bootstrap LR test, so its two regimes are recessions and expansions.' What is wrong?",
                "options": [
                    "The bootstrap LR test is never significant",
                    "Significance shows that two regimes fit better, not what they mean; on 1947–2019 the regimes are volatility eras (the Great Moderation), not recessions",
                    "The model has three regimes",
                    "Nothing: a significant test identifies recessions"
                ],
                "correctExplanation": "In the lecture the two regimes have standard deviations of about 0.46 and 1.1 pp and last decades: they separate the high-volatility era before 1984 from the calm one after it.",
                "incorrectExplanation": "The test is significant here; the model has two regimes; significance says nothing about the economic meaning of the regimes, which must be checked against external events."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI: regimuri și recesiuni",
                "text": "Un asistent AI scrie: „Modelul MSIH(2)-AR(1) pentru PIB-ul SUA este semnificativ după testul LR bootstrap, deci cele două regimuri sînt recesiuni și expansiuni.” Ce este greșit?",
                "options": [
                    "Testul LR bootstrap nu este niciodată semnificativ",
                    "Semnificația arată că două regimuri se potrivesc mai bine, nu ce înseamnă ele; pe 1947–2019 regimurile sînt ere de volatilitate (Marea Moderație), nu recesiuni",
                    "Modelul are trei regimuri",
                    "Nimic: un test semnificativ identifică recesiunile"
                ],
                "correctExplanation": "În curs, cele două regimuri au abateri standard de aproximativ 0,46 și 1,1 pp și durează decenii: separă era de volatilitate ridicată de dinainte de 1984 de cea calmă de după.",
                "incorrectExplanation": "Testul este semnificativ aici; modelul are două regimuri; semnificația nu spune nimic despre sensul economic al regimurilor, care trebuie verificat față de evenimente externe."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer: one specification",
                "text": "An AI summary reports: 'Markov-switching models date the 2001 US recession correctly.' In the lecture's mini-case, 12 defensible specifications were estimated. What is wrong with the summary?",
                "options": [
                    "All 12 variants date 2001 correctly",
                    "None of the variants dates 2008",
                    "Only one of the 12 variants dates both 2001 and 2008 without false alarms; reporting one variant as the result hides the dependence on specification and sample",
                    "Markov-switching models cannot be compared with NBER dates"
                ],
                "correctExplanation": "The QPS against the NBER quarters ranges widely across specifications and samples; a robust claim needs the whole set of pre-registered variants.",
                "incorrectExplanation": "Most variants miss 2001 or flag almost every quarter; most catch 2008; comparing with NBER dates through QPS and concordance is standard."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI: o singură specificație",
                "text": "Un rezumat AI afirmă: „Modelele Markov switching datează corect recesiunea din 2001 din SUA.” În mini studiul de caz din curs au fost estimate 12 specificații justificabile. Ce este greșit în rezumat?",
                "options": [
                    "Toate cele 12 variante datează corect 2001",
                    "Niciuna dintre variante nu datează 2008",
                    "Doar una dintre cele 12 variante datează atît 2001, cît și 2008 fără alarme false; raportarea unei singure variante drept rezultat ascunde dependența de specificație și de eșantion",
                    "Modelele Markov switching nu pot fi comparate cu datările NBER"
                ],
                "correctExplanation": "QPS față de trimestrele NBER variază mult între specificații și eșantioane; o afirmație robustă cere întregul set de variante preînregistrate.",
                "incorrectExplanation": "Majoritatea variantelor ratează 2001 sau semnalează aproape fiecare trimestru; cele mai multe prind 2008; compararea cu datările NBER prin QPS și concordanță este standard."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer: EM",
                "text": "An AI assistant writes code for EM and says: 'Since every EM step increases the likelihood, one run from any starting value gives the maximum likelihood estimate.' What is wrong?",
                "options": [
                    "EM can decrease the likelihood",
                    "EM always converges in one step",
                    "EM does not apply to Markov-switching models",
                    "Monotonicity guarantees convergence to a stationary point, not to the global maximum; in the lecture 30 starts converge to two different limits (one degenerate) and statsmodels stops at a third"
                ],
                "correctExplanation": "Mixture likelihoods are multimodal; good practice uses many starts, a numerical polish and a check that the chosen maximum is not degenerate.",
                "incorrectExplanation": "With a free initial distribution EM never lowers the likelihood; convergence is typically slow; Hamilton (1990) derived EM precisely for this model."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI: EM",
                "text": "Un asistent AI scrie cod pentru EM și afirmă: „Deoarece fiecare pas EM crește verosimilitatea, o singură rulare din orice punct de pornire dă estimația de verosimilitate maximă.” Ce este greșit?",
                "options": [
                    "EM poate scădea verosimilitatea",
                    "EM converge întotdeauna într-un singur pas",
                    "EM nu se aplică modelelor Markov switching",
                    "Monotonia garantează convergența la un punct staționar, nu la maximul global; în curs, 30 de puncte de pornire converg la două limite diferite (una degenerată), iar statsmodels se oprește la a treia"
                ],
                "correctExplanation": "Verosimilitățile amestecurilor sînt multimodale; buna practică folosește multe puncte de pornire, o rafinare numerică și verificarea faptului că maximul ales nu este degenerat.",
                "incorrectExplanation": "Cu o distribuție inițială liberă, EM nu scade niciodată verosimilitatea; convergența este de obicei lentă; Hamilton (1990) a derivat EM tocmai pentru acest model."
            }
        }
    ]
};
