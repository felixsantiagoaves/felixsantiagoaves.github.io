#!/usr/bin/env python3
"""Fondos de ambiente para las mascotas animadas. Genera assets/mascotas/fondos/<ambiente>.svg (400x300).
Ambientes: humedal, bosque, arbustal, ocaso, pastizal, sierras, cielo.  Uso: python3 _build/mascotas/gen_fondos.py"""
import random, os
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'mascotas', 'fondos')
W, H = 400, 300
CSS = ('<style>.nube{animation:nb 60s linear infinite}.nube2{animation:nb 90s linear infinite;animation-delay:-30s}'
       '@keyframes nb{from{transform:translateX(-120px)}to{transform:translateX(520px)}}'
       '.mece{transform-box:fill-box;transform-origin:50% 100%;animation:mc 4s ease-in-out infinite}'
       '.mece2{animation-duration:5.3s;animation-delay:-1.6s}'
       '@keyframes mc{0%,100%{transform:rotate(-2deg)}50%{transform:rotate(2.5deg)}}'
       '.brilla{animation:br 5s ease-in-out infinite}@keyframes br{0%,100%{opacity:.25}50%{opacity:.6}}'
       '@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>')

def svg(body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">'
            f'{CSS}<defs>{defs}</defs>{body}</svg>')
def grad(i, a, b, x2=0, y2=1):
    return f'<linearGradient id="{i}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
def nube(x, y, s=1, c='#fff', o=.75, cl='nube'):
    return (f'<g class="{cl}" opacity="{o}"><g transform="translate({x} {y}) scale({s})" fill="{c}"><ellipse cx="0" cy="0" rx="34" ry="11"/>'
            f'<ellipse cx="-18" cy="-8" rx="20" ry="11"/><ellipse cx="10" cy="-12" rx="24" ry="13"/></g></g>')
def lomas(y, amp, col, seed, step=40):
    r = random.Random(seed); pts = [(0, y)]
    for x in range(0, W + step, step): pts.append((x, y - r.uniform(0, amp)))
    d = f'M0 {H} L0 {y} ' + ' '.join(f'Q{x-step/2:.0f} {py-8:.0f} {x} {py:.0f}' for x, py in pts[1:]) + f' L{W} {H}Z'
    return f'<path d="{d}" fill="{col}"/>'
def pasto(n, y0, y1, cols, seed, h=(8, 20)):
    r = random.Random(seed); s = ''
    for _ in range(n):
        x = r.uniform(0, W); y = r.uniform(y0, y1); hh = r.uniform(*h); c = r.choice(cols)
        s += f'<path d="M{x:.0f} {y:.0f} q{r.uniform(-4,4):.0f} {-hh*.6:.0f} {r.uniform(-6,6):.0f} {-hh:.0f} M{x+2:.0f} {y:.0f} q{r.uniform(-3,3):.0f} {-hh*.5:.0f} {r.uniform(-4,8):.0f} {-hh*.8:.0f}" stroke="{c}" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
    return s
def caña(x, h, col, cl):
    return (f'<g class="mece {cl}"><path d="M{x} 300 Q{x+3} {300-h/2:.0f} {x+2} {300-h:.0f}" stroke="{col}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{x+2}" cy="{300-h-6:.0f}" rx="3.2" ry="11" fill="#6b4a2e"/></g>')

