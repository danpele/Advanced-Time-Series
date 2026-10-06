"""
prepare_realized_data.py -- the intraday and realised-measure data of Chapter 8 (ATS), saved once in data/realized
==================================================================================================================
Two public sources, no account and no key:

  1. The Oxford-Man Institute's realized library, version 0.3 (Heber, Lunde, Shephard and Sheppard 2009), daily
     realised measures of 31 equity indices, 3 January 2000 - 25 February 2022. The library was discontinued in 2022;
     the last public file (oxfordmanrealizedvolatilityindices.zip, 28 February 2022) is preserved by the Internet
     Archive. Terms of the library: "Researchers may use this library freely without restrictions so long as they
     quote in any work which uses it: Heber, Gerd, Asger Lunde, Neil Shephard and Kevin K. Sheppard (2009)
     'Oxford-Man Institute's realized library', Oxford-Man Institute, University of Oxford. The quotation should
     include the version number of the library."  We keep six indices and the main measures. The library is not
     redistributed with the course: ats_data.read_omi downloads the archived file and extracts the six indices; the
     local copy below (instructor's machine) is git-ignored:
       data/realized/omi_realized_library_v03.csv

  2. Binance public market data (https://data.binance.vision): one-minute klines of BTCUSDT and ETHUSDT, January
     2018 - 18 September 2026 (UTC days, 1440 one-minute returns a day), from which we compute our own daily realised
     measures; one-second klines of August 2026 for the signature plot and the Epps effect:
       data/realized/binance_daily_realized.csv          daily RV, BV, RQ, TQ, realised kernel, semivariances, RCov
       data/realized/binance_signature_2026-08.csv       average RV and realised correlation by sampling interval
       data/realized/binance_1s_2026-08-05.csv.gz        one day of one-second prices (BTC and ETH)

Downloads are cached in ~/.cache/ats_ch8 (outside the repository).
Run:  OMP_NUM_THREADS=1 python3 Quantlets/Ch_08/prepare_realized_data.py
Advanced Time Series Analysis and Forecasting - Daniel Traian PELE
"""

import io
import os
import sys
import urllib.request
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
from ats_data import read_omi   # noqa: E402  (OMI_URL, OMI_SYMBOLS, OMI_COLS live in ats_data)
OUT = os.path.join(HERE, '..', '..', 'data', 'realized')
CACHE = os.path.expanduser('~/.cache/ats_ch8')
BIN = 'https://data.binance.vision/data/spot'
END = '2026-09-18'


def fetch(url, name):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=300) as r, open(p, 'wb') as f:
            f.write(r.read())
    return p


# =============================================================================
# 1. OXFORD-MAN REALIZED LIBRARY (v0.3, Internet Archive copy)
# =============================================================================
def omi():
    """Local (git-ignored) copy of the six indices, extracted by ats_data.read_omi from the archived file."""
    d = read_omi(local=False)
    d.to_csv(os.path.join(OUT, 'omi_realized_library_v03.csv'), index=False, float_format='%.6g')
    print('OMI', d.shape, d['date'].min().date(), d['date'].max().date())


# =============================================================================
# 2. BINANCE ONE-MINUTE KLINES -> DAILY REALISED MEASURES
# =============================================================================
def klines(symbol, interval, period, daily=False):
    kind = 'daily' if daily else 'monthly'
    name = f'{symbol}-{interval}-{period}.zip'
    p = fetch(f'{BIN}/{kind}/klines/{symbol}/{interval}/{name}', name)
    with zipfile.ZipFile(p) as z:
        raw = z.open(z.namelist()[0]).read()
    t = pd.read_csv(io.BytesIO(raw), header=None, usecols=[0, 4])
    if not str(t.iloc[0, 0]).isdigit():          # some files carry a header line
        t = t.iloc[1:].astype(float)
    ts = t.iloc[:, 0].astype('int64')
    unit = 'us' if ts.iloc[0] > 10 ** 14 else 'ms'   # Binance switched to microseconds in 2025
    return pd.Series(t.iloc[:, 1].astype(float).values, index=pd.to_datetime(ts.values, unit=unit), name=symbol)


