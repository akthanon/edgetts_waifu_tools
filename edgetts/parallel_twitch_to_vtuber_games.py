import subprocess
import time
import os

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
    process1 = subprocess.Popen(["python", "twitch2test.py", "calyseym"])
    time.sleep(5)  # Esperar 5 segundos antes de iniciar el siguiente script
    process2 = subprocess.Popen(["python", "twitch2waifuXvtuber_farm.py", "--png_name", "Calyseym"])

    # Ejecutar el script del juego
    subprocess.run(["python", "games/game_snake.py"])

    # Esperar a que los procesos en paralelo terminen
    process1.wait()
    process2.wait()

    # Eliminar archivos temporales después de ejecutar los scripts
    delete_temp_files()

if __name__ == "__main__":
    run_scripts()
