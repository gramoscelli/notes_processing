#!/usr/bin/env python3
"""
inline_css.py - Convert CSS in style tags to inline style attributes and remove class attributes

This script takes an HTML file and:
1. Converts all CSS rules from style tags and external stylesheets into inline style attributes
2. Removes all class attributes from HTML elements
3. Preserves pseudo-classes, pseudo-elements, and media queries

Usage:
    python inline_css.py input.html
    python inline_css.py input.html -o output.html
    python inline_css.py input.html --output output.html

Options:
    -o, --output       Specify the output file name (optional, default: input_inline.html)
"""

import os
import sys
import re
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import urllib.parse
import cssutils
import logging

# Suppress cssutils warning logs
cssutils.log.setLevel(logging.CRITICAL)

def parse_css_rules(css_content):
    """
    Parse CSS content and extract rules as a dictionary
    
    Args:
        css_content (str): CSS content as string
        
    Returns:
        dict: Dictionary of selectors and their style declarations
    """
    stylesheet = cssutils.parseString(css_content)
    rules = {}
    
    for rule in stylesheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            styles = {}
            for property in rule.style:
                if property.name and property.value:
                    if property.priority == "important":
                        styles[property.name] = property.value + " !important"
                    else:
                        styles[property.name] = property.value
            if selector in rules:
                # Merge styles if selector already exists
                rules[selector].update(styles)
            else:
                rules[selector] = styles
        elif rule.type == rule.MEDIA_RULE:
            # Handle media queries
            media_query = rule.media.mediaText
            for media_rule in rule:
                if media_rule.type == media_rule.STYLE_RULE:
                    # Create a specific media query style tag for these rules
                    selector = media_rule.selectorText
                    styles = {}
                    for property in media_rule.style:
                        if property.name and property.value:
                            if property.priority == "important":
                                styles[property.name] = property.value + " !important"
                            else:
                                styles[property.name] = property.value
                    
                    # Use a special key format for media queries
                    media_selector = f"@media {media_query} || {selector}"
                    rules[media_selector] = styles
    
    return rules

def apply_styles_to_elements(soup, rules):
    """
    Apply CSS rules to matching elements in the soup and preserve pseudo-elements
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the HTML
        rules (dict): Dictionary of CSS selectors and their styles
        
    Returns:
        BeautifulSoup: Modified soup with inline styles
    """
    # First, separate regular rules from pseudo-class/element rules
    regular_rules = {}
    pseudo_rules = {}
    
    for selector, styles in rules.items():
        if ':' in selector:
            # This is a pseudo-class or pseudo-element rule
            base_selector = selector.split(':', 1)[0].strip()
            if base_selector not in pseudo_rules:
                pseudo_rules[base_selector] = []
            pseudo_rules[base_selector].append((selector, styles))
        else:
            # This is a regular rule
            regular_rules[selector] = styles
    
    # Apply regular rules as inline styles
    for selector, styles in regular_rules.items():
        try:
            # Try to select elements using the selector
            elements = soup.select(selector)
            
            for element in elements:
                # Get existing inline style
                existing_style = element.get('style', '')
                existing_styles = {}
                
                # Parse existing inline styles
                if existing_style:
                    for item in existing_style.split(';'):
                        if ':' in item:
                            prop, val = item.split(':', 1)
                            existing_styles[prop.strip()] = val.strip()
                
                # Add new styles (don't override existing inline styles)
                for prop, val in styles.items():
                    if prop not in existing_styles:
                        existing_styles[prop] = val
                
                # Create the new style attribute
                new_style = '; '.join(f"{prop}: {val}" for prop, val in existing_styles.items())
                if new_style:
                    element['style'] = new_style
        except Exception as e:
            print(f"Warning: Failed to apply selector '{selector}': {str(e)}")
    
    # Create a style tag for pseudo-class and pseudo-element rules
    if pseudo_rules:
        pseudo_style = soup.new_tag('style')
        pseudo_css = []
        
        for base_selector, rules_list in pseudo_rules.items():
            for selector, styles in rules_list:
                css_rule = f"{selector} {{"
                for prop, val in styles.items():
                    css_rule += f" {prop}: {val};"
                css_rule += " }"
                pseudo_css.append(css_rule)
        
        # Set the content of the style tag
        pseudo_style.string = "\n".join(pseudo_css)
        
        # Find the head tag, or create one if it doesn't exist
        head = soup.find('head')
        if not head:
            head = soup.new_tag('head')
            if soup.html:
                soup.html.insert(0, head)
            else:
                soup.append(head)
        
        # Add the style tag to the head
        head.append(pseudo_style)
        print(f"Added {len(pseudo_css)} pseudo-class/element rules to a style tag")
    
    # Remove class attributes from all elements
    for element in soup.find_all(True):  # Find all elements
        if element.has_attr('class'):
            del element['class']
    
    return soup

