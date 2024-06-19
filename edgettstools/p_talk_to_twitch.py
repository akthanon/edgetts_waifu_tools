import subprocess
import os
import tempfile
import speech_recognition as sr
import pygame
import argparse
import time
import random
import numpy as np
import threading
import shutil
import wave
from pydub import AudioSegment


global args
# Configuración de argparse
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--png', type=str, default='Caly the Cattrap', help='Name of the PNGtuber')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
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
color_screen = (0, 255, 0)

# Ruta de las imágenes y el audio
global emotions, emotions_similar

emotions_similar = {
    "aburrida": ["aburrido", "desinteresada", "desinteresado", "cansada", "cansado", "indiferente", "aburrir", "cansar", "desinteresar", "aburriendo", "cansando", "desinteresando", "aburro", "canso", "desintereso"],
    "emocionada": ["contenta","contento","alegre","emocionado", "entusiasmada", "entusiasmado", "animada", "animado", "emocionada", "feliz", "emocionar", "entusiasmar", "animar", "emocionando", "entusiasmando", "animando", "emociono", "entusiasmo", "animo"],
    "enojada": ["enojado", "furiosa", "furioso", "molesta", "molesto", "irritada", "irritado", "enojar", "molestar", "irritar", "enojando", "molestando", "irritando", "enojo", "molesto", "irrito"],
    "llorando": ["llorando", "sollozando", "lagrimando", "desconsolada", "desconsolado", "triste", "llorar", "sollozar", "lagrimar", "llorando", "sollozando", "lagrimando", "lloro", "sollozo", "lagrimeo"],
    "nerviosa": ["asustado","asustada", "asustar","asustando","nervioso", "alterada", "alterado", "ansiosa", "ansioso", "preocupada", "preocupado", "tensa", "tenso", "nervar", "alterar", "ansiar", "preocupar", "nervando", "alterando", "ansiando", "preocupando", "nervo", "altero", "ansío", "preocupo"],
    "neutral": ["neutro", "indiferente", "despreocupada", "despreocupado", "neutralizar", "despreocupar", "neutralizando", "despreocupando", "neutralizo", "despreocupo"],
    "pensativa": ["pensativo", "reflexiva", "reflexivo", "meditativa", "meditativo", "considerativa", "considerativo", "seria", "serio", "mili", "pensar", "reflexionar", "meditar", "considerar", "pensando", "reflexionando", "meditando", "considerando", "pienso", "reflexiono", "medito", "considero"],
    "riendo": ["cachonda","horny","sexy","caliente","riendo", "sonriendo", "carcajeando", "divertida", "divertido", "reír", "sonreír", "carcajear", "divertir", "riendo", "sonriendo", "carcajeando", "divirtiendo", "río", "sonrío", "carcajeo", "divierto"],
    "sorprendida": ["sorprendido", "asombrada", "asombrado", "impactada", "impactado", "espantada", "espantado", "sorprender", "asombrar", "impactar", "espantar", "sorprendiendo", "asombrando", "impactando", "espantando", "sorprendo", "asombro", "impacto", "espanto"],
    "vengativa": ["exitada", "vengativo", "exitado", "venganza", "ira", "emperra", "vengar", "irritar", "emperrar", "vengando", "irritando", "emperrando", "vengo", "irrito", "emperro"],
}



# Convertir la lista de emociones a minúsculas
emotions = ["aburrida", "emocionada", "enojada", "llorando", "nerviosa", "neutral", "pensativa", "riendo", "sorprendida", "vengativa"]

audio_path = os.path.join("audios", "sonido2.wav")


def find_similar_emotion(emotion):
    emotion = emotion.lower()
    for key, similar_emotions in emotions_similar.items():
        if emotion == key or emotion in similar_emotions:
            return key
    return emotions


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
    current_emotion = "pensativa"
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


def extraer_emociones(texto):
    # Inicializar una lista para almacenar las emociones encontradas
    emociones_encontradas = []
    
    # Convertir el texto a una lista de palabras
    palabras = texto.split()
    
    # Recorrer las palabras y buscar emociones
    for palabra in palabras:
        emocione=find_similar_emotion(palabra)
        if emocione in emotions:
            emociones_encontradas.append(palabra)
    
    return emociones_encontradas



def listen_to_voice():
    global estado_voz, emotions_list
    """Captura el audio del micrófono y lo convierte en texto"""
    with mic as source:
        print("*Se queda escuchando*")
        estado_voz=1
        audio = recognizer.listen(source,phrase_time_limit=10)
    try:
        os.system("cls")
        text = recognizer.recognize_google(audio, language='es-ES')
        emotions_list=extraer_emociones(text)
        print(emotions_list)
        print(f"Has dicho: {text}")
        estado_voz=0
        return text
    except sr.UnknownValueError:
        print("*No lo entiende*")
        estado_voz=3
    except sr.RequestError as e:
        print(f"Error al solicitar resultados de reconocimiento; {e}")
        estado_voz=3
    return ""

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


def talk_to_twitch():
    while True:
        message = listen_to_voice()
        if message.lower() == "salir":
            break
        speak_text_with_edge_tts(message)


if __name__ == "__main__":
    twitch_thread = threading.Thread(target=talk_to_twitch)
    twitch_thread.start()
    pngtuber()
    pygame.quit()
    print("FINALIZADO")
    
    