/* Vista de LIBRO del álbum (opción de visualización). Se carga recién al tocar "Ver como libro".
   Modelo: P = páginas (0 = tapa). Hoja k: frente = P[2k], dorso = P[2k+1]. Spread s muestra P[2s-1] (izq.) y P[2s] (der.).
   Las hojas dadas vuelta (k < s) giran -180° sobre el lomo. Todas las especies, con huecos las no vistas y la figurita pegada las vistas. */
(function () {
  const CAP = 12, PW = 700, PH = 740;     // figuritas por hoja; tamaño natural de una página (px, luego se escala)
  let P = [], L = 0, S = 0, ctx = null, busy = false, book = null, drag = null;

  function armar() {
    const todas = avesReg().slice().sort((a, b) => a.tx - b.tx), numMap = {};
    todas.forEach((a, i) => numMap[a.id] = i + 1);
    ctx = { todas, numMap, nuevas: new Set(recientes(8, false).map(a => a.id)) };
    const fi = new Map(); todas.forEach(x => { if (!fi.has(x.familiaEsp)) fi.set(x.familiaEsp, fi.size); });
    ctx.col = x => fi.get(x.familiaEsp) % 6;
    const hojas = [];
    for (let i = 0; i < todas.length; i += CAP) hojas.push({ aves: todas.slice(i, i + CAP) });
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
    // grupos de familia dentro de la hoja: la etiqueta va sobre la primera figurita de cada tramo (por fila)
    const A = pg.aves, tag = {}, pk = i > 1 && P[i - 1].aves ? P[i - 1].aves[P[i - 1].aves.length - 1] : null;
    for (let j = 0; j < A.length; j++) {
      const ini = j > 0 ? A[j - 1].familiaEsp !== A[j].familiaEsp : !(pk && pk.familiaEsp === A[j].familiaEsp);
      const cont = j === 0 && !ini;
      if (!ini && !cont) continue;
      let e = j; while (e + 1 < A.length && A[e + 1].familiaEsp === A[j].familiaEsp && Math.floor((e + 1) / 4) === Math.floor(j / 4)) e++;
      const tot = ctx.todas.filter(x => x.familiaEsp === A[j].familiaEsp), v = tot.filter(visto).length;
      tag[j] = { n: e - j + 1, t: A[j].familiaEsp + ' ' + v + '/' + tot.length + (cont ? ' · sigue' : '') };
    }
    return `<div class="lpag"><div class="album-grid stk libro-grid">${A.map((a, j) => `<div class="lcell fc${ctx.col(a)}${tag[j] ? ' ini' : ''}">${tag[j] ? `<span class="lgt" style="width:calc(${tag[j].n}00% + ${(tag[j].n - 1) * 0}px)" title="${escHtml(tag[j].t)}">${escHtml(tag[j].t)}</span>` : ''}${albFig(a, j, ctx.numMap, ctx.nuevas)}</div>`).join('')}</div><div class="lpag-n">${i}</div></div>`;
  }

  function llenar() {
    book.querySelectorAll('.leaf').forEach(el => {
      const k = +el.dataset.k;
      if (!el.dataset.ok && Math.abs(k - S) <= 2) { el.querySelector('.front').innerHTML = cara(2 * k); el.querySelector('.back').innerHTML = cara(2 * k + 1); el.dataset.ok = 1; }
    });
  }

  function marca() {
    const ix = document.getElementById('libro-idx'); if (!ix) return;
    ix.querySelectorAll('button').forEach(b => b.classList.toggle('on', +b.dataset.s === S));
    const b = ix.querySelector('button.on'); if (b) ix.scrollTo({ top: b.offsetTop - ix.clientHeight / 2 + b.clientHeight / 2, behavior: MENOS_MOV ? 'auto' : 'smooth' });
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
    llenar(); marca();
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
    llenar(); marca();
  }

  const esMov = () => Math.min(window.innerWidth, window.innerHeight) < 600;

  function escala() {
    const st = document.getElementById('libro-stage'); if (!st) return;
    const full = esMov(), sc = full ? Math.min((window.innerWidth - 110) / (2 * PW), (window.innerHeight - 50) / PH) : Math.min(1.5, (window.innerWidth - 390) / (2 * PW), (window.innerHeight - st.getBoundingClientRect().top - scrollY - 120) / PH), k = Math.max(.2, sc);
    book.style.setProperty('--sc', k.toFixed(3));
    st.style.height = Math.round(PH * k) + 'px';
    const ix = document.getElementById('libro-idx'); if (ix) ix.style.maxHeight = Math.round(PH * k + 56) + 'px';
  }

  window.libroRender = function () {
    const c = document.getElementById('album-container'); if (!c) return;
    armar(); if (S > L) S = 0; busy = false;
    const grupos = P.map((pg, i) => pg.t === 'hoja' ? '<option value="' + Math.ceil(i / 2) + '">Hoja ' + i + ' · ' + pg.aves[0].comun + ' …</option>' : '').join('');
    const full = esMov();
    let host = c; const h0 = document.getElementById('libro-host'); if (h0) h0.remove();
    if (full) { c.innerHTML = ''; host = document.body.appendChild(Object.assign(document.createElement('div'), { id: 'libro-host' })); }
    const idx = Array.from({ length: L + 1 }, (_, s) => { const pg = P[2 * s - 1], f = pg && pg.aves ? pg.aves[0].familiaEsp : '';
      return `<button data-s="${s}" onclick="libroSalta(${s})"><b>${s === 0 ? 'Tapa' : s === L ? (pg && pg.aves ? 'Hoja ' + (2 * s - 1) : 'Final') : (2 * s - 1) + '–' + (2 * s)}</b><span>${escHtml(f)}</span></button>`; }).join('');
    host.innerHTML = `<div class="libro stickers${full ? ' libro-full' : ''}" id="libro">${full ? '' : `<aside class="libro-idx" id="libro-idx"><h4>Índice</h4>${idx}</aside>`}<div class="libro-main"><div class="libro-stage" id="libro-stage"><button class="libro-nav pv" id="libro-prev" onclick="libroIr(-1)" aria-label="Hoja anterior">◀</button><div class="libro-book" id="libro-book">${
      Array.from({ length: L }, (_, k) => `<div class="leaf" data-k="${k}"><div class="face front"></div><div class="face back"></div></div>`).join('')
    }</div><button class="libro-nav nx" id="libro-next" onclick="libroIr(1)" aria-label="Hoja siguiente">▶</button></div>
    <div class="libro-bar"><select id="libro-sel" aria-label="Ir a una hoja" onchange="libroSalta(this.value)"><option value="0">Tapa</option>${grupos}</select><span id="libro-info"></span>${full ? '<button class="libro-x" onclick="libroToggle()">✕ Cerrar</button>' : ''}</div>
    ${full ? '<div class="libro-girar"><b>↻</b><p>Girá el celular<br>para ver el álbum como libro</p><button class="libro-x" onclick="libroToggle()">✕ Cerrar</button></div>' : '<p class="libro-ayuda">Tocá una figurita para verla · pasá de hoja con ◀ ▶, con las flechas del teclado o arrastrando una esquina</p>'}</div></div>`;
    if (full) { try { (document.documentElement.requestFullscreen() || Promise.reject()).then(() => screen.orientation.lock('landscape')).catch(() => {}); } catch (e) {} }
    book = document.getElementById('libro-book'); escala(); pos();
    if (!full) window.scrollTo(0, 0);
    book.addEventListener('pointerdown', onDown);
  };
  window.libroIr = d => ir(S + d);
  window.libroSalta = v => ir(+v);
  window.libroSalir = () => { S = 0; const h = document.getElementById('libro-host'); if (h) h.remove(); try { document.fullscreenElement && document.exitFullscreen(); } catch (e) {} };

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
