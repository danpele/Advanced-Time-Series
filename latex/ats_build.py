r"""
ats_build.py -- cadrul comun al generatoarelor ATS (curs + seminar, EN + RO dintr-o singura sursa)
================================================================================================
Copiat din cursul TSA (latex/tsa_build.py, la randul lui preluat din MFM) si adaptat pentru ATS. Un generator de capitol arata asa:

    import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ats_build import Deck, Values, n, items, cols, block, table, photo, fig

    V = Values(); V.put('pers', 0.9812, 3)                   # cifre calculate in Quantlets/Ch_NN
    D = Deck(5, 'lecture', refs=r'\newcommand{\refBollerslev}{\href{https://doi.org/10.1016/0304-4076(86)90063-1}{Bollerslev (1986)}}')
    D.section('Motivation', 'Motivație')
    D.frame('⟦Persistence||Persistența⟧', items('⟦Estimated persistence: @{pers}||Persistența estimată: @{pers}⟧'))
    D.chart('⟦Conditional volatility||Volatilitatea condiționată⟧', 'ats_ch5_sigma', 'ATS_ch5_sigma', ['⟦...||...⟧'])
    D.references([r"Bollerslev, T. (1986). ...", ...])
    D.write(V)                       # EN/Courses/chapter5_conditional_volatility_garch.tex
                                     # + RO/Cursuri/capitol5_volatilitate_conditionata_garch.tex
                                     # + glosarul de acronime (acronyms.py 5) + legaturile catre Anexa

Conventii (aceleasi ca in MFM):
  * ⟦english||romana⟧ se inlocuieste in functie de limba;
  * @{cheie} se inlocuieste cu cifre din Values (calculate in Quantlets, niciodata scrise de mina);
  * in RO, zecimalele marcate ⁅...⁆ (Values.put, n()) si cele din $...$ devin virgule; "de" se adauga dupa
    numeralele >= 20 ("131 de zile");
  * seminarele: versiunea pentru studenti este implicita; D.write scrie si wrapper-ul *_solutions.tex
    (\solutionstrue), exclus din git.

Alte comenzi:
  python3 latex/ats_build.py compile 0            -> pdflatex de doua ori pe toate deck-urile noi ale capitolului 0
                                                     (+ wrapper-ele _solutions); raporteaza erorile si overfull vbox
  python3 latex/ats_build.py convert <vechi.tex> <N> <en|ro>
                                                  -> converteste un deck vechi (cu preambulul copiat in fisier) la
                                                     noul flux: preambul comun, titlu standard, nume nou
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from ats_chapters import COURSE, TITLES, deck, paths, new_decks   # noqa: E402

MARK = re.compile(r'⟦(.*?)\|\|(.*?)⟧', flags=re.S)
TOKEN = re.compile(r'@\{([\w.-]+)\}')
QL_REPO = 'https://github.com/danpele/Advanced-Time-Series/tree/main/Quantlets'

AUTHOR_LECTURE = r'\author[D.T. Pele]{Daniel Traian PELE}'
# Seminarii: intregul curs este sub numele lui Pele (decizia titularului, 5 octombrie 2026); niciun titular de seminar numit
AUTHOR_SEMINAR = AUTHOR_LECTURE

INSTITUTE = {
    'en': r"""\institute{Bucharest University of Economic Studies\\
IDA Institute Digital Assets\\
Blockchain Research Center\\
AI4EFin Artificial Intelligence for Energy Finance\\
Romanian Academy, Institute for Economic Forecasting\\
MSCA Digital Finance}""",
    'ro': r"""\institute{Academia de Studii Economice din București\\
IDA Institute Digital Assets\\
Blockchain Research Center\\
AI4EFin Artificial Intelligence for Energy Finance\\
Academia Română, Institutul de Prognoză Economică\\
MSCA Digital Finance}""",
}
PROGRAMME = {'en': "Master's programme Applied Statistics and Data Science, year 1, semester 2, Bucharest University of Economic Studies",
             'ro': 'Programul de master Statistică aplicată și data science, anul I, semestrul 2, Academia de Studii Economice din București'}


# =============================================================================
# TEXT BILINGV SI CIFRE
# =============================================================================
def fmt(x, d=3, sign=False, pct=False):
    """Numar cu d zecimale, in format EN (punctul devine virgula in RO la randare)."""
    if pct:
        x = 100 * x
    return f'{x:+.{d}f}' if sign else f'{x:.{d}f}'


def n(x, d=3, sign=False, pct=False):
    """Cifra marcata pentru conversia zecimala RO, de folosit direct in text sau tabele."""
    return '⁅' + fmt(float(x), d, sign, pct) + '⁆'


class Values(dict):
    """Dictionar de cifre; fiecare valoare numerica este marcata ⁅...⁆ pentru conversia zecimala RO."""

    def put(self, key, x, d=3, sign=False, pct=False):
        self[key] = n(x, d, sign, pct)

    def raw(self, key, s):
        self[key] = s

    def int(self, key, x):
        """Intreg cu spatiu fin pentru mii (2\\,692)."""
        self[key] = f'{int(x):,}'.replace(',', '\\,')


RO_NOUNS = ('zile|randamente|perechi|traiectorii|decalaje|laguri|observații|extrageri|prognoze|prognozatori|'
            'acțiuni|ferestre|reziduuri|luni|ani|trimestre|simulări|valori|companii|săptămîni|săptămâni|tranzacții|'
            'indici|serii|lei|depășiri|puncte|regresii|reguli|replicări|reeșantionări|țări|modele|iterații|'
            'parametri|predictori|origini|estimații|perioade')
RO_NUM = re.compile(r'(?<![\d,.}{\\-])(⁅?)(\d{1,3}(?:(?:\\,|\\ )\d{3})+|\d+)(⁆?) (?=(?:' + RO_NOUNS + r')\b)')
# a range "74--131 zile": the noun follows the second numeral, which the rule above skips (it follows a dash)
RO_RANGE = re.compile(r'(?<![\d,.}{\\-])(⁅?\d+⁆?--)(⁅?)(\d+)(⁆?) (?=(?:' + RO_NOUNS + r')\b)')


def ro_de(tex):
    """RO: „de” intre numeral si substantiv cind ultimele doua cifre sint >= 20 sau 00 (131 de zile)."""
    def f(m):
        v = int(re.sub(r'\D', '', m.group(2)))
        need = v >= 20 and (v % 100 >= 20 or v % 100 == 0)
        return m.group(0) + ('de ' if need else '')

    def g(m):
        v = int(m.group(3))
        need = v >= 20 and (v % 100 >= 20 or v % 100 == 0)
        return m.group(0) + ('de ' if need else '')
    return RO_RANGE.sub(g, RO_NUM.sub(f, tex))


def render(tex, lang, values=None):
    values = values or {}

    def tok(m):
        key = m.group(1)
        if key not in values:
            raise KeyError(f'missing value @{{{key}}}')
        return str(values[key])
    tex = TOKEN.sub(tok, tex)
    # negative numbers from the formatter (n(), Values.put): a real minus sign, valid in text and in math mode
    tex = tex.replace('⁅-', '⁅\\ensuremath{-}')
    tex = MARK.sub(lambda m: m.group(1) if lang == 'en' else m.group(2), tex)
    if lang == 'ro':
        # the comma becomes the decimal mark: two numbers separated by a comma ([1.23, 1.45]) get a semicolon
        tex = re.sub(r'(⁅[^⁆]*⁆),(\s*)(?=⁅)', lambda m: m.group(1) + (';' if '.' in m.group(1) else ',') + m.group(2), tex)
        tex = re.sub(r'(⁅[^⁆]*⁆),(\s*)(⁅[^⁆]*\.[^⁆]*⁆)', r'\1;\2\3', tex)
        tex = re.sub(r'⁅([^⁆]*)⁆', lambda m: re.sub(r'(\d)\.(\d)', r'\1{,}\2', m.group(1)), tex)
        tex = re.sub(r'(?<!\\)\$(.+?)(?<!\\)\$', lambda m: '$' + re.sub(r'(\d)\.(\d)', r'\1{,}\2', m.group(1)) + '$', tex)
        tex = re.sub(r'\b(ES|VaR|CoVaR|MES) (\d+)\.(\d+)\\%', r'\1 \2,\3\\%', tex)   # risk-measure levels in plain text: ES 2,5%
        tex = ro_de(tex)
    tex = re.sub(r'⁅([^⁆]*)⁆', r'\1', tex)
    leftover = MARK.search(tex) or re.search(r'⟦|⟧', tex)
    if leftover:
        raise ValueError(f'unbalanced ⟦..||..⟧ near: {tex[max(0, leftover.start() - 60):leftover.start() + 60]!r}')
    return tex


# =============================================================================
# BLOCURI DE SLIDE (functii pure, intorc text LaTeX)
# =============================================================================
def items(*xs):
    """Lista de nivel 1; un element poate fi (text, [subelemente])."""
    out = ['\\begin{itemize}']
    for x in xs:
        if isinstance(x, tuple):
            out.append(f'    \\item {x[0]}')
            out.append('    \\begin{itemize}')
            out += [f'        \\item {s}' for s in x[1]]
            out.append('    \\end{itemize}')
        else:
            out.append(f'    \\item {x}')
    out.append('\\end{itemize}')
    return '\n'.join(out)


def enum(*xs, start=None):
    s = '\\begin{enumerate}\n' + (f'\\setcounter{{enumi}}{{{start - 1}}}\n' if start else '')
    return s + '\n'.join(f'    \\item {x}' for x in xs) + '\n\\end{enumerate}'


def block(title, content, kind='block'):
    return f'\\begin{{{kind}}}{{{title}}}\n{content}\n\\end{{{kind}}}'


def cols(left, right, wl='0.48', wr='0.48'):
    return (f'\\begin{{columns}}[T]\n\\begin{{column}}{{{wl}\\textwidth}}\n{left}\n\\end{{column}}\n'
            f'\\begin{{column}}{{{wr}\\textwidth}}\n{right}\n\\end{{column}}\n\\end{{columns}}')


def table(spec, header, rows, size='scriptsize'):
    return (f'\\begin{{center}}\n\\{size}\n\\begin{{tabular}}{{{spec}}}\n\\toprule\n{header} \\\\\n\\midrule\n'
            + '\n'.join(r + ' \\\\' for r in rows) + '\n\\bottomrule\n\\end{tabular}\n\\end{center}\n')


def fig(name, h='0.46', w='0.96'):
    return (f'\\begin{{center}}\n\\includegraphics[width={w}\\textwidth,height={h}\\textheight,keepaspectratio]{{{name}.pdf}}\n'
            f'\\end{{center}}\n\\vspace{{-2mm}}\n')


def photo(file, cap, url, credit, h='0.52\\textheight'):
    """Fotografie cu legenda si credit vizibil (sursa + licenta verificata)."""
    return (f'\\centering\n\\includegraphics[height={h}]{{{file}}}\\\\[1mm]\n\\imgcap{{{cap}}}\n'
            f'\\imgcredit{{{url}}}{{{credit}}}')


def ql(folder):
    """Linkul Quantlet al unui folder din capitolul curent (\\qlurl este definit de Deck)."""
    return f'\\quantlet{{{folder.replace("_", chr(92) + "_")}}}{{\\qlurl{{{folder}}}}}'


# =============================================================================
# DECK
# =============================================================================
SOLVED = '⟦[Solved]||[Rezolvat]⟧'
PROP = '⟦[Proposed]||[Propus]⟧'
TASK = '⟦Task||Cerință⟧'
SOL = '⟦Solution||Rezolvare⟧'
INTERP = '⟦Interpretation||Interpretare⟧'

DOC_START = r"""
%=============================================================================
\begin{document}
%=============================================================================

