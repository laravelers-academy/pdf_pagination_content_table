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