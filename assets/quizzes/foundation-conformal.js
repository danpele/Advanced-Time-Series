// ============================================================
// Chapter 13 quiz bank: Foundation models and conformal prediction (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['foundation-conformal'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 2,
            "en": {
                "title": "The range of the Chronos vocabulary",
                "text": "Chronos scales a context by $s = \\frac1C\\sum_{t \\le C}|y_t|$ and maps $y_t/s$ to uniform bins on $[-15, 15]$. The context has mean absolute value 40. Which future value can the model not forecast?",
                "options": [
                    "Any value below 40",
                    "Any negative value",
                    "Any value above 600",
                    "Any value that did not occur in the context"
                ],
                "correctExplanation": "The largest representable value is $15s = 15 \\cdot 40 = 600$; larger values fall in the last bin.",
                "incorrectExplanation": "The bins cover $[-15s, 15s]$, including negative values and values never observed; only values beyond $15s = 600$ are clipped."
            },
            "ro": {
                "title": "Domeniul vocabularului Chronos",
                "text": "Chronos scalează un context prin $s = \\frac1C\\sum_{t \\le C}|y_t|$ și asociază lui $y_t/s$ intervale egale pe $[-15, 15]$. Contextul are media valorilor absolute 40. Ce valoare viitoare nu poate fi prognozată de model?",
                "options": [
                    "Orice valoare sub 40",
                    "Orice valoare negativă",
                    "Orice valoare peste 600",
                    "Orice valoare care nu a apărut în context"
                ],
                "correctExplanation": "Cea mai mare valoare reprezentabilă este $15s = 15 \\cdot 40 = 600$; valorile mai mari cad în ultimul interval.",
                "incorrectExplanation": "Intervalele acoperă $[-15s, 15s]$, inclusiv valori negative și valori neobservate; doar valorile peste $15s = 600$ sînt tăiate."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "A VaR 1% from Chronos-Bolt",
                "text": "Chronos-Bolt is trained on the quantile levels 0.1, 0.2, ..., 0.9. A risk manager needs a VaR 1% of daily returns from it. What is the correct approach?",
                "options": [
                    "Calibrate a shift of its 10% quantile so that the past exceedance rate is 1% (a one-sided conformal step)",
                    "Request the 0.01 quantile: the model extrapolates its quantile function",
                    "Take the 10% quantile and divide it by 10",
                    "Use the median minus three times the interquartile range"
                ],
                "correctExplanation": "The model cannot output levels outside 0.1-0.9 (requests are clipped); a conformal threshold on the score $\\hat q_{0.1} - y$ at level 0.01 gives the right exceedance rate.",
                "incorrectExplanation": "A request for 0.01 is silently clipped to 0.1; scaling a quantile or using the interquartile range assumes a distribution that nobody checked."
            },
            "ro": {
                "title": "Un VaR 1% din Chronos-Bolt",
                "text": "Chronos-Bolt este antrenat pe nivelurile de cuantilă 0,1; 0,2; ...; 0,9. Un manager de risc are nevoie de un VaR 1% al randamentelor zilnice pe baza lui. Care este abordarea corectă?",
                "options": [
                    "Calibrarea unei deplasări a cuantilei de 10%, astfel încît rata depășirilor trecute să fie 1% (un pas conformal unilateral)",
                    "Cererea cuantilei de 0,01: modelul își extrapolează funcția cuantilă",
                    "Cuantila de 10% împărțită la 10",
                    "Mediana minus de trei ori abaterea intercuartilică"
                ],
                "correctExplanation": "Modelul nu poate produce niveluri în afara intervalului 0,1-0,9 (cererile sînt tăiate); un prag conformal pe scorul $\\hat q_{0,1} - y$ la nivelul 0,01 dă rata corectă de depășire.",
                "incorrectExplanation": "O cerere pentru 0,01 este tăiată fără avertisment la 0,1; scalarea unei cuantile sau folosirea abaterii intercuartilice presupun o distribuție pe care nu a verificat-o nimeni."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Zero-shot forecasting",
                "text": "Which statement defines zero-shot use of a time series foundation model?",
                "options": [
                    "The model is fine-tuned for a few steps on the target series before forecasting",
                    "The model forecasts without any context",
                    "The model is trained from scratch on the target series with a Transformer architecture",
                    "The pretrained weights stay fixed and only the recent history of the target series is passed as context"
                ],
                "correctExplanation": "Zero-shot: no parameter is estimated on the target; the forecast is $f_{\\hat\\theta}(y_{T-C+1:T})$.",
                "incorrectExplanation": "Fine-tuning and training from scratch estimate parameters on the target; a forecast without context has nothing to condition on."
            },
            "ro": {
                "title": "Prognoza zero-shot",
                "text": "Ce afirmație definește folosirea zero-shot a unui foundation model pentru serii de timp?",
                "options": [
                    "Modelul trece prin fine-tuning cîțiva pași pe seria-țintă înainte de prognoză",
                    "Modelul prognozează fără niciun context",
                    "Modelul este antrenat de la zero pe seria-țintă, cu o arhitectură Transformer",
                    "Ponderile preantrenate rămîn fixe și doar istoria recentă a seriei-țintă este transmisă drept context"
                ],
                "correctExplanation": "Zero-shot: niciun parametru nu se estimează pe seria-țintă; prognoza este $f_{\\hat\\theta}(y_{T-C+1:T})$.",
                "incorrectExplanation": "Fine-tuning-ul și antrenarea de la zero estimează parametri pe seria-țintă; o prognoză fără context nu are nimic de care să depindă."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Why patching",
                "text": "A context of $C = 2048$ values is split into patches of $P = 16$. By what factor does patching reduce the cost of full self-attention, which is quadratic in the number of tokens?",
                "options": [
                    "16",
                    "256",
                    "2048",
                    "It does not change the cost"
                ],
                "correctExplanation": "Tokens fall from $C$ to $C/P$, so the quadratic cost falls by $P^2 = 256$.",
                "incorrectExplanation": "Attention cost is $O(n^2)$ in the number of tokens $n$; dividing $n$ by 16 divides the cost by $16^2$."
            },
            "ro": {
                "title": "Rostul patching-ului",
                "text": "Un context de $C = 2048$ valori este împărțit în patch-uri de $P = 16$. De cîte ori reduce patching-ul costul atenției complete, care este pătratic în numărul de token-uri?",
                "options": [
                    "De 16 ori",
                    "De 256 de ori",
                    "De 2048 de ori",
                    "Nu schimbă costul"
                ],
                "correctExplanation": "Numărul de token-uri scade de la $C$ la $C/P$, deci costul pătratic scade de $P^2 = 256$ de ori.",
                "incorrectExplanation": "Costul atenției este $O(n^2)$ în numărul de token-uri $n$; împărțirea lui $n$ la 16 împarte costul la $16^2$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Scaling evidence for time series",
                "text": "What did Yao et al. (2025) find about scaling laws of time series foundation models?",
                "options": [
                    "Scaling laws do not exist for time series because series are not language",
                    "Larger models are always better on every individual series",
                    "The log-likelihood scales similarly in and out of distribution, but architecture matters and some in-distribution improvements reduce out-of-distribution scalability",
                    "Only the amount of synthetic data matters, not the number of parameters"
                ],
                "correctExplanation": "Their study compares encoder-only and decoder-only models in and out of distribution: similar scaling, strong architectural effects.",
                "incorrectExplanation": "Power-law scaling is documented for time series (also by Edwards et al. 2024); it is a statement about average loss, not about every series, and parameters do matter."
            },
            "ro": {
                "title": "Dovezi de scalare pentru serii de timp",
                "text": "Ce au găsit Yao et al. (2025) despre legile de scalare ale foundation models pentru serii de timp?",
                "options": [
                    "Legile de scalare nu există pentru serii de timp, deoarece seriile nu sînt limbaj",
                    "Modelele mai mari sînt întotdeauna mai bune pe fiecare serie în parte",
                    "Log-verosimilitatea se scalează asemănător în și în afara distribuției, dar arhitectura contează, iar unele îmbunătățiri în distribuție reduc scalabilitatea în afara ei",
                    "Contează doar cantitatea de date sintetice, nu numărul de parametri"
                ],
                "correctExplanation": "Studiul compară modele encoder-only și decoder-only în și în afara distribuției: scalare asemănătoare, efecte puternice ale arhitecturii.",
                "incorrectExplanation": "Scalarea după o lege de putere este documentată pentru serii de timp (și de Edwards et al. 2024); este o afirmație despre pierderea medie, nu despre fiecare serie, iar numărul de parametri contează."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Aggregating relative errors",
                "text": "Models A and B are compared with a baseline on 20 series through ratios $r_s = L_s(\\cdot)/L_s(\\text{baseline})$. Why is the geometric mean of the ratios preferred to their arithmetic mean?",
                "options": [
                    "The ranking of A and B by geometric means does not depend on which baseline is used",
                    "The geometric mean is always smaller, so models look better",
                    "The arithmetic mean of ratios cannot be computed when the baseline is a naive forecast",
                    "The geometric mean gives more weight to the series with the largest scale"
                ],
                "correctExplanation": "The ratio of geometric means of A and B equals the geometric mean of $L_s(A)/L_s(B)$: the baseline cancels (Fleming and Wallace 1986).",
                "incorrectExplanation": "Making models look better is not a criterion; relative scores remove scale, so no series dominates; arithmetic means of ratios can be computed but reward the baseline's weak series."
            },
            "ro": {
                "title": "Agregarea erorilor relative",
                "text": "Modelele A și B sînt comparate cu un model de referință pe 20 de serii prin rapoartele $r_s = L_s(\\cdot)/L_s(\\text{referință})$. De ce este preferată media geometrică a rapoartelor față de media lor aritmetică?",
                "options": [
                    "Ordinea dintre A și B dată de mediile geometrice nu depinde de modelul de referință folosit",
                    "Media geometrică este întotdeauna mai mică, deci modelele par mai bune",
                    "Media aritmetică a rapoartelor nu se poate calcula cînd referința este o prognoză naivă",
                    "Media geometrică dă o pondere mai mare seriilor cu scala cea mai mare"
                ],
                "correctExplanation": "Raportul mediilor geometrice pentru A și B este media geometrică a lui $L_s(A)/L_s(B)$: modelul de referință se simplifică (Fleming și Wallace 1986).",
                "incorrectExplanation": "Faptul că modelele par mai bune nu este un criteriu; scorurile relative elimină scala, deci nicio serie nu domină; media aritmetică a rapoartelor se poate calcula, dar recompensează seriile slabe ale referinței."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "A contamination-safe evaluation window",
                "text": "Chronos-2 was released on 30 October 2025, TimesFM 2.5 on 2 September 2025. Which evaluation window avoids temporal contamination for a comparison of both?",
                "options": [
                    "January 2020 to December 2024, because it is long",
                    "Any window, provided the series is Romanian",
                    "September 2025 to September 2026",
                    "November 2025 onwards"
                ],
                "correctExplanation": "Only data after the release (or declared cutoff) of every model in the comparison cannot have been in their training corpora.",
                "incorrectExplanation": "Length does not protect against leakage; public series of any country may be in a corpus; September and October 2025 precede the Chronos-2 release."
            },
            "ro": {
                "title": "O fereastră de evaluare fără contaminare",
                "text": "Chronos-2 a fost lansat pe 30 octombrie 2025, TimesFM 2.5 pe 2 septembrie 2025. Ce fereastră de evaluare evită contaminarea temporală într-o comparație a celor două?",
                "options": [
                    "Ianuarie 2020 -- decembrie 2024, pentru că este lungă",
                    "Orice fereastră, dacă seria este românească",
                    "Septembrie 2025 -- septembrie 2026",
                    "Din noiembrie 2025 încolo"
                ],
                "correctExplanation": "Doar datele de după lansarea (sau data-limită declarată) a fiecărui model din comparație nu pot fi fost în corpusurile lor de antrenare.",
                "incorrectExplanation": "Lungimea nu protejează de scurgere; seriile publice ale oricărei țări pot face parte dintr-un corpus; septembrie și octombrie 2025 preced lansarea Chronos-2."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Holm and Benjamini-Hochberg",
                "text": "Twenty-seven country-level DM tests are run. Which statement is correct?",
                "options": [
                    "Holm controls the false discovery rate and is more powerful than Benjamini-Hochberg",
                    "Holm controls the family-wise error rate; Benjamini-Hochberg controls the false discovery rate and rejects at least as often",
                    "Both corrections are needed only when the tests are independent",
                    "Without correction, about 27% of the tests reject under the null at 5%"
                ],
                "correctExplanation": "Holm bounds the probability of any false rejection; BH bounds the expected share of false rejections, a weaker target, hence more rejections.",
                "incorrectExplanation": "Holm controls the FWER under any dependence; BH is valid under independence or positive dependence; at 5% about 5% of true nulls are rejected without correction."
            },
            "ro": {
                "title": "Holm și Benjamini-Hochberg",
                "text": "Se aplică 27 de teste DM pe țări. Ce afirmație este corectă?",
                "options": [
                    "Holm controlează rata descoperirilor false și este mai puternic decît Benjamini-Hochberg",
                    "Holm controlează eroarea pe familie; Benjamini-Hochberg controlează rata descoperirilor false și respinge cel puțin la fel de des",
                    "Ambele corecții sînt necesare doar cînd testele sînt independente",
                    "Fără corecție, aproximativ 27% dintre teste resping sub ipoteza nulă la 5%"
                ],
                "correctExplanation": "Holm limitează probabilitatea oricărei respingeri false; BH limitează ponderea așteptată a respingerilor false, o țintă mai slabă, deci mai multe respingeri.",
                "incorrectExplanation": "Holm controlează FWER sub orice dependență; BH este valid sub independență sau dependență pozitivă; la 5%, fără corecție se resping circa 5% dintre ipotezele nule adevărate."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The pooled DM test",
                "text": "Why average the loss differential across countries at each origin and run one DM test with a HAC variance, instead of bootstrapping countries as independent units?",
                "options": [
                    "Because the bootstrap cannot be computed with fewer than 30 countries",
                    "Because the average differential is always zero",
                    "Because overlapping multi-step errors are serially dependent and countries are correlated at each date; the time-series HAC variance keeps both",
                    "Because DM tests require Gaussian losses"
                ],
                "correctExplanation": "Errors at $h > 1$ overlap in time and shocks are common across countries; resampling countries ignores the time dependence and overstates precision.",
                "incorrectExplanation": "A bootstrap over countries can be computed but treats dependent units as independent; DM tests rely on asymptotic normality of the mean, not on Gaussian losses."
            },
            "ro": {
                "title": "Testul DM agregat",
                "text": "De ce se mediază diferența de pierdere pe țări la fiecare origine și se aplică un singur test DM cu varianță HAC, în loc de un bootstrap care tratează țările ca unități independente?",
                "options": [
                    "Pentru că bootstrap-ul nu se poate calcula cu mai puțin de 30 de țări",
                    "Pentru că diferența medie este întotdeauna zero",
                    "Pentru că erorile pe mai mulți pași se suprapun și sînt dependente în timp, iar țările sînt corelate la fiecare dată; varianța HAC în timp le păstrează pe amîndouă",
                    "Pentru că testele DM cer pierderi gaussiene"
                ],
                "correctExplanation": "Erorile pentru $h > 1$ se suprapun în timp, iar șocurile sînt comune țărilor; reeșantionarea țărilor ignoră dependența în timp și exagerează precizia.",
                "incorrectExplanation": "Un bootstrap pe țări se poate calcula, dar tratează unități dependente ca independente; testele DM se sprijină pe normalitatea asimptotică a mediei, nu pe pierderi gaussiene."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Are language models useful?",
                "text": "What did Tan et al. (2024) find in their ablations of LLM-based forecasters such as Time-LLM?",
                "options": [
                    "Removing the language model, or replacing it by a simple attention layer, does not degrade accuracy and often improves it",
                    "Time series foundation models such as Chronos are not useful",
                    "Larger language models always forecast better",
                    "LLMs help mainly when only a few observations are available"
                ],
                "correctExplanation": "Their ablations show the LLM component adds cost, not accuracy; pretrained LLMs did not help in few-shot settings either.",
                "incorrectExplanation": "The study concerns LLM-based forecasters, not models pretrained on series; it finds no benefit of the LLM component, including in few-shot settings."
            },
            "ro": {
                "title": "Sînt utile modelele de limbaj?",
                "text": "Ce au găsit Tan et al. (2024) în ablațiile prognozatorilor bazați pe LLM, precum Time-LLM?",
                "options": [
                    "Eliminarea modelului de limbaj sau înlocuirea lui cu un simplu strat de atenție nu degradează acuratețea și adesea o îmbunătățește",
                    "Foundation models pentru serii de timp, precum Chronos, nu sînt utile",
                    "Modelele de limbaj mai mari prognozează întotdeauna mai bine",
                    "LLM-urile ajută mai ales cînd sînt disponibile puține observații"
                ],
                "correctExplanation": "Ablațiile arată că componenta LLM adaugă cost, nu acuratețe; LLM-urile preantrenate nu au ajutat nici cînd datele sînt puține.",
                "incorrectExplanation": "Studiul privește prognozatori bazați pe LLM, nu modele preantrenate pe serii; nu găsește niciun beneficiu al componentei LLM, nici cînd datele sînt puține."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "LLMTime and number tokens",
                "text": "Gruver et al. (2023) forecast with LLMs by writing values as digits. Why could a newer LLM forecast worse than an older one?",
                "options": [
                    "Newer LLMs have shorter context windows",
                    "Newer LLMs cannot read commas",
                    "Newer LLMs were trained without any numbers",
                    "The way the tokenizer splits numbers into tokens, and alignment that hurts calibration"
                ],
                "correctExplanation": "The paper attributes the result to number tokenization and to alignment (RLHF) degrading calibration.",
                "incorrectExplanation": "Context length, punctuation and the absence of numbers in training are not the reasons given; the tokenization of digits is."
            },
            "ro": {
                "title": "LLMTime și token-urile numerelor",
                "text": "Gruver et al. (2023) prognozează cu LLM-uri scriind valorile ca cifre. De ce ar putea un LLM mai nou să prognozeze mai prost decît unul mai vechi?",
                "options": [
                    "LLM-urile mai noi au ferestre de context mai scurte",
                    "LLM-urile mai noi nu pot citi virgulele",
                    "LLM-urile mai noi au fost antrenate fără niciun număr",
                    "Felul în care tokenizatorul împarte numerele în token-uri și alinierea care strică calibrarea"
                ],
                "correctExplanation": "Lucrarea pune rezultatul pe seama tokenizării numerelor și a alinierii (RLHF), care degradează calibrarea.",
                "incorrectExplanation": "Lungimea contextului, punctuația și lipsa numerelor din antrenare nu sînt motivele indicate; tokenizarea cifrelor este."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Exchangeable or not",
                "text": "Which sequence is exchangeable but not independent?",
                "options": [
                    "A stationary AR(1) with $\\phi = 0.5$",
                    "Draws without replacement from an urn",
                    "Daily returns with GARCH volatility",
                    "A random walk"
                ],
                "correctExplanation": "Draws without replacement have a permutation-invariant joint law but are dependent.",
                "incorrectExplanation": "An AR(1), a GARCH process and a random walk have joint laws that change when dates are permuted: they are not exchangeable."
            },
            "ro": {
                "title": "Interschimbabil sau nu",
                "text": "Care șir este interschimbabil, dar nu independent?",
                "options": [
                    "Un AR(1) staționar cu $\\phi = 0{,}5$",
                    "Extrageri fără întoarcere dintr-o urnă",
                    "Randamente zilnice cu volatilitate GARCH",
                    "Un mers aleator"
                ],
                "correctExplanation": "Extragerile fără întoarcere au o lege comună invariantă la permutări, dar sînt dependente.",
                "incorrectExplanation": "Un AR(1), un proces GARCH și un mers aleator au legi comune care se schimbă dacă se permută momentele: nu sînt interschimbabile."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The split conformal threshold",
                "text": "There are $n = 99$ calibration scores and $\\alpha = 0.05$. Which order statistic is the split conformal threshold?",
                "options": [
                    "The 94th smallest",
                    "The 99th smallest (the maximum)",
                    "The 95th smallest",
                    "The 5th largest plus one"
                ],
                "correctExplanation": "$k = \\lceil (n + 1)(1 - \\alpha)\\rceil = \\lceil 100 \\cdot 0.95\\rceil = 95$.",
                "incorrectExplanation": "The rank uses $n + 1$, not $n$: $\\lceil 100 \\cdot 0.95\\rceil = 95$; the maximum would give coverage close to 99%."
            },
            "ro": {
                "title": "Pragul split conformal",
                "text": "Există $n = 99$ scoruri de calibrare și $\\alpha = 0{,}05$. Ce statistică de ordine este pragul split conformal?",
                "options": [
                    "A 94-a cea mai mică valoare",
                    "A 99-a cea mai mică valoare (maximul)",
                    "A 95-a cea mai mică valoare",
                    "A cincea cea mai mare valoare plus unu"
                ],
                "correctExplanation": "$k = \\lceil (n + 1)(1 - \\alpha)\\rceil = \\lceil 100 \\cdot 0{,}95\\rceil = 95$.",
                "incorrectExplanation": "Rangul folosește $n + 1$, nu $n$: $\\lceil 100 \\cdot 0{,}95\\rceil = 95$; maximul ar da o acoperire apropiată de 99%."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The upper bound on coverage",
                "text": "With continuous scores (no ties), exchangeable data, $n = 20$ and $\\alpha = 0.1$, what is the marginal coverage of split conformal?",
                "options": [
                    "Between 0.90 and 0.95",
                    "Exactly 0.90",
                    "At least 0.95",
                    "Between 0.85 and 0.90"
                ],
                "correctExplanation": "$1 - \\alpha \\le$ coverage $\\le 1 - \\alpha + 1/(n + 1) = 0.90 + 1/21$; here $k = \\lceil 21 \\cdot 0.9\\rceil = 19$ gives exactly $19/21 \\approx 0.905$.",
                "incorrectExplanation": "The guarantee is never below $1 - \\alpha$ and exceeds it by at most $1/(n + 1) \\approx 0.048$; with $n = 20$ the rank argument gives $19/21$, not exactly 0.90."
            },
            "ro": {
                "title": "Marginea superioară a acoperirii",
                "text": "Cu scoruri continue (fără egalități), date interschimbabile, $n = 20$ și $\\alpha = 0{,}1$, care este acoperirea marginală a metodei split conformal?",
                "options": [
                    "Între 0,90 și 0,95",
                    "Exact 0,90",
                    "Cel puțin 0,95",
                    "Între 0,85 și 0,90"
                ],
                "correctExplanation": "$1 - \\alpha \\le$ acoperirea $\\le 1 - \\alpha + 1/(n + 1) = 0{,}90 + 1/21$; aici $k = \\lceil 21 \\cdot 0{,}9\\rceil = 19$ dă exact $19/21 \\approx 0{,}905$.",
                "incorrectExplanation": "Garanția nu coboară niciodată sub $1 - \\alpha$ și o depășește cu cel mult $1/(n + 1) \\approx 0{,}048$; cu $n = 20$, argumentul de rang dă $19/21$, nu exact 0,90."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Coverage given the calibration set",
                "text": "Given one calibration set of $n$ continuous scores, what is the distribution of the coverage $F(\\hat q)$ of the next point under exchangeability?",
                "options": [
                    "A point mass at $1 - \\alpha$",
                    "Uniform on $[0, 1]$",
                    "Normal with mean $1 - \\alpha$ and variance $\\alpha$",
                    "Beta($k$, $n + 1 - k$) with $k = \\lceil (n + 1)(1 - \\alpha)\\rceil$"
                ],
                "correctExplanation": "$F(S_i)$ are i.i.d. uniform, so the $k$-th order statistic $F(S_{(k)})$ is Beta($k$, $n + 1 - k$).",
                "incorrectExplanation": "Coverage given the calibration set is random; it concentrates around $k/(n + 1)$ with variance about $\\alpha(1 - \\alpha)/n$, not $\\alpha$."
            },
            "ro": {
                "title": "Acoperirea condiționată de setul de calibrare",
                "text": "Dat fiind un set de calibrare cu $n$ scoruri continue, care este distribuția acoperirii $F(\\hat q)$ a punctului următor sub interschimbabilitate?",
                "options": [
                    "O masă punctuală în $1 - \\alpha$",
                    "Uniformă pe $[0, 1]$",
                    "Normală cu media $1 - \\alpha$ și varianța $\\alpha$",
                    "Beta($k$, $n + 1 - k$), cu $k = \\lceil (n + 1)(1 - \\alpha)\\rceil$"
                ],
                "correctExplanation": "$F(S_i)$ sînt uniforme i.i.d., deci statistica de ordine $k$, $F(S_{(k)})$, are legea Beta($k$, $n + 1 - k$).",
                "incorrectExplanation": "Acoperirea condiționată de setul de calibrare este aleatoare; se concentrează în jurul lui $k/(n + 1)$, cu varianța aproximativ $\\alpha(1 - \\alpha)/n$, nu $\\alpha$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The CQR interval",
                "text": "In conformalized quantile regression the calibration threshold is $\\hat q = -0.3$ (negative). What is the interval for a new point with quantile forecasts $[2, 5]$?",
                "options": [
                    "$[1.7, 5.3]$",
                    "$[2.3, 4.7]$",
                    "$[2, 5]$, because negative thresholds are set to zero",
                    "The empty set"
                ],
                "correctExplanation": "$[\\hat q_{\\mathrm{lo}} - \\hat q, \\hat q_{\\mathrm{hi}} + \\hat q] = [2.3, 4.7]$: a negative threshold narrows an over-wide band.",
                "incorrectExplanation": "The band is shifted by $\\hat q$ on each side, inwards when $\\hat q < 0$; nothing is truncated at zero."
            },
            "ro": {
                "title": "Intervalul CQR",
                "text": "În regresia cuantilică conformalizată, pragul de calibrare este $\\hat q = -0{,}3$ (negativ). Care este intervalul pentru un punct nou cu prognozele cuantilelor $[2; 5]$?",
                "options": [
                    "$[1{,}7; 5{,}3]$",
                    "$[2{,}3; 4{,}7]$",
                    "$[2; 5]$, deoarece pragurile negative se înlocuiesc cu zero",
                    "Mulțimea vidă"
                ],
                "correctExplanation": "$[\\hat q_{\\mathrm{lo}} - \\hat q; \\hat q_{\\mathrm{hi}} + \\hat q] = [2{,}3; 4{,}7]$: un prag negativ îngustează o bandă prea largă.",
                "incorrectExplanation": "Banda se deplasează cu $\\hat q$ pe fiecare parte, spre interior cînd $\\hat q < 0$; nimic nu este trunchiat la zero."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Conditional coverage",
                "text": "What do Vovk (2012) and Foygel Barber et al. (2021) show about distribution-free conditional coverage for a continuous covariate?",
                "options": [
                    "It is achieved by CQR in finite samples",
                    "It is achieved by split conformal with at least 1000 calibration points",
                    "Any method guaranteeing it for every distribution must have infinite expected length",
                    "It holds whenever the data are i.i.d."
                ],
                "correctExplanation": "Exact conditional coverage at almost every $x$ for all distributions forces infinite expected length: only marginal or group-wise guarantees are possible.",
                "incorrectExplanation": "CQR and split conformal give marginal coverage only, whatever the calibration size and even under i.i.d. data."
            },
            "ro": {
                "title": "Acoperirea condiționată",
                "text": "Ce arată Vovk (2012) și Foygel Barber et al. (2021) despre acoperirea condiționată fără ipoteze de distribuție pentru o covariabilă continuă?",
                "options": [
                    "Este obținută de CQR în eșantioane finite",
                    "Este obținută de split conformal cu cel puțin 1000 de puncte de calibrare",
                    "Orice metodă care o garantează pentru orice distribuție trebuie să aibă lungime așteptată infinită",
                    "Este valabilă ori de cîte ori datele sînt i.i.d."
                ],
                "correctExplanation": "Acoperirea condiționată exactă în aproape orice $x$, pentru toate distribuțiile, impune o lungime așteptată infinită: sînt posibile doar garanții marginale sau pe grupuri.",
                "incorrectExplanation": "CQR și split conformal dau doar acoperire marginală, oricare ar fi mărimea calibrării și chiar cu date i.i.d."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Weighted conformal beyond exchangeability",
                "text": "In Barber et al. (2023) the coverage of weighted conformal is at least $1 - \\alpha$ minus a term. Which term?",
                "options": [
                    "$\\sum_i \\tilde w_i\\, d_{\\mathrm{TV}}(Z, Z^i)$, the weighted total-variation distance after swapping the test point with point $i$",
                    "$1/(n + 1)$",
                    "$\\gamma$, the step size",
                    "The mixing coefficient of the scores at lag one"
                ],
                "correctExplanation": "The bound is $1 - \\alpha - \\sum_i \\tilde w_i d_{\\mathrm{TV}}(Z, Z^i)$; small weights on old points keep the gap small under drift.",
                "incorrectExplanation": "$1/(n + 1)$ is the upper slack of split conformal, $\\gamma$ belongs to ACI, and mixing coefficients appear in other analyses of split conformal."
            },
            "ro": {
                "title": "Conformal ponderat dincolo de interschimbabilitate",
                "text": "La Barber et al. (2023), acoperirea metodei conformale ponderate este cel puțin $1 - \\alpha$ minus un termen. Care termen?",
                "options": [
                    "$\\sum_i \\tilde w_i\\, d_{\\mathrm{TV}}(Z, Z^i)$, distanța în variație totală ponderată după schimbarea punctului de test cu punctul $i$",
                    "$1/(n + 1)$",
                    "$\\gamma$, pasul",
                    "Coeficientul de mixing al scorurilor la decalajul unu"
                ],
                "correctExplanation": "Marginea este $1 - \\alpha - \\sum_i \\tilde w_i d_{\\mathrm{TV}}(Z, Z^i)$; ponderile mici pe punctele vechi țin abaterea mică sub o derivă.",
                "incorrectExplanation": "$1/(n + 1)$ este rezerva superioară a metodei split conformal, $\\gamma$ aparține ACI, iar coeficienții de mixing apar în alte analize ale metodei split conformal."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The ACI update",
                "text": "ACI uses $\\alpha_{t+1} = \\alpha_t + \\gamma(\\alpha - \\mathrm{err}_t)$ with $\\alpha = 0.1$. What happens after a miss ($\\mathrm{err}_t = 1$)?",
                "options": [
                    "$\\alpha_t$ rises by $0.1\\gamma$ and the next set is narrower",
                    "$\\alpha_t$ is reset to 0.1",
                    "The calibration window is emptied",
                    "$\\alpha_t$ falls by $0.9\\gamma$ and the next set is wider"
                ],
                "correctExplanation": "A miss subtracts $\\gamma(1 - \\alpha) = 0.9\\gamma$: a lower level means a higher quantile, hence a wider set.",
                "incorrectExplanation": "A hit raises $\\alpha_t$ by $0.1\\gamma$; nothing is reset or emptied: the level moves by the update rule only."
            },
            "ro": {
                "title": "Actualizarea ACI",
                "text": "ACI folosește $\\alpha_{t+1} = \\alpha_t + \\gamma(\\alpha - \\mathrm{err}_t)$ cu $\\alpha = 0{,}1$. Ce se întîmplă după o ratare ($\\mathrm{err}_t = 1$)?",
                "options": [
                    "$\\alpha_t$ crește cu $0{,}1\\gamma$, iar mulțimea următoare este mai îngustă",
                    "$\\alpha_t$ este readus la 0,1",
                    "Fereastra de calibrare este golită",
                    "$\\alpha_t$ scade cu $0{,}9\\gamma$, iar mulțimea următoare este mai largă"
                ],
                "correctExplanation": "O ratare scade $\\gamma(1 - \\alpha) = 0{,}9\\gamma$: un nivel mai mic înseamnă o cuantilă mai mare, deci o mulțime mai largă.",
                "incorrectExplanation": "O acoperire crește $\\alpha_t$ cu $0{,}1\\gamma$; nimic nu este readus sau golit: nivelul se mișcă doar după regula de actualizare."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The ACI bound",
                "text": "For $\\alpha = \\alpha_1 = 0.1$, $\\gamma = 0.005$ and $T = 2000$, what is the bound on $|\\frac1T\\sum_t \\mathrm{err}_t - \\alpha|$?",
                "options": [
                    "0.005",
                    "about 0.09",
                    "about 0.45",
                    "0.1"
                ],
                "correctExplanation": "$(\\max\\{0.1, 0.9\\} + 0.005)/(0.005 \\cdot 2000) = 0.905/10 \\approx 0.09$.",
                "incorrectExplanation": "The bound is $(\\max\\{\\alpha_1, 1 - \\alpha_1\\} + \\gamma)/(\\gamma T)$; it shrinks like $1/T$ and here equals about 0.09."
            },
            "ro": {
                "title": "Marginea ACI",
                "text": "Pentru $\\alpha = \\alpha_1 = 0{,}1$, $\\gamma = 0{,}005$ și $T = 2000$, cît este marginea pentru $|\\frac1T\\sum_t \\mathrm{err}_t - \\alpha|$?",
                "options": [
                    "0,005",
                    "aproximativ 0,09",
                    "aproximativ 0,45",
                    "0,1"
                ],
                "correctExplanation": "$(\\max\\{0{,}1; 0{,}9\\} + 0{,}005)/(0{,}005 \\cdot 2000) = 0{,}905/10 \\approx 0{,}09$.",
                "incorrectExplanation": "Marginea este $(\\max\\{\\alpha_1, 1 - \\alpha_1\\} + \\gamma)/(\\gamma T)$; scade ca $1/T$ și aici este aproximativ 0,09."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Quantile tracking",
                "text": "Conformal PID starts from quantile tracking, $q_{t+1} = q_t + \\eta(\\mathrm{err}_t - \\alpha)$. How does it differ from ACI?",
                "options": [
                    "It needs exchangeable scores",
                    "It updates the miscoverage level instead of the threshold",
                    "It moves the threshold directly on the scale of the scores, with a bound $(B + \\eta)/(\\eta T)$ for scores in $[0, B]$",
                    "It guarantees conditional coverage"
                ],
                "correctExplanation": "Quantile tracking is online gradient descent on the pinball loss of the score; ACI moves the level $\\alpha_t$ instead.",
                "incorrectExplanation": "Neither method needs exchangeability or delivers conditional coverage; it is ACI that updates the level."
            },
            "ro": {
                "title": "Urmărirea cuantilei",
                "text": "PID conformal pornește de la urmărirea cuantilei, $q_{t+1} = q_t + \\eta(\\mathrm{err}_t - \\alpha)$. Prin ce diferă de ACI?",
                "options": [
                    "Are nevoie de scoruri interschimbabile",
                    "Actualizează nivelul de neacoperire în locul pragului",
                    "Mută pragul direct pe scala scorurilor, cu marginea $(B + \\eta)/(\\eta T)$ pentru scoruri în $[0, B]$",
                    "Garantează acoperirea condiționată"
                ],
                "correctExplanation": "Urmărirea cuantilei este o coborîre pe gradient online pe pierderea pinball a scorului; ACI mută în schimb nivelul $\\alpha_t$.",
                "incorrectExplanation": "Niciuna dintre metode nu cere interschimbabilitate și nu dă acoperire condiționată; ACI este cea care actualizează nivelul."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "EnbPI",
                "text": "Which feature characterises EnbPI (Xu and Xie 2021)?",
                "options": [
                    "Bootstrap ensembles with leave-one-out residuals and a sliding window of residuals, without refitting at each step",
                    "An exact finite-sample guarantee under any dependence",
                    "A separate calibration set chosen at random from the whole sample",
                    "A step size $\\gamma$ that moves the miscoverage level"
                ],
                "correctExplanation": "EnbPI aggregates models fitted on bootstrap samples, uses out-of-bag residuals and updates the residual window online.",
                "incorrectExplanation": "Its guarantee is asymptotic, under mixing and a consistent ensemble; random calibration splits ignore time order; the step size belongs to ACI."
            },
            "ro": {
                "title": "EnbPI",
                "text": "Ce caracterizează metoda EnbPI (Xu și Xie 2021)?",
                "options": [
                    "Ansambluri bootstrap cu reziduuri leave-one-out și o fereastră mobilă de reziduuri, fără reestimare la fiecare pas",
                    "O garanție exactă în eșantioane finite sub orice dependență",
                    "Un set de calibrare separat, ales aleator din tot eșantionul",
                    "Un pas $\\gamma$ care mută nivelul de neacoperire"
                ],
                "correctExplanation": "EnbPI agregă modele estimate pe eșantioane bootstrap, folosește reziduuri din afara eșantionului bootstrap și actualizează online fereastra de reziduuri.",
                "incorrectExplanation": "Garanția ei este asimptotică, sub mixing și pentru un ansamblu consistent; o calibrare aleatoare ignoră ordinea în timp; pasul aparține ACI."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer: ACI",
                "text": "An AI assistant writes: \"(i) ACI keeps the long-run miss rate close to alpha for any sequence of data. (ii) Its sets can become infinite. (iii) It guarantees that misses are independent over time.\" Which statement is wrong?",
                "options": [
                    "(i)",
                    "(ii)",
                    "(i) and (ii)",
                    "(iii)"
                ],
                "correctExplanation": "ACI controls only the long-run frequency; misses can cluster, which a Christoffersen test detects.",
                "incorrectExplanation": "(i) is the ACI theorem and (ii) happens when $\\alpha_t \\le 0$; neither is wrong."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI: ACI",
                "text": "Un asistent AI scrie: „(i) ACI menține frecvența ratărilor pe termen lung aproape de alpha pentru orice șir de date. (ii) Mulțimile lui pot deveni infinite. (iii) Garantează că ratările sînt independente în timp.” Ce afirmație este greșită?",
                "options": [
                    "(i)",
                    "(ii)",
                    "(i) și (ii)",
                    "(iii)"
                ],
                "correctExplanation": "ACI controlează doar frecvența pe termen lung; ratările se pot grupa, lucru pe care îl detectează testul Christoffersen.",
                "incorrectExplanation": "(i) este teorema ACI, iar (ii) se întîmplă cînd $\\alpha_t \\le 0$; niciuna nu este greșită."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the error in the AI answer: calibration",
                "text": "An AI assistant writes: \"(i) A foundation model's quantiles are calibrated on its corpus, not necessarily on your series. (ii) Online CQR with ACI also fixes the clustering of VaR exceedances. (iii) A conformal step can give a 95% interval from a model that outputs only deciles.\" Which statement is wrong?",
                "options": [
                    "(i)",
                    "(ii)",
                    "(iii)",
                    "None"
                ],
                "correctExplanation": "Calibration fixes the exceedance frequency; clustering depends on how well the underlying forecasts track volatility.",
                "incorrectExplanation": "(i) is why calibration is needed and (iii) is what online CQR does with the score built on the 10% and 90% quantiles."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI: calibrarea",
                "text": "Un asistent AI scrie: „(i) Cuantilele unui foundation model sînt calibrate pe corpusul lui, nu neapărat pe seria dumneavoastră. (ii) CQR online cu ACI corectează și gruparea depășirilor VaR. (iii) Un pas conformal poate da un interval de 95% dintr-un model care produce doar decile.” Ce afirmație este greșită?",
                "options": [
                    "(i)",
                    "(ii)",
                    "(iii)",
                    "Niciuna"
                ],
                "correctExplanation": "Calibrarea corectează frecvența depășirilor; gruparea depinde de cît de bine urmăresc prognozele de bază volatilitatea.",
                "incorrectExplanation": "(i) este motivul pentru care calibrarea este necesară, iar (iii) este ceea ce face CQR online cu scorul construit pe cuantilele de 10% și 90%."
            }
        }
    ]
};
