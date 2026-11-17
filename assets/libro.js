/* Vista de LIBRO del álbum (opción de visualización). Se carga recién al tocar "Ver como libro".
   Modelo: P = páginas (0 = tapa). Hoja k: frente = P[2k], dorso = P[2k+1]. Spread s muestra P[2s-1] (izq.) y P[2s] (der.).
   Las hojas dadas vuelta (k < s) giran -180° sobre el lomo. Todas las especies, con huecos las no vistas y la figurita pegada las vistas. */
(function () {
  const CAP = 12, PW = 700; let PH = 740;     // figuritas por hoja; tamaño natural de una página (px, luego se escala)
  let LM = 0, COLS = 4, V = 0, vModo = false, P = [], L = 0, S = 0, ctx = null, busy = false, book = null, drag = null;

  function armar() {
    const todas = avesReg().slice().sort((a, b) => a.tx - b.tx), numMap = {};
    todas.forEach((a, i) => numMap[a.id] = i + 1);
    ctx = { todas, numMap, nuevas: new Set(recientes(8, false).map(a => a.id)) };
    const fi = new Map(); todas.forEach(x => { if (!fi.has(x.familiaEsp)) fi.set(x.familiaEsp, fi.size); });
    ctx.col = x => fi.get(x.familiaEsp) % 6;
    const hojas = [];
    for (let i = 0; i < todas.length; i += CAP) hojas.push({ aves: todas.slice(i, i + CAP) });
    if (vModo) {   // celular vertical: UNA página por vez (cada hoja ocupa el lado de abajo; el de arriba queda vacío)
      P = [{ t: 'tapa' }]; hojas.forEach(h => { P.push({ t: 'vacia' }); P.push(Object.assign({ t: 'hoja' }, h)); }); P.push({ t: 'vacia' }, { t: 'dorso' }, { t: 'vacia' });   // al final: interior de la contratapa
      L = P.length / 2; LM = L - 1; return;
    }
    P = [{ t: 'tapa' }, { t: 'dorso', guia: 1 }].concat(hojas.map(h => Object.assign({ t: 'hoja' }, h)));   // 'dorso' = interior de la tapa, a la izquierda de la 1.ª hoja
    if (hojas.length % 2) P.push({ t: 'blanca' });   // hoja en blanco para que la última hoja quede a la izquierda
    P.push({ t: 'dorso' }, { t: 'fin' });             // interior de la contratapa (a la derecha de la última hoja) y contratapa
    L = P.length / 2; LM = L;
  }

  function cara(i) {
    if (vModo && P[i] && P[i].t === 'vacia') {   // página izquierda 'de relleno' (realismo): solo la 3.ª columna (la pegada al pliegue) de una hoja anterior, con miniaturas livianas
      const q = P[i - 1]; if (q && q.t === 'tapa') return '<div class="lpag lpag-dorso"></div>'; if (!q || q.t !== 'hoja') return '<div class="lpag lpag-vacia"></div>';
      return '<div class="lpag lpag-izq"><div class="album-grid stk libro-grid">' + q.aves.map((a, j) => { if (j % 3 !== 2) return '<div class="lcell" style="visibility:hidden"></div>'; return `<div class="lcell fc${ctx.col(a)}">${albFig(a, j, ctx.numMap, ctx.nuevas)}</div>`; }).join('') + '</div></div>';
    }
    const pg = P[i]; if (!pg || pg.t === 'vacia') return '<div class="lpag lpag-vacia"></div>';
    if (pg.t === 'tapa') {
      const v = ctx.todas.filter(visto).length;
      const tot = ctx.todas.length, pct = tot ? Math.round(v / tot * 100) : 0, C = 2 * Math.PI * 44, cba = REGION === 'cba';
      const ult = ctx.todas.filter(a => visto(a) && avist[a.id] && avist[a.id].foto).slice(-3).map(a => { const f = String(avist[a.id].foto).replace(/^\//, ''); return `<img src="${TH(f)}" alt="" onerror="this.onerror=null;this.src='/${f}'">`; }).join('');
      return `<div class="lpag lpag-tapa" style="--tp:url(/assets/paisajes/${cba ? 'sierra' : 'cerro'}.jpg)"><div class="lt-foto"><i class="lt-cinta"></i><div class="lt-ph"></div><span>${cba ? 'Córdoba' : '<i class="ar"></i>Argentina'}</span></div><div class="lt-titulo"><h2>Álbum de <em>aves</em></h2></div><p class="lt-sub">Félix Santiago · Aves · Río Cuarto</p><div class="lt-guia2"><h3>Cómo está organizado</h3><ul><li><b>Por familias.</b> Agrupadas por familia, cada una con su color y su etiqueta al comienzo.</li><li><b>Con foto.</b> Las figuritas a color son las que ya vi; las grises están por encontrar.</li><li><b>Fichas.</b> Tocá una figurita para ver su ficha.</li><li><b>Para moverte.</b> Pasá de hoja con las flechas o arrastrando, y saltá de familia con el selector de arriba.</li></ul></div><div class="lt-pie"><div class="lt-anillo"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44"/><circle class="rg" cx="50" cy="50" r="44" stroke-dasharray="${(C * pct / 100).toFixed(1)} ${C.toFixed(1)}"/></svg><b>${v}</b><small>de ${tot}</small></div>${ult ? `<div class="lt-ult">${ult}<small>Últimas especies</small></div>` : ''}</div></div>`;
    }
    if (pg.t === 'blanca') return '<div class="lpag"></div>';
    if (pg.t === 'dorso') return pg.guia ? '<div class="lpag lpag-dorso"><div class="ld-guia"><h3>Cómo está organizado</h3><ul><li><b>Por familias.</b> Las aves van agrupadas por familia, cada una con su color y su etiqueta al comienzo.</li><li><b>Con foto.</b> Las figuritas a color son las que ya vi; las grises están por encontrar.</li><li><b>Fichas.</b> Tocá una figurita para ver su ficha.</li><li><b>Para moverte.</b> Pasá de hoja con las flechas o arrastrando, y saltá de familia con el índice de la izquierda.</li></ul></div></div>' : '<div class="lpag lpag-dorso"></div>';
    if (pg.t === 'fin') return '<div class="lpag lpag-fin"><div class="lt-foto lt-foto-fin"><i class="lt-cinta"></i><div class="lt-ph" style="--tp:url(/assets/paisajes/ocaso.jpg)"></div></div><div class="lt-logo"></div><p>Seguirá completándose<br>en cada salida.</p><small>felixsantiago.com.ar</small></div>';
    // grupos de familia dentro de la hoja: la etiqueta va sobre la primera figurita de cada tramo (por fila)
    const A = pg.aves, tag = {}, pp = P[i - (vModo ? 2 : 1)], pk = i > 1 && pp && pp.aves ? pp.aves[pp.aves.length - 1] : null;
    for (let j = 0; j < A.length; j++) {
      const ini = j > 0 ? A[j - 1].familiaEsp !== A[j].familiaEsp : !(pk && pk.familiaEsp === A[j].familiaEsp);
      const cont = j === 0 && !ini;
      if (!ini && !cont) continue;
      let e = j; while (e + 1 < A.length && A[e + 1].familiaEsp === A[j].familiaEsp && Math.floor((e + 1) / COLS) === Math.floor(j / COLS)) e++;
      const tot = ctx.todas.filter(x => x.familiaEsp === A[j].familiaEsp), v = tot.filter(visto).length;
      tag[j] = { n: e - j + 1, t: A[j].familiaEsp + ' ' + v + '/' + tot.length + (cont ? ' · sigue' : '') };
    }
    return `<div class="lpag"><div class="album-grid stk libro-grid">${A.map((a, j) => `<div class="lcell fc${ctx.col(a)}${tag[j] ? ' ini' : ''}">${tag[j] ? `<span class="lgt" style="width:calc(${tag[j].n}00% + ${(tag[j].n - 1) * 0}px)" title="${escHtml(tag[j].t)}">${escHtml(tag[j].t)}</span>` : ''}${albFig(a, j, ctx.numMap, ctx.nuevas)}</div>`).join('')}</div><div class="lpag-n">${vModo ? i / 2 : i - 1}</div></div>`;
  }

  // Memoria: sólo las hojas cercanas a la actual tienen contenido y se dibujan (en Argentina son ~90 hojas; en celular se caía la pestaña)
  function llenar() {
    book.querySelectorAll('.leaf').forEach(el => {
      const k = +el.dataset.k, d = Math.abs(k - S), lim = vModo ? 1 : 2;
      if (d <= lim && !el.dataset.ok) { el.querySelector('.front').innerHTML = cara(2 * k); el.querySelector('.back').innerHTML = cara(2 * k + 1); el.dataset.ok = 1; }
      else if (d > lim + 1 && el.dataset.ok) { el.querySelector('.front').innerHTML = ''; el.querySelector('.back').innerHTML = ''; delete el.dataset.ok; }
      el.style.display = d > lim + 1 ? 'none' : '';
    });
  }

  function marca() {
    if (vModo) return marcaV();
    const ix = document.getElementById('libro-idx'); if (!ix) return;
    const en = new Set(); [P[2 * S - 1], P[2 * S]].forEach(pg => pg && pg.aves && pg.aves.forEach(a => en.add(a.familiaEsp)));
    ix.querySelectorAll('button[data-s]').forEach(b => b.classList.toggle('on', b.dataset.f ? en.has(b.dataset.f) : S === 0));
    const b = ix.querySelector('button[data-s].on'); if (b) ix.scrollTo({ top: b.offsetTop - ix.clientHeight / 2 + b.clientHeight / 2, behavior: MENOS_MOV ? 'auto' : 'smooth' });
  }

  function pos() {
    book.querySelectorAll('.leaf').forEach(el => {
      const k = +el.dataset.k, volt = k < S;
      el.classList.toggle('volt', volt); el.classList.toggle('cur', k === S);
      el.style.zIndex = volt ? k + 1 : L - k + 1;
    });
    book.style.setProperty('--sh', vModo ? 0 : S === 0 ? -0.5 : S === LM && !vModo ? 0.5 : 0);   // cerrado: la tapa/contratapa queda centrada
    const sel = document.getElementById('libro-sel'); if (sel) sel.value = S;
    const info = document.getElementById('libro-info'); if (info) info.textContent = S === 0 ? 'Tapa' : S === LM ? 'Contratapa' : S === 1 ? 'Hoja 1' : 'Hojas ' + (2 * S - 2) + ' y ' + (2 * S - 1);
    document.getElementById('libro-prev').disabled = S === 0; document.getElementById('libro-next').disabled = S === LM;
    llenar(); marca();
  }

  function ir(n) {
    n = Math.max(0, Math.min(LM, n)); if (n === S || busy) return;
    const dir = n > S ? 1 : -1, ms = MENOS_MOV ? 0 : 650;
    const k = dir > 0 ? S : S - 1, el = book.querySelector('.leaf[data-k="' + k + '"]');
    busy = true; llenar();
    // hojas intermedias saltan; sólo la más cercana anima
    const leafs = [...book.querySelectorAll('.leaf')];
    el.style.zIndex = L + 5;
    const prev = S; S = n;
    leafs.forEach(l => { const kk = +l.dataset.k; if (l !== el) { l.classList.toggle('volt', kk < S); l.style.zIndex = kk < S ? kk + 1 : L - kk + 1; } });
    el.classList.toggle('volt', dir > 0);
    if (vModo) leafs.forEach(l => l.classList.toggle('cur', +l.dataset.k === S));
    book.style.setProperty('--sh', vModo ? 0 : S === 0 ? -0.5 : S === LM && !vModo ? 0.5 : 0);
    setTimeout(() => { busy = false; pos(); }, ms);
    const sel = document.getElementById('libro-sel'); if (sel) sel.value = S;
    if (prev !== S) { const info = document.getElementById('libro-info'); if (info) info.textContent = S === 0 ? 'Tapa' : S === LM ? 'Contratapa' : S === 1 ? 'Hoja 1' : 'Hojas ' + (2 * S - 2) + ' y ' + (2 * S - 1); }
    document.getElementById('libro-prev').disabled = S === 0; document.getElementById('libro-next').disabled = S === LM;
    llenar(); marca();
  }

  const esMov = () => Math.min(window.innerWidth, window.innerHeight) < 600;

  function escala() {
    const st = document.getElementById('libro-stage'); if (!st) return;
    const full = esMov(), fit = !full && document.body.classList.contains('fit-pc') && document.body.classList.contains('libro-modo');
    if (vModo && full) {
      const top = (document.querySelector('.lv-top') || { offsetHeight: 44 }).offsetHeight, k = Math.max(.2, Math.min((innerWidth - 8) / (PW + 16), (innerHeight - top - 126) / PH));
      book.style.setProperty('--sc', k.toFixed(3)); book.style.setProperty('--ph', PH + 'px'); st.style.height = Math.round(PH * k) + 'px'; return;
    }
    let sc;
    if (full) sc = Math.min((window.innerWidth - 120 - 96) / (2 * PW), (window.innerHeight - 12) / PH);
    else if (fit) {
      // PC en pantalla fija: el libro (proporción fija) ocupa el mayor tamaño que entra en el hueco de su contenedor
      const main = st.parentElement, bar = main.querySelector('.libro-bar'), ay = main.querySelector('.libro-ayuda');
      const usado = (bar ? bar.offsetHeight + 12 : 0) + (ay && getComputedStyle(ay).display !== 'none' ? ay.offsetHeight + 4 : 0) + 14;
      sc = Math.min(2, (main.clientWidth - 110) / (2 * PW), (main.clientHeight - usado) / PH);
    } else sc = Math.min(1.5, (window.innerWidth - 390) / (2 * PW), (window.innerHeight - st.getBoundingClientRect().top - scrollY - 120) / PH);
    const k = Math.max(.2, sc);
    book.style.setProperty('--sc', k.toFixed(3));
    st.style.height = Math.round(PH * k) + 'px';
    const ix = document.getElementById('libro-idx'); if (ix) ix.style.maxHeight = full ? window.innerHeight + 'px' : fit ? document.getElementById('libro').clientHeight + 'px' : Math.round(PH * k + 56) + 'px';
  }
  window.libroEscala = escala;

  window.libroRender = function () {
    const c = document.getElementById('album-container'); if (!c) return;
    const full0 = esMov(); vModo = full0 && innerHeight > innerWidth; COLS = vModo ? 3 : 4; PH = vModo ? 1120 : 740; armar(); if (S > LM) S = 0; busy = false;
    const grupos = P.map((pg, i) => pg.t === 'hoja' ? '<option value="' + Math.ceil(i / 2) + '">Hoja ' + i + ' · ' + pg.aves[0].comun + ' …</option>' : '').join('');
    const full = esMov(), vert = full && innerHeight > innerWidth; vModo = vert; COLS = vert ? 3 : 4; PH = vert ? 1120 : 740;
    if (vert) return renderV(c);
    let host = c; const h0 = document.getElementById('libro-host'); if (h0) h0.remove();
    if (full) { c.innerHTML = ''; host = document.body.appendChild(Object.assign(document.createElement('div'), { id: 'libro-host' })); }
    const fa = new Map(); ctx.todas.forEach((x, n) => { let g = fa.get(x.familiaEsp); if (!g) fa.set(x.familiaEsp, g = { f: x.familiaEsp, c: ctx.col(x), s: Math.ceil((Math.floor(n / CAP) + 2) / 2), n: 0, v: 0 }); g.n++; if (visto(x)) g.v++; });
    const idx = '<button data-s="0" data-f="" onclick="libroSalta(0)"><b>Tapa</b></button>' + [...fa.values()].map(g => `<button class="fc${g.c}" data-s="${g.s}" data-f="${escHtml(g.f)}" onclick="libroSalta(${g.s})"><i></i><span>${escHtml(g.f)}</span><em>${g.v}/${g.n}</em></button>`).join('');
    host.innerHTML = `<div class="libro stickers${full ? ' libro-full' : ''}" id="libro"><aside class="libro-idx" id="libro-idx">${full ? `<div class="libro-reg"><button class="${REGION === 'cba' ? 'on' : ''}" onclick="setRegion('cba')">Córdoba</button><button class="${REGION === 'arg' ? 'on' : ''}" onclick="setRegion('arg')"><i class="ar"></i>Argentina</button></div>` : ''}<h4>Familias</h4>${idx}</aside><div class="libro-main"><div class="libro-stage" id="libro-stage"><button class="libro-nav pv" id="libro-prev" onclick="libroIr(-1)" aria-label="Hoja anterior">◀</button><div class="libro-book" id="libro-book">${
      Array.from({ length: L }, (_, k) => `<div class="leaf" data-k="${k}"><div class="face front"></div><div class="face back"></div></div>`).join('')
    }</div><button class="libro-nav nx" id="libro-next" onclick="libroIr(1)" aria-label="Hoja siguiente">▶</button></div>
    <div class="libro-bar"><select id="libro-sel" aria-label="Ir a una hoja" onchange="libroSalta(this.value)"><option value="0">Tapa</option>${grupos}</select><span id="libro-info"></span>${full ? '<button class="libro-x" onclick="libroToggle()">✕ Cerrar</button>' : ''}</div>
    ${full ? '<div class="libro-girar"><b>↻</b><p>Girá el celular<br>para ver el álbum como libro</p><button class="libro-x" onclick="libroToggle()">✕ Cerrar</button></div>' : '<p class="libro-ayuda">Tocá una figurita para verla · pasá de hoja con ◀ ▶, con las flechas del teclado o arrastrando una esquina</p>'}</div></div>`;
    { const ix = document.getElementById('libro-idx'); if (ix) { const fijo = document.createElement('div'); fijo.className = 'libro-idx-fijo'; const k = [...ix.children]; const tapa = k.find(e => e.tagName === 'BUTTON'); k.filter(e => e.classList.contains('libro-reg') || e.tagName === 'H4').concat(tapa ? [tapa] : []).forEach(e => fijo.appendChild(e)); ix.prepend(fijo); } }
    sinZoom(full);
    if (full && !vert) { try { (document.documentElement.requestFullscreen() || Promise.reject()).then(() => screen.orientation.lock('landscape')).catch(() => {}); } catch (e) {} }
    book = document.getElementById('libro-book'); escala(); pos();
    if (full) [150, 500, 1200].forEach(t => setTimeout(() => { if (window.libroOn && book && book.isConnected) escala(); }, t));
    if (!full) window.scrollTo(0, 0);
    book.addEventListener('pointerdown', onDown);
  };

  // ── Libro en celular VERTICAL: doble página APILADA (como un almanaque de pared). Hoja de arriba = página par, hoja de abajo = página impar; al pasar, la hoja de abajo se levanta hacia arriba. Mismo motor y paginación que el libro apaisado, con el lomo horizontal. ──
  window.libroVFam = f => { const i = P.findIndex(pg => pg.aves && pg.aves[0].familiaEsp === f); window.libroSalta(f ? Math.ceil(i / 2) : 0); };
  function marcaV() {
    const sel = document.getElementById('lv-sel'); if (!sel) return;
    let f = ''; const en = new Set(); [P[2 * S - 1], P[2 * S]].forEach(pg => { if (pg && pg.aves) { pg.aves.forEach(a => en.add(a.familiaEsp)); if (!f) f = pg.aves[0].familiaEsp; } }); sel.value = f;
  }
  function renderV(c) {
    c.innerHTML = ''; const h0 = document.getElementById('libro-host'); if (h0) h0.remove();
    const host = document.body.appendChild(Object.assign(document.createElement('div'), { id: 'libro-host' }));
    const fams = []; P.forEach(pg => { if (pg.aves && !fams.includes(pg.aves[0].familiaEsp)) fams.push(pg.aves[0].familiaEsp); });
    host.innerHTML = `<div class="libro stickers libro-full libro-vv" id="libro"><div class="lv-top"><div class="reg-sel reg-sticky" role="group" aria-label="Región"><button class="reg-b ${REGION === 'cba' ? 'on' : ''}" data-reg="cba" onclick="setRegion('cba')">Córdoba</button><button class="reg-b ${REGION === 'arg' ? 'on' : ''}" data-reg="arg" onclick="setRegion('arg')"><i class="ar"></i>Argentina</button></div><button class="fb2 lv-lista" onclick="libroToggle()" aria-label="Ver como lista">☰ Lista</button><select id="lv-sel" class="fb2" aria-label="Ir a una familia" onchange="libroVFam(this.value)"><option value="">Tapa</option>${fams.map(f => `<option value="${escHtml(f)}">${escHtml(f)}</option>`).join('')}</select></div><div class="libro-stage" id="libro-stage"><button class="libro-nav pv" id="libro-prev" onclick="libroIr(-1)" aria-label="Hoja anterior">◀</button><div class="libro-book" id="libro-book">${Array.from({ length: L }, (_, k) => `<div class="leaf" data-k="${k}"><div class="face front"></div><div class="face back"></div></div>`).join('')}</div><button class="libro-nav nx" id="libro-next" onclick="libroIr(1)" aria-label="Hoja siguiente">▶</button></div></div>`;
    sinZoom(true); book = document.getElementById('libro-book'); escala(); pos();
    [150, 500, 1200].forEach(t => setTimeout(() => { if (window.libroOn && book && book.isConnected) escala(); }, t));
    book.addEventListener('pointerdown', onDown);
  }
  ['resize', 'orientationchange'].forEach(ev => window.addEventListener(ev, () => {
    if (!window.libroOn || !document.getElementById('libro-host')) return;
    const vert = esMov() && innerHeight > innerWidth;
    if (vert !== vModo && window.libroRender) libroRender();
  }));
  window.libroIr = d => ir(S + d);
  window.libroSalta = v => ir(+v);
  const vp = () => document.querySelector('meta[name=viewport]'); let vpOrig = null;
  function sinZoom(on) { const m = vp(); if (!m) return; if (on) { if (vpOrig === null) vpOrig = m.content; m.content = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'; } else if (vpOrig !== null) { m.content = vpOrig; vpOrig = null; } }
  ['gesturestart', 'gesturechange'].forEach(ev => document.addEventListener(ev, e => { if (document.getElementById('libro-host')) e.preventDefault(); }));
  document.addEventListener('touchmove', e => { if (e.touches.length > 1 && document.getElementById('libro-host')) e.preventDefault(); }, { passive: false });
  window.libroSalir = () => { sinZoom(false); S = 0; const h = document.getElementById('libro-host'); if (h) h.remove(); try { document.fullscreenElement && document.exitFullscreen(); } catch (e) {} };

  // Arrastrar una esquina: sólo decide la dirección (el giro lo anima el CSS)
  function onDown(e) {
    if (e.pointerType === 'touch') { drag = { x: e.clientX, y: e.clientY, d: 0, any: 1 }; return; }
    if (e.button || e.target.closest('.fig')) return;
    const r = book.getBoundingClientRect(), x = e.clientX - r.left, w = r.width;
    const borde = x < w * .12 ? -1 : x > w * .88 ? 1 : 0;
    if (!borde) return; drag = { x: e.clientX, d: borde };
  }
  window.addEventListener('pointermove', e => { if (!drag) return; const dx = e.clientX - drag.x; if (drag.any) { if (Math.abs(dx) > 50) { const d = dx < 0 ? 1 : -1; drag = null; ir(S + d); } return; } if (Math.abs(dx) > 60 && Math.sign(dx) === -drag.d) { const d = drag.d; drag = null; ir(S + d); } });
  window.addEventListener('pointerup', () => { drag = null; });
  window.addEventListener('keydown', e => { if (!window.libroOn || !book || e.target.closest('input,select,textarea')) return; if (e.key === 'ArrowRight') ir(S + 1); if (e.key === 'ArrowLeft') ir(S - 1); });
  ['resize', 'orientationchange', 'fullscreenchange'].forEach(ev => window.addEventListener(ev, () => { if (window.libroOn && book && book.isConnected) escala(); }));
})();
