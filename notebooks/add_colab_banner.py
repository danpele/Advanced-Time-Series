"""
Adaugă, după titlul fiecărui notebook publicat al noului flux ATS (notebooks/EN și folderele Quantlet construite
cu Quantlets/common/ats_quantlets.py), două celule:
  1. un banner: în Colab, salvați întâi o copie în Drive, altfel modificările se pierd;
  2. o celulă opțională care montează Google Drive și creează MyDrive/ATS/Chapter_N/ pentru rezultate.
Quantlet-urile vechi (fără metadata {"ats": {"build": "ats-pipeline"}}) nu sînt atinse.
Idempotent: celulele poartă metadata {"ats": "colab-banner"} și nu se adaugă de două ori.
Rulare (după orice reconstruire a notebook-urilor sau a Quantlet-urilor):  python3 notebooks/add_colab_banner.py
"""

import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TAG = {'ats': 'colab-banner'}

BANNER = (
    "> **Working in Google Colab? Save your own copy first.**\n"
    "> The Colab link opens a temporary copy: when you close the tab or the session times out, your changes are lost.\n"
    "> Use **File → Save a copy in Drive** (it goes to the *Colab Notebooks* folder of your ASE Google Drive) and work in that copy.\n"
    "> For the team project, **File → Save a copy in GitHub** puts the notebook directly in your team's repository.\n"
    "> Files you create while the notebook runs (CSV, charts) are also temporary: set `SAVE_TO_DRIVE = True` in the next cell to keep them."
)

SAVE_CELL = """# Optional (Colab only): keep the files you create in Google Drive
SAVE_TO_DRIVE = False   # set to True, run this cell and allow access to your Drive

import os
OUT_DIR = '.'
if SAVE_TO_DRIVE:
    from google.colab import drive
    drive.mount('/content/drive')
    OUT_DIR = '/content/drive/MyDrive/ATS/{folder}'
    os.makedirs(OUT_DIR, exist_ok=True)
print('Save your outputs to:', os.path.abspath(OUT_DIR))
"""


def chapter_folder(path):
    m = re.search(r'chapter(\d+)_', os.path.basename(path)) or re.search(r'Ch_(\d+)', path)
    return f'Chapter_{int(m.group(1))}' if m else 'ATS'


def add(path):
    with open(path) as f:
        nb = json.load(f)
    if any(c.get('metadata', {}).get('ats') == 'colab-banner' for c in nb['cells']):
        return False
    if not isinstance(nb.get('metadata', {}).get('ats'), dict):      # notebook vechi, din afara noului flux
        return False
    # after the title cell: the first markdown cell starting with '#' (else after the badge / first cell)
    pos = next((i + 1 for i, c in enumerate(nb['cells'][:4])
                if c['cell_type'] == 'markdown' and ''.join(c['source']).lstrip().startswith('#')), 1)
    md = {'cell_type': 'markdown', 'metadata': dict(TAG), 'source': BANNER.splitlines(keepends=True)}
    code = {'cell_type': 'code', 'metadata': dict(TAG), 'execution_count': None, 'outputs': [],
            'source': SAVE_CELL.format(folder=chapter_folder(path)).splitlines(keepends=True)}
    if nb.get('nbformat_minor', 0) >= 5:                              # nbformat 4.5+: every cell has an id
        import uuid
        md['id'], code['id'] = uuid.uuid4().hex[:8], uuid.uuid4().hex[:8]
    nb['cells'][pos:pos] = [md, code]
    with open(path, 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write('\n')
    return True


if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(HERE, 'EN', '*.ipynb')) +
                   glob.glob(os.path.join(ROOT, 'Quantlets', 'Ch_*', 'ATS_*', '*.ipynb')))
    n = sum(add(p) for p in files)
    print(f'{n} of {len(files)} notebooks updated')
