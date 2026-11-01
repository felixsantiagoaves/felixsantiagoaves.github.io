"""Mascotas dibujadas a mano (un dibujo por especie), tomando de las láminas de la guía de Pearman y Areta
solo las marcas de campo, proporciones y postura; los trazos son originales.
Cada una devuelve un SVG con la misma animación base (respira, mueve la cabeza, parpadea, sacude la cola)."""
OUT = '#2a1f14'


def S(fill, w=3.5, extra=''):
    return f'fill="{fill}" stroke="{OUT}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {extra}'


def css(head_o, tail_o, root_o=(150, 275), hb=1.0, tf=1.0, peck=False, blink='4.4s'):
    hx, hy = head_o
    tx, ty = tail_o
    if peck:
        hk = (f'0%,100%{{transform:rotate(0)}}18%{{transform:rotate(-5deg)}}34%{{transform:rotate(7deg) translate(-4px,10px)}}'
              f'42%{{transform:rotate(9deg) translate(-6px,18px)}}50%{{transform:rotate(7deg) translate(-4px,8px)}}66%{{transform:rotate(-3deg)}}84%{{transform:rotate(4deg)}}')
        dur = '7s'
    else:
        hk = (f'0%,100%{{transform:rotate(0)}}22%{{transform:rotate({-7 * hb}deg)}}45%{{transform:rotate({4 * hb}deg) translateY(1px)}}'
              f'62%{{transform:rotate({-3 * hb}deg)}}80%{{transform:rotate({6 * hb}deg)}}')
        dur = '4.6s'
    return (f'#m-root{{transform-box:view-box;transform-origin:{root_o[0]}px {root_o[1]}px;animation:br 3.6s ease-in-out infinite}}'
            f'@keyframes br{{0%,100%{{transform:scale(1,1)}}50%{{transform:scale(1,1.012)}}}}'
            f'#m-head{{transform-box:view-box;transform-origin:{hx}px {hy}px;animation:hb {dur} ease-in-out infinite}}'
            f'@keyframes hb{{{hk}}}'
            f'#m-tail{{transform-box:view-box;transform-origin:{tx}px {ty}px;animation:tl 3.1s ease-in-out infinite}}'
            f'@keyframes tl{{0%,66%,100%{{transform:rotate(0)}}74%{{transform:rotate({-9 * tf}deg)}}84%{{transform:rotate({4 * tf}deg)}}92%{{transform:rotate({-3 * tf}deg)}}}}'
            f'.lid{{transform-box:fill-box;transform-origin:center;animation:bl {blink} infinite}}'
            f'@keyframes bl{{0%,92%,100%{{transform:scaleY(0)}}95%{{transform:scaleY(1)}}}}'
            f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}')


def svg(name, style, body):
    return (f'<svg role="img" aria-label="{name}" viewBox="-20 0 360 300" width="360" height="300" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">'
            f'<style>{style}</style><g id="m-root">{body}</g></svg>')


def ojo(x, y, r=5, col='#1b120c', lid='#999', ring=None, rr=3):
    s = ''
    if ring:
        s += f'<circle cx="{x}" cy="{y}" r="{r + rr}" fill="{ring}"/>'
    s += (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/><circle cx="{x - r * .3:.1f}" cy="{y - r * .35:.1f}" r="{r * .32:.1f}" fill="#fff"/>'
          f'<ellipse class="lid" cx="{x}" cy="{y}" rx="{r + rr + .4}" ry="{r + rr + .4}" fill="{lid}"/>')
    return s


