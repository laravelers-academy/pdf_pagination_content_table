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

# **Parte V — Crear y agregar la Tabla de Contenido (TOC) al PDF**

## **¿Qué vamos a lograr?**

1. Tomar la lista de capítulos/temas con sus páginas (ya calculados).
2. Generar un PDF (usando FPDF) con una o varias páginas de TOC, formateada de manera profesional.
3. Insertar esas páginas **antes de la primera página numerada** (respetando el offset).

---

## **A. Nueva estructura del proyecto**

Agrega un archivo más en `src/` para la lógica del TOC:

```
pdf-num-toc/
├── requirements.txt
├── input.pdf
├── content.txt
└── src/
    ├── __init__.py
    ├── main.py
    ├── numbering.py
    ├── toc.py
    ├── outline_parser.py
    └── toc_pdf.py       # Nuevo: crea el PDF de la tabla de contenido
```

---

## **B. Generar la tabla de contenido en PDF**

**Crea `src/toc_pdf.py`**
Este archivo generará la(s) página(s) de TOC usando FPDF, basada en la estructura que ya tienes.

```python
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
    create_toc_pdf(toc_items, "../toc.pdf")
```

---

## **C. Insertar la(s) página(s) de TOC al PDF numerado**

Puedes hacerlo desde tu `main.py` o con un módulo nuevo. Aquí te muestro la lógica:

```python
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

```

---

### **Notas clave:**

* El TOC se insertará **antes de la numeración**, así el usuario ve el índice antes de los capítulos/temas.
* Si tu numeración empieza en la página 2 (por ejemplo, offset=1), asegúrate de ajustar el conteo de páginas al generar el TOC.
* Puedes hacer el flujo completamente automático (crear TOC, generar PDF numerado, insertar TOC) con un solo script.

---

## **¿Qué sigue?**

* Puedes personalizar el diseño del TOC (tamaño de fuente, títulos, márgenes).
* Si tu TOC ocupa más de una página, FPDF lo maneja automáticamente.
* Si tienes portadas o páginas preliminares, considera el offset en todos los pasos para que la paginación y el TOC sean coherentes.

---


# **Parte VI — Insertar TOC después del offset y ajustar la numeración**

---

## **A. Objetivo**

* Insertar el TOC **después de la(s) página(s) de offset** (no al inicio absoluto).
* Asegurar que los números de página en el TOC sean los que se ven en el PDF numerado (es decir, que el primer capítulo siempre tenga el número que corresponde a la página donde inicia la numeración).
* ¡El resultado: portada(s), luego TOC, luego el resto del documento con la paginación correcta!

---

## **B. Ajustes en el flujo**

### 1. **Genera el PDF numerado igual que antes.**

### 2. **Detecta capítulos/temas y asigna números de página del PDF numerado, NO del original.**

* Esto es importante, porque si insertas páginas (el TOC), cambian las posiciones.
* Lo más robusto: **Primero inserta el TOC, luego numera el PDF final**.

### 3. **Inserta el TOC después del offset**:

* Por ejemplo, si `offset = 1`, deja la primera página intacta, luego mete el TOC, luego el resto.

### 4. **Numera todas las páginas (incluyendo el TOC) después de haber insertado el TOC**.

* Así, la numeración se ajusta a la posición real de cada capítulo/tema.
* En el TOC, las páginas reflejarán el número **visible** en el PDF, no la física del archivo original.

---

## **C. Implementación: Flujo corregido**

### **1. Crea primero el PDF con offset intacto (portadas, etc).**

### **2. Inserta el TOC después del offset (por ejemplo, después de la portada).**

```python
from pypdf import PdfReader, PdfWriter

def insert_toc_after_offset(toc_pdf_path, original_pdf_path, output_pdf_path, offset):
    """
    Inserta las páginas del TOC después del offset indicado.
    offset=1 -> deja la primera página (portada) intacta, luego inserta el TOC.
    """
    toc_reader = PdfReader(toc_pdf_path)
    orig_reader = PdfReader(original_pdf_path)
    writer = PdfWriter()

    # 1. Copia las páginas de offset (por ejemplo, portada)
    for i in range(offset):
        writer.add_page(orig_reader.pages[i])

    # 2. Añade el TOC
    for page in toc_reader.pages:
        writer.add_page(page)

    # 3. Añade el resto del PDF original
    for i in range(offset, len(orig_reader.pages)):
        writer.add_page(orig_reader.pages[i])

    # 4. Guarda el nuevo PDF combinado
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)
```

---

### **3. Ahora, cuando generes el TOC, debes calcular las páginas como el usuario las verá.**

* Si hay portada (offset=1) y luego TOC de 1 página, el **primer capítulo** estará en la página (offset + len(TOC) + 1).
* Por lo tanto, **detecta los capítulos/temas** en el PDF ya con TOC insertado (no el original).

**Ejemplo para ajustar el find\_outline\_pages:**

* Primero, inserta el TOC provisional (puede estar vacío o solo con títulos).
* Después, **extrae el texto** de cada página (ahora portada, TOC, contenido).
* Busca en qué página aparece cada capítulo/tema.
* Al generar el TOC definitivo, los números serán exactos.

---

### **4. Numera el PDF final (con TOC ya insertado)**

* Usa tu función `add_page_numbers`, pero ahora el offset debe incluir portada + TOC.

  * Ejemplo: offset = 1 (portada) + páginas de TOC

---

## **D. Ejemplo de flujo corregido en main.py**

```python
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

    # 4. Insertar el TOC después de la portada
    insert_toc_after_offset(
        toc_pdf_path=toc_pdf,
        original_pdf_path=numbered_pdf,
        output_pdf_path=final_pdf,
        offset=offset
    )
    print(f"¡Listo! PDF final generado en: {final_pdf}")
```

---

### **¿Cómo funciona esto?**

* Se inserta el TOC **después de la portada** (offset).
* La numeración salta portada + TOC.
* El TOC muestra los números reales y visibles para el usuario.
* Si el TOC es de varias páginas, todo sigue alineado.
* Si tienes más de una portada, ajusta el offset.

---

## **E. Tips y recomendaciones**

* Si no quieres reescribir el TOC dos veces, puedes estimar primero el número de páginas del TOC (por ej., generar uno, contar páginas, luego el real).
* Si quieres mantener archivos temporales limpios, bórralos después del flujo.
* Puedes mostrar un resumen del proceso al usuario: “Portada(s): X páginas, TOC: Y páginas, Contenido: Z páginas”.

