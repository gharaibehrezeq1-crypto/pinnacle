import re
from playwright.sync_api import sync_playwright
def bub(pg): return re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText"))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/index.html#/');pg.evaluate('window.__pnNoHold=true');pg.wait_for_timeout(1000)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock');sessionStorage.setItem('pnbo','1')")
    bad=0
    for ph in ['بدي اشتري ايفون 17 برو ماكس','كمل الطلب','اطلب سامسونج اس 25 الترا','بدي ارينو 16 برو','اشتري اس 26 الترا']:
        pg.evaluate("q=>window.pnBot.final(q)",ph);pg.wait_for_timeout(500)
        has=pg.evaluate("!!document.getElementById('pnform')")
        print(ph,'→ form',has,'|',bub(pg)[:80]);
        if not has: bad+=1; pg.evaluate("location.hash='#/'");continue
        pre=pg.evaluate("document.getElementById('pfn').value")
        # validation
        pg.fill('#pfn','');pg.click('#pfok');e1=pg.inner_text('#pfe')
        pg.fill('#pfn','أحمد خالد');pg.click('#pfok');pg.fill('#pfp','123');pg.click('#pfok');e2=pg.inner_text('#pfe');print('  errs:',e1,'|',e2,'| title:',pg.inner_text('#pft'))
        pg.fill('#pfp','0791234567');pg.click('#pfok');print('  step3 title:',pg.inner_text('#pft'));pg.fill('#pfa','عمان، الجبيهة، شارع الجامعة');pg.click('#pfok');pg.wait_for_timeout(2500)
        print('  form closed:',not pg.evaluate("!!document.getElementById('pnform')"),'| invoice:',pg.evaluate("!!document.getElementById('pcconf')"),'|',bub(pg)[:70])
        if pg.evaluate("!!document.getElementById('pnform')") or not pg.evaluate("!!document.getElementById('pcconf')"): bad+=1
        pg.evaluate("location.hash='#/'");pg.wait_for_timeout(300)
    # cancel
    pg.evaluate("q=>window.pnBot.final(q)",'بدي اشتري ايفون 17');pg.wait_for_timeout(400);pg.click('#pfx');print('cancel ok:',not pg.evaluate("!!document.getElementById('pnform')"))
    # voice fills form
    pg.evaluate("q=>window.pnBot.final(q)",'بدي اشتري ايفون 17');pg.wait_for_timeout(400)
    pg.evaluate("q=>window.pnBot.final(q)",'اسمي سامر العلي ورقمي 0781234567');pg.wait_for_timeout(300)
    print('prefill:',pg.evaluate("[pfn.value,pfp.value,pft.textContent]"))
    pg.screenshot(path='/tmp/t/form.png')
    print('bad',bad,errs);b.close()
