from __future__ import annotations

import argparse

import pandas as pd

from src.data_fetcher import BinanceDataFetcher
from src.metrics import print_summary
from src.strategy import TrendStrategy
from src.backtest import BacktestEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Backtest de estratégia para Binance")
    parser.add_argument("--symbol", type=str, default="BTC/USDT")
    parser.add_argument("--timeframe", type=str, default="1h")
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--initial-balance", type=float, default=10_000.0)
    parser.add_argument("--position-fraction", type=float, default=0.20)
    parser.add_argument("--fee-rate", type=float, default=0.001)
    args = parser.parse_args()

    fetcher = BinanceDataFetcher()
    df = fetcher.fetch_ohlcv(args.symbol, timeframe=args.timeframe, limit=args.limit)

    if df.empty:
        raise ValueError(f"Nenhum dado encontrado para {args.symbol}")

    strategy = TrendStrategy()
    prepared = strategy.prepare(df)

    engine = BacktestEngine(
        initial_balance=args.initial_balance,
        position_fraction=args.position_fraction,
        fee_rate=args.fee_rate,
    )
    results = engine.run(prepared, strategy.signal)

    print_summary(results, args.symbol)


if __name__ == "__main__":
    main()
