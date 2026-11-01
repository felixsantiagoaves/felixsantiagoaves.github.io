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


MANO = {'colorada': colorada, 'pepitero-chico': pepitero_chico, 'atajacaminos-tijera': atajacaminos}
