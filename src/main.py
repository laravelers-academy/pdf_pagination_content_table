import os
from pypdf import PdfReader
from numbering import add_page_numbers
from toc import find_outline_pages
from toc_pdf import create_toc_pdf
from outline_parser import parse_outline
from pypdf import PdfReader, PdfWriter

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

def insert_toc_after_offset(toc_pdf_path, original_pdf_path, output_pdf_path, offset):
    toc_reader = PdfReader(toc_pdf_path)
    orig_reader = PdfReader(original_pdf_path)
    writer = PdfWriter()

    # 1. Copia las páginas de offset (ej. portada)
    for i in range(offset):
        writer.add_page(orig_reader.pages[i])
    # 2. Añade TOC
    for page in toc_reader.pages:
        writer.add_page(page)
    # 3. Añade el resto del PDF
    for i in range(offset, len(orig_reader.pages)):
        writer.add_page(orig_reader.pages[i])
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)

def split_pdf_first_pages(input_pdf, output_pdf, num_pages=50):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Añadir las primeras N páginas
    for i in range(min(num_pages, len(reader.pages))):
        writer.add_page(reader.pages[i])

    # Guardar el nuevo PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)

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


    writer = PdfWriter(clone_from="numbered.pdf")

    for page in writer.pages:
        page.compress_content_streams() 

    with open("full.pdf", "wb") as f:
        writer.write(f)

    print("PDF comprimido generado.")

    # Split PDF
    split_pdf_first_pages(
        input_pdf="full.pdf",
        output_pdf="demo.pdf",
        num_pages=50
    )

    print("PDF dividido correctamente.")