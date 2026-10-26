# Estructura del sitio (desde octubre 2026: una página por sección)

Ya NO existe un único index.html con todo. Cada sección del menú es su propio HTML:

  /                 Sobre mí (portada)         fragmento: _build/fragmentos/sobre-mi.html
  /album/           Álbum                      _build/fragmentos/album.html
  /mapa/            Mapa                       _build/fragmentos/mapa.html
  /galeria/         Galería                    _build/fragmentos/galeria.html
  /estadisticas/    Estadísticas               _build/fragmentos/datos.html
  /contacto/        Contacto                   _build/fragmentos/redes.html
  /aves/            Índice de especies (168)   generado por _fichas/gen_fichas.py
  /aves/<especie>/  Ficha de cada especie      generado por _fichas/gen_fichas.py (+ _fichas/<slug>.json con el texto)

Archivos compartidos (los cargan todas las páginas, se cachean una sola vez):
  assets/site.css    todo el CSS
  assets/site.js     toda la lógica (álbum, mapa, galería, estadísticas, modal, lightbox...)
  assets/datos.js    AVES y FICHAS (lo lee sync/sync_ebird.py y _fichas/gen_fichas.py: NO cambiar su formato)

Cómo se editan:
  - CSS/JS/datos: editar el archivo de assets/ y correr:   python3 _build/build.py   (actualiza el número de versión ?v= en las páginas)
  - Contenido de una sección (HTML): editar _build/fragmentos/<seccion>.html y correr python3 _build/build.py
  - Menú, <head>, título y descripción de cada página: _build/build.py (lista PAGINAS y plantilla). No editar a mano los index.html generados.
  - Fichas de especie e índice /aves/: python3 -I _fichas/gen_fichas.py . _fichas   (desde la raíz del repo; también regenera sitemap.xml y aves/indice.json)
  - Siempre correr build.py Y gen_fichas.py después de tocar assets/ para que todas las páginas pidan la misma versión.

Navegación entre páginas (assets/site.js): showPage/irAlbum/irMapaLugar/irDatos/irAlbumFamilia/mapaAlbum llaman a aOtra(): si la sección no está
en la página actual, guardan la acción en sessionStorage ('pend') y navegan; la página de destino la ejecuta al iniciar.
Los enlaces viejos (/#album, /#mapa, /#galeria, /#datos, /#redes, /#ave-<slug>) se redirigen desde la portada.
Todas las rutas en JS son absolutas (/avistamientos.json, /fotos/..., /galeria/...): las páginas viven en subcarpetas.
Para probar en local hay que servir desde la raíz (python3 -m http.server).

Lo que sigue valiendo de abajo: donde dice "este HTML" o "la pestaña", leer "assets/datos.js" y "la página".

=======================================================================
  DOCUMENTACIÓN PARA CLAUDE — LEER ANTES DE MODIFICAR EL SITIO
=======================================================================

Web personal de avistamiento de aves en Córdoba, Argentina. Los avistamientos
y el mapa son un REFLEJO de la cuenta de eBird del usuario: no se cargan a
mano en este HTML, se generan con un script desde el CSV de eBird.

-----------------------------------------------------------------------
1. DÓNDE VIVE CADA COSA
-----------------------------------------------------------------------

A) const AVES = [ ... ]            (en assets/datos.js)
   Las 1.088 aves de Argentina (lista de eBird). Los ids 1–416 son el álbum de Córdoba; 417+ solo cuentan para Argentina. Forma:
     {id:N, nombre:"Nombre científico", comun:"Nombre común", familia:"...", familiaEsp:"...", tx:N}
   familiaEsp = grupo/familia como lo nombra eBird; tx = posición en el orden taxonómico de eBird; FAM_ORDEN = orden de las familias.

B) avistamientos.json              (archivo aparte, GENERADO, no editar a mano)
   Lo escribe sync/sync_ebird.py. Se carga con fetch() al abrir la web.
     "avistamientos": { "<id especie>": {fecha:"AAAA-MM-DD", hora:"HH:MM", lugar:"Nombre", foto:"fotos/x.jpg" | null, notas:""} }
     "lugares": [ {id, nombre, lat, lon, count, ids:[id de especie, ...]} ]
   - fecha/lugar = PRIMER registro de esa especie en eBird.
   - Cada lugar de "lugares" lista TODAS las especies vistas ahí (ids).
   - foto null => la web muestra la silueta de la familia.

C) const FICHAS = { ... }          (en assets/datos.js)
   Texto del modal de cada especie encontrada. La clave es el nombre científico:
     'Nombre científico': {estado:'Frase corta', curiosidad:'Texto más largo.'}
   Toda especie que aparezca en avistamientos.json debe tener ficha.
   Este es el único paso de contenido que NO sale de eBird.

