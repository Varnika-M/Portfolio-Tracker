# Portfolio Tracker & Performance Dashboard

An interactive Streamlit dashboard for tracking portfolio performance and risk across crypto (BTC, ETH), commodities (gold, oil) and forex (e.g., USD/INR), using live market data.

## Features
1. Live and historical price data for multiple asset classes via `yfinance`
2. Portfolio value, daily and cumulative returns
3. Risk metrics: volatility, maximum drawdown and Sharpe ratio
4. Asset allocation chart and rebalancing view
5. Correlation heatmap across assets
6. Exportable performance log (CSV)

## Tech Stack
Python, Pandas, NumPy, Streamlit, Plotly, yfinance

## Getting Started
```bash
git clone https://github.com/Varnika-M/portfolio-tracker.git
cd portfolio-tracker
pip install -r requirements.txt
streamlit run app.py
```

## How It Works
1. Enter your holdings (asset and quantity or weight) in the sidebar.
2. The app downloads price history and calculates daily returns.
3. Portfolio-level metrics are computed from weighted asset returns.
4. Charts and tables update automatically when holdings or the date range change.

## Metrics Explained
1. Volatility: annualized standard deviation of daily returns
2. Max Drawdown: largest peak-to-trough decline in portfolio value
3. Sharpe Ratio: return per unit of risk (risk-free rate set to X%)

## Limitations
Uses free, delayed data and is not suitable for live trading decisions
Does not account for fees, slippage or taxes

## Future Improvements
1. Add backtesting of simple strategies
2. Add position sizing and risk-per-trade calculator
3. Add macro indicators (inflation, interest rates)

