from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://www.amazon.com/dp/B07FZ8S74R"  # replace with your URL

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")
opts.add_argument("--window-size=1200,900")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)

# Create a Service object and pass it to webdriver.Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)

# Hide webdriver flag
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

try:
    driver.get(url)
    time.sleep(4)  # wait for JS; increase if needed
    html = driver.page_source
    with open("last_page_rendered.html", "w", encoding="utf-8") as f:
        f.write(html)
    driver.save_screenshot("last_page_screenshot.png")
    print("Saved last_page_rendered.html and last_page_screenshot.png")
finally:
    driver.quit()
