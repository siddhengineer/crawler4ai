import os
import requests
from bs4 import BeautifulSoup
import json

def scrape_product_urls(base_url, pattern="/product"):
    # Send a GET request to the base URL
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {base_url}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all anchor tags and filter URLs matching the pattern
    product_urls = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if pattern in href:
            # Ensure the URL is absolute
            if not href.startswith("http"):
                href = base_url.rstrip("/") + "/" + href.lstrip("/")
            product_urls.append(href)

    return list(set(product_urls))  # Remove duplicates

def save_urls_to_file(urls, folder_name="product_url", file_name="product_page_urls.json"):
    # Create the folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    # Save the URLs to a JSON file
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "w") as f:
        json.dump(urls, f, indent=2)
    print(f"Saved {len(urls)} product URLs to {file_path}")

if __name__ == "__main__":
    # Base URL to scrape
    base_url = "https://mamaearth.in/shop"  # Replace with the actual URL

    # Scrape product URLs
    product_urls = scrape_product_urls(base_url)

    # Save the URLs to a file
    save_urls_to_file(product_urls)