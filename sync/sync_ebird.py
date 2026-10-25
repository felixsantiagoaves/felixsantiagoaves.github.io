#!/usr/bin/env python3
"""
sync_ebird.py - genera avistamientos.json y registros.json a partir del CSV de eBird.

Como se usa (desde la raiz del repo, donde esta index.html):
    1. En eBird: My eBird > Download My Data (llega por mail).
    2. python sync/sync_ebird.py MyEBirdData.csv
    3. Revisar el resumen que imprime, completar lo que falte y subir los cambios.

Catalogo: index.html tiene las aves de Argentina (ids 1-416 = album de Cordoba; 417+ = resto del pais).
Cada especie vista guarda en que provincias se registro ("prov", codigo ISO sin 'AR-': X = Cordoba).
Los domesticos (Domestic type) no cuentan.

Criterio "reflejo de eBird":
  - Cada especie aparece con la fecha y el lugar de su PRIMER registro en eBird.
  - Cada localidad de eBird es un lugar del mapa (a menos que en sync/lugares.json
    dos IDs compartan el mismo 'nombre': ahi se fusionan).
  - Cada lugar lista TODAS las especies vistas ahi, no solo las que se vieron primero ahi.

registros.json: por especie y por fecha, en que lugares se registro (sin el detalle de cada
checklist). Lo usa la galeria para ponerle el lugar a cada foto segun la fecha del nombre del archivo.

Lo que NO viene de eBird y se conserva del avistamientos.json anterior: 'foto' y 'notas'.
Una foto nueva se detecta sola si existe fotos/<nombre_cientifico>.jpg.
"""
import csv, json, os, re, sys
from collections import defaultdict, Counter
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
HTML = os.path.join(RAIZ, "assets", "datos.js")   # AVES y FICHAS viven aca
SALIDA = os.path.join(RAIZ, "avistamientos.json")
SALIDA_REG = os.path.join(RAIZ, "registros.json")
CFG_LUGARES = os.path.join(AQUI, "lugares.json")


def leer_aves(html):
    m = re.search(r"const AVES = \[\n(.*?)\n\];", html, re.S)
    aves = re.findall(r'\{id:(\d+), nombre:"([^"]+)", comun:"([^"]*)"', m.group(1))
    return {n: (int(i), c) for i, n, c in aves}


def leer_fichas(html):
    m = re.search(r"const FICHAS = \{\n(.*?)\n\};", html, re.S)
    return set(re.findall(r"^\s*'([^']+)':\s*\{estado", m.group(1), re.M))


def normalizar(nombre):
    """'Caracara plancus plancus' -> 'Caracara plancus'; '(Domestic type)' se descarta;
    los 'A/B' y los 'sp.' no son una especie concreta -> None."""
    if "(domestic" in nombre.lower():
        return None
    n = re.sub(r"\s*\(.*?\)", "", nombre).strip()
    if "/" in n or " sp." in n or " x " in n:
        return None
    partes = n.split()
    return " ".join(partes[:2]) if len(partes) >= 2 else None


def minutos(h):
    try:
        t = datetime.strptime((h or "").strip(), "%I:%M %p")
        return t.hour * 60 + t.minute
    except ValueError:
        return 0