# ───────────────────────── Colorada (Rhynchotus rufescens) ─────────────────────────
def colorada():
    pata = '#c9a27e'
    legs = ''.join(
        f'<path d="M{hx} 214 L{fx} 268" stroke="{OUT}" stroke-width="12" stroke-linecap="round"/><path d="M{hx} 214 L{fx} 268" stroke="{pata}" stroke-width="7.5" stroke-linecap="round"/>'
        f'<path d="M{fx} 268 L{fx - 26} 274 M{fx} 268 L{fx - 18} 282 M{fx} 268 L{fx + 10} 278" stroke="{OUT}" stroke-width="9" stroke-linecap="round"/>'
        f'<path d="M{fx} 268 L{fx - 26} 274 M{fx} 268 L{fx - 18} 282 M{fx} 268 L{fx + 10} 278" stroke="{pata}" stroke-width="5" stroke-linecap="round"/>'
        for hx, fx in ((196, 190), (166, 160)))
    cuerpo_d = 'M112 170 C100 206 126 242 174 246 C226 250 272 228 278 192 C282 160 246 138 198 136 C158 134 124 146 112 170 Z'
    cuerpo = (f'<path d="{cuerpo_d}" {S("#d8b273")}/>'
              f'<clipPath id="cc"><path d="{cuerpo_d}"/></clipPath><g clip-path="url(#cc)">'
              # dorso oscuro barrado, mitad alta y trasera
              f'<path d="M104 150 C150 130 232 130 276 168 L276 200 C240 176 190 172 150 186 C128 184 112 172 104 150 Z" fill="#4e3a28"/>'
              + ''.join(f'<path d="M{128 + i * 17} {146 + (i % 2) * 4} q10 22 {2 + i} 40" stroke="#e8cf95" stroke-width="5" fill="none" stroke-linecap="round"/>' for i in range(8))
              + ''.join(f'<path d="M{150 + i * 16} {198 + (i % 2) * 4} q8 10 {i} 20" stroke="#5a4430" stroke-width="3.5" fill="none" stroke-linecap="round"/>' for i in range(5))
              + '</g>'
              f'<path d="{cuerpo_d}" fill="none" stroke="{OUT}" stroke-width="3.5" stroke-linejoin="round"/>')
    ala = (f'<path d="M140 170 C170 150 226 154 252 184 C230 206 176 208 146 192 Z" {S("#5a4430", 3)}/>'
           + ''.join(f'<path d="M{158 + i * 18} {170 + i * 3} q8 14 {-2} 30" stroke="#e8cf95" stroke-width="4.5" fill="none" stroke-linecap="round"/>' for i in range(5)))
    cola = f'<g id="m-tail"><path d="M246 188 C262 180 276 186 282 196 C268 206 254 206 244 202 Z" {S("#4e3a28", 3)}/></g>'
    cuello_d = 'M104 176 C86 144 74 120 74 90 L118 84 C122 112 138 138 154 160 Z'
    cabeza = (f'<g id="m-head">'
              f'<path d="{cuello_d}" {S("#dcbb7e")}/>'
              + ''.join(f'<path d="M{92 + i * 3} {104 + i * 12} q12 3 {20 + i * 4} -2" stroke="#8a6a3e" stroke-width="2.6" fill="none" stroke-linecap="round"/>' for i in range(4))
              # pico largo curvo hacia abajo
              + f'<path d="M76 82 C60 80 44 88 32 108 C44 100 58 98 78 98 Z" {S("#8a6a58", 3)}/>'
              f'<path d="M78 97 C58 98 46 102 34 109 C54 108 68 104 80 100 Z" fill="#c9a08e" stroke="{OUT}" stroke-width="2" stroke-linejoin="round"/>'
              f'<ellipse cx="95" cy="84" rx="24" ry="19" transform="rotate(-8 95 84)" {S("#d9b87c")}/>'
              f'<clipPath id="hc"><ellipse cx="95" cy="84" rx="24" ry="19" transform="rotate(-8 95 84)"/></clipPath><g clip-path="url(#hc)">'
              f'<path d="M70 64 Q96 60 124 78 L124 70 Q100 52 70 56 Z" fill="#3a2c1e"/><rect x="70" y="60" width="60" height="12" fill="#3a2c1e" transform="rotate(-8 95 84)"/>'
              f'<path d="M72 80 Q92 74 118 82" stroke="#f1e3b4" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
              f'<path d="M76 90 Q96 84 118 92" stroke="#3a2c1e" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>'
              f'<ellipse cx="95" cy="84" rx="24" ry="19" transform="rotate(-8 95 84)" fill="none" stroke="{OUT}" stroke-width="3.5"/>'
              + ojo(86, 83, 4.6, ring='#f4ead0', rr=2.4, lid='#d9b87c') + '</g>')
    return svg('Colorada', css((116, 164), (250, 192), peck=True, tf=.5), f'{legs}{cola}{cuerpo}{ala}{cabeza}')


# ───────────────────────── Pepitero Chico (Saltatricula multicolor) ─────────────────────────
def pepitero_chico():
    pata = '#7a6454'
    legs = ''.join(
        f'<path d="M{hx} 226 L{fx} 270" stroke="{OUT}" stroke-width="9" stroke-linecap="round"/><path d="M{hx} 226 L{fx} 270" stroke="{pata}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M{fx} 270 L{fx - 20} 274 M{fx} 270 L{fx - 14} 281 M{fx} 270 L{fx + 9} 277" stroke="{OUT}" stroke-width="7.5" stroke-linecap="round"/>'
        f'<path d="M{fx} 270 L{fx - 20} 274 M{fx} 270 L{fx - 14} 281 M{fx} 270 L{fx + 9} 277" stroke="{pata}" stroke-width="3.8" stroke-linecap="round"/>'
        for hx, fx in ((172, 168), (150, 144)))
    cola_d = 'M196 214 C214 210 250 226 296 258 C298 268 282 268 262 262 C232 254 206 240 190 228 Z'
    cola = (f'<g id="m-tail"><path d="{cola_d}" {S("#1f1a18", 3)}/>'
            f'<clipPath id="tc"><path d="{cola_d}"/></clipPath><g clip-path="url(#tc)"><path d="M262 238 L312 252 L312 290 L270 290 Z" fill="#fbf6ea"/></g>'
            f'<path d="{cola_d}" fill="none" stroke="{OUT}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M206 218 C230 222 262 238 284 256" stroke="#fbf6ea" stroke-width="3.5" fill="none" opacity=".8" stroke-linecap="round"/></g>')
    cuerpo_d = 'M108 124 C92 150 100 196 126 220 C150 240 196 238 214 218 C222 196 206 158 176 132 C158 116 124 112 108 124 Z'
    cuerpo = (f'<path d="{cuerpo_d}" {S("#9a6a3c")}/>'
              f'<clipPath id="cc"><path d="{cuerpo_d}"/></clipPath><g clip-path="url(#cc)">'
              f'<path d="M84 146 C100 150 124 150 140 140 C128 190 140 232 172 246 L84 250 Z" fill="#9ca2a6"/>'    # pecho gris
              f'<path d="M96 186 C120 196 150 190 170 176 C196 200 214 226 210 244 L100 244 Z" fill="#ebaa80"/>'  # flanco durazno
              f'<path d="M110 224 C140 236 176 232 204 222 L206 250 L100 250 Z" fill="#f1e6d2"/></g>'
              f'<path d="{cuerpo_d}" fill="none" stroke="{OUT}" stroke-width="3.5" stroke-linejoin="round"/>')
    ala = (f'<path d="M132 134 C160 130 196 150 214 190 C204 222 184 232 170 226 C150 214 128 176 132 134 Z" {S("#8c5e34", 3)}/>'
           f'<path d="M150 146 q22 20 22 56 M166 142 q24 22 26 56" stroke="#5c3c1e" stroke-width="3" fill="none" stroke-linecap="round"/>'
           f'<path d="M156 218 C178 226 200 214 208 196" stroke="#f1e6d2" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    cabeza = (f'<g id="m-head">'
              f'<path d="M72 98 L52 104 Q50 108 54 112 L74 113 Z" {S("#f0c935", 3)}/><path d="M72 98 L52 104 L58 106 L74 102 Z" fill="#3a2e22"/>'
              f'<circle cx="100" cy="102" r="29" {S("#9a6a3c")}/>'
              f'<clipPath id="hc"><circle cx="100" cy="102" r="29"/></clipPath><g clip-path="url(#hc)">'
              f'<path d="M68 96 C84 88 104 92 120 112 C124 124 128 132 134 140 L108 140 C96 124 80 118 68 112 Z" fill="#1d1a19"/>'   # máscara negra
              f'<path d="M64 116 C84 120 100 130 114 140 L94 142 C84 132 72 126 64 124 Z" fill="#fbf6ea"/>'                            # bigote blanco
              f'<path d="M60 128 C80 130 100 140 110 156 L60 156 Z" fill="#fbf6ea"/></g>'
              f'<circle cx="100" cy="102" r="29" fill="none" stroke="{OUT}" stroke-width="3.5"/>'
              + ojo(90, 98, 4.6, lid='#1d1a19') + '</g>')
    return svg('Pepitero Chico', css((120, 130), (200, 222), tf=1.5), f'{legs}{cola}{cuerpo}{ala}{cabeza}')


