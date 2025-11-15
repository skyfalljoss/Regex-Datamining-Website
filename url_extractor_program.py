"""
Regex Data Mining of Websites
Combined Local HTML Files and URLs Version
Authors: Adapted for educational purposes

This program reads a list of URLs and/or HTML file paths from sources.txt,
extracts all href/src links using regular expressions, and exports results
to Excel/CSV.
"""

import re
import os
from typing import Dict, List, Tuple
from urllib.parse import urlparse
from datetime import datetime

import requests
import pandas as pd

# Define the base directory where results will be saved
BASE_DIR ="./results"

class URLExtractor:
    def __init__(self):
        # Pattern for complete URLs with protocol (http, https, ftp)
        # This regex looks for href or src attributes followed by an equals sign,
        # optional whitespace, a quote (single or double), the URL content,
        # and a closing quote. It captures the URL content in group 1.
        # Example matches: href="https://example.com", src='ftp://file.txt'
        self.url_with_protocol = re.compile(
            r"(?:href|src)\s*=\s*['\"]\s*((?:https?|ftp)://[^'\"\s>]+)['\"]",
            re.IGNORECASE
        )

        # Pattern for protocol-relative URLs (//example.com)
        # This matches URLs that start with //, often used for CDN resources
        # to inherit the protocol (http/https) from the current page.
        # Example matches: href="//cdn.example.com/style.css"
        self.protocol_relative = re.compile(
            r"(?:href|src)\s*=\s*['\"]\s*(//[^'\"\s>]+)['\"]",
            re.IGNORECASE
        )

        # Pattern for absolute paths (/path/to/resource)
        # This matches paths that start with /, representing the root of the domain.
        # Example matches: href="/about", src="/images/logo.png"
        self.absolute_path = re.compile(
            r"(?:href|src)\s*=\s*['\"]\s*(/[^'\"\s>]+)['\"]",
            re.IGNORECASE
        )

        # File extension patterns for categorizing extracted URLs
        # These are used in the categorize_url method to determine the type of resource
        self.image_extensions = re.compile(r'\.(jpg|jpeg|png|gif|bmp|svg|webp|ico)(?:\?.*)?$', re.IGNORECASE)
        self.video_extensions = re.compile(r'\.(mp4|avi|mov|wmv|flv|webm|mkv)(?:\?.*)?$', re.IGNORECASE)
        self.audio_extensions = re.compile(r'\.(mp3|wav|ogg|flac|aac|m4a)(?:\?.*)?$', re.IGNORECASE)
        self.document_extensions = re.compile(r'\.(pdf|doc|docx|xls|xlsx|ppt|pptx|txt|csv)(?:\?.*)?$', re.IGNORECASE)
        self.script_extensions = re.compile(r'\.(js|css)(?:\?.*)?$', re.IGNORECASE)
        self.archive_extensions = re.compile(r'\.(zip|rar|tar|gz|7z)(?:\?.*)?$', re.IGNORECASE)

    def fetch_html_from_url(self, url: str) -> str:
        """
        Fetches the HTML content from a given URL.
        Returns the content as a string, or an empty string if an error occurs.
        """
        try:
            # Send an HTTP GET request to the URL with a 10-second timeout
            response = requests.get(url, timeout=10)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            # Return the text content of the response
            return response.text
        except requests.RequestException as e:
            # If any error occurs during the request, print an error message and return an empty string
            print(f"Error fetching URL {url}: {e}")
            return ""

    def read_html_file(self, filepath: str) -> str:
        """
        Reads the content of an HTML file from the local filesystem.
        Returns the content as a string, or an empty string if an error occurs.
        """
        try:
            # Open the file in read mode with UTF-8 encoding, ignoring characters that can't be decoded
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                # Read and return the entire file content
                return f.read()
        except Exception as e:
            # If any error occurs during file reading, print an error message and return an empty string
            print(f"Error reading file {filepath}: {e}")
            return ""

    def categorize_url(self, url: str) -> str:
        """
        Categorizes a URL based on its file extension or special protocol.
        Returns a string representing the category.
        """
        # Check the URL against pre-compiled regex patterns for different file types
        if self.image_extensions.search(url):
            return "Image"
        elif self.video_extensions.search(url):
            return "Video"
        elif self.audio_extensions.search(url):
            return "Audio"
        elif self.document_extensions.search(url):
            return "Document"
        elif self.script_extensions.search(url):
            return "Script/Style"
        elif self.archive_extensions.search(url):
            return "Archive"
        # Check for special link types that don't have file extensions
        elif re.search(r'#', url): # Anchor links like #section1
            return "Anchor Link"
        elif re.search(r'mailto:', url, re.IGNORECASE): # Email links like mailto:someone@example.com
            return "Email Link"
        elif re.search(r'tel:', url, re.IGNORECASE): # Phone links like tel:+1234567890
            return "Phone Link"
        else: # If none of the above, assume it's a webpage link
            return "Webpage"

    def extract_urls(self, html_content: str) -> List[Tuple[str, str, str]]:
        """
        Extracts URLs from the provided HTML content using the defined regex patterns.
        Returns a list of tuples containing (URL, URL Type, Category).
        """
        # Initialize an empty list to store all extracted URLs
        extracted_urls = []

        # Extract URLs with protocol (e.g., https://example.com)
        # Find all matches using the compiled regex pattern
        for match in self.url_with_protocol.finditer(html_content):
            # Extract the captured group (the URL itself)
            url = match.group(1)
            # Assign the type based on the pattern used
            url_type = "Complete URL"
            # Determine the category of the URL
            category = self.categorize_url(url)
            # Append the extracted information as a tuple to the list
            extracted_urls.append((url, url_type, category))

        # Extract protocol-relative URLs (e.g., //example.com/resource)
        for match in self.protocol_relative.finditer(html_content):
            url = match.group(1)
            url_type = "Protocol-Relative"
            category = self.categorize_url(url)
            extracted_urls.append((url, url_type, category))

        # Extract absolute paths (e.g., /path/to/page.html)
        for match in self.absolute_path.finditer(html_content):
            url = match.group(1)
            # Ensure it's not already a full URL (to avoid double processing if a full URL accidentally matches this pattern)
            if not url.startswith(('http://', 'https://', 'ftp://', '//')):
                url_type = "Absolute Path"
                category = self.categorize_url(url)
                extracted_urls.append((url, url_type, category))

        # Remove duplicates while preserving the original order
        # Create a set to track seen URLs
        seen = set()
        # Create a new list for unique URLs
        unique_urls = []
        for url_tuple in extracted_urls:
            # Check if the URL part (index 0) has been seen before
            if url_tuple[0] not in seen:
                # Add the URL to the seen set
                seen.add(url_tuple[0])
                # Add the entire tuple to the unique list
                unique_urls.append(url_tuple)

        # Return the list of unique URLs with their types and categories
        return unique_urls

    def process_source(self, source: str) -> Dict:
        """
        Detects whether the source is a URL or a file path and processes it accordingly.
        Returns a dictionary containing the results for the source.
        """
        # Parse the source string to check if it has a URL scheme (http, https, ftp)
        is_url = bool(urlparse(source).scheme in ("http", "https", "ftp"))
        # Print a message indicating which source is being processed
        print(f"Processing: {source}")

        # Fetch HTML content based on whether it's a URL or a file
        html_content = self.fetch_html_from_url(source) if is_url else self.read_html_file(source)

        # Check if content retrieval was successful
        if not html_content:
            # Return a dictionary indicating failure
            return {
                'filename': source, # Store the original source name
                'total_urls': 0, # No URLs found
                'urls': [], # Empty list of URLs
                'category_counts': {}, # Empty category counts
                'error': 'Failed to retrieve content' # Error message
            }

        # Extract URLs from the retrieved HTML content
        urls = self.extract_urls(html_content)

        # Count the occurrences of each category
        category_counts = {}
        for _, _, category in urls:
            # Increment the count for the current category
            category_counts[category] = category_counts.get(category, 0) + 1

        # Return a dictionary containing the results for this source
        return {
            'filename': source, # Store the original source name
            'total_urls': len(urls), # Total number of unique URLs found
            'urls': urls, # List of extracted URL tuples
            'category_counts': category_counts, # Dictionary of category counts
            'error': None # No error occurred
        }

    def export_to_csv(self, results: List[Dict], output_filename: str):
        """
        Exports the extraction results to a CSV file.
        """
        # Prepare a list of dictionaries for the pandas DataFrame
        data = []
        # Iterate through each source's results
        for result in results:
            # Iterate through each URL tuple found in the source
            for url, url_type, category in result['urls']:
                # Create a dictionary for each URL and add it to the data list
                data.append({
                    'Source': result['filename'], # The source file/URL where the link was found
                    'URL': url, # The extracted URL
                    'URL Type': url_type, # The type (Complete, Relative, etc.)
                    'Category': category # The category (Image, Webpage, etc.)
                })
        # Create a pandas DataFrame from the collected data
        df = pd.DataFrame(data)
        # Construct the full output path
        output_dir = f"{BASE_DIR}/{output_filename}"
        # Write the DataFrame to a CSV file without the index column
        df.to_csv(output_dir, index=False)
        # Print a confirmation message
        print(f"\nResults exported to: {output_dir}")

    def export_to_excel(self, results: List[Dict], output_filename: str):
        """
        Exports the extraction results to an Excel file with multiple sheets.
        """
        # Construct the full output path
        output_dir = f"{BASE_DIR}/{output_filename}"
        try:
            # Prepare data for the main sheet (All URLs)
            data = []
            for result in results:
                for url, url_type, category in result['urls']:
                    data.append({
                        'Source': result['filename'],
                        'URL': url,
                        'URL Type': url_type,
                        'Category': category
                    })

            # Prepare data for the summary sheet
            summary_data = []
            for result in results:
                # Create a base summary row
                summary_row = {
                    'Source': result['filename'],
                    'Total URLs': result['total_urls']
                }
                # Add category counts dynamically. If a category wasn't found in this source,
                # it will be added with a count of 0.
                # This ensures all categories found across all sources appear in the summary,
                # with 0s for sources that don't have that category.
                all_categories = set()
                for r in results:
                    all_categories.update(r.get('category_counts', {}).keys())
                for cat in all_categories:
                    summary_row[cat] = result.get('category_counts', {}).get(cat, 0)
                
                summary_data.append(summary_row)

            # Use pandas ExcelWriter to create an Excel file with multiple sheets
            with pd.ExcelWriter(output_dir, engine='openpyxl') as writer:
                # Create DataFrames
                df_main = pd.DataFrame(data)
                df_summary = pd.DataFrame(summary_data)
                # Write DataFrames to respective sheets
                df_main.to_excel(writer, sheet_name='All URLs', index=False)
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
            # Print a confirmation message
            print(f"\nResults exported to: {output_dir}")
        except Exception as e:
            # If Excel export fails, print an error and fall back to CSV
            print(f"Error exporting to Excel: {e}")
            print("Falling back to CSV export...")
            # Replace .xlsx with .csv for the fallback filename
            self.export_to_csv(results, output_filename.replace('.xlsx', '.csv'))

    def print_summary(self, results: List[Dict]):
        """
        Prints a summary of the extraction results to the console.
        """
        print("\n" + "="*70)
        print("EXTRACTION SUMMARY")
        print("="*70)
        
        # Calculate the total number of URLs found across all sources
        total_urls = sum(r['total_urls'] for r in results)
        print(f"\nTotal Sources Processed (URLs/files): {len(results)}")
        print(f"Total URLs Found: {total_urls}")
        
        print("\nPer-Source Breakdown:")
        print("-" * 70)
        # Iterate through each source's results and print details
        for result in results:
            print(f"\n{result['filename']}: {result['total_urls']} URLs")
            # If category counts exist for this source, print them
            if result.get('category_counts'):
                # Sort categories alphabetically for consistent output
                for category, count in sorted(result['category_counts'].items()):
                    print(f"  - {category}: {count}")
                    

