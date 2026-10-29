#!/bin/bash

# Verifica si se proporcionó un archivo .md
if [ $# -lt 1 ]; then
  echo "Uso: $0 archivo.md [--skip-collapsible] [--skip-toc] [--skip-mermaid] [--keep-temp]"
  echo "  --skip-collapsible: Omitir el procesamiento de elementos colapsables"
  echo "  --skip-toc: Omitir la adición de tabla de contenidos"
  echo "  --skip-mermaid: Omitir pre-renderizado de diagramas Mermaid a SVG"
  echo "  --keep-temp: Conservar archivos temporales"
  exit 1
fi

INPUT_MD="$1"
BASENAME="${INPUT_MD%.md}"
MD_DIR="$(dirname "$INPUT_MD")"
OUTPUT_DIR="$MD_DIR/html_output"
SKIP_COLLAPSIBLE=false
SKIP_TOC=false
SKIP_MERMAID=false
KEEP_TEMP=false

# Crear directorio de salida en el mismo directorio del archivo MD
mkdir -p "$OUTPUT_DIR"

# Verificar parámetros opcionales
for arg in "$@"; do
  case $arg in
    --skip-collapsible)
      SKIP_COLLAPSIBLE=true
      ;;
    --skip-toc)
      SKIP_TOC=true
      ;;
    --skip-mermaid)
      SKIP_MERMAID=true
      ;;
    --keep-temp)
      KEEP_TEMP=true
      ;;
  esac
done

# Paso 1: Convertir Markdown a HTML
echo "[1/6] Ejecutando md2html.py..."
python3 md2html.py "$INPUT_MD" -o "${OUTPUT_DIR}/$(basename "$BASENAME").html" -s "assets/sintax.css"
if [ $? -ne 0 ]; then echo "Error en md2html.py"; exit 1; fi

# Paso 2: Pre-renderizar Mermaid a SVG (OPCIONAL)
if [ "$SKIP_MERMAID" = true ]; then
  echo "[2/6] Omitiendo pre-renderizado de Mermaid..."
else
  echo "[2/6] Ejecutando add_graphs.py (Mermaid → SVG)..."
  python3 add_graphs.py "${OUTPUT_DIR}/$(basename "$BASENAME").html" -o "${OUTPUT_DIR}/$(basename "$BASENAME").html"
  if [ $? -ne 0 ]; then echo "Error en add_graphs.py"; exit 1; fi
fi

# Paso 3: Procesar colapsables (OPCIONAL)
if [ "$SKIP_COLLAPSIBLE" = true ]; then
  echo "[3/6] Omitiendo procesamiento de colapsables..."
  cp "${OUTPUT_DIR}/$(basename "$BASENAME").html" "${OUTPUT_DIR}/$(basename "$BASENAME")_collapsible.html"
else
  echo "[3/6] Ejecutando collapsible.py..."
  python3 collapsible.py "${OUTPUT_DIR}/$(basename "$BASENAME").html" -o "${OUTPUT_DIR}/$(basename "$BASENAME")_collapsible.html"
  if [ $? -ne 0 ]; then echo "Error en collapsible.py"; exit 1; fi
fi

# Paso 4: Agregar tabla de contenidos (OPCIONAL)
if [ "$SKIP_TOC" = true ]; then
  echo "[4/6] Omitiendo adición de tabla de contenidos..."
  cp "${OUTPUT_DIR}/$(basename "$BASENAME")_collapsible.html" "${OUTPUT_DIR}/$(basename "$BASENAME")_withcontent.html"
else
  echo "[4/6] Ejecutando add_content_table.js..."
  node add_content_table.js "${OUTPUT_DIR}/$(basename "$BASENAME")_collapsible.html" -o "${OUTPUT_DIR}/$(basename "$BASENAME")_withcontent.html" --css "assets/toc.css"
  if [ $? -ne 0 ]; then echo "Error en add_content_table.js"; exit 1; fi
fi

# Paso 5: Simplificar CSS
echo "[5/6] Ejecutando simplify_css.py..."
python3 simplify_css.py "${OUTPUT_DIR}/$(basename "$BASENAME")_withcontent.html" --output "${OUTPUT_DIR}/$(basename "$BASENAME")_simplify.html"
if [ $? -ne 0 ]; then echo "Error en simplify_css.py"; exit 1; fi

# Paso 6: Convertir a estilos inline
echo "[6/6] Ejecutando inline_css.py..."
python3 inline_css.py "${OUTPUT_DIR}/$(basename "$BASENAME")_simplify.html" --output "${OUTPUT_DIR}/$(basename "$BASENAME")_final.html"
if [ $? -ne 0 ]; then echo "Error en inline_css.py"; exit 1; fi

# Mostrar archivo final
echo
echo "Proceso completo. Archivo final generado: ${OUTPUT_DIR}/$(basename "$BASENAME")_final.html"

# Manejo de archivos temporales
if [ "$KEEP_TEMP" = true ]; then
  echo
  echo "Archivos intermedios conservados en ${OUTPUT_DIR}/."
else
  echo
  echo "Eliminando archivos temporales..."
  rm -f "${OUTPUT_DIR}/$(basename "$BASENAME").html" \
        "${OUTPUT_DIR}/$(basename "$BASENAME")_collapsible.html" \
        "${OUTPUT_DIR}/$(basename "$BASENAME")_withcontent.html" \
        "${OUTPUT_DIR}/$(basename "$BASENAME")_simplify.html"
  echo "Archivos eliminados."
fi
