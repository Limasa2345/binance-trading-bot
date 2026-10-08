from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from src.metrics import compute_metrics


@dataclass
class Trade:
    side: str
    entry_index: int
    exit_index: int
    entry_price: float
    exit_price: float
    pnl: float
    pnl_pct: float
    duration: int


class BacktestEngine:
    def __init__(
        self,
        initial_balance: float = 10_000.0,
        position_fraction: float = 0.2,
        fee_rate: float = 0.001,
        stop_loss_pct: float = 0.04,
        take_profit_pct: float = 0.08,
    ) -> None:
        self.initial_balance = initial_balance
        self.position_fraction = position_fraction
        self.fee_rate = fee_rate
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

    def run(self, df: pd.DataFrame, strategy_signal) -> dict:
        equity = self.initial_balance
        position = None
        trades: List[Trade] = []
        equity_curve = [equity]
        trade_count = 0

        for idx, row in df.iterrows():
            signal = strategy_signal(row)

            if position is None:
                if signal == 1:
                    position = {
                        "side": "long",
                        "entry_index": idx,
                        "entry_price": float(row["close"]),
                        "qty": (equity * self.position_fraction) / float(row["close"]),
                        "entry_value": equity * self.position_fraction,
                        "stop_loss": float(row["close"]) * (1 - self.stop_loss_pct),
                        "take_profit": float(row["close"]) * (1 + self.take_profit_pct),
                    }
                elif signal == -1:
                    position = {
                        "side": "short",
                        "entry_index": idx,
                        "entry_price": float(row["close"]),
                        "qty": (equity * self.position_fraction) / float(row["close"]),
                        "entry_value": equity * self.position_fraction,
                        "stop_loss": float(row["close"]) * (1 + self.stop_loss_pct),
                        "take_profit": float(row["close"]) * (1 - self.take_profit_pct),
                    }
                continue

            current_price = float(row["close"])

            if position["side"] == "long":
                pnl_before_fees = (current_price - position["entry_price"]) * position["qty"]
                if current_price <= position["stop_loss"] or current_price >= position["take_profit"] or signal == -1:
                    fee = abs(pnl_before_fees) * self.fee_rate
                    pnl_after_fees = pnl_before_fees - fee
                    equity += pnl_after_fees
                    trades.append(
                        Trade(
                            side="long",
                            entry_index=position["entry_index"],
                            exit_index=idx,
                            entry_price=position["entry_price"],
                            exit_price=current_price,
                            pnl=pnl_after_fees,
                            pnl_pct=(pnl_after_fees / position["entry_value"]),
                            duration=idx - position["entry_index"],
                        )
                    )
                    trade_count += 1
                    position = None
            else:
                pnl_before_fees = (position["entry_price"] - current_price) * position["qty"]
                if current_price >= position["stop_loss"] or current_price <= position["take_profit"] or signal == 1:
                    fee = abs(pnl_before_fees) * self.fee_rate
                    pnl_after_fees = pnl_before_fees - fee
                    equity += pnl_after_fees
                    trades.append(
                        Trade(
                            side="short",
                            entry_index=position["entry_index"],
                            exit_index=idx,
                            entry_price=position["entry_price"],
                            exit_price=current_price,
                            pnl=pnl_after_fees,
                            pnl_pct=(pnl_after_fees / position["entry_value"]),
                            duration=idx - position["entry_index"],
                        )
                    )
                    trade_count += 1
                    position = None

            equity_curve.append(equity)

        results = compute_metrics(
            trades=trades,
            initial_balance=self.initial_balance,
            equity_curve=equity_curve,
            total_trades=trade_count,
        )
        results["trades"] = trades
        return results
