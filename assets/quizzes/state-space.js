// ============================================================
// Chapter 6 quiz bank: State space models and Bayesian filtering (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['state-space'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Big-kappa initialisation",
                "text": "A local level model is initialised with $P_1 = \\kappa$ and all $n$ likelihood terms are kept. As $\\kappa$ grows, the log-likelihood",
                "options": [
                    "falls without bound, because the first term contains $-\\frac12\\ln\\kappa$",
                    "converges to the exact diffuse log-likelihood",
                    "is unchanged, because $\\kappa$ only affects the first state",
                    "rises without bound, because $F_1$ grows"
                ],
                "correctExplanation": "With $P_1 = \\kappa$, $F_1 = \\kappa + \\sigma^2_\\varepsilon$, so the first term behaves like $-\\frac12\\ln\\kappa$; the exact diffuse likelihood drops this term.",
                "incorrectExplanation": "Only the first prediction-error variance grows with $\\kappa$; its log enters with a minus sign, so the total falls by $\\frac12\\ln 10$ per decade of $\\kappa$."
            },
            "ro": {
                "title": "Inițializarea big kappa",
                "text": "Un model local level este inițializat cu $P_1 = \\kappa$ și se păstrează toți cei $n$ termeni ai verosimilității. Cînd $\\kappa$ crește, log-verosimilitatea",
                "options": [
                    "scade nelimitat, pentru că primul termen conține $-\\frac12\\ln\\kappa$",
                    "converge către log-verosimilitatea difuză exactă",
                    "nu se schimbă, pentru că $\\kappa$ afectează doar prima stare",
                    "crește nelimitat, pentru că $F_1$ crește"
                ],
                "correctExplanation": "Cu $P_1 = \\kappa$, $F_1 = \\kappa + \\sigma^2_\\varepsilon$, deci primul termen se comportă ca $-\\frac12\\ln\\kappa$; verosimilitatea difuză exactă elimină acest termen.",
                "incorrectExplanation": "Doar prima varianță a erorii de predicție crește cu $\\kappa$; logaritmul ei intră cu semnul minus, deci totalul scade cu $\\frac12\\ln 10$ la fiecare ordin de mărime al lui $\\kappa$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Diffuse steps",
                "text": "For a local linear trend model (level and slope both diffuse) with no missing observations, the exact diffuse filter needs",
                "options": [
                    "one diffuse step, $d = 1$",
                    "two diffuse steps, $d = 2$",
                    "no diffuse step, because the slope is stationary",
                    "$n$ diffuse steps"
                ],
                "correctExplanation": "Each observation identifies one linear combination of the diffuse states; two states need two observations before $P_{\\infty,t} = 0$.",
                "incorrectExplanation": "Both the level and the slope are random walks without a stationary distribution; two observations are needed to pin them down."
            },
            "ro": {
                "title": "Pașii difuzi",
                "text": "Pentru un model local linear trend (nivelul și panta ambele difuze), fără observații lipsă, filtrul difuz exact are nevoie de",
                "options": [
                    "un pas difuz, $d = 1$",
                    "doi pași difuzi, $d = 2$",
                    "niciun pas difuz, pentru că panta este staționară",
                    "$n$ pași difuzi"
                ],
                "correctExplanation": "Fiecare observație identifică o combinație liniară a stărilor difuze; două stări au nevoie de două observații pînă cînd $P_{\\infty,t} = 0$.",
                "incorrectExplanation": "Atît nivelul, cît și panta sînt mersuri aleatoare fără distribuție staționară; sînt necesare două observații pentru a le fixa."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Kalman gain",
                "text": "In the notation $a_{t+1} = Ta_t + K_tv_t$, the Kalman gain is",
                "options": [
                    "$K_t = P_tZ'F_t$",
                    "$K_t = TP_tZ'F_t^{-1}$",
                    "$K_t = F_t^{-1}Z P_t T'$",
                    "$K_t = T P_t T' + RQR'$"
                ],
                "correctExplanation": "The gain is the covariance of the next state with the innovation, $TP_tZ'$, times the inverse innovation variance.",
                "incorrectExplanation": "The gain must scale the innovation by the inverse of its variance $F_t$ and map it through the transition matrix."
            },
            "ro": {
                "title": "Cîștigul Kalman",
                "text": "În notația $a_{t+1} = Ta_t + K_tv_t$, cîștigul Kalman este",
                "options": [
                    "$K_t = P_tZ'F_t$",
                    "$K_t = TP_tZ'F_t^{-1}$",
                    "$K_t = F_t^{-1}Z P_t T'$",
                    "$K_t = T P_t T' + RQR'$"
                ],
                "correctExplanation": "Cîștigul este covarianța stării următoare cu inovația, $TP_tZ'$, înmulțită cu inversa varianței inovației.",
                "incorrectExplanation": "Cîștigul trebuie să scaleze inovația cu inversa varianței ei $F_t$ și să o transmită prin matricea de tranziție."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Without normality",
                "text": "If the errors of a linear state space model are not Gaussian but have finite variances, the Kalman filter",
                "options": [
                    "gives the exact conditional mean of the state",
                    "is biased and must not be used",
                    "still gives the minimum-MSE linear predictor of the state",
                    "gives the exact likelihood"
                ],
                "correctExplanation": "The recursions only use first and second moments: they deliver the best linear predictor; normality adds exactness of the conditional mean and of the likelihood.",
                "incorrectExplanation": "Linearity of the projections does not need normality; what is lost is the exact conditional distribution, hence the exact likelihood."
            },
            "ro": {
                "title": "Fără normalitate",
                "text": "Dacă erorile unui model liniar în spațiul stărilor nu sînt gaussiene, dar au varianțe finite, filtrul Kalman",
                "options": [
                    "dă media condiționată exactă a stării",
                    "este deplasat și nu trebuie folosit",
                    "dă în continuare predictorul liniar cu eroare pătratică medie minimă al stării",
                    "dă verosimilitatea exactă"
                ],
                "correctExplanation": "Recursiile folosesc doar momentele de ordinul unu și doi: ele dau cel mai bun predictor liniar; normalitatea adaugă exactitatea mediei condiționate și a verosimilității.",
                "incorrectExplanation": "Liniaritatea proiecțiilor nu cere normalitate; se pierde distribuția condiționată exactă, deci și verosimilitatea exactă."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Pile-up",
                "text": "In a local level model with true $q = \\sigma^2_\\eta/\\sigma^2_\\varepsilon = 0.01$ and $T = 100$, the ML estimate of $q$",
                "options": [
                    "is never exactly zero, because $q > 0$",
                    "is always positive and unbiased",
                    "equals exactly zero in a non-negligible share of samples",
                    "is zero only if the sample is shorter than 50"
                ],
                "correctExplanation": "Pile-up (Shephard and Harvey 1990): the likelihood is often maximised at the boundary even when the variance is positive.",
                "incorrectExplanation": "The score at $q = 0$ is often negative, so the maximum sits on the boundary with positive probability for small true $q$."
            },
            "ro": {
                "title": "Pile-up",
                "text": "Într-un model local level cu $q = \\sigma^2_\\eta/\\sigma^2_\\varepsilon = 0{,}01$ adevărat și $T = 100$, estimația ML a lui $q$",
                "options": [
                    "nu este niciodată exact zero, pentru că $q > 0$",
                    "este întotdeauna pozitivă și nedeplasată",
                    "este exact zero într-o proporție deloc neglijabilă a eșantioanelor",
                    "este zero doar dacă eșantionul are mai puțin de 50 de observații"
                ],
                "correctExplanation": "Pile-up (Shephard și Harvey 1990): verosimilitatea are adesea maximul pe frontieră chiar dacă varianța este pozitivă.",
                "incorrectExplanation": "Scorul în $q = 0$ este adesea negativ, deci maximul se află pe frontieră cu probabilitate pozitivă pentru $q$ mic."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Testing a constant coefficient",
                "text": "To test $H_0$: $\\sigma^2_b = 0$ for a random-walk coefficient in a TVP regression, the most reliable approach is",
                "options": [
                    "a parametric bootstrap of the LR statistic under the restricted model",
                    "the $\\chi^2_1$ distribution of the LR statistic",
                    "a $t$-test of $\\hat\\sigma^2_b$ with the Hessian standard error",
                    "a rolling-window regression"
                ],
                "correctExplanation": "The null is on the boundary and the alternative is nonstationary, so the LR law is nonstandard; simulating it under the null is robust.",
                "incorrectExplanation": "Boundary nulls invalidate both the $\\chi^2_1$ limit and Hessian standard errors; rolling windows confuse sampling noise with time variation."
            },
            "ro": {
                "title": "Testarea unui coeficient constant",
                "text": "Pentru a testa $H_0$: $\\sigma^2_b = 0$ pentru un coeficient de tip mers aleator într-o regresie TVP, abordarea cea mai fiabilă este",
                "options": [
                    "un bootstrap parametric al statisticii LR sub modelul restricționat",
                    "distribuția $\\chi^2_1$ a statisticii LR",
                    "un test $t$ pentru $\\hat\\sigma^2_b$ cu eroarea standard din hessiană",
                    "o regresie pe ferestre mobile"
                ],
                "correctExplanation": "Ipoteza nulă se află pe frontieră, iar alternativa este nestaționară, deci legea LR este nestandard; simularea ei sub ipoteza nulă este robustă.",
                "incorrectExplanation": "Ipotezele nule pe frontieră invalidează atît limita $\\chi^2_1$, cît și erorile standard din hessiană; ferestrele mobile confundă zgomotul de eșantionare cu variația în timp."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Simulation smoother",
                "text": "The Durbin--Koopman (2002) simulation smoother produces a draw from $p(\\alpha | y)$ as",
                "options": [
                    "$\\hat\\alpha(y) + $ i.i.d. noise with variance $P_t$",
                    "a backward pass that draws $\\alpha_t$ given $\\alpha_{t+1}$",
                    "$\\alpha^+ + \\hat\\alpha(y - y^+)$, with $(\\alpha^+, y^+)$ simulated from the model",
                    "$\\hat\\alpha(y^+)$ only"
                ],
                "correctExplanation": "Gaussianity makes $\\alpha - \\hat\\alpha(y)$ independent of $y$ with a fixed law; one smoother pass on $y - y^+$ corrects the simulated path.",
                "incorrectExplanation": "The draw needs the joint simulation of states and observations and one smoother pass on their difference; backward sampling is the Carter--Kohn method."
            },
            "ro": {
                "title": "Simulation smoother",
                "text": "Simulation smoother-ul Durbin--Koopman (2002) produce o extragere din $p(\\alpha | y)$ ca",
                "options": [
                    "$\\hat\\alpha(y) + $ zgomot i.i.d. cu varianța $P_t$",
                    "o trecere înapoi care extrage $\\alpha_t$ dat $\\alpha_{t+1}$",
                    "$\\alpha^+ + \\hat\\alpha(y - y^+)$, cu $(\\alpha^+, y^+)$ simulate din model",
                    "doar $\\hat\\alpha(y^+)$"
                ],
                "correctExplanation": "Gaussianitatea face ca $\\alpha - \\hat\\alpha(y)$ să fie independent de $y$, cu o lege fixă; o singură trecere a netezitorului pe $y - y^+$ corectează traiectoria simulată.",
                "incorrectExplanation": "Extragerea cere simularea comună a stărilor și a observațiilor și o trecere a netezitorului pe diferența lor; eșantionarea înapoi este metoda Carter--Kohn."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Backward sampling",
                "text": "In forward filtering backward sampling, the conditional mean of $\\alpha_t$ given $\\alpha_{t+1}$ and $Y_t$ uses",
                "options": [
                    "the smoothed moments $\\hat\\alpha_t$ and $V_t$",
                    "only the observation $y_{t+1}$",
                    "the predicted moments $a_t$ and $P_t$ only",
                    "the filtered moments $a_{t|t}$, $P_{t|t}$ and the drawn $\\alpha_{t+1}$"
                ],
                "correctExplanation": "By the Markov property, future data enter only through $\\alpha_{t+1}$; the lemma combines it with the filtered moments.",
                "incorrectExplanation": "Smoothed moments would count the future data twice; the predicted moments ignore $y_t$."
            },
            "ro": {
                "title": "Eșantionarea înapoi",
                "text": "În filtrarea înainte cu eșantionare înapoi, media condiționată a lui $\\alpha_t$ dat $\\alpha_{t+1}$ și $Y_t$ folosește",
                "options": [
                    "momentele netezite $\\hat\\alpha_t$ și $V_t$",
                    "doar observația $y_{t+1}$",
                    "doar momentele prezise $a_t$ și $P_t$",
                    "momentele filtrate $a_{t|t}$, $P_{t|t}$ și valoarea extrasă $\\alpha_{t+1}$"
                ],
                "correctExplanation": "Din proprietatea Markov, datele viitoare intră doar prin $\\alpha_{t+1}$; lema îl combină cu momentele filtrate.",
                "incorrectExplanation": "Momentele netezite ar număra de două ori datele viitoare; momentele prezise ignoră $y_t$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Precision sampler",
                "text": "For a random-walk state with time-varying variances, the precision sampler is fast because",
                "options": [
                    "it avoids the Gaussian assumption",
                    "it samples one $\\alpha_t$ at a time",
                    "the posterior precision matrix is banded, so a banded Cholesky factor costs $O(n)$",
                    "the covariance matrix of the states is diagonal"
                ],
                "correctExplanation": "Random-walk increments give a tridiagonal precision; solving and sampling with a banded factor is linear in $n$.",
                "incorrectExplanation": "The speed comes from the band structure of the precision (not of the covariance, which is dense), and the whole path is drawn at once."
            },
            "ro": {
                "title": "Eșantionarea pe baza preciziei",
                "text": "Pentru o stare de tip mers aleator cu varianțe variabile în timp, eșantionarea pe baza matricei de precizie este rapidă pentru că",
                "options": [
                    "evită ipoteza de normalitate",
                    "extrage cîte un $\\alpha_t$",
                    "matricea de precizie a posteriori este în bandă, deci un factor Cholesky în bandă costă $O(n)$",
                    "matricea de covarianță a stărilor este diagonală"
                ],
                "correctExplanation": "Incrementele mersului aleator dau o precizie tridiagonală; rezolvarea și extragerea cu un factor în bandă sînt liniare în $n$.",
                "incorrectExplanation": "Viteza vine din structura în bandă a preciziei (nu a covarianței, care este plină), iar întreaga traiectorie se extrage deodată."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "SV and GARCH",
                "text": "The key difference between stochastic volatility and GARCH(1,1) is that in SV",
                "options": [
                    "the variance depends on past squared returns",
                    "returns cannot have excess kurtosis",
                    "the likelihood has a closed form",
                    "the variance has its own shock, so it is not known given past returns"
                ],
                "correctExplanation": "GARCH variance is a function of past returns; SV log-variance is a latent AR(1) with its own innovation, so the likelihood is an integral.",
                "incorrectExplanation": "In SV even Gaussian errors produce excess kurtosis, and the likelihood has no closed form; dependence on past squared returns is the GARCH mechanism."
            },
            "ro": {
                "title": "SV și GARCH",
                "text": "Diferența esențială dintre volatilitatea stochastică și GARCH(1,1) este că în SV",
                "options": [
                    "varianța depinde de pătratele randamentelor trecute",
                    "randamentele nu pot avea exces de boltire",
                    "verosimilitatea are formă închisă",
                    "varianța are propriul șoc, deci nu este cunoscută date randamentele trecute"
                ],
                "correctExplanation": "Varianța GARCH este o funcție de randamentele trecute; logaritmul varianței SV este un AR(1) latent cu propria inovație, deci verosimilitatea este o integrală.",
                "incorrectExplanation": "În SV chiar și erorile gaussiene produc exces de boltire, iar verosimilitatea nu are formă închisă; dependența de pătratele randamentelor trecute este mecanismul GARCH."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "SV kurtosis",
                "text": "In an SV model with Gaussian $\\epsilon_t$ and unconditional variance of the log-variance $\\sigma^2_h = \\ln 2$, the kurtosis of $y_t$ is",
                "options": [
                    "3",
                    "$3\\ln 2$",
                    "4.5",
                    "6"
                ],
                "correctExplanation": "Kurtosis $= 3\\exp(\\sigma^2_h) = 3\\cdot 2 = 6$.",
                "incorrectExplanation": "Use $\\E y^4/(\\E y^2)^2 = 3\\E e^{2h}/(\\E e^h)^2 = 3e^{\\sigma^2_h}$."
            },
            "ro": {
                "title": "Coeficientul de boltire SV",
                "text": "Într-un model SV cu $\\epsilon_t$ gaussian și varianța necondiționată a logaritmului varianței $\\sigma^2_h = \\ln 2$, coeficientul de boltire al lui $y_t$ este",
                "options": [
                    "3",
                    "$3\\ln 2$",
                    "4,5",
                    "6"
                ],
                "correctExplanation": "Coeficientul de boltire $= 3\\exp(\\sigma^2_h) = 3\\cdot 2 = 6$.",
                "incorrectExplanation": "Folosiți $\\E y^4/(\\E y^2)^2 = 3\\E e^{2h}/(\\E e^h)^2 = 3e^{\\sigma^2_h}$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Log chi-square noise",
                "text": "In $\\ln y_t^2 = h_t + \\ln\\epsilon_t^2$ with $\\epsilon_t \\sim N(0, 1)$, the noise $\\ln\\epsilon_t^2$ has",
                "options": [
                    "mean 0 and variance 1",
                    "mean about $-1.27$, variance $\\pi^2/2$ and a long left tail",
                    "mean 1 and variance 2, symmetric",
                    "mean about $-1.27$ and variance 1, symmetric"
                ],
                "correctExplanation": "$\\ln\\chi^2_1$ has mean $-1.2704$, variance $\\pi^2/2 \\approx 4.93$ and is skewed to the left (small returns give very negative logs).",
                "incorrectExplanation": "The log of a $\\chi^2_1$ variable is neither standard nor symmetric: near-zero values of $\\epsilon_t$ produce a long left tail."
            },
            "ro": {
                "title": "Zgomotul log chi-pătrat",
                "text": "În $\\ln y_t^2 = h_t + \\ln\\epsilon_t^2$ cu $\\epsilon_t \\sim N(0, 1)$, zgomotul $\\ln\\epsilon_t^2$ are",
                "options": [
                    "media 0 și varianța 1",
                    "media aproximativ $-1{,}27$, varianța $\\pi^2/2$ și o coadă lungă la stînga",
                    "media 1 și varianța 2, simetric",
                    "media aproximativ $-1{,}27$ și varianța 1, simetric"
                ],
                "correctExplanation": "$\\ln\\chi^2_1$ are media $-1{,}2704$, varianța $\\pi^2/2 \\approx 4{,}93$ și este asimetric la stînga (randamentele mici dau logaritmi foarte negativi).",
                "incorrectExplanation": "Logaritmul unei variabile $\\chi^2_1$ nu este nici standard, nici simetric: valorile lui $\\epsilon_t$ apropiate de zero produc o coadă lungă la stînga."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "KSC mixture",
                "text": "The seven-component mixture of Kim, Shephard and Chib (1998) is used because",
                "options": [
                    "it makes the returns Gaussian",
                    "it removes the need for a prior on $\\phi$",
                    "it turns SV into GARCH",
                    "given the component indicators, the model is linear Gaussian, so the whole log-volatility path can be drawn in one block"
                ],
                "correctExplanation": "Conditioning on the indicators makes $\\ln y_t^2$ a linear Gaussian model with known time-varying variances: a simulation or precision sampler draws $h_{1:n}$ at once.",
                "incorrectExplanation": "The mixture approximates the $\\ln\\chi^2_1$ noise; it does not change the return distribution, the priors or the model class."
            },
            "ro": {
                "title": "Mixtura KSC",
                "text": "Mixtura cu șapte componente din Kim, Shephard și Chib (1998) se folosește pentru că",
                "options": [
                    "face randamentele gaussiene",
                    "elimină nevoia unei distribuții a priori pentru $\\phi$",
                    "transformă SV în GARCH",
                    "dați indicatorii componentelor, modelul este liniar gaussian, deci întreaga traiectorie a logaritmului volatilității se extrage într-un bloc"
                ],
                "correctExplanation": "Condiționarea pe indicatori face din $\\ln y_t^2$ un model liniar gaussian cu varianțe cunoscute, variabile în timp: un simulation smoother sau eșantionarea pe baza preciziei extrage $h_{1:n}$ deodată.",
                "incorrectExplanation": "Mixtura aproximează zgomotul $\\ln\\chi^2_1$; nu schimbă distribuția randamentelor, distribuțiile a priori sau clasa de modele."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "EKF in the SV model",
                "text": "An extended Kalman filter applied directly to $y_t = \\exp(h_t/2)\\epsilon_t$ fails because",
                "options": [
                    "$\\partial\\E(y_t | h_t)/\\partial h_t = 0$, so the gain is zero",
                    "the Jacobian does not exist",
                    "the state equation is nonlinear",
                    "the filter diverges to infinity"
                ],
                "correctExplanation": "The conditional mean of $y_t$ is zero for every $h_t$; linearisation keeps no information about $h_t$, which sits in $y_t^2$.",
                "incorrectExplanation": "The state equation is linear and the Jacobian exists; it is simply zero, so the filter never updates."
            },
            "ro": {
                "title": "EKF în modelul SV",
                "text": "Un filtru Kalman extins aplicat direct lui $y_t = \\exp(h_t/2)\\epsilon_t$ eșuează pentru că",
                "options": [
                    "$\\partial\\E(y_t | h_t)/\\partial h_t = 0$, deci cîștigul este zero",
                    "iacobianul nu există",
                    "ecuația stării este neliniară",
                    "filtrul diverge la infinit"
                ],
                "correctExplanation": "Media condiționată a lui $y_t$ este zero pentru orice $h_t$; liniarizarea nu păstrează nicio informație despre $h_t$, care se află în $y_t^2$.",
                "incorrectExplanation": "Ecuația stării este liniară, iar iacobianul există; el este pur și simplu zero, deci filtrul nu se actualizează niciodată."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Unscented transform",
                "text": "For an $n$-dimensional Gaussian state, the basic unscented transform uses",
                "options": [
                    "$n$ sigma points",
                    "$2n + 1$ sigma points",
                    "$n^2$ sigma points",
                    "thousands of random particles"
                ],
                "correctExplanation": "One central point plus a pair along each axis of the scaled square root of the covariance.",
                "incorrectExplanation": "The points are deterministic, symmetric around the mean: one at the mean and two per dimension."
            },
            "ro": {
                "title": "Transformarea unscented",
                "text": "Pentru o stare gaussiană $n$-dimensională, transformarea unscented de bază folosește",
                "options": [
                    "$n$ puncte sigma",
                    "$2n + 1$ puncte sigma",
                    "$n^2$ puncte sigma",
                    "mii de particule aleatoare"
                ],
                "correctExplanation": "Un punct central plus o pereche de-a lungul fiecărei axe a rădăcinii pătrate scalate a covarianței.",
                "incorrectExplanation": "Punctele sînt deterministe, simetrice în jurul mediei: unul în medie și cîte două pe dimensiune."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Particle likelihood",
                "text": "The bootstrap particle filter estimate $\\hat L(\\psi)$ of the likelihood is",
                "options": [
                    "unbiased on the log scale",
                    "biased upwards for any $N$",
                    "exact for $N \\ge 100$",
                    "unbiased for $L(\\psi)$, while $\\ln\\hat L$ is biased downwards"
                ],
                "correctExplanation": "$\\E\\hat L = L$ for any $N$ (Del Moral 2004); by Jensen $\\E\\ln\\hat L < \\ln L$, by about half the variance of $\\ln\\hat L$.",
                "incorrectExplanation": "Unbiasedness holds in levels only; the log of an unbiased estimator is biased downwards and no finite $N$ makes it exact."
            },
            "ro": {
                "title": "Verosimilitatea din filtrul de particule",
                "text": "Estimația $\\hat L(\\psi)$ a verosimilității din filtrul de particule bootstrap este",
                "options": [
                    "nedeplasată pe scala logaritmică",
                    "deplasată în sus pentru orice $N$",
                    "exactă pentru $N \\ge 100$",
                    "nedeplasată pentru $L(\\psi)$, în timp ce $\\ln\\hat L$ este deplasat în jos"
                ],
                "correctExplanation": "$\\E\\hat L = L$ pentru orice $N$ (Del Moral 2004); din Jensen, $\\E\\ln\\hat L < \\ln L$, cu aproximativ jumătate din varianța lui $\\ln\\hat L$.",
                "incorrectExplanation": "Nedeplasarea are loc doar în nivel; logaritmul unui estimator nedeplasat este deplasat în jos, iar niciun $N$ finit nu îl face exact."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Effective sample size",
                "text": "With normalised weights $W^{(i)}$, the effective sample size of a particle system is",
                "options": [
                    "$\\sum_i W^{(i)}$",
                    "$1/\\sum_i(W^{(i)})^2$",
                    "$N\\max_iW^{(i)}$",
                    "the number of distinct particles before resampling"
                ],
                "correctExplanation": "It equals $N$ for equal weights and 1 when one particle has all the weight.",
                "incorrectExplanation": "The sum of normalised weights is always one; the formula must penalise unequal weights."
            },
            "ro": {
                "title": "Mărimea efectivă a eșantionului",
                "text": "Cu ponderile normalizate $W^{(i)}$, mărimea efectivă a eșantionului unui sistem de particule este",
                "options": [
                    "$\\sum_i W^{(i)}$",
                    "$1/\\sum_i(W^{(i)})^2$",
                    "$N\\max_iW^{(i)}$",
                    "numărul de particule distincte înainte de reeșantionare"
                ],
                "correctExplanation": "Este egală cu $N$ pentru ponderi egale și cu 1 cînd o singură particulă are toată ponderea.",
                "incorrectExplanation": "Suma ponderilor normalizate este întotdeauna unu; formula trebuie să penalizeze ponderile inegale."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Number of particles in PMMH",
                "text": "In particle marginal Metropolis--Hastings, a common rule chooses the number of particles $N$ so that",
                "options": [
                    "the variance of $\\ln\\hat L$ at the posterior mean is about 1 to 2",
                    "$N$ equals the sample size",
                    "the acceptance rate is 100\\%",
                    "$\\ln\\hat L$ has zero variance"
                ],
                "correctExplanation": "Too few particles make the chain stick after lucky overestimates; too many waste computation (Pitt et al. 2012; Doucet et al. 2015).",
                "incorrectExplanation": "Zero variance needs infinitely many particles; the optimum balances mixing against cost per iteration."
            },
            "ro": {
                "title": "Numărul de particule în PMMH",
                "text": "În particle marginal Metropolis--Hastings, o regulă uzuală alege numărul de particule $N$ astfel încît",
                "options": [
                    "varianța lui $\\ln\\hat L$ la media a posteriori să fie aproximativ între 1 și 2",
                    "$N$ să fie egal cu mărimea eșantionului",
                    "rata de acceptare să fie 100\\%",
                    "$\\ln\\hat L$ să aibă varianță zero"
                ],
                "correctExplanation": "Prea puține particule blochează lanțul după supraestimări norocoase; prea multe irosesc calculul (Pitt et al. 2012; Doucet et al. 2015).",
                "incorrectExplanation": "Varianța zero cere o infinitate de particule; optimul echilibrează amestecarea și costul pe iterație."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Auxiliary particle filter",
                "text": "The auxiliary particle filter of Pitt and Shephard (1999) improves on the bootstrap filter by",
                "options": [
                    "resampling the previous particles with weights that use $g(y_t | \\mu_t)$ before propagating",
                    "using more particles",
                    "never resampling",
                    "replacing the measurement density by a Gaussian"
                ],
                "correctExplanation": "Looking ahead at $y_t$ moves the particles towards regions that explain the new observation, which matters most for outliers.",
                "incorrectExplanation": "The gain does not come from more particles or from approximating the model; it comes from first-stage weights based on the next observation."
            },
            "ro": {
                "title": "Filtrul de particule auxiliar",
                "text": "Filtrul de particule auxiliar al lui Pitt și Shephard (1999) îmbunătățește filtrul bootstrap prin",
                "options": [
                    "reeșantionarea particulelor anterioare cu ponderi care folosesc $g(y_t | \\mu_t)$, înainte de propagare",
                    "folosirea mai multor particule",
                    "renunțarea la reeșantionare",
                    "înlocuirea densității de măsurare cu una gaussiană"
                ],
                "correctExplanation": "Privirea înainte la $y_t$ mută particulele spre regiunile care explică noua observație, ceea ce contează mai ales pentru valorile extreme.",
                "incorrectExplanation": "Cîștigul nu vine din mai multe particule sau din aproximarea modelului, ci din ponderile din prima etapă, bazate pe observația următoare."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Morley, Nelson and Zivot",
                "text": "Morley, Nelson and Zivot (2003) show for US GDP that",
                "options": [
                    "the HP filter and BN coincide",
                    "with correlated trend and cycle shocks, the UC cycle equals the Beveridge--Nelson cycle of an ARIMA(2,1,2)",
                    "the correlation is identified with an AR(1) cycle",
                    "the UC0 cycle is the correct one"
                ],
                "correctExplanation": "Freeing $\\rho$ (identified with an AR(2) cycle) makes the UC model observationally equivalent to the ARIMA(2,1,2) and the filtered cycle equal to BN; $\\hat\\rho$ is close to $-1$.",
                "incorrectExplanation": "The large, smooth UC0 cycle comes from the restriction $\\rho = 0$; an AR(1) cycle does not identify $\\rho$."
            },
            "ro": {
                "title": "Morley, Nelson și Zivot",
                "text": "Morley, Nelson și Zivot (2003) arată pentru PIB-ul SUA că",
                "options": [
                    "filtrul HP și BN coincid",
                    "cu șocuri corelate ale trendului și ciclului, ciclul UC coincide cu ciclul Beveridge--Nelson al unui ARIMA(2,1,2)",
                    "corelația este identificată cu un ciclu AR(1)",
                    "ciclul UC0 este cel corect"
                ],
                "correctExplanation": "Eliberarea lui $\\rho$ (identificat cu un ciclu AR(2)) face modelul UC echivalent observațional cu ARIMA(2,1,2), iar ciclul filtrat egal cu ciclul BN; $\\hat\\rho$ este apropiat de $-1$.",
                "incorrectExplanation": "Ciclul UC0 mare și neted provine din restricția $\\rho = 0$; un ciclu AR(1) nu identifică $\\rho$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Beveridge--Nelson cycle",
                "text": "If $\\Delta y_t - \\mu = 0.5(\\Delta y_{t-1} - \\mu) + e_t$ and this quarter $\\Delta y_t - \\mu = 1$, the BN cycle is",
                "options": [
                    "$-1$",
                    "$1$",
                    "$-0.5$",
                    "$2$"
                ],
                "correctExplanation": "$c_t = -\\frac{\\phi}{1-\\phi}(\\Delta y_t - \\mu) = -\\frac{0.5}{0.5}\\cdot 1 = -1$.",
                "incorrectExplanation": "The trend adds all expected future excess growth, $\\phi/(1-\\phi)$ times today's; the cycle is output minus trend, hence negative."
            },
            "ro": {
                "title": "Ciclul Beveridge--Nelson",
                "text": "Dacă $\\Delta y_t - \\mu = 0{,}5(\\Delta y_{t-1} - \\mu) + e_t$, iar în acest trimestru $\\Delta y_t - \\mu = 1$, ciclul BN este",
                "options": [
                    "$-1$",
                    "$1$",
                    "$-0{,}5$",
                    "$2$"
                ],
                "correctExplanation": "$c_t = -\\frac{\\phi}{1-\\phi}(\\Delta y_t - \\mu) = -\\frac{0{,}5}{0{,}5}\\cdot 1 = -1$.",
                "incorrectExplanation": "Trendul adaugă toată creșterea suplimentară viitoare așteptată, de $\\phi/(1-\\phi)$ ori cea de azi; ciclul este producția minus trendul, deci negativ."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "UC-SV tuning",
                "text": "In the UC-SV model of Stock and Watson (2007), the parameter $\\gamma$ is",
                "options": [
                    "the estimated trend inflation",
                    "the MA coefficient of the reduced form",
                    "the variance of the transitory shock",
                    "the fixed variance of the log-volatility shocks; a larger $\\gamma$ lets the volatilities move faster"
                ],
                "correctExplanation": "SW fix $\\gamma = 0.2$; it governs the speed of change of both volatilities, and conclusions about trend shifts can depend on it.",
                "incorrectExplanation": "$\\gamma$ is not a state or a reduced-form coefficient; the transitory variance is itself time varying."
            },
            "ro": {
                "title": "Calibrarea UC-SV",
                "text": "În modelul UC-SV al lui Stock și Watson (2007), parametrul $\\gamma$ este",
                "options": [
                    "inflația de trend estimată",
                    "coeficientul MA al formei reduse",
                    "varianța șocului tranzitoriu",
                    "varianța fixată a șocurilor logaritmului volatilității; un $\\gamma$ mai mare permite volatilităților să se miște mai repede"
                ],
                "correctExplanation": "SW fixează $\\gamma = 0{,}2$; el guvernează viteza de schimbare a ambelor volatilități, iar concluziile despre deplasarea trendului pot depinde de el.",
                "incorrectExplanation": "$\\gamma$ nu este o stare și nici un coeficient al formei reduse; varianța tranzitorie este ea însăși variabilă în timp."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: ``Rolling 12-quarter OLS slopes of Romanian on euro-area inflation range from $-0.5$ to $1.6$, which proves that the link is unstable.'' The error is that",
                "options": [
                    "OLS cannot be used with inflation data",
                    "the slopes should be between 0 and 1 by definition",
                    "short windows produce large sampling noise; time variation must be tested, e.g. by a boundary LR test with a bootstrap",
                    "rolling windows always understate time variation"
                ],
                "correctExplanation": "In the lecture the TVP regression gives an almost constant slope and the bootstrap LR test does not reject a constant coefficient.",
                "incorrectExplanation": "Nothing forbids slopes outside $[0, 1]$; the issue is that the dispersion of rolling estimates mixes noise with genuine change."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Pantele OLS mobile pe 12 trimestre ale inflației din România pe inflația din zona euro variază între $-0{,}5$ și $1{,}6$, ceea ce demonstrează că legătura este instabilă.” Eroarea este că",
                "options": [
                    "OLS nu se poate folosi pentru date de inflație",
                    "pantele ar trebui să fie între 0 și 1 prin definiție",
                    "ferestrele scurte produc zgomot mare de eșantionare; variația în timp trebuie testată, de exemplu printr-un test LR la frontieră cu bootstrap",
                    "ferestrele mobile subestimează întotdeauna variația în timp"
                ],
                "correctExplanation": "În curs, regresia TVP dă o pantă aproape constantă, iar testul LR bootstrap nu respinge un coeficient constant.",
                "incorrectExplanation": "Nimic nu interzice pante în afara intervalului $[0, 1]$; problema este că dispersia estimațiilor mobile amestecă zgomotul cu schimbarea reală."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant recommends: ``Estimate the SV parameters by maximising the bootstrap particle-filter log-likelihood with BFGS.'' The main problem is that",
                "options": [
                    "particle filters cannot evaluate SV likelihoods",
                    "BFGS needs at least 100 parameters",
                    "$\\ln\\hat L(\\psi)$ is noisy and not smooth in $\\psi$ because of resampling, so gradient methods fail; use it inside PMMH or with common random numbers and smooth resampling",
                    "the SV likelihood has a closed form, so no filter is needed"
                ],
                "correctExplanation": "Resampling makes the estimate discontinuous in $\\psi$; the pseudo-marginal MCMC uses it exactly as it is.",
                "incorrectExplanation": "The particle filter does estimate the SV likelihood, which has no closed form; the issue is the roughness of the estimate as a function of $\\psi$."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI recomandă: „Estimați parametrii SV maximizînd cu BFGS log-verosimilitatea din filtrul de particule bootstrap.” Problema principală este că",
                "options": [
                    "filtrele de particule nu pot evalua verosimilitatea SV",
                    "BFGS are nevoie de cel puțin 100 de parametri",
                    "$\\ln\\hat L(\\psi)$ este zgomotos și nu este neted în $\\psi$ din cauza reeșantionării, deci metodele de gradient eșuează; folosiți-l în PMMH sau cu numere aleatoare comune și reeșantionare netedă",
                    "verosimilitatea SV are formă închisă, deci nu este nevoie de filtru"
                ],
                "correctExplanation": "Reeșantionarea face estimația discontinuă în $\\psi$; MCMC-ul pseudo-marginal o folosește exact așa cum este.",
                "incorrectExplanation": "Filtrul de particule chiar estimează verosimilitatea SV, care nu are formă închisă; problema este asperitatea estimației ca funcție de $\\psi$."
            }
        }
    ]
};
