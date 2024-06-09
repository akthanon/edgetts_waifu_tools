import subprocess
import os
import tempfile
from pathlib import Path
import speech_recognition as sr
import importlib.metadata
import io
import sys
from collections import namedtuple
from typing_extensions import Annotated
import typer
from gpt4all import GPT4All
import random
import time
import pygame
import re
import wave
import numpy as np
import threading
from pydub import AudioSegment
import shutil
import argparse

global args
# Configuración de argparse
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--png', type=str, default='Caly the Cattrap', help='Name of the PNGtuber')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
parser.add_argument('--perso', type=str, default='waifu', help='Nombre del archivo de sistema de inicio')
args = parser.parse_args()

# Ruta de las imágenes y el audio
default_pngtuber_name = "Caly the Cattrap"
base_dir = "PNGtubers"
pngtuber_name = args.png

# Crear la ruta completa del directorio del PNGtuber
pngtuber_path = os.path.join(base_dir, pngtuber_name)
print(pngtuber_path)
# Verificar si el directorio especificado existe
if not os.path.exists(pngtuber_path):
    print(f"El directorio '{pngtuber_path}' no existe. Usando el nombre predeterminado '{default_pngtuber_name}'.")

    # Crear la ruta completa del directorio predeterminado
    default_pngtuber_path = os.path.join(base_dir, default_pngtuber_name)

    # Verificar si el directorio predeterminado existe
    if not os.path.exists(default_pngtuber_path):
        print(f"Error: El directorio predeterminado '{default_pngtuber_path}' tampoco existe. Cerrando el programa.")
        sys.exit(1)
    else:
        pngtuber_path = default_pngtuber_path

# Configuración de reconocimiento de voz
recognizer = sr.Recognizer()
mic = sr.Microphone()

#Variables
running_repl = True
global global_audio_path
global current_time_ms
global_audio_path = ""

# Inicializar pygame para la reproducción de audio
pygame.mixer.init()

# Configuración de pygame
pygame.init()

# Dimensiones de la ventana
screen_width = 720*2
screen_height = 405*2
screen = pygame.display.set_mode((screen_width, screen_height))

# Título de la ventana
pygame.display.set_caption(f"{pngtuber_name} PNGtuber")

# Colores
color_screen = (125, 125, 200)

# Ruta de las imágenes y el audio
global emotions, emotions_similar

emotions_similar = {
    "Aburrida": ["Aburrido", "Desinteresada", "Desinteresado", "Cansada", "Cansado", "Indiferente"],
    "Emocionada": ["Emocionado", "Entusiasmada", "Entusiasmado", "Animada", "Animado"],
    "Enojada": ["Enojado", "Furiosa", "Furioso", "Molesta", "Molesto", "Irritada", "Irritado"],
    "Llorando": ["Llorando", "Sollozando", "Lagrimando", "Desconsolada", "Desconsolado","Triste"],
    "Nerviosa": ["Nervioso", "Alterada", "Alterado", "Ansiosa", "Ansioso", "Preocupada", "Preocupado", "Tensa", "Tenso"],
    "Neutral": ["Neutro", "Indiferente", "Despreocupada", "Despreocupado"],
    "Pensativa": ["Pensativo", "Reflexiva", "Reflexivo", "Meditativa", "Meditativo", "Considerativa", "Considerativo","Seria","Serio","Mili"],
    "Riendo": ["Riendo", "Sonriendo", "Carcajeando", "Divertida", "Divertido"],
    "Sorprendida": ["Sorprendido", "Asombrada", "Asombrado", "Impactada", "Impactado","Espantada","Espantado"],
    "Vengativa": ["Exitada", "Vengativo", "Exitado", "Venganza", "Ira"],
}


emotions = ["Aburrida", "Emocionada", "Enojada", "Llorando", "Nerviosa", "Neutral", "Pensativa", "Riendo", "Sorprendida", "Vengativa"]
audio_path = os.path.join("audios", "sonido2.wav")


def find_similar_emotion(emotion):
    for key, similar_emotions in emotions_similar.items():
        if emotion == key or emotion in similar_emotions:
            return key
    return None


