#!/bin/bash

# md2html_process.sh - Process a markdown file through md2html, add_content_table, and inline_css
# Usage: ./md2html_process.sh input.md [highlight_style] [max_heading_depth] [css_file]

# Display help if no arguments provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <markdown_file> [highlight_style] [max_heading_depth] [css_file]"
    echo ""
    echo "Arguments:"
    echo "  markdown_file      Path to the markdown file to process"
    echo "  highlight_style    Optional: Pygments style for syntax highlighting (default: monokai)"
    echo "  max_heading_depth  Optional: Maximum heading level for table of contents (2-6, default: 6)"
    echo "  css_file           Optional: Path to custom CSS file (if not provided, no custom CSS will be used)"
    echo ""
    echo "Example:"
    echo "  $0 document.md dracula 3 custom.css"
    echo "  $0 /path/to/document.md monokai 6 /path/to/custom.css"
    exit 1
fi

# Path to the markdown file
MARKDOWN_FILE="$1"
HIGHLIGHT_STYLE="${2:-dracula}"
MAX_HEADING_DEPTH="${3:-2}"
CSS_FILE="${4:-style.css}"

# Ensure the input file exists
if [ ! -f "$MARKDOWN_FILE" ]; then
    echo "Error: File not found: $MARKDOWN_FILE"
    exit 1
fi

# Extract the directory and filename components
FILE_DIR=$(dirname "$MARKDOWN_FILE")
FILE_NAME=$(basename "$MARKDOWN_FILE")
BASE_NAME="${FILE_NAME%.*}"  # Remove extension

# Initialize CSS argument for md2html.py
CSS_ARG=""

# Check if a CSS file was specified
if [ -n "$CSS_FILE" ]; then
    # Check if specified CSS file exists
    if [ ! -f "$CSS_FILE" ]; then
        echo "Warning: CSS file not found: $CSS_FILE"
        echo "Continuing without custom CSS styling..."
    else
        CSS_ARG="-s $CSS_FILE"
        echo "Using CSS file: $CSS_FILE"
    fi
fi

echo "Processing $MARKDOWN_FILE..."

# Define output file paths with correct directory
HTML_FILE="$FILE_DIR/$BASE_NAME.html"
TOC_HTML_FILE="$FILE_DIR/${BASE_NAME}_toc.html"
FINAL_HTML_FILE="$FILE_DIR/${BASE_NAME}_final.html"

# Step 1: Convert markdown to HTML using md2html.py
echo "Step 1: Converting markdown to HTML with style $HIGHLIGHT_STYLE..."
python3 md2html.py "$MARKDOWN_FILE" $CSS_ARG -hl "$HIGHLIGHT_STYLE" -o "$HTML_FILE"

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: Failed to convert markdown to HTML"
    exit 1
fi

# Step 2: Add table of contents using add_content_table.js
echo "Step 2: Adding table of contents with depth $MAX_HEADING_DEPTH..."
node add_content_table.js -d "$MAX_HEADING_DEPTH" -o "$TOC_HTML_FILE" "$HTML_FILE"

if [ ! -f "$TOC_HTML_FILE" ]; then
    echo "Error: Failed to add table of contents"
    exit 1
fi

# Step 3: Inline CSS using inline_css.py
echo "Step 3: Inlining CSS styles..."
python3 inline_css.py -o "$FINAL_HTML_FILE" "$TOC_HTML_FILE"

if [ ! -f "$FINAL_HTML_FILE" ]; then
    echo "Error: Failed to inline CSS"
    exit 1
else
    echo "Success! Final file created: $FINAL_HTML_FILE"
fi

# Optionally: clean up intermediate files
echo -n "Remove intermediate files? (y/n): "
read -r ANSWER
if [ "$ANSWER" = "y" ] || [ "$ANSWER" = "Y" ]; then
    echo "Removing intermediate files..."
    rm -f "$HTML_FILE"
    rm -f "$TOC_HTML_FILE"
    echo "Done!"
fi

echo "Process completed! Final HTML file: $FINAL_HTML_FILE"
