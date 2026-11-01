#!/usr/bin/env python3
"""Genera mascotas animadas (SVG) de especies que Félix vio y todavía no fotografió.
Uso:  python3 -I _build/mascotas/gen_mascotas.py <carpeta_salida>
Cada especie es un diccionario con medidas y colores sobre un mismo esqueleto de ave (mira a la izquierda).
Sumar una especie = sumar un diccionario en ESPECIES. Animación en el lugar: respira, mueve la cabeza, parpadea y sacude la cola."""
import math, os, sys

OUT = '#2a1f14'
GROUND = 272

BASE = dict(
    cx=158, cy=176, rx=62, ry=44, rot=10,          # cuerpo
    hx=104, hy=122, hr=30,                          # cabeza
    nw=34, nbx=128, nby=150,                        # cuello (grosor y base)
    back='#8a7a66', belly='#d8cdb8', breast=None, head=None, wing=None, bars=None, barcol='#f1ece0',
    tail='#6a5a48', tl=66, tw0=26, tw1=32, tang=34, fork=0, tipcol=None,
    bill='#3a3030', bl=18, bd=9, bcurve=0, btype='cono', billtip=None,
    legs='#7a6a58', lw=6, toe=1.0, legx=(-12, 12), legtop=None,
    eye='#1b120c', eyering=None, er=4.6,
    wingext=8, extras_head='', extras_body='', crest=0, crestcol=None,
    spots=None, bars_n=2, head_bob=1.0, tail_flick=1.0, name='',
)


