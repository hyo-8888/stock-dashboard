"""Fetch Korean stock prices from Naver Finance and save as JSON."""
import json
import re
import urllib.request

TICKERS = [
    "005930.KS", "005380.KS", "003550.KS", "010120.KS",
    "107640.KQ", "450080.KQ", "035720.KS", "034020.KS",
    "018260.KS", "480040.KS", "006400.KS", "064400.KS",
    "035420.KS", "042700.KS", "103590.KS",
]


def fetch_naver(code: str) -> int | None:
    url = f"https://m.stock.naver.com/api/stock/{code}/basic"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            price = data.get("closePrice") or data.get("stockEndPrice")
            if price:
                return int(str(price).replace(",", ""))
    except Exception:
        pass
    return None


def main():
    prices = {}
    for ticker in TICKERS:
        code = re.sub(r"\.(KS|KQ)$", "", ticker)
        price = fetch_naver(code)
        if price is not None:
            prices[ticker] = price
            print(f"  {ticker}: {price:,}")
        else:
            print(f"  {ticker}: FAILED")

    with open("prices.json", "w") as f:
        json.dump(prices, f, indent=2)
    print(f"\nSaved {len(prices)}/{len(TICKERS)} prices to prices.json")


if __name__ == "__main__":
    main()
