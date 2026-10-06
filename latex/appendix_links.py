"""
appendix_links.py -- legaturi clicabile intre textul cursului si Anexa, cu buton de intoarcere (ATS, preluat din MFM)
=============================================================================================
Doar deck-urile din noul flux (latex/ats_chapters.py). Trimiterile "Capitolul N" / "Chapter N" duc la PDF-ul
capitolului N de pe https://danpele.github.io/Advanced-Time-Series/ (EN/Courses/chapterN_<slug>.pdf, RO/Cursuri/capitolN_<slug>.pdf),
numai pentru capitolele deja reconstruite (altfel textul ramane fara legatura).
In fiecare deck de curs (EN + RO):
  * fiecare mentiune a Anexei din partea principala ("Anexă", "Anexa", "Appendix") devine un buton
    care duce la slide-ul de anexa potrivit (ales dupa cuvintele comune cu titlul si continutul lui);
    mentiunile generale ("Anexa de la final") duc la primul slide al anexei;
  * fiecare slide din anexa primeste, in coltul din dreapta jos, un buton "Înapoi" / "Back" catre
    slide-ul de unde a fost trimis cititorul (prima trimitere; altfel, prima trimitere generala).
Nu se leaga anexele lucrarilor citate ("Anexa A a lucrării", "Appendix A of the paper", "Online Appendix").
Indiciu explicit (optional): un comentariu LaTeX pe acelasi rand cu mentiunea,
    ... \\atsapplink{..}{..}{Anexă}  % applink: <cuvinte din titlul slide-ului de anexa>
alege slide-ul de anexa al carui titlu contine textul indiciului (altfel, cel mai multe cuvinte comune cu el);
indiciul are prioritate fata de potrivirea automata. Slide-urile de anexa de tip "(2/2)" fara trimitere proprie
primesc butonul de intoarcere al slide-ului precedent din aceeasi serie; o trimitere specifica are prioritate
fata de una generala pentru butonul de intoarcere.

Rulare (dupa orice build; acronyms.py il apeleaza automat):
    python3 latex/appendix_links.py            -> toate cursurile
    python3 latex/appendix_links.py 0 4        -> doar capitolele 0 si 4
Trimiterile la cursurile surori devin linkuri catre PDF-urile lor:
  * TSA (licenta, cursul prealabil, https://danpele.github.io/Time-Series-Analysis/):
      "TSA Chapter 7", "TSA, Chapter 7", "Chapter 7 of TSA" / "TSA, Capitolul 7", "Capitolul 7 din TSA";
  * MFM (master, anul II, cursul care continua ATS, https://danpele.github.io/MFM/):
      "MFM Chapter 9", "Chapter 9 of MFM" / "MFM, Capitolul 9", "Capitolul 9 din MFM".
  Numele PDF-urilor sint in EXTERNAL (actualizati-le daca TSA sau MFM isi redenumesc capitolele).
Idempotent: legaturile vechi sînt sterse si refacute la fiecare rulare.
"""
import glob
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

MACROS = (r'\providecommand{\atsapplink}[3]{\hypertarget{#2}{}\hyperlink{#1}{\beamergotobutton{#3}}}  % APPLINKS-MACROS' '\n'
          r'\providecommand{\atsappback}[2]{\begin{tikzpicture}[remember picture,overlay]'
          r'\node[anchor=south east] at ([xshift=-3mm,yshift=7mm]current page.south east)'
          r'{\hyperlink{#1}{\beamerreturnbutton{#2}}};\end{tikzpicture}}' '  % APPLINKS-MACROS\n'
          r'\providecommand{\atschlink}[2]{\href{#1}{#2}}  % APPLINKS-MACROS' '\n'
          r'\providecommand{\atschlinkt}[2]{\href{#1}{\usebeamercolor[fg]{frametitle}#2}}  % APPLINKS-MACROS' '\n')

