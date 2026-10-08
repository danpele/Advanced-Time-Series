r"""
split_quantlet_seminars.py -- Quantlet-urile de seminar: versiunea pentru studenti (public) vs. completa (profesor)
=================================================================================================================
Decizia profesorului: studentii nu au acces la rezolvarile problemelor [Proposed] / [Propus].
Quantlet-urile de seminar sunt publice (github.com/danpele/Advanced-Time-Series, Quantinar), deci, pentru fiecare capitol 0-16:

  1. COPIA COMPLETA -> folderul privat, in afara depozitului git:
         <ATS>/../instructor/Quantlets/Ch_NN/<folder>/            (notebook complet + toate graficele + rezultate)
         <ATS>/../instructor/Quantlets/Ch_NN/seminarN.py, semN_results.json, ...   (cod si rezultate de seminar)
     Notebook-ul si Metainfo.txt se copiaza doar cand folderul public contine inca versiunea completa
     (proaspat construita de build_quantlets.py); o versiune pentru studenti nu suprascrie niciodata copia completa.

  2. VERSIUNEA PENTRU STUDENTI in folderul public (STUDENT_FOLDERS):
     notebook-ul = notebooks/EN/chapterN_seminar_notebook.ipynb, adica rezultatul aceleiasi impartiri ca in
     split_seminar_notebooks.py (HEADING / SOLVED / SOLUTION_MD / SOLUTION_CODE / PLACEHOLDER / SOLUTIONS_ONLY):
       - Setup, date, functii date: pastrate;
       - problemele [Solved]: complete, cu cod si rezultate;
       - problemele [Proposed]: o singura celula goala "# Your code here", fara rezultate;
     cu butonul Colab indreptat spre Quantlet. Metainfo.txt este rescris (Description/Output fara rezultatele
     problemelor propuse). Graficele-raspuns ale problemelor [Proposed] si fisierele de rezultate se sterg.

  3. FOLDERE NUMAI PENTRU PROFESOR (INSTRUCTOR_ONLY): referinte pentru Part C / parti mixte, fara legatura
     vizibila in prezentarea pentru studenti; se copiaza in folderul privat si sunt excluse din git (.gitignore).

Graficele-raspuns ale problemelor [Proposed] (chN_sem_<id>*): se citesc din prezentarea EN pentru studenti
EN/Seminars/seminarN_*.tex. Un grafic este privat daca NU apare in versiunea pentru studenti (doar in blocuri
\\ifsolutions ... \\fi sau \\solonly{...}) si nu apartine unei probleme [Solved] (dupa cadrul in care apare sau,
daca nu apare deloc, dupa ID-ul din nume: a2 -> A2, b1x -> B1 Extended, a56 -> A5+A6). Lista explicita este in
.gitignore (blocul "Proposed-exercise answer charts"); --gitignore o regenereaza.

Rulare:
    python3 notebooks/split_quantlet_seminars.py            # toate capitolele (si din split_seminar_notebooks.py)
    python3 notebooks/split_quantlet_seminars.py 5 8        # doar capitolele 5 si 8
    python3 notebooks/split_quantlet_seminars.py --check    # verificare: nimic privat in folderele publice / in git
    python3 notebooks/split_quantlet_seminars.py --gitignore  # tipareste blocul .gitignore cu graficele private
    python3 notebooks/split_quantlet_seminars.py --write-gitignore  # il scrie direct in .gitignore
De rulat dupa ORICE Quantlets/Ch_NN/build_quantlets.py (care rescrie notebook-ul complet si graficele).
"""

import os
import re
import sys
import glob
import copy
import shutil
import subprocess
import nbformat

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
INSTRUCTOR = os.path.join(os.path.dirname(REPO), 'instructor', 'Quantlets')
sys.path.insert(0, HERE)
from split_seminar_notebooks import PLACEHOLDER, split as split_course_notebook   # noqa: E402

CHAPTERS = range(17)   # ATS chapters 0-16

