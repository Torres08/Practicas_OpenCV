import cv2
import numpy as np
lena = cv2.imread('./media/lena.tif')

# Escalado con resize, le pasamos la imagen, el tamaño de la imagen de salida y el factor de escala
minilena = cv2.resize(lena, None, fx=0.5, fy=0.5)

cv2.imshow('LENA', minilena)
cv2.waitKey()
cv2.destroyAllWindows()