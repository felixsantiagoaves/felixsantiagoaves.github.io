# Mi año pajarero — documentación del juego

Juego web en `felixsantiago.com.ar/juego/` (página de entrada en `/juegos/`). Todo corre en el navegador;
lo único con servidor es el ranking (Cloudflare Worker + D1). Última actualización: 11/11/2026.

## 1. Cómo se arma
Código fuente en `_juego/`. NUNCA editar `juego/index.html` a mano: se genera con

    python3 _juego/build.py        # concatena todo y escribe juego/index.html (~360 KB)

Orden: `head.html` (HTML + CSS) → `assets3.js` (fondos IMG, siluetas SILD, FSIL familia→silueta) → `const D=data2.json`
(421 especies de Córdoba) → `compartir.js` → `sonido.js` → `game.js`.

| Archivo | Qué tiene |
|---|---|
| `head.html` | CSS de todo el juego, barra superior (← Félix Santiago Aves / Juegos), clima, animaciones |
| `game.js` | Lógica y pantallas: perfiles, meses, lugares, imprevistos, suerte, decisiones, final, ranking, libreta |
| `compartir.js` | Imagen para compartir en canvas (Historia 1080x1920, Feed 4:5, Cuadrado) + Web Share / descarga |
| `sonido.js` | Música y ambiente generados con WebAudio, cantos reales desde xeno-canto |
| `data2.json` | Especies: [id, común, científico, familiaIdx, frecuencia %, pesos por zona, estacionalidad] |
| `assets3.js` | Fondos de lugares (SVG base64), siluetas `SILD`, mapa familia→silueta `FSIL` |
| `logo.svg` | Logo "Mi año pajarero" (también inline en game.js `LOGO` y en `_build/fragmentos/juegos.html` y `sobre-mi.html`) |
| `worker/` | Código del ranking (ver sección 6) |
| `herramientas/` | Scripts de simulación y de generación de siluetas (sección 8) |

Datos de eBird: frecuencias de 85.637 listas completas de Córdoba. Zonas, hotspots y probabilidades salen de ahí.

## 2. Flujo del juego
`inicio()` portada (paisajes que pasan solos + hilera de figuritas que gira) → `perfil()` (nombre/alias OBLIGATORIO, mín. 2
letras + 3 perfiles) → `empezar(modo)` → `nuevo(seed,modo)` → `pintarMes()` → `elegirZona(i)` (va directo, SIN pantalla de
viaje; se sacó a pedido de Felix) → `viaje2()` tira en orden: imprevisto (`G.P.mi`) → suerte (`G.P.su`) → si no, decisión
(`evento()`/`expertoEv()`); imprevisto, suerte y decisión son mutuamente excluyentes en una salida → `resolver(o)` →
`sig()` → `final()`.

Probabilidad de ver una especie: `prob = .8*(1-exp(-p/.8))`, `p = f/100 * q[zona] * K * ZM[zona]`, con estacionalidad.
`MK(lugar)` = riqueza del lugar. Encuentro: `1-(1-min(.8,prob*MK))^e`. Las opciones modifican con `G.mod`, `G.permM`, `ari`
(aves con f<2), `fam:[famIdx,mult]`, `rara:p`.

## 3. Perfiles (`PERF` en game.js) y calibración
| Perfil | Salidas | Notas | Títulos (umbrales) |
|---|---|---|---|
| Principiante (guiado) | 6, una cada 2 meses | solo aves comunes (f>=1), más nafta/energía, pistas | 45/65/85/105/125 |
| Aficionado (normal) | 12 | comunes y raras | 60/90/125/155/180 |
| Experto | 12 | 4-6 opciones por decisión, sin etiquetas, más imprevistos y suerte, techo alto | 70/100/130/165/200 |

Calibración (50-60 simulaciones): guiado azar ~100 / bien jugado ~120 (máx ~140); normal azar ~150 / bien ~165 (máx 190);
experto azar ~125 (80-176) / óptimo ~169 (125-224). Títulos: Pajarero de balcón, Salidor de domingo, Libreta gastada,
Ojo entrenado, Cazador de lifers, Leyenda cordobesa. PENDIENTE: que Experto supere 200 jugando bien de forma consistente.

## 4. Sonido (`sonido.js`)
Música ambiente + clima (lluvia, tormenta, grillos, búho, fuego) generados por código, sin archivos de audio. Cantos reales:
al revelar una especie rara se baja de xeno-canto (`https://xeno-canto.org/{xc}/download`) usando los metadatos `CANTOS` de
`/assets/cantos.js` de la web; se muestra el crédito. El audio arranca recién tras el primer toque (política de los
navegadores). El botón "Sonido" apaga todo. Nunca se pudo escuchar en el sandbox de Claude: probar en un dispositivo real.

## 5. Final, compartir, historial y libreta
- Final: botón principal "Compartir mi año" (o "Descargar imagen" si el navegador no puede compartir archivos), imagen debajo,
  formatos Historia/Feed/Cuadrado como píldoras chicas, y el bloque del ranking.