# folderele de seminar mixte sau de Part C fara legatura vizibila pentru studenti -> doar la profesor
INSTRUCTOR_ONLY = {
    # N: ['ATS_chN_sem_partc'],     # exemplu: analiza de referinta pentru Part C
}

# fisiere de rezultate / cod de seminar (nivelul Ch_NN si folderele de seminar): private
RESULT_FILE = re.compile(r'^((sem|seminar)\d+_\w*\.json|ch\d+_sem_\w*\.(csv|json|npz)|ch\d+_seminar_\w+\.json)$')
SEMINAR_CODE = re.compile(r'^(seminar\d+(_charts)?\.py|c3_reference\.py)$')

ID_RE = r'([A-C]\d+[a-z]?(?:\s+Extended)?)'


# ----------------------------------------------------------------------------- prezentarea pentru studenti
def _deck(n):
    sys.path.insert(0, os.path.join(REPO, 'latex'))
    from ats_chapters import deck, is_new_pipeline
    p = os.path.join(REPO, deck(n, 'seminar', 'en'))
    return open(p, encoding='utf-8').read() if is_new_pipeline(p) else ''


def exercise_status(n):
    """ID -> 'Proposed' / 'Solved', din titlurile cadrelor."""
    st = {}
    for m in re.finditer(r'\\begin\{frame\}(?:\[[^\]]*\])?\{([^\n]*)', _deck(n)):
        mm = re.match(r'\s*' + ID_RE + r'\b[^\[]*\[(Proposed|Solved)\]', m.group(1))
        if mm:
            st[mm.group(1)] = mm.group(2)
    return st


def _deck_refs(n):
    """(nume_grafic, vizibil_pentru_studenti, id_exercitiu) pentru fiecare aparitie chN_sem_* in prezentare."""
    text = '\n'.join(re.sub(r'(?<!\\)%.*', '', line) for line in _deck(n).split('\n'))
    tok = re.compile(r'\\newif\\if\w+|\\if(?!thenelse|toggle)(\w+)|\\else\b|\\fi\b|\\solonly\{'
                     r'|\\begin\{frame\}(?:\[[^\]]*\])?\{([^\n]*)|(ch\d+_sem_[A-Za-z0-9_]+)')
    out, stack, solonly, cur = [], [], [], None
    for m in tok.finditer(text):
        t = m.group(0)
        while solonly and m.start() >= solonly[-1]:
            solonly.pop()
        if t.startswith('\\newif'):
            continue
        if t.startswith('\\solonly{'):
            d, j = 1, m.end()
            while d and j < len(text):
                d += {'{': 1, '}': -1}.get(text[j], 0) if text[j - 1] != '\\' else 0
                j += 1
            solonly.append(j)
        elif m.group(1) is not None:
            stack.append([m.group(1), True])
        elif t.startswith('\\else'):
            if stack:
                stack[-1][1] = not stack[-1][1]
        elif t.startswith('\\fi'):
            if stack:
                stack.pop()
        elif m.group(2) is not None:
            mm = re.match(r'\s*' + ID_RE + r'\b', m.group(2))
            cur = mm.group(1) if mm else None
        else:
            sol = any(name == 'solutions' and branch for name, branch in stack) or bool(solonly)
            out.append((m.group(3), not sol, cur))
    return out


def _ids_in_name(n, name):
    tail = re.match(rf'ch{n}_sem_(.*)', name).group(1)
    m2 = re.match(r'([abc]\d+)([abc]\d+)', tail)                       # a1a2 -> A1, A2
    if m2:
        return [m2.group(1).upper(), m2.group(2).upper()]
    m = re.match(r'([abc])(\d+)([a-z0-9]*)', tail)
    if not m:
        return []
    L, d, rest = m.group(1).upper(), m.group(2), m.group(3)
    if rest == '' and len(d) == 2 and d[0] != '1':                     # a56 -> A5, A6
        return [L + d[0], L + d[1]]
    return [L + d + (' Extended' if rest.startswith('x') else '')]