APP_SEC = re.compile(r'\\section\*?\{(Anex[ăae]|Anexe|Appendix|Appendices)[^}]*\}')
END_SEC = re.compile(r'\\section\*?\{(Bibliografie|Referințe|References|Bibliography)\}|\\end\{document\}')
FRAME = re.compile(r'\\begin\{frame\}(\[[^\]]*\])?(\{((?:[^{}]|\{[^{}]*\})*)\})?')
MENTION = re.compile(r'(?<![\\\w])(Anex[ăae]|anex[ăae]|Appendix|appendix|Appendices|appendices)(?![\w])')
PAPER_AFTER = re.compile(r'^\s*([A-Z]\b)?[\s,]*(a lucrării|al lucrării|lucrării|din lucrare|of the paper|of the article|online|Online|din articol|a articolului)')
PAPER_BEFORE = re.compile(r'(Online|online|Internet|paper\'s|Supplementary|supplementary|lucrării,?)\s*$')
GENERIC = re.compile(r'de la final|at the end|at the back', re.I)
HINT = re.compile(r'(?<!\\)%\s*applink:\s*(.+?)\s*$')
PART = re.compile(r'^(.*?)\s*\((\d+)/(\d+)\)\s*$')


def comment_start(line):
    """Pozitia primului % neprotejat dintr-un rand (inceputul comentariului) sau len(line)."""
    m = re.search(r'(?<!\\)%', line)
    return m.start() if m else len(line)


def plain(t):
    t = re.sub(r'\\[a-zA-Z]+\*?', ' ', t)
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9/()]+', ' ', t).strip()


def hint_target(hint, frames):
    """Indexul slide-ului de anexa indicat de un comentariu '% applink: ...' (None daca nu se potriveste)."""
    h = plain(hint)
    exact = [k for k, f in enumerate(frames) if h and h in plain(f['title'])]
    if exact:
        return exact[0]
    hw = norm(hint)
    sc = [len(hw & norm(f['title'])) for f in frames]
    best = max(range(len(frames)), key=lambda k: (sc[k], -k)) if frames else None
    return best if best is not None and sc[best] > 0 else None

STOP = set('''acest aceasta aceste pentru dintre despre sînt este care prin într între fără după pînă cînd unde
cele care toate toți mult mare mari doar sau și din ale lui unui unei with from that this these those into than then
their there where which while about between under over each more most very only also used uses using appendix anexa
anexă anexe slide slides frame title capitol chapter''' .split())


def norm(s):
    s = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?', ' ', s)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return {w[:5] for w in re.findall(r'[a-z]{4,}', s) if w not in STOP}


def strip_old(s):
    s = re.sub(r'.*% APPLINKS-MACROS\n', '', s)
    s = re.sub(r'\\providecommand\{\\atsapplink\}.*\n', '', s)
    s = re.sub(r'\\atschlinkt?\{[^{}]*\}\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\atsapplink\{[^{}]*\}\{[^{}]*\}\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\n\\hypertarget\{atsapp\d+\}\{\}\\atsappback\{[^{}]*\}\{[^{}]*\}', '', s)
    return s


def protected_spans(s):
    spans = []
    for m in re.finditer(r'\\begin\{(lstlisting|verbatim|minted)\}.*?\\end\{\1\}', s, re.S):
        spans.append(m.span())
    for m in re.finditer(r'\\(texttt|url|href|quantlet|frametitle|section|subsection)\*?\{', s):
        depth, i = 1, m.end()
        while i < len(s) and depth:
            depth += {'{': 1, '}': -1}.get(s[i], 0)
            i += 1
        spans.append((m.start(), i))
    for m in FRAME.finditer(s):          # titlurile slide-urilor nu primesc butoane
        spans.append(m.span())
    return spans


from ats_chapters import SITE, new_decks, deck as _deck, is_new_pipeline, TITLES  # noqa: E402

