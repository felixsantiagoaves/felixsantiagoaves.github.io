#!/usr/bin/env python3
"""Genera las tiras del calendario 2027 (21 x 9,9 cm) y las renderiza a PNG.
Uso: python3 gen_calendario.py <carpeta_fotos> <carpeta_salida> [meses...]
Las fotos (jpg) están en la PC de Felix, no en el repo. Config en MESES/PORTADA abajo."""
import sys, os, calendar, base64
PORTADA = ('cuervillo_de_canada', 'Cuervillo de cañada')
# mes -> (archivo, nombre, lado de la foto, feriados)
MESES = {
 1:('picaflor_verde','Picaflor verde','L',[1]),
}
NOM = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{background:#fff;font-family:Lato,Helvetica,Arial,sans-serif;color:#2a1f14}
.s{width:210mm;height:99mm;background:#ede0d4;position:relative;overflow:hidden}
.ph{position:absolute;top:0;height:99mm;background-size:cover;background-position:center}
.a{font-size:2.6mm;letter-spacing:1.2mm;color:#7f5539;font-weight:700}h1{font:italic 700 13mm/1 'Playfair Display',Georgia,serif;color:#414833}
table{border-collapse:collapse;table-layout:fixed;width:100%}th{font-size:2.3mm;color:#7f5539;padding-bottom:1mm}
td{height:6.4mm;text-align:center;font-size:3mm;font-weight:700;color:#414833;border-top:.25mm solid #c4a882}td.d{color:#7f5539}
td.f{background:#414833;color:#ede0d4;border-radius:50%}.pie{font:italic 3mm 'Playfair Display',Georgia,serif;color:#5c3d28;margin-top:3mm}
.ig{font-size:2.3mm;letter-spacing:.4mm;color:#7f5539;margin-top:1mm}
.cv{position:absolute;inset:0;background-size:cover;background-position:center}.cv:after{content:"";position:absolute;inset:0;background:linear-gradient(270deg,#000b 0,#0000 55%)}
.ct{position:absolute;right:10mm;bottom:10mm;color:#fff;text-align:right}.ct h1{color:#fff;font-size:17mm}.ct .a{color:#f0e2d0}.ct p{font:italic 3.4mm Georgia,serif;margin-top:2mm}"""
def img(d, n):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(d, n + '.jpg'), 'rb').read()).decode()
def mes(d, m):
    f, nom, lado, fer = MESES[m]
    cal = calendar.Calendar(0).monthdayscalendar(2027, m)
    rows = ''.join('<tr>' + ''.join('<td></td>' if x == 0 else '<td class="%s">%d</td>' % (('f' if x in fer else 'd' if i == 6 else ''), x) for i, x in enumerate(w)) + '</tr>' for w in cal)
    th = ''.join('<th>%s</th>' % c for c in 'LMMJVSD')
    foto = 'left:0' if lado == 'L' else 'right:0'
    panel = 'left:144mm' if lado == 'L' else 'left:6mm'
    return ('<div class="s"><div class="ph" style="%s;width:137mm;background-image:url(%s)"></div>'
            '<div style="position:absolute;%s;top:6mm;width:60mm"><span class="a">2027</span><h1>%s</h1><div style="height:3mm"></div>'
            '<table><tr>%s</tr>%s</table><div class="pie">%s</div><div class="ig">@felix_santiago_aves</div></div></div>') % (foto, img(d, f), panel, NOM[m-1], th, rows, nom)
def portada(d):
    return ('<div class="s"><div class="cv" style="background-image:url(%s)"></div><div class="ct"><span class="a">CALENDARIO DE ESCRITORIO</span>'
            '<h1>Aves 2027</h1><p>%s · @felix_santiago_aves</p></div></div>') % (img(d, PORTADA[0]), PORTADA[1])
if __name__ == '__main__':
    fotos, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    pags = {'portada': portada(fotos)}
    for m in (map(int, sys.argv[3:]) if len(sys.argv) > 3 else MESES):
        pags['%02d-%s' % (m, NOM[m-1].lower())] = mes(fotos, m)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 374}, device_scale_factor=2)
        for k, h in pags.items():
            pg.set_content('<meta charset="utf-8"><style>%s</style>%s' % (CSS, h)); pg.wait_for_timeout(300)
            pg.locator('.s').screenshot(path=os.path.join(out, k + '.png')); print(k)
        b.close()
