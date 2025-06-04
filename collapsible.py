#!/usr/bin/env python3
import sys
import os
import argparse
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN POR DEFECTO ---
DEFAULT_MAX_LINES = 6
CSS_ID = "collapsible-styles"

# CSS y JS a inyectar en el <head>
COLLAPSIBLE_CSS = """
/* Estilos para el contenedor colapsable */
.collapsible-container {
  position: relative;
  overflow: hidden;
  transition: max-height 0.3s ease;
  border-radius: 8px;
  margin: 0;
}
.collapsible-container pre {
  margin: 0;
  line-height: 1.4; /* Forzar line-height consistente */
}
.collapsible-container .toggle-button {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255,255,255,0.9);
  border: 1px solid #ccc;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 4px 8px;
  border-radius: 4px;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.collapsible-container .toggle-button:hover {
  background: rgba(255,255,255,1);
}
/* Estilos para el botón de copiar */
.collapsible-container .copy-button {
  position: absolute;
  top: 8px;
  width: 24px;
  display: flex;           /* Usamos flexbox para centrar el icono/texto */
  align-items: center;
  justify-content: center;
  right: 48px;           /* A 40 px a la izquierda del botón de colapsar */
  background: rgba(255,255,255,0.9);
  border: 1px solid #ccc;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 4px 8px;
  border-radius: 4px;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.collapsible-container .copy-button:hover {
  background: rgba(255,255,255,1);
}
.collapsible-container .fade-overlay {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 42px;
  background: linear-gradient(
    to bottom, 
    rgba(255,249,229,0), 
    rgba(255,249,229,1)
  );
  pointer-events: none;
  z-index: 5;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}
.collapsible-container .ellipsis {
  position: absolute;
  bottom: 8px;
  width: 100%;
  text-align: center;
  color: #888;
  font-size: 18px;
  font-weight: bold;
  z-index: 6;
}
.collapsible-container.expanded .fade-overlay,
.collapsible-container.expanded .ellipsis {
  display: none;
}
"""

COLLAPSIBLE_JS = """(function() {
  function initCollapsibles() {
    // Esperar un poco para que los estilos se apliquen
    setTimeout(() => {
      document.querySelectorAll('.collapsible-container').forEach(container => {
        const pre = container.querySelector('pre');
        if (!pre) return;
        
        const maxLines = parseInt(container.dataset.maxLines, 10) || 6;
        
        // Crear un elemento temporal para medir line-height
        const tempSpan = document.createElement('span');
        tempSpan.style.visibility = 'hidden';
        tempSpan.style.position = 'absolute';
        tempSpan.style.fontSize = getComputedStyle(pre).fontSize;
        tempSpan.style.fontFamily = getComputedStyle(pre).fontFamily;
        tempSpan.style.lineHeight = '1.4';
        tempSpan.textContent = 'M';
        document.body.appendChild(tempSpan);
        
        const lineHeight = tempSpan.offsetHeight;
        document.body.removeChild(tempSpan);
        
        const fullHeight = pre.scrollHeight;
        const collapsedHeight = Math.ceil(lineHeight * maxLines);
        
        console.log('Debug:', {
          maxLines,
          lineHeight,
          fullHeight,
          collapsedHeight,
          shouldCollapse: fullHeight > collapsedHeight + 10
        });
        
        // Solo colapsar si realmente es necesario
        if (fullHeight <= collapsedHeight + 10) {
          return;
        }

        // Estado inicial: colapsado
        container.style.maxHeight = collapsedHeight + 'px';
        container.classList.add('collapsed');

         // === Aquí agregamos primero el botón de "copiar" ===
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-button';
        copyBtn.innerHTML = '📋';
        copyBtn.title = 'Copiar código';
        container.appendChild(copyBtn);

        // Evento para copiar el texto del <pre> al portapapeles
        copyBtn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          // Copiar el contenido de 'pre'
          const codeText = pre.innerText;
          navigator.clipboard.writeText(codeText).then(() => {
            // Opcional: retroalimentación breve (por ejemplo cambiar texto o color)
            copyBtn.textContent = '✔';
            setTimeout(() => { copyBtn.innerHTML = '📋'; }, 1000);
          }).catch(err => {
            console.error('Error al copiar al portapapeles:', err);
          });
        });

        // Crear botón
        const btn = document.createElement('button');
        btn.className = 'toggle-button';
        btn.textContent = '+';
        btn.title = 'Expandir/Colapsar código';
        container.appendChild(btn);

        // Crear overlay y ellipsis
        const overlay = document.createElement('div');
        overlay.className = 'fade-overlay';
        container.appendChild(overlay);
        
        const ell = document.createElement('div');
        ell.className = 'ellipsis';
        ell.textContent = '...';
        container.appendChild(ell);

        // Evento toggle
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          
          const isCollapsed = container.classList.contains('collapsed');
          
          if (isCollapsed) {
            // Expandir
            container.style.maxHeight = fullHeight + 20 + 'px';
            container.classList.remove('collapsed');
            container.classList.add('expanded');
            btn.textContent = '−';
          } else {
            // Colapsar
            container.style.maxHeight = collapsedHeight + 'px';
            container.classList.add('collapsed');
            container.classList.remove('expanded');
            btn.textContent = '+';
          }
        });
      });
    }, 100); // Esperar 100ms para que se apliquen los estilos
  }
  
  // Múltiples puntos de inicialización para mayor compatibilidad
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCollapsibles);
  } else {
    initCollapsibles();
  }
  
  // También inicializar en window.load por si acaso
  window.addEventListener('load', initCollapsibles);
})();"""


