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

## Estadísticas (`#page-datos`) — REHECHO 16/11 (4 pestañas: Resumen · Línea de tiempo · Territorio · Las que me faltan)
Contenedor: grid de 2 filas (`--fit-h`): [título + pestañas en una fila] · pane activo. En PC fija ninguna pestaña scrollea.
- **Resumen = un tablero** (antes eran 2 pestañas: "Lugares y grupos" se unió acá). Fila fina de filtros/hint arriba + 3 columnas (`.dat-col-a/b/c`): A = "Camino a N especies" + 6 contadores KPI (2×3, la foto de fondo se estira); B = gráfico acumulado + gráfico mensual (dibujados al tamaño real, `CH_DIM`); C = lugares con más especies + grupos más vistos (barras que se reparten el alto). Tocar mes/lugar/grupo filtra todo. En celular `.dat-col`/`.dat-kpis` son `display:contents` (los hijos van a la grilla de siempre).
- **Línea de tiempo** = línea REAL horizontal (`.tl` en `row-reverse`: lo nuevo a la derecha, se arrastra hacia atrás). Un tramo por mes: título + punto sobre el eje + miniaturas de las especies nuevas; `fitTimeline()` elige columnas y tamaño por mes para que entren todas. Nombre/fecha en el tooltip (`title`).
- **Territorio**: mapa y barras llenan la tarjeta (mapa = alto completo; barras con alto máximo 54 px).
- **Las que me faltan** = cajas de familia que llenan toda la pantalla (`fitFaltan()` elige columnas/filas con caja ~1,35:1). Color = `fc0..5` (mismo ciclo que el libro), relleno de abajo hacia arriba = % que ya tengo, ✓ si está completa. Tocar una caja abre un panel central con las especies (el `<details>` original) y un velo para cerrar.
Trampa: `datTab()` pone `style="display:block"` inline en el pane → para usar grid en un pane se selecciona `[style*="block"]` con `!important`.

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

## Con scroll controlado (páginas que sí scrollean)
Regla: la página puede scrollear, pero **máximo ~3 pantallas**. No se achican letras ni se deforman piezas: cambia CUÁNTAS entran por fila (las piezas conservan su proporción).
- **Especies** (`/aves/`): `ficha.js` (bloque final) elige columnas (`--lc`, de 3 a 14, mínimo 84 px por tarjeta) para que el largo total quepa en 3 pantallas; se recalcula al filtrar/redimensionar. Cabecera compacta, texto de la tarjeta escala con `cqw`. Clase `body.lista-fit` (solo PC). 126 especies: ~2,7 pantallas a 1440×800, ~3,3 a 1215×613.
- **Juegos**: pantalla fija (`page-juegos` en FIT_IDS → `fitSobreMi`); la tarjeta de cada juego centrada, logo = 26 % del alto.
- **Álbum en lista** (`#album-container`): `fitAlbumLista()` en site.js reparte las familias cerradas en 2–4 columnas (`--alc`); la que se abre ocupa todo el ancho (`grid-column:1/-1`). ~2,3–2,8 pantallas. Se llama desde `renderAlbum()` y `fitPantalla()`.
- Para otra página con scroll: misma idea, un `fit…()` que mide el presupuesto `3*innerHeight` y elige columnas.

## Rendimiento (regla)
- Fotos chicas (línea de tiempo, figuritas del álbum, carrusel, miniaturas de familia) usan la miniatura de 400 px `fotos/th/NOMBRE.jpg` vía `TH(url)` en site.js (con `onerror` que vuelve a la foto grande). Las fotos grandes (960 px, ~300 KB) solo en modal/galería/ficha.
- Al agregar fotos nuevas correr `python3 _build/miniaturas.py` (crea las que falten en `fotos/th/`), y después `build.py`.
- Antes: la línea de tiempo bajaba ~180 fotos grandes para mostrarlas de 60–100 px.