# Cursurile surori: TSA (prerechizit, licenta) si MFM (continuare, master anul II); N -> (PDF EN, PDF RO)
EXTERNAL = {
    'TSA': ('https://danpele.github.io/Time-Series-Analysis/', {
        0: ('chapter0_introduction', 'capitol0_introducere'),
        1: ('chapter1_stochastic_processes_stationarity', 'capitol1_procese_stochastice_stationaritate'),
        2: ('chapter2_arma_models', 'capitol2_modele_arma'),
        3: ('chapter3_unit_roots_arima_models', 'capitol3_radacini_unitare_modele_arima'),
        4: ('chapter4_seasonality_forecasting', 'capitol4_sezonalitate_prognoza'),
        5: ('chapter5_conditional_volatility_garch', 'capitol5_volatilitate_conditionata_garch'),
        6: ('chapter6_var_models_granger_causality', 'capitol6_modele_var_cauzalitate_granger'),
        7: ('chapter7_cointegration_vecm', 'capitol7_cointegrare_vecm'),
        8: ('chapter8_long_memory_arfima', 'capitol8_memorie_lunga_arfima'),
        9: ('chapter9_machine_learning_time_series', 'capitol9_invatare_automata_serii_timp'),
        10: ('chapter10_state_space_kalman_markov_switching', 'capitol10_spatiul_starilor_kalman_markov_switching'),
        11: ('chapter11_foundation_models_time_series', 'capitol11_foundation_models_serii_timp'),
        12: ('chapter12_spectral_analysis', 'capitol12_analiza_spectrala'),
        13: ('chapter13_bubbles_lppl', 'capitol13_bule_lppl'),
        14: ('chapter14_multivariate_garch_models', 'capitol14_modele_garch_multivariate'),
        15: ('chapter15_review', 'capitol15_recapitulare'),
    }),
    'MFM': ('https://danpele.github.io/MFM/', {
        0: ('chapter0_financial_markets', 'capitol0_piete_financiare'),
        1: ('chapter1_stylised_facts', 'capitol1_fapte_stilizate'),
        2: ('chapter2_market_efficiency', 'capitol2_eficienta_pietei'),
        3: ('chapter3_factor_models', 'capitol3_modele_factoriale'),
        4: ('chapter4_portfolio_optimization', 'capitol4_optimizarea_portofoliului'),
        5: ('chapter5_garch_models', 'capitol5_modele_garch'),
        6: ('chapter6_multivariate_dependence', 'capitol6_dependenta_multivariata'),
        7: ('chapter7_var_expected_shortfall', 'capitol7_var_expected_shortfall'),
        8: ('chapter8_backtesting_risk', 'capitol8_backtesting_risc'),
        9: ('chapter9_realized_volatility', 'capitol9_volatilitate_realizata'),
        10: ('chapter10_market_microstructure', 'capitol10_microstructura_pietei'),
        11: ('chapter11_continuous_time', 'capitol11_timp_continuu'),
        12: ('chapter12_options_volatility_surface', 'capitol12_optiuni_suprafata_volatilitate'),
        13: ('chapter13_machine_learning', 'capitol13_machine_learning'),
        14: ('chapter14_deep_learning_foundation_models', 'capitol14_deep_learning_modele_fundationale'),
        15: ('chapter15_llm_sentiment', 'capitol15_llm_sentiment'),
        16: ('chapter16_digital_assets_defi', 'capitol16_active_digitale_defi'),
        17: ('chapter17_bubbles_crashes', 'capitol17_bule_crahuri'),
        18: ('chapter18_systemic_risk_networks', 'capitol18_risc_sistemic_retele'),
        19: ('chapter19_review_projects', 'capitol19_recapitulare_proiecte'),
        20: ('chapter20_signatures_realized_volatility', 'capitol20_signaturi_volatilitate_realizata'),
    }),
}
EXT_BEFORE = re.compile(r'(?<![\\\w])(TSA|MFM)(,?)(~|\s)+(Chapter|Capitolul)(~|\s)+(\d{1,2})(?!\d)')
EXT_AFTER = re.compile(r'(?<![\\\w])(Chapter|Capitolul)(~|\s)+(\d{1,2})(~|\s)+(of|din)(~|\s)+(TSA|MFM)(?![\w])')


