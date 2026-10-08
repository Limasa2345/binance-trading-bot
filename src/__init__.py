from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd


def win_rate(trades: List) -> float:
    if not trades:
        return 0.0
    wins = sum(1 for trade in trades if trade.pnl > 0)
    return wins / len(trades)


def profit_factor(trades: List) -> float:
    if not trades:
        return 0.0
    gross_profit = sum(trade.pnl for trade in trades if trade.pnl > 0)
    gross_loss = -sum(trade.pnl for trade in trades if trade.pnl < 0)
    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0
    return gross_profit / gross_loss


def max_drawdown(equity_curve: List[float]) -> float:
    if not equity_curve:
        return 0.0
    curve = np.array(equity_curve, dtype=float)
    peak = np.maximum.accumulate(curve)
    drawdown = (curve - peak) / peak
    return float(np.min(drawdown)) if len(drawdown) else 0.0


def sharpe_ratio(returns: List[float], risk_free: float = 0.0) -> float:
    if len(returns) < 2:
        return 0.0
    arr = np.array(returns, dtype=float)
    if arr.std() == 0:
        return 0.0
    return float((arr.mean() - risk_free) / arr.std() * np.sqrt(252))


def expectancy(trades: List) -> float:
    if not trades:
        return 0.0
    avg_win = np.mean([trade.pnl for trade in trades if trade.pnl > 0]) if any(t.pnl > 0 for t in trades) else 0.0
    avg_loss = np.mean([trade.pnl for trade in trades if trade.pnl < 0]) if any(t.pnl < 0 for t in trades) else 0.0
    win_prob = win_rate(trades)
    loss_prob = 1 - win_prob
    if avg_loss == 0:
        return avg_win * win_prob
    return (win_prob * avg_win) + (loss_prob * avg_loss)


def compute_metrics(trades: List, initial_balance: float, equity_curve: List[float], total_trades: int) -> dict:
    if trades:
        net_profit = sum(trade.pnl for trade in trades)
        total_return = (equity_curve[-1] - initial_balance) / initial_balance
        trade_returns = [trade.pnl_pct for trade in trades]
        returns_series = pd.Series(trade_returns)
    else:
        net_profit = 0.0
        total_return = 0.0
        returns_series = pd.Series(dtype=float)

    accuracy = win_rate(trades)
    metrics = {
        "total_trades": total_trades,
        "wins": sum(1 for trade in trades if trade.pnl > 0),
        "losses": sum(1 for trade in trades if trade.pnl < 0),
        "accuracy": accuracy,
        "net_profit": net_profit,
        "total_return": total_return,
        "profit_factor": profit_factor(trades),
        "max_drawdown": max_drawdown(equity_curve),
        "sharpe": sharpe_ratio(returns_series.tolist()),
        "expectancy": expectancy(trades),
        "final_balance": equity_curve[-1] if equity_curve else initial_balance,
    }
    return metrics


def print_summary(metrics: dict, symbol: str) -> None:
    print("\n=== Resumo do Backtest ===")
    print(f"Símbolo: {symbol}")
    print(f"Trades: {metrics['total_trades']}")
    print(f"Acurácia: {metrics['accuracy'] * 100:.2f}%")
    print(f"Lucro líquido: {metrics['net_profit']:.2f}")
    print(f"Retorno total: {metrics['total_return'] * 100:.2f}%")
    print(f"Profit factor: {metrics['profit_factor']:.2f}")
    print(f"Máxima drawdown: {metrics['max_drawdown'] * 100:.2f}%")
    print(f"Sharpe: {metrics['sharpe']:.2f}")
    print(f"Expectancy: {metrics['expectancy']:.4f}")
    print(f"Saldo final: {metrics['final_balance']:.2f}")
