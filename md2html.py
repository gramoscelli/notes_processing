#!/usr/bin/env python3
"""
md2html.py - Convierte un archivo Markdown a HTML con resaltado de sintaxis,
diagramas Mermaid y bloques SVG.

Uso:
    python md2html.py entrada.md [-s estilo.css] [-o salida.html] [-hl estilo_pygments]
"""

import re
import sys
import html
import argparse
import markdown
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
from pygments.util import ClassNotFound

# Versión de Mermaid del CDN; mantenerla alineada con la que trae mmdc
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.esm.min.mjs"

# Alias de lenguaje -> nombre de lexer de Pygments
LANG_ALIASES = {
    'js': 'javascript', 'javascript': 'javascript', 'mongodb': 'javascript',
    'jsx': 'jsx', 'react': 'jsx',
    'tsx': 'tsx', 'typescript-jsx': 'tsx',
    'ts': 'typescript', 'typescript': 'typescript',
    'py': 'python', 'python': 'python',
    'sh': 'bash', 'bash': 'bash', 'shell': 'bash',
}

# Apertura de bloque: indentación, cerco (``` o ~~~) y lenguaje opcional.
# En cercos de backticks el resto de la línea no puede contener backticks
# (así "```as const```: ..." no se confunde con un bloque).
FENCE_OPEN_RE = re.compile(r'^( *)(`{3,}|~{3,})[ \t]*([^\s`{]*)(.*)$')
LIST_ITEM_RE = re.compile(r'^( *)([-*+]|\d+[.)])( +|$)')


class FencedBlockPreprocessor(markdown.preprocessors.Preprocessor):
    """
    Procesa los bloques de código cercados (también los indentados dentro de
    listas) y normaliza la indentación de las listas anidadas.

    Python-Markdown exige 4 espacios por nivel de lista; los apuntes suelen
    usar 2 o 3. Se calcula la profundidad de cada ítem con una pila y se
    reindenta a 4*profundidad. Cada bloque se renderiza a HTML, se guarda en
    el htmlStash y en el texto queda solo el placeholder, indentado al nivel
    de la lista que lo contiene.
    """

    def __init__(self, md, highlight_style='default'):
        super().__init__(md)
        self.highlight_style = highlight_style

    def run(self, lines):
        salida = []
        pila = []  # indentación del marcador de cada ítem de lista abierto
        tras_bloque = False  # hubo un bloque en el ítem actual (el ítem ya es "loose")
        i = 0
        while i < len(lines):
            linea = lines[i]
            apertura = FENCE_OPEN_RE.match(linea)
            if apertura and not (apertura.group(2)[0] == '`' and '`' in apertura.group(4)):
                cierre = self._buscar_cierre(lines, i + 1, apertura.group(2))
                if cierre is None:
                    print(f"Advertencia: bloque de código sin cerrar en la línea {i + 1}")
                else:
                    indent = len(apertura.group(1))
                    profundidad = self._profundidad(pila, indent)
                    codigo = '\n'.join(self._desindentar(l, indent) for l in lines[i + 1:cierre])
                    placeholder = self.md.htmlStash.store(self._renderizar(apertura.group(3) or None, codigo))
                    salida += ['', ' ' * (4 * profundidad) + placeholder, '']
                    tras_bloque = True
                    i = cierre + 1
                    continue

            item = LIST_ITEM_RE.match(linea)
            if item:
                indent = len(item.group(1))
                profundidad = self._profundidad(pila, indent)
                pila.append(indent)
                linea = ' ' * (4 * profundidad) + linea[indent:]
                # Tras un bloque, el texto que sigue es un párrafo y Markdown
                # absorbería el próximo ítem como continuación si no hay línea en blanco
                if tras_bloque and salida and salida[-1].strip():
                    salida.append('')
                tras_bloque = False
            elif linea.strip() and not linea.startswith(' '):
                # Texto sin indentar: cierra cualquier lista abierta
                pila.clear()
                tras_bloque = False

            salida.append(linea)
            i += 1
        return salida

    @staticmethod
    def _profundidad(pila, indent):
        while pila and pila[-1] >= indent:
            pila.pop()
        return len(pila)

    @staticmethod
    def _buscar_cierre(lines, desde, cerco):
        cierre_re = re.compile(r'^ *' + re.escape(cerco[0]) + '{' + str(len(cerco)) + r',}[ \t]*$')
        for j in range(desde, len(lines)):
            if cierre_re.match(lines[j]):
                return j
        return None

    @staticmethod
    def _desindentar(linea, indent):
        espacios = len(linea) - len(linea.lstrip(' '))
        return linea[min(espacios, indent):]

    def _renderizar(self, lang, codigo):
        if not codigo.strip():
            return f'<pre class="empty-code-block">{html.escape(codigo)}</pre>'

        if lang and lang.lower() == 'svg':
            return f'<div class="svg-container">\n{codigo}\n</div>'

        if lang and lang.lower() == 'mermaid':
            # Escapado: así "<br/>" o "A<-->B" llegan como texto a Mermaid
            return f'<div class="mermaid">\n{html.escape(codigo, quote=False)}\n</div>'

        nombre = LANG_ALIASES.get(lang.lower(), lang) if lang else 'text'
        try:
            lexer = get_lexer_by_name(nombre)
        except ClassNotFound:
            print(f"Advertencia: no hay lexer para '{lang}', se usa texto plano.")
            lexer = TextLexer()

        formatter = HtmlFormatter(cssclass=f'highlight language-{lang or "text"}', style=self.highlight_style)
        return highlight(codigo + '\n', lexer, formatter)


