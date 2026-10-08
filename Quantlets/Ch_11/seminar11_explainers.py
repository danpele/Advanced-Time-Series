"""
seminar11_explainers.py -- Explanatory (primer) charts for Seminar 11 (ATS): spectral and wavelet analysis
==========================================================================================================
Teaching charts for the primer slides "Prerequisites for Today" / "Noțiuni necesare azi" of Seminar 11, which takes
place BEFORE Lecture 11. All charts use SIMULATED data only (fixed seeds) and parameters that differ from those of
the exercises: spectra of AR models, the noisy periodogram and its smoothing, lag windows, Slepian tapers,
coherence and phase of a delayed copy, the gains of the HP and Baxter-King filters, the spurious HP cycle of a
random walk, a MODWT multiresolution analysis and a Morlet scalogram with its cone of influence. No exercise answers.

Output: charts/ch11_sem_primer_*.pdf and .png (transparent background, legend outside at the bottom), each sized for
its box on the slides (ats_style.fit_for_slide), and Quantlets/Ch_11/seminar11_explainers.json (the few numbers the
primer slides quote about these simulations).

Run:  python3 Quantlets/Ch_11/seminar11_explainers.py

Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_style as st                                  # noqa: E402
from spectral_core import (KERNEL_CONST, arma_spectrum, bk_weights, cross_spectrum, cwt, dpss, filter_gain,   # noqa: E402
                           hp_filter, hp_gain, ideal_gain, kernel, lag_window, mra, multitaper, periodogram,
                           simulate_arma)

st.apply()
MainBlue, IDAred, Forest, Amber, Navy, Purple = st.MainBlue, st.IDAred, st.Forest, st.Amber, st.DarkText, st.Purple
BandBlue = '#C5D2E8'
CHART_DIR = st.CHART_DIR
TW, TH = 409.72 / 72, 214.79 / 72                       # \textwidth, \textheight of the decks (inches)
TWO = (0.50 * TW, 0.80 * TH)                            # chart in the left column of a two-column primer frame
FULL = (0.96 * TW, 0.62 * TH)                           # full-width chart above two or three bullets
OUT = {}
AR2 = (2 * 0.9 * np.cos(2 * np.pi / 20), -0.81)         # AR(2) with complex roots of modulus 1/0.9: a 20-period cycle


def save(fig, name, box):
    st.fit_for_slide(fig, name, box=box)
    st.check_no_grey(fig)
    os.makedirs(CHART_DIR, exist_ok=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.pdf'), bbox_inches='tight', transparent=True)
    fig.savefig(os.path.join(CHART_DIR, f'{name}.png'), bbox_inches='tight', transparent=True, dpi=180)
    plt.close(fig)
    print(f'   saved {name}')


# =============================================================================
# 1. three AR models: paths and spectra
# =============================================================================
def fig_spectra(n=200, seed=4):
    rng = np.random.default_rng(seed)
    models = [((0.8,), 'AR(1), $\\phi = 0.8$', MainBlue), ((-0.6,), 'AR(1), $\\phi = -0.6$', Amber),
              (AR2, 'AR(2), cycle of 20 periods', IDAred)]
    w = np.linspace(0.005, np.pi, 600)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    for i, (ar, lab, c) in enumerate(models):
        x = simulate_arma(n, ar=ar, rng=rng)
        ax[0].plot(x / x.std() - 5 * i, color=c, lw=0.8, label=lab)
        ax[1].semilogy(w / (2 * np.pi), arma_spectrum(w, ar=ar), color=c, lw=1.6)
    ax[0].set_yticks([])
    ax[0].set_xlabel('$t$')
    ax[0].set_title('Simulated paths (standardised, shifted)', loc='left')
    ax[1].set_xlabel(r'frequency $\omega/2\pi$ (cycles per period)')
    ax[1].set_ylabel(r'$f(\omega)$ (log scale)')
    ax[1].set_title('Spectral densities', loc='left')
    ax[1].axvline(1 / 20, color=IDAred, ls=':', lw=1.0)
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch11_sem_primer_spectra', FULL)


# =============================================================================
# 2. the periodogram is noisy; a lag-window estimate with its chi-square band
# =============================================================================
def fig_smoothing(n=256, M=24, seed=8):
    x = simulate_arma(n, ar=AR2, rng=seed)
    w, I = periodogram(x)
    _, f = lag_window(x, M, 'parzen')
    nu = 2 * n / (M * KERNEL_CONST['parzen'][2])
    lo, hi = nu * f / stats.chi2.ppf(0.975, nu), nu * f / stats.chi2.ppf(0.025, nu)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.fill_between(w, lo, hi, color=BandBlue, alpha=0.9, lw=0, label='95% band (Parzen)')
    ax.semilogy(w, I, '.', color=Amber, ms=3, label=r'periodogram $I(\omega_j)$')
    ax.semilogy(w, f, color=MainBlue, lw=1.6, label=f'Parzen, $M = {M}$')
    ax.semilogy(w, arma_spectrum(w, ar=AR2), color=IDAred, lw=1.2, ls='--', label=r'true $f(\omega)$')
    ax.set_xlabel(r'frequency $\omega$')
    ax.set_ylabel('log scale')
    ax.set_title(f'AR(2), $n = {n}$', loc='left')
    st.legend_outside_bottom(ax, ncol=2)
    save(fig, 'ch11_sem_primer_smoothing', TWO)
    OUT['smooth'] = dict(n=n, M=M, nu=nu, ratio=float(stats.chi2.ppf(0.975, nu) / stats.chi2.ppf(0.025, nu)))


# =============================================================================
# 3. lag windows and their spectral windows
# =============================================================================
def fig_kernels(M=10):
    u = np.linspace(-1.2, 1.2, 500)
    w = np.linspace(-np.pi, np.pi, 800)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    h = np.arange(-60, 61)
    for name, c, lab in (('bartlett', MainBlue, 'Bartlett'), ('parzen', IDAred, 'Parzen')):
        ax[0].plot(u, kernel(u, name), color=c, lw=1.6, label=lab)
        W = (kernel(h / M, name) @ np.cos(np.outer(h, w))) / (2 * np.pi)
        ax[1].plot(w, W, color=c, lw=1.4)
    ax[0].plot(u, (np.abs(u) <= 1).astype(float), color=Amber, lw=1.2, ls='--', label='truncated')
    ax[0].set_xlabel('$u = h/M$')
    ax[0].set_ylabel('$k(u)$')
    ax[0].set_title('Lag windows', loc='left')
    ax[1].axhline(0, color=Navy, lw=0.6)
    ax[1].set_xlabel(r'$\omega$')
    ax[1].set_ylabel('weight')
    ax[1].set_title(f'Spectral windows, $M = {M}$', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch11_sem_primer_kernels', FULL)


# =============================================================================
# 4. Slepian tapers and the multitaper estimate
# =============================================================================
def fig_multitaper(n=256, NW=3, seed=8):
    K = 2 * NW - 1
    v, lam = dpss(n, NW, K)
    x = simulate_arma(n, ar=AR2, rng=seed)
    mt = multitaper(x, NW=NW, K=K)
    w, I = periodogram(x)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    cols = [MainBlue, IDAred, Forest, Amber, Purple]
    for k in range(K):
        ax[0].plot(v[k], color=cols[k], lw=1.2, label=f'tapers $h^{{(k)}}_t$, $k = 1, \\dots, {K}$' if k == 0 else '_')
    ax[0].set_xlabel('$t$')
    ax[0].set_title(f'Slepian tapers, $n = {n}$, $NW = {NW}$, $K = {K}$', loc='left')
    ax[1].fill_between(mt['w'], mt['lo'], mt['hi'], color=BandBlue, alpha=0.9, lw=0, label='95% band')
    ax[1].semilogy(w, I, '.', color=Amber, ms=2.5, label='periodogram')
    ax[1].semilogy(mt['w'], mt['f'], color=MainBlue, lw=1.6, label='multitaper')
    ax[1].semilogy(w, arma_spectrum(w, ar=AR2), color=IDAred, lw=1.2, ls='--', label='true $f$')
    ax[1].set_xlabel(r'frequency $\omega$')
    ax[1].set_title('Average of the $K$ tapered periodograms', loc='left')
    st.fig_legend_bottom(fig, ncol=5)
    save(fig, 'ch11_sem_primer_multitaper', FULL)
    OUT['mt'] = dict(n=n, NW=NW, K=K, conc=float(lam.min()))


# =============================================================================
# 5. coherence and phase of a delayed noisy copy
# =============================================================================
def fig_coherence(n=512, delay=3, b=0.8, s2=1.0, seed=12):
    rng = np.random.default_rng(seed)
    e = simulate_arma(n + delay, ar=(0.5,), rng=rng)
    x = e[delay:]
    y = b * e[:n] + np.sqrt(s2) * rng.standard_normal(n)
    cs = cross_spectrum(x, y, NW=4)
    w = cs['w']
    fx = arma_spectrum(w, ar=(0.5,))
    coh_true = b ** 2 * fx / (b ** 2 * fx + s2 / (2 * np.pi))
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    ax[0].plot(w, cs['coh'], color=MainBlue, lw=1.1, label=r'$\hat\kappa^2$ ($K = 7$ tapers)')
    ax[0].plot(w, coh_true, color=IDAred, lw=1.4, ls='--', label=r'true $\kappa^2$')
    ax[0].axhline(cs['thr'], color=Forest, lw=1.1, ls=':', label='5% threshold')
    ax[0].set_ylim(0, 1)
    ax[0].set_xlabel(r'frequency $\omega$')
    ax[0].set_title('Squared coherence', loc='left')
    ax[1].plot(w, cs['phase'], '.', color=MainBlue, ms=2.5, label=r'$\hat\phi(\omega)$')
    wrap = np.angle(np.exp(1j * delay * w))
    wrap[1:][np.diff(wrap) < -np.pi] = np.nan                  # no vertical line at the jump from pi to -pi
    ax[1].plot(w, wrap, color=IDAred, lw=1.0, ls='--', label=r'$\omega d$, wrapped')
    ax[1].set_xlabel(r'frequency $\omega$')
    ax[1].set_ylabel('radians')
    ax[1].set_title(f'Phase: $x$ leads $y$ by $d = {delay}$', loc='left')
    st.fig_legend_bottom(fig, ncol=5)
    save(fig, 'ch11_sem_primer_coherence', FULL)
    OUT['coh'] = dict(thr=float(cs['thr']), delay=delay)


# =============================================================================
# 6. gains of the HP, Baxter-King and ideal band-pass filters
# =============================================================================
def fig_gains():
    w = np.linspace(2 * np.pi / 200, np.pi, 2000)
    per = 2 * np.pi / w
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.fill_between(per, 0, ideal_gain(w), color=BandBlue, alpha=0.9, lw=0, label='ideal band 6–32')
    ax.semilogx(per, hp_gain(w, 1600), color=IDAred, lw=1.6, label=r'HP cycle, $\lambda = 1600$')
    ax.semilogx(per, filter_gain(bk_weights(6, 32, 12), w), color=MainBlue, lw=1.6, label='Baxter–King, K = 12')
    ax.set_xlabel('period in quarters (log scale)')
    ax.set_ylabel('gain $|A(e^{-i\\omega})|$')
    ax.set_title('Which cycles does a filter keep?', loc='left')
    ax.set_xticks([2, 4, 6, 8, 16, 32, 64, 128])
    ax.set_xticklabels(['2', '4', '6', '8', '16', '32', '64', '128'])
    st.legend_outside_bottom(ax, ncol=1)
    save(fig, 'ch11_sem_primer_gains', TWO)
    OUT['hp32'] = float(hp_gain(2 * np.pi / 32, 1600))


# =============================================================================
# 7. the HP filter applied to a random walk
# =============================================================================
def fig_hp_rw(n=200, seed=31, lam=1600):
    rng = np.random.default_rng(seed)
    y = np.cumsum(rng.standard_normal(n))
    c, tau = hp_filter(y, lam)
    w = np.linspace(0.01, np.pi, 2000)
    u = 1 - np.cos(w)
    fc = hp_gain(w, lam) ** 2 / (2 * u)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    ax[0].plot(y, color=MainBlue, lw=1.0, label='random walk $y_t$')
    ax[0].plot(tau, color=IDAred, lw=1.6, label=r'HP trend $\hat\tau_t$')
    ax[0].plot(c + y.min() - 3, color=Forest, lw=1.0, label=r'HP cycle $y_t - \hat\tau_t$ (shifted)')
    ax[0].set_xlabel('quarter $t$')
    ax[0].set_title('A random walk has no cycle...', loc='left')
    ax[1].plot(2 * np.pi / w, fc / fc.max(), color=Forest, lw=1.6)
    ax[1].set_xscale('log')
    ax[1].set_xticks([2, 4, 8, 16, 32, 64, 128, 256])
    ax[1].set_xticklabels(['2', '4', '8', '16', '32', '64', '128', '256'])
    ax[1].set_xlabel('period in quarters (log scale)')
    ax[1].set_ylabel('relative spectrum')
    ax[1].set_title('...but its HP cycle has a spectral peak', loc='left')
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch11_sem_primer_hp_rw', FULL)


# =============================================================================
# 8. MODWT multiresolution analysis
# =============================================================================
def fig_mra(n=512, seed=3, J=5):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    x = 0.004 * t + np.sin(2 * np.pi * t / 32) + 0.6 * rng.standard_normal(n)
    D, S = mra(x, J, 'sym4')
    fig, ax = plt.subplots(figsize=(10, 3.6))
    rows = [('$X_t$', x, Navy)] + [(f'$D_{j + 1}$, periods {2 ** (j + 1)}–{2 ** (j + 2)}', D[j], c)
                                   for j, c in zip(range(J), (Amber, Purple, MainBlue, IDAred, Forest))] + [(f'$S_{J}$', S, Navy)]
    off = 0
    ticks, labs = [], []
    for lab, s, c in rows:
        ax.plot(t, s - s.mean() + off, color=c, lw=0.9)
        ticks.append(off)
        labs.append(lab)
        off -= 3.2
    ax.set_yticks(ticks)
    ax.set_yticklabels(labs)
    ax.set_xlabel('$t$')
    ax.set_title(r'$X_t = 0.004t + \sin(2\pi t/32) + $ noise $= D_1 + \dots + D_5 + S_5$ (LA(8) MODWT)', loc='left')
    save(fig, 'ch11_sem_primer_mra', FULL)


# =============================================================================
# 9. the Morlet wavelet and a scalogram with its cone of influence
# =============================================================================
def fig_morlet(n=512, seed=5):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    x = np.where(t < n // 2, np.sin(2 * np.pi * t / 16), np.sin(2 * np.pi * t / 64)) + 0.4 * rng.standard_normal(n)
    c = cwt(x, dj=1 / 12)
    P = np.abs(c['W']) ** 2
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4), gridspec_kw=dict(width_ratios=[1, 1.6]))
    u = np.linspace(-4, 4, 400)
    psi = np.pi ** -0.25 * np.exp(1j * 6 * u) * np.exp(-u ** 2 / 2)
    ax[0].plot(u, psi.real, color=MainBlue, lw=1.4, label='real part')
    ax[0].plot(u, psi.imag, color=IDAred, lw=1.2, ls='--', label='imaginary part')
    ax[0].set_xlabel('$u$')
    ax[0].set_title(r'Morlet $\psi(u)$, $\omega_0 = 6$', loc='left')
    im = ax[1].contourf(t, c['period'], np.log2(P), levels=20, cmap='Blues')
    ax[1].plot(t, c['coi'], color=IDAred, lw=1.4)
    ax[1].fill_between(t, c['coi'], c['period'].max(), facecolor='white', alpha=0.6, edgecolor=IDAred, lw=0.8,
                       label='outside the cone of influence (faded)')
    ax[1].set_yscale('log', base=2)
    ax[1].set_ylim(c['period'].max(), c['period'].min())
    ax[1].set_xlabel('$t$')
    ax[1].set_ylabel('period')
    ax[1].set_title('Scalogram $\\log_2|W(s, t)|^2$: period 16, then 64', loc='left')
    fig.colorbar(im, ax=ax[1], pad=0.02)
    st.fig_legend_bottom(fig, ncol=3)
    save(fig, 'ch11_sem_primer_morlet', FULL)


if __name__ == '__main__':
    fig_spectra()
    fig_smoothing()
    fig_kernels()
    fig_multitaper()
    fig_coherence()
    fig_gains()
    fig_hp_rw()
    fig_mra()
    fig_morlet()
    with open(os.path.join(HERE, 'seminar11_explainers.json'), 'w') as fh:
        json.dump(OUT, fh, indent=1)
    print(json.dumps(OUT, indent=1))
