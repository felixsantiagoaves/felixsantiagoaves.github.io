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
 'chingolo':('Chingolo','Zonotrichia capensis','Casa, Río Cuarto','02/01/2026'),
 'chimango':('Chimango','Daptrius chimango','UNRC, Río Cuarto','27/12/2025'),
 'picaflor_verde':('Picaflor común','Chlorostilbon lucidus','Casa, Río Cuarto','16/03/2026'),
 'gallineta_pico_pintado':('Gallineta pico pintado','Pardirallus sanguinolentus','Laguna Los Medanitos, Paso del Durazno','27/06/2026'),
 'tachuri_siete_colores':('Tachurí sietecolores','Tachuris rubrigastra','Laguna Rivero, Alcira Gigena','31/10/2026'),
 'tacuarita_azul':('Tacuarita azul','Polioptila dumicola','Los Hornillos, Córdoba','12/06/2026'),
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
# mes -> [(texto del día, descripción, [días])]  (nacionales 2027; 20/11 podría moverse)
FERIADOS = {
 1:[('1','Año Nuevo',[1])],
 2:[('8 y 9','Carnaval',[8,9])],
 3:[('24','Día de la Memoria, por la Verdad y la Justicia',[24]),('26','Viernes Santo',[26])],
 4:[('2','Día del Veterano y de los Caídos en Malvinas',[2])],
 5:[('1','Día del Trabajador',[1]),('25','Día de la Revolución de Mayo',[25])],
 6:[('20','Paso a la Inmortalidad del Gral. Belgrano',[20]),('21','Paso a la Inmortalidad del Gral. Güemes',[21])],
 7:[('9','Día de la Independencia',[9])],
 8:[('16','Paso a la Inmortalidad del Gral. San Martín',[16])],
 9:[],
 10:[('11','Día del Respeto a la Diversidad Cultural',[11])],
 11:[('20','Día de la Soberanía Nacional',[20])],
 12:[('8','Inmaculada Concepción de María',[8]),('25','Navidad',[25])],
}

