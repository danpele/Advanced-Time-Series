// ============================================================
// Chapter 14 quiz bank: Causal inference for time series (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['causal'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Granger causality and the information set",
                "text": "Two series x and y are both driven by a persistent unobserved factor w, which moves x one period before y; x has no effect on y. What does a bivariate Granger test of x -> y typically conclude in large samples?",
                "options": [
                    "It rejects non-causality: x Granger-causes y, although an intervention on x would not change y",
                    "It does not reject, because x has no causal effect on y",
                    "It rejects only if HAC standard errors are used",
                    "It rejects in both directions with equal frequency, whatever the timing"
                ],
                "correctExplanation": "x carries early information about the common driver, so its lags improve the forecast of y; Granger causality is predictive and relative to the information set.",
                "incorrectExplanation": "The test does not know about interventions: with w omitted, x is informative about y. HAC is not the issue, and the timing makes the x -> y rejection much more frequent."
            },
            "ro": {
                "title": "Cauzalitatea Granger și mulțimea de informație",
                "text": "Două serii x și y sînt influențate de un factor neobservat persistent w, care îl mișcă pe x cu o perioadă înaintea lui y; x nu are niciun efect asupra lui y. Ce conclude de obicei un test Granger bivariat x -> y în eșantioane mari?",
                "options": [
                    "Respinge non-cauzalitatea: x cauzează în sens Granger pe y, deși o intervenție asupra lui x nu l-ar schimba pe y",
                    "Nu respinge, pentru că x nu are niciun efect cauzal asupra lui y",
                    "Respinge doar dacă se folosesc erori standard HAC",
                    "Respinge în ambele direcții cu aceeași frecvență, indiferent de momentul observării"
                ],
                "correctExplanation": "x aduce informație timpurie despre factorul comun, deci lagurile lui îmbunătățesc prognoza lui y; cauzalitatea Granger este predictivă și relativă la mulțimea de informație.",
                "incorrectExplanation": "Testul nu știe nimic despre intervenții: cu w omis, x este informativ despre y. HAC nu este problema, iar momentul observării face respingerea x -> y mult mai frecventă."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Gaussian transfer entropy",
                "text": "In a Gaussian VAR, the residual variance of y_t is 2.0 without the lags of x and 1.5 with them. What is the transfer entropy from x to y?",
                "options": [
                    "ln(2.0/1.5) = 0.288 nats",
                    "0.5 ln(2.0/1.5) = 0.144 nats",
                    "0.5 nats",
                    "2.0 - 1.5 = 0.5 nats"
                ],
                "correctExplanation": "For Gaussian variables the transfer entropy is half the Geweke measure: 0.5 ln(2/1.5) = 0.144 nats (Barnett, Barrett and Seth 2009).",
                "incorrectExplanation": "The log variance ratio itself is the Geweke measure F, twice the transfer entropy; differences of variances are not information measures."
            },
            "ro": {
                "title": "Entropia de transfer gaussiană",
                "text": "Într-un VAR gaussian, varianța reziduală a lui y_t este 2,0 fără lagurile lui x și 1,5 cu ele. Care este entropia de transfer de la x la y?",
                "options": [
                    "ln(2,0/1,5) = 0,288 nats",
                    "0,5 ln(2,0/1,5) = 0,144 nats",
                    "0,5 nats",
                    "2,0 - 1,5 = 0,5 nats"
                ],
                "correctExplanation": "Pentru variabile gaussiene, entropia de transfer este jumătate din măsura Geweke: 0,5 ln(2/1,5) = 0,144 nats (Barnett, Barrett și Seth 2009).",
                "incorrectExplanation": "Logaritmul raportului varianțelor este măsura Geweke F, de două ori entropia de transfer; diferențele de varianțe nu sînt măsuri de informație."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Granger tests across time zones",
                "text": "Daily returns: the S&P 500 Granger-causes the BET (p < 0.001), the DAX does not (p = 0.45), and both indices are strongly correlated with the BET on the same day. What is the best explanation?",
                "options": [
                    "US prices have a causal effect on Romanian firms one day later",
                    "The BET is inefficient and ignores European news",
                    "New York closes after Bucharest: the lagged S&P 500 return carries news that arrives after the Bucharest close",
                    "The HAC correction creates spurious rejections"
                ],
                "correctExplanation": "Timing: the DAX closes together with Bucharest and shows only contemporaneous correlation, while the S&P 500 return of day t-1 contains news released after the Bucharest close of day t-1.",
                "incorrectExplanation": "Nothing in the test identifies an effect on firms; the DAX result shows that European news is priced on the same day; HAC makes the test more conservative, not less."
            },
            "ro": {
                "title": "Teste Granger între fusuri orare",
                "text": "Randamente zilnice: S&P 500 cauzează în sens Granger indicele BET (p < 0,001), DAX nu (p = 0,45), iar ambii indici sînt puternic corelați cu BET în aceeași zi. Care este cea mai bună explicație?",
                "options": [
                    "Prețurile americane au un efect cauzal asupra firmelor românești cu o zi mai tîrziu",
                    "BET este ineficient și ignoră știrile europene",
                    "New York se închide după București: randamentul S&P 500 din ziua anterioară conține știri sosite după închiderea Bucureștiului",
                    "Corecția HAC creează respingeri false"
                ],
                "correctExplanation": "Momentul observării: DAX se închide odată cu Bucureștiul și are doar corelație contemporană, iar randamentul S&P 500 din ziua t-1 conține știri apărute după închiderea Bucureștiului din ziua t-1.",
                "incorrectExplanation": "Nimic din test nu identifică un efect asupra firmelor; rezultatul DAX arată că știrile europene sînt încorporate în aceeași zi; HAC face testul mai conservator, nu mai puțin."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Non-anticipation",
                "text": "In the potential-outcomes framework for time series (Rambachan and Shephard), what does non-anticipation require?",
                "options": [
                    "That the treatment is randomly assigned in every period",
                    "That the outcome is stationary",
                    "That the treatment path is fully observed",
                    "That the outcome at t does not depend on treatments assigned after t"
                ],
                "correctExplanation": "Non-anticipation: Y_t(w_1:T) = Y_t(w_1:t); announced future policies violate it unless the announcement itself is defined as the treatment.",
                "incorrectExplanation": "Random assignment is a separate (and stronger) condition; stationarity and full observation of the path are not part of the definition."
            },
            "ro": {
                "title": "Non-anticiparea",
                "text": "În cadrul rezultatelor potențiale pentru serii de timp (Rambachan și Shephard), ce cere non-anticiparea?",
                "options": [
                    "Ca tratamentul să fie atribuit aleator în fiecare perioadă",
                    "Ca rezultatul să fie staționar",
                    "Ca traiectoria tratamentului să fie observată complet",
                    "Ca rezultatul de la momentul t să nu depindă de tratamentele atribuite după t"
                ],
                "correctExplanation": "Non-anticipare: Y_t(w_1:T) = Y_t(w_1:t); politicile viitoare anunțate o încalcă, dacă anunțul însuși nu este definit ca tratament.",
                "incorrectExplanation": "Atribuirea aleatoare este o condiție separată (și mai tare); staționaritatea și observarea completă a traiectoriei nu fac parte din definiție."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The MCI step of PCMCI",
                "text": "Why does the MCI test of PCMCI condition on the parents of the source variable X^i_{t-tau} as well as on those of the target?",
                "options": [
                    "To remove the autocorrelation of the source, so that false positives stay close to the nominal level",
                    "To increase the number of detected links",
                    "To make the test nonlinear",
                    "To identify contemporaneous links"
                ],
                "correctExplanation": "Conditioning on the source's own past whitens it: the test then behaves as on i.i.d. data and its false positive rate is controlled (Runge et al. 2019).",
                "incorrectExplanation": "The extra conditioning controls false positives rather than increasing detections; the test stays a partial correlation test with lagged links only."
            },
            "ro": {
                "title": "Pasul MCI din PCMCI",
                "text": "De ce condiționează testul MCI din PCMCI și pe părinții variabilei sursă X^i_{t-tau}, nu doar pe cei ai țintei?",
                "options": [
                    "Pentru a elimina autocorelația sursei, astfel încît alarmele false să rămînă aproape de nivelul nominal",
                    "Pentru a crește numărul legăturilor detectate",
                    "Pentru a face testul neliniar",
                    "Pentru a identifica legăturile contemporane"
                ],
                "correctExplanation": "Condiționarea pe trecutul propriu al sursei o „albește”: testul se comportă ca pe date i.i.d., iar rata alarmelor false este controlată (Runge et al. 2019).",
                "incorrectExplanation": "Condiționarea suplimentară controlează alarmele false, nu crește detecțiile; testul rămîne unul de corelație parțială, doar cu legături cu lag."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "PCMCI against the full VAR",
                "text": "In the chapter's simulation, when does PCMCI clearly outperform the full VAR (one regression of each variable on all lags of all variables)?",
                "options": [
                    "Always, because the VAR cannot control false positives",
                    "With many variables relative to the sample size (20 variables, T = 150), where the VAR loses power",
                    "Only when the links are nonlinear",
                    "Only with six variables and T = 500"
                ],
                "correctExplanation": "With 20 variables and three lags the VAR conditions on 60 regressors and its power falls (0.78), while PCMCI keeps small conditioning sets and high power (0.94) at the same false positive rate.",
                "incorrectExplanation": "With six variables and T = 500 the two methods are equivalent; both used partial correlations, so nonlinearity was not the reason."
            },
            "ro": {
                "title": "PCMCI față de VAR complet",
                "text": "În simularea din capitol, cînd este PCMCI clar superior VAR complet (o regresie a fiecărei variabile pe toate lagurile tuturor variabilelor)?",
                "options": [
                    "Întotdeauna, pentru că VAR nu poate controla alarmele false",
                    "Cu multe variabile relativ la dimensiunea eșantionului (20 de variabile, T = 150), unde VAR își pierde puterea",
                    "Doar cînd legăturile sînt neliniare",
                    "Doar cu șase variabile și T = 500"
                ],
                "correctExplanation": "Cu 20 de variabile și trei laguri, VAR condiționează pe 60 de regresori și puterea lui scade (0,78), iar PCMCI păstrează mulțimi de condiționare mici și o putere mare (0,94), cu aceeași rată a alarmelor false.",
                "incorrectExplanation": "Cu șase variabile și T = 500 cele două metode sînt echivalente; ambele au folosit corelații parțiale, deci neliniaritatea nu a fost motivul."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Convergent cross mapping",
                "text": "Two uncoupled logistic maps receive the same strong periodic forcing. What does convergent cross mapping report?",
                "options": [
                    "No causality in either direction, because the maps are uncoupled",
                    "Causality only from the map with the larger growth rate",
                    "High cross-map skill in both directions: spurious bidirectional causality from synchrony",
                    "An error, because CCM requires stochastic data"
                ],
                "correctExplanation": "A shared driver synchronises the maps, so each shadow manifold predicts the other; this is a known failure of CCM (seasonality and synchrony critiques).",
                "incorrectExplanation": "CCM sees only cross-map skill; uncoupled but synchronised systems look coupled. Growth rates do not decide the direction, and CCM is designed for deterministic dynamics."
            },
            "ro": {
                "title": "Convergent cross mapping",
                "text": "Două aplicații logistice necuplate primesc același factor periodic puternic. Ce raportează convergent cross mapping?",
                "options": [
                    "Nicio cauzalitate în nicio direcție, pentru că aplicațiile sînt necuplate",
                    "Cauzalitate doar de la aplicația cu rata de creștere mai mare",
                    "O abilitate mare de estimare încrucișată în ambele direcții: cauzalitate falsă în ambele sensuri, din sincronizare",
                    "O eroare, pentru că CCM cere date stochastice"
                ],
                "correctExplanation": "Un factor comun sincronizează aplicațiile, deci fiecare varietate reconstruită o prezice pe cealaltă; este un eșec cunoscut al CCM (criticile privind sezonalitatea și sincronizarea).",
                "incorrectExplanation": "CCM vede doar abilitatea de estimare încrucișată; sisteme necuplate, dar sincronizate, par cuplate. Ratele de creștere nu decid direcția, iar CCM este conceput pentru dinamici deterministe."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Cumulative effects with dependent errors",
                "text": "An interrupted time series has AR(1) errors with rho = 0.5. Over a long post-period, by what factor are i.i.d. standard errors of the cumulative effect too small?",
                "options": [
                    "1.00",
                    "1.22",
                    "2.00",
                    "about 1.73"
                ],
                "correctExplanation": "The long-run variance is sigma^2/(1 - rho)^2 and the variance is gamma_0 = sigma^2/(1 - rho^2); the ratio of standard deviations is sqrt((1 + rho)/(1 - rho)) = sqrt(3) = 1.73.",
                "incorrectExplanation": "Positive autocorrelation makes the sum vary more than n independent terms; the factor depends on (1 + rho)/(1 - rho), not on rho alone."
            },
            "ro": {
                "title": "Efecte cumulate cu erori dependente",
                "text": "O serie de timp întreruptă are erori AR(1) cu rho = 0,5. Pe o perioadă lungă după intervenție, cu ce factor sînt prea mici erorile standard i.i.d. ale efectului cumulat?",
                "options": [
                    "1,00",
                    "1,22",
                    "2,00",
                    "aproximativ 1,73"
                ],
                "correctExplanation": "Varianța pe termen lung este sigma^2/(1 - rho)^2, iar varianța este gamma_0 = sigma^2/(1 - rho^2); raportul abaterilor standard este sqrt((1 + rho)/(1 - rho)) = sqrt(3) = 1,73.",
                "incorrectExplanation": "Autocorelația pozitivă face ca suma să varieze mai mult decît n termeni independenți; factorul depinde de (1 + rho)/(1 - rho), nu doar de rho."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "A placebo date in an ITS",
                "text": "The ITS of Romanian monthly inflation, rerun with a fictitious intervention in July 2024, gives z = 2.0 with i.i.d. errors and z = 1.6 with HAC. What does this show?",
                "options": [
                    "i.i.d. inference can declare effects at dates when nothing happened; HAC inference is needed and the single-series counterfactual is fragile",
                    "There was a real policy shock in July 2024",
                    "HAC standard errors are biased downwards",
                    "The July 2025 effect must be spurious too"
                ],
                "correctExplanation": "A placebo should give no effect; with i.i.d. errors it looks significant, with HAC it does not. The true July 2025 effect stays significant with HAC (z = 3.0).",
                "incorrectExplanation": "Nothing happened in July 2024; HAC errors are larger, not smaller; the placebo does not invalidate an effect that remains significant under HAC."
            },
            "ro": {
                "title": "O dată placebo într-o ITS",
                "text": "ITS pentru inflația lunară a României, rulată din nou cu o intervenție fictivă în iulie 2024, dă z = 2,0 cu erori i.i.d. și z = 1,6 cu HAC. Ce arată acest lucru?",
                "options": [
                    "Inferența i.i.d. poate declara efecte la date la care nu s-a întîmplat nimic; inferența HAC este necesară, iar contrafactualul dintr-o singură serie este fragil",
                    "A existat un șoc real de politică în iulie 2024",
                    "Erorile standard HAC sînt deplasate în jos",
                    "Efectul din iulie 2025 trebuie să fie și el fals"
                ],
                "correctExplanation": "Un placebo nu ar trebui să dea niciun efect; cu erori i.i.d. pare semnificativ, cu HAC nu. Efectul real din iulie 2025 rămîne semnificativ cu HAC (z = 3,0).",
                "incorrectExplanation": "În iulie 2024 nu s-a întîmplat nimic; erorile HAC sînt mai mari, nu mai mici; placebo nu invalidează un efect care rămîne semnificativ cu HAC."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Event studies and anticipation",
                "text": "The BET shows no abnormal return on the day the Romanian government assumed responsibility for the 2025 fiscal package. What is the right conclusion?",
                "options": [
                    "The fiscal package had no economic effect",
                    "The event was not a surprise on day 0: the measures had been discussed for weeks, so the market priced them earlier",
                    "The market model is misspecified",
                    "Event studies cannot be used for fiscal news"
                ],
                "correctExplanation": "An event study measures the reaction to news; anticipated measures are priced before the window, so a null result says nothing about the economic effect.",
                "incorrectExplanation": "The test does not measure economic effects, only the surprise; the market model can be fine; event studies work for fiscal news when the timing of the surprise is known."
            },
            "ro": {
                "title": "Studii de eveniment și anticipare",
                "text": "Indicele BET nu are randament anormal în ziua în care guvernul României și-a asumat răspunderea pentru pachetul fiscal din 2025. Care este concluzia corectă?",
                "options": [
                    "Pachetul fiscal nu a avut niciun efect economic",
                    "Evenimentul nu a fost o surpriză în ziua 0: măsurile fuseseră discutate săptămîni întregi, deci piața le încorporase mai devreme",
                    "Modelul de piață este greșit specificat",
                    "Studiile de eveniment nu pot fi folosite pentru știri fiscale"
                ],
                "correctExplanation": "Un studiu de eveniment măsoară reacția la știri; măsurile anticipate sînt încorporate înaintea ferestrei, deci un rezultat nul nu spune nimic despre efectul economic.",
                "incorrectExplanation": "Testul nu măsoară efecte economice, ci doar surpriza; modelul de piață poate fi corect; studiile de eveniment funcționează pentru știri fiscale cînd momentul surprizei este cunoscut."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The convex hull",
                "text": "Before July 2025 Romania had the highest inflation in the EU. What happens to a classic synthetic control (weights non-negative, summing to one, no intercept)?",
                "options": [
                    "It fits perfectly, because there are 26 donors",
                    "It puts equal weight on all donors",
                    "It cannot reproduce Romania's level: the pre-fit is poor and the effect is overstated",
                    "It becomes identical to difference in differences"
                ],
                "correctExplanation": "Outside the convex hull no convex combination matches the level; in the chapter the classic SC puts all weight on Croatia and Hungary, with a pre-period RMSPE of 1.45 against 0.23 for the demeaned SC.",
                "incorrectExplanation": "The number of donors does not help when all lie below the treated unit; the weights concentrate on the closest donors, and DiD would need equal weights and an intercept."
            },
            "ro": {
                "title": "Înfășurătoarea convexă",
                "text": "Înainte de iulie 2025, România avea cea mai mare inflație din UE. Ce se întîmplă cu un control sintetic clasic (ponderi nenegative, cu suma unu, fără termen liber)?",
                "options": [
                    "Se potrivește perfect, pentru că există 26 de donatori",
                    "Pune ponderi egale pe toți donatorii",
                    "Nu poate reproduce nivelul României: potrivirea anterioară este slabă, iar efectul este supraestimat",
                    "Devine identic cu diferența în diferențe"
                ],
                "correctExplanation": "În afara înfășurătorii convexe nicio combinație convexă nu reproduce nivelul; în capitol, SC clasic pune toată ponderea pe Croația și Ungaria, cu RMSPE anterior 1,45 față de 0,23 pentru SC cu termen liber.",
                "incorrectExplanation": "Numărul donatorilor nu ajută cînd toți se află sub unitatea tratată; ponderile se concentrează pe cei mai apropiați donatori, iar DiD ar cere ponderi egale și un termen liber."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Placebo inference",
                "text": "A synthetic control study has one treated unit and 26 donors. The treated unit has the largest post/pre RMSPE ratio. What is the permutation p-value?",
                "options": [
                    "0.01",
                    "0.05",
                    "1/26 = 0.038",
                    "1/27 = 0.037"
                ],
                "correctExplanation": "There are 27 units in the permutation distribution; the treated unit ranks first, so p = 1/27, also the smallest attainable value.",
                "incorrectExplanation": "The p-value counts the treated unit itself: the denominator is J + 1 = 27; values such as 0.01 are impossible with 27 units."
            },
            "ro": {
                "title": "Inferența prin placebo",
                "text": "Un studiu cu control sintetic are o unitate tratată și 26 de donatori. Unitatea tratată are cel mai mare raport RMSPE după/înainte. Care este p-value-ul prin permutare?",
                "options": [
                    "0,01",
                    "0,05",
                    "1/26 = 0,038",
                    "1/27 = 0,037"
                ],
                "correctExplanation": "Distribuția de permutare are 27 de unități; unitatea tratată este pe primul loc, deci p = 1/27, care este și cea mai mică valoare posibilă.",
                "incorrectExplanation": "P-value-ul include unitatea tratată: numitorul este J + 1 = 27; valori ca 0,01 sînt imposibile cu 27 de unități."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Replicating German reunification",
                "text": "With the public data of Abadie, Diamond and Hainmueller (2015), which result is reproduced in the chapter?",
                "options": [
                    "The weights Austria 0.42, USA 0.22, Japan 0.16, Switzerland 0.11, Netherlands 0.09 and an average gap of about 1,600 USD per capita a year",
                    "A positive effect of reunification on West German GDP",
                    "Equal weights on all 16 OECD donors",
                    "A significant effect at the 1% level by the permutation test"
                ],
                "correctExplanation": "The cross-validated V and the quadratic programme give the published Table 1 weights to two decimals and the average 1990-2003 gap of about 1,600 USD.",
                "incorrectExplanation": "The gap is negative; the weights are sparse; with 17 units the permutation p-value cannot be below 1/17 = 0.059."
            },
            "ro": {
                "title": "Replicarea reunificării Germaniei",
                "text": "Cu datele publice ale lui Abadie, Diamond și Hainmueller (2015), ce rezultat este reprodus în capitol?",
                "options": [
                    "Ponderile Austria 0,42; SUA 0,22; Japonia 0,16; Elveția 0,11; Țările de Jos 0,09 și o diferență medie de aproximativ 1600 USD pe locuitor pe an",
                    "Un efect pozitiv al reunificării asupra PIB-ului Germaniei de Vest",
                    "Ponderi egale pe toți cei 16 donatori OCDE",
                    "Un efect semnificativ la nivelul de 1% după testul de permutare"
                ],
                "correctExplanation": "V ales prin validare încrucișată și programarea pătratică dau ponderile publicate în tabelul 1 cu două zecimale și diferența medie 1990--2003 de aproximativ 1600 USD.",
                "incorrectExplanation": "Diferența este negativă; ponderile sînt rare; cu 17 unități, p-value-ul prin permutare nu poate fi sub 1/17 = 0,059."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The Brexit replication",
                "text": "Re-estimating the Brexit doppelganger of Born et al. (2019) on today's OECD data, GDP path only, gives a 2018Q4 gap of about -1.5% and a UK rank of 11 of 24 in the country placebos. What is the right reading?",
                "options": [
                    "Brexit had no effect on UK output",
                    "The published result is sensitive to data revisions and specification; on revised data the placebo evidence is weak",
                    "The original paper made a coding error",
                    "Synthetic control cannot be used for countries"
                ],
                "correctExplanation": "A replication changes the data vintage and drops the covariates; the sign remains but the size and significance weaken. Each deviation must be reported separately.",
                "incorrectExplanation": "Weak evidence is not evidence of no effect; nothing points to a coding error; the method is designed exactly for one treated country."
            },
            "ro": {
                "title": "Replicarea Brexit",
                "text": "Reestimarea dublurii Brexit a lui Born et al. (2019) pe datele OCDE de azi, doar pe traiectoria PIB, dă o diferență de aproximativ -1,5% în 2018T4 și locul 11 din 24 pentru Regatul Unit în testele placebo pe țări. Care este interpretarea corectă?",
                "options": [
                    "Brexit nu a avut niciun efect asupra producției Regatului Unit",
                    "Rezultatul publicat este sensibil la revizuirea datelor și la specificație; pe datele revizuite dovezile placebo sînt slabe",
                    "Lucrarea originală conține o eroare de cod",
                    "Controlul sintetic nu poate fi folosit pentru țări"
                ],
                "correctExplanation": "O replicare schimbă ediția datelor și renunță la covariate; semnul rămîne, dar mărimea și semnificația slăbesc. Fiecare abatere trebuie raportată separat.",
                "incorrectExplanation": "Dovezile slabe nu sînt dovada lipsei efectului; nimic nu indică o eroare de cod; metoda este concepută exact pentru o singură țară tratată."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Augmented synthetic control",
                "text": "What does the ridge-augmented synthetic control of Ben-Michael, Feller and Rothstein (2021) add to the classic estimator?",
                "options": [
                    "A ridge penalty that makes all weights equal",
                    "Time weights on the pre-periods",
                    "A correction for the remaining pre-period imbalance through a ridge outcome model, which may give negative weights",
                    "An exact permutation test"
                ],
                "correctExplanation": "The augmented estimate adds (X_1 - X_0 w)' eta_hat, with eta_hat from a ridge regression across donors; the implied weights can be negative (controlled extrapolation).",
                "incorrectExplanation": "Equal weights are DiD; time weights belong to synthetic DiD; the augmentation concerns estimation, not inference."
            },
            "ro": {
                "title": "Controlul sintetic augmentat",
                "text": "Ce adaugă controlul sintetic augmentat ridge al lui Ben-Michael, Feller și Rothstein (2021) estimatorului clasic?",
                "options": [
                    "O penalizare ridge care face toate ponderile egale",
                    "Ponderi ale perioadelor anterioare",
                    "O corecție a dezechilibrului rămas în perioada anterioară printr-un model ridge al rezultatului, care poate da ponderi negative",
                    "Un test exact de permutare"
                ],
                "correctExplanation": "Estimația augmentată adaugă (X_1 - X_0 w)' eta_hat, cu eta_hat dintr-o regresie ridge între donatori; ponderile implicite pot fi negative (extrapolare controlată).",
                "incorrectExplanation": "Ponderile egale corespund DiD; ponderile perioadelor aparțin DiD sintetic; augmentarea privește estimarea, nu inferența."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Synthetic DiD",
                "text": "How does synthetic difference in differences (Arkhangelsky et al. 2021) relate to DiD and synthetic control?",
                "options": [
                    "It is DiD with a different standard error",
                    "It is SC applied to first differences",
                    "It replaces unit fixed effects by covariates",
                    "It weights both units and pre-periods and keeps unit and time fixed effects"
                ],
                "correctExplanation": "DiD uses uniform unit and time weights; SC uses unit weights without unit fixed effects; SDID combines regularised unit weights, time weights and two-way fixed effects.",
                "incorrectExplanation": "The weights, not only the standard errors, differ from DiD; it is not SC on differences, and it does not need covariates."
            },
            "ro": {
                "title": "DiD sintetic",
                "text": "Cum se raportează diferența în diferențe sintetică (Arkhangelsky et al. 2021) la DiD și la controlul sintetic?",
                "options": [
                    "Este DiD cu o altă eroare standard",
                    "Este SC aplicat diferențelor de ordinul întîi",
                    "Înlocuiește efectele fixe ale unităților cu covariate",
                    "Ponderează atît unitățile, cît și perioadele anterioare și păstrează efectele fixe ale unităților și perioadelor"
                ],
                "correctExplanation": "DiD folosește ponderi uniforme ale unităților și perioadelor; SC folosește ponderi ale unităților fără efecte fixe ale unităților; SDID combină ponderi regularizate ale unităților, ponderi ale perioadelor și efecte fixe bidirecționale.",
                "incorrectExplanation": "Ponderile, nu doar erorile standard, diferă de DiD; nu este SC pe diferențe și nu are nevoie de covariate."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The tax component of Romanian inflation",
                "text": "Eurostat's HICP at constant tax rates assumes full and immediate pass-through of tax changes. In the chapter the 12-month gap of total HICP inflation is 2.70 pp and the gap of constant-tax inflation is 0.40 pp. What does the difference measure?",
                "options": [
                    "The mechanical tax contribution (mainly the VAT increase), about 72% of the total effect, under the full pass-through assumption",
                    "The effect of the end of the electricity price cap",
                    "The measurement error of the HICP",
                    "The second-round effects of the VAT increase"
                ],
                "correctExplanation": "The constant-tax index removes tax changes as if passed through fully; the wedge isolates the mechanical tax part, while the non-tax part (0.40 pp) peaks in July 2025 with the electricity cap.",
                "incorrectExplanation": "The electricity cap is a price, not a tax, so it appears in the constant-tax gap; second-round effects are part of the non-tax gap, not of the tax wedge."
            },
            "ro": {
                "title": "Componenta fiscală a inflației României",
                "text": "IAPC la cote de taxare constante al Eurostat presupune transmiterea completă și imediată a modificărilor fiscale. În capitol, diferența pe 12 luni a inflației IAPC totale este 2,70 pp, iar cea a inflației la taxe constante 0,40 pp. Ce măsoară diferența?",
                "options": [
                    "Contribuția fiscală mecanică (în principal majorarea TVA), aproximativ 72% din efectul total, sub ipoteza transmiterii complete",
                    "Efectul încheierii plafonării prețului electricității",
                    "Eroarea de măsurare a IAPC",
                    "Efectele de runda a doua ale majorării TVA"
                ],
                "correctExplanation": "Indicele la taxe constante elimină modificările fiscale ca și cum ar fi transmise complet; diferența izolează partea fiscală mecanică, iar partea nefiscală (0,40 pp) are maximul în iulie 2025, odată cu plafonarea electricității.",
                "incorrectExplanation": "Plafonarea electricității este un preț, nu o taxă, deci apare în diferența la taxe constante; efectele de runda a doua fac parte din diferența nefiscală, nu din componenta fiscală."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "A built-in falsification",
                "text": "The outcome of the Romanian synthetic control is annual inflation, 100(ln P_t - ln P_{t-12}). What should happen to the gap in August 2026 if the measures were one-off price-level shocks?",
                "options": [
                    "It should double",
                    "It should close, because the August 2025 price jump leaves the 12-month window",
                    "It should become negative by the same amount",
                    "Nothing: annual rates keep a price-level shock forever"
                ],
                "correctExplanation": "A one-off level shift raises the annual rate for exactly twelve months; in August 2026 the demeaned SC gap falls to 0.22 pp and SDID to 0.26 pp, as predicted.",
                "incorrectExplanation": "Annual rates difference out level shifts after twelve months; a negative gap would require a fall in the price level, which did not happen."
            },
            "ro": {
                "title": "O falsificare încorporată",
                "text": "Rezultatul controlului sintetic pentru România este inflația anuală, 100(ln P_t - ln P_{t-12}). Ce ar trebui să se întîmple cu diferența în august 2026 dacă măsurile au fost șocuri unice ale nivelului prețurilor?",
                "options": [
                    "Ar trebui să se dubleze",
                    "Ar trebui să dispară, pentru că saltul prețurilor din august 2025 iese din fereastra de 12 luni",
                    "Ar trebui să devină negativă cu aceeași valoare",
                    "Nimic: ratele anuale păstrează pentru totdeauna un șoc al nivelului prețurilor"
                ],
                "correctExplanation": "O deplasare unică a nivelului crește rata anuală exact douăsprezece luni; în august 2026, diferența SC cu termen liber scade la 0,22 pp, iar SDID la 0,26 pp, așa cum se prevedea.",
                "incorrectExplanation": "Ratele anuale elimină deplasările de nivel după douăsprezece luni; o diferență negativă ar cere o scădere a nivelului prețurilor, care nu a avut loc."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Staggered adoption",
                "text": "Units adopt a policy at different dates and the effect grows with exposure. Why can a static two-way fixed effects estimate be far below the average effect on the treated?",
                "options": [
                    "Because the panel is unbalanced",
                    "Because the standard errors are clustered",
                    "Because it includes forbidden comparisons that use already-treated units, whose effect is still growing, as controls",
                    "Because the never-treated group is too small"
                ],
                "correctExplanation": "Goodman-Bacon (2021): TWFE averages all 2x2 DiDs; comparisons with already-treated controls subtract part of the effect (in the chapter 0.55 against a true 1.99; Callaway-Sant'Anna gives 2.04).",
                "incorrectExplanation": "The simulated panel is balanced and the issue is the point estimate, not its standard error; the never-treated group is not the source of the bias."
            },
            "ro": {
                "title": "Adoptarea eșalonată",
                "text": "Unitățile adoptă o politică la date diferite, iar efectul crește cu expunerea. De ce poate o estimație TWFE statică să fie mult sub efectul mediu asupra unităților tratate?",
                "options": [
                    "Pentru că panelul este neechilibrat",
                    "Pentru că erorile standard sînt grupate",
                    "Pentru că include comparații interzise, care folosesc drept control unități deja tratate, al căror efect încă crește",
                    "Pentru că grupul niciodată tratat este prea mic"
                ],
                "correctExplanation": "Goodman-Bacon (2021): TWFE mediază toate DiD 2x2; comparațiile cu controale deja tratate scad o parte din efect (în capitol 0,55 față de 1,99 real; Callaway-Sant'Anna dă 2,04).",
                "incorrectExplanation": "Panelul simulat este echilibrat, iar problema este estimația punctuală, nu eroarea ei standard; grupul niciodată tratat nu este sursa deplasării."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "CausalImpact assumptions",
                "text": "In a CausalImpact analysis of the Bitcoin ETF approval, Ether volatility is added as a control. What is the main risk?",
                "options": [
                    "Ether volatility is not stationary",
                    "The model gets too many parameters",
                    "The posterior intervals become too wide",
                    "Ether may itself respond to the approval: a treated control biases the effect towards zero"
                ],
                "correctExplanation": "CausalImpact requires controls unaffected by the treatment; Ether reacts to crypto-wide news (a peer-reviewed study found lower Ether volatility after the approval), so it absorbs part of the effect.",
                "incorrectExplanation": "Stationarity and parameter count are secondary; wider intervals are a symptom of noise, while a treated control creates bias."
            },
            "ro": {
                "title": "Ipotezele CausalImpact",
                "text": "Într-o analiză CausalImpact a aprobării ETF-urilor Bitcoin, volatilitatea Ether este adăugată ca serie de control. Care este riscul principal?",
                "options": [
                    "Volatilitatea Ether nu este staționară",
                    "Modelul capătă prea mulți parametri",
                    "Intervalele a posteriori devin prea largi",
                    "Ether poate răspunde el însuși la aprobare: un control tratat deplasează efectul spre zero"
                ],
                "correctExplanation": "CausalImpact cere serii de control neafectate de tratament; Ether reacționează la știrile din întreaga piață cripto (un studiu publicat a găsit o volatilitate mai mică a Ether după aprobare), deci absoarbe o parte din efect.",
                "incorrectExplanation": "Staționaritatea și numărul de parametri sînt secundare; intervalele mai largi sînt un simptom al zgomotului, în timp ce un control tratat creează deplasare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Detectable effects",
                "text": "A local level counterfactual for weekly log realised variance has sigma^2_eps = 0.94, sigma^2_eta = 0.01, P = 0.02 and 25 post weeks. The 95% half-width of the average effect is about 0.75. What follows?",
                "options": [
                    "Effects on log variance smaller than about 0.75 cannot be detected with this design, so a null result is not evidence of no effect",
                    "The ETF approval had no effect on Bitcoin volatility",
                    "The model should use daily data to remove noise",
                    "Any effect larger than 0.1 will be detected"
                ],
                "correctExplanation": "The interval width sets the minimal detectable effect; with this noise the analysis can only rule out large changes.",
                "incorrectExplanation": "Absence of evidence is not evidence of absence; daily data change the noise structure but do not guarantee more power; 0.1 is far inside the interval."
            },
            "ro": {
                "title": "Efecte detectabile",
                "text": "Un contrafactual cu nivel local pentru logaritmul varianței realizate săptămînale are sigma^2_eps = 0,94, sigma^2_eta = 0,01, P = 0,02 și 25 de săptămîni după. Jumătatea lățimii intervalului de 95% al efectului mediu este aproximativ 0,75. Ce rezultă?",
                "options": [
                    "Efectele asupra logaritmului varianței mai mici de aproximativ 0,75 nu pot fi detectate cu acest design, deci un rezultat nul nu dovedește lipsa efectului",
                    "Aprobarea ETF nu a avut niciun efect asupra volatilității Bitcoin",
                    "Modelul ar trebui să folosească date zilnice pentru a elimina zgomotul",
                    "Orice efect mai mare de 0,1 va fi detectat"
                ],
                "correctExplanation": "Lățimea intervalului fixează efectul minim detectabil; cu acest zgomot analiza poate exclude doar schimbări mari.",
                "incorrectExplanation": "Lipsa dovezilor nu este dovada lipsei; datele zilnice schimbă structura zgomotului, dar nu garantează mai multă putere; 0,1 se află mult în interiorul intervalului."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Double machine learning",
                "text": "What does double/debiased machine learning NOT provide in a time-series policy evaluation?",
                "options": [
                    "Robustness of theta to first-order errors in the nuisance functions",
                    "Identification: if the treatment is confounded by unobservables, DML is still biased",
                    "Valid standard errors when the cross-fitting uses contiguous blocks and HAC",
                    "Flexible adjustment for nonlinear confounding by observed covariates"
                ],
                "correctExplanation": "DML removes regularisation and overfitting bias through orthogonal scores and cross-fitting; it assumes the treatment is unconfounded given X.",
                "incorrectExplanation": "Orthogonality, blocked cross-fitting with HAC and flexible adjustment are exactly what DML provides; identification must come from the design."
            },
            "ro": {
                "title": "Double machine learning",
                "text": "Ce NU oferă double/debiased machine learning într-o evaluare de politică pe serii de timp?",
                "options": [
                    "Robustețea lui theta la erorile de ordinul întîi din funcțiile auxiliare",
                    "Identificarea: dacă tratamentul este confundat de factori neobservați, DML rămîne deplasat",
                    "Erori standard valide cînd cross-fitting-ul folosește blocuri contigue și HAC",
                    "Ajustarea flexibilă pentru confuzia neliniară produsă de covariatele observate"
                ],
                "correctExplanation": "DML elimină deplasarea din regularizare și supraajustare prin scoruri ortogonale și cross-fitting; presupune că tratamentul este neconfundat, dat X.",
                "incorrectExplanation": "Ortogonalitatea, cross-fitting-ul pe blocuri cu HAC și ajustarea flexibilă sînt exact ce oferă DML; identificarea trebuie să vină din design."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in an AI answer (1)",
                "text": "An AI assistant wrote: \"With 23 donors, our synthetic control placebo test gives p = 0.01, so the effect is significant at the 1% level.\" What is wrong?",
                "options": [
                    "Nothing; placebo tests can reach any p-value",
                    "Placebo tests give confidence intervals, not p-values",
                    "With 23 donors the smallest attainable permutation p-value is 1/24 = 0.042",
                    "The p-value should be multiplied by the number of donors"
                ],
                "correctExplanation": "The permutation distribution has J + 1 = 24 values; the treated unit ranking first gives p = 1/24, so p = 0.01 is impossible.",
                "incorrectExplanation": "Permutation p-values are discrete with step 1/(J + 1); they are p-values, not intervals; no Bonferroni-type multiplication applies."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI (1)",
                "text": "Un asistent AI a scris: „Cu 23 de donatori, testul placebo al controlului sintetic dă p = 0,01, deci efectul este semnificativ la nivelul de 1%.” Ce este greșit?",
                "options": [
                    "Nimic; testele placebo pot da orice p-value",
                    "Testele placebo dau intervale de încredere, nu p-value-uri",
                    "Cu 23 de donatori, cel mai mic p-value posibil prin permutare este 1/24 = 0,042",
                    "P-value-ul ar trebui înmulțit cu numărul donatorilor"
                ],
                "correctExplanation": "Distribuția de permutare are J + 1 = 24 de valori; unitatea tratată pe primul loc dă p = 1/24, deci p = 0,01 este imposibil.",
                "incorrectExplanation": "P-value-urile prin permutare sînt discrete, cu pasul 1/(J + 1); sînt p-value-uri, nu intervale; nu se aplică nicio înmulțire de tip Bonferroni."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in an AI answer (2)",
                "text": "An AI assistant wrote: \"Our synthetic control has an almost perfect fit over the 6 pre-treatment months, which proves that it is unbiased.\" What is wrong?",
                "options": [
                    "Nothing; a perfect fit removes the bias",
                    "Synthetic controls never fit perfectly",
                    "The fit should be checked after the treatment, not before",
                    "With a short pre-period a perfect fit can be overfitting noise; the bias bound needs a long pre-period relative to the number of donors"
                ],
                "correctExplanation": "Abadie, Diamond and Hainmueller (2010) bound the bias by a term that shrinks only when T0 is large relative to J and the noise; six months with many donors can fit noise.",
                "incorrectExplanation": "A good fit is necessary but not sufficient; perfect fits are common with many donors and short windows; the post-period gap is the effect, not a fit check."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI (2)",
                "text": "Un asistent AI a scris: „Controlul nostru sintetic are o potrivire aproape perfectă pe cele 6 luni anterioare tratamentului, ceea ce dovedește că este nedeplasat.” Ce este greșit?",
                "options": [
                    "Nimic; o potrivire perfectă elimină deplasarea",
                    "Controalele sintetice nu se potrivesc niciodată perfect",
                    "Potrivirea ar trebui verificată după tratament, nu înainte",
                    "Cu o perioadă anterioară scurtă, o potrivire perfectă poate fi supraajustarea zgomotului; marginea deplasării cere o perioadă anterioară lungă relativ la numărul donatorilor"
                ],
                "correctExplanation": "Abadie, Diamond și Hainmueller (2010) mărginesc deplasarea printr-un termen care scade doar cînd T0 este mare relativ la J și la zgomot; șase luni cu mulți donatori pot reproduce zgomotul.",
                "incorrectExplanation": "O potrivire bună este necesară, dar nu suficientă; potrivirile perfecte sînt frecvente cu mulți donatori și ferestre scurte; diferența de după tratament este efectul, nu o verificare a potrivirii."
            }
        }
    ]
};
