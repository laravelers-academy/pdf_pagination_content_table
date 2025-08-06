import pdfplumber  # Importa la librería pdfplumber, que sirve para extraer texto de archivos PDF

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

# --- Bloque de prueba: solo se ejecuta si corres este archivo directamente ---
if __name__ == "__main__":
    # Extrae el texto de todas las páginas del PDF "../input.pdf"
    texts = extract_pages_text("input.pdf")
    
    # Imprime el texto de las primeras 5 páginas para verificar que funciona
    for i, t in enumerate(texts[:5]):
        print(f"--- Página {i+1} ---\n{t}\n")
