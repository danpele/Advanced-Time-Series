// ============================================================
// Chapter 0 quiz bank: Refresher and inference for dependent data (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['refresher'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Long-run variance of an AR(1)",
                "text": "For a stationary AR(1) $x_t = \\phi x_{t-1} + \\varepsilon_t$ with $\\Var(\\varepsilon_t) = \\sigma^2$, what is the long-run variance $\\Omega = \\sum_j \\gamma_j$?",
                "options": [
                    "$\\sigma^2/(1-\\phi)^2$",
                    "$\\sigma^2/(1-\\phi^2)$",
                    "$\\sigma^2(1+\\phi)^2$",
                    "$\\sigma^2/(1+\\phi)^2$"
                ],
                "correctExplanation": "$\\Omega = \\sigma^2\\theta(1)^2/\\phi(1)^2$ with $\\phi(1) = 1 - \\phi$ and $\\theta(1) = 1$, so $\\Omega = \\sigma^2/(1-\\phi)^2$.",
                "incorrectExplanation": "$\\sigma^2/(1-\\phi^2)$ is $\\gamma_0$, the variance, not the long-run variance; the long-run variance is $2\\pi f(0) = \\sigma^2/(1-\\phi)^2$."
            },
            "ro": {
                "title": "Varianța de termen lung a unui AR(1)",
                "text": "Pentru un AR(1) staționar $x_t = \\phi x_{t-1} + \\varepsilon_t$ cu $\\Var(\\varepsilon_t) = \\sigma^2$, cît este varianța de termen lung $\\Omega = \\sum_j \\gamma_j$?",
                "options": [
                    "$\\sigma^2/(1-\\phi)^2$",
                    "$\\sigma^2/(1-\\phi^2)$",
                    "$\\sigma^2(1+\\phi)^2$",
                    "$\\sigma^2/(1+\\phi)^2$"
                ],
                "correctExplanation": "$\\Omega = \\sigma^2\\theta(1)^2/\\phi(1)^2$ cu $\\phi(1) = 1 - \\phi$ și $\\theta(1) = 1$, deci $\\Omega = \\sigma^2/(1-\\phi)^2$.",
                "incorrectExplanation": "$\\sigma^2/(1-\\phi^2)$ este $\\gamma_0$, varianța, nu varianța de termen lung; varianța de termen lung este $2\\pi f(0) = \\sigma^2/(1-\\phi)^2$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Size of the naive test",
                "text": "Data follow an AR(1) with $\\phi = 0.6$. What is the asymptotic size of the naive 5% $t$-test for the mean, which uses $\\hat\\gamma_0$ as the variance?",
                "options": [
                    "5%",
                    "About 33%",
                    "About 10%",
                    "About 60%"
                ],
                "correctExplanation": "The naive $t$ is asymptotically $N(0, (1+\\phi)/(1-\\phi)) = N(0, 4)$, so the size is $2[1 - \\Phi(1.96/2)] = 32.7\\%$.",
                "incorrectExplanation": "The variance factor is $(1+\\phi)/(1-\\phi) = 4$: the $t$-statistic has standard deviation 2, not 1, and the rejection probability is $2[1 - \\Phi(0.98)]$, about one third."
            },
            "ro": {
                "title": "Mărimea testului naiv",
                "text": "Datele urmează un AR(1) cu $\\phi = 0,6$. Care este mărimea asimptotică a testului $t$ naiv de 5% pentru medie, care folosește $\\hat\\gamma_0$ ca varianță?",
                "options": [
                    "5%",
                    "Aproximativ 33%",
                    "Aproximativ 10%",
                    "Aproximativ 60%"
                ],
                "correctExplanation": "$t$ naiv este asimptotic $N(0, (1+\\phi)/(1-\\phi)) = N(0, 4)$, deci mărimea este $2[1 - \\Phi(1,96/2)] = 32,7\\%$.",
                "incorrectExplanation": "Factorul de varianță este $(1+\\phi)/(1-\\phi) = 4$: statistica $t$ are abaterea standard 2, nu 1, iar probabilitatea de respingere este $2[1 - \\Phi(0,98)]$, aproximativ o treime."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Negative autocorrelation",
                "text": "A series has $\\rho_1 < 0$ and $\\rho_j = 0$ for $j \\ge 2$. Compared with the naive standard error of the mean, the correct (long-run) standard error is:",
                "options": [
                    "larger",
                    "equal",
                    "smaller",
                    "undefined"
                ],
                "correctExplanation": "$\\Omega/\\gamma_0 = 1 + 2\\rho_1 < 1$: the long-run variance is below the variance, so the naive standard error is too large (the S&P 500 mean return is an example).",
                "incorrectExplanation": "With only $\\rho_1 \\neq 0$, $\\Omega = \\gamma_0(1 + 2\\rho_1)$, which is below $\\gamma_0$ when $\\rho_1 < 0$; robust inference is not always more conservative."
            },
            "ro": {
                "title": "Autocorelație negativă",
                "text": "O serie are $\\rho_1 < 0$ și $\\rho_j = 0$ pentru $j \\ge 2$. Față de eroarea standard naivă a mediei, eroarea standard corectă (de termen lung) este:",
                "options": [
                    "mai mare",
                    "egală",
                    "mai mică",
                    "nedefinită"
                ],
                "correctExplanation": "$\\Omega/\\gamma_0 = 1 + 2\\rho_1 < 1$: varianța de termen lung este sub varianță, deci eroarea standard naivă este prea mare (media randamentelor S&P 500 este un exemplu).",
                "incorrectExplanation": "Cu doar $\\rho_1 \\neq 0$, $\\Omega = \\gamma_0(1 + 2\\rho_1)$, care este sub $\\gamma_0$ cînd $\\rho_1 < 0$; inferența robustă nu este întotdeauna mai conservatoare."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Ergodicity",
                "text": "Let $x_t = Z + \\varepsilon_t$, where $Z \\sim N(0,1)$ is drawn once and $\\varepsilon_t$ is i.i.d. $N(0,1)$ independent of $Z$. Which statement is true?",
                "options": [
                    "$x_t$ is ergodic, so $\\bar x \\to 0$",
                    "$x_t$ is not stationary",
                    "$x_t$ is a martingale difference sequence",
                    "$x_t$ is strictly stationary but not ergodic, and $\\bar x \\to Z$"
                ],
                "correctExplanation": "All finite-dimensional distributions are shift-invariant, but the time average converges to the realised $Z$, not to $E x_t = 0$: stationarity without ergodicity.",
                "incorrectExplanation": "The process is stationary (its distribution does not depend on $t$), its mean is not learned from one path, and $E(x_t \\mid x_{t-1}, \\dots) \\neq 0$ because the past reveals $Z$."
            },
            "ro": {
                "title": "Ergodicitate",
                "text": "Fie $x_t = Z + \\varepsilon_t$, unde $Z \\sim N(0,1)$ este extras o singură dată, iar $\\varepsilon_t$ este i.i.d. $N(0,1)$, independent de $Z$. Ce afirmație este adevărată?",
                "options": [
                    "$x_t$ este ergodic, deci $\\bar x \\to 0$",
                    "$x_t$ nu este staționar",
                    "$x_t$ este o secvență de diferențe de martingală",
                    "$x_t$ este strict staționar, dar nu ergodic, iar $\\bar x \\to Z$"
                ],
                "correctExplanation": "Toate distribuțiile finit-dimensionale sînt invariante la translație, dar media în timp converge la valoarea realizată $Z$, nu la $E x_t = 0$: staționaritate fără ergodicitate.",
                "incorrectExplanation": "Procesul este staționar (distribuția nu depinde de $t$), media lui nu poate fi aflată dintr-o singură traiectorie, iar $E(x_t \\mid x_{t-1}, \\dots) \\neq 0$, pentru că trecutul îl dezvăluie pe $Z$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Martingale differences",
                "text": "For a strictly stationary GARCH(1,1) return $r_t = \\sigma_t z_t$ with finite variance, which estimator of $\\Var(\\sqrt{T}\\bar r)$ is consistent?",
                "options": [
                    "Only a HAC estimator, because $r_t^2$ is autocorrelated",
                    "The sample variance $\\hat\\gamma_0$: $r_t$ is a martingale difference, so $\\Omega = \\gamma_0$",
                    "None, because returns are heteroskedastic",
                    "Only the wild bootstrap"
                ],
                "correctExplanation": "$E(r_t \\mid \\mathcal{F}_{t-1}) = 0$ makes all autocovariances of $r_t$ zero, so $\\Omega = \\gamma_0$; the autocorrelation of $r_t^2$ matters for the mean of squares, not of returns.",
                "incorrectExplanation": "Conditional heteroskedasticity does not create autocorrelation in $r_t$; a HAC estimator is also consistent here but not required, and the naive variance is consistent too."
            },
            "ro": {
                "title": "Diferențe de martingală",
                "text": "Pentru un randament GARCH(1,1) strict staționar $r_t = \\sigma_t z_t$ cu varianță finită, ce estimator al lui $\\Var(\\sqrt{T}\\bar r)$ este consistent?",
                "options": [
                    "Doar un estimator HAC, pentru că $r_t^2$ este autocorelat",
                    "Varianța de selecție $\\hat\\gamma_0$: $r_t$ este o diferență de martingală, deci $\\Omega = \\gamma_0$",
                    "Niciunul, pentru că randamentele sînt heteroscedastice",
                    "Doar wild bootstrap"
                ],
                "correctExplanation": "$E(r_t \\mid \\mathcal{F}_{t-1}) = 0$ anulează toate autocovarianțele lui $r_t$, deci $\\Omega = \\gamma_0$; autocorelația lui $r_t^2$ contează pentru media pătratelor, nu pentru media randamentelor.",
                "incorrectExplanation": "Heteroscedasticitatea condiționată nu creează autocorelație în $r_t$; un estimator HAC este și el consistent aici, dar nu este necesar, iar varianța naivă este consistentă."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Mixing models",
                "text": "Which process is NOT covered by the standard mixing CLT for its sample mean?",
                "options": [
                    "A stationary ARMA(1,1) with Gaussian innovations",
                    "A strictly stationary GARCH(1,1) with finite fourth moment",
                    "An i.i.d. sequence with finite variance",
                    "A random walk $x_t = x_{t-1} + \\varepsilon_t$"
                ],
                "correctExplanation": "A random walk is not stationary, $\\Omega = \\infty$ and the mixing coefficients do not vanish: the mean has a nonstandard limit.",
                "incorrectExplanation": "Stationary ARMA and GARCH(1,1) are geometrically $\\beta$-mixing (Mokkadem 1988; Carrasco and Chen 2002), and i.i.d. sequences mix trivially."
            },
            "ro": {
                "title": "Modele mixing",
                "text": "Ce proces NU este acoperit de TLC standard pentru procese mixing, în cazul mediei de selecție?",
                "options": [
                    "Un ARMA(1,1) staționar cu inovații gaussiene",
                    "Un GARCH(1,1) strict staționar cu moment de ordinul patru finit",
                    "O secvență i.i.d. cu varianță finită",
                    "Un mers aleator $x_t = x_{t-1} + \\varepsilon_t$"
                ],
                "correctExplanation": "Un mers aleator nu este staționar, $\\Omega = \\infty$, iar coeficienții de mixing nu tind la zero: media are o limită nestandard.",
                "incorrectExplanation": "ARMA staționar și GARCH(1,1) sînt $\\beta$-mixing geometric (Mokkadem 1988; Carrasco și Chen 2002), iar secvențele i.i.d. sînt trivial mixing."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Newey–West by hand",
                "text": "With $\\hat\\gamma_0 = 1$, $\\hat\\gamma_1 = 0.5$, $\\hat\\gamma_2 = 0.2$ and $L = 2$ lags, what is the Newey–West estimate $\\hat\\Omega$?",
                "options": [
                    "$1 + 2(\\tfrac23 \\cdot 0.5 + \\tfrac13 \\cdot 0.2) \\approx 1.80$",
                    "$1 + 2(0.5 + 0.2) = 2.40$",
                    "$1 + 0.5 + 0.2 = 1.70$",
                    "$1 + 2(\\tfrac12 \\cdot 0.5) = 1.50$"
                ],
                "correctExplanation": "Bartlett weights are $1 - j/(L+1)$: $2/3$ and $1/3$; so $\\hat\\Omega = 1 + 2(0.333 + 0.067) = 1.80$.",
                "incorrectExplanation": "The truncated kernel would give 2.40 (no down-weighting); the Newey–West weights for $L = 2$ are $2/3$ and $1/3$, and each autocovariance enters twice."
            },
            "ro": {
                "title": "Newey–West de mînă",
                "text": "Cu $\\hat\\gamma_0 = 1$, $\\hat\\gamma_1 = 0,5$, $\\hat\\gamma_2 = 0,2$ și $L = 2$ decalaje, cît este estimarea Newey–West $\\hat\\Omega$?",
                "options": [
                    "$1 + 2(\\tfrac23 \\cdot 0,5 + \\tfrac13 \\cdot 0,2) \\approx 1,80$",
                    "$1 + 2(0,5 + 0,2) = 2,40$",
                    "$1 + 0,5 + 0,2 = 1,70$",
                    "$1 + 2(\\tfrac12 \\cdot 0,5) = 1,50$"
                ],
                "correctExplanation": "Ponderile Bartlett sînt $1 - j/(L+1)$: $2/3$ și $1/3$; deci $\\hat\\Omega = 1 + 2(0,333 + 0,067) = 1,80$.",
                "incorrectExplanation": "Nucleul trunchiat ar da 2,40 (fără subponderare); ponderile Newey–West pentru $L = 2$ sînt $2/3$ și $1/3$, iar fiecare autocovarianță apare de două ori."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Positive semi-definiteness",
                "text": "Why is the Newey–West (Bartlett) estimator never negative?",
                "options": [
                    "Because it uses few lags",
                    "Because the sample autocovariances are always positive",
                    "It equals a scaled sum of squared moving sums of the data",
                    "Because it is consistent"
                ],
                "correctExplanation": "$\\hat\\Omega_{NW} = \\frac{1}{(L+1)T}\\sum_t s_t^2$ with $s_t$ a moving sum of $L+1$ observations: a sum of squares is nonnegative.",
                "incorrectExplanation": "Few lags do not guarantee a positive sum (the truncated kernel with one lag can be negative), sample autocovariances can be negative, and consistency is an asymptotic property."
            },
            "ro": {
                "title": "Pozitiv semidefinire",
                "text": "De ce estimatorul Newey–West (Bartlett) nu este niciodată negativ?",
                "options": [
                    "Pentru că folosește puține decalaje",
                    "Pentru că autocovarianțele de selecție sînt întotdeauna pozitive",
                    "Este egal cu o sumă scalată de pătrate ale unor sume mobile ale datelor",
                    "Pentru că este consistent"
                ],
                "correctExplanation": "$\\hat\\Omega_{NW} = \\frac{1}{(L+1)T}\\sum_t s_t^2$, cu $s_t$ o sumă mobilă de $L+1$ observații: o sumă de pătrate este nenegativă.",
                "incorrectExplanation": "Puține decalaje nu garantează o sumă pozitivă (nucleul trunchiat cu un decalaj poate fi negativ), autocovarianțele de selecție pot fi negative, iar consistența este o proprietate asimptotică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Bandwidth rates",
                "text": "For the quadratic spectral kernel (order $q = 2$), the MSE-optimal bandwidth of Andrews (1991) grows at rate:",
                "options": [
                    "$T^{1/3}$",
                    "$T^{1/2}$",
                    "$\\log T$",
                    "$T^{1/5}$"
                ],
                "correctExplanation": "Bias is $O(S^{-q})$ and variance $O(S/T)$; balancing gives $S \\propto T^{1/(2q+1)} = T^{1/5}$ for $q = 2$.",
                "incorrectExplanation": "$T^{1/3}$ is the rate for the Bartlett kernel ($q = 1$); $T^{1/2}$ is the LLSW test-oriented rule, not the MSE-optimal rate."
            },
            "ro": {
                "title": "Ratele lățimii de bandă",
                "text": "Pentru nucleul spectral pătratic (ordinul $q = 2$), lățimea de bandă optimă în sensul erorii pătratice medii (Andrews 1991) crește cu rata:",
                "options": [
                    "$T^{1/3}$",
                    "$T^{1/2}$",
                    "$\\log T$",
                    "$T^{1/5}$"
                ],
                "correctExplanation": "Deplasarea este $O(S^{-q})$, iar varianța $O(S/T)$; echilibrul dă $S \\propto T^{1/(2q+1)} = T^{1/5}$ pentru $q = 2$.",
                "incorrectExplanation": "$T^{1/3}$ este rata pentru nucleul Bartlett ($q = 1$); $T^{1/2}$ este regula LLSW orientată spre test, nu rata optimă în sensul erorii pătratice medii."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Fixed-b",
                "text": "In fixed-b asymptotics (Kiefer and Vogelsang 2005), the ratio $b = S/T$ is held fixed. What happens to the 5% critical value of the Bartlett $t$-test as $b$ increases from 0 to 1?",
                "options": [
                    "It rises from 1.96 to about 4.8",
                    "It stays at 1.96",
                    "It falls below 1.96",
                    "It becomes infinite"
                ],
                "correctExplanation": "With a larger $b$, $\\hat\\Omega$ is less biased but more variable; the limit $W(1)/\\sqrt{Q(b)}$ has fatter tails, so the critical value rises.",
                "incorrectExplanation": "1.96 is only the limit as $b \\to 0$; the critical value increases with $b$ and stays finite (the $b = 1$ case is the Kiefer–Vogelsang–Bunzel statistic)."
            },
            "ro": {
                "title": "Fixed-b",
                "text": "În asimptotica fixed-b (Kiefer și Vogelsang 2005), raportul $b = S/T$ rămîne fix. Ce se întîmplă cu valoarea critică de 5% a testului $t$ Bartlett cînd $b$ crește de la 0 la 1?",
                "options": [
                    "Crește de la 1,96 la aproximativ 4,8",
                    "Rămîne 1,96",
                    "Scade sub 1,96",
                    "Devine infinită"
                ],
                "correctExplanation": "Cu un $b$ mai mare, $\\hat\\Omega$ este mai puțin deplasat, dar mai variabil; limita $W(1)/\\sqrt{Q(b)}$ are cozi mai groase, deci valoarea critică crește.",
                "incorrectExplanation": "1,96 este doar limita pentru $b \\to 0$; valoarea critică crește cu $b$ și rămîne finită (cazul $b = 1$ este statistica Kiefer–Vogelsang–Bunzel)."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "LLSW recommendations",
                "text": "Which pair matches the recommendations of Lazarus, Lewis, Stock and Watson (2018) for HAR inference?",
                "options": [
                    "NW with $L = \\lfloor 4(T/100)^{2/9}\\rfloor$ and normal critical values",
                    "The truncated kernel with $L = T - 1$",
                    "NW with $S = 1.3\\sqrt{T}$ and fixed-b critical values, or EWC with $\\nu = 0.4T^{2/3}$ and $t_\\nu$ critical values",
                    "White (1980) standard errors with normal critical values"
                ],
                "correctExplanation": "LLSW choose the bandwidth for the test (size–power), with critical values that account for the noise in $\\hat\\Omega$.",
                "incorrectExplanation": "The rule of thumb with normal critical values over-rejects under persistence; the truncated kernel with all lags is degenerate; White errors ignore autocorrelation."
            },
            "ro": {
                "title": "Recomandările LLSW",
                "text": "Ce pereche corespunde recomandărilor Lazarus, Lewis, Stock și Watson (2018) pentru inferența HAR?",
                "options": [
                    "NW cu $L = \\lfloor 4(T/100)^{2/9}\\rfloor$ și valori critice normale",
                    "Nucleul trunchiat cu $L = T - 1$",
                    "NW cu $S = 1,3\\sqrt{T}$ și valori critice fixed-b sau EWC cu $\\nu = 0,4T^{2/3}$ și valori critice $t_\\nu$",
                    "Erori standard White (1980) cu valori critice normale"
                ],
                "correctExplanation": "LLSW aleg lățimea de bandă pentru test (mărime–putere), cu valori critice care țin cont de zgomotul din $\\hat\\Omega$.",
                "incorrectExplanation": "Regula practică cu valori critice normale respinge prea des sub persistență; nucleul trunchiat cu toate decalajele este degenerat; erorile White ignoră autocorelația."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Monte Carlo of size",
                "text": "In the chapter's Monte Carlo (AR(1), $\\phi = 0.9$, $T = 100$), the naive test rejected a true null in 68% of the samples and NW fixed-b in 21%. What is the correct reading?",
                "options": [
                    "Fixed-b is exact",
                    "Fixed-b reduces the distortion a lot, but no method is exact at this persistence and sample size",
                    "The naive test is preferable because it has more power",
                    "The Monte Carlo is wrong because sizes must be 5%"
                ],
                "correctExplanation": "Size is the rejection rate under a true null; fixed-b removes most of the excess, yet the remaining distortion at $\\phi = 0.9$, $T = 100$ is real.",
                "incorrectExplanation": "A test that rejects a true null two thirds of the time has no meaningful power; Monte Carlo sizes differ from 5% precisely when a method is invalid."
            },
            "ro": {
                "title": "Monte Carlo pentru mărime",
                "text": "În studiul Monte Carlo din capitol (AR(1), $\\phi = 0,9$, $T = 100$), testul naiv a respins o ipoteză nulă adevărată în 68% din eșantioane, iar NW fixed-b în 21%. Care este interpretarea corectă?",
                "options": [
                    "Fixed-b este exact",
                    "Fixed-b reduce mult distorsiunea, dar nicio metodă nu este exactă la această persistență și mărime a eșantionului",
                    "Testul naiv este preferabil, pentru că are putere mai mare",
                    "Studiul Monte Carlo este greșit, pentru că mărimile trebuie să fie 5%"
                ],
                "correctExplanation": "Mărimea este rata de respingere sub o ipoteză nulă adevărată; fixed-b elimină cea mai mare parte a excesului, dar distorsiunea rămasă la $\\phi = 0,9$, $T = 100$ este reală.",
                "incorrectExplanation": "Un test care respinge o ipoteză nulă adevărată în două treimi din cazuri nu are o putere cu sens; mărimile Monte Carlo diferă de 5% tocmai cînd o metodă nu este validă."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Monte Carlo error",
                "text": "A Monte Carlo with $R = 5000$ replications estimates a rejection rate of 5%. What is its Monte Carlo standard error?",
                "options": [
                    "About 3 percentage points",
                    "About 0.03 percentage points",
                    "About 0.3 percentage points",
                    "Zero, because the seed is fixed"
                ],
                "correctExplanation": "$\\sqrt{p(1-p)/R} = \\sqrt{0.05 \\cdot 0.95/5000} \\approx 0.0031$.",
                "incorrectExplanation": "Fixing the seed makes the result reproducible, not exact; the binomial standard error $\\sqrt{p(1-p)/R}$ is about 0.31 pp."
            },
            "ro": {
                "title": "Eroarea Monte Carlo",
                "text": "Un studiu Monte Carlo cu $R = 5000$ de replicări estimează o rată de respingere de 5%. Cît este eroarea standard Monte Carlo?",
                "options": [
                    "Aproximativ 3 puncte procentuale",
                    "Aproximativ 0,03 puncte procentuale",
                    "Aproximativ 0,3 puncte procentuale",
                    "Zero, pentru că sămînța este fixată"
                ],
                "correctExplanation": "$\\sqrt{p(1-p)/R} = \\sqrt{0,05 \\cdot 0,95/5000} \\approx 0,0031$.",
                "incorrectExplanation": "Fixarea seminței face rezultatul reproductibil, nu exact; eroarea standard binomială $\\sqrt{p(1-p)/R}$ este de aproximativ 0,31 pp."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The i.i.d. bootstrap",
                "text": "What does Efron's i.i.d. bootstrap of the sample mean estimate when the data are autocorrelated?",
                "options": [
                    "The long-run variance $\\Omega/T$",
                    "Zero",
                    "Twice the long-run variance",
                    "$\\hat\\gamma_0/T$, the naive variance, not the long-run variance"
                ],
                "correctExplanation": "Resampling single observations destroys the dependence: $\\Var^*(\\bar x^*) = \\hat\\gamma_0/T$ (Singh 1981 shows the inconsistency).",
                "incorrectExplanation": "The i.i.d. bootstrap reproduces the naive standard error; to capture $\\Omega$ one must resample blocks."
            },
            "ro": {
                "title": "Bootstrap i.i.d.",
                "text": "Ce estimează bootstrap i.i.d. al lui Efron pentru media de selecție cînd datele sînt autocorelate?",
                "options": [
                    "Varianța de termen lung $\\Omega/T$",
                    "Zero",
                    "Dublul varianței de termen lung",
                    "$\\hat\\gamma_0/T$, varianța naivă, nu varianța de termen lung"
                ],
                "correctExplanation": "Reeșantionarea observațiilor individuale distruge dependența: $\\Var^*(\\bar x^*) = \\hat\\gamma_0/T$ (Singh 1981 arată inconsistența).",
                "incorrectExplanation": "Bootstrap i.i.d. reproduce eroarea standard naivă; pentru a capta $\\Omega$ trebuie reeșantionate blocuri."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Moving blocks and Bartlett",
                "text": "Asymptotically, the variance of the moving-block bootstrap mean with block length $l$ behaves like:",
                "options": [
                    "A truncated-kernel estimate with $L = l$",
                    "A Bartlett (Newey–West) estimate with bandwidth $S = l$",
                    "The naive variance $\\hat\\gamma_0/T$",
                    "A quadratic spectral estimate"
                ],
                "correctExplanation": "Each block of length $l$ contributes the autocovariances up to lag $l-1$ with weights $1 - |j|/l$: the Bartlett weights (Künsch 1989).",
                "incorrectExplanation": "Within a block, lag $j$ appears $l - j$ times, so the weights decline linearly; they are not constant (truncated) and not QS."
            },
            "ro": {
                "title": "Blocuri mobile și Bartlett",
                "text": "Asimptotic, varianța mediei bootstrap pe blocuri mobile cu lungimea blocului $l$ se comportă ca:",
                "options": [
                    "O estimare cu nucleu trunchiat și $L = l$",
                    "O estimare Bartlett (Newey–West) cu lățimea de bandă $S = l$",
                    "Varianța naivă $\\hat\\gamma_0/T$",
                    "O estimare spectrală pătratică"
                ],
                "correctExplanation": "Fiecare bloc de lungime $l$ contribuie cu autocovarianțele pînă la decalajul $l-1$, cu ponderile $1 - |j|/l$: ponderile Bartlett (Künsch 1989).",
                "incorrectExplanation": "Într-un bloc, decalajul $j$ apare de $l - j$ ori, deci ponderile scad liniar; nu sînt constante (trunchiate) și nu sînt QS."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Circular blocks",
                "text": "What is the main advantage of the circular block bootstrap over the moving-block bootstrap?",
                "options": [
                    "Every observation belongs to the same number of blocks, so $E^*\\bar x^* = \\bar x$",
                    "It needs no block length",
                    "It is valid for unit-root processes",
                    "It preserves the dependence across block joints"
                ],
                "correctExplanation": "Wrapping the data on a circle removes the edge effect of the moving-block bootstrap, whose end observations enter fewer blocks.",
                "incorrectExplanation": "A block length is still needed, unit roots break all these methods, and dependence across joints is lost in every block bootstrap."
            },
            "ro": {
                "title": "Blocuri circulare",
                "text": "Care este principalul avantaj al bootstrap-ului circular pe blocuri față de bootstrap pe blocuri mobile?",
                "options": [
                    "Fiecare observație aparține aceluiași număr de blocuri, deci $E^*\\bar x^* = \\bar x$",
                    "Nu necesită o lungime a blocului",
                    "Este valid pentru procese cu rădăcină unitară",
                    "Păstrează dependența de la granițele blocurilor"
                ],
                "correctExplanation": "Așezarea datelor pe un cerc elimină efectul de capăt al bootstrap-ului pe blocuri mobile, la care observațiile de la margini intră în mai puține blocuri.",
                "incorrectExplanation": "Lungimea blocului este tot necesară, rădăcinile unitare invalidează toate aceste metode, iar dependența de la granițe se pierde la orice bootstrap pe blocuri."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Stationary bootstrap",
                "text": "In the stationary bootstrap of Politis and Romano (1994), block lengths are:",
                "options": [
                    "geometric with mean $1/p$, so the resampled series is stationary",
                    "fixed and equal to $T^{1/3}$",
                    "uniform between 1 and $T$",
                    "chosen to maximise the bootstrap variance"
                ],
                "correctExplanation": "At each step the block continues with probability $1-p$ or restarts at a random point with probability $p$; with wrapping, the resample is stationary conditional on the data.",
                "incorrectExplanation": "Fixed blocks define the moving-block and circular bootstraps; the block length is chosen to minimise the MSE (Politis–White), not to maximise the variance."
            },
            "ro": {
                "title": "Bootstrap staționar",
                "text": "În bootstrap staționar al lui Politis și Romano (1994), lungimile blocurilor sînt:",
                "options": [
                    "geometrice cu media $1/p$, deci seria reeșantionată este staționară",
                    "fixe și egale cu $T^{1/3}$",
                    "uniforme între 1 și $T$",
                    "alese astfel încît să maximizeze varianța bootstrap"
                ],
                "correctExplanation": "La fiecare pas blocul continuă cu probabilitatea $1-p$ sau reîncepe într-un punct aleator cu probabilitatea $p$; cu înfășurare, reeșantionarea este staționară condiționat de date.",
                "incorrectExplanation": "Blocurile fixe definesc bootstrap pe blocuri mobile și cel circular; lungimea blocului se alege pentru a minimiza eroarea pătratică medie (Politis–White), nu pentru a maximiza varianța."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Wild bootstrap",
                "text": "For which problem is the wild bootstrap (residuals multiplied by i.i.d. signs) NOT valid?",
                "options": [
                    "An AR(1) with GARCH errors",
                    "A cross-section regression with heteroskedastic errors",
                    "A regression of 4-quarter-ahead growth with overlapping observations",
                    "A regression whose scores are a martingale difference sequence"
                ],
                "correctExplanation": "Overlap creates MA(3) errors; the i.i.d. multipliers destroy that autocorrelation, so the bootstrap variance is too small.",
                "incorrectExplanation": "The wild bootstrap keeps heteroskedasticity and is valid whenever the scores are uncorrelated: GARCH-type errors (Gonçalves and Kilian 2004), cross sections, martingale differences."
            },
            "ro": {
                "title": "Wild bootstrap",
                "text": "Pentru ce problemă NU este valid wild bootstrap (reziduuri înmulțite cu semne i.i.d.)?",
                "options": [
                    "Un AR(1) cu erori GARCH",
                    "O regresie transversală cu erori heteroscedastice",
                    "O regresie a creșterii pe patru trimestre înainte, cu observații suprapuse",
                    "O regresie ale cărei scoruri sînt o secvență de diferențe de martingală"
                ],
                "correctExplanation": "Suprapunerea creează erori MA(3); multiplicatorii i.i.d. distrug această autocorelație, deci varianța bootstrap este prea mică.",
                "incorrectExplanation": "Wild bootstrap păstrează heteroscedasticitatea și este valid cînd scorurile sînt necorelate: erori de tip GARCH (Gonçalves și Kilian 2004), date transversale, diferențe de martingală."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Overlapping observations",
                "text": "Quarterly growth over the next $h = 4$ quarters is regressed on the term spread. Under the null of no predictability and white-noise quarterly growth, the regression errors are:",
                "options": [
                    "white noise",
                    "AR(1) with $\\phi = 0.75$",
                    "a random walk",
                    "MA(3)"
                ],
                "correctExplanation": "Consecutive dependent variables share three quarters, so $u_t$ and $u_{t-j}$ are correlated for $j \\le 3$ and uncorrelated beyond: an MA($h-1$).",
                "incorrectExplanation": "Overlap creates a moving average of order $h - 1 = 3$; it is not white noise, and the correlation cuts off after lag 3 instead of decaying geometrically."
            },
            "ro": {
                "title": "Observații suprapuse",
                "text": "Creșterea trimestrială pe următoarele $h = 4$ trimestre este regresată pe marja la termen. Sub ipoteza nulă fără predictibilitate și cu creșteri trimestriale de tip zgomot alb, erorile regresiei sînt:",
                "options": [
                    "zgomot alb",
                    "AR(1) cu $\\phi = 0,75$",
                    "un mers aleator",
                    "MA(3)"
                ],
                "correctExplanation": "Variabilele dependente consecutive au trei trimestre comune, deci $u_t$ și $u_{t-j}$ sînt corelate pentru $j \\le 3$ și necorelate dincolo de acest decalaj: un MA($h-1$).",
                "incorrectExplanation": "Suprapunerea creează o medie mobilă de ordinul $h - 1 = 3$; nu este zgomot alb, iar corelația se oprește după decalajul 3, în loc să scadă geometric."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Spurious regression",
                "text": "Two independent random walks ($T = 50$) are regressed on each other. Our replication of Granger and Newbold (1974) gives $|t| > 2$ in 66% of the cases with OLS and 54% with Newey–West standard errors. Why does HAC not fix the problem?",
                "options": [
                    "Because the Newey–West bandwidth was too small",
                    "The $t$-statistic diverges under a unit root: the problem is the regression, not the standard error",
                    "Because the errors are heteroskedastic",
                    "HAC fixes it with enough lags"
                ],
                "correctExplanation": "Phillips (1986): in a spurious regression the $t$-statistic diverges at rate $\\sqrt{T}$; no consistent estimator of a finite $\\Omega$ exists for the residuals, which are I(1). Differencing restores the size.",
                "incorrectExplanation": "Larger bandwidths reduce but cannot remove the over-rejection, because the residuals have a unit root; heteroskedasticity is not the issue."
            },
            "ro": {
                "title": "Regresia falsă",
                "text": "Două mersuri aleatoare independente ($T = 50$) sînt regresate unul pe celălalt. Replicarea noastră a lucrării Granger și Newbold (1974) dă $|t| > 2$ în 66% din cazuri cu MCMMP și în 54% cu erori standard Newey–West. De ce nu rezolvă HAC problema?",
                "options": [
                    "Pentru că lățimea de bandă Newey–West a fost prea mică",
                    "Statistica $t$ diverge sub o rădăcină unitară: problema este regresia, nu eroarea standard",
                    "Pentru că erorile sînt heteroscedastice",
                    "HAC o rezolvă cu suficiente decalaje"
                ],
                "correctExplanation": "Phillips (1986): într-o regresie falsă statistica $t$ diverge cu viteza $\\sqrt{T}$; reziduurile sînt I(1), deci nu există un $\\Omega$ finit de estimat. Diferențierea readuce mărimea corectă.",
                "incorrectExplanation": "Lățimi de bandă mai mari reduc, dar nu pot elimina respingerile excesive, pentru că reziduurile au o rădăcină unitară; heteroscedasticitatea nu este problema."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Family-wise error",
                "text": "A researcher tests 20 independent useless predictors at 5% each and reports the best one. What is the probability of at least one false rejection?",
                "options": [
                    "5%",
                    "About 20%",
                    "100%",
                    "About 64%"
                ],
                "correctExplanation": "$1 - 0.95^{20} \\approx 0.64$; Bonferroni would test each at $0.05/20 = 0.0025$.",
                "incorrectExplanation": "Each test has a 5% false-rejection probability; with 20 independent tests the chance that none rejects is $0.95^{20} \\approx 0.36$."
            },
            "ro": {
                "title": "Eroarea la nivelul familiei de teste",
                "text": "Un cercetător testează 20 de predictori independenți și inutili, fiecare la 5%, și îl raportează pe cel mai bun. Care este probabilitatea a cel puțin unei respingeri false?",
                "options": [
                    "5%",
                    "Aproximativ 20%",
                    "100%",
                    "Aproximativ 64%"
                ],
                "correctExplanation": "$1 - 0,95^{20} \\approx 0,64$; Bonferroni ar testa fiecare predictor la $0,05/20 = 0,0025$.",
                "incorrectExplanation": "Fiecare test are o probabilitate de respingere falsă de 5%; cu 20 de teste independente, șansa ca niciunul să nu respingă este $0,95^{20} \\approx 0,36$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The Reality Check",
                "text": "In White's (2000) Reality Check, how is the null distribution of $\\max_k \\sqrt{n}\\,\\bar f_k$ obtained?",
                "options": [
                    "From the standard normal distribution",
                    "By a stationary bootstrap of the whole vector of performance differences, recentred at the sample means",
                    "By Bonferroni-adjusting each $p$-value",
                    "By an i.i.d. bootstrap of each rule separately"
                ],
                "correctExplanation": "Resampling the vector $f_t$ jointly keeps the correlation across rules and over time; recentring imposes the least favourable null $E f_k = 0$.",
                "incorrectExplanation": "The maximum of correlated statistics is not normal; Bonferroni ignores the correlation; resampling each rule separately destroys the cross-rule dependence that the test exploits."
            },
            "ro": {
                "title": "Testul Reality Check",
                "text": "În testul Reality Check al lui White (2000), cum se obține distribuția sub ipoteza nulă a lui $\\max_k \\sqrt{n}\\,\\bar f_k$?",
                "options": [
                    "Din distribuția Normală standard",
                    "Prin bootstrap staționar al întregului vector al diferențelor de performanță, recentrat în mediile de selecție",
                    "Prin ajustarea Bonferroni a fiecărei valori $p$",
                    "Printr-un bootstrap i.i.d. al fiecărei reguli separat"
                ],
                "correctExplanation": "Reeșantionarea comună a vectorului $f_t$ păstrează corelația dintre reguli și în timp; recentrarea impune ipoteza nulă cea mai puțin favorabilă, $E f_k = 0$.",
                "incorrectExplanation": "Maximul unor statistici corelate nu urmează distribuția Normală; Bonferroni ignoră corelația; reeșantionarea separată a fiecărei reguli distruge dependența dintre reguli pe care testul o folosește."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant wrote: \"(i) Newey–West standard errors are always larger than OLS ones; (ii) the circular block bootstrap removes the edge bias of the moving-block bootstrap; (iii) for overlapping $h$-step forecasts the errors are MA($h-1$).\" Which statement is wrong?",
                "options": [
                    "(i)",
                    "(ii)",
                    "(iii)",
                    "None of them"
                ],
                "correctExplanation": "With negative autocorrelation the HAC standard error is smaller than the naive one (S&P 500 returns in this chapter); (ii) and (iii) are correct.",
                "incorrectExplanation": "Statement (ii) is the defining property of the circular bootstrap and (iii) follows from the overlap; only (i) is false."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI a scris: „(i) Erorile standard Newey–West sînt întotdeauna mai mari decît cele MCMMP; (ii) bootstrap circular pe blocuri elimină deplasarea de capăt a bootstrap-ului pe blocuri mobile; (iii) pentru prognoze suprapuse pe $h$ pași, erorile sînt MA($h-1$).” Ce afirmație este greșită?",
                "options": [
                    "(i)",
                    "(ii)",
                    "(iii)",
                    "Niciuna"
                ],
                "correctExplanation": "Cu autocorelație negativă, eroarea standard HAC este mai mică decît cea naivă (randamentele S&P 500 din acest capitol); (ii) și (iii) sînt corecte.",
                "incorrectExplanation": "Afirmația (ii) este proprietatea definitorie a bootstrap-ului circular, iar (iii) rezultă din suprapunere; doar (i) este falsă."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer (2)",
                "text": "Asked to test whether Romanian inflation averaged 2.5% since 2013 (monthly annual rates, $\\hat\\rho_1 \\approx 0.99$), an AI assistant proposed a Newey–West $t$-test with $\\lfloor 4(T/100)^{2/9}\\rfloor$ lags and normal critical values. What is the main problem?",
                "options": [
                    "Newey–West cannot be used for means",
                    "The test should use the median instead of the mean",
                    "At this persistence the test over-rejects badly; even fixed-b and EWC tests are far from 5%",
                    "There is no problem: $T = 164$ is large"
                ],
                "correctExplanation": "In the chapter's calibrated Monte Carlo this test rejects a true null in about 79% of the samples; near unit roots defeat kernel and EWC tests (Müller 2014).",
                "incorrectExplanation": "Newey–West is designed precisely for means and regression coefficients; the issue is persistence, which makes the rule-of-thumb bandwidth and normal critical values invalid at $T = 164$."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI (2)",
                "text": "Rugat să testeze dacă inflația din România a fost în medie 2,5% din 2013 (rate anuale lunare, $\\hat\\rho_1 \\approx 0,99$), un asistent AI a propus un test $t$ Newey–West cu $\\lfloor 4(T/100)^{2/9}\\rfloor$ decalaje și valori critice normale. Care este problema principală?",
                "options": [
                    "Newey–West nu poate fi folosit pentru medii",
                    "Testul ar trebui să folosească mediana în loc de medie",
                    "La această persistență testul respinge mult prea des; chiar și testele fixed-b și EWC sînt departe de 5%",
                    "Nu există nicio problemă: $T = 164$ este mare"
                ],
                "correctExplanation": "În studiul Monte Carlo calibrat din capitol, acest test respinge o ipoteză nulă adevărată în aproximativ 79% din eșantioane; rădăcinile aproape unitare invalidează testele cu nucleu și EWC (Müller 2014).",
                "incorrectExplanation": "Newey–West este construit tocmai pentru medii și coeficienți de regresie; problema este persistența, care face invalide regula practică și valorile critice normale la $T = 164$."
            }
        }
    ]
};
