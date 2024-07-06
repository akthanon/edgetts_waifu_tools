import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import psutil

# Variable global para almacenar el proceso en ejecución
proceso_actual = None

# Función para ejecutar los archivos .py con argumentos según el programa seleccionado
def ejecutar_py(ruta_py, botones):
    global proceso_actual
    try:
        # Deshabilitar todos los botones
        for boton in botones:
            boton.config(state=tk.DISABLED)
        
        # Variables comunes
        perso = combo_personalidad.get()
        png = combo_pngtuber.get()
        voz = combo_voz.get()
        model = combo_modelos.get()
        lang = combo_idioma.get()
        request = str(request_var.get())
        temp = str(slider_temp.get())
        reppen = str(slider_repeat_penalty.get())
        channel = combo.get()

        # Diccionario que mapea cada programa con sus argumentos
        argumentos_programas = {
            "p_talk_with_Vtuber.py": ["--perso", perso, "--png", png, "--voz", voz, "--model", model, "--option",
                                      "voz", "--lang", lang, "--request", request, "--temp", temp, "--reppen", reppen],

            "p_text_with_Vtuber.py": ["--perso", perso, "--png", png, "--voz", voz, "--model", model, "--option",
                                      "text", "--lang", lang, "--request", request, "--temp", temp, "--reppen", reppen],

            "p_twitch_to_vtuber.py": ["--perso", perso, "--channel", channel, "--png", png, "--voz", voz, "--model", model, "--option",
                                      "otwi", "--lang", lang, "--request", request, "--temp", temp, "--reppen", reppen],

            "p_twitch_to_Vtuber_games.py": ["--perso", perso, "--channel", channel, "--png", png, "--voz", voz, "--model", model, "--option",
                                            "vtwi", "--lang", lang, "--request", request, "--temp", temp, "--reppen", reppen],

            "p_SUPREMUS.py": ["--perso", perso, "--channel", channel, "--png", png, "--voz", voz, "--model", model, "--option",
                              "vtwi", "--lang", lang, "--request", request, "--temp", temp, "--reppen", reppen],

            "p_only_twitch_games.py": [],
            "p_voice_to_edgetts.py": ["--voz", voz],
            "p_twitch_voice.py": ["--channel", channel, "--voz", voz],
            "p_talk_to_twitch.py": ["--png", channel, "--voz", voz],
        }
        
        # Obtener los argumentos correspondientes al programa seleccionado
        argumentos = argumentos_programas.get(os.path.basename(ruta_py), [])
        
        # Construir la lista de argumentos
        args = ["python", os.path.basename(ruta_py)] + argumentos
        
        # Ejecutar el archivo .py con los argumentos
        proceso_actual = subprocess.Popen(args)
        
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

# Función para terminar el proceso en ejecución y sus subprocesos
def cerrar_py():
    global proceso_actual
    if proceso_actual and proceso_actual.poll() is None:
        try:
            # Obtener el proceso principal
            proceso_principal = psutil.Process(proceso_actual.pid)
            
            # Terminar el proceso principal y sus subprocesos
            for subproceso in proceso_principal.children(recursive=True):
                subproceso.terminate()
            proceso_principal.terminate()

            # Esperar a que todos los procesos terminen
            gone, still_alive = psutil.wait_procs([proceso_principal] + proceso_principal.children(), timeout=5)
            for p in still_alive:
                p.kill()  # Forzar terminación si alguno sigue vivo

            #messagebox.showinfo("Información", "El programa en ejecución y sus subprocesos han sido cerrados.")
            print("El programa en ejecución y sus subprocesos han sido cerrados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cerrar el programa.\n{e}")
    #else:
        #messagebox.showinfo("Información", "No hay ningún programa en ejecución.")

def cerrar_todo():
    ventana.quit()
    cerrar_py()

# Funciones para cambiar el color de los botones al pasar el ratón
def on_enter(e):
    e.widget['background'] = '#007ACC'

def on_leave(e):
    e.widget['background'] = '#00A2E8'

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Lanzador de Programas")
ventana.geometry("900x800")
ventana.configure(bg="#333333")

