const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:420,height:900}});const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto('file:///home/claude/felixsantiagoaves.github.io/juego/index.html');await p.waitForTimeout(600);
await p.evaluate(()=>{window.SIMULA=1});
let mis=0,steps=0;
await p.click('.btn:has-text("Empezar")');await p.fill('#nom','Santi');await p.click('.op >> nth='+(process.argv[2]||1));
while(steps++<200){
 if(await p.$('#cv'))break;
 const st=await p.evaluate(()=>{const o=[...document.querySelectorAll('.op:not([disabled])')];if(o.length)return document.querySelector('.vig')?'mi':'op';const bt=[...document.querySelectorAll('.btn')].map(x=>x.textContent.trim());return 'btn:'+bt.join('|')});
 if(st==='mi')mis++;
 if(st==='mi'||st==='op'){const ops=await p.$$('.op:not([disabled])');await ops[Math.floor(Math.random()*ops.length)].click()}
 else{const t=st.split(':')[1];if(/Seguir|Siguiente|Cerrar|suerte/.test(t)){await p.click('.btn:has-text("Seguir"), .btn:has-text("Siguiente mes"), .btn:has-text("Cerrar el año"), .btn:has-text("Qué suerte")')}else await p.waitForTimeout(300)}
 await p.waitForTimeout(60)}
await p.waitForTimeout(2500);
console.log('mishaps',mis,'steps',steps,e,await p.evaluate(()=>G.vistas.size));
await p.screenshot({path:'fin.png',fullPage:true});require('fs').writeFileSync('cfin.png',Buffer.from((await p.evaluate(()=>document.getElementById('cv').toDataURL())).split(',')[1],'base64'));await b.close()})()
