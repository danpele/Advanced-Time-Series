"""
generate_all_charts.py -- charts and numbers of Chapter 14 (ATS): causal inference for time series
==================================================================================================
Course data (ats_data.py), chart style (ats_style.py), the engine causal_core.py (numpy, scipy, statsmodels).
Every number on the slides comes from here.
  * Granger causality     a common driver with different delays (Monte Carlo, pairwise against conditional tests);
                          lead-lag between the S&P 500, the DAX and the BET (daily returns, HAC Wald tests);
                          transfer entropy against linear Granger for a nonlinear coupling;
  * causal discovery      PCMCI against pairwise correlations and the full VAR on a known 6-variable system;
                          PCMCI on weekly log realised variances of five equity indices and EUR/RON;
                          convergent cross mapping for coupled logistic maps, with and without common forcing;
  * ITS and event study   Romanian monthly HICP inflation around the end of the electricity price cap (July 2025)
                          and the VAT increase (August 2025): segmented regression with HAC errors; the Romanian
                          10-year yield around five fiscal and political events of 2024-2025;
  * synthetic control     German reunification, the replication of Abadie, Diamond and Hainmueller (2015) with their
                          public data (CC0, Harvard Dataverse), cross-validated V, in-space, in-time and leave-one-out
                          placebos; the Brexit doppelganger of Born, Mueller, Schularick and Sedlacek (2019) on
                          OECD quarterly real GDP;
  * Romania 2025          annual HICP inflation of Romania against 26 EU donors (Eurostat): synthetic control,
                          demeaned SC, ridge-augmented SC, synthetic DiD; placebos; the tax component from the HICP
                          at constant tax rates;
  * staggered DiD         two-way fixed effects against Callaway and Sant'Anna (2021) on a simulated panel;
  * BSTS                  a CausalImpact-type analysis of the US spot Bitcoin ETF approval (10 January 2024) on
                          weekly Bitcoin realised volatility, with placebo dates and the anticipation question;
  * DML                   the partially linear model with blocked cross-fitting on simulated dependent data;
  * AI mini-case          a specification curve for the Romanian estimate.
Output: charts/ats_ch14_*.pdf/.png, Quantlets/Ch_14/ch14_numbers.json
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_14/generate_all_charts.py [name ...]
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import io
import json
import os
import sys
import urllib.request
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
sys.path.insert(0, HERE)
from ats_data import END, load_close, log_returns                                                       # noqa: E402
import ats_style as st                                                                                  # noqa: E402
from causal_core import (ascm_lambda, ascm_ridge, causal_impact, ccm_curve, corr_links, cs_att, dml_plr,  # noqa: E402,F401
                         full_granger_links, granger, link_rates, ols_hac, nw_lags, pcmci, placebo_ratios,
                         sc_demeaned, sc_weights, sdid, sdid_placebo_se, sim_common_driver, sim_dml,
                         sim_logistic_pair, sim_nonlinear_coupling, sim_pcmci_system, sim_staggered,
                         synth_v, transfer_entropy, twfe_event)

warnings.filterwarnings('ignore')
SEED = 2026
EUROSTAT = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/'
EU27 = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU',
        'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']
EURO_AREA = ['AT', 'BE', 'CY', 'DE', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL',
             'PT', 'SI', 'SK']
RO_SC = dict(pre_start='2023-07-01', T0='2025-06-01', end='2026-08-01', eval_end='2026-06-01')
GERMANY_URL = 'https://dataverse.harvard.edu/api/access/datafile/2457914'   # repgermany.tab, CC0 (version 2.1)
OECD_QNA = ('https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA,1.1/Q.Y.{c}.S1..B1GQ._Z._Z._Z.'
            'USD_PPP.LR.LA.T0102?startPeriod=1995-Q1&format=csvfile')
BMSS = dict(donors=['AUS', 'AUT', 'BEL', 'CAN', 'FIN', 'FRA', 'DEU', 'HUN', 'ISL', 'IRL', 'ITA', 'JPN', 'KOR', 'LUX',
                    'NLD', 'NZL', 'NOR', 'PRT', 'SVK', 'ESP', 'SWE', 'CHE', 'USA'],
            published={'DEU': 0.05, 'HUN': 0.11, 'ISL': 0.01, 'IRL': 0.01, 'ITA': 0.17, 'NZL': 0.14, 'USA': 0.51},
            pre=('1995-Q1', '2016-Q2'), end='2018-Q4')
EVENTS = [('2024-12-06', 'Constitutional Court annuls the presidential election'),
          ('2025-01-27', 'S&P outlook to negative (announced Friday 24 January)'),
          ('2025-06-20', 'ECOFIN: no effective action under the EDP'),
          ('2025-07-07', 'Government assumes responsibility for the fiscal package')]
BTC = dict(start='2023-01-02', T0='2024-01-07', end='2024-06-30', anticip='2023-06-11',
           controls=('sp500', 'ndx', 'gold', 'eurusd'))
STAG_SLOPES = {6: 0.40, 11: 0.20, 16: 0.05}   # effect per period of exposure, by adoption cohort
_MEM = {}


def datefmt(*axes):
    """Concise date ticks (at most six per axis)."""
    import matplotlib.dates as mdates
    for a in axes:
        loc = mdates.AutoDateLocator(maxticks=6)
        a.xaxis.set_major_locator(loc)
        a.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))


def save(name, save_it=True):
    st.check_no_grey(plt.gcf())
    if save_it:
        st.save_fig(name)
    else:
        plt.show()
        plt.close()


# =============================================================================
# 0. DATA
# =============================================================================
def get_bytes(url):
    """Download a public file once per session (no key); optional local cache folder in ATS_CACHE."""
    import hashlib
    if url in _MEM:
        return _MEM[url]
    cache = os.environ.get('ATS_CACHE')
    path = os.path.join(cache, hashlib.md5(url.encode()).hexdigest()) if cache else None
    if path and os.path.exists(path):
        _MEM[url] = open(path, 'rb').read()
        return _MEM[url]
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ATS course)'})
    _MEM[url] = urllib.request.urlopen(req, timeout=300).read()
    if path:
        os.makedirs(cache, exist_ok=True)
        open(path, 'wb').write(_MEM[url])
    return _MEM[url]


def eurostat_panel(dataset, key_prefix, geos, start='2015-01'):
    """Monthly Eurostat panel (date x geo) from the SDMX 2.1 API; key_prefix such as 'M.I25.TOTAL.'."""
    url = EUROSTAT + dataset + '/' + key_prefix + '+'.join(geos) + f'?format=SDMX-CSV&startPeriod={start}'
    t = pd.read_csv(io.BytesIO(get_bytes(url)))
    t['date'] = pd.to_datetime(t['TIME_PERIOD'] + '-01')
    return t.pivot_table(index='date', columns='geo', values='OBS_VALUE')[geos]


def hicp_annual(ct=False):
    """Annual HICP inflation (%), monthly, of the 27 EU countries, computed as 100 (ln P_t - ln P_{t-12}) from the
    index 2025 = 100 (Eurostat prc_hicp_minr; with ct=True the HICP at constant tax rates, prc_hicp_ct)."""
    key = 'ct' if ct else 'hicp'
    if key not in _MEM:
        P = eurostat_panel('prc_hicp_ct' if ct else 'prc_hicp_minr', 'M.I25.TOTAL.', EU27, start='2014-01')
        L = np.log(P)
        _MEM[key] = (100 * (L - L.shift(12))).loc['2015-01-01':]
    return _MEM[key]


def hicp_index():
    """HICP index 2025 = 100 of the 27 EU countries (Eurostat prc_hicp_minr)."""
    if 'hicpidx' not in _MEM:
        _MEM['hicpidx'] = eurostat_panel('prc_hicp_minr', 'M.I25.TOTAL.', EU27, start='2014-01')
    return _MEM['hicpidx']


def germany():
    """The panel of Abadie, Diamond and Hainmueller (2015): West Germany and 16 OECD countries, 1960-2003
    (Harvard Dataverse doi:10.7910/DVN/24714, version 2.1, CC0): GDP per capita (PPP, current USD), inflation,
    trade openness, schooling, investment rates, industry share."""
    if 'ger' not in _MEM:
        _MEM['ger'] = pd.read_csv(io.BytesIO(get_bytes(GERMANY_URL)), sep='\t')
    return _MEM['ger']


def oecd_gdp():
    """Quarterly real GDP (chain-linked volumes, PPP USD, seasonally adjusted) of the UK and the 23 donors of
    Born et al. (2019) from the OECD Quarterly National Accounts (public SDMX API), normalised to 1 in 1995."""
    if 'oecd' not in _MEM:
        c = '+'.join(['GBR'] + BMSS['donors'])
        t = pd.read_csv(io.BytesIO(get_bytes(OECD_QNA.format(c=c))))
        P = t.pivot_table(index='TIME_PERIOD', columns='REF_AREA', values='OBS_VALUE')
        P = P[['GBR'] + BMSS['donors']]
        _MEM['oecd'] = P / P.loc['1995-Q1':'1995-Q4'].mean()
    return _MEM['oecd']


def weekly_logrv(names, start='2008-01-01', end=END):
    """Weekly log realised variance: log of the sum of squared daily log returns (in %) within each week
    (Monday-Sunday), each series on its own calendar."""
    out = {}
    for k in names:
        r = log_returns(k, start=start, end=end)
        out[k] = np.log((r ** 2).resample('W-SUN').sum().replace(0, np.nan))
    return pd.DataFrame(out).dropna()


def daily_returns(names, start, end=END):
    """Daily log returns (%) on the common trading days of several markets."""
    return pd.concat([log_returns(k, start=start, end=end) for k in names], axis=1).dropna()


# =============================================================================
# 1. OVERVIEW
# =============================================================================
def fig_overview(save_it=True):
    A = hicp_annual()
    G = germany()
    U = oecd_gdp()
    W = weekly_logrv(['btc'], start='2022-06-01', end='2024-12-29')
    fig, ax = plt.subplots(2, 2, figsize=(11, 7.6))
    a = ax[0, 0]
    for c in EU27:
        if c != 'RO':
            a.plot(A.index, A[c], color=st.Teal, lw=0.6, alpha=0.45, label='_')
    a.plot(A.index, A.drop(columns='RO').median(axis=1), color=st.MainBlue, lw=1.6, label='EU median')
    a.plot(A.index, A['RO'], color=st.IDAred, lw=1.8, label='Romania')
    a.axvline(pd.Timestamp('2025-07-01'), color=st.Amber, ls='--', lw=1)
    a.set_title('HICP inflation, % y/y (Eurostat)')
    st.legend_outside_bottom(a, ncol=2, y=-0.16)
    a = ax[0, 1]
    for nm, g in G.groupby('country'):
        if nm != 'West Germany':
            a.plot(g['year'], g['gdp'], color=st.Teal, lw=0.6, alpha=0.5, label='_')
    g = G[G['country'] == 'West Germany']
    a.plot(g['year'], g['gdp'], color=st.IDAred, lw=1.8, label='West Germany')
    a.axvline(1990, color=st.Amber, ls='--', lw=1)
    a.set_title('GDP per capita, PPP USD (ADH 2015 data)')
    st.legend_outside_bottom(a, ncol=2, y=-0.16)
    a = ax[1, 0]
    x = pd.PeriodIndex(U.index, freq='Q').to_timestamp()
    for c in BMSS['donors']:
        a.plot(x, U[c], color=st.Teal, lw=0.6, alpha=0.5, label='_')
    a.plot(x, U['GBR'], color=st.IDAred, lw=1.8, label='United Kingdom')
    a.axvline(pd.Timestamp('2016-07-01'), color=st.Amber, ls='--', lw=1)
    a.set_xlim(pd.Timestamp('1995-01-01'), pd.Timestamp('2019-12-31'))
    a.set_ylim(0.9, 2.4)
    a.set_title('Real GDP, 1995 = 1 (OECD)')
    st.legend_outside_bottom(a, ncol=2, y=-0.16)
    a = ax[1, 1]
    a.plot(W.index, W['btc'], color=st.Amber, lw=1.2, label='Bitcoin')
    a.axvline(pd.Timestamp('2024-01-10'), color=st.IDAred, ls='--', lw=1)
    a.set_title('Bitcoin weekly log realised variance')
    st.legend_outside_bottom(a, ncol=2, y=-0.16)
    datefmt(ax[0, 0], ax[1, 0], ax[1, 1])
    plt.tight_layout(h_pad=3.0)
    save('ats_ch14_overview', save_it)
    return {'hicp_end': str(A['RO'].dropna().index[-1].date()), 'n_eu': len(EU27),
            'ro_jun25': float(A.loc['2025-06-01', 'RO']), 'ro_aug25': float(A.loc['2025-08-01', 'RO']),
            'ro_max': float(A.loc['2025-07-01':, 'RO'].max()), 'ro_max_date': str(A.loc['2025-07-01':, 'RO'].idxmax().date()),
            'ro_last': float(A['RO'].dropna().iloc[-1]), 'eu_med_last': float(A.drop(columns='RO').loc[A['RO'].dropna().index[-1]].median()),
            'oecd_end': str(U.index[-1])}


# =============================================================================
# 2. GRANGER CAUSALITY
# =============================================================================
def fig_granger_sim(save_it=True, reps=500, sizes=(100, 250, 500, 1000)):
    """Monte Carlo: x and y share a driver w (x with delay 1, y with delay 3); x has no effect on y.
    Rejection rates at 5% of the pairwise test x -> y, the test conditional on w, and the reverse test y -> x."""
    res = {}
    for T in sizes:
        rej = {'pairwise': 0, 'conditional': 0, 'reverse': 0}
        for r in range(reps):
            x, y, w = sim_common_driver(T, seed=SEED + r)
            rej['pairwise'] += granger(y, x, p=2, hac=False)['p'] < 0.05
            rej['conditional'] += granger(y, x, z=w, p=4, hac=False)['p'] < 0.05
            rej['reverse'] += granger(x, y, p=2, hac=False)['p'] < 0.05
        res[str(T)] = {k: v / reps for k, v in rej.items()}
    fig, ax = plt.subplots(figsize=(9, 3.8))
    xs = np.arange(len(sizes))
    for i, (k, lab, c) in enumerate([('pairwise', 'x -> y, pairwise', st.IDAred),
                                     ('conditional', 'x -> y, conditional on the driver w', st.MainBlue),
                                     ('reverse', 'y -> x, pairwise', st.Amber)]):
        ax.bar(xs + (i - 1) * 0.26, [res[str(T)][k] for T in sizes], 0.26, color=c, label=lab)
    ax.axhline(0.05, color=st.Forest, ls='--', lw=1, label='nominal 5%')
    ax.set_xticks(xs)
    ax.set_xticklabels([f'T = {T}' for T in sizes])
    ax.set_ylabel('rejection rate at 5%')
    ax.set_ylim(0, 1.05)
    st.legend_outside_bottom(ax, ncol=4, y=-0.16)
    save('ats_ch14_granger_sim', save_it)
    return {'reps': reps, 'res': res}


def fig_granger_markets(save_it=True, p=2, start='2015-01-01'):
    """Lead-lag of daily returns: S&P 500 (closes after Bucharest and Frankfurt), DAX and BET. Wald tests of Granger
    non-causality with HAC covariance; cross-correlations corr(BET_t, S&P_{t-k})."""
    R = daily_returns(['sp500', 'dax', 'bet'], start)
    sp, dx, bt = R['sp500'].values, R['dax'].values, R['bet'].values
    tests = {'sp_bet': granger(bt, sp, p=p), 'bet_sp': granger(sp, bt, p=p), 'sp_bet_dax': granger(bt, sp, z=dx, p=p),
             'dax_bet': granger(bt, dx, p=p), 'sp_dax': granger(dx, sp, p=p), 'sp_bet_cl': granger(bt, sp, p=p, hac=False)}
    ks = list(range(-3, 4))
    cc = {}
    for nm, src in (('sp500', sp), ('dax', dx)):
        cc[nm] = [float(np.corrcoef(bt[max(0, k):len(bt) + min(0, k)], src[max(0, -k):len(src) - max(0, k)])[0, 1]) for k in ks]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    xs = np.arange(len(ks))
    ax.bar(xs - 0.2, cc['sp500'], 0.4, color=st.MainBlue, label='S&P 500 at t - k')
    ax.bar(xs + 0.2, cc['dax'], 0.4, color=st.Forest, label='DAX at t - k')
    ax.axhline(2 / np.sqrt(len(bt)), color=st.IDAred, ls='--', lw=1, label='+/- 2/sqrt(T)')
    ax.axhline(-2 / np.sqrt(len(bt)), color=st.IDAred, ls='--', lw=1, label='_')
    ax.set_xticks(xs)
    ax.set_xticklabels([f'k = {k}' for k in ks])
    ax.set_ylabel('correlation with BET at t')
    st.legend_outside_bottom(ax, ncol=3, y=-0.16)
    save('ats_ch14_granger_markets', save_it)
    out = {k: {'W': v['W'], 'p': v['p'], 'te': v['te']} for k, v in tests.items()}
    out.update({'T': int(len(R)), 'start': str(R.index[0].date()), 'end': str(R.index[-1].date()), 'p': p,
                'cc_sp1': cc['sp500'][4], 'cc_sp0': cc['sp500'][3], 'cc_dax0': cc['dax'][3], 'cc_dax1': cc['dax'][4]})
    return out


def fig_te(save_it=True, T=1000, B=199):
    """Nonlinear coupling: linear Granger misses the effect of x on y, the transfer entropy finds it."""
    x, y = sim_nonlinear_coupling(T, seed=SEED)
    lin = granger(y, x, p=1, hac=True)
    te_xy = transfer_entropy(x, y, lag=1, B=B, seed=SEED)
    te_yx = transfer_entropy(y, x, lag=1, B=B, seed=SEED)
    xn, yn = sim_nonlinear_coupling(T, c=0.0, seed=SEED + 1)
    te_null = transfer_entropy(xn, yn, lag=1, B=B, seed=SEED)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    e = y[1:] - 0.4 * y[:-1]
    ax[0].scatter(x[:-1], e, s=6, color=st.MainBlue, alpha=0.5, label='y_t - 0.4 y_(t-1)')
    g = np.linspace(x.min(), x.max(), 100)
    ax[0].plot(g, 0.6 * (g ** 2 - 1), color=st.IDAred, lw=2, label='0.6 (x^2 - 1)')
    ax[0].set_xlabel('x at t - 1')
    ax[0].set_title('The effect of x on y is symmetric')
    st.legend_outside_bottom(ax[0], ncol=2, y=-0.22)
    labels = ['x -> y\n(coupled)', 'y -> x\n(coupled)', 'x -> y\n(no coupling)']
    vals = [te_xy['te'], te_yx['te'], te_null['te']]
    nulls = [te_xy['null95'], te_yx['null95'], te_null['null95']]
    ax[1].bar(range(3), vals, color=[st.IDAred, st.Amber, st.MainBlue], label='kNN transfer entropy')
    ax[1].scatter(range(3), nulls, marker='_', s=900, color=st.Forest, label='95% of the permutation null', zorder=3)
    ax[1].set_xticks(range(3))
    ax[1].set_xticklabels(labels)
    ax[1].set_ylabel('nats')
    ax[1].set_title('Transfer entropy and its permutation null')
    st.legend_outside_bottom(ax[1], ncol=2, y=-0.3)
    plt.tight_layout()
    save('ats_ch14_te', save_it)
    return {'T': T, 'B': B, 'lin_W': lin['W'], 'lin_p': lin['p'], 'gauss_te': lin['te'], 'te_xy': te_xy['te'],
            'p_xy': te_xy['p'], 'te_yx': te_yx['te'], 'p_yx': te_yx['p'], 'te_null': te_null['te'], 'p_null': te_null['p']}


# =============================================================================
# 3. CAUSAL DISCOVERY
# =============================================================================
def fig_pcmci_sim(save_it=True, reps=50, tau_max=3, alpha=0.01, designs=((0, 500), (14, 150))):
    """Detection rates of lagged cross links: pairwise lagged correlations, the full VAR (one regression per
    target with all lags of all variables) and PCMCI, in a low-dimensional design (6 variables, T = 500) and a
    high-dimensional one (20 variables, T = 150)."""
    out = {}
    for n_extra, T in designs:
        rates = {'pairwise correlation': [], 'full VAR': [], 'PCMCI': []}
        for r in range(reps):
            X, true = sim_pcmci_system(T, seed=SEED + r, n_extra=n_extra, tau_max=tau_max)
            rates['pairwise correlation'].append(link_rates(corr_links(X, tau_max, alpha)['links'], true))
            rates['full VAR'].append(link_rates(full_granger_links(X, tau_max, alpha)['links'], true))
            rates['PCMCI'].append(link_rates(pcmci(X, tau_max, 0.2, alpha)['links'], true))
        out[f'N{6 + n_extra}_T{T}'] = {k: {'tpr': float(np.mean([a for a, b in v])), 'fpr': float(np.mean([b for a, b in v]))}
                                       for k, v in rates.items()}
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    for ax, (key, o) in zip(axs, out.items()):
        xs = np.arange(3)
        ks = list(o)
        ax.bar(xs - 0.2, [o[k]['tpr'] for k in ks], 0.4, color=st.Forest, label='true positive rate (power)')
        ax.bar(xs + 0.2, [o[k]['fpr'] for k in ks], 0.4, color=st.IDAred, label='false positive rate')
        ax.axhline(alpha, color=st.MainBlue, ls='--', lw=1, label=f'alpha = {alpha}')
        for i, k in enumerate(ks):
            ax.text(i - 0.2, o[k]['tpr'] + 0.02, f"{o[k]['tpr']:.2f}", ha='center', fontsize=9)
            ax.text(i + 0.2, o[k]['fpr'] + 0.02, f"{o[k]['fpr']:.3f}", ha='center', fontsize=9)
        ax.set_xticks(xs)
        ax.set_xticklabels(['pairwise corr.', 'full VAR', 'PCMCI'])
        n_, t_ = key[1:].split('_T')
        ax.set_title(f'{n_} variables, T = {t_}', fontsize=11)
        ax.set_ylim(0, 1.12)
    st.fig_legend_bottom(fig, ncol=3, y=-0.0)
    plt.tight_layout(rect=(0, 0.07, 1, 1))
    save('ats_ch14_pcmci_sim', save_it)
    return {'reps': reps, 'tau_max': tau_max, 'alpha': alpha, 'rates': out}


PCMCI_NAMES = ['nikkei', 'stoxx50', 'wig20', 'bet', 'sp500', 'eurron']
PCMCI_LABELS = {'nikkei': 'Nikkei', 'stoxx50': 'Euro Stoxx', 'wig20': 'WIG20', 'bet': 'BET', 'sp500': 'S&P 500',
                'eurron': 'EUR/RON'}


def fig_pcmci_vol(save_it=True, tau_max=2, alpha=0.01, start='2008-01-01'):
    """PCMCI on weekly log realised variances (weeks remove the time-zone ordering of daily closes)."""
    W = weekly_logrv(PCMCI_NAMES, start=start)
    res = pcmci(W.values, tau_max, 0.2, alpha)
    N = len(PCMCI_NAMES)
    links = []
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for tau in range(1, tau_max + 1):
                if res['links'][i, j, tau]:
                    links.append((PCMCI_NAMES[i], PCMCI_NAMES[j], tau, float(res['val'][i, j, tau])))
    corr = corr_links(W.values, tau_max, alpha)['links']
    n_corr = int(sum(corr[i, j, t] for i in range(N) for j in range(N) for t in range(1, tau_max + 1) if i != j))
    ang = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, N, endpoint=False)
    pos = {k: (np.cos(a), np.sin(a)) for k, a in zip(PCMCI_NAMES, ang)}
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    for k, (x0, y0) in pos.items():
        ax.add_patch(plt.Circle((x0, y0), 0.17, color=st.MainBlue, alpha=0.15))
        ax.text(x0, y0, PCMCI_LABELS[k], ha='center', va='center', fontsize=11, color=st.DarkText)
    for a_, b_, tau, v in links:
        (x0, y0), (x1, y1) = pos[a_], pos[b_]
        d = np.hypot(x1 - x0, y1 - y0)
        sx, sy = x0 + 0.19 * (x1 - x0) / d, y0 + 0.19 * (y1 - y0) / d
        ex, ey = x1 - 0.19 * (x1 - x0) / d, y1 - 0.19 * (y1 - y0) / d
        col = st.IDAred if v > 0 else st.MainBlue
        ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=1 + 8 * abs(v), alpha=0.85,
                                    connectionstyle='arc3,rad=0.12' if tau == 1 else 'arc3,rad=-0.25'))
    ax.plot([], [], color=st.IDAred, lw=2, label='positive MCI')
    ax.plot([], [], color=st.MainBlue, lw=2, label='negative MCI')
    ax.plot([], [], color=st.DarkText, lw=0, label='lag 1: arc to the left; lag 2: arc to the right')
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')
    st.legend_outside_bottom(ax, ncol=3, y=-0.0)
    save('ats_ch14_pcmci_vol', save_it)
    return {'T': int(len(W)), 'start': str(W.index[0].date()), 'end': str(W.index[-1].date()), 'tau_max': tau_max,
            'alpha': alpha, 'links': links, 'n_links': len(links), 'n_corr': n_corr,
            'n_possible': N * (N - 1) * tau_max}


def fig_ccm(save_it=True, T=1000, libs=(25, 50, 100, 200, 400, 800), reps=20):
    """Convergent cross mapping (Sugihara et al. 2012): (a) x drives y (byx = 0.32, bxy = 0): the y-manifold
    cross-maps x with skill growing in L, the reverse does not converge to the same level; (b) no coupling but a
    strong common periodic forcing: both directions have high skill (spurious bidirectional causality)."""
    x, y = sim_logistic_pair(T, bxy=0.0, byx=0.32, seed=SEED)
    a = ccm_curve(x, y, libs, E=2, reps=reps, seed=SEED)
    xf, yf = sim_logistic_pair(T, bxy=0.0, byx=0.0, rx=3.7, ry=3.7, forcing=(0.2, 12), seed=SEED + 1)
    b = ccm_curve(xf, yf, libs, E=2, reps=reps, seed=SEED)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for k, (r, t) in enumerate(((a, 'x drives y (Sugihara et al. 2012, Fig. 3)'), (b, 'no coupling, common periodic forcing'))):
        ax[k].plot(r['L'], r['x_drives_y'], 'o-', color=st.IDAred, label='cross-map x from M_y (evidence x -> y)')
        ax[k].plot(r['L'], r['y_drives_x'], 's-', color=st.MainBlue, label='cross-map y from M_x (evidence y -> x)')
        ax[k].set_xscale('log')
        ax[k].set_xlabel('library size L')
        ax[k].set_title(t, fontsize=11)
    ax[0].set_ylabel('cross-map skill (correlation)')
    st.fig_legend_bottom(fig, ncol=2, y=-0.02)
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    save('ats_ch14_ccm', save_it)
    return {'T': T, 'reps': reps, 'a_xy': a['x_drives_y'], 'a_yx': a['y_drives_x'], 'b_xy': b['x_drives_y'],
            'b_yx': b['y_drives_x'], 'libs': list(libs)}


# =============================================================================
# 4. INTERRUPTED TIME SERIES AND EVENT STUDY
# =============================================================================
def its_design(idx, crisis=('2021-07-01', '2023-06-01')):
    """Design of the pre-intervention model of monthly inflation: 12 month dummies (no constant) and a step for the
    2021-2023 inflation surge."""
    M = np.column_stack([(idx.month == m).astype(float) for m in range(1, 13)])
    surge = ((idx >= crisis[0]) & (idx <= crisis[1])).astype(float)
    return np.column_stack([M, surge])


def fig_its(save_it=True, start='2015-01-01', T0='2025-06-01', end='2026-06-01'):
    """Interrupted time series for Romanian monthly HICP inflation (100 x log change): the seasonal model is fitted
    on the pre-intervention months only and projected over July 2025 - June 2026; the effect is actual minus
    projected. Standard error of the 12-month cumulative effect: (i) i.i.d. errors, 12 sigma^2 + parameter
    uncertainty; (ii) dependent errors, 12 x the Newey-West long-run variance of the pre-period residuals +
    parameter uncertainty (HAC covariance)."""
    P = hicp_index()['RO']
    m = (100 * np.log(P).diff()).loc[start:end].dropna()
    pre = m.index <= T0
    X = its_design(m.index)
    out = {}
    for hac in (False, True):
        b, V, e = ols_hac(m.values[pre], X[pre], hac=hac)
        pred = X[~pre] @ b
        eff = m.values[~pre] - pred
        a = X[~pre].sum(0)
        s2 = float(e @ e / (pre.sum() - X.shape[1]))
        lrv = s2
        if hac:
            L = nw_lags(int(pre.sum()))
            for j in range(1, L + 1):
                lrv += 2 * (1 - j / (L + 1)) * float(e[j:] @ e[:-j]) / (pre.sum() - X.shape[1])
        n = int((~pre).sum())
        se = float(np.sqrt(n * lrv + a @ V @ a))
        out['hac' if hac else 'iid'] = {'cum': float(eff.sum()), 'cum_se': se, 'sigma': float(np.sqrt(s2)),
                                        'lrv_ratio': float(lrv / s2)}
    out['eff'] = {str(d.date())[:7]: float(x) for d, x in zip(m.index[~pre], eff)}
    out['rest'] = float(eff[2:].mean())
    rho = float(np.corrcoef(e[1:], e[:-1])[0, 1])
    cf = X @ b
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.8))
    sel = m.index >= '2023-01-01'
    ax[0].bar(m.index[sel], m.values[sel], width=20, color=st.MainBlue, alpha=0.6, label='monthly inflation, Romania')
    ax[0].plot(m.index[sel], cf[sel], color=st.Forest, lw=1.8, label='seasonal model fitted before July 2025')
    ax[0].axvline(pd.Timestamp('2025-06-15'), color=st.Amber, ls='--', lw=1)
    ax[0].set_ylabel('% month on month')
    st.legend_outside_bottom(ax[0], ncol=2, y=-0.16)
    xi = m.index[~pre]
    ct = np.cumsum(eff)
    ax[1].plot(xi, ct, 'o-', color=st.IDAred, label='cumulative effect')
    k = np.arange(1, len(ct) + 1)
    for key, c, lab in (('iid', st.Amber, '95% band, i.i.d. errors'), ('hac', st.MainBlue, '95% band, HAC')):
        sd = out[key]['cum_se'] * np.sqrt(k / len(ct))
        ax[1].fill_between(xi, ct - 1.96 * sd, ct + 1.96 * sd, color=c, alpha=0.15, label=lab)
    ax[1].axhline(0, color=st.DarkText, lw=0.6)
    ax[1].set_ylabel('percentage points (log)')
    st.legend_outside_bottom(ax[1], ncol=2, y=-0.16)
    datefmt(ax[0], ax[1])
    plt.tight_layout()
    save('ats_ch14_its', save_it)
    out.update({'T_pre': int(pre.sum()), 'start': str(m.index[0].date()), 'end': str(m.index[-1].date()), 'rho': rho,
                'lags': nw_lags(int(pre.sum())), 'surge': float(b[12])})
    return out


def fig_event(save_it=True, est=(-250, -11), win=(0, 2)):
    """Event study of the BET index (MacKinlay 1997): market model r_BET = a + b r_STOXX50 estimated in [-250, -11]
    trading days; abnormal returns and the cumulative abnormal return over [0, 2]; standard errors from the
    estimation residuals, i.i.d. against Newey-West (the CAR variance uses the long-run variance)."""
    R = daily_returns(['bet', 'stoxx50'], start='2023-06-01')
    res = []
    paths = {}
    for date, label in EVENTS:
        t0 = R.index.searchsorted(pd.Timestamp(date))
        sub = R.iloc[t0 + est[0]:t0 + est[1]]
        X = np.column_stack([np.ones(len(sub)), sub['stoxx50'].values])
        b, V, e = ols_hac(sub['bet'].values, X, hac=False)
        w = R.iloc[t0 - 5:t0 + 6]
        ar = w['bet'].values - (b[0] + b[1] * w['stoxx50'].values)
        k = win[1] - win[0] + 1
        car = float(ar[5 + win[0]:5 + win[1] + 1].sum())
        s2 = float(e @ e / (len(e) - 2))
        L = nw_lags(len(e))
        lrv = s2
        for j in range(1, L + 1):
            lrv += 2 * (1 - j / (L + 1)) * float(e[j:] @ e[:-j]) / (len(e) - 2)
        se_iid, se_hac = np.sqrt(k * s2), np.sqrt(k * max(lrv, 1e-12))
        res.append({'date': date, 'label': label, 'day0': str(R.index[t0].date()), 'ar0': float(ar[5]), 'car': car,
                    'se_iid': float(se_iid), 'se_hac': float(se_hac), 't_iid': car / se_iid, 't_hac': car / se_hac,
                    'beta': float(b[1]), 'rho': float(np.corrcoef(e[1:], e[:-1])[0, 1])})
        paths[date] = np.cumsum(ar)
    fig, ax = plt.subplots(figsize=(11, 3.6))
    cols = [st.IDAred, st.MainBlue, st.Forest, st.Purple, st.Amber]
    for (date, label), c in zip(EVENTS, cols):
        ax.plot(range(-5, 6), paths[date] - paths[date][4], 'o-', color=c, ms=4, label=f'{date}: {label}')
    ax.axvline(-0.5, color=st.DarkText, ls=':', lw=1)
    ax.axhline(0, color=st.DarkText, lw=0.6)
    ax.set_xlabel('trading days relative to the event')
    ax.set_ylabel('BET cumulative abnormal return, %')
    st.legend_outside_bottom(ax, ncol=2, y=-0.2, fontsize=9)
    save('ats_ch14_event', save_it)
    return {'events': res, 'est': list(est), 'win': list(win)}


# =============================================================================
# 5. SYNTHETIC CONTROL: GERMAN REUNIFICATION (ADH 2015)
# =============================================================================
def adh_matrices(d, unit, controls, pred_years, special, z_years):
    """Synth's dataprep: predictors gdp, trade, infrate averaged over pred_years (missing values ignored), special
    predictors [(var, years)] averaged over their years; outcomes Z (gdp) over z_years. Returns X1, X0, Z1, Z0."""
    def col(u):
        g = d[d['index'] == u].set_index('year')
        v = [g.loc[list(pred_years), c].mean() for c in ('gdp', 'trade', 'infrate')]
        v += [g.loc[list(yrs), c].mean() for c, yrs in special]
        return np.array(v, float)
    X1 = col(unit)
    X0 = np.column_stack([col(u) for u in controls])
    Y = d.pivot_table(index='year', columns='index', values='gdp')
    return X1, X0, Y.loc[list(z_years), unit].values, Y.loc[list(z_years), controls].values


ADH_SPEC = {   # rep.r of Abadie, Diamond and Hainmueller (2015): (training, main) dataprep specifications
    1990: (dict(prior=range(1971, 1981), special=[('industry', range(1971, 1981)), ('schooling', (1970, 1975)),
                                                  ('invest70', (1980,))], ssr=range(1981, 1991)),
           dict(prior=range(1981, 1991), special=[('industry', range(1981, 1991)), ('schooling', (1980, 1985)),
                                                  ('invest80', (1980,))], ssr=range(1960, 1990))),
    1975: (dict(prior=range(1960, 1965), special=[('industry', (1971,)), ('schooling', (1960, 1965)),
                                                  ('invest60', (1980,))], ssr=range(1965, 1976)),
           dict(prior=range(1965, 1976), special=[('industry', range(1971, 1976)), ('schooling', (1970, 1975)),
                                                  ('invest70', (1980,))], ssr=range(1960, 1976)))}


def adh_fit(d, unit, controls, t_treat=1990, starts=3):
    """ADH (2015, Section 4 and rep.r): V chosen by cross-validation (training predictors, validation outcomes),
    then the weights from the main predictors with that V (Synth's custom.v)."""
    tr, mn = ADH_SPEC[t_treat]
    X1, X0, Z1, Z0 = adh_matrices(d, unit, controls, tr['prior'], tr['special'], tr['ssr'])
    v, _, _, _ = synth_v(X1, X0, Z1, Z0, starts=starts, seed=SEED)
    X1m, X0m, _, _ = adh_matrices(d, unit, controls, mn['prior'], mn['special'], mn['ssr'])
    sd = np.column_stack([X1m, X0m]).std(axis=1, ddof=1)
    w = sc_weights(X1m / sd, X0m / sd[:, None], v)
    return w, v, X1m, X0m


def fig_germany(save_it=True):
    d = germany()
    names = d.groupby('index')['country'].first()
    controls = [u for u in sorted(d['index'].unique()) if u != 7]
    w, v, X1m, X0m = adh_fit(d, 7, controls)
    Y = d.pivot_table(index='year', columns='index', values='gdp')
    synth = Y[controls].values @ w
    gap = Y[7].values - synth
    yrs = Y.index.values
    pre = yrs < 1990
    rmspe_pre = float(np.sqrt(np.mean(gap[pre] ** 2)))
    post = (yrs >= 1990)
    weights = {names[u]: float(x) for u, x in zip(controls, w)}
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.9))
    ax[0].plot(yrs, Y[7].values, color=st.IDAred, lw=2, label='West Germany')
    ax[0].plot(yrs, synth, color=st.MainBlue, lw=2, ls='--', label='synthetic West Germany')
    ax[0].axvline(1990, color=st.Amber, ls=':', lw=1)
    ax[0].set_ylabel('GDP per capita (PPP, current USD)')
    st.legend_outside_bottom(ax[0], ncol=2, y=-0.16)
    ax[1].plot(yrs, gap, color=st.IDAred, lw=2, label='gap')
    ax[1].axhline(0, color=st.DarkText, lw=0.6)
    ax[1].axvline(1990, color=st.Amber, ls=':', lw=1)
    ax[1].set_ylabel('gap, USD per capita')
    st.legend_outside_bottom(ax[1], ncol=2, y=-0.16)
    plt.tight_layout()
    save('ats_ch14_germany', save_it)
    g03 = float(gap[yrs == 2003][0])
    avg = float(gap[(yrs >= 1990)].mean())
    rel = float(np.mean(gap[post] / synth[post]))
    return {'weights': weights, 'v': [float(x) for x in v], 'rmspe_pre': rmspe_pre, 'gap2003': g03, 'avg_post': avg,
            'rel_post': rel, 'rel2003': float(gap[yrs == 2003][0] / synth[yrs == 2003][0]),
            'pred': {'treated': X1m.tolist(), 'synth': (X0m @ w).tolist(), 'avg': X0m.mean(1).tolist()},
            'published': {'Austria': 0.42, 'Japan': 0.16, 'Netherlands': 0.09, 'Switzerland': 0.11, 'USA': 0.22}}


