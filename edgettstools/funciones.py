import pytz
import requests
from datetime import datetime
from googlesearch import search
from youtube_dl import YoutubeDL

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
