# Moving-Average Crossover Backtest

A backtest of the classic moving-average crossover trading strategy, built from scratch to learn how systematic strategies are constructed and evaluated. For a set of tickers, it goes long when a short-term moving average sits above a long-term one and compares that strategy against simply buying and holding.

## The strategy

The moving-average crossover is one of the foundational trend-following strategies. The idea: when a short-term moving average (50-day) rises above a long-term one (200-day), the recent trend is upward, so hold a long position; when it falls below, stay out. This project implements that rule and measures whether it would have beaten buy-and-hold.

## What it does

For each ticker (AAPL, MSFT, GOOG by default), the pipeline:

1. **Ingests data** — daily OHLCV from Yahoo Finance (2020–2024), indexed by ticker and date.
2. **Builds features** — daily returns, 50-day and 200-day moving averages, and 10-day rolling volatility.
3. **Generates signals** — long (1) when the 50-day MA is above the 200-day MA, flat (0) otherwise. The signal is shifted one day before it is applied to returns, so the strategy only acts on information it would actually have had at the time.
4. **Backtests** — computes strategy cumulative return against buy-and-hold cumulative return.
5. **Reports** — total return, volatility, and days in market per ticker, plus plots of price against the two moving averages and the strategy equity curve against buy-and-hold.

## Running it

```bash
pip install pandas numpy yfinance matplotlib
python main.py
```

Edit `tickers_list` in `main.py` to change the universe.

## Structure

- `main.py` — the pipeline: data ingestion, feature building, backtest, and reporting.
- `helper.py` — moving averages, signal and strategy-return logic, cumulative returns, evaluation metrics, and plotting.

## A finding

In the 2020–2024 window, the crossover outperformed buy-and-hold for GOOG but lagged it for MSFT and especially AAPL. The likely reason is structural to the strategy: the 50/200-day crossover is slow, so during the sharp post-COVID recovery it re-entered too late to capture much of the rebound in the names that snapped back fastest. Trend-following strategies trade responsiveness for stability, and this is that tradeoff showing up in the results.

## Known limitations

Deliberate, since this is a strategy-research prototype rather than a live-tradeable system:

- **No transaction costs or slippage.** Each signal change is assumed free; real costs would reduce the returns shown.
- **A 50/200-day crossover is intentionally slow** and lags sharp reversals, as the finding above shows.
- **The first 200 days have no long-term average defined,** so the strategy holds no position until the 200-day window fills.
- **Long-only, single fixed parameter pair.** A fuller version would test other MA windows, allow short positions, and validate across more tickers and time periods.

## Possible next steps

Model transaction costs, sweep the moving-average windows, add short positions, and test on a broader universe and multiple market regimes.
