import subprocess
import time
import os
import argparse

# Parsear los argumentos de la línea de comandos
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--channel', type=str, default='Caly the Cattrap', help='Name of the PNGtuber')
parser.add_argument('--perso', type=str, default='waifu', help='Nombre del archivo de sistema de inicio')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
parser.add_argument('--png', type=str, default='Calyseym', help='Nombre Vtuber')
parser.add_argument('--model', type=str, default='Meta-Llama-3-8B-Instruct.Q4_0.gguf', help='Nombre del modelo')
parser.add_argument('--option', type=str, default='', help='Opcion')
args = parser.parse_args()

# Eliminar archivos temporales
def delete_temp_files():
    try:
        os.remove("salida_temporal.mp3")
        os.remove("salida_temporal.wav")
    except FileNotFoundError:
        pass

# Ejecutar scripts en paralelo
def run_scripts():
    # Eliminar archivos temporales inicialmente
    delete_temp_files()

    # Iniciar los scripts en paralelo
    process1 = subprocess.Popen(["python", "twitch2test.py", "--channel", args.channel,])
    time.sleep(5)  # Esperar 5 segundos antes de iniciar el siguiente script
    process2 = subprocess.Popen(["python", "twitch2waifuXvtuber.py", "--png", args.png,"--perso", args.perso, "--voz", args.voz, "--model", args.model, "--option", args.option])
    process3 = subprocess.Popen(["python", "small_monsters_twitch.py"])
    process4 = subprocess.Popen(["python", "game_voice.py"])

    # Esperar a que los procesos en paralelo terminen
    process1.wait()
    process2.wait()
    process3.wait()
    process4.wait()

    # Eliminar archivos temporales después de ejecutar los scripts
    delete_temp_files()

if __name__ == "__main__":
    run_scripts()
