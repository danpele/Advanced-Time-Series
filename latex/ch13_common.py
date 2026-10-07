r"""
ch13_common.py -- shared helpers of the Chapter 13 generators (lecture and seminar), ATS
========================================================================================
Bilingual text T(en, ro); numbers from Quantlets/Ch_13/ch13_numbers.json (generate_all_charts.py) and
sem13_results.json (seminar13.py); the clickable citations of Chapter 13 (DOIs checked against Crossref, arXiv
identifiers against the arXiv API, other links with HTTP 200; 6 October 2026).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ats_build import ROOT, Values, n   # noqa: E402,F401

QL = os.path.join(ROOT, 'Quantlets', 'Ch_13')
QLURL = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets/Ch_13'
MONTHS_RO = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie',
             'octombrie', 'noiembrie', 'decembrie']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']


def T(en, ro):
    """Bilingual text; in raw strings a prime may be written as \\' and becomes '."""
    return f'⟦{en}||{ro}⟧'.replace("\\'", "'")


def V2(en, ro):
    """A bilingual value that can sit inside ⟦..||..⟧ text: resolved in the written files by finalize()."""
    return f'⟪{en}¦{ro}⟫'


def finalize(paths):
    """Resolve the ⟪en¦ro⟫ values in the written decks (EN file first, RO file second)."""
    for p, k in zip(paths, (1, 2)):
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'⟪(.*?)¦(.*?)⟫', lambda m: m.group(k), s)
        open(p, 'w', encoding='utf-8').write(s)


def month(s):
    y, m = int(s[:4]), int(s[5:7]) - 1
    return V2(f'{MONTHS_EN[m]} {y}', f'{MONTHS_RO[m]} {y}')


def day(s):
    """'2025-05-09' -> 9 May 2025 / 9 mai 2025."""
    y, m, d = int(s[:4]), int(s[5:7]) - 1, int(s[8:10])
    return V2(f'{d} {MONTHS_EN[m]} {y}', f'{d} {MONTHS_RO[m]} {y}')


def minus_fix(V):
    """Negative numbers: a real minus sign in text and in math mode."""
    for k, v in list(V.items()):
        if isinstance(v, str) and v.startswith('⁅-'):
            V[k] = '⁅\\ensuremath{-}' + v[2:]


def load():
    with open(os.path.join(QL, 'ch13_numbers.json')) as f:
        return json.load(f)


def load_sem():
    with open(os.path.join(QL, 'sem13_results.json')) as f:
        return json.load(f)


def ref(key, url, en, ro=None):
    return f'\\newcommand{{\\ref{key}}}{{\\href{{{url}}}{{{T(en, ro or en)}}}}}\n'


D_ = 'https://doi.org/'
AX = 'https://arxiv.org/abs/'
# key: (doi or url, EN label, RO label, bibliography entry)
R = {
    # ---------------------------------------------------------------- foundation models
    'Aks': (AX + '2410.10393', 'Aksu et al.\\ (2024)', 'Aksu et al.\\ (2024)',
            r'Aksu, T., Woo, G., Liu, J., Liu, X., Liu, C., Savarese, S., Xiong, C., \& Sahoo, D. (2024). GIFT-Eval: A benchmark for general time series forecasting model evaluation. \textit{arXiv:2410.10393}.'),
    'Ans': (AX + '2403.07815', 'Ansari et al.\\ (2024)', 'Ansari et al.\\ (2024)',
            r'Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Shen, H., et al.\ (2024). Chronos: Learning the language of time series. \textit{Transactions on Machine Learning Research}; \textit{arXiv:2403.07815}.'),
    'AnsB': (AX + '2510.15821', 'Ansari et al.\\ (2025)', 'Ansari et al.\\ (2025)',
             r'Ansari, A. F., Shchur, O., Küken, J., Auer, A., Han, B., Mercado, P., et al.\ (2025). Chronos-2: From univariate to universal forecasting. \textit{arXiv:2510.15821}.'),
    'Aue': (AX + '2505.23719', 'Auer et al.\\ (2025)', 'Auer et al.\\ (2025)',
            r'Auer, A., Podest, P., Klotz, D., Böck, S., Klambauer, G., \& Hochreiter, S. (2025). TiRex: Zero-shot forecasting across long and short horizons with enhanced in-context learning. \textit{Advances in Neural Information Processing Systems}; \textit{arXiv:2505.23719}.'),
    'Bom': (AX + '2108.07258', 'Bommasani et al.\\ (2021)', 'Bommasani et al.\\ (2021)',
            r'Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., et al.\ (2021). On the opportunities and risks of foundation models. \textit{arXiv:2108.07258}.'),
    'Bri': (AX + '2607.05291', 'Brini (2026)', 'Brini (2026)',
            r'Brini, A. (2026). Forecasting realized volatility with time series foundation models: A comparison with econometric benchmarks. \textit{arXiv:2607.05291}.'),
    'Coh': (AX + '2505.14766', 'Cohen et al.\\ (2025)', 'Cohen et al.\\ (2025)',
            r'Cohen, B., Khwaja, E., Doubli, Y., Lemaachi, S., Lettieri, C., Masson, C., et al.\ (2025). This time is different: An observability perspective on time series foundation models. \textit{arXiv:2505.14766}.'),
    'Das': (AX + '2310.10688', 'Das et al.\\ (2024)', 'Das et al.\\ (2024)',
            r'Das, A., Kong, W., Sen, R., \& Zhou, Y. (2024). A decoder-only foundation model for time-series forecasting. \textit{Proceedings of the 41st International Conference on Machine Learning (ICML)}; \textit{arXiv:2310.10688}.'),
    'Edw': (AX + '2405.13867', 'Edwards et al.\\ (2024)', 'Edwards et al.\\ (2024)',
            r'Edwards, T. D. P., Alvey, J., Alsing, J., Nguyen, N. H., \& Wandelt, B. D. (2024). Scaling-laws for large time-series models. \textit{arXiv:2405.13867}.'),
    'Gar': (AX + '2310.03589', 'Garza et al.\\ (2023)', 'Garza et al.\\ (2023)',
            r'Garza, A., Challu, C., \& Mergenthaler-Canseco, M. (2023). TimeGPT-1. \textit{arXiv:2310.03589}.'),
    'GarB': (AX + '2603.08707', 'Garza et al.\\ (2026)', 'Garza et al.\\ (2026)',
             r'Garza, A., Rosillo, R., Mendoza-Smith, R., Salinas, D., Williams, A. R., Ashok, A., Goswami, M., et al.\ (2026). Impermanent: A live benchmark for temporal generalization in time series forecasting. \textit{arXiv:2603.08707}.'),
    'Goe': (AX + '2505.11163', 'Goel et al.\\ (2025)', 'Goel et al.\\ (2025)',
            r'Goel, A., Pasricha, P., Magris, M., \& Kanniainen, J. (2025). Foundation time-series AI model for realized volatility forecasting. \textit{arXiv:2505.11163}.'),
    'Gos': (AX + '2402.03885', 'Goswami et al.\\ (2024)', 'Goswami et al.\\ (2024)',
            r'Goswami, M., Szafer, K., Choudhry, A., Cai, Y., Li, S., \& Dubrawski, A. (2024). MOMENT: A family of open time-series foundation models. \textit{Proceedings of the 41st International Conference on Machine Learning (ICML)}; \textit{arXiv:2402.03885}.'),
    'Gru': (AX + '2310.07820', 'Gruver et al.\\ (2023)', 'Gruver et al.\\ (2023)',
            r'Gruver, N., Finzi, M., Qiu, S., \& Wilson, A. G. (2023). Large language models are zero-shot time series forecasters. \textit{Advances in Neural Information Processing Systems 36}; \textit{arXiv:2310.07820}.'),
    'Hof': (AX + '2203.15556', 'Hoffmann et al.\\ (2022)', 'Hoffmann et al.\\ (2022)',
            r'Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., et al.\ (2022). Training compute-optimal large language models. \textit{arXiv:2203.15556}.'),
    'Jin': (AX + '2310.01728', 'Jin et al.\\ (2024)', 'Jin et al.\\ (2024)',
            r'Jin, M., Wang, S., Ma, L., Chu, Z., Zhang, J. Y., Shi, X., et al.\ (2024). Time-LLM: Time series forecasting by reprogramming large language models. \textit{International Conference on Learning Representations (ICLR)}; \textit{arXiv:2310.01728}.'),
    'Kap': (AX + '2001.08361', 'Kaplan et al.\\ (2020)', 'Kaplan et al.\\ (2020)',
            r'Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., et al.\ (2020). Scaling laws for neural language models. \textit{arXiv:2001.08361}.'),
    'Liu': (AX + '2511.11698', 'Liu et al.\\ (2025)', 'Liu et al.\\ (2025)',
            r'Liu, C., Aksu, T., Liu, J., Liu, X., Yan, H., Pham, Q., Savarese, S., et al.\ (2025). Moirai 2.0: When less is more for time series forecasting. \textit{arXiv:2511.11698}.'),
    'LTZ': (AX + '2504.14765', 'Lopez-Lira, Tang and Zhu (2025)', 'Lopez-Lira, Tang și Zhu (2025)',
            r"Lopez-Lira, A., Tang, Y., \& Zhu, M. (2025). The memorization problem: Can we trust LLMs' economic forecasts? \textit{arXiv:2504.14765}."),
    'Mey': (AX + '2512.20761', 'Meyer et al.\\ (2025)', 'Meyer et al.\\ (2025)',
            r'Meyer, M., Kaltenpoth, S., Albers, H., Zalipski, K., \& Müller, O. (2025). TS-Arena: A live forecast pre-registration platform. \textit{arXiv:2512.20761}.'),
    'Nie': (AX + '2211.14730', 'Nie et al.\\ (2023)', 'Nie et al.\\ (2023)',
            r'Nie, Y., Nguyen, N. H., Sinthong, P., \& Kalagnanam, J. (2023). A time series is worth 64 words: Long-term forecasting with Transformers. \textit{International Conference on Learning Representations (ICLR)}; \textit{arXiv:2211.14730}.'),
    'PE': (AX + '2607.02623', 'Pan and Ezzat (2026)', 'Pan și Ezzat (2026)',
           r'Pan, Z., \& Ezzat, A. A. (2026). Evaluating time series foundation models for electricity price forecasting: Contamination risk, distributional shifts, and covariate dependence. \textit{arXiv:2607.02623}.'),
    'Ras': (AX + '2310.08278', 'Rasul et al.\\ (2023)', 'Rasul et al.\\ (2023)',
            r'Rasul, K., Ashok, A., Williams, A. R., Ghonia, H., Bhagwatkar, R., Khorasani, A., et al.\ (2023). Lag-Llama: Towards foundation models for probabilistic time series forecasting. \textit{arXiv:2310.08278}.'),
    'RNW': (AX + '2511.18578', 'Rahimikia, Ni and Wang (2025)', 'Rahimikia, Ni și Wang (2025)',
            r'Rahimikia, E., Ni, H., \& Wang, W. (2025). Re(Visiting) time series foundation models in finance. \textit{arXiv:2511.18578}.'),
    'Shc': (AX + '2509.26468', 'Shchur et al.\\ (2025)', 'Shchur et al.\\ (2025)',
            r'Shchur, O., Ansari, A. F., Turkmen, C., Stella, L., Erickson, N., Guerron, P., et al.\ (2025). fev-bench: A realistic benchmark for time series forecasting. \textit{arXiv:2509.26468}.'),
    'Shi': (AX + '2405.15124', 'Shi et al.\\ (2024)', 'Shi et al.\\ (2024)',
            r'Shi, J., Ma, Q., Ma, H., \& Li, L. (2024). Scaling law for time series forecasting. \textit{Advances in Neural Information Processing Systems 37}; \textit{arXiv:2405.15124}.'),
    'Tan': (AX + '2406.16964', 'Tan et al.\\ (2024)', 'Tan et al.\\ (2024)',
            r'Tan, M., Merrill, M. A., Gupta, V., Althoff, T., \& Hartvigsen, T. (2024). Are language models actually useful for time series forecasting? \textit{Advances in Neural Information Processing Systems 37}; \textit{arXiv:2406.16964}.'),
    'Vas': (AX + '1706.03762', 'Vaswani et al.\\ (2017)', 'Vaswani et al.\\ (2017)',
            r'Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., \& Polosukhin, I. (2017). Attention is all you need. \textit{Advances in Neural Information Processing Systems 30}; \textit{arXiv:1706.03762}.'),
    'Woo': (AX + '2402.02592', 'Woo et al.\\ (2024)', 'Woo et al.\\ (2024)',
            r'Woo, G., Liu, C., Kumar, A., Xiong, C., Savarese, S., \& Sahoo, D. (2024). Unified training of universal time series forecasting Transformers. \textit{Proceedings of the 41st International Conference on Machine Learning (ICML)}; \textit{arXiv:2402.02592}.'),
    'Yao': (AX + '2410.12360', 'Yao et al.\\ (2025)', 'Yao et al.\\ (2025)',
            r'Yao, Q., Yang, C.-H. H., Jiang, R., Liang, Y., Jin, M., \& Pan, S. (2025). Towards neural scaling laws for time series foundation models. \textit{International Conference on Learning Representations (ICLR)}; \textit{arXiv:2410.12360}.'),
    'Zho': (AX + '2302.11939', 'Zhou et al.\\ (2023)', 'Zhou et al.\\ (2023)',
            r'Zhou, T., Niu, P., Wang, X., Sun, L., \& Jin, R. (2023). One fits all: Power general time series analysis by pretrained LM. \textit{Advances in Neural Information Processing Systems 36}; \textit{arXiv:2302.11939}.'),
    # ---------------------------------------------------------------- forecasting, evaluation, baselines
    'BH': ('10.1111/j.2517-6161.1995.tb02031.x', 'Benjamini and Hochberg (1995)', 'Benjamini și Hochberg (1995)',
           r'Benjamini, Y., \& Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. \textit{Journal of the Royal Statistical Society: Series B}, 57(1), 289--300.'),
    'Bol': ('10.1016/0304-4076(86)90063-1', 'Bollerslev (1986)', 'Bollerslev (1986)',
            r'Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. \textit{Journal of Econometrics}, 31(3), 307--327.'),
    'Chr': ('10.2307/2527341', 'Christoffersen (1998)', 'Christoffersen (1998)',
            r'Christoffersen, P. F. (1998). Evaluating interval forecasts. \textit{International Economic Review}, 39(4), 841--862.'),
    'Cor': ('10.1093/jjfinec/nbp001', 'Corsi (2009)', 'Corsi (2009)',
            r'Corsi, F. (2009). A simple approximate long-memory model of realized volatility. \textit{Journal of Financial Econometrics}, 7(2), 174--196.'),
    'Dem': ('https://jmlr.org/papers/v7/demsar06a.html', 'Demšar (2006)', 'Demšar (2006)',
            r'Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. \textit{Journal of Machine Learning Research}, 7, 1--30.'),
    'DM': ('10.1080/07350015.1995.10524599', 'Diebold and Mariano (1995)', 'Diebold și Mariano (1995)',
           r'Diebold, F. X., \& Mariano, R. S. (1995). Comparing predictive accuracy. \textit{Journal of Business \& Economic Statistics}, 13(3), 253--263.'),
    'EM': ('10.1198/073500104000000370', 'Engle and Manganelli (2004)', 'Engle și Manganelli (2004)',
           r'Engle, R. F., \& Manganelli, S. (2004). CAViaR: Conditional autoregressive value at risk by regression quantiles. \textit{Journal of Business \& Economic Statistics}, 22(4), 367--381.'),
    'FW': ('10.1145/5666.5673', 'Fleming and Wallace (1986)', 'Fleming și Wallace (1986)',
           r'Fleming, P. J., \& Wallace, J. J. (1986). How not to lie with statistics: The correct way to summarize benchmark results. \textit{Communications of the ACM}, 29(3), 218--221.'),
    'GR': ('10.1198/016214506000001437', 'Gneiting and Raftery (2007)', 'Gneiting și Raftery (2007)',
           r'Gneiting, T., \& Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. \textit{Journal of the American Statistical Association}, 102(477), 359--378.'),
    'GW': ('10.1111/j.1468-0262.2006.00718.x', 'Giacomini and White (2006)', 'Giacomini și White (2006)',
           r'Giacomini, R., \& White, H. (2006). Tests of conditional predictive ability. \textit{Econometrica}, 74(6), 1545--1578.'),
    'HAB': ('10.1007/s10618-022-00894-5', 'Hewamalage, Ackermann and Bergmeir (2023)', 'Hewamalage, Ackermann și Bergmeir (2023)',
            r'Hewamalage, H., Ackermann, K., \& Bergmeir, C. (2023). Forecast evaluation for data scientists: Common pitfalls and best practices. \textit{Data Mining and Knowledge Discovery}, 37, 788--832.'),
    'HLN': ('10.1016/S0169-2070(96)00719-4', 'Harvey, Leybourne and Newbold (1997)', 'Harvey, Leybourne și Newbold (1997)',
            r'Harvey, D., Leybourne, S., \& Newbold, P. (1997). Testing the equality of prediction mean squared errors. \textit{International Journal of Forecasting}, 13(2), 281--291.'),
    'HLNa': ('10.3982/ECTA5771', 'Hansen, Lunde and Nason (2011)', 'Hansen, Lunde și Nason (2011)',
             r'Hansen, P. R., Lunde, A., \& Nason, J. M. (2011). The model confidence set. \textit{Econometrica}, 79(2), 453--497.'),
    'HF': ('10.1016/j.ijforecast.2015.11.011', 'Hong and Fan (2016)', 'Hong și Fan (2016)',
           r'Hong, T., \& Fan, S. (2016). Probabilistic electric load forecasting: A tutorial review. \textit{International Journal of Forecasting}, 32(3), 914--938.'),
    'HK': ('10.1016/j.ijforecast.2006.03.001', 'Hyndman and Koehler (2006)', 'Hyndman și Koehler (2006)',
           r'Hyndman, R. J., \& Koehler, A. B. (2006). Another look at measures of forecast accuracy. \textit{International Journal of Forecasting}, 22(4), 679--688.'),
    'HKSG': ('10.1016/S0169-2070(01)00110-8', 'Hyndman et al.\\ (2002)', 'Hyndman et al.\\ (2002)',
             r'Hyndman, R. J., Koehler, A. B., Snyder, R. D., \& Grose, S. (2002). A state space framework for automatic forecasting using exponential smoothing methods. \textit{International Journal of Forecasting}, 18(3), 439--454.'),
    'Hol': ('https://www.jstor.org/stable/4615733', 'Holm (1979)', 'Holm (1979)',
            r'Holm, S. (1979). A simple sequentially rejective multiple test procedure. \textit{Scandinavian Journal of Statistics}, 6(2), 65--70.'),
    'Kup': ('10.3905/jod.1995.407942', 'Kupiec (1995)', 'Kupiec (1995)',
            r'Kupiec, P. H. (1995). Techniques for verifying the accuracy of risk measurement models. \textit{The Journal of Derivatives}, 3(2), 73--84.'),
    'Lim': ('10.1016/j.ijforecast.2021.03.012', 'Lim et al.\\ (2021)', 'Lim et al.\\ (2021)',
            r'Lim, B., Arık, S. Ö., Loeff, N., \& Pfister, T. (2021). Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. \textit{International Journal of Forecasting}, 37(4), 1748--1764.'),
    'Mak': ('10.1016/j.ijforecast.2021.11.013', 'Makridakis, Spiliotis and Assimakopoulos (2022)', 'Makridakis, Spiliotis și Assimakopoulos (2022)',
            r'Makridakis, S., Spiliotis, E., \& Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. \textit{International Journal of Forecasting}, 38(4), 1346--1364.'),
    'OMI': ('https://web.archive.org/web/20220301022212/https://realized.oxford-man.ox.ac.uk/', 'Heber et al.\\ (2009)', 'Heber et al.\\ (2009)',
            r"Heber, G., Lunde, A., Shephard, N., \& Sheppard, K. (2009). \textit{Oxford-Man Institute's realized library}, version 0.3. Oxford-Man Institute, University of Oxford."),
    'Ore': (AX + '1905.10437', 'Oreshkin et al.\\ (2020)', 'Oreshkin et al.\\ (2020)',
            r'Oreshkin, B. N., Carpov, D., Chapados, N., \& Bengio, Y. (2020). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. \textit{International Conference on Learning Representations (ICLR)}; \textit{arXiv:1905.10437}.'),
    'Pat': ('10.1016/j.jeconom.2010.03.034', 'Patton (2011)', 'Patton (2011)',
            r'Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. \textit{Journal of Econometrics}, 160(1), 246--256.'),
    'Pet': ('10.1016/j.ijforecast.2021.11.001', 'Petropoulos et al.\\ (2022)', 'Petropoulos et al.\\ (2022)',
            r'Petropoulos, F., Apiletti, D., Assimakopoulos, V., Babai, M. Z., et al.\ (2022). Forecasting: Theory and practice. \textit{International Journal of Forecasting}, 38(3), 705--871.'),
    'Sal': ('10.1016/j.ijforecast.2019.07.001', 'Salinas et al.\\ (2020)', 'Salinas et al.\\ (2020)',
            r'Salinas, D., Flunkert, V., Gasthaus, J., \& Januschowski, T. (2020). DeepAR: Probabilistic forecasting with autoregressive recurrent networks. \textit{International Journal of Forecasting}, 36(3), 1181--1191.'),
    'Zen': ('10.1609/aaai.v37i9.26317', 'Zeng et al.\\ (2023)', 'Zeng et al.\\ (2023)',
            r'Zeng, A., Chen, M., Zhang, L., \& Xu, Q. (2023). Are Transformers effective for time series forecasting? \textit{Proceedings of the AAAI Conference on Artificial Intelligence}, 37(9), 11121--11128.'),
    'ZW': ('10.1016/j.eneco.2017.12.016', 'Ziel and Weron (2018)', 'Ziel și Weron (2018)',
           r'Ziel, F., \& Weron, R. (2018). Day-ahead electricity price forecasting with high-dimensional structures: Univariate vs.\ multivariate modeling frameworks. \textit{Energy Economics}, 70, 396--420.'),
    # ---------------------------------------------------------------- conformal prediction
    'AB': ('10.1561/2200000101', 'Angelopoulos and Bates (2023)', 'Angelopoulos și Bates (2023)',
           r'Angelopoulos, A. N., \& Bates, S. (2023). Conformal prediction: A gentle introduction. \textit{Foundations and Trends in Machine Learning}, 16(4), 494--591.'),
    'ACT': (AX + '2307.16895', 'Angelopoulos, Candès and Tibshirani (2023)', 'Angelopoulos, Candès și Tibshirani (2023)',
            r'Angelopoulos, A. N., Candès, E. J., \& Tibshirani, R. J. (2023). Conformal PID control for time series prediction. \textit{Advances in Neural Information Processing Systems 36}; \textit{arXiv:2307.16895}.'),
    'Bar': ('10.1214/23-AOS2276', 'Barber et al.\\ (2023)', 'Barber et al.\\ (2023)',
            r'Barber, R. F., Candès, E. J., Ramdas, A., \& Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. \textit{The Annals of Statistics}, 51(2), 816--845.'),
    'BarB': ('10.1093/imaiai/iaaa017', 'Foygel Barber et al.\\ (2021)', 'Foygel Barber et al.\\ (2021)',
             r'Foygel Barber, R., Candès, E. J., Ramdas, A., \& Tibshirani, R. J. (2021). The limits of distribution-free conditional predictive inference. \textit{Information and Inference: A Journal of the IMA}, 10(2), 455--482.'),
    'CWZ': (AX + '1802.06300', 'Chernozhukov, Wüthrich and Zhu (2018)', 'Chernozhukov, Wüthrich și Zhu (2018)',
            r'Chernozhukov, V., Wüthrich, K., \& Zhu, Y. (2018). Exact and robust conformal inference methods for predictive machine learning with dependent data. \textit{Proceedings of the 31st Conference on Learning Theory (COLT)}; \textit{arXiv:1802.06300}.'),
    'GC': (AX + '2106.00170', 'Gibbs and Candès (2021)', 'Gibbs și Candès (2021)',
           r'Gibbs, I., \& Candès, E. (2021). Adaptive conformal inference under distribution shift. \textit{Advances in Neural Information Processing Systems 34}; \textit{arXiv:2106.00170}.'),
    'GCb': ('https://jmlr.org/papers/v25/22-1218.html', 'Gibbs and Candès (2024)', 'Gibbs și Candès (2024)',
            r'Gibbs, I., \& Candès, E. J. (2024). Conformal inference for online prediction with arbitrary distribution shifts. \textit{Journal of Machine Learning Research}, 25(162), 1--36.'),
    'KB': ('10.2307/1913643', 'Koenker and Bassett (1978)', 'Koenker și Bassett (1978)',
           r'Koenker, R., \& Bassett, G. (1978). Regression quantiles. \textit{Econometrica}, 46(1), 33--50.'),
    'Lei': ('10.1080/01621459.2017.1307116', 'Lei et al.\\ (2018)', 'Lei et al.\\ (2018)',
            r"Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., \& Wasserman, L. (2018). Distribution-free predictive inference for regression. \textit{Journal of the American Statistical Association}, 113(523), 1094--1111."),
    'LW': ('10.1111/rssb.12021', 'Lei and Wasserman (2014)', 'Lei și Wasserman (2014)',
           r'Lei, J., \& Wasserman, L. (2014). Distribution-free prediction bands for non-parametric regression. \textit{Journal of the Royal Statistical Society: Series B}, 76(1), 71--96.'),
    'Oli': (AX + '2203.15885', 'Oliveira et al.\\ (2024)', 'Oliveira et al.\\ (2024)',
            r'Oliveira, R. I., Orenstein, P., Ramos, T., \& Romano, J. V. (2024). Split conformal prediction and non-exchangeable data. \textit{Journal of Machine Learning Research}, 25; \textit{arXiv:2203.15885}.'),
    'Pap': ('10.1007/3-540-36755-1_29', 'Papadopoulos et al.\\ (2002)', 'Papadopoulos et al.\\ (2002)',
            r'Papadopoulos, H., Proedrou, K., Vovk, V., \& Gammerman, A. (2002). Inductive confidence machines for regression. In \textit{Machine Learning: ECML 2002}, Lecture Notes in Computer Science 2430, 345--356. Springer.'),
    'RPC': (AX + '1905.03222', 'Romano, Patterson and Candès (2019)', 'Romano, Patterson și Candès (2019)',
            r'Romano, Y., Patterson, E., \& Candès, E. (2019). Conformalized quantile regression. \textit{Advances in Neural Information Processing Systems 32}; \textit{arXiv:1905.03222}.'),
    'TBCR': (AX + '1904.06019', 'Tibshirani et al.\\ (2019)', 'Tibshirani et al.\\ (2019)',
             r'Tibshirani, R. J., Barber, R. F., Candès, E. J., \& Ramdas, A. (2019). Conformal prediction under covariate shift. \textit{Advances in Neural Information Processing Systems 32}; \textit{arXiv:1904.06019}.'),
    'VGS': ('10.1007/b106715', 'Vovk, Gammerman and Shafer (2005)', 'Vovk, Gammerman și Shafer (2005)',
            r'Vovk, V., Gammerman, A., \& Shafer, G. (2005). \textit{Algorithmic Learning in a Random World}. Springer.'),
    'VGSb': ('10.1007/978-3-031-06649-8', 'Vovk, Gammerman and Shafer (2022)', 'Vovk, Gammerman și Shafer (2022)',
             r'Vovk, V., Gammerman, A., \& Shafer, G. (2022). \textit{Algorithmic Learning in a Random World} (2nd ed.). Springer.'),
    'Vov': ('https://proceedings.mlr.press/v25/vovk12.html', 'Vovk (2012)', 'Vovk (2012)',
            r'Vovk, V. (2012). Conditional validity of inductive conformal predictors. \textit{Proceedings of the Asian Conference on Machine Learning}, PMLR 25, 475--490.'),
    'Win': ('10.1080/01621459.1972.10481224', 'Winkler (1972)', 'Winkler (1972)',
            r'Winkler, R. L. (1972). A decision-theoretic approach to interval estimation. \textit{Journal of the American Statistical Association}, 67(337), 187--191.'),
    'XX': ('https://proceedings.mlr.press/v139/xu21h.html', 'Xu and Xie (2021)', 'Xu și Xie (2021)',
           r'Xu, C., \& Xie, Y. (2021). Conformal prediction interval for dynamic time-series. \textit{Proceedings of the 38th International Conference on Machine Learning (ICML)}, PMLR 139, 11559--11569.'),
    'XXb': ('10.1109/TPAMI.2023.3272339', 'Xu and Xie (2023)', 'Xu și Xie (2023)',
            r'Xu, C., \& Xie, Y. (2023). Conformal prediction for time series. \textit{IEEE Transactions on Pattern Analysis and Machine Intelligence}, 45(10), 11575--11587.'),
    'Zaf': (AX + '2202.07282', 'Zaffran et al.\\ (2022)', 'Zaffran et al.\\ (2022)',
            r'Zaffran, M., Dieuleveut, A., Féron, O., Goude, Y., \& Josse, J. (2022). Adaptive conformal predictions for time series. \textit{Proceedings of the 39th International Conference on Machine Learning (ICML)}; \textit{arXiv:2202.07282}.'),
    # ---------------------------------------------------------------- further reading (instructor's repositories)
    'CO': ('https://github.com/danpele/Conformal_Oracle', 'Pele et al., Conformal\\_Oracle (GitHub)', 'Pele et al., Conformal\\_Oracle (GitHub)',
           r'Pele, D. T., et al. Conformal\_Oracle: conformal VaR recalibration for time series foundation models and classical models. GitHub repository.'),
    'TV': ('https://github.com/danpele/TSFM_VaR_CEE', 'Pele et al., TSFM\\_VaR\\_CEE (GitHub)', 'Pele et al., TSFM\\_VaR\\_CEE (GitHub)',
           r'Pele, D. T., et al. TSFM\_VaR\_CEE: benchmarking time-series foundation models for VaR and ES forecasting in Central and Eastern European markets. GitHub repository.'),
}


def _url(x):
    return x if x.startswith('http') else D_ + x


def _safe(u):
    return u.replace('<', '\\%3C').replace('>', '\\%3E').replace('#', '\\#')


REFS = ''.join(ref(k, _safe(_url(v[0])), v[1], v[2]) for k, v in R.items())


def bib(keys=None):
    """Bibliography entries (alphabetical) with a clickable DOI or URL."""
    out = []
    for k, v in sorted(R.items(), key=lambda kv: re.sub(r'[^a-z]', '', kv[1][3].lower())):
        if keys is not None and k not in keys:
            continue
        u = _safe(_url(v[0]))
        if not v[0].startswith('http'):
            shown = 'doi:' + v[0]
        elif 'arxiv.org' in v[0]:
            shown = 'arXiv:' + v[0].rsplit('/', 1)[1]
        else:
            shown = v[0].split('/')[2].replace('www.', '')
        shown = shown.replace('_', '\\_').replace('<', '\\textless{}').replace('>', '\\textgreater{}').replace('#', '\\#')
        out.append(v[3] + f' \\href{{{u}}}{{{shown}}}')
    return out
