# Calendario de escritorio 2027 — decisiones y estado

Estado (13/11/2026): estructura decidida, falta armar los 12 meses con las fotos reales.

## Decisiones de Felix
- Calendario de escritorio con forma de triángulo (base tipo atril), hojas que se pasan hacia atrás. Plazo: listo hacia diciembre.
- Hojas: A4 vertical cortada en **3 tiras de 21 × 9,9 cm** (3 páginas por hoja). 13 páginas (tapa + 12 meses) = 5 hojas A4 (sobran 2 lugares).
- Diseño elegido: **opción B** (`opciones-3-por-hoja.png`): foto 3:2 grande a sangre (137 × 99 mm) + panel del mes (60 mm).
  Se **intercala la orientación mes a mes**: foto a la izquierda en unos meses y a la derecha en otros (alternar B y su espejo).
- Portada: la foto del **cuervillo de cañada**.
- Semana empieza en lunes; domingos en marrón; feriados con círculo verde oliva. Pie: nombre del ave (+ @felix_santiago_aves).
- Pendiente de definir: qué más lleva cada mes (luna, "aves que llegan/se van"), método de impresión (casera o imprenta), molde de la base en A4.

## Archivos
- `maqueta-enero.html/.png/.pdf`: primera maqueta (A5 apaisado, foto 4:5), descartada por el formato de 3 por hoja.
- `opciones-3-por-hoja.html/.png`: las 4 opciones (A foto cuadrada, B foto grande, C espejo, D panorámica). Se eligió B.
- Las fotos para el calendario están en la PC de Felix: `WEB/claude-procesamiento/seleccion calendario/` (no están en el repo).

## Cómo se trabaja (acordado)
- Se arma en HTML con medidas en mm y se renderiza con Playwright a PNG/PDF (como las maquetas de esta carpeta).
- Entregables previstos: (1) PDF de las 5 hojas A4 con marcas de corte, (2) PDF aparte con el molde/base A4 del atril, (3) PNG de vista previa de cada mes.
- Las fotos hay que leerlas de la carpeta de la PC de Felix (chat de la app de escritorio con la carpeta `WEB` conectada) o que las adjunte al chat. No están en el repo (pesan mucho).
- Orden de meses: enero con foto a un lado, febrero al otro, y así alternando. La portada es el cuervillo de cañada.
- Preguntas aún abiertas (hacer pocas y solo si hacen falta): qué extras lleva cada mes (feriados sí; luna / "aves que llegan" sin decidir), impresión casera (margen blanco) o imprenta (sangrado), y encuadernación/base.

## Avance (13/11/2026)
- Llegaron las 14 fotos por el chat (la conexión con la PC seguía caída). Nombres: churrinche, maca cara blanca, varillero congo, cuervillo de cañada (portada), tachurí siete colores, pico de plata, cigüeña americana, jote cabeza negra, águila mora, gallineta pico pintado, tacuarita azul, picaflor verde, chingolo, chimango. Sobra una (13 usables para portada + 12 meses → falta decidir cuál queda afuera).
- `gen_calendario.py <carpeta_fotos> <salida> [meses]` genera cada tira (210×99 mm) en PNG. Los meses se configuran en el dict `MESES` (archivo, nombre, lado de la foto L/R, feriados). Las fotos se llaman como en la lista (ej. `picaflor_verde.jpg`).

## Versión completa (13/11/2026)
- 12 meses + portada generados con `gen_calendario.py` (las imágenes NO se guardan en el repo, por pedido de Felix: se regeneran cuando hacen falta; `_calendario/vistas/` está en .gitignore). Cada mes lleva: nombre común, científico, lugar y fecha de la foto (de `registros.json`), logo, felixsantiago.com.ar y @felix_santiago_aves. Feriados nacionales 2027 en círculo verde (fuente: calcularsueldo.com.ar; Jueves Santo 25/3 es no laborable, no marcado; días turísticos 2027 no encontrados, revisar si se decretaron; 20/11 podría moverse).
- Orden: Ene chingolo, Feb chimango, Mar picaflor común, Abr gallineta pico pintado, May tachurí sietecolores, Jun tacuarita azul, Jul águila mora, Ago varillero congo, Sep churrinche, Oct jote cabeza negra, Nov pico de plata, Dic macá cara blanca. Alterna foto izquierda/derecha. Queda afuera la cigüeña americana.
- Pendiente: lugares de chingolo (02/01/2026), picaflor (16/03/2026) y tacuarita azul (12/06/2026, hay 2 lugares ese día) — figuran "POR CONFIRMAR" en `AVES` del script. Después: hojas A4 con marcas de corte, molde de la base, método de impresión.

## Dónde están los archivos pesados
- En la PC de Felix: `WEB/claude-procesamiento/calendario-2027/` (portada, 12 meses en PNG, montaje, copia del script). Las fotos originales: `WEB/claude-procesamiento/seleccion calendario/`. El repo es público: nada pesado ni privado va ahí, solo scripts y textos.
- La conexión con la PC volvió a funcionar el 13/11 a las 12:19; con ella se leen y se escriben archivos en esas carpetas.

## Diseño v3 (13/11/2026)
- Nombres de aves con cada palabra en mayúscula (salvo de/del/la/y). Datos del ave sobre la foto. Tipografías: Cormorant Garamond (nombres, meses; npm `@fontsource/cormorant-garamond`, los woff2 viven en la carpeta `fuentes/` de la PC, no en el repo; el script las lee de ahí o de la variable CAL_FUENTES) e Inter (números y rótulos).
- Portada: panel verde oscuro con el logo, "Félix Santiago · Aves", 2027 grande y la foto del cuervillo de cañada ampliada a la derecha.

## Decisiones 13/11 (tarde)
- Lugares confirmados por Felix: picaflor y chingolo en casa, Río Cuarto; tacuarita azul en Los Hornillos. En el calendario va solo nombre común, científico y lugar (sin fecha de la foto).
- Portada (boceto de Felix en Canva): ave grande a la derecha, "Calendario de escritorio" + 2027 grande a la izquierda, logo + Félix Santiago · Aves + web abajo a la izquierda, nombre/científico/lugar del ave abajo a la derecha.
- Encuadre de las fotos: queda pendiente. Idea de Felix: un HTML donde él reencuadre cada foto y me pase las posiciones.

## Encuadre de fotos (13/11)
- `encuadre_plantilla.html` (en el repo, sin fotos) → `encuadre.html` se genera con las fotos embebidas y vive en la PC de Felix (`WEB/claude-procesamiento/calendario-2027/`). Se abre con doble clic en el navegador; Felix arrastra y hace zoom en cada marco (portada + 12 meses) y toca "Copiar encuadres", después pega el texto en el chat.
- Ese texto (JSON `{"portada":{foto,z,cx,cy},"01":{...}}`) se guarda como `encuadres.json` junto a `gen_calendario.py` (o en la variable CAL_ENC) y el script lo aplica solo. z = zoom sobre "cubrir el marco", cx/cy = punto de la foto que queda al centro del marco. Los defaults reproducen el diseño previo.
