"""
ats_notebook.py -- common framework of the ATS notebook builders (English only, Colab-ready)
===========================================================================================
The same pattern as the MFM builders (notebooks/build_notebooks_chN.py), reduced to English: ATS notebooks are
published in English only. A chapter builder looks like this:

    from ats_notebook import md, code, common_cells, build, src
    import generate_all_charts as g                       # Quantlets/Ch_NN (sys.path set by chapter_paths)
    LECTURE = [md('# Advanced Time Series Analysis and Forecasting — Chapter N: ...'), *common_cells(),
               md('## 1. ...'), code(src(g.fig_x) + '\\n\\nfig_x()')]
    build(LECTURE, N, 'lecture')                           # notebooks/EN/chapterN_lecture_notebook.ipynb
    build(SEMINAR, N, 'seminar')                           # notebooks/EN/chapterN_seminar_notebook.ipynb

Every notebook gets: the Colab badge (first cell), the title, the Colab banner "Save a copy in Drive" and the
optional Drive-save cell (add_colab_banner.py), the imports, the chart style (ats_style.py) and the data loader
(ats_data.py) as self-contained code (no local imports, so it runs in Colab).
Seminar notebooks: exercise headings carry [Solved] / [Proposed]; solution cells start with '# Solution'; answer
functions of [Proposed] exercises go in a cell that starts with '# [solutions only]'. After executing the full
notebook, python3 notebooks/split_seminar_notebooks.py N writes the student version (public) and the
_solutions copy (git-ignored), and splits the seminar Quantlets (private copy in ../instructor).

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import inspect
import os
import sys

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'Quantlets', 'common'))
sys.path.insert(0, HERE)
from ats_quantlets import IMPORTS, MARKER, data_cell, style_cell   # noqa: E402
import add_colab_banner                                           # noqa: E402

COLAB = 'https://colab.research.google.com/github/danpele/Advanced-Time-Series/blob/main/notebooks'


def chapter_paths(n):
    """Put Quantlets/Ch_NN on sys.path (the chapter scripts whose code goes into the notebooks)."""
    p = os.path.join(ROOT, 'Quantlets', f'Ch_{n:02d}')
    sys.path.insert(0, p)
    return p


def src(*objs):
    return '\n\n\n'.join(inspect.getsource(o).rstrip() for o in objs)


def md(text):
    return ('md', text)


def code(text):
    return ('code', text)


def badge(path):
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}/{path})"


def common_cells(install=''):
    """Imports, chart style and data loader (the same in every notebook)."""
    cells = [code(install)] if install else []
    return cells + [code(IMPORTS),
                    md('## Chart style\n\n- Transparent background, legend below the plot, course palette.'),
                    code(style_cell()),
                    md('## Data\n\n- Daily market data from EODHD, saved in `data/market` of the ATS repository; '
                       'EUR/RON is the official BNR reference rate.\n'
                       '- Macroeconomic series: FRED (St. Louis Fed), Eurostat and the classic data sets of statsmodels.\n'
                       '- Returns in %: $r_t = 100(\\ln P_t - \\ln P_{t-1})$; each series on its own calendar.'),
                    code(data_cell())]


def build(cells, n, kind):
    """Write notebooks/EN/chapter{n}_{kind}_notebook.ipynb and add the Colab banner."""
    path = f'EN/chapter{n}_{kind}_notebook.ipynb'
    nb = nbf.v4.new_notebook()
    out = [nbf.v4.new_markdown_cell(badge(path))]
    for typ, text in cells:
        out.append(nbf.v4.new_markdown_cell(text) if typ == 'md' else nbf.v4.new_code_cell(text))
    nb['cells'] = out
    nb['metadata'] = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                      'language_info': {'name': 'python'}, 'ats': dict(MARKER, chapter=n, kind=kind)}
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    nbf.write(nb, full)
    add_colab_banner.add(full)
    print('built', path)
    return full
