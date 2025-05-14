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

Examples:
  node add_content_table.js document.html
  node add_content_table.js -d 3 document.html
  node add_content_table.js --depth 4 --output result.html document.html
  
Note:
  The script will automatically add IDs to headings that don't have them.
  The table of contents will be inserted after the first h1 tag or at the beginning of the body.
`);
}

/**
 * Adds a table of contents to an HTML file using regex (no dependencies)
 * @param {string} filePath - Path to the HTML file
 * @param {number} maxDepth - Maximum heading level to include (2=h2, 3=h3, etc.)
 * @param {string} outputPath - Path for the output file (optional)
 */
function addTableOfContents(filePath, maxDepth = 6, outputPath = null) {
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
    
    // Create TOC HTML
    let tocHtml = '<div id="table-of-contents" class="toc">\n' +
                 '  <h2 id="contents-header">Tabla de contenidos</h2>\n' +
                 '  <ul class="toc">\n';
    
    for (const heading of headings) {
      tocHtml += `    <li class="toc"><a class="toc" href="#${heading.id}">${heading.text}</a></li>\n`;
    }
    
    tocHtml += '  </ul>\n</div>\n\n';
    
    // Find insertion point (after first h1 or at beginning of body)
    let insertPosition = 0;
    
    // Look for the first h1
    const h1Match = /<h1\b[^>]*>.*?<\/h1>/i.exec(modifiedHtml);
    if (h1Match) {
      insertPosition = h1Match.index + h1Match[0].length;
    } else {
      // Try to find the body tag opening
      const bodyMatch = /<body\b[^>]*>/i.exec(modifiedHtml);
      if (bodyMatch) {
        insertPosition = bodyMatch.index + bodyMatch[0].length;
      }
    }
    
    // Insert TOC at the determined position
    modifiedHtml = modifiedHtml.slice(0, insertPosition) +
                  '\n\n' + tocHtml +
                  modifiedHtml.slice(insertPosition);
    
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
  let maxDepth = 6;
  let outputPath = null;

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

  addTableOfContents(filePath, maxDepth, outputPath);
}

module.exports = { addTableOfContents };