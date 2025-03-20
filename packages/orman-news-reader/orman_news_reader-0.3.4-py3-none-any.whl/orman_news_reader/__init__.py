"""
Orman News Reader

A Python package that extracts the main content from webpages and generates clean, reader-friendly HTML.
"""

from orman_news_reader.reader_mode import extract_content, download_image
from orman_news_reader.html_generator import generate_html
from orman_news_reader.google_rss_extractor import extract_google_news_content, follow_redirect, extract_banner_image

__version__ = "0.2.2"
