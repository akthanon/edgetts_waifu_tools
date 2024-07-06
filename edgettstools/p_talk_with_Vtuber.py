import subprocess
import os
import argparse

# Parsear los argumentos de la línea de comandos
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--png', type=str, default='Caly the Cattrap', help='Name of the PNGtuber')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
parser.add_argument('--perso', type=str, default='waifu', help='Nombre del archivo de sistema de inicio')
parser.add_argument('--model', type=str, default='Meta-Llama-3-8B-Instruct.Q4_0.gguf', help='Nombre del modelo')
parser.add_argument('--option', type=str, default='', help='Opcion')
parser.add_argument('--lang', type=str, default='Español', help='Opcion')
parser.add_argument('--request', type=str, default='False', help='Opcion')
parser.add_argument('--temp', type=str, default='0.9', help='Opcion')
parser.add_argument('--reppen', type=str, default='1', help='Opcion')
args = parser.parse_args()

# Eliminar archivos temporales
def delete_temp_files():
    try:
        os.remove("salida_temporal.mp3")
        os.remove("salida_temporal.wav")
    except FileNotFoundError:
        pass

# Ejecutar el archivo .bat
def run_bat_file():
    # Eliminar archivos temporales inicialmente
    delete_temp_files()

    # Ejecutar el archivo .bat
    subprocess.run(["python", "talk2vtuber.py", "--png", args.png, "--perso", args.perso, "--voz", args.voz, "--model", args.model, "--option", args.option, "--lang", args.lang, "--request", args.request, "--temp", args.temp, "--reppen", args.reppen])

    # Eliminar archivos temporales después de ejecutar el archivo .bat
    delete_temp_files()

if __name__ == "__main__":
    run_bat_file()