def humedal():
    d = grad('c', '#cfe6e0', '#f3efd9') + grad('a', '#7fb3ae', '#3f7f80')
    b = f'<rect width="{W}" height="{H}" fill="url(#c)"/>' + nube(70, 55, 1) + nube(300, 80, .8, cl='nube2')
    b += lomas(150, 14, '#a9c6b0', 3) + lomas(165, 10, '#86ad8e', 5)
    b += f'<rect y="170" width="{W}" height="130" fill="url(#a)"/>'
    r = random.Random(9)
    for i in range(14): b += f'<ellipse class="brilla" cx="{r.uniform(20,380):.0f}" cy="{r.uniform(185,295):.0f}" rx="{r.uniform(12,30):.0f}" ry="1.6" fill="#fff" style="animation-delay:{-r.uniform(0,5):.1f}s"/>'
    for x, y in ((90, 262), (300, 275), (210, 288)): b += f'<ellipse cx="{x}" cy="{y}" rx="16" ry="4.5" fill="#5f9a54" opacity=".9"/>'
    for i, x in enumerate((8, 22, 34, 360, 376, 390, 348)): b += caña(x, 110 + (i * 17) % 50, '#6f8a45', 'mece2' if i % 2 else '')
    return svg(b, d)
def bosque():
    d = grad('c', '#27412b', '#648a49') + grad('r', '#fff6c0', '#fff6c0')
    b = f'<rect width="{W}" height="{H}" fill="url(#c)"/>'
    b += '<g opacity=".16" fill="#fff6c0"><polygon points="140,0 175,0 120,300 60,300"/><polygon points="260,0 285,0 300,300 240,300"/></g>'
    r = random.Random(4)
    for i, (col, op) in enumerate((('#1d3322', .55), ('#18291c', .8))):
        for k in range(5):
            x = r.uniform(0, W); w = r.uniform(14, 28) - i * 3
            b += f'<rect x="{x:.0f}" y="0" width="{w:.0f}" height="300" fill="{col}" opacity="{op}"/>'
    for k in range(9):
        x, y = r.uniform(0, W), r.uniform(-10, 70)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(40,70):.0f}" ry="{r.uniform(20,34):.0f}" fill="{r.choice(["#2f5a33","#3d6b3a","#244a2c"])}" opacity=".85"/>'
    b += f'<rect y="262" width="{W}" height="40" fill="#3b2c1c"/><path d="M0 262 Q100 250 200 262 T400 262 V272 H0Z" fill="#4d6b34"/>'
    b += pasto(36, 258, 296, ['#7fa84c', '#5b8a3c', '#9fc060'], 2, (10, 24))
    return svg(b, d)
def arbustal(dusk=False):
    sky = ('#f2a65a', '#f8d9a0') if dusk else ('#9fc8d8', '#f1e6c7')
    ground = '#7a5a34' if dusk else '#a98b55'
    d = grad('c', *sky)
    b = f'<rect width="{W}" height="{H}" fill="url(#c)"/>'
    if dusk: b += '<circle cx="300" cy="150" r="30" fill="#ffd27a" opacity=".85"/>'
    b += lomas(185, 10, '#9a7a4a' if not dusk else '#6b4a30', 8)
    b += (f'<g fill="#3a2c1c"><rect x="68" y="120" width="7" height="85"/><path d="M20 118 Q71 92 124 118 Q71 110 20 118Z"/>'
          f'<ellipse cx="72" cy="112" rx="58" ry="16" fill="#4f6a34" opacity="{.9 if not dusk else .6}"/></g>')
    r = random.Random(6)
    for i in range(10):
        x = r.uniform(130, 390); y = r.uniform(205, 250); s = r.uniform(.8, 1.5)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="{r.choice(["#5d7a3a","#6f8a45","#4a6a33"]) if not dusk else r.choice(["#3e4a2a","#4a5430"])}"/>'
        b += f'<path d="M{x-12*s:.0f} {y:.0f} l5 -12 l3 10 l6 -14 l3 12" stroke="#3a2c1c" stroke-width="1.2" fill="none"/>'
    b += f'<rect y="245" width="{W}" height="60" fill="{ground}"/>' + pasto(60, 244, 298, ['#c9ad6a', '#a98b55', '#d8c07f'] if not dusk else ['#8f6d3d', '#a98b55'], 3, (8, 18))
    return svg(b, d)
