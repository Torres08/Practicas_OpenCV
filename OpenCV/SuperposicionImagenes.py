import cv2
import numpy as np

# Cargar la imagen de Lena y la imagen del logo de OpenCV
lena = cv2.imread('./media/lena.tif')
opencv = cv2.imread('./media/opencv.png', cv2.IMREAD_UNCHANGED)

# Establecer la imagen de fondo como Lena
bg = lena

# Obtener las dimensiones de la imagen de fondo
hbg, wbg, _ = bg.shape

# Extraer la imagen de primer plano de la imagen del logo de OpenCV
fg = opencv[:, :, 0:3]

# Obtener las dimensiones de la imagen de primer plano
hfg, wfg, _ = fg.shape

# Extraer el canal alfa de la imagen del logo de OpenCV
alfa = opencv[:, :, 3]

# Calcular el canal alfa invertido
afla = 255 - alfa

# Convertir los canales alfa y alfa invertido a formato BGR y normalizarlos
alfa = cv2.cvtColor(alfa, cv2.COLOR_GRAY2BGR) / 255
afla = cv2.cvtColor(afla, cv2.COLOR_GRAY2BGR) / 255

# Calcular la posición para colocar la imagen de primer plano en la imagen de fondo
x = wbg//2 - wfg//2
y = hbg//2 - hfg//2

# Crear una copia de la imagen de fondo
mezcla = bg

# Superponer la imagen de primer plano en la imagen de fondo utilizando mezcla alfa
mezcla[y:y+hfg, x:x+wfg] = mezcla[y:y+hfg, x:x+wfg]*afla + fg*alfa

# Mostrar la imagen resultante
cv2.imshow('MEZCLA', mezcla)
cv2.waitKey()
