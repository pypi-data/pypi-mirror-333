#!/usr/bin/env python3
"""
Selenium-based redirect tracker for Google News URLs.

Uses Selenium to automate a browser for reliable tracking of redirects from Google News URLs.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def follow_redirects_with_selenium(url, timeout=10):
    """Uses Selenium to follow all redirects from a Google News URL.
    
    Args:
        url: The Google News URL to follow redirects from
        timeout: Maximum time to wait for page load in seconds
        
    Returns:
        The final URL after all redirects have been followed
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
        driver.set_page_load_timeout(timeout)
        
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
    
    except TimeoutException:
        print("Timeout waiting for page to load")
        return url
    except Exception as e:
        print(f"Error following redirects: {e}")
        return url
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    import sys
    
    # Use command line argument if provided
    url = sys.argv[1] if len(sys.argv) > 1 else "https://news.google.com/rss/articles/CBMiqgFBVV95cUxOTTJ2NTJ5UktQSVc5RVd2Ti1oYWR6emc2dVc3MmgxQWFOR3hvYnNtN29INUVmZjEzWVFobUFVcjJ1YWxoR0kzSDBIMGJtTWxnZWc1ZWNHTWNuc2lYYmRBOWc0dWh0eG5IYndCd1VyUVJvVm1FcHVwNFpLWGdmTE1HRERKY1VaQ0p6c0xvWC1yYk5rdlRQSTdFMElhUW5TUUZuUURZTEY0T3ZaUQ?oc=5"
    
    final_url = follow_redirects_with_selenium(url)
    
    print(f"Original URL: {url}")
    print(f"Final URL: {final_url}") 