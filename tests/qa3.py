import json,re,sys,itertools
from playwright.sync_api import sync_playwright
D=json.load(open('/tmp/t/dev.json'))
NM={'iPhone 17 Pro':['ايفون 17 برو','آيفون ١٧ برو','ايفون سبعطعش برو','ايفون سبعتاشر برو','iPhone 17 Pro'],
'iPhone 17 Pro Max':['ايفون 17 برو ماكس','آيفون ١٧ برو ماكس','ايفون سبعطعش برو ماكس','ايفون 17 برومكس','iPhone 17 Pro Max'],
'iPhone 17':['ايفون 17','آيفون ١٧','ايفون سبعطعش','ايفون سبعتاشر','iPhone 17'],
'iPhone 18 Pro Max':['ايفون 18 برو ماكس','آيفون ١٨ برو ماكس','ايفون تمنطعش برو ماكس','ايفون ثمانتاشر برو ماكس','iPhone 18 Pro Max'],
'iPhone 18 Pro':['ايفون 18 برو','آيفون ١٨ برو','ايفون تمنطعش برو','ايفون ثمانتاشر برو','iPhone 18 Pro'],
'Galaxy S26 Ultra':['اس 26 الترا','سامسونج اس٢٦ الترا','جالكسي اس ستة وعشرين الترا','سامسونج s26 ultra','Galaxy S26 Ultra'],
'Galaxy S25 Ultra':['اس 25 الترا','سامسونج اس٢٥ ألترا','جالكسي اس خمسة وعشرين الترا','سامسونج s25 ultra','Galaxy S25 Ultra'],
'Reno16 Pro':['رينو 16 برو','اوبو رينو ١٦ برو','رينو ستاشر برو','ريينو 16 برو','Reno 16 Pro'],
'Reno16':['رينو 16','اوبو رينو ١٦','رينو ستاشر','ريينو 16','Reno 16'],
'Reno16 F':['رينو 16 اف','اوبو رينو ١٦ اف','رينو ستاشر اف','ريينو 16 f','Reno 16 F']}
TP={'price':(None,None,['كم سعر {n}','بكم {n}','قديش {n}','{n} بكم دينار','شو سعر {n}','كم ثمن {n}','كم بدو {n}','سعر {n} لو سمحت','بكام {n}','{n} كام سعره','شكد سعر {n}','وش سعر {n}']),
'screen':('الشاشة','الحجم',['كم حجم شاشة {n}','شو مقاس شاشة {n}','قديش الشاشة تبع {n}','كم انش {n}','كم بوصة {n}','ما هو حجم شاشة {n}','شكد حجم شاشة {n}','كام بوصة {n}']),
'hz':('الشاشة','التحديث',['كم هرتز {n}','معدل التحديث {n}','شو الهيرتز بـ {n}','كم هيرتز شاشة {n}','ما هو معدل تحديث {n}']),
'bright':('الشاشة','السطوع',['كم سطوع شاشة {n}','{n} كم نيتس','ما هو سطوع {n}','شو درجة السطوع {n}']),
'battery':('البطارية','السعة',['كم بطارية {n}','شو سعة البطارية {n}','قديش mAh {n}','ما سعة بطارية {n}','كم ملي امبير {n}','بطارية {n} كم','شكد بطارية {n}']),
'charge':('الشحن','الشحن',['كم واط شحن {n}','شو سرعة الشحن {n}','ما هي سرعة شحن {n}','الشحن السريع {n}','كم واط الشاحن {n}']),
'storage':('التخزين','السعات',['كم مساحة {n}','شو سعات التخزين {n}','كم جيجا {n}','ما هي سعات تخزين {n}','شو الستوريج {n}','كم ذاكرة {n}']),
'weight':('التصميم','الوزن',['كم وزن {n}','قديش وزنه {n}','ما وزن {n}','شكد وزن {n}','{n} ثقيل؟ كم وزنه']),
'cpu':('المعالج','المعالج',['شو معالج {n}','ايش البروسيسور {n}','ما هو معالج {n}','{n} على اي شريحة','شو نوع المعالج في {n}','وش معالج {n}']),
'water':('التصميم','مقاومة',['هل {n} ضد الماء','{n} بيتحمل المي','هل {n} يتحمل الغبار والماء','{n} بينزل بالمسبح','{n} مقاوم للماء؟']),
'os':('التصميم','نظام',['شو نظام تشغيل {n}','ما نظام تشغيل {n}','{n} على اي نظام']),
'dims':('التصميم','الأبعاد',['شو ابعاد {n}','كم سماكة {n}','ما هي أبعاد {n}','{n} طوله وعرضه كم']),
'front':('الكاميرا الأمامية','الدقة',['كم ميجا كاميرا السيلفي {n}','الكاميرا الامامية تبع {n}','سيلفي {n} كم ميجا','ما دقة الكاميرا الأمامية في {n}']),
'cam':('الكاميرا الخلفية','الرئيسية',['كم ميجا الكاميرا الرئيسية {n}','شو كاميرا {n}','كاميرات {n} كم','ما دقة الكاميرا الخلفية في {n}'])}
def toks(v):
    return re.findall(r'\d+(?:\.\d+)?',v.replace(',',''))[:1]
cases=[]
for key,names in NM.items():
    d=D[key]
    for tn,(sec,lab,tpl) in TP.items():
        if tn=='price': exp=[d['price'].replace(',','')]
        else:
            exp=None
            for S in d['data']:
                if S['k'].startswith(sec):
                    for r in S['rows']:
                        if lab in r[0]:
                            exp=(re.findall(r'IP\d+K?|One UI|iOS|ColorOS|Android',r[1])[:1] if tn in('water','os') else toks(r[1]));break
                if exp:break
            if not exp:continue
        for nm in names:
            for t in tpl: cases.append((key,tn,t.format(n=nm),exp))
print('cases',len(cases))
js="""cs=>cs.map(c=>{location.hash='#/';window.pnBot.final(c[0]);return document.getElementById('pnbub').innerText.replace(/,/g,'')})"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock');window.__pnNoHold=true")
    fails=[]
    for i in range(0,len(cases),200):
        ch=cases[i:i+200]
        res=pg.evaluate(js,[[c[2]] for c in ch])
        for c,t in zip(ch,res):
            if not all(e in t for e in c[3]):fails.append((c[0],c[1],c[2],c[3],re.sub(r'\s+',' ',t)[:80]))
    b.close()
print(len(cases),len(fails))
for f in fails[:int(sys.argv[1]) if len(sys.argv)>1 else 40]:print(f)
