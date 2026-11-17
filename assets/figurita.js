/* Rediseño "figurita": menú inferior en el celular, aros de los contadores y botón de la última especie. */
(function(){
  /* Contadores: aro del porcentaje, "faltan para…" */
  window.fgStats = function(v, pc, pa){
    var set = function(id, p){ var e = document.getElementById(id); if(e) e.setAttribute('stroke-dasharray', (p * 2.827) + ' 283'); };
    set('fg-ring-cba', pc); set('fg-ring-arg', pa);
    var nx = (typeof HITOS !== 'undefined') ? HITOS.find(function(h){ return h > v; }) : null;
    var f = document.getElementById('fg-faltan'), l = document.getElementById('fg-faltan-l');
    if(f && nx){ f.textContent = nx - v; if(l) l.textContent = 'Faltan para las ' + nx; }
    else if(f){ f.textContent = '✓'; if(l) l.textContent = '¡Álbum completo!'; }
  };
  /* Última especie sumada: burst */
  var ult = null;
  window.fgUltima = function(a, lista){
    ult = [a, lista];
    var n = document.getElementById('fg-burst-n'); if(n && a) n.textContent = 'N.º ' + String(a.id).padStart(3, '0');
  };
  window.fgAbrirUltima = function(){ if(ult && typeof abrirDesdePortada === 'function') abrirDesdePortada(ult[0].id, ult[1]); };

  /* Puntitos del carrusel de fotos de campo */
  function dots(){
    var g = document.getElementById('campo-grid'), d = document.getElementById('fgh-dots');
    if(!g || !d || !g.children.length) return false;
    d.innerHTML = Array.prototype.map.call(g.children, function(){ return '<i></i>'; }).join('');
    var upd = function(){ var i = Math.round(g.scrollLeft / Math.max(1, g.clientWidth)); Array.prototype.forEach.call(d.children, function(x, k){ x.className = k === i ? 'on' : ''; }); };
    g.addEventListener('scroll', upd, {passive: true}); upd(); return true;
  }
  var tries = 0, t = setInterval(function(){ if(dots() || ++tries > 40) clearInterval(t); }, 250);


  /* Fotos "En el campo": avanzan solas; se frenan si las tocás o las mirás con el mouse */
  (function(){
    if(window.matchMedia('(prefers-reduced-motion:reduce)').matches) return;
    var pausa = 0, n = 0;
    function marca(){ pausa = Date.now() + 9000; }
    var t = setInterval(function(){
      var g = document.getElementById('campo-grid'); if(!g){ if(++n > 40) clearInterval(t); return; }
      if(!g.dataset.auto){ g.dataset.auto = 1; ['pointerdown','touchstart','wheel','mouseenter','focusin'].forEach(function(e){ g.addEventListener(e, marca, {passive: true}); }); }
      if(document.hidden || Date.now() < pausa || g.children.length < 2) return;
      var r = g.getBoundingClientRect(); if(r.bottom < 0 || r.top > innerHeight) return;
      var w = g.clientWidth, i = Math.round(g.scrollLeft / Math.max(1, w)), fin = g.scrollLeft + w >= g.scrollWidth - 4;
      g.scrollTo({left: fin ? 0 : (i + 1) * w, behavior: 'smooth'});
    }, 4000);
  })();

  /* Mascota de la portada: una al azar entre las dibujadas; cambia sola cada tanto o al tocarla */
  var MAS = ['aguatero','atajacaminos-tijera','calandrita','carancho','carpintero-hembra','carpintero-macho','chiricote','chivi-comun','crespin','barullero','colorada','gallineta','golondrina-ceja-blanca','inambu-montaraz','inambu-silbon','juan-chiviro','monterita-de-collar','pecho-colorado','pepitero-chico','pepitero-gris','pijui-frente-gris','pitiayumi'];
  function mascota(){
    var im = document.querySelector('.fgh-dc'); if(!im) return;
    var actual = -1, ver = (typeof MASC_V !== 'undefined') ? '?v=' + MASC_V : '';
    var otra = function(){ var i; do { i = Math.floor(Math.random() * MAS.length); } while(i === actual && MAS.length > 1); actual = i; return '/assets/mascotas/' + MAS[i] + (window.matchMedia('(prefers-reduced-motion:reduce)').matches ? '-quieto.svg' : '-animado.svg') + ver; };
    var poner = function(){ im.style.opacity = 0; setTimeout(function(){ im.src = otra(); im.style.opacity = 1; }, 250); };
    im.src = otra();
    setInterval(function(){ if(!document.hidden) poner(); }, 9000);
    im.addEventListener('click', poner);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mascota); else mascota();

  /* Estadísticas: cada número lleva una foto de ave al azar (menos "Lugares", que lleva un paisaje) */
  function statsFotos(){
    var pane = document.getElementById('dat-num'); if(!pane) return;
    var elegidas = null;
    var poner = function(){
      if(typeof avist === 'undefined') return;
      var ks = pane.querySelectorAll('.dat-kpi'); if(!ks.length) return;
      if(!elegidas){
        var con = Object.keys(avist).filter(function(k){ return avist[k] && avist[k].foto; });
        for(var i = con.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = con[i]; con[i] = con[j]; con[j] = t; }
        elegidas = con.slice(0, ks.length).map(function(k){ return avist[k].foto; });
      }
      Array.prototype.forEach.call(ks, function(k, i){
        if(k.dataset.fgf === '1') return; k.dataset.fgf = '1';
        if(i === 1 || !elegidas[i]) return;   /* la 2.ª es "Lugares": se queda con el paisaje */
        k.style.setProperty('--k', 'linear-gradient(rgba(0,0,0,.22),rgba(0,0,0,.32)),url(/' + String(elegidas[i]).replace(/^\//, '') + ')');
      });
    };
    new MutationObserver(poner).observe(pane, {childList: true, subtree: true});
    var n = 0, t = setInterval(function(){ poner(); if(++n > 40) clearInterval(t); }, 300);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', statsFotos); else statsFotos();

  /* Menú inferior (celular): "Más" abre Especies, Estadísticas y Contacto */
  function menu(){
    var ul = document.querySelector('.nav-links'); if(!ul || ul.querySelector('.nav-mas')) return;
    var li = document.createElement('li'); li.className = 'nav-mas';
    li.innerHTML = '<a href="#" role="button" aria-haspopup="true" aria-expanded="false">Más</a>';
    ul.appendChild(li);
    var sh = document.createElement('div'); sh.className = 'fg-sheet'; sh.hidden = true;
    sh.innerHTML = '<a href="/aves/">Especies</a><a href="/estadisticas/">Estadísticas</a><a href="/juegos/">Juegos</a><a href="/contacto/">Contacto</a>';
    document.body.appendChild(sh);
    var a = li.firstChild, cerrar = function(){ sh.hidden = true; a.setAttribute('aria-expanded', 'false'); };
    a.addEventListener('click', function(e){ e.preventDefault(); sh.hidden = !sh.hidden; a.setAttribute('aria-expanded', String(!sh.hidden)); });
    document.addEventListener('click', function(e){ if(!sh.hidden && !e.target.closest('.nav-mas') && !e.target.closest('.fg-sheet')) cerrar(); });
    var act = ul.querySelector('a.active[href="/estadisticas/"], a.active[href="/contacto/"], a.active[href="/aves/"]');
    if(act) a.classList.add('active');
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', menu); else menu();

  /* Álbum en celu: la búsqueda y los botones Todas/Encontradas/Faltantes se mudan dentro del panel de Filtros,
     así la barra fija es corta y no hay que deslizar hacia el costado */
  function albumFiltros(){
    var inner = document.querySelector('.album-controls-inner'), panel = document.getElementById('album-filtros');
    var bus = document.getElementById('busqueda'); if(!inner || !panel || !bus) return;
    var wrap = document.createElement('div'); wrap.className = 'fgh-mfil'; wrap.hidden = true;
    var mql = window.matchMedia('(max-width:760px)');
    var btn = document.getElementById('btn-mas');
    var mover = function(){
      var fbs = Array.prototype.slice.call(inner.querySelectorAll('.fb')).concat(Array.prototype.slice.call(wrap.querySelectorAll('.fb')));
      if(mql.matches){
        if(!wrap.parentNode) panel.insertBefore(wrap, panel.firstChild);
        wrap.appendChild(bus); fbs.forEach(function(b){ wrap.appendChild(b); });
        wrap.hidden = false;
      } else {
        wrap.hidden = true;
        inner.insertBefore(bus, btn);
        fbs.forEach(function(b){ inner.insertBefore(b, btn); });
      }
    };
    mover();
    if(mql.addEventListener) mql.addEventListener('change', mover); else mql.addListener(mover);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', albumFiltros); else albumFiltros();
})();

/* ── Efectos ── */
(function(){
  var menos = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  /* foto de borrosa a nítida: se marca .ok cuando la imagen terminó (o falló) */
  var SEL = '.fig-foto,.rec-circulo>img';
  var ok = function(e){ var t = e.target; if(t && t.tagName === 'IMG' && t.matches(SEL)) t.classList.add('ok'); };
  document.addEventListener('load', ok, true); document.addEventListener('error', ok, true);
  setInterval(function(){ var l = document.querySelectorAll('.fig-foto:not(.ok),.rec-circulo>img:not(.ok)'); for(var i = 0; i < l.length; i++) if(l[i].complete) l[i].classList.add('ok'); }, 2500);
  if(menos) return;
  /* brillo: una pasada cuando la figurita difícil entra en pantalla */
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ var t = e.target; io.unobserve(t); setTimeout(function(){ t.classList.add('holo'); setTimeout(function(){ t.classList.remove('holo'); }, 1300); }, 350); } }); }, {threshold: .6});
    var mirar = function(){ var l = document.querySelectorAll('.fig.rara:not(.hz)'); for(var i = 0; i < l.length; i++){ l[i].classList.add('hz'); io.observe(l[i]); } };
    var c = document.getElementById('album-container');
    if(c){ new MutationObserver(mirar).observe(c, {childList: true}); mirar(); }
  }
})();

