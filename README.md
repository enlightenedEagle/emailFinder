# Web Crawler

A simple web crawler designed to extract email addresses from websites while logging visited URLs and any errors encountered. This crawler supports basic URL validation to ignore unwanted file types and provides insights into the crawling process through log files.

## Features

- **Email Extraction**: Collects email addresses found on crawled web pages.
- **URL Logging**: Records all visited URLs and any errors encountered during the crawling process.
- **Ignored URLs Log**: Maintains a log of URLs that were ignored due to invalid file extensions (e.g., `.pdf`, `.jpg`).
- **Custom Headers**: Generates random user-agent headers to mimic real browser requests and avoid detection.
- **Recursive Crawling**: Follows internal links to explore the entire website.

## Requirements

To run this project, ensure you have Python 3.x installed. The required packages can be installed using pip.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/enlightenedEagle/web_crawler.git
   cd web_crawler
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Set the starting URL**:
   - Open the `crawler.py` file and modify the `start_url` variable to the desired website URL you want to crawl.

2. **Run the crawler**:
   ```bash
   python crawler.py
   ```

3. **Access log files**:
   - The output will generate the following log files in the `crawler_logs/` directory:

   ```
   crawler_logs/
   └── <website_name>/
       ├── crawled_urls.txt       # List of successfully crawled URLs
       ├── emails.csv              # Extracted email addresses with corresponding URLs
       ├── ignored_logs.txt        # URLs that were ignored due to invalid extensions
       └── error_urls.txt          # URLs that encountered errors during the crawling process
   ```

## Logging

The logs are structured in the following way:

- **crawled_urls.txt**: Contains a list of all the URLs that the crawler has successfully visited.
- **emails.csv**: Records all extracted email addresses along with the URLs where they were found.
- **ignored_logs.txt**: Lists any URLs that were skipped due to being deemed invalid (e.g., ending in `.pdf`, `.jpg`, etc.).
- **error_urls.txt**: Documents any URLs that resulted in errors during the crawl, along with the error message.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - for HTML parsing.
- [Requests](https://docs.python-requests.org/en/master/) - for making HTTP requests.
