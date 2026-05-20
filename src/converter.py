"""
Módulo encargado de la lógica central de conversión de archivos.
Utiliza la biblioteca markitdown de Microsoft.
"""
from markitdown import MarkItDown

def convert_file(file_path: str) -> str:
    """
    Convierte un archivo a formato Markdown utilizando MarkItDown.
    
    Args:
        file_path (str): Ruta absoluta o relativa del archivo a convertir.
        
    Returns:
        str: El contenido del archivo convertido en formato Markdown.
        
    Raises:
        Exception: Si ocurre un error durante el procesamiento con MarkItDown.
    """
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content