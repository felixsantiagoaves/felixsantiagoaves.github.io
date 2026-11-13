#!/usr/bin/env python3
"""Genera las tiras del calendario 2027 (21 x 9,9 cm) y las renderiza a PNG.
Uso: python3 gen_calendario.py <carpeta_fotos> <carpeta_salida> [meses...]
Las fotos (jpg) están en la PC de Felix, no en el repo. Config en MESES/PORTADA abajo."""
import sys, os, calendar, base64
PORTADA = 'cuervillo_de_canada'
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logo-nav.png')
# archivo -> (nombre común, nombre científico, lugar, fecha de la foto). Datos de registros.json / avistamientos (eBird).
AVES = {
 'cuervillo_de_canada':('Cuervillo de cañada','Plegadis chihi','Laguna Rivero, Alcira Gigena','31/10/2026'),
 'chingolo':('Chingolo','Zonotrichia capensis','POR CONFIRMAR','02/01/2026'),
 'chimango':('Chimango','Daptrius chimango','UNRC, Río Cuarto','27/12/2025'),
 'picaflor_verde':('Picaflor común','Chlorostilbon lucidus','POR CONFIRMAR','16/03/2026'),
 'gallineta_pico_pintado':('Gallineta pico pintado','Pardirallus sanguinolentus','Laguna Los Medanitos, Paso del Durazno','27/06/2026'),
 'tachuri_siete_colores':('Tachurí sietecolores','Tachuris rubrigastra','Laguna Rivero, Alcira Gigena','31/10/2026'),
 'tacuarita_azul':('Tacuarita azul','Polioptila dumicola','POR CONFIRMAR (Villa de las Rosas o Dique La Viña)','12/06/2026'),
 'aguila_mora':('Águila mora','Geranoaetus melanoleucus','Laguna Seca, Suco','27/07/2026'),
 'varillero_congo':('Varillero congo','Chrysomus ruficapillus','Laguna Rivero, Alcira Gigena','31/10/2026'),
 'churrinche':('Churrinche','Pyrocephalus rubinus','Río Cuarto','30/09/2026'),
 'jote_cabeza_negra':('Jote cabeza negra','Coragyps atratus','Reserva Hídrica Achiras','10/10/2026'),
 'pico_de_plata':('Pico de plata','Hymenops perspicillatus','Laguna Rivero, Alcira Gigena','25/10/2026'),
 'maca_cara_blanca':('Macá cara blanca','Rollandia rolland','Laguna Rivero, Alcira Gigena','31/10/2026'),
 'ciguena_americana':('Cigüeña americana','Ciconia maguari','Laguna Rivero, Alcira Gigena','25/10/2026'),
}
# mes -> (archivo, lado de la foto L/R). Feriados nacionales 2027 abajo. Queda afuera: cigüeña americana.
MESES = {1:('chingolo','L'),2:('chimango','R'),3:('picaflor_verde','L'),4:('gallineta_pico_pintado','R'),5:('tachuri_siete_colores','L'),6:('tacuarita_azul','R'),
 7:('aguila_mora','L'),8:('varillero_congo','R'),9:('churrinche','L'),10:('jote_cabeza_negra','R'),11:('pico_de_plata','L'),12:('maca_cara_blanca','R')}
