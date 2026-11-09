"""
exercise_links.py -- clickable exercise codes and back buttons in the ATS seminar decks (model: MFM seminar 1)
==============================================================================================================
In every seminar deck (EN + RO; the *_solutions.tex wrappers \\input the same file):
  * the first task frame of each exercise ("A1: ... [Solved]", "B2: ... [Propus]") gets the target ex-A1, ex-B2, ...
    placed inline right after its first "\\item ", followed by \\exback{}: two buttons in the bottom right corner,
    "Back" / "Înapoi" (the viewer's GoBack) and "Exercise list" / "Lista exercițiilor" (to the structure slide);
  * the structure slide "Today's question and seminar structure (2/4)" / "Întrebarea de azi și structura
    seminarului (2/4)" gets the target ex-list inline after its first "\\item " (otherwise the exercise map);
  * every other mention of an exercise code in the body (structure slides, exercise map, "Model: A1", ...) becomes
    \\exlink{ex-A1}{A1}; frame titles, math, \\texttt, \\href, \\quantlet and \\includegraphics lines are left alone.
Idempotent: old links, targets, buttons and macros are removed and rebuilt at every run.
Run (after every seminar build; latex/acronyms.py calls it automatically):
    python3 latex/exercise_links.py          -> all seminars
    python3 latex/exercise_links.py 1 4      -> seminars 1 and 4
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

ID = r'[ABC]\d{1,2}(?:\([a-e](?:--[a-e])?\))?'
TITLE = re.compile(r'^\\begin\{frame\}(?:\[[^\]]*\])?\{(' + ID + r'):.*\}\s*$')   # first frame of each exercise
LIST_TITLES = (re.compile(r"^\\begin\{frame\}\{(?:Întrebarea de azi și structura seminarului|Today's question and seminar structure) \(2/\d+\)\}"),
               re.compile(r'^\\begin\{frame\}\{(?:Harta exercițiilor|Exercise map)\}'))
REF = re.compile(r'(?:(?<=--)|(?<![A-Za-z0-9_\\{-]))(' + ID + r')(?![0-9A-Za-z_])')
PROTECT = re.compile(r'(\$[^$]*\$|\\texttt\{[^}]*\}|\\href\{[^}]*\}\{(?:[^{}]|\{[^{}]*\})*\}|\\atschlinkt?\{[^}]*\}\{[^{}]*\})')
MARK = '  % EXLINKS-MACROS'


def macros(lang):
    back, lst = ('Înapoi', 'Lista exercițiilor') if lang == 'ro' else ('Back', 'Exercise list')
    return (r'\providecommand{\exback}{\begin{tikzpicture}[remember picture,overlay]'
            r'\node[anchor=south east] at ([xshift=-3mm,yshift=7mm]current page.south east)'
            r'{\Acrobatmenu{GoBack}{\beamerreturnbutton{%s}}\ \hyperlink{ex-list}{\beamergotobutton{%s}}};\end{tikzpicture}}' % (back, lst)
            + MARK + '\n' + r'\providecommand{\exlink}[2]{\hyperlink{#1}{\textcolor{MainBlue}{#2}}}' + MARK + '\n')


def strip(s):
    s = re.sub(r'.*' + re.escape(MARK) + r'\n', '', s)
    s = re.sub(r'\\hypertarget\{ex-[A-Za-z0-9]+\}\{\}', '', s)
    s = s.replace('\\exback{}', '')
    s = re.sub(r'\\exlink\{ex-[A-Za-z0-9]+\}\{([^{}]*)\}', r'\1', s)
    return s


def key(code):
    return 'ex-' + re.sub(r'[^A-Za-z0-9]', '', code)


def first_item(lines, i):
    """Index of the first line after the frame title i that holds '\\item ' outside \\solonly / \\ifsolutions."""
    for j in range(i + 1, len(lines)):
        l = lines[j]
        if l.startswith('\\end{frame}'):
            return None
        if '\\solonly' in l or l.strip() == '\\ifsolutions':
            return None
        if '\\item ' in l:
            return j
    return None


def process(path, lang):
    s = strip(open(path, encoding='utf-8').read())
    d = s.find('\\begin{document}')
    head, body = s[:d], s[d:]
    lines = body.split('\n')
    targets, missing = {}, []
    for i, l in enumerate(lines):
        m = TITLE.match(l)
        if m and m.group(1) not in targets:
            if i and lines[i - 1].strip() == '\\ifsolutions':     # instructor-only frame: not in the student deck
                continue
            j = first_item(lines, i)
            if j is None:
                missing.append(m.group(1))
                continue
            targets[m.group(1)] = key(m.group(1))
            lines[j] = lines[j].replace('\\item ', '\\item \\hypertarget{%s}{}\\exback{}' % key(m.group(1)), 1)
    listed = False
    for rx in LIST_TITLES:
        for i, l in enumerate(lines):
            if rx.match(l):
                j = first_item(lines, i)
                if j is not None:
                    lines[j] = lines[j].replace('\\item ', '\\item \\hypertarget{ex-list}{}', 1)
                    listed = True
                break
        if listed:
            break

    def target_for(code):
        if code in targets:
            return targets[code]
        base = re.match(r'[ABC]\d+', code).group(0)
        if base in targets:
            return targets[base]
        c = [k for k in targets if k.startswith(base + '(')]
        return targets[c[0]] if c else None

    def rep(m):
        t = target_for(m.group(1))
        return '\\exlink{%s}{%s}' % (t, m.group(1)) if t else m.group(1)

    out = []
    for l in lines:
        st = l.lstrip()
        if (st.startswith('\\begin{frame}') or st.startswith('%') or st.startswith('\\hypertarget')
                or '\\includegraphics' in l or '\\quantlet' in l or '\\frametitle' in l or '\\section' in l):
            out.append(l)
            continue
        parts = PROTECT.split(l)
        out.append(''.join(p if k % 2 else REF.sub(rep, p) for k, p in enumerate(parts)))
    body = '\n'.join(out)
    s = head + macros(lang) + body
    open(path, 'w', encoding='utf-8').write(s)
    return len(targets), body.count('\\exlink{'), listed, missing


def seminar_decks(chapters=None):
    from ats_chapters import new_decks
    return [(p, lang) for p, lang, kind, n in new_decks(kinds=('seminar',), chapters=chapters)]


if __name__ == '__main__':
    for f, lang in seminar_decks(set(sys.argv[1:]) or None):
        t, k, listed, missing = process(f, lang)
        print(f'{os.path.relpath(f, ROOT)}: {t} exercise targets, {k} links'
              + ('' if listed else '; NO ex-list TARGET') + (f'; no task item for {missing}' if missing else ''))