class FencedBlockExtension(markdown.Extension):
    def __init__(self, highlight_style='default'):
        super().__init__()
        self.highlight_style = highlight_style

    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(FencedBlockPreprocessor(md, self.highlight_style), 'fenced_blocks', 25)


def _reglas_por_lenguaje(lenguajes, reglas):
    """Genera reglas CSS para varios lenguajes sin repetirlas a mano.
    El div de Pygments lleva ambas clases: 'highlight language-xxx'."""
    css = []
    for tokens, decl in reglas:
        selectores = ', '.join(f'.highlight.language-{lang} .{t}' for lang in lenguajes for t in tokens)
        css.append(f'        {selectores} {{ {decl} }}')
    return css


# Colores tipo GitHub para JSX/TSX
REGLAS_JSX = [
    (('k', 'kd', 'kr'), 'color: #af00db !important; font-weight: normal;'),  # palabras clave
    (('nx', 'nf'), 'color: #0969da !important;'),                           # funciones / variables
    (('nt', 'nc'), 'color: #116329 !important;'),                           # tags / componentes
    (('o', 'p'), 'color: #666666 !important;'),                             # operadores / puntuación
    (('na',), 'color: #0969da !important;'),                                # atributos
    (('s', 's1', 's2'), 'color: #0a3069 !important;'),                      # strings
    (('c', 'c1', 'cm'), 'color: #656d76 !important; font-style: italic;'),  # comentarios
    (('m', 'mi', 'mf'), 'color: #0969da !important;'),                      # números
]

BASE_CSS = [
    '        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; padding: 20px; }',
    # Bloque que reemplaza al h1
    '        #main-title-block { background-color: #2e2e2e; color: #f0f0f0; padding: 18px; border-radius: 10px; border: 1px solid #444; box-shadow: 0 2px 5px rgba(0,0,0,0.2); font-size: 1.8em; font-weight: bold; margin-bottom: 20px; text-align: center; }',
    '        pre:not(.highlight pre) { background-color: #fef6e4; color: #2e2e2e; padding: 12px; border-radius: 5px; overflow-x: auto; border: 1px solid #f0e6d4; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 15px 0; }',
    '        code { font-family: "Courier New", Courier, monospace; }',
    # Contenedor externo del resaltado; el pre interno no repite bordes ni fondo
    '        .highlight { padding: 0; border-radius: 5px; margin: 15px 0; background-color: #fef6e4 !important; border: 1px solid #f0e6d4; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }',
    '        .highlight pre { background: none; border: none; box-shadow: none; padding: 12px; margin: 0; border-radius: 0; }',
    # Colores generales de tokens
    '        .highlight .c, .highlight .c1, .highlight .cm { color: #9a8052 !important; font-style: italic; }',
    '        .highlight .k, .highlight .kd, .highlight .kn { color: #8250df !important; font-weight: normal; }',
    '        .highlight .s, .highlight .s1, .highlight .s2, .highlight .sb, .highlight .si { color: #327d41 !important; }',
    '        .highlight .m, .highlight .mi, .highlight .mf { color: #606060 !important; }',
    '        .highlight .o, .highlight .ow { color: #666666 !important; font-weight: normal; }',
    '        .highlight .kc, .highlight .no { color: #9a5b13 !important; }',
    '        .highlight .nf, .highlight .nb, .highlight .nx { color: #606060 !important; font-weight: normal; }',
    '        .highlight .p { color: #666666 !important; font-weight: normal; }',
    *_reglas_por_lenguaje(('jsx', 'react', 'tsx'), REGLAS_JSX),
    '        .highlight.language-tsx .kt { color: #0969da !important; }',  # tipos TypeScript
    # Tags JSX de cierre que el lexer de JS marca como error
    '        .highlight.language-javascript .err, .highlight.language-js .err { color: #116329 !important; }',
    '        .highlight span { background: none !important; border: none !important; box-shadow: none !important; text-decoration: none !important; outline: none !important; }',
    '        .svg-container { margin: 15px 0; text-align: center; padding: 10px; }',
    '        .svg-container svg { max-width: 100%; height: auto; }',
    '        .mermaid { margin: 15px 0; text-align: center; }',
    '        .mermaid svg { max-width: 100%; height: auto; }',
    '        .empty-code-block { background-color: #fef6e4; color: #2e2e2e; padding: 12px; border-radius: 5px; margin: 15px 0; font-family: monospace; border: 1px solid #f0e6d4; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }',
    '        img { max-width: 100%; height: auto; }',
    '        table { border-collapse: collapse; width: 100%; }',
    '        th, td { border: 1px solid #ddd; padding: 8px; }',
    '        th { background-color: #f2f2f2; }',
    '        .chapter-container { background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }',
    '        .chapter-container h2 { margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px; color: #444; }',
]


