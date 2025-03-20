#!/usr/bin/env python3
"""
Google RSS Extractor for Reader Mode

Handles Google News RSS feeds, extracts content from redirected articles,
and finds suitable images for carousel banners.
"""

import requests
from urllib.parse import urlparse, parse_qs
import re
from bs4 import BeautifulSoup
from web_reader_mode.reader_mode import extract_content
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def follow_redirect(url):
    """Follows Google News redirects to get the actual article URL using Selenium.
    
    Args:
        url: Google News URL with redirect
        
    Returns:
        The final URL after following redirects
    """
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    try:
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)
        
        # Navigate to the URL
        driver.get(url)
        
        # Wait for any JavaScript redirects to complete
        time.sleep(3)
        
        # Get the current URL (after all redirects)
        final_url = driver.current_url
        
        # If we're still on a Google domain, try to find the actual article link
        if 'google.com' in final_url:
            # Try to find links that might be the article
            links = driver.find_elements("tag name", "a")
            for link in links:
                href = link.get_attribute("href")
                if href and 'google.com' not in href and href.startswith('http'):
                    # If we find a non-Google link, that's likely our article
                    final_url = href
                    break
        
        return final_url
    
    except Exception as e:
        print(f"Error following redirect: {e}")
        return url
    finally:
        try:
            driver.quit()
        except:
            pass


def extract_banner_image(url):
    """Extracts a suitable image for a carousel banner from the article.
    
    Args:
        url: URL of the article
        
    Returns:
        URL of the best image for a banner, or None if no suitable image found
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # First try to find Open Graph image (usually high quality and meant for sharing)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # Then try Twitter card image
        twitter_image = soup.find('meta', property='twitter:image')
        if twitter_image and twitter_image.get('content'):
            return twitter_image['content']
        
        # Look for article header image or featured image
        # These are common patterns but may vary by site
        potential_images = []
        
        # Look for large images in the article
        for img in soup.find_all('img'):
            src = img.get('src')
            if not src:
                continue
                
            # Check for keywords in class or id that suggest it's a featured image
            parent = img.parent
            for _ in range(3):  # Check up to 3 levels up
                if parent is None:
                    break
                    
                classes = parent.get('class', [])
                if isinstance(classes, str):
                    classes = [classes]
                    
                id_attr = parent.get('id', '')
                
                keywords = ['featured', 'header', 'banner', 'hero', 'thumbnail', 'main']
                for keyword in keywords:
                    if (any(keyword in cls.lower() for cls in classes) or 
                        keyword in id_attr.lower()):
                        return src
                        
                parent = parent.parent
            
            # Check image size attributes for large images
            width = img.get('width')
            height = img.get('height')
            
            try:
                if width and height:
                    width = int(width)
                    height = int(height)
                    if width >= 600 and height >= 300:
                        potential_images.append((src, width * height))
            except ValueError:
                pass
        
        # Sort by image size (largest first)
        potential_images.sort(key=lambda x: x[1], reverse=True)
        
        # Return the largest image if available
        if potential_images:
            return potential_images[0][0]
            
        # If no suitable image found, return the first large image
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and (src.endswith('.jpg') or src.endswith('.jpeg') or 
                       src.endswith('.png') or src.endswith('.webp')):
                return src
                
    except Exception as e:
        print(f"Error extracting banner image: {e}")
    
    return None


def extract_google_news_content(url, output_dir=None, preserve_structure=True):
    """Extracts content from a Google News article, handling redirects.
    
    Args:
        url: Google News URL
        output_dir: Directory to save images to
        preserve_structure: Whether to preserve the original structure with images in context
        
    Returns:
        Dictionary containing the extracted content with an additional banner_image field
    """
    # Follow redirects to get the actual article URL
    actual_url = follow_redirect(url)
    print(f"Redirected to: {actual_url}")
    
    # Extract a suitable banner image
    banner_image_url = extract_banner_image(actual_url)
    
    # Extract the content using the existing function
    content = extract_content(actual_url, output_dir, preserve_structure)
    
    # Add the banner image URL to the content
    if banner_image_url:
        content['banner_image_url'] = banner_image_url
    
    return content


def main():
    """Main function for testing the Google RSS extractor."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Extract content from Google News RSS feeds')
    parser.add_argument('url', help='Google News URL to extract content from')
    parser.add_argument('--output-dir', '-o', default='images',
                        help='Directory to save images to (default: images)')
    parser.add_argument('--json', '-j', action='store_true', help='Output in JSON format')
    args = parser.parse_args()
    
    content = extract_google_news_content(args.url, args.output_dir)
    
    if args.json:
        print(json.dumps(content, indent=2))
    else:
        print(f"Title: {content['title']}\n")
        
        if 'banner_image_url' in content:
            print(f"Banner Image: {content['banner_image_url']}\n")
            
        print("Content:")
        for element in content['content_elements']:
            if element['type'] in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                print(f"{element['text']}\n")
            elif element['type'] in ['image', 'figure']:
                print(f"[Image: {element['local_path']}]\n")


if __name__ == "__main__":
    main() 