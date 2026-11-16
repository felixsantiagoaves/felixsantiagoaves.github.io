#!/usr/bin/env python3
"""Crea/actualiza miniaturas de 400 px en fotos/th/ para TODAS las fotos de fotos/*.jpg (si faltan o la foto cambió).
La web usa fotos/th/ en listas chicas (línea de tiempo, álbum, carrusel) con la función TH() de site.js. Correr tras agregar fotos."""
import os, glob
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.makedirs(os.path.join(R, 'fotos', 'th'), exist_ok=True); n = 0
for src in glob.glob(os.path.join(R, 'fotos', '*.jpg')):
    dst = os.path.join(R, 'fotos', 'th', os.path.basename(src))
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src): continue
    im = Image.open(src).convert('RGB'); im.thumbnail((400, 400)); im.save(dst, 'JPEG', quality=80, optimize=True); n += 1
print('miniaturas nuevas/actualizadas:', n)
