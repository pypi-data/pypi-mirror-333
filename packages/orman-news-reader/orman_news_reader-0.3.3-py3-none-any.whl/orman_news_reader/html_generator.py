#!/usr/bin/env python3
"""
HTML Generator for Reader Mode

Generates a clean, reader-friendly HTML page from extracted content.
"""

import os
import argparse
from orman_news_reader.reader_mode import extract_content
from orman_news_reader.google_rss_extractor import extract_google_news_content, follow_redirect


def generate_html(content, output_file, css_file=None):
    """Generates an HTML file from the extracted content.
    
    Args:
        content: Dictionary containing title, text, and images
        output_file: Path to save the HTML file
        css_file: Optional path to a custom CSS file
    """
    # Default CSS for a clean reader experience
    default_css = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
    }
    h1 {
        font-size: 2em;
        margin-bottom: 0.5em;
        color: #222;
    }
    h2 {
        font-size: 1.7em;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        color: #333;
    }
    h3 {
        font-size: 1.4em;
        margin-top: 1.2em;
        margin-bottom: 0.5em;
        color: #444;
    }
    h4, h5, h6 {
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #555;
    }
    p {
        margin-bottom: 1.2em;
        font-size: 1.1em;
    }
    img {
        max-width: 100%;
        height: auto;
        margin: 1.5em 0;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    figure {
        margin: 2em 0;
        text-align: center;
    }
    figcaption {
        font-size: 0.9em;
        color: #666;
        margin-top: 0.5em;
        font-style: italic;
    }
    .banner-image {
        width: 100%;
        height: 300px;
        object-fit: cover;
        margin: 0 0 2em 0;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    @media (prefers-color-scheme: dark) {
        body {
            background-color: #222;
            color: #eee;
        }
        h1 {
            color: #fff;
        }
        h2 {
            color: #eee;
        }
        h3 {
            color: #ddd;
        }
        h4, h5, h6 {
            color: #ccc;
        }
        figcaption {
            color: #aaa;
        }
        img {
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .banner-image {
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        }
    }
    """
    
    # Start building the HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['title']}</title>
    <style>
    {default_css}
    </style>
"""
    
    # Add custom CSS if provided
    if css_file and os.path.exists(css_file):
        with open(css_file, 'r') as f:
            custom_css = f.read()
        html += f"""    <style>
    {custom_css}
    </style>
"""
    
    html += """</head>
<body>
"""
    
    # Add banner image if available
    if 'banner_image_url' in content and content['banner_image_url']:
        html += f'    <img class="banner-image" src="{content["banner_image_url"]}" alt="Article banner image">\n'
    elif 'banner_image_path' in content and content['banner_image_path']:
        # Convert absolute paths to relative paths
        rel_path = os.path.relpath(content['banner_image_path'], os.path.dirname(output_file))
        html += f'    <img class="banner-image" src="{rel_path}" alt="Article banner image">\n'
    
    # Add title
    html += f"    <h1>{content['title']}</h1>\n"
    
    # Add content elements in their original order
    if 'content_elements' in content:
        for element in content['content_elements']:
            if element['type'] in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                html += f"    <{element['type']}>{element['text']}</{element['type']}>\n"
            elif element['type'] == 'image':
                # Convert absolute paths to relative paths
                rel_path = os.path.relpath(element['local_path'], os.path.dirname(output_file))
                html += f'    <img src="{rel_path}" alt="{element.get("alt", "Image from article")}">\n'
            elif element['type'] == 'figure':
                rel_path = os.path.relpath(element['local_path'], os.path.dirname(output_file))
                html += f'    <figure>\n'
                html += f'        <img src="{rel_path}" alt="{element.get("alt", "Image from article")}">\n'
                if element.get('caption'):
                    html += f'        <figcaption>{element["caption"]}</figcaption>\n'
                html += f'    </figure>\n'
    else:
        # Handle old format (separate text and images)
        for paragraph in content['text']:
            html += f"    <p>{paragraph}</p>\n"
        
        for img in content['images']:
            # Convert absolute paths to relative paths
            rel_path = os.path.relpath(img['local_path'], os.path.dirname(output_file))
            html += f'    <img src="{rel_path}" alt="Image from article">\n'
    
    # Close HTML
    html += """</body>
</html>"""
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_file


def main():
    """Main function to parse arguments and generate HTML."""
    parser = argparse.ArgumentParser(description='Generate a clean HTML page from a webpage')
    parser.add_argument('url', help='URL of the webpage to extract content from')
    parser.add_argument('--output-file', '-o', default='reader_output.html', 
                        help='Path to save the HTML file (default: reader_output.html)')
    parser.add_argument('--image-dir', '-i', default='images',
                        help='Directory to save images to (default: images)')
    parser.add_argument('--css-file', '-c', help='Path to a custom CSS file')
    parser.add_argument('--google-news', '-g', action='store_true',
                        help='Process as a Google News RSS article with redirect handling')
    args = parser.parse_args()
    
    if args.google_news:
        # Extract content with Google News redirect handling
        content = extract_google_news_content(args.url, args.image_dir, preserve_structure=True)
    else:
        # Extract content with images in context
        content = extract_content(args.url, args.image_dir, preserve_structure=True)
    
    # Generate HTML
    output_file = generate_html(content, args.output_file, args.css_file)
    
    print(f"Generated HTML file: {output_file}")
    print(f"Downloaded {len(content['images'])} images to {args.image_dir}/")
    
    if 'banner_image_url' in content:
        print(f"Banner image URL: {content['banner_image_url']}")


if __name__ == "__main__":
    main() 