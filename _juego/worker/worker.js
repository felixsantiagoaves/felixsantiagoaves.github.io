// Ranking de "Mi año pajarero" — Cloudflare Worker + D1 (binding: DB)
const ORIGENES = ['https://felixsantiago.com.ar', 'https://www.felixsantiago.com.ar', 'https://felixsantiagoaves.github.io'];
// Techo por perfil: un poco por encima del máximo de las simulaciones (140 / 190 / 224)
const MAX = { guiado: 150, normal: 205, experto: 250 };
const MALAS = /(put[oa]s?|mierda|pelotud|boludo|conchudo|verga|pij[ao]|cagon|culo|forr[oa]|nazi|hitler|http|www\.|\.com|@)/i;

function cors(req) {
  const o = req.headers.get('Origin') || '';
  return {
    'Access-Control-Allow-Origin': ORIGENES.includes(o) ? o : ORIGENES[0],
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}
const json = (req, obj, status = 200, extra = {}) =>
  new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json', ...cors(req), ...extra } });

async function sha(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].slice(0, 12).map(x => x.toString(16).padStart(2, '0')).join('');
}
async function top(env, perfil, n = 20) {
  const r = await env.DB.prepare(
    'SELECT nombre, MAX(especies) AS e FROM scores WHERE perfil = ? GROUP BY nombre ORDER BY e DESC, MIN(ts) ASC LIMIT ?'
  ).bind(perfil, n).all();
  return r.results;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(req) });

    if (req.method === 'GET' && url.pathname === '/top') {
      const p = url.searchParams.get('perfil');
      if (!MAX[p]) return json(req, { error: 'perfil' }, 400);
      return json(req, { perfil: p, top: await top(env, p) }, 200, { 'Cache-Control': 'public, max-age=30' });
    }

    if (req.method === 'POST' && url.pathname === '/score') {
      if (!ORIGENES.includes(req.headers.get('Origin') || '')) return json(req, { error: 'origen' }, 403);
      let b; try { b = await req.json(); } catch { return json(req, { error: 'json' }, 400); }
      const perfil = String(b.perfil || ''), esp = Number(b.especies);
      let nombre = String(b.nombre || '').replace(/[\u0000-\u001f<>"'`\\]/g, '').trim().slice(0, 20);
      if (!nombre) nombre = 'Anónimo';
      if (MALAS.test(nombre)) nombre = 'Pajarero anónimo';
      if (!MAX[perfil] || !Number.isInteger(esp) || esp < 0 || esp > MAX[perfil]) return json(req, { error: 'puntaje' }, 400);

      const ip = await sha((req.headers.get('CF-Connecting-IP') || 'x') + (env.SALT || ''));
      const ahora = Date.now();
      const rec = await env.DB.prepare('SELECT COUNT(*) AS c FROM scores WHERE ip = ? AND ts > ?').bind(ip, ahora - 3600e3).first();
      if (rec.c >= 12) return json(req, { error: 'demasiadas' }, 429);

      await env.DB.prepare('INSERT INTO scores (nombre, perfil, especies, ip, ts) VALUES (?, ?, ?, ?, ?)').bind(nombre, perfil, esp, ip, ahora).run();
      const mejores = await env.DB.prepare(
        'SELECT COUNT(*) AS c FROM (SELECT nombre, MAX(especies) AS m FROM scores WHERE perfil = ? GROUP BY nombre) WHERE m > ?'
      ).bind(perfil, esp).first();
      return json(req, { ok: true, nombre, puesto: mejores.c + 1, top: await top(env, perfil, 10) });
    }
    return json(req, { error: 'no' }, 404);
  },
};
