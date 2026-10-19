import re,sys
from playwright.sync_api import sync_playwright
STARTS=['تمم لي عملية الشراء','تمم الشراء','كمل الطلب','خلصلي الطلب','بدي اطلبه','اشتريه','بدي اشتريه','اطلب هذا الجهاز','سجل لي طلب','اتمم عملية الشراء','ابدأ الطلب','بدي اشتري هذا','حطه بالسلة','ضيفه للسلة','بدي اكمل الشراء','يلا اطلب']
PH=['صفر سبعة تسعة واحد اثنين ثلاثة اربعة خمسة ستة سبعة','0791234567','٠٧٩١٢٣٤٥٦٧','079 123 4567','صفر سبعة سبعة صفر صفر واحد اثنين ثلاثة اربعة خمسة','سبعة تسعة واحد اثنين ثلاثة اربعة خمسة ستة سبعة','صفر سبعة ثمانية تمانية تسعة اربعة اربعة اثنين اثنين خمسة','صفر سبعة تسعة ، واحد اثنين ثلاثة ، اربعة خمسة ستة سبعة','07 9 1 2 3 4 5 6 7']
def bub(pg): return re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText"))
bad=0
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    pg.evaluate('window.__pnNoHold=true')
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
    for st in STARTS:
        pg.evaluate("location.hash='#/d/Galaxy%20S25%20Ultra'");pg.wait_for_timeout(900)
        pg.evaluate("window.pnBot.final('الغي')");pg.evaluate("q=>window.pnBot.final(q)",st);pg.wait_for_timeout(300)
        t=bub(pg);ok='اسمك' in t
        if not ok: bad+=1;print('START FAIL',st,'→',t[:90])
    pg.evaluate("window.pnBot.final('الغي')")
    for ph in PH:
        pg.evaluate("location.hash='#/d/Galaxy%20S25%20Ultra'");pg.wait_for_timeout(900)
        for q in ['اطلب','اسمي احمد خالد',ph,'عمان تلاع العلي شارع الجامعة']:
            pg.evaluate("q=>window.pnBot.final(q)",q);pg.wait_for_timeout(300)
        pg.wait_for_timeout(1500)
        body=pg.evaluate("document.body.innerText")
        ok=('0791234567' in body or '0770012345' in body or '0788944225' in body or '0791234567' in body) and 'S25' in body
        t=bub(pg)
        print('PH',ph[:30],'→',('OK' if re.search(r'07\d{8}',body) else 'NO'),t[:70])
        pg.evaluate("window.pnBot.final('الغي')")
    print(errs,bad);b.close()