# Función para redimensionar imágenes manteniendo la relación de aspecto
def scale_image(image, target_width, target_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height

    if target_width / target_height > aspect_ratio:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

    return pygame.transform.scale(image, (new_width, new_height))

# Cargar y redimensionar imágenes de emociones
images = {}
for emotion in emotions:
    images[emotion] = []
    for i in range(4):
        img_path = os.path.join(pngtuber_path, f"{emotion}", f"{i}.png")
        img = pygame.image.load(img_path).convert_alpha()
        img = scale_image(img, screen_width, screen_height)
        images[emotion].append(img)

# Función para obtener amplitud del fragmento de audio
def get_fragment_amplitude(sound, segundo):
    # Abre el archivo WAV
    estado="iniciado"
    with wave.open(sound, 'rb') as archivo:
        # Obtiene la información del audio
        frecuencia_muestreo = archivo.getframerate()
        duracion = archivo.getnframes() / float(frecuencia_muestreo)
        
        # Calcula el número de frames en el segundo especificado
        frames_por_segundo = frecuencia_muestreo
        frames_desde_el_principio = int(frames_por_segundo * segundo)
        
        # Asegurarse de que la posición no exceda la duración total
        frames_desde_el_principio = min(frames_desde_el_principio, int(duracion * frames_por_segundo))
        
        # Establece la posición del puntero en el segundo especificado
        archivo.setpos(frames_desde_el_principio)
        
        # Lee los frames para ese segundo
        frames = archivo.readframes(frames_por_segundo)
        
        # Decodifica los frames a un arreglo de numpy
        arreglo = np.frombuffer(frames, dtype=np.int16)
        
        # Verificar si el arreglo está vacío o contiene valores no válidos
        if arreglo.size == 0 or not np.isfinite(arreglo).all():
            return 0  # Devolver cero en caso de que no haya datos válidos
        
        # Calcula la amplitud promedio
        amplitud_promedio = np.abs(arreglo).mean()
        tiempo_actual = archivo.tell() / float(frecuencia_muestreo)
        if tiempo_actual >= duracion:
            estado="finalizado"
        return amplitud_promedio, estado


# Función principal del PNGtuber
def pngtuber():
    global global_audio_path, estado_voz
    global current_time_ms, emotions_list, emotions
    current_time_ms = -1
    running = True
    current_emotion = "Pensativa"
    current_frame = 0
    next_blink_time = time.time() + random.randint(3, 6)
    is_blinking = False
    blink_start_time = 0
    blink_duration = 0.1

    mp3_input_file = os.path.join("audios", "sonido3.mp3")
    framon = 0.02
    timey = 0
    amplitude_sine = 20
    frequency_sine = 0.2
    vertical_position = screen_height // 2
    amplitude = 0
    estado = "finalizado"
    audio_path = ""
    old_sound = ""
    audio_mp3 = "salida_temporal.mp3"
    duration = 0
    terminado = []
    time_blinking = 0.5
    stepts_time = 1

    speak_duration = 0.2
    is_speaking = True
    next_speak_time = 0
    amplitude_threshold = 1000
    # Inicializar pygame
    pygame.init()

    # Crear pantalla
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PngTuber")

    # Definir colores
    #color_screen = (255, 255, 255)
    colores_bolita = {
        0: (0, 255, 0),  # Verde
        1: (0, 0, 255),  # Azul
        2: (255, 255, 0),  # Amarillo
        3: (255, 0, 0)   # Rojo
    }

    # Variable para almacenar la última lista de emociones procesada
    last_emotions_list = None
    sound_init = False
    sound_initialized = False  # Bandera para controlar la inicialización del sonido

    estado_voz = 3

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not is_blinking and time.time() >= next_blink_time:
            is_blinking = True
            blink_start_time = time.time()
            current_frame = 1

        if is_blinking and time.time() >= blink_start_time + blink_duration:
            is_blinking = False
            next_blink_time = time.time() + random.randint(1, 4)
            current_frame = 0

        try:
            if os.path.exists(audio_mp3):
                if sound_init and not sound_initialized:
                    sound = AudioSegment.from_mp3(audio_mp3)
                    audio_path = audio_mp3.replace(".mp3", ".wav")
                    sound.export(audio_path, format="wav")
                    sound = pygame.mixer.Sound(audio_mp3)
                    duration = sound.get_length() * 1000
                    amplitude, estado = get_fragment_amplitude(audio_path, 0)
                    amplitude = 0
                    current_frame = 0
                    sound_initialized = True  # Marcar que el sonido ha sido inicializado
                elif current_time_ms > 0 and current_time_ms < duration:
                    amplitude, estado = get_fragment_amplitude(audio_path, current_time_ms / 1000)
                    old_sound = global_audio_path
            if current_time_ms + 20 >= duration:
                amplitude = 0
                current_frame = 0
                duration = 0
        except:
            pass

        if pygame.mixer.music.get_busy():
            sound_init = True
        else:
            sound_init = False
            sound_initialized = False  # Resetear la bandera cuando el sonido se detenga

        if emotions_list != last_emotions_list:
            emotions_presentes = [find_similar_emotion(emotion) for emotion in emotions_list if find_similar_emotion(emotion) in emotions]

            print("POSIBLES EMOCIONES: ", end="")
            print(emotions_presentes)
            if emotions_presentes:
                current_emotion = random.choice(emotions_presentes)
                print("EMOCION SELECCIONADA: ", end="")
                print(current_emotion)
        
        last_emotions_list = emotions_list
        

        if amplitude > amplitude_threshold:
            if not is_speaking:
                if current_frame == 0 or current_frame == 2:
                    current_frame = 2
                else:
                    current_frame = 3
            stepts_time = 10
        else:
            if not is_blinking and time.time() >= next_blink_time:
                is_blinking = True
                blink_start_time = time.time()
                current_frame = 1

            if is_blinking and time.time() >= blink_start_time + blink_duration:
                is_blinking = False
                next_blink_time = time.time() + random.randint(1, 4)
                current_frame = 0
            stepts_time = 1

        if amplitude > amplitude_threshold:
            if not is_speaking and time.time() >= next_speak_time:
                is_speaking = True
                speak_start_time = time.time()
                current_frame = 0

            if is_speaking and time.time() >= next_speak_time + speak_duration:
                is_speaking = False
                next_speak_time = time.time() + speak_duration
                if current_frame == 3 or current_frame == 2:
                    current_frame = 3

        vertical_position = screen_height // 2 + int(amplitude_sine * np.sin(2 * np.pi * frequency_sine * timey)) + 19 * 2

        screen.fill(color_screen)
        image = images[current_emotion][current_frame]
        image_rect = image.get_rect(center=(screen_width // 2, vertical_position))
        screen.blit(image, image_rect)

        # Dibujar bolita de color en la esquina inferior derecha
        color_bolita = colores_bolita.get(estado_voz, (0, 0, 0))
        pygame.draw.circle(screen, color_bolita, (screen_width - 20, screen_height - 20), 10)

        pygame.display.flip()

        timey += framon * stepts_time
        time.sleep(framon)

global emotions_list
emotions_list=[]
print("Loading GPT4WAIFU...")
MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello there."},
    {"role": "assistant", "content": "Hi, how can I help you?"},
]

SPECIAL_COMMANDS = {
    "Comando reiniciar": lambda messages: messages.clear(),
    "Comando salir": lambda _: sys.exit(),
    "Comando borrar": lambda _: print("\n" * 100),
    "Comando ayuda": lambda _: print("Special commands: /reset, /exit, /help and /clear"),
}

VersionInfo = namedtuple('VersionInfo', ['major', 'minor', 'micro'])
VERSION_INFO = VersionInfo(1, 0, 0)
VERSION = '.'.join(map(str, VERSION_INFO))


# Crear aplicación typer
app = typer.Typer()

def read_message_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def read_system_prompt():
    global args
    """Lee el mensaje inicial desde el archivo especificado por el usuario."""
    file_name = f"personalidad\\system_prompt_{args.perso}.txt"
    print(args.perso)
    try:
        with open(file_name, "r") as file:

            initial_prompt = file.read()
    except FileNotFoundError:
        print(f"El archivo {file_name} no existe.")
        initial_prompt = ""
    return initial_prompt

def repl(
    model: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
    n_threads: int = 18,
    device: str = "gpu"
):
    """The CLI read-eval-print loop."""
    gpt4all_instance = GPT4All(model, device=device)

    # Configurar número de hilos si se especifica
    if n_threads is not None:
        num_threads = gpt4all_instance.model.thread_count()

        # Configurar número de hilos
        gpt4all_instance.model.set_thread_count(n_threads)

        num_threads = gpt4all_instance.model.thread_count()

    use_new_loop = False
    try:
        version = importlib.metadata.version('gpt4all')
        version_major = int(version.split('.')[0])
        if version_major >= 1:
            use_new_loop = True
    except:
        pass  # fall back to old loop
    if use_new_loop:
        _new_loop(gpt4all_instance)

    use_new_loop = False
    try:
        version = importlib.metadata.version('gpt4all')
        version_major = int(version.split('.')[0])
        if version_major >= 1:
            use_new_loop = True
    except:
        pass  # fall back to old loop
    if use_new_loop:
        _new_loop(gpt4all_instance)

def limpiar_texto(texto):
    # Expresión regular para mantener letras, números, espacios, acentos, ñ y signos de puntuación
    patron = r'[^a-zA-Z0-9\sáéíóúüñÁÉÍÓÚÜÑ.!?¿¡]'
    texto_limpio = re.sub(patron, '', texto)
    return texto_limpio

def cadena_valida(cadena):
    # Eliminar espacios en blanco al inicio y al final
    cadena = cadena.strip()
    # Verificar que no esté vacía y que contenga al menos una letra o número
    return bool(cadena) and any(c.isalnum() for c in cadena)

def extraer_emociones(texto):
    # Buscar emociones en el texto
    emociones = re.findall(r'\[([^\]]+)\]', texto)
    
    # Eliminar las emociones del texto
    texto_sin_emociones = re.sub(r'\[[^\]]+\]', '', texto)
    
    # Buscar texto entre asteriscos
    texto_entre_asteriscos = re.findall(r'\*([^*]+)\*', texto)

    # Eliminar texto entre asteriscos
    #texto_sin_emociones = re.sub(r'\*([^*]+)\*', '', texto_sin_emociones)
    
    return texto_sin_emociones.strip(), emociones


def speak_text_with_edge_tts(text):
    global global_audio_path, args
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
            output_file_path = temp_audio_file.name
            global_audio_path= output_file_path
        quoted_text = f'"{text}"'
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
        # Copy a file
        shutil.copy(output_file_path, "salida_temporal.mp3")
        if os.path.exists(output_file_path):
            try:
                play_audio(output_file_path)
                global_audio_path = output_file_path  # Actualizar global_audio_path
            except Exception as e:
                print(f"*se confunde*")
        else:
            print("*se traba al hablar*")
    except Exception as e:
        print(f"*se hace la oidos sordos*")

# Función para reproducir audio con pygame y esperar a que termine
def play_audio(audio_file):
    global current_time_ms
    # Cargar el archivo de audio
    pygame.mixer.music.load(audio_file)
    # Reproducir el audio
    pygame.mixer.music.play()
     #Esperar a que termine el audio
    while pygame.mixer.music.get_busy():
        current_time_ms = pygame.mixer.music.get_pos()
        time.sleep(0.01)

# Reemplaza la función speak_text con speak_text_with_edge_tts
def speak_text(text):
    speak_text_with_edge_tts(text)

def normalize_phonetics(word):
    phonetic_map = {
        'v': 'b', 'b': 'b', 
        'c': 'k', 'k': 'k', 'q': 'k', 'qu': 'k', 
        'z': 's', 's': 's', 'x': 's', 'ch': 'sh', 'sh': 'sh',  
        'll': 'y', 'y': 'y', 'i': 'y', 
        'h': '', 
        'g': 'j', 'j': 'j',  # General, jeneral
        'rr': 'r', 'r': 'r',  # Carro, caro
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

def listen_to_voice():
    """Captura el audio del micrófono y lo convierte en texto"""
    global running_repl, estado_voz  # Asegurarse de usar la variable global
    print("*Se queda escuchando*")
    while running_repl:
        global args
        with mic as source:
            try:
                estado_voz = 1
                audio = recognizer.listen(source, timeout=5)  # Añadir timeout
                print("*Escuchado*")
            except sr.WaitTimeoutError:
                #print("*Tiempo de espera excedido, reintentando...*")
                continue  # Volver al comienzo del bucle si se excede el tiempo de espera
        try:
            estado_voz = 2
            text = recognizer.recognize_google(audio, language='es-ES')
            print(f"Has dicho: {text}")
            # Verificar si el texto contiene la palabra clave
            normalized_text = normalize_phonetics(text.lower())
            normalized_keyword = normalize_phonetics(args.perso.lower())
            if normalized_keyword in normalized_text:
                # Extraer el texto después de la palabra clave
                keyword_index = normalized_text.index(normalized_keyword)
                # Añadir la longitud de la palabra clave para saltar la palabra y el espacio después de ella
                command = text[keyword_index + len(args.perso):].strip()
                #print(f"Comando recibido: {command}")
                return command
            else:
                estado_voz = 1
        except sr.UnknownValueError:
            print("*No lo entiende*")
        except sr.RequestError as e:
            print(f"Error al solicitar resultados de reconocimiento; {e}")

    print("El programa ha sido detenido.")

def _new_loop(gpt4all_instance):
    global emotions_list, estado_voz
    initial_message = read_system_prompt()
    emocion=["Aliviada"]
    print("Cargando waifu...") 
    prev_message = ""                   
    message_counter=0
    max_tokens=300
    condition=True

    with gpt4all_instance.chat_session(initial_message):
        while True:

            estado_voz=1
            message = listen_to_voice()  # Usar reconocimiento de voz en lugar de input()

            if running_repl == False:
                message="Comando salir"

            # Check if special command and take action

            if message in SPECIAL_COMMANDS:
                SPECIAL_COMMANDS[message](MESSAGES)
                continue

            # if regular message, append to messages
            MESSAGES.append({"role": "user", "content": message})

            # if regular message, append to messages
            MESSAGES.append({"role": "user", "content": message})
            # execute chat completion and ignore the full response since
            # we are outputting it incrementally
            print("*Se pone a pensar*")
            estado_voz=0
            response_generator = gpt4all_instance.generate(
                message,
                max_tokens=max_tokens,
                temp=0.9,
                top_k=40,
                top_p=0.9,
                min_p=0.0,
                repeat_penalty=1.18,
                repeat_last_n=64,
                n_batch=9,
                streaming=True,
                )
            response = io.StringIO()
            chunk = ""
            emociones =["Neutral"]
            texto =""
            emocion=""
            asteriscos=""


            response_text=""
            for token in response_generator:
                response_text+=token
            response_text+="\n"
            textox, emotions_lista  = extraer_emociones(response_text)

            print("EL USUARIO DICE:")
            print(message)
            print("")
            print("LA WAIFU DICE:")
            print(response_text)
            print("TODAS LAS EMOCIONES:", end="")
            print(emotions_lista)
            
            tmp_emotion=[]
            emotion=[]
            token_max=len(response_text)
            for token in response_text:
                response.write(token)
                chunk += token
                if token.endswith("\n"):
                    texto, emociones = extraer_emociones(chunk)
                    if len(emociones)>0:
                        for i in emociones:
                            emotion.append(i)
                    
                    texto=limpiar_texto(texto)

                    if cadena_valida(texto):
                        tmp_emotion+=emotion
                        emotions_list=tmp_emotion
                        estado_voz=3
                        speak_text(texto)
                        tmp_emotion=[]
                        emotion=[]
                    else:
                        tmp_emotion+=emotion
                        emotions_list=tmp_emotion
                        tmp_emotion=[]
                    chunk = ""
            message_counter=message_counter+1
            # record assistant's response to messages
            response_message = {'role': 'assistant', 'content': response.getvalue()}
            response.close()
            gpt4all_instance.current_chat_session.append(response_message)
            MESSAGES.append(response_message)
            print()


@app.command()
def version():
    """The CLI version command."""
    print(f"gpt4all-cli v{VERSION}")
    print(f"gpt4all-cli v{Path.home()}")


if __name__ == "__main__":  
    repl_thread = threading.Thread(target=repl)
    repl_thread.start()
    pngtuber()
    pygame.quit()
    running_repl = False
    print("FINALIZADO")
    
