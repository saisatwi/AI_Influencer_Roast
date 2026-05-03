# scraper_helpers.py
from bs4 import BeautifulSoup

def safe_select_text(soup, selector, default=None, index=0):
    elems = soup.select(selector)
    if not elems:
        return default
    try:
        return elems[index].get_text(strip=True)
    except Exception:
        return default

def safe_select_list(soup, selector):
    elems = soup.select(selector)
    return [e.get_text(strip=True) for e in elems] if elems else []

def is_blocked_html(content):
    txt = content.lower()
    checks = ["captcha", "robot", "unusual traffic", "enable javascript", "access denied"]
    return any(c in txt for c in checks)
