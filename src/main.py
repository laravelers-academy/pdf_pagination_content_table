import os
from pypdf import PdfReader
from numbering import add_page_numbers

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_path, "input.pdf")
    output_file = os.path.join(base_path, "numbered.pdf")

    reader = PdfReader(input_file)
    print("Is Encrypted:", reader.is_encrypted)

    add_page_numbers(
        input_path=input_file,
        output_path=output_file,
        offset=1,       # Numerar desde la primera
        font_size=12    # ¡Grande!
    )
