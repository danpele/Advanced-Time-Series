// ============================================================
// Chapter 10 quiz bank: Long memory and rough volatility (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['long-memory'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Spectral pole and autocorrelations",
                "text": "A stationary process has $f(\\lambda) \\sim G\\lambda^{-2d}$ as $\\lambda \\to 0^+$ with $0 < d < 1/2$ and regularly behaved autocovariances. How do its autocorrelations decay?",
                "options": [
                    "Like $c\\,k^{2d-1}$",
                    "Like $c\\,\\phi^k$ for some $|\\phi| < 1$",
                    "Like $c\\,k^{-2d}$",
                    "Like $c\\,k^{-d-1}$"
                ],
                "correctExplanation": "The Abelian--Tauberian link pairs a pole $\\lambda^{-2d}$ with hyperbolic decay $k^{2d-1}$, which is not summable for $d > 0$.",
                "incorrectExplanation": "Geometric decay belongs to ARMA processes, and $k^{-d-1}$ is the decay of the fractional differencing weights, not of the autocorrelations."
            },
            "ro": {
                "title": "Polul spectral și autocorelațiile",
                "text": "Un proces staționar are $f(\\lambda) \\sim G\\lambda^{-2d}$ cînd $\\lambda \\to 0^+$, cu $0 < d < 1/2$ și autocovarianțe regulate. Cum scad autocorelațiile lui?",
                "options": [
                    "Ca $c\\,k^{2d-1}$",
                    "Ca $c\\,\\phi^k$ pentru un $|\\phi| < 1$",
                    "Ca $c\\,k^{-2d}$",
                    "Ca $c\\,k^{-d-1}$"
                ],
                "correctExplanation": "Legătura abeliană--tauberiană asociază polului $\\lambda^{-2d}$ descreșterea hiperbolică $k^{2d-1}$, nesumabilă pentru $d > 0$.",
                "incorrectExplanation": "Descreșterea geometrică aparține proceselor ARMA, iar $k^{-d-1}$ este descreșterea ponderilor diferențierii fracționare, nu a autocorelațiilor."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "First autocorrelation of ARFIMA",
                "text": "What is $\\rho(1)$ of an ARFIMA$(0, d, 0)$ process with $|d| < 1/2$?",
                "options": [
                    "$d$",
                    "$d/(1 - d)$",
                    "$1 - d$",
                    "$d^2$"
                ],
                "correctExplanation": "The recursion $\\rho(k) = \\rho(k - 1)(k - 1 + d)/(k - d)$ with $\\rho(0) = 1$ gives $\\rho(1) = d/(1 - d)$.",
                "incorrectExplanation": "The other expressions do not follow from the Hosking autocorrelation formula; for $d = 0.4$ the correct value is $2/3$."
            },
            "ro": {
                "title": "Prima autocorelație ARFIMA",
                "text": "Cît este $\\rho(1)$ pentru un proces ARFIMA$(0, d, 0)$ cu $|d| < 1/2$?",
                "options": [
                    "$d$",
                    "$d/(1 - d)$",
                    "$1 - d$",
                    "$d^2$"
                ],
                "correctExplanation": "Recursia $\\rho(k) = \\rho(k - 1)(k - 1 + d)/(k - d)$ cu $\\rho(0) = 1$ dă $\\rho(1) = d/(1 - d)$.",
                "incorrectExplanation": "Celelalte expresii nu rezultă din formula autocorelațiilor lui Hosking; pentru $d = 0{,}4$ valoarea corectă este $2/3$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Variance of the sample mean",
                "text": "Under long memory with $0 < d < 1/2$, the variance of the sample mean $\\bar X_n$ is of order:",
                "options": [
                    "$n^{-1}$",
                    "$n^{-1/2}$",
                    "$n^{2d-1}$",
                    "$n^{-2d}$"
                ],
                "correctExplanation": "Summing $\\gamma(k) \\sim ck^{2d-1}$ in $\\Var(\\bar X_n) = n^{-1}\\sum_{|k|<n}(1 - |k|/n)\\gamma(k)$ gives order $n^{2d-1}$, slower than $n^{-1}$.",
                "incorrectExplanation": "The rate $n^{-1}$ holds only for summable autocovariances; the other rates do not match the hyperbolic sum."
            },
            "ro": {
                "title": "Varianța mediei de eșantion",
                "text": "Sub memorie lungă cu $0 < d < 1/2$, varianța mediei de eșantion $\\bar X_n$ este de ordinul:",
                "options": [
                    "$n^{-1}$",
                    "$n^{-1/2}$",
                    "$n^{2d-1}$",
                    "$n^{-2d}$"
                ],
                "correctExplanation": "Însumînd $\\gamma(k) \\sim ck^{2d-1}$ în $\\Var(\\bar X_n) = n^{-1}\\sum_{|k|<n}(1 - |k|/n)\\gamma(k)$ obținem ordinul $n^{2d-1}$, mai lent decît $n^{-1}$.",
                "incorrectExplanation": "Viteza $n^{-1}$ este valabilă doar pentru autocovarianțe sumabile; celelalte viteze nu corespund sumei hiperbolice."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Aggregation",
                "text": "Granger (1980) aggregates independent AR(1) series whose squared coefficients follow a Beta$(p, q)$ distribution, $1 < q < 2$. What memory parameter does the aggregate have?",
                "options": [
                    "$d = q/2$",
                    "$d = 1 - p$",
                    "$d = p/2$",
                    "$d = 1 - q/2$"
                ],
                "correctExplanation": "The aggregate autocovariance behaves like $k^{-(q-1)}$; matching $k^{2d-1}$ gives $d = 1 - q/2$.",
                "incorrectExplanation": "Only the mass of coefficients near one, governed by $q$, matters at long lags; $p$ affects the short lags."
            },
            "ro": {
                "title": "Agregarea",
                "text": "Granger (1980) agregă serii AR(1) independente cu pătratele coeficienților din distribuția Beta$(p, q)$, $1 < q < 2$. Ce parametru de memorie are agregatul?",
                "options": [
                    "$d = q/2$",
                    "$d = 1 - p$",
                    "$d = p/2$",
                    "$d = 1 - q/2$"
                ],
                "correctExplanation": "Autocovarianța agregatului se comportă ca $k^{-(q-1)}$; identificînd cu $k^{2d-1}$ obținem $d = 1 - q/2$.",
                "incorrectExplanation": "La laguri mari contează doar masa coeficienților apropiați de unu, determinată de $q$; $p$ influențează lagurile mici."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Local Whittle variance",
                "text": "Under the conditions of Robinson (1995), what is the asymptotic variance of $\\sqrt m(\\hat d_{LW} - d)$?",
                "options": [
                    "$1/4$",
                    "$\\pi^2/24$",
                    "$\\pi^2/6$",
                    "$1$"
                ],
                "correctExplanation": "The score is a weighted sum of $\\xi_j - 1$ with unit variance and the Hessian tends to 4, so the variance is $4/16 = 1/4$.",
                "incorrectExplanation": "The value $\\pi^2/24$ belongs to GPH, whose errors are $\\log\\xi_j$ with variance $\\pi^2/6$."
            },
            "ro": {
                "title": "Varianța local Whittle",
                "text": "În condițiile lui Robinson (1995), care este varianța asimptotică a lui $\\sqrt m(\\hat d_{LW} - d)$?",
                "options": [
                    "$1/4$",
                    "$\\pi^2/24$",
                    "$\\pi^2/6$",
                    "$1$"
                ],
                "correctExplanation": "Scorul este o sumă ponderată de $\\xi_j - 1$ cu varianța unu, iar hessiana tinde la 4, deci varianța este $4/16 = 1/4$.",
                "incorrectExplanation": "Valoarea $\\pi^2/24$ aparține estimatorului GPH, ale cărui erori sînt $\\log\\xi_j$, cu varianța $\\pi^2/6$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Where $\\pi^2/24$ comes from",
                "text": "Why is the asymptotic variance of the GPH estimator $\\pi^2/(24m)$?",
                "options": [
                    "Because the regressor $\\log\\lambda_j$ has variance 24",
                    "Because $\\Var\\log\\xi_j = \\pi^2/6$ for $\\xi_j \\sim$ Exp(1) and the centred regressor $-2\\log\\lambda_j$ has sum of squares about $4m$",
                    "Because GPH maximises a Gaussian likelihood",
                    "Because the periodogram is Normal"
                ],
                "correctExplanation": "OLS variance equals the error variance $\\pi^2/6$ divided by the sum of squares of the centred regressor, about $4m$.",
                "incorrectExplanation": "GPH is a regression, not a likelihood estimator, and the periodogram ordinates are approximately exponential, not Normal."
            },
            "ro": {
                "title": "De unde vine $\\pi^2/24$",
                "text": "De ce este varianța asimptotică a estimatorului GPH egală cu $\\pi^2/(24m)$?",
                "options": [
                    "Pentru că regresorul $\\log\\lambda_j$ are varianța 24",
                    "Pentru că $\\Var\\log\\xi_j = \\pi^2/6$ pentru $\\xi_j \\sim$ Exp(1), iar regresorul centrat $-2\\log\\lambda_j$ are suma pătratelor de circa $4m$",
                    "Pentru că GPH maximizează o verosimilitate gaussiană",
                    "Pentru că periodograma are distribuția Normală"
                ],
                "correctExplanation": "Varianța OLS este varianța erorii, $\\pi^2/6$, împărțită la suma pătratelor regresorului centrat, circa $4m$.",
                "incorrectExplanation": "GPH este o regresie, nu un estimator de verosimilitate, iar ordonatele periodogramei sînt aproximativ exponențiale, nu din distribuția Normală."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Local Whittle beyond the unit root",
                "text": "What happens to the (untapered) local Whittle estimator when the true $d$ is 1.2?",
                "options": [
                    "It is consistent and asymptotically Normal",
                    "It is consistent but non-Normal",
                    "It converges in probability to 1",
                    "It diverges to infinity"
                ],
                "correctExplanation": "Phillips and Shimotsu (2004): for $d > 1$ local Whittle converges to 1; exact local Whittle fixes this.",
                "incorrectExplanation": "Consistency holds only for $d < 1$ and normality for $d < 3/4$."
            },
            "ro": {
                "title": "Local Whittle dincolo de rădăcina unitară",
                "text": "Ce se întîmplă cu estimatorul local Whittle (fără fereastră) cînd $d$ adevărat este 1,2?",
                "options": [
                    "Este consistent și asimptotic normal",
                    "Este consistent, dar nu normal",
                    "Converge în probabilitate la 1",
                    "Diverge la infinit"
                ],
                "correctExplanation": "Phillips și Shimotsu (2004): pentru $d > 1$, local Whittle converge la 1; local Whittle exact corectează aceasta.",
                "incorrectExplanation": "Consistența are loc doar pentru $d < 1$, iar normalitatea pentru $d < 3/4$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Unknown mean in exact local Whittle",
                "text": "How does Shimotsu (2010) treat the unknown mean in exact local Whittle estimation?",
                "options": [
                    "He always subtracts the sample mean",
                    "He always subtracts the median",
                    "He always subtracts the first observation",
                    "He subtracts a weighted mean of $\\bar X$ and $X_1$: the sample mean for $d \\le 1/2$, the first observation for $d \\ge 3/4$"
                ],
                "correctExplanation": "The sample mean estimates the level poorly when $d > 1/2$, while $X_1$ is a good estimate of the initial level there; the weight switches smoothly.",
                "incorrectExplanation": "A single fixed choice fails in one of the two regimes of $d$."
            },
            "ro": {
                "title": "Media necunoscută în local Whittle exact",
                "text": "Cum tratează Shimotsu (2010) media necunoscută în estimarea local Whittle exactă?",
                "options": [
                    "Scade întotdeauna media de eșantion",
                    "Scade întotdeauna mediana",
                    "Scade întotdeauna prima observație",
                    "Scade o medie ponderată între $\\bar X$ și $X_1$: media de eșantion pentru $d \\le 1/2$, prima observație pentru $d \\ge 3/4$"
                ],
                "correctExplanation": "Media de eșantion estimează prost nivelul cînd $d > 1/2$, iar acolo $X_1$ estimează bine nivelul inițial; ponderea trece lin de la una la alta.",
                "incorrectExplanation": "O singură alegere fixă eșuează într-unul dintre cele două regimuri ale lui $d$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Bandwidth bias",
                "text": "For ARFIMA$(1, d, 0)$ with $\\phi > 0$, what is the leading bias of GPH and local Whittle?",
                "options": [
                    "Upward, growing like $(m/n)^2$",
                    "Downward, shrinking like $m^{-1/2}$",
                    "Zero for every $m$",
                    "Upward, growing like $\\log m$"
                ],
                "correctExplanation": "The bias is $-\\frac{2\\pi^2}{9}\\frac{f^{*\\prime\\prime}(0)}{f^*(0)}(m/n)^2$ and $f^{*\\prime\\prime}(0) < 0$ when $\\phi > 0$.",
                "incorrectExplanation": "The term $m^{-1/2}$ is the standard deviation, not the bias; a positive AR root adds low-frequency power that looks like memory."
            },
            "ro": {
                "title": "Deplasarea lățimii de bandă",
                "text": "Pentru ARFIMA$(1, d, 0)$ cu $\\phi > 0$, care este deplasarea principală a estimatorilor GPH și local Whittle?",
                "options": [
                    "În sus, crescînd ca $(m/n)^2$",
                    "În jos, scăzînd ca $m^{-1/2}$",
                    "Zero pentru orice $m$",
                    "În sus, crescînd ca $\\log m$"
                ],
                "correctExplanation": "Deplasarea este $-\\frac{2\\pi^2}{9}\\frac{f^{*\\prime\\prime}(0)}{f^*(0)}(m/n)^2$, iar $f^{*\\prime\\prime}(0) < 0$ cînd $\\phi > 0$.",
                "incorrectExplanation": "Termenul $m^{-1/2}$ este abaterea standard, nu deplasarea; o rădăcină AR pozitivă adaugă putere la frecvențe joase care seamănă cu memoria."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Optimal bandwidth",
                "text": "Balancing a bias of order $(m/n)^2$ against a variance $1/(4m)$, the MSE-optimal bandwidth is of order:",
                "options": [
                    "$n^{1/2}$",
                    "$n^{4/5}$",
                    "$n$",
                    "$\\log n$"
                ],
                "correctExplanation": "Minimising $C^2(m/n)^4 + 1/(4m)$ gives $m^* = (n^4/(16C^2))^{1/5}$, of order $n^{4/5}$.",
                "incorrectExplanation": "The rate $n^{1/2}$ is a common rule of thumb, not the MSE optimum under a $\\lambda^2$ expansion."
            },
            "ro": {
                "title": "Lățimea de bandă optimă",
                "text": "Echilibrînd o deplasare de ordinul $(m/n)^2$ cu o varianță $1/(4m)$, lățimea de bandă optimă în MSE este de ordinul:",
                "options": [
                    "$n^{1/2}$",
                    "$n^{4/5}$",
                    "$n$",
                    "$\\log n$"
                ],
                "correctExplanation": "Minimizînd $C^2(m/n)^4 + 1/(4m)$ obținem $m^* = (n^4/(16C^2))^{1/5}$, de ordinul $n^{4/5}$.",
                "incorrectExplanation": "Viteza $n^{1/2}$ este o regulă empirică obișnuită, nu optimul MSE sub o dezvoltare în $\\lambda^2$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Level-shift signature",
                "text": "For short memory plus rare random level shifts, how does the local Whittle estimate $\\hat d(m)$ behave as the bandwidth grows?",
                "options": [
                    "It stays flat",
                    "It increases",
                    "It falls steeply",
                    "It oscillates around $1/2$"
                ],
                "correctExplanation": "Level shifts create a $\\lambda^{-2}$ region only at the lowest frequencies; adding higher frequencies brings in the flat short-memory part (Perron and Qu 2010).",
                "incorrectExplanation": "A flat profile is the signature of genuine long memory, and an increasing one of positive short-run autocorrelation."
            },
            "ro": {
                "title": "Semnătura salturilor de nivel",
                "text": "Pentru memorie scurtă plus salturi aleatoare rare de nivel, cum se comportă estimația local Whittle $\\hat d(m)$ cînd crește lățimea de bandă?",
                "options": [
                    "Rămîne plată",
                    "Crește",
                    "Scade abrupt",
                    "Oscilează în jurul lui $1/2$"
                ],
                "correctExplanation": "Salturile de nivel creează o zonă $\\lambda^{-2}$ doar la frecvențele cele mai joase; frecvențele mai înalte aduc partea plată de memorie scurtă (Perron și Qu 2010).",
                "incorrectExplanation": "Un profil plat este semnătura memoriei lungi reale, iar unul crescător a autocorelației pozitive de termen scurt."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Reading the Qu test",
                "text": "The Qu (2011) statistic exceeds its 1% critical value. What can you conclude?",
                "options": [
                    "That $d = 0$",
                    "That the series has structural breaks",
                    "That $d > 1/2$",
                    "That the data are inconsistent with stationary long memory; level shifts, breaks or trends are candidate explanations"
                ],
                "correctExplanation": "The null is stationary long memory; rejection points to alternatives such as level shifts, breaks or trends, without proving one of them.",
                "incorrectExplanation": "The test does not estimate $d$ and does not identify which alternative generated the data."
            },
            "ro": {
                "title": "Interpretarea testului Qu",
                "text": "Statistica Qu (2011) depășește valoarea critică de 1\\%. Ce puteți concluziona?",
                "options": [
                    "Că $d = 0$",
                    "Că seria are rupturi structurale",
                    "Că $d > 1/2$",
                    "Că datele nu sînt compatibile cu memoria lungă staționară; salturile de nivel, rupturile sau trendurile sînt explicații posibile"
                ],
                "correctExplanation": "Ipoteza nulă este memoria lungă staționară; respingerea indică alternative precum salturile de nivel, rupturile sau trendurile, fără a o demonstra pe vreuna.",
                "incorrectExplanation": "Testul nu estimează $d$ și nu identifică alternativa care a generat datele."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "FCVAR rank tests",
                "text": "In the FCVAR of Johansen and Nielsen (2012), when is the LR trace test for the cointegration rank asymptotically $\\chi^2$?",
                "options": [
                    "When $b < 1/2$",
                    "When $b > 1/2$",
                    "Only when $d = b = 1$",
                    "Always"
                ],
                "correctExplanation": "For $b < 1/2$ the limit is $\\chi^2_{(p-r)^2}$; for $b > 1/2$ it is a fractional Dickey--Fuller distribution (MacKinnon and Nielsen 2014).",
                "incorrectExplanation": "With $d = b = 1$ the model is the VECM, whose trace test has the non-standard Johansen distribution."
            },
            "ro": {
                "title": "Testele de rang FCVAR",
                "text": "În FCVAR al lui Johansen și Nielsen (2012), cînd este testul trace LR pentru rangul de cointegrare asimptotic $\\chi^2$?",
                "options": [
                    "Cînd $b < 1/2$",
                    "Cînd $b > 1/2$",
                    "Doar cînd $d = b = 1$",
                    "Întotdeauna"
                ],
                "correctExplanation": "Pentru $b < 1/2$ limita este $\\chi^2_{(p-r)^2}$; pentru $b > 1/2$ este o distribuție Dickey--Fuller fracționară (MacKinnon și Nielsen 2014).",
                "incorrectExplanation": "Cu $d = b = 1$ modelul este VECM, al cărui test trace are distribuția nestandard Johansen."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "FIGARCH variance",
                "text": "What is the unconditional variance of returns in a FIGARCH(1, $d$, 1) model with $0 < d < 1$?",
                "options": [
                    "Finite if $d < 1/2$",
                    "Infinite, because the ARCH($\\infty$) weights sum to one",
                    "Finite if $\\beta < d$",
                    "$\\omega/(1 - \\beta)$"
                ],
                "correctExplanation": "At $L = 1$ the polynomial $(1 - L)^d$ vanishes, so $\\sum_k\\lambda_k = 1$ and $\\E\\varepsilon_t^2 = \\infty$; the process is strictly but not covariance stationary.",
                "incorrectExplanation": "HYGARCH with amplitude below one restores a finite variance; $\\omega/(1 - \\beta)$ is only the intercept of the ARCH($\\infty$) form."
            },
            "ro": {
                "title": "Varianța FIGARCH",
                "text": "Care este varianța necondiționată a randamentelor într-un model FIGARCH(1, $d$, 1) cu $0 < d < 1$?",
                "options": [
                    "Finită dacă $d < 1/2$",
                    "Infinită, pentru că ponderile ARCH($\\infty$) au suma unu",
                    "Finită dacă $\\beta < d$",
                    "$\\omega/(1 - \\beta)$"
                ],
                "correctExplanation": "În $L = 1$ polinomul $(1 - L)^d$ se anulează, deci $\\sum_k\\lambda_k = 1$ și $\\E\\varepsilon_t^2 = \\infty$; procesul este staționar strict, dar nu în covarianță.",
                "incorrectExplanation": "HYGARCH cu amplitudine sub unu redă o varianță finită; $\\omega/(1 - \\beta)$ este doar termenul liber al formei ARCH($\\infty$)."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Noise in $\\log r_t^2$",
                "text": "In a long-memory stochastic volatility model, how does the noise $\\log\\eta_t^2$ in $\\log r_t^2$ affect the local Whittle estimate of $d$?",
                "options": [
                    "It biases $\\hat d$ upward",
                    "It has no effect",
                    "It biases $\\hat d$ downward, because its flat spectrum flattens the low-frequency slope",
                    "It makes $\\hat d$ negative"
                ],
                "correctExplanation": "The spectrum is $G\\lambda^{-2d} + \\sigma_\\xi^2/(2\\pi)$; the noise term flattens the slope, which the estimator of Hurvich, Moulines and Soulier (2005) corrects.",
                "incorrectExplanation": "The noise is i.i.d., so it cannot add memory; it attenuates, not reverses, the estimate."
            },
            "ro": {
                "title": "Zgomotul din $\\log r_t^2$",
                "text": "Într-un model de volatilitate stochastică cu memorie lungă, cum afectează zgomotul $\\log\\eta_t^2$ din $\\log r_t^2$ estimația local Whittle a lui $d$?",
                "options": [
                    "Deplasează $\\hat d$ în sus",
                    "Nu are niciun efect",
                    "Deplasează $\\hat d$ în jos, pentru că spectrul lui plat aplatizează panta de frecvență joasă",
                    "Face $\\hat d$ negativ"
                ],
                "correctExplanation": "Spectrul este $G\\lambda^{-2d} + \\sigma_\\xi^2/(2\\pi)$; termenul de zgomot aplatizează panta, iar estimatorul lui Hurvich, Moulines și Soulier (2005) o corectează.",
                "incorrectExplanation": "Zgomotul este i.i.d., deci nu poate adăuga memorie; el atenuează estimația, nu îi schimbă semnul."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "What HAR is",
                "text": "Which description of the HAR model of Corsi (2009) is correct?",
                "options": [
                    "An ARFIMA model with $d$ estimated by OLS",
                    "A genuine long-memory process",
                    "A nonlinear threshold model",
                    "A restricted AR(22), formally short memory, that approximates long memory over horizons up to a few months"
                ],
                "correctExplanation": "Daily, weekly and monthly averages impose a step pattern on 22 AR coefficients; the implied ACF decays geometrically beyond a few months.",
                "incorrectExplanation": "HAR is linear, estimated by OLS, and has summable autocorrelations."
            },
            "ro": {
                "title": "Ce este HAR",
                "text": "Care descriere a modelului HAR al lui Corsi (2009) este corectă?",
                "options": [
                    "Un model ARFIMA cu $d$ estimat prin OLS",
                    "Un proces autentic cu memorie lungă",
                    "Un model neliniar cu prag",
                    "Un AR(22) restricționat, formal cu memorie scurtă, care aproximează memoria lungă pe orizonturi de pînă la cîteva luni"
                ],
                "correctExplanation": "Mediile zilnice, săptămînale și lunare impun un tipar în trepte celor 22 de coeficienți AR; ACF implicată scade geometric după cîteva luni.",
                "incorrectExplanation": "HAR este liniar, estimat prin OLS, și are autocorelații sumabile."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Rough increments",
                "text": "What is the lag-one autocorrelation of fractional Gaussian noise with $H = 0.1$?",
                "options": [
                    "$2^{2H-1} - 1 \\approx -0.43$",
                    "0",
                    "$+0.43$",
                    "$-0.1$"
                ],
                "correctExplanation": "For fGn $\\rho(1) = \\frac12(2^{2H} - 2) = 2^{2H-1} - 1$, which is about $-0.43$ for $H = 0.1$.",
                "incorrectExplanation": "Zero is the Brownian case $H = 1/2$; positive values require $H > 1/2$."
            },
            "ro": {
                "title": "Creșteri neregulate",
                "text": "Care este autocorelația de ordinul unu a zgomotului gaussian fracționar cu $H = 0{,}1$?",
                "options": [
                    "$2^{2H-1} - 1 \\approx -0{,}43$",
                    "0",
                    "$+0{,}43$",
                    "$-0{,}1$"
                ],
                "correctExplanation": "Pentru fGn, $\\rho(1) = \\frac12(2^{2H} - 2) = 2^{2H-1} - 1$, circa $-0{,}43$ pentru $H = 0{,}1$.",
                "incorrectExplanation": "Zero corespunde cazului brownian $H = 1/2$; valorile pozitive cer $H > 1/2$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The scaling exponent",
                "text": "If log volatility has fBm-like Gaussian increments with Hurst exponent $H$, how does the slope $\\zeta_q$ of $\\log m(q, \\Delta)$ on $\\log\\Delta$ depend on $q$?",
                "options": [
                    "$\\zeta_q = q/H$",
                    "$\\zeta_q = qH$",
                    "$\\zeta_q = H/q$",
                    "$\\zeta_q = q + H$"
                ],
                "correctExplanation": "Increments are $N(0, \\nu^2\\Delta^{2H})$, so $\\E|\\cdot|^q = \\nu^q\\Delta^{qH}\\E|Z|^q$: linear (monofractal) scaling.",
                "incorrectExplanation": "Concave departures from $qH$ indicate multifractality or heavy-tailed increments."
            },
            "ro": {
                "title": "Exponentul de scalare",
                "text": "Dacă logaritmul volatilității are creșteri gaussiene de tip fBm cu exponentul Hurst $H$, cum depinde panta $\\zeta_q$ a lui $\\log m(q, \\Delta)$ pe $\\log\\Delta$ de $q$?",
                "options": [
                    "$\\zeta_q = q/H$",
                    "$\\zeta_q = qH$",
                    "$\\zeta_q = H/q$",
                    "$\\zeta_q = q + H$"
                ],
                "correctExplanation": "Creșterile sînt $N(0, \\nu^2\\Delta^{2H})$, deci $\\E|\\cdot|^q = \\nu^q\\Delta^{qH}\\E|Z|^q$: scalare liniară (monofractală).",
                "incorrectExplanation": "Abaterile concave de la $qH$ indică multifractalitate sau creșteri cu cozi groase."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Circulant embedding",
                "text": "What is the computational cost of simulating $n$ points of fractional Gaussian noise by the Davies--Harte method?",
                "options": [
                    "$O(n^3)$",
                    "$O(n^2)$",
                    "$O(n\\log n)$",
                    "$O(n)$"
                ],
                "correctExplanation": "The circulant of size $2(n - 1)$ is diagonalised by the FFT: two FFTs give an exact path.",
                "incorrectExplanation": "$O(n^3)$ is the Cholesky factorisation of the Toeplitz covariance."
            },
            "ro": {
                "title": "Scufundarea circulantă",
                "text": "Care este costul de calcul al simulării a $n$ puncte de zgomot gaussian fracționar prin metoda Davies--Harte?",
                "options": [
                    "$O(n^3)$",
                    "$O(n^2)$",
                    "$O(n\\log n)$",
                    "$O(n)$"
                ],
                "correctExplanation": "Matricea circulantă de ordin $2(n - 1)$ este diagonalizată de FFT: două FFT dau o traiectorie exactă.",
                "incorrectExplanation": "$O(n^3)$ este costul factorizării Cholesky a covarianței Toeplitz."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The hybrid scheme",
                "text": "Why does the hybrid scheme of Bennedsen, Lunde and Pakkanen (2017) beat a forward Riemann sum for a Riemann--Liouville process with $H = 0.1$?",
                "options": [
                    "It uses a Cholesky factorisation",
                    "It uses a coarser time step",
                    "It replaces the Gaussian driver by a heavy-tailed one",
                    "It integrates the singular kernel exactly near zero and evaluates it at optimal points further away"
                ],
                "correctExplanation": "The kernel $x^{H-1/2}$ is singular at zero; the Riemann sum misses that mass and understates the variance, increasingly as $H$ falls.",
                "incorrectExplanation": "The scheme keeps Gaussian increments and the same grid; its gain comes from the treatment of the first cells."
            },
            "ro": {
                "title": "Schema hibridă",
                "text": "De ce este schema hibridă a lui Bennedsen, Lunde și Pakkanen (2017) mai precisă decît o sumă Riemann înainte pentru un proces Riemann--Liouville cu $H = 0{,}1$?",
                "options": [
                    "Folosește o factorizare Cholesky",
                    "Folosește un pas de timp mai mare",
                    "Înlocuiește motorul gaussian cu unul cu cozi groase",
                    "Integrează exact nucleul singular lîngă zero și îl evaluează în puncte optime mai departe"
                ],
                "correctExplanation": "Nucleul $x^{H-1/2}$ este singular în zero; suma Riemann omite această masă și subestimează varianța, cu atît mai mult cu cît $H$ scade.",
                "incorrectExplanation": "Schema păstrează creșterile gaussiene și aceeași grilă; cîștigul vine din tratarea primelor celule."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The lognormal correction",
                "text": "An RFSV variance forecast is reported as $\\exp(\\E[\\log\\sigma^2_{t+h} \\mid \\mathcal F_t])$, without the term $2c\\nu^2h^{2H}$. What is the consequence?",
                "options": [
                    "The forecast of $\\sigma^2_{t+h}$ is biased downward, more so at longer horizons",
                    "It is biased upward",
                    "It is unbiased",
                    "It is undefined"
                ],
                "correctExplanation": "By Jensen, $\\E\\exp(X) = \\exp(\\E X + \\Var X/2)$ for Gaussian $X$; the omitted variance grows with $h^{2H}$.",
                "incorrectExplanation": "The exponential of a conditional mean of logs is a conditional median, which lies below the mean of a lognormal."
            },
            "ro": {
                "title": "Corecția lognormală",
                "text": "O prognoză RFSV a varianței este raportată ca $\\exp(\\E[\\log\\sigma^2_{t+h} \\mid \\mathcal F_t])$, fără termenul $2c\\nu^2h^{2H}$. Care este consecința?",
                "options": [
                    "Prognoza lui $\\sigma^2_{t+h}$ este deplasată în jos, mai mult la orizonturi lungi",
                    "Este deplasată în sus",
                    "Este nedeplasată",
                    "Nu este definită"
                ],
                "correctExplanation": "Prin Jensen, $\\E\\exp(X) = \\exp(\\E X + \\Var X/2)$ pentru $X$ gaussian; varianța omisă crește cu $h^{2H}$.",
                "incorrectExplanation": "Exponențiala unei medii condiționate a logaritmilor este o mediană condiționată, mai mică decît media unei variabile lognormale."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the error in the AI answer: roughness",
                "text": "An AI assistant writes: \"Realised volatility has $H \\approx 0.1$, so volatility has short memory, since $H < 1/2$ means antipersistence.\" What is wrong?",
                "options": [
                    "Nothing: the statement is correct",
                    "Small $H$ makes the increments of log volatility antipersistent, while its level is highly persistent ($\\hat d$ near 0.6)",
                    "The Hurst exponent of volatility must exceed 1",
                    "Fractional Brownian motion applies only to prices"
                ],
                "correctExplanation": "Roughness concerns small scales and increments; the level of log volatility keeps hyperbolically decaying autocorrelations.",
                "incorrectExplanation": "Antipersistence of increments is compatible with, and in fBm implies, a non-stationary, persistent level."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI: neregularitatea",
                "text": "Un asistent AI scrie: „Volatilitatea realizată are $H \\approx 0{,}1$, deci volatilitatea are memorie scurtă, deoarece $H < 1/2$ înseamnă antipersistență.” Ce este greșit?",
                "options": [
                    "Nimic: afirmația este corectă",
                    "$H$ mic face antipersistente creșterile logaritmului volatilității, în timp ce nivelul lui este foarte persistent ($\\hat d$ aproape de 0,6)",
                    "Exponentul Hurst al volatilității trebuie să depășească 1",
                    "Mișcarea browniană fracționară se aplică doar prețurilor"
                ],
                "correctExplanation": "Neregularitatea (roughness) privește scările mici și creșterile; nivelul logaritmului volatilității păstrează autocorelații cu descreștere hiperbolică.",
                "incorrectExplanation": "Antipersistența creșterilor este compatibilă cu un nivel nestaționar și persistent, iar în fBm chiar îl implică."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer: measurement error",
                "text": "An AI assistant writes: \"Measurement error in realised variance biases the estimate of $H$ upward, so true volatility is even rougher.\" What is the correct statement?",
                "options": [
                    "The statement is correct",
                    "Measurement error has no effect on $H$",
                    "An error that is independent across days adds a constant to $m(2, \\Delta)$ at every lag and biases $\\hat H$ downward",
                    "Measurement error affects $d$ but never $H$"
                ],
                "correctExplanation": "The variogram becomes $\\nu^2\\Delta^{2H} + 2s^2$; the constant flattens the log-log slope, so $\\hat H$ falls (daily integration pushes the other way).",
                "incorrectExplanation": "Noise lowers both $\\hat d$ and $\\hat H$; the coarser the RV grid, the lower the plain estimate."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI: eroarea de măsurare",
                "text": "Un asistent AI scrie: „Eroarea de măsurare a varianței realizate deplasează estimația lui $H$ în sus, deci volatilitatea adevărată este și mai neregulată.” Care este afirmația corectă?",
                "options": [
                    "Afirmația este corectă",
                    "Eroarea de măsurare nu are niciun efect asupra lui $H$",
                    "O eroare independentă de la o zi la alta adaugă o constantă la $m(2, \\Delta)$ pentru orice lag și deplasează $\\hat H$ în jos",
                    "Eroarea de măsurare afectează $d$, dar niciodată $H$"
                ],
                "correctExplanation": "Variograma devine $\\nu^2\\Delta^{2H} + 2s^2$; constanta aplatizează panta log-log, deci $\\hat H$ scade (integrarea zilnică acționează în sens opus).",
                "incorrectExplanation": "Zgomotul scade atît $\\hat d$, cît și $\\hat H$; cu cît grila RV este mai rară, cu atît estimația simplă este mai mică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Honest forecast comparison",
                "text": "Which choice invalidates an out-of-sample comparison of RFSV and HAR forecasts of realised variance?",
                "options": [
                    "A rolling estimation window",
                    "The QLIKE loss",
                    "DM tests with a Newey--West variance",
                    "Estimating $H$ and $\\nu$ once on the full sample, evaluation period included"
                ],
                "correctExplanation": "Parameters estimated with future data leak information into the forecasts; every parameter must use data up to $t$ only.",
                "incorrectExplanation": "Rolling windows, QLIKE (robust to the noise of the RV proxy) and HAC-based DM tests are standard good practice."
            },
            "ro": {
                "title": "Comparație riguroasă a prognozelor",
                "text": "Care alegere invalidează o comparație în afara eșantionului a prognozelor RFSV și HAR pentru varianța realizată?",
                "options": [
                    "O fereastră de estimare mobilă",
                    "Pierderea QLIKE",
                    "Testele DM cu varianță Newey--West",
                    "Estimarea lui $H$ și $\\nu$ o singură dată pe tot eșantionul, inclusiv perioada de evaluare"
                ],
                "correctExplanation": "Parametrii estimați cu date viitoare transferă informație în prognoze; fiecare parametru trebuie să folosească doar datele pînă la $t$.",
                "incorrectExplanation": "Ferestrele mobile, QLIKE (robustă la zgomotul proxy-ului RV) și testele DM cu HAC sînt practici bune obișnuite."
            }
        }
    ]
};