def fig_germany_placebo(save_it=True):
    """ADH (2015): in-space placebos (ratio of post- to pre-1990 RMSPE, Figure 6), the in-time placebo 1975
    (Figure 4) and leave-one-out (Figure 5)."""
    d = germany()
    names = d.groupby('index')['country'].first()
    units = sorted(d['index'].unique())
    Y = d.pivot_table(index='year', columns='index', values='gdp')
    yrs = Y.index.values
    ratios, gaps = {}, {}
    for u in units:
        ctrl = [c for c in units if c != u]
        w, _, _, _ = adh_fit(d, u, ctrl, starts=2)
        g = Y[u].values - Y[ctrl].values @ w
        gaps[names[u]] = g
        ratios[names[u]] = float(np.sqrt(np.mean(g[yrs >= 1990] ** 2)) / np.sqrt(np.mean(g[yrs < 1990] ** 2)))
    rank = sorted(ratios, key=lambda k: -ratios[k])
    p = (rank.index('West Germany') + 1) / len(units)
    # in-time placebo: reunification moved to 1975, sample to 1990; outcome-only SC on 1960-1974, because the
    # cross-validated V of the 1975 specification is not well identified (Kloessner et al. 2018)
    ctrl = [c for c in units if c != 7]
    pre75 = yrs < 1975
    w75 = sc_weights(Y.loc[pre75, 7].values, Y.loc[pre75, ctrl].values)
    s75 = Y[ctrl].values @ w75
    v_starts = {}
    for k in (1, 8):
        tr, _ = ADH_SPEC[1975]
        X1, X0, Z1, Z0 = adh_matrices(d, 7, ctrl, tr['prior'], tr['special'], tr['ssr'])
        v_, _, loss_, _ = synth_v(X1, X0, Z1, Z0, starts=k, seed=SEED)
        w_, _, _, _ = adh_fit(d, 7, ctrl, t_treat=1975, starts=k)
        v_starts[k] = {'loss': loss_, 'donors': [names[u] for u, x in zip(ctrl, w_) if x > 0.05]}
    # leave-one-out: drop each donor with positive weight
    w0, _, _, _ = adh_fit(d, 7, ctrl)
    loo = {}
    for u, x in zip(ctrl, w0):
        if x > 0.01:
            c2 = [c for c in ctrl if c != u]
            wl, _, _, _ = adh_fit(d, 7, c2, starts=2)
            loo[names[u]] = Y[c2].values @ wl
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
    ax[0].barh(range(len(rank)), [ratios[k] for k in rank][::-1],
               color=[st.IDAred if k == 'West Germany' else st.MainBlue for k in rank][::-1])
    ax[0].set_yticks(range(len(rank)))
    ax[0].set_yticklabels(rank[::-1], fontsize=8)
    ax[0].set_xlabel('post/pre RMSPE ratio')
    ax[0].set_title('In-space placebos', fontsize=11)
    sel = yrs <= 1990
    ax[1].plot(yrs[sel], Y[7].values[sel], color=st.IDAred, lw=2, label='West Germany')
    ax[1].plot(yrs[sel], s75[sel], color=st.MainBlue, lw=2, ls='--', label='synthetic (outcomes 1960-1974)')
    ax[1].axvline(1975, color=st.Amber, ls=':', lw=1)
    ax[1].set_title('In-time placebo: 1975', fontsize=11)
    st.legend_outside_bottom(ax[1], ncol=2, y=-0.16)
    ax[2].plot(yrs, Y[7].values, color=st.IDAred, lw=2, label='West Germany')
    ax[2].plot(yrs, Y[ctrl].values @ w0, color=st.MainBlue, lw=2, ls='--', label='synthetic')
    for i, (k, s) in enumerate(loo.items()):
        ax[2].plot(yrs, s, color=st.Teal, lw=1, alpha=0.8, label='leave-one-out' if i == 0 else '_')
    ax[2].axvline(1990, color=st.Amber, ls=':', lw=1)
    ax[2].set_title('Leave one donor out', fontsize=11)
    st.legend_outside_bottom(ax[2], ncol=2, y=-0.16)
    plt.tight_layout()
    save('ats_ch14_germany_placebo', save_it)
    g75 = Y[7].values - s75
    return {'ratios': ratios, 'rank': rank, 'p': p, 'n_units': len(units), 'second': rank[1] if rank[0] == 'West Germany' else rank[0],
            'ratio_wg': ratios['West Germany'],
            'gap75_1980s': float(np.mean(g75[(yrs >= 1975) & (yrs <= 1990)])),
            'rel75': float(np.mean(g75[(yrs >= 1975) & (yrs <= 1990)] / s75[(yrs >= 1975) & (yrs <= 1990)])),
            'rmspe75': float(np.sqrt(np.mean(g75[pre75] ** 2))), 'v_starts': v_starts,
            'loo_dropped': list(loo),
            'loo_gap2003': {k: float(Y[7].values[-1] - s[-1]) for k, s in loo.items()}}


