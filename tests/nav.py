import json,sys
from playwright.sync_api import sync_playwright
exec(open('/tmp/t/qa3.py',encoding='utf8').read().split("TP={")[0].split("D=json")[0])
D=json.load(open('/tmp/t/dev.json'))
src=open('/tmp/t/qa3.py',encoding='utf8').read()
NM=eval(src[src.index("NM={")+3:src.index("TP={")])
VERBS=['انقلني على صفحة {n}','خذني على {n}','خذني لصفحة {n}','وديني على {n}','روح على {n}','افتح {n}','افتح لي {n}','افتحلي صفحة {n}','وريني {n}','ورجيني {n}','اعرض {n}','اعرض لي {n}','بدي اشوف {n}','بدي افتح {n}','بدي اشوف صفحة {n}','ادخلني على {n}','ادخل على {n}','حولني على {n}','نقلني الى {n}','طلعني على {n}','اذهب الى {n}','انتقل الى صفحة {n}','ممكن تفتح {n}','لو سمحت افتح لي {n}','show me {n}','open {n}','go to {n}','بدي اشوف مواصفات {n}','شوف لي {n}','صفحة {n}']
cases=[]
for key,names in NM.items():
    for nm in names[:2]:
        for v in VERBS: cases.append((key,v.format(n=nm)))
js="""async cs=>{var o=[];for(var c of cs){location.hash='#/';window.pnBot.final(c[1]);await new Promise(r=>setTimeout(r,120));o.push(decodeURIComponent(location.hash));}return o}"""
fails=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
    for i in range(0,len(cases),100):
        ch=cases[i:i+100];res=pg.evaluate(js,[[c[0],c[1]] for c in ch])
        for c,h in zip(ch,res):
            if h!='#/d/'+c[0]: fails.append((c[0],c[1],h))
    b.close()
print(len(cases),len(fails))
for f in fails[:int(sys.argv[1]) if len(sys.argv)>1 else 40]:print(f)
