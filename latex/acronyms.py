r"""
acronyms.py -- dictionarul acronimelor cursului ATS si inserarea glosarului in fiecare deck
===========================================================================================
(Preluat din MFM; acelasi dictionar comun A, plus latex/acronyms_extra/chN.py pentru capitolele 0-16 ale ATS.)
Fiecare acronim este explicat in limba lui de origine, urmat de traducere in limba deck-ului:
  deck RO, acronim englezesc:  SML -- Security Market Line (dreapta pieței titlurilor)
  deck EN, acronim românesc:   BVB -- Bursa de Valori București (the Bucharest Stock Exchange)

Se proceseaza DOAR deck-urile din noul flux (latex/ats_chapters.py: numele noi si \input{../../latex/preamble});
deck-urile vechi (RO/Courses, RO/Seminars, EN/Courses cu nume vechi) nu sint atinse.

Rulare (dupa orice modificare a unui deck sau a unui generator):
    python3 latex/acronyms.py
Scriptul detecteaza acronimele din fiecare deck, insereaza un glosar imediat dupa pagina de
titlu (inaintea cuprinsului, deci inaintea oricarei alte aparitii) si elimina vechile slide-uri
de glosar de la final. Este idempotent (blocul inserat este marcat cu % BEGIN-ACRONYMS).
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# acronim: (forma de origine, limba de origine, traducere RO, traducere EN)
A = {
    # --- statistica si econometrie
    'ACF': ('Autocorrelation Function', 'en', 'funcția de autocorelație', None),
    'ADF': ('Augmented Dickey–Fuller (test)', 'en', 'testul Dickey–Fuller augmentat', None),
    'VAR': ('Vector AutoRegression', 'en', 'model vector autoregresiv', None),
    'AR': ('AutoRegressive (model); in event studies: Abnormal Return', 'en', 'model autoregresiv; în studiile de eveniment: randament anormal', None),
    'ARCH': ('AutoRegressive Conditional Heteroskedasticity', 'en', 'heteroscedasticitate condiționată autoregresivă', None),
    'ARCH-LM': ('ARCH Lagrange Multiplier (test)', 'en', 'testul multiplicatorului Lagrange pentru efecte ARCH', None),
    'BDS': ('Brock–Dechert–Scheinkman (test)', 'en', 'testul Brock–Dechert–Scheinkman de independență', None),
    'BH': ('Benjamini–Hochberg (procedure)', 'en', 'procedura Benjamini–Hochberg', None),
    'CD': ('Chow–Denning (multiple variance-ratio test)', 'en', 'testul multiplu Chow–Denning pentru raportul varianțelor', None),
    'CI': ('Confidence Interval', 'en', 'interval de încredere', None),
    'IC': ('Interval de încredere', 'ro', None, 'confidence interval'),
    'CLT': ('Central Limit Theorem', 'en', 'teorema limită centrală', None),
    'TLC': ('Teorema Limită Centrală', 'ro', None, 'central limit theorem'),
    'DCC': ('Dynamic Conditional Correlation', 'en', 'corelație condiționată dinamică', None),
    'DFA': ('Detrended Fluctuation Analysis', 'en', 'analiza fluctuațiilor fără tendință', None),
    'DM': ('Diebold–Mariano (test)', 'en', 'testul Diebold–Mariano de comparare a prognozelor', None),
    'EGARCH': ('Exponential GARCH', 'en', 'GARCH exponențial', None),
    'EWMA': ('Exponentially Weighted Moving Average', 'en', 'medie mobilă ponderată exponențial', None),
    'FDR': ('False Discovery Rate', 'en', 'rata descoperirilor false', None),
    'FM': ('Fama–MacBeth (regressions)', 'en', 'regresiile Fama–MacBeth', None),
    'FWER': ('Family-Wise Error Rate', 'en', 'probabilitatea de cel puțin o eroare de tip I în familia de teste', None),
    'GARCH': ('Generalised AutoRegressive Conditional Heteroskedasticity', 'en', 'heteroscedasticitate condiționată autoregresivă generalizată', None),
    'GJR-GARCH': ('Glosten–Jagannathan–Runkle GARCH', 'en', 'GARCH asimetric Glosten–Jagannathan–Runkle', None),
    'GMM': ('Generalized Method of Moments', 'en', 'metoda generalizată a momentelor', None),
    'GRS': ('Gibbons–Ross–Shanken (test)', 'en', 'testul Gibbons–Ross–Shanken', None),
    'HAC': ('Heteroskedasticity and Autocorrelation Consistent (standard errors)', 'en', 'erori standard robuste la heteroscedasticitate și autocorelație', None),
    'HAR': ('Heterogeneous AutoRegressive (model)', 'en', 'model autoregresiv heterogen', None),
    'HAR-RV': ('Heterogeneous AutoRegressive model of Realised Volatility', 'en', 'model autoregresiv heterogen al volatilității realizate', None),
    'HP': ('Hodrick–Prescott (filter)', 'en', 'filtrul Hodrick–Prescott', None),
    'JB': ('Jarque–Bera (test)', 'en', 'testul de normalitate Jarque–Bera', None),
    'LB': ('Ljung–Box (test)', 'en', 'testul de autocorelație Ljung–Box', None),
    'LM': ('Lagrange Multiplier', 'en', 'multiplicatorul Lagrange', None),
    'MA': ('Moving Average', 'en', 'medie mobilă', None),
    'MA20': ('20-day Moving Average', 'en', 'medie mobilă pe 20 de zile', None),
    'MAD': ('Median Absolute Deviation', 'en', 'abaterea absolută mediană', None),
    'MLE': ('Maximum Likelihood Estimation', 'en', 'estimarea prin metoda verosimilității maxime', None),
    'NW': ('Newey–West (standard errors)', 'en', 'erori standard Newey–West', None),
    'OLS': ('Ordinary Least Squares', 'en', 'metoda celor mai mici pătrate', None),
    'PC1': ('first Principal Component', 'en', 'prima componentă principală', None),
    'PC2': ('second Principal Component', 'en', 'a doua componentă principală', None),
    'PC3': ('third Principal Component', 'en', 'a treia componentă principală', None),
    'PCA': ('Principal Component Analysis', 'en', 'analiza componentelor principale', None),
    'PCR': ('Principal Component Regression', 'en', 'regresia pe componente principale', None),
    'PLS': ('Partial Least Squares', 'en', 'regresia prin cele mai mici pătrate parțiale', None),
    'QQ': ('Quantile–Quantile (plot)', 'en', 'graficul cuantilă–cuantilă', None),
    'RMSE': ('Root Mean Squared Error', 'en', 'rădăcina erorii pătratice medii', None),
    'RW1': ('Random Walk 1 (i.i.d. increments)', 'en', 'mersul aleator 1 (creșteri i.i.d.)', None),
    'RW2': ('Random Walk 2 (independent increments)', 'en', 'mersul aleator 2 (creșteri independente)', None),
    'RW3': ('Random Walk 3 (uncorrelated increments)', 'en', 'mersul aleator 3 (creșteri necorelate)', None),
    'SE': ('Standard Error', 'en', 'eroare standard', None),
    'VR': ('Variance Ratio', 'en', 'raportul varianțelor', None),
    # --- serii de timp (din TSA)
    'ACVF': ('AutoCoVariance Function', 'en', 'funcția de autocovarianță', None),
    'AIC': ('Akaike Information Criterion', 'en', 'criteriul informațional Akaike', None),
    'AICc': ('corrected Akaike Information Criterion', 'en', 'criteriul Akaike corectat', None),
    'ARFIMA': ('AutoRegressive Fractionally Integrated Moving Average (model)', 'en', 'model autoregresiv fracționar integrat cu medie mobilă', None),
    'ARIMA': ('AutoRegressive Integrated Moving Average (model)', 'en', 'model autoregresiv integrat cu medie mobilă', None),
    'ARMA': ('AutoRegressive Moving Average (model)', 'en', 'model autoregresiv cu medie mobilă', None),
    'BEKK': ('Baba–Engle–Kraft–Kroner (multivariate GARCH model)', 'en', 'modelul GARCH multivariat Baba–Engle–Kraft–Kroner', None),
    'BIC': ('Bayesian Information Criterion', 'en', 'criteriul informațional bayesian (Schwarz)', None),
    'CCC': ('Constant Conditional Correlation (model)', 'en', 'model cu corelație condiționată constantă', None),
    'CPI': ('Consumer Price Index', 'en', 'indicele prețurilor de consum', None),
    'DFT': ('Discrete Fourier Transform', 'en', 'transformata Fourier discretă', None),
    'DGP': ('Data-Generating Process', 'en', 'procesul generator al datelor', None),
    'ETS': ('Error, Trend, Seasonality (exponential smoothing state space models)', 'en', 'eroare, trend, sezonalitate (modele de netezire exponențială)', None),
    'FEVD': ('Forecast Error Variance Decomposition', 'en', 'descompunerea varianței erorii de prognoză', None),
    'FFT': ('Fast Fourier Transform', 'en', 'transformata Fourier rapidă', None),
    'GDP': ('Gross Domestic Product', 'en', 'produsul intern brut', None),
    'GPH': ('Geweke–Porter-Hudak (estimator)', 'en', 'estimatorul Geweke–Porter-Hudak al parametrului de memorie lungă', None),
    'HEGY': ('Hylleberg–Engle–Granger–Yoo (seasonal unit-root test)', 'en', 'testul Hylleberg–Engle–Granger–Yoo de rădăcină unitară sezonieră', None),
    'HQ': ('Hannan–Quinn (information criterion)', 'en', 'criteriul informațional Hannan–Quinn', None),
    'INS': ('Institutul Național de Statistică', 'ro', None, 'the National Institute of Statistics (Romania)'),
    'IRF': ('Impulse Response Function', 'en', 'funcția de răspuns la impuls', None),
    'KPSS': ('Kwiatkowski–Phillips–Schmidt–Shin (test)', 'en', 'testul de staționaritate Kwiatkowski–Phillips–Schmidt–Shin', None),
    'LPPL': ('Log-Periodic Power Law', 'en', 'legea de putere log-periodică', None),
    'LPPLS': ('Log-Periodic Power Law Singularity (model)', 'en', 'modelul singularității cu lege de putere log-periodică', None),
    'MAE': ('Mean Absolute Error', 'en', 'eroarea absolută medie', None),
    'MAPE': ('Mean Absolute Percentage Error', 'en', 'eroarea procentuală absolută medie', None),
    'MASE': ('Mean Absolute Scaled Error', 'en', 'eroarea absolută medie scalată', None),
    'MGARCH': ('Multivariate GARCH', 'en', 'GARCH multivariat', None),
    'MSE': ('Mean Squared Error', 'en', 'eroarea pătratică medie', None),
    'PACF': ('Partial AutoCorrelation Function', 'en', 'funcția de autocorelație parțială', None),
    'PIB': ('Produsul intern brut', 'ro', None, 'gross domestic product'),
    'PP': ('Phillips–Perron (test)', 'en', 'testul Phillips–Perron de rădăcină unitară', None),
    'RNN': ('Recurrent Neural Network', 'en', 'rețea neuronală recurentă', None),
    'SARIMA': ('Seasonal ARIMA (model)', 'en', 'model ARIMA sezonier', None),
    'SES': ('Simple Exponential Smoothing', 'en', 'netezire exponențială simplă', None),
    'sMAPE': ('symmetric Mean Absolute Percentage Error', 'en', 'eroarea procentuală absolută medie simetrică', None),
    'STL': ('Seasonal and Trend decomposition using Loess', 'en', 'descompunerea în sezonalitate și trend cu Loess', None),
    'SVAR': ('Structural Vector AutoRegression', 'en', 'model vector autoregresiv structural', None),
    'TBATS': ('Trigonometric seasonality, Box–Cox, ARMA errors, Trend, Seasonal components (model)', 'en', 'model cu sezonalitate trigonometrică, transformare Box–Cox, erori ARMA, trend și componente sezoniere', None),
    'VECM': ('Vector Error Correction Model', 'en', 'model vectorial cu corecția erorii', None),
    'WN': ('White Noise', 'en', 'zgomot alb', None),
    # --- finante si evaluarea activelor
    'AMH': ('Adaptive Markets Hypothesis', 'en', 'ipoteza piețelor adaptive', None),
    'APT': ('Arbitrage Pricing Theory', 'en', 'teoria evaluării prin arbitraj', None),
    'BAB': ('Betting Against Beta', 'en', 'strategia „pariu împotriva lui beta”', None),
    'CAGR': ('Compound Annual Growth Rate', 'en', 'rata anuală compusă de creștere', None),
    'CAPM': ('Capital Asset Pricing Model', 'en', 'modelul de evaluare a activelor financiare', None),
    'CAR': ('Cumulative Abnormal Return', 'en', 'randamentul anormal cumulat', None),
    'CMA': ('Conservative Minus Aggressive (investment factor)', 'en', 'factorul investiții: firme conservatoare minus agresive', None),
    'CML': ('Capital Market Line', 'en', 'dreapta pieței de capital', None),
    'EMH': ('Efficient Market Hypothesis', 'en', 'ipoteza pieței eficiente', None),
    'ES': ('Expected Shortfall', 'en', 'pierderea așteptată în coadă', None),
    'FF3': ('Fama–French three-factor model', 'en', 'modelul Fama–French cu trei factori', None),
    'FF5': ('Fama–French five-factor model', 'en', 'modelul Fama–French cu cinci factori', None),
    'HML': ('High Minus Low (value factor)', 'en', 'factorul valoare: B/M mare minus mic', None),
    'IPCA': ('Instrumented Principal Component Analysis', 'en', 'analiza componentelor principale instrumentată', None),
    'MDD': ('Maximum DrawDown', 'en', 'drawdown maxim', None),
    'MKT': ('MarKeT factor (market excess return)', 'en', 'factorul piață (randamentul în exces al pieței)', None),
    'MOM': ('MOMentum factor', 'en', 'factorul momentum', None),
    'OHLC': ('Open, High, Low, Close', 'en', 'deschidere, maxim, minim, închidere', None),
    'RF': ('Risk-Free rate (Fama–French data) / Random Forest (machine learning)', 'en', 'rata fără risc (datele Fama–French) / pădure aleatoare (machine learning)', None),
    'RMW': ('Robust Minus Weak (profitability factor)', 'en', 'factorul profitabilitate: firme robuste minus slabe', None),
    'ROE': ('Return On Equity', 'en', 'rentabilitatea capitalului propriu', None),
    'SDF': ('Stochastic Discount Factor', 'en', 'factorul stochastic de actualizare', None),
    'SMB': ('Small Minus Big (size factor)', 'en', 'factorul mărime: firme mici minus mari', None),
    'SML': ('Security Market Line', 'en', 'dreapta pieței titlurilor', None),
    'SR': ('Sharpe Ratio', 'en', 'raportul Sharpe', None),
    'TOM': ('Turn Of the Month', 'en', 'schimbarea lunii', None),
    'TSMOM': ('Time-Series MOMentum', 'en', 'momentum în serie de timp', None),
    'UMD': ('Up Minus Down (momentum factor)', 'en', 'factorul momentum: cîștigători minus perdanți', None),
    'VIX': ('CBOE Volatility IndeX', 'en', 'indicele de volatilitate CBOE', None),
    # --- machine learning
    'AI': ('Artificial Intelligence', 'en', 'inteligență artificială', None),
    'AUC': ('Area Under the (ROC) Curve', 'en', 'aria de sub curba ROC', None),
    'CPCV': ('Combinatorial Purged Cross-Validation', 'en', 'validare încrucișată combinatorie cu purjare', None),
    'CSCV': ('Combinatorially Symmetric Cross-Validation', 'en', 'validare încrucișată combinatorie simetrică', None),
    'CV': ('Cross-Validation', 'en', 'validare încrucișată', None),
    'DSR': ('Deflated Sharpe Ratio', 'en', 'raportul Sharpe deflatat', None),
    'FFD': ('Fixed-width window Fractional Differentiation', 'en', 'diferențiere fracționară cu fereastră fixă', None),
    'FN': ('False Negative', 'en', 'fals negativ', None),
    'GAN': ('Generative Adversarial Network', 'en', 'rețea generativă adversarială', None),
    'GB': ('Gradient Boosting', 'en', 'boosting pe gradient', None),
    'GBM': ('Geometric Brownian Motion', 'en', 'mișcarea browniană geometrică', None),
    'GRU': ('Gated Recurrent Unit', 'en', 'unitate recurentă cu porți', None),
    'IS': ('In-Sample', 'en', 'în eșantion', None),
    'LASSO': ('Least Absolute Shrinkage and Selection Operator', 'en', 'regresie penalizată L1 cu selecția variabilelor', None),
    'LLM': ('Large Language Model', 'en', 'model lingvistic de mari dimensiuni', None),
    'LSTM': ('Long Short-Term Memory (network)', 'en', 'rețea cu memorie pe termen lung și scurt', None),
    'MDA': ('Mean Decrease Accuracy', 'en', 'scăderea medie a acurateței (importanța prin permutare)', None),
    'MDI': ('Mean Decrease Impurity', 'en', 'scăderea medie a impurității', None),
    'ML': ('Machine Learning', 'en', 'învățare automată', None),
    'MLP': ('MultiLayer Perceptron', 'en', 'perceptron multistrat', None),
    'OOB': ('Out-Of-Bag (error)', 'en', 'eroarea pe observațiile din afara eșantionului bootstrap', None),
    'OOS': ('Out-Of-Sample', 'en', 'în afara eșantionului', None),
    'PAC': ('Probably Approximately Correct (learning)', 'en', 'învățare probabil aproximativ corectă', None),
    'PBO': ('Probability of Backtest Overfitting', 'en', 'probabilitatea de supraajustare a backtest-ului', None),
    'PSR': ('Probabilistic Sharpe Ratio', 'en', 'raportul Sharpe probabilistic', None),
    'RL': ('Reinforcement Learning', 'en', 'învățare prin recompensă', None),
    'ROC': ('Receiver Operating Characteristic (curve)', 'en', 'curba caracteristică de operare', None),
    'RSI': ('Relative Strength Index', 'en', 'indicele puterii relative', None),
    'SHAP': ('SHapley Additive exPlanations', 'en', 'explicații aditive Shapley', None),
    'TN': ('True Negative', 'en', 'adevărat negativ', None),
    'TP': ('True Positive', 'en', 'adevărat pozitiv', None),
    'WF': ('Walk-Forward (validation)', 'en', 'validare progresivă în timp', None),
    'XAI': ('eXplainable Artificial Intelligence', 'en', 'inteligență artificială explicabilă', None),
    # --- piete, institutii, instrumente
    'AMM': ('Automated Market Maker', 'en', 'formator de piață automat', None),
    'AP': ('Authorised Participant', 'en', 'participant autorizat', None),
    'API': ('Application Programming Interface', 'en', 'interfață de programare a aplicațiilor', None),
    'ASE': ('Academia de Studii Economice din București', 'ro', None, 'the Bucharest University of Economic Studies'),
    'BET': ('Bucharest Exchange Trading (index)', 'en', 'indicele de referință al Bursei de Valori București', None),
    'BET-FI': ('BET Financial Investment companies index', 'en', 'indicele BVB al societăților de investiții financiare', None),
    'BET-TR': ('BET Total Return (index)', 'en', 'indicele BET cu dividendele reinvestite', None),
    'BIS': ('Bank for International Settlements', 'en', 'Banca Reglementelor Internaționale', None),
    'BIST': ('Borsa İstanbul (BIST 100 index)', 'tr', 'Bursa din Istanbul (indicele BIST 100)', 'the Istanbul Stock Exchange (BIST 100 index)'),
    'BNR': ('Banca Națională a României', 'ro', None, 'the National Bank of Romania'),
    'BUX': ('Budapesti Értéktőzsde index', 'hu', 'indicele Bursei din Budapesta', 'the Budapest Stock Exchange index'),
    'BVB': ('Bursa de Valori București', 'ro', None, 'the Bucharest Stock Exchange'),
    'CBOE': ('Chicago Board Options Exchange', 'en', 'bursa de opțiuni din Chicago', None),
    'CCP': ('Central CounterParty', 'en', 'contraparte centrală', None),
    'CFTC': ('Commodity Futures Trading Commission', 'en', 'Comisia americană pentru tranzacționarea contractelor futures pe mărfuri', None),
    'CME': ('Chicago Mercantile Exchange', 'en', 'Bursa de mărfuri din Chicago', None),
    'COVID-19': ('COronaVIrus Disease 2019', 'en', 'boala provocată de coronavirus, 2019', None),
    'CRIX': ('CRypto IndeX', 'en', 'indicele pieței cripto', None),
    'EBA': ('European Banking Authority', 'en', 'Autoritatea Bancară Europeană', None),
    'ESMA': ('European Securities and Markets Authority', 'en', 'Autoritatea Europeană pentru Valori Mobiliare și Piețe', None),
    'ETF': ('Exchange-Traded Fund', 'en', 'fond tranzacționat la bursă', None),
    'EODHD': ('EOD Historical Data (market-data provider)', 'en', 'furnizor de date de piață', None),
    'WTI': ('West Texas Intermediate (crude oil benchmark)', 'en', 'țițeiul de referință West Texas Intermediate', None),
    'NYMEX': ('New York Mercantile Exchange', 'en', 'bursa de mărfuri din New York', None),
    'COMEX': ('Commodity Exchange (metals futures, CME Group)', 'en', 'bursa de contracte futures pe metale a CME Group', None),
    'BCE': ('Banca Centrală Europeană', 'ro', None, 'European Central Bank'),
    'ISO': ('International Organization for Standardization', 'en', 'Organizația Internațională de Standardizare', None),
    'ETP': ('Exchange-Traded Product', 'en', 'produs tranzacționat la bursă', None),
    'EU': ('European Union', 'en', 'Uniunea Europeană', None),
    'UE': ('Uniunea Europeană', 'ro', None, 'the European Union'),
    'FRED': ('Federal Reserve Economic Data', 'en', 'baza de date economice a Rezervei Federale din St. Louis', None),
    'FTSE': ('Financial Times Stock Exchange (FTSE Russell, index provider)', 'en', 'furnizorul de indici FTSE Russell', None),
    'FX': ('Foreign eXchange', 'en', 'piața valutară', None),
    'GENIUS': ('Guiding and Establishing National Innovation for U.S. Stablecoins (Act)', 'en', 'legea americană privind stablecoin-urile', None),
    'GEO': ('Government Emergency Ordinance', 'en', 'ordonanță de urgență a Guvernului (OUG)', None),
    'OUG': ('Ordonanță de Urgență a Guvernului', 'ro', None, 'government emergency ordinance'),
    'HFT': ('High-Frequency Trading', 'en', 'tranzacționare de înaltă frecvență', None),
    'HK': ('Hong Kong', 'en', 'Hong Kong', None),
    'IPC': ('Indicele prețurilor de consum', 'ro', None, 'the consumer price index (CPI)'),
    'IPO': ('Initial Public Offering', 'en', 'ofertă publică inițială', None),
    'MIT': ('Massachusetts Institute of Technology', 'en', 'Institutul de Tehnologie din Massachusetts', None),
    'MSCA': ('Marie Skłodowska-Curie Actions', 'en', 'programul european Acțiunile Marie Skłodowska-Curie', None),
    'MTF': ('Multilateral Trading Facility', 'en', 'sistem multilateral de tranzacționare', None),
    'NAV': ('Net Asset Value', 'en', 'valoarea activului net', None),
    'NYSE': ('New York Stock Exchange', 'en', 'Bursa din New York', None),
    'OMV': ('Österreichische Mineralölverwaltung', 'de', 'Administrația austriacă a uleiurilor minerale, grupul OMV', 'Austrian Mineral Oil Administration (OMV group)'),
    'OTC': ('Over-The-Counter', 'en', 'piață extrabursieră', None),
    'PX': ('Prague Stock Exchange index (index Burzy cenných papírů Praha)', 'cs', 'indicele Bursei din Praga', None),
    'ROL': ('Romanian old leu (ISO 4217 code, until 2005)', 'en', 'leul vechi (cod ISO 4217, pînă în 2005)', None),
    'RWA': ('Real-World Assets', 'en', 'active din economia reală tokenizate', None),
    'SEC': ('Securities and Exchange Commission', 'en', 'Comisia americană pentru valori mobiliare', None),
    'SIF': ('Societate de Investiții Financiare', 'ro', None, 'financial investment company'),
    'SPDR': ('Standard & Poor’s Depositary Receipts', 'en', 'certificate de depozit Standard & Poor’s (familia de ETF-uri SPDR)', None),
    'SUA': ('Statele Unite ale Americii', 'ro', None, 'the United States of America'),
    'US': ('United States', 'en', 'Statele Unite ale Americii', None),
    'UDR': ('Uzinele și Domeniile Reșița', 'ro', None, 'the Reșița Works and Domains'),
    'UTC': ('Coordinated Universal Time (Temps Universel Coordonné)', 'en', 'timpul universal coordonat', None),
    'DAX': ('Deutscher Aktienindex', 'de', 'indicele principal al Bursei din Frankfurt', 'the German stock index of the Frankfurt Stock Exchange'),
    'SFM': ('Statistics of Financial Markets', 'en', 'Statistica piețelor financiare, cursul de licență', None),
    'SPF': ('Survey of Professional Forecasters', 'en', 'ancheta specialiștilor în prognoză (Survey of Professional Forecasters)', None),
    'ATS': ('Advanced Time Series Analysis and Forecasting', 'en', 'Analiza avansată a seriilor de timp și previziune, cursul de master', None),
    'TSA': ('Time Series Analysis', 'en', 'Serii de timp, cursul de licență', None),
    'ASDS': ('Statistică aplicată și data science', 'ro', None, "the Master's programme Applied Statistics and Data Science"),
    'MFM': ('Modelling Financial Markets', 'en', 'Modelarea piețelor financiare, cursul de master', None),
    'CSIE': ('Facultatea de Cibernetică, Statistică și Informatică Economică', 'ro', None, 'the Faculty of Cybernetics, Statistics and Economic Informatics'),
    'WIG20': ('Warszawski Indeks Giełdowy 20', 'pl', 'indicele celor mai mari 20 de companii de la Bursa din Varșovia', 'the Warsaw Stock Exchange index of the 20 largest companies'),
}
IGNORE = set("""CC CC0 BY BY-SA EDHAC QK VQ NDSR RS RISK SA AG SUM SIGKDD TB3MS DE""".split())   # licente, credite, simboluri matematice


OVERRIDE = {  # acelasi acronim, sens diferit in capitole diferite: (capitol, acronim) -> tuplu
    ('13', 'RF'): ('Random Forest', 'en', 'pădure aleatoare', None),
}


# Acronime specifice capitolelor: latex/acronyms_extra/chN.py cu dictionarele EXTRA (acelasi format ca A)
# si, optional, OVERRIDE_CH (acronim -> tuplu, doar pentru capitolul N). Fiecare capitol isi editeaza fisierul lui.
import glob as _glob
import importlib.util as _ilu
for _f in sorted(_glob.glob(os.path.join(HERE, 'acronyms_extra', 'ch*.py'))):
    _spec = _ilu.spec_from_file_location(os.path.basename(_f)[:-3], _f)
    _m = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_m)
    _n = os.path.basename(_f)[2:-3]
    for _k, _v in getattr(_m, 'EXTRA', {}).items():
        A.setdefault(_k, _v)
    for _k, _v in getattr(_m, 'OVERRIDE_CH', {}).items():
        OVERRIDE[(_n, _k)] = _v


def entry(key, lang, chap=None):
    origin, olang, ro, en = (OVERRIDE[(chap, key)] if (chap, key) in OVERRIDE else A[key])
    if lang == 'ro':
        tr = ro if olang != 'ro' else None
    else:
        tr = en if olang != 'en' else None
    tex = origin if not tr else (f'{origin} — {tr}' if origin.endswith(')') else f'{origin} ({tr})')   # no doubled parentheses
    return r'\item \textbf{' + key + '}: ' + tex.replace('&', r'\&')


sys.path.insert(0, HERE)


def found_in(tex_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('scan', os.path.join(HERE, '_acr_scan.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return [a for a in m.scan(tex_path) if a not in IGNORE]


def glossary_frames(keys, lang, per_col=13, chap=None):
    title = 'Acronime folosite în acest material' if lang == 'ro' else 'Acronyms used in this material'
    keys = sorted(keys, key=lambda k: k.upper())
    chunks = [keys[i:i + 2 * per_col] for i in range(0, len(keys), 2 * per_col)]
    out = ['% BEGIN-ACRONYMS (generat de latex/acronyms.py; nu editati manual)']
    for n, ch in enumerate(chunks, 1):
        t = title + (f' ({n}/{len(chunks)})' if len(chunks) > 1 else '')
        left, right = ch[:per_col], ch[per_col:]
        out.append(r'\begin{frame}{' + t + '}')
        out.append(r'\setbeamertemplate{itemize/enumerate body begin}{\tiny}')
        out.append(r'\begin{columns}[T]')
        for col in (left, right):
            out.append(r'\begin{column}{0.49\textwidth}')
            if col:
                out.append(r'\begin{itemize}\setlength{\itemsep}{0pt}')
                out += ['    ' + entry(k, lang, chap) for k in col]
                out.append(r'\end{itemize}')
            out.append(r'\end{column}')
        out.append(r'\end{columns}')
        out.append(r'\end{frame}')
    out.append('% END-ACRONYMS')
    return '\n'.join(out) + '\n'


OLD_GLOSSARY = re.compile(r'\\begin\{frame\}(\[[^\]]*\])?\{(Glossary of Acronyms|Glosar de acronime)[^}]*\}.*?\\end\{frame\}\n?', re.S)


def process(tex_path, lang):
    s = open(tex_path, encoding='utf-8').read()
    s = re.sub(r'\n*% BEGIN-ACRONYMS.*?% END-ACRONYMS\n+', '\n', s, flags=re.S)
    s = OLD_GLOSSARY.sub('', s)
    open(tex_path, 'w', encoding='utf-8').write(s)
    keys = found_in(tex_path)
    m = re.search(r'(chapter|capitol|seminar)(\d+)_', os.path.basename(tex_path))
    ch = m.group(2) if m else None
    missing = [k for k in keys if k not in A and (ch, k) not in OVERRIDE]
    keys = [k for k in keys if k in A or (ch, k) in OVERRIDE]
    block = glossary_frames(keys, lang, chap=m.group(2) if m else None)
    i = s.find(r'\titlepage')
    j = s.find(r'\end{frame}', i) + len(r'\end{frame}')
    k = s.find('\n}', j)
    pos = k + 2 if 0 <= k - j < 5 else j + 1          # dupa grupul {...} al paginii de titlu
    s = s[:pos] + ('' if s[pos - 1] == '\n' else '\n') + block + '\n' + s[pos:].lstrip('\n')
    open(tex_path, 'w', encoding='utf-8').write(s)
    return keys, missing


def discover_decks(chapters=None):
    """Deck-urile din noul flux (curs + seminar, EN + RO), fara wrapper-ele *_solutions.tex."""
    from ats_chapters import new_decks
    return [(os.path.relpath(p, ROOT), lang) for p, lang, kind, n in new_decks(chapters=chapters)]


if __name__ == '__main__':
    # python3 latex/acronyms.py            -> toate deck-urile
    # python3 latex/acronyms.py 4 5        -> doar capitolele 4 si 5
    for rel, lang in discover_decks(set(sys.argv[1:]) or None):
        keys, missing = process(os.path.join(ROOT, rel), lang)
        print(f'{rel}: {len(keys)} acronyms' + (f'; NOT IN DICTIONARY: {missing}' if missing else ''))
    # legaturile catre Anexa si butoanele de intoarcere (latex/appendix_links.py)
    import subprocess
    subprocess.run([sys.executable, os.path.join(HERE, 'appendix_links.py')] + sys.argv[1:], check=True,
                   stdout=subprocess.DEVNULL)
