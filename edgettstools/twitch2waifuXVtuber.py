import os
import sys
from gpt4all import GPT4All # type: ignore
import time
import pygame # type: ignore
import threading
import argparse
global current_time_ms
from funciones_tts import *
global args

# Configuración de argparse
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--perso', type=str, default='waifu', help='Nombre del archivo de sistema de inicio')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
parser.add_argument('--png', type=str, default='Calyseym', help='Nombre Vtuber')
parser.add_argument('--model', type=str, default='Meta-Llama-3-8B-Instruct.Q4_0.gguf', help='Nombre del modelo')
parser.add_argument('--option', type=str, default='', help='Opcion')
parser.add_argument('--lang', type=str, default='Español', help='Opcion')
parser.add_argument('--request', type=str, default='False', help='Opcion')
parser.add_argument('--temp', type=str, default='0.9', help='Opcion')
parser.add_argument('--reppen', type=str, default='1', help='Opcion')
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

#Variables
running_repl = True
global global_audio_path
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

emotions_similar, emotions = list_emotions_similar()

audio_path = os.path.join("audios", "sonido2.wav")

images=load_red_images(emotions, pngtuber_path, screen_width, screen_height)

# Función principal del PNGtuber
def pngtuber(screen, screen_width, screen_height):
    global global_audio_path, estado_voz
    global current_time_ms, emotions_list, emotions, emotion

    # Inicialización de variables
    (current_time_ms, emotions_list, current_emotion, current_frame, next_blink_time,
     is_blinking, blink_start_time, blink_duration, amplitude_sine, frequency_sine,
     amplitude_threshold, stepts_time, speak_duration, is_speaking, next_speak_time,
     last_emotions_list, estado_voz, running, mp3_input_file, framon, timey, amplitude,
     estado, audio_path, old_sound, audio_mp3, duration, terminado, time_blinking,
     colores_bolita, sound_init, sound_initialized) = inicializar_variables()

    vertical_position = screen_height // 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        is_blinking, next_blink_time, blink_start_time, current_frame = handle_blinking(is_blinking, next_blink_time, blink_duration, blink_start_time, current_frame)
        
        from funciones_tts import current_time_ms
        
        try:
            sound_initialized, amplitude, current_frame, duration, estado, audio_path, sound_init=handle_audio(audio_mp3, sound_init, sound_initialized, current_time_ms, global_audio_path, duration, estado, audio_path, current_frame, is_blinking)
        except:
            pass

        if pygame.mixer.music.get_busy():
            sound_init = True
        else:
            sound_init = False
            sound_initialized = False  # Resetear la bandera cuando el sonido se detenga

        if emotions_list != last_emotions_list:
            current_emotion, last_emotions_list = procesar_emociones(emotions_list, last_emotions_list, emotions, emotions_similar)
        
        is_speaking, is_blinking, current_frame, stepts_time, vertical_position, next_speak_time, blink_start_time, next_blink_time = manage_expression(amplitude, amplitude_threshold, is_speaking, is_blinking, current_frame, timey, screen_height, amplitude_sine, frequency_sine, next_blink_time, blink_start_time, blink_duration, next_speak_time, speak_duration)

        dibujar_pantalla(screen, screen_width, screen_height, color_screen, current_emotion, current_frame, vertical_position, estado_voz, colores_bolita, images)
        timey += framon * stepts_time
        time.sleep(framon)

global emotions_list
emotions_list=[]


class MessageLogger:
    def __init__(self, filename, max_messages=1):
        self.filename = filename
        self.max_messages = max_messages
        self.messages = []

    def log(self, message):
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)
        self.messages.append(message)
        self.write_to_file()

    def write_to_file(self):
        with open(self.filename, 'w') as file:
            for message in self.messages:
                file.write(str(message) + '\n')

# Crear una instancia de MessageLogger
logger = MessageLogger("historial_chat.txt")

def repl(
    model: str = args.model,
    n_threads: int = None,
    device: str = "gpu"
):
    print(f"Model: {model}")
    gpt4all_instance = GPT4All(model, device=device, n_ctx=8192, model_path="modelos")

    # Configurar número de hilos si se especifica
    if n_threads is not None:
        num_threads = gpt4all_instance.model.thread_count()

        # Configurar número de hilos
        gpt4all_instance.model.set_thread_count(n_threads)

        num_threads = gpt4all_instance.model.thread_count()

    if args.option == "otwi":
        ejecutar_modelo(gpt4all_instance)
    elif args.option == "vtwi":
        ejecutar_modelo_voice(gpt4all_instance)

