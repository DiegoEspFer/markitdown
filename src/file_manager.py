"""
Módulo de utilidades para manejo de archivos, directorios y archivos temporales.
"""
import os
import tempfile
import shutil
import zipfile
import io
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Extensiones comúnmente soportadas por herramientas de extracción de texto y MarkItDown
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.pptx', '.html', '.txt', '.csv', '.json', '.xml'}

def save_uploaded_files(uploaded_files: List[Any]) -> Tuple[str, List[str]]:
    """
    Guarda los archivos subidos a través de Streamlit en un directorio temporal.
    
    Args:
        uploaded_files: Lista de objetos UploadedFile de Streamlit.
        
    Returns:
        Tuple[str, List[str]]: Una tupla que contiene:
            - La ruta al directorio temporal creado.
            - Una lista de rutas absolutas de los archivos guardados.
    """
    temp_dir = tempfile.mkdtemp()
    saved_paths = []
    
    for uf in uploaded_files:
        file_path = os.path.join(temp_dir, uf.name)
        with open(file_path, "wb") as f:
            f.write(uf.getbuffer())
        saved_paths.append(file_path)
        
    return temp_dir, saved_paths

def scan_directory(dir_path: str) -> List[str]:
    """
    Escanea un directorio local en busca de archivos compatibles.
    
    Args:
        dir_path (str): Ruta al directorio local.
        
    Returns:
        List[str]: Lista de rutas absolutas a los archivos encontrados.
    """
    found_files = []
    path = Path(dir_path)
    
    if path.is_dir():
        for file in path.rglob("*"):
            if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
                found_files.append(str(file.absolute()))
                
    return found_files

def cleanup_temp_dir(temp_dir: str) -> None:
    """
    Elimina el directorio temporal y todo su contenido.
    
    Args:
        temp_dir (str): Ruta al directorio temporal.
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

def create_zip_archive(files_data: List[Dict[str, str]]) -> bytes:
    """
    Crea un archivo ZIP en memoria que contiene todos los archivos convertidos.
    
    Args:
        files_data: Lista de diccionarios con formato {'name': 'nombre.md', 'content': '...'}
        
    Returns:
        bytes: Datos binarios del archivo ZIP.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_data in files_data:
            zip_file.writestr(file_data['name'], file_data['content'])
            
    return zip_buffer.getvalue()
