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

  /* Menú inferior (celular): "Más" abre Especies, Estadísticas y Contacto */
  function menu(){
    var ul = document.querySelector('.nav-links'); if(!ul || ul.querySelector('.nav-mas')) return;
    var li = document.createElement('li'); li.className = 'nav-mas';
    li.innerHTML = '<a href="#" role="button" aria-haspopup="true" aria-expanded="false">Más</a>';
    ul.appendChild(li);
    var sh = document.createElement('div'); sh.className = 'fg-sheet'; sh.hidden = true;
    sh.innerHTML = '<a href="/aves/">Especies</a><a href="/estadisticas/">Estadísticas</a><a href="/contacto/">Contacto</a>';
    document.body.appendChild(sh);
    var a = li.firstChild, cerrar = function(){ sh.hidden = true; a.setAttribute('aria-expanded', 'false'); };
    a.addEventListener('click', function(e){ e.preventDefault(); sh.hidden = !sh.hidden; a.setAttribute('aria-expanded', String(!sh.hidden)); });
    document.addEventListener('click', function(e){ if(!sh.hidden && !e.target.closest('.nav-mas') && !e.target.closest('.fg-sheet')) cerrar(); });
    var act = ul.querySelector('a.active[href="/estadisticas/"], a.active[href="/contacto/"], a.active[href="/aves/"]');
    if(act) a.classList.add('active');
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', menu); else menu();
})();