# ───────────────────────── Atajacaminos Tijera (Hydropsalis torquata) ─────────────────────────
def atajacaminos():
    cola = (f'<g id="m-tail">'
            f'<path d="M248 222 C280 220 312 214 340 204 C316 224 286 238 250 246 Z" {S("#6a5a48", 3)}/>'
            f'<path d="M252 230 C282 232 312 240 342 256 C310 252 280 252 250 244 Z" {S("#5a4a3a", 3)}/>'
            f'<path d="M266 222 l6 14 M284 218 l5 14 M302 212 l5 12 M270 242 l-2 -10 M290 246 l-2 -10 M310 252 l-2 -10" stroke="#f1ead8" stroke-width="3.4" stroke-linecap="round"/></g>')
    cuerpo_d = 'M94 196 C84 226 100 262 146 268 C196 272 244 262 262 240 C268 218 244 200 196 194 C160 190 112 184 94 196 Z'
    cuerpo = (f'<path d="{cuerpo_d}" {S("#85735c")}/>'
              f'<clipPath id="cc"><path d="{cuerpo_d}"/></clipPath><g clip-path="url(#cc)">'
              f'<path d="M80 236 C120 256 190 262 270 240 L270 280 L80 280 Z" fill="#b6a68a"/>'
              + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .7:.1f}" fill="#3b3024"/>' for x, y, r in
                        [(116, 214, 4), (136, 204, 4.4), (158, 212, 4), (182, 204, 5), (206, 214, 4.4), (228, 222, 4), (124, 236, 4), (150, 244, 4.6), (176, 250, 4), (206, 246, 4.6), (232, 240, 4)])
              + '</g>'
              f'<path d="{cuerpo_d}" fill="none" stroke="{OUT}" stroke-width="3.5" stroke-linejoin="round"/>')
    ala = (f'<path d="M126 208 C160 196 214 202 258 234 C226 252 170 252 134 232 Z" {S("#7a6650", 3)}/>'
           f'<path d="M150 218 L232 238 M146 230 L214 246" stroke="#e8dcc0" stroke-width="3.8" stroke-linecap="round"/>'
           + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="2.4" fill="#3b3024"/>' for x, y in [(164, 210), (184, 212), (204, 220), (226, 230), (176, 226)]))
    cabeza = (f'<g id="m-head">'
              f'<path d="M62 192 L50 196 L62 200 Z" {S("#4a3d34", 2.6)}/>'
              f'<path d="M58 188 l-8 -5 M60 198 l-8 5" stroke="{OUT}" stroke-width="2" stroke-linecap="round"/>'
              f'<ellipse cx="98" cy="190" rx="38" ry="31" {S("#8a7862")}/>'
              f'<clipPath id="hc"><ellipse cx="98" cy="190" rx="38" ry="31"/></clipPath><g clip-path="url(#hc)">'
              f'<path d="M60 176 Q98 150 142 178 L142 186 Q98 164 60 190 Z" fill="#4e4132"/>'
              f'<path d="M116 210 C128 196 142 196 150 206 L150 230 L112 230 Z" fill="#b5683a"/>'
              + ''.join(f'<circle cx="{x}" cy="{y}" r="2.8" fill="#3b3024"/>' for x, y in [(80, 178), (96, 170), (112, 176), (88, 206), (104, 212), (120, 190)])
              + f'<path d="M62 202 Q76 198 88 203" stroke="#ece0c4" stroke-width="3.6" fill="none" stroke-linecap="round"/></g>'
              f'<ellipse cx="98" cy="190" rx="38" ry="31" fill="none" stroke="{OUT}" stroke-width="3.5"/>'
              + ojo(80, 186, 9, col='#0d0906', ring='#3a2e24', rr=3.2, lid='#8a7862')
              + f'<path d="M72 176 q10 -8 22 -4" stroke="#ece0c4" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
    return svg('Atajacaminos Tijera', css((112, 206), (252, 232), hb=.6, tf=.5, blink='6.5s'), f'{cola}{cuerpo}{ala}{cabeza}')




# ───────────────────────── ayudas para el resto ─────────────────────────
def patas(pares, col, w=5.5, y0=None, ground=270, toes=(-20, -14, 9)):
    out = ''
    for hip, foot in pares:
        hx, hy = hip
        t = ''.join(f'M{foot} {ground} L{foot + dx} {ground + (4 if i == 0 else 11 if i == 1 else 7)}' for i, dx in enumerate(toes))
        out += (f'<path d="M{hx} {hy} L{foot} {ground}" stroke="{OUT}" stroke-width="{w + 3.5}" stroke-linecap="round"/>'
                f'<path d="M{hx} {hy} L{foot} {ground}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
                f'<path d="{t}" stroke="{OUT}" stroke-width="{w * .8 + 3.5}" stroke-linecap="round"/>'
                f'<path d="{t}" stroke="{col}" stroke-width="{w * .8}" stroke-linecap="round"/>')
    return out


def cuerpo(d, base, inner='', idn='cc'):
    return (f'<path d="{d}" {S(base)}/><clipPath id="{idn}"><path d="{d}"/></clipPath><g clip-path="url(#{idn})">{inner}</g>'
            f'<path d="{d}" fill="none" stroke="{OUT}" stroke-width="3.5" stroke-linejoin="round"/>')


def cola(d, col, tipcol=None, tipd='', extra='', w=3):
    t = ''
    if tipcol:
        t = f'<clipPath id="tc"><path d="{d}"/></clipPath><g clip-path="url(#tc)"><path d="{tipd}" fill="{tipcol}"/></g><path d="{d}" fill="none" stroke="{OUT}" stroke-width="{w}" stroke-linejoin="round"/>'
    return f'<g id="m-tail"><path d="{d}" {S(col, w)}/>{t}{extra}</g>'


def ala(d, col, extra=''):
    return f'<path d="{d}" {S(col, 3)}/>{extra}'


def cabeza(cx, cy, r, base, inner='', bill='', bill_col='#3a3030', eye=None, pre='', post='', rx=None, ry=None):
    rx = rx or r
    ry = ry or r
    return (f'<g id="m-head">{pre}<path d="{bill}" {S(bill_col, 3)}/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {S(base)}/>'
            f'<clipPath id="hc"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath><g clip-path="url(#hc)">{inner}</g>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{OUT}" stroke-width="3.5"/>{eye or ""}{post}</g>')


def pico_cono(x, y, L, D, curve=0):
    return f'M{x} {y - D / 2} L{x - L} {y + 3 + curve} L{x} {y + D / 2} Z'


# ───────────────────────── Aguatero ─────────────────────────
def aguatero():
    legs = patas([((166, 224), 158), ((190, 222), 184)], '#a9b27a', 6)
    tl = cola('M240 190 C262 188 274 196 278 206 C262 214 246 210 238 204 Z', '#4a3a2e')
    cd = 'M104 196 C98 160 150 146 202 156 C248 164 264 198 244 222 C220 246 150 250 118 234 C106 226 104 212 104 196 Z'
    cu = cuerpo(cd, '#4a3a2e',
                '<path d="M96 206 C130 238 200 246 262 214 L262 270 L96 270 Z" fill="#f4efe2"/>'
                '<path d="M128 160 Q168 140 214 164" stroke="#dba52e" stroke-width="7" fill="none" stroke-linecap="round"/>'
                '<path d="M126 176 Q168 156 220 180" stroke="#dba52e" stroke-width="5" fill="none" stroke-linecap="round"/>'
                + ''.join(f'<circle cx="{x}" cy="{y}" r="3.6" fill="#f4efe2"/>' for x, y in [(160, 184), (182, 190), (204, 194), (170, 202), (196, 208), (146, 196)]) +
                '<path d="M100 178 C108 214 120 226 134 230 L134 196 Z" fill="#f4efe2"/>')
    hd = cabeza(96, 148, 29, '#6e2f26',
                '<path d="M64 114 Q96 100 132 122 L132 130 Q96 112 64 128 Z" fill="#ecd8a4"/>'
                '<path d="M64 140 Q92 132 128 142" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>',
                'M74 142 C52 144 34 158 24 188 C36 172 54 166 76 164 Z', '#b9b44a',
                ojo(86, 146, 4.4, lid='#6e2f26'),
                post='<circle cx="25" cy="187" r="4" fill="#e8902a"/>')
    return svg('Aguatero', css((120, 178), (240, 196), hb=.9, tf=.6), f'{legs}{tl}{cu}{hd}')


# ───────────────────────── Pitiayumí ─────────────────────────
def pitiayumi():
    legs = patas([((142, 206), 138), ((166, 206), 162)], '#4a4a4a', 4.5)
    tl = cola('M204 186 C236 192 268 214 288 244 C262 242 232 228 204 208 Z', '#5d7890')
    cd = 'M98 126 C84 148 96 188 124 204 C154 218 196 206 206 184 C210 162 188 138 162 126 C142 114 112 114 98 126 Z'
    cu = cuerpo(cd, '#f2c230',
                '<path d="M80 100 C110 116 150 100 214 130 L214 150 C170 140 120 150 70 130 Z" fill="#6f8fa8"/>'
                '<path d="M120 126 C150 116 190 124 210 140 L206 156 C170 142 140 140 114 150 Z" fill="#8aa84a"/>'
                '<path d="M84 140 C100 160 120 170 142 172 C136 150 120 140 96 134 Z" fill="#ec8a35"/>', 'cc')
    wg = ala('M122 140 C150 134 186 146 202 176 C180 196 146 190 126 168 Z', '#587a94',
             '<path d="M138 150 q24 6 40 24 M130 160 q24 6 40 26" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>')
    hd = cabeza(94, 108, 22, '#6f8fa8',
                '<path d="M70 118 C90 130 110 126 120 112 L120 136 L70 136 Z" fill="#ec8a35"/>',
                pico_cono(74, 110, 22, 7, 1), '#2d2a2a', ojo(84, 104, 4, lid='#6f8fa8'),
                post='<path d="M78 98 Q86 93 94 97" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    return svg('Pitiayumí', css((118, 132), (206, 190), tf=1.3), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Chiricote ─────────────────────────
def chiricote():
    legs = patas([((164, 218), 152), ((190, 214), 194)], '#e0736a', 8, toes=(-26, -18, 12))
    tl = cola('M236 128 C250 112 262 98 276 94 C280 112 272 134 252 150 Z', '#26221f')
    cd = 'M102 146 C106 120 160 112 204 122 C242 132 258 164 240 192 C220 220 160 226 126 208 C108 196 98 166 102 146 Z'
    cu = cuerpo(cd, '#6e6a3a',
                '<path d="M80 168 C120 160 170 170 200 150 C240 160 270 190 262 230 L90 232 Z" fill="#c4682a"/>'
                '<path d="M90 118 C120 112 126 140 116 170 L84 170 Z" fill="#8c959d"/>')
    wg = ala('M126 140 C160 128 216 138 240 170 C214 200 160 196 130 170 Z', '#6a6b3a',
             '<path d="M160 148 q22 18 14 40 M186 146 q24 18 16 38" stroke="#4a4a28" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    hd = cabeza(92, 98, 25, '#8c959d', '', 'M70 92 L30 100 Q28 106 34 108 L70 108 Z', '#cdc93a', ojo(84, 94, 4.8, col='#b3211e', lid='#8c959d'),
                pre='<path d="M122 144 L100 112" stroke="#2a1f14" stroke-width="40" stroke-linecap="round"/><path d="M122 144 L100 112" stroke="#8c959d" stroke-width="33" stroke-linecap="round"/>')
    return svg('Chiricote', css((122, 140), (240, 140), tf=1.5), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Golondrina Ceja Blanca ─────────────────────────
def golondrina():
    legs = patas([((142, 222), 140), ((164, 224), 164)], '#5a4a40', 4.2, toes=(-14, -9, 7))
    tl = cola('M210 214 C236 226 262 250 286 280 L266 258 L282 292 C250 276 226 252 204 232 Z', '#1f5f84')
    cd = 'M100 128 C86 152 96 202 130 228 C160 248 202 240 216 220 C222 198 202 162 174 138 C152 120 114 116 100 128 Z'
    cu = cuerpo(cd, '#fbfaf6',
                '<path d="M70 110 C110 128 160 118 226 150 L226 170 C170 156 124 170 78 144 Z" fill="#2b7ea0"/>'
                '<path d="M120 126 C160 128 214 168 232 240 L196 244 C190 200 150 160 112 150 Z" fill="#2b7ea0"/>')
    wg = ala('M122 136 C164 138 214 176 270 266 C226 262 176 226 140 176 Z', '#1d5a78',
             '<path d="M150 154 C186 170 220 200 250 250" stroke="#2b7ea0" stroke-width="3.4" fill="none" stroke-linecap="round" opacity=".7"/>')
    hd = cabeza(96, 108, 22, '#2b7ea0', '<path d="M64 124 C84 130 104 126 116 116 L116 140 L64 140 Z" fill="#fbfaf6"/>',
                pico_cono(76, 110, 14, 7), '#1c1c1c', ojo(86, 104, 3.8, lid='#2b7ea0'),
                post='<circle cx="80" cy="96" r="3.4" fill="#fff"/>')
    return svg('Golondrina Ceja Blanca', css((120, 128), (210, 218), hb=.8, tf=1.2), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Pijuí Frente Gris ─────────────────────────
def pijui():
    legs = patas([((140, 208), 136), ((166, 208), 162)], '#6a5a4c', 4.6)
    tl = cola('M214 168 C262 162 306 164 340 174 C304 184 262 190 216 188 Z', '#a8502c',
              extra='<path d="M232 174 L322 172 M232 180 L320 178" stroke="#7a3820" stroke-width="2.4" stroke-linecap="round"/>')
    cd = 'M96 164 C94 138 150 132 196 144 C228 154 228 188 202 204 C170 220 120 216 104 192 Z'
    cu = cuerpo(cd, '#8a6c4a',
                '<path d="M80 176 C104 190 150 200 220 190 L220 230 L80 230 Z" fill="#b3a496"/>'
                '<path d="M84 160 C100 170 116 176 130 176 L130 196 L84 196 Z" fill="#e0d4c2"/>')
    wg = ala('M128 150 C160 140 210 150 224 184 C196 202 150 196 130 176 Z', '#b5502a',
             '<path d="M150 158 q24 10 32 30 M170 154 q22 12 30 30" stroke="#8a3a1e" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    hd = cabeza(94, 144, 26, '#8a6c4a',
                '<path d="M60 112 C80 108 108 112 124 132 L124 124 C110 100 78 96 60 104 Z" fill="#b5502a"/>'
                '<path d="M62 132 L90 124 L96 132 L62 140 Z" fill="#6e665e"/><path d="M62 156 C82 160 104 166 118 176 L62 176 Z" fill="#e0d4c2"/>',
                pico_cono(70, 146, 26, 7, 2), '#3a2e28', ojo(84, 140, 4.4, col='#7a2a1e', lid='#8a6c4a'))
    return svg('Pijuí Frente Gris', css((120, 160), (214, 176), tf=1.1), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Monterita de Collar ─────────────────────────
def monterita():
    legs = patas([((150, 226), 146), ((172, 224), 170)], '#4e4e50', 4.8)
    tl = cola('M200 202 C234 212 262 234 282 262 C256 262 224 244 196 226 Z', '#4e545a')
    cd = 'M106 128 C90 152 98 198 126 220 C150 238 196 236 212 216 C220 196 204 158 176 134 C156 118 122 114 106 128 Z'
    cu = cuerpo(cd, '#8f969b',
                '<path d="M80 150 C100 168 126 184 150 200 C168 216 190 232 214 224 L214 270 L80 270 Z" fill="#f6f3ec"/>'
                '<path d="M90 156 Q124 190 160 160" stroke="#1d1b1a" stroke-width="11" fill="none" stroke-linecap="round"/>'
                '<ellipse cx="200" cy="228" rx="18" ry="10" fill="#a8532e"/>')
    wg = ala('M132 140 C162 134 200 152 214 190 C192 222 160 216 140 190 C126 170 126 152 132 140 Z', '#767d84',
             '<path d="M156 154 q22 18 22 44" stroke="#e6e9eb" stroke-width="4" fill="none" stroke-linecap="round"/>')
    hd = cabeza(100, 102, 27, '#8f969b',
                '<path d="M66 100 L128 90 L128 78 L66 78 Z" fill="#8f969b"/>'
                '<path d="M64 94 Q92 82 130 98" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
                '<path d="M64 108 C84 100 108 100 126 112 C114 126 90 124 64 116 Z" fill="#1d1b1a"/>'
                '<path d="M62 124 C84 128 104 134 116 144 L62 144 Z" fill="#fbfaf6"/>',
                pico_cono(76, 106, 20, 9), '#59595c', ojo(90, 106, 4.4, lid='#1d1b1a'))
    return svg('Monterita de Collar', css((124, 134), (200, 206), tf=1.4), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Pepitero Gris ─────────────────────────
def pepitero_gris():
    legs = patas([((152, 228), 148), ((176, 226), 172)], '#4a4545', 6)
    tl = cola('M198 212 C232 218 270 238 298 266 C288 276 262 270 236 258 C214 246 196 232 188 224 Z', '#5a5752')
    cd = 'M104 122 C86 150 94 198 122 222 C148 244 198 240 216 218 C224 194 208 156 178 130 C158 112 122 108 104 122 Z'
    cu = cuerpo(cd, '#6f7780',
                '<path d="M92 156 C110 190 140 206 170 190 C196 200 220 214 224 232 L224 280 L90 280 Z" fill="#d9a066"/>'
                '<path d="M84 132 C112 142 134 150 146 164 C134 184 108 188 84 170 Z" fill="#8a9096"/>')
    wg = ala('M130 138 C162 132 202 152 218 192 C194 224 160 216 138 190 C124 170 124 150 130 138 Z', '#5e666f',
             '<path d="M152 152 q22 18 24 44 M170 146 q24 20 28 46" stroke="#454c54" stroke-width="3" fill="none" stroke-linecap="round"/>')
    hd = cabeza(98, 100, 30, '#6f7780',
                '<path d="M62 124 C82 128 104 136 118 150 L62 150 Z" fill="#fff"/>'
                '<path d="M66 112 C88 114 108 126 120 140" stroke="#1d1a19" stroke-width="4.4" fill="none" stroke-linecap="round"/>'
                '<path d="M66 84 Q88 76 112 86" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>',
                'M74 94 C58 92 44 100 38 112 C54 112 66 112 76 114 Z', '#2b2a2a', ojo(86, 98, 4.8, lid='#6f7780'))
    return svg('Pepitero Gris', css((124, 132), (200, 216), tf=1.1), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Inambú Montaraz ─────────────────────────
def inambu_montaraz():
    legs = patas([((192, 228), 188), ((160, 228), 156)], '#e0a07a', 7, toes=(-24, -16, 10))
    cd = 'M108 180 C100 208 128 238 176 242 C226 246 268 226 274 198 C278 172 246 156 204 154 C160 152 118 158 108 180 Z'
    cu = cuerpo(cd, '#e6dcc4',
                ''.join(f'<path d="M{124 + i * 18} {164 + (i % 2) * 6} q8 16 {-2 + i} 34" stroke="#4a4036" stroke-width="5" fill="none" stroke-linecap="round"/>' for i in range(8))
                + ''.join(f'<path d="M{132 + i * 20} {210 + (i % 2) * 4} q8 8 0 16" stroke="#7a6a54" stroke-width="3.4" fill="none" stroke-linecap="round"/>' for i in range(6)))
    wg = ala('M144 176 C176 160 228 164 258 196 C232 214 178 214 148 196 Z', '#8a8678',
             ''.join(f'<path d="M{160 + i * 18} {174 + i * 2} q8 12 0 26" stroke="#f0ebdc" stroke-width="3.6" fill="none" stroke-linecap="round"/>' for i in range(5)))
    tl = '<g id="m-tail"><path d="M250 176 C264 170 276 176 282 186 C270 194 256 194 248 190 Z" ' + S('#6a6558', 3) + '/></g>'
    hd = cabeza(90, 106, 19, '#cdc3aa',
                '<path d="M64 88 Q90 80 116 96 L116 88 Q90 70 64 78 Z" fill="#26231f"/>'
                '<path d="M66 100 Q86 94 112 102" stroke="#f1ead6" stroke-width="4" fill="none" stroke-linecap="round"/>',
                'M74 104 C56 102 42 110 32 128 C44 120 58 118 76 118 Z', '#6a5648', ojo(84, 104, 4.2, ring='#f4ead0', rr=2, lid='#cdc3aa'),
                pre='<path d="M108 176 L90 124" stroke="#2a1f14" stroke-width="30" stroke-linecap="round"/><path d="M108 176 L90 124" stroke="#d6cdb6" stroke-width="23.5" stroke-linecap="round"/>',
                post='<path d="M84 84 l-4 -18 M92 82 l0 -22 M100 84 l6 -18 M108 88 l10 -14" stroke="#26231f" stroke-width="5" stroke-linecap="round"/>')
    return svg('Inambú Montaraz', css((110, 172), (250, 182), peck=True, tf=.4), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Inambú Silbón ─────────────────────────
def inambu_silbon():
    legs = patas([((190, 236), 186), ((158, 236), 154)], '#e3c75a', 6.5, toes=(-22, -14, 10))
    cd = 'M96 190 C90 232 128 252 180 252 C238 252 276 224 270 184 C264 148 220 132 170 136 C122 140 100 160 96 190 Z'
    cu = cuerpo(cd, '#6a7a8c',
                '<path d="M80 200 C110 230 160 240 220 218 L270 270 L80 270 Z" fill="#9aa4ae"/>'
                + ''.join(f'<circle cx="{x}" cy="{y}" r="3.2" fill="#f2f4f6"/>' for x, y in
                          [(116, 176), (132, 160), (150, 148), (170, 158), (190, 150), (212, 160), (236, 172), (126, 198), (146, 184), (166, 176), (186, 182), (208, 188), (232, 196), (140, 218), (164, 210), (188, 214), (212, 218), (110, 214), (248, 206)]))
    wg = ala('M140 170 C174 152 232 160 262 196 C236 228 176 226 146 200 Z', '#5c6a7a',
             ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#f2f4f6"/>' for x, y in [(170, 182), (194, 176), (218, 184), (186, 200), (212, 204), (236, 196)]))
    tl = '<g id="m-tail"><path d="M254 186 C268 180 280 188 284 198 C272 206 258 204 250 200 Z" ' + S('#566272', 3) + '/></g>'
    hd = cabeza(98, 134, 21, '#5c6a7a',
                '<path d="M70 112 Q98 104 126 120 L126 112 Q98 94 70 100 Z" fill="#2c3238"/>'
                '<path d="M72 124 Q92 116 122 126" stroke="#f2f4f6" stroke-width="4" fill="none" stroke-linecap="round"/>'
                '<path d="M72 134 Q92 128 120 136" stroke="#2c3238" stroke-width="3.2" fill="none" stroke-linecap="round"/>',
                'M80 134 C62 134 48 142 40 156 C54 150 68 148 82 148 Z', '#e0a8a0', ojo(90, 132, 4.4, ring='#eee', rr=2, lid='#5c6a7a'),
                pre='<path d="M120 170 L102 146" stroke="#2a1f14" stroke-width="40" stroke-linecap="round"/><path d="M120 170 L102 146" stroke="#5c6a7a" stroke-width="33" stroke-linecap="round"/>',
                post='<path d="M92 114 l-2 -14 M100 112 l2 -16 M108 114 l6 -12" stroke="#2c3238" stroke-width="4.4" stroke-linecap="round"/>')
    return svg('Inambú Silbón', css((118, 166), (254, 192), peck=True, tf=.4), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Calandrita ─────────────────────────
def calandrita():
    legs = patas([((140, 206), 136), ((164, 206), 160)], '#4a4540', 4.6)
    tl = cola('M206 172 C240 190 272 230 292 272 C270 276 238 250 206 206 Z', '#6b6b3a', 'rgb(251,248,236)', 'M250 232 L304 262 L304 300 L262 300 Z',
              '<path d="M224 190 L270 252" stroke="#4e4e2a" stroke-width="2.4" stroke-linecap="round"/>')
    cd = 'M98 158 C94 134 146 126 192 140 C226 152 226 186 200 202 C170 216 120 212 104 190 Z'
    cu = cuerpo(cd, '#8c8c4e', '<path d="M80 176 C104 190 150 202 224 190 L224 230 L80 230 Z" fill="#efe6a2"/>')
    wg = ala('M126 148 C160 138 212 150 226 184 C196 202 150 196 128 174 Z', '#7d7d42',
             '<path d="M146 156 q26 12 36 32 M160 152 q26 12 34 30" stroke="#f1ecd2" stroke-width="4" fill="none" stroke-linecap="round"/>')
    hd = cabeza(92, 142, 25, '#8c8c4e',
                '<path d="M62 150 C82 154 104 162 118 174 L62 174 Z" fill="#efe6a2"/>'
                '<path d="M62 130 Q90 120 120 134" stroke="#f1e68c" stroke-width="5" fill="none" stroke-linecap="round"/>'
                '<path d="M62 138 L112 142" stroke="#4e4e2a" stroke-width="3" stroke-linecap="round"/>',
                pico_cono(68, 144, 22, 6, 1), '#2d2a28', ojo(82, 138, 4.2, lid='#8c8c4e'))
    return svg('Calandrita', css((120, 158), (206, 178), tf=1.8), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Pecho Colorado ─────────────────────────
def pecho_colorado():
    legs = patas([((150, 226), 146), ((174, 224), 170)], '#3e3a3a', 5.6)
    tl = cola('M204 202 C230 208 254 224 270 246 C250 252 224 240 198 224 Z', '#222020')
    cd = 'M104 124 C86 152 94 200 124 224 C150 244 200 240 218 218 C226 194 210 156 180 130 C160 112 122 108 104 124 Z'
    cu = cuerpo(cd, '#1f1d1d', '<path d="M70 140 C100 150 134 156 150 178 C150 206 120 222 84 214 Z" fill="#c8203a"/>')
    wg = ala('M132 138 C164 132 204 152 220 192 C196 224 162 216 140 190 C126 170 126 152 132 138 Z', '#2a2727',
             '<path d="M156 152 q22 18 24 44" stroke="#3a3636" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    hd = cabeza(100, 104, 28, '#1f1d1d',
                '<path d="M60 120 C86 118 110 130 124 150 L60 150 Z" fill="#c8203a"/>'
                '<path d="M62 94 Q92 82 136 104" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>',
                pico_cono(76, 108, 26, 11, 1), '#55504f', ojo(88, 106, 4.6, ring=None, lid='#1f1d1d'))
    return svg('Pecho Colorado', css((126, 136), (204, 206), tf=1.2), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Chiví Común ─────────────────────────
def chivi():
    legs = patas([((142, 206), 138), ((166, 206), 162)], '#6a7078', 4.8)
    tl = cola('M204 170 C240 176 274 190 304 210 C274 214 238 204 204 190 Z', '#7a8a3e')
    cd = 'M98 156 C94 132 148 126 194 138 C226 148 226 184 200 200 C170 214 120 210 104 188 Z'
    cu = cuerpo(cd, '#8c9b4c', '<path d="M80 172 C104 188 150 200 224 188 L224 230 L80 230 Z" fill="#f1ecdc"/><path d="M90 176 C110 192 140 196 170 190 L170 206 L90 206 Z" fill="#ece3b8"/>')
    wg = ala('M126 146 C160 136 212 148 226 182 C196 200 150 194 128 172 Z', '#7a8a3e',
             '<path d="M150 154 q24 10 36 28" stroke="#5e6c2c" stroke-width="3" fill="none" stroke-linecap="round"/>')
    hd = cabeza(92, 138, 25, '#8c9b4c',
                '<path d="M62 108 L124 112 L124 128 Q92 116 62 124 Z" fill="#8d9391"/>'
                '<path d="M60 128 Q92 120 124 134" stroke="#fff" stroke-width="4.6" fill="none" stroke-linecap="round"/>'
                '<path d="M62 138 L116 144" stroke="#3b3a36" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M62 152 C84 156 104 162 118 174 L62 174 Z" fill="#f1ecdc"/>',
                'M70 138 C58 134 44 136 34 142 C48 148 62 150 72 148 Z', '#7a6a68', ojo(84, 138, 4.4, col='#7a2a1e', lid='#8c9b4c'))
    return svg('Chiví Común', css((120, 156), (204, 176), tf=1.2), f'{legs}{tl}{cu}{wg}{hd}')


# ───────────────────────── Juan Chiviro ─────────────────────────
def juan_chiviro():
    legs = patas([((152, 228), 148), ((176, 226), 172)], '#8a7a78', 5.8)
    tl = cola('M200 212 C228 218 258 236 280 262 C262 270 238 262 214 248 C198 238 190 226 190 220 Z', '#6f8c34')
    cd = 'M102 122 C84 150 92 198 122 222 C148 244 198 240 216 218 C224 194 208 156 178 130 C158 112 120 108 102 122 Z'
    cu = cuerpo(cd, '#7f9a3c',
                '<path d="M86 160 C110 194 140 204 172 192 C200 202 222 216 226 234 L226 280 L84 280 Z" fill="#efe3b8"/>'
                '<path d="M84 142 C112 148 138 156 150 168 C142 190 112 196 84 178 Z" fill="#e8c43a"/>')
    wg = ala('M130 138 C162 132 202 152 218 192 C194 224 160 216 138 190 C124 170 124 150 130 138 Z', '#6f8c34',
             '<path d="M154 152 q22 18 24 44" stroke="#52701e" stroke-width="3" fill="none" stroke-linecap="round"/>')
    hd = cabeza(98, 100, 31, '#8b9296',
                '<path d="M60 76 C80 66 108 66 130 84 L130 70 L60 70 Z" fill="#9aa0a4"/>'
                '<path d="M62 92 Q92 80 130 96" stroke="#b5683a" stroke-width="6" fill="none" stroke-linecap="round"/>'
                '<path d="M62 126 C86 130 104 138 118 152 L62 152 Z" fill="#e8c43a"/>',
                'M72 96 C56 94 40 98 32 110 C36 120 50 124 66 118 C58 116 52 112 54 108 C62 108 70 108 76 110 Z', '#a09290', ojo(86, 98, 5.2, col='#e8742a', ring=None, lid='#8b9296'))
    return svg('Juan Chiviro', css((124, 134), (200, 218), tf=1.1), f'{legs}{tl}{cu}{wg}{hd}')


MANO = {'colorada': colorada, 'pepitero-chico': pepitero_chico, 'atajacaminos-tijera': atajacaminos,
        'aguatero': aguatero, 'pitiayumi': pitiayumi, 'chiricote': chiricote, 'golondrina-ceja-blanca': golondrina,
        'pijui-frente-gris': pijui, 'monterita-de-collar': monterita, 'pepitero-gris': pepitero_gris,
        'inambu-montaraz': inambu_montaraz, 'inambu-silbon': inambu_silbon, 'calandrita': calandrita,
        'pecho-colorado': pecho_colorado, 'chivi-comun': chivi, 'juan-chiviro': juan_chiviro}
