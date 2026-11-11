/* Compartir resultado: imagen PNG en 3 formatos (historia, post 4:5, cuadrado) */
const FMT={historia:{w:1080,h:1920,n:'Historia'},post:{w:1080,h:1350,n:'Post 4:5'},cuadrado:{w:1080,h:1080,n:'Cuadrado'}};
const SH={fmt:'historia',file:null,url:'felixsantiago.com.ar/juego'};
const C={papel:'#ede0d4',oliva:'#414833',tierra:'#7f5539',arena:'#c4a882',rojo:'#b23a2e',oro:'#d8b04a',ink:'#2d3322'};
const FL="Lato,'Helvetica Neue',Arial,sans-serif",FP="'Playfair Display',Georgia,serif";
const _si={};
const siluImg=k=>_si[k]||(_si[k]=new Promise(r=>{const im=new Image();im.onload=()=>r(im);im.onerror=()=>r(null);im.src=SILD[k]||SILD.pajarito}));
function tintada(im,s,col){const c=document.createElement('canvas');c.width=c.height=s;const x=c.getContext('2d');const k=Math.min(s/im.width,s/im.height),w=im.width*k,h=im.height*k;x.drawImage(im,(s-w)/2,(s-h)/2,w,h);x.globalCompositeOperation='source-in';x.fillStyle=col;x.fillRect(0,0,s,s);return c}
function rr(x,a,b,w,h,r){x.beginPath();x.moveTo(a+r,b);x.arcTo(a+w,b,a+w,b+h,r);x.arcTo(a+w,b+h,a,b+h,r);x.arcTo(a,b+h,a,b,r);x.arcTo(a,b,a+w,b,r);x.closePath()}
function lineas(x,t,mw,max){const p=t.split(' ');let l=[],c='';for(const w of p){const n=c?c+' '+w:w;if(x.measureText(n).width>mw&&c){l.push(c);c=w}else c=n}if(c)l.push(c);return l.slice(0,max)}
function tracking(x,v){try{x.letterSpacing=v+'px'}catch(e){}}
async function figuCanvas(x,i,cx,cy,w,rot){const s=SP[i],h=w*1.4,p=w*.055,pic=w-2*p,rara=s[4]<.5,mit=s[4]<.05;
 x.save();x.translate(cx,cy);x.rotate(rot*Math.PI/180);
 x.shadowColor='rgba(42,31,20,.3)';x.shadowBlur=w*.1;x.shadowOffsetY=w*.04;x.fillStyle='#fff';rr(x,-w/2,-h/2,w,h,w*.03);x.fill();x.shadowColor='transparent';
 if(rara||mit){x.lineWidth=w*.025;x.strokeStyle=mit?C.oro:C.rojo;rr(x,-w/2,-h/2,w,h,w*.03);x.stroke()}
 x.fillStyle=ZC[s.zb];x.fillRect(-w/2+p,-h/2+p,pic,pic);
 const im=await siluImg(silDe(i));if(im){x.globalAlpha=.85;const t=tintada(im,Math.round(pic*.78),'#3a4029');x.drawImage(t,-t.width/2,-h/2+p+(pic-t.width)/2);x.globalAlpha=1}
 x.textAlign='center';x.fillStyle=C.ink;let fs=w*.088;x.font=`900 ${fs}px ${FL}`;const nm=s[1].toUpperCase();let L=lineas(x,nm,w-2*p,2);
 while(L.join(' ').length<nm.length&&fs>w*.05){fs*=.92;x.font=`900 ${fs}px ${FL}`;L=lineas(x,nm,w-2*p,2)}
 const ty=-h/2+p+pic+fs*1.45;L.forEach((l,k)=>x.fillText(l,0,ty+k*fs*1.12));
 x.fillStyle=C.tierra;x.font=`700 ${w*.07}px ${FL}`;x.fillText(pc(s[4]),0,h/2-p*1.1);
 x.restore()}