def load_sources_from_file(filename):
    """
    Loads a list of sources (URLs or file paths) from a text file.
    Each source should be on a separate line.
    """
    # Open the file and read lines, stripping whitespace and filtering out empty lines
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def main():
    """
    The main execution function.
    Orchestrates the loading of sources, processing, summarizing, and exporting.
    """
    # Create an instance of the URLExtractor class
    extractor = URLExtractor()
    
    # Load the list of sources from the 'sources.txt' file
    sources = load_sources_from_file('sources.txt')
    
    # Process each source and collect the results
    results = [extractor.process_source(src) for src in sources]
    
    # Check if any sources were successfully processed
    if not results:
        print("No sources were successfully processed.")
        return
    
    # Print a summary of the extraction results to the console
    extractor.print_summary(results)
    
    # Generate a timestamp for the output filenames (e.g., 20231027_153045)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define the output filenames using the timestamp
    output_excel = f"url_extraction_results_{timestamp}.xlsx"
    # Export results to an Excel file
    extractor.export_to_excel(results, output_excel)
    
    # Define the CSV output filename
    output_csv = f"url_extraction_results_{timestamp}.csv"
    # Export results to a CSV file
    extractor.export_to_csv(results, output_csv)
    
    # Print a final completion message
    print("\nExtraction complete!")

if __name__ == "__main__":
    main()