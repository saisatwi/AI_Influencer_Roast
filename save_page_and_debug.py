# save_page_and_debug.py
import sys, traceback, requests
from bs4 import BeautifulSoup
from scraper_helpers import safe_select_text, safe_select_list

def save_html(content, filename="last_page.html"):
    with open(filename, "wb") as f:
        f.write(content if isinstance(content, bytes) else content.encode("utf-8"))

def log_error(exc):
    with open("scrape_error.log", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())
    print("Saved traceback to scrape_error.log")

def debug_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    print(f"Fetching: {url}")
    r = requests.get(url, headers=headers, timeout=20)
    print(f"HTTP {r.status_code}; content length {len(r.content)} bytes")
    save_html(r.content, "last_page.html")
    soup = BeautifulSoup(r.content, "html.parser")

    selectors = [
        ("title", "h1#title, span#productTitle"),
        ("price", "#priceblock_ourprice, #priceblock_dealprice, .a-price .a-offscreen"),
        ("description", "#productDescription, #feature-bullets"),
        ("images", "#imgTagWrapperId img, .imgTagWrapper img"),
    ]

    for name, sel in selectors:
        elems = soup.select(sel)
        print(f"{name}: selector='{sel}' -> found {len(elems)} elements")
        if elems:
            print("  sample:", elems[0].get_text(strip=True)[:200])

    try:
        # fragile extraction to reproduce IndexError if selectors fail
        title_elem = soup.select("h1#title, span#productTitle")
        title = title_elem[0].get_text(strip=True)
        price_elem = soup.select("#priceblock_ourprice, #priceblock_dealprice, .a-price .a-offscreen")
        price = price_elem[0].get_text(strip=True)
        bullets = [li.get_text(strip=True) for li in soup.select("#feature-bullets li")]
        data = {"title": title, "price": price, "features": bullets}
        print("Extracted data preview:", data)
    except Exception as e:
        print("Exception during extraction:", type(e).__name__, e)
        log_error(e)
        save_html(soup.prettify().encode("utf-8"), "last_page_pretty.html")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python save_page_and_debug.py \"PRODUCT_URL\"")
        sys.exit(1)
    url = sys.argv[1]
    try:
        debug_url(url)
    except Exception:
        print("Debug run failed. See last_page.html and scrape_error.log for details.")
        sys.exit(2)
    else:
        print("Debug run completed. Inspect last_page.html and scrape_error.log if needed.")
