# ATS build pipeline

How the materials of *Analiza avansată a seriilor de timp și previziune / Advanced Time Series Analysis and Forecasting* (ATS; master's programme Applied Statistics and Data Science, year 1, semester 2, 7 ECTS) are built. The pipeline is copied from the TSA course (bachelor, the prerequisite), which took it from SFM and MFM: same slide design, same bilingual generators, same data and notebook rules. Run every command from the repository root. The chapter rules are in `tools/HOUSE_RULES.md`.

This repository is local only (branch `main`, no remote). The future public repository is `danpele/Advanced-Time-Series`, with the site `https://danpele.github.io/Advanced-Time-Series/`; all Colab, raw-data, Quantlet and chapter links already point there.

## Layout

| Path | Content |
|---|---|
| `index.html`, `index_ro.html` | Site shell (EN, RO). Everything else comes from `assets/`. |
| `assets/site.js`, `assets/site.css` | Rendering and quiz engine (shared with the MFM, SFM and TSA sites). Reads `window.ATS_DATA`, `window.ATS_CONFIG`, `window.ATS_LANG`. |
| `assets/config.js` | Google client ID (shared "MFM Quiz Login" client), Apps Script URLs, instructor e-mails. Values starting with `YOUR_` count as not configured. |
| `assets/course-data.js` | Course facts, chapters 0–16 with their links, project, AI policy, resources, bibliography. |
| `assets/quizzes/<id>.js` | Quiz bank of one chapter (`window.ATS_DATA.quizzes['<id>']`, `draw: 20`), created with the chapter. |
| `latex/preamble.tex` | Shared Beamer preamble: logos, `\quantlet`, `\atsquantlet`, `\colaburl`, `\nb`, `\itemsize`, `\imgcredit`, `\imgcap`, `\ifsolutions`/`\solonly`/`\propsub`, the appendix and chapter-link macros. |
| `latex/ats_chapters.py` | Chapter registry (TITLES as in `assets/course-data.js`, `SELF_STUDY = {16}`) and the file-naming scheme. |
| `latex/ats_build.py` | Common generator framework: `⟦EN‖RO⟧` text, `@{key}` numbers, the `Deck` class, compilation. |
| `latex/build_chapterN.py`, `latex/build_seminarN.py` | One bilingual generator per deck. |
| `latex/acronyms.py`, `_acr_scan.py`, `acronyms_extra/chN.py` | Acronym glossary, inserted after the title page. |
| `latex/appendix_links.py` | Appendix buttons and back-buttons; "Chapter N" becomes a link to the ATS PDF on the site (built chapters only); "TSA, Chapter N" / "Chapter N of TSA" and "MFM, Chapter N" / "Chapter N of MFM" link to the sister courses (`EXTERNAL`). |
| `data/market/*.csv`, `data/manifest.csv` | Daily market data from EODHD, saved once (91 series, copied from TSA, ending 18.09.2026). |
| `Quantlets/common/ats_data.py` | Data loader: local `data/market` or the raw GitHub URL of this repository; `read_omi` for the Oxford-Man realized library (local copy, otherwise downloaded from the Internet Archive); BNR reference rate, FRED, Eurostat, ECB Data Portal (online, no key); statsmodels data sets. |
| `Quantlets/common/ats_style.py` | Chart style: transparent background, legend below the plot, course palette, no grey; `check_no_grey`; `save_fig` sizes each slide chart for its box on the slides (text at least 6 pt there) and darkens pale confidence bands. |
| `Quantlets/common/chart_boxes.json`, `tools/chart_boxes.py` | The box (width, height) of every chart on the slides, read from the decks; re-run `python3 tools/chart_boxes.py` after changing the size of a chart in a generator, then redraw the chart. |
| `Quantlets/common/ats_quantlets.py` | Quantlet builder: `Metainfo.txt` plus a self-contained Colab notebook plus charts. |
| `Quantlets/Ch_NN/` | Per chapter: `generate_all_charts.py`, `build_quantlets.py`, `ATS_chN_*` folders. |
| `notebooks/ats_notebook.py`, `notebooks/build_notebooks_chN.py` | Notebook builders. Output is English only, in `notebooks/EN/`. |
| `notebooks/add_colab_banner.py` | Adds the "Save a copy in Drive" banner and the optional Drive-save cell (`MyDrive/ATS/Chapter_N`). |
| `notebooks/split_seminar_notebooks.py`, `split_quantlet_seminars.py` | Split each seminar notebook and Quantlet into a public student version and a private instructor version (`CHAPTERS = range(17)`). |
| `photos/`, `photos/CREDITS.md` | Images with verified free licences and their credits. |
| `tools/HOUSE_RULES.md` | Rules for every chapter (level, language, slides, data, charts, seminars, quizzes, evaluation). |

### File names

Slugs are derived from the chapter titles. To list them all, run `python3 latex/ats_chapters.py`.

| Material | Path |
|---|---|
| Lecture, EN | `EN/Courses/chapterN_<slug_en>.pdf` |
| Lecture, RO | `RO/Cursuri/capitolN_<slug_ro>.pdf` |
| Seminar, EN | `EN/Seminars/seminarN_<slug_en>.pdf` (instructor version: `…_solutions.pdf`, git-ignored) |
| Seminar, RO | `RO/Seminarii/seminarN_<slug_ro>_ro.pdf` (instructor version: `…_solutions.pdf`, git-ignored) |
| Notebooks | `notebooks/EN/chapterN_lecture_notebook.ipynb`, `notebooks/EN/chapterN_seminar_notebook.ipynb` |
| Site | `https://danpele.github.io/Advanced-Time-Series/<path>` |

## Chapters

| N | id | Title (RO) | Status |
|---|---|---|---|
| 0 | refresher | Recapitulare și inferență pentru date dependente | organisation part built (pipeline check); content to follow |
| 1 | forecast-evaluation | Evaluarea prognozelor, reguli de scor și combinarea prognozelor | in preparation |
| 2 | breaks-nonlinear | Rupturi structurale și modele neliniare | in preparation |
| 3 | svar-lp | Modele VAR structurale și proiecții locale | in preparation |
| 4 | cointegration-panel | Cointegrare: VECM, ARDL și date panel | in preparation |
| 5 | bvar-nowcasting | Modele VAR bayesiene, modele factoriale și nowcasting | in preparation |
| 6 | state-space | Modele în spațiul stărilor și filtrare bayesiană | in preparation |
| 7 | regime-switching | Modele cu schimbare de regim | in preparation |
| 8 | volatility | Modelarea avansată a volatilității: măsuri realizate, HAR și GARCH multivariat | in preparation |
| 9 | var-es | VaR, ES și backtesting: elicitabilitate, funcții de scor și riscul de model | in preparation |
| 10 | long-memory | Memorie lungă și volatilitate rugoasă | in preparation |
| 11 | spectral-wavelet | Analiză spectrală și analiză wavelet | in preparation |
| 12 | ml-dl | Machine learning și deep learning pentru serii de timp | in preparation |
| 13 | foundation-conformal | Foundation models și predicție conformală | in preparation |
| 14 | causal | Inferență cauzală pentru serii de timp | in preparation |
| 15 | review | Recapitulare și susținerea proiectelor | in preparation |
| 16 | bubbles | Rădăcini explozive și bule speculative (studiu individual) | in preparation |

## Building a chapter (commands in order)

```bash
# 1. charts, tables and numbers (Quantlets/Ch_NN)
python3 Quantlets/Ch_NN/generate_all_charts.py
python3 Quantlets/Ch_NN/seminarN.py                    # if the chapter has seminar computations
#    (after changing the size of a chart on a slide: python3 tools/chart_boxes.py, then step 1 again)
# 2. Quantlet folders (Metainfo.txt + Colab notebook + charts)
python3 Quantlets/Ch_NN/build_quantlets.py
# 3. decks EN + RO (each generator also runs latex/acronyms.py N, which runs appendix_links.py)
python3 latex/build_chapterN.py
python3 latex/build_seminarN.py                        # also writes the *_solutions.tex wrappers
# 4. compile: pdflatex twice per deck (and per _solutions wrapper); prints errors and overfull vbox
python3 latex/ats_build.py compile N
# 5. notebooks (EN only), then execute them
python3 notebooks/build_notebooks_chN.py
jupyter nbconvert --to notebook --execute --inplace notebooks/EN/chapterN_lecture_notebook.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/EN/chapterN_seminar_notebook.ipynb
# 6. Colab banner + Drive-save cell (idempotent)
python3 notebooks/add_colab_banner.py
# 7. seminars: student version public, full version private (../instructor/Quantlets/Ch_NN)
python3 notebooks/split_seminar_notebooks.py N         # also runs split_quantlet_seminars.py N
python3 notebooks/split_quantlet_seminars.py --write-gitignore   # private answer charts -> .gitignore block
python3 notebooks/split_quantlet_seminars.py --check   # nothing private in public folders or in git
```

Re-run step 7 after **any** `build_quantlets.py`, because that script rewrites the full seminar notebooks.

Before publishing a chapter, in `assets/course-data.js` replace `SOON()` by the real links (`pdf(...)`, `nb(..., NB_LECT)`, `nb(..., NB_SEM)`, `ql('Quantlets/Ch_NN')`), create `assets/quizzes/<id>.js` (24 questions) and add its `<script>` to both `index*.html`, then bump the `?v=` cache keys.

## Writing a generator

`latex/ats_build.py` has a worked example in its docstring; `latex/build_chapter0.py` is the smallest complete generator. The rules:

- Write all text as `⟦english||română⟧`.
- Never type numbers by hand. Use `@{key}` with `Values.put(key, x, decimals)`.
- In RO decks, decimal points become commas and „de” is added after numerals of 20 and above.
- Lecture helpers: `D.section`, `D.frame`, `D.chart` (chart plus Quantlet link), `D.recap`, `D.references`.
- Seminar helpers: `D.solved`, `D.proposed` (solution only with `\solutionstrue`), `D.task`, `D.frame(..., instructor_only=True)`.
- Images: `photo(file, caption, url, credit)` adds a visible credit; record the licence in `photos/CREDITS.md`. Citations are `\href` links to the DOI.
- Chapter-specific acronyms go in `latex/acronyms_extra/chN.py`; the glossary step must print no `NOT IN DICTIONARY`.
- Each lecture ends with the section "AI în descoperirea științifică" / "AI for scientific discovery".

## Data

- Daily market data from EODHD, saved once in `data/market`. Do not call any API with a key.
- Indices, FX, crypto and yields use `close`; ETFs and stocks use `adjusted_close`. Weekend quotes and holiday-filled closes are dropped, except for crypto. Annualise with the actual observation frequency.
- EUR/RON is the official BNR reference rate (`ats_data.load_close('eurron')`).
- Online, no key: `ats_data.read_fred('UNRATE')`, `ats_data.read_eurostat('namq_10_gdp', 'Q.CLV10_MEUR.SCA.B1GQ.RO')`, `ats_data.read_ecb('EXR', 'M.USD.EUR.SP00.A')`, BNR; statsmodels data sets with `ats_data.load_statsmodels(...)`.
- Realised measures: `data/realized` holds our own daily measures of Bitcoin and Ether from Binance one-minute and one-second prices (`Quantlets/Ch_08/prepare_realized_data.py`).
- The Oxford-Man Institute's realized library v0.3 (Heber, Lunde, Shephard and Sheppard 2009; chapters 8, 10, 12, 13) is not redistributed: `ats_data.read_omi()` reads the local copy `data/realized/omi_realized_library_v03.csv` if present (git-ignored, instructor's machine only), otherwise it downloads the last public file (28 February 2022) from the Internet Archive, extracts the six indices and caches them in the temporary folder. Never read the library file directly; cite it with its version number.

## Private material (never committed)

- Instructor versions of seminars (`*_solutions.*`), `instructor/`, oral-defence notes, grades and rosters.
- Everything listed in the "PRIVATE MATERIAL" block of `.gitignore`: student projects, the unpublished manuscript and department decks, unpublished book chapters, third-party solutions and books, unpublished research output.

## Chapter 0 (pipeline check)

```bash
python3 latex/build_chapter0.py && python3 latex/ats_build.py compile 0
```

## Note for chapter authors

- Citation macro names cannot contain digits (`\refJoh88` breaks LaTeX); use letters only (`\refJohA`).
- Seminar sources (`latex/build_seminar*.py`, `notebooks/build_notebooks_ch*.py`, seminar `.tex`) contain the instructor-only solutions and are git-ignored: never commit them.
