// ============================================================
// Chapter 2 quiz bank: Structural breaks and nonlinear models (EN + RO)
// 24 questions, 20 drawn per attempt.
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.ATS_DATA.quizzes['breaks-nonlinear'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "The sup-Wald critical value",
                "text": "With one coefficient tested and 15% trimming, the 5% critical value of the sup-Wald test is about 8.6, not 3.84. Why?",
                "options": [
                    "Because the statistic is maximised over all candidate break dates, so its null distribution is that of a supremum of a stochastic process",
                    "Because the errors are assumed to be heteroskedastic",
                    "Because the test has two degrees of freedom when the date is unknown",
                    "Because the sample is split into two halves of equal size"
                ],
                "correctExplanation": "Under the null the break date is not identified; maximising the Wald statistic over dates gives the supremum of a squared standardised Brownian bridge (Andrews 1993), whose 95% quantile is far above that of chi2(1).",
                "incorrectExplanation": "Heteroskedasticity changes the variance estimator, not the shape of the limit; the number of restrictions is still one; the sample is split at every candidate date, not only in halves."
            },
            "ro": {
                "title": "Valoarea critică sup-Wald",
                "text": "Cu un coeficient testat și trunchiere de 15%, valoarea critică de 5% a testului sup-Wald este aproximativ 8,6, nu 3,84. De ce?",
                "options": [
                    "Pentru că statistica este maximizată după toate datele candidate ale rupturii, deci distribuția ei sub ipoteza nulă este cea a supremumului unui proces stochastic",
                    "Pentru că erorile sînt presupuse heteroscedastice",
                    "Pentru că testul are două grade de libertate cînd data este necunoscută",
                    "Pentru că eșantionul este împărțit în două jumătăți egale"
                ],
                "correctExplanation": "Sub ipoteza nulă data rupturii nu este identificată; maximizarea statisticii Wald după date dă supremumul unei punți browniene standardizate la pătrat (Andrews 1993), a cărei cuantilă de 95% este mult peste cea a lui chi2(1).",
                "incorrectExplanation": "Heteroscedasticitatea schimbă estimatorul varianței, nu forma limitei; numărul restricțiilor rămîne unu; eșantionul este împărțit la fiecare dată candidată, nu doar în jumătăți."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Trimming",
                "text": "Why does the sup-Wald test search only over break fractions in [0.15, 0.85]?",
                "options": [
                    "To make the test robust to serial correlation",
                    "Because without trimming the supremum of the limiting process is infinite almost surely",
                    "Because breaks near the ends of the sample cannot happen",
                    "To reduce the computing time of the test"
                ],
                "correctExplanation": "Near the ends one regime rests on very few observations; the standardised Brownian bridge has an infinite supremum over (0, 1), so a compact range is needed for a nondegenerate limit.",
                "incorrectExplanation": "Serial correlation is handled by HAC variances; breaks near the ends can happen but are not detectable with this statistic; computing time is not the reason."
            },
            "ro": {
                "title": "Trunchierea",
                "text": "De ce caută testul sup-Wald doar fracții ale rupturii în intervalul [0,15; 0,85]?",
                "options": [
                    "Pentru a face testul robust la autocorelație",
                    "Pentru că fără trunchiere supremumul procesului-limită este infinit aproape sigur",
                    "Pentru că rupturile de lîngă capetele eșantionului nu se pot produce",
                    "Pentru a reduce timpul de calcul al testului"
                ],
                "correctExplanation": "Lîngă capete un regim se sprijină pe foarte puține observații; puntea browniană standardizată are supremum infinit pe (0, 1), deci este nevoie de un interval compact pentru o limită nedegenerată.",
                "incorrectExplanation": "Autocorelația se tratează prin varianțe HAC; rupturile de lîngă capete se pot produce, dar nu pot fi detectate cu această statistică; timpul de calcul nu este motivul."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Precision of the break date",
                "text": "For a break of fixed size, how precisely does least squares estimate the break date T1 as the sample grows?",
                "options": [
                    "The error in the date grows like the square root of T",
                    "The error in the break fraction shrinks like 1/sqrt(T), as for the regression coefficients",
                    "The error in the date stays bounded in probability, so the break fraction is estimated at rate T",
                    "The date cannot be estimated consistently"
                ],
                "correctExplanation": "Bai (1997): the estimated date is within O_p(1) observations of the truth, so the fraction converges at rate T, faster than the sqrt(T) rate of the coefficients.",
                "incorrectExplanation": "The date error does not grow; the sqrt(T) rate belongs to the regression coefficients, not to the break fraction; the estimator is consistent."
            },
            "ro": {
                "title": "Precizia datei rupturii",
                "text": "Pentru o ruptură de mărime fixă, cît de precis estimează cele mai mici pătrate data rupturii T1 cînd eșantionul crește?",
                "options": [
                    "Eroarea datei crește ca rădăcina pătrată a lui T",
                    "Eroarea fracției rupturii scade ca 1/sqrt(T), ca pentru coeficienții regresiei",
                    "Eroarea datei rămîne mărginită în probabilitate, deci fracția rupturii se estimează cu rata T",
                    "Data nu poate fi estimată consistent"
                ],
                "correctExplanation": "Bai (1997): data estimată se află la O_p(1) observații de cea adevărată, deci fracția converge cu rata T, mai repede decît rata sqrt(T) a coeficienților.",
                "incorrectExplanation": "Eroarea datei nu crește; rata sqrt(T) aparține coeficienților regresiei, nu fracției rupturii; estimatorul este consistent."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Andrews and Ploberger",
                "text": "Against which alternatives is the ave-Wald statistic (the average of W_T over the break dates) optimal?",
                "options": [
                    "Against one very large break at the middle of the sample",
                    "Against breaks in the variance only",
                    "Against a break known to occur at the first trimmed date",
                    "Against very small breaks, close to the null hypothesis"
                ],
                "correctExplanation": "Andrews and Ploberger (1994): the exp-Wald statistic maximises a weighted average power; its limit for alternatives local to the null is the ave-Wald, close to the Nyblom test of random-walk coefficients.",
                "incorrectExplanation": "Large breaks are well detected by sup- and exp-Wald; the statistic concerns coefficients, not only variances; a known date needs no averaging."
            },
            "ro": {
                "title": "Andrews și Ploberger",
                "text": "Împotriva căror alternative este optimă statistica ave-Wald (media lui W_T peste datele rupturii)?",
                "options": [
                    "Împotriva unei rupturi foarte mari la mijlocul eșantionului",
                    "Împotriva rupturilor doar în varianță",
                    "Împotriva unei rupturi despre care se știe că apare la prima dată din intervalul trunchiat",
                    "Împotriva rupturilor foarte mici, apropiate de ipoteza nulă"
                ],
                "correctExplanation": "Andrews și Ploberger (1994): statistica exp-Wald maximizează o putere medie ponderată; limita ei pentru alternative apropiate de ipoteza nulă este ave-Wald, apropiat de testul Nyblom pentru coeficienți de tip mers aleator.",
                "incorrectExplanation": "Rupturile mari sînt detectate bine de sup- și exp-Wald; statistica privește coeficienții, nu doar varianțele; o dată cunoscută nu are nevoie de mediere."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Dynamic programming",
                "text": "What does dynamic programming achieve in the Bai-Perron estimator of m breaks?",
                "options": [
                    "It finds the global SSR minimiser over all partitions with O(T^2) segment regressions instead of O(T^m)",
                    "It replaces least squares by maximum likelihood",
                    "It estimates the breaks one at a time, conditional on the previous ones",
                    "It chooses the number of breaks automatically"
                ],
                "correctExplanation": "All segment SSRs are computed once (O(T^2)) and the Bellman recursion combines them; the solution is the exact global minimiser for every m up to M.",
                "incorrectExplanation": "The estimator remains least squares; sequential one-at-a-time estimation is a different, non-global method; the number of breaks is chosen afterwards by tests or criteria."
            },
            "ro": {
                "title": "Programarea dinamică",
                "text": "Ce realizează programarea dinamică în estimatorul Bai-Perron pentru m rupturi?",
                "options": [
                    "Găsește minimul global al SSR peste toate partițiile cu O(T^2) regresii pe segmente, în loc de O(T^m)",
                    "Înlocuiește cele mai mici pătrate cu verosimilitatea maximă",
                    "Estimează rupturile una cîte una, condiționat de cele anterioare",
                    "Alege automat numărul rupturilor"
                ],
                "correctExplanation": "Toate SSR pe segmente se calculează o singură dată (O(T^2)), iar recursia Bellman le combină; soluția este minimul global exact pentru orice m pînă la M.",
                "incorrectExplanation": "Estimatorul rămîne cel al celor mai mici pătrate; estimarea secvențială, una cîte una, este o altă metodă, care nu este globală; numărul rupturilor se alege ulterior prin teste sau criterii."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The sequential procedure",
                "text": "How does the sequential Bai-Perron procedure choose the number of breaks?",
                "options": [
                    "It adds breaks until BIC stops decreasing",
                    "Given l breaks, it tests for one more break inside each of the l + 1 segments and adds a break while the largest statistic rejects",
                    "It starts from the maximum M and removes the least significant break",
                    "It compares sup F(k) for all k and takes the largest"
                ],
                "correctExplanation": "The statistic sup F(l + 1 | l) takes the largest single-break statistic over the l + 1 segments of the l-break model; a rejection adds a break and the step is repeated.",
                "incorrectExplanation": "BIC is a separate criterion; the procedure goes upwards, not downwards; taking the largest sup F(k) is the UDmax test, which tests no break against an unknown number."
            },
            "ro": {
                "title": "Procedura secvențială",
                "text": "Cum alege procedura secvențială Bai-Perron numărul rupturilor?",
                "options": [
                    "Adaugă rupturi pînă cînd BIC nu mai scade",
                    "Dat fiind l rupturi, testează încă o ruptură în fiecare dintre cele l + 1 segmente și adaugă o ruptură cît timp cea mai mare statistică respinge",
                    "Pornește de la maximul M și elimină ruptura cea mai puțin semnificativă",
                    "Compară sup F(k) pentru toți k și îl alege pe cel mai mare"
                ],
                "correctExplanation": "Statistica sup F(l + 1 | l) ia cea mai mare statistică pentru o ruptură peste cele l + 1 segmente ale modelului cu l rupturi; o respingere adaugă o ruptură, iar pasul se repetă.",
                "incorrectExplanation": "BIC este un criteriu separat; procedura merge în sus, nu în jos; alegerea celui mai mare sup F(k) este testul UDmax, care testează nicio ruptură față de un număr necunoscut."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Information criteria",
                "text": "What is the known weakness of BIC for choosing the number of mean shifts?",
                "options": [
                    "It never selects any break",
                    "It needs HAC standard errors",
                    "It tends to select too many breaks when the errors are serially correlated",
                    "It can only be used with one break"
                ],
                "correctExplanation": "Serial correlation lowers the SSR of extra segments enough for BIC to accept spurious breaks; the LWZ criterion has a heavier penalty and errs the other way with small breaks.",
                "incorrectExplanation": "BIC does select breaks; it uses SSRs, not standard errors; it compares any number of breaks."
            },
            "ro": {
                "title": "Criterii informaționale",
                "text": "Care este slăbiciunea cunoscută a criteriului BIC în alegerea numărului de schimbări de medie?",
                "options": [
                    "Nu alege niciodată vreo ruptură",
                    "Are nevoie de erori standard HAC",
                    "Tinde să aleagă prea multe rupturi cînd erorile sînt autocorelate",
                    "Poate fi folosit doar cu o ruptură"
                ],
                "correctExplanation": "Autocorelația reduce SSR al segmentelor suplimentare suficient ca BIC să accepte rupturi false; criteriul LWZ are o penalizare mai mare și greșește în sens invers cu rupturi mici.",
                "incorrectExplanation": "BIC alege rupturi; folosește SSR, nu erori standard; compară orice număr de rupturi."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Confidence interval for a break date",
                "text": "In the Bai (1997) interval for a mean-shift date, which situation gives the shortest interval?",
                "options": [
                    "A small shift and a large error variance",
                    "A long sample with no shift",
                    "Errors with a large long-run variance",
                    "A large shift relative to the long-run standard deviation of the errors"
                ],
                "correctExplanation": "The date error is scaled by delta^2 / sigma^2 (long-run variance): the half-width is about 11 sigma^2/delta^2 periods for a 95% interval with equal variances.",
                "incorrectExplanation": "A small shift or a large (long-run) variance widens the interval; without a shift there is no date to estimate."
            },
            "ro": {
                "title": "Intervalul de încredere pentru data unei rupturi",
                "text": "În intervalul Bai (1997) pentru data unei schimbări de medie, ce situație dă cel mai scurt interval?",
                "options": [
                    "O schimbare mică și o varianță mare a erorilor",
                    "Un eșantion lung, fără nicio schimbare",
                    "Erori cu o varianță de termen lung mare",
                    "O schimbare mare în raport cu abaterea standard de termen lung a erorilor"
                ],
                "correctExplanation": "Eroarea datei este scalată prin delta^2 / sigma^2 (varianța de termen lung): semilățimea este de aproximativ 11 sigma^2/delta^2 perioade pentru un interval de 95% cu varianțe egale.",
                "incorrectExplanation": "O schimbare mică sau o varianță (de termen lung) mare lărgesc intervalul; fără schimbare nu există nicio dată de estimat."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Testing a variance break",
                "text": "McConnell and Perez-Quiros (2000) test for a break in the volatility of US GDP growth. Which variable do they test for a break in its mean?",
                "options": [
                    "sqrt(pi/2) times the absolute residual of an AR(1) for growth",
                    "The level of GDP growth",
                    "The squared level of GDP",
                    "The AR(1) coefficient of growth"
                ],
                "correctExplanation": "Under Normality E|e_t| = sigma sqrt(2/pi), so sqrt(pi/2)|e_t| is an unbiased estimate of the standard deviation; a break in its mean is a break in volatility (dated 1984Q1).",
                "incorrectExplanation": "The level of growth and the AR coefficient concern the conditional mean, which showed no break; the level of GDP is nonstationary."
            },
            "ro": {
                "title": "Testarea unei rupturi în varianță",
                "text": "McConnell și Perez-Quiros (2000) testează o ruptură în volatilitatea creșterii PIB din SUA. Pentru ce variabilă testează o ruptură în medie?",
                "options": [
                    "sqrt(pi/2) înmulțit cu reziduul absolut al unui AR(1) pentru creștere",
                    "Nivelul creșterii PIB",
                    "Nivelul PIB la pătrat",
                    "Coeficientul AR(1) al creșterii"
                ],
                "correctExplanation": "Sub distribuția Normală E|e_t| = sigma sqrt(2/pi), deci sqrt(pi/2)|e_t| este o estimare nedeplasată a abaterii standard; o ruptură în media ei este o ruptură în volatilitate (datată T1 1984).",
                "incorrectExplanation": "Nivelul creșterii și coeficientul AR privesc media condiționată, care nu a avut nicio ruptură; nivelul PIB este nestaționar."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Monitoring",
                "text": "A central bank repeats a 5% stability test every month as new data arrive, for many years. What happens under a true null of no break?",
                "options": [
                    "The overall false-alarm rate stays at 5%",
                    "A false alarm occurs eventually with probability one",
                    "The false-alarm rate falls to zero as data accumulate",
                    "The test becomes undersized but valid"
                ],
                "correctExplanation": "By the law of the iterated logarithm, a one-shot boundary is crossed eventually; the simulation in the lecture gives about 52% false alarms by n = 10m. The CSW boundary controls the size.",
                "incorrectExplanation": "Repeated testing does not keep the size; more data do not remove the repeated-testing problem; the test is oversized, not undersized."
            },
            "ro": {
                "title": "Monitorizarea",
                "text": "O bancă centrală repetă în fiecare lună, ani la rînd, un test de stabilitate de 5% pe măsură ce sosesc date noi. Ce se întîmplă sub o ipoteză nulă adevărată fără ruptură?",
                "options": [
                    "Rata totală a alarmelor false rămîne 5%",
                    "O alarmă falsă apare pînă la urmă cu probabilitatea unu",
                    "Rata alarmelor false scade la zero pe măsură ce se acumulează datele",
                    "Testul respinge prea rar, dar rămîne valid"
                ],
                "correctExplanation": "Din legea logaritmului iterat, o frontieră pentru un test unic este depășită pînă la urmă; simularea din curs dă aproximativ 52% alarme false pînă la n = 10m. Frontiera CSW controlează mărimea.",
                "incorrectExplanation": "Testarea repetată nu păstrează mărimea; mai multe date nu elimină problema testării repetate; testul respinge prea des, nu prea rar."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The CSW boundary",
                "text": "With m historical observations, the Chu-Stinchcombe-White CUSUM detector stops when the cumulated standardised recursive residuals exceed which boundary?",
                "options": [
                    "1.96 sqrt(n - m)",
                    "0.948 sqrt(n)",
                    "sqrt(n [a^2 + ln(n/m)])",
                    "a constant equal to the 5% critical value of sup-Wald"
                ],
                "correctExplanation": "The boundary comes from the Robbins-Siegmund crossing probability 2[1 - Phi(a) + a phi(a)]; a^2 = 7.78 gives about 5% over an infinite horizon.",
                "incorrectExplanation": "1.96 sqrt(n - m) is the repeated one-shot test; 0.948 is the constant of the retrospective CUSUM of Brown, Durbin and Evans; a constant boundary would be crossed eventually."
            },
            "ro": {
                "title": "Frontiera CSW",
                "text": "Cu m observații istorice, detectorul CUSUM Chu-Stinchcombe-White se oprește cînd reziduurile recursive standardizate cumulate depășesc ce frontieră?",
                "options": [
                    "1,96 sqrt(n - m)",
                    "0,948 sqrt(n)",
                    "sqrt(n [a^2 + ln(n/m)])",
                    "o constantă egală cu valoarea critică de 5% a sup-Wald"
                ],
                "correctExplanation": "Frontiera vine din probabilitatea de depășire Robbins-Siegmund 2[1 - Phi(a) + a phi(a)]; a^2 = 7,78 dă aproximativ 5% pe un orizont infinit.",
                "incorrectExplanation": "1,96 sqrt(n - m) este testul unic repetat; 0,948 este constanta CUSUM-ului retrospectiv Brown, Durbin și Evans; o frontieră constantă ar fi depășită pînă la urmă."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "ICSS and fat tails",
                "text": "On daily EUR/RON returns the Inclán-Tiao ICSS finds 46 variance breaks and the kappa-2 version finds 5. Which explanation is correct?",
                "options": [
                    "The kappa-2 statistic has a different limiting distribution",
                    "The Inclán-Tiao statistic uses absolute returns instead of squares",
                    "The kappa-2 statistic ignores the first and last 15% of the sample",
                    "The Inclán-Tiao scaling assumes Var(a^2) = 2 sigma^4; fat tails and volatility clustering inflate it, while kappa-2 uses a long-run variance of a^2"
                ],
                "correctExplanation": "Sansó, Aragó and Carrion (2004): with kurtosis kappa the IT statistic is inflated by sqrt((kappa - 1)/2), and GARCH adds autocorrelation of a^2; kappa-2 keeps the same Brownian bridge limit.",
                "incorrectExplanation": "Both statistics share the sup |Brownian bridge| limit (5% value 1.358); both use squares; neither trims the sample in this way."
            },
            "ro": {
                "title": "ICSS și cozile groase",
                "text": "Pe randamentele zilnice EUR/RON, ICSS cu statistica Inclán-Tiao găsește 46 de rupturi în varianță, iar varianta kappa-2 găsește 5. Ce explicație este corectă?",
                "options": [
                    "Statistica kappa-2 are o altă distribuție-limită",
                    "Statistica Inclán-Tiao folosește randamentele absolute în locul pătratelor",
                    "Statistica kappa-2 ignoră primele și ultimele 15% din eșantion",
                    "Scalarea Inclán-Tiao presupune Var(a^2) = 2 sigma^4; cozile groase și volatility clustering o umflă, în timp ce kappa-2 folosește o varianță de termen lung a lui a^2"
                ],
                "correctExplanation": "Sansó, Aragó și Carrion (2004): cu coeficientul de boltire kappa, statistica IT este mărită de sqrt((kappa - 1)/2) ori, iar GARCH adaugă autocorelația lui a^2; kappa-2 păstrează aceeași limită a punții browniene.",
                "incorrectExplanation": "Ambele statistici au limita sup |punte browniană| (valoarea de 5% 1,358); ambele folosesc pătrate; niciuna nu trunchiază eșantionul în acest fel."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Unit roots with breaks",
                "text": "What is the main weakness of the Zivot-Andrews test identified by Lee and Strazicich (2003)?",
                "options": [
                    "Its null hypothesis is a unit root without a break, so a break under the null can make it reject a true unit root",
                    "It cannot estimate the break date",
                    "It assumes the break date is known",
                    "It allows only for breaks in the variance"
                ],
                "correctExplanation": "If the data have a unit root and a break, the test may reject and attribute the break to a stationary alternative; LM tests whose null allows breaks, and the Kim-Perron pre-test, fix this.",
                "incorrectExplanation": "Zivot-Andrews estimates the date by minimising the t statistic, so it does not assume it known; it models breaks in level and trend, not variance."
            },
            "ro": {
                "title": "Rădăcini unitare cu rupturi",
                "text": "Care este principala slăbiciune a testului Zivot-Andrews identificată de Lee și Strazicich (2003)?",
                "options": [
                    "Ipoteza lui nulă este o rădăcină unitară fără ruptură, deci o ruptură sub ipoteza nulă îl poate face să respingă o rădăcină unitară adevărată",
                    "Nu poate estima data rupturii",
                    "Presupune că data rupturii este cunoscută",
                    "Admite doar rupturi în varianță"
                ],
                "correctExplanation": "Dacă datele au o rădăcină unitară și o ruptură, testul poate respinge și atribui ruptura unei alternative staționare; testele LM a căror ipoteză nulă admite rupturi și testul preliminar Kim-Perron rezolvă problema.",
                "incorrectExplanation": "Zivot-Andrews estimează data minimizînd statistica t, deci nu o presupune cunoscută; modelează rupturi în nivel și în trend, nu în varianță."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The estimation window",
                "text": "After a mean shift of size delta that happened n2 periods ago, when does the MSFE-optimal window include some pre-break observations?",
                "options": [
                    "Never: only post-break data should be used",
                    "When delta/sigma is small or n2 is short, so that the variance reduction outweighs the bias",
                    "Only when the break date is unknown",
                    "Always: the expanding window is optimal"
                ],
                "correctExplanation": "MSFE(w) = sigma^2(1 + 1/w) + [(w - n2) delta / w]^2: old data add bias but cut variance; Pesaran and Timmermann (2007) show the optimum can lie before the break.",
                "incorrectExplanation": "Using only post-break data is optimal only for large breaks; the trade-off exists even with a known date; the expanding window is optimal only without a break."
            },
            "ro": {
                "title": "Fereastra de estimare",
                "text": "După o schimbare de medie de mărime delta, petrecută acum n2 perioade, cînd include fereastra optimă după MSFE cîteva observații dinaintea rupturii?",
                "options": [
                    "Niciodată: trebuie folosite doar datele de după ruptură",
                    "Cînd delta/sigma este mic sau n2 este scurt, astfel încît reducerea varianței depășește deplasarea",
                    "Doar cînd data rupturii este necunoscută",
                    "Întotdeauna: fereastra extinsă este optimă"
                ],
                "correctExplanation": "MSFE(w) = sigma^2(1 + 1/w) + [(w - n2) delta / w]^2: datele vechi adaugă deplasare, dar reduc varianța; Pesaran și Timmermann (2007) arată că optimul poate fi înaintea rupturii.",
                "incorrectExplanation": "Folosirea doar a datelor de după ruptură este optimă numai pentru rupturi mari; compromisul există și cu o dată cunoscută; fereastra extinsă este optimă doar fără ruptură."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Averaging across windows",
                "text": "What does the AveW forecast of Pesaran and Pick (2011) do?",
                "options": [
                    "It selects the window with the smallest in-sample SSR",
                    "It estimates the break date and uses only post-break data",
                    "It averages the forecasts obtained with many estimation windows, from short to the full sample",
                    "It averages the observations over a rolling window of fixed length"
                ],
                "correctExplanation": "Averaging across windows is robust to the uncertain size and date of breaks; in the lecture it beat the expanding window for Romanian inflation one month ahead (HLN p about 0.03).",
                "incorrectExplanation": "Selecting by in-sample SSR favours short windows and overfits; post-break estimation needs a date; a rolling mean uses a single window."
            },
            "ro": {
                "title": "Medierea peste ferestre",
                "text": "Ce face prognoza AveW a lui Pesaran și Pick (2011)?",
                "options": [
                    "Alege fereastra cu cel mai mic SSR în eșantion",
                    "Estimează data rupturii și folosește doar datele de după ruptură",
                    "Mediază prognozele obținute cu multe ferestre de estimare, de la scurte pînă la întregul eșantion",
                    "Mediază observațiile pe o fereastră mobilă de lungime fixă"
                ],
                "correctExplanation": "Medierea peste ferestre este robustă la mărimea și data incerte ale rupturilor; în curs a bătut fereastra extinsă pentru inflația din România la o lună (HLN p aproximativ 0,03).",
                "incorrectExplanation": "Alegerea după SSR în eșantion favorizează ferestrele scurte și supraajustează; estimarea după ruptură cere o dată; media mobilă folosește o singură fereastră."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "SETAR stationarity",
                "text": "A SETAR(2; 1, 1) has AR coefficients phi1 = 0.5 and phi2 = -1.5. Is it ergodic?",
                "options": [
                    "No, because one regime is explosive on its own",
                    "No, because phi1 + phi2 < 0",
                    "Only if the threshold is zero",
                    "Yes, because phi1 < 1, phi2 < 1 and phi1 phi2 < 1"
                ],
                "correctExplanation": "The ergodicity conditions of a SETAR(2; 1, 1) are phi1 < 1, phi2 < 1 and phi1 phi2 < 1; here phi1 phi2 = -0.75. An explosive regime can be stable when the process leaves it quickly.",
                "incorrectExplanation": "A regime explosive on its own does not prevent ergodicity; the sum of the coefficients is not the condition; the conditions do not depend on the threshold value."
            },
            "ro": {
                "title": "Staționaritatea SETAR",
                "text": "Un SETAR(2; 1, 1) are coeficienții AR phi1 = 0,5 și phi2 = -1,5. Este ergodic?",
                "options": [
                    "Nu, pentru că un regim este exploziv luat separat",
                    "Nu, pentru că phi1 + phi2 < 0",
                    "Doar dacă pragul este zero",
                    "Da, pentru că phi1 < 1, phi2 < 1 și phi1 phi2 < 1"
                ],
                "correctExplanation": "Condițiile de ergodicitate ale unui SETAR(2; 1, 1) sînt phi1 < 1, phi2 < 1 și phi1 phi2 < 1; aici phi1 phi2 = -0,75. Un regim exploziv poate fi stabil cînd procesul îl părăsește repede.",
                "incorrectExplanation": "Un regim exploziv luat separat nu împiedică ergodicitatea; suma coeficienților nu este condiția; condițiile nu depind de valoarea pragului."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Testing for a threshold",
                "text": "Why does Hansen (1996) compute p-values of the sup-Wald test for a TAR by a bootstrap?",
                "options": [
                    "Because the threshold is not identified under linearity and the limiting distribution depends on the data",
                    "Because the errors are always non-Normal",
                    "Because the threshold estimator is super-consistent",
                    "Because the sample is too short for asymptotics"
                ],
                "correctExplanation": "This is the Davies problem: the limit of sup W is a functional of a Gaussian process whose covariance depends on the regressors; the fixed-regressor bootstrap simulates it.",
                "incorrectExplanation": "Non-Normal errors alone would not require a bootstrap; super-consistency concerns estimation under the alternative; the bootstrap reproduces the asymptotic distribution, not a small-sample correction."
            },
            "ro": {
                "title": "Testarea unui prag",
                "text": "De ce calculează Hansen (1996) valorile p ale testului sup-Wald pentru un TAR prin bootstrap?",
                "options": [
                    "Pentru că pragul nu este identificat sub liniaritate, iar distribuția-limită depinde de date",
                    "Pentru că erorile nu urmează niciodată distribuția Normală",
                    "Pentru că estimatorul pragului este superconsistent",
                    "Pentru că eșantionul este prea scurt pentru asimptotică"
                ],
                "correctExplanation": "Aceasta este problema Davies: limita lui sup W este o funcțională a unui proces gaussian a cărui covarianță depinde de regresori; bootstrap-ul cu regresori ficși o simulează.",
                "incorrectExplanation": "Erorile non-Normale singure nu ar cere bootstrap; superconsistența privește estimarea sub alternativă; bootstrap-ul reproduce distribuția asimptotică, nu o corecție pentru eșantion mic."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Confidence interval for a threshold",
                "text": "Hansen (2000) builds a 95% confidence set for the threshold gamma by collecting the values with LR(gamma) below which number?",
                "options": [
                    "3.84",
                    "7.35",
                    "8.65",
                    "1.358"
                ],
                "correctExplanation": "The limit of the LR is xi with P(xi <= x) = (1 - exp(-x/2))^2, so the 95% value is -2 ln(1 - sqrt(0.95)) = 7.35.",
                "incorrectExplanation": "3.84 is the chi2(1) value; 8.65 is the 5% value of sup-Wald with one restriction; 1.358 is the 5% value of the supremum of a Brownian bridge (ICSS)."
            },
            "ro": {
                "title": "Intervalul de încredere pentru prag",
                "text": "Hansen (2000) construiește o mulțime de încredere de 95% pentru pragul gamma adunînd valorile cu LR(gamma) sub ce număr?",
                "options": [
                    "3,84",
                    "7,35",
                    "8,65",
                    "1,358"
                ],
                "correctExplanation": "Limita lui LR este xi cu P(xi <= x) = (1 - exp(-x/2))^2, deci valoarea de 95% este -2 ln(1 - sqrt(0,95)) = 7,35.",
                "incorrectExplanation": "3,84 este valoarea pentru chi2(1); 8,65 este valoarea de 5% a sup-Wald cu o restricție; 1,358 este valoarea de 5% a supremumului unei punți browniene (ICSS)."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "LSTAR limits",
                "text": "In an LSTAR with transition G = [1 + exp(-gamma (s - c) / sigma_s)]^(-1), what happens as gamma tends to infinity?",
                "options": [
                    "The model becomes a linear AR",
                    "The model becomes an ESTAR",
                    "The model becomes a two-regime threshold autoregression",
                    "The transition variable drops out of the model"
                ],
                "correctExplanation": "As gamma grows, G becomes the indicator 1{s > c}: abrupt switching, the TAR; as gamma tends to 0, G tends to 1/2 and the model is linear.",
                "incorrectExplanation": "The linear AR is the gamma -> 0 limit; ESTAR uses a different (exponential) transition; the transition variable defines the regimes in the TAR limit."
            },
            "ro": {
                "title": "Limitele LSTAR",
                "text": "Într-un LSTAR cu tranziția G = [1 + exp(-gamma (s - c) / sigma_s)]^(-1), ce se întîmplă cînd gamma tinde la infinit?",
                "options": [
                    "Modelul devine un AR liniar",
                    "Modelul devine un ESTAR",
                    "Modelul devine o autoregresie cu prag cu două regimuri",
                    "Variabila de tranziție dispare din model"
                ],
                "correctExplanation": "Cînd gamma crește, G devine indicatorul 1{s > c}: o comutare bruscă, adică TAR; cînd gamma tinde la 0, G tinde la 1/2, iar modelul este liniar.",
                "incorrectExplanation": "AR-ul liniar este limita pentru gamma -> 0; ESTAR folosește o altă tranziție (exponențială); în limita TAR variabila de tranziție definește regimurile."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Choosing the STAR family",
                "text": "In the Teräsvirta (1994) sequence, the strongest rejection is for H03: beta2 = 0 given beta3 = 0. Which family does the rule suggest?",
                "options": [
                    "LSTAR, because the cubic term is significant",
                    "A linear model",
                    "A TAR with two thresholds",
                    "ESTAR, because its Taylor expansion has squared terms but no cubic term"
                ],
                "correctExplanation": "The expansion of 1 - exp(-gamma(s - c)^2) contains only even powers to first order, so ESTAR shows up through beta2; LSTAR shows up through beta1 and beta3.",
                "incorrectExplanation": "A strong H04 or H02 rejection points to LSTAR; a rejection rules out linearity; the sequence chooses between LSTAR and ESTAR, not between thresholds."
            },
            "ro": {
                "title": "Alegerea familiei STAR",
                "text": "În secvența Teräsvirta (1994), cea mai puternică respingere este pentru H03: beta2 = 0 dat fiind beta3 = 0. Ce familie sugerează regula?",
                "options": [
                    "LSTAR, pentru că termenul cubic este semnificativ",
                    "Un model liniar",
                    "Un TAR cu două praguri",
                    "ESTAR, pentru că dezvoltarea lui Taylor are termeni la pătrat, dar nu are termen cubic"
                ],
                "correctExplanation": "Dezvoltarea lui 1 - exp(-gamma(s - c)^2) conține, la ordinul întîi, doar puteri pare, deci ESTAR apare prin beta2; LSTAR apare prin beta1 și beta3.",
                "incorrectExplanation": "O respingere puternică pentru H04 sau H02 indică LSTAR; o respingere exclude liniaritatea; secvența alege între LSTAR și ESTAR, nu între praguri."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Half-lives in an ESTAR",
                "text": "In the ESTAR of Taylor, Peel and Sarno (2001), why are half-lives reported for several shock sizes?",
                "options": [
                    "Because mean reversion strengthens with the size of the deviation, so large shocks die out faster than small ones",
                    "Because the model is linear and the half-life is a scale factor",
                    "Because the variance of the shocks changes over time",
                    "Because the half-life does not exist for small shocks"
                ],
                "correctExplanation": "The local AR coefficient exp(-theta^2 x^2) falls with the deviation x; in the lecture the half-life is about 29 months for a 1% shock and 7 months for a 40% shock.",
                "incorrectExplanation": "In a linear model the shock size is a scale factor, which is exactly what fails here; the error variance is constant in the model; small shocks have long but finite half-lives."
            },
            "ro": {
                "title": "Timpii de înjumătățire într-un ESTAR",
                "text": "În ESTAR-ul lui Taylor, Peel și Sarno (2001), de ce se raportează timpi de înjumătățire pentru mai multe mărimi ale șocului?",
                "options": [
                    "Pentru că revenirea la medie se întărește cu mărimea abaterii, deci șocurile mari se sting mai repede decît cele mici",
                    "Pentru că modelul este liniar, iar timpul de înjumătățire este un factor de scală",
                    "Pentru că varianța șocurilor se schimbă în timp",
                    "Pentru că timpul de înjumătățire nu există pentru șocuri mici"
                ],
                "correctExplanation": "Coeficientul AR local exp(-theta^2 x^2) scade cu abaterea x; în curs timpul de înjumătățire este de aproximativ 29 de luni pentru un șoc de 1% și 7 luni pentru un șoc de 40%.",
                "incorrectExplanation": "Într-un model liniar mărimea șocului este un factor de scală, exact ce nu mai este valabil aici; varianța erorilor este constantă în model; șocurile mici au timpi de înjumătățire lungi, dar finiți."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Multi-step nonlinear forecasts",
                "text": "How should a two-step-ahead conditional mean forecast of a SETAR be computed?",
                "options": [
                    "By iterating the skeleton twice, ignoring the noise",
                    "By simulating many paths with resampled residuals and averaging them",
                    "By using the linear AR coefficients of the lower regime",
                    "By taking the threshold value as the forecast"
                ],
                "correctExplanation": "For h >= 2, E[F(F(y) + e)] differs from F(F(y)) because F is nonlinear (Jensen); simulation also gives the predictive density, which may be skewed or bimodal.",
                "incorrectExplanation": "The skeleton forecast is biased; one regime alone ignores switching; the threshold is a parameter, not a forecast."
            },
            "ro": {
                "title": "Prognoze neliniare pe mai mulți pași",
                "text": "Cum trebuie calculată prognoza mediei condiționate la doi pași a unui SETAR?",
                "options": [
                    "Prin iterarea de două ori a scheletului, ignorînd zgomotul",
                    "Prin simularea mai multor traiectorii cu reziduuri reeșantionate și medierea lor",
                    "Prin folosirea coeficienților AR liniari ai regimului inferior",
                    "Prin luarea valorii pragului ca prognoză"
                ],
                "correctExplanation": "Pentru h >= 2, E[F(F(y) + e)] diferă de F(F(y)) deoarece F este neliniară (Jensen); simularea dă și densitatea predictivă, care poate fi asimetrică sau bimodală.",
                "incorrectExplanation": "Prognoza prin schelet este deplasată; un singur regim ignoră comutarea; pragul este un parametru, nu o prognoză."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: \"On daily EUR/RON returns the BDS test rejects independence of the AR residuals with p < 0.001, so the conditional mean follows a threshold model.\" What is wrong?",
                "options": [
                    "BDS cannot be applied to residuals",
                    "A p-value below 0.001 is not significant for daily data",
                    "BDS has power against any dependence, including volatility clustering; the heteroskedasticity-robust TAR test does not reject (p about 0.15)",
                    "Daily returns cannot be nonlinear"
                ],
                "correctExplanation": "BDS is a general test of i.i.d.; ARCH effects alone make it reject. Only a test aimed at the conditional mean and robust to heteroskedasticity can support a threshold model.",
                "incorrectExplanation": "BDS is designed for residuals of linear models; p < 0.001 is significant; daily returns can be nonlinear, but this test does not show which kind."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Pe randamentele zilnice EUR/RON, testul BDS respinge independența reziduurilor AR cu p < 0,001, deci media condiționată urmează un model cu prag.” Ce este greșit?",
                "options": [
                    "BDS nu se poate aplica reziduurilor",
                    "O valoare p sub 0,001 nu este semnificativă pentru date zilnice",
                    "BDS are putere împotriva oricărei dependențe, inclusiv volatility clustering; testul TAR robust la heteroscedasticitate nu respinge (p aproximativ 0,15)",
                    "Randamentele zilnice nu pot fi neliniare"
                ],
                "correctExplanation": "BDS este un test general pentru i.i.d.; doar efectele ARCH îl fac să respingă. Doar un test care vizează media condiționată și este robust la heteroscedasticitate poate susține un model cu prag.",
                "incorrectExplanation": "BDS este conceput pentru reziduurile modelelor liniare; p < 0,001 este semnificativ; randamentele zilnice pot fi neliniare, dar acest test nu arată ce tip de neliniaritate este."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Find the error in the AI answer",
                "text": "An AI assistant writes: \"The KSS test rejects a unit root for the real dollar-sterling rate (p about 0.04), so nonlinear mean reversion (ESTAR) is established.\" What is the main flaw?",
                "options": [
                    "The KSS test cannot be applied to exchange rates",
                    "A p-value of 0.04 means the unit root is accepted",
                    "KSS tests against LSTAR, not ESTAR",
                    "A few shifts in the mean can produce the same rejection; when Bai-Perron mean regimes are part of the null procedure the evidence disappears (p about 0.8)"
                ],
                "correctExplanation": "Structural breaks and nonlinearity mimic each other (Carrasco 2002); in the lecture mini-case the KSS statistic within regimes is not significant once the break search is simulated under the null.",
                "incorrectExplanation": "KSS is designed for real exchange rates; p = 0.04 rejects at 5%; KSS has ESTAR as its alternative."
            },
            "ro": {
                "title": "Găsiți eroarea din răspunsul AI",
                "text": "Un asistent AI scrie: „Testul KSS respinge rădăcina unitară pentru cursul real dolar-liră (p aproximativ 0,04), deci revenirea neliniară la medie (ESTAR) este demonstrată.” Care este principala greșeală?",
                "options": [
                    "Testul KSS nu se poate aplica cursurilor de schimb",
                    "O valoare p de 0,04 înseamnă că rădăcina unitară este acceptată",
                    "KSS testează față de LSTAR, nu față de ESTAR",
                    "Cîteva schimbări ale mediei pot produce aceeași respingere; cînd regimurile de medie Bai-Perron fac parte din procedura sub ipoteza nulă, dovezile dispar (p aproximativ 0,8)"
                ],
                "correctExplanation": "Rupturile structurale și neliniaritatea se imită reciproc (Carrasco 2002); în mini studiul de caz din curs, statistica KSS în interiorul regimurilor nu este semnificativă odată ce căutarea rupturilor este simulată sub ipoteza nulă.",
                "incorrectExplanation": "KSS este conceput pentru cursurile reale; p = 0,04 respinge la 5%; KSS are ESTAR ca alternativă."
            }
        }
    ]
};
