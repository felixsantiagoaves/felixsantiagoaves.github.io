import os
from playwright.sync_api import sync_playwright
os.makedirs('fr',exist_ok=True)
FPS=24;DUR=15
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1280,'height':720})
    pg.goto('http://localhost:8123/index.html');pg.wait_for_function('window.ready===true',timeout=60000)
    for f in range(FPS*DUR):
        pg.evaluate(f'setT({f/FPS})');pg.screenshot(path='fr/f%04d.png'%f)
    pg2=b.new_page(viewport={'width':1920,'height':1080})
    pg2.goto('http://localhost:8123/index.html');pg2.wait_for_function('window.ready===true',timeout=60000)
    for n,t in (('mockup-portada',1.0),('mockup-enero',5.0),('mockup-trasera',14.5)):
        pg2.evaluate(f'setT({t})');pg2.screenshot(path=n+'.png')
    b.close()
