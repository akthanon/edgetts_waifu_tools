import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pytz
import requests
from datetime import datetime
from googlesearch import search
from youtube_dl import YoutubeDL
import pyautogui
from gpt4all import GPT4All
import re

def ejecutar_funcion(funcion):
    funciones_permitidas = {
        'google_search': google_search,
        'get_local_time': get_local_time,
        'get_current_time': get_current_time,
        'get_current_date': get_current_date,
        'get_weather': get_weather,
        'kilometers_to_miles': kilometers_to_miles,
        'youtube_search': youtube_search,
        'play_music': play_music,
        'hackear_nasa': hackear_nasa,
        "describe_image": describe_image,
    }
    
    # Comprobar si la función está en el formato esperado
    if '(' not in funcion or ')' not in funcion:
        return "XNAX"
    
    # Extraer el nombre de la función y el argumento de la cadena
    nombre_funcion = funcion.split('(')[0]
    argumento = funcion.split('(')[1].split(')')[0].strip("'")
    
    if nombre_funcion in funciones_permitidas:
        resultado = funciones_permitidas[nombre_funcion](argumento)
        return resultado
    else:
        return "XNAX."

def get_local_time(city_name):
    try:
        tz = pytz.timezone('America/Mexico_City')  # Cambia esto según la ciudad
        local_time = datetime.now(tz).strftime('%H:%M:%S')
        return local_time
    except Exception as e:
        return {"error": str(e)}

def get_current_time(a):
    return datetime.now().strftime("%H:%M:%S")

def get_current_date(a):
    return datetime.now().strftime("%Y-%m-%d")

def get_weather(city_name):
    try:
        # Tu código para obtener el clima
        return {"weather": "Soleado"}  # Reemplaza con la lógica real
    except Exception as e:
        return {"error": str(e)}

def kilometers_to_miles(km):
    return km * 0.621371

from googlesearch import search
import requests
from bs4 import BeautifulSoup

def google_search(query):
    try:
        results = search(query, num_results=1, lang='es')  # Ajuste para obtener hasta 5 resultados en español
        formatted_results = []
        for url in results:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else 'No title'
                description_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
                description = description_tag['content'] if description_tag else 'No description'
                formatted_results.append({
                    "title": title,
                    "url": url,
                    "description": description
                })
            except Exception as e:
                formatted_results.append({
                    "error": str(e)
                })
        return {"results": formatted_results}
    except Exception as e:
        return {"error": str(e)}

def youtube_search(query):
    try:
        options = {
            'format': 'bestaudio/best',
            'quiet': True,
        }
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            video_url = info['entries'][0]['formats'][0]['url']
            return video_url
    except Exception as e:
        return {"error": str(e)}

def play_music(query):
    try:
        options = {
            'format': 'bestaudio/best',
            'quiet': True,
        }
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            url = info['entries'][0]['formats'][0]['url']
            return url
    except Exception as e:
        return {"error": str(e)}

def hackear_nasa(a):
    return "NASA HACKEADA"


# Ciclo infinito para tomar capturas cada interval_seconds segundos
def describe_image(a):
        # Función para generar prompts basados en la imagen
    def image_to_prompt(image, mode, ci):
        try:
            image = image.convert('RGB')
            if mode == 'best':
                return ci.interrogate(image)
            elif mode == 'classic':
                return ci.interrogate_classic(image)
            elif mode == 'fast':
                return ci.interrogate_fast(image)
            elif mode == 'negative':
                return ci.interrogate_negative(image)
            else:
                return "Invalid mode selected."
        except:
            pass
    filename = f"image.png" 
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    from clip_interrogator import Config, Interrogator
    from PIL import Image # type: ignore
    # Configuración inicial
    clip_model_name = 'ViT-L-14/openai'

    # Configurar el interrogador CLIP
    config = Config(
        clip_model_name=clip_model_name,
    )
    config.apply_low_vram_defaults()

    ci = Interrogator(config)

    ci.config.clip_model_name = clip_model_name
    ci.load_clip_model()
    # Cargar la imagen
    image_path = 'image.png'
    image = Image.open(image_path)
    mode = 'fast'  # Puedes cambiar el modo según tus necesidades ('best', 'classic', 'fast', 'negative')
    prompt_generated = image_to_prompt(image, mode, ci)
    return prompt_generated

def load_modela(
    model: str = "qwen2-7b-instruct-q2_k.gguf",
    n_threads: int = None,
    device: str = "cpu"
):
    """The CLI read-eval-print loop."""
    gpt4all_instance = GPT4All(model, device=device, n_ctx=1024, model_path="modelos")

    # Configure number of threads if specified
    if n_threads is not None:
        gpt4all_instance.model.set_thread_count(n_threads)

    return gpt4all_instance

def ejecutar_modeloa(gpt4all_instance, message):
    resultado=""
    system_prompt = """You are a natural language model to functions converter. Translate the request from natural language to functions from the following list. if the message is not in the list then a "NA" is returned:
        get_local_time(city_name) < get local time
        get_weather(city_name) < get weather
        get_current_time() < get current time
        get_current_date() < get current date
        kilometers_to_miles() < convert kilometers to miles
        google_search(query) < google search
        hackear_nasa() < hackea la nasa
        describe_image() < describe what is happening in an image/describe what is on the screen
        """
    with gpt4all_instance.chat_session(system_prompt):
        response_generator = gpt4all_instance.generate(
            message,
            max_tokens=30,
            temp=0.4,
            top_k=40,
            top_p=0.9,
            min_p=0.0,
            repeat_penalty=1,
            repeat_last_n=64,
            n_batch=9,
            streaming=True,
        )
        respuesta = ""
        for token in response_generator:
            respuesta += token
        
        print(respuesta)
        # Execute function based on generated response
        if respuesta.strip():
            resultado = ejecutar_funcion(respuesta.strip())
        else:
            print("XNAX")
        return str(resultado)

# Función para determinar si una petición general
def es_peticion(frase):
    # Expresión regular para identificar palabras que suelen indicar petición
    patron_peticion = r'\b(quiero|necesito|deseo|por favor|podrías|me podrías|puedes|me gustaría|haz|dime|dame)\b'

    # Buscar coincidencias en la frase
    return bool(re.search(patron_peticion, frase, re.IGNORECASE))

# Función para determinar si una petición está relacionada con alguna función específica
def peticion_relacionada(frase):
    # Lista de funciones y sus descripciones
    funciones = {
        get_local_time: ["get local time", "hora local"],
        get_weather: ["get weather", "clima","temperatura"],
        get_current_time: ["get current time", "hora actual"],
        get_current_date: ["get current date", "fecha actual"],
        kilometers_to_miles: ["convert kilometers to miles", "kilómetros a millas"],
        google_search: ["google search", "buscar en google","busqueda","google"],
        hackear_nasa: ["hackear nasa", "hackear la nasa"],
        describe_image: ["describe image", "describe what is happening in an image", "describe what is on the screen","imagen","pantalla"]
    }

    # Verificar si es una petición general
    if es_peticion(frase):
        for funcion, descripciones in funciones.items():
            for desc in descripciones:
                if desc in frase.lower():
                    return True, funcion
        # Si ninguna descripción coincide con la frase, no es una petición relacionada
        return True, None
    else:
        return False, None

# Función que determina si una frase contiene una petición
def peticiones(frase):
    es_pet, funcion = peticion_relacionada(frase)
    if es_pet and funcion:
        return True
    else:
        return False