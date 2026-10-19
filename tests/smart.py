import sys,re
from playwright.sync_api import sync_playwright
F=sys.argv[1]
Q=[('#/b/2','كم كاميرا ايفون 17 برو ماكس'),('#/b/0','شو سعر سامسونج اس 26'),('#/d/Galaxy%20S26%20Ultra','شو الشاشة'),('#/d/Galaxy%20S26%20Ultra','هل بتنزل بالمي'),('#/d/Galaxy%20S26%20Ultra','وين بصور فيديو'),
('#/d/Galaxy%20S26%20Ultra','شو القلم'),('#/','شو الاجهزة اللي عندكم'),('#/','ارخص جهاز'),('#/','اغلى جهاز'),('#/','شو عندك بأقل من 800 دينار'),('#/','شو عندكم سامسونج'),
('#/','قارن بين ايفون 17 برو وايفون 17 برو ماكس بالبطارية'),('#/','ايفون 16 كم سعره'),('#/','كيف التوصيل'),('#/','الدفع كيف'),('#/','في ضمان؟'),('#/d/iPhone%2017%20Pro%20Max','شو الاتصال 5g'),('#/d/iPhone%2017%20Pro%20Max','شو الشريحة'),
('#/d/iPhone%2017%20Pro%20Max','ايش المعالج'),('#/d/iPhone%2017%20Pro%20Max','وزنه'),('#/d/iPhone%2017%20Pro%20Max','ايفون 17'),('#/b/1','ايش اللون')]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+F); pg.wait_for_timeout(1500)
    pg.evaluate('window.__pnNoHold=true')
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
    for h,q in Q:
        pg.evaluate("h=>location.hash=h",h); pg.wait_for_timeout(300)
        pg.evaluate("q=>window.pnBot.final(q)",q); pg.wait_for_timeout(200)
        print(q,'→',re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText")).replace('\n',' / '))
    print(errs); b.close()
