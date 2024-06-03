import os
import random
import time
import numpy as np
import pygame
import wave
from pydub import AudioSegment

# Ruta del archivo MP3 de entrada y nombre del archivo WAV de salida
mp3_input_file = os.path.join("audios", "sonido3.mp3")
audio_path = os.path.join("audios", "salida.wav")

print(audio_path)

# Cargar el archivo MP3
sound = AudioSegment.from_mp3(mp3_input_file)

# Exportar el archivo WAV
sound.export(audio_path, format="wav")

# Configuración de pygame
pygame.init()

# Dimensiones de la ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Título de la ventana
pygame.display.set_caption("Caly the Cattrap PNGtuber")

# Colores
color_screen = (0, 255, 0)

# Ruta de las imágenes y el audio
pngtuber_name = "Caly the Cattrap"
emotions = ["Aburrido", "Emocionado", "Enojado", "Llorando", "Nervioso", "Neutral", "Pensativo", "Riendo", "Sorprendido"]
base_path = os.path.join(pngtuber_name)


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
        img_path = os.path.join(base_path, f"{pngtuber_name}_{emotion}", f"{i}.png")
        img = pygame.image.load(img_path).convert_alpha()
        img = scale_image(img, screen_width, screen_height)
        images[emotion].append(img)

# Función para obtener amplitud del fragmento de audio
def get_fragment_amplitude(sound, segundo):
    # Abre el archivo WAV
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
        
        return amplitud_promedio


# Función principal del PNGtuber
def pngtuber():
    running = True
    current_emotion = "Neutral"
    current_frame = 0
    next_blink_time = time.time() + random.randint(3, 6)
    blink_duration = 0.1
    is_blinking = False

    # Cargar el audio
    #sound = pygame.mixer.Sound(audio_path)
    #sound.play()
    
    # Duración de cada fragmento de audio
    frame = 0.1
    timex = 0
    # Parámetros de la función sinusoidal para el movimiento vertical
    amplitude_sine = 20  # Amplitud de la onda
    frequency_sine = 0.5  # Frecuencia de la onda
    vertical_position = screen_height // 2  # Posición inicial vertical
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Manejar el parpadeo
        if not is_blinking and time.time() >= next_blink_time:
            is_blinking = True
            blink_start_time = time.time()
            current_frame = 1

        if is_blinking and time.time() >= blink_start_time + blink_duration:
            is_blinking = False
            next_blink_time = time.time() + random.randint(3, 6)
            current_frame = 0

        # Obtener la amplitud del fragmento de audio actual
        amplitude = get_fragment_amplitude(audio_path, timex)

        # Sincronización labial en función del umbral de amplitud
        amplitude_threshold = 3000  # Umbral de volumen ajustable
        if amplitude > amplitude_threshold:
            if current_frame == 0:
                current_frame = 3 
            else:
                current_frame=2
            #amplitude_sine = 50  # Amplitud de la onda
            frequency_sine = 2  # Frecuencia de la onda
        else:
            current_frame=0
            #amplitude_sine = 20  # Amplitud de la onda
            frequency_sine = 0.2  # Frecuencia de la onda
        print(frequency_sine)

        # Calcular la posición vertical usando una función sinusoidal
        vertical_position = screen_height // 2 + int(amplitude_sine * np.sin(2 * np.pi * frequency_sine * timex))
        
        # Dibujar la imagen actual
        screen.fill(color_screen)
        image = images[current_emotion][current_frame]
        image_rect = image.get_rect(center=(screen_width // 2, vertical_position))
        screen.blit(image, image_rect)
        pygame.display.flip()

        # Controlar la velocidad de fotogramas
        timex += frame
        time.sleep(frame)

# Iniciar el PNGtuber

pngtuber()
pygame.quit()
# Salir de pygame
