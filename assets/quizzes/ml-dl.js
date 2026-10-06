// ============================================================
// Chapter 12 quiz bank: Machine learning and deep learning for time series (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['ml-dl'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Validity of K-fold CV",
                "text": "According to Bergmeir, Hyndman and Koo (2018), when does random K-fold cross-validation give asymptotically unbiased error estimates for an autoregressive forecasting model?",
                "options": [
                    "When the model's errors are uncorrelated, as for a well-specified autoregression",
                    "Only when the series is i.i.d.",
                    "Never: only out-of-sample evaluation is valid for time series",
                    "Whenever the series is stationary, whatever the model"
                ],
                "correctExplanation": "With uncorrelated errors a test row shares no error with the training rows, so the K-fold estimate is unbiased and, using every row, more precise than OOS.",
                "incorrectExplanation": "Stationarity alone is not enough (an under-specified model leaves autocorrelated errors), and K-fold is not restricted to i.i.d. data."
            },
            "ro": {
                "title": "Validitatea validării cu K subeșantioane",
                "text": "Potrivit lui Bergmeir, Hyndman și Koo (2018), cînd dă validarea încrucișată cu K subeșantioane aleatoare estimații asimptotic nedeplasate ale erorii pentru un model autoregresiv de prognoză?",
                "options": [
                    "Cînd erorile modelului sînt necorelate, ca pentru o autoregresie bine specificată",
                    "Doar cînd seria este i.i.d.",
                    "Niciodată: pentru serii de timp este validă doar evaluarea în afara eșantionului",
                    "Ori de cîte ori seria este staționară, indiferent de model"
                ],
                "correctExplanation": "Cu erori necorelate, un rînd de test nu are nicio eroare comună cu rîndurile de antrenare, deci estimația este nedeplasată și, folosind toate rîndurile, mai precisă decît OOS.",
                "incorrectExplanation": "Staționaritatea singură nu este suficientă (un model subspecificat lasă erori autocorelate), iar validarea nu este limitată la date i.i.d."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Overlapping targets",
                "text": "The target is the mean of the next h = 22 values of a white-noise series. What is the correlation between the targets of two consecutive rows?",
                "options": [
                    "1/22",
                    "21/22",
                    "0",
                    "1/2"
                ],
                "correctExplanation": "The two means share 21 of their 22 terms, so the correlation is (h - 1)/h = 21/22.",
                "incorrectExplanation": "Consecutive 22-day means overlap almost completely; their correlation is far from zero or one half."
            },
            "ro": {
                "title": "Ținte suprapuse",
                "text": "Ținta este media următoarelor h = 22 de valori ale unui zgomot alb. Care este corelația dintre țintele a două rînduri consecutive?",
                "options": [
                    "1/22",
                    "21/22",
                    "0",
                    "1/2"
                ],
                "correctExplanation": "Cele două medii au în comun 21 din cei 22 de termeni, deci corelația este (h - 1)/h = 21/22.",
                "incorrectExplanation": "Mediile consecutive pe 22 de zile se suprapun aproape complet; corelația lor este departe de zero sau de o jumătate."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The variance floor of bagging",
                "text": "B identically distributed trees have variance $\\sigma^2$ and pairwise correlation $\\rho$. What is the variance of their average as $B \\to \\infty$?",
                "options": [
                    "0",
                    "$\\sigma^2/B$",
                    "$\\rho\\sigma^2$",
                    "$(1 - \\rho)\\sigma^2$"
                ],
                "correctExplanation": "The variance is $\\rho\\sigma^2 + (1 - \\rho)\\sigma^2/B$; only the second term vanishes with B.",
                "incorrectExplanation": "Adding trees removes only the independent part; the correlated part $\\rho\\sigma^2$ remains."
            },
            "ro": {
                "title": "Pragul varianței în bagging",
                "text": "B arbori identic distribuiți au varianța $\\sigma^2$ și corelația între perechi $\\rho$. Care este varianța mediei lor cînd $B \\to \\infty$?",
                "options": [
                    "0",
                    "$\\sigma^2/B$",
                    "$\\rho\\sigma^2$",
                    "$(1 - \\rho)\\sigma^2$"
                ],
                "correctExplanation": "Varianța este $\\rho\\sigma^2 + (1 - \\rho)\\sigma^2/B$; doar al doilea termen dispare cu B.",
                "incorrectExplanation": "Adăugarea de arbori elimină doar partea independentă; partea corelată $\\rho\\sigma^2$ rămîne."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Soft thresholding",
                "text": "Under an orthonormal design the OLS coefficient of a predictor is $z = 1.2$. What is its lasso coefficient for $\\lambda = 0.5$?",
                "options": [
                    "0.8",
                    "1.2",
                    "0",
                    "0.7"
                ],
                "correctExplanation": "Soft thresholding gives $\\mathrm{sign}(z)(|z| - \\lambda)_+ = 1.2 - 0.5 = 0.7$.",
                "incorrectExplanation": "0.8 is the ridge value $z/(1 + \\lambda)$; the lasso sets the coefficient to zero only when $|z| \\le \\lambda$."
            },
            "ro": {
                "title": "Pragul moale",
                "text": "Cu design ortonormal, coeficientul OLS al unui predictor este $z = 1{,}2$. Care este coeficientul lui lasso pentru $\\lambda = 0{,}5$?",
                "options": [
                    "0,8",
                    "1,2",
                    "0",
                    "0,7"
                ],
                "correctExplanation": "Pragul moale dă $\\mathrm{sign}(z)(|z| - \\lambda)_+ = 1{,}2 - 0{,}5 = 0{,}7$.",
                "incorrectExplanation": "0,8 este valoarea ridge $z/(1 + \\lambda)$; lasso anulează coeficientul doar cînd $|z| \\le \\lambda$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Adaptive lasso",
                "text": "Which property does the adaptive lasso (weights $1/|\\tilde\\beta_j|^\\gamma$) obtain without the irrepresentable condition?",
                "options": [
                    "Consistent selection with asymptotically Normal estimates of the non-zero coefficients (the oracle property)",
                    "Exact finite-sample confidence intervals after selection",
                    "Selection of all correlated predictors as a group",
                    "A prediction error smaller than that of OLS in every sample"
                ],
                "correctExplanation": "Zou (2006) shows that data-dependent weights give the oracle property: the right model is selected and the non-zero coefficients are estimated as if it were known.",
                "incorrectExplanation": "Grouping correlated predictors is the elastic net; exact post-selection intervals need conditional inference; no estimator dominates OLS in every sample."
            },
            "ro": {
                "title": "Lasso adaptiv",
                "text": "Ce proprietate obține lasso-ul adaptiv (ponderi $1/|\\tilde\\beta_j|^\\gamma$) fără condiția de nereprezentare?",
                "options": [
                    "Selecție consistentă cu estimații asimptotic normale ale coeficienților nenuli (proprietatea de oracol)",
                    "Intervale de încredere exacte în eșantion finit după selecție",
                    "Selecția în grup a tuturor predictorilor corelați",
                    "O eroare de predicție mai mică decît cea OLS în orice eșantion"
                ],
                "correctExplanation": "Zou (2006) arată că ponderile dependente de date dau proprietatea de oracol: modelul corect este selectat, iar coeficienții nenuli sînt estimați ca și cum el ar fi cunoscut.",
                "incorrectExplanation": "Gruparea predictorilor corelați este elastic net; intervalele exacte după selecție cer inferență condiționată; niciun estimator nu domină OLS în orice eșantion."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Inference after the lasso",
                "text": "A researcher selects predictors with the lasso and then reports the OLS $t$-statistics of the selected ones. What is wrong?",
                "options": [
                    "Nothing, if the lasso penalty was chosen by cross-validation",
                    "The $p$-values are too small because the same data chose the model; post-selection or double-selection inference is needed",
                    "The $t$-statistics are too small because the lasso shrinks the coefficients",
                    "Nothing, if HAC standard errors are used"
                ],
                "correctExplanation": "The distribution of the estimates is conditional on being selected; PoSI, exact conditional intervals or double selection correct for it.",
                "incorrectExplanation": "Cross-validation and HAC errors address other problems; the OLS refit removes the shrinkage, so shrinkage is not the issue."
            },
            "ro": {
                "title": "Inferența după lasso",
                "text": "Un cercetător selectează predictorii cu lasso și apoi raportează statisticile $t$ OLS ale celor selectați. Ce este greșit?",
                "options": [
                    "Nimic, dacă penalizarea lasso a fost aleasă prin validare încrucișată",
                    "Valorile $p$ sînt prea mici pentru că aceleași date au ales modelul; este nevoie de inferență după selecție sau de dubla selecție",
                    "Statisticile $t$ sînt prea mici pentru că lasso micșorează coeficienții",
                    "Nimic, dacă se folosesc erori standard HAC"
                ],
                "correctExplanation": "Distribuția estimațiilor este condiționată de faptul că au fost selectate; PoSI, intervalele condiționate exacte sau dubla selecție corectează aceasta.",
                "incorrectExplanation": "Validarea încrucișată și erorile HAC tratează alte probleme; reestimarea OLS elimină micșorarea, deci nu aceasta este problema."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Quantile regression forests",
                "text": "How does a quantile regression forest (Meinshausen 2006) produce the $\\tau$-quantile at a point $x$?",
                "options": [
                    "By fitting one forest per quantile level with the pinball loss",
                    "By adding Normal quantiles of the residual variance to the forest mean",
                    "From the weighted empirical distribution of the training targets, with weights given by co-membership with $x$ in the leaves",
                    "From the spread of the predictions of the individual trees"
                ],
                "correctExplanation": "The leaves keep all training targets; the weights $w_i(x)$ average $1\\{x_i \\in L_b(x)\\}/|L_b(x)|$ over the trees.",
                "incorrectExplanation": "One forest gives all quantiles; neither a Normal assumption nor the dispersion of tree means is used."
            },
            "ro": {
                "title": "Păduri de regresie cuantilică",
                "text": "Cum produce o pădure de regresie cuantilică (Meinshausen 2006) cuantila de nivel $\\tau$ într-un punct $x$?",
                "options": [
                    "Estimînd o pădure pentru fiecare nivel cu pierderea pinball",
                    "Adăugînd la media pădurii cuantile normale ale varianței reziduale",
                    "Din distribuția empirică ponderată a țintelor de antrenare, cu ponderi date de apartenența comună cu $x$ la frunze",
                    "Din dispersia prognozelor arborilor individuali"
                ],
                "correctExplanation": "Frunzele păstrează toate țintele de antrenare; ponderile $w_i(x)$ mediază $1\\{x_i \\in L_b(x)\\}/|L_b(x)|$ pe arbori.",
                "incorrectExplanation": "O singură pădure dă toate cuantilele; nu se folosește nici o ipoteză normală, nici dispersia mediilor arborilor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Quantile boosting",
                "text": "In gradient boosting with the pinball loss of level $\\tau$, what does each new tree fit at observation $i$?",
                "options": [
                    "$y_i - F(x_i)$",
                    "$|y_i - F(x_i)|$",
                    "$\\tau(y_i - F(x_i))^2$",
                    "$\\tau - 1\\{y_i < F(x_i)\\}$"
                ],
                "correctExplanation": "The negative gradient of $\\rho_\\tau(y - F)$ with respect to F is $\\tau$ above the forecast and $\\tau - 1$ below it.",
                "incorrectExplanation": "The residual is the gradient of the squared loss; the other expressions are not gradients of the pinball loss."
            },
            "ro": {
                "title": "Boosting cuantilic",
                "text": "În gradient boosting cu pierderea pinball de nivel $\\tau$, ce ajustează fiecare arbore nou la observația $i$?",
                "options": [
                    "$y_i - F(x_i)$",
                    "$|y_i - F(x_i)|$",
                    "$\\tau(y_i - F(x_i))^2$",
                    "$\\tau - 1\\{y_i < F(x_i)\\}$"
                ],
                "correctExplanation": "Gradientul negativ al lui $\\rho_\\tau(y - F)$ în raport cu F este $\\tau$ deasupra prognozei și $\\tau - 1$ sub ea.",
                "incorrectExplanation": "Reziduul este gradientul pierderii pătratice; celelalte expresii nu sînt gradienți ai pierderii pinball."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Second-order leaf values",
                "text": "In XGBoost-type boosting, a leaf collects gradient sum $G$ and Hessian sum $H$, with L2 penalty $\\lambda$. What is the optimal leaf value?",
                "options": [
                    "$-G/(H + \\lambda)$",
                    "$-G/H$",
                    "$-H/(G + \\lambda)$",
                    "$G^2/(H + \\lambda)$"
                ],
                "correctExplanation": "Minimising $Gw + \\frac12(H + \\lambda)w^2$ gives $w^* = -G/(H + \\lambda)$.",
                "incorrectExplanation": "The penalty enters the denominator; $G^2/(H + \\lambda)$ is (twice) the loss reduction, not the leaf value."
            },
            "ro": {
                "title": "Valorile frunzelor de ordinul doi",
                "text": "Într-un boosting de tip XGBoost, o frunză adună suma gradienților $G$ și suma hessianelor $H$, cu penalizarea L2 $\\lambda$. Care este valoarea optimă a frunzei?",
                "options": [
                    "$-G/(H + \\lambda)$",
                    "$-G/H$",
                    "$-H/(G + \\lambda)$",
                    "$G^2/(H + \\lambda)$"
                ],
                "correctExplanation": "Minimizarea lui $Gw + \\frac12(H + \\lambda)w^2$ dă $w^* = -G/(H + \\lambda)$.",
                "incorrectExplanation": "Penalizarea intră la numitor; $G^2/(H + \\lambda)$ este (de două ori) reducerea pierderii, nu valoarea frunzei."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Monotone constraints",
                "text": "A boosted model of day-ahead load is constrained to be increasing in yesterday's load at the same hour. What does the constraint guarantee?",
                "options": [
                    "A lower out-of-sample error than the unconstrained model",
                    "The fitted function is non-decreasing in that feature for every value of the other features",
                    "That the partial dependence is linear",
                    "That the feature receives the largest Shapley value"
                ],
                "correctExplanation": "Splits that violate the order are refused and children inherit bounds, so monotonicity holds everywhere.",
                "incorrectExplanation": "Constraints can cost accuracy (as at the Romanian evening peak) and say nothing about linearity or importance."
            },
            "ro": {
                "title": "Restricții de monotonie",
                "text": "Un model boosting pentru consumul din ziua următoare este restricționat să fie crescător în consumul de ieri la aceeași oră. Ce garantează restricția?",
                "options": [
                    "O eroare în afara eșantionului mai mică decît a modelului fără restricție",
                    "Funcția estimată este nedescrescătoare în acea variabilă pentru orice valori ale celorlalte variabile",
                    "Că dependența parțială este liniară",
                    "Că variabila primește cea mai mare valoare Shapley"
                ],
                "correctExplanation": "Ramificările care încalcă ordinea sînt refuzate, iar descendenții moștenesc limitele, deci monotonia este valabilă peste tot.",
                "incorrectExplanation": "Restricțiile pot costa acuratețe (ca la vîrful de seară din România) și nu spun nimic despre liniaritate sau importanță."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Vanishing gradients",
                "text": "For $h_t = \\tanh(Wh_{t-1} + Ux_t)$, which bound holds for $\\|\\partial h_T/\\partial h_t\\|$?",
                "options": [
                    "$\\|W\\|/(T - t)$",
                    "$\\gamma^{-(T-t)}\\|W\\|$",
                    "$(\\gamma\\|W\\|)^{T-t}$ with $\\gamma = \\max|\\tanh'| \\le 1$",
                    "$1$ for every lag"
                ],
                "correctExplanation": "The Jacobian is a product of $T - t$ factors $\\mathrm{diag}(1 - h_k^2)W$, each bounded by $\\gamma\\|W\\|$.",
                "incorrectExplanation": "The decay is geometric in the lag, not hyperbolic, and it does not stay at one."
            },
            "ro": {
                "title": "Gradienți care se sting",
                "text": "Pentru $h_t = \\tanh(Wh_{t-1} + Ux_t)$, ce margine este valabilă pentru $\\|\\partial h_T/\\partial h_t\\|$?",
                "options": [
                    "$\\|W\\|/(T - t)$",
                    "$\\gamma^{-(T-t)}\\|W\\|$",
                    "$(\\gamma\\|W\\|)^{T-t}$ cu $\\gamma = \\max|\\tanh'| \\le 1$",
                    "$1$ pentru orice decalaj"
                ],
                "correctExplanation": "Jacobianul este un produs de $T - t$ factori $\\mathrm{diag}(1 - h_k^2)W$, fiecare mărginit de $\\gamma\\|W\\|$.",
                "incorrectExplanation": "Stingerea este geometrică în decalaj, nu hiperbolică, și nu rămîne la unu."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The LSTM forget gate",
                "text": "An LSTM is initialised with forget-gate bias 0, so $f \\approx 0.5$. By roughly how much is the cell-state gradient reduced after 10 steps along the direct path?",
                "options": [
                    "Not at all: the cell path is additive",
                    "By a factor of 2",
                    "By a factor of 10",
                    "By a factor of about 1000 ($0.5^{10} \\approx 0.001$)"
                ],
                "correctExplanation": "Along the cell, $\\partial c_t/\\partial c_{t-1} = f_t$; ten steps give $0.5^{10} \\approx 0.001$.",
                "incorrectExplanation": "Additivity removes the tanh squashing, but the forget gate still multiplies the gradient at each step."
            },
            "ro": {
                "title": "Poarta de uitare LSTM",
                "text": "Un LSTM este inițializat cu bias 0 al porții de uitare, deci $f \\approx 0{,}5$. Cu cît se reduce aproximativ gradientul stării celulei după 10 pași pe drumul direct?",
                "options": [
                    "Deloc: drumul celulei este aditiv",
                    "De 2 ori",
                    "De 10 ori",
                    "De aproximativ 1000 de ori ($0{,}5^{10} \\approx 0{,}001$)"
                ],
                "correctExplanation": "De-a lungul celulei, $\\partial c_t/\\partial c_{t-1} = f_t$; zece pași dau $0{,}5^{10} \\approx 0{,}001$.",
                "incorrectExplanation": "Aditivitatea elimină compresia tanh, dar poarta de uitare înmulțește în continuare gradientul la fiecare pas."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Receptive field of a TCN",
                "text": "A TCN has kernel size 3 and five levels with dilations 1, 2, 4, 8, 16, each level containing two dilated causal convolutions. What is its receptive field?",
                "options": [
                    "125",
                    "63",
                    "31",
                    "243"
                ],
                "correctExplanation": "$R = 1 + 2(k - 1)(2^\\ell - 1) = 1 + 2 \\cdot 2 \\cdot 31 = 125$.",
                "incorrectExplanation": "63 counts one convolution per level; 31 is $2^5 - 1$; 243 is $3^5$."
            },
            "ro": {
                "title": "Cîmpul receptiv al unui TCN",
                "text": "Un TCN are nucleul 3 și cinci niveluri cu dilatările 1, 2, 4, 8, 16, fiecare nivel avînd două convoluții cauzale dilatate. Care este cîmpul lui receptiv?",
                "options": [
                    "125",
                    "63",
                    "31",
                    "243"
                ],
                "correctExplanation": "$R = 1 + 2(k - 1)(2^\\ell - 1) = 1 + 2 \\cdot 2 \\cdot 31 = 125$.",
                "incorrectExplanation": "63 numără o singură convoluție pe nivel; 31 este $2^5 - 1$; 243 este $3^5$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Attention and order",
                "text": "What happens to the output of self-attention without positional encodings if the input tokens are permuted?",
                "options": [
                    "The output is unchanged token by token",
                    "The outputs are permuted in the same way: the order of the tokens is ignored",
                    "The attention weights become uniform",
                    "The softmax is no longer defined"
                ],
                "correctExplanation": "Self-attention is permutation equivariant; only positional encodings give it the order of a time series.",
                "incorrectExplanation": "The weights are permuted with the tokens; they do not become uniform and nothing becomes undefined."
            },
            "ro": {
                "title": "Atenția și ordinea",
                "text": "Ce se întîmplă cu ieșirea auto-atenției fără codificări poziționale dacă tokenii de intrare sînt permutați?",
                "options": [
                    "Ieșirea nu se schimbă, token cu token",
                    "Ieșirile sînt permutate la fel: ordinea tokenilor este ignorată",
                    "Ponderile atenției devin uniforme",
                    "Softmax nu mai este definit"
                ],
                "correctExplanation": "Auto-atenția este echivariantă la permutări; doar codificările poziționale îi dau ordinea unei serii de timp.",
                "incorrectExplanation": "Ponderile se permută odată cu tokenii; nu devin uniforme și nimic nu devine nedefinit."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "DLinear",
                "text": "DLinear splits the input window $x$ into a moving-average trend $Ax$ and a remainder, with one linear layer each. Which statement is correct?",
                "options": [
                    "It is a nonlinear model because of the decomposition",
                    "It has a larger function class than the plain Linear model",
                    "Its forecast equals $Wx$ with $W = W_s(I - A) + W_tA$: it is one linear map",
                    "It needs attention to combine trend and remainder"
                ],
                "correctExplanation": "Both parts are linear in $x$, so their sum is one linear map; the decomposition only changes the parametrisation.",
                "incorrectExplanation": "The function class equals that of Linear; there is no nonlinearity and no attention."
            },
            "ro": {
                "title": "DLinear",
                "text": "DLinear separă fereastra de intrare $x$ într-un trend prin medie mobilă $Ax$ și un rest, cu cîte un strat liniar. Ce afirmație este corectă?",
                "options": [
                    "Este un model neliniar din cauza descompunerii",
                    "Are o clasă de funcții mai largă decît modelul Linear simplu",
                    "Prognoza lui este $Wx$ cu $W = W_s(I - A) + W_tA$: o singură aplicație liniară",
                    "Are nevoie de atenție pentru a combina trendul și restul"
                ],
                "correctExplanation": "Ambele părți sînt liniare în $x$, deci suma lor este o singură aplicație liniară; descompunerea schimbă doar parametrizarea.",
                "incorrectExplanation": "Clasa de funcții este aceeași cu a modelului Linear; nu există neliniaritate și nici atenție."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The critique of Zeng et al.",
                "text": "Which finding is reported by Zeng et al. (2023), 'Are Transformers effective for time series forecasting?'",
                "options": [
                    "Patch-based Transformers are always worse than linear models",
                    "Transformers cannot be trained on more than 336 time steps",
                    "Linear models beat every deep model on the M4 competition",
                    "One-layer linear models beat Informer, Autoformer and their successors on most standard long-horizon benchmarks"
                ],
                "correctExplanation": "They compared point-token Transformers with Linear, NLinear and DLinear on long-horizon benchmarks; PatchTST came later and beat DLinear.",
                "incorrectExplanation": "Their claim concerns the Transformers they tested on those benchmarks, not patch Transformers or the M4 data."
            },
            "ro": {
                "title": "Critica lui Zeng et al.",
                "text": "Ce rezultat raportează Zeng et al. (2023), „Are Transformers effective for time series forecasting?”",
                "options": [
                    "Transformers pe segmente sînt întotdeauna mai slabe decît modelele liniare",
                    "Transformers nu pot fi antrenate pe mai mult de 336 de pași",
                    "Modelele liniare bat orice model deep în competiția M4",
                    "Modelele liniare cu un strat bat Informer, Autoformer și succesorii lor pe majoritatea seturilor standard pentru orizonturi lungi"
                ],
                "correctExplanation": "Au comparat Transformers cu tokeni punctuali cu Linear, NLinear și DLinear pe seturi pentru orizonturi lungi; PatchTST a apărut ulterior și a bătut DLinear.",
                "incorrectExplanation": "Afirmația lor privește Transformers testate pe acele seturi, nu Transformers pe segmente sau datele M4."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "PatchTST",
                "text": "What is the main design change of PatchTST (Nie et al. 2023) relative to earlier long-horizon Transformers?",
                "options": [
                    "Tokens are patches of consecutive values, and each channel is modelled separately",
                    "Attention is replaced by a moving average",
                    "Every time step is a token with a learned positional encoding",
                    "The decoder generates the horizon one step at a time"
                ],
                "correctExplanation": "Patching gives each token local meaning and reduces the number of tokens; channel independence shares weights across series.",
                "incorrectExplanation": "Point tokens are exactly what PatchTST abandons; it keeps attention and outputs the horizon with a linear head."
            },
            "ro": {
                "title": "PatchTST",
                "text": "Care este principala schimbare de design a PatchTST (Nie et al. 2023) față de Transformers anterioare pentru orizonturi lungi?",
                "options": [
                    "Tokenii sînt segmente de valori consecutive, iar fiecare canal este modelat separat",
                    "Atenția este înlocuită cu o medie mobilă",
                    "Fiecare moment de timp este un token cu o codificare pozițională învățată",
                    "Decodorul generează orizontul pas cu pas"
                ],
                "correctExplanation": "Segmentarea dă fiecărui token o semnificație locală și reduce numărul de tokeni; independența canalelor partajează ponderile între serii.",
                "incorrectExplanation": "Tokenii punctuali sînt exact ce abandonează PatchTST; el păstrează atenția și dă orizontul printr-un cap liniar."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "N-BEATS",
                "text": "In N-BEATS, what does block $\\ell + 1$ receive as input?",
                "options": [
                    "The forecast of block $\\ell$",
                    "The input of block $\\ell$ minus its backcast, $x_{\\ell+1} = x_\\ell - \\hat x_\\ell$",
                    "The original window, unchanged",
                    "The residuals of a seasonal naive forecast"
                ],
                "correctExplanation": "Doubly residual stacking: each block removes what it explains from the input, and the forecasts of all blocks are summed.",
                "incorrectExplanation": "The forecasts are summed, not passed on; the input changes from block to block."
            },
            "ro": {
                "title": "N-BEATS",
                "text": "În N-BEATS, ce primește ca intrare blocul $\\ell + 1$?",
                "options": [
                    "Prognoza blocului $\\ell$",
                    "Intrarea blocului $\\ell$ minus reconstrucția lui, $x_{\\ell+1} = x_\\ell - \\hat x_\\ell$",
                    "Fereastra originală, neschimbată",
                    "Reziduurile unei prognoze naive sezoniere"
                ],
                "correctExplanation": "Stivuirea dublu reziduală: fiecare bloc scade din intrare ce explică, iar prognozele tuturor blocurilor se adună.",
                "incorrectExplanation": "Prognozele se adună, nu se transmit mai departe; intrarea se schimbă de la un bloc la altul."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "N-HiTS",
                "text": "What distinguishes N-HiTS (Challu et al. 2023) from N-BEATS?",
                "options": [
                    "Blocks use attention between the input and the forecast",
                    "Each block is a separate recurrent network",
                    "Blocks max-pool their input at different rates and forecast few coefficients interpolated to the horizon",
                    "It replaces the backcast by the seasonal naive forecast"
                ],
                "correctExplanation": "Multi-rate pooling and hierarchical interpolation force coarse blocks to model smooth, low-frequency components.",
                "incorrectExplanation": "N-HiTS keeps fully connected blocks and residual stacking; it adds neither attention nor recurrence."
            },
            "ro": {
                "title": "N-HiTS",
                "text": "Ce deosebește N-HiTS (Challu et al. 2023) de N-BEATS?",
                "options": [
                    "Blocurile folosesc atenție între intrare și prognoză",
                    "Fiecare bloc este o rețea recurentă separată",
                    "Blocurile aplică max-pooling pe intrare la rate diferite și prognozează puțini coeficienți interpolați pe orizont",
                    "Înlocuiește reconstrucția cu prognoza naivă sezonieră"
                ],
                "correctExplanation": "Pooling-ul pe mai multe rate și interpolarea ierarhică obligă blocurile grosiere să modeleze componente netede, de frecvență joasă.",
                "incorrectExplanation": "N-HiTS păstrează blocurile complet conectate și stivuirea reziduală; nu adaugă nici atenție, nici recurență."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "DeepAR",
                "text": "How does DeepAR (Salinas et al. 2020) produce a probabilistic forecast for $H$ steps?",
                "options": [
                    "By a separate quantile output for each horizon and level",
                    "By adding bootstrap residuals to a point forecast",
                    "By conformal calibration of a point forecast",
                    "By ancestral sampling: each draw from the predicted likelihood is fed back as the next input, and quantiles are taken over the sample paths"
                ],
                "correctExplanation": "The LSTM outputs the parameters of a likelihood; sampled paths give the joint predictive distribution.",
                "incorrectExplanation": "Quantile heads belong to the TFT and MQ-RNN; bootstrap and conformal methods are not part of DeepAR."
            },
            "ro": {
                "title": "DeepAR",
                "text": "Cum produce DeepAR (Salinas et al. 2020) o prognoză probabilistică pe $H$ pași?",
                "options": [
                    "Printr-o ieșire cuantilică separată pentru fiecare orizont și nivel",
                    "Adăugînd reziduuri bootstrap la o prognoză punctuală",
                    "Prin calibrarea conformală a unei prognoze punctuale",
                    "Prin simulare ancestrală: fiecare extragere din verosimilitatea prognozată este reintrodusă ca intrare următoare, iar cuantilele se iau pe traiectoriile simulate"
                ],
                "correctExplanation": "LSTM dă parametrii unei verosimilități; traiectoriile simulate dau distribuția predictivă comună.",
                "incorrectExplanation": "Ieșirile cuantilice aparțin TFT și MQ-RNN; metodele bootstrap și conformale nu fac parte din DeepAR."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Global models",
                "text": "Why can a global AR model of 27 inflation series afford a much longer memory than 27 local AR models?",
                "options": [
                    "It estimates one set of coefficients from all series, so the number of observations per parameter is about 27 times larger",
                    "Global models are immune to structural breaks",
                    "Pooling removes the autocorrelation of the errors",
                    "Global models need no lags"
                ],
                "correctExplanation": "With $NT$ rows for one coefficient vector, the variance of long-memory coefficients stays small (Montero-Manso and Hyndman 2021).",
                "incorrectExplanation": "Pooling does not remove breaks or residual autocorrelation; lags are still the inputs."
            },
            "ro": {
                "title": "Modele globale",
                "text": "De ce își poate permite un model AR global pentru 27 de serii de inflație o memorie mult mai lungă decît 27 de modele AR locale?",
                "options": [
                    "Estimează un singur set de coeficienți din toate seriile, deci numărul de observații pe parametru este de circa 27 de ori mai mare",
                    "Modelele globale sînt imune la rupturi structurale",
                    "Reunirea datelor elimină autocorelația erorilor",
                    "Modelele globale nu au nevoie de decalaje"
                ],
                "correctExplanation": "Cu $NT$ rînduri pentru un singur vector de coeficienți, varianța coeficienților cu memorie lungă rămîne mică (Montero-Manso și Hyndman 2021).",
                "incorrectExplanation": "Reunirea nu elimină rupturile sau autocorelația reziduală; decalajele rămîn intrările modelului."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Shapley efficiency",
                "text": "For interventional SHAP with a background sample, what do the Shapley values of all features at $x$ sum to?",
                "options": [
                    "$f(x)$",
                    "$f(x)$ minus the average prediction over the background",
                    "One",
                    "The variance of $f$ over the background"
                ],
                "correctExplanation": "Efficiency: $\\sum_g\\phi_g = v(\\mathrm{all}) - v(\\emptyset)$, with $v(\\emptyset)$ the mean prediction over the background.",
                "incorrectExplanation": "The base value is subtracted; the values are not normalised to one and do not decompose a variance."
            },
            "ro": {
                "title": "Eficiența valorilor Shapley",
                "text": "Pentru SHAP intervențional cu un eșantion de fundal, cu cît este egală suma valorilor Shapley ale tuturor variabilelor în $x$?",
                "options": [
                    "$f(x)$",
                    "$f(x)$ minus prognoza medie pe eșantionul de fundal",
                    "Unu",
                    "Varianța lui $f$ pe eșantionul de fundal"
                ],
                "correctExplanation": "Eficiența: $\\sum_g\\phi_g = v(\\mathrm{toate}) - v(\\emptyset)$, cu $v(\\emptyset)$ prognoza medie pe eșantionul de fundal.",
                "incorrectExplanation": "Valoarea de bază se scade; valorile nu sînt normalizate la unu și nu descompun o varianță."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: 'The Transformer puts most attention on the patch from 14 days ago, so that patch drives the forecast.' On the chapter's model the last day carried most of the occlusion importance. What is the error?",
                "options": [
                    "The attention weights were computed on the training set",
                    "Occlusion importance is always proportional to attention",
                    "Attention weights are not importance; importance must be measured, e.g. by occlusion or Shapley values",
                    "Only the first attention head should be read"
                ],
                "correctExplanation": "Attention is a mixing pattern; the flatten head can use token states regardless of the weights (Jain and Wallace 2019).",
                "incorrectExplanation": "The disagreement is not about the sample or the head; occlusion and attention need not agree at all."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Transformer-ul acordă cea mai mare atenție segmentului de acum 14 zile, deci acel segment determină prognoza.” Pe modelul din capitol, ultima zi purta cea mai mare parte a importanței prin ocluzie. Care este eroarea?",
                "options": [
                    "Ponderile atenției au fost calculate pe setul de antrenare",
                    "Importanța prin ocluzie este întotdeauna proporțională cu atenția",
                    "Ponderile atenției nu sînt importanță; importanța trebuie măsurată, de exemplu prin ocluzie sau valori Shapley",
                    "Trebuie citit doar primul cap de atenție"
                ],
                "correctExplanation": "Atenția este un tipar de amestecare; capul care aplatizează poate folosi stările tokenilor indiferent de ponderi (Jain și Wallace 2019).",
                "incorrectExplanation": "Dezacordul nu ține de eșantion sau de cap; ocluzia și atenția nu trebuie să coincidă deloc."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: 'I trained the LSTM with 20 random seeds, kept the seed with the lowest test QLIKE, and its DM test against HAR rejects at 5%, so the LSTM is better.' What is the error?",
                "options": [
                    "The DM test cannot be used with QLIKE",
                    "Twenty seeds are too few to train an LSTM",
                    "HAR should have been trained with 20 seeds as well",
                    "Choosing the best of many seeds on the test set is data snooping: the DM test must account for the search (SPA, MCS) or use untouched data"
                ],
                "correctExplanation": "With K equally good models the best one rejects far more often than 5%; the search must be part of the test or the claim must be checked on new data.",
                "incorrectExplanation": "DM works with any loss differential, including QLIKE; the number of seeds is not the issue."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Am antrenat LSTM cu 20 de seed-uri, am păstrat seed-ul cu cel mai mic QLIKE de test, iar testul lui DM față de HAR respinge la 5%, deci LSTM este mai bun.” Care este eroarea?",
                "options": [
                    "Testul DM nu poate fi folosit cu QLIKE",
                    "Douăzeci de seed-uri sînt prea puține pentru antrenarea unui LSTM",
                    "Și HAR ar fi trebuit antrenat cu 20 de seed-uri",
                    "Alegerea celui mai bun dintre multe seed-uri pe setul de test este data snooping: testul trebuie să țină cont de căutare (SPA, MCS) sau să folosească date neatinse"
                ],
                "correctExplanation": "Cu K modele la fel de bune, cel mai bun respinge mult mai des decît în 5% din cazuri; căutarea trebuie inclusă în test sau afirmația verificată pe date noi.",
                "incorrectExplanation": "DM funcționează cu orice diferență de pierderi, inclusiv QLIKE; numărul de seed-uri nu este problema."
            }
        }
    ]
};
