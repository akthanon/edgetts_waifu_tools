import subprocess
import os
import tempfile
from pathlib import Path
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
from pydub import AudioSegment
import shutil

def list_emotions_similar():
    emotions_similar = {
        "Aburrida": ["Aburrido", "Desinteresada", "Desinteresado", "Cansada", "Cansado", "Indiferente"],
        "Emocionada": ["Emocionado", "Entusiasmada", "Entusiasmado", "Animada", "Animado","Muy emocionada"],
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
    return emotions_similar, emotions


def find_similar_emotion(emotion, emotions_similar, emotions):
    for key, similar_emotions in emotions_similar.items():
        if emotion == key or emotion in similar_emotions:
            return key
    return random.choice(emotions)

# Cargar y redimensionar imágenes de emociones
def load_red_images(emotions, pngtuber_path, screen_width, screen_height):
    images = {}
    for emotion in emotions:
        images[emotion] = []
        for i in range(4):
            img_path = os.path.join(pngtuber_path, f"{emotion}", f"{i}.png")
            img = pygame.image.load(img_path).convert_alpha()
            img = scale_image(img, screen_width, screen_height)
            images[emotion].append(img)
    return images

def inicializar_variables():
    current_time_ms = -1
    emotions_list = []
    current_emotion = "Pensativa"
    current_frame = 0
    next_blink_time = time.time() + random.randint(3, 6)
    is_blinking = False
    blink_start_time = 0
    blink_duration = 0.1
    amplitude_sine = 20
    frequency_sine = 0.2
    amplitude_threshold = 1000
    stepts_time = 1
    speak_duration = 0.2
    is_speaking = True
    next_speak_time = 0
    last_emotions_list = None
    estado_voz = 3
    running = True

    # Resto de inicializaciones
    sound_init = False
    sound_initialized = False  # Bandera para controlar la inicialización del sonido

    mp3_input_file = os.path.join("audios", "sonido3.mp3")
    framon = 0.02
    timey = 0
    amplitude = 0
    estado = "finalizado"
    audio_path = ""
    old_sound = ""
    audio_mp3 = "salida_temporal.mp3"
    duration = 0
    terminado = []
    time_blinking = 0.5
    
    # Definir colores
    colores_bolita = {
        0: (0, 255, 0),   # Verde
        1: (0, 0, 255),   # Azul
        2: (255, 255, 0), # Amarillo
        3: (255, 0, 0)    # Rojo
    }

    return (current_time_ms, emotions_list, current_emotion, current_frame, next_blink_time,
            is_blinking, blink_start_time, blink_duration, amplitude_sine,
            frequency_sine, amplitude_threshold, stepts_time, speak_duration,
            is_speaking, next_speak_time, last_emotions_list, estado_voz, running,
            mp3_input_file, framon, timey, amplitude, estado, audio_path,
            old_sound, audio_mp3, duration, terminado, time_blinking, colores_bolita,
            sound_init, sound_initialized)

def procesar_emociones(emotions_list, last_emotions_list, emotions, emotions_similar):
    emotions_presentes = [find_similar_emotion(emotion, emotions_similar, emotions) for emotion in emotions_list if find_similar_emotion(emotion, emotions_similar, emotions) in emotions]
    print("POSIBLES EMOCIONES: ", end="")
    print(emotions_presentes)
    if emotions_presentes:
        current_emotion = random.choice(emotions_presentes)
        print("EMOCION SELECCIONADA: ", end="")
        print(current_emotion)
    else:
        current_emotion = random.choice(emotions)
        print("EMOCION SELECCIONADA: ", end="")
        print(current_emotion)
    last_emotions_list = emotions_list
    return current_emotion, last_emotions_list

def dibujar_pantalla(screen, screen_width, screen_height, color_screen, current_emotion, current_frame, vertical_position, estado_voz, colores_bolita, images):
    screen.fill(color_screen)
    image = images[current_emotion][current_frame]
    image_rect = image.get_rect(center=(screen_width // 2, vertical_position))
    screen.blit(image, image_rect)

    # Dibujar bolita de color en la esquina inferior derecha
    color_bolita = colores_bolita.get(estado_voz, (0, 0, 0))
    pygame.draw.circle(screen, color_bolita, (screen_width - 20, screen_height - 20), 10)

    pygame.display.flip()

def manage_expression(amplitude, amplitude_threshold, is_speaking, is_blinking, current_frame, timey, screen_height, amplitude_sine, frequency_sine, next_blink_time, blink_start_time, blink_duration, next_speak_time, speak_duration):

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
            current_frame = 0

        if is_speaking and time.time() >= next_speak_time + speak_duration:
            is_speaking = False
            next_speak_time = time.time() + speak_duration
            if current_frame == 3 or current_frame == 2:
                current_frame = 3

    vertical_position = screen_height // 2 + int(amplitude_sine * np.sin(2 * np.pi * frequency_sine * timey)) + 19 * 2

    return is_speaking, is_blinking, current_frame, stepts_time, vertical_position, next_speak_time, blink_start_time, next_blink_time

def handle_blinking(is_blinking, next_blink_time, blink_duration, blink_start_time, current_frame):
    if not is_blinking and time.time() >= next_blink_time:
        is_blinking = True
        blink_start_time = time.time()
        current_frame = 1

    if is_blinking and time.time() >= blink_start_time + blink_duration:
        is_blinking = False
        next_blink_time = time.time() + random.randint(1, 4)
        current_frame = 0

    return is_blinking, next_blink_time, blink_start_time, current_frame


def handle_audio(audio_mp3, sound_init, sound_initialized, current_time_ms, global_audio_path, duration, estado, audio_path, current_frame):
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
    if current_time_ms + 20 >= duration:
        amplitude = 0
        current_frame = 0
        duration = 0

    return sound_initialized, amplitude, current_frame, duration, estado, audio_path, sound_init

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

def read_system_prompt(args):
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

def limpiar_texto(texto):
    # Expresión regular para mantener letras, números, espacios, acentos, ñ y signos de puntuación
    patron = r'[^a-zA-Z0-9\sáéíóúüñÁÉÍÓÚÜÑ.,!?¿¡]'
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
    #texto_sin_emociones = re.sub(r'\[[^\]]+\]', '', texto)
    
    # Buscar texto entre asteriscos
    texto_entre_asteriscos = re.findall(r'\*([^*]+)\*', texto)

    # Eliminar texto entre asteriscos
    texto_sin_emociones = re.sub(r'\*([^*]+)\*', '', texto)
    #texto_sin_emociones = texto
    
    return texto_sin_emociones.strip(), texto_entre_asteriscos


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

def speak_text_with_edge_tts(text, global_audio_path, args):
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
global current_time_ms
current_time_ms = 0
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

def remove_timestamps(messages):
    # Quitar la parte de [hora:minuto:segundo] de cada línea
    messages_notime=[message.split("] ", 1)[1] if "] " in message else message for message in messages.splitlines()]
    #print(messages)
    return messages_notime

def count_tokens(text):
    return int(len(text.split()) * 2)

def deslistar(liste, args):
    lista_salida=[]
    length = len(liste)
    num_pares = length // 2
    cuarto_pares = num_pares // 6  # Encontrar un cuarto del número de pares

    # Extraer el 25% final de la lista en términos de pares
    resultado = liste[-cuarto_pares*2:]
    lista_salida=resultado

    formatted_text = ""

    for entry in lista_salida:
        role = entry['role']
        content = entry['content']
        
        if role == 'user':
            role = 'usuarios'
        elif role == 'assistant':
            role = args.perso
        
        formatted_text += f'{role}: "{content}"\n'
    formatted_text = f"ESTO ES PARTE DEL HISTORIAL DE UNA CONVERSACIÓN PASADA QUE TU {args.perso} TUVISTE CON LOS USUARIOS: \n{formatted_text}"
    return formatted_text

def read_message_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""
