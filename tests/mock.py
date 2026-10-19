import re
from playwright.sync_api import sync_playwright
MOCK="""
window.__recs=[];
window.webkitSpeechRecognition=function(){this.start=function(){window.__recs.push(this);setTimeout(()=>this.onstart&&this.onstart(),10);};this.abort=function(){};this.stop=function(){};};
window.SpeechRecognition=window.webkitSpeechRecognition;
"""
def res(final,txt,idx=0):
    return "(function(){var r=window.__recs[window.__recs.length-1];var o=[{0:{transcript:%r},isFinal:%s,length:1}];o.length=1;r.onresult({resultIndex:0,results:o});})()"%(txt,'true' if final else 'false')
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream']);pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script(MOCK)
    pg.goto('http://localhost:8765/index.html#/d/iPhone%2017%20Pro%20Max');pg.wait_for_timeout(800)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock');sessionStorage.setItem('pnbo','1')")
    pg.mouse.click(200,300);pg.wait_for_timeout(1500)
    print('engine recs started:',pg.evaluate("window.__recs.length"))
    # partial then stall >1.6s then final longer
    pg.evaluate(res(False,'انتقل الى صفحة'));pg.wait_for_timeout(1900)
    print('after partial:',pg.evaluate("location.hash"))
    pg.evaluate(res(True,'انتقل الى صفحة اس 25 الترا'));pg.wait_for_timeout(600)
    print('after final:',pg.evaluate("location.hash"),'|',re.sub(r'\s+',' ',pg.evaluate("document.getElementById('pnbub').innerText"))[:80])
    print(errs);b.close()
