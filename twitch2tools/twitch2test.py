import os
import time
import argparse  # Importar el módulo argparse
from twitchchatreader import TwitchChatReader
from twitchchatreaderevents import CommentEvent, ConnectEvent

global texto
texto = ""
update_counter = 0
user_comments = {}
last_update_time = time.time()

def save_to_file(text):
    with open("messages.txt", "w") as file:
        file.write(text + "\n")

def on_comment_handler(event: CommentEvent):
    global texto, update_counter, last_update_time

    user = event.user.name
    comment = event.comment
    new_text = user + " dice: " + comment

    if comment:
        update_counter += 1

        if update_counter <= 5:
            texto = texto + new_text + "\n"

        if update_counter >= 5 or (time.time() - last_update_time) >= 10:
            print(texto)
            save_to_file(texto)
            update_counter = 0
            last_update_time = time.time()
            texto = ""

if __name__ == "__main__":
    # Configurar argparse para manejar los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description="Twitch Chat Reader")
    parser.add_argument("channel", type=str, help="Nombre del canal de Twitch")
    args = parser.parse_args()

    # Utilizar el nombre del canal proporcionado como argumento
    twitch_reader = TwitchChatReader(args.channel)

    @twitch_reader.on("comment")
    def on_comment(event: CommentEvent):
        on_comment_handler(event)

    @twitch_reader.on("connect")
    def on_connect(event: ConnectEvent):
        print("Connection established!")

    while True:
        pass  # Mantener el bucle principal funcionando para escuchar el chat de Twitch
