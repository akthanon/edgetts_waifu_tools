import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

# Variable global para almacenar el proceso en ejecución
proceso_actual = None

# Función para ejecutar los archivos .py con argumentos según el programa seleccionado
def ejecutar_py(ruta_py, botones):
    global proceso_actual
    try:
        # Deshabilitar todos los botones
        for boton in botones:
            boton.config(state=tk.DISABLED)
        
        # Diccionario que mapea cada programa con sus argumentos
        argumentos_programas = {
            "parallel_only_twitch_games.py": [],
            "parallel_voice_to_edgetts.py": [],
            "parallel_talk_with_txt_waifu.py": ["--perso", combo_personalidad.get()],
            "parallel_talk_with_Vtuber.py": ["--perso", combo_personalidad.get(), "--png", combo_pngtuber.get()],
            "parallel_twitch_to_txt_waifu.py": ["--perso", combo_personalidad.get(), "--channel", combo.get()],
            "parallel_twitch_to_vtuber.py": ["--perso", combo_personalidad.get(), "--channel", combo.get(), "--png", combo_pngtuber.get()],
            "parallel_twitch_voice.py": ["--channel", combo.get()],
            "parallel_twitch_to_Vtuber_games.py": ["--perso", combo_personalidad.get(), "--channel", combo.get(), "--png", combo_pngtuber.get()]
        }
        
        # Obtener los argumentos correspondientes al programa seleccionado
        argumentos = argumentos_programas.get(os.path.basename(ruta_py), [])
        
        # Construir la lista de argumentos
        args = ["cmd", "/c", "python", os.path.basename(ruta_py)] + argumentos
        
        # Ejecutar el archivo .py con los argumentos
        proceso_actual = subprocess.Popen(args, shell=True)
        
        # Esperar a que el proceso termine para volver a habilitar los botones
        ventana.after(100, lambda: chequear_proceso(proceso_actual, botones))
    except Exception as e:
        messagebox.showerror("Error", f"El archivo {ruta_py} no se pudo ejecutar.\n{e}")
        for boton in botones:
            boton.config(state=tk.NORMAL)

# Función para verificar si el proceso en ejecución ha terminado
def chequear_proceso(proceso, botones):
    if proceso.poll() is None:
        ventana.after(100, lambda: chequear_proceso(proceso, botones))
    else:
        # Habilitar todos los botones cuando el proceso termine
        for boton in botones:
            boton.config(state=tk.NORMAL)
        # Restablecer la variable proceso_actual
        global proceso_actual
        proceso_actual = None

# Función para terminar el proceso en ejecución
def cerrar_py():
    global proceso_actual
    if proceso_actual and proceso_actual.poll() is None:
        try:
            proceso_actual.terminate()  # Terminar el proceso
            proceso_actual.wait()  # Esperar a que el proceso termine
            messagebox.showinfo("Información", "El programa en ejecución ha sido cerrado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cerrar el programa.\n{e}")
    else:
        messagebox.showinfo("Información", "No hay ningún programa en ejecución.")

# Funciones para cambiar el color de los botones al pasar el ratón
def on_enter(e):
    e.widget['background'] = '#007ACC'

def on_leave(e):
    e.widget['background'] = '#00A2E8'

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Lanzador de Programas")
ventana.geometry("600x700")
ventana.configure(bg="#333333")

# Título
titulo = tk.Label(ventana, text="Seleccione un programa para ejecutar", font=("Helvetica", 20, "bold"), bg="#333333", fg="#FFFFFF")
titulo.pack(pady=20)

# Frame para contener los botones de los archivos .bat
frame_botones = tk.Frame(ventana, bg="#444444")
frame_botones.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Lista de archivos .bat con rutas
archivos_py = [
    "parallel_only_twitch_games.py",
    "parallel_voice_to_edgetts.py",
    "parallel_talk_with_txt_waifu.py",
    "parallel_talk_with_Vtuber.py",
    "parallel_twitch_to_txt_waifu.py",
    "parallel_twitch_to_vtuber.py",
    "parallel_twitch_voice.py",
    "parallel_twitch_to_Vtuber_games.py"
]

# Crear y colocar los botones para cada archivo .bat
botones = []
for i, archivo in enumerate(archivos_py):
    nombre_amigable = archivo.replace("parallel_", "").replace(".py", "").replace("_", " ").capitalize()
    boton = tk.Button(frame_botones, text=nombre_amigable, font=("Helvetica", 14), bg="#00A2E8", fg="black", command=lambda a=archivo: ejecutar_py(a, botones))
    boton.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="ew")
    boton.bind("<Enter>", on_enter)
    boton.bind("<Leave>", on_leave)
    botones.append(boton)

# Lista de nombres para el combobox
nombres = ["crisbelgs", "calyseym", "ibai", "srtaminyeon"]

# Crear una etiqueta para explicar el propósito del combobox
etiqueta_combobox = tk.Label(ventana, text="Seleccionar canal:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox.pack(pady=(0, 5))  # Ajuste del espaciado

# Crear y colocar el combobox
combo = ttk.Combobox(ventana, values=nombres)
combo.set("srtaminyeon")  # Establecer "crisbelgs" como opción predeterminada
combo.pack(pady=5)

# Configurar las columnas del frame para que se expandan uniformemente
frame_botones.grid_columnconfigure(0, weight=1)
frame_botones.grid_columnconfigure(1, weight=1)

# Obtener los nombres de los directorios dentro de las carpetas "PNGtubers" y "Personalidad"
nombres_pngtuber = os.listdir("PNGtubers")
nombres_personalidad = os.listdir("Personalidad")

# Crear una etiqueta y combobox para seleccionar de la lista "PNGtuber"
etiqueta_combobox_pngtuber = tk.Label(ventana, text="Seleccionar PNGtuber:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox_pngtuber.pack(pady=(0, 5))  # Ajuste del espaciado
combo_pngtuber = ttk.Combobox(ventana, values=nombres_pngtuber)
combo_pngtuber.set("Calyseym")
combo_pngtuber.pack(pady=5)

# Limpiar los nombres de los archivos quitando "system_prompt_" y ".txt"
nombres_personalidad_limpio = [nombre.replace("system_prompt_", "").replace(".txt", "") for nombre in nombres_personalidad]

# Crear una etiqueta y combobox para seleccionar de la lista "Personalidad"
etiqueta_combobox_personalidad = tk.Label(ventana, text="Seleccionar personalidad:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox_personalidad.pack(pady=(0, 5))  # Ajuste del espaciado
combo_personalidad = ttk.Combobox(ventana, values=nombres_personalidad_limpio)
combo_personalidad.set("waifu")
combo_personalidad.pack(pady=5)

# Botón para cerrar el programa en ejecución
cerrar_py_boton = tk.Button(ventana, text="Cerrar Programa en Ejecución", font=("Helvetica", 14), bg="#FFAA00", fg="black", command=cerrar_py)
cerrar_py_boton.pack(padx=20, pady=10)
cerrar_py_boton.config(height=2)  # Ajustar la altura del botón

# Botón para cerrar la aplicación
cerrar_boton = tk.Button(ventana, text="Cerrar Aplicación", font=("Helvetica", 14), bg="#FF5555", fg="white", command=ventana.quit)
cerrar_boton.pack(padx=20, pady=10)
cerrar_boton.config(height=2)  # Ajustar la altura del botón

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
