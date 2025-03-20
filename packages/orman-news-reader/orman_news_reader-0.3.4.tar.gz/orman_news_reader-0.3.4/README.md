# Web Reader Mode

A Python package that extracts the main content (text and images) from a webpage, similar to iPhone's browser reader mode.

## Features

- Extracts the main article content from a webpage
- Removes ads, navigation, and other distractions
- Downloads and saves images locally
- Outputs content in plain text or JSON format
- Generates clean, reader-friendly HTML pages

## Installation

### Using Poetry (Recommended)

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install with Poetry:
   ```
   poetry install
   ```

3. Alternatively, install from PyPI:
   ```
   pip install orman-news-reader
   ```

## Usage

### Using Poetry

```
poetry run orman-web-reader [command] [options]
```

Available commands:
- `reader`: Extract content from a webpage
- `html`: Generate a clean HTML page from a webpage
- `google`: Extract content from Google News RSS articles

### Reader Mode

Extract content from a webpage:
```
poetry run orman-web-reader reader https://example.com/article
```

Save images to a specific directory:
```
poetry run orman-web-reader reader https://example.com/article --output-dir images
```

Output in JSON format:
```
poetry run orman-web-reader reader https://example.com/article --json
```

Full options:
```
poetry run orman-web-reader reader --help
```

### Google News RSS Extractor

Extract content from Google News RSS articles with redirect handling:
```
poetry run orman-web-reader google https://news.google.com/rss/articles/[article-id]
```

Output in JSON format:
```
poetry run orman-web-reader google https://news.google.com/rss/articles/[article-id] --json
```

Save images to a specific directory:
```
poetry run orman-web-reader google https://news.google.com/rss/articles/[article-id] --output-dir images
```

Full options:
```
poetry run orman-web-reader google --help
```

### HTML Generator

Generate a clean HTML page from a webpage:
```
poetry run orman-web-reader html https://example.com/article
```

Specify output file and image directory:
```
poetry run orman-web-reader html https://example.com/article --output-file my_article.html --image-dir my_images
```

Process a Google News RSS article with redirect handling:
```
poetry run orman-web-reader html https://news.google.com/rss/articles/[article-id] --google-news
```

Use a custom CSS file:
```
poetry run orman-web-reader html https://example.com/article --css-file custom.css
```

Full options:
```
poetry run orman-web-reader html --help
```

### Direct Script Execution

You can also use the individual scripts directly:

```
poetry run orman-reader-mode https://example.com/article
poetry run orman-html-generator https://example.com/article
```

### Using as a Module

You can use the reader mode as a module in your own Python scripts:

```python
from orman_news_reader import extract_content
from orman_news_reader.html_generator import generate_html
from orman_news_reader.google_rss_extractor import extract_google_news_content

# Extract content from a regular URL
content = extract_content("https://example.com/article", "images")

# Access the extracted content
title = content['title']
paragraphs = content['text']
images = content['images']

# Generate HTML from the content
generate_html(content, "output.html")

# Extract content from a Google News RSS URL
google_content = extract_google_news_content("https://news.google.com/rss/articles/[article-id]", "images")

# Access Google News content with banner image
title = google_content['title']
banner_image = google_content.get('banner_image_url')
content_elements = google_content['content_elements']
```

## Example

```
poetry run orman-web-reader html https://example.com/article --output-file article.html
```

This will:
1. Extract the main content from the article
2. Save any images to the 'images' directory
3. Generate a clean HTML file with the article content
4. Apply a responsive design that works well on all devices

## How It Works

The package uses:
- `requests` to fetch the webpage
- `readability-lxml` to extract the main content
- `BeautifulSoup` to parse the HTML and extract text and images
- `Pillow` for image processing
- `Selenium` for handling JavaScript redirects in Google News RSS articles

### Standard Reader Mode
The standard reader mode extracts content directly from the provided URL using readability algorithms.

### Google News RSS Extractor
The Google News RSS extractor:
1. Uses Selenium WebDriver to follow redirects from Google News URLs to the actual article
2. Extracts high-quality banner images for carousels from Open Graph tags, Twitter cards, or featured images
3. Processes the article content using the standard reader mode
4. Returns a structured object with the article title, content, and banner image URL

## Requirements

- Python 3.8+
- Chrome/Chromium browser (for Selenium when using Google News features)
- Dependencies are managed by Poetry

## Development

### Setting up the development environment

```
git clone <repository-url>
cd <repository-directory>
poetry install
```

### Running tests

```
poetry run pytest
```

### Building the package

```
poetry build
```

### Publishing to PyPI

```
poetry publish
```
