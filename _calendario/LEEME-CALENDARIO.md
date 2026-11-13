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
