# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

A Markdown-to-HTML pipeline for UTN course notes. Takes `.md` files (in `notes/<subject>/`) and produces self-contained HTML files with syntax highlighting, collapsible code blocks, table of contents, Mermaid diagrams, and inlined CSS — ready for sharing or offline viewing.

## Build Pipeline

The full pipeline is orchestrated by `md2html.sh`. Run from the repo root (it also works from elsewhere: scripts are resolved relative to `md2html.sh`):

```bash
bash md2html.sh notes/Prog4/some_file.md [other.md ...] [flags]
```

Flags (any order, mixed with files): `--skip-collapsible`, `--skip-toc`, `--skip-mermaid`, `--keep-temp`, `-h`

Output lands in `notes/<subject>/html_output/<basename>_final.html`. Intermediate files go to a `mktemp -d` directory that is removed on exit; with `--keep-temp` they are written to `html_output/` instead. Each file is converted independently; the script exits 1 if any file fails (and reports which ones).

### Pipeline Steps (in order)

1. **`md2html.py`** — Markdown → HTML with Pygments syntax highlighting and Mermaid support. A custom fence preprocessor handles fences inside lists and admonitions. Uses `assets/sintax.css` for code styling.
2. **`add_graphs.py`** — Pre-renders Mermaid blocks to inline SVG with `mmdc`. If `mmdc` is missing or a diagram fails, it warns and keeps Mermaid.js so diagrams render client-side. Skip with `--skip-mermaid`.
3. **`collapsible.py`** — Wraps long code blocks (>6 lines) in collapsible containers (BeautifulSoup).
4. **`add_content_table.js`** — Generates a table of contents from heading tags and inserts it after the title block. Uses `assets/toc.css`. Plain Node.js (no npm dependencies).
5. **`simplify_css.py`** — Merges all `<style>` blocks into one, dropping overridden declarations while preserving cascade order, `!important`, and at-rules (`@media`, `@keyframes`) verbatim.
6. **`inline_css.py`** — Prepares the HTML for Moodle: head CSS goes into a hidden `<textarea>` reinjected by JS, head scripts are wrapped in `DOMContentLoaded`, SVG `viewBox` is saved in `data-viewbox`, and Mermaid source in `data-mermaid-src` (base64), each restored by JS.

## Dependencies

- **Python 3**: `pip install -r requirements.txt` (`markdown`, `pygments`, `beautifulsoup4`)
- **Node.js**: only to run `add_content_table.js`; no npm packages needed
- **Optional**: `npm install -g @mermaid-js/mermaid-cli` (`mmdc`) to pre-render Mermaid diagrams

## Project Structure

- `notes/` — Source markdown files organized by subject (`Prog3/`, `Prog4/`, `BDI/`, `ECA/`, etc.), each with its own `html_output/` for generated files
- `assets/` — Shared CSS (`sintax.css`, `toc.css`)
- `~notes/` — Auxiliary/scratch notes directory

## Key Conventions

- All scripts are run from the repo root directory
- The pipeline produces a single `_final.html` file per markdown source
- Comments and variable names in the codebase are in Spanish
- Each processing step reads the previous step's output file and writes a new one with a suffix (`_collapsible`, `_withcontent`, `_simplify`, `_final`)
- Moodle strips `viewBox`/`width`/`height` from `<svg>` and alters text whitespace, but keeps `style` and `data-*` attributes — that is why the pipeline stores data in `data-*` and restores it with JS
