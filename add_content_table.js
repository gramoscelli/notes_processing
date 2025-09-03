// No-dependency Table of Contents Generator
// Uses only Node.js built-in modules with regex-based parsing

const fs = require('fs');
const path = require('path');

/**
 * Displays help information about how to use the script
 */
function showHelp() {
  console.log(`
Table of Contents Generator
---------------------------
This script adds a table of contents to an HTML file by scanning for heading tags.

Usage:
  node add_content_table.js [options] <html-file>

Options:
  -h, --help     Show this help message
  -d, --depth N  Maximum heading level to include (2-6, default: 6)
                 Example: -d 3 will include h2 and h3 only
  -o, --output   Specify output filename (default: <input>_withcontent.html)
  -c, --css      Specify CSS file to style the table of contents
                 Example: -c styles.css

Examples:
  node add_content_table.js document.html
  node add_content_table.js -d 3 document.html
  node add_content_table.js --depth 4 --output result.html document.html
  node add_content_table.js --css toc-styles.css document.html
  
Note:
  The script will automatically add IDs to headings that don't have them.
  The table of contents will be inserted after the first h1 tag or at the beginning of the body.
  Headings will be indented in the table of contents according to their level.
  CSS styles from the specified file will be embedded in the HTML document.
`);
}

/**
 * Adds a table of contents to an HTML file using regex (no dependencies)
 * @param {string} filePath - Path to the HTML file
 * @param {number} maxDepth - Maximum heading level to include (2=h2, 3=h3, etc.)
 * @param {string} outputPath - Path for the output file (optional)
 * @param {string} cssPath - Path to CSS file for styling (optional)
 */
