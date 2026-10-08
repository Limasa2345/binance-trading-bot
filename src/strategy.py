from __future__ import annotations

import pandas as pd


class TrendStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50, rsi_period: int = 14) -> None:
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_period = rsi_period

    def _rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(com=period - 1, adjust=False).mean()
        avg_loss = loss.ewm(com=period - 1, adjust=False).mean()
        rs = avg_gain / avg_loss.replace(0, 1e-9)
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)

    def prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        prepared = df.copy()
        prepared["sma_short"] = prepared["close"].rolling(self.short_window).mean()
        prepared["sma_long"] = prepared["close"].rolling(self.long_window).mean()
        prepared["rsi"] = self._rsi(prepared["close"], self.rsi_period)
        prepared["volume_sma"] = prepared["volume"].rolling(20).mean()
        prepared["trend_strength"] = prepared["sma_short"] - prepared["sma_long"]
        return prepared

    def signal(self, row: pd.Series) -> int:
        bullish = (
            row["close"] > row["sma_short"]
            and row["sma_short"] > row["sma_long"]
            and row["rsi"] > 50
            and row["volume"] > row["volume_sma"]
        )
        bearish = (
            row["close"] < row["sma_short"]
            and row["sma_short"] < row["sma_long"]
            and row["rsi"] < 50
            and row["volume"] > row["volume_sma"]
        )
        if bullish:
            return 1
        if bearish:
            return -1
        return 0
