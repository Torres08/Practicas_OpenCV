import os
import VisualizarModelo
import threading
import ReconocimientoFacial
import requests
import ReconocimientoVoz
import Comer
import Cucu
import Atributos

# https://api.openweathermap.org/data/2.5/weather?q=Granada&appid=b6bda6b06d87f4ae4f869bf020508802&units=metric
BASE_URL = ""
API_KEY = 'b6bda6b06d87f4ae4f869bf020508802'
ciudad = 'Granada'

def obtener_temperatura_actual(ciudad, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric'
    response = requests.get(url)
    datos_clima = response.json()
    
    if response.status_code == 200:
        temperatura_actual = datos_clima['main']['temp']
        return temperatura_actual
    else:
        print("Error al obtener los datos del clima:", response.status_code)
        return None

def clear_terminal():
    # Limpia la terminal en Windows, macOS y Linux
    #print("/n")
    os.system('cls' if os.name == 'nt' else 'clear')   

bloqueo = False
bloqueo2 = False

def seleccionar_escenario():
    global bloqueo, bloqueo2  # Declare bloqueo as global
    
    if bloqueo == True:
        
        seleccion = 'DOS'
    
    elif bloqueo2 == True:
        seleccion = 'TRES'

    elif bloqueo == False and bloqueo2 == False:
        
        voz1 = 'UNO'
        voz2 = 'DOS'
        voz3 = 'TRES'
        seleccion = ReconocimientoVoz.recognize_speech_escenario(voz1,voz2,voz3)
        
    temperatura_actual = obtener_temperatura_actual(ciudad, API_KEY)
    #print(f"Temperatura actual en {ciudad}: {temperatura_actual} °C")
    tiempo = ciudad + " | " + str(temperatura_actual) + " *C"

    # ESCENARIO 1: te saluda, si es de noche tiene sueño (haz uso del tiempo) (por ahora cargar el modelo por defecto)
    if seleccion == 'UNO':
        current_usuario = ReconocimientoFacial.usuario_status()
        modelo = "media/modeloComienzo.glb"
        mensajeEscenario = "Escenario 1: Bienvenido!"
        mensaje1 = f"Hola {current_usuario}!"
        mensajeTiempo = tiempo

        return modelo, mensajeEscenario, mensaje1, mensajeTiempo
    
    # ESCENARIO 2: pulsa espacio para darle de comer, cuando este lleno cambia de model 
    elif seleccion == 'DOS':
        modelo = "media/modeloSentado.glb"
        mensajeEscenario = "Escenario 2: Dale de Comer"
        mensaje1 = (f"Llenado: {Atributos.llenado }%")
        mensajeTiempo = tiempo
        
        # si estoy jugando forzar la seleccion a 2 y no tocarlo 
        modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo = Comer.juego_comer(mensajeTiempo)
        
        return modelo, mensajeEscenario, mensaje1, mensajeTiempo
    
    # ESCENARIO 3: cucu, si dices cucu cambia el modelo
    elif seleccion == 'TRES':
        modelo = "media/modeloCucu.glb"
        mensajeEscenario = "Escenario 3: Donde estas?"
        mensaje1 = "Pregunta: Donde Estas?"
        mensajeTiempo = tiempo

        # si estoy jugando forzar la seleccion a 3 y no tocarlo
        modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo2 = Cucu.juego_cucu(mensajeTiempo)

        return modelo, mensajeEscenario, mensaje1, mensajeTiempo
    else:
        print("Selección inválida. Cargando escenario por defecto (1).")
        current_usuario = ReconocimientoFacial.usuario_status()
        return "media/modeloComienzo.glb", "Escenario 1", f"Hola {current_usuario}!", tiempo


def update_model(face_recognized, cameraMatrix, update_scene_callback):
    def _update():
        while True:
            if face_recognized():
                modelo_filename, mensaje , mensaje2, mensaje3 = seleccionar_escenario()
                escena = VisualizarModelo.create_scene(modelo_filename)
                camera_node = VisualizarModelo.setup_camera(escena, cameraMatrix)
                update_scene_callback(escena, camera_node, mensaje, mensaje2, mensaje3)
                #print(f"Modelo actualizado a: {modelo_filename}, Mensaje: {mensaje}")
    
    threading.Thread(target=_update, daemon=True).start()

