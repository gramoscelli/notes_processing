from bs4 import BeautifulSoup
import os
import re
import sys
import argparse

HELP_TEXT = '''
CSS Simplifier (desagrupando y fusionando reglas)
--------------------------------------------------
Extrae todos los bloques <style> de un HTML (salvo los que están dentro de <defs>)
y los concatena en uno solo. Elimina las declaraciones que quedan anuladas por otra
del mismo selector, respetando !important y la cascada: cada declaración que
sobrevive conserva su posición original. Los bloques @media, @keyframes, etc.
se conservan intactos y en su lugar.

Uso:
  python simplify_css.py archivo.html [opciones]

Opciones:
  -o, --output archivo   Nombre del archivo de salida.
                         Si no se especifica, se usa <archivo>_simplify.html

Ejemplos:
  python simplify_css.py documento.html
  python simplify_css.py documento.html --output resultado.html
'''


def _dividir(texto, separador):
    """Divide por un carácter que no esté dentro de paréntesis, corchetes o comillas."""
    partes, actual, profundidad, comilla = [], [], 0, None
    for c in texto:
        if comilla:
            if c == comilla:
                comilla = None
        elif c in '"\'':
            comilla = c
        elif c in '([':
            profundidad += 1
        elif c in ')]':
            profundidad -= 1
        elif c == separador and profundidad == 0:
            partes.append(''.join(actual))
            actual = []
            continue
        actual.append(c)
    partes.append(''.join(actual))
    return partes


def _fin_de_bloque(css, inicio):
    """Dada la posición de una '{', devuelve la posición de su '}' correspondiente."""
    profundidad, comilla = 0, None
    for i in range(inicio, len(css)):
        c = css[i]
        if comilla:
            if c == comilla:
                comilla = None
        elif c in '"\'':
            comilla = c
        elif c == '{':
            profundidad += 1
        elif c == '}':
            profundidad -= 1
            if profundidad == 0:
                return i
    return len(css) - 1


def parsear_css(css):
    """Devuelve una lista ordenada de elementos:
    ('at', texto) para @-reglas (se conservan tal cual) y
    ('decl', selector, propiedad, valor) para cada declaración de cada selector."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    elementos = []
    i = 0
    while i < len(css):
        llave = css.find('{', i)
        punto_y_coma = css.find(';', i)
        if llave == -1:
            break
        # @-regla sin bloque (@import, @charset)
        if css[i:].lstrip().startswith('@') and -1 < punto_y_coma < llave:
            elementos.append(('at', css[i:punto_y_coma + 1].strip()))
            i = punto_y_coma + 1
            continue
        fin = _fin_de_bloque(css, llave)
        preludio = css[i:llave].strip()
        cuerpo = css[llave + 1:fin]
        if preludio.startswith('@'):
            elementos.append(('at', f"{preludio} {{{cuerpo}}}"))
        elif preludio:
            selectores = [s.strip() for s in _dividir(preludio, ',') if s.strip()]
            for declaracion in _dividir(cuerpo, ';'):
                if ':' not in declaracion:
                    continue
                propiedad, valor = (p.strip() for p in declaracion.split(':', 1))
                for selector in selectores:
                    elementos.append(('decl', ' '.join(selector.split()), propiedad, valor))
        i = fin + 1
    return elementos


def fusionar_reglas(elementos):
    """Conserva, para cada (selector, propiedad), solo la declaración ganadora:
    la última con !important o, si no hay, la última. Las ganadoras mantienen su
    posición, así que el orden de la cascada entre selectores no cambia."""
    ganadora = {}
    for pos, el in enumerate(elementos):
        if el[0] != 'decl':
            continue
        clave = (el[1], el[2])
        importante = el[3].replace(' ', '').endswith('!important')
        previa = ganadora.get(clave)
        if previa is None or importante or not previa[1]:
            ganadora[clave] = (pos, importante)
    posiciones = {pos for pos, _ in ganadora.values()}

    # Agrupar declaraciones consecutivas del mismo selector en una regla
    bloques = []  # ('at', texto) o ('regla', [selectores], [declaraciones])
    for pos, el in enumerate(elementos):
        if el[0] == 'at':
            bloques.append(el)
        elif pos in posiciones:
            _, selector, propiedad, valor = el
            if bloques and bloques[-1][0] == 'regla' and bloques[-1][1] == [selector]:
                bloques[-1][2].append(f"{propiedad}: {valor}")
            else:
                bloques.append(('regla', [selector], [f"{propiedad}: {valor}"]))

    # Reagrupar reglas consecutivas con el mismo cuerpo
    compactados = []
    for b in bloques:
        if b[0] == 'regla' and compactados and compactados[-1][0] == 'regla' and compactados[-1][2] == b[2]:
            compactados[-1][1].extend(b[1])
        else:
            compactados.append(b)

    resultado = []
    for b in compactados:
        if b[0] == 'at':
            resultado.append(b[1])
        else:
            resultado.append(f"{', '.join(b[1])} {{ {'; '.join(b[2])}; }}")
    return '\n'.join(resultado)


def combine_styles(html_file_path, output_file_path=None):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    if not output_file_path:
        file_name, file_ext = os.path.splitext(html_file_path)
        output_file_path = f"{file_name}_simplify{file_ext}"

    # Bloques que se deben simplificar (NO dentro de <defs>)
    bloques = [b for b in soup.find_all('style') if b.find_parent('defs') is None and b.string]
    elementos = []
    for bloque in bloques:
        elementos += parsear_css(bloque.string)

    if elementos:
        for bloque in bloques:
            bloque.decompose()
        new_style_tag = soup.new_tag("style")
        new_style_tag.string = fusionar_reglas(elementos)
        if soup.head:
            soup.head.append(new_style_tag)
        else:
            soup.insert(0, new_style_tag)
    else:
        print("No se encontraron bloques <style> para simplificar.")

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup).replace(' viewbox=', ' viewBox='))

    print(f"Estilos simplificados y guardados en {output_file_path}")
    return output_file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combina bloques <style> desagrupando y fusionando reglas.', add_help=False)
    parser.add_argument('input_file', nargs='?', help='Archivo HTML de entrada')
    parser.add_argument('-o', '--output', help='Archivo HTML de salida')
    parser.add_argument('-h', '--help', action='store_true', help='Muestra la ayuda')
    args = parser.parse_args()

    if args.help or not args.input_file:
        print(HELP_TEXT)
        sys.exit(0 if args.help else 1)

    try:
        combine_styles(args.input_file, args.output)
    except Exception as e:
        print(f"Error simplificando estilos: {e}")
        sys.exit(1)