def private_charts(n, names):
    """Graficele-raspuns ale problemelor [Proposed] dintre `names` (nume fara extensie)."""
    st, refs, out = exercise_status(n), _deck_refs(n), set()
    for nm in names:
        if '_sem_primer_' in nm:
            continue                                                   # grafic explicativ din primer: public
        r = [x for x in refs if x[0] == nm]
        if any(v for _, v, _ in r):
            continue                                                   # apare in prezentarea pentru studenti
        owners = {o for _, _, o in r if o} or set(_ids_in_name(n, nm))
        if owners and all(st.get(o, st.get(o.replace(' Extended', ''))) == 'Solved' for o in owners):
            continue                                                   # grafic al unei probleme rezolvate
        out.add(nm)
    return out


def all_sem_chart_names(n):
    pats = [os.path.join(REPO, 'charts', f'ch{n}_sem_*'),
            os.path.join(REPO, 'Quantlets', f'Ch_{n:02d}', '**', f'ch{n}_sem_*')]
    names = set()
    for p in pats:
        for f in glob.glob(p, recursive=True):
            if f.endswith(('.pdf', '.png')):
                names.add(os.path.splitext(os.path.basename(f))[0])
    return names


# ----------------------------------------------------------------------------- foldere
def seminar_folders(n):
    qd = os.path.join(REPO, 'Quantlets', f'Ch_{n:02d}')
    found = sorted(os.path.basename(p) for p in glob.glob(os.path.join(qd, f'ATS_ch{n}_sem*')) if os.path.isdir(p))
    instr = [f for f in INSTRUCTOR_ONLY.get(n, []) if os.path.isdir(os.path.join(qd, f))]
    return [f for f in found if f not in instr], instr


def is_student_version(nb):
    return bool((nb.metadata.get('ats') if isinstance(nb.metadata.get('ats'), dict) else {}).get('student_version')) or any(
        c.cell_type == 'code' and c.source.strip() in {v.strip() for v in PLACEHOLDER.values()} for c in nb.cells)


def _copy_to_instructor(n, folder, full_copy):
    src = os.path.join(REPO, 'Quantlets', f'Ch_{n:02d}', folder)
    dst = os.path.join(INSTRUCTOR, f'Ch_{n:02d}', folder)
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        p = os.path.join(src, f)
        if not os.path.isfile(p):
            continue
        if not full_copy and (f.endswith('.ipynb') or f == 'Metainfo.txt'):
            continue                                                   # nu suprascriem copia completa
        shutil.copy2(p, os.path.join(dst, f))


def _copy_chapter_files(n):
    qd = os.path.join(REPO, 'Quantlets', f'Ch_{n:02d}')
    dst = os.path.join(INSTRUCTOR, f'Ch_{n:02d}')
    os.makedirs(dst, exist_ok=True)
    out = []
    for f in sorted(os.listdir(qd)):
        if os.path.isfile(os.path.join(qd, f)) and (RESULT_FILE.match(f) or SEMINAR_CODE.match(f)):
            shutil.copy2(os.path.join(qd, f), os.path.join(dst, f))
            out.append(f)
    return out


def _student_notebook(n, folder, solved, proposed):
    src = os.path.join(HERE, 'EN', f'chapter{n}_seminar_notebook.ipynb')
    nb = nbformat.read(src, as_version=4)
    if not is_student_version(nb):                                     # build proaspat, inca neimpartit
        split_course_notebook(src, 'en')
        nb = nbformat.read(src, as_version=4)
    nb = copy.deepcopy(nb)
    rel = f'Quantlets/Ch_{n:02d}/{folder}/{folder}.ipynb'
    nb.cells[0].source = re.sub(r'(colab\.research\.google\.com/github/danpele/Advanced-Time-Series/blob/main/)[^)\s]+',
                                r'\g<1>' + rel, nb.cells[0].source)
    idx = next((i for i, c in enumerate(nb.cells) if c.cell_type == 'markdown' and c.source.lstrip().startswith('# ')), 0)
    nb.cells.insert(idx + 1, nbformat.v4.new_markdown_cell(
        f'> Quantlet `{folder}`: student version of the Seminar {n} notebook. '
        f'Solved exercises ({", ".join(solved)}) are shown with code and output; '
        f'the proposed exercises ({", ".join(proposed)}) are not solved here '
        f'(an empty code cell where they need code).'))
    meta = nb.metadata.get('ats')
    nb.metadata['ats'] = dict(meta if isinstance(meta, dict) else {}, student_version=True)
    return nb


