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
Objeto 3 · **Carrusel "Últimas especies"** (`.recientes > #rec-track`): figurita `.rec-item` = foto o mascota `.rec-circulo` (aspect 100/118) + número `.rec-num` + nombre `.rec-nom` (2 líneas) + "Ver todas" `.rec-mas`. Ancho de figurita = `(--rec-h − 32px) × .64`; auto-scroll de `recAuto()` (clones `.rec-clon`), se frena con el mouse.
Variantes de figurita: foto real · mascota dibujada (`rec-masc-c`) · silueta de familia (`rec-sin-foto`) · "Ver todas".

## Estadísticas (`#page-datos`) — HECHO (nov 2026)
Contenedor: grid de 2 filas (`--fit-h`): [título + pestañas en una fila] · pane activo.
Resumen = fila 1: tarjeta "Camino a las N especies" (chips en una línea, sin wrap) + frase del filtro · fila 2: 6 KPI (foto de fondo + número + rótulo; alto proporcional a vh) · fila 3 (elástica): gráfico acumulado + gráfico mensual.
Los gráficos NO se escalan: `pintarNumeros()` mide su tarjeta (`CH_DIM`) y `chartAcumulado/chartMensual` dibujan con viewBox = píxeles reales (textos siempre del mismo tamaño). Se redibujan en cada `fitPantalla`.
Lugares y grupos: dos tarjetas; las barras (`.hb`) se reparten el alto (grid `1fr`). Línea de tiempo / Territorio / Las que me faltan: listas largas → scroll interno del panel (única excepción).

## Contacto (`#page-redes`) — HECHO
Objeto 1: tarjeta "Trabajemos juntos" (foto elástica `::before` · título · texto · 2 botones · "copiar mail"). Objeto 2: "Mis redes" = 5 figuritas `.red-card` de proporción fija 1:1,12 (ancho = mín(columna, fila)), 3 arriba + 2 centradas; íconos escalan con la figurita. Objeto 3: copyright (letra chica).

## Galería (`#page-galeria`) — HECHO
Cada foto = figurita con foto 4:5 + pie (66 px). `fitGaleria()`: el alto disponible fija filas y tamaño; el ancho solo cambia CUÁNTAS entran por fila (`--gal-cols`); paginación ‹ n/total ›.

## Álbum (`#page-album`) — vista libro HECHA, vista lista scrollea normal
Objeto 1: barra (Córdoba/Argentina + "Ver como lista") compacta. Objeto 2: índice de familias (scroll propio, alto = contenedor). Objeto 3: el libro (`.libro-book` 1400×740, proporción fija): `escala()` en libro.js lo agranda a lo que entra en el hueco (ancho y alto del contenedor, tope 2×); cada hoja = 12 figuritas en grilla 4×3. Barra de hoja/ayuda debajo (ayuda se oculta si hay <780 px de alto).
En Estadísticas: tocar un lugar/grupo en su pestaña pasa solo al Resumen (ahí se ve el filtro); la barra de filtros vive en su celda y no flota sobre los números.

## Sin migrar (decisión de Felix: pueden scrollear o no aplica)
Especies (tipo blog, scrollea), Mapa, Juegos, Calendario (privado).

## Trampas conocidas (variables CSS con nombre repetido)
- `--rh` = alto del cuadro de foto de la figurita (lo usa la mascota para escalar). La tira usa `--rec-h`. NO reutilizar `--rh` para otra cosa: en PC se redefine en `.rec-circulo`.
- Antes de crear una variable nueva: `grep -n "\-\-nombre" assets/*.css`.
