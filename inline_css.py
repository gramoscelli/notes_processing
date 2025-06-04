import sys
import os
import argparse
from bs4 import BeautifulSoup

def _parse_arguments():
    parser = argparse.ArgumentParser(description='Convertir estilos CSS en <style> a inline y mover scripts.')
    parser.add_argument('input_file', help='Input HTML file')
    parser.add_argument('-o', '--output', nargs='?', const=True,
                        help='Optional output file name. If used without value, default to input filename with _inline.')
    return parser.parse_args()

def main():
    args = _parse_arguments()
    archivo_entrada = args.input_file

    # Determinar archivo de salida
    if args.output:
        # Si se proporcionó '-o' sin valor, args.output == True
        if args.output is True:
            base, ext = os.path.splitext(archivo_entrada)
            archivo_salida = f"{base}_inline.html"
        else:
            archivo_salida = args.output
    else:
        base, ext = os.path.splitext(archivo_entrada)
        archivo_salida = f"{base}_inline.html"

    with open(archivo_entrada, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    head = soup.head
    style_tags = head.find_all("style")
    css_content = "\n\n".join(tag.string for tag in style_tags if tag.string)

    # Eliminar las etiquetas <style> del <head>
    for tag in style_tags:
        tag.decompose()

    # Extraer y envolver los scripts en <head>
    script_tags = head.find_all("script")
    wrapped_scripts = []

    for tag in script_tags:
        if tag.string:
            # Crear una nueva etiqueta <script> que se ejecutará con el evento DOMContentLoaded
            new_script = soup.new_tag("script")
            new_script.string = f"document.addEventListener('DOMContentLoaded', function() {{\n{tag.string}\n}});"
            wrapped_scripts.append(new_script)
        tag.decompose()  # Eliminar el <script> original del <head>

    # Crear <textarea> para el CSS extraído (invisible al usuario)
    textarea_tag = soup.new_tag("textarea")
    textarea_tag['id'] = "css-editor"
    textarea_tag['style'] = "display:none;"
    textarea_tag.string = css_content

    # Insertar el <textarea> al final del <body>
    soup.body.append(textarea_tag)

    # Agregar script que recargue el CSS desde el <textarea>
    css_loader_script = soup.new_tag("script")
    css_loader_script.string = """
document.addEventListener('DOMContentLoaded', function() {
    var cssCode = document.getElementById('css-editor').value;
    var style = document.createElement('style');
    style.textContent = cssCode;
    document.head.appendChild(style);
});
"""
    soup.body.append(css_loader_script)

    # Agregar script para "arreglar" botones con clase .toggle-button
    button_fix_script = soup.new_tag("script")
    button_fix_script.string = """
document.addEventListener('DOMContentLoaded', function() {
    // Aplicar estilo con retraso de 100ms para superar posibles hojas de estilo heredadas
    setTimeout(function() {
        document.querySelectorAll('.toggle-button').forEach(btn => {
            btn.style.setProperty('color', 'black', 'important');
            if (!btn.textContent.trim()) {
                btn.textContent = '+';
            }
        });
        document.querySelectorAll('.copy-button').forEach(btn => {
            btn.style.setProperty('color', 'black', 'important');
        });
    }, 1000);
});
"""
    soup.body.append(button_fix_script)

    # Insertar los scripts originalmente extraídos y envueltos
    for tag in wrapped_scripts:
        soup.body.append(tag)

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))


if __name__ == '__main__':
    main()
