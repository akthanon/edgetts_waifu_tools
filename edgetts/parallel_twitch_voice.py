import subprocess
import os
import tempfile
import speech_recognition as sr
import pygame
import time
import argparse  # Importar el módulo argparse

from twitchchatreader import TwitchChatReader
from twitchchatreaderevents import CommentEvent, ConnectEvent

# Inicializar pygame para la reproducción de audio
pygame.mixer.init()

# Configuración de reconocimiento de voz
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Función para reproducir audio con pygame y esperar a que termine
def play_audio(audio_file):
    # Cargar el archivo de audio
    sound = pygame.mixer.Sound(audio_file)
    # Reproducir el audio
    sound.play()
    # Esperar a que termine el audio
    #while pygame.mixer.get_busy():
        #time.sleep(0.1)

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
    """Convierte el texto en voz utilizando Edge TTS"""
    try:
        # Crear un archivo temporal para almacenar el audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            output_file_path = temp_audio_file.name

        # Agregar comillas alrededor del texto
        quoted_text = f'"{text}"'
        # Ejecutar el comando edge-tts para convertir el texto en audio
        command = [
            "edge-tts",
            "--rate=+15%",
            "--voice",
            "es-PA-MargaritaNeural",
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
                print(f"", end="")
        else:
            print("*se traba al hablar*")
    except Exception as e:
        print(f"*se hace la oidos sordos*")

if __name__ == "__main__":
    # Configurar argparse para manejar los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description="Twitch Chat Reader")
    parser.add_argument("--channel", type=str, help="Nombre del canal de Twitch")
    args = parser.parse_args()

    if args.channel:
        # Utilizar el nombre del canal proporcionado como argumento
        twitch_reader = TwitchChatReader(args.channel)

        @twitch_reader.on("comment")
        def on_comment(event: CommentEvent):
            print(event.user.name, " dice: ", event.comment)
            texto = event.user.name + " dice: " + event.comment
            speak_text_with_edge_tts(texto)

        @twitch_reader.on("connect")
        def on_connect(event: ConnectEvent):
            print("Connection established!")

        while True:
            pass  # Mantener el bucle principal funcionando para escuchar el chat de Twitch
    else:
        print("Se requiere el nombre del canal como argumento.")
