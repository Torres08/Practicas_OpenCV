# Ejemplo de programa openCV
# Autor: Torres Ramos, Juan Luis

# instalacion necesaria, librerias que usamos
#   pip install opencv-contrib-python
#   pip install numpy
#   pip install matplotlib

# vuelve a pulsar enter en la terminal para cerrar la ventana

import cv2
import numpy as np

# Cargar una imagen, definimos una matriz de 3x3
rgb = np.random.randint(255, size=(250, 250, 3), dtype=np.uint8)
cv2.imshow('TEST', rgb)
cv2.waitKey()
cv2.destroyWindow('TEST')