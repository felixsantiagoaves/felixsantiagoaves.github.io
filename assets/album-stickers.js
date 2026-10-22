/* Prototipo: álbum estilo figuritas, agrupado en páginas por familia.
   Reemplaza renderAlbum() de site.js. Solo se carga en /album/prototipo/ */
function renderAlbum() {
  const container = document.getElementById('album-container');
  const todas = avesReg().slice().sort((a, b) => a.tx - b.tx);
  const numMap = {}; todas.forEach((a, i) => numMap[a.id] = i + 1);
  const lista = avesFiltradas();
  const fig = (ave, i) => {
    const enc = visto(ave), av = enc ? avist[ave.id] : null;
    const foto = av && av.foto
      ? `<img class="fig-foto" loading="lazy" decoding="async" src="/${av.foto.replace(/^\//, '')}" alt="${ave.comun} (${ave.nombre}) - Fotografiado en Argentina por Félix Santiago">`
      : getSilueta(ave.familiaEsp);
    const rot = (((ave.id * 37) % 7) - 3) * 0.7;
    return `<div class="fig ${enc ? 'enc' : 'no'}" onclick="openM(${ave.id})" data-id="${ave.id}" style="--r:${rot}deg;animation-delay:${Math.min(i * 0.04, 0.5)}s">
      <span class="fig-num">${String(numMap[ave.id]).padStart(3, '0')}</span>
      <div class="fig-img"><div class="fig-svg-wrap">${foto}</div></div>
      <div class="fig-info">
        <div class="fig-co">${ave.comun}</div>
        <div class="fig-ci">${ave.nombre}</div>
        <div class="fig-fecha">${av ? fmtFecha(av.fecha) : 'Por encontrar'}</div>
      </div></div>`;
  };
  if (!lista.length) { container.innerHTML = `<div style="text-align:center;padding:3rem;font-family:'Caveat',cursive;font-size:1.2rem;color:var(--ti)">No se encontraron aves con ese criterio 🔍</div>`; return; }
  let html = '';
  if (ordenAlbum === 'tax') {
    const grupos = new Map();
    lista.forEach(a => { if (!grupos.has(a.familiaEsp)) grupos.set(a.familiaEsp, []); grupos.get(a.familiaEsp).push(a); });
    const fams = [...grupos.keys()].sort((a, b) => famIdx(a) - famIdx(b));
    fams.forEach((f, pi) => {
      const aves = grupos.get(f), tot = avesReg().filter(a => a.familiaEsp === f);
      const ok = tot.filter(a => visto(a)).length;
      html += `<section class="alb-pag"><header class="alb-pag-hd"><span class="alb-pag-n">Página ${pi + 1}</span><h3>${escHtml(f)}</h3><span class="alb-pag-c${ok === tot.length ? ' full' : ''}">${ok} de ${tot.length}</span></header><div class="album-grid stk">${aves.map(fig).join('')}</div></section>`;
    });
  } else {
    html = `<section class="alb-pag"><div class="album-grid stk">${lista.map(fig).join('')}</div></section>`;
  }
  container.innerHTML = html;
}
(function () {
  filtro = 'todas'; ordenAlbum = 'tax';
  document.querySelectorAll('.fb').forEach(b => b.classList.toggle('active', /todas/i.test(b.textContent)));
  document.getElementById('page-album').classList.add('stickers');
})();
