# Binance Trading Bot Backtest

Este projeto implementa um backtesting de estratégia para Binance com coleta de dados históricos, indicadores técnicos, cálculo de métricas de desempenho e verificação de acurácia.

## Objetivo

Validar uma estratégia antes de rodar em ambiente real, com foco em:

- coleta de candles da Binance
- indicadores técnicos
- lógica de entrada/saída
- backtesting
- métricas de acurácia
- comparação entre trades vencedores e perdedores

## Estrutura

- `main.py` – execução principal
- `src/data_fetcher.py` – acesso aos dados históricos da Binance
- `src/strategy.py` – indicadores e geração de sinais
- `src/backtest.py` – engine de backtesting
- `src/metrics.py` – métricas e relatório
- `tests/test_backtest.py` – testes básicos

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python main.py --symbol BTC/USDT --timeframe 1h --limit 500 --initial-balance 10000
```

### Opções

- `--symbol`: par da Binance, por exemplo `BTC/USDT`
- `--timeframe`: candle interval, como `1m`, `5m`, `15m`, `1h`
- `--limit`: número de candles
- `--initial-balance`: saldo inicial do backtest
- `--position-fraction`: percentual do saldo alocado por posição

## Estratégia usada

A estratégia base considerada aqui combina:

- SMA de 20 e 50 períodos
- RSI de 14 períodos
- volume relativo
- filtro de tendência

A regra é simples:

- compra quando o preço está acima da SMA20 e da SMA50 e o RSI está acima de 50
- venda quando o preço está abaixo da SMA20 e da SMA50 e o RSI abaixo de 50
- fechamento de posição quando aparece sinal oposto

## Métricas principais

- Acertividade (win rate)
- Total de trades
- Lucro total
- Profit factor
- Máxima drawdown
- Sharpe ratio
- Expectancy

## Importante

Backtesting não garante retorno em ambiente real. Use este projeto para validar e comparar estratégias antes de operar com dinheiro real.

## Exemplo de resultado esperado

```text
=== Resumo do Backtest ===
Símbolo: BTC/USDT
Candles: 500
Trades: 16
Acurácia: 68.75%
Win rate: 68.75%
Retorno total: 12.35%
Profit factor: 2.14
Max drawdown: 9.80%
Sharpe: 1.42
Expectancy: 0.71
```
