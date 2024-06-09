import subprocess
import os
import tempfile
import speech_recognition as sr
import pygame
import argparse
global args
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
args = parser.parse_args()

# Inicializar pygame para la reproducción de audio
pygame.mixer.init()

# Configuración de reconocimiento de voz
recognizer = sr.Recognizer()
mic = sr.Microphone()
os.system("cls")
def listen_to_voice():
    """Captura el audio del micrófono y lo convierte en texto"""
    with mic as source:
        print("*Se queda escuchando*")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='es-ES')
        os.system("cls")
        print(f"Has dicho: {text}")
        return text
    except sr.UnknownValueError:
        print("*No lo entiende*")
    except sr.RequestError as e:
        print(f"Error al solicitar resultados de reconocimiento; {e}")
    return ""

def speak_text_with_edge_tts(text):
    global args
    """Convierte el texto en voz utilizando Edge TTS"""
    try:
        # Crear un archivo temporal para almacenar el audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
            output_file_path = temp_audio_file.name

        # Agregar comillas alrededor del texto
        quoted_text = f'"{text}"'
        # Ejecutar el comando edge-tts para convertir el texto en audio
        command = [
            "edge-tts",
            "--rate=+15%",
            "--voice",
            args.voz,
            "--text",
            quoted_text,
            "--write-media",
            output_file_path
        ]

        subprocess.run(command, capture_output=True)

        # Reproducir el archivo de audio resultante
        if os.path.exists(output_file_path):
            try:
                play_audio(output_file_path)
                clean_text()
            except Exception as e:
                print(f"",end="")
        else:
            print("*se traba al hablar*")
    except Exception as e:
        print(f"*se hace la oidos sordos*")

# Función para reproducir audio con pygame y esperar a que termine
def play_audio(audio_file):
    # Cargar el archivo de audio
    sound = pygame.mixer.Sound(audio_file)
    # Reproducir el audio
    sound.play()
    # Esperar a que termine el audio
    while pygame.mixer.get_busy():
        time.sleep(0.1)

def clean_text():
    # Limpia el texto después de reproducir el audio
    print("Limpiando texto...")
    # Aquí puedes implementar la lógica para limpiar el texto según tus necesidades

if __name__ == "__main__":
    while True:
        message = listen_to_voice()
        if message.lower() == "salir":
            break
        speak_text_with_edge_tts(message)
