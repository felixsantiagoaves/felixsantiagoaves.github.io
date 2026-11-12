import math,json
def rot(x,y,a,cx=0,cy=0):
    a=math.radians(a);c,s=math.cos(a),math.sin(a);x-=cx;y-=cy
    return cx+x*c-y*s, cy+x*s+y*c
def P(pts):return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+'z'
def ell(cx,cy,rx,ry,a=0):return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({a} {cx} {cy})"/>'
def beak(hx,hy,r,L,th,ang=0,droop=0,hook=0):
    # base at head front; tip at distance L, angle ang(deg, +down)
    bx,by=hx+r*.7*math.cos(math.radians(ang)),hy+r*.7*math.sin(math.radians(ang))
    a=math.radians(ang)
    tx,ty=bx+L*math.cos(a),by+L*math.sin(a)+droop
    nx,ny=-math.sin(a),math.cos(a)
    t1=(bx+nx*th,by+ny*th);t2=(bx-nx*th,by-ny*th)
    mx,my=(bx+tx)/2,(by+ty)/2+droop*.6
    d=f'M{t1[0]:.1f} {t1[1]:.1f} Q{mx+nx*th*.5:.1f} {my+ny*th*.5:.1f} {tx:.1f} {ty+hook:.1f} Q{mx-nx*th*.5:.1f} {my-ny*th*.5:.1f} {t2[0]:.1f} {t2[1]:.1f}z'
    return f'<path d="{d}"/>'
def tail(bx,by,L,w,ang,fork=0):
    a=math.radians(ang);dx,dy=math.cos(a),math.sin(a);nx,ny=-dy,dx
    tip=(bx+dx*L,by+dy*L)
    k=.75+fork*.5;pts=[(bx+nx*w*.8,by+ny*w*.8),(tip[0]+nx*w*k,tip[1]+ny*w*k),(tip[0]-dx*fork*L*.35,tip[1]-dy*fork*L*.35),(tip[0]-nx*w*k,tip[1]-ny*w*k),(bx-nx*w*.8,by-ny*w*.8)]
    return f'<path d="{P(pts)}"/>'
def legs(x,y,L,sp=14,th=10,foot=18,dx=0):
    o=''
    for s in(-1,1):
        lx=x+s*sp
        o+=f'<path d="M{lx} {y} L{lx+dx} {y+L}" stroke="#fff" stroke-width="{th}" stroke-linecap="round" fill="none"/>'
        o+=f'<path d="M{lx+dx-foot*.4} {y+L} L{lx+dx+foot} {y+L}" stroke="#fff" stroke-width="{th-1}" stroke-linecap="round" fill="none"/>'
    return o
def neck(pts,w):
    d='M'+' L'.join(f'{x} {y}' for x,y in pts) if len(pts)!=3 else f'M{pts[0][0]} {pts[0][1]} Q{pts[1][0]} {pts[1][1]} {pts[2][0]} {pts[2][1]}'
    return f'<path d="{d}" stroke="#fff" stroke-width="{w}" stroke-linecap="round" fill="none"/>'
def head(x,y,r):return f'<circle cx="{x}" cy="{y}" r="{r}"/>'
def svg(body):return f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 600 600"><g fill="#fff">{body}</g></svg>'
S={}
# perched passerine helper: body angled upright
def perch(bcx=290,bcy=330,rx=95,ry=62,ba=-30,hx=370,hy=235,hr=40,bk=(48,12,0,0,0),tl=(140,18,150,0),lg=(75,16,7,18),extra='',legy=None):
    o=ell(bcx,bcy,rx,ry,ba)+head(hx,hy,hr)+neck([(bcx+rx*.6,bcy-ry*.5),(hx-8,hy+10)],hr*1.4)
    o+=beak(hx,hy,hr,*bk)
    bx,by=rot(bcx-rx,bcy,ba,bcx,bcy)
    o+=tail(bx+10,by,tl[0],tl[1],tl[2],tl[3])
    ly=bcy+ry*.7
    o+=legs(bcx-5,ly,lg[0],lg[1],lg[2],lg[3])+extra
    return o
