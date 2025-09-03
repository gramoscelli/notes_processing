#!/usr/bin/env python3
"""
md2html.py - Convert Markdown files to HTML with optional CSS styling and syntax highlighting

Usage:
    python md2html.py input.md [-s style.css] [-o output.html] [-hl highlight_style]
"""

import sys
import argparse
import markdown
from pathlib import Path
from pygments import highlight
from pygments.lexers import JavascriptLexer, get_lexer_by_name
from pygments.lexers.python import PythonLexer
from pygments.lexers.shell import BashLexer
from pygments.lexers.javascript import JavascriptLexer, TypeScriptLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
from pygments.util import ClassNotFound
from pygments.lexers.special import TextLexer

class EnhancedSyntaxExtension(markdown.Extension):
    """
    Markdown extension for syntax highlighting with focus on MongoDB, JavaScript, JSX, Python, and Bash
    """
    def extendMarkdown(self, md):
        md.registerExtension(self)
        
        # Replace the default code block processor with our custom one
        md.preprocessors.register(EnhancedSyntaxPreprocessor(md), 'enhanced_syntax', 175)
        
class EnhancedSyntaxPreprocessor(markdown.preprocessors.Preprocessor):
    """
    Preprocessor to handle code blocks with MongoDB, JavaScript, JSX, Python, and Bash syntax highlighting
    """
    FENCED_BLOCK_RE = r'```([\w+-]+)?\n([\s\S]*?)```'
    
    def __init__(self, md):
        super().__init__(md)
        
    def run(self, lines):
        import re
        
        text = '\n'.join(lines)
        while True:
            m = re.search(self.FENCED_BLOCK_RE, text, re.MULTILINE)
            if not m:
                break
                
            original_lang = m.group(1)
            code = m.group(2)
            
            # Skip empty code blocks or blocks with just whitespace
            if not code or code.strip() == '':
                # Replace with a simple pre tag to avoid errors
                original_block = f'```{original_lang or ""}\n{code}```'
                replacement = f'<pre class="empty-code-block">{code}</pre>'
                text = text.replace(original_block, replacement, 1)
                continue
                
            # Handle language selection with good defaults including JSX
            if original_lang is None:
                # Default to plain text if no language specified
                lang = 'text'
            elif original_lang.lower() in ('js', 'javascript', 'mongodb'):
                lang = 'javascript'
            elif original_lang.lower() in ('jsx', 'react'):
                lang = 'jsx'
            elif original_lang.lower() in ('tsx', 'typescript-jsx'):
                lang = 'tsx'
            elif original_lang.lower() in ('ts', 'typescript'):
                lang = 'typescript'
            elif original_lang.lower() in ('py', 'python'):
                lang = 'python'
            elif original_lang.lower() in ('sh', 'bash', 'shell'):
                lang = 'bash'
            else:
                # Keep the original language identifier for generic handling
                lang = original_lang
                
            try:
                # Try to get a lexer for the specified language
                lexer = get_lexer_by_name(lang)
                
                # Try highlighting the code, but handle potential errors
                try:
                    formatter = HtmlFormatter(cssclass=f'highlight language-{original_lang or "text"}', style='default')
                    highlighted = highlight(code, lexer, formatter)
                except Exception as e:
                    print(f"Warning: Error highlighting code: {str(e)}. Using plain text fallback.")
                    # Use TextLexer as a fallback for problematic code
                    formatter = HtmlFormatter(cssclass='highlight language-text', style='default')
                    highlighted = highlight(code, TextLexer(), formatter)
                    
            except ClassNotFound:
                # If lexer not found, select a fallback based on language hints
                print(f"Warning: No lexer found for language '{lang}'. Using fallback.")
                try:
                    if lang.lower() in ('py', 'python'):
                        lexer = PythonLexer()
                    elif lang.lower() in ('sh', 'bash', 'shell'):
                        lexer = BashLexer()
                    elif lang.lower() in ('js', 'javascript', 'mongodb'):
                        lexer = JavascriptLexer()
                    elif lang.lower() in ('jsx', 'react'):
                        # Use JavaScript lexer for JSX - Pygments doesn't have a separate JSX lexer
                        lexer = JavascriptLexer()
                    elif lang.lower() in ('tsx', 'typescript-jsx'):
                        # Use TypeScript lexer for TSX
                        try:
                            lexer = TypeScriptLexer()
                        except:
                            lexer = JavascriptLexer()  # Fallback to JS if TS not available
                    elif lang.lower() in ('ts', 'typescript'):
                        try:
                            lexer = TypeScriptLexer()
                        except:
                            lexer = JavascriptLexer()  # Fallback to JS if TS not available
                    else:
                        # Use TextLexer as a last resort for any unrecognized language
                        lexer = TextLexer()
                    
                    formatter = HtmlFormatter(cssclass=f'highlight language-{original_lang or "text"}', style='default')
                    highlighted = highlight(code, lexer, formatter)
                except Exception as e:
                    print(f"Warning: Error highlighting fallback code: {str(e)}. Using simple pre tag.")
                    # If all else fails, just wrap in a pre tag
                    highlighted = f'<pre class="highlight-error">{code}</pre>'
            
            # Ensure we replace the exact original code block
            original_block = f'```{original_lang or ""}\n{code}```'
            text = text.replace(original_block, highlighted, 1)
            
        return text.split('\n')