# =============================================================================
# 6. THE BREXIT DOPPELGANGER (BORN ET AL. 2019)
# =============================================================================
def bmss_fit(U, unit, donors, pre_end):
    """Outcome-only doppelganger: weights matching real GDP (1995 = 1) over 1995Q1 to pre_end."""
    pre = U.loc[:pre_end]
    return sc_weights(pre[unit].values, pre[donors].values)


def fig_brexit(save_it=True):
    U = oecd_gdp().loc[:'2019-Q4']
    donors = BMSS['donors']
    w = bmss_fit(U, 'GBR', donors, BMSS['pre'][1])
    synth = U[donors].values @ w
    uk = U['GBR'].values
    q = list(U.index)
    i0 = q.index(BMSS['pre'][1])
    base = uk[i0]
    gap = 100 * (uk - synth) / base
    pre_sd = float(np.std(gap[:i0 + 1], ddof=1))
    rmspe = float(np.sqrt(np.mean(gap[:i0 + 1] ** 2)))
    # time placebos: fictitious votes in every quarter 2010Q1-2016Q1
    tp = {}
    for qq in [x for x in q if '2010-Q1' <= x <= '2016-Q1']:
        wp = bmss_fit(U, 'GBR', donors, qq)
        tp[qq] = U[donors].values @ wp
    # country placebos: RMSPE ratio over 2016Q3-2018Q4
    j1 = q.index(BMSS['end'])
    ratios = {}
    for u in ['GBR'] + donors:
        others = [c for c in donors + ['GBR'] if c != u]
        wu = bmss_fit(U, u, others, BMSS['pre'][1])
        g = U[u].values - U[others].values @ wu
        ratios[u] = float(np.sqrt(np.mean(g[i0 + 1:j1 + 1] ** 2)) / np.sqrt(np.mean(g[:i0 + 1] ** 2)))
    rank = sorted(ratios, key=lambda k: -ratios[k])
    x = pd.PeriodIndex(q, freq='Q').to_timestamp()
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.9))
    s = x >= '2014-01-01'
    for i, (k, v) in enumerate(tp.items()):
        ax[0].plot(x[s], 100 * (v[s] / base - 1), color=st.Teal, lw=0.8, alpha=0.6, label='time placebos 2010Q1-2016Q1' if i == 0 else '_')
    ax[0].plot(x[s], 100 * (uk[s] / base - 1), color=st.IDAred, lw=2, label='United Kingdom')
    ax[0].plot(x[s], 100 * (synth[s] / base - 1), color=st.MainBlue, lw=2, ls='--', label='doppelganger')
    ax[0].fill_between(x[s], 100 * (synth[s] / base - 1) - pre_sd, 100 * (synth[s] / base - 1) + pre_sd, color=st.MainBlue, alpha=0.12,
                       label='+/- 1 sd of the pre-vote gap')
    ax[0].axvline(pd.Timestamp('2016-07-01'), color=st.Amber, ls=':', lw=1)
    ax[0].set_ylabel('% deviation from 2016Q2')
    st.legend_outside_bottom(ax[0], ncol=2, y=-0.16)
    top = rank[:12]
    ax[1].barh(range(len(top)), [ratios[k] for k in top][::-1],
               color=[st.IDAred if k == 'GBR' else st.MainBlue for k in top][::-1])
    ax[1].set_yticks(range(len(top)))
    ax[1].set_yticklabels(top[::-1], fontsize=10)
    ax[1].set_xlabel('post/pre RMSPE ratio, 2016Q3-2018Q4 (12 largest of 24)')
    datefmt(ax[0])
    plt.tight_layout()
    save('ats_ch14_brexit', save_it)
    k18 = q.index('2018-Q4')
    k19 = q.index('2019-Q4')
    tp_gap = {k: float(100 * (uk[k18] - v[k18]) / base) for k, v in tp.items()}
    return {'weights': {c: float(x_) for c, x_ in zip(donors, w) if x_ > 0.005}, 'published': BMSS['published'],
            'gap2018': float(gap[k18]), 'gap2019': float(gap[k19]), 'gap2017': float(gap[q.index('2017-Q4')]),
            'pre_sd': pre_sd, 'rmspe': rmspe, 'rank_uk': rank.index('GBR') + 1, 'n_units': len(rank),
            'p': (rank.index('GBR') + 1) / len(rank), 'tp_min': min(tp_gap.values()), 'tp_max': max(tp_gap.values()),
            'n_tp': len(tp), 'top': rank[:3]}


