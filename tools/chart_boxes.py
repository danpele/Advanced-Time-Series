"""
chart_boxes.py -- the box each chart gets on the slides (for ats_style.save_fig)
================================================================================
Reads every deck (.tex of EN/Courses, EN/Seminars, RO/Cursuri, RO/Seminarii), finds each
\\includegraphics[width=a\\textwidth,height=b\\textheight,keepaspectratio]{chart.pdf} of a file in charts/,
works out the width of the enclosing column (beamer columns, minipages, the \\taskw/\\solw columns of the seminar
decks, solutions version) and writes the smallest box per chart (inches) to Quantlets/common/chart_boxes.json.

ats_style.save_fig then sizes the figure so that its text is at least ats_style.SLIDE_MIN_PT on the slide.
Re-run after changing the size of a chart in a generator (python3 tools/chart_boxes.py), then redraw the chart.

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import glob
import json
import os
import re

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TW, TH = 409.72 / 72, 214.79 / 72       # \textwidth, \textheight of the decks (inches; beamer 16:9, 9pt, 8 mm)
OUT = os.path.join(REPO, 'Quantlets', 'common', 'chart_boxes.json')

TOKEN = re.compile(r'\\begin\{(column|minipage)\}(?:\[[^\]]*\])*\{([^}]*)\}|\\end\{(column|minipage)\}|'
                   r'\\includegraphics\[([^\]]*)\]\{([^}]*)\}')


def width_of(spec, cur):
    spec = spec.strip()
    if spec == r'\taskw':
        return 0.47 * cur
    if spec == r'\solw':
        return 0.49 * cur
    m = re.match(r'([0-9.]*)\\(textwidth|linewidth|columnwidth)$', spec)
    if m:
        return (float(m.group(1)) if m.group(1) else 1.0) * cur
    m = re.match(r'([0-9.]+)(cm|mm|in|pt)$', spec)
    if m:
        return float(m.group(1)) / {'cm': 2.54, 'mm': 25.4, 'in': 1.0, 'pt': 72.27}[m.group(2)]
    return cur


def length(v, cur, ref):
    v = v.strip()
    m = re.match(r'([0-9.]*)\\(textwidth|linewidth|columnwidth|textheight)$', v)
    if m:
        f = float(m.group(1)) if m.group(1) else 1.0
        return f * (TH if m.group(2) == 'textheight' else cur)
    m = re.match(r'([0-9.]+)(cm|mm|in|pt)$', v)
    if m:
        return float(m.group(1)) / {'cm': 2.54, 'mm': 25.4, 'in': 1.0, 'pt': 72.27}[m.group(2)]
    return ref


def boxes():
    charts = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(REPO, 'charts', '*.pdf'))}
    out = {}
    tex = [f for d in ('EN/Courses', 'EN/Seminars', 'RO/Cursuri', 'RO/Seminarii')
           for f in glob.glob(os.path.join(REPO, d, '*.tex')) if not f.endswith('_solutions.tex')]
    for f in sorted(tex):
        s = open(f, encoding='utf-8').read()
        stack = [TW]
        for m in TOKEN.finditer(s):
            if m.group(1):
                stack.append(width_of(m.group(2), stack[-1]))
            elif m.group(3):
                if len(stack) > 1:
                    stack.pop()
            else:
                name = os.path.splitext(m.group(5))[0]
                if name not in charts:
                    continue
                opts = dict(kv.split('=', 1) for kv in m.group(4).split(',') if '=' in kv)
                w = length(opts['width'], stack[-1], stack[-1]) if 'width' in opts else stack[-1]
                h = length(opts['height'], stack[-1], 99.0) if 'height' in opts else 99.0
                if name in out:
                    w, h = min(w, out[name][0]), min(h, out[name][1])
                out[name] = [round(w, 3), round(h, 3)]
    return dict(sorted(out.items()))


if __name__ == '__main__':
    b = boxes()
    json.dump(b, open(OUT, 'w'), indent=0)
    print(f'{len(b)} charts -> {os.path.relpath(OUT, REPO)}')
