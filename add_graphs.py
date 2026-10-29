#!/usr/bin/env python3
"""
Pre-renderiza bloques Mermaid en un HTML a SVG inline usando mmdc (mermaid-cli).
Elimina la dependencia de Mermaid.js en el cliente.
"""
import os
import re
import sys
import shutil
import tempfile
import argparse
import subprocess
from bs4 import BeautifulSoup


def find_mermaid_blocks(soup):
    """Encuentra todos los divs con clase 'mermaid'."""
    return soup.find_all('div', class_='mermaid')


def render_mermaid_to_svg(code, tmpdir, index):
    """Renderiza código Mermaid a SVG usando mmdc."""
    input_path = os.path.join(tmpdir, f'diagram_{index}.mmd')
    output_path = os.path.join(tmpdir, f'diagram_{index}.svg')

    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(code)

    result = subprocess.run(
        ['mmdc', '-i', input_path, '-o', output_path, '-b', 'transparent', '--quiet'],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode != 0:
        print(f"  Error en diagrama {index + 1}: {result.stderr.strip()}")
        return None

    with open(output_path, 'r', encoding='utf-8') as f:
        return f.read()


def clean_svg(svg_content, index):
    """Limpia el SVG para embebido inline: IDs únicos y tamaño natural."""
    # Reemplazar id="my-svg" con un id único por diagrama
    svg_content = svg_content.replace('id="my-svg"', f'id="mermaid-svg-{index}"')
    svg_content = svg_content.replace('#my-svg', f'#mermaid-svg-{index}')
    svg_content = svg_content.replace('my-svg_', f'mermaid-svg-{index}_')

    # Usar el ancho/alto del viewBox como dimensiones fijas del SVG
    # Moodle stripea width, height y viewBox del <svg>, así que:
    # 1. Guardamos viewBox en data-viewbox (Moodle no stripea data-*)
    # 2. Ponemos las dimensiones en CSS style (que Moodle preserva)
    vb_match = re.search(r'viewBox="([\d.]+ [\d.]+ ([\d.]+) ([\d.]+))"', svg_content)
    if vb_match:
        vb_full = vb_match.group(1)
        vb_width = vb_match.group(2)
        vb_height = vb_match.group(3)
        svg_content = svg_content.replace('width="100%"', f'width="{vb_width}" height="{vb_height}"', 1)
        # Agregar data-viewbox para restauración JS en Moodle
        svg_content = svg_content.replace('viewBox=', f'data-viewbox="{vb_full}" viewBox=', 1)

    # Poner dimensiones en CSS style para que sobrevivan al stripping de Moodle
    svg_content = re.sub(
        r'style="max-width:\s*[\d.]+px;\s*background-color:\s*transparent;"',
        lambda m: f'style="width: {vb_width}px; height: {vb_height}px; max-width: 100%; background-color: transparent;"' if vb_match else m.group(0),
        svg_content
    )

    # Agregar overflow:visible a foreignObject para evitar recorte de texto
    # cuando las métricas de fuente del navegador difieren de las de mmdc
    svg_content = svg_content.replace('<foreignObject ', '<foreignObject style="overflow: visible;" ')

    return svg_content


def main():
    parser = argparse.ArgumentParser(
        description='Pre-renderiza bloques Mermaid en HTML a SVG inline usando mmdc'
    )
    parser.add_argument('input_file', help='Archivo HTML de entrada')
    parser.add_argument('-o', '--output', help='Archivo HTML de salida (por defecto sobreescribe el input)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Salida detallada')

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if not shutil.which('mmdc'):
        print("Error: mmdc no encontrado. Instalar con: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)

    output_file = args.output or args.input_file

    with open(args.input_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    mermaid_blocks = find_mermaid_blocks(soup)

    if not mermaid_blocks:
        print("No se encontraron bloques Mermaid.")
        if output_file != args.input_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
        return

    print(f"Encontrados {len(mermaid_blocks)} diagramas Mermaid")

    with tempfile.TemporaryDirectory() as tmpdir:
        ok = 0
        for i, div in enumerate(mermaid_blocks):
            code = div.get_text().strip()
            # Restaurar saltos de línea si están codificados como #10
            code = code.replace('#10', '\n')

            if args.verbose:
                print(f"  Diagrama {i + 1}: {code[:60]}...")

            svg = render_mermaid_to_svg(code, tmpdir, i)
            if svg:
                svg = clean_svg(svg, i)
                container = soup.new_tag('div')
                container['class'] = 'mermaid-rendered'
                container['style'] = 'text-align: center; margin: 15px 0; overflow-x: auto;'
                container.append(BeautifulSoup(svg, 'html.parser'))
                div.replace_with(container)
                ok += 1
            else:
                print(f"  Diagrama {i + 1} falló, se mantiene como texto")

    # Eliminar el script de mermaid.js (ya no se necesita)
    for script in soup.find_all('script'):
        text = script.string or ''
        src = script.get('src', '')
        if 'mermaid' in src or 'mermaid' in text:
            if args.verbose:
                print(f"  Eliminando script de mermaid: {src or text[:50]}")
            script.decompose()

    # Eliminar estilos de .mermaid que ya no aplican
    for style in soup.find_all('style'):
        if style.string and '.mermaid' in style.string:
            style.string = re.sub(
                r'\.mermaid\s*\{[^}]*\}', '', style.string
            )

    output_html = str(soup)
    # BeautifulSoup html.parser convierte atributos SVG camelCase a minúsculas
    output_html = output_html.replace(' viewbox=', ' viewBox=')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_html)

    print(f"Renderizados: {ok}/{len(mermaid_blocks)} diagramas")
    print(f"Archivo de salida: {output_file}")


if __name__ == "__main__":
    main()
