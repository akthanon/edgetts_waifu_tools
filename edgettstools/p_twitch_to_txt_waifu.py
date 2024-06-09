import subprocess
import time
import argparse

# Parsear los argumentos de la línea de comandos
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--channel', type=str, default='Caly the Cattrap', help='Name of the PNGtuber')
parser.add_argument('--voz', type=str, default='es-PA-MargaritaNeural', help='Voice')
parser.add_argument('--perso', type=str, default='waifu', help='Nombre del archivo de sistema de inicio')
args = parser.parse_args()

# Ejecutar scripts en paralelo
def run_scripts():
    # Eliminar archivos temporales inicialmente

    # Iniciar los scripts en paralelo
    process1 = subprocess.Popen(["python", "twitch2test.py", "--channel", args.channel,])
    time.sleep(5)  # Esperar 5 segundos antes de iniciar el siguiente script
    process2 = subprocess.Popen(["python", "twitch2waifu.py", "--perso", args.perso, "--voz", args.voz])

    # Esperar a que los procesos en paralelo terminen
    process1.wait()
    process2.wait()

    # Eliminar archivos temporales después de ejecutar los scripts
    delete_temp_files()

if __name__ == "__main__":
    run_scripts()