D) sync/lugares.json               (configuración de lugares)
   Une cada Location ID de eBird con el nombre que se ve en la web (y, si hace
   falta, coordenadas propias). Dos IDs con el mismo "nombre" se fusionan en un lugar.
   El lugar "Río Cuarto" (ex "Rio Cuarto - Casa") usa coordenadas genéricas A PROPÓSITO:
   no publicar la ubicación exacta de la casa.

E) El mapa (Leaflet + OpenStreetMap, se carga solo al abrir la pestaña Mapa) dibuja un marcador por cada "lugar" de avistamientos.json;
   el tamaño del círculo y el número son la cantidad de especies; al tocarlo se abre la lista de aves de ese lugar.
   Ya no hay bloques HTML por lugar ni contadores para actualizar a mano.

-----------------------------------------------------------------------
2. CÓMO ACTUALIZAR LA WEB
-----------------------------------------------------------------------

  1. eBird > My eBird > Download My Data (llega por mail) => MyEBirdData.csv
  2. Desde la raíz del repo:  python sync/sync_ebird.py MyEBirdData.csv
       (Se ignoran los registros con cantidad 0: eBird no los cuenta como especie vista.)
  3. El script imprime un resumen. Hay que resolver:
       - "FALTA FICHA": agregar la entrada en FICHAS (estado + curiosidad).
       - "Sin foto todavía": el usuario sube fotos/nombre_cientifico_en_minusculas.jpg
         y vuelve a correr el script (la detecta sola).
       - "Lugares nuevos sin nombre": agregar el ID en sync/lugares.json con nombre prolijo.
       - "Registros que no se pudieron asignar": son identificaciones tipo "A/B", "sp."
         o domésticos; no van al álbum.
  4. Subir assets/datos.js (si se tocó FICHAS), avistamientos.json, registros.json, sync/ y fotos/.

Si una especie NO existe en AVES (caso raro): agregarla al final con id = total + 1
(los totales de Córdoba/Argentina se calculan solos desde AVES y CBA; si es de Córdoba, sumar su id a CBA_EXTRA).