def list_available_styles():
    """Return a formatted list of all available Pygments styles."""
    styles = sorted(list(get_all_styles()))
    
    # Create formatted list
    style_list = "Available highlighting styles:\n"
    style_list += " All styles: " + ", ".join(styles) + "\n\n"
    style_list += " Popular styles:\n"
    style_list += " - Light: default, friendly, colorful, autumn, emacs\n"
    style_list += " - Dark: monokai, dracula, solarized-dark, gruvbox-dark, one-dark\n"
    
    return style_list

def convert_markdown_to_html(md_file, css_file=None, output_file=None, highlight_style='default'):
    """
    Convert a Markdown file to HTML with optional CSS styling
    
    Args:
        md_file (str): Path to the Markdown file
        css_file (str, optional): Path to a CSS file to include
        output_file (str, optional): Path for the output HTML file
        highlight_style (str, optional): Pygments style for syntax highlighting
    
    Returns:
        str: Path to the generated HTML file
    """
    # Check if input file exists
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"Error: File not found: {md_file}")
        sys.exit(1)
    
    # Determine output file name if not specified
    if output_file:
        html_path = Path(output_file)
    else:
        html_path = md_path.with_suffix('.html')
    
    # Read markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Set up Pygments formatter with the specified style
    # Verificar si el estilo existe en Pygments
    available_styles = list(get_all_styles())
    
    if highlight_style not in available_styles:
        print(f"Warning: Style '{highlight_style}' not found. Available styles: {', '.join(available_styles[:10])}...")
        print(f"Using 'default' style instead.")
        highlight_style = 'default'
    
    try:
        pygments_formatter = HtmlFormatter(style=highlight_style)
        print(f"Using syntax highlighting style: {highlight_style}")
    except Exception as e:
        print(f"Warning: Error with highlight style '{highlight_style}': {str(e)}. Using 'default' instead.")
        pygments_formatter = HtmlFormatter(style='default')
    
    pygments_css = pygments_formatter.get_style_defs('.highlight')
    
    # Configure the Enhanced syntax extension to use the specified style
    class CustomEnhancedSyntaxPreprocessor(EnhancedSyntaxPreprocessor):
        def run(self, lines):
            import re
            from pygments.lexers.special import TextLexer
            
            text = '\n'.join(lines)
            
            while True:
                m = re.search(self.FENCED_BLOCK_RE, text, re.MULTILINE)
                if not m:
                    break
                    
                original_lang = m.group(1)
                code = m.group(2)
                
                # Skip empty code blocks or blocks with just whitespace
                if not code or code.strip() == '':
                    # Replace with a simple pre tag to avoid errors
                    original_block = f'```{original_lang or ""}\n{code}```'
                    replacement = f'<pre class="empty-code-block">{code}</pre>'
                    text = text.replace(original_block, replacement, 1)
                    continue
                    
                # Handle language selection with good defaults including JSX
                if original_lang is None:
                    # Default to plain text if no language specified
                    lang = 'text'
                elif original_lang.lower() in ('js', 'javascript', 'mongodb'):
                    lang = 'javascript'
                elif original_lang.lower() in ('jsx', 'react'):
                    lang = 'jsx'
                elif original_lang.lower() in ('tsx', 'typescript-jsx'):
                    lang = 'tsx'
                elif original_lang.lower() in ('ts', 'typescript'):
                    lang = 'typescript'
                elif original_lang.lower() in ('py', 'python'):
                    lang = 'python'
                elif original_lang.lower() in ('sh', 'bash', 'shell'):
                    lang = 'bash'
                else:
                    # Keep the original language identifier for generic handling
                    lang = original_lang
                
                try:
                    # Try to get a lexer for the specified language
                    lexer = get_lexer_by_name(lang)
                    
                    # Try highlighting the code, but handle potential errors
                    try:
                        formatter = HtmlFormatter(cssclass=f'highlight language-{original_lang or "text"}', style=highlight_style)
                        highlighted = highlight(code, lexer, formatter)
                    except Exception as e:
                        print(f"Warning: Error highlighting code: {str(e)}. Using plain text fallback.")
                        # Use TextLexer as a fallback for problematic code
                        formatter = HtmlFormatter(cssclass='highlight language-text', style=highlight_style)
                        highlighted = highlight(code, TextLexer(), formatter)
                        
                except ClassNotFound:
                    # If lexer not found, select a fallback based on language hints
                    print(f"Warning: No lexer found for language '{lang}'. Using fallback.")
                    try:
                        if lang.lower() in ('py', 'python'):
                            lexer = PythonLexer()
                        elif lang.lower() in ('sh', 'bash', 'shell'):
                            lexer = BashLexer()
                        elif lang.lower() in ('js', 'javascript', 'mongodb'):
                            lexer = JavascriptLexer()
                        elif lang.lower() in ('jsx', 'react'):
                            # Use JavaScript lexer for JSX - Pygments doesn't have a separate JSX lexer
                            lexer = JavascriptLexer()
                        elif lang.lower() in ('tsx', 'typescript-jsx'):
                            # Use TypeScript lexer for TSX
                            try:
                                lexer = TypeScriptLexer()
                            except:
                                lexer = JavascriptLexer()  # Fallback to JS if TS not available
                        elif lang.lower() in ('ts', 'typescript'):
                            try:
                                lexer = TypeScriptLexer()
                            except:
                                lexer = JavascriptLexer()  # Fallback to JS if TS not available
                        else:
                            # Use TextLexer as a last resort for any unrecognized language
                            lexer = TextLexer()
                        
                        formatter = HtmlFormatter(cssclass=f'highlight language-{original_lang or "text"}', style=highlight_style)
                        highlighted = highlight(code, lexer, formatter)
                    except Exception as e:
                        print(f"Warning: Error highlighting fallback code: {str(e)}. Using simple pre tag.")
                        # If all else fails, just wrap in a pre tag
                        highlighted = f'<pre class="highlight-error">{code}</pre>'
                
                # Simple replacement without collapsible functionality
                replacement = highlighted
                
                # Ensure we replace the exact original code block
                original_block = f'```{original_lang or ""}\n{code}```'
                text = text.replace(original_block, replacement, 1)
                
            return text.split('\n')
    
    # Create custom extension with the specified highlight style
    class CustomEnhancedSyntaxExtension(markdown.Extension):
        def extendMarkdown(self, md):
            md.registerExtension(self)
            md.preprocessors.register(CustomEnhancedSyntaxPreprocessor(md), 'enhanced_syntax', 175)
    
    # Convert markdown to HTML with syntax highlighting
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',
            CustomEnhancedSyntaxExtension()  # Custom extension with the specified highlight style
        ]
    )
    
    # Add custom styling for h2 headers (chapters)
    # This will wrap each h2 and all content until the next h2 in a container
    import re
    
    # Process h2 headers and wrap them in chapter-container divs
    # Using a more robust approach to ensure all content is properly wrapped
    html_content_parts = []
    last_pos = 0
    
    # Find all h2 tags
    h2_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>', re.DOTALL)
    h2_matches = list(h2_pattern.finditer(html_content))
    
    if h2_matches:
        # Process content before the first h2 (if any)
        if h2_matches[0].start() > 0:
            html_content_parts.append(html_content[:h2_matches[0].start()])
        
        # Process each h2 section
        for i, match in enumerate(h2_matches):
            h2_start = match.start()
            h2_tag = match.group(0)
            
            # Find where this section ends (either at the next h2 or at the end of content)
            if i < len(h2_matches) - 1:
                section_end = h2_matches[i + 1].start()
            else:
                section_end = len(html_content)
            
            # Extract section content
            section_content = html_content[h2_start:section_end]
            
            # Wrap the section in a chapter-container div
            wrapped_section = f'<div class="chapter-container">{section_content}</div>'
            html_content_parts.append(wrapped_section)
            
            last_pos = section_end
        
        # Add any content after the last h2
        if last_pos < len(html_content):
            html_content_parts.append(html_content[last_pos:])
        
        # Replace the original content
        html_content = ''.join(html_content_parts)
    
    
    # Build the HTML document with syntax highlighting CSS and optional external CSS
    html_doc = []
    html_doc.append('<!DOCTYPE html>')
    html_doc.append('<html lang="en">')
    html_doc.append('<head>')
    html_doc.append('    <meta charset="UTF-8">')
    html_doc.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    
    # Extract title from the first heading or use the filename
    title = md_path.stem
    if html_content.find('<h1>') != -1:
        title_start = html_content.find('<h1>') + 4
        title_end = html_content.find('</h1>')
        if title_start != -1 and title_end != -1:
            title = html_content[title_start:title_end]

            # Replace h1 with a styled div
            h1_block = html_content[title_start - 4:title_end + 5]  # '<h1>...</h1>'
            new_block = f'<div id="main-title-block"><span>{title}</span></div>'
            html_content = html_content.replace(h1_block, new_block, 1)

    html_doc.append(f'    <title>{title}</title>')

    # Add Pygments CSS for syntax highlighting
    html_doc.append('    <style>')
    html_doc.append(pygments_css)
    html_doc.append('    </style>')

    # Add default styling for readability
    html_doc.append('    <style>')
    html_doc.append('        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; padding: 20px; }')

    # Estilo para el div que reemplaza al h1
    html_doc.append('        #main-title-block { background-color: #2e2e2e; color: #f0f0f0; padding: 18px; border-radius: 10px; border: 1px solid #444; box-shadow: 0 2px 5px rgba(0,0,0,0.2); font-size: 1.8em; font-weight: bold; margin-bottom: 20px; text-align: center; }')

    # Estilo para bloques pre fuera de .highlight
    html_doc.append('        pre:not(.highlight pre) { background-color: #fef6e4; color: #2e2e2e; padding: 12px; border-radius: 5px; overflow-x: auto; border: 1px solid #f0e6d4; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 15px 0; }')
    html_doc.append('        code { font-family: "Courier New", Courier, monospace; }')
    
    # Configuración mejorada para los bloques de resaltado de sintaxis (contenedor externo)
    html_doc.append('        .highlight { padding: 0; border-radius: 5px; margin: 15px 0; background-color: #fef6e4 !important; border: 1px solid #f0e6d4; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }')
    
    # Quitar bordes y fondos duplicados del pre dentro de .highlight
    html_doc.append('        .highlight pre { background: none; border: none; box-shadow: none; padding: 12px; margin: 0; border-radius: 0; }')
    
    # Configuración para las líneas de comentarios en los bloques de código
    html_doc.append('        .highlight .c, .highlight .c1, .highlight .cm { color: #9a8052 !important; font-style: italic; }') 
    
    # Configuración para las palabras clave en los bloques de código
    html_doc.append('        .highlight .k, .highlight .kd, .highlight .kn { color: #8250df !important; font-weight: normal; }')
    
    # Configuración para las cadenas de texto en los bloques de código
    html_doc.append('        .highlight .s, .highlight .s1, .highlight .s2, .highlight .sb, .highlight .si { color: #327d41 !important; }')
    
    # Configuración para los números en los bloques de código
    html_doc.append('        .highlight .m, .highlight .mi, .highlight .mf { color: #606060 !important; }')
    
    # Configuración para los operadores en los bloques de código
    html_doc.append('        .highlight .o, .highlight .ow { color: #666666 !important; font-weight: normal; }')
    
    # Configuración para las constantes en los bloques de código
    html_doc.append('        .highlight .kc, .highlight .no { color: #9a5b13 !important; }')
    
    # Configuración para las funciones y clases en los bloques de código
    html_doc.append('        .highlight .nf, .highlight .nb, .highlight .nx { color: #606060 !important; font-weight: normal; }')
    
    # Mejorar la visibilidad de paréntesis, corchetes, llaves, puntos y coma, etc.
    html_doc.append('        .highlight .p { color: #666666 !important; font-weight: normal; }')
    
    # JSX/React specific styling - Colores basados en la imagen proporcionada
    html_doc.append('        .language-jsx .highlight .k, .language-jsx .highlight .kd, .language-jsx .highlight .kr { color: #af00db !important; font-weight: normal; background: none !important; border: none !important; }')  # Keywords (function, const, return) - púrpura
    html_doc.append('        .language-jsx .highlight .nx, .language-jsx .highlight .nf { color: #0969da !important; background: none !important; border: none !important; }')  # Functions/variables - azul
    html_doc.append('        .language-jsx .highlight .nt { color: #116329 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Opening tags - verde
    html_doc.append('        .language-jsx .highlight .nc { color: #116329 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Component names - verde
    html_doc.append('        .language-jsx .highlight .o  { color: #666666 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Operators
    html_doc.append('        .language-jsx .highlight .p  { color: #666666 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Punctuation
    html_doc.append('        .language-jsx .highlight .na { color: #0969da !important; background: none !important; border: none !important; }')  # JSX attributes - azul
    html_doc.append('        .language-jsx .highlight .s, .language-jsx .highlight .s1, .language-jsx .highlight .s2 { color: #0a3069 !important; background: none !important; border: none !important; }')   # Strings - azul oscuro
    html_doc.append('        .language-jsx .highlight .c, .language-jsx .highlight .c1, .language-jsx .highlight .cm { color: #656d76 !important; font-style: italic; background: none !important; border: none !important; }')   # Comments - gris
    html_doc.append('        .language-jsx .highlight .m, .language-jsx .highlight .mi, .language-jsx .highlight .mf { color: #0969da !important; background: none !important; border: none !important; }')   # Numbers - azul
    
    html_doc.append('        .language-react .highlight .k, .language-react .highlight .kd, .language-react .highlight .kr { color: #af00db !important; font-weight: normal; background: none !important; border: none !important; }')  # Keywords - púrpura
    html_doc.append('        .language-react .highlight .nx, .language-react .highlight .nf { color: #0969da !important; background: none !important; border: none !important; }')  # Functions/variables - azul
    html_doc.append('        .language-react .highlight .nt { color: #116329 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Opening tags - verde
    html_doc.append('        .language-react .highlight .nc { color: #116329 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Component names - verde
    html_doc.append('        .language-react .highlight .o  { color: #666666 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Operators
    html_doc.append('        .language-react .highlight .p  { color: #666666 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Punctuation
    html_doc.append('        .language-react .highlight .na { color: #0969da !important; background: none !important; border: none !important; }')  # React attributes - azul
    html_doc.append('        .language-react .highlight .s, .language-react .highlight .s1, .language-react .highlight .s2 { color: #0a3069 !important; background: none !important; border: none !important; }')   # Strings - azul oscuro
    html_doc.append('        .language-react .highlight .c, .language-react .highlight .c1, .language-react .highlight .cm { color: #656d76 !important; font-style: italic; background: none !important; border: none !important; }')   # Comments - gris
    html_doc.append('        .language-react .highlight .m, .language-react .highlight .mi, .language-react .highlight .mf { color: #0969da !important; background: none !important; border: none !important; }')   # Numbers - azul
    
    # TSX specific styling - mismos colores con adición de tipos TypeScript
    html_doc.append('        .language-tsx .highlight .k, .language-tsx .highlight .kd, .language-tsx .highlight .kr { color: #af00db !important; font-weight: normal; background: none !important; border: none !important; }')  # Keywords - púrpura
    html_doc.append('        .language-tsx .highlight .nx, .language-tsx .highlight .nf { color: #0969da !important; background: none !important; border: none !important; }')  # Functions/variables - azul
    html_doc.append('        .language-tsx .highlight .nt { color: #116329 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Opening tags - verde
    html_doc.append('        .language-tsx .highlight .nc { color: #116329 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Component names - verde
    html_doc.append('        .language-tsx .highlight .o  { color: #666666 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Operators
    html_doc.append('        .language-tsx .highlight .p  { color: #666666 !important; background:none !important; border:none !important; box-shadow:none !important; outline:none !important; }')  # Punctuation
    html_doc.append('        .language-tsx .highlight .na { color: #0969da !important; background: none !important; border: none !important; }')  # TSX attributes - azul
    html_doc.append('        .language-tsx .highlight .s, .language-tsx .highlight .s1, .language-tsx .highlight .s2 { color: #0a3069 !important; background: none !important; border: none !important; }')   # Strings - azul oscuro
    html_doc.append('        .language-tsx .highlight .c, .language-tsx .highlight .c1, .language-tsx .highlight .cm { color: #656d76 !important; font-style: italic; background: none !important; border: none !important; }')   # Comments - gris
    html_doc.append('        .language-tsx .highlight .m, .language-tsx .highlight .mi, .language-tsx .highlight .mf { color: #0969da !important; background: none !important; border: none !important; }')   # Numbers - azul
    html_doc.append('        .language-tsx .highlight .kt { color: #0969da !important; background: none !important; border: none !important; }')   # TypeScript types - azul
    
    # JavaScript specific styling
    html_doc.append('        .language-javascript .highlight .err { color: #116329 !important; background: none !important; border: none !important; }')  # Error class (for JSX closing tags in JS) - verde
    html_doc.append('        .language-js .highlight .err { color: #116329 !important; background: none !important; border: none !important; }')  # Error class (for JSX closing tags in JS) - verde
    
    # Remover cualquier decoración adicional
    html_doc.append('        .highlight span { background: none !important; border: none !important; box-shadow: none !important; text-decoration: none !important; outline: none !important; }')
    
    # Otras configuraciones de estilo
    html_doc.append('        .empty-code-block { background-color: #fef6e4; color: #2e2e2e; padding: 12px; border-radius: 5px; margin: 15px 0; font-family: monospace; border: 1px solid #f0e6d4; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }')
    html_doc.append('        .highlight-error { background-color: #fef6e4; color: #000080; padding: 12px; border-radius: 5px; margin: 15px 0; font-family: monospace; border: 1px solid #f0e6d4; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }')
    
    html_doc.append('        img { max-width: 100%; height: auto; }')
    html_doc.append('        table { border-collapse: collapse; width: 100%; }')
    html_doc.append('        th, td { border: 1px solid #ddd; padding: 8px; }')
    html_doc.append('        th { background-color: #f2f2f2; }')
    html_doc.append('        .chapter-container { background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }')
    html_doc.append('        .chapter-container h2 { margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px; color: #444; }')
    html_doc.append('    </style>')
    
    # Include CSS if specified - embed the CSS content directly
    if css_file:
        css_path = Path(css_file)
        if css_path.exists():
            try:
                # Read the CSS file content
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                # Add the CSS content directly into the HTML head
                html_doc.append('    <style>')
                html_doc.append(f'        /* CSS from {css_path.name} */')
                html_doc.append(css_content)
                html_doc.append('    </style>')
                
                print(f"Embedded CSS from {css_file} directly into the HTML")
            except Exception as e:
                print(f"Warning: Could not read CSS file {css_file}: {str(e)}")
        else:
            print(f"Warning: CSS file not found: {css_file}")
    
    html_doc.append('</head>')
    html_doc.append('<body>')
    html_doc.append(html_content)
    html_doc.append('</body>')
    html_doc.append('</html>')
    
    # Write the HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_doc))
    
    print(f"Successfully converted {md_file} to {html_path}")
    return str(html_path)

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown files to HTML with optional CSS styling and syntax highlighting.')
    parser.add_argument('input', help='Path to the input Markdown file', nargs='?')
    parser.add_argument('-s', '--style', help='Path to a CSS file to include')
    parser.add_argument('-o', '--output', help='Path for the output HTML file')
    parser.add_argument('-hl', '--highlight', default='default', help='Syntax highlighting style (default: default)')
    parser.add_argument('-ls', '--list-styles', action='store_true', help='List all available syntax highlighting styles')
    
    args = parser.parse_args()
    
    # If --list-styles is specified, just list styles and exit
    if args.list_styles:
        print(list_available_styles())
        return
    
    # Check if input file is provided
    if not args.input:
        parser.error("the following arguments are required: input")
    
    convert_markdown_to_html(args.input, args.style, args.output, args.highlight)

if __name__ == "__main__":
    main()