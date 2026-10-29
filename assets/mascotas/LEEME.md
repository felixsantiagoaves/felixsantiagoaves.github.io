# Mascotas de Félix Santiago Aves

Personajes originales dibujados en SVG (sin fondo, se escalan sin perder calidad).
Se usan en los reels y se pueden usar en la web.

| Archivo | Qué es |
|---|---|
| `carancho.svg` / `carancho.png` | Caranchito, quieto |
| `carancho-animado.svg` | Caranchito quieto pero vivo: respira, mueve la cabeza, parpadea, abre el pico y mueve cola y ala |
| `carancho-caminar.svg` | Caminando (en el lugar; lo desplazás vos con CSS) |
| `carancho-saltar.svg` | Saltando (agacha, salta, bate el ala, cae) |
| `carancho-volar.svg` | Volando (alas abiertas batiendo) |
| `carancho-comer.svg` | Comiendo: se come una por una carroña, insecto, huevo y fruto, masticando (ciclo de 8 s) |
| `carpintero-macho.svg` / `.png` | Carpintero lomo blanco macho (cabeza toda roja), agarrado a un tronco que va a su izquierda |
| `carpintero-hembra.svg` / `.png` | Hembra (frente y copete negros, lista blanca en la mejilla) |
| `carpintero-macho-animado.svg` / `carpintero-hembra-animado.svg` | Picando: dos golpes seguidos, pausa, golpes otra vez; parpadea |
| `carpintero-macho-trepar.svg` / `carpintero-hembra-trepar.svg` | Trepando a saltitos por un tronco (el tronco viene dibujado en el mismo archivo) |
| `carpintero-macho-volar.svg` / `carpintero-hembra-volar.svg` | Volando (alas abiertas con el parche canela) |
| `carpintero-macho-comer.svg` / `carpintero-hembra-comer.svg` | Comiendo una larva y un escarabajo, masticando (ciclo de 4,4 s) |
| `gallineta.svg` / `gallineta.png` | Gallineta pico pintado, quieta (mira a la izquierda) |
| `gallineta-animado.svg` | Quieta pero viva: mueve la cabeza, parpadea y sacude la cola |
| `gallineta-caminar.svg` | Caminando (en el lugar), con patas rojas largas alternando |
| `gallineta-volar.svg` | Vuelo corto (alas batiendo, patas hacia atrás) |
| `gallineta-comer.svg` | Picotea y se come un insecto, un caracol, una lombriz y semillas (ciclo de 8 s) |
| `gallineta-llamar.svg` | Llamando: levanta la cabeza, abre el pico y salen ondas de sonido (ciclo de 2,4 s) |
| `demo.html` | Página de prueba: abrila en el navegador y ves todas las animaciones, y ejemplos de cómo hacerlas cruzar la pantalla |

## Importante: dónde se mueven
Las animaciones son *en el lugar*: el personaje camina, vuela o salta sin avanzar. Para que recorra la pantalla lo desplazás con CSS (hay ejemplos en `demo.html`), por ejemplo:

```css
.carancho-camina{position:absolute;animation:cruza 14s linear infinite}
@keyframes cruza{from{left:105%}to{left:-200px}}
```
Los personajes miran a la izquierda: para que avancen hacia la derecha, espejalos con `transform:scaleX(-1)`.

## Cómo usarlos en la web

```html
<img src="/assets/mascotas/carancho-animado.svg" alt="Caranchito" height="160">
```

- Usalos con `<img>` (las animaciones corren solas, sin JavaScript).
- Las animaciones respetan `prefers-reduced-motion` (se detienen si la persona lo tiene activado).
- Los PNG son de 720 px de ancho con fondo transparente, por si necesitás un formato que no sea SVG.
- El carpintero está dibujado mirando a la izquierda, con el tronco a su izquierda. Para pegarlo a un borde derecho de otra imagen, o espejarlo: `style="transform:scaleX(-1)"`.
- Si los metés inline en el HTML (no con `<img>`), los `id` internos (`m-head`, `m-lid`, etc.) y los estilos se repiten entre mascotas y se pisan: usá un solo personaje por página en ese caso, o seguí usando `<img>`.

## En la web (fichas de especie)
- `mascotas.js` hace que el personaje pase por el borde de la pantalla en su ficha: Carancho (camina, vuela, come, salta, se asoma), Gallineta Pico Pintado (camina, llama, come, vuela, se asoma) y Carpintero Lomo Blanco (tronco en el borde izquierdo: trepa, pica, come y se va volando; sale macho o hembra al azar).
- Al tocarlo reacciona (el carancho salta y se va volando, la gallineta y el carpintero salen volando).
- No tapa ni bloquea nada, se apaga con "reducir movimiento" y en celular va más chico.
- Para sumar otra especie: agregar sus SVG acá, sus medidas en `VB` y una rutina en `mascotas.js`, y el slug en `MASCOTAS` de `_fichas/gen_fichas.py`.
- `carpintero-tronco.svg` es solo el tronco (sin pájaro) para pegarlo al borde de la pantalla.
- Las versiones de la web no llevan los metadatos de procedencia que traían los archivos originales (pesan la mitad).
