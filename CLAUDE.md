# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

A Markdown-to-HTML pipeline for UTN course notes. Takes `.md` files (in `notes/<subject>/`) and produces self-contained HTML files with syntax highlighting, collapsible code blocks, table of contents, Mermaid diagrams, and inlined CSS — ready for sharing or offline viewing.

## Build Pipeline

The full pipeline is orchestrated by `md2html.sh`. Run from the repo root:

```bash
bash md2html.sh notes/Prog4/some_file.md
```

Flags: `--skip-collapsible`, `--skip-toc`, `--keep-temp`

Output lands in `notes/<subject>/html_output/<basename>_final.html`. Intermediate files are deleted by default unless `--keep-temp` is passed.

### Pipeline Steps (in order)

1. **`md2html.py`** — Markdown → HTML with Pygments syntax highlighting, Mermaid diagram support, and SVG rendering. Uses `assets/sintax.css` for code styling.
2. **`collapsible.py`** — Wraps long code blocks (>6 lines) in collapsible containers (BeautifulSoup).
3. **`add_content_table.js`** — Generates a table of contents from heading tags. Uses `assets/toc.css`. Node.js script (jsdom).
4. **`simplify_css.py`** — Merges all `<style>` blocks into one, deduplicates and simplifies CSS rules.
5. **`inline_css.py`** — Converts all CSS to inline styles so the final HTML is fully self-contained.

### Additional Tool

- **`add_graphs.py`** — Converts Mermaid code blocks in HTML to inline SVGs (pre-renders diagrams).

## Dependencies

- **Python 3**: `markdown`, `pygments`, `beautifulsoup4` (bs4)
- **Node.js**: `jsdom` (installed via `npm install`)

## Project Structure

- `notes/` — Source markdown files organized by subject (`Prog3/`, `Prog4/`, `BDI/`, `ECA/`, etc.), each with its own `html_output/` for generated files
- `assets/` — Shared CSS (`sintax.css`, `toc.css`)
- `~notes/` — Auxiliary/scratch notes directory

## Key Conventions

- All scripts are run from the repo root directory
- The pipeline produces a single `_final.html` file per markdown source
- Comments and variable names in the codebase are in Spanish
- Each processing step reads the previous step's output file and writes a new one with a suffix (`_collapsible`, `_withcontent`, `_simplify`, `_final`)
