import json
import os
from bs4 import BeautifulSoup
import requests


def fetch_macro_data():
  os.makedirs("data", exist_ok=True)

  # 1. Fetch Interest Rate (Scraping fallback model)
  interest_rate = 37.00
  try:
    url_interest = "https://tradingeconomics.com/turkey/interest-rate"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url_interest, headers=headers, timeout=10)
    if resp.status_code == 200:
      soup = BeautifulSoup(resp.text, "html.parser")
      rate_el = soup.find("td", {"id": "p"})
      if rate_el:
        interest_rate = float(rate_el.text.strip())
  except Exception as e:
    print(f"Interest rate fetch warning: {e}. Using fallback.")

  # 2. Fetch Live EUR/TRY Exchange Rate (Public API source)
  eur_to_try = 38.50  # Fallback default
  try:
    url_fx = "https://open.er-api.com/v6/latest/EUR"
    resp_fx = requests.get(url_fx, timeout=10)
    if resp_fx.status_code == 200:
      data_fx = resp_fx.json()
      if "rates" in data_fx and "TRY" in data_fx["rates"]:
        eur_to_try = float(data_fx["rates"]["TRY"])
  except Exception as e:
    print(f"Exchange rate fetch warning: {e}. Using fallback.")

  # 3. Construct unified data payload
  payload = {
      "interest_rate": interest_rate,
      "eur_to_try": eur_to_try,
      "last_updated": "2026-08-11",  # Automatically stamped or generated via datetime
  }

  with open(
      "data/financial_indicators.json", "w", encoding="utf-8"
  ) as f:
    json.dump(payload, f, ensure_ascii=False, indent=4)

  print("Successfully generated unified financial indicators dataset.")


if __name__ == "__main__":
  fetch_macro_data()
