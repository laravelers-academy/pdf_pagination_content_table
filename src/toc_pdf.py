from fpdf import FPDF

def create_toc_pdf(toc_items, output_path, title="Tabla de Contenido"):
    """
    Genera un PDF de TOC profesional a partir de una lista de dicts.
    Cada item debe tener: title, level, page
    """
    pdf = FPDF(unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, title, 0, 1, "C")
    pdf.ln(8)

    pdf.set_font("Arial", size=12)
    line_height = pdf.font_size * 2.2

    for item in toc_items:
        if item['page'] is None:
            continue  # Opcional: saltar temas no encontrados
        # Sangría según nivel (capítulo, subtema, etc)
        indent = "    " * item['level']
        title = f"{indent}{item['raw']}"
        # Ajusta el ancho disponible para puntos y página
        title_width = pdf.get_string_width(title)
        dots_width = pdf.w - 40 - title_width - 20
        dots = '.' * max(8, int(dots_width / 2.2))
        page_str = str(item['page'])
        # Imprime línea del TOC
        pdf.cell(0, line_height, f"{title} {dots} {page_str}", 0, 1, "L")

    pdf.output(output_path)

# Prueba rápida
if __name__ == "__main__":
    # Ejemplo de uso
    # Supón que ya tienes tu lista de capítulos con páginas (toc_items)
    toc_items = [
        {'title': 'Capítulo 1', 'raw': '1. Capítulo 1', 'level': 0, 'page': 3},
        {'title': 'Tema 1.1', 'raw': '1.1 Tema 1.1', 'level': 1, 'page': 4},
        {'title': 'Tema 1.2', 'raw': '1.2 Tema 1.2', 'level': 1, 'page': 6},
        # ...
    ]
    create_toc_pdf(toc_items, "toc.pdf")