def minute_grid(s, day):
    """Last price on the 1440 one-minute marks of a UTC day (previous-tick), with the close of the previous day."""
    grid = pd.date_range(day - pd.Timedelta(minutes=1), periods=1441, freq='1min')
    g = s.reindex(s.index.union(grid)).ffill().reindex(grid)
    return g


def parzen(x):
    x = np.abs(x)
    return np.where(x <= 0.5, 1 - 6 * x ** 2 + 6 * x ** 3, np.where(x <= 1, 2 * (1 - x) ** 3, 0.0))


def realised_kernel(r, H):
    """Flat-top-free realised kernel of Barndorff-Nielsen, Hansen, Lunde and Shephard (2008), Parzen weights."""
    rk = r @ r
    for h in range(1, H + 1):
        rk += 2 * parzen(h / (H + 1)) * (r[h:] @ r[:-h])
    return rk


def kernel_bandwidth(r_fine, r_sparse, n):
    """BNHLS (2009, Econometrics Journal) rule: H = c* xi^(4/5) n^(3/5), c* = 3.5134 for Parzen;
    omega^2 from the fine returns (RV/2n), IV from the sparse (20-minute) RV."""
    omega2 = (r_fine @ r_fine) / (2 * n)
    iv = r_sparse @ r_sparse
    xi2 = omega2 / max(iv, 1e-12)
    return max(1, int(np.ceil(3.5134 * xi2 ** 0.4 * n ** 0.6)))


MU1 = np.sqrt(2 / np.pi)


def daily_measures(p):
    """p: 1441 log prices (previous close + 1440 minutes). Returns a dict of realised measures (returns in %)."""
    from math import gamma
    mu43 = 2 ** (2 / 3) * gamma(7 / 6) / gamma(1 / 2)
    out = {}
    lp = 100 * np.log(p)
    r1 = np.diff(lp)
    out['ret'] = lp[-1] - lp[0]
    for k in (1, 5, 15, 30, 60):
        rk_ = np.diff(lp[::k])
        out[f'rv{k}'] = rk_ @ rk_
    # subsampled 5-minute RV (average over the 5 offsets)
    out['rv5_ss'] = np.mean([np.sum(np.diff(lp[o::5]) ** 2) for o in range(5)])
    r5 = np.diff(lp[::5])
    n5 = len(r5)
    out['bv5'] = MU1 ** -2 * n5 / (n5 - 1) * np.sum(np.abs(r5[1:]) * np.abs(r5[:-1]))
    out['bv1'] = MU1 ** -2 * len(r1) / (len(r1) - 1) * np.sum(np.abs(r1[1:]) * np.abs(r1[:-1]))
    out['rq5'] = n5 / 3 * np.sum(r5 ** 4)
    out['tq5'] = n5 * mu43 ** -3 * n5 / (n5 - 2) * np.sum(np.prod([np.abs(r5[2:]), np.abs(r5[1:-1]), np.abs(r5[:-2])], 0) ** (4 / 3))
    out['medrv5'] = np.pi / (6 - 4 * np.sqrt(3) + np.pi) * n5 / (n5 - 2) * np.sum(
        np.median(np.vstack([np.abs(r5[2:]), np.abs(r5[1:-1]), np.abs(r5[:-2])]), 0) ** 2)
    out['rsn5'] = np.sum(r5[r5 < 0] ** 2)
    out['rsp5'] = np.sum(r5[r5 > 0] ** 2)
    H = kernel_bandwidth(r1, np.diff(lp[::20]), len(r1))
    out['rk1'] = realised_kernel(r1, H)
    out['rk_H'] = H
    return out


