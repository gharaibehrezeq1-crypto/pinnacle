import re
from playwright.sync_api import sync_playwright
def txt(pg): return re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText"))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1000)
    pg.evaluate('window.__pnNoHold=true')
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
    pg.evaluate("sessionStorage.setItem('pnbo','1')");pg.wait_for_timeout(500)
    pg.evaluate("q=>window.pnBot.final(q)",'اهم شي عندي التصوير');pg.wait_for_timeout(300)
    def click(q):
        pg.click("#pnbub button[data-q='%s']"%q);pg.wait_for_timeout(300);print('>',q,'\n ',txt(pg))
    click('ميزانيتي لحد 800')
    for q in ['ايفون 17 برو كم كاميرا','شو الوان الجهاز','شفته ارخص بمحل ثاني','ما عجبتني','بدكيش','كم بدو رينو 16 اف']:
        pg.evaluate("q=>window.pnBot.final(q)",q);pg.wait_for_timeout(300);print('>',q,'\n ',txt(pg))
    print(errs);b.close()
