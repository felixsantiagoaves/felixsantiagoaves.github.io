#!/usr/bin/env python3
"""Genera las páginas individuales de especie (aves/<slug>/index.html), aves/indice.json y sitemap.xml.
Uso: gen_fichas.py RAIZ_SITIO CARPETA_FUENTES   (fuentes = fichas-src/*.json)"""
import sys, os, json, subprocess, html, re, unicodedata
from datetime import date
from urllib.parse import quote
from xml.sax.saxutils import escape as xesc
from PIL import Image

RAIZ, SRC = sys.argv[1], sys.argv[2]
import hashlib
MASCOTAS = {'carancho': 'carancho', 'gallineta-pico-pintado': 'gallineta', 'carpintero-lomo-blanco': 'carpintero'}   # slug -> personaje (assets/mascotas/)
MVER = hashlib.md5(open(os.path.join(RAIZ, 'assets', 'mascotas', 'mascotas.js'), 'rb').read()).hexdigest()[:8]
VER = hashlib.md5(open(os.path.join(RAIZ, 'aves', 'ficha.css'), 'rb').read() + open(os.path.join(RAIZ, 'aves', 'ficha.js'), 'rb').read()).hexdigest()[:8]
BASE = 'https://felixsantiago.com.ar/'
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
MES3 = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
esc = lambda s: html.escape(str(s), quote=True)
def larga(d): y, m, dd = d.split('-'); return f'{int(dd)} de {MESES[int(m)-1]} de {y}'
def corta(d): y, m, dd = d.split('-'); return f'{int(dd)} {MES3[int(m)-1]} {y}'

# Datos del sitio (AVES y FICHAS salen del index.html)
js = subprocess.run(['node', '-e', """
const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');
const i=s.indexOf('\\nconst AVES = [\\n'), j=s.indexOf('\\n];',i);
const AVES=eval('('+s.slice(i+'\\nconst AVES = '.length, j+2)+')');
const k=s.indexOf('\\nconst FICHAS = {\\n'); const e=s.indexOf('\\n};',k);
const FICHAS=eval('('+s.slice(k+'\\nconst FICHAS = '.length, e+2)+')');
process.stdout.write(JSON.stringify({AVES,FICHAS}));""", os.path.join(RAIZ, 'assets', 'datos.js')], capture_output=True, text=True, check=True).stdout
D = json.loads(js); AVES = {a['id']: a for a in D['AVES']}; FICHAS = D['FICHAS']
REG = json.load(open(os.path.join(RAIZ, 'registros.json'), encoding='utf-8'))
AVIST = json.load(open(os.path.join(RAIZ, 'avistamientos.json'), encoding='utf-8'))
FX = json.load(open(os.path.join(RAIZ, 'fotos.json'), encoding='utf-8')).get('fotos', {}) if os.path.exists(os.path.join(RAIZ, 'fotos.json')) else {}
LUG = REG['lugares']

def dims(rel):
    try:
        with Image.open(os.path.join(RAIZ, 'fotos', rel)) as im: return im.size
    except Exception: return (1280, 853)

def slugify(t):
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
def arreglar(c): return re.sub(r'\bAguila\b', 'Águila', c)
def fold(t): return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn')

# Fuentes con texto completo (por id) y lista de todas las especies con foto
FUENTES = {}
for fn in sorted(os.listdir(SRC)):
    if fn.endswith('.json'):
        S0 = json.load(open(os.path.join(SRC, fn), encoding='utf-8')); FUENTES[S0['id']] = S0
