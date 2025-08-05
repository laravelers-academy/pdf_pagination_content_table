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
