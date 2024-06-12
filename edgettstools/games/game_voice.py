import subprocess
import os
import tempfile
import speech_recognition as sr
import pygame
import argparse
from datetime import datetime
import re
global args

# Eliminar el contenido del archivo messages.txt al iniciar el programa
with open("messages_game.txt", "w") as file:
    file.write("")

def read_messages_from_file():
    with open("messages_game.txt", "r") as file:
        return file.readlines()

def save_messages_to_file(messages):
    with open("messages_game.txt", "w") as file:
        file.writelines(messages)

class MessageLogger:
    def __init__(self, filename, max_messages=10):
        self.filename = filename
        self.max_messages = max_messages
        self.messages = []

    def log(self, message):
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)
        self.messages.append("NO RESPONDAS ESTE MENSAJE PERO SIGUE LAS INSTRUCCIONES "+datetime.now().strftime("[%H:%M:%S]")+": ["+message+"]")
        self.write_to_file()

    def write_to_file(self):
        with open(self.filename, 'w') as file:
            for message in self.messages:
                file.write(message + '\n')

# Crear una instancia de MessageLogger
logger = MessageLogger("messages_game.txt")

parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
args = parser.parse_args()

# Inicializar pygame para la reproducción de audio
pygame.mixer.init()

# Configuración de reconocimiento de voz
recognizer = sr.Recognizer()
mic = sr.Microphone()
#os.system("cls")


def normalize_phonetics(word):
    phonetic_map = {
        'v': 'b', 'b': 'b', 
        'c': 'k', 'k': 'k', 'q': 'k', 
        'z': 's', 's': 's', 'x': 's', 'ch': 'sh', 'sh': 'sh',  
        'y': 'y', 'i': 'y', 
        'g': 'j', 'j': 'j',  # General, jeneral
        'r': 'r',  # Carro, caro
        'm': 'b','á': 'a','é': 'e','í': 'y','ó': 'o','ú': 'u'  # PULIDAS
    }
    
    normalized_word = ""
    i = 0
    while i < len(word):
        if i < len(word) - 1 and word[i:i+2] in phonetic_map:  # Check for two-letter mappings
            normalized_word += phonetic_map[word[i:i+2]]
            i += 2
        else:
            normalized_word += phonetic_map.get(word[i], word[i])  # Default to the same letter if not found
            i += 1
    return normalized_word


nombre_strem="kali"
global running_repl
running_repl=True
def listen_to_voice():
    """Captura el audio del micrófono y lo convierte en texto"""
    global running_repl, estado_voz  # Asegurarse de usar la variable global
    print("*Se queda escuchando*")
    while running_repl:
        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=5)  # Añadir timeout
                print("*Escuchado*")
            except sr.WaitTimeoutError:
                #print("*Tiempo de espera excedido, reintentando...*")
                continue  # Volver al comienzo del bucle si se excede el tiempo de espera
        try:
            text = recognizer.recognize_google(audio, language='es-ES')  
            print(f"Has dicho: {text}")
            # Verificar si el texto contiene la palabra clave
            normalized_text = normalize_phonetics(text.lower())
            normalized_keyword = normalize_phonetics(nombre_strem.lower())
            
            if re.search(rf'\b{normalized_keyword}\b', normalized_text):
                # Extraer el texto después de la palabra clave
                keyword_index = normalized_text.index(normalized_keyword)
                # Añadir la longitud de la palabra clave para saltar la palabra y el espacio después de ella
                command = text[keyword_index + len(nombre_strem):].strip()
                #print(f"Comando: {Command}")
                logger.log(f"{command}")
                print(f"Comando recibido: {command}")
                return command
            else:
                print("*Se queda escuchando*")
        except sr.UnknownValueError:
            print("*No lo entiende*")
        except sr.RequestError as e:
            print(f"Error al solicitar resultados de reconocimiento; {e}")

    print("El programa ha sido detenido.")

if __name__ == "__main__":
    while True:
        message = listen_to_voice()
        if message.lower() == "salir":
            break
