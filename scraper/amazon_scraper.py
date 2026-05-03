import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def _get_html(url, timeout=15):
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def _safe_text(el):
    return el.get_text(strip=True) if el else ""

def scrape_amazon(url):
    """
    Returns a dict:
    {
      "title": str,
      "price": str or None,
      "top_image": url or None,
      "description": str or None,
      "top_reviews": [str,...]
    }
    """
    # Basic validation
    parsed = urlparse(url)
    if "amazon." not in parsed.netloc:
        raise ValueError("URL does not look like an Amazon product page.")

    html = _get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title = None
    title_el = soup.find(id="productTitle")
    if title_el:
        title = _safe_text(title_el)
    else:
        # fallback
        og_title = soup.find("meta", property="og:title")
        title = og_title["content"] if og_title and og_title.get("content") else None

    # Price
    price = None
    price_el = soup.find(id="priceblock_ourprice") or soup.find(id="priceblock_dealprice")
    if price_el:
        price = _safe_text(price_el)
    else:
        # meta fallback
        price_meta = soup.find("span", class_="a-offscreen")
        price = _safe_text(price_meta) if price_meta else None

    # Top image
    top_image = None
    img_el = soup.find(id="landingImage") or soup.find("img", {"id": "imgBlkFront"})
    if img_el and img_el.get("src"):
        top_image = img_el.get("src")
    else:
        og_img = soup.find("meta", property="og:image")
        top_image = og_img["content"] if og_img and og_img.get("content") else None

    # Description
    desc = None
    desc_el = soup.find(id="productDescription")
    if desc_el:
        desc = _safe_text(desc_el)
    else:
        bullets = soup.select("#feature-bullets ul li")
        if bullets:
            desc = " ".join([_safe_text(b) for b in bullets if _safe_text(b)])

    # Top reviews (grab a few)
    reviews = []
    review_els = soup.select(".review-text-content span")
    for r in review_els[:5]:
        text = _safe_text(r)
        if text:
            reviews.append(text)

    # If no reviews on page, try the reviews iframe link pattern
    if not reviews:
        try:
            asin = None
            # attempt to extract ASIN
            path_parts = parsed.path.split("/")
            if "dp" in path_parts:
                dp_index = path_parts.index("dp")
                asin = path_parts[dp_index + 1] if len(path_parts) > dp_index + 1 else None
            if not asin:
                q = parse_qs(parsed.query)
                asin = q.get("ASIN", [None])[0]
            if asin:
                reviews_url = f"https://www.amazon.com/product-reviews/{asin}/?sortBy=recent"
                html2 = _get_html(reviews_url)
                soup2 = BeautifulSoup(html2, "html.parser")
                review_els2 = soup2.select(".review-text-content span")
                for r in review_els2[:5]:
                    t = _safe_text(r)
                    if t:
                        reviews.append(t)
        except Exception:
            pass

    return {
        "title": title,
        "price": price,
        "top_image": top_image,
        "description": desc,
        "top_reviews": reviews
    }
