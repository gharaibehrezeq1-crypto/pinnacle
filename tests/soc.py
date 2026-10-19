import re,sys
from playwright.sync_api import sync_playwright
Q=sys.argv[1:] or ['السلام عليكم','مرحبا','هلا سهل','كيفك','شو اخبارك','صباح الخير','مساء الخير','شكرا','يعطيك العافية','مع السلامة','مين انت','شو بتعرف تعمل','غالي كتير','بفكر','محتار','انصحني','مضمون؟','في خصم؟','اخر سعر','هل الجهاز اصلي','ميزانيتي محدودة','اهم شي عندي التصوير','اهم شي عندي البطارية','اهم شي عندي السعر','اهم شي عندي الاداء','ليش ما اشتريت','لا شكرا','ايفون 17 برو','شكرا']
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    pg.evaluate('window.__pnNoHold=true')
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
    for q in Q:
        pg.evaluate("q=>window.pnBot.final(q)",q);pg.wait_for_timeout(200)
        print(q,'→',re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText")))
    print(errs);pg.screenshot(path='/tmp/t/s1.png');b.close()
