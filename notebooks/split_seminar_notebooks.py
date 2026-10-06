r"""
split_seminar_notebooks.py -- versiunea pentru studenti vs. versiunea completa (profesor)  [ATS, preluat din MFM]
=====================================================================================
Pentru fiecare notebook de seminar executat (cu rezolvari):
  * copia completa se salveaza ca <nume>_solutions.ipynb (exclusa din git, .gitignore);
  * la calea originala (legata pe site) ramane versiunea pentru studenti:
    cerinte + celulele de pregatire (importuri, date, functii date);
    - PROBLEMELE REZOLVATE (titlu cu "[Solved]" / "[Rezolvat]") raman complete, cu cod si rezultate;
    - la PROBLEMELE PROPUSE, in locul rezolvarii apare o celula goala, fara rezultate si fara raspunsuri.

MARCAJE "DOAR IN REZOLVARI" in celulele de cod (pentru functiile care rezolva probleme [Proposed] si sunt
definite in celulele de pregatire, ex. "Seminar functions"):
    # [solutions only]                 ca PRIMA linie a unei celule: celula lipseste integral din versiunea
                                       pentru studenti (fara celula goala in locul ei);
    # >>> [solutions only]  ...  # <<< [solutions only]
                                       blocul dintre marcaje (inclusiv) lipseste din celula;
    ... cod ...  # [solutions only]    orice alta linie marcata lipseste din celula.
  (echivalent in romana: [doar în rezolvări]). Constructorii (build_notebooks_chN.py) pun functiile-raspuns ale
  problemelor propuse intr-o celula separata care incepe cu "# [solutions only]", imediat dupa celula de functii;
  versiunea completa (_solutions) le defineste si ruleaza integral.

Notebook-urile ATS sint doar in engleza (notebooks/EN/chapterN_seminar_notebook.ipynb).
Rulare (dupa build + executie):  python3 notebooks/split_seminar_notebooks.py [N ...]

QUANTLET-URILE DE SEMINAR (Quantlets/Ch_NN/ATS_chN_seminar*, ATS_chN_sem_*), publice pe GitHub:
  la sfarsit, scriptul apeleaza split_quantlet_seminars.run(...), care
    * copiaza versiunile complete (notebook cu rezolvari, graficele-raspuns, seminarN.py, semN_results.json)
      in folderul PRIVAT  ../instructor/Quantlets/Ch_NN/  (in afara depozitului git);
    * inlocuieste notebook-ul public cu versiunea pentru studenti (aceeasi impartire ca mai sus);
    * sterge din folderul public graficele-raspuns ale problemelor [Proposed] si fisierele de rezultate.
  Dupa ORICE rulare a Quantlets/Ch_NN/build_quantlets.py (care rescrie notebook-ul complet) rulati din nou:
      python3 notebooks/split_quantlet_seminars.py [N ...]      (sau acest script)
  Verificare:  python3 notebooks/split_quantlet_seminars.py --check
"""

import os
import re
import copy
import nbformat

HERE = os.path.dirname(os.path.abspath(__file__))

# notebook -> limba: descoperite automat (doar EN)
import glob as _glob
def discover(chapters=None):
    out = {}
    for f in sorted(_glob.glob(os.path.join(HERE, 'EN', 'chapter*_seminar_notebook.ipynb'))):
        if f.endswith('_solutions.ipynb'):
            continue
        n = re.search(r'chapter(\d+)_', os.path.basename(f)).group(1)
        if chapters and n not in chapters:
            continue
        out[os.path.relpath(f, HERE)] = 'en'
    return out


PLACEHOLDER = {'en': '# Your code here\n', 'ro': '# Codul vostru aici\n'}
NOTE = {'en': '> The solutions are discussed in the seminar.',
        'ro': '> Rezolvările se discută la seminar.'}

# celule de cod care sunt rezolvari (prima linie)
SOLUTION_CODE = re.compile(r'^\s*#\s*(Solution|Solu[țt]ie|Rezolvare|Reference analysis|Analiz[aă] de referin|A\d+\b)', re.I)
# celule markdown care anunta o rezolvare sau contin un raspuns
SOLUTION_MD = re.compile(r'^\s*(#+\s*)?(\*\*)?\s*(Solution|Solu[țt]ie|Rezolvare|Discussion|Discu[țt]ie|Interpretation of the result|Interpretarea rezultatului)\b', re.I)
# titluri de exercitii / parti: deschid o sectiune noua
HEADING = re.compile(r'^\s*#{1,3}\s')
# linii marcate care apar doar in versiunea completa (raspunsuri ale problemelor propuse)
SOLUTIONS_ONLY = re.compile(r'\[(solutions only|doar în rezolvări)\]')

# celula intreaga doar in rezolvari (prima linie) si blocuri delimitate
SOLUTIONS_ONLY_CELL = re.compile(r'^\s*#\s*\[(solutions only|doar în rezolvări)\]')
SOLUTIONS_ONLY_BEGIN = re.compile(r'^\s*#\s*>>>\s*\[(solutions only|doar în rezolvări)\]')
SOLUTIONS_ONLY_END = re.compile(r'^\s*#\s*<<<\s*\[(solutions only|doar în rezolvări)\]')


def strip_solutions_only(src):
    """Codul unei celule fara partile marcate "doar in rezolvari"; None daca celula intreaga este marcata."""
    first = next((l for l in src.split('\n') if l.strip()), '')
    if SOLUTIONS_ONLY_CELL.match(first):
        return None
    if not SOLUTIONS_ONLY.search(src):
        return src
    out, skip = [], False
    for l in src.split('\n'):
        if SOLUTIONS_ONLY_BEGIN.match(l):
            skip = True
            continue
        if SOLUTIONS_ONLY_END.match(l):
            skip = False
            continue
        if skip or SOLUTIONS_ONLY.search(l):
            continue
        out.append(l)
    return re.sub(r'\n{4,}', '\n\n\n', '\n'.join(out))