# Título
titulo = tk.Label(ventana, text="EDGETTS WAIFU TOOLS", font=("Helvetica", 20, "bold"), bg="#333333", fg="#FFFFFF")
titulo.pack(pady=20)

# Frame para contener los botones de los archivos .bat
frame_botones = tk.Frame(ventana, bg="#444444")
frame_botones.pack(fill=tk.BOTH, expand=True, padx=20, pady=10, side=tk.LEFT)

# Lista de archivos .py con rutas
archivos_py = [
    "p_talk_with_Vtuber.py",
    "p_text_with_Vtuber.py",
    "p_twitch_to_vtuber.py",
    "p_twitch_to_Vtuber_farm.py",
    "p_SUPREMUS.py",
    "p_talk_to_twitch.py",
    "p_only_twitch_games.py",
    "p_voice_to_edgetts.py",
    "p_twitch_voice.py",
]

etiquetas= [
    "Talk with a PNGtuber",
    "Text with a PNGtuber",
    "Twitch AI PNGtuber",
    "Twitch AI PNGtuber, Games",
    "Twitch AI PNGtuber, SmMo, TwVo",
    "Fake AI PNGtuber",
    "Play Videogames",
    "Voice to AI voice",
    "Listen Twitch Commentaries",
]

max_width = max(len(etiqueta) for etiqueta in etiquetas)

