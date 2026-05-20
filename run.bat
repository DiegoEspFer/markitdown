@echo off
echo ==============================================
echo    Iniciando MarkItDown Converter App
echo ==============================================

cd /d "%~dp0"

REM Si borraste la carpeta venv, esta condición se cumplirá y creará el entorno correcto
IF NOT EXIST "venv\Scripts\activate" (
    echo Creando entorno virtual con Python 3.12 en "venv"...
    py -3.12 -m venv venv
)

echo.
echo Activando entorno virtual...
call venv\Scripts\activate

echo.
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

echo.
echo Ejecutando la aplicacion Streamlit...
streamlit run app.py

pause