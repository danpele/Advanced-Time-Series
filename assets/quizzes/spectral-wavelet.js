// ============================================================
// Chapter 11 quiz bank: Spectral and wavelet analysis (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['spectral-wavelet'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 1,
            "en": {
                "title": "Consistency of the periodogram",
                "text": "For a linear process with a positive continuous spectrum, why is the raw periodogram $I(\\omega_j)$ not a consistent estimator of $f(\\omega_j)$?",
                "options": [
                    "It is asymptotically biased at every interior frequency",
                    "Its variance tends to $f(\\omega_j)^2$ and does not shrink as $n$ grows",
                    "It can take negative values",
                    "It is consistent only at the Fourier frequencies"
                ],
                "correctExplanation": "Asymptotically $I(\\omega_j) \\approx f(\\omega_j)\\chi^2_2/2$: unbiased in the limit, with variance $f(\\omega_j)^2$ for every $n$.",
                "incorrectExplanation": "The periodogram is non-negative and asymptotically unbiased; its problem is the variance, at Fourier frequencies as everywhere else."
            },
            "ro": {
                "title": "Consistența periodogramei",
                "text": "Pentru un proces liniar cu spectru continuu și pozitiv, de ce nu este periodograma brută $I(\\omega_j)$ un estimator consistent al lui $f(\\omega_j)$?",
                "options": [
                    "Este asimptotic deplasată la orice frecvență interioară",
                    "Varianța ei tinde la $f(\\omega_j)^2$ și nu scade cînd $n$ crește",
                    "Poate lua valori negative",
                    "Este consistentă doar la frecvențele Fourier"
                ],
                "correctExplanation": "Asimptotic $I(\\omega_j) \\approx f(\\omega_j)\\chi^2_2/2$: nedeplasată la limită, cu varianța $f(\\omega_j)^2$ oricare ar fi $n$.",
                "incorrectExplanation": "Periodograma este nenegativă și asimptotic nedeplasată; problema ei este varianța, la frecvențele Fourier ca peste tot."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Spectrum of a filtered process",
                "text": "If $Y_t = \\sum_j a_jX_{t-j}$ with $\\sum_j|a_j| < \\infty$ and $A(\\omega) = \\sum_j a_je^{-i\\omega j}$, the spectrum of $Y$ is:",
                "options": [
                    "$f_Y(\\omega) = A(\\omega)f_X(\\omega)$",
                    "$f_Y(\\omega) = |A(\\omega)|f_X(\\omega)$",
                    "$f_Y(\\omega) = f_X(\\omega)/|A(\\omega)|^2$",
                    "$f_Y(\\omega) = |A(\\omega)|^2f_X(\\omega)$"
                ],
                "correctExplanation": "By Cramér's representation $dZ_Y = A\\,dZ_X$, so $\\E|dZ_Y|^2 = |A|^2\\E|dZ_X|^2$.",
                "incorrectExplanation": "A spectrum is real and non-negative: the complex transfer function enters through its squared modulus, not linearly or inverted."
            },
            "ro": {
                "title": "Spectrul unui proces filtrat",
                "text": "Dacă $Y_t = \\sum_j a_jX_{t-j}$, cu $\\sum_j|a_j| < \\infty$ și $A(\\omega) = \\sum_j a_je^{-i\\omega j}$, spectrul lui $Y$ este:",
                "options": [
                    "$f_Y(\\omega) = A(\\omega)f_X(\\omega)$",
                    "$f_Y(\\omega) = |A(\\omega)|f_X(\\omega)$",
                    "$f_Y(\\omega) = f_X(\\omega)/|A(\\omega)|^2$",
                    "$f_Y(\\omega) = |A(\\omega)|^2f_X(\\omega)$"
                ],
                "correctExplanation": "Prin reprezentarea lui Cramér, $dZ_Y = A\\,dZ_X$, deci $\\E|dZ_Y|^2 = |A|^2\\E|dZ_X|^2$.",
                "incorrectExplanation": "Un spectru este real și nenegativ: funcția de transfer complexă intră prin pătratul modulului, nu liniar sau inversată."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Optimal bandwidth",
                "text": "For a lag window with characteristic exponent $q = 2$ (Parzen, quadratic spectral), the MSE-optimal truncation $M^*$ grows with the sample size as:",
                "options": [
                    "$n^{1/5}$",
                    "$n^{1/3}$",
                    "$n^{1/2}$",
                    "$n$"
                ],
                "correctExplanation": "Minimising $k_q^2f^{(q)2}M^{-2q} + (M/n)f^2\\int k^2$ gives $M^* \\propto n^{1/(2q+1)} = n^{1/5}$.",
                "incorrectExplanation": "$n^{1/3}$ is the rate for Bartlett ($q = 1$); $M$ proportional to $n^{1/2}$ or $n$ does not balance squared bias and variance."
            },
            "ro": {
                "title": "Lățimea de bandă optimă",
                "text": "Pentru o fereastră de decalaje cu exponentul caracteristic $q = 2$ (Parzen, pătratic spectral), trunchierea optimă în MSE $M^*$ crește cu mărimea eșantionului ca:",
                "options": [
                    "$n^{1/5}$",
                    "$n^{1/3}$",
                    "$n^{1/2}$",
                    "$n$"
                ],
                "correctExplanation": "Minimizînd $k_q^2f^{(q)2}M^{-2q} + (M/n)f^2\\int k^2$ obținem $M^* \\propto n^{1/(2q+1)} = n^{1/5}$.",
                "incorrectExplanation": "$n^{1/3}$ este rata pentru Bartlett ($q = 1$); un $M$ proporțional cu $n^{1/2}$ sau cu $n$ nu echilibrează deplasarea la pătrat și varianța."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Equivalent degrees of freedom",
                "text": "A Bartlett lag-window estimate with $n = 200$ and $M = 20$ ($\\int k^2 = 2/3$) is approximately $f\\chi^2_\\nu/\\nu$ with $\\nu$ equal to:",
                "options": [
                    "10",
                    "20",
                    "60",
                    "30"
                ],
                "correctExplanation": "$\\nu = 2n/(M\\int k^2) = 400/(20\\cdot2/3) = 30$.",
                "incorrectExplanation": "The formula is $2n/(M\\int k^2)$; 10, 20 and 60 come from dropping the factor 2, the kernel integral or both."
            },
            "ro": {
                "title": "Grade de libertate echivalente",
                "text": "O estimare Bartlett cu fereastră de decalaje, cu $n = 200$ și $M = 20$ ($\\int k^2 = 2/3$), este aproximativ $f\\chi^2_\\nu/\\nu$, cu $\\nu$ egal cu:",
                "options": [
                    "10",
                    "20",
                    "60",
                    "30"
                ],
                "correctExplanation": "$\\nu = 2n/(M\\int k^2) = 400/(20\\cdot2/3) = 30$.",
                "incorrectExplanation": "Formula este $2n/(M\\int k^2)$; valorile 10, 20 și 60 provin din omiterea factorului 2, a integralei nucleului sau a ambelor."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Multitaper degrees of freedom",
                "text": "A multitaper estimate with time--bandwidth product $NW = 4$ and the usual number of Slepian tapers has approximately how many degrees of freedom?",
                "options": [
                    "4",
                    "8",
                    "14",
                    "7"
                ],
                "correctExplanation": "$K = 2NW - 1 = 7$ nearly uncorrelated eigenspectra, each with 2 degrees of freedom: $2K\\hat f/f \\approx \\chi^2_{14}$.",
                "incorrectExplanation": "7 is the number of tapers, not the degrees of freedom; 4 and 8 confuse $NW$ with $K$."
            },
            "ro": {
                "title": "Gradele de libertate multitaper",
                "text": "O estimare multitaper cu produsul timp--bandă $NW = 4$ și numărul uzual de taper-e Slepian are aproximativ cîte grade de libertate?",
                "options": [
                    "4",
                    "8",
                    "14",
                    "7"
                ],
                "correctExplanation": "$K = 2NW - 1 = 7$ spectre proprii aproape necorelate, fiecare cu 2 grade de libertate: $2K\\hat f/f \\approx \\chi^2_{14}$.",
                "incorrectExplanation": "7 este numărul taper-elor, nu numărul gradelor de libertate; 4 și 8 confundă $NW$ cu $K$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Adaptive multitaper weights",
                "text": "What do Thomson's adaptive weights achieve?",
                "options": [
                    "They down-weight tapers with poor spectral concentration at frequencies where the spectrum is small, reducing leakage",
                    "They increase the number of degrees of freedom above $2K$",
                    "They remove the need to choose $NW$",
                    "They make the estimate consistent without increasing $K$"
                ],
                "correctExplanation": "The weight $d_k = \\sqrt{\\lambda_k}f/(\\lambda_kf + (1 - \\lambda_k)\\sigma^2)$ shrinks the leaky high-order tapers where $f$ is small relative to the broadband level.",
                "incorrectExplanation": "Adaptive weighting can only lower the equivalent degrees of freedom; $NW$ still fixes the resolution; consistency needs $K$ (or $NW$) to grow."
            },
            "ro": {
                "title": "Ponderile multitaper adaptive",
                "text": "Ce realizează ponderile adaptive ale lui Thomson?",
                "options": [
                    "Reduc ponderea taper-elor slab concentrate la frecvențele unde spectrul este mic, reducînd scurgerea",
                    "Cresc numărul gradelor de libertate peste $2K$",
                    "Elimină necesitatea alegerii lui $NW$",
                    "Fac estimarea consistentă fără creșterea lui $K$"
                ],
                "correctExplanation": "Ponderea $d_k = \\sqrt{\\lambda_k}f/(\\lambda_kf + (1 - \\lambda_k)\\sigma^2)$ micșorează taper-ele de ordin mare, care au scurgeri, acolo unde $f$ este mic față de nivelul de bandă largă.",
                "incorrectExplanation": "Ponderarea adaptivă poate doar să scadă gradele de libertate echivalente; $NW$ fixează în continuare rezoluția; consistența cere creșterea lui $K$ (sau a lui $NW$)."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Thomson's harmonic F test",
                "text": "Thomson's harmonic F test at frequency $\\omega$ with $K$ tapers tests:",
                "options": [
                    "a deterministic sinusoid (a spectral line) at $\\omega$, with an $F(2, 2K - 2)$ distribution under the null",
                    "whether the spectrum has a peak at $\\omega$, with a $\\chi^2_{2K}$ distribution",
                    "whether two series are coherent at $\\omega$",
                    "white noise against any alternative, with an $F(K, K)$ distribution"
                ],
                "correctExplanation": "The eigencoefficients are regressed on the taper means $U_k(0)$; a line makes the regression coefficient non-zero; numerator 2 and denominator $2K - 2$ degrees of freedom.",
                "incorrectExplanation": "A stochastic peak is not a line; coherence and white-noise tests are different statistics."
            },
            "ro": {
                "title": "Testul F armonic al lui Thomson",
                "text": "Testul F armonic al lui Thomson la frecvența $\\omega$, cu $K$ taper-e, testează:",
                "options": [
                    "o sinusoidă deterministă (o linie spectrală) la $\\omega$, cu distribuția $F(2, 2K - 2)$ sub ipoteza nulă",
                    "dacă spectrul are un vîrf la $\\omega$, cu distribuția $\\chi^2_{2K}$",
                    "dacă două serii sînt coerente la $\\omega$",
                    "zgomotul alb față de orice alternativă, cu distribuția $F(K, K)$"
                ],
                "correctExplanation": "Coeficienții proprii se regresează pe mediile taper-elor $U_k(0)$; o linie face coeficientul de regresie nenul; 2 grade de libertate la numărător și $2K - 2$ la numitor.",
                "incorrectExplanation": "Un vîrf stochastic nu este o linie; testele de coerență și de zgomot alb sînt alte statistici."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Raw coherence",
                "text": "Squared coherence computed from the raw cross-periodogram, without any averaging, equals:",
                "options": [
                    "zero at every frequency for independent series",
                    "the squared correlation of the two series",
                    "the true coherence, but with a large variance",
                    "one at every frequency, whatever the data"
                ],
                "correctExplanation": "With a single ordinate $|I_{xy}|^2 = I_xI_y$ identically, so the ratio is 1: averaging over frequencies or tapers is what makes coherence an estimator.",
                "incorrectExplanation": "Without averaging the statistic carries no information; it does not equal zero, the correlation, or a noisy version of the truth."
            },
            "ro": {
                "title": "Coerența brută",
                "text": "Coerența pătratică calculată din periodograma încrucișată brută, fără nicio mediere, este egală cu:",
                "options": [
                    "zero la orice frecvență pentru serii independente",
                    "pătratul corelației celor două serii",
                    "coerența adevărată, dar cu o varianță mare",
                    "unu la orice frecvență, oricare ar fi datele"
                ],
                "correctExplanation": "Cu o singură ordonată, $|I_{xy}|^2 = I_xI_y$ identic, deci raportul este 1: medierea pe frecvențe sau pe taper-e face din coerență un estimator.",
                "incorrectExplanation": "Fără mediere, statistica nu conține nicio informație; nu este egală cu zero, cu corelația sau cu o versiune zgomotoasă a valorii adevărate."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Coherence threshold",
                "text": "Squared coherence is estimated by averaging over $L = 7$ independent ordinates (for example 7 tapers). Its 5% critical value under no coherence is approximately:",
                "options": [
                    "0.393",
                    "0.050",
                    "0.143",
                    "0.700"
                ],
                "correctExplanation": "$\\Pr(\\hat\\kappa^2 > c) = (1 - c)^{L-1}$, so $c = 1 - 0.05^{1/6} \\approx 0.393$.",
                "incorrectExplanation": "0.05 is the size, not the threshold; $1/L$ and 0.7 do not follow from the null distribution."
            },
            "ro": {
                "title": "Pragul coerenței",
                "text": "Coerența pătratică se estimează prin medierea a $L = 7$ ordonate independente (de exemplu 7 taper-e). Valoarea ei critică de 5% fără coerență este aproximativ:",
                "options": [
                    "0,393",
                    "0,050",
                    "0,143",
                    "0,700"
                ],
                "correctExplanation": "$\\Pr(\\hat\\kappa^2 > c) = (1 - c)^{L-1}$, deci $c = 1 - 0{,}05^{1/6} \\approx 0{,}393$.",
                "incorrectExplanation": "0,05 este nivelul testului, nu pragul; $1/L$ și 0,7 nu rezultă din distribuția sub ipoteza nulă."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Reading the phase",
                "text": "With $\\gamma_{xy}(h) = \\Cov(x_{t+h}, y_t)$ and $y_t = x_{t-3} + u_t$ ($u$ independent noise), the phase of $f_{xy}$ at frequency $\\omega$ is:",
                "options": [
                    "$-3\\omega$: $y$ leads $x$ by 3 periods",
                    "zero, because the series are contemporaneously uncorrelated",
                    "$\\pi$ at every frequency",
                    "$3\\omega$: $x$ leads $y$ by 3 periods"
                ],
                "correctExplanation": "$\\Cov(x_{t+h}, x_{t-3})$ is non-zero at $h = -3$, so $f_{xy} \\propto e^{3i\\omega}$: phase $3\\omega$, a lead of $\\phi/\\omega = 3$ periods for $x$.",
                "incorrectExplanation": "The sign follows from the convention for $\\gamma_{xy}$; a pure delay gives a phase linear in $\\omega$, not zero or constant."
            },
            "ro": {
                "title": "Interpretarea fazei",
                "text": "Cu $\\gamma_{xy}(h) = \\Cov(x_{t+h}, y_t)$ și $y_t = x_{t-3} + u_t$ ($u$ zgomot independent), faza lui $f_{xy}$ la frecvența $\\omega$ este:",
                "options": [
                    "$-3\\omega$: $y$ conduce $x$ cu 3 perioade",
                    "zero, deoarece seriile sînt necorelate simultan",
                    "$\\pi$ la orice frecvență",
                    "$3\\omega$: $x$ conduce $y$ cu 3 perioade"
                ],
                "correctExplanation": "$\\Cov(x_{t+h}, x_{t-3})$ este nenul pentru $h = -3$, deci $f_{xy} \\propto e^{3i\\omega}$: faza $3\\omega$, un avans de $\\phi/\\omega = 3$ perioade pentru $x$.",
                "incorrectExplanation": "Semnul rezultă din convenția pentru $\\gamma_{xy}$; un decalaj pur dă o fază liniară în $\\omega$, nu nulă sau constantă."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Coherence and filtering",
                "text": "If $x$ and $y$ are each passed through (different) invertible linear filters, their squared coherence:",
                "options": [
                    "is multiplied by the product of the squared gains",
                    "does not change, although the phase may change",
                    "becomes one at the frequencies where the filters have unit gain",
                    "is unchanged only if both filters are identical"
                ],
                "correctExplanation": "$f_{\\tilde x\\tilde y} = A\\bar Bf_{xy}$, $f_{\\tilde x} = |A|^2f_x$, $f_{\\tilde y} = |B|^2f_y$: the gains cancel in the ratio; the phase shifts by $\\arg A - \\arg B$.",
                "incorrectExplanation": "The gains cancel whatever the filters are, as long as they are non-zero at that frequency."
            },
            "ro": {
                "title": "Coerența și filtrarea",
                "text": "Dacă $x$ și $y$ trec fiecare printr-un filtru liniar inversabil (diferit), coerența lor pătratică:",
                "options": [
                    "se înmulțește cu produsul pătratelor cîștigurilor",
                    "nu se schimbă, deși faza se poate schimba",
                    "devine unu la frecvențele unde filtrele au cîștigul unu",
                    "rămîne neschimbată doar dacă filtrele sînt identice"
                ],
                "correctExplanation": "$f_{\\tilde x\\tilde y} = A\\bar Bf_{xy}$, $f_{\\tilde x} = |A|^2f_x$, $f_{\\tilde y} = |B|^2f_y$: cîștigurile se simplifică în raport; faza se mută cu $\\arg A - \\arg B$.",
                "incorrectExplanation": "Cîștigurile se simplifică oricare ar fi filtrele, cîtă vreme sînt nenule la acea frecvență."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Dynamic correlation",
                "text": "How does the dynamic correlation of Croux, Forni and Reichlin (2001) differ from squared coherence?",
                "options": [
                    "It is always larger than the squared coherence",
                    "It cannot be averaged over a band of frequencies",
                    "It uses only the co-spectrum, so it has a sign and ignores out-of-phase co-movement",
                    "It is defined only for non-stationary series"
                ],
                "correctExplanation": "$\\rho(\\omega) = c_{xy}/\\sqrt{f_xf_y} \\in [-1, 1]$ and $\\kappa^2 = \\rho^2 + q_{xy}^2/(f_xf_y)$.",
                "incorrectExplanation": "Since $\\kappa^2 = \\rho^2 + $ a non-negative term, $\\rho^2$ never exceeds $\\kappa^2$; band averages are the main use of the measure, for stationary series."
            },
            "ro": {
                "title": "Corelația dinamică",
                "text": "Prin ce diferă corelația dinamică a lui Croux, Forni și Reichlin (2001) de coerența pătratică?",
                "options": [
                    "Este întotdeauna mai mare decît coerența pătratică",
                    "Nu se poate media pe o bandă de frecvențe",
                    "Folosește doar cospectrul, deci are semn și ignoră co-mișcarea defazată",
                    "Este definită doar pentru serii nestaționare"
                ],
                "correctExplanation": "$\\rho(\\omega) = c_{xy}/\\sqrt{f_xf_y} \\in [-1, 1]$ și $\\kappa^2 = \\rho^2 + q_{xy}^2/(f_xf_y)$.",
                "incorrectExplanation": "Deoarece $\\kappa^2 = \\rho^2 + $ un termen nenegativ, $\\rho^2$ nu depășește niciodată $\\kappa^2$; mediile pe benzi sînt utilizarea principală a măsurii, pentru serii staționare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Geweke's decomposition",
                "text": "In Geweke (1982), the frequency-domain causality measure $M_{y \\to x}(\\omega)$ is related to the time-domain Granger measure $F_{y \\to x} = \\ln(\\sigma^2_{x|x}/\\sigma^2_{x|x,y})$ by:",
                "options": [
                    "$\\frac1\\pi\\int_0^\\pi M_{y \\to x}(\\omega)\\,d\\omega = F_{y \\to x}$ under a mild condition",
                    "$M_{y \\to x}(0) = F_{y \\to x}$",
                    "$\\max_\\omega M_{y \\to x}(\\omega) = F_{y \\to x}$",
                    "$M_{y \\to x}(\\omega) = F_{y \\to x}$ at every $\\omega$"
                ],
                "correctExplanation": "The measure decomposes the total Granger measure over frequencies: its average over $[0, \\pi]$ is the time-domain measure.",
                "incorrectExplanation": "The total measure is an average over frequencies, not the value at zero, the maximum or a constant."
            },
            "ro": {
                "title": "Descompunerea lui Geweke",
                "text": "La Geweke (1982), măsura cauzalității în domeniul frecvenței $M_{y \\to x}(\\omega)$ este legată de măsura Granger din domeniul timpului $F_{y \\to x} = \\ln(\\sigma^2_{x|x}/\\sigma^2_{x|x,y})$ prin:",
                "options": [
                    "$\\frac1\\pi\\int_0^\\pi M_{y \\to x}(\\omega)\\,d\\omega = F_{y \\to x}$, sub o condiție slabă",
                    "$M_{y \\to x}(0) = F_{y \\to x}$",
                    "$\\max_\\omega M_{y \\to x}(\\omega) = F_{y \\to x}$",
                    "$M_{y \\to x}(\\omega) = F_{y \\to x}$ la orice $\\omega$"
                ],
                "correctExplanation": "Măsura descompune măsura Granger totală pe frecvențe: media ei pe $[0, \\pi]$ este măsura din domeniul timpului.",
                "incorrectExplanation": "Măsura totală este o medie pe frecvențe, nu valoarea în zero, maximul sau o constantă."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The Breitung--Candelon test",
                "text": "In a bivariate VAR(2), the Breitung--Candelon test of no causality from $y$ to $x$ at frequency $\\omega \\in (0, \\pi)$:",
                "options": [
                    "rejects only at low frequencies",
                    "is equivalent to the ordinary Granger test at every such frequency",
                    "has a $\\chi^2_4$ distribution",
                    "cannot be computed because it needs at least two restrictions"
                ],
                "correctExplanation": "The two restrictions $\\sum_j\\psi_j\\cos(j\\omega) = \\sum_j\\psi_j\\sin(j\\omega) = 0$ on $(\\psi_1, \\psi_2)$ are non-singular, so they force $\\psi_1 = \\psi_2 = 0$; frequency profiles need $p \\ge 3$.",
                "incorrectExplanation": "The test has two restrictions (an $F(2, \\cdot)$ or $\\chi^2_2$ statistic) and can be computed; with $p = 2$ it simply does not vary with $\\omega$."
            },
            "ro": {
                "title": "Testul Breitung--Candelon",
                "text": "Într-un VAR(2) bivariat, testul Breitung--Candelon al absenței cauzalității de la $y$ la $x$ la frecvența $\\omega \\in (0, \\pi)$:",
                "options": [
                    "respinge doar la frecvențe joase",
                    "este echivalent cu testul Granger obișnuit la orice astfel de frecvență",
                    "are distribuția $\\chi^2_4$",
                    "nu se poate calcula, deoarece cere cel puțin două restricții"
                ],
                "correctExplanation": "Cele două restricții $\\sum_j\\psi_j\\cos(j\\omega) = \\sum_j\\psi_j\\sin(j\\omega) = 0$ asupra lui $(\\psi_1, \\psi_2)$ sînt nesingulare, deci impun $\\psi_1 = \\psi_2 = 0$; profilurile pe frecvențe cer $p \\ge 3$.",
                "incorrectExplanation": "Testul are două restricții (o statistică $F(2, \\cdot)$ sau $\\chi^2_2$) și se poate calcula; cu $p = 2$ pur și simplu nu variază cu $\\omega$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The gain of the HP filter",
                "text": "The cycle extracted by the HP filter with $\\lambda = 1600$ has gain $G(\\omega) = 4\\lambda(1 - \\cos\\omega)^2/(1 + 4\\lambda(1 - \\cos\\omega)^2)$. Which statement is correct?",
                "options": [
                    "It is an ideal band-pass filter for 6--32 quarters",
                    "It removes all cycles longer than 8 quarters",
                    "It is a high-pass filter: about 0.70 of a 32-quarter cycle and about 0.49 of a 40-quarter cycle pass into the cycle",
                    "Its gain is zero at the business-cycle frequencies"
                ],
                "correctExplanation": "$G$ rises monotonically from 0 at $\\omega = 0$ to 1; at periods of 32 and 40 quarters it is about 0.70 and 0.49, so long cycles leak into the HP cycle.",
                "incorrectExplanation": "There is no upper cutoff and the gain is close to one at business-cycle frequencies; the filter is neither band-pass nor a remover of 8-quarter cycles."
            },
            "ro": {
                "title": "Cîștigul filtrului HP",
                "text": "Ciclul extras de filtrul HP cu $\\lambda = 1600$ are cîștigul $G(\\omega) = 4\\lambda(1 - \\cos\\omega)^2/(1 + 4\\lambda(1 - \\cos\\omega)^2)$. Care afirmație este corectă?",
                "options": [
                    "Este un filtru trece-bandă ideal pentru 6--32 de trimestre",
                    "Elimină toate ciclurile mai lungi de 8 trimestre",
                    "Este un filtru trece-sus: aproximativ 0,70 dintr-un ciclu de 32 de trimestre și 0,49 dintr-unul de 40 de trimestre trec în ciclu",
                    "Cîștigul lui este zero la frecvențele ciclului economic"
                ],
                "correctExplanation": "$G$ crește monoton de la 0 în $\\omega = 0$ la 1; la perioade de 32 și 40 de trimestre este aproximativ 0,70 și 0,49, deci ciclurile lungi trec în ciclul HP.",
                "incorrectExplanation": "Nu există o limită superioară, iar cîștigul este aproape de unu la frecvențele ciclului economic; filtrul nu este trece-bandă și nu elimină ciclurile de 8 trimestre."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The spurious HP cycle",
                "text": "Cogley and Nason (1995): when the HP filter ($\\lambda = 1600$) is applied to a quarterly random walk, the spectrum of the extracted cycle:",
                "options": [
                    "is flat, as for white noise",
                    "peaks at a period of 6 quarters",
                    "is identical to the spectrum of the random walk",
                    "peaks at a period of about 30 quarters, although the random walk has no cycle"
                ],
                "correctExplanation": "Its spectrum is proportional to $u^3/(1 + 4\\lambda u^2)^2$ in $u = 1 - \\cos\\omega$, maximised at $u^* = \\sqrt{3/(4\\lambda)}$: a period of about 30.1 quarters.",
                "incorrectExplanation": "The filter shapes the spectrum: the product of the squared gain and the random-walk spectrum has an interior maximum near 7.5 years."
            },
            "ro": {
                "title": "Ciclul fals al filtrului HP",
                "text": "Cogley și Nason (1995): cînd filtrul HP ($\\lambda = 1600$) se aplică unui mers aleator trimestrial, spectrul ciclului extras:",
                "options": [
                    "este plat, ca pentru un zgomot alb",
                    "are un vîrf la perioada de 6 trimestre",
                    "este identic cu spectrul mersului aleator",
                    "are un vîrf la o perioadă de circa 30 de trimestre, deși mersul aleator nu are niciun ciclu"
                ],
                "correctExplanation": "Spectrul este proporțional cu $u^3/(1 + 4\\lambda u^2)^2$ în $u = 1 - \\cos\\omega$, maxim în $u^* = \\sqrt{3/(4\\lambda)}$: o perioadă de circa 30,1 trimestre.",
                "incorrectExplanation": "Filtrul modelează spectrul: produsul dintre pătratul cîștigului și spectrul mersului aleator are un maxim interior în jur de 7,5 ani."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Hamilton's regression filter",
                "text": "For a random walk, Hamilton's (2018) filter with $h = 8$ gives the cycle $y_{t+8} - y_t$. Its gain from the level to the cycle, $2|\\sin(4\\omega)|$:",
                "options": [
                    "is 1 on the 6--32-quarter band and 0 elsewhere",
                    "equals 2 at a period of 16 quarters and 0 at a period of 8 quarters",
                    "is increasing in the frequency",
                    "equals 1 at every frequency"
                ],
                "correctExplanation": "At period 16, $\\omega = \\pi/8$ and $\\sin(\\pi/2) = 1$; at period 8, $\\omega = \\pi/4$ and $\\sin(\\pi) = 0$: the filter doubles some cycles and removes others.",
                "incorrectExplanation": "The 8-quarter difference is not a band-pass filter: its gain oscillates between 0 and 2."
            },
            "ro": {
                "title": "Filtrul de regresie al lui Hamilton",
                "text": "Pentru un mers aleator, filtrul lui Hamilton (2018) cu $h = 8$ dă ciclul $y_{t+8} - y_t$. Cîștigul lui de la nivel la ciclu, $2|\\sin(4\\omega)|$:",
                "options": [
                    "este 1 pe banda de 6--32 de trimestre și 0 în rest",
                    "este 2 la perioada de 16 trimestre și 0 la perioada de 8 trimestre",
                    "este crescător în frecvență",
                    "este 1 la orice frecvență"
                ],
                "correctExplanation": "La perioada 16, $\\omega = \\pi/8$ și $\\sin(\\pi/2) = 1$; la perioada 8, $\\omega = \\pi/4$ și $\\sin(\\pi) = 0$: filtrul dublează unele cicluri și le elimină pe altele.",
                "incorrectExplanation": "Diferența pe 8 trimestre nu este un filtru trece-bandă: cîștigul ei oscilează între 0 și 2."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The end-point problem",
                "text": "Why do HP output-gap estimates for the most recent quarters get revised substantially when new data arrive?",
                "options": [
                    "Because the HP filter is a random-walk forecast",
                    "Because $\\lambda$ is re-estimated every quarter",
                    "At the end of the sample the filter is one-sided, while the final estimate uses future observations",
                    "Because the Baxter--King constraint fails at the end"
                ],
                "correctExplanation": "The HP smoother uses both past and future data; at the last observation only the past is available, and the weights change when new data arrive.",
                "incorrectExplanation": "$\\lambda$ is fixed by convention, the HP filter is not a forecast, and the Baxter--King constraint concerns another filter."
            },
            "ro": {
                "title": "Problema capetelor de eșantion",
                "text": "De ce sînt revizuite substanțial estimările HP ale deviației PIB-ului pentru ultimele trimestre cînd sosesc date noi?",
                "options": [
                    "Deoarece filtrul HP este o prognoză de tip mers aleator",
                    "Deoarece $\\lambda$ se reestimează în fiecare trimestru",
                    "La capătul eșantionului filtrul este unilateral, în timp ce estimarea finală folosește observații viitoare",
                    "Deoarece restricția Baxter--King nu este îndeplinită la capăt"
                ],
                "correctExplanation": "Netezitorul HP folosește date trecute și viitoare; la ultima observație este disponibil doar trecutul, iar ponderile se schimbă cînd sosesc date noi.",
                "incorrectExplanation": "$\\lambda$ este fixat prin convenție, filtrul HP nu este o prognoză, iar restricția Baxter--King privește alt filtru."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "MODWT and DWT",
                "text": "Which property does the MODWT have that the DWT does not?",
                "options": [
                    "It is an orthonormal transform with exactly $n$ coefficients",
                    "It does not need boundary corrections",
                    "It is defined for any sample size and is invariant to circular shifts of the series",
                    "It gives a Fourier spectrum at every time point"
                ],
                "correctExplanation": "The MODWT does not downsample: $J \\times n$ coefficients, any $n$, shift-invariant, energy-preserving through the rescaled filters.",
                "incorrectExplanation": "Exactly $n$ orthonormal coefficients is the DWT; both transforms have boundary coefficients; neither is a time-local Fourier spectrum."
            },
            "ro": {
                "title": "MODWT și DWT",
                "text": "Ce proprietate are MODWT și nu are DWT?",
                "options": [
                    "Este o transformare ortonormată cu exact $n$ coeficienți",
                    "Nu are nevoie de corecții la margini",
                    "Este definită pentru orice mărime a eșantionului și este invariantă la translațiile circulare ale seriei",
                    "Dă un spectru Fourier în fiecare moment"
                ],
                "correctExplanation": "MODWT nu reduce eșantionarea: $J \\times n$ coeficienți, orice $n$, invarianță la translații, conservarea energiei prin filtrele rescalate.",
                "incorrectExplanation": "Exact $n$ coeficienți ortonormați înseamnă DWT; ambele transformări au coeficienți de margine; niciuna nu este un spectru Fourier local în timp."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Wavelet variance of white noise",
                "text": "For white noise with variance $\\sigma^2$, the MODWT wavelet variance at level $j$ (periods $2^j$ to $2^{j+1}$) is:",
                "options": [
                    "$\\sigma^2/2^j$",
                    "$\\sigma^2$ at every level",
                    "$\\sigma^2\\cdot2^j$",
                    "$\\sigma^2/j$"
                ],
                "correctExplanation": "Level $j$ captures the octave $[1/2^{j+1}, 1/2^j]$ of a flat spectrum, a share $1/2^j$ of the variance.",
                "incorrectExplanation": "A flat spectrum spreads variance evenly over frequencies, and each lower octave is half as wide as the previous one."
            },
            "ro": {
                "title": "Varianța wavelet a unui zgomot alb",
                "text": "Pentru un zgomot alb cu varianța $\\sigma^2$, varianța wavelet MODWT la nivelul $j$ (perioade de la $2^j$ la $2^{j+1}$) este:",
                "options": [
                    "$\\sigma^2/2^j$",
                    "$\\sigma^2$ la orice nivel",
                    "$\\sigma^2\\cdot2^j$",
                    "$\\sigma^2/j$"
                ],
                "correctExplanation": "Nivelul $j$ captează octava $[1/2^{j+1}, 1/2^j]$ a unui spectru plat, adică o parte $1/2^j$ din varianță.",
                "incorrectExplanation": "Un spectru plat distribuie varianța uniform pe frecvențe, iar fiecare octavă inferioară are o lățime pe jumătate față de precedenta."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Morlet scale and period",
                "text": "For the Morlet wavelet with $\\omega_0 = 6$, a scale $s = 50$ weeks corresponds to a Fourier period of about:",
                "options": [
                    "50 weeks",
                    "52 weeks",
                    "25 weeks",
                    "314 weeks"
                ],
                "correctExplanation": "The Fourier factor is $4\\pi/(\\omega_0 + \\sqrt{2 + \\omega_0^2}) \\approx 1.033$, so the period is about $51.7$ weeks.",
                "incorrectExplanation": "Scale and period are close but not equal for $\\omega_0 = 6$; halving or multiplying by $2\\pi$ uses the wrong conversion."
            },
            "ro": {
                "title": "Scala și perioada Morlet",
                "text": "Pentru wavelet-ul Morlet cu $\\omega_0 = 6$, o scală $s = 50$ de săptămîni corespunde unei perioade Fourier de aproximativ:",
                "options": [
                    "50 de săptămîni",
                    "52 de săptămîni",
                    "25 de săptămîni",
                    "314 de săptămîni"
                ],
                "correctExplanation": "Factorul Fourier este $4\\pi/(\\omega_0 + \\sqrt{2 + \\omega_0^2}) \\approx 1{,}033$, deci perioada este de circa 51,7 săptămîni.",
                "incorrectExplanation": "Scala și perioada sînt apropiate, dar nu egale pentru $\\omega_0 = 6$; înjumătățirea sau înmulțirea cu $2\\pi$ folosește o conversie greșită."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Significance of wavelet coherence",
                "text": "In Grinsted et al. (2004), the 5% significance level of wavelet coherence is obtained:",
                "options": [
                    "from a $\\chi^2_2$ distribution at each point",
                    "from the 1 $- 0.05^{1/(L-1)}$ formula with $L$ the number of scales",
                    "by comparing with the coherence of the series with itself",
                    "by Monte Carlo, from pairs of independent AR(1) series with the lag-1 autocorrelations of the data"
                ],
                "correctExplanation": "The smoothing operator has no simple closed-form null distribution, so Grinsted et al. simulate red-noise pairs and take the 95th percentile at each scale.",
                "incorrectExplanation": "The $\\chi^2_2$ law is for wavelet power, the closed-form threshold is for averages of independent ordinates, and self-coherence is always one."
            },
            "ro": {
                "title": "Semnificația coerenței wavelet",
                "text": "La Grinsted et al. (2004), nivelul de semnificație de 5% al coerenței wavelet se obține:",
                "options": [
                    "dintr-o distribuție $\\chi^2_2$ în fiecare punct",
                    "din formula $1 - 0{,}05^{1/(L-1)}$, cu $L$ numărul de scale",
                    "prin comparație cu coerența seriei cu ea însăși",
                    "prin Monte Carlo, din perechi de serii AR(1) independente cu autocorelațiile de ordinul 1 ale datelor"
                ],
                "correctExplanation": "Operatorul de netezire nu are o distribuție nulă simplă în formă închisă, deci Grinsted et al. simulează perechi de zgomot roșu și iau percentila 95 la fiecare scală.",
                "incorrectExplanation": "Legea $\\chi^2_2$ privește puterea wavelet, pragul în formă închisă privește medii de ordonate independente, iar coerența unei serii cu ea însăși este întotdeauna unu."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the error in the AI answer (1)",
                "text": "An AI assistant summarised a BET--DAX wavelet-coherence map: (i) ``every island inside the 5% contour is a contagion episode''; (ii) ``arrows pointing right mean the markets move in phase''; (iii) ``results inside the cone of influence are unreliable''. Which statement is wrong?",
                "options": [
                    "(ii): right-pointing arrows mean anti-phase",
                    "(i): independent series also produce significant islands (about 5% of the area), so islands are not episodes by themselves",
                    "(iii): the cone of influence marks the most reliable region",
                    "None: all three statements are correct"
                ],
                "correctExplanation": "Pointwise testing over thousands of points produces islands by chance; an areawise check or a volatility-matched null is needed before naming episodes.",
                "incorrectExplanation": "Right-pointing arrows do mean in phase, and the cone of influence marks the unreliable edge region; so one statement is wrong."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI (1)",
                "text": "Un asistent AI a rezumat o hartă de coerență wavelet BET--DAX: (i) „fiecare insulă din interiorul conturului de 5% este un episod de contagiune”; (ii) „săgețile spre dreapta înseamnă că piețele se mișcă în fază”; (iii) „rezultatele din conul de influență nu sînt fiabile”. Care afirmație este greșită?",
                "options": [
                    "(ii): săgețile spre dreapta înseamnă antifază",
                    "(i): și seriile independente produc insule semnificative (circa 5% din arie), deci o insulă nu este, prin ea însăși, un episod",
                    "(iii): conul de influență marchează zona cea mai fiabilă",
                    "Niciuna: toate cele trei afirmații sînt corecte"
                ],
                "correctExplanation": "Testarea punctuală în mii de puncte produce insule din întîmplare; este nevoie de o verificare pe arii sau de o ipoteză nulă cu aceeași volatilitate înainte de a numi episoade.",
                "incorrectExplanation": "Săgețile spre dreapta înseamnă într-adevăr în fază, iar conul de influență marchează zona nefiabilă de la margini; deci o afirmație este greșită."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer (2)",
                "text": "An AI assistant wrote: (i) ``Baxter--King with $K = 12$ loses 12 observations at each end''; (ii) ``the BK weights sum to zero, so the filter removes a unit root''; (iii) ``a squared coherence of 0.30 with 7 tapers is significant at 5%''. Which statement is wrong?",
                "options": [
                    "(i): BK loses no observations",
                    "(ii): the BK weights sum to one",
                    "(iii): with 7 tapers the 5% threshold is about 0.39",
                    "None: all three statements are correct"
                ],
                "correctExplanation": "$1 - 0.05^{1/6} \\approx 0.393 > 0.30$; statements (i) and (ii) describe the Baxter--King filter correctly.",
                "incorrectExplanation": "BK is a symmetric moving average of length $2K + 1$, so it loses $K$ observations at each end, and its weights are constrained to sum to zero."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI (2)",
                "text": "Un asistent AI a scris: (i) „Baxter--King cu $K = 12$ pierde 12 observații la fiecare capăt”; (ii) „ponderile BK au suma zero, deci filtrul elimină o rădăcină unitară”; (iii) „o coerență pătratică de 0,30 cu 7 taper-e este semnificativă la 5%”. Care afirmație este greșită?",
                "options": [
                    "(i): BK nu pierde nicio observație",
                    "(ii): ponderile BK au suma unu",
                    "(iii): cu 7 taper-e pragul de 5% este aproximativ 0,39",
                    "Niciuna: toate cele trei afirmații sînt corecte"
                ],
                "correctExplanation": "$1 - 0{,}05^{1/6} \\approx 0{,}393 > 0{,}30$; afirmațiile (i) și (ii) descriu corect filtrul Baxter--King.",
                "incorrectExplanation": "BK este o medie mobilă simetrică de lungime $2K + 1$, deci pierde $K$ observații la fiecare capăt, iar ponderile sînt constrînse să aibă suma zero."
            }
        }
    ]
};
