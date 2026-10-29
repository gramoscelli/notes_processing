import os
import base64
import argparse
from bs4 import BeautifulSoup

def _parse_arguments():
    parser = argparse.ArgumentParser(description='Convertir estilos CSS en <style> a inline y mover scripts.')
    parser.add_argument('input_file', help='Archivo HTML de entrada')
    parser.add_argument('-o', '--output', nargs='?', const=True,
                        help='Archivo de salida (por defecto: <entrada>_inline.html)')
    return parser.parse_args()

def process_mermaid_divs(soup):
    """Guarda el código de cada div 'mermaid' en base64 en data-mermaid-src.
    Moodle altera los saltos de línea del texto, pero no los atributos data-*;
    un script restaura el código antes de que Mermaid.js lo procese."""
    mermaid_divs = soup.find_all("div", class_="mermaid")
    for div in mermaid_divs:
        codigo = div.get_text().replace('\r\n', '\n')
        div['data-mermaid-src'] = base64.b64encode(codigo.encode('utf-8')).decode('ascii')
    return mermaid_divs

def _asegurar_body(soup):
    """Devuelve el <body>, creándolo si no existe."""
    if not soup.body:
        body = soup.new_tag("body")
        (soup.html or soup).append(body)
    return soup.body

def _merge_style(tag, new_styles):
    """Agrega estilos inline a un tag sin perder los existentes."""
    existing = tag.get('style', '').rstrip(';').strip()
    if existing:
        merged = existing + '; ' + new_styles
    else:
        merged = new_styles
    tag['style'] = merged

def apply_inline_responsive_styles(soup):
    """Aplica estilos inline en SVGs e imágenes para que funcionen en Moodle.
    Moodle stripea width, height y viewBox del <svg>, pero preserva style y data-*.
    Guardamos viewBox en data-viewbox y las dimensiones en CSS style."""

    for svg in soup.find_all('svg'):
        current_style = svg.get('style', '')
        viewbox = svg.get('viewbox') or svg.get('viewBox')
        if viewbox and 'data-viewbox' not in svg.attrs:
            svg['data-viewbox'] = viewbox
        if viewbox and 'width' not in current_style:
            parts = viewbox.split()
            if len(parts) == 4:
                w, h = parts[2], parts[3]
                _merge_style(svg, f'width: {w}px; height: {h}px; max-width: 100%')
        elif 'max-width' not in current_style:
            _merge_style(svg, 'max-width: 100%; height: auto')

    for img in soup.find_all('img'):
        current_style = img.get('style', '')
        if 'max-width' not in current_style:
            _merge_style(img, 'max-width: 100%; height: auto')

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
    
    # MODIFICACIÓN: Solo procesar las etiquetas <style> del <head>, no tocar CSS inline
    style_tags = head.find_all("style") if head else []
    css_content = "\n\n".join(tag.string for tag in style_tags if tag.string)

    # Eliminar SOLO las etiquetas <style> del <head> (preservar atributos style inline)
    for tag in style_tags:
        tag.decompose()

    # Extraer y envolver los scripts SOLO del <head>
    script_tags = head.find_all("script") if head else []
    wrapped_scripts = []

    for tag in script_tags:
        if tag.string:
            # Crear una nueva etiqueta <script> que se ejecutará con el evento DOMContentLoaded
            new_script = soup.new_tag("script")
            new_script.string = f"document.addEventListener('DOMContentLoaded', function() {{\n{tag.string}\n}});"
            wrapped_scripts.append(new_script)
        tag.decompose()  # Eliminar el <script> original del <head>

    mermaid_divs = process_mermaid_divs(soup)

    # Aplicar estilos responsivos críticos como atributos inline directamente
    # en SVGs e imágenes, para que funcionen en Moodle incluso si el JS
    # que recarga CSS desde el textarea es bloqueado.
    apply_inline_responsive_styles(soup)

    # Solo crear el textarea si hay contenido CSS para procesar
    if css_content.strip():
        # Crear <textarea> para el CSS extraído (invisible al usuario)
        textarea_tag = soup.new_tag("textarea")
        textarea_tag['id'] = "css-editor"
        textarea_tag['style'] = "display:none;"
        textarea_tag.string = css_content

        # Insertar el <textarea> al final del <body>
        _asegurar_body(soup).append(textarea_tag)

        # Agregar script que recargue el CSS desde el <textarea>
        css_loader_script = soup.new_tag("script")
        css_loader_script.string = """
document.addEventListener('DOMContentLoaded', function() {
    var cssEditor = document.getElementById('css-editor');
    if (cssEditor) {
        var cssCode = cssEditor.value;
        var style = document.createElement('style');
        style.textContent = cssCode;
        document.head.appendChild(style);
    }
});
"""
        soup.body.append(css_loader_script)

    # Script para restaurar viewBox en SVGs (Moodle stripea viewBox pero no data-*)
    svgs_with_data_viewbox = soup.find_all('svg', attrs={'data-viewbox': True})
    if svgs_with_data_viewbox:
        viewbox_restore_script = soup.new_tag("script")
        viewbox_restore_script.string = """
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('svg[data-viewbox]').forEach(function(svg) {
        if (!svg.getAttribute('viewBox')) {
            svg.setAttribute('viewBox', svg.getAttribute('data-viewbox'));
        }
    });
});
"""
        _asegurar_body(soup).append(viewbox_restore_script)

    # Insertar los scripts originalmente extraídos y envueltos
    body = _asegurar_body(soup)
    for tag in wrapped_scripts:
        body.append(tag)

    # Script para restaurar el código de los divs mermaid desde data-mermaid-src.
    # IMPORTANTE: debe ejecutarse de forma sincrónica ANTES del módulo mermaid,
    # que usa startOnLoad y se dispara en DOMContentLoaded.
    if mermaid_divs:
        mermaid_restore_script = soup.new_tag("script")
        mermaid_restore_script.string = """
document.querySelectorAll('div.mermaid[data-mermaid-src]').forEach(function(div) {
    var bytes = Uint8Array.from(atob(div.dataset.mermaidSrc), function(c) { return c.charCodeAt(0); });
    div.textContent = new TextDecoder().decode(bytes);
});
"""
        # Insertar ANTES del script module de mermaid para que se ejecute primero
        mermaid_script = soup.find("script", attrs={"type": "module"})
        if mermaid_script:
            mermaid_script.insert_before(mermaid_restore_script)
        else:
            body.append(mermaid_restore_script)

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(str(soup).replace(' viewbox=', ' viewBox='))

    print(f"Archivo procesado: {archivo_entrada}")
    print(f"Archivo de salida: {archivo_salida}")
    if css_content.strip():
        print(f"CSS extraído y convertido a inline: {len(style_tags)} etiquetas <style>")
    else:
        print("No se encontraron etiquetas <style> para procesar")
    if wrapped_scripts:
        print(f"Scripts del <head> movidos al final del <body>: {len(wrapped_scripts)}")
    if mermaid_divs:
        print(f"Divs Mermaid procesados: {len(mermaid_divs)}")

if __name__ == '__main__':
    main()