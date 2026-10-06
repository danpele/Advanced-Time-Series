// ============================================================
// Chapter 5 quiz bank: Bayesian VAR, factor models and nowcasting (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['bvar-nowcasting'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Tight Minnesota prior",
                "text": "In a Minnesota BVAR, the overall tightness $\\lambda$ goes to 0. What does the posterior mean of the VAR coefficients become?",
                "options": [
                    "The prior mean: a random walk for persistent series, white noise for the others",
                    "The OLS estimates",
                    "A matrix of zeros for every variable",
                    "The estimates obtained with $\\lambda = \\infty$"
                ],
                "correctExplanation": "With $\\lambda \\to 0$ the prior variances vanish, so the data receive no weight and the posterior equals the prior mean ($\\delta_i$ on the own first lag, 0 elsewhere).",
                "incorrectExplanation": "OLS is the limit $\\lambda \\to \\infty$; the prior mean is not zero for persistent series ($\\delta_i = 1$)."
            },
            "ro": {
                "title": "Distribuția Minnesota foarte strînsă",
                "text": "Într-un BVAR Minnesota, gradul general de strîngere $\\lambda$ tinde la 0. Ce devine media a posteriori a coeficienților VAR?",
                "options": [
                    "Media a priori: mers aleator pentru seriile persistente, zgomot alb pentru celelalte",
                    "Estimațiile OLS",
                    "O matrice de zerouri pentru toate variabilele",
                    "Estimațiile obținute cu $\\lambda = \\infty$"
                ],
                "correctExplanation": "Cu $\\lambda \\to 0$ variațiile a priori dispar, deci datele nu primesc nicio pondere, iar media a posteriori este media a priori ($\\delta_i$ pe primul decalaj propriu, 0 în rest).",
                "incorrectExplanation": "OLS este limita $\\lambda \\to \\infty$; media a priori nu este zero pentru seriile persistente ($\\delta_i = 1$)."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The price of conjugacy",
                "text": "Why does the natural conjugate Normal–inverse-Wishart prior force the cross-variable shrinkage $\\vartheta$ of the Minnesota prior to equal 1?",
                "options": [
                    "Because the inverse-Wishart has too few degrees of freedom",
                    "Because the prior covariance $\\Sigma\\otimes\\Omega_0$ gives every equation the same $\\Omega_0$",
                    "Because the marginal likelihood is otherwise infinite",
                    "Because the sum-of-coefficients prior requires it"
                ],
                "correctExplanation": "The Kronecker structure scales one common $\\Omega_0$ by $\\Sigma_{ii}$ in each equation, so own and cross lags cannot be shrunk differently across equations.",
                "incorrectExplanation": "Degrees of freedom, the finiteness of the marginal likelihood and the sum-of-coefficients dummies have nothing to do with the restriction."
            },
            "ro": {
                "title": "Prețul conjugării",
                "text": "De ce impune distribuția a priori natural conjugată Normal–inverse-Wishart ca shrinkage-ul între variabile $\\vartheta$ al distribuției Minnesota să fie 1?",
                "options": [
                    "Pentru că inverse-Wishart are prea puține grade de libertate",
                    "Pentru că covarianța a priori $\\Sigma\\otimes\\Omega_0$ dă fiecărei ecuații același $\\Omega_0$",
                    "Pentru că altfel verosimilitatea marginală este infinită",
                    "Pentru că o cere distribuția pentru suma coeficienților"
                ],
                "correctExplanation": "Structura Kronecker scalează un singur $\\Omega_0$ comun cu $\\Sigma_{ii}$ în fiecare ecuație, deci decalajele proprii și cele încrucișate nu pot fi strînse diferit de la o ecuație la alta.",
                "incorrectExplanation": "Gradele de libertate, caracterul finit al verosimilității marginale și observațiile fictive pentru suma coeficienților nu au legătură cu această restricție."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Normal updating",
                "text": "An AR(1) coefficient has OLS estimate 0.8 with data precision 50 and prior $N(1, 0.2^2)$ (precision 25), $\\sigma^2$ known. What is the posterior mean?",
                "options": [
                    "0.900",
                    "0.800",
                    "0.867",
                    "0.933"
                ],
                "correctExplanation": "Precisions add (25 + 50 = 75) and the mean is the precision-weighted average: $(25 \\cdot 1 + 50 \\cdot 0.8)/75 = 0.867$.",
                "incorrectExplanation": "0.800 ignores the prior; 0.900 and 0.933 give the prior more weight than its precision justifies."
            },
            "ro": {
                "title": "Actualizarea Normală",
                "text": "Un coeficient AR(1) are estimația OLS 0,8 cu precizia datelor 50 și distribuția a priori $N(1; 0{,}2^2)$ (precizia 25), $\\sigma^2$ cunoscut. Care este media a posteriori?",
                "options": [
                    "0,900",
                    "0,800",
                    "0,867",
                    "0,933"
                ],
                "correctExplanation": "Preciziile se adună (25 + 50 = 75), iar media este media ponderată cu precizii: $(25 \\cdot 1 + 50 \\cdot 0{,}8)/75 = 0{,}867$.",
                "incorrectExplanation": "0,800 ignoră distribuția a priori; 0,900 și 0,933 dau distribuției a priori o pondere mai mare decît justifică precizia ei."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Effective sample size",
                "text": "A Gibbs chain of $M = 10\\,000$ draws has AR(1)-type autocorrelation $\\rho = 0.9$. What is its effective sample size?",
                "options": [
                    "9 000",
                    "1 000",
                    "5 000",
                    "526"
                ],
                "correctExplanation": "$\\mathrm{ESS} = M(1 - \\rho)/(1 + \\rho) = 10\\,000 \\times 0.1/1.9 \\approx 526$: one effective draw in every 19.",
                "incorrectExplanation": "9 000 subtracts the autocorrelation from the size, 1 000 multiplies by $1 - \\rho$ only, and 5 000 halves the chain; none uses the sum of autocorrelations."
            },
            "ro": {
                "title": "Mărimea efectivă a eșantionului",
                "text": "Un lanț Gibbs de $M = 10\\,000$ de extrageri are autocorelație de tip AR(1) $\\rho = 0{,}9$. Care este mărimea lui efectivă?",
                "options": [
                    "9 000",
                    "1 000",
                    "5 000",
                    "526"
                ],
                "correctExplanation": "$\\mathrm{ESS} = M(1 - \\rho)/(1 + \\rho) = 10\\,000 \\times 0{,}1/1{,}9 \\approx 526$: o extragere efectivă din 19.",
                "incorrectExplanation": "9 000 scade autocorelația din mărime, 1 000 înmulțește doar cu $1 - \\rho$, iar 5 000 înjumătățește lanțul; niciuna nu folosește suma autocorelațiilor."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Sum-of-coefficients prior",
                "text": "The sum-of-coefficients dummies have tightness $\\mu$. What model does the VAR approach as $\\mu \\to 0$?",
                "options": [
                    "A VAR in first differences without cointegration",
                    "A stationary VAR around the sample mean",
                    "A white-noise model for every variable",
                    "The OLS VAR in levels"
                ],
                "correctExplanation": "The dummies shrink $\\Pi = I - \\sum_l A_l$ towards 0; in the limit the error-correction term disappears: exact differencing.",
                "incorrectExplanation": "Stationarity around $\\bar y$ is the pull of the dummy initial observation; white noise is the Minnesota mean with $\\delta = 0$; OLS is no prior at all."
            },
            "ro": {
                "title": "Distribuția pentru suma coeficienților",
                "text": "Observațiile fictive pentru suma coeficienților au gradul de strîngere $\\mu$. Spre ce model tinde VAR-ul cînd $\\mu \\to 0$?",
                "options": [
                    "Un VAR în prime diferențe, fără cointegrare",
                    "Un VAR staționar în jurul mediei eșantionului",
                    "Un model de zgomot alb pentru fiecare variabilă",
                    "VAR-ul în niveluri estimat prin OLS"
                ],
                "correctExplanation": "Observațiile fictive strîng $\\Pi = I - \\sum_l A_l$ spre 0; la limită termenul de corecție a erorii dispare: diferențiere exactă.",
                "incorrectExplanation": "Staționaritatea în jurul lui $\\bar y$ este efectul observației inițiale fictive; zgomotul alb este media Minnesota cu $\\delta = 0$; OLS înseamnă absența distribuției a priori."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Dummy initial observation",
                "text": "Which property distinguishes the dummy-initial-observation prior from the sum-of-coefficients prior?",
                "options": [
                    "It forces every variable to have a unit root",
                    "It allows cointegration: it pulls towards unit roots or towards stationarity around the initial mean",
                    "It shrinks only the constant",
                    "It only changes the prior on the error covariance"
                ],
                "correctExplanation": "The single dummy row $\\bar y/\\phi$ is fitted either by unit roots or by a stationary model whose mean is $\\bar y$, so common trends and cointegration remain possible.",
                "incorrectExplanation": "It does not impose unit roots on each variable, it involves the lag coefficients and the constant jointly, and it leaves $\\Sigma$ to the inverse-Wishart."
            },
            "ro": {
                "title": "Observația inițială fictivă",
                "text": "Ce proprietate deosebește distribuția cu observația inițială fictivă de cea pentru suma coeficienților?",
                "options": [
                    "Impune o rădăcină unitară fiecărei variabile",
                    "Permite cointegrarea: împinge spre rădăcini unitare sau spre staționaritate în jurul mediei inițiale",
                    "Strînge doar termenul liber",
                    "Schimbă doar distribuția a priori a covarianței erorilor"
                ],
                "correctExplanation": "Linia fictivă unică $\\bar y/\\phi$ este potrivită fie prin rădăcini unitare, fie printr-un model staționar cu media $\\bar y$, deci trendurile comune și cointegrarea rămîn posibile.",
                "incorrectExplanation": "Nu impune rădăcini unitare fiecărei variabile, implică împreună coeficienții decalajelor și termenul liber și lasă $\\Sigma$ distribuției inverse-Wishart."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Shrinkage and system size",
                "text": "In Bańbura, Giannone and Reichlin (2010), how does the tightness $\\lambda$ chosen by the fit rule change from MEDIUM (20 variables) to LARGE?",
                "options": [
                    "It increases, because more variables carry more information",
                    "It stays the same, because the fit is held constant",
                    "It decreases: larger systems need tighter priors",
                    "It is set to infinity for the large system"
                ],
                "correctExplanation": "Holding the in-sample fit fixed requires more shrinkage as parameters multiply: in our replication 0.158 for MEDIUM and 0.059 for LARGE (0.108 and 0.035 in the paper).",
                "incorrectExplanation": "Keeping the fit constant is precisely what forces $\\lambda$ down; an infinite $\\lambda$ is OLS, which does not exist when $k > T$."
            },
            "ro": {
                "title": "Shrinkage și mărimea sistemului",
                "text": "În Bańbura, Giannone și Reichlin (2010), cum se schimbă gradul de strîngere $\\lambda$ ales prin regula potrivirii de la MEDIUM (20 de variabile) la LARGE?",
                "options": [
                    "Crește, pentru că mai multe variabile aduc mai multă informație",
                    "Rămîne același, pentru că potrivirea este menținută constantă",
                    "Scade: sistemele mai mari cer distribuții mai strînse",
                    "Este infinit pentru sistemul mare"
                ],
                "correctExplanation": "Menținerea potrivirii în eșantion cere mai mult shrinkage cînd parametrii se înmulțesc: în replicarea noastră 0,158 pentru MEDIUM și 0,059 pentru LARGE (0,108 și 0,035 în lucrare).",
                "incorrectExplanation": "Tocmai menținerea constantă a potrivirii împinge $\\lambda$ în jos; un $\\lambda$ infinit înseamnă OLS, care nu există cînd $k > T$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Marginal likelihood with dummies",
                "text": "GLP (2015) implement the sum-of-coefficients and initial-observation priors with dummy observations $Y_d$. How is the marginal likelihood of the data computed?",
                "options": [
                    "As the likelihood of $Y$ at the OLS estimates",
                    "As $\\ln p(Y, Y_d)$ alone",
                    "As $\\ln p(Y_d)$ alone",
                    "As $\\ln p(Y, Y_d\\mid\\gamma) - \\ln p(Y_d\\mid\\gamma)$"
                ],
                "correctExplanation": "The dummies are prior information, so the evidence for the data is the joint density of data and dummies divided by the density of the dummies.",
                "incorrectExplanation": "The OLS likelihood ignores the prior; the joint term alone counts the artificial rows as data; the dummies alone contain no data."
            },
            "ro": {
                "title": "Verosimilitatea marginală cu observații fictive",
                "text": "GLP (2015) implementează distribuțiile pentru suma coeficienților și observația inițială cu observații fictive $Y_d$. Cum se calculează verosimilitatea marginală a datelor?",
                "options": [
                    "Ca verosimilitatea lui $Y$ în estimațiile OLS",
                    "Doar ca $\\ln p(Y, Y_d)$",
                    "Doar ca $\\ln p(Y_d)$",
                    "Ca $\\ln p(Y, Y_d\\mid\\gamma) - \\ln p(Y_d\\mid\\gamma)$"
                ],
                "correctExplanation": "Observațiile fictive sînt informație a priori, deci evidența pentru date este densitatea comună a datelor și observațiilor fictive împărțită la densitatea observațiilor fictive.",
                "incorrectExplanation": "Verosimilitatea OLS ignoră distribuția a priori; termenul comun singur numără liniile artificiale drept date; observațiile fictive singure nu conțin date."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Why the marginal likelihood penalises complexity",
                "text": "Which identity explains why the log marginal likelihood behaves like an out-of-sample score?",
                "options": [
                    "$\\ln p(y) = \\sum_t \\ln p(y_t\\mid y_{1:t-1})$",
                    "$\\ln p(y) = \\max_\\theta \\ln p(y\\mid\\theta)$",
                    "$\\ln p(y) = \\ln p(\\theta\\mid y) - \\ln p(\\theta)$",
                    "$\\ln p(y) = -\\frac T2\\ln\\hat\\sigma^2$"
                ],
                "correctExplanation": "The prediction-error decomposition writes the evidence as a sum of one-step-ahead predictive log scores, each computed before seeing the observation.",
                "incorrectExplanation": "The maximised likelihood is in-sample; the other two expressions are not identities for the marginal likelihood."
            },
            "ro": {
                "title": "De ce penalizează verosimilitatea marginală complexitatea",
                "text": "Ce identitate explică de ce logaritmul verosimilității marginale se comportă ca un scor în afara eșantionului?",
                "options": [
                    "$\\ln p(y) = \\sum_t \\ln p(y_t\\mid y_{1:t-1})$",
                    "$\\ln p(y) = \\max_\\theta \\ln p(y\\mid\\theta)$",
                    "$\\ln p(y) = \\ln p(\\theta\\mid y) - \\ln p(\\theta)$",
                    "$\\ln p(y) = -\\frac T2\\ln\\hat\\sigma^2$"
                ],
                "correctExplanation": "Descompunerea erorilor de predicție scrie evidența ca sumă de scoruri logaritmice predictive la un pas, fiecare calculat înainte de a vedea observația.",
                "incorrectExplanation": "Verosimilitatea maximizată este în eșantion; celelalte două expresii nu sînt identități pentru verosimilitatea marginală."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Reading R-hat",
                "text": "Four Gibbs chains give $\\widehat R = 1.56$ for a parameter. What should you conclude?",
                "options": [
                    "The chains have converged, since $\\widehat R > 1$",
                    "The chains have not converged: at least one explores a different region",
                    "The posterior is bimodal for certain",
                    "The effective sample size is 1.56 times the number of draws"
                ],
                "correctExplanation": "$\\widehat R$ compares between-chain and within-chain variance; values well above about 1.01 signal that the chains disagree.",
                "incorrectExplanation": "Convergence requires $\\widehat R$ close to 1; disagreement may come from a stuck chain, not necessarily from bimodality; $\\widehat R$ is not an ESS ratio."
            },
            "ro": {
                "title": "Interpretarea lui R-hat",
                "text": "Patru lanțuri Gibbs dau $\\widehat R = 1{,}56$ pentru un parametru. Ce concluzionați?",
                "options": [
                    "Lanțurile au ajuns la convergență, deoarece $\\widehat R > 1$",
                    "Lanțurile nu au ajuns la convergență: cel puțin unul explorează o altă regiune",
                    "Distribuția a posteriori este sigur bimodală",
                    "Mărimea efectivă a eșantionului este de 1,56 ori numărul de extrageri"
                ],
                "correctExplanation": "$\\widehat R$ compară varianța dintre lanțuri cu cea din interiorul lor; valorile mult peste aproximativ 1,01 arată că lanțurile nu sînt de acord.",
                "incorrectExplanation": "Convergența cere $\\widehat R$ apropiat de 1; dezacordul poate veni dintr-un lanț blocat, nu neapărat din bimodalitate; $\\widehat R$ nu este un raport de ESS."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "What PCA identifies",
                "text": "In the approximate factor model $x_{it} = \\lambda_i'F_t + e_{it}$, what do principal components estimate consistently as $N, T \\to \\infty$?",
                "options": [
                    "Each factor with its economic label",
                    "The idiosyncratic covariance matrix",
                    "The factor space, i.e. $F_t$ up to an invertible rotation $H$",
                    "The number of factors, without any criterion"
                ],
                "correctExplanation": "$\\Lambda F_t = (\\Lambda H)(H^{-1}F_t)$ for any invertible $H$, so only the space spanned by the factors is identified; PCA estimates $HF_t$.",
                "incorrectExplanation": "Labels depend on the chosen rotation, the idiosyncratic part is only approximately diagonal, and the number of factors needs a criterion such as Bai–Ng."
            },
            "ro": {
                "title": "Ce identifică PCA",
                "text": "În modelul factorial aproximativ $x_{it} = \\lambda_i'F_t + e_{it}$, ce estimează consistent componentele principale cînd $N, T \\to \\infty$?",
                "options": [
                    "Fiecare factor cu eticheta lui economică",
                    "Matricea de covarianță idiosincratică",
                    "Spațiul factorilor, adică $F_t$ pînă la o rotație inversabilă $H$",
                    "Numărul de factori, fără niciun criteriu"
                ],
                "correctExplanation": "$\\Lambda F_t = (\\Lambda H)(H^{-1}F_t)$ pentru orice $H$ inversabilă, deci este identificat doar spațiul generat de factori; PCA estimează $HF_t$.",
                "incorrectExplanation": "Etichetele depind de rotația aleasă, partea idiosincratică este doar aproximativ diagonală, iar numărul de factori cere un criteriu precum Bai–Ng."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "An equicorrelated panel",
                "text": "Three standardised series have all pairwise correlations equal to 0.6. Which share of the total variance does the first principal component explain?",
                "options": [
                    "60.0%",
                    "20.0%",
                    "40.0%",
                    "73.3%"
                ],
                "correctExplanation": "The largest eigenvalue of $R = 0.4I + 0.6\\mathbf{1}\\mathbf{1}'$ is $1 + 2 \\times 0.6 = 2.2$, so the share is $2.2/3 = 73.3\\%$.",
                "incorrectExplanation": "60% is the limit as the number of series grows; 20% and 40% confuse the eigenvalues $1 - \\rho = 0.4$ with shares."
            },
            "ro": {
                "title": "Un panel echicorelat",
                "text": "Trei serii standardizate au toate corelațiile perechi egale cu 0,6. Ce pondere din varianța totală explică prima componentă principală?",
                "options": [
                    "60,0%",
                    "20,0%",
                    "40,0%",
                    "73,3%"
                ],
                "correctExplanation": "Cea mai mare valoare proprie a lui $R = 0{,}4I + 0{,}6\\mathbf{1}\\mathbf{1}'$ este $1 + 2 \\times 0{,}6 = 2{,}2$, deci ponderea este $2{,}2/3 = 73{,}3\\%$.",
                "incorrectExplanation": "60% este limita cînd numărul de serii crește; 20% și 40% confundă valorile proprii $1 - \\rho = 0{,}4$ cu ponderi."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The Bai–Ng penalty",
                "text": "Which expression is the $IC_{p2}$ criterion of Bai and Ng (2002) for $k$ factors, with $V(k)$ the residual mean square?",
                "options": [
                    "$\\ln V(k) + k\\frac{N + T}{NT}\\ln\\min(N, T)$",
                    "$\\ln V(k) + 2k/T$",
                    "$V(k) - k\\ln N$",
                    "$\\ln V(k) + k\\ln(NT)/N$"
                ],
                "correctExplanation": "The penalty grows with $k$ at a rate that vanishes as both $N$ and $T$ grow, which makes the selection consistent.",
                "incorrectExplanation": "$2k/T$ is an AIC-type penalty for one series; subtracting a penalty rewards complexity; the last expression does not vanish correctly when only $T$ grows."
            },
            "ro": {
                "title": "Penalizarea Bai–Ng",
                "text": "Ce expresie este criteriul $IC_{p2}$ al lui Bai și Ng (2002) pentru $k$ factori, cu $V(k)$ media pătratelor reziduurilor?",
                "options": [
                    "$\\ln V(k) + k\\frac{N + T}{NT}\\ln\\min(N, T)$",
                    "$\\ln V(k) + 2k/T$",
                    "$V(k) - k\\ln N$",
                    "$\\ln V(k) + k\\ln(NT)/N$"
                ],
                "correctExplanation": "Penalizarea crește cu $k$, cu o rată care se anulează cînd $N$ și $T$ cresc amîndouă, ceea ce face selecția consistentă.",
                "incorrectExplanation": "$2k/T$ este o penalizare de tip AIC pentru o singură serie; scăderea unei penalizări recompensează complexitatea; ultima expresie nu se anulează corect cînd crește doar $T$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Diffusion-index target for prices",
                "text": "In Stock and Watson (2002, JBES), what is the $h$-step target for a price index $P_t$ (an I(2) series in logs)?",
                "options": [
                    "$\\frac{1200}{h}\\ln(P_{t+h}/P_t)$",
                    "$\\frac{1200}{h}\\ln(P_{t+h}/P_t) - 1200\\ln(P_t/P_{t-1})$",
                    "$1200\\ln(P_{t+h}/P_{t+h-1})$",
                    "$\\ln P_{t+h}$"
                ],
                "correctExplanation": "For prices the target is the average inflation over the next $h$ months minus current inflation: the change of inflation, which is I(0).",
                "incorrectExplanation": "The first option is the target for real series; the third is one month of inflation at $t + h$; the log level is I(2)."
            },
            "ro": {
                "title": "Ținta indicilor de difuziune pentru prețuri",
                "text": "În Stock și Watson (2002, JBES), care este ținta la $h$ pași pentru un indice de prețuri $P_t$ (o serie I(2) în logaritmi)?",
                "options": [
                    "$\\frac{1200}{h}\\ln(P_{t+h}/P_t)$",
                    "$\\frac{1200}{h}\\ln(P_{t+h}/P_t) - 1200\\ln(P_t/P_{t-1})$",
                    "$1200\\ln(P_{t+h}/P_{t+h-1})$",
                    "$\\ln P_{t+h}$"
                ],
                "correctExplanation": "Pentru prețuri ținta este inflația medie din următoarele $h$ luni minus inflația curentă: variația inflației, care este I(0).",
                "incorrectExplanation": "Prima variantă este ținta pentru seriile reale; a treia este inflația unei singure luni la $t + h$; logaritmul nivelului este I(2)."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "FAVAR in two steps",
                "text": "In the two-step FAVAR of Bernanke, Boivin and Eliasz (2005), how is the policy rate removed from the estimated factors?",
                "options": [
                    "By ordering the funds rate first in a Cholesky decomposition",
                    "By dropping all interest rates from the panel",
                    "By regressing the principal components on slow-moving factors and the funds rate and subtracting the funds-rate part",
                    "By differencing the factors twice"
                ],
                "correctExplanation": "Slow-moving factors cannot respond to the policy shock within the month, so $\\hat F_t = \\hat C_t - \\hat b_Y Y_t$ removes the direct contemporaneous effect of the rate.",
                "incorrectExplanation": "The funds rate is ordered last; interest rates stay in the panel as fast-moving series; differencing does not remove the rate."
            },
            "ro": {
                "title": "FAVAR în doi pași",
                "text": "În FAVAR-ul în doi pași al lui Bernanke, Boivin și Eliasz (2005), cum se elimină dobînda de politică din factorii estimați?",
                "options": [
                    "Ordonînd dobînda federal funds prima într-o descompunere Cholesky",
                    "Eliminînd toate dobînzile din panel",
                    "Regresînd componentele principale pe factorii lenți și pe dobîndă și scăzînd partea dobînzii",
                    "Diferențiind factorii de două ori"
                ],
                "correctExplanation": "Factorii lenți nu pot răspunde la șocul de politică în aceeași lună, deci $\\hat F_t = \\hat C_t - \\hat b_Y Y_t$ elimină efectul contemporan direct al dobînzii.",
                "incorrectExplanation": "Dobînda este ordonată ultima; dobînzile rămîn în panel ca serii rapide; diferențierea nu elimină dobînda."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Months and quarters",
                "text": "Quarterly GDP is the 3-month average of a latent monthly level. With monthly growth rates $y_t$, what are the Mariano–Murasawa weights of $(y_t, \\dots, y_{t-4})$ in quarterly growth?",
                "options": [
                    "$(1, 1, 1, 0, 0)/3$",
                    "$(1, 1, 1, 1, 1)/5$",
                    "$(3, 2, 1, 0, 0)/6$",
                    "$(1, 2, 3, 2, 1)/3$"
                ],
                "correctExplanation": "Writing each three-month log difference of the averages as a sum of monthly growth rates gives the triangular weights $(1, 2, 3, 2, 1)/3$.",
                "incorrectExplanation": "The other weights treat the quarter as the sum of its own months only, or average five months equally; they ignore the overlap of the averages."
            },
            "ro": {
                "title": "Luni și trimestre",
                "text": "PIB-ul trimestrial este media pe 3 luni a unui nivel lunar latent. Cu ratele lunare de creștere $y_t$, care sînt ponderile Mariano–Murasawa ale lui $(y_t, \\dots, y_{t-4})$ în creșterea trimestrială?",
                "options": [
                    "$(1, 1, 1, 0, 0)/3$",
                    "$(1, 1, 1, 1, 1)/5$",
                    "$(3, 2, 1, 0, 0)/6$",
                    "$(1, 2, 3, 2, 1)/3$"
                ],
                "correctExplanation": "Scriind fiecare diferență de logaritmi pe trei luni a mediilor ca sumă de rate lunare obținem ponderile triunghiulare $(1, 2, 3, 2, 1)/3$.",
                "incorrectExplanation": "Celelalte ponderi tratează trimestrul doar ca suma propriilor luni sau mediază egal cinci luni; ignoră suprapunerea mediilor."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "What news is",
                "text": "In the news decomposition of Bańbura and Modugno (2014), what is the news of a new release $x_j$?",
                "options": [
                    "$x_j - \\mathrm{E}[x_j\\mid\\Omega_{old}]$, the surprise relative to the model forecast",
                    "The released value $x_j$",
                    "The revision of $x_j$ by the statistical office",
                    "The loading of $x_j$ on the factor"
                ],
                "correctExplanation": "Only the unexpected part of a release can change the nowcast; a release equal to its model forecast has zero news.",
                "incorrectExplanation": "The released value includes the predictable part; data revisions are a separate source of change; the loading enters the weight, not the news."
            },
            "ro": {
                "title": "Ce este o știre",
                "text": "În descompunerea în știri a lui Bańbura și Modugno (2014), care este știrea unei publicări noi $x_j$?",
                "options": [
                    "$x_j - \\mathrm{E}[x_j\\mid\\Omega_{old}]$, surpriza față de prognoza modelului",
                    "Valoarea publicată $x_j$",
                    "Revizuirea lui $x_j$ de către institutul de statistică",
                    "Ponderea factorială a lui $x_j$"
                ],
                "correctExplanation": "Doar partea neașteptată a unei publicări poate schimba nowcast-ul; o publicare egală cu prognoza modelului are știrea zero.",
                "incorrectExplanation": "Valoarea publicată include partea previzibilă; revizuirile datelor sînt o sursă separată de schimbare; ponderea factorială intră în greutate, nu în știre."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "News adds up",
                "text": "With the model parameters held fixed and no data revisions, how does the revision of a nowcast relate to the news?",
                "options": [
                    "It is approximately equal to the largest single news",
                    "It equals exactly $\\sum_j w_j I_j$ with $w = \\mathrm{E}[yI']\\mathrm{E}[II']^{-1}$",
                    "It equals the average of the news",
                    "It cannot be decomposed when releases are correlated"
                ],
                "correctExplanation": "Gaussian projection: the update of $\\mathrm{E}[y\\mid\\Omega]$ is a linear function of the innovations of the new releases; in the lecture the eleven impacts add up exactly to the revision.",
                "incorrectExplanation": "All releases contribute; the weights are not equal; correlation is handled by $\\mathrm{E}[II']^{-1}$, which splits the weight among correlated releases."
            },
            "ro": {
                "title": "Știrile se adună",
                "text": "Cu parametrii modelului ficși și fără revizuiri ale datelor, cum se leagă revizuirea unui nowcast de știri?",
                "options": [
                    "Este aproximativ egală cu cea mai mare știre",
                    "Este exact $\\sum_j w_j I_j$ cu $w = \\mathrm{E}[yI']\\mathrm{E}[II']^{-1}$",
                    "Este media știrilor",
                    "Nu poate fi descompusă cînd publicările sînt corelate"
                ],
                "correctExplanation": "Proiecția gaussiană: actualizarea lui $\\mathrm{E}[y\\mid\\Omega]$ este o funcție liniară de inovațiile noilor publicări; în curs cele unsprezece impacturi însumează exact revizuirea.",
                "incorrectExplanation": "Toate publicările contribuie; ponderile nu sînt egale; corelația este tratată de $\\mathrm{E}[II']^{-1}$, care împarte ponderea între publicările corelate."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Exponential Almon",
                "text": "Why does MIDAS use a parametric lag polynomial such as the exponential Almon $w_j(\\theta) \\propto e^{\\theta_1 j + \\theta_2 j^2}$?",
                "options": [
                    "Because OLS cannot be used with mixed frequencies",
                    "Because the weights must be negative",
                    "Because two parameters describe the weights of many high-frequency lags, avoiding parameter proliferation",
                    "Because it makes the regression linear in $\\theta$"
                ],
                "correctExplanation": "With $K$ monthly or daily lags an unrestricted polynomial needs $K$ coefficients; the Almon form needs two, estimated by nonlinear least squares.",
                "incorrectExplanation": "Unrestricted MIDAS is estimated by OLS when $K$ is small; the weights are positive; the model is nonlinear in $\\theta$."
            },
            "ro": {
                "title": "Almon exponențial",
                "text": "De ce folosește MIDAS un polinom parametric al decalajelor, precum Almon exponențial $w_j(\\theta) \\propto e^{\\theta_1 j + \\theta_2 j^2}$?",
                "options": [
                    "Pentru că OLS nu poate fi folosit cu frecvențe mixte",
                    "Pentru că ponderile trebuie să fie negative",
                    "Pentru că doi parametri descriu ponderile multor decalaje de frecvență înaltă, evitînd înmulțirea parametrilor",
                    "Pentru că face regresia liniară în $\\theta$"
                ],
                "correctExplanation": "Cu $K$ decalaje lunare sau zilnice un polinom nerestricționat cere $K$ coeficienți; forma Almon cere doi, estimați prin cele mai mici pătrate neliniare.",
                "incorrectExplanation": "MIDAS nerestricționat se estimează prin OLS cînd $K$ este mic; ponderile sînt pozitive; modelul este neliniar în $\\theta$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The ragged edge",
                "text": "At the end of the sample industrial production stops two months earlier than the surveys. How does the Kalman filter of a dynamic factor model handle the missing values?",
                "options": [
                    "It replaces them with zeros",
                    "It drops the whole month for every series",
                    "It interpolates them linearly first",
                    "It keeps only the observed rows of the measurement equation at each date"
                ],
                "correctExplanation": "The measurement equation is restricted to the available series with a selection matrix; the prediction step continues, so every observed value is used.",
                "incorrectExplanation": "Zeros would be treated as data, dropping the month wastes the surveys, and interpolation is impossible at the end of the sample."
            },
            "ro": {
                "title": "Datele incomplete la sfîrșitul eșantionului",
                "text": "La sfîrșitul eșantionului producția industrială se oprește cu două luni înaintea anchetelor. Cum tratează filtrul Kalman al unui model factorial dinamic valorile lipsă?",
                "options": [
                    "Le înlocuiește cu zerouri",
                    "Elimină întreaga lună pentru toate seriile",
                    "Le interpolează mai întîi liniar",
                    "Păstrează la fiecare dată doar liniile observate ale ecuației de măsurare"
                ],
                "correctExplanation": "Ecuația de măsurare se restrînge la seriile disponibile cu o matrice de selecție; pasul de predicție continuă, deci fiecare valoare observată este folosită.",
                "incorrectExplanation": "Zerourile ar fi tratate ca date, eliminarea lunii risipește anchetele, iar interpolarea este imposibilă la sfîrșitul eșantionului."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant says: 'Estimate the 102-variable VAR(13) by OLS on each 10-year window; OLS is unbiased, so its forecasts will be the most accurate.' What is wrong?",
                "options": [
                    "With $k = 1\\,327$ regressors and $T = 120$, $X'X$ is singular: OLS does not exist, and unbiasedness would not imply low MSE anyway",
                    "Nothing: OLS is the best linear unbiased estimator",
                    "The VAR should have 26 lags, not 13",
                    "OLS forecasts are biased only for the funds rate"
                ],
                "correctExplanation": "When regressors outnumber observations the normal equations have no unique solution; even with $k < T$, variance dominates the forecast error, which is why shrinkage wins.",
                "incorrectExplanation": "Unbiasedness says nothing about variance; the lag length is not the issue; the problem concerns every equation."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI spune: „Estimați VAR(13) cu 102 variabile prin OLS pe fiecare fereastră de 10 ani; OLS este nedeplasat, deci prognozele lui vor fi cele mai precise.” Ce este greșit?",
                "options": [
                    "Cu $k = 1\\,327$ de regresori și $T = 120$, $X'X$ este singulară: OLS nu există, iar nedeplasarea nu ar implica oricum un MSE mic",
                    "Nimic: OLS este cel mai bun estimator liniar nedeplasat",
                    "VAR-ul ar trebui să aibă 26 de decalaje, nu 13",
                    "Prognozele OLS sînt deplasate doar pentru dobînda federal funds"
                ],
                "correctExplanation": "Cînd regresorii depășesc observațiile, ecuațiile normale nu au soluție unică; chiar cu $k < T$ varianța domină eroarea de prognoză, de aceea shrinkage-ul cîștigă.",
                "incorrectExplanation": "Nedeplasarea nu spune nimic despre varianță; numărul de decalaje nu este problema; problema privește fiecare ecuație."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant comments a nowcast update: 'Romanian industrial production for July was released and it is a large number, so it must have moved the GDP nowcast a lot.' What is wrong?",
                "options": [
                    "Industrial production never enters a GDP nowcast",
                    "A release moves the nowcast only through its surprise relative to the model forecast, times its weight; a large but expected value moves nothing",
                    "Releases only matter in the third month of the quarter",
                    "Only surveys can revise a nowcast"
                ],
                "correctExplanation": "The impact is $w_j(x_j - \\mathrm{E}[x_j\\mid\\Omega_{old}])$; in the lecture the July IP release did matter, but because it came 3.7 pp below the model's expectation.",
                "incorrectExplanation": "Industrial production is a key hard indicator; releases matter in every month; hard data moved the September 2026 nowcast more than the surveys."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI comentează o actualizare a nowcast-ului: „Producția industrială a României pentru iulie a fost publicată și este o cifră mare, deci a mișcat mult nowcast-ul PIB.” Ce este greșit?",
                "options": [
                    "Producția industrială nu intră niciodată într-un nowcast al PIB",
                    "O publicare mișcă nowcast-ul doar prin surpriza față de prognoza modelului, înmulțită cu ponderea ei; o valoare mare, dar așteptată, nu mișcă nimic",
                    "Publicările contează doar în a treia lună a trimestrului",
                    "Doar anchetele pot revizui un nowcast"
                ],
                "correctExplanation": "Impactul este $w_j(x_j - \\mathrm{E}[x_j\\mid\\Omega_{old}])$; în curs publicarea IP pentru iulie a contat, dar pentru că a venit cu 3,7 pp sub așteptarea modelului.",
                "incorrectExplanation": "Producția industrială este un indicator hard esențial; publicările contează în fiecare lună; datele hard au mișcat nowcast-ul din septembrie 2026 mai mult decît anchetele."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI summary of the Romanian nowcasting case says: 'The dynamic factor model significantly outperforms the AR benchmark at the end of the quarter.' What is wrong?",
                "options": [
                    "The DFM has a larger RMSE than the AR at every date",
                    "The comparison is not possible because the AR uses no monthly data",
                    "The RMSE is slightly lower, but the Diebold–Mariano test does not reject equal accuracy ($p \\approx 0.76$)",
                    "The DFM cannot be evaluated before 2020"
                ],
                "correctExplanation": "A lower point RMSE on about 50 quarters is not evidence of a better model; the lecture reports $t = -0.30$ and $p = 0.76$ at the end of month 3.",
                "incorrectExplanation": "The DFM's RMSE is lower late in the quarter; models with different information sets can be compared on the same targets; the evaluation covers 2013–2026."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un rezumat AI al studiului de caz de nowcasting pentru România spune: „Modelul factorial dinamic depășește semnificativ reperul AR la sfîrșitul trimestrului.” Ce este greșit?",
                "options": [
                    "DFM are un RMSE mai mare decît AR la fiecare dată",
                    "Comparația nu este posibilă pentru că AR nu folosește date lunare",
                    "RMSE este ușor mai mic, dar testul Diebold–Mariano nu respinge acuratețea egală ($p \\approx 0{,}76$)",
                    "DFM nu poate fi evaluat înainte de 2020"
                ],
                "correctExplanation": "Un RMSE punctual mai mic pe aproximativ 50 de trimestre nu este o dovadă a unui model mai bun; cursul raportează $t = -0{,}30$ și $p = 0{,}76$ la sfîrșitul lunii 3.",
                "incorrectExplanation": "RMSE al DFM este mai mic spre sfîrșitul trimestrului; modelele cu seturi de informații diferite pot fi comparate pe aceleași ținte; evaluarea acoperă 2013–2026."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant claims: 'A homoskedastic Gaussian BVAR estimated on rolling windows handles March–April 2020 automatically, because the prior shrinks everything.' What is wrong?",
                "options": [
                    "Nothing: shrinkage removes outliers",
                    "The prior only affects the constant",
                    "The pandemic months affect only the funds rate",
                    "The pandemic months are fitted as ordinary dynamics; in the lecture the 12-month employment MSFE explodes, which calls for rescaling their variance or stochastic volatility"
                ],
                "correctExplanation": "Shrinkage acts on coefficients, not on the error distribution; April 2020 is about 176 times the median squared residual, so the windows containing it distort the dynamics (Lenza and Primiceri 2022).",
                "incorrectExplanation": "Shrinkage does not downweight observations; the prior acts on all slope coefficients; employment and CPI are affected as well."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI afirmă: „Un BVAR gaussian homoscedastic estimat pe ferestre mobile tratează automat lunile martie–aprilie 2020, pentru că distribuția a priori strînge totul.” Ce este greșit?",
                "options": [
                    "Nimic: shrinkage-ul elimină valorile extreme",
                    "Distribuția a priori afectează doar termenul liber",
                    "Lunile pandemiei afectează doar dobînda federal funds",
                    "Lunile pandemiei sînt potrivite ca dinamică obișnuită; în curs MSFE la 12 luni pentru ocupare explodează, ceea ce cere rescalarea varianței lor sau volatilitate stochastică"
                ],
                "correctExplanation": "Shrinkage-ul acționează asupra coeficienților, nu asupra distribuției erorilor; aprilie 2020 este de aproximativ 176 de ori reziduul pătratic median, deci ferestrele care îl conțin distorsionează dinamica (Lenza și Primiceri 2022).",
                "incorrectExplanation": "Shrinkage-ul nu reduce ponderea observațiilor; distribuția a priori acționează asupra tuturor coeficienților; ocuparea și IPC sînt și ele afectate."
            }
        }
    ]
};
