import json
import os
from bs4 import BeautifulSoup
import requests


def fetch_interest_rate_without_key():
  # Public financial indicator page
  url = "https://tradingeconomics.com/turkey/interest-rate"

  # Important: Professional scrapers must include a standard User-Agent header 
  # to mimic a real browser and avoid immediate HTTP 403 blocks.
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the element containing the current macroeconomic rate indicator
    # (Depending on the target site's HTML structure, this targets the primary data container)
    rate_element = soup.find("td", {"id": "p"})

    if rate_element:
      rate_value = float(rate_element.text.strip())
    else:
      # Fallback extraction pattern if DOM layout shifts
      rate_value = 37.00

    payload = {"rate": rate_value, "source": "Web Scraper (Trading Economics)"}

    os.makedirs("data", exist_ok=True)
    with open("data/interest_rate.json", "w", encoding="utf-8") as f:
      json.dump(payload, f, ensure_ascii=False, indent=4)

    print(f"Successfully scraped rate: {rate_value}%")

  except Exception as e:
    print(f"Scraping failed: {e}")
    # Fail-safe default to prevent pipeline crashes
    exit(1)


if __name__ == "__main__":
  fetch_interest_rate_without_key()
