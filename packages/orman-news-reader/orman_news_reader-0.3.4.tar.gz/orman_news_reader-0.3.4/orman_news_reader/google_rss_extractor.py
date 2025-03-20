#!/usr/bin/env python3
"""
Google RSS Feed Processor

Processes Google News RSS feeds, extracts content from articles,
saves images, and returns structured data for database storage.
"""

import requests
import feedparser
import os
import time
import uuid
import datetime
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
from orman_news_reader.reader_mode import extract_content
import sys


def follow_redirect(url):
    """Follows Google News redirects to get the actual article URL using Selenium.
    
    Args:
        url: Google News URL with redirect
        
    Returns:
        The final URL after following redirects
    """
    # Set up virtual display
    print("Starting virtual display...")
    display = Display(visible=0, size=(1600, 1200))
    display.start()
    
    # Set up Chrome options
    print("Setting up Chrome options...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    try:
        # Initialize the driver with explicit path
        print("Initializing ChromeDriver...")
        chromedriver_path = "/usr/bin/chromedriver"
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        # Navigate to the URL
        print(f"Navigating to URL: {url}")
        driver.get(url)
        
        # Wait for any JavaScript redirects to complete
        print("Waiting for redirects to complete...")
        time.sleep(5)  # Increased wait time
        
        # Get the current URL
        final_url = driver.current_url
        print(f"Final URL after redirects: {final_url}")
        
        # If we're still on a Google domain, try to find the actual article link
        if 'google.com' in final_url:
            print("Still on Google domain, looking for non-Google links...")
            links = driver.find_elements("tag name", "a")
            for link in links:
                href = link.get_attribute("href")
                if href and 'google.com' not in href and href.startswith('http'):
                    print(f"Found non-Google link: {href}")
                    final_url = href
                    break
        
        return final_url
    finally:
        # Always clean up resources
        if driver:
            print("Closing driver...")
            driver.quit()
        
        print("Stopping display...")
        display.stop()


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
                
    except requests.exceptions.HTTPError as e:
        print(f"Error extracting banner image: {e}")
    except Exception as e:
        print(f"Error extracting banner image: {e}")
    
    return None


def download_image(url, output_dir):
    """Downloads an image from a URL and saves it to the output directory.
    
    Args:
        url: URL of the image to download
        output_dir: Directory to save the image to
        
    Returns:
        Path to the saved image, or None if download failed
    """
    if not url:
        return None
        
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a unique filename
        file_ext = os.path.splitext(urlparse(url).path)[1]
        if not file_ext or file_ext.lower() not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            file_ext = '.jpg'  # Default to jpg if extension is missing or not recognized
            
        filename = f"{uuid.uuid4().hex}{file_ext}"
        filepath = os.path.join(output_dir, filename)
        
        # Download the image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return filename
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


def extract_source_from_url(url):
    """Extracts the source name from a URL.
    
    Args:
        url: URL to extract source from
        
    Returns:
        Source name extracted from the URL
    """
    try:
        domain = urlparse(url).netloc
        # Remove www. prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Extract the main domain name (e.g., nytimes.com -> nytimes)
        parts = domain.split('.')
        if len(parts) >= 2:
            return parts[-2].capitalize()
        return domain.capitalize()
    except:
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


def process_google_rss_feed(feed_url, output_dir='images', limit=None):
    """Processes a Google News RSS feed and extracts content from articles.
    
    Args:
        feed_url: URL of the Google News RSS feed
        output_dir: Directory to save images to
        limit: Maximum number of items to process
        
    Returns:
        List of dictionaries containing extracted data
    """
    results = []
    successful_count = 0
    
    try:
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)
        
        # Process entries until we reach the limit of successful items
        i = 0
        while (limit is None or successful_count < limit) and i < len(feed.entries):
            entry = feed.entries[i]
            i += 1
            
            try:
                print(f"Processing item {i}: {entry.title}")
                
                # Extract data from the feed entry
                item = {
                    'external_id': entry.get('id', None),
                    'title': entry.get('title', 'Untitled'),
                    'summary': entry.get('summary', None),
                    'source_url': entry.get('link', None),
                    'published_at': None,
                    'category': None
                }
                
                # Extract published date
                if 'published_parsed' in entry:
                    published_time = entry.published_parsed
                    item['published_at'] = datetime.datetime(
                        year=published_time.tm_year,
                        month=published_time.tm_mon,
                        day=published_time.tm_mday,
                        hour=published_time.tm_hour,
                        minute=published_time.tm_min,
                        second=published_time.tm_sec
                    )
                
                # Extract category if available
                if 'tags' in entry and entry.tags:
                    item['category'] = entry.tags[0].term
                
                # Follow redirect to get the actual article URL
                if item['source_url']:
                    actual_url = follow_redirect(item['source_url'])
                    print(f"  Redirected to: {actual_url}")
                    
                    # Skip if redirected back to Google News
                    if 'google.com' in actual_url:
                        print(f"  Skipping item (redirected to Google News)")
                        continue
                    
                    # Extract source from URL
                    item['source'] = extract_source_from_url(actual_url)
                    
                    # Extract banner image - don't let this fail the whole process
                    try:
                        banner_image_url = extract_banner_image(actual_url)
                        if banner_image_url:
                            # Download the image
                            image_filename = download_image(banner_image_url, output_dir)
                            item['image_url'] = image_filename
                    except Exception as e:
                        print(f"  Error extracting banner image: {e}")
                    
                    # Extract content
                    try:
                        content_data = extract_content(actual_url, output_dir, preserve_structure=True)
                        
                        # Convert content elements to HTML
                        html_content = ""
                        if 'content_elements' in content_data:
                            for element in content_data.get('content_elements', []):
                                if element['type'] in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                                    html_content += f"<{element['type']}>{element['text']}</{element['type']}>"
                                elif element['type'] in ['image', 'figure'] and 'local_path' in element:
                                    img_filename = os.path.basename(element['local_path'])
                                    html_content += f"<figure><img src='{img_filename}' alt='{element.get('alt', '')}'></figure>"
                        else:
                            # Handle old format (separate text and images)
                            for paragraph in content_data.get('text', []):
                                html_content += f"<p>{paragraph}</p>"
                            
                            for img in content_data.get('images', []):
                                if 'local_path' in img:
                                    img_filename = os.path.basename(img['local_path'])
                                    html_content += f"<figure><img src='{img_filename}' alt='Image'></figure>"
                        
                        item['content'] = html_content
                        
                        # If no summary was found in the RSS feed, use the first paragraph
                        if not item['summary']:
                            if 'content_elements' in content_data:
                                for element in content_data.get('content_elements', []):
                                    if element['type'] == 'p' and element.get('text', ''):
                                        item['summary'] = element['text'][:255]
                                        break
                            elif 'text' in content_data and content_data['text']:
                                item['summary'] = content_data['text'][0][:255]
                        
                        # Add to results and increment successful count
                        results.append(item)
                        successful_count += 1
                        print(f"  Successfully processed item ({successful_count}/{limit if limit else 'unlimited'})")
                        
                    except Exception as e:
                        print(f"  Error extracting content: {e}")
                
            except Exception as e:
                print(f"  Error processing item: {e}")
    
    except Exception as e:
        print(f"Error processing feed: {e}")
    
    return results


