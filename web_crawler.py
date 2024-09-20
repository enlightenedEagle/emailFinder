import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os
import time
import csv
import random
import argparse

# Create a folder for logs if it doesn't exist
log_folder = "crawler_logs"
os.makedirs(log_folder, exist_ok=True)

# Function to create subfolder for a specific website
def create_website_folder(website_name):
    website_folder = os.path.join(log_folder, website_name)
    os.makedirs(website_folder, exist_ok=True)
    return website_folder

# Initialize sets for tracking visited URLs and emails
visited_urls = set()
found_emails = set()

def extract_emails(text):
    """Extract emails from the given text using regex."""
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

def save_to_file(file_path, content):
    """Append content to a given file."""
    with open(file_path, 'a') as f:
        f.write(content + '\n')

def log_emails(emails, url, email_log_file):
    """Log emails to CSV file."""
    with open(email_log_file, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        for email in emails:
            csv_writer.writerow([email, url])

def get_headers():
    """Generate random headers to mimic a real browser."""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.google.com',
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'fr-FR,fr;q=0.9', 'es-ES,es;q=0.9'])
    }

def is_valid_url(url):
    """Check if the URL has valid extensions."""
    invalid_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.docx', '.pptx')
    return not url.endswith(invalid_extensions)

def crawl(url, website_folder, delay):
    """Crawl the given URL, extract emails, and follow internal links."""
    if url in visited_urls or not is_valid_url(url):
        if not is_valid_url(url):
            save_to_file(os.path.join(website_folder, "ignored_logs.txt"), url)  # Log ignored URLs
        return
    
    visited_urls.add(url)  # Mark URL as visited
    print(f"\n--- Crawling: {url} ---")
    
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = extract_emails(soup.get_text())

        if emails:
            print(f"Emails found on {url}:")
            for email in set(emails):
                print(f"  - {email}")
                found_emails.add(email)
            log_emails(set(emails), url, os.path.join(website_folder, "emails.csv"))  # Log emails to CSV
        
        # Save the URL to the crawled URLs log
        save_to_file(os.path.join(website_folder, "crawled_urls.txt"), url)

        # Find and follow internal links
        base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))
        for link in soup.find_all('a', href=True):
            href = link['href']
            next_url = urljoin(base_url, href)
            if urlparse(next_url).netloc == urlparse(base_url).netloc:
                time.sleep(delay)  # Use the provided delay
                crawl(next_url, website_folder, delay)
    
    except requests.exceptions.RequestException as e:
        # Log the error and save the URL to the error log
        print(f"Error crawling {url}: {e}")
        save_to_file(os.path.join(website_folder, "error_urls.txt"), f"{url} - {e}")

# Function to set up argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description='Web Crawler for extracting emails.')
    parser.add_argument('-url', type=str, required=True, help='The starting website URL to crawl.')
    parser.add_argument('-delay', type=float, default=0.5, help='Delay in seconds between requests (default: 0.5).')
    return parser.parse_args()

# Start crawling from the initial URL
if __name__ == '__main__':
    args = parse_arguments()
    start_url = args.url
    delay = args.delay
    website_name = urlparse(start_url).netloc.replace('.', '_')  # Create a safe folder name
    website_folder = create_website_folder(website_name)

    crawl(start_url, website_folder, delay)

    # Summary of the crawl
    print("\n--- Crawl Summary ---")
    print(f"Total URLs crawled: {len(visited_urls)}")
    print(f"Total emails found: {len(found_emails)}")
