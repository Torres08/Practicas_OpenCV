import cv2
import cuia
import camara
import pyrender
import ReconocimientoFacial
import VisualizarModelo
import escenarios
from escenarios import seleccionar_escenario, update_model

face_recognized = False
# Inicialización de variables globales para la escena y el nodo de la cámara
escena = None
camera_node = None

BASE_URL = ""
API_KEY = 'b6bda6b06d87f4ae4f869bf020508802'
ciudad = 'Granada'
temperatura_actual = escenarios.obtener_temperatura_actual(ciudad, API_KEY)
tiempo = ciudad + " | " + str(temperatura_actual) + " *C"

# Inicialización de usuario
current_usuario = ReconocimientoFacial.usuario_status()

# Nombre del archivo del modelo y mensajes iniciales
modelo_filename = "media/modeloComienzo.glb"
modelo_filename2 = "media/cactus.glb"
mensaje = "Escenario 1: Bienvenido!"
mensaje2 = f"Hola {current_usuario}!"
mensaje3 = tiempo


# Función para actualizar la escena y los mensajes
def update_scene(new_escena, new_camera_node, new_mensaje, new_mensaje2, new_mensaje3):
    global escena, camera_node, mensaje, mensaje2, mensaje3
    escena = new_escena
    camera_node = new_camera_node
    mensaje = new_mensaje
    mensaje2 = new_mensaje2
    mensaje3 = new_mensaje3

if __name__ == "__main__":
    #camId = '/dev/video0'
    camId = 1 # Define el ID de la cámara que deseas usar ver id con adb devices -l

    # Verificar si la cámara se puede abrir
    cap = cv2.VideoCapture(camId)
    if not cap.isOpened():
        raise Exception(f"No se puede abrir la cámara con ID {camId}")
    cap.release()#22

    bk = cuia.bestBackend(camId)
    ar = cuia.myVideo(camId, bk)
    hframe = ar.get(cv2.CAP_PROP_FRAME_HEIGHT)
    wframe = ar.get(cv2.CAP_PROP_FRAME_WIDTH)
    mirender = pyrender.OffscreenRenderer(wframe, hframe)

    # Crear la escena con el modelo por defecto
    escena = VisualizarModelo.create_scene(modelo_filename)
    escena2 = VisualizarModelo.create_scene(modelo_filename2)

    cameraMatrix = camara.cameraMatrix
    distCoeffs = camara.distCoeffs
    camera_node = VisualizarModelo.setup_camera(escena, cameraMatrix)

    # Iniciar el hilo para actualizar el modelo
    update_model(lambda: face_recognized, cameraMatrix, update_scene)

    # Reconocimiento facial
    escenarios.clear_terminal()
    print("""
        $$$$$$$\  $$\                                $$$$$$\            
        $$  __$$\ \__|                              $$  __$$\           
        $$ |  $$ |$$\ $$$$$$$\   $$$$$$\  $$\   $$\ $$ /  $$ | $$$$$$\  
        $$$$$$$  |$$ |$$  __$$\ $$  __$$\ $$ |  $$ |$$$$$$$$ |$$  __$$\ 
        $$  ____/ $$ |$$ |  $$ |$$ /  $$ |$$ |  $$ |$$  __$$ |$$ |  \__|
        $$ |      $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |      
        $$ |      $$ |$$ |  $$ |\$$$$$$$ |\$$$$$$  |$$ |  $$ |$$ |      
        \__|      \__|\__|  \__| \____$$ | \______/ \__|  \__|\__|      
                                $$\   $$ |                              
                                \$$$$$$  |                              
                                \______/                               
        """)
    #print(f"Temperatura actual en {ciudad}: {temperatura_actual} °C")
    print("Buscando reconocimiento facial...")
    fr = ReconocimientoFacial.FaceRecognition()

    # Manejar los frames que se usan para la representación del modelo 3D + reconocimiento facial
    def process_frame(frame):
        global face_recognized, escena, camera_node, mensaje, mensaje2, mensaje3, current_usuario

        if not face_recognized:
            frame_with_faces = fr.run_recognition(frame)
            if fr.face_detected:
                face_recognized = True
                # Actualizar el usuario actual y los mensajes
                current_usuario = ReconocimientoFacial.usuario_status()
                mensaje2 = "Hola " + current_usuario 
                print("Usuario reconocido:", current_usuario)
            return frame_with_faces
        else:
            # Mostrar el modelo 3D
            frame_with_model = VisualizarModelo.mostrar_modelo(frame, escena, mirender, camera_node, cameraMatrix, distCoeffs, mensaje, mensaje2, mensaje3,1)
                        
            return frame_with_model

    ar.process = process_frame

    try:
        # Para salir pulse space
        ar.play("PinguAR", key=ord(' '))
    finally:
        ar.release()








    












