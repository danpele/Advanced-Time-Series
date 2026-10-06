// ============================================================
// Chapter 4 quiz bank: Cointegration revisited: VECM, ARDL and panel data (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['cointegration-panel'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 3,
            "en": {
                "title": "Johansen eigenvalues",
                "text": "In the Johansen procedure, the eigenvalues $\\hat\\lambda_i$ of $S_{11}^{-1}S_{10}S_{00}^{-1}S_{01}$ are",
                "options": [
                    "the roots of the characteristic polynomial of the VAR in levels",
                    "the variances of the cointegrating relations",
                    "the speeds of adjustment of each variable",
                    "the squared canonical correlations between $\\Delta y_t$ and $y_{t-1}$ after the short-run dynamics are concentrated out"
                ],
                "correctExplanation": "Concentrating out the short run gives $R_{0t}$ and $R_{1t}$; the eigenvalue problem is the canonical correlation analysis between them.",
                "incorrectExplanation": "The eigenvalues are neither VAR roots nor variances nor adjustment speeds; they measure how well linear combinations of levels predict the changes."
            },
            "ro": {
                "title": "Valorile proprii Johansen",
                "text": "În procedura Johansen, valorile proprii $\\hat\\lambda_i$ ale lui $S_{11}^{-1}S_{10}S_{00}^{-1}S_{01}$ sînt",
                "options": [
                    "rădăcinile polinomului caracteristic al VAR-ului în niveluri",
                    "varianțele relațiilor de cointegrare",
                    "vitezele de ajustare ale fiecărei variabile",
                    "corelațiile canonice la pătrat dintre $\\Delta y_t$ și $y_{t-1}$, după eliminarea dinamicii pe termen scurt"
                ],
                "correctExplanation": "Eliminarea dinamicii pe termen scurt dă $R_{0t}$ și $R_{1t}$; problema de valori proprii este analiza corelațiilor canonice dintre ele.",
                "incorrectExplanation": "Valorile proprii nu sînt nici rădăcini ale VAR-ului, nici varianțe, nici viteze de ajustare; ele măsoară cît de bine prezic combinațiile liniare de niveluri modificările."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Trace statistic",
                "text": "With $T = 100$ and eigenvalues $(0.30, 0.12, 0.03)$, the trace statistic for $H(1)$ is approximately",
                "options": [
                    "51.50",
                    "15.83",
                    "12.78",
                    "3.05"
                ],
                "correctExplanation": "$LR_{tr}(1) = -100[\\ln(0.88) + \\ln(0.97)] = 12.78 + 3.05 = 15.83$.",
                "incorrectExplanation": "51.50 is the statistic for $r = 0$; 12.78 is the max-eigenvalue statistic for $r = 1$; 3.05 is the statistic for $r = 2$."
            },
            "ro": {
                "title": "Statistica trace",
                "text": "Cu $T = 100$ și valorile proprii $(0,30; 0,12; 0,03)$, statistica trace pentru $H(1)$ este aproximativ",
                "options": [
                    "51,50",
                    "15,83",
                    "12,78",
                    "3,05"
                ],
                "correctExplanation": "$LR_{tr}(1) = -100[\\ln(0,88) + \\ln(0,97)] = 12,78 + 3,05 = 15,83$.",
                "incorrectExplanation": "51,50 este statistica pentru $r = 0$; 12,78 este statistica max-eigenvalue pentru $r = 1$; 3,05 este statistica pentru $r = 2$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Deterministic case",
                "text": "Two interest rates without drift, whose spread has a non-zero mean, should be modelled in",
                "options": [
                    "case 3: unrestricted constant",
                    "case 4: trend restricted to the cointegrating relation",
                    "case 1: no deterministic terms",
                    "case 2: constant restricted to the cointegrating relation"
                ],
                "correctExplanation": "No drift in the levels and a constant in the relation is exactly the restricted-constant case.",
                "incorrectExplanation": "An unrestricted constant would imply a linear trend in the rates; a restricted trend implies trending relations; case 1 would force a zero-mean spread."
            },
            "ro": {
                "title": "Cazul determinist",
                "text": "Două dobînzi fără drift, a căror diferență are o medie nenulă, se modelează în",
                "options": [
                    "cazul 3: constantă nerestricționată",
                    "cazul 4: trend restricționat la relația de cointegrare",
                    "cazul 1: fără termeni determiniști",
                    "cazul 2: constantă restricționată la relația de cointegrare"
                ],
                "correctExplanation": "Fără drift în niveluri și cu o constantă în relație: exact cazul constantei restricționate.",
                "incorrectExplanation": "O constantă nerestricționată ar implica un trend liniar în dobînzi; un trend restricționat implică relații cu trend; cazul 1 ar forța o diferență de medie zero."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Wrong critical values",
                "text": "A researcher estimates a case-2 model but uses case-3 critical values. The effect on the rank test is",
                "options": [
                    "too few rejections, because case-3 critical values are larger",
                    "none, because the limit distribution does not depend on the case",
                    "too many rejections, because case-3 critical values are smaller",
                    "none, as long as the bootstrap is not used"
                ],
                "correctExplanation": "The 95% quantile for $n - r = 1$ is about 9.2 in case 2 and 3.8 in case 3: using the smaller value rejects too often and overstates the rank.",
                "incorrectExplanation": "The case changes the limit distribution; case-3 quantiles are the smaller ones, so the error goes in the direction of over-rejection."
            },
            "ro": {
                "title": "Valori critice greșite",
                "text": "Un cercetător estimează un model al cazului 2, dar folosește valorile critice ale cazului 3. Efectul asupra testului de rang este",
                "options": [
                    "prea puține respingeri, pentru că valorile critice ale cazului 3 sînt mai mari",
                    "niciunul, pentru că distribuția limită nu depinde de caz",
                    "prea multe respingeri, pentru că valorile critice ale cazului 3 sînt mai mici",
                    "niciunul, atîta timp cît nu se folosește bootstrap-ul"
                ],
                "correctExplanation": "Cuantila de 95% pentru $n - r = 1$ este aproximativ 9,2 în cazul 2 și 3,8 în cazul 3: valoarea mai mică duce la respingeri prea dese și supraestimează rangul.",
                "incorrectExplanation": "Cazul schimbă distribuția limită; cuantilele cazului 3 sînt cele mai mici, deci eroarea merge în direcția respingerilor excesive."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Reinsel–Ahn",
                "text": "The Reinsel–Ahn correction of the trace statistic in a VAR($p$) with $n$ variables and $T$ observations",
                "options": [
                    "divides the statistic by $(T - np)/T$",
                    "multiplies the statistic by $(T - np)/T$",
                    "adds $np$ to the critical value",
                    "replaces the statistic by its bootstrap mean"
                ],
                "correctExplanation": "Scaling by $(T - np)/T < 1$ shrinks the statistic and reduces the over-rejection in small samples.",
                "incorrectExplanation": "Dividing would increase the over-rejection; the correction acts on the statistic, not by adding to or replacing it."
            },
            "ro": {
                "title": "Corecția Reinsel–Ahn",
                "text": "Corecția Reinsel–Ahn a statisticii trace într-un VAR($p$) cu $n$ variabile și $T$ observații",
                "options": [
                    "împarte statistica la $(T - np)/T$",
                    "înmulțește statistica cu $(T - np)/T$",
                    "adaugă $np$ la valoarea critică",
                    "înlocuiește statistica cu media ei bootstrap"
                ],
                "correctExplanation": "Scalarea cu $(T - np)/T < 1$ micșorează statistica și reduce respingerile excesive în eșantioane mici.",
                "incorrectExplanation": "Împărțirea ar mări respingerile excesive; corecția acționează asupra statisticii, nu prin adunare sau înlocuire."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Bootstrap rank test",
                "text": "In the bootstrap rank test of $H(r)$ (Swensen; Cavaliere, Rahbek and Taylor), the bootstrap samples are generated from",
                "options": [
                    "the VECM estimated under $H(r)$, so that the bootstrap data have exactly $n - r$ unit roots",
                    "the unrestricted VAR in levels, estimated under $H(n)$",
                    "a VAR in first differences in every case",
                    "independent random walks with the variance of the data"
                ],
                "correctExplanation": "Under $H(r)$ the null configuration of unit roots is imposed; this is what makes the sequential bootstrap procedure consistent.",
                "incorrectExplanation": "The unrestricted VAR has no imposed unit roots; a VAR in differences is $H(0)$ only; independent random walks ignore the short-run dynamics."
            },
            "ro": {
                "title": "Testul de rang bootstrap",
                "text": "În testul de rang bootstrap pentru $H(r)$ (Swensen; Cavaliere, Rahbek și Taylor), eșantioanele bootstrap se generează din",
                "options": [
                    "VECM estimat sub $H(r)$, astfel încît datele bootstrap să aibă exact $n - r$ rădăcini unitare",
                    "VAR-ul nerestricționat în niveluri, estimat sub $H(n)$",
                    "un VAR în diferențe, în orice caz",
                    "mersuri aleatoare independente cu varianța datelor"
                ],
                "correctExplanation": "Sub $H(r)$ se impune configurația nulă a rădăcinilor unitare; acest lucru face procedura bootstrap secvențială consistentă.",
                "incorrectExplanation": "VAR-ul nerestricționat nu are rădăcini unitare impuse; VAR-ul în diferențe corespunde doar lui $H(0)$; mersurile aleatoare independente ignoră dinamica pe termen scurt."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Wild bootstrap",
                "text": "Why is the wild bootstrap preferred for monthly interest rates over 2005–2026?",
                "options": [
                    "the wild bootstrap makes the residuals Gaussian",
                    "the i.i.d. bootstrap cannot be used when $n > 2$",
                    "the volatility changes strongly over time (2008–2009, 2022), and the wild bootstrap keeps each date's volatility",
                    "the wild bootstrap removes the need to choose the deterministic case"
                ],
                "correctExplanation": "Multiplying each residual by an independent $N(0,1)$ weight preserves conditional heteroskedasticity, which the i.i.d. bootstrap would average out.",
                "incorrectExplanation": "The wild bootstrap does not make residuals Gaussian, the i.i.d. bootstrap works for any $n$, and the deterministic case must still be chosen."
            },
            "ro": {
                "title": "Bootstrap-ul wild",
                "text": "De ce se preferă bootstrap-ul wild pentru dobînzile lunare din 2005–2026?",
                "options": [
                    "bootstrap-ul wild face reziduurile gaussiene",
                    "bootstrap-ul i.i.d. nu se poate folosi cînd $n > 2$",
                    "volatilitatea se schimbă puternic în timp (2008–2009, 2022), iar bootstrap-ul wild păstrează volatilitatea fiecărei date",
                    "bootstrap-ul wild elimină nevoia de a alege cazul determinist"
                ],
                "correctExplanation": "Înmulțirea fiecărui reziduu cu o pondere $N(0,1)$ independentă păstrează heteroscedasticitatea condiționată, pe care bootstrap-ul i.i.d. ar media-o.",
                "incorrectExplanation": "Bootstrap-ul wild nu face reziduurile gaussiene, bootstrap-ul i.i.d. funcționează pentru orice $n$, iar cazul determinist trebuie ales în continuare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Identification of beta",
                "text": "With rank $r = 3$, how many restrictions beyond the normalisation are needed to just-identify $\\beta$?",
                "options": [
                    "6",
                    "3",
                    "9",
                    "2"
                ],
                "correctExplanation": "Each vector needs $r - 1 = 2$ restrictions besides its normalisation: $r(r - 1) = 6$ in total.",
                "incorrectExplanation": "Three is the number of normalisations; nine is $r^2$; two is the number per vector, not the total."
            },
            "ro": {
                "title": "Identificarea lui beta",
                "text": "Cu rangul $r = 3$, cîte restricții pe lîngă normalizare sînt necesare pentru identificarea exactă a lui $\\beta$?",
                "options": [
                    "6",
                    "3",
                    "9",
                    "2"
                ],
                "correctExplanation": "Fiecare vector are nevoie de $r - 1 = 2$ restricții pe lîngă normalizare: $r(r - 1) = 6$ în total.",
                "incorrectExplanation": "Trei este numărul normalizărilor; nouă este $r^2$; două este numărul pe vector, nu totalul."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Degrees of freedom",
                "text": "In a VECM with $n_1 = 4$ rows of $\\beta$ and $r = 2$, an LR test that both cointegrating vectors are fully known has",
                "options": [
                    "2 degrees of freedom",
                    "8 degrees of freedom",
                    "6 degrees of freedom",
                    "4 degrees of freedom"
                ],
                "correctExplanation": "A fully specified $\\beta$ fixes $r(n_1 - r) = 2 \\cdot 2 = 4$ free parameters of the cointegration space.",
                "incorrectExplanation": "Two would be the count for weak exogeneity of one variable; eight is $n_1 r$ and ignores the normalisation and rotation; six has no justification here."
            },
            "ro": {
                "title": "Grade de libertate",
                "text": "Într-un VECM cu $n_1 = 4$ rînduri ale lui $\\beta$ și $r = 2$, testul LR că ambii vectori de cointegrare sînt complet cunoscuți are",
                "options": [
                    "2 grade de libertate",
                    "8 grade de libertate",
                    "6 grade de libertate",
                    "4 grade de libertate"
                ],
                "correctExplanation": "Un $\\beta$ complet specificat fixează $r(n_1 - r) = 2 \\cdot 2 = 4$ parametri liberi ai spațiului de cointegrare.",
                "incorrectExplanation": "Două ar fi numărul pentru exogenitatea slabă a unei variabile; opt este $n_1 r$ și ignoră normalizarea și rotația; șase nu are justificare aici."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Weak exogeneity",
                "text": "In a cointegrated system, a variable $x_t$ is weakly exogenous for $\\beta$ when",
                "options": [
                    "its column of $\\beta$ is zero",
                    "it is not Granger-caused by any other variable",
                    "its row of $\\alpha$ is zero: it does not adjust to past disequilibria",
                    "it is stationary"
                ],
                "correctExplanation": "A zero row of $\\alpha$ means $\\Delta x_t$ does not react to $\\beta'y_{t-1}$; then the conditional model of the other variables is efficient for $\\beta$.",
                "incorrectExplanation": "A zero entry of $\\beta$ is an exclusion restriction; Granger non-causality is a short-run property (strong exogeneity adds it); a stationary variable is a different issue."
            },
            "ro": {
                "title": "Exogenitatea slabă",
                "text": "Într-un sistem cointegrat, o variabilă $x_t$ este slab exogenă pentru $\\beta$ cînd",
                "options": [
                    "coloana ei din $\\beta$ este zero",
                    "nu este cauzată Granger de nicio altă variabilă",
                    "rîndul ei din $\\alpha$ este zero: nu se ajustează la dezechilibrele trecute",
                    "este staționară"
                ],
                "correctExplanation": "Un rînd zero în $\\alpha$ înseamnă că $\\Delta x_t$ nu reacționează la $\\beta'y_{t-1}$; atunci modelul condiționat al celorlalte variabile este eficient pentru $\\beta$.",
                "incorrectExplanation": "Un zero în $\\beta$ este o restricție de excludere; non-cauzalitatea Granger este o proprietate pe termen scurt (exogenitatea tare o adaugă); o variabilă staționară este o altă problemă."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Granger representation",
                "text": "In the Granger representation $y_t = C\\sum_{s\\le t}\\varepsilon_s + \\dots$, the matrix $C$ satisfies",
                "options": [
                    "$\\alpha'C = 0$ and $C\\beta = 0$",
                    "$C = \\alpha\\beta'$",
                    "$C$ has full rank $n$",
                    "$\\beta'C = 0$ and $C\\alpha = 0$"
                ],
                "correctExplanation": "$C = \\beta_\\perp(\\alpha_\\perp'\\Gamma\\beta_\\perp)^{-1}\\alpha_\\perp'$: the relations contain no stochastic trend and disequilibria have no permanent effect.",
                "incorrectExplanation": "The orthogonality runs through $\\beta'$ on the left and $\\alpha$ on the right; $\\alpha\\beta' = \\Pi$, not $C$; $C$ has rank $n - r$."
            },
            "ro": {
                "title": "Reprezentarea Granger",
                "text": "În reprezentarea Granger $y_t = C\\sum_{s\\le t}\\varepsilon_s + \\dots$, matricea $C$ satisface",
                "options": [
                    "$\\alpha'C = 0$ și $C\\beta = 0$",
                    "$C = \\alpha\\beta'$",
                    "$C$ are rang complet $n$",
                    "$\\beta'C = 0$ și $C\\alpha = 0$"
                ],
                "correctExplanation": "$C = \\beta_\\perp(\\alpha_\\perp'\\Gamma\\beta_\\perp)^{-1}\\alpha_\\perp'$: relațiile nu conțin trend stochastic, iar dezechilibrele nu au efect permanent.",
                "incorrectExplanation": "Ortogonalitatea trece prin $\\beta'$ la stînga și prin $\\alpha$ la dreapta; $\\alpha\\beta' = \\Pi$, nu $C$; $C$ are rangul $n - r$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Permanent shocks",
                "text": "A VECM with $n = 4$ variables and cointegration rank $r = 1$ has",
                "options": [
                    "1 permanent and 3 transitory shocks",
                    "4 permanent shocks and no transitory shock",
                    "3 permanent and 1 transitory shocks, with no further restriction needed",
                    "3 permanent and 1 transitory shocks; 3 additional restrictions identify the permanent shocks among themselves"
                ],
                "correctExplanation": "There are $k = n - r = 3$ common trends; the permanent shocks need $k(k - 1)/2 = 3$ further restrictions (and the transitory one needs $r(r - 1)/2 = 0$).",
                "incorrectExplanation": "The numbers of permanent and transitory shocks are $n - r$ and $r$; with $k > 1$ the permanent shocks are not identified by cointegration alone."
            },
            "ro": {
                "title": "Șocuri permanente",
                "text": "Un VECM cu $n = 4$ variabile și rangul de cointegrare $r = 1$ are",
                "options": [
                    "1 șoc permanent și 3 tranzitorii",
                    "4 șocuri permanente și niciun șoc tranzitoriu",
                    "3 șocuri permanente și 1 tranzitoriu, fără nicio restricție suplimentară",
                    "3 șocuri permanente și 1 tranzitoriu; 3 restricții suplimentare identifică șocurile permanente între ele"
                ],
                "correctExplanation": "Există $k = n - r = 3$ trenduri comune; șocurile permanente cer încă $k(k - 1)/2 = 3$ restricții (iar cel tranzitoriu $r(r - 1)/2 = 0$).",
                "incorrectExplanation": "Numerele de șocuri permanente și tranzitorii sînt $n - r$ și $r$; cu $k > 1$ șocurile permanente nu sînt identificate doar prin cointegrare."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "KPSW",
                "text": "In King, Plosser, Stock and Watson (1991), the cointegrating vectors imposed on (consumption, investment, output) are",
                "options": [
                    "$c - i$ and $c + i - y$",
                    "a single vector $(1, 1, -1)$",
                    "the first differences of the three series",
                    "the great ratios $c - y$ and $i - y$"
                ],
                "correctExplanation": "Balanced growth implies stationary consumption–output and investment–output ratios, leaving one common (productivity) trend.",
                "incorrectExplanation": "The model has two relations, not one; the relations are the great ratios; first differences are not cointegrating vectors."
            },
            "ro": {
                "title": "KPSW",
                "text": "În King, Plosser, Stock și Watson (1991), vectorii de cointegrare impuși pentru (consum, investiții, producție) sînt",
                "options": [
                    "$c - i$ și $c + i - y$",
                    "un singur vector $(1, 1, -1)$",
                    "primele diferențe ale celor trei serii",
                    "raporturile mari $c - y$ și $i - y$"
                ],
                "correctExplanation": "Creșterea echilibrată implică rapoarte staționare consum–producție și investiții–producție, lăsînd un singur trend comun (al productivității).",
                "incorrectExplanation": "Modelul are două relații, nu una; relațiile sînt raporturile mari; primele diferențe nu sînt vectori de cointegrare."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "I(2) condition",
                "text": "The I(1) cointegrated VAR breaks down (I(2) components appear) when",
                "options": [
                    "$\\Pi$ has full rank",
                    "$\\alpha_\\perp'\\Gamma\\beta_\\perp$ has reduced rank",
                    "$\\alpha$ has a zero row",
                    "the deterministic case is 4"
                ],
                "correctExplanation": "Full rank of $\\alpha_\\perp'\\Gamma\\beta_\\perp$ is the condition of the Granger representation theorem; its failure produces I(2) trends.",
                "incorrectExplanation": "A full-rank $\\Pi$ means a stationary VAR; a zero row of $\\alpha$ is weak exogeneity; the deterministic case is unrelated to I(2)."
            },
            "ro": {
                "title": "Condiția I(2)",
                "text": "VAR-ul cointegrat I(1) nu mai este valabil (apar componente I(2)) cînd",
                "options": [
                    "$\\Pi$ are rang complet",
                    "$\\alpha_\\perp'\\Gamma\\beta_\\perp$ are rang redus",
                    "$\\alpha$ are un rînd zero",
                    "cazul determinist este 4"
                ],
                "correctExplanation": "Rangul complet al lui $\\alpha_\\perp'\\Gamma\\beta_\\perp$ este condiția teoremei de reprezentare Granger; încălcarea ei produce trenduri I(2).",
                "incorrectExplanation": "Un $\\Pi$ de rang complet înseamnă un VAR staționar; un rînd zero în $\\alpha$ este exogenitate slabă; cazul determinist nu are legătură cu I(2)."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "ARDL long run",
                "text": "In the conditional ECM $\\Delta y_t = c - 0.25y_{t-1} + 0.20x_{t-1} + 0.1\\Delta x_t + u_t$, the long-run coefficient of $x$ is",
                "options": [
                    "0.20",
                    "0.80",
                    "0.10",
                    "1.25"
                ],
                "correctExplanation": "$\\theta = -\\pi_{yx}/\\pi_{yy} = -0.20/(-0.25) = 0.80$.",
                "incorrectExplanation": "0.20 and 0.10 are short-run coefficients; 1.25 is the inverse ratio."
            },
            "ro": {
                "title": "Termenul lung ARDL",
                "text": "În ECM-ul condiționat $\\Delta y_t = c - 0,25y_{t-1} + 0,20x_{t-1} + 0,1\\Delta x_t + u_t$, coeficientul de termen lung al lui $x$ este",
                "options": [
                    "0,20",
                    "0,80",
                    "0,10",
                    "1,25"
                ],
                "correctExplanation": "$\\theta = -\\pi_{yx}/\\pi_{yy} = -0,20/(-0,25) = 0,80$.",
                "incorrectExplanation": "0,20 și 0,10 sînt coeficienți pe termen scurt; 1,25 este raportul invers."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Bounds decision",
                "text": "The bounds $F$ statistic lies between the 5% I(0) and I(1) bounds. The correct conclusion is",
                "options": [
                    "inconclusive: the decision depends on the integration order of the regressors",
                    "a level relationship exists",
                    "no level relationship exists",
                    "the regressors are I(2)"
                ],
                "correctExplanation": "Between the bounds the test cannot decide without knowing whether the regressors are I(0) or I(1).",
                "incorrectExplanation": "Only $F$ above the upper bound supports a level relationship and only $F$ below the lower bound rejects it; the bounds say nothing about I(2), for which they are invalid."
            },
            "ro": {
                "title": "Decizia bounds",
                "text": "Statistica bounds $F$ se află între limitele I(0) și I(1) de 5%. Concluzia corectă este",
                "options": [
                    "neconcludent: decizia depinde de ordinul de integrare al regresorilor",
                    "există o relație în niveluri",
                    "nu există o relație în niveluri",
                    "regresorii sînt I(2)"
                ],
                "correctExplanation": "Între limite testul nu poate decide fără a ști dacă regresorii sînt I(0) sau I(1).",
                "incorrectExplanation": "Doar un $F$ peste limita superioară susține relația în niveluri și doar un $F$ sub limita inferioară o respinge; limitele nu spun nimic despre I(2), caz în care nu sînt valabile."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Small-sample bounds",
                "text": "With 40 annual observations, using the asymptotic bounds of Pesaran, Shin and Smith (2001) tends to",
                "options": [
                    "under-reject, because small-sample bounds are lower",
                    "be exact, because the bounds do not depend on $T$",
                    "over-reject the null of no level relationship, because small-sample bounds are higher",
                    "be invalid only if the regressors are I(0)"
                ],
                "correctExplanation": "Simulated bounds for small $T$ (Narayan 2005; Kripfganz and Schneider 2020) lie above the asymptotic ones, so the asymptotic table rejects too often.",
                "incorrectExplanation": "The small-sample bounds are higher, not lower, they do depend on $T$, and the problem concerns I(0) and I(1) regressors alike."
            },
            "ro": {
                "title": "Limitele pentru eșantioane mici",
                "text": "Cu 40 de observații anuale, folosirea limitelor asimptotice din Pesaran, Shin și Smith (2001) tinde să",
                "options": [
                    "respingă prea rar, pentru că limitele pentru eșantioane mici sînt mai mici",
                    "fie exactă, pentru că limitele nu depind de $T$",
                    "respingă prea des ipoteza nulă de absență a relației în niveluri, pentru că limitele pentru eșantioane mici sînt mai mari",
                    "fie invalidă doar dacă regresorii sînt I(0)"
                ],
                "correctExplanation": "Limitele simulate pentru $T$ mic (Narayan 2005; Kripfganz și Schneider 2020) sînt peste cele asimptotice, deci tabelul asimptotic respinge prea des.",
                "incorrectExplanation": "Limitele pentru eșantioane mici sînt mai mari, nu mai mici, depind de $T$, iar problema privește în egală măsură regresorii I(0) și I(1)."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "ARDL or VECM",
                "text": "A Johansen test rejects weak exogeneity of the regressor $x_t$ (it adjusts to the equilibrium error). For the long-run coefficient, you should",
                "options": [
                    "use the VECM: the single-equation ARDL is inefficient and can be inconsistent with feedback",
                    "use the ARDL, because it does not require pre-testing",
                    "use the ARDL with case V",
                    "use Toda–Yamamoto, which estimates the long-run coefficient"
                ],
                "correctExplanation": "The conditional ARDL is fully efficient only under weak exogeneity; with feedback from the equilibrium error to $x_t$ the system must be modelled.",
                "incorrectExplanation": "Avoiding pre-tests of integration does not remove the need for weak exogeneity; the deterministic case does not fix feedback; Toda–Yamamoto tests causality and does not estimate long-run coefficients."
            },
            "ro": {
                "title": "ARDL sau VECM",
                "text": "Un test Johansen respinge exogenitatea slabă a regresorului $x_t$ (acesta se ajustează la eroarea de echilibru). Pentru coeficientul de termen lung trebuie să",
                "options": [
                    "folosiți VECM: ARDL pe o singură ecuație este ineficient și poate fi inconsistent în prezența feedback-ului",
                    "folosiți ARDL, pentru că nu cere teste prealabile",
                    "folosiți ARDL cu cazul V",
                    "folosiți Toda–Yamamoto, care estimează coeficientul de termen lung"
                ],
                "correctExplanation": "ARDL condiționat este complet eficient doar sub exogenitate slabă; cu feedback de la eroarea de echilibru la $x_t$ trebuie modelat sistemul.",
                "incorrectExplanation": "Evitarea testelor prealabile de integrare nu elimină nevoia de exogenitate slabă; cazul determinist nu rezolvă feedback-ul; Toda–Yamamoto testează cauzalitatea și nu estimează coeficienți de termen lung."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "CD test",
                "text": "$N = 4$, $T = 25$ and the six pairwise residual correlations sum to 3.0. The Pesaran CD statistic is about",
                "options": [
                    "6.12",
                    "3.00",
                    "1.50",
                    "0.50"
                ],
                "correctExplanation": "$CD = \\sqrt{2T/(N(N-1))}\\sum_{i<j}\\hat\\rho_{ij} = \\sqrt{50/12}\\cdot 3.0 \\approx 6.12$.",
                "incorrectExplanation": "3.00 is the raw sum; 1.50 and 0.50 omit or misplace the scaling factor."
            },
            "ro": {
                "title": "Testul CD",
                "text": "$N = 4$, $T = 25$, iar cele șase corelații ale reziduurilor pe perechi au suma 3,0. Statistica Pesaran CD este aproximativ",
                "options": [
                    "6,12",
                    "3,00",
                    "1,50",
                    "0,50"
                ],
                "correctExplanation": "$CD = \\sqrt{2T/(N(N-1))}\\sum_{i<j}\\hat\\rho_{ij} = \\sqrt{50/12}\\cdot 3,0 \\approx 6,12$.",
                "incorrectExplanation": "3,00 este suma brută; 1,50 și 0,50 omit sau aplică greșit factorul de scalare."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "IPS against CIPS",
                "text": "For EU-27 consumption, IPS rejects a panel unit root while CIPS does not. The most likely explanation is",
                "options": [
                    "CIPS has no power with $N = 27$",
                    "IPS assumes a common autoregressive root across countries",
                    "strong cross-section dependence: common shocks make IPS over-reject, CIPS removes a common factor",
                    "the CD test is positive, so both tests are invalid"
                ],
                "correctExplanation": "IPS treats correlated countries as independent evidence; CIPS augments each regression with cross-section averages to absorb the common factor.",
                "incorrectExplanation": "CIPS is designed for this setting; the common-root assumption belongs to LLC, not IPS; dependence invalidates IPS, not CIPS."
            },
            "ro": {
                "title": "IPS față de CIPS",
                "text": "Pentru consumul din UE-27, IPS respinge rădăcina unitară în panel, iar CIPS nu. Explicația cea mai probabilă este",
                "options": [
                    "CIPS nu are putere cu $N = 27$",
                    "IPS presupune o rădăcină autoregresivă comună tuturor țărilor",
                    "dependența puternică între unități: șocurile comune fac IPS să respingă prea des, iar CIPS elimină un factor comun",
                    "testul CD este pozitiv, deci ambele teste sînt invalide"
                ],
                "correctExplanation": "IPS tratează țările corelate ca dovezi independente; CIPS augmentează fiecare regresie cu mediile pe secțiune pentru a absorbi factorul comun.",
                "incorrectExplanation": "CIPS este conceput pentru această situație; ipoteza rădăcinii comune aparține LLC, nu IPS; dependența invalidează IPS, nu CIPS."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "PMG",
                "text": "The pooled mean group estimator of Pesaran, Shin and Smith (1999) assumes",
                "options": [
                    "common short-run and long-run coefficients for all countries",
                    "country-specific long-run coefficients averaged across countries",
                    "common long-run coefficients and country-specific short-run coefficients, adjustment speeds and variances",
                    "no adjustment towards equilibrium"
                ],
                "correctExplanation": "PMG pools only the long run; MG lets everything differ; dynamic fixed effects pool all slopes.",
                "incorrectExplanation": "Pooling everything is dynamic fixed effects; averaging country long runs is MG; PMG requires negative adjustment speeds."
            },
            "ro": {
                "title": "PMG",
                "text": "Estimatorul pooled mean group al lui Pesaran, Shin și Smith (1999) presupune",
                "options": [
                    "coeficienți comuni pe termen scurt și pe termen lung pentru toate țările",
                    "coeficienți de termen lung specifici țărilor, mediați între țări",
                    "coeficienți comuni pe termen lung și coeficienți pe termen scurt, viteze de ajustare și varianțe specifice fiecărei țări",
                    "absența ajustării spre echilibru"
                ],
                "correctExplanation": "PMG impune doar un termen lung comun; MG lasă totul să difere; efectele fixe dinamice impun toate pantele comune.",
                "incorrectExplanation": "Pantele comune pentru tot înseamnă efecte fixe dinamice; media termenilor lungi pe țări este MG; PMG cere viteze de ajustare negative."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Hausman test",
                "text": "MG gives $\\hat\\theta = 0.85$ (SE 0.10), PMG gives $\\hat\\theta = 0.95$ (SE 0.04). The Hausman statistic is about",
                "options": [
                    "1.19, so long-run homogeneity is not rejected at 5%",
                    "6.25, so long-run homogeneity is rejected",
                    "0.10, the difference of the estimates",
                    "2.50, the difference divided by the PMG standard error"
                ],
                "correctExplanation": "$H = 0.1^2/(0.10^2 - 0.04^2) = 0.01/0.0084 \\approx 1.19 < 3.84$.",
                "incorrectExplanation": "The variance of the difference is $V_{MG} - V_{PMG}$, not $V_{PMG}$ alone; the raw difference is not a test statistic."
            },
            "ro": {
                "title": "Testul Hausman",
                "text": "MG dă $\\hat\\theta = 0,85$ (SE 0,10), PMG dă $\\hat\\theta = 0,95$ (SE 0,04). Statistica Hausman este aproximativ",
                "options": [
                    "1,19, deci omogenitatea termenului lung nu este respinsă la 5%",
                    "6,25, deci omogenitatea termenului lung este respinsă",
                    "0,10, diferența estimațiilor",
                    "2,50, diferența împărțită la eroarea standard PMG"
                ],
                "correctExplanation": "$H = 0,1^2/(0,10^2 - 0,04^2) = 0,01/0,0084 \\approx 1,19 < 3,84$.",
                "incorrectExplanation": "Varianța diferenței este $V_{MG} - V_{PMG}$, nu doar $V_{PMG}$; diferența brută nu este o statistică de test."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the AI error (1)",
                "text": "An AI assistant writes: \"(a) Johansen's trace test has a chi-square limit with $(n-r)^2$ degrees of freedom; (b) given the rank, LR tests on $\\beta$ are chi-square; (c) weak exogeneity is a zero row of $\\alpha$.\" Which statement is wrong?",
                "options": [
                    "(b): tests on $\\beta$ are also non-standard",
                    "(a): the trace limit is a non-standard Brownian functional that depends on $n - r$ and the deterministic case",
                    "(c): weak exogeneity is a zero column of $\\beta$",
                    "none: all three statements are correct"
                ],
                "correctExplanation": "The rank test is a multivariate Dickey–Fuller-type problem; only after the rank is fixed do tests on $\\beta$ and $\\alpha$ become chi-square.",
                "incorrectExplanation": "Given the rank, $\\hat\\beta$ is mixed Gaussian and its LR tests are chi-square; weak exogeneity is indeed a zero row of $\\alpha$."
            },
            "ro": {
                "title": "Găsiți eroarea AI (1)",
                "text": "Un asistent AI scrie: „(a) testul trace Johansen are o limită chi-pătrat cu $(n-r)^2$ grade de libertate; (b) pentru un rang dat, testele LR asupra lui $\\beta$ sînt chi-pătrat; (c) exogenitatea slabă este un rînd zero în $\\alpha$.” Ce afirmație este greșită?",
                "options": [
                    "(b): testele asupra lui $\\beta$ sînt și ele nestandard",
                    "(a): limita testului trace este o funcțională browniană nestandard care depinde de $n - r$ și de cazul determinist",
                    "(c): exogenitatea slabă este o coloană zero în $\\beta$",
                    "niciuna: toate trei afirmațiile sînt corecte"
                ],
                "correctExplanation": "Testul de rang este o problemă de tip Dickey–Fuller multivariat; doar după fixarea rangului testele asupra lui $\\beta$ și $\\alpha$ devin chi-pătrat.",
                "incorrectExplanation": "Pentru un rang dat, $\\hat\\beta$ este mixt gaussian și testele lui LR sînt chi-pătrat; exogenitatea slabă este într-adevăr un rînd zero în $\\alpha$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the AI error (2)",
                "text": "An AI assistant summarises a bounds test: \"F = 5.8 exceeds the 5% I(1) bound 5.71 (case III, k = 1), so with T = 40 annual observations there is a level relationship; the regressor is I(2), which the bounds test allows.\" What is wrong?",
                "options": [
                    "only the claim about I(2); the bounds are correct for any T",
                    "both the use of asymptotic bounds with T = 40 and the claim that I(2) regressors are allowed",
                    "only the bounds; I(2) regressors are allowed",
                    "nothing: the conclusion follows"
                ],
                "correctExplanation": "With T = 40 the 5% upper bound is above 6, so F = 5.8 is inconclusive; and the bounds are derived for I(0) and I(1) regressors only.",
                "incorrectExplanation": "Each of the two claims is wrong on its own: small-sample bounds are higher than 5.71, and I(2) regressors invalidate the bounds."
            },
            "ro": {
                "title": "Găsiți eroarea AI (2)",
                "text": "Un asistent AI rezumă un test bounds: „F = 5,8 depășește limita I(1) de 5% egală cu 5,71 (cazul III, k = 1), deci cu T = 40 de observații anuale există o relație în niveluri; regresorul este I(2), ceea ce testul bounds permite.” Ce este greșit?",
                "options": [
                    "doar afirmația despre I(2); limitele sînt corecte pentru orice T",
                    "atît folosirea limitelor asimptotice cu T = 40, cît și afirmația că regresorii I(2) sînt permiși",
                    "doar limitele; regresorii I(2) sînt permiși",
                    "nimic: concluzia este corectă"
                ],
                "correctExplanation": "Cu T = 40, limita superioară de 5% este peste 6, deci F = 5,8 este neconcludent; iar limitele sînt derivate doar pentru regresori I(0) și I(1).",
                "incorrectExplanation": "Fiecare dintre cele două afirmații este greșită în sine: limitele pentru eșantioane mici sînt mai mari decît 5,71, iar regresorii I(2) invalidează limitele."
            }
        }
    ]
};
