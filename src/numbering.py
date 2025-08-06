from pypdf import PdfReader, PdfWriter  # Para leer y escribir archivos PDF
from fpdf import FPDF                   # Para generar páginas PDF desde cero (el overlay del número)
import os                               # Para eliminar archivos temporales

def add_page_numbers(input_path, output_path, offset=0, font_size=12):
    """
    Añade números de página a un PDF existente.
    El número aparece en la esquina superior derecha de cada página, a partir del offset.
    
    Args:
        input_path (str): Ruta del PDF original (entrada).
        output_path (str): Ruta donde se guardará el PDF numerado (salida).
        offset (int): Número de páginas a omitir antes de empezar la numeración (por ejemplo, portadas o índice).
        font_size (int): Tamaño de la fuente para el número de página.
    """

    # Lee el PDF de entrada completo
    reader = PdfReader(input_path)
    # Crea un escritor (output) para el PDF final numerado
    writer = PdfWriter()
    # Número total de páginas
    num_pages = len(reader.pages)

    # Recorre todas las páginas del PDF original
    for i, page in enumerate(reader.pages):
        # Solo añade el número si la página está después del offset
        if i >= offset:
            # Convierte el tamaño de la página de puntos a milímetros (fpdf trabaja en mm)
            width = float(page.mediabox.width) * 0.352778
            height = float(page.mediabox.height) * 0.352778

            # Crea un nuevo PDF temporal del mismo tamaño que la página original
            num_pdf = FPDF(unit="mm", format=[width, height])
            num_pdf.add_page()
            num_pdf.set_font("Arial", size=font_size)
            
            # Establece la posición del número (esquina superior derecha)
            # width - 30: 30 mm del borde derecho
            # 10: 10 mm desde la parte superior
            num_pdf.set_xy(width - 30, 10)
            
            # Escribe el número de página (centrado a la derecha)
            num_pdf.cell(15, 10, str(i - offset + 1), 0, 0, "R")
            
            # Guarda el PDF temporal con solo el número
            temp_name = "temp_page_num.pdf"
            num_pdf.output(temp_name)

            # Lee el PDF temporal y obtiene la primera (y única) página
            num_reader = PdfReader(temp_name)
            number_page = num_reader.pages[0]
            
            # Superpone (merge) el PDF temporal sobre la página original
            # NOTA: El fondo blanco del overlay puede tapar contenido original debajo.
            page.merge_page(number_page)
            
            # Elimina el archivo temporal para no dejar basura en disco
            os.remove(temp_name)

        # Añade la página (numerada o no) al PDF de salida
        writer.add_page(page)

    # Escribe el PDF final en el disco
    with open(output_path, "wb") as f_out:
        writer.write(f_out)