# Ejemplo de programa openCV: Leer parte alfa imagen
# Autor: Torres Ramos, Juan Luis

# alpha = opacidad de la imagen, 1: opaco, 0: transparente

import cv2
import numpy as np
opencv = cv2.imread('./media/opencv.png', cv2.IMREAD_UNCHANGED)
opencv_bgr = opencv[:, :, 0:3]
opencv_alfa = opencv[:, :, 3] 
cv2.imshow('COLOR', opencv_bgr)
cv2.imshow('ALFA', opencv_alfa) # alfa es el resultado blanco
cv2.waitKey()
cv2.destroyAllWindows()  