FUENTES = os.environ.get('CAL_FUENTES', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes'))  # woff2 de Cormorant Garamond (npm i @fontsource/cormorant-garamond)
def fuentes_css():
    out = ''
    for w in (400, 500, 600, 700):
        for st in ('normal', 'italic'):
            f = os.path.join(FUENTES, 'cormorant-garamond-latin-%d-%s.woff2' % (w, st))
            out += "@font-face{font-family:Corm;font-weight:%d;font-style:%s;src:url(data:font/woff2;base64,%s)}" % (w, st, base64.b64encode(open(f, 'rb').read()).decode())
    return out
def titulo(t):
    return ' '.join(p if p in ('de', 'del', 'la', 'y') else p[:1].upper() + p[1:] for p in t.split(' '))
NOM = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{background:#fff;font-family:Inter,Helvetica,Arial,sans-serif;color:#2b2a20}
.s{width:210mm;height:99mm;background:#f3ece1;position:relative;overflow:hidden}
.ph{position:absolute;top:0;height:99mm;width:137mm;background-size:cover;background-position:center}
.ph{overflow:hidden}.ph:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,#000c 0,#0007 22%,#0000 48%)}
.cap{position:absolute;left:7mm;bottom:6mm;color:#fff;z-index:2;max-width:100mm}
.cap .n{font:600 8.4mm/1 Corm,Georgia,serif;letter-spacing:.1mm}.cap .sc{font:italic 500 4.2mm Corm,Georgia,serif;margin-top:.8mm;opacity:.95}
.cap .lg{font-size:2.1mm;letter-spacing:.5mm;font-weight:500;margin-top:1.4mm;opacity:.85;text-transform:uppercase}
.p{position:absolute;top:6mm;bottom:5mm;width:59mm;display:flex;flex-direction:column}
.y{font-size:2.3mm;letter-spacing:2.2mm;color:#8a6a3d;font-weight:600}
h1{font:600 16mm/.95 Corm,Georgia,serif;color:#2f3a1e;margin-top:.8mm}
table{border-collapse:collapse;table-layout:fixed;width:100%;margin-top:3mm}
th{font-size:1.9mm;color:#8a6a3d;font-weight:600;letter-spacing:.3mm;padding-bottom:1.2mm;border-bottom:.3mm solid #2f3a1e}
td{height:5.7mm;text-align:center;font-size:3mm;font-weight:500;color:#2b2a20;font-variant-numeric:tabular-nums}
tr.sp td{height:1.3mm}td.d{color:#b5532f}td.f{color:#fff;font-weight:700;background:radial-gradient(circle,#b5532f 0,#b5532f 2.45mm,#0000 2.5mm)}
.fl{margin-top:2.6mm;display:flex;flex-direction:column;gap:.9mm}.fl div{font-size:2.25mm;line-height:1.2;color:#4a4636;display:flex;gap:1.6mm}
.fl b{color:#b5532f;font-weight:700;min-width:6.2mm}
.ft{margin-top:auto;display:flex;align-items:center;gap:3mm;border-top:.3mm solid #cbb89a;padding-top:2.6mm}
.lo{width:5.6mm;height:8.4mm;background:#2f3a1e;-webkit-mask:url(LOGO) center/contain no-repeat;mask:url(LOGO) center/contain no-repeat;flex:none}
.ft b{font-size:2.1mm;letter-spacing:.95mm;color:#2f3a1e;display:block;font-weight:600}.ft i{font:italic 500 3.5mm Corm,Georgia,serif;color:#8a6a3d;display:block;margin-top:.5mm}
.cv{position:absolute;inset:0;overflow:hidden}
.cv2{position:absolute;inset:0;background:linear-gradient(90deg,#000d 0,#000a 24%,#0000 52%),linear-gradient(0deg,#000a 0,#0000 32%)}
.cl{position:absolute;left:10mm;top:9mm;bottom:8mm;width:100mm;color:#fff;display:flex;flex-direction:column}
.cl .ca{font-size:2.6mm;letter-spacing:1.6mm;font-weight:500;margin-top:17mm;opacity:.92}
.cl .yr{font:300 36mm/1 'Inter Display',Inter,sans-serif;letter-spacing:-1.6mm;margin:1mm 0 0 -1.2mm}
.cl .ft{margin-top:auto;display:flex;align-items:center;gap:3mm;border:0;padding:0}
.clo{width:8mm;height:12mm;background:#fff;-webkit-mask:url(LOGO) left center/contain no-repeat;mask:url(LOGO) left center/contain no-repeat}
.cl .mk{font-size:3mm;letter-spacing:1.2mm;font-weight:500}.cl .wb{font-size:2.5mm;margin-top:1.2mm;opacity:.9;letter-spacing:.2mm}
.cap2{position:absolute;right:8mm;bottom:8mm;color:#fff;text-align:right}.cap2 .n{font:600 7mm/1 Corm,Georgia,serif}.cap2 .sc{font:italic 500 3.8mm Corm,Georgia,serif;margin-top:.7mm}.cap2 .lg{font-size:2.1mm;letter-spacing:.5mm;font-weight:500;margin-top:1.3mm;opacity:.9;text-transform:uppercase}"""
def img(d, n):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(d, n + '.jpg'), 'rb').read()).decode()
import json
ENC_F = os.environ.get('CAL_ENC', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'encuadres.json'))
ENC = json.load(open(ENC_F)) if os.path.exists(ENC_F) else {}   # lo exporta encuadre.html: {"portada":{foto,z,cx,cy},"01":{...}}
def caja(d, f, key, FW, FH, z0=1.0, cx0=.5, cy0=.5):
    """Posición de la foto dentro del marco FWxFH mm: z=zoom sobre 'cubrir', (cx,cy)=punto de la foto que queda al centro."""
    from PIL import Image
    e = ENC.get(key, {}); z = e.get('z', z0); cx = e.get('cx', cx0); cy = e.get('cy', cy0)
    iw, ih = Image.open(os.path.join(d, f + '.jpg')).size
    Wc = max(FW, FH * iw / ih); W = Wc * z; H = W * ih / iw
    L = min(0, max(FW - W, FW / 2 - cx * W)); T = min(0, max(FH - H, FH / 2 - cy * H))
    return 'position:absolute;width:%.2fmm;height:%.2fmm;left:%.2fmm;top:%.2fmm;background-size:100%% 100%%;background-image:url(%s)' % (W, H, L, T, img(d, f))
def logo():
    return 'data:image/png;base64,' + base64.b64encode(open(LOGO, 'rb').read()).decode()
def mes(d, m):
    f, lado = MESES[m]; f = ENC.get('%02d' % m, {}).get('foto', f); nom, cie, lug, fec = AVES[f]; nom = titulo(nom); fer = FERIADOS.get(m, [])
    dias = [x for _, _, ds in fer for x in ds]
    cal = calendar.Calendar(0).monthdayscalendar(2027, m)
    rows = ''.join('<tr>' + ''.join('<td></td>' if x == 0 else '<td class="%s">%d</td>' % (('f' if x in dias else 'd' if i == 6 else ''), x) for i, x in enumerate(w)) + '</tr>' for w in cal)
    th = ''.join('<th>%s</th>' % c for c in 'LMMJVSD')
    fl = ''.join('<div><b>%s</b><span>%s</span></div>' % (t, tx) for t, tx, _ in fer)
    foto = 'left:0' if lado == 'L' else 'right:0'
    panel = 'left:144mm' if lado == 'L' else 'left:7mm'
    return ('<div class="s"><div class="ph" style="%s"><div class="im" style="%s"></div><div class="cap"><div class="n">%s</div><div class="sc">%s</div><div class="lg">%s</div></div></div>'
            '<div class="p" style="%s"><span class="y">2027</span><h1 style="font-size:%smm">%s</h1><table><tr>%s</tr>%s</table><div class="fl">%s</div>'
            '<div class="ft"><div class="lo"></div><div><b>FÉLIX SANTIAGO · AVES</b><i>felixsantiago.com.ar</i></div></div></div></div>') % (foto, caja(d, f, '%02d' % m, 137, 99), nom, cie, lug, panel, ('16' if len(NOM[m-1]) <= 7 else '13.5' if len(NOM[m-1]) <= 8 else '11.6'), NOM[m-1], th, rows, fl)
def portada(d):
    nom, cie, lug, fec = AVES[PORTADA]; nom = titulo(nom)
    return ('<div class="s"><div class="cv"><div style="%s"></div></div><div class="cv2"></div>'
            '<div class="cl"><div class="ca">CALENDARIO DE ESCRITORIO</div><div class="yr">2027</div>'
            '<div class="ft"><div class="clo"></div><div><div class="mk">FÉLIX SANTIAGO · AVES</div><div class="wb">felixsantiago.com.ar · @felix_santiago_aves</div></div></div></div>'
            '<div class="cap2"><div class="n">%s</div><div class="sc">%s</div><div class="lg">%s</div></div></div>') % (caja(d, ENC.get('portada', {}).get('foto', PORTADA), 'portada', 210, 99, 1.4286, .397, .5075), nom, cie, lug)
if __name__ == '__main__':
    fotos, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    pags = {'portada': portada(fotos)}
    for m in ([int(x) for x in sys.argv[3:] if x.isdigit()] if len(sys.argv) > 3 else MESES):
        pags['%02d-%s' % (m, NOM[m-1].lower())] = mes(fotos, m)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 374}, device_scale_factor=2)
        for k, h in pags.items():
            pg.set_content('<meta charset="utf-8"><style>%s</style>%s' % (fuentes_css() + CSS.replace('LOGO', logo()), h)); pg.wait_for_timeout(300)
            pg.locator('.s').screenshot(path=os.path.join(out, k + '.png')); print(k)
        b.close()
