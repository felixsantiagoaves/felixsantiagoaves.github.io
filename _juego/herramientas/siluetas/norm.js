const {chromium}=require('playwright');const fs=require('fs');(async()=>{const S=JSON.parse(fs.readFileSync('sil.json'));const b=await chromium.launch();const p=await b.newPage();const out={};
for(const k in S){await p.setContent(S[k].replace('<svg ','<svg id="s" '));const bb=await p.evaluate(()=>{const g=document.querySelector('#s g');const r=g.getBBox();return [r.x,r.y,r.width,r.height]});
const [x,y,w,h]=bb;const side=Math.max(w,h)*1.18;const cx=x+w/2,cy=y+h/2;let vb=[cx-side/2,cy-side/2,side,side].map(v=>v.toFixed(1)).join(' ');
out[k]=S[k].replace('viewBox="0 0 600 600"',`viewBox="${vb}"`)}
fs.writeFileSync('sil_n.json',JSON.stringify(out));
let cells='';for(const k in out){cells+=`<div style="display:inline-block;width:150px;text-align:center;font:12px sans-serif;margin:6px"><div style="background:#d8c8a0;border-radius:6px;width:150px;height:150px">${out[k].replace('<svg ','<svg style="width:150px;height:150px" ').replace('<g fill="#fff"','<g fill="#3b3a2c"').replace(/stroke="#fff"/g,'stroke="#3b3a2c"')}</div>${k}</div>`}
await p.setContent(`<body style="margin:10px;background:#ede0d4;width:1000px">${cells}</body>`);await p.screenshot({path:'sheet2.png',fullPage:true});await b.close()})()
