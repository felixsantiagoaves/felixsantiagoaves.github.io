/* Página individual de especie: tema, visor de fotos y mapa de avistamientos */
(function(){
  var de=document.documentElement;
  // Tema claro/oscuro (misma preferencia que el resto del sitio)
  var btn=document.getElementById('tema-btn');
  function pintaBtn(){ if(btn){ var d=de.dataset.theme==='dark'; btn.textContent=d?'☀':'☾'; btn.title=d?'Modo claro':'Modo oscuro'; } }
  pintaBtn();
  if(btn) btn.addEventListener('click',function(){
    var d=de.dataset.theme==='dark'; if(d) delete de.dataset.theme; else de.dataset.theme='dark';
    try{ localStorage.setItem('tema', d?'light':'dark'); }catch(e){}
    pintaBtn();
  });
  // Visor de fotos
  var lb=document.getElementById('lb'), items=[].slice.call(document.querySelectorAll('[data-full]')), idx=0;
  function show(i){
    idx=Math.max(0,Math.min(items.length-1,i)); var a=items[idx];
    lb.querySelector('img').src=a.getAttribute('data-full'); lb.querySelector('img').alt=a.getAttribute('data-alt')||'';
    lb.querySelector('.cap').textContent=a.getAttribute('data-cap')||'';
    lb.querySelector('.pv').disabled=idx===0; lb.querySelector('.nx').disabled=idx===items.length-1;
    var ar=lb.querySelectorAll('.pv,.nx'); for(var k=0;k<ar.length;k++) ar[k].style.display=items.length>1?'':'none';
  }
  function open(i){ show(i); lb.classList.add('open'); document.body.style.overflow='hidden'; }
  function close(){ lb.classList.remove('open'); document.body.style.overflow=''; }
  var hero=document.getElementById('hero-img'); if(hero&&items.length){ hero.addEventListener('click',function(){ open(0); }); }
  items.forEach(function(a,i){ a.addEventListener('click',function(e){ e.preventDefault(); open(i); }); });
  if(lb){
    lb.querySelector('.x').addEventListener('click',close);
    lb.querySelector('.pv').addEventListener('click',function(){show(idx-1);});
    lb.querySelector('.nx').addEventListener('click',function(){show(idx+1);});
    lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
    document.addEventListener('keydown',function(e){ if(!lb.classList.contains('open')) return; if(e.key==='Escape') close(); else if(e.key==='ArrowLeft') show(idx-1); else if(e.key==='ArrowRight') show(idx+1); });
    var x0=null; lb.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; },{passive:true});
    lb.addEventListener('touchend',function(e){ if(x0===null) return; var dx=e.changedTouches[0].clientX-x0; if(Math.abs(dx)>50) show(idx+(dx<0?1:-1)); x0=null; });
  }
  // Compartir
  var sh=document.getElementById('compartir');
  if(sh) sh.addEventListener('click',function(){
    var u=location.href.split('#')[0], t=document.title;
    if(navigator.share){ navigator.share({title:t,url:u}).catch(function(){}); }
    else if(navigator.clipboard){ navigator.clipboard.writeText(u).then(function(){ sh.textContent='¡Enlace copiado!'; setTimeout(function(){ sh.textContent='Compartir'; },1800); }); }
  });
  // Mapa con mis avistamientos de esta especie
  var el=document.getElementById('mapa-ave'); if(!el) return;
  var id=el.getAttribute('data-id'), nota=document.getElementById('mapa-nota');
  Promise.all([fetch('/registros.json').then(function(r){return r.json();}),fetch('/avistamientos.json').then(function(r){return r.json();})]).then(function(res){
    var reg=res[0], av=res[1], fechas=(reg.r&&reg.r[id])||{}, coords={};
    (av.lugares||[]).forEach(function(l){ coords[l.nombre]={lat:l.lat,lon:l.lon}; });
    var por={}; Object.keys(fechas).forEach(function(d){ fechas[d].forEach(function(i){ var n=reg.lugares[i]; if(!n||!coords[n]) return; var p=por[n]||(por[n]={n:n,c:0,u:''}); p.c++; if(d>p.u) p.u=d; }); });
    var lugares=Object.keys(por).map(function(k){return por[k];});
    if(!lugares.length){ el.style.display='none'; if(nota) nota.style.display='none'; return; }
    var css=document.createElement('link'); css.rel='stylesheet'; css.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'; document.head.appendChild(css);
    var sc=document.createElement('script'); sc.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    sc.onload=function(){
      var m=L.map(el,{scrollWheelZoom:false}), pts=[];
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'}).addTo(m);
      function f(d){ var p=d.split('-'); return p[2]+'/'+p[1]+'/'+p[0]; }
      lugares.forEach(function(p){
        var c=coords[p.n], ll=[c.lat,c.lon]; pts.push(ll);
        L.circleMarker(ll,{radius:7+Math.min(10,Math.sqrt(p.c)*3),color:'#414833',weight:2,fillColor:'#a68a64',fillOpacity:.85}).addTo(m)
         .bindPopup('<b>'+p.n.replace(/</g,'&lt;')+'</b><br>'+p.c+(p.c===1?' encuentro':' encuentros')+' · último: '+f(p.u));
      });
      if(pts.length===1) m.setView(pts[0],11); else m.fitBounds(pts,{padding:[30,30],maxZoom:12});
      if(nota) nota.textContent=lugares.length+(lugares.length===1?' lugar':' lugares')+'. El tamaño del círculo indica cuántas veces la vi en cada uno.';
    };
    document.head.appendChild(sc);
  }).catch(function(){ el.style.display='none'; });
})();
