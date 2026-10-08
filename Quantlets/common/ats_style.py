"""
ats_style.py -- chart style of the ATS course (the same as MFM)
===============================================================
  * transparent background (figure, axes, saved files), no grid, no top/right spines;
  * the legend always OUTSIDE the plot, at the bottom centre (legend_outside_bottom), without a frame;
  * colours from the course palette (the LaTeX colours of latex/preamble.tex); no grey series and no grey text:
    text and axes are dark (DarkText), reference lines use a palette colour (dashed);
  * charts saved as PDF (for the slides) and PNG (for the notebooks and the site) in charts/.

Use:
    import ats_style as st
    st.apply()                                   # once, before the first chart
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(x, y, color=st.COL['sp500'], label='S&P 500')
    st.legend_outside_bottom(ax, ncol=3)
    st.save_fig('ats_ch1_returns')               # charts/ats_ch1_returns.pdf + .png
    st.check_no_grey(fig)                        # optional: raises if a series or a text is grey

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

# Palette (RGB values of latex/preamble.tex)
MainBlue = '#1A3A6E'
IDAred = '#CD0000'
Forest = '#2E7D32'
Amber = '#B5853F'
Orange = '#E67E22'
Purple = '#8E44AD'
Teal = '#17A2B8'
Crimson = '#DC3545'
DarkText = '#1F2A44'          # text, axes and ticks (dark navy, not grey)
LightBlue = '#7EA6E0'         # thin background series (e.g. the other countries of a panel): a blue tint, never grey

PALETTE = [MainBlue, IDAred, Forest, Amber, Purple, Orange, Teal, Crimson]
# fixed colours for the series used in several chapters
COL = {'sp500': MainBlue, 'bet': IDAred, 'bettr': Orange, 'dax': Teal, 'btc': Amber, 'eth': Crimson,
       'eurron': Forest, 'gold': Purple, 'vix': Crimson, 'stoxx50': Forest, 'ndx': Teal}

_HERE = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(_HERE, '..', '..', 'charts')


def apply():
    """Set the course style for matplotlib."""
    rc = plt.rcParams
    rc['figure.facecolor'] = 'none'
    rc['axes.facecolor'] = 'none'
    rc['savefig.facecolor'] = 'none'
    rc['savefig.transparent'] = True
    rc['axes.grid'] = False
    rc['font.family'] = 'sans-serif'
    rc['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
    # font sizes for slides (charts are 9-11 inches wide and shown at 8-14 cm)
    rc['font.size'] = 12
    rc['axes.labelsize'] = 13
    rc['axes.titlesize'] = 13
    rc['xtick.labelsize'] = 11.5
    rc['ytick.labelsize'] = 11.5
    rc['legend.fontsize'] = 11
    rc['axes.spines.top'] = False
    rc['axes.spines.right'] = False
    rc['axes.linewidth'] = 0.6
    rc['lines.linewidth'] = 1.4
    rc['legend.facecolor'] = 'none'
    rc['legend.framealpha'] = 0
    rc['legend.frameon'] = False
    for k in ('text.color', 'axes.labelcolor', 'axes.edgecolor', 'xtick.color', 'ytick.color', 'axes.titlecolor'):
        rc[k] = DarkText
    rc['axes.prop_cycle'] = mpl.cycler(color=PALETTE)


def legend_outside_bottom(ax, ncol=2, y=-0.22, **kw):
    """Place the legend outside the plot, bottom centre (for a figure with several axes, pass the last one
    or use fig.legend with the same arguments)."""
    return ax.legend(loc='upper center', bbox_to_anchor=(0.5, y), ncol=ncol, frameon=False, **kw)


def fig_legend_bottom(fig, handles=None, labels=None, ncol=3, y=-0.02):
    """One legend for a whole figure (several panels), below the panels."""
    if handles is None:
        handles, labels = [], []
        for ax in fig.axes:
            for h, l in zip(*ax.get_legend_handles_labels()):
                if l not in labels and not l.startswith('_'):
                    handles.append(h)
                    labels.append(l)
    return fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, y), ncol=ncol, frameon=False)


def save_fig(name, out_dir=None, show=False):
    """Save the current figure as transparent PDF and PNG (charts/ by default); a chart shown on the slides is first
    sized for its box there (fit_for_slide)."""
    d = out_dir or CHART_DIR
    os.makedirs(d, exist_ok=True)
    _keep(plt.gcf(), name)
    fit_for_slide(plt.gcf(), name)
    plt.savefig(os.path.join(d, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    plt.savefig(os.path.join(d, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    if show:
        plt.show()
    plt.close()
    print(f'   saved {name}')


def _is_grey(c, tol=0.06):
    try:
        r, g, b = to_rgb(c)
    except ValueError:
        return False
    return max(r, g, b) - min(r, g, b) < tol and 0.25 < (r + g + b) / 3 < 0.95


def check_no_grey(fig):
    """House rule: no grey series and no grey text. Raises ValueError listing the offending elements."""
    bad = []
    for ax in fig.axes:
        for ln in ax.get_lines():
            if not ln.get_label().startswith('_') and _is_grey(ln.get_color()):
                bad.append(f'line {ln.get_label()!r}')
        for coll in ax.collections:
            fc = coll.get_facecolor()
            if len(fc) and coll.get_label() and not coll.get_label().startswith('_') and _is_grey(fc[0][:3]):
                bad.append(f'series {coll.get_label()!r}')
        for t in ax.texts + [ax.title, ax.xaxis.label, ax.yaxis.label]:
            if t.get_text() and _is_grey(t.get_color()):
                bad.append(f'text {t.get_text()[:30]!r}')
    if bad:
        raise ValueError('grey elements: ' + ', '.join(bad))


# =============================================================================
# SLIDE FIT: every chart shown on the slides is sized for the box it gets there (tools/chart_boxes.py writes
# chart_boxes.json), so that its text is at least SLIDE_MIN_PT points on the slide (the slide text is 8 pt);
# pale confidence bands (fill_between) are made clearly visible.
# =============================================================================
SLIDE_MIN_PT = 6.2           # smallest chart text on the slide (pt)
SLIDE_BASE_PT = 6.6          # usual chart text (tick labels) on the slide (pt)
BAND_MIN_ALPHA = 0.30        # confidence bands at least this opaque
PAD_IN = 0.1                 # savefig pad (inches, matplotlib default)
SLIDE_WIDEN = 1.5            # a chart limited by the height of its box may become this much wider
SCRIPT_SHRINK = 0.7          # size of a mathtext sub- or superscript relative to its text (matplotlib)
_BOXES = None


def _boxes():
    global _BOXES
    if _BOXES is None:
        try:
            import json
            with open(os.path.join(_HERE, 'chart_boxes.json')) as fh:
                _BOXES = json.load(fh)
        except (OSError, ValueError):
            _BOXES = {}
    return _BOXES


def _keep(fig, name):
    """Optional (ATS_FIG_PICKLE=<folder>): keep the figure before the slide fit, to refit it without recomputing."""
    d = os.environ.get('ATS_FIG_PICKLE')
    if d:
        import pickle
        path = os.path.join(d, name + '.pkl')
        try:
            os.makedirs(d, exist_ok=True)
            with open(path, 'wb') as fh:
                pickle.dump(fig, fh)
        except Exception as e:                      # noqa: BLE001
            if os.path.exists(path):
                os.remove(path)
            _log(f'  {name}: not pickled ({e})')


def _log(msg):
    p = os.environ.get('ATS_FIT_LOG')
    if p:
        with open(p, 'a') as fh:
            fh.write(msg + '\n')


def _drawn_texts(fig, renderer):
    """The texts that are drawn: visible, non-empty, in a visible axes or legend, tick labels inside the view."""
    from matplotlib.text import Text
    hidden = set()
    for ax in fig.axes:
        if not ax.get_visible():
            hidden.update(id(t) for t in ax.findobj(Text))
        lg = ax.get_legend()
        if lg is not None and not lg.get_visible():
            hidden.update(id(t) for t in lg.findobj(Text))
    ticks, drawn = set(), set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            for tk in axis.get_major_ticks() + axis.get_minor_ticks():
                ticks.update((id(tk.label1), id(tk.label2)))
            if ax.axison and axis.get_visible():
                for tk in axis._update_ticks():
                    drawn.update((id(tk.label1), id(tk.label2)))
    out = []
    for t in fig.findobj(Text):
        if id(t) in hidden or not t.get_visible() or not t.get_text().strip():
            continue
        if id(t) in ticks and id(t) not in drawn:
            continue
        try:
            bb = t.get_window_extent(renderer)
        except Exception:
            continue
        if bb.width > 0 and bb.height > 0:
            out.append((t, bb))
    return out


def _bands(fig):
    """Pale fill_between bands (and their legend keys) at least BAND_MIN_ALPHA opaque."""
    from matplotlib.patches import Patch
    changed = {}
    for ax in fig.axes:
        for c in ax.collections:
            if type(c).__name__ not in ('FillBetweenPolyCollection', 'PolyCollection'):
                continue
            fc = c.get_facecolor()
            if not len(fc):
                continue
            a = c.get_alpha()
            a = fc[0][3] if a is None else a
            if 0 < a < BAND_MIN_ALPHA:
                new = min(0.45, max(BAND_MIN_ALPHA, 2 * a))
                changed[round(float(a), 3)] = new
                if c.get_alpha() is not None:
                    c.set_alpha(new)
                else:
                    fc = fc.copy()
                    fc[:, 3] = new
                    c.set_facecolor(fc)
        for pt in ax.patches:                       # horizontal bands (axhspan): a confidence band around zero
            if type(pt).__name__ == 'Rectangle' and pt.get_x() == 0 and pt.get_width() == 1:
                a = pt.get_alpha()
                a = pt.get_facecolor()[3] if a is None else a
                if 0 < a < BAND_MIN_ALPHA and pt.get_transform() != ax.transData:
                    new = min(0.45, max(BAND_MIN_ALPHA, 2 * a))
                    changed[round(float(a), 3)] = new
                    pt.set_alpha(new)
    if not changed:
        return
    for lg in [ax.get_legend() for ax in fig.axes if ax.get_legend()] + list(fig.legends):
        for h in lg.legend_handles:
            if isinstance(h, Patch):
                a = h.get_alpha()
                a = h.get_facecolor()[3] if a is None else a
                if round(float(a), 3) in changed:
                    h.set_alpha(changed[round(float(a), 3)])
                elif 0 < a < BAND_MIN_ALPHA:               # a pale key drawn by hand for a band
                    h.set_alpha(min(0.45, max(BAND_MIN_ALPHA, 2 * a)))


def _outside_bottom(lg, fig_level):
    if getattr(lg, '_loc', None) != 9:             # 'upper center'
        return False
    bb = lg.get_bbox_to_anchor()
    parent = lg.figure.bbox if fig_level else lg.axes.bbox
    y = (bb.y0 - parent.y0) / max(parent.height, 1e-9)
    return y < (0.16 if fig_level else 0.0)


def _renew_legend(lg, ncols):
    """The same legend with fewer columns (matplotlib lays a legend out only when it is created)."""
    from matplotlib.transforms import IdentityTransform
    handles, texts = lg.legend_handles, lg.texts
    if any(h is None for h in handles):
        lg._ncols = 1
        return lg
    kw = dict(loc='upper center', ncols=ncols, frameon=lg.get_frame_on(), handlelength=lg.handlelength,
              handletextpad=lg.handletextpad, columnspacing=lg.columnspacing, borderaxespad=lg.borderaxespad,
              labelspacing=lg.labelspacing, markerscale=lg.markerscale, numpoints=lg.numpoints,
              scatterpoints=lg.scatterpoints)
    if texts:
        kw['fontsize'] = texts[0].get_fontsize()
    if lg.get_title().get_text():
        kw.update(title=lg.get_title().get_text(), title_fontsize=lg.get_title().get_fontsize())
    anchor = lg.get_bbox_to_anchor()
    fig = lg.figure
    if lg in fig.legends:
        fig.legends.remove(lg)
        new = fig.legend(handles, [t.get_text() for t in texts], **kw)
        new.set_bbox_to_anchor((anchor.x0, anchor.y0), transform=IdentityTransform())
    else:
        new = lg.axes.legend(handles, [t.get_text() for t in texts], **kw)
        new.set_bbox_to_anchor((anchor.x0, anchor.y0), transform=IdentityTransform())
    for a, b in zip(texts, new.texts):
        b.set_color(a.get_color())
        b.set_fontsize(a.get_fontsize())
    fig.canvas.draw()
    return new


def _widen_legend(lg, room, fig, renderer):
    """A tall legend (one entry per row) under a short, wide figure: more columns while it still fits its room."""
    n = len(lg.texts)
    while lg._ncols < n and lg.get_window_extent(renderer).height > 0.2 * fig.bbox.height:
        new = _renew_legend(lg, lg._ncols + 1)
        if new.get_window_extent(renderer).width > room:
            return _renew_legend(new, new._ncols - 1)
        lg = new
    return lg


def _place_legends(fig, renderer):
    """Legends outside at the bottom: just below the decorations of their axes (axes legends) or below all axes
    (figure legends); fewer columns when a legend is wider than its room."""
    pad = 3.0 * fig.dpi / 72
    W = fig.bbox.width
    columns = len({round(ax.get_position().x0, 2) for ax in fig.axes if ax.get_visible()})
    for ax in fig.axes:
        lg = ax.get_legend()
        if lg is None or not lg.get_visible() or not _outside_bottom(lg, False):
            continue
        room = W * 0.98 if columns <= 1 else ax.bbox.width * 1.15
        while lg._ncols > 1 and lg.get_window_extent(renderer).width > room:
            lg = _renew_legend(lg, lg._ncols - 1)
        lg = _widen_legend(lg, room, fig, renderer)
        lg.set_visible(False)
        twins = [a for a in fig.axes if a.get_visible() and a.bbox.bounds == ax.bbox.bounds]
        y0 = min(a.get_tightbbox(renderer).y0 for a in twins)
        lg.set_visible(True)
        x = (lg.get_bbox_to_anchor().x0 - ax.bbox.x0) / ax.bbox.width
        lg.set_bbox_to_anchor((x, (y0 - ax.bbox.y0 - pad) / ax.bbox.height), transform=ax.transAxes)
    for lg in list(fig.legends):
        if not lg.get_visible() or not _outside_bottom(lg, True):
            continue
        while lg._ncols > 1 and lg.get_window_extent(renderer).width > W * 0.99:
            lg = _renew_legend(lg, lg._ncols - 1)
        lg = _widen_legend(lg, W * 0.99, fig, renderer)
        bbs = [a.get_tightbbox(renderer) for a in fig.axes if a.get_visible()]
        y0 = min(b.y0 for b in bbs if b is not None)
        x = (lg.get_bbox_to_anchor().x0 - fig.bbox.x0) / W
        lg.set_bbox_to_anchor((x, (y0 - pad) / fig.bbox.height), transform=fig.transFigure)


def _wrap(t, width_px, renderer, max_lines=3, vertical=False):
    """A title or axis label longer than width_px (the height for a vertical label) goes on two (three) lines."""
    def size():
        e = t.get_window_extent(renderer)
        return e.height if vertical else e.width
    s = getattr(t, '_fit_text', None) or t.get_text()      # rewrap from the author's text at every layout
    if not s or '\n' in s or s.count('$') % 2:
        return
    t._fit_text = s
    t.set_text(s)
    if size() <= width_px:
        return
    words, cur, math = [], '', False           # split at the spaces outside $...$
    for ch in s:
        if ch == '$':
            math = not math
        if ch == ' ' and not math:
            words.append(cur)
            cur = ''
        else:
            cur += ch
    words.append(cur)
    if len(words) < 2:
        return
    for n in range(2, max_lines + 1):
        per = -(-len(s) // n)
        lines, cur = [], ''
        for w in words:
            if cur and len(cur) + 1 + len(w) > per * 1.12:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + ' ' + w).strip()
        lines.append(cur)
        t.set_text('\n'.join(lines))
        if size() <= width_px:
            break
    _log(f'  wrapped {s[:40]!r}')


def _thin_ticks(fig, renderer):
    """Overlapping tick labels: keep every second (third, ...) label."""
    from matplotlib.ticker import FixedFormatter, FixedLocator
    gap = 2.0 * fig.dpi / 72
    done = set()
    for ax in fig.axes:
        if not ax.get_visible():
            continue
        for axis, horiz in ((ax.xaxis, True), (ax.yaxis, False)):
            if id(axis.major) in done:
                continue
            minors = [t for t in axis.get_minor_ticks() if t.label1.get_visible() and t.label1.get_text().strip()]
            if minors and axis.get_scale() == 'log':
                mb = [t.label1.get_window_extent(renderer) for t in axis._update_ticks()
                      if t.label1.get_visible() and t.label1.get_text().strip()]
                sp = sorted((b.x0, b.x1) if horiz else (b.y0, b.y1) for b in mb)
                if any(sp[i + 1][0] - sp[i][1] < gap for i in range(len(sp) - 1)):
                    from matplotlib.ticker import NullFormatter
                    axis.set_minor_formatter(NullFormatter())
                    _log('  minor tick labels hidden')
            ticks = [t for t in axis._update_ticks() if t.label1.get_visible() and t.label1.get_text().strip()]
            if len(ticks) < 3:
                continue
            bbs = [t.label1.get_window_extent(renderer) for t in ticks]

            def ok(idx):
                sp = sorted((bbs[i].x0, bbs[i].x1) if horiz else (bbs[i].y0, bbs[i].y1) for i in idx)
                return all(sp[i + 1][0] - sp[i][1] >= gap for i in range(len(sp) - 1))
            if ok(range(len(ticks))):
                continue
            loc = axis.get_major_locator()
            if (type(loc).__name__ in ('FixedLocator', 'StrCategoryLocator')        # categories: keep every label
                    and not getattr(loc, '_fit_thinned', False)):
                rot = getattr(axis, '_fit_rotated', 0)
                if horiz and rot < 90:
                    rot = 30 if rot == 0 else 90                  # first 30 degrees, then vertical
                    for t in ticks:
                        t.label1.set_rotation(rot)
                        t.label1.set_ha('right' if rot == 30 else 'center')
                        t.label1.set_rotation_mode('anchor' if rot == 30 else 'default')
                    axis._fit_rotated = rot
                    _log(f'  rotated x category labels ({rot} degrees)')
                else:
                    _log(f'  CATEGORY LABELS OVERLAP ({"x" if horiz else "y"})')
                continue
            import re
            years = [bool(re.search(r'\d{4}', t.label1.get_text())) for t in ticks]
            for k in (2, 3, 4, 5, 6, 8, 10):
                # of the k offsets, keep the one with most year labels (concise date axes name the year once)
                offs = sorted(range(k), key=lambda o: -sum(years[o::k]))
                sel = list(range(offs[0], len(ticks), k))
                if ok(sel):
                    break
            axis.set_major_locator(FixedLocator([ticks[i].get_loc() for i in sel]))
            axis.set_major_formatter(FixedFormatter([ticks[i].label1.get_text() for i in sel]))
            axis.get_major_locator()._fit_thinned = True
            done.add(id(axis.major))
            _log(f'  thinned {"x" if horiz else "y"} tick labels: every {k}')


def _tight(fig):
    eng = fig.get_layout_engine()
    if eng is None or type(eng).__name__ in ('TightLayoutEngine', 'PlaceHolderLayoutEngine'):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            fig.tight_layout()


def _relayout(fig, renderer):
    for _ in range(2):
        _tight(fig)
        fig.canvas.draw()
        _place_legends(fig, renderer)
    for ax in fig.axes:
        if ax.get_visible():
            for t in (ax.title, ax._left_title, ax._right_title, ax.xaxis.label):
                _wrap(t, ax.bbox.width * 0.98, renderer)
            _wrap(ax.yaxis.label, ax.bbox.height * 1.02, renderer, vertical=True)
    _thin_ticks(fig, renderer)
    _tight(fig)
    fig.canvas.draw()
    _place_legends(fig, renderer)
    fig.canvas.draw()


def _tight_in(fig, renderer):
    bb = fig.get_tightbbox(renderer)
    return bb.width + 2 * PAD_IN, bb.height + 2 * PAD_IN


def _overlaps(fig, renderer):
    """Pairs of drawn texts that overlap (for the log)."""
    tx = _drawn_texts(fig, renderer)
    tol = 1.0 * fig.dpi / 72
    bad = []
    for i in range(len(tx)):
        a, ba = tx[i]
        for b, bb in tx[i + 1:]:
            if min(ba.x1, bb.x1) - max(ba.x0, bb.x0) > tol and min(ba.y1, bb.y1) - max(ba.y0, bb.y0) > tol:
                bad.append((a.get_text()[:25], b.get_text()[:25]))
    return bad


def _plain_log_ticks(fig, floor):
    """Log axes: plain numbers (0.01, 0.1, 1, 10) instead of powers of ten when the range allows it, so that no
    tick label has a small exponent; otherwise tick labels large enough for the exponent to be legible."""
    from matplotlib.ticker import FuncFormatter, LogFormatterSciNotation, LogLocator, NullFormatter
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            if axis.get_scale() != 'log' or not isinstance(axis.get_major_formatter(), LogFormatterSciNotation):
                continue
            lo, hi = sorted(axis.get_view_interval())
            if lo >= 1e-4 and hi <= 1e5:
                fmt = FuncFormatter(lambda v, pos: f'{v:g}')
                if hi / max(lo, 1e-12) < 10:              # less than a decade: labelled ticks at 1-9 x 10^k
                    axis.set_major_locator(LogLocator(base=10, subs=tuple(range(1, 10))))
                axis.set_major_formatter(fmt)
                axis.set_minor_formatter(NullFormatter())
                _log('  log axis: plain tick labels')
            else:
                labels = axis.get_ticklabels()
                size = max(floor / SCRIPT_SHRINK, labels[0].get_fontsize() if labels else 0)
                axis.set_tick_params(labelsize=size)
                _log('  log axis: larger tick labels for the exponents')


def fit_for_slide(fig, name, box=None):
    """Size the figure for its box on the slides: text at least SLIDE_MIN_PT and tick labels about SLIDE_BASE_PT on the
    slide, the aspect ratio of the figure kept, legends just below the plots, overlapping tick labels thinned, long
    titles wrapped, pale bands darkened. Charts that are not on the slides keep their size."""
    _bands(fig)
    box = box or _boxes().get(name)
    if not box:
        return
    shared_cbar = any(len(getattr(a, '_colorbar_info', {}).get('parents', [])) > 1 for a in fig.axes)
    if shared_cbar and fig.get_layout_engine() is None:
        fig.set_layout_engine('constrained')          # tight_layout misplaces a colorbar shared by several panels
    import numpy as np
    Wb, Hb = box
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    w0, h0 = _tight_in(fig, r)
    asp = w0 / h0
    dw, dh = (Wb, Wb / asp) if asp >= Wb / Hb else (Hb * asp, Hb)
    tx = _drawn_texts(fig, r)
    sizes = np.array([t.get_fontsize() for t, _ in tx]) if tx else np.array([11.5])
    s_now = dw / w0
    tick_ids = {id(tk.label1) for a in fig.axes if a.axison
                for axis in (a.xaxis, a.yaxis) for tk in axis._update_ticks()}
    tick_sizes = [t.get_fontsize() for t, _ in tx if id(t) in tick_ids]
    base = float(np.median(tick_sizes)) if tick_sizes else float(np.median(sizes))   # the tick labels set the scale
    s_star = SLIDE_BASE_PT / base
    if s_now >= s_star:
        if sizes.min() * s_now >= SLIDE_MIN_PT:
            return
        s_star = s_now
    if dw < Wb * 0.98:                               # limited by the height: up to half as much width again
        dw = min(Wb, dw * SLIDE_WIDEN)
    floor = SLIDE_MIN_PT / s_star
    _plain_log_ticks(fig, floor)
    fig.canvas.draw()
    tx = _drawn_texts(fig, r)
    for t, _ in tx:
        if t.get_fontsize() < floor:                    # (sub- and superscripts stay at the usual mathtext ratio)
            t.set_fontsize(floor)
    for lg in [a.get_legend() for a in fig.axes if a.get_legend()] + list(fig.legends):
        if lg.texts:                                   # one size for all the entries of a legend
            big = max(t.get_fontsize() for t in lg.texts)
            for t in lg.texts:
                t.set_fontsize(big)
    tw, th = dw / s_star, dh / s_star                # target size of the saved PDF (inches)
    W, H = fig.get_size_inches()
    best = None
    for _ in range(8):
        _relayout(fig, r)
        w, h = _tight_in(fig, r)
        err = max(abs(w - tw) / tw, abs(h - th) / th)
        if best is None or err < best[0]:
            best = (err, W, H)
        if err < 0.015:
            break
        W, H = max(1.2, W + (tw - w)), max(0.9, H + (th - h))
        fig.set_size_inches(W, H)
    if err >= 0.015:                                  # not converged: keep the closest size
        fig.set_size_inches(best[1], best[2])
        _relayout(fig, r)
        w, h = _tight_in(fig, r)
        _log(f'  {name}: size not reached ({best[0]:.0%} off)')
    for _ in range(2):                                # tick labels checked again at the final size
        _thin_ticks(fig, r)
        _tight(fig)
        fig.canvas.draw()
        _place_legends(fig, r)
        fig.canvas.draw()
    w, h = _tight_in(fig, r)
    W, H = fig.get_size_inches()
    s = min(Wb / w, Hb / h)
    tx = _drawn_texts(fig, r)
    mn = min(t.get_fontsize() for t, _ in tx) * s if tx else 99.0
    ov = _overlaps(fig, r)
    axh = min((a.bbox.height / fig.dpi * s for a in fig.axes if a.get_visible() and a.bbox.height > 0), default=9.0)
    flag = (('  LOW' if mn < SLIDE_MIN_PT - 0.15 else '') + ('  OVERLAP' if ov else '')
            + ('  SMALL' if axh < 0.6 else ''))
    _log(f'{name}: box {Wb:.2f}x{Hb:.2f} in, fig {W:.2f}x{H:.2f} in, scale {s:.3f}, min text {mn:.2f} pt, '
         f'plot height {axh:.2f} in{flag}'
         + (f'  {ov[:6]}' if ov else ''))
