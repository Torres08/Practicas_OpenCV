import cv2
import numpy as np
lena = cv2.imread('./media/lena.tif')
b, g, r = cv2.split(lena)
cv2.imshow('ROJO', cv2.cvtColor(r, cv2.COLOR_BAYER_BG2BGR))
cv2.imshow('VERDE', g)
cv2.imshow('AZUL', b)
cv2.waitKey()
cv2.destroyAllWindows()