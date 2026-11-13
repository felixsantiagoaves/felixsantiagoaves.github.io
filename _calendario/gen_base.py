# Hoja A4 de la base triangular (prisma): caras de 95 mm + solapa 12 mm. uso: CAL_FUENTES=... python3 gen_base.py salida.pdf
import sys,os,base64,importlib.util
from playwright.sync_api import sync_playwright
here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location('g',here+'/gen_calendario.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
F=95; FL=12  # cara 95 mm, solapa 12 mm (12+3*95=297)
CR='#f3ece1'; VD='#2f3a1e'
html=f'''<!doctype html><meta charset=utf-8><style>{g.fuentes_css()}
@page{{size:210mm 297mm;margin:0}}*{{box-sizing:border-box;margin:0}}
body{{width:210mm;height:297mm;background:{CR};position:relative;font-family:Corm,serif;color:{VD};-webkit-print-color-adjust:exact}}
.p{{position:absolute;left:0;width:210mm;height:{F}mm}}
.fl{{position:absolute;left:0;top:0;width:210mm;height:{FL}mm;background:#e4d9c6}}
.t{{position:absolute;font:600 2.6mm 'Corm';letter-spacing:.35em;text-transform:uppercase;opacity:.75}}
.ln{{position:absolute;left:0;width:210mm;border-top:.25mm dashed {VD}}}
.ln.m{{border-top:.25mm dashed #9a3a22}}
.lo{{width:12mm;height:18mm;background:{VD};-webkit-mask:url({g.logo()}) center/contain no-repeat;mask:url({g.logo()}) center/contain no-repeat}}
.pf{{position:absolute;left:0;width:210mm;border-top:.25mm solid #9a3a22}}
.h{{position:absolute;width:3mm;height:3mm;border:.3mm solid #9a3a22;border-radius:50%}}
</style>
<div class=fl></div>
<div class=t style="top:{FL/2-1.3}mm;left:14mm">Solapa · pegar por dentro, sobre el borde inferior de la base</div>
<div class=ln style="top:{FL}mm"></div>
<div class=p style="top:{FL}mm"></div>
<div class=t style="top:{FL+14}mm;left:14mm">Cara frontal · acá van las hojas</div>
<div class=pf style="top:{FL+6}mm;border-top-style:dotted"></div>
<div class=t style="top:{FL+8.5}mm;left:14mm;color:#9a3a22;font-size:2.2mm;letter-spacing:.2em;opacity:1">Línea de perforado (6 mm del borde) · ajustar al anillo</div>
<div class=ln style="top:{FL+F}mm"></div>
<div class=p style="top:{FL+F}mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2.2mm">
<div class=lo></div><div style="font:600 5.2mm Corm;letter-spacing:.4em;text-indent:.4em">FÉLIX SANTIAGO · AVES</div>
<div style="font:italic 500 5mm Corm">Calendario de escritorio 2027</div>
<div style="font:italic 400 4mm Corm;opacity:.85">felixsantiago.com.ar</div></div>
<div class=t style="top:{FL+F+2}mm;left:14mm">Cara trasera</div>
<div class=ln style="top:{FL+2*F}mm"></div>
<div class=t style="top:{FL+2*F+2}mm;left:14mm">Base · apoya sobre el escritorio</div>
<div class=t style="bottom:3mm;left:14mm;font-size:2.2mm;letter-spacing:.2em">Guías: línea punteada = doblar (hundir con regla antes) · imprimir A4 al 100 % · cartulina 250–300 g</div>
'''
# cuatro marcas de perforado sugeridas (centradas): posiciones ejemplo
for x in (30,105-1.5,180-3): html+=f'<div class=h style="left:{x}mm;top:{FL+6-1.5}mm"></div>'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.set_content(html);pg.wait_for_timeout(300)
    pg.pdf(path=sys.argv[1],width='210mm',height='297mm',print_background=True);b.close()