def external_url(course, n, lang):
    base, chs = EXTERNAL[course]
    if n not in chs:
        return None
    en, ro = chs[n]
    return base + ('EN/Courses/' + en if lang == 'en' else 'RO/Cursuri/' + ro) + '.pdf'


def external_links(s, lang):
    """'TSA, Capitolul 7' / 'Chapter 9 of MFM' -> link catre PDF-ul capitolului din cursul sora (inainte de bibliografie)."""
    b = max(s.find('\\begin{document}'), 0)
    bm = re.search(r'\\section\*?\{(Bibliografie|Referințe|References|Bibliography)\}', s)
    cut = bm.start() if bm else len(s)
    spans = protected_spans(s)
    edits = []
    for rx, ci, ni in ((EXT_BEFORE, 1, 6), (EXT_AFTER, 7, 3)):
        for m in rx.finditer(s, b, cut):
            if any(x <= m.start() < y for x, y in spans):
                continue
            ls = s.rfind('\n', 0, m.start()) + 1
            if m.start() - ls >= comment_start(s[ls:s.find('\n', m.start())]):
                continue
            url = external_url(m.group(ci), int(m.group(ni)), lang)
            if url:
                edits.append((m.start(), m.end(), r'\atschlink{%s}{%s}' % (url, m.group(0))))
    for i, j, rep in sorted(edits, reverse=True):
        s = s[:i] + rep + s[j:]
    return s


CH_WORD = re.compile(r'(?<![\w\\])(Capitolul|Capitolului|Capitolele|Capitolelor|capitolul|capitolului|capitolele|capitolelor|Chapters|Chapter|chapters|chapter)(~|\s)+(\d{1,2})((?:\s*(?:,|și|and|--|–)\s*\d{1,2})*)')
NUM = re.compile(r'\d{1,2}')


def chapter_urls(lang):
    """N -> URL-ul PDF-ului de curs pe site, doar pentru capitolele reconstruite in noul flux."""
    out = {}
    for n in TITLES:
        rel = _deck(n, 'lecture', lang)
        if is_new_pipeline(os.path.join(ROOT, rel)):
            out[n] = SITE + rel.replace('.tex', '.pdf')
    return out


def chapter_links(s, lang):
    """Trimiterile la capitolele cursului ("Capitolul 14", "Capitolele 14 și 15", "Chapters 5--9") devin linkuri
    catre PDF-ul capitolului de pe site-ul cursului."""
    urls = chapter_urls(lang)
    b = s.find('\\begin{document}')
    spans = protected_spans(s)
    bm = re.search(r'\\section\*?\{(Bibliografie|Referințe|References|Bibliography)\}', s)
    bib_start = bm.start() if bm else len(s)
    edits = []
    for m in CH_WORD.finditer(s, max(b, 0)):
        if any(x <= m.start() < y for x, y in spans):
            continue
        if m.start() >= bib_start:          # bibliografia: capitolele cartilor citate nu sint capitolele cursului
            continue
        after = s[m.end():m.end() + 30]
        if re.match(r'\s*(al lucrării|al cărții|din carte|din cartea|of the book|of the paper|of \\ref|din \\ref|(of|din)(~|\s)+(TSA|MFM)\b)', after):
            continue
        if re.search(r'(TSA|MFM),?(~|\s)+$', s[max(0, m.start() - 6):m.start()]):
            continue
        ls = s.rfind('\n', 0, m.start()) + 1
        if s[ls:m.start()].lstrip().startswith('%') or m.start() - ls >= comment_start(s[ls:s.find('\n', m.start())]):
            continue
        first = int(m.group(3))
        if first not in urls:
            continue
        rep = r'\atschlink{%s}{%s%s%s}' % (urls[first], m.group(1), m.group(2), m.group(3))
        rest = m.group(4)
        rest = NUM.sub(lambda n: (r'\atschlink{%s}{%s}' % (urls[int(n.group(0))], n.group(0))) if int(n.group(0)) in urls else n.group(0), rest)
        edits.append((m.start(), m.end(), rep + rest))
    for i, j, rep in reversed(edits):
        s = s[:i] + rep + s[j:]
    # titlurile slide-urilor: aceleasi linkuri, in culoarea titlului
    def title_fix(fm):
        t = fm.group(3)
        if not t or 'atschlink' in t:
            return fm.group(0)
        def one(m):
            first = int(m.group(3))
            if first not in urls:
                return m.group(0)
            rest = NUM.sub(lambda n: (r'\atschlinkt{%s}{%s}' % (urls[int(n.group(0))], n.group(0))) if int(n.group(0)) in urls else n.group(0), m.group(4))
            return r'\atschlinkt{%s}{%s%s%s}' % (urls[first], m.group(1), m.group(2), m.group(3)) + rest
        t2 = CH_WORD.sub(one, t)
        return fm.group(0).replace('{' + t + '}', '{' + t2 + '}', 1) if t2 != t else fm.group(0)
    bm2 = re.search(r'\\section\*?\{(Bibliografie|Referințe|References|Bibliography)\}', s)
    cut = bm2.start() if bm2 else len(s)
    s = FRAME.sub(title_fix, s[:cut]) + s[cut:]
    return s, len(edits)



