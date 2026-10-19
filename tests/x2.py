from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();c=b.new_context(viewport={'width':390,'height':844});pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(800)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')");pg.wait_for_timeout(500)
    d=lambda s:pg.evaluate("getComputedStyle(document.querySelector('%s')).display"%s)
    print('start bot',d('#pnbot'),'rev',d('.pnrev'))
    pg.click('.pnx');pg.wait_for_timeout(300);print('after X bot',d('#pnbot'),'rev',d('.pnrev'));pg.screenshot(path='/tmp/t/x2.png')
    pg.reload();pg.wait_for_timeout(700);print('reload bot',d('#pnbot'),'rev',d('.pnrev'))
    pg.click('.pnrev');pg.wait_for_timeout(400);print('after face bot',d('#pnbot'),'rev',d('.pnrev'),pg.evaluate("localStorage.getItem('pnoff')"))
    pg.evaluate("window.pnBot.final('كم سعر اس 26 الترا')");pg.wait_for_timeout(300);print('works:',pg.evaluate("document.getElementById('pnbub').innerText")[:40])
    print(errs);b.close()