# =============================================================================
# 7. ROMANIA 2025: SYNTHETIC CONTROL FAMILY
# =============================================================================
def ro_panel(ct=False, pre_start=RO_SC['pre_start'], end=RO_SC['end'], donors=None):
    """Units x periods matrix of annual HICP inflation, donors first, Romania last."""
    A = hicp_annual(ct).loc[pre_start:end]
    donors = donors or [c for c in EU27 if c != 'RO']
    A = A[donors + ['RO']].dropna(axis=0)
    return A, donors


def ro_estimates(A, donors, T0=RO_SC['T0'], grid=(0.1, 1, 10, 100, 1000)):
    """Four counterfactuals for Romania: SC (no intercept), demeaned SC, ridge-augmented demeaned SC, SDID."""
    pre = A.index <= T0
    y1, Y0 = A['RO'].values, A[donors].values
    w = sc_weights(y1[pre], Y0[pre])
    sc = Y0 @ w
    wd, c = sc_demeaned(y1[pre], Y0[pre])
    dsc = Y0 @ wd + c
    y1c, Y0c = y1 - y1[pre].mean(), Y0 - Y0[pre].mean(0)
    lam, _ = ascm_lambda(y1c[pre], Y0c[pre], grid, holdout=6)
    wd2 = sc_weights(y1c[pre], Y0c[pre])
    _, w_aug, _ = ascm_ridge(y1c[pre], Y0c[pre], Y0c[~pre], wd2, lam)
    asc = Y0c @ w_aug + y1[pre].mean()
    Ymat = np.vstack([Y0.T, y1[None, :]])
    T0i = int(pre.sum())
    sd = sdid(Ymat, 1, T0i)
    sdid_cf = np.r_[np.full(T0i, np.nan), y1[~pre] - sd['per']]
    return {'SC': (sc, w), 'demeaned SC': (dsc, wd), 'augmented SC': (asc, w_aug), 'SDID': (sdid_cf, sd['omega'])}, sd, lam