## Celular (mismo principio: ≈3 pantallas de scroll, se adapta al teléfono)
Celular = todo lo que no es `fit-pc` (ancho < 1000, alto < 560 o sin mouse; incluye teléfonos apaisados). Las piezas conservan proporción; cambia cuántas entran por fila.
- Especies: `ficha.js` elige columnas (2–14, mín. 76 px) → clase `lista-m` (cabecera compacta). 16–20 pantallas → ~5 (tope por tamaño legible de tarjeta).
- Álbum lista: `fitAlbumLista()` → 2 columnas (3 si ancho ≥ 700); familias cerradas muestran solo nombre + contador. 6–8 → ~2–3 pantallas.
- Galería: `#foto-grid` CSS columns 2 (3 a ≥700, 4 apaisado), miniaturas `TH()`. 5–6 → ~2.
- Sobre mí, Contacto, Juegos, Estadísticas ya andan en 1–3,6 pantallas en vertical; no se tocaron.
- Prueba: `mob2.js` (SE 375×667, 390×844, 430×932, 360×780, apaisado 844×390) mide pantallas de largo por página.
- Estadísticas en celular (`body.fit-datm`, `fitDatosM()`): Línea de tiempo = misma línea horizontal que en PC, ocupa el alto que queda bajo las pestañas (columnas de 130 px, se arrastra de lado); Las que me faltan = mismas cajas de color en 3 columnas (5 apaisado). Reusa los CSS de PC (`body:is(.fit-pc,.fit-datm) #dat-tl/#dat-falt`). Resumen y Territorio siguen en vertical.
- Libro (todas las pantallas): `.libro-idx-fijo` deja Córdoba/Argentina, "Familias" y Tapa fijos arriba del índice; solo scrollean las familias.
- Portadas del libro (`cara()` en libro.js, CSS `.lt-*` al final de figurita.css): TAPA = polaroid con paisaje (sierra para Córdoba, cerro para Argentina) + etiqueta "Álbum de aves" + anillo de progreso + las 3 últimas especies con foto; CONTRATAPA = polaroid del ocaso + logo + "Seguirá completándose".
- Banderita argentina: `<i class="ar"></i>` (CSS en figurita.css, dibujada con degradado, sin imagen) delante de todo "Argentina" de la interfaz: botones de región (álbum, libro, faltantes, territorio, mapa), círculo "En Argentina" y ubicación en Sobre mí, subtítulo del álbum y portada. Al sumar un nuevo "Argentina" visible, ponerla.
- **Mapa** (PC): `page-mapa` en FIT_IDS → `fitSobreMi`; barra de título/botones/leyenda compacta arriba y el mapa se lleva todo el resto (ancho y alto), `mapa.invalidateSize()` al reajustar. Celular sigue con su altura propia (`calc(100svh …)`). Nota: en el entorno de pruebas no cargan los mosaicos del mapa, así que solo se verificó el marco.
- Libro en celular apaisado (`.libro-full`): sin contador "Hojas X y Y" ni barra inferior; "Cerrar" arriba a la derecha; índice de 120 px → el libro usa todo el alto (`escala()` en libro.js: ancho − 216, alto − 12).
- **Libro en celular VERTICAL** (`renderV()` en libro.js, CSS `.libro-vv`): doble página APILADA como un almanaque de pared (lomo horizontal): hoja de arriba = página par, de abajo = impar; al pasar, la hoja de abajo se levanta (giro `rotateX`). Mismo motor, paginación y 4×3 figuritas por página que el libro apaisado; se pasa deslizando el dedo hacia arriba/abajo o con ▲▼. Arriba, fijo: desplegable "Ir a una familia" + Córdoba/Argentina + ✕. Al girar el teléfono cambia solo al libro apaisado (`vModo`).
  - (Se probó un índice lateral de pestañitas con abreviaturas: no servía, se sacó. El libro vertical queda limitado por el ALTO de pantalla; con 4×3 figuritas por página el ancho sobrante no agranda las figuritas.)
