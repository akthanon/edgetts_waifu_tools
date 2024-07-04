#!/usr/bin/env python3
import typer
from gpt4all import GPT4All
from funciones import *

app = typer.Typer()

@app.command()
def repl(
    message: str,
    model: str = "qwen2-7b-instruct-q2_k.gguf",
    n_threads: int = 12,
    device: str = "cpu"
):
    """The CLI read-eval-print loop."""
    gpt4all_instance = GPT4All(model, device=device, n_ctx=1024, model_path="modelos")

    # Configure number of threads if specified
    if n_threads is not None:
        num_threads = gpt4all_instance.model.thread_count()
        gpt4all_instance.model.set_thread_count(n_threads)
        num_threads = gpt4all_instance.model.thread_count()

    ejecutar_modelo(gpt4all_instance, message)

def ejecutar_modelo(gpt4all_instance, message):
    system_prompt = """You are a natural language model to functions converter. Translate the request from natural language to functions from the following list. if the message is not in the list then a "NA" is returned:
        get_local_time(city_name) < get local time
        get_weather(city_name) < get weather
        get_current_time() < get current time
        get_current_date() < get current date
        kilometers_to_miles() < convert kilometers to miles
        google_search(query) < google search
        hackear_nasa() < hackea la nasa
        """
    with gpt4all_instance.chat_session(system_prompt):
        response_generator = gpt4all_instance.generate(
            message,
            max_tokens=50,
            temp=0.1,
            top_k=40,
            top_p=0.9,
            min_p=0.0,
            repeat_penalty=1,
            repeat_last_n=64,
            n_batch=9,
            streaming=False,
        )
        respuesta = ""
        for token in response_generator:
            respuesta += token
        
        print(respuesta)
        # Execute function based on generated response
        if respuesta.strip():
            resultado = ejecutar_funcion(respuesta.strip())
            print(resultado)
        else:
            print("XNAX")

if __name__ == "__main__":
    app()
