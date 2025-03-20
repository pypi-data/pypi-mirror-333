#!/usr/bin/env python3
"""
Reader Mode Script

Extracts the main content (text and images) from a webpage,
similar to iPhone's browser reader mode.
"""

import os
import sys
import requests
import argparse
from bs4 import BeautifulSoup
from readability import Document
from urllib.parse import urljoin, urlparse
import json


def download_image(img_url, output_dir):
    """Downloads an image from the given URL to the output directory.
    
    Args:
        img_url: URL of the image to download
        output_dir: Directory to save the image to
        
    Returns:
        Path to the saved image or None if download failed
    """
    try:
        # Create a valid filename from the URL
        img_filename = os.path.basename(urlparse(img_url).path)
        
        # Handle cases where the filename is missing or invalid
        if not img_filename or '.' not in img_filename:
            img_filename = f"image_{abs(hash(img_url))}.jpg"
        else:
            # Add a hash to the filename to avoid conflicts
            name, ext = os.path.splitext(img_filename)
            img_filename = f"{name}_{str(abs(hash(img_url)))[:8]}{ext}"
        
        img_path = os.path.join(output_dir, img_filename)
        
        # Download the image
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        
        with open(img_path, 'wb') as img_file:
            for chunk in response.iter_content(chunk_size=8192):
                img_file.write(chunk)
                
        return img_path
    except Exception as e:
        print(f"Error downloading image {img_url}: {e}")
        return None


def extract_content(url, output_dir=None, preserve_structure=False):
    """Extracts main content (text and images) from a webpage.
    
    Args:
        url: URL of the webpage to extract content from
        output_dir: Directory to save images to (optional)
        preserve_structure: Whether to preserve the original structure with images in context
        
    Returns:
        Dictionary containing the extracted title, text, and image paths
    """
    # Fetch the webpage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        # Return a minimal result instead of exiting
        return {
            'title': 'Error fetching content',
            'text': [f'Error fetching content: {e}'],
            'images': [],
            'content_elements': [] if preserve_structure else None
        }
    
    # Use readability to extract the main content
    doc = Document(response.text)
    title = doc.title()
    content = doc.summary()
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Dictionary to track downloaded images to avoid duplicates
    downloaded_images = {}
    
    if preserve_structure:
        # Create output directory if needed
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Process images in place
        content_elements = []
        images = []
        
        # Keep track of processed image elements to avoid duplicates
        processed_elements = set()
        # Track image URLs to avoid duplicates with the same source
        processed_urls = set()
        
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'figure']):
            # Skip elements we've already processed (to avoid duplicates)
            if element in processed_elements:
                continue
                
            if element.name == 'img':
                processed_elements.add(element)
                src = element.get('src')
                if src and output_dir:
                    try:
                        # Convert relative URLs to absolute URLs
                        img_url = urljoin(url, src)
                        
                        # Skip if we've already processed this URL
                        if img_url in processed_urls:
                            continue
                        
                        processed_urls.add(img_url)
                        
                        # Check if we've already downloaded this image
                        if img_url in downloaded_images:
                            img_path = downloaded_images[img_url]
                        else:
                            img_path = download_image(img_url, output_dir)
                            if img_path:
                                downloaded_images[img_url] = img_path
                        
                        if img_path:
                            img_info = {
                                'original_url': img_url,
                                'local_path': img_path,
                                'alt': element.get('alt', ''),
                                'type': 'image'
                            }
                            images.append(img_info)
                            content_elements.append(img_info)
                    except Exception as e:
                        print(f"Error processing image: {e}")
                        # Continue without this image
            elif element.name == 'figure':
                processed_elements.add(element)
                # Handle figure elements with captions
                img = element.find('img')
                if img:
                    processed_elements.add(img)  # Mark the img inside figure as processed
                figcaption = element.find('figcaption')
                
                if img and img.get('src') and output_dir:
                    try:
                        img_url = urljoin(url, img.get('src'))
                        
                        # Skip if we've already processed this URL
                        if img_url in processed_urls:
                            continue
                        
                        processed_urls.add(img_url)
                        
                        # Check if we've already downloaded this image
                        if img_url in downloaded_images:
                            img_path = downloaded_images[img_url]
                        else:
                            img_path = download_image(img_url, output_dir)
                            if img_path:
                                downloaded_images[img_url] = img_path
                        
                        if img_path:
                            caption = figcaption.text.strip() if figcaption else ''
                            img_info = {
                                'original_url': img_url,
                                'local_path': img_path,
                                'alt': img.get('alt', ''),
                                'caption': caption,
                                'type': 'figure'
                            }
                            images.append(img_info)
                            content_elements.append(img_info)
                    except Exception as e:
                        print(f"Error processing figure: {e}")
                        # Continue without this figure
            elif element.text.strip():
                processed_elements.add(element)
                # Handle text elements
                content_elements.append({
                    'type': element.name,
                    'text': element.text.strip()
                })
        
        return {
            'title': title,
            'content_elements': content_elements,
            'images': images
        }
    else:
        # Original behavior: separate text and images
        paragraphs = []
        for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if p.text.strip():
                paragraphs.append(p.text.strip())
        
        # Extract images
        images = []
        if output_dir:
            try:
                os.makedirs(output_dir, exist_ok=True)
                
                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        try:
                            # Convert relative URLs to absolute URLs
                            img_url = urljoin(url, src)
                            
                            # Check if we've already downloaded this image
                            if img_url in downloaded_images:
                                img_path = downloaded_images[img_url]
                            else:
                                img_path = download_image(img_url, output_dir)
                                if img_path:
                                    downloaded_images[img_url] = img_path
                            
                            if img_path:
                                images.append({
                                    'original_url': img_url,
                                    'local_path': img_path
                                })
                        except Exception as e:
                            print(f"Error processing image: {e}")
                            # Continue without this image
            except Exception as e:
                print(f"Error creating output directory: {e}")
        
        return {
            'title': title,
            'text': paragraphs,
            'images': images
        }


def main():
    """Main function to parse arguments and run the content extraction."""
    parser = argparse.ArgumentParser(description='Extract readable content from a webpage')
    parser.add_argument('url', help='URL of the webpage to extract content from')
    parser.add_argument('--output-dir', '-o', help='Directory to save images to')
    parser.add_argument('--json', '-j', action='store_true', help='Output in JSON format')
    parser.add_argument('--preserve-structure', '-p', action='store_true', 
                        help='Preserve the original structure with images in context')
    args = parser.parse_args()
    
    content = extract_content(args.url, args.output_dir, args.preserve_structure)
    
    if args.json:
        print(json.dumps(content, indent=2))
    else:
        print(f"Title: {content['title']}\n")
        
        if args.preserve_structure:
            print("Content:")
            for element in content['content_elements']:
                if element['type'] in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    print(f"{element['text']}\n")
                elif element['type'] in ['image', 'figure']:
                    print(f"[Image: {element['local_path']}]\n")
        else:
            print("Text:")
            for p in content['text']:
                print(f"{p}\n")
            
            if content['images']:
                print("Images:")
                for img in content['images']:
                    print(f"- {img['local_path']} (from {img['original_url']})")


if __name__ == "__main__":
    main() 