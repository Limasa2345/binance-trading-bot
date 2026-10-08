from src.data_fetcher import BinanceDataFetcher

if __name__ == "__main__":
    fetcher = BinanceDataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", timeframe="1h", limit=100)
    print(df.head())