def list_available_styles():
    """Devuelve la lista de estilos de Pygments disponibles."""
    styles = sorted(get_all_styles())
    return ("Estilos de resaltado disponibles:\n"
            " Todos: " + ", ".join(styles) + "\n\n"
            " Populares:\n"
            " - Claros: default, friendly, colorful, autumn, emacs\n"
            " - Oscuros: monokai, dracula, solarized-dark, gruvbox-dark, one-dark\n")


def _envolver_capitulos(html_content):
    """Envuelve cada h2 y su contenido hasta el próximo h2 en un div.chapter-container."""
    h2s = list(re.finditer(r'<h2[^>]*>.*?</h2>', html_content, re.DOTALL))
    if not h2s:
        return html_content
    partes = [html_content[:h2s[0].start()]]
    for i, m in enumerate(h2s):
        fin = h2s[i + 1].start() if i + 1 < len(h2s) else len(html_content)
        partes.append(f'<div class="chapter-container">{html_content[m.start():fin]}</div>')
    return ''.join(partes)


def _extraer_titulo(html_content, titulo_por_defecto):
    """Reemplaza el primer h1 por #main-title-block y devuelve (html, título en texto)."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if not m:
        return html_content, titulo_por_defecto
    bloque = f'<div id="main-title-block"><span>{m.group(1)}</span></div>'
    titulo = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return html_content[:m.start()] + bloque + html_content[m.end():], titulo


def convert_markdown_to_html(md_file, css_file=None, output_file=None, highlight_style='default'):
    """Convierte md_file a HTML y devuelve la ruta del archivo generado."""
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"Error: no existe el archivo {md_file}")
        sys.exit(1)

    html_path = Path(output_file) if output_file else md_path.with_suffix('.html')
    md_content = md_path.read_text(encoding='utf-8')

    if highlight_style not in get_all_styles():
        print(f"Advertencia: no existe el estilo '{highlight_style}', se usa 'default'.")
        highlight_style = 'default'
    pygments_css = HtmlFormatter(style=highlight_style).get_style_defs('.highlight')

    html_content = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',
            FencedBlockExtension(highlight_style),
        ]
    )

    html_content = _envolver_capitulos(html_content)
    html_content, titulo = _extraer_titulo(html_content, md_path.stem)

    html_doc = [
        '<!DOCTYPE html>',
        '<html lang="es">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'    <title>{html.escape(titulo)}</title>',
        '    <style>',
        pygments_css,
        '    </style>',
        '    <style>',
        *BASE_CSS,
        '    </style>',
    ]

    if css_file:
        css_path = Path(css_file)
        if css_path.exists():
            html_doc += ['    <style>', f'        /* CSS de {css_path.name} */',
                         css_path.read_text(encoding='utf-8'), '    </style>']
            print(f"CSS embebido desde {css_file}")
        else:
            print(f"Advertencia: no existe el archivo CSS {css_file}")

    html_doc += [
        '</head>',
        '<body>',
        html_content,
        '    <script type="module">',
        f'        import mermaid from "{MERMAID_CDN}";',
        '        mermaid.initialize({',
        '            startOnLoad: true,',
        '            theme: "default",',
        '            securityLevel: "loose",',
        '            flowchart: {',
        '                useMaxWidth: true,',
        '                htmlLabels: true',
        '            }',
        '        });',
        '    </script>',
        '</body>',
        '</html>',
    ]

    html_path.write_text('\n'.join(html_doc), encoding='utf-8')
    print(f"Convertido {md_file} -> {html_path}")
    return str(html_path)


def main():
    parser = argparse.ArgumentParser(description='Convierte Markdown a HTML con resaltado de sintaxis y CSS opcional.')
    parser.add_argument('input', help='Archivo Markdown de entrada', nargs='?')
    parser.add_argument('-s', '--style', help='Archivo CSS a embeber')
    parser.add_argument('-o', '--output', help='Archivo HTML de salida')
    parser.add_argument('-hl', '--highlight', default='default', help='Estilo de Pygments (por defecto: default)')
    parser.add_argument('-ls', '--list-styles', action='store_true', help='Lista los estilos de Pygments disponibles')
    args = parser.parse_args()

    if args.list_styles:
        print(list_available_styles())
        return
    if not args.input:
        parser.error("falta el archivo de entrada")

    convert_markdown_to_html(args.input, args.style, args.output, args.highlight)


if __name__ == "__main__":
    main()
