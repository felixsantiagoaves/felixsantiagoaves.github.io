/* Sonido: música generativa suave + ambiente según el clima + trinos sintéticos + cantos reales (xeno-canto) */
const MU={on:false,amb:'day',n:0};
const mf=m=>440*Math.pow(2,(m-69)/12);
function actx(){try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();if(AC.state==='suspended')AC.resume();return AC}catch(e){return null}}
const PAD=[[50,57,61,66],[47,54,57,62],[43,50,54,59],[45,52,57,61]],PEN=[62,64,66,69,71,74,76,78];
function ruido(c,s){const b=c.createBuffer(1,c.sampleRate*s,c.sampleRate),d=b.getChannelData(0);let l=0;for(let i=0;i<d.length;i++){l=.97*l+.03*(Math.random()*2-1);d[i]=l*6}return b}
function musica(on){if(on&&!MU.on){const c=actx();if(!c)return;MU.on=true;armar(c)}else if(!on&&MU.on){MU.on=false;if(MU.bus){const c=AC;MU.bus.gain.cancelScheduled&&MU.bus.gain.cancelScheduledValues(c.currentTime);MU.bus.gain.setTargetAtTime(0,c.currentTime,.3)}clearInterval(MU.t);cantoStop()}}
function armar(c){
 if(!MU.bus){const bus=c.createGain();bus.gain.value=0;bus.connect(c.destination);
  const d=c.createDelay(1);d.delayTime.value=.42;const fb=c.createGain();fb.gain.value=.36;const lp=c.createBiquadFilter();lp.type='lowpass';lp.frequency.value=2000;const wet=c.createGain();wet.gain.value=.5;
  bus.connect(d);d.connect(lp);lp.connect(fb);fb.connect(d);lp.connect(wet);wet.connect(c.destination);
  const nz=c.createBufferSource();nz.buffer=ruido(c,3);nz.loop=true;const nf=c.createBiquadFilter();nf.type='bandpass';nf.frequency.value=500;nf.Q.value=.6;const ng=c.createGain();ng.gain.value=.02;nz.connect(nf);nf.connect(ng);ng.connect(bus);nz.start();
  const lfo=c.createOscillator();lfo.frequency.value=.12;const lg=c.createGain();lg.gain.value=.012;lfo.connect(lg);lg.connect(ng.gain);lfo.start();
  MU.bus=bus;MU.ng=ng;MU.nf=nf;MU.t0=c.currentTime;MU.next={pad:c.currentTime+.2,mel:c.currentTime+2,bird:c.currentTime+4,amb:c.currentTime+1};MU.ci=0}
 MU.bus.gain.cancelScheduledValues&&MU.bus.gain.cancelScheduledValues(c.currentTime);MU.bus.gain.setTargetAtTime(.55,c.currentTime,1.2);
 clearInterval(MU.t);MU.t=setInterval(tick,300);ambiente(MU.amb)}
function env(c,g,t,a,d,v){g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(v,t+a);g.gain.exponentialRampToValueAtTime(.0001,t+a+d)}
function nota(c,f,t,a,d,v,tipo,out){const o=c.createOscillator(),g=c.createGain();o.type=tipo||'triangle';o.frequency.value=f;env(c,g,t,a,d,v);o.connect(g);g.connect(out||MU.bus);o.start(t);o.stop(t+a+d+.1)}
function chirp(c,k,t,vol){const p=c.createStereoPanner?c.createStereoPanner():null;if(p)p.pan.value=Math.random()*1.6-.8;const out=p||MU.bus;if(p)p.connect(MU.bus);
 const g=(f0,f1,t0,d,v)=>{const o=c.createOscillator(),ga=c.createGain();o.type='sine';o.frequency.setValueAtTime(f0,t0);o.frequency.exponentialRampToValueAtTime(f1,t0+d);env(c,ga,t0,d*.25,d*.75,v);o.connect(ga);ga.connect(out);o.start(t0);o.stop(t0+d+.05)};
 const b=2200+Math.random()*1800,v=vol||.04;
 if(k===0){g(b,b*1.5,t,.28,v)}
 else if(k===1){const n=5+Math.floor(Math.random()*5);for(let i=0;i<n;i++)g(b,b*.9,t+i*.055,.04,v*.8)}
 else if(k===2){g(b*.7,b*.55,t,.18,v);g(b*.7,b*.55,t+.26,.18,v)}
 else if(k===3){g(b*.8,b*1.3,t,.1,v);g(b*.9,b*1.5,t+.16,.1,v);g(b,b*.8,t+.34,.16,v)}
 else{for(let i=0;i<3;i++)g(b*(1+i*.12),b*(1.2+i*.12),t+i*.14,.09,v)}}
