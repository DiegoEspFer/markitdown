@echo off
:: Navega a la carpeta del script (por seguridad)
cd /d %~dp0

echo Verificando entorno virtual...
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
)

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Instalando dependencias...
:: Usar la ruta directa asegura que se instale dentro de este entorno
.venv\Scripts\python.exe -m pip install -r requirements.txt

echo Ejecutando la aplicacion Streamlit...
.venv\Scripts\streamlit.exe run app.py

pause