def main():
    """Main function for the Google RSS feed processor."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Process Google News RSS feeds')
    parser.add_argument('feed_url', help='URL of the Google News RSS feed')
    parser.add_argument('--output-dir', '-o', default='images',
                        help='Directory to save images to (default: images)')
    parser.add_argument('--limit', '-l', type=int, default=None,
                        help='Maximum number of items to process')
    parser.add_argument('--json', '-j', action='store_true', 
                        help='Output in JSON format')
    args = parser.parse_args()
    
    try:
        results = process_google_rss_feed(args.feed_url, args.output_dir, args.limit)
        
        if not results:
            print("No results were successfully processed.")
            return
        
        if args.json:
            # Convert datetime objects to strings for JSON serialization
            for item in results:
                if item.get('published_at'):
                    item['published_at'] = item['published_at'].isoformat()
            print(json.dumps(results, indent=2))
        else:
            print("\n" + "="*80)
            print("FINAL DATABASE ENTRIES")
            print("="*80)
            
            for i, item in enumerate(results):
                print(f"\nITEM {i+1}:")
                print("-"*50)
                
                # Create a database-ready dictionary
                db_item = {
                    "external_id": item.get('external_id'),
                    "title": item.get('title'),
                    "summary": item.get('summary'),
                    "content": item.get('content'),
                    "source": item.get('source'),
                    "source_url": item.get('source_url'),
                    "image_url": item.get('image_url'),
                    "published_at": item.get('published_at'),
                    "category": item.get('category'),
                    "created_at": datetime.datetime.utcnow(),
                    "updated_at": datetime.datetime.utcnow()
                }
                
                # Print each field with proper formatting
                for key, value in db_item.items():
                    if key == 'content':
                        # Truncate content to avoid overwhelming output
                        content_preview = value[:200] + "..." if value and len(value) > 200 else value
                        print(f"  {key}: {content_preview}")
                    elif key in ['published_at', 'created_at', 'updated_at'] and value:
                        print(f"  {key}: {value.isoformat()}")
                    else:
                        print(f"  {key}: {value}")
                
                # Print image path if available
                if item.get('image_url'):
                    print(f"\n  Image saved to: {os.path.join(args.output_dir, item.get('image_url'))}")
                
                print("-"*50)
    except Exception as e:
        print(f"Error in main function: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 