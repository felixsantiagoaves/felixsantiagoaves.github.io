# Mapa de componentes y reglas de adaptación (leer ANTES de tocar el diseño de una página)

Idea de Felix (16/11/2026): cada página es un **contenedor** (la pantalla) con **objetos**; cada objeto tiene **subobjetos**.
La flexibilidad y la coherencia se evalúan en los DOS niveles. Si se toca un subobjeto, se revisan TODAS sus variantes (lista abajo).

## Reglas generales
1. Pantalla fija en PC = contenedor de alto fijo (`--fit-h`). NO se usa `zoom` para encajar (queda todo amontonado).
2. Cada objeto reparte el espacio con grid/flex; un subobjeto "elástico" absorbe el sobrante (foto, panel de paisaje), el resto mantiene su tamaño natural o se oculta por altura (`max-height`).
3. Un sticker/figurita tiene **proporción propia fija**: su ancho sale del alto disponible (o al revés) y NUNCA se deforma. Lo que cambia con la pantalla es **cuántos** se ven (carrusel), no su forma.
4. Dentro de un panel con varias figuritas se usa una unidad común (`--u`, container query units) para que todas escalen juntas.
5. Todo subobjeto tiene variantes (con foto / mascota dibujada / sin dato / clon del carrusel). Al cambiar uno, probar las variantes. Mascotas: `.rec-masc-c img.rec-masc` (ancho 175 %, centrada, `--esc`) depende de la proporción del cuadro: por eso el cuadro de foto tiene `aspect-ratio:100/118`.
6. Probar siempre a 1215×613, 1440×800 y 1920×1000 y ver capturas. Después de cambiar assets: `python3 _build/build.py` (regenera `?v=`; si no, el navegador usa archivos viejos).

## Sobre mí (`#page-sobre-mi`, clases `fgh-*`) — HECHO con este principio
Objeto 1 · **Tarjeta personal** (`.fgh-card`): foto/slider `.fgh-ph` (elástica, min 150 px) · nombre/etiquetas `.fgh-info` · video YouTube (solo ≥980 px de alto) · "Para jugar" `.ult-juego` (solo ≥860 px) · botones Explorar/Compartir.
Objeto 2 · **Paisaje con contadores** (`.fgh-hoy > .fgh-stk`, container query): círculo Córdoba, círculo Argentina (`.stk-circ`), "Especies vistas" (`.stk-sq`), ticket "Faltan" (`.stk-tick`), estrella "Última" (`.stk-burst`), carancho/mascota (`.fgh-dc`). Todo en `calc(N*var(--u))`. El paisaje es `cover` (se recorta, no se deforma).
Objeto 3 · **Carrusel "Últimas especies"** (`.recientes > #rec-track`): figurita `.rec-item` = foto o mascota `.rec-circulo` (aspect 100/118) + número `.rec-num` + nombre `.rec-nom` (2 líneas) + "Ver todas" `.rec-mas`. Ancho de figurita = `(--rh − 32px) × .64`; auto-scroll de `recAuto()` (clones `.rec-clon`), se frena con el mouse.
Variantes de figurita: foto real · mascota dibujada (`rec-masc-c`) · silueta de familia (`rec-sin-foto`) · "Ver todas".

## Pendiente de migrar al mismo principio
Estadísticas (`#page-datos`: tarjetas KPI, gráfico acumulado, gráfico mensual, pestañas), Contacto (`#page-redes`), Galería (`#foto-grid`). Antes de hacerlo, escribir aquí su árbol objeto→subobjeto y qué proporción mantiene cada uno.
