# Acronime specifice Capitolului 11 ATS (Analiză spectrală și analiză wavelet)
# format: acronim -> (forma de origine, limba de origine, traducere RO, traducere EN)
# OVERRIDE_CH: acronim -> tuplu, sens diferit doar in acest capitol (BC, CF, BK, CFR, LA au alt sens in alte capitole).
EXTRA = {
    'MODWT': ('Maximal Overlap Discrete Wavelet Transform', 'en', 'transformata wavelet discretă cu suprapunere maximă', None),
    'DWT': ('Discrete Wavelet Transform', 'en', 'transformata wavelet discretă', None),
    'CWT': ('Continuous Wavelet Transform', 'en', 'transformata wavelet continuă', None),
    'MRA': ('MultiResolution Analysis', 'en', 'analiza multirezoluție', None),
    'COI': ('Cone Of Influence (of a wavelet transform)', 'en', 'conul de influență al transformatei wavelet', None),
    'DPSS': ('Discrete Prolate Spheroidal Sequences (Slepian tapers)', 'en', 'șiruri sferoidale prolate discrete (taper-ele Slepian)', None),
    'VARMA': ('Vector AutoRegressive Moving Average (model)', 'en', 'model vectorial autoregresiv cu medie mobilă', None),
    'SVD': ('Singular Value Decomposition', 'en', 'descompunerea valorilor singulare', None),
    'SSA': ('Singular Spectrum Analysis', 'en', 'analiza spectrului singular', None),
    'DCC-GARCH': ('Dynamic Conditional Correlation GARCH', 'en', 'model GARCH cu corelație condiționată dinamică', None),
    'BG': ('Bulgaria (Eurostat country code)', 'en', 'Bulgaria (codul de țară Eurostat)', None),
    'CZ': ('Czechia (Eurostat country code)', 'en', 'Cehia (codul de țară Eurostat)', None),
    'HU': ('Hungary (Eurostat country code)', 'en', 'Ungaria (codul de țară Eurostat)', None),
    'PL': ('Poland (Eurostat country code)', 'en', 'Polonia (codul de țară Eurostat)', None),
    'SK': ('Slovakia (Eurostat country code)', 'en', 'Slovacia (codul de țară Eurostat)', None),
    'EA20': ('Euro Area, 20 member states (Eurostat code)', 'en', 'zona euro cu 20 de state membre (codul Eurostat)', None),
    'GS10': ('10-year US Treasury constant-maturity yield (FRED code)', 'en', 'randamentul titlurilor de stat americane la 10 ani (codul FRED)', None),
    'MCO': ('Metoda celor mai mici pătrate obișnuite', 'ro', None, 'ordinary least squares'),
}
# acronyms.py evaluates A[key] eagerly in entry(), so an OVERRIDE_CH key must also exist in A: the same tuples are
# registered in EXTRA (setdefault: they never replace a meaning defined elsewhere) and in OVERRIDE_CH (this chapter).
OVERRIDE_CH = {
    'BC': ('Breitung–Candelon (frequency-domain causality test)', 'en', 'testul de cauzalitate în domeniul frecvenței Breitung–Candelon', None),
    'BK': ('Baxter–King (band-pass filter)', 'en', 'filtrul trece-bandă Baxter–King', None),
    'CF': ('Christiano–Fitzgerald (band-pass filter)', 'en', 'filtrul trece-bandă Christiano–Fitzgerald', None),
    'CFR': ('Croux, Forni and Reichlin (2001)', 'en', 'Croux, Forni și Reichlin (2001)', None),
    'LA': ('Least Asymmetric (Daubechies wavelet filter)', 'en', 'filtrul wavelet Daubechies cel mai puțin asimetric', None),
}
EXTRA.update({k: v for k, v in OVERRIDE_CH.items()})