- Celular: el LIBRO es la vista por defecto del Álbum (antes lista). El libro vertical deja visible la barra de abajo de la web (sin "Cerrar"; botón "☰ Lista" para cambiar de vista) y `.modal-ov` tiene z-index 10050 para que las fichas abran POR ENCIMA del libro (antes quedaban detrás y "no andaban"). Una elección guardada en localStorage (`albumVista`) tiene prioridad sobre el default.

## Álbum en celular: barra única (lista y libro), con el nav de arriba visible
Se mantiene el nav (logo) arriba; sin título de página. Una sola barra fija de 46px: [Córdoba|Argentina] [Libro/Lista] [Filtros ▾ (lista) / Ir a familia (libro)]. CSS al final de `assets/figurita.css` (`body:not(.fit-pc):has(#page-album.active)`); markup del libro en `renderV()` de `assets/libro.js`; texto del botón en `libroBtnTxt()` (site.js).
Textos de stickers del libro vertical agrandados (.libro-vv .fig-co/.fig-ci/.fig-num al final de figurita.css); overlay del libro empieza en top:54px (altura del nav).
Libro vertical en celular = UNA página por vez (ancho completo): en vModo armar() intercala páginas 'vacia' (P=[tapa,vacia,h1,vacia,h2…]), LM=L-1, --sh=-1, escala por ancho/alto de 1 página. Reemplaza la doble página apilada.
Libro vertical celular: 3 columnas × 4 filas por página (COLS=3, PH=1080 en vModo; --ph en CSS).
Libro vertical: sin giro de hoja; solo la hoja .cur es visible y la página nueva se desliza (@keyframes vslide, --vd según dirección).
Libro vertical (celular): página única que gira sobre su borde izquierdo hacia los costados (como pasar página); flechas ◀▶, swipe horizontal. Reemplaza el deslizado vertical.
Libro vertical: libro grueso abierto (referencia: foto de libro abierto): pliegue central con degradé en la página derecha (.front .lpag) y espejado en la izquierda (.back .lpag), canto de hojas apiladas a derecha y abajo + tapa verde (.libro-book::after). Hojas a left:4px, book width 716.
Libro vertical: libro apoyado a la derecha (stage justify-content:flex-end, padding-right 14px, transform-origin top right).
Libro vertical: sombra del pliegue como overlay (.lpag::after, multiply) sobre el contenido para que oscurezca también las fotos.
Libro vertical: pliegue tenue (≈.26 de opacidad máx.) para igualar la sutileza del libro de PC; el de PC no se toca.
Libro vertical: la página izquierda (reverso de la hoja pasada) muestra SOLO la 3.ª columna de una hoja anterior con miniaturas livianas (.lpag-izq/.lf-col); antes se duplicaba la hoja completa y se caía la pestaña en el celular. En vModo solo se mantienen 3 hojas con contenido (lim=1) y .back sin clicks.
Libro vertical: sin mix-blend-mode en la sombra del pliegue (causaba glitch al terminar el giro 3D); .leaf will-change:transform.
Libro vertical: pliegue ESTÁTICO (.libro-book::before simétrico, z alto) en vez de sombra por hoja (evita glitch al pasar); la página izquierda siempre muestra la col. 3 de la hoja inmediata anterior (cara(i-1)).
Libro: dorso de la tapa (interior verde, .lpag-dorso) a la izquierda de la 1.ª hoja, tanto en PC (P=[tapa,dorso,h1…]; numeración de hojas = índice-1) como en celular vertical (relleno izquierdo de la hoja 1).
Libro: final realista = última hoja a la izquierda + interior de la contratapa (.lpag-dorso) a la derecha, luego contratapa ('blanca' si la cantidad de hojas es impar); en celular vertical la última página es el dorso verde. Tapa: mini guía de uso (.lt-guia) sobre cómo está organizado el álbum.
Guía de uso: en PC va en el dorso de la tapa (.ld-guia, dorso con guia:1) y se oculta de la tapa; en celular vertical queda en la tapa (el dorso casi no se ve).
Guía en la tapa del libro vertical: .lt-guia2 (mismo contenido que .ld-guia de PC), visible solo en .libro-vv.
