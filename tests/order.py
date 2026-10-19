import sys,re
from playwright.sync_api import sync_playwright
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+F+'#/'); pg.wait_for_timeout(1500)
    pg.evaluate('window.__pnNoHold=true')
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
    bub=lambda:re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText"))
    def say(q,w=400):
        pg.evaluate("q=>window.pnBot.final(q)",q); pg.wait_for_timeout(w); print('»',q,'→',bub())
    say('بدي ايفون 16 اسمي احمد')
    say('بدي ايفون 17 برو ماكس اسمي أحمد خالد عنواني عمان تلاع العلي شارع الجامعة قديش سعره',300)
    say('0791234567')
    say('كم الشحن',300)
    pg.wait_for_timeout(3500); print(bub()); print(pg.evaluate("location.hash"))
    print('receipt:',pg.evaluate("(document.querySelector('.pcpaper')||{}).innerText"))
    pg.screenshot(path='/tmp/t/order.png')
    # navigation
    say('افتح لي سامسونج اس 26',3500); print(pg.evaluate("location.hash"))
    say('وريني الكاميرا',1500); pg.screenshot(path='/tmp/t/nav2.png')
    say('رجوع',500);print(pg.evaluate("location.hash"))
    print(errs); b.close()
