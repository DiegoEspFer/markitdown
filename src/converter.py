import os
import re
import pdfplumber


def _limpiar_texto(texto: str) -> str:
    if not texto:
        return ""
    lineas = [re.sub(r'[ \t]+', ' ', l.strip()) for l in texto.split('\n') if l.strip()]
    return ' '.join(lineas)


def _matriz_a_markdown(matriz: list) -> str:
    if not matriz:
        return ""

    num_cols = max(len(fila) for fila in matriz)
    cleaned = []
    for fila in matriz:
        celdas = [str(c or "").strip().replace("\n", " ") for c in fila]
        while len(celdas) < num_cols:
            celdas.append("")
        cleaned.append(celdas)

    encabezado = cleaned[0]
    separador = ["---"] * num_cols
    filas = cleaned[1:]

    lineas = ["| " + " | ".join(encabezado) + " |",
              "| " + " | ".join(separador) + " |"]
    for fila in filas:
        if any(c for c in fila):
            lineas.append("| " + " | ".join(fila) + " |")

    return "\n".join(lineas)


def convert_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    if not file_path.lower().endswith('.pdf'):
        from markitdown import MarkItDown
        md = MarkItDown()
        return md.convert(file_path).text_content

    bloques = []

    with pdfplumber.open(file_path) as pdf:
        for pagina in pdf.pages:
            ancho = pagina.width
            alto = pagina.height
            tablas = sorted(pagina.find_tables(), key=lambda t: (t.bbox[1], t.bbox[0]))
            y_actual = 0

            for tabla in tablas:
                _, top, _, bottom = tabla.bbox

                if top > (y_actual + 0.5):
                    texto = pagina.crop((0, y_actual, ancho, top)).extract_text()
                    if texto:
                        limpio = _limpiar_texto(texto)
                        if limpio:
                            bloques.append(limpio)

                matriz = tabla.extract()
                if matriz:
                    md_tabla = _matriz_a_markdown(matriz)
                    if md_tabla:
                        bloques.append(md_tabla)

                y_actual = max(y_actual, bottom)

            if y_actual < (alto - 0.5):
                texto = pagina.crop((0, y_actual, ancho, alto)).extract_text()
                if texto:
                    limpio = _limpiar_texto(texto)
                    if limpio:
                        bloques.append(limpio)

    return "\n\n".join(bloques)