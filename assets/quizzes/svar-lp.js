// ============================================================
// Chapter 3 quiz bank: Structural VAR and local projections (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['svar-lp'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Counting restrictions",
                "text": "A structural VAR has $n = 5$ variables and $u_t = B_0\\varepsilon_t$ with $\\mathbb{E}\\varepsilon_t\\varepsilon_t' = I$. How many restrictions on $B_0$ are needed, at a minimum, for exact identification?",
                "options": [
                    "10",
                    "5",
                    "15",
                    "25"
                ],
                "correctExplanation": "$\\Sigma_u = B_0B_0'$ gives $n(n + 1)/2 = 15$ distinct equations for $n^2 = 25$ unknowns, so $n(n - 1)/2 = 10$ restrictions are needed (order condition).",
                "incorrectExplanation": "Five would be one restriction per variable; 15 is the number of distinct moments in $\\Sigma_u$; 25 is the number of unknowns in $B_0$."
            },
            "ro": {
                "title": "Numărarea restricțiilor",
                "text": "Un VAR structural are $n = 5$ variabile și $u_t = B_0\\varepsilon_t$ cu $\\mathbb{E}\\varepsilon_t\\varepsilon_t' = I$. Cîte restricții asupra lui $B_0$ sînt necesare, cel puțin, pentru identificarea exactă?",
                "options": [
                    "10",
                    "5",
                    "15",
                    "25"
                ],
                "correctExplanation": "$\\Sigma_u = B_0B_0'$ dă $n(n + 1)/2 = 15$ ecuații distincte pentru $n^2 = 25$ de necunoscute, deci sînt necesare $n(n - 1)/2 = 10$ restricții (condiția de ordin).",
                "incorrectExplanation": "Cinci ar fi o restricție pe variabilă; 15 este numărul momentelor distincte din $\\Sigma_u$; 25 este numărul necunoscutelor din $B_0$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Observational equivalence",
                "text": "Let $P$ be the Cholesky factor of $\\Sigma_u$. Which matrix $\\tilde B_0$ is observationally equivalent to $B_0 = P$, for any orthogonal $Q$?",
                "options": [
                    "$P + Q$",
                    "$PQ$",
                    "$Q'PQ$ with $Q$ diagonal and positive",
                    "$P\\Sigma_u$"
                ],
                "correctExplanation": "$(PQ)(PQ)' = PQQ'P' = PP' = \\Sigma_u$: every rotation of $P$ reproduces the reduced-form covariance and fits the data equally well.",
                "incorrectExplanation": "A sum or a product with $\\Sigma_u$ does not reproduce $\\Sigma_u$ in general, and a positive diagonal $Q$ is not orthogonal unless it is the identity."
            },
            "ro": {
                "title": "Echivalența observațională",
                "text": "Fie $P$ factorul Cholesky al lui $\\Sigma_u$. Ce matrice $\\tilde B_0$ este echivalentă observațional cu $B_0 = P$, pentru orice $Q$ ortogonală?",
                "options": [
                    "$P + Q$",
                    "$PQ$",
                    "$Q'PQ$ cu $Q$ diagonală și pozitivă",
                    "$P\\Sigma_u$"
                ],
                "correctExplanation": "$(PQ)(PQ)' = PQQ'P' = PP' = \\Sigma_u$: orice rotație a lui $P$ reproduce covarianța formei reduse și descrie datele la fel de bine.",
                "incorrectExplanation": "O sumă sau un produs cu $\\Sigma_u$ nu reproduc în general $\\Sigma_u$, iar o matrice $Q$ diagonală pozitivă nu este ortogonală decît dacă este matricea unitate."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Cholesky by hand",
                "text": "With $\\Sigma_u = \\begin{pmatrix}4 & 1\\\\ 1 & 2\\end{pmatrix}$, what is the impact response of variable 2 to the first Cholesky shock?",
                "options": [
                    "1",
                    "0.25",
                    "0.5",
                    "1.32"
                ],
                "correctExplanation": "$p_{11} = \\sqrt 4 = 2$ and $p_{21} = \\sigma_{21}/p_{11} = 1/2 = 0.5$.",
                "incorrectExplanation": "1 is the covariance, not the Cholesky element; 0.25 is $p_{21}^2$; 1.32 is $p_{22} = \\sqrt{2 - 0.25}$, the response to the second shock."
            },
            "ro": {
                "title": "Cholesky de mînă",
                "text": "Cu $\\Sigma_u = \\begin{pmatrix}4 & 1\\\\ 1 & 2\\end{pmatrix}$, care este răspunsul la impact al variabilei 2 la primul șoc Cholesky?",
                "options": [
                    "1",
                    "0,25",
                    "0,5",
                    "1,32"
                ],
                "correctExplanation": "$p_{11} = \\sqrt 4 = 2$ și $p_{21} = \\sigma_{21}/p_{11} = 1/2 = 0{,}5$.",
                "incorrectExplanation": "1 este covarianța, nu elementul Cholesky; 0,25 este $p_{21}^2$; 1,32 este $p_{22} = \\sqrt{2 - 0{,}25}$, răspunsul la al doilea șoc."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The role of the ordering",
                "text": "In a recursive monetary VAR (slow block, policy rate, fast block), which change leaves the responses to the policy shock unchanged?",
                "options": [
                    "Moving the policy rate to the first position",
                    "Moving the policy rate to the last position",
                    "Moving a fast variable before the policy rate",
                    "Reordering the variables inside the slow block"
                ],
                "correctExplanation": "Christiano, Eichenbaum and Evans (1999): only the position of the policy variable relative to the blocks matters for its shock; orderings inside the blocks are irrelevant for it.",
                "incorrectExplanation": "Moving the policy rate, or moving a variable across it, changes which variables may react within the period and therefore the identified policy shock."
            },
            "ro": {
                "title": "Rolul ordonării",
                "text": "Într-un VAR monetar recursiv (bloc lent, dobînda de politică, bloc rapid), ce modificare lasă neschimbate răspunsurile la șocul de politică?",
                "options": [
                    "Mutarea dobînzii de politică pe primul loc",
                    "Mutarea dobînzii de politică pe ultimul loc",
                    "Mutarea unei variabile rapide înaintea dobînzii de politică",
                    "Reordonarea variabilelor în interiorul blocului lent"
                ],
                "correctExplanation": "Christiano, Eichenbaum și Evans (1999): pentru șocul de politică contează doar poziția variabilei de politică față de blocuri; ordonarea din interiorul blocurilor este irelevantă pentru el.",
                "incorrectExplanation": "Mutarea dobînzii de politică sau mutarea unei variabile peste ea schimbă variabilele care pot reacționa în aceeași perioadă, deci șocul de politică identificat."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The price puzzle",
                "text": "In the recursive CEE VAR of the lecture, prices rise slightly for a few months after a contractionary funds-rate shock. What is the standard explanation?",
                "options": [
                    "Monetary tightening raises inflation in the long run",
                    "The bootstrap bands are too narrow",
                    "The policy shock still contains the Fed's response to expected inflation that the VAR omits",
                    "The VAR has too many lags"
                ],
                "correctExplanation": "The Fed tightens when it expects inflation; if the VAR omits that information, part of the systematic response is mislabelled as a shock, and prices appear to rise after it.",
                "incorrectExplanation": "Long-run prices fall in the CEE responses; the puzzle concerns the point estimate, not the width of the bands; and it appears with few or many lags."
            },
            "ro": {
                "title": "Anomalia prețurilor",
                "text": "În VAR-ul recursiv CEE din curs, prețurile cresc ușor cîteva luni după un șoc contracționist al dobînzii federal funds. Care este explicația standard?",
                "options": [
                    "Înăsprirea monetară crește inflația pe termen lung",
                    "Benzile bootstrap sînt prea înguste",
                    "Șocul de politică conține încă reacția Fed la inflația așteptată, pe care VAR-ul o omite",
                    "VAR-ul are prea multe decalaje"
                ],
                "correctExplanation": "Fed înăsprește politica atunci cînd anticipează inflație; dacă VAR-ul omite această informație, o parte din reacția sistematică este etichetată greșit drept șoc, iar prețurile par să crească după el.",
                "incorrectExplanation": "Prețurile scad pe termen lung în răspunsurile CEE; anomalia privește estimația punctuală, nu lățimea benzilor; și apare și cu puține, și cu multe decalaje."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Kilian's oil shocks",
                "text": "In Kilian (2009), which assumption identifies the oil supply shock as the first shock of a recursive VAR?",
                "options": [
                    "Crude oil production does not respond within the month to demand shocks",
                    "The real price of oil does not respond within the month to any shock",
                    "Global real activity is not affected by oil supply shocks",
                    "Demand shocks have no long-run effect on oil production"
                ],
                "correctExplanation": "Ordering production first means it reacts within the month only to its own shock: adjustment costs make supply inelastic in the very short run.",
                "incorrectExplanation": "The price is ordered last precisely because it reacts to everything; real activity may respond to supply shocks within the month; the identification is short-run, not long-run."
            },
            "ro": {
                "title": "Șocurile petrolului la Kilian",
                "text": "În Kilian (2009), ce ipoteză identifică șocul de ofertă pe piața petrolului ca prim șoc al unui VAR recursiv?",
                "options": [
                    "Producția de țiței nu răspunde în aceeași lună la șocurile de cerere",
                    "Prețul real al petrolului nu răspunde în aceeași lună la niciun șoc",
                    "Activitatea reală globală nu este afectată de șocurile de ofertă",
                    "Șocurile de cerere nu au efect pe termen lung asupra producției de petrol"
                ],
                "correctExplanation": "Ordonarea producției pe primul loc înseamnă că ea reacționează în aceeași lună doar la propriul șoc: costurile de ajustare fac oferta inelastică pe termen foarte scurt.",
                "incorrectExplanation": "Prețul este pus pe ultimul loc tocmai pentru că reacționează la toate șocurile; activitatea reală poate răspunde în aceeași lună la șocurile de ofertă; identificarea este pe termen scurt, nu pe termen lung."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Blanchard and Quah",
                "text": "In Blanchard and Quah (1989), how is $B_0$ obtained from the reduced form?",
                "options": [
                    "$B_0 = \\mathrm{chol}(\\Sigma_u)$",
                    "$B_0 = A(1)^{-1}\\mathrm{chol}(\\Sigma_u)$",
                    "$B_0 = \\mathrm{chol}(A(1)\\Sigma_uA(1)')$",
                    "$B_0 = A(1)\\,\\mathrm{chol}(A(1)^{-1}\\Sigma_uA(1)^{-1\\prime})$"
                ],
                "correctExplanation": "The long-run matrix $\\Theta(1) = A(1)^{-1}B_0$ is made lower triangular: $\\Theta(1)$ is the Cholesky factor of $A(1)^{-1}\\Sigma_uA(1)^{-1\\prime}$, and $B_0 = A(1)\\Theta(1)$.",
                "incorrectExplanation": "The plain Cholesky factor imposes a short-run zero; the other two expressions do not make the long-run response of output to demand zero."
            },
            "ro": {
                "title": "Blanchard și Quah",
                "text": "În Blanchard și Quah (1989), cum se obține $B_0$ din forma redusă?",
                "options": [
                    "$B_0 = \\mathrm{chol}(\\Sigma_u)$",
                    "$B_0 = A(1)^{-1}\\mathrm{chol}(\\Sigma_u)$",
                    "$B_0 = \\mathrm{chol}(A(1)\\Sigma_uA(1)')$",
                    "$B_0 = A(1)\\,\\mathrm{chol}(A(1)^{-1}\\Sigma_uA(1)^{-1\\prime})$"
                ],
                "correctExplanation": "Matricea de termen lung $\\Theta(1) = A(1)^{-1}B_0$ este făcută inferior triunghiulară: $\\Theta(1)$ este factorul Cholesky al lui $A(1)^{-1}\\Sigma_uA(1)^{-1\\prime}$, iar $B_0 = A(1)\\Theta(1)$.",
                "incorrectExplanation": "Factorul Cholesky simplu impune un zero pe termen scurt; celelalte două expresii nu anulează răspunsul pe termen lung al producției la cerere."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Fragility of long-run restrictions",
                "text": "In the seminar, removing the 1973:4 break in mean growth and the trend in unemployment changes the share of demand shocks in the one-year output variance from about 92% to about 22%. What does this illustrate?",
                "options": [
                    "Demand shocks became unimportant after 1973",
                    "Long-run restrictions depend heavily on how low frequencies are treated (Faust and Leeper 1997)",
                    "The VAR(8) is not stable",
                    "Long-run restrictions are immune to data treatment"
                ],
                "correctExplanation": "The long-run multiplier $A(1)^{-1}$ is estimated from the lowest frequencies, exactly those changed by breaks and trends; the identified shocks change with them.",
                "incorrectExplanation": "The comparison uses the same sample, so it says nothing about a change after 1973; stability is not the issue; and the result shows the opposite of immunity."
            },
            "ro": {
                "title": "Fragilitatea restricțiilor de termen lung",
                "text": "În seminar, eliminarea rupturii din 1973:4 în creșterea medie și a trendului din șomaj schimbă ponderea șocurilor de cerere în varianța producției la un an de la aproximativ 92% la aproximativ 22%. Ce ilustrează acest rezultat?",
                "options": [
                    "Șocurile de cerere au devenit neimportante după 1973",
                    "Restricțiile de termen lung depind mult de tratarea frecvențelor joase (Faust și Leeper 1997)",
                    "VAR(8) nu este stabil",
                    "Restricțiile de termen lung nu sînt afectate de tratarea datelor"
                ],
                "correctExplanation": "Multiplicatorul de termen lung $A(1)^{-1}$ se estimează din frecvențele cele mai joase, exact cele modificate de rupturi și trenduri; șocurile identificate se schimbă odată cu ele.",
                "incorrectExplanation": "Comparația folosește același eșantion, deci nu spune nimic despre o schimbare după 1973; stabilitatea nu este problema; iar rezultatul arată opusul imunității."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Sign restrictions",
                "text": "What do sign restrictions on the responses of prices, reserves and the policy rate deliver for the response of output?",
                "options": [
                    "A unique point estimate, as with Cholesky",
                    "A set of responses consistent with the data and the restrictions",
                    "A response that is negative by construction",
                    "The same answer as the long-run restriction"
                ],
                "correctExplanation": "Sign restrictions only rule out rotations; many rotations remain, so the output response is set-identified (Uhlig 2005).",
                "incorrectExplanation": "A point estimate needs equality restrictions; output is left unrestricted, so it is not negative by construction; and different restrictions identify different shocks."
            },
            "ro": {
                "title": "Restricții de semn",
                "text": "Ce furnizează restricțiile de semn asupra răspunsurilor prețurilor, rezervelor și dobînzii de politică pentru răspunsul producției?",
                "options": [
                    "O estimație punctuală unică, ca la Cholesky",
                    "O mulțime de răspunsuri compatibile cu datele și cu restricțiile",
                    "Un răspuns negativ prin construcție",
                    "Același răspuns ca restricția de termen lung"
                ],
                "correctExplanation": "Restricțiile de semn doar exclud rotații; rămîn multe rotații, deci răspunsul producției este identificat pe mulțimi (Uhlig 2005).",
                "incorrectExplanation": "O estimație punctuală cere restricții de egalitate; producția este lăsată nerestricționată, deci nu este negativă prin construcție; iar restricții diferite identifică șocuri diferite."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The Haar prior",
                "text": "Why do Baumeister and Hamilton (2015) criticise drawing the rotation $Q$ uniformly (Haar) in sign-restricted VARs?",
                "options": [
                    "Because Haar draws are too slow to compute",
                    "Because the Haar distribution is not defined for $n > 2$",
                    "Because it violates the sign restrictions",
                    "Because the uniform prior on $Q$ is informative about the impulse responses inside the identified set"
                ],
                "correctExplanation": "Inside the set the data are silent; a uniform distribution of $Q$ implies a non-uniform, informative distribution of the responses, which then drives the posterior.",
                "incorrectExplanation": "Haar draws are cheap (QR of a Gaussian matrix), exist in any dimension, and the draws that violate the signs are simply rejected."
            },
            "ro": {
                "title": "Distribuția a priori Haar",
                "text": "De ce critică Baumeister și Hamilton (2015) extragerea uniformă (Haar) a rotației $Q$ în VAR-urile cu restricții de semn?",
                "options": [
                    "Pentru că extragerile Haar se calculează prea lent",
                    "Pentru că distribuția Haar nu este definită pentru $n > 2$",
                    "Pentru că încalcă restricțiile de semn",
                    "Pentru că distribuția a priori uniformă pe $Q$ este informativă pentru răspunsurile din interiorul mulțimii identificate"
                ],
                "correctExplanation": "În interiorul mulțimii datele nu spun nimic; o distribuție uniformă a lui $Q$ implică o distribuție neuniformă și informativă a răspunsurilor, care determină apoi distribuția a posteriori.",
                "incorrectExplanation": "Extragerile Haar sînt ieftine (QR al unei matrice gaussiene), există în orice dimensiune, iar extragerile care încalcă semnele sînt pur și simplu respinse."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The posterior median",
                "text": "Fry and Pagan (2011) warn against reporting the pointwise posterior median of sign-restricted responses. Why?",
                "options": [
                    "At different horizons and variables the median may come from different rotations, so it need not be any admissible structural model",
                    "Because the median is always zero",
                    "Because the mean is always inside the identified set and the median is not",
                    "Because the median ignores the sign restrictions"
                ],
                "correctExplanation": "The pointwise median combines responses of different models; it can violate the orthogonality of the shocks implied by any single $Q$.",
                "incorrectExplanation": "The median is not zero in general; neither the mean nor the median is guaranteed to correspond to one model; and both are computed from draws that satisfy the signs."
            },
            "ro": {
                "title": "Mediana a posteriori",
                "text": "Fry și Pagan (2011) avertizează împotriva raportării medianei a posteriori punctuale a răspunsurilor identificate prin semne. De ce?",
                "options": [
                    "La orizonturi și variabile diferite mediana poate proveni din rotații diferite, deci nu este neapărat un model structural admisibil",
                    "Pentru că mediana este întotdeauna zero",
                    "Pentru că media se află întotdeauna în mulțimea identificată, iar mediana nu",
                    "Pentru că mediana ignoră restricțiile de semn"
                ],
                "correctExplanation": "Mediana punctuală combină răspunsuri ale unor modele diferite; ea poate încălca ortogonalitatea șocurilor implicată de o singură matrice $Q$.",
                "incorrectExplanation": "Mediana nu este zero în general; nici media, nici mediana nu corespund garantat unui singur model; și ambele se calculează din extrageri care respectă semnele."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Identification through heteroskedasticity",
                "text": "Two regimes have $\\Sigma_1 = B_0B_0'$ and $\\Sigma_2 = B_0\\Lambda B_0'$ with $\\Lambda$ diagonal. When is $B_0$ identified (up to column signs and ordering)?",
                "options": [
                    "Always, whatever $\\Lambda$",
                    "Only when $\\Lambda = I$",
                    "When the diagonal elements of $\\Lambda$ are distinct",
                    "Only if the shocks are Normal"
                ],
                "correctExplanation": "$\\Sigma_1^{-1}\\Sigma_2 = B_0^{-1\\prime}\\Lambda B_0'$; distinct eigenvalues give unique eigenvectors (Rigobon 2003).",
                "incorrectExplanation": "With equal variance ratios any rotation within the eigenspace is admissible; $\\Lambda = I$ means no change of regime and no identification; Normality is not needed."
            },
            "ro": {
                "title": "Identificarea prin heteroscedasticitate",
                "text": "Două regimuri au $\\Sigma_1 = B_0B_0'$ și $\\Sigma_2 = B_0\\Lambda B_0'$, cu $\\Lambda$ diagonală. Cînd este identificat $B_0$ (pînă la semnul și ordinea coloanelor)?",
                "options": [
                    "Întotdeauna, oricare ar fi $\\Lambda$",
                    "Doar cînd $\\Lambda = I$",
                    "Cînd elementele diagonale ale lui $\\Lambda$ sînt distincte",
                    "Doar dacă șocurile urmează distribuția Normală"
                ],
                "correctExplanation": "$\\Sigma_1^{-1}\\Sigma_2 = B_0^{-1\\prime}\\Lambda B_0'$; valorile proprii distincte dau vectori proprii unici (Rigobon 2003).",
                "incorrectExplanation": "Cu rapoarte egale ale varianțelor, orice rotație în subspațiul propriu este admisibilă; $\\Lambda = I$ înseamnă lipsa schimbării de regim și lipsa identificării; distribuția Normală nu este necesară."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Proxy SVAR",
                "text": "An external instrument $z_t$ is relevant for shock 1 and exogenous to all other shocks. What does $\\mathbb{E} u_tz_t$ identify?",
                "options": [
                    "The whole matrix $B_0$",
                    "The reduced-form coefficients $A_1, \\dots, A_p$",
                    "The variance of shock 1",
                    "The impact column $b_1$ up to scale"
                ],
                "correctExplanation": "$\\mathbb{E} u_tz_t = B_0\\mathbb{E}\\varepsilon_tz_t = \\alpha b_1$; the relative impacts $b_{i1}/b_{11}$ follow, and a normalisation fixes the scale.",
                "incorrectExplanation": "Only one column is identified; the reduced form is estimated by OLS without the instrument; the variance is fixed by the normalisation, not identified separately."
            },
            "ro": {
                "title": "Proxy SVAR",
                "text": "Un instrument extern $z_t$ este relevant pentru șocul 1 și exogen față de toate celelalte șocuri. Ce identifică $\\mathbb{E} u_tz_t$?",
                "options": [
                    "Întreaga matrice $B_0$",
                    "Coeficienții formei reduse $A_1, \\dots, A_p$",
                    "Varianța șocului 1",
                    "Coloana de impact $b_1$, pînă la o constantă"
                ],
                "correctExplanation": "$\\mathbb{E} u_tz_t = B_0\\mathbb{E}\\varepsilon_tz_t = \\alpha b_1$; rezultă impacturile relative $b_{i1}/b_{11}$, iar o normalizare fixează scala.",
                "incorrectExplanation": "Se identifică doar o coloană; forma redusă se estimează prin OLS fără instrument; varianța este fixată de normalizare, nu identificată separat."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Weak instruments",
                "text": "In the lecture, the Jarociński--Karadi ECB shock has a first-stage $F$ of about 5 for the monthly euro-area 1-year rate. Which inference should be reported for the spillover to Romanian HICP?",
                "options": [
                    "A Wald interval $\\hat\\beta \\pm 1.96\\,\\mathrm{se}$",
                    "No interval, since $F > 1$",
                    "An Anderson--Rubin confidence set, which stays valid with weak instruments and may be wide or unbounded",
                    "A one-sided $t$ test on $\\hat\\beta$"
                ],
                "correctExplanation": "With $F$ well below 10 the 2SLS estimator is biased and Wald intervals undercover; Anderson--Rubin sets have correct coverage for any strength (Montiel Olea, Stock and Watson 2021).",
                "incorrectExplanation": "Wald and $t$ tests rely on a strong first stage; $F > 1$ is no guarantee of relevance."
            },
            "ro": {
                "title": "Instrumente slabe",
                "text": "În curs, șocul BCE Jarociński--Karadi are o statistică $F$ din prima etapă de aproximativ 5 pentru dobînda lunară la 1 an din zona euro. Ce inferență trebuie raportată pentru efectul asupra IAPC din România?",
                "options": [
                    "Un interval Wald $\\hat\\beta \\pm 1{,}96\\,\\mathrm{se}$",
                    "Niciun interval, deoarece $F > 1$",
                    "O mulțime de încredere Anderson--Rubin, valabilă cu instrumente slabe, posibil largă sau nemărginită",
                    "Un test $t$ unilateral pe $\\hat\\beta$"
                ],
                "correctExplanation": "Cu $F$ mult sub 10, estimatorul 2SLS este deplasat, iar intervalele Wald au acoperire prea mică; mulțimile Anderson--Rubin au acoperirea corectă pentru orice tărie (Montiel Olea, Stock și Watson 2021).",
                "incorrectExplanation": "Testele Wald și $t$ se bazează pe o primă etapă puternică; $F > 1$ nu garantează relevanța."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "High-frequency surprises",
                "text": "Why are FOMC surprises measured in a narrow window (about 30 minutes) around the announcement?",
                "options": [
                    "Because futures trade only for 30 minutes after an FOMC meeting",
                    "So that no other systematic news moves rates in the window, which makes the surprise exogenous",
                    "To make the surprises larger",
                    "Because monthly data are not available"
                ],
                "correctExplanation": "Within a narrow window the announcement is the only systematic event, so other shocks are (nearly) uncorrelated with the surprise (Kuttner 2001; Gürkaynak, Sack and Swanson 2005).",
                "incorrectExplanation": "Futures trade continuously; a narrow window makes surprises smaller, not larger; and the surprises are later aggregated to monthly frequency anyway."
            },
            "ro": {
                "title": "Surprize de frecvență înaltă",
                "text": "De ce se măsoară surprizele FOMC într-o fereastră îngustă (aproximativ 30 de minute) în jurul anunțului?",
                "options": [
                    "Pentru că futures se tranzacționează doar 30 de minute după ședința FOMC",
                    "Pentru ca nicio altă știre sistematică să nu miște dobînzile în fereastră, ceea ce face surpriza exogenă",
                    "Pentru a face surprizele mai mari",
                    "Pentru că datele lunare nu sînt disponibile"
                ],
                "correctExplanation": "Într-o fereastră îngustă anunțul este singurul eveniment sistematic, deci celelalte șocuri sînt (aproape) necorelate cu surpriza (Kuttner 2001; Gürkaynak, Sack și Swanson 2005).",
                "incorrectExplanation": "Futures se tranzacționează continuu; o fereastră îngustă face surprizele mai mici, nu mai mari; iar surprizele se agregă oricum ulterior la frecvență lunară."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The information effect",
                "text": "Nakamura and Steinsson (2018) argue that a policy surprise can partly be an information shock. What is the implication for identification?",
                "options": [
                    "The surprise may violate exogeneity, because it also reveals the central bank's view of the economy",
                    "The surprise becomes a weak instrument by construction",
                    "The VAR must be estimated in first differences",
                    "Local projections cannot be used"
                ],
                "correctExplanation": "A tightening can signal good news about demand; then $z_t$ is correlated with a demand shock and $\\mathbb{E} z_t\\varepsilon_{jt} \\ne 0$; Jarociński and Karadi (2020) separate the two with stock-price co-movement.",
                "incorrectExplanation": "Relevance can be strong even with an information component; differencing and the choice between LP and VAR do not address exogeneity."
            },
            "ro": {
                "title": "Efectul informațional",
                "text": "Nakamura și Steinsson (2018) arată că o surpriză de politică poate fi parțial un șoc informațional. Ce implică acest lucru pentru identificare?",
                "options": [
                    "Surpriza poate încălca exogenitatea, pentru că dezvăluie și evaluarea băncii centrale despre economie",
                    "Surpriza devine prin construcție un instrument slab",
                    "VAR-ul trebuie estimat în diferențe",
                    "Proiecțiile locale nu se mai pot folosi"
                ],
                "correctExplanation": "O înăsprire poate semnala vești bune despre cerere; atunci $z_t$ este corelat cu un șoc de cerere și $\\mathbb{E} z_t\\varepsilon_{jt} \\ne 0$; Jarociński și Karadi (2020) separă cele două prin co-mișcarea cu prețurile acțiunilor.",
                "incorrectExplanation": "Relevanța poate fi puternică și cu o componentă informațională; diferențierea și alegerea între LP și VAR nu rezolvă exogenitatea."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Bootstrap for proxy SVARs",
                "text": "Which bootstrap gives valid bands for a proxy SVAR, according to Jentsch and Lunsford (2019)?",
                "options": [
                    "The moving-block bootstrap of residuals and instrument jointly",
                    "The wild bootstrap with Rademacher weights",
                    "The i.i.d. residual bootstrap without the instrument",
                    "The delta method only"
                ],
                "correctExplanation": "The wild bootstrap fails to reproduce the dependence between squared shocks and the instrument; the moving-block bootstrap keeps it.",
                "incorrectExplanation": "The wild bootstrap of Mertens and Ravn is invalid here; ignoring the instrument loses the identification uncertainty; the delta method is not a bootstrap."
            },
            "ro": {
                "title": "Bootstrap pentru proxy SVAR",
                "text": "Ce bootstrap dă benzi valide pentru un proxy SVAR, conform lui Jentsch și Lunsford (2019)?",
                "options": [
                    "Bootstrap-ul pe blocuri mobile al reziduurilor și al instrumentului împreună",
                    "Bootstrap-ul wild cu ponderi Rademacher",
                    "Bootstrap-ul i.i.d. pe reziduuri, fără instrument",
                    "Doar metoda delta"
                ],
                "correctExplanation": "Bootstrap-ul wild nu reproduce dependența dintre pătratele șocurilor și instrument; bootstrap-ul pe blocuri mobile o păstrează.",
                "incorrectExplanation": "Bootstrap-ul wild al lui Mertens și Ravn nu este valid aici; ignorarea instrumentului pierde incertitudinea identificării; metoda delta nu este un bootstrap."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Kilian's bias correction",
                "text": "What does the bootstrap-after-bootstrap of Kilian (1998) do when the bias-corrected VAR would be explosive?",
                "options": [
                    "It doubles the correction",
                    "It switches to the delta method",
                    "It shrinks the bias correction until the corrected VAR is stationary, or leaves the estimate uncorrected",
                    "It drops the most persistent variable"
                ],
                "correctExplanation": "The correction $\\hat A - \\delta\\hat b$ is applied with $\\delta$ reduced from 1 towards 0 until all roots are inside the unit circle; with a root above one already, no correction is applied.",
                "incorrectExplanation": "Doubling would make it more explosive; the procedure stays a bootstrap and never changes the variables of the model."
            },
            "ro": {
                "title": "Corecția deplasării Kilian",
                "text": "Ce face bootstrap-ul după bootstrap al lui Kilian (1998) cînd VAR-ul cu deplasarea corectată ar fi exploziv?",
                "options": [
                    "Dublează corecția",
                    "Trece la metoda delta",
                    "Micșorează corecția pînă cînd VAR-ul corectat este staționar sau lasă estimația necorectată",
                    "Elimină variabila cea mai persistentă"
                ],
                "correctExplanation": "Corecția $\\hat A - \\delta\\hat b$ se aplică cu $\\delta$ redus de la 1 spre 0 pînă cînd toate rădăcinile sînt în interiorul cercului unitate; dacă există deja o rădăcină peste unu, nu se aplică nicio corecție.",
                "incorrectExplanation": "Dublarea ar face modelul și mai exploziv; procedura rămîne un bootstrap și nu schimbă niciodată variabilele modelului."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Joint bands",
                "text": "A researcher wants to claim that “output falls for the whole first two years” after a shock. Which bands are appropriate?",
                "options": [
                    "Pointwise 68% bands",
                    "Pointwise 95% bands at the 24-month horizon only",
                    "Bands from the delta method at horizon 0",
                    "Simultaneous (joint) bands over the horizons, such as sup-$t$ bands"
                ],
                "correctExplanation": "A statement about a whole path needs coverage of the whole path; pointwise bands cover each horizon separately (Montiel Olea and Plagborg-Møller 2019).",
                "incorrectExplanation": "Pointwise bands at one or many horizons do not control the probability that the whole path lies inside them."
            },
            "ro": {
                "title": "Benzi simultane",
                "text": "Un cercetător vrea să afirme că „producția scade pe tot parcursul primilor doi ani” după un șoc. Ce benzi sînt potrivite?",
                "options": [
                    "Benzi punctuale de 68%",
                    "Benzi punctuale de 95% doar la orizontul de 24 de luni",
                    "Benzi prin metoda delta la orizontul 0",
                    "Benzi simultane pe orizonturi, de exemplu benzi sup-$t$"
                ],
                "correctExplanation": "O afirmație despre o traiectorie întreagă cere acoperirea traiectoriei întregi; benzile punctuale acoperă fiecare orizont separat (Montiel Olea și Plagborg-Møller 2019).",
                "incorrectExplanation": "Benzile punctuale, la un orizont sau la mai multe, nu controlează probabilitatea ca întreaga traiectorie să se afle în interiorul lor."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "LP and VAR in population",
                "text": "What do Plagborg-Møller and Wolf (2021) show about local projections and VARs?",
                "options": [
                    "LP is always unbiased and VAR always biased",
                    "With the same lags as controls, they estimate the same responses in population up to horizon $p$, and at all horizons with unrestricted lags",
                    "They identify different shocks",
                    "LP needs invertibility and VAR does not"
                ],
                "correctExplanation": "Both are linear projections on the same information; differences arise only in finite samples, as a bias--variance trade-off.",
                "incorrectExplanation": "Both can be biased in finite samples; with the same identifying restriction they target the same shock; it is the VAR that needs invertibility for some schemes, not LP."
            },
            "ro": {
                "title": "LP și VAR în populație",
                "text": "Ce arată Plagborg-Møller și Wolf (2021) despre proiecțiile locale și VAR-uri?",
                "options": [
                    "LP este întotdeauna nedeplasată, iar VAR întotdeauna deplasat",
                    "Cu aceleași decalaje drept controale, estimează în populație aceleași răspunsuri pînă la orizontul $p$, iar cu decalaje nerestricționate, la toate orizonturile",
                    "Identifică șocuri diferite",
                    "LP are nevoie de inversabilitate, iar VAR nu"
                ],
                "correctExplanation": "Ambele sînt proiecții liniare pe aceeași informație; diferențele apar doar în eșantioane finite, ca un compromis între deplasare și varianță.",
                "incorrectExplanation": "Ambele pot fi deplasate în eșantioane finite; cu aceeași restricție de identificare țintesc același șoc; VAR-ul are nevoie de inversabilitate pentru unele scheme, nu LP."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Bias and variance",
                "text": "In the simulation of the lecture, at horizon 16 a misspecified VAR(2) has a lower RMSE than LP(2). Why?",
                "options": [
                    "The VAR(2) is correctly specified",
                    "LP is biased at every horizon by construction",
                    "Its small bias at that horizon is outweighed by a much lower variance",
                    "The VAR uses more observations than LP at every horizon"
                ],
                "correctExplanation": "Li, Plagborg-Møller and Wolf (2024): LP has low bias and high variance; where the VAR's bias is small, its lower variance wins in mean squared error.",
                "incorrectExplanation": "The DGP has a hump-shaped moving-average term that a VAR(2) cannot capture; LP is nearly unbiased; the sample-size difference is too small to explain the gap."
            },
            "ro": {
                "title": "Deplasare și varianță",
                "text": "În simularea din curs, la orizontul 16 un VAR(2) greșit specificat are un RMSE mai mic decît LP(2). De ce?",
                "options": [
                    "VAR(2) este corect specificat",
                    "LP este deplasată prin construcție la orice orizont",
                    "Deplasarea lui mică la acel orizont este compensată de o varianță mult mai mică",
                    "VAR-ul folosește mai multe observații decît LP la orice orizont"
                ],
                "correctExplanation": "Li, Plagborg-Møller și Wolf (2024): LP are deplasare mică și varianță mare; acolo unde deplasarea VAR-ului este mică, varianța lui mai mică cîștigă în eroarea medie pătratică.",
                "incorrectExplanation": "DGP-ul are un termen de medie mobilă în formă de cocoașă pe care un VAR(2) nu îl poate surprinde; LP este aproape nedeplasată; diferența de dimensiune a eșantionului este prea mică pentru a explica decalajul."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Inference for local projections",
                "text": "What does lag augmentation (Montiel Olea and Plagborg-Møller 2021) allow in local projections?",
                "options": [
                    "Dropping all controls",
                    "Using Eicker--Huber--White standard errors, valid even for highly persistent data, after adding one more lag of the controls",
                    "Using the i.i.d. variance without any extra lag",
                    "Estimating all horizons in one regression"
                ],
                "correctExplanation": "With one extra lag the regression score becomes serially uncorrelated, so heteroskedasticity-robust errors suffice, uniformly over persistence.",
                "incorrectExplanation": "Controls are still needed; the i.i.d. variance ignores heteroskedasticity; LP remains one regression per horizon."
            },
            "ro": {
                "title": "Inferența pentru proiecțiile locale",
                "text": "Ce permit decalajele suplimentare (Montiel Olea și Plagborg-Møller 2021) în proiecțiile locale?",
                "options": [
                    "Renunțarea la toate controalele",
                    "Folosirea erorilor standard Eicker--Huber--White, valabile și pentru date foarte persistente, după adăugarea unui decalaj suplimentar al controalelor",
                    "Folosirea varianței i.i.d. fără vreun decalaj suplimentar",
                    "Estimarea tuturor orizonturilor într-o singură regresie"
                ],
                "correctExplanation": "Cu un decalaj suplimentar, scorul regresiei devine necorelat serial, deci erorile robuste la heteroscedasticitate sînt suficiente, uniform după persistență.",
                "incorrectExplanation": "Controalele rămîn necesare; varianța i.i.d. ignoră heteroscedasticitatea; LP rămîne o regresie pentru fiecare orizont."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: “Ramey and Zubairy (2018) show that government spending multipliers are well above one in slack times and below one otherwise.” What is wrong?",
                "options": [
                    "Their state-dependent estimates are below one in both states, with no significant difference",
                    "They study monetary, not fiscal, policy",
                    "They use a VAR, not local projections",
                    "Their sample covers only 2008--2015"
                ],
                "correctExplanation": "With military news shocks and LP-IV on 1889--2015 they find multipliers between about 0.6 and 0.7 in both states (the lecture: 0.62 and 0.68 in slack, 0.59 and 0.66 otherwise).",
                "incorrectExplanation": "The paper is about fiscal multipliers, it uses state-dependent local projections, and its sample starts in 1889."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Ramey și Zubairy (2018) arată că multiplicatorii cheltuielilor publice sînt mult peste unu în perioadele de subutilizare și sub unu în rest.” Ce este greșit?",
                "options": [
                    "Estimațiile lor dependente de stare sînt sub unu în ambele stări, fără o diferență semnificativă",
                    "Ei studiază politica monetară, nu cea fiscală",
                    "Folosesc un VAR, nu proiecții locale",
                    "Eșantionul lor acoperă doar 2008--2015"
                ],
                "correctExplanation": "Cu șocuri de știri militare și LP-IV pe 1889--2015, găsesc multiplicatori între aproximativ 0,6 și 0,7 în ambele stări (în curs: 0,62 și 0,68 la subutilizare, 0,59 și 0,66 în rest).",
                "incorrectExplanation": "Lucrarea privește multiplicatorii fiscali, folosește proiecții locale dependente de stare, iar eșantionul începe în 1889."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant summarises the Romanian VAR of the lecture: “A ROBOR tightening raises prices and depreciates the leu, so in Romania monetary tightening is inflationary.” What is wrong?",
                "options": [
                    "ROBOR is not related to BNR policy",
                    "The VAR has no euro-area variables",
                    "Romanian prices are not measured monthly",
                    "The price and exchange-rate puzzles signal a failed recursive identification, not a causal effect"
                ],
                "correctExplanation": "The ROBOR innovation still contains the BNR's systematic reaction to expected inflation and to pressure on the leu; the puzzle survives every ordering, which points to missing information, not to a true effect.",
                "incorrectExplanation": "ROBOR transmits the policy rate; the VAR includes a euro-area block; and HICP is monthly."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI rezumă VAR-ul pentru România din curs: „O înăsprire ROBOR crește prețurile și depreciază leul, deci în România înăsprirea monetară este inflaționistă.” Ce este greșit?",
                "options": [
                    "ROBOR nu are legătură cu politica BNR",
                    "VAR-ul nu conține variabile din zona euro",
                    "Prețurile din România nu se măsoară lunar",
                    "Anomaliile prețurilor și ale cursului semnalează eșecul identificării recursive, nu un efect cauzal"
                ],
                "correctExplanation": "Inovația ROBOR conține încă reacția sistematică a BNR la inflația așteptată și la presiunea asupra leului; anomalia rezistă la orice ordonare, ceea ce indică informație lipsă, nu un efect real.",
                "incorrectExplanation": "ROBOR transmite dobînda de politică; VAR-ul include un bloc al zonei euro; iar IAPC este lunar."
            }
        }
    ]
};