def binance_daily(symbols=('BTCUSDT', 'ETHUSDT'), start='2018-01', end=END):
    months = pd.period_range(start, end[:7], freq='M')
    frames = []
    tail = {}
    for m in months:
        ss = {}
        for s in symbols:
            cur = klines(s, '1m', str(m))
            ss[s] = pd.concat([tail[s], cur]) if s in tail else cur
            tail[s] = cur.iloc[-5:]
        days = pd.date_range(m.start_time, min(m.end_time, pd.Timestamp(end)), freq='D').normalize()
        for d in days:
            row = {'date': d}
            grids = {}
            for s in symbols:
                x = ss[s]
                prev = x.loc[:d - pd.Timedelta(minutes=1)]
                g = minute_grid(x, d) if len(prev) else None
                if g is None or g.isna().any():
                    continue
                inday = x.loc[d:d + pd.Timedelta(hours=23, minutes=59)]
                if len(inday) < 1300:                      # exchange outage: skip the day
                    continue
                grids[s] = g.values
                key = s[:3].lower()
                row.update({f'{key}_{k}': v for k, v in daily_measures(g.values).items()})
                row[f'{key}_nmin'] = len(inday)
            if len(grids) == 2:
                a, b = (100 * np.diff(np.log(grids[s])) for s in symbols)
                row['rcov1'] = a @ b
                a5, b5 = (100 * np.diff(np.log(grids[s][::5])) for s in symbols)
                row['rcov5'] = a5 @ b5
            if len(row) > 1:
                frames.append(row)
        print('Binance', m, len(frames))
    d = pd.DataFrame(frames).set_index('date').sort_index()
    d.to_csv(os.path.join(OUT, 'binance_daily_realized.csv'), float_format='%.6g')
    print('Binance daily', d.shape)


# =============================================================================
# 3. ONE-SECOND KLINES (AUGUST 2026): SIGNATURE PLOT AND EPPS EFFECT
# =============================================================================
SECS = [1, 2, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600]


def binance_seconds(month='2026-08', keep_day='2026-08-05'):
    bt = klines('BTCUSDT', '1s', month)
    et = klines('ETHUSDT', '1s', month)
    rows = []
    for d in pd.date_range(month + '-01', periods=pd.Period(month).days_in_month, freq='D'):
        grid = pd.date_range(d, periods=86401, freq='1s')
        pb = bt.reindex(bt.index.union(grid)).ffill().reindex(grid).values
        pe = et.reindex(et.index.union(grid)).ffill().reindex(grid).values
        if np.isnan(pb).any() or np.isnan(pe).any():
            continue
        lb, le = 100 * np.log(pb), 100 * np.log(pe)
        row = {'date': d}
        for k in SECS:
            # average over offsets (subsampling) to remove the dependence on the starting second
            offs = range(0, k, max(1, k // 10))
            rvb = np.mean([np.sum(np.diff(lb[o::k]) ** 2) * 86400 / (86400 - o) for o in offs])
            rve = np.mean([np.sum(np.diff(le[o::k]) ** 2) * 86400 / (86400 - o) for o in offs])
            cbe = np.mean([np.sum(np.diff(lb[o::k]) * np.diff(le[o::k])) * 86400 / (86400 - o) for o in offs])
            row[f'btc_rv_{k}'], row[f'eth_rv_{k}'], row[f'rcov_{k}'] = rvb, rve, cbe
        rb = np.diff(lb)
        row['btc_rk'] = realised_kernel(rb, kernel_bandwidth(rb, np.diff(lb[::1200]), len(rb)))
        row['btc_rk_H'] = kernel_bandwidth(rb, np.diff(lb[::1200]), len(rb))
        row['btc_nzero'] = float(np.mean(rb == 0))
        rows.append(row)
        if str(d.date()) == keep_day:
            pd.DataFrame({'time': grid, 'btc': pb, 'eth': pe}).to_csv(
                os.path.join(OUT, f'binance_1s_{keep_day}.csv.gz'), index=False, float_format='%.2f', compression='gzip')
    t = pd.DataFrame(rows).set_index('date')
    t.to_csv(os.path.join(OUT, f'binance_signature_{month}.csv'), float_format='%.6g')
    print('Binance 1s', t.shape)


if __name__ == '__main__':
    import sys
    os.makedirs(OUT, exist_ok=True)
    what = sys.argv[1:] or ['omi', 'daily', 'seconds']
    if 'omi' in what:
        omi()
    if 'seconds' in what:
        binance_seconds()
    if 'daily' in what:
        binance_daily()
