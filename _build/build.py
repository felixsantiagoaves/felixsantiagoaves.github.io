#!/usr/bin/env python3
"""Arma las páginas del sitio (index.html, album/, mapa/, galeria/, estadisticas/, contacto/)
a partir de _build/fragmentos/*.html + _build/comunes.html + la plantilla de este archivo.
Uso (desde la raíz del repo):  python3 _build/build.py
Editar el contenido de una sección = editar su fragmento y volver a correr este script."""
import os, json, hashlib, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = 'https://felixsantiago.com.ar/'
esc = lambda t: html.escape(t, quote=True)
rd = lambda p: open(os.path.join(R, p), encoding='utf-8').read()
VER = hashlib.md5(b''.join(open(os.path.join(R, 'assets', f), 'rb').read() for f in ('site.css', 'site.js', 'datos.js'))).hexdigest()[:8]

PAGINAS = [
 # id, carpeta, fragmento, título, descripción, ruta nav
 ('sobre-mi', '', 'sobre-mi', 'Félix Santiago Aves · Aves de Córdoba y Argentina',
  'Diario de campo visual de Félix Santiago Allendes: álbum de aves de Córdoba y Argentina, mapa interactivo de salidas y galería de fotos de aves. Desde Río Cuarto, Córdoba.'),
 ('album', 'album', 'album', 'Álbum de aves de Córdoba y Argentina · Félix Santiago Aves',
  'Álbum de las aves que fotografié y registré en Córdoba y toda Argentina: buscá por nombre, grupo o lugar y abrí la ficha de cada especie.'),
 ('mapa', 'mapa', 'mapa', 'Mapa de mis salidas de campo · Félix Santiago Aves',
  'Mapa interactivo de mis salidas de campo: los lugares de Córdoba y Argentina donde observé aves, con la lista de especies de cada uno.'),
 ('galeria', 'galeria', 'galeria', 'Galería de fotos de aves · Félix Santiago Aves',
  'Mis mejores fotos de aves de Córdoba y Argentina, con la especie, la fecha y el lugar de cada encuentro.'),
 ('datos', 'estadisticas', 'datos', 'Estadísticas de mi lista de aves · Félix Santiago Aves',
  'Estadísticas de mi lista de aves: cuántas especies registré, cómo creció mi álbum mes a mes y cuáles me faltan por grupo.'),
 ('redes', 'contacto', 'redes', 'Contacto y licencias de fotos · Félix Santiago Aves',
  'Contacto de Félix Santiago Allendes: escribime para colaboraciones, notas, salidas de campo o para pedir permiso de uso de mis fotos de aves. Mis redes.'),
]
NAV = [('sobre-mi', '/', 'Sobre mí'), ('album', '/album/', 'Álbum'), (None, '/aves/', 'Especies'), ('mapa', '/mapa/', 'Mapa'),
       ('galeria', '/galeria/', 'Galería'), ('datos', '/estadisticas/', None), ('redes', '/contacto/', 'Contacto')]
HOME_LD = rd('_build/jsonld_home.json').replace(B + '#redes', B + 'contacto/')
LD_GRAPH = json.loads(HOME_LD)['@graph']
COMUNES = rd('_build/comunes.html')
ICONOS = '''<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">'''

def nav(activo):
    li = []
    for pid, url, nombre in NAV:
        cls = ' class="active"' if pid == activo else ''
        if pid == 'datos': lab = '<span class="nl-l">Estadísticas</span><span class="nl-c">Stats</span>'
        elif pid == 'album': lab = 'Álbum<span class="nav-badge" id="nav-album-badge"></span>'
        else: lab = nombre
        idattr = ' id="nav-album"' if pid == 'album' else ''
        lic = ' class="nav-stats"' if pid == 'datos' else ''
        li.append(f'      <li{lic}><a href="{url}"{idattr}{cls}>{lab}</a></li>')
    return ('<nav>\n  <div class="nav-i">\n    <div class="nav-logo"><a href="/"><img src="/logo-nav.png" alt="Felix Santiago Aves" style="height:38px;display:block;"></a></div>\n'
            '    <ul class="nav-links">\n' + '\n'.join(li) + '\n    </ul>\n  </div>\n</nav>')

def ld(pid, carpeta, titulo, desc, url):
    if pid == 'sobre-mi': return HOME_LD
    g = [x for x in LD_GRAPH if x['@type'] in ('WebSite', 'Person')]
    g.append({'@type': 'WebPage', '@id': url, 'url': url, 'name': titulo, 'description': desc, 'inLanguage': 'es-AR', 'isPartOf': {'@id': B + '#web'}, 'author': {'@id': B + '#felix'}})
    g.append({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': B}, {'@type': 'ListItem', 'position': 2, 'name': titulo.split(' · ')[0], 'item': url}]})
    if pid == 'galeria':
        g += [dict(x, url=url) for x in LD_GRAPH if x['@type'] == 'ImageGallery']
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False)

HOME_REDIR = '''<script>(function(){var h=location.hash.slice(1),m={album:'/album/',mapa:'/mapa/',galeria:'/galeria/',datos:'/estadisticas/',redes:'/contacto/'};if(m[h])location.replace(m[h]);else if(h.indexOf('ave-')===0)location.replace('/album/#'+h);})();</script>
'''

for pid, carpeta, frag, titulo, desc in PAGINAS:
    url = B + (carpeta + '/' if carpeta else '')
    page = f'''<!DOCTYPE html>
<html lang="es">
<!-- Página generada con _build/build.py: para cambiarla, editar _build/fragmentos/{frag}.html (o assets/) y volver a correr el script. Guía completa: _build/LEEME-CLAUDE.md -->
<head>
<meta charset="UTF-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-X5B10D1495"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-X5B10D1495');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#3f4733">
<script>try{{if(localStorage.getItem("tema")==="dark")document.documentElement.dataset.theme="dark"}}catch(e){{}}</script>
{HOME_REDIR if pid == 'sobre-mi' else ''}<script type="application/ld+json">
{ld(pid, carpeta, titulo, desc, url)}
</script>
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Félix Santiago Aves">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{B}preview.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Félix Santiago Aves: diario de campo visual de aves de Argentina">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(titulo)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{B}preview.jpg">
<meta name="robots" content="index,follow,max-image-preview:large">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&family=Caveat:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={VER}">
{ICONOS}
</head>
<body>
<button class="tema-btn" id="tema-btn" onclick="toggleTema()" aria-label="Cambiar entre modo claro y modo oscuro" title="Modo oscuro">☾</button>
{nav(pid)}

{rd('_build/fragmentos/' + frag + '.html')}
{COMUNES}
<footer id="site-footer-global"></footer>
<script src="/assets/datos.js?v={VER}"></script>
<script src="/assets/site.js?v={VER}"></script>
</body>
</html>
'''
    out = os.path.join(R, carpeta, 'index.html') if carpeta else os.path.join(R, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page)
    print('OK', out.replace(R + '/', ''), len(page))
print('versión de assets:', VER)
