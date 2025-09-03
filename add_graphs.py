#!/usr/bin/env python3
"""
Convert Mermaid code blocks in HTML to inline SVG graphs.
"""
import os
import re
import sys
import argparse
from bs4 import BeautifulSoup, Tag

def find_mermaid_blocks(soup, verbose=False):
    """Find all Mermaid code blocks in the HTML."""
    mermaid_blocks = []
    
    # Method 1: Find divs with class "mermaid" (new md2html.py format)
    for div in soup.find_all('div', class_='mermaid'):
        mermaid_blocks.append(div)
        if verbose:
            print(f"Found Mermaid div: {div.get_text()[:50]}...")
    
    # Method 2: Find pre tags with language-mermaid class (legacy support)
    for pre in soup.find_all('pre', class_=lambda c: c and 'language-mermaid' in c):
        mermaid_blocks.append(pre)
        if verbose:
            print(f"Found Mermaid pre: {pre.get_text()[:50]}...")
    
    # Method 3: Find divs with language-mermaid class that contain pre tags
    for div in soup.find_all('div', class_=lambda c: c and 'language-mermaid' in c):
        if div not in mermaid_blocks:  # Avoid duplicates
            mermaid_blocks.append(div)
            if verbose:
                print(f"Found Mermaid div with language class: {div.get_text()[:50]}...")
    
    # Method 4: Find any pre tags that look like they contain Mermaid code
    for pre in soup.find_all('pre'):
        if pre in mermaid_blocks:
            continue  # Skip if already found
            
        code = pre.text.strip()
        if any(keyword in code for keyword in ['graph ', 'flowchart ', 'sequenceDiagram', 'classDiagram']):
            mermaid_blocks.append(pre)
            if verbose:
                print(f"Found Mermaid-like pre: {code[:50]}...")
    
    return mermaid_blocks

def extract_mermaid_code(element):
    """Extract the Mermaid code from an element."""
    # If it's a div with class "mermaid", get its text content directly
    if element.name == 'div' and 'mermaid' in element.get('class', []):
        code = element.get_text().strip()
    # If it's a div, find the pre tag inside it
    elif element.name == 'div':
        pre = element.find('pre')
        if pre:
            code = pre.text.strip()
        else:
            code = element.text.strip()
    else:
        code = element.text.strip()
    
    # Clean up the code
    if code.startswith('```') and code.endswith('```'):
        code = code[3:-3].strip()
    if code.startswith('mermaid'):
        code = code[7:].strip()

    return code

def create_mermaid_div(code):
    """Create a div with Mermaid code that will be rendered by mermaid.js."""
    div = Tag(name='div')
    div['class'] = 'mermaid'
    div['style'] = 'text-align: center; max-width: 100%; overflow: visible; margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;'
    
    # Simplemente agregar el código Mermaid como texto, sin pre tags adicionales
    div.string = code
    
    return div

def convert_to_inline_styles(soup):
    """Convert all CSS styles to inline styles."""
    # Process all style tags
    for style in soup.find_all('style'):
        if not style.string:
            continue
            
        # Very simple CSS parser
        css_text = style.string
        rules = re.findall(r'([^{]+){([^}]+)}', css_text)
        
        for selector, style_block in rules:
            selector = selector.strip()
            styles = {}
            
            # Extract properties
            for prop in style_block.split(';'):
                prop = prop.strip()
                if not prop:
                    continue
                parts = prop.split(':', 1)
                if len(parts) == 2:
                    styles[parts[0].strip()] = parts[1].strip()
            
            # Apply styles to matching elements
            try:
                if selector.startswith('.'):
                    # Class selector
                    class_name = selector[1:]
                    elements = soup.find_all(class_=lambda c: c and class_name in c.split())
                elif selector.startswith('#'):
                    # ID selector
                    id_name = selector[1:]
                    elements = [soup.find(id=id_name)] if soup.find(id=id_name) else []
                else:
                    # Tag or complex selector
                    elements = soup.select(selector)
                
                for element in elements:
                    if not element:
                        continue
                        
                    existing_style = element.get('style', '')
                    style_parts = []
                    
                    if existing_style:
                        style_parts.append(existing_style.rstrip(';'))
                    
                    for prop, value in styles.items():
                        style_parts.append(f"{prop}: {value}")
                    
                    element['style'] = '; '.join(style_parts)
            except Exception as e:
                print(f"Error applying style for selector '{selector}': {e}")
        
        # Remove the style tag
        style.decompose()

