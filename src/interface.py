"""
Módulo que define los componentes modulares de la interfaz de usuario en Streamlit,
adaptado visualmente a los lineamientos del HIC y diseño minimalista.
"""
import streamlit as st
import os
from pathlib import Path
from typing import Tuple, List, Any
from .file_manager import SUPPORTED_EXTENSIONS 

def inject_hic_styling() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 1rem !important;
            max-width: 48rem !important;
        }
        
        header { display: none !important; } 
        #MainMenu { visibility: hidden; }
        .stApp { background-color: #F8F9FA; }
        
        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed #A0B3C6 !important;
            border-radius: 12px !important;
            background-color: #FFFFFF !important;
            padding: 3.5rem 1rem !important;
        }
        
        button[kind="primary"] {
            background-color: #004B87 !important;
            border-color: #004B87 !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            padding: 0.6rem 2rem !important;
        }
        button[kind="primary"]:hover {
            background-color: #00335C !important;
            border-color: #00335C !important;
        }
        
        .hic-title {
            color: #004B87 !important; 
            font-size: 2.9rem !important; 
            font-weight: 700 !important; 
            margin: 0px !important; 
            padding: 0px !important;
            line-height: 1.1;
        }

        .custom-warning-box {
            margin-top: 10px !important;
            padding: 12px 16px !important; 
            border: 1px solid #FFEBAA !important; 
            background-color: #FFF8E1 !important; 
            border-radius: 8px !important;
            width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_header() -> None:
    inject_hic_styling()
    
    logo_filename = None
    for ext in [".png", ".jpg", ".jpeg", ".svg"]:
        test_path = Path("LOGO-HIC" + ext)
        if test_path.exists():
            logo_filename = str(test_path)
            break

    if logo_filename:
        col_logo, col_title = st.columns([1.6, 5], vertical_alignment="center")
        with col_logo:
            st.image(logo_filename, use_container_width=True)
        with col_title:
            st.markdown("<h1 class='hic-title'>Conversor Markdown</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 class='hic-title'>Conversor Markdown</h1>", unsafe_allow_html=True)

def render_input_section() -> List[Any]:
    with st.container(border=True):
        uploaded_files = st.file_uploader(
            "Arrastra archivos o carpetas aquí", 
            accept_multiple_files=True,
            type=None, 
            label_visibility="collapsed"
        )
        
    doc_files_detected = []
    unknown_files_detected = []
    valid_files = []
    
    base_supported = [ext.lower() for ext in SUPPORTED_EXTENSIONS]
    
    for uf in uploaded_files:
        ext = os.path.splitext(uf.name)[1].lower()
        if ext == '.doc':
            doc_files_detected.append(uf.name)
        elif ext in base_supported:
            valid_files.append(uf)
        else:
            unknown_files_detected.append((uf.name, ext if ext else "sin extensión"))

    if doc_files_detected or unknown_files_detected:
        html_content = "<div class='custom-warning-box'>"
        
        if doc_files_detected:
            html_content += f"""
            <p style="color: #B78103; font-size: 0.9rem; margin: 0 0 6px 0; font-weight: 500; line-height: 1.4;">
                ⚠️ <strong>Nota del sistema (.doc):</strong> El archivo antiguo de Word <code>{", ".join(doc_files_detected)}</code> no es compatible de forma nativa. Por favor, guárdelo como <strong>.docx</strong> antes de subirlo.
            </p>
            """
        
        if unknown_files_detected:
            for name, ext_name in unknown_files_detected:
                html_content += f"""
                <p style="color: #D32F2F; font-size: 0.9rem; margin: 0 0 6px 0; font-weight: 500; line-height: 1.4;">
                    🚫 <strong>Formato no admitido:</strong> El archivo <code>{name}</code> tiene un formato no compatible (<code>{ext_name}</code>) y será omitido en la conversión.
                </p>
                """
        
        html_content += "</div>"
        st.markdown(html_content, unsafe_allow_html=True)

    return valid_files

def render_conversion_status(total_files: int) -> Tuple[Any, Any]:
    progress_bar = st.progress(0.0)
    status_text = st.empty()
    return progress_bar, status_text

def render_token_metrics(file_name: str, original_tokens: int, markdown_tokens: int) -> None:
    """
    Renderiza el reporte de tokens en formato de columnas para la parte inferior de la app.
    """
    st.markdown(f"**Archivo:** `{file_name}`")
    
    diferencia = original_tokens - markdown_tokens
    porcentaje_optimizado = (diferencia / original_tokens) * 100 if original_tokens > 0 else 0.0
    
    col1, col2, col3 = st.columns(3)
    
    # Cambio de etiqueta para reflejar la nueva lógica de archivo crudo
    col1.metric(label="Tokens Archivo Original (Crudo)", value=f"{original_tokens:,}")
    col2.metric(label="Tokens Markdown", value=f"{markdown_tokens:,}")
    
    if diferencia >= 0:
        col3.metric(label="Optimización (Ahorro)", value=f"{diferencia:,}", delta=f"{porcentaje_optimizado:.1f}% Menos")
    else:
        col3.metric(label="Estructura Markdown (Aumento)", value=f"{abs(diferencia):,}", delta=f"{abs(porcentaje_optimizado):.1f}% Más", delta_color="inverse")
        
    st.markdown("---")