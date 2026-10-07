# Acronime specifice Capitolului 4 ATS (Cointegrare: VECM, ARDL și date panel)
# format: acronim -> (forma de origine, limba de origine, traducere RO, traducere EN)
# OVERRIDE_CH (optional): acronim -> tuplu, sens diferit doar in acest capitol.
EXTRA = {
    'BUBOR': ('Budapest Interbank Offered Rate', 'en', 'rata dobînzii interbancare de pe piața din Budapesta', None),
    'VAT': ('Value Added Tax', 'en', 'taxa pe valoarea adăugată', None),
    'TVA': ('Taxa pe valoarea adăugată', 'ro', None, 'value added tax'),
    'ECM': ('Error Correction Model', 'en', 'model cu corecția erorii', None),
    'MG': ('Mean Group (estimator)', 'en', 'estimatorul mean group (media estimațiilor pe unități)', None),
    'PMG': ('Pooled Mean Group (estimator)', 'en', 'estimatorul pooled mean group (termen lung comun, termen scurt eterogen)', None),
    'CCE': ('Common Correlated Effects (estimator)', 'en', 'estimatorul efectelor comune corelate', None),
    'CCEMG': ('Common Correlated Effects Mean Group', 'en', 'estimatorul mean group cu efecte comune corelate', None),
    'CS-ARDL': ('Cross-Sectionally augmented ARDL', 'en', 'ARDL augmentat cu medii pe secțiune', None),
    'LLC': ('Levin–Lin–Chu (panel unit-root test)', 'en', 'testul Levin–Lin–Chu de rădăcină unitară în panel', None),
    'IPS': ('Im–Pesaran–Shin (panel unit-root test)', 'en', 'testul Im–Pesaran–Shin de rădăcină unitară în panel', None),
    'CIPS': ('Cross-sectionally augmented IPS (test)', 'en', 'testul IPS augmentat cu medii pe secțiune', None),
    'CADF': ('Cross-sectionally augmented Dickey–Fuller (regression)', 'en', 'regresia Dickey–Fuller augmentată cu medii pe secțiune', None),
    'FMOLS': ('Fully Modified Ordinary Least Squares', 'en', 'metoda celor mai mici pătrate complet modificată', None),
    'DOLS': ('Dynamic Ordinary Least Squares', 'en', 'metoda celor mai mici pătrate dinamică (cu avansuri și laguri)', None),
    'FE': ('Fixed Effects', 'en', 'efecte fixe', None),
    'RA': ('Reinsel–Ahn (small-sample correction)', 'en', 'corecția Reinsel–Ahn pentru eșantioane mici', None),
    'KPSW': ('King–Plosser–Stock–Watson (common-trends model, 1991)', 'en', 'modelul cu trenduri comune King–Plosser–Stock–Watson (1991)', None),
    'PSS': ('Pesaran–Shin–Smith', 'en', 'Pesaran–Shin–Smith', None),
    'NARDL': ('Nonlinear AutoRegressive Distributed Lag (model)', 'en', 'model autoregresiv neliniar cu laguri distribuite', None),
    'NPISH': ('Non-Profit Institutions Serving Households', 'en', 'instituții fără scop lucrativ în serviciul gospodăriilor', None),
    'EU-27': ('the 27 member states of the European Union', 'en', 'cele 27 de state membre ale Uniunii Europene', None),
    'UE-27': ('cele 27 de state membre ale Uniunii Europene', 'ro', None, 'the 27 member states of the European Union'),
    'ECE': ('Europa Centrală și de Est', 'ro', None, 'Central and Eastern Europe'),
    'OCDE': ('Organizația pentru Cooperare și Dezvoltare Economică', 'ro', None, 'Organisation for Economic Co-operation and Development'),
}
OVERRIDE_CH = {
    'CD': ('Cross-section Dependence (test of Pesaran)', 'en', 'testul Pesaran de dependență între unități', None),
}
