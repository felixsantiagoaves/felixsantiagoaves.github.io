# Arma las variantes de impresion a partir de las tiras 300 dpi.
# uso: python3 armar_pdfs.py <dir_tiras_png> <dir_salida>
import sys,glob,os
from PIL import Image,ImageDraw
H_,OUT=sys.argv[1],sys.argv[2]; os.makedirs(OUT,exist_ok=True)
mm=300/25.4
names=['portada']+[os.path.basename(f)[:-4] for f in sorted(glob.glob(H_+'/[0-9]*.png'))]
SW,SH=2480,1169  # tira 210 x 99 mm
strips=[Image.open(f'{H_}/{n}.png').convert('RGB').resize((SW,SH),Image.LANCZOS) for n in names]
def grupos(): return [strips[i:i+3] for i in range(0,len(strips),3)]
def save(pages,name): pages[0].save(f'{OUT}/{name}.pdf','PDF',resolution=300,save_all=True,append_images=pages[1:],quality=93)
def bleed(im,b):  # extiende b px replicando el borde
    w,h=im.size; o=Image.new('RGB',(w+2*b,h+2*b))
    o.paste(im,(b,b))
    o.paste(im.crop((0,0,1,h)).resize((b,h)),(0,b)); o.paste(im.crop((w-1,0,w,h)).resize((b,h)),(w+b,b))
    o.paste(o.crop((0,b,w+2*b,b+1)).resize((w+2*b,b)),(0,0)); o.paste(o.crop((0,b+h-1,w+2*b,b+h)).resize((w+2*b,b)),(0,b+h))
    return o
# 1) casa sin bordes: A4 lleno (hay que activar 'sin margenes' en la impresora)
W,H=2480,3508; pg=[]
for g in grupos():
    p=Image.new('RGB',(W,H),'white')
    for j,s in enumerate(g): p.paste(s,(0,j*SH))
    pg.append(p)
save(pg,'1-casa-sin-bordes-A4')
# 2) casa con margen 5 mm + guias de corte (reduce a 95 %)
sc=(210-10)/210; w2,h2=round(SW*sc),round(SH*sc); mx=round(5*mm); my=(H-3*h2)//2; pg=[]
for g in grupos():
    p=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(p)
    for j,s in enumerate(g): p.paste(s.resize((w2,h2),Image.LANCZOS),(mx,my+j*h2))
    t=round(4*mm)
    for j in range(len(g)+1):
        y=my+j*h2
        d.line([(0,y),(t,y)],fill='black',width=2); d.line([(W-t,y),(W,y)],fill='black',width=2)
    for x in (mx,W-mx):
        d.line([(x,my-t if my>t else 0),(x,my-4)],fill='black',width=2); d.line([(x,my+len(g)*h2+4),(x,min(H,my+len(g)*h2+t))],fill='black',width=2)
    pg.append(p)
save(pg,'2-casa-con-margen-5mm-guias-corte')
# 3) imprenta: pagina 230x317 con sangrado 3 mm y marcas de corte
b=round(3*mm); sl=round(10*mm); PW,PH=SW+2*sl,3*SH+2*sl; pg=[]
for g in grupos():
    p=Image.new('RGB',(PW,PH),'white'); d=ImageDraw.Draw(p)
    for j,s in enumerate(g):
        top=b if j==0 else 0; bot=b if j==len(g)-1 else 0
        e=bleed(s,b); e=e.crop((0,0 if top else b,e.width,e.height if bot else e.height-b))
        p.paste(e,(sl-b,sl+j*SH-top))
    x0,x1=sl,sl+SW; n=len(g); y0,y1=sl,sl+n*SH; o=b; L=round(5*mm)
    for x in (x0,x1):
        d.line([(x,y0-o-L),(x,y0-o)],fill='black',width=2); d.line([(x,y1+o),(x,y1+o+L)],fill='black',width=2)
    for k in range(n+1):
        y=sl+k*SH
        d.line([(x0-o-L,y),(x0-o,y)],fill='black',width=2); d.line([(x1+o,y),(x1+o+L,y)],fill='black',width=2)
    pg.append(p)
save(pg,'3-imprenta-A4-sangrado-marcas-de-corte')
# 4) imprenta: 13 paginas sueltas (cada tira = 1 pagina) 216x105 mm con 3 mm de sangrado
save([bleed(s,b) for s in strips],'4-imprenta-13-paginas-sangrado')