def analyze(path):
    s = strip_old(open(path, encoding='utf-8').read())
    an = {'path': path, 's': s, 'frames': [], 'mentions': []}
    a = APP_SEC.search(s)
    if not a:
        return an
    e = END_SEC.search(s, a.end())
    app_end = e.start() if e else len(s)
    for m in FRAME.finditer(s, a.end(), app_end):
        body_end = s.find(r'\end{frame}', m.end())
        an['frames'].append({'hdr_end': m.end(), 'title': m.group(3) or '',
                             'words': norm((m.group(3) or '') * 2 + ' ' + s[m.end():min(body_end, m.end() + 600)])})
    df = {}
    for f in an['frames']:
        for w in f['words']:
            df[w] = df.get(w, 0) + 1
    idf = {w: 1.0 / d for w, d in df.items()}
    spans = protected_spans(s[:a.start()])
    main_frames = [(m.start(), m.group(3) or '') for m in FRAME.finditer(s, 0, a.start())]
    for m in MENTION.finditer(s, 0, a.start()):
        i = m.start()
        if any(x <= i < y for x, y in spans):
            continue
        if PAPER_AFTER.match(s[m.end():m.end() + 40]) or PAPER_BEFORE.search(s[max(0, i - 25):i]):
            continue
        ls = s.rfind('\n', 0, i) + 1
        line = s[ls:s.find('\n', i)]
        if line.lstrip().startswith('%') or i - ls >= comment_start(line):
            continue
        hm = HINT.search(line)
        hint = hint_target(hm.group(1), an['frames']) if hm else None
        fst, ftitle = next(((st, t) for st, t in reversed(main_frames) if st < i), (0, ''))
        ctx_line = norm(line + ' ' + ftitle)
        ctx_frame = norm(s[fst:s.find('\n', i)])
        scores = [2 * sum(idf[w] for w in ctx_line & f['words']) + 0.5 * sum(idf[w] for w in (ctx_frame - ctx_line) & f['words'])
                  for f in an['frames']]
        generic = bool(GENERIC.search(line[:i - ls + len(m.group(0)) + 20]))
        an['mentions'].append({'i': i, 'j': m.end(), 'text': m.group(0), 'scores': scores, 'generic': generic,
                               'hint': hint})
    return an


