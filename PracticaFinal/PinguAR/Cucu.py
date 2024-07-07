import os
import vosk
import pyaudio
import json
import time
import escenarios
import ReconocimientoFacial
import ReconocimientoVoz
import Atributos

bloqueo2 = True
primera_vez = True

def juego_cucu(tiempo):
    global primera_vez  # Declare primera_vez as global
    #global felicidad
    
    modelo = "media/modeloCucu.glb"
    mensajeEscenario = "Escenario 3: Donde estas?"
    mensaje1 = "Pregunta: Donde Estas?"
    mensajeTiempo = tiempo

    bloqueo2 = True
    
    escenarios.clear_terminal()

    if primera_vez:
        primera_vez = False
        return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo2  

    voz1 = 'DÓNDE ESTÁS'
    cucu = ReconocimientoVoz.recognize_speech(voz1)

    if cucu == 'DÓNDE ESTÁS' or cucu == 'DÓNDE ESTÁ':
        primera_vez = True
        Atributos.felicidad += 1
        mensaje1 = "Aqui estoy!"
        modelo = "media/modeloCucu2.glb"
        print(mensaje1)
        bloqueo2 = False
        return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo2
    elif cucu == 'SALIR':
        print("Saliendo del juego...")
        #current_usuario = ReconocimientoFacial.usuario_status()
        primera_vez = True
        bloqueo2 = False
        #modelo = "media/modeloComienzo.glb"
        #mensajeEscenario = "Escenario 1: Bienvenido!"
        #mensaje1 = f"Hola {current_usuario}!"
        #mensajeTiempo = tiempo

        return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo2
        
    else:
        print("No se ha escuchado, repitelo")

    return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo2