def fig_ro_sc(save_it=True):
    A, donors = ro_panel()
    T0 = RO_SC['T0']
    pre = A.index <= T0
    ev = (A.index > T0) & (A.index <= RO_SC['eval_end'])
    est, sd, lam = ro_estimates(A, donors)
    y1 = A['RO'].values
    out = {'T0': T0, 'pre_start': RO_SC['pre_start'], 'end': str(A.index[-1].date()), 'n_pre': int(pre.sum()),
           'lambda': lam, 'zeta': sd['zeta'], 'est': {}}
    for k, (cf, w) in est.items():
        gap = y1 - cf
        out['est'][k] = {'avg': float(np.nanmean(gap[ev])), 'rmspe_pre': float(np.sqrt(np.nanmean(gap[pre] ** 2))) if k != 'SDID' else None,
                         'aug26': float(gap[A.index == '2026-08-01'][0]) if (A.index == '2026-08-01').any() else None,
                         'aug25': float(gap[A.index == '2025-08-01'][0]), 'jul25': float(gap[A.index == '2025-07-01'][0]),
                         'weights': {c: float(x) for c, x in zip(donors, w) if abs(x) > 0.02}}
    se, taus = sdid_placebo_se(np.vstack([A[donors].values.T, y1[None, :]]), int(pre.sum()))
    out['sdid_se'] = se
    # per-period SDID average over the evaluation window only
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.9))
    x = A.index
    ax[0].plot(x, y1, color=st.IDAred, lw=2.2, label='Romania')
    cols = {'SC': st.Amber, 'demeaned SC': st.MainBlue, 'augmented SC': st.Forest, 'SDID': st.Purple}
    for k, (cf, w) in est.items():
        ax[0].plot(x, cf, color=cols[k], lw=1.4, ls='--', label=k)
        ax[1].plot(x, y1 - cf, color=cols[k], lw=1.6, label=k)
    for a in ax:
        a.axvline(pd.Timestamp('2025-06-15'), color=st.DarkText, ls=':', lw=1)
    ax[0].set_ylabel('HICP inflation, % y/y')
    ax[1].axhline(0, color=st.DarkText, lw=0.6)
    ax[1].set_ylabel('gap, percentage points')
    st.fig_legend_bottom(fig, ncol=5, y=-0.01)
    datefmt(*ax)
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    save('ats_ch14_ro_sc', save_it)
    return out


