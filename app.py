import os
import streamlit as st
from src.security import apply as _apply_security
_apply_security()
import base64
import tiktoken 

from src.interface import (
    render_header, 
    render_input_section, 
    render_conversion_status,
    render_token_metrics  
)
from src.file_manager import save_uploaded_files, cleanup_temp_dir, create_zip_archive
from src.converter import convert_file

st.set_page_config(
    page_title="MarkItDown App", 
    page_icon="📄", 
    layout="centered"
)

def get_original_tokens_estimate(file_path: str, ext: str, md_content: str, encoding) -> int:
    """
    Calcula el peso original en tokens.
    Para texto puro, hace un conteo exacto.
    Para archivos binarios (PDF, DOCX, etc.), usa la heurística estándar de la industria:
    1 token ≈ 4 bytes de tamaño de archivo.
    """
    try:
        # Para archivos de texto puro, el conteo es exacto
        if ext in ['.txt', '.csv', '.json']:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return len(encoding.encode(f.read()))
        
        # Para binarios, aplicamos la regla de 1 token ≈ 4 bytes
        file_size_bytes = os.path.getsize(file_path)
        return int(file_size_bytes / 4)
        
    except Exception:
        # Fallback en caso de error de lectura
        return len(encoding.encode(md_content))

def trigger_multiple_downloads(files_list):
    js_code = "<script>"
    for idx, file in enumerate(files_list):
        b64_content = base64.b64encode(file['content'].encode('utf-8')).decode('utf-8')
        file_name = file['name']
        
        js_code += f"""
        setTimeout(() => {{
            const link_{idx} = document.createElement('a');
            link_{idx}.href = 'data:text/markdown;base64,{b64_content}';
            link_{idx}.download = '{file_name}';
            document.body.appendChild(link_{idx});
            link_{idx}.click();
            document.body.removeChild(link_{idx});
        }}, {idx * 250});
        """
    js_code += "</script>"
    st.components.v1.html(js_code, height=0, width=0)

def main():
    if "processed" not in st.session_state:
        st.session_state.processed = False
        st.session_state.zip_data = None
        st.session_state.files = []

    render_header()
    uploaded_files = render_input_section()
    
    if not uploaded_files and st.session_state.processed:
        st.session_state.processed = False
        st.session_state.zip_data = None
        st.session_state.files = []
        st.rerun()

    success_placeholder = st.empty()

    if st.button("Iniciar Conversión", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("⚠️ No hay archivos válidos cargados o listos para procesar.")
            return
            
        temp_dir, files_to_process = save_uploaded_files(uploaded_files)
        total_files = len(files_to_process)
        
        progress_bar, status_text = render_conversion_status(total_files)
        converted_files = []
        
        # Instanciamos el tokenizador de OpenAI (GPT-4 / GPT-3.5)
        tokenizer = tiktoken.get_encoding("cl100k_base")
        
        for i, file_path in enumerate(files_to_process):
            file_name = os.path.basename(file_path)
            ext = os.path.splitext(file_name)[1].lower()
            status_text.markdown(f"**Procesando ({i+1}/{total_files}):** `{file_name}`")
            
            try:
                md_content = convert_file(file_path)
                
                orig_tokens = get_original_tokens_estimate(file_path, ext, md_content, tokenizer)
                md_tokens = len(tokenizer.encode(md_content))
                
                converted_files.append({
                    "name": f"{os.path.splitext(file_name)[0]}.md",
                    "content": md_content,
                    "orig_tokens": orig_tokens,
                    "md_tokens": md_tokens
                })
            except Exception as e:
                st.toast(f"Error procesando {file_name}: {e}", icon="❌")
            
            progress_bar.progress((i + 1) / total_files)
            
        if temp_dir:
            cleanup_temp_dir(temp_dir)
            
        status_text.empty()
        progress_bar.empty()
        
        if converted_files:
            st.session_state.processed = True
            st.session_state.files = converted_files
            st.session_state.zip_data = create_zip_archive(converted_files)
            st.rerun()

    if st.session_state.processed:
        success_placeholder.success("¡Proceso de conversión finalizado!")
        
    st.write("") 

    # --- BOTONES DE DESCARGA ---
    c1, c2 = st.columns(2)
    
    with c1:
        if st.session_state.processed:
            st.download_button(
                label="📁 Markdown (.ZIP)",
                data=st.session_state.zip_data,
                file_name="HIC_markdown_procesados.zip",
                mime="application/zip",
                use_container_width=True
            )
        else:
            st.button("📁 Markdown (.ZIP)", disabled=True, use_container_width=True)
            
    with c2:
        if st.session_state.processed:
            if st.button("⬇️ Markdown (.md)", use_container_width=True):
                trigger_multiple_downloads(st.session_state.files)
                st.toast("Descargando todos los archivos individualmente...", icon="📥")
        else:
            st.button("⬇️ Markdown (.md)", disabled=True, use_container_width=True)

    # --- REPORTE DE TOKENS EN LA PARTE INFERIOR ---
    if st.session_state.processed:
        st.write("")
        st.write("")
        st.markdown("<h3 style='color: #004B87;'>Reporte de Tokens</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        for file_info in st.session_state.files:
            render_token_metrics(
                file_name=file_info["name"],
                original_tokens=file_info["orig_tokens"],
                markdown_tokens=file_info["md_tokens"]
            )

if __name__ == "__main__":
    main()