def rect_poly(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'


def tail_path(p):
    x0 = p['cx'] + p['rx'] - 10
    y0 = p['cy'] + 2
    a = math.radians(p['tang'])
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    L, w0, w1 = p['tl'], p['tw0'], p['tw1']
    bx1, by1 = x0 + nx * w0 / 2, y0 + ny * w0 / 2
    bx2, by2 = x0 - nx * w0 / 2, y0 - ny * w0 / 2
    tx, ty = x0 + dx * L, y0 + dy * L
    t1 = (tx + nx * w1 / 2, ty + ny * w1 / 2)
    t2 = (tx - nx * w1 / 2, ty - ny * w1 / 2)
    if p['fork']:
        f = p['fork']
        mid = (tx - dx * f, ty - dy * f)
        pts = [(bx1, by1), t1, mid, t2, (bx2, by2)]
    else:
        pts = [(bx1, by1), t1, t2, (bx2, by2)]
    return rect_poly(pts), (x0, y0), (tx, ty), (dx, dy, nx, ny)


def bill_path(p):
    hx, hy, hr = p['hx'], p['hy'], p['hr']
    bx = hx - hr + 4
    by = hy + 2
    L, D, c = p['bl'], p['bd'], p['bcurve']
    tip = (bx - L, by + 4 + c)
    top = (bx, by - D / 2)
    bot = (bx, by + D / 2)
    t = p['btype']
    if t == 'gancho':
        return (f'M{top[0]:.1f} {top[1]:.1f} Q{bx - L * .6:.1f} {by - D / 2 - 2:.1f} {tip[0]:.1f} {tip[1] + 3:.1f} '
                f'Q{tip[0] + 3:.1f} {tip[1] - 1:.1f} {bx - L * .6:.1f} {by + D * .1:.1f} L{bot[0]:.1f} {bot[1]:.1f} Z')
    if t == 'curvo':
        return (f'M{top[0]:.1f} {top[1]:.1f} Q{bx - L * .55:.1f} {by - D / 2 - 1:.1f} {tip[0]:.1f} {tip[1]:.1f} '
                f'Q{bx - L * .55:.1f} {by + D / 2 + 1:.1f} {bot[0]:.1f} {bot[1]:.1f} Z')
    return (f'M{top[0]:.1f} {top[1]:.1f} L{tip[0]:.1f} {tip[1]:.1f} L{bot[0]:.1f} {bot[1]:.1f} Z')


def build(p):
    p = {**BASE, **p}
    p['nw'] = p['nw'] + 8 if p['nw'] else 0
    head = p['head'] or p['back']
    wing = p['wing'] or p['back']
    breast = p['breast'] or p['belly']
    cx, cy, rx, ry, rot = p['cx'], p['cy'], p['rx'], p['ry'], p['rot']
    hx, hy, hr = p['hx'], p['hy'], p['hr']
    tpath, (tx0, ty0), (ttx, tty), _ = tail_path(p)
    # patas
    legtop = p['legtop'] or (cy + ry - 8)
    legs = ''
    for lx in p['legx']:
        x = cx + lx
        ln = GROUND - legtop
        legs += (f'<path d="M{x} {legtop} L{x - 2} {GROUND - 4}" stroke="{OUT}" stroke-width="{p["lw"] + 3}" stroke-linecap="round"/>'
                 f'<path d="M{x} {legtop} L{x - 2} {GROUND - 4}" stroke="{p["legs"]}" stroke-width="{p["lw"]}" stroke-linecap="round"/>')
        t = p['toe']
        for dx, dy in ((-26 * t, 6), (-18 * t, 12), (10 * t, 8)):
            legs += (f'<path d="M{x - 2} {GROUND - 4} L{x - 2 + dx:.1f} {GROUND - 4 + dy * .5:.1f}" stroke="{OUT}" stroke-width="{p["lw"] * .75 + 3}" stroke-linecap="round"/>'
                     f'<path d="M{x - 2} {GROUND - 4} L{x - 2 + dx:.1f} {GROUND - 4 + dy * .5:.1f}" stroke="{p["legs"]}" stroke-width="{p["lw"] * .75}" stroke-linecap="round"/>')
    # cola
    tail_extra = ''
    if p['tipcol']:
        tail_extra = (f'<clipPath id="tc"><path d="{tpath}"/></clipPath><g clip-path="url(#tc)">'
                      f'<circle cx="{ttx:.1f}" cy="{tty:.1f}" r="{p["tw1"] + 14}" fill="{p["tipcol"]}"/></g>')
    tail = (f'<g id="m-tail"><path d="{tpath}" fill="{p["tail"]}" stroke="{OUT}" stroke-width="3.5" stroke-linejoin="round"/>{tail_extra}'
            f'{p.get("extras_tail", "")}</g>')
    # cuerpo
    body = (f'<ellipse id="m-body" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="{p["back"]}"/>'
            f'<clipPath id="bc"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})"/></clipPath>'
            f'<g clip-path="url(#bc)">'
            f'<ellipse cx="{cx - 16}" cy="{cy + ry * .78}" rx="{rx * 1.1}" ry="{ry * .9}" fill="{p["belly"]}"/>'
            f'<ellipse cx="{cx - rx * .62}" cy="{cy + 6}" rx="{rx * .42}" ry="{ry * .85}" fill="{breast}"/>'
            f'{p["extras_body"]}</g>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="none" stroke="{OUT}" stroke-width="3.5"/>')
    # ala
    wx0, wy0 = cx - 34, cy - 20
    wtx, wty = cx + rx + p['wingext'], cy + 16 + p['wingext'] * .3
    wingp = (f'M{wx0} {wy0} C{cx - 8} {cy - 38} {cx + 40} {cy - 24} {wtx} {wty} '
             f'C{cx + 40} {cy + 24} {cx - 4} {cy + 24} {cx - 34} {cy + 8} Z')
    bars = ''
    if p['bars']:
        for i in range(p['bars_n']):
            y = cy - 12 + i * 11
            bars += f'<path d="M{cx - 26 + i * 3} {y} Q{cx + 4} {y - 9} {cx + 36 + i * 6} {y + 4 + i}" stroke="{p["bars"]}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    wingg = (f'<g id="m-wing"><path d="{wingp}" fill="{wing}" stroke="{OUT}" stroke-width="3" stroke-linejoin="round"/>{bars}{p.get("extras_wing", "")}</g>')
    # cabeza
    nb = (p['nbx'], p['nby'])
    neck = ''
    if p['nw']:
        neck = (f'<path d="M{nb[0]} {nb[1]} L{hx + 10} {hy + 14}" stroke="{OUT}" stroke-width="{p["nw"] + 7}" stroke-linecap="round"/>'
                f'<path d="M{nb[0]} {nb[1]} L{hx + 10} {hy + 14}" stroke="{p["neckcol"] if "neckcol" in p else head}" stroke-width="{p["nw"]}" stroke-linecap="round"/>')
        if 'neckextra' in p:
            neck += p['neckextra']
    crest = ''
    if p['crest']:
        c = p['crest']
        crest = (f'<path d="M{hx - 6} {hy - hr + 3} C{hx - 4} {hy - hr - c} {hx + 14} {hy - hr - c * .9} {hx + 22} {hy - hr + 6} Z" fill="{p["crestcol"] or head}" stroke="{OUT}" stroke-width="3" stroke-linejoin="round"/>')
    ex, ey = hx - 9, hy - 4
    eyeg = ''
    if p['eyering']:
        eyeg += f'<circle cx="{ex}" cy="{ey}" r="{p["er"] + 3}" fill="{p["eyering"]}"/>'
    eyeg += (f'<circle cx="{ex}" cy="{ey}" r="{p["er"]}" fill="{p["eye"]}"/>'
             f'<circle cx="{ex - 1.5}" cy="{ey - 1.7}" r="1.5" fill="#fff"/>')
    lid = f'<ellipse id="m-lid" cx="{ex}" cy="{ey}" rx="{p["er"] + 3.2}" ry="{p["er"] + 3.2}" fill="{head}"/>'
    headg = (f'<g id="m-head">{neck}{crest}'
             f'<path d="{bill_path(p)}" fill="{p["bill"]}" stroke="{OUT}" stroke-width="3" stroke-linejoin="round"/>'
             f'{p.get("extras_bill", "")}'
             f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="{head}"/>'
             f'<clipPath id="hc"><circle cx="{hx}" cy="{hy}" r="{hr}"/></clipPath><g clip-path="url(#hc)">{p["extras_head"]}</g>'
             f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="none" stroke="{OUT}" stroke-width="3.5"/>'
             f'{eyeg}{lid}{p.get("extras_front", "")}</g>')
    hb, tf = p['head_bob'], p['tail_flick']
    css = (f'#m-root{{transform-box:view-box;transform-origin:150px {GROUND}px;animation:br 3.6s ease-in-out infinite}}'
           f'@keyframes br{{0%,100%{{transform:scale(1,1)}}50%{{transform:scale(1,1.012)}}}}'
           f'#m-head{{transform-box:view-box;transform-origin:{nb[0]}px {nb[1]}px;animation:hb 4.6s ease-in-out infinite}}'
           f'@keyframes hb{{0%,100%{{transform:rotate(0)}}22%{{transform:rotate({-7 * hb}deg)}}45%{{transform:rotate({4 * hb}deg) translateY(1px)}}'
           f'62%{{transform:rotate({-3 * hb}deg)}}80%{{transform:rotate({6 * hb}deg)}}}}'
           f'#m-tail{{transform-box:view-box;transform-origin:{tx0:.0f}px {ty0:.0f}px;animation:tl 3.1s ease-in-out infinite}}'
           f'@keyframes tl{{0%,66%,100%{{transform:rotate(0)}}74%{{transform:rotate({-11 * tf}deg)}}84%{{transform:rotate({4 * tf}deg)}}92%{{transform:rotate({-3 * tf}deg)}}}}'
           f'#m-lid{{transform-box:fill-box;transform-origin:center;animation:bl 4.4s infinite}}'
           f'@keyframes bl{{0%,92%,100%{{transform:scaleY(0)}}95%{{transform:scaleY(1)}}}}'
           f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}')
    return (f'<svg role="img" aria-label="{p["name"]}" viewBox="-20 0 360 300" width="360" height="300" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">'
            f'<style>{css}</style><g id="m-root">{tail}<g id="m-legs">{legs}</g>{body}{wingg}{headg}</g></svg>')


def H(p):  # atajo para marcas de la cabeza, usa la geometría final
    q = {**BASE, **p}
    return q['hx'], q['hy'], q['hr']


def cap(p, col, h=0.46):          # gorro: cubre la parte alta de la cabeza
    hx, hy, hr = H(p)
    return f'<rect x="{hx - hr - 2}" y="{hy - hr - 2}" width="{hr * 2 + 4}" height="{hr * (1 - h + .0) :.1f}" fill="{col}"/>'


def stripe(p, col, w=5, dy=-10, x0=-4):   # ceja (supercilium) hacia atrás
    hx, hy, hr = H(p)
    return f'<path d="M{hx - hr} {hy + dy + 4} Q{hx - 8} {hy + dy - 3} {hx + hr} {hy + dy + 2}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


def eyeline(p, col, w=4, dy=-4):
    hx, hy, hr = H(p)
    return f'<path d="M{hx - hr} {hy + dy + 2} L{hx + hr} {hy + dy + 6}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'


def mottle(col, pts, r=3.2):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>' for x, y in pts)


def barras(col, x0, x1, y0, y1, n, w=3):
    s = ''
    for i in range(n):
        y = y0 + (y1 - y0) * i / max(1, n - 1)
        s += f'<path d="M{x0} {y:.1f} Q{(x0 + x1) / 2} {y - 6:.1f} {x1} {y + 2:.1f}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
    return s


ESPECIES = {}

# 1. Aguatero: cabeza grande y oscura, pico largo caído, tirantes dorados
_p = dict(name='Aguatero', hr=32, hy=124, back='#6f6a3a', belly='#f4efe2', head='#6e2f26', bars=None,
          tail='#6a5f38', tl=34, tw0=22, tw1=24, tang=40, bill='#b9b44a', bl=44, bd=8, bcurve=14, btype='curvo',
          legs='#9aa36a', lw=5, legx=(-6, 16), cy=170, ry=46, rx=58, nw=36)
_p['extras_head'] = (f'<path d="M72 92 Q104 80 136 100" stroke="#ecd8a4" stroke-width="7" fill="none"/>'
                     f'<path d="M72 108 Q96 104 134 112" stroke="#fff" stroke-width="3.5" fill="none"/>')
_p['extras_body'] = ('<path d="M120 150 Q150 128 196 150" stroke="#e0a830" stroke-width="7" fill="none"/>'
                     '<path d="M118 164 Q150 144 192 164" stroke="#e0a830" stroke-width="5" fill="none"/>'
                     '<path d="M104 148 Q104 178 128 184" stroke="#fff" stroke-width="9" fill="none"/>'
                     + mottle('#fff', [(168, 156), (182, 164), (150, 160)], 3.4))
_p['extras_bill'] = f'<path d="M{BASE["hx"]-32-40} {BASE["hy"]+22} l8 4" stroke="#e8902a" stroke-width="5" stroke-linecap="round"/>'
ESPECIES['aguatero'] = _p

# 2. Pitiayumí: azul grisáceo, manto verde, dos barras alares, amarillo con garganta naranja
_p = dict(name='Pitiayumí', hr=27, hy=126, hx=106, back='#6f8fa8', belly='#f2c230', breast='#f2c230', head='#6f8fa8',
          bars='#ffffff', tail='#5d7890', tl=58, tw0=20, tw1=22, tang=34, bill='#2d2a2a', bl=17, bd=7, btype='fino',
          legs='#4a4a4a', lw=4.5, cx=156, cy=178, rx=54, ry=40, nw=30, nbx=126, nby=152, wing='#587a94')
_p['extras_head'] = '<ellipse cx="96" cy="150" rx="26" ry="16" fill="#ec8a35"/>'
_p['extras_body'] = ('<ellipse cx="118" cy="172" rx="30" ry="22" fill="#ec8a35"/>'
                     '<path d="M120 142 Q152 130 188 150 L188 160 Q150 150 120 160 Z" fill="#8aa84a"/>')
ESPECIES['pitiayumi'] = _p

# 3. Atajacaminos Tijera: postura baja, ojo enorme, collar rojizo, cola muy larga con tijera
_p = dict(name='Atajacaminos Tijera', cx=160, cy=196, rx=66, ry=34, rot=2, hx=100, hy=162, hr=30, nw=36, nbx=126, nby=184,
          back='#8b7b66', belly='#b9a98e', head='#86765f', wing='#7d6d58', tail='#5f503f', tl=118, tw0=22, tw1=14, tang=14, fork=22,
          bill='#4a3d34', bl=10, bd=8, btype='cono', legs='#c7b8a0', lw=5, legtop=214, er=7.5, eyering='#3a2e24', eye='#0d0906',
          head_bob=.7, tail_flick=.6, ground=0)
_p['extras_head'] = mottle('#4b3e30', [(88, 146), (104, 140), (120, 150), (96, 172), (112, 176)], 3.4) + '<path d="M70 176 Q104 188 136 176" stroke="#b5683a" stroke-width="9" fill="none"/>'
_p['extras_body'] = mottle('#3f3328', [(120, 190), (140, 184), (160, 192), (180, 186), (200, 194), (150, 206), (176, 208)], 4)
_p['extras_wing'] = mottle('#3f3328', [(150, 180), (170, 176), (190, 184), (160, 192)], 3.5)
_p['extras_tail'] = '<path d="M250 206 L330 214" stroke="#f1ece0" stroke-width="5" stroke-linecap="round"/>'
ESPECIES['atajacaminos-tijera'] = _p

# 4. Chiricote: gris atrás de la cabeza, pecho y abdomen castaños, pico verde-amarillo, patas rosadas
_p = dict(name='Chiricote', hr=29, hy=116, hx=100, back='#6b6a38', belly='#9a4a28', breast='#9a4a28', head='#8c959d',
          tail='#2a2623', tl=38, tw0=22, tw1=24, tang=-20, bill='#cfc83a', bl=30, bd=10, btype='cono',
          legs='#d9605a', lw=7, legx=(-10, 14), cx=160, cy=172, rx=64, ry=46, nw=36, nbx=130, nby=148, eye='#b3211e',
          wing='#6a6b3a', wingext=6, tail_flick=1.4, head_bob=1.1)
_p['extras_body'] = '<ellipse cx="120" cy="150" rx="26" ry="22" fill="#8c959d"/>'
ESPECIES['chiricote'] = _p

# 5. Golondrina Ceja Blanca: azul verdoso brillante, vientre blanco, cola muy ahorquillada
_p = dict(name='Golondrina Ceja Blanca', cx=156, cy=178, rx=60, ry=36, rot=14, hx=102, hy=132, hr=26, nw=30, nbx=124, nby=156,
          back='#2c7ea6', belly='#fbfaf6', breast='#fbfaf6', head='#2c7ea6', wing='#1f6a8f', wingext=36,
          tail='#1f5f84', tl=84, tw0=22, tw1=30, tang=30, fork=34, bill='#2a2a2a', bl=10, bd=7, btype='cono',
          legs='#5a4a40', lw=4.5, legtop=200, head_bob=.8, tail_flick=1.2, wl=1)
_p['extras_head'] = '<circle cx="86" cy="124" r="4.5" fill="#fff"/>'
ESPECIES['golondrina-ceja-blanca'] = _p

# 6. Pijuí Frente Gris: gorro y alas rojizos, frente parda, cola rojiza larga y puntiaguda
_p = dict(name='Pijuí Frente Gris', cx=156, cy=176, rx=52, ry=40, rot=24, hx=104, hy=124, hr=26, nw=30, nbx=124, nby=152,
          back='#8a6c4a', belly='#a8998a', breast='#a8998a', head='#b5502a', wing='#b5502a', tail='#b0502c',
          tl=104, tw0=16, tw1=6, tang=48, bill='#3a2e28', bl=15, bd=7, btype='fino', legs='#6a5a4c', lw=4.5, tail_flick=1.1, wingext=2)
_p['extras_head'] = '<rect x="60" y="86" width="26" height="26" fill="#8f735b"/>'
ESPECIES['pijui-frente-gris'] = _p

# 7. Monterita de Collar: gris y blanca, oreja negra, ceja blanca, collar negro en el pecho
_p = dict(name='Monterita de Collar', cx=156, cy=178, rx=52, ry=40, rot=10, hx=104, hy=126, hr=26, nw=30, nbx=124, nby=154,
          back='#8b9298', belly='#f6f3ec', breast='#f6f3ec', head='#8b9298', wing='#767d84', tail='#6a7178', tl=58, tw0=18, tw1=20, tang=32,
          bill='#59595c', bl=15, bd=9, btype='cono', legs='#4e4e50', lw=4.5, bars='#d9dde0', bars_n=1)
_p['extras_head'] = ('<path d="M72 90 Q100 82 132 98" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
                     '<ellipse cx="108" cy="124" rx="16" ry="10" fill="#1d1b1a"/>')
_p['extras_body'] = ('<path d="M96 148 Q122 168 150 150" stroke="#1d1b1a" stroke-width="10" fill="none"/>'
                     '<ellipse cx="204" cy="190" rx="14" ry="9" fill="#a8532e"/>')
ESPECIES['monterita-de-collar'] = _p

# 8. Pepitero Chico: pico amarillo grueso, cara negra con tira en el cuello, lomo arena, flancos durazno, cola negra con banda blanca
_p = dict(name='Pepitero Chico', cx=158, cy=176, rx=60, ry=44, rot=14, hx=104, hy=122, hr=30, nw=34, nbx=126, nby=152,
          back='#bb9c6c', belly='#9ea4a8', breast='#9ea4a8', head='#bb9c6c', wing='#a98a5c', tail='#1f1a18', tl=82, tw0=22, tw1=22, tang=38,
          tipcol='#fbf7ee', bill='#f0c935', bl=22, bd=15, btype='cono', legs='#6a5a4c', lw=5.5)
_p['extras_head'] = ('<path d="M70 108 Q92 98 112 120 Q124 136 134 146 L120 150 Q100 132 70 124 Z" fill="#1d1a19"/>')
_p['extras_body'] = '<ellipse cx="180" cy="196" rx="38" ry="18" fill="#ecaa84"/>'
_p['extras_bill'] = ''
ESPECIES['pepitero-chico'] = _p

# 9. Pepitero Gris: gris, ceja corta blanca, garganta blanca con bigotera negra, pecho gris, vientre ocre
_p = dict(name='Pepitero Gris', cx=160, cy=176, rx=62, ry=46, rot=12, hx=104, hy=120, hr=30, nw=36, nbx=128, nby=150,
          back='#6f7780', belly='#d3b588', breast='#8a9096', head='#6f7780', wing='#5e666f', tail='#5a5752', tl=86, tw0=24, tw1=24, tang=36,
          bill='#2b2a2a', bl=21, bd=15, btype='cono', legs='#4a4545', lw=6)
_p['extras_head'] = ('<path d="M72 98 Q90 92 108 100" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
                     '<ellipse cx="92" cy="146" rx="22" ry="14" fill="#fff"/>'
                     '<path d="M78 130 Q96 140 116 150" stroke="#1d1a19" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
ESPECIES['pepitero-gris'] = _p

# 10. Colorada: tinamú grande de cuello largo, lomo barrado pardo y crema, pecho gris, pico largo curvo
_p = dict(name='Colorada', cx=170, cy=186, rx=70, ry=52, rot=16, hx=86, hy=80, hr=24, nw=28, nbx=132, nby=160,
          back='#8b6a45', belly='#a7a8ae', breast='#a7a8ae', head='#b08a5c', neckcol='#c59a68', wing='#8b6a45',
          tail='#8b6a45', tl=20, tw0=26, tw1=30, tang=40, bill='#a0705a', bl=34, bd=7, bcurve=8, btype='curvo',
          legs='#c89a8c', lw=7, legtop=222, legx=(-14, 12), head_bob=.8, tail_flick=.3)
_p['extras_head'] = '<path d="M60 52 Q86 44 110 62" stroke="#7a5a38" stroke-width="9" fill="none"/>'
_p['extras_body'] = barras('#e8d7ac', 120, 226, 150, 196, 6, 4)
_p['extras_wing'] = barras('#e8d7ac', 140, 220, 154, 190, 4, 4)
ESPECIES['colorada'] = _p

# 11. Inambú Montaraz: copete negro, gris estriado de blanco, pecho moteado
_p = dict(name='Inambú Montaraz', cx=160, cy=184, rx=64, ry=48, rot=14, hx=98, hy=112, hr=25, nw=30, nbx=128, nby=160,
          back='#85878b', belly='#a7a7a3', breast='#9a9b9b', head='#85878b', wing='#85878b', tail='#85878b', tl=16, tw0=24, tw1=26, tang=40,
          bill='#c08a78', bl=20, bd=7, bcurve=6, btype='curvo', legs='#d4b896', lw=6, legtop=222, crest=16, crestcol='#26231f', head_bob=.9, tail_flick=.3)
_p['extras_body'] = barras('#f4f1ea', 118, 214, 150, 202, 6, 3) + mottle('#fff', [(104, 176), (116, 188), (126, 168), (134, 192), (142, 176)], 3)
_p['extras_head'] = mottle('#dcdde0', [(92, 126), (108, 130), (100, 138)], 2.2)
ESPECIES['inambu-montaraz'] = _p

# 12. Inambú Silbón: gris oscuro, finamente moteado de blanco, copete, pico rosado curvo, patas amarillentas
_p = dict(name='Inambú Silbón', cx=160, cy=184, rx=62, ry=46, rot=14, hx=100, hy=114, hr=25, nw=30, nbx=128, nby=160,
          back='#6f6860', belly='#5d626a', breast='#5d626a', head='#585d65', wing='#6f6860', tail='#6f6860', tl=16, tw0=24, tw1=26, tang=40,
          bill='#d9a0a0', bl=24, bd=7, bcurve=9, btype='curvo', legs='#e3c75a', lw=6, legtop=222, crest=18, crestcol='#3a3d44', head_bob=.9, tail_flick=.3)
_p['extras_body'] = mottle('#e9ebee', [(112, 170), (122, 184), (134, 170), (146, 190), (158, 172), (170, 190), (184, 176), (196, 190), (128, 200), (150, 204)], 2.4)
_p['extras_head'] = mottle('#dfe2e6', [(90, 126), (104, 132), (112, 124)], 1.8)
ESPECIES['inambu-silbon'] = _p

# 13. Calandrita: oliva apagado, ceja amarillenta, barra alar clara, vientre amarillo pálido, cola larga con puntas blancas
_p = dict(name='Calandrita', cx=156, cy=176, rx=50, ry=38, rot=18, hx=104, hy=124, hr=25, nw=28, nbx=124, nby=152,
          back='#8c8c4e', belly='#efe6a2', breast='#efe6a2', head='#8c8c4e', wing='#7d7d42', bars='#f1ecd2', bars_n=2,
          tail='#6b6b3a', tl=96, tw0=18, tw1=26, tang=42, tipcol='#fbf8ec', bill='#2d2a28', bl=15, bd=7, btype='fino', legs='#4a4540', lw=4.5, tail_flick=1.6)
_p['extras_head'] = '<path d="M72 106 Q98 96 130 108" stroke="#f1e68c" stroke-width="5" fill="none" stroke-linecap="round"/>'
ESPECIES['calandrita'] = _p

# 14. Pecho Colorado: negro, ceja blanca atrás, garganta y pecho carmesí
_p = dict(name='Pecho Colorado', cx=158, cy=176, rx=58, ry=44, rot=12, hx=104, hy=122, hr=28, nw=34, nbx=126, nby=152,
          back='#1f1d1d', belly='#1f1d1d', breast='#c8203a', head='#1f1d1d', wing='#2a2727', tail='#222020', tl=56, tw0=24, tw1=26, tang=34,
          bill='#4a4646', bl=24, bd=11, btype='cono', legs='#3e3a3a', lw=5.5)
_p['extras_head'] = ('<path d="M104 96 Q124 92 138 104" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
                     '<ellipse cx="86" cy="148" rx="26" ry="18" fill="#c8203a"/>')
_p['extras_body'] = '<ellipse cx="110" cy="164" rx="30" ry="26" fill="#c8203a"/>'
ESPECIES['pecho-colorado'] = _p

# 15. Chiví Común: oliva arriba, corona gris, ceja blanca con línea oscura, blanquecino abajo
_p = dict(name='Chiví Común', cx=156, cy=178, rx=52, ry=40, rot=12, hx=104, hy=126, hr=26, nw=30, nbx=124, nby=154,
          back='#8c9b4c', belly='#f1ecdc', breast='#efe9d6', head='#8c9b4c', wing='#7a8a3e', tail='#7a8a3e', tl=52, tw0=20, tw1=22, tang=34,
          bill='#7a6a68', bl=17, bd=8, btype='gancho', legs='#6a7078', lw=5, eye='#7a2a1e')
_p['extras_head'] = ('<rect x="66" y="88" width="76" height="18" fill="#8d9391"/>'
                     '<path d="M72 106 Q100 98 134 108" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
                     '<path d="M72 118 L134 120" stroke="#3b3a36" stroke-width="3" stroke-linecap="round"/>')
ESPECIES['chivi-comun'] = _p

# 16. Juan Chiviro: iris naranja, ceja rojiza, cara gris, oliva arriba, banda pectoral amarilla
_p = dict(name='Juan Chiviro', cx=158, cy=178, rx=56, ry=42, rot=12, hx=104, hy=124, hr=29, nw=34, nbx=126, nby=152,
          back='#7f9a3c', belly='#f1ead2', breast='#f1ead2', head='#8b9296', wing='#6f8c34', tail='#6f8c34', tl=58, tw0=22, tw1=24, tang=34,
          bill='#9a8a86', bl=22, bd=13, btype='gancho', legs='#8a7a78', lw=5.5, eye='#e8742a', eyering=None, er=5)
_p['extras_head'] = ('<path d="M70 104 Q98 94 134 106" stroke="#b5683a" stroke-width="5" fill="none" stroke-linecap="round"/>'
                     '<rect x="130" y="84" width="40" height="30" fill="#7f9a3c"/>')
_p['extras_body'] = '<path d="M92 150 Q124 176 160 150 L160 166 Q124 192 92 168 Z" fill="#e8c43a"/>'
ESPECIES['juan-chiviro'] = _p


def main(out):
    os.makedirs(out, exist_ok=True)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from dibujadas import MANO
    for slug, p in ESPECIES.items():
        txt = MANO[slug]() if slug in MANO else build(p)       # los dibujados a mano pisan al esqueleto común
        open(os.path.join(out, f'{slug}-animado.svg'), 'w', encoding='utf8').write(txt)
    # versión para que el navegador no use mascotas viejas guardadas en caché (la leen assets/pistas.js y el álbum)
    import hashlib, glob, re as _re
    h = hashlib.md5(b''.join(open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(out, '*-animado.svg'))))).hexdigest()[:8]
    pj = os.path.join(os.path.dirname(out.rstrip('/')), 'pistas.js')
    if os.path.exists(pj):
        t = open(pj, encoding='utf8').read()
        t = _re.sub(r"\nconst MASC_V='[0-9a-f]*';", '', t) + f"\nconst MASC_V='{h}';\n"
        open(pj, 'w', encoding='utf8').write(t)
    print(len(ESPECIES), 'mascotas en', out, f'({len(MANO)} dibujadas a mano)')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'assets/mascotas')
