# edgettstools
EDGETTS WAIFU TOOLS Kit de códigos para interactuar con IAs a través de la voz utilizando EDGE-TTS, la interfáz gráfica está diseñada para facilitar la ejecución de varios scripts de Python que interactúan con Twitch y otras herramientas relacionadas. La interfaz permite seleccionar diferentes configuraciones y ejecutar scripts con los argumentos adecuados.

los códigos para el chat de twitch fueron modificados de:
https://github.com/nomic-ai/gpt4all/blob/main/gpt4all-bindings/cli/app.py

## Programas

only_twitch_games: interfaz para ejecutar juegos que se juegan solos

voice_to_edgetts: voz a edge-tts

talk_with_txt_waifu: habla con una waifu en ascii

talk_with_Vtuber: habla con una Vtuber en PNG

twitch_to_txt_waifu: transmite interacciones del chat de twitch con tu waifu ASCII

twitch_to_vtuber: transmite interacciones del chat de twitch con tu waifu PNG

p_twitch_voice: escucha lo que dice la gente en el chat

twitch_to_Vtuber_games: transmite interacciones del chat de twitch con tu waifu PNG mientras ella juega videojuegos

# archivos necesarios
zona en construcción...
por el momento se necesitan descargar todas las librerías manualmente
también se necesitan descargar manualmente y tener en el directorio principal ffmpeg, ffplay y ffprobe para la interfáz gráfica

# DESCRIPCION BASICA

**Ejecución de Scripts**: Ejecuta varios scripts de Python con diferentes argumentos seleccionables desde la interfaz.
**Control de Procesos**: Verifica si el proceso en ejecución ha terminado y permite cerrarlo junto con sus subprocesos.
**Interfaz Amigable**: Ofrece una interfaz gráfica intuitiva y fácil de usar.

Ecosistema: GPT4ALL

Modelo utilizado: Llama 3 Instruct

Lenguaje principal: Python

Librerías principales: Pygame(Movimientos del personaje), edge-tts (Voz del personaje)

Librerias secundarias: subprocess, os, tempfile, pathlib, importlib.metadata, io, sys, collections, typing_extensions, typer, random, time, re, wave, numpy, threading, pydub, shutil, argparse

Codigos externos principales: Twitch-Chat-Reader (Interacción con Twitch), GPT4All CLI (Interacción los modelos)

Programas .exe: ffmpeg, ffplay, ffprobe


# Funcionalidades

Ejecución de Scripts

La aplicación permite ejecutar scripts Python con argumentos específicos seleccionados a través de la interfaz. Los argumentos se configuran automáticamente según el script seleccionado.
