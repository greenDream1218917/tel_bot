import requests
import concurrent.futures

def fetch_15m_perp_volume(symbol):
    try:
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=15m&limit=1"
        res = requests.get(url, timeout=2).json()
        quote_volume = float(res[0][7])  # index 7 = quote volume in USDT
        return symbol, quote_volume
    except:
        return None

def get_top_15m_perp_volumes():
    info_url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    info_res = requests.get(info_url).json()
    symbols = [
        s["symbol"] for s in info_res["symbols"]
        if s["contractType"] == "PERPETUAL" and s["quoteAsset"] == "USDT"
    ]
    volumes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_15m_perp_volume, symbol) for symbol in symbols]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                volumes.append(result)
    top_20 = sorted(volumes, key=lambda x: x[1], reverse=True)[:20]
    return top_20

def get_perp_report():
    top_20 = get_top_15m_perp_volumes()
    lines = ["Top 20 Perpetual Futures by 15-Minute Quote Volume:\n"]
    for i, (symbol, volume) in enumerate(top_20, start=1):
        lines.append(f"{i:02}. {symbol}: ${volume:,.2f}")
    return "\n".join(lines)

if __name__ == "__main__":
    print(get_perp_report())