def _ids_sorted(ids):
    return sorted(ids, key=lambda s: (s[0], int(re.match(r'[A-C](\d+)', s).group(1)), s))


def _metainfo(path, n, folder, solved, proposed):
    s = open(path, encoding='utf-8').read() if os.path.exists(path) else f"Name of QuantLet: '{folder}'\n"
    desc = (f"Seminar {n} of Advanced Time Series Analysis and Forecasting (ATS), student version: setup, data, helper functions and the "
            f"solved exercises {', '.join(solved)} with code and output. The proposed exercises "
            f"{', '.join(proposed)} are not solved here (an empty code cell where they need code); "
            f"their solutions are discussed in the seminar.")
    charts = sorted(f for f in os.listdir(os.path.dirname(path)) if f.endswith('.pdf'))
    out = ', '.join(charts) if charts else 'none (the notebook draws the charts of the solved exercises)'
    if re.search(r"^Description: .*$", s, flags=re.M):
        s = re.sub(r"^Description: .*$", lambda m: f"Description: '{desc}'", s, flags=re.M)
    else:
        s += f"\nDescription: '{desc}'\n"
    if re.search(r"^Output: .*$", s, flags=re.M):
        s = re.sub(r"^Output: .*$", lambda m: f"Output: '{out}'", s, flags=re.M)
    else:
        s += f"\nOutput: '{out}'\n"
    open(path, 'w', encoding='utf-8').write(s)


def run(chapters=None):
    chapters = list(CHAPTERS) if chapters is None else chapters
    for n in chapters:
        qd = os.path.join(REPO, 'Quantlets', f'Ch_{n:02d}')
        if not os.path.isdir(qd) or not _deck(n):
            continue                                                   # capitol inca nereconstruit in noul flux
        st = exercise_status(n)
        solved = _ids_sorted([k for k, v in st.items() if v == 'Solved'])
        proposed = _ids_sorted([k for k, v in st.items() if v == 'Proposed'])
        priv = private_charts(n, all_sem_chart_names(n))
        student, instr = seminar_folders(n)
        log = []
        for folder in student + instr:
            nbp = os.path.join(qd, folder, f'{folder}.ipynb')
            full = os.path.exists(nbp) and not is_student_version(nbformat.read(nbp, as_version=4))
            _copy_to_instructor(n, folder, full_copy=full)
        for folder in student:
            fd = os.path.join(qd, folder)
            removed = []
            for f in sorted(os.listdir(fd)):
                stem, ext = os.path.splitext(f)
                if (ext in ('.pdf', '.png') and stem in priv) or RESULT_FILE.match(f):
                    os.remove(os.path.join(fd, f))
                    removed.append(f)
            nbformat.write(_student_notebook(n, folder, solved, proposed), os.path.join(fd, f'{folder}.ipynb'))
            _metainfo(os.path.join(fd, 'Metainfo.txt'), n, folder, solved, proposed)
            log.append(f'{folder}: student notebook; removed {len(removed)} files')
        files = _copy_chapter_files(n)
        print(f'ch{n}: ' + '; '.join(log) + (f'; instructor-only: {", ".join(instr)}' if instr else '')
              + (f'; seminar files copied: {len(files)}' if files else ''))


