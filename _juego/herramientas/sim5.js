const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent(require('fs').readFileSync('/home/claude/felixsantiagoaves.github.io/juego/index.html','utf8'));await p.evaluate(()=>{window.SIMULA=true});
const res=await p.evaluate((mds)=>{const out={};const avail=o=>!((o.en<0&&G.en+o.en<0)||(o.na<0&&G.nafta+o.na<0));
// valor esperado de una opción (nuevas especies esperadas - costo de recursos)
const val=(o,zi,modOverride)=>{let ef=(o.ef||1)*(G.mod||1)*(G.permM||1)*(modOverride||1);if(G.P.amp)ef=Math.pow(ef,ef<1?G.P.amp[0]:G.P.amp[1]);let s=0;for(let i=0;i<N;i++){const x=SP[i];if(G.vistas.has(x[0])||x[4]<G.P.fmin)continue;let e=ef;if(o.ari&&x[4]<2)e*=o.ari;if(G.ari>1&&x[4]<2)e*=G.ari;if(o.fam&&o.fam[0].includes(x[3]))e*=o.fam[1];const p0=Math.min(.8,prob(i,zi,G.mes)*MK(G.lugar));s+=1-Math.pow(1-p0,e)}if(o.rara)s+=o.rara*1.3;if(o.perm)s+=(o.perm-1)*22*(G.P.cal.length-G.k-1);let c=0;if(o.en)c-=o.en*2.2;if(o.na)c-=o.na*1.6;return s+ -c};
const valMi=(o,zi)=>{let m=o.mod||1;if(o.az)m=o.az[0]*o.az[1]+(1-o.az[0])*o.az[2];return val({ef:1,en:o.en,na:o.na},zi,m)-(o.az&&o.naMal?o.az[0]*Math.abs(o.naMal)*1.6:0)};
for(const md of mds)for(const st of ['azar','mejor']){const a=[];for(let k=0;k<50;k++){nuevo('t'+k+st,md);const NN=G.P.cal.length;for(let m=0;m<NN;m++){const ok=G.ops.map((z,i)=>[z,i]).filter(x=>x[0].c<=G.nafta);let pick;if(st==='azar')pick=ok[Math.floor(Math.random()*ok.length)];else pick=ok.map(x=>[x,potencial(x[0])-x[0].c*1.2]).sort((u,v)=>v[1]-u[1])[0][0];
elegirZona(pick[1]);const zi=ZK.indexOf(G.zona);viaje2();
if(G.kind==='su')aplicarSu();
else if(G.kind==='mi'){let os=G.mi.o.map((o,j)=>[o,j]).filter(([o])=>avail(o));if(!os.length)os=[[G.mi.o[G.mi.o.length-1],G.mi.o.length-1]];const c=st==='azar'?os[Math.floor(Math.random()*os.length)]:os.sort((u,v)=>valMi(v[0],zi)-valMi(u[0],zi))[0];elegirMi(c[1])}
else{let ev=G.ev.o.map((o,j)=>[o,j]).filter(([o])=>avail(o));if(!ev.length)ev=[[G.ev.o[G.ev.o.length-1],G.ev.o.length-1]];const e=st==='azar'?ev[Math.floor(Math.random()*ev.length)]:ev.sort((u,v)=>val(v[0],zi)-val(u[0],zi))[0];elegirEv(e[1])}
if(m<NN-1)sig()}a.push(G.vistas.size)}a.sort((x,y)=>x-y);out[md+'_'+st]=[a[0],a[25],a[49],Math.round(a.reduce((s,x)=>s+x,0)/a.length)]}
return out},process.argv.slice(2).length?process.argv.slice(2):['guiado','normal','experto']);
console.log(JSON.stringify(res),errs);await b.close()})()