ESP = []
MIN_FOTOS = 4   # una especie tiene página propia solo si tiene la portada + al menos 3 fotos más
for sid, r in AVIST['avistamientos'].items():
    id_ = int(sid)
    if not r.get('foto') or id_ not in AVES or not os.path.exists(os.path.join(RAIZ, r['foto'])): continue
    if 1 + len(FX.get(sid, {}).get('fotos', [])) < MIN_FOTOS: continue
    ave = AVES[id_]; comun = FUENTES.get(id_, {}).get('comun') or arreglar(ave['comun'])
    w, h = dims(r['foto'].replace('fotos/', '', 1))
    ESP.append({'id': id_, 'slug': slugify(comun), 'comun': comun, 'sci': ave['nombre'], 'grupo': ave['familiaEsp'], 'thumb': '/' + r['foto'], 'w': w, 'h': h, 'completa': id_ in FUENTES, 'ok': id_ in FUENTES and bool(FX.get(str(id_), {}).get('fotos'))})
ESP.sort(key=lambda e: fold(e['comun']))
assert len({e['slug'] for e in ESP}) == len(ESP), 'slugs repetidos'
POS = {e['id']: i for i, e in enumerate(ESP)}

def otras(e):
    i = POS[e['id']]; mismo = [x for x in ESP[i+1:] + ESP[:i] if x['grupo'] == e['grupo']][:3]
    if len(mismo) < 3: mismo += [x for x in ESP[i+1:] + ESP[:i] if x not in mismo][:3 - len(mismo)]
    return mismo
def miniatura(thumb):
    """Miniatura de 400 px de la portada (fotos/th/...) para el índice; se crea si falta o si la portada cambió."""
    src = os.path.join(RAIZ, thumb.lstrip('/')); dst = os.path.join(RAIZ, 'fotos', 'th', os.path.basename(src))
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with Image.open(src) as im:
            im = im.convert('RGB'); im.thumbnail((400, 400), Image.LANCZOS); im.save(dst, 'JPEG', quality=78, optimize=True, progressive=True)
    with Image.open(dst) as im: w, h = im.size
    return '/fotos/th/' + os.path.basename(src), w, h

def tarjeta(x, cls='card', th=False):
    ins = ''
    if th:
        t, w, h = miniatura(x['thumb']); x = dict(x, thumb=t, w=w, h=h)
    return (f'<a class="{cls}" href="/aves/{x["slug"]}/">{ins}<img src="{x["thumb"]}" width="{x["w"]}" height="{x["h"]}" loading="lazy" decoding="async" alt="{esc(x["comun"])} ({esc(x["sci"])}), fotografiada por Félix Santiago">'
            f'<span class="n">{esc(x["comun"])}</span><span class="c">{esc(x["sci"])}</span></a>')

