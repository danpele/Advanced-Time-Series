"""Detectarea acronimelor dintr-un deck (folosit de latex/acronyms.py; ATS, preluat din MFM)."""
import re, sys, json
TICK=set("""NOT AND OR AAPL MSFT NVDA USD EUR RON JPY GBP CHF CNY BTC ETH SOL USDT SPY RSP QQQ TLT GLD IBIT TVBETETF BTBETRETF GDAXI DAX XAU XAUUSD TLV SNP BRD TGN FP SNG SNN EL DIGI TEL H2O XLB XLE XLF XLI XLK XLP XLU XLV XLY XLRE XLC MTUM VLUE QUAL USMV IWM IWD IWF EEM EFA ATB ONE TTS TRP SFG AQ PE CFH M GSPC BTC-USD ETH-USD README PDF PNG CSV XML JSON URL HTTP HTTPS DOI ISBN EN RO OK I II III IV V VI VII VIII IX X XI XII DNA""".split())
def body(tex):
    s=open(tex,encoding='utf-8').read()
    i=s.find(r'\begin{document}'); s=s[i:] if i>=0 else s
    for kw in [r'\section{References}', r'\section{Bibliografie}', r'\section{Referințe}', r'\section{Bibliography}']:
        j=s.find(kw)
        if j>0: s=s[:j]
    s=re.sub(r'(?<!\\)%.*','',s)
    s=re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}','',s,flags=re.S)
    s=re.sub(r'\\\[.*?\\\]','',s,flags=re.S)
    s=re.sub(r'\\begin\{(equation|align|gather)\*?\}.*?\\end\{\1\*?\}','',s,flags=re.S)
    s=s.replace(r'\$',' ')  # dollar sign in text, not a math delimiter
    s=re.sub(r'\$[^$]*\$','',s)
    s=re.sub(r'\\imgcredit\{[^}]*\}\{[^}]*\}','',s)  # imgcredit2: both arguments (author names are not acronyms)
    s=re.sub(r'\\(href|url|texttt|quantletleft|atsquantlet|quantlet|imgcredit|includegraphics|citeAFML|colaburl|qlurl|cite|citep|citet|bibitem|label|ref|hyperlink|hypertarget|atsapplink|atschlink|atschlinkt)(\[[^\]]*\])?\{[^}]*\}','',s)
    s=re.sub(r'\\[a-zA-Z]+\*?','',s)
    return s
def scan(tex):
    b=body(tex); out=[]
    for m in re.finditer(r'(?<![\w/.\-])([A-Z][A-Z0-9]*[A-Z0-9](?:-[A-Z0-9]+)*)(?![\w])',b):
        a=m.group(1)
        if a in TICK or a in out or re.fullmatch(r'[A-Z]\d+|\d+|X{0,3}(IX|IV|V?I{0,3})',a): continue
        out.append(a)
    return out
