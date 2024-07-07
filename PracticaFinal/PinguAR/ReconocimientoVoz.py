import os
import vosk
import pyaudio
import json
import time
import escenarios
vosk_model_path = "model"
pa = None
recognizer = None

def initialize_vosk():
    global recognizer
    model = vosk.Model(vosk_model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

def check_microphone():
    global pa
    pa = pyaudio.PyAudio()
    info = pa.get_default_input_device_info()
    if info:
        print("Micrófono activo: Sí")
    else:
        print("Micrófono activo: No")
    return pa

def recognize_speech(mensaje1):
    global recognizer, pa
    
    if pa is None:
        print("Inicializando PyAudio...")
        check_microphone()  # Llama a check_microphone si pa no está inicializado

    if recognizer is None:
        print("Inicializando Vosk recognizer...")
        initialize_vosk()  # Llama a initialize_vosk si recognizer no está inicializado

    if recognizer is None:
        raise ValueError("Recognizer no se inicializó correctamente.")

    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

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
    print("Escuchando juego...")

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '').strip().upper()
                
                if text == mensaje1 or text == 'SALIR':
                    return text
                
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result).get('partial', '').strip().upper()
                if partial_text:
                    print(f"Escuchando: {partial_text}", end='\r')

    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    finally:
        stream.stop_stream()
        stream.close()

##

def recognize_speech_escenario(mensaje1,mensaje2,mensaje3):
    global recognizer, pa
    
    if pa is None:
        print("Inicializando PyAudio...")
        check_microphone()  # Llama a check_microphone si pa no está inicializado

    if recognizer is None:
        print("Inicializando Vosk recognizer...")
        initialize_vosk()  # Llama a initialize_vosk si recognizer no está inicializado

    if recognizer is None:
        raise ValueError("Recognizer no se inicializó correctamente.")

    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

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
    print("Escuchando Escenario...")

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '').strip().upper()
                
                if text == mensaje1 or text == 'SALIR' or text == mensaje2 and mensaje2 is not None or text == mensaje3 and mensaje3 is not None:
                    return text
                
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result).get('partial', '').strip().upper()
                if partial_text:
                    print(f"Escuchando: {partial_text}", end='\r')

    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    finally:
        stream.stop_stream()
        stream.close()