-----------------------------------------------------------------------
3. PORTADA (Sobre mí) — acceso al álbum
-----------------------------------------------------------------------

  - Botón "Explorar el álbum" (.album-cta) en el panel izquierdo: abre el álbum con irAlbum('enc').
  - Tira "Últimas especies sumadas" (#recientes, buildRecientes): las 8 especies más recientes
    (orden fecha+hora del primer registro en eBird), CON O SIN FOTO. Las que aún no tienen foto
    se ven con la silueta de su familia (.rec-sin-foto, borde punteado). Al tocar una se abre su ficha
    y las flechas del modal recorren la tira. Cuando se sube la foto, la silueta se reemplaza sola.
  - Tarjetas "Última ave registrada" y "Última localización": son clickeables (ficha / mapa en ese lugar).
  - El menú "Álbum" muestra el contador de especies (#nav-album-badge). irAlbum() ubica la pestaña por id (#nav-album),
    no por su texto.
  - En escritorio la portada es una pantalla partida de alto fijo y el pie de redes es fijo (~40px):
    ambas columnas reservan ese alto y se compactan en pantallas bajas (media queries max-height).

-----------------------------------------------------------------------
4. GALERÍA (pestaña Galería) — dinámica
-----------------------------------------------------------------------

  - Se muestra TODO lo que haya en la carpeta galeria/ (jpg, jpeg, png, webp, gif, avif). No hay que editar nada:
    se sube la foto al repo y aparece sola (puede tardar 1-2 min hasta que GitHub Pages publica).
  - La carpeta se lista con la API pública de GitHub (loadGaleria). El repo se deduce solo si el sitio está en
    <usuario>.github.io; con dominio propio hay que completar GALERIA_REPO = 'usuario/repo' en el script.
  - Nombre del archivo, siempre en este orden:   DDMMAAAA-DSC_0249-especie en minúsculas.jpg
      * DDMMAAAA = fecha del encuentro (10102026 = 10 Oct 2026). Es opcional pero recomendable.
      * El código de cámara se ignora. La especie se busca entre los nombres comunes de AVES
        (sin importar mayúsculas ni tildes). Si no la reconoce, igual muestra la foto con el texto del nombre.
      * El LUGAR sale de registros.json (especie + fecha). Si ese día la especie se vio en 2 o más lugares,
        o todavía no está en eBird/CSV, no se muestra lugar (nunca se inventa).
      * registros.json lo genera sync/sync_ebird.py junto con avistamientos.json: hay que subirlo cada vez.
  - Orden: fotos con fecha, de la más nueva a la más vieja; después las que no tienen fecha.
  - OTROS ANIMALES (anfibios, roedores, etc.): subir las fotos a galeria/fauna/ con el mismo formato de nombre
    (DDMMAAAA-IMG_0123-escuerzo.jpg). Aparece sola una pestaña "Otros animales" dentro de Galería (si la carpeta está
    vacía o no existe, no se muestra). El nombre sale del archivo; no se busca en el álbum de aves ni suma a las estadísticas.
  - No existe más galeria.json: la galería muestra solo las fotos que haya en la carpeta, con los datos del nombre.
    Si la API de GitHub no responde (límite de pedidos), se avisa con un mensaje en vez de mostrar fotos.
  - Conviene subir fotos livianas (~1600-2000 px de lado largo, <500 KB): la galería carga los archivos tal cual.

-----------------------------------------------------------------------
5. DATOS, FILTROS Y EXTRAS (todo sale de avistamientos.json + registros.json; no hay que tocar nada a mano)
  - REGIÓN: el álbum y "Las que me faltan" tienen selector Córdoba / Argentina (REGION, setRegion). Córdoba = ids 1–416
    (CBA); Argentina = todo AVES (1.088, lista de eBird). La portada muestra las dos barras (Córdoba y Argentina).
    Una especie de Córdoba vista solo en otra provincia cuenta para Argentina, no para la barra de Córdoba
    (avistamientos.json guarda "prov" por especie: X = Córdoba, M = Mendoza, etc.). Los ids 417+ no tienen ficha (FICHAS) todavía.
-----------------------------------------------------------------------

  - Portada: tarjeta "Próximo hito" (HITOS = 50,100,150,200,... en el script) y "Ave del día" (una especie con foto,
    la misma durante todo el día).
  - Pestaña Datos (buildDatos): Números (gráficos propios en SVG), Línea de tiempo (cada especie nueva, con su número
    de orden) y Las que me faltan (por familia). Se recalcula sola con cada CSV nuevo.
  - Álbum: botón "Filtros" (familia, lugar, orden) además del buscador, que ahora ignora tildes.
  - Galería: buscador y filtro por año (aparecen con 4 fotos o más); cada foto con especie reconocida tiene "Ficha →".
  - Lightbox: doble toque / pellizco / rueda para ampliar y deslizar para pasar de foto.
  - Modo oscuro: botón ☾ abajo a la izquierda (la elección se guarda en el navegador de cada visitante).

-----------------------------------------------------------------------
6. CONVENCIONES
-----------------------------------------------------------------------

  - Fechas: AAAA-MM-DD.
  - Fotos: fotos/nombre_cientifico_en_minusculas_con_guiones_bajos.jpg (las sube el usuario).
  - Si eBird corrige una identificación, se corrige en eBird y se vuelve a correr el script.
  - Todo sale de avistamientos.json / registros.json (en el navegador solo se guarda el modo claro/oscuro elegido).
  - La web hay que abrirla desde un servidor (GitHub Pages o similar): con doble clic
    (file://) el navegador bloquea fetch() y no cargan ni avistamientos ni galería.

=======================================================================

## Fichas en la voz de Felix: chequeo con cada CSV

Los textos de las fichas (`_fichas/<slug>.json`, `secciones`) y los minis de `assets/datos.js` (`estado`, `curiosidad`) están escritos en el tono de Felix (casual, argentino, títulos de sección variados). Reglas:

- Nada de arrancar con cantidad de visitas o lugares. Cada ficha declara su apertura en la clave `apertura` del JSON (`primera`, `ultima`, `cualquiera`, `unica`, `mismo_lugar` o `ninguna`). El "primer registro" y la lista de encuentros de la página son dinámicos (salen de registros.json), esos no se desactualizan.
- Solo datos verificables (eBird/registros.json, fotos.json, guía Pearman & Areta, Wikipedia). Nada de anécdotas inventadas ni "cantidad máxima de ejemplares" (eBird no lo da).
- **Después de cada CSV/actualización de registros.json correr:** `python3 -I _fichas/verificar_aperturas.py .` Si marca fichas desactualizadas (por ejemplo una apertura `ultima` o `unica` que ya no es cierta porque se la vio de nuevo), reescribir esa apertura en el JSON (cambiar el tipo o la fecha) y volver a correr `gen_fichas.py`.
- Los minis de especies sin ficha son reformulaciones de textos sin verificar; si se hace la ficha, se reescriben con sus datos.
