import os
import vosk
import pyaudio
import json

# Set up the Vosk model with the correct path
vosk_model_path = "model"

if not os.path.exists(vosk_model_path):
    print("Please download the Vosk model and place it in the specified directory.")
    exit(1)

model = vosk.Model(vosk_model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

def check_microphone():
    pa = pyaudio.PyAudio()
    info = pa.get_default_input_device_info()
    if info:
        print("Micrófono activo: Sí")
    else:
        print("Micrófono activo: No")
    return pa

def recognize_and_listen(pa):
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Escuchando... (Presione Ctrl+C para detener)")

    try:
        while True:
            data = stream.read(4096, exception_on_overflow = False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '')
                if text:
                    print(f"Has dicho: {text}")
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result).get('partial', '')
                if partial_text:
                    print(f"Escuchando: {partial_text}", end='\r')
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

def main():
    pa = check_microphone()
    recognize_and_listen(pa)

if __name__ == "__main__":
    main()





