// ============================================================
// Chapter 9 quiz bank: VaR, ES and backtesting: elicitability, scoring and model risk (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['var-es'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Consistent loss for a quantile",
                "text": "Which loss is strictly consistent for the $\\alpha$-quantile of a continuous distribution with positive density?",
                "options": [
                    "$(\\mathbf 1\\{y \\le x\\} - \\alpha)(x - y)$",
                    "$(x - y)^2$",
                    "$|x - y|$ for every $\\alpha$",
                    "$\\mathbf 1\\{y \\le x\\}$"
                ],
                "correctExplanation": "The expected pinball loss has derivative $F(x) - \\alpha$, which is zero only at the $\\alpha$-quantile.",
                "incorrectExplanation": "Squared error elicits the mean, absolute error the median ($\\alpha = 1/2$ only), and the hit indicator alone is minimised by forecasting $-\\infty$."
            },
            "ro": {
                "title": "Pierdere consistentă pentru o cuantilă",
                "text": "Ce pierdere este strict consistentă pentru cuantila de nivel $\\alpha$ a unei distribuții continue cu densitate pozitivă?",
                "options": [
                    "$(\\mathbf 1\\{y \\le x\\} - \\alpha)(x - y)$",
                    "$(x - y)^2$",
                    "$|x - y|$ pentru orice $\\alpha$",
                    "$\\mathbf 1\\{y \\le x\\}$"
                ],
                "correctExplanation": "Pierderea pinball așteptată are derivata $F(x) - \\alpha$, care se anulează doar în cuantila de nivel $\\alpha$.",
                "incorrectExplanation": "Eroarea pătratică elicitează media, eroarea absolută mediana (doar $\\alpha = 1/2$), iar indicatorul de depășire singur este minimizat prognozînd $-\\infty$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Why ES alone is not elicitable",
                "text": "Which property rules out a strictly consistent loss function for ES alone?",
                "options": [
                    "ES is not coherent",
                    "Its level sets are not convex: a mixture of two distributions with the same ES can have a different ES",
                    "ES needs a finite variance",
                    "ES is not a functional of the distribution"
                ],
                "correctExplanation": "An elicitable functional has convex level sets; mixing two distributions with equal ES moves the quantile and changes the ES of the mixture.",
                "incorrectExplanation": "ES is coherent, needs only a finite first moment and is a law-invariant functional; the obstacle is the non-convexity of its level sets."
            },
            "ro": {
                "title": "De ce ES singur nu este elicitabil",
                "text": "Ce proprietate exclude o funcție de pierdere strict consistentă pentru ES singur?",
                "options": [
                    "ES nu este coerent",
                    "Mulțimile lui de nivel nu sînt convexe: un amestec de două distribuții cu același ES poate avea alt ES",
                    "ES cere o varianță finită",
                    "ES nu este o funcțională a distribuției"
                ],
                "correctExplanation": "O funcțională elicitabilă are mulțimi de nivel convexe; amestecul a două distribuții cu același ES mută cuantila și schimbă ES-ul amestecului.",
                "incorrectExplanation": "ES este coerent, cere doar primul moment finit și este o funcțională a distribuției; obstacolul este neconvexitatea mulțimilor de nivel."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The FZ0 loss",
                "text": "In the Fissler--Ziegel class with $v, e < 0$, which choice gives loss differences that do not depend on the scale of returns (the FZ0 loss)?",
                "options": [
                    "$G_1(x) = x$, $G_2(e) = e$",
                    "$G_1(x) = x$, $G_2(e) = \\exp(e)$",
                    "$G_1 = 0$, $G_2(e) = -1/e$",
                    "$G_1 = 0$, $G_2(e) = e^2$"
                ],
                "correctExplanation": "Patton, Ziegel and Chen (2019, Proposition 1) show that zero homogeneity holds if and only if $G_1 = 0$ and $G_2(e) = -1/e$.",
                "incorrectExplanation": "The other pairs either violate the conditions of the class (positive increasing $G_2$) or give losses that scale with the volatility of returns."
            },
            "ro": {
                "title": "Pierderea FZ0",
                "text": "În clasa Fissler--Ziegel cu $v, e < 0$, ce alegere dă diferențe de pierdere independente de scala randamentelor (pierderea FZ0)?",
                "options": [
                    "$G_1(x) = x$, $G_2(e) = e$",
                    "$G_1(x) = x$, $G_2(e) = \\exp(e)$",
                    "$G_1 = 0$, $G_2(e) = -1/e$",
                    "$G_1 = 0$, $G_2(e) = e^2$"
                ],
                "correctExplanation": "Patton, Ziegel și Chen (2019, Propoziția 1) arată că omogenitatea de grad zero are loc dacă și numai dacă $G_1 = 0$ și $G_2(e) = -1/e$.",
                "incorrectExplanation": "Celelalte perechi fie încalcă condițiile clasei ($G_2$ pozitivă și crescătoare), fie dau pierderi care cresc cu volatilitatea randamentelor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Why zero homogeneity matters",
                "text": "What does the zero homogeneity of FZ0 buy in a forecast comparison over a long period?",
                "options": [
                    "It makes FZ0 always positive",
                    "It removes the need for a VaR forecast",
                    "It makes the loss elicit ES alone",
                    "Volatile periods do not dominate the loss differences merely because returns are larger"
                ],
                "correctExplanation": "Rescaling $(y, v, e)$ by $s$ shifts FZ0 by $\\ln s$ for every forecast, so loss differences are scale-free and calm and volatile days count comparably.",
                "incorrectExplanation": "FZ0 can be negative, still needs the VaR forecast and never elicits ES alone."
            },
            "ro": {
                "title": "De ce contează omogenitatea de grad zero",
                "text": "Ce aduce omogenitatea de grad zero a FZ0 într-o comparație a prognozelor pe o perioadă lungă?",
                "options": [
                    "FZ0 devine întotdeauna pozitivă",
                    "Nu mai este nevoie de o prognoză VaR",
                    "Pierderea elicitează ES singur",
                    "Perioadele volatile nu domină diferențele de pierdere doar pentru că randamentele sînt mai mari"
                ],
                "correctExplanation": "Rescalarea lui $(y, v, e)$ cu $s$ mută FZ0 cu $\\ln s$ pentru orice prognoză, deci diferențele de pierdere nu depind de scală, iar zilele calme și cele volatile contează comparabil.",
                "incorrectExplanation": "FZ0 poate fi negativă, cere în continuare prognoza VaR și nu elicitează niciodată ES singur."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Identification function",
                "text": "Which function identifies the $\\alpha$-quantile, i.e.\\ has zero expectation only at the true quantile?",
                "options": [
                    "$\\mathbf 1\\{y \\le x\\} - \\alpha$",
                    "$x - y$",
                    "$(x - y)^2 - \\alpha$",
                    "$\\mathbf 1\\{y \\le x\\}(x - y)$"
                ],
                "correctExplanation": "$\\E[\\mathbf 1\\{Y \\le x\\} - \\alpha] = F(x) - \\alpha$, zero exactly at the quantile; centred hits are the basis of every VaR backtest.",
                "incorrectExplanation": "$x - y$ identifies the mean; the other two do not have zero expectation at the quantile."
            },
            "ro": {
                "title": "Funcția de identificare",
                "text": "Ce funcție identifică cuantila de nivel $\\alpha$, adică are media zero doar în cuantila corectă?",
                "options": [
                    "$\\mathbf 1\\{y \\le x\\} - \\alpha$",
                    "$x - y$",
                    "$(x - y)^2 - \\alpha$",
                    "$\\mathbf 1\\{y \\le x\\}(x - y)$"
                ],
                "correctExplanation": "$\\E[\\mathbf 1\\{Y \\le x\\} - \\alpha] = F(x) - \\alpha$, nulă exact în cuantilă; depășirile centrate stau la baza oricărui backtest VaR.",
                "incorrectExplanation": "$x - y$ identifică media; celelalte două nu au media zero în cuantilă."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The DQ test",
                "text": "In the out-of-sample DQ test of Engle and Manganelli with a constant, four lagged hits and the VaR forecast as regressors, the statistic is compared with:",
                "options": [
                    "$N(0, 1)$",
                    "$\\chi^2_6$",
                    "$\\chi^2_1$",
                    "$\\chi^2_2$"
                ],
                "correctExplanation": "Six regressors, all coefficients zero under $H_0$: the Wald-type statistic is $\\chi^2_6$ asymptotically.",
                "incorrectExplanation": "$\\chi^2_1$ is the Kupiec test, $\\chi^2_2$ the Christoffersen conditional coverage test; the DQ statistic is a quadratic form, not a $t$ ratio."
            },
            "ro": {
                "title": "Testul DQ",
                "text": "În testul DQ al lui Engle și Manganelli în afara eșantionului, cu regresorii constantă, patru depășiri întîrziate și prognoza VaR, statistica se compară cu:",
                "options": [
                    "$N(0, 1)$",
                    "$\\chi^2_6$",
                    "$\\chi^2_1$",
                    "$\\chi^2_2$"
                ],
                "correctExplanation": "Șase regresori, toți coeficienții nuli sub $H_0$: statistica de tip Wald are asimptotic distribuția $\\chi^2_6$.",
                "incorrectExplanation": "$\\chi^2_1$ corespunde testului Kupiec, $\\chi^2_2$ testului Christoffersen de acoperire condiționată; statistica DQ este o formă pătratică, nu un raport $t$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Asymmetric slope CAViaR",
                "text": "In $\\mathrm{VaR}_t = \\beta_1 + \\beta_2\\mathrm{VaR}_{t-1} + \\beta_3y_{t-1}^+ + \\beta_4y_{t-1}^-$, estimates $\\beta_3 = 0.04$ and $\\beta_4 = 0.62$ mean that:",
                "options": [
                    "the VaR does not depend on past returns",
                    "gains raise the VaR more than losses",
                    "losses raise the VaR far more than gains of the same size",
                    "the model is not stationary"
                ],
                "correctExplanation": "$y^- = \\max(-y, 0)$ enters with 0.62 and $y^+$ with 0.04: a loss raises the VaR about fifteen times more than a gain, the leverage effect in the tail.",
                "incorrectExplanation": "Both slopes are non-negative so past returns matter, the asymmetry goes the other way for gains, and stationarity depends on $\\beta_2$."
            },
            "ro": {
                "title": "CAViaR cu pantă asimetrică",
                "text": "În $\\mathrm{VaR}_t = \\beta_1 + \\beta_2\\mathrm{VaR}_{t-1} + \\beta_3y_{t-1}^+ + \\beta_4y_{t-1}^-$, estimațiile $\\beta_3 = 0{,}04$ și $\\beta_4 = 0{,}62$ înseamnă că:",
                "options": [
                    "VaR nu depinde de randamentele trecute",
                    "cîștigurile cresc VaR mai mult decît pierderile",
                    "pierderile cresc VaR mult mai mult decît cîștigurile de aceeași mărime",
                    "modelul nu este staționar"
                ],
                "correctExplanation": "$y^- = \\max(-y, 0)$ intră cu 0,62, iar $y^+$ cu 0,04: o pierdere crește VaR de circa cincisprezece ori mai mult decît un cîștig, efectul de levier în coadă.",
                "incorrectExplanation": "Ambele pante sînt nenegative, deci randamentele trecute contează; asimetria este inversă pentru cîștiguri, iar staționaritatea depinde de $\\beta_2$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Estimating CAViaR",
                "text": "Why do Engle and Manganelli start the estimation of CAViaR from many random parameter vectors?",
                "options": [
                    "The model has no parameters",
                    "The likelihood is Gaussian",
                    "Quantile regression has a closed form",
                    "The regression-quantile objective is non-differentiable and non-convex in the parameters of the recursion"
                ],
                "correctExplanation": "The pinball objective of a recursive quantile is piecewise smooth with many local minima, so a global random search precedes the local simplex and quasi-Newton steps.",
                "incorrectExplanation": "CAViaR has parameters, uses no likelihood, and only linear quantile regression is a linear program; the recursion destroys that structure."
            },
            "ro": {
                "title": "Estimarea CAViaR",
                "text": "De ce pornesc Engle și Manganelli estimarea CAViaR din mulți vectori de parametri aleatori?",
                "options": [
                    "Modelul nu are parametri",
                    "Verosimilitatea este Gaussiană",
                    "Regresia cuantilică are formă închisă",
                    "Criteriul de regresie cuantilică este nediferențiabil și neconvex în parametrii recursiei"
                ],
                "correctExplanation": "Criteriul pinball al unei cuantile recursive este neted pe porțiuni și are multe minime locale, deci o căutare aleatoare globală precedă pașii locali simplex și cvasi-Newton.",
                "incorrectExplanation": "CAViaR are parametri, nu folosește o verosimilitate, iar doar regresia cuantilică liniară este o problemă de programare liniară; recursia distruge această structură."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Duration-based backtest",
                "text": "In the duration test of Christoffersen and Pelletier, an estimated Weibull shape $b < 1$ indicates:",
                "options": [
                    "a decreasing hazard: hits cluster",
                    "a constant hazard: a correct VaR",
                    "too few hits",
                    "an increasing hazard: hits are evenly spaced"
                ],
                "correctExplanation": "A decreasing hazard means that a new hit is most likely soon after the previous one: clustering, which a correct VaR rules out.",
                "incorrectExplanation": "$b = 1$ is the memoryless case of a correct VaR, $b > 1$ an increasing hazard; the shape says nothing directly about the number of hits."
            },
            "ro": {
                "title": "Testul pe baza duratelor",
                "text": "În testul pe durate al lui Christoffersen și Pelletier, o formă Weibull estimată $b < 1$ indică:",
                "options": [
                    "un hazard descrescător: depășirile se grupează",
                    "un hazard constant: un VaR corect",
                    "prea puține depășiri",
                    "un hazard crescător: depășirile sînt egal distanțate"
                ],
                "correctExplanation": "Un hazard descrescător înseamnă că o nouă depășire este cea mai probabilă imediat după cea anterioară: grupare, pe care un VaR corect o exclude.",
                "incorrectExplanation": "$b = 1$ este cazul fără memorie al unui VaR corect, $b > 1$ un hazard crescător; forma nu spune direct nimic despre numărul depășirilor."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Estimation risk in backtests",
                "text": "A correct GARCH model is estimated once on $R = 250$ days and its VaR 1\\% is backtested with the Kupiec test on the next $P$ days. As $P$ grows:",
                "options": [
                    "the size of the test converges to 5\\%",
                    "the test rejects the correct model more and more often",
                    "the test loses all power",
                    "the estimation error disappears"
                ],
                "correctExplanation": "The estimation term is of order $\\sqrt{P/R}$: with a fixed window it grows with $P$, the Kupiec variance becomes too small and a correct model is over-rejected.",
                "incorrectExplanation": "Only when $P/R \\to 0$ does the estimation effect vanish; with fixed $R$ it does not, so the size moves away from 5\\%."
            },
            "ro": {
                "title": "Riscul de estimare în backtesting",
                "text": "Un model GARCH corect este estimat o singură dată pe $R = 250$ de zile, iar VaR 1\\% este testat cu testul Kupiec pe următoarele $P$ zile. Cînd $P$ crește:",
                "options": [
                    "mărimea testului converge la 5\\%",
                    "testul respinge tot mai des modelul corect",
                    "testul își pierde toată puterea",
                    "eroarea de estimare dispare"
                ],
                "correctExplanation": "Termenul de estimare este de ordinul $\\sqrt{P/R}$: cu o fereastră fixă crește odată cu $P$, varianța Kupiec devine prea mică, iar modelul corect este respins prea des.",
                "incorrectExplanation": "Efectul estimării dispare doar cînd $P/R \\to 0$; cu $R$ fix nu dispare, deci mărimea se îndepărtează de 5\\%."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Murphy diagrams",
                "text": "The Murphy diagrams (mean elementary scores against the threshold) of two VaR forecasts cross. What follows?",
                "options": [
                    "Both forecasts are miscalibrated",
                    "The pinball loss cannot be computed",
                    "Their ranking depends on the consistent scoring function chosen",
                    "The forecasts are identical"
                ],
                "correctExplanation": "Every consistent quantile score is a mixture of elementary scores; crossing curves mean that some mixtures favour one forecast and others the other.",
                "incorrectExplanation": "Crossing says nothing about calibration, the pinball loss is one particular mixture, and identical forecasts would give identical curves."
            },
            "ro": {
                "title": "Diagramele Murphy",
                "text": "Diagramele Murphy (scorurile elementare medii în funcție de prag) a două prognoze VaR se intersectează. Ce rezultă?",
                "options": [
                    "Ambele prognoze sînt necalibrate",
                    "Pierderea pinball nu se poate calcula",
                    "Ordonarea lor depinde de funcția de scor consistentă aleasă",
                    "Prognozele sînt identice"
                ],
                "correctExplanation": "Orice scor consistent pentru cuantile este un amestec de scoruri elementare; curbele care se intersectează înseamnă că unele amestecuri favorizează o prognoză, iar altele pe cealaltă.",
                "incorrectExplanation": "Intersecția nu spune nimic despre calibrare, pierderea pinball este un amestec particular, iar prognozele identice ar da curbe identice."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The square-root-of-time rule under GARCH",
                "text": "A GARCH(1,1) has persistence 0.98 and today's conditional variance is four times the unconditional one. The $\\sqrt{10}$ scaling of the 1-day volatility:",
                "options": [
                    "is exact",
                    "understates the 10-day volatility",
                    "is undefined",
                    "overstates the 10-day volatility, because volatility is expected to revert down"
                ],
                "correctExplanation": "The 10-day variance is $\\sum_{k=0}^{9}[\\bar\\sigma^2 + 0.98^k(\\sigma^2_{t+1} - \\bar\\sigma^2)] < 10\\sigma^2_{t+1}$ when $\\sigma^2_{t+1} > \\bar\\sigma^2$.",
                "incorrectExplanation": "The rule is exact only with constant variance; it understates risk when today's variance is below its long-run level, not above."
            },
            "ro": {
                "title": "Regula rădăcinii pătrate sub GARCH",
                "text": "Un GARCH(1,1) are persistența 0,98, iar varianța condiționată de azi este de patru ori varianța necondiționată. Scalarea cu $\\sqrt{10}$ a volatilității pe o zi:",
                "options": [
                    "este exactă",
                    "subestimează volatilitatea pe 10 zile",
                    "nu este definită",
                    "supraestimează volatilitatea pe 10 zile, deoarece volatilitatea este așteptată să scadă"
                ],
                "correctExplanation": "Varianța pe 10 zile este $\\sum_{k=0}^{9}[\\bar\\sigma^2 + 0{,}98^k(\\sigma^2_{t+1} - \\bar\\sigma^2)] < 10\\sigma^2_{t+1}$ cînd $\\sigma^2_{t+1} > \\bar\\sigma^2$.",
                "incorrectExplanation": "Regula este exactă doar cu varianță constantă; subestimează riscul cînd varianța de azi este sub nivelul de termen lung, nu deasupra lui."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "VaR convention",
                "text": "For daily returns $Y \\sim N(0, 1)$ (in \\%), the course convention gives VaR 1\\% equal to:",
                "options": [
                    "$2.33$, i.e.\\ minus the 1\\% quantile of returns",
                    "$-2.33$",
                    "$2.33$, the 99th percentile of returns",
                    "$1.64$"
                ],
                "correctExplanation": "$\\mathrm{VaR}_{0.01} = -q_{0.01} = -\\Phi^{-1}(0.01) = 2.33$: a loss level exceeded with probability 1\\%.",
                "incorrectExplanation": "The quantile itself is $-2.33$; calling it the 99th percentile mixes the loss and return scales; 1.64 is the 5\\% level."
            },
            "ro": {
                "title": "Convenția VaR",
                "text": "Pentru randamente zilnice $Y \\sim N(0, 1)$ (în \\%), convenția cursului dă VaR 1\\% egal cu:",
                "options": [
                    "$2{,}33$, adică minus cuantila de 1\\% a randamentelor",
                    "$-2{,}33$",
                    "$2{,}33$, percentila 99 a randamentelor",
                    "$1{,}64$"
                ],
                "correctExplanation": "$\\mathrm{VaR}_{0,01} = -q_{0,01} = -\\Phi^{-1}(0{,}01) = 2{,}33$: un nivel de pierdere depășit cu probabilitatea 1\\%.",
                "incorrectExplanation": "Cuantila însăși este $-2{,}33$; denumirea „percentila 99” amestecă scala pierderilor cu cea a randamentelor; 1,64 corespunde nivelului de 5\\%."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "ES of the Normal distribution",
                "text": "For $Y \\sim N(0, 1)$, ES 2.5\\% (the loss-scale tail mean beyond the 2.5\\% quantile) is approximately:",
                "options": [
                    "$1.96$",
                    "$2.34$",
                    "$2.58$",
                    "$1.64$"
                ],
                "correctExplanation": "$\\mathrm{ES}_{0.025} = \\varphi(\\Phi^{-1}(0.025))/0.025 = 0.0584/0.025 \\approx 2.34$.",
                "incorrectExplanation": "1.96 is VaR 2.5\\%, 2.58 is VaR 0.5\\%, 1.64 is VaR 5\\%; ES exceeds the VaR at the same level."
            },
            "ro": {
                "title": "ES pentru distribuția Normală",
                "text": "Pentru $Y \\sim N(0, 1)$, ES 2,5\\% (media cozii dincolo de cuantila de 2,5\\%, pe scala pierderilor) este aproximativ:",
                "options": [
                    "$1{,}96$",
                    "$2{,}34$",
                    "$2{,}58$",
                    "$1{,}64$"
                ],
                "correctExplanation": "$\\mathrm{ES}_{0,025} = \\varphi(\\Phi^{-1}(0{,}025))/0{,}025 = 0{,}0584/0{,}025 \\approx 2{,}34$.",
                "incorrectExplanation": "1,96 este VaR 2,5\\%, 2,58 este VaR 0,5\\%, 1,64 este VaR 5\\%; ES depășește VaR la același nivel."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Interpreting a large MCS",
                "text": "In a stress window of 90 days, the 90\\% model confidence set under FZ0 loss contains nine of ten models. The right conclusion is:",
                "options": [
                    "the nine models are equally good",
                    "the MCS procedure failed",
                    "the data cannot separate these models at the chosen level",
                    "the tenth model is the best"
                ],
                "correctExplanation": "The MCS contains the best models with a given probability; with few tail days the test of equal predictive ability has little power, so most models survive.",
                "incorrectExplanation": "Non-rejection is not equality, the procedure works as designed, and the eliminated model is the worst, not the best."
            },
            "ro": {
                "title": "Interpretarea unei mulțimi MCS mari",
                "text": "Într-o fereastră de criză de 90 de zile, mulțimea de încredere a modelelor de 90\\% sub pierderea FZ0 conține nouă din zece modele. Concluzia corectă este:",
                "options": [
                    "cele nouă modele sînt la fel de bune",
                    "procedura MCS a eșuat",
                    "datele nu pot separa aceste modele la nivelul ales",
                    "al zecelea model este cel mai bun"
                ],
                "correctExplanation": "MCS conține modelele cele mai bune cu o probabilitate dată; cu puține zile în coadă, testul egalității capacității predictive are putere mică, deci majoritatea modelelor rămîn.",
                "incorrectExplanation": "Nerespingerea nu înseamnă egalitate, procedura funcționează cum a fost construită, iar modelul eliminat este cel mai slab, nu cel mai bun."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Comparative backtesting zones",
                "text": "In the three-zone comparative backtest of Nolde and Ziegel, the internal model falls in the red zone when:",
                "options": [
                    "it passes the Kupiec test",
                    "the two models have equal average loss",
                    "neither one-sided test rejects",
                    "the test rejects $H_0^-$: the internal model is significantly worse than the standard one"
                ],
                "correctExplanation": "Red means significant evidence that the internal model has a higher expected consistent score than the standard model.",
                "incorrectExplanation": "Equal losses or no rejection give the yellow zone; a Kupiec test is a traditional, not a comparative, backtest."
            },
            "ro": {
                "title": "Zonele backtesting-ului comparativ",
                "text": "În backtesting-ul comparativ în trei zone al lui Nolde și Ziegel, modelul intern ajunge în zona roșie cînd:",
                "options": [
                    "trece testul Kupiec",
                    "cele două modele au aceeași pierdere medie",
                    "niciun test unilateral nu respinge",
                    "testul respinge $H_0^-$: modelul intern este semnificativ mai slab decît cel standard"
                ],
                "correctExplanation": "Roșu înseamnă evidență semnificativă că modelul intern are un scor consistent așteptat mai mare decît modelul standard.",
                "incorrectExplanation": "Pierderile egale sau lipsa respingerii dau zona galbenă; testul Kupiec este un backtest tradițional, nu unul comparativ."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The one-factor GAS model",
                "text": "In the GAS-1F model of Patton, Ziegel and Chen, what happens to the VaR and ES forecasts on a day without a VaR hit?",
                "options": [
                    "They move deterministically back towards their long-run level",
                    "They jump by the squared return",
                    "They stay exactly unchanged",
                    "They become positive"
                ],
                "correctExplanation": "Without a hit the forcing variable is $-\\frac{1}{e}(-e) = 1$, a constant, so $\\kappa_t$ follows a deterministic recursion and the forecasts decay smoothly.",
                "incorrectExplanation": "Squared returns drive GARCH, not GAS-1F; the forecasts do change on non-hit days, and $b < a < 0$ keeps them negative."
            },
            "ro": {
                "title": "Modelul GAS cu un factor",
                "text": "În modelul GAS-1F al lui Patton, Ziegel și Chen, ce se întîmplă cu prognozele VaR și ES într-o zi fără depășire a VaR?",
                "options": [
                    "Revin determinist spre nivelul lor de termen lung",
                    "Sar cu pătratul randamentului",
                    "Rămîn exact neschimbate",
                    "Devin pozitive"
                ],
                "correctExplanation": "Fără depășire, variabila de impuls este $-\\frac{1}{e}(-e) = 1$, o constantă, deci $\\kappa_t$ urmează o recursie deterministă, iar prognozele scad lin.",
                "incorrectExplanation": "Pătratele randamentelor determină GARCH, nu GAS-1F; prognozele se schimbă în zilele fără depășire, iar $b < a < 0$ le păstrează negative."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Replicating Patton, Ziegel and Chen",
                "text": "Replicating the S\\&P 500 design of Patton, Ziegel and Chen (2019) on the course data gives:",
                "options": [
                    "completely different average losses",
                    "average out-of-sample FZ0 losses within about 0.02 of the paper, but different goodness-of-fit $p$-values",
                    "identical $p$-values but different losses",
                    "no ranking of the models"
                ],
                "correctExplanation": "Average losses are smooth functions of many days and replicate closely; tests that rest on a handful of tail days are sensitive to data and covariance choices.",
                "incorrectExplanation": "The ranking and the losses of the paper are reproduced; it is the goodness-of-fit results that differ."
            },
            "ro": {
                "title": "Replicarea lui Patton, Ziegel și Chen",
                "text": "Replicarea designului S\\&P 500 al lui Patton, Ziegel și Chen (2019) pe datele cursului dă:",
                "options": [
                    "pierderi medii complet diferite",
                    "pierderi FZ0 medii în afara eșantionului la circa 0,02 de cele din lucrare, dar valori $p$ diferite la testele de adecvare",
                    "valori $p$ identice, dar pierderi diferite",
                    "nicio ordonare a modelelor"
                ],
                "correctExplanation": "Pierderile medii sînt funcții netede de multe zile și se replică îndeaproape; testele care se sprijină pe cîteva zile din coadă sînt sensibile la date și la alegerea covarianței.",
                "incorrectExplanation": "Ordonarea și pierderile din lucrare se reproduc; diferă rezultatele testelor de adecvare."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The extremal index",
                "text": "Daily losses above their 95\\% quantile have an estimated extremal index $\\hat\\theta = 0.3$. This means:",
                "options": [
                    "extremes are independent",
                    "the series has no extremes",
                    "extremes arrive in clusters of about three days on average",
                    "the GARCH filter is correct"
                ],
                "correctExplanation": "The mean cluster size of exceedances is $1/\\theta \\approx 3.3$ days.",
                "incorrectExplanation": "$\\theta = 1$ would mean no clustering; a GARCH filter is judged by the extremal index of the standardised, not the raw, losses."
            },
            "ro": {
                "title": "Indicele extremal",
                "text": "Pierderile zilnice peste cuantila lor de 95\\% au indicele extremal estimat $\\hat\\theta = 0{,}3$. Aceasta înseamnă:",
                "options": [
                    "extremele sînt independente",
                    "seria nu are extreme",
                    "extremele vin în grupuri de circa trei zile în medie",
                    "filtrul GARCH este corect"
                ],
                "correctExplanation": "Mărimea medie a unui grup de depășiri este $1/\\theta \\approx 3{,}3$ zile.",
                "incorrectExplanation": "$\\theta = 1$ ar însemna că extremele nu se grupează; un filtru GARCH se judecă după indicele extremal al pierderilor standardizate, nu al celor brute."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Adaptive conformal inference",
                "text": "What does adaptive conformal inference (Gibbs and Candès 2021) guarantee for a VaR forecast?",
                "options": [
                    "Conditional calibration given $\\mathcal F_{t-1}$",
                    "A correct ES forecast",
                    "Exchangeability of returns",
                    "A long-run hit frequency close to $\\alpha$ for any sequence of returns"
                ],
                "correctExplanation": "The update $\\alpha_{t+1} = \\alpha_t + \\gamma(\\alpha - \\mathrm{err}_t)$ bounds the deviation of the average hit rate from $\\alpha$ by a term of order $1/(\\gamma T)$, deterministically.",
                "incorrectExplanation": "ACI says nothing about conditional calibration or ES and needs no exchangeability; that is why it works on dependent returns."
            },
            "ro": {
                "title": "Inferența conformală adaptivă",
                "text": "Ce garantează inferența conformală adaptivă (Gibbs și Candès 2021) pentru o prognoză VaR?",
                "options": [
                    "Calibrarea condiționată de $\\mathcal F_{t-1}$",
                    "O prognoză ES corectă",
                    "Interschimbabilitatea randamentelor",
                    "O frecvență a depășirilor pe termen lung apropiată de $\\alpha$ pentru orice șir de randamente"
                ],
                "correctExplanation": "Actualizarea $\\alpha_{t+1} = \\alpha_t + \\gamma(\\alpha - \\mathrm{err}_t)$ mărginește abaterea ratei medii de depășire de la $\\alpha$ printr-un termen de ordinul $1/(\\gamma T)$, determinist.",
                "incorrectExplanation": "ACI nu spune nimic despre calibrarea condiționată sau despre ES și nu cere interschimbabilitate; de aceea funcționează pe randamente dependente."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Find the error in an AI answer (1)",
                "text": "An AI assistant writes: ``VaR 99\\% is the 99th percentile of daily returns.'' What is wrong?",
                "options": [
                    "The tail of interest is the 1\\% left tail of returns: VaR 1\\% is minus the 1\\% quantile of returns",
                    "Nothing: this is the standard definition",
                    "VaR is a mean, not a percentile",
                    "VaR is defined only for Normal returns"
                ],
                "correctExplanation": "The 99th percentile of returns is in the right (profit) tail; the course convention VaR 1\\% $= -q_{0.01}$ names the level by the tail probability.",
                "incorrectExplanation": "VaR is a quantile, not a mean, and it is defined for any distribution."
            },
            "ro": {
                "title": "Găsiți eroarea dintr-un răspuns AI (1)",
                "text": "Un asistent AI scrie: „VaR 99\\% este percentila 99 a randamentelor zilnice.” Ce este greșit?",
                "options": [
                    "Coada relevantă este coada stîngă de 1\\% a randamentelor: VaR 1\\% este minus cuantila de 1\\% a randamentelor",
                    "Nimic: aceasta este definiția standard",
                    "VaR este o medie, nu o percentilă",
                    "VaR este definit doar pentru randamente din distribuția Normală"
                ],
                "correctExplanation": "Percentila 99 a randamentelor se află în coada dreaptă (a cîștigurilor); convenția cursului VaR 1\\% $= -q_{0,01}$ denumește nivelul după probabilitatea cozii.",
                "incorrectExplanation": "VaR este o cuantilă, nu o medie, și este definit pentru orice distribuție."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the error in an AI answer (2)",
                "text": "An AI assistant proposes to rank ES models by the mean squared error between the ES forecast and the realised return on hit days. Why is this wrong?",
                "options": [
                    "MSE cannot be computed on hit days",
                    "No loss of the ES forecast alone is consistent for ES; the pair (VaR, ES) must be scored, e.g.\\ with FZ0",
                    "MSE is consistent for ES but too slow",
                    "ES models cannot be compared at all"
                ],
                "correctExplanation": "ES alone is not elicitable, so any ranking based only on ES forecasts can prefer a wrong forecast; the Fissler--Ziegel losses score the pair consistently.",
                "incorrectExplanation": "MSE can be computed but targets a conditional mean on a forecast-dependent event; ES models can be compared through the pair."
            },
            "ro": {
                "title": "Găsiți eroarea dintr-un răspuns AI (2)",
                "text": "Un asistent AI propune ordonarea modelelor ES după eroarea pătratică medie dintre prognoza ES și randamentul realizat în zilele cu depășiri. De ce este greșit?",
                "options": [
                    "MSE nu se poate calcula în zilele cu depășiri",
                    "Nicio pierdere a prognozei ES singure nu este consistentă pentru ES; trebuie evaluată perechea (VaR, ES), de exemplu cu FZ0",
                    "MSE este consistentă pentru ES, dar prea lentă",
                    "Modelele ES nu pot fi comparate deloc"
                ],
                "correctExplanation": "ES singur nu este elicitabil, deci orice ordonare bazată doar pe prognozele ES poate prefera o prognoză greșită; pierderile Fissler--Ziegel evaluează consistent perechea.",
                "incorrectExplanation": "MSE se poate calcula, dar țintește o medie condiționată pe un eveniment care depinde de prognoză; modelele ES pot fi comparate prin pereche."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Overlapping multi-day backtests",
                "text": "Daily forecasts of the 10-day VaR are backtested by counting all daily 10-day hits as independent Bernoulli trials. The problem is that:",
                "options": [
                    "10-day VaR cannot be backtested",
                    "the hit rate is biased downwards",
                    "overlapping windows make the hits dependent (MA(9) under $H_0$), so the test size is inflated",
                    "there are too many hits"
                ],
                "correctExplanation": "Consecutive 10-day windows share nine days, so hits are serially dependent even under a correct model; use non-overlapping windows or a HAC variance.",
                "incorrectExplanation": "Multi-day VaR can be backtested; overlap does not bias the hit rate, it understates the variance of the hit count."
            },
            "ro": {
                "title": "Backtesting pe mai multe zile cu suprapunere",
                "text": "Prognozele zilnice ale VaR pe 10 zile sînt testate numărînd toate depășirile zilnice pe 10 zile ca încercări Bernoulli independente. Problema este că:",
                "options": [
                    "VaR pe 10 zile nu se poate testa",
                    "rata de depășire este deplasată în jos",
                    "ferestrele suprapuse fac depășirile dependente (MA(9) sub $H_0$), deci mărimea testului crește",
                    "există prea multe depășiri"
                ],
                "correctExplanation": "Ferestrele consecutive de 10 zile au nouă zile comune, deci depășirile sînt dependente serial chiar pentru un model corect; folosiți ferestre fără suprapunere sau o varianță HAC.",
                "incorrectExplanation": "VaR pe mai multe zile se poate testa; suprapunerea nu deplasează rata de depășire, ci subestimează varianța numărului de depășiri."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Joint (VaR, ES) regression",
                "text": "In the joint quantile and ES regression of Dimitriadis and Bayer (2019), estimated by minimising a Fissler--Ziegel loss, the choice of the functions $(G_1, G_2)$:",
                "options": [
                    "changes the target of the estimation",
                    "must make the loss non-convex",
                    "determines whether ES is elicitable",
                    "affects the efficiency of the M-estimator but not its consistency"
                ],
                "correctExplanation": "Every strictly consistent member of the class identifies the same true parameters; the choice of $(G_1, G_2)$ changes only the asymptotic variance.",
                "incorrectExplanation": "The target is the pair (quantile, ES) for any member; elicitability of the pair does not depend on the member chosen."
            },
            "ro": {
                "title": "Regresia comună (VaR, ES)",
                "text": "În regresia comună pentru cuantilă și ES a lui Dimitriadis și Bayer (2019), estimată prin minimizarea unei pierderi Fissler--Ziegel, alegerea funcțiilor $(G_1, G_2)$:",
                "options": [
                    "schimbă ținta estimării",
                    "trebuie să facă pierderea neconvexă",
                    "determină dacă ES este elicitabil",
                    "afectează eficiența M-estimatorului, dar nu și consistența lui"
                ],
                "correctExplanation": "Orice membru strict consistent al clasei identifică aceiași parametri adevărați; alegerea lui $(G_1, G_2)$ schimbă doar varianța asimptotică.",
                "incorrectExplanation": "Ținta este perechea (cuantilă, ES) pentru orice membru; elicitabilitatea perechii nu depinde de membrul ales."
            }
        }
    ]
};
