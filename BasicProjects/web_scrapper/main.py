import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import json
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Setting up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s %(message)s')

def get_soup(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logging.error(f"Failed to get the soup for {url}: {e}")
        return None

def clean_text(text):
    # Remove excessive newlines and strip leading/trailing whitespace
    cleaned = " ".join(text.split())
    return cleaned

def scrape_website(url, output_format, progress_bar=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    soup = get_soup(url, headers)
    if not soup:
        return
    
    data = {}

    # Extract title
    data["Title"] = soup.title.text.strip() if soup.title else "No title found"
    
    # Extract all paragraphs
    data["Paragraphs"] = list(set([clean_text(p.text) for p in soup.find_all("p")])) if soup.find_all("p") else ["No paragraphs found"]
    
    # Extract all divs
    data["Divs"] = list(set([clean_text(div.text) for div in soup.find_all("div")])) if soup.find_all("div") else ["No divs found"]
    
    # Extract all spans
    data["Spans"] = list(set([clean_text(span.text) for span in soup.find_all("span")])) if soup.find_all("span") else ["No spans found"]
    
    # Extract external links
    data["External Links"] = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(url, link['href'])
        if full_url.startswith('http'):
            data["External Links"].append(full_url)
    
    # Extract images
    data["Images"] = []
    for img in soup.find_all('img', src=True):
        img_url = urljoin(url, img['src'])
        data["Images"].append(img_url)
    
    # Extract meta tags
    data["Meta Description"] = clean_text(soup.find("meta", attrs={"name": "description"})['content']) if soup.find("meta", attrs={"name": "description"}) else "No description found"
    data["Meta Keywords"] = clean_text(soup.find("meta", attrs={"name": "keywords"})['content']) if soup.find("meta", attrs={"name": "keywords"}) else "No keywords found"
    
    # Save data to file
    if output_format == 'csv':
        with open('scraped_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())
            writer.writerow([data[key] if isinstance(data[key], str) else " | ".join(data[key]) for key in data])
    elif output_format == 'json':
        with open('scraped_data.json', mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    logging.info(f"Scraped {url} successfully.")
    if progress_bar:
        progress_bar.update(1)

def main():
    urls = []
    while True:
        url = input("Enter a URL to scrape (or 'q' to quit): ")
        if url.lower() == 'q':
            break
        urls.append(url)
    
    output_format = input("Choose output format (csv/json) [default: csv]: ").strip().lower()
    if output_format not in ['csv', 'json']:
        output_format = 'csv'  # Default to CSV if input is invalid
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        total_urls = len(urls)
        with tqdm(total=total_urls, desc='Scraping Progress') as progress_bar:
            futures = [executor.submit(scrape_website, url, output_format, progress_bar) for url in urls]
            for future in as_completed(futures):
                future.result()
    
    print("Scraping completed. Check scraped_data.csv or scraped_data.json and scraper.log for details.")

if __name__ == "__main__":
    main()
