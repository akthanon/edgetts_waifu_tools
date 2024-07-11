@echo off
setlocal

rem Verificar si Python está instalado y obtener la ubicación del ejecutable
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no está instalado o no se puede encontrar en la ruta del sistema. Favor de instalar Python y añadirlo a la variable de entorno PATH.
    pause
    goto :end
)
set PYTHON_EXECUTABLE=python

rem Verificar si pip está instalado
%PYTHON_EXECUTABLE% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    rem Verificar si curl está instalado
    curl --version >nul 2>&1
    if %errorlevel% equ 0 (
        rem Utilizar curl si está instalado
        set DOWNLOADER=curl
    ) else (
        rem Verificar si wget está instalado
        wget --version >nul 2>&1
        if %errorlevel% equ 0 (
            rem Utilizar wget si está instalado
            set DOWNLOADER=wget
        ) else (
            echo Curl o Wget no están instalados. Favor de descargar Curl, Wget o pip manualmente y luego instalar pip.
            pause
            goto :end
        )
    )
    echo Pip no está instalado. Descargando e instalando pip...
    %DOWNLOADER% https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    %PYTHON_EXECUTABLE% get-pip.py
    pause
)

rem Crear un entorno virtual
%PYTHON_EXECUTABLE% -m venv venv

rem Activar el entorno virtual
call venv\Scripts\activate

rem Verificar si el archivo requirements.txt está presente
if not exist requirements.txt (
    echo El archivo requirements.txt no está presente en el directorio actual. Por favor, asegúrese de que el archivo esté presente y vuelva a ejecutar este script.
    pause
    goto :end
)

rem Obtener lista de bibliotecas instaladas
pip freeze > installed_libs.txt

rem Leer el archivo requirements.txt línea por línea y comprobar e instalar las bibliotecas
for /f "delims=" %%i in (requirements.txt) do (
    findstr /i "\<%%i\>" installed_libs.txt > nul
    if errorlevel 1 (
        echo Instalando %%i...
        pip install %%i
    ) else (
        echo %%i ya está instalado.
    )
)

rem Eliminar el archivo temporal
del installed_libs.txt

rem Verificar si los archivos ffmpeg.exe, ffplay.exe y ffprobe.exe están presentes en la ruta edgettstools\
if not exist edgettstools\ffmpeg.exe (
    echo ffmpeg.exe no está presente en la ruta edgettstools\.
    set DOWNLOAD_FILES=true
)

if not exist edgettstools\ffplay.exe (
    echo ffplay.exe no está presente en la ruta edgettstools\.
    set DOWNLOAD_FILES=true
)

if not exist edgettstools\ffprobe.exe (
    echo ffprobe.exe no está presente en la ruta edgettstools\.
    set DOWNLOAD_FILES=true
)

if "%DOWNLOAD_FILES%"=="true" (
    echo Descargando archivos...
    curl -OJL https://github.com/GyanD/codexffmpeg/releases/download/7.0.1/ffmpeg-7.0.1-essentials_build.zip
    rem Descomprimir el archivo zip
    tar -xf ffmpeg-7.0.1-essentials_build.zip 
    rem Copiar todo el contenido de la carpeta bin a la carpeta edgettstools
    xcopy /s /e /i ffmpeg-7.0.1-essentials_build\bin\* edgettstools\
    del ffmpeg-7.0.1-essentials_build.zip
    rmdir /s /q ffmpeg-7.0.1-essentials_build
)

echo INSTALACION EXITOSA
pause
rem Desactivar el entorno virtual
deactivate
:end