- "Compartir el juego" (link) en la portada del juego y botón "Compartir" en `/juegos/` (función `compartirJuego()` en `assets/site.js`).
- Historial local: `localStorage` clave `ap_hist` (últimas 60 partidas, por dispositivo). Pantalla "Mis partidas".
- Libreta: tocar "Especies ▾" en la barra del juego abre las especies vistas agrupadas por familia ("5 de 29") y los grupos sin ver.
- Nombre guardado en `localStorage` clave `pajarero_nombre`.

## 6. Ranking compartido (Cloudflare)
- Worker `ranking-pajarero` (cuenta Cloudflare de Felix, la misma del dominio), dirección `https://api.felixsantiago.com.ar`
  (custom domain del Worker sobre la zona felixsantiago.com.ar). También responde en
  `https://ranking-pajarero.santiagoallendes.workers.dev`. Base D1 `ranking-pajarero`, binding `DB`.
- Código: `_juego/worker/worker.js` (se pega en Edit code del Worker y Deploy), tabla en `_juego/worker/schema.sql`.
- Endpoints: `GET /top?perfil=guiado|normal|experto` (top 20, mejor puntaje por nombre) y `POST /score` con
  `{nombre, perfil, especies}` → `{ok, nombre, puesto, top}`.
- Sin autenticación. Defensas: solo acepta Origin de felixsantiago.com.ar / www / felixsantiagoaves.github.io; tope por perfil
  (150 / 205 / 250 especies, un poco sobre el máximo simulado); limpia el nombre y reemplaza malas palabras; máximo 12 envíos por
  hora por IP (guardada hasheada). NO verifica la partida (se descartó la verificación por semilla por ahora: haría falta
  separar la lógica del DOM y correrla en el Worker; ver sección 9).
- En el juego: constante `API` en `game.js`. Si queda vacía (`''`) se apagan el envío y el botón Ranking.
- Si se cambia el código del Worker hay que volver a pegarlo y hacer Deploy en Cloudflare. Si se cambian las reglas del juego
  que modifican el techo de especies, actualizar `MAX` en el Worker.
- Mantenimiento en la consola de D1 (Cloudflare → D1 → ranking-pajarero → Console):
  `SELECT nombre, perfil, especies FROM scores ORDER BY especies DESC;`
  `DELETE FROM scores WHERE nombre = 'xxx';`   `DELETE FROM scores;` (vacía todo)
- Costos: plan gratis. Workers 100.000 pedidos/día; D1 5 M lecturas y 100.000 escrituras por día, 5 GB. Al pasarse devuelve
  error hasta medianoche UTC (no cobra). Se eligió D1 y no KV porque KV gratis solo permite ~1.000 escrituras/día.

## 7. Siluetas
Hay ~34 siluetas nuevas (además de las 9 originales) para cubrir los grupos de aves del álbum y del juego. Se usan en la web
(`SILUETAS` y `FAM_SILUETA` en `assets/site.js`) y en el juego (`SILD`/`FSIL` en `assets3.js`): son las mismas, hay que
actualizar ambos lugares. Las nuevas son SVG blanco, viewBox cuadrado normalizado, con detalles recortados por máscara (ojo, línea
del ala). Se generan con `_juego/herramientas/siluetas/` (gen.py → gen2.py → gen3.py → norm.js, ver sección 8). Las más flojas
según el propio criterio: tucán (pico algo despegado), ratona (cola), cuclillo y urraca (muy diagonales), cormorán.

## 8. Herramientas (`_juego/herramientas/`)
- `sim5.js`: simula partidas con Playwright sobre `juego/index.html` (jugador al azar vs. "oráculo" por valor esperado) para calibrar
  perfiles. Requiere `npm i playwright` o el Playwright ya instalado; las rutas dentro del script son absolutas, ajustarlas.
- `t11.js <0|1|2>`: recorre una partida completa por la interfaz del perfil indicado y avisa errores de página.
- `siluetas/`: generadores. Flujo: `python3 gen.py` (siluetas base) → `python3 gen2.py` (en vuelo/agua) → `python3 gen3.py`
  (percha) → unir los JSON (`sil.json`, `sil2.json`, `sil3.json`) en `sil.json` → `node norm.js` (normaliza el encuadre y
  genera `sil_n.json` y una hoja de prueba) → pegar en `assets/site.js` y `_juego/assets3.js` codificadas como data URI.

## 9. Pendientes e ideas
- Experto: lograr que superar 200 sea posible y consistente con buenas decisiones.
- Verificación de partidas por semilla en el Worker (opcional, si aparecen trampas).
- Posible 2º juego (la página `/juegos/` ya dice "Más juegos, pronto").
- Mejorar las siluetas más flojas (sección 7).
- Probar sonido y cantos en celular real.
- Código del juego: el repo es público, por lo que `_juego/` también. Felix preguntó si se puede mantener privado; opciones planteadas: A) repo privado aparte con el código fuente y publicar solo `juego/index.html`, B) dejarlo público, C) ofuscar. Sin decidir, no se hizo nada.
- Borrar la fila de prueba "Anónimo" de la base D1 del ranking (Cloudflare → D1 → Console: `DELETE FROM scores WHERE nombre='Anónimo';`).
