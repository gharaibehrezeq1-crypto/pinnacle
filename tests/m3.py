import re
from playwright.sync_api import sync_playwright
MOCK="window.__recs=[];window.webkitSpeechRecognition=function(){this.start=function(){window.__recs.push(this);setTimeout(()=>this.onstart&&this.onstart(),10);};this.abort=function(){};this.stop=function(){};};window.SpeechRecognition=window.webkitSpeechRecognition;"
def run(choice):
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream']);c=b.new_context(viewport={'width':390,'height':844});pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.add_init_script(MOCK)
        pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(500)
        pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
        pg.wait_for_timeout(4000)
        print(choice,'| prompt:',re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText"))[:90],'| mic before:',pg.evaluate("document.getElementById('pnbot').classList.contains('always')"))
        pg.screenshot(path='/tmp/t/m3.png')
        bb=pg.locator("#pnbub button[data-q='%s']"%choice).bounding_box();pg.mouse.click(bb['x']+10,bb['y']+10);pg.wait_for_timeout(1500)
        print('  mic after:',pg.evaluate("document.getElementById('pnbot').classList.contains('always')"),'recs',pg.evaluate("window.__recs.length"),'|',re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText"))[:60])
        if choice=='__micyes':
            pg.reload();pg.wait_for_timeout(4500);print('  reload: mic on:',pg.evaluate("document.getElementById('pnbot').classList.contains('always')"),'| prompt shown (expect True):',pg.evaluate("!!document.querySelector(\"#pnbub button[data-q='__micyes']\")"))
        print(errs);b.close()
run('__micyes');run('__micno')