def fig_ro_placebo(save_it=True):
    """In-space placebos for the demeaned SC: gaps of all 27 countries and the post/pre RMSPE ratio over
    July 2025 - June 2026."""
    A, donors = ro_panel()
    A = A.loc[:RO_SC['eval_end']]
    T0i = int((A.index <= RO_SC['T0']).sum())
    Y = A[donors + ['RO']].values.T
    gaps, ratios, p = placebo_ratios(Y, T0i, method='demeaned')
    units = donors + ['RO']
    rank = [units[i] for i in np.argsort(-ratios)]
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.9))
    for i, u in enumerate(units[:-1]):
        ax[0].plot(A.index, gaps[i], color=st.Teal, lw=0.7, alpha=0.6, label='placebo countries' if i == 0 else '_')
    ax[0].plot(A.index, gaps[-1], color=st.IDAred, lw=2.2, label='Romania')
    ax[0].axvline(pd.Timestamp('2025-06-15'), color=st.DarkText, ls=':', lw=1)
    ax[0].axhline(0, color=st.DarkText, lw=0.6)
    ax[0].set_ylabel('gap, percentage points')
    st.legend_outside_bottom(ax[0], ncol=2, y=-0.16)
    srt = np.argsort(ratios)[-12:]
    ax[1].barh(range(len(srt)), ratios[srt], color=[st.IDAred if units[i] == 'RO' else st.MainBlue for i in srt])
    ax[1].set_yticks(range(len(srt)))
    ax[1].set_yticklabels([units[i] for i in srt], fontsize=10)
    ax[1].set_xlabel('post/pre RMSPE ratio (12 largest of 27)')
    datefmt(ax[0])
    plt.tight_layout()
    save('ats_ch14_ro_placebo', save_it)
    return {'p': p, 'rank_ro': rank.index('RO') + 1, 'n': len(units), 'ratio_ro': float(ratios[-1]),
            'second': rank[1] if rank[0] == 'RO' else rank[0], 'ratio_second': float(sorted(ratios)[-2])}