# Crear y colocar los botones para cada archivo .bat
botones = []
columnas=1
col=0
for i, archivo in enumerate(archivos_py):
    #nombre_amigable = archivo.replace("p_", "").replace(".py", "").replace("_", " ").capitalize()
    nombre_amigable = etiquetas[col]
    # Crear un cuadro de texto adicional para mostrar las etiquetas de los argumentos
    boton_frame = tk.Frame(frame_botones, bg="#444444")
    boton_frame.grid(row=i // columnas, column=0 if i % columnas == 0 else 1, padx=(10, 0), pady=10, sticky="ew")
    boton = tk.Button(boton_frame, text=nombre_amigable, font=("Helvetica", 14), bg="#00A2E8", fg="black", command=lambda a=archivo: ejecutar_py(a, botones), width=max_width)
    boton.pack(side="right", padx=(0, 5))
    #etiqueta_args = tk.Label(boton_frame, text=f"({etiquetas[i]})", font=("Helvetica", 12), bg="#444444", fg="#FFFFFF")
    #etiqueta_args.pack(side="left")
    boton.bind("<Enter>", on_enter)
    boton.bind("<Leave>", on_leave)
    botones.append(boton)
    col+=1

# Lista de nombres para el combobox
nombres = ["crisbelgs", "calyseym", "srtaminyeon"]

# Crear una etiqueta para explicar el propósito del combobox
etiqueta_combobox = tk.Label(ventana, text="Choise Channel:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox.pack(pady=(0, 5))  # Ajuste
# Crear y colocar el combobox
combo = ttk.Combobox(ventana, values=nombres)
combo.set("calyseym")  # Establecer "srtaminyeon" como opción predeterminada
combo.pack(pady=5)

# Configurar las columnas del frame para que se expandan uniformemente
frame_botones.grid_columnconfigure(0, weight=1)
frame_botones.grid_columnconfigure(1, weight=1)

# Obtener los nombres de los directorios dentro de las carpetas "PNGtubers" y "Personalidad"
nombres_pngtuber = os.listdir("PNGtubers")
nombres_personalidad = os.listdir("Personalidad")

# Crear una etiqueta y combobox para seleccionar de la lista "PNGtuber"
etiqueta_combobox_pngtuber = tk.Label(ventana, text="Choise PNGtuber:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox_pngtuber.pack(pady=(0, 5))  # Ajuste del espaciado
combo_pngtuber = ttk.Combobox(ventana, values=nombres_pngtuber)
combo_pngtuber.set("CalyHD")
combo_pngtuber.pack(pady=5)

nombres_personalidad_limpio = [nombre.replace("system_prompt_", "").replace(".txt", "") for nombre in nombres_personalidad]

# Crear una etiqueta y combobox para seleccionar de la lista "Personalidad"
etiqueta_combobox_personalidad = tk.Label(ventana, text="Choise personality:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox_personalidad.pack(pady=(0, 5))  # Ajuste del espaciado
combo_personalidad = ttk.Combobox(ventana, values=nombres_personalidad_limpio)
combo_personalidad.set("cali")
combo_personalidad.pack(pady=5)

nombres_modelos = os.listdir("modelos")
# Crear una etiqueta y combobox para seleccionar de la lista "Personalidad"
etiqueta_combobox_modelos = tk.Label(ventana, text="Choise model", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox_modelos.pack(pady=(0, 5))  # Ajuste del espaciado
combo_modelos = ttk.Combobox(ventana, values=nombres_modelos)
combo_modelos.set("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
combo_modelos.pack(pady=5)

nombres_voz = [
    "es-PA-MargaritaNeural",
    "es-MX-DaliaNeural",
    "es-AR-ElenaNeural",
    "es-ES-ElviraNeural",
    "es-CL-CatalinaNeural",
    "es-MX-JorgeNeural",
    "es-SV-RodrigoNeural",
    "es-ES-AlvaroNeural",
    "es-NI-FedericoNeural",
    "es-VE-SebastianNeural"
]

# Crear una etiqueta y combobox para seleccionar de la lista "voz"
etiqueta_combobox_voz = tk.Label(ventana, text="Choise Voice:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox_voz.pack(pady=(0, 5))  # Ajuste del espaciado
combo_voz = ttk.Combobox(ventana, values=nombres_voz)
combo_voz.set("es-MX-DaliaNeural")
combo_voz.pack(pady=5)


# Crear una etiqueta y combobox para seleccionar de la lista "idiomas"
idioma = [
    "English",
    "Español",
    "Italian",
    "Portugués"
]
etiqueta_combobox_idioma = tk.Label(ventana, text="Choise Language:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_combobox_idioma.pack(pady=(0, 5))  # Ajuste del espaciado
combo_idioma = ttk.Combobox(ventana, values=idioma)
combo_idioma.set("Español")
combo_idioma.pack(pady=5)

# Checkbutton para "request"
request_var = tk.BooleanVar(value=False)
check_request = tk.Checkbutton(ventana, text="Request", variable=request_var, font=("Helvetica", 12), bg="#333333", fg="#FFFFFF", selectcolor="#444444")
check_request.pack(pady=5)

# Deslizador para "temp"
etiqueta_temp = tk.Label(ventana, text="Temp:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_temp.pack(pady=(10, 5))
slider_temp = tk.Scale(ventana, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg="#333333", fg="#FFFFFF", highlightbackground="#333333")
slider_temp.pack(pady=5)
slider_temp.set("0.9")

# Deslizador para "repeat_penalty"
etiqueta_repeat_penalty = tk.Label(ventana, text="Repeat Penalty:", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF")
etiqueta_repeat_penalty.pack(pady=(10, 5))
slider_repeat_penalty = tk.Scale(ventana, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg="#333333", fg="#FFFFFF", highlightbackground="#333333")
slider_repeat_penalty.pack(pady=5)
slider_repeat_penalty.set("1")

# Botón para cerrar el programa en ejecución
cerrar_py_boton = tk.Button(ventana, text="Cerrar Programa en Ejecución", font=("Helvetica", 14), bg="#FFAA00", fg="black", command=cerrar_py)
cerrar_py_boton.pack(padx=20, pady=10)
cerrar_py_boton.config(height=1)  # Ajustar la altura del botón

# Botón para cerrar la aplicación
cerrar_boton = tk.Button(ventana, text="Cerrar Aplicación", font=("Helvetica", 14), bg="#FF5555", fg="white", command=cerrar_todo)
cerrar_boton.pack(padx=20, pady=10)
cerrar_boton.config(height=1)  # Ajustar la altura del botón

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
