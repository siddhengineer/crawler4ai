import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_image_urls():
    # 1. Define the extraction schema for image URLs
    schema = {
        "name": "Image URLs",
        "baseSelector": "div.ProductCard_Wrapper_DisplayArea",  # Repeated elements
        "fields": [
            {
                "name": "image_url",
                "selector": "img",
                "type": "attribute",
                "attribute": "src"  # Extract the 'src' attribute of <img> tags
            }
        ]
    }

    # 2. Create the extraction strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    # 3. Set up your crawler config
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        # 4. Run the crawl and extraction
        result = await crawler.arun(
            url="https://mamaearth.in/shop",
            config=config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return

        # 5. Parse the extracted JSON
        data = json.loads(result.extracted_content)
        print(f"Extracted {len(data)} image entries")
        
        # Save the extracted data to a file
        with open("test_image_urls.json", "w") as f:
            json.dump(data, f, indent=2)

        print("Image URLs have been saved to test_image_urls.json")

# Run the async function
asyncio.run(extract_image_urls())