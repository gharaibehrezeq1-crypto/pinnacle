import sys,itertools
from playwright.sync_api import sync_playwright
IP={'17':['17','١٧','سبعتاشر','سبعطعش','سبعتعش','سبعطاش','سبعتشر','سبعة عشر','سبع عشر','سفنتين'],'18':['18','١٨','تمنتاشر','تمانتاشر','تمنطعش','ثمانتاشر','ثمنطعش','تمنطاش','ثمانية عشر','ثمان عشر']}
PRO=['','برو','بروو','برو ماكس','بروماكس','برومكس','pro','pro max','بُرو']
BR=['ايفون','آيفون','ايفن','اي فون','iPhone','ابل ايفون','ايفون رقم']
cases=[]
def exp(n,v):
    t='M' if ('ماكس' in v or 'max' in v or 'مكس' in v) else ('P' if v else '')
    return 'iPhone %s%s'%(n,{'':'','P':' Pro','M':' Pro Max'}[t])
for n,vs in IP.items():
    for v in PRO:
        for b in BR:
            for nv in vs[:]:
                cases.append((f'{b} {nv} {v}'.strip(),exp(n,v)))
# samsung
S={'25':['25','٢٥','خمسة وعشرين','خمسه وعشرين','خمس وعشرين','خمسة و عشرين'],'26':['26','٢٦','ستة وعشرين','ستة و عشرين','ست وعشرين','ستة وعشرين']}
SB=['اس','إس','S','s','es','سامسونج اس','سامسونغ اس','سامسنج اس','جالكسي اس','جلاكسي اس','galaxy s','samsung s','اس اس','ايس']
UL=['الترا','ألترا','ولترا','ultra','Ultra','اولترا','التراا']
for n,vs in S.items():
    for b in SB:
        for nv in vs:
            for u in UL:
                cases.append((f'{b} {nv} {u}','Galaxy S%s Ultra'%n))
    for nv in vs[:3]:
        for u in UL[:3]: cases.append((f'{u} {nv}','Galaxy S%s Ultra'%n))
# reno
R=['16','١٦','ستاشر','ستطعش','ستة عشر','ست عشر','ستعش']
RB=['رينو','اوبو رينو','رنو','reno','Reno','ريينو','اوبّو رينو']
for b in RB:
    for nv in R:
        for v,e in [('',''),('برو',' Pro'),('pro',' Pro'),('اف',' F'),('f',' F'),('F',' F')]:
            cases.append((f'{b} {nv} {v}'.strip(),'Reno16'+e))
fails=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto('http://localhost:8765/index.html#/');pg.wait_for_timeout(1500)
    res=pg.evaluate("c=>c.map(x=>{var r=window.pnBot.find(x[0]);return [x[0],x[1],r.keys.join(','),r.miss.map(m=>m.label).join(',')]})",[list(c) for c in cases])
    for t,e,k,m in res:
        if e=='iPhone 18': continue
        if k!=e: fails.append((t,e,k,m))
    b.close()
print(len(cases),len(fails))
for f in fails[:int(sys.argv[1]) if len(sys.argv)>1 else 60]:print(f)
