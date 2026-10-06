// ============================================================
// Chapter 16 quiz bank: Explosive roots and bubbles (self-study; EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['bubbles'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 1,
            "en": {
                "title": "The bubble condition",
                "text": "In the present-value model $P_t = (1+r)^{-1}\\E_t[P_{t+1} + D_{t+1}]$, every solution is $P_t = F_t + B_t$. Which condition must the bubble term $B_t$ satisfy?",
                "options": [
                    "$B_t$ is a martingale: $\\E_t B_{t+1} = B_t$",
                    "$\\E_t B_{t+1} = (1 + r)B_t$",
                    "$B_t$ is stationary with mean zero",
                    "$B_t$ grows at the dividend growth rate"
                ],
                "correctExplanation": "Substituting $P_t = F_t + B_t$ into the pricing equation leaves $B_t = (1+r)^{-1}\\E_t B_{t+1}$: the bubble has an explosive conditional mean.",
                "incorrectExplanation": "A martingale or a stationary term would violate the pricing equation unless it is zero; the dividend growth rate plays no role in the bubble condition."
            },
            "ro": {
                "title": "Condiția bulei",
                "text": "În modelul valorii actualizate $P_t = (1+r)^{-1}\\E_t[P_{t+1} + D_{t+1}]$, orice soluție are forma $P_t = F_t + B_t$. Ce condiție trebuie să îndeplinească termenul de bulă $B_t$?",
                "options": [
                    "$B_t$ este o martingală: $\\E_t B_{t+1} = B_t$",
                    "$\\E_t B_{t+1} = (1 + r)B_t$",
                    "$B_t$ este staționar, cu media zero",
                    "$B_t$ crește cu rata de creștere a dividendelor"
                ],
                "correctExplanation": "Înlocuind $P_t = F_t + B_t$ în ecuația de evaluare rămîne $B_t = (1+r)^{-1}\\E_t B_{t+1}$: bula are o medie condiționată explozivă.",
                "incorrectExplanation": "O martingală sau un termen staționar ar încălca ecuația de evaluare, dacă nu sînt zero; rata de creștere a dividendelor nu intervine în condiția bulei."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The Diba-Grossman argument",
                "text": "Why can a rational bubble not start after the first trading day, according to Diba and Grossman?",
                "options": [
                    "If $B_t = 0$, then $\\E_t B_{t+1} = 0$ and $B_{t+1} \\ge 0$, so $B_{t+1} = 0$ almost surely",
                    "Because dividends are cointegrated with prices",
                    "Because the transversality condition always holds",
                    "Because bubbles grow at the risk-free rate only after they start"
                ],
                "correctExplanation": "With no negative bubbles, a non-negative variable with zero conditional mean is zero almost surely, so a zero bubble stays zero.",
                "incorrectExplanation": "Cointegration and transversality describe the no-bubble case; they do not explain why a bubble cannot be born."
            },
            "ro": {
                "title": "Argumentul Diba-Grossman",
                "text": "De ce nu poate o bulă rațională să apară după prima zi de tranzacționare, potrivit lui Diba și Grossman?",
                "options": [
                    "Dacă $B_t = 0$, atunci $\\E_t B_{t+1} = 0$ și $B_{t+1} \\ge 0$, deci $B_{t+1} = 0$ aproape sigur",
                    "Pentru că dividendele sînt cointegrate cu prețurile",
                    "Pentru că transversalitatea este întotdeauna îndeplinită",
                    "Pentru că bulele cresc cu rata fără risc doar după apariție"
                ],
                "correctExplanation": "Fără bule negative, o variabilă nenegativă cu media condiționată zero este zero aproape sigur, deci o bulă nulă rămîne nulă.",
                "incorrectExplanation": "Cointegrarea și transversalitatea descriu cazul fără bulă; nu explică de ce o bulă nu poate apărea."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Evans' pitfall",
                "text": "Why do whole-sample unit-root and cointegration tests have little power against periodically collapsing bubbles?",
                "options": [
                    "Because the bubble is negative after each collapse",
                    "Because the ADF test needs Gaussian errors",
                    "Because the collapses pair the largest falls with the highest lagged levels and pull the OLS slope down",
                    "Because the bubble never grows faster than $1 + r$"
                ],
                "correctExplanation": "Over the whole sample, the large negative changes at the highest levels dominate the OLS slope, so the series looks I(1) or even stationary.",
                "incorrectExplanation": "An Evans bubble stays positive and grows faster than $1 + r$ in its fast phase; the ADF test does not need Gaussian errors."
            },
            "ro": {
                "title": "Capcana lui Evans",
                "text": "De ce au testele de rădăcină unitară și de cointegrare pe tot eșantionul putere mică în fața bulelor care se prăbușesc periodic?",
                "options": [
                    "Pentru că bula este negativă după fiecare prăbușire",
                    "Pentru că testul ADF cere erori gaussiene",
                    "Pentru că prăbușirile împerechează cele mai mari scăderi cu cele mai mari niveluri anterioare și trag panta OLS în jos",
                    "Pentru că bula nu crește niciodată mai repede decît $1 + r$"
                ],
                "correctExplanation": "Pe tot eșantionul, variațiile negative mari de la nivelurile cele mai înalte domină panta OLS, iar seria arată I(1) sau chiar staționară.",
                "incorrectExplanation": "O bulă Evans rămîne pozitivă și crește mai repede decît $1 + r$ în faza rapidă; testul ADF nu cere erori gaussiene."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "A fundamental value",
                "text": "Dividends follow $D_t = \\mu + D_{t-1} + \\varepsilon_t$ with $\\mu = 0.02$; $r = 0.05$ and $D_t = 1$. What is the fundamental value $F_t = D_t/r + \\mu(1 + r)/r^2$?",
                "options": [
                    "20",
                    "28.4",
                    "21.05",
                    "8.4"
                ],
                "correctExplanation": "$1/0.05 + 0.02 \\cdot 1.05/0.0025 = 20 + 8.4 = 28.4$.",
                "incorrectExplanation": "Both terms count: $D_t/r = 20$ is the value with no growth, and $\\mu(1+r)/r^2 = 8.4$ is the value of the expected dividend growth."
            },
            "ro": {
                "title": "O valoare fundamentală",
                "text": "Dividendele urmează $D_t = \\mu + D_{t-1} + \\varepsilon_t$ cu $\\mu = 0,02$; $r = 0,05$ și $D_t = 1$. Cît este valoarea fundamentală $F_t = D_t/r + \\mu(1 + r)/r^2$?",
                "options": [
                    "20",
                    "28,4",
                    "21,05",
                    "8,4"
                ],
                "correctExplanation": "$1/0,05 + 0,02 \\cdot 1,05/0,0025 = 20 + 8,4 = 28,4$.",
                "incorrectExplanation": "Ambii termeni contează: $D_t/r = 20$ este valoarea fără creștere, iar $\\mu(1+r)/r^2 = 8,4$ este valoarea creșterii așteptate a dividendelor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Fixed explosive roots",
                "text": "For $y_t = \\rho y_{t-1} + u_t$ with a fixed $\\rho > 1$ and $y_0 = 0$, what is the limit of $\\rho^n(\\hat\\rho - \\rho)/(\\rho^2 - 1)$?",
                "options": [
                    "Standard normal for any i.i.d. errors with finite variance",
                    "The Dickey-Fuller distribution",
                    "Degenerate at zero",
                    "Standard Cauchy if the errors are Gaussian; otherwise a law that depends on the error distribution"
                ],
                "correctExplanation": "The statistic is approximately a ratio of two sums dominated by a few shocks; they are Gaussian, and the ratio Cauchy, only with Gaussian errors (White 1958, Anderson 1959).",
                "incorrectExplanation": "No central limit theorem acts inside sums dominated by a few shocks, so neither a normal limit nor an invariance principle holds; the Dickey-Fuller law belongs to $\\rho = 1$."
            },
            "ro": {
                "title": "Rădăcini explozive fixe",
                "text": "Pentru $y_t = \\rho y_{t-1} + u_t$ cu $\\rho > 1$ fix și $y_0 = 0$, care este limita lui $\\rho^n(\\hat\\rho - \\rho)/(\\rho^2 - 1)$?",
                "options": [
                    "Normală standard pentru orice erori i.i.d. cu dispersie finită",
                    "Distribuția Dickey-Fuller",
                    "Degenerată în zero",
                    "Cauchy standard dacă erorile sînt gaussiene; altfel o lege care depinde de distribuția erorilor"
                ],
                "correctExplanation": "Statistica este aproximativ un raport a două sume dominate de cîteva șocuri; acestea sînt gaussiene, iar raportul Cauchy, doar cu erori gaussiene (White 1958, Anderson 1959).",
                "incorrectExplanation": "Nicio teoremă limită centrală nu acționează în sume dominate de cîteva șocuri, deci nu există nici limită normală, nici principiu de invarianță; legea Dickey-Fuller corespunde cazului $\\rho = 1$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Mildly explosive roots",
                "text": "Phillips and Magdalinos (2007) study $\\rho_n = 1 + c/k_n$ with $c > 0$. Which condition on $k_n$ defines a mildly explosive root?",
                "options": [
                    "$k_n \\to \\infty$ and $k_n/n \\to 0$",
                    "$k_n = n$",
                    "$k_n$ fixed",
                    "$k_n \\to 0$"
                ],
                "correctExplanation": "Mild explosion lies between a local-to-unity root ($k_n = n$) and a fixed explosive root ($k_n$ fixed): $k_n \\to \\infty$ more slowly than $n$.",
                "incorrectExplanation": "$k_n = n$ gives a local-to-unity root, a fixed $k_n$ a fixed explosive root, and $k_n \\to 0$ an ever larger root."
            },
            "ro": {
                "title": "Rădăcini ușor explozive",
                "text": "Phillips și Magdalinos (2007) studiază $\\rho_n = 1 + c/k_n$ cu $c > 0$. Ce condiție asupra lui $k_n$ definește o rădăcină ușor explozivă?",
                "options": [
                    "$k_n \\to \\infty$ și $k_n/n \\to 0$",
                    "$k_n = n$",
                    "$k_n$ fix",
                    "$k_n \\to 0$"
                ],
                "correctExplanation": "Explozia ușoară se află între o rădăcină locală la unitate ($k_n = n$) și o rădăcină explozivă fixă ($k_n$ fix): $k_n \\to \\infty$ mai încet decît $n$.",
                "incorrectExplanation": "$k_n = n$ dă o rădăcină locală la unitate, un $k_n$ fix o rădăcină explozivă fixă, iar $k_n \\to 0$ o rădăcină tot mai mare."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Why mild explosion is invariant",
                "text": "Why is the Cauchy limit of the mildly explosive OLS estimator valid for any i.i.d. errors with finite variance?",
                "options": [
                    "Because the errors are assumed Gaussian",
                    "Because the estimator is consistent at rate $\\sqrt n$",
                    "Because about $k_n \\to \\infty$ shocks enter each of the two sums with comparable weights, so a central limit theorem applies",
                    "Because the intercept removes the non-Gaussian part"
                ],
                "correctExplanation": "With weights $\\rho_n^{-j} \\approx e^{-cj/k_n}$, no single shock dominates; the two sums become independent normals and their ratio is Cauchy.",
                "incorrectExplanation": "No Gaussian assumption is needed, the rate is $k_n\\rho_n^n$ rather than $\\sqrt n$, and the intercept plays no role in the argument."
            },
            "ro": {
                "title": "Invarianța în cazul ușor exploziv",
                "text": "De ce este limita Cauchy a estimatorului OLS în cazul ușor exploziv valabilă pentru orice erori i.i.d. cu dispersie finită?",
                "options": [
                    "Pentru că erorile sînt presupuse gaussiene",
                    "Pentru că estimatorul este consistent cu rata $\\sqrt n$",
                    "Pentru că aproximativ $k_n \\to \\infty$ șocuri intră în fiecare dintre cele două sume cu ponderi comparabile, deci se aplică o teoremă limită centrală",
                    "Pentru că termenul liber elimină partea negaussiană"
                ],
                "correctExplanation": "Cu ponderile $\\rho_n^{-j} \\approx e^{-cj/k_n}$, niciun șoc nu domină; cele două sume devin normale independente, iar raportul lor este Cauchy.",
                "incorrectExplanation": "Nu este nevoie de ipoteza gaussiană, rata este $k_n\\rho_n^n$, nu $\\sqrt n$, iar termenul liber nu intervine în argument."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Minimum window",
                "text": "A weekly sample has $T = 625$ observations. With the rule $r_0 = 0.01 + 1.8/\\sqrt T$, what is the minimum window $\\lfloor r_0T\\rfloor$?",
                "options": [
                    "72 weeks",
                    "18 weeks",
                    "625 weeks",
                    "51 weeks"
                ],
                "correctExplanation": "$r_0 = 0.01 + 1.8/25 = 0.082$ and $\\lfloor 0.082 \\cdot 625\\rfloor = \\lfloor 51.25\\rfloor = 51$.",
                "incorrectExplanation": "$\\sqrt{625} = 25$, so $r_0 = 0.082$; multiplying by $T$ gives 51.25, rounded down."
            },
            "ro": {
                "title": "Fereastra minimă",
                "text": "Un eșantion săptămînal are $T = 625$ de observații. Cu regula $r_0 = 0,01 + 1,8/\\sqrt T$, cît este fereastra minimă $\\lfloor r_0T\\rfloor$?",
                "options": [
                    "72 de săptămîni",
                    "18 săptămîni",
                    "625 de săptămîni",
                    "51 de săptămîni"
                ],
                "correctExplanation": "$r_0 = 0,01 + 1,8/25 = 0,082$ și $\\lfloor 0,082 \\cdot 625\\rfloor = \\lfloor 51,25\\rfloor = 51$.",
                "incorrectExplanation": "$\\sqrt{625} = 25$, deci $r_0 = 0,082$; înmulțind cu $T$ se obține 51,25, rotunjit în jos."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The right tail of the ADF statistic",
                "text": "A researcher tests $H_1$: $\\delta > 0$ with the whole-sample ADF statistic and rejects when it exceeds 1.645. What happens under the unit-root null?",
                "options": [
                    "The test rejects about 5% of the time",
                    "The test almost never rejects, because the 95% quantile of the Dickey-Fuller law with a constant is close to zero, not 1.645",
                    "The test always rejects",
                    "The test is valid only with lagged differences"
                ],
                "correctExplanation": "The Dickey-Fuller law with a constant is shifted to the left; its 95% quantile is near zero, so 1.645 is far in the right tail and the size is close to zero.",
                "incorrectExplanation": "The normal quantile does not apply to the ADF statistic under a unit root; lags do not change this."
            },
            "ro": {
                "title": "Coada dreaptă a statisticii ADF",
                "text": "Un cercetător testează $H_1$: $\\delta > 0$ cu statistica ADF pe tot eșantionul și respinge cînd depășește 1,645. Ce se întîmplă sub ipoteza nulă a rădăcinii unitare?",
                "options": [
                    "Testul respinge în aproximativ 5% din cazuri",
                    "Testul aproape nu respinge niciodată, fiindcă cuantila de 95% a legii Dickey-Fuller cu termen liber este aproape de zero, nu 1,645",
                    "Testul respinge întotdeauna",
                    "Testul este valid doar cu diferențe decalate"
                ],
                "correctExplanation": "Legea Dickey-Fuller cu termen liber este deplasată spre stînga; cuantila ei de 95% este aproape de zero, deci 1,645 este departe în coada dreaptă, iar nivelul este aproape zero.",
                "incorrectExplanation": "Cuantila normală nu se aplică statisticii ADF sub o rădăcină unitară; decalajele nu schimbă acest lucru."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "GSADF against SADF",
                "text": "Why is the 95% critical value of GSADF larger than that of SADF for the same $T$ and $r_0$?",
                "options": [
                    "Because GSADF uses lagged differences",
                    "Because GSADF is computed on log prices",
                    "Because GSADF takes the supremum over more windows (all start and end points), which shifts the null distribution to the right",
                    "Because GSADF has a different null hypothesis"
                ],
                "correctExplanation": "SADF searches over end points with the start fixed; GSADF also searches over start points; a maximum over more statistics is larger under the null.",
                "incorrectExplanation": "Both statistics share the null, the data transformation and the lag choice; only the set of windows differs."
            },
            "ro": {
                "title": "GSADF față de SADF",
                "text": "De ce este valoarea critică de 95% a GSADF mai mare decît cea a SADF pentru aceleași $T$ și $r_0$?",
                "options": [
                    "Pentru că GSADF folosește diferențe decalate",
                    "Pentru că GSADF se calculează pe logaritmul prețurilor",
                    "Pentru că GSADF ia supremul pe mai multe ferestre (toate punctele de început și de sfîrșit), ceea ce mută distribuția sub ipoteza nulă spre dreapta",
                    "Pentru că GSADF are o altă ipoteză nulă"
                ],
                "correctExplanation": "SADF caută pe punctele de sfîrșit, cu începutul fixat; GSADF caută și pe punctele de început; maximul mai multor statistici este mai mare sub ipoteza nulă.",
                "incorrectExplanation": "Cele două statistici au aceeași ipoteză nulă, aceeași transformare a datelor și aceeași alegere a decalajelor; diferă doar mulțimea ferestrelor."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The wild bootstrap",
                "text": "In the wild bootstrap of Phillips and Shi, the null residuals $\\hat e_t$ are multiplied by Rademacher signs $w_t = \\pm 1$ and cumulated. What does this keep from the data?",
                "options": [
                    "The pattern of volatility over time, while imposing a unit root and removing any explosive component",
                    "The explosive root of the data",
                    "The serial correlation of the squared returns only",
                    "The marginal distribution of the price level"
                ],
                "correctExplanation": "$|w_t\\hat e_t| = |\\hat e_t|$ preserves the volatility profile; random signs destroy any predictable or explosive component, and cumulating imposes a unit root.",
                "incorrectExplanation": "The bootstrap paths are built to satisfy the null, so they cannot keep an explosive root or the level of the data."
            },
            "ro": {
                "title": "Wild bootstrap",
                "text": "În wild bootstrap al lui Phillips și Shi, reziduurile sub ipoteza nulă $\\hat e_t$ se înmulțesc cu semne Rademacher $w_t = \\pm 1$ și se cumulează. Ce păstrează această procedură din date?",
                "options": [
                    "Tiparul volatilității în timp, impunînd o rădăcină unitară și eliminînd orice componentă explozivă",
                    "Rădăcina explozivă a datelor",
                    "Doar autocorelația randamentelor la pătrat",
                    "Distribuția marginală a nivelului prețului"
                ],
                "correctExplanation": "$|w_t\\hat e_t| = |\\hat e_t|$ păstrează profilul volatilității; semnele aleatoare distrug orice componentă predictibilă sau explozivă, iar cumularea impune o rădăcină unitară.",
                "incorrectExplanation": "Traiectoriile bootstrap sînt construite să respecte ipoteza nulă, deci nu pot păstra o rădăcină explozivă sau nivelul datelor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "A late rise in volatility",
                "text": "The shocks of a random walk triple their standard deviation in the second half of the sample. What happens to GSADF with homoskedastic Monte Carlo critical values?",
                "options": [
                    "It becomes conservative",
                    "Nothing: the null limit is pivotal",
                    "It loses power but keeps its size",
                    "It over-rejects: the late rise in volatility looks like acceleration"
                ],
                "correctExplanation": "The pivotal limit assumes constant variance; a late volatility rise inflates the window statistics, and the rejection rate rises far above 5% (33.8% in the chapter's simulation).",
                "incorrectExplanation": "Pivotality holds only under homoskedasticity; a fall in volatility, not a rise, makes the test conservative."
            },
            "ro": {
                "title": "O creștere tîrzie a volatilității",
                "text": "Șocurile unui mers aleator își triplează abaterea standard în a doua jumătate a eșantionului. Ce se întîmplă cu GSADF evaluat cu valori critice Monte Carlo homoscedastice?",
                "options": [
                    "Devine conservator",
                    "Nimic: limita sub ipoteza nulă este pivotală",
                    "Pierde putere, dar își păstrează nivelul",
                    "Respinge prea des: creșterea tîrzie a volatilității arată ca o accelerare"
                ],
                "correctExplanation": "Limita pivotală presupune dispersie constantă; o creștere tîrzie a volatilității umflă statisticile pe ferestre, iar rata de respingere urcă mult peste 5% (33,8% în simularea capitolului).",
                "incorrectExplanation": "Pivotalitatea este valabilă doar sub homoscedasticitate; o scădere a volatilității, nu o creștere, face testul conservator."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Pointwise dating",
                "text": "BSADF is compared with its pointwise 95% critical value at each of several hundred dates of a random walk without any bubble. What is true?",
                "options": [
                    "At most 5% of samples contain a false episode",
                    "Far more than 5% of samples contain at least one false episode, even with a minimum-duration rule",
                    "No false episode can occur, because BSADF is a supremum",
                    "False episodes occur only under changing volatility"
                ],
                "correctExplanation": "Each date has a 5% false-alarm chance; over hundreds of autocorrelated dates, at least one run of exceedances becomes likely (about a third of samples in the chapter's simulation).",
                "incorrectExplanation": "The 5% applies date by date, not to the sample; false episodes appear even with constant volatility."
            },
            "ro": {
                "title": "Datarea punctuală",
                "text": "BSADF este comparat cu valoarea critică punctuală de 95% la fiecare dintre cîteva sute de date ale unui mers aleator fără bulă. Ce este adevărat?",
                "options": [
                    "Cel mult 5% dintre eșantioane conțin un episod fals",
                    "Mult mai mult de 5% dintre eșantioane conțin cel puțin un episod fals, chiar cu regula duratei minime",
                    "Nu poate apărea niciun episod fals, fiindcă BSADF este un suprem",
                    "Episoadele false apar doar sub volatilitate variabilă"
                ],
                "correctExplanation": "Fiecare dată are o probabilitate de 5% de alarmă falsă; pe sute de date autocorelate, cel puțin o serie de depășiri devine probabilă (aproximativ o treime dintre eșantioane în simularea capitolului).",
                "incorrectExplanation": "Cei 5% se aplică dată cu dată, nu eșantionului; episoadele false apar chiar și cu volatilitate constantă."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Family-wise control over the sample",
                "text": "Which threshold controls at 5% the probability of at least one false alarm of BSADF over the whole sample?",
                "options": [
                    "The pointwise 95% quantile of BSADF at each date",
                    "The 95% quantile of the whole-sample ADF",
                    "The 95% quantile of the maximum of BSADF over all dates, i.e. the GSADF critical value",
                    "The normal quantile 1.645"
                ],
                "correctExplanation": "$\\Pr(\\max_t \\mathrm{BSADF}_t > c) \\le 5\\%$ when $c$ is the 95% quantile of the maximum, which is the GSADF critical value.",
                "incorrectExplanation": "Pointwise quantiles control each date separately; the whole-sample ADF and the normal quantile do not describe BSADF."
            },
            "ro": {
                "title": "Controlul de familie pe tot eșantionul",
                "text": "Ce prag controlează la 5% probabilitatea a cel puțin unei alarme false a BSADF pe tot eșantionul?",
                "options": [
                    "Cuantila punctuală de 95% a BSADF la fiecare dată",
                    "Cuantila de 95% a ADF pe tot eșantionul",
                    "Cuantila de 95% a maximului BSADF pe toate datele, adică valoarea critică GSADF",
                    "Cuantila normală 1,645"
                ],
                "correctExplanation": "$\\Pr(\\max_t \\mathrm{BSADF}_t > c) \\le 5\\%$ cînd $c$ este cuantila de 95% a maximului, adică valoarea critică GSADF.",
                "incorrectExplanation": "Cuantilele punctuale controlează fiecare dată separat; ADF pe tot eșantionul și cuantila normală nu descriu BSADF."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The alarm date",
                "text": "An episode is dated when BSADF exceeds its critical value for at least $L$ consecutive dates, starting at date $s$. In real time, when is the alarm known?",
                "options": [
                    "At date $s + L - 1$, the confirmation date",
                    "At date $s$",
                    "At the end of the episode",
                    "At the price peak"
                ],
                "correctExplanation": "The start $s$ is known to be part of an episode only after $L$ exceedances; using $s$ as the alarm date would use future information.",
                "incorrectExplanation": "The end of the episode and the peak are known later still; only the confirmation date is available in real time."
            },
            "ro": {
                "title": "Data alarmei",
                "text": "Un episod este datat cînd BSADF depășește valoarea critică la cel puțin $L$ date consecutive, începînd cu data $s$. În timp real, cînd este cunoscută alarma?",
                "options": [
                    "La data $s + L - 1$, data confirmării",
                    "La data $s$",
                    "La sfîrșitul episodului",
                    "La maximul prețului"
                ],
                "correctExplanation": "Se știe că data $s$ face parte dintr-un episod doar după $L$ depășiri; folosirea lui $s$ ca dată a alarmei ar folosi informație din viitor.",
                "incorrectExplanation": "Sfîrșitul episodului și maximul se cunosc și mai tîrziu; doar data confirmării este disponibilă în timp real."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Precision at the base rate",
                "text": "An alarm has hit rate $H = 0.6$ and false-alarm rate $F = 0.2$; the base rate of crashes is 10%. What is the probability of a crash given an alarm?",
                "options": [
                    "0.60",
                    "0.10",
                    "0.75",
                    "0.25"
                ],
                "correctExplanation": "By Bayes: $0.6 \\cdot 0.1/(0.6 \\cdot 0.1 + 0.2 \\cdot 0.9) = 0.06/0.24 = 0.25$.",
                "incorrectExplanation": "The hit rate conditions on the crash, not on the alarm; the precision weighs hits and false alarms by the base rate."
            },
            "ro": {
                "title": "Precizia la frecvența de bază",
                "text": "O alarmă are rata de detecție $H = 0,6$ și rata alarmelor false $F = 0,2$; frecvența de bază a crahurilor este 10%. Cît este probabilitatea unui crah, dată fiind o alarmă?",
                "options": [
                    "0,60",
                    "0,10",
                    "0,75",
                    "0,25"
                ],
                "correctExplanation": "Din regula lui Bayes: $0,6 \\cdot 0,1/(0,6 \\cdot 0,1 + 0,2 \\cdot 0,9) = 0,06/0,24 = 0,25$.",
                "incorrectExplanation": "Rata de detecție condiționează pe crah, nu pe alarmă; precizia ponderează detecțiile și alarmele false cu frecvența de bază."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "An AUC below one half",
                "text": "For the S&P 500, the AUC of BSADF as a predictor of a 20% fall within 182 days is about 0.41. What does it mean?",
                "options": [
                    "BSADF predicts crashes better than chance",
                    "Dates followed by a crash tend to have lower BSADF values than other dates",
                    "The test has the wrong size",
                    "The AUC cannot be below 0.5"
                ],
                "correctExplanation": "AUC is the probability that an event date has a higher score than a non-event date; below 0.5, event dates have lower scores (most of them lie in bear markets).",
                "incorrectExplanation": "An AUC below 0.5 is possible and says nothing about the size of the test; better than chance would need an AUC above 0.5."
            },
            "ro": {
                "title": "O AUC sub o jumătate",
                "text": "Pentru S&P 500, AUC a BSADF ca predictor al unei scăderi de 20% în 182 de zile este aproximativ 0,41. Ce înseamnă?",
                "options": [
                    "BSADF prognozează crahurile mai bine decît întîmplarea",
                    "Datele urmate de un crah tind să aibă valori BSADF mai mici decît celelalte date",
                    "Testul are un nivel greșit",
                    "AUC nu poate fi sub 0,5"
                ],
                "correctExplanation": "AUC este probabilitatea ca o dată cu eveniment să aibă un scor mai mare decît o dată fără eveniment; sub 0,5, datele cu eveniment au scoruri mai mici (majoritatea se află în piețe în declin).",
                "incorrectExplanation": "O AUC sub 0,5 este posibilă și nu spune nimic despre nivelul testului; o performanță peste întîmplare ar cere o AUC peste 0,5."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Ratio and fundamental",
                "text": "The log price-to-rent ratio of a housing market is explosive, while the log real rent is not. What is the most defensible reading?",
                "options": [
                    "Rents explain the acceleration of prices",
                    "The test is invalid because rents are I(1)",
                    "Prices accelerate beyond what the fundamental implies: the signature of a bubble component",
                    "The ratio must be stationary by construction"
                ],
                "correctExplanation": "Under the present-value model the ratio is stationary; an explosive ratio with a non-explosive fundamental points to an explosive component in prices.",
                "incorrectExplanation": "If rents explained the rise, the rent series would carry the explosive behaviour; an I(1) fundamental does not invalidate the test."
            },
            "ro": {
                "title": "Raportul și fundamentul",
                "text": "Logaritmul raportului preț/chirie al unei piețe imobiliare este exploziv, iar logaritmul chiriei reale nu este. Care este interpretarea cea mai ușor de apărat?",
                "options": [
                    "Chiriile explică accelerarea prețurilor",
                    "Testul nu este valid, fiindcă chiriile sînt I(1)",
                    "Prețurile accelerează peste ce implică fundamentul: semnătura unei componente de bulă",
                    "Raportul trebuie să fie staționar prin construcție"
                ],
                "correctExplanation": "În modelul valorii actualizate raportul este staționar; un raport exploziv cu un fundament neexploziv indică o componentă explozivă a prețurilor.",
                "incorrectExplanation": "Dacă chiriile ar explica creșterea, seria chiriilor ar purta comportamentul exploziv; un fundament I(1) nu invalidează testul."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Smoothed house price indices",
                "text": "Monthly repeat-sales house price indices have strongly autocorrelated changes. What should a right-tailed test on them include?",
                "options": [
                    "Lagged differences in every window regression, and a bootstrap under the AR null",
                    "Nothing: autocorrelation does not affect the ADF statistic",
                    "A larger minimum window only",
                    "Logarithms of the changes instead of the levels"
                ],
                "correctExplanation": "Without lags, autocorrelated changes look like acceleration and the tests reject almost everywhere; lags (chosen, for example, by BIC) and an AR null in the bootstrap correct this.",
                "incorrectExplanation": "Autocorrelation biases the no-lag ADF statistic; a larger window does not remove the bias, and the test is run on the log level."
            },
            "ro": {
                "title": "Indici netezîți ai prețurilor locuințelor",
                "text": "Indicii lunari ai prețurilor locuințelor, construiți din vînzări repetate, au variații puternic autocorelate. Ce trebuie să includă un test pe coada din dreapta aplicat lor?",
                "options": [
                    "Diferențe decalate în fiecare regresie pe fereastră și un bootstrap sub ipoteza nulă AR",
                    "Nimic: autocorelația nu afectează statistica ADF",
                    "Doar o fereastră minimă mai mare",
                    "Logaritmul variațiilor în locul nivelurilor"
                ],
                "correctExplanation": "Fără decalaje, variațiile autocorelate arată ca o accelerare, iar testele resping aproape peste tot; decalajele (alese, de exemplu, prin BIC) și ipoteza nulă AR din bootstrap corectează aceasta.",
                "incorrectExplanation": "Autocorelația deplasează statistica ADF fără decalaje; o fereastră mai mare nu elimină deplasarea, iar testul se aplică logaritmului nivelului."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The monitoring boundary",
                "text": "A CUSUM monitor uses the boundary of Chu, Stinchcombe and White with constant $a$. The one-sided crossing probability is $1 - \\Phi(a) + a\\varphi(a)$. Which $a$ gives about 5%?",
                "options": [
                    "$a = 1.645$",
                    "$a = 1.96$",
                    "$a = 3.84$",
                    "$a = 2.5$"
                ],
                "correctExplanation": "$1 - \\Phi(2.5) + 2.5\\varphi(2.5) \\approx 0.0062 + 0.0438 = 0.05$, so $a^2 = 6.25$.",
                "incorrectExplanation": "The term $a\\varphi(a)$ adds a lot to the normal tail; at $a = 1.645$ or $1.96$ the crossing probability is far above 5%."
            },
            "ro": {
                "title": "Frontiera de monitorizare",
                "text": "Un monitor CUSUM folosește frontiera Chu, Stinchcombe și White cu constanta $a$. Probabilitatea unilaterală de traversare este $1 - \\Phi(a) + a\\varphi(a)$. Ce $a$ dă aproximativ 5%?",
                "options": [
                    "$a = 1,645$",
                    "$a = 1,96$",
                    "$a = 3,84$",
                    "$a = 2,5$"
                ],
                "correctExplanation": "$1 - \\Phi(2,5) + 2,5\\varphi(2,5) \\approx 0,0062 + 0,0438 = 0,05$, deci $a^2 = 6,25$.",
                "incorrectExplanation": "Termenul $a\\varphi(a)$ adaugă mult la coada normală; pentru $a = 1,645$ sau $1,96$ probabilitatea de traversare este mult peste 5%."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Interval for the critical time",
                "text": "A 95% profile-likelihood interval for the LPPLS critical time $t_c$ keeps the values with $2[\\ell(\\hat t_c) - \\ell(t_c)] \\le c$. What is $c$, and when is the interval too narrow?",
                "options": [
                    "$c = 1.96$; when the window is long",
                    "$c = 3.84$; when the residuals are autocorrelated and the nuisance parameters are ignored",
                    "$c = 5.99$; when $m$ is close to one",
                    "$c = 3.84$; never, it is exact"
                ],
                "correctExplanation": "The likelihood-ratio statistic for one parameter is compared with the 95% quantile of $\\chi^2_1$, 3.84; autocorrelated residuals and nuisance parameters make the likelihood too sharp, which the modified profile likelihood corrects.",
                "incorrectExplanation": "1.96 is a normal quantile and 5.99 a $\\chi^2_2$ quantile; the interval is only approximate."
            },
            "ro": {
                "title": "Intervalul pentru timpul critic",
                "text": "Un interval de 95% din verosimilitatea profil pentru timpul critic LPPLS $t_c$ păstrează valorile cu $2[\\ell(\\hat t_c) - \\ell(t_c)] \\le c$. Cît este $c$ și cînd este intervalul prea îngust?",
                "options": [
                    "$c = 1,96$; cînd fereastra este lungă",
                    "$c = 3,84$; cînd reziduurile sînt autocorelate și parametrii de deranj sînt ignorați",
                    "$c = 5,99$; cînd $m$ este aproape de unu",
                    "$c = 3,84$; niciodată, intervalul este exact"
                ],
                "correctExplanation": "Statistica raportului de verosimilitate pentru un parametru se compară cu cuantila de 95% a $\\chi^2_1$, 3,84; reziduurile autocorelate și parametrii de deranj fac verosimilitatea prea ascuțită, iar verosimilitatea profil modificată corectează aceasta.",
                "incorrectExplanation": "1,96 este o cuantilă normală, iar 5,99 o cuantilă $\\chi^2_2$; intervalul este doar aproximativ."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer (1)",
                "text": "An AI assistant writes: \"SADF = 1.2 on the Nasdaq; since 1.2 < 1.645, the 5% normal critical value, there is no evidence of explosiveness.\" What is wrong?",
                "options": [
                    "Nothing: SADF is asymptotically normal",
                    "SADF should be compared with the left-tail Dickey-Fuller value",
                    "SADF has a non-standard null distribution; its critical value must be simulated for the same $T$, $r_0$ and specification (or bootstrapped), not taken from the normal law",
                    "The test should use GSADF only"
                ],
                "correctExplanation": "The null law of SADF is a supremum of Dickey-Fuller functionals, neither normal nor left-tailed; the 95% value (about 1.4 for $T = 400$ without lags) must be simulated.",
                "incorrectExplanation": "SADF is not asymptotically normal, the alternative is in the right tail, and SADF is a valid statistic in itself."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI (1)",
                "text": "Un asistent AI scrie: „SADF = 1,2 pentru Nasdaq; cum 1,2 < 1,645, valoarea critică normală de 5%, nu există dovezi de explozivitate.” Ce este greșit?",
                "options": [
                    "Nimic: SADF are asimptotic distribuția Normală",
                    "SADF trebuie comparat cu valoarea Dickey-Fuller din coada stîngă",
                    "SADF are o distribuție nestandard sub ipoteza nulă; valoarea critică trebuie simulată pentru aceleași $T$, $r_0$ și specificație (sau obținută prin bootstrap), nu luată din distribuția Normală",
                    "Testul trebuie să folosească doar GSADF"
                ],
                "correctExplanation": "Legea SADF sub ipoteza nulă este un suprem de funcționale Dickey-Fuller, nici normală, nici pe coada stîngă; valoarea de 95% (aproximativ 1,4 pentru $T = 400$ fără decalaje) trebuie simulată.",
                "incorrectExplanation": "SADF nu are asimptotic distribuția Normală, alternativa se află în coada dreaptă, iar SADF este o statistică validă în sine."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer (2)",
                "text": "An AI summary of a screen of 71 asset prices reads: \"GSADF rejects at 5% for 42 assets with Monte Carlo critical values, so speculative bubbles are widespread.\" Which two corrections come first?",
                "options": [
                    "Use more lags and a longer sample",
                    "Replace GSADF by SADF and test at 10%",
                    "Report only the assets with the largest GSADF",
                    "Use critical values that allow for changing volatility (wild bootstrap), and correct for testing 71 hypotheses (Holm or Benjamini-Hochberg)"
                ],
                "correctExplanation": "In the chapter's screen, the wild bootstrap reduces the rejections from 42 to 20, and Holm leaves 2 (Benjamini-Hochberg 12), with 3.6 expected by chance at 5%.",
                "incorrectExplanation": "Changing the lag order, the statistic or the level does not address the two errors: a homoskedastic null on heteroskedastic prices and no correction for multiplicity."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI (2)",
                "text": "Un rezumat AI al unei analize pe 71 de serii de prețuri spune: „GSADF respinge la 5% pentru 42 de active cu valori critice Monte Carlo, deci bulele speculative sînt larg răspîndite.” Care sînt primele două corecții?",
                "options": [
                    "Mai multe decalaje și un eșantion mai lung",
                    "Înlocuirea GSADF cu SADF și testarea la 10%",
                    "Raportarea doar a activelor cu cel mai mare GSADF",
                    "Valori critice care țin seama de volatilitatea variabilă (wild bootstrap) și corecția pentru testarea a 71 de ipoteze (Holm sau Benjamini-Hochberg)"
                ],
                "correctExplanation": "În analiza din capitol, wild bootstrap reduce respingerile de la 42 la 20, iar Holm lasă 2 (Benjamini-Hochberg 12), cu 3,6 așteptate din întîmplare la 5%.",
                "incorrectExplanation": "Schimbarea numărului de decalaje, a statisticii sau a nivelului nu corectează cele două erori: o ipoteză nulă homoscedastică pe prețuri heteroscedastice și lipsa corecției pentru multiplicitate."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Date-stamping delay",
                "text": "In the chapter's experiment, bubbles last 60 periods with $\\rho = 1.005$, $1.01$ or $1.02$. How does the median delay of the dated start change as $\\rho$ rises?",
                "options": [
                    "It falls (from about 19 to about 4 periods): faster bubbles are detected sooner",
                    "It rises, because faster bubbles collapse sooner",
                    "It does not depend on $\\rho$",
                    "It is always zero, because BSADF is consistent"
                ],
                "correctExplanation": "A window needs enough explosive observations for its ADF statistic to cross the critical value; the faster the explosion, the fewer observations are needed.",
                "incorrectExplanation": "Consistency is an asymptotic property; in finite samples the start is dated late, and the delay shrinks with the speed of the explosion."
            },
            "ro": {
                "title": "Întîrzierea datării",
                "text": "În experimentul capitolului, bulele durează 60 de perioade, cu $\\rho = 1,005$, $1,01$ sau $1,02$. Cum se schimbă întîrzierea mediană a începutului datat cînd $\\rho$ crește?",
                "options": [
                    "Scade (de la aproximativ 19 la aproximativ 4 perioade): bulele mai rapide sînt detectate mai devreme",
                    "Crește, fiindcă bulele mai rapide se prăbușesc mai devreme",
                    "Nu depinde de $\\rho$",
                    "Este întotdeauna zero, fiindcă BSADF este consistent"
                ],
                "correctExplanation": "O fereastră are nevoie de suficiente observații explozive pentru ca statistica ADF să depășească valoarea critică; cu cît explozia este mai rapidă, cu atît sînt necesare mai puține observații.",
                "incorrectExplanation": "Consistența este o proprietate asimptotică; în eșantioane finite începutul este datat tîrziu, iar întîrzierea scade odată cu viteza exploziei."
            }
        }
    ]
};
