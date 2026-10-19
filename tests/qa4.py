import json,re,sys,random
from playwright.sync_api import sync_playwright
exec(open('/tmp/t/qa3.py').read().split("def toks")[0].split("D=json.load(open('/tmp/t/dev.json'))")[1])
D=json.load(open('/tmp/t/dev.json'))
def toks(v):
    return re.findall(r'\d+(?:\.\d+)?',v.replace(',',''))[:1]
random.seed(7)
KEYS=list(NM.keys())
BR={'iPhone':['ايفون','آيفون','الايفون','ابل'],'Samsung':['سامسونج','سامسونغ','الجالكسي','جالكسي'],'OPPO':['اوبو','الاوبو','أوبو','رينو']}
BRH={'iPhone':'#/b/0','Samsung':'#/b/1','OPPO':'#/b/2'}
NAVT=['انتقل لصفحة {n}','انتقل الى صفحة {n}','انقلني على صفحة {n}','روح على {n}','وديني على {n}','خذني ل{n}','افتح {n}','افتح لي {n}','ورجيني {n}','بدي اشوف {n}','بدي افتح صفحة {n}','طلعني على {n}','دخلني على {n}','ممكن تفتح {n}','لو سمحت انقلني ل{n}','يلا وديني على {n}','انتقل ل{n} الله يخليك','فوت على صفحة {n}','روح لصفحة {n}','وريني {n}']
def exp_hash(k): return '#/d/'+k.replace(' ','%20')
cases=[]
starts=['#/']+[exp_hash(k) for k in KEYS]+['#/b/0','#/b/1','#/b/2']
# a) device navigation from every start page
for st in starts:
    for k in KEYS:
        for nm in random.sample(NM[k],3):
            for t in random.sample(NAVT,4):
                cases.append(('nav',st,t.format(n=nm),exp_hash(k)))
# b) brand navigation
for st in starts:
    for b,ws in BR.items():
        if b=='OPPO': ws=ws[:3]
        for w in ws:
            for t in random.sample(NAVT,3):
                cases.append(('brand',st,t.format(n=w),BRH[b]))
# c) topic questions with named device asked from another page
for st in random.sample(starts,6):
    for k in KEYS:
        d=D[k]
        for tn,(sec,lab,tpl) in TP.items():
            if tn!='price' and tn not in('battery','charge','storage','weight','cpu'):continue
            if tn=='price': exp=[d['price'].replace(',','')]
            else:
                exp=None
                for S in d['data']:
                    if S['k'].startswith(sec):
                        for r in S['rows']:
                            if lab in r[0]: exp=toks(r[1]);break
                    if exp:break
                if not exp:continue
            for nm in random.sample(NM[k],2):
                t=random.choice(tpl).format(n=nm)
                cases.append(('topic',st,t,exp))
# d) topic without device -> all devices listed (battery/price/screen...)
GEN=['بطارية','كم البطارية','شو سعات البطاريات','كم سعر الاجهزة','الشحن','كم واط الشحن','كم حجم الشاشة','الكاميرا','كم ميجا الكاميرا','المعالج','الوزن','التخزين']
for st in starts:
    for g in GEN: cases.append(('all',st,g,None))
print('cases',len(cases))
js="""cs=>cs.map(c=>{location.hash=c[0];window.pnBot.final(c[1]);return [location.hash,document.getElementById('pnbub').innerText.replace(/,/g,'')]})"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock');window.__pnNoHold=true")
    fails=[];i=0
    while i<len(cases):
        ch=cases[i:i+60];i+=60
        # hash changes are async -> run one by one inside page with awaits
        res=pg.evaluate("""async cs=>{const out=[];for(const c of cs){location.hash=c[0];window.__pnCtxReset();await new Promise(r=>setTimeout(r,25));window.pnBot.final(c[1]);await new Promise(r=>setTimeout(r,30));out.push([location.hash,document.getElementById('pnbub').innerText.replace(/,/g,'')]);}return out}""",[[c[1],c[2]] for c in ch])
        for c,(h,t) in zip(ch,res):
            kind,st,q,ex=c
            if kind in('nav','brand'): ok=(h==ex)
            elif kind=='topic': ok=all(e in t for e in ex)
            else: ok=len(re.findall(r'iPhone \d+|Galaxy S\d+|Reno16',t))>=5
            if not ok: fails.append((kind,st,q,ex,h,re.sub(r'\s+',' ',t)[:70]))
    b.close()
print(len(cases),len(fails))
for f in fails[:int(sys.argv[1]) if len(sys.argv)>1 else 40]:print(f)
