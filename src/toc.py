import pdfplumber  # Importa la librería pdfplumber, que sirve para extraer texto de archivos PDF
from outline_parser import parse_outline, clean_title

def extract_pages_text(pdf_path):
    """
    Devuelve una lista con el texto extraído de cada página de un PDF.

    Args:
        pdf_path (str): Ruta al archivo PDF que quieres procesar.

    Returns:
        list[str]: Una lista donde cada elemento es el texto completo de una página del PDF.
    """
    pages_text = []  # Aquí se guardarán los textos de cada página

    # Abre el PDF usando pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        # Recorre todas las páginas del PDF
        for page in pdf.pages:
            # Extrae el texto de la página; si no hay texto, usa string vacío ("")
            text = page.extract_text() or ""
            # Agrega el texto extraído a la lista
            pages_text.append(text)

    # Retorna la lista con los textos de todas las páginas
    return pages_text

def find_outline_pages(pdf_path, outline_path, offset=0):
    """
    Devuelve una lista donde cada item es:
    {'title': ..., 'level': ..., 'page': ...}

    Busca cada título del outline en el texto de cada página del PDF.
    Si lo encuentra, asocia el número de página (respetando offset).
    """
    outline = parse_outline(outline_path)
    pages_text = extract_pages_text(pdf_path)
    results = []

    for item in outline:
        found = False
        for page_num, page_text in enumerate(pages_text):
            # Para búsqueda robusta, limpiamos los títulos y comparamos insensible a mayúsculas/minúsculas
            if clean_title(item['title']).lower() in (page_text or "").lower():
                results.append({
                    'title': item['title'],
                    'level': item['level'],
                    'raw': item['raw'],
                    # El número de página debe respetar el offset (1-indexed)
                    'page': page_num + 1 + offset
                })
                found = True
                break
        if not found:
            results.append({
                'title': item['title'],
                'level': item['level'],
                'raw': item['raw'],
                'page': None  # No se encontró el título en ninguna página
            })
    return results

# Prueba rápida
if __name__ == "__main__":
    outline_pages = find_outline_pages(
        pdf_path="../input.pdf",
        outline_path="../content.txt",
        offset=1  # Si la numeración inicia en la página 2 (por ejemplo), pon 1
    )
    for item in outline_pages:
        print(f"{item['raw']} --- Página: {item['page']}")