FERIADOS = {1:[1],2:[8,9],3:[24,26],4:[2],5:[1,25],6:[20,21],7:[9],8:[16],10:[11],11:[20],12:[8,25]}
NOM = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{background:#fff;font-family:Lato,Helvetica,Arial,sans-serif;color:#2a1f14}
.s{width:210mm;height:99mm;background:#ede0d4;position:relative;overflow:hidden}
.ph{position:absolute;top:0;height:99mm;background-size:cover;background-position:center}
.a{font-size:2.4mm;letter-spacing:1.2mm;color:#7f5539;font-weight:700}h1{font:italic 700 11mm/1 'Playfair Display',Georgia,serif;color:#414833}
.p{position:absolute;top:5mm;bottom:4mm;width:60mm;display:flex;flex-direction:column}
table{border-collapse:collapse;table-layout:fixed;width:100%;margin-top:2.5mm}th{font-size:2.1mm;color:#7f5539;padding-bottom:.8mm}
td{height:5.6mm;text-align:center;font-size:2.9mm;font-weight:700;color:#414833;border-top:.25mm solid #c4a882}td.d{color:#7f5539}
td.f{background:#414833;color:#ede0d4;border-radius:50%}
.n{font:italic 700 4mm 'Playfair Display',Georgia,serif;color:#414833;margin-top:2.5mm}.sc{font:italic 2.7mm Georgia,serif;color:#5c3d28}.lg{font-size:2.3mm;color:#7f5539;margin-top:.6mm;line-height:1.25}
.ft{margin-top:auto;display:flex;align-items:center;gap:2mm;border-top:.25mm solid #c4a882;padding-top:1.6mm}
.lo{width:5.5mm;height:8mm;background:#414833;-webkit-mask:url(LOGO) center/contain no-repeat;mask:url(LOGO) center/contain no-repeat}
.ft b{font-size:2.5mm;color:#414833;display:block}.ft i{font-style:normal;font-size:2.2mm;color:#7f5539}
.cv{position:absolute;background-size:100% 100%}.cv2{position:absolute;inset:0;background:linear-gradient(270deg,#000b 0,#0000 52%)}
.ct{position:absolute;right:10mm;bottom:9mm;color:#fff;text-align:right}.ct h1{color:#fff;font-size:17mm}.ct .a{color:#f0e2d0}.ct p{font:italic 3.4mm Georgia,serif;margin-top:2mm}.ct small{display:block;font-size:2.6mm;margin-top:1mm;opacity:.9}"""
def img(d, n):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(d, n + '.jpg'), 'rb').read()).decode()
def logo():
    return 'data:image/png;base64,' + base64.b64encode(open(LOGO, 'rb').read()).decode()
def mes(d, m):
    f, lado = MESES[m]; nom, cie, lug, fec = AVES[f]; fer = FERIADOS.get(m, [])
    cal = calendar.Calendar(0).monthdayscalendar(2027, m)
    rows = ''.join('<tr>' + ''.join('<td></td>' if x == 0 else '<td class="%s">%d</td>' % (('f' if x in fer else 'd' if i == 6 else ''), x) for i, x in enumerate(w)) + '</tr>' for w in cal)
    th = ''.join('<th>%s</th>' % c for c in 'LMMJVSD')
    foto = 'left:0' if lado == 'L' else 'right:0'
    panel = 'left:144mm' if lado == 'L' else 'left:6mm'
    return ('<div class="s"><div class="ph" style="%s;width:137mm;background-image:url(%s)"></div>'
            '<div class="p" style="%s"><span class="a">2027</span><h1>%s</h1><table><tr>%s</tr>%s</table>'
            '<div class="n">%s</div><div class="sc">%s</div><div class="lg">%s · %s</div>'
            '<div class="ft"><div class="lo"></div><div><b>felixsantiago.com.ar</b><i>@felix_santiago_aves</i></div></div></div></div>') % (foto, img(d, f), panel, NOM[m-1], th, rows, nom, cie, lug, fec)
def portada(d):
    nom, cie, lug, fec = AVES[PORTADA]
    # foto ampliada y corrida para que el ave quede a la izquierda y el texto a la derecha
    return ('<div class="s"><div class="cv" style="background-image:url(%s);width:280mm;height:187mm;left:-70mm;top:-47mm"></div><div class="cv2"></div><div class="ct">'
            '<span class="a">CALENDARIO DE ESCRITORIO</span><h1>Aves 2027</h1><p>%s · <i>%s</i></p><small>%s · %s</small>'
            '<small>felixsantiago.com.ar · @felix_santiago_aves</small></div></div>') % (img(d, PORTADA), nom, cie, lug, fec)
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
            pg.set_content('<meta charset="utf-8"><style>%s</style>%s' % (CSS.replace('LOGO', logo()), h)); pg.wait_for_timeout(300)
            pg.locator('.s').screenshot(path=os.path.join(out, k + '.png')); print(k)
        b.close()
