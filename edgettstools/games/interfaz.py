import tkinter as tk
from tkinter import messagebox
import subprocess

# Función para ejecutar los juegos
def ejecutar_juego(nombre_juego):
    try:
        subprocess.run(["python", nombre_juego], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"El juego {nombre_juego} no se pudo ejecutar.\n{e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Lanzador de Juegos en Python")
ventana.geometry("600x800")

# Título
titulo = tk.Label(ventana, text="Seleccione un juego para ejecutar", font=("Helvetica", 16))
titulo.pack(pady=20)

# Lista de juegos
juegos = [
    "game_antfarmsimulator.py",
    "game_arkanoid.py",
    "game_bacterycolony.py",
    "game_ecosistema.py",
    "game_voice.py",
    "game_snake.py",
    "game_trafico.py",
    "game_vehicle.py",
    "game_war.py",
    "game_20natural.py"
]

# Crear y colocar los botones para cada juego
for juego in juegos:
    nombre_amigable = juego.replace("game_", "").replace(".py", "").replace("_", " ").capitalize()
    boton = tk.Button(ventana, text=nombre_amigable, font=("Helvetica", 14), bg="lightblue", fg="black", command=lambda j=juego: ejecutar_juego(j))
    boton.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Botón para cerrar la aplicación
cerrar_boton = tk.Button(ventana, text="Cerrar Aplicación", font=("Helvetica", 14), bg="red", fg="white", command=ventana.quit)
cerrar_boton.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