def transform_html(input_path, output_path, max_lines):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Asegurar que existe <html> y <head>
        if not soup.html:
            soup.wrap(soup.new_tag('html'))
        
        head = soup.head
        if not head:
            head = soup.new_tag('head')
            soup.html.insert(0, head)

        # Solo inyectar CSS y JS si no existen ya
        if not soup.find(id=CSS_ID):
            # Inyectar CSS
            style_tag = soup.new_tag('style', id=CSS_ID)
            style_tag.string = COLLAPSIBLE_CSS
            head.append(style_tag)
            
            # Inyectar JS
            script_tag = soup.new_tag('script')
            script_tag.string = COLLAPSIBLE_JS
            head.append(script_tag)

        # Procesar cada <pre>
        pre_elements = soup.find_all('pre')
        processed = 0
        
        for pre in pre_elements:
            # Omitir si ya está dentro de un contenedor colapsable
            if pre.find_parent('div', class_='collapsible-container'):
                continue
                
            # Omitir diagramas Mermaid
            if pre.find_parent('div', class_=['mermaid', 'language-mermaid']):
                continue
            
            # Contar líneas reales
            text_content = pre.get_text()
            lines = len([line for line in text_content.split('\n') if line.strip()])
            
            if lines <= max_lines:
                continue

            # Crear wrapper
            wrapper = soup.new_tag('div', **{
                'class': 'collapsible-container',
                'data-max-lines': str(max_lines)
            })
            
            # NO heredar clases del pre para evitar conflictos
            # Solo preservar atributos esenciales si es necesario
            if pre.has_attr('style'):
                # Aplicar algunos estilos del pre al wrapper si son relevantes
                wrapper['style'] = pre['style']
            
            # Envolver el pre
            pre.wrap(wrapper)
            processed += 1

        print(f"Procesados {processed} bloques <pre> con más de {max_lines} líneas")

        # Guardar resultado
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Convierte bloques <pre> muy largos en contenedores colapsables.")
    parser.add_argument('input', help='HTML de entrada')
    parser.add_argument('-o', '--output', help='Archivo HTML de salida (por defecto: <input>_collapsible.html)')
    parser.add_argument('-l', '--lines', type=int, default=DEFAULT_MAX_LINES,
                        help=f'Máximo de líneas antes de colapsar (por defecto: {DEFAULT_MAX_LINES})')
    
    args = parser.parse_args()
    
    # Validar archivo de entrada
    if not os.path.exists(args.input):
        print(f"Error: El archivo '{args.input}' no existe.")
        sys.exit(1)
    
    # Determinar archivo de salida
    if args.output:
        output_path = args.output
    else:
        name, ext = os.path.splitext(args.input)
        output_path = f"{name}_collapsible{ext or '.html'}"
    
    # Procesar archivo
    success = transform_html(args.input, output_path, args.lines)
    
    if success:
        print(f"✓ Se guardó correctamente el archivo: \"{output_path}\"")
    else:
        print("✗ Hubo errores durante el procesamiento")
        sys.exit(1)


if __name__ == '__main__':
    main()