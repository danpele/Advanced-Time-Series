r"""
ats_chapters.py -- registrul capitolelor ATS si schema de nume a fisierelor noi
================================================================================
Titlurile vin din assets/course-data.js (capitolele 0-16). Din ele se deriveaza "slug"-urile fisierelor:

  curs EN       EN/Courses/chapterN_<slug_en>.tex/.pdf
  curs RO       RO/Cursuri/capitolN_<slug_ro>.tex/.pdf
  seminar EN    EN/Seminars/seminarN_<slug_en>.tex/.pdf          (+ seminarN_<slug_en>_solutions.tex, privat)
  seminar RO    RO/Seminarii/seminarN_<slug_ro>_ro.tex/.pdf      (+ seminarN_<slug_ro>_ro_solutions.tex, privat)
  notebook-uri  notebooks/EN/chapterN_lecture_notebook.ipynb, notebooks/EN/chapterN_seminar_notebook.ipynb
  Quantlet-uri  Quantlets/Ch_NN/ATS_chN_<nume>/
  site          https://danpele.github.io/Advanced-Time-Series/<cale>.pdf

Slug = titlul fara diacritice, cu litere mici, fara cuvintele de legatura (and, of, the, si, ...), cuvintele unite
cu "_"; pentru titlurile lungi se foloseste o forma scurta (SHORT). ATS nu are deck-uri vechi: fiecare capitol are
generatoarele lui (latex/build_chapterN.py, latex/build_seminarN.py).

Un deck face parte din noul flux daca exista la calea de mai sus SI contine "\input{../../latex/preamble}"
(is_new_pipeline). Doar aceste deck-uri primesc glosar (acronyms.py) si legaturi intre capitole (appendix_links.py).

Verificare:  python3 latex/ats_chapters.py        (tabelul numelor; avertizeaza daca titlurile din site s-au schimbat)
"""

import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = 'https://danpele.github.io/Advanced-Time-Series/'
REPO = 'https://github.com/danpele/Advanced-Time-Series'
COLAB = 'https://colab.research.google.com/github/danpele/Advanced-Time-Series/blob/main/'

COURSE = {'en': 'Advanced Time Series Analysis and Forecasting', 'ro': 'Analiza avansată a seriilor de timp și previziune'}
PRESET_MARK = r'\input{../../latex/preamble}'

# N -> (titlu EN, titlu RO), ca in assets/course-data.js (capitolul 16: studiu individual)
TITLES = {
    0: ('Refresher and inference for dependent data', 'Recapitulare și inferență pentru date dependente'),
    1: ('Forecast evaluation, scoring rules and combination', 'Evaluarea prognozelor, reguli de scor și combinarea prognozelor'),
    2: ('Structural breaks and nonlinear models', 'Rupturi structurale și modele neliniare'),
    3: ('Structural VAR and local projections', 'Modele VAR structurale și proiecții locale'),
    4: ('Cointegration revisited: VECM, ARDL and panel data', 'Cointegrare: VECM, ARDL și date panel'),
    5: ('Bayesian VAR, factor models and nowcasting', 'Modele VAR bayesiene, modele factoriale și nowcasting'),
    6: ('State space models and Bayesian filtering', 'Modele în spațiul stărilor și filtrare bayesiană'),
    7: ('Regime-switching models', 'Modele cu schimbare de regim'),
    8: ('Advanced volatility modelling: realised measures, HAR and multivariate GARCH', 'Modelarea avansată a volatilității: măsuri realizate, HAR și GARCH multivariat'),
    9: ('VaR, ES and backtesting: elicitability, scoring and model risk', 'VaR, ES și backtesting: elicitabilitate, funcții de scor și riscul de model'),
    10: ('Long memory and rough volatility', 'Memorie lungă și rough volatility'),
    11: ('Spectral and wavelet analysis', 'Analiză spectrală și analiză wavelet'),
    12: ('Machine learning and deep learning for time series', 'Machine learning și deep learning pentru serii de timp'),
    13: ('Foundation models and conformal prediction', 'Foundation models și predicție conformală'),
    14: ('Causal inference for time series', 'Inferență cauzală pentru serii de timp'),
    15: ('Review and project defence', 'Recapitulare și susținerea proiectelor'),
    16: ('Explosive roots and bubbles', 'Rădăcini explozive și bule speculative'),
}
SELF_STUDY = {16}

