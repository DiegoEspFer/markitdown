import os
import re
import pdfplumber
from collections import Counter


def _tamaño_cuerpo(pdf) -> float:
    sizes = []
    for pagina in pdf.pages:
        for char in pagina.chars:
            s = char.get('size')
            if s and s > 4:
                sizes.append(round(s, 1))
    if not sizes:
        return 10.0
    return Counter(sizes).most_common(1)[0][0]


def _agrupar_palabras_en_lineas(words, tolerancia=3):
    if not words:
        return []
    words_sorted = sorted(words, key=lambda w: (w['top'], w['x0']))
    lineas = []
    linea_actual = [words_sorted[0]]
    for word in words_sorted[1:]:
        if abs(word['top'] - linea_actual[0]['top']) <= tolerancia:
            linea_actual.append(word)
        else:
            lineas.append(linea_actual)
            linea_actual = [word]
    lineas.append(linea_actual)
    return lineas


def _es_negrita(fontname: str) -> bool:
    fn = fontname.lower()
    return any(k in fn for k in ('bold', ',bd', '-bd', 'heavy', 'black', 'demi'))


def _nivel_heading(size: float, body_size: float, bold: bool, texto: str) -> int:
    ratio = size / body_size if body_size > 0 else 1.0
    if ratio >= 1.5:
        return 1
    if ratio >= 1.2 or (bold and ratio >= 1.1):
        return 2
    if bold and len(texto) < 100:
        return 3
    return 0


def _formatear_linea(texto: str, size: float, body_size: float, fontname: str):
    """Retorna (texto_md, tipo): tipo >0 = heading, -1 = lista, 0 = párrafo."""
    texto = re.sub(r'[ \t]+', ' ', texto).strip()
    if not texto:
        return None, 0

    if re.match(r'^[•·▪▸►]\s*', texto):
        return '- ' + re.sub(r'^[•·▪▸►]\s*', '', texto), -1
    if re.match(r'^\d+[\.\)]\s+\S', texto):
        return texto, -1

    bold = _es_negrita(fontname)
    nivel = _nivel_heading(size, body_size, bold, texto)
    if nivel:
        return f'{"#" * nivel} {texto}', nivel
    return texto, 0


def _extraer_bloques_formateados(pagina, bbox, body_size: float) -> str:
    crop = pagina.crop(bbox)

    # extract_words calcula correctamente los espacios entre palabras
    # y permite incluir atributos de fuente por palabra
    words = crop.extract_words(
        extra_attrs=['size', 'fontname'],
        keep_blank_chars=False,
        x_tolerance=3,
        y_tolerance=3,
    )
    if not words:
        return ''

    lineas_words = _agrupar_palabras_en_lineas(words)

    # Construir objetos de línea con texto, estilo y posición
    lineas = []
    for grupo in lineas_words:
        ws = sorted(grupo, key=lambda w: w['x0'])
        texto = ' '.join(w['text'] for w in ws)
        texto = re.sub(r'[ \t]+', ' ', texto).strip()
        if not texto:
            continue

        size = max((w.get('size') or body_size) for w in ws)
        fontname = next((w.get('fontname', '') for w in ws if w.get('fontname')), '')
        top = ws[0].get('top', 0)
        bottom = max(w.get('bottom', top + (size or body_size)) for w in ws)

        md, tipo = _formatear_linea(texto, size, body_size, fontname)
        if md:
            lineas.append({'md': md, 'tipo': tipo, 'top': top, 'bottom': bottom})

    if not lineas:
        return ''

    # Calcular umbral de salto de párrafo: gap mayor al doble del interlineado típico
    gaps = [lineas[i + 1]['top'] - lineas[i]['bottom'] for i in range(len(lineas) - 1)]
    gap_tipico = sorted(gaps)[len(gaps) // 2] if gaps else 2
    umbral_parrafo = max(gap_tipico * 2, gap_tipico + 4)

    bloques = []
    parrafo = []
    prev_bottom = None

    for linea in lineas:
        if linea['tipo'] == 0:
            # Salto de párrafo real si el gap vertical es mayor al umbral
            if prev_bottom is not None and (linea['top'] - prev_bottom) > umbral_parrafo:
                if parrafo:
                    bloques.append(' '.join(parrafo))
                    parrafo = []
            parrafo.append(linea['md'])
        else:
            if parrafo:
                bloques.append(' '.join(parrafo))
                parrafo = []
            bloques.append(linea['md'])
        prev_bottom = linea['bottom']

    if parrafo:
        bloques.append(' '.join(parrafo))

    return '\n\n'.join(bloques)


def _matriz_a_markdown(matriz: list) -> str:
    if not matriz:
        return ''
    num_cols = max(len(fila) for fila in matriz)
    cleaned = []
    for fila in matriz:
        celdas = [str(c or '').strip().replace('\n', ' ') for c in fila]
        while len(celdas) < num_cols:
            celdas.append('')
        cleaned.append(celdas)

    lineas = [
        '| ' + ' | '.join(cleaned[0]) + ' |',
        '| ' + ' | '.join(['---'] * num_cols) + ' |',
    ]
    for fila in cleaned[1:]:
        if any(c for c in fila):
            lineas.append('| ' + ' | '.join(fila) + ' |')

    return '\n'.join(lineas)


def convert_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'No se encontró el archivo: {file_path}')

    if not file_path.lower().endswith('.pdf'):
        from markitdown import MarkItDown
        return MarkItDown().convert(file_path).text_content

    bloques = []

    with pdfplumber.open(file_path) as pdf:
        body_size = _tamaño_cuerpo(pdf)

        for pagina in pdf.pages:
            ancho = pagina.width
            alto = pagina.height
            tablas = sorted(pagina.find_tables(), key=lambda t: (t.bbox[1], t.bbox[0]))
            y_actual = 0

            for tabla in tablas:
                _, top, _, bottom = tabla.bbox

                if top > (y_actual + 0.5):
                    bloque = _extraer_bloques_formateados(
                        pagina, (0, y_actual, ancho, top), body_size
                    )
                    if bloque:
                        bloques.append(bloque)

                md_tabla = _matriz_a_markdown(tabla.extract() or [])
                if md_tabla:
                    bloques.append(md_tabla)

                y_actual = max(y_actual, bottom)

            if y_actual < (alto - 0.5):
                bloque = _extraer_bloques_formateados(
                    pagina, (0, y_actual, ancho, alto), body_size
                )
                if bloque:
                    bloques.append(bloque)

    return '\n\n'.join(bloques)