function addTableOfContents(filePath, maxDepth = 2, outputPath = null, cssPath = null) {
  console.time('toc');
  try {
    // Check if file exists
    if (!fs.existsSync(filePath)) {
      console.error(`File not found: ${filePath}`);
      return;
    }

    // Read file content
    const htmlContent = fs.readFileSync(filePath, 'utf8');

    // Create regex pattern for finding heading tags
    const headingPattern = new RegExp(`<h([2-${Math.min(maxDepth, 6)}])\\b([^>]*)>(.*?)</h\\1>`, 'gi');

    // Find all matching headings
    const headings = [];
    let match;

    while ((match = headingPattern.exec(htmlContent)) !== null) {
      const level = parseInt(match[1]);
      const attributes = match[2];
      const content = match[3];
      const fullTag = match[0];

      // Extract id attribute if it exists
      let id = '';
      const idMatch = attributes.match(/id=["']([^"']*)["']/i);
      if (idMatch) {
        id = idMatch[1];
      }

      // Extract text content (remove any HTML tags)
      const text = content.replace(/<[^>]*>/g, '');

      headings.push({
        level,
        id,
        text,
        fullTag,
        start: match.index,
        end: match.index + fullTag.length
      });
    }

    if (headings.length === 0) {
      console.log('No headings found in the document to create a table of contents');
      // Determinar el nombre del archivo de salida
      let outputFilePath;
      if (outputPath) {
        outputFilePath = outputPath;
      } else {
        const dirname = path.dirname(filePath);
        const basename = path.basename(filePath, '.html');
        outputFilePath = path.join(dirname, `${basename}_withcontent.html`);
      }

      // Escribir el archivo de salida (mismo contenido que el de entrada)
      fs.writeFileSync(outputFilePath, htmlContent);
      console.log(`No headings found. Original content written to: ${outputFilePath}`);

      return;
    }

    // Assign ids to headings that don't have them
    let modifiedHtml = htmlContent;
    let offset = 0;

    for (let i = 0; i < headings.length; i++) {
      const heading = headings[i];

      if (!heading.id) {
        heading.id = `heading-${i}`;

        // Create new tag with ID
        const oldTag = heading.fullTag;
        const tagStart = `<h${heading.level}`;
        const newTag = `${tagStart} id="${heading.id}"${heading.fullTag.substring(tagStart.length)}`;

        // Replace tag in HTML
        const startPos = heading.start + offset;
        modifiedHtml = modifiedHtml.substring(0, startPos) +
          newTag +
          modifiedHtml.substring(startPos + oldTag.length);

        // Adjust offset for next replacements
        offset += (newTag.length - oldTag.length);
      }
    }

    // Create hierarchical TOC HTML
    let tocHtml = '<div id="table-of-contents" class="toc">\n' +
      '  <h2 id="contents-header">Tabla de contenidos</h2>\n';

    // Function to create nested TOC structure
    function createTocStructure(headings, minLevel, indentLevel = 0) {
      if (headings.length === 0) return '';

      // Create indentation based on the depth
      const indent = '  '.repeat(indentLevel);
      const itemIndent = '  '.repeat(indentLevel + 1);

      let result = `${indent}<ul class="toc">\n`;
      let i = 0;

      while (i < headings.length) {
        const currentHeading = headings[i];
        const currentLevel = currentHeading.level;

        if (currentLevel < minLevel) {
          // We've moved back up the hierarchy
          break;
        }

        if (currentLevel === minLevel) {
          // Same level heading - add to current list
          result += `${itemIndent}<li class="toc"><a class="toc" href="#${currentHeading.id}">${currentHeading.text}</a>`;

          // Get subheadings
          const subHeadings = [];
          let j = i + 1;
          while (j < headings.length && headings[j].level > currentLevel) {
            subHeadings.push(headings[j]);
            j++;
          }

          // If we have subheadings, nest them
          if (subHeadings.length > 0) {
            result += '\n' + createTocStructure(subHeadings, minLevel + 1, indentLevel + 1);
            result += `${itemIndent}`;
          }

          result += '</li>\n';
          i = j; // Skip the subheadings we've processed
        } else {
          // We should never reach here, but just in case
          i++;
        }
      }

      result += `${indent}</ul>\n`;
      return result;
    }

    // Find the minimum heading level (usually 2)
    const minLevel = headings.length === 0 ?
      2 : // Valor predeterminado si no hay encabezados
      headings.reduce((min, h) => Math.min(min, h.level), Number.MAX_SAFE_INTEGER);
    tocHtml += createTocStructure(headings, minLevel);
    tocHtml += '</div>\n\n';

    // Handle CSS styling
    let cssContent = '';
    if (cssPath) {
      if (!fs.existsSync(cssPath)) {
        console.warn(`CSS file not found: ${cssPath}. Continuing without CSS styling.`);
      } else {
        // Read CSS file and prepare to inline it
        cssContent = fs.readFileSync(cssPath, 'utf8');
        cssContent = `<style type="text/css">\n${cssContent}\n</style>\n`;
      }
    }

    // Find insertion points for TOC and CSS
    let tocInsertPosition = 0;
    let cssInsertPosition = 0;

    // Look for the first h1 for TOC insertion
    const h1Match = /<h1\b[^>]*>.*?<\/h1>/i.exec(modifiedHtml);
    if (h1Match) {
      tocInsertPosition = h1Match.index + h1Match[0].length;
    } else {
      // Try to find the body tag opening
      const bodyMatch = /<body\b[^>]*>/i.exec(modifiedHtml);
      if (bodyMatch) {
        tocInsertPosition = bodyMatch.index + bodyMatch[0].length;
      }
    }

    // Find head tag for CSS insertion
    if (cssContent) {
      const headEndMatch = /<\/head>/i.exec(modifiedHtml);
      if (headEndMatch) {
        cssInsertPosition = headEndMatch.index;
      } else {
        // If no head tag, try to find html opening and create a head tag
        const htmlMatch = /<html\b[^>]*>/i.exec(modifiedHtml);
        if (htmlMatch) {
          cssInsertPosition = htmlMatch.index + htmlMatch[0].length;
          // Insert a head tag if none exists
          modifiedHtml = modifiedHtml.slice(0, cssInsertPosition) +
            '\n<head>\n</head>\n' +
            modifiedHtml.slice(cssInsertPosition);
          cssInsertPosition += 8; // Position right after <head>
        } else {
          // Just insert at the beginning of the file and hope for the best
          cssInsertPosition = 0;
          modifiedHtml = '<head>\n</head>\n' + modifiedHtml;
          cssInsertPosition = 7; // Position right after <head>
        }
      }
    }

    // Insert CSS at the determined position
    if (cssContent) {
      modifiedHtml = modifiedHtml.slice(0, cssInsertPosition) +
        cssContent +
        modifiedHtml.slice(cssInsertPosition);

      // Adjust tocInsertPosition if it's after cssInsertPosition
      if (tocInsertPosition > cssInsertPosition) {
        tocInsertPosition += cssContent.length;
      }
    }

    // Insert TOC at the determined position
    modifiedHtml = modifiedHtml.slice(0, tocInsertPosition) +
      '\n\n' + tocHtml +
      modifiedHtml.slice(tocInsertPosition);

    // Determine output filename
    let outputFilePath;
    if (outputPath) {
      outputFilePath = outputPath;
    } else {
      const dirname = path.dirname(filePath);
      const basename = path.basename(filePath, '.html');
      outputFilePath = path.join(dirname, `${basename}_withcontent.html`);
    }

    fs.writeFileSync(outputFilePath, modifiedHtml);
    console.log(`Table of contents added successfully. Output file: ${outputFilePath}`);
    if (cssPath && fs.existsSync(cssPath)) {
      console.log(`CSS styling embedded from: ${cssPath}`);
    }

  } catch (error) {
    console.error(`Error processing file: ${error.message}`);
    console.error(error.stack);
  }

  console.timeEnd('toc');
}

// CLI Execution
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
    showHelp();
    process.exit(args.length === 0 ? 1 : 0);
  }

  let filePath = null;
  let maxDepth = 2;
  let outputPath = null;
  let cssPath = null;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = i + 1 < args.length ? args[i + 1] : null;

    if (['-d', '--depth'].includes(arg) && nextArg) {
      const depthValue = parseInt(nextArg);
      if (!isNaN(depthValue) && depthValue >= 2 && depthValue <= 6) {
        maxDepth = depthValue;
        console.log(`Using maximum heading depth of h${maxDepth}`);
      } else {
        console.warn(`Invalid depth value: ${nextArg}. Using default (h6).`);
      }
      i++;
    } else if (['-o', '--output'].includes(arg) && nextArg) {
      outputPath = nextArg;
      console.log(`Output will be saved to: ${outputPath}`);
      i++;
    } else if (['-c', '--css'].includes(arg) && nextArg) {
      cssPath = nextArg;
      console.log(`Using CSS file: ${cssPath} (styles will be embedded in the HTML)`);
      i++;
    } else if (arg.startsWith('-')) {
      console.warn(`Unknown option: ${arg}`);
    } else if (!filePath) {
      filePath = arg;
    }
  }

  if (!filePath) {
    console.error('No HTML file path provided');
    showHelp();
    process.exit(1);
  }

  addTableOfContents(filePath, maxDepth, outputPath, cssPath);
}

module.exports = { addTableOfContents };