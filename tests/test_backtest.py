from __future__ import annotations

import pandas as pd

from src.backtest import BacktestEngine
from src.strategy import TrendStrategy


def test_backtest_basic() -> None:
    candles = []
    base = 100.0
    for i in range(1, 120):
        close = base + i * 0.8
        candles.append(
            {
                "open": close - 1,
                "high": close + 1,
                "low": close - 2,
                "close": close,
                "volume": 1000 + i,
            }
        )

    df = pd.DataFrame(candles)
    strategy = TrendStrategy()
    prepared = strategy.prepare(df)
    engine = BacktestEngine(initial_balance=1000.0)
    results = engine.run(prepared, strategy.signal)

    assert "accuracy" in results
    assert results["total_trades"] >= 0
    assert results["final_balance"] >= 0


if __name__ == "__main__":
    test_backtest_basic()
    print("Test passed")
