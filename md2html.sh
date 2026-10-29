#!/bin/bash
# Convierte uno o más archivos Markdown en HTML autocontenido.
# Ejemplo: bash md2html.sh notes/Prog4/apunte.md [otro.md ...] [opciones]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

uso() {
  echo "Uso: $0 archivo.md [archivo2.md ...] [--skip-collapsible] [--skip-toc] [--skip-mermaid] [--keep-temp]"
  echo "  --skip-collapsible: Omitir el procesamiento de elementos colapsables"
  echo "  --skip-toc: Omitir la adición de tabla de contenidos"
  echo "  --skip-mermaid: Omitir pre-renderizado de diagramas Mermaid a SVG"
  echo "  --keep-temp: Conservar archivos intermedios en html_output/"
}

SKIP_COLLAPSIBLE=false
SKIP_TOC=false
SKIP_MERMAID=false
KEEP_TEMP=false
ARCHIVOS=()

# Opciones y archivos en cualquier orden
for arg in "$@"; do
  case $arg in
    --skip-collapsible) SKIP_COLLAPSIBLE=true ;;
    --skip-toc)         SKIP_TOC=true ;;
    --skip-mermaid)     SKIP_MERMAID=true ;;
    --keep-temp)        KEEP_TEMP=true ;;
    -h|--help)          uso; exit 0 ;;
    -*)                 echo "Opción desconocida: $arg"; uso; exit 1 ;;
    *)                  ARCHIVOS+=("$arg") ;;
  esac
done

if [ ${#ARCHIVOS[@]} -eq 0 ]; then
  uso
  exit 1
fi

# Directorio para los intermedios: html_output/ con --keep-temp, si no uno temporal
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

convertir() {
  local INPUT_MD="$1"
  local NOMBRE OUTPUT_DIR WORK_DIR BASE
  NOMBRE="$(basename "${INPUT_MD%.md}")"
  OUTPUT_DIR="$(dirname "$INPUT_MD")/html_output"
  mkdir -p "$OUTPUT_DIR"
  if [ "$KEEP_TEMP" = true ]; then WORK_DIR="$OUTPUT_DIR"; else WORK_DIR="$TMP_DIR"; fi
  BASE="$WORK_DIR/$NOMBRE"

  echo "[1/6] Ejecutando md2html.py..."
  python3 "$SCRIPT_DIR/md2html.py" "$INPUT_MD" -o "$BASE.html" -s "$SCRIPT_DIR/assets/sintax.css"

  if [ "$SKIP_MERMAID" = true ]; then
    echo "[2/6] Omitiendo pre-renderizado de Mermaid..."
  else
    echo "[2/6] Ejecutando add_graphs.py (Mermaid → SVG)..."
    python3 "$SCRIPT_DIR/add_graphs.py" "$BASE.html" -o "$BASE.html"
  fi

  if [ "$SKIP_COLLAPSIBLE" = true ]; then
    echo "[3/6] Omitiendo procesamiento de colapsables..."
    cp "$BASE.html" "${BASE}_collapsible.html"
  else
    echo "[3/6] Ejecutando collapsible.py..."
    python3 "$SCRIPT_DIR/collapsible.py" "$BASE.html" -o "${BASE}_collapsible.html"
  fi

  if [ "$SKIP_TOC" = true ]; then
    echo "[4/6] Omitiendo adición de tabla de contenidos..."
    cp "${BASE}_collapsible.html" "${BASE}_withcontent.html"
  else
    echo "[4/6] Ejecutando add_content_table.js..."
    node "$SCRIPT_DIR/add_content_table.js" "${BASE}_collapsible.html" -o "${BASE}_withcontent.html" --css "$SCRIPT_DIR/assets/toc.css"
  fi

  echo "[5/6] Ejecutando simplify_css.py..."
  python3 "$SCRIPT_DIR/simplify_css.py" "${BASE}_withcontent.html" --output "${BASE}_simplify.html"

  echo "[6/6] Ejecutando inline_css.py..."
  python3 "$SCRIPT_DIR/inline_css.py" "${BASE}_simplify.html" --output "$OUTPUT_DIR/${NOMBRE}_final.html"

  echo
  echo "Archivo final generado: $OUTPUT_DIR/${NOMBRE}_final.html"
  if [ "$KEEP_TEMP" = true ]; then
    echo "Archivos intermedios conservados en $OUTPUT_DIR/"
  fi
}

FALLIDOS=()
for md in "${ARCHIVOS[@]}"; do
  echo "=== $md"
  if [ ! -f "$md" ]; then
    echo "Error: no existe el archivo $md"
    FALLIDOS+=("$md")
    continue
  fi
  # En un subshell para que set -e corte solo la conversión de este archivo
  # (dentro de un if o un ! bash ignoraría set -e, por eso se toma el código aparte)
  set +e
  (set -e; convertir "$md")
  rc=$?
  set -e
  if [ $rc -ne 0 ]; then
    echo "Error al convertir $md"
    FALLIDOS+=("$md")
  fi
  echo
done

if [ ${#FALLIDOS[@]} -gt 0 ]; then
  echo "Fallaron ${#FALLIDOS[@]} de ${#ARCHIVOS[@]} archivos: ${FALLIDOS[*]}"
  exit 1
fi