# ----------------------------------------------------------------------------- verificare
def check():
    ok = True
    tracked = subprocess.run(['git', 'ls-files'], cwd=REPO, capture_output=True, text=True).stdout.split('\n')
    for n in CHAPTERS:
        if not os.path.isdir(os.path.join(REPO, 'Quantlets', f'Ch_{n:02d}')) or not _deck(n):
            continue
        priv = private_charts(n, all_sem_chart_names(n))
        st = exercise_status(n)
        student, instr = seminar_folders(n)
        bad_git = [t for t in tracked if os.path.splitext(os.path.basename(t))[0] in priv
                   or (t.startswith(f'Quantlets/Ch_{n:02d}/') and (RESULT_FILE.match(os.path.basename(t))
                       or SEMINAR_CODE.match(os.path.basename(t))))
                   or any(t.startswith(f'Quantlets/Ch_{n:02d}/{f}/') for f in instr)]
        msgs = []
        for folder in student:
            fd = os.path.join(REPO, 'Quantlets', f'Ch_{n:02d}', folder)
            nb = nbformat.read(os.path.join(fd, f'{folder}.ipynb'), as_version=4)
            if not (nb.metadata.get('ats') if isinstance(nb.metadata.get('ats'), dict) else {}).get('student_version'):
                msgs.append(f'{folder}: notebook is NOT the student version')
            sec, seen = None, set()
            for c in nb.cells:
                if c.cell_type == 'markdown' and re.match(r'^\s*#{1,3}\s', c.source):
                    h = c.source.split('\n')[0]
                    mm = re.search(r'#+\s*' + ID_RE + r'\b', h)
                    sec = ('P' if re.search(r'\[(Proposed|Propus)\]', h) else 'S' if re.search(r'\[(Solved|Rezolvat)', h) else None)
                    if sec == 'P' and mm:
                        seen.add(mm.group(1))
                elif c.cell_type == 'code' and sec == 'P' and c.get('outputs'):
                    msgs.append(f'{folder}: outputs in a Proposed section')
            missing = {p for p in st if st[p] == 'Proposed' and ' Extended' not in p} - seen
            if missing:
                msgs.append(f'{folder}: proposed IDs without a notebook section {sorted(missing)} (deck-only tasks)')
            left = [f for f in os.listdir(fd) if os.path.splitext(f)[0] in priv or RESULT_FILE.match(f)]
            if left:
                ok = False
                msgs.append(f'{folder}: private files present {left}')
        if bad_git:
            ok = False
            msgs.append(f'TRACKED private files: {bad_git}')
        print(f'ch{n}: {len(priv)} private charts; ' + ('; '.join(msgs) if msgs else 'OK'))
    print('CHECK', 'PASSED' if ok else 'FAILED')
    return ok


def gitignore_block():
    lines = ['# ---- Proposed-exercise answer charts (instructor only; generated by split_quantlet_seminars.py --gitignore)',
             '# Students must not see the solutions of [Proposed] seminar exercises. Local files stay (instructor PDFs',
             '# need them); full Quantlet versions live in ../instructor/Quantlets (outside the repository).']
    for n in CHAPTERS:
        if not _deck(n):
            continue
        priv = sorted(private_charts(n, all_sem_chart_names(n)))
        if priv:
            lines.append(f'# Seminar {n}')
            lines += [f'{p}.pdf\n{p}.png' for p in priv]
    lines.append('# ---- end of Proposed-exercise answer charts')
    return '\n'.join(lines)


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--check' in args:
        sys.exit(0 if check() else 1)
    elif '--gitignore' in args:
        print(gitignore_block())
    elif '--write-gitignore' in args:                                  # inlocuieste blocul din .gitignore
        gi = os.path.join(REPO, '.gitignore')
        t = open(gi, encoding='utf-8').read()
        t2 = re.sub(r'# ---- Proposed-exercise answer charts.*?# ---- end of Proposed-exercise answer charts',
                    lambda m: gitignore_block(), t, flags=re.S)
        open(gi, 'w', encoding='utf-8').write(t2)
        print('.gitignore', 'updated' if t2 != t else 'unchanged')
    else:
        run(sorted(int(a) for a in args) or None)