def inline_css(html_file, output_file=None):
    """
    Convert all CSS to inline styles in an HTML file and remove class attributes
    
    Args:
        html_file (str): Path to the HTML file
        output_file (str, optional): Path for the output HTML file
    
    Returns:
        str: Path to the generated HTML file
    """
    # Check if input file exists
    html_path = Path(html_file)
    if not html_path.exists():
        print(f"Error: File not found: {html_file}")
        sys.exit(1)
    
    # Determine output file name if not specified
    if output_file:
        output_path = Path(output_file)
        print(f"Will create output file: {output_path}")
    else:
        # Add "_inline" to the filename before the extension
        output_path = html_path.with_name(html_path.stem + "_inline" + html_path.suffix)
        print(f"No output file specified, will create: {output_path}")
    
    # Read HTML content
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Collect all CSS rules
    all_css_content = []
    
    # Find all external CSS links
    css_links = soup.find_all('link', rel='stylesheet')
    
    # Process all CSS links
    for link in css_links:
        href = link.get('href')
        if not href:
            continue
        
        # Handle relative paths
        if href.startswith('http://') or href.startswith('https://'):
            css_url = href
        else:
            # If it's a relative path, resolve it relative to the HTML file
            base_dir = html_path.parent
            css_path = base_dir / href
            
            if css_path.exists():
                # Read local CSS file
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                    all_css_content.append(css_content)
                    print(f"Processing CSS from local file: {css_path}")
            else:
                # Try to convert relative URL to absolute URL
                base_url = f"file://{base_dir}/"
                css_url = urllib.parse.urljoin(base_url, href)
                
                if css_url.startswith('file://'):
                    print(f"Warning: Could not find local CSS file: {css_path}")
                    continue
                
                try:
                    # Fetch CSS content from URL
                    response = requests.get(css_url, timeout=5)
                    if response.status_code == 200:
                        css_content = response.text
                        all_css_content.append(css_content)
                        print(f"Processing CSS from URL: {css_url}")
                    else:
                        print(f"Warning: Failed to fetch CSS from {css_url}, status code: {response.status_code}")
                except Exception as e:
                    print(f"Warning: Error fetching CSS from {css_url}: {str(e)}")
        
        # Remove the link element after processing
        link.extract()
    
    # Find all style tags
    style_tags = soup.find_all('style')
    
    # Extract CSS from style tags
    for style in style_tags:
        if style.string:
            all_css_content.append(style.string)
            print("Processing CSS from style tag")
        
        # Remove the style element
        style.extract()
    
    # Parse all CSS content and get rules
    all_rules = {}
    media_rules = []
    
    for css_content in all_css_content:
        try:
            rules = parse_css_rules(css_content)
            
            # Separate media queries from regular rules
            for selector, styles in rules.items():
                if selector.startswith('@media'):
                    media_rules.append((selector, styles))
                else:
                    # Merge regular rules
                    if selector in all_rules:
                        all_rules[selector].update(styles)
                    else:
                        all_rules[selector] = styles
        except Exception as e:
            print(f"Warning: Error parsing CSS: {str(e)}")
    
    # Apply styles to elements
    soup = apply_styles_to_elements(soup, all_rules)
    
    # Process and add media queries
    if media_rules:
        media_style = soup.new_tag('style')
        media_css = []
        
        for selector, styles in media_rules:
            # Parse media query and actual selector
            if ' || ' in selector:  # Our special separator for media queries
                media_query, actual_selector = selector.split(' || ', 1)
                
                css_rule = f"{media_query} {{\n"
                css_rule += f"  {actual_selector} {{\n"
                
                for prop, val in styles.items():
                    css_rule += f"    {prop}: {val};\n"
                
                css_rule += "  }\n"
                css_rule += "}\n"
                
                media_css.append(css_rule)
        
        if media_css:
            media_style.string = "\n".join(media_css)
            
            # Find the head tag
            head = soup.find('head')
            if not head:
                head = soup.new_tag('head')
                if soup.html:
                    soup.html.insert(0, head)
                else:
                    soup.append(head)
            
            # Add the media queries style tag
            head.append(media_style)
            print(f"Added {len(media_css)} media query rules to a style tag")
    
    # Write the modified HTML to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Successfully created {output_path} with inlined CSS and removed class attributes")
    return str(output_path)

def main():
    parser = argparse.ArgumentParser(description='Convert CSS to inline style attributes and remove class attributes in HTML files.')
    parser.add_argument('input', help='Path to the input HTML file')
    parser.add_argument('-o', '--output', help='Path for the output HTML file (optional, default: input_inline.html)')
    
    args = parser.parse_args()
    
    if args.output:
        print(f"Processing {args.input} to create {args.output}")
    else:
        output_path = Path(args.input).with_name(Path(args.input).stem + "_inline" + Path(args.input).suffix)
        print(f"Processing {args.input} to create {output_path}")
    
    inline_css(args.input, args.output)

if __name__ == "__main__":
    main()