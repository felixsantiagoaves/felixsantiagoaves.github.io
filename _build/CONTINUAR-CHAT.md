# Prompt para retomar el trabajo en un chat nuevo

Pegar esto al abrir un chat desde la app de escritorio, con la carpeta `WEB` conectada:

---
Hola. Seguimos con mi web felixsantiago.com.ar (repo público `felixsantiagoaves/felixsantiagoaves.github.io`; clonalo con add_repo).
Antes de hacer nada leé estos archivos del repo, ahí está todo lo decidido:
- `_build/LEEME-CLAUDE.md` (cómo se construye el sitio)
- `_juego/LEEME-JUEGO.md` (juego "Mi año pajarero", ranking en Cloudflare, pendientes)
- `_calendario/LEEME-CALENDARIO.md` (calendario 2027)

Tarea de hoy: armar el calendario de escritorio 2027 con las fotos que dejé en `WEB/claude-procesamiento/seleccion calendario/` (de mi carpeta conectada). Decisiones: opción B alternando foto izquierda/derecha cada mes, portada = cuervillo de cañada, A4 vertical en 3 tiras de 21×9,9 cm. Mostrame primero enero + portada para aprobar y después hacés el resto.

Reglas mías: hablame en español, gastá pocos tokens, no agregues cosas que no pedí, no uses agentes salvo que te lo pida, y todo lo que decidamos tiene que quedar escrito en archivos del repo (no solo en memoria ni en el chat). Corré siempre `python3 _build/build.py` y `python3 -I _fichas/gen_fichas.py . _fichas` si tocás `assets/`.
---
