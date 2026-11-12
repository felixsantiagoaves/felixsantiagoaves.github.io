import json
def build(paths,cuts='',over=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 600 600"><defs><mask id="m"><rect x="-100" y="-100" width="800" height="800" fill="#fff"/>'+cuts+'</mask></defs><g fill="#fff" stroke="none" mask="url(#m)">'+paths+'</g>'+over+'</svg>')
def L(d,w=9):return f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def cut(d,w=4):return f'<path d="{d}" fill="none" stroke="#000" stroke-width="{w*2.2:.1f}" stroke-linecap="round"/>'
def hole(x,y,r):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#000"/>'
def mir(d):  # mirror path over y=300 (only simple M/L/C/Z uppercase commands)
    import re
    toks=re.findall(r'[MLCZ]|-?\d+\.?\d*',d);o=[];i=0;n=0
    for t in toks:
        if t in 'MLCZ':o.append(t);n=0
        else:
            v=float(t)
            o.append(str(600-v if n%2==1 else v));n+=1
    return ' '.join(o)
def wings(up):  # upper wing path (top view) + mirrored
    return f'<path d="{up}"/><path d="{mir(up)}"/>'
S={}
# ---- aerial, top view, facing right ----
def body(x0=150,x1=430,w=20,headr=13,bill=None,tailp=''):
    b=f'<path d="M{x0} 298 C{x0+60} {300-w} {x1-100} {300-w} {x1-30} 294 C{x1-8} 294 {x1} 300 {x1} 300 C{x1} 300 {x1-8} 306 {x1-30} 306 C{x1-100} {300+w} {x0+60} {300+w} {x0} 302Z"/><circle cx="{x1}" cy="300" r="{headr}"/>'
    return b+(bill or '')+tailp
S['vencejo']=build(wings('M360 292 C335 215 250 120 95 50 C150 130 190 200 238 292Z')+body(150,425,22,16,'<path d="M434 297 L452 300 L434 303Z"/>','<path d="M165 296 L95 276 L132 300 L95 324 L165 304Z"/>'),cut('M425 296 L428 296',3))
S['golondrina']=build(wings('M355 292 C335 210 285 120 205 55 C190 140 205 215 245 292Z')+body(185,425,22,17,'<path d="M436 296 L456 300 L436 304Z"/>','<path d="M195 295 L50 258 L72 270 L60 285 L128 298 L60 315 L72 330 L50 342 L195 305Z"/>'),hole(430,296,3))
S['gaviota']=build(wings('M352 288 C335 220 300 130 245 62 L205 66 C206 90 214 110 224 130 L190 120 C196 160 214 200 242 252 L232 258 C248 276 252 286 250 292Z')+body(185,420,26,22,'<path d="M436 292 L478 297 C484 300 482 306 476 306 L436 310Z"/>','<path d="M200 292 L148 285 L138 300 L148 315 L200 308Z"/>'),hole(424,292,4)+cut('M222 130 L246 150 M205 98 L238 112',3))
S['albatros']=build(wings('M345 292 C335 200 322 120 285 22 C270 22 262 24 258 28 C268 120 268 200 268 292Z')+body(165,425,28,24,'<path d="M440 288 L508 292 C518 296 516 308 504 308 L440 312Z"/>','<path d="M180 288 L140 282 L128 300 L140 318 L180 312Z"/>'),hole(430,292,4)+cut('M444 300 L505 298',3))
S['petrel']=build(wings('M352 292 C320 225 250 150 160 82 C150 100 175 120 195 138 C170 130 150 132 130 138 C190 190 215 240 245 292Z')+body(190,418,22,18,'<path d="M430 294 L465 298 C470 300 468 306 462 306 L430 306Z"/>','<path d="M205 294 L160 286 L150 300 L160 314 L205 306Z"/>'),hole(422,294,3))
S['fragata']=build(wings('M358 292 L318 172 L110 52 L205 150 L170 160 L255 205 L250 292Z')+body(200,415,20,16,'<path d="M426 293 L470 296 C480 298 480 306 470 305 L430 304Z"/>','<path d="M215 296 L38 244 L72 272 L132 292 L52 322 L38 352 L215 304Z"/>'),hole(420,296,3))
# ---- standing / swimming ----
S['pinguino']=build('<path d="M300 160 C250 200 226 300 230 400 C234 470 262 512 300 522 C345 512 372 470 376 400 C380 300 356 200 322 160Z"/><circle cx="316" cy="122" r="46"/><path d="M350 112 L412 126 C416 130 414 136 408 138 L352 142Z"/><path d="M238 255 C195 300 188 372 204 424 C226 384 246 332 254 288Z"/><path d="M232 470 L214 524 L264 506Z"/><ellipse cx="268" cy="530" rx="34" ry="11"/><ellipse cx="340" cy="530" rx="34" ry="11"/>',cut('M262 205 C250 290 254 390 268 480',5)+hole(334,112,6)+cut('M356 145 C340 168 318 172 300 168',3))
S['flamenco']=build('<path d="M110 305 C115 255 190 235 270 250 C320 258 345 285 350 310 C352 350 310 395 240 398 C170 398 118 365 110 305Z"/><path d="M345 300 C395 270 425 205 372 158 C340 130 350 95 385 92 C398 92 408 96 412 108 C395 108 392 120 400 132 C425 160 430 230 380 290 C368 308 352 320 340 322Z"/><circle cx="388" cy="98" r="22"/><path d="M398 84 C436 82 456 100 450 134 C446 118 430 108 402 112Z"/><path d="M132 292 L90 305 L128 322Z"/>'+L('M255 392 L252 540',9)+L('M290 392 L300 458 L330 428 L338 480',9),cut('M160 305 C220 345 305 345 340 300',4)+hole(392,98,5))
S['maca']=build('<path d="M105 412 C112 350 210 332 295 340 C345 344 366 330 372 296 C378 255 366 228 376 196 C382 170 395 152 420 152 L482 162 C470 168 440 172 418 176 C412 196 414 222 416 252 C420 305 410 352 398 388 C380 424 330 442 250 442 C170 442 112 436 105 412Z"/><path d="M372 160 C380 140 396 130 410 138 C400 142 398 152 396 160Z"/>'+L('M70 468 Q120 450 180 468 T300 468 T420 468 T540 468',10),hole(406,166,5)+cut('M120 405 C200 425 320 425 385 395',4))
S['ciguena']=build('<path d="M100 340 C108 280 190 265 270 270 C330 274 360 292 362 322 C360 372 310 400 240 402 C170 402 98 390 100 340Z"/><path d="M345 310 C395 275 395 205 372 160 L412 140 C420 190 424 270 380 322Z"/><circle cx="392" cy="130" r="27"/><path d="M410 118 L548 156 C552 160 550 164 545 164 L412 148Z"/><path d="M110 330 L60 392 L122 380Z"/>'+L('M258 398 L254 545',12)+L('M300 400 L308 545',12)+L('M240 548 L290 548',8)+L('M292 548 L342 548',8),cut('M150 330 C215 395 320 380 352 318',4)+hole(398,126,6))
S['cormoran']=build('<ellipse cx="285" cy="385" rx="92" ry="128" transform="rotate(18 285 385)"/><path d="M335 220 C300 250 320 300 345 300 L368 275 C350 255 350 240 362 205Z"/><circle cx="370" cy="170" r="30"/><path d="M392 156 L450 168 C462 170 462 184 450 184 L440 186 C440 176 425 175 398 188Z"/><path d="M245 480 L186 562 L238 560 L285 486Z"/>'+L('M310 498 L326 535',10)+'<path d="M300 540 L372 540 L352 530 L340 520Z"/>',cut('M246 300 C214 376 232 450 262 490',5)+hole(376,166,7)+cut('M340 340 C355 380 350 430 330 470',3))
json.dump(S,open('sil2.json','w'))
