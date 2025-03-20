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
   pip install web-reader-mode
   ```

## Usage

### Using Poetry

```
poetry run web-reader-mode [command] [options]
```

Available commands:
- `reader`: Extract content from a webpage
- `html`: Generate a clean HTML page from a webpage

### Reader Mode

Extract content from a webpage:
```
poetry run web-reader-mode reader https://example.com/article
```

Save images to a specific directory:
```
poetry run web-reader-mode reader https://example.com/article --output-dir images
```

Output in JSON format:
```
poetry run web-reader-mode reader https://example.com/article --json
```

Full options:
```
poetry run web-reader-mode reader --help
```

### HTML Generator

Generate a clean HTML page from a webpage:
```
poetry run web-reader-mode html https://example.com/article
```

Specify output file and image directory:
```
poetry run web-reader-mode html https://example.com/article --output-file my_article.html --image-dir my_images
```

Use a custom CSS file:
```
poetry run web-reader-mode html https://example.com/article --css-file custom.css
```

Full options:
```
poetry run web-reader-mode html --help
```

### Direct Script Execution

You can also use the individual scripts directly:

```
poetry run reader-mode https://example.com/article
poetry run html-generator https://example.com/article
```

### Using as a Module

You can use the reader mode as a module in your own Python scripts:

```python
from web_reader_mode import extract_content, generate_html

# Extract content from a URL
content = extract_content("https://example.com/article", "images")

# Access the extracted content
title = content['title']
paragraphs = content['text']
images = content['images']

# Generate HTML from the content
generate_html(content, "output.html")
```

## Example

```
poetry run web-reader-mode html https://example.com/article --output-file article.html
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

## Requirements

- Python 3.8+
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
