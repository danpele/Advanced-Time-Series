"""
generate_all_charts.py -- charts and numbers of Chapter 15 (ATS): review and project defence
============================================================================================
Engine review_core.py (numpy, scipy). Every number of the new material on the slides comes from here; the numbers
of the chapter recaps are read from the numbers files of Chapters 0-14 and 16 (latex/ch15_common.py).
  * snooping     a specification search over K persistent candidate predictors of a series with no
                 predictability: naive, Bonferroni and max-t family-wise false-positive rates (Monte Carlo);
  * leakage      out-of-sample R^2 after predictor selection on the whole sample against the training sample;
  * power        the power of the Diebold-Mariano test by out-of-sample length, effect size and dependence of the
                 loss differential, and the evaluation length needed for 80% power (the AI mini-case);
  * scoreboard   the replications of the course: our estimate against the published one (values from the
                 chapter numbers files and the published values quoted on the chapter slides).
Output: charts/ats_ch15_*.pdf/.png, Quantlets/Ch_15/ch15_numbers.json
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_15/generate_all_charts.py [name ...]
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
import ats_style as st                                                                     # noqa: E402
from review_core import dm_power, dm_power_approx, leakage_r2, p_required, snooping_rates  # noqa: E402

st.apply()
SEED = 2026
KS = [1, 2, 5, 10, 20, 50]
PS = [50, 100, 250, 500, 1000]
DELTAS = [0.1, 0.2, 0.3]


def save(name, save_it=True):
    st.check_no_grey(plt.gcf())
    if save_it:
        st.save_fig(name)
    else:
        plt.show()
        plt.close()


def fig_snooping(save_it=True, reps=1000):
    """Family-wise false-positive rate of a specification search (Monte Carlo)."""
    rows = [snooping_rates(K, reps=reps, seed=SEED + K) for K in KS]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(KS, [100 * r['naive'] for r in rows], 'o-', color=st.IDAred, label='Best of K, naive 5% test')
    ax.plot(KS, [100 * r['bonf'] for r in rows], 's-', color=st.Amber, label='Bonferroni (5%/K)')
    ax.plot(KS, [100 * r['maxt'] for r in rows], 'D-', color=st.Forest, label='max-t over the K statistics (Reality Check logic)')
    ax.axhline(5, color=st.MainBlue, ls='--', lw=1, label='Nominal 5%')
    ax.set_xscale('log')
    ax.set_xticks(KS)
    ax.set_xticklabels([str(k) for k in KS])
    ax.set_xlabel('Number of candidate predictors tried (K)')
    ax.set_ylabel('False-positive rate, %')
    st.legend_outside_bottom(ax, ncol=2, y=-0.2)
    save('ats_ch15_snooping', save_it)
    return {'reps': reps, 'T': 250, 'rows': rows}


def fig_leakage(save_it=True, reps=1000):
    """Out-of-sample R^2 with predictor selection on the whole sample against the training sample."""
    r = leakage_r2(reps=reps, seed=SEED)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    bins = np.linspace(-0.6, 0.4, 41)
    ax.hist(100 * r['honest'], bins=100 * bins, color=st.MainBlue, alpha=0.6, label='Selection on the training sample (honest)')
    ax.hist(100 * r['leaky'], bins=100 * bins, color=st.IDAred, alpha=0.6, label='Selection on the whole sample (look-ahead)')
    ax.axvline(0, color=st.DarkText, ls='--', lw=1)
    ax.set_xlabel('Out-of-sample $R^2$, % (pure-noise predictors: the true value is negative)')
    ax.set_ylabel('Replications')
    st.legend_outside_bottom(ax, ncol=2, y=-0.22)
    save('ats_ch15_leakage', save_it)
    return {'reps': reps, 'T': 240, 'n_test': 60, 'P': 100, 'k': 5,
            'leaky_mean': float(r['leaky'].mean()), 'honest_mean': float(r['honest'].mean()),
            'leaky_pos': float(np.mean(r['leaky'] > 0)), 'honest_pos': float(np.mean(r['honest'] > 0))}


def fig_power(save_it=True, reps=2000):
    """Power of the DM test by out-of-sample length (AI mini-case: is the planned evaluation long enough?)."""
    cols = {0.1: st.IDAred, 0.2: st.MainBlue, 0.3: st.Forest}
    res = {}
    fig, ax = plt.subplots(figsize=(10, 4.2))
    for d in DELTAS:
        mc = [dm_power(P, d, rho=0.3, reps=reps, seed=SEED + P) for P in PS]
        ap = [dm_power_approx(P, d, rho=0.3) for P in PS]
        res[str(d)] = {'mc': mc, 'approx': ap, 'p80': p_required(d, rho=0.3)}
        ax.plot(PS, [100 * x for x in mc], 'o-', color=cols[d], label=f'Mean gain {d} sd of the loss differential')
        ax.plot(PS, [100 * x for x in ap], ':', color=cols[d], label='_approx')
    size = [dm_power(P, 0.0, rho=0.3, reps=reps, seed=SEED + 7 * P) for P in PS]
    res['size'] = size
    ax.plot(PS, [100 * x for x in size], 's--', color=st.Amber, label='No gain (size)')
    ax.axhline(80, color=st.Purple, ls='--', lw=1, label='80% power')
    ax.set_xscale('log')
    ax.set_xticks(PS)
    ax.set_xticklabels([str(p) for p in PS])
    ax.set_xlabel('Out-of-sample length P (dotted: large-sample approximation)')
    ax.set_ylabel('Rejection rate of the DM test, %')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch15_power', save_it)
    return {'reps': reps, 'rho': 0.3, 'P': PS, 'res': res}


FIGS = ['snooping', 'leakage', 'power']


def main(names=None):
    """Run the figures and merge their numbers into ch15_numbers.json (re-read before each write)."""
    path = os.path.join(HERE, 'ch15_numbers.json')
    for nm in names or FIGS:
        print('==', nm, flush=True)
        res = globals()['fig_' + nm]()
        N = json.load(open(path)) if os.path.exists(path) else {}
        N[nm] = res
        with open(path, 'w') as f:
            json.dump(N, f, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))


if __name__ == '__main__':
    main(sys.argv[1:] or None)