function grillo(c,t){const o=c.createOscillator(),g=c.createGain(),m=c.createOscillator(),mg=c.createGain();o.frequency.value=4300;m.frequency.value=22;mg.gain.value=.5;g.gain.value=0;m.connect(mg);mg.connect(g.gain);const e=c.createGain();e.gain.setValueAtTime(.0001,t);e.gain.exponentialRampToValueAtTime(.012,t+.2);e.gain.exponentialRampToValueAtTime(.0001,t+1.4);o.connect(g);g.connect(e);e.connect(MU.bus);o.start(t);m.start(t);o.stop(t+1.5);m.stop(t+1.5)}
function rafaga(c,t,d,f,v,tp){const s=c.createBufferSource();s.buffer=MU.nb||(MU.nb=ruido(c,2));const fl=c.createBiquadFilter();fl.type=tp||'highpass';fl.frequency.value=f;const g=c.createGain();g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.0001,t+d);s.connect(fl);fl.connect(g);g.connect(MU.bus);s.start(t,Math.random());s.stop(t+d+.05)}
function ambiente(w){MU.amb=w;if(!MU.ng||!AC)return;const c=AC,t=c.currentTime,P={day:[.02,500],dawn:[.018,500],dusk:[.02,420],night:[.012,300],rain:[.05,1400],storm:[.08,900],wind:[.07,700],fog:[.012,350],heat:[.015,600],frost:[.03,800],fire:[.03,1000]}[w]||[.02,500];MU.ng.gain.setTargetAtTime(P[0],t,1.5);MU.nf.frequency.setTargetAtTime(P[1],t,1.5)}
function tick(){if(!MU.on||!AC||AC.state!=='running')return;const c=AC,now=c.currentTime,N=MU.next,w=MU.amb;
 while(N.pad<now+1.5){const ch=PAD[MU.ci++%4];ch.forEach((m,i)=>{nota(c,mf(m+(i>0?12:0)),N.pad+i*.07,2.4,5.2,.05,'triangle')});N.pad+=7.6}
 while(N.mel<now+1.2){if(Math.random()<(w==='storm'?.3:.62)){const m=PEN[Math.floor(Math.random()*PEN.length)];nota(c,mf(m),N.mel,.012,1.6,.05,'triangle')}N.mel+=.7+Math.random()*1.5}
 while(N.bird<now+1.2){const day=w!=='night';if(day&&w!=='storm'&&w!=='fire'){chirp(c,Math.floor(Math.random()*5),N.bird,w==='rain'?.02:.04)}else if(w==='night'){if(Math.random()<.5)grillo(c,N.bird);else{const o=c.createOscillator(),g=c.createGain();o.frequency.setValueAtTime(380,N.bird);o.frequency.exponentialRampToValueAtTime(320,N.bird+.5);env(c,g,N.bird,.12,.5,.05);o.connect(g);g.connect(MU.bus);o.start(N.bird);o.stop(N.bird+.7)}}
  N.bird+=(w==='dawn'?1.4:3)+Math.random()*(w==='dawn'?2.5:6)}
 while(N.amb<now+1.2){if(w==='rain'||w==='storm'){rafaga(c,N.amb,.04,4500,.03);N.amb+=.05+Math.random()*.1;if(w==='storm'&&Math.random()<.012)rafaga(c,N.amb,2.2,120,.28,'lowpass')}else if(w==='fire'){rafaga(c,N.amb,.05,2500,.05);N.amb+=.08+Math.random()*.35}else N.amb+=.5}
}
document.addEventListener('visibilitychange',()=>{if(!AC)return;if(document.hidden)AC.suspend();else if(MU.on||SND)AC.resume()});
/* cantos reales: xeno-canto (mismos metadatos que el sitio) */
let _ca=null,_cp=false;
function cargarCantos(cb){if(typeof CANTOS!=='undefined'){cb&&cb();return}if(_cp)return;_cp=true;try{const s=document.createElement('script');s.src='/assets/cantos.js';s.onload=()=>cb&&cb();s.onerror=()=>{};document.body.appendChild(s)}catch(e){}}
function cantoDe(i){return(typeof CANTOS!=='undefined')?CANTOS[SP[i][2]]:null}
function duck(on){if(MU.bus&&AC)MU.bus.gain.setTargetAtTime(on?.15:.55,AC.currentTime,.4)}
function cantoStop(){if(_ca){try{_ca.pause()}catch(e){}_ca=null}duck(false)}
function cantoReal(i){if(!SND||window.SIMULA)return;const ct=cantoDe(i);if(!ct)return;cantoStop();const au=new Audio('https://xeno-canto.org/'+ct.xc+'/download');au.volume=.9;_ca=au;duck(true);au.play().catch(()=>{cantoStop()});au.onended=()=>{if(_ca===au)cantoStop()};setTimeout(()=>{if(_ca===au)cantoStop()},15000)}
function cantoCred(i){const ct=cantoDe(i);if(!ct)return '';return `<button class="btn md" style="background:transparent;color:#f3d77c;box-shadow:inset 0 0 0 2px #f3d77c" onclick="cantoReal(${i})">Escuchar su ${ct.tipo&&ct.tipo.startsWith('grab')?'grabación':ct.tipo||'canto'}</button><p class="cred">${ct.pais?'Grabación de '+ct.pais:'Argentina'} · ${ct.autor} · xeno-canto XC${ct.xc}</p>`}
function sndToggle(b){SND=!SND;b.textContent=SND?'Sonido: sí':'Sonido: no';if(SND)musica(true);else musica(false)}
/* efectos sueltos */
function sfx(k){if(!SND)return;const c=actx();if(!c)return;if(!MU.bus){armar(c);MU.on=true}const t=c.currentTime+.01;
 if(k==='bien'){[659,880].forEach((f,i)=>nota(c,f,t+i*.1,.01,.5,.07,'triangle'))}
 else if(k==='mal'){nota(c,196,t,.01,.45,.08,'sawtooth');nota(c,147,t+.12,.01,.5,.07,'sawtooth')}
 else if(k==='suerte'){[784,988,1175,1568].forEach((f,i)=>nota(c,f,t+i*.08,.01,.6,.06,'triangle'))}
 else if(k==='ave'){chirp(c,Math.floor(Math.random()*5),t,.06)}}