{
\setbeamertemplate{headline}{}
\setbeamertemplate{footline}{}
\begin{frame}[noframenumbering]
    \titlepage
\end{frame}
}

"""


class Deck:
    """Un deck bilingv (curs sau seminar) al capitolului `chapter`."""

    def __init__(self, chapter, kind='lecture', refs='', macros='', subtitle=None, generator=None):
        assert kind in ('lecture', 'seminar')
        self.n, self.kind = chapter, kind
        self.refs, self.macros = refs, macros
        en, ro = TITLES[chapter]
        word = ('Chapter', 'Capitolul') if kind == 'lecture' else ('Seminar', 'Seminarul')
        self.subtitle = subtitle or (f'{word[0]} {chapter}: {en}', f'{word[1]} {chapter}: {ro}')
        self.generator = generator or os.path.basename(sys.argv[0]) or 'ats_build.py'
        self.FR = []

    # ---- elemente
    def section(self, en, ro):
        self.FR.append('\n%' + '=' * 77 + f'\n\\section{{⟦{en}||{ro}⟧}}\n%' + '=' * 77 + '\n')

    def frame(self, title, body, size='small', opts='', instructor_only=False):
        o = f'[{opts}]' if opts else ''
        sz = f'\\itemsize{{\\{size}}}\n' if size else ''
        t = f'\\begin{{frame}}{o}{{{title}}}\n{sz}{body.strip()}\n\\end{{frame}}\n'
        self.FR.append('\\ifsolutions\n' + t + '\\fi\n' if instructor_only else t)

    def raw(self, tex):
        self.FR.append(tex)

    def chart(self, title, figname, folder, bullets, width='0.84\\textwidth', height=None, size='footnotesize'):
        g = f'width=0.97\\textwidth,height={height},keepaspectratio' if height else f'width={width}'
        body = (f'\\begin{{center}}\n    \\includegraphics[{g}]{{{figname}.pdf}}\n\\end{{center}}\n\\vspace{{-0.25cm}}\n'
                + items(*bullets) + '\n' + ql(folder))
        self.frame(title, body, size)

    def recap(self, title, bullets):
        ro = title[1]
        w = ro.split(' ')[0]
        if w[1:].isalpha() and w[1:].islower() and not w.startswith('Student'):   # RO: lower case after the colon, except names and acronyms
            ro = ro[0].lower() + ro[1:]
        self.frame(f'⟦Recap: {title[0]}||Recapitulare: {ro}⟧', items(*bullets))

    # ---- seminar: probleme rezolvate / propuse (formatul A/B/C din MFM)
    def solved(self, title, task, solution, size='small'):
        body = ('\\begin{columns}[T]\n\\begin{column}{0.47\\textwidth}\n' + block(TASK, task) +
                '\n\\end{column}\n\\begin{column}{0.49\\textwidth}\n' + block(SOL, solution, 'exampleblock') +
                '\n\\end{column}\n\\end{columns}')
        self.frame(f'{title} {SOLVED}', body, size)

    def proposed(self, title, task, solution, size='small'):
        body = ('\\propsub\n' + (f'\\itemsize{{\\{size}}}\n' if size else '') +
                '\\begin{columns}[T]\n\\begin{column}{\\taskw}\n' + block(TASK, task) +
                '\n\\end{column}\n\\begin{column}{\\solw}\n\\solonly{%\n' + block(SOL, solution, 'exampleblock') +
                '\n}\n\\end{column}\n\\end{columns}')
        self.FR.append(f'\\begin{{frame}}{{{title} {PROP}}}\n' + body + '\n\\end{frame}\n')

    def task(self, title, question, inputs, tasks, report, size='small', nb=None):
        """Cerinta explicita: intrebare, date, sub-cerinte numerotate (propozitii complete), ce se raporteaza."""
        body = [f'\\item \\textbf{{⟦Question||Întrebarea⟧}}: {question}']
        if inputs:
            body.append(f'\\item \\textbf{{⟦Inputs||Date⟧}}: {inputs}')
        body.append('\\item \\textbf{⟦Tasks||Cerințe⟧}\n' + enum(*tasks))
        if report:
            body.append(f'\\item \\textbf{{⟦Report||Raportați⟧}}: {report}')
        if nb:
            body.append(f'\\item ⟦Notebook: section {nb}||Notebook: secțiunea {nb}⟧')
        self.frame(title, '\\begin{itemize}\n' + '\n'.join(body) + '\n\\end{itemize}', size)

    def references(self, refs, per=16):
        """Bibliografia: intrari complete cu \\href (DOI verificat), in ordine alfabetica."""
        self.section('References', 'Bibliografie')
        pages = max(1, -(-len(refs) // per))
        size = -(-len(refs) // pages)          # balanced pages: 17 entries -> 9 + 8, not 16 + 1
        chunks = [refs[i:i + size] for i in range(0, len(refs), size)]
        for i, ch in enumerate(chunks, 1):
            num = f' ({i}/{len(chunks)})' if len(chunks) > 1 else ''
            self.FR.append(f'\\begin{{frame}}{{⟦References||Bibliografie⟧{num}}}\n\\itemsize{{\\tiny}}\n'
                           + items(*ch) + '\n\\end{frame}\n')

    # ---- antet
    def head(self, lang):
        en, ro = TITLES[self.n]
        what = {('lecture', 'en'): f'Chapter {self.n}: {en}', ('lecture', 'ro'): f'Capitolul {self.n}: {ro}',
                ('seminar', 'en'): f'Seminar {self.n}: {en}', ('seminar', 'ro'): f'Seminarul {self.n}: {ro}'}[(self.kind, lang)]
        gen = (f'% GENERATED by latex/{self.generator} -- edit the generator, not this file.' if lang == 'en'
               else f'% GENERAT de latex/{self.generator} -- modificați generatorul, nu acest fișier.')
        h = f'% {what}\n% {COURSE[lang]} -- {PROGRAMME[lang]}\n{gen}\n'
        if self.kind == 'seminar':
            h += ('% Student version by default; the instructor version is the *_solutions.tex wrapper.\n' if lang == 'en'
                  else '% Implicit versiunea pentru studenți; versiunea profesorului este wrapper-ul *_solutions.tex.\n')
            h += '\\makeatletter\\@ifundefined{ifsolutions}{\\expandafter\\newif\\csname ifsolutions\\endcsname}{}\\makeatother\n'
        h += f'\n\\newcommand{{\\coursename}}{{{COURSE[lang]}}}\n'
        if lang == 'ro':
            h += '\\def\\atslang{ro}\n'
        return h + '\\input{../../latex/preamble}\n'

    def title_block(self, lang):
        sub = self.subtitle[0 if lang == 'en' else 1]
        if self.kind == 'seminar':
            sub += '\\ifsolutions\\ (' + ('instructor version' if lang == 'en' else 'versiunea profesorului') + ')\\fi'
        auth = AUTHOR_SEMINAR if self.kind == 'seminar' else AUTHOR_LECTURE
        return (f'\n\\title[{COURSE[lang]}]{{{COURSE[lang]}}}\n\\subtitle{{{sub}}}\n{auth}\n{INSTITUTE[lang]}\n\\date{{}}\n')

    def chapter_macros(self):
        m = f'\n\\newcommand{{\\qlurl}}[1]{{{QL_REPO}/Ch_{self.n:02d}/#1}}\n'
        if self.kind == 'seminar':
            p = paths(self.n)['nb_seminar']
            m += (f'\\renewcommand{{\\nb}}{{\\colaburl{{{p}}}}}\n'
                  f'\\renewcommand{{\\nbname}}{{{os.path.basename(p).replace("_", chr(92) + "_")}}}\n'
                  '% left column: full width in the student version, narrower next to the solution\n'
                  '\\newcommand{\\taskw}{\\ifsolutions 0.47\\textwidth\\else 0.96\\textwidth\\fi}\n'
                  '\\newcommand{\\solw}{\\ifsolutions 0.49\\textwidth\\else 0pt\\fi}\n')
        return m + self.macros + ('\n% Clickable citations (DOIs verified via Crossref)\n' + self.refs if self.refs else '')

    # ---- scriere
    def write(self, values=None, glossary=True):
        src = self.chapter_macros() + '@@TITLE@@' + DOC_START + '\n'.join(self.FR) + '\n\\end{document}\n'
        out = []
        for lang in ('en', 'ro'):
            rel = deck(self.n, self.kind, lang)
            tex = self.head(lang) + render(src.replace('@@TITLE@@', self.title_block(lang), 1), lang, values)
            # a citation macro followed by a space would swallow it (\refX text): add {} after it
            tex = re.sub(r'(\\ref[A-Z][A-Za-z]*)(?= [^\s])', r'\1{}', tex)
            path = os.path.join(ROOT, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(tex)
            if self.kind == 'seminar':
                write_solutions_wrapper(path, lang, self.n)
            print(rel, tex.count('\\begin{frame}'), 'frames')
            out.append(path)
        if glossary:
            run_acronyms(self.n)
        return out


def write_solutions_wrapper(path, lang, n):
    name = os.path.basename(path)[:-4]
    sol = (f'% Instructor version of Seminar {n} (with solutions) -- not published; see .gitignore\n' if lang == 'en'
           else f'% Versiunea profesorului pentru Seminarul {n} (cu rezolvări) -- nu se publică; vezi .gitignore\n')
    with open(os.path.join(os.path.dirname(path), name + '_solutions.tex'), 'w', encoding='utf-8') as f:
        f.write(sol + '\\newif\\ifsolutions\n\\solutionstrue\n\\input{' + name + '}\n')


def run_acronyms(*chapters):
    """Glosarul de acronime (dupa pagina de titlu) + legaturile catre Anexa/capitole (appendix_links.py)."""
    subprocess.run([sys.executable, os.path.join(HERE, 'acronyms.py')] + [str(c) for c in chapters], check=True)


# =============================================================================
# CONVERSIA UNUI DECK VECHI (preambul copiat in fisier) LA NOUL FLUX
# =============================================================================
def convert_legacy(src_path, chapter, lang, kind='lecture', subtitle=None, replace=()):
    """Pastreaza tot ce este dupa \\begin{document}; inlocuieste preambulul inline si blocul de titlu cu
    preambulul comun + titlul standard. `replace`: perechi (vechi, nou) aplicate corpului. Idempotent."""
    s = open(src_path, encoding='utf-8').read().replace('\r\n', '\n')
    i = s.index('\\begin{document}')
    body = s[i:]
    body = re.sub(r'\n*% BEGIN-ACRONYMS.*?% END-ACRONYMS\n+', '\n', body, flags=re.S)
    for a, b in replace:
        body = body.replace(a, b)
    # macro-urile proprii ale deck-ului vechi care nu sint in preambulul comun
    pre = s[:i]
    own = []
    shared = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
    for m in re.finditer(r'^\\(?:newcommand|renewcommand|providecommand)\{(\\[A-Za-z]+)\}.*$', pre, flags=re.M):
        name = m.group(1)
        if ('{' + name + '}') not in shared and 'APPLINKS-MACROS' not in m.group(0) and name not in ('\\coursename', '\\qlurl'):
            own.append(m.group(0))
    d = Deck(chapter, kind, subtitle=subtitle, generator=os.path.basename(sys.argv[0]) or 'ats_build.py')
    head = d.head(lang).replace('GENERATED by', 'CONVERTED by').replace('GENERAT de', 'CONVERTIT de')
    head = head.replace('-- edit the generator, not this file.', '-- from the older deck; edit this file or move it to a generator.')
    head = head.replace('-- modificați generatorul, nu acest fișier.', '-- din deck-ul vechi; se editează direct sau se mută într-un generator.')
    macros = d.chapter_macros() + ('\n% macro-uri preluate din deck-ul vechi\n' + '\n'.join(own) + '\n' if own else '')
    out = head + macros + d.title_block(lang) + '\n' + body
    dst = os.path.join(ROOT, deck(chapter, kind, lang))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(out)
    if kind == 'seminar':
        write_solutions_wrapper(dst, lang, chapter)
    print(os.path.relpath(dst, ROOT), out.count('\\begin{frame}'), 'frames (converted from', os.path.relpath(src_path, ROOT) + ')')
    return dst


# =============================================================================
# COMPILARE
# =============================================================================
def compile_tex(path, runs=2):
    """pdflatex de `runs` ori in folderul fisierului; intoarce (erori, overfull vbox, pagini)."""
    d, f = os.path.dirname(path), os.path.basename(path)
    for _ in range(runs):
        subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', f], cwd=d,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log = open(os.path.join(d, f[:-4] + '.log'), encoding='latin-1').read()
    errors = len(re.findall(r'^! ', log, flags=re.M))
    vbox = len(re.findall(r'Overfull \\vbox', log))
    m = re.search(r'Output written on .*?\((\d+) pages?', log.replace('\n', ''), flags=re.S)
    return errors, vbox, int(m.group(1)) if m else 0


def compile_chapter(chapter):
    ok = True
    for p, lang, kind, n in new_decks(chapters={str(chapter)}):
        targets = [p] + ([p[:-4] + '_solutions.tex'] if kind == 'seminar' else [])
        for t in targets:
            e, v, pages = compile_tex(t)
            ok &= e == 0
            print(f'{os.path.relpath(t, ROOT)}: {pages} pages, {e} errors, {v} overfull vbox')
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'compile':
        sys.exit(0 if all(compile_chapter(int(c)) for c in a[1:]) else 1)
    elif a and a[0] == 'convert':
        convert_legacy(os.path.abspath(a[1]), int(a[2]), a[3], kind=a[4] if len(a) > 4 else 'lecture')
    else:
        print(__doc__)
