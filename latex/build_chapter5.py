r"""
build_chapter5.py -- Capitolul 5 (Modele VAR bayesiene, modele factoriale și nowcasting), EN + RO
==================================================================================================
Text T(en, ro); cifrele @{cheie} vin din Quantlets/Ch_05/ch5_numbers.json (generate_all_charts.py). Nicio cifră nu
este scrisă de mînă (în afara exemplelor teoretice). TSA, Capitolul 6 a predat VAR în formă redusă, TSA, Capitolul 10
filtrul Kalman; Capitolul 3 a construit identificarea structurală; aici: dimensiuni mari, shrinkage, factori, nowcasting.
Ieșire:
  EN/Courses/chapter5_bvar_factor_models_nowcasting.tex
  RO/Cursuri/capitol5_bvar_modele_factoriale_nowcasting.tex
Rulare:
  python3 Quantlets/Ch_05/generate_all_charts.py
  python3 latex/build_chapter5.py && python3 latex/ats_build.py compile 5
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ats_build import Deck, Values, table, photo, cols, block   # noqa: E402
from ats_build import items as _items   # noqa: E402
from ch5_common import REFS, QLURL, T, bib, finalize, load, minus_fix, quarter   # noqa: E402


def items(*xs):
    return _items(*[x[0] if isinstance(x, tuple) and not x[1] else x for x in xs])


N = load()
V = Values()
D = Deck(5, 'lecture', refs=REFS)
C = 'https://commons.wikimedia.org/wiki/File:'
P = V.put


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
    'laplace': ('ch5_laplace_guerin_1838.jpg', C + 'Pierre-Simon_Laplace.jpg',
                T('Portrait', 'Portret') + ': Paulin Guérin (1838); ' + PD + '; Wikimedia Commons'),
    'minneapolis': ('ch5_minneapolis_fed_2010.jpg', C + 'Federal_Reserve_Bank_of_Minneapolis_building_2.jpg',
                    FOTO + ': Innotata (2010); CC BY-SA 3.0; Wikimedia Commons'),
    'reichlin': ('ch5_reichlin_2013.jpg', C + 'Lucrezia_Reichlin_-_Festival_Economia_2013_(cropped).JPG',
                 FOTO + ': Niccolò Caranti (2013); CC BY-SA 3.0; Wikimedia Commons'),
    'bernanke': ('ch5_bernanke_2008.jpg', C + 'Ben_Bernanke_official_portrait_(cropped).jpg',
                 FOTO + ': Federal Reserve (2008); ' + PD + '; Wikimedia Commons'),
    'ins': ('ch5_ins_bucharest_2009.jpg', C + 'Institutul_Național_de_Statistică.jpg',
            FOTO + ': Dan Mihai Pitea (2009); CC BY-SA 3.0; Wikimedia Commons'),
}


def ph(key, cap, h='0.42\\textheight'):
    f, url, cred = PH[key]
    return photo(f, cap, url, cred, h=h)


def two(left, right, wl='0.4', wr='0.58'):
    return cols(left, right, wl, wr)


# =============================================================================
# CIFRE
# =============================================================================
c = N['curse']
P('cu.ols24', c['ols'][-1], 2)
P('cu.ols8', c['ols'][2], 2)
P('cu.bv24', c['bvar'][-1], 2)
P('cu.ar24', c['ar'][-1], 2)
P('cu.lam2', c['lam'][0], 2)
P('cu.lam24', c['lam'][-1], 2)
V.raw('cu.k24', str(c['k'][-1]))
V.raw('cu.reps', str(c['reps']))
cj = N['conj']
for t in ('T24', 'T240'):
    for k in ('ols', 'post', 'post_sd', 'se'):
        P(f'cj.{t}.{k}', cj[t][k], 3)
    P(f'cj.{t}.w', 100 * cj[t]['w_prior'], 1)
g = N['gibbs']
for t in ('raw', 'centred'):
    V.int(f'gb.{t}.ess', round(g[t]['ess']))
    P(f'gb.{t}.rhat', g[t]['rhat'], 2)
    P(f'gb.{t}.gw', g[t]['geweke'], 2)
    P(f'gb.{t}.acf1', g[t]['acf1'], 3)
    P(f'gb.{t}.corr', g[t]['corr_ab'], 3)
    P(f'gb.{t}.mean', g[t]['mean'], 4)
    P(f'gb.{t}.sd', g[t]['sd'], 4)
V.int('gb.n', g['n_kept'])
V.raw('gb.T', str(g['T']))
P('gb.xm', g['xmean'], 1)
P('gb.xs', g['xsd'], 1)
lb = N['lambda']
for s in ('SMALL', 'MEDIUM', 'LARGE'):
    P(f'lb.{s}', lb[s]['lam'], 3)
    V.raw(f'lb.{s}.n', str(lb[s]['n']))
    P(f'lb.{s}.l02', lb[s]['lml_02'], 1)
    P(f'lb.{s}.l1', lb[s]['lml_1'], 1)
for s in ('SMALL', 'MEDIUM'):
    for k in ('mu', 'phi'):
        P(f'lb.{s}.{k}', lb[s]['glp'][k], 2)
V.raw('lb.T', str(lb['SMALL']['T']))
tr = N['tradeoff']
P('tr.best', tr['best'], 2)
P('tr.bestoos', tr['best_oos'], 2)
P('tr.loose', tr['loose_oos'], 2)
P('tr.tight', tr['tight_oos'], 2)
V.raw('tr.k', str(tr['k']))
b = N['bgr']
P('bg.lmed', b['lam_fit']['MEDIUM'], 3)
P('bg.llar', b['lam_fit']['LARGE'], 3)
P('bg.fit', b['lam_fit']['target'], 2)
V.raw('bg.nl', str(b['n_large']))
V.int('bg.kl', b['k_large'])
V.raw('bg.no', str(b['n_origins']))
for s in ('SMALL', 'MEDIUM'):
    P(f'bg.glp.{s}', b['glp_lam'][s]['median'], 2)
    P(f'bg.glp.{s}.lo', b['glp_lam'][s]['q10'], 2)
    P(f'bg.glp.{s}.hi', b['glp_lam'][s]['q90'], 2)
MOD = {'OLS SMALL': 'ols', 'BGR MEDIUM': 'med', 'BGR LARGE': 'lar', 'GLP SMALL': 'gsm', 'GLP MEDIUM': 'gme'}
VAR = {'USPRIV': 'emp', 'CPIAUCSL': 'cpi', 'FEDFUNDS': 'ffr'}
for per in ('eval1', 'pre2020', 'eval2'):
    for m, mk in MOD.items():
        for v, vk in VAR.items():
            for h in (1, 3, 6, 12):
                x = b[per][f'{m}|{v}|{h}']
                if x < 1000:
                    P(f'bg.{per}.{mk}.{vk}{h}', x, 2)
                else:
                    V.raw(f'bg.{per}.{mk}.{vk}{h}', '$>1000$')
ir = N['irf']
for s in ('SMALL', 'MEDIUM', 'LARGE'):
    for k in ('emp_min', 'emp12', 'emp12_lo', 'emp12_hi', 'emp48', 'emp48_lo', 'emp48_hi', 'cpi_max', 'cpi48', 'cpi48_lo', 'cpi48_hi'):
        P(f'ir.{s}.{k}', ir[s][k], 2)
    V.raw(f'ir.{s}.ea', str(ir[s]['emp_arg']))
    V.raw(f'ir.{s}.ca', str(ir[s]['cpi_argmax']))
V.raw('ir.nd', str(ir['LARGE']['ndraw']))
vo = N['vol']
P('vo.gm', vo['ratio_gm'], 2)
V.int('vo.peak', round(vo['ratio_peak']))
P('vo.tail', 100 * vo['share_tail'], 2)
fa = N['factors']
V.raw('fa.N', str(fa['N']))
V.raw('fa.T', str(fa['T']))
P('fa.miss', 100 * fa['miss'], 1)
P('fa.s1', 100 * fa['share'][0], 1)
P('fa.s2', 100 * fa['share'][1], 1)
P('fa.c5', 100 * fa['cum5'], 1)
P('fa.c8', 100 * fa['cum8'], 1)
for k, v in fa['k'].items():
    V.raw(f'fa.k.{k}', str(v))
P('fa.rec', fa['corr_rec'], 2)
V.raw('fa.nout', str(fa['n_out']))
mr = N['mr2']
for j in (1, 2, 3):
    for gname, key in (('Output and income', 'out'), ('Labour market', 'lab'), ('Housing', 'hou'), ('Prices', 'pri'),
                       ('Interest and exchange rates', 'rat')):
        P(f'mr.f{j}.{key}', mr[f'f{j}'][gname], 2)
P('mr.top1', mr['top1'][0][1], 2)
di = N['di']
for per in ('eval1', 'pre2020', 'eval2'):
    for v, vk in (('INDPRO', 'ip'), ('PAYEMS', 'emp'), ('CPIAUCSL', 'cpi')):
        for h in (1, 6, 12):
            for m, mk in (('DI', 'di'), ('DI-AR, Lag', 'dl')):
                P(f'di.{per}.{vk}.{mk}{h}', di[per][f'{v}|{h}|{m}'], 2)
V.raw('di.kmed', str(int(di['k_median'])))
V.raw('di.kq10', str(int(di['k_q10'])))
V.raw('di.kq90', str(int(di['k_q90'])))
fv = N['favar']
V.raw('fv.T', str(fv['info']['T']))
V.raw('fv.N', str(fv['info']['N']))
V.raw('fv.Ns', str(fv['info']['Nslow']))
P('fv.ipmin', fv['INDPRO']['min'], 2)
V.raw('fv.iparg', str(fv['INDPRO']['argmin']))
P('fv.cpimax', fv['CPIAUCSL']['max'], 3)
V.raw('fv.cpiarg', str(fv['CPIAUCSL']['argmax']))
P('fv.cpi48', fv['CPIAUCSL']['h48'], 2)
P('fv.cpi48lo', fv['CPIAUCSL']['lo48'], 2)
P('fv.cpi48hi', fv['CPIAUCSL']['hi48'], 2)
P('fv.cpi482', fv['CPIAUCSL']['h48_2'], 2)
P('fv.umax', fv['UNRATE']['max'], 3)
P('fv.hmin', fv['HOUST']['min'], 2)
V.raw('fv.harg', str(fv['HOUST']['argmin']))
P('fv.empmin', fv['PAYEMS']['min'], 2)
P('fv.ffrmax', fv['FEDFUNDS']['max'], 2)
P('fv.cumin', fv['CUMFNS']['min'], 2)
rd = N['rodata']
V.raw('rd.N', str(rd['N']))
V.raw('rd.nq', str(rd['n_q']))
V.raw('rd.lastq', quarter(rd['last_q']))
P('rd.lasty', rd['last_y'], 2)
P('rd.covid', rd['y2020q2'], 1)
P('rd.cesi', rd['corr_esi'], 2)
md = N['midas']
for k in ('ip', 'esi'):
    P(f'md.{k}.b', md[k]['b'], 2)
    P(f'md.{k}.w0', md[k]['w'][0], 2)
P('md.ipmax', max(md['ip']['w']), 2)
V.raw('md.iparg', str(int(max(range(6), key=lambda j: md['ip']['w'][j]))))
P('md.rho', md['rho'], 2)
nc = N['nowcast']
for m, mk in (('AR', 'ar'), ('Bridge', 'br'), ('MIDAS', 'md'), ('DFM', 'dfm'), ('DFM (EM)', 'em')):
    for vv in ('M1', 'M2', 'M3', 'M+1'):
        tag = vv.replace('+', 'p')
        P(f'nc.{mk}.{tag}', nc['rmse'][f'{m}|{vv}'], 2)
        P(f'nc.cv.{mk}.{tag}', nc['rmse_covid'][f'{m}|{vv}'], 2)
        P(f'nc.lg.{mk}.{tag}', nc['rmse_long'][f'{m}|{vv}'], 2)
P('nc.sd', nc['sd_y'], 2)
P('nc.dmt', nc['dm_t'], 2)
P('nc.dmp', nc['dm_p'], 2)
V.raw('nc.nq', str(nc['nq']))
nw = N['news']
pth = nw['path']
for k, lab in (('2026-06-01', 'jun'), ('2026-07-01', 'jul'), ('2026-08-01', 'aug'), ('2026-09-01', 'sep')):
    for m in ('dfm', 'em', 'bridge', 'ar'):
        P(f'nw.{lab}.{m}', pth[k][m], 2)
P('nw.old', nw['old'], 2)
P('nw.new', nw['new'], 2)
P('nw.sum', nw['sum_impact'], 2)
for k in ('ip', 'esi', 'ip_ea', 'retail', 'bci'):
    P(f'nw.by.{k}', nw['by'][k], 2)
P('nw.ipnews', nw['top'][0]['news'], 1)
P('nw.ipw', nw['top'][0]['weight'], 3)
V.raw('nw.n', str(nw['n_news']))
ai = N['ai']
P('ai.min', ai['vmin'], 2)
P('ai.max', ai['vmax'], 2)
V.raw('ai.n', str(ai['n']))
V.raw('ai.nb', str(ai['n_better']))
minus_fix(V)

TB = '>{\\raggedright\\arraybackslash}'

# =============================================================================
# DESCHIDERE
# =============================================================================
D.frame(T("Today's question and route", 'Întrebarea de azi și traseul'), items(
    (T(r'\textbf{Question}: how do we forecast and analyse an economy described by a hundred series, some of them published monthly and late, others quarterly?',
       r'\textbf{Întrebarea}: cum prognozăm și analizăm o economie descrisă de o sută de serii, unele publicate lunar și cu întîrziere, altele trimestrial?'),
     [T('an unrestricted VAR with 100 variables and 13 lags has more than 130\\,000 coefficients: the data alone cannot pin them down',
        'un VAR nerestricționat cu 100 de variabile și 13 laguri are peste 130\\,000 de coeficienți: datele singure nu îi pot determina')]),
    (T(r'\textbf{Route} of the chapter', r'\textbf{Traseul} capitolului'),
     [T('the curse of dimensionality; Bayesian inference at the depth we need (conjugacy, Gibbs sampling, MCMC diagnostics)',
        'blestemul dimensionalității; inferența bayesiană la nivelul necesar (conjugare, eșantionarea Gibbs, diagnosticarea MCMC)'),
      T('Minnesota and Normal--inverse-Wishart priors, dummy observations, shrinkage chosen by the marginal likelihood, large BVARs',
        'distribuțiile a priori Minnesota și Normal--inverse-Wishart, observații fictive, shrinkage ales prin verosimilitatea marginală, modele BVAR mari'),
      T('factor models: principal components, the number of factors, diffusion indexes, FAVAR, dynamic factor models',
        'modele factoriale: componente principale, numărul de factori, indici de difuziune, FAVAR, modele factoriale dinamice'),
      T('mixed frequencies and nowcasting: bridge equations, MIDAS, the Kalman filter with a ragged edge, news; Romanian GDP',
        'frecvențe mixte și nowcasting: ecuații punte, MIDAS, filtrul Kalman cu date incomplete la sfîrșitul eșantionului, știri; PIB-ul României')]),
    T('We build on TSA, Chapter 6 (VAR), TSA, Chapter 10 (Kalman filter) and Chapter 3 (structural VAR); Seminar 5 comes before this lecture',
      'Pornim de la TSA, Capitolul 6 (VAR), TSA, Capitolul 10 (filtrul Kalman) și Capitolul 3 (VAR structural); Seminarul 5 are loc înaintea acestui curs')), 'small')

D.frame(T('Learning outcomes', 'Rezultatele învățării'), items(
    T('Derive conjugate posteriors, run a Gibbs sampler and judge its convergence with trace plots, effective sample size and $\\widehat R$',
      'Derivați distribuții a posteriori conjugate, rulați un eșantionator Gibbs și judecați convergența cu grafice de traiectorie, mărimea efectivă a eșantionului și $\\widehat R$'),
    T('Write the Minnesota prior in natural conjugate form and with dummy observations, and explain each hyperparameter',
      'Scrieți distribuția a priori Minnesota în formă natural conjugată și cu observații fictive și explicați fiecare hiperparametru'),
    T('Choose the tightness of a large BVAR by the marginal likelihood or by the in-sample fit rule, and evaluate the forecasts out of sample',
      'Alegeți gradul de shrinkage al unui BVAR mare prin verosimilitatea marginală sau prin regula potrivirii în eșantion și evaluați prognozele în afara eșantionului'),
    T('Estimate approximate factor models by principal components, select the number of factors and build diffusion-index forecasts and a FAVAR',
      'Estimați modele factoriale aproximative prin componente principale, alegeți numărul de factori și construiți prognoze cu indici de difuziune și un FAVAR'),
    T('Nowcast quarterly GDP from monthly data with bridge equations, MIDAS and a dynamic factor model, and decompose each revision into news',
      'Realizați nowcasting pentru PIB-ul trimestrial din date lunare cu ecuații punte, MIDAS și un model factorial dinamic și descompuneți fiecare revizuire în știri')), 'small')

D.frame(T('Reading, data and tools', 'Bibliografie, date și instrumente'), items(
    (T(r'Backbone: \refKL, Ch.~5 (Bayesian VAR) and Ch.~16 (large VARs, factors); \refKarl; \refSWc', r'Manualul de bază: \refKL, cap.~5 (VAR bayesian) și cap.~16 (VAR mari, factori); \refKarl; \refSWc'),
     [T(r'Bayesian background: \refBDA; state space: \refDK; nowcasting survey: \refBGMR', r'Fundamente bayesiene: \refBDA; spațiul stărilor: \refDK; sinteză despre nowcasting: \refBGMR')]),
    (T(r'Python Quantlets of this chapter: \href{' + QLURL + r'}{Quantlets/Ch\_05}', r'Quantlet-urile Python ale capitolului: \href{' + QLURL + r'}{Quantlets/Ch\_05}'),
     [T(r'Minnesota and Normal--inverse-Wishart BVAR, marginal likelihood, PCA with EM, Bai--Ng, FAVAR, Kalman filter and news written in \texttt{numpy}',
        r'BVAR Minnesota și Normal--inverse-Wishart, verosimilitatea marginală, PCA cu EM, Bai--Ng, FAVAR, filtrul Kalman și știrile scrise explicit în \texttt{numpy}'),
      T(r'comparison packages: \texttt{statsmodels} (DynamicFactorMQ, EM estimation of the nowcasting model) and \texttt{bvar} of the Bank of England (GLP hyperparameters)',
        r'pachete de comparație: \texttt{statsmodels} (DynamicFactorMQ, estimarea EM a modelului de nowcasting) și \texttt{bvar} al Băncii Angliei (hiperparametri GLP)')]),
    T(r'Lecture notebook: \href{\colaburl{notebooks/EN/chapter5_lecture_notebook.ipynb}}{open in Google Colab}',
      r'Notebook-ul cursului: \href{\colaburl{notebooks/EN/chapter5_lecture_notebook.ipynb}}{deschideți în Google Colab}')), 'small')

D.frame(T('Data used in this chapter', 'Datele folosite în acest capitol'), table(
    TB + 'p{5.0cm}' + TB + 'p{4.6cm}' + TB + 'p{2.4cm}',
    T(r'\textbf{Series}', r'\textbf{Seria}') + ' & ' + T(r'\textbf{Source}', r'\textbf{Sursa}') + ' & ' + T(r'\textbf{Use}', r'\textbf{Utilizare}'),
    [T(r'@{fa.N} US monthly series in the FRED-MD format (output, labour, housing, orders, money, rates, prices), 1960:1--2026:7',
       r'@{fa.N} serii lunare SUA în formatul FRED-MD (producție, muncă, locuințe, comenzi, monedă, dobînzi, prețuri), 1960:1--2026:7') + ' & ' +
     T(r'FRED (St.~Louis Fed), one CSV per series; FRED-MD transformation codes \refMN', r'FRED (St.~Louis Fed), cîte un CSV pe serie; codurile de transformare FRED-MD \refMN') + ' & BVAR, ' + T('factors, FAVAR', 'factori, FAVAR'),
     T('NBER recession dates; US capacity utilisation, unemployment rate', 'datele recesiunilor NBER; gradul de utilizare a capacităților, rata șomajului din SUA') + ' & FRED (USREC, CUMFNS, UNRATE) & ' + T('charts, Gibbs', 'grafice, Gibbs'),
     T(r'Romania: IP, retail trade, construction, unemployment, six confidence indicators (@{rd.N} monthly series); euro-area IP', r'România: IP, comerț cu amănuntul, construcții, șomaj, șase indicatori de încredere (@{rd.N} serii lunare); IP din zona euro') + ' & ' +
     T('Eurostat (sts\\_inpr\\_m, sts\\_trtu\\_m, sts\\_copr\\_m, une\\_rt\\_m, ei\\_bssi\\_m\\_r2)', 'Eurostat (sts\\_inpr\\_m, sts\\_trtu\\_m, sts\\_copr\\_m, une\\_rt\\_m, ei\\_bssi\\_m\\_r2)') + ' & nowcasting',
     T('Romanian real GDP, quarterly, seasonally and calendar adjusted', 'PIB-ul real al României, trimestrial, ajustat sezonier și cu numărul de zile lucrătoare') + ' & Eurostat (namq\\_10\\_gdp) & ' + T('target', 'variabila-țintă')],
    size='scriptsize') + items(
    T('All sources are public and need no account or key; FRED-MD codes: 1 level, 2 difference, 4 log, 5 log difference, 6 second log difference',
      'Toate sursele sînt publice și nu cer cont sau cheie; codurile FRED-MD: 1 nivel, 2 diferență, 4 logaritm, 5 diferența logaritmilor, 6 a doua diferență a logaritmilor'),
    T('October 2025: the US household survey and CPI were not collected (federal shutdown); the isolated missing month is interpolated',
      'Octombrie 2025: ancheta în gospodării și IPC din SUA nu au fost colectate (închiderea guvernului federal); luna lipsă izolată este interpolată')), 'footnotesize')

D.frame(T('Shrinkage was born in Minneapolis', 'Originea shrinkage-ului: Minneapolis'), two(
    ph('minneapolis', T('Federal Reserve Bank of Minneapolis, 2010', 'Federal Reserve Bank of Minneapolis, 2010'), h='0.34\\textheight'),
    items((T(r'Early 1980s: Litterman forecasts with Bayesian VARs at the Minneapolis Fed \refLit; the ``Minnesota prior\'\'', r'Începutul anilor 1980: Litterman realizează prognoze cu VAR bayesiene la Fed Minneapolis \refLit; distribuția a priori „Minnesota”'),
           [T(r'\refDLS: sum-of-coefficients and conditional projections; \refSims, \refSZ: dummy initial observations', r'\refDLS: suma coeficienților și proiecții condiționate; \refSims, \refSZ: observația inițială fictivă')]),
          T(r'1989--2002: dynamic factor indexes \refSWd, generalised dynamic factors \refFHLR, diffusion indexes \refSWa', r'1989--2002: indici factoriali dinamici \refSWd, factori dinamici generalizați \refFHLR, indici de difuziune \refSWa'),
          T(r'2005--2015: FAVAR \refBBE, nowcasting \refGRS, large BVARs \refBGR, hierarchical priors \refGLP', r'2005--2015: FAVAR \refBBE, nowcasting \refGRS, BVAR mari \refBGR, distribuții a priori ierarhice \refGLP'),
          T('One idea throughout: when parameters outnumber observations, add information (a prior) or reduce dimension (factors)', 'O singură idee: cînd parametrii depășesc observațiile, adăugăm informație (o distribuție a priori) sau reducem dimensiunea (factori)')), '0.40', '0.58'), 'footnotesize')

# =============================================================================
# 1. BLESTEMUL DIMENSIONALITĂȚII
# =============================================================================
D.section('The curse of dimensionality', 'Blestemul dimensionalității')

D.frame(T('Counting parameters', 'Numărarea parametrilor'), items(
    (T(r'VAR($p$) in $n$ variables: $k = np + 1$ regressors per equation, $n k$ slope coefficients and $n(n + 1)/2$ covariances', r'VAR($p$) cu $n$ variabile: $k = np + 1$ regresori pe ecuație, $nk$ coeficienți și $n(n + 1)/2$ covarianțe'),
     [T(r'$n = 3$, $p = 13$: $k = 40$; $n = 20$: $k = 261$; $n = @{bg.nl}$: $k = @{bg.kl}$ per equation', r'$n = 3$, $p = 13$: $k = 40$; $n = 20$: $k = 261$; $n = @{bg.nl}$: $k = @{bg.kl}$ pe ecuație'),
      T(r'a 10-year window has $T = 120$ months: with $k > T$, OLS does not exist ($X\'X$ is singular)', r'o fereastră de 10 ani are $T = 120$ de luni: cu $k > T$, OLS nu există ($X\'X$ este singulară)')]),
    (T(r'Even with $k < T$, the estimation error grows with $k/T$: one-step MSE $\approx \sigma^2(1 + k/T)$ for a correctly specified regression', r'Chiar cu $k < T$, eroarea de estimare crește cu $k/T$: MSE la un pas $\approx \sigma^2(1 + k/T)$ pentru o regresie corect specificată'),
     [T('overfitting: in-sample fit improves, out-of-sample accuracy deteriorates', 'supraajustare: potrivirea în eșantion se îmbunătățește, acuratețea în afara eșantionului se deteriorează')]),
    (T('Three remedies', 'Trei remedii'),
     [T('shrinkage: Bayesian priors, ridge, LASSO', 'shrinkage: distribuții a priori bayesiene, ridge, LASSO'),
      T('dimension reduction: factors; variable selection', 'reducerea dimensiunii: factori; selecția variabilelor')])), 'small')

chart(T('Simulation: OLS VAR against a Minnesota BVAR', 'Simulare: VAR estimat prin OLS comparat cu un BVAR Minnesota'), 'ats_ch5_curse', 'ATS_ch5_bvar', [
    T(r'True model: stationary VAR(1) $A = 0.5I + (0.3/n)\mathbf{1}\mathbf{1}\'$ ($\mathbf{1}$: a vector of ones); estimated VAR(4), $T = 120$; one-step MSE of variable 1 relative to the true model; @{cu.reps} replications',
      r'Modelul adevărat: VAR(1) staționar $A = 0.5I + (0.3/n)\mathbf{1}\mathbf{1}\'$ ($\mathbf{1}$: vectorul de unu); se estimează un VAR(4), $T = 120$; MSE la un pas al variabilei 1 raportat la modelul adevărat; @{cu.reps} de replicări')],
    h='0.65\\textheight')

interp(('the simulation', 'simulării'), [
    T(r'OLS: the relative MSE climbs to @{cu.ols24} at $n = 24$ ($k = @{cu.k24}$ regressors for 116 observations)', r'OLS: MSE relativ urcă la @{cu.ols24} pentru $n = 24$ ($k = @{cu.k24}$ de regresori pentru 116 observații)'),
    T(r'BVAR: @{cu.bv24} at $n = 24$; the tightness chosen by the marginal likelihood falls from @{cu.lam2} ($n = 2$) to @{cu.lam24} ($n = 24$)', r'BVAR: @{cu.bv24} pentru $n = 24$; gradul de strîngere ales prin verosimilitatea marginală scade de la @{cu.lam2} ($n = 2$) la @{cu.lam24} ($n = 24$)'),
    T(r'A univariate AR(4) stays near @{cu.ar24}: the cross-variable information is real but small, and OLS spends it on noise', r'Un AR(4) univariat rămîne în jurul valorii @{cu.ar24}: informația dintre variabile există, dar este mică, iar OLS o irosește pe zgomot'),
    T('The larger the system, the tighter the prior should be: the theme of the whole chapter \\refDGRa', 'Cu cît sistemul este mai mare, cu atît distribuția a priori trebuie să fie mai strînsă: tema întregului capitol \\refDGRa')])

D.recap(('The curse of dimensionality', 'blestemul dimensionalității'), [
    T('Parameters grow with $n^2p$; observations do not', 'Parametrii cresc cu $n^2p$; observațiile nu'),
    T('Shrinkage trades a small bias for a large reduction of variance', 'Shrinkage-ul acceptă o deplasare mică în schimbul unei reduceri mari a varianței'),
    T('Factors summarise many series by a few common components', 'Factorii rezumă multe serii prin cîteva componente comune')])

# =============================================================================
# 2. INFERENȚA BAYESIANĂ
# =============================================================================
D.section('Bayesian inference: what we need', 'Inferența bayesiană: noțiunile necesare')

D.frame(T('Prior, likelihood, posterior', 'Distribuția a priori, verosimilitatea, distribuția a posteriori'), two(
    ph('laplace', T('Pierre-Simon Laplace, who developed inverse probability', 'Pierre-Simon Laplace, care a dezvoltat probabilitatea inversă'), h='0.36\\textheight'),
    items((T(r'Bayes: $p(\theta\mid y) = p(y\mid\theta)p(\theta)/p(y)$, with $p(y) = \int p(y\mid\theta)p(\theta)\,d\theta$', r'Bayes: $p(\theta\mid y) = p(y\mid\theta)p(\theta)/p(y)$, cu $p(y) = \int p(y\mid\theta)p(\theta)\,d\theta$'),
           [T(r'$\theta$: the parameters; $y$: the data; $p(\theta)$: \textbf{prior}; $p(y\mid\theta)$: likelihood; $p(\theta\mid y)$: \textbf{posterior}', r'$\theta$: parametrii; $y$: datele; $p(\theta)$: distribuția \textbf{a priori}; $p(y\mid\theta)$: verosimilitatea; $p(\theta\mid y)$: distribuția \textbf{a posteriori}'),
            T(r'$p(y)$: \textbf{marginal likelihood}, the evidence for the model and its prior', r'$p(y)$: \textbf{verosimilitatea marginală}, evidența în favoarea modelului și a distribuției a priori')]),
          (T('Conjugacy: prior and posterior in the same family, so the posterior has a closed form', 'Conjugarea: distribuția a priori și cea a posteriori sînt din aceeași familie, deci cea a posteriori are formă închisă'),
           [T('Normal mean with known variance: Normal; regression coefficients and variance: Normal--inverse-gamma', 'media distribuției Normale cu varianța cunoscută: Normală; coeficienți și varianță în regresie: Normal--inverse-gamma')]),
          T('Point summaries: posterior mean (quadratic loss), median (absolute loss); credible sets from posterior quantiles', 'Rezumate punctuale: media a posteriori (pierdere pătratică), mediana (pierdere absolută); mulțimi credibile din cuantilele a posteriori')), '0.34', '0.64'), 'footnotesize')

D.frame(T('The Normal update is a precision-weighted average (1/2)', 'Actualizarea Normală este o medie ponderată cu precizii (1/2)'), items(
    (T(r'Data: $\hat\beta\mid\beta \sim N(\beta, s^2)$ with $s^2 = \sigma^2/\sum x_t^2$; prior: $\beta \sim N(m_0, v_0)$', r'Datele: $\hat\beta\mid\beta \sim N(\beta, s^2)$ cu $s^2 = \sigma^2/\sum x_t^2$; distribuția a priori: $\beta \sim N(m_0, v_0)$'),
     [T(r'$\hat\beta$: the OLS estimate of a slope $\beta$ on regressor $x_t$; $\sigma^2$: the error variance, taken as known; $s^2$: the sampling variance of $\hat\beta$', r'$\hat\beta$: estimația OLS a pantei $\beta$ pentru regresorul $x_t$; $\sigma^2$: varianța erorii, considerată cunoscută; $s^2$: varianța de eșantionare a lui $\hat\beta$'),
      T(r'$m_0$, $v_0$: the prior mean and variance; precision = 1/variance', r'$m_0$, $v_0$: media și varianța a priori; precizia = 1/varianța')]),
    (T(r'Complete the square in $\beta$: the posterior is Normal, $\beta\mid y \sim N(m_1, v_1)$', r'Completăm pătratul în $\beta$: distribuția a posteriori este Normală, $\beta\mid y \sim N(m_1, v_1)$'),
     [T(r'precisions add: $v_1^{-1} = v_0^{-1} + s^{-2}$', r'preciziile se adună: $v_1^{-1} = v_0^{-1} + s^{-2}$'),
      T(r'means average: $m_1 = w\,m_0 + (1 - w)\hat\beta$, with prior weight $w = v_0^{-1}/(v_0^{-1} + s^{-2}) \in (0, 1)$', r'mediile se mediază: $m_1 = w\,m_0 + (1 - w)\hat\beta$, cu ponderea distribuției a priori $w = v_0^{-1}/(v_0^{-1} + s^{-2}) \in (0, 1)$'),
      T(r'$w$ is large when the prior is tight ($v_0$ small) or the data are weak ($s^2$ large)', r'$w$ este mare cînd distribuția a priori este strînsă ($v_0$ mic) sau datele sînt puțin informative ($s^2$ mare)')])), 'small')

D.frame(T('The Normal update is a precision-weighted average (2/2)', 'Actualizarea Normală este o medie ponderată cu precizii (2/2)'), items(
    (T(r'In regression form: \[ \bar\beta = (V_0^{-1} + X\'X/\sigma^2)^{-1}(V_0^{-1}m_0 + X\'y/\sigma^2) \]', r'În forma de regresie: \[ \bar\beta = (V_0^{-1} + X\'X/\sigma^2)^{-1}(V_0^{-1}m_0 + X\'y/\sigma^2) \]'),
     [T(r'$y$ ($T\times 1$), $X$ ($T\times k$): the data; $m_0$, $V_0$: prior mean vector and covariance matrix; $\bar\beta$: the posterior mean', r'$y$ ($T\times 1$), $X$ ($T\times k$): datele; $m_0$, $V_0$: vectorul mediilor și matricea de covarianță a priori; $\bar\beta$: media a posteriori'),
      T(r'the same weighting: prior precision $V_0^{-1}$ plus data precision $X\'X/\sigma^2$', r'aceeași ponderare: precizia a priori $V_0^{-1}$ plus precizia datelor $X\'X/\sigma^2$')]),
    (T(r'With $m_0 = 0$ and $V_0 = \tau^2I$ this is ridge regression with penalty $\sigma^2/\tau^2$', r'Cu $m_0 = 0$ și $V_0 = \tau^2I$ aceasta este regresia ridge cu penalizarea $\sigma^2/\tau^2$'),
     [T(r'$\tau^2$: the prior variance of every coefficient; a small $\tau^2$ shrinks more towards 0', r'$\tau^2$: varianța a priori a fiecărui coeficient; un $\tau^2$ mic strînge mai mult spre 0')]),
    T(r'As $T \to \infty$, $X\'X$ grows and the prior weight $w \to 0$: the prior matters in small samples and in large models', r'Cînd $T \to \infty$, $X\'X$ crește și ponderea distribuției a priori $w \to 0$: distribuția a priori contează în eșantioane mici și în modele mari'),
    T('Seminar 5, A1: the update by hand and the empirical-Bayes choice of $\\tau^2$', 'Seminarul 5, A1: actualizarea de mînă și alegerea bayesiană empirică a lui $\\tau^2$')), 'small')

chart(T('Updating an AR(1) coefficient', 'Actualizarea unui coeficient AR(1)'), 'ats_ch5_conjugate', 'ATS_ch5_bayes', [
    T(r'US unemployment rate, monthly, windows ending December 2019; prior $N(1, 0.2^2)$ (random walk), $\sigma^2$ at its OLS estimate',
      r'Rata șomajului din SUA, lunar, ferestre care se încheie în decembrie 2019; distribuția a priori $N(1, 0.2^2)$ (mers aleator), $\sigma^2$ la estimația OLS')],
    h='0.65\\textheight')

interp(('the update', 'actualizării'), [
    T(r'$T = 24$: OLS @{cj.T24.ols} (SE @{cj.T24.se}), posterior mean @{cj.T24.post} (sd @{cj.T24.post_sd}); the prior has weight @{cj.T24.w}\%',
      r'$T = 24$: OLS @{cj.T24.ols} (SE @{cj.T24.se}), media a posteriori @{cj.T24.post} (abaterea standard @{cj.T24.post_sd}); distribuția a priori are ponderea @{cj.T24.w}\%'),
    T(r'$T = 240$: OLS @{cj.T240.ols}, posterior @{cj.T240.post}; the prior weight falls to @{cj.T240.w}\%', r'$T = 240$: OLS @{cj.T240.ols}, a posteriori @{cj.T240.post}; ponderea distribuției a priori scade la @{cj.T240.w}\%'),
    T('In a VAR, each equation has hundreds of coefficients but the same $T$: the prior keeps the weight it has at $T = 24$ here', 'Într-un VAR, fiecare ecuație are sute de coeficienți, dar același $T$: distribuția a priori păstrează ponderea pe care o are aici la $T = 24$')])

D.frame(T('Marginal likelihood and Bayes factors', 'Verosimilitatea marginală și factorii Bayes'), items(
    (T(r'$p(y\mid M) = \int p(y\mid\theta, M)p(\theta\mid M)\,d\theta$: the density of the data \emph{before} seeing them', r'$p(y\mid M) = \int p(y\mid\theta, M)p(\theta\mid M)\,d\theta$: densitatea datelor \emph{înainte} de a le vedea'),
     [T(r'$M$: a model, i.e.\ a likelihood together with its prior; the integral averages the likelihood over the prior', r'$M$: un model, adică o verosimilitate împreună cu distribuția ei a priori; integrala mediază verosimilitatea după distribuția a priori'),
      T(r'prediction-error decomposition: $\ln p(y) = \sum_t \ln p(y_t\mid y_{1:t-1})$, a sum of one-step log scores (Chapter 1); $y_{1:t-1}$: the data up to $t - 1$', r'descompunerea erorilor de predicție: $\ln p(y) = \sum_t \ln p(y_t\mid y_{1:t-1})$, o sumă de scoruri logaritmice la un pas (Capitolul 1); $y_{1:t-1}$: datele pînă la $t - 1$'),
      T('it penalises complexity automatically: a diffuse prior spreads probability over data that never occur', 'penalizează automat complexitatea: o distribuție a priori difuză împrăștie probabilitatea pe date care nu apar')]),
    (T(r'Bayes factor $B_{12} = p(y\mid M_1)/p(y\mid M_2)$; $2\ln B_{12} > 6$ is ``strong\'\' evidence \refKR', r'Factorul Bayes $B_{12} = p(y\mid M_1)/p(y\mid M_2)$; $2\ln B_{12} > 6$ este o evidență „puternică” \refKR'),
     [T('sensitive to the prior: with an improper prior it is not defined', 'este sensibil la distribuția a priori: cu o distribuție a priori improprie nu este definit')]),
    T(r'Hierarchical use: treat the hyperparameters $\gamma$ of the prior as parameters and maximise $p(y\mid\gamma)$ (empirical Bayes) or put a hyperprior on them \refGLP', r'Folosirea ierarhică: tratăm hiperparametrii $\gamma$ ai distribuției a priori ca parametri și maximizăm $p(y\mid\gamma)$ (Bayes empiric) sau le dăm o distribuție a priori \refGLP')), 'small')

D.frame(T('Gibbs sampling (1/2)', 'Eșantionarea Gibbs (1/2)'), items(
    (T(r'Use: the joint posterior has no closed form, but each \textbf{full conditional} has one \refGG, \refGS', r'Utilizarea: distribuția a posteriori comună nu are formă închisă, dar fiecare \textbf{distribuție condiționată completă} are \refGG, \refGS'),
     [T(r'draw $\theta_1\mid\theta_2, y$, then $\theta_2\mid\theta_1, y$, and repeat', r'extragem $\theta_1\mid\theta_2, y$, apoi $\theta_2\mid\theta_1, y$ și repetăm'),
      T(r'$\theta_1$, $\theta_2$: two blocks of parameters; full conditional: the distribution of one block given the other and the data', r'$\theta_1$, $\theta_2$: două blocuri de parametri; distribuția condiționată completă: distribuția unui bloc dat fiind celălalt și datele'),
      T('the draws form a Markov chain whose stationary distribution is the posterior', 'extragerile formează un lanț Markov a cărui distribuție staționară este cea a posteriori'),
      T('discard a burn-in, then average functions of the draws (ergodic theorem)', 'eliminăm o perioadă inițială (burn-in), apoi mediem funcții ale extragerilor (teorema ergodică)')]),
    T('In VARs: stochastic volatility, non-conjugate priors and set-identified SVARs (Chapter 3) need Gibbs or Metropolis--Hastings steps', 'În VAR: volatilitatea stochastică, distribuțiile a priori neconjugate și SVAR identificate pe mulțimi (Capitolul 3) cer pași Gibbs sau Metropolis--Hastings')), 'small')

D.frame(T('Gibbs sampling (2/2): the linear regression', 'Eșantionarea Gibbs (2/2): regresia liniară'), items(
    (T(r'Regression $y = X\beta + e$ with independent priors $\beta \sim N(b_0, V_0)$, $\sigma^2 \sim IG(a_0, d_0)$', r'Regresia $y = X\beta + e$ cu distribuții a priori independente $\beta \sim N(b_0, V_0)$, $\sigma^2 \sim IG(a_0, d_0)$'),
     [T(r'$b_0$, $V_0$: prior mean and covariance of $\beta$; $IG(a_0, d_0)$: inverse gamma with shape $a_0$ and scale $d_0$', r'$b_0$, $V_0$: media și covarianța a priori ale lui $\beta$; $IG(a_0, d_0)$: distribuția inverse gamma cu parametrul de formă $a_0$ și de scală $d_0$')]),
    (T(r'Step 1, the coefficients given the variance: $\beta\mid\sigma^2, y \sim N(\bar b, \bar V)$', r'Pasul 1, coeficienții dată fiind varianța: $\beta\mid\sigma^2, y \sim N(\bar b, \bar V)$'),
     [T(r'$\bar V = (V_0^{-1} + X\'X/\sigma^2)^{-1}$, $\bar b = \bar V(V_0^{-1}b_0 + X\'y/\sigma^2)$: the Normal update of the previous slides', r'$\bar V = (V_0^{-1} + X\'X/\sigma^2)^{-1}$, $\bar b = \bar V(V_0^{-1}b_0 + X\'y/\sigma^2)$: actualizarea Normală de pe slide-urile anterioare')]),
    (T(r'Step 2, the variance given the coefficients: $\sigma^2\mid\beta, y \sim IG(a_0 + T/2,\ d_0 + e\'e/2)$', r'Pasul 2, varianța dați fiind coeficienții: $\sigma^2\mid\beta, y \sim IG(a_0 + T/2,\ d_0 + e\'e/2)$'),
     [T(r'$e = y - X\beta$: the residuals at the current draw of $\beta$; the data add $T/2$ to the shape and half the residual sum of squares to the scale', r'$e = y - X\beta$: reziduurile la extragerea curentă a lui $\beta$; datele adaugă $T/2$ la parametrul de formă și jumătate din suma pătratelor reziduurilor la scală')])), 'small')

D.frame(T('MCMC diagnostics (1/2)', 'Diagnosticarea MCMC (1/2)'), items(
    (T(r'\textbf{Effective sample size}: $\mathrm{ESS} = M/(1 + 2\sum_{k\ge1}\rho_k)$: the number of independent draws with the same precision', r'\textbf{Mărimea efectivă a eșantionului}: $\mathrm{ESS} = M/(1 + 2\sum_{k\ge1}\rho_k)$: numărul de extrageri independente cu aceeași precizie'),
     [T(r'$M$: the number of draws kept; $\rho_k$: the autocorrelation of the draws at lag $k$', r'$M$: numărul de extrageri păstrate; $\rho_k$: autocorelația extragerilor la lagul $k$'),
      T(r'AR(1)-type chain: $\mathrm{ESS} = M(1 - \rho)/(1 + \rho)$; $\rho = 0.9$ keeps about 5\% of the draws', r'lanț de tip AR(1): $\mathrm{ESS} = M(1 - \rho)/(1 + \rho)$; $\rho = 0.9$ păstrează aproximativ 5\% din extrageri')]),
    (T(r'\textbf{$\widehat R$} \refGR: several chains from dispersed starts; $\widehat R = \sqrt{\hat V/W}$, $\hat V = \frac{n-1}{n}W + B/n$', r'\textbf{$\widehat R$} \refGR: mai multe lanțuri din puncte de pornire dispersate; $\widehat R = \sqrt{\hat V/W}$, $\hat V = \frac{n-1}{n}W + B/n$'),
     [T(r'$n$: draws per chain; $W$: within-chain variance; $B$: $n\times$ the variance of the chain means; $\hat V$: the pooled variance estimate', r'$n$: numărul de extrageri pe lanț; $W$: varianța în interiorul lanțurilor; $B$: $n\times$ varianța mediilor lanțurilor; $\hat V$: estimația comună a varianței'),
      T(r'$\widehat R \approx 1$: the chains agree', r'$\widehat R \approx 1$: lanțurile sînt de acord')])), 'small')

D.frame(T('MCMC diagnostics (2/2)', 'Diagnosticarea MCMC (2/2)'), items(
    (T(r'$\widehat R$ in current practice \refVGS', r'$\widehat R$ în practica actuală \refVGS'),
     [T(r'rank-normalised, split chains; require $\widehat R < 1.01$', r'cu ranguri normalizate și lanțuri divizate; cerem $\widehat R < 1{,}01$')]),
    (T(r'\textbf{Geweke} $z$: $z = (\bar\theta_A - \bar\theta_B)/\sqrt{\hat S_A(0)/n_A + \hat S_B(0)/n_B}$', r'Statistica \textbf{Geweke}: $z = (\bar\theta_A - \bar\theta_B)/\sqrt{\hat S_A(0)/n_A + \hat S_B(0)/n_B}$'),
     [T(r'$\bar\theta_A$, $\bar\theta_B$: the means of the first 10\% and of the last 50\% of a chain; $n_A$, $n_B$: their lengths', r'$\bar\theta_A$, $\bar\theta_B$: mediile primelor 10\% și ale ultimelor 50\% din lanț; $n_A$, $n_B$: lungimile lor'),
      T(r'$\hat S(0)$: the spectral density at frequency zero, which accounts for autocorrelation', r'$\hat S(0)$: densitatea spectrală la frecvența zero, care ține cont de autocorelare'),
      T(r'$z \approx N(0, 1)$ after convergence; $|z| > 2$ signals non-convergence', r'$z \approx N(0, 1)$ după convergență; $|z| > 2$ semnalează lipsa convergenței')]),
    T('None of the three proves convergence; each can reveal a failure', 'Niciuna dintre cele trei nu demonstrează convergența; fiecare poate dezvălui un eșec')), 'small')

chart(T('Gibbs sampling: a bad and a good parametrisation', 'Eșantionarea Gibbs: o parametrizare ineficientă și una eficientă'), 'ats_ch5_gibbs', 'ATS_ch5_bayes', [
    T(r'Monthly US IP growth on lagged capacity utilisation (mean @{gb.xm}\%, sd @{gb.xs}), 1967--2019, $T = @{gb.T}$; one-at-a-time Gibbs, four chains, 4\,000 draws, burn-in 1\,000',
      r'Creșterea lunară a IP din SUA pe gradul de utilizare a capacităților cu lag (media @{gb.xm}\%, abaterea standard @{gb.xs}), 1967--2019, $T = @{gb.T}$; Gibbs pe cîte un parametru, patru lanțuri, 4\,000 de extrageri, burn-in 1\,000')],
    h='0.65\\textheight')

interp(('the two samplers', 'celor două eșantionatoare'), [
    (T(r'Raw regressor: the posterior correlation of intercept and slope is @{gb.raw.corr}, so each conditional step moves very little', r'Regresorul brut: corelația a posteriori dintre termenul liber și pantă este @{gb.raw.corr}, deci fiecare pas condiționat se mișcă foarte puțin'),
     [T(r'lag-1 autocorrelation @{gb.raw.acf1}; ESS = @{gb.raw.ess} out of @{gb.n} draws; $\widehat R$ = @{gb.raw.rhat}; Geweke $z$ = @{gb.raw.gw}', r'autocorelația de ordinul 1 @{gb.raw.acf1}; ESS = @{gb.raw.ess} din @{gb.n} de extrageri; $\widehat R$ = @{gb.raw.rhat}; $z$ Geweke = @{gb.raw.gw}')]),
    (T(r'Centred regressor: correlation @{gb.centred.corr}, ESS = @{gb.centred.ess}, $\widehat R$ = @{gb.centred.rhat}, Geweke $z$ = @{gb.centred.gw}', r'Regresorul centrat: corelația @{gb.centred.corr}, ESS = @{gb.centred.ess}, $\widehat R$ = @{gb.centred.rhat}, $z$ Geweke = @{gb.centred.gw}'),
     [T(r'same model, same posterior of the slope (mean @{gb.centred.mean}); only the sampler changed', r'același model, aceeași distribuție a posteriori a pantei (media @{gb.centred.mean}); s-a schimbat doar eșantionatorul')]),
    T('Lesson: reparametrise or draw correlated blocks jointly; conjugate BVARs avoid the problem by drawing $B$ in one block', 'Lecția: reparametrizați sau extrageți împreună blocurile corelate; BVAR-urile conjugate evită problema extrăgînd $B$ într-un singur bloc')])

D.recap(('Bayesian inference', 'inferența bayesiană'), [
    T('Posterior precision = prior precision + data precision; the mean is a weighted average', 'Precizia a posteriori = precizia a priori + precizia datelor; media este o medie ponderată'),
    T('The marginal likelihood scores a model with its prior and can choose hyperparameters', 'Verosimilitatea marginală evaluează un model împreună cu distribuția lui a priori și poate alege hiperparametri'),
    T('Gibbs sampling needs full conditionals; check ESS, $\\widehat R$ and Geweke before trusting the draws', 'Eșantionarea Gibbs cere distribuțiile condiționate complete; verificați ESS, $\\widehat R$ și Geweke înainte de a avea încredere în extrageri')])

# =============================================================================
# 3. MINNESOTA ȘI NIW
# =============================================================================
D.section('The Minnesota prior and its conjugate form', 'Distribuția a priori Minnesota și forma ei conjugată')

D.frame(T('The Minnesota prior', 'Distribuția a priori Minnesota'), items(
    (T(r'VAR($p$): $y_t = c + A_1y_{t-1} + \dots + A_py_{t-p} + u_t$; $(A_l)_{ij}$: the effect of variable $j$ at lag $l$ on variable $i$', r'VAR($p$): $y_t = c + A_1y_{t-1} + \dots + A_py_{t-p} + u_t$; $(A_l)_{ij}$: efectul variabilei $j$ cu lagul $l$ asupra variabilei $i$'),
     [T(r'prior means \refLit: $\E[(A_1)_{ii}] = \delta_i$, all other coefficients 0; $\delta_i = 1$ (random walk) for persistent series, 0 (white noise) otherwise', r'mediile a priori \refLit: $\E[(A_1)_{ii}] = \delta_i$, toți ceilalți coeficienți 0; $\delta_i = 1$ (mers aleator) pentru serii persistente, 0 (zgomot alb) în rest'),
      T(r'prior variances \refBGR, eq.~(2): $\Var[(A_l)_{ij}] = \lambda^2/l^2$ if $j = i$, $\vartheta\lambda^2\sigma_i^2/(l^2\sigma_j^2)$ if $j \ne i$', r'varianțele a priori \refBGR, ec.~(2): $\Var[(A_l)_{ij}] = \lambda^2/l^2$ dacă $j = i$, $\vartheta\lambda^2\sigma_i^2/(l^2\sigma_j^2)$ dacă $j \ne i$')]),
    (T('Hyperparameters', 'Hiperparametrii'),
     [T(r'$\lambda$: overall tightness; $1/l^2$: the decay with the lag; $\vartheta \in (0, 1]$: cross-variable shrinkage', r'$\lambda$: gradul general de strîngere; $1/l^2$: descreșterea cu lagul; $\vartheta \in (0, 1]$: shrinkage-ul între variabile'),
      T(r'$\sigma_i^2$: residual variance of a univariate AR for $y_i$, so that $\sigma_i^2/\sigma_j^2$ fixes units', r'$\sigma_i^2$: varianța reziduală a unui AR univariat pentru $y_i$, astfel încît $\sigma_i^2/\sigma_j^2$ fixează unitățile de măsură'),
      T(r'$\lambda = 0$: posterior = prior; $\lambda \to \infty$: posterior mean = OLS', r'$\lambda = 0$: a posteriori = a priori; $\lambda \to \infty$: media a posteriori = OLS')]),
    T('Original version: $\\Sigma$ diagonal and fixed, each equation a separate ridge-type regression with a diffuse constant', 'Versiunea originală: $\\Sigma$ diagonală și fixă, fiecare ecuație o regresie separată de tip ridge, cu termen liber difuz')), 'small')

D.frame(T('The natural conjugate prior (1/2)', 'Distribuția a priori natural conjugată (1/2)'), items(
    (T(r'The VAR as a multivariate regression $Y = XB + U$, rows of $U$ i.i.d.\ $N(0, \Sigma)$', r'VAR-ul ca regresie multivariată $Y = XB + U$, liniile lui $U$ i.i.d.\ $N(0, \Sigma)$'),
     [T(r'$Y$ ($T\times n$): the observations; $X$ ($T\times k$): constant and $p$ lags; $B$ ($k\times n$): the coefficients, one column per equation', r'$Y$ ($T\times n$): observațiile; $X$ ($T\times k$): constanta și cele $p$ laguri; $B$ ($k\times n$): coeficienții, cîte o coloană pentru fiecare ecuație')]),
    (T(r'Prior \refKK: $\mathrm{vec}(B)\mid\Sigma \sim N(\mathrm{vec}(B_0), \Sigma\otimes\Omega_0)$, $\Sigma \sim IW(\Psi, d)$', r'Distribuția a priori \refKK: $\mathrm{vec}(B)\mid\Sigma \sim N(\mathrm{vec}(B_0), \Sigma\otimes\Omega_0)$, $\Sigma \sim IW(\Psi, d)$'),
     [T(r'$\mathrm{vec}$: stacks the columns; $\otimes$: Kronecker product; $B_0$: prior mean; $\Omega_0$ ($k\times k$): prior covariance across regressors', r'$\mathrm{vec}$: așază coloanele una sub alta; $\otimes$: produsul Kronecker; $B_0$: media a priori; $\Omega_0$ ($k\times k$): covarianța a priori între regresori'),
      T(r'$IW(\Psi, d)$: inverse Wishart with scale matrix $\Psi$ and $d$ degrees of freedom', r'$IW(\Psi, d)$: distribuția inverse Wishart cu matricea de scală $\Psi$ și $d$ grade de libertate')]),
    (T('Posterior: the same families, with updated parameters (derivation: Appendix)  % applink: natural conjugate posterior', 'Distribuția a posteriori: aceleași familii, cu parametri actualizați (derivarea: Anexa)  % applink: posteriori natural conjugată'),
     [T(r'$\bar\Omega^{-1} = \Omega_0^{-1} + X\'X$, $\bar B = \bar\Omega(\Omega_0^{-1}B_0 + X\'Y)$: the precision-weighted average again', r'$\bar\Omega^{-1} = \Omega_0^{-1} + X\'X$, $\bar B = \bar\Omega(\Omega_0^{-1}B_0 + X\'Y)$: din nou media ponderată cu precizii'),
      T(r'$\Sigma\mid Y \sim IW(\bar\Psi, T + d)$, $\bar\Psi = \Psi + \hat U\'\hat U + (\bar B - B_0)\'\Omega_0^{-1}(\bar B - B_0)$, $\hat U = Y - X\bar B$', r'$\Sigma\mid Y \sim IW(\bar\Psi, T + d)$, $\bar\Psi = \Psi + \hat U\'\hat U + (\bar B - B_0)\'\Omega_0^{-1}(\bar B - B_0)$, $\hat U = Y - X\bar B$')])), 'small')

D.frame(T('The natural conjugate prior (2/2)', 'Distribuția a priori natural conjugată (2/2)'), items(
    (T(r'Price of conjugacy: the Kronecker structure gives every equation the same $\Omega_0$, so $\vartheta = 1$', r'Prețul conjugării: structura Kronecker dă fiecărei ecuații același $\Omega_0$, deci $\vartheta = 1$'),
     [T(r'Minnesota moments with $\Omega_0 = \mathrm{diag}(\lambda^2/(l^2\sigma_j^2))$ and $\E\Sigma = \mathrm{diag}(\sigma_i^2)$ ($d = n + 2$, $\Psi = \mathrm{diag}(\sigma_i^2)$)', r'momentele Minnesota cu $\Omega_0 = \mathrm{diag}(\lambda^2/(l^2\sigma_j^2))$ și $\E\Sigma = \mathrm{diag}(\sigma_i^2)$ ($d = n + 2$, $\Psi = \mathrm{diag}(\sigma_i^2)$)')]),
    T(r'Gain: one $k\times k$ inversion for all equations; exact draws without MCMC; a closed-form marginal likelihood (Appendix)  % applink: marginal likelihood in closed form', r'Cîștigul: o singură inversare $k\times k$ pentru toate ecuațiile; extrageri exacte fără MCMC; verosimilitatea marginală în formă închisă (Anexa)  % applink: verosimilitatea marginală în formă închisă')), 'small')

D.frame(T('Dummy observations (1/2)', 'Observații fictive (1/2)'), items(
    (T('Theil mixed estimation', 'Estimarea mixtă Theil'),
     [T(r'add $T_d$ artificial rows $(Y_d, X_d)$ and run OLS on $\binom{Y_d}{Y}$, $\binom{X_d}{X}$', r'adăugăm $T_d$ linii artificiale $(Y_d, X_d)$ și aplicăm OLS pe $\binom{Y_d}{Y}$, $\binom{X_d}{X}$'),
      T('each row states a prior belief as if it were data', 'fiecare linie exprimă o convingere a priori ca și cum ar fi date'),
      T(r'equivalent to the NIW prior with $B_0 = (X_d\'X_d)^{-1}X_d\'Y_d$, $\Omega_0 = (X_d\'X_d)^{-1}$ \refBGR, eq.~(5)', r'echivalent cu distribuția a priori NIW cu $B_0 = (X_d\'X_d)^{-1}X_d\'Y_d$, $\Omega_0 = (X_d\'X_d)^{-1}$ \refBGR, ec.~(5)'),
      T(r'Minnesota block: $Y_d = \mathrm{diag}(\delta_i\sigma_i)/\lambda$, $X_d = J_p\otimes\mathrm{diag}(\sigma_i)/\lambda$, $J_p = \mathrm{diag}(1, \dots, p)$', r'blocul Minnesota: $Y_d = \mathrm{diag}(\delta_i\sigma_i)/\lambda$, $X_d = J_p\otimes\mathrm{diag}(\sigma_i)/\lambda$, $J_p = \mathrm{diag}(1, \dots, p)$')])), 'small')

D.frame(T('Dummy observations (2/2)', 'Observații fictive (2/2)'), items(
    (T(r'\textbf{Sum of coefficients} \refDLS: $Y_d = \mathrm{diag}(\bar y_i)/\mu$, $X_d = (\mathbf{1}_p\'\otimes\mathrm{diag}(\bar y_i)/\mu,\ 0)$', r'\textbf{Suma coeficienților} \refDLS: $Y_d = \mathrm{diag}(\bar y_i)/\mu$, $X_d = (\mathbf{1}_p\'\otimes\mathrm{diag}(\bar y_i)/\mu,\ 0)$'),
     [T(r'$\bar y_i$: the mean of the first $p$ observations of $y_i$; $\mathbf{1}_p$: a vector of $p$ ones; $\mu > 0$: the tightness of this prior', r'$\bar y_i$: media primelor $p$ observații ale lui $y_i$; $\mathbf{1}_p$: un vector de $p$ unități; $\mu > 0$: gradul de strîngere al acestei distribuții'),
      T(r'shrinks $\Pi = I - \sum_l A_l$ to 0 (``inexact differencing\'\'): $\mu \to 0$ gives a VAR in differences without cointegration', r'strînge $\Pi = I - \sum_l A_l$ spre 0 („diferențiere inexactă”): $\mu \to 0$ dă un VAR în diferențe, fără cointegrare')]),
    (T(r'\textbf{Dummy initial observation} \refSims, \refSZ: one row $y = \bar y\'/\phi$, $x = (\bar y\'/\phi, \dots, \bar y\'/\phi, 1/\phi)$', r'\textbf{Observația inițială fictivă} \refSims, \refSZ: o linie $y = \bar y\'/\phi$, $x = (\bar y\'/\phi, \dots, \bar y\'/\phi, 1/\phi)$'),
     [T('$\\bar y$: the vector of the $\\bar y_i$; $\\phi > 0$: its tightness', '$\\bar y$: vectorul valorilor $\\bar y_i$; $\\phi > 0$: gradul de strîngere'),
      T('pushes towards unit roots \\emph{or} towards a stationary model whose mean is $\\bar y$', 'împinge spre rădăcini unitare \\emph{sau} spre un model staționar cu media $\\bar y$'),
      T('so it allows cointegration (Chapter 4)', 'permite deci cointegrarea (Capitolul 4)')])), 'small')

chart(T('How much shrinkage? In-sample fit against out-of-sample accuracy', 'Cît shrinkage? Potrivirea în eșantion comparată cu acuratețea în afara eșantionului'), 'ats_ch5_tradeoff', 'ATS_ch5_large_bvar', [
    T(r'MEDIUM system (20 variables, $p = 13$, $k = @{tr.k}$), BGR prior, rolling 10-year windows; out-of-sample: one-step MSFE of employment, CPI and the funds rate, 1971--2003, relative to a random walk',
      r'Sistemul MEDIUM (20 de variabile, $p = 13$, $k = @{tr.k}$), distribuția a priori BGR, ferestre mobile de 10 ani; în afara eșantionului: MSFE la un pas pentru ocupare, IPC și dobînda federal funds, 1971--2003, relativ la mersul aleator')],
    h='0.65\\textheight')

interp(('the trade-off', 'compromisului'), [
    T(r'The in-sample fit improves without limit as $\lambda$ grows: with $k = @{tr.k}$ and $T = 120$, a loose prior interpolates the data', r'Potrivirea în eșantion se îmbunătățește fără limită cînd $\lambda$ crește: cu $k = @{tr.k}$ și $T = 120$, o distribuție a priori largă interpolează datele'),
    T(r'Out of sample: U-shape; minimum @{tr.bestoos} at $\lambda = @{tr.best}$; @{tr.tight} with $\lambda = 0.005$ (almost the random walk); @{tr.loose} with $\lambda = 20$', r'În afara eșantionului: formă de U; minimul @{tr.bestoos} la $\lambda = @{tr.best}$; @{tr.tight} cu $\lambda = 0{,}005$ (aproape mersul aleator); @{tr.loose} cu $\lambda = 20$'),
    T('The shrinkage must be chosen without looking at the evaluation sample: by a fit rule (BGR) or by the marginal likelihood (GLP)', 'Shrinkage-ul trebuie ales fără a privi eșantionul de evaluare: printr-o regulă de potrivire (BGR) sau prin verosimilitatea marginală (GLP)')])

D.recap(('Minnesota and NIW priors', 'distribuțiile a priori Minnesota și NIW'), [
    T('Minnesota: centre each equation on a random walk or white noise; shrink distant lags and other variables more', 'Minnesota: centrăm fiecare ecuație pe un mers aleator sau pe zgomot alb; strîngem mai mult lagurile îndepărtate și celelalte variabile'),
    T('The natural conjugate form keeps closed forms at the cost of $\\vartheta = 1$', 'Forma natural conjugată păstrează formulele închise cu prețul $\\vartheta = 1$'),
    T('Dummy observations implement the prior by OLS and add sum-of-coefficients and initial-observation beliefs', 'Observațiile fictive implementează distribuția a priori prin OLS și adaugă convingeri despre suma coeficienților și observația inițială')])

# =============================================================================
# 4. GLP
# =============================================================================
D.section('Choosing the shrinkage: hierarchical priors', 'Alegerea shrinkage-ului: distribuții a priori ierarhice')

D.frame(T('Giannone, Lenza and Primiceri (2015)', 'Giannone, Lenza și Primiceri (2015)'), items(
    (T(r'Treat $\gamma = (\lambda, \mu, \phi)$ as parameters with hyperpriors: $p(\gamma\mid y) \propto p(y\mid\gamma)p(\gamma)$ \refGLP', r'Tratăm $\gamma = (\lambda, \mu, \phi)$ ca parametri cu distribuții a priori proprii: $p(\gamma\mid y) \propto p(y\mid\gamma)p(\gamma)$ \refGLP'),
     [T(r'$p(y\mid\gamma)$ is known in closed form for the NIW prior with dummies: data plus dummies, minus dummies alone', r'$p(y\mid\gamma)$ este cunoscută în formă închisă pentru distribuția NIW cu observații fictive: datele plus observațiile fictive, minus observațiile fictive singure'),
      T(r'hyperpriors: Gamma with mode 0.2 and sd 0.4 for $\lambda$, mode 1 and sd 1 for $\mu$ and $\phi$', r'distribuții a priori pentru hiperparametri: Gamma cu modul 0,2 și abaterea standard 0,4 pentru $\lambda$, modul 1 și abaterea standard 1 pentru $\mu$ și $\phi$')]),
    (T('Interpretation: the marginal likelihood is an out-of-sample score of one-step predictive densities (previous section)', 'Interpretare: verosimilitatea marginală este un scor în afara eșantionului al densităților predictive la un pas (secțiunea anterioară)'),
     [T('so it trades fit against complexity without an evaluation sample', 'deci echilibrează potrivirea și complexitatea fără un eșantion de evaluare')]),
    T(r'Use the posterior mode of $\gamma$ (as here) or integrate $\gamma$ out by Metropolis--Hastings; GLP find both forecast about as well as factor models', r'Folosim modul a posteriori al lui $\gamma$ (ca aici) sau integrăm $\gamma$ prin Metropolis--Hastings; GLP constată că ambele prognozează cam la fel de bine ca modelele factoriale')), 'small')

chart(T('The marginal likelihood as a function of the tightness', 'Verosimilitatea marginală în funcție de gradul de strîngere'), 'ats_ch5_lambda', 'ATS_ch5_large_bvar', [
    T(r'SMALL ($n = 3$), MEDIUM ($n = 20$), LARGE ($n = @{lb.LARGE.n}$), $p = 13$, 1960:1--2019:12 ($T = @{lb.T}$); $\mu = \phi = 1$; log ML minus its maximum, divided by $nT$',
      r'SMALL ($n = 3$), MEDIUM ($n = 20$), LARGE ($n = @{lb.LARGE.n}$), $p = 13$, 1960:1--2019:12 ($T = @{lb.T}$); $\mu = \phi = 1$; log ML minus maximul, împărțit la $nT$')],
    h='0.65\\textheight')

interp(('the marginal likelihood', 'verosimilității marginale'), [
    T(r'Optimal tightness: @{lb.SMALL} (SMALL), @{lb.MEDIUM} (MEDIUM), @{lb.LARGE} (LARGE): bigger systems need a tighter prior', r'Gradul optim de strîngere: @{lb.SMALL} (SMALL), @{lb.MEDIUM} (MEDIUM), @{lb.LARGE} (LARGE): sistemele mai mari cer o distribuție a priori mai strînsă'),
    T(r'Using the textbook value $\lambda = 0.2$ costs @{lb.MEDIUM.l02} log points for MEDIUM and @{lb.LARGE.l02} for LARGE; $\lambda = 1$ costs @{lb.LARGE.l1} for LARGE', r'Valoarea din manuale $\lambda = 0{,}2$ costă @{lb.MEDIUM.l02} puncte logaritmice pentru MEDIUM și @{lb.LARGE.l02} pentru LARGE; $\lambda = 1$ costă @{lb.LARGE.l1} pentru LARGE'),
    T(r'Joint mode with the hyperpriors: SMALL $\mu = @{lb.SMALL.mu}$, $\phi = @{lb.SMALL.phi}$; MEDIUM $\mu = @{lb.MEDIUM.mu}$, $\phi = @{lb.MEDIUM.phi}$: the data ask for tight sum-of-coefficients and initial-observation priors', r'Modul comun cu distribuțiile hiperparametrilor: SMALL $\mu = @{lb.SMALL.mu}$, $\phi = @{lb.SMALL.phi}$; MEDIUM $\mu = @{lb.MEDIUM.mu}$, $\phi = @{lb.MEDIUM.phi}$: datele cer distribuții strînse pentru suma coeficienților și observația inițială')])

D.frame(T('Two rules for one hyperparameter (1/2)', 'Două reguli pentru un singur hiperparametru (1/2)'), items(
    (T(r'\textbf{BGR fit rule} \refBGR, Section~3', r'\textbf{Regula potrivirii BGR} \refBGR, secțiunea~3'),
     [T(r'choose $\lambda$ so that the in-sample one-step fit of the key variables equals that of a small OLS VAR', r'alegem $\lambda$ astfel încît potrivirea în eșantion la un pas a variabilelor-cheie să fie egală cu cea a unui VAR mic estimat prin OLS'),
      T(r'$\mathrm{Fit}(\lambda) = \frac13\sum_{i\in I}\mathrm{msfe}_i^{(\lambda)}/\mathrm{msfe}_i^{(0)}$ on 1960--1969; here the target is @{bg.fit}', r'$\mathrm{Fit}(\lambda) = \frac13\sum_{i\in I}\mathrm{msfe}_i^{(\lambda)}/\mathrm{msfe}_i^{(0)}$ pe 1960--1969; aici ținta este @{bg.fit}'),
      T(r'$I$: the three key variables; $\mathrm{msfe}_i^{(\lambda)}$: in-sample one-step mean squared error of variable $i$ with tightness $\lambda$; $\lambda = 0$: the prior mean alone', r'$I$: cele trei variabile-cheie; $\mathrm{msfe}_i^{(\lambda)}$: eroarea pătratică medie la un pas, în eșantion, a variabilei $i$ cu gradul de strîngere $\lambda$; $\lambda = 0$: doar media a priori'),
      T(r'our values: MEDIUM @{bg.lmed}, LARGE @{bg.llar} (BGR Table~1: 0.108 and 0.035 on their data set)', r'valorile noastre: MEDIUM @{bg.lmed}, LARGE @{bg.llar} (BGR, tabelul~1: 0,108 și 0,035 pe setul lor de date)')])), 'small')

D.frame(T('Two rules for one hyperparameter (2/2)', 'Două reguli pentru un singur hiperparametru (2/2)'), items(
    (T(r'\textbf{GLP marginal likelihood} \refGLP', r'\textbf{Verosimilitatea marginală GLP} \refGLP'),
     [T('the mode of $\\lambda$ is re-estimated on each window', 'modul lui $\\lambda$ se reestimează pe fiecare fereastră'),
      T(r'on 10-year windows the median mode is @{bg.glp.SMALL} (SMALL) and @{bg.glp.MEDIUM} (MEDIUM)', r'pe ferestre de 10 ani modul median este @{bg.glp.SMALL} (SMALL) și @{bg.glp.MEDIUM} (MEDIUM)'),
      T(r'10\%--90\% range of the MEDIUM mode across windows: [@{bg.glp.MEDIUM.lo}, @{bg.glp.MEDIUM.hi}]', r'intervalul 10\%--90\% al modului MEDIUM între ferestre: [@{bg.glp.MEDIUM.lo}, @{bg.glp.MEDIUM.hi}]')]),
    T(r'The Python package \texttt{bvar} of the Bank of England implements the GLP optimisation for the conjugate model; the notebook compares it with our \texttt{numpy} code', r'Pachetul Python \texttt{bvar} al Băncii Angliei implementează optimizarea GLP pentru modelul conjugat; notebook-ul îl compară cu codul nostru \texttt{numpy}')), 'small')

D.recap(('Hierarchical priors', 'distribuții a priori ierarhice'), [
    T('The marginal likelihood chooses the shrinkage; it falls as the system grows', 'Verosimilitatea marginală alege shrinkage-ul; acesta scade cînd sistemul crește'),
    T('Sum-of-coefficients and initial-observation priors are chosen in the same way', 'Distribuțiile pentru suma coeficienților și observația inițială se aleg la fel'),
    T('A fit rule is a transparent alternative when the evaluation must mimic a published study', 'O regulă de potrivire este o alternativă transparentă atunci cînd evaluarea trebuie să reproducă un studiu publicat')])

# =============================================================================
# 5. BGR
# =============================================================================
D.section('Case study: large Bayesian VARs', 'Studiu de caz: modele VAR bayesiene mari')

D.frame(T('Bańbura, Giannone and Reichlin (2010): the design', 'Bańbura, Giannone și Reichlin (2010): designul'), items(
    (T(r'\refBGR', r'\refBGR'),
     [T('question: can a VAR with 131 variables forecast and identify shocks?', 'întrebarea: poate un VAR cu 131 de variabile să prognozeze și să identifice șocuri?'),
      T('systems: SMALL (employment, CPI, funds rate), MEDIUM (20), LARGE (all)', 'sistemele: SMALL (ocupare, IPC, dobînda federal funds), MEDIUM (20), LARGE (toate)'),
      T(r'$p = 13$; rolling 10-year windows; posterior-mean point forecasts iterated to $h = 12$; benchmark: random walk with drift', r'$p = 13$; ferestre mobile de 10 ani; prognoze punctuale din media a posteriori, iterate pînă la $h = 12$; reper: mers aleator cu derivă'),
      T(r'Minnesota NIW prior plus sum-of-coefficients with $\tau = 10\lambda$ (Section~3.3); $\lambda$ by the fit rule on 1960--1969', r'distribuția a priori NIW Minnesota plus suma coeficienților cu $\tau = 10\lambda$ (secțiunea~3.3); $\lambda$ prin regula potrivirii pe 1960--1969')])), 'small')

D.frame(T('Bańbura, Giannone and Reichlin (2010): our replication', 'Bańbura, Giannone și Reichlin (2010): replicarea noastră'), items(
    (T(r'Our data: FRED-MD-format panel; LARGE = the @{bg.nl} series observed over 1960--2026 (aggregates and components)', r'Datele noastre: panelul în format FRED-MD; LARGE = cele @{bg.nl} serii observate pe 1960--2026 (agregate și componente)'),
     [T('MEDIUM: the BGR list, with three substitutions', 'MEDIUM: lista BGR, cu trei înlocuiri'),
      T('the S\\&P 500, the effective exchange rate and nonborrowed reserves are replaced by the Baa yield, the 3-month bill rate and building permits', 'S\\&P 500, cursul de schimb efectiv și rezervele neîmprumutate sînt înlocuite de randamentul Baa, dobînda la 3 luni și autorizațiile de construcție'),
      T('reason: not available for 1960--2026, or negative after 2008', 'motivul: indisponibile pentru 1960--2026 sau negative după 2008')]),
    (T('Evaluation', 'Evaluarea'),
     [T('targets 1971--2003 (the paper), 2004--2019 and 2004--2026 (extensions)', 'ținte 1971--2003 (lucrarea), 2004--2019 și 2004--2026 (extinderi)'),
      T(r'@{bg.no} forecast origins; GLP SMALL and MEDIUM added', r'@{bg.no} de origini ale prognozelor; adăugăm GLP SMALL și MEDIUM')])), 'small')

chart(T('Forecast accuracy, 1971--2003', 'Acuratețea prognozelor, 1971--2003'), 'ats_ch5_bgr', 'ATS_ch5_large_bvar', [
    T('MSFE relative to the random walk with drift (log scale; below 1 = better), employment and CPI in 100 $\\times$ log levels, funds rate in percent',
      'MSFE relativ la mersul aleator cu derivă (scară logaritmică; sub 1 = mai bine), ocuparea și IPC în 100 $\\times$ logaritmul nivelului, dobînda în procente')],
    h='0.62\\textheight')

interp(('the forecast comparison', 'comparației prognozelor'), [
    (T(r'$h = 1$, employment: OLS SMALL @{bg.eval1.ols.emp1}, BGR MEDIUM @{bg.eval1.med.emp1}, LARGE @{bg.eval1.lar.emp1} (BGR Table~1: 1.14, 0.54, 0.46)', r'$h = 1$, ocuparea: OLS SMALL @{bg.eval1.ols.emp1}, BGR MEDIUM @{bg.eval1.med.emp1}, LARGE @{bg.eval1.lar.emp1} (BGR, tabelul~1: 1,14; 0,54; 0,46)'),
     [T(r'CPI: @{bg.eval1.ols.cpi1}, @{bg.eval1.med.cpi1}, @{bg.eval1.lar.cpi1}; funds rate: @{bg.eval1.ols.ffr1}, @{bg.eval1.med.ffr1}, @{bg.eval1.lar.ffr1}', r'IPC: @{bg.eval1.ols.cpi1}; @{bg.eval1.med.cpi1}; @{bg.eval1.lar.cpi1}; dobînda federal funds: @{bg.eval1.ols.ffr1}; @{bg.eval1.med.ffr1}; @{bg.eval1.lar.ffr1}')]),
    T(r'Adding variables with more shrinkage helps: LARGE beats SMALL for every variable at $h \le 6$', r'Adăugarea de variabile cu mai mult shrinkage ajută: LARGE este superior lui SMALL pentru fiecare variabilă la $h \le 6$'),
    T(r'GLP SMALL is nearly as good as the large systems for employment and CPI (@{bg.eval1.gsm.emp1}, @{bg.eval1.gsm.cpi1}): most of the gain comes from the prior, not only from the variables', r'GLP SMALL este aproape la fel de bun ca sistemele mari pentru ocupare și IPC (@{bg.eval1.gsm.emp1}; @{bg.eval1.gsm.cpi1}): mare parte din cîștig vine din distribuția a priori, nu doar din variabile'),
    T(r'The funds rate beyond 3 months is hard for all models (LARGE @{bg.eval1.lar.ffr12} at $h = 12$)', r'Dobînda federal funds după 3 luni este dificilă pentru toate modelele (LARGE @{bg.eval1.lar.ffr12} la $h = 12$)')])

D.frame(T('After 2003: the extension and March 2020', 'După 2003: extinderea și martie 2020'), table(
    'lcccccc', T(r'\textbf{Model}', r'\textbf{Modelul}') + r' & \textbf{EMPL, 1} & \textbf{EMPL, 12} & \textbf{CPI, 1} & \textbf{CPI, 12} & \textbf{FFR, 1} & \textbf{FFR, 12}',
    [T(name, name) + ' & ' + ' & '.join(f'@{{bg.{per}.{mk}.{v}{h}}}' for v in ('emp', 'cpi', 'ffr') for h in (1, 12))
     for per, label in (('pre2020', ''),) for name, mk in (('OLS SMALL', 'ols'), ('BGR MEDIUM', 'med'), ('BGR LARGE', 'lar'), ('GLP SMALL', 'gsm'), ('GLP MEDIUM', 'gme'))],
    size='scriptsize') + items(
    T('Targets 2004:1--2019:12, relative MSFE (random walk with drift = 1)', 'Ținte 2004:1--2019:12, MSFE relativ (mersul aleator cu derivă = 1)'),
    T(r'Including 2020--2026, the 12-month employment MSFE explodes: BGR MEDIUM @{bg.eval2.med.emp12}, GLP SMALL @{bg.eval2.gsm.emp12}: windows containing April 2020 fit the collapse as dynamics', r'Incluzînd 2020--2026, MSFE la 12 luni pentru ocupare explodează: BGR MEDIUM @{bg.eval2.med.emp12}, GLP SMALL @{bg.eval2.gsm.emp12}: ferestrele care conțin aprilie 2020 tratează prăbușirea ca dinamică'),
    T(r'Remedy: scale the residual variance of the pandemic months by estimated factors \refLP, or stochastic volatility (next section)', r'Remediul: scalăm varianța reziduală a lunilor pandemiei cu factori estimați \refLP sau folosim volatilitatea stochastică (secțiunea următoare)')), 'footnotesize')

D.frame(T('A monetary policy shock in a large VAR', 'Un șoc de politică monetară într-un VAR mare'), items(
    (T(r'Recursive scheme of \refBGR, Section~4: $y_t = (X_t, r_t, Z_t)$, slow variables $X_t$ (real activity, prices), the funds rate $r_t$, fast variables $Z_t$ (money, rates, exchange rates)', r'Schema recursivă din \refBGR, secțiunea~4: $y_t = (X_t, r_t, Z_t)$, variabile lente $X_t$ (activitate reală, prețuri), dobînda $r_t$, variabile rapide $Z_t$ (monedă, dobînzi, cursuri de schimb)'),
     [T('only the position of $r_t$ matters (Chapter 3): no ordering inside the blocks is needed', 'contează doar poziția lui $r_t$ (Capitolul 3): nu este nevoie de nicio ordonare în interiorul blocurilor')]),
    (T(r'Bayesian bands: for each draw $(B, \Sigma)$ from the NIW posterior, compute the Cholesky impact column and the responses; report posterior quantiles', r'Benzi bayesiene: pentru fiecare extragere $(B, \Sigma)$ din distribuția a posteriori NIW calculăm coloana de impact Cholesky și răspunsurile; raportăm cuantilele a posteriori'),
     [T(r'@{ir.nd} draws, 100 bp shock, sample 1961--2002, $p = 13$; SMALL with a nearly flat prior', r'@{ir.nd} de extrageri, șoc de 100 bp, eșantion 1961--2002, $p = 13$; SMALL cu o distribuție a priori aproape plată')]),
    T('These are the posterior bands Chapter 3 announced: pointwise credible intervals, conditional on the identifying assumption', 'Acestea sînt benzile a posteriori anunțate în Capitolul 3: intervale credibile punctuale, condiționate de ipoteza de identificare')), 'small')

chart(T('Responses to a 100 bp funds-rate shock', 'Răspunsuri la un șoc de 100 bp al dobînzii federal funds'), 'ats_ch5_bvar_irf', 'ATS_ch5_large_bvar', [
    T('Posterior medians with 68\\% and 90\\% bands; rows: SMALL, MEDIUM, LARGE; employment and CPI in percent', 'Mediane a posteriori cu benzi de 68\\% și 90\\%; liniile: SMALL, MEDIUM, LARGE; ocuparea și IPC în procente')],
    h='0.68\\textheight')

interp(('the responses', 'răspunsurilor'), [
    T(r'Employment: trough @{ir.SMALL.emp_min}\% (SMALL, month @{ir.SMALL.ea}), @{ir.LARGE.emp_min}\% (LARGE, month @{ir.LARGE.ea}); after four years LARGE is back to @{ir.LARGE.emp48}\% (band [@{ir.LARGE.emp48_lo}, @{ir.LARGE.emp48_hi}])', r'Ocuparea: minimum @{ir.SMALL.emp_min}\% (SMALL, luna @{ir.SMALL.ea}), @{ir.LARGE.emp_min}\% (LARGE, luna @{ir.LARGE.ea}); după patru ani LARGE revine la @{ir.LARGE.emp48}\% (banda [@{ir.LARGE.emp48_lo}, @{ir.LARGE.emp48_hi}])'),
    T(r'CPI: the price puzzle shrinks from @{ir.SMALL.cpi_max}\% (SMALL) to @{ir.LARGE.cpi_max}\% (LARGE); after four years LARGE gives @{ir.LARGE.cpi48}\% (band [@{ir.LARGE.cpi48_lo}, @{ir.LARGE.cpi48_hi}])', r'IPC: anomalia prețurilor scade de la @{ir.SMALL.cpi_max}\% (SMALL) la @{ir.LARGE.cpi_max}\% (LARGE); după patru ani LARGE dă @{ir.LARGE.cpi48}\% (banda [@{ir.LARGE.cpi48_lo}, @{ir.LARGE.cpi48_hi}])'),
    T('As in BGR: more information makes the employment response less persistent and the price response more plausible', 'Ca în BGR: mai multă informație face răspunsul ocupării mai puțin persistent și răspunsul prețurilor mai plauzibil'),
    T('The bands do not widen with 102 variables: the prior pays for the extra coefficients', 'Benzile nu se lărgesc cu 102 variabile: distribuția a priori compensează coeficienții suplimentari')])

D.recap(('Large BVARs', 'modele BVAR mari'), [
    T('With shrinkage that grows with the system, a 102-variable VAR forecasts better than a 3-variable OLS VAR', 'Cu un shrinkage care crește odată cu sistemul, un VAR cu 102 variabile prognozează mai bine decît un VAR cu 3 variabile estimat prin OLS'),
    T('The 1971--2003 results of BGR replicate on today\'s data; after 2020 the homoskedastic BVAR fails', 'Rezultatele BGR pentru 1971--2003 se replică pe datele actuale; după 2020 BVAR-ul homoscedastic eșuează'),
    T('Large information sets reduce the price puzzle of small monetary VARs', 'Seturile mari de informații reduc anomalia prețurilor din VAR-urile monetare mici')])

# =============================================================================
# 6. SV
# =============================================================================
D.section('Stochastic volatility in BVARs', 'Volatilitate stochastică în modelele BVAR')

D.frame(T('Large BVARs with stochastic volatility', 'Modele BVAR mari cu volatilitate stochastică'), items(
    (T(r'\textbf{Common volatility} \refCCMa: $u_t = \sqrt{f_t}\,\varepsilon_t$, $\varepsilon_t \sim N(0, \Sigma)$, $\ln f_t = \phi\ln f_{t-1} + \nu_t$', r'\textbf{Volatilitate comună} \refCCMa: $u_t = \sqrt{f_t}\,\varepsilon_t$, $\varepsilon_t \sim N(0, \Sigma)$, $\ln f_t = \phi\ln f_{t-1} + \nu_t$'),
     [T(r'$u_t$: the VAR residual; $f_t > 0$: a volatility factor common to all equations; $\phi$: its persistence; $\nu_t$: its shock', r'$u_t$: reziduul VAR; $f_t > 0$: un factor de volatilitate comun tuturor ecuațiilor; $\phi$: persistența lui; $\nu_t$: șocul lui'),
      T(r'given $f_{1:T}$, the model is a weighted conjugate BVAR (rows divided by $\sqrt{f_t}$); $f_t$ is drawn by a Kim--Shephard--Chib step', r'dat fiind $f_{1:T}$, modelul este un BVAR conjugat ponderat (liniile împărțite la $\sqrt{f_t}$); $f_t$ se extrage cu un pas Kim--Shephard--Chib')]),
    (T(r'\textbf{Variable-specific volatilities} \refCCMb, \refClark: $\Sigma_t = A^{-1}H_tA^{-1\prime}$, $H_t$ diagonal with log-AR volatilities \refPrim', r'\textbf{Volatilități specifice fiecărei variabile} \refCCMb, \refClark: $\Sigma_t = A^{-1}H_tA^{-1\prime}$, $H_t$ diagonală cu volatilități log-AR \refPrim'),
     [T(r'$A$: lower triangular with unit diagonal (the contemporaneous relations); $H_t$: the time-varying variances of the orthogonalised shocks', r'$A$: inferior triunghiulară cu diagonala unu (relațiile contemporane); $H_t$: varianțele variabile în timp ale șocurilor ortogonalizate'),
      T('conjugacy is lost; the triangular algorithm draws the equations one at a time and makes $n = 100$ feasible', 'conjugarea se pierde; algoritmul triunghiular extrage ecuațiile una cîte una și face posibil $n = 100$')]),
    T('Gains: mainly in density forecasts (calibrated intervals) and in robustness to outliers such as 2020', 'Cîștigurile: mai ales în prognozele de densitate (intervale calibrate) și în robustețea la valori extreme precum 2020')), 'small')

chart(T('A common volatility factor in the BVAR residuals', 'Un factor comun de volatilitate în reziduurile BVAR'), 'ats_ch5_common_vol', 'ATS_ch5_large_bvar', [
    T('MEDIUM BVAR (GLP hyperparameters), 1960--2026: log of the cross-sectional mean of the squared standardised residuals', 'BVAR MEDIUM (hiperparametri GLP), 1960--2026: logaritmul mediei transversale a pătratelor reziduurilor standardizate')],
    h='0.68\\textheight')

interp(('the volatility proxy', 'indicatorului de volatilitate'), [
    T(r'Common movements: the residual variance rises in every recession and falls in the Great Moderation (1960--1984 is @{vo.gm} times 1985--2007)', r'Mișcări comune: varianța reziduală crește în fiecare recesiune și scade în Marea Moderație (1960--1984 este de @{vo.gm} ori 1985--2007)'),
    T(r'April 2020 is @{vo.peak} times the median month: a homoskedastic Gaussian BVAR treats it as an ordinary observation', r'Aprilie 2020 este de @{vo.peak} ori luna mediană: un BVAR gaussian homoscedastic o tratează ca pe o observație obișnuită'),
    T('This is the case for the common-volatility model (one extra state) before the full variable-specific model; Chapter 6 gives the filtering tools', 'Acesta este argumentul pentru modelul cu volatilitate comună (o singură stare în plus) înaintea modelului complet cu volatilități specifice; Capitolul 6 dă instrumentele de filtrare')])

# =============================================================================
# 7. MODELE FACTORIALE
# =============================================================================
D.section('Approximate factor models', 'Modele factoriale aproximative')

D.frame(T('The approximate factor model', 'Modelul factorial aproximativ'), items(
    (T(r'$x_{it} = \lambda_i\'F_t + e_{it}$, $i = 1, \dots, N$, $t = 1, \dots, T$; $F_t$: $r$ common factors, $\lambda_i$: loadings, $e_{it}$: idiosyncratic', r'$x_{it} = \lambda_i\'F_t + e_{it}$, $i = 1, \dots, N$, $t = 1, \dots, T$; $F_t$: $r$ factori comuni, $\lambda_i$: ponderi factoriale (loadings), $e_{it}$: componente idiosincratice'),
     [T(r'\emph{approximate} \refCR: the $e_{it}$ may be weakly correlated across $i$ and over $t$, provided the correlation is bounded as $N \to \infty$', r'\emph{aproximativ} \refCR: $e_{it}$ pot fi slab corelate între $i$ și în timp, cu condiția ca acea corelație să rămînă mărginită cînd $N \to \infty$'),
      T(r'$\Lambda$ ($N\times r$): the stacked loadings; $X$ ($T\times N$): the panel; $\Sigma_\Lambda$: a positive definite limit', r'$\Lambda$ ($N\times r$): ponderile factoriale așezate pe linii; $X$ ($T\times N$): panelul; $\Sigma_\Lambda$: o limită pozitiv definită'),
      T(r'pervasiveness: $\Lambda\'\Lambda/N \to \Sigma_\Lambda > 0$, every factor affects many series; the $r$ largest eigenvalues of $XX\'$ grow with $N$, the others do not', r'caracterul general (pervasiveness): $\Lambda\'\Lambda/N \to \Sigma_\Lambda > 0$, fiecare factor afectează multe serii; cele mai mari $r$ valori proprii ale lui $XX\'$ cresc cu $N$, celelalte nu')]),
    (T(r'Identification: $\Lambda F_t = (\Lambda H)(H^{-1}F_t)$ for any invertible $H$: only the factor space is identified', r'Identificarea: $\Lambda F_t = (\Lambda H)(H^{-1}F_t)$ pentru orice $H$ inversabilă: este identificat doar spațiul factorilor'),
     [T(r'normalisation for PCA: $F\'F/T = I_r$ and $\Lambda\'\Lambda$ diagonal', r'normalizarea pentru PCA: $F\'F/T = I_r$ și $\Lambda\'\Lambda$ diagonală')]),
    T('Static form of a dynamic model: lags of the dynamic factors are stacked in $F_t$ \\refSWc; the generalised dynamic model works in the frequency domain \\refFHLR', 'Forma statică a unui model dinamic: lagurile factorilor dinamici sînt așezate în $F_t$ \\refSWc; modelul dinamic generalizat lucrează în domeniul frecvențelor \\refFHLR')), 'small')

D.frame(T('Principal components', 'Componente principale'), items(
    (T(r'Least squares: $\min_{F, \Lambda}\sum_{i,t}(x_{it} - \lambda_i\'F_t)^2$ with $F\'F/T = I$: $\hat F = \sqrt T\times$ the first $r$ eigenvectors of $XX\'$, $\hat\Lambda = X\'\hat F/T$', r'Cele mai mici pătrate: $\min_{F, \Lambda}\sum_{i,t}(x_{it} - \lambda_i\'F_t)^2$ cu $F\'F/T = I$: $\hat F = \sqrt T\times$ primii $r$ vectori proprii ai lui $XX\'$, $\hat\Lambda = X\'\hat F/T$'),
     [T('standardise each series first: PCA is not scale invariant', 'standardizați întîi fiecare serie: PCA nu este invariantă la scară')]),
    (T(r'Consistency \refSWa, \refBai: $\hat F_t \to HF_t$ as $N, T \to \infty$ at rate $\min(\sqrt N, \sqrt T)$', r'Consistența \refSWa, \refBai: $\hat F_t \to HF_t$ cînd $N, T \to \infty$, cu viteza $\min(\sqrt N, \sqrt T)$'),
     [T(r'$H$: an invertible $r\times r$ rotation; PCA recovers the factors up to this rotation', r'$H$: o rotație inversabilă de $r\times r$; PCA recuperează factorii pînă la această rotație'),
      T(r'if $\sqrt T/N \to 0$, the estimated factors can be used as regressors as if observed (no generated-regressor correction)', r'dacă $\sqrt T/N \to 0$, factorii estimați pot fi folosiți ca regresori ca și cum ar fi observați (fără corecția pentru regresori generați)')]),
    T(r'Missing values and mixed start dates: EM \refSWb, \refMN: fill with 0, run PCA, refill the missing cells with $\hat\lambda_i\'\hat F_t$, iterate', r'Valori lipsă și date de început diferite: EM \refSWb, \refMN: completăm cu 0, aplicăm PCA, recompletăm celulele lipsă cu $\hat\lambda_i\'\hat F_t$, iterăm')), 'small')

D.frame(T('The FRED-MD database', 'Baza de date FRED-MD'), items(
    (T(r'\refMN: about 130 US monthly series since 1959, updated monthly, with a transformation code per series and vintages for real-time work', r'\refMN: aproximativ 130 de serii lunare SUA începînd din 1959, actualizate lunar, cu un cod de transformare pentru fiecare serie și cu ediții pentru analize în timp real'),
     [T('eight groups: output and income, labour market, housing, consumption and orders, money and credit, interest and exchange rates, prices, stock market', 'opt grupe: producție și venit, piața muncii, locuințe, consum și comenzi, monedă și credit, dobînzi și cursuri de schimb, prețuri, piața de acțiuni'),
      T(r'outliers: an observation more than 10 interquartile ranges from the median is set to missing (@{fa.nout} cells here)', r'valori extreme: o observație aflată la mai mult de 10 abateri intercuartilice de mediană devine lipsă (@{fa.nout} celule aici)')]),
    (T(r'Our panel: @{fa.N} FRED-MD series that FRED distributes (stock-market series are not), 1960:1--2026:7, @{fa.miss}\% missing cells', r'Panelul nostru: @{fa.N} serii FRED-MD distribuite de FRED (seriile bursiere nu sînt), 1960:1--2026:7, @{fa.miss}\% celule lipsă'),
     [T('the official file (current.csv of the St.~Louis Fed) can replace it in the notebook with one line', 'fișierul oficial (current.csv al St.~Louis Fed) îl poate înlocui în notebook printr-o singură linie')]),
    T(r'Current vintage only: the results are pseudo out of sample, not real time \refCS', r'Doar ediția curentă: rezultatele sînt pseudo în afara eșantionului, nu în timp real \refCS')), 'small')

chart(T('Factors of the FRED-MD panel', 'Factorii panelului FRED-MD'), 'ats_ch5_factors', 'ATS_ch5_factors', [
    T(r'Left: share of the variance of the standardised panel explained by each principal component; right: the first factor (EM, 8 factors), NBER recessions shaded',
      r'Stînga: ponderea varianței panelului standardizat explicată de fiecare componentă principală; dreapta: primul factor (EM, 8 factori), recesiunile NBER marcate')],
    h='0.61\\textheight')

interp(('the factors', 'factorilor'), [
    T(r'The first component explains @{fa.s1}\%, the second @{fa.s2}\%; five explain @{fa.c5}\%, eight @{fa.c8}\%', r'Prima componentă explică @{fa.s1}\%, a doua @{fa.s2}\%; cinci explică @{fa.c5}\%, opt @{fa.c8}\%'),
    T(r'The first factor is a real activity index: correlation @{fa.rec} with the NBER recession indicator; its minimum is April 2020', r'Primul factor este un indice al activității reale: corelația @{fa.rec} cu indicatorul recesiunilor NBER; minimul este în aprilie 2020'),
    T('No component dominates: macro panels have a few strong factors and a long tail of weak ones, which makes the number of factors a real question', 'Nicio componentă nu domină: panelurile macro au cîțiva factori puternici și o coadă lungă de factori slabi, ceea ce face din numărul de factori o întrebare reală')])

D.frame(T('How many factors? Bai and Ng (2002)', 'Cîți factori? Bai și Ng (2002)'), items(
    (T(r'$V(k) = (NT)^{-1}\sum_{i,t}(x_{it} - \hat\lambda_i\'\hat F_t)^2$ after $k$ components; it falls with $k$, so it needs a penalty \refBN', r'$V(k) = (NT)^{-1}\sum_{i,t}(x_{it} - \hat\lambda_i\'\hat F_t)^2$ după $k$ componente; scade cu $k$, deci are nevoie de o penalizare \refBN'),
     [T(r'$IC_{p1}(k) = \ln V(k) + k\frac{N + T}{NT}\ln\frac{NT}{N + T}$, $IC_{p2}(k) = \ln V(k) + k\frac{N + T}{NT}\ln C_{NT}^2$, $C_{NT}^2 = \min(N, T)$', r'$IC_{p1}(k) = \ln V(k) + k\frac{N + T}{NT}\ln\frac{NT}{N + T}$, $IC_{p2}(k) = \ln V(k) + k\frac{N + T}{NT}\ln C_{NT}^2$, $C_{NT}^2 = \min(N, T)$'),
      T(r'$IC_{p3}(k) = \ln V(k) + k\ln C_{NT}^2/C_{NT}^2$; choose the $k$ that minimises the criterion; the penalty grows with $k$ and vanishes as $N, T \to \infty$', r'$IC_{p3}(k) = \ln V(k) + k\ln C_{NT}^2/C_{NT}^2$; alegem $k$ care minimizează criteriul; penalizarea crește cu $k$ și dispare cînd $N, T \to \infty$'),
      T(r'$PC_{p}$ versions: $V(k) + k\hat\sigma^2 g(N, T)$ with $\hat\sigma^2 = V(k_{\max})$, $g(N, T)$ the same penalties: depend on $k_{\max}$, the largest $k$ tried', r'variantele $PC_{p}$: $V(k) + k\hat\sigma^2 g(N, T)$ cu $\hat\sigma^2 = V(k_{\max})$, $g(N, T)$ aceleași penalizări: depind de $k_{\max}$, cel mai mare $k$ încercat')]),
    (T(r'Our panel ($k_{\max} = 15$): $IC_{p1}$ = @{fa.k.IC_p1}, $IC_{p2}$ = @{fa.k.IC_p2}, $IC_{p3}$ = @{fa.k.IC_p3}, $PC_{p1}$ = @{fa.k.PC_p1}, $PC_{p2}$ = @{fa.k.PC_p2}', r'Panelul nostru ($k_{\max} = 15$): $IC_{p1}$ = @{fa.k.IC_p1}, $IC_{p2}$ = @{fa.k.IC_p2}, $IC_{p3}$ = @{fa.k.IC_p3}, $PC_{p1}$ = @{fa.k.PC_p1}, $PC_{p2}$ = @{fa.k.PC_p2}'),
     [T('the criteria disagree when the eigenvalues decline slowly; report the choice and its sensitivity', 'criteriile nu sînt de acord atunci cînd valorile proprii scad lent; raportați alegerea și sensibilitatea ei')]),
    T('For forecasting, the number of factors in the regression is chosen separately (by BIC), as in diffusion-index forecasts', 'Pentru prognoză, numărul de factori din regresie se alege separat (prin BIC), ca în prognozele cu indici de difuziune')), 'small')

chart(T('The economic content of the factors', 'Conținutul economic al factorilor'), 'ats_ch5_mr2', 'ATS_ch5_factors', [
    T(r'Average marginal $R^2$ of the regression of each standardised series on one factor, by group (as in McCracken and Ng 2016)', r'$R^2$ marginal mediu al regresiei fiecărei serii standardizate pe un singur factor, pe grupe (ca în McCracken și Ng 2016)')],
    h='0.68\\textheight')

interp(('the marginal $R^2$', 'lui $R^2$ marginal'), [
    T(r'Factor 1 is real activity: $R^2$ @{mr.f1.out} for output, @{mr.f1.lab} for labour; the best single series has @{mr.top1}', r'Factorul 1 este activitatea reală: $R^2$ @{mr.f1.out} pentru producție, @{mr.f1.lab} pentru muncă; cea mai bine explicată serie are @{mr.top1}'),
    T(r'Factors 2 and 3 load on prices (@{mr.f2.pri}, @{mr.f3.pri}) and housing (@{mr.f2.hou}, @{mr.f3.hou})', r'Factorii 2 și 3 se încarcă pe prețuri (@{mr.f2.pri}; @{mr.f3.pri}) și pe locuințe (@{mr.f2.hou}; @{mr.f3.hou})'),
    T('Interest rates load weakly on the first three factors: monetary information sits in later factors or in the rates themselves, the motivation for the FAVAR', 'Dobînzile se încarcă slab pe primii trei factori: informația monetară se află în factori ulteriori sau în dobînzile înseși, motivația pentru FAVAR'),
    T('Labels are a rotation choice: the factor space, not each factor, is identified', 'Etichetele sînt o alegere de rotație: este identificat spațiul factorilor, nu fiecare factor')])

D.frame(T('Diffusion-index forecasts: Stock and Watson (2002)', 'Prognoze cu indici de difuziune: Stock și Watson (2002)'), items(
    (T(r'\refSWb: $y_{t+h}^h = \alpha_h + \beta_h\'\hat F_t + \sum_{j=0}^{p}\gamma_{hj}z_{t-j} + \varepsilon_{t+h}$ (direct forecast, one equation per $h$)', r'\refSWb: $y_{t+h}^h = \alpha_h + \beta_h\'\hat F_t + \sum_{j=0}^{p}\gamma_{hj}z_{t-j} + \varepsilon_{t+h}$ (prognoză directă, o ecuație pentru fiecare $h$)'),
     [T(r'$y_{t+h}^h$: the target over the next $h$ months, annualised; $\hat F_t$: the estimated factors; $z_t$: the target\'s own current growth; $\alpha_h$, $\beta_h$, $\gamma_{hj}$: coefficients estimated by OLS for each $h$', r'$y_{t+h}^h$: ținta pe următoarele $h$ luni, anualizată; $\hat F_t$: factorii estimați; $z_t$: creșterea curentă a țintei; $\alpha_h$, $\beta_h$, $\gamma_{hj}$: coeficienți estimați prin OLS pentru fiecare $h$'),
      T(r'real series: $y_{t+h}^h = \frac{1200}{h}\ln(Y_{t+h}/Y_t)$; prices: $\frac{1200}{h}\ln(P_{t+h}/P_t) - 1200\ln(P_t/P_{t-1})$ ($Y_t$, $P_t$: levels)', r'serii reale: $y_{t+h}^h = \frac{1200}{h}\ln(Y_{t+h}/Y_t)$; prețuri: $\frac{1200}{h}\ln(P_{t+h}/P_t) - 1200\ln(P_t/P_{t-1})$ ($Y_t$, $P_t$: nivelurile)'),
      T(r'DI: factors only, $k \in \{1, \dots, 12\}$ by BIC; DI-AR, Lag: factors and $p \in \{0, \dots, 5\}$ lags by BIC; benchmark: AR with BIC lags', r'DI: doar factori, $k \in \{1, \dots, 12\}$ prin BIC; DI-AR, Lag: factori și $p \in \{0, \dots, 5\}$ laguri prin BIC; reperul: AR cu laguri alese prin BIC')]),
    (T('Recursive: factors re-estimated at each origin by EM on the data available then; origins from 1970:1', 'Recursiv: factorii sînt reestimați la fiecare origine prin EM pe datele disponibile atunci; originile încep în 1970:1'),
     [T('evaluation 1970--1998 (the paper) and 1999--2019 (extension), by forecast origin', 'evaluarea 1970--1998 (lucrarea) și 1999--2019 (extindere), după originea prognozei')]),
    T('Targets: industrial production, payroll employment, CPI inflation; $h = 1, 6, 12$ months', 'Variabilele-țintă: producția industrială, numărul de salariați, inflația IPC; $h = 1, 6, 12$ luni')), 'small')

chart(T('Diffusion-index forecasts against an AR', 'Prognoze cu indici de difuziune comparate cu un AR'), 'ats_ch5_di', 'ATS_ch5_factors', [
    T('MSE relative to the AR forecast with BIC lags (below 1 = better)', 'MSE relativ la prognoza AR cu laguri alese prin BIC (sub 1 = mai bine)')],
    h='0.60\\textheight')

interp(('the diffusion indexes', 'indicilor de difuziune'), [
    T(r'1970--1998: large gains for real activity at $h = 12$: IP @{di.eval1.ip.di12}, employment @{di.eval1.emp.di12}; for inflation only with own lags (DI-AR, Lag @{di.eval1.cpi.dl12})', r'1970--1998: cîștiguri mari pentru activitatea reală la $h = 12$: IP @{di.eval1.ip.di12}, ocupare @{di.eval1.emp.di12}; pentru inflație doar cu lagurile proprii (DI-AR, Lag @{di.eval1.cpi.dl12})'),
    T(r'1999--2019: the gains vanish (IP @{di.pre2020.ip.di12}, employment @{di.pre2020.emp.di12}, inflation @{di.pre2020.cpi.dl12}): the Great Moderation made activity less predictable from the panel', r'1999--2019: cîștigurile dispar (IP @{di.pre2020.ip.di12}, ocupare @{di.pre2020.emp.di12}, inflație @{di.pre2020.cpi.dl12}): Marea Moderație a făcut activitatea mai puțin previzibilă din panel'),
    T(r'BIC selects a median of @{di.kmed} factors (10\%--90\%: @{di.kq10}--@{di.kq90}) for DI-AR, Lag at $h = 12$', r'BIC alege în mediană @{di.kmed} factori (10\%--90\%: @{di.kq10}--@{di.kq90}) pentru DI-AR, Lag la $h = 12$'),
    T(r'Bayesian shrinkage and principal components give highly correlated forecasts in large panels \refDGRa: two ways to use the same information', r'Shrinkage-ul bayesian și componentele principale dau prognoze puternic corelate în panelurile mari \refDGRa: două căi pentru aceeași informație')])

D.recap(('Factor models', 'modele factoriale'), [
    T('A few factors summarise a hundred series; PCA estimates the factor space consistently as $N, T \\to \\infty$', 'Cîțiva factori rezumă o sută de serii; PCA estimează consistent spațiul factorilor cînd $N, T \\to \\infty$'),
    T('Bai--Ng criteria choose the number of factors; check their sensitivity', 'Criteriile Bai--Ng aleg numărul de factori; verificați sensibilitatea lor'),
    T('Diffusion indexes helped strongly before 1999 and much less after: evaluate on more than one period', 'Indicii de difuziune au ajutat mult înainte de 1999 și mult mai puțin după: evaluați pe mai multe perioade')])

# =============================================================================
# 8. FAVAR
# =============================================================================
D.section('Factor-augmented VARs', 'Modele VAR augmentate cu factori')

D.frame(T('FAVAR: Bernanke, Boivin and Eliasz (2005)', 'FAVAR: Bernanke, Boivin și Eliasz (2005)'), two(
    ph('bernanke', T('Ben Bernanke, 2008', 'Ben Bernanke, 2008'), h='0.32\\textheight'),
    items((T(r'\refBBE', r'\refBBE'),
           [T(r'VAR: $\binom{F_t}{Y_t} = \Phi(L)\binom{F_{t-1}}{Y_{t-1}} + v_t$; panel: $X_t = \Lambda^fF_t + \Lambda^yY_t + e_t$', r'VAR-ul: $\binom{F_t}{Y_t} = \Phi(L)\binom{F_{t-1}}{Y_{t-1}} + v_t$; panelul: $X_t = \Lambda^fF_t + \Lambda^yY_t + e_t$'),
            T(r'$Y_t$: the funds rate; $F_t$: $K$ unobserved factors; $X_t$: the large panel', r'$Y_t$: dobînda federal funds; $F_t$: $K$ factori neobservați; $X_t$: panelul mare'),
            T(r'$\Lambda^f$, $\Lambda^y$: loadings; $\Phi(L)$: a lag polynomial; $v_t$, $e_t$: errors', r'$\Lambda^f$, $\Lambda^y$: ponderile factoriale; $\Phi(L)$: un polinom în operatorul lag; $v_t$, $e_t$: erorile')]),
          (T('Why it helps', 'Avantajul'),
           [T('the VAR sees the information of 100 series through $K$ factors', 'VAR-ul vede informația a 100 de serii prin $K$ factori'),
            T('responses are available for every series in $X_t$', 'răspunsurile sînt disponibile pentru fiecare serie din $X_t$')])), '0.30', '0.68'), 'footnotesize')

D.frame(T('FAVAR: estimation and our replication', 'FAVAR: estimarea și replicarea noastră'), items(
    (T('Two-step estimation (Section III of the paper)', 'Estimarea în doi pași (secțiunea III a lucrării)'),
     [T(r'principal components $\hat C_t$ of $X_t$; slow factors from slow-moving series', r'componentele principale $\hat C_t$ ale lui $X_t$; factorii lenți din seriile lente'),
      T(r'remove $Y_t$: $\hat F_t = \hat C_t - \hat b_YY_t$; $\hat b_Y$: the coefficient of $Y_t$ in a regression of $\hat C_t$ on the slow factors and $Y_t$', r'eliminăm $Y_t$: $\hat F_t = \hat C_t - \hat b_YY_t$; $\hat b_Y$: coeficientul lui $Y_t$ într-o regresie a lui $\hat C_t$ pe factorii lenți și pe $Y_t$'),
      T(r'Cholesky identification with $Y_t$ last; a 25 bp shock', r'identificare Cholesky cu $Y_t$ ultimul; un șoc de 25 bp')]),
    (T('Specification', 'Specificația'),
     [T('paper: $K = 3$, VAR(13), 1960:1--2001:8', 'lucrarea: $K = 3$, VAR(13), 1960:1--2001:8'),
      T(r'ours: $T = @{fv.T}$, $N = @{fv.N}$ balanced series, of which @{fv.Ns} slow', r'la noi: $T = @{fv.T}$, $N = @{fv.N}$ serii complete, dintre care @{fv.Ns} lente'),
      T('prices and money enter as monthly growth rates; responses are cumulated to levels', 'prețurile și masa monetară intră ca rate lunare de creștere; răspunsurile se cumulează în niveluri')])), 'small')

chart(T('FAVAR responses to a 25 bp monetary policy shock', 'Răspunsurile FAVAR la un șoc de politică monetară de 25 bp'), 'ats_ch5_favar', 'ATS_ch5_favar', [
    T(r'Levels in percent (rates and unemployment in pp); 90\% residual-bootstrap bands, factors treated as data; dashed: sample to 2007:12', r'Niveluri în procente (dobînzi și șomaj în pp); benzi bootstrap pe reziduuri de 90\%, factorii tratați ca date; linia întreruptă: eșantion pînă în 2007:12')],
    h='0.65\\textheight')

interp(('the FAVAR', 'FAVAR'), [
    T(r'Real activity falls with a lag: IP trough @{fv.ipmin}\% after @{fv.iparg} months, capacity utilisation @{fv.cumin} pp, payrolls @{fv.empmin}\%, unemployment up by @{fv.umax} pp', r'Activitatea reală scade cu întîrziere: IP minim @{fv.ipmin}\% după @{fv.iparg} luni, gradul de utilizare a capacităților @{fv.cumin} pp, numărul de salariați @{fv.empmin}\%, șomajul crește cu @{fv.umax} pp'),
    T(r'Housing starts react first and most (@{fv.hmin}\% after @{fv.harg} months): the interest-sensitive sector', r'Locuințele începute reacționează primele și cel mai puternic (@{fv.hmin}\% după @{fv.harg} luni): sectorul sensibil la dobîndă'),
    T(r'The price puzzle is small (at most @{fv.cpimax}\%, month @{fv.cpiarg}); CPI ends at @{fv.cpi48}\% after 48 months (band [@{fv.cpi48lo}, @{fv.cpi48hi}]); to 2007: @{fv.cpi482}\%', r'Anomalia prețurilor este mică (cel mult @{fv.cpimax}\%, luna @{fv.cpiarg}); IPC ajunge la @{fv.cpi48}\% după 48 de luni (banda [@{fv.cpi48lo}, @{fv.cpi48hi}]); pînă în 2007: @{fv.cpi482}\%'),
    T('Seminar 5, B4: with $K = 1$ or $K = 5$ the puzzle returns; the choice of $K$ is an identifying assumption, not a detail', 'Seminarul 5, B4: cu $K = 1$ sau $K = 5$ anomalia revine; alegerea lui $K$ este o ipoteză de identificare, nu un detaliu')])

# =============================================================================
# 9. DFM
# =============================================================================
D.section('Dynamic factor models in state-space form', 'Modele factoriale dinamice în forma spațiului stărilor')

D.frame(T('The dynamic factor model (1/2)', 'Modelul factorial dinamic (1/2)'), items(
    (T(r'Measurement equation: $x_t = \Lambda f_t + e_t$, $e_t \sim N(0, \Psi)$', r'Ecuația de măsurare: $x_t = \Lambda f_t + e_t$, $e_t \sim N(0, \Psi)$'),
     [T(r'$x_t$: the $N$ observed series; $f_t$: the $r$ factors; $\Lambda$ ($N\times r$): the loadings', r'$x_t$: cele $N$ serii observate; $f_t$: cei $r$ factori; $\Lambda$ ($N\times r$): ponderile factoriale'),
      T(r'$e_t$: idiosyncratic errors with diagonal covariance $\Psi$', r'$e_t$: erorile idiosincratice, cu covarianța diagonală $\Psi$')]),
    (T(r'Transition equation: $f_t = A_1f_{t-1} + \dots + A_qf_{t-q} + u_t$, $u_t \sim N(0, Q)$', r'Ecuația de tranziție: $f_t = A_1f_{t-1} + \dots + A_qf_{t-q} + u_t$, $u_t \sim N(0, Q)$'),
     [T(r'$A_j$: the factor VAR($q$) matrices; $Q$: the covariance of the factor shocks $u_t$', r'$A_j$: matricele VAR($q$) ale factorilor; $Q$: covarianța șocurilor factorilor $u_t$')]),
    (T('A state-space model (TSA, Chapter 10; Chapter 6)', 'Un model în spațiul stărilor (TSA, Capitolul 10; Capitolul 6)'),
     [T(r'state $s_t = (f_t\', \dots, f_{t-m}\')\'$, with $m \ge q - 1$ lags', r'starea $s_t = (f_t\', \dots, f_{t-m}\')\'$, cu $m \ge q - 1$ laguri'),
      T('estimated by the Kalman filter and smoother', 'estimată prin filtrul și netezitorul Kalman')])), 'small')

D.frame(T('The dynamic factor model (2/2)', 'Modelul factorial dinamic (2/2)'), items(
    (T(r'\textbf{Two-step estimation} \refDGRb', r'\textbf{Estimarea în doi pași} \refDGRb'),
     [T(r'PCA for $\hat f_t$; OLS for $\Lambda$ and $\Psi$; a VAR on $\hat f_t$ for $A$ and $Q$', r'PCA pentru $\hat f_t$; OLS pentru $\Lambda$ și $\Psi$; un VAR pe $\hat f_t$ pentru $A$ și $Q$'),
      T(r'then the Kalman smoother re-estimates $f_t$', r'apoi netezitorul Kalman reestimează $f_t$'),
      T('consistent for large $N$ and $T$ even though $\\Psi$ diagonal is misspecified', 'consistent pentru $N$ și $T$ mari, deși $\\Psi$ diagonală este o specificare greșită')]),
    (T(r'\textbf{Quasi-maximum likelihood by EM} \refDGRc, \refBM', r'\textbf{Verosimilitate cvasi-maximă prin EM} \refDGRc, \refBM'),
     [T('E-step: the Kalman smoother; M-step: regressions on the smoothed moments', 'pasul E: netezitorul Kalman; pasul M: regresii pe momentele netezite'),
      T('handles any pattern of missing data and idiosyncratic AR(1) terms', 'tratează orice structură de date lipsă și componente idiosincratice AR(1)')])), 'small')

D.frame(T('Missing data are not a problem for the Kalman filter', 'Datele lipsă nu sînt o problemă pentru filtrul Kalman'), items(
    (T(r'At time $t$, keep only the observed rows: $x_t^o = W_tx_t$, $\Lambda_t = W_t\Lambda$, $\Psi_t = W_t\Psi W_t\'$ with $W_t$ a selection matrix', r'La momentul $t$ păstrăm doar liniile observate: $x_t^o = W_tx_t$, $\Lambda_t = W_t\Lambda$, $\Psi_t = W_t\Psi W_t\'$, cu $W_t$ o matrice de selecție'),
     [T('if nothing is observed, the update step is skipped and the prediction is carried forward', 'dacă nu se observă nimic, pasul de actualizare se omite și predicția se transmite mai departe')]),
    (T(r'\textbf{Ragged edge}: at the end of the sample each series stops at a different month (publication lags); the filter uses whatever is there', r'\textbf{Date incomplete la sfîrșitul eșantionului (ragged edge)}: fiecare serie se oprește în altă lună (întîrzieri de publicare); filtrul folosește ce există'),
     [T('the same mechanism handles series that start late (services confidence from 2002) and quarterly series observed every third month', 'același mecanism tratează seriile care încep tîrziu (încrederea în servicii din 2002) și seriile trimestriale observate în fiecare a treia lună')]),
    T('This is why nowcasting is a filtering problem, and why Chapter 6 develops the filter in full', 'De aceea nowcasting-ul este o problemă de filtrare și de aceea Capitolul 6 dezvoltă filtrul complet')), 'small')

# =============================================================================
# 10. NOWCASTING
# =============================================================================
D.section('Mixed frequencies and nowcasting', 'Frecvențe mixte și nowcasting')

D.frame(T('The nowcasting problem', 'Problema nowcasting-ului'), two(
    ph('reichlin', T('Lucrezia Reichlin, 2013', 'Lucrezia Reichlin, 2013'), h='0.34\\textheight'),
    items((T(r'\textbf{Nowcasting}: estimating the present and the recent past of a low-frequency variable (GDP) from timelier high-frequency data \refGRS, \refBGMR', r'\textbf{Nowcasting}: estimarea prezentului și a trecutului recent al unei variabile de frecvență joasă (PIB) din date de frecvență înaltă, publicate mai repede \refGRS, \refBGMR'),
           [T('backcast (last quarter, not yet published), nowcast (this quarter), forecast (next quarter)', 'backcast (trimestrul trecut, încă nepublicat), nowcast (trimestrul curent), forecast (trimestrul următor)')]),
          (T('Three difficulties: mixed frequencies, many indicators, asynchronous releases (the ragged edge)', 'Trei dificultăți: frecvențe mixte, mulți indicatori, publicări asincrone (ragged edge)'),
           [T('surveys are out at the end of the month; industrial production more than a month later; GDP weeks after the quarter', 'anchetele apar la sfîrșitul lunii; producția industrială după mai mult de o lună; PIB-ul la cîteva săptămîni după trimestru')]),
          T(r'Tools: bridge equations \refBGP, MIDAS \refGSV, \refGSVb, mixed-frequency DFM \refMM, \refBM and mixed-frequency VARs \refSS', r'Instrumente: ecuații punte \refBGP, MIDAS \refGSV, \refGSVb, DFM cu frecvențe mixte \refMM, \refBM și VAR cu frecvențe mixte \refSS')), '0.32', '0.66'), 'footnotesize')

D.frame(T('Bridge equations and MIDAS', 'Ecuații punte și MIDAS'), items(
    (T(r'\textbf{Bridge}: forecast the missing months of each indicator (AR), aggregate to the quarter, regress GDP on the quarterly aggregates \refBGP', r'\textbf{Punte}: prognozăm lunile lipsă ale fiecărui indicator (AR), agregăm la trimestru, regresăm PIB-ul pe agregatele trimestriale \refBGP'),
     [T('simple and transparent; the error of the monthly AR forecasts passes into the nowcast', 'simplă și transparentă; eroarea prognozelor AR lunare trece în nowcast')]),
    (T(r'\textbf{MIDAS} \refGSV: $y_\tau = \beta_0 + \beta_1\sum_{j=0}^{K-1}w_j(\theta)x_{m_\tau - j} + \rho y_{\tau - s} + \varepsilon_\tau$, with the latest monthly value $x_{m_\tau}$', r'\textbf{MIDAS} \refGSV: $y_\tau = \beta_0 + \beta_1\sum_{j=0}^{K-1}w_j(\theta)x_{m_\tau - j} + \rho y_{\tau - s} + \varepsilon_\tau$, cu ultima valoare lunară disponibilă $x_{m_\tau}$'),
     [T(r'$\tau$: the quarter; $m_\tau$: its latest available month; $x$: a monthly indicator with $K$ lags; $w_j(\theta)$: weights summing to 1; $y_{\tau - s}$: lagged GDP growth', r'$\tau$: trimestrul; $m_\tau$: ultima lună disponibilă a lui; $x$: un indicator lunar cu $K$ laguri; $w_j(\theta)$: ponderi cu suma 1; $y_{\tau - s}$: creșterea PIB cu lag'),
      T(r'exponential Almon: $w_j(\theta) = e^{\theta_1j + \theta_2j^2}/\sum_ke^{\theta_1k + \theta_2k^2}$; two parameters for $K$ lags, estimated by NLS', r'Almon exponențial: $w_j(\theta) = e^{\theta_1j + \theta_2j^2}/\sum_ke^{\theta_1k + \theta_2k^2}$; doi parametri pentru $K$ laguri, estimați prin NLS'),
      T(r'MIDAS with leads \refAGK, \refCG: one regression per information set; U-MIDAS leaves $w_j$ unrestricted when $K$ is small \refFMS', r'MIDAS cu valori anticipate \refAGK, \refCG: o regresie pentru fiecare set de informații; U-MIDAS lasă $w_j$ nerestricționate cînd $K$ este mic \refFMS')]),
    T('Neither uses the joint dynamics of the indicators; the DFM does', 'Niciuna nu folosește dinamica comună a indicatorilor; DFM o folosește')), 'small')

D.frame(T('Linking months and quarters: Mariano and Murasawa (2003)', 'Legătura dintre luni și trimestre: Mariano și Murasawa (2003)'), items(
    (T(r'Let $Y_t^M$ be a latent monthly level and the quarterly GDP the 3-month average, observed in the third month', r'Fie $Y_t^M$ un nivel lunar latent, iar PIB-ul trimestrial media pe 3 luni, observată în a treia lună'),
     [T(r'geometric-mean approximation: $\ln Y_t^Q \approx \frac13(\ln Y_t^M + \ln Y_{t-1}^M + \ln Y_{t-2}^M)$', r'aproximarea prin media geometrică: $\ln Y_t^Q \approx \frac13(\ln Y_t^M + \ln Y_{t-1}^M + \ln Y_{t-2}^M)$'),
      T(r'quarterly growth $y_t^Q = \ln Y_t^Q - \ln Y_{t-3}^Q = \frac13(y_t + 2y_{t-1} + 3y_{t-2} + 2y_{t-3} + y_{t-4})$, $y_t$ = monthly growth \refMM', r'creșterea trimestrială $y_t^Q = \ln Y_t^Q - \ln Y_{t-3}^Q = \frac13(y_t + 2y_{t-1} + 3y_{t-2} + 2y_{t-3} + y_{t-4})$, $y_t$ = creșterea lunară \refMM')]),
    (T(r'In the DFM: $y_t^Q = \lambda_y\'\sum_{j=0}^{4}w_jf_{t-j} + e_t^Q$, $w = (1, 2, 3, 2, 1)/3$: the state must hold five lags of $f_t$', r'În DFM: $y_t^Q = \lambda_y\'\sum_{j=0}^{4}w_jf_{t-j} + e_t^Q$, $w = (1, 2, 3, 2, 1)/3$: starea trebuie să conțină cinci laguri ale lui $f_t$'),
     [T(r'$\lambda_y$: the loadings of GDP growth; $w_j$: the Mariano--Murasawa weights; $e_t^Q$: the idiosyncratic error of GDP', r'$\lambda_y$: ponderile factoriale ale creșterii PIB; $w_j$: ponderile Mariano--Murasawa; $e_t^Q$: eroarea idiosincratică a PIB'),
      T('GDP is a monthly variable observed every third month: missing in months 1 and 2 of each quarter', 'PIB-ul este o variabilă lunară observată din trei în trei luni: lipsește în lunile 1 și 2 ale fiecărui trimestru')]),
    T('Seminar 5, A7: the weights by hand', 'Seminarul 5, A7: ponderile de mînă')), 'small')

D.frame(T('Case study: nowcasting Romanian GDP', 'Studiu de caz: nowcasting pentru PIB-ul României'), two(
    ph('ins', T('Institutul Național de Statistică, Bucharest', 'Institutul Național de Statistică, București'), h='0.3\\textheight'),
    items((T(r'Target: q/q growth of real GDP (Eurostat), @{rd.nq} quarters to @{rd.lastq}; monthly panel: @{rd.N} series from 2003 (Eurostat)', r'Ținta: creșterea t/t a PIB-ului real (Eurostat), @{rd.nq} de trimestre pînă în @{rd.lastq}; panelul lunar: @{rd.N} serii din 2003 (Eurostat)'),
           [T('hard data in monthly growth: IP, retail, construction, euro-area IP; change of unemployment; levels of six confidence balances', 'date „hard” ca rate lunare de creștere: IP, comerț, construcții, IP din zona euro; variația șomajului; nivelurile a șase solduri de încredere')]),
          (T('Stylised release lags at the end of each month: surveys 0, unemployment 1, hard data 2 months; GDP 2 months after the quarter', 'Întîrzieri stilizate de publicare la sfîrșitul fiecărei luni: anchete 0, șomaj 1, date hard 2 luni; PIB-ul la 2 luni după trimestru'),
           [T('current-vintage data: pseudo real time (no revisions)', 'datele din ediția curentă: pseudo timp real (fără revizuiri)')]),
          T('Models: AR(1), bridge (IP, retail, ESI), MIDAS (IP, ESI; $K = 6$), DFM with two factors (two-step and EM)', 'Modelele: AR(1), punte (IP, comerț, ESI), MIDAS (IP, ESI; $K = 6$), DFM cu doi factori (în doi pași și EM)')), '0.34', '0.64'), 'footnotesize')

chart(T('Romanian GDP and two monthly indicators', 'PIB-ul României și doi indicatori lunari'), 'ats_ch5_ro_data', 'ATS_ch5_nowcast', [
    T(r'Quarterly GDP growth (2020Q2: @{rd.covid}\%, truncated); IP growth (3-month average) and the standardised ESI', r'Creșterea trimestrială a PIB-ului (T2 2020: @{rd.covid}\%, trunchiată); creșterea IP (medie pe 3 luni) și ESI standardizat')],
    h='0.60\\textheight')

interp(('the Romanian data', 'datelor pentru România'), [
    T('Quarterly growth is volatile: 2009--2012 swings of $\\pm 5$ pp and the 2020 collapse dominate the variance', 'Creșterea trimestrială este volatilă: oscilațiile de $\\pm 5$ pp din 2009--2012 și prăbușirea din 2020 domină varianța'),
    T(r'The ESI (3-month average) has correlation @{rd.cesi} with GDP growth before 2020: informative, far from perfect', r'ESI (medie pe 3 luni) are corelația @{rd.cesi} cu creșterea PIB înainte de 2020: informativ, departe de perfect'),
    T(r'Latest published quarter: @{rd.lastq}, growth @{rd.lasty}\%; the nowcast target is 2026Q3', r'Ultimul trimestru publicat: @{rd.lastq}, creștere @{rd.lasty}\%; ținta nowcast-ului este T3 2026')])

chart(T('MIDAS weights for Romania', 'Ponderile MIDAS pentru România'), 'ats_ch5_midas', 'ATS_ch5_nowcast', [
    T('ADL-MIDAS with exponential Almon weights at the end of the third month of the quarter, 2003--2026', 'ADL-MIDAS cu ponderi Almon exponențiale la sfîrșitul lunii a treia a trimestrului, 2003--2026')],
    h='0.68\\textheight')

interp(('the MIDAS weights', 'ponderilor MIDAS'), [
    T(r'IP: hump-shaped weights peaking at lag @{md.iparg} (@{md.ipmax}): the months of the quarter itself matter, as the Mariano--Murasawa weights predict', r'IP: ponderi în formă de cocoașă, cu maximul la lagul @{md.iparg} (@{md.ipmax}): contează lunile trimestrului însuși, cum prezic ponderile Mariano--Murasawa'),
    T(r'ESI: weight @{md.esi.w0} on the latest month: a level indicator already summarises the past', r'ESI: ponderea @{md.esi.w0} pe ultima lună: un indicator de nivel rezumă deja trecutul'),
    T(r'Lagged GDP growth has coefficient @{md.rho}: the noisy q/q series mean-reverts', r'Creșterea PIB cu lag are coeficientul @{md.rho}: seria zgomotoasă t/t revine la medie')])

D.frame(T('Pseudo-real-time evaluation', 'Evaluarea în pseudo timp real'), items(
    (T(r'For each quarter 2013Q1--2026Q2, nowcasts at the ends of months 1, 2, 3 of the quarter and of month 1 after it', r'Pentru fiecare trimestru T1 2013--T2 2026, nowcast-uri la sfîrșitul lunilor 1, 2, 3 ale trimestrului și la sfîrșitul primei luni de după'),
     [T('all parameters re-estimated on the data available at that date; 2020Q2--Q3 excluded from the RMSE (also reported with them)', 'toți parametrii sînt reestimați pe datele disponibile la acea dată; T2--T3 2020 sînt excluse din RMSE (raportăm și cu ele)')]),
    (T(r'The evaluation sample starts in 2013 because the 2009--2012 swings are larger than any model error; from 2010 the RMSEs rise to about 2 pp for every model', r'Eșantionul de evaluare începe în 2013 pentru că oscilațiile din 2009--2012 sînt mai mari decît orice eroare de model; din 2010 RMSE urcă la aproximativ 2 pp pentru toate modelele'),
     [T(r'standard deviation of the target 2013--2026 (without 2020Q2--Q3): @{nc.sd} pp', r'abaterea standard a țintei 2013--2026 (fără T2--T3 2020): @{nc.sd} pp')]),
    T('Question: does the RMSE fall as the quarter unfolds, and by how much relative to an AR?', 'Întrebarea: scade RMSE pe măsură ce trimestrul avansează și cu cît față de un AR?')), 'small')

chart(T('Nowcast accuracy by information set', 'Acuratețea nowcast-ului în funcție de setul de informații'), 'ats_ch5_nowcast', 'ATS_ch5_nowcast', [
    T('RMSE of the nowcasts of q/q GDP growth, 2013Q1--2026Q2 without 2020Q2--Q3', 'RMSE al nowcast-urilor pentru creșterea t/t a PIB-ului, T1 2013--T2 2026 fără T2--T3 2020')],
    h='0.68\\textheight')

interp(('the nowcast accuracy', 'acurateței nowcast-ului'), [
    T(r'AR: @{nc.ar.M3} pp throughout; DFM: @{nc.dfm.M1} (month 1) to @{nc.dfm.Mp1} (month 1 after); MIDAS: @{nc.md.M1} to @{nc.md.Mp1}', r'AR: @{nc.ar.M3} pp peste tot; DFM: de la @{nc.dfm.M1} (luna 1) la @{nc.dfm.Mp1} (luna 1 de după); MIDAS: de la @{nc.md.M1} la @{nc.md.Mp1}'),
    T(r'Bridge does not beat the AR (@{nc.br.M3}); the EM estimate of the DFM is close to the AR (@{nc.em.M3} at month 3)', r'Ecuația punte nu este superioară modelului AR (@{nc.br.M3}); estimarea EM a DFM este apropiată de AR (@{nc.em.M3} în luna 3)'),
    T(r'Diebold--Mariano DFM against AR at month 3: $t = @{nc.dmt}$, $p = @{nc.dmp}$: the gain is not significant on @{nc.nq} quarters', r'Diebold--Mariano DFM comparat cu AR în luna 3: $t = @{nc.dmt}$, $p = @{nc.dmp}$: cîștigul nu este semnificativ pe @{nc.nq} de trimestre'),
    T(r'With 2020: AR @{nc.cv.ar.M3}, DFM @{nc.cv.dfm.Mp1} at month 1 after: the monthly data catch the collapse, the AR cannot', r'Cu 2020: AR @{nc.cv.ar.M3}, DFM @{nc.cv.dfm.Mp1} în luna 1 de după: datele lunare surprind prăbușirea, AR nu poate')])

D.frame(T('News and revisions: Bańbura and Modugno (2014) (1/2)', 'Știri și revizuiri: Bańbura și Modugno (2014) (1/2)'), items(
    (T(r'The \textbf{news} of a release: $I_j = x_j - \E[x_j\mid\Omega_v]$, not $x_j$ itself', r'\textbf{Știrea} unei publicări: $I_j = x_j - \E[x_j\mid\Omega_v]$, nu $x_j$ însăși'),
     [T(r'$\Omega_v \subset \Omega_{v+1}$: two successive information sets (data vintages)', r'$\Omega_v \subset \Omega_{v+1}$: două seturi de informații succesive (ediții ale datelor)'),
      T(r'$x_j$, $j \in J_{v+1}$: the releases that are new in $\Omega_{v+1}$', r'$x_j$, $j \in J_{v+1}$: publicările noi din $\Omega_{v+1}$')]),
    (T(r'With fixed parameters, the revision is a weighted sum of the news \refBM', r'Cu parametri ficși, revizuirea este o sumă ponderată a știrilor \refBM'),
     [T(r'$\E[y\mid\Omega_{v+1}] - \E[y\mid\Omega_v] = \E[yI\']\E[II\']^{-1}I = \sum_j w_jI_j$', r'$\E[y\mid\Omega_{v+1}] - \E[y\mid\Omega_v] = \E[yI\']\E[II\']^{-1}I = \sum_j w_jI_j$'),
      T(r'$y$: the target (GDP growth); $I$: the vector of news $I_j$; $w_j$: the weight of release $j$', r'$y$: ținta (creșterea PIB); $I$: vectorul știrilor $I_j$; $w_j$: ponderea publicării $j$')]),
    T('A large release that was expected moves nothing; a small surprise in a heavily weighted series moves a lot; correlated releases share their weight', 'O publicare mare, dar așteptată, nu schimbă nimic; o surpriză mică într-o serie cu pondere mare schimbă mult; publicările corelate își împart ponderea')), 'small')

D.frame(T('News and revisions: Bańbura and Modugno (2014) (2/2)', 'Știri și revizuiri: Bańbura și Modugno (2014) (2/2)'), items(
    (T(r'In the DFM: $I_j = \lambda_j\'(f_{t_j} - \hat f_{t_j\mid v}) + e_j$, so $\E[II\'] = H P_{\mid v}H\' + \Psi_J$ and $\E[yI\'] = z_y\'P_{\mid v}H\'$', r'În DFM: $I_j = \lambda_j\'(f_{t_j} - \hat f_{t_j\mid v}) + e_j$, deci $\E[II\'] = H P_{\mid v}H\' + \Psi_J$ și $\E[yI\'] = z_y\'P_{\mid v}H\'$'),
     [T(r'$\lambda_j$: the loadings of release $j$; $t_j$: its reference month; $\hat f_{t_j\mid v}$: the factor estimate given $\Omega_v$; $H$: the stacked $\lambda_j\'$; $\Psi_J$: their idiosyncratic variances; $z_y$: the loading of the target', r'$\lambda_j$: ponderile factoriale ale publicării $j$; $t_j$: luna la care se referă; $\hat f_{t_j\mid v}$: estimația factorului dat fiind $\Omega_v$; $H$: vectorii $\lambda_j\'$ așezați pe linii; $\Psi_J$: varianțele lor idiosincratice; $z_y$: ponderea factorială a țintei'),
      T(r'$P_{\mid v}$: the covariance of the stacked state given $\Omega_v$, from the Kalman filter', r'$P_{\mid v}$: covarianța stării stivuite dat fiind $\Omega_v$, din filtrul Kalman')])), 'small')

chart(T('Nowcasting 2026Q3, and where the revision came from', 'Nowcast pentru T3 2026 și sursa revizuirii'), 'ats_ch5_news', 'ATS_ch5_nowcast', [
    T('Left: nowcasts at the ends of June--September 2026; right: news decomposition of the two-step DFM nowcast between the August and September information sets', 'Stînga: nowcast-uri la sfîrșitul lunilor iunie--septembrie 2026; dreapta: descompunerea în știri a nowcast-ului DFM în doi pași între seturile de informații din august și septembrie')],
    h='0.61\\textheight')

interp(('the news', 'știrilor'), [
    T(r'DFM nowcast of 2026Q3: @{nw.aug.dfm}\% at the end of August, @{nw.sep.dfm}\% at the end of September; the @{nw.n} new releases add up to @{nw.sum} pp exactly', r'Nowcast-ul DFM pentru T3 2026: @{nw.aug.dfm}\% la sfîrșitul lui august, @{nw.sep.dfm}\% la sfîrșitul lui septembrie; cele @{nw.n} publicări noi însumează exact @{nw.sum} pp'),
    T(r'The July IP release was @{nw.ipnews} pp below the model\'s expectation; with weight @{nw.ipw} it cut the nowcast by @{nw.by.ip} pp; ESI @{nw.by.esi}, euro-area IP @{nw.by.ip_ea}', r'Publicarea IP pentru iulie a fost cu @{nw.ipnews} pp sub așteptarea modelului; cu ponderea @{nw.ipw} a redus nowcast-ul cu @{nw.by.ip} pp; ESI @{nw.by.esi}, IP din zona euro @{nw.by.ip_ea}'),
    T(r'Other models at the end of September: EM DFM @{nw.sep.em}\%, bridge @{nw.sep.bridge}\%, AR @{nw.sep.ar}\%: the first official estimate for 2026Q3 will judge them', r'Alte modele la sfîrșitul lui septembrie: DFM EM @{nw.sep.em}\%, punte @{nw.sep.bridge}\%, AR @{nw.sep.ar}\%: prima estimare oficială pentru T3 2026 le va judeca'),
    T('The news decomposition turns a number into a story that a central bank can check release by release', 'Descompunerea în știri transformă o cifră într-o explicație pe care o bancă centrală o poate verifica publicare cu publicare')])

D.recap(('Nowcasting', 'nowcasting'), [
    T('Nowcasting = filtering a mixed-frequency system with a ragged edge', 'Nowcasting = filtrarea unui sistem cu frecvențe mixte și date incomplete la sfîrșitul eșantionului'),
    T('Bridge, MIDAS and DFM share the Mariano--Murasawa link between months and quarters', 'Ecuațiile punte, MIDAS și DFM folosesc aceeași legătură Mariano--Murasawa între luni și trimestre'),
    T('For Romania, monthly data improve the nowcast late in the quarter; the gain is modest and not significant', 'Pentru România, datele lunare îmbunătățesc nowcast-ul spre sfîrșitul trimestrului; cîștigul este modest și nesemnificativ'),
    T('Every revision decomposes exactly into news with fixed parameters', 'Orice revizuire se descompune exact în știri cînd parametrii sînt ficși')])

# =============================================================================
# 11. AI
# =============================================================================
D.section('AI for scientific discovery', 'AI în descoperirea științifică')

D.frame(T('An open question', 'O întrebare deschisă'), items(
    (T('Can a nowcasting model beat a simple AR for Romanian GDP growth in a statistically significant way, and which releases carry the information?', 'Poate un model de nowcasting să fie semnificativ statistic superior unui AR simplu pentru creșterea PIB-ului României și ce publicări poartă informația?'),
     [T(r'formal: $H_0$: equal MSE of the DFM and AR nowcasts at the end of month 3 (Diebold--Mariano, Chapter 1), pre-registered sample, models and lags', r'formal: $H_0$: MSE egal pentru nowcast-urile DFM și AR la sfîrșitul lunii 3 (Diebold--Mariano, Capitolul 1), cu eșantionul, modelele și lagurile preînregistrate'),
      T('falsified by a rejection on quarters the model never saw, with real-time vintages of GDP', 'infirmată de o respingere pe trimestre pe care modelul nu le-a văzut, cu ediții în timp real ale PIB')]),
    (T('Why it matters: fiscal and monetary decisions in 2025--2026 were taken with GDP known only weeks after each quarter', 'Miza: deciziile fiscale și monetare din 2025--2026 s-au luat cu PIB-ul cunoscut la cîteva săptămîni după fiecare trimestru'),
     [T(r'literature to start from: \refGRS, \refBM, \refBGMR, \refGLPb, \refSS', r'literatura de pornire: \refGRS, \refBM, \refBGMR, \refGLPb, \refSS')])), 'small')

D.frame(T('The discovery loop with an AI assistant', 'Bucla de cercetare cu un asistent AI'), items(
    (T('An AI assistant (an LLM such as Claude, ChatGPT, Gemini or Copilot) speeds up each step; Semantic Scholar and Elicit help with the literature', 'Un asistent AI (un LLM precum Claude, ChatGPT, Gemini sau Copilot) accelerează fiecare etapă; Semantic Scholar și Elicit ajută la literatură'),
     [T(r'\textbf{literature}: \aiprompt{List peer-reviewed papers that nowcast GDP of Central and Eastern European countries with factor models or MIDAS; give DOIs.} Then check every DOI on Crossref', r'\textbf{literatura}: \aiprompt{Listează articole recenzate care fac nowcasting pentru PIB-ul țărilor din Europa Centrală și de Est cu modele factoriale sau MIDAS; dă DOI-urile.} Apoi verificați fiecare DOI pe Crossref'),
      T(r'\textbf{hypothesis}: \aiprompt{Which Romanian monthly releases should carry news about GDP, and in which month of the quarter?}', r'\textbf{ipoteza}: \aiprompt{Ce publicări lunare din România ar trebui să conțină știri despre PIB și în ce lună a trimestrului?}'),
      T(r'\textbf{code and replication}: ask for a Kalman filter with missing data, then reproduce a known number first (the news sum of this lecture)', r'\textbf{cod și replicare}: cereți un filtru Kalman cu date lipsă, apoi reproduceți întîi o cifră cunoscută (suma știrilor din acest curs)'),
      T(r'\textbf{robustness and critique}: \aiprompt{Act as a hostile referee of a nowcasting paper: list the ways the pseudo-real-time design could flatter the model.}', r'\textbf{robustețe și critică}: \aiprompt{Joacă rolul unui recenzent ostil al unui articol de nowcasting: enumeră felurile în care designul în pseudo timp real ar putea favoriza artificial modelul.}')]),
    T(r'Report: what was asked, what was kept, what was rejected (AI\_USE.md, AI\_ERRORS.md)', r'Raportul: ce s-a cerut, ce s-a păstrat, ce s-a respins (AI\_USE.md, AI\_ERRORS.md)')), 'footnotesize')

D.frame(T('What the human checks', 'Verificări necesare'), items(
    T('Every reference exists and says what is claimed (DOI resolves, title matches, the result is in the paper)', 'Fiecare referință există și spune ce se afirmă (DOI-ul funcționează, titlul coincide, rezultatul se află în lucrare)'),
    T('The information set at each date contains only data published by then; current-vintage data overstate accuracy', 'Setul de informații la fiecare dată conține doar datele publicate pînă atunci; datele din ediția curentă supraestimează acuratețea'),
    T('Hyperparameters, factors and lags are chosen inside each estimation window, never on the evaluation sample', 'Hiperparametrii, factorii și lagurile se aleg în interiorul fiecărei ferestre de estimare, niciodată pe eșantionul de evaluare'),
    T('The evaluation period and the treatment of 2020 are fixed before the results; all variants are reported', 'Perioada de evaluare și tratarea anului 2020 sînt fixate înaintea rezultatelor; toate variantele sînt raportate'),
    T('A claim of ``better nowcasts\'\' is backed by a test, not by a lower RMSE alone', 'O afirmație despre „nowcast-uri mai bune” se sprijină pe un test, nu doar pe un RMSE mai mic')), 'small')

chart(T('Mini-case: how robust is one ranking?', 'Mini studiu de caz: cît de robustă este o clasificare?'), 'ats_ch5_ai_case', 'ATS_ch5_nowcast', [
    T(r'RMSE of the DFM nowcast relative to the AR at the end of month 3, 2013--2026, across factors, sample start, release lags and the treatment of 2020', r'RMSE al nowcast-ului DFM relativ la AR la sfîrșitul lunii 3, 2013--2026, pentru diferite numere de factori, începuturi ale eșantionului, întîrzieri de publicare și tratări ale anului 2020'),
    T(r'@{ai.n} variants range from @{ai.min} to @{ai.max}; the DFM wins in @{ai.nb} of them: an AI summary that reports the best variant as ``the\'\' result is wrong', r'Cele @{ai.n} variante variază între @{ai.min} și @{ai.max}; DFM este superior în @{ai.nb} dintre ele: un rezumat AI care raportează cea mai bună variantă drept „rezultatul” greșește')],
    h='0.55\\textheight')

D.frame(T('Project idea', 'Idee de proiect'), items(
    (T(r'\textbf{A real-time nowcasting model for Romanian GDP}: replicate first, then extend', r'\textbf{Un model de nowcasting în timp real pentru PIB-ul României}: întîi replicare, apoi extindere'),
     [T(r'replicate: the news decomposition of this lecture (@{nw.sum} pp between August and September 2026) and the BGR table for 1971--2003', r'replicați: descompunerea în știri din acest curs (@{nw.sum} pp între august și septembrie 2026) și tabelul BGR pentru 1971--2003'),
      T('extend: real release dates (INS calendar), GDP vintages saved from now on, blocks of factors for hard and soft data, a mixed-frequency BVAR, density nowcasts', 'extindeți: datele reale de publicare (calendarul INS), edițiile PIB salvate de acum înainte, blocuri de factori pentru date hard și soft, un BVAR cu frecvențe mixte, nowcast-uri de densitate'),
      T('pre-register: target, quarters, models, information sets, the treatment of 2020 and the Diebold--Mariano test', 'preînregistrați: ținta, trimestrele, modelele, seturile de informații, tratarea anului 2020 și testul Diebold--Mariano')]),
    T(r'Deliverables follow the course rules: repository, report, AI\_USE.md, AI\_ERRORS.md, oral defence', r'Livrabilele urmează regulile cursului: repository, raport, AI\_USE.md, AI\_ERRORS.md, susținere orală')), 'small')

# =============================================================================
# ÎNCHEIERE
# =============================================================================
D.section('Wrap-up', 'Încheiere')

D.frame(T('Key takeaways', 'Idei de reținut'), items(
    T('Many series and few observations: shrink (priors) or compress (factors)', 'Multe serii și puține observații: strîngeți (distribuții a priori) sau comprimați (factori)'),
    T('The Minnesota prior in conjugate form gives closed-form posteriors, exact draws and a marginal likelihood that chooses the shrinkage', 'Distribuția Minnesota în formă conjugată dă distribuții a posteriori închise, extrageri exacte și o verosimilitate marginală care alege shrinkage-ul'),
    T('Bigger systems need tighter priors; then they forecast better and give more plausible responses', 'Sistemele mai mari cer distribuții mai strînse; atunci prognozează mai bine și dau răspunsuri mai plauzibile'),
    T('Principal components estimate the factor space; Bai--Ng chooses its dimension; FAVAR and DFM put it to work', 'Componentele principale estimează spațiul factorilor; Bai--Ng îi alege dimensiunea; FAVAR și DFM îl folosesc'),
    T('Nowcasting is Kalman filtering with a ragged edge; every revision is a sum of news', 'Nowcasting-ul este filtrare Kalman cu date incomplete la sfîrșitul eșantionului; orice revizuire este o sumă de știri')), 'small')

D.frame(T('Self-assessment', 'Autoevaluare'), cols(
    block(T('Questions', 'Întrebări'), items(
        T(r'What happens to the Minnesota posterior mean when $\lambda \to 0$?', r'Ce se întîmplă cu media a posteriori Minnesota cînd $\lambda \to 0$?'),
        T(r'Why does the natural conjugate prior force $\vartheta = 1$?', r'De ce impune distribuția natural conjugată $\vartheta = 1$?'),
        T('Which prior allows cointegration: sum-of-coefficients or initial observation?', 'Ce distribuție permite cointegrarea: suma coeficienților sau observația inițială?'),
        T('Why can PCA identify only the factor space?', 'De ce poate identifica PCA doar spațiul factorilor?'),
        T('Why is a large but expected release not news?', 'De ce o publicare mare, dar așteptată, nu este o știre?'))),
    block(T('Next: Chapter 6', 'Urmează: Capitolul 6'), items(
        T('State space models and Bayesian filtering', 'Modele în spațiul stărilor și filtrare bayesiană'),
        T('The Kalman filter and smoother in full; EM, particle filters, stochastic volatility', 'Filtrul și netezitorul Kalman complet; EM, filtre de particule, volatilitate stochastică'))),
    '0.56', '0.40'), 'small')

# =============================================================================
# ANEXA
# =============================================================================
D.section('Appendix', 'Anexă')

D.frame(T('Appendix: the natural conjugate posterior', 'Anexă: distribuția a posteriori natural conjugată'), items(
    T(r'Likelihood: $p(Y\mid B, \Sigma) \propto |\Sigma|^{-T/2}\exp\{-\frac12\mathrm{tr}[\Sigma^{-1}(Y - XB)\'(Y - XB)]\}$', r'Verosimilitatea: $p(Y\mid B, \Sigma) \propto |\Sigma|^{-T/2}\exp\{-\frac12\mathrm{tr}[\Sigma^{-1}(Y - XB)\'(Y - XB)]\}$'),
    T(r'Prior: $|\Sigma|^{-k/2}\exp\{-\frac12\mathrm{tr}[\Sigma^{-1}(B - B_0)\'\Omega_0^{-1}(B - B_0)]\}\times|\Sigma|^{-(d + n + 1)/2}\exp\{-\frac12\mathrm{tr}(\Sigma^{-1}\Psi)\}$', r'Distribuția a priori: $|\Sigma|^{-k/2}\exp\{-\frac12\mathrm{tr}[\Sigma^{-1}(B - B_0)\'\Omega_0^{-1}(B - B_0)]\}\times|\Sigma|^{-(d + n + 1)/2}\exp\{-\frac12\mathrm{tr}(\Sigma^{-1}\Psi)\}$'),
    T(r'Complete the square in $B$: $(Y - XB)\'(Y - XB) + (B - B_0)\'\Omega_0^{-1}(B - B_0) = (B - \bar B)\'\bar\Omega^{-1}(B - \bar B) + \hat U\'\hat U + (\bar B - B_0)\'\Omega_0^{-1}(\bar B - B_0)$', r'Completăm pătratul în $B$: $(Y - XB)\'(Y - XB) + (B - B_0)\'\Omega_0^{-1}(B - B_0) = (B - \bar B)\'\bar\Omega^{-1}(B - \bar B) + \hat U\'\hat U + (\bar B - B_0)\'\Omega_0^{-1}(\bar B - B_0)$'),
    T(r'Hence $B\mid\Sigma, Y \sim MN(\bar B, \bar\Omega, \Sigma)$ and $\Sigma\mid Y \sim IW(\bar\Psi, T + d)$: the same families as the prior', r'Deci $B\mid\Sigma, Y \sim MN(\bar B, \bar\Omega, \Sigma)$ și $\Sigma\mid Y \sim IW(\bar\Psi, T + d)$: aceleași familii ca distribuția a priori'),
    T(r'$MN(\bar B, \bar\Omega, \Sigma)$: the matrix normal distribution, i.e.\ $\mathrm{vec}(B) \sim N(\mathrm{vec}(\bar B), \Sigma\otimes\bar\Omega)$', r'$MN(\bar B, \bar\Omega, \Sigma)$: distribuția Normală matriceală, adică $\mathrm{vec}(B) \sim N(\mathrm{vec}(\bar B), \Sigma\otimes\bar\Omega)$')), 'small')

D.frame(T('Appendix: the marginal likelihood in closed form', 'Anexă: verosimilitatea marginală în formă închisă'), items(
    T(r'Integrating $B$ and $\Sigma$ out (the online appendix of GLP): $p(Y) = \pi^{-nT/2}\frac{\Gamma_n(\frac{T + d}2)}{\Gamma_n(\frac d2)}|\Omega_0|^{-\frac n2}|X\'X + \Omega_0^{-1}|^{-\frac n2}|\Psi|^{\frac d2}|\bar\Psi|^{-\frac{T + d}2}$', r'Integrînd după $B$ și $\Sigma$ (anexa online a lucrării GLP): $p(Y) = \pi^{-nT/2}\frac{\Gamma_n(\frac{T + d}2)}{\Gamma_n(\frac d2)}|\Omega_0|^{-\frac n2}|X\'X + \Omega_0^{-1}|^{-\frac n2}|\Psi|^{\frac d2}|\bar\Psi|^{-\frac{T + d}2}$'),
    T(r'$\Gamma_n(a) = \pi^{n(n-1)/4}\prod_{j=1}^n\Gamma(a + (1 - j)/2)$: the multivariate gamma function', r'$\Gamma_n(a) = \pi^{n(n-1)/4}\prod_{j=1}^n\Gamma(a + (1 - j)/2)$: funcția gamma multivariată'),
    T(r'$|\Omega_0|\,|X\'X + \Omega_0^{-1}| = |I + \Omega_0X\'X|$: the complexity penalty, growing with $\lambda$', r'$|\Omega_0|\,|X\'X + \Omega_0^{-1}| = |I + \Omega_0X\'X|$: penalizarea complexității, care crește cu $\lambda$'),
    T(r'$|\bar\Psi|$: the fit term, falling with $\lambda$; the optimum balances the two', r'$|\bar\Psi|$: termenul de potrivire, care scade cu $\lambda$; optimul le echilibrează'),
    T(r'With dummies: $\ln p(Y\mid\gamma) = \ln p(Y, Y_d\mid\gamma) - \ln p(Y_d\mid\gamma)$, each by the formula above', r'Cu observații fictive: $\ln p(Y\mid\gamma) = \ln p(Y, Y_d\mid\gamma) - \ln p(Y_d\mid\gamma)$, fiecare cu formula de mai sus')), 'small')

D.references(bib(), per=12)

if __name__ == '__main__':
    finalize(D.write(V))