def fig_ro_tax(save_it=True):
    """The tax component: Romanian HICP against the HICP at constant tax rates (Eurostat, full and immediate
    pass-through of tax changes by construction); the demeaned SC applied to the constant-tax inflation of all
    countries estimates the non-tax part of the effect."""
    A, donors = ro_panel()
    C, _ = ro_panel(ct=True)
    idx = A.index.intersection(C.index)
    A, C = A.loc[idx], C.loc[idx]
    pre = idx <= RO_SC['T0']
    ev = (idx > RO_SC['T0']) & (idx <= RO_SC['eval_end'])
    wd, c = sc_demeaned(A['RO'].values[pre], A[donors].values[pre])
    g_all = A['RO'].values - (A[donors].values @ wd + c)
    wc, cc = sc_demeaned(C['RO'].values[pre], C[donors].values[pre])
    g_ct = C['RO'].values - (C[donors].values @ wc + cc)
    tax = A['RO'] - C['RO']
    tax_pre = float(tax[pre].mean())
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.9))
    ax[0].plot(idx, A['RO'], color=st.IDAred, lw=2, label='HICP')
    ax[0].plot(idx, C['RO'], color=st.MainBlue, lw=2, ls='--', label='HICP at constant tax rates')
    ax[0].axvline(pd.Timestamp('2025-06-15'), color=st.DarkText, ls=':', lw=1)
    ax[0].set_ylabel('Romania, % y/y')
    st.legend_outside_bottom(ax[0], ncol=2, y=-0.16)
    ax[1].plot(idx, g_all, color=st.IDAred, lw=2, label='gap, HICP (total effect)')
    ax[1].plot(idx, g_ct, color=st.MainBlue, lw=2, ls='--', label='gap, constant-tax HICP (non-tax part)')
    ax[1].plot(idx, tax - tax_pre, color=st.Forest, lw=1.6, label='HICP minus constant-tax HICP (tax part)')
    ax[1].axhline(0, color=st.DarkText, lw=0.6)
    ax[1].axvline(pd.Timestamp('2025-06-15'), color=st.DarkText, ls=':', lw=1)
    ax[1].set_ylabel('percentage points')
    st.legend_outside_bottom(ax[1], ncol=2, y=-0.16)
    datefmt(*ax)
    plt.tight_layout()
    save('ats_ch14_ro_tax', save_it)
    return {'avg_total': float(g_all[ev].mean()), 'avg_ct': float(g_ct[ev].mean()),
            'avg_tax': float((tax[ev] - tax_pre).mean()), 'tax_pre': tax_pre,
            'tax_aug25': float(tax.loc['2025-08-01'] - tax_pre), 'tax_jul25': float(tax.loc['2025-07-01'] - tax_pre),
            'ct_jul25': float(g_ct[idx == '2025-07-01'][0]), 'ct_end': str(idx[-1].date())}


# =============================================================================
# 8. STAGGERED ADOPTION
# =============================================================================
def fig_staggered(save_it=True, K=8):
    df = sim_staggered(seed=SEED, slope=STAG_SLOPES)
    tw, tw_static = twfe_event(df, K)
    cs, cs_all = cs_att(df, K)
    post = df[df['d'] == 1].copy()
    post['k'] = post['t'] - post['g']
    post['te'] = post['g'].map(STAG_SLOPES) * (post['k'] + 1)
    tk = post[post['k'] <= K].groupby('k')['te'].mean().to_dict()
    truth = {k: (tk.get(k, np.nan) if k >= 0 else 0.0) for k in range(-K, K + 1)}
    true_att = float(post['te'].mean())
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ks = list(range(-K, K + 1))
    ax.plot(ks, [truth[k] for k in ks], color=st.Forest, lw=2, label='true effect by exposure')
    ax.plot([k for k in ks if k in tw], [tw[k] for k in ks if k in tw], 's--', color=st.IDAred, label='TWFE event study')
    ax.plot([k for k in ks if k in cs], [cs[k] for k in ks if k in cs], 'o-', color=st.MainBlue, label="Callaway-Sant'Anna")
    ax.axvline(-0.5, color=st.DarkText, ls=':', lw=1)
    ax.axhline(0, color=st.DarkText, lw=0.6)
    ax.set_xlabel('periods since adoption')
    ax.set_ylabel('effect')
    st.legend_outside_bottom(ax, ncol=3, y=-0.18)
    save('ats_ch14_staggered', save_it)
    return {'twfe_static': tw_static, 'cs_all': cs_all, 'true_att': true_att, 'tw_m5': float(tw[-5]), 'cs_m5': float(cs[-5]),
            'tw_8': float(tw[K]), 'cs_8': float(cs[K]), 'true_8': float(truth[K]),
            'tw_4': float(tw[4]), 'cs_4': float(cs[4]), 'true_4': float(truth[4])}


# =============================================================================
# 9. BSTS / CAUSALIMPACT: THE SPOT BITCOIN ETF
# =============================================================================
def btc_data(start=BTC['start'], end=BTC['end'], extra=()):
    names = ['btc'] + list(BTC['controls']) + list(extra)
    W = weekly_logrv(names, start=pd.Timestamp(start) - pd.Timedelta(days=7), end=end)
    return W.loc[start:end]


def fig_btc(save_it=True, draws=1000):
    W = btc_data()
    ci = causal_impact(W['btc'], W[list(BTC['controls'])], BTC['T0'], draws=draws, seed=SEED)
    We = btc_data(extra=('eth',))
    ci_eth = causal_impact(We['btc'], We[list(BTC['controls']) + ['eth']], BTC['T0'], draws=draws, seed=SEED)
    Wa = btc_data()
    ci_a = causal_impact(Wa['btc'], Wa[list(BTC['controls'])], BTC['anticip'], draws=draws, seed=SEED)
    x = W.index
    post = x > BTC['T0']
    fig, ax = plt.subplots(3, 1, figsize=(12, 5.4), sharex=True)
    ax[0].plot(x, W['btc'], color=st.IDAred, lw=1.6, label='Bitcoin weekly log RV')
    ax[0].plot(x[post], ci['pred'], color=st.MainBlue, lw=1.6, ls='--', label='counterfactual')
    ax[0].fill_between(x[post], ci['pred_lo'], ci['pred_hi'], color=st.MainBlue, alpha=0.15, label='95% interval')
    ax[1].plot(x[post], ci['effect'], color=st.IDAred, lw=1.4, label='pointwise effect')
    ax[1].fill_between(x[post], ci['lo'], ci['hi'], color=st.IDAred, alpha=0.15, label='_')
    ax[1].axhline(0, color=st.DarkText, lw=0.6)
    ax[2].plot(x[post], ci['cum'], color=st.Forest, lw=1.6, label='cumulative effect')
    ax[2].fill_between(x[post], ci['cum_lo'], ci['cum_hi'], color=st.Forest, alpha=0.15, label='_')
    ax[2].axhline(0, color=st.DarkText, lw=0.6)
    for a in ax:
        a.axvline(pd.Timestamp('2024-01-10'), color=st.Amber, ls=':', lw=1)
    ax[0].axvline(pd.Timestamp('2023-06-15'), color=st.Purple, ls=':', lw=1)
    ax[0].axvline(pd.Timestamp('2023-08-29'), color=st.Purple, ls=':', lw=1)
    st.fig_legend_bottom(fig, ncol=5, y=-0.0)
    datefmt(*ax)
    plt.tight_layout(rect=(0, 0.05, 1, 1))
    save('ats_ch14_btc', save_it)
    return {'avg': ci['avg'], 'avg_lo': ci['avg_lo'], 'avg_hi': ci['avg_hi'], 'p': ci['p'],
            'pct': float(100 * (np.exp(ci['avg']) - 1)), 'cum_end': float(ci['cum'][-1]),
            'cum_lo': float(ci['cum_lo'][-1]), 'cum_hi': float(ci['cum_hi'][-1]),
            'n_pre': int((~post).sum()), 'n_post': int(post.sum()), 'params': ci['params'],
            'eth_avg': ci_eth['avg'], 'eth_lo': ci_eth['avg_lo'], 'eth_hi': ci_eth['avg_hi'], 'eth_p': ci_eth['p'],
            'ant_avg': ci_a['avg'], 'ant_lo': ci_a['avg_lo'], 'ant_hi': ci_a['avg_hi'], 'ant_p': ci_a['p'],
            'draws': draws, 'start': BTC['start'], 'end': BTC['end']}


