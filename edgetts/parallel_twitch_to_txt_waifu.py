import subprocess
import time

# Función para ejecutar los comandos del archivo .bat
def run_bat_commands():
    # Comando 1: iniciar twitch2test.py con argumento crisbelgs
    subprocess.Popen(["python", "twitch2test.py", "crisbelgs"])

    # Esperar 5 segundos
    time.sleep(5)

    # Comando 2: iniciar twitch2waifu.py
    subprocess.Popen(["python", "twitch2waifu.py"])

if __name__ == "__main__":
    run_bat_commands()
