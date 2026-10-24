#!/usr/bin/env python3
"""Chequea que las frases de las fichas que dependen de tus registros sigan siendo ciertas.

Correr desde la raíz del repo, SIEMPRE después de actualizar registros.json con un CSV nuevo de eBird:
    python3 -I _fichas/verificar_aperturas.py

Cada _fichas/<slug>.json puede tener una clave "apertura" que declara el hecho en que se apoya el texto:
  {"tipo": "primera",   "fecha": "AAAA-MM-DD", "lugar": "Nombre"}   -> "la primera vez fue..." (sigue valiendo salvo que cargues algo anterior)
  {"tipo": "ultima",    "fecha": "AAAA-MM-DD", "lugar": "Nombre"}   -> "la última vez, hasta ahora, fue..." (se desactualiza al volver a verla)
  {"tipo": "cualquiera","fecha": "AAAA-MM-DD", "lugar": "Nombre"}   -> "un día cualquiera" (vale mientras exista ese registro)
  {"tipo": "unica",     "fecha": "AAAA-MM-DD", "lugar": "Nombre"}   -> "la vi una sola vez" (se desactualiza al volver a verla)
  {"tipo": "mismo_lugar","n": N, "lugar": "Nombre"}                   -> "las N veces fue en el mismo lugar"
  {"tipo": "ninguna"}                                                  -> sin dato de registro en el texto
  opcionales: "min_fechas": N  (el texto dice que la ve seguido: exige al menos N fechas)
              "foto_fecha": "AAAA-MM-DD" (el texto menciona una foto de ese día: debe existir en fotos.json)
Sale con código 1 si alguna ficha quedó desactualizada y muestra qué hay que reescribir.
"""
import json, glob, os, sys
R = sys.argv[1] if len(sys.argv) > 1 else '.'
reg = json.load(open(os.path.join(R, 'registros.json'))); L = reg['lugares']
fx = json.load(open(os.path.join(R, 'fotos.json')))['fotos']
mal = 0; ok = 0; sin = []
for p in sorted(glob.glob(os.path.join(R, '_fichas', '*.json'))):
    j = json.load(open(p)); slug = os.path.basename(p)[:-5]; a = j.get('apertura')
    if a is None: sin.append(slug); continue
    r = reg['r'].get(str(j['id']), {}); ds = sorted(r); errs = []
    t = a['tipo']
    lug = lambda d: [L[i] for i in r.get(d, [])]
    if t in ('primera', 'ultima', 'cualquiera', 'unica'):
        d = a['fecha']
        if d not in r: errs.append(f'ya no hay registro del {d}')
        else:
            if a.get('lugar') and not any(a['lugar'] in x for x in lug(d)): errs.append(f'el {d} ahora figura en {lug(d)}')
            if t == 'primera' and ds[0] != d: errs.append(f'hay un registro anterior: {ds[0]}')
            if t == 'ultima' and ds[-1] != d: errs.append(f'hay un registro posterior: {ds[-1]} ({len(ds)} fechas)')
            if t == 'unica' and len(ds) != 1: errs.append(f'ya no es una sola vez: {len(ds)} fechas ({", ".join(ds)})')
    elif t == 'mismo_lugar':
        ls = {x for d in ds for x in lug(d)}
        if len(ds) != a['n']: errs.append(f'ahora son {len(ds)} fechas (el texto dice {a["n"]})')
        if len(ls) != 1 or not any(a['lugar'] in x for x in ls): errs.append(f'lugares ahora: {sorted(ls)}')
    elif t != 'ninguna': errs.append(f'tipo desconocido {t}')
    if a.get('min_fechas') and len(ds) < a['min_fechas']: errs.append(f'el texto supone al menos {a["min_fechas"]} fechas y hay {len(ds)}')
    if a.get('foto_fecha') and a['foto_fecha'] not in {x['d'] for x in fx.get(str(j['id']), {}).get('fotos', [])}: errs.append(f'no hay foto del {a["foto_fecha"]}')
    if errs: mal += 1; print(f'⚠ {slug}: ' + ' | '.join(errs))
    else: ok += 1
print(f'\n{ok} fichas al día, {mal} desactualizadas, {len(sin)} sin "apertura" declarada' + (f' ({", ".join(sin[:8])}{"…" if len(sin) > 8 else ""})' if sin else ''))
sys.exit(1 if mal else 0)
