import os
import requests
from bs4 import BeautifulSoup
import json

def scrape_product_and_image_urls(base_url, product_pattern="/product"):
    try:
        # Send a GET request to the base URL
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {base_url}: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Initialize a list for storing product and image URL pairs
    product_data = []

    # Find all product links and their associated images
    for product_card in soup.find_all("div", class_="ProductCard_Wrapper_DisplayArea"):
        # Extract product URL
        product_url = None
        a_tag = product_card.find("a", href=True)
        if a_tag:
            href = a_tag["href"]
            if product_pattern in href:
                product_url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")

        # Extract image URL
        image_url = None
        img_tag = product_card.find("img", src=True)
        if img_tag:
            src = img_tag["src"]
            image_url = src if src.startswith("http") else base_url.rstrip("/") + "/" + src.lstrip("/")

        # Add to the list if both URLs are found
        if product_url and image_url:
            product_data.append({"product_url": product_url, "image_url": image_url})

    return product_data

def save_data_to_file(data, folder_name="product_url", file_name="product_and_image_urls.json"):
    # Create the folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    # Save the data to a JSON file
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved data to {file_path}")

if __name__ == "__main__":
    # Base URL to scrape
    base_url = "https://mamaearth.in/shop"

    # Scrape product and image URLs
    data = scrape_product_and_image_urls(base_url)

    # Save the data to a file
    save_data_to_file(data)