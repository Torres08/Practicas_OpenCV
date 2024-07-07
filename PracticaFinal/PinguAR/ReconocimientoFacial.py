# https://www.youtube.com/watch?v=tl2eEBFEHqM

# opcv-python face_recognition

import os
import cv2
import face_recognition
import numpy as np
import math
import time

usuario = "Desconocido"

def usuario_status():
    global usuario
    return usuario

def face_confidence(face_distance, face_match_threshold=0.6):
    range = 1.0 - face_match_threshold
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (linear_val + (1.0 - linear_val)) * math.pow((linear_val - 0.5) * 2, 0.2) * 100
        return str(round(value, 2)) + "%"

class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    face_detected = False  # Nueva bandera para rastrear si se ha detectado una cara conocida

    def __init__(self):
        self.encoded_faces()

    def encoded_faces(self):
        media_directory = 'media/faces'
        for image in os.listdir(media_directory):
            image_path = os.path.join(media_directory, image)
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split('.')[0])

        #print(self.known_face_names)

    def run_recognition(self, frame):
        global face_recognized, usuario
        
        if not self.face_detected:  # Solo si no se ha detectado una cara conocida
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Desconocido"
                confidence = "Desconocido"

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

                    if float(confidence[:-1]) > 40:  # Si la confianza es mayor al 40%
                        print("¡Cara reconocida con confianza superior al 40%!")
                        print(f"Nombre: {name}, Confianza: {confidence}")
                        self.face_detected = True  # Establecer la bandera en True para indicar que se ha detectado una cara conocida
                        face_recognized = True  # Establecer la bandera en True para indicar que se ha reconocido una cara
                        usuario = name
                        print(f"Hola {usuario}")  # Muestra el nombre del usuario en la terminal

                self.face_names.append(f'{name} ({confidence})')

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Cambiar el color del marco a verde si se detecta una cara conocida
                frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame









