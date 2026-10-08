r"""
build_chapter12.py -- Capitolul 12 (Machine learning și deep learning pentru serii de timp), EN + RO
=====================================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_12/ch12_numbers.json (generate_all_charts.py). Nicio cifră nu este
scrisă de mînă, în afara exemplelor teoretice.
TSA, Capitolul 9 a predat variabilele cu laguri, validarea walk-forward, leakage, ridge/lasso, arbori, RF, GB, un MLP
mic, predicția conformală de bază și competițiile M4/M5; aici: teoria învățării pentru date dependente și validitatea
validării încrucișate (Bergmeir, Hyndman și Koo 2018), modele globale și locale, lasso în dimensiune mare și inferența
după selecție, ansambluri de arbori în profunzime (QRF, boosting cu restricții de monotonie), RNN/LSTM/GRU și gradienții
care se sting, TCN, seq2seq, atenție și Transformers (Informer, Autoformer, critica lui Zeng et al. 2023, DLinear,
PatchTST), N-BEATS, N-HiTS, DeepAR, TFT, interpretabilitate (Shapley, atenția nu este explicație) și cultura comparațiilor
oneste (repere puternice, teste, data snooping).
Ieșire:
  EN/Courses/chapter12_machine_learning_deep_learning.tex
  RO/Cursuri/capitol12_machine_learning_deep_learning.tex
Rulare:
  OMP_NUM_THREADS=1 python3 Quantlets/Ch_12/generate_all_charts.py
  python3 latex/build_chapter12.py && python3 latex/ats_build.py compile 12
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block, n   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch12_common import REFS, QLURL, T, V2, day, month, bib, finalize, load, minus_fix   # noqa: E402


def M(tex):
    """Displayed formula with decimals: decimal comma in RO (the renderer converts only inline math)."""
    return T(tex, re.sub(r'(\d)\.(\d)', r'\1{,}\2', tex))


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(12, 'lecture', refs=REFS)
C = 'https://commons.wikimedia.org/wiki/File:'
P = V.put
TB = '>{\\raggedright\\arraybackslash}'


def ql(folder):
    return f'\\quantlet{{{folder.replace("_", chr(92) + "_")}}}{{\\qlurl{{{folder}}}}}'


def chart(title, fig, folder, bullets, h='0.56\\textheight', size='footnotesize'):
    body = (f'\\begin{{center}}\n\\includegraphics[width=0.97\\textwidth,height={h},keepaspectratio]{{{fig}.pdf}}\n'
            f'\\end{{center}}\n\\vspace{{-0.25cm}}\n' + items(*bullets) + '\n' + ql(folder))
    D.frame(title, body, size)


def interp(title, bullets, size='small'):
    D.frame(T(f'Interpreting {title[0]}', f'Interpretarea {title[1]}'), items(*bullets), size)


FOTO = T('Photo', 'Foto')
PD = T('public domain', 'domeniu public')
PH = {
    'hinton': ('ch12_hinton_2024.jpg', C + 'Geoffrey_E._Hinton,_2024_Nobel_Prize_Laureate_in_Physics_(cropped).jpg',
               FOTO + ': Arthur Petron (2024); CC BY-SA 4.0; Wikimedia Commons'),
    'gpu': ('ch12_nvidia_g80.jpg', C + 'NVIDIA_G80_GPU_Core.jpg', FOTO + ': Hyins (2011); ' + PD + '; Wikimedia Commons'),
    'tower': ('ch12_marasesti_750kv_2022.jpg', C + '750_kV_electricity_tower_at_M\\%C4\\%83r\\%C4\\%83\\%C8\\%99e\\%C8\\%99ti,_Romania.jpg',
              FOTO + ': TrainSimFan (2022); CC BY-SA 4.0; Wikimedia Commons'),
    'hochreiter': ('ch12_hochreiter_2015.jpg', C + 'Sepp_Hochreiter.JPG', FOTO + ': Eulenreich (2015); CC BY-SA 4.0; Wikimedia Commons'),
    'bengio': ('ch12_bengio_2019.jpg', C + 'Yoshua_Bengio_2019_cropped.jpg', FOTO + ': Maryse Boyce (2019); CC BY 4.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


def pv(key, x, d=3):
    if x < 10 ** (-d):
        V.raw(key, '$<$' + n(10 ** (-d), d))
    else:
        P(key, x, d)


def word(k, en=('none', 'one', 'two', 'three', 'four', 'five', 'six'), ro=('niciunul', 'unul', 'două', 'trei', 'patru', 'cinci', 'șase')):
    return V2(en[k], ro[k]) if k < len(en) else str(k)


# =============================================================================
# CIFRE
# =============================================================================
o = N['overview']
V.int('ov.days', o['load_days'])
V.raw('ov.lend', day(o['load_end']))
V.raw('ov.hend', month(o['hicp_end']))
V.int('ov.rvn', o['rv_n'])
V.raw('ov.rvend', day(o['rv_end']))
V.raw('ov.m4', str(o['m4_n']))
V.raw('ov.m4min', str(o['m4_min']))
V.raw('ov.m4max', str(o['m4_max']))
P('ov.lmean', o['load_mean'], 2)

cv = N['cv']
V.int('cv.reps', cv['reps'])
for dg, kk in (('AR(3)', 'ar'), ('MA(1)', 'ma'), ('SAR', 'sar')):
    for pr, kp in (('5-fold CV', 'cv'), ('LOOCV', 'loo'), ('nonDepCV', 'nd'), ('OOS', 'oos')):
        for p_ in (1, 3, 5):
            r = cv[dg][f'AR({p_})'][pr]
            P(f'cv.{kk}.{kp}.{p_}.a', r['mapae'], 3)
            P(f'cv.{kk}.{kp}.{p_}.b', r['mpae'], 3)
P('cv.phi', cv['sar_par'][0], 2)
P('cv.Phi', cv['sar_par'][1], 2)
lk = N['leakage']
for k, kk in (('random 5-fold', 'rnd'), ('blocked 5-fold', 'blk'), ('purged 5-fold', 'pur'), ('last 20%', 'oos')):
    P(f'lk.{kk}', lk[k]['med'], 2)
    P(f'lk.{kk}.q1', lk[k]['q1'], 2)
    P(f'lk.{kk}.q3', lk[k]['q3'], 2)
V.raw('lk.reps', str(lk['reps']))

g = N['global']
for h in ('1', '12'):
    r = g[h]
    lags = g['lags']
    for i, p_ in enumerate(lags):
        P(f'gl.{h}.l{p_}', r['local'][i], 2)
        P(f'gl.{h}.g{p_}', r['glob'][i], 2)
        P(f'gl.{h}.lr{p_}', r['local_ro'][i], 2)
        P(f'gl.{h}.gr{p_}', r['glob_ro'][i], 2)
    V.raw(f'gl.{h}.bl', str(r['best_l']))
    V.raw(f'gl.{h}.bg', str(r['best_g']))
    P(f'gl.{h}.dmall', r['dm_all'], 2)
    pv(f'gl.{h}.pall', r['p_all'], 3)
    P(f'gl.{h}.dmro', r['dm_ro'], 2)
    P(f'gl.{h}.pro', r['p_ro'], 2)
    V.raw(f'gl.{h}.T', str(r['T']))
    P(f'gl.{h}.lbest', min(r['local']), 2)
    P(f'gl.{h}.gbest', min(r['glob']), 2)
la = N['lasso']
for k, kk in (('AR(3)', 'ar'), ('ridge', 'ridge'), ('lasso', 'lasso'), ('adaptive lasso', 'ada'), ('elastic net', 'enet'),
              ('post-lasso OLS', 'post'), ('global AR(12)', 'glob')):
    P(f'la.{kk}', la['rmse'][k], 2)
    if k != 'AR(3)':
        P(f'la.{kk}.rel', la['rmse'][k] / la['rmse']['AR(3)'], 2)
        P(f'la.{kk}.p', la['dm'][k]['p'], 2)
V.raw('la.T', str(la['T']))
V.raw('la.nsel', str(int(la['n_sel_med'])))
V.raw('la.nmin', str(la['n_sel_min']))
V.raw('la.nmax', str(la['n_sel_max']))
V.raw('la.top', ', '.join(la['top'][:3]))
V.raw('la.nf', str(la['n_feat']))
P('la.top1', 100 * la['top_share'][0], 0)
V.raw('la.first', month(la['first']))
V.raw('la.last', month(la['last']))

ld = N['load']
for k, kk in (('ARX', 'arx'), ('RF', 'rf'), ('HGB', 'hgb'), ('HGB monotone', 'mono'), ('ARX + HGB', 'comb')):
    P(f'ld.{kk}', 1000 * ld['mae'][k], 0)
    P(f'ld.{kk}.mcs', ld['mcs'][k], 2)
    if k != 'ARX':
        P(f'ld.{kk}.t', ld['dm'][k]['t'], 2)
        pv(f'ld.{kk}.p', ld['dm'][k]['p'], 3)
for k, kk in (('ARX', 'arx'), ('QRF', 'qrf'), ('HGB', 'hgb')):
    P(f'ld.pin.{kk}', 1000 * ld['pin'][k], 1)
    P(f'ld.cov.{kk}', 100 * ld['cov'][k], 0)
    P(f'ld.mq.{kk}', ld['mcs_q'][k], 3)
V.raw('ld.days', str(ld['days']))
mo = N['monotone']
V.raw('mo.down', str(mo['unconstrained']['n_down']))
P('mo.worst', 1000 * abs(mo['unconstrained']['worst']), 1)
P('mo.r0', mo['unconstrained']['range'], 2)
P('mo.r1', mo['monotone increasing']['range'], 2)

va = N['vanishing']
for k in ('rnn', 'gru', 'lstm', 'lstm_b1', 'lstm_b3'):
    r = va[k]
    V.raw(f'va.{k}.e50', f'$10^{{{int(round(__import__("math").log10(r["ratio50"])))}}}$')
    P(f'va.{k}.r50', r['ratio50'], 2)
    P(f'va.{k}.rate', r['rate'], 2)
V.raw('va.T', str(va['T']))
V.raw('va.seeds', str(va['seeds']))

rv = N['rv']
V.raw('rv.oos', day(rv['oos_start']))
V.raw('rv.end', day(rv['end']))
V.int('rv.T', rv['oos_T'])
for h in ('1', '5', '22'):
    e = rv['eval'][h]
    P(f'rv.{h}.har', e['qlike']['HAR'], 3)
    for k, kk in (('MLP', 'mlp'), ('LSTM', 'lstm'), ('TCN', 'tcn'), ('HGB', 'hgb')):
        P(f'rv.{h}.{kk}', e['rel'][k], 3)
        P(f'rv.{h}.{kk}.t', e['dm'][k]['t'], 2)
        pv(f'rv.{h}.{kk}.p', e['dm'][k]['p'], 3)
        P(f'rv.{h}.{kk}.mcs', e['mcs'][k], 2)
    P(f'rv.{h}.har.mcs', e['mcs']['HAR'], 2)
sn = N['snooping']
P('sn.best', sn['seeds']['best'], 3)
P('sn.worst', sn['seeds']['worst'], 3)
P('sn.med', sn['seeds']['med'], 3)
P('sn.ens', sn['seeds']['ens'], 3)
V.raw('sn.n', str(sn['seeds']['n']))
for k in ('1', '10', '100'):
    P(f'sn.rej{k}', 100 * sn['sim'][k]['reject'], 0)
sh = N['shap']
for i, k in enumerate(('d', 'w', 'm')):
    P(f'sh.{k}', 100 * sh['share'][i], 0)
    P(f'sh.har.{k}', sh['har'][i], 2)
V.raw('sh.ne', str(sh['n_eval']))
V.raw('sh.nb', str(sh['n_bg']))

z = N['zeng']
V.int('ze.n', z['n'])
V.raw('ze.test', day(z['test_start']))
ZM = (('repeat', 'rep'), ('seasonal naive', 'sn'), ('Linear', 'lin'), ('NLinear', 'nlin'), ('DLinear', 'dlin'),
      ('Transformer', 'tr'), ('Transformer, point tokens', 'trp'))
for H in z['res']:
    for k, kk in ZM:
        if k in z['res'][H]:
            P(f'ze.{H}.{kk}', z['res'][H][k]['mse'], 3)
            P(f'ze.{H}.{kk}.mae', z['res'][H][k]['mae'], 3)
at = N['attention']
P('at.rho', at['rho'], 2)
V.raw('at.ta', str(at['top_att']))
V.raw('at.to', str(at['top_occ']))
P('at.la', 100 * at['share_last_att'], 0)
P('at.lo', 100 * at['share_last_occ'], 0)
V.raw('at.nt', str(at['n_tok']))
m4 = N['m4']
for k, kk in (('Naive', 'nv'), ('seasonal naive', 'sn'), ('Naive 2', 'n2'), ('DLinear', 'dl'), ('N-BEATS', 'nb'), ('N-HiTS', 'nh')):
    r = m4['scores'][k]
    P(f'm4.{kk}.s', r['smape'], 2)
    P(f'm4.{kk}.m', r['mase'], 2)
    P(f'm4.{kk}.o', r['owa'], 3)
off = m4['official']
for k, kk in (('Naive2', 'n2'), ('sNaive', 'sn'), ('Theta', 'th'), ('MLP', 'mlp'), ('RNN', 'rnn'), ('118', 'smyl'), ('245', 'mm')):
    P(f'mo4.{kk}.s', off[k]['smape'], 2)
    P(f'mo4.{kk}.m', off[k]['mase'], 2)
    P(f'mo4.{kk}.o', off[k]['owa'], 3)
V.raw('m4.seeds', str(m4['seeds']))
da = N['deepar']
for k, kk in (('DeepAR', 'da'), ('seasonal naive', 'sn')):
    P(f'da.{kk}.w', da[k]['wql'], 3)
    P(f'da.{kk}.c', 100 * da[k]['cov80'], 0)
    P(f'da.{kk}.s', da[k]['smape'], 2)
V.int('da.steps', da['steps'])
for c_ in ('500', '1000', '2000', '4000'):
    P(f'da.b{c_}', da['budget'][c_]['wql'], 4)
    P(f'da.c{c_}', 100 * da['budget'][c_]['cov80'], 0)
P('da.snw', da['seasonal naive']['wql'], 4)
ai = N['ai']
V.raw('ai.n', str(ai['n']))
V.raw('ai.better', str(ai['better']))
V.raw('ai.sb', str(ai['sig_better']))
V.raw('ai.sw', str(ai['sig_worse']))
P('ai.min', ai['rel_min'], 2)
P('ai.max', ai['rel_max'], 2)
P('ai.med', ai['rel_med'], 3)
P('ai.mlp', ai['by_model']['MLP'], 3)
P('ai.hgb', ai['by_model']['HGB'], 3)
for h in ('1', '5', '22'):
    P(f'ai.h{h}', ai['by_h'][h], 3)
minus_fix(V)

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: when do flexible learners (penalised regressions, tree ensembles, deep networks) forecast time series better than strong statistical baselines, and how do we know it honestly?',
       r'\textbf{Întrebarea}: cînd prognozează instrumentele flexibile (regresii penalizate, ansambluri de arbori, rețele deep) seriile de timp mai bine decît reperele statistice puternice și cum stabilim acest lucru riguros?'),
     [T('dependence breaks the i.i.d.\\ logic of machine learning: validation, generalisation and inference all change',
        'dependența strică logica i.i.d.\\ a machine learning: validarea, generalizarea și inferența se schimbă toate')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('learning from dependent data: mixing, bounds, when cross-validation is valid', 'învățarea din date dependente: mixing, margini de eroare, cînd este validă validarea încrucișată'),
      T('global and local models; lasso and its relatives in high dimension; tree ensembles in depth', 'modele globale și locale; lasso și variantele lui în dimensiune mare; ansambluri de arbori în profunzime'),
      T('recurrent and convolutional networks; attention and Transformers; N-BEATS, N-HiTS, DeepAR, TFT', 'rețele recurente și convoluționale; atenție și Transformers; N-BEATS, N-HiTS, DeepAR, TFT'),
      T('interpretation and the honest benchmark: baselines, tests, data snooping', 'interpretare și comparația riguroasă: repere, teste, data snooping')]),
    T('We build on TSA, Chapter 9 (lag features, walk-forward validation, trees, a small MLP, M4 and M5) and on Chapter 1 (DM, MCS, scoring rules); Seminar 12 comes before this lecture',
      'Pornim de la TSA, Capitolul 9 (variabile cu laguri, validare walk-forward, arbori, un MLP mic, M4 și M5) și de la Capitolul 1 (DM, MCS, reguli de scor); Seminarul 12 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('State when K-fold cross-validation is valid for autoregressive prediction, and design blocked, purged and rolling-origin validation that avoids leakage',
      'Enunțați cînd este validă validarea încrucișată cu K subeșantioane pentru predicția autoregresivă și construiți validări pe blocuri, cu purjare și cu origine mobilă, fără leakage'),
    T('Derive the lasso, adaptive lasso and elastic net solutions, state their consistency conditions for dependent data, and explain why naive inference after selection fails',
      'Deduceți soluțiile lasso, lasso adaptiv și elastic net, enunțați condițiile lor de consistență pentru date dependente și explicați de ce inferența naivă după selecție eșuează'),
    T('Explain the bias--variance mechanics of bagging, random forests, quantile regression forests and gradient boosting with constraints',
      'Explicați mecanica deplasare--varianță pentru bagging, păduri aleatoare, păduri de regresie cuantilică și gradient boosting cu restricții'),
    T('Derive vanishing gradients in recurrent networks and the role of gates; read the architectures of TCN, Transformers, N-BEATS, N-HiTS, DeepAR and TFT',
      'Deduceți stingerea gradienților în rețelele recurente și rolul porților; citiți arhitecturile TCN, Transformers, N-BEATS, N-HiTS, DeepAR și TFT'),
    T('Run a pre-registered comparison against strong baselines with DM, MCS and seeds reported, and interpret Shapley values and attention correctly',
      'Realizați o comparație preînregistrată cu repere puternice, raportînd DM, MCS și seed-urile, și interpretați corect valorile Shapley și atenția')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Validation and learning theory: \refBHK; \refRac; \refMR; \refHAB', r'Validare și teoria învățării: \refBHK; \refRac; \refMR; \refHAB'),
     [T(r'High dimension and trees: \refTib; \refZou; \refBM; \refMei; \refFri; \refKeA', r'Dimensiune mare și arbori: \refTib; \refZou; \refBM; \refMei; \refFri; \refKeA'),
      T(r'Deep learning: \refHS; \refVas; \refZeng; \refOre; \refDeepAR; \refTFT; survey \refBen', r'Deep learning: \refHS; \refVas; \refZeng; \refOre; \refDeepAR; \refTFT; sinteza \refBen')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_12}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_12}'),
     [T(r'\texttt{numpy}, \texttt{scikit-learn} and \texttt{PyTorch} on a CPU: small networks, fixed seeds, runs of minutes',
        r'\texttt{numpy}, \texttt{scikit-learn} și \texttt{PyTorch} pe procesor: rețele mici, seed-uri fixate, rulări de cîteva minute')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter12_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter12_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{3.0cm}' + TB + 'p{5.6cm}' + TB + 'p{3.6cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source, sample}', r'\textbf{Sursa, eșantionul}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizarea}'),
    [T('Romanian electricity load, hourly', 'Consumul de electricitate al României, orar') + ' & ' + T(r'Energy-Charts (ENTSO-E transparency data), @{ov.days} days to @{ov.lend}', r'Energy-Charts (date de transparență ENTSO-E), @{ov.days} de zile pînă la @{ov.lend}') + ' & ' + T('trees, Transformers, DLinear', 'arbori, Transformers, DLinear'),
     T('HICP inflation, 27 EU countries', 'Inflația IAPC, 27 de țări UE') + ' & ' + T(r'Eurostat prc\_hicp\_minr, annual rates, monthly, January 2000 -- @{ov.hend}', r'Eurostat prc\_hicp\_minr, rate anuale, lunar, ianuarie 2000 -- @{ov.hend}') + ' & ' + T('global models, lasso', 'modele globale, lasso'),
     T('S\\&P 500 and five other indices, realised variance', 'S\\&P 500 și alți cinci indici, varianța realizată') + r' & \refOMI: ' + T(r'5-minute RV, @{ov.rvn} days to @{ov.rvend}', r'RV din randamente de 5 minute, @{ov.rvn} zile pînă la @{ov.rvend}') + ' & ' + T('deep models against HAR', 'modele deep față de HAR'),
     T('M4 hourly subset', 'Subsetul orar M4') + ' & ' + T(r'\refMfourA: @{ov.m4} series of @{ov.m4min}--@{ov.m4max} hours, horizon 48', r'\refMfourA: @{ov.m4} de serii de @{ov.m4min}--@{ov.m4max} de ore, orizont 48') + ' & ' + T('N-BEATS, N-HiTS, DeepAR', 'N-BEATS, N-HiTS, DeepAR')],
    size='scriptsize') + items(
    T('Every comparison has a forecast period fixed before the models are run; losses, tests and seeds are reported with it',
      'Fiecare comparație are o perioadă de prognoză fixată înainte de rularea modelelor; pierderile, testele și seed-urile sînt raportate împreună cu ea')), 'footnotesize')

D.frame(T('Four generations of forecasting models', 'Patru generații de modele de prognoză'), two(
    ph('hinton', T('Geoffrey Hinton, Nobel Prize in Physics 2024', 'Geoffrey Hinton, Premiul Nobel pentru fizică 2024'), h='0.48\\textheight'),
    items(T(r'\textbf{Statistical}: ARIMA, ETS, HAR, state space: few parameters, one model per series', r'\textbf{Statistice}: ARIMA, ETS, HAR, spațiul stărilor: puțini parametri, un model pe serie'),
          T(r'\textbf{Machine learning}: penalised regressions, forests, boosting on lag features, often global', r'\textbf{Machine learning}: regresii penalizate, păduri, boosting pe variabile cu laguri, adesea globale'),
          T(r'\textbf{Deep sequence models} trained by backpropagation \refRHW: RNN, LSTM, TCN, Transformers, N-BEATS, DeepAR', r'\textbf{Modele deep de secvențe}, antrenate prin retropropagare \refRHW: RNN, LSTM, TCN, Transformers, N-BEATS, DeepAR'),
          T('\\textbf{Foundation models}: pretrained on many series, used zero-shot (Chapter 13)', '\\textbf{Foundation models}: preantrenate pe multe serii, folosite zero-shot (Capitolul 13)'),
          T('Each generation must beat the previous one out of sample, with tests, on the same data', 'Fiecare generație trebuie să fie mai bună decît cea dinainte în afara eșantionului, cu teste, pe aceleași date')), '0.36', '0.62'), 'small')

chart(T('Four data sets, four kinds of structure', 'Patru seturi de date, patru tipuri de structură'), 'ats_ch12_overview', 'ATS_ch12_validation', [
    T(r'Romanian load (daily mean, @{ov.lmean} GW on average); EU inflation (Romania in red); S\&P 500 realised variance (log scale); three M4 hourly series (last two weeks)',
      r'Consumul României (media zilnică, în medie @{ov.lmean} GW); inflația UE (România cu roșu); varianța realizată S\&P 500 (scară logaritmică); trei serii orare M4 (ultimele două săptămîni)')], h='0.66\\textheight')

interp(('the four data sets', 'celor patru seturi de date'), [
    T('Load: strong daily and weekly seasonality, holidays, slow annual cycle: calendar structure that trees and linear models capture well',
      'Consumul: sezonalitate zilnică și săptămînală puternică, sărbători, ciclu anual lent: o structură de calendar pe care arborii și modelele liniare o captează bine'),
    T('Inflation: 27 short, co-moving series with a common shock in 2021--2023: the natural ground for global models and for the high-dimensional panel',
      'Inflația: 27 de serii scurte, care se mișcă împreună, cu un șoc comun în 2021--2023: terenul natural pentru modelele globale și pentru panelul în dimensiune mare'),
    T('Realised variance: long memory and heavy tails; the HAR benchmark of Chapter 8 is hard to beat',
      'Varianța realizată: memorie lungă și cozi groase; reperul HAR din Capitolul 8 este greu de depășit'),
    T('M4 hourly: many related series of the same frequency, the setting where global deep models were first shown to win',
      'M4 orar: multe serii înrudite de aceeași frecvență, cadrul în care modelele deep globale au cîștigat prima dată')])

# =============================================================================
# 1. ÎNVĂȚAREA DIN DATE DEPENDENTE
# =============================================================================
D.section('Learning from dependent data', 'Învățarea din date dependente')

D.frame(T('Known from TSA, and new here', 'Cunoscut din TSA și elemente noi'), items(
    (T('Known from TSA, Chapter 9', 'Cunoscut din TSA, Capitolul 9'),
     [T('lag features, walk-forward validation, leakage by example, ridge and lasso', 'variabile cu laguri, validare walk-forward, leakage între exemple, ridge și lasso'),
      T('trees, random forests, gradient boosting, a small MLP, conformal basics, M4 and M5', 'arbori, păduri aleatoare, gradient boosting, un MLP mic, elemente de predicție conformală, M4 și M5')]),
    (T('New: the statistics behind the recipes', 'Nou: statistica din spatele rețetelor'),
     [T('generalisation under mixing; when cross-validation is valid; global models', 'generalizarea sub mixing; cînd este validă validarea încrucișată; modele globale'),
      T('selection consistency and post-selection inference; quantile forests; constrained boosting', 'consistența selecției și inferența după selecție; păduri cuantilice; boosting cu restricții'),
      T('gradients through time; attention; basis expansion; likelihood-based deep models; interpretation', 'gradienți în timp; atenție; dezvoltări în baze de funcții; modele deep cu verosimilitate; interpretare')]),
    T('Replications: Bergmeir, Hyndman and Koo (2018, Section 4); Montero-Manso and Hyndman (2021) on EU inflation; Zeng et al.\\ (2023) protocol on Romanian load; the M4 hourly evaluation',
      'Replicări: Bergmeir, Hyndman și Koo (2018, secțiunea 4); Montero-Manso și Hyndman (2021) pe inflația UE; protocolul Zeng et al.\\ (2023) pe consumul României; evaluarea M4 pe seriile orare')), 'small')

D.frame(T('Risk, empirical risk and the generalisation gap (1/2)', 'Riscul, riscul empiric și diferența de generalizare (1/2)'), items(
    (T(r'A forecast rule $f$ from a class $\mathcal F$ is judged by its expected loss under the stationary law', r'O regulă de prognoză $f$ dintr-o clasă $\mathcal F$ se judecă după pierderea ei așteptată sub legea staționară'
       ) + r'''
    \[ R(f) = \E\,\ell\big(Y_{t+h}, f(X_t)\big), \qquad \hat R_n(f) = \frac1n\sum_{t=1}^n \ell\big(y_{t+h}, f(x_t)\big) \]''',
     [T(r'$R(f)$: \textbf{risk}; $\hat R_n(f)$: \textbf{empirical risk} on $n$ training pairs; $\ell$: loss (e.g.\ squared error); $X_t$: features known at $t$; $h$: horizon',
        r'$R(f)$: \textbf{riscul}; $\hat R_n(f)$: \textbf{riscul empiric} pe $n$ perechi de antrenare; $\ell$: pierderea (de exemplu eroarea pătratică); $X_t$: variabilele cunoscute la $t$; $h$: orizontul')]),
    (T(r'Empirical risk minimisation (ERM) and the generalisation gap', r'Minimizarea riscului empiric (ERM) și diferența de generalizare'
       ) + r'''
    \[ \hat f = \arg\min_{f \in \mathcal F}\hat R_n(f), \qquad R(\hat f) - \hat R_n(\hat f) \le \sup_{f \in \mathcal F}|R(f) - \hat R_n(f)| \]''',
     [T(r'the gap: how much worse the fitted rule does on new data than on the training data', r'diferența: cu cît este mai slabă regula estimată pe date noi decît pe datele de antrenare')])), 'small')

D.frame(T('Risk, empirical risk and the generalisation gap (2/2)', 'Riscul, riscul empiric și diferența de generalizare (2/2)'), items(
    (T(r'i.i.d.\ data: the uniform deviation shrinks with the complexity of the class', r'Date i.i.d.: abaterea uniformă scade în funcție de complexitatea clasei'
       ) + T(r'''
    \[ \sup_{\mathcal F}|R - \hat R_n| = O_p\Big(\sqrt{\mathrm{complexity}(\mathcal F)/n}\Big) \]''', r'''
    \[ \sup_{\mathcal F}|R - \hat R_n| = O_p\Big(\sqrt{\mathrm{complexitate}(\mathcal F)/n}\Big) \]'''),
     [T(r'complexity: VC dimension or Rademacher complexity, roughly the number of patterns the class can fit', r'complexitatea: dimensiunea VC sau complexitatea Rademacher, aproximativ numărul de tipare pe care clasa le poate potrivi')]),
    (T(r'Dependent data: the $n$ observations carry less information; the bound holds with an \textbf{effective sample size} smaller than $n$',
       r'Date dependente: cele $n$ observații conțin mai puțină informație; marginea este valabilă cu o \textbf{dimensiune efectivă a eșantionului} mai mică decît $n$'),
     [T('and only if the series forgets its past fast enough: mixing', 'și numai dacă seria își uită trecutul suficient de repede: mixing')]),
    T('Non-stationarity (breaks, Chapter 2) adds a second gap: the future law differs from the training law; no bound covers it', 'Nestaționaritatea (rupturi, Capitolul 2) adaugă o a doua diferență: legea viitoare diferă de cea de antrenare; nicio margine nu o acoperă')), 'small')

D.frame(T('Mixing coefficients', 'Coeficienții de mixing'), items(
    (T(r'$\beta$-mixing: how far the distant future is from being independent of the past', r'$\beta$-mixing: cît de departe este viitorul îndepărtat de independența față de trecut'
       ) + r'''
    \[ \beta(a) = \sup_t\,\E\sup_{B\in\sigma(X_{t+a},\dots)}\big|P\big(B\mid\sigma(\dots,X_t)\big) - P(B)\big| \]''',
     [T(r'$\sigma(\dots, X_t)$: the information in the past up to $t$; $\sigma(X_{t+a}, \dots)$: events $B$ of the future beyond the gap $a$; $\alpha$-mixing uses $|P(A\cap B) - P(A)P(B)|$ instead',
        r'$\sigma(\dots, X_t)$: informația din trecut pînă la $t$; $\sigma(X_{t+a}, \dots)$: evenimentele $B$ din viitor după distanța $a$; $\alpha$-mixing folosește în schimb $|P(A\cap B) - P(A)P(B)|$'),
      T(r'mixing: $\beta(a) \to 0$ as the gap $a \to \infty$: the far future is almost independent of the past', r'mixing: $\beta(a) \to 0$ cînd distanța $a \to \infty$: viitorul îndepărtat este aproape independent de trecut')]),
    (T(r'Stationary ARMA with continuous innovations, GARCH and Markov-switching models with ergodic chains are \textbf{geometrically} $\beta$-mixing: $\beta(a) \le Cr^a$, $C > 0$, $0 < r < 1$',
       r'ARMA staționar cu inovații continue, GARCH și modelele cu schimbare de regim cu lanț ergodic sînt $\beta$-mixing \textbf{geometric}: $\beta(a) \le Cr^a$, $C > 0$, $0 < r < 1$'),
     [T('long memory (Chapter 10) is not geometrically mixing: the effective sample size shrinks much more', 'memoria lungă (Capitolul 10) nu este mixing geometric: dimensiunea efectivă a eșantionului scade mult mai mult')]),
    T('Mixing is assumed, rarely tested: it is a statement about the data-generating process, not about the sample', 'Mixing-ul este presupus, rar testat: este o afirmație despre procesul generator, nu despre eșantion')), 'small')

D.frame(T('Blocking and a generalisation bound', 'Blocuri și o margine de generalizare'), items(
    (T(r'\refYu: split the sample into $2\mu$ alternating blocks of length $a$; under $\beta$-mixing the odd blocks behave like $\mu$ \textbf{independent} blocks up to an error $\mu\,\beta(a)$',
       r'\refYu: împărțim eșantionul în $2\mu$ blocuri alternante de lungime $a$; sub $\beta$-mixing, blocurile impare se comportă ca $\mu$ blocuri \textbf{independente}, pînă la o eroare $\mu\,\beta(a)$'),
     [T(r'i.i.d.\ tools then apply with $\mu = n/(2a)$ observations instead of $n$', r'instrumentele i.i.d.\ se aplică apoi cu $\mu = n/(2a)$ observații în loc de $n$')]),
    (T(r'\refMR: for a uniformly stable learner, with probability at least $1 - \delta$', r'\refMR: pentru un algoritm uniform stabil, cu probabilitatea de cel puțin $1 - \delta$'
       ) + r'''
    \[ R(\hat f) \le \hat R_n(\hat f) + O(\kappa_n a) + O\Big(\sqrt{\log(1/\delta')/\mu}\Big), \qquad \delta' = \delta - 2(\mu - 1)\beta(a) \]''',
     [T(r'$\kappa_n$: uniform stability, the largest change of the loss when one training point changes; $\delta$: confidence level',
        r'$\kappa_n$: stabilitatea uniformă, cea mai mare modificare a pierderii cînd se schimbă un punct de antrenare; $\delta$: nivelul de încredere'),
      T(r'trade-off in $a$: long blocks make $\beta(a)$ small but leave few blocks $\mu$; ridge and regularised models are uniformly stable, deep networks trained by SGD only approximately',
        r'compromisul în $a$: blocurile lungi fac $\beta(a)$ mic, dar lasă puține blocuri $\mu$; ridge și modelele regularizate sînt uniform stabile, rețelele deep antrenate prin SGD doar aproximativ')]),
    T('The same blocking idea gives blocked bootstrap (Chapter 0) and blocked cross-validation', 'Aceeași idee a blocurilor dă bootstrap-ul pe blocuri (Capitolul 0) și validarea încrucișată pe blocuri')), 'small')

D.frame(T('Cross-validation for time series: the schemes', 'Validarea încrucișată pentru serii de timp: schemele'), items(
    T(r'\textbf{Random K-fold}: rows of the lag matrix $(y_t; y_{t-1},\dots,y_{t-p})$ assigned to folds at random', r'\textbf{K subeșantioane aleatoare}: rîndurile matricei de laguri $(y_t; y_{t-1},\dots,y_{t-p})$ repartizate aleator'),
    T(r'\textbf{Non-dependent CV} \refBHK: the same folds, but training rows within $p$ lags of a test row are removed', r'\textbf{Validarea nedependentă} \refBHK: aceleași subeșantioane, dar rîndurile de antrenare aflate la mai puțin de $p$ laguri de un rînd de test sînt eliminate'),
    T(r'\textbf{Blocked K-fold} and \textbf{hv-block} \refBCN, \refRac: contiguous test blocks, a gap of $h$ rows (purge) on each side', r'\textbf{K blocuri contigue} și \textbf{hv-block} \refBCN, \refRac: blocuri de test contigue, cu un interval de $h$ rînduri (purjare) de fiecare parte'),
    T(r'\textbf{Out-of-sample (OOS)} and \textbf{rolling origin}: test only on the end; the only scheme that mimics real use, at the price of a high variance', r'\textbf{În afara eșantionului (OOS)} și \textbf{originea mobilă}: test doar la sfîrșit; singura schemă care imită utilizarea reală, cu prețul unei varianțe mari'),
    T('The question is not which scheme is ``correct\'\' but which estimates the future risk with small bias and small variance', 'Întrebarea nu este care schemă este „corectă”, ci care estimează riscul viitor cu deplasare mică și varianță mică')), 'small')

D.frame(T('When K-fold is valid: Bergmeir, Hyndman and Koo (2018)', 'Validitatea validării cu K subeșantioane: Bergmeir, Hyndman și Koo (2018)'), items(
    (T(r'A nonlinear autoregression with \textbf{uncorrelated} errors \refBHK', r'O autoregresie neliniară cu erori \textbf{necorelate} \refBHK'
       ) + r'''
    \[ y_t = g(y_{t-1},\dots,y_{t-p}; \theta) + \varepsilon_t \]''',
     [T(r'$g$: any regression function (linear, tree, network) with parameters $\theta$; $p$: number of lags; $\varepsilon_t$: errors, $\Cov(\varepsilon_t, \varepsilon_s) = 0$ for $t \ne s$',
        r'$g$: orice funcție de regresie (liniară, arbore, rețea) cu parametrii $\theta$; $p$: numărul de laguri; $\varepsilon_t$: erorile, $\Cov(\varepsilon_t, \varepsilon_s) = 0$ pentru $t \ne s$'),
      T('the rows of the lag matrix are then exchangeable enough: a test row shares no error with a training row', 'rîndurile matricei de laguri sînt atunci suficient de interschimbabile: un rînd de test nu are nicio eroare comună cu un rînd de antrenare'),
      T(r'result: the K-fold estimate of the MSE is asymptotically unbiased, and has a lower variance than OOS because every row is used', r'rezultat: estimația MSE prin K subeșantioane este asimptotic nedeplasată și are o varianță mai mică decît OOS, pentru că fiecare rînd este folosit')]),
    (T('It fails when the residuals are autocorrelated: an under-specified model, overlapping $h$-step targets, or features that identify time', 'Eșuează cînd reziduurile sînt autocorelate: un model subspecificat, ținte suprapuse la $h$ pași sau variabile care identifică momentul'),
     [T('then a test error is predictable from the neighbouring training errors: optimistic estimates', 'atunci o eroare de test este previzibilă din erorile de antrenare vecine: estimații optimiste'),
      T('the size of this bias: Appendix  % applink: the bias of K-fold under autocorrelated errors', 'mărimea acestei deplasări: Anexa  % applink: deplasarea validării cu K subeșantioane')]),
    T(r'Practical rule: check the residual ACF of the fitted model (Ljung--Box, TSA, Chapter 2) before trusting random K-fold', r'Regula practică: verificați ACF a reziduurilor modelului estimat (Ljung--Box, TSA, Capitolul 2) înainte de a avea încredere în K subeșantioane aleatoare')), 'small')

D.frame(T('Replication design: Bergmeir, Hyndman and Koo (2018, Section 4)', 'Schema replicării: Bergmeir, Hyndman și Koo (2018, secțiunea 4)'), items(
    T(r'Series of length 200: in-set 140, out-set 60; models AR(1)--AR(5) by OLS; one-step forecasts', r'Serii de lungime 200: 140 de observații de estimare, 60 de evaluare; modele AR(1)--AR(5) prin OLS; prognoze la un pas'),
    T(r'Procedures on the in-set: 5-fold CV, LOOCV, non-dependent CV ($p = 5$), OOS (last 20\%); ``true\'\' error: the model on the whole in-set, RMSE on the out-set', r'Procedurile pe datele de estimare: 5 subeșantioane, LOOCV, validare nedependentă ($p = 5$), OOS (ultimele 20\%); eroarea „adevărată”: modelul pe toate datele de estimare, RMSE pe datele de evaluare'),
    T(r'@{cv.reps} trials per DGP: stationary AR(3) with random coefficients, invertible MA(1), and a seasonal AR fitted to US accidental deaths 1973--1978 ($\phi = @{cv.phi}$, $\Phi_{12} = @{cv.Phi}$) as the counterexample', r'@{cv.reps} de repetări pentru fiecare proces: AR(3) staționar cu coeficienți aleatori, MA(1) inversabil și un AR sezonier estimat pe decesele accidentale din SUA 1973--1978 ($\phi = @{cv.phi}$, $\Phi_{12} = @{cv.Phi}$) drept contraexemplu'),
    (T(r'Precision and bias of each procedure', r'Precizia și deplasarea fiecărei proceduri'
       ) + T(r'''
    \[ \mathrm{MAPAE} = \mathrm{mean}\,|\widehat{PE} - PE|, \qquad \mathrm{MPAE} = \mathrm{mean}\,(\widehat{PE} - PE) \]''', r'''
    \[ \mathrm{MAPAE} = \mathrm{media}\,|\widehat{PE} - PE|, \qquad \mathrm{MPAE} = \mathrm{media}\,(\widehat{PE} - PE) \]'''),
     [T(r'$PE$: the true prediction error (RMSE on the out-set); $\widehat{PE}$: its estimate by the procedure; averages over the trials; MPAE $< 0$: optimistic',
        r'$PE$: eroarea de predicție adevărată (RMSE pe datele de evaluare); $\widehat{PE}$: estimația ei prin procedură; medii pe repetări; MPAE $< 0$: estimare optimistă')])), 'small')

chart(T('Which validation estimates the future error?', 'Precizia și deplasarea schemelor de validare'), 'ats_ch12_cv_bhk', 'ATS_ch12_validation', [
    T('Top: precision (log scale); bottom: bias, by fitted AR order and data-generating process', 'Sus: precizia (scară logaritmică); jos: deplasarea, după ordinul AR estimat și procesul generator')], h='0.68\\textheight')

interp(('the replication', 'replicării'), [
    T(r'AR(3) data, AR(3) model: 5-fold CV has MAPAE @{cv.ar.cv.3.a} against @{cv.ar.oos.3.a} for OOS, bias @{cv.ar.cv.3.b}: as in the paper, CV is unbiased and more precise',
      r'Date AR(3), model AR(3): 5 subeșantioane dau MAPAE @{cv.ar.cv.3.a} față de @{cv.ar.oos.3.a} pentru OOS, deplasare @{cv.ar.cv.3.b}: ca în lucrare, validarea încrucișată este nedeplasată și mai precisă'),
    T(r'Under-specified AR(1) on AR(3) data: residuals are autocorrelated and CV loses its edge (MAPAE @{cv.ar.cv.1.a} against @{cv.ar.oos.1.a})', r'AR(1) subspecificat pe date AR(3): reziduurile sînt autocorelate, iar validarea încrucișată își pierde avantajul (MAPAE @{cv.ar.cv.1.a} față de @{cv.ar.oos.1.a})'),
    T(r'Seasonal counterexample: every AR($p \le 5$) misses lag 12; CV is biased down (MPAE @{cv.sar.cv.5.b} for AR(5)) and no more precise than OOS (@{cv.sar.cv.5.a} against @{cv.sar.oos.5.a})', r'Contraexemplul sezonier: orice AR($p \le 5$) omite lagul 12; validarea încrucișată este deplasată în jos (MPAE @{cv.sar.cv.5.b} pentru AR(5)) și nu mai este mai precisă decît OOS (@{cv.sar.cv.5.a} față de @{cv.sar.oos.5.a})'),
    T(r'Non-dependent CV removes so many rows that its models are poor: bias @{cv.ar.nd.3.b} for AR(3); the price of independence is paid in data', r'Validarea nedependentă elimină atît de multe rînduri încît modelele ei sînt slabe: deplasare @{cv.ar.nd.3.b} pentru AR(3); prețul independenței se plătește în date')])

D.frame(T('Leakage through overlapping targets and time features', 'Leakage prin ținte suprapuse și variabile de timp'), items(
    (T(r'Target $z_t = \frac1h\sum_{j=1}^h y_{t+j}$ (a month of volatility, a quarter of sales): $\mathrm{corr}(z_t, z_{t+1}) \ge (h - 1)/h$ when $y$ is white noise, more when $y$ is persistent',
       r'Ținta $z_t = \frac1h\sum_{j=1}^h y_{t+j}$ (o lună de volatilitate, un trimestru de vînzări): $\mathrm{corr}(z_t, z_{t+1}) \ge (h - 1)/h$ cînd $y$ este zgomot alb, mai mult cînd $y$ este persistent'),
     [T('a random fold puts $z_{t-1}$ and $z_{t+1}$ in training when $z_t$ is tested: the answer is almost in the training set', 'un subeșantion aleator pune $z_{t-1}$ și $z_{t+1}$ în antrenare cînd $z_t$ este testat: răspunsul este aproape în setul de antrenare')]),
    (T(r'A time index or a date feature lets a flexible learner \textbf{locate} the test row between its neighbours', r'Un indice de timp sau o variabilă de dată permite unui algoritm flexibil să \textbf{localizeze} rîndul de test între vecinii lui'), []),
    T(r'Simulation: AR(1) with $\phi = 0.9$, $h = 20$, a random forest on $y_t,\dots,y_{t-4}$ and a time index; @{lk.reps} replications; ratio of the estimated to the true RMSE on new data',
      r'Simulare: AR(1) cu $\phi = 0{,}9$, $h = 20$, o pădure aleatoare pe $y_t,\dots,y_{t-4}$ și un indice de timp; @{lk.reps} de repetări; raportul dintre RMSE estimat și RMSE adevărat pe date noi')), 'small')

chart(T('How optimistic is each validation scheme?', 'Optimismul fiecărei scheme de validare'), 'ats_ch12_leakage', 'ATS_ch12_validation', [
    T('Ratio 1: the scheme estimates the error on new data without bias; below 1: optimistic', 'Raportul 1: schema estimează fără deplasare eroarea pe date noi; sub 1: optimistă')], h='0.68\\textheight')

interp(('the leakage experiment', 'experimentului de leakage'), [
    T(r'Random 5-fold: median ratio @{lk.rnd} (quartiles @{lk.rnd.q1}--@{lk.rnd.q3}): it claims an error three times smaller than the truth', r'5 subeșantioane aleatoare: raportul median @{lk.rnd} (quartile @{lk.rnd.q1}--@{lk.rnd.q3}): pretinde o eroare de trei ori mai mică decît cea reală'),
    T(r'Blocked 5-fold @{lk.blk}, purged 5-fold @{lk.pur}, last 20\% @{lk.oos}: contiguity and the purge remove most of the bias', r'5 blocuri contigue @{lk.blk}, 5 blocuri cu purjare @{lk.pur}, ultimele 20\% @{lk.oos}: contiguitatea și purjarea elimină cea mai mare parte a deplasării'),
    T('The interior blocks still let the forest interpolate in time; only the last block reproduces extrapolation into the future', 'Blocurile interioare lasă încă pădurea să interpoleze în timp; doar ultimul bloc reproduce extrapolarea în viitor'),
    T('Rule: purge at least $h$ rows around every test block and drop time indices unless the trend is modelled explicitly', 'Regula: purjați cel puțin $h$ rînduri în jurul fiecărui bloc de test și eliminați indicii de timp, cu excepția cazului în care trendul este modelat explicit')])

D.recap(('Learning from dependent data', 'învățarea din date dependente'), [
    T('Generalisation bounds hold with an effective sample size set by mixing; blocking is the common tool', 'Marginile de generalizare sînt valabile cu o dimensiune efectivă a eșantionului dată de mixing; blocurile sînt instrumentul comun'),
    T('Random K-fold is valid for autoregressions with uncorrelated errors, and then better than OOS', 'Validarea cu K subeșantioane aleatoare este validă pentru autoregresii cu erori necorelate și atunci este mai bună decît OOS'),
    T('Overlapping targets, under-fitting and time features break it: block, purge, and keep a final untouched period', 'Țintele suprapuse, subspecificarea și variabilele de timp o strică: blocuri, purjare și o perioadă finală neatinsă')])

# =============================================================================
# 2. MODELE GLOBALE, LOCALE ȘI ÎN DIMENSIUNE MARE
# =============================================================================
D.section('Global models and high-dimensional regression', 'Modele globale și regresie în dimensiune mare')

D.frame(T('Local and global models', 'Modele locale și modele globale'), items(
    (T(r'\textbf{Local}: one model per series, $\hat y_{i,t+h} = f_i(y_{i,t}, y_{i,t-1},\dots)$; \textbf{global}: one function for all series, $\hat y_{i,t+h} = f(y_{i,t}, y_{i,t-1},\dots)$',
       r'\textbf{Local}: un model pentru fiecare serie, $\hat y_{i,t+h} = f_i(y_{i,t}, y_{i,t-1},\dots)$; \textbf{global}: o singură funcție pentru toate seriile, $\hat y_{i,t+h} = f(y_{i,t}, y_{i,t-1},\dots)$'),
     [T('global models pool $N \\times T$ rows: far more data per parameter', 'modelele globale reunesc $N \\times T$ rînduri: mult mai multe date pe parametru')]),
    (T(r'\refMMH: for any set of series a global model exists that forecasts as well as the local ones; global models can afford \textbf{longer memory} and more complexity',
       r'\refMMH: pentru orice mulțime de serii există un model global care prognozează la fel de bine ca modelele locale; modelele globale își permit \textbf{memorie mai lungă} și complexitate mai mare'),
     [T('their bound: the complexity of a global model grows with $NT$, that of $N$ local models with $T$ each', 'marginea lor: complexitatea unui model global crește cu $NT$, cea a $N$ modele locale cu cîte $T$')]),
    T('The M4 and M5 winners were global (\\refSmyl; LightGBM in \\refMfiveA): pooling, not depth, was the common ingredient', 'Cîștigătorii M4 și M5 au fost globali (\\refSmyl; LightGBM în \\refMfiveA): reunirea datelor, nu adîncimea, a fost ingredientul comun'),
    T(r'Scaling matters: series of different levels are divided by their own scale before pooling (inflation rates share a scale)', r'Scalarea contează: seriile de niveluri diferite se împart la propria scală înainte de reunire (ratele inflației au aceeași scală)')), 'small')

D.frame(T('Design: EU inflation, local against global', 'Schema studiului: inflația UE, local față de global'), items(
    T(r'Annual HICP inflation of the 27 EU countries; direct forecasts $h = 1$ and $h = 12$ months ahead from AR($p$) models, $p \in \{1, 2, 3, 6, 12, 18, 24, 36\}$', r'Inflația anuală IAPC a celor 27 de țări UE; prognoze directe la $h = 1$ și $h = 12$ luni din modele AR($p$), $p \in \{1, 2, 3, 6, 12, 18, 24, 36\}$'),
    T('Rolling window of 120 months; forecast origins from January 2015 (@{gl.1.T} origins for $h = 1$)', 'Fereastră mobilă de 120 de luni; origini ale prognozei din ianuarie 2015 (@{gl.1.T} origini pentru $h = 1$)'),
    T(r'Local: 27 OLS regressions per origin; global: one pooled OLS (the same coefficients for all countries), as in \refMMH', r'Local: 27 de regresii OLS pentru fiecare origine; global: o singură regresie OLS reunită (aceiași coeficienți pentru toate țările), ca în \refMMH'),
    T('Loss: RMSE in percentage points; DM test on the cross-country average loss differential (HLN correction, Chapter 1)', 'Pierderea: RMSE în puncte procentuale; testul DM pe diferența medie a pierderilor dintre țări (corecția HLN, Capitolul 1)')), 'small')

chart(T('Memory helps global models and hurts local ones', 'Memoria ajută modelele globale și le afectează pe cele locale'), 'ats_ch12_global_local', 'ATS_ch12_global_models', [
    T('RMSE against the memory $p$; circles: average over the 27 countries; squares: Romania', 'RMSE în funcție de memoria $p$; cercuri: media celor 27 de țări; pătrate: România')], h='0.68\\textheight')

interp(('local and global', 'modelelor locale și globale'), [
    T(r'$h = 1$: local RMSE is best at $p = @{gl.1.bl}$ (@{gl.1.lbest}) and then deteriorates; global keeps improving up to $p = @{gl.1.bg}$ (@{gl.1.gbest}); DM on the 27-country average @{gl.1.dmall} ($p$ @{gl.1.pall})',
      r'$h = 1$: RMSE local este minim la $p = @{gl.1.bl}$ (@{gl.1.lbest}), apoi se deteriorează; cel global scade pînă la $p = @{gl.1.bg}$ (@{gl.1.gbest}); DM pe media celor 27 de țări @{gl.1.dmall} ($p$ @{gl.1.pall})'),
    T(r'$h = 12$: the 2021--2023 surge dominates; local AR(36) reaches @{gl.12.l36} against @{gl.12.g36} global; best global @{gl.12.gbest} against best local @{gl.12.lbest}, DM @{gl.12.dmall} ($p$ @{gl.12.pall})',
      r'$h = 12$: valul din 2021--2023 domină; AR(36) local ajunge la @{gl.12.l36} față de @{gl.12.g36} global; cel mai bun global @{gl.12.gbest} față de cel mai bun local @{gl.12.lbest}, DM @{gl.12.dmall} ($p$ @{gl.12.pall})'),
    T(r'Romania alone: the global model helps at $h = 1$ with long memory (@{gl.1.gr36} against @{gl.1.lr36} at $p = 36$), not significantly (DM $p$ @{gl.1.pro})', r'România separat: modelul global ajută la $h = 1$ cu memorie lungă (@{gl.1.gr36} față de @{gl.1.lr36} la $p = 36$), nesemnificativ (DM $p$ @{gl.1.pro})'),
    T('Lesson of Montero-Manso and Hyndman confirmed: pooling buys memory; for a single series the gain is real but hard to prove', 'Lecția lui Montero-Manso și Hyndman se confirmă: reunirea datelor permite o memorie mai lungă; pentru o singură serie, cîștigul este real, dar greu de demonstrat')])

D.frame(T('The lasso (1/2): optimality conditions', 'Lasso (1/2): condițiile de optimalitate'), items(
    (T(r'\refTib: least squares with an $\ell_1$ penalty', r'\refTib: cele mai mici pătrate cu o penalizare $\ell_1$'
       ) + r'''
    \[ \hat\beta = \arg\min_\beta \frac1{2n}\|y - X\beta\|^2 + \lambda\|\beta\|_1, \qquad \|\beta\|_1 = \sum_j|\beta_j| \]''',
     [T(r'$y$: $n \times 1$ target; $X$: $n \times p$ predictors, columns $x_j$; $\lambda \ge 0$: penalty, the larger the more coefficients set to zero',
        r'$y$: ținta, $n \times 1$; $X$: predictorii, $n \times p$, cu coloanele $x_j$; $\lambda \ge 0$: penalizarea; cu cît este mai mare, cu atît mai mulți coeficienți devin zero'),
      T(r'Karush--Kuhn--Tucker (KKT): $\frac1n x_j\'(y - X\hat\beta) = \lambda\,\mathrm{sign}(\hat\beta_j)$ if $\hat\beta_j \ne 0$, and $|\frac1n x_j\'(y - X\hat\beta)| \le \lambda$ otherwise',
        r'condițiile Karush--Kuhn--Tucker (KKT): $\frac1n x_j\'(y - X\hat\beta) = \lambda\,\mathrm{sign}(\hat\beta_j)$ dacă $\hat\beta_j \ne 0$ și $|\frac1n x_j\'(y - X\hat\beta)| \le \lambda$ altfel')]),
    (T(r'Orthonormal predictors ($X\'X = nI$): soft thresholding of the OLS coefficient $z_j$', r'Predictori ortonormali ($X\'X = nI$): pragul moale aplicat coeficientului OLS $z_j$'
       ) + r'''
    \[ \hat\beta_j^{\mathrm{lasso}} = \mathrm{sign}(z_j)\,(|z_j| - \lambda)_+, \qquad \hat\beta_j^{\mathrm{ridge}} = \frac{z_j}{1 + \lambda} \]''',
     [T(r'$(u)_+ = \max(u, 0)$; the lasso selects (sets small $z_j$ to zero), ridge only shrinks', r'$(u)_+ = \max(u, 0)$; lasso selectează (anulează coeficienții $z_j$ mici), ridge doar îi micșorează'),
      T('derivation, also for the elastic net: Appendix  % applink: soft thresholding and the elastic net', 'derivarea, inclusiv pentru elastic net: Anexa  % applink: pragul moale și elastic net')])), 'small')

D.frame(T('The lasso (2/2): prediction and selection', 'Lasso (2/2): predicție și selecție'), items(
    (T(r'Prediction: with $s$ non-zero coefficients and a restricted eigenvalue $\kappa$, for $\lambda \asymp \sigma\sqrt{\log p/n}$', r'Predicția: cu $s$ coeficienți nenuli și o valoare proprie restrînsă $\kappa$, pentru $\lambda \asymp \sigma\sqrt{\log p/n}$'
       ) + r'''
    \[ \frac1n\|X(\hat\beta - \beta)\|^2 = O_p\Big(\frac{s\log p}{n\kappa^2}\Big) \]''',
     [T(r'$\sigma$: error standard deviation; $\kappa$: how far $X$ is from collinearity on sparse directions; time series: the same rate for stable VARs \refBM, heavy-tailed errors \refMM',
        r'$\sigma$: abaterea standard a erorii; $\kappa$: cît de departe este $X$ de colinearitate pe direcțiile rare; serii de timp: aceeași rată pentru VAR stabile \refBM, erori cu cozi groase \refMM')]),
    (T(r'Selection is harder than prediction: sign consistency needs the \textbf{irrepresentable condition} \refZY', r'Selecția este mai grea decît predicția: consistența semnelor cere \textbf{condiția de nereprezentare} \refZY'
       ) + r'''
    \[ \big\|X_{S^c}'X_S(X_S'X_S)^{-1}\mathrm{sign}(\beta_S)\big\|_\infty < 1 \]''',
     [T(r'$S$: the set of relevant predictors, $S^c$: the others; it fails when relevant and irrelevant predictors are correlated (neighbouring countries, lags)',
        r'$S$: mulțimea predictorilor relevanți, $S^c$: ceilalți; eșuează cînd predictorii relevanți și irelevanți sînt corelați (țări vecine, laguri)')])), 'small')

D.frame(T('Adaptive lasso and elastic net', 'Lasso adaptiv și elastic net'), items(
    (T(r'\textbf{Adaptive lasso} \refZou: coefficient-specific weights from a first-step estimate', r'\textbf{Lasso adaptiv} \refZou: ponderi specifice fiecărui coeficient, dintr-o estimație de prima etapă'
       ) + r'''
    \[ \lambda\sum_j w_j|\beta_j|, \qquad w_j = 1/|\tilde\beta_j|^\gamma \]''',
     [T(r'$\tilde\beta_j$: first-step estimate (OLS, ridge); $\gamma > 0$; large coefficients are penalised little, small ones a lot',
        r'$\tilde\beta_j$: estimația de prima etapă (OLS, ridge); $\gamma > 0$; coeficienții mari sînt penalizați puțin, cei mici mult'),
      T(r'\textbf{oracle property}: consistent selection and $\sqrt n$-normal estimates of the non-zero coefficients, without the irrepresentable condition',
        r'\textbf{proprietatea de oracol}: selecție consistentă și estimații $\sqrt n$-normale ale coeficienților nenuli, fără condiția de nereprezentare')]),
    (T(r'\textbf{Elastic net} \refZH: a mix of the lasso and ridge penalties', r'\textbf{Elastic net} \refZH: o combinație a penalizărilor lasso și ridge'
       ) + r'''
    \[ \lambda\Big(\alpha\|\beta\|_1 + \frac{1 - \alpha}2\|\beta\|_2^2\Big) \]
    \[ \hat\beta_j = \frac{\mathrm{sign}(z_j)(|z_j| - \lambda\alpha)_+}{1 + \lambda(1 - \alpha)} \ (X'X = nI) \]''',
     [T(r'$\alpha \in [0, 1]$: $\alpha = 1$ lasso, $\alpha = 0$ ridge; grouping effect: correlated predictors enter together instead of one being chosen at random',
        r'$\alpha \in [0, 1]$: $\alpha = 1$ lasso, $\alpha = 0$ ridge; efectul de grup: predictorii corelați intră împreună, în loc să fie ales unul la întîmplare')]),
    T(r'The penalty is tuned by CV: with $h$-step targets use blocked folds with a purge of $h$ periods (Section 1)', r'Penalizarea se alege prin validare încrucișată: cu ținte la $h$ pași folosiți blocuri cu purjare de $h$ perioade (secțiunea 1)')), 'small')

D.frame(T('Inference after selection', 'Inferența după selecție'), items(
    (T(r'Naive practice: select with the lasso, then report OLS $t$-statistics of the selected variables: the $p$-values are \textbf{too small}', r'Practica naivă: selecție cu lasso, apoi raportarea statisticilor $t$ OLS ale variabilelor selectate: p-value-urile sînt \textbf{prea mici}'),
     [T('the same data chose the model and test it: the distribution of $\\hat\\beta$ is conditional on being selected', 'aceleași date au ales modelul și îl testează: distribuția lui $\\hat\\beta$ este condiționată de faptul că a fost selectat')]),
    (T('Remedies', 'Remedii'),
     [T(r'\textbf{PoSI} intervals, valid for any selection \refBerk', r'intervale \textbf{PoSI}, valabile pentru orice selecție \refBerk'),
      T(r'\textbf{exact conditional} intervals for the lasso (a polyhedral selection event) \refLSST', r'intervale \textbf{condiționate exacte} pentru lasso (un eveniment de selecție poliedral) \refLSST')]),
    (T(r'One coefficient of interest (a policy rate, a foreign shock): \textbf{double selection} \refBCH',
       r'Un coeficient de interes (o dobîndă de politică, un șoc extern): \textbf{dubla selecție} \refBCH'),
     [T(r'lasso of $y$ on the controls, lasso of the regressor of interest on the controls, OLS on the union',
        r'lasso al lui $y$ pe variabilele de control, lasso al regresorului de interes pe aceleași variabile, OLS pe reuniune'),
      T('with HAC standard errors for time series (Chapter 0)', 'cu erori standard HAC pentru serii de timp (Capitolul 0)')]),
    T('For forecasting, selection is a means: judge it by out-of-sample loss and by the stability of what is selected', 'Pentru prognoză, selecția este un mijloc: se judecă după pierderea în afara eșantionului și după stabilitatea a ceea ce este selectat')), 'small')

D.frame(T('Design: Romanian inflation from the EU panel', 'Schema studiului: inflația României din panelul UE'), items(
    T(r'Target: Romanian annual HICP inflation 12 months ahead; window 120 months, re-estimation every 3 months; @{la.T} forecasts (@{la.first} -- @{la.last})', r'Ținta: inflația anuală IAPC a României peste 12 luni; fereastră de 120 de luni, reestimare la fiecare 3 luni; @{la.T} prognoze (@{la.first} -- @{la.last})'),
    T(r'Features: 3 own lags (never penalised) and 3 lags of the 26 other countries: @{la.nf} penalised predictors for about 105 observations', r'Variabile: 3 laguri proprii (nepenalizate) și 3 laguri ale celorlalte 26 de țări: @{la.nf} predictori penalizați pentru circa 105 observații'),
    T(r'Models: AR(3) (benchmark), ridge, lasso, adaptive lasso, elastic net ($\alpha = 0.5$), post-lasso OLS, global AR(12) of the panel; penalty by blocked 5-fold CV with a 12-month purge', r'Modele: AR(3) (reper), ridge, lasso, lasso adaptiv, elastic net ($\alpha = 0{,}5$), OLS după lasso, AR(12) global al panelului; penalizarea prin 5 blocuri cu purjare de 12 luni'),
    T(r'In the spirit of the data-rich inflation literature \refMVVZ, \refGCLSS, with the EU panel as the data set', r'Literatura despre prognoza inflației cu multe date \refMVVZ, \refGCLSS, aplicată aici pe panelul UE')), 'small')

chart(T('What the panel lasso selects, and what it delivers', 'Selecția lasso pe panel și acuratețea ei'), 'ats_ch12_ro_lasso', 'ATS_ch12_global_models', [
    T('Left: share of forecast origins in each year at which a country enters the lasso; right: RMSE relative to AR(3), colour by the DM test', 'Stînga: ponderea originilor din fiecare an în care o țară intră în lasso; dreapta: RMSE relativ la AR(3), culoarea după testul DM')], h='0.65\\textheight')

interp(('the panel lasso', 'lasso pe panel'), [
    T(r'Selection is unstable: median @{la.nsel} of @{la.nf} predictors (from @{la.nmin} to @{la.nmax}); the most frequent are @{la.top}, not Romania\'s neighbours', r'Selecția este instabilă: mediana de @{la.nsel} din @{la.nf} predictori (între @{la.nmin} și @{la.nmax}); cele mai frecvente sînt @{la.top}, nu vecinii României'),
    T(r'Accuracy: AR(3) RMSE @{la.ar}; lasso @{la.lasso.rel}, adaptive lasso @{la.ada.rel}, elastic net @{la.enet.rel}, ridge @{la.ridge.rel} times as large; global AR(12) @{la.glob.rel}', r'Acuratețea: RMSE AR(3) @{la.ar}; lasso de @{la.lasso.rel} ori, lasso adaptiv de @{la.ada.rel} ori, elastic net de @{la.enet.rel} ori, ridge de @{la.ridge.rel} ori mai mare; AR(12) global @{la.glob.rel}'),
    T(r'None of the differences is significant (DM $p$ from @{la.lasso.p} to @{la.glob.p}): about 10 independent 12-month periods, one dominated by the 2022 surge', r'Niciuna dintre diferențe nu este semnificativă (DM $p$ între @{la.lasso.p} și @{la.glob.p}): circa 10 perioade independente de 12 luni, una dominată de valul din 2022'),
    T('High dimension with 105 observations of a persistent target: CV picks small penalties, the panel fits past co-movement that does not repeat; parsimony wins here', 'Dimensiune mare cu 105 observații ale unei ținte persistente: validarea alege penalizări mici, panelul potrivește co-mișcări trecute care nu se repetă; aici cîștigă parcimonia')])

D.recap(('Global models and high dimension', 'modele globale și dimensiune mare'), [
    T('Global models pool many series and can afford long memory; on EU inflation they win at one month', 'Modelele globale reunesc multe serii și își permit memorie lungă; pe inflația UE cîștigă la o lună'),
    T('The lasso predicts well under sparsity and restricted eigenvalues; it selects well only under the irrepresentable condition; adaptive lasso and elastic net relax it', 'Lasso prognozează bine sub raritate și valori proprii restrînse; selectează bine doar sub condiția de nereprezentare; lasso adaptiv și elastic net o relaxează'),
    T('Report selection stability and use PoSI, exact or double-selection inference, never naive $t$-statistics', 'Raportați stabilitatea selecției și folosiți inferența PoSI, exactă sau prin dubla selecție, niciodată statisticile $t$ naive')])

# =============================================================================
# 3. ANSAMBLURI DE ARBORI
# =============================================================================
D.section('Tree ensembles in depth', 'Ansambluri de arbori în profunzime')

D.frame(T('Bagging: the variance of an average', 'Bagging: varianța unei medii'), items(
    (T(r'Average of $B$ predictors $\hat f_b(x)$ trained on bootstrap samples \refBreA', r'Media a $B$ predictori $\hat f_b(x)$ antrenați pe eșantioane bootstrap \refBreA'
       ) + r'''
    \[ \Var\Big(\frac1B\sum_{b=1}^B\hat f_b(x)\Big) = \frac1{B^2}\big(B\sigma^2 + B(B - 1)\rho\sigma^2\big) = \rho\sigma^2 + \frac{1 - \rho}B\sigma^2 \]''',
     [T(r'$\sigma^2$: variance of one predictor; $\rho$: pairwise correlation of two predictors (over the data and the randomisation)',
        r'$\sigma^2$: varianța unui singur predictor; $\rho$: corelația dintre doi predictori (după date și randomizare)'),
      T(r'more trees remove only the second term; the floor $\rho\sigma^2$ is lowered only by \textbf{decorrelating} the trees', r'mai mulți arbori elimină doar al doilea termen; pragul $\rho\sigma^2$ scade doar prin \textbf{decorelarea} arborilor')]),
    (T(r'\textbf{Random forests} \refBreB: a random subset of $m_{\mathrm{try}}$ features at each split lowers $\rho$ at the cost of a little bias', r'\textbf{Pădurile aleatoare} \refBreB: un subset aleator de $m_{\mathrm{try}}$ variabile la fiecare ramificare scade $\rho$, cu prețul unei deplasări mici'),
     [T(r'theory: consistency for additive regression \refSBV; honest trees (separate samples for splits and leaf values) give asymptotically Normal forecasts \refWA',
        r'teorie: consistența pentru regresia aditivă \refSBV; arborii onești (eșantioane separate pentru ramificări și valorile din frunze) dau prognoze asimptotic normale \refWA')]),
    T('Trees cannot extrapolate: a forecast is an average of past targets, so trends and level shifts need differencing or a linear part', 'Arborii nu pot extrapola: o prognoză este o medie a țintelor trecute, deci trendurile și salturile de nivel cer diferențiere sau o parte liniară')), 'small')

D.frame(T('Quantile regression forests', 'Păduri de regresie cuantilică'), items(
    (T(r'\refMei: keep \textbf{all} training targets in the leaves and weight them by how often they share a leaf with $x$', r'\refMei: păstrăm \textbf{toate} țintele de antrenare în frunze și le ponderăm după cît de des împart o frunză cu $x$'
       ) + r'''
    \[ w_i(x) = \frac1B\sum_{b=1}^B \frac{\mathbf 1\{x_i \in L_b(x)\}}{|L_b(x)|}, \qquad \hat F(y\mid x) = \sum_i w_i(x)\,\mathbf 1\{y_i \le y\} \]''',
     [T(r'$L_b(x)$: the leaf of tree $b$ that contains $x$; $|L_b(x)|$: number of training points in it; $\sum_i w_i(x) = 1$',
        r'$L_b(x)$: frunza arborelui $b$ care conține $x$; $|L_b(x)|$: numărul punctelor de antrenare din ea; $\sum_i w_i(x) = 1$'),
      T(r'$\hat F(y\mid x)$: estimated conditional distribution function; quantile $\hat q_\tau(x) = \inf\{y: \hat F(y\mid x) \ge \tau\}$', r'$\hat F(y\mid x)$: funcția de repartiție condiționată estimată; cuantila $\hat q_\tau(x) = \inf\{y: \hat F(y\mid x) \ge \tau\}$')]),
    (T('The same forest gives every quantile: no crossing, no refit per level', 'Aceeași pădure dă toate cuantilele: fără încrucișări, fără reestimare pentru fiecare nivel'),
     [T('consistent for the conditional distribution under regularity conditions; a random forest is an adaptive nearest-neighbour method', 'consistentă pentru distribuția condiționată, în condiții de regularitate; o pădure aleatoare este o metodă adaptivă de tip vecini apropiați')]),
    T(r'Evaluation with the pinball loss and coverage (Chapter 1): the bands are honest only if the forest was trained on data like the future', r'Evaluarea prin pierderea pinball și acoperire (Capitolul 1): benzile sînt corecte doar dacă pădurea a fost antrenată pe date asemănătoare viitorului')), 'small')

D.frame(T('Gradient boosting (1/2): functional gradient descent', 'Gradient boosting (1/2): coborîre pe gradient în spațiul funcțiilor'), items(
    (T(r'\refFri: add small trees, each fitted to the negative gradient of the loss at the current fit', r'\refFri: se adaugă arbori mici, fiecare ajustat pe gradientul negativ al pierderii în punctul curent'
       ) + r'''
    \[ F_m = F_{m-1} + \nu\,h_m, \qquad g_i = -\frac{\partial\ell(y_i, F)}{\partial F}\Big|_{F = F_{m-1}(x_i)} \]''',
     [T(r'$F_m$: the fit after $m$ trees; $h_m$: a small tree fitted to $(x_i, g_i)$; $\nu \in (0, 1]$: learning rate (shrinkage): smaller steps, more trees, lower variance',
        r'$F_m$: funcția estimată după $m$ arbori; $h_m$: un arbore mic ajustat pe $(x_i, g_i)$; $\nu \in (0, 1]$: rata de învățare (shrinkage): pași mai mici, mai mulți arbori, varianță mai mică'),
      T(r'squared loss: $g_i$ = residual; pinball loss: $g_i = \tau - \mathbf 1\{y_i < F\}$ (quantile boosting)', r'pierderea pătratică: $g_i$ = reziduul; pierderea pinball: $g_i = \tau - \mathbf 1\{y_i < F\}$ (boosting cuantilic)')])), 'small')

D.frame(T('Gradient boosting (2/2): second order, histograms, constraints', 'Gradient boosting (2/2): ordinul doi, histograme, restricții'), items(
    (T(r'Second order \refCG: optimal leaf value and the gain of a split', r'Ordinul doi \refCG: valoarea optimă a unei frunze și cîștigul unei ramificări'
       ) + T(r'''
    \[ w^* = -\frac{G}{H + \lambda}, \qquad \mathrm{gain} = \frac12\Big[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{G^2}{H + \lambda}\Big] - \gamma \]''', r'''
    \[ w^* = -\frac{G}{H + \lambda}, \qquad \text{cîștigul} = \frac12\Big[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{G^2}{H + \lambda}\Big] - \gamma \]'''),
     [T(r'$G$, $H$: sums of the first and second derivatives of the loss over the points of a leaf ($L$, $R$: left and right child); $\lambda$: penalty on leaf values; $\gamma$: cost of a split',
        r'$G$, $H$: sumele derivatelor de ordinul întîi și doi ale pierderii pe punctele unei frunze ($L$, $R$: descendentul stîng și drept); $\lambda$: penalizarea valorilor frunzelor; $\gamma$: costul unei ramificări')]),
    (T(r'LightGBM \refKeA', r'LightGBM \refKeA'),
     [T('features binned into histograms (at most 255 bins), leaf-wise growth, gradient-based one-side sampling', 'variabile grupate în histograme (cel mult 255 de intervale), creștere pe frunze, eșantionare unilaterală după gradient'),
      T('scikit-learn HistGradientBoosting (used here) follows the same construction', 'HistGradientBoosting din scikit-learn (folosit aici) urmează aceeași construcție')]),
    (T('Monotone constraints', 'Restricțiile de monotonie'),
     [T('a split is allowed only if the left and right leaf values respect the order; children inherit the bounds', 'o ramificare este permisă doar dacă valorile frunzelor stîngă și dreaptă respectă ordinea; descendenții moștenesc limitele'),
      T('the fit is then monotone in that feature everywhere', 'funcția estimată este atunci monotonă în acea variabilă peste tot')])), 'small')

D.frame(T('Design: Romanian day-ahead load', 'Schema studiului: consumul României pentru ziua următoare'), two(
    ph('tower', T('750 kV line at Mărășești, Romania', 'Linie de 750 kV la Mărășești, România'), h='0.42\\textheight'),
    items(T(r'Forecast the 24 hourly loads of day $d + 1$ with data up to day $d$; evaluation @{ld.days} days, January 2025 -- September 2026', r'Prognozăm cele 24 de valori orare ale zilei $d + 1$ cu date pînă în ziua $d$; evaluare pe @{ld.days} de zile, ianuarie 2025 -- septembrie 2026'),
          T(r'Benchmark: the expert ARX of Chapter 1 (\refZW): one regression per hour, 364-day window, refitted daily', r'Reper: ARX-ul expert din Capitolul 1 (\refZW): o regresie pe oră, fereastră de 364 de zile, reestimat zilnic'),
          (T('Global learners (one model for all hours), refitted monthly on all earlier data', 'Algoritmi globali (un model pentru toate orele), reestimați lunar pe toate datele anterioare'),
           [T('inputs: the same lags, hour, weekday, Romanian holidays, annual cycle', 'intrări: aceleași laguri, ora, ziua săptămînii, sărbătorile din România, ciclul anual'),
            T('RF with QRF bands, HGB, HGB increasing in the three load lags, quantile HGB', 'RF cu benzi QRF, HGB, HGB crescător în cele trei laguri ale consumului, HGB cuantilic')]),
          T('Losses: MAE, average pinball over the deciles, 80\\% coverage; DM against ARX and MCS (Chapter 1)', 'Pierderi: MAE, pinball mediu pe decile, acoperirea de 80\\%; DM față de ARX și MCS (Capitolul 1)')), '0.34', '0.64'), 'small')

chart(T('Trees against the expert ARX', 'Arbori față de ARX-ul expert'), 'ats_ch12_load_trees', 'ATS_ch12_trees', [
    T('Left: one January week with QRF 10\\%--90\\% bands; right: MAE in MW, MCS marks the models in the 90\\% Model Confidence Set', 'Stînga: o săptămînă din ianuarie cu benzile QRF 10\\%--90\\%; dreapta: MAE în MW, MCS marchează modelele din mulțimea de încredere de 90\\%')], h='0.61\\textheight')

interp(('the load comparison', 'comparației pentru consum'), [
    T(r'MAE (MW): ARX @{ld.arx}, RF @{ld.rf}, HGB @{ld.hgb}, monotone HGB @{ld.mono}; the forest is significantly worse (DM @{ld.rf.t}), boosting is not significantly different from ARX', r'MAE (MW): ARX @{ld.arx}, RF @{ld.rf}, HGB @{ld.hgb}, HGB monoton @{ld.mono}; pădurea este semnificativ mai slabă (DM @{ld.rf.t}), boosting nu diferă semnificativ de ARX'),
    T(r'The equal-weight average of ARX and boosting: @{ld.comb} MW, DM @{ld.comb.t} ($p$ @{ld.comb.p}), the only model in the MCS: combination beats selection (Chapter 1)', r'Media egală dintre ARX și boosting: @{ld.comb} MW, DM @{ld.comb.t} ($p$ @{ld.comb.p}), singurul model din MCS: combinarea este mai bună decît selecția (Capitolul 1)'),
    T(r'Quantiles: pinball (MW) ARX @{ld.pin.arx}, quantile HGB @{ld.pin.hgb}, QRF @{ld.pin.qrf}; 80\% coverage @{ld.cov.arx}\%, @{ld.cov.hgb}\%, @{ld.cov.qrf}\%: quantile boosting is sharp but under-covers, QRF over-covers', r'Cuantile: pinball (MW) ARX @{ld.pin.arx}, HGB cuantilic @{ld.pin.hgb}, QRF @{ld.pin.qrf}; acoperirea de 80\%: @{ld.cov.arx}\%, @{ld.cov.hgb}\%, @{ld.cov.qrf}\%: boosting-ul cuantilic este îngust, dar acoperă prea puțin, QRF acoperă prea mult'),
    T('A daily-refitted linear model with the right structure is a strong baseline; trees add value as a complement, not as a replacement', 'Un model liniar reestimat zilnic, cu structura corectă, este un reper puternic; arborii aduc valoare ca o completare, nu ca un înlocuitor')])

chart(T('Monotone constraints in practice', 'Restricțiile de monotonie în practică'), 'ats_ch12_monotone', 'ATS_ch12_trees', [
    T('Partial dependence of the boosted forecast on the load of day $d$ at the same hour, trained on 2023--2024', 'Dependența parțială a prognozei boosting de consumul din ziua $d$ la aceeași oră, antrenat pe 2023--2024')], h='0.68\\textheight')

interp(('the constraint', 'restricției'), [
    T(r'Unconstrained: @{mo.down} decreasing steps (the largest @{mo.worst} MW): more load yesterday would sometimes mean less load tomorrow, a fit to noise', r'Fără restricție: @{mo.down} pași descrescători (cel mai mare de @{mo.worst} MW): mai mult consum ieri ar însemna uneori mai puțin consum mîine, o potrivire a zgomotului'),
    T(r'Constrained: monotone by construction; total range @{mo.r1} GW against @{mo.r0} GW: part of the effect moves to the other lags', r'Cu restricție: monoton prin construcție; amplitudinea totală @{mo.r1} GW față de @{mo.r0} GW: o parte a efectului trece la celelalte laguri'),
    T('Accuracy barely changes (@{ld.mono} against @{ld.hgb} MW); the gain is plausibility and robustness at the edges of the data', 'Acuratețea abia se schimbă (@{ld.mono} față de @{ld.hgb} MW); cîștigul este plauzibilitatea și robustețea la marginile datelor'),
    T('Constraints are how economic knowledge enters a black box: sign restrictions, as in Chapter 3, but for nonlinear learners', 'Restricțiile sînt calea prin care cunoașterea economică intră într-o cutie neagră: restricții de semn, ca în Capitolul 3, dar pentru algoritmi neliniari')])

D.recap(('Tree ensembles', 'ansamblurile de arbori'), [
    T('Bagging and forests reduce variance down to the floor $\\rho\\sigma^2$; decorrelation, not the number of trees, lowers it', 'Bagging-ul și pădurile reduc varianța pînă la pragul $\\rho\\sigma^2$; decorelarea, nu numărul de arbori, îl coboară'),
    T('QRF gives the whole conditional distribution from one forest; boosting fits gradients, with second-order leaves and histograms in LightGBM', 'QRF dă întreaga distribuție condiționată dintr-o singură pădure; boosting-ul ajustează gradienți, cu frunze de ordinul doi și histograme în LightGBM'),
    T('On Romanian load, trees match but do not beat the expert ARX; their combination wins', 'Pe consumul României, arborii egalează ARX-ul expert, dar nu îl depășesc; combinația lor cîștigă')])

# =============================================================================
# 4. DEEP LEARNING PENTRU SECVENȚE
# =============================================================================
D.section('Deep learning for sequences', 'Deep learning pentru secvențe')

D.frame(T('From the MLP to sequence models', 'De la MLP la modelele de secvențe'), two(
    ph('gpu', T('NVIDIA G80, the first CUDA graphics processor (2006)', 'NVIDIA G80, primul procesor grafic CUDA (2006)'), h='0.3\\textheight'),
    items((T(r'An MLP on a window of $L$ lags is a nonlinear AR($L$)', r'Un MLP pe o fereastră de $L$ laguri este un AR($L$) neliniar'
             ) + r'''
    \[ \hat y_{t+h} = W_2\,\sigma(W_1x_t + b_1) + b_2 \]''',
           [T(r'$x_t$: the $L$ most recent values; $W_1$, $W_2$: weight matrices; $b_1$, $b_2$: biases; $\sigma$: activation applied elementwise (ReLU or tanh)',
              r'$x_t$: cele mai recente $L$ valori; $W_1$, $W_2$: matricele de ponderi; $b_1$, $b_2$: termenii liberi (bias); $\sigma$: funcția de activare aplicată pe elemente (ReLU sau tanh)')]),
          (T(r'Training: backpropagation \refRHW\ with Adam \refKB', r'Antrenarea: retropropagare \refRHW\ cu Adam \refKB'),
           [T('early stopping on the last block of the training sample', 'oprire timpurie pe ultimul bloc al eșantionului de antrenare'),
            T('inputs standardised with training moments only', 'intrări standardizate doar cu momentele de antrenare')]),
          (T('Universal approximation says nothing about data needs', 'Aproximarea universală nu spune nimic despre necesarul de date'),
           [T('with a few thousand daily observations, a network has little room over a linear model', 'cu cîteva mii de observații zilnice, o rețea are puțin spațiu față de un model liniar')]),
          T('Sequence models share weights across time: recurrence (RNN), convolution (TCN) or attention (Transformer)', 'Modelele de secvențe partajează ponderile în timp: recurență (RNN), convoluție (TCN) sau atenție (Transformer)')), '0.32', '0.66'), 'small')

D.frame(T('Recurrent networks and backpropagation through time (1/2)', 'Rețele recurente și retropropagarea în timp (1/2)'), items(
    (T(r'Elman RNN: a hidden state updated by the same weights at every step', r'RNN Elman: o stare ascunsă actualizată cu aceleași ponderi la fiecare pas'
       ) + r'''
    \[ h_t = \tanh(W h_{t-1} + U x_t + b), \qquad \hat y_t = V h_t \]''',
     [T(r'$h_t$: hidden state, a learned summary of the past (like the Kalman state of Chapter 6); $x_t$: input; $W$, $U$, $V$, $b$: weights shared over time',
        r'$h_t$: starea ascunsă, un rezumat învățat al trecutului (ca starea Kalman din Capitolul 6); $x_t$: intrarea; $W$, $U$, $V$, $b$: ponderi comune tuturor momentelor')]),
    (T(r'Backpropagation through time (BPTT): the gradient sums contributions of all past steps', r'Retropropagarea în timp (BPTT): gradientul însumează contribuțiile tuturor pașilor trecuți'
       ) + r'''
    \[ \frac{\partial\mathcal L_T}{\partial W} = \sum_{t\le T}\frac{\partial\mathcal L_T}{\partial h_T}\Big(\prod_{k=t+1}^T\frac{\partial h_k}{\partial h_{k-1}}\Big)\frac{\partial^+ h_t}{\partial W} \]
    \[ \frac{\partial h_k}{\partial h_{k-1}} = \mathrm{diag}(1 - h_k^2)\,W \]''',
     [T(r'$\mathcal L_T$: loss at time $T$; $\partial^+h_t/\partial W$: the direct effect of $W$ at step $t$; the contribution of lag $T - t$ is a product of $T - t$ Jacobians',
        r'$\mathcal L_T$: pierderea la momentul $T$; $\partial^+h_t/\partial W$: efectul direct al lui $W$ la pasul $t$; contribuția lagului $T - t$ este un produs de $T - t$ jacobiene')])), 'small')

D.frame(T('Recurrent networks and backpropagation through time (2/2)', 'Rețele recurente și retropropagarea în timp (2/2)'), items(
    (T(r'\refBSF, \refPMB: the product of Jacobians is bounded geometrically', r'\refBSF, \refPMB: produsul jacobienelor este mărginit geometric'
       ) + r'''
    \[ \Big\|\prod_{k=t+1}^T\frac{\partial h_k}{\partial h_{k-1}}\Big\| \le (\gamma\,\|W\|)^{T-t}, \qquad \gamma = \max|\tanh'| \le 1 \]''',
     [T(r'$\gamma\|W\| < 1$: \textbf{vanishing} gradients, long lags cannot be learned', r'$\gamma\|W\| < 1$: gradienți care \textbf{se sting}, lagurile lungi nu pot fi învățate'),
      T(r'spectral radius of $W$ above 1: possible \textbf{explosion}, cured by gradient clipping', r'raza spectrală a lui $W$ peste 1: posibilă \textbf{explozie}, tratată prin limitarea normei gradientului')])), 'small')

D.frame(T('LSTM and GRU: gates (1/2)', 'LSTM și GRU: porțile (1/2)'), two(
    ph('hochreiter', T('Sepp Hochreiter, co-author of the LSTM', 'Sepp Hochreiter, coautor al LSTM'), h='0.36\\textheight'),
    items((T(r'LSTM \refHS: three gates and a candidate, all from $[h_{t-1}, x_t]$', r'LSTM \refHS: trei porți și un candidat, toate calculate din $[h_{t-1}, x_t]$'
             ) + r'''
    \[ i_t, f_t, o_t = \sigma(W_\bullet[h_{t-1}, x_t] + b_\bullet) \]
    \[ \tilde c_t = \tanh(W_c[h_{t-1}, x_t] + b_c) \]''',
           [T(r'$i_t$: input gate; $f_t$: forget gate; $o_t$: output gate; $\sigma$: logistic function, values in $(0, 1)$; $\tilde c_t$: candidate memory',
              r'$i_t$: poarta de intrare; $f_t$: poarta de uitare; $o_t$: poarta de ieșire; $\sigma$: funcția logistică, cu valori în $(0, 1)$; $\tilde c_t$: memoria candidată')]),
          (T(r'Cell and output', r'Celula și ieșirea'
             ) + r'''
    \[ c_t = f_t\odot c_{t-1} + i_t\odot\tilde c_t, \qquad h_t = o_t\odot\tanh(c_t) \]''',
           [T(r'$\odot$: elementwise product; along the cell $\partial c_t/\partial c_{t-1} = \mathrm{diag}(f_t)$: additive, no squashing', r'$\odot$: produsul pe elemente; de-a lungul celulei $\partial c_t/\partial c_{t-1} = \mathrm{diag}(f_t)$: aditiv, fără compresie')])), '0.28', '0.7'), 'footnotesize')

D.frame(T('LSTM and GRU: gates (2/2)', 'LSTM și GRU: porțile (2/2)'), items(
    (T(r'The forget gate \refGSC\ must stay open: $f \approx 1$', r'Poarta de uitare \refGSC\ trebuie să rămînă deschisă: $f \approx 1$'),
     [T(r'a forget bias of 1 is the usual initialisation \refJZS: $\sigma(1) = 0.73$ at the start of training', r'un bias de 1 al porții de uitare este inițializarea obișnuită \refJZS: $\sigma(1) = 0{,}73$ la începutul antrenării')]),
    (T(r'GRU \refCho: two gates, update $z_t$ and reset $r_t$', r'GRU \refCho: două porți, de actualizare $z_t$ și de resetare $r_t$'
       ) + r'''
    \[ h_t = (1 - z_t)\odot h_{t-1} + z_t\odot\tilde h_t \]''',
     [T(r'$\tilde h_t$: candidate state computed from $r_t\odot h_{t-1}$ and $x_t$; fewer parameters than the LSTM, similar behaviour',
        r'$\tilde h_t$: starea candidată, calculată din $r_t\odot h_{t-1}$ și $x_t$; mai puțini parametri decît LSTM, comportament asemănător')])), 'small')

chart(T('How far back does the gradient reach?', 'Distanța în timp pînă la care ajunge gradientul'), 'ats_ch12_vanishing', 'ATS_ch12_recurrent', [
    T(r'Mean $|\partial h_T/\partial x_t|$ of freshly initialised networks (32 units, $T = @{va.T}$, Gaussian inputs, average of @{va.seeds} seeds), log scale', r'Media $|\partial h_T/\partial x_t|$ pentru rețele proaspăt inițializate (32 de unități, $T = @{va.T}$, intrări gaussiene, media a @{va.seeds} seed-uri), scară logaritmică')], h='0.65\\textheight')

interp(('the gradients', 'gradienților'), [
    T(r'At lag 50 the gradient is a fraction @{va.rnn.e50} of its lag-1 value for the tanh RNN, @{va.gru.e50} for the GRU and @{va.lstm.e50} for the LSTM with the default forget bias 0', r'La lagul 50, gradientul este o fracțiune @{va.rnn.e50} din valoarea de la lagul 1 pentru RNN tanh, @{va.gru.e50} pentru GRU și @{va.lstm.e50} pentru LSTM cu bias-ul implicit 0 al porții de uitare'),
    T(r'Forget bias 1: @{va.lstm_b1.e50}; forget bias 3: @{va.lstm_b3.r50}: gates help only when the forget gate is open ($\sigma(3) = 0.95$)', r'Bias 1 al porții de uitare: @{va.lstm_b1.e50}; bias 3: @{va.lstm_b3.r50}: porțile ajută doar cînd poarta de uitare este deschisă ($\sigma(3) = 0{,}95$)'),
    T(r'Decay rates per lag: @{va.rnn.rate} (RNN), @{va.lstm.rate} (LSTM, bias 0), @{va.lstm_b3.rate} (LSTM, bias 3): geometric in every case', r'Ratele de stingere pe lag: @{va.rnn.rate} (RNN), @{va.lstm.rate} (LSTM, bias 0), @{va.lstm_b3.rate} (LSTM, bias 3): geometrice în toate cazurile'),
    T('For daily series this matters less than it seems: HAR-type memory (22 lags) is within reach; for hourly data with weekly cycles (168 lags) it decides the architecture', 'Pentru seriile zilnice contează mai puțin decît pare: memoria de tip HAR (22 de laguri) este accesibilă; pentru datele orare cu ciclu săptămînal (168 de laguri), ea decide arhitectura')])

D.frame(T('Temporal convolutional networks', 'Rețele convoluționale temporale'), items(
    (T(r'Causal dilated convolution: a weighted sum of past inputs spaced $d$ steps apart \refWaveNet', r'Convoluția cauzală dilatată: o sumă ponderată a intrărilor trecute, aflate la distanță de $d$ pași \refWaveNet'
       ) + r'''
    \[ z_t = \sum_{j=0}^{k-1} w_j\,x_{t - d\,j} \]''',
     [T(r'$k$: kernel size; $w_j$: filter weights; $d$: dilation (skips $d - 1$ steps); only the past enters (causal)',
        r'$k$: mărimea nucleului; $w_j$: ponderile filtrului; $d$: dilatarea (sare $d - 1$ pași); intră doar trecutul (cauzal)'),
      T(r'TCN \refBaiK: residual blocks of two dilated causal convolutions, $d = 1, 2, 4, \dots, 2^{\ell-1}$ over $\ell$ levels', r'TCN \refBaiK: blocuri reziduale cu cîte două convoluții cauzale dilatate, $d = 1, 2, 4, \dots, 2^{\ell-1}$ pe $\ell$ niveluri')]),
    (T(r'Receptive field: how far back the network can look', r'Cîmpul receptiv: cît de departe în trecut poate privi rețeaua'
       ) + r'''
    \[ R = 1 + 2(k - 1)(2^\ell - 1) \]''',
     [T(r'$k = 3$, $\ell = 4$: $R = 61$; one week of hours needs $\ell = 7$ ($R = 509$); memory is set by the architecture: no vanishing over time, but nothing beyond $R$',
        r'$k = 3$, $\ell = 4$: $R = 61$; o săptămînă de ore cere $\ell = 7$ ($R = 509$); memoria este fixată de arhitectură: fără stingere în timp, dar nimic dincolo de $R$')]),
    T('Parallel over time (fast training), stable gradients; Bai et al.\\ found TCNs competitive with LSTMs on standard sequence tasks', 'Paralelă în timp (antrenare rapidă), gradienți stabili; Bai et al.\\ au găsit TCN competitive cu LSTM pe sarcini standard de secvențe')), 'small')

D.frame(T('Multi-step forecasts and sequence-to-sequence', 'Prognoze pe mai mulți pași și sequence-to-sequence'), items(
    (T(r'\textbf{Recursive}: one-step model iterated, forecasts fed back as inputs: errors accumulate, the model is trained for $h = 1$ only', r'\textbf{Recursiv}: un model la un pas iterat, prognozele reintroduse ca intrări: erorile se acumulează, modelul este antrenat doar pentru $h = 1$'), []),
    (T(r'\textbf{Direct}: one model per horizon $h$ (our HAR and network forecasts); \textbf{MIMO}: one network outputs the whole vector $(\hat y_{t+1},\dots,\hat y_{t+H})$ (DLinear, N-BEATS, Transformers here)',
       r'\textbf{Direct}: un model pentru fiecare orizont $h$ (prognozele HAR și ale rețelelor de aici); \textbf{MIMO}: o rețea dă întregul vector $(\hat y_{t+1},\dots,\hat y_{t+H})$ (DLinear, N-BEATS, Transformers aici)'), []),
    (T(r'\textbf{Encoder--decoder} \refSVL: an encoder RNN reads the past into a state, a decoder RNN unrolls the future; trained with teacher forcing', r'\textbf{Encoder--decoder} \refSVL: o rețea recurentă codifică trecutul într-o stare, alta desfășoară viitorul; antrenare cu teacher forcing'),
     [T('exposure bias: at test time the decoder sees its own errors; DeepAR samples paths instead', 'deplasarea de expunere: la test, decodorul își vede propriile erori; DeepAR simulează în schimb traiectorii')]),
    T(r'Survey of recurrent forecasting practice \refHBB: deseasonalise or add seasonal lags, scale per series, train globally, ensemble seeds', r'Sinteza practicii recurente \refHBB: desezonalizare sau laguri sezoniere, scalare pe serie, antrenare globală, ansamblu de seed-uri')), 'small')

D.frame(T('Design: deep models against HAR', 'Schema studiului: modele deep față de HAR'), items(
    T(r'Target $y = \log RV$ of the S\&P 500 (\refOMI); forecasts of $RV_{t+h}$, $h \in \{1, 5, 22\}$, direct; level forecast $\exp(\hat m + s^2/2)$ with the training residual variance', r'Ținta $y = \log RV$ pentru S\&P 500 (\refOMI); prognoze ale $RV_{t+h}$, $h \in \{1, 5, 22\}$, directe; prognoza nivelului $\exp(\hat m + s^2/2)$ cu varianța reziduală de antrenare'),
    T(r'Expanding window, first forecast after 2500 days (@{rv.oos}), re-estimation every 500 days; @{rv.T} forecasts per horizon', r'Fereastră extinsă, prima prognoză după 2500 de zile (@{rv.oos}), reestimare la fiecare 500 de zile; @{rv.T} prognoze pe orizont'),
    T(r'Models on the last 22 values: HAR \refCor\ (OLS), MLP (2 $\times$ 32 units), LSTM (16 units), TCN (3 levels, $R = 29$), HGB on the 22 lags; one seed per network', r'Modele pe ultimele 22 de valori: HAR \refCor\ (OLS), MLP (2 $\times$ 32 de unități), LSTM (16 unități), TCN (3 niveluri, $R = 29$), HGB pe cele 22 de laguri; un seed pe rețea'),
    T(r'QLIKE \refPat, DM (HLN) against HAR, MCS; the literature: neural networks gain little over HAR \refBuc; ML gains appear mostly with many predictors \refCSV', r'QLIKE \refPat, DM (HLN) față de HAR, MCS; literatura: rețelele neuronale cîștigă puțin față de HAR \refBuc; cîștigurile ML apar mai ales cu mulți predictori \refCSV')), 'small')

chart(T('Can deep networks beat HAR?', 'Rețele deep față de HAR'), 'ats_ch12_rv_deep', 'ATS_ch12_recurrent', [
    T(r'QLIKE relative to HAR (1 = HAR); a star marks a DM rejection at 5\%', r'QLIKE relativ la HAR (1 = HAR); steaua marchează o respingere DM la 5\%')], h='0.68\\textheight')

interp(('deep models against HAR', 'modelelor deep față de HAR'), [
    T(r'$h = 1$: MLP @{rv.1.mlp}, LSTM @{rv.1.lstm} (DM @{rv.1.lstm.t}), TCN @{rv.1.tcn}, HGB @{rv.1.hgb} (DM @{rv.1.hgb.t}): nothing beats HAR, two are significantly worse', r'$h = 1$: MLP @{rv.1.mlp}, LSTM @{rv.1.lstm} (DM @{rv.1.lstm.t}), TCN @{rv.1.tcn}, HGB @{rv.1.hgb} (DM @{rv.1.hgb.t}): niciun model nu este mai bun decît HAR, două modele sînt semnificativ mai slabe'),
    T(r'$h = 22$: MLP @{rv.22.mlp}, LSTM @{rv.22.lstm}, TCN @{rv.22.tcn}: gains of 3--5\% that DM does not confirm ($p$ @{rv.22.mlp.p}, @{rv.22.lstm.p}); HAR stays in the MCS ($p$ @{rv.22.har.mcs})', r'$h = 22$: MLP @{rv.22.mlp}, LSTM @{rv.22.lstm}, TCN @{rv.22.tcn}: cîștiguri de 3--5\% pe care DM nu le confirmă ($p$ @{rv.22.mlp.p}, @{rv.22.lstm.p}); HAR rămîne în MCS ($p$ @{rv.22.har.mcs})'),
    T(r'Boosting on raw lags is the worst at every horizon: trees cannot extrapolate to the volatility peaks of 2020', r'Boosting-ul pe lagurile brute este cel mai slab la toate orizonturile: arborii nu pot extrapola la vîrfurile de volatilitate din 2020'),
    T('HAR is a linear model with the right three features; a network must rediscover them from a few thousand days', 'HAR este un model liniar cu cele trei variabile potrivite; o rețea trebuie să le redescopere din cîteva mii de zile')])

D.recap(('Deep learning for sequences', 'deep learning pentru secvențe'), [
    T('Gradients through time are products of Jacobians: they vanish geometrically unless the LSTM forget gate stays open', 'Gradienții în timp sînt produse de jacobiene: se sting geometric, cu excepția cazului în care poarta de uitare LSTM rămîne deschisă'),
    T('TCNs fix the memory by the receptive field; multi-step forecasts are recursive, direct or MIMO', 'TCN fixează memoria prin cîmpul receptiv; prognozele pe mai mulți pași sînt recursive, directe sau MIMO'),
    T('On daily realised variance, networks do not significantly beat HAR at any horizon', 'Pe varianța realizată zilnică, rețelele nu sînt semnificativ mai bune decît HAR la niciun orizont')])

# =============================================================================
# 5. ATENȚIE ȘI TRANSFORMERS
# =============================================================================
D.section('Attention and Transformers', 'Atenție și Transformers')

D.frame(T('Scaled dot-product attention', 'Atenția cu produs scalar scalat'), items(
    (T(r'\refVas: each token attends to all tokens, with weights given by query--key similarity', r'\refVas: fiecare token „privește” toți tokenii, cu ponderi date de similaritatea interogare--cheie'
       ) + r'''
    \[ Q = XW_Q, \quad K = XW_K, \quad V = XW_V \]
    \[ \mathrm{Att}(Q, K, V) = \mathrm{softmax}\Big(\frac{QK'}{\sqrt{d_k}}\Big)V \]''',
     [T(r'$X \in \mathbb R^{n\times d}$: $n$ tokens of dimension $d$; $W_Q, W_K, W_V$: learned projections to queries, keys and values; $d_k$: key dimension; softmax normalises each row to weights that sum to 1',
        r'$X \in \mathbb R^{n\times d}$: $n$ tokeni de dimensiune $d$; $W_Q, W_K, W_V$: proiecții învățate în interogări, chei și valori; $d_k$: dimensiunea cheilor; softmax normalizează fiecare rînd în ponderi care însumează 1'),
      T(r'each output is a weighted average of the values, with data-dependent weights; $\sqrt{d_k}$ keeps the logits of order one; multi-head: several projections in parallel, concatenated',
        r'fiecare ieșire este o medie ponderată a valorilor, cu ponderi dependente de date; $\sqrt{d_k}$ menține logiții de ordinul unu; multi-head: mai multe proiecții în paralel, concatenate')]),
    (T(r'Permutation equivariant: without \textbf{positional encodings} the order of the tokens is lost, which is fatal for time series', r'Echivariantă la permutări: fără \textbf{codificări poziționale}, ordinea tokenilor se pierde, ceea ce este fatal pentru serii de timp'), []),
    (T(r'Cost $O(n^2 d)$ in time and memory: one token per hour and a week of input give $n = 168$; a month gives $n = 720$', r'Cost $O(n^2 d)$ în timp și memorie: un token pe oră și o săptămînă de intrare dau $n = 168$; o lună dă $n = 720$'),
     [T('the long-horizon Transformers of 2020--2022 were mostly about this cost', 'Transformers pentru orizonturi lungi din 2020--2022 au urmărit mai ales acest cost')])), 'small')

D.frame(T('Transformers for long horizons', 'Transformers pentru orizonturi lungi'), items(
    (T(r'\textbf{Informer} \refInf: ProbSparse attention (only the most informative queries), self-attention distilling, a generative decoder that outputs the horizon at once: $O(n\log n)$',
       r'\textbf{Informer} \refInf: atenție ProbSparse (doar interogările cele mai informative), distilarea atenției, un decodor generativ care dă orizontul dintr-o dată: $O(n\log n)$'), []),
    (T(r'\textbf{Autoformer} \refAuto: series decomposition inside every layer (moving-average trend and remainder) and an auto-correlation mechanism that aggregates sub-series at lags found by FFT',
       r'\textbf{Autoformer} \refAuto: descompunerea seriei în fiecare strat (trend prin medie mobilă și rest) și un mecanism de autocorelație care agregă subserii la laguri găsite prin FFT'), []),
    (T(r'\textbf{PatchTST} \refNie: tokens are \textbf{patches} of consecutive values (e.g.\ 16 or 24), each channel modelled separately, instance normalisation',
       r'\textbf{PatchTST} \refNie: tokenii sînt \textbf{segmente} de valori consecutive (de exemplu 16 sau 24), fiecare canal modelat separat, normalizare pe instanță'),
     [T('fewer tokens ($n/P$), local semantics in each token, longer look-backs affordable', 'mai puțini tokeni ($n/P$), semnificație locală în fiecare token, ferestre de intrare mai lungi accesibile')]),
    T('All were evaluated on the same handful of benchmarks (electricity, traffic, weather, ETT) with MSE on standardised data', 'Toate au fost evaluate pe aceleași cîteva seturi de date (electricitate, trafic, vreme, ETT), cu MSE pe date standardizate')), 'small')

D.frame(T('Are Transformers effective? The Zeng et al.\\ (2023) critique', 'Critica lui Zeng et al.\\ (2023): eficiența Transformers'), items(
    (T(r'\refZeng: self-attention is permutation-invariant; point-wise tokens carry no local semantics; positional encodings only partly restore order', r'\refZeng: auto-atenția este invariantă la permutări; tokenii punctuali nu au semnificație locală; codificările poziționale restabilesc ordinea doar parțial'), []),
    (T(r'LTSF-Linear baselines: one linear map from the last $L$ values to the next $H$', r'Reperele LTSF-Linear: o singură aplicație liniară de la ultimele $L$ valori la următoarele $H$'
       ) + r'''
    \[ \textbf{Linear:}\ \hat y_{t+1:t+H} = W\,x_{t-L+1:t} \]
    \[ \textbf{DLinear:}\ \hat y = \big(W_s(I - A) + W_tA\big)\,x \]''',
     [T(r'$W$: an $H \times L$ weight matrix; \textbf{NLinear} subtracts and adds back the last value; \textbf{DLinear}: $A$ the moving-average matrix, $W_t$ for the trend $Ax$, $W_s$ for the remainder (Seminar 12, A8)',
        r'$W$: o matrice de ponderi $H \times L$; \textbf{NLinear} scade și adaugă înapoi ultima valoare; \textbf{DLinear}: $A$ matricea mediei mobile, $W_t$ pentru trendul $Ax$, $W_s$ pentru rest (Seminarul 12, A8)')]),
    (T('Their finding: these one-layer models beat Informer, Autoformer and their successors on most of the standard long-horizon benchmarks', 'Rezultatul lor: aceste modele cu un singur strat sînt mai bune decît Informer, Autoformer și succesorii lor pe majoritatea seturilor standard pentru orizonturi lungi'),
     [T('and the Transformers did not improve with a longer look-back $L$: a sign they did not use the extra history', 'iar Transformers nu se îmbunătățeau cu o fereastră $L$ mai lungă: un semn că nu foloseau istoria suplimentară')]),
    T('PatchTST was the reply: patching and channel independence put Transformers back ahead of DLinear on the same benchmarks', 'PatchTST a fost răspunsul: segmentarea și independența canalelor au readus Transformers înaintea DLinear pe aceleași seturi de date')), 'small')

D.frame(T('Replication design: the Zeng et al.\\ protocol on Romanian load', 'Schema replicării: protocolul Zeng et al.\\ pe consumul României'), items(
    T(r'Hourly Romanian load as one series ($n = @{ze.n}$ hours), z-scored with training moments; chronological split 7:1:2; test from @{ze.test}', r'Consumul orar al României ca o singură serie ($n = @{ze.n}$ ore), standardizat cu momentele de antrenare; împărțire cronologică 7:1:2; testul de la @{ze.test}'),
    T(r'Look-back $L = 336$ hours; horizons $H = 96$ and $336$; MSE and MAE on the z-scored series, as in their tables', r'Fereastra de intrare $L = 336$ de ore; orizonturi $H = 96$ și $336$; MSE și MAE pe seria standardizată, ca în tabelele lor'),
    T(r'Models: repeat the last value, seasonal naive (last week), Linear, NLinear, DLinear (kernel 25), a patch Transformer (14 patches of 24 hours, 1 layer, 4 heads) and the same Transformer with one token per hour', r'Modele: repetarea ultimei valori, naiv sezonier (ultima săptămînă), Linear, NLinear, DLinear (nucleu 25), un Transformer pe segmente (14 segmente de 24 de ore, 1 strat, 4 capete) și același Transformer cu un token pe oră'),
    T(r'Adam, MSE, early stopping on the validation block; three seeds averaged (one for the point-token Transformer, whose cost is $O(n^2)$)', r'Adam, MSE, oprire timpurie pe blocul de validare; media a trei seed-uri (unul pentru Transformer-ul cu tokeni punctuali, al cărui cost este $O(n^2)$)')), 'small')

chart(T('Linear models, Transformers and the role of tokens', 'Modele liniare, Transformers și rolul tokenilor'), 'ats_ch12_zeng', 'ATS_ch12_transformers', [
    T(r'Left: test MSE by horizon (repeating the last value, @{ze.96.rep} and @{ze.336.rep}, is off the scale); right: one test window at $H = 96$ (the last week of input, the actual load and three forecasts)', r'Stînga: MSE de test după orizont (repetarea ultimei valori, @{ze.96.rep} și @{ze.336.rep}, iese din scară); dreapta: o fereastră de test la $H = 96$ (ultima săptămînă de intrare, consumul real și trei prognoze)')], h='0.63\\textheight')

interp(('the protocol', 'protocolului'), [
    T(r'$H = 96$: seasonal naive @{ze.96.sn}, Linear @{ze.96.lin}, NLinear @{ze.96.nlin}, DLinear @{ze.96.dlin}; point-token Transformer @{ze.96.trp}; patch Transformer @{ze.96.tr}', r'$H = 96$: naiv sezonier @{ze.96.sn}, Linear @{ze.96.lin}, NLinear @{ze.96.nlin}, DLinear @{ze.96.dlin}; Transformer cu tokeni punctuali @{ze.96.trp}; Transformer pe segmente @{ze.96.tr}'),
    T(r'$H = 336$: DLinear @{ze.336.dlin}, point tokens @{ze.336.trp} (worse than every linear model), patches @{ze.336.tr}', r'$H = 336$: DLinear @{ze.336.dlin}, tokeni punctuali @{ze.336.trp} (mai slab decît orice model liniar), segmente @{ze.336.tr}'),
    T('Both papers replicate on our data: the point-token Transformer is no better than NLinear or DLinear at $H = 96$ and worse than every linear model at $H = 336$; patching overturns the ranking', 'Ambele lucrări se replică pe datele noastre: Transformer-ul cu tokeni punctuali nu este mai bun decît NLinear sau DLinear la $H = 96$ și este mai slab decît orice model liniar la $H = 336$; segmentarea răstoarnă clasamentul'),
    T(r'The gap between the best linear model and the patch Transformer shrinks from @{ze.96.nlin} against @{ze.96.tr} at $H = 96$ to @{ze.336.nlin} against @{ze.336.tr} at $H = 336$: at long horizons the series is mostly seasonal level', r'Distanța dintre cel mai bun model liniar și Transformer-ul pe segmente scade de la @{ze.96.nlin} față de @{ze.96.tr} la $H = 96$ la @{ze.336.nlin} față de @{ze.336.tr} la $H = 336$: la orizonturi lungi seria este mai ales nivel sezonier')])

D.frame(T('The Temporal Fusion Transformer', 'Temporal Fusion Transformer'), items(
    (T(r'\refTFT: built for multi-horizon forecasts with three kinds of inputs: static (the store, the country), known future (calendar, prices), observed past', r'\refTFT: construit pentru prognoze pe mai multe orizonturi, cu trei tipuri de intrări: statice (magazinul, țara), viitoare cunoscute (calendar, prețuri), trecute observate'), []),
    (T('Components', 'Componente'),
     [T(r'gated residual networks (GRN): $\mathrm{LayerNorm}\big(a + \mathrm{GLU}(\eta)\big)$, a gate that can switch a block off', r'rețele reziduale cu poartă (GRN): $\mathrm{LayerNorm}\big(a + \mathrm{GLU}(\eta)\big)$, o poartă care poate opri un bloc'),
      T('variable selection networks: softmax weights over the inputs at each time', 'rețele de selecție a variabilelor: ponderi softmax pe intrări la fiecare moment'),
      T('static covariate encoders that condition every other block; an LSTM encoder--decoder for local patterns', 'codificatori ai covariatelor statice care condiționează celelalte blocuri; un encoder--decoder LSTM pentru tipare locale'),
      T('interpretable multi-head attention (values shared across heads) for long-range dependence; quantile outputs trained with the pinball loss', 'atenție multi-head interpretabilă (valori comune tuturor capetelor) pentru dependența de lungă durată; ieșiri cuantilice antrenate cu pierderea pinball')]),
    T('Its ``interpretability\'\' is the variable-selection weights and the attention pattern: useful diagnostics, not causal explanations (Section 7)', '„Interpretabilitatea” lui înseamnă ponderile de selecție a variabilelor și tiparul atenției: diagnostice utile, nu explicații cauzale (secțiunea 7)')), 'small')

D.recap(('Attention and Transformers', 'atenție și Transformers'), [
    T('Attention is a data-dependent weighted average; order comes only from positional encodings; cost is quadratic in the tokens', 'Atenția este o medie ponderată dependentă de date; ordinea vine doar din codificările poziționale; costul este pătratic în numărul de tokeni'),
    T('Zeng et al.: one linear layer beat point-token Transformers; PatchTST: patches restore the advantage; both replicate on Romanian load', 'Zeng et al.: un strat liniar a fost mai bun decît Transformers cu tokeni punctuali; PatchTST: segmentele refac avantajul; ambele se replică pe consumul României'),
    T('The TFT organises static, known and observed inputs with gates, selection and attention, and outputs quantiles', 'TFT organizează intrările statice, cunoscute și observate prin porți, selecție și atenție și dă cuantile')])

# =============================================================================
# 6. N-BEATS, N-HiTS, DeepAR
# =============================================================================
D.section('Global deep models: N-BEATS, N-HiTS, DeepAR', 'Modele deep globale: N-BEATS, N-HiTS, DeepAR')

D.frame(T('N-BEATS: basis expansion with residual stacking', 'N-BEATS: dezvoltare în baze de funcții cu stivuire reziduală'), items(
    (T(r'\refOre: each block reconstructs part of its input (backcast) and forecasts the rest', r'\refOre: fiecare bloc reconstruiește o parte a intrării (backcast) și prognozează restul'
       ) + r'''
    \[ \hat x_\ell = g^b(\theta^b_\ell), \quad \hat y_\ell = g^f(\theta^f_\ell) \]
    \[ x_{\ell+1} = x_\ell - \hat x_\ell, \quad \hat y = \sum_\ell\hat y_\ell \]''',
     [T(r'$x_\ell$: input of block $\ell$; $\theta^b_\ell, \theta^f_\ell$: coefficients produced by four fully connected layers; $g^b$, $g^f$: basis functions; doubly residual: each block explains what the previous ones left',
        r'$x_\ell$: intrarea blocului $\ell$; $\theta^b_\ell, \theta^f_\ell$: coeficienții produși de patru straturi complet conectate; $g^b$, $g^f$: funcțiile de bază; dublu rezidual: fiecare bloc explică ce au lăsat cele anterioare')]),
    (T(r'\textbf{Generic}: $g$ linear and learned; \textbf{interpretable}: trend basis $\{(t/H)^j\}_{j\le3}$ and seasonality basis $\{\cos 2\pi jt/H, \sin 2\pi jt/H\}$',
       r'\textbf{Generic}: $g$ liniar și învățat; \textbf{interpretabil}: baza de trend $\{(t/H)^j\}_{j\le3}$ și baza sezonieră $\{\cos 2\pi jt/H, \sin 2\pi jt/H\}$'),
     [T(r'$H$: forecast horizon; a learned decomposition, similar to exponential smoothing', r'$H$: orizontul prognozei; o descompunere învățată, asemănătoare netezirii exponențiale')]),
    (T('Pure deep learning, no time-series features; trained globally per frequency with sMAPE/MASE losses; the published results are ensembles of 180 networks', 'Deep learning pur, fără variabile specifice seriilor de timp; antrenat global pe fiecare frecvență cu pierderi sMAPE/MASE; rezultatele publicate sînt ansambluri de 180 de rețele'),
     [T('their M4 result beat the competition winner, the ES-RNN hybrid of \\refSmyl', 'rezultatul lor pe M4 l-a depășit pe cîștigătorul competiției, hibridul ES-RNN al lui \\refSmyl')])), 'small')

D.frame(T('N-HiTS: multi-rate inputs, hierarchical outputs', 'N-HiTS: intrări pe mai multe rate, ieșiri ierarhice'), items(
    (T(r'\refNHiTS: block $\ell$ first max-pools its input with kernel $k_\ell$ (e.g.\ 8, 4, 1): low-resolution blocks see the long-run shape, high-resolution blocks the detail', r'\refNHiTS: blocul $\ell$ aplică întîi max-pooling cu nucleul $k_\ell$ (de exemplu 8, 4, 1): blocurile de rezoluție mică văd forma pe termen lung, cele de rezoluție mare detaliul'), []),
    (T(r'Each block outputs only $H/r_\ell$ coefficients, interpolated to $H$ points: the expressiveness ratio $r_\ell$ forces coarse blocks to forecast smooth components', r'Fiecare bloc dă doar $H/r_\ell$ coeficienți, interpolați la $H$ puncte: raportul de expresivitate $r_\ell$ obligă blocurile grosiere să prognozeze componente netede'),
     [T('an explicit frequency decomposition of the forecast, close in spirit to the wavelet multiresolution of Chapter 11', 'o descompunere explicită pe frecvențe a prognozei, apropiată de multirezoluția wavelet din Capitolul 11')]),
    T('Fewer parameters and less compute than N-BEATS for long horizons, with similar accuracy on short ones', 'Mai puțini parametri și mai puțin calcul decît N-BEATS la orizonturi lungi, cu acuratețe asemănătoare la cele scurte'),
    T(r'Ours: generic N-BEATS (3 blocks $\times$ 3 layers $\times$ 256 units) and N-HiTS (pools 8, 4, 1), input 336 hours, each window divided by its mean absolute level, MAE loss, median of @{m4.seeds} seeds', r'Ale noastre: N-BEATS generic (3 blocuri $\times$ 3 straturi $\times$ 256 de unități) și N-HiTS (pooling 8, 4, 1), intrare de 336 de ore, fiecare fereastră împărțită la nivelul ei mediu absolut, pierdere MAE, mediana a @{m4.seeds} seed-uri')), 'small')

D.frame(T('Design: the M4 hourly subset', 'Schema studiului: subsetul orar M4'), items(
    T(r'\refMfourA: @{ov.m4} hourly series, horizon 48', r'\refMfourA: @{ov.m4} de serii orare, orizont 48'),
    (T(r'Accuracy measures: symmetric MAPE, scaled error and their average relative to Naive 2', r'Măsurile de acuratețe: MAPE simetric, eroarea scalată și media lor relativă la Naive 2'
       ) + r'''
    \[ \mathrm{OWA} = \frac12\Big(\frac{\mathrm{sMAPE}}{\mathrm{sMAPE}_{\mathrm{Naive2}}} + \frac{\mathrm{MASE}}{\mathrm{MASE}_{\mathrm{Naive2}}}\Big) \]''',
     [T(r'sMAPE: mean of $2|y - \hat y|/(|y| + |\hat y|)$ in \%; MASE: mean absolute error divided by the in-sample MAE of the seasonal naive (period 24) \refHK; OWA $< 1$: better than Naive 2',
        r'sMAPE: media lui $2|y - \hat y|/(|y| + |\hat y|)$, în \%; MASE: eroarea absolută medie împărțită la MAE din eșantion al naivului sezonier (perioada 24) \refHK; OWA $< 1$: mai bun decît Naive 2')]),
    (T('Naive, seasonal naive and Naive 2 are computed here', 'Naive, naivul sezonier și Naive 2 sînt calculate aici'),
     [T(r'Naive 2: sMAPE @{m4.n2.s} (official M4 value @{mo4.n2.s}), MASE @{m4.n2.m} (official @{mo4.n2.m})', r'Naive 2: sMAPE @{m4.n2.s} (valoarea oficială M4 @{mo4.n2.s}), MASE @{m4.n2.m} (oficial @{mo4.n2.m})')]),
    (T('Reference points from the official M4 evaluation file (OWA)', 'Repere din fișierul oficial de evaluare M4 (OWA)'),
     [T(r'the M4 MLP and RNN benchmarks: @{mo4.mlp.o} and @{mo4.rnn.o}; Theta @{mo4.th.o}', r'reperele M4 MLP și RNN: @{mo4.mlp.o} și @{mo4.rnn.o}; Theta @{mo4.th.o}'),
      T(r'the winner \refSmyl\ @{mo4.smyl.o}; the runner-up Montero-Manso et al.\ @{mo4.mm.o}', r'cîștigătorul \refSmyl\ @{mo4.smyl.o}; locul doi Montero-Manso et al.\ @{mo4.mm.o}')]),
    T('All global models are trained only on the training parts', 'Toate modelele globale sînt antrenate doar pe părțile de antrenare')), 'small')

chart(T('Global deep models on the M4 hourly series', 'Modele deep globale pe seriile orare M4'), 'ats_ch12_m4', 'ATS_ch12_global_deep', [
    T(r'Left: OWA (Naive 2 = 1); right: one series with the seasonal naive, N-BEATS and N-HiTS forecasts', r'Stînga: OWA (Naive 2 = 1); dreapta: o serie cu prognozele naivului sezonier, N-BEATS și N-HiTS')], h='0.58\\textheight')

interp(('the M4 hourly results', 'rezultatelor M4 orare'), [
    T(r'OWA: seasonal naive @{m4.sn.o}, DLinear @{m4.dl.o}, N-BEATS @{m4.nb.o} (sMAPE @{m4.nb.s}, MASE @{m4.nb.m}), N-HiTS @{m4.nh.o}', r'OWA: naiv sezonier @{m4.sn.o}, DLinear @{m4.dl.o}, N-BEATS @{m4.nb.o} (sMAPE @{m4.nb.s}, MASE @{m4.nb.m}), N-HiTS @{m4.nh.o}'),
    T(r'A few minutes of CPU training put N-BEATS ahead of every M4 benchmark and of the M4 neural benchmarks (@{mo4.mlp.o}, @{mo4.rnn.o}), behind the two best entries (@{mo4.smyl.o}, @{mo4.mm.o})', r'Cîteva minute de antrenare pe procesor pun N-BEATS înaintea tuturor reperelor M4 și a reperelor neuronale M4 (@{mo4.mlp.o}, @{mo4.rnn.o}), în urma primelor două participări (@{mo4.smyl.o}, @{mo4.mm.o})'),
    T(r'The M4 neural benchmarks were local (one network per series); ours are global: pooling 414 series is what makes the difference', r'Reperele neuronale M4 erau locale (o rețea pe serie); ale noastre sînt globale: reunirea celor 414 serii face diferența'),
    T('DLinear is weaker here: hourly M4 series need nonlinear interactions of level and season that one linear layer cannot express', 'DLinear este mai slab aici: seriile orare M4 cer interacțiuni neliniare între nivel și sezon pe care un singur strat liniar nu le poate exprima')])

D.frame(T('DeepAR: probabilistic forecasts from a global RNN', 'DeepAR: prognoze probabilistice dintr-o rețea recurentă globală'), items(
    (T(r'\refDeepAR: an LSTM state per series drives the parameters of a likelihood', r'\refDeepAR: o stare LSTM pentru fiecare serie determină parametrii unei verosimilități'
       ) + r'''
    \[ h_{i,t} = \mathrm{LSTM}(h_{i,t-1}, z_{i,t-1}, x_{i,t}), \qquad z_{i,t} \sim \ell\big(\cdot\mid\theta(h_{i,t})\big) \]''',
     [T(r'$z_{i,t}$: value of series $i$ at $t$; $x_{i,t}$: covariates (lags at 1, 24, 168, calendar); $\theta(h)$: e.g.\ Gaussian $(\mu, \sigma)$ for real data, negative binomial for counts',
        r'$z_{i,t}$: valoarea seriei $i$ la $t$; $x_{i,t}$: covariabilele (laguri la 1, 24, 168, calendar); $\theta(h)$: de exemplu gaussiană $(\mu, \sigma)$ pentru date reale, binomială negativă pentru numărări'),
      T(r'training: maximise $\sum_{i,t}\log\ell(z_{i,t}\mid\theta(h_{i,t}))$ over random windows of all series, each scaled by $1 + $ the mean of its context', r'antrenarea: maximizăm $\sum_{i,t}\log\ell(z_{i,t}\mid\theta(h_{i,t}))$ pe ferestre aleatoare din toate seriile, fiecare scalată cu $1 + $ media contextului')]),
    (T('Forecast: ancestral sampling, each draw fed back as the next input; quantiles from the sample paths', 'Prognoza: simulare ancestrală, fiecare extragere reintrodusă ca intrare următoare; cuantilele din traiectoriile simulate'
       ) + r'''
    \[ \mathrm{wQL} = \sum_\tau\frac{2\sum_{i,t}\rho_\tau(z_{i,t} - \hat q_{\tau,i,t})}{\sum_{i,t}|z_{i,t}|} \]''',
     [T(r'weighted quantile loss: $\rho_\tau$ the pinball loss at level $\tau$, $\hat q_\tau$ the forecast quantile; an approximation of the CRPS \refGR, lower is better',
        r'pierderea cuantilică ponderată: $\rho_\tau$ pierderea pinball la nivelul $\tau$, $\hat q_\tau$ cuantila prognozată; o aproximare a CRPS \refGR, o valoare mai mică este mai bună')]),
    T('The model of choice for large retail and energy panels; the base of several foundation models (Chapter 13)', 'Modelul preferat pentru paneluri mari din retail și energie; baza mai multor foundation models (Capitolul 13)')), 'small')

chart(T('A small DeepAR on the M4 hourly series', 'Un DeepAR mic pe seriile orare M4'), 'ats_ch12_deepar', 'ATS_ch12_global_deep', [
    T(r'Two-layer LSTM (40 units), context 168 hours, @{da.steps} training steps of 64 windows, 100 sample paths; the same series as on the previous chart', r'LSTM cu două straturi (40 de unități), context de 168 de ore, @{da.steps} de pași de antrenare cu cîte 64 de ferestre, 100 de traiectorii simulate; aceeași serie ca în graficul anterior')], h='0.54\\textheight')

interp(('DeepAR', 'DeepAR'), [
    T(r'wQL by training budget (steps): 500: @{da.b500}, 1000: @{da.b1000}, 2000: @{da.b2000}, 4000: @{da.b4000}; seasonal naive with empirical quantiles: @{da.snw}', r'wQL după bugetul de antrenare (pași): 500: @{da.b500}, 1000: @{da.b1000}, 2000: @{da.b2000}, 4000: @{da.b4000}; naivul sezonier cu cuantile empirice: @{da.snw}'),
    T(r'After 1000 steps DeepAR beats the benchmark (80\% coverage @{da.c1000}\%); with longer training it overfits the training windows and loses (@{da.c4000}\% at 4000 steps)', r'După 1000 de pași, DeepAR este mai bun decît reperul (acoperirea de 80\%: @{da.c1000}\%); cu antrenare mai lungă, supraajustează ferestrele de antrenare și pierde (@{da.c4000}\% la 4000 de pași)'),
    T('Choosing the best checkpoint on this table would be data snooping: the budget must be fixed on a validation block before the test period is opened', 'Alegerea celui mai bun punct de control din acest tabel ar fi data snooping: bugetul trebuie fixat pe un bloc de validare înainte de a deschide perioada de test'),
    T('Probabilistic deep models are sensitive to the training budget; report the rule that set it, and the benchmark under a proper score', 'Modelele deep probabilistice sînt sensibile la bugetul de antrenare; raportați regula care l-a fixat și reperul sub o regulă de scor proprie')])

D.frame(T('Lessons from the M5 competition', 'Lecțiile competiției M5'), items(
    (T(r'\refMfiveA: 42\,840 Walmart series in a hierarchy, daily unit sales, 28 days ahead; accuracy and uncertainty tracks', r'\refMfiveA: 42\,840 de serii Walmart într-o ierarhie, vînzări zilnice în unități, 28 de zile înainte; secțiunile de acuratețe și de incertitudine'),
     [T('the winning accuracy methods were global LightGBM models on engineered features (lags, rolling means, prices, calendar), often combined', 'metodele cîștigătoare la acuratețe au fost modele LightGBM globale pe variabile construite (laguri, medii mobile, prețuri, calendar), adesea combinate')]),
    T('Global models, cross-learning and external information (prices, events) mattered more than architecture', 'Modelele globale, învățarea între serii și informația externă (prețuri, evenimente) au contat mai mult decît arhitectura'),
    T('The simple benchmarks were beaten, but by smaller margins than ML marketing suggests, and least at the bottom level of the hierarchy', 'Reperele simple au fost depășite, dar cu marje mai mici decît sugerează publicitatea ML și cel mai puțin la nivelul de jos al ierarhiei'),
    T(r'An earlier warning: ML methods lost to statistical ones on the M3 monthly data \refMSAa; the difference between M3 and M5 is data size and cross-series learning', r'Un avertisment anterior: metodele ML au pierdut în fața celor statistice pe datele lunare M3 \refMSAa; diferența dintre M3 și M5 este volumul de date și învățarea între serii')), 'small')

D.recap(('Global deep models', 'modele deep globale'), [
    T('N-BEATS and N-HiTS: residual stacks of fully connected blocks, generic or with trend and seasonal bases, multi-rate in N-HiTS', 'N-BEATS și N-HiTS: stive reziduale de blocuri complet conectate, generice sau cu baze de trend și sezon, pe mai multe rate în N-HiTS'),
    T('On M4 hourly, global N-BEATS beats every benchmark and the local neural networks of M4', 'Pe M4 orar, N-BEATS global depășește toate reperele și rețelele neuronale locale din M4'),
    T('DeepAR gives sample paths from a likelihood; it beats the seasonal naive under the wQL only at the right training budget, which must be set on validation data', 'DeepAR dă traiectorii dintr-o verosimilitate; depășește naivul sezonier sub wQL doar la bugetul de antrenare potrivit, care trebuie fixat pe date de validare')])

# =============================================================================
# 7. INTERPRETARE ȘI COMPARAȚII ONESTE
# =============================================================================
D.section('Interpretation and the honest benchmark', 'Interpretare și comparații riguroase')

D.frame(T('Shapley values (1/2): the definition', 'Valorile Shapley (1/2): definiția'), items(
    (T(r'\refSha: the fair share of player $g$ in a cooperative game $v$ with $G$ players', r'\refSha: partea echitabilă a jucătorului $g$ într-un joc cooperativ $v$ cu $G$ jucători'
       ) + r'''
    \[ \phi_g = \sum_{S \subseteq \{1..G\}\setminus g}\frac{|S|!\,(G - |S| - 1)!}{G!}\big[v(S\cup g) - v(S)\big] \]''',
     [T(r'$v(S)$: the value of coalition $S$; $v(S\cup g) - v(S)$: the marginal contribution of $g$; the weights average it over all orders in which players can join',
        r'$v(S)$: valoarea coaliției $S$; $v(S\cup g) - v(S)$: contribuția marginală a lui $g$; ponderile o mediază pe toate ordinile în care jucătorii pot intra')]),
    (T(r'The unique allocation with four axioms', r'Singura alocare care respectă patru axiome'),
     [T(r'efficiency ($\sum_g\phi_g = v(\mathrm{all}) - v(\emptyset)$), symmetry, dummy (a player who adds nothing gets 0) and additivity',
        r'eficiența ($\sum_g\phi_g = v(\mathrm{toate}) - v(\emptyset)$), simetria, jucătorul nul (un jucător care nu adaugă nimic primește 0) și aditivitatea')])), 'small')

D.frame(T('Shapley values (2/2): SHAP for forecasts', 'Valorile Shapley (2/2): SHAP pentru prognoze'), items(
    (T(r'SHAP \refLL: players are features; the value of a coalition $S$ is the expected forecast when only $x_S$ is known', r'SHAP \refLL: jucătorii sînt variabilele; valoarea unei coaliții $S$ este prognoza așteptată cînd se cunoaște doar $x_S$'
       ) + r'''
    \[ v(S) = \E\big[f(x_S, X_{\bar S})\big] \]''',
     [T(r'$f$: the fitted model; $\bar S$: the other features; \textbf{interventional}: $X_{\bar S}$ from a background sample, independent of $x_S$; \textbf{observational}: conditional on $x_S$',
        r'$f$: modelul estimat; $\bar S$: celelalte variabile; \textbf{intervențional}: $X_{\bar S}$ dintr-un eșantion de fundal, independent de $x_S$; \textbf{observațional}: condiționat de $x_S$'),
      T('with lags, features are strongly correlated: interventional values evaluate the model at impossible histories; group correlated lags instead', 'cu laguri, variabilele sînt puternic corelate: valorile intervenționale evaluează modelul pe istorii imposibile; grupați în schimb lagurile corelate')]),
    T(r'Here: exact Shapley values of three lag groups (day, days 2--5, days 6--22) for boosting on S\&P 500 log RV, @{sh.ne} forecast days, @{sh.nb} background days', r'Aici: valori Shapley exacte pentru trei grupuri de laguri (ziua, zilele 2--5, zilele 6--22) pentru boosting pe logaritmul RV S\&P 500, @{sh.ne} zile de prognoză, @{sh.nb} zile de fundal')), 'small')

chart(T('What the boosted model has learned', 'Tiparul învățat de modelul boosting'), 'ats_ch12_shap', 'ATS_ch12_interpretation', [
    T('Each point: one forecast day; horizontal: the mean log RV of the group; vertical: its Shapley value', 'Fiecare punct: o zi de prognoză; orizontal: media logaritmului RV a grupului; vertical: valoarea lui Shapley')], h='0.54\\textheight')

interp(('the Shapley values', 'valorilor Shapley'), [
    T(r'Mean $|\phi|$ shares: last day @{sh.d}\%, days 2--5 @{sh.w}\%, days 6--22 @{sh.m}\%', r'Ponderile mediei $|\phi|$: ultima zi @{sh.d}\%, zilele 2--5 @{sh.w}\%, zilele 6--22 @{sh.m}\%'),
    T(r'HAR on the same sample: coefficients @{sh.har.d}, @{sh.har.w}, @{sh.har.m} on the daily, weekly and monthly means: the boosted trees rediscovered the HAR cascade', r'HAR pe același eșantion: coeficienți @{sh.har.d}, @{sh.har.w}, @{sh.har.m} pentru mediile zilnică, săptămînală și lunară: arborii boosting au redescoperit cascada HAR'),
    T('The values flatten at the extremes: trees cap their forecasts at the training range, the reason boosting lost to HAR in 2020', 'Valorile se aplatizează la extreme: arborii își limitează prognozele la intervalul de antrenare, motivul pentru care boosting a pierdut față de HAR în 2020'),
    T('Shapley values describe the model, not the data-generating process: a correct description of a wrong model is still wrong', 'Valorile Shapley descriu modelul, nu procesul generator: descrierea corectă a unui model greșit rămîne greșită')])

D.frame(T('Attention is not explanation', 'Atenția nu este explicație'), items(
    (T(r'\refJW: attention weights are often uncorrelated with gradient-based importance, and very different attention patterns give the same predictions', r'\refJW: ponderile atenției sînt adesea necorelate cu importanța bazată pe gradient, iar tipare de atenție foarte diferite dau aceleași prognoze'), []),
    (T(r'\refWP: attention can be a faithful explanation under conditions, but this must be tested, not assumed', r'\refWP: atenția poate fi o explicație fidelă în anumite condiții, dar acest lucru trebuie testat, nu presupus'), []),
    (T(r'A test: occlusion importance, the increase of the MSE when one input patch is replaced by the window mean, against the attention each patch receives', r'Un test: importanța prin ocluzie, creșterea MSE cînd un segment de intrare este înlocuit cu media ferestrei, față de atenția primită de fiecare segment'),
     [T(r'on the patch Transformer of Section 5 ($H = 96$), the first 1000 test windows', r'pe Transformer-ul pe segmente din secțiunea 5 ($H = 96$), primele 1000 de ferestre de test')])), 'small')

chart(T('Where the Transformer looks, and what it uses', 'Atenția Transformer-ului și informația folosită'), 'ats_ch12_attention', 'ATS_ch12_interpretation', [
    T(r'Share of attention received by each of the @{at.nt} daily patches against the share of occlusion importance', r'Ponderea atenției primite de fiecare dintre cele @{at.nt} segmente zilnice față de ponderea importanței prin ocluzie')], h='0.68\\textheight')

interp(('attention and occlusion', 'atenției și ocluziei'), [
    T(r'The last day carries @{at.lo}\% of the occlusion importance but receives only @{at.la}\% of the attention', r'Ultima zi poartă @{at.lo}\% din importanța prin ocluzie, dar primește doar @{at.la}\% din atenție'),
    T(r'Most attention goes to the patch @{at.ta} days back; the most important patch is @{at.to} day back; Spearman correlation @{at.rho}', r'Cea mai mare atenție merge la segmentul de acum @{at.ta} zile; cel mai important segment este cel de acum @{at.to} zi; corelația Spearman @{at.rho}'),
    T('The flatten head reads the token states directly: what matters can bypass the attention weights entirely', 'Capul care aplatizează citește direct stările tokenilor: ce contează poate ocoli complet ponderile atenției'),
    T('Report attention maps as what they are, a mixing pattern; for importance, use occlusion, Shapley or gradients, with a sanity check', 'Raportați hărțile de atenție drept ceea ce sînt, un tipar de amestecare; pentru importanță folosiți ocluzia, Shapley sau gradienții, cu o verificare de control')])

D.frame(T('The honest benchmark', 'Comparația riguroasă'), items(
    (T('Strong baselines first: seasonal naive, ETS/Theta, HAR, an expert ARX; Lago et al.\\ built an open benchmark because published electricity-price models were rarely compared with them \\refLMDW', 'Întîi repere puternice: naiv sezonier, ETS/Theta, HAR, un ARX expert; Lago et al.\\ au construit un reper deschis pentru că modelele publicate de prețuri ale electricității erau rar comparate cu ele \\refLMDW'), []),
    (T(r'Pitfalls catalogued by \refHAB: test-set reuse, leakage in scaling and features, errors averaged across series of different scales, no significance tests, unreported tuning budget', r'Capcanele inventariate de \refHAB: reutilizarea setului de test, leakage prin scalare și variabile, erori mediate pe serii de scări diferite, fără teste de semnificație, buget de reglare neraportat'), []),
    (T(r'Tests (Chapter 1): DM for two models, MCS \refHLN\ for many, the reality check \refWhi\ and SPA \refHan\ when the best of many was chosen on the same data', r'Teste (Capitolul 1): DM pentru două modele, MCS \refHLN\ pentru mai multe, reality check \refWhi\ și SPA \refHan\ cînd cel mai bun dintre multe a fost ales pe aceleași date'), []),
    T('Report seeds, hardware, training time, every architecture tried; pre-register the design (Chapter 0)', 'Raportați seed-urile, hardware-ul, timpul de antrenare, fiecare arhitectură încercată; preînregistrați schema (Capitolul 0)')), 'small')

chart(T('Seeds and data snooping', 'Seed-uri și data snooping'), 'ats_ch12_snooping', 'ATS_ch12_interpretation', [
    T(r'Left: MLP against HAR for S\&P 500 RV, $h = 1$, with @{sn.n} seeds and their ensemble; right: simulation, $K$ equally good models, 2500 test days, correlation 0.5', r'Stînga: MLP față de HAR pentru RV S\&P 500, $h = 1$, cu @{sn.n} seed-uri și ansamblul lor; dreapta: simulare, $K$ modele la fel de bune, 2500 de zile de test, corelație 0,5')], h='0.62\\textheight')

interp(('seeds and snooping', 'seed-urilor și a data snooping'), [
    T(r'Seeds alone move the QLIKE ratio from @{sn.best} to @{sn.worst} (median @{sn.med}); the ensemble of the seeds reaches @{sn.ens}, better than every single seed', r'Doar seed-urile mută raportul QLIKE între @{sn.best} și @{sn.worst} (mediana @{sn.med}); ansamblul seed-urilor ajunge la @{sn.ens}, mai bun decît orice seed individual'),
    T(r'Picking the best of $K$ equally good models on the test set: the DM test declares it better (one-sided, nominal 2.5\%) in @{sn.rej1}\% of cases for $K = 1$, @{sn.rej10}\% for $K = 10$, @{sn.rej100}\% for $K = 100$', r'Alegerea celui mai bun dintre $K$ modele la fel de bune pe setul de test: testul DM îl declară mai bun (unilateral, nivel nominal 2,5\%) în @{sn.rej1}\% din cazuri pentru $K = 1$, @{sn.rej10}\% pentru $K = 10$, @{sn.rej100}\% pentru $K = 100$'),
    T('Hyper-parameter searches, seeds and architectures are all $K$: count them, and test the winner with SPA or MCS on data not used for the choice', 'Căutările de hiperparametri, seed-urile și arhitecturile sînt toate $K$: numărați-le și testați cîștigătorul cu SPA sau MCS pe date nefolosite pentru alegere'),
    T('Ensembles are the cheap cure for seed variance; pre-registration is the cure for snooping', 'Ansamblurile sînt remediul ieftin pentru varianța seed-urilor; preînregistrarea este remediul pentru data snooping')])

D.recap(('Interpretation and honest benchmarks', 'interpretare și comparații riguroase'), [
    T('Shapley values have axioms; with lagged features use groups and remember they describe the model', 'Valorile Shapley au axiome; cu variabile întîrziate folosiți grupuri și amintiți-vă că ele descriu modelul'),
    T('Attention weights are not importance: on our Transformer they point the other way', 'Ponderile atenției nu sînt importanță: pe Transformer-ul nostru ele indică în direcția opusă'),
    T('Strong baselines, DM/MCS/SPA, all seeds and all tries reported: otherwise any model can be made to win', 'Repere puternice, DM/MCS/SPA, toate seed-urile și toate încercările raportate: altfel orice model poate fi făcut să cîștige')])

# =============================================================================
# AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Do machine-learning and deep models forecast realised volatility better than HAR, across markets and horizons, once the comparison is pre-registered?', 'Prognozează modelele de machine learning și deep learning volatilitatea realizată mai bine decît HAR, pe mai multe piețe și orizonturi, atunci cînd comparația este preînregistrată?'),
     [T(r'formal: $H_0$: $\E[\mathrm{QLIKE}_{\mathrm{ML}} - \mathrm{QLIKE}_{\mathrm{HAR}}] \ge 0$ in each cell; a cell supports ML only if DM rejects at 5\% and the MCS excludes HAR', r'formal: $H_0$: $\E[\mathrm{QLIKE}_{\mathrm{ML}} - \mathrm{QLIKE}_{\mathrm{HAR}}] \ge 0$ în fiecare celulă; o celulă susține ML doar dacă DM respinge la 5\% și MCS exclude HAR'),
      T('falsified if fewer than a fifth of the cells support ML', 'infirmată dacă mai puțin de o cincime din celule susțin ML')]),
    (T('Why it matters: risk systems (VaR, margins, option hedging) run on volatility forecasts; a spurious ML gain becomes a model risk', 'Miza: sistemele de risc (VaR, marje, acoperirea opțiunilor) se bazează pe prognoze de volatilitate; un cîștig ML aparent devine un risc de model'),
     [T(r'literature to start from: \refCor, \refBuc, \refCSV, \refHAB', r'literatura de pornire: \refCor, \refBuc, \refCSV, \refHAB')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers since 2019 comparing neural networks or boosting with HAR for realised volatility out of sample; give DOIs and the test used.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează articole recenzate din 2019 încoace care compară rețele neuronale sau boosting cu HAR pentru volatilitatea realizată în afara eșantionului; dă DOI-urile și testul folosit.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{design}: \aiprompt{Write a pre-registration: assets, horizons, windows, refit schedule, loss, tests, seeds, what counts as a win.}', r'\textbf{schema}: \aiprompt{Scrie o preînregistrare: active, orizonturi, ferestre, calendarul reestimării, pierderea, testele, seed-urile, ce înseamnă un cîștig.}'),
      T(r'\textbf{code and replication}: reproduce first the S\&P 500 HAR QLIKE (@{rv.1.har} at $h = 1$ here), then add learners one at a time', r'\textbf{cod și replicare}: reproduceți întîi QLIKE HAR pentru S\&P 500 (@{rv.1.har} la $h = 1$ aici), apoi adăugați algoritmii pe rînd'),
      T(r'\textbf{critique}: \aiprompt{Act as a hostile referee: list every source of leakage, snooping and unfair tuning in this comparison.}', r'\textbf{critica}: \aiprompt{Joacă rolul unui recenzent ostil: enumeră fiecare sursă de leakage, data snooping și reglare inechitabilă din această comparație.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('No future information: scaling, feature construction and tuning use only data before each origin; purge around $h$-step targets', 'Nicio informație din viitor: scalarea, construcția variabilelor și reglarea folosesc doar date dinaintea fiecărei origini; purjare în jurul țintelor la $h$ pași'),
    T('The baseline is tuned as carefully as the learner, and refitted on the same schedule', 'Reperul este reglat la fel de atent ca algoritmul și reestimat după același calendar'),
    T('Seeds, architectures and hyper-parameters tried are all reported; the winner is tested with MCS or SPA', 'Seed-urile, arhitecturile și hiperparametrii încercați sînt toți raportați; cîștigătorul este testat cu MCS sau SPA'),
    T('An AI claim that ``LSTMs capture long memory, so they beat HAR\'\' is checked against the numbers, not accepted', 'O afirmație AI de tipul „LSTM captează memoria lungă, deci este mai bun decît HAR” se verifică pe cifre, nu se acceptă')), 'small')

chart(T('Mini-case: do learners beat HAR across markets?', 'Mini studiu de caz: algoritmii față de HAR pe mai multe piețe'), 'ats_ch12_ai_case', 'ATS_ch12_ai_case', [
    T(r'@{ai.n} cells: six indices $\times$ three horizons $\times$ two learners (MLP, boosting), the expanding design of Section 4; QLIKE ratio to HAR, a star where DM rejects at 5\%', r'@{ai.n} de celule: șase indici $\times$ trei orizonturi $\times$ doi algoritmi (MLP, boosting), schema cu fereastră extinsă din secțiunea 4; raportul QLIKE față de HAR, o stea unde DM respinge la 5\%'),
    T(r'Ratios from @{ai.min} to @{ai.max}, median @{ai.med} (MLP @{ai.mlp}, boosting @{ai.hgb}); @{ai.better} cells below 1, @{ai.sb} significantly better, @{ai.sw} significantly worse: the hypothesis is falsified for these learners', r'Rapoarte între @{ai.min} și @{ai.max}, mediana @{ai.med} (MLP @{ai.mlp}, boosting @{ai.hgb}); @{ai.better} celule sub 1, @{ai.sb} semnificativ mai bune, @{ai.sw} semnificativ mai slabe: ipoteza este infirmată pentru acești algoritmi')],
    h='0.55\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{Deep learning against HAR for Central and Eastern European volatility}: replicate first, then extend', r'\textbf{Deep learning față de HAR pentru volatilitatea din Europa Centrală și de Est}: întîi replicare, apoi extindere'),
     [T(r'replicate: \refCor\ HAR and the neural comparison of \refBuc\ on the Oxford-Man indices, with the design of Section 4', r'replicați: HAR \refCor\ și comparația neuronală din \refBuc\ pe indicii Oxford-Man, cu schema din secțiunea 4'),
      T('extend: intraday-based RV for the BET, WIG20 and EUR/RON; global models across markets; exogenous predictors (VIX, macro news) as in \\refCSV', 'extindeți: RV din date intraday pentru BET, WIG20 și EUR/RON; modele globale pe mai multe piețe; predictori exogeni (VIX, știri macro) ca în \\refCSV'),
      T('pre-register: markets, horizons, windows, every learner and its tuning budget, QLIKE, DM, MCS, seeds', 'preînregistrați: piețele, orizonturile, ferestrele, fiecare algoritm și bugetul lui de reglare, QLIKE, DM, MCS, seed-urile')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Validation must respect dependence: K-fold only for well-specified autoregressions; otherwise block, purge and keep a final test period', 'Validarea trebuie să respecte dependența: K subeșantioane doar pentru autoregresii bine specificate; altfel blocuri, purjare și o perioadă finală de test'),
    T('Global models pool series and afford memory; high-dimensional selection on short macro samples is unstable', 'Modelele globale reunesc seriile și își permit memorie; selecția în dimensiune mare pe eșantioane macro scurte este instabilă'),
    T('Trees and networks rarely beat strong structured baselines alone (expert ARX, HAR); they help in combinations and in large panels', 'Arborii și rețelele depășesc rar, singure, reperele puternice și structurate (ARX expert, HAR); ajută în combinații și în paneluri mari'),
    T('Architecture details matter: open forget gates, patches instead of point tokens, global training', 'Detaliile de arhitectură contează: porți de uitare deschise, segmente în loc de tokeni punctuali, antrenare globală'),
    T('Attention is not explanation; seeds and searches are hidden multiple testing', 'Atenția nu este explicație; seed-urile și căutările sînt testare multiplă ascunsă')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T('Why is random K-fold valid for an AR(3) fitted to AR(3) data but not for 22-day targets?', 'De ce este validă validarea cu K subeșantioane aleatoare pentru un AR(3) estimat pe date AR(3), dar nu pentru ținte de 22 de zile?'),
        T('Which condition does the adaptive lasso remove, and how?', 'Ce condiție elimină lasso-ul adaptiv și cum?'),
        T('Why does adding trees not reduce the variance of a forest below $\\rho\\sigma^2$?', 'De ce adăugarea de arbori nu reduce varianța unei păduri sub $\\rho\\sigma^2$?'),
        T('What is the receptive field of a TCN with $k = 3$ and five levels?', 'Care este cîmpul receptiv al unui TCN cu $k = 3$ și cinci niveluri?'),
        T('Why can a patch Transformer beat DLinear when a point-token Transformer cannot?', 'De ce poate un Transformer pe segmente să fie mai bun decît DLinear, iar unul cu tokeni punctuali nu?'))),
    block(T('Next: Chapter 13', 'Urmează: Capitolul 13'), items(
        T('Foundation models and conformal prediction', 'Foundation models și predicție conformală'),
        T('pretrained models used zero-shot, and distribution-free intervals for any forecaster, including the ones of this chapter', 'modele preantrenate folosite zero-shot și intervale fără ipoteze de distribuție pentru orice model, inclusiv cele din acest capitol'))),
    '0.58', '0.38'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the bias of K-fold under autocorrelated errors', 'Anexă: deplasarea validării cu K subeșantioane sub erori autocorelate'), items(
    T(r'Linear model $y = X\beta + \varepsilon$; leave out row $i$: $e_{(i)} = e_i/(1 - h_{ii})$, $h_{ii}$ the leverage', r'Model liniar $y = X\beta + \varepsilon$; omitem rîndul $i$: $e_{(i)} = e_i/(1 - h_{ii})$, $h_{ii}$ efectul de pîrghie'),
    T(r'$\E\,e_{(i)}^2 \approx \sigma^2(1 + h_{ii}) - 2\sum_{j\ne i}\frac{H_{ij}}{1 - h_{ii}}\Cov(\varepsilon_i, \varepsilon_j)$ to first order', r'$\E\,e_{(i)}^2 \approx \sigma^2(1 + h_{ii}) - 2\sum_{j\ne i}\frac{H_{ij}}{1 - h_{ii}}\Cov(\varepsilon_i, \varepsilon_j)$, la ordinul întîi'),
    T(r'Uncorrelated errors: the second term vanishes and LOOCV estimates the out-of-sample MSE $\sigma^2(1 + h)$: the Bergmeir--Hyndman--Koo case', r'Erori necorelate: al doilea termen dispare, iar LOOCV estimează MSE în afara eșantionului $\sigma^2(1 + h)$: cazul Bergmeir--Hyndman--Koo'),
    T(r'Positive correlation between the left-out error and the neighbouring training errors ($H_{ij} > 0$ for neighbours with similar lags): the estimate is too small; purging sets the neighbouring terms to zero', r'Corelație pozitivă între eroarea omisă și erorile de antrenare vecine ($H_{ij} > 0$ pentru vecinii cu laguri asemănătoare): estimația este prea mică; purjarea anulează termenii vecini')), 'small')

D.frame(T('Appendix: soft thresholding and the elastic net', 'Anexă: pragul moale și elastic net'), items(
    T(r'With $X\'X = nI$ the objective separates: $\frac12(\beta_j - z_j)^2 + \lambda|\beta_j|$ for each $j$, $z_j = x_j\'y/n$', r'Cu $X\'X = nI$, funcția obiectiv se separă: $\frac12(\beta_j - z_j)^2 + \lambda|\beta_j|$ pentru fiecare $j$, $z_j = x_j\'y/n$'),
    T(r'Subgradient: $0 \in \beta_j - z_j + \lambda\,\partial|\beta_j|$; if $|z_j| \le \lambda$, $\beta_j = 0$; otherwise $\beta_j = z_j - \lambda\,\mathrm{sign}(z_j)$', r'Subgradientul: $0 \in \beta_j - z_j + \lambda\,\partial|\beta_j|$; dacă $|z_j| \le \lambda$, $\beta_j = 0$; altfel $\beta_j = z_j - \lambda\,\mathrm{sign}(z_j)$'),
    T(r'Elastic net: $\frac12(\beta_j - z_j)^2 + \lambda\alpha|\beta_j| + \frac{\lambda(1 - \alpha)}2\beta_j^2$ gives $\beta_j = S(z_j, \lambda\alpha)/(1 + \lambda(1 - \alpha))$', r'Elastic net: $\frac12(\beta_j - z_j)^2 + \lambda\alpha|\beta_j| + \frac{\lambda(1 - \alpha)}2\beta_j^2$ dă $\beta_j = S(z_j, \lambda\alpha)/(1 + \lambda(1 - \alpha))$'),
    T(r'Adaptive lasso: threshold $\lambda w_j = \lambda/|\tilde\beta_j|^\gamma$, small for large $|\tilde\beta_j|$: the bias on large coefficients vanishes, which gives the oracle property', r'Lasso adaptiv: pragul $\lambda w_j = \lambda/|\tilde\beta_j|^\gamma$, mic pentru $|\tilde\beta_j|$ mare: deplasarea coeficienților mari dispare, de unde proprietatea de oracol')), 'small')

D.references(bib(), per=14)

if __name__ == '__main__':
    finalize(D.write(V))
