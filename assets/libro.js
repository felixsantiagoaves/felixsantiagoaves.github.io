/* Vista de LIBRO del álbum (opción de visualización). Se carga recién al tocar "Ver como libro".
   Modelo: P = páginas (0 = tapa). Hoja k: frente = P[2k], dorso = P[2k+1]. Spread s muestra P[2s-1] (izq.) y P[2s] (der.).
   Las hojas dadas vuelta (k < s) giran -180° sobre el lomo. Todas las especies, con huecos las no vistas y la figurita pegada las vistas. */
(function () {
  const CAP = 9, PW = 540, PH = 860;     // figuritas por hoja; tamaño natural de una página (px, luego se escala)
  let P = [], L = 0, S = 0, ctx = null, busy = false, book = null, drag = null;

  function armar() {
    const todas = avesReg().slice().sort((a, b) => a.tx - b.tx), numMap = {};
    todas.forEach((a, i) => numMap[a.id] = i + 1);
    ctx = { todas, numMap, nuevas: new Set(recientes(8, false).map(a => a.id)) };
    const fams = [], m = new Map();
    todas.forEach(a => { if (!m.has(a.familiaEsp)) { m.set(a.familiaEsp, []); fams.push(a.familiaEsp); } m.get(a.familiaEsp).push(a); });
    const hojas = []; let cur = null;
    const flush = () => { if (cur && cur.aves.length) hojas.push(cur); cur = null; };
    fams.forEach(f => {
      const l = m.get(f);
      if (l.length > CAP) {                       // familia grande: varias hojas parejas
        flush(); const n = Math.ceil(l.length / CAP), sz = Math.ceil(l.length / n);
        for (let i = 0; i < n; i++) hojas.push({ fams: [f + ' (' + (i + 1) + '/' + n + ')'], aves: l.slice(i * sz, (i + 1) * sz) });
        return;
      }
      if (cur && cur.aves.length + l.length > CAP) flush();   // familias chicas se juntan hasta llenar una hoja
      if (!cur) cur = { fams: [], aves: [] };
      cur.fams.push(f); cur.aves.push(...l);
    });
    flush();
    P = [{ t: 'tapa' }].concat(hojas.map(h => Object.assign({ t: 'hoja' }, h)));
    if (P.length % 2) P.push({ t: 'fin' });
    L = P.length / 2;
  }

  function cara(i) {
    const pg = P[i]; if (!pg) return '<div class="lpag lpag-vacia"></div>';
    if (pg.t === 'tapa') {
      const v = ctx.todas.filter(visto).length;
      return `<div class="lpag lpag-tapa"><div class="lt-logo"></div><h2>Álbum de aves</h2><p>${REGION === 'cba' ? 'Córdoba' : 'Argentina'}</p><b>${v} <i>de</i> ${ctx.todas.length}</b><small>Félix Santiago · Aves</small></div>`;
    }
    if (pg.t === 'fin') return '<div class="lpag lpag-fin"><p>Seguirá completándose<br>en cada salida.</p></div>';
    const ok = pg.aves.filter(visto).length;
    return `<div class="lpag"><div class="lpag-hd"><span class="lpag-fam">${pg.fams.map(escHtml).join(' · ')}</span><span class="lpag-c${ok === pg.aves.length ? ' full' : ''}">${ok} de ${pg.aves.length}</span></div>
      <div class="album-grid stk libro-grid">${pg.aves.map((a, j) => albFig(a, j, ctx.numMap, ctx.nuevas)).join('')}</div><div class="lpag-n">${i}</div></div>`;
  }

  function llenar() {
    book.querySelectorAll('.leaf').forEach(el => {
      const k = +el.dataset.k;
      if (!el.dataset.ok && Math.abs(k - S) <= 2) { el.querySelector('.front').innerHTML = cara(2 * k); el.querySelector('.back').innerHTML = cara(2 * k + 1); el.dataset.ok = 1; }
    });
  }

  function pos() {
    book.querySelectorAll('.leaf').forEach(el => {
      const k = +el.dataset.k, volt = k < S;
      el.classList.toggle('volt', volt);
      el.style.zIndex = volt ? k + 1 : L - k + 1;
    });
    book.style.setProperty('--sh', S === 0 ? -0.5 : S === L ? 0.5 : 0);   // cerrado: la tapa/contratapa queda centrada
    const sel = document.getElementById('libro-sel'); if (sel) sel.value = S;
    const info = document.getElementById('libro-info'); if (info) info.textContent = S === 0 ? 'Tapa' : S === L ? 'Contratapa' : 'Hojas ' + (2 * S - 1) + ' y ' + (2 * S);
    document.getElementById('libro-prev').disabled = S === 0; document.getElementById('libro-next').disabled = S === L;
    llenar();
  }

  function ir(n) {
    n = Math.max(0, Math.min(L, n)); if (n === S || busy) return;
    const dir = n > S ? 1 : -1, ms = MENOS_MOV ? 0 : 650;
    const k = dir > 0 ? S : S - 1, el = book.querySelector('.leaf[data-k="' + k + '"]');
    busy = true; llenar();
    // hojas intermedias saltan; sólo la más cercana anima
    const leafs = [...book.querySelectorAll('.leaf')];
    el.style.zIndex = L + 5;
    const prev = S; S = n;
    leafs.forEach(l => { const kk = +l.dataset.k; if (l !== el) { l.classList.toggle('volt', kk < S); l.style.zIndex = kk < S ? kk + 1 : L - kk + 1; } });
    el.classList.toggle('volt', dir > 0);
    book.style.setProperty('--sh', S === 0 ? -0.5 : S === L ? 0.5 : 0);
    setTimeout(() => { busy = false; pos(); }, ms);
    const sel = document.getElementById('libro-sel'); if (sel) sel.value = S;
    if (prev !== S) { const info = document.getElementById('libro-info'); if (info) info.textContent = S === 0 ? 'Tapa' : S === L ? 'Contratapa' : 'Hojas ' + (2 * S - 1) + ' y ' + (2 * S); }
    document.getElementById('libro-prev').disabled = S === 0; document.getElementById('libro-next').disabled = S === L;
    // si saltamos varias hojas, pre-llenar las del destino
    llenar();
  }

  function escala() {
    const st = document.getElementById('libro-stage'); if (!st) return;
    const sc = Math.min(1, (window.innerWidth - 60) / (2 * PW), (window.innerHeight - 300) / PH);
    book.style.setProperty('--sc', Math.max(.35, sc).toFixed(3));
    st.style.height = Math.round(PH * Math.max(.35, sc)) + 'px';
  }

  window.libroRender = function () {
    const c = document.getElementById('album-container'); if (!c) return;
    armar(); if (S > L) S = 0; busy = false;
    const grupos = P.map((pg, i) => pg.t === 'hoja' ? '<option value="' + Math.ceil(i / 2) + '">' + i + ' · ' + escHtml(pg.fams.join(' · ')) + '</option>' : '').join('');
    c.innerHTML = `<div class="libro" id="libro"><div class="libro-stage" id="libro-stage"><div class="libro-book" id="libro-book">${
      Array.from({ length: L }, (_, k) => `<div class="leaf" data-k="${k}"><div class="face front"></div><div class="face back"></div></div>`).join('')
    }</div></div>
    <div class="libro-bar"><button id="libro-prev" onclick="libroIr(-1)" aria-label="Hoja anterior">◀</button><select id="libro-sel" aria-label="Ir a una hoja" onchange="libroSalta(this.value)"><option value="0">Tapa</option>${grupos}</select><span id="libro-info"></span><button id="libro-next" onclick="libroIr(1)" aria-label="Hoja siguiente">▶</button></div>
    <p class="libro-ayuda">Tocá una figurita para verla · pasá de hoja con ◀ ▶, con las flechas del teclado o arrastrando una esquina</p></div>`;
    book = document.getElementById('libro-book'); escala(); pos();
    book.addEventListener('pointerdown', onDown);
  };
  window.libroIr = d => ir(S + d);
  window.libroSalta = v => ir(+v);
  window.libroSalir = () => { S = 0; };

  // Arrastrar una esquina: sólo decide la dirección (el giro lo anima el CSS)
  function onDown(e) {
    if (e.button || e.target.closest('.fig')) return;
    const r = book.getBoundingClientRect(), x = e.clientX - r.left, w = r.width;
    const borde = x < w * .12 ? -1 : x > w * .88 ? 1 : 0;
    if (!borde) return; drag = { x: e.clientX, d: borde };
  }
  window.addEventListener('pointermove', e => { if (!drag) return; const dx = e.clientX - drag.x; if (Math.abs(dx) > 60 && Math.sign(dx) === -drag.d) { const d = drag.d; drag = null; ir(S + d); } });
  window.addEventListener('pointerup', () => { drag = null; });
  window.addEventListener('keydown', e => { if (!window.libroOn || !book || e.target.closest('input,select,textarea')) return; if (e.key === 'ArrowRight') ir(S + 1); if (e.key === 'ArrowLeft') ir(S - 1); });
  window.addEventListener('resize', () => { if (window.libroOn) escala(); });
})();
