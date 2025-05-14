#!/usr/bin/env python3
"""
md2html.py - Convert Markdown files to HTML with optional CSS styling and syntax highlighting

Usage:
    python md2html.py input.md [-s style.css] [-o output.html] [-hl highlight_style]
"""

import os
import sys
import argparse
import markdown
import shutil
from pathlib import Path
from pygments import highlight
from pygments.lexers import JavascriptLexer, get_lexer_by_name
from pygments.lexers.python import PythonLexer
from pygments.lexers.shell import BashLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
from pygments.util import ClassNotFound
from pygments.lexers.special import TextLexer

class EnhancedSyntaxExtension(markdown.Extension):
    """
    Markdown extension for syntax highlighting with focus on MongoDB, JavaScript, Python, and Bash
    """
    def extendMarkdown(self, md):
        md.registerExtension(self)
        
        # Replace the default code block processor with our custom one
        md.preprocessors.register(EnhancedSyntaxPreprocessor(md), 'enhanced_syntax', 175)
        
class EnhancedSyntaxPreprocessor(markdown.preprocessors.Preprocessor):
    """
    Preprocessor to handle code blocks with MongoDB, JavaScript, Python, and Bash syntax highlighting
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
                
            # Handle language selection with good defaults
            if original_lang is None:
                # Default to plain text if no language specified
                lang = 'text'
            elif original_lang.lower() in ('js', 'javascript', 'mongodb'):
                lang = 'javascript'
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
                    formatter = HtmlFormatter(cssclass=f'highlight language-{original_lang or "text"}', style='monokai')
                    highlighted = highlight(code, lexer, formatter)
                except Exception as e:
                    print(f"Warning: Error highlighting code: {str(e)}. Using plain text fallback.")
                    # Use TextLexer as a fallback for problematic code
                    formatter = HtmlFormatter(cssclass='highlight language-text', style='monokai')
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
                    else:
                        # Use TextLexer as a last resort for any unrecognized language
                        lexer = TextLexer()
                    
                    formatter = HtmlFormatter(cssclass=f'highlight language-{original_lang or "text"}', style='monokai')
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
    
    # Group styles into categories (approximation)
    dark_styles = [
        'monokai', 'dracula', 'fruity', 'gruvbox-dark', 'inkpot', 
        'material-theme', 'native', 'nord', 'nord-darker', 'one-dark', 
        'paraiso-dark', 'rrt', 'solarized-dark', 'stata-dark', 'tango', 
        'vim', 'vs-dark', 'zenburn'
    ]
    
    # Create formatted list
    style_list = "Available highlighting styles:\n"
    style_list += " All styles: " + ", ".join(styles) + "\n\n"
    style_list += " Popular styles:\n"
    style_list += " - Light: default, friendly, colorful, autumn, emacs, solarized-light\n"
    style_list += " - Dark: monokai, dracula, solarized-dark, gruvbox-dark, one-dark\n"
    
    return style_list

def convert_markdown_to_html(md_file, css_file=None, output_file=None, highlight_style='monokai'):
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
    try:
        pygments_formatter = HtmlFormatter(style=highlight_style)
        print(f"Using syntax highlighting style: {highlight_style}")
    except Exception:
        print(f"Warning: Invalid highlight style '{highlight_style}'. Using 'monokai' instead.")
        pygments_formatter = HtmlFormatter(style='monokai')
    
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
                    
                # Handle language selection with good defaults
                if original_lang is None:
                    # Default to plain text if no language specified
                    lang = 'text'
                elif original_lang.lower() in ('js', 'javascript', 'mongodb'):
                    lang = 'javascript'
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
                        else:
                            # Use TextLexer as a last resort for any unrecognized language
                            lexer = TextLexer()
                        
                        formatter = HtmlFormatter(cssclass=f'highlight language-{original_lang or "text"}', style=highlight_style)
                        highlighted = highlight(code, lexer, formatter)
                    except Exception as e:
                        print(f"Warning: Error highlighting fallback code: {str(e)}. Using simple pre tag.")
                        # If all else fails, just wrap in a pre tag
                        highlighted = f'<pre class="highlight-error">{code}</pre>'
                
                # Ensure we replace the exact original code block
                original_block = f'```{original_lang or ""}\n{code}```'
                text = text.replace(original_block, highlighted, 1)
                
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
    
    html_doc.append(f'    <title>{title}</title>')
    
    # Add Pygments CSS for syntax highlighting
    html_doc.append('    <style>')
    html_doc.append(pygments_css)
    html_doc.append('    </style>')
    
    # Add default styling for readability
    html_doc.append('    <style>')
    html_doc.append('        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; padding: 20px; }')
    html_doc.append('        pre { background-color: #1a1a35; color: #f8f8f2; padding: 5px; border-radius: 5px; overflow-x: auto; }')
    html_doc.append('        code { font-family: "Courier New", Courier, monospace; }')
    html_doc.append('        img { max-width: 100%; height: auto; }')
    html_doc.append('        table { border-collapse: collapse; width: 100%; }')
    html_doc.append('        th, td { border: 1px solid #ddd; padding: 8px; }')
    html_doc.append('        th { background-color: #f2f2f2; }')
    html_doc.append('        .highlight { padding: 5px; border-radius: 5px; margin: 5px 0; background-color: #1a1a35 !important; }')
    html_doc.append('        .empty-code-block { background-color: #1a1a35; color: #f8f8f2; padding: 5px; border-radius: 5px; margin: 5px 0; font-family: monospace; }')
    html_doc.append('        .highlight-error { background-color: #1a1a35; color: #f08080; padding: 5px; border-radius: 5px; margin: 5px 0; font-family: monospace; }')
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
    parser.add_argument('input', help='Path to the input Markdown file')
    parser.add_argument('-s', '--style', help='Path to a CSS file to include')
    parser.add_argument('-o', '--output', help='Path for the output HTML file')
    parser.add_argument('-hl', '--highlight', default='monokai', help='Syntax highlighting style (default: monokai)')
    parser.add_argument('-ls', '--list-styles', action='store_true', help='List all available syntax highlighting styles')
    
    args = parser.parse_args()
    
    # If --list-styles is specified, just list styles and exit
    if args.list_styles:
        print(list_available_styles())
        return
    
    convert_markdown_to_html(args.input, args.style, args.output, args.highlight)

if __name__ == "__main__":
    main()