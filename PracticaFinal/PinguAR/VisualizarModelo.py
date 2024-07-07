import pyrender
import trimesh
import mathutils
import math
import numpy as np
import cv2
import datetime
import Atributos

# primero necesitamos crear una escena a la que pondremos luz ambiental blanca y un fondo negro
# cargamos modelo blg y lo adaptamos con modelo trimes y modelo mesh
# definimos pose  
# representar con py render = pose + modelo y lo añadimos a una escena

def create_scene(model_filename):
    scene = pyrender.Scene(bg_color=(0, 0, 0), ambient_light=(1.0, 1.0, 1.0))

    model_trimesh = trimesh.load(model_filename, file_type='glb')
    model_mesh = pyrender.Mesh.from_trimesh(list(model_trimesh.geometry.values()))

    # Define pose
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    mat_rot = mathutils.Matrix.Rotation(math.radians(0.0), 4, 'X')
    mat_rot2 = mathutils.Matrix.Rotation(math.radians(180.0), 4, 'Y')
    mat_sca = mathutils.Matrix.Scale(1.0, 4)
    mesh_pose = mat_loc @ mat_rot @ mat_sca @ mat_rot2

    modelo = pyrender.Node(mesh=model_mesh, matrix=mesh_pose)
    scene.add_node(modelo)

    return scene

# pasos para hacer el set up de la camapra, 
# escena de la camara
# necesitamos que el renderizado de la escena 3D se realice con las mismas caracteristicas de la webcam
# creamos una cámara intrinseca con las mismas caracteristicas que la webcam
def setup_camera(scene, camera_matrix):
    fx = camera_matrix[0][0]
    fy = camera_matrix[1][1]
    cx = camera_matrix[0][2]
    cy = camera_matrix[1][2]

    camera_intrinsics = pyrender.IntrinsicsCamera(fx, fy, cx, cy)
    camera_node = pyrender.Node(camera=camera_intrinsics)
    scene.add_node(camera_node)

    return camera_node

# sistema de corrdenadas de OPenCV es distinto al de pyrender
# dada la pose recivida del marcador rvec calculamos un vector de translacion tvec y un vector rotacion rvec
def from_opencv_to_pyrender(rvec, tvec):
    pose = np.eye(4)
    pose[0:3, 3] = tvec.T
    pose[0:3, 0:3] = cv2.Rodrigues(rvec)[0]
    pose[[1, 2]] *= -1
    pose = np.linalg.inv(pose)
    return pose


# renderizamos la escena y la imagen de la webcam
# ofrece la imagen en color RGB resultado del render asi como una matriz de profundidad que indica, lpara cada
# pixel la distancia en que se encuentra la camara, 
def realidad_mixta(renderizador, frame, escena):
    color, m = renderizador.render(escena)
    bgr = cv2.cvtColor(color, cv2.COLOR_RGB2BGR)

    _, m = cv2.threshold(m, 0, 1, cv2.THRESH_BINARY)
    m = (m*255).astype(np.uint8)
    m = np.stack((m, m, m), axis=2)

    inversa = cv2.bitwise_not(m)
    pp = cv2.bitwise_and(bgr, m)
    fondo = cv2.bitwise_and(frame, inversa)
    res = cv2.bitwise_or(fondo, pp)
    return res

# detecta aruco en la imagen de la webcam
# cada frame caputrado por la webcam en el que hayamos detectado el marcador adecuado    
def detectar_pose(frame, id_marcador, tam, cameraMatrix, distCoeffs, mensaje, mensaje2, mensaje3):
    diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    detector = cv2.aruco.ArucoDetector(diccionario)
    global felicidad

    bboxs, ids, rechazados = detector.detectMarkers(frame)
    if ids is not None:
        #print("Buscando Marcador ... ".format(id_marcador))
        for i in range(len(ids)):
            if ids[i] == id_marcador:
                obj_points = np.array([[-tam/2.0, tam/2.0, 0.0],
                                       [tam/2.0, tam/2.0, 0.0],
                                       [tam/2.0, -tam/2.0, 0.0],
                                       [-tam/2.0, -tam/2.0, 0.0]])
                ret, rvec, tvec = cv2.solvePnP(obj_points, bboxs[i], cameraMatrix, distCoeffs)
                if ret:
                    
                    for marker in bboxs:
                        cv2.polylines(frame, [np.int32(marker)], True, (0, 255, 255), thickness=2)


                    x = int(bboxs[i][i][0][0])
                    y = int(bboxs[i][0][0][1] - 10)
                    org = (x, y)  

                    #message = "ID: {}".format(ids[i])
                    #message = "Escenario 1" 

                    # mensaje1 = Escenario
                    # mensaje2 = Pista, datos
                    # mensaje3 = Tiempo
                    # mensaje4 = Hora
                    mensajeFelicidad = f"Felicidad: {Atributos.felicidad}"

                    cv2.putText(frame, mensaje3, org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)                                                       

                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
                    cv2.putText(frame, hora_actual + " | " + fecha_actual, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    cv2.putText(frame, mensajeFelicidad, (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    cv2.putText(frame, mensaje2, (x, y - 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 80, 0), 2)

                    cv2.putText(frame, mensaje, (x, y - 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    return True, rvec, tvec

    # Mensaje de depuración si el marcador no se detecta
    # print("Marcador {} no detectado.".format(id_marcador))
    return False, None, None


def mostrar_modelo(frame, escena, renderizador, camera_node, cameraMatrix, distCoeffs, mensaje, mensaje2, mensaje3,id):
    # aqui se le pasa el mensaje 
    ret, rvec, tvec = detectar_pose(frame, id, 0.19, cameraMatrix, distCoeffs, mensaje, mensaje2, mensaje3)
    if ret:
        pose_camara = from_opencv_to_pyrender(rvec, tvec)
        escena.set_pose(camera_node, pose_camara)
        frame = realidad_mixta(renderizador, frame, escena)
    return frame

