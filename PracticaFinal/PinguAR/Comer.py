import time
import escenarios
import ReconocimientoFacial
import ReconocimientoVoz
import Atributos

primera_vez = True

def juego_comer(tiempo):
    #global llenado  # Declare llenado as global
    global primera_vez  # Declare primera_vez as global
    #global felicidad 
    
    modelo = "media/modeloSentado.glb"
    mensajeEscenario = "Escenario 2: Dale de Comer"
    mensaje1 = (f"Saciado: {Atributos.llenado}%")
    mensajeTiempo = tiempo

    bloqueo = True
    
    escenarios.clear_terminal()

    if primera_vez:
        primera_vez = False
        print("Primera Vez, cargando modelo...")
        return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo

    print(mensaje1)
    #comida = input("Presiona 'C' para darle de comer ('Q' para salir): ").upper()
    voz1 = 'COME'
    comida = ReconocimientoVoz.recognize_speech(voz1)

    if comida == voz1:
        Atributos.llenado  += 25
        if Atributos.llenado  > 100:
            Atributos.llenado  = 100
        if Atributos.llenado  == 100:
            Atributos.felicidad += 1
            Atributos.llenado = 0
            primera_vez = True
            mensaje1 = "El pinguino esta lleno!"
            modelo = "media/modeloCucu2.glb"
            print(mensaje1)
            bloqueo = False
            return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo
        
    elif comida == 'SALIR':
        print("Saliendo del juego...")
        #current_usuario = ReconocimientoFacial.usuario_status()
        primera_vez = True
        bloqueo = False
        #modelo = "media/modeloComienzo.glb"
        #mensajeEscenario = "Escenario 1: Bienvenido!"
        #mensaje1 = f"Hola {current_usuario}!"
        #mensajeTiempo = tiempo

        return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo
    else:
        print("No se ha escuchado bien, repitelo")
    
    #print(f"Llenado: {llenado}%")
    #mensaje1 = f"Llenado: {llenado}%"
    mensaje1 = (f"Llenado: {Atributos.llenado }%")
    
    return modelo, mensajeEscenario, mensaje1, mensajeTiempo, bloqueo
    
