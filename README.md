# Global Portfolio Tracker & Performance Dashboard

An interactive Streamlit dashboard that tracks a multi-currency, multi-asset portfolio using live market data from Yahoo Finance. It converts every holding into a base currency of your choice, calculates risk and performance metrics, and compares the portfolio against global benchmark indices.

## Features
1. Editable holdings table: ticker, shares, buy price, currency, region and asset class (add or remove rows)
2. Automatic FX conversion of all holdings into a selectable base currency (USD, INR, EUR, GBP, JPY)
3. Portfolio value, total P&L and return for each position
4. Risk metrics: annualized volatility, Sharpe ratio and maximum drawdown
5. Benchmark comparison, rebased to 100: S&P 500, MSCI World, Nifty 50, Nikkei 225, Euro Stoxx 50
6. Allocation charts by region, asset class and currency
7. Drawdown chart and a correlation heatmap of daily returns between holdings
8. Configurable history window (6 months to 5 years) and risk-free rate

## Tech Stack
Python, Streamlit, Pandas, NumPy, Plotly, yfinance

## Getting Started
```bash
git clone https://github.com/Varnika-M/Portfolio-Tracker.git
cd Portfolio-Tracker
pip install -r requirements.txt
streamlit run global_portfolio_app.py
```

## Usage
1. Choose the base currency, history window, risk-free rate and benchmark in the sidebar.
2. Edit the holdings table. Use Yahoo Finance tickers (for example `AAPL`, `ASML.AS`, `7203.T`, `RELIANCE.NS`, `GLD`).
3. Enter each buy price in the asset's own currency, and set the Currency column to match.
4. The dashboard updates automatically with metrics, charts and tables.

## How It Works
1. Daily closing prices are downloaded with `yfinance` (cached for 10 minutes).
2. Each holding's price history is converted to the base currency using the matching FX rate (for example `EURUSD=X`) and multiplied by shares to get its value over time.
3. Holding values are summed to create the portfolio value series.
4. Daily returns are used to calculate volatility, Sharpe ratio and drawdown.
5. The portfolio and the selected benchmark are both rebased to 100 for comparison.

## Metrics Explained
1. Annualized volatility: standard deviation of daily portfolio returns × √252
2. Sharpe ratio: (annualized return − risk-free rate) ÷ annualized volatility. The default risk-free rate is 4% and can be changed in the sidebar.
3. Max drawdown: largest peak-to-trough decline in portfolio value over the selected window
4. P&L / Return %: current value minus cost, where cost = shares × buy price

## Limitations
1. Uses free, delayed data from Yahoo Finance; not suitable for live trading decisions
2. Cost basis is converted at today's FX rate rather than the FX rate on the purchase date
3. The portfolio history starts from the date all holdings have data
4. Does not account for fees, slippage, dividends or taxes
5. Past performance does not predict future results

## Future Improvements
1. Add crypto and commodity futures to the default holdings (for example `BTC-USD`, `GC=F`, `CL=F`)
2. Add position sizing and a risk-per-trade calculator
3. Add rebalancing suggestions and a CSV export of the performance log
4. Add backtesting of simple strategies

## Future Improvements
1. Add backtesting of simple strategies
2. Add position sizing and risk-per-trade calculator
3. Add macro indicators (inflation, interest rates)

