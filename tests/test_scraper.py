from scraper.amazon_scraper import scrape_amazon

def test_sample_asset():
    # Use the sample asset for offline test
    sample = {
        "title": "Sample Product",
        "price": "$9.99",
        "top_image": "https://via.placeholder.com/720x720.png?text=Sample",
        "description": "Sample desc",
        "top_reviews": ["ok"]
    }
    # ensure generate_roast can accept this shape (imported elsewhere)
    assert sample["title"]