async function dibujar(cv,fmt,d){const F=FMT[fmt],W=F.w,H=F.h,x=cv.getContext('2d');cv.width=W;cv.height=H;
 await Promise.all([document.fonts.load('900 40px '+FL),document.fonts.load('700 40px '+FL),document.fonts.load('italic 400 40px '+FP)]);
 x.fillStyle=C.papel;x.fillRect(0,0,W,H);
 x.strokeStyle=C.arena;x.lineWidth=4;rr(x,26,26,W-52,H-52,22);x.stroke();
 const L={historia:{lab:225,ns:390,ny:650,sub:735,st:840,hd:965,gy:990,cols:3,cw:250,gap:36,n:6,foot:1790,fs:1,tf:64},
  post:{lab:80,ns:230,ny:370,sub:425,st:505,hd:615,gy:640,cols:3,cw:195,gap:26,n:6,foot:1262,fs:.9,tf:56},
  cuadrado:{lab:85,ns:230,ny:335,sub:390,st:478,hd:580,gy:605,cols:4,cw:215,gap:20,n:4,foot:975,fs:.85,tf:46}}[fmt];
 const mid=W/2;x.textAlign='center';x.textBaseline='alphabetic';
 x.fillStyle=C.tierra;x.font='900 '+(44*L.fs)+'px '+FL;tracking(x,8);x.fillText('MI AÑO PAJARERO',mid,L.lab);tracking(x,0);
 x.font='italic 400 '+(40*L.fs)+'px '+FP;x.fillText('Doce meses por Córdoba',mid,L.lab+55*L.fs);
 // número
 const nx=mid;
 x.fillStyle=C.oliva;x.font=`900 ${L.ns}px ${FL}`;x.fillText(String(d.n),nx,L.ny);
 x.fillStyle=C.tierra;x.font=`italic 400 ${L.ns*.14}px ${FP}`;x.fillText('especies en un año',nx,L.sub);
 // sello
 const sx=mid,sy=L.st;
 x.save();x.translate(sx,sy);x.rotate(-4*Math.PI/180);const tf=L.tf;x.font=`900 ${tf}px ${FL}`;tracking(x,3);
 const tw=Math.min(x.measureText(d.titulo.toUpperCase()).width+80,W-120),th=tf*1.9;x.fillStyle=C.oliva;rr(x,-tw/2,-th/2,tw,th,10);x.fill();
 x.fillStyle=C.papel;x.textBaseline='middle';x.fillText(d.titulo.toUpperCase(),0,4);tracking(x,0);x.restore();x.textBaseline='alphabetic';
 // figuritas
 x.fillStyle=C.tierra;x.font='900 '+(32*L.fs)+'px '+FL;tracking(x,6);x.fillText(fmt==='cuadrado'?'MIS FIGURITAS MÁS DIFÍCILES':'MIS FIGURITAS MÁS DIFÍCILES',mid,L.hd);tracking(x,0);
 const top=d.top.slice(0,L.n),cw=L.cw,ch=cw*1.4,cols=L.cols,rows=Math.ceil(top.length/cols);
 for(let k=0;k<top.length;k++){const r=Math.floor(k/cols),c=k%cols,inRow=Math.min(cols,top.length-r*cols),gw=inRow*cw+(inRow-1)*L.gap;
  const cx=mid-gw/2+cw/2+c*(cw+L.gap),cy=L.gy+ch/2+r*(ch+L.gap*.8);await figuCanvas(x,top[k],cx,cy,cw,((SP[top[k]][0]*37)%7-3)*.7)}
 x.fillStyle=C.oliva;x.font='900 '+(40*L.fs)+'px '+FL;x.fillText('¿ME GANÁS?',mid,L.foot);
 x.fillStyle=C.tierra;x.font='700 '+(32*L.fs)+'px '+FL;x.fillText(SH.url,mid,L.foot+46*L.fs)}
async function elegirFmt(f,b){SH.fmt=f;SH.file=null;document.querySelectorAll('.tabs button').forEach(t=>t.classList.toggle('on',t.dataset.f===f));
 const cv=document.getElementById('cv'),bs=document.getElementById('bsh');if(bs)bs.disabled=true;
 await dibujar(cv,f,SH.d);
 cv.toBlob(bl=>{if(!bl)return;SH.file=new File([bl],'mi-anio-pajarero-'+f+'.png',{type:'image/png'});if(bs){bs.disabled=false;const cs=!!(navigator.canShare&&navigator.canShare({files:[SH.file]}));bs.textContent=cs?'Compartir':'Descargar imagen';const bd=document.getElementById('bdl');if(bd)bd.style.display=cs?'':'none'}},'image/png')}
async function compartir(){const f=SH.file;if(!f)return;
 if(navigator.canShare&&navigator.canShare({files:[f]})){try{await navigator.share({files:[f],title:'Mi año pajarero',text:SH.txt});return}catch(e){if(e&&e.name==='AbortError')return}}
 descargar()}
function descargar(){if(!SH.file)return;const a=document.createElement('a');a.href=URL.createObjectURL(SH.file);a.download=SH.file.name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1500)}
