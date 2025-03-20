"""
Main entry point for the orman_news_reader package.
"""

import sys
import argparse
from orman_news_reader.reader_mode import main as reader_main
from orman_news_reader.html_generator import main as html_generator_main
from orman_news_reader.google_rss_extractor import main as google_rss_main


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Web Reader Mode - Extract content from webpages and generate clean HTML"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Reader mode command
    reader_parser = subparsers.add_parser("reader", help="Extract content from a webpage")
    reader_parser.add_argument("url", help="URL of the webpage to extract content from")
    reader_parser.add_argument("--output-dir", "-o", default="output",
                        help="Directory to save output to (default: output)")
    reader_parser.add_argument("--json", "-j", action="store_true",
                        help="Output in JSON format")
    
    # HTML generator command
    html_parser = subparsers.add_parser("html", help="Generate a clean HTML page from a webpage")
    html_parser.add_argument("url", help="URL of the webpage to extract content from")
    html_parser.add_argument("--output-file", "-o", default="reader_output.html", 
                        help="Path to save the HTML file (default: reader_output.html)")
    html_parser.add_argument("--image-dir", "-i", default="images",
                        help="Directory to save images to (default: images)")
    html_parser.add_argument("--css-file", "-c", help="Path to a custom CSS file")
    html_parser.add_argument("--google-news", "-g", action="store_true",
                        help="Process as a Google News RSS article with redirect handling")
    
    # Google RSS extractor command
    google_parser = subparsers.add_parser("google", help="Extract content from a Google News RSS article")
    google_parser.add_argument("url", help="Google News URL to extract content from")
    google_parser.add_argument("--output-dir", "-o", default="images",
                        help="Directory to save images to (default: images)")
    google_parser.add_argument("--json", "-j", action="store_true", 
                        help="Output in JSON format")
    
    args = parser.parse_args()
    
    if args.command == "reader":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        reader_main()
    elif args.command == "html":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        html_generator_main()
    elif args.command == "google":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        google_rss_main()
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 