def ocaso(): return arbustal(True)
def pastizal():
    d = grad('c', '#8fc3e0', '#f5ecd2') + grad('g', '#b7b45e', '#7d8f3e')
    b = f'<rect width="{W}" height="{H}" fill="url(#c)"/>' + nube(80, 50, 1.2) + nube(240, 35, 1, cl='nube2') + nube(340, 85, .8)
    b += lomas(170, 12, '#a7b36a', 11, 60) + lomas(190, 10, '#8fa04f', 12, 50)
    b += f'<rect y="205" width="{W}" height="100" fill="url(#g)"/>'
    b += pasto(140, 200, 298, ['#d9cf7a', '#9aa845', '#6f8a35', '#e6dd9c'], 7, (10, 30))
    b += '<g stroke="#5b4630" stroke-width="2"><line x1="330" y1="150" x2="330" y2="215"/></g><path d="M300 165 Q330 170 360 164" stroke="#5b4630" fill="none" stroke-width="1"/>'
    return svg(b, d)
def sierras():
    d = grad('c', '#8fb7d9', '#efe4cc')
    b = f'<rect width="{W}" height="{H}" fill="url(#c)"/>' + nube(300, 45, 1) + nube(110, 70, .8, cl='nube2')
    b += '<path d="M0 190 L70 110 L120 150 L190 85 L260 160 L320 120 L400 180 V300 H0Z" fill="#9aa7c4"/>'
    b += '<path d="M0 215 L60 160 L130 200 L210 140 L290 205 L360 165 L400 200 V300 H0Z" fill="#7b8f78"/>'
    b += '<path d="M190 85 L206 108 L194 104 L186 112 L178 102Z" fill="#fff" opacity=".7"/>'
    b += '<path d="M0 250 Q80 225 160 245 T400 240 V300 H0Z" fill="#8a8a56"/>'
    for x, y, s in ((60, 262, 1), (330, 270, 1.3), (200, 285, .9)): b += f'<path d="M{x-24*s:.0f} {y+12} L{x-12*s:.0f} {y-14*s:.0f} L{x+8*s:.0f} {y-20*s:.0f} L{x+26*s:.0f} {y+12}Z" fill="#8c8478"/><path d="M{x-12*s:.0f} {y-14*s:.0f} L{x+8*s:.0f} {y-20*s:.0f} L{x+4*s:.0f} {y}Z" fill="#a69e90" opacity=".7"/>'
    b += pasto(70, 255, 298, ['#b9a85a', '#8a8a56', '#d0c284'], 5, (8, 20))
    return svg(b, d)
def cielo():
    d = grad('c', '#6fb0e0', '#f3f0e2') + grad('l', '#9ccbe0', '#5f9fbd')
    b = f'<rect width="{W}" height="{H}" fill="url(#c)"/>' + nube(70, 60, 1.5) + nube(250, 40, 1.2, cl='nube2') + nube(340, 110, 1) + nube(150, 125, .9)
    b += lomas(190, 8, '#9bb58a', 13, 60) + f'<rect y="200" width="{W}" height="50" fill="url(#l)"/><rect y="246" width="{W}" height="60" fill="#8fa857"/>'
    r = random.Random(2)
    for i in range(8): b += f'<ellipse class="brilla" cx="{r.uniform(20,380):.0f}" cy="{r.uniform(205,244):.0f}" rx="{r.uniform(14,34):.0f}" ry="1.5" fill="#fff" style="animation-delay:{-r.uniform(0,5):.1f}s"/>'
    b += pasto(70, 250, 298, ['#6f8a35', '#9aa845', '#b6c26a'], 21, (8, 20))
    return svg(b, d)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n, f in (('humedal', humedal), ('bosque', bosque), ('arbustal', arbustal), ('ocaso', ocaso), ('pastizal', pastizal), ('sierras', sierras), ('cielo', cielo)):
        open(os.path.join(OUT, n + '.svg'), 'w', encoding='utf8').write(f())
    print('ok')
