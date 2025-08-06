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

# **Parte III — Detección de capítulos y temas para la tabla de contenido**

## **¿Qué vamos a lograr en esta sección?**

1. **Leer el texto de cada página del PDF.**
2. **Comparar el texto con tu lista jerárquica de capítulos/temas.**
3. **Registrar en qué página aparece cada capítulo/tema (para el TOC).**

---

## **A. Nueva estructura del proyecto**

Agrega un archivo más en `src/` para este propósito:

```
pdf-num-toc/
├── requirements.txt
├── input.pdf
└── src/
    ├── __init__.py
    ├── main.py
    ├── numbering.py
    └── toc.py         # Nuevo: lógica para buscar capítulos/temas y crear TOC
```

---

## **B. Paso 1 — Leer el texto de cada página del PDF**

Usaremos `pdfplumber` porque es confiable para extraer texto de cada página de forma legible.

### **1. Instala pdfplumber si no lo hiciste:**

```bash
pip install pdfplumber
```

Actualizar `requirements.txt`, para ello ejecutas
```bash
pip freeze > requirements.txt
```

---

### **2. Crea el archivo `src/toc.py`**

**Solo este paso: función para extraer el texto de cada página y dejarlo listo para analizar.**

```python
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
```

---

### **¿Qué sigue?**

Cuando tengas esto listo:

* Verifica que **sí imprime texto de cada página**.

---

¡Por supuesto! Aquí tienes **todo desde la Parte IV**, súper detallado y **con los comentarios incluidos** en cada sección de código. Así puedes continuar el desarrollo y usarlo como referencia didáctica:

---

# **Parte IV — Parsear el outline (content.txt) y buscar capítulos/temas en el PDF**

---

## **A. Estructura profesional del proyecto**

```
pdf-num-toc/
├── requirements.txt
├── .gitignore
├── input.pdf             # PDF de prueba
├── content.txt           # Outline numerado e indentado
└── src/
    ├── __init__.py
    ├── main.py
    ├── numbering.py
    ├── toc.py            # Extrae texto de PDF y busca capítulos
    └── outline_parser.py # Parseador de content.txt (outline)
```

---

## **B. Paso 1 — Parsear el archivo outline**

Crea `src/outline_parser.py`
Este archivo lee y procesa tu archivo outline (numerado e indentado), entregando una estructura de capítulos/temas con sus niveles.

```python
import re

def clean_title(title):
    """
    Elimina la numeración inicial (1. o 1.1, etc) y espacios extras para facilitar comparación.
    """
    return re.sub(r"^\s*\d+(\.\d+)*\s*\.?\s*", "", title).strip()

def parse_outline(txt_path):
    """
    Lee el outline de capítulos/temas y devuelve una lista:
    [
        {'title': '...', 'level': 0, 'raw': '1. ...'},
        {'title': '...', 'level': 1, 'raw': '1.1 ...'},
        ...
    ]
    """
    outline = []
    with open(txt_path, encoding="utf-8") as f:
        for line in f:
            clean = line.rstrip("\n")
            if not clean.strip():
                continue  # ignora líneas vacías
            # Cuenta la indentación (4 espacios = 1 nivel, o tabs)
            leading_spaces = len(clean) - len(clean.lstrip(' \t'))
            level = clean.count('\t') + (leading_spaces // 4)
            raw = clean.strip()
            title = clean_title(raw)
            outline.append({'title': title, 'level': level, 'raw': raw})
    return outline

# Prueba rápida
if __name__ == "__main__":
    outline = parse_outline("../content.txt")
    for item in outline:
        print(f"Level {item['level']} | Title: {item['title']} | Raw: {item['raw']}")
```

---

## **C. Paso 2 — Buscar los capítulos/temas en el PDF y asociar página**

Modifica `src/toc.py` para usar tu outline y encontrar en qué página está cada título.

```python
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
```

---

## **¿Qué hace este flujo?**

* **parse\_outline:** Lee tu `content.txt` y entrega una lista ordenada y con jerarquía.
* **extract\_pages\_text:** Saca el texto de todas las páginas.
* **find\_outline\_pages:** Busca cada título del outline en el texto de las páginas y asocia en cuál lo encontró (respetando offset para que coincida con la numeración real del PDF).

---

## **¿Cómo pruebas este paso?**

1. **Pon tu `input.pdf` y tu `content.txt` en la raíz del proyecto.**
2. **Ejecuta:**

   ```bash
   python src/toc.py
   ```
3. **Verifica que te imprime para cada capítulo/tema en qué página lo encontró (o None si no lo halló).**

---

¿Quieres que la siguiente parte sea cómo **generar la página de TOC en PDF** y cómo inyectarla antes de la primera página numerada?
¿Necesitas que te explique cómo ajustar la búsqueda para diferentes formatos?
¿O quieres afinar algo antes?
