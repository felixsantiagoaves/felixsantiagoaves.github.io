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

  /* Mascota de la portada: una al azar entre las dibujadas; cambia sola cada tanto o al tocarla */
  var MAS = ['aguatero','atajacaminos-tijera','calandrita','carancho','carpintero-hembra','carpintero-macho','chiricote','chivi-comun','colorada','gallineta','golondrina-ceja-blanca','inambu-montaraz','inambu-silbon','juan-chiviro','monterita-de-collar','pecho-colorado','pepitero-chico','pepitero-gris','pijui-frente-gris','pitiayumi'];
  function mascota(){
    var im = document.querySelector('.fgh-dc'); if(!im) return;
    var actual = -1, ver = (typeof MASC_V !== 'undefined') ? '?v=' + MASC_V : '';
    var otra = function(){ var i; do { i = Math.floor(Math.random() * MAS.length); } while(i === actual && MAS.length > 1); actual = i; return '/assets/mascotas/' + MAS[i] + '-animado.svg' + ver; };
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
