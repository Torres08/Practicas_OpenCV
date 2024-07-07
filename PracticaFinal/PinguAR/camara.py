# camara.py
import numpy as np

# Parámetros intrínsecos de la cámara
fx = 600.0
fy = 600.0
cx = 320.0
cy = 240.0

# Coeficientes de distorsión
k1 = 0.0
k2 = 0.0
p1 = 0.0
p2 = 0.0
k3 = 0.0

# Parámetros intrínsecos de la cámara como matriz de NumPy
cameraMatrix = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])

# Coeficientes de distorsión como matriz de NumPy
distCoeffs = np.array([k1, k2, p1, p2, k3])

