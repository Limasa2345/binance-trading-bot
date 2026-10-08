from __future__ import annotations

from typing import Optional

import pandas as pd


class BinanceDataFetcher:
    def __init__(self, exchange_name: str = "binance") -> None:
        self.exchange_name = exchange_name

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1h",
        limit: int = 500,
        since: Optional[int] = None,
    ) -> pd.DataFrame:
        """Fetch OHLCV data for a Binance symbol."""
        try:
            import ccxt
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install the dependencies first: pip install -r requirements.txt") from exc

        exchange = ccxt.binance({"enableRateLimit": True})
        try:
            if since is None:
                ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
            else:
                ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since, limit=limit)

            df = pd.DataFrame(
                ohlcv,
                columns=["timestamp", "open", "high", "low", "close", "volume"],
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df = df.set_index("timestamp")
            df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
            return df
        finally:
            exchange.close()
