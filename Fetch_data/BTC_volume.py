import requests

intervals = ["5m", "15m", "30m", "1h", "2h", "4h", "8h", "12h", "1d", "3d"]

def get_binance_kline_volume(base_url, symbol, interval):
    url = f"{base_url}/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data or "code" in data:
        raise Exception(f"Error fetching data from {base_url} for {interval}: {data}")
    return float(data[0][5])  # Base asset volume (BTC)

def get_all_volumes(symbol="BTCUSDT"):
    result = {}
    for interval in intervals:
        try:
            spot_volume = get_binance_kline_volume(
                base_url="https://api.binance.com/api/v3", 
                symbol=symbol,
                interval=interval
            )
        except Exception as e:
            spot_volume = None
        try:
            perp_volume = get_binance_kline_volume(
                base_url="https://fapi.binance.com/fapi/v1", 
                symbol=symbol,
                interval=interval
            )
        except Exception as e:
            perp_volume = None
        result[interval] = {
            "spot_volume_btc": spot_volume,
            "perp_volume_btc": perp_volume,
            "total_volume_btc": (spot_volume or 0) + (perp_volume or 0)
        }
    return result

def get_volumes_report(symbol="BTCUSDT"):
    volumes = get_all_volumes(symbol)
    lines = []
    lines.append(f"{'Interval':<6} | {'Spot Volume':>12} | {'Perp Volume':>12} | {'Total Volume':>13}")
    lines.append("-" * 55)
    for interval, data in volumes.items():
        spot = f"{data['spot_volume_btc']:.4f}" if data['spot_volume_btc'] is not None else "N/A"
        perp = f"{data['perp_volume_btc']:.4f}" if data['perp_volume_btc'] is not None else "N/A"
        total = f"{data['total_volume_btc']:.4f}" if data['total_volume_btc'] is not None else "N/A"
        lines.append(f"{interval:<6} | {spot:>12} | {perp:>12} | {total:>13}")
    return "\n".join(lines)

if __name__ == "__main__":
    print(get_volumes_report())
