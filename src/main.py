import os
from pypdf import PdfReader
from numbering import add_page_numbers
from toc import find_outline_pages
from toc_pdf import create_toc_pdf
from outline_parser import parse_outline
from pypdf import PdfWriter

def insert_toc_into_pdf(toc_pdf_path, original_pdf_path, output_pdf_path):
    """
    Inserta las páginas del TOC (toc_pdf_path) antes del PDF original (original_pdf_path).
    """
    toc_reader = PdfReader(toc_pdf_path)
    orig_reader = PdfReader(original_pdf_path)
    writer = PdfWriter()

    # Añade TOC
    for page in toc_reader.pages:
        writer.add_page(page)
    # Añade el resto del PDF numerado
    for page in orig_reader.pages:
        writer.add_page(page)
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_pdf = os.path.join(base_path, "input.pdf")
    numbered_pdf = os.path.join(base_path, "numbered.pdf")
    toc_txt = os.path.join(base_path, "content.txt")
    toc_pdf = os.path.join(base_path, "toc.pdf")
    final_pdf = os.path.join(base_path, "final_with_toc.pdf")
    offset = 1  # Por ejemplo, portada

    # 1. Numerar el PDF
    reader = PdfReader(input_pdf)
    print("Is Encrypted:", reader.is_encrypted)
    add_page_numbers(
        input_path=input_pdf,
        output_path=numbered_pdf,
        offset=offset,
        font_size=12
    )
    print("PDF numerado generado.")

    # 2. Encontrar capítulos/temas y sus páginas
    outline_items = find_outline_pages(
        pdf_path=input_pdf,
        outline_path=toc_txt,
        offset=offset
    )
    print("Capítulos/temas identificados.")

    # 3. Generar el PDF del TOC
    create_toc_pdf(outline_items, toc_pdf)
    print("PDF de TOC generado.")

    # 4. Insertar el TOC antes del contenido numerado
    insert_toc_into_pdf(
        toc_pdf_path=toc_pdf,
        original_pdf_path=numbered_pdf,
        output_pdf_path=final_pdf
    )
    print(f"¡Listo! PDF final generado en: {final_pdf}")