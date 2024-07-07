# Ejemplo de programa openCV: Ver un video
# Autor: Torres Ramos, Juan Luis

import cv2
import numpy as np
import time

video = cv2.VideoCapture("./media/1 Minute Timer.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
numframes = video.get(cv2.CAP_PROP_FRAME_COUNT)

if not video.isOpened():
    print("No se puede abrir el fichero")
    exit()
inicio = time.time()
while True:
    ret, frame = video.read()

    if not ret:
        print("No he podido leer el frame")
        break

    cv2.imshow('VIDEO', frame)

    if cv2.waitKey(1) == ord(' '):
        break
fin = time.time()
video.release()

print("FPS: ", fps)
print("Número de frames: ", numframes)
print("Duración: ", fin-inicio, " segundos")
print("FPS efectivos: ", numframes/(fin-inicio))


cv2.destroyWindow('VIDEO')