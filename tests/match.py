from playwright.sync_api import sync_playwright
import json
cases=[
("افتح لي شاشة الاس 25 الترا","Galaxy S25 Ultra"),
("اس 25 الترا شو سعرها","Galaxy S25 Ultra"),
("إس خمسة وعشرين ألترا","Galaxy S25 Ultra"),
("S25 Ultra camera","Galaxy S25 Ultra"),
("الايفون سبعطعش برو ماكس بكم","iPhone 17 Pro Max"),
("ايفون ١٧ برو ماكس قديش","iPhone 17 Pro Max"),
("كم بطارية الاس ٢٦ الترا","Galaxy S26 Ultra"),
("سامسونج اس 26 الترا","Galaxy S26 Ultra"),
("سامسونج جالكسي اس25","Galaxy S25 Ultra"),
("اس25 الترا","Galaxy S25 Ultra"),
("ولترا 25 شو معالجه","Galaxy S25 Ultra"),
("ultra 26","Galaxy S26 Ultra"),
("ايفون 18 برو ماكس","iPhone 18 Pro Max"),
("الـ 17 برو","iPhone 17 Pro"),
("17 برو ماكس","iPhone 17 Pro Max"),
("ايفون سبعتاشر","iPhone 17"),
("ايفون ستاشر برو","MISS"),
("رينو 16 برو","Reno16 Pro"),
("رينو ستطعش اف","Reno16 F"),
("اس 24 الترا","MISS"),
("ما فيش اس 24 الترا","MISS"),
("ايفون 16 برو","MISS"),
("شو سعر الايفون 17","iPhone 17"),
("قارن بين اس 25 الترا و اس 26 الترا","Galaxy S25 Ultra,Galaxy S26 Ultra"),
("قارن بين ايفون 17 برو وايفون 18 برو","iPhone 17 Pro,iPhone 18 Pro"),
]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    pg.evaluate("var i=document.getElementById('intro');i&&i.remove();document.body.classList.remove('lock')")
    keys=pg.evaluate("Object.keys(window.pnDEV)");print(keys)
    bad=0
    for t,exp in cases:
        r=pg.evaluate("t=>{var f=window.pnBot.find(t);return {k:f.keys,m:f.miss.map(x=>x.label)}}",t)
        got=",".join(r['k']) if r['k'] else ("MISS" if r['m'] else "NONE:"+",".join(r['m']))
        ok=(got==exp) or (exp=="MISS" and r['m'])
        if not ok:bad+=1
        print('OK ' if ok else 'BAD',t,'->',got,r['m'])
    print('bad',bad,errs);b.close()