def wrap_solutions_only(code, names, note='answers a Proposed exercise: instructor version only'):
    """Pentru constructori: incadreaza definitiile de nivel superior `names` (functii/clase) din `code` intre
    '# >>> [solutions only]' si '# <<< [solutions only]', ca make_student sa le scoata din versiunea pentru studenti.
    Folosit cand functiile-raspuns sunt in mijlocul unei celule comune (ex. instrumentele cursului)."""
    import ast
    names = set(names)
    lines = code.split('\n')
    found, spans = set(), []
    for node in ast.parse(code).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in names:
            start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
            spans.append((start, node.end_lineno))
            found.add(node.name)
    missing = names - found
    if missing:
        raise ValueError(f'wrap_solutions_only: not found {sorted(missing)}')
    for start, end in sorted(spans, reverse=True):
        lines[end:end] = ['# <<< [solutions only]']
        lines[start:start] = [f'# >>> [solutions only] {note}']
    return '\n'.join(lines)


# marcaj pentru problemele rezolvate (raman complete in versiunea pentru studenti)
SOLVED = re.compile(r'\[(Solved|Rezolvat[aă]?)\]', re.I)


def split(path, lang):
    full = nbformat.read(path, as_version=4)
    sol_path = path.replace('.ipynb', '_solutions.ipynb')
    # pornind dintr-un _solutions existent, butonul trimite la el: il readucem la notebook-ul studentilor
    full.cells[0].source = full.cells[0].source.replace(os.path.basename(sol_path), os.path.basename(path))
    sol = copy.deepcopy(full)             # butonul Colab al copiei complete trimite la ea insasi
    sol.cells[0].source = sol.cells[0].source.replace(os.path.basename(path), os.path.basename(sol_path))
    nbformat.write(sol, sol_path)

    student = make_student(full, lang)
    nbformat.write(student, path)
    n_ph = sum(1 for c in student.cells if c.cell_type == 'code' and c.source in PLACEHOLDER.values())
    print(f'{os.path.relpath(path, HERE)}: {len(student.cells)} cells, {n_ph} empty exercise cells; '
          f'full -> {os.path.basename(sol_path)}')


def make_student(full, lang):
    """Versiunea pentru studenti a unui notebook complet (fara a scrie nimic pe disc)."""
    cells, in_solution, placed, solved = [], False, False, False
    for c in full.cells:
        src = c.source
        if c.cell_type == 'markdown' and HEADING.match(src):
            solved = bool(SOLVED.search(src.split('\n')[0]))
        if solved:                      # problema rezolvata: se pastreaza integral
            cc = copy.deepcopy(c)
            if cc.cell_type == 'code' and SOLUTIONS_ONLY.search(cc.source):
                stripped = strip_solutions_only(cc.source)
                if stripped is None:
                    continue
                cc.source = stripped
                cc.outputs, cc.execution_count = [], None
            cells.append(cc)
            in_solution, placed = False, False
            continue
        if c.cell_type == 'markdown':
            if SOLUTION_MD.match(src):
                in_solution, placed = True, False
                continue
            if HEADING.match(src):
                in_solution, placed = False, False
            cells.append(copy.deepcopy(c))
            continue
        # cod
        is_solution = in_solution or bool(SOLUTION_CODE.match(src))
        if is_solution:
            if not placed:
                cells.append(nbformat.v4.new_code_cell(PLACEHOLDER[lang]))
                placed = True
            continue
        stripped = strip_solutions_only(src)
        if stripped is None:            # functii-raspuns ale problemelor propuse: lipsesc la studenti
            continue
        cc = copy.deepcopy(c)
        cc.source = stripped
        cc.outputs, cc.execution_count = [], None
        cells.append(cc)
        placed = False

    student = copy.deepcopy(full)
    student.cells = cells
    # nota la inceput, dupa titlu
    idx = next((i for i, c in enumerate(cells) if c.cell_type == 'markdown' and c.source.lstrip().startswith('# ')), 0)
    student.cells.insert(idx + 1, nbformat.v4.new_markdown_cell(NOTE[lang]))
    meta = student.metadata.get('ats')
    student.metadata['ats'] = dict(meta if isinstance(meta, dict) else {}, student_version=True)
    return student


if __name__ == '__main__':
    import sys
    # python3 notebooks/split_seminar_notebooks.py        -> toate capitolele
    # python3 notebooks/split_seminar_notebooks.py 4 5    -> doar capitolele 4 si 5
    for rel, lang in discover(set(sys.argv[1:]) or None).items():
        p = os.path.join(HERE, rel)
        sol = p.replace('.ipynb', '_solutions.ipynb')
        cur = nbformat.read(p, as_version=4)
        already_split = any(c.cell_type == 'code' and c.source in PLACEHOLDER.values() for c in cur.cells)
        if already_split:
            # notebook-ul de la cale este deja versiunea pentru studenti: pornim de la versiunea completa
            if not os.path.exists(sol):
                raise SystemExit(f'{rel}: deja impartit, dar lipseste {os.path.basename(sol)}')
            nbformat.write(nbformat.read(sol, as_version=4), p)
        # altfel: notebook proaspat construit (complet) -> il folosim pe el, nu vechiul _solutions
        split(p, lang)

    # Quantlet-urile de seminar (public pe GitHub): aceeasi impartire; versiunile complete -> folderul privat
    # al profesorului (vezi split_quantlet_seminars.py).
    import split_quantlet_seminars
    split_quantlet_seminars.run(sorted({int(a) for a in sys.argv[1:]}) or None)
