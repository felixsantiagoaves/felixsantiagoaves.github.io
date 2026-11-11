import os
d=os.path.dirname(os.path.abspath(__file__))
r=lambda f:open(os.path.join(d,f),encoding='utf-8').read()
out=r('head.html')+'<script>'+r('assets3.js')+'const D='+r('data2.json')+';\n'+r('compartir.js')+'\n'+r('game.js')+'</script>\n</body>\n</html>\n'
os.makedirs(os.path.join(d,'..','juego'),exist_ok=True)
open(os.path.join(d,'..','juego','index.html'),'w',encoding='utf-8').write(out)
print('juego/index.html',len(out)//1024,'KB')
