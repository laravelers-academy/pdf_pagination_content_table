# Instrucciones de desarrollo

## **Paso 1: Preparar el Entorno y Elegir Herramientas**

### **¿Qué vas a necesitar?**

* **Python 3.9+**
* Librerías:

  * `PyPDF2` o `pypdf`: para manipular PDFs (leer, extraer, escribir).
  * `pdfplumber`: para leer el texto del PDF y encontrar las coincidencias de capítulos/temas.
  * `fpdf` o `reportlab`: para crear páginas nuevas (como la tabla de contenido).
  * `tkinter` o consola para una interfaz sencilla (opcional, después).

### **¿Por qué estas herramientas?**

* **PyPDF2/pypdf**:
  * Añade números de página, inserta páginas nuevas, manipula PDFs fácilmente.

* **pdfplumber**:
  * Extrae el texto de cada página de forma más precisa (ideal para buscar capítulos/temas).

* **fpdf/reportlab**:
  * Permite crear una página de tabla de contenido bien formateada, agregarla al PDF final.

¡Perfecto! Vamos desde cero, como si fuera un curso bien estructurado.
Vamos con **entorno virtual**, **instalación de dependencias** y el **archivo requirements.txt**.

---

## **Paso 2: Preparar el entorno de desarrollo (virtualenv)**

### **2.1. Crear un entorno virtual**

Esto te ayuda a mantener tu proyecto aislado de otras dependencias de Python:

```bash
python -m venv venv
```

> Esto crea una carpeta llamada `venv` con un Python “limpio” solo para tu proyecto.

---

### **1.2. Activar el entorno virtual**

* **Windows:**

  ```bash
  source venv/Scripts/activate
  ```
  Ve si ves algo como `(venv)` al inicio de tu línea de comandos, ¡significa que está activo!


* **Mac/Linux:**

  ```bash
  source venv/bin/activate
  ```

> Sabrás que está activo porque tu línea de comandos ahora inicia con `(venv)`.

---

## **Paso 2: Instalar dependencias necesarias con pip**

Instalamos las librerías que usaremos en el proyecto:

```bash
pip install pypdf pdfplumber fpdf
```

* `pypdf` → Manipulación de PDF (modificar, combinar, numerar).
* `pdfplumber` → Extraer texto de páginas para detectar capítulos y temas.
* `fpdf` → Crear páginas nuevas (como la tabla de contenido).

---

## **Paso 3: Generar el archivo requirements.txt**

Para guardar las versiones exactas que instalaste, ejecuta:

```bash
pip freeze > requirements.txt
```

Esto generará un archivo `requirements.txt` como este (puede variar la versión):

```txt
fpdf==1.7.2
pdfplumber==0.11.0
pypdf==4.2.0
```

> **Recomendación:** Si subes el proyecto a GitHub, ¡agrega este archivo para que cualquiera pueda instalarlo igual!

---

## Añadir a gitignore

Crea un archivo `.gitignore` en la raíz del proyecto y añade lo siguiente:

venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
*.log   
*.env

¡Por supuesto! Aquí va **Parte II**, adaptada a la estructura profesional del proyecto que definimos, con explicación paso a paso.

---

¡Perfecto! Aquí tienes **Parte II** con todo el **código, nombres de archivos, variables y funciones en inglés**. Las explicaciones siguen en español.

---

# **Parte II — Numerar páginas de un PDF con offset**

## **Estructura del proyecto (actualizada):**

```
pdf-num-toc/
├── requirements.txt
├── input.pdf             # PDF de prueba
└── src/
    ├── __init__.py
    ├── main.py           # Script principal
    └── numbering.py      # Lógica para numerar páginas
```

*Nota: ahora el PDF se llama `input.pdf` y el archivo de salida será `numbered.pdf`.*

---

## **¿Qué va a hacer este módulo?**

* Recibe un PDF de entrada.
* Añade número de página en cada hoja, **empezando desde una página X** (offset).
* Guarda un PDF nuevo con la numeración añadida.

---

## **A. Crea el archivo `src/numbering.py`**

```python
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
```

---

## **B. Crea el archivo `src/main.py`**

```python
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
```

---

## **Explicación rápida**

* **offset:** Desde qué página empieza la numeración (0 = la primera página).
* **merge\_page:** Usa el número generado con FPDF y lo superpone a la página real.
* **os.remove:** Borra el PDF temporal que contiene el número, así nunca dejas archivos basura.

---

## **¿Cómo probarlo?**

1. **Pon tu archivo PDF de prueba** en la raíz del proyecto y nómbralo `input.pdf`.
2. **Desde la raíz del proyecto**, ejecuta:

   ```bash
   python src/main.py
   ```
3. **Revisa el archivo** `numbered.pdf` que debe aparecer junto a tu PDF de entrada.

---


