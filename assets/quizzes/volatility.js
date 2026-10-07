// ============================================================
// Chapter 8 quiz bank: Advanced volatility modelling (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['volatility'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "What QML needs",
                "text": "Gaussian quasi-maximum likelihood for GARCH(1,1) is consistent when",
                "options": [
                    "the conditional variance equation is correctly specified, whatever the law of the standardised innovations",
                    "the standardised innovations are Gaussian",
                    "the returns have a finite fourth moment",
                    "the model is covariance stationary, $\\alpha + \\beta < 1$"
                ],
                "correctExplanation": "The Gaussian score has conditional mean zero at the true parameter as long as $\\E(\\eta_t^2) = 1$: only the variance equation matters; strict stationarity suffices.",
                "incorrectExplanation": "Normality is not needed, and strict stationarity ($\\E\\ln(\\alpha\\eta^2 + \\beta) < 0$) replaces finite moments of the returns; a finite fourth moment of $\\eta_t$ is needed only for asymptotic normality."
            },
            "ro": {
                "title": "Ce cere QML",
                "text": "Verosimilitatea cvasi-maximă gaussiană pentru GARCH(1,1) este consistentă cînd",
                "options": [
                    "ecuația varianței condiționate este corect specificată, oricare ar fi legea inovațiilor standardizate",
                    "inovațiile standardizate sînt gaussiene",
                    "randamentele au momentul de ordinul patru finit",
                    "modelul este staționar în covarianță, $\\alpha + \\beta < 1$"
                ],
                "correctExplanation": "Scorul gaussian are media condiționată zero în parametrul adevărat dacă $\\E(\\eta_t^2) = 1$: contează doar ecuația varianței; staționaritatea strictă este suficientă.",
                "incorrectExplanation": "Normalitatea nu este necesară, iar staționaritatea strictă ($\\E\\ln(\\alpha\\eta^2 + \\beta) < 0$) înlocuiește momentele finite ale randamentelor; un moment de ordinul patru finit al lui $\\eta_t$ este necesar doar pentru normalitatea asimptotică."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Hessian standard errors",
                "text": "Gaussian QML of GARCH(1,1) with standardised Student-$t(5)$ innovations ($\\kappa_\\eta = 9$). Compared with the correct (sandwich) standard errors, the Hessian-only standard errors are",
                "options": [
                    "correct, because the Hessian does not depend on the innovations",
                    "too small by the factor 2",
                    "too large by the factor 2",
                    "too small by the factor 4"
                ],
                "correctExplanation": "The sandwich is $(\\kappa_\\eta - 1)J^{-1}$, the Hessian-only variance $2J^{-1}$: the ratio of standard errors is $\\sqrt{(9 - 1)/2} = 2$.",
                "incorrectExplanation": "For GARCH the sandwich variance equals $(\\kappa_\\eta - 1)/2$ times the Hessian-only variance; with $\\kappa_\\eta = 9$ the variance ratio is 4, so the standard errors differ by the factor 2, with the Hessian ones smaller."
            },
            "ro": {
                "title": "Erorile standard din hessiană",
                "text": "QML gaussian pentru GARCH(1,1) cu inovații Student-$t(5)$ standardizate ($\\kappa_\\eta = 9$). Comparativ cu erorile standard corecte (sandwich), erorile standard obținute doar din hessiană sînt",
                "options": [
                    "corecte, pentru că hessiana nu depinde de inovații",
                    "prea mici cu factorul 2",
                    "prea mari cu factorul 2",
                    "prea mici cu factorul 4"
                ],
                "correctExplanation": "Sandwich-ul este $(\\kappa_\\eta - 1)J^{-1}$, varianța doar din hessiană $2J^{-1}$: raportul erorilor standard este $\\sqrt{(9 - 1)/2} = 2$.",
                "incorrectExplanation": "Pentru GARCH, varianța sandwich este de $(\\kappa_\\eta - 1)/2$ ori varianța doar din hessiană; cu $\\kappa_\\eta = 9$, raportul varianțelor este 4, deci erorile standard diferă cu factorul 2, cele din hessiană fiind mai mici."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "OPG standard errors",
                "text": "For GARCH QML with $\\kappa_\\eta > 3$, the outer-product-of-gradient (OPG) standard errors are",
                "options": [
                    "valid, because they use the scores",
                    "larger than the sandwich ones",
                    "even smaller than the Hessian-only ones",
                    "equal to the Hessian-only ones"
                ],
                "correctExplanation": "OPG uses $B^{-1} = \\frac{4}{\\kappa_\\eta - 1}J^{-1}$, which is below $2J^{-1}$ (Hessian) and far below $(\\kappa_\\eta - 1)J^{-1}$ (sandwich) when $\\kappa_\\eta > 3$.",
                "incorrectExplanation": "Both OPG and Hessian-only standard errors rely on the information-matrix equality, which fails without normality; with fat tails OPG understates the variance most."
            },
            "ro": {
                "title": "Erorile standard OPG",
                "text": "Pentru QML în GARCH cu $\\kappa_\\eta > 3$, erorile standard din produsul exterior al scorurilor (OPG) sînt",
                "options": [
                    "valide, pentru că folosesc scorurile",
                    "mai mari decît cele sandwich",
                    "chiar mai mici decît cele obținute doar din hessiană",
                    "egale cu cele obținute doar din hessiană"
                ],
                "correctExplanation": "OPG folosește $B^{-1} = \\frac{4}{\\kappa_\\eta - 1}J^{-1}$, care este sub $2J^{-1}$ (hessiana) și mult sub $(\\kappa_\\eta - 1)J^{-1}$ (sandwich) cînd $\\kappa_\\eta > 3$.",
                "incorrectExplanation": "Erorile standard OPG și cele doar din hessiană se bazează pe egalitatea matricei de informație, care nu are loc fără normalitate; cu cozi groase, OPG subestimează cel mai mult varianța."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Strict stationarity",
                "text": "GARCH(1,1) is strictly stationary if and only if",
                "options": [
                    "$\\alpha + \\beta < 1$",
                    "$\\alpha + \\beta \\le 1$",
                    "$\\E\\varepsilon_t^4 < \\infty$",
                    "$\\E\\ln(\\alpha\\eta_t^2 + \\beta) < 0$"
                ],
                "correctExplanation": "By Jensen, $\\E\\ln(\\alpha\\eta^2 + \\beta) \\le \\ln(\\alpha + \\beta)$, so IGARCH ($\\alpha + \\beta = 1$) is still strictly stationary, with an infinite variance.",
                "incorrectExplanation": "Covariance stationarity ($\\alpha + \\beta < 1$) is sufficient but not necessary; the strict-stationarity condition is the negative Lyapunov exponent $\\E\\ln(\\alpha\\eta_t^2 + \\beta) < 0$."
            },
            "ro": {
                "title": "Staționaritatea strictă",
                "text": "GARCH(1,1) este strict staționar dacă și numai dacă",
                "options": [
                    "$\\alpha + \\beta < 1$",
                    "$\\alpha + \\beta \\le 1$",
                    "$\\E\\varepsilon_t^4 < \\infty$",
                    "$\\E\\ln(\\alpha\\eta_t^2 + \\beta) < 0$"
                ],
                "correctExplanation": "Prin Jensen, $\\E\\ln(\\alpha\\eta^2 + \\beta) \\le \\ln(\\alpha + \\beta)$, deci IGARCH ($\\alpha + \\beta = 1$) rămîne strict staționar, cu varianță infinită.",
                "incorrectExplanation": "Staționaritatea în covarianță ($\\alpha + \\beta < 1$) este suficientă, dar nu necesară; condiția de staționaritate strictă este exponentul Lyapunov negativ $\\E\\ln(\\alpha\\eta_t^2 + \\beta) < 0$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Component GARCH",
                "text": "In the Engle--Lee component GARCH, the parameter $\\rho$ in $q_t = \\omega + \\rho q_{t-1} + \\phi(\\varepsilon^2_{t-1} - \\sigma^2_{t-1})$ is",
                "options": [
                    "the persistence of the long-run component",
                    "the persistence of the transitory component",
                    "the leverage effect",
                    "the weight of the long-run component in the total variance"
                ],
                "correctExplanation": "A shock to $q_t$ decays like $\\rho^h$; with $\\rho$ close to 1 the half-life $\\ln 0.5/\\ln\\rho$ is long, while the transitory part decays with $\\alpha + \\beta < \\rho$.",
                "incorrectExplanation": "The transitory deviation $\\sigma^2_t - q_t$ has persistence $\\alpha + \\beta$; $\\rho$ governs the slowly moving level $q_t$."
            },
            "ro": {
                "title": "Component GARCH",
                "text": "În component GARCH al lui Engle și Lee, parametrul $\\rho$ din $q_t = \\omega + \\rho q_{t-1} + \\phi(\\varepsilon^2_{t-1} - \\sigma^2_{t-1})$ este",
                "options": [
                    "persistența componentei de termen lung",
                    "persistența componentei tranzitorii",
                    "efectul de levier",
                    "ponderea componentei de termen lung în varianța totală"
                ],
                "correctExplanation": "Un șoc al lui $q_t$ scade ca $\\rho^h$; cu $\\rho$ apropiat de 1, timpul de înjumătățire $\\ln 0{,}5/\\ln\\rho$ este lung, iar partea tranzitorie scade cu $\\alpha + \\beta < \\rho$.",
                "incorrectExplanation": "Abaterea tranzitorie $\\sigma^2_t - q_t$ are persistența $\\alpha + \\beta$; $\\rho$ guvernează nivelul care se mișcă lent, $q_t$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Variance ratio",
                "text": "In GARCH-MIDAS, a macro variable has a significant $\\hat\\theta$ but the variance ratio $\\Var(\\ln\\tau_t)/\\Var(\\ln\\tau_tg_{i,t})$ is 3\\%. This means",
                "options": [
                    "the macro variable explains most of daily volatility",
                    "the long-run component driven by the macro variable explains little of the variation of log volatility",
                    "the short-run GARCH component is not identified",
                    "the model must be rejected in favour of GARCH(1,1)"
                ],
                "correctExplanation": "The variance ratio measures the share of the variation of log volatility due to the long-run component: significance and importance are different questions.",
                "incorrectExplanation": "A small variance ratio does not invalidate the model or the identification; it says the slow component moves little relative to daily fluctuations."
            },
            "ro": {
                "title": "Raportul de varianță",
                "text": "În GARCH-MIDAS, o variabilă macroeconomică are $\\hat\\theta$ semnificativ, dar raportul de varianță $\\Var(\\ln\\tau_t)/\\Var(\\ln\\tau_tg_{i,t})$ este 3\\%. Aceasta înseamnă că",
                "options": [
                    "variabila macroeconomică explică cea mai mare parte a volatilității zilnice",
                    "componenta de termen lung determinată de variabila macroeconomică explică puțin din variația logaritmului volatilității",
                    "componenta GARCH de termen scurt nu este identificată",
                    "modelul trebuie respins în favoarea GARCH(1,1)"
                ],
                "correctExplanation": "Raportul de varianță măsoară ponderea variației logaritmului volatilității datorată componentei de termen lung: semnificația și importanța sînt întrebări diferite.",
                "incorrectExplanation": "Un raport de varianță mic nu invalidează modelul sau identificarea; arată că componenta lentă se mișcă puțin față de fluctuațiile zilnice."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Identification in GARCH-MIDAS",
                "text": "What separates $\\tau_t$ from $g_{i,t}$ in GARCH-MIDAS without a latent-variable filter?",
                "options": [
                    "the Gaussian likelihood",
                    "the restriction $\\theta > 0$",
                    "$\\tau_t$ is constant within each month and $g_{i,t}$ has unconditional mean 1",
                    "the beta lag weights sum to one"
                ],
                "correctExplanation": "The long-run component changes only at the monthly frequency and the short-run component is a unit-mean GARCH: the mixed frequencies identify the split.",
                "incorrectExplanation": "The likelihood and the weights alone do not separate the components; the monthly step function of $\\tau_t$ and the normalisation of $g$ do."
            },
            "ro": {
                "title": "Identificarea în GARCH-MIDAS",
                "text": "Ce separă $\\tau_t$ de $g_{i,t}$ în GARCH-MIDAS fără un filtru pentru o variabilă latentă?",
                "options": [
                    "verosimilitatea gaussiană",
                    "restricția $\\theta > 0$",
                    "$\\tau_t$ este constant în fiecare lună, iar $g_{i,t}$ are media necondiționată 1",
                    "ponderile beta au suma unu"
                ],
                "correctExplanation": "Componenta de termen lung se schimbă doar la frecvența lunară, iar componenta de termen scurt este un GARCH cu media 1: frecvențele mixte identifică descompunerea.",
                "incorrectExplanation": "Verosimilitatea și ponderile singure nu separă componentele; o fac funcția în trepte lunare a lui $\\tau_t$ și normalizarea lui $g$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "CLT for realised variance",
                "text": "Without jumps or noise, with $n$ intraday returns, $\\mathrm{RV}_t - \\mathrm{IV}_t$ is approximately mixed normal with variance",
                "options": [
                    "$\\mathrm{IV}_t/n$",
                    "$2\\,\\mathrm{IV}_t^2$",
                    "$\\mathrm{IQ}_t/(3n)$",
                    "$2\\,\\mathrm{IQ}_t/n$"
                ],
                "correctExplanation": "Barndorff-Nielsen and Shephard (2002): $\\sqrt n(\\mathrm{RV}_t - \\mathrm{IV}_t) \\to MN(0, 2\\,\\mathrm{IQ}_t)$, with $\\mathrm{IQ}_t = \\int\\sigma^4_s\\,ds$ estimated by $\\frac n3\\sum r^4$.",
                "incorrectExplanation": "The variance involves the integrated quarticity and shrinks like $1/n$; the factor $\\frac n3$ belongs to the estimator of IQ, not to the variance of RV."
            },
            "ro": {
                "title": "TLC pentru varianța realizată",
                "text": "Fără salturi și fără zgomot, cu $n$ randamente intraday, $\\mathrm{RV}_t - \\mathrm{IV}_t$ este aproximativ mixt normal, cu varianța",
                "options": [
                    "$\\mathrm{IV}_t/n$",
                    "$2\\,\\mathrm{IV}_t^2$",
                    "$\\mathrm{IQ}_t/(3n)$",
                    "$2\\,\\mathrm{IQ}_t/n$"
                ],
                "correctExplanation": "Barndorff-Nielsen și Shephard (2002): $\\sqrt n(\\mathrm{RV}_t - \\mathrm{IV}_t) \\to MN(0, 2\\,\\mathrm{IQ}_t)$, cu $\\mathrm{IQ}_t = \\int\\sigma^4_s\\,ds$ estimat prin $\\frac n3\\sum r^4$.",
                "incorrectExplanation": "Varianța conține cuarticitatea integrată și scade ca $1/n$; factorul $\\frac n3$ aparține estimatorului lui IQ, nu varianței lui RV."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Stable convergence",
                "text": "Why does the CLT of realised variance need convergence that is stable in law?",
                "options": [
                    "so that dividing by a random, consistently estimated $\\sqrt{\\mathrm{IQ}_t}$ still gives a standard normal limit",
                    "because realised variance is not consistent",
                    "because the returns are independent across days",
                    "because jumps make the limit non-normal"
                ],
                "correctExplanation": "The limit is mixed normal (normal given the volatility path); stable convergence allows studentising by an estimate of the random variance.",
                "incorrectExplanation": "Ordinary convergence in law is not enough to combine the limit with a random normaliser; stability is exactly the property that makes the feasible statistic $N(0, 1)$."
            },
            "ro": {
                "title": "Convergența stabilă",
                "text": "De ce are nevoie TLC pentru varianța realizată de o convergență stabilă în lege?",
                "options": [
                    "pentru ca împărțirea la $\\sqrt{\\mathrm{IQ}_t}$, aleator și estimat consistent, să dea în continuare o limită normală standard",
                    "pentru că varianța realizată nu este consistentă",
                    "pentru că randamentele sînt independente de la o zi la alta",
                    "pentru că salturile fac limita nenormală"
                ],
                "correctExplanation": "Limita este mixt normală (normală dată traiectoria volatilității); convergența stabilă permite studentizarea cu o estimație a varianței aleatoare.",
                "incorrectExplanation": "Convergența obișnuită în lege nu permite combinarea limitei cu un factor de normalizare aleator; stabilitatea este exact proprietatea care face statistica fezabilă $N(0, 1)$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Noise bias",
                "text": "With i.i.d. noise of variance $\\omega^2$ added to the log price, the expected realised variance from $n$ returns is",
                "options": [
                    "$\\mathrm{IV}$",
                    "$\\mathrm{IV} + 2n\\omega^2$",
                    "$\\mathrm{IV} + \\omega^2$",
                    "$\\mathrm{IV} - 2n\\omega^2$"
                ],
                "correctExplanation": "Each observed return contains $u_i - u_{i-1}$, with variance $2\\omega^2$; summing $n$ of them adds $2n\\omega^2$.",
                "incorrectExplanation": "The noise adds a bias that grows linearly with the number of returns; it does not cancel and is not negative for i.i.d. noise."
            },
            "ro": {
                "title": "Deplasarea din zgomot",
                "text": "Cu zgomot i.i.d. de varianță $\\omega^2$ adăugat logaritmului prețului, media varianței realizate din $n$ randamente este",
                "options": [
                    "$\\mathrm{IV}$",
                    "$\\mathrm{IV} + 2n\\omega^2$",
                    "$\\mathrm{IV} + \\omega^2$",
                    "$\\mathrm{IV} - 2n\\omega^2$"
                ],
                "correctExplanation": "Fiecare randament observat conține $u_i - u_{i-1}$, cu varianța $2\\omega^2$; însumarea a $n$ astfel de termeni adaugă $2n\\omega^2$.",
                "incorrectExplanation": "Zgomotul adaugă o deplasare care crește liniar cu numărul de randamente; ea nu dispare și nu este negativă pentru zgomot i.i.d."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Optimal sparse sampling",
                "text": "Minimising $2\\,\\mathrm{IQ}/n + (2n\\omega^2)^2$ over $n$ gives",
                "options": [
                    "$n^* = \\mathrm{IQ}/\\omega^2$",
                    "$n^* = (\\mathrm{IQ}/\\omega^2)^{1/2}$",
                    "$n^* = (\\mathrm{IQ}/(4\\omega^4))^{1/3}$",
                    "the largest available $n$"
                ],
                "correctExplanation": "The first-order condition $-2\\,\\mathrm{IQ}/n^2 + 8n\\omega^4 = 0$ gives $n^3 = \\mathrm{IQ}/(4\\omega^4)$ (Bandi and Russell 2008).",
                "incorrectExplanation": "Variance falls like $1/n$ and squared bias rises like $n^2$: the optimum is interior and depends on $\\omega^4$, hence the cube root."
            },
            "ro": {
                "title": "Eșantionarea rară optimă",
                "text": "Minimizarea lui $2\\,\\mathrm{IQ}/n + (2n\\omega^2)^2$ în raport cu $n$ dă",
                "options": [
                    "$n^* = \\mathrm{IQ}/\\omega^2$",
                    "$n^* = (\\mathrm{IQ}/\\omega^2)^{1/2}$",
                    "$n^* = (\\mathrm{IQ}/(4\\omega^4))^{1/3}$",
                    "cel mai mare $n$ disponibil"
                ],
                "correctExplanation": "Condiția de ordinul întîi $-2\\,\\mathrm{IQ}/n^2 + 8n\\omega^4 = 0$ dă $n^3 = \\mathrm{IQ}/(4\\omega^4)$ (Bandi și Russell 2008).",
                "incorrectExplanation": "Varianța scade ca $1/n$, iar pătratul deplasării crește ca $n^2$: optimul este interior și depinde de $\\omega^4$, de aici rădăcina cubică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Realised kernels",
                "text": "Which statement about the Parzen realised kernel of Barndorff-Nielsen, Hansen, Lunde and Shephard (2008) is correct?",
                "options": [
                    "it discards all returns except one every five minutes",
                    "it can be negative on calm days",
                    "it is consistent for IV only without noise",
                    "it adds weighted autocovariances of the returns, which removes the noise bias, and it is nonnegative by construction"
                ],
                "correctExplanation": "The kernel $\\gamma_0 + \\sum k(h/(H+1))(\\gamma_h + \\gamma_{-h})$ corrects the negative first-order autocovariance created by noise; Parzen weights guarantee a nonnegative estimate.",
                "incorrectExplanation": "The realised kernel uses all returns and is designed for noisy data; with Parzen weights it cannot be negative."
            },
            "ro": {
                "title": "Realised kernels",
                "text": "Care afirmație despre realised kernel-ul Parzen al lui Barndorff-Nielsen, Hansen, Lunde și Shephard (2008) este corectă?",
                "options": [
                    "renunță la toate randamentele, cu excepția unuia la cinci minute",
                    "poate fi negativ în zilele liniștite",
                    "este consistent pentru IV doar fără zgomot",
                    "adaugă autocovarianțe ponderate ale randamentelor, ceea ce elimină deplasarea din zgomot, și este nenegativ prin construcție"
                ],
                "correctExplanation": "Kernel-ul $\\gamma_0 + \\sum k(h/(H+1))(\\gamma_h + \\gamma_{-h})$ corectează autocovarianța negativă de ordinul întîi creată de zgomot; ponderile Parzen garantează o estimație nenegativă.",
                "incorrectExplanation": "Realised kernel-ul folosește toate randamentele și este construit pentru date cu zgomot; cu ponderi Parzen nu poate fi negativ."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "A rising signature plot",
                "text": "For Bitcoin in August 2026 the average RV is lower at one second than at one minute. The most plausible reason is",
                "options": [
                    "positively autocorrelated one-second returns (zero returns, gradual price adjustment)",
                    "i.i.d. bid--ask noise",
                    "jumps at the one-second scale",
                    "an error in the definition of RV"
                ],
                "correctExplanation": "Positive autocovariance $\\gamma_1 > 0$ makes RV at the finest scale too small; i.i.d. noise would make it too large.",
                "incorrectExplanation": "I.i.d. noise produces negative autocorrelation and a falling signature plot; jumps raise RV at every scale; the rising pattern points to stale or gradually adjusting prices."
            },
            "ro": {
                "title": "Un signature plot crescător",
                "text": "Pentru Bitcoin, în august 2026, RV mediu este mai mic la o secundă decît la un minut. Motivul cel mai plauzibil este",
                "options": [
                    "autocorelația pozitivă a randamentelor la o secundă (randamente nule, ajustarea treptată a prețului)",
                    "zgomotul i.i.d. de tip bid--ask",
                    "salturile la scara de o secundă",
                    "o eroare în definiția lui RV"
                ],
                "correctExplanation": "O autocovarianță pozitivă $\\gamma_1 > 0$ face RV la scara cea mai fină prea mic; zgomotul i.i.d. l-ar face prea mare.",
                "incorrectExplanation": "Zgomotul i.i.d. produce autocorelație negativă și un signature plot descrescător; salturile cresc RV la orice scară; forma crescătoare indică prețuri stale (neactualizate) sau care se ajustează treptat."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Bipower variation",
                "text": "Why is bipower variation $\\mu_1^{-2}\\sum|r_i||r_{i-1}|$ robust to (finite-activity) jumps?",
                "options": [
                    "because it removes the largest returns",
                    "because a jump enters only two products, each multiplied by a return of order $n^{-1/2}$",
                    "because it uses squared returns",
                    "because it is computed from daily returns"
                ],
                "correctExplanation": "A jump of fixed size meets a neighbouring diffusive return that vanishes as $n$ grows, so its contribution goes to zero.",
                "incorrectExplanation": "Bipower variation keeps all returns; it is robust because products of adjacent absolute returns dampen isolated large moves."
            },
            "ro": {
                "title": "Variația bipower",
                "text": "De ce este variația bipower $\\mu_1^{-2}\\sum|r_i||r_{i-1}|$ robustă la salturi (cu activitate finită)?",
                "options": [
                    "pentru că elimină randamentele cele mai mari",
                    "pentru că un salt intră doar în două produse, fiecare înmulțit cu un randament de ordinul $n^{-1/2}$",
                    "pentru că folosește pătratele randamentelor",
                    "pentru că se calculează din randamente zilnice"
                ],
                "correctExplanation": "Un salt de mărime fixă întîlnește un randament difuziv vecin care tinde la zero cînd $n$ crește, deci contribuția lui dispare.",
                "incorrectExplanation": "Variația bipower păstrează toate randamentele; este robustă pentru că produsele randamentelor absolute vecine atenuează mișcările mari izolate."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Expected false jump days",
                "text": "A daily jump test at level 0.1\\% is applied to 3\\,000 days without jumps. The expected number of false jump days is",
                "options": [
                    "0",
                    "0.1",
                    "3",
                    "30"
                ],
                "correctExplanation": "$0.001 \\times 3000 = 3$: with many days, a small level still produces false detections; control the family-wise error or the FDR.",
                "incorrectExplanation": "The level is a per-test probability; over 3\\,000 tests the expected count is the level times the number of tests."
            },
            "ro": {
                "title": "Numărul așteptat de zile false cu salturi",
                "text": "Un test zilnic de salt la nivelul 0,1\\% se aplică pe 3\\,000 de zile fără salturi. Numărul așteptat de zile cu salturi false este",
                "options": [
                    "0",
                    "0,1",
                    "3",
                    "30"
                ],
                "correctExplanation": "$0{,}001 \\times 3000 = 3$: cu multe zile, un nivel mic produce totuși detectări false; controlați FWER sau FDR.",
                "incorrectExplanation": "Nivelul este o probabilitate pe test; pe 3\\,000 de teste, numărul așteptat este nivelul înmulțit cu numărul testelor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "HAR as an AR(22)",
                "text": "How many linear restrictions does the HAR model impose on an AR(22) for realised variance?",
                "options": [
                    "3",
                    "4",
                    "22",
                    "19"
                ],
                "correctExplanation": "The AR(22) has 22 slope coefficients; HAR describes them with 3 (daily, weekly, monthly), so 19 restrictions.",
                "incorrectExplanation": "Count the slopes: 22 in the AR(22) against 3 in HAR; the intercept is common to both."
            },
            "ro": {
                "title": "HAR ca AR(22)",
                "text": "Cîte restricții liniare impune modelul HAR unui AR(22) pentru varianța realizată?",
                "options": [
                    "3",
                    "4",
                    "22",
                    "19"
                ],
                "correctExplanation": "AR(22) are 22 de coeficienți de pantă; HAR îi descrie prin 3 (zilnic, săptămînal, lunar), deci 19 restricții.",
                "incorrectExplanation": "Numărați pantele: 22 în AR(22) față de 3 în HAR; termenul liber este comun ambelor modele."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The sign in HARQ",
                "text": "In HARQ, $\\mathrm{RV}_{t+1} = \\beta_0 + (\\beta_d + \\beta_{dQ}\\sqrt{\\mathrm{RQ}_t})\\mathrm{RV}_t + \\dots$, the coefficient $\\beta_{dQ}$ is expected to be negative because",
                "options": [
                    "when RQ is high, $\\mathrm{RV}_t$ is a noisier measure of $\\mathrm{IV}_t$, so it deserves less weight",
                    "volatility is mean-reverting",
                    "quarticity is always larger than variance",
                    "of the leverage effect"
                ],
                "correctExplanation": "The measurement error of RV has variance $2\\,\\mathrm{IQ}_t/n$; errors in variables attenuate the optimal weight more on imprecise days.",
                "incorrectExplanation": "Mean reversion and leverage concern the dynamics of IV, not the precision of its measurement, which is what RQ tracks."
            },
            "ro": {
                "title": "Semnul din HARQ",
                "text": "În HARQ, $\\mathrm{RV}_{t+1} = \\beta_0 + (\\beta_d + \\beta_{dQ}\\sqrt{\\mathrm{RQ}_t})\\mathrm{RV}_t + \\dots$, ne așteptăm ca $\\beta_{dQ}$ să fie negativ pentru că",
                "options": [
                    "cînd RQ este mare, $\\mathrm{RV}_t$ este o măsură mai zgomotoasă a lui $\\mathrm{IV}_t$, deci merită o pondere mai mică",
                    "volatilitatea revine la medie",
                    "cuarticitatea este întotdeauna mai mare decît varianța",
                    "din cauza efectului de levier"
                ],
                "correctExplanation": "Eroarea de măsurare a lui RV are varianța $2\\,\\mathrm{IQ}_t/n$; erorile în variabile atenuează mai mult ponderea optimă în zilele imprecise.",
                "incorrectExplanation": "Revenirea la medie și levierul privesc dinamica lui IV, nu precizia măsurării ei, pe care o urmărește RQ."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The insanity filter",
                "text": "In the out-of-sample HARQ comparison of Bollerslev, Patton and Quaedvlieg (2016), the insanity filter",
                "options": [
                    "removes jump days from the sample",
                    "replaces a forecast outside the range of the in-sample RV by the in-sample mean",
                    "sets negative forecasts to zero",
                    "is applied only to HAR"
                ],
                "correctExplanation": "Linear forecasts can be implausible (even negative) after a spike; the filter is a fixed rule applied to every model and must be reported.",
                "incorrectExplanation": "The filter acts on forecasts, not on data, and is applied to all competing models; setting forecasts to zero would make QLIKE undefined."
            },
            "ro": {
                "title": "Filtrul de plauzibilitate",
                "text": "În comparația HARQ în afara eșantionului din Bollerslev, Patton și Quaedvlieg (2016), filtrul de plauzibilitate („insanity filter”)",
                "options": [
                    "elimină din eșantion zilele cu salturi",
                    "înlocuiește o prognoză din afara intervalului RV din eșantionul de estimare cu media din eșantion",
                    "pune zero în locul prognozelor negative",
                    "se aplică doar pentru HAR"
                ],
                "correctExplanation": "Prognozele liniare pot fi neplauzibile (chiar negative) după un vîrf; filtrul este o regulă fixă aplicată fiecărui model și trebuie raportat.",
                "incorrectExplanation": "Filtrul acționează asupra prognozelor, nu asupra datelor, și se aplică tuturor modelelor comparate; o prognoză zero ar face QLIKE nedefinită."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Realized GARCH persistence",
                "text": "In the log-linear Realized GARCH, $\\ln h_t = \\omega + \\beta\\ln h_{t-1} + \\gamma\\ln x_{t-1}$ and $\\ln x_t = \\xi + \\varphi\\ln h_t + \\tau(z_t) + u_t$. The persistence of $\\ln h_t$ is",
                "options": [
                    "$\\beta$",
                    "$\\beta + \\gamma$",
                    "$\\beta + \\varphi\\gamma$",
                    "$\\varphi$"
                ],
                "correctExplanation": "Substituting the measurement equation gives $\\ln h_t = \\dots + (\\beta + \\varphi\\gamma)\\ln h_{t-1} + \\gamma(\\tau(z_{t-1}) + u_{t-1})$: an AR(1) with coefficient $\\beta + \\varphi\\gamma$.",
                "incorrectExplanation": "The realised measure feeds back into $h_t$ through $\\gamma$, scaled by how strongly it loads on $\\ln h_t$ ($\\varphi$)."
            },
            "ro": {
                "title": "Persistența Realized GARCH",
                "text": "În Realized GARCH log-liniar, $\\ln h_t = \\omega + \\beta\\ln h_{t-1} + \\gamma\\ln x_{t-1}$ și $\\ln x_t = \\xi + \\varphi\\ln h_t + \\tau(z_t) + u_t$. Persistența lui $\\ln h_t$ este",
                "options": [
                    "$\\beta$",
                    "$\\beta + \\gamma$",
                    "$\\beta + \\varphi\\gamma$",
                    "$\\varphi$"
                ],
                "correctExplanation": "Înlocuind ecuația de măsurare obținem $\\ln h_t = \\dots + (\\beta + \\varphi\\gamma)\\ln h_{t-1} + \\gamma(\\tau(z_{t-1}) + u_{t-1})$: un AR(1) cu coeficientul $\\beta + \\varphi\\gamma$.",
                "incorrectExplanation": "Măsura realizată revine în $h_t$ prin $\\gamma$, scalată de cît de puternic depinde de $\\ln h_t$ ($\\varphi$)."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Robust losses",
                "text": "Which losses rank volatility forecasts consistently when the target is a noisy but unbiased proxy (Patton 2011)?",
                "options": [
                    "MAE and MSE",
                    "MSE on logs and QLIKE",
                    "MAE and MSE on standard deviations",
                    "MSE and QLIKE"
                ],
                "correctExplanation": "MSE and QLIKE belong to the robust class $\\tilde C(h) + B(\\hat\\sigma^2) + C(h)(\\hat\\sigma^2 - h)$; their expected value is minimised by the conditional variance for any unbiased proxy.",
                "incorrectExplanation": "MAE targets the median of the proxy and MSE on logs targets $\\exp\\E\\ln\\hat\\sigma^2$: both reward forecasts that are biased downwards when the proxy is noisy."
            },
            "ro": {
                "title": "Funcții de pierdere robuste",
                "text": "Ce funcții de pierdere ordonează consistent prognozele de volatilitate cînd ținta este un proxy zgomotos, dar nedeplasat (Patton 2011)?",
                "options": [
                    "MAE și MSE",
                    "MSE pe logaritmi și QLIKE",
                    "MAE și MSE pe abateri standard",
                    "MSE și QLIKE"
                ],
                "correctExplanation": "MSE și QLIKE aparțin clasei robuste $\\tilde C(h) + B(\\hat\\sigma^2) + C(h)(\\hat\\sigma^2 - h)$; media lor este minimizată de varianța condiționată pentru orice proxy nedeplasat.",
                "incorrectExplanation": "MAE țintește mediana proxy-ului, iar MSE pe logaritmi țintește $\\exp\\E\\ln\\hat\\sigma^2$: ambele recompensează prognozele deplasate în jos cînd proxy-ul este zgomotos."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: \"Comparing volatility forecasts with MSE on log variances against squared daily returns is fine, since logs only stabilise the scale.\" The correct statement is",
                "options": [
                    "with $r_t^2$ as proxy, MSE-log is minimised by $h = \\exp(\\E\\ln r_t^2) \\approx 0.28\\,\\sigma^2_t$, so it rewards a strongly biased forecast",
                    "the statement is correct because logs are monotone",
                    "MSE-log is robust, but QLIKE is not",
                    "MSE-log is robust only for Student-$t$ returns"
                ],
                "correctExplanation": "For Gaussian returns $\\E\\ln z^2 \\approx -1.27$, so the MSE-log optimum is $e^{-1.27}\\sigma^2 \\approx 0.28\\sigma^2$: the loss is not robust to the noisy proxy.",
                "incorrectExplanation": "A monotone transformation of the proxy changes the functional that the loss elicits; only the Patton class (MSE, QLIKE) keeps the ranking."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Compararea prognozelor de volatilitate cu MSE pe logaritmii varianțelor față de pătratele randamentelor zilnice este în regulă, pentru că logaritmii doar stabilizează scala.” Afirmația corectă este",
                "options": [
                    "cu $r_t^2$ ca proxy, MSE-log este minimizat de $h = \\exp(\\E\\ln r_t^2) \\approx 0{,}28\\,\\sigma^2_t$, deci recompensează o prognoză puternic deplasată",
                    "afirmația este corectă, pentru că logaritmul este monoton",
                    "MSE-log este robust, dar QLIKE nu este",
                    "MSE-log este robust doar pentru randamente Student-$t$"
                ],
                "correctExplanation": "Pentru randamente gaussiene, $\\E\\ln z^2 \\approx -1{,}27$, deci optimul MSE-log este $e^{-1{,}27}\\sigma^2 \\approx 0{,}28\\sigma^2$: funcția nu este robustă la proxy-ul zgomotos.",
                "incorrectExplanation": "O transformare monotonă a proxy-ului schimbă funcționala pe care o elicitează funcția de pierdere; doar clasa Patton (MSE, QLIKE) păstrează ordinea."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Aielli's critique of DCC",
                "text": "Why is the standard DCC estimator with the sample correlation of $z_t$ as target inconsistent (Aielli 2013)?",
                "options": [
                    "because the univariate GARCH step is estimated first",
                    "because $\\E(z_tz_t' | \\mathcal F_{t-1}) = R_t \\ne Q_t$, so the unconditional mean of $Q_t$ differs from $\\E z_tz_t'$",
                    "because $a + b < 1$",
                    "because the correlation matrix is not positive definite"
                ],
                "correctExplanation": "cDCC uses $z^*_t = \\mathrm{diag}(Q_t)^{1/2}z_t$, for which $\\E(z^*_tz^{*\\prime}_t | \\mathcal F_{t-1}) = Q_t$, so the moment target becomes valid.",
                "incorrectExplanation": "Two-step estimation affects standard errors, not consistency; the problem is the mismatch between the conditional moments of $z_t$ and the recursion for $Q_t$."
            },
            "ro": {
                "title": "Critica lui Aielli la DCC",
                "text": "De ce este inconsistent estimatorul DCC standard cu corelația de eșantion a lui $z_t$ ca țintă (Aielli 2013)?",
                "options": [
                    "pentru că pasul GARCH univariat se estimează primul",
                    "pentru că $\\E(z_tz_t' | \\mathcal F_{t-1}) = R_t \\ne Q_t$, deci media necondiționată a lui $Q_t$ diferă de $\\E z_tz_t'$",
                    "pentru că $a + b < 1$",
                    "pentru că matricea de corelație nu este pozitiv definită"
                ],
                "correctExplanation": "cDCC folosește $z^*_t = \\mathrm{diag}(Q_t)^{1/2}z_t$, pentru care $\\E(z^*_tz^{*\\prime}_t | \\mathcal F_{t-1}) = Q_t$, deci ținta estimată prin momente devine validă.",
                "incorrectExplanation": "Estimarea în doi pași afectează erorile standard, nu consistența; problema este nepotrivirea dintre momentele condiționate ale lui $z_t$ și recursia pentru $Q_t$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "DCC-NL",
                "text": "In DCC-NL (Engle, Ledoit and Wolf 2019), nonlinear shrinkage is applied to",
                "options": [
                    "the univariate GARCH parameters",
                    "the daily returns before standardisation",
                    "the correlation target of the standardised residuals",
                    "the forecast covariance matrix after each update"
                ],
                "correctExplanation": "In large dimensions the DCC target is a noisy sample correlation matrix; shrinking its eigenvalues nonlinearly gives a better-conditioned target, while the DCC dynamics are kept.",
                "incorrectExplanation": "The variances come from univariate GARCH and the dynamics from $(a, b)$; only the large $N \\times N$ target is shrunk."
            },
            "ro": {
                "title": "DCC-NL",
                "text": "În DCC-NL (Engle, Ledoit și Wolf 2019), shrinkage-ul neliniar se aplică",
                "options": [
                    "parametrilor GARCH univariați",
                    "randamentelor zilnice înainte de standardizare",
                    "țintei de corelație a reziduurilor standardizate",
                    "matricei de covarianță prognozate după fiecare actualizare"
                ],
                "correctExplanation": "În dimensiune mare, ținta DCC este o matrice de corelație de eșantion zgomotoasă; shrinkage-ul neliniar al valorilor ei proprii dă o țintă mai bine condiționată, iar dinamica DCC se păstrează.",
                "incorrectExplanation": "Varianțele provin din GARCH univariat, iar dinamica din $(a, b)$; shrinkage-ul se aplică doar țintei mari, de dimensiune $N \\times N$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: \"Sampling every second gives the most accurate realised correlation between two assets, because more data always reduce error.\" The correct statement is",
                "options": [
                    "the statement is correct for liquid assets",
                    "realised correlation is unaffected by the sampling frequency",
                    "correlations rise towards one at high frequency",
                    "asynchronous trading biases realised covariances towards zero at high frequency (the Epps effect), so correlations are understated"
                ],
                "correctExplanation": "Previous-tick prices create zero returns for the asset that has not traded; the realised correlation of Bitcoin and Ether falls from about 0.8 at five minutes to about 0.64 at one second.",
                "incorrectExplanation": "More observations help only if prices are synchronous and noise-free; refresh-time sampling or the multivariate realised kernel fix the bias."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Eșantionarea la fiecare secundă dă cea mai precisă corelație realizată între două active, pentru că mai multe date reduc întotdeauna eroarea.” Afirmația corectă este",
                "options": [
                    "afirmația este corectă pentru active lichide",
                    "corelația realizată nu depinde de frecvența de eșantionare",
                    "corelațiile cresc spre unu la frecvență înaltă",
                    "tranzacționarea asincronă deplasează covarianțele realizate spre zero la frecvență înaltă (efectul Epps), deci corelațiile sînt subestimate"
                ],
                "correctExplanation": "Prețurile previous-tick creează randamente nule pentru activul care nu a fost tranzacționat; corelația realizată Bitcoin--Ether scade de la aproximativ 0,8 la cinci minute la aproximativ 0,64 la o secundă.",
                "incorrectExplanation": "Mai multe observații ajută doar dacă prețurile sînt sincrone și fără zgomot; eșantionarea la timpul de reîmprospătare sau realised kernel-ul multivariat corectează deplasarea."
            }
        }
    ]
};
