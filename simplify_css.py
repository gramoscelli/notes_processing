from bs4 import BeautifulSoup
import os
import argparse
import re
from collections import defaultdict

HELP_TEXT = '''
CSS Simplifier (desagrupando y fusionando reglas)
--------------------------------------------------
Extrae todos los bloques <style> de un HTML y los concatena en uno solo,
desagrupando reglas con múltiples selectores, preservando el orden,
y fusionando propiedades repetidas respetando !important y la cascada.

Uso:
  python simplify_css.py archivo.html [opciones]

Opciones:
  -o, --output archivo   Nombre del archivo de salida.
                         Si no se especifica, se generará automáticamente.

Ejemplos:
  python simplify_css.py documento.html
  python simplify_css.py documento.html --output resultado.html
'''

def desagrupar_reglas(css):
    bloques = re.findall(r'([^{}]+){([^{}]+)}', css, re.DOTALL)
    reglas = []
    for selectores, propiedades in bloques:
        for selector in selectores.split(','):
            reglas.append((selector.strip(), propiedades.strip()))
    return reglas

def fusionar_reglas(reglas):
    reglas_por_selector = defaultdict(list)

    # recolectar propiedades por selector
    for selector, props in reglas:
        for linea in props.split(';'):
            linea = linea.strip()
            if not linea:
                continue
            if ':' not in linea:
                continue
            propiedad, valor = map(str.strip, linea.split(':', 1))
            reglas_por_selector[selector].append((propiedad, valor))

    # aplicar la cascada: últimas definiciones prevalecen, salvo !important
    reglas_finales = {}
    for selector, pares in reglas_por_selector.items():
        propiedades = {}
        for prop, val in pares:
            es_important = val.endswith('!important')
            if prop not in propiedades:
                propiedades[prop] = (val, es_important)
            else:
                _, ya_important = propiedades[prop]
                if es_important or not ya_important:
                    propiedades[prop] = (val, es_important)
        reglas_finales[selector] = propiedades

    resultado = []
    for selector, props in reglas_finales.items():
        cuerpo = '; '.join(f"{k}: {v}" for k, (v, _) in props.items())
        resultado.append(f"{selector} {{{cuerpo};}}")
    return '\n\n'.join(resultado)

def combine_styles(html_file_path, output_file_path=None):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    style_blocks = soup.find_all('style')

    if len(style_blocks) == 0:
        print("No style blocks found.")
        return

    # recolecta y desagrupa todas las reglas CSS
    reglas = []
    for block in style_blocks:
        if block.string:
            css_limpio = block.string.strip()
            reglas += desagrupar_reglas(css_limpio)

    # fusiona reglas por selector teniendo en cuenta !important y orden
    css_fusionado = fusionar_reglas(reglas)

    # elimina los bloques <style> originales
    for block in style_blocks:
        block.decompose()

    # inserta el nuevo bloque <style> al final del <head>
    new_style_tag = soup.new_tag("style")
    new_style_tag.string = css_fusionado

    if soup.head:
        soup.head.append(new_style_tag)
    else:
        soup.insert(0, new_style_tag)

    # guarda salida
    if not output_file_path:
        file_name, file_ext = os.path.splitext(html_file_path)
        output_file_path = f"{file_name}_simplify{file_ext}"

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Style blocks successfully simplified and saved to {output_file_path}")
    return output_file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine <style> blocks desagrupando y fusionando reglas.', add_help=False)
    parser.add_argument('input_file', help='Input HTML file')
    parser.add_argument('-o', '--output', help='Output HTML file')
    parser.add_argument('-h', '--help', action='store_true', help='Show help message')
    args = parser.parse_args()

    if args.help:
        print(HELP_TEXT)
        exit(0)

    combine_styles(args.input_file, args.output)