def main(ruta_csv):
    html = open(HTML, encoding="utf-8").read()
    aves = leer_aves(html)
    fichas = leer_fichas(html)
    cfg = {k: v for k, v in json.load(open(CFG_LUGARES, encoding="utf-8")).items() if k.startswith("L")}
    previo = {}
    if os.path.exists(SALIDA):
        previo = json.load(open(SALIDA, encoding="utf-8")).get("avistamientos", {})

    filas = list(csv.DictReader(open(ruta_csv, encoding="utf-8-sig")))
    omitidos = Counter()
    primero = {}                      # id especie -> (fecha, minutos, loc_id)
    por_lugar = defaultdict(set)      # loc_id -> {id especie}
    por_dia = defaultdict(lambda: defaultdict(set))   # id especie -> fecha -> {loc_id}
    coords = {}                       # loc_id -> (lat, lon, nombre eBird)
    prov_de_loc = {}                  # loc_id -> codigo de provincia ('X')
    prov_de_sp = defaultdict(set)     # id especie -> {codigos de provincia}

    for r in filas:
        sci = normalizar(r["Scientific Name"])
        if sci is None or sci not in aves:
            omitidos[r["Scientific Name"]] += 1
            continue
        sid = aves[sci][0]
        lid = r["Location ID"]
        coords.setdefault(lid, (float(r["Latitude"]), float(r["Longitude"]), r["Location"]))
        cod = (r.get("State/Province") or "").replace("AR-", "") or "?"
        prov_de_loc[lid] = cod
        prov_de_sp[sid].add(cod)
        por_lugar[lid].add(sid)
        por_dia[sid][r["Date"]].add(lid)
        clave = (r["Date"], minutos(r["Time"]))
        if sid not in primero or clave < primero[sid][:2]:
            primero[sid] = (clave[0], clave[1], lid)

    # --- lugares (fusionando IDs que compartan nombre) ---
    sin_config = []
    grupos = {}                       # nombre -> {lat, lon, ids:set, loc_ids:[]}
    for lid, (lat, lon, nom_ebird) in coords.items():
        c = cfg.get(lid)
        if c is None:
            sin_config.append((lid, nom_ebird))
            c = {}
        nombre = c.get("nombre", nom_ebird)
        g = grupos.setdefault(nombre, {"lat": c.get("lat", lat), "lon": c.get("lon", lon), "ids": set(), "loc_ids": []})
        g["ids"] |= por_lugar[lid]
        g["loc_ids"].append(lid)
    orden = sorted(grupos.items(), key=lambda kv: (-len(kv[1]["ids"]), kv[0]))
    lugares = []
    nombre_de_loc = {}
    for i, (nombre, g) in enumerate(orden):
        lugares.append({"id": i, "nombre": nombre, "lat": round(g["lat"], 5), "lon": round(g["lon"], 5),
                        "prov": prov_de_loc[g["loc_ids"][0]], "count": len(g["ids"]), "ids": sorted(g["ids"])})
        for lid in g["loc_ids"]:
            nombre_de_loc[lid] = nombre

    # --- avistamientos ---
    id2sci = {v[0]: k for k, v in aves.items()}
    avist, sin_foto, nuevas = {}, [], []
    for sid in sorted(primero):
        fecha, mins, lid = primero[sid]
        conv = "fotos/" + id2sci[sid].lower().replace(" ", "_") + ".jpg"
        p = previo.get(str(sid), {})
        foto = p.get("foto")
        if os.path.exists(os.path.join(RAIZ, conv)):
            foto = conv
        avist[str(sid)] = {"fecha": fecha, "hora": f"{mins // 60:02d}:{mins % 60:02d}", "lugar": nombre_de_loc[lid], "prov": sorted(prov_de_sp[sid]), "foto": foto, "notas": p.get("notas", "")}
        if not foto:
            sin_foto.append(id2sci[sid])
        if str(sid) not in previo:
            nuevas.append(id2sci[sid])

    salida = {"generado": datetime.now().strftime("%Y-%m-%d"), "fuente": os.path.basename(ruta_csv),
              "avistamientos": avist, "lugares": lugares}
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)

    # --- registros por especie y fecha (los lugares se guardan como indices a una tabla de nombres) ---
    tabla = [l["nombre"] for l in lugares]
    indice = {n: i for i, n in enumerate(tabla)}
    reg = {str(sid): {fecha: sorted({indice[nombre_de_loc[lid]] for lid in lids}) for fecha, lids in sorted(dias.items())}
           for sid, dias in sorted(por_dia.items())}
    with open(SALIDA_REG, "w", encoding="utf-8") as f:
        json.dump({"generado": salida["generado"], "lugares": tabla, "r": reg}, f, ensure_ascii=False, separators=(",", ":"))


    # --- resumen ---
    print(f"OK: {len(avist)} especies, {len(lugares)} lugares -> {os.path.basename(SALIDA)}")
    print(f"    {sum(len(d) for d in reg.values())} pares especie+fecha -> {os.path.basename(SALIDA_REG)}")
    if nuevas:
        print(f"\nEspecies nuevas desde la ultima corrida ({len(nuevas)}):")
        for s in nuevas:
            print(f"  - {s} ({aves[s][1]}){'' if s in fichas else '   << FALTA FICHA'}")
    faltan = sorted(s for s in id2sci.values() if s in {id2sci[int(k)] for k in avist} and s not in fichas)
    if faltan and not nuevas:
        print(f"\nEspecies sin ficha: {faltan}")
    if sin_foto:
        print(f"\nSin foto todavia ({len(sin_foto)}): se muestran con silueta hasta que subas fotos/<nombre>.jpg")
    if sin_config:
        print("\nLugares nuevos sin nombre en sync/lugares.json (se usaron los de eBird, revisalos):")
        for lid, n in sin_config:
            print(f"  - {lid}: {n}")
    if omitidos:
        print("\nRegistros que no se pudieron asignar a una especie de la web (se omiten):")
        for n, c in omitidos.most_common():
            print(f"  - {n}: {c}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
