/* Mascotas animadas de las fichas de especie · Félix Santiago Aves
   Cada tanto el personaje de la especie pasa por el borde de la pantalla (sin tapar ni bloquear nada)
   y al tocarlo reacciona. Se apaga con "reducir movimiento". Los SVG miran a la izquierda. */
(function () {
  var host = document.getElementById('mascota');
  if (!host) return;
  var kind = host.getAttribute('data-m');
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var BASE = '/assets/mascotas/';
  // viewBox de cada SVG: [x, y, ancho, alto]. Todos comparten el mismo sistema de coordenadas del dibujo.
  var VB = {
    'carancho-animado': [20, 8, 240, 392], 'carancho-caminar': [20, 8, 240, 392], 'carancho-comer': [-55, 8, 315, 392],
    'carancho-saltar': [20, -110, 240, 510], 'carancho-volar': [-150, -80, 560, 540],
    'carpintero-macho-animado': [30, 14, 215, 392], 'carpintero-macho-comer': [-20, 14, 265, 392],
    'carpintero-macho-trepar': [-40, 14, 285, 392], 'carpintero-macho-volar': [-170, -90, 600, 560],
    'carpintero-hembra-animado': [30, 14, 215, 392], 'carpintero-hembra-comer': [-20, 14, 265, 392],
    'carpintero-hembra-trepar': [-40, 14, 285, 392], 'carpintero-hembra-volar': [-170, -90, 600, 560],
    'carpintero-tronco': [-40, 14, 285, 392],
    'gallineta-animado': [-30, -20, 370, 320], 'gallineta-caminar': [-30, -20, 370, 320], 'gallineta-comer': [-30, -20, 370, 320],
    'gallineta-llamar': [-30, -20, 370, 320], 'gallineta-volar': [-30, -20, 370, 320]
  };
  // G = y del dibujo donde apoya el personaje, P = x del dibujo alrededor del cual se espeja
  var CFG = {
    carancho: { G: 400, P: 140, name: 'Caranchito' },
    gallineta: { G: 300, P: 155, name: 'Gallineta' },
    carpintero: { G: 406, P: -40, name: 'Carpintero lomo blanco' }
  }[kind];
  if (!CFG) return;

  // estilos (se inyectan acá para no tocar el resto del sitio)
  var st = document.createElement('style');
  st.textContent = '.ma-stage{position:fixed;left:0;right:0;bottom:0;height:0;z-index:5;pointer-events:none}' +
    '.ma{position:absolute;left:0;bottom:0;width:0;height:0;will-change:transform;pointer-events:none}' +
    '.ma .fl{position:absolute;left:0;bottom:0;width:0;height:0}' +
    '.ma img{position:absolute;max-width:none;display:block;user-select:none;-webkit-user-select:none;-webkit-user-drag:none;pointer-events:none}' +
    '.ma.tap img{pointer-events:auto;cursor:pointer;-webkit-tap-highlight-color:transparent}';
  document.head.appendChild(st);
  var stage = document.createElement('div'); stage.className = 'ma-stage'; stage.setAttribute('aria-hidden', 'true');
  document.body.appendChild(stage);

  var K = 0.3;
  function medida() { K = window.innerWidth < 640 ? 0.2 : 0.3; }
  function W() { return window.innerWidth; }
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function visible() {
    return new Promise(function (r) {
      if (!document.hidden) return r();
      var f = function () { if (!document.hidden) { document.removeEventListener('visibilitychange', f); r(); } };
      document.addEventListener('visibilitychange', f);
    });
  }

  // Actor: un personaje con su sprite actual, posición y dirección
  function Actor(lift) {
    this.el = document.createElement('div'); this.el.className = 'ma';
    this.fl = document.createElement('div'); this.fl.className = 'fl';
    this.img = document.createElement('img'); this.img.alt = ''; this.img.draggable = false;
    this.fl.appendChild(this.img); this.el.appendChild(this.fl); stage.appendChild(this.el);
    this.lift = lift || 0; this.anim = null; this.dir = 1; this.file = null;
    this.x = -9999; this.y = 0; this.pos();
  }
  Actor.prototype.sprite = function (file) {
    var v = VB[file]; if (!v) return;
    this.file = file;
    var i = this.img;
    if (i.getAttribute('data-f') !== file) { i.setAttribute('data-f', file); i.src = BASE + file + '.svg'; }
    i.style.width = v[2] * K + 'px'; i.style.height = v[3] * K + 'px';
    i.style.left = (v[0] - CFG.P) * K + 'px';
    i.style.bottom = -(v[1] + v[3] - CFG.G) * K + 'px';
    this.fl.style.transformOrigin = '0 0';
  };
  Actor.prototype.face = function (d) { this.dir = d; this.fl.style.transform = 'scaleX(' + d + ')'; };
  Actor.prototype.pos = function () { this.el.style.transform = 'translate(' + this.x + 'px,' + (-this.lift - this.y) + 'px)'; };
  Actor.prototype.stop = function () { if (this.anim) { try { this.anim.cancel(); } catch (e) {} this.anim = null; } };
  Actor.prototype.put = function (x, y) { this.stop(); this.x = x; this.y = y || 0; this.pos(); };
  // mueve de (x0,y0) a (x1,y1); arco: altura extra en el punto medio
  Actor.prototype.go = function (x1, ms, y1, arco) {
    var self = this, x0 = this.curX(), y0 = this.curY(); y1 = y1 == null ? y0 : y1;
    this.stop();
    var t = function (x, y) { return { transform: 'translate(' + x + 'px,' + (-self.lift - y) + 'px)' }; };
    var kf = [t(x0, y0)];
    if (arco) { kf.push(t((x0 + x1) / 2, Math.max(y0, y1) + arco)); }
    kf.push(t(x1, y1));
    this.x = x1; this.y = y1;
    this.anim = this.el.animate(kf, { duration: ms, easing: arco ? 'ease-in-out' : 'linear', fill: 'forwards' });
    var a = this.anim;
    return new Promise(function (res) { a.onfinish = function () { if (self.anim === a) { self.pos(); a.cancel(); self.anim = null; } res(); }; a.oncancel = res; });
  };
  Actor.prototype.curX = function () { var r = this.el.getBoundingClientRect(); return r.left; };
  Actor.prototype.curY = function () { var r = this.el.getBoundingClientRect(); return (window.innerHeight - r.bottom) - this.lift; };
  Actor.prototype.remove = function () { this.stop(); this.el.remove(); };

  var token = 0, actores = [];
  function limpia() { actores.forEach(function (a) { a.remove(); }); actores = []; }
  function nuevo(lift) { var a = new Actor(lift); actores.push(a); return a; }
  function ok(t) { return t === token; }
  function marg() { return 620 * K + 40; }   // para entrar/salir de pantalla sin que se vea el recorte

  /* ---------- carancho ---------- */
  var carancho = {
    // cruza caminando
    caminar: async function (t) {
      var a = nuevo(); var d = pick([-1, 1]); a.face(d); a.sprite('carancho-caminar');
      var x0 = d < 0 ? W() + marg() : -marg(), x1 = d < 0 ? -marg() : W() + marg();
      a.put(x0); a.tapear = true; ligar(a);
      await a.go(x1, Math.abs(x1 - x0) / (80 * K / .3) * 1000);
    },
    // cruza volando, haciendo un arco
    volar: async function (t) {
      var a = nuevo(); var d = pick([-1, 1]); a.face(d); a.sprite('carancho-volar');
      var x0 = d < 0 ? W() + marg() : -marg(), x1 = d < 0 ? -marg() : W() + marg();
      var h = rnd(0.25, 0.55) * window.innerHeight;
      a.put(x0, h * 0.5); ligar(a);
      await a.go(x1, Math.abs(x1 - x0) / 230 * 1000 * (K / .3 < 1 ? .8 : 1), h * 0.7, h * 0.35);
    },
    // camina, se frena, come y sigue
    comer: async function (t) {
      var a = nuevo(); var d = pick([-1, 1]); a.face(d); a.sprite('carancho-caminar');
      var x0 = d < 0 ? W() + marg() : -marg(), x1 = d < 0 ? -marg() : W() + marg();
      var xm = rnd(0.3, 0.7) * W();
      a.put(x0); ligar(a);
      await a.go(xm, Math.abs(xm - x0) / (80 * K / .3) * 1000); if (!ok(t)) return;
      a.sprite('carancho-animado'); await sleep(rnd(1500, 2800)); if (!ok(t)) return;
      a.sprite('carancho-comer'); await sleep(8000); if (!ok(t)) return;
      a.sprite('carancho-animado'); await sleep(1200); if (!ok(t)) return;
      a.sprite('carancho-caminar'); await a.go(x1, Math.abs(x1 - xm) / (80 * K / .3) * 1000);
    },
    // camina y en el medio pega unos saltos
    saltar: async function (t) {
      var a = nuevo(); var d = pick([-1, 1]); a.face(d); a.sprite('carancho-caminar');
      var x0 = d < 0 ? W() + marg() : -marg(), x1 = d < 0 ? -marg() : W() + marg();
      var xm = rnd(0.3, 0.7) * W();
      a.put(x0); ligar(a);
      await a.go(xm, Math.abs(xm - x0) / (80 * K / .3) * 1000); if (!ok(t)) return;
      a.sprite('carancho-saltar'); await sleep(1300 * 3); if (!ok(t)) return;
      a.sprite('carancho-caminar'); await a.go(x1, Math.abs(x1 - xm) / (80 * K / .3) * 1000);
    },
    // asoma desde abajo, mira y se esconde
    asomar: async function (t) {
      var a = nuevo(); a.face(pick([-1, 1])); a.sprite('carancho-animado');
      var xm = rnd(0.2, 0.8) * W(), h = 392 * K;
      a.put(xm, -h); ligar(a);
      await a.go(xm, 900, -h * 0.55); if (!ok(t)) return;
      await sleep(4800); if (!ok(t)) return;
      await a.go(xm, 700, -h);
    },
    // toque: salta dos veces y se va volando
    reaccion: async function (a, t) {
      var x = a.curX(), d = a.dir;
      a.sprite('carancho-saltar'); a.put(x, 0);
      await sleep(1300 * 2); if (!ok(t)) return;
      a.sprite('carancho-volar'); var x1 = d < 0 ? -marg() : W() + marg();
      await a.go(x1, Math.abs(x1 - x) / 260 * 1000 + 500, window.innerHeight * 0.6, window.innerHeight * 0.15);
    },
    pesos: ['caminar', 'volar', 'comer', 'saltar', 'asomar', 'caminar', 'comer']
  };

  /* ---------- gallineta ---------- */
  var gallineta = {
    caminar: async function (t) {
      var a = nuevo(); var d = pick([-1, 1]); a.face(d); a.sprite('gallineta-caminar');
      var x0 = d < 0 ? W() + marg() : -marg(), x1 = d < 0 ? -marg() : W() + marg();
      a.put(x0); ligar(a);
      await a.go(x1, Math.abs(x1 - x0) / (95 * K / .3) * 1000);
    },
    // camina, para a llamar y a comer
    llamar: async function (t) {
      var a = nuevo(); var d = pick([-1, 1]); a.face(d); a.sprite('gallineta-caminar');
      var x0 = d < 0 ? W() + marg() : -marg(), x1 = d < 0 ? -marg() : W() + marg();
      var xm = rnd(0.25, 0.75) * W(); a.put(x0); ligar(a);
      await a.go(xm, Math.abs(xm - x0) / (95 * K / .3) * 1000); if (!ok(t)) return;
      a.sprite('gallineta-animado'); await sleep(1500); if (!ok(t)) return;
      a.sprite('gallineta-llamar'); await sleep(2400 * 2); if (!ok(t)) return;
      a.sprite('gallineta-comer'); await sleep(rnd(5000, 8000)); if (!ok(t)) return;
      a.sprite('gallineta-caminar'); await a.go(x1, Math.abs(x1 - xm) / (95 * K / .3) * 1000);
    },
    // vuelo corto de un lado al otro
    volar: async function (t) {
      var a = nuevo(); var d = pick([-1, 1]); a.face(d); a.sprite('gallineta-volar');
      var x0 = d < 0 ? W() + marg() : -marg(), x1 = d < 0 ? -marg() : W() + marg();
      a.put(x0, 20); ligar(a);
      await a.go(x1, Math.abs(x1 - x0) / 260 * 1000, 20, rnd(60, 140));
    },
    // se asoma tímida entre los juncos del borde
    asomar: async function (t) {
      var a = nuevo(); a.face(pick([-1, 1])); a.sprite('gallineta-animado');
      var xm = rnd(0.15, 0.85) * W(), h = 300 * K;
      a.put(xm, -h); ligar(a);
      await a.go(xm, 800, -h * 0.5); if (!ok(t)) return;
      await sleep(3200); if (!ok(t)) return;
      a.sprite('gallineta-llamar'); await sleep(2400); if (!ok(t)) return;
      await a.go(xm, 600, -h);
    },
    // toque: se asusta y sale volando
    reaccion: async function (a, t) {
      var x = a.curX(), d = a.dir;
      var y = Math.max(0, a.y); a.sprite('gallineta-volar'); a.put(x, y);
      var x1 = d < 0 ? -marg() : W() + marg();
      await a.go(x1, Math.abs(x1 - x) / 300 * 1000 + 400, window.innerHeight * 0.45, window.innerHeight * 0.1);
    },
    pesos: ['caminar', 'llamar', 'volar', 'asomar', 'llamar', 'caminar']
  };

  /* ---------- carpintero: tronco pegado al borde izquierdo ---------- */
  var carpintero = {
    tronco: async function (t) {
      var sx = pick(['macho', 'hembra']); var alt = window.innerHeight * rnd(0.18, 0.4);
      var tr = nuevo(alt); tr.sprite('carpintero-tronco'); tr.face(1);
      var a = nuevo(alt); a.face(1); a.sprite('carpintero-' + sx + '-animado'); a.img.title = CFG.name + ' ' + sx; a.sx = sx;
      var out = -(285 * K) - 20; tr.put(out); a.put(out); ligar(a);
      await Promise.all([tr.go(0, 1100), a.go(0, 1100)]); if (!ok(t)) return;
      // trepa, pica, come y se va volando
      a.sprite('carpintero-' + sx + '-trepar'); await sleep(rnd(2500, 3600)); if (!ok(t)) return;
      a.sprite('carpintero-' + sx + '-animado'); await sleep(rnd(3500, 5500)); if (!ok(t)) return;
      a.sprite('carpintero-' + sx + '-comer'); await sleep(4400 * 1.5); if (!ok(t)) return;
      a.sprite('carpintero-' + sx + '-animado'); await sleep(1500); if (!ok(t)) return;
      await irse(a, tr, sx, t);
    },
    reaccion: async function (a, t) {
      var sx = a.sx || 'macho';
      await irse(a, actores[0], sx, t);
    },
    pesos: ['tronco']
  };
  async function irse(a, tr, sx, t) {
    // da la vuelta y sale volando hacia la derecha; el tronco se retira por la izquierda
    var y = a.y; a.face(-1); a.sprite('carpintero-' + sx + '-volar'); a.put(a.x + 360 * K, y);
    var h = window.innerHeight;
    var p1 = a.go(W() + marg(), (W() / 240) * 1000 + 600, y + h * 0.15, h * 0.18);
    await sleep(500); if (tr) await tr.go(-(285 * K) - 20, 800);
    await p1;
  }

  /* ---------- interacción y rutina ---------- */
  var ESC = { carancho: carancho, gallineta: gallineta, carpintero: carpintero }[kind];
  var reaccionando = false;
  function ligar(a) {
    a.el.classList.add('tap');
    a.img.title = a.img.title || CFG.name;
    a.img.addEventListener('click', function () {
      if (reaccionando) return; reaccionando = true;
      var t = ++token;
      Promise.resolve(ESC.reaccion(a, t)).catch(function () {}).then(function () {
        limpia(); reaccionando = false; programa(rnd(20000, 35000));
      });
    });
  }

  var veces = 0, ultima = '';
  async function programa(espera) {
    var t = ++token;
    await sleep(espera); if (!ok(t)) return;
    await visible(); if (!ok(t)) return;
    medida(); limpia();
    var opciones = ESC.pesos.filter(function (n) { return n !== ultima || ESC.pesos.length === 1; });
    var n = pick(opciones); ultima = n; veces++;
    try { await ESC[n](t); } catch (e) {}
    if (!ok(t)) return;
    limpia();
    programa(veces < 6 ? rnd(14000, 26000) : rnd(40000, 70000));
  }
  // precarga de los SVG de esta especie para que no parpadeen al cambiar de movimiento
  Object.keys(VB).forEach(function (f) {
    if (f.indexOf(kind === 'carpintero' ? 'carpintero' : kind) === 0) { var i = new Image(); i.src = BASE + f + '.svg'; }
  });
  programa(3000);
})();
