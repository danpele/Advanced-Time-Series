"""
ats_quantlets.py -- builder of ATS Quantlet folders (Metainfo.txt + self-contained Colab notebook + charts)
=========================================================================================================
The same scheme as the MFM Quantlets. Each chapter has Quantlets/Ch_NN/build_quantlets.py with a list QUANTLETS of
dictionaries and calls build_all(QUANTLETS, chapter=N, ...). For each Quantlet:

    Quantlets/Ch_NN/ATS_chN_<name>/
        Metainfo.txt             Name of QuantLet, Published in, Description, Keywords, Author, Submitted,
                                 Datafile, Output  (the QuantLet.com format)
        ATS_chN_<name>.ipynb     self-contained notebook (Colab badge, imports, style, data loader, code, run);
                                 the code is taken with inspect.getsource from the chapter scripts, so the
                                 Quantlets stay in sync with the slides
        <chart>.pdf / .png       copies of the charts from charts/

Quantlet dictionary:
    name      'ATS_ch0_markets'                        (folder and notebook name)
    desc      one paragraph: what is computed, on which data
    keywords  comma-separated keywords
    funcs     functions (or classes) whose source goes into the notebook
    run       code that runs the analysis and draws the charts
    charts    chart names in charts/ (without extension)
    extra     other files from Quantlets/Ch_NN copied into the folder (CSV tables)
    consts    optional lines of code placed before the functions
    data      optional Datafile text (default: DATA of the chapter)

After building, run  python3 notebooks/add_colab_banner.py  (Colab banner + Drive-save cell) and, for seminar
Quantlets, python3 notebooks/split_quantlet_seminars.py N  (student version public, full version private).

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import inspect
import os
import shutil
import sys

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import ats_data as D        # noqa: E402
import ats_style as ST      # noqa: E402

CHART_DIR = os.path.join(REPO, 'charts')
COLAB = 'https://colab.research.google.com/github/danpele/Advanced-Time-Series/blob/main/Quantlets'
PUBLISHED = 'Advanced Time Series Analysis and Forecasting (ATS)'
AUTHOR = 'Daniel Traian Pele'
DATA = 'Course data: daily market data from EODHD (data/manifest.csv of the ATS repository); public macro data from FRED, Eurostat, BNR; statsmodels data sets'
MARKER = {'build': 'ats-pipeline'}        # notebook metadata of the new pipeline (add_colab_banner.py uses it)

IMPORTS = """import os
import re
import json
import urllib.request
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from scipy import optimize
from scipy import stats
import warnings
warnings.filterwarnings('ignore')"""


def src(*objs):
    return '\n\n\n'.join(inspect.getsource(o).rstrip() for o in objs)


def module_body(mod, start, end=None):
    """The source of a module between two markers (e.g. constants block)."""
    s = inspect.getsource(mod)
    i = s.index(start)
    j = s.index(end, i) if end else len(s)
    return s[i:j].rstrip()


def style_cell():
    """Chart style (ats_style.py), with save_fig writing into the current folder (or OUT_DIR in Colab)."""
    body = module_body(ST, '# Palette', '_HERE = ')
    funcs = src(ST.apply, ST.legend_outside_bottom, ST.fig_legend_bottom, ST._is_grey, ST.check_no_grey)
    return (body + '\n\n\n' + funcs + '''


def save_fig(name, out_dir=None, show=True):
    """Save the figure as transparent PDF and PNG (OUT_DIR if defined, else the current folder), then show it."""
    d = out_dir or globals().get('OUT_DIR', '.')
    plt.savefig(os.path.join(d, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    plt.savefig(os.path.join(d, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    if show:
        plt.show()
    plt.close()


apply()
# the chapter scripts call the style as st.<name> (import ats_style as st): the same names here
import types
st = types.SimpleNamespace(COL=COL, PALETTE=PALETTE, MainBlue=MainBlue, IDAred=IDAred, Forest=Forest, Amber=Amber,
                           Orange=Orange, Purple=Purple, Teal=Teal, Crimson=Crimson, DarkText=DarkText, apply=apply, legend_outside_bottom=legend_outside_bottom,
                           fig_legend_bottom=fig_legend_bottom, save_fig=save_fig, check_no_grey=check_no_grey)''')


def data_cell():
    """The data loader (ats_data.py) without local file dependencies: local data/market if present, else GitHub;
    the Oxford-Man realized library from a local copy if present, else from the Internet Archive."""
    consts = module_body(D, 'END = ', '_CACHE = {}')
    return ("REPO_RAW = 'https://raw.githubusercontent.com/danpele/Advanced-Time-Series/main/data/market/'\n"
            "# local copy of the course data, if the notebook runs inside the repository\n"
            "MARKET_DIR = next((os.path.join(d, 'data', 'market') for d in ('.', '..', '../..', '../../..')\n"
            "                   if os.path.isdir(os.path.join(d, 'data', 'market'))), '')\n"
            "# local copy of the Oxford-Man realized library, if present (not distributed; read_omi downloads it)\n"
            "REALIZED_DIR = next((os.path.join(d, 'data', 'realized') for d in ('.', '..', '../..', '../../..')\n"
            "                     if os.path.isdir(os.path.join(d, 'data', 'realized'))), '')\n"
            + consts + "\n_CACHE = {}\n\n\n"
            + src(D.read_market, D.read_omi, D.read_reference_rate, D.load_close, D.load_ohlc, D.log_returns, D.simple_returns,
                  D.load_panel, D.periods_per_year, D.read_fred, D._eurostat_period, D.read_eurostat,
                  D.load_statsmodels))


def metainfo(q, data=DATA, submitted=''):
    out = [c + '.pdf' for c in q.get('charts', [])] + q.get('extra', [])
    return (f"Name of QuantLet: '{q['name']}'\n\n"
            f"Published in: '{PUBLISHED}'\n\n"
            f"Description: '{q['desc']}'\n\n"
            f"Keywords: '{q['keywords']}'\n\n"
            f"Author: '{AUTHOR}'\n\n"
            f"Submitted: '{submitted}'\n\n"
            f"Datafile: '{q.get('data', data)}'\n\n"
            f"Output: '{', '.join(out) if out else 'printed tables'}'\n")


def notebook(q, chapter, chapter_title, install=''):
    ch = f'Ch_{chapter:02d}'
    cells = [
        nbf.v4.new_markdown_cell(f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
                                 f"({COLAB}/{ch}/{q['name']}/{q['name']}.ipynb)"),
        nbf.v4.new_markdown_cell(f"# {q['name']}\n\n{q['desc']}\n\n*{PUBLISHED}, Chapter {chapter}: {chapter_title}. "
                                 f"Author: {AUTHOR}.*"),
    ]
    if install:
        cells.append(nbf.v4.new_code_cell(install))
    cells += [nbf.v4.new_code_cell(IMPORTS),
              nbf.v4.new_markdown_cell('## Chart style'), nbf.v4.new_code_cell(style_cell()),
              nbf.v4.new_markdown_cell('## Data'), nbf.v4.new_code_cell(data_cell())]
    if q.get('consts') or q.get('funcs'):
        cells += [nbf.v4.new_markdown_cell('## Analysis'),
                  nbf.v4.new_code_cell('\n\n'.join(q.get('consts', []) + ([src(*q['funcs'])] if q.get('funcs') else [])))]
    cells += [nbf.v4.new_markdown_cell('## Run'), nbf.v4.new_code_cell(q['run'])]
    for c in q.get('charts', []):
        cells.append(nbf.v4.new_markdown_cell(f"![{c}](./{c}.png)\n\nOutput: `{c}.pdf`"))
    nb = nbf.v4.new_notebook()
    nb['cells'] = cells
    nb['metadata'] = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                      'language_info': {'name': 'python'}, 'ats': dict(MARKER, chapter=chapter)}
    return nb


def build(q, chapter, chapter_title, ql_dir, data=DATA, submitted='', install=''):
    folder = os.path.join(ql_dir, q['name'])
    os.makedirs(folder, exist_ok=True)
    nbf.write(notebook(q, chapter, chapter_title, install), os.path.join(folder, q['name'] + '.ipynb'))
    with open(os.path.join(folder, 'Metainfo.txt'), 'w', encoding='utf-8') as f:
        f.write(metainfo(q, data, submitted))
    for c in q.get('charts', []):
        for ext in ('pdf', 'png'):
            shutil.copy(os.path.join(CHART_DIR, f'{c}.{ext}'), folder)
    for e in q.get('extra', []):
        shutil.copy(os.path.join(ql_dir, e), folder)
    print('built', q['name'])


def build_all(quantlets, chapter, chapter_title, ql_dir, data=DATA, submitted='', install='', only=None):
    only = only if only is not None else sys.argv[1:]
    for q in quantlets:
        if not only or q['name'] in only:
            build(q, chapter, chapter_title, ql_dir, data, submitted, install)