def fig_btc_placebo(save_it=True, draws=400, n_post=25):
    """Placebo dates: the same analysis with fictitious approval dates in 2019-2022 (25 post weeks each), and the
    distribution of the estimated average effects."""
    W = weekly_logrv(['btc'] + list(BTC['controls']), start='2017-01-01', end=BTC['end'])
    dates = pd.date_range('2019-01-06', '2022-06-26', freq='13W-SUN')
    eff = []
    for d0 in dates:
        sub = W.loc[d0 - pd.Timedelta(weeks=53):d0 + pd.Timedelta(weeks=n_post)]
        ci = causal_impact(sub['btc'], sub[list(BTC['controls'])], d0, draws=draws, seed=SEED)
        eff.append((str(d0.date()), ci['avg'], ci['avg_lo'], ci['avg_hi']))
    sub = W.loc[pd.Timestamp(BTC['T0']) - pd.Timedelta(weeks=53):BTC['end']]
    ci = causal_impact(sub['btc'], sub[list(BTC['controls'])], BTC['T0'], draws=draws, seed=SEED)
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    xs = np.arange(len(eff))
    ax.errorbar(xs, [e[1] for e in eff], yerr=[[e[1] - e[2] for e in eff], [e[3] - e[1] for e in eff]], fmt='o',
                color=st.MainBlue, label='placebo approval dates')
    ax.errorbar([len(eff)], [ci['avg']], yerr=[[ci['avg'] - ci['avg_lo']], [ci['avg_hi'] - ci['avg']]], fmt='s',
                color=st.IDAred, label='10 January 2024')
    ax.axhline(0, color=st.DarkText, lw=0.6)
    ax.set_xticks(list(xs) + [len(eff)])
    ax.set_xticklabels([e[0][:7] for e in eff] + ['2024-01'], rotation=60, fontsize=8)
    ax.set_ylabel('average effect on log RV')
    st.legend_outside_bottom(ax, ncol=2, y=-0.35)
    save('ats_ch14_btc_placebo', save_it)
    n_excl = sum(1 for e in eff if e[2] > 0 or e[3] < 0)
    return {'n': len(eff), 'n_excl0': n_excl, 'avg53': ci['avg'], 'lo53': ci['avg_lo'], 'hi53': ci['avg_hi'],
            'sd_placebo': float(np.std([e[1] for e in eff], ddof=1)), 'eff': eff}


# =============================================================================
# 10. DML
# =============================================================================
def fig_dml(save_it=True, reps=60, T=1000, theta=0.5):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression

    def rf():
        return RandomForestRegressor(n_estimators=150, min_samples_leaf=2, max_features=1.0, random_state=0, n_jobs=1)
    est = {'OLS with linear controls': [], 'DML, random forest, blocked folds': []}
    cover = 0
    for r in range(reps):
        y, d, X = sim_dml(T, theta, seed=SEED + r)
        b, V, _ = ols_hac(y, np.column_stack([np.ones(T), d, X]))
        est['OLS with linear controls'].append(b[1])
        res = dml_plr(y, d, X, rf, K=5, gap=5)
        est['DML, random forest, blocked folds'].append(res['theta'])
        cover += abs(res['theta'] - theta) <= 1.96 * res['se']
    fig, ax = plt.subplots(figsize=(9, 3.6))
    cols = [st.IDAred, st.MainBlue]
    for (k, v), c in zip(est.items(), cols):
        ax.hist(v, bins=20, color=c, alpha=0.6, label=k)
    ax.axvline(theta, color=st.Forest, lw=2, label='true theta')
    ax.set_xlabel('estimate of theta')
    st.legend_outside_bottom(ax, ncol=3, y=-0.2)
    save('ats_ch14_dml', save_it)
    _ = LinearRegression
    return {'reps': reps, 'T': T, 'theta': theta,
            'mean': {k: float(np.mean(v)) for k, v in est.items()}, 'sd': {k: float(np.std(v, ddof=1)) for k, v in est.items()},
            'cover': cover / reps}


# =============================================================================
# 11. AI MINI-CASE: SPECIFICATION CURVE FOR ROMANIA
# =============================================================================
def fig_ai_case(save_it=True):
    pools = {'EU-26': [c for c in EU27 if c != 'RO'], 'euro area': EURO_AREA,
             'non-euro EU': [c for c in EU27 if c not in EURO_AREA and c != 'RO']}
    starts = ['2017-01-01', '2019-01-01', '2023-07-01', '2024-01-01']
    rows = []
    for pn, pool in pools.items():
        for s in starts:
            A, donors = ro_panel(pre_start=s, donors=pool)
            if s < '2021-01-01':
                # pre-period without the 2021-2023 surge: estimation on the months outside July 2021-June 2023
                keep = ~((A.index >= '2021-07-01') & (A.index <= '2023-06-01'))
                A = A[keep]
            ev = (A.index > RO_SC['T0']) & (A.index <= RO_SC['eval_end'])
            est, sd, lam = ro_estimates(A, donors)
            for k, (cf, w) in est.items():
                g = A['RO'].values - cf
                rows.append({'pool': pn, 'start': s, 'method': k, 'avg': float(np.nanmean(g[ev]))})
    R = pd.DataFrame(rows).sort_values('avg').reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    cols = {'SC': st.Amber, 'demeaned SC': st.MainBlue, 'augmented SC': st.Forest, 'SDID': st.Purple}
    for k, c in cols.items():
        s = R[R['method'] == k]
        ax.scatter(s.index, s['avg'], color=c, s=28, label=k)
    ax.axhline(0, color=st.DarkText, lw=0.6)
    ax.set_xlabel('specification (sorted by the estimate)')
    ax.set_ylabel('average gap Jul 2025 - Jun 2026, pp')
    st.legend_outside_bottom(ax, ncol=4, y=-0.2)
    save('ats_ch14_ai_case', save_it)
    noSC = R[R['method'] != 'SC']
    return {'n': len(R), 'min': float(R['avg'].min()), 'max': float(R['avg'].max()), 'med': float(R['avg'].median()),
            'min_noSC': float(noSC['avg'].min()), 'max_noSC': float(noSC['avg'].max()), 'med_noSC': float(noSC['avg'].median()),
            'n_neg': int((R['avg'] <= 0).sum()), 'by_method': R.groupby('method')['avg'].median().to_dict(),
            'by_pool': R.groupby('pool')['avg'].median().to_dict(), 'rows': rows}


# =============================================================================
# RUN
# =============================================================================
STEPS = {'overview': fig_overview, 'granger_sim': fig_granger_sim, 'granger_markets': fig_granger_markets, 'te': fig_te,
         'pcmci_sim': fig_pcmci_sim, 'pcmci_vol': fig_pcmci_vol, 'ccm': fig_ccm, 'its': fig_its, 'event': fig_event,
         'germany': fig_germany, 'germany_placebo': fig_germany_placebo, 'brexit': fig_brexit, 'ro_sc': fig_ro_sc,
         'ro_placebo': fig_ro_placebo, 'ro_tax': fig_ro_tax, 'staggered': fig_staggered, 'btc': fig_btc,
         'btc_placebo': fig_btc_placebo, 'dml': fig_dml, 'ai': fig_ai_case}


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x


if __name__ == '__main__':
    st.apply()
    path = os.path.join(HERE, 'ch14_numbers.json')
    out = json.load(open(path)) if os.path.exists(path) else {}
    for k in (sys.argv[1:] or list(STEPS)):
        print('---', k)
        out[k] = _json(STEPS[k]())
        json.dump(out, open(path, 'w'), indent=1)
    print('saved', path)