/* Portada (Sobre mí, PC): el panel "Mi álbum hoy" muestra el álbum REAL (mismas hojas, familias, etiquetas y figuritas que /album) pasando hojas solo. Contadores a la izquierda. Se pausa con el mouse, respeta "reducir movimiento", se arma en idle. Doc: _build/COMPONENTES.md */
(function(){
  var menos = window.matchMedia && matchMedia('(prefers-reduced-motion:reduce)').matches;
  function armar(){
    var stk = document.querySelector('.fgh-stk');
    if(!stk || stk.querySelector('.hl-book') || !document.body.classList.contains('fit-pc') || typeof avesReg !== 'function' || typeof albFig !== 'function') return;
    var todas = avesReg().slice().sort(function(a, b){ return a.tx - b.tx; }), numMap = {}, fi = new Map(), CAP = 12;
    todas.forEach(function(x, n){ numMap[x.id] = n + 1; if(!fi.has(x.familiaEsp)) fi.set(x.familiaEsp, fi.size); });
    var nuevas = new Set(recientes(8, false).map(function(a){ return a.id; }));
    var pgs = Math.ceil(todas.length / CAP), NP = 13, sel = [];
    for(var g0 = 0; g0 < pgs; g0++){ var c = 0; for(var q = g0 * CAP; q < (g0 + 1) * CAP && q < todas.length; q++) if(visto(todas[q]) && avist[todas[q].id] && avist[todas[q].id].foto) c++; sel.push([g0, c]); }
    sel = sel.sort(function(x, y){ return y[1] - x[1] || x[0] - y[0]; }).slice(0, NP).map(function(x){ return x[0]; }).sort(function(x, y){ return x - y; });
    var esc = typeof escHtml === 'function' ? escHtml : function(t){ return t; };
    var cara = function(n){
      var g = sel[n], A = todas.slice(g * CAP, (g + 1) * CAP), pk = g > 0 && sel[n - 1] === g - 1 ? todas[g * CAP - 1] : null, tag = {};
      for(var j = 0; j < A.length; j++){
        var ini = j > 0 ? A[j - 1].familiaEsp !== A[j].familiaEsp : !(pk && pk.familiaEsp === A[j].familiaEsp), cont = j === 0 && !ini;
        if(!ini && !cont) continue;
        var e = j; while(e + 1 < A.length && A[e + 1].familiaEsp === A[j].familiaEsp && Math.floor((e + 1) / 4) === Math.floor(j / 4)) e++;
        var tot = todas.filter(function(x){ return x.familiaEsp === A[j].familiaEsp; }), v = tot.filter(visto).length;
        tag[j] = { n: e - j + 1, t: A[j].familiaEsp + ' ' + v + '/' + tot.length + (cont ? ' · sigue' : '') };
      }
      return '<div class="lpag"><div class="album-grid stk libro-grid">' + A.map(function(a, j){
        return '<div class="lcell fc' + (fi.get(a.familiaEsp) % 6) + (tag[j] ? ' ini' : '') + '">' + (tag[j] ? '<span class="lgt" style="width:' + tag[j].n + '00%">' + esc(tag[j].t) + '</span>' : '') + albFig(a, j, numMap, nuevas) + '</div>';
      }).join('') + '</div><div class="lpag-n">' + (g + 1) + '</div></div>';
    };
    var v = todas.filter(visto).length;
    var tapa = '<div class="lpag lpag-tapa"><div class="lt-titulo"><h2>Álbum de <em>aves</em></h2></div><p class="lt-sub">Félix Santiago · Aves · Río Cuarto</p><div class="lt-pie"><div class="lt-anillo"><b>' + v + '</b><small>de ' + todas.length + '</small></div></div></div>';
    var hojas = '<div class="leaf" style="z-index:' + 9 + '"><div class="face front">' + tapa + '</div><div class="face back"><div class="lpag lpag-dorso"></div></div></div>';
    for(var k = 0; k < 6; k++) hojas += '<div class="leaf" style="z-index:' + (8 - k) + '"><div class="face front">' + cara(2 * k) + '</div><div class="face back">' + cara(2 * k + 1) + '</div></div>';
    var el = document.createElement('div'); el.className = 'hl-book libro stickers'; el.setAttribute('role', 'link'); el.setAttribute('aria-label', 'Ir al álbum'); el.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); irAlbum('todas'); }, true);
    el.innerHTML = '<div class="libro-book hb2"><div class="face front hb2-r">' + cara(NP - 1) + '</div>' + hojas + '</div>';
    stk.insertBefore(el, stk.firstChild);
    var bk = el.firstChild; bk.style.setProperty('--sh', -0.5);
    var  leaves = el.querySelectorAll('.leaf'), i = 0, pausa = false, ya = 0;
    var fit = function(){ var w = el.clientWidth, h = el.clientHeight; if(w) bk.style.setProperty('--sc', Math.min(w / 1420, h / 760).toFixed(4)); };
    fit(); addEventListener('resize', fit); if(window.ResizeObserver) new ResizeObserver(fit).observe(el);
    stk.addEventListener('mouseenter', function(){ pausa = true; }); stk.addEventListener('mouseleave', function(){ pausa = false; });
    if(menos) return;
    var paso = function(){
      if(document.hidden || pausa) return;
      if(i < leaves.length){ leaves[i].classList.add('volt'); bk.style.setProperty('--sh', 0); i++; }
      else { bk.classList.add('fade'); setTimeout(function(){ leaves.forEach(function(l){ l.style.transition = 'none'; l.classList.remove('volt'); }); leaves[0].classList.add('volt'); if(!ya){ ya = 1; leaves[0].querySelector('.back').innerHTML = cara(NP - 1); } bk.style.setProperty('--sh', 0); void bk.offsetWidth; leaves.forEach(function(l){ l.style.transition = ''; }); i = 1; bk.classList.remove('fade'); }, 700); }
    };
    setTimeout(function(){ paso(); setInterval(paso, 850); }, 700);
  }
  var arrancar = function(){ var n = 0, last = -1, est = 0, t = setInterval(function(){ n++; if(document.querySelector('.fgh-stk .hl-book') || n > 60){ clearInterval(t); return; } if(typeof avesReg !== 'function' || typeof avist === 'undefined') return; var c = 0; try{ avesReg().forEach(function(a){ if(visto(a) && avist[a.id] && avist[a.id].foto) c++; }); }catch(e){ return; } est = c > 0 && c === last ? est + 1 : 0; last = c; if(est >= 2) armar(); }, 100);   /* espera a que los datos de fotos terminen de cargar (si no, elige páginas vacías) */ };
  if(document.readyState !== 'loading') arrancar(); else addEventListener('DOMContentLoaded', arrancar);
})();