def choose(an, other=None):
    """Slide-ul de anexa pentru fiecare mentiune; cu deck-ul paralel (EN/RO), scorurile se aduna."""
    paired = (other is not None and len(other['mentions']) == len(an['mentions'])
              and len(other['frames']) == len(an['frames']))
    out = []
    for n, m in enumerate(an['mentions']):
        sc = list(m['scores'])
        generic = m['generic']
        if paired:
            sc = [x + y for x, y in zip(sc, other['mentions'][n]['scores'])]
            generic = generic or other['mentions'][n]['generic']
        hint = m['hint'] if m['hint'] is not None else (other['mentions'][n]['hint'] if paired else None)
        if hint is not None:
            out.append(hint)
            continue
        thr = 2.0 if paired else 1.2
        best = max(range(len(sc)), key=lambda k: (sc[k], -k)) if sc else 0
        out.append(best if sc and sc[best] >= thr and not generic else 0)
    return out


def apply(an, choice, lang):
    s, frames = an['s'], an['frames']
    if not frames:
        s, _ = chapter_links(s, lang)
        s = external_links(s, lang)
        d = s.find('\\begin{document}')
        s = s[:d] + MACROS + s[d:]
        open(an['path'], 'w', encoding='utf-8').write(s)
        return 0, 0
    back = [None] * len(frames)
    edits, generic_src = [], None
    for n, (m, k) in enumerate(zip(an['mentions'], choice), 1):
        src = f'atssrc{n}'
        is_generic = k == 0 and m['generic'] and m['hint'] is None
        if back[k] is None and not is_generic:
            back[k] = src
        if k == 0 and generic_src is None:
            generic_src = src
        edits.append((m['i'], m['j'], r'\atsapplink{atsapp%d}{%s}{%s}' % (k + 1, src, m['text'])))
    for k in range(1, len(frames)):       # "(2/2)" fara trimitere proprie: intoarcerea slide-ului (1/2)
        a, b = PART.match(frames[k - 1]['title']), PART.match(frames[k]['title'])
        if back[k] is None and a and b and a.group(1) == b.group(1):
            back[k] = back[k - 1]
    label = 'Înapoi' if lang == 'ro' else 'Back'
    for k, f in enumerate(frames):
        target = back[k] or generic_src or ('atssrc1' if an['mentions'] else None)
        if target:
            edits.append((f['hdr_end'], f['hdr_end'], '\n\\hypertarget{atsapp%d}{}\\atsappback{%s}{%s}' % (k + 1, target, label)))
    for i, j, rep in sorted(edits, key=lambda t: t[0], reverse=True):
        s = s[:i] + rep + s[j:]
    s, _ = chapter_links(s, lang)
    s = external_links(s, lang)
    d = s.find('\\begin{document}')
    s = s[:d] + MACROS + s[d:]
    open(an['path'], 'w', encoding='utf-8').write(s)
    return len(an['mentions']), len(frames)


def decks(chapters=None):
    return [(p, lang) for p, lang, kind, n in new_decks(kinds=('lecture',), chapters=chapters)]


def seminar_decks(chapters=None):
    return [(p, lang) for p, lang, kind, n in new_decks(kinds=('seminar',), chapters=chapters)]


if __name__ == '__main__':
    for f, lang in seminar_decks(set(sys.argv[1:]) or None):
        t = strip_old(open(f, encoding='utf-8').read())
        t, k = chapter_links(t, lang)
        t = external_links(t, lang)
        d = t.find('\\begin{document}')
        t = t[:d] + MACROS + t[d:]
        open(f, 'w', encoding='utf-8').write(t)
    ds = decks(set(sys.argv[1:]) or None)
    by_ch = {}
    for f, lang in ds:
        n = re.search(r'(chapter|capitol)(\d+)_', os.path.basename(f)).group(2)
        by_ch.setdefault(n, {})[lang] = analyze(f)
    for n, pair in sorted(by_ch.items(), key=lambda t: int(t[0])):
        for lang, an in pair.items():
            other = pair.get('ro' if lang == 'en' else 'en')
            cnt, k = apply(an, choose(an, other), lang)
            paired = other is not None and len(other['mentions']) == len(an['mentions']) and len(other['frames']) == len(an['frames'])
            print(f'{os.path.relpath(an["path"], ROOT)}: {cnt} links to {k} appendix slides' + ('' if paired else '  [EN/RO not parallel]'))
