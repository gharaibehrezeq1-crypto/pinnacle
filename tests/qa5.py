import re,sys,itertools
from playwright.sync_api import sync_playwright
G={
'disc':(['خصم','بدي خصم','اخر سعر','شو اخر سعر','كم اخر سعر','نزلي السعر','نزل السعر شوي','فصل شوي','في عرض','في خصم','عندكم عروض','بتعمل خصم','بدي سعر احسن','سعر خاص','اقل سعر ممكن','تخفيض','هات اخر كلمه','فصال'],'بخصوص السعر|خيارات تناسبك|الميزانية'),
'inst':(['بدي اقسط','في تقسيط','بتقسطوا','تقسيط','اقساط','ممكن دفعات','الدفع كيف','طريقه الدفع','كيف ادفع','بتقبلوا فيزا','بتقبلوا كريدت','الدفع كاش'],'طريقة الدفع|الدفع عند الاستلام'),
'warr':(['في كفاله','كم الكفاله','فيه ضمان','الضمان كم سنه','عندكم ضمان','في كفاله على الجهاز','الكفاله كم'],'الكفالة والضمان'),
'nomo':(['ما معي كل المبلغ','ما معي مصاري','مش معي كفايه','ميزانيتي ضيقه','ما بكفي المبلغ','ما عندي مصاري'],'لا مشكلة'),
'gift':(['بدي جهاز لبنتي','بدي جهاز لابني','بدي اشتري لامي','بدي هديه لزوجتي','بدي جهاز لاخوي','بدي اشتري لابوي','هدية لصديقي','بدي جهاز لخطيبتي'],'هدية موفقة'),
'free':(['بتعطيني هديه','في هديه معه','بتهديني اشي','اكسسوار مجاني','كفر مجاني','في هديه مع الجهاز'],'الهدايا والعروض'),
'trade':(['بدي ابدل جهازي القديم','جهازي القديم بتاخذوه','بتشتروا جهازي القديم','بدل جهازي'],'الجهاز القديم'),
'think':(['بدي افكر','رح افكر','لسا بفكر','ما قررت','بفكر وبرجع','مش متاكد','مش مقتنع'],'سبب|ما الذي|ما زلت'),
'trust':(['الجهاز اصلي','هل انتم موثوقين','مضمون','في نصب','موقع امن','مقلد','في احتيال'],'الوكيل الرسمي|اشترِ بأمان|بأمان'),
'comp':(['لقيته ارخص بمحل ثاني','شفته ارخص عند غيركم','محل ثاني اوفر','ارخص عند حدا ثاني'],'قارن براحتك'),
'lost':(['محتار','مش عارف اي واحد اشتري','ساعدني اختار','انصحني','شو تنصحني','اختار لي جهاز','شو الافضل'],'يسعدني|ما أهم'),
'buy':(['بدي اشتري ايفون 17','اطلب اس 26 الترا','بدي رينو 16 برو','خلص اشتريه رينو 16'],'اكتب بياناتك'),
}
PRE=['','يا سهل ','طيب ','يعني ','والله ','لو سمحت ','هاي ','اسمع ']
SUF=['',' الله يخليك',' يا زلمة',' بالله']
cases=[]
for g,(bs,exp) in G.items():
    for b in bs:
        for pr in PRE:
            for sf in SUF:
                cases.append((g,pr+b+sf,exp))
print('cases',len(cases))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock');window.__pnNoHold=true")
    fails=[];i=0
    while i<len(cases):
        ch=cases[i:i+80];i+=80
        res=pg.evaluate("""async cs=>{const out=[];for(const c of cs){location.hash='#/';document.getElementById('pnform')&&document.getElementById('pnform').remove();window.pnBot.final('الغي');await new Promise(r=>setTimeout(r,8));window.pnBot.final(c);await new Promise(r=>setTimeout(r,20));out.push(document.getElementById('pnbub').innerText);}return out}""",[c[1] for c in ch])
        for c,t in zip(ch,res):
            t=re.sub(r'\s+',' ',t)
            if not re.search(c[2],t): fails.append((c[0],c[1],t[:90]))
    b.close()
print(len(cases),len(fails))
import collections
cn=collections.Counter(f[0] for f in fails);print(cn)
seen=set()
for f in fails:
    if f[1].strip() in seen:continue
    seen.add(f[1].strip())
    if len(seen)>int(sys.argv[1] if len(sys.argv)>1 else 30):break
    print(f)