# forme scurte pentru titlurile lungi (aceleasi cuvinte-cheie ca titlul)
SHORT = {
    0: ('refresher_inference', 'recapitulare_inferenta'),
    1: ('forecast_evaluation', 'evaluarea_prognozelor'),
    4: ('cointegration_vecm_ardl_panel', 'cointegrare_vecm_ardl_panel'),
    5: ('bvar_factor_models_nowcasting', 'bvar_modele_factoriale_nowcasting'),
    8: ('advanced_volatility', 'volatilitate_avansata'),
    9: ('var_es_backtesting', 'var_es_backtesting'),
    12: ('machine_learning_deep_learning', 'machine_learning_deep_learning'),
    13: ('foundation_models_conformal', 'foundation_models_conformal'),
    15: ('review_project_defence', 'recapitulare_proiecte'),
}

STOP = {'cu', 'and', 'of', 'the', 'a', 'an', 'in', 'for', 'si', 'de', 'ale', 'al', 'a', 'in', 'pentru', 'testele',
        'ipoteza', 'hypothesis', 'tests'}


def slugify(title):
    t = title.replace('α', 'alpha ').replace('&', ' ')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    t = t.replace('variance-ratio', 'vr')
    words = [w for w in re.findall(r'[a-z0-9]+', t) if w not in STOP]
    words = ['alfa' if w == 'alpha' and any(x in title for x in 'ăâîșțȘȚ') else w for w in words]
    return '_'.join(words)


def slugs(n):
    if n in SHORT:
        return SHORT[n]
    en, ro = TITLES[n]
    s_ro = slugify(ro)
    if 'α' in ro:
        s_ro = s_ro.replace('alpha', 'alfa')
    return slugify(en), s_ro


def paths(n):
    """Caile relative la radacina depozitului (fara extensie pentru deck-uri)."""
    en, ro = slugs(n)
    return {
        'lecture_en': f'EN/Courses/chapter{n}_{en}',
        'lecture_ro': f'RO/Cursuri/capitol{n}_{ro}',
        'seminar_en': f'EN/Seminars/seminar{n}_{en}',
        'seminar_ro': f'RO/Seminarii/seminar{n}_{ro}_ro',
        'nb_lecture': f'notebooks/EN/chapter{n}_lecture_notebook.ipynb',
        'nb_seminar': f'notebooks/EN/chapter{n}_seminar_notebook.ipynb',
        'quantlets': f'Quantlets/Ch_{n:02d}',
    }


def deck(n, kind, lang):
    """Calea relativa a unui deck (.tex): kind in {'lecture', 'seminar'}, lang in {'en', 'ro'}."""
    return paths(n)[f'{kind}_{lang}'] + '.tex'


def is_new_pipeline(path):
    """True daca fisierul .tex exista si foloseste preambulul comun latex/preamble.tex."""
    if not os.path.exists(path):
        return False
    with open(path, encoding='utf-8') as f:
        return PRESET_MARK in f.read(20000)


def pdf_url(n, kind, lang):
    return SITE + deck(n, kind, lang).replace('.tex', '.pdf')


def new_decks(kinds=('lecture', 'seminar'), chapters=None):
    """(cale absoluta, limba, kind, N) pentru deck-urile existente in noul flux."""
    out = []
    for n in sorted(TITLES):
        if chapters and str(n) not in chapters and n not in chapters:
            continue
        for kind in kinds:
            for lang in ('en', 'ro'):
                p = os.path.join(ROOT, deck(n, kind, lang))
                if is_new_pipeline(p):
                    out.append((p, lang, kind, n))
    return out


def site_titles():
    """Titlurile din assets/course-data.js (pentru verificare)."""
    p = os.path.join(ROOT, 'assets', 'course-data.js')
    if not os.path.exists(p):
        return {}
    s = open(p, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r"num:\s*(\d+),\s*\n\s*title:\s*\{\s*en:\s*'([^']*)',\s*ro:\s*'([^']*)'", s):
        out[int(m.group(1))] = (m.group(2), m.group(3))
    return out


if __name__ == '__main__':
    st = site_titles()
    for n in sorted(TITLES):
        p = paths(n)
        flag = '' if st.get(n, TITLES[n]) == TITLES[n] else '   <-- title differs from assets/course-data.js: ' + str(st.get(n))
        built = [k for k in ('lecture_en', 'lecture_ro', 'seminar_en', 'seminar_ro')
                 if is_new_pipeline(os.path.join(ROOT, p[k] + '.tex'))]
        print(f'{n:2d}  {p["lecture_en"]}.pdf | {p["lecture_ro"]}.pdf | {p["seminar_en"]}.pdf | {p["seminar_ro"]}.pdf'
              + (f'   [built: {", ".join(built)}]' if built else '') + flag)
