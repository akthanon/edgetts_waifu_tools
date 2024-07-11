@echo off
setlocal

rem Verificar si el programa principal está presente
if not exist edgettstools\interfaz.py (
    echo El archivo interfaz.py no está presente en el directorio actual. Por favor, asegúrese de que el archivo esté presente y vuelva a ejecutar este script.
    pause
    goto :end
)

rem Activar el entorno virtual
call venv\Scripts\activate

rem Ejecutar el programa
cd edgettstools
python interfaz.py
cd ..

rem Desactivar el entorno virtual
deactivate

:end