def ejecutar_modelo(gpt4all_instance):
    global emotions_list, estado_voz, args, global_audio_path
    emocion=["Aliviada"]
    print("Cargando waifu...")                 
    message_new=""
    message_old=""
    message=""
    ram_message=0
    max_tokens=200
    system_prompt = read_system_prompt(args)+"\nLanguage: "+args.lang
    total_count=count_tokens(system_prompt)
    while True:
        system_prompt = read_system_prompt(args)+"\nLanguage: "+args.lang
        with gpt4all_instance.chat_session(system_prompt):
            while True:
                if total_count>=count_tokens(system_prompt):
                    estado_voz=1
                    message_new = read_message_from_file('messages.txt')
                    lines_new = message_new.splitlines()
                    lines_unique = []
                    for line in lines_new:
                        if line not in message_old:
                            lines_unique.append(line)

                    message_new = "\n".join(lines_unique)      # Reconstruir el mensaje sin repeticiones 
                    message_notime = remove_timestamps(message_new)
                    message_notime = "\n".join(message_notime)
                    if (lines_unique) and message_notime!="":
                        message_old = message_old+"\n"+message_new
                        ram_message +=1

                        if ram_message==2000:
                            lines_old = message_old.splitlines()
                            message_old = "\n".join(lines_old[len(lines_old)//2:])
                            ram_message=0

                        message= message_notime
                    elif running_repl == True:
                        time.sleep(1)
                        continue
                    if running_repl == False:
                        sys.exit()
                    # Check if special command and take action

                    # execute chat completion and ignore the full response since
                    # we are outputting it incrementally
                if "comando reiniciar".lower() in message.lower():
                    total_count=7000
                    print("Reiniciando manualmente, por favor espere...")
                    message=""
                if total_count+max_tokens+count_tokens(message)>7000:
                    print(f"Reacomodando contexto...{total_count+max_tokens+count_tokens(message)} tokens")
                    total_count=0
                    break
                if total_count==0:
                    mensaje_colox = deslistar(old_chat[1:], args)
                    print(mensaje_colox)
                    old_chat=""
                    response_generatoro=gpt4all_instance.generate(
                        mensaje_colox,
                        max_tokens=0,
                        temp=float(args.temp),
                        top_k=40,
                        top_p=0.9,
                        min_p=0.0,
                        repeat_penalty=float(args.reppen),
                        repeat_last_n=64,
                        streaming=True,
                        )
                    total_count=count_tokens(system_prompt)+count_tokens(mensaje_colox)
                    response_texto=""
                    for token in response_generatoro:
                        response_texto+=token
                    response_texto+="\n"
                estado_voz=0
                response_generator = gpt4all_instance.generate(
                    message,
                    max_tokens=max_tokens,
                    temp=float(args.temp),
                    top_k=40,
                    top_p=0.9,
                    min_p=0.0,
                    repeat_penalty=float(args.reppen),
                    repeat_last_n=max_tokens*2,
                    n_batch=9,
                    #n_batch=128,
                    streaming=True,
                    )
                
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

                print("LOS SEGUIDORES DICEN:")
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
                            estado_voz=0
                            speak_text_with_edge_tts(texto, global_audio_path, args)
                            tmp_emotion=[]
                            emotion=[]
                        else:
                            tmp_emotion+=emotion
                            emotions_list=tmp_emotion
                            tmp_emotion=[]
                        chunk = ""

                total_count=total_count+count_tokens(message)+count_tokens(response_text)
                old_chat=gpt4all_instance.current_chat_session
                
                print(f"TOKENS: {total_count}")

def ejecutar_modelo_voice(gpt4all_instance):
    global emotions_list, estado_voz, args, global_audio_path
    emocion=["Aliviada"]
    print("Cargando waifu...")                  
    message_new=""
    message_new_games=""
    message_old=""
    message=""
    ram_message=0
    max_tokens=200
    system_prompt = read_system_prompt(args)+"\nLanguage: "+args.lang
    total_count=count_tokens(system_prompt)
    while True:
        system_prompt = read_system_prompt(args)
        with gpt4all_instance.chat_session(system_prompt):
            while True:
                if total_count>=count_tokens(system_prompt):
                    estado_voz=1
                    message_new = read_message_from_file('messages.txt')
                    message_new_games = read_message_from_file('games\\messages_game.txt')

                    # Eliminar líneas repetidas (manteniendo el orden)
                    lines_new = message_new.splitlines()
                    lines_unique = []
                    for line in lines_new:
                        if line not in message_old:
                            lines_unique.append(line)

                    # Eliminar líneas repetidas (manteniendo el orden)
                    lines_new_games = message_new_games.splitlines()
                    lines_unique_games = []
                    for line in lines_new_games:
                        if line not in message_old:
                            lines_unique.append(line)

                    message_new = "\n".join(lines_unique)      # Reconstruir el mensaje sin repeticiones 
                    message_new_games = "\n".join(lines_unique_games)      # Reconstruir el mensaje sin repeticiones 
                   
                    # Actualizar mensajes antiguos si hay nuevos
                    message_notime = remove_timestamps(message_new)
                    message_notime = "\n".join(message_notime)

                    if (lines_unique or lines_unique_games) and (message_notime!="" or message_new_games!=""):

                        message_old = message_old+"\n"+message_new+"\n"+message_new_games
                        ram_message +=1

                        if ram_message==2000:
                            lines_old = message_old.splitlines()
                            message_old = "\n".join(lines_old[len(lines_old)//2:])
                            ram_message=0

                        if lines_unique and not lines_unique_games:
                            message= message_notime
                        if not lines_unique and lines_unique_games:
                            message= message_new_games
                        if lines_unique and lines_unique_games:
                            message= message_notime + "\n" + message_new_games
                    elif running_repl == True:
                        time.sleep(0.5)
                        continue
                    if running_repl == False:
                        sys.exit()
                if "comando reiniciar".lower() in message.lower():
                    total_count=7000
                    old_chat=""
                    print("Reiniciando manualmente, por favor espere...")
                    message=""
                if total_count+max_tokens+count_tokens(message)>6000:
                    print(f"Reacomodando contexto...{total_count+max_tokens+count_tokens(message)} tokens")
                    total_count=0
                    break
                if total_count==0:
                    mensaje_colox = deslistar(old_chat[1:], args)
                    print(mensaje_colox)
                    old_chat=""
                    response_generatoro=gpt4all_instance.generate(
                        mensaje_colox,
                        max_tokens=0,
                        temp=float(args.temp),
                        top_k=40,
                        top_p=0.9,
                        min_p=0.0,
                        repeat_penalty=float(args.reppen),
                        repeat_last_n=64,
                        streaming=True,
                        )
                    total_count=count_tokens(system_prompt)+count_tokens(mensaje_colox)
                    response_texto=""
                    for token in response_generatoro:
                        response_texto+=token
                    response_texto+="\n"
                estado_voz=0
                response_generator = gpt4all_instance.generate(
                    message,
                    max_tokens=max_tokens,
                    temp=float(args.temp),
                    top_k=40,
                    top_p=0.9,
                    min_p=0.0,
                    repeat_penalty=float(args.reppen),
                    repeat_last_n=max_tokens*2,
                    streaming=True,
                    )
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

                print("LOS SEGUIDORES DICEN:")
                print(message)
                print("")
                print("LA WAIFU DICE:")
                print(response_text)
                print("TODAS LAS EMOCIONES:", end="")
                print(emotions_lista)
                
                tmp_emotion=[]
                emotion=[]
                token_futuro=""
                cuenta_token=0
                token_max=len(response_text)
                for token in response_text:
                    chunk += token
                    cuenta_token=cuenta_token+1
                    if cuenta_token<token_max:
                        token_futuro=chunk+response_text[cuenta_token]
                    if token.endswith("\n") or token_futuro.endswith("["):
                        texto, emociones = extraer_emociones(chunk)
                        #print(chunk)
                        if len(emociones)>0:
                            for i in emociones:
                                emotion.append(i)
                        
                        texto=limpiar_texto(texto)

                        if cadena_valida(texto):
                            tmp_emotion+=emotion
                            emotions_list=tmp_emotion
                            estado_voz=3
                            speak_text_with_edge_tts(texto, global_audio_path, args)
                            tmp_emotion=[]
                            emotion=[]
                        else:
                            tmp_emotion+=emotion
                            emotions_list=tmp_emotion
                            tmp_emotion=[]

                        chunk = ""
                #print(gpt4all_instance.current_chat_session)
                total_count=total_count+count_tokens(message)+count_tokens(response_text)
                old_chat=gpt4all_instance.current_chat_session
                #logger.log(old_chat)
                print(f"TOKENS: {total_count}")

if __name__ == "__main__":  
    repl_thread = threading.Thread(target=repl)
    repl_thread.start()
    pngtuber(screen, screen_width, screen_height)
    pygame.quit()
    running_repl = False