S['tiranido']=perch(hr=44,bk=(50,15,0,3,0),tl=(115,20,148,0),ry=60,extra='<path d="M340 205 L375 160 L395 205z"/>')
S['churrin']=perch(bcx=290,bcy=360,rx=80,ry=58,ba=-10,hx=360,hy=290,hr=36,bk=(38,9,0,0,0),tl=(110,16,-70,0),lg=(70,14,7,16))
S['fringilido']=perch(rx=90,ry=70,hr=42,bk=(34,17,0,0,0),tl=(100,16,150,0),lg=(70,16,7,16))
S['cardenal']=perch(rx=92,ry=68,hr=42,bk=(38,19,0,0,0),tl=(130,17,150,0),extra='<path d="M345 205 L330 135 L385 200z"/>')
S['zorzal']=perch(bcy=340,rx=100,ry=62,ba=-38,hx=375,hy=225,hr=38,bk=(44,10,0,0,0),tl=(125,18,148,0),lg=(95,15,7,20))
S['calandria']=perch(rx=88,ry=52,ba=-25,hx=372,hy=245,hr=34,bk=(55,9,0,6,2),tl=(200,15,160,0),lg=(80,14,6,18))
S['tordo']=perch(rx=102,ry=62,ba=-22,hx=385,hy=250,hr=40,bk=(62,16,0,0,2),tl=(165,22,158,0),lg=(80,17,8,20))
S['furnarido']=perch(bcy=340,rx=98,ry=58,ba=-18,hx=380,hy=255,hr=36,bk=(52,9,0,4,0),tl=(105,20,155,0),lg=(88,15,8,20))
# carpintero: vertical on trunk
S['carpintero']=('<rect x="120" y="40" width="60" height="520" rx="8"/>'.replace('<rect','<rect opacity="0"')+
  ell(250,320,50,100,-8)+head(262,190,38)+neck([(255,240),(262,200)],60)+beak(262,190,38,75,12,8,0)+'<path d="M232 165 L205 120 L250 152z"/>'+tail(236,405,120,20,100,0)+'<path d="M215 300 L180 320 L214 345z"/>')
# aerial
S['golondrina']=svg('') and (ell(300,310,95,24,-8)+head(395,300,30)+beak(395,300,30,22,9,10)+
  '<path d="M300 300 C250 230 190 190 100 170 C160 230 220 280 280 320z"/>'+tail(210,335,150,14,172,1.4))
