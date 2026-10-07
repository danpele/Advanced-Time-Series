// ============================================================
// Chapter 15 quiz bank: Review and project defence (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['review'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Long-run variance of an AR(1)",
                "text": "For an AR(1) with $\\phi = 0.6$, by what factor is the variance of the sample mean understated when i.i.d. standard errors are used (ratio $\\Omega/\\gamma_0$)?",
                "options": [
                    "4",
                    "1.6",
                    "2.5",
                    "0.64"
                ],
                "correctExplanation": "$\\Omega/\\gamma_0 = (1 + \\phi)/(1 - \\phi) = 1.6/0.4 = 4$, so standard errors are too small by a factor of 2.",
                "incorrectExplanation": "The ratio is $(1 + \\phi)/(1 - \\phi)$, not $1 + \\phi$, $1/(1 - \\phi)$ or $\\phi^2$."
            },
            "ro": {
                "title": "Varianța de termen lung a unui AR(1)",
                "text": "Pentru un AR(1) cu $\\phi = 0{,}6$, de cîte ori este subestimată varianța mediei de selecție cînd se folosesc erori standard i.i.d. (raportul $\\Omega/\\gamma_0$)?",
                "options": [
                    "4",
                    "1,6",
                    "2,5",
                    "0,64"
                ],
                "correctExplanation": "$\\Omega/\\gamma_0 = (1 + \\phi)/(1 - \\phi) = 1{,}6/0{,}4 = 4$, deci erorile standard sînt prea mici de 2 ori.",
                "incorrectExplanation": "Raportul este $(1 + \\phi)/(1 - \\phi)$, nu $1 + \\phi$, $1/(1 - \\phi)$ sau $\\phi^2$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Nested forecast comparison",
                "text": "A team compares an AR(1) forecast of the monthly EUR/RON change with the random walk (zero change). Which test of equal accuracy is appropriate?",
                "options": [
                    "The Diebold--Mariano test with Normal critical values",
                    "The Clark--West test",
                    "A Kupiec test of the forecast errors",
                    "A Ljung--Box test of the random-walk errors"
                ],
                "correctExplanation": "The random walk is nested in the AR(1); under the null the DM statistic is not asymptotically Normal and is undersized, and Clark--West adjusts the loss differential for the estimation noise of the larger model.",
                "incorrectExplanation": "DM is designed for non-nested comparisons; Kupiec tests VaR exceedances and Ljung--Box tests autocorrelation, not relative accuracy."
            },
            "ro": {
                "title": "Comparație între modele imbricate",
                "text": "O echipă compară prognoza AR(1) a variației lunare EUR/RON cu mersul aleator (variație zero). Ce test de egalitate a preciziei este potrivit?",
                "options": [
                    "Testul Diebold--Mariano cu valori critice din distribuția Normală",
                    "Testul Clark--West",
                    "Un test Kupiec pentru erorile de prognoză",
                    "Un test Ljung--Box pentru erorile mersului aleator"
                ],
                "correctExplanation": "Mersul aleator este inclus în AR(1); sub ipoteza nulă statistica DM nu are asimptotic distribuția Normală și este subdimensionată, iar Clark--West ajustează diferența pierderilor pentru zgomotul de estimare al modelului mai mare.",
                "incorrectExplanation": "DM este construit pentru comparații între modele neimbricate; Kupiec testează depășirile VaR, iar Ljung--Box autocorelația, nu precizia relativă."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "A break date chosen from the data",
                "text": "A researcher picks the date with the largest Chow statistic and compares it with the $\\chi^2_1$ 5% critical value 3.84. What is the consequence?",
                "options": [
                    "The test is conservative: it rejects less than 5% of the time",
                    "Nothing: the Chow test is valid at any date",
                    "The test rejects far more than 5% of the time under the null; sup-type critical values are needed",
                    "The test becomes valid only if the sample is large"
                ],
                "correctExplanation": "Searching over dates makes the statistic a supremum of a process; Chapter 2 found sizes of 33--40% with 3.84, and the sup critical value is about 8.65.",
                "incorrectExplanation": "The date search inflates size at every sample size; the remedy is Andrews-type critical values for sup, exp or ave statistics."
            },
            "ro": {
                "title": "O dată a rupturii aleasă din date",
                "text": "Un cercetător alege data cu cea mai mare statistică Chow și o compară cu valoarea critică $\\chi^2_1$ de 5%, 3,84. Care este consecința?",
                "options": [
                    "Testul este conservator: respinge în mai puțin de 5% din cazuri",
                    "Niciuna: testul Chow este valid la orice dată",
                    "Testul respinge mult mai des decît în 5% din cazuri sub ipoteza nulă; sînt necesare valori critice de tip sup",
                    "Testul devine valid doar dacă eșantionul este mare"
                ],
                "correctExplanation": "Căutarea datei face din statistică supremul unui proces; în Capitolul 2 mărimea a fost 33--40% cu 3,84, iar valoarea critică sup este aproximativ 8,65.",
                "incorrectExplanation": "Căutarea datei mărește mărimea testului la orice dimensiune a eșantionului; remediul îl constituie valorile critice de tip Andrews pentru statisticile sup, exp sau ave."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The identifying assumption of a recursive SVAR",
                "text": "In a recursive (Cholesky) SVAR, what is the identifying assumption?",
                "options": [
                    "That the reduced-form errors are uncorrelated",
                    "That all variables are stationary",
                    "That the impulse responses die out within one year",
                    "That the variables ordered first do not respond on impact to shocks of the variables ordered later"
                ],
                "correctExplanation": "The Cholesky factor imposes zeros on impact above the diagonal; the ordering is the economics of the identification.",
                "incorrectExplanation": "Reduced-form errors are correlated in general (that is why a rotation is needed); stationarity and the decay of responses do not identify the shocks."
            },
            "ro": {
                "title": "Ipoteza de identificare a unui SVAR recursiv",
                "text": "Într-un SVAR recursiv (Cholesky), care este ipoteza de identificare?",
                "options": [
                    "Că erorile formei reduse sînt necorelate",
                    "Că toate variabilele sînt staționare",
                    "Că răspunsurile la impuls se sting într-un an",
                    "Că variabilele ordonate primele nu răspund imediat la șocurile variabilelor ordonate după ele"
                ],
                "correctExplanation": "Factorul Cholesky impune zerouri pe impact deasupra diagonalei; ordonarea reprezintă conținutul economic al identificării.",
                "incorrectExplanation": "Erorile formei reduse sînt în general corelate (de aceea este necesară o rotație); staționaritatea și stingerea răspunsurilor nu identifică șocurile."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Half-life of an equilibrium error",
                "text": "In a VECM without short-run terms, $\\beta'\\alpha = -0.25$. What is the half-life of a deviation from equilibrium?",
                "options": [
                    "About 2.4 periods",
                    "About 4 periods",
                    "About 0.25 periods",
                    "About 2.8 periods"
                ],
                "correctExplanation": "$z_t = (1 + \\beta'\\alpha)z_{t-1} + \\dots = 0.75z_{t-1} + \\dots$, so the half-life is $\\ln 0.5/\\ln 0.75 \\approx 2.41$.",
                "incorrectExplanation": "The coefficient of the equilibrium error is $1 + \\beta'\\alpha$, not $\\beta'\\alpha$; $1/0.25 = 4$ is not a half-life and $\\ln 2/0.25$ uses a continuous-time approximation that is inaccurate here."
            },
            "ro": {
                "title": "Timpul de înjumătățire al unei abateri de la echilibru",
                "text": "Într-un VECM fără termeni de termen scurt, $\\beta'\\alpha = -0{,}25$. Care este timpul de înjumătățire al unei abateri de la echilibru?",
                "options": [
                    "Aproximativ 2,4 perioade",
                    "Aproximativ 4 perioade",
                    "Aproximativ 0,25 perioade",
                    "Aproximativ 2,8 perioade"
                ],
                "correctExplanation": "$z_t = (1 + \\beta'\\alpha)z_{t-1} + \\dots = 0{,}75z_{t-1} + \\dots$, deci timpul de înjumătățire este $\\ln 0{,}5/\\ln 0{,}75 \\approx 2{,}41$.",
                "incorrectExplanation": "Coeficientul abaterii de la echilibru este $1 + \\beta'\\alpha$, nu $\\beta'\\alpha$; $1/0{,}25 = 4$ nu este un timp de înjumătățire, iar $\\ln 2/0{,}25$ folosește o aproximare în timp continuu, imprecisă aici."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "One Kalman step",
                "text": "Local level model with predicted state variance $P = 2$ and measurement variance $\\sigma^2_\\varepsilon = 4$. What is the Kalman gain?",
                "options": [
                    "2",
                    "1/3",
                    "1/2",
                    "2/3"
                ],
                "correctExplanation": "$F = P + \\sigma^2_\\varepsilon = 6$ and $K = P/F = 1/3$: the filter moves one third of the way towards the new observation.",
                "incorrectExplanation": "The gain is the share of the prediction-error variance due to the state, $P/(P + \\sigma^2_\\varepsilon)$, a number between 0 and 1."
            },
            "ro": {
                "title": "Un pas Kalman",
                "text": "Modelul cu nivel local, cu varianța stării prognozate $P = 2$ și varianța măsurătorii $\\sigma^2_\\varepsilon = 4$. Care este cîștigul Kalman?",
                "options": [
                    "2",
                    "1/3",
                    "1/2",
                    "2/3"
                ],
                "correctExplanation": "$F = P + \\sigma^2_\\varepsilon = 6$, iar $K = P/F = 1/3$: filtrul se deplasează o treime din distanța pînă la noua observație.",
                "incorrectExplanation": "Cîștigul este proporția din varianța erorii de prognoză datorată stării, $P/(P + \\sigma^2_\\varepsilon)$, un număr între 0 și 1."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Expected duration of a regime",
                "text": "In a two-state Markov chain the probability of staying in regime 1 is $p_{11} = 0.95$ (monthly data). What is the expected duration of regime 1?",
                "options": [
                    "0.95 months",
                    "5 months",
                    "20 months",
                    "95 months"
                ],
                "correctExplanation": "Durations are geometric: $\\E D_1 = 1/(1 - p_{11}) = 1/0.05 = 20$ months.",
                "incorrectExplanation": "The expected duration is $1/(1 - p_{11})$; the other values confuse it with the probability or with the duration of the other regime."
            },
            "ro": {
                "title": "Durata așteptată a unui regim",
                "text": "Într-un lanț Markov cu două stări, probabilitatea de a rămîne în regimul 1 este $p_{11} = 0{,}95$ (date lunare). Care este durata așteptată a regimului 1?",
                "options": [
                    "0,95 luni",
                    "5 luni",
                    "20 de luni",
                    "95 de luni"
                ],
                "correctExplanation": "Duratele sînt geometrice: $\\E D_1 = 1/(1 - p_{11}) = 1/0{,}05 = 20$ de luni.",
                "incorrectExplanation": "Durata așteptată este $1/(1 - p_{11})$; celelalte valori o confundă cu probabilitatea sau cu durata celuilalt regim."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Testing the number of regimes",
                "text": "Why can the likelihood-ratio test of one regime against two not use $\\chi^2$ critical values?",
                "options": [
                    "Because the likelihood of a Markov-switching model cannot be computed",
                    "Because the test has two degrees of freedom instead of one",
                    "Because regime models are always estimated by Bayesian methods",
                    "Because under the null the transition probabilities are not identified, a parameter is on the boundary and the score is zero"
                ],
                "correctExplanation": "These non-standard conditions (the Davies problem, the boundary and a degenerate score) invalidate the $\\chi^2$ limit; Chapter 7 found a bootstrap 95% quantile of 12.32 against 5.99.",
                "incorrectExplanation": "The Hamilton filter computes the likelihood exactly; the number of degrees of freedom is not the issue, and the test is a frequentist problem."
            },
            "ro": {
                "title": "Testarea numărului de regimuri",
                "text": "De ce nu poate testul raportului de verosimilitate al unui regim față de două regimuri să folosească valori critice $\\chi^2$?",
                "options": [
                    "Pentru că verosimilitatea unui model cu schimbare de regim nu poate fi calculată",
                    "Pentru că testul are două grade de libertate în loc de unul",
                    "Pentru că modelele cu regimuri se estimează întotdeauna prin metode bayesiene",
                    "Pentru că sub ipoteza nulă probabilitățile de tranziție nu sînt identificate, un parametru este la limită și scorul este zero"
                ],
                "correctExplanation": "Aceste condiții nestandard (problema Davies, limita și scorul degenerat) anulează limita $\\chi^2$; în Capitolul 7 cuantila bootstrap de 95% a fost 12,32, față de 5,99.",
                "incorrectExplanation": "Filtrul Hamilton calculează exact verosimilitatea; numărul gradelor de libertate nu este problema, iar testul este o problemă frecvenționistă."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "GARCH with fat tails",
                "text": "A GARCH(1,1) is estimated by Gaussian QML on daily returns with Student-$t(5)$-like innovations. Which standard errors should be reported?",
                "options": [
                    "Sandwich (Bollerslev--Wooldridge) standard errors",
                    "Hessian standard errors, because QML is efficient",
                    "Outer-product-of-gradient standard errors only",
                    "No standard errors: QML is inconsistent with fat tails"
                ],
                "correctExplanation": "QML stays consistent, but its covariance is $(\\kappa_\\eta - 1)J^{-1}$; Chapter 8 found Hessian intervals covering 73% instead of 95%, sandwich intervals 92%.",
                "incorrectExplanation": "With fat tails the information matrix equality fails, so neither the Hessian nor the outer product alone is valid; QML remains consistent."
            },
            "ro": {
                "title": "GARCH cu cozi groase",
                "text": "Un GARCH(1,1) este estimat prin QML gaussian pe randamente zilnice cu inovații de tip Student-$t(5)$. Ce erori standard trebuie raportate?",
                "options": [
                    "Erori standard sandwich (Bollerslev--Wooldridge)",
                    "Erori standard din hessiană, pentru că QML este eficient",
                    "Doar erori standard din produsul exterior al gradienților",
                    "Niciuna: QML nu este consistent cu cozi groase"
                ],
                "correctExplanation": "QML rămîne consistent, dar covarianța lui este $(\\kappa_\\eta - 1)J^{-1}$; în Capitolul 8 intervalele din hessiană au acoperit 73% în loc de 95%, iar cele sandwich 92%.",
                "incorrectExplanation": "Cu cozi groase egalitatea matricei de informație nu mai este valabilă, deci nici hessiana, nici produsul exterior nu sînt valide singure; QML rămîne consistent."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Scoring expected shortfall",
                "text": "Which statement about expected shortfall (ES) is correct?",
                "options": [
                    "ES is elicitable alone, so the average quantile loss ranks ES forecasts",
                    "ES is jointly elicitable with VaR, for example with the FZ0 loss",
                    "ES cannot be backtested or compared at all",
                    "ES is elicitable because it is a coherent risk measure"
                ],
                "correctExplanation": "ES has no consistent scoring function on its own, but the pair (VaR, ES) has, which is why Chapter 9 compared models with FZ0.",
                "incorrectExplanation": "Coherence and elicitability are different properties; ES alone is not elicitable, yet joint scores and backtests exist."
            },
            "ro": {
                "title": "Evaluarea expected shortfall",
                "text": "Ce afirmație despre expected shortfall (ES) este corectă?",
                "options": [
                    "ES este elicitabil singur, deci pierderea medie de cuantilă ierarhizează prognozele ES",
                    "ES este elicitabil împreună cu VaR, de exemplu cu pierderea FZ0",
                    "ES nu poate fi testat retroactiv sau comparat deloc",
                    "ES este elicitabil pentru că este o măsură de risc coerentă"
                ],
                "correctExplanation": "ES nu are o funcție de scor consistentă singur, dar perechea (VaR, ES) are, de aceea în Capitolul 9 modelele au fost comparate cu FZ0.",
                "incorrectExplanation": "Coerența și elicitabilitatea sînt proprietăți diferite; ES singur nu este elicitabil, dar există scoruri comune și backtest-uri."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Long memory or level shifts?",
                "text": "Which evidence points to spurious long memory created by level shifts?",
                "options": [
                    "A local Whittle estimate $\\hat d$ that is stable across bandwidths",
                    "A slowly decaying sample autocorrelation function",
                    "A rejection by the Qu test and $\\hat d(m)$ that falls as the bandwidth $m$ grows",
                    "A Hurst exponent of about 0.1"
                ],
                "correctExplanation": "Level shifts add power at the lowest frequencies only, so $\\hat d(m)$ decreases with $m$; the Qu (2011) test is built on this signature.",
                "incorrectExplanation": "A slow ACF decay is shared by true long memory and shifts; stable $\\hat d(m)$ supports true memory, and $H \\approx 0.1$ is about roughness, not persistence."
            },
            "ro": {
                "title": "Memorie lungă sau salturi de nivel?",
                "text": "Ce dovadă indică o memorie lungă falsă, produsă de salturi de nivel?",
                "options": [
                    "O estimație local Whittle $\\hat d$ stabilă la toate lățimile de bandă",
                    "O funcție de autocorelație de selecție care scade lent",
                    "O respingere în testul Qu și un $\\hat d(m)$ care scade cînd lățimea de bandă $m$ crește",
                    "Un exponent Hurst de aproximativ 0,1"
                ],
                "correctExplanation": "Salturile de nivel adaugă putere doar la frecvențele cele mai joase, deci $\\hat d(m)$ scade odată cu $m$; testul Qu (2011) se bazează pe această semnătură.",
                "incorrectExplanation": "O scădere lentă a ACF este comună memoriei lungi reale și salturilor; un $\\hat d(m)$ stabil susține memoria reală, iar $H \\approx 0{,}1$ privește caracterul rough, nu persistența."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The HP filter and a random walk",
                "text": "What did Cogley and Nason (1995) show, and Chapter 11 replicate?",
                "options": [
                    "The HP filter removes all cycles from a random walk",
                    "The HP cycle of a random walk is white noise",
                    "The HP filter is optimal for any integrated series",
                    "Applied to a random walk, the HP filter creates a spurious cycle with a peak at about 7.5 years for quarterly data"
                ],
                "correctExplanation": "The squared gain of the HP cycle filter applied to the spectrum of a random walk peaks at about 30 quarters: a cycle produced by the filter, not by the data.",
                "incorrectExplanation": "The HP cycle of a random walk is strongly autocorrelated, not white noise, and the filter is not optimal for difference-stationary series."
            },
            "ro": {
                "title": "Filtrul HP și mersul aleator",
                "text": "Ce au arătat Cogley și Nason (1995), replicat în Capitolul 11?",
                "options": [
                    "Filtrul HP elimină toate ciclurile unui mers aleator",
                    "Ciclul HP al unui mers aleator este zgomot alb",
                    "Filtrul HP este optim pentru orice serie integrată",
                    "Aplicat unui mers aleator, filtrul HP creează un ciclu fals cu vîrful la aproximativ 7,5 ani pentru date trimestriale"
                ],
                "correctExplanation": "Pătratul cîștigului filtrului HP aplicat spectrului unui mers aleator are vîrful la aproximativ 30 de trimestre: un ciclu produs de filtru, nu de date.",
                "incorrectExplanation": "Ciclul HP al unui mers aleator este puternic autocorelat, nu zgomot alb, iar filtrul nu este optim pentru seriile staționare în diferențe."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Cross-validation for time series",
                "text": "According to Bergmeir, Hyndman and Koo (2018), when is standard K-fold cross-validation valid for time series?",
                "options": [
                    "For well-specified autoregressions with uncorrelated errors",
                    "For any model, if the folds are chosen at random",
                    "Never: only the last observation may be used for validation",
                    "Only for tree ensembles"
                ],
                "correctExplanation": "With uncorrelated residuals the folds behave like independent samples; Chapter 12 found a validation error of 0.094 against 0.137 out of sample, as in the paper.",
                "incorrectExplanation": "With autocorrelated residuals (under-specified models, overlapping targets) random folds leak; then use blocked or purged validation."
            },
            "ro": {
                "title": "Validarea încrucișată pentru serii de timp",
                "text": "Conform lui Bergmeir, Hyndman și Koo (2018), cînd este validă validarea încrucișată K-fold standard pentru serii de timp?",
                "options": [
                    "Pentru autoregresii bine specificate, cu erori necorelate",
                    "Pentru orice model, dacă partițiile sînt alese aleator",
                    "Niciodată: doar ultima observație poate fi folosită pentru validare",
                    "Doar pentru ansamblurile de arbori"
                ],
                "correctExplanation": "Cu reziduuri necorelate, partițiile se comportă ca eșantioane independente; în Capitolul 12 eroarea de validare a fost 0,094, față de 0,137 în afara eșantionului, ca în lucrare.",
                "incorrectExplanation": "Cu reziduuri autocorelate (modele subspecificate, ținte suprapuse) partițiile aleatoare produc leakage; atunci se folosește validarea pe blocuri sau cu purjare."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The split-conformal quantile",
                "text": "Split conformal prediction with $n = 19$ calibration scores and $\\alpha = 0.1$: which order statistic is the threshold $\\hat q$?",
                "options": [
                    "The 17th smallest",
                    "The 18th smallest",
                    "The 19th smallest",
                    "The 10th smallest"
                ],
                "correctExplanation": "$k = \\lceil (n + 1)(1 - \\alpha) \\rceil = \\lceil 20 \\cdot 0.9 \\rceil = 18$.",
                "incorrectExplanation": "The finite-sample correction uses $n + 1$; the 10th order statistic is the median, and the 17th and 19th do not satisfy the formula."
            },
            "ro": {
                "title": "Cuantila split conformal",
                "text": "Predicție split conformal cu $n = 19$ scoruri de calibrare și $\\alpha = 0{,}1$: ce statistică de ordine este pragul $\\hat q$?",
                "options": [
                    "A 17-a cea mai mică",
                    "A 18-a cea mai mică",
                    "A 19-a cea mai mică",
                    "A 10-a cea mai mică"
                ],
                "correctExplanation": "$k = \\lceil (n + 1)(1 - \\alpha) \\rceil = \\lceil 20 \\cdot 0{,}9 \\rceil = 18$.",
                "incorrectExplanation": "Corecția pentru eșantion finit folosește $n + 1$; a 10-a statistică de ordine este mediana, iar a 17-a și a 19-a nu corespund formulei."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Placebo inference for synthetic control",
                "text": "A synthetic control study has 19 donor units and the treated unit has the largest post/pre RMSPE ratio. What is the placebo $p$-value?",
                "options": [
                    "0.01",
                    "0.019",
                    "0.05",
                    "0.10"
                ],
                "correctExplanation": "$p = \\#\\{j: r_j \\ge r_1\\}/(J + 1) = 1/20 = 0.05$, which is also the smallest attainable value.",
                "incorrectExplanation": "With $J$ donors the permutation $p$-value is a multiple of $1/(J + 1)$; values below $1/20$ cannot occur."
            },
            "ro": {
                "title": "Inferența placebo pentru controlul sintetic",
                "text": "Un studiu cu control sintetic are 19 donatori, iar unitatea tratată are cel mai mare raport RMSPE după/înainte. Care este p-value-ul placebo?",
                "options": [
                    "0,01",
                    "0,019",
                    "0,05",
                    "0,10"
                ],
                "correctExplanation": "$p = \\#\\{j: r_j \\ge r_1\\}/(J + 1) = 1/20 = 0{,}05$, care este și cea mai mică valoare posibilă.",
                "incorrectExplanation": "Cu $J$ donatori, p-value-ul prin permutare este un multiplu de $1/(J + 1)$; valori sub $1/20$ nu sînt posibile."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Bubble tests under changing volatility",
                "text": "Volatility triples late in a sample with no bubble. What happens to GSADF with Monte Carlo critical values, and what fixes it?",
                "options": [
                    "Nothing: GSADF is pivotal under any volatility",
                    "The test loses all power; a longer window fixes it",
                    "The test becomes conservative; Bonferroni fixes it",
                    "The test over-rejects (about 34% in Chapter 16); the wild bootstrap restores the size"
                ],
                "correctExplanation": "Monte Carlo critical values assume constant variance; the wild bootstrap of Harvey et al. (2016) keeps the volatility path and brought the size back to about 3%.",
                "incorrectExplanation": "Non-stationary volatility changes the null distribution, so the test over-rejects; window length and Bonferroni do not address it."
            },
            "ro": {
                "title": "Teste de bule sub volatilitate variabilă",
                "text": "Volatilitatea se triplează spre sfîrșitul unui eșantion fără bulă. Ce se întîmplă cu GSADF cu valori critice Monte Carlo și ce corectează problema?",
                "options": [
                    "Nimic: GSADF este pivotal sub orice volatilitate",
                    "Testul își pierde toată puterea; o fereastră mai lungă rezolvă problema",
                    "Testul devine conservator; Bonferroni rezolvă problema",
                    "Testul respinge prea des (aproximativ 34% în Capitolul 16); wild bootstrap restabilește mărimea"
                ],
                "correctExplanation": "Valorile critice Monte Carlo presupun varianța constantă; wild bootstrap-ul lui Harvey et al. (2016) păstrează traiectoria volatilității și a adus mărimea la aproximativ 3%.",
                "incorrectExplanation": "Volatilitatea nestaționară schimbă distribuția sub ipoteza nulă, deci testul respinge prea des; lungimea ferestrei și Bonferroni nu rezolvă această problemă."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "A specification search",
                "text": "A team tries 20 independent predictors of a series with no predictability, each tested at 5%, and reports the best. What is the probability of at least one ``significant'' predictor?",
                "options": [
                    "About 64%",
                    "Exactly 5%",
                    "About 20%",
                    "About 1%"
                ],
                "correctExplanation": "$1 - 0.95^{20} \\approx 0.64$: Chapter 0 found 64% by simulation; persistent predictors make it worse.",
                "incorrectExplanation": "Each test has a 5% false-positive rate, so the chance that at least one of 20 rejects is far above 5%."
            },
            "ro": {
                "title": "O căutare de specificații",
                "text": "O echipă încearcă 20 de predictori independenți ai unei serii fără predictibilitate, fiecare testat la 5%, și îl raportează pe cel mai bun. Care este probabilitatea ca cel puțin un predictor să fie „semnificativ”?",
                "options": [
                    "Aproximativ 64%",
                    "Exact 5%",
                    "Aproximativ 20%",
                    "Aproximativ 1%"
                ],
                "correctExplanation": "$1 - 0{,}95^{20} \\approx 0{,}64$: în Capitolul 0 simularea a dat 64%; predictorii persistenți agravează situația.",
                "incorrectExplanation": "Fiecare test are o rată de 5% a rezultatelor fals pozitive, deci șansa ca cel puțin unul din 20 să respingă este mult peste 5%."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Leakage by selection",
                "text": "Predictors are selected by their correlation with the target over the whole sample, then a model is fitted on the training period and evaluated on the last 60 periods. With pure-noise predictors, what happens?",
                "options": [
                    "The out-of-sample $R^2$ is negative on average, as it should be",
                    "The out-of-sample $R^2$ is positive in most replications although nothing is predictable",
                    "The model cannot be estimated",
                    "The out-of-sample $R^2$ is exactly zero"
                ],
                "correctExplanation": "The test period took part in the selection, so noise that happens to correlate with the target there is kept; in Lecture 15 the $R^2$ was positive in 81% of runs against 8% with honest selection.",
                "incorrectExplanation": "An honest protocol gives a negative mean $R^2$ for noise; selection on the whole sample leaks the test period into the model."
            },
            "ro": {
                "title": "Leakage prin selecție",
                "text": "Predictorii sînt selectați după corelația cu ținta pe întregul eșantion, apoi un model este estimat pe perioada de antrenare și evaluat pe ultimele 60 de perioade. Cu predictori de tip zgomot pur, ce se întîmplă?",
                "options": [
                    "$R^2$ în afara eșantionului este negativ în medie, cum ar trebui",
                    "$R^2$ în afara eșantionului este pozitiv în majoritatea replicărilor, deși nimic nu este predictibil",
                    "Modelul nu poate fi estimat",
                    "$R^2$ în afara eșantionului este exact zero"
                ],
                "correctExplanation": "Perioada de test a participat la selecție, deci zgomotul care se întîmplă să fie corelat cu ținta acolo este păstrat; în Cursul 15, $R^2$ a fost pozitiv în 81% din rulări, față de 8% cu selecția corectă.",
                "incorrectExplanation": "Un protocol corect dă un $R^2$ mediu negativ pentru zgomot; selecția pe întregul eșantion introduce perioada de test în model."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Power and the evaluation length",
                "text": "The out-of-sample length needed for 80% power of a DM test is $P \\approx \\Omega_d (z_{0.975} + z_{0.8})^2/\\delta^2$. If the expected gain $\\delta$ doubles, the needed length",
                "options": [
                    "doubles",
                    "is halved",
                    "falls to one quarter",
                    "does not change"
                ],
                "correctExplanation": "$P$ is proportional to $1/\\delta^2$, so doubling $\\delta$ divides $P$ by 4.",
                "incorrectExplanation": "The length depends on the square of the effect size, not on the effect size itself."
            },
            "ro": {
                "title": "Puterea și lungimea evaluării",
                "text": "Lungimea eșantionului de evaluare necesară pentru o putere de 80% a unui test DM este $P \\approx \\Omega_d (z_{0{,}975} + z_{0{,}8})^2/\\delta^2$. Dacă cîștigul așteptat $\\delta$ se dublează, lungimea necesară",
                "options": [
                    "se dublează",
                    "se înjumătățește",
                    "scade la un sfert",
                    "nu se schimbă"
                ],
                "correctExplanation": "$P$ este proporțional cu $1/\\delta^2$, deci dublarea lui $\\delta$ împarte $P$ la 4.",
                "incorrectExplanation": "Lungimea depinde de pătratul mărimii efectului, nu de mărimea efectului."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "A replication that differs",
                "text": "A team cannot reproduce Table 2 of its landmark paper on today's data. What is the best practice?",
                "options": [
                    "Report the extension only and drop the replication",
                    "Adjust the sample until the published number appears",
                    "Conclude that the paper is wrong",
                    "Run the original sample and specification first, then attribute the difference to data vintage, sample, implementation or inference"
                ],
                "correctExplanation": "Separating the sources of the difference turns a failed replication into a result; the course found vintage, sample and inference to be the usual causes.",
                "incorrectExplanation": "Dropping or tuning the replication hides information, and a difference alone does not show that the paper is wrong."
            },
            "ro": {
                "title": "O replicare care diferă",
                "text": "O echipă nu poate reproduce tabelul 2 al lucrării de referință pe datele de azi. Care este practica recomandată?",
                "options": [
                    "Raportarea doar a extensiei, fără replicare",
                    "Ajustarea eșantionului pînă cînd apare rezultatul publicat",
                    "Concluzia că lucrarea este greșită",
                    "Rularea întîi a eșantionului și a specificației originale, apoi atribuirea diferenței ediției datelor, eșantionului, implementării sau inferenței"
                ],
                "correctExplanation": "Separarea surselor diferenței transformă o replicare nereușită într-un rezultat; în curs, cauzele obișnuite au fost ediția datelor, eșantionul și inferența.",
                "incorrectExplanation": "Renunțarea la replicare sau ajustarea ei ascunde informație, iar o diferență nu arată singură că lucrarea este greșită."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant gave four statements about forecast comparison. Which one is wrong?",
                "options": [
                    "The Diebold--Mariano test is valid for nested models without any adjustment",
                    "With overlapping $h$-step errors, the HAC variance needs at least $h - 1$ lags",
                    "With few multi-step forecasts, the HLN correction and $t_{P-1}$ critical values are advisable",
                    "With many models, a model confidence set is preferable to pairwise tests"
                ],
                "correctExplanation": "For nested models the DM statistic is not asymptotically Normal under the null and is undersized; Clark--West is the adjustment.",
                "incorrectExplanation": "The other three statements are correct recommendations of Chapter 1."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI a formulat patru afirmații despre compararea prognozelor. Care este greșită?",
                "options": [
                    "Testul Diebold--Mariano este valid pentru modele imbricate fără nicio ajustare",
                    "Cu erori suprapuse la $h$ pași, varianța HAC are nevoie de cel puțin $h - 1$ laguri",
                    "Cu puține prognoze pe mai mulți pași, corecția HLN și valorile critice $t_{P-1}$ sînt recomandabile",
                    "Cu multe modele, un model confidence set este preferabil testelor pe perechi"
                ],
                "correctExplanation": "Pentru modele imbricate, statistica DM nu are asimptotic distribuția Normală sub ipoteza nulă și este subdimensionată; ajustarea este Clark--West.",
                "incorrectExplanation": "Celelalte trei afirmații sînt recomandări corecte din Capitolul 1."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Checking an AI-suggested reference",
                "text": "An AI assistant suggests a reference with a DOI for your literature review. What is the adequate check before citing it?",
                "options": [
                    "Ask the assistant whether the reference is real",
                    "Resolve the DOI (for example on Crossref) and check that title, authors and the claimed result match the paper",
                    "Check that the journal name sounds plausible",
                    "Cite it with a note that it was suggested by AI"
                ],
                "correctExplanation": "Fabricated or mismatched citations are a documented failure of language models; the DOI must resolve to the same paper, and the paper must contain the claimed result.",
                "incorrectExplanation": "The assistant cannot verify itself, plausibility is what fabrications imitate, and a note does not make a wrong reference acceptable; the error belongs in AI_ERRORS.md."
            },
            "ro": {
                "title": "Verificarea unei referințe sugerate de AI",
                "text": "Un asistent AI sugerează o referință cu DOI pentru analiza literaturii. Care este verificarea adecvată înainte de a o cita?",
                "options": [
                    "Întrebarea asistentului dacă referința este reală",
                    "Verificarea DOI-ului (de exemplu în Crossref) și a concordanței titlului, autorilor și rezultatului invocat cu lucrarea",
                    "Verificarea faptului că numele revistei pare plauzibil",
                    "Citarea ei cu mențiunea că a fost sugerată de AI"
                ],
                "correctExplanation": "Citările inventate sau nepotrivite sînt o eroare documentată a modelelor de limbaj; DOI-ul trebuie să ducă la aceeași lucrare, iar lucrarea trebuie să conțină rezultatul invocat.",
                "incorrectExplanation": "Asistentul nu se poate verifica singur, plauzibilitatea este exact ce imită referințele inventate, iar o mențiune nu face acceptabilă o referință greșită; eroarea se trece în AI_ERRORS.md."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The oral defence",
                "text": "Which statement about the oral defence of the ATS project is correct?",
                "options": [
                    "All team members receive the team grade for the defence",
                    "AI tools may be used during the defence if declared in AI_USE.md",
                    "Each member is graded individually and must explain the code, the results and the related chapters without AI tools",
                    "The defence covers only the part of the project the member wrote"
                ],
                "correctExplanation": "The defence is 50% of the final grade and individual; grades can differ within a team, and no AI tools are allowed during it.",
                "incorrectExplanation": "The declaration in AI_USE.md covers the project work, not the defence, and each member can be asked about the whole project."
            },
            "ro": {
                "title": "Susținerea orală",
                "text": "Ce afirmație despre susținerea orală a proiectului ATS este corectă?",
                "options": [
                    "Toți membrii echipei primesc la susținere nota echipei",
                    "Instrumentele AI pot fi folosite la susținere dacă sînt declarate în AI_USE.md",
                    "Fiecare membru este evaluat individual și trebuie să explice codul, rezultatele și capitolele corespunzătoare fără instrumente AI",
                    "Susținerea privește doar partea de proiect scrisă de membrul respectiv"
                ],
                "correctExplanation": "Susținerea reprezintă 50% din nota finală și este individuală; notele pot diferi în cadrul unei echipe, iar instrumentele AI nu sînt permise în timpul ei.",
                "incorrectExplanation": "Declarația din AI_USE.md acoperă lucrul la proiect, nu susținerea, iar fiecare membru poate fi întrebat despre întregul proiect."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The pre-registration",
                "text": "Which element must the pre-registration fix before any estimation?",
                "options": [
                    "The final numbers of the report",
                    "Only the title of the project",
                    "The list of references",
                    "The sample split, the loss functions and the tests of the forecast evaluation"
                ],
                "correctExplanation": "Fixing the evaluation design in advance prevents the results from shaping the test; deviations remain possible but are reported.",
                "incorrectExplanation": "Results cannot be fixed in advance, and a title or a reference list does not constrain the analysis."
            },
            "ro": {
                "title": "Preînregistrarea",
                "text": "Ce element trebuie fixat de preînregistrare înaintea oricărei estimări?",
                "options": [
                    "Rezultatele finale ale raportului",
                    "Doar titlul proiectului",
                    "Lista de referințe",
                    "Împărțirea eșantionului, funcțiile de pierdere și testele evaluării prognozelor"
                ],
                "correctExplanation": "Fixarea dinainte a designului evaluării împiedică rezultatele să influențeze testul; abaterile rămîn posibile, dar se raportează.",
                "incorrectExplanation": "Rezultatele nu pot fi fixate dinainte, iar un titlu sau o listă de referințe nu constrîng analiza."
            }
        }
    ]
};
