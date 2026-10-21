#!/usr/bin/env python3
"""Procesa fotos de Lightroom -> fotos finales del sitio. Uso: procesar.py ENTRADA SALIDA EXISTENTES.txt
ENTRADA tiene subcarpetas album/ y galeria/. SALIDA recibe fotos/, galeria/, fotos.json."""
import sys, os, re, json, difflib, unicodedata
from PIL import Image, ImageOps
ent, sal, exist_f = sys.argv[1:4]
AVES = json.load(open('/tmp/aves_rows.json'))          # [id, cientifico, comun]
def norm(x): return ' '.join(''.join(c for c in unicodedata.normalize('NFD', x.lower()) if unicodedata.category(c) != 'Mn').split())
POR = {norm(c): (i, s, c) for i, s, c in AVES}
existentes = set(l.strip() for l in open(exist_f) if l.strip())   # nombres cientificos con foto principal
ficha_prev = os.path.join(sal, 'fotos.json')
FJ = json.load(open(ficha_prev)) if os.path.exists(ficha_prev) else {'fotos': {}}
rx = re.compile(r'^(\d{2})(\d{2})(\d{4})-(.+?)-(.+)\.(jpe?g|png|webp)$', re.I)
avisos, hechos = [], []

def guardar(im, ruta, lado, q=85):
    im = ImageOps.exif_transpose(im).convert('RGB'); im.thumbnail((lado, lado), Image.LANCZOS)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    im.save(ruta, 'JPEG', quality=q, optimize=True, progressive=True, icc_profile=im.info.get('icc_profile'))
    return os.path.getsize(ruta)

def especie(txt):
    k = norm(txt)
    if k in POR: return POR[k], None
    m = difflib.get_close_matches(k, POR.keys(), 1, 0.85)
    return (POR[m[0]], f'"{txt.strip()}" -> "{POR[m[0]][2]}"') if m else (None, None)

for tipo in ('album', 'galeria'):
    d = os.path.join(ent, tipo)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if f.startswith('.') or f.upper().startswith('LEEME'): continue
        m = rx.match(f)
        if not m: avisos.append(f'{tipo}/{f}: nombre no reconocido (esperaba DDMMAAAA-DSC_0000-nombre común.jpg)'); continue
        dd, mm, aa, cam, com = m.groups()[:5]; fecha = f'{aa}-{mm}-{dd}'
        sp, corr = especie(com)
        if not sp: avisos.append(f'{tipo}/{f}: no reconozco la especie "{com.strip()}"'); continue
        if corr: avisos.append(f'{tipo}/{f}: corregí el nombre {corr}')
        id_, sci, comun = sp; im = Image.open(os.path.join(d, f)); base = f'{dd}{mm}{aa}-{cam.strip()}'
        if tipo == 'album':
            slug = sci.lower().replace(' ', '_')
            rel = f'mas/{slug}/{base}.jpg'; dest = os.path.join(sal, 'fotos', rel)
            if os.path.exists(dest): avisos.append(f'{tipo}/{f}: ya existe {rel}, no la piso'); continue
            sz = guardar(im, dest, 1280)
            if slug not in existentes:
                guardar(im, os.path.join(sal, 'fotos', f'{slug}.jpg'), 640); existentes.add(slug); avisos.append(f'{comun}: no tenia foto principal, la primera ({f}) pasó a serlo')
            lst = FJ['fotos'].setdefault(str(id_), {'especie': sci, 'fotos': []})['fotos']
            lst.append({'f': rel, 'd': fecha}); lst.sort(key=lambda x: x['f'])
            hechos.append((f, f'fotos/{rel}', sz))
        else:
            nombre = f'{base}-{norm(com)}.jpg'; dest = os.path.join(sal, 'galeria', nombre)
            if os.path.exists(dest): avisos.append(f'{tipo}/{f}: ya existe {nombre}, no la piso'); continue
            hechos.append((f, f'galeria/{nombre}', guardar(im, dest, 1280)))
from datetime import date
FJ['generado'] = date.today().isoformat()
json.dump(FJ, open(ficha_prev, 'w'), ensure_ascii=False, indent=1)
for h in hechos: print('OK ', h[0][:44].ljust(44), '->', h[1], f'{h[2]//1024} KB')
for a in avisos: print('AVISO', a)