paginas = {}
for E in ESP:
    id_ = E['id']; slug = E['slug']; S = FUENTES.get(id_); base_mode = S is None
    if base_mode:
        S = {'id': id_, 'resumen': '', 'datos': [], 'secciones': [], 'fuentes': []}; ave = AVES[id_]
    else: ave = AVES[id_]
    sci, comun, grupo = E['sci'], E['comun'], E['grupo']; ficha = FICHAS.get(sci, {})
    url = f'{BASE}aves/{slug}/'
    extras = sorted(FX.get(str(id_), {}).get('fotos', []), key=lambda x: (x['d'], x['f']), reverse=True)
    reg = REG['r'].get(str(id_), {})
    def lugar_de(d):
        a = reg.get(d, []); return LUG[a[0]] if len(a) == 1 else ''
    # fotos
    fotos = []
    for x in extras:
        w, h = dims(x['f']); fotos.append({'src': f'/fotos/{quote(x["f"])}', 'abs': f'{BASE}fotos/{quote(x["f"])}', 'd': x['d'], 'lug': lugar_de(x['d']), 'w': w, 'h': h, 'f': x['f']})
    if S.get('portada'):
        fotos.sort(key=lambda p: p['f'] != S['portada'])
    principal = AVIST['avistamientos'].get(str(id_), {}).get('foto')
    if fotos: hero = fotos[0]
    elif principal:
        w, h = Image.open(os.path.join(RAIZ, principal)).size; hero = {'src': '/' + principal, 'abs': BASE + principal, 'd': '', 'lug': '', 'w': w, 'h': h, 'f': principal}
    else: hero = None
    alt = f'{comun} ({sci}), fotografiada por Félix Santiago en Argentina'
    mascota_html = (f'<div id="mascota" data-m="{MASCOTAS[slug]}" hidden></div>\n<script src="/assets/mascotas/mascotas.js?v={MVER}" defer></script>\n') if slug in MASCOTAS else ''
    # encuentros
    fechas = sorted(reg.keys(), reverse=True)
    n_foto = lambda d: sum(1 for p in fotos if p['d'] == d)
    def li(d):
        lugares = ' · '.join(LUG[i] for i in reg[d]); n = n_foto(d)
        return f'<li class="{"foto" if n else ""}"><b>{corta(d)}</b><span>{esc(lugares)}</span>' + (f'<em>📷 {n}</em>' if n else '') + '</li>'
    enc_html = ''
    if fechas:
        ver = fechas[:6]; resto = fechas[6:]
        enc_html = f'<ul class="enc">{"".join(li(d) for d in ver)}</ul>'
        if resto: enc_html += f'<details class="mas"><summary class="pill">Ver los {len(resto)} anteriores</summary><ul class="enc">{"".join(li(d) for d in resto)}</ul></details>'
    primero = ''
    if fechas:
        d0 = fechas[-1]; primero = f'<p class="primero"><strong>Primer registro</strong>{larga(d0)} · {esc(" · ".join(LUG[i] for i in reg[d0]))}</p>'
    if base_mode:
        n_lug = len({i for d in fechas for i in reg[d]})
        S['resumen'] = f'{comun} ({sci}): mis fotos y el mapa de mis avistamientos de esta especie, con la fecha y el lugar de cada encuentro.'
        S['datos'] = ([['Encuentros', str(len(fechas))], ['Lugares', str(n_lug)], ['Último registro', corta(fechas[0])]] if fechas else [])
    datos = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in S.get('datos', []))
    secs = ''.join(f'<h2>{esc(s["t"])}</h2><p>{esc(s["p"])}</p>' for s in S['secciones'])
    if base_mode:
        secs = '<div class="pendiente"><strong>Ficha en preparación</strong>Todavía no escribí la descripción de esta especie (cómo reconocerla, dónde vive, qué come y cómo nidifica). Cuando lo haga, va a tener las fuentes citadas. Mientras tanto podés ver mis fotos, el mapa de mis avistamientos y los enlaces para saber más.</div>'
    curioso = f'<div class="curioso"><strong>Dato curioso</strong>{esc(ficha["curiosidad"])}</div>' if ficha.get('curiosidad') else ''
    gal = ''
    if fotos:
        figs = ''.join(
            f'<figure><a href="{p["src"]}" data-full="{p["src"]}" data-alt="{esc(alt)}" data-cap="{esc(comun + " · " + corta(p["d"]) + (" · " + p["lug"] if p["lug"] else ""))}">'
            f'<img src="{p["src"]}" width="{p["w"]}" height="{p["h"]}" loading="lazy" decoding="async" alt="{esc(alt)}"></a>'
            f'<figcaption>{corta(p["d"])}{(" · " + esc(p["lug"])) if p["lug"] else ""}</figcaption></figure>' for p in fotos)
        gal = f'<section class="sec" id="fotos"><div class="fotos-h"><h2>Mis fotos</h2><span>{len(fotos)} {"foto" if len(fotos)==1 else "fotos"}</span></div><div class="galeria">{figs}</div></section>'
    fuentes = ''.join((f'<li><a href="{esc(f["u"])}" target="_blank" rel="noopener">{esc(f["t"])}</a></li>' if f.get('u') else f'<li>{esc(f["t"])}</li>') for f in S['fuentes'])
    q = quote(sci)
    saber = ((f'<a class="pill" href="https://es.wikipedia.org/wiki/{sci.replace(" ", "_")}" target="_blank" rel="noopener">Wikipedia</a>' if not base_mode else f'<a class="pill" href="https://es.wikipedia.org/w/index.php?search={q}" target="_blank" rel="noopener">Wikipedia</a>') +
             f'<a class="pill" href="https://xeno-canto.org/explore?query={q}" target="_blank" rel="noopener">Escuchar su canto</a>'
             f'<a class="pill" href="https://www.inaturalist.org/taxa/search?q={q}" target="_blank" rel="noopener">iNaturalist</a>')
    hero_html = ''
    if hero:
        cap = f'{corta(hero["d"])}{(" · " + esc(hero["lug"])) if hero["lug"] else ""}' if hero['d'] else ''
        hero_html = (f'<figure class="hero-fig"><div class="cr-w"><img src="{hero["src"]}" width="{hero["w"]}" height="{hero["h"]}" alt="{esc(alt)}" fetchpriority="high" id="hero-img"'
                     + (f' data-full="{hero["src"]}" data-alt="{esc(alt)}" data-cap="{esc(comun)}"' if not fotos else '')
                     + f'></div>{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>')
    title = f'{comun} ({sci}) · Félix Santiago Aves'
    imgs_ld = [{'@type': 'ImageObject', '@id': f'{url}#foto-{i+1}', 'contentUrl': p['abs'], 'name': f'{comun} ({sci})', 'caption': alt, 'creator': {'@id': BASE + '#felix'},
                'copyrightHolder': {'@id': BASE + '#felix'}, 'copyrightNotice': '© Félix Santiago Allendes. Uso solo con permiso previo y por escrito.', 'license': BASE + 'contacto/', 'acquireLicensePage': BASE + 'contacto/'}
               for i, p in enumerate(fotos[:10])]
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': url, 'url': url, 'name': title, 'description': S['resumen'], 'inLanguage': 'es-AR', 'isPartOf': {'@id': BASE + '#web'}, 'author': {'@id': BASE + '#felix'},
         'about': {'@type': 'Taxon', 'name': sci, 'alternateName': comun, 'taxonRank': 'Species', **({'sameAs': [f['u'] for f in S.get('fuentes', []) if 'wikipedia.org' in f.get('u', '')][:1]} if any('wikipedia.org' in f.get('u', '') for f in S.get('fuentes', [])) else {})}, **({'primaryImageOfPage': {'@id': f'{url}#foto-1'}} if imgs_ld else {})},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE},
            {'@type': 'ListItem', 'position': 2, 'name': 'Especies', 'item': BASE + 'aves/'},
            {'@type': 'ListItem', 'position': 3, 'name': comun, 'item': url}]}] + imgs_ld}
    og_img = (f'<meta property="og:image" content="{hero["abs"]}"><meta property="og:image:width" content="{hero["w"]}"><meta property="og:image:height" content="{hero["h"]}">'
              f'<meta property="og:image:alt" content="{esc(alt)}"><meta name="twitter:image" content="{hero["abs"]}">') if hero else ''
    i0 = POS[id_]; ant, sig = ESP[i0-1], ESP[(i0+1) % len(ESP)]
    pn_html = f'<a href="/aves/{ant["slug"]}/"><small>← Anterior</small>{esc(ant["comun"])}</a><a href="/aves/{sig["slug"]}/"><small>Siguiente →</small>{esc(sig["comun"])}</a>'
    page = f'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-X5B10D1495"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-X5B10D1495');</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(S['resumen'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#3f4733">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="es_AR"><meta property="og:site_name" content="Félix Santiago Aves">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(S['resumen'])}"><meta property="og:url" content="{url}">
{og_img}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(S['resumen'])}">
<link rel="icon" href="/favicon.ico"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script>try{{if(localStorage.getItem("tema")==="dark")document.documentElement.dataset.theme="dark"}}catch(e){{}}</script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&family=Caveat:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/aves/ficha.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<nav class="gnav"><div class="nav-i">
  <a class="nav-logo" href="/"><img src="/logo-nav.png" alt="Félix Santiago Aves" width="38" height="38"></a>
  <ul class="nav-links">
    <li><a href="/">Sobre mí</a></li>
    <li><a href="/album/">Álbum</a></li>
    <li><a class="active" href="/aves/">Especies</a></li>
    <li><a href="/mapa/">Mapa</a></li>
    <li><a href="/galeria/">Galería</a></li>
    <li class="nav-stats"><a href="/estadisticas/"><span class="nl-l">Estadísticas</span><span class="nl-c">Stats</span></a></li>
    <li><a href="/contacto/">Contacto</a></li>
  </ul>
</div></nav>
<main class="wrap">
  <p class="crumbs"><a href="/">Inicio</a> › <a href="/aves/">Especies</a> › {esc(comun)}</p>
  <div class="hero">
    {hero_html}
    <div class="hero-txt">
      <p class="grupo">{esc(grupo)}</p>
      <h1>{esc(comun)}</h1>
      <p class="sci">{esc(sci)}</p>
      {f'<p class="car">{esc(ficha["estado"])}</p>' if ficha.get('estado') else ''}
      {primero}
      <dl class="datos">{datos}</dl>
      <div class="acciones"><button class="pill fill" id="compartir" type="button">Compartir</button><a class="pill" href="/aves/">← Todas las especies</a></div>
    </div>
  </div>
  {gal}
  <div class="cols">
    <div class="texto">{curioso}{secs}</div>
    <aside>
      <section class="sec"><h2>Dónde la vi</h2><div id="mapa-ave" data-id="{id_}" role="img" aria-label="Mapa con los lugares donde registré esta especie"></div><p class="mapa-nota" id="mapa-nota"></p></section>
      {f'<section class="sec"><h2>Mis encuentros ({len(fechas)})</h2>{enc_html}</section>' if fechas else ''}
      <section class="sec"><h2>Para saber más</h2><div class="saber">{saber}</div></section>
    </aside>
  </div>
  {f'<section class="sec fuentes"><h2>Fuentes</h2><ul>{fuentes}</ul><p class="nota-fuentes">Los textos están escritos con mis palabras a partir de estas fuentes. Los datos de avistamientos y las fotos son propios.</p></section>' if S['fuentes'] else ''}
  <nav class="pn" aria-label="Otras fichas">{pn_html}</nav>
  <section class="sec otras"><h2>Otras fichas</h2><div class="grid mini">{"".join(tarjeta(x) for x in otras(E))}</div><p><a class="pill" href="/aves/">Ver todas las especies</a></p></section>
  <p class="pie">© Félix Santiago Allendes. Todas las fotografías de este sitio son de mi autoría y no pueden usarse, copiarse ni publicarse sin mi permiso previo y por escrito. Para pedir una licencia de uso, <a href="/contacto/">escribime</a>.</p>
</main>
<button class="tema-btn" id="tema-btn" type="button" aria-label="Cambiar entre modo claro y modo oscuro">☾</button>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Foto ampliada"><button class="x" aria-label="Cerrar">✕</button><button class="pv" aria-label="Anterior">‹</button><button class="nx" aria-label="Siguiente">›</button><img src="" alt=""><p><span class="cap"></span><small>© Félix Santiago Allendes · Uso solo con permiso</small></p></div>
<script src="/aves/ficha.js?v={VER}" defer></script>
{mascota_html}</body>
</html>
'''
    os.makedirs(os.path.join(RAIZ, 'aves', slug), exist_ok=True)
    open(os.path.join(RAIZ, 'aves', slug, 'index.html'), 'w', encoding='utf-8').write(page)
    paginas[str(id_)] = {'slug': slug, 'fotos': [p['abs'] for p in fotos] or ([hero['abs']] if hero else []), 'comun': comun, 'sci': sci}
    print('OK', slug, f'{len(fotos)} fotos, {len(fechas)} encuentros')

json.dump({k: v['slug'] for k, v in paginas.items()}, open(os.path.join(RAIZ, 'aves', 'indice.json'), 'w'), ensure_ascii=False)


# Índice de especies /aves/
grupos = sorted({e['grupo'] for e in ESP}, key=fold)
cards = ''.join(f'<li data-q="{esc(fold(e["comun"] + " " + e["sci"]))}" data-g="{esc(e["grupo"])}">{tarjeta(e, th=True)}</li>' for e in ESP)
opts = ''.join(f'<option value="{esc(g)}">{esc(g)}</option>' for g in grupos)
IURL = BASE + 'aves/'
ititle = 'Especies de aves que fotografié · Félix Santiago Aves'
idesc = f'{len(ESP)} especies de aves de Argentina fotografiadas por Félix Santiago, cada una con su ficha: mis fotos, el mapa de mis avistamientos y datos de la especie.'
ild = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'CollectionPage', '@id': IURL, 'url': IURL, 'name': ititle, 'description': idesc, 'inLanguage': 'es-AR', 'isPartOf': {'@id': BASE + '#web'}, 'author': {'@id': BASE + '#felix'}},
    {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE}, {'@type': 'ListItem', 'position': 2, 'name': 'Especies', 'item': IURL}]}]}
ipage = f'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-X5B10D1495"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-X5B10D1495');</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(ititle)}</title>
<meta name="description" content="{esc(idesc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#3f4733">
<link rel="canonical" href="{IURL}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_AR"><meta property="og:site_name" content="Félix Santiago Aves">
<meta property="og:title" content="{esc(ititle)}"><meta property="og:description" content="{esc(idesc)}"><meta property="og:url" content="{IURL}">
<meta property="og:image" content="{BASE}preview.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(ititle)}"><meta name="twitter:description" content="{esc(idesc)}"><meta name="twitter:image" content="{BASE}preview.jpg">
<link rel="icon" href="/favicon.ico"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script>try{{if(localStorage.getItem("tema")==="dark")document.documentElement.dataset.theme="dark"}}catch(e){{}}</script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&family=Caveat:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/aves/ficha.css?v={VER}">
<script type="application/ld+json">{json.dumps(ild, ensure_ascii=False)}</script>
</head>
<body>
<nav class="gnav"><div class="nav-i">
  <a class="nav-logo" href="/"><img src="/logo-nav.png" alt="Félix Santiago Aves" width="38" height="38"></a>
  <ul class="nav-links">
    <li><a href="/">Sobre mí</a></li>
    <li><a href="/album/">Álbum</a></li>
    <li><a class="active" href="/aves/">Especies</a></li>
    <li><a href="/mapa/">Mapa</a></li>
    <li><a href="/galeria/">Galería</a></li>
    <li class="nav-stats"><a href="/estadisticas/"><span class="nl-l">Estadísticas</span><span class="nl-c">Stats</span></a></li>
    <li><a href="/contacto/">Contacto</a></li>
  </ul>
</div></nav>
<main class="wrap">
  <p class="crumbs"><a href="/">Inicio</a> › Especies</p>
  <h1>Especies que fotografié</h1>
  <p class="intro">{len(ESP)} especies de aves que tengo bien fotografiadas, cada una con su ficha: mis fotos, el mapa de dónde la vi y datos de la especie. Se suman a medida que reúno más fotos de cada una.</p>
  <div class="filtros">
    <input type="search" id="q" placeholder="Buscar por nombre común o científico" aria-label="Buscar especie" autocomplete="off">
    <select id="g" aria-label="Filtrar por grupo"><option value="">Todos los grupos</option>{opts}</select>
  </div>
  <p class="lugar-f" id="lugar-f" hidden></p>
  <p class="cuenta" id="cuenta" aria-live="polite">{len(ESP)} especies</p>
  <ul class="grid" id="lista">{cards}</ul>
  <p class="vacio" id="vacio" hidden>No encontré ninguna especie con ese nombre.</p>
  <p class="pie">© Félix Santiago Allendes. Todas las fotografías de este sitio son de mi autoría y no pueden usarse, copiarse ni publicarse sin mi permiso previo y por escrito. Para pedir una licencia de uso, <a href="/contacto/">escribime</a>.</p>
</main>
<button class="tema-btn" id="tema-btn" type="button" aria-label="Cambiar entre modo claro y modo oscuro">☾</button>
<script src="/aves/ficha.js?v={VER}" defer></script>
<script>
(function(){{
  var q=document.getElementById('q'), g=document.getElementById('g'), c=document.getElementById('cuenta'), v=document.getElementById('vacio'), li=[].slice.call(document.querySelectorAll('#lista li')), t=li.length;
  function fold(s){{ return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,''); }}
  var ls=null;
  function f(){{ var k=fold(q.value.trim()), gr=g.value, n=0;
    li.forEach(function(e){{ var ok=(!k||e.getAttribute('data-q').indexOf(k)>-1)&&(!gr||e.getAttribute('data-g')===gr)&&(!ls||ls[e.querySelector('a').getAttribute('href').split('/')[2]]); e.hidden=!ok; if(ok) n++; }});
    c.textContent=(n===t?t+' especies':n+(n===1?' especie':' especies')+' de '+t); v.hidden=n>0; }}
  q.addEventListener('input',f); g.addEventListener('change',f);
  var lg=new URLSearchParams(location.search).get('lugar');
  if(lg!==null){{ Promise.all([fetch('/avistamientos.json').then(function(r){{return r.json();}}), fetch('/aves/indice.json').then(function(r){{return r.json();}})]).then(function(r){{
    var L=(r[0].lugares||[])[+lg]; if(!L) return; ls={{}}; L.ids.forEach(function(i){{ if(r[1][i]) ls[r[1][i]]=1; }});
    var b=document.getElementById('lugar-f'); b.hidden=false; b.innerHTML='Especies con ficha vistas en <strong></strong> ('+Object.keys(ls).length+' de '+L.ids.length+') · <a href="/aves/">ver todas</a>'; b.querySelector('strong').textContent=L.nombre; f(); }}).catch(function(){{}}); }}
}})();
</script>
</body>
</html>
'''
open(os.path.join(RAIZ, 'aves', 'index.html'), 'w', encoding='utf-8').write(ipage)
print('índice:', len(ESP), 'especies')

# Sitemap: inicio + páginas de especie, con fotos para Google Imágenes
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
def url_entry(loc, imgs, prio, freq):
    o = ['<url>', f'<loc>{loc}</loc>', f'<lastmod>{date.today().isoformat()}</lastmod>', f'<changefreq>{freq}</changefreq>', f'<priority>{prio}</priority>']
    for u, comun, sci in imgs:
        o += ['<image:image>', f'<image:loc>{u}</image:loc>', f'<image:title>{xesc(comun)} ({xesc(sci)})</image:title>',
              f'<image:caption>{xesc(comun)}, {xesc(sci)}. Fotografiada por Félix Santiago en Argentina.</image:caption>', f'<image:license>{BASE}contacto/</image:license>', '</image:image>']
    return o + ['</url>']
home = []
for sid, r in sorted(AVIST['avistamientos'].items(), key=lambda kv: int(kv[0])):
    if r.get('foto') and int(sid) in AVES: home.append((BASE + quote(r['foto']), AVES[int(sid)]['comun'], AVES[int(sid)]['nombre']))
out += url_entry(BASE, home, '1.0', 'weekly')
out += url_entry(BASE + 'aves/', [], '0.9', 'weekly')
for carp, prio in [('album', '0.9'), ('galeria', '0.8'), ('mapa', '0.7'), ('estadisticas', '0.6'), ('contacto', '0.5')]: out += url_entry(BASE + carp + '/', [], prio, 'weekly' if carp != 'contacto' else 'yearly')
for sid, p in paginas.items(): out += url_entry(f'{BASE}aves/{p["slug"]}/', [(u, p['comun'], p['sci']) for u in p['fotos'][:10]], '0.8' if FUENTES.get(int(sid)) else '0.6', 'monthly')
out += ['</urlset>', '']
open(os.path.join(RAIZ, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(out))
print('sitemap:', len(home), 'fotos en inicio,', len(paginas), 'páginas')
