import subprocess
import os

# Función para ejecutar los comandos del archivo .bat
def run_bat_commands():
    # Cambiar al directorio "games"
    os.chdir("games")

    # Ejecutar el script interfaz.py dentro del directorio "games"
    subprocess.run(["python", "interfaz.py"])

    # Volver al directorio anterior
    os.chdir("..")

if __name__ == "__main__":
    run_bat_commands()