def main():
    parser = argparse.ArgumentParser(description='Convert Mermaid code blocks in HTML to inline SVG graphs')
    parser.add_argument('input_file', help='Input HTML file')
    parser.add_argument('-o', '--output', help='Output HTML file (default: input_file_mermaid.html)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    # Show help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nExample usage:")
        print("  python add_graphs.py objetos.html")
        print("  python add_graphs.py objetos.html -v")
        print("  python add_graphs.py path/to/objetos.html -o path/to/converted.html")
        print("  python add_graphs.py objetos.html --output converted.html --verbose")
        return
    
    args = parser.parse_args()
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        input_dir = os.path.dirname(args.input_file)
        input_base = os.path.basename(args.input_file)
        name, ext = os.path.splitext(input_base)
        output_file = os.path.join(input_dir, f"{name}_mermaid{ext}")
    
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read input file
    with open(args.input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find Mermaid blocks
    mermaid_blocks = find_mermaid_blocks(soup, args.verbose)
    
    if not mermaid_blocks:
        if args.verbose:
            print("No Mermaid code blocks found in the input file.")
            print("Searched for:")
            print("- <div class='mermaid'>")
            print("- <pre class='language-mermaid'>") 
            print("- <div class='language-mermaid'>")
            print("- Pre tags containing 'graph', 'flowchart', 'sequenceDiagram', or 'classDiagram'")
            print("Creating output file as a copy of the input file...")
        else:
            print("No Mermaid blocks found. Creating copy of input file...")
        
        # Write the original content to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Output file saved to: {output_file}")
        return
    
    print(f"Found {len(mermaid_blocks)} Mermaid code block(s)")
    
    # Replace each Mermaid block with a renderable div
    for i, block in enumerate(mermaid_blocks):
        code = extract_mermaid_code(block)
        if args.verbose:
            print(f"Processing block {i+1}: {code[:100]}...")
        
        # If it's already a properly formatted Mermaid div, leave it as is
        if (block.name == 'div' and 
            'mermaid' in block.get('class', []) and 
            not block.find('pre')):
            if args.verbose:
                print(f"Block {i+1} is already properly formatted, skipping...")
            continue
        
        mermaid_div = create_mermaid_div(code)
        block.replace_with(mermaid_div)
        if args.verbose:
            print(f"Replaced block {i+1} with Mermaid div")
    
    # Apply inline styles
    if args.verbose:
        print("Converting CSS to inline styles...")
    convert_to_inline_styles(soup)
    
    # Ensure we have a body tag
    if not soup.body:
        if soup.html:
            body = soup.new_tag('body')
            # Move all content that should be in body
            for element in soup.html.contents[:]:
                if element.name not in ['head', 'body']:
                    body.append(element)
            soup.html.append(body)
        else:
            html = soup.new_tag('html')
            body = soup.new_tag('body')
            # Move all content to body
            for element in soup.contents[:]:
                body.append(element)
            html.append(body)
            soup.append(html)
    
    # Check if Mermaid script already exists
    existing_script = soup.find('script', src=lambda x: x and 'mermaid' in x)
    
    if not existing_script:
        if args.verbose:
            print("Adding Mermaid.js script...")
        # Add Mermaid.js script at the end of the body
        script = soup.new_tag('script')
        script['src'] = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js'
        soup.body.append(script)
        
        # Add initialization script
        init_script = soup.new_tag('script')
        init_script.string = """
        document.addEventListener('DOMContentLoaded', function () {
            // Función para reemplazar caracteres escapados
            function unescapeHTML(html) {
                return html
                    .replace(/<pre class="mermaid">/g, "")
                    .replace(/<\/pre>/g, "")
                    .replace(/&lt;/g, '<')
                    .replace(/&gt;/g, '>')
                    .replace(/&amp;/g, '&')
                    .replace(/&quot;/g, '"');
            }

            // Buscar todos los divs con clase mermaid
            const mermaidDivs = document.querySelectorAll('div.mermaid');
            console.log('Found', mermaidDivs.length, 'Mermaid divs');

            // Procesar cada div
            mermaidDivs.forEach(function (div, index) {
                // Obtener el contenido actual y desescaparlo
                const escapedContent = div.innerHTML;
                const unescapedContent = unescapeHTML(escapedContent);

                // Reemplazar el contenido
                div.innerHTML = unescapedContent;
                console.log('Processed Mermaid div', index + 1, ':', unescapedContent.substring(0, 50));
            });

            // Inicializar Mermaid después de hacer los reemplazos
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                fontFamily: 'Arial, sans-serif',
                securityLevel: 'loose',
                flowchart: {
                    htmlLabels: true,
                    curve: 'basis'
                }
            });
        });
        """
        soup.body.append(init_script)
    else:
        if args.verbose:
            print("Mermaid script already exists in the document.")
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Converted file saved to: {output_file}")

if __name__ == "__main__":
    main()