S['atajacaminos']=(ell(285,330,120,50,-4)+head(405,300,48)+beak(405,300,48,24,24,12)+tail(170,335,130,36,176,0)+'<path d="M260 300 C240 240 210 210 150 200 C200 260 220 300 250 330z"/>'+legs(300,370,34,12,7,14))
# ground plump
S['inambu']=(ell(285,350,125,92,-12)+head(405,262,30)+neck([(375,300),(400,270)],40)+beak(405,262,30,40,7,18,3)+legs(285,430,60,18,8,22)+tail(170,360,45,35,165,0))
S['cracido']=(ell(280,310,115,64,-20)+head(395,225,34)+neck([(350,280),(392,235)],52)+beak(395,225,34,38,12,12,0)+tail(180,350,210,34,140,0)+legs(290,350,115,16,8,20)+'<path d="M390 195 L385 150 L412 192z"/>')
S['cuclillo']=(ell(290,310,100,34,-18)+head(385,252,34)+beak(385,252,34,52,10,6,8,4)+tail(200,345,240,15,150,0)+legs(280,330,60,12,7,16))
S['tucan']=(ell(280,340,92,70,-25)+head(360,250,42)+beak(360,250,42,190,40,-4,34,0)+tail(210,385,100,22,112,0)+legs(285,395,85,14,8,20))
S['martin']=(ell(270,370,85,60,-15)+head(350,285,52)+beak(350,285,52,150,13,2,0,0)+tail(210,405,70,24,112,0)+legs(275,420,40,12,7,14))
S['nandu']=(ell(250,360,140,88,-18)+neck([(350,300),(405,200),(425,120)],34)+head(432,112,32)+beak(432,112,32,46,11,6,2)+legs(250,430,110,26,11,34)+'<path d="M120 335 Q95 330 85 360 Q100 380 130 372z"/>')
S['pinguino']=('<path d="M300 90 C380 90 410 190 405 320 C402 420 372 505 300 520 C228 505 198 420 195 320 C190 190 220 90 300 90z"/>'+beak(330,115,40,50,9,10,2)+'<path d="M200 270 Q145 340 160 410 Q205 380 215 320z"/>'+'<ellipse cx="260" cy="535" rx="40" ry="14"/><ellipse cx="345" cy="535" rx="40" ry="14"/>')
S['albatros']=('<path d="M300 285 C220 240 120 245 25 290 C90 300 170 340 275 335z"/><path d="M300 285 C380 240 480 245 575 290 C510 300 430 340 325 335z"/>'+ell(300,315,70,26,0)+head(375,310,22)+beak(375,310,22,50,10,5,3,6)+tail(240,318,70,16,180,0))
S['flamenco']=('<path d="M268 330 C220 300 215 250 270 215" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round"/>'+ell(240,370,100,60,-8)+neck([(325,350),(380,250),(330,190)],26)+head(325,180,22)+beak(325,180,22,50,12,50,20,10)+tail(145,365,50,26,172,0)+'<path d="M255 405 L270 520 M275 405 L300 520" stroke="#fff" stroke-width="9" stroke-linecap="round"/>')
S['pelicano']=(ell(260,380,120,64,-8)+neck([(340,350),(390,300),(385,250)],44)+head(392,240,32)+beak(392,240,32,150,16,18,12,0)+'<path d="M420 262 Q480 340 420 360 Q400 330 405 275z"/>'+tail(150,385,60,30,175,0)+legs(255,430,60,22,10,30))
S['cormoran']=(ell(255,350,100,50,-35)+neck([(320,310),(350,230),(365,180)],30)+head(375,170,24)+beak(375,170,24,50,8,14,2,12)+tail(180,410,110,22,125,0)+legs(250,390,70,16,9,26)+'<path d="M210 320 Q130 300 90 350 Q150 360 215 365z"/>')
S['gallareta']=(ell(285,365,115,70,-5)+head(385,295,38)+neck([(355,330),(380,300)],50)+beak(385,295,38,38,10,5,0,0)+tail(180,330,40,28,-150,0)+legs(285,420,70,20,9,28))
S['gaviota']=('<path d="M300 300 C240 230 160 205 60 240 C130 262 200 320 275 340z"/><path d="M300 300 C360 230 440 205 540 240 C470 262 400 320 325 340z"/>'+ell(300,320,80,28,0)+head(385,308,24)+beak(385,308,24,42,9,10,2,5)+tail(225,322,65,26,178,0))
S['rapaz2']=None
del S['rapaz2']
S['vencejo']=(ell(300,300,60,18,-5)+head(360,295,18)+'<path d="M300 295 C240 200 160 140 60 110 C140 190 220 260 275 315z"/><path d="M300 295 C340 200 420 140 520 110 C440 190 360 260 330 315z"/>'+tail(250,305,100,10,170,1.2))
if __name__=='__main__':
    json.dump({k:svg(v) for k,v in S.items()},open('sil.json','w'))
    cells=''
    names=list(S)
    for i,k in enumerate(names):
        c,r=i%6,i//6
        cells+=f'<div style="display:inline-block;width:150px;text-align:center;font:12px sans-serif;margin:6px"><div style="background:#d8c8a0;border-radius:6px;width:150px;height:150px">{svg(S[k]).replace("<svg ","<svg style=\"width:150px;height:150px\" ").replace("fill=\"#fff\"","fill=\"#3b3a2c\"").replace("stroke=\"#fff\"","stroke=\"#3b3a2c\"")}</div>{k}</div>'
    open('sheet.html','w').write(f'<body style="margin:10px;background:#ede0d4;width:1000px">{